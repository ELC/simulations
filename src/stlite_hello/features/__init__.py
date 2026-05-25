from streamlit.navigation.page import StreamlitPage

from .about import pages as about_pages
from .charts import pages as charts_pages
from .home import pages as home_pages


def pages() -> list[StreamlitPage]:
    return [*home_pages(), *charts_pages(), *about_pages()]


__all__ = ["pages"]
