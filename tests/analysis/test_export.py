from datetime import UTC, datetime

import pandas as pd
import pytest
from pydantic import BaseModel
from syrupy.assertion import SnapshotAssertion

from stlite_hello.analysis import (
    AggregationConfig,
    RunBundle,
    SimulationReport,
    SimulationRunExport,
    build_export,
    deserialize_run,
    export_filename,
    serialize_run,
)


class _DummyParams(BaseModel):
    rate: float = 1.5
    label: str = "demo"


@pytest.fixture
def dummy_params() -> _DummyParams:
    return _DummyParams()


@pytest.fixture
def feature_name() -> str:
    return "demo_simulation"


@pytest.fixture
def exponential_export(
    feature_name: str,
    aggregation_config: AggregationConfig,
    dummy_params: _DummyParams,
    exponential_bundle: RunBundle,
    exponential_report: SimulationReport,
) -> SimulationRunExport:
    return build_export(
        feature=feature_name,
        config=aggregation_config,
        params=dummy_params,
        bundle=exponential_bundle,
        report=exponential_report,
    )


def test_build_export_uses_seed_derived_generated_at(
    exponential_export: SimulationRunExport,
    aggregation_seed: int,
) -> None:
    assert exponential_export.generated_at.tzinfo == UTC
    epoch = datetime(2026, 1, 1, tzinfo=UTC)
    expected_seconds = (exponential_export.generated_at - epoch).total_seconds()

    assert expected_seconds == aggregation_seed


def test_serialize_run_round_trips_byte_identical(
    feature_name: str,
    aggregation_config: AggregationConfig,
    dummy_params: _DummyParams,
    exponential_bundle: RunBundle,
    exponential_report: SimulationReport,
) -> None:
    first = serialize_run(
        feature=feature_name,
        config=aggregation_config,
        params=dummy_params,
        bundle=exponential_bundle,
        report=exponential_report,
    )

    parsed = deserialize_run(first)
    second = parsed.model_dump_json().encode("utf-8")

    assert first == second


def test_deserialize_run_reconstructs_typed_bundle(
    exponential_export: SimulationRunExport,
    exponential_bundle: RunBundle,
) -> None:
    payload = exponential_export.model_dump_json().encode("utf-8")
    parsed = deserialize_run(payload)

    bundle = parsed.to_run_bundle()
    pd.testing.assert_frame_equal(bundle.final_population, exponential_bundle.final_population)


def test_deserialize_run_reconstructs_typed_report(
    exponential_export: SimulationRunExport,
    exponential_report: SimulationReport,
) -> None:
    payload = exponential_export.model_dump_json().encode("utf-8")
    parsed = deserialize_run(payload)

    report = parsed.to_simulation_report()
    pd.testing.assert_frame_equal(
        report.metrics_ci.reset_index(drop=True),
        exponential_report.metrics_ci.reset_index(drop=True),
    )


def test_export_filename_is_deterministic(
    aggregation_config: AggregationConfig,
    feature_name: str,
) -> None:
    name = export_filename(feature=feature_name, config=aggregation_config)

    assert name == f"{feature_name}_seed-{aggregation_config.seed}_runs-{aggregation_config.runs}.json"


def test_export_schema_is_snapshotted(snapshot: SnapshotAssertion) -> None:
    schema = SimulationRunExport.model_json_schema()

    assert schema == snapshot
