"""Materialize an exact replay CNF for a fixed P5 coordinate-cycle branch."""

from __future__ import annotations

import argparse
import collections
import hashlib
import importlib.util
import json
import pathlib


ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXED_PROBE = ROOT / "tmp" / "probe_p5_max3_coordinate_support.py"
SPEC = importlib.util.spec_from_file_location("p5_fixed_probe_replay", FIXED_PROBE)
FIXED = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(FIXED)
P5 = FIXED.P5


def sha256(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_dimacs(
    path: pathlib.Path, variable_count: int, clauses: list[list[int]]
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="ascii", newline="\n") as handle:
        handle.write(f"p cnf {variable_count} {len(clauses)}\n")
        for clause in clauses:
            handle.write(" ".join(str(literal) for literal in clause))
            handle.write(" 0\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--shape", choices=tuple(FIXED.SHAPES), required=True)
    parser.add_argument("--state", type=pathlib.Path, required=True)
    parser.add_argument("--general-state", type=pathlib.Path, required=True)
    parser.add_argument("--output", type=pathlib.Path, required=True)
    parser.add_argument("--metadata", type=pathlib.Path, required=True)
    parser.add_argument(
        "--allow-in-progress",
        action="store_true",
        help="permit a nonterminal discovery ledger for rehearsal only",
    )
    args = parser.parse_args()

    state = json.loads(args.state.read_text(encoding="utf-8"))
    if state.get("shape") != args.shape:
        raise AssertionError("fixed ledger has the wrong shape")
    if state.get("status") != "UNSAT" and not args.allow_in_progress:
        raise AssertionError("refusing to certify a non-UNSAT discovery ledger")
    records = list(state.get("learned_records", []))
    if not records:
        raise AssertionError("fixed ledger contains no learned records")

    allowed = P5.finite_field_local_signatures()
    cnf, pool = P5.build_cnf(
        allowed,
        double_lex=False,
        pair_hierarchy=True,
    )
    counts: dict[str, int] = {"base": len(cnf.clauses)}
    automorphisms = FIXED.shape_automorphisms(args.shape)
    before = len(cnf.clauses)
    lex_leaders = FIXED.add_shape_lex_leaders(
        cnf, pool, args.shape, automorphisms
    )
    counts["shape_lex"] = len(cnf.clauses) - before

    general_clauses, general_summary = FIXED.transported_general_preload(
        pool,
        allowed,
        args.shape,
        automorphisms,
        args.general_state,
    )
    before = len(cnf.clauses)
    cnf.extend(general_clauses)
    counts["transported_general"] = len(cnf.clauses) - before

    before = len(cnf.clauses)
    required_by_mode = [
        set(FIXED.SHAPES[args.shape][mode]) for mode in P5.MODES
    ]
    forbidden_patterns_by_mode = []
    for mode in P5.MODES:
        forbidden = [
            pattern_index
            for pattern_index, signature in enumerate(allowed)
            if {
                source
                for source, mask in enumerate(signature[0])
                if mask not in (1, 2, 4)
            }
            != required_by_mode[mode]
        ]
        forbidden_patterns_by_mode.append(len(forbidden))
        cnf.extend(
            [
                [-pool.id(("local_pattern", mode, pattern_index))]
                for pattern_index in forbidden
            ]
        )
    counts["fixed_shape_units"] = len(cnf.clauses) - before

    fixed_orbit_clauses: set[tuple[int, ...]] = set()
    base_clauses: set[tuple[int, ...]] = set()
    mode_counts: collections.Counter[str] = collections.Counter()
    for record in records:
        base_clause = tuple(sorted(int(value) for value in record["clause"]))
        if base_clause in base_clauses:
            raise AssertionError("fixed ledger repeats a base clause")
        base_clauses.add(base_clause)
        mode_counts[str(record["contradiction_mode"])] += 1
        for clause in FIXED.shape_clause_orbit(
            pool, record["clause"], allowed, automorphisms
        ):
            fixed_orbit_clauses.add(tuple(clause))
    before = len(cnf.clauses)
    cnf.extend([list(clause) for clause in sorted(fixed_orbit_clauses)])
    counts["fixed_ledger_orbits"] = len(cnf.clauses) - before

    variable_count = pool.top
    clause_count = len(cnf.clauses)
    write_dimacs(args.output, variable_count, cnf.clauses)
    payload = {
        "status": "REHEARSAL" if state.get("status") != "UNSAT" else "FINAL",
        "shape": args.shape,
        "fixed_state": str(args.state),
        "fixed_state_status": state.get("status"),
        "fixed_state_sha256": sha256(args.state),
        "general_state": str(args.general_state),
        "general_state_sha256": sha256(args.general_state),
        "probe_source": str(FIXED_PROBE),
        "probe_source_sha256": sha256(FIXED_PROBE),
        "local_probe_source": str(FIXED.PROBE_PATH),
        "local_probe_source_sha256": sha256(FIXED.PROBE_PATH),
        "output": str(args.output),
        "output_sha256": sha256(args.output),
        "variables": variable_count,
        "clauses": clause_count,
        "clause_groups": counts,
        "shape_automorphisms": len(automorphisms),
        "shape_lex_leaders": lex_leaders,
        "forbidden_patterns_per_mode": forbidden_patterns_by_mode,
        "fixed_records": len(records),
        "fixed_unique_orbit_clauses": len(fixed_orbit_clauses),
        "fixed_modes": dict(sorted(mode_counts.items())),
        "general_preload": general_summary,
    }
    args.metadata.parent.mkdir(parents=True, exist_ok=True)
    args.metadata.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
