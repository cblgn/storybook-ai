"""Read effective GitHub protections; exit nonzero on drift or inaccessible state.

Requires an authenticated maintainer gh session. Never reads secret values and
never modifies GitHub. Sonar authentication and analysis are verified separately.
"""

import json
import subprocess
import sys
from pathlib import Path

REPO = "cblgn/storybook-ai"
ROOT = Path(__file__).resolve().parents[1]


def api(endpoint: str):
    result = subprocess.run(
        ["gh", "api", f"repos/{REPO}/{endpoint}".rstrip("/")],
        capture_output=True,
        text=True,
        check=False,
        timeout=60,
    )
    if result.returncode:
        # Do not echo API bodies, which could contain sensitive data.
        raise RuntimeError(f"Cannot verify GitHub endpoint: {endpoint or 'repository'}")
    return json.loads(result.stdout) if result.stdout.strip() else None


def main() -> int:
    rows = []

    def check(name, desired, effective, mechanism, blocking):
        passed = effective == desired
        rows.append((name, desired, effective, mechanism, blocking, passed))

    repo = api("")
    check("Visibility", "public", repo.get("visibility"), "Repository", "No")
    check("Issues", True, repo.get("has_issues"), "Repository", "No")
    for key, desired in {
        "allow_squash_merge": True,
        "allow_merge_commit": False,
        "allow_rebase_merge": False,
        "allow_auto_merge": True,
        "delete_branch_on_merge": True,
        "squash_merge_commit_title": "PR_TITLE",
    }.items():
        check(key, desired, repo.get(key), "Repository merge policy", "Yes (merge methods)")

    workflow = api("actions/permissions/workflow")
    check("Token permissions", "read", workflow.get("default_workflow_permissions"),
          "Actions default token", "Yes")
    check("Actions approve PRs", False, workflow.get("can_approve_pull_request_reviews"),
          "Actions default token", "Yes")
    actions = api("actions/permissions")
    for key, desired in {"enabled": True, "allowed_actions": "selected",
                         "sha_pinning_required": True}.items():
        check(key, desired, actions.get(key), "Actions execution policy", "Yes")
    selected = api("actions/permissions/selected-actions")
    check("GitHub actions allowed", True, selected.get("github_owned_allowed"),
          "Actions allowlist", "Yes")
    check("All marketplace verified actions allowed", False, selected.get("verified_allowed"),
          "Actions allowlist", "Yes")
    check("Official vendor allowlist", sorted([
        "astral-sh/setup-uv@*", "pnpm/action-setup@*", "SonarSource/sonarqube-scan-action@*",
        "dependabot/fetch-metadata@*",
    ]), sorted(selected.get("patterns_allowed", [])), "Actions allowlist", "Yes")

    desired_ruleset = json.loads((ROOT / ".github/rulesets/protect-main.json").read_text())
    matches = [r for r in api("rulesets?includes_parents=true")
               if r["name"] == desired_ruleset["name"]]
    check("Protect main rulesets", 1, len(matches), "Repository rulesets", "Yes")
    if len(matches) != 1:
        raise RuntimeError("Expected exactly one Protect main ruleset")
    ruleset = api(f"rulesets/{matches[0]['id']}")
    for key in ("target", "enforcement", "conditions", "bypass_actors"):
        check(key, desired_ruleset[key], ruleset.get(key), "Protect main", "Yes")
    effective = api("rules/branches/main")
    for rule in desired_ruleset["rules"]:
        actual = [r for r in effective if r["type"] == rule["type"]
                  and r.get("ruleset_id") == ruleset["id"]]
        check(rule["type"], 1, len(actual), "Effective main rules", "Yes")
        if len(actual) == 1:
            for key, value in rule.get("parameters", {}).items():
                found = actual[0].get("parameters", {}).get(key)
                # API list ordering is not a policy change.
                if isinstance(value, list):
                    value = sorted(json.dumps(v, sort_keys=True) for v in value)
                    found = (sorted(json.dumps(v, sort_keys=True) for v in found)
                             if isinstance(found, list) else found)
                check(f"{rule['type']}.{key}", value, found, "Effective main rules", "Yes")

    security = repo.get("security_and_analysis", {})
    for key in ("secret_scanning", "secret_scanning_push_protection",
                "dependabot_security_updates"):
        check(key, "enabled", security.get(key, {}).get("status"),
              "GitHub security", "Yes (push protection)" if "push" in key else "No; detection/fixes")
    api("vulnerability-alerts")  # 204 enabled; errors fail closed.
    check("Vulnerability alerts", True, True, "GitHub vulnerability alerts API", "No; detection")
    auto = api("automated-security-fixes")
    check("Dependabot security fixes", True, auto.get("enabled"), "Dependabot API", "No; PRs")
    check("Dependabot paused", False, auto.get("paused"), "Dependabot API", "No; PRs")
    check("Private vulnerability reporting", True,
          api("private-vulnerability-reporting").get("enabled"), "Security advisories API", "No")
    sbom = api("dependency-graph/sbom")
    check("Dependency graph", True, bool(sbom.get("sbom", {}).get("packages")),
          "Dependency graph SBOM API", "No; detection")
    check("Duplicate CodeQL default setup", "not-configured",
          api("code-scanning/default-setup").get("state"), "Advanced workflow only", "No")
    analyses = api("code-scanning/analyses?ref=refs/heads/main&per_page=100")
    for language in ("python", "javascript-typescript"):
        exists = any(a.get("tool", {}).get("name") == "CodeQL" and not a.get("error")
                     and a.get("category") == f"/language:{language}" for a in analyses)
        check(f"CodeQL main {language}", True, exists, "Code scanning analyses API", "Yes; ruleset")

    print("| Protection | Desired | Effective | Enforcement | Blocking | Plan | Result |")
    print("|---|---|---|---|---|---|---|")
    for name, desired, effective, mechanism, blocking, passed in rows:
        values = [name, str(desired), str(effective), mechanism, blocking,
                  "Free for this public repository", "PASS" if passed else "FAIL"]
        print("| " + " | ".join(v.replace("|", "\\|") for v in values) + " |")
    return 0 if all(row[-1] for row in rows) else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (RuntimeError, OSError, ValueError, KeyError, subprocess.TimeoutExpired) as exc:
        print(f"Security verification failed: {exc}", file=sys.stderr)
        sys.exit(1)
