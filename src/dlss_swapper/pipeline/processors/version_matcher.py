import logging
from dataclasses import dataclass

from ..ingest.game_scanner import GameCandidate
from ..ingest.manifest_reader import DlssPackage

log = logging.getLogger("dlss_swapper.processors.matcher")


@dataclass
class SwapPlan:
    game: GameCandidate
    current_version: str | None
    target: DlssPackage
    needs_update: bool


class DlssVersionMatcher:
    """Compares installed DLL versions against the manifest to build swap plans."""

    def match(self, games: list[GameCandidate], packages: list[DlssPackage]) -> list[SwapPlan]:
        latest_by_name: dict[str, DlssPackage] = {}
        for pkg in packages:
            prev = latest_by_name.get(pkg.dll_name)
            if prev is None or self._version_tuple(pkg.version) > self._version_tuple(prev.version):
                latest_by_name[pkg.dll_name] = pkg

        plans: list[SwapPlan] = []
        for game in games:
            for dll in game.dlss_files:
                target = latest_by_name.get(dll.name)
                if target is None:
                    continue
                current = self._read_file_version(dll)
                needs = current is None or self._version_tuple(current) < self._version_tuple(target.version)
                plans.append(SwapPlan(game=game, current_version=current, target=target, needs_update=needs))
        log.info("matcher produced %d swap plans", len(plans))
        return plans

    @staticmethod
    def _version_tuple(value: str) -> tuple[int, ...]:
        parts = []
        for chunk in value.replace("v", "").split("."):
            digits = "".join(c for c in chunk if c.isdigit())
            parts.append(int(digits) if digits else 0)
        return tuple(parts)

    @staticmethod
    def _read_file_version(path) -> str | None:
        # Placeholder for Windows version-info via ctypes; returns None on non-Windows.
        try:
            from ctypes import windll, wintypes  # type: ignore
        except ImportError:
            return None
        return None