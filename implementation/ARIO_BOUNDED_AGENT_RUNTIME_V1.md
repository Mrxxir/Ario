# Ario Bounded Workspace Agent Runtime V1

## Purpose

`ario_agent.py` is a first executable, bounded workspace agent. It is deliberately not an unrestricted shell agent and does not claim general autonomy. A task declares a goal and a short sequence of allowlisted actions; the runtime records observations and stops on the first failed step.

## Run on Windows

Create a UTF-8 task file such as `$env:TEMP\ario-task.json`:

```json
{
  "task_id": "WORKSPACE-INSPECTION-001",
  "goal": "Inspect the Ario implementation and confirm the working tree state",
  "actions": [
    {"step_id": "s1", "tool": "git_status"},
    {"step_id": "s2", "tool": "inspect_directory", "path": "implementation"},
    {"step_id": "s3", "tool": "read_text", "path": "implementation/M0_JSON_RUNTIME_V1.md"}
  ]
}
```

From the repository root, run:

```powershell
python .\implementation\ario_agent.py --task "$env:TEMP\ario-task.json" --workspace "$HOME\Ario" --ledger "$HOME\Ario\runtime\agent-events.jsonl"
```

The ledger is append-only JSONL. Keep it in a trusted directory and protect it with normal filesystem permissions.

## Allowlisted tools

- `inspect_directory`: list a directory (maximum 200 entries).
- `read_text`: read UTF-8 text under the workspace, capped at 20,000 bytes.
- `git_status`: run fixed `git status --short --branch`.
- `compile_python`: compile one existing `.py` file.
- `run_tests`: run the fixed `python -m pytest -q tests` command from `implementation/`.

There is no arbitrary shell, arbitrary command, network, write-file, delete-file, or privilege-escalation tool. Paths must be relative and remain within the resolved workspace. Each subprocess uses `shell=False` and a timeout.

## Control and recovery

- The full task schema and allowlist are validated before execution.
- Each step produces an observation recorded to the JSONL ledger.
- A failed step stops the task; no automatic retry or corrective write is attempted.
- `COMPLETED` means all declared steps returned success. It does **not** prove the natural-language goal was semantically achieved.
- The event ledger is an audit aid, not tamper-proof storage. A local administrator can modify it; cryptographic integrity, OS-level isolation, approvals for writes, and independent goal verification remain future work.
