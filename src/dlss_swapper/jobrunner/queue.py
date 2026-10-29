from dataclasses import dataclass, field
from typing import Any, Protocol


class Stage(Protocol):
    name: str

    def __call__(self, payload: Any) -> Any: ...


@dataclass
class Job:
    stage: Stage
    payload: Any = None
    output: Any = None
    error: str | None = None


@dataclass
class JobQueue:
    jobs: list[Job] = field(default_factory=list)

    def push(self, stage: Stage, payload: Any = None) -> None:
        self.jobs.append(Job(stage=stage, payload=payload))

    def pop(self) -> Job | None:
        return self.jobs.pop(0) if self.jobs else None

    def __len__(self) -> int:
        return len(self.jobs)