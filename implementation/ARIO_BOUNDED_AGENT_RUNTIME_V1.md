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

## Guarded multi-step workflow

The runtime can combine a hash-preconditioned write, an exact postcondition, and a read-back in one task. The hash must be computed from the actual starting file at task creation time; do not guess or reuse a stale hash.

```json
{
  "task_id": "GUARDED-CHANGE-001",
  "goal": "Change one known text file and verify its declared result",
  "actions": [
    {
      "step_id": "s1-replace",
      "tool": "replace_text",
      "path": "notes.txt",
      "expected_sha256": "<64-character SHA-256 of the current file bytes>",
      "content": "EXPECTED RESULT"
    },
    {
      "step_id": "s2-postcondition",
      "tool": "verify_text",
      "path": "notes.txt",
      "expected_text": "EXPECTED RESULT"
    },
    {
      "step_id": "s3-readback",
      "tool": "read_text",
      "path": "notes.txt"
    }
  ]
}
```

The placeholder hash is illustrative, not executable. If the precondition fails, the write is refused. If the postcondition fails, the task stops before read-back or any later action. The runtime does not automatically undo a completed write just because a later independent verification fails; use `restore_backup` as a separate guarded action after reviewing the failure. This limitation is intentional and must remain visible in the audit trail.

## Allowlisted tools

- `inspect_directory`: list a directory (maximum 200 entries).
- `read_text`: read UTF-8 text under the workspace, capped at 20,000 bytes.
- `file_fingerprint`: read-only SHA-256 and byte count for an existing workspace file; it does not expose file contents or modify the file.
- `inspect_backup`: read-only SHA-256 and byte count for an existing backup selected by a relative path under the external backup directory; it rejects traversal and symbolic-link paths.
- `git_status`: run fixed `git status --short --branch`.
- `compile_python`: compile one existing `.py` file.
- `run_tests`: run the fixed `python -m pytest -q tests` command from `implementation/`.
- `replace_text`: replace an existing UTF-8 text file only when its current SHA-256 matches the task's expected hash. It writes a byte-for-byte backup outside the workspace (under the ledger directory's `backups/` folder), atomically replaces the file, and verifies the resulting hash. Original and replacement content are capped at 20,000 bytes.
- `restore_backup`: restore a backup selected by a relative path beneath the external `backups/` folder, only when the current target's SHA-256 matches the task's expected hash. Before restoration, it preserves the current target as a new backup and verifies the restored hash. A backup path cannot escape the backup folder.
- `verify_text`: compare an existing UTF-8 text file against an explicitly declared `expected_text` postcondition. A mismatch fails the step and stops the task, preventing later steps from running. This is exact text verification, not proof of broader semantic success.

There is no arbitrary shell, arbitrary command, network, delete-file, or privilege-escalation tool. The sole write capability is `replace_text`, which requires a precondition hash and an external backup. It must not be used for critical files without a separate review. Paths must be relative and remain within the resolved workspace. Each subprocess uses `shell=False` and a timeout.

## Control and recovery

- The full task schema and allowlist are validated before execution.
- Each step produces an observation recorded to the JSONL ledger.
- A failed step stops the task; no automatic retry or corrective write is attempted.
- Recovery preflight can use `file_fingerprint` to obtain the target's current hash and `inspect_backup` to confirm the candidate backup's hash. A subsequent `restore_backup` task must explicitly supply the observed current hash; inspection never triggers a write or chooses a backup automatically.
- `recovery_preflight` combines target and selected-backup fingerprinting into one read-only, ledger-recorded step. It records both SHA-256 hashes, byte counts, and whether the bytes are identical. `DIFFERENT_CONTENT` is evidence of difference, not evidence that either version is correct. The tool never selects a backup, restores, retries, or writes; a separate task must explicitly request `restore_backup` with the observed current-target hash.
- `COMPLETED` means all declared steps returned success. It does **not** prove the natural-language goal was semantically achieved.
- The event ledger is an audit aid, not tamper-proof storage. A local administrator can modify it; cryptographic integrity, OS-level isolation, approvals for writes, and independent goal verification remain future work.
- Rollback is itself a guarded write, not magic undo: it requires a known backup-relative path and the exact current-file hash, and preserves the replaced current version before restoration.
