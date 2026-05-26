from streamlit.navigation.page import StreamlitPage

from stlite_hello.features.preferential_attachment import pages


def test_pages_returns_single_preferential_attachment_streamlit_page() -> None:
    streamlit_pages = pages()

    assert len(streamlit_pages) == 1
    assert isinstance(streamlit_pages[0], StreamlitPage)
