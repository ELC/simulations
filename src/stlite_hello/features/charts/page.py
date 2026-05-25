import streamlit as st
from streamlit.navigation.page import StreamlitPage

from .charts import WaveChartParams, build_sine_wave_chart, wave_dataframe


def charts_page() -> None:
    st.title("Wave charts")
    st.caption("Interactive Altair charts backed by presentation-agnostic chart logic.")

    waves = st.slider("Wave cycles", min_value=1, max_value=10, value=3)
    amplitude = st.slider("Amplitude", min_value=0.1, max_value=2.0, value=1.0)

    params = WaveChartParams(waves=waves, amplitude=amplitude)
    wave_data = wave_dataframe(params)
    chart = build_sine_wave_chart(wave_data, params=params)
    st.altair_chart(chart, width="stretch")


def pages() -> list[StreamlitPage]:
    return [st.Page(charts_page, title="Wave charts", icon="📈")]
