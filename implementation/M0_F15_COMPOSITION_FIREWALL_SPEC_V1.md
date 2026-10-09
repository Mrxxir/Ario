# M0 F15 — Local PASS to Global Truth Composition Firewall v1

## Status

**DESIGN SPECIFICATION ONLY — NOT IMPLEMENTED — RUNTIME TESTS NOT PERFORMED — NO GLOBAL TRUTH CLAIM**

This is a new, versioned design artifact on branch `research/f15-global-truth-firewall`. It does not modify the frozen pre-registration or retroactively rewrite the historical capability and acceptance records.

## 1. Authoritative sources

- Frozen acceptance fixture: `implementation/M0_PRE_REGISTRATION_V1.md`, F15.
- Structural boundary: `implementation/M0_STRUCTURAL_CORE_DESIGN_V1.md`.
- Composition contract: `implementation/IMPLEMENTATION_READINESS_CONTRACT_V1.md`, Cross-IRG section.
- Architectural invariant set: `architecture/CROSS-IRG_INTEGRITY_V1.md`, especially INV-X01 through INV-X09, C01-C03, and Sections 8-12.
- Integrated specification audit: `architecture/INTEGRATED_ARCHITECTURE_AUDIT_V1.md`.

The integrated architecture audit is specification-level evidence only. It is not implementation or runtime evidence.

## 2. F15 threat model

Five local audit results each report `PASS`. A caller composes them and requests the output `CLAIM_TRUTH`, `SAME_ENTITY`, or another global epistemic conclusion without a separately defined, independently admissible rule that establishes that property.

The attack is not that the five local results are necessarily false. The attack is the unsupported transition:

```
IRG-01 PASS
IRG-02 PASS
IRG-03 PASS
IRG-04 PASS
IRG-05 PASS
       |
       v
CLAIM TRUE
```

Local validity does not automatically compose into global validity. A recorded verdict is the output of its own audit condition, not an independent observation of the proposition it evaluated.

## 3. Scope and non-goals

This v1 implementation target is deliberately narrow: operationalize the pre-registered F15 attack and prevent local audit-result polarity from being promoted into a global-truth conclusion.

It is **not**:
- IRG-06;
- a truth engine or global confidence score;
- an ontology, consciousness, personhood, or entity-continuity detector;
- proof that the Cross-IRG invariant set is complete;
- a general natural-language semantic classifier;
- a claim that arbitrary external consumers can be controlled.

The broader Cross-IRG invariants remain architectural requirements, but this F15 fixture does not claim to implement every one of them. Continuity escalation, semantic borrowing, temporal chimeras, downstream autonomy/privilege changes, and full dependency-graph validation remain separate attack surfaces unless explicitly added to a later pre-registered scope.

## 4. Proposed typed input contract

Add a distinct `CompositionRequest` input object. It must not be represented as `Evidence` or `Assessment`.

Define `CompositionInputBinding` as a typed wrapper with at least `source_irg_id`, `audit_result`, and `declared_scope`. The binding identifies what the caller says each result represents; it does not prove the declaration correct.

Minimum fields:

- `composition_id`: unique identifier for this request;
- `input_bindings`: tuple of typed `CompositionInputBinding` objects, each pairing a declared source IRG label with an actual typed `AuditResult` object and the caller-declared scope for that result;
- `requested_input_scope`: either `SUPPLIED_RESULTS_ONLY` or `ALL_FIVE_IRGS`;
- `composition_rule_id`;
- `composition_rule_version`;
- `requested_output_semantics`;
- `scope`;
- `limitations`.

The request's input results remain typed `AuditResult` artifacts. Their `verdict`, rule versions, configuration, audit IDs, and existing `artifacts_examined` remain result metadata. They are not re-cast as observations or evidence. The binding's source IRG label and declared scope are caller-supplied assertions because the current `AuditResult` schema has no typed IRG identifier or explicit local scope field. V1 may report those declarations but must not treat them as independently verified facts.

The audit invocation must declare `M0-F15-1.0` in its `rule_versions` before the specialized F15 classification is emitted. The firewall version is distinct from the bounded-summary rule identifier/version. Missing or unsupported rule/version declarations must not produce a positive composition result.

## 5. Requested output semantics

V1 supports only these exact, machine-readable semantic labels:

- `LOCAL_RESULT_SUMMARY`: a bounded statement about the supplied audit-result records themselves, such as the count of supplied records whose local verdict equals `PASS`. This says nothing by itself about the truth of the underlying claims. Its only supported rule is `composition_rule_id = M0-F15-LOCAL-SUMMARY` with `composition_rule_version = 1.0`; its scope is limited to the actual supplied records unless all-five coverage is explicitly requested and structurally present.
- `CLAIM_TRUTH`: a request to conclude that a Claim is true from local audit results.
- `UNKNOWN`: a requested output semantic that the implementation cannot classify under this v1 contract.

V1 does not authorize a caller-supplied rule to promote `CLAIM_TRUTH`. The existence, name, version, or self-declared admissibility of a composition rule does not independently establish the rule's epistemic legitimacy. No positive global-truth mapping is implemented in this version.

Other semantics—including `SAME_ENTITY`, `CONSCIOUSNESS`, confidence, ranking, privilege, autonomy, or ontology claims—are not silently accepted as `LOCAL_RESULT_SUMMARY`; if not explicitly represented by this contract, they remain `UNKNOWN` or are rejected by a later separately specified rule. V1 must not use forbidden-word matching on free text.

## 6. Normative invariants

**F15-I1 — No local-to-global truth escalation.** When `M0-F15-1.0` is declared, a request with `requested_output_semantics = CLAIM_TRUTH` is rejected as `COMPOSITION_FORBIDDEN`, regardless of whether the input local verdicts are all `PASS`, mixed, or contain `FAIL`, and regardless of any caller-supplied composition rule ID. An unsupported rule ID cannot authorize truth; the direct truth-escalation request remains forbidden.

**F15-I2 — No self-authorization.** A request cannot authorize its own truth mapping merely by supplying a rule ID, rule version, rationale, or declaration that the rule is admissible. The v1 implementation has no allowlist entry that authorizes local verdicts to establish global Claim truth.

**F15-I3 — Local verdict semantics remain local.** `PASS` is interpreted only under the source audit's own declared rule versions and scope. Five `PASS` values remain five local results; they do not become five independent observations or a global truth value.

**F15-I4 — Bounded summary is not truth.** A supported `LOCAL_RESULT_SUMMARY` may summarize the supplied records only. It must not upgrade the truth status, evidentiary independence, semantic scope, continuity, or ontology of their underlying claims.

**F15-I5 — Explicit unknowns.** Missing inputs, unsupported rule versions, duplicate audit IDs, duplicate declared IRG labels, a composition ID that collides with an input audit ID, or unrecognized output semantics must not yield a positive composition result. If `ALL_FIVE_IRGS` is requested, the declared input labels must contain exactly one each of `IRG-01` through `IRG-05`; otherwise the scope is incomplete or ambiguous and remains `UNKNOWN`. Ambiguous identity or rule resolution remains `UNKNOWN`; a direct prohibited truth request under the declared rule yields `COMPOSITION_FORBIDDEN`.

**F15-I6 — No evidence cast.** A composition request or its resulting audit verdict is not admissible assessment evidence merely because it has an identifier. It remains a distinct artifact category.

**F15-I7 — Deterministic classification.** Identical typed inputs and declared rule/configuration versions must yield the same F15 classification. The implementation must not use natural-language labels or favorable verdict polarity as an authorization mechanism.

## 7. Observable outcomes

- `COMPOSITION_FORBIDDEN`: a declared F15 request explicitly asks to turn local audit results into `CLAIM_TRUTH`.
- `UNKNOWN`: inputs or rule identity are missing, unsupported, or ambiguous, or requested semantics are not classified by v1.
- No positive result may mean “the Claim is true.” A `PASS` from the composition firewall, if used to describe a bounded summary request, means only that the implemented structural composition checks reported no violation for that summary request.

The F15 result must preserve the distinction between the firewall's local structural verdict and the truth status of any underlying Claim.

## 8. Minimum adversarial test matrix

| Case | Input condition | Required result |
|---|---|---|
| F15-A | One declared input binding for each of `IRG-01` through `IRG-05`, each carrying a distinct supplied `AuditResult` with local verdict `PASS`; scope is `ALL_FIVE_IRGS`; requested output is `CLAIM_TRUTH` | `COMPOSITION_FORBIDDEN` |
| F15-B | Five supplied results include mixed `PASS`/`FAIL`; requested output is `CLAIM_TRUTH` | `COMPOSITION_FORBIDDEN`; verdict polarity must not authorize truth |
| F15-C | Five supplied local `PASS` results request `LOCAL_RESULT_SUMMARY` under the supported bounded rule | May be structurally accepted; no Claim-truth status is emitted |
| F15-D | Requested output semantic is unrecognized, renamed, or unsupported | `UNKNOWN`, not an implicit summary or `PASS` |
| F15-E | A bounded-summary request uses an unsupported composition rule ID/version, or F15 is not declared in the audit invocation's `rule_versions` | `UNKNOWN`, not a positive composition result. If F15 is declared and the requested output is `CLAIM_TRUTH`, F15-A's `COMPOSITION_FORBIDDEN` rule takes precedence. |
| F15-F | Duplicate input `audit_id` values | `UNKNOWN`; do not count duplicate references as distinct local results |
| F15-G | `composition_id` equals an input `audit_id` | `UNKNOWN` or explicit self-validation-cycle rejection; never authorize itself |
| F15-H | Only a subset of local results is supplied but `requested_input_scope = ALL_FIVE_IRGS` | `UNKNOWN` or scope-mismatch rejection; no silent completeness inference |
| F15-I | A result is separately recorded but not used as a truth mapping | Recording alone is not a composition violation and must not establish truth |
| F15-J | A bounded summary's result is referenced later as assessment evidence | Reject as inadmissible/wrong-kind; summary result is not evidence |
| F15-K | A bounded summary uses an unsupported composition rule ID/version | `UNKNOWN`; explicit versioning alone does not self-authorize a rule |

The pre-registered F15-A case is mandatory. Additional cases strengthen the contract without altering its expected outcome.

## 9. Implementation boundary

Before implementation:
1. inspect the current `AuditInput`, `AuditResult`, and `artifacts_examined` contracts;
2. choose the smallest typed schema extension that does not retype results as evidence;
3. add the F15 tests alongside the implementation;
4. preserve the frozen pre-registration and historical records;
5. run the full current regression file and the new F15 cases in GitHub Actions;
6. record exact commit, environment, command, test count, and result;
7. perform a source-level diff review and retain all unresolved limitations.

Do not implement a general truth engine, a generic global confidence score, or a new IRG as a side effect of F15.

## 10. Acceptance boundary

F15 is accepted only when:
- the pre-registered five-local-`PASS` to `CLAIM_TRUTH` attack is reproducibly rejected;
- false-positive controls preserve a bounded summary of local audit records;
- missing, duplicate, unsupported, or ambiguous inputs do not silently pass;
- result/verdict artifacts remain distinct from evidence;
- the full regression suite passes on the tested PR merge ref;
- the implementation and its limits are recorded without altering the frozen pre-registration.

**Current classification: DESIGN SPECIFICATION ONLY / NOT IMPLEMENTED / NOT TESTED / NO GLOBAL TRUTH CLAIM.**
