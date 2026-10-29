from pathlib import Path

from dlss_swapper.pipeline.ingest.game_scanner import GameCandidate
from dlss_swapper.pipeline.ingest.manifest_reader import DlssPackage
from dlss_swapper.pipeline.processors.version_matcher import DlssVersionMatcher


def _pkg(version: str, dll: str = "nvngx_dlss.dll") -> DlssPackage:
    return DlssPackage(version=version, channel="release", sha256="0" * 64,
                       download_url="https://example.invalid/x", dll_name=dll)


def test_matcher_prefers_highest_version():
    game = GameCandidate(name="GameA", install_dir=Path("/tmp/GameA"),
                         dlss_files=[Path("/tmp/GameA/nvngx_dlss.dll")])
    plans = DlssVersionMatcher().match([game], [_pkg("3.7.10"), _pkg("3.8.2")])
    assert len(plans) == 1
    assert plans[0].target.version == "3.8.2"
    assert plans[0].needs_update is True


def test_matcher_handles_missing_dll():
    game = GameCandidate(name="GameB", install_dir=Path("/tmp/GameB"), dlss_files=[])
    assert DlssVersionMatcher().match([game], [_pkg("3.8.2")]) == []