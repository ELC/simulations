# Stlite Hello World

A minimal [Stlite](https://stlite.net/browser/) demo: Streamlit in the browser on GitHub Pages, with Altair charts and a Python backend managed by [uv](https://docs.astral.sh/uv/).

## Quick start

```bash
uv sync --group dev
uv run poe dev          # local Streamlit
uv run poe build-site   # generate _site/ for GitHub Pages
uv run poe serve-site   # serve _site/ at http://localhost:8000
uv run poe test         # pytest with 100% coverage
```

## GitHub Pages

1. Enable **GitHub Pages** → source: **GitHub Actions**.
2. Push to `main`; the **Deploy GitHub Pages** workflow publishes `_site/`.

The static site loads `@stlite/browser` from jsDelivr and installs `pandas`, `numpy`, and `altair` in the browser via Pyodide.

## Project layout

| Path | Purpose |
|------|---------|
| `stlite_hello/charts.py` | Altair chart logic (presentation-agnostic, pytest-covered) |
| `stlite_hello/presentation/` | Multipage Streamlit app (home + `pages/`) |
| `stlite_hello/site/` | Builds `_site/` for GitHub Pages |
| `_site/` | Generated static site (commit after `build-site` or let CI build it) |
