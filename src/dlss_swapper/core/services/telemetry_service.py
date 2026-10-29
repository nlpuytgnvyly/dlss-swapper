import json
import logging
import os
from pathlib import Path

from .settings_service import SettingsService

log = logging.getLogger("dlss_swapper.telemetry")


class TelemetryService:
    """Opt-in local-only telemetry; writes a rolling event log under the user profile."""

    def __init__(self, settings: SettingsService, enabled: bool | None = None) -> None:
        self.settings = settings
        self.enabled = enabled if enabled is not None else os.environ.get("DLSS_SWAPPER_TELEMETRY", "0") == "1"
        self.log_path = Path(settings.report_dir()).parent / "telemetry.jsonl"

    def flush(self, result) -> None:
        if not self.enabled:
            return
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        with self.log_path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps({"event": "pipeline_run", **result.summary()}) + "\n")
        log.debug("telemetry flushed to %s", self.log_path)