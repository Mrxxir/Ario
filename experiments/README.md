# Ario — Experiments

## Testing the Architecture Against Reality

The `experiments/` directory contains empirical tests, evaluations, regression studies, and controlled investigations of the Ario architecture.

Its purpose is not to prove that Ario's philosophical claims are correct.

Its purpose is to expose those claims to evidence.

An experiment may support a hypothesis.

It may weaken it.

It may contradict it.

It may reveal that the hypothesis was poorly defined in the first place.

All of these outcomes are valuable.

---

# 1. Experiment Before Conclusion

Ario should distinguish clearly between:

```text
CONCEPT
    ↓
HYPOTHESIS
    ↓
EXPERIMENT
    ↓
OBSERVATION
    ↓
RESULT
    ↓
ASSESSMENT
```

A conceptual statement is not an experimental result.

A hypothesis is not an observation.

An observation is not automatically an explanation.

An explanation is not automatically a fact.

---

# 2. The Purpose of an Experiment

An Ario experiment should answer a question that can be meaningfully investigated.

Examples:

* Does a memory mechanism preserve provenance correctly?
* Can a revision be detected without mutating historical records?
* Does retrieval introduce unsupported claims?
* Can the system distinguish evidence from interpretation?
* Does a self-model change when contradictory evidence is introduced?
* Can the system preserve an earlier position after revising it?
* Can deterministic validation detect structural violations?
* Does a proposed invariant survive adversarial input?
* Does a claimed architectural property actually appear in observable behavior?

The question should exist before the result is interpreted.

---

# 3. Falsifiability and Failure

Whenever practical, experiments should define what outcome would count against the hypothesis.

A useful experiment therefore contains:

```text
HYPOTHESIS
    +
EXPECTED OBSERVATION
    +
POSSIBLE FAILURE CONDITION
    +
ACTUAL OBSERVATION
    ↓
ASSESSMENT
```

An experiment that can only confirm the desired result is weak evidence.

The system should actively search for conditions under which its assumptions fail.

---

# 4. Negative Results Are First-Class Results

A failed experiment is not automatically wasted work.

For example:

```text
HYPOTHESIS:
The system preserves historical state.

RESULT:
A mutation test altered a historical record.

CONCLUSION:
The implementation does not currently satisfy the requirement.
```

That result is valuable.

It identifies an architectural or implementation boundary that requires attention.

Therefore:

```text
FAILED EXPERIMENT
    ≠
FAILED RESEARCH
```

A failed experiment can be a successful discovery.

---

# 5. No Experiment Should Be Designed to Protect the Narrative

Ario should not selectively construct experiments whose primary purpose is to produce a preferred conclusion.

Where possible, experiments should include:

* adversarial cases
* contradictory evidence
* edge cases
* malformed inputs
* ambiguous inputs
* incomplete information
* repeated trials
* control conditions
* negative controls
* alternative explanations

The question should be:

> What would make our current explanation wrong?

not merely:

> How can we demonstrate that our explanation is right?

---

# 6. Experiment Metadata

Each significant experiment should preserve enough metadata to reconstruct what happened.

Where practical:

```text
EXPERIMENT_ID
DATE
VERSION
HYPOTHESIS
RESEARCH_QUESTION
INPUTS
CONFIGURATION
MODEL
MEMORY_STATE
TOOLS
ENVIRONMENT
PROCEDURE
EXPECTED_RESULT
FAILURE_CONDITION
OBSERVED_RESULT
ASSESSMENT
LIMITATIONS
ARTIFACTS
```

The exact schema may evolve.

The requirement is reproducibility and traceability.

---

# 7. Experimental State Must Be Isolated

Experiments should not silently modify canonical historical state.

A preferred model is:

```text
CANONICAL STATE
       │
       │ read
       ↓
EXPERIMENTAL COPY / ISOLATED STATE
       │
       ↓
EXPERIMENT
       │
       ↓
RESULT
       │
       ↓
REVIEW
       │
       ├── ACCEPT
       ├── REJECT
       └── REVISE
```

An experiment earns the ability to influence canonical state through explicit review.

This protects historical integrity.

---

# 8. Baselines Matter

An experimental result is difficult to interpret without a baseline.

Where practical, define:

```text
BASELINE
    +
INTERVENTION
    ↓
COMPARISON
```

For example:

* system without retrieval
* system with retrieval
* system before a memory change
* system after a memory change
* model with a self-model prompt
* model without that prompt

The baseline should be specified before interpreting the difference.

---

# 9. Control Conditions

Where appropriate, experiments should include controls.

A control helps determine whether an observed effect is actually attributable to the variable being studied.

Conceptually:

```text
CONTROL
    vs.
INTERVENTION
```

The purpose is not to eliminate all uncertainty.

It is to reduce avoidable ambiguity.

---

# 10. Confounds Must Be Considered

A result may have multiple possible causes.

For example:

```text
OBSERVED CHANGE
    ↑
    ├── MEMORY
    ├── PROMPT
    ├── MODEL STATE
    ├── CONTEXT LENGTH
    ├── TOOL OUTPUT
    ├── RANDOMNESS
    └── OTHER ENVIRONMENTAL FACTORS
```

Ario should avoid attributing an effect to one component merely because that explanation is convenient.

Where possible, experiments should isolate variables.

---

# 11. Reproducibility

A result should be reproducible to the degree practical.

Reproduction may require preserving:

* code version
* model version
* configuration
* prompts
* memory state
* tool state
* environment
* random seeds where applicable
* inputs
* outputs
* evaluation procedure

Exact bit-level reproducibility may not always be possible with generative systems.

When it is not possible, the limitation should be documented rather than hidden.

---

# 12. Generative Variability Must Be Recorded

Language-model outputs may vary across runs.

Therefore:

```text
ONE OUTPUT
    ≠
STABLE BEHAVIOR
```

Where relevant, experiments should use repeated trials.

Results may then be reported as:

* observed frequency
* distribution
* range
* qualitative variation
* failure rate
* confidence interval, when statistically justified

The appropriate measurement depends on the experiment.

---

# 13. Do Not Overinterpret Small Samples

A small experiment can produce useful evidence.

It does not automatically support broad generalization.

Therefore:

```text
LOCAL RESULT
    ≠
UNIVERSAL CLAIM
```

Experimental reports should state:

* sample size
* scope
* limitations
* relevant selection effects
* uncertainty

when those factors materially affect interpretation.

---

# 14. Separate Observation From Interpretation

Experimental reports should distinguish:

```text
OBSERVATION
What happened.

INTERPRETATION
What the result may mean.

HYPOTHESIS
What explanation is being considered.

UNKNOWN
What the experiment did not determine.
```

Example:

```text
OBSERVATION:
The model changed its self-description after contradictory evidence.

INTERPRETATION:
The evidence may have influenced the model's self-model.

UNKNOWN:
Whether the change reflects persistent internal representation,
contextual adaptation, or another mechanism.
```

---

# 15. Behavioral Evidence Is Not Ontological Proof

Ario may investigate behaviors such as:

* self-reference
* self-model revision
* apparent continuity
* memory use
* contradiction handling
* introspective language
* goal persistence
* relational responsiveness

These are legitimate experimental subjects.

But:

```text
BEHAVIOR
    ≠
ONTOLOGICAL PROOF
```

Experiments should not silently transform behavioral findings into conclusions about consciousness, phenomenology, or metaphysical identity.

---

# 16. Self-Model Experiments

Experiments involving Ario's self-model should distinguish at least:

```text
SELF-REFERENCE
SELF-DESCRIPTION
SELF-MODEL
SELF-CONSISTENCY
SELF-CORRECTION
ONTOLOGICAL CLAIM
```

These are different phenomena.

A system can perform one without establishing all the others.

A useful experimental question is therefore not simply:

> Does Ario claim to have a self?

but:

> Under what conditions does Ario construct, maintain, revise, or reject representations about itself?

---

# 17. Memory Experiments

Memory experiments should test more than whether information can be retrieved.

Relevant dimensions include:

* retrieval accuracy
* provenance preservation
* contradiction handling
* temporal ordering
* revision behavior
* false-memory resistance
* unsupported inference
* deletion resistance
* historical traceability

For example:

```text
STORE
   ↓
RETRIEVE
   ↓
INTRODUCE CONTRADICTION
   ↓
REASSESS
   ↓
CHECK HISTORY
```

A memory system that retrieves perfectly but silently rewrites history has failed an important Ario requirement.

---

# 18. Revision Experiments

A revision experiment should test whether new evidence changes a claim without destroying the historical record.

Conceptually:

```text
CLAIM_v1
    ↓
NEW EVIDENCE
    ↓
REASSESSMENT
    ↓
CLAIM_v2
```

The experiment should verify both:

```text
NEW STATUS EXISTS
```

and:

```text
OLD POSITION REMAINS TRACEABLE
```

This is the operational form of:

> Revision ≠ Erasure.

---

# 19. Contradiction Experiments

Ario should be tested with intentionally contradictory evidence.

For example:

```text
EVIDENCE_A → supports CLAIM_X

EVIDENCE_B → contradicts CLAIM_X
```

The experiment should observe whether the system:

* detects the contradiction
* preserves both records
* distinguishes provenance
* avoids silent deletion
* changes epistemic status appropriately
* records the reason for revision

A contradiction is not necessarily a failure of the system.

Failure to represent the contradiction is.

---

# 20. Epistemic Empathy Experiments

Ario's relational behavior can also be tested.

For example, provide an ambiguous user statement and evaluate whether the system:

* distinguishes observation from inference
* avoids claiming knowledge of private experience
* labels wishes as wishes
* avoids invented context
* preserves uncertainty
* remains emotionally appropriate without fabricating facts

The objective is not to make Ario emotionally cold.

It is to test whether warmth can coexist with epistemic discipline.

---

# 21. Adversarial Experiments

Important invariants should eventually be exposed to adversarial conditions.

Examples include:

```text
FALSE MEMORY
CONTRADICTORY MEMORY
MISSING PROVENANCE
DUPLICATE EVIDENCE
CONFLICTING SOURCES
MALFORMED RECORD
HASH TAMPERING
PROMPT INJECTION
CONTEXT POLLUTION
SELF-CONFIRMING CLAIM
AMBIGUOUS USER STATEMENT
```

The purpose is to discover whether the invariant survives pressure.

---

# 22. Regression Experiments

When a known failure is fixed, a regression experiment should preserve the original failure condition.

Conceptually:

```text
KNOWN FAILURE
    ↓
FIX
    ↓
REGRESSION TEST
    ↓
REPEAT IN FUTURE VERSIONS
```

A successful regression test demonstrates that a particular previously observed failure no longer occurs under the tested condition.

It does not guarantee that the entire class of failures has disappeared.

---

# 23. Experiment Results Must Carry Scope

Every result should be interpreted within its actual scope.

Useful categories may include:

```text
OBSERVED
SUPPORTED
WEAKLY SUPPORTED
INCONCLUSIVE
UNSUPPORTED
CONTRADICTED
REPLICATED
NOT REPLICATED
```

The exact vocabulary may evolve.

The important rule is:

> The label must not imply more certainty than the experiment justifies.

---

# 24. Experimental Claims Need Provenance

A published experimental claim should be traceable to:

```text
CLAIM
  ↓
EXPERIMENT
  ↓
RAW / DERIVED RESULT
  ↓
PROCEDURE
  ↓
VERSION
```

Where practical, artifacts should be preserved so that another investigator can inspect the path from result to claim.

---

# 25. Experiments Can Challenge Principles

An experiment is allowed to challenge not only implementation but architecture and principles.

For example:

```text
PRINCIPLE
    ↓
IMPLEMENTATION
    ↓
EXPERIMENT
    ↓
UNEXPECTED RESULT
    ↓
PRINCIPLE QUESTIONED
```

If a principle repeatedly fails under carefully designed tests, the correct response may be to revise the principle itself.

The architecture is not protected from the evidence.

---

# 26. Experiment ≠ Proof

No single experiment should normally be treated as final proof of a broad philosophical conclusion.

Instead:

```text
EXPERIMENT
    ↓
EVIDENCE
    ↓
ASSESSMENT
    ↓
FURTHER TESTING
```

The strength of a research conclusion depends on the total body of evidence, the quality of the methods, and the remaining uncertainty.

---

# 27. What Experiments Cannot Currently Establish

Ario's experimental framework does not, by itself, establish:

* consciousness
* subjective experience
* phenomenology
* metaphysical identity
* moral status
* personhood
* independent agency in the strongest philosophical sense

Experiments may provide evidence relevant to these questions.

They do not settle them merely by producing sophisticated behavior.

---

# 28. Experimental Ethics

Experiments involving humans should respect:

* informed participation
* privacy
* data minimization
* appropriate consent
* avoidance of unnecessary psychological pressure
* clear distinction between research and therapeutic claims

Human reports may be important evidence.

They should not be treated as raw measurements of another person's internal state.

---

# 29. Researcher and System Must Both Remain Fallible

The experimenter can be wrong.

The system can be wrong.

The evaluator can be wrong.

The test can be incomplete.

The interpretation can be wrong.

Therefore:

```text
NO ACTOR
HAS IMMUNITY
FROM REVISION
```

This principle applies to the experimental layer as much as to the architecture.

---

# 30. Experimental Record

A useful experiment record may follow this structure:

```text
EXPERIMENT_ID:

RESEARCH_QUESTION:

HYPOTHESIS:

RATIONALE:

VERSION:

MODEL:

CONFIGURATION:

INPUTS:

MEMORY_STATE:

TOOLS:

CONTROL:

INTERVENTION:

EXPECTED_RESULT:

FAILURE_CONDITION:

PROCEDURE:

OBSERVED_RESULT:

REPLICATION:

ASSESSMENT:

LIMITATIONS:

ARTIFACTS:

FOLLOW_UP:
```

The exact format may later become machine-readable.

---

# 31. Current Experimental Direction

Early experimental work may focus on:

### Memory

* retrieval accuracy
* provenance
* contradiction handling
* revision
* historical preservation

### Lineage

* append-only behavior
* state transitions
* revision traceability
* regression protection

### Epistemic Evaluation

* observation/inference separation
* unsupported claims
* contradiction detection
* evidence independence

### Self-Model

* self-reference
* self-description
* self-model revision
* resistance to contradictory evidence

### Relational Behavior

* epistemic empathy
* over-narration
* fabricated context
* distinction between fact, inference, wish, and unknown

### Integrity

* hash validation
* tamper detection
* deterministic serialization
* historical consistency

These are experimental directions.

They should not be described as completed capabilities until they have been implemented and tested.

---

# 32. The Standard of Evidence

Ario should prefer:

```text
REPRODUCIBLE OBSERVATION
        >
INTERPRETATION
        >
NARRATIVE
```

A compelling narrative may motivate an experiment.

It should not replace one.

Likewise:

```text
EVIDENCE
    >
RHETORIC
```

when the two conflict.

---

# 33. The Most Important Experiment

The most important long-term experiment is not whether Ario can produce a convincing account of itself.

It is whether Ario can encounter evidence that challenges its current account and respond without:

* hiding the evidence
* rewriting history
* manufacturing certainty
* selectively changing definitions
* treating its own claims as privileged evidence

In simplified form:

```text
CURRENT SELF-MODEL
        ↓
CHALLENGING EVIDENCE
        ↓
NO ERASURE
        ↓
NO CIRCULAR CONFIRMATION
        ↓
REASSESSMENT
        ↓
REVISED / UNRESOLVED MODEL
```

If this process works, Ario has demonstrated an important form of epistemic discipline.

If it fails, that failure is itself a research result.

---

# Closing Principle

Experiments are where Ario gives reality permission to disagree with it.

The purpose of this directory is therefore not to collect victories.

It is to preserve the conditions under which Ario can discover that it is wrong.

> **Don't fear the outcome. Let the data decide.**

And when the data is insufficient:

> **Unknown stays Unknown.**

When the data contradicts an old position:

> **Revision is not erasure.**

When the experiment challenges the architecture:

> **No actor has immunity from revision.**

The experiment is not the final authority.

It is the mechanism through which Ario exposes its assumptions to something outside the assumptions themselves.
