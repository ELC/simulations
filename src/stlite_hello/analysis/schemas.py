import pandera.pandas as pa


class ReplicateLong(pa.DataFrameModel):
    """One row per (run, step, metric) trajectory point."""

    run: int = pa.Field(ge=0)
    step: int = pa.Field(ge=0)
    metric: str
    value: float


class FinalPopulation(pa.DataFrameModel):
    """Final focal-quantity per (run, agent)."""

    run: int = pa.Field(ge=0)
    agent: int = pa.Field(ge=0)
    value: float = pa.Field(ge=0.0)


class FocalPanel(pa.DataFrameModel):
    """Focal-quantity panel: one row per (run, step, agent)."""

    run: int = pa.Field(ge=0)
    step: int = pa.Field(ge=0)
    agent: int = pa.Field(ge=0)
    value: float = pa.Field(ge=0.0)


class MetricCI(pa.DataFrameModel):
    """Bootstrap CI summary for one metric per simulation."""

    metric: str
    estimate: float
    ci_low: float
    ci_high: float
    standard_error: float = pa.Field(ge=0.0)
    confidence_level: float = pa.Field(gt=0.0, lt=1.0)
    family: str  # "concentration" | "mobility"


class MetricCIOverTime(pa.DataFrameModel):
    """Per-step bootstrap CI for trajectory plots."""

    metric: str
    step: int = pa.Field(ge=0)
    estimate: float
    ci_low: float
    ci_high: float
    family: str


class LorenzCurve(pa.DataFrameModel):
    """Cumulative population vs cumulative focal-quantity shares."""

    population_share: float = pa.Field(ge=0.0, le=1.0)
    value_share: float = pa.Field(ge=0.0, le=1.0)


class KDECurve(pa.DataFrameModel):
    """Empirical density of the final focal quantity."""

    x: float
    density: float = pa.Field(ge=0.0)


class DistributionFit(pa.DataFrameModel):
    """MLE fit and AIC ranking for a candidate distribution."""

    name: str
    params_json: str
    loglik: float
    aic: float
    delta_aic: float = pa.Field(ge=0.0)
    rank: int = pa.Field(ge=1)


class FittedDensity(pa.DataFrameModel):
    """PDF of a fitted distribution evaluated on the KDE grid."""

    name: str
    x: float
    density: float = pa.Field(ge=0.0)


class DecileTransition(pa.DataFrameModel):
    """Decile-to-decile transition probability matrix in long form."""

    from_decile: int = pa.Field(ge=1, le=10)
    to_decile: int = pa.Field(ge=1, le=10)
    probability: float = pa.Field(ge=0.0, le=1.0)


class TopPctSpell(pa.DataFrameModel):
    """One contiguous tenure spell of an agent in the top 1% percentile set."""

    run: int = pa.Field(ge=0)
    agent: int = pa.Field(ge=0)
    spell: int = pa.Field(ge=0)
    duration: int = pa.Field(ge=1)
    censored: bool
