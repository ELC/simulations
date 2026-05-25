import streamlit as st

from stlite_hello.features import pages


def main() -> None:
    st.set_page_config(page_title="Stlite Hello World", layout="wide")
    page = st.navigation(pages(), position="sidebar")
    page.run()


if __name__ == "__main__":
    main()
