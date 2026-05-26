from stlite_hello.analysis import ChartHeading, DecileHeatmapHeading, KdeFitsHeading
from stlite_hello.view_models import (
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

from .charts import BeveridgeHeading

LABOR_MATCHING_COPY = FeatureCopy(
    page_header=PageHeader(
        title="Labor search-and-matching dynamics",
        icon=":material/work:",
        caption=(
            "Workers and vacancies meet through a Cobb-Douglas matching function. "
            "Separations dissolve jobs at a constant rate while new vacancies open every period; "
            "earnings accrue only while employed."
        ),
    ),
    example=ExampleCallout(
        headline="Seasonal hospitality hiring in a tourist town",
        summary=(
            "A coastal town with three big resorts, two ski lodges, and a long tail of "
            "family-run inns. During peak season every owner posts vacancies (`v` jobs "
            "open) while a pool of seasonal workers (`u` unemployed) walks door to door "
            "or scrolls Indeed. The number of matches that actually form each week is "
            "not `min(u, v)` — many workers and vacancies miss each other because of "
            "skills, schedules, language, distance. It is well approximated by a "
            "Cobb-Douglas function `M = A * u^alpha * v^(1 - alpha)`. At the end of each season a "
            "fraction of the matches dissolve. Over a worker's career, lifetime earnings "
            "hinge on how lucky their matching draws were — and the income distribution "
            "across the workforce ends up looking lognormal, with a thicker tail when the "
            "matching efficiency `A` is low and separations are frequent."
        ),
        mechanism=(
            "The simulation tracks a population of workers (each either unemployed or "
            "matched) and a pool of vacancies. At every step new matches are drawn from "
            "the Cobb-Douglas matching function, existing matches dissolve at the "
            "separation rate `s`, and a fresh batch of vacancies opens. Workers earn a "
            "per-period wage only while employed; cumulative wage income across the "
            "horizon is what the metrics, Lorenz curve, and KDE describe. This is the "
            "Diamond-Mortensen-Pissarides (DMP) workhorse model that won the 2010 Nobel "
            "Prize — and which generates the negatively-sloped **Beveridge curve** "
            "between unemployment and vacancies that you can see in the special chart."
        ),
        references_title="Seminal papers and further reading",
        references=(
            Reference(
                citation="Pissarides (2000)",
                title="Equilibrium Unemployment Theory (2nd ed.)",
                venue="MIT Press",
                url="https://mitpress.mit.edu/9780262161879/equilibrium-unemployment-theory/",
            ),
            Reference(
                citation="Mortensen & Pissarides (1994)",
                title="Job creation and job destruction in the theory of unemployment",
                venue="The Review of Economic Studies, 61(3), 397-415",
                url="https://doi.org/10.2307/2297896",
            ),
            Reference(
                citation="Diamond (1982)",
                title="Aggregate demand management in search equilibrium",
                venue="Journal of Political Economy, 90(5), 881-894",
                url="https://doi.org/10.1086/261099",
            ),
            Reference(
                citation="Petrongolo & Pissarides (2001)",
                title="Looking into the black box: a survey of the matching function",
                venue="Journal of Economic Literature, 39(2), 390-431",
                url="https://doi.org/10.1257/jel.39.2.390",
            ),
        ),
    ),
    headings=CommonChartHeadings(
        metrics_table=MetricsTableHeading(
            title="Headline metrics with bootstrap CI",
            caption="Six concentration + five mobility metrics on cumulative wage income.",
        ),
        metric_trajectories=ChartHeading(
            title="Metric trajectories with 95% CI band",
            x_label="Step",
            y_label="Estimate",
        ),
        lorenz=ChartHeading(
            title="Lorenz curve of final wage income",
            x_label="Cumulative share of workers",
            y_label="Cumulative share of income",
        ),
        kde_fits=KdeFitsHeading(
            title="Final-income KDE with top-3 fitted PDFs",
            x_label="Cumulative wage income",
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
        label="Labor-matching seed",
        help="Deterministic seed for this simulation only.",
    ),
    run_control=DEFAULT_RUN_CONTROL_LABELS,
    explainers=DEFAULT_CHART_EXPLAINERS,
    special_chart_title="Beveridge curve",
    special_chart_explainer=ChartExplainer(
        expander_title="How to read this chart",
        how_to_read=(
            "Every dot is one (unemployment rate, vacancy rate) snapshot from "
            "the simulation, coloured from light to dark as the simulation "
            "advances. The dots trace the path the labour market walks "
            "through `(u, v)` space."
        ),
        what_it_means=(
            "Classical theory predicts a **downward-sloping Beveridge "
            "curve**: when unemployment is high, vacancies are scarce, and "
            "vice versa. If the trace bends in that direction the matching "
            "function is doing its job; lateral outward shifts of the cloud "
            "are the empirical signature of falling matching efficiency — "
            "the diagnosis labour economists use to argue about skill "
            "mismatch and structural unemployment."
        ),
    ),
)


LABOR_MATCHING_SPECIAL_HEADING = BeveridgeHeading(
    title="Beveridge curve traced through the simulation",
    x_label="Unemployment rate",
    y_label="Vacancy rate",
    step_label="Step",
)
