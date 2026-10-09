from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


MAX_STEPS = 8
MAX_READ_BYTES = 20_000
ALLOWED_TOOLS = {"inspect_directory", "read_text", "git_status", "compile_python", "run_tests"}


class AgentRequestError(ValueError):
    pass


def _inside(root: Path, relative: str) -> Path:
    if not isinstance(relative, str) or not relative.strip():
        raise AgentRequestError("path must be a non-empty relative path")
    candidate = Path(relative)
    if candidate.is_absolute():
        raise AgentRequestError("absolute paths are not permitted")
    resolved = (root / candidate).resolve()
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
        if not isinstance(action, dict) or set(action) - {"step_id", "tool", "path"}:
            raise AgentRequestError(f"actions[{index}] has an invalid shape")
        if not {"step_id", "tool"} <= set(action):
            raise AgentRequestError(f"actions[{index}] requires step_id and tool")
        step_id, tool = action["step_id"], action["tool"]
        if not isinstance(step_id, str) or not step_id.strip() or step_id in seen:
            raise AgentRequestError(f"actions[{index}].step_id must be unique and non-empty")
        if tool not in ALLOWED_TOOLS:
            raise AgentRequestError(f"actions[{index}].tool is not allowlisted")
        if tool in {"inspect_directory", "read_text", "compile_python"}:
            if not isinstance(action.get("path"), str):
                raise AgentRequestError(f"actions[{index}] requires a relative path")
        elif "path" in action:
            raise AgentRequestError(f"actions[{index}] does not accept path")
        seen.add(step_id)
        normalized.append({"step_id": step_id, "tool": tool, **({"path": action["path"]} if "path" in action else {})})
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


def execute_action(action: dict, root: Path) -> dict:
    tool = action["tool"]
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
        result = _run([sys.executable, "-m", "py_compile", str(target)], root)
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
            observation = execute_action(action, root)
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
