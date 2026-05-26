import pytest
from streamlit.testing.v1 import AppTest

from stlite_hello.features import navigation, pages

_EXPECTED_GROUPS = {"Wealth dynamics"}
_EXPECTED_PAGE_COUNT = 1


@pytest.fixture
def stlite_main_app() -> AppTest:
    return AppTest.from_file("src/stlite_hello/app.py")


def test_main_app_renders_without_exception(stlite_main_app: AppTest) -> None:
    stlite_main_app.session_state["yard_sale_runs"] = 2
    stlite_main_app.session_state["yard_sale_trajectory_samples"] = 4
    stlite_main_app.session_state["yard_sale_resamples"] = 200
    stlite_main_app.session_state["yard_sale_simple_agents"] = 12
    stlite_main_app.session_state["yard_sale_simple_steps"] = 20

    stlite_main_app.run(timeout=120)

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
