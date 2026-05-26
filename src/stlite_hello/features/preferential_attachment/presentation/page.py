import streamlit as st
from streamlit.navigation.page import StreamlitPage

from .controller import render


def pages() -> list[StreamlitPage]:
    return [
        st.Page(
            render,
            title="Preferential Attachment",
            icon=":material/hub:",
            url_path="preferential_attachment",
        ),
    ]
