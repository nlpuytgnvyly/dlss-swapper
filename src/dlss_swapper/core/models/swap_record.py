from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class SwapRecord:
    game_name: str
    dll_name: str
    from_version: str
    to_version: str
    backup_path: str
    applied_at: datetime

    def as_dict(self) -> dict:
        return {
            "game": self.game_name,
            "dll": self.dll_name,
            "from": self.from_version,
            "to": self.to_version,
            "backup": self.backup_path,
            "applied_at": self.applied_at.isoformat(),
        }