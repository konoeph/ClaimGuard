from collections.abc import Callable, Mapping
from typing import Any, Literal, TypeAlias

from agentclaimguard.core.result import VerificationResult


LangGraphGuardState: TypeAlias = Mapping[str, Any]
LangGraphGuardUpdate: TypeAlias = dict[str, VerificationResult]
EvidenceGuardNode: TypeAlias = Callable[[LangGraphGuardState], LangGraphGuardUpdate]
GuardRoute: TypeAlias = Literal[
    "passed",
    "blocked",
    "need_check",
    "insufficient_evidence",
    "conflicting_evidence",
]
