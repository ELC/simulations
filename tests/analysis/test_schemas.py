import pandas as pd
import pytest
from pandera.errors import SchemaError
from pandera.typing import DataFrame

from stlite_hello.analysis import (
    DecileTransition,
    DistributionFit,
    FinalPopulation,
    FittedDensity,
    FocalPanel,
    KDECurve,
    LorenzCurve,
    MetricCI,
    MetricCIOverTime,
    ReplicateLong,
    TopPctSpell,
)


def test_replicate_long_accepts_valid_frame() -> None:
    frame = pd.DataFrame(
        {
            "run": pd.Series([0, 1], dtype="int64"),
            "step": pd.Series([0, 1], dtype="int64"),
            "metric": ["gini", "gini"],
            "value": pd.Series([0.1, 0.2], dtype="float64"),
        },
    )

    assert isinstance(DataFrame[ReplicateLong](frame), pd.DataFrame)


def test_final_population_rejects_negative_value() -> None:
    frame = pd.DataFrame(
        {
            "run": pd.Series([0], dtype="int64"),
            "agent": pd.Series([0], dtype="int64"),
            "value": pd.Series([-1.0], dtype="float64"),
        },
    )

    with pytest.raises(SchemaError):
        DataFrame[FinalPopulation](frame)


def test_focal_panel_validates_dtypes() -> None:
    frame = pd.DataFrame(
        {
            "run": pd.Series([0], dtype="int64"),
            "step": pd.Series([0], dtype="int64"),
            "agent": pd.Series([0], dtype="int64"),
            "value": pd.Series([1.0], dtype="float64"),
        },
    )

    assert isinstance(DataFrame[FocalPanel](frame), pd.DataFrame)


def test_metric_ci_requires_family_column() -> None:
    frame = pd.DataFrame(
        {
            "metric": ["gini"],
            "estimate": pd.Series([0.5], dtype="float64"),
            "ci_low": pd.Series([0.4], dtype="float64"),
            "ci_high": pd.Series([0.6], dtype="float64"),
            "standard_error": pd.Series([0.01], dtype="float64"),
            "confidence_level": pd.Series([0.95], dtype="float64"),
        },
    )

    with pytest.raises(SchemaError):
        DataFrame[MetricCI](frame)


def test_metric_ci_over_time_accepts_valid_frame() -> None:
    frame = pd.DataFrame(
        {
            "metric": ["gini"],
            "step": pd.Series([0], dtype="int64"),
            "estimate": pd.Series([0.1], dtype="float64"),
            "ci_low": pd.Series([0.05], dtype="float64"),
            "ci_high": pd.Series([0.15], dtype="float64"),
            "family": ["concentration"],
        },
    )

    assert isinstance(DataFrame[MetricCIOverTime](frame), pd.DataFrame)


def test_lorenz_curve_rejects_out_of_range_share() -> None:
    frame = pd.DataFrame(
        {
            "population_share": pd.Series([0.5], dtype="float64"),
            "value_share": pd.Series([1.5], dtype="float64"),
        },
    )

    with pytest.raises(SchemaError):
        DataFrame[LorenzCurve](frame)


def test_kde_curve_rejects_negative_density() -> None:
    frame = pd.DataFrame(
        {
            "x": pd.Series([0.0], dtype="float64"),
            "density": pd.Series([-0.1], dtype="float64"),
        },
    )

    with pytest.raises(SchemaError):
        DataFrame[KDECurve](frame)


def test_distribution_fit_rejects_negative_delta_aic() -> None:
    frame = pd.DataFrame(
        {
            "name": ["norm"],
            "params_json": ["[0.0, 1.0]"],
            "loglik": pd.Series([-100.0], dtype="float64"),
            "aic": pd.Series([200.0], dtype="float64"),
            "delta_aic": pd.Series([-1.0], dtype="float64"),
            "rank": pd.Series([1], dtype="int64"),
        },
    )

    with pytest.raises(SchemaError):
        DataFrame[DistributionFit](frame)


def test_fitted_density_accepts_valid_frame() -> None:
    frame = pd.DataFrame(
        {
            "name": ["norm"],
            "x": pd.Series([0.0], dtype="float64"),
            "density": pd.Series([0.4], dtype="float64"),
        },
    )

    assert isinstance(DataFrame[FittedDensity](frame), pd.DataFrame)


def test_decile_transition_rejects_out_of_range_decile() -> None:
    frame = pd.DataFrame(
        {
            "from_decile": pd.Series([11], dtype="int64"),
            "to_decile": pd.Series([1], dtype="int64"),
            "probability": pd.Series([0.5], dtype="float64"),
        },
    )

    with pytest.raises(SchemaError):
        DataFrame[DecileTransition](frame)


def test_top_pct_spell_requires_minimum_duration() -> None:
    frame = pd.DataFrame(
        {
            "run": pd.Series([0], dtype="int64"),
            "agent": pd.Series([0], dtype="int64"),
            "spell": pd.Series([0], dtype="int64"),
            "duration": pd.Series([0], dtype="int64"),
            "censored": pd.Series([False], dtype="bool"),
        },
    )

    with pytest.raises(SchemaError):
        DataFrame[TopPctSpell](frame)
