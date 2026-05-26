"""Tests for the shared run-control helper.

Exercises both the idle path (no click → ``None`` returned, idle message
rendered) and the clicked path (run + cached outcome + elapsed caption).
We drive Streamlit via :class:`streamlit.testing.v1.AppTest` so the
assertions reflect real session-state behaviour rather than mocked widgets.
"""

import numpy as np
import pandas as pd
from pandera.typing import DataFrame
from streamlit.testing.v1 import AppTest

from stlite_hello.analysis import (
    AggregationConfig,
    DistributionFit,
    FittedDensity,
    KDECurve,
    LorenzCurve,
    MetricCI,
    MetricCIOverTime,
    RunBundle,
    SimulationReport,
    TopPctSpell,
)
from stlite_hello.analysis.schemas import DecileTransition, FinalPopulation, FocalPanel
from stlite_hello.presentation import DownloadHeading, RunControlInputs, RunControlLabels

_FEATURE = "runner_test"
_BUTTON_KEY = f"run_outcome::{_FEATURE}::button"
_SCRIPT = (
    "from tests.presentation.test_runner import build_fake_run_inputs\n"
    "from stlite_hello.presentation import render_run_control\n"
    "import streamlit as st\n"
    "outcome = render_run_control(build_fake_run_inputs())\n"
    "st.write('rendered_outcome=' + ('yes' if outcome is not None else 'no'))\n"
)


def _empty_metric_trajectories() -> DataFrame[MetricCIOverTime]:
    return DataFrame[MetricCIOverTime](
        pd.DataFrame(
            {
                "metric": pd.Series([], dtype="object"),
                "step": pd.Series([], dtype="int64"),
                "estimate": pd.Series([], dtype="float64"),
                "ci_low": pd.Series([], dtype="float64"),
                "ci_high": pd.Series([], dtype="float64"),
                "family": pd.Series([], dtype="object"),
            },
        ),
    )


def _empty_fitted_densities() -> DataFrame[FittedDensity]:
    return DataFrame[FittedDensity](
        pd.DataFrame(
            {
                "name": pd.Series([], dtype="object"),
                "x": pd.Series([], dtype="float64"),
                "density": pd.Series([], dtype="float64"),
            },
        ),
    )


def _empty_spells() -> DataFrame[TopPctSpell]:
    return DataFrame[TopPctSpell](
        pd.DataFrame(
            {
                "run": pd.Series([], dtype="int64"),
                "agent": pd.Series([], dtype="int64"),
                "spell": pd.Series([], dtype="int64"),
                "duration": pd.Series([], dtype="int64"),
                "censored": pd.Series([], dtype="bool"),
            },
        ),
    )


def _identity_decile_transitions() -> DataFrame[DecileTransition]:
    return DataFrame[DecileTransition](
        pd.DataFrame(
            {
                "from_decile": np.repeat(np.arange(1, 11, dtype=np.int64), 10),
                "to_decile": np.tile(np.arange(1, 11, dtype=np.int64), 10),
                "probability": np.zeros(100, dtype=np.float64),
            },
        ),
    )


def _fake_bundle() -> RunBundle:
    panel = np.array([[1.0, 2.0]], dtype=np.float64)
    return RunBundle(
        final_population=DataFrame[FinalPopulation](
            pd.DataFrame(
                {
                    "run": pd.Series([0, 0], dtype="int64"),
                    "agent": pd.Series([0, 1], dtype="int64"),
                    "value": pd.Series([1.0, 2.0], dtype="float64"),
                },
            ),
        ),
        focal_panel=DataFrame[FocalPanel](
            pd.DataFrame(
                {
                    "run": pd.Series([0, 0], dtype="int64"),
                    "step": pd.Series([0, 0], dtype="int64"),
                    "agent": pd.Series([0, 1], dtype="int64"),
                    "value": pd.Series([1.0, 2.0], dtype="float64"),
                },
            ),
        ),
        panels=(panel,),
        step_indices=(np.array([0], dtype=np.int_),),
    )


def _fake_report() -> SimulationReport:
    return SimulationReport(
        metrics_ci=DataFrame[MetricCI](
            pd.DataFrame(
                {
                    "metric": ["gini"],
                    "estimate": [0.1],
                    "ci_low": [0.0],
                    "ci_high": [0.2],
                    "standard_error": [0.05],
                    "confidence_level": [0.95],
                    "family": ["concentration"],
                },
            ),
        ),
        metrics_ci_over_time=_empty_metric_trajectories(),
        lorenz=DataFrame[LorenzCurve](
            pd.DataFrame({"population_share": [0.0, 1.0], "value_share": [0.0, 1.0]}),
        ),
        kde=DataFrame[KDECurve](pd.DataFrame({"x": [0.0, 1.0], "density": [0.0, 0.0]})),
        fits=DataFrame[DistributionFit](
            pd.DataFrame(
                {
                    "name": ["norm"],
                    "params_json": ["[]"],
                    "loglik": [0.0],
                    "aic": [0.0],
                    "delta_aic": [0.0],
                    "rank": pd.Series([1], dtype="int64"),
                },
            ),
        ),
        fitted_densities=_empty_fitted_densities(),
        decile_transitions=_identity_decile_transitions(),
        top_pct_spells=_empty_spells(),
    )


def build_fake_run_inputs() -> RunControlInputs:
    """Construct deterministic ``RunControlInputs`` for the AppTest script."""
    bundle = _fake_bundle()
    report = _fake_report()
    config = AggregationConfig(seed=7, runs=1, bootstrap_resamples=200, trajectory_step_samples=2)
    return RunControlInputs(
        feature=_FEATURE,
        config=config,
        params=config,
        run=lambda: bundle,
        summarize=lambda _: report,
        labels=RunControlLabels(
            run_button="Go",
            idle_message="Idle here.",
            spinner_template="Running {runs} replicates",
            elapsed_template="Done in {elapsed:.3f}s across {runs} replicates.",
        ),
        download=DownloadHeading(label="Download JSON", help="Download the run as JSON."),
    )


def test_render_run_control_returns_none_until_button_is_clicked() -> None:
    test = AppTest.from_string(_SCRIPT)

    test.run(timeout=10)

    assert not test.exception
    assert any("Idle here." in block.value for block in test.info)
    assert any("rendered_outcome=no" in block.value for block in test.markdown)


def test_render_run_control_renders_download_button_disabled_when_idle() -> None:
    test = AppTest.from_string(_SCRIPT)

    test.run(timeout=10)

    assert not test.exception
    downloads = test.get("download_button")
    assert len(downloads) == 1
    assert downloads[0].proto.disabled is True
    assert downloads[0].proto.label == "Download JSON"


def test_render_run_control_caches_outcome_and_emits_elapsed_caption() -> None:
    test = AppTest.from_string(_SCRIPT)
    test.run(timeout=10)
    test.button(key=_BUTTON_KEY).click()

    test.run(timeout=30)

    assert not test.exception
    captions = [block.value for block in test.caption]
    assert any("Done in" in cap and "replicates." in cap for cap in captions)
    assert any("rendered_outcome=yes" in block.value for block in test.markdown)


def test_render_run_control_enables_download_after_run_completes() -> None:
    test = AppTest.from_string(_SCRIPT)
    test.run(timeout=10)
    test.button(key=_BUTTON_KEY).click()

    test.run(timeout=30)

    assert not test.exception
    downloads = test.get("download_button")
    assert len(downloads) == 1
    assert downloads[0].proto.disabled is False
    assert downloads[0].proto.label == "Download JSON"
