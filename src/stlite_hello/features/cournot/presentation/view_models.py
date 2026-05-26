"""Frozen view-model singletons holding Cournot UI text."""

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

from .special_chart import BestResponseHeading

COURNOT_COPY = FeatureCopy(
    page_header=PageHeader(
        title="Cournot oligopoly best-response dynamics",
        icon=":material/oil_barrel:",
        caption=(
            "N firms with heterogeneous marginal costs iterate best responses on linear inverse "
            "demand. Quantities converge to the Nash equilibrium; metrics track distance to Nash "
            "and profit dispersion."
        ),
    ),
    example=ExampleCallout(
        headline="OPEC+ crude-oil quota negotiations",
        summary=(
            "Picture the monthly OPEC+ video call. Each member country knows that pumping "
            "*more* barrels lowers the global price (hurting everyone, including itself) while "
            "pumping *fewer* barrels lets rivals steal market share. Saudi Arabia is the "
            "lowest-cost producer, the UAE and Iraq are mid-tier, Venezuela and Nigeria are "
            "the most expensive. Round after round, each minister revises their pledged output "
            "as the **best response** to what they expect rivals to do. After a handful of "
            "iterations, quotas converge to the Nash equilibrium of producer share — exactly "
            "the fixed-point this simulation finds, with the lowest-cost producer capturing the "
            "lion's share of profit."
        ),
        mechanism=(
            "The model assigns each of N firms a heterogeneous marginal cost and an inverse "
            "demand curve `P = a - b·Σq`. At every step every firm computes the quantity that "
            "maximises its own profit, **assuming rivals hold their last move constant** — the "
            "Cournot best-response map. Iterating this map converges geometrically to the "
            "interior Nash equilibrium when the slope condition holds. Cost asymmetry is what "
            "drives the profit dispersion the metrics pick up: low-cost firms are pushed to the "
            "top of the Lorenz curve, high-cost firms hug the bottom."
        ),
        references_title="Seminal papers and further reading",
        references=(
            Reference(
                citation="Cournot (1838)",
                title=("Recherches sur les principes mathématiques de la théorie des richesses"),
                venue="Hachette, Paris (English translation: Macmillan, 1897)",
                url="https://archive.org/details/researchesintom00fishgoog",
            ),
            Reference(
                citation="Nash (1950)",
                title="Equilibrium points in n-person games",
                venue="Proceedings of the National Academy of Sciences, 36(1), 48-49",
                url="https://doi.org/10.1073/pnas.36.1.48",
            ),
            Reference(
                citation="Theocharis (1960)",
                title="On the stability of the Cournot solution on the oligopoly problem",
                venue="The Review of Economic Studies, 27(2), 133-134",
                url="https://doi.org/10.2307/2296135",
            ),
            Reference(
                citation="Vives (1999)",
                title="Oligopoly Pricing: Old Ideas and New Tools",
                venue="MIT Press",
                url="https://mitpress.mit.edu/9780262720403/oligopoly-pricing/",
            ),
        ),
    ),
    headings=CommonChartHeadings(
        metrics_table=MetricsTableHeading(
            title="Headline metrics with bootstrap CI",
            caption="Six concentration + five mobility metrics on per-firm profit.",
        ),
        metric_trajectories=ChartHeading(
            title="Metric trajectories with 95% CI band",
            x_label="Iteration",
            y_label="Estimate",
        ),
        lorenz=ChartHeading(
            title="Lorenz curve of final firm profit",
            x_label="Cumulative share of firms",
            y_label="Cumulative share of profit",
        ),
        kde_fits=KdeFitsHeading(
            title="Final-profit KDE with top-3 fitted PDFs",
            x_label="Profit",
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
        label="Cournot seed",
        help="Deterministic seed for this simulation only.",
    ),
    run_control=DEFAULT_RUN_CONTROL_LABELS,
    explainers=DEFAULT_CHART_EXPLAINERS,
    special_chart_title="Best-response trajectory in (q1, q2) space",
    special_chart_explainer=ChartExplainer(
        expander_title="How to read this chart",
        how_to_read=(
            "The two diagonal lines are the analytic best-response functions "
            "for firms A and B (each firm's optimal quantity as a function of "
            "the rival's). The connected dots trace one replicate's iterates "
            "in (qA, qB) space, hopping from one curve to the other. The "
            "intersection of the two lines is the **Nash equilibrium**."
        ),
        what_it_means=(
            "If the dots zig-zag tightly into the intersection, the Cournot "
            "best-response dynamic is convergent under the chosen parameters. "
            "If they oscillate or diverge, the slope condition fails — a "
            "classic result Theocharis (1960) used to show that with too "
            "many firms or steep demand the naive dynamic becomes unstable."
        ),
    ),
)

COURNOT_SPECIAL_HEADING = BestResponseHeading(
    title="Best-response iterates and analytic lines",
    x_label="Firm A quantity",
    y_label="Firm B quantity",
    line_legend_label="Best response",
)


__all__ = ["COURNOT_COPY", "COURNOT_SPECIAL_HEADING"]
