# Stlite Hello World

A minimal [Stlite](https://stlite.net/browser/) demo: Streamlit in the browser on GitHub Pages, with Altair charts and a Python backend managed by [uv](https://docs.astral.sh/uv/).

## Quick start

```bash
uv sync --group dev
uv run poe dev                  # local Streamlit, full app
uv run poe dev-feature home     # run a single feature slice
uv run poe build-site           # generate _site/ for GitHub Pages
uv run poe serve-site           # serve _site/ at http://localhost:8000
uv run poe test                 # pytest with 100% coverage
uv run poe sync-pyodide-constraints  # refresh Pyodide lock + uv constraints
```

## Pyodide / uv lock alignment

`@stlite/browser@1.7.3` bundles **Pyodide 0.29.3**. The repo keeps that inventory in `constraints/pyodide-lock.json` and mirrors every PEP 508-valid package into `[tool.uv].constraint-dependencies` in `pyproject.toml`. Dev dependencies are pinned to versions compatible with that constraint set (for example `pytest==8.3.5`, `poethepoet==0.37.0`, `pytest-cov==6.0.0`).

After bumping `pyodide_version` in `src/stlite_hello/pyodide_sync/config.py` (or `stlite_browser_version` in `src/stlite_hello/site/config.py`), run `uv run poe sync-pyodide-constraints`, resolve any lock conflicts in `[project]` / `[dependency-groups].dev`, then `uv lock`.

## GitHub Pages

1. Enable **GitHub Pages** → source: **GitHub Actions**.
2. Push to `main`; the **Deploy GitHub Pages** workflow publishes `_site/`.

The static site loads `@stlite/browser` from jsDelivr and installs `pandas`, `numpy`, and `altair` in the browser via Pyodide.

## Project layout

| Path | Purpose |
|------|---------|
| `src/stlite_hello/app.py` | Streamlit entrypoint; wires `features.pages()` into `st.navigation` |
| `src/stlite_hello/features/` | Vertical slices (`home`, `charts`, `about`), each runnable on its own |
| `src/stlite_hello/site/` | Builds `_site/` for GitHub Pages |
| `src/stlite_hello/pyodide_sync/` | Vendors `pyodide-lock.json` and syncs `[tool.uv].constraint-dependencies` |
| `_site/` | Generated static site (commit after `build-site` or let CI build it) |
