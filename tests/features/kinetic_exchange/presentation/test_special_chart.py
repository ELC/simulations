from stlite_hello.analysis import RunBundle
from stlite_hello.features.kinetic_exchange import (
    AdvancedParams,
    KineticExchangeConfig,
    SavingsWealthHeading,
    build_savings_wealth_chart,
    build_savings_wealth_panel,
)

_EXPECTED_LAYERS = 2

_HEADING = SavingsWealthHeading(
    title="Savings vs wealth",
    x_label="lambda",
    y_label="wealth",
    rolling_label="rolling",
)


def test_build_savings_wealth_panel_pairs_each_agent_with_a_savings_rate(
    kinetic_fast_bundle: RunBundle,
    kinetic_fast_config: KineticExchangeConfig,
    kinetic_fast_params: AdvancedParams,
) -> None:
    panel = build_savings_wealth_panel(
        bundle=kinetic_fast_bundle,
        params=kinetic_fast_params,
        seed=kinetic_fast_config.seed,
        runs=kinetic_fast_config.runs,
    )

    expected_rows = kinetic_fast_params.n_agents * kinetic_fast_config.runs
    assert panel.shape[0] == expected_rows
    assert panel["savings_rate"].between(0.0, 1.0).all()
    assert (panel["final_wealth"] >= 0.0).all()


def test_build_savings_wealth_chart_titles_and_axes(
    kinetic_fast_bundle: RunBundle,
    kinetic_fast_config: KineticExchangeConfig,
    kinetic_fast_params: AdvancedParams,
) -> None:
    panel = build_savings_wealth_panel(
        bundle=kinetic_fast_bundle,
        params=kinetic_fast_params,
        seed=kinetic_fast_config.seed,
        runs=kinetic_fast_config.runs,
    )
    chart = build_savings_wealth_chart(panel, _HEADING)

    spec = chart.to_dict()

    assert spec["title"] == _HEADING.title
    assert len(spec["layer"]) == _EXPECTED_LAYERS
