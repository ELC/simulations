from collections.abc import Callable

from pydantic import BaseModel, ConfigDict, Field

from stlite_hello.analysis import (
    AggregationConfig,
    ChartHeading,
    DecileHeatmapHeading,
    KdeFitsHeading,
    RunBundle,
    SimulationReport,
)


class PageHeader(BaseModel):
    model_config = ConfigDict(frozen=True)

    title: str
    icon: str
    caption: str


class Reference(BaseModel):
    model_config = ConfigDict(frozen=True)

    citation: str
    title: str
    venue: str
    url: str


class ExampleCallout(BaseModel):
    """Real-world analogue + seminal-paper references shown above the run toolbar."""

    model_config = ConfigDict(frozen=True)

    headline: str
    summary: str
    mechanism: str
    references_title: str
    references: tuple[Reference, ...]


class MetricsTableHeading(BaseModel):
    model_config = ConfigDict(frozen=True)

    title: str
    caption: str


class DownloadHeading(BaseModel):
    model_config = ConfigDict(frozen=True)

    label: str
    help: str
    mime: str = "application/json"


class ChartExplainer(BaseModel):
    """How-to-read narrative rendered as a collapsible expander below a chart."""

    model_config = ConfigDict(frozen=True)

    expander_title: str
    how_to_read: str
    what_it_means: str


class AggregationSidebarLabels(BaseModel):
    model_config = ConfigDict(frozen=True)

    expander_title: str
    runs_label: str
    seed_label: str
    confidence_label: str
    bootstrap_resamples_label: str
    trajectory_samples_label: str


class AggregationSidebarInputs(BaseModel):
    model_config = ConfigDict(frozen=True)

    defaults: AggregationConfig
    labels: AggregationSidebarLabels
    key_prefix: str = Field(min_length=1)


class RunControlLabels(BaseModel):
    model_config = ConfigDict(frozen=True)

    run_button: str
    idle_message: str
    spinner_template: str
    elapsed_template: str


class SimulationOutcome(BaseModel):
    """Cached result of one run, replayed on every Streamlit re-render."""

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    bundle: RunBundle
    report: SimulationReport
    elapsed_seconds: float
    config: AggregationConfig
    params: BaseModel


class RunControlInputs(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    feature: str
    config: AggregationConfig
    params: BaseModel
    run: Callable[[], RunBundle]
    summarize: Callable[[RunBundle], SimulationReport]
    labels: RunControlLabels
    download: DownloadHeading


class CommonChartHeadings(BaseModel):
    model_config = ConfigDict(frozen=True)

    metrics_table: MetricsTableHeading
    metric_trajectories: ChartHeading
    lorenz: ChartHeading
    kde_fits: KdeFitsHeading
    aic_ranking: ChartHeading
    decile_transitions: DecileHeatmapHeading


class ChartExplainers(BaseModel):
    model_config = ConfigDict(frozen=True)

    metrics_table: ChartExplainer
    metric_trajectories: ChartExplainer
    lorenz: ChartExplainer
    kde_fits: ChartExplainer
    aic_ranking: ChartExplainer
    decile_transitions: ChartExplainer


class SeedSliderLabels(BaseModel):
    model_config = ConfigDict(frozen=True)

    label: str
    help: str


class AdvancedToggleLabels(BaseModel):
    model_config = ConfigDict(frozen=True)

    label: str
    simple_option: str
    advanced_option: str


class FeatureCopy(BaseModel):
    model_config = ConfigDict(frozen=True)

    page_header: PageHeader
    example: ExampleCallout
    headings: CommonChartHeadings
    explainers: ChartExplainers
    download: DownloadHeading
    sidebar: AggregationSidebarLabels
    view_toggle: AdvancedToggleLabels
    seed: SeedSliderLabels
    run_control: RunControlLabels
    special_chart_title: str
    special_chart_explainer: ChartExplainer


DEFAULT_RUN_CONTROL_LABELS = RunControlLabels(
    run_button="Run simulation",
    idle_message="Adjust parameters in the sidebar, then click *Run simulation* to start.",
    spinner_template="Running {runs} replicates...",
    elapsed_template="Last run: {runs} replicates in {elapsed:.2f}s.",
)


DEFAULT_CHART_EXPLAINERS = ChartExplainers(
    metrics_table=ChartExplainer(
        expander_title="How to read this table",
        how_to_read=(
            "Each row is one metric averaged across all replicates. The point "
            "estimate sits between a **lower** and **upper** bound that form a "
            "95% bootstrap confidence interval: with the same seed family and "
            "parameters, a fresh run would land inside that interval ~95% of the "
            "time. Wider intervals mean the metric is noisier — usually because "
            "fewer replicates or a stochastic mechanism dominates."
        ),
        what_it_means=(
            "Concentration metrics (Gini, top-1%, top-10%, Theil, Atkinson, "
            "coefficient of variation) describe **how unequal** the final state "
            "is; mobility metrics (Spearman, decile-overlap, top-decile spell "
            "length, turnover) describe **how much agents move between ranks**. "
            "High concentration + low mobility is an oligarchy; high concentration "
            "+ high mobility is a churn-driven boom-bust regime."
        ),
    ),
    metric_trajectories=ChartExplainer(
        expander_title="How to read this chart",
        how_to_read=(
            "Each panel plots one metric versus the simulation step. The solid "
            "line is the mean across replicates and the shaded band is the 95% "
            "bootstrap CI at every snapshot. A narrowing band means replicates "
            "agree; a widening band means the system is still exploring."
        ),
        what_it_means=(
            "Look for the **shape**: a monotonically rising Gini means the system "
            "keeps concentrating; a plateau means a steady-state distribution has "
            "emerged; oscillations hint at cyclical dynamics or a stochastic "
            "attractor. Compare against the same chart on a different simulation "
            "to see whose dynamics settle faster."
        ),
    ),
    lorenz=ChartExplainer(
        expander_title="How to read this chart",
        how_to_read=(
            "The x-axis is the cumulative share of agents (poorest on the left); "
            "the y-axis is the cumulative share of the resource they hold. The "
            "**diagonal** is perfect equality (everyone holds the same). The "
            "**curve** bulges below the diagonal; the bigger the gap, the more "
            "unequal the distribution. Gini is exactly twice the area between "
            "the curve and the diagonal."
        ),
        what_it_means=(
            "A near-diagonal Lorenz means the simulation produced an egalitarian "
            "outcome. A curve hugging the bottom-right corner means a tiny "
            "minority owns almost everything. The shape lets you eyeball "
            "inequality without committing to a single scalar like Gini."
        ),
    ),
    kde_fits=ChartExplainer(
        expander_title="How to read this chart",
        how_to_read=(
            "The grey histogram-like curve is a kernel density estimate (KDE) "
            "of the final empirical distribution — a smoothed shape of where "
            "agents end up. The coloured lines on top are the **three best-fit "
            "parametric distributions** ranked by AIC: closer overlap = better "
            "model. A heavy right tail dragging the KDE away from the fits is a "
            "tell-tale of an emergent power law."
        ),
        what_it_means=(
            "If a single fit hugs the KDE tightly, the simulation reproduces a "
            "known statistical regime (lognormal labour earnings, exponential "
            "intertrade times, Pareto wealth, etc.). If all fits miss the tail, "
            "the dynamics produced a heavier-tailed regime than any standard "
            "family captures."
        ),
    ),
    aic_ranking=ChartExplainer(
        expander_title="How to read this chart",
        how_to_read=(
            "Each bar is one candidate distribution; the length is the ΔAIC "
            "relative to the best fit (best = 0). Rules of thumb from Burnham & "
            "Anderson (2002): ΔAIC < 2 means roughly equivalent support, 4-7 "
            "means considerably less support, > 10 means essentially no support."
        ),
        what_it_means=(
            "The winning family is your best parametric summary of the final "
            "state. If lognormal and gamma tie, the regime is light-tailed and "
            "well behaved; if Pareto / power-law wins by a wide margin, the "
            "mechanism produced scale-free concentration that mean / variance "
            "summaries will systematically mis-describe."
        ),
    ),
    decile_transitions=ChartExplainer(
        expander_title="How to read this chart",
        how_to_read=(
            "Rows are the agent's **initial** decile (1 = poorest, 10 = richest); "
            "columns are the **final** decile. Each cell is the probability of "
            "moving from row to column, averaged across replicates. A bright "
            "diagonal means everyone stays where they started; a flat heatmap "
            "means decile membership is essentially random by the end."
        ),
        what_it_means=(
            "This is the mobility chart. Highly diagonal heatmaps describe "
            "**sticky** societies / markets (where you start determines where "
            "you end); flat heatmaps describe **churn** regimes. Asymmetries "
            "(e.g. easier to fall than to rise) jump out as off-diagonal mass "
            "shifted to one side."
        ),
    ),
)
