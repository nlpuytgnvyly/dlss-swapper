import json
import os
from pathlib import Path

DEFAULT_CONFIG = {
    "game_roots": [
        r"C:\Program Files (x86)\Steam\steamapps\common",
        r"C:\Program Files\Epic Games",
    ],
    "manifest_url": "https://cdn.dlss-swapper.dev/manifest.json",
    "report_dir": str(Path.home() / ".dlss-swapper" / "reports"),
}


class SettingsService:
    """Loads user settings from %APPDATA%\\dlss-swapper\\config.json."""

    def __init__(self, config_path: Path | None = None) -> None:
        base = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
        self.config_path = Path(config_path or base / "dlss-swapper" / "config.json")
        self._data = dict(DEFAULT_CONFIG)
        if self.config_path.exists():
            try:
                self._data.update(json.loads(self.config_path.read_text(encoding="utf-8")))
            except json.JSONDecodeError:
                pass

    def game_roots(self) -> list[str]:
        return list(self._data.get("game_roots", []))

    def manifest_path(self) -> Path:
        return Path(self._data["report_dir"]).parent / "manifest.json"

    def report_dir(self) -> Path:
        return Path(self._data["report_dir"])

    def save(self) -> None:
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        self.config_path.write_text(json.dumps(self._data, indent=2), encoding="utf-8")