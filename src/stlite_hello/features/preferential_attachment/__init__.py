"""Preferential attachment growth simulation slice."""

import streamlit as st

from .model import (
    PREFERENTIAL_ATTACHMENT_DEFAULT_ATTACHMENTS,
    PREFERENTIAL_ATTACHMENT_DEFAULT_INITIAL_CLIQUE,
    PREFERENTIAL_ATTACHMENT_DEFAULT_NODES,
    PREFERENTIAL_ATTACHMENT_DEFAULT_SEED,
    PREFERENTIAL_ATTACHMENT_FEATURE,
    AdvancedParams,
    PreferentialAttachmentConfig,
    SimpleParams,
    final_graph,
    simulate_once,
)
from .page import pages
from .presentation import (
    PREFERENTIAL_ATTACHMENT_COPY,
    PREFERENTIAL_ATTACHMENT_SPECIAL_HEADING,
    SpecialChartInputs,
    ZipfData,
    ZipfHeading,
    build_zipf_chart,
    build_zipf_frame,
    render,
    render_special_chart,
)


def main() -> None:
    st.set_page_config(page_title="Preferential attachment", layout="wide")
    page = st.navigation(pages(), position="sidebar")
    page.run()


__all__ = [
    "PREFERENTIAL_ATTACHMENT_COPY",
    "PREFERENTIAL_ATTACHMENT_DEFAULT_ATTACHMENTS",
    "PREFERENTIAL_ATTACHMENT_DEFAULT_INITIAL_CLIQUE",
    "PREFERENTIAL_ATTACHMENT_DEFAULT_NODES",
    "PREFERENTIAL_ATTACHMENT_DEFAULT_SEED",
    "PREFERENTIAL_ATTACHMENT_FEATURE",
    "PREFERENTIAL_ATTACHMENT_SPECIAL_HEADING",
    "AdvancedParams",
    "PreferentialAttachmentConfig",
    "SimpleParams",
    "SpecialChartInputs",
    "ZipfData",
    "ZipfHeading",
    "build_zipf_chart",
    "build_zipf_frame",
    "final_graph",
    "main",
    "pages",
    "render",
    "render_special_chart",
    "simulate_once",
]
