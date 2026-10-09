import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import MagicMock, patch

from ario_agent import AgentRequestError
import ario_planner
from ario_planner import _local_ollama_endpoint, _validate_plan_quality, build_observation, request_plan


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

    def test_planner_prompt_requires_distinct_source_and_test_evidence(self):
        self.assertIn("exactly TWO actions", ario_planner.SYSTEM_PROMPT)
        self.assertIn('"tool": "read_text"', ario_planner.SYSTEM_PROMPT)
        self.assertIn("Do not use inspect_directory", ario_planner.SYSTEM_PROMPT)
        self.assertIn("concrete bounded engineering question", ario_planner.SYSTEM_PROMPT)

    def test_planning_context_prioritizes_planner_and_its_tests(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            paths = (
                "implementation/ario_planner.py",
                "implementation/tests/test_planner_runtime.py",
                "implementation/ario_workflow.py",
                "implementation/tests/test_workflow_runtime.py",
                "implementation/ario_agent.py",
                "implementation/tests/test_agent_runtime.py",
            )
            for relative in paths:
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(f"# evidence from {relative}\\n", encoding="utf-8")
            context = build_observation(root)["planning_context"]
            self.assertEqual([item["path"] for item in context], list(paths[:4]))

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
            self.assertIn("does not read arbitrary file contents", observation["note"])

    def test_planning_context_reads_only_bounded_allowlisted_source_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            implementation = root / "implementation"
            implementation.mkdir()
            (implementation / "ario_agent.py").write_text(
                "def safe_runtime():\\n    return 'bounded-source-evidence'\\n",
                encoding="utf-8",
            )
            (root / "private.txt").write_text("DO NOT SEND THIS SECRET", encoding="utf-8")
            observation = build_observation(root)
            context = observation["planning_context"]
            self.assertEqual([item["path"] for item in context], ["implementation/ario_agent.py"])
            self.assertIn("bounded-source-evidence", context[0]["content"])
            self.assertNotIn("DO NOT SEND THIS SECRET", json.dumps(observation))
            self.assertLessEqual(
                sum(len(item["content"]) for item in context),
                ario_planner.MAX_CONTEXT_TOTAL_CHARS,
            )

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
            self.assertEqual(urlopen.call_args.kwargs["timeout"], 300)

    @patch("ario_planner.urllib.request.urlopen")
    def test_duplicate_model_task_and_step_ids_are_normalized_locally(self, urlopen):
        with tempfile.TemporaryDirectory() as directory:
            proposed = self.valid_workflow()
            second = json.loads(json.dumps(proposed["stages"][0]))
            second["stage_id"] = "review"
            second["task"]["goal"] = "Review bounded implementation evidence"
            second["task"]["task_id"] = proposed["stages"][0]["task"]["task_id"]
            second["task"]["actions"][0]["step_id"] = proposed["stages"][0]["task"]["actions"][0]["step_id"]
            second["task"]["actions"][0]["path"] = "notes.txt"
            second["when"] = {"stage_id": "inspect", "status": "COMPLETED"}
            proposed["stages"].append(second)
            urlopen.return_value = ollama_response(proposed)
            plan = request_plan("Inspect repository", directory)
            self.assertEqual([stage["stage_id"] for stage in plan["stages"]], ["inspect", "review"])
            self.assertEqual(plan["stages"][1]["when"]["stage_id"], "inspect")
            task_ids = [stage["task"]["task_id"] for stage in plan["stages"]]
            self.assertEqual(len(task_ids), len(set(task_ids)))
            step_ids = [stage["task"]["actions"][0]["step_id"] for stage in plan["stages"]]
            self.assertEqual(len(step_ids), len(set(step_ids)))

    @patch("ario_planner.urllib.request.urlopen")
    def test_ambiguous_duplicate_stage_ids_fail_closed(self, urlopen):
        with tempfile.TemporaryDirectory() as directory:
            proposed = self.valid_workflow()
            second = json.loads(json.dumps(proposed["stages"][0]))
            proposed["stages"].append(second)
            urlopen.return_value = ollama_response(proposed)
            with self.assertRaisesRegex(AgentRequestError, "stage_id values are ambiguous"):
                request_plan("Inspect repository", directory)
            self.assertEqual(urlopen.call_count, 1)

    @patch("ario_planner.urllib.request.urlopen")
    def test_schema_error_gets_one_correction_attempt(self, urlopen):
        with tempfile.TemporaryDirectory() as directory:
            invalid = self.valid_workflow()
            invalid["unexpected"] = "model echoed unrelated context"
            urlopen.side_effect = [ollama_response(invalid), ollama_response(self.valid_workflow())]
            plan = request_plan("Inspect repository", directory)
            self.assertEqual(len(plan["stages"]), 1)
            self.assertEqual(urlopen.call_count, 2)
            second_request = json.loads(urlopen.call_args_list[1].args[0].data.decode("utf-8"))
            correction = second_request["messages"][-1]["content"]
            self.assertIn("exactly these top-level keys", correction)
            self.assertIn("planning_context", correction)

    @patch("ario_planner.urllib.request.urlopen")
    def test_first_stage_condition_gets_explicit_correction_guidance(self, urlopen):
        with tempfile.TemporaryDirectory() as directory:
            invalid = self.valid_workflow()
            invalid["stages"][0]["when"] = {"stage_id": "inspect", "status": "COMPLETED"}
            corrected = self.valid_workflow()
            urlopen.side_effect = [ollama_response(invalid), ollama_response(corrected)]
            plan = request_plan("Inspect repository", directory)
            self.assertEqual(len(plan["stages"]), 1)
            self.assertNotIn("when", plan["stages"][0])
            self.assertEqual(urlopen.call_count, 2)
            second_request = json.loads(urlopen.call_args_list[1].args[0].data.decode("utf-8"))
            correction = second_request["messages"][-1]["content"]
            self.assertIn("first stage MUST omit the when field", correction)
            self.assertIn("stage_id earlier in the stages list", correction)

    @patch("ario_planner.urllib.request.urlopen")
    def test_schema_error_stops_after_one_correction_attempt(self, urlopen):
        with tempfile.TemporaryDirectory() as directory:
            invalid = self.valid_workflow()
            invalid["unexpected"] = "extra"
            urlopen.side_effect = [ollama_response(invalid), ollama_response(invalid)]
            with self.assertRaisesRegex(AgentRequestError, "remained invalid after one correction attempt"):
                request_plan("Inspect repository", directory)
            self.assertEqual(urlopen.call_count, 2)

    @patch("ario_planner.urllib.request.urlopen")
    def test_unresolved_template_plan_is_rejected(self, urlopen):
        with tempfile.TemporaryDirectory() as directory:
            template = self.valid_workflow()
            template["stages"][0]["stage_id"] = "unique-id"
            template["stages"][0]["task"]["goal"] = "short task goal"
            template["stages"][0]["task"]["actions"][0]["step_id"] = "unique-id"
            urlopen.return_value = ollama_response(template)
            with self.assertRaisesRegex(AgentRequestError, "unresolved template placeholder"):
                request_plan("Inspect repository", directory)

    def test_plan_quality_rejects_directory_only_plan_when_source_context_exists(self):
        workflow = self.valid_workflow()
        observation = {"planning_context": [{"path": "implementation/ario_agent.py", "content": "def example(): pass"}]}
        with self.assertRaisesRegex(AgentRequestError, "only lists directories"):
            _validate_plan_quality(workflow, observation)

    def test_plan_quality_rejects_repeated_action_across_stages(self):
        workflow = self.valid_workflow()
        second = json.loads(json.dumps(workflow["stages"][0]))
        second["stage_id"] = "review"
        second["task"]["task_id"] = "TASK-SECOND"
        second["task"]["actions"][0]["step_id"] = "different-step-id"
        second["task"]["actions"][0]["tool"] = "read_text"
        second["task"]["actions"][0]["path"] = "implementation/ario_agent.py"
        workflow["stages"][0]["task"]["actions"][0] = {
            "step_id": "step-one", "tool": "read_text", "path": "implementation/ario_agent.py"
        }
        workflow["stages"].append(second)
        with self.assertRaisesRegex(AgentRequestError, "duplicates an action"):
            _validate_plan_quality(workflow, {"planning_context": []})

    def test_timeout_must_be_within_supported_bounds(self):
        with tempfile.TemporaryDirectory() as directory:
            for timeout in (0, -1, 1801, True, "300"):
                with self.subTest(timeout=timeout):
                    with self.assertRaisesRegex(AgentRequestError, "timeout must be an integer"):
                        request_plan("Inspect repository", directory, timeout=timeout)

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
