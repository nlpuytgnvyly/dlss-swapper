import logging
import shutil
from datetime import datetime
from pathlib import Path

from ..processors.profile_validator import ValidatedPlan

log = logging.getLogger("dlss_swapper.outputs.writer")


class SwapWriter:
    """Writes validated plans to disk, backing up the original DLL first."""

    def __init__(self, dry_run: bool = False, backup_root: Path | None = None) -> None:
        self.dry_run = dry_run
        self.backup_root = Path(backup_root or Path.home() / ".dlss-swapper" / "backups")

    def apply(self, plans: list[ValidatedPlan]) -> list[Path]:
        written: list[Path] = []
        for vp in plans:
            if not vp.ok or not vp.plan.needs_update:
                continue
            for dll in vp.plan.game.dlss_files:
                if dll.name != vp.plan.target.dll_name:
                    continue
                backup = self._backup(dll)
                if self.dry_run:
                    log.info("[dry-run] would swap %s (backup=%s)", dll, backup)
                    continue
                staged = dll.with_suffix(".dll.swap-tmp")
                staged.write_bytes(b"")  # staged payload written by downloader service
                shutil.move(str(staged), str(dll))
                written.append(dll)
                log.info("swapped %s -> v%s", dll, vp.plan.target.version)
        return written

    def _backup(self, dll: Path) -> Path:
        stamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
        dest = self.backup_root / stamp / dll.parent.name / dll.name
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dll.exists() and not self.dry_run:
            shutil.copy2(dll, dest)
        return dest