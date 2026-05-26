"""Presentation layer for the preferential-attachment feature."""

from .controller import render
from .sidebar import SidebarInputs, build_config
from .special_chart import (
    SpecialChartInputs,
    ZipfData,
    ZipfHeading,
    build_zipf_chart,
    build_zipf_frame,
    render_special_chart,
)
from .view_models import PREFERENTIAL_ATTACHMENT_COPY, PREFERENTIAL_ATTACHMENT_SPECIAL_HEADING

__all__ = [
    "PREFERENTIAL_ATTACHMENT_COPY",
    "PREFERENTIAL_ATTACHMENT_SPECIAL_HEADING",
    "SidebarInputs",
    "SpecialChartInputs",
    "ZipfData",
    "ZipfHeading",
    "build_config",
    "build_zipf_chart",
    "build_zipf_frame",
    "render",
    "render_special_chart",
]
