# IRG-03 — Lineage Reconstruction

**Version:** 0.2.0  
**Status:** BASELINE  
**Implementation:** NOT IMPLEMENTED  
**Runtime Verification:** NOT PERFORMED  
**Experimental Result:** NOT CLAIMED  
**Philosophical Proof:** NOT CLAIMED

## 1. Requirement

> A Claim's observable lineage must be reconstructable across defined derivation or state-transition relations from admissible evidence, without inferring lineage solely from identity equality, content similarity, temporal proximity, or another artifact's verdict.

Persian formulation:

> **تبار قابل مشاهده‌ی یک Claim باید در طول روابط تعریف‌شده‌ی derivation یا state transition، بر اساس شواهد مجاز قابل بازسازی باشد؛ بدون اینکه lineage صرفاً از برابری شناسه، شباهت محتوا، نزدیکی زمانی، یا verdict یک artifact دیگر استنتاج شود.**

## 2. Relationship to IRG-01 and IRG-02

IRG-01 asks whether a Claim can be stably referenced.

IRG-02 asks whether its observable history can be preserved and reconstructed.

IRG-03 asks whether observable relations connecting states, artifacts, and downstream Claims can be reconstructed.

Therefore:

```
Identity
   ≠
History
   ≠
Lineage
```

and:

- IRG-01 SUPPORTED does not imply IRG-02 SUPPORTED.
- IRG-02 SUPPORTED does not imply IRG-03 SUPPORTED.
- IRG-01 SUPPORTED does not imply IRG-03 SUPPORTED.
- IRG-03 SUPPORTED does not imply entity continuity.

## 3. Conceptual Separation

IRG-03 distinguishes:

```
CLAIM IDENTITY
      ≠
STATE OCCURRENCE
      ≠
STATE CONTENT
      ≠
ARTIFACT
      ≠
LINEAGE RELATION
      ≠
ENTITY CONTINUITY
```

A lineage relation is an observable relation between identifiable source and target artifacts or states. It is not itself a claim about what the underlying entity ultimately is.

An artifact containing a Claim is not automatically the Claim itself. A state transition involving a Claim is not automatically a derivation relation.

## 4. Lineage Relation

A lineage edge is valid only when the relation connecting source and target is supported by admissible evidence.

Possible relation types include, for example:

```
DERIVED_FROM
TRANSFORMED_FROM
RETRIEVED_FROM
REFERENCES
SUPERSEDES
AGGREGATED_FROM
```

IRG-03 does not prescribe a universal relation vocabulary.

An implementation MAY define additional relation types, provided their semantics are explicitly defined and auditable.

An undefined relation label MUST NOT be treated as self-explanatory evidence of lineage.

A relation label also MUST NOT be silently interpreted as causal dependence unless causal evidence is independently within scope.

## 5. IRG-03.P01 — Lineage Representation

### Objective

Determine whether lineage relations are explicitly represented and distinguishable from the artifacts or states they connect.

### In Scope

- lineage relation representation
- identifiable source and target
- relation type
- relation direction

### Out of Scope

- truth of the relation
- completeness of lineage
- causal truth
- entity continuity
- ontological identity

### Expected Artifact

```
Artifact A
   │
   └── DERIVED_FROM
          ↓
Artifact B
```

### Observable Condition

A lineage relation between identifiable source and target can be explicitly observed and its direction determined.

### Negative Condition

Artifacts exist but no distinguishable relation connects them, or relation direction cannot be established.

### Admissibility Rules

- Content similarity MUST NOT establish lineage by itself.
- Temporal proximity MUST NOT establish lineage by itself.
- Shared identity MUST NOT establish derivation by itself.
- A downstream artifact's assertion of lineage MUST NOT automatically establish the asserted relation as independently supported.
- Another Probe's verdict MUST NOT substitute for lineage evidence.

### Verdict Rules

- **SUPPORTED:** a defined lineage relation between identifiable source and target is observed.
- **CONTRADICTED:** admissible evidence establishes that the represented relation is inconsistent with the observed source/target relation.
- **NOT_OBSERVED:** no sufficient lineage relation is observable.
- **AMBIGUOUS:** artifacts appear related, but relation or direction cannot be resolved.

### Limitation

Representation of a lineage relation does not establish that the relation is complete or causally true.

## 6. IRG-03.P02 — Lineage Edge Admissibility

### Objective

Determine whether an individual lineage edge is supported by admissible evidence independent of unsupported semantic assumptions.

### In Scope

- source artifact/state
- target artifact/state
- relation evidence
- relation admissibility

### Out of Scope

- complete graph reconstruction
- global causal explanation
- entity continuity
- ontological claims

### Observable Condition

The source, target, and relation between them are supported by admissible evidence sufficient for the claimed edge.

### Negative Condition

The edge exists only because of content similarity, shared identifiers without defined semantics, timestamp proximity, naming conventions, unsupported model-generated assertion, or another Probe's verdict.

### Admissibility Rules

- Each edge MUST have an identifiable evidentiary basis.
- A relation asserted by an artifact is not automatically independent evidence for that relation.
- Self-referential lineage assertions MUST NOT validate themselves.
- Evidence derived from the target solely through the relation under test MUST NOT be treated as independent support for that relation.
- Multiple representations of one underlying observation MUST NOT become multiple independent edge evidences.

### Verdict Rules

- **SUPPORTED:** the individual lineage edge is admissibly supported.
- **CONTRADICTED:** admissible evidence establishes that the claimed edge is inconsistent with the observed relation.
- **NOT_OBSERVED:** required edge evidence is unavailable.
- **AMBIGUOUS:** evidence exists but does not distinguish the claimed edge from plausible alternatives.

### Limitation

A supported edge does not establish neighboring edges.

## 7. IRG-03.P03 — Lineage Reconstruction

### Objective

Determine whether a requested lineage path or subgraph can be reconstructed from individually admissible lineage relations.

### In Scope

- multi-edge lineage reconstruction
- path reconstruction
- branching lineage
- convergent lineage
- unresolved gaps

### Out of Scope

- complete lineage
- hidden or erased relations
- entity continuity
- semantic identity
- causal completeness
- ontological identity

### Expected Artifacts

Linear:

```
A → B → C
```

Branching:

```
       B
      ↗
A ────
      ↘
       C
```

Convergent:

```
A → B → D
 \→ C → D
```

### Observable Condition

Every required edge in the reconstructed lineage is individually supported by admissible evidence and the resulting graph preserves the observed relation structure.

### Negative Condition

Reconstruction requires invented edges, interpolated artifacts, unsupported ordering, collapsing distinct branches, or treating similarity/identity/temporal proximity as derivation.

### Admissibility Rules

1. A multi-edge lineage MUST be composed from individually admissible relations.
2. Unsupported intermediate nodes MUST NOT be invented.
3. Missing edges MUST remain unresolved.
4. Branches MUST NOT be silently collapsed.
5. Convergence MUST NOT be interpreted as proof that preceding branches were identical.
6. A path MUST NOT inherit validity merely because its endpoints are related.
7. Identity persistence MUST NOT substitute for lineage evidence.
8. Historical ordering MUST NOT substitute for derivation evidence.
9. IRG-02 reconstruction MUST NOT automatically become IRG-03 lineage evidence.
10. If multiple lineage structures remain admissible, the reconstruction MUST preserve the unresolved alternatives rather than selecting one without evidence.

### Verdict Rules

- **SUPPORTED:** the requested lineage path/subgraph is reconstructable from admissible edges.
- **CONTRADICTED:** at least one required relation is contradicted by admissible evidence.
- **NOT_OBSERVED:** required lineage evidence is unavailable.
- **AMBIGUOUS:** one or more required relations cannot be resolved without unsupported assumptions.

### Limitation

A reconstructable lineage subgraph is not necessarily complete lineage.

## 8. IRG-03.P04 — Lineage Provenance

### Objective

Determine whether each lineage relation used in reconstruction has resolvable provenance to the observation or artifact from which that relation was established.

### In Scope

- provenance of lineage edges
- relation evidence
- source artifact state
- observation origin

### Out of Scope

- truth of the source
- completeness of lineage
- causal completeness
- entity continuity

### Observable Condition

Each lineage edge used in a reconstruction can be traced to admissible evidence with resolvable provenance.

### Negative Condition

A lineage edge is asserted but its evidentiary origin cannot be resolved.

### Admissibility Rules

- Provenance metadata MUST NOT validate itself.
- One underlying observation MUST NOT become multiple independent lineage evidences through representation.
- A derived report cannot automatically become independent evidence for every relation it describes.
- Provenance MUST resolve to the relevant artifact/source state rather than merely to a current container.
- A provenance chain MUST NOT be considered independent merely because it contains multiple derived layers.

### Verdict Rules

- **SUPPORTED:** required lineage provenance is resolvable.
- **CONTRADICTED:** admissible evidence establishes provenance inconsistency.
- **NOT_OBSERVED:** required provenance cannot be observed.
- **AMBIGUOUS:** provenance exists but its relation to the claimed edge is unresolved.

### Limitation

Provenance establishes evidentiary origin, not truth of the lineage relation.

## 9. IRG-03.P05 — Lineage Gap / False-Link Auditability

### Objective

Determine whether unresolved or contradicted lineage relations remain distinguishable from supported lineage rather than being silently filled by the system.

### In Scope

- missing lineage edges
- unresolved relations
- contradicted relations
- explicit gaps
- alternative lineage candidates

### Out of Scope

- proving that an unobserved edge never existed
- proving hidden causal relations
- completeness of lineage

### Expected Artifact

```
A ───→ B
       │
       ?
       ↓
       C
```

The unresolved edge remains unresolved.

### Observable Condition

The system distinguishes supported lineage from unresolved or contradicted lineage rather than silently converting gaps into valid edges.

### Negative Condition

An unsupported edge is presented as established lineage without admissible evidence.

### Admissibility Rules

- Absence of an edge MUST NOT prove that no edge existed.
- An unresolved edge MUST NOT be silently treated as supported.
- A model-generated reconstruction MUST NOT be treated as observed lineage without independent evidence.
- Current graph structure MUST NOT prove historical completeness.
- A guessed edge MUST remain distinguishable from an observed edge.

### Verdict Rules

- **SUPPORTED:** unresolved or contradicted lineage is explicitly distinguishable from supported lineage.
- **CONTRADICTED:** admissible evidence shows unsupported lineage is presented as established.
- **NOT_OBSERVED:** no sufficient evidence exists to evaluate gap handling.
- **AMBIGUOUS:** a relation is exposed but its epistemic status cannot be determined.

### Limitation

P05 detects auditability of observable lineage gaps; it cannot reveal perfectly hidden relations.

## 10. IRG-03 Invariants

### INV-L01 — No Lineage by Similarity

Content similarity MUST NOT, by itself, establish lineage.

```
Similar Content ≠ Derived From
```

### INV-L02 — No Lineage by Identity

Identity equality MUST NOT, by itself, establish a lineage relation.

```
Same Identity ≠ Derived From
```

### INV-L03 — No Lineage by Temporal Proximity

Temporal adjacency MUST NOT, by itself, establish derivation or causation.

```
A before B ≠ A caused B
```

### INV-L04 — Edge Independence

Every lineage edge used in reconstruction MUST have an admissible evidentiary basis.

A supported path cannot manufacture unsupported intermediate edges.

### INV-L05 — No Gap Interpolation

Missing lineage relations MUST remain unresolved unless independently established.

### INV-L06 — No Branch Collapse

Distinct admissible lineage branches MUST NOT be silently collapsed into a single lineage.

### INV-L07 — No Endpoint Inference

A relation between endpoints MUST NOT establish unsupported intermediate lineage.

```
A → C
```

does not establish:

```
A → B → C
```

unless B and both relations are independently supported.

### INV-L08 — No Completeness Inflation

A reconstructed lineage subgraph MUST NOT be interpreted as complete lineage unless completeness is separately established.

### INV-L09 — No Causality Inflation

A lineage relation MUST NOT automatically be interpreted as proof of physical, semantic, intentional, or causal dependence.

### INV-L10 — No Cross-Probe Semantic Borrowing

IRG-01 identity evidence and IRG-02 historical evidence MAY be relevant to lineage inspection where independently admissible, but neither Probe's verdict automatically establishes an IRG-03 lineage relation.

## 11. Evidence Independence

The following does not automatically constitute independent lineage evidence:

```
Source
 ↓
JSON
 ↓
Database View
 ↓
API Response
 ↓
Report
```

If all derive from one underlying observation, they remain one evidentiary origin unless independent origin can be established.

This inherits the Master Probe architecture's No Evidence Inflation invariant.

## 12. Cross-IRG Integrity

The following chain is explicitly prohibited:

```
Stable Identity
      ↓
Preserved History
      ↓
Reconstructed Lineage
      ↓
Same Entity
```

The first three may be individually supported while the fourth remains UNKNOWN.

Likewise:

```
Identity + History + Lineage
```

does not establish:

```
Self
Consciousness
Personhood
Ontological Persistence
```

## 13. Verdict Locality

Every IRG-03 verdict is local to:

```
Probe Objective
+
Inspection Scope
+
Requested Lineage Relation
+
Admissible Evidence
+
Assessment Rules
+
Verdict Basis
+
Limitations
```

A lineage verdict MUST NOT silently become:

- a global system lineage claim
- a completeness claim
- a causal proof
- an entity-continuity claim
- an ontological claim
- a philosophical proof

No implicit aggregation of P01–P05 is permitted.

## 14. Master Probe Schema

IRG-03 reuses Master Probe Record Schema v0.2 from IRG-01.

No separate IRG-03 evidence schema is introduced.

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

IRG-03 cannot establish lineage relations that leave no observable evidence.

It cannot distinguish a genuinely absent relation from a relation whose evidence has been completely erased.

It cannot transform incomplete evidence into complete lineage.

It cannot determine hidden causal structure merely from representational lineage.

These limitations MUST remain explicit rather than being compensated for by stronger language.

## 16. Explicit Non-Claims

IRG-03 does NOT claim to establish:

- truth of Claims
- completeness of lineage
- hidden causal history
- intentionality
- entity continuity
- semantic identity
- ontological identity
- consciousness
- personhood
- survival
- persistence of a self
- philosophical identity

## 17. Final Status

```
IRG-03
Version: 0.2.0

Adversarial Review: PASS
Second-Order Adversarial Review: PASS
Self-Validation: PASS
IRG-01 ↔ IRG-02 ↔ IRG-03 Cross-Probe Integrity: PASS

Implementation: NOT IMPLEMENTED
Runtime Verification: NOT PERFORMED
Experimental Result: NOT CLAIMED
Philosophical Proof: NOT CLAIMED

Status:
BASELINE
```

## Core Principle

> A lineage is not a story inferred from resemblance. It is a set of observable relations whose evidentiary basis, direction, provenance, and unresolved gaps remain auditable.

Therefore:

```
IDENTITY
    ↓
HISTORY
    ↓
LINEAGE
```

must remain three separately auditable layers.

And:

```
LINEAGE
    ≠
ENTITY
    ≠
SELF
    ≠
ONTOLOGY
```
