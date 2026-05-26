import time
from typing import cast

import streamlit as st

from stlite_hello.analysis import export_filename, serialize_run
from stlite_hello.view_models import RunControlInputs, SimulationOutcome


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
