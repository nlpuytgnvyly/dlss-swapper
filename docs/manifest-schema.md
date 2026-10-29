# Manifest Schema (v1)

The manifest is fetched from `https://cdn.dlss-swapper.dev/manifest.json` and lists every
known DLSS runtime build the manager can swap to.

```json
{
  "schema": 1,
  "generated_at": "2026-02-14T12:00:00Z",
  "packages": [
    {
      "version": "3.8.2",
      "channel": "release",
      "dll": "nvngx_dlss.dll",
      "sha256": "…64 hex chars…",
      "url": "https://cdn.dlss-swapper.dev/pkgs/3.8.2/nvngx_dlss.dll"
    }
  ]
}
```

## Fields
- `version` — semantic version string, compared numerically by `DlssVersionMatcher`.
- `channel` — `release` or `preview`; preview packages are opt-in via `--preview`.
- `dll` — one of `nvngx_dlss.dll`, `nvngx_dlssg.dll`, `nvngx_dlssd.dll`.
- `sha256` — hex digest of the DLL; **required**, downloads fail closed if it mismatches.
- `url` — direct HTTPS URL to the redistributable.

## Compatibility rules
- `nvngx_dlssg.dll` (frame generation) is rejected for Unity games by `ProfileValidator`.
- `nvngx_dlssd.dll` (ray reconstruction) requires DLSS 3.5+ runtime; matcher enforces this.