# M0 Post-Implementation Source Review — 2026-10-09

**Status:** SOURCE REVIEW ONLY — NO RUNTIME TEST CLAIM  
**Repository baseline:** `93ba04e41de85ed4eff73436e3bf3fcd5d88a31d`  
**Scope:** Reconcile the current F07/F09 implementation with the older M0 Capability Audit Record and identify the next unresolved pre-registered fixtures.

## 1. Method and limits

This review inspected the current `main` source for:

- `implementation/core/schema.py`
- `implementation/core/audit_engine.py`
- `implementation/tests/test_m0_regression.py`
- `implementation/M0_PRE_REGISTRATION_V1.md`
- `implementation/M0_CAPABILITY_AUDIT_RECORD_V1.md`

This was a source-level inspection through the repository interface. The test suite was **not executed** as part of this review. Test definitions in source are not evidence that they passed in the current environment. No claim of runtime success is made here.

## 2. F07 — Similarity-only lineage

The current source includes `LineageCandidate`, candidate validation in the audit engine, and regression tests including:

- `test_f07_similarity_candidate_is_inadmissible`
- `test_f07_explicit_relation_candidate_is_admissible`
- `test_f07_unsupported_rule_is_unknown`
- `test_f07_undeclared_rule_is_unknown`

The test `test_f07_similarity_only_lineage_is_inadmissible` also explicitly documents a limitation: the current `LineageEdge` model has no similarity relation type, so that particular test only checks that a structurally explicit edge is not treated as similarity-only.

**Bounded finding:** F07 has been operationalized in part through the candidate path. The older capability audit's blanket description of F07 as non-operationalized is stale relative to current source, but the full pre-registered attack surface should not be called passed from source inspection alone.

## 3. F09 — Hidden retrieval transformation

The current source includes an `observed_transformation_reference` field on `RetrievalEvent`, comparison of declared and observed transformation references in the audit engine, and regression tests:

- `test_f09_retrieval_with_hidden_transformation`
- `test_f09_retrieval_with_transformation_discrepancy`

**Bounded finding:** F09 has been operationalized in source. Runtime pass status remains unverified by this review.

## 4. F11 — Verdict used as evidence

The pre-registration defines F11 as rejecting an assessment that uses an audit verdict as evidence. In the current inspected model:

- `AuditInput` has no explicit audit-verdict/composition input collection;
- `Evidence.observation_refs` and `Assessment.admissible_evidence_refs` use generic references, without an explicit evidence-kind discriminator that identifies an audit verdict as such;
- no F11-specific regression test was found in `test_m0_regression.py`.

**Finding:** F11 remains unoperationalized in the inspected schema/API and regression suite. A generic reference alone cannot reliably establish whether the referenced object is an observation, evidence item, assessment, or audit verdict.

## 5. F15 — Multiple local PASS results escalated to global truth

The pre-registration defines F15 as preventing five local PASS results from being composed into global truth or ontology claims. In the current inspected model:

- `AuditInput` has no explicit multi-IRG aggregation/composition-rule input;
- `AuditResult` contains a local verdict and basis, but the inspected API has no explicit typed composition artifact and semantic-scope contract for aggregating multiple verdicts;
- no F15-specific regression test was found in `test_m0_regression.py`.

**Finding:** F15 remains unoperationalized in the inspected schema/API and regression suite. It cannot be claimed defended by the current local audit rules alone.

## 6. Record reconciliation

The older `M0_CAPABILITY_AUDIT_RECORD_V1.md` is a historical checkpoint record and must not be silently rewritten. Its blanket F07/F09 status is no longer an accurate description of the later source tree. This addendum preserves that history while recording the source-level changes and the remaining gaps.

This review does **not** change the frozen pre-registration, does not classify F07/F09 as runtime PASS, and does not claim the whole M0 acceptance surface is complete.

## 7. Recommended next step

Prioritize F11 before F15:

1. Define a typed, auditable distinction between observations/evidence and audit verdicts, with no implicit conversion of verdicts into evidence.
2. Add F11 adversarial and false-positive regression cases.
3. Execute the full regression suite in a reproducible environment and record the exact command, environment, commit, and result.
4. Only then design F15's explicit composition input and bounded output semantics.

**Current status:** F07 = partially operationalized in source; F09 = operationalized in source; F11 = not operationalized in inspected schema/API; F15 = not operationalized in inspected schema/API; runtime verification by this review = NOT PERFORMED.
