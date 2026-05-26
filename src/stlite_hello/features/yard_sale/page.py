"""Streamlit page wiring for the Yard-Sale simulation."""

import streamlit as st
from streamlit.navigation.page import StreamlitPage

from .presentation import render


def pages() -> list[StreamlitPage]:
    return [
        st.Page(
            render,
            title="Yard-Sale",
            icon=":material/savings:",
            url_path="yard_sale",
        ),
    ]


__all__ = ["pages"]
