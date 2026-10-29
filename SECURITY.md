# Security Policy

## Scope
`dlss-swapper` writes to game install directories and touches `nvngx_dlss*.dll` files.
If you find a vulnerability — path traversal in the scanner, unsafe DLL loading, or
manifest tampering — please report it privately.

## Reporting
Email **security@dlss-swapper.dev** with:
- affected version (`dlss-swapper --version`)
- reproduction steps
- impact assessment

Do **not** open a public GitHub issue for security reports.

## Threat model notes
- The manifest is fetched over HTTPS and every package is verified against a pinned SHA-256
  before being staged (`infrastructure/http_client.py::ManifestDownloader.download`).
- `SwapWriter` always backs up the original DLL under `%USERPROFILE%\.dlss-swapper\backups`
  before moving the staged payload into place.
- The pipeline refuses to touch directories whose path matches known anti-cheat hints
  (`EasyAntiCheat`, `BattlEye`, `anticheat`).
- No elevation is requested; run the tool with the same privileges as your game launcher.

## Supported versions
| Version | Supported |
|---------|-----------|
| 0.9.x   | yes       |
| < 0.9   | no        |