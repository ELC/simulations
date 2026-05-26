import numpy as np
import pandas as pd

from stlite_hello.analysis import (
    RunBundle,
    SimulationReport,
    build_export,
    run_replicates,
    serialize_run,
    summarize,
)
from stlite_hello.features.yard_sale import (
    YARD_SALE_FEATURE,
    YardSaleConfig,
    simulate_once,
)


def _run_and_summarize(config: YardSaleConfig) -> tuple[RunBundle, SimulationReport]:
    bundle = run_replicates(
        simulate_once=simulate_once,
        params=config.params,
        config=config,
    )
    report = summarize(bundle=bundle, config=config)
    return bundle, report


def test_yard_sale_run_with_default_seed_is_byte_identical_across_runs(
    yard_sale_fast_config: YardSaleConfig,
) -> None:
    first_bundle, first_report = _run_and_summarize(yard_sale_fast_config)
    second_bundle, second_report = _run_and_summarize(yard_sale_fast_config)

    pd.testing.assert_frame_equal(first_bundle.final_population, second_bundle.final_population)
    pd.testing.assert_frame_equal(first_bundle.focal_panel, second_bundle.focal_panel)
    pd.testing.assert_frame_equal(first_report.metrics_ci, second_report.metrics_ci)


def test_yard_sale_export_round_trip_is_byte_identical(
    yard_sale_fast_config: YardSaleConfig,
) -> None:
    bundle, report = _run_and_summarize(yard_sale_fast_config)
    first = serialize_run(
        feature=YARD_SALE_FEATURE,
        config=yard_sale_fast_config,
        params=yard_sale_fast_config.params,
        bundle=bundle,
        report=report,
    )
    second = serialize_run(
        feature=YARD_SALE_FEATURE,
        config=yard_sale_fast_config,
        params=yard_sale_fast_config.params,
        bundle=bundle,
        report=report,
    )

    assert first == second


def test_yard_sale_export_snapshot_matches(
    yard_sale_fast_config: YardSaleConfig,
    snapshot: object,
) -> None:
    bundle, report = _run_and_summarize(yard_sale_fast_config)
    export = build_export(
        feature=YARD_SALE_FEATURE,
        config=yard_sale_fast_config,
        params=yard_sale_fast_config.params,
        bundle=bundle,
        report=report,
    )

    headline_metrics = export.report.metrics_ci
    rounded = [
        {
            "metric": row["metric"],
            "estimate": float(np.round(row["estimate"], 6)),
            "family": row["family"],
        }
        for row in headline_metrics
    ]

    assert rounded == snapshot
