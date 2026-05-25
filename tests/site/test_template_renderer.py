from stlite_hello.site import SemanticVersion, SiteTemplateRenderer


def test_template_renderer_substitutes_version_and_requirements(
    template_renderer: SiteTemplateRenderer,
    app_entrypoint: str,
) -> None:
    rendered = template_renderer.render_index_html(
        version=SemanticVersion.parse("9.9.9"),
        requirements=("altair",),
        package_files=("stlite_hello/__init__.py",),
        entrypoint=app_entrypoint,
    )

    assert "@stlite/browser@9.9.9" in rendered
    assert "altair" in rendered
    assert '<app-file name="stlite_hello/__init__.py"' in rendered
    assert f'<streamlit-app src="./{app_entrypoint}">' in rendered


def test_template_renderer_not_found_html_returns_redirect_page(
    template_renderer: SiteTemplateRenderer,
) -> None:
    html = template_renderer.render_not_found_html()

    assert "sessionStorage.setItem" in html
    assert "location.replace" in html


def test_jinja_environment_does_not_autoescape_python_templates(
    template_renderer: SiteTemplateRenderer,
    app_entrypoint: str,
) -> None:
    rendered = template_renderer.render_index_html(
        version=SemanticVersion.parse("1.0.0"),
        requirements=(),
        package_files=("stlite_hello/app.py",),
        entrypoint=app_entrypoint,
    )

    assert "->" not in rendered or "-&gt;" not in rendered
    assert "&gt;" not in rendered
    assert "&lt;" not in rendered
