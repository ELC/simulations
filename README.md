# Free-Market Simulations

An in-browser suite of seven micro-founded, stochastic free-market simulations
built on [Stlite](https://stlite.net/browser/) (Streamlit on Pyodide) and
deployed as a static GitHub Pages site. Every simulation reports the same
panel of bootstrap-CI metrics and mobility statistics, draws the same family
of comparison charts, and adds one chart that is specific to the mechanism
under study.

## The seven simulations

| Group | Slice | Mechanism | Real-world analogue | Model-specific chart |
|-------|-------|-----------|---------------------|----------------------|
| Wealth dynamics | `yard_sale` | Random pairwise wealth swap with a small win bias | OPEC+ crude-oil quota negotiations would be too specific - here, neighbourhood swap meets | Wealth condensation heatmap |
| Wealth dynamics | `kinetic_exchange` | Chakraborti-Chakrabarti exchange with per-agent savings rates | Informal money-lender networks in pre-industrial bazaars | Wealth-vs-savings-rate scatter |
| Wealth dynamics | `sugarscape` | Spatial harvest-and-metabolism on a toroidal sugar landscape | Artisanal gold panning along a watershed | Sugar-landscape heatmap with agent bubbles |
| Market structure | `double_auction` | Continuous double auction with bid/ask shading | Day-ahead electricity spot markets | Marshallian supply-demand cross |
| Market structure | `cournot` | N-firm Cournot best-response with adjustable inertia | OPEC+ output-quota deliberations | Best-response trajectory in (q1, q2) space |
| Labor markets | `labor_matching` | Mortensen-Pissarides search-and-matching | Seasonal hospitality hiring in a tourist town | Beveridge curve |
| Network effects | `preferential_attachment` | Barabási-Albert graph growth | Academic citation networks | Zipf log-log degree vs rank |

All seven reach the same headline metrics (Gini, top-1/5/10 % shares,
Herfindahl-Hirschman, P90/P10 ratio) and mobility metrics (rank-rank Spearman,
quintile staircase rate, decile turnover, bottom-to-top rise count, Shorrocks
index) and run on a configurable number of independently-seeded replicates
(default 30).

## Stack

- **Stlite / Pyodide 0.29.3** for in-browser execution.
- **Streamlit** with `st.navigation` groups for sidebar organisation.
- **NumPy + SciPy + Statsmodels + NetworkX** for simulation and statistics,
  pinned to the versions Pyodide ships.
- **Pandera** schemas around every internal DataFrame; **Pydantic** models
  around every config, parameter set, and view-model.
- **Altair** for every chart.
- **uv + poethepoet + ruff + mypy + pylint + pytest-cov + syrupy** for the
  development loop.

## Quick start

```bash
uv sync --group dev
uv run poe dev                       # launch the full app locally
uv run poe dev-feature cournot       # run a single simulation in isolation
uv run poe build-site                # generate _site/ for GitHub Pages
uv run poe serve-site                # serve _site/ at http://localhost:8000
uv run poe test                      # pytest with 100% coverage gate
uv run poe check                     # ruff + mypy + pylint (matches CI)
uv run poe snapshot-update           # refresh syrupy snapshots
uv run poe sync-pyodide-constraints  # refresh Pyodide lock + uv constraints
```

The available `dev-feature` slices are
`yard_sale | kinetic_exchange | sugarscape | double_auction | cournot | labor_matching | preferential_attachment`.

## How a feature is shaped

Every simulation lives under `src/stlite_hello/features/<slice>/` and
follows the same six-file contract:

```
features/<slice>/
  model.py                       # SimulationConfig, params, simulate_once(...)
  page.py                        # thin wrapper that returns the StreamlitPage
  __main__.py                    # python -m stlite_hello.features.<slice>
  __init__.py                    # public re-exports (model + presentation)
  presentation/
    controller.py                # sidebar -> analysis -> sections orchestrator
    sidebar.py                   # build_config(...) returning the frozen config
    sections.py                  # re-exports the shared section renderers
    special_chart.py             # the model-specific chart + its inputs schema
    view_models.py               # frozen Pydantic models with all UI text
```

Every metric, chart, CI computation and export is delegated to the shared
`stlite_hello/analysis/` and `stlite_hello/presentation/` packages, so a new
simulation only writes the mechanism and the special chart.

## Stlite / Pyodide alignment

`@stlite/browser@1.7.3` bundles **Pyodide 0.29.3**. The repo keeps that
inventory in `constraints/pyodide-lock.json` and mirrors every PEP 508-valid
package into `[tool.uv].constraint-dependencies` in `pyproject.toml`, so
`uv lock` resolves identical versions to the ones the browser will install.

After bumping `pyodide_version` in `src/stlite_hello/pyodide_sync/config.py`
(or `stlite_browser_version` in `src/stlite_hello/site/config.py`), run
`uv run poe sync-pyodide-constraints`, resolve any lock conflicts in
`[project]` / `[dependency-groups].dev`, then `uv lock`.

## GitHub Pages

1. Enable **GitHub Pages** -> source: **GitHub Actions**.
2. Push to `main`; the **Deploy GitHub Pages** workflow runs `poe build-site`
   and publishes `_site/`.

The static site loads `@stlite/browser` from jsDelivr and Pyodide installs
`numpy`, `pandas`, `scipy`, `statsmodels`, `networkx`, `altair`, `pandera`
and `pydantic` in the browser before mounting the app.

## Project layout

| Path | Purpose |
|------|---------|
| `src/stlite_hello/app.py` | Streamlit entrypoint; wires `features.navigation()` into `st.navigation` |
| `src/stlite_hello/features/` | The seven simulation slices, each runnable on its own via `python -m` |
| `src/stlite_hello/analysis/` | Bootstrap-CI, KDE, AIC fits, mobility metrics, JSON export |
| `src/stlite_hello/presentation/` | Shared sidebar/sections/view-models reused by every slice |
| `src/stlite_hello/site/` | Builds `_site/` for GitHub Pages |
| `src/stlite_hello/pyodide_sync/` | Vendors `pyodide-lock.json` and syncs `[tool.uv].constraint-dependencies` |
| `_site/` | Generated static site (commit after `build-site` or let CI build it) |
