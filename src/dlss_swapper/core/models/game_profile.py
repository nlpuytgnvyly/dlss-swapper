from dataclasses import dataclass, field


@dataclass
class GameProfile:
    name: str
    install_dir: str
    engine_hint: str | None = None
    dlss_dlls: list[str] = field(default_factory=list)
    pinned_version: str | None = None
    excluded: bool = False

    def pin(self, version: str) -> None:
        self.pinned_version = version

    def exclude(self) -> None:
        self.excluded = True