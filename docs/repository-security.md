# Repository security baseline

This baseline applies to the **public** `cblgn/storybook-ai` repository. The initial
API verification was performed on 2026-09-16 for issue #11. Settings can drift;
rerun `python3 scripts/verify_github_security.py` with an authenticated maintainer
`gh` session to read effective settings and produce a fresh security matrix.
The command exits nonzero on missing protections, API errors or unexpected state.
It does not mutate settings or read secret values. Workflow files alone are not
proof of repository enforcement.

| Desired protection | Verified effective state | Enforcement | Blocking | Plan dependency |
|---|---|---|---|---|
| PRs, current base, resolved conversations | Active Protect main, zero required approvals, no bypass actors | Repository ruleset | Merge | Free on public repositories |
| Seven quality/security checks | Required from GitHub Actions, app 15368 | Ruleset strict status checks | Merge | Free on public repositories |
| Linear history, no force push or deletion | Active | Ruleset | Push/merge/deletion | Free on public repositories |
| Squash only, automatic branch deletion | Enabled; merge/rebase methods disabled | Repository settings | Other merge methods | Free |
| Token read-only, no Actions PR approval | Enabled | Actions repository permissions | Token operations | Free |
| Full SHA pins and official Actions | Mandatory SHA policy; GitHub plus three explicit official vendors | Actions execution policy and reviewed workflow pins | Workflow execution | Free for this repository |
| Dependency graph, vulnerability alerts, security updates | Enabled; SBOM API returns dependencies | GitHub/Dependabot | Detection and update PRs; audits block merge | Free public repository |
| Private vulnerability reporting | Enabled | GitHub advisories | Private intake | Free public repository |
| Secret scanning and push protection | Enabled | GitHub secret protection | Detection / blocks supported secret pushes | Free public repository |
| Python and JS/TS CodeQL | Advanced workflow; default setup not configured | Required jobs and CodeQL rule blocking all alert severities | Merge | Free public repository |
| Dependency audits | pip-audit rejects all known vulnerabilities; pnpm rejects high/critical | Required Security workflow | Merge | Free |
| Deterministic quality and coverage | Backend threshold 80%; frontend reports coverage without arbitrary threshold | Required CI workflow | Merge | Free |
| Sonar analysis with coverage | Project exists; CI authentication unavailable; Quality Gate not computed | Prepared main-only workflow, conditional until credentials exist | Not a PR gate; activation incomplete | Free main analysis; other branches/PRs excluded |

Required check names: `Backend quality`, `Frontend quality`, `Browser integration`,
`Backend dependency audit`, `Frontend dependency audit`, `CodeQL (python)` and
`CodeQL (javascript-typescript)`. The expected ruleset payload is versioned in
[protect-main.json](../.github/rulesets/protect-main.json). No signing requirement,
paid merge queue or additional reviewer is introduced. Administrators must not
change protections merely to merge a failing PR.

## Supply chain and secrets

All remote Actions use upstream-resolved full commit SHAs with release comments.
Dependabot checks Actions, uv and npm/pnpm weekly, grouping minor/patch upgrades.
GitHub-owned Actions and `astral-sh/setup-uv`, `pnpm/action-setup` and
`SonarSource/sonarqube-scan-action` are the only allowed remote vendors/actions.
Checkout credentials are not persisted. Only the CodeQL job requests
`security-events: write`; it does not require packages access for this public repo.
No workflow executes PR code through `pull_request_target` or interpolates PR text
into shell commands. Superseded PR runs are cancelled; jobs have timeouts.

The uv install/run commands use `--no-build` to refuse new third-party source
builds. uv may reuse cached wheels and still builds the reviewed first-party
editable package; this is not a sandbox for arbitrary PR code. Normal PR jobs
have no LLM or Sonar secrets. pnpm permits the existing esbuild install script;
other dependency build scripts remain disallowed.

The initial history inspection covered all 89 reachable blobs and found no obvious
credential patterns; GitHub reported no open secret-scanning alerts. Pattern scans
are not proof that no secret can exist. See [SECURITY.md](../SECURITY.md) for private
reporting and rotation guidance. Do not log scanner payloads containing secrets.

## Sonar external activation

The existing public project is `cblgn_storybook-ai` in organization `cblgn`.
`sonar-project.properties` maps both source trees and the backend XML/frontend LCOV
reports into that single project. Generated files and caches are excluded. The
public automatic analysis initially reported 18 Actions/install security findings;
this PR pins Actions and adds uv's no-build option to address their source causes.
Only a subsequent Sonar analysis can confirm those findings are closed.

No SONAR_TOKEN Actions secret, authenticated Sonar CLI or Sonar token environment
is available. GitHub authentication cannot administer the Sonar account. Once Sonar
authentication is available, disable the project's automatic analysis via its API,
configure `SONAR_TOKEN` through the GitHub secret API/CLI without exposing its value,
then set `SONAR_ENABLED=true` and dispatch `sonar.yml` on main. The workflow waits
for the Quality Gate and fails if analysis or the gate fails. The ref guard prevents
manual execution on a feature branch with this secret.

Sonar PR/secondary-branch analysis is not required by this free-plan setup. Sonar
badges are intentionally absent until the gate and coverage provide real signals.
A successful GitHub API verification does **not** mean Sonar activation is complete.

References: [rulesets on public GitHub Free repositories](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets),
[CodeQL merge protection](https://docs.github.com/en/code-security/how-tos/find-and-fix-code-vulnerabilities/manage-your-configuration/set-merge-protection),
[Actions policy API](https://docs.github.com/en/rest/actions/permissions),
[uv no-build semantics](https://docs.astral.sh/uv/reference/cli/#uv-sync--no-build),
[Sonar branch analysis](https://docs.sonarsource.com/sonarqube-cloud/enriching/branch-analysis).
