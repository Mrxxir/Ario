import json
import tempfile
import unittest
from pathlib import Path

from ario_agent import AgentRequestError, parse_task, run_task


class BoundedAgentTests(unittest.TestCase):
    def task(self, actions):
        return {"task_id": "TASK-001", "goal": "Inspect a workspace safely", "actions": actions}

    def test_rejects_unknown_fields_and_non_allowlisted_tools(self):
        with self.assertRaisesRegex(AgentRequestError, "exactly"):
            parse_task({**self.task([{"step_id": "s1", "tool": "git_status"}]), "shell": "whoami"})
        with self.assertRaisesRegex(AgentRequestError, "not allowlisted"):
            parse_task(self.task([{"step_id": "s1", "tool": "run_shell"}]))

    def test_rejects_non_string_tool_and_path_escape(self):
        with self.assertRaisesRegex(AgentRequestError, "must be a string"):
            parse_task(self.task([{"step_id": "s1", "tool": [], "path": "."}]))
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            task = self.task([{"step_id": "s1", "tool": "inspect_directory", "path": "../"}])
            with self.assertRaisesRegex(AgentRequestError, "workspace"):
                run_task(task, root, root / "audit.jsonl")

    def test_successful_steps_are_observed_and_ledger_is_append_only(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "notes.txt").write_text("read-only observation", encoding="utf-8")
            ledger = root / "audit.jsonl"
            ledger.write_text('{"previous":true}\n', encoding="utf-8")
            task = self.task([
                {"step_id": "s1", "tool": "read_text", "path": "notes.txt"},
                {"step_id": "s2", "tool": "inspect_directory", "path": "."},
            ])
            result = run_task(task, root, ledger)
            self.assertEqual(result["status"], "COMPLETED")
            self.assertEqual(result["steps"][0]["observation"]["content"], "read-only observation")
            records = [json.loads(line) for line in ledger.read_text(encoding="utf-8").splitlines()]
            self.assertTrue(records[0]["previous"])
            self.assertEqual(records[-1]["status"], "COMPLETED")

    def test_stops_after_first_failed_observation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            task = self.task([
                {"step_id": "s1", "tool": "read_text", "path": "missing.txt"},
                {"step_id": "s2", "tool": "inspect_directory", "path": "."},
            ])
            result = run_task(task, root, root / "audit.jsonl")
            self.assertEqual(result["status"], "STOPPED")
            self.assertEqual(len(result["steps"]), 1)
            self.assertIn("Fail-closed", result["recovery"])


if __name__ == "__main__":
    unittest.main()
