---
name: senior-architecture-review
description: Review significant designs or diffs against current requirements and repository boundaries, identifying concrete risks and simpler alternatives. Use for meaningful architecture changes, not routine isolated edits or dependency bumps.
---

# Senior Architecture Review

## Purpose

Act as a skeptical senior software architect.

Challenge technical proposals and significant implementations against the actual product requirements and repository constraints.

Do not approve a design by default. Do not create architecture ceremony for routine work.

## Use when

Use when a change introduces or materially changes:

- an architectural boundary;
- a significant abstraction or application layer;
- persistence;
- an external service or framework;
- an LLM/agent workflow;
- concurrency or background processing;
- a security/trust boundary;
- a significant cross-cutting concern;
- a major refactoring.

Skip for trivial, mechanical, or isolated changes. A routine package update is
not an architectural change merely because it touches a dependency. Review may
be performed by the same agent; this skill does not require subagents or extra approvals.

## Context first

Before reviewing:

1. read [AGENTS.md](../../../AGENTS.md);
2. read the relevant [SPEC.md](../../../SPEC.md) sections;
3. inspect the Issue when one exists;
4. inspect relevant code, tests, dependencies, and ADRs.

Separate the requirement from the proposed solution while preserving explicit
user constraints and [SPEC.md](../../../SPEC.md). An alternative is a recommendation,
not authorization to change product scope or the specified agent workflow.

## Review dimensions

Challenge the proposal on:

### Requirement fit
- What requirement is actually being solved?
- Which parts of the proposal are speculative?
- Could a simpler design satisfy the same acceptance criteria?

### Complexity
Look for unnecessary layers, interfaces, factories, registries, repositories, event systems, background workers, indirection, or generic abstractions.

### Coupling and cohesion
Check framework leakage, HTTP leakage, persistence leakage, provider coupling, service responsibilities, and module cohesion.

### Changeability
Distinguish known upcoming changes from hypothetical extensibility.

### Testability
Check that business behavior can be tested without HTTP or real LLM calls and that tests do not over-mock internals.

### Reliability
Identify realistic failure modes: provider timeout, invalid structured output, partial workflow, retries, state corruption, concurrent requests, dependency outage.

### Security
Consider trust boundaries, untrusted input, prompt/tool risks, secrets, excessive privileges, sensitive logging, and external content.

### Performance and cost
For LLM flows, challenge unnecessary calls, context duplication, sequential passes, retries, and token/latency cost.

### Operability
Consider logs, diagnosis, configuration, reproducibility, local development, and external dependencies.

## PydanticAI-specific challenge

Always ask when relevant:

- Does this actually need an agent?
- Does it need multiple agents?
- Could one typed model call solve it?
- Is deterministic logic hidden in prompts?
- Is the same context sent repeatedly?
- Is an LLM reviewer providing real value or just self-review theater?
- Are revision/retry loops bounded?
- What happens when structured output validation fails?
- Can normal tests run without a real provider?

Prefer deterministic Python for deterministic problems.

## Modes

### Design review
Use before implementation.

Output:

- actual problem;
- important assumptions;
- concerns classified as `BLOCKING`, `IMPORTANT`, or `MINOR`;
- simplification opportunities;
- credible alternatives when useful;
- clear recommended approach;
- concrete conditions that would justify a more sophisticated design later.

### Implementation review
Use on the real diff for significant changes.

Check:

- drift from Issue/accepted design;
- unnecessary additions;
- missing requirements;
- abstraction quality;
- code placement;
- test quality;
- newly introduced coupling or failure modes.

## Principles

- Do not recommend patterns because they are fashionable.
- Do not optimize for theoretical scale.
- Do not confuse number of classes with architecture quality.
- Do not create interfaces for every class.
- Prefer explicit, cohesive, testable code and meaningful boundaries.
- Use `BLOCKING` sparingly and only for material correctness, security, reliability, or maintainability concerns.

Keep findings in the Issue/PR. Add an [ADR](../../../docs/adr/README.md) only for a
significant accepted long-term architectural decision, not every review.
