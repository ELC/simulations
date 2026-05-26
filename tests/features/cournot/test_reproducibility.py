import pandas as pd

from stlite_hello.analysis import (
    RunBundle,
    SimulationReport,
    run_replicates,
    serialize_run,
    summarize,
)
from stlite_hello.features.cournot import (
    COURNOT_FEATURE,
    CournotConfig,
    simulate_once,
)


def _run_and_summarize(config: CournotConfig) -> tuple[RunBundle, SimulationReport]:
    bundle = run_replicates(
        simulate_once=simulate_once,
        params=config.params,
        config=config,
    )
    report = summarize(bundle=bundle, config=config)
    return bundle, report


def test_cournot_run_with_default_seed_is_deterministic(
    cournot_fast_config: CournotConfig,
) -> None:
    first_bundle, first_report = _run_and_summarize(cournot_fast_config)
    second_bundle, second_report = _run_and_summarize(cournot_fast_config)

    pd.testing.assert_frame_equal(first_bundle.final_population, second_bundle.final_population)
    pd.testing.assert_frame_equal(first_report.metrics_ci, second_report.metrics_ci)


def test_cournot_export_round_trip_is_byte_identical(
    cournot_fast_config: CournotConfig,
) -> None:
    bundle, report = _run_and_summarize(cournot_fast_config)
    first = serialize_run(
        feature=COURNOT_FEATURE,
        config=cournot_fast_config,
        params=cournot_fast_config.params,
        bundle=bundle,
        report=report,
    )
    second = serialize_run(
        feature=COURNOT_FEATURE,
        config=cournot_fast_config,
        params=cournot_fast_config.params,
        bundle=bundle,
        report=report,
    )

    assert first == second
