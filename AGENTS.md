# AGENTS.md

Conventions for AI agents and contributors working in this repository. These rules
apply to every pattern under `patterns/` and to the project as a whole.

> **Keep this file alive.** See [Keeping AGENTS.md up to date](#keeping-agentsmd-up-to-date)
> at the bottom. Whenever a new convention is introduced, agreed on in review, or
> applied to the codebase, update this file in the **same change** that introduces it.

---

## Project tooling

The project is managed with `uv`, with **all** configuration centralized in
`pyproject.toml`. Do not introduce parallel config files (`pytest.ini`,
`.coveragerc`, `setup.cfg`, `tox.ini`, etc.); fold any new setting into
`pyproject.toml` instead.

- **Python version**: `3.13` (pinned in `.python-version` and `requires-python`).
- **Dependency manager**: `uv` (lockfile `uv.lock` is committed; `.venv/` is local).
- **Task runner**: `poethepoet` via `[tool.poe.tasks]`. Never define ad-hoc shell
  scripts that duplicate a `poe` task; add or extend a task instead.
- **Formatter & linter**: `ruff` (replaces `black`). Configure under `[tool.ruff]`
  and `[tool.ruff.format]`. Enforced via **prek** (`.pre-commit-config.yaml`);
  use `uv run poe check`, not bare `ruff` invocations.
- **Git hooks**: `prek` (drop-in pre-commit runner). Install with
  `uv run prek install` after cloning.
- **Type checker**: `mypy` configured under `[tool.mypy]`.
- **Tests**: `pytest` + `pytest-cov`, all options under `[tool.pytest.ini_options]`
  and `[tool.coverage.*]`.

### Running things

Always invoke tools through `uv` so the right interpreter and lockfile are used:

```bash
uv run poe test          # pytest with coverage, fails under 100%
uv run poe check         # prek hooks (ruff check + format), used in CI
```

When adding a new pattern directory, scope `poe` tasks to it (don't broaden them
to the whole repo) and add it to `[tool.coverage.run].source`.

---

## Source-code conventions

### Determinism over mocks

When tests need stable output, make the **source** deterministic instead of
mocking in tests. Examples:

- Replace `uuid.uuid4()` with `uuid.uuid5(NAMESPACE, key)` and a fixed namespace
  (e.g. `uuid.UUID(int=5)`).
- Seed any randomness through an explicit parameter (`seed: int | None = None`)
  rather than relying on global state.

**Mocks are forbidden in tests.** If a test would need a mock, change the
production code so it doesn't.

### Type hints (Python 3.13)

- Prefer **built-in generics**: `list[X]`, `dict[K, V]`, `tuple[X, Y]`, `set[X]`.
- Prefer `collections.abc` over `typing` for abstract container types:
  `Sequence`, `MutableSequence`, `Mapping`, `MutableMapping`, `Iterable`,
  `Iterator`, `Callable`.
- Use `X | None` instead of `Optional[X]`, and `A | B` instead of `Union[A, B]`.
- Reserve `typing` imports for things `collections.abc` doesn't cover
  (`Any`, `Protocol`, `TypeVar`, `cast`, etc.).

For dataclass fields, type the field by **what callers should see** and use a
matching factory:

```python
from collections.abc import MutableSequence
from dataclasses import dataclass, field

@dataclass
class CustomerSupport:
    tickets: MutableSequence[SupportTicket] = field(default_factory=list[SupportTicket])
```

### Type aliases

- Define type aliases **in the SUT**, never in tests.
- Re-export them from the package's `__init__.py` so tests can import them.
- **Do not create simple rename aliases** (e.g. `ProcessingStrategy = TicketOrderingStrategy`).
  If the original name is good enough, use it directly.

### Package layout & exports

Every variant directory is a real package and re-exports its public API from
`__init__.py`:

```python
# patterns/.../solution_05/__init__.py
from .main import main
from .support import (
    CustomerSupport,
    SupportTicket,
    TicketOrderingStrategy,
    fifo_strategy,
    filo_strategy,
    random_strategy,
)

__all__ = [
    "CustomerSupport",
    "SupportTicket",
    "TicketOrderingStrategy",
    "fifo_strategy",
    "filo_strategy",
    "main",
    "random_strategy",
]
```

This lets tests import from the package root rather than reaching into submodules.

### Imports

- Use **absolute imports** for cross-module references
  (`from patterns.behavioural.strategy.problem import SupportTicket`).
- Relative imports are allowed **only inside a single package** (e.g. a
  `support/` subpackage importing from a sibling module).
- All imports go at the **top of the file**. Never import inside a test or
  function body.
- **Tests must import from the variant package root, never from submodules.**
  Write `from patterns.behavioural.state.problem import employee_id`, not
  `from patterns.behavioural.state.problem.support.ids import employee_id`. If
  a symbol a test legitimately needs isn't re-exported, fix the package's
  `__init__.py` (and its `support/__init__.py`) — don't reach into internals
  from a test.

### `if __name__ == "__main__":`

Keep these blocks minimal — they should only call `main()`. They are excluded
from coverage globally via `pyproject.toml`; do **not** add `# pragma: no cover`
to them.

---

## Test conventions

### Directory structure mirrors the SUT (1:1)

For every SUT module `patterns/.../<variant>/<pkg>/<mod>.py`, there is a test
module at `patterns/.../tests/<variant>/<pkg>/test_<mod>.py`. The test tree is a
mirror image of the source tree, including `__init__.py` files.

```
strategy/
  problem/support/app.py
  solution_01/support/app.py
  tests/
    conftest.py            # cross-variant fixtures and helpers
    utils.py               # shared assertion helpers
    test_parity.py         # cross-variant behavioural parity
    problem/
      conftest.py
      test_main.py
      support/
        test_app.py
        test_ticket.py
    solution_01/
      conftest.py
      test_main.py
      support/
        test_app.py
        test_ticket.py
```

### 100% coverage, enforced

- `[tool.coverage.run].source` includes both the SUT directories **and** the
  `tests/` directory.
- `[tool.coverage.report].fail_under = 100`.
- Global `exclude_lines` covers `if __name__ == "__main__":`, `TYPE_CHECKING`,
  `@abstractmethod`, and `Protocol` ellipsis (`^\s*\.\.\.$`).

If you add code, add tests; if you can't cover a line, it shouldn't exist.

### No mocks. No trivial tests.

- **No `unittest.mock`, `pytest-mock`, or monkeypatching SUT internals.** Make
  the source deterministic instead.
- Don't write tests that only assert `X is not None`, that re-exports exist,
  that a dataclass has the field you just declared, or that `__str__` returns
  the string you literally just constructed. Test **behaviour**.

### Every test must have an ACT

Arrange → Act → Assert. Each test body must contain at least one explicit ACT
statement — a call into the SUT being tested — followed by assertions on the
result. A test that only contains assertions on a fixture is not testing
anything; either move the call into the body or delete the test.

```python
def test_screen_returns_new_process_with_screened_description(
    sam_sourced_process: HiringProcess,  # Arrange (fixture)
    sourced_screen_score: float,
    second_screening_at: datetime,
) -> None:
    after = sam_sourced_process.screen(  # Act
        score=sourced_screen_score, at=second_screening_at,
    )

    assert sam_sourced_process is not after  # Assert
    assert str(after).startswith("screened (via ")
```

### One test per behaviour

For any class that exposes multiple methods (or any module that exposes
multiple branches), write **one focused test per method/branch**. Each test
exercises a single public API call from a known precondition; do not combine
multiple unrelated transitions in a single test.

The "problem" reference variant additionally gets one end-to-end test of
`main()` to lock in stdout for parity.

### Don't alias fixtures

When a fixture is already named for the precondition under test
(`screened_applied_process`, `interviewed_applied_process`, …), use it
**directly** as the receiver of the ACT and the operand of immutability
assertions. Don't introduce a local `before = fixture` alias.

```python
# Bad — pointless rename
def test_abandon(screened_applied_process, abandon_at):
    before = screened_applied_process
    after = before.abandon(at=abandon_at)
    assert before is not after

# Good — fixture name carries the meaning
def test_abandon(screened_applied_process, abandon_at):
    after = screened_applied_process.abandon(at=abandon_at)
    assert screened_applied_process is not after
```

### Fixtures

- Every fixture has explicit type annotations on parameters and return type.
- Move **all** object instantiation and multi-step setup into fixtures
  (`customer_support`, `support_ticket`, `support_tickets`,
  `screened_applied_process`, `interviewed_applied_process`, …). Tests that
  only call a function and assert on its return don't need a fixture; tests
  that build objects or chain transitions to set up a precondition do.
- **Compose preconditions by stacking small fixtures.** When a test needs a
  multi-step setup (e.g. applied → screen → interview → offer), express each
  step as a fixture that depends on the previous one (`screened_applied`,
  `interviewed_applied`, `offered_applied`). Tests then pick the right
  precondition by name; they never chain transitions inline.
- **Atomic fixtures over grouped data.** Prefer
  `applied_candidate_name`, `applied_role`, `recruiter` over a single
  `applied_data` tuple/dict. Each value gets its own fixture.
- **Side-effect fixtures** (those that mutate state and return nothing) are
  prefixed with `_`, are typed `-> None`, and are consumed via
  `@pytest.mark.usefixtures("_name")`, never by parameter injection. Example:
  `_populate_tickets`.
- Inject fixtures by **default pytest mechanism** (function parameter). Do not
  `from .conftest import some_fixture`.
- Constants used by tests (sample data, expected messages) live as fixtures in
  `conftest.py`, not as module-level constants. This keeps them in coverage and
  forces a single source of truth.
- Helpers that aren't fixtures (e.g. assertion helpers) live in `tests/utils.py`,
  not in `conftest.py`.

### Parametrization

Use `pytest.param(..., id=...)` for human-readable IDs. Pass real callables and
real instances — not strings to be looked up:

```python
@pytest.fixture(
    params=[
        pytest.param(fifo_strategy, id="fifo"),
        pytest.param(filo_strategy, id="filo"),
        pytest.param(partial(random_strategy, seed=5), id="random-seed-5"),
    ],
)
def processing_strategy(request: pytest.FixtureRequest) -> TicketOrderingStrategy:
    return request.param
```

Avoid fixtures that shadow SUT functions just to "wrap" them; import the
function directly and put it in `pytest.param`.

### Assertions

- Assert **content, not shape**. Compare full lists/objects, not just lengths.
- For `capsys` output, assign to an `output` variable and use `in` for partial
  matches (`assert expected in output`). Don't reconstruct the expected string
  with helpers; partial matching is enough and is robust to trailing newlines.
- Move expected-value computation into fixtures so tests stay declarative
  (e.g. `expected_random_tickets`, `fifo_customer_order`).
- For ordering checks across stdout, use the shared
  `assert_customers_in_order(output, names)` helper from `tests/utils.py`.

### Test granularity

For any module that exposes multiple strategies/branches:

- Write **one test per strategy** that exercises the strategy in isolation.
- Plus **one parametrized test** (`test_*_all_strategies`) that exhausts every
  strategy through the public entry point.

The "problem" variant is special: because it's the reference for parity, its
per-strategy tests **also** assert output **order**, not just membership.

### Cross-variant parity

`tests/test_parity.py` runs every solution's `main()` and asserts its `capsys`
output equals the problem's. Whenever a new solution variant is added, append
it to the parametrization there.

---

## Simulation feature contract

Every entry under `src/stlite_hello/features/<slice>/` is a free-market
simulation that participates in the shared analysis + presentation pipeline.
A slice **must** ship:

1. **`model.py`** with:
   - `SimpleParams` (2-4 knobs) and `AdvancedParams(SimpleParams)` (full
     parametrisation), both frozen Pydantic `BaseModel`s with `Field`
     bounds on every value.
   - `<Slice>Config(AggregationConfig)` whose `seed` default is a
     **distinct integer constant** unique to that slice and exported as
     `<SLICE>_DEFAULT_SEED`.
   - `<SLICE>_FEATURE` string constant used by `serialize_run`.
   - `simulate_once(params, rng) -> ReplicateResult` whose
     `focal_panel[t, i]` is the per-step focal quantity. The function
     must be deterministic for a given `np.random.default_rng(seed)`.
   - Any extra helper that replays the simulation for the special chart
     (e.g. `final_orderbook`, `final_snapshot`, `labor_market_history`,
     `final_graph`) so the chart never re-runs the analysis pipeline.

2. **`presentation/`** subpackage with one file per concern:
   - `view_models.py` — frozen `FeatureCopy` carrying **every string the
     page renders**:
     - `PageHeader` (title, icon, caption).
     - `ExampleCallout` with **four required fields** describing the
       real-world analogue: `headline` (one-line tagline), `summary` (the
       multi-sentence story — a concrete scenario the reader can picture,
       not a one-liner), `mechanism` (paragraph mapping that scenario
       onto the simulation's rules), and `references: tuple[Reference,
       ...]` listing the seminal papers. Each `Reference` carries
       `citation`, `title`, `venue`, and `url` so the renderer can build
       a "Seminal papers and further reading" expander with markdown
       links. Aim for ~3-5 references per slice.
     - `CommonChartHeadings` (axis labels, titles for every shared
       chart).
     - `ChartExplainers` — typically `DEFAULT_CHART_EXPLAINERS`, which
       supplies the "How to read it" / "What it tells you" copy shared
       across all simulations. Override only when a slice measures
       something the default copy mis-describes.
     - `special_chart_title` + a slice-specific
       `special_chart_explainer: ChartExplainer` (custom per slice
       because the chart is unique).
     - `DownloadHeading`, sidebar/seed/toggle labels, and
       `run_control` (typically `DEFAULT_RUN_CONTROL_LABELS`).
     - The slice-specific `*Heading` for the special chart. **All UI
       text lives here — no free-floating literals in controllers or
       sections.**
   - `sidebar.py` exposing `SidebarInputs` and `build_config(...)`. The
     public surface must take a `SidebarInputs(defaults=<Slice>Config)`
     and return the same frozen config type — never raw primitives.
   - `sections.py` re-exports the shared section renderers from
     `stlite_hello.presentation` (including
     `render_special_chart_explainer`), nothing more.
   - `special_chart.py` with:
     - One or more `pa.DataFrameModel`s for every dataframe the chart
       consumes,
     - A frozen `<Slice>Heading` Pydantic model,
     - A `SpecialChartInputs` Pydantic model,
     - Pure `build_*_chart(...)` returning `alt.TopLevelMixin`,
     - `render_special_chart(inputs: SpecialChartInputs)` that calls
       `st.altair_chart` with `width="stretch"` (cast to `alt.Chart`).
   - `controller.py` orchestrating page header → `render_example_callout`
     (real-world analogue + seminal-paper references, **must be rendered
     before the run toolbar**) → sidebar → `render_run_control` →
     section renderers → special chart →
     `render_special_chart_explainer`. The controller **must** gate
     every analysis call behind
     `render_run_control(RunControlInputs(..., download=copy.download))`;
     the simulation only runs when the user clicks the **Run simulation**
     button. The run-control helper renders a side-by-side toolbar with
     the **Run simulation** primary button and the JSON **Download**
     button (disabled until a run completes), so controllers must **not**
     call `render_download` themselves — passing `download=copy.download`
     into `RunControlInputs` is the only download wiring needed. Each
     shared `sections.render_*` takes a matching
     `copy.explainers.<name>` so a collapsible "How to read this
     chart" expander sits below every chart and table; the controller
     pulls them from `copy.explainers` (don't reach into
     `DEFAULT_CHART_EXPLAINERS` directly). If `render_run_control`
     returns `None`, the controller returns immediately (the helper
     renders the idle prompt and the disabled download). When the
     controller needs the slice's typed `AdvancedParams` (e.g. for the
     special chart), import it under `if TYPE_CHECKING:` and use
     `cast("AdvancedParams", outcome.params)` so pyright/mypy stay
     strict while pylint sees the import as type-only. Must not contain
     any free-floating literal strings — pull them from the
     `FeatureCopy` view model.

3. **`page.py`** that exposes `pages() -> list[StreamlitPage]` with a
   single `st.Page(render, ...)`. **No analysis or UI logic** beyond the
   page construction.

4. **`__main__.py`** containing only `from … import main` and the
   `if __name__ == "__main__"` block.

5. **`__init__.py`** re-exporting the model + presentation public API and
   providing a `main()` that mounts the page via `st.navigation`.

6. The slice is wired into `src/stlite_hello/features/__init__.py`
   `navigation()` under the appropriate group, and into the
   `dev-feature` poe task help string.

### Test contract

Mirror the layout under `tests/features/<slice>/`:

```
tests/features/<slice>/
  conftest.py                                  # *_fast_params, *_fast_config
  test_model.py                                # determinism + behavioural assertions
  test_page.py                                 # pages() returns one StreamlitPage
  test_main.py                                 # AppTest with session_state pre-populated
  test_reproducibility.py                      # byte-identical run + round-trip export
  presentation/
    test_sidebar.py                            # AppTest covering Advanced view
    test_special_chart.py                      # frame schema + chart layer count/title
```

`test_main.py` is split into two cases per slice:

1. A short *idle* assertion (`test_<slice>_main_renders_without_exception`)
   that calls `AppTest.run(timeout=10)` without any session-state setup
   and asserts the page rendered the idle prompt without exception. This
   guards the gated-run behaviour: opening a page **must not** trigger a
   simulation.
2. A *run-button* assertion that pre-populates `<slice>_simple_*`,
   `<slice>_runs`, `<slice>_resamples`, `<slice>_trajectory_samples`,
   then runs the script once, clicks the run button via
   `test.button(key="run_outcome::<slice>::button").click()`, and runs
   again with `timeout=120`. This exercises the full controller → run →
   render path and is what keeps coverage at 100%.

`test_sidebar.py` similarly pre-populates the same keys so the sidebar
test stays under the timeout budget.

Only one slice (`yard_sale`) keeps a syrupy snapshot of the export schema;
the rest only assert byte-identical round-trips, because the shared schema
is already snapshotted in `tests/analysis/test_export.py`.

## Adding a new pattern or variant — checklist

1. Create the SUT package with its own `__init__.py` re-exporting its public API.
2. Add a mirrored test directory: `tests/<variant>/...`, with `conftest.py`
   for variant-specific fixtures.
3. Add the SUT path to `[tool.coverage.run].source` in `pyproject.toml`.
4. If the variant introduces a new top-level pattern directory, scope the
   `format`/`lint`/`check` poe tasks accordingly.
5. Add a parity entry to `tests/test_parity.py` if applicable.
6. Run `uv run poe check && uv run poe test` and verify 100% coverage.
7. **Update this file** if the variant introduces any new convention.

---

## Keeping AGENTS.md up to date

This file is the source of truth for agent-facing conventions. **Treat it like
code**: stale conventions are bugs.

**When you must update this file (in the same PR/change):**

1. A new tool, command, or `poe` task is added or renamed.
2. A new test, typing, fixture, import, or naming convention is agreed on
   (in review, in chat, or by precedent set in committed code).
3. An existing convention is changed, relaxed, tightened, or removed.
4. A new pattern category, variant, or top-level directory is added.
5. A Python version, dependency, or coverage target changes.
6. A previously implicit rule is made explicit because an agent or contributor
   got it wrong.

**How to update it:**

- Edit the relevant section directly. Prefer editing existing sections over
  appending new ones.
- Keep examples minimal and concrete; cite real files only when stable.
- If a rule has an exception, document the exception **next to** the rule
  (see "problem variant" notes under [Test granularity](#test-granularity)).
- Remove obsolete guidance — don't leave it behind "deprecated" headers.
- Bump the **Last reviewed** date below whenever you touch the file.

**Agent instructions:** Before finishing any task that introduces a new
convention, re-read this file and update it. If you're unsure whether
something qualifies as a "new convention", err on the side of documenting it.
The corresponding user-level skills (`python-test-structure`,
`python-pytest-fixtures`, `python-modern-typing`, `python-uv-poe-ruff`) should
be kept in sync with this file; if you change a rule here, update the
matching skill in the same change.

---

_Last reviewed: 2026-05-26 (Python 3.13) — seven free-market simulation slices in place; gated runs via shared `render_run_control` (Run + disabled-until-ready Download toolbar) + numpy `RunBundle.panels` view to keep summarize fast; real-world analogue (narrative `ExampleCallout` with `headline`/`summary`/`mechanism`/`references` and seminal-paper links) rendered above the run toolbar; every chart carries a "How to read it" `ChartExplainer` expander, defaulting to `DEFAULT_CHART_EXPLAINERS` plus a per-slice `special_chart_explainer`._
