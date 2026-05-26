"""Frozen view-model singletons holding Double Auction UI text."""

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

from .special_chart import SupplyDemandHeading

DOUBLE_AUCTION_COPY = FeatureCopy(
    page_header=PageHeader(
        title="Continuous double-auction price discovery",
        icon=":material/storefront:",
        caption=(
            "Buyers and sellers post bids and asks with private values; matching is "
            "price-time-priority. Price converges to the Walrasian crossing as agents arrive."
        ),
    ),
    example=ExampleCallout(
        headline="Wholesale day-ahead electricity pools",
        summary=(
            "Every afternoon, generators across a national grid (gas peakers, wind farms, "
            "nuclear baseload) submit *ask* offers for the next 24 hours — 'I'll deliver "
            "100 MWh between 18:00 and 19:00 for at least €82/MWh'. At the same time, "
            "retailers and large industrial buyers submit *bid* curves — 'I'll buy that block "
            "for at most €95/MWh'. The independent system operator stacks asks from cheapest "
            "to most expensive (the supply curve), stacks bids from highest to lowest (the "
            "demand curve), and the **single clearing price** for that hour is where the two "
            "curves cross. The remarkable thing — first shown experimentally by Vernon Smith "
            "and theoretically by Gode & Sunder — is that even with traders submitting nearly "
            "random orders, the clearing price hits the competitive equilibrium within a few "
            "rounds. The market is more intelligent than its participants."
        ),
        mechanism=(
            "Each agent in the simulation receives a private valuation drawn from a fixed "
            "distribution and posts either a buy or a sell quote noisily anchored on that "
            "value. Orders enter a continuous limit order book; matches obey price-time "
            "priority and accrue surplus to both sides. After enough orders arrive, the "
            "realised trade prices concentrate on the Walrasian crossing and *allocative "
            "efficiency* approaches one — even though no agent knew the equilibrium price in "
            "advance. The surplus distribution across traders is what the headline metrics "
            "and Lorenz curve track."
        ),
        references_title="Seminal papers and further reading",
        references=(
            Reference(
                citation="Smith (1962)",
                title="An experimental study of competitive market behavior",
                venue="Journal of Political Economy, 70(2), 111-137",
                url="https://doi.org/10.1086/258609",
            ),
            Reference(
                citation="Gode & Sunder (1993)",
                title=(
                    "Allocative efficiency of markets with zero-intelligence traders: "
                    "market as a partial substitute for individual rationality"
                ),
                venue="Journal of Political Economy, 101(1), 119-137",
                url="https://doi.org/10.1086/261868",
            ),
            Reference(
                citation="Friedman & Rust (Eds., 1993)",
                title="The Double Auction Market: Institutions, Theories, and Evidence",
                venue="Addison-Wesley, Santa Fe Institute Studies in the Sciences of Complexity",
                url=(
                    "https://www.routledge.com/The-Double-Auction-Market-Institutions-"
                    "Theories-And-Evidence/Friedman-Rust/p/book/9780201624595"
                ),
            ),
            Reference(
                citation="Cliff & Bruten (1997)",
                title=("Minimal-intelligence agents for bargaining behaviours in market-based environments"),
                venue="HP Laboratories Technical Report HPL-97-91",
                url="https://www.hpl.hp.com/techreports/97/HPL-97-91.html",
            ),
        ),
    ),
    headings=CommonChartHeadings(
        metrics_table=MetricsTableHeading(
            title="Headline metrics with bootstrap CI",
            caption="Six concentration + five mobility metrics on cumulative trader surplus.",
        ),
        metric_trajectories=ChartHeading(
            title="Metric trajectories with 95% CI band",
            x_label="Step",
            y_label="Estimate",
        ),
        lorenz=ChartHeading(
            title="Lorenz curve of final trader surplus",
            x_label="Cumulative share of traders",
            y_label="Cumulative share of surplus",
        ),
        kde_fits=KdeFitsHeading(
            title="Final-surplus KDE with top-3 fitted PDFs",
            x_label="Cumulative surplus",
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
        label="Double Auction seed",
        help="Deterministic seed for this simulation only.",
    ),
    run_control=DEFAULT_RUN_CONTROL_LABELS,
    explainers=DEFAULT_CHART_EXPLAINERS,
    special_chart_title="Marshallian supply-demand cross (final round)",
    special_chart_explainer=ChartExplainer(
        expander_title="How to read this chart",
        how_to_read=(
            "The upward-sloping staircase is the **supply curve** built from all "
            "ask offers sorted from cheapest to most expensive. The downward "
            "staircase is the **demand curve** built from all bids sorted from "
            "highest to lowest. Their intersection marks the competitive "
            "(Walrasian) clearing price and quantity; the dashed horizontal "
            "line shows the price at which the market actually cleared."
        ),
        what_it_means=(
            "If the dashed line sits exactly on the staircase crossing, the "
            "double auction discovered the equilibrium price despite agents "
            "submitting noisy quotes — the Gode-Sunder zero-intelligence "
            "result. A persistent gap means the institutional rules (tick "
            "size, queue priority, noisy valuations) are leaking surplus that "
            "could in principle be captured."
        ),
    ),
)

DOUBLE_AUCTION_SPECIAL_HEADING = SupplyDemandHeading(
    title="Final-round supply and demand curves",
    x_label="Quantity",
    y_label="Price",
    clearing_label="Clearing price",
)


__all__ = ["DOUBLE_AUCTION_COPY", "DOUBLE_AUCTION_SPECIAL_HEADING"]
