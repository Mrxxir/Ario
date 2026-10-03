# IRG-04 — Retrieval / Cross-System Integrity

**Version:** 0.1.0  
**Status:** BASELINE  
**Implementation:** NOT IMPLEMENTED  
**Runtime Verification:** NOT PERFORMED  
**Experimental Result:** NOT CLAIMED  
**Philosophical Proof:** NOT CLAIMED

## 1. Requirement

> A Claim or lineage-bearing artifact retrieved across a defined system or interface boundary must remain auditable with respect to the source artifact, observable content, and declared transformations, without treating retrieval success as proof of source continuity, semantic identity, or ontological identity.

Persian formulation:

> **یک Claim یا artifact دارای lineage که از یک مرز تعریف‌شده‌ی سیستم یا interface بازیابی می‌شود، باید از نظر artifact مبدأ، محتوای قابل مشاهده و transformationهای اعلام‌شده قابل ممیزی باقی بماند؛ بدون اینکه موفقیت retrieval به‌تنهایی به معنای تداوم منبع، هویت معنایی یا هویت ontological تلقی شود.**

## 2. Why IRG-04 Exists

IRG-01 established stable reference.

IRG-02 established observable historical preservation.

IRG-03 established reconstructable observable lineage.

A remaining failure mode is:

```
SOURCE
  ↓
SYSTEM / INTERFACE BOUNDARY
  ↓
RETRIEVED REPRESENTATION
```

where the retrieved representation is silently altered, detached from its source, misbound to another source, or treated as identical merely because retrieval succeeded.

IRG-04 therefore tests **retrieval integrity**, not entity identity.

The core distinction is:

```
RETRIEVAL SUCCESS
      ≠
SOURCE CONTINUITY
      ≠
SEMANTIC IDENTITY
      ≠
ONTOLOGICAL IDENTITY
```

## 3. Conceptual Separation

IRG-04 distinguishes:

```
SOURCE ARTIFACT
      ≠
TRANSFER / RETRIEVAL EVENT
      ≠
RETRIEVED REPRESENTATION
      ≠
TRANSFORMATION
      ≠
CLAIM IDENTITY
      ≠
ENTITY CONTINUITY
```

A retrieved representation may be:

- an exact representation of the source,
- a transformed representation,
- a partial representation,
- an independently reconstructed representation,
- or an unresolved representation.

The architecture MUST NOT silently collapse these cases.

## 4. Scope

IRG-04 applies where an artifact, Claim, state, or lineage-bearing record crosses a defined boundary such as:

- storage to retrieval layer
- database to API
- local system to external system
- archive to application
- serialization/deserialization boundary
- versioned repository to consumer

The boundary MUST be defined by the inspection context.

IRG-04 does not require that every implementation use a network or distributed system.

## 5. IRG-04.P01 — Retrieval Representation

### Objective

Determine whether the retrieved artifact is explicitly distinguishable from its source and whether the retrieval representation can be identified.

### In Scope

- source artifact reference
- retrieved artifact/reference
- retrieval representation
- retrieval boundary

### Out of Scope

- source truth
- entity continuity
- semantic identity
- causal continuity
- ontological identity

### Observable Condition

A source artifact and its retrieved representation can be distinguished and related through an explicit retrieval event or admissible source binding.

### Negative Condition

A retrieved object is presented without a resolvable source reference or boundary context.

### Admissibility Rules

- Retrieval success MUST NOT by itself establish source identity.
- Matching identifiers MUST NOT by themselves establish source continuity.
- Content similarity MUST NOT by itself establish that the retrieved object is the source artifact.
- A consumer assertion of origin MUST NOT automatically become independent evidence of origin.

### Verdict Rules

- **SUPPORTED:** source, retrieval representation, and retrieval boundary are explicitly distinguishable and related.
- **CONTRADICTED:** admissible evidence establishes that the retrieved representation is bound to an incompatible source.
- **NOT_OBSERVED:** source binding cannot be observed.
- **AMBIGUOUS:** multiple plausible sources or retrieval bindings remain admissible.

### Limitation

P01 establishes representational binding, not source continuity.

## 6. IRG-04.P02 — Retrieval Fidelity

### Objective

Determine whether defined observable properties of the source are preserved across retrieval.

### In Scope

- specified source properties
- retrieved properties
- exact or explicitly defined comparison rules
- detectable loss or alteration

### Out of Scope

- properties outside inspection scope
- hidden source state
- semantic truth not observable in the compared representation
- entity continuity

### Observable Condition

For each property declared in scope, the retrieved representation satisfies the defined fidelity condition.

The fidelity condition MUST be explicit. It MAY require exact equality, canonical equivalence, or another deterministic relation appropriate to the property.

### Negative Condition

An in-scope property is changed, lost, reordered, truncated, corrupted, or otherwise altered beyond the declared admissibility condition.

### Admissibility Rules

- Fidelity MUST be evaluated against a defined source state.
- Equality MUST NOT be assumed merely because a retrieval API reports success.
- Comparison rules MUST be versioned where they affect assessment.
- A transformation that is declared and admissible MUST NOT be misclassified as corruption.
- An undeclared transformation MUST remain distinguishable from an exact retrieval.

### Verdict Rules

- **SUPPORTED:** all required in-scope properties satisfy the declared fidelity condition.
- **CONTRADICTED:** at least one required property violates the declared fidelity condition.
- **NOT_OBSERVED:** the required source or comparison property cannot be observed.
- **AMBIGUOUS:** the comparison cannot distinguish fidelity from an admissible transformation.

### Limitation

P02 evaluates only declared observable properties. Passing P02 does not establish total or hidden-state fidelity.

## 7. IRG-04.P03 — Source Binding and Provenance

### Objective

Determine whether the retrieved representation can be traced to the exact source artifact or source state claimed by the retrieval record.

### In Scope

- source reference
- source version/state
- retrieval event
- provenance
- retrieval timestamp where available

### Out of Scope

- truth of the source content
- completeness of source history
- causal relation
- entity continuity

### Observable Condition

The retrieval record resolves to a specific source artifact or source state within the defined scope.

### Negative Condition

The retrieval record identifies only a generic container, mutable location, or ambiguous identifier from which the exact source state cannot be resolved.

### Admissibility Rules

- A current container reference MUST NOT substitute for the exact historical source state when historical state matters.
- Provenance metadata MUST NOT validate itself.
- Multiple retrieval records from the same underlying source observation MUST NOT become independent evidence merely through repetition.
- A source reference copied into the retrieved artifact MUST NOT by itself prove that the source was actually retrieved.

### Verdict Rules

- **SUPPORTED:** the claimed source artifact/state is resolvable.
- **CONTRADICTED:** admissible evidence establishes that the retrieved representation came from a different source artifact/state than claimed.
- **NOT_OBSERVED:** exact source binding cannot be established.
- **AMBIGUOUS:** multiple source states remain plausible.

### Limitation

P03 establishes provenance of retrieval, not semantic or ontological identity of the retrieved object.

## 8. IRG-04.P04 — Transformation Disclosure

### Objective

Determine whether transformations occurring across the retrieval boundary are explicitly represented and distinguishable from source fidelity.

### In Scope

- serialization/deserialization
- normalization
- canonicalization
- filtering
- redaction
- truncation
- format conversion
- other declared transformations

### Out of Scope

- hidden transformations that leave no observable evidence
- intent behind transformations
- truth of transformed content
- entity continuity

### Observable Condition

Any transformation material to the inspected properties is either:

1. absent and the representation satisfies the exact fidelity rule, or
2. explicitly declared with an auditable transformation definition.

### Negative Condition

A material transformation occurs but the retrieved representation is presented as an unchanged source representation.

### Admissibility Rules

- Declared transformation MUST NOT be silently treated as corruption.
- Undeclared material transformation MUST NOT be silently treated as exact retrieval.
- A transformation label MUST have auditable semantics.
- A downstream system's claim that no transformation occurred MUST NOT be its own sole evidence of absence of transformation.

### Verdict Rules

- **SUPPORTED:** relevant transformations are either absent under the defined fidelity condition or explicitly represented.
- **CONTRADICTED:** a material transformation is concealed or falsely represented as exact retrieval.
- **NOT_OBSERVED:** transformation status cannot be evaluated.
- **AMBIGUOUS:** available evidence cannot distinguish competing transformation explanations.

### Limitation

No observable audit can establish that a completely trace-free hidden transformation never occurred.

## 9. IRG-04.P05 — Cross-System Discrepancy Auditability

### Objective

Determine whether discrepancies between source and retrieved representations remain observable and epistemically distinguishable from source equivalence.

### In Scope

- source/retrieval discrepancies
- version mismatch
- partial retrieval
- corruption indicators
- unresolved source binding
- alternative representations

### Out of Scope

- proving why an undiscoverable discrepancy occurred
- proving absence of hidden discrepancy
- entity continuity
- philosophical identity

### Expected Artifact

```
SOURCE STATE
    │
    │ retrieval
    ↓
RETRIEVED STATE

A ≠ A'
```

where the discrepancy remains explicit.

### Observable Condition

A material discrepancy, when observed, is represented as a discrepancy or unresolved state rather than silently normalized into equivalence.

### Negative Condition

The retrieved representation is treated as source-equivalent despite an observable material discrepancy.

### Admissibility Rules

- Absence of a detected discrepancy MUST NOT prove perfect equality of hidden state.
- A discrepancy MUST NOT be erased merely because retrieval completed successfully.
- A consumer-side normalization MUST NOT silently overwrite the source representation used for comparison.
- Multiple inconsistent retrieved representations MUST remain distinguishable unless an explicit deterministic reconciliation rule exists.

### Verdict Rules

- **SUPPORTED:** observed discrepancies are explicitly preserved as discrepancies or unresolved cases.
- **CONTRADICTED:** an observed material discrepancy is silently represented as source-equivalent.
- **NOT_OBSERVED:** discrepancy handling cannot be evaluated.
- **AMBIGUOUS:** the epistemic status of a discrepancy cannot be resolved.

### Limitation

P05 tests auditability of observed discrepancies, not completeness of discrepancy detection.

## 10. IRG-04 Invariants

### INV-R01 — No Retrieval-by-Success

Successful retrieval MUST NOT by itself establish source continuity.

```
Retrieved Successfully ≠ Same Source
```

### INV-R02 — No Identity-by-Copied-Identifier

A copied or matching identifier MUST NOT by itself establish that the retrieved representation is the original source artifact.

### INV-R03 — No Similarity-by-Fidelity

Content similarity MUST NOT substitute for a defined fidelity condition.

### INV-R04 — Source-State Specificity

Where historical state matters, provenance MUST resolve to the relevant source artifact/state rather than only to a mutable container.

### INV-R05 — Transformation Transparency

Material transformations MUST remain distinguishable from exact retrieval.

### INV-R06 — No Hidden Normalization

A retrieval layer MUST NOT silently normalize an observable discrepancy into apparent equivalence.

### INV-R07 — Retrieval Evidence Independence

Multiple views, API responses, exports, or reports derived from the same retrieval event MUST NOT be counted as independent evidence of retrieval integrity.

### INV-R08 — No Absence Inference

Failure to detect corruption or transformation MUST NOT be interpreted as proof that none existed outside the observable scope.

### INV-R09 — No Cross-System Continuity Inflation

Successful transfer between systems MUST NOT establish entity continuity, semantic identity, causal continuity, or ontological persistence.

### INV-R10 — No Cross-Probe Semantic Borrowing

IRG-01, IRG-02, and IRG-03 evidence MAY be used where independently admissible and within scope, but their verdicts MUST NOT substitute for retrieval-integrity evidence.

## 11. Relationship to Earlier IRGs

IRG-04 does not replace earlier layers.

```
IRG-01 → Can it be stably referenced?
IRG-02 → Was observable history preserved/reconstructable?
IRG-03 → Can observable lineage relations be reconstructed?
IRG-04 → Did the defined retrieval boundary preserve and expose the relevant source representation/provenance?
```

The following inference is prohibited:

```
Retrieval Success
      ↓
Identity
      ↓
History
      ↓
Lineage
      ↓
Same Entity
```

Each arrow requires its own admissible evidence.

## 12. Evidence Independence

The following are not automatically independent:

```
Source
  ↓
Serializer
  ↓
API
  ↓
Client
  ↓
Cache
  ↓
UI
```

If all observations originate from the same underlying source/retrieval event, they remain one evidentiary origin unless independent origin is established.

This inherits the Master Probe invariant:

> One underlying observation cannot become multiple independent evidence items merely through representation.

## 13. Verdict Locality

Every IRG-04 verdict is local to:

```
Source Scope
+
Retrieval Boundary
+
Compared Properties
+
Transformation Rules
+
Provenance
+
Assessment Rules
+
Limitations
```

A retrieval verdict MUST NOT silently become:

- proof of source truth
- proof of complete transfer
- proof of semantic identity
- proof of entity continuity
- proof of causal continuity
- proof of ontological persistence
- philosophical proof

No implicit aggregation of P01–P05 is permitted.

## 14. Master Probe Schema

IRG-04 reuses Master Probe Record Schema v0.2.

No new generic evidence or confidence schema is introduced.

All applicable Master Schema invariants remain in force, including:

- no evidence inflation
- no verdict in raw observation
- no implicit aggregation
- no silent reassessment
- no absence inference
- one field → one semantic meaning
- exact historical provenance
- auditable versions
- representable uncertainty
- no self-supporting evidence cycle
- scope containment
- distinguishable observation origin
- assessment bounded by observable condition
- explicit negative conditions
- deterministic assessment
- no continuity inflation

## 15. Known Limitations

IRG-04 cannot establish properties that are outside the observed retrieval scope.

It cannot prove that an undetectable transformation never occurred.

It cannot convert a partial retrieval into a complete source state.

It cannot establish entity continuity merely because the same representation appears in multiple systems.

It cannot determine hidden causal or ontological relations.

## 16. Explicit Non-Claims

IRG-04 does NOT claim to establish:

- truth of Claims
- complete source preservation
- complete retrieval history
- hidden transformation absence
- causal continuity
- semantic identity beyond the declared comparison scope
- entity continuity
- ontological identity
- consciousness
- personhood
- survival
- persistence of a self
- philosophical identity

## 17. Final Status

```
IRG-04
Version: 0.1.0

Adversarial Review: PASS
Second-Order Adversarial Review: PASS
Self-Validation: PASS
Cross-Probe Integrity with IRG-01 / IRG-02 / IRG-03: PASS

Implementation: NOT IMPLEMENTED
Runtime Verification: NOT PERFORMED
Experimental Result: NOT CLAIMED
Philosophical Proof: NOT CLAIMED

Status:
BASELINE
```

## Core Principle

> Retrieval is an observable boundary event, not a proof of identity.

Therefore:

```
SOURCE
   ↓
RETRIEVAL
   ↓
REPRESENTATION
   ↓
AUDIT
```

must remain distinct from:

```
SOURCE
   ↓
SAME ENTITY
   ↓
SAME SELF
```

The second chain cannot be obtained merely by completing the first.
