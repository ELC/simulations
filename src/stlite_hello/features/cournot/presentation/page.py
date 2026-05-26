import streamlit as st
from streamlit.navigation.page import StreamlitPage

from .controller import render


def pages() -> list[StreamlitPage]:
    return [
        st.Page(
            render,
            title="Cournot",
            icon=":material/oil_barrel:",
            url_path="cournot",
        ),
    ]
