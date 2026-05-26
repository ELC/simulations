"""Frozen view-model singletons holding Sugarscape UI text."""

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

from .special_chart import SpatialHeading

SUGARSCAPE_COPY = FeatureCopy(
    page_header=PageHeader(
        title="Sugarscape resource-foraging dynamics",
        icon=":material/grass:",
        caption=(
            "Agents on a toroidal sugar landscape search within their visual range, harvest, and "
            "pay metabolism each step. Heterogeneous metabolisms and birth positions seed the "
            "emergence of a heavy-tailed wealth distribution."
        ),
    ),
    example=ExampleCallout(
        headline="Artisanal gold panning along a Madre de Dios watershed",
        summary=(
            "Follow a few hundred informal prospectors along a stretch of the Madre de "
            "Dios river in the Peruvian Amazon. Each panner can only see and reach the "
            "few sandbars within walking distance; gold-bearing sediment regenerates "
            "slowly downstream and is unevenly distributed (two or three legendary "
            "sandbars contain most of the alluvial gold). Every day each panner pays "
            "a metabolic cost (food, fuel, mercury) and either harvests sediment from "
            "the cell they stand on or walks to a richer one in sight. Within months, "
            "even though the rules and the river are the same for everyone, a small "
            "number of well-positioned, low-metabolism, fortunate-start prospectors "
            "accumulate vastly more gold than the rest. Anthropologists and "
            "development economists studying these scenes consistently find Pareto-"
            "shaped income distributions — exactly the shape Epstein & Axtell got "
            "from their 1996 Sugarscape with no inheritance, no rent-seeking, no "
            "policy: only **vision, metabolism, and luck of birth**."
        ),
        mechanism=(
            "Agents live on a 2D toroidal sugar landscape. Each step every agent "
            "looks within their vision radius (von Neumann neighbourhood up to v "
            "cells away), moves to the cell with the most sugar, harvests it, and "
            "pays a per-agent metabolism cost. Sugar regrows slowly. Heterogeneity "
            "in vision and metabolism (drawn at birth and **never updated**) is the "
            "only source of agent difference. Despite the symmetric rules, the "
            "interaction of vision, metabolism, and the spatial distribution of "
            "resources reliably produces a heavy-tailed wealth distribution."
        ),
        references_title="Seminal papers and further reading",
        references=(
            Reference(
                citation="Epstein & Axtell (1996)",
                title="Growing Artificial Societies: Social Science from the Bottom Up",
                venue="Brookings Institution Press / MIT Press",
                url="https://mitpress.mit.edu/9780262550253/growing-artificial-societies/",
            ),
            Reference(
                citation="Axtell (2001)",
                title="Zipf distribution of U.S. firm sizes",
                venue="Science, 293(5536), 1818-1820",
                url="https://doi.org/10.1126/science.1062081",
            ),
            Reference(
                citation="Bonabeau (2002)",
                title=("Agent-based modeling: methods and techniques for simulating human systems"),
                venue="Proceedings of the National Academy of Sciences, 99(suppl. 3), 7280-7287",
                url="https://doi.org/10.1073/pnas.082080899",
            ),
            Reference(
                citation="Hamill & Gilbert (2016)",
                title="Agent-Based Modelling in Economics",
                venue="Wiley",
                url="https://www.wiley.com/en-us/Agent+Based+Modelling+in+Economics-p-9781118456071",
            ),
        ),
    ),
    headings=CommonChartHeadings(
        metrics_table=MetricsTableHeading(
            title="Headline metrics with bootstrap CI",
            caption="Six concentration + five mobility metrics on per-agent wealth.",
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
        label="Sugarscape seed",
        help="Deterministic seed for this simulation only.",
    ),
    run_control=DEFAULT_RUN_CONTROL_LABELS,
    explainers=DEFAULT_CHART_EXPLAINERS,
    special_chart_title="Spatial wealth heatmap",
    special_chart_explainer=ChartExplainer(
        expander_title="How to read this chart",
        how_to_read=(
            "The background heatmap shows **remaining sugar** on every grid "
            "cell at the end of the simulation (darker = more sugar). "
            "Overlaid dots are surviving agents, sized by their accumulated "
            "wealth and positioned at their final coordinates."
        ),
        what_it_means=(
            "Bright clusters of large dots reveal the **wealth oases** — "
            "patches where high-sugar cells, low-metabolism agents, and "
            "lucky vision aligned. Empty corners far from sugar peaks expose "
            "the **geographic poverty** the model generates from nothing but "
            "spatial heterogeneity. Toggling the parameters (vision, "
            "metabolism range, regrowth) and re-running shows how sensitive "
            "the spatial inequality is to each lever."
        ),
    ),
)

SUGARSCAPE_SPECIAL_HEADING = SpatialHeading(
    title="Final sugar landscape and agent wealth",
    row_label="Row",
    col_label="Column",
    sugar_label="Remaining sugar",
    agent_label="Agent wealth",
)


__all__ = ["SUGARSCAPE_COPY", "SUGARSCAPE_SPECIAL_HEADING"]
