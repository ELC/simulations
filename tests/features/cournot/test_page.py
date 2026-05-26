from streamlit.navigation.page import StreamlitPage

from stlite_hello.features.cournot import pages


def test_pages_returns_single_cournot_streamlit_page() -> None:
    streamlit_pages = pages()

    assert len(streamlit_pages) == 1
    assert isinstance(streamlit_pages[0], StreamlitPage)
