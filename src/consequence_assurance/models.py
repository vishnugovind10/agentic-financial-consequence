"""Small typed model for consequence envelopes and decisions."""

from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any


class Result(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    ABSTAIN = "ABSTAIN"


class Decision(str, Enum):
    GO = "GO"
    CONDITIONAL_GO = "CONDITIONAL_GO"
    NO_GO = "NO_GO"
    ABSTAIN = "ABSTAIN"


@dataclass(frozen=True)
class Evaluation:
    scenario: str
    checks: dict[str, Result]
    final_decision: Decision
    reasons: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["checks"] = {key: value.value for key, value in self.checks.items()}
        data["final_decision"] = self.final_decision.value
        data["reasons"] = list(self.reasons)
        return data
