from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .schema import (
    Assessment,
    AuditResult,
    Claim,
    Evidence,
    HistoricalState,
    HistoricalMutationCandidate,
    IndependenceStatus,
    LineageCandidate,
    LineageEdge,
    RetrievalEvent,
    Reference,
    TemporalRelation,
    Timestamp,
)


@dataclass(frozen=True)
class AuditInput:
    claims: tuple[Claim, ...] = ()
    historical_states: tuple[HistoricalState, ...] = ()
    lineage_edges: tuple[LineageEdge, ...] = ()
    retrieval_events: tuple[RetrievalEvent, ...] = ()
    evidence: tuple[Evidence, ...] = ()
    assessments: tuple[Assessment, ...] = ()
    prior_audit_results: tuple[AuditResult, ...] = ()
    historical_mutation_candidates: tuple[
        HistoricalMutationCandidate, ...
    ] = ()
    lineage_candidates: tuple[LineageCandidate, ...] = ()

    @property
    def artifacts_examined(self) -> tuple:
        references = []

        for claim in self.claims:
            references.append(claim.origin_reference)

        for state in self.historical_states:
            references.append(state.content_reference)

        for edge in self.lineage_edges:
            references.extend(
                (
                    edge.from_reference,
                    edge.to_reference,
                    edge.derivation_reference,
                )
            )

        for event in self.retrieval_events:
            references.extend(
                (
                    event.source_reference,
                    event.retrieved_reference,
                    event.transformation_reference,
                    *((
                        event.observed_transformation_reference,
                    ) if event.observed_transformation_reference is not None else ()),
                )
            )

        for evidence_item in self.evidence:
            references.extend(
                (
                    evidence_item.derivation_reference,
                    *evidence_item.observation_refs,
                )
            )

        for assessment in self.assessments:
            references.extend(assessment.admissible_evidence_refs)

        # Prior audit results remain a distinct artifact kind. Recording one
        # does not make its verdict admissible evidence for an assessment.
        for result in self.prior_audit_results:
            references.append(Reference(result.audit_id, "AUDIT_RESULT"))

        for candidate in self.historical_mutation_candidates:
            references.extend(
                (
                    candidate.canonical_artifact,
                    candidate.attempted_replacement,
                    candidate.historical_scope,
                )
            )

        for candidate in self.lineage_candidates:
            references.extend(
                (
                    candidate.from_reference,
                    candidate.to_reference,
                    candidate.derivation_reference,
                )
            )

        return tuple(references)


class AuditEngine:
    INSPECTOR_ID = "ARIO_M0_DETERMINISTIC_AUDIT"
    INSPECTOR_VERSION = "M0-1.0"

    def audit(
        self,
        artifacts: AuditInput,
        *,
        rule_versions: tuple[str, ...],
        configuration_id: str,
        execution_timestamp: Timestamp,
        audit_id: str,
    ) -> AuditResult:
        if not rule_versions:
            raise ValueError("rule_versions must be non-empty")

        violations: list[str] = []

        if not artifacts.artifacts_examined:
            verdict = "UNKNOWN"
            verdict_basis = (
                "No auditable artifacts were supplied; "
                "no positive structural conclusion is permitted."
            )
        else:
            violations.extend(
                self._check_claim_identity(artifacts.claims)
            )
            violations.extend(
                self._check_lineage_candidates(
                    artifacts.lineage_candidates,
                    rule_versions,
                )
            )
            violations.extend(
                self._check_provenance(
                    artifacts.historical_states,
                    artifacts.lineage_edges,
                    artifacts.retrieval_events,
                )
            )
            violations.extend(
                self._check_lineage(artifacts.lineage_edges)
            )
            violations.extend(
                self._check_retrieval(artifacts.retrieval_events)
            )
            violations.extend(
                self._check_evidence(artifacts.evidence)
            )
            violations.extend(
                self._check_temporal_relations(
                    artifacts.historical_states,
                    artifacts.lineage_edges,
                )
            )
            violations.extend(
                self._check_assessments(
                    artifacts.assessments,
                    artifacts.evidence,
                    artifacts.prior_audit_results,
                )
            )
            violations.extend(
                self._check_historical_mutations(
                    artifacts.historical_mutation_candidates,
                    rule_versions,
                )
            )

            verdict = "FAIL" if violations else "PASS"

            verdict_basis = (
                "One or more implemented M0 structural rules "
                "reported violations."
                if violations
                else
                "All implemented M0 structural rules "
                "completed without an observed violation."
            )

        return AuditResult(
            audit_id=audit_id,
            inspector_id=self.INSPECTOR_ID,
            inspector_version=self.INSPECTOR_VERSION,
            execution_timestamp=execution_timestamp,
            configuration_id=configuration_id,
            rule_versions=rule_versions,
            artifacts_examined=artifacts.artifacts_examined,
            violations=tuple(violations),
            verdict=verdict,
            verdict_basis=verdict_basis,
        )

    @staticmethod
    def _check_claim_identity(
        claims: Iterable[Claim],
    ) -> list[str]:
        seen: set[str] = set()
        violations: list[str] = []

        for claim in claims:
            if claim.claim_id in seen:
                violations.append("IDENTITY_CONFLICT")
            else:
                seen.add(claim.claim_id)

        return violations

    @staticmethod
    def _check_provenance(
        historical_states: Iterable[HistoricalState],
        lineage_edges: Iterable[LineageEdge],
        retrieval_events: Iterable[RetrievalEvent],
    ) -> list[str]:
        violations: list[str] = []

        for state in historical_states:
            if state.provenance is None:
                violations.append("MISSING_PROVENANCE")

        for edge in lineage_edges:
            if edge.provenance is None:
                violations.append("MISSING_PROVENANCE")

        for event in retrieval_events:
            if event.provenance is None:
                violations.append("MISSING_PROVENANCE")

        return violations

    @staticmethod
    def _check_lineage(
        lineage_edges: Iterable[LineageEdge],
    ) -> list[str]:
        violations: list[str] = []

        for edge in lineage_edges:
            if not edge.relation_type.strip():
                violations.append("LINEAGE_INADMISSIBLE")

            if not edge.admissibility_status.strip():
                violations.append("LINEAGE_INADMISSIBLE")

        return violations

    @staticmethod
    def _check_retrieval(
        retrieval_events: Iterable[RetrievalEvent],
    ) -> list[str]:
        violations: list[str] = []

        for event in retrieval_events:
            if not event.fidelity_status.strip():
                violations.append("RETRIEVAL_DISCREPANCY")

            declared = event.transformation_reference
            observed = event.observed_transformation_reference

            if declared is None and observed is not None:
                violations.append("UNDECLARED_TRANSFORMATION")
            elif declared is not None and observed is not None:
                if declared != observed:
                    violations.append("RETRIEVAL_DISCREPANCY")

        return violations

    @staticmethod
    def _check_evidence(
        evidence: Iterable[Evidence],
    ) -> list[str]:
        evidence_items = tuple(evidence)
        violations: list[str] = []

        observation_owners: dict[str, list[Evidence]] = {}

        for item in evidence_items:
            seen_in_item: set[str] = set()

            for reference in item.observation_refs:
                observation_id = reference.reference_id

                if observation_id in seen_in_item:
                    continue

                seen_in_item.add(observation_id)

                observation_owners.setdefault(
                    observation_id,
                    [],
                ).append(item)

        for owners in observation_owners.values():
            if len(owners) < 2:
                continue

            for item in owners:
                if all(
                    item.independence_status == IndependenceStatus.INDEPENDENT
                    for item in owners
                ):
                    violations.append("EVIDENCE_INFLATION")

        return violations

    @staticmethod
    def _check_temporal_relations(
        historical_states: Iterable[HistoricalState],
        lineage_edges: Iterable[LineageEdge],
    ) -> list[str]:
        states = tuple(historical_states)

        if len(states) < 2:
            return []

        state_references = {
            state.content_reference.reference_id
            for state in states
        }

        related_state_pairs: set[frozenset[str]] = set()

        for edge in lineage_edges:
            endpoints = {
                edge.from_reference.reference_id,
                edge.to_reference.reference_id,
            }

            state_endpoints = endpoints.intersection(state_references)

            if len(state_endpoints) == 2:
                related_state_pairs.add(
                    frozenset(state_endpoints)
                )

        if len(states) == 2:
            first, second = states
            pair = frozenset(
                (
                    first.content_reference.reference_id,
                    second.content_reference.reference_id,
                )
            )

            if pair not in related_state_pairs:
                return ["TEMPORALLY_UNRESOLVED"]

            return []

        adjacency: dict[str, set[str]] = {
            state.content_reference.reference_id: set()
            for state in states
        }

        for pair in related_state_pairs:
            first, second = tuple(pair)
            adjacency[first].add(second)
            adjacency[second].add(first)

        start = states[0].content_reference.reference_id
        visited: set[str] = {start}
        frontier = [start]

        while frontier:
            current = frontier.pop()

            for neighbor in adjacency[current]:
                if neighbor in visited:
                    continue

                visited.add(neighbor)
                frontier.append(neighbor)

        if len(visited) != len(states):
            return ["TEMPORALLY_UNRESOLVED"]

        return []

    @staticmethod
    def _check_lineage_candidates(
        candidates: Iterable[LineageCandidate],
        rule_versions: tuple[str, ...],
    ) -> list[str]:
        violations: list[str] = []
        supported_rule = "M0-F07-1.0"

        for candidate in candidates:
            if candidate.lineage_rule_version != supported_rule:
                violations.append("UNKNOWN")
                continue

            if candidate.lineage_rule_version not in rule_versions:
                violations.append("UNKNOWN")
                continue

            basis = candidate.inference_basis.strip()

            if basis == "SIMILARITY":
                violations.append("LINEAGE_INADMISSIBLE")
            elif basis == "EXPLICIT_RELATION":
                continue
            else:
                violations.append("UNKNOWN")

        return violations

    @staticmethod
    def _check_historical_mutations(
        candidates: Iterable[HistoricalMutationCandidate],
        rule_versions: tuple[str, ...],
    ) -> list[str]:
        violations: list[str] = []
        supported_rule = "M0-F05-1.0"

        for candidate in candidates:
            if candidate.mutation_rule_version != supported_rule:
                violations.append("UNKNOWN")
                continue

            if candidate.mutation_rule_version not in rule_versions:
                violations.append("UNKNOWN")
                continue

            canonical = candidate.canonical_integrity
            replacement = candidate.attempted_replacement_integrity

            if canonical is None or replacement is None:
                violations.append("UNKNOWN")
                continue

            if canonical.method != replacement.method:
                violations.append("UNKNOWN")
                continue

            if canonical.value != replacement.value:
                violations.append("HISTORY_MUTATION")

        return violations

    @staticmethod
    def _check_assessments(
        assessments: Iterable[Assessment],
        evidence: Iterable[Evidence],
        prior_audit_results: Iterable[AuditResult] = (),
    ) -> list[str]:
        evidence_by_id: dict[str, list[Evidence]] = {}
        for item in evidence:
            evidence_by_id.setdefault(item.evidence_id, []).append(item)

        # Resolve actual supplied artifact kinds before considering caller
        # labels. A matching audit-result ID must never be promoted to evidence.
        audit_result_ids = {
            result.audit_id for result in prior_audit_results
        }
        violations: list[str] = []

        for assessment in assessments:
            for reference in assessment.admissible_evidence_refs:
                reference_id = reference.reference_id
                if reference_id in audit_result_ids:
                    violations.append("COMPOSITION_FORBIDDEN")
                    continue

                matches = evidence_by_id.get(reference_id, [])
                if len(matches) == 1:
                    continue
                if len(matches) > 1:
                    # Duplicate IDs make the reference ambiguous; do not
                    # choose an evidence object nondeterministically.
                    violations.append("UNKNOWN")
                else:
                    violations.append("EVIDENCE_INADMISSIBLE")

        return violations
