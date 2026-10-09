# Ario M0 JSON Runtime

This is the first executable boundary around the deterministic M0 audit engine.
It accepts a JSON request, validates it against the typed Python schema, invokes
the existing audit engine, and emits a structured JSON result. It does not execute
arbitrary commands or treat a model-generated claim as an audit verdict.

## Run on Windows PowerShell

From the repository root:

```powershell
@'
{
  "audit_id": "AUDIT-LOCAL-001",
  "rule_versions": ["M0-1.0"],
  "configuration_id": "LOCAL-JSON-CLI-V1",
  "execution_timestamp": "2026-10-09T12:00:00+03:30",
  "artifacts": {}
}
'@ | Set-Content -Encoding utf8 .\implementation\sample_audit.json

python .\implementation\ario_cli.py --input .\implementation\sample_audit.json
```

The example intentionally returns `UNKNOWN`: no primary audit artifacts were
provided. A successful process exit means the request was parsed and the audit
ran; it does not mean the audit verdict is PASS.

To append the result to a JSON Lines history without replacing prior entries:

```powershell
python .\implementation\ario_cli.py --input .\implementation\sample_audit.json --ledger .\runtime-data\audit-ledger.jsonl
```

The ledger is opened in append mode. Keep it outside the Git repository if it
contains real local records. This is append-only application behavior, not a
tamper-proof storage guarantee.

## Request shape

The top-level keys are exactly `audit_id`, `rule_versions`,
`configuration_id`, `execution_timestamp`, and `artifacts`. The `artifacts`
object uses the field names and typed structures in `core.audit_engine.AuditInput`
and `core.schema`. Unknown fields are rejected rather than silently ignored.

## Current boundary

This entry point executes deterministic audits only. It is not yet a general
purpose autonomous OS agent and does not grant shell, network, or arbitrary file
execution. The next integration step is a separately audited tool-execution
adapter with explicit action records, observed outcomes, and failure handling.
