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

    def test_planner_prompt_requests_recommendation_not_workflow_structure(self):
        self.assertIn("not a workflow generator", ario_planner.SYSTEM_PROMPT)
        self.assertIn('"engineering_question"', ario_planner.SYSTEM_PROMPT)
        self.assertIn("Do not propose workflow stages", ario_planner.SYSTEM_PROMPT)


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
    @patch("ario_planner.urllib.request.urlopen")
    def test_valid_recommendation_builds_deterministic_workflow(self, urlopen):
        with tempfile.TemporaryDirectory() as directory:
            for relative in (
                "implementation/ario_planner.py",
                "implementation/tests/test_planner_runtime.py",
                "implementation/ario_workflow.py",
                "implementation/tests/test_workflow_runtime.py",
            ):
                path = Path(directory) / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("# bounded evidence", encoding="utf-8")
            recommendation = {
                "implementation_path": "implementation/ario_planner.py",
                "test_path": "implementation/tests/test_planner_runtime.py",
                "engineering_question": "Which missing edge-case test would improve fail-closed planner validation?",
                "rationale": "The planner normalizes identifiers and validates model proposals before returning a workflow.",
            }
            urlopen.return_value = ollama_response(recommendation)
            plan = request_plan("Inspect this repository", directory)
            self.assertEqual(plan["goal"], "Inspect this repository")
            self.assertTrue(plan["workflow_id"].startswith("WF-PLANNER-"))
            self.assertEqual(len(plan["stages"]), 1)
            stage = plan["stages"][0]
            self.assertEqual(stage["stage_id"], "stage-source-review")
            self.assertTrue(stage["task"]["task_id"].startswith("TASK-PLANNER-"))
            self.assertEqual(
                [(a["tool"], a["path"]) for a in stage["task"]["actions"]],
                [
                    ("read_text", "implementation/ario_planner.py"),
                    ("read_text", "implementation/tests/test_planner_runtime.py"),
                ],
            )
            self.assertEqual(len({a["step_id"] for a in stage["task"]["actions"]}), 2)
            request = urlopen.call_args.args[0]
            self.assertEqual(request.full_url, "http://127.0.0.1:11434/api/chat")
            sent = json.loads(request.data.decode("utf-8"))
            self.assertEqual(sent["model"], "qwen2.5:7b")
            self.assertEqual(sent["format"], "json")
            self.assertFalse(sent["stream"])
            self.assertEqual(urlopen.call_args.kwargs["timeout"], 300)


    @patch("ario_planner.urllib.request.urlopen")
    def test_model_cannot_control_workflow_structure_or_duplicate_stage_ids(self, urlopen):
        with tempfile.TemporaryDirectory() as directory:
            for relative in (
                "implementation/ario_planner.py",
                "implementation/tests/test_planner_runtime.py",
                "implementation/ario_workflow.py",
                "implementation/tests/test_workflow_runtime.py",
            ):
                path = Path(directory) / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("# bounded evidence", encoding="utf-8")
            old_style = {
                "workflow_id": "model-workflow",
                "goal": "model goal",
                "stages": [
                    {"stage_id": "duplicate", "task": {}},
                    {"stage_id": "duplicate", "task": {}},
                ],
            }
            recommendation = {
                "implementation_path": "implementation/ario_planner.py",
                "test_path": "implementation/tests/test_planner_runtime.py",
                "engineering_question": "Which missing edge-case test would improve fail-closed planner validation?",
                "rationale": "The planner currently validates a model response before constructing an executable workflow.",
            }
            urlopen.side_effect = [ollama_response(old_style), ollama_response(recommendation)]
            plan = request_plan("Inspect repository", directory)
            self.assertEqual(urlopen.call_count, 2)
            self.assertEqual(len(plan["stages"]), 1)
            self.assertEqual(plan["stages"][0]["stage_id"], "stage-source-review")
            self.assertEqual(len(plan["stages"][0]["task"]["actions"]), 2)
            correction = json.loads(urlopen.call_args_list[1].args[0].data.decode("utf-8"))
            self.assertIn("Do not return stages, actions, IDs", correction["messages"][-1]["content"])


    @patch("ario_planner.urllib.request.urlopen")
    def test_duplicate_or_ambiguous_model_stage_ids_are_not_part_of_recommendation_schema(self, urlopen):
        with tempfile.TemporaryDirectory() as directory:
            invalid = {
                "implementation_path": "implementation/ario_planner.py",
                "test_path": "implementation/tests/test_planner_runtime.py",
                "engineering_question": "Which missing edge-case test would improve fail-closed planner validation?",
                "rationale": "The source and tests provide bounded evidence for a focused regression question.",
                "stages": [{"stage_id": "same"}, {"stage_id": "same"}],
            }
            urlopen.return_value = ollama_response(invalid)
            with self.assertRaisesRegex(AgentRequestError, "recommendation remained invalid"):
                request_plan("Inspect repository", directory)
            self.assertEqual(urlopen.call_count, 2)


    @patch("ario_planner.urllib.request.urlopen")
    def test_recommendation_schema_error_gets_one_correction_attempt(self, urlopen):
        with tempfile.TemporaryDirectory() as directory:
            invalid = {"unexpected": "extra"}
            valid = {
                "implementation_path": "implementation/ario_planner.py",
                "test_path": "implementation/tests/test_planner_runtime.py",
                "engineering_question": "Which missing edge-case test would improve fail-closed planner validation?",
                "rationale": "The planner and regression tests are both present in bounded context.",
            }
            urlopen.side_effect = [ollama_response(invalid), ollama_response(valid)]
            plan = request_plan("Inspect repository", directory)
            self.assertEqual(len(plan["stages"]), 1)
            self.assertEqual(urlopen.call_count, 2)
            second_request = json.loads(urlopen.call_args_list[1].args[0].data.decode("utf-8"))
            correction = second_request["messages"][-1]["content"]
            self.assertIn("implementation_path, test_path, engineering_question, rationale", correction)
            self.assertIn("Do not return stages, actions, IDs", correction)


    @patch("ario_planner.urllib.request.urlopen")
    def test_model_conditions_are_rejected_and_never_enter_workflow(self, urlopen):
        with tempfile.TemporaryDirectory() as directory:
            invalid = {
                "implementation_path": "implementation/ario_planner.py",
                "test_path": "implementation/tests/test_planner_runtime.py",
                "engineering_question": "Which missing edge-case test would improve fail-closed planner validation?",
                "rationale": "The implementation and test excerpts support a bounded regression review.",
                "when": {"stage_id": "self", "status": "COMPLETED"},
            }
            valid = {
                "implementation_path": "implementation/ario_planner.py",
                "test_path": "implementation/tests/test_planner_runtime.py",
                "engineering_question": "Which missing edge-case test would improve fail-closed planner validation?",
                "rationale": "The implementation and test excerpts support a bounded regression review.",
            }
            urlopen.side_effect = [ollama_response(invalid), ollama_response(valid)]
            plan = request_plan("Inspect repository", directory)
            self.assertNotIn("when", plan["stages"][0])
            self.assertEqual(urlopen.call_count, 2)


    @patch("ario_planner.urllib.request.urlopen")
    def test_recommendation_stops_after_one_correction_attempt(self, urlopen):
        with tempfile.TemporaryDirectory() as directory:
            invalid = {"unexpected": "extra"}
            urlopen.side_effect = [ollama_response(invalid), ollama_response(invalid)]
            with self.assertRaisesRegex(AgentRequestError, "recommendation remained invalid"):
                request_plan("Inspect repository", directory)
            self.assertEqual(urlopen.call_count, 2)


    @patch("ario_planner.urllib.request.urlopen")
    def test_unresolved_template_recommendation_is_rejected(self, urlopen):
        with tempfile.TemporaryDirectory() as directory:
            template = {
                "implementation_path": "implementation/ario_planner.py",
                "test_path": "implementation/tests/test_planner_runtime.py",
                "engineering_question": "placeholder",
                "rationale": "This rationale is sufficiently long but includes placeholder text.",
            }
            urlopen.side_effect = [ollama_response(template), ollama_response(template)]
            with self.assertRaisesRegex(AgentRequestError, "recommendation remained invalid"):
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
    @patch("ario_planner.urllib.request.urlopen")
    def test_extra_workflow_fields_are_rejected_before_construction(self, urlopen):
        with tempfile.TemporaryDirectory() as directory:
            bad = {
                "implementation_path": "implementation/ario_planner.py",
                "test_path": "implementation/tests/test_planner_runtime.py",
                "engineering_question": "Which missing edge-case test would improve fail-closed planner validation?",
                "rationale": "The planner implementation and tests provide bounded evidence.",
                "shell": "not allowed",
            }
            urlopen.side_effect = [ollama_response(bad), ollama_response(bad)]
            with self.assertRaisesRegex(AgentRequestError, "recommendation remained invalid"):
                request_plan("Inspect repository", directory)


    @patch("ario_planner.urllib.request.urlopen")
    def test_unapproved_paths_are_rejected_before_workflow_construction(self, urlopen):
        with tempfile.TemporaryDirectory() as directory:
            bad = {
                "implementation_path": "../outside.py",
                "test_path": "implementation/tests/test_planner_runtime.py",
                "engineering_question": "Which missing edge-case test would improve fail-closed planner validation?",
                "rationale": "The planner implementation and tests provide bounded evidence.",
            }
            urlopen.side_effect = [ollama_response(bad), ollama_response(bad)]
            with self.assertRaisesRegex(AgentRequestError, "recommendation remained invalid"):
                request_plan("Inspect repository", directory)


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
            with self.assertRaisesRegex(AgentRequestError, "valid JSON recommendation"):
                request_plan("Inspect repository", directory)


if __name__ == "__main__":
    unittest.main()
