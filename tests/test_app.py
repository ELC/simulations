import pytest
from streamlit.testing.v1 import AppTest

from stlite_hello.features import navigation, pages

_EXPECTED_GROUPS = {"Wealth dynamics"}
_EXPECTED_PAGE_COUNT = 1


@pytest.fixture
def stlite_main_app() -> AppTest:
    return AppTest.from_file("src/stlite_hello/app.py")


def test_main_app_renders_without_exception(stlite_main_app: AppTest) -> None:
    stlite_main_app.run(timeout=10)

    assert not stlite_main_app.exception


def test_navigation_exposes_expected_groups_and_pages() -> None:
    groups = navigation()

    assert set(groups) >= _EXPECTED_GROUPS
    total_pages = sum(len(group) for group in groups.values())
    assert total_pages >= _EXPECTED_PAGE_COUNT


def test_pages_helper_flattens_navigation_groups() -> None:
    flat = pages()
    total_grouped = sum(len(group) for group in navigation().values())

    assert len(flat) == total_grouped
