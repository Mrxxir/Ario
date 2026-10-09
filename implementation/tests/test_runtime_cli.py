import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from ario_cli import execute_request


class RuntimeEntryPointTests(unittest.TestCase):
    def request(self, **overrides):
        payload = {
            "audit_id": "AUDIT-CLI-001",
            "rule_versions": ["M0-1.0"],
            "configuration_id": "CLI-TEST",
            "execution_timestamp": "TEST-TIMESTAMP-001",
            "artifacts": {},
        }
        payload.update(overrides)
        return payload

    def test_empty_primary_input_stays_unknown(self):
        result = execute_request(self.request())
        self.assertEqual(result["verdict"], "UNKNOWN")
        self.assertEqual(result["audit_id"], "AUDIT-CLI-001")

    def test_unknown_top_level_field_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "unknown field"):
            execute_request(self.request(unrestricted_shell=True))

    def test_unknown_artifact_field_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "unknown field"):
            execute_request(self.request(artifacts={"arbitrary_python": "print(1)"}))

    def test_cli_appends_ledger_without_overwriting(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            request_path = root / "request.json"
            ledger_path = root / "audit.jsonl"
            request_path.write_text(json.dumps(self.request()), encoding="utf-8")
            ledger_path.write_text('{"previous":"entry"}\n', encoding="utf-8")
            completed = subprocess.run(
                [
                    sys.executable,
                    str(Path(__file__).resolve().parents[1] / "ario_cli.py"),
                    "--input", str(request_path),
                    "--ledger", str(ledger_path),
                ],
                cwd=Path(__file__).resolve().parents[1],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            lines = ledger_path.read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(lines), 2)
            self.assertEqual(json.loads(lines[1])["verdict"], "UNKNOWN")
            self.assertEqual(json.loads(completed.stdout)["verdict"], "UNKNOWN")

    def test_malformed_input_returns_nonzero_and_unknown(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.json"
            path.write_text("{not-json", encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, str(Path(__file__).resolve().parents[1] / "ario_cli.py"),
                 "--input", str(path)],
                cwd=Path(__file__).resolve().parents[1],
                capture_output=True, text=True, check=False,
            )
            self.assertEqual(completed.returncode, 2)
            self.assertEqual(json.loads(completed.stderr)["verdict"], "UNKNOWN")


if __name__ == "__main__":
    unittest.main()
