#!/usr/bin/env python3
"""Independently reconstruct a global or profile-sliced rare CEGAR ledger."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from pysat.card import CardEnc, EncType
from pysat.solvers import Solver

import sys

for _parent in Path(__file__).resolve().parents:
    if (_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        sys.path.insert(0, str(_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__, also=["."])

from krenn_gu import p5_q5_311_support as COVER
from krenn_gu import p5_support_system as GENERATOR
from krenn_gu.p5_split_saturation import convert_text
from krenn_gu import p5_high_coordinate as HIGH
from krenn_gu import p5_pair_support_semantics as SEMANTICS
from krenn_gu import p5_q5_311_program as RARE
import verify_p5_high_coordinate_chart_ledgers as LEDGER


BRANCH = "q5_311"
STRONG_SUBSUMER_MAX_LITERALS = 10


def add_coordinate_profile_restriction(
    cnf,
    pool,
    profile: tuple[int, ...],
) -> int:
    """Independently rebuild exact per-mode singleton counts."""
    clauses_before = len(cnf.clauses)
    for mode, bound in enumerate(profile):
        literals = [
            pool.id(("singleton", mode, source, colour))
            for source in SEMANTICS.SOURCES
            for colour in SEMANTICS.COLOURS
        ]
        cnf.extend(
            CardEnc.equals(
                lits=literals,
                bound=bound,
                vpool=pool,
                encoding=EncType.seqcounter,
            ).clauses
        )
    return len(cnf.clauses) - clauses_before


def remove_strongly_subsumed_clauses(
    clauses: tuple[tuple[int, ...], ...],
) -> tuple[tuple[tuple[int, ...], ...], dict]:
    """Independently remove clauses implied by short exact clauses."""
    strong_clauses = tuple(
        clause
        for clause in clauses
        if len(clause) <= STRONG_SUBSUMER_MAX_LITERALS
    )
    by_first_literal = defaultdict(list)
    for clause in strong_clauses:
        if not clause:
            raise AssertionError("empty chart clause")
        by_first_literal[clause[0]].append(frozenset(clause))

    retained = []
    removed = 0
    for clause in clauses:
        if len(clause) <= STRONG_SUBSUMER_MAX_LITERALS:
            retained.append(clause)
            continue
        clause_set = frozenset(clause)
        if any(
            strong_clause.issubset(clause_set)
            for literal in clause
            for strong_clause in by_first_literal.get(literal, ())
        ):
            removed += 1
        else:
            retained.append(clause)
    return tuple(retained), {
        "max_subsumer_literals": STRONG_SUBSUMER_MAX_LITERALS,
        "strong_clauses": len(strong_clauses),
        "removed_clauses": removed,
        "retained_clauses": len(retained),
    }


def normalized_json(value):
    return json.loads(json.dumps(value))


def validate_record(
    record: dict,
    pool,
) -> tuple[str, tuple[tuple[int, ...], ...], str]:
    supports = LEDGER.normalized_supports(record["supports"])
    closure = LEDGER.normalized_supports(record["closure_supports"])
    tree = LEDGER.normalized_tree(record["gauge_tree"])
    LEDGER.validate_forest(supports, closure, tree)
    if closure[0] != HIGH.BRANCH_BACKBONES[BRANCH]:
        raise AssertionError("record left normalized q5_311")
    certificate = record.get("certificate", {})
    equation_scope = record.get("equation_scope", "rare")
    if equation_scope == "rare":
        program, split_program, metadata = RARE.build_program(
            record,
            include_majority_pure=True,
            basis_algorithm=certificate.get("metadata", {}).get(
                "basis_algorithm",
                "slimgb",
            ),
            inverse_first=certificate.get("metadata", {}).get(
                "split_inverse_variables_first",
                False,
            ),
        )
        scope_metadata_valid = (
            metadata.get("majority_mixed_equations") == 0
            and tuple(metadata.get("saturated_pure_colours", ()))
            == (0, 1, 2)
        )
    elif equation_scope == "full":
        indices = tuple(map(int, record["signature_indices"]))
        program, metadata = GENERATOR.generate(
            closure,
            indices,
            expected_partial_cells=0,
            pure_saturation_only=True,
            gauge_tree_edges=tree,
            allow_arbitrary_support=True,
        )
        split_program = convert_text(program)
        scope_metadata_valid = metadata.get("pure_coefficients") == 3
    else:
        raise AssertionError("unknown chart equation scope")
    method = certificate.get("method")
    split_hash_valid = (
        method == "direct"
        and certificate.get("split_source_sha256") is None
    ) or (
        certificate.get("split_source_sha256")
        == HIGH.sha256_text(split_program)
    )
    if (
        certificate.get("status") != "UNIT_IDEAL"
        or method not in ("direct", "split")
        or certificate.get("cas", {}).get("status") != "UNIT_IDEAL"
        or certificate.get("source_sha256")
        != HIGH.sha256_text(program)
        or not split_hash_valid
        or certificate.get("metadata") != normalized_json(metadata)
        or not scope_metadata_valid
    ):
        raise AssertionError(
            f"{equation_scope} chart certificate changed"
        )
    clause = HIGH.chart_clause(pool, closure, tree, BRANCH)
    stored_clause = tuple(map(int, record.get("clause", clause)))
    general_clause = COVER.general_chart_clause(
        pool,
        closure,
        tree,
    )
    if stored_clause not in (clause, general_clause):
        raise AssertionError("rare chart representative clause changed")
    source = program if method == "direct" else split_program
    return (
        f"{equation_scope}_{method}",
        HIGH.chart_symmetry_orbit_clauses(
        closure,
        tree,
        BRANCH,
        pool,
        ),
        source,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, required=True)
    parser.add_argument("--require-unsat", action="store_true")
    parser.add_argument("--rerun-singular", action="store_true")
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--singular-timeout", type=float, default=30)
    args = parser.parse_args()
    if args.jobs <= 0 or args.singular_timeout <= 0:
        raise ValueError("invalid verifier arguments")

    state = json.loads(args.state.read_bytes())
    metadata = state.get("metadata", {})
    if (
        state.get("branch") != BRANCH
        or metadata.get("majority_mixed_colourings") != 0
        or metadata.get("pure_colour_nonvanishing") != [0, 1, 2]
        or metadata.get("learn_chart_orbits") is not True
        or metadata.get("global_conjecture_resolved") is not False
        or (args.require_unsat and state.get("status") != "UNSAT")
    ):
        raise AssertionError("rare CEGAR state metadata changed")

    allowed = SEMANTICS.finite_field_local_signatures()
    retained_mixed = COVER.rare_mixed_colourings()
    cnf, pool = SEMANTICS.build_pair_support_cnf(
        allowed,
        mixed_colourings=retained_mixed,
    )
    branch_metadata = HIGH.add_branch_restriction(
        cnf,
        pool,
        allowed,
        BRANCH,
    )
    lex_leaders = HIGH.add_stabilizer_lex_leaders(
        cnf,
        pool,
        BRANCH,
    )
    raw_profile = metadata.get("coordinate_profile_restriction")
    coordinate_profile = (
        tuple(map(int, raw_profile))
        if raw_profile is not None
        else None
    )
    if coordinate_profile is not None and (
        len(coordinate_profile) != len(SEMANTICS.MODES)
        or coordinate_profile[0] != 5
        or any(
            value < 0 or value > len(SEMANTICS.SOURCES)
            for value in coordinate_profile
        )
    ):
        raise AssertionError("invalid coordinate-profile restriction")
    profile_clauses = (
        add_coordinate_profile_restriction(
            cnf,
            pool,
            coordinate_profile,
        )
        if coordinate_profile is not None
        else 0
    )
    base_clauses = len(cnf.clauses)
    if (
        metadata.get("catalogue_signatures") != len(allowed)
        or metadata.get("rare_mixed_colourings")
        != len(retained_mixed)
        or metadata.get("branch_restriction")
        != normalized_json(branch_metadata)
        or metadata.get("lex_leaders") != lex_leaders
        or metadata.get("coordinate_profile_clauses", 0)
        != profile_clauses
        or metadata.get("base_variables") != pool.top
        or metadata.get("base_clauses") != base_clauses
    ):
        raise AssertionError("rare support CNF reconstruction changed")

    all_clauses = set()
    sources_to_replay = []
    method_counts: Counter[str] = Counter()
    seed_record_count = 0
    seed_sources = metadata.get("seed_sources", [])
    for source_metadata in seed_sources:
        path = Path(source_metadata["path"])
        raw = path.read_bytes()
        seed = json.loads(raw)
        records = seed.get("records", [])
        before = len(all_clauses)
        if (
            hashlib.sha256(raw).hexdigest()
            != source_metadata.get("sha256")
            or seed.get("branch") != BRANCH
            or len(records)
            != source_metadata.get("representative_records")
        ):
            raise AssertionError(f"rare seed {path} changed")
        for record in records:
            method, orbit, source = validate_record(record, pool)
            all_clauses.update(orbit)
            sources_to_replay.append(source)
            method_counts[method] += 1
        if (
            len(all_clauses) - before
            != source_metadata.get("new_transported_clauses")
        ):
            raise AssertionError(f"rare seed orbit count {path} changed")
        seed_record_count += len(records)
    if len(all_clauses) != metadata.get("transported_seed_clauses"):
        raise AssertionError("transported rare seed union changed")
    effective_seed_clauses, seed_subsumption = (
        remove_strongly_subsumed_clauses(
            tuple(sorted(all_clauses))
        )
    )
    stored_subsumption = metadata.get("strong_seed_subsumption")
    if stored_subsumption is not None and (
        stored_subsumption != normalized_json(seed_subsumption)
        or metadata.get("effective_transported_seed_clauses")
        != len(effective_seed_clauses)
    ):
        raise AssertionError("strong seed subsumption changed")

    dynamic_records = state.get("records", [])
    dynamic_new_clauses = 0
    forest_sizes: Counter[int] = Counter()
    for index, record in enumerate(dynamic_records):
        supports = LEDGER.normalized_supports(record["supports"])
        closure = LEDGER.normalized_supports(
            record["closure_supports"]
        )
        if closure != HIGH.closure_supports(supports):
            raise AssertionError(
                f"dynamic closure {index} is not canonical"
            )
        method, orbit, source = validate_record(record, pool)
        new = sum(clause not in all_clauses for clause in orbit)
        if (
            len(orbit) != record.get("transported_orbit_clauses")
            or new != record.get("new_transported_orbit_clauses")
        ):
            raise AssertionError(
                f"dynamic orbit accounting {index} changed"
            )
        all_clauses.update(orbit)
        dynamic_new_clauses += new
        sources_to_replay.append(source)
        method_counts[method] += 1
        forest_sizes[len(record["gauge_tree"])] += 1

    fresh_replays = 0
    if args.rerun_singular:
        def replay(source: str) -> str:
            return HIGH.run_singular(
                source,
                args.singular_timeout,
            )["status"]

        with ThreadPoolExecutor(max_workers=args.jobs) as executor:
            statuses = list(executor.map(replay, sources_to_replay))
        if any(status != "UNIT_IDEAL" for status in statuses):
            raise AssertionError("fresh rare Singular replay failed")
        fresh_replays = len(statuses)

    effective_all_clauses, final_subsumption = (
        remove_strongly_subsumed_clauses(
            tuple(sorted(all_clauses))
        )
    )
    cnf.extend([list(clause) for clause in effective_all_clauses])
    solver_results = {}
    for name in ("cadical195", "glucose4"):
        with Solver(name=name, bootstrap_with=cnf.clauses) as solver:
            solver_results[name] = "SAT" if solver.solve() else "UNSAT"
    if args.require_unsat and set(solver_results.values()) != {"UNSAT"}:
        raise AssertionError("rare q5_311 cover is not UNSAT")
    cover_unsat = set(solver_results.values()) == {"UNSAT"}

    print(
        json.dumps(
            {
                "verified": True,
                "state_status": state.get("status"),
                "catalogue_signatures": len(allowed),
                "rare_mixed_colourings": len(retained_mixed),
                "majority_mixed_colourings": 0,
                "lex_leaders": lex_leaders,
                "coordinate_profile_restriction": coordinate_profile,
                "coordinate_profile_clauses": profile_clauses,
                "seed_records": seed_record_count,
                "dynamic_records": len(dynamic_records),
                "transported_seed_clauses": metadata[
                    "transported_seed_clauses"
                ],
                "effective_transported_seed_clauses": (
                    len(effective_seed_clauses)
                ),
                "strong_seed_subsumption": seed_subsumption,
                "dynamic_new_clauses": dynamic_new_clauses,
                "unique_chart_clauses": len(all_clauses),
                "effective_chart_clauses": len(
                    effective_all_clauses
                ),
                "final_strong_subsumption": final_subsumption,
                "certificate_methods": dict(method_counts),
                "dynamic_gauge_forest_edges": {
                    str(size): count
                    for size, count in sorted(forest_sizes.items())
                },
                "fresh_singular_replays": fresh_replays,
                "solver_results": solver_results,
                "coordinate_profile_slice_resolved": (
                    coordinate_profile is not None and cover_unsat
                ),
                "q5_311_rare_branch_resolved": (
                    coordinate_profile is None and cover_unsat
                ),
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
