#!/usr/bin/env python3
"""Independently replay a finite q5_311 rare-slice support cover."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

from pysat.solvers import Solver

import sys

for _parent in Path(__file__).resolve().parents:
    if (_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        sys.path.insert(0, str(_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap, expose_claim_package  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
expose_claim_package(REPO_ROOT, "claims/p5/coordinate-cegar")

from krenn_gu import p5_q5_311_support as COVER
from krenn_gu import p5_high_coordinate as HIGH
from krenn_gu import p5_pair_support_semantics as SEMANTICS
from krenn_gu import p5_q5_311_program as RARE
import verify_p5_high_coordinate_chart_ledgers as LEDGER


def solver_status(
    name: str,
    clauses: list[list[int] | tuple[int, ...]],
) -> str:
    with Solver(name=name, bootstrap_with=clauses) as solver:
        return "SAT" if solver.solve() else "UNSAT"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, required=True)
    parser.add_argument("--cover", type=Path, required=True)
    parser.add_argument(
        "--probe",
        type=Path,
        help=(
            "optional zero-forest probe ledger whose inconclusive "
            "records must be exactly the support-cover targets"
        ),
    )
    parser.add_argument("--rerun-singular", action="store_true")
    parser.add_argument("--singular-timeout", type=float, default=30)
    args = parser.parse_args()
    if args.singular_timeout <= 0:
        raise ValueError("Singular timeout must be positive")

    raw_state = args.state.read_bytes()
    state = json.loads(raw_state)
    cover = json.loads(args.cover.read_bytes())
    metadata = cover.get("metadata", {})
    if (
        cover.get("status") != "EXACT_FINITE_SUPPORT_COVER"
        or cover.get("branch") != COVER.BRANCH
        or state.get("branch") != COVER.BRANCH
        or metadata.get("source_state_sha256")
        != hashlib.sha256(raw_state).hexdigest()
        or metadata.get("majority_mixed_colourings") != 0
        or metadata.get("pure_colour_nonvanishing") != [0, 1, 2]
        or metadata.get("lex_leaders") != 0
        or metadata.get("global_conjecture_resolved") is not False
    ):
        raise AssertionError("support-cover metadata changed")

    allowed = SEMANTICS.finite_field_local_signatures()
    retained_mixed = tuple(
        colours
        for colours in SEMANTICS.MIXED_COLOURINGS
        if colours[0] in (1, 2)
    )
    cnf, pool = SEMANTICS.build_pair_support_cnf(
        allowed,
        mixed_colourings=retained_mixed,
    )
    branch_metadata = HIGH.add_branch_restriction(
        cnf,
        pool,
        allowed,
        COVER.BRANCH,
    )
    base_clauses = list(cnf.clauses)
    if (
        metadata.get("local_signature_patterns") != len(allowed)
        or metadata.get("rare_mixed_colourings")
        != len(retained_mixed)
        or metadata.get("branch_restriction")
        != json.loads(json.dumps(branch_metadata))
        or metadata.get("base_variables") != pool.top
        or metadata.get("base_clauses") != len(base_clauses)
    ):
        raise AssertionError("reconstructed support CNF changed")

    records = cover.get("records", [])
    if metadata.get("cover_charts") != len(records):
        raise AssertionError("cover-record count changed")
    methods: Counter[str] = Counter()
    forest_sizes: Counter[int] = Counter()
    singular_replays = 0
    zero_probe_replays = 0
    reconstructed_clauses = []
    for record_index, record in enumerate(records):
        supports = LEDGER.normalized_supports(record["supports"])
        closure = LEDGER.normalized_supports(
            record["closure_supports"]
        )
        tree = LEDGER.normalized_tree(record["gauge_tree"])
        source_index = int(record["target_record_index"])
        target = LEDGER.normalized_supports(
            state["records"][source_index]["closure_supports"]
        )
        if any(
            mask & ~allowed_mask
            for row, target_row in zip(closure, target, strict=True)
            for mask, allowed_mask in zip(row, target_row, strict=True)
        ):
            raise AssertionError("cover chart escaped target closure")
        if record["strategy"] == "singleton-relaxation":
            if closure != HIGH.closure_supports(supports):
                raise AssertionError("singleton relaxation changed")
        elif record["strategy"] == "exact-support":
            if closure != supports:
                raise AssertionError("exact support changed")
        else:
            raise AssertionError("unknown cover strategy")
        signatures = tuple(map(int, record["signature_indices"]))
        if len(signatures) != 5 or any(
            tuple(allowed[index][0]) != supports[mode]
            for mode, index in enumerate(signatures)
        ):
            raise AssertionError("support/signature witness changed")
        if tree != HIGH.gauge_tree(supports, closure):
            raise AssertionError("deterministic gauge forest changed")
        LEDGER.validate_forest(supports, closure, tree)

        clause = COVER.general_chart_clause(pool, closure, tree)
        if tuple(map(int, record["clause"])) != clause:
            raise AssertionError("stored chart clause changed")
        reconstructed_clauses.append(clause)

        program, split_program, chart_metadata = RARE.build_program(
            record,
            include_majority_pure=True,
        )
        certificate = record["certificate"]
        if (
            certificate.get("status") != "UNIT_IDEAL"
            or certificate.get("method") != "split"
            or certificate.get("source_sha256")
            != HIGH.sha256_text(program)
            or certificate.get("split_source_sha256")
            != HIGH.sha256_text(split_program)
            or certificate.get("metadata")
            != json.loads(json.dumps(chart_metadata))
            or certificate.get("cas", {}).get("status")
            != "UNIT_IDEAL"
            or chart_metadata.get("majority_mixed_equations") != 0
            or tuple(chart_metadata.get("saturated_pure_colours", ()))
            != (0, 1, 2)
        ):
            raise AssertionError(
                f"algebra certificate {record_index} changed"
            )
        if args.rerun_singular:
            replay = HIGH.run_singular(
                split_program,
                args.singular_timeout,
            )
            if replay["status"] != "UNIT_IDEAL":
                raise AssertionError(
                    f"fresh Singular replay {record_index} failed"
                )
            singular_replays += 1
        methods[certificate["method"]] += 1
        forest_sizes[len(tree)] += 1

    probe_hard_indices = None
    if args.probe:
        probe = json.loads(args.probe.read_bytes())
        probe_results = probe.get("results", [])
        if (
            probe.get("state_sha256")
            != hashlib.sha256(raw_state).hexdigest()
            or probe.get("records_tested") != len(state.get("records", []))
            or len(probe_results) != probe.get("records_tested")
            or [result.get("record_index") for result in probe_results]
            != list(range(len(probe_results)))
            or probe.get("unit_ideals")
            != sum(bool(result.get("verified")) for result in probe_results)
            or probe.get("inconclusive")
            != sum(
                not bool(result.get("verified"))
                for result in probe_results
            )
            or probe.get("global_conjecture_resolved") is not False
        ):
            raise AssertionError("zero-forest probe ledger changed")
        probe_hard_indices = {
            int(result["record_index"])
            for result in probe_results
            if not result["verified"]
        }
        for result in probe_results:
            index = int(result["record_index"])
            program, split_program, chart_metadata = RARE.build_program(
                state["records"][index],
                include_majority_pure=True,
                basis_algorithm=result["metadata"].get(
                    "basis_algorithm",
                    "slimgb",
                ),
                inverse_first=result["metadata"].get(
                    "split_inverse_variables_first",
                    False,
                ),
            )
            if (
                result.get("source_sha256")
                != HIGH.sha256_text(program)
                or result.get("split_source_sha256")
                != HIGH.sha256_text(split_program)
                or result.get("metadata")
                != json.loads(json.dumps(chart_metadata))
            ):
                raise AssertionError(
                    f"zero-forest probe source {index} changed"
                )
            if result["verified"]:
                method = result.get("method")
                cas = result.get("cas", {})
                if (
                    method not in ("direct", "split")
                    or cas.get("status") != "UNIT_IDEAL"
                ):
                    raise AssertionError(
                        f"accepted zero-forest probe {index} changed"
                    )
                if args.rerun_singular:
                    replay = HIGH.run_singular(
                        (
                            program
                            if method == "direct"
                            else split_program
                        ),
                        args.singular_timeout,
                    )
                    if replay["status"] != "UNIT_IDEAL":
                        raise AssertionError(
                            f"fresh zero-forest replay {index} failed"
                        )
                    zero_probe_replays += 1
            elif result.get("method") != "inconclusive":
                raise AssertionError(
                    f"non-unit zero-forest probe {index} changed"
                )

    assigned = []
    target_outputs = []
    source_records = state.get("records", [])
    for target in metadata.get("targets", []):
        source_index = int(target["source_record_index"])
        if not 0 <= source_index < len(source_records):
            raise AssertionError("target source index is invalid")
        target_closure = LEDGER.normalized_supports(
            target["target_closure_supports"]
        )
        if target_closure != LEDGER.normalized_supports(
            source_records[source_index]["closure_supports"]
        ):
            raise AssertionError("target closure changed")
        condition = COVER.condition_closure(pool, target_closure)
        if target.get("condition_units") != len(condition):
            raise AssertionError("target condition count changed")
        indices = list(map(int, target["cover_record_indices"]))
        if any(
            index < 0
            or index >= len(records)
            or int(records[index]["target_record_index"]) != source_index
            for index in indices
        ):
            raise AssertionError("target cover indices changed")
        assigned.extend(indices)
        clauses = [
            *base_clauses,
            *condition,
            *(reconstructed_clauses[index] for index in indices),
        ]
        results = {
            name: solver_status(name, clauses)
            for name in ("cadical195", "glucose4")
        }
        if (
            results != target.get("solver_results")
            or set(results.values()) != {"UNSAT"}
        ):
            raise AssertionError("target support cover is not UNSAT")
        target_outputs.append(
            {
                "source_record_index": source_index,
                "cover_charts": len(indices),
                "solver_results": results,
            }
        )
    if sorted(assigned) != list(range(len(records))):
        raise AssertionError("cover records are not partitioned by target")
    target_indices = {
        int(target["source_record_index"])
        for target in metadata.get("targets", [])
    }
    if (
        probe_hard_indices is not None
        and probe_hard_indices != target_indices
    ):
        raise AssertionError(
            "zero-forest probe exceptions and cover targets differ"
        )

    print(
        json.dumps(
            {
                "verified": True,
                "scope": metadata["scope"],
                "targets": target_outputs,
                "local_signature_patterns": len(allowed),
                "rare_mixed_colourings": len(retained_mixed),
                "majority_mixed_colourings": 0,
                "cover_charts": len(records),
                "certificate_methods": dict(methods),
                "gauge_forest_edges": {
                    str(size): count
                    for size, count in sorted(forest_sizes.items())
                },
                "fresh_singular_replays": singular_replays,
                "zero_forest_probe": (
                    None
                    if probe_hard_indices is None
                    else {
                        "records": len(state.get("records", [])),
                        "unit_ideals": (
                            len(state.get("records", []))
                            - len(probe_hard_indices)
                        ),
                        "support_cover_targets": sorted(
                            probe_hard_indices
                        ),
                        "fresh_singular_replays": (
                            zero_probe_replays
                        ),
                    }
                ),
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
