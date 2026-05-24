from pathlib import Path

import pytest
from pandera.typing import DataFrame
from streamlit.testing.v1 import AppTest

from stlite_hello.charts import WaveChartParams, WaveData, wave_dataframe
from stlite_hello.site import (
    SITE_SETTINGS,
    Requirements,
    RequirementsAdapter,
    SiteFilePublisher,
    SiteTemplateRenderer,
    main,
)


@pytest.fixture
def stlite_main_app() -> AppTest:
    return AppTest.from_file("stlite_hello/presentation/app.py")


@pytest.fixture
def stlite_charts_page() -> AppTest:
    return AppTest.from_string(
        "from stlite_hello.presentation.pages import charts_page\ncharts_page()\n",
    )


@pytest.fixture
def stlite_about_page() -> AppTest:
    return AppTest.from_string(
        "from stlite_hello.presentation.pages import about_page\nabout_page()\n",
    )


@pytest.fixture
def default_params() -> WaveChartParams:
    return WaveChartParams(waves=3, amplitude=1.0, points=120)


@pytest.fixture
def default_wave_data(default_params: WaveChartParams) -> DataFrame[WaveData]:
    return wave_dataframe(default_params)


@pytest.fixture
def output_dir(tmp_path: Path) -> Path:
    site_output = tmp_path / "_site"
    site_output.mkdir()
    return site_output


@pytest.fixture
def template_renderer() -> SiteTemplateRenderer:
    return SiteTemplateRenderer(jinja_environment=SITE_SETTINGS.jinja_environment)


@pytest.fixture
def browser_requirements() -> Requirements:
    return RequirementsAdapter.validate_python(
        {"requirements": SITE_SETTINGS.project_dependency_specifications},
    )


@pytest.fixture
def file_publisher(
    template_renderer: SiteTemplateRenderer,
    output_dir: Path,
) -> SiteFilePublisher:
    return SiteFilePublisher(
        templates=template_renderer,
        destination=output_dir,
    )


@pytest.fixture
def site_dir(
    output_dir: Path,
    file_publisher: SiteFilePublisher,
    browser_requirements: Requirements,
) -> Path:
    return main(
        output_dir,
        publisher=file_publisher,
        browser_requirements=browser_requirements,
    )
