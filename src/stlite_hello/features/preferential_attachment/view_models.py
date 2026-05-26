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

from .charts import ZipfHeading

PREFERENTIAL_ATTACHMENT_COPY = FeatureCopy(
    page_header=PageHeader(
        title="Preferential attachment growth dynamics",
        icon=":material/hub:",
        caption=(
            "Each new node attaches to existing nodes with probability proportional to current "
            "degree. The resulting degree distribution is heavy-tailed; concentration metrics "
            "track the emergence of a few dominant hubs."
        ),
    ),
    example=ExampleCallout(
        headline="Academic citation networks (the Matthew effect)",
        summary=(
            "When a PhD student writes the literature review of a new paper on, say, "
            "transformer attention, they overwhelmingly cite the handful of canonical "
            "papers everyone already cites (Vaswani 2017, Devlin 2018, ...) rather than "
            "trawling arXiv for obscure but relevant work. Multiply that behaviour over "
            "millions of submissions across decades and you get the empirical shape that "
            "**~80% of citations accrue to ~20% of papers**, with a long tail of "
            "uncited niche work and a handful of papers cited tens of thousands of "
            "times. Robert Merton called this the **Matthew effect** in 1968 — 'unto "
            "everyone that hath shall be given' — and Derek de Solla Price formalised "
            "it as 'cumulative advantage' in 1976. The same mechanism shapes who you "
            "follow on Twitter/X, which YouTube channels get recommended, and which "
            "open-source repositories get starred."
        ),
        mechanism=(
            "Each step adds a new node that connects to `m` existing nodes, choosing "
            "each target with probability proportional to its current degree (Barabási-"
            "Albert preferential attachment). The result is a degree distribution that "
            "converges to a power law `P(k) ~ k^{-3}` regardless of starting conditions. "
            "Once a hub becomes large enough, every newcomer is overwhelmingly likely to "
            "link to it — the **rich-get-richer** dynamic that the metrics, the Lorenz "
            "curve, and the Zipf log-log plot all detect from different angles."
        ),
        references_title="Seminal papers and further reading",
        references=(
            Reference(
                citation="Barabási & Albert (1999)",
                title="Emergence of scaling in random networks",
                venue="Science, 286(5439), 509-512",
                url="https://doi.org/10.1126/science.286.5439.509",
            ),
            Reference(
                citation="Price (1976)",
                title="A general theory of bibliometric and other cumulative advantage processes",
                venue="Journal of the American Society for Information Science, 27(5), 292-306",
                url="https://doi.org/10.1002/asi.4630270505",
            ),
            Reference(
                citation="Merton (1968)",
                title="The Matthew effect in science",
                venue="Science, 159(3810), 56-63",
                url="https://doi.org/10.1126/science.159.3810.56",
            ),
            Reference(
                citation="Newman (2005)",
                title="Power laws, Pareto distributions and Zipf's law",
                venue="Contemporary Physics, 46(5), 323-351",
                url="https://doi.org/10.1080/00107510500052444",
            ),
        ),
    ),
    headings=CommonChartHeadings(
        metrics_table=MetricsTableHeading(
            title="Headline metrics with bootstrap CI",
            caption="Six concentration + five mobility metrics on per-node degree.",
        ),
        metric_trajectories=ChartHeading(
            title="Metric trajectories with 95% CI band",
            x_label="Node arrivals",
            y_label="Estimate",
        ),
        lorenz=ChartHeading(
            title="Lorenz curve of final degree",
            x_label="Cumulative share of nodes",
            y_label="Cumulative share of degree",
        ),
        kde_fits=KdeFitsHeading(
            title="Final-degree KDE with top-3 fitted PDFs",
            x_label="Degree",
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
        label="Preferential-attachment seed",
        help="Deterministic seed for this simulation only.",
    ),
    run_control=DEFAULT_RUN_CONTROL_LABELS,
    explainers=DEFAULT_CHART_EXPLAINERS,
    special_chart_title="Zipf log-log degree-rank plot",
    special_chart_explainer=ChartExplainer(
        expander_title="How to read this chart",
        how_to_read=(
            "Nodes are sorted from most-connected (rank 1) to least-connected "
            "(rank N) and plotted on a **log-log axis**: x = log(rank), "
            "y = log(degree). A straight line on this chart means the degree "
            "distribution follows a power law `degree ~ rank^{-alpha}`; the "
            "slope is the Zipf exponent and the intercept calibrates the "
            "size of the largest hub."
        ),
        what_it_means=(
            "A perfectly linear cloud is the visual fingerprint of "
            "scale-free behaviour — the same shape Barabási-Albert predicted "
            "and that Newman documented for word frequencies, city sizes, "
            "and web links. Curvature at the top tail (the largest hubs) "
            "would suggest a finite-size cutoff; curvature at the bottom "
            "tail comes from the discrete-degree floor."
        ),
    ),
)


PREFERENTIAL_ATTACHMENT_SPECIAL_HEADING = ZipfHeading(
    title="Degree vs rank on log-log axes",
    x_label="Rank (log)",
    y_label="Degree (log)",
)
