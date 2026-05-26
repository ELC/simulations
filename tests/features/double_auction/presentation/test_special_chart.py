from stlite_hello.features.double_auction import (
    DoubleAuctionConfig,
    SupplyDemandHeading,
    build_supply_demand_chart,
    build_supply_demand_frame,
)

_EXPECTED_LAYERS = 2

_HEADING = SupplyDemandHeading(
    title="S/D cross",
    x_label="Quantity",
    y_label="Price",
    clearing_label="Clearing",
)


def test_build_supply_demand_frame_produces_two_sides(
    double_auction_fast_config: DoubleAuctionConfig,
) -> None:
    frame, clearing = build_supply_demand_frame(
        params=double_auction_fast_config.params,
        seed=double_auction_fast_config.seed,
    )

    sides = set(frame["side"].unique())
    assert sides == {"Demand", "Supply"}
    assert clearing >= 0.0


def test_build_supply_demand_chart_layers_curves_and_clearing_rule(
    double_auction_fast_config: DoubleAuctionConfig,
) -> None:
    frame, clearing = build_supply_demand_frame(
        params=double_auction_fast_config.params,
        seed=double_auction_fast_config.seed,
    )
    chart = build_supply_demand_chart(data=frame, clearing_price=clearing, heading=_HEADING)

    spec = chart.to_dict()

    assert spec["title"] == _HEADING.title
    assert len(spec["layer"]) == _EXPECTED_LAYERS
