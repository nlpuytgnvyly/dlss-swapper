# Pipeline Architecture

`dlss-swapper` runs every operation as a chain of stages drained by `JobScheduler`.
Each stage receives the previous stage's return value and can be replaced independently.

```
GameScanner ──► ManifestReader ──► DlssVersionMatcher ──► ProfileValidator ──► SwapWriter ──► ReportEmitter
```

| Stage | Input | Output | Module |
|-------|-------|--------|--------|
| `GameScanner` | roots (list[str]) | `list[GameCandidate]` | `pipeline/ingest/game_scanner.py` |
| `ManifestReader` | manifest path | `list[DlssPackage]` | `pipeline/ingest/manifest_reader.py` |
| `DlssVersionMatcher` | games + packages | `list[SwapPlan]` | `pipeline/processors/version_matcher.py` |
| `ProfileValidator` | swap plans | `list[ValidatedPlan]` | `pipeline/processors/profile_validator.py` |
| `SwapWriter` | validated plans | `list[Path]` written | `pipeline/outputs/swap_writer.py` |
| `ReportEmitter` | summary dict | report path | `pipeline/outputs/report_emitter.py` |

## Dry-run mode
Pass `--dry-run` to run the pipeline end-to-end without writing DLLs. The `SwapWriter`
still computes backup paths so you can inspect what would change.

## Backups
Every swap is preceded by a copy of the original DLL under
`%USERPROFILE%\.dlss-swapper\backups\<timestamp>\<game>\<dll>`. Restore manually by copying
back if a game misbehaves with the new DLSS runtime.