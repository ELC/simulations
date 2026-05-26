"""Streamlit page wiring for the labor-matching simulation."""

import streamlit as st
from streamlit.navigation.page import StreamlitPage

from .presentation import render


def pages() -> list[StreamlitPage]:
    return [
        st.Page(
            render,
            title="Labor matching",
            icon=":material/work:",
            url_path="labor-matching",
        ),
    ]


__all__ = ["pages"]
