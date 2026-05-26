import streamlit as st
from streamlit.navigation.page import StreamlitPage

from .controller import render


def pages() -> list[StreamlitPage]:
    return [
        st.Page(
            render,
            title="Yard-Sale",
            icon=":material/savings:",
            url_path="yard_sale",
        ),
    ]
