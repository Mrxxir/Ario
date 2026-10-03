# IRG-01 — Claim Identity Reference Persistence

**Version:** 0.2.1  
**Status:** BASELINE  
**Type:** Experimental Specification  
**Implementation Status:** NOT IMPLEMENTED  
**Validation Status:** SPECIFICATION-LEVEL BASELINE  
**Requirement ID:** IRG-01

---

## 1. Requirement

> Every Claim should have a stable, referable identity that can be followed through creation, storage, retrieval, and lineage.

IRG-01 defines an implementation-independent probe set for examining whether a Claim has an explicit and observable identity that can be followed across defined operations.

IRG-01 does not assume that the requirement is satisfied.

It does not define the internal implementation mechanism by which identity is created, stored, retrieved, or referenced.

---

## 2. Scope

IRG-01 examines:

- explicit Claim identity semantics;
- identity assignment during Claim creation;
- identity preservation during retrieval;
- downstream references to Claim identity;
- persistence of the defined identity reference across an observed state transition.

IRG-01 does **not** establish:

- Claim truth;
- semantic continuity;
- entity continuity;
- causal continuity;
- ontological identity;
- complete historical preservation;
- global identifier uniqueness;
- cryptographic security;
- correctness of implementation outside the inspected scope;
- completeness of lineage;
- correctness of a Claim's new state.

Identifier equality alone must not be interpreted as proof of any of the above.

---

# 3. Probe Set

## IRG-01.P01 — Schema Identity

### Objective

Determine whether Claim Identity is explicitly defined in the observable Claim structure and whether its semantic relation to the Claim can be reconstructed without free interpretation.

### In Scope

- Claim structure;
- Claim identity;
- defined relation between Claim and Identity.

### Out of Scope

- global uniqueness;
- cryptographic security;
- Claim truth;
- operational persistence;
- entity continuity.

### Expected Artifact

An observable structure showing the relation:

`Claim → Identity`

### Observable Condition

An inspector can reconstruct the Claim-to-Identity relation from the examined artifact without inventing an unstated semantic interpretation.

### Negative Condition

The Claim exists but:

- its identity cannot be identified;
- identity semantics are undefined; or
- multiple possible identity relations exist without a resolvable definition.

### Verdicts

- `SUPPORTED`
- `CONTRADICTED`
- `NOT_OBSERVED`
- `AMBIGUOUS`

### Limitation

P01 establishes only the structural definition and observable semantics of Claim Identity. It does not establish that identity is operationally created or preserved.

---

## IRG-01.P02 — Identity Creation

### Objective

Determine whether an identity is actually assigned during Claim creation according to the identity semantics defined by P01.

### In Scope

The Claim creation path.

### Out of Scope

- retrieval;
- identity uniqueness;
- identity persistence across later operations;
- lineage;
- cryptographic properties.

### Expected Artifact

An observable creation sequence equivalent to:

`CREATE CLAIM → IDENTITY ASSIGNED → CREATION RESULT AVAILABLE`

### Observable Condition

The examined creation path visibly establishes the relationship between Claim creation and identity assignment.

### Negative Condition

A valid Claim creation path is observed in which the required identity is absent.

### Verdicts

- `SUPPORTED`
- `CONTRADICTED`
- `NOT_OBSERVED`
- `AMBIGUOUS`

### Limitation

P02 does not establish identity uniqueness, retrieval persistence, or lineage.

---

## IRG-01.P03 — Identity Retrieval

### Objective

Determine whether the defined Claim Identity is preserved when the Claim is retrieved through the examined retrieval path.

### In Scope

The relationship:

`Creation → Retrieval`

for the inspected Claim.

### Out of Scope

- other retrieval paths;
- global uniqueness;
- cryptographic security;
- semantic identity;
- entity continuity.

### Required Input

Observable creation and retrieval artifacts sufficient to establish:

1. the Claim inspected at creation;
2. the Claim inspected at retrieval;
3. the identity observed at each point.

The relation establishing that the two inspected objects are the same Claim must be supported by admissible evidence **independent of the identity value under test**.

### Expected Condition

`Creation: Claim = C123, Identity = I123`

`Retrieval: Claim = C123, Identity = I123`

### Observable Condition

The same Claim is established at both points by admissible non-identity evidence, and its defined identity reference matches.

### Negative Condition

The same Claim is established at both points by admissible non-identity evidence, but its defined identity reference differs.

### Verdicts

- `SUPPORTED`
- `CONTRADICTED`
- `NOT_OBSERVED`
- `AMBIGUOUS`

### Limitation

Equality of identity references establishes only reference continuity under the defined identity semantics.

It does not independently establish:

- entity continuity;
- semantic continuity;
- causal continuity;
- ontological identity.

Identity under test must not be used as the sole basis for establishing the same-Claim relation.

---

## IRG-01.P04 — Reference / Lineage

### Objective

Determine whether a downstream artifact can resolve a reference to a specific Claim Identity.

### In Scope

`Downstream Reference → Claim Identity → Claim`

### Out of Scope

- Claim truth;
- Evidence truth;
- complete lineage;
- historical completeness;
- causal continuity.

### Observable Condition

At least one examined downstream reference resolves unambiguously to an existing Claim Identity.

### Negative Condition

A valid downstream reference is observed that resolves to an incorrect or inconsistent Claim Identity.

### Verdicts

- `SUPPORTED`
- `CONTRADICTED`
- `NOT_OBSERVED`
- `AMBIGUOUS`

### Limitation

One successful reference does not establish complete lineage.

---

## IRG-01.P05 — Identity Reference Persistence Across State Transition

### Objective

Determine whether the defined Claim Identity reference remains stable across an observed state transition for the inspected Claim.

### In Scope

The probe examines:

- Claim at `t1`;
- identity reference at `t1`;
- observed state transition;
- Claim at `t2`;
- identity reference at `t2`;
- identity semantics established by P01.

### Out of Scope

P05 does **not** establish:

- entity continuity;
- semantic continuity;
- causal continuity;
- ontological identity;
- historical continuity;
- append-only integrity;
- truth;
- correctness of the new state.

### Required Identity-Independent Relation

The relation establishing that the inspected Claim at `t1` and the inspected Claim at `t2` are the same Claim must be established through admissible evidence independent of the identity reference being tested.

The identity value itself must not be sufficient to establish this relation.

### Expected Artifact

`t1: Claim = C123, Identity = I123, State = A`

`t2: Claim = C123, Identity = I123, State = B`

### Supported Condition

`SUPPORTED` if:

1. the same inspected Claim is established at `t1` and `t2` by admissible identity-independent evidence;
2. the state transition is established by admissible observation;
3. the defined identity reference matches across the transition.

### Contradicted Condition

`CONTRADICTED` if:

1. the same Claim is established at `t1` and `t2` by admissible identity-independent evidence;
2. the transition is established; and
3. the defined identity reference differs.

Example:

`C123 / I123 / A → C123 / I987 / B`

### Not Observed

`NOT_OBSERVED` when the required transition or required identity observation is missing.

### Ambiguous

`AMBIGUOUS` when observations exist but the relation establishing the same Claim across the transition cannot be determined.

Example:

`C123 / I123 → C456 / I123`

The same identity value does not establish that `C123` and `C456` are the same Claim.

### Limitation

P05 establishes only persistence of the defined identity reference across the tested transition.

It must not be interpreted as evidence of:

- semantic continuity;
- entity continuity;
- causal continuity;
- historical continuity;
- ontological identity.

This limitation is reinforced by `INV-S12 — No Continuity Inflation`.

---

# 4. Master Probe Record Schema v0.2

```
MASTER_PROBE_RECORD
│
├── record_id
├── schema_version
│
├── probe
│   ├── probe_id
│   ├── requirement_id
│   ├── probe_version
│   ├── status
│   ├── objective
│   ├── scope
│   │   ├── in_scope
│   │   └── out_of_scope
│   ├── input
│   ├── expected_artifact
│   ├── observable_condition
│   ├── negative_condition
│   ├── admissibility_rules
│   ├── verdict_rules
│   │   ├── SUPPORTED
│   │   ├── CONTRADICTED
│   │   ├── NOT_OBSERVED
│   │   └── AMBIGUOUS
│   └── limitations
│
├── inspection
│   ├── inspection_scope
│   ├── inspector_context
│   │   ├── inspector_id
│   │   ├── inspector_version
│   │   ├── execution_timestamp
│   │   └── configuration_id
│   └── artifacts_examined
│
├── observations[]
│   ├── observation_id
│   ├── modality
│   ├── origin
│   ├── source_reference
│   ├── retrieval_timestamp
│   ├── derivation_id
│   ├── dependency_refs[]
│   └── raw_content
│
├── evidence[]
│   ├── evidence_id
│   ├── observation_refs[]
│   ├── evidence_level
│   └── independence_status
│
├── assessment
│   ├── assessment_id
│   ├── assessment_version
│   ├── rule_version
│   ├── admissible_evidence_refs[]
│   ├── condition_evaluation
│   └── assessment_basis
│
├── verdict
│   ├── verdict
│   └── verdict_basis
│
└── provenance
    ├── created_at
    ├── derived_from[]
    └── supersedes[]
```

The schema separates raw observations from evidence, assessment, and verdict.

Raw observations must not contain assessment or verdict.

Raw observations are historical records of what was observed and must remain immutable.

Assessments are versioned and must never silently overwrite previous assessments.

Evidence references observations rather than embedding the raw observation itself.

---

# 5. Evidence Semantics

## Evidence Levels

`E0 — NO_EVIDENCE`  
`E1 — INDICATIVE`  
`E2 — CORROBORATED`  
`E3 — DIRECTLY_OBSERVED`

Evidence level describes the character of the available evidence.

It does not determine the verdict by itself.

IRG-01 does not impose a universal minimum evidence level such as `E2` for every probe.

Admissibility remains governed by the probe's explicit observable condition and admissibility rules.

---

## Independence

`INDEPENDENT`  
`DEPENDENT`  
`UNKNOWN`

Independence status describes the relationship of an evidence item to other evidence and observations.

Multiple representations of the same underlying observation must not be counted as multiple independent evidence items.

---

# 6. Observation Requirements

Each observation must have an explicit:

- `observation_id`
- `modality`
- `origin`
- `source_reference`
- `retrieval_timestamp`
- `derivation_id`
- `dependency_refs`
- `raw_content`

Observation identity does not imply observation truth.

Observation provenance does not imply evidential independence.

Origin and authenticity must remain distinguishable from descriptive metadata.

---

# 7. Assessment and Verdict Semantics

A verdict is local to:

`Objective + Scope + Observable Condition + Admissible Evidence + Verdict Basis + Limitations`

Therefore:

`SUPPORTED` means that the defined observable condition was satisfied within the examined scope.

It does not mean that the broader philosophical or ontological claim is true.

`CONTRADICTED` means that admissible evidence directly violates the defined condition within scope.

`NOT_OBSERVED` means that the required observation was not obtained or was insufficiently available.

`NOT_OBSERVED` must never silently become `CONTRADICTED`.

`AMBIGUOUS` means relevant evidence exists but the relation required by the probe cannot be resolved.

`UNKNOWN` is an epistemic state, not an additional probe verdict. Where evidence is insufficient, the reason for the unknown state must be represented through `NOT_OBSERVED` or `AMBIGUOUS`, as appropriate.

---

# 8. Global Invariants

## INV-P01 — No Evidence Inflation

One underlying observation must not become multiple independent evidence items merely through:

- representation;
- duplication;
- documentation;
- search;
- reformatting;
- repeated probing.

## INV-P02 — No Verdict in Raw Observation

Raw observations must not contain verdicts or assessments.

## INV-P03 — No Implicit Aggregation

Individual probe verdicts must not be silently aggregated into a higher-level IRG-01 verdict.

Any aggregation requires an explicit, versioned aggregation rule.

## INV-P04 — No Silent Reassessment

A new assessment must not overwrite or erase an earlier assessment.

Historical assessments remain resolvable.

## INV-P05 — No Absence Inference

Failure to observe an expected artifact is not automatically evidence that the artifact does not exist.

Absence of observation must remain distinguishable from contradiction.

---

# 9. Semantic Invariants

## INV-S01 — One Field → One Semantic Meaning

A field must not silently carry multiple incompatible meanings.

## INV-S02 — Raw Observation Purity

Raw observations contain observations, not verdicts or assessments.

## INV-S03 — Exact Historical Provenance

Historical provenance must remain resolvable to the exact artifact or source state that was observed.

## INV-S04 — Version Auditability

Probe, rule, schema, and inspector versions must be auditable.

## INV-S05 — UNKNOWN Must Remain Representable

When available evidence is insufficient, an unknown epistemic state must remain representable together with the reason for insufficiency.

## INV-S06 — No Self-Supporting Evidence Cycle

Evidence must not ultimately establish its own validity through a circular support chain.

## INV-S07 — Scope Isolation

Out-of-scope observations must not silently satisfy an in-scope requirement.

## INV-S08 — Origin / Authenticity Distinction

Observation origin or authenticity must remain distinguishable from metadata describing the observation.

## INV-S09 — Assessment Cannot Exceed Observable Condition

An assessment must not claim more than the probe's observable condition establishes.

## INV-S10 — Explicit Negative Conditions

Negative conditions must be explicitly defined rather than inferred from the absence of a positive result.

## INV-S11 — Deterministic Assessment

Given the same admissible inputs and the same versioned rules, assessment must be deterministic.

## INV-S12 — No Continuity Inflation

Equality of an identifier or reference must not by itself be interpreted as proof of:

- entity continuity;
- semantic continuity;
- causal continuity;
- historical continuity;
- ontological identity.

---

# 10. Locality of Verdict

Every probe verdict must remain local to its own:

`objective + scope + observable condition + admissible evidence + verdict basis + limitations`

A verdict from one probe must not silently expand the semantic scope of another probe.

For example:

`P05 = SUPPORTED`

does not entail:

- entity continuity = SUPPORTED
- semantic continuity = SUPPORTED
- causal continuity = SUPPORTED
- historical continuity = SUPPORTED
- ontological identity = SUPPORTED

---

# 11. Semantic Borrowing Prohibition

A probe may not borrow the validity or semantic scope of another probe's verdict.

For example:

`P01 = SUPPORTED`

does not establish:

`P03 = SUPPORTED`

and:

`P05 = SUPPORTED`

does not establish:

`semantic continuity = SUPPORTED`

Each probe must independently satisfy its own observable condition within its own scope.

---

# 12. Architectural Anti-Self-Confidence

The architecture must remain auditable even when previous observations have consistently produced successful results.

> ایستاده بودن امروز، تضمینِ ایستادن فردا نیست؛ بنابراین معماری باید همچنان قابل ممیزی بماند.

Successful prior assessments do not grant immunity from future contradiction, reassessment, or failure.

---

# 13. Architectural Non-Closure

No principle in this specification is protected from review.

This includes:

- probe definitions;
- invariants;
- identity semantics;
- evidence rules;
- assessment rules;
- the Non-Closure principle itself.

> اصلِ عدم‌بسته‌شدن، خودش نباید بسته شود.

A future observation may justify revision, replacement, restriction, or rejection of any component of IRG-01.

Any such revision must preserve the historical record of the earlier version.

---

# 14. Failure Interpretation

The following distinctions are mandatory:

`Missing observation ≠ Contradiction`

`Identifier equality ≠ Entity continuity`

`Repeated representation ≠ Independent evidence`

`Documentation ≠ Implementation`

`Implementation ≠ Validation`

`Passing probe ≠ Philosophical proof`

---

# 15. Probe Dependency Structure

The conceptual dependency order is:

`P01 → P02 → P03 → P04 → P05 → INV-P01…P05 → INV-S01…S12 → Cross-Probe Semantic Borrowing Review → Final Baseline Decision`

This ordering describes methodological dependency.

It does not authorize one probe's verdict to become another probe's evidence.

---

# 16. Baseline Integrity Conditions

IRG-01 is considered a specification baseline only when the following are satisfied at the specification level:

1. P01–P05 have explicit objectives.
2. Every probe has explicit scope and limitations.
3. Observable and negative conditions are distinguishable.
4. `NOT_OBSERVED` is distinguishable from `CONTRADICTED`.
5. Raw observations are separated from assessment and verdict.
6. Evidence cannot silently multiply from one underlying observation.
7. Assessment history cannot be silently overwritten.
8. Scope cannot silently expand.
9. Identifier equality cannot silently become continuity proof.
10. Cross-probe semantic borrowing is prohibited.
11. No aggregate IRG-01 verdict exists without an explicit aggregation rule.
12. The same-Claim relation used by P03/P05 cannot be established solely from the identity value under test.
13. The specification itself remains open to future contradiction and revision.

---

# 17. Current Status

`IRG-01 — Version 0.2.1 — Status BASELINE`

- Implementation: NOT IMPLEMENTED
- Runtime Verification: NOT PERFORMED
- Experimental Result: NOT CLAIMED
- Philosophical Proof: NOT CLAIMED

This document defines a probe specification.

It does not report an implementation result.

It does not establish that the requirement has been satisfied.

It defines how the requirement may be examined without assuming the outcome.

---

# 18. Core Epistemic Boundary

IRG-01 follows the broader Ario epistemic chain:

`REALITY → OBSERVATION → EVIDENCE → AUDIT → ASSESSMENT`

The specification therefore preserves the distinction:

`What exists ≠ What was observed ≠ What counts as evidence ≠ What an audit establishes ≠ What may be assessed`

The purpose of IRG-01 is not to prove identity.

Its purpose is to make identity-reference claims **observable, auditable, bounded, and falsifiable**.

---

# 19. Guiding Principle

> Don't fear the outcome. Let the data decide.

A successful probe is not a victory over uncertainty.

A failed probe is not a failure of the project.

Both are observations about the system under examination.

**Unknown stays Unknown.**
