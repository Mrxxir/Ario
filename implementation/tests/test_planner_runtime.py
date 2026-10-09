import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import MagicMock, patch

from ario_agent import AgentRequestError
import ario_planner
from ario_planner import _local_ollama_endpoint, build_observation, request_plan


def ollama_response(workflow):
    response = MagicMock()
    response.__enter__.return_value.read.return_value = json.dumps({
        "message": {"content": json.dumps(workflow)}
    }).encode("utf-8")
    return response


class LocalOllamaPlannerTests(unittest.TestCase):
    def valid_workflow(self):
        return {
            "workflow_id": "MODEL-CHOSEN-ID",
            "goal": "model goal",
            "stages": [{
                "stage_id": "inspect",
                "task": {
                    "task_id": "TASK-MODEL-ID",
                    "goal": "Inspect workspace",
                    "actions": [{"step_id": "list", "tool": "inspect_directory", "path": "."}],
                },
            }],
        }

    def test_endpoint_accepts_loopback_and_rejects_remote_hosts(self):
        self.assertEqual(
            _local_ollama_endpoint("http://127.0.0.1:11434"),
            "http://127.0.0.1:11434/api/chat",
        )
        with self.assertRaisesRegex(AgentRequestError, "loopback"):
            _local_ollama_endpoint("http://example.com:11434")
        with self.assertRaisesRegex(AgentRequestError, "loopback"):
            _local_ollama_endpoint("https://127.0.0.1:11434")

    def test_observation_is_bounded_metadata_and_does_not_read_file_contents(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "private.txt").write_text("secret body must not be sent", encoding="utf-8")
            observation = build_observation(root)
            self.assertIn({"path": "private.txt", "kind": "file"}, observation["entries"])
            self.assertNotIn("secret body must not be sent", json.dumps(observation))
            self.assertIn("file contents were not read", observation["note"])

    @patch("ario_planner.urllib.request.urlopen")
    def test_valid_plan_is_schema_checked_and_runtime_ids_are_local(self, urlopen):
        with tempfile.TemporaryDirectory() as directory:
            urlopen.return_value = ollama_response(self.valid_workflow())
            plan = request_plan("Inspect this repository", directory)
            self.assertEqual(plan["goal"], "Inspect this repository")
            self.assertTrue(plan["workflow_id"].startswith("WF-PLANNER-"))
            self.assertNotEqual(plan["stages"][0]["task"]["task_id"], "TASK-MODEL-ID")
            request = urlopen.call_args.args[0]
            self.assertEqual(request.full_url, "http://127.0.0.1:11434/api/chat")
            sent = json.loads(request.data.decode("utf-8"))
            self.assertEqual(sent["model"], "qwen2.5:7b")
            self.assertEqual(sent["format"], "json")
            self.assertFalse(sent["stream"])

    @patch("ario_planner.urllib.request.urlopen")
    def test_invalid_workflow_is_rejected_before_execution(self, urlopen):
        with tempfile.TemporaryDirectory() as directory:
            bad = self.valid_workflow()
            bad["shell"] = "not allowed"
            urlopen.return_value = ollama_response(bad)
            with self.assertRaisesRegex(AgentRequestError, "exactly workflow_id"):
                request_plan("Inspect repository", directory)

    @patch("ario_planner.urllib.request.urlopen")
    def test_path_escape_is_rejected_during_plan_validation(self, urlopen):
        with tempfile.TemporaryDirectory() as directory:
            bad = self.valid_workflow()
            bad["stages"][0]["task"]["actions"][0]["path"] = ".."
            urlopen.return_value = ollama_response(bad)
            with self.assertRaisesRegex(AgentRequestError, "escapes the configured workspace"):
                request_plan("Inspect repository", directory)

    @patch("ario_planner.run_workflow")
    @patch("ario_planner.request_plan")
    def test_cli_is_plan_only_by_default(self, request_plan_mock, run_workflow_mock):
        request_plan_mock.return_value = self.valid_workflow()
        with patch("sys.argv", ["ario_planner.py", "--goal", "inspect", "--workspace", ".", "--ledger", "events.jsonl"]):
            with redirect_stdout(io.StringIO()) as output:
                code = ario_planner.main()
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(output.getvalue())["status"], "PLAN_READY")
        run_workflow_mock.assert_not_called()

    @patch("ario_planner.run_workflow")
    @patch("ario_planner.request_plan")
    def test_cli_executes_only_with_explicit_execute_flag(self, request_plan_mock, run_workflow_mock):
        request_plan_mock.return_value = self.valid_workflow()
        run_workflow_mock.return_value = {"status": "COMPLETED"}
        with patch("sys.argv", ["ario_planner.py", "--goal", "inspect", "--workspace", ".", "--ledger", "events.jsonl", "--execute"]):
            with redirect_stdout(io.StringIO()) as output:
                code = ario_planner.main()
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(output.getvalue())["status"], "COMPLETED")
        run_workflow_mock.assert_called_once()

    @patch("ario_planner.urllib.request.urlopen")
    def test_malformed_ollama_envelope_is_rejected(self, urlopen):
        response = MagicMock()
        response.__enter__.return_value.read.return_value = b'{"message": {}}'
        urlopen.return_value = response
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(AgentRequestError, "valid JSON workflow"):
                request_plan("Inspect repository", directory)


if __name__ == "__main__":
    unittest.main()
