"""Public feature registry, grouped for sidebar navigation."""

from streamlit.navigation.page import StreamlitPage

from . import cournot, double_auction, kinetic_exchange, sugarscape, yard_sale


def navigation() -> dict[str, list[StreamlitPage]]:
    """Return the grouped navigation dict consumed by ``st.navigation``.

    Returns
    -------
    dict[str, list[StreamlitPage]]
        Mapping from sidebar group label to the list of pages for that group.
    """
    return {
        "Wealth dynamics": [*yard_sale.pages(), *kinetic_exchange.pages(), *sugarscape.pages()],
        "Market structure": [*double_auction.pages(), *cournot.pages()],
    }


def pages() -> list[StreamlitPage]:
    """Return the flat list of pages across every group.

    Returns
    -------
    list[StreamlitPage]
        Every page in every group, in declaration order.
    """
    return [page for group in navigation().values() for page in group]


__all__ = ["navigation", "pages"]
