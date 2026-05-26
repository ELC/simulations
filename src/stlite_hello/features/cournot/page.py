"""Streamlit page wiring for the Cournot simulation."""

import streamlit as st
from streamlit.navigation.page import StreamlitPage

from .presentation import render


def pages() -> list[StreamlitPage]:
    return [
        st.Page(
            render,
            title="Cournot oligopoly",
            icon=":material/oil_barrel:",
            url_path="cournot",
        ),
    ]


__all__ = ["pages"]
