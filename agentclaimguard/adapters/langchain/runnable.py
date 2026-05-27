from collections.abc import Mapping
from typing import Any

from langchain_core.runnables import Runnable, RunnableSerializable
from pydantic import ConfigDict

from agentclaimguard.core.policy import Policy
from agentclaimguard.core.result import VerificationResult
from agentclaimguard.core.runtime import AgentClaimGuard

from .types import FieldExtractor, FieldMapper, OutputMerger


_DEFAULT_FIELD_MAP: dict[str, str] = {
    "claims": "claims",
    "evidence": "evidence",
    "tool_results": "tool_results",
}


class GuardedRunnable(RunnableSerializable[Any, Any]):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    runnable: Runnable[Any, Any]
    policy: Policy
    field_map: FieldMapper = None
    result_key: str = "guard_result"
    output_key: str = "output"

    def invoke(self, input: Any, config=None, **kwargs: Any) -> Any:
        output = self.runnable.invoke(input, config=config, **kwargs)
        guard_result = self._run_guard(input=input, output=output)
        return self._merge_output(output=output, guard_result=guard_result)

    async def ainvoke(self, input: Any, config=None, **kwargs: Any) -> Any:
        output = await self.runnable.ainvoke(input, config=config, **kwargs)
        guard_result = self._run_guard(input=input, output=output)
        return self._merge_output(output=output, guard_result=guard_result)

    def _run_guard(self, *, input: Any, output: Any) -> VerificationResult:
        guard = AgentClaimGuard(policy=self.policy)
        field_map = dict(_DEFAULT_FIELD_MAP)
        if self.field_map:
            field_map.update(self.field_map)

        claims = _resolve_field(field_map["claims"], input=input, output=output) or []
        evidence = (
            _resolve_field(field_map["evidence"], input=input, output=output) or []
        )
        tool_results = (
            _resolve_field(field_map["tool_results"], input=input, output=output) or []
        )

        return guard.verify(
            claims=claims,
            evidence=evidence,
            tool_results=tool_results,
        )

    def _merge_output(self, *, output: Any, guard_result: VerificationResult) -> Any:
        if isinstance(output, Mapping):
            merged = dict(output)
            merged[self.result_key] = guard_result
            return merged

        return {
            self.output_key: output,
            self.result_key: guard_result,
        }


def create_guarded_runnable(
    runnable: Runnable[Any, Any],
    policy: Policy,
    *,
    field_map: FieldMapper = None,
    result_key: str = "guard_result",
    output_key: str = "output",
) -> GuardedRunnable:
    """Wrap a LangChain Runnable and attach AgentClaimGuard verification."""
    return GuardedRunnable(
        runnable=runnable,
        policy=policy,
        field_map=field_map,
        result_key=result_key,
        output_key=output_key,
    )


def _resolve_field(
    extractor: FieldExtractor,
    *,
    input: Any,
    output: Any,
) -> list[Any] | None:
    if callable(extractor):
        value = extractor(input, output)
    elif isinstance(extractor, str):
        value = _lookup_value(output, extractor)
        if value is None:
            value = _lookup_value(input, extractor)
    else:
        value = None

    if value is None:
        return None
    if isinstance(value, list):
        return value
    raise TypeError(
        "LangChain adapter field extractors must resolve to a list or None. "
        f"Got {type(value).__name__}."
    )


def _lookup_value(source: Any, key: str) -> Any:
    if isinstance(source, Mapping):
        return source.get(key)
    return None
