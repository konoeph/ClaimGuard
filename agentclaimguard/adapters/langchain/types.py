from collections.abc import Callable, Mapping
from typing import Any, TypeAlias

from agentclaimguard.core.result import VerificationResult


LangChainAdapterInput: TypeAlias = Any
LangChainAdapterOutput: TypeAlias = Any
FieldExtractor: TypeAlias = str | Callable[[Any, Any], list[Any] | None]
FieldMapper: TypeAlias = Mapping[str, FieldExtractor] | None
OutputMerger: TypeAlias = Callable[[Any, VerificationResult], Any]
