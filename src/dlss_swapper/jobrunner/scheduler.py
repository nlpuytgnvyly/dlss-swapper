import logging
import time
from dataclasses import dataclass, field
from typing import Any

from .queue import JobQueue

log = logging.getLogger("dlss_swapper.scheduler")


@dataclass
class PipelineResult:
    ok: bool = True
    durations_ms: dict[str, float] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)

    def summary(self) -> dict:
        return {
            "ok": self.ok,
            "stages": list(self.durations_ms.keys()),
            "total_ms": round(sum(self.durations_ms.values()), 2),
            "errors": self.errors,
        }


class JobScheduler:
    """Drains a JobQueue, threading payloads between stages."""

    def __init__(self, queue: JobQueue) -> None:
        self.queue = queue

    def enqueue(self, stage) -> None:
        self.queue.push(stage)

    def drain(self) -> PipelineResult:
        result = PipelineResult()
        payload: Any = None
        while len(self.queue):
            job = self.queue.pop()
            if job is None:
                break
            started = time.perf_counter()
            try:
                payload = job.stage(payload) if callable(job.stage) else job.stage.run(payload)
                job.output = payload
            except Exception as exc:  # noqa: BLE001
                log.exception("stage %s failed", getattr(job.stage, "name", "?"))
                result.ok = False
                result.errors.append(f"{job.stage}: {exc}")
            finally:
                result.durations_ms[getattr(job.stage, "name", "stage")] = (
                    time.perf_counter() - started
                ) * 1000
        return result