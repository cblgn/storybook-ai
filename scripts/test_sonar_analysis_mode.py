"""Regression checks for fail-closed analysis migration; no network or credentials."""

import unittest
from unittest.mock import patch

import sonar_analysis_mode as sonar


def state(value):
    return {"settings": [{"key": "sonar.autoscan.enabled", "value": value}]}


class AnalysisModeTests(unittest.TestCase):
    @patch.object(sonar, "request")
    def test_disabled_project_is_not_mutated(self, request):
        request.return_value = state("false")
        sonar.enforce_ci_analysis("test-placeholder")
        self.assertEqual(request.call_count, 1)

    @patch.object(sonar, "request")
    def test_migration_verifies_effective_state(self, request):
        request.side_effect = [state("true"), None, state("false")]
        sonar.enforce_ci_analysis("test-placeholder")
        self.assertEqual(request.call_count, 3)
        self.assertEqual(request.call_args_list[1].args[2]["enable"], "false")

    @patch.object(sonar, "request")
    def test_successful_mutation_with_enabled_state_still_fails(self, request):
        request.side_effect = [state("true"), None, state("true")]
        with self.assertRaises(ValueError):
            sonar.enforce_ci_analysis("test-placeholder")

    @patch.object(sonar, "request")
    def test_missing_or_unknown_state_fails(self, request):
        for payload in ({"settings": []}, state("unknown"), state(None)):
            with self.subTest(payload=payload):
                request.return_value = payload
                with self.assertRaises(ValueError):
                    sonar.enforce_ci_analysis("test-placeholder")

    @patch.object(sonar, "request")
    def test_missing_secret_fails_before_network(self, request):
        with self.assertRaises(ValueError):
            sonar.enforce_ci_analysis("")
        request.assert_not_called()

    def test_redirects_are_not_followed(self):
        result = sonar.NoRedirects().redirect_request(
            None, None, 302, "", {}, "https://example.com"
        )
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
