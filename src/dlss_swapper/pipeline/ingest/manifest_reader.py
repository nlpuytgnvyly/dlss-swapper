import json
import logging
from dataclasses import dataclass
from pathlib import Path

log = logging.getLogger("dlss_swapper.ingest.manifest")


@dataclass
class DlssPackage:
    version: str
    channel: str
    sha256: str
    download_url: str
    dll_name: str


class ManifestReader:
    """Reads the remote-compatible manifest of known DLSS runtime builds."""

    def __init__(self, manifest_path: Path) -> None:
        self.manifest_path = Path(manifest_path)

    def load(self) -> list[DlssPackage]:
        if not self.manifest_path.exists():
            log.warning("manifest missing at %s", self.manifest_path)
            return []
        data = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        packages = [
            DlssPackage(
                version=entry["version"],
                channel=entry.get("channel", "release"),
                sha256=entry["sha256"],
                download_url=entry["url"],
                dll_name=entry["dll"],
            )
            for entry in data.get("packages", [])
        ]
        log.info("manifest loaded: %d packages", len(packages))
        return packages