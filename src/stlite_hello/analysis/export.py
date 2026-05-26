"""Versioned JSON export of a complete simulation run.

The export is round-trippable: ``deserialize_run(serialize_run(...))`` parses
back to the same :class:`SimulationRunExport`, and a second
``serialize_run`` yields byte-identical output. The schema is pinned via
``schema_version`` so future evolution stays explicit.
"""

from datetime import UTC, datetime, timedelta
from typing import Any, Literal

import numpy as np
import pandas as pd
from numpy.typing import NDArray
from pandera.typing import DataFrame
from pydantic import BaseModel, ConfigDict, Field

from .aggregation import RunBundle
from .config import AggregationConfig
from .schemas import (
    DecileTransition,
    DistributionFit,
    FinalPopulation,
    FittedDensity,
    FocalPanel,
    KDECurve,
    LorenzCurve,
    MetricCI,
    MetricCIOverTime,
    TopPctSpell,
)
from .summarize import SimulationReport

_EXPORT_EPOCH = datetime(2026, 1, 1, tzinfo=UTC)


def _panels_from_focal_frame(
    frame: pd.DataFrame,
) -> tuple[tuple[NDArray[np.float64], ...], tuple[NDArray[np.int_], ...]]:
    panels: list[NDArray[np.float64]] = []
    step_indices: list[NDArray[np.int_]] = []
    for run_id in sorted(frame["run"].unique()):
        run_frame = frame[frame["run"] == run_id]
        pivot = run_frame.pivot_table(
            index="step",
            columns="agent",
            values="value",
            aggfunc="first",
        ).sort_index()
        panels.append(pivot.to_numpy(dtype=np.float64))
        step_indices.append(pivot.index.to_numpy(dtype=np.int_))
    return tuple(panels), tuple(step_indices)


class SerializedBundle(BaseModel):
    """``RunBundle`` projected onto records for JSON round-trip."""

    model_config = ConfigDict(frozen=True)

    final_population: list[dict[str, Any]]
    focal_panel: list[dict[str, Any]]


class SerializedReport(BaseModel):
    """``SimulationReport`` projected onto records for JSON round-trip."""

    model_config = ConfigDict(frozen=True)

    metrics_ci: list[dict[str, Any]]
    metrics_ci_over_time: list[dict[str, Any]]
    lorenz: list[dict[str, Any]]
    kde: list[dict[str, Any]]
    fits: list[dict[str, Any]]
    fitted_densities: list[dict[str, Any]]
    decile_transitions: list[dict[str, Any]]
    top_pct_spells: list[dict[str, Any]]


class SimulationRunExport(BaseModel):
    """The complete payload a user downloads from the page."""

    model_config = ConfigDict(frozen=True)

    schema_version: Literal["1"] = "1"
    feature: str = Field(min_length=1)
    generated_at: datetime
    config: AggregationConfig
    params: dict[str, Any]
    bundle: SerializedBundle
    report: SerializedReport

    def to_run_bundle(self) -> RunBundle:
        """Reconstruct the typed RunBundle from the JSON payload.

        Returns
        -------
        RunBundle
            Pandera-validated bundle with the original ``final_population``
            and ``focal_panel`` frames plus the numpy panels rebuilt by
            pivoting the focal panel back into per-replicate matrices.
        """
        focal_frame = pd.DataFrame(self.bundle.focal_panel)
        panels, step_indices = _panels_from_focal_frame(focal_frame)
        return RunBundle(
            final_population=DataFrame[FinalPopulation](pd.DataFrame(self.bundle.final_population)),
            focal_panel=DataFrame[FocalPanel](focal_frame),
            panels=panels,
            step_indices=step_indices,
        )

    def to_simulation_report(self) -> SimulationReport:
        """Reconstruct the typed SimulationReport from the JSON payload.

        Returns
        -------
        SimulationReport
            Fully validated report frames, ready for chart builders.
        """
        return SimulationReport(
            metrics_ci=DataFrame[MetricCI](pd.DataFrame(self.report.metrics_ci)),
            metrics_ci_over_time=DataFrame[MetricCIOverTime](pd.DataFrame(self.report.metrics_ci_over_time)),
            lorenz=DataFrame[LorenzCurve](pd.DataFrame(self.report.lorenz)),
            kde=DataFrame[KDECurve](pd.DataFrame(self.report.kde)),
            fits=DataFrame[DistributionFit](pd.DataFrame(self.report.fits)),
            fitted_densities=DataFrame[FittedDensity](pd.DataFrame(self.report.fitted_densities)),
            decile_transitions=DataFrame[DecileTransition](pd.DataFrame(self.report.decile_transitions)),
            top_pct_spells=DataFrame[TopPctSpell](pd.DataFrame(self.report.top_pct_spells)),
        )


def _generated_at_for(seed: int) -> datetime:
    return _EXPORT_EPOCH + timedelta(seconds=seed)


def build_export(
    *,
    feature: str,
    config: AggregationConfig,
    params: BaseModel,
    bundle: RunBundle,
    report: SimulationReport,
) -> SimulationRunExport:
    """Build the typed export payload for one simulation run.

    Returns
    -------
    SimulationRunExport
        Ready for ``serialize_run`` or direct dict access.
    """
    return SimulationRunExport(
        feature=feature,
        generated_at=_generated_at_for(config.seed),
        config=config,
        params=params.model_dump(mode="json"),
        bundle=SerializedBundle(
            final_population=bundle.final_population.to_dict(orient="records"),
            focal_panel=bundle.focal_panel.to_dict(orient="records"),
        ),
        report=SerializedReport(
            metrics_ci=report.metrics_ci.to_dict(orient="records"),
            metrics_ci_over_time=report.metrics_ci_over_time.to_dict(orient="records"),
            lorenz=report.lorenz.to_dict(orient="records"),
            kde=report.kde.to_dict(orient="records"),
            fits=report.fits.to_dict(orient="records"),
            fitted_densities=report.fitted_densities.to_dict(orient="records"),
            decile_transitions=report.decile_transitions.to_dict(orient="records"),
            top_pct_spells=report.top_pct_spells.to_dict(orient="records"),
        ),
    )


def serialize_run(
    *,
    feature: str,
    config: AggregationConfig,
    params: BaseModel,
    bundle: RunBundle,
    report: SimulationReport,
) -> bytes:
    """Serialize a run as UTF-8 JSON bytes suitable for ``st.download_button``.

    Returns
    -------
    bytes
        Canonical JSON payload (sorted keys for byte-identical round-trip).
    """
    export = build_export(
        feature=feature,
        config=config,
        params=params,
        bundle=bundle,
        report=report,
    )
    return export.model_dump_json().encode("utf-8")


def deserialize_run(payload: bytes) -> SimulationRunExport:
    """Parse and validate a previously serialized run.

    Returns
    -------
    SimulationRunExport
        The same export model produced by :func:`build_export`.
    """
    return SimulationRunExport.model_validate_json(payload.decode("utf-8"))


def export_filename(*, feature: str, config: AggregationConfig) -> str:
    """Return the deterministic filename suggestion for an export.

    Returns
    -------
    str
        e.g. ``yard_sale_seed-1000003_runs-30.json``.
    """
    return f"{feature}_seed-{config.seed}_runs-{config.runs}.json"


__all__ = [
    "SerializedBundle",
    "SerializedReport",
    "SimulationRunExport",
    "build_export",
    "deserialize_run",
    "export_filename",
    "serialize_run",
]
