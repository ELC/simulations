from stlite_hello.features.sugarscape import (
    SpatialHeading,
    SugarscapeConfig,
    build_spatial_chart,
    build_spatial_frames,
)

_EXPECTED_LAYERS = 2

_HEADING = SpatialHeading(
    title="Spatial wealth",
    row_label="Row",
    col_label="Col",
    sugar_label="Sugar",
    agent_label="Wealth",
)


def test_build_spatial_frames_emits_cells_for_every_grid_position(
    sugarscape_fast_config: SugarscapeConfig,
) -> None:
    cells, agents = build_spatial_frames(
        params=sugarscape_fast_config.params,
        seed=sugarscape_fast_config.seed,
    )

    grid = sugarscape_fast_config.params.grid_size
    assert len(cells) == grid * grid
    assert len(agents) == sugarscape_fast_config.params.n_agents


def test_build_spatial_chart_layers_heatmap_and_bubbles(
    sugarscape_fast_config: SugarscapeConfig,
) -> None:
    cells, agents = build_spatial_frames(
        params=sugarscape_fast_config.params,
        seed=sugarscape_fast_config.seed,
    )

    chart = build_spatial_chart(cells=cells, agents=agents, heading=_HEADING)
    spec = chart.to_dict()

    assert spec["title"] == _HEADING.title
    assert len(spec["layer"]) == _EXPECTED_LAYERS
