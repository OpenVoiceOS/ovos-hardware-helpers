
# Suggestions — `ovos_hardware_helpers`

> This file tracks proposed improvements for human developers. Each entry includes
> the problem/opportunity, proposed solution, and estimated impact.

### 1. Migrate `setup.py` → `pyproject.toml`

**Problem/Opportunity**: This repo still uses `setup.py` for packaging.
`setup.py` is legacy and `pyproject.toml` is the modern standard (PEP 517/518/621).

**Proposed Solution**:
1. Create `pyproject.toml` with `[project]` metadata and `[build-system]`.
2. Move `setup.cfg` content into `[project]` tables.
3. Remove `setup.py` (keep only if needed for legacy editable installs).

**Estimated Impact**: Medium — improves build reproducibility and tool compatibility.

### 2. Add type hints to public API

**Problem/Opportunity**: Functions and classes may lack full type annotations,
reducing IDE support and making the codebase harder to audit.

**Proposed Solution**: Annotate all public function signatures with PEP 484
type hints. Run `mypy` to verify.

**Estimated Impact**: Low effort, high long-term benefit for maintainability.

### 3. Expand unit test coverage

**Problem/Opportunity**: Test coverage may be incomplete, leading to undetected
regressions during refactors or dependency upgrades.

**Proposed Solution**: Review `test/` coverage report and add tests for
uncovered edge cases, especially around plugin loading and error paths.

**Estimated Impact**: Medium — reduces regression risk significantly.

### 4. Enrich this `SUGGESTIONS.md`

**Problem/Opportunity**: This file was auto-generated and contains only generic
suggestions.

**Proposed Solution**: After reading the source code, replace these stubs with
repo-specific, evidence-backed proposals (pointing to specific files/lines).

**Estimated Impact**: High — makes this file useful for future maintainers.
