"""Regression checks for fail-closed analysis migration; no network or credentials."""

import unittest
from unittest.mock import MagicMock, patch
from urllib.error import HTTPError

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

    @patch.object(sonar, "request")
    def test_permission_failure_stops_migration(self, request):
        error = HTTPError("", 403, "Forbidden", {}, None)
        request.side_effect = [state("true"), error]
        try:
            with self.assertRaises(HTTPError):
                sonar.enforce_ci_analysis("test-placeholder")
        finally:
            error.close()
        self.assertEqual(request.call_count, 2)

    @patch.object(sonar, "build_opener")
    def test_transport_uses_fixed_host_and_encoded_post(self, opener):
        response = MagicMock()
        response.read.side_effect = [b'{"settings": []}', b'']
        opener.return_value.open.return_value.__enter__.return_value = response
        self.assertEqual(sonar.request("settings/values", "test-placeholder"), {"settings": []})
        self.assertIsNone(sonar.request("autoscan/activation", "test-placeholder", {"enable": "false"}))
        sent = opener.return_value.open.call_args.args[0]
        self.assertEqual(sent.full_url, "https://sonarcloud.io/api/autoscan/activation")
        self.assertEqual(sent.get_method(), "POST")
        self.assertEqual(sent.data, b"enable=false")
        self.assertEqual(sent.get_header("Authorization"), "Bearer test-placeholder")


if __name__ == "__main__":
    unittest.main()
