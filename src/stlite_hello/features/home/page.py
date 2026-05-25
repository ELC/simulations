import streamlit as st
from streamlit.navigation.page import StreamlitPage


def home_page() -> None:
    st.title("Hello, Stlite!")
    st.caption("A static Streamlit app powered by @stlite/browser and Altair.")

    name = st.text_input("Your name", value="world")
    st.write(f"Hello, **{name}**! Pick a page from the sidebar to explore the demo.")


def pages() -> list[StreamlitPage]:
    return [st.Page(home_page, title="Home", icon="🏠")]
