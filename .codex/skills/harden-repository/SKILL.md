---
name: harden-repository
description: Inspect, change and verify Storybook AI repository security configuration, GitHub rulesets, Actions, Dependabot, CodeQL and Sonar. Use for repository hardening or security configuration work, not routine feature implementation or merely running existing checks.
---

# Harden the repository

Use this procedure for repository security/configuration changes. Follow
[implement-github-issue](../implement-github-issue/SKILL.md) for Issue, branch,
validation and PR delivery; do not duplicate that workflow or invent another task
source. Read [AGENTS.md](../../../AGENTS.md) for permanent constraints and
[SECURITY.md](../../../SECURITY.md) for private reporting.

All repository paths and commands below are relative to the repository root.

## Scope and authority

The maintained baseline and enforcement limitations are in
[docs/repository-security.md](../../../docs/repository-security.md). The expected
ruleset payload is [.github/rulesets/protect-main.json](../../../.github/rulesets/protect-main.json).
Read these instead of maintaining another list of check names or vendor identities.

Use existing task authorization. A request to inspect or edit documentation does
not authorize changing remote security settings. For authorized hardening, use
`gh`/APIs where available; do not send the user to manual settings unnecessarily.
Prepare reviewable changes before requesting any additional authorization.
Preserve unrelated settings, visibility and published history. Stay within free
capabilities unless a paid capability has been explicitly authorized; report an
unavailable protection instead of silently substituting a weaker one.

## Inspect before changing configuration

- Inspect Git status, branch, existing changes and relevant documentation. Reuse
  correct configuration; do not duplicate workflows, rulesets or Sonar projects.
- Check `gh auth status`, repository identity/visibility and effective settings.
  Inspect rulesets and effective `main` rules, actual successful check names,
  merge methods, default Actions permissions and allowed Actions.
- Read [.github/](../../../.github), including workflows, issue/PR templates and
  [Dependabot configuration](../../../.github/dependabot.yml). Inspect relevant
  manifests, lockfiles, [.gitignore](../../../.gitignore),
  [Sonar properties](../../../sonar-project.properties) and recent Actions runs.
- Read vulnerability-alert, Dependabot-security-update, secret-scanning,
  push-protection and code-scanning state where available. Review findings using
  sanitized identifiers; never print secret values or sensitive alert payloads.
- Use `gh secret list` for secret names only. An existing secret is not evidence
  that a workflow or external service is correctly configured.

Summarize the gap, intended change and validation evidence before modifying it.
Sensitive vulnerabilities follow private reporting, not public Issue disclosure.

## Preserve the enforcement baseline

Keep protected `main`: PRs, current-base checks, resolved conversations, linear
history, force-push/deletion restrictions and no bypass actors. Preserve the
solo-maintainer policy of zero mandatory approvals and squash-only merges with
GitHub deleting merged branches. Discover actual check names before changing
required checks; never remove them merely to merge a failing change.

Default `GITHUB_TOKEN` permissions remain read-only and Actions cannot approve PR
reviews. Grant extra permissions only to the specific job that needs them.
For example, CodeQL publishes security events and the existing Dependabot policy
job manages auto-merge; these are not reasons to grant other jobs write access.
Do not use `write-all` or execute untrusted PR code through `pull_request_target`.
Avoid interpolating untrusted PR text into shell code. Keep timeouts and suitable
concurrency cancellation.

Pin remote Actions to upstream-verified full **40-character commit SHAs**, with
readable release comments. Dependabot maintains pins. New Actions require a
concrete justification and compliance with the restricted vendor allowlist.
Prefer GitHub-maintained or official vendor Actions, or a small shell operation.
Keep checkout credentials disabled where appropriate and preserve scanner binary
signature verification. Update expected-state documentation/verifier assumptions
only for justified, authorized policy changes, then verify the effective state.

Use locked dependencies and retain the existing dependency build restrictions:
`uv --no-build` rejects new third-party source builds while permitting the reviewed
local editable package. Do not remove it just because a wheel is unavailable.
Keep pnpm frozen-lockfile installs and its explicit
[build-script allowlist](../../../frontend/pnpm-workspace.yaml) small and justified.

Preserve weekly uv, npm/pnpm and Actions updates, with compatible minor/patch
updates grouped and majors separate. Retain the approved Dependabot auto-merge
eligibility restrictions and all merge protections. Audits include locked runtime
and development dependencies: backend rejects all known vulnerabilities;
frontend high/critical findings must fail. Fix findings or document a justified
exception; do not silently ignore or suppress them.

Keep one coherent CodeQL configuration covering Python and JavaScript/TypeScript
and publishing results. Avoid simultaneous default and advanced setups. Preserve
PR/main, weekly and manual coverage in the current workflow and existing alert
merge protection. Enable or retain free vulnerability alerts, security updates,
secret scanning, push protection and private reporting when supported.

## Sonar analysis and findings

Use the existing project/configuration and
[Sonar workflow](../../../.github/workflows/sonar.yml), not a separate project for
each application. Inspect the current analysis method and revision before changing
code. Never enable conflicting Automatic Analysis and CI analysis together.
[sonar_analysis_mode.py](../../../scripts/sonar_analysis_mode.py) verifies the
setting and blocks CI if its effective state cannot be established.

Keep Sonar credentials exclusively in the trusted Actions steps; never retrieve,
print or copy the token into files, logs, Issues or PRs. Preserve the current
main-only secret guard. Missing authentication or permissions are blockers to
report, not reasons to broaden credential exposure or bypass a gate.

Maintain explicit production/test classification and a Python version matching
the backend. Preserve import of `backend/coverage.xml`,
`frontend/coverage/lcov.info` and the existing script coverage report. Do not drop
workflow/script security analysis or count tests as production coverage. Generated
files and caches remain excluded; excluding real source to hide findings is not a fix.

Before remediation, collect each finding's rule, type, severity, file/location,
description and affected area. Separate vulnerabilities from Security Hotspots,
group common causes, and propose code/configuration/dependency fixes or justified
contextual reviews. Prioritize exploitable issues and unsafe CI. Do not mark a
finding false-positive or suppress a rule without evidence and authorization.

Monitor the scanner and wait for the Quality Gate. Confirm the analyzed Git SHA,
report imports, coverage for both applications, warnings, gate and security/
reliability/maintainability results through logs and the Sonar API. GitHub security
verification does not establish Sonar success. Main-only analysis is not a
pre-merge PR gate; report that limit and do not merge to obtain analysis without
explicit authorization. Publish badges only for real, working project/workflow signals.

## Verify effective state and finish

After authorized setting changes, read back the actual configuration and run:

```bash
python3 scripts/verify_github_security.py
```

This is the repository's read-only effective-state verifier. Inspect its output
and exit status: missing, unreadable or mismatched protection fails closed. A
successful write command or a matching repository file is not proof of enforcement.
For capabilities outside the verifier, query the corresponding API separately.

Run relevant local checks, locked audits and workflow validation following
`CONTRIBUTING.md`. Review the complete diff and monitor PR checks using the
implementation skill. Keep private reports and credentials out of public evidence.

Report desired versus effective state, enforcement mechanism, blocking behavior
and plan dependency. Link the Issue/PR, show CI/security/Sonar results, and identify
only genuine external authentication/account blockers after completing independent
work. Never describe missing protections as enabled or weaken them to finish.
Stop at maintainer review unless the user explicitly authorized the merge.
