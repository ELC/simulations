import streamlit as st


def about_page() -> None:
    st.title("About this demo")
    st.markdown(
        """
This is a multipage [Stlite](https://stlite.net/) app: Streamlit running in the
browser via Pyodide, packaged for static hosting on GitHub Pages.

- **Home** — a simple greeting with a text input.
- **Wave charts** — sliders drive an Altair sine wave; chart logic lives in
  `stlite_hello.charts`, separate from this presentation layer.
- **About** — you are here.

Navigation passes callable page functions to `st.navigation` in
`presentation/app.py`. The same layout works locally with `streamlit run` and in
the browser build under `_site/`.
""",
    )
