import streamlit as st
from streamlit.navigation.page import StreamlitPage


def about_page() -> None:
    st.title("About this demo")
    st.markdown(
        """
This is a multipage [Stlite](https://stlite.net/) app: Streamlit running in the
browser via Pyodide, packaged for static hosting on GitHub Pages.

The app is organised as **vertical slices** under `stlite_hello.features`:

- **Home** — a simple greeting with a text input.
- **Wave charts** — sliders drive an Altair sine wave; chart logic lives in
  `stlite_hello.features.charts.charts`, alongside the page that consumes it.
- **About** — you are here.

Each feature exposes its own `pages()` list. `stlite_hello.app` calls
`stlite_hello.features.pages()`, which merges every slice, and hands the
resulting `list[StreamlitPage]` to `st.navigation`. Each feature is also runnable on
its own via `poe dev-feature <name>`.
""",
    )


def pages() -> list[StreamlitPage]:
    return [st.Page(about_page, title="About", icon="📖")]
