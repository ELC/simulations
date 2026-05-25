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
```

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
| `_site/` | Generated static site (commit after `build-site` or let CI build it) |
