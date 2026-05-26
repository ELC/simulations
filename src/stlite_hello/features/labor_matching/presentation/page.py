import streamlit as st
from streamlit.navigation.page import StreamlitPage

from .controller import render


def pages() -> list[StreamlitPage]:
    return [
        st.Page(
            render,
            title="Labor Matching",
            icon=":material/work:",
            url_path="labor_matching",
        ),
    ]
