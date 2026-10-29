import logging
from dataclasses import dataclass
from typing import Sequence

from .pipeline.ingest import GameScanner, ManifestReader
from .pipeline.processors import DlssVersionMatcher, ProfileValidator
from .pipeline.outputs import SwapWriter, ReportEmitter
from .jobrunner.scheduler import JobScheduler
from .jobrunner.queue import JobQueue
from .core.services.settings_service import SettingsService
from .core.services.telemetry_service import TelemetryService
from .util.logging_setup import configure_logging

log = logging.getLogger("dlss_swapper.app")


@dataclass
class RuntimeContext:
    dry_run: bool
    verbose: bool
    game_roots: Sequence[str]


class DlssSwapperApp:
    """Entry point that wires the ingest -> process -> output pipeline."""

    def __init__(self) -> None:
        self.settings = SettingsService()
        self.telemetry = TelemetryService(settings=self.settings)

    def run(self, argv: Sequence[str]) -> int:
        ctx = RuntimeContext(
            dry_run="--dry-run" in argv,
            verbose="-v" in argv or "--verbose" in argv,
            game_roots=self.settings.game_roots(),
        )
        configure_logging(ctx.verbose)
        log.info("dlss-swapper starting dry_run=%s roots=%d", ctx.dry_run, len(ctx.game_roots))

        queue = JobQueue()
        scheduler = JobScheduler(queue)
        scheduler.enqueue(GameScanner(ctx.game_roots))
        scheduler.enqueue(ManifestReader(self.settings.manifest_path()))
        scheduler.enqueue(DlssVersionMatcher())
        scheduler.enqueue(ProfileValidator())
        scheduler.enqueue(SwapWriter(dry_run=ctx.dry_run))
        scheduler.enqueue(ReportEmitter(self.settings.report_dir()))

        result = scheduler.drain()
        self.telemetry.flush(result)
        log.info("pipeline complete: %s", result.summary())
        return 0 if result.ok else 1