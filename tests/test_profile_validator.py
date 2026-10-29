from pathlib import Path

from dlss_swapper.pipeline.ingest.game_scanner import GameCandidate
from dlss_swapper.pipeline.ingest.manifest_reader import DlssPackage
from dlss_swapper.pipeline.processors.version_matcher import SwapPlan
from dlss_swapper.pipeline.processors.profile_validator import ProfileValidator


def _plan(dir_path: str, engine: str | None, dll: str = "nvngx_dlss.dll") -> SwapPlan:
    game = GameCandidate(name=Path(dir_path).name, install_dir=Path(dir_path),
                         dlss_files=[Path(dir_path) / dll], engine_hint=engine)
    pkg = DlssPackage(version="3.8.2", channel="release", sha256="0" * 64,
                      download_url="https://example.invalid/x", dll_name=dll)
    return SwapPlan(game=game, current_version="3.5.0", target=pkg, needs_update=True)


def test_validator_blocks_anticheat_dirs():
    result = ProfileValidator().validate([_plan("/games/EasyAntiCheat-protected", "unreal")])
    assert result[0].ok is False


def test_validator_blocks_unity_frame_gen():
    result = ProfileValidator().validate([_plan("/games/IndieUnity", "unity", "nvngx_dlssg.dll")])
    assert result[0].ok is False


def test_validator_allows_plain_unreal():
    result = ProfileValidator().validate([_plan("/games/Shooter", "unreal")])
    assert result[0].ok is True