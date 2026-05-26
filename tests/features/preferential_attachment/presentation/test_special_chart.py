from stlite_hello.features.preferential_attachment import (
    PreferentialAttachmentConfig,
    ZipfHeading,
    build_zipf_chart,
    build_zipf_frame,
)

_HEADING = ZipfHeading(
    title="Zipf",
    x_label="Rank",
    y_label="Degree",
)


def test_build_zipf_frame_has_one_row_per_node_sorted_by_degree(
    preferential_attachment_fast_config: PreferentialAttachmentConfig,
) -> None:
    frame = build_zipf_frame(
        params=preferential_attachment_fast_config.params,
        seed=preferential_attachment_fast_config.seed,
    )

    assert len(frame) == preferential_attachment_fast_config.params.n_nodes
    degrees = frame["degree"].tolist()
    assert degrees == sorted(degrees, reverse=True)


def test_build_zipf_chart_uses_log_scales_on_both_axes(
    preferential_attachment_fast_config: PreferentialAttachmentConfig,
) -> None:
    frame = build_zipf_frame(
        params=preferential_attachment_fast_config.params,
        seed=preferential_attachment_fast_config.seed,
    )

    chart = build_zipf_chart(data=frame, heading=_HEADING)
    spec = chart.to_dict()

    assert spec["title"] == _HEADING.title
    assert spec["encoding"]["x"]["scale"]["type"] == "log"
    assert spec["encoding"]["y"]["scale"]["type"] == "log"
