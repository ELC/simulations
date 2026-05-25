import streamlit as st
from streamlit.navigation.page import StreamlitPage

from .charts import WaveChartParams, WaveData, build_sine_wave_chart, wave_dataframe
from .page import charts_page
from .page import pages as page_pages


def pages() -> list[StreamlitPage]:
    return list(page_pages())


def main() -> None:
    st.set_page_config(page_title="Stlite Hello — Wave charts", layout="wide")
    page = st.navigation(pages(), position="sidebar")
    page.run()


__all__ = [
    "WaveChartParams",
    "WaveData",
    "build_sine_wave_chart",
    "charts_page",
    "main",
    "pages",
    "wave_dataframe",
]
