from stlite_hello.features.labor_matching import (
    BeveridgeHeading,
    LaborMatchingConfig,
    build_beveridge_chart,
    build_beveridge_frame,
)

_EXPECTED_LAYERS = 2

_HEADING = BeveridgeHeading(
    title="Beveridge",
    x_label="U",
    y_label="V",
    step_label="t",
)


def test_build_beveridge_frame_has_one_row_per_step(
    labor_matching_fast_config: LaborMatchingConfig,
) -> None:
    frame = build_beveridge_frame(
        params=labor_matching_fast_config.params,
        seed=labor_matching_fast_config.seed,
    )

    assert len(frame) == labor_matching_fast_config.params.n_steps + 1
    assert (frame["unemployment_rate"] >= 0.0).all()


def test_build_beveridge_chart_layers_line_and_points(
    labor_matching_fast_config: LaborMatchingConfig,
) -> None:
    frame = build_beveridge_frame(
        params=labor_matching_fast_config.params,
        seed=labor_matching_fast_config.seed,
    )

    chart = build_beveridge_chart(data=frame, heading=_HEADING)
    spec = chart.to_dict()

    assert spec["title"] == _HEADING.title
    assert len(spec["layer"]) == _EXPECTED_LAYERS
