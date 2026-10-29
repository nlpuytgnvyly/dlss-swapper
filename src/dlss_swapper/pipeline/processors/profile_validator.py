import logging
from dataclasses import dataclass

from .version_matcher import SwapPlan

log = logging.getLogger("dlss_swapper.processors.validator")

BLOCKED_PROCESS_HINTS = ("anticheat", "easyanti", "battleye")


@dataclass
class ValidatedPlan:
    plan: SwapPlan
    ok: bool
    reason: str | None = None


class ProfileValidator:
    """Guards against swapping DLLs in protected or unsupported directories."""

    def validate(self, plans: list[SwapPlan]) -> list[ValidatedPlan]:
        out: list[ValidatedPlan] = []
        for plan in plans:
            lowered = str(plan.game.install_dir).lower()
            if any(hint in lowered for hint in BLOCKED_PROCESS_HINTS):
                out.append(ValidatedPlan(plan=plan, ok=False, reason="protected directory"))
                continue
            if plan.game.engine_hint == "unity" and plan.target.dll_name.endswith("_dlssg.dll"):
                out.append(ValidatedPlan(plan=plan, ok=False, reason="frame-gen unsupported"))
                continue
            out.append(ValidatedPlan(plan=plan, ok=True))
        log.info("validator approved %d/%d plans", sum(p.ok for p in out), len(out))
        return out