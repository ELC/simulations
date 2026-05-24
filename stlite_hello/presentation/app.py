import streamlit as st

from stlite_hello.presentation.pages import about_page, charts_page, home_page


def main() -> None:
    st.set_page_config(page_title="Stlite Hello World", layout="wide")

    page = st.navigation(
        [
            st.Page(home_page, title="Home", icon="🏠"),
            st.Page(charts_page, title="Wave charts", icon="📈"),
            st.Page(about_page, title="About", icon="📖"),
        ],
        position="sidebar",
    )
    page.run()


if __name__ == "__main__":
    main()
