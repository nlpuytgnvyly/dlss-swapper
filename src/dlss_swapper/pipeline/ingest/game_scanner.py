import logging
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Sequence

log = logging.getLogger("dlss_swapper.ingest.scanner")

DLSS_DLL_NAMES = ("nvngx_dlss.dll", "nvngx_dlssg.dll", "nvngx_dlssd.dll")
KNOWN_STEAM_LIBRARY_HINTS = ("steamapps", "common")


@dataclass
class GameCandidate:
    name: str
    install_dir: Path
    dlss_files: list[Path] = field(default_factory=list)
    engine_hint: str | None = None


class GameScanner:
    """Walks configured roots and yields GameCandidate records with DLSS DLLs."""

    def __init__(self, roots: Sequence[str], max_depth: int = 5) -> None:
        self.roots = [Path(r) for r in roots if r and Path(r).exists()]
        self.max_depth = max_depth

    def _walk_depth(self, root: Path) -> Iterable[Path]:
        base = len(root.parts)
        for dirpath, dirnames, filenames in os.walk(root):
            depth = len(Path(dirpath).parts) - base
            if depth >= self.max_depth:
                dirnames[:] = []
            lower = {d.lower() for d in dirnames}
            if lower & set(KNOWN_STEAM_LIBRARY_HINTS):
                dirnames[:] = [d for d in dirnames if d.lower() not in KNOWN_STEAM_LIBRARY_HINTS]
            yield Path(dirpath)

    def discover(self) -> list[GameCandidate]:
        found: list[GameCandidate] = []
        for root in self.roots:
            for folder in self._walk_depth(root):
                dlls = [folder / n for n in DLSS_DLL_NAMES if (folder / n).exists()]
                if not dlls:
                    continue
                found.append(
                    GameCandidate(
                        name=folder.name,
                        install_dir=folder,
                        dlss_files=dlls,
                        engine_hint=self._detect_engine(folder),
                    )
                )
        log.info("scanner discovered %d candidate game dirs", len(found))
        return found

    @staticmethod
    def _detect_engine(folder: Path) -> str | None:
        if (folder / "Engine" / "Binaries").exists():
            return "unreal"
        if (folder / "UnityPlayer.dll").exists():
            return "unity"
        return None