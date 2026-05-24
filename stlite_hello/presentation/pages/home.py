import streamlit as st


def home_page() -> None:
    st.title("Hello, Stlite!")
    st.caption("A static Streamlit app powered by @stlite/browser and Altair.")

    name = st.text_input("Your name", value="world")
    st.write(f"Hello, **{name}**! Pick a page from the sidebar to explore the demo.")
