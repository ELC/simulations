"""Frozen view-model singletons holding Yard-Sale UI text."""

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

from .special_chart import WealthCondensationHeading

YARD_SALE_COPY = FeatureCopy(
    page_header=PageHeader(
        title="Yard-Sale wealth exchange",
        icon=":material/savings:",
        caption=(
            "Random pairwise transfers of a fraction of the loser's wealth — a fair coin still "
            "produces emergent wealth condensation (Pareto / oligarchy)."
        ),
    ),
    example=ExampleCallout(
        headline=("Commission-pool redistribution in high-turnover sales teams"),
        summary=(
            "Imagine a 100-rep enterprise sales floor where every quarter each rep is "
            "randomly paired with a teammate to chase a fresh prospect. The winner of the "
            "deal earns the commission *and* a small override on the loser's next pipeline "
            "(say 17%, the loser keeps the rest). Both reps started equally skilled, the "
            "coin is fair, and the override percentage is uniform — yet within a few years "
            "two or three 'rainmakers' on the floor end up booking 60-80% of all commissions, "
            "while the bulk of the team grinds at a sliver of the total. No one cheated; the "
            "geometry of betting a fixed fraction guarantees it."
        ),
        mechanism=(
            "The simulation pairs agents at random each step and transfers a fraction of the "
            "**loser's** wealth to the winner. The fair coin is what trips intuition: under "
            "multiplicative dynamics, expected log-wealth strictly decreases for the loser even "
            "though the expected linear wealth is preserved. Across many rounds, Jensen's "
            "inequality compounds and almost-all wealth ends up on a vanishing fraction of "
            "agents — the same 'inescapable casino' Boghosian and Yakovenko documented for "
            "real-world wealth distributions."
        ),
        references_title="Seminal papers and further reading",
        references=(
            Reference(
                citation="Boghosian (2019)",
                title="The Inescapable Casino",
                venue="Scientific American, 321(5), 70-77",
                url="https://www.scientificamerican.com/article/is-inequality-inevitable/",
            ),
            Reference(
                citation="Boghosian, Devitt-Lee, Johnson, Li, Marcq & Wang (2017)",
                title=("Oligarchy as a phenomenon of asset exchange in the Yard-Sale model"),
                venue="Physica A: Statistical Mechanics and its Applications, 476, 15-37",
                url="https://doi.org/10.1016/j.physa.2017.01.071",
            ),
            Reference(
                citation="Chakraborti (2002)",
                title=("Distributions of money in model markets of economy"),
                venue="International Journal of Modern Physics C, 13(10), 1315-1321",
                url="https://doi.org/10.1142/S0129183102003905",
            ),
            Reference(
                citation="Hayes (2002)",
                title="Follow the money",
                venue="American Scientist, 90(5), 400-405",
                url="https://www.americanscientist.org/article/follow-the-money",
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
        label="Yard-Sale seed",
        help="Deterministic seed for this simulation only.",
    ),
    run_control=DEFAULT_RUN_CONTROL_LABELS,
    explainers=DEFAULT_CHART_EXPLAINERS,
    special_chart_title="Wealth-condensation heatmap",
    special_chart_explainer=ChartExplainer(
        expander_title="How to read this heatmap",
        how_to_read=(
            "Rows are the agent's wealth rank at every snapshot (1 = richest, "
            "40 = poorest tier); columns are simulation steps. Brighter cells "
            "carry a larger mean share of total wealth, averaged across "
            "replicates. Reading **left to right** shows how the share owned "
            "by each rank tier evolves; reading **top to bottom** shows the "
            "share-vs-rank distribution at a fixed time."
        ),
        what_it_means=(
            "The Yard-Sale signature is a thin bright strip clamping onto the "
            "top rows while the rest of the heatmap fades to dark — total "
            "wealth condenses onto a vanishing fraction of agents. The faster "
            "the strip brightens, the more aggressive the multiplicative bias; "
            "a uniform colour band would mean perfect equality and never "
            "occurs in this model under the default parameters."
        ),
    ),
)

YARD_SALE_SPECIAL_HEADING = WealthCondensationHeading(
    title="Wealth-condensation heatmap (rank vs step)",
    x_label="Step",
    y_label="Rank (1 = richest)",
    color_label="Mean wealth share",
)


__all__ = ["YARD_SALE_COPY", "YARD_SALE_SPECIAL_HEADING"]
