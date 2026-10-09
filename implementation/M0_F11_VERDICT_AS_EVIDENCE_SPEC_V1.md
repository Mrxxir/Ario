# M0 F11 — Verdict-as-Evidence Composition Firewall v1

## Status

**DESIGN SPECIFICATION — IMPLEMENTED ON PR BRANCH; RUNTIME TESTS NOT CONFIRMED; NOT ACCEPTANCE EVIDENCE**

Pre-registration source: `implementation/M0_PRE_REGISTRATION_V1.md`, fixture F11.
Reviewed baseline: `23d45feb3efcada7cc821e6202ae8a9a5613ecfc`.
This document does not modify or reinterpret the frozen pre-registration.

## 1. Threat model

An assessment or downstream audit may cite an earlier audit's verdict (for example, `PASS`) as if it were admissible observation evidence. That can create circular support: an audit conclusion is reintroduced as evidence for another conclusion without any new observation. A verdict may be recorded as a reported result or future composition input, but it does not thereby become an observation of the world.

## 2. Required distinctions

- **Observation reference:** points to a declared observation artifact.
- **Evidence reference:** points to an `Evidence` artifact whose observation references and provenance are auditable.
- **Audit-result reference:** points to an `AuditResult`, including verdict, basis, inspector/rule versions, scope, and run identity.
- **Assessment basis:** explicitly states which admissible evidence references support an assessment. Audit-result references must remain separately typed and must never be implicitly cast to evidence.

A generic `Reference` or a caller-supplied label is insufficient to change one category into another. Resolution must inspect the actual supplied artifact collections and detect missing or ambiguous IDs.

## 3. Normative invariants

**F11-I1 — No implicit cast.** An `AuditResult` or its verdict must never satisfy an `Assessment.admissible_evidence_refs` entry merely because IDs match or the result says `PASS`.

**F11-I2 — Referential resolution.** Every assessment evidence reference must resolve to exactly one admissible `Evidence` object under the declared ID rule. Missing, ambiguous, or wrong-kind references are rejected or remain explicitly UNKNOWN; they must not be treated as valid evidence.

**F11-I3 — Verdicts remain results.** A prior result may be stored in a separate typed result/composition field if a later contract needs it. Its presence alone grants no evidence, truth, or ontology status.

**F11-I4 — No circular laundering.** A verdict cannot upgrade its own underlying evidence, create an independent observation, or count as a second independent source.

**F11-I5 — Local scope only.** A local `PASS` means only that the named implementation's implemented checks reported no violation for the supplied input and declared rules. It does not mean the claim is true, all rules are implemented, or an ontology-level conclusion follows.

**F11-I6 — Deterministic classification.** Identical typed inputs and rule/configuration versions must yield the same F11 classification. Classification must not rely on natural-language labels such as “proof,” “verified,” or “PASS.”

## 4. Observable outcomes

The current engine reports violation strings rather than a complete typed composition-verdict algebra. Before implementation, choose one canonical outcome consistent with existing conventions:

- `COMPOSITION_FORBIDDEN`: a verdict is structurally detected in an evidence-only position.
- `EVIDENCE_INADMISSIBLE`: a reference resolves to an artifact of the wrong kind.
- `UNKNOWN`: artifact kind or resolution cannot be established from supplied data.

Do not silently produce `PASS` for an unresolved reference. Avoid emitting multiple aliases for one condition unless the specification explicitly requires both.

## 5. Minimum adversarial test matrix

| Case | Input condition | Required result |
|---|---|---|
| F11-A | Assessment reference resolves to a real `Evidence` object | No F11 violation; preserve valid F10 behavior |
| F11-B | Assessment evidence reference uses an `AuditResult.audit_id`; no Evidence has that ID | Reject as wrong-kind / composition forbidden |
| F11-C | Caller labels an audit-result ID as an evidence reference, but supplied artifacts identify it as an audit result | Reject; actual artifact kind takes precedence |
| F11-D | Assessment contains valid evidence plus an audit-result reference in its evidence list | Reject the wrong-kind reference without silently discarding valid evidence |
| F11-E | Unknown reference appears in the assessment evidence list | Must not yield PASS |
| F11-F | Audit result is recorded in a separately typed result field | No F11 violation solely for recording a result; no evidence/truth upgrade |
| F11-G | Same underlying observation is referenced by evidence and a derived verdict | Must not count the verdict as an additional independent observation |
| F11-H | Verdict is PASS versus FAIL while artifact typing is identical | Classification depends on artifact kind, not favorable/unfavorable verdict |

## 6. False-positive controls

- Ordinary evidence IDs containing words such as `PASS`, `AUDIT`, or `VERDICT` must not be rejected on string patterns alone.
- A report may quote or summarize a verdict without treating it as evidence.
- A future composition engine may consume typed audit results for a bounded meta-audit, provided the result remains a distinct category and no unsupported truth/ontology escalation occurs.
- Valid assessments citing ordinary admissible evidence must continue to pass the F10 path.

## 7. Implementation sequence

1. Inspect current reference-resolution and assessment contracts before modifying code.
2. Add the smallest explicit representation needed to distinguish observations, evidence, and audit results.
3. Add F11 adversarial and false-positive tests before or alongside implementation.
4. Run the complete regression suite and record the exact command, environment, commit SHA, test count, and output.
5. Review the diff for unintended changes; then update a separate post-implementation capability record.

Do not modify `M0_PRE_REGISTRATION_V1.md` or overwrite an earlier capability record as if it had always reflected this later design.

## 8. Acceptance boundary

F11 is accepted only when adversarial cases reject verdict laundering, false-positive controls preserve legitimate evidence, and the complete regression suite passes in a reproducible recorded run. Source presence, a design document, or unexecuted test definitions are not acceptance evidence.

**Current classification: IMPLEMENTED ON PR BRANCH / RUNTIME TESTS NOT CONFIRMED / NOT ACCEPTED.**
