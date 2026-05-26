from stlite_hello.features.cournot import (
    BestResponseHeading,
    CournotConfig,
    build_best_response_chart,
    build_trajectory_data,
)

_EXPECTED_LAYERS = 3

_HEADING = BestResponseHeading(
    title="Best response",
    x_label="Firm A",
    y_label="Firm B",
    line_legend_label="BR",
)


def test_build_trajectory_data_emits_one_row_per_step(
    cournot_fast_config: CournotConfig,
) -> None:
    trajectory, lines = build_trajectory_data(
        params=cournot_fast_config.params,
        seed=cournot_fast_config.seed,
    )

    assert len(trajectory) == cournot_fast_config.params.n_steps + 1
    assert set(lines["firm"].unique()) == {"Firm A", "Firm B"}


def test_build_best_response_chart_layers_trace_and_two_lines(
    cournot_fast_config: CournotConfig,
) -> None:
    trajectory, lines = build_trajectory_data(
        params=cournot_fast_config.params,
        seed=cournot_fast_config.seed,
    )

    chart = build_best_response_chart(trajectory=trajectory, lines=lines, heading=_HEADING)
    spec = chart.to_dict()

    assert spec["title"] == _HEADING.title
    assert len(spec["layer"]) == _EXPECTED_LAYERS
