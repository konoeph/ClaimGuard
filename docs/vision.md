# Vision

ClaimGuard exists because many LLM systems can produce confident answers before
their key claims have earned the right to be returned.

The project is built around a narrow but important idea:

```text
Important LLM claims should be constrained by policy, evidence, and tool results.
```

## The Boundary

ClaimGuard does not try to be a universal fact checker.

It does not decide whether a claim is true by itself. Instead, it answers a more
operational question:

```text
Is this claim allowed to be returned under the active evidence and tool policy?
```

That boundary matters. A policy can require citations, source facts, calculator
results, regulation evidence, test results, or other deterministic inputs before
the claim can pass. When those requirements are missing, ClaimGuard blocks or
downgrades the claim instead of letting the model present it as settled.

## Why Claim-Level Verification

Most LLM application reliability work happens around larger objects:

- the whole answer
- the prompt
- the retrieved context
- the tool-calling trace
- the JSON schema

Those layers are useful, but they can miss the smaller unit where risk often
appears: a specific conclusion inside an otherwise fluent answer.

ClaimGuard treats the claim as the unit of control. That makes it possible to
ask direct questions:

- Does this numeric conclusion cite source facts?
- Does it cite a calculator result?
- Does this compliance judgment cite a regulation and a source fact?
- Does this RAG answer bind its key conclusion to retrieved context?
- Are the cited evidence items marked as conflicting?

The goal is not to make LLM systems rigid. The goal is to make unsupported
certainty harder to ship.

## The v0.1 Philosophy

The first version should stay small and sharp.

v0.1 assumes that upstream systems provide structured claims, evidence, and tool
results. ClaimGuard then runs deterministic policy checks and returns a clear
verification result.

That means v0.1 intentionally avoids:

- automatic claim extraction
- LLM-as-verifier
- framework-specific adapters
- a web UI
- complex policy DSL features
- industry-specific policy packs

Those features may be useful later, but the first version should prove the core
runtime contract:

```text
Structured claims come in.
Policy checks run.
Unsupported claims are blocked, downgraded, or marked for review.
```

## Design Principles

### Be Framework-Agnostic

ClaimGuard should work after a plain LLM call, inside a RAG pipeline, behind an
HTTP endpoint, or as a node in an agent graph.

The core should not depend on any one orchestration framework.

### Prefer Explicit Policy

The first line of defense should be visible, deterministic policy checks.

Users should be able to read a YAML policy and understand why a claim passed or
failed.

### Keep Failure Useful

A failed claim should return enough structure for the caller to act:

- which claim failed
- which requirement was missing
- which references were invalid
- which fallback verdict is safe
- whether more evidence or a tool call is needed

Blocking is only useful when the next step is clear.

### Do Not Overclaim

ClaimGuard is a reliability constraint layer. It is not an oracle.

Passing a ClaimGuard policy means the claim satisfied the configured evidence
and tool requirements. It does not mean the world itself has been proven.

That distinction should stay visible in the API, docs, examples, and roadmap.

