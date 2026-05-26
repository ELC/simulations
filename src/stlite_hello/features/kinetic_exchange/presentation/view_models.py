"""Frozen view-model singletons holding Kinetic Exchange UI text."""

from stlite_hello.analysis import ChartHeading, DecileHeatmapHeading, KdeFitsHeading
from stlite_hello.presentation import (
    DEFAULT_CHART_EXPLAINERS,
    DEFAULT_RUN_CONTROL_LABELS,
    AdvancedToggleLabels,
    AggregationSidebarLabels,
    ChartExplainer,
    CommonChartHeadings,
    DownloadHeading,
    ExampleCallout,
    FeatureCopy,
    MetricsTableHeading,
    PageHeader,
    Reference,
    SeedSliderLabels,
)

from .special_chart import SavingsWealthHeading

KINETIC_COPY = FeatureCopy(
    page_header=PageHeader(
        title="Kinetic wealth exchange (with savings)",
        icon=":material/payments:",
        caption=(
            "Chakraborti-Chakrabarti pairwise updates with per-agent savings rates. "
            "Homogeneous savings produce a Gamma body; heterogeneous savings grow a Pareto tail."
        ),
    ),
    example=ExampleCallout(
        headline="Rotating-savings clubs (ROSCAs, tandas, chamas, susus)",
        summary=(
            "From Mexican *tandas* to West-African *susus* to Indian *chit funds*, hundreds of "
            "millions of households participate in rotating-savings clubs every year. Twelve "
            "neighbours meet monthly, each contributes a fixed share of their disposable income, "
            "and a randomly drawn member takes the whole pot that month. The catch: each member "
            "saves a personal fraction of their pre-club income — some are frugal (high λ), "
            "others spend down (low λ). After enough cycles, the wealth distribution across "
            "members looks almost exactly like a Gamma when everyone saves at the same rate, "
            "but acquires a heavy Pareto tail as soon as savings rates become heterogeneous. "
            "Field economists studying these clubs in Ghana and Kerala have measured both "
            "regimes — and the model below reproduces them from nothing but pairwise random "
            "exchange."
        ),
        mechanism=(
            "At every step the model picks a random pair (i, j) and redistributes their pooled "
            "wealth `wi + wj` according to a uniform draw ε ∈ [0, 1], but each agent first "
            "shields a personal fraction `λi`, `λj` of their wealth (their savings rate). "
            "Setting all λ to a common value yields a Gamma stationary distribution whose shape "
            "parameter is `1 + 3λ/(1-λ)` (Chakraborti & Chakrabarti 2000). Allowing λ to vary "
            "across agents collapses the high-end to a Pareto-tailed distribution with exponent "
            "≈ 2 (Chatterjee, Chakrabarti & Manna 2004) — exactly the regime econophysicists "
            "use to argue that **inequality is driven more by savings heterogeneity than by "
            "rapacity**."
        ),
        references_title="Seminal papers and further reading",
        references=(
            Reference(
                citation="Chakraborti & Chakrabarti (2000)",
                title=("Statistical mechanics of money: how saving propensity affects its distribution"),
                venue="European Physical Journal B, 17(1), 167-170",
                url="https://doi.org/10.1007/s100510070173",
            ),
            Reference(
                citation="Chatterjee, Chakrabarti & Manna (2004)",
                title=("Pareto law in a kinetic model of market with random saving propensity"),
                venue="Physica A, 335(1-2), 155-163",
                url="https://doi.org/10.1016/j.physa.2003.11.014",
            ),
            Reference(
                citation="Patriarca, Chakraborti & Kaski (2004)",
                title=("Statistical model with a standard Gamma distribution"),
                venue="Physical Review E, 70, 016104",
                url="https://doi.org/10.1103/PhysRevE.70.016104",
            ),
            Reference(
                citation="Yakovenko & Rosser (2009)",
                title="Colloquium: Statistical mechanics of money, wealth, and income",
                venue="Reviews of Modern Physics, 81(4), 1703-1725",
                url="https://doi.org/10.1103/RevModPhys.81.1703",
            ),
        ),
    ),
    headings=CommonChartHeadings(
        metrics_table=MetricsTableHeading(
            title="Headline metrics with bootstrap CI",
            caption="Six concentration + five mobility metrics aggregated across replicates.",
        ),
        metric_trajectories=ChartHeading(
            title="Metric trajectories with 95% CI band",
            x_label="Step",
            y_label="Estimate",
        ),
        lorenz=ChartHeading(
            title="Lorenz curve of final wealth",
            x_label="Cumulative share of agents",
            y_label="Cumulative share of wealth",
        ),
        kde_fits=KdeFitsHeading(
            title="Final-wealth KDE with top-3 fitted PDFs",
            x_label="Wealth",
            density_label="Density",
            fit_legend_label="Best-AIC fit",
        ),
        aic_ranking=ChartHeading(
            title="Candidate distribution AIC ranking",
            x_label="ΔAIC (lower is better)",
            y_label="Distribution",
        ),
        decile_transitions=DecileHeatmapHeading(
            title="Decile transition heatmap (initial → final)",
            from_label="Initial decile",
            to_label="Final decile",
            probability_label="Transition probability",
        ),
    ),
    download=DownloadHeading(
        label="Download run as JSON",
        help="Includes the run bundle and the full simulation report.",
    ),
    sidebar=AggregationSidebarLabels(
        expander_title="Aggregation",
        runs_label="Replicates",
        seed_label="Seed",
        confidence_label="Confidence level",
        bootstrap_resamples_label="Bootstrap resamples",
        trajectory_samples_label="Trajectory snapshots",
    ),
    view_toggle=AdvancedToggleLabels(
        label="View",
        simple_option="Simple",
        advanced_option="Advanced",
    ),
    seed=SeedSliderLabels(
        label="Kinetic Exchange seed",
        help="Deterministic seed for this simulation only.",
    ),
    run_control=DEFAULT_RUN_CONTROL_LABELS,
    explainers=DEFAULT_CHART_EXPLAINERS,
    special_chart_title="Wealth vs savings rate scatter",
    special_chart_explainer=ChartExplainer(
        expander_title="How to read this chart",
        how_to_read=(
            "Every dot is one agent at the end of one replicate. The x-axis "
            "is that agent's individual saving propensity λ (how much wealth "
            "they shield in each pairwise exchange); the y-axis is their "
            "final wealth. The thicker line is a rolling mean of final wealth "
            "binned by λ."
        ),
        what_it_means=(
            "If the rolling mean rises sharply with λ, **frugality is "
            "rewarded** — the same lesson Chatterjee, Chakrabarti & Manna "
            "drew when they showed that quenched-disorder savings rates "
            "generate the Pareto tail. A flat rolling mean would mean the "
            "exchange process is so dominant that personal savings rate "
            "doesn't matter; the visible upward slope is the microscopic "
            "driver of macroscopic inequality."
        ),
    ),
)

KINETIC_SPECIAL_HEADING = SavingsWealthHeading(
    title="Final wealth vs saving propensity (with rolling mean)",
    x_label="Saving propensity λ",
    y_label="Final wealth",
    rolling_label="Rolling-mean wealth",
)


__all__ = ["KINETIC_COPY", "KINETIC_SPECIAL_HEADING"]
