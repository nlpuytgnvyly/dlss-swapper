import json
import logging
from datetime import datetime
from pathlib import Path

log = logging.getLogger("dlss_swapper.outputs.report")


class ReportEmitter:
    """Emits a JSON report summarizing the last pipeline run."""

    def __init__(self, report_dir: Path) -> None:
        self.report_dir = Path(report_dir)

    def emit(self, summary: dict) -> Path:
        self.report_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
        out = self.report_dir / f"run-{stamp}.json"
        payload = {"generated_at": datetime.utcnow().isoformat() + "Z", **summary}
        out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        log.info("report written to %s", out)
        return out