import pandas as pd

from stlite_hello.analysis import (
    RunBundle,
    SimulationReport,
    run_replicates,
    serialize_run,
    summarize,
)
from stlite_hello.features.kinetic_exchange import (
    KINETIC_FEATURE,
    KineticExchangeConfig,
    simulate_once,
)


def _run_and_summarize(config: KineticExchangeConfig) -> tuple[RunBundle, SimulationReport]:
    bundle = run_replicates(
        simulate_once=simulate_once,
        params=config.params,
        config=config,
    )
    report = summarize(bundle=bundle, config=config)
    return bundle, report


def test_kinetic_exchange_run_with_default_seed_is_deterministic(
    kinetic_fast_config: KineticExchangeConfig,
) -> None:
    first_bundle, first_report = _run_and_summarize(kinetic_fast_config)
    second_bundle, second_report = _run_and_summarize(kinetic_fast_config)

    pd.testing.assert_frame_equal(first_bundle.final_population, second_bundle.final_population)
    pd.testing.assert_frame_equal(first_report.metrics_ci, second_report.metrics_ci)


def test_kinetic_exchange_export_round_trip_is_byte_identical(
    kinetic_fast_config: KineticExchangeConfig,
) -> None:
    bundle, report = _run_and_summarize(kinetic_fast_config)
    first = serialize_run(
        feature=KINETIC_FEATURE,
        config=kinetic_fast_config,
        params=kinetic_fast_config.params,
        bundle=bundle,
        report=report,
    )
    second = serialize_run(
        feature=KINETIC_FEATURE,
        config=kinetic_fast_config,
        params=kinetic_fast_config.params,
        bundle=bundle,
        report=report,
    )

    assert first == second
