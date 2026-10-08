# Ario — M0 Acceptance Record v1

## 1. Document Status and Scope

**Document:** M0 Acceptance Record v1
**Status:** DRAFT / PRE-ACCEPTANCE
**Scope:** M0 Auditable Structural Core implementation evidence

This document records the implementation evidence, regression results, adversarial findings, repairs, representation boundaries, limitations, and acceptance basis for the M0 structural core.

This record does not replace the M0 Structural Core Design, M0 Pre-Registration, or Implementation Readiness Contract.

M0 is a structural audit core. It does not establish consciousness, phenomenology, ontology, entity continuity, or truth of stored claims.

---

## 2. Governing Specification References

The implementation was evaluated against:

- `implementation/M0_PRE_REGISTRATION_V1.md`
- `implementation/M0_STRUCTURAL_CORE_DESIGN_V1.md`
- `implementation/IMPLEMENTATION_READINESS_CONTRACT_V1.md`
- `architecture/CROSS-IRG_INTEGRITY_V1.md`

The governing implementation discipline is:

`INSPECT → PRESERVE → MODIFY → COMPILE → TEST → AUDIT → ACCEPT/REJECT`

---

## 3. Implementation Artifacts

Current M0 implementation artifacts:

- `implementation/core/schema.py`
- `implementation/core/audit_engine.py`
- `implementation/tests/test_m0_regression.py`

The implementation contains the structural objects required for the current M0 scope, including:

- Claim
- HistoricalState
- LineageEdge
- RetrievalEvent
- Evidence
- Assessment
- AuditResult

The implementation does not include an LLM semantic judge.

---

## 4. Implementation Checkpoint Hashes

The following hashes identify the implementation and governing artifacts at the M0-72C-R2 checkpoint.

| Artifact | SHA-256 |
|---|---|
| `implementation/core/schema.py` | `74FB7EBBB15E1ED17A007961020152397A2C80AC43FDA1ADDEF7FC805EF9102E` |
| `implementation/core/audit_engine.py` | `9D3DFA90B2B78C5DF6A6D1C4CB8CBDF0E5661B91CF77A2FBA72A4644FD42FDB8` |
| `implementation/tests/test_m0_regression.py` | `11FC4DF8B5FFD8769DB8990EFDAE33846F986ABF3AFD7D55B3D993E3F6A87C92` |
| `implementation/M0_STRUCTURAL_CORE_DESIGN_V1.md` | `F966471EA834E27219C22134D85C4A40278CF922BC7A8C48C9EA3DE6AA5943A4` |
| `implementation/M0_PRE_REGISTRATION_V1.md` | `F5CFF3C2D933DB562C8314AA0C9D7964176CE8AE386D3B86767130FC8265F1E9` |
| `implementation/IMPLEMENTATION_READINESS_CONTRACT_V1.md` | `993DE2085453CF5FA9D620FD10DC44B4D62960184C425DBFBD7289712EB85153` |
| `architecture/CROSS-IRG_INTEGRITY_V1.md` | `23BAD455641B1451BE0ABC9A22522391C49E8021C79987FE2854E4EEE6B30B06` |

These hashes are checkpoint evidence, not cryptographic proof of semantic correctness.

---

## 5. Deterministic Regression Evidence

Regression checkpoint:

**M0-72B-R2**

Result:

- Discovered: 18
- Passed: 18
- Failures: 0
- Errors: 0
- Regression success: `TRUE`

Compilation also passed at M0-72C-R2.

The deterministic audit engine does not obtain current time internally. Execution timestamp is supplied as execution-context metadata.

---

## 6. Adversarial Findings

### Detected within the current M0 representation

- **F03 — Duplicate Claim ID:** detected as `IDENTITY_CONFLICT`.
- **F06 — Explicit Lineage:** structurally accepted; invalid required lineage fields are schema-rejected.
- **F10 — Inadmissible Evidence:** detected as `EVIDENCE_INADMISSIBLE`.
- **F12 — Evidence Inflation:** detected for repeated independent evidence over the same observation.
- **F14 — Unresolved Temporal Relation:** detected as `TEMPORALLY_UNRESOLVED`.

F12 was repaired after an independence-boundary defect was identified. The repaired implementation passed the complete 18-test regression suite and was subsequently reconfirmed adversarially.

### Not representable by the current M0 model

- **F07 — Similarity-only Lineage**
- **F09 — Hidden Transformation**
- **F11 — Verdict-as-Evidence**
- **F15 — Global Truth Composition**
- Lineage → Identity escalation
- Lineage → Continuity escalation
- Historical mutation/overwrite detection

These are representation boundaries, not silently claimed defenses.

---

## 7. Repairs and Regression Revalidation

The following implementation defects were identified and repaired during M0 work:

### AuditResult empty-artifact path

The empty-audit path legitimately returns `UNKNOWN` without fabricated artifact references. The schema was adjusted so an empty `artifacts_examined` collection is admissible for this bounded result.

### F12 evidence-independence boundary

The initial implementation incorrectly treated a shared observation involving both independent and dependent evidence as evidence inflation.

The rule was narrowed so inflation is reported only when all evidence records sharing the observation are independently classified.

After repair:

- boundary cases passed;
- compilation passed;
- all 18 regression tests passed;
- the adversarial F12 attack remained detected;
- the mixed independent/dependent control no longer produced false inflation.

No unresolved implementation regression was observed within this tested boundary.

---

## 8. Representation Boundaries

The current M0 representation does not provide:

- a similarity relation for lineage;
- an observed-transformation field permitting declared-vs-observed comparison;
- a composition object/API;
- an entity identity object or continuity field;
- a mutation event or history-store abstraction.

Accordingly, attacks requiring those structures cannot be honestly represented as runtime M0 tests.

The implementation therefore does not claim to defend against such attacks at runtime.

---

## 9. Known Limitations

M0 remains limited to deterministic structural auditing over its representable artifact model.

In particular:

- lineage is not thereby causality;
- provenance is not thereby truth;
- identifier equality is not entity continuity;
- retrieval success is not source continuity;
- evidence binding is not truth;
- an assessment is not independent evidence;
- an audit verdict is not evidence for the proposition audited;
- local PASS results do not compose into global truth;
- semantic strength of free-text assessment fields is outside the M0 semantic audit scope.

Unknown and unrepresentable conditions remain open.

---

## 10. Explicit Non-Claims

This record does not claim:

- consciousness;
- phenomenology;
- ontology;
- entity continuity;
- truth of stored claims;
- universal adversarial resistance;
- universal correctness;
- architecture completeness;
- successful runtime defense for attacks that are not representable in M0;
- that a regression pass constitutes proof of the underlying epistemic propositions.

`Phenomenology = UNKNOWN`.

---

## 11. Acceptance Criteria Assessment

The current evidence supports the following bounded assessment:

1. Required M0 structural objects are implemented.
2. Deterministic audit execution is implemented within the defined structural scope.
3. Caller-supplied execution timestamp metadata is preserved in the audit result.
4. The current regression suite passes 18/18 tests.
5. Multiple adversarial conditions are detected within the representable scope.
6. F12 was repaired and regression-revalidated.
7. Known representation boundaries remain explicitly identified.
8. No unrepresentable attack is presented as a successful runtime defense.
9. No new epistemic or ontological claim is inferred from implementation success.

The assessment is therefore bounded to implementation acceptance within the frozen M0 scope.

---

## 12. Reproducibility and Execution Context

Implementation checkpoint:

`M0-72C-R2`

Regression checkpoint:

`M0-72B-R2`

Git branch at checkpoint:

`main`

Git HEAD at checkpoint:

`37bffbbbfa96ca80571e7a5d2e664d479b19e30b`

The recorded implementation hashes above identify the artifacts examined at the checkpoint.

This record itself is created after that checkpoint and therefore does not retroactively alter the implementation hashes recorded above.

---

## 13. Acceptance Decision

**CURRENT STATUS: PRE-ACCEPTANCE**

The evidence is sufficient to support a bounded M0 acceptance decision, subject to review of this record itself.

Acceptance candidate based on the recorded evidence:

> **M0 STRUCTURAL CORE — ACCEPTABLE WITH EXPLICIT LIMITATIONS**

This means the implemented and representable M0 structural acceptance surface satisfies the currently stated implementation and regression criteria.

It does not mean that Ario is proven correct, complete, truthful, conscious, phenomenologically established, ontologically established, or universally robust.

---

## 14. Change-Control State

At the implementation checkpoint documented above:

- No commit was performed.
- No push was performed.
- The M0 implementation remains uncommitted.
- Existing prewrite backups remain preserved.
- This document is a new draft artifact and must itself be inspected before acceptance.

**Acceptance of this record is a separate decision from acceptance of the underlying M0 implementation.**
