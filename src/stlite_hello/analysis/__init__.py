"""Shared analysis core for free-market simulations.

Holds aggregation, bootstrap CI, KDE, distribution fitting, mobility metrics
and Altair builders. Only the modules under :mod:`analysis.adapters` import
``scipy``/``statsmodels`` directly; everything else consumes typed wrappers.
"""

from .aggregation import ReplicateResult, RunBundle, SimulateOnce, run_replicates
from .charts import (
    ChartHeading,
    DecileHeatmapHeading,
    KdeFitsHeading,
    build_aic_ranking,
    build_decile_transitions,
    build_kde_with_fits,
    build_lorenz,
    build_metric_trajectories,
)
from .config import AggregationConfig
from .export import (
    SerializedBundle,
    SerializedReport,
    SimulationRunExport,
    build_export,
    deserialize_run,
    export_filename,
    serialize_run,
)
from .schemas import (
    DecileTransition,
    DistributionFit,
    FinalPopulation,
    FittedDensity,
    FocalPanel,
    KDECurve,
    LorenzCurve,
    MetricCI,
    MetricCIOverTime,
    ReplicateLong,
    TopPctSpell,
)
from .summarize import SimulationReport, summarize

__all__ = [
    "AggregationConfig",
    "ChartHeading",
    "DecileHeatmapHeading",
    "DecileTransition",
    "DistributionFit",
    "FinalPopulation",
    "FittedDensity",
    "FocalPanel",
    "KDECurve",
    "KdeFitsHeading",
    "LorenzCurve",
    "MetricCI",
    "MetricCIOverTime",
    "ReplicateLong",
    "ReplicateResult",
    "RunBundle",
    "SerializedBundle",
    "SerializedReport",
    "SimulateOnce",
    "SimulationReport",
    "SimulationRunExport",
    "TopPctSpell",
    "build_aic_ranking",
    "build_decile_transitions",
    "build_export",
    "build_kde_with_fits",
    "build_lorenz",
    "build_metric_trajectories",
    "deserialize_run",
    "export_filename",
    "run_replicates",
    "serialize_run",
    "summarize",
]
