from stlite_hello.site import SITE_SETTINGS, SemanticVersion


def test_pyodide_bundle_versions_pins_binary_packages() -> None:
    bundle = SITE_SETTINGS.pyodide_bundle_versions

    assert bundle["numpy"] == SemanticVersion.parse("2.2.5")
    assert bundle["pandas"] == SemanticVersion.parse("2.3.3")
