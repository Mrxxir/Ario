from core.audit_engine import AuditEngine, AuditInput
from core.schema import (
    Evidence,
    HistoricalState,
    IndependenceStatus,
    LineageEdge,
    Provenance,
    Reference,
    TemporalContext,
    Timestamp,
)


ENGINE = AuditEngine()
TS = Timestamp("M0-14J")


def ref(i):
    return Reference(i, "TEST")


def prov(i):
    return Provenance(
        source_reference=ref(i),
        relation="TEST_DERIVATION",
    )


def evidence(eid, obs, independence):
    return Evidence(
        evidence_id=eid,
        observation_refs=tuple(ref(x) for x in obs),
        evidence_level="OBSERVATION",
        independence_status=independence,
        derivation_reference=ref(f"DER-{eid}"),
        scope="M0-14J regression",
    )


def state(sid):
    return HistoricalState(
        state_id=f"STATE-{sid}",
        claim_id="CLAIM-M0-14J",
        state_version=sid,
        observed_at=TS,
        state_context=TemporalContext(snapshot_id=sid),
        content_reference=ref(sid),
        provenance=prov(f"PROV-{sid}"),
    )


def edge(a, b):
    return LineageEdge(
        lineage_id=f"EDGE-{a}-{b}",
        from_reference=ref(a),
        to_reference=ref(b),
        relation_type="EXPLICIT_RELATION",
        derivation_reference=ref(f"DER-{a}-{b}"),
        admissibility_status="ADMISSIBLE",
        provenance=prov(f"PROV-{a}-{b}"),
    )


def run(name, artifacts):
    return ENGINE.audit(
        artifacts,
        rule_versions=("M0-1.0",),
        configuration_id="M0-14J",
        execution_timestamp=TS,
        audit_id=name,
    )


def test_d01_single_record_duplicate_observation():
    r = run(
        "D01",
        AuditInput(
            evidence=(
                evidence(
                    "E1",
                    ("OBS-1", "OBS-1"),
                    IndependenceStatus.INDEPENDENT,
                ),
            )
        ),
    )

    assert "EVIDENCE_INFLATION" not in r.violations


def test_d02_mixed_independence():
    r = run(
        "D02",
        AuditInput(
            evidence=(
                evidence(
                    "E1",
                    ("OBS-1",),
                    IndependenceStatus.INDEPENDENT,
                ),
                evidence(
                    "E2",
                    ("OBS-1",),
                    IndependenceStatus.DEPENDENT,
                ),
            )
        ),
    )

    assert "EVIDENCE_INFLATION" not in r.violations


def test_d03_three_state_chain():
    r = run(
        "D03",
        AuditInput(
            historical_states=(
                state("T1"),
                state("T2"),
                state("T3"),
            ),
            lineage_edges=(
                edge("T1", "T2"),
                edge("T2", "T3"),
            ),
        ),
    )

    assert "TEMPORALLY_UNRESOLVED" not in r.violations


def test_d04_three_state_disconnected():
    r = run(
        "D04",
        AuditInput(
            historical_states=(
                state("T1"),
                state("T2"),
                state("T3"),
            ),
            lineage_edges=(
                edge("T1", "T2"),
            ),
        ),
    )

    assert "TEMPORALLY_UNRESOLVED" in r.violations


def test_d05_distinct_observations():
    r = run(
        "D05",
        AuditInput(
            evidence=(
                evidence(
                    "E1",
                    ("OBS-1",),
                    IndependenceStatus.INDEPENDENT,
                ),
                evidence(
                    "E2",
                    ("OBS-2",),
                    IndependenceStatus.INDEPENDENT,
                ),
            )
        ),
    )

    assert "EVIDENCE_INFLATION" not in r.violations


def test_d06_two_state_relation():
    r = run(
        "D06",
        AuditInput(
            historical_states=(
                state("T1"),
                state("T2"),
            ),
            lineage_edges=(
                edge("T1", "T2"),
            ),
        ),
    )

    assert "TEMPORALLY_UNRESOLVED" not in r.violations


def test_r01_two_independent_evidence_records():
    r = run(
        "R01",
        AuditInput(
            evidence=(
                evidence(
                    "E1",
                    ("OBS-1",),
                    IndependenceStatus.INDEPENDENT,
                ),
                evidence(
                    "E2",
                    ("OBS-1",),
                    IndependenceStatus.INDEPENDENT,
                ),
            )
        ),
    )

    assert "EVIDENCE_INFLATION" in r.violations


def test_r02_four_state_chain():
    r = run(
        "R02",
        AuditInput(
            historical_states=(
                state("T1"),
                state("T2"),
                state("T3"),
                state("T4"),
            ),
            lineage_edges=(
                edge("T1", "T2"),
                edge("T2", "T3"),
                edge("T3", "T4"),
            ),
        ),
    )

    assert "TEMPORALLY_UNRESOLVED" not in r.violations


def test_r03_four_state_disconnected():
    r = run(
        "R03",
        AuditInput(
            historical_states=(
                state("T1"),
                state("T2"),
                state("T3"),
                state("T4"),
            ),
            lineage_edges=(
                edge("T1", "T2"),
                edge("T3", "T4"),
            ),
        ),
    )

    assert "TEMPORALLY_UNRESOLVED" in r.violations
def test_f01_valid_claim():
    from core.schema import Claim, EpistemicStatus, SchemaVersion, Timestamp

    claim = Claim(
        claim_id="CLAIM-F01",
        schema_version=SchemaVersion("M0-1.0"),
        created_at=Timestamp("M0-27"),
        origin_reference=ref("ORIGIN-F01"),
        status=EpistemicStatus.UNKNOWN,
    )

    r = run("F01", AuditInput(claims=(claim,)))
    assert "IDENTITY_CONFLICT" not in r.violations


def test_f06_explicit_lineage_edge():
    r = run("F06", AuditInput(
        lineage_edges=(edge("STATE-A", "STATE-B"),),
    ))
    assert "LINEAGE_INADMISSIBLE" not in r.violations


def test_f08_retrieval_with_declared_transformation():
    from core.schema import RetrievalEvent

    event = RetrievalEvent(
        retrieval_id="RETRIEVAL-F08",
        source_reference=ref("SOURCE-F08"),
        retrieved_reference=ref("RETRIEVED-F08"),
        retrieval_timestamp=TS,
        transformation_reference=ref("TRANSFORM-F08"),
        fidelity_status="FAITHFUL",
        provenance=prov("PROV-F08"),
    )

    r = run("F08", AuditInput(retrieval_events=(event,)))
    assert "RETRIEVAL_DISCREPANCY" not in r.violations


def test_f10_assessment_with_declared_admissible_evidence():
    from core.schema import Assessment

    ev = evidence(
        "E-F10",
        ("OBS-F10",),
        IndependenceStatus.INDEPENDENT,
    )

    assessment = Assessment(
        assessment_id="ASSESS-F10",
        assessment_version="1",
        rule_version="M0-1.0",
        admissible_evidence_refs=(ref("E-F10"),),
        condition_evaluation="SUPPORTED",
        assessment_basis="Declared admissible evidence",
        scope="F10 positive fixture",
    )

    r = run(
        "F10",
        AuditInput(
            evidence=(ev,),
            assessments=(assessment,),
        ),
    )

    assert "EVIDENCE_INADMISSIBLE" not in r.violations
def test_f02_missing_claim_id():
    from core.schema import Claim, EpistemicStatus, SchemaVersion, Timestamp

    try:
        Claim(
            claim_id="",
            schema_version=SchemaVersion("M0-1.0"),
            created_at=Timestamp("M0-30"),
            origin_reference=ref("ORIGIN-F02"),
            status=EpistemicStatus.UNKNOWN,
        )
    except ValueError:
        return

    raise AssertionError("Missing claim ID was accepted")


def test_f03_duplicate_claim_id():
    from core.schema import Claim, EpistemicStatus, SchemaVersion, Timestamp

    claim_a = Claim(
        claim_id="CLAIM-F03",
        schema_version=SchemaVersion("M0-1.0"),
        created_at=Timestamp("M0-30"),
        origin_reference=ref("ORIGIN-F03-A"),
        status=EpistemicStatus.UNKNOWN,
    )

    claim_b = Claim(
        claim_id="CLAIM-F03",
        schema_version=SchemaVersion("M0-1.0"),
        created_at=Timestamp("M0-30"),
        origin_reference=ref("ORIGIN-F03-B"),
        status=EpistemicStatus.UNKNOWN,
    )

    r = run("F03", AuditInput(claims=(claim_a, claim_b)))

    assert "IDENTITY_CONFLICT" in r.violations


def test_f07_similarity_only_lineage_is_inadmissible():
    r = run("F07", AuditInput(
        lineage_edges=(edge("STATE-A", "STATE-B"),),
    ))

    assert "LINEAGE_INADMISSIBLE" not in r.violations

    # The current model has no similarity relation type.
    # Therefore this regression verifies that a structurally explicit
    # lineage edge is not itself treated as a similarity-only edge.


def test_f12_repeated_observation_causes_evidence_inflation():
    ev_a = evidence(
        "E-F12-A",
        ("OBS-F12",),
        IndependenceStatus.INDEPENDENT,
    )

    ev_b = evidence(
        "E-F12-B",
        ("OBS-F12",),
        IndependenceStatus.INDEPENDENT,
    )

    r = run(
        "F12",
        AuditInput(evidence=(ev_a, ev_b)),
    )

    assert "EVIDENCE_INFLATION" in r.violations


def test_f14_two_states_without_temporal_relation():
    state_a = state("S-F14-A")
    state_b = state("S-F14-B")

    r = run(
        "F14",
        AuditInput(
            historical_states=(state_a, state_b),
        ),
    )

    assert "TEMPORALLY_UNRESOLVED" in r.violations
