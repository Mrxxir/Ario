# M0 F11 Post-Implementation Source Review — 2026-10-09

## Status

**BOUNDED SOURCE REVIEW COMPLETE; DECLARED M0 REGRESSION FIXTURES PASS ON THE TESTED PR MERGE REF; NOT A CLAIM OF GENERAL PROOF OR ONTOLOGICAL TRUTH.**

This is a post-implementation review record. It does not alter the frozen pre-registration or retroactively rewrite earlier capability/acceptance records.

## Scope reviewed

- Frozen acceptance source: `implementation/M0_PRE_REGISTRATION_V1.md`, fixture F11.
- Structural contract: `implementation/M0_STRUCTURAL_CORE_DESIGN_V1.md`.
- Assessment and deterministic audit requirements: `implementation/IMPLEMENTATION_READINESS_CONTRACT_V1.md`.
- F11 implementation: `implementation/core/audit_engine.py` and `implementation/core/schema.py`.
- Regression cases: `implementation/tests/test_m0_regression.py`.
- Dedicated contract: `implementation/M0_F11_VERDICT_AS_EVIDENCE_SPEC_V1.md`.
- GitHub Actions workflow: `.github/workflows/implementation-regression.yml`.

The historical M0 acceptance record, capability audit record, and prior source review remain unchanged. Their statements describe the earlier inspected implementation and remain useful as historical evidence.

## Findings and changes made

### F11-R1 — Rule-version activation

**Finding:** The initial F11 patch emitted `COMPOSITION_FORBIDDEN` without checking that `M0-F11-1.0` was declared in the audit invocation's `rule_versions`. This differed from the version-gated pattern used by F05/F07 and risked changing outcomes for an invocation that declared only older rules.

**Change:** F11-specific result-kind classification is activated only when `M0-F11-1.0` is declared. If the version is absent, an audit-result-only ID follows the legacy unresolved-reference path and is `EVIDENCE_INADMISSIBLE`, not the F11-specific classification.

### F11-R2 — Ambiguous artifact identity

**Finding:** The initial patch collapsed audit-result IDs into a set and could not distinguish duplicate audit-result IDs or a collision between an Evidence ID and an AuditResult ID.

**Change:** Under F11, cross-kind collisions and duplicate audit-result IDs produce `UNKNOWN`. The resolver does not silently choose one kind or one result. Duplicate Evidence IDs also remain `UNKNOWN`.

### F11-R3 — Prior result alone could yield PASS

**Finding:** Because prior audit results were included in `artifacts_examined`, an input containing only a prior result could pass the engine's former non-empty-input guard. That risked making mere result recording look like a successful fresh audit.

**Change:** The engine now requires at least one primary artifact collection for a new structural audit. If only prior audit results are supplied, the fresh result is `UNKNOWN`; the prior result is still recorded and does not itself trigger `COMPOSITION_FORBIDDEN`.

### F11-R4 — Test strength and false-positive boundaries

The regression cases cover admissible evidence, a prior result referenced as evidence, caller-supplied type labels, mixed valid and invalid references, unknown IDs, separately recorded results, verdict polarity, keyword false positives, duplicate evidence IDs, version gating, cross-kind collisions, and duplicate audit-result IDs. The nested prior result's observation references are not re-expanded into the current audit's examined-artifact list.

## Runtime validation

- Workflow: GitHub Actions `Implementation Regression`, run `37917807274`.
- Tested PR head: `84a0fee68550d52fc2857bf48f82a245f448af63`.
- Tested pull-request merge ref: `40adefd8eb4f70fb7d8e263928c2ffbf5c5cf30e`.
- Base: `23d45feb3efcada7cc821e6202ae8a9a5613ecfc`.
- Environment: GitHub-hosted Ubuntu 24.04.5; CPython 3.13.16.
- Command: `python -m pytest -q tests/test_m0_regression.py`.
- Observed result: **45 passed in 0.07s**.

The test command covers the repository's only current test file under `implementation/tests`. This is evidence for the declared regression fixtures on the tested merge ref, not evidence that every conceivable adversarial input has been covered. The specification-only follow-up commit must receive its own workflow run as well.

## Bounded disposition

The reviewed implementation now explicitly distinguishes supplied prior audit results from assessment evidence, refuses to treat unresolved/ambiguous IDs as admissible evidence, gates the F11-specific classification by its declared rule version, and avoids producing a fresh `PASS` from prior-result-only input.

This does **not** establish:
- that an audit verdict is true merely because it is `PASS`;
- that every possible route for semantic or evidentiary laundering has been eliminated;
- that F15's five-local-PASS-to-global-truth composition firewall is implemented;
- any conclusion about consciousness, identity ontology, or truth beyond the tested structural contract.

F15 remains a separate fixture and must be designed and tested independently. The frozen pre-registration is unchanged. No change in this PR has been merged into `main`.
