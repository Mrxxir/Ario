# IRG-02 — Historical / Temporal Integrity

**Version:** 0.2.0  
**Status:** BASELINE  
**Implementation:** NOT IMPLEMENTED  
**Runtime Verification:** NOT PERFORMED  
**Experimental Result:** NOT CLAIMED  
**Philosophical Proof:** NOT CLAIMED

## 1. Requirement

> A Claim's observable history must remain reconstructable across defined state transitions without silent historical replacement, while preserving the distinction between historical continuity and entity, semantic, causal, or ontological continuity.

IRG-02 asks whether the observable history of a Claim can be preserved and reconstructed. It does not infer entity continuity from historical persistence.

## 2. Relationship to IRG-01

IRG-01 asks whether a Claim can be stably referenced. IRG-02 asks whether its observable history can be preserved and reconstructed.

IRG-01 and IRG-02 are independent:

- IRG-01 SUPPORTED does not imply IRG-02 SUPPORTED.
- IRG-02 SUPPORTED does not imply IRG-01 SUPPORTED.
- Same Identity != Preserved History.
- Preserved History != Same Entity.
- Historical Continuity != Entity Continuity.
- Historical Continuity != Semantic Continuity.
- Historical Continuity != Causal Continuity.
- Historical Continuity != Ontological Identity.

## 3. Conceptual Separation

```
HISTORICAL EXISTENCE
        ↓
PRESERVATION
        ↓
ORDERABILITY
        ↓
RECONSTRUCTABILITY
        ↓
COMPLETENESS
```

These properties MUST NOT be collapsed.

Preserving A and B does not establish A → B. Reconstructing A → B → C does not establish that the reconstruction is complete. Historical reconstructability does not establish entity, semantic, causal, or ontological continuity.

## 4. State Occurrence vs State Content

```
Claim Identity
      ≠
State Occurrence
      ≠
State Content
```

Identical content MUST NOT automatically imply identical historical occurrence. For example, A → B → A may contain two distinct occurrences of content A.

IRG-02 does not mandate a particular implementation mechanism such as state_occurrence_id, content hashes, logical clocks, vector clocks, or predecessor pointers. The requirement is that distinct historical occurrences remain distinguishable through admissible observable relations.

## 5. Master Probe Schema

IRG-02 reuses Master Probe Record Schema v0.2 from IRG-01. No separate evidence schema is introduced.

The Master Schema invariants remain applicable, including no evidence inflation, no verdict in raw observation, no implicit aggregation, no silent reassessment, no absence inference, one field → one semantic meaning, exact historical provenance, auditable versions, representable uncertainty, no self-supporting evidence cycle, scope containment, distinguishable observation origin, assessment bounded by observable condition, explicit negative conditions, deterministic assessment, and no continuity inflation.

## 6. Inspection Scope

Historical conclusions are valid only within the explicitly examined scope.

Where applicable, inspection scope identifies the target Claim, temporal boundary, retention boundary, artifacts examined, and the basis for any material scope boundary.

A retention boundary MUST NOT be treated as valid merely because the inspected system declares it. Where a retention or temporal boundary materially affects a conclusion, its basis MUST be supported by admissible, provenance-resolvable evidence or artifact reference.

A self-declared or retroactively created scope boundary MUST NOT establish its own validity.

## 7. IRG-02.P01 — Historical Representation

### Objective

Determine whether historical states of a Claim are explicitly represented as discrete and distinguishable historical artifacts or records.

### In Scope

Historical state representation, distinguishability of historical states, multiple observed states, and the relation between Claim and historical states.

### Out of Scope

Claim truth, historical completeness, historical causal explanation, entity continuity, semantic continuity, ontological identity, and global durability.

### Expected Artifact

```
Claim C123

t1 → State A
t2 → State B
t3 → State C
```

### Observable Condition

Historical states can be identified and distinguished within the inspected scope.

### Negative Condition

Historical representation is absent, indistinguishable, or presented only as a current state without independently observable historical differentiation.

### Admissibility Rules

- Current state alone MUST NOT establish historical representation.
- Identical content MUST NOT automatically establish identical historical occurrence.
- Identity equality MUST NOT by itself establish historical relation.
- Observations MUST remain distinguishable from assessments derived from them.

### Verdict Rules

- **SUPPORTED:** required historical representation is observed within scope.
- **CONTRADICTED:** admissible evidence establishes required historical representation is explicitly replaced or destroyed within scope.
- **NOT_OBSERVED:** required representation cannot be observed.
- **AMBIGUOUS:** artifacts exist but their historical-state relation cannot be resolved.

### Limitation

Multiple represented states do not establish completeness.

## 8. IRG-02.P02 — Historical Preservation

### Objective

Determine whether creation or recording of a subsequent state preserves previously observable historical states from unrecorded replacement or destruction within scope.

### In Scope

State transitions, persistence of prior state, preservation after subsequent state creation, and observable replacement/destruction.

### Out of Scope

Eternal durability, completeness, Claim truth, entity continuity, semantic continuity, causal continuity, and ontological identity.

### Expected Artifact

```
t1:
C123 → A

transition

t2:
C123 → B

A remains historically resolvable
B is additionally observable
```

### Observable Condition

The prior state remains historically resolvable after a subsequent state is recorded, within the declared and independently supportable scope.

### Negative Condition

A previously observable state becomes unresolvable through an unrecorded replacement or destruction within scope.

### Admissibility Rules

- Current state alone MUST NOT establish preservation.
- Absence of an old state MUST NOT by itself establish that overwrite occurred.
- Retention boundaries are scope constraints only when their basis is admissibly established.
- A legitimate, explicitly recorded revision or supersession is not by itself a silent replacement.

### Verdict Rules

- **SUPPORTED:** prior state remains resolvable after transition.
- **CONTRADICTED:** admissible evidence establishes unrecorded replacement or destruction.
- **NOT_OBSERVED:** required before/after or preservation evidence is unavailable.
- **AMBIGUOUS:** historical state is unavailable but cause cannot be resolved.

### Limitation

Observable preservation does not establish indefinite durability or complete retention.

## 9. IRG-02.P03 — Historical Ordering & Reconstruction

### Objective

Determine whether observed historical states and their relations can be reconstructed within scope using an explicit, admissible, provenance-resolvable ordering or causal basis.

### In Scope

Historical ordering, temporal relation, causal/dependency relation, reconstruction, branching or convergent structures, and ordering uncertainty.

### Out of Scope

Complete history, truth of historical content, canonicality of a branch without independent evidence, entity continuity, semantic continuity, causal explanation beyond observed relations, and ontological identity.

### Expected Artifact

Linear:

```
A → B → C
```

Branching:

```
       B
      /
A ---<
      \
       C
```

Convergent:

```
A → B → D
 \→ C → D
```

### Ordering Basis

The ordering basis MUST be explicitly identifiable, admissible within scope, provenance-resolvable, and sufficient for the specific reconstruction claimed.

IRG-02 does NOT mandate physical timestamps, logical clocks, vector clocks, sequence numbers, predecessor pointers, or another particular mechanism.

Physical timestamps MAY be admissible where their provenance and scope support their use. Conflicting ordering evidence MUST NOT be silently resolved by assumption.

### Observable Condition

The relevant historical states and their ordering or relation can be reconstructed from admissible historical evidence without interpolation or forced linearization.

### Negative Condition

Required historical relations cannot be reconstructed, or reconstruction would require inventing missing states, silently collapsing branches, or assuming unsupported order.

### Admissibility Rules

1. Reconstruction MUST use historical evidence.
2. Current state MUST NOT substitute for historical evidence.
3. Missing states MUST NOT be silently interpolated.
4. Divergent branches MUST NOT be silently collapsed.
5. A system label such as canonical MUST NOT establish historical validity by itself.
6. Incomparable observations MUST remain incomparable unless admissible evidence establishes an ordering.
7. Conflicting ordering evidence MUST produce unresolved assessment rather than arbitrary selection.
8. Same-Claim relation MUST NOT be established solely through the identity property under evaluation.
9. One Probe's verdict MUST NOT automatically become semantic evidence for another Probe.

### Verdict Rules

- **SUPPORTED:** claimed historical relation/order is reconstructable from admissible evidence.
- **CONTRADICTED:** admissible evidence directly conflicts with the required reconstruction.
- **NOT_OBSERVED:** insufficient historical evidence exists.
- **AMBIGUOUS:** evidence exists but ordering, branching, convergence, or relation cannot be resolved without unsupported assumptions.

### Limitation

Successful reconstruction applies only to observed and examined history and does not establish completeness.

## 10. IRG-02.P04 — Historical Provenance

### Objective

Determine whether each historical state used in reconstruction has resolvable provenance to the artifact, observation, or source state from which it was observed.

### In Scope

Historical-state provenance, source/artifact resolution, historical observation origin, and provenance integrity.

### Out of Scope

Source truth, Claim correctness, completeness, entity continuity, semantic continuity, and ontological identity.

### Expected Artifact

```
Historical State B
      ↓
Observation ID
      ↓
Source Reference
      ↓
Exact artifact/source state
```

### Observable Condition

Historical state resolves through admissible provenance to the relevant observed source or artifact state.

### Negative Condition

A historical state is presented as historical but its provenance is unresolvable or demonstrably altered without recorded historical basis.

### Admissibility Rules

- Provenance MUST NOT be established solely by circular reference to the historical chain it is intended to validate.
- Provenance metadata is not itself proof of truth.
- Multiple representations of one underlying source MUST NOT automatically become independent evidence.
- Another Probe's verdict MUST NOT be borrowed as provenance evidence without an independently admissible relation.

### Verdict Rules

- **SUPPORTED:** provenance is resolvable within scope.
- **CONTRADICTED:** admissible evidence establishes provenance inconsistency or unrecorded replacement.
- **NOT_OBSERVED:** required provenance artifacts are unavailable.
- **AMBIGUOUS:** provenance exists but its relation to the historical state cannot be resolved.

### Limitation

Provenance establishes source relation, not truth or ontological continuity.

## 11. IRG-02.P05 — Historical Replacement Auditability

### Objective

Determine whether observable historical replacements, overwrites, corrections, or supersessions are recorded in an auditable manner rather than executed as silent historical erasures.

### In Scope

Observed historical replacement, supersession, correction, overwrite, and auditability of transition.

### Out of Scope

Detection of perfectly trace-free deletion, truth of either state, entity legitimacy, semantic continuity, causal continuity, and ontological identity.

### Expected Artifact

```
A
 ↓
superseded_by
 ↓
B
```

or an equivalent auditable historical relation.

### Observable Condition

Where replacement or supersession is observable, the transition is represented so that the relation between prior and subsequent states remains auditable.

### Negative Condition

Admissible evidence shows a previously observable state was replaced or altered without a recorded historical transition within scope.

### Critical Limitation

A perfectly trace-free deletion cannot be established merely because the resulting history is incomplete.

```
No trace of deletion
≠
Proof that deletion occurred

No trace of deletion
≠
Proof that no deletion occurred
```

### Verdict Rules

- **SUPPORTED:** observed replacement/supersession has an auditable transition.
- **CONTRADICTED:** observable replacement lacks the required historical transition record.
- **NOT_OBSERVED:** insufficient evidence exists to evaluate replacement or its recording.
- **AMBIGUOUS:** a change is observable but its mechanism cannot be resolved.

### Limitation

P05 evaluates auditability of observable replacement; it does not provide epistemic access to perfectly erased history.

## 12. IRG-02 Invariants

### INV-T01 — No Silent Historical Replacement

A previously observable historical state MUST NOT become unresolvable through an unrecorded replacement within the examined scope.

This does not establish that an unobservable deletion did or did not occur.

### INV-T02 — Current State ≠ Historical Record

Current state MUST NOT be treated as evidence of prior historical states unless those states are independently observable.

### INV-T03 — Reconstruction Requires Historical Evidence

Historical reconstruction MUST be based on admissible historical observations. Missing states MUST NOT be silently interpolated or gap-filled.

### INV-T04 — Provenance Preservation

Historical records used for reconstruction MUST retain resolvable provenance to the source observation, artifact, or source state from which they were observed.

### INV-T05 — No Continuity Inflation

Historical persistence or reconstructability MUST NOT, by itself, be interpreted as proof of entity continuity, semantic continuity, causal continuity, or ontological identity.

### INV-T06 — No Completeness Inflation

Successful reconstruction of observed history MUST NOT be interpreted as proof that the reconstructed history is complete.

## 13. Retention Boundary Principle

Retention is an inspection-scope boundary, not an epistemic exemption.

An independently established retention boundary may define what is evaluated; it does not establish that history outside the boundary never existed or that deletion was legitimate.

A self-declared or retroactively created retention policy MUST NOT establish its own validity.

Where a material retention boundary cannot be independently grounded in admissible evidence, the affected scope conclusion remains unresolved and MUST NOT be upgraded merely because the system asserts a policy.

## 14. Fork and Branching Principle

IRG-02 does not assume history is necessarily linear.

Where admissible evidence establishes:

```
A → B
A → C
```

the reconstruction MUST preserve the observed branching relation rather than silently selecting one branch.

Where branches converge, the observed structure MAY be represented as a DAG.

IRG-02 does not determine which branch is ontologically or administratively real unless that question is independently within scope and supported by admissible evidence.

Fork handling belongs to P03 and is not a separate invariant.

## 15. Ordering Principle

IRG-02 does not prescribe a universal temporal mechanism.

An ordering basis may include timestamp, sequence relation, causal dependency, logical ordering, or another explicitly defined historical relation.

The basis MUST be explicit, admissible, provenance-resolvable, and sufficient for the specific reconstruction claim.

If independent admissible ordering evidence conflicts, AMBIGUOUS is preferable to unsupported selection.

## 16. Cross-Probe Independence

IRG-02 MUST NOT borrow semantic validity from IRG-01.

Identity persistence does not establish historical preservation. Historical reconstruction does not establish identity persistence.

The same underlying observation MAY be relevant to multiple Probes, but MUST NOT be counted as multiple independent evidence items merely because it is represented or analyzed in multiple ways.

## 17. Same-Claim Constraint

Whenever a Probe requires establishing that observations at different times concern the same Claim, that relation MUST be supported by admissible evidence independent of the identity property currently under evaluation.

Therefore, same identity MUST NOT be the sole proof of same historical Claim when identity persistence itself is under evaluation.

## 18. Verdict Locality

Every IRG-02 verdict is local to:

```
Probe Objective
+
Inspection Scope
+
Observable Condition
+
Admissible Evidence
+
Assessment Rules
+
Verdict Basis
+
Limitations
```

A Probe verdict MUST NOT silently become a global system verdict, completeness claim, entity-continuity claim, ontological claim, or philosophical proof.

No implicit aggregation of P01–P05 is permitted.

## 19. Evidence Independence

The following does not automatically constitute independent evidence:

```
same source
→ JSON representation
→ HTML representation
→ UI representation
→ exported report
```

Multiple representations of one underlying observation remain one evidentiary origin unless independent origin can be established.

This inherits INV-P01 — No Evidence Inflation from the Master Probe Record architecture.

## 20. Known Limitations

IRG-02 cannot directly establish the existence of a historical state that has been perfectly erased together with every trace of its existence.

IRG-02 cannot collapse genuinely unresolved asynchronous forks into a single historical path without additional admissible evidence.

These are epistemic limitations, not failures to be hidden by stronger verdict language.

## 21. Explicit Non-Claims

IRG-02 does NOT claim to establish:

- truth of Claims
- completeness of history
- eternal persistence
- absence of deletion
- entity continuity
- semantic continuity
- causal continuity
- ontological identity
- consciousness
- personhood
- survival
- persistence of a self
- philosophical identity

## 22. Final Status

```
IRG-02
Version: 0.2.0

Adversarial Review: PASS
Second-Order Adversarial Review: PASS
Self-Validation: PASS
IRG-01 ↔ IRG-02 Cross-Probe Integrity: PASS

Implementation: NOT IMPLEMENTED
Runtime Verification: NOT PERFORMED
Experimental Result: NOT CLAIMED
Philosophical Proof: NOT CLAIMED

Status:
BASELINE
```

## Core Principle

> Preserved history is evidence about observable history. It is not, by itself, evidence of what the entity was, whether the entity remained the same, whether the history is complete, or whether the underlying reality continued unchanged.

Therefore:

```
HISTORY
    ↓
OBSERVATION
    ↓
EVIDENCE
    ↓
AUDIT
    ↓
ASSESSMENT
```

must remain distinct from:

```
HISTORY
    ↓
ENTITY
    ↓
SELF
    ↓
ONTOLOGY
```

The second chain cannot be inferred from the first merely because the historical record is persistent or reconstructable.
