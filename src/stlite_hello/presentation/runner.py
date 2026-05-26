"""Gated run-control: button + download toolbar + cached outcome.

Every simulation page renders the same shape: read params from the sidebar,
ask the user to click "Run simulation", then summarise. This helper owns
that loop so the per-feature controllers stay short and consistent.
Outcomes are cached in ``st.session_state`` keyed by feature, so re-renders
triggered by other widgets keep showing the last result without re-running
the simulation.

The toolbar also exposes the per-run JSON download right next to the run
button. The download button stays *disabled* until a run completes, so the
user never sees a stale or empty file.
"""

import time
from collections.abc import Callable
from typing import cast

import streamlit as st
from pydantic import BaseModel, ConfigDict

from stlite_hello.analysis import (
    AggregationConfig,
    RunBundle,
    SimulationReport,
    export_filename,
    serialize_run,
)

from .sections import DownloadHeading


class RunControlLabels(BaseModel):
    """User-facing strings for the run-control widget."""

    model_config = ConfigDict(frozen=True)

    run_button: str
    idle_message: str
    spinner_template: str
    elapsed_template: str


class SimulationOutcome(BaseModel):
    """Result of one completed run, cached across reruns."""

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    bundle: RunBundle
    report: SimulationReport
    elapsed_seconds: float
    config: AggregationConfig
    params: BaseModel


class RunControlInputs(BaseModel):
    """Typed inputs for :func:`render_run_control`."""

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    feature: str
    config: AggregationConfig
    params: BaseModel
    run: Callable[[], RunBundle]
    summarize: Callable[[RunBundle], SimulationReport]
    labels: RunControlLabels
    download: DownloadHeading


def _session_key(feature: str) -> str:
    return f"run_outcome::{feature}"


def _render_toolbar(
    inputs: RunControlInputs,
    *,
    outcome: SimulationOutcome | None,
) -> bool:
    key = _session_key(inputs.feature)
    run_col, download_col = st.columns([1, 1])
    with run_col:
        clicked = st.button(
            inputs.labels.run_button,
            type="primary",
            key=f"{key}::button",
            width="stretch",
        )
    with download_col:
        if outcome is None:
            st.download_button(
                label=inputs.download.label,
                data=b"",
                file_name=export_filename(feature=inputs.feature, config=inputs.config),
                mime=inputs.download.mime,
                help=inputs.download.help,
                disabled=True,
                key=f"{key}::download::idle",
                width="stretch",
            )
        else:
            payload = serialize_run(
                feature=inputs.feature,
                config=outcome.config,
                params=outcome.params,
                bundle=outcome.bundle,
                report=outcome.report,
            )
            st.download_button(
                label=inputs.download.label,
                data=payload,
                file_name=export_filename(feature=inputs.feature, config=outcome.config),
                mime=inputs.download.mime,
                help=inputs.download.help,
                key=f"{key}::download::ready",
                width="stretch",
            )
    return clicked


def render_run_control(inputs: RunControlInputs) -> SimulationOutcome | None:
    """Render the Run/Download toolbar and return the (cached) outcome.

    Returns
    -------
    SimulationOutcome | None
        ``None`` when no run has been requested yet; the latest outcome
        (either freshly computed or cached from a previous click) otherwise.
    """
    key = _session_key(inputs.feature)
    cached = cast("SimulationOutcome | None", st.session_state.get(key))
    clicked = _render_toolbar(inputs, outcome=cached)
    if clicked:
        spinner_msg = inputs.labels.spinner_template.format(runs=inputs.config.runs)
        start = time.perf_counter()
        with st.spinner(spinner_msg):
            bundle = inputs.run()
            report = inputs.summarize(bundle)
        elapsed = time.perf_counter() - start
        st.session_state[key] = SimulationOutcome(
            bundle=bundle,
            report=report,
            elapsed_seconds=elapsed,
            config=inputs.config,
            params=inputs.params,
        )
        st.rerun()
    if cached is None:
        st.info(inputs.labels.idle_message, icon=":material/play_circle:")
        return None
    st.caption(
        inputs.labels.elapsed_template.format(
            elapsed=cached.elapsed_seconds,
            runs=cached.config.runs,
        ),
    )
    return cached


__all__ = [
    "RunControlInputs",
    "RunControlLabels",
    "SimulationOutcome",
    "render_run_control",
]
