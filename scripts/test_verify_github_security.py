"""Exercise effective protection checks with a deterministic, offline GitHub API."""

import copy
import io
import json
import subprocess
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

import verify_github_security as verifier


def protected_repository():
    ruleset = json.loads((verifier.ROOT / ".github/rulesets/protect-main.json").read_text())
    ruleset["id"] = 123
    rules = [{**rule, "ruleset_id": 123} for rule in ruleset["rules"]]
    return {
        "": {
            "visibility": "public", "has_issues": True,
            "allow_squash_merge": True, "allow_merge_commit": False,
            "allow_rebase_merge": False, "allow_auto_merge": True,
            "delete_branch_on_merge": True, "squash_merge_commit_title": "PR_TITLE",
            "security_and_analysis": {
                feature: {"status": "enabled"} for feature in (
                    "secret_scanning", "secret_scanning_push_protection",
                    "dependabot_security_updates",
                )
            },
        },
        "actions/permissions/workflow": {
            "default_workflow_permissions": "read", "can_approve_pull_request_reviews": False,
        },
        "actions/permissions": {
            "enabled": True, "allowed_actions": "selected", "sha_pinning_required": True,
        },
        "actions/permissions/selected-actions": {
            "github_owned_allowed": True, "verified_allowed": False,
            "patterns_allowed": ["pnpm/action-setup@*", "astral-sh/setup-uv@*",
                                 "SonarSource/sonarqube-scan-action@*"],
        },
        "rulesets?includes_parents=true": [ruleset],
        "rulesets/123": ruleset,
        "rules/branches/main": rules,
        "vulnerability-alerts": None,
        "automated-security-fixes": {"enabled": True, "paused": False},
        "private-vulnerability-reporting": {"enabled": True},
        "dependency-graph/sbom": {"sbom": {"packages": [{"name": "example"}]}},
        "code-scanning/default-setup": {"state": "not-configured"},
        "code-scanning/analyses?ref=refs/heads/main&per_page=100": [
            {"tool": {"name": "CodeQL"}, "category": f"/language:{language}"}
            for language in ("python", "javascript-typescript")
        ],
    }


class EffectiveProtectionTests(unittest.TestCase):
    def verify(self, responses):
        output = io.StringIO()
        with patch.object(verifier, "api", side_effect=responses.__getitem__), redirect_stdout(output):
            result = verifier.main()
        return result, output.getvalue()

    def test_complete_protections_and_unordered_api_lists_pass(self):
        responses = protected_repository()
        responses["rules/branches/main"].reverse()
        result, matrix = self.verify(responses)
        self.assertEqual(result, 0)
        self.assertNotIn("FAIL", matrix)
        self.assertIn("CodeQL main python", matrix)

    def test_missing_or_weakened_protections_fail(self):
        baseline = protected_repository()
        mutations = [
            ("actions/permissions/workflow", "default_workflow_permissions", "write"),
            ("actions/permissions/workflow", "can_approve_pull_request_reviews", True),
            ("actions/permissions", "sha_pinning_required", False),
            ("", "allow_merge_commit", True),
            ("", "security_and_analysis", {}),
            ("rulesets/123", "enforcement", "disabled"),
            ("rulesets/123", "bypass_actors", [{"actor_type": "RepositoryRole", "actor_id": 5}]),
            ("automated-security-fixes", "paused", True),
            ("dependency-graph/sbom", "sbom", {}),
        ]
        for endpoint, key, value in mutations:
            with self.subTest(endpoint=endpoint, key=key):
                responses = copy.deepcopy(baseline)
                responses[endpoint][key] = value
                result, matrix = self.verify(responses)
                self.assertEqual(result, 1)
                self.assertIn("FAIL", matrix)

    def test_declared_but_ineffective_rules_fail(self):
        responses = protected_repository()
        responses["rules/branches/main"] = []
        self.assertEqual(self.verify(responses)[0], 1)

    def test_missing_check_and_failed_codeql_fail(self):
        responses = protected_repository()
        for rule in responses["rules/branches/main"]:
            if rule["type"] == "required_status_checks":
                rule["parameters"]["required_status_checks"] = []
        responses["code-scanning/analyses?ref=refs/heads/main&per_page=100"][0]["error"] = "failed"
        self.assertEqual(self.verify(responses)[0], 1)

    def test_missing_or_duplicate_ruleset_fails_closed(self):
        for count in (0, 2):
            with self.subTest(count=count):
                responses = protected_repository()
                responses["rulesets?includes_parents=true"] *= count
                with self.assertRaises(RuntimeError):
                    self.verify(responses)

    @patch.object(verifier.subprocess, "run")
    def test_api_failure_does_not_disclose_response_body(self, run):
        run.return_value = subprocess.CompletedProcess([], 1, "sensitive-response", "private-error")
        with self.assertRaisesRegex(RuntimeError, "Cannot verify GitHub endpoint") as raised:
            verifier.api("vulnerability-alerts")
        self.assertNotIn("sensitive-response", str(raised.exception))
        self.assertNotIn("private-error", str(raised.exception))

    @patch.object(verifier.subprocess, "run")
    def test_api_handles_empty_success_and_json(self, run):
        run.side_effect = [subprocess.CompletedProcess([], 0, ""),
                           subprocess.CompletedProcess([], 0, '{"enabled": true}')]
        self.assertIsNone(verifier.api("vulnerability-alerts"))
        self.assertEqual(verifier.api("automated-security-fixes"), {"enabled": True})
        self.assertEqual(run.call_args.args[0][:2], ["gh", "api"])


if __name__ == "__main__":
    unittest.main()
