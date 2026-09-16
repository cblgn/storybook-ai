---
name: refine-work-item
description: Turn an informal non-trivial request into a scoped English GitHub Issue, reusing matching work items. Use before implementation when no suitable Issue exists.
---

# Refine Work Item

## Purpose

Turn an informal non-trivial request into a small, actionable GitHub Issue.

This skill produces a work item. It does not implement it.

## Use when

Use when the user requests a feature, bug fix, refactoring, CI change, or other non-trivial change and no suitable GitHub Issue already exists.

Skip for trivial typo, formatting, or tiny documentation fixes where an Issue would add more overhead than value.

## Workflow

1. Read [AGENTS.md](../../../AGENTS.md).
2. Read the relevant parts of [SPEC.md](../../../SPEC.md).
3. Inspect the existing implementation related to the request.
4. Search open and related closed GitHub Issues and reuse an existing matching Issue when appropriate.
5. Distinguish the requirement from a proposed solution while respecting explicit
   user choices and constraints; do not silently replace the requested scope.
6. Refine the request into the smallest independently deliverable change.
7. If the request is too large for one reasonable PR, propose and create multiple Issues instead of one oversized Issue.
8. Create or update the Issue in English when authorized; reuse existing authorization.
   Follow the repository [issue templates](../../../.github/ISSUE_TEMPLATE/feature.md);
   bugs also need reproduction steps and expected/actual behavior from the
   [bug template](../../../.github/ISSUE_TEMPLATE/bug.md).

## Issue structure

Use:

### Context
Why the change is useful or necessary.

### Objective
What should be possible when the work is complete.

### Requirements
Clear functional requirements and only relevant technical constraints.

### Acceptance criteria
Concrete, verifiable checkboxes.

### Technical notes
Only constraints or observations useful to implementation. Do not prematurely prescribe architecture.

### Out of scope
Explicitly state what this iteration will not implement.

## Rules

- The Issue describes what should change and why.
- Do not copy large parts of [SPEC.md](../../../SPEC.md); link or reference the relevant behavior instead.
- Do not create local Markdown task files.
- Do not implement code in this skill.
- Do not create architecture ceremony for a straightforward change.
- If a meaningful architecture decision is already apparent, recommend [senior-architecture-review](../senior-architecture-review/SKILL.md) before implementation.

If remote operations are prohibited or unavailable, prepare the Issue text locally
and report the missing linkage without claiming publication. A related closed
Issue provides context; it is not a tracker for new scope.

## Completion

Report:

- Issue number and URL;
- concise scope summary;
- whether architecture review is recommended;
- whether the request was split into multiple Issues.

If implementation is already requested and authorized, continue with
[implement-issue](../implement-issue/SKILL.md); stop after refinement only for a
refinement-only request or a genuine blocker.
