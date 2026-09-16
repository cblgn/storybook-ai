---
name: harden-repository
description: Inspect, safely change and verify GitHub repository security, Actions, rulesets, Dependabot, CodeQL and Sonar configuration. Use for repository hardening, not normal product features or merely running existing checks.
---

# Harden Repository

## Purpose

Audit and harden the GitHub repository, CI/CD security, dependency security, and Sonar integration without weakening developer usability.

## Use when

Use for work involving:

- GitHub repository settings;
- branch rulesets;
- Actions permissions;
- GitHub Actions supply-chain security;
- Dependabot;
- CodeQL;
- dependency audits;
- secret scanning / push protection;
- SonarQube Cloud;
- security badges or repository security verification.

Do not run this skill for normal product features. Follow
[refine-work-item](../refine-work-item/SKILL.md),
[implement-issue](../implement-issue/SKILL.md) and
[prepare-pull-request](../prepare-pull-request/SKILL.md) for the relevant delivery phases.

Read the maintained [security baseline](../../../docs/repository-security.md) and
[expected ruleset](../../../.github/rulesets/protect-main.json) for exact checks and
allowed vendors. They remain authoritative; this skill does not grant permission
to change remote settings. Reuse task authorization, preserve visibility and
unrelated settings, and use free CLI/API capabilities where possible.

## Workflow

1. Read [AGENTS.md](../../../AGENTS.md), [SECURITY.md](../../../SECURITY.md), and relevant repository documentation.
2. Inspect current GitHub settings through `gh` / GitHub APIs before changing anything.
3. Inspect existing workflows, Dependabot, Sonar config, and security tooling.
4. Determine the desired state and compare it with the effective remote state.
5. Explain the gap and proposed verification, then apply only justified, authorized changes.
6. Verify the effective state after every remote configuration change.
7. Run the existing read-only [verifier](../../../scripts/verify_github_security.py)
   from the repository root: `python3 scripts/verify_github_security.py`.
   Inspect its exit status; use specific APIs for protections outside its coverage.
8. Report any protection that cannot be enabled on the current plan rather than silently downgrading it.

## GitHub baseline

Preserve these required protections:

- protected `main`;
- PR-based integration;
- required CI/security checks, current-base enforcement, resolved conversations
  and linear history, with no bypass actors;
- blocked force pushes and branch deletion;
- squash-only merge;
- read-only default `GITHUB_TOKEN`, with least-privilege job permissions;
- Actions unable to approve PR reviews;
- automatic deletion of merged branches.

Keep zero mandatory human approvals for solo maintenance. Discover actual check
names from successful runs; do not invent names or remove checks to unblock a PR.

Do not create rules that make the repository unusable for a solo maintainer without a demonstrated security benefit.

## GitHub Actions security

- Default to read-only permissions.
- Grant write permissions only to the specific job that needs them.
- Never use `write-all`.
- Never execute untrusted PR code with `pull_request_target`.
- Follow the repository policy for pinning remote Actions to verified full 40-character commit SHAs with readable release comments.
- Require justification for new Actions and respect the vendor allowlist; prefer
  GitHub-owned or official-vendor Actions. Dependabot maintains Action pins.
- Avoid untrusted text interpolation into shell code; retain job timeouts and
  appropriate concurrency cancellation. Preserve scanner signature verification.
- Keep checkout credentials disabled when not needed.

## Dependency security

Maintain Dependabot coverage for:

- backend / uv;
- frontend / npm-pnpm;
- GitHub Actions.

Keep weekly updates, compatible minor/patch groups and separate major upgrades.
Preserve the existing Dependabot auto-merge eligibility restrictions and all gates.
Use locked dependencies: retain `uv --no-build` (reviewed local editable package
excepted), pnpm frozen-lockfile installs and the small
[build-script allowlist](../../../frontend/pnpm-workspace.yaml).

Keep the locked runtime/development audits in [CONTRIBUTING.md](../../../CONTRIBUTING.md):
backend rejects all known vulnerabilities; frontend rejects high/critical findings.

Do not suppress known vulnerabilities without documented justification.

## GitHub security features

Enable free features when supported by repository visibility/plan:

- dependency graph;
- vulnerability alerts;
- Dependabot security updates;
- CodeQL/code scanning;
- secret scanning;
- push protection;
- private vulnerability reporting when appropriate.

Never purchase or enable paid features without explicit user authorization.
Preserve one CodeQL setup covering Python and JavaScript/TypeScript on PRs, main,
weekly schedule and manual dispatch, publishing results with alert merge protection.
Do not duplicate advanced and default setup. Sensitive reports follow
[SECURITY.md](../../../SECURITY.md); never log secret-scanning payloads.

## Sonar

- Reuse the existing project and [workflow](../../../.github/workflows/sonar.yml).
  Never enable conflicting Automatic Analysis and CI analysis together; keep the
  [analysis-mode guard](../../../scripts/sonar_analysis_mode.py) failing closed.
- Use `gh secret list` for names only. Never retrieve or expose `SONAR_TOKEN`;
  keep it within the existing trusted main-only Actions steps.
- Keep project key, organization, sources, tests, language versions, exclusions, and coverage paths accurate.
- Preserve backend XML, frontend LCOV and script coverage imports, correct test
  classification and workflow/script analysis scope. Do not exclude real source
  or count tests as production coverage.
- Before fixes, collect rules, severity, file/location, description and affected
  area; separate vulnerabilities from hotspots and group shared root causes.
  Prioritize exploitable issues and unsafe CI; false positives need evidence
  and authorization. Treat findings as evidence, not numbers to suppress.
- Do not weaken the Quality Gate merely to obtain green status.
- Validate the analyzed SHA, report imports, coverage, warnings, Quality Gate and
  security/reliability/maintainability results via logs/API. GitHub verification
  does not prove Sonar success. Main-only analysis is not a PR gate; never merge
  without authorization to obtain it. Use only working project/workflow badges.

## Verification

Do not assume configuration is enforced because a write command succeeded.

Query the effective GitHub state and produce a concise matrix containing:

- desired state;
- effective state;
- enforcement mechanism;
- blocking/non-blocking status;
- plan limitation when relevant.

Missing, mismatched or unreadable protection is a failed verification and must
block any claim of completed hardening. Fail closed, report the exact limitation
and never silently downgrade controls. Run relevant local checks and audits
from [CONTRIBUTING.md](../../../CONTRIBUTING.md) and monitor the PR after pushing.

## Completion

Report:

- ruleset state;
- Actions permission state;
- required checks;
- Dependabot/security features;
- CodeQL state;
- secret scanning/push protection state;
- Sonar state;
- remaining manual/account-level blockers.

Stop at maintainer review unless the user explicitly authorized merging that PR.
