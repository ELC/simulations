"""Streamlit page wiring for the Double Auction simulation."""

import streamlit as st
from streamlit.navigation.page import StreamlitPage

from .presentation import render


def pages() -> list[StreamlitPage]:
    return [
        st.Page(
            render,
            title="Double Auction",
            icon=":material/storefront:",
            url_path="double_auction",
        ),
    ]


__all__ = ["pages"]
