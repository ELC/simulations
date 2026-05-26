from stlite_hello.analysis import RunBundle
from stlite_hello.features.yard_sale import (
    WealthCondensationHeading,
    aggregate_wealth_condensation,
    build_wealth_condensation_chart,
)

_HEADING = WealthCondensationHeading(
    title="Wealth condensation",
    x_label="step",
    y_label="rank",
    color_label="share",
)


def test_aggregate_wealth_condensation_emits_long_form_per_step_rank(
    yard_sale_fast_bundle: RunBundle,
) -> None:
    aggregated = aggregate_wealth_condensation(yard_sale_fast_bundle.focal_panel)

    assert {"step", "rank", "wealth_share"} <= set(aggregated.columns)
    assert aggregated["rank"].between(1, 40).all()
    assert aggregated["wealth_share"].between(0.0, 1.0).all()


def test_build_wealth_condensation_chart_uses_heatmap_marks(
    yard_sale_fast_bundle: RunBundle,
) -> None:
    aggregated = aggregate_wealth_condensation(yard_sale_fast_bundle.focal_panel)
    chart = build_wealth_condensation_chart(aggregated, _HEADING)

    spec = chart.to_dict()

    assert spec["mark"] == "rect" or spec["mark"]["type"] == "rect"
    assert spec["title"] == _HEADING.title
