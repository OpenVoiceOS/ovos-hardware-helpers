
# ovos-hardware-helpers — Audit Report

## Documentation Status
- [ ] AGENTS.md Header Format
- [ ] QUICK_FACTS.md (Moved from docs/)
- [ ] FAQ.md (Moved from docs/)
- [ ] MAINTENANCE_REPORT.md
- [x] AUDIT.md
- [ ] SUGGESTIONS.md
- [ ] docs/index.md

## Technical Debt & Issues
- `[MINOR]` **ci**: Action `pypa/gh-action-pypi-publish` pinned to `@master` (should be `@release/v1`)
- `[MINOR]` **ci**: Action `ad-m/github-push-action` pinned to `@master` (should be `@pinned ref`)
- `[INFO]` **tests**: Only 1 test file found (test_hardware.py) — coverage may be low
- `[INFO]` **packaging**: Uses setup.py (consider migrating to pyproject.toml)

## Next Steps
- Pin `pypa/gh-action-pypi-publish` to `@release/v1` instead of `@master`
- Pin `ad-m/github-push-action` to `@pinned ref` instead of `@master`
- Migrate from setup.py to pyproject.toml
