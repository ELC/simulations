"""Streamlit page wiring for the Kinetic Exchange simulation."""

import streamlit as st
from streamlit.navigation.page import StreamlitPage

from .presentation import render


def pages() -> list[StreamlitPage]:
    return [
        st.Page(
            render,
            title="Kinetic Exchange",
            icon=":material/payments:",
            url_path="kinetic_exchange",
        ),
    ]


__all__ = ["pages"]
