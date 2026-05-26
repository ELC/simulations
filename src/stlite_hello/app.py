import streamlit as st

from stlite_hello.features import navigation


def main() -> None:
    st.set_page_config(page_title="Free-market simulations", layout="wide")
    page = st.navigation(navigation(), position="sidebar")
    page.run()


if __name__ == "__main__":
    main()
