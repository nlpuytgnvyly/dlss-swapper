# Contributing to dlss-swapper

Thanks for helping improve **DLSS 5 Manager**. Please keep contributions focused on the
pipeline architecture (`ingest -> processors -> outputs`) so stages stay independently testable.

## Dev setup

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\activate
pip install -e ".[dev]"
pytest -q
```

## Adding a new processor
1. Create a module under `src/dlss_swapper/pipeline/processors/`.
2. Implement a callable that takes the previous stage's payload and returns the next payload.
3. Register it in `app.py::DlssSwapperApp.run` in the correct position.
4. Add at least one test under `tests/`.

## Adding a DLSS DLL target
Extend the manifest schema only after confirming SHA-256 for the redistributable. Never
bundle NVIDIA binaries in this repo — reference the official redistribution channel.

## Style
- Line length <= 110, Ruff config in `pyproject.toml`.
- No network calls in unit tests; use the `ManifestDownloader` interface with a stub.

## Reporting DLSS version issues
Open an issue with the game name, engine hint, and the current `nvngx_dlss.dll` version
reported by `dlss-swapper --verbose`.