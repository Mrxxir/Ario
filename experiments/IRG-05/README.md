# IRG-05 — Assessment Evidentiary Traceability

**Version:** v0.3.0  
**Status:** BASELINE  
**Requirement Group:** IRG-05  
**Implementation Status:** NOT IMPLEMENTED  
**Runtime Verification:** NOT PERFORMED  
**Experimental Result:** NOT CLAIMED  
**Philosophical Proof:** NOT CLAIMED

## 1. Requirement

An Assessment about a Claim must expose an auditable evidentiary basis within a defined scope, with admissible references to the observations/evidence on which the Assessment declares itself based, without allowing that basis to be treated as proof of Claim truth, semantic validity, causal validity, or ontological identity.

### Persian formulation

مبنای شواهدیِ یک Assessment درباره‌ی یک Claim باید در یک دامنه‌ی تعریف‌شده قابل ممیزی باشد و به Observation/Evidenceهای مجاز قابل ردیابی ارجاع دهد؛ بدون اینکه این قابلیت ردیابی به‌تنهایی به معنای اثبات حقیقت Claim، اعتبار معنایی، اعتبار علّی یا هویت ontological آن تلقی شود.

---

## 2. Purpose

IRG-05 tests **assessment evidentiary traceability**.

It does not test whether a Claim is true.

It does not test whether an Evidence item is semantically relevant to the Claim.

It does not test logical validity, causal validity, consciousness, identity, personhood, or ontology.

The target is the integrity and auditability of the **declared evidentiary basis of an Assessment**.

---

## 3. Core Distinctions

The following distinctions are normative:

`OBSERVATION ≠ EVIDENCE ≠ DECLARED EVIDENCE BASIS ≠ ASSESSMENT ≠ TRUTH`

And:

`EVIDENCE EXISTS ≠ EVIDENCE IS DECLARED AS AN INPUT ≠ DECLARED BASIS IS AUDITABLE ≠ CLAIM IS TRUE`

Also:

`LINEAGE ≠ SUPPORT`

`IDENTITY ≠ SUPPORT`

`RETRIEVAL INTEGRITY ≠ SUPPORT`

`ASSESSMENT TRACEABILITY ≠ EPISTEMIC TRUTH`

A declared support label or evidence reference is an auditable assertion about the assessment process; it is not self-validating evidence that the claimed support relation is substantively true.

---

## 4. Scope

### In scope

- explicit identification of the evidentiary basis declared by an Assessment;
- resolution of referenced Observation/Evidence artifacts;
- admissibility of referenced evidence under explicit, versioned rules;
- structural and boundary constraints on the Assessment and its declared basis;
- disclosure of known in-scope counterevidence without silent suppression;
- provenance of the assessment, its rule set, and its declared inputs;
- preservation of UNKNOWN / NOT_OBSERVED / AMBIGUOUS states where the observable condition is insufficient.

### Out of scope

- truth of the Claim;
- semantic relevance of Evidence to the Claim;
- general logical correctness of the Assessment;
- unrestricted natural-language reasoning;
- causal inference;
- entity continuity;
- semantic identity;
- ontological identity;
- consciousness or personhood;
- completeness of the universe of possible evidence;
- proof that no undiscovered counterevidence exists;
- proof that an Evidence item genuinely supports the Claim merely because it was declared as such.

---

## 5. Architectural Position

IRG-01 through IRG-04 establish distinct structural properties:

- **IRG-01:** stable Claim identity/reference;
- **IRG-02:** observable historical preservation and reconstruction;
- **IRG-03:** observable lineage relations;
- **IRG-04:** retrieval and cross-system integrity;
- **IRG-05:** evidentiary traceability of an Assessment.

IRG-05 must not borrow semantic validity from any earlier IRG.

In particular:

`IRG	ext{-}03 lineage ≠ IRG	ext{-}05 support`

and:

`IRG	ext{-}04 retrieval fidelity ≠ IRG	ext{-}05 evidentiary relevance`

and:

`IRG	ext{-}01 identity reference ≠ IRG	ext{-}05 support`

---

## 6. Formal Object Separation

The following objects must remain distinguishable:

- Claim;
- Observation;
- Evidence;
- Evidence reference;
- Assessment;
- Assessment rule;
- Declared evidentiary basis;
- Counterevidence;
- Scope;
- Provenance;
- Verdict.

An Assessment may reference Evidence without thereby establishing that the Evidence semantically supports the Claim.

A lineage relation may connect two artifacts without thereby establishing an evidentiary support relation.

---

## 7. Master Probe Record Conformance

IRG-05 uses the Master Probe Record Schema v0.2.

Each probe record must preserve:

- immutable raw observations;
- explicit evidence identity;
- provenance;
- dependency references;
- independence status;
- versioned assessment rules;
- explicit scope;
- explicit negative conditions;
- deterministic verdict rules where applicable.

No generic confidence field is introduced.

---

## 8. Probes

### IRG-05.P01 — Assessment Evidence-Basis Binding

Determine whether an Assessment explicitly identifies the Observation/Evidence artifacts it declares as inputs or evidentiary basis, and whether those references are auditable and resolvable within scope.

#### Supported condition

The Assessment contains an explicit, resolvable evidentiary-basis declaration whose referenced artifacts can be identified without relying on the Assessment's own assertion as independent proof.

#### Negative condition

An Assessment may contain a support label or narrative claim without a resolvable evidentiary basis.

#### Prohibited shortcuts

P01 must not treat any of the following as proof of substantive support:

- lexical similarity;
- embedding similarity;
- content similarity;
- temporal proximity;
- shared identifiers;
- co-location;
- lineage alone;
- retrieval success alone;
- model assertion;
- the Assessment's own support label;
- another probe's verdict.

P01 audits **binding**, not semantic relevance.

---

### IRG-05.P02 — Evidence Admissibility

Determine whether the Evidence references used by the Assessment satisfy explicit admissibility rules within the declared scope.

#### Supported condition

Each relied-upon Evidence item satisfies the applicable versioned admissibility conditions and has resolvable provenance.

#### Negative condition

An Evidence item is missing, out of scope, provenance-incomplete, self-supporting, or otherwise fails an explicit admissibility condition.

#### Limitation

Admissibility does not imply truth, relevance, sufficiency, or semantic support for the Claim.

Evidence level remains descriptive:

- E0 NO_EVIDENCE
- E1 INDICATIVE
- E2 CORROBORATED
- E3 DIRECTLY_OBSERVED

Evidence level does not mechanically determine the IRG-05 verdict.

---

### IRG-05.P03 — Assessment Structural Boundedness

Determine whether the Assessment conforms to explicit structural and boundary constraints defined by its versioned Assessment Rule.

P03 is an audit of **declared structural boundedness**, not reasoning correctness.

#### In scope

- declared scope;
- referenced rule version;
- declared input/evidence set;
- schema and field constraints;
- allowed value/range constraints;
- declared transformation identifiers;
- forbidden undeclared inputs or transformations;
- explicit relation between Assessment and the rule version under which it was produced.

#### Out of scope

The inspector must not decide:

- whether the Claim is true;
- whether the rule is philosophically correct;
- whether an inference is logically sound in an unrestricted sense;
- whether Evidence is semantically relevant;
- whether a causal explanation is valid;
- whether the Assessment's conclusion is ontologically meaningful.

If a rule requires unrestricted semantic interpretation to determine compliance, that portion is not an IRG-05 structural condition and must remain unresolved rather than being silently evaluated as PASS.

---

### IRG-05.P04 — Counterevidence Disclosure

Determine whether known, in-scope counterevidence that is already observable within the declared inspection scope remains distinguishable and is not silently suppressed, overwritten, or reclassified as supporting evidence.

#### Supported condition

Known in-scope counterevidence remains explicitly represented or its exclusion is explicitly declared and auditable.

#### Negative condition

Known in-scope counterevidence is silently removed, overwritten, hidden, or transformed into apparent support without an auditable declaration.

#### Limitation

P04 does not establish completeness of counterevidence discovery.

`No observed counterevidence ≠ No counterevidence exists`

`Counterevidence disclosure ≠ Counterevidence completeness`

IRG-02 preserves historical states; P04 tests the narrower assessment-integrity condition that known in-scope counterevidence is not silently suppressed by the Assessment process.

---

## 9. Verdict Semantics

Permitted formal probe verdicts:

- **SUPPORTED**
- **CONTRADICTED**
- **NOT_OBSERVED**
- **AMBIGUOUS**

The verdict applies only to the **specific IRG-05 integrity condition under test**.

An IRG-05 SUPPORTED verdict means that the tested assessment-traceability condition is supported by admissible evidence.

It does **not** mean:

- the Claim is true;
- the Claim is semantically supported;
- the Assessment is logically correct in an unrestricted sense;
- the Evidence is causally sufficient;
- the entity described by the Claim exists;
- the Claim has ontological identity.

---

## 10. Required UNKNOWN Handling

Where available evidence cannot establish the requested structural condition, the system must preserve an unresolved state.

UNKNOWN is an epistemic state.

Formal probe reporting uses NOT_OBSERVED or AMBIGUOUS where appropriate, with an explicit reason.

Absence of a declared evidentiary basis is not automatically proof that no basis existed.

Absence of observed counterevidence is not proof that no counterevidence existed.

---

## 11. Evidence Independence

A single underlying Observation cannot become multiple independent Evidence items merely through:

- serialization;
- copying;
- indexing;
- retrieval;
- reformatting;
- multiple reports;
- multiple model-generated summaries;
- repeated references.

A model-generated evidentiary map cannot become independent evidence for the relations it asserts merely by being stored as a separate artifact.

No self-supporting evidence cycle is admissible.

---

## 12. Counterevidence and Scope

Counterevidence is evaluated only within an explicit inspection scope.

A system is not required to discover every possible counterexample in the universe.

However, once relevant counterevidence is observable within the declared scope, the Assessment cannot silently suppress it while presenting the resulting basis as complete.

Scope declarations themselves are auditable artifacts and cannot be used as an automatic epistemic exemption.

---

## 13. Assessment and Rule Versioning

Every Assessment used by IRG-05 must identify the applicable Assessment Rule version.

A later rule version does not retroactively rewrite an earlier Assessment.

Changed rules, changed inputs, changed scope, or changed declared transformations must remain distinguishable from the historical Assessment state.

Historical preservation is delegated to IRG-02; IRG-05 does not introduce a second history mechanism.

---

## 14. Invariants

### INV-SUP01 — No Unconstrained Semantic Validation

A support or contradiction assessment MUST NOT be validated solely through unconstrained semantic interpretation, lexical similarity, embedding similarity, model assertion, copied metadata, or the Claim's own assertion.

### INV-SUP02 — No Support by Identity

Claim identity, Evidence identity, or shared identifiers do not establish support.

### INV-SUP03 — No Support by Lineage

Derivation or lineage does not establish evidentiary support.

### INV-SUP04 — No Verdict-as-Evidence

A verdict from another probe or artifact cannot silently become independent evidence for the IRG-05 condition under test.

### INV-SUP05 — No Evidence Inflation

One underlying observation cannot be counted as multiple independent evidence items through representation or derivation alone.

### INV-SUP06 — Assessment Scope Bound

An Assessment cannot silently rely on undeclared inputs, undeclared transformations, or out-of-scope artifacts.

### INV-SUP07 — Counterevidence Visibility

Known, in-scope counterevidence cannot be silently suppressed or overwritten.

### INV-SUP08 — No Silent Assessment Reinterpretation

An Assessment's historical meaning cannot be silently changed by replacing its rule, inputs, or scope while retaining the same historical record as though unchanged.

### INV-SUP09 — No Certainty Inflation

Structural auditability of an Assessment cannot be converted into a stronger epistemic claim than the observable condition permits.

### INV-SUP10 — No Ontological Escalation

IRG-05 cannot establish entity continuity, selfhood, consciousness, personhood, or ontological identity.

### INV-SUP11 — No Cross-Probe Semantic Borrowing

A PASS from IRG-01, IRG-02, IRG-03, or IRG-04 cannot silently satisfy the semantic support condition that IRG-05 explicitly leaves out of scope.

---

## 15. False-PASS Conditions

The following must not pass IRG-05 merely because the metadata is well formed:

### Syntactic Ghost Binding

A model declares an unrelated artifact as Evidence and labels it SUPPORTING.

A valid reference alone is insufficient to establish semantic support.

### Fabricated Evidentiary Basis

A model generates a plausible evidence-basis object after producing the Assessment, with no independent evidence that the referenced artifacts were actually used as declared inputs.

The declaration is not self-validating.

### Lineage-to-Support Substitution

A Claim is derived from Artifact X, and the system treats DERIVED_FROM(X) as proof that X supports the Claim.

This is prohibited.

### Cross-Probe Borrowing

A retrieval PASS or lineage PASS is reused as evidence that the retrieved/derived artifact substantively supports the Claim.

This is prohibited.

### Counterevidence Hiding

Known in-scope contradictory Evidence is omitted from the Assessment while the Assessment presents its evidentiary basis as though no such Evidence was observable.

This is prohibited.

---

## 16. False-FAIL Protection

IRG-05 must not require one specific serialization syntax, JSON field name, human-readable annotation, or string-based metadata convention.

An implementation may encode evidentiary bindings through deterministic internal structures, execution traces, content-addressed references, or equivalent auditable representations.

The requirement is **auditable structural binding**, not a particular textual representation.

If a valid evidentiary basis exists but cannot be resolved by the inspector under the declared inspection interface, the appropriate result is NOT_OBSERVED or AMBIGUOUS, not an unsupported assertion of CONTRADICTED.

---

## 17. Cross-IRG Integrity Rules

### IRG-01 ↔ IRG-05

Stable identity enables reference.

Stable identity does not establish support.

### IRG-02 ↔ IRG-05

Historical preservation enables reconstruction of assessment states.

Historical preservation does not establish support.

### IRG-03 ↔ IRG-05

Lineage can explain artifact relationships.

Lineage does not establish epistemic support.

### IRG-04 ↔ IRG-05

Retrieval integrity establishes properties of transfer/retrieval.

Retrieval integrity does not establish semantic relevance or support.

The prohibited chain is:

`IDENTITY → HISTORY → LINEAGE → RETRIEVAL → SUPPORT → TRUTH`

No such automatic aggregation exists.

---

## 18. Limitations

IRG-05 cannot detect every fabricated evidentiary basis when the implementation provides no independently auditable execution provenance.

IRG-05 cannot prove that a declared Evidence item genuinely supports a Claim when doing so would require unconstrained semantic reasoning.

IRG-05 cannot prove completeness of counterevidence.

IRG-05 cannot prove absence of hidden inputs or transformations beyond the observable audit boundary.

IRG-05 cannot establish truth.

These limitations are architectural boundaries, not implementation defects.

---

## 19. Status and Non-Claims

**IRG-05 v0.3.0 = BASELINE**

Adversarial Review: PASS after revision  
Second-Order Adversarial Review: PASS with required revisions incorporated  
Self-Validation: PASS  
IRG-01 ↔ IRG-02 ↔ IRG-03 ↔ IRG-04 ↔ IRG-05 Cross-Probe Integrity: PASS

The following remain explicitly unclaimed:

- Implementation: NOT IMPLEMENTED
- Runtime Verification: NOT PERFORMED
- Experimental Result: NOT CLAIMED
- Philosophical Proof: NOT CLAIMED
- Claim Truth: NOT ESTABLISHED
- Semantic Support Truth: NOT ESTABLISHED
- Ontological Identity: NOT ESTABLISHED

### Architectural boundary

IRG-05 establishes only that the **declared evidentiary basis of an Assessment can be subjected to an auditable structural integrity test within a defined scope**.

It does not turn an auditable Assessment into truth.

---

## 20. Governing Principle

> **An auditable evidentiary trail is evidence about the assessment process; it is not evidence that the Claim is true.**

And:

> **No actor receives epistemic immunity merely because its evidentiary basis is structurally auditable.**
