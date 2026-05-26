"""Streamlit page wiring for the Sugarscape simulation."""

import streamlit as st
from streamlit.navigation.page import StreamlitPage

from .presentation import render


def pages() -> list[StreamlitPage]:
    return [
        st.Page(
            render,
            title="Sugarscape foraging",
            icon=":material/grass:",
            url_path="sugarscape",
        ),
    ]


__all__ = ["pages"]
