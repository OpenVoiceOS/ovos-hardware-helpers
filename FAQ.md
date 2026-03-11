
# FAQ — `ovos_hardware_helpers`

## What is `ovos_hardware_helpers`?
`ovos_hardware_helpers` is Helper scripts for some hardware.

## How do I install it?
```bash
pip install ovos_hardware_helpers
```
Or for development:
```bash
uv pip install -e ovos-hardware-helpers/
```

## Where do I report bugs?
Open an issue on the GitHub repository. Ensure you are targeting the `dev` branch for fixes.

## How do I run tests?
```bash
uv run pytest test/unittests/test_hardware.py -v --cov=ovos_hardware_helpers --cov-report=term-missing
```

The test suite includes 44+ tests covering all LED animations, abstract base classes, and color handling with 91% code coverage.

## How do I contribute?
1. Fork the repository and create a feature branch from `dev`.
2. Write tests for your changes.
3. Open a PR targeting the `dev` branch.
4. Ensure CI passes before requesting review.

## What Python versions are supported?
See `QUICK_FACTS.md` — currently `>=3.9`.

## What build system does this project use?
As of v1.0.0, `ovos_hardware_helpers` uses modern PEP 517/518-compliant `pyproject.toml` configuration with `setuptools` as the backend. The version is dynamically resolved from `ovos_hardware_helpers/version.py`. The old `setup.py` is no longer needed and can be removed in future versions.
