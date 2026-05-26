"""Streamlit page wiring for the preferential-attachment simulation."""

import streamlit as st
from streamlit.navigation.page import StreamlitPage

from .presentation import render


def pages() -> list[StreamlitPage]:
    return [
        st.Page(
            render,
            title="Preferential attachment",
            icon=":material/hub:",
            url_path="preferential-attachment",
        ),
    ]


__all__ = ["pages"]
