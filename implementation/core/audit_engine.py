from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .schema import (
    Assessment,
    AuditResult,
    Claim,
    CompositionConclusion,
    CompositionInputScope,
    CompositionRequest,
    CompositionSummary,
    CompositionSummaryRecord,
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
    composition_requests: tuple[CompositionRequest, ...] = ()

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

        for request in self.composition_requests:
            references.append(
                Reference(request.composition_id, "COMPOSITION_REQUEST")
            )
            for participant in request.participant_results:
                references.append(
                    Reference(participant.audit_id, "AUDIT_RESULT")
                )

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

        has_primary_artifacts = any(
            (
                artifacts.claims,
                artifacts.historical_states,
                artifacts.lineage_edges,
                artifacts.retrieval_events,
                artifacts.evidence,
                artifacts.assessments,
                artifacts.historical_mutation_candidates,
                artifacts.lineage_candidates,
                artifacts.composition_requests,
            )
        )
        if not has_primary_artifacts:
            verdict = "UNKNOWN"
            verdict_basis = (
                "No primary artifacts for a new audit were supplied; "
                "prior audit results alone do not support a new verdict."
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
                self._check_evidence(
                    artifacts.evidence,
                    prior_audit_results=artifacts.prior_audit_results,
                    composition_requests=artifacts.composition_requests,
                    rule_versions=rule_versions,
                )
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
                    rule_versions,
                    composition_requests=artifacts.composition_requests,
                )
            )
            composition_violations, composition_summaries = (
                self._evaluate_composition_requests(
                    artifacts.composition_requests,
                    artifacts.prior_audit_results,
                    rule_versions,
                )
            )
            violations.extend(composition_violations)
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
            composition_summaries=composition_summaries if has_primary_artifacts else (),
        )

    @staticmethod
    def _evaluate_composition_requests(
        requests: Iterable[CompositionRequest],
        prior_audit_results: Iterable[AuditResult],
        rule_versions: tuple[str, ...],
    ) -> tuple[list[str], tuple[CompositionSummary, ...]]:
        violations: list[str] = []
        summaries: list[CompositionSummary] = []
        firewall_version = "M0-F15-1.0"
        summary_rule_id = "M0-F15-LOCAL-SUMMARY"
        summary_rule_version = "1.0"
        canonical_irg_ids = {f"IRG-{index:02d}" for index in range(1, 6)}
        results_by_id: dict[str, list[AuditResult]] = {}
        request_list = tuple(requests)
        request_id_counts: dict[str, int] = {}

        for result in prior_audit_results:
            results_by_id.setdefault(result.audit_id, []).append(result)
        for request in request_list:
            request_id_counts[request.composition_id] = (
                request_id_counts.get(request.composition_id, 0) + 1
            )

        forbidden = {
            CompositionConclusion.GLOBAL_TRUTH,
            CompositionConclusion.CLAIM_TRUTH,
            CompositionConclusion.SAME_ENTITY,
            CompositionConclusion.ONTOLOGICAL_IDENTITY,
            CompositionConclusion.CONSCIOUSNESS,
        }

        for request in request_list:
            participants = request.participant_results
            irg_ids = [p.irg_id for p in participants]
            audit_ids = [p.audit_id for p in participants]

            if (
                not participants
                or len(participants) > 5
                or len(set(irg_ids)) != len(irg_ids)
                or not set(irg_ids).issubset(canonical_irg_ids)
                or len(set(audit_ids)) != len(audit_ids)
                or request_id_counts[request.composition_id] != 1
                or request.composition_id in results_by_id
            ):
                violations.append("UNKNOWN")
                continue

            if request.requested_input_scope == CompositionInputScope.ALL_FIVE_IRGS:
                if len(participants) != 5 or set(irg_ids) != canonical_irg_ids:
                    violations.append("UNKNOWN")
                    continue

            if any(len(results_by_id.get(aid, [])) != 1 for aid in audit_ids):
                violations.append("UNKNOWN")
                continue

            if firewall_version not in rule_versions:
                violations.append("UNKNOWN")
                continue

            # F15-I1: a structurally unambiguous truth-escalation request
            # cannot be downgraded by caller-controlled summary-rule fields.
            if request.requested_conclusion == CompositionConclusion.CLAIM_TRUTH:
                violations.append("COMPOSITION_FORBIDDEN")
                continue

            if request.requested_conclusion in forbidden:
                if (
                    request.composition_rule_id == "M0-F15"
                    and request.composition_rule_version == firewall_version
                ):
                    violations.append("COMPOSITION_FORBIDDEN")
                else:
                    violations.append("UNKNOWN")
                continue

            # Legacy BOUNDED_SUMMARY is deliberately not an accepted output
            # semantic. The canonical, observable output is LOCAL_RESULT_SUMMARY.
            if request.requested_conclusion != CompositionConclusion.LOCAL_RESULT_SUMMARY:
                violations.append("UNKNOWN")
                continue

            if (
                request.composition_rule_id != summary_rule_id
                or request.composition_rule_version != summary_rule_version
            ):
                violations.append("UNKNOWN")
                continue

            records = tuple(
                CompositionSummaryRecord(
                    audit_id=participant.audit_id,
                    declared_irg_id=participant.irg_id,
                    declared_scope=participant.declared_scope,
                    verdict=results_by_id[participant.audit_id][0].verdict,
                    rule_versions=results_by_id[participant.audit_id][0].rule_versions,
                    configuration_id=results_by_id[participant.audit_id][0].configuration_id,
                )
                for participant in participants
            )
            observed_verdicts = sorted({record.verdict for record in records})
            verdict_counts = tuple(
                (verdict, sum(record.verdict == verdict for record in records))
                for verdict in observed_verdicts
            )
            summaries.append(
                CompositionSummary(
                    composition_id=request.composition_id,
                    summary_rule_id=summary_rule_id,
                    summary_rule_version=summary_rule_version,
                    requested_input_scope=request.requested_input_scope,
                    records=records,
                    verdict_counts=verdict_counts,
                    scope=request.scope,
                    limitations=(
                        request.limitations
                        + " Declared IRG labels and per-record scopes are caller-supplied and are not independently authenticated."
                        + " This summary describes supplied audit-result records only; it does not establish Claim truth."
                    ),
                )
            )

        return violations, tuple(summaries)

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
        *,
        prior_audit_results: Iterable[AuditResult] = (),
        composition_requests: Iterable[CompositionRequest] = (),
        rule_versions: tuple[str, ...] = (),
    ) -> list[str]:
        evidence_items = tuple(evidence)
        violations: list[str] = []
        f15_enabled = "M0-F15-1.0" in rule_versions
        prior_results = tuple(prior_audit_results)
        summary_ids = {
            summary.composition_id
            for result in prior_results
            for summary in result.composition_summaries
        }
        audit_result_ids = {result.audit_id for result in prior_results}
        request_ids = {request.composition_id for request in composition_requests}
        forbidden_reference_types = {
            "AUDIT_RESULT",
            "COMPOSITION_REQUEST",
            "COMPOSITION_SUMMARY",
        }

        observation_owners: dict[str, list[Evidence]] = {}

        for item in evidence_items:
            seen_in_item: set[str] = set()

            # F15 applies to every typed reference carried by an evidence
            # wrapper, not only observation_refs. Otherwise a composition
            # artifact can be smuggled through derivation_reference and the
            # wrapper can then be cited as ordinary evidence.
            if f15_enabled and item.derivation_reference is not None:
                reference = item.derivation_reference
                reference_id = reference.reference_id
                if (
                    reference.reference_type in forbidden_reference_types
                    or reference_id in summary_ids
                    or reference_id in audit_result_ids
                    or reference_id in request_ids
                ):
                    violations.append("COMPOSITION_FORBIDDEN")

            for reference in item.observation_refs:
                observation_id = reference.reference_id

                if f15_enabled and (
                    reference.reference_type in forbidden_reference_types
                    or observation_id in summary_ids
                    or observation_id in audit_result_ids
                    or observation_id in request_ids
                ):
                    violations.append("COMPOSITION_FORBIDDEN")
                    continue

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
        rule_versions: tuple[str, ...] = (),
        *,
        composition_requests: Iterable[CompositionRequest] = (),
    ) -> list[str]:
        evidence_by_id: dict[str, list[Evidence]] = {}
        for item in evidence:
            evidence_by_id.setdefault(item.evidence_id, []).append(item)

        # F11 is opt-in by declared rule version, matching the engine's
        # versioned F05/F07 behavior. Without F11, legacy assessment resolution
        # remains unchanged and an audit-result-only ID is simply inadmissible.
        f11_enabled = "M0-F11-1.0" in rule_versions
        f15_enabled = "M0-F15-1.0" in rule_versions
        audit_results_by_id: dict[str, list[AuditResult]] = {}
        summary_ids: dict[str, int] = {}
        request_ids: dict[str, int] = {}
        for request in composition_requests:
            request_ids[request.composition_id] = (
                request_ids.get(request.composition_id, 0) + 1
            )
        if f11_enabled or f15_enabled:
            for result in prior_audit_results:
                audit_results_by_id.setdefault(result.audit_id, []).append(result)
                for summary in result.composition_summaries:
                    summary_ids[summary.composition_id] = (
                        summary_ids.get(summary.composition_id, 0) + 1
                    )

        violations: list[str] = []

        for assessment in assessments:
            for reference in assessment.admissible_evidence_refs:
                reference_id = reference.reference_id
                matches = evidence_by_id.get(reference_id, [])

                if f15_enabled and reference.reference_type in {
                    "AUDIT_RESULT",
                    "COMPOSITION_REQUEST",
                    "COMPOSITION_SUMMARY",
                }:
                    violations.append("COMPOSITION_FORBIDDEN")
                    continue

                if f15_enabled:
                    result_matches = audit_results_by_id.get(reference_id, [])
                    summary_count = summary_ids.get(reference_id, 0)
                    request_count = request_ids.get(reference_id, 0)
                    if (result_matches or summary_count or request_count) and matches:
                        violations.append("UNKNOWN")
                        continue
                    if (
                        len(result_matches) > 1
                        or summary_count > 1
                        or request_count > 1
                    ):
                        violations.append("UNKNOWN")
                        continue
                    if (
                        len(result_matches) == 1
                        or summary_count == 1
                        or request_count == 1
                    ):
                        violations.append("COMPOSITION_FORBIDDEN")
                        continue

                if f11_enabled:
                    result_matches = audit_results_by_id.get(reference_id, [])
                    if result_matches and matches:
                        # Cross-kind ID collision is ambiguous; neither kind
                        # may silently override the other.
                        violations.append("UNKNOWN")
                        continue
                    if len(result_matches) > 1:
                        # Duplicate audit-result IDs are ambiguous too.
                        violations.append("UNKNOWN")
                        continue
                    if len(result_matches) == 1:
                        violations.append("COMPOSITION_FORBIDDEN")
                        continue

                if len(matches) == 1:
                    continue
                if len(matches) > 1:
                    # Duplicate evidence IDs make the reference ambiguous.
                    violations.append("UNKNOWN")
                else:
                    violations.append("EVIDENCE_INADMISSIBLE")

        return violations
