import streamlit as st

from .charts import (
    ZipfHeading,
    build_zipf_chart,
    build_zipf_frame,
)
from .model import (
    PREFERENTIAL_ATTACHMENT_DEFAULT_ATTACHMENTS,
    PREFERENTIAL_ATTACHMENT_DEFAULT_INITIAL_CLIQUE,
    PREFERENTIAL_ATTACHMENT_DEFAULT_NODES,
    PREFERENTIAL_ATTACHMENT_DEFAULT_SEED,
    PREFERENTIAL_ATTACHMENT_FEATURE,
    AdvancedParams,
    PreferentialAttachmentConfig,
    SimpleParams,
)
from .presentation import (
    SidebarInputs,
    SpecialChartInputs,
    build_config,
    pages,
    render,
    render_special_chart,
)
from .schemas import ZipfData
from .simulation import final_graph, simulate_once
from .view_models import (
    PREFERENTIAL_ATTACHMENT_COPY,
    PREFERENTIAL_ATTACHMENT_SPECIAL_HEADING,
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
    "SidebarInputs",
    "SimpleParams",
    "SpecialChartInputs",
    "ZipfData",
    "ZipfHeading",
    "build_config",
    "build_zipf_chart",
    "build_zipf_frame",
    "final_graph",
    "main",
    "pages",
    "render",
    "render_special_chart",
    "simulate_once",
]
