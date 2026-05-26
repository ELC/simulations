"""Turn a ``RunBundle`` into the typed ``SimulationReport`` consumed by the UI."""

import json
import operator
from collections.abc import Callable

import numpy as np
import pandas as pd
from numpy.typing import NDArray
from pandera.typing import DataFrame
from pydantic import BaseModel, ConfigDict

from .adapters import (
    BootstrapSettings,
    DistributionName,
    bootstrap_ci,
    fit_distribution,
    gaussian_kde_grid,
    pdf_values,
)
from .aggregation import RunBundle
from .config import AggregationConfig
from .metrics import (
    bottom_to_top_rise_count,
    coefficient_of_variation,
    convergence_half_life,
    decile_transition_matrix,
    gini,
    hill_alpha,
    lorenz_curve,
    mean_tenure_from_spells,
    median_time_to_rise,
    shannon_entropy,
    top_pct_persistence_rate,
    top_pct_spells,
    top_pct_turnover_rate,
    top_share,
)
from .schemas import (
    DecileTransition,
    DistributionFit,
    FittedDensity,
    KDECurve,
    LorenzCurve,
    MetricCI,
    MetricCIOverTime,
    TopPctSpell,
)

_KDE_GRID_SIZE = 200
_MINIMUM_BOOTSTRAP_SAMPLES = 2
_TOP_FRACTION = 0.01
_TOP_FITS_TO_OVERLAY = 3
_CONCENTRATION_FAMILY = "concentration"
_MOBILITY_FAMILY = "mobility"
_DISTRIBUTION_CATALOG: tuple[DistributionName, ...] = (
    "norm",
    "lognorm",
    "expon",
    "pareto",
    "gamma",
    "weibull_min",
)

_Statistic = Callable[[NDArray[np.float64]], float]


class SimulationReport(BaseModel):
    """Everything the presentation layer needs to render a feature's body."""

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    metrics_ci: DataFrame[MetricCI]
    metrics_ci_over_time: DataFrame[MetricCIOverTime]
    lorenz: DataFrame[LorenzCurve]
    kde: DataFrame[KDECurve]
    fits: DataFrame[DistributionFit]
    fitted_densities: DataFrame[FittedDensity]
    decile_transitions: DataFrame[DecileTransition]
    top_pct_spells: DataFrame[TopPctSpell]


def _panel_for_run(bundle: RunBundle, *, run: int) -> NDArray[np.float64]:
    rows = bundle.focal_panel[bundle.focal_panel["run"] == run]
    steps = sorted(rows["step"].unique())
    n_agents = int(rows["agent"].max() + 1)
    panel = np.zeros((len(steps), n_agents), dtype=np.float64)
    step_to_index = {int(step): idx for idx, step in enumerate(steps)}
    for _, row in rows.iterrows():
        panel[step_to_index[int(row["step"])], int(row["agent"])] = float(row["value"])
    return panel


def _final_per_run(bundle: RunBundle) -> list[NDArray[np.float64]]:
    final = bundle.final_population
    return [
        final[final["run"] == run].sort_values("agent")["value"].to_numpy(dtype=np.float64)
        for run in sorted(final["run"].unique())
    ]


def _panels_per_run(bundle: RunBundle) -> list[NDArray[np.float64]]:
    return [_panel_for_run(bundle, run=int(run)) for run in sorted(bundle.focal_panel["run"].unique())]


def _bootstrap_mean(
    values: NDArray[np.float64],
    *,
    seed: int,
    config: AggregationConfig,
) -> tuple[float, float, float, float]:
    if values.size < _MINIMUM_BOOTSTRAP_SAMPLES or np.allclose(values, values[0]):
        estimate = float(np.mean(values)) if values.size > 0 else 0.0
        return estimate, estimate, estimate, 0.0
    settings = BootstrapSettings(
        n_resamples=config.bootstrap_resamples,
        confidence_level=config.confidence_level,
        method=config.bootstrap_method,
        seed=seed,
    )
    result = bootstrap_ci(
        values,
        statistic=lambda data: float(np.mean(data)),
        settings=settings,
    )
    return result.estimate, result.ci_low, result.ci_high, result.standard_error


def _per_run(
    final_per_run: list[NDArray[np.float64]],
    statistic: _Statistic,
) -> NDArray[np.float64]:
    return np.array([statistic(arr) for arr in final_per_run], dtype=np.float64)


def _half_life_per_run(panels: list[NDArray[np.float64]]) -> NDArray[np.float64]:
    values: list[float] = []
    for panel in panels:
        trajectory = np.array([gini(panel[step, :]) for step in range(panel.shape[0])], dtype=np.float64)
        values.append(
            convergence_half_life(trajectory, initial=gini(panel[0, :]), final=gini(panel[-1, :])),
        )
    return np.array(values, dtype=np.float64)


def _mean_tenure_per_run(panels: list[NDArray[np.float64]]) -> NDArray[np.float64]:
    return np.array(
        [
            mean_tenure_from_spells(top_pct_spells(panel, run_index=idx)).mean_lifetime
            for idx, panel in enumerate(panels)
        ],
        dtype=np.float64,
    )


def _concentration_pairs(
    final_per_run: list[NDArray[np.float64]],
    panels: list[NDArray[np.float64]],
) -> list[tuple[str, NDArray[np.float64]]]:
    return [
        ("gini", _per_run(final_per_run, gini)),
        ("top_1pct_share", _per_run(final_per_run, lambda v: top_share(v, fraction=_TOP_FRACTION))),
        ("hill_alpha", _per_run(final_per_run, hill_alpha)),
        ("coefficient_of_variation", _per_run(final_per_run, coefficient_of_variation)),
        ("shannon_entropy", _per_run(final_per_run, shannon_entropy)),
        ("convergence_half_life", _half_life_per_run(panels)),
    ]


def _mobility_pairs(panels: list[NDArray[np.float64]]) -> list[tuple[str, NDArray[np.float64]]]:
    return [
        ("top_1pct_turnover", np.array([top_pct_turnover_rate(p) for p in panels], dtype=np.float64)),
        ("top_1pct_persistence", np.array([top_pct_persistence_rate(p) for p in panels], dtype=np.float64)),
        ("mean_top_1pct_tenure", _mean_tenure_per_run(panels)),
        ("bottom_to_top_rise_count", np.array([bottom_to_top_rise_count(p) for p in panels], dtype=np.float64)),
        ("median_time_to_rise", np.array([median_time_to_rise(p) for p in panels], dtype=np.float64)),
    ]


def _metric_row(
    *,
    name: str,
    values: NDArray[np.float64],
    seed: int,
    family: str,
    config: AggregationConfig,
) -> dict[str, str | float]:
    estimate, lo, hi, se = _bootstrap_mean(values, seed=seed, config=config)
    return {
        "metric": name,
        "estimate": estimate,
        "ci_low": lo,
        "ci_high": hi,
        "standard_error": se,
        "confidence_level": config.confidence_level,
        "family": family,
    }


def _build_metrics_ci(
    *,
    final_per_run: list[NDArray[np.float64]],
    panels_per_run: list[NDArray[np.float64]],
    config: AggregationConfig,
) -> DataFrame[MetricCI]:
    rows: list[dict[str, str | float]] = []
    for offset, (name, values) in enumerate(_concentration_pairs(final_per_run, panels_per_run)):
        rows.append(
            _metric_row(
                name=name, values=values, seed=config.seed + offset, family=_CONCENTRATION_FAMILY, config=config
            ),
        )
    for offset, (name, values) in enumerate(_mobility_pairs(panels_per_run)):
        rows.append(
            _metric_row(
                name=name, values=values, seed=config.seed + 100 + offset, family=_MOBILITY_FAMILY, config=config
            ),
        )
    frame = pd.DataFrame(
        rows,
        columns=["metric", "estimate", "ci_low", "ci_high", "standard_error", "confidence_level", "family"],
    )
    return DataFrame[MetricCI](frame)


def _turnover_between_steps(panel: NDArray[np.float64], *, step: int) -> float:
    n_agents = panel.shape[1]
    k = max(1, int(np.ceil(n_agents * _TOP_FRACTION)))
    current_top = set(np.argpartition(panel[step, :], -k)[-k:])
    next_top = set(np.argpartition(panel[step + 1, :], -k)[-k:])
    return 1.0 - len(current_top & next_top) / k


def _snapshot_steps(panels: list[NDArray[np.float64]], *, samples: int) -> NDArray[np.int_]:
    n_steps = panels[0].shape[0]
    actual = min(samples, n_steps)
    return np.linspace(0, n_steps - 1, num=actual, dtype=np.int_)


class _ConcentrationTrajectorySpec(BaseModel):
    """Inputs for a single concentration trajectory row."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    metric: str
    statistic: _Statistic
    step: int
    panels: list[NDArray[np.float64]]
    seed: int


def _concentration_trajectory_row(
    *,
    spec: _ConcentrationTrajectorySpec,
    config: AggregationConfig,
) -> dict[str, str | int | float]:
    values = np.array([spec.statistic(panel[spec.step, :]) for panel in spec.panels], dtype=np.float64)
    estimate, lo, hi, _ = _bootstrap_mean(values, seed=spec.seed, config=config)
    return {
        "metric": spec.metric,
        "step": spec.step,
        "estimate": estimate,
        "ci_low": lo,
        "ci_high": hi,
        "family": _CONCENTRATION_FAMILY,
    }


def _mobility_trajectory_rows(
    *,
    step: int,
    panels: list[NDArray[np.float64]],
    config: AggregationConfig,
) -> list[dict[str, str | int | float]]:
    values = np.array([_turnover_between_steps(p, step=step) for p in panels], dtype=np.float64)
    estimate, lo, hi, _ = _bootstrap_mean(values, seed=config.seed + 300 + step, config=config)
    return [
        {
            "metric": "top_1pct_turnover",
            "step": step,
            "estimate": estimate,
            "ci_low": lo,
            "ci_high": hi,
            "family": _MOBILITY_FAMILY,
        },
        {
            "metric": "top_1pct_persistence",
            "step": step,
            "estimate": 1.0 - estimate,
            "ci_low": 1.0 - hi,
            "ci_high": 1.0 - lo,
            "family": _MOBILITY_FAMILY,
        },
    ]


def _empty_metrics_over_time() -> DataFrame[MetricCIOverTime]:
    return DataFrame[MetricCIOverTime](
        pd.DataFrame(
            {"metric": [], "step": [], "estimate": [], "ci_low": [], "ci_high": [], "family": []},
        ).astype({"step": "int64", "estimate": "float64", "ci_low": "float64", "ci_high": "float64"}),
    )


def _concentration_statistics() -> dict[str, _Statistic]:
    return {
        "gini": gini,
        "top_1pct_share": lambda v: top_share(v, fraction=_TOP_FRACTION),
        "hill_alpha": hill_alpha,
        "coefficient_of_variation": coefficient_of_variation,
        "shannon_entropy": shannon_entropy,
    }


def _build_metrics_ci_over_time(
    *,
    panels_per_run: list[NDArray[np.float64]],
    config: AggregationConfig,
) -> DataFrame[MetricCIOverTime]:
    if not panels_per_run:
        return _empty_metrics_over_time()
    snapshot_steps = _snapshot_steps(panels_per_run, samples=config.trajectory_step_samples)
    rows: list[dict[str, str | int | float]] = []
    seed_offset = 0
    for metric_name, statistic in _concentration_statistics().items():
        for step in snapshot_steps:
            rows.append(
                _concentration_trajectory_row(
                    spec=_ConcentrationTrajectorySpec(
                        metric=metric_name,
                        statistic=statistic,
                        step=int(step),
                        panels=panels_per_run,
                        seed=config.seed + 200 + seed_offset,
                    ),
                    config=config,
                ),
            )
            seed_offset += 1

    transition_steps = snapshot_steps[snapshot_steps < panels_per_run[0].shape[0] - 1]
    for step in transition_steps:
        rows.extend(
            _mobility_trajectory_rows(step=int(step), panels=panels_per_run, config=config),
        )
    frame = pd.DataFrame(rows, columns=["metric", "step", "estimate", "ci_low", "ci_high", "family"])
    frame["step"] = frame["step"].astype("int64")
    for column in ("estimate", "ci_low", "ci_high"):
        frame[column] = frame[column].astype("float64")
    return DataFrame[MetricCIOverTime](frame)


def _empty_fits_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "name": list(_DISTRIBUTION_CATALOG),
            "params_json": ["[]"] * len(_DISTRIBUTION_CATALOG),
            "loglik": [0.0] * len(_DISTRIBUTION_CATALOG),
            "aic": [0.0] * len(_DISTRIBUTION_CATALOG),
            "delta_aic": [0.0] * len(_DISTRIBUTION_CATALOG),
            "rank": list(range(1, len(_DISTRIBUTION_CATALOG) + 1)),
        },
    )


def _empty_densities_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "name": pd.Series([], dtype="object"),
            "x": pd.Series([], dtype="float64"),
            "density": pd.Series([], dtype="float64"),
        },
    )


def _empty_fits_payload() -> tuple[DataFrame[DistributionFit], DataFrame[FittedDensity]]:
    return (
        DataFrame[DistributionFit](_empty_fits_frame()),
        DataFrame[FittedDensity](_empty_densities_frame()),
    )


def _build_fits_and_densities(
    pooled: NDArray[np.float64],
    *,
    kde: DataFrame[KDECurve],
) -> tuple[DataFrame[DistributionFit], DataFrame[FittedDensity]]:
    if pooled.size < _MINIMUM_BOOTSTRAP_SAMPLES or not pooled.sum():
        return _empty_fits_payload()
    positives = pooled[pooled > 0.0]
    fit_input = positives if positives.size >= _MINIMUM_BOOTSTRAP_SAMPLES else pooled
    if not float(np.var(fit_input)):
        return _empty_fits_payload()
    raw_fits = []
    for name in _DISTRIBUTION_CATALOG:
        fitted = fit_distribution(fit_input, name=name)
        aic = 2 * len(fitted.params) - 2 * fitted.loglik
        raw_fits.append((name, fitted, aic))
    raw_fits.sort(key=operator.itemgetter(2))
    min_aic = raw_fits[0][2]
    fits_rows: list[dict[str, str | float | int]] = [
        {
            "name": name,
            "params_json": json.dumps(list(fitted.params)),
            "loglik": fitted.loglik,
            "aic": aic,
            "delta_aic": aic - min_aic,
            "rank": rank,
        }
        for rank, (name, fitted, aic) in enumerate(raw_fits, start=1)
    ]
    fits_frame = pd.DataFrame(fits_rows)
    fits_frame["rank"] = fits_frame["rank"].astype("int64")
    fits_df = DataFrame[DistributionFit](fits_frame)

    grid = kde["x"].to_numpy(dtype=np.float64)
    density_rows: list[dict[str, str | float]] = [
        {"name": name, "x": float(x_value), "density": max(0.0, float(density_value))}
        for name, fitted, _ in raw_fits[:_TOP_FITS_TO_OVERLAY]
        for x_value, density_value in zip(grid, pdf_values(fitted, grid), strict=True)
    ]
    densities_frame = pd.DataFrame(density_rows, columns=["name", "x", "density"])
    densities_frame["density"] = densities_frame["density"].astype("float64")
    densities_frame["x"] = densities_frame["x"].astype("float64")
    return fits_df, DataFrame[FittedDensity](densities_frame)


def _build_kde(pooled: NDArray[np.float64]) -> DataFrame[KDECurve]:
    if pooled.size < _MINIMUM_BOOTSTRAP_SAMPLES or not float(np.var(pooled)):
        single_value = float(pooled[0]) if pooled.size > 0 else 0.0
        grid = np.linspace(single_value - 1.0, single_value + 1.0, _KDE_GRID_SIZE, dtype=np.float64)
        density = np.zeros_like(grid)
        return DataFrame[KDECurve](pd.DataFrame({"x": grid, "density": density}))
    kde = gaussian_kde_grid(pooled, grid_size=_KDE_GRID_SIZE)
    frame = pd.DataFrame({"x": kde.x, "density": np.maximum(0.0, kde.density)})
    return DataFrame[KDECurve](frame)


def _build_decile_transitions(panels: list[NDArray[np.float64]]) -> DataFrame[DecileTransition]:
    if not panels:
        empty = pd.DataFrame(
            {
                "from_decile": np.repeat(np.arange(1, 11, dtype=np.int64), 10),
                "to_decile": np.tile(np.arange(1, 11, dtype=np.int64), 10),
                "probability": np.zeros(100, dtype=np.float64),
            },
        )
        return DataFrame[DecileTransition](empty)
    aggregated = np.zeros((10, 10), dtype=np.float64)
    for panel in panels:
        per_run = decile_transition_matrix(panel)
        for _, row in per_run.iterrows():
            aggregated[int(row["from_decile"]) - 1, int(row["to_decile"]) - 1] += float(row["probability"])
    aggregated /= max(1, len(panels))
    from_grid, to_grid = np.meshgrid(
        np.arange(1, 11, dtype=np.int64),
        np.arange(1, 11, dtype=np.int64),
        indexing="ij",
    )
    frame = pd.DataFrame(
        {
            "from_decile": from_grid.ravel(),
            "to_decile": to_grid.ravel(),
            "probability": aggregated.ravel(),
        },
    )
    return DataFrame[DecileTransition](frame)


def _build_pooled_spells(panels: list[NDArray[np.float64]]) -> DataFrame[TopPctSpell]:
    pieces = [top_pct_spells(panel, run_index=run_idx) for run_idx, panel in enumerate(panels)]
    if not pieces:
        empty = pd.DataFrame(
            {
                "run": pd.Series([], dtype="int64"),
                "agent": pd.Series([], dtype="int64"),
                "spell": pd.Series([], dtype="int64"),
                "duration": pd.Series([], dtype="int64"),
                "censored": pd.Series([], dtype="bool"),
            },
        )
        return DataFrame[TopPctSpell](empty)
    return DataFrame[TopPctSpell](pd.concat(pieces, ignore_index=True))


def summarize(*, bundle: RunBundle, config: AggregationConfig) -> SimulationReport:
    final_per_run = _final_per_run(bundle)
    panels_per_run = _panels_per_run(bundle)
    pooled_final = np.concatenate(final_per_run) if final_per_run else np.zeros(0, dtype=np.float64)

    kde = _build_kde(pooled_final)
    fits, fitted_densities = _build_fits_and_densities(pooled_final, kde=kde)

    return SimulationReport(
        metrics_ci=_build_metrics_ci(
            final_per_run=final_per_run,
            panels_per_run=panels_per_run,
            config=config,
        ),
        metrics_ci_over_time=_build_metrics_ci_over_time(
            panels_per_run=panels_per_run,
            config=config,
        ),
        lorenz=lorenz_curve(pooled_final),
        kde=kde,
        fits=fits,
        fitted_densities=fitted_densities,
        decile_transitions=_build_decile_transitions(panels_per_run),
        top_pct_spells=_build_pooled_spells(panels_per_run),
    )


__all__ = ["SimulationReport", "summarize"]
