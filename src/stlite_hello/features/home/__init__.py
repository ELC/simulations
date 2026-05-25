import streamlit as st
from streamlit.navigation.page import StreamlitPage

from .page import home_page
from .page import pages as page_pages


def pages() -> list[StreamlitPage]:
    return list(page_pages())


def main() -> None:
    st.set_page_config(page_title="Stlite Hello — Home", layout="wide")
    page = st.navigation(pages(), position="sidebar")
    page.run()


__all__ = [
    "home_page",
    "main",
    "pages",
]
