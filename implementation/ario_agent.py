from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


MAX_STEPS = 8
MAX_READ_BYTES = 20_000
ALLOWED_TOOLS = {"inspect_directory", "read_text", "git_status", "compile_python", "run_tests", "replace_text", "restore_backup"}


class AgentRequestError(ValueError):
    pass


def _inside(root: Path, relative: str) -> Path:
    if not isinstance(relative, str) or not relative.strip():
        raise AgentRequestError("path must be a non-empty relative path")
    candidate = Path(relative)
    if candidate.is_absolute():
        raise AgentRequestError("absolute paths are not permitted")
    lexical = root / candidate
    probe = root
    for part in candidate.parts:
        if part in ("", "."):
            continue
        if part == "..":
            probe = probe / part
            continue
        probe = probe / part
        if probe.is_symlink():
            raise AgentRequestError("symbolic-link paths are not permitted")
    resolved = lexical.resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise AgentRequestError("path escapes the configured workspace") from exc
    return resolved


def parse_task(payload: Any) -> dict:
    if not isinstance(payload, dict):
        raise AgentRequestError("task must be a JSON object")
    if set(payload) != {"task_id", "goal", "actions"}:
        raise AgentRequestError("task must contain exactly task_id, goal, and actions")
    if not isinstance(payload["task_id"], str) or not payload["task_id"].strip():
        raise AgentRequestError("task_id must be a non-empty string")
    if not isinstance(payload["goal"], str) or not payload["goal"].strip():
        raise AgentRequestError("goal must be a non-empty string")
    actions = payload["actions"]
    if not isinstance(actions, list) or not actions or len(actions) > MAX_STEPS:
        raise AgentRequestError(f"actions must contain between 1 and {MAX_STEPS} steps")
    seen: set[str] = set()
    normalized = []
    for index, action in enumerate(actions):
        if not isinstance(action, dict) or set(action) - {"step_id", "tool", "path", "content", "expected_sha256", "backup_path"}:
            raise AgentRequestError(f"actions[{index}] has an invalid shape")
        if not {"step_id", "tool"} <= set(action):
            raise AgentRequestError(f"actions[{index}] requires step_id and tool")
        step_id, tool = action["step_id"], action["tool"]
        if not isinstance(tool, str):
            raise AgentRequestError(f"actions[{index}].tool must be a string")
        if not isinstance(step_id, str) or not step_id.strip() or step_id in seen:
            raise AgentRequestError(f"actions[{index}].step_id must be unique and non-empty")
        if tool not in ALLOWED_TOOLS:
            raise AgentRequestError(f"actions[{index}].tool is not allowlisted")
        if tool in {"inspect_directory", "read_text", "compile_python", "replace_text", "restore_backup"}:
            if not isinstance(action.get("path"), str):
                raise AgentRequestError(f"actions[{index}] requires a relative path")
        elif "path" in action:
            raise AgentRequestError(f"actions[{index}] does not accept path")
        if tool == "replace_text":
            if not isinstance(action.get("content"), str):
                raise AgentRequestError(f"actions[{index}].content must be a string")
            expected = action.get("expected_sha256")
            if not isinstance(expected, str) or len(expected) != 64 or any(ch not in "0123456789abcdefABCDEF" for ch in expected):
                raise AgentRequestError(f"actions[{index}].expected_sha256 must be a 64-character SHA-256 hex digest")
        elif tool == "restore_backup":
            if not isinstance(action.get("backup_path"), str) or not action["backup_path"].strip():
                raise AgentRequestError(f"actions[{index}].backup_path must be a relative backup path")
            expected = action.get("expected_sha256")
            if not isinstance(expected, str) or len(expected) != 64 or any(ch not in "0123456789abcdefABCDEF" for ch in expected):
                raise AgentRequestError(f"actions[{index}].expected_sha256 must be a 64-character SHA-256 hex digest")
            if "content" in action:
                raise AgentRequestError(f"actions[{index}] restore_backup does not accept content")
        elif "content" in action or "expected_sha256" in action or "backup_path" in action:
            raise AgentRequestError(f"actions[{index}] content/hash/backup fields are not valid for this tool")
        seen.add(step_id)
        normalized_action = {"step_id": step_id, "tool": tool}
        for field in ("path", "content", "expected_sha256", "backup_path"):
            if field in action:
                normalized_action[field] = action[field]
        normalized.append(normalized_action)
    return {"task_id": payload["task_id"], "goal": payload["goal"], "actions": normalized}


def _run(command: list[str], cwd: Path, timeout: int = 90) -> dict:
    try:
        completed = subprocess.run(
            command, cwd=cwd, capture_output=True, text=True, timeout=timeout,
            check=False, shell=False,
        )
        return {
            "exit_code": completed.returncode,
            "stdout": completed.stdout[-6000:],
            "stderr": completed.stderr[-3000:],
        }
    except subprocess.TimeoutExpired:
        return {"exit_code": 124, "stdout": "", "stderr": f"Timed out after {timeout} seconds."}
    except OSError as exc:
        return {"exit_code": 127, "stdout": "", "stderr": str(exc)}


def _replace_existing_text(action: dict, root: Path, backup_root: Path) -> dict:
    target = _inside(root, action["path"])
    if not target.is_file():
        raise AgentRequestError("replace_text requires an existing regular file")
    if target.is_symlink():
        raise AgentRequestError("replace_text refuses symbolic links")
    backup_root = backup_root.resolve()
    try:
        backup_root.relative_to(root)
    except ValueError:
        pass
    else:
        raise AgentRequestError("backup directory must be outside the workspace")
    old_bytes = target.read_bytes()
    if len(old_bytes) > MAX_READ_BYTES:
        raise AgentRequestError(f"replace_text is limited to {MAX_READ_BYTES} original bytes")
    actual_hash = hashlib.sha256(old_bytes).hexdigest()
    expected_hash = action["expected_sha256"].lower()
    if actual_hash != expected_hash:
        raise AgentRequestError("SHA-256 precondition failed; file was not changed")
    new_bytes = action["content"].encode("utf-8")
    if len(new_bytes) > MAX_READ_BYTES:
        raise AgentRequestError(f"replace_text is limited to {MAX_READ_BYTES} replacement bytes")
    relative = target.relative_to(root)
    backup = backup_root / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ") / relative
    backup.parent.mkdir(parents=True, exist_ok=False)
    backup.write_bytes(old_bytes)
    temp_name = None
    try:
        with tempfile.NamedTemporaryFile(mode="wb", dir=target.parent, prefix=".ario-replace-", delete=False) as temp:
            temp.write(new_bytes)
            temp.flush()
            os.fsync(temp.fileno())
            temp_name = temp.name
        os.replace(temp_name, target)
        temp_name = None
        written_hash = hashlib.sha256(target.read_bytes()).hexdigest()
        expected_new_hash = hashlib.sha256(new_bytes).hexdigest()
        if written_hash != expected_new_hash:
            restore_name = None
            try:
                with tempfile.NamedTemporaryFile(mode="wb", dir=target.parent, prefix=".ario-restore-", delete=False) as restore:
                    restore.write(old_bytes)
                    restore.flush()
                    os.fsync(restore.fileno())
                    restore_name = restore.name
                os.replace(restore_name, target)
                restore_name = None
            finally:
                if restore_name and os.path.exists(restore_name):
                    os.unlink(restore_name)
            raise AgentRequestError("post-write hash verification failed; original bytes restored from memory")
    except Exception:
        if temp_name and os.path.exists(temp_name):
            os.unlink(temp_name)
        raise
    return {
        "ok": True,
        "path": str(relative),
        "backup_path": str(backup),
        "before_sha256": actual_hash,
        "after_sha256": written_hash,
        "bytes_written": len(new_bytes),
        "verified": True,
    }


def _restore_existing_backup(action: dict, root: Path, backup_root: Path) -> dict:
    target = _inside(root, action["path"])
    if not target.is_file() or target.is_symlink():
        raise AgentRequestError("restore_backup requires an existing regular target file")
    candidate = Path(action["backup_path"])
    if candidate.is_absolute():
        raise AgentRequestError("backup_path must be relative to the backup directory")
    backup = (backup_root / candidate).resolve()
    resolved_backup_root = backup_root.resolve()
    try:
        backup.relative_to(resolved_backup_root)
    except ValueError as exc:
        raise AgentRequestError("backup_path escapes the backup directory") from exc
    probe = resolved_backup_root
    for part in candidate.parts:
        if part in ("", "."):
            continue
        if part == "..":
            raise AgentRequestError("backup_path traversal is not permitted")
        probe = probe / part
        if probe.is_symlink():
            raise AgentRequestError("symbolic-link backup paths are not permitted")
    if not backup.is_file():
        raise AgentRequestError("backup_path does not identify an existing regular file")
    current_bytes = target.read_bytes()
    if len(current_bytes) > MAX_READ_BYTES:
        raise AgentRequestError(f"restore_backup is limited to {MAX_READ_BYTES} current bytes")
    current_hash = hashlib.sha256(current_bytes).hexdigest()
    if current_hash != action["expected_sha256"].lower():
        raise AgentRequestError("SHA-256 precondition failed; target was not changed")
    backup_bytes = backup.read_bytes()
    if len(backup_bytes) > MAX_READ_BYTES:
        raise AgentRequestError(f"restore_backup is limited to {MAX_READ_BYTES} backup bytes")
    backup_hash = hashlib.sha256(backup_bytes).hexdigest()
    relative = target.relative_to(root)
    preserve = backup_root / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ") / "rollback-preimage" / relative
    preserve.parent.mkdir(parents=True, exist_ok=False)
    preserve.write_bytes(current_bytes)
    temp_name = None
    try:
        with tempfile.NamedTemporaryFile(mode="wb", dir=target.parent, prefix=".ario-restore-", delete=False) as temp:
            temp.write(backup_bytes)
            temp.flush()
            os.fsync(temp.fileno())
            temp_name = temp.name
        os.replace(temp_name, target)
        temp_name = None
        restored_hash = hashlib.sha256(target.read_bytes()).hexdigest()
        if restored_hash != backup_hash:
            raise AgentRequestError("restored file hash verification failed")
    except Exception:
        if temp_name and os.path.exists(temp_name):
            os.unlink(temp_name)
        restore_name = None
        try:
            with tempfile.NamedTemporaryFile(mode="wb", dir=target.parent, prefix=".ario-recover-", delete=False) as recovery:
                recovery.write(current_bytes)
                recovery.flush()
                os.fsync(recovery.fileno())
                restore_name = recovery.name
            os.replace(restore_name, target)
            restore_name = None
        finally:
            if restore_name and os.path.exists(restore_name):
                os.unlink(restore_name)
        raise
    return {
        "ok": True,
        "path": str(relative),
        "restored_from": str(backup),
        "preserved_current_version": str(preserve),
        "before_sha256": current_hash,
        "after_sha256": restored_hash,
        "verified": True,
    }


def execute_action(action: dict, root: Path, backup_root: Path | None = None) -> dict:
    tool = action["tool"]
    if tool == "restore_backup":
        if backup_root is None:
            raise AgentRequestError("restore_backup requires an external backup directory")
        return _restore_existing_backup(action, root, backup_root)
    if tool == "replace_text":
        if backup_root is None:
            raise AgentRequestError("replace_text requires an external backup directory")
        return _replace_existing_text(action, root, backup_root)
    if tool == "inspect_directory":
        target = _inside(root, action["path"])
        if not target.is_dir():
            raise AgentRequestError("inspect_directory target is not a directory")
        entries = sorted(
            ({"name": p.name, "kind": "directory" if p.is_dir() else "file"} for p in target.iterdir()),
            key=lambda item: (item["kind"], item["name"].casefold()),
        )
        return {"ok": True, "entries": entries[:200], "truncated": len(entries) > 200}
    if tool == "read_text":
        target = _inside(root, action["path"])
        if not target.is_file():
            raise AgentRequestError("read_text target is not a file")
        raw = target.read_bytes()
        if len(raw) > MAX_READ_BYTES:
            raise AgentRequestError(f"read_text is limited to {MAX_READ_BYTES} bytes")
        return {"ok": True, "path": action["path"], "content": raw.decode("utf-8-sig")}
    if tool == "git_status":
        result = _run(["git", "status", "--short", "--branch"], root)
    elif tool == "compile_python":
        target = _inside(root, action["path"])
        if not target.is_file() or target.suffix != ".py":
            raise AgentRequestError("compile_python requires an existing .py file")
        # Compile in memory so this inspection tool does not create __pycache__ files.
        result = _run([
            sys.executable, "-c",
            "from pathlib import Path; import sys; p=Path(sys.argv[1]); compile(p.read_text(encoding='utf-8-sig'), str(p), 'exec')",
            str(target),
        ], root)
    elif tool == "run_tests":
        tests = root / "implementation" / "tests"
        if not tests.is_dir():
            raise AgentRequestError("implementation/tests directory not found")
        result = _run([sys.executable, "-m", "pytest", "-q", "tests"], root / "implementation", timeout=180)
    else:
        raise AgentRequestError("tool is not allowlisted")
    return {"ok": result["exit_code"] == 0, **result}


def _append_event(ledger: Path, event: dict) -> None:
    ledger.parent.mkdir(parents=True, exist_ok=True)
    with ledger.open("a", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")


def run_task(payload: Any, workspace: str | Path, ledger_path: str | Path) -> dict:
    task = parse_task(payload)
    root = Path(workspace).resolve()
    if not root.is_dir():
        raise AgentRequestError("workspace must be an existing directory")
    ledger = Path(ledger_path).resolve()
    backup_root = ledger.parent / "backups"
    started = datetime.now(timezone.utc).isoformat()
    result = {
        "task_id": task["task_id"], "goal": task["goal"], "status": "RUNNING",
        "started_at": started, "steps": [],
        "completion_basis": "Completion means all declared allowlisted steps returned success; it does not establish that the goal is semantically achieved.",
    }
    _append_event(ledger, {"event": "TASK_STARTED", "task_id": task["task_id"], "goal": task["goal"], "timestamp": started})
    for action in task["actions"]:
        step = {"step_id": action["step_id"], "tool": action["tool"], "status": "RUNNING"}
        try:
            observation = execute_action(action, root, backup_root)
            step["observation"] = observation
            step["status"] = "SUCCEEDED" if observation.get("ok", True) else "FAILED"
        except (AgentRequestError, OSError, UnicodeError) as exc:
            step["status"] = "FAILED"
            step["observation"] = {"ok": False, "error": str(exc)}
        result["steps"].append(step)
        _append_event(ledger, {"event": "STEP_OBSERVED", "task_id": task["task_id"], **step, "timestamp": datetime.now(timezone.utc).isoformat()})
        if step["status"] != "SUCCEEDED":
            result["status"] = "STOPPED"
            result["recovery"] = "Fail-closed: stopped after the first failed step; no automatic retry or unapproved corrective action was attempted."
            break
    else:
        result["status"] = "COMPLETED"
    result["finished_at"] = datetime.now(timezone.utc).isoformat()
    _append_event(ledger, {"event": "TASK_FINISHED", "task_id": task["task_id"], "status": result["status"], "timestamp": result["finished_at"]})
    return result


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Run a bounded, allowlisted Ario Windows workspace task.")
    parser.add_argument("--task", required=True, help="Path to a declarative task JSON file")
    parser.add_argument("--workspace", required=True, help="Existing workspace root")
    parser.add_argument("--ledger", required=True, help="Append-only JSONL audit ledger path")
    args = parser.parse_args(argv)
    try:
        payload = json.loads(Path(args.task).read_text(encoding="utf-8-sig"))
        result = run_task(payload, args.workspace, args.ledger)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0 if result["status"] == "COMPLETED" else 2
    except (OSError, json.JSONDecodeError, AgentRequestError) as exc:
        print(json.dumps({"status": "UNKNOWN", "error": str(exc)}, ensure_ascii=False, sort_keys=True), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
