#!/usr/bin/env bash
# Quick local scan without touching DLLs. Useful for debugging the scanner on a dev box.
set -euo pipefail

python -m dlss_swapper --dry-run --verbose "$@"