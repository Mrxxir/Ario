# Ario — Implementation Readiness Contract v1

## 1. Purpose

This document translates the frozen architecture into an implementation contract without claiming that any requirement is already implemented.

It is the boundary between specification and executable work.

The contract is intentionally narrower than the full architecture: implementation begins with auditable structural behavior, not philosophical identity claims.

## 2. Governing Rule

> An architectural requirement is not implemented until its required observable behavior can be produced, inspected, tested, and reproduced.

The implementation contract must preserve:

- `UNKNOWN` as a valid epistemic state;
- historical preservation without silent replacement;
- identity, history, lineage, retrieval, and assessment as distinct properties;
- deterministic structural auditing separate from generative interpretation;
- provenance and evidence independence;
- explicit failure states;
- versioned rules and schemas;
- no continuity, truth, or ontology inflation.

## 3. Implementation Boundary

### In scope for the first implementation milestone

- Claim identity representation;
- immutable historical representation;
- explicit lineage edges;
- source/retrieval/transformation representation;
- assessment-to-evidence binding;
- deterministic invariant validation;
- provenance and version metadata;
- negative/failure conditions;
- reproducible test fixtures.

### Out of scope for the first milestone

- consciousness detection;
- phenomenology detection;
- ontological identity classification;
- autonomous self-authorization;
- universal identity inference;
- unrestricted natural-language semantic validation;
- claims that the implementation proves the architecture.

## 4. Required Component Separation

The first implementation should maintain these logical boundaries:

```text
RAW ARTIFACTS
    ↓
STRUCTURED RECORDS
    ↓
DETERMINISTIC AUDIT
    ↓
ADMISSIBLE EVIDENCE
    ↓
ASSESSMENT
    ↓
OPTIONAL LLM INTERPRETATION
```

The LLM must not be the sole authority for deterministic structural invariants.

## 5. IRG Implementation Contract

### IRG-01 — Identity

Implementation MUST support:

- stable Claim identifier;
- explicit identity creation event;
- retrieval by identifier;
- referable identity across defined state transitions;
- lineage/reference records that do not derive continuity merely from identifier equality.

Minimum negative tests:

- duplicate identifier creation;
- missing identifier;
- identity reused for unrelated content;
- identity equality presented as continuity evidence.

Acceptance condition:

> The implementation can distinguish identity reference from entity/semantic/causal/ontological continuity.

### IRG-02 — History

Implementation MUST support:

- append-oriented historical records;
- explicit event/state ordering;
- historical provenance;
- reconstruction from recorded transitions;
- auditability of replacement or correction;
- preservation of earlier records after revision.

Minimum negative tests:

- destructive overwrite;
- deleted historical event with no trace;
- reordered events;
- incomplete history presented as complete;
- history preservation presented as entity continuity.

Acceptance condition:

> A revised state can be produced without silently replacing the historical state.

### IRG-03 — Lineage

Implementation MUST support:

- explicit lineage edges;
- edge provenance;
- admissibility checks;
- unresolved lineage gaps;
- branch preservation;
- rejection of lineage inferred solely from identity, similarity, temporal proximity, or endpoint equality.

Minimum negative tests:

- identity-only lineage;
- similarity-only lineage;
- temporal-proximity lineage;
- missing intermediate edge;
- branch collapse;
- causal conclusion from lineage alone.

Acceptance condition:

> A lineage relation is represented as an auditable relation rather than an inferred consequence of artifact similarity.

### IRG-04 — Retrieval

Implementation MUST preserve:

- source artifact identity;
- retrieval event identity;
- retrieved representation;
- declared transformation;
- source binding/provenance;
- discrepancy state;
- temporal/state context where applicable.

Minimum negative tests:

- silent transformation;
- truncated representation treated as identical;
- retrieval success treated as source continuity;
- missing source binding;
- unresolved discrepancy silently accepted.

Acceptance condition:

> Retrieval can be audited without silently converting transfer success into semantic or entity continuity.

### IRG-05 — Assessment

Implementation MUST support:

- explicit assessment object;
- explicit declared evidence references;
- evidence admissibility checks;
- structural scope checks;
- counterevidence visibility;
- assessment version and rule version;
- separation of assessment from evidence.

Minimum negative tests:

- verdict used as evidence;
- identity used as support;
- lineage used as support without admissibility;
- evidence outside declared scope;
- counterevidence silently omitted;
- assessment rewritten without version history.

Acceptance condition:

> An assessment exposes what evidence it declares as input without becoming proof of the Claim itself.

## 6. Cross-IRG Composition Contract

Cross-IRG behavior MUST NOT be implemented as an implicit final score or global truth classifier.

Any composition mechanism MUST explicitly record:

- participating IRGs/probes;
- versions of their rules;
- input verdicts/assessments;
- temporal/state context;
- composition rule identifier;
- derived artifact identity;
- derived semantic status;
- limitations and unresolved inputs.

Required negative tests:

- all local probes PASS → global truth;
- all local probes PASS → same entity;
- local verdicts → evidence;
- score → ontology;
- shared provenance → same state;
- temporally distinct inputs → silently unified state;
- self-authored composition → self-authorization.

Acceptance condition:

> A composed artifact cannot silently acquire stronger epistemic status than its admissible inputs and explicit composition rule justify.

## 7. Temporal Contract

Any state-bearing composition MUST preserve, where applicable:

- execution epoch or temporal scope;
- state/snapshot/event identity;
- relation between distinct states/events;
- temporal compatibility status.

Supported statuses:

- `TEMPORALLY_ALIGNED`;
- `TEMPORALLY_DISTINCT`;
- `TEMPORALLY_UNRESOLVED`.

Temporal overlap is not required.

Required negative test:

> T1 and T2 records share an identifier but lack a defined transition relation; the implementation MUST NOT represent them as one state.

## 8. Provenance and Independence Contract

Every observation/evidence object used by the first milestone MUST be traceable to its source or declared derivation.

Where independence is relevant, the implementation MUST distinguish:

- `INDEPENDENT`;
- `DEPENDENT`;
- `UNKNOWN`.

Repeated representations of one underlying observation MUST NOT automatically become multiple independent evidence items.

## 9. Deterministic Audit Contract

The deterministic audit layer MUST:

- consume explicit structured inputs;
- use versioned rules;
- produce reproducible results for identical inputs and versions;
- expose failure reasons;
- preserve `UNKNOWN` or unresolved states where evidence is insufficient;
- never mutate historical inputs;
- never use its own verdict as evidence for the same verdict.

Minimum audit outputs should identify:

- inspector/version;
- execution timestamp or epoch;
- configuration identifier;
- artifacts examined;
- rule versions;
- observed violations;
- resulting bounded verdict.

## 10. Failure Contract

Failure MUST be observable.

At minimum, the implementation must distinguish conditions such as:

- `SCHEMA_MISMATCH`;
- `MISSING_PROVENANCE`;
- `IDENTITY_CONFLICT`;
- `LINEAGE_GAP`;
- `RETRIEVAL_DISCREPANCY`;
- `TEMPORALLY_UNRESOLVED`;
- `EVIDENCE_INADMISSIBLE`;
- `COMPOSITION_FORBIDDEN`;
- `UNKNOWN`.

A failure MUST NOT silently become a successful or more certain result.

## 11. Reproducibility Contract

Every implementation test used as acceptance evidence SHOULD record:

- implementation version/commit;
- schema version;
- rule version;
- inspector version;
- model/configuration when applicable;
- exact fixture/input;
- expected condition;
- observed output;
- execution timestamp;
- artifact hashes or equivalent stable references where applicable.

Same inputs + same versioned deterministic rules MUST produce the same deterministic assessment.

## 12. Test Strategy

Implementation begins with fixtures, not production-scale optimization.

Each requirement should have:

1. one minimal positive fixture;
2. one direct negative fixture;
3. one boundary/ambiguous fixture;
4. one provenance/independence fixture where relevant;
5. one regression fixture after the first defect is discovered.

Tests are evidence about implementation behavior.

Test PASS does not establish architectural truth.

## 13. First Milestone — Structural Core

The first executable milestone is:

**M0 — Auditable Structural Core**

M0 is complete only when the implementation can:

1. create and persist a Claim identity;
2. append a historical state without mutating the prior state;
3. represent an explicit lineage edge;
4. represent source/retrieval/transformation boundaries;
5. bind an assessment to declared evidence;
6. run deterministic invariant checks;
7. expose failure reasons;
8. preserve unresolved states;
9. reproduce deterministic assessments from fixed fixtures;
10. preserve all relevant provenance/version metadata.

M0 does NOT include an LLM-based semantic judge.

## 14. Change Discipline

Implementation changes follow:

```text
INSPECT
  ↓
PRESERVE
  ↓
CHANGE ONE THING
  ↓
COMPILE
  ↓
TEST
  ↓
AUDIT
  ↓
RECORD
  ↓
ACCEPT / REJECT
```

A failed patch must leave the previous working implementation recoverable.

Historical artifacts must not be rewritten to make a test pass.

## 15. Implementation Status

| Item | Status |
|---|---|
| Architecture | FROZEN WITH EXPLICIT LIMITATIONS |
| IRG-01 implementation | NOT STARTED |
| IRG-02 implementation | NOT STARTED |
| IRG-03 implementation | NOT STARTED |
| IRG-04 implementation | NOT STARTED |
| IRG-05 implementation | NOT STARTED |
| Cross-IRG implementation | NOT STARTED |
| M0 Structural Core | NOT STARTED |
| Runtime Verification | NOT PERFORMED |
| Experimental Result | NOT CLAIMED |

## 16. Boundary to Future Experiments

Once M0 passes its deterministic acceptance suite, the next stage is controlled adversarial experimentation.

The first experimental questions should be implementation-facing:

- Can historical mutation be detected?
- Can provenance loss be detected?
- Can lineage gaps remain unresolved?
- Can retrieval transformations be surfaced?
- Can inadmissible evidence be rejected?
- Can temporal chimeras be prevented?
- Can local PASS results be prevented from becoming global truth?

Only after these structural behaviors are observed should broader behavioral or self-model experiments begin.

## Closing Principle

> The implementation is not asked to prove what Ario is.

> It is asked to make Ario's claims, limits, failures, and revisions observable.

> If the architecture survives executable reality, that is evidence.

> If it fails, that failure is evidence too.