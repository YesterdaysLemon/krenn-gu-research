"""Explore the branch where every P_5 local map has at most three coordinate rows."""

from __future__ import annotations

import argparse
import collections
import importlib.util
import itertools
import json
import pathlib

from pysat.solvers import Solver


ROOT = pathlib.Path(__file__).resolve().parents[1]
PROBE_PATH = ROOT / "tmp" / "probe_p5_tricolour_support_sat.py"
SHAPES = {
    "c10": ((0, 1), (1, 2), (2, 3), (3, 4), (0, 4)),
    "c4c6": ((0, 1), (0, 1), (2, 3), (3, 4), (2, 4)),
}
SPEC = importlib.util.spec_from_file_location("p5_probe", PROBE_PATH)
P5 = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(P5)


def shape_automorphisms(
    shape: str,
) -> tuple[tuple[tuple[int, ...], tuple[int, ...]], ...]:
    """All bipartition-preserving automorphisms of a fixed loop shape."""
    edges = {
        (mode, source)
        for mode, sources in enumerate(SHAPES[shape])
        for source in sources
    }
    automorphisms = []
    for mode_permutation in itertools.permutations(P5.MODES):
        for source_permutation in itertools.permutations(P5.SOURCES):
            transformed = {
                (
                    mode_permutation[mode],
                    source_permutation[source],
                )
                for mode, source in edges
            }
            if transformed == edges:
                automorphisms.append(
                    (mode_permutation, source_permutation)
                )
    expected = {"c10": 10, "c4c6": 24}[shape]
    assert len(automorphisms) == expected
    return tuple(automorphisms)


def shape_clause_orbit(
    pool,
    clause: list[int],
    allowed: tuple[tuple, ...],
    automorphisms: tuple[
        tuple[tuple[int, ...], tuple[int, ...]], ...
    ],
) -> list[list[int]]:
    """Aut(shape) x S3(colour) orbit of an entry/signature clause."""
    signature_index = {
        signature: index for index, signature in enumerate(allowed)
    }
    source_subsets = tuple(
        subset
        for size in (2, 3, 4)
        for subset in itertools.combinations(P5.SOURCES, size)
    )
    subset_index = {
        subset: index for index, subset in enumerate(source_subsets)
    }
    transformed_signature_cache = {}

    def colour_mask(mask: int, permutation: tuple[int, ...]) -> int:
        return sum(
            ((mask >> colour) & 1) << permutation[colour]
            for colour in P5.COLOURS
        )

    def transformed_signature(
        pattern_index: int,
        source_permutation: tuple[int, ...],
        colour_permutation: tuple[int, ...],
    ) -> int:
        cache_key = (
            pattern_index,
            source_permutation,
            colour_permutation,
        )
        if cache_key in transformed_signature_cache:
            return transformed_signature_cache[cache_key]
        supports, incidences = allowed[pattern_index]
        new_supports = [0] * len(P5.SOURCES)
        for old_source in P5.SOURCES:
            new_supports[source_permutation[old_source]] = colour_mask(
                supports[old_source], colour_permutation
            )
        new_incidences = [0] * len(source_subsets)
        for old_subset_index, old_subset in enumerate(source_subsets):
            new_subset = tuple(
                sorted(source_permutation[source] for source in old_subset)
            )
            new_incidences[subset_index[new_subset]] = colour_mask(
                incidences[old_subset_index], colour_permutation
            )
        new_signature = (
            tuple(new_supports),
            tuple(new_incidences),
        )
        result = signature_index[new_signature]
        transformed_signature_cache[cache_key] = result
        return result

    output = set()
    for mode_permutation, source_permutation in automorphisms:
        for colour_permutation in itertools.permutations(P5.COLOURS):
            transformed = []
            for literal in clause:
                key = pool.obj(abs(literal))
                if key[0] == "x":
                    _, mode, source, colour = key
                    new_key = P5.entry_key(
                        mode_permutation[mode],
                        source_permutation[source],
                        colour_permutation[colour],
                    )
                else:
                    assert key[0] == "local_pattern"
                    _, mode, pattern_index = key
                    new_key = (
                        "local_pattern",
                        mode_permutation[mode],
                        transformed_signature(
                            pattern_index,
                            source_permutation,
                            colour_permutation,
                        ),
                    )
                new_variable = pool.id(new_key)
                transformed.append(
                    new_variable if literal > 0 else -new_variable
                )
            output.add(tuple(sorted(transformed)))
    return [list(item) for item in sorted(output)]


def add_shape_lex_leaders(
    cnf,
    pool,
    shape: str,
    automorphisms: tuple[
        tuple[tuple[int, ...], tuple[int, ...]], ...
    ],
) -> int:
    """Keep a lexicographically least support in every shape orbit."""
    identity_modes = tuple(P5.MODES)
    identity_sources = tuple(P5.SOURCES)
    identity_colours = tuple(P5.COLOURS)
    left = [
        pool.id(P5.entry_key(mode, source, colour))
        for mode in P5.MODES
        for source in P5.SOURCES
        for colour in P5.COLOURS
    ]
    count = 0
    for mode_permutation, source_permutation in automorphisms:
        for colour_permutation in itertools.permutations(P5.COLOURS):
            if (
                mode_permutation == identity_modes
                and source_permutation == identity_sources
                and colour_permutation == identity_colours
            ):
                continue
            right = [
                pool.id(
                    P5.entry_key(
                        mode_permutation[mode],
                        source_permutation[source],
                        colour_permutation[colour],
                    )
                )
                for mode in P5.MODES
                for source in P5.SOURCES
                for colour in P5.COLOURS
            ]
            P5.add_lex_leq(
                cnf,
                pool,
                left,
                right,
                ("fixed_shape", shape, count),
            )
            count += 1
    expected = len(automorphisms) * 6 - 1
    assert count == expected
    return count


def transported_general_preload(
    pool,
    allowed: tuple[tuple, ...],
    shape: str,
    automorphisms: tuple[
        tuple[tuple[int, ...], tuple[int, ...]], ...
    ],
    state_path: pathlib.Path,
) -> tuple[list[list[int]], dict]:
    """Transport a general-loop ledger into one fixed labelled shape."""
    state = json.loads(state_path.read_text(encoding="utf-8"))
    if state.get("shape") is not None:
        raise ValueError("general preload ledger must have shape null")
    target_edges = frozenset(
        (mode, source)
        for mode, sources in enumerate(SHAPES[shape])
        for source in sources
    )
    transports = {}
    for mode_permutation in itertools.permutations(P5.MODES):
        inverse_mode = {
            new: old
            for old, new in enumerate(mode_permutation)
        }
        for source_permutation in itertools.permutations(P5.SOURCES):
            inverse_source = {
                new: old
                for old, new in enumerate(source_permutation)
            }
            old_edges = frozenset(
                (
                    inverse_mode[mode],
                    inverse_source[source],
                )
                for mode, source in target_edges
            )
            transports.setdefault(
                old_edges,
                (mode_permutation, source_permutation),
            )

    output = set()
    selected_records = 0
    for record in state.get("learned_records", []):
        supports = record["supports"]
        old_edges = frozenset(
            (mode, source)
            for mode, rows in enumerate(supports)
            for source, mask in enumerate(rows)
            if mask not in (1, 2, 4)
        )
        transport = transports.get(old_edges)
        if transport is None:
            continue
        selected_records += 1
        transported = shape_clause_orbit(
            pool,
            record["clause"],
            allowed,
            (transport,),
        )[0]
        output.update(
            tuple(clause)
            for clause in shape_clause_orbit(
                pool,
                transported,
                allowed,
                automorphisms,
            )
        )
    expected_records = {"c10": 388, "c4c6": 572}[shape]
    assert selected_records == expected_records
    return (
        [list(clause) for clause in sorted(output)],
        {
            "path": str(state_path),
            "selected_records": selected_records,
            "transported_clauses": len(output),
        },
    )


def global_local_signature_preload(
    pool,
    allowed: tuple[tuple, ...],
    state_path: pathlib.Path,
) -> tuple[list[list[int]], dict]:
    """Import a compatible full-local-signature ledger under global symmetry."""
    state = json.loads(state_path.read_text(encoding="utf-8"))
    output = set()
    selected_records = 0
    for record in state.get("learned_records", []):
        clause = [int(literal) for literal in record["clause"]]
        keys = [pool.obj(abs(literal)) for literal in clause]
        if any(key is None for key in keys):
            raise ValueError(
                f"incompatible variable numbering in preload {state_path}"
            )
        key_kinds = {key[0] for key in keys}
        if key_kinds == {"local_pattern"}:
            selected = {}
            for literal, key in zip(clause, keys):
                if literal >= 0:
                    raise ValueError(
                        "preloaded local-pattern cube has a positive literal"
                    )
                _, mode, pattern_index = key
                if mode in selected:
                    raise ValueError(
                        "preloaded local-pattern cube repeats a mode"
                    )
                selected[mode] = pattern_index
            if set(selected) != set(P5.MODES):
                raise ValueError(
                    "preloaded local-pattern cube omits a mode"
                )
            decoded_support = tuple(
                tuple(allowed[selected[mode]][0])
                for mode in P5.MODES
            )
            recorded_support = tuple(
                tuple(row) for row in record["supports"]
            )
            if decoded_support != recorded_support:
                raise ValueError(
                    "preloaded local-pattern numbering is incompatible"
                )
            orbit = P5.local_pattern_clause_orbit(
                pool, clause, allowed
            )
        elif key_kinds == {"x"}:
            recorded_support = tuple(
                tuple(row) for row in record["supports"]
            )
            for literal, key in zip(clause, keys):
                _, mode, source, colour = key
                value = bool(
                    recorded_support[mode][source] & (1 << colour)
                )
                if value == (literal > 0):
                    raise ValueError(
                        "preloaded x clause is not false on its record"
                    )
            orbit = P5.symmetry_clause_orbit(pool, clause)
        else:
            raise ValueError(
                "global preload must use only x or local_pattern clauses; "
                f"found {key_kinds}"
            )
        selected_records += 1
        output.update(tuple(item) for item in orbit)
    return (
        [list(clause) for clause in sorted(output)],
        {
            "path": str(state_path),
            "selected_records": selected_records,
            "orbit_clauses": len(output),
        },
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--models", type=int, default=10_000)
    parser.add_argument("--state", type=pathlib.Path)
    parser.add_argument("--shape", choices=tuple(SHAPES))
    parser.add_argument(
        "--coordinate-branch",
        choices=("max3", "high"),
        default="max3",
        help=(
            "with no fixed shape, require every mode to have at most "
            "three coordinate rows or require at least one mode to have four"
        ),
    )
    parser.add_argument("--no-shape-symmetry", action="store_true")
    parser.add_argument(
        "--no-all-full-theorem",
        action="store_true",
        help=(
            "disable the certified all-full blocking clause; intended only "
            "for historical differential replay"
        ),
    )
    parser.add_argument(
        "--no-one-partial-theorem",
        action="store_true",
        help=(
            "disable the certified exact-one-partial blocking clauses; "
            "intended only for historical differential replay"
        ),
    )
    parser.add_argument("--general-state", type=pathlib.Path)
    parser.add_argument(
        "--artifact-dir",
        type=pathlib.Path,
        default=ROOT / "tmp",
        help=(
            "directory for generated Singular sources and logs; use a "
            "branch-specific directory when searches run concurrently"
        ),
    )
    parser.add_argument(
        "--support-only-after",
        type=int,
        default=3,
        help=(
            "after this many signature-level Singular exclusions share one "
            "support, test the larger exact-support stratum once; zero disables"
        ),
    )
    parser.add_argument(
        "--support-only-timeout",
        type=int,
        default=30,
        help="seconds allowed for one opportunistic exact-support CAS probe",
    )
    parser.add_argument(
        "--preload-state",
        type=pathlib.Path,
        action="append",
        default=[],
        help="compatible full-local-signature ledger to import",
    )
    parser.add_argument(
        "--replay-through-state",
        type=pathlib.Path,
        help=(
            "deterministically replay and validate this ledger prefix before "
            "running fresh contradiction discovery"
        ),
    )
    args = parser.parse_args()
    if args.support_only_after < 0:
        raise ValueError("--support-only-after must be nonnegative")
    if args.support_only_timeout <= 0:
        raise ValueError("--support-only-timeout must be positive")
    if args.shape is not None and args.coordinate_branch != "max3":
        raise ValueError("--coordinate-branch applies only without --shape")
    if args.shape is not None and args.preload_state:
        raise ValueError("--preload-state is for the unfixed global branch")

    allowed = P5.finite_field_local_signatures()
    automorphisms = (
        ()
        if args.shape is None or args.no_shape_symmetry
        else shape_automorphisms(args.shape)
    )
    cnf, pool = P5.build_cnf(
        allowed,
        double_lex=args.shape is None,
        pair_hierarchy=True,
    )
    shape_lex_leaders = (
        add_shape_lex_leaders(
            cnf, pool, args.shape, automorphisms
        )
        if automorphisms
        else 0
    )
    general_preload = None
    if args.general_state is not None:
        if not automorphisms:
            raise ValueError(
                "--general-state requires fixed-shape symmetry"
            )
        general_clauses, general_preload = transported_general_preload(
            pool,
            allowed,
            args.shape,
            automorphisms,
            args.general_state,
        )
        cnf.extend(general_clauses)
    global_preloads = []
    for preload_path in args.preload_state:
        if args.shape is not None:
            raise ValueError("--preload-state requires no fixed shape")
        preload_clauses, preload_summary = (
            global_local_signature_preload(
                pool, allowed, preload_path
            )
        )
        cnf.extend(preload_clauses)
        global_preloads.append(preload_summary)
    forbidden_patterns_by_mode = []
    for mode in P5.MODES:
        if args.shape is None:
            if args.coordinate_branch == "max3":
                forbidden_patterns = tuple(
                    index
                    for index, signature in enumerate(allowed)
                    if sum(
                        mask in (1, 2, 4)
                        for mask in signature[0]
                    )
                    >= 4
                )
            else:
                forbidden_patterns = ()
        else:
            required_noncoordinate = set(SHAPES[args.shape][mode])
            forbidden_patterns = tuple(
                index
                for index, signature in enumerate(allowed)
                if {
                    source
                    for source, mask in enumerate(signature[0])
                    if mask not in (1, 2, 4)
                }
                != required_noncoordinate
            )
        forbidden_patterns_by_mode.append(forbidden_patterns)
        for pattern_index in forbidden_patterns:
            cnf.append(
                [-pool.id(("local_pattern", mode, pattern_index))]
            )
    all_full_boundary_clause = None
    one_partial_boundary_clauses = []
    if args.shape is not None and not args.no_all_full_theorem:
        all_full_boundary_clause = [
            -pool.id(P5.entry_key(mode, source, colour))
            for mode, noncoordinate_sources in enumerate(
                SHAPES[args.shape]
            )
            for source in noncoordinate_sources
            for colour in P5.COLOURS
        ]
        if len(all_full_boundary_clause) != 30:
            raise AssertionError("all-full boundary clause changed")
        cnf.append(all_full_boundary_clause)
    if args.shape is not None and not args.no_one_partial_theorem:
        noncoordinate_cells = [
            (mode, source)
            for mode, noncoordinate_sources in enumerate(
                SHAPES[args.shape]
            )
            for source in noncoordinate_sources
        ]
        if len(noncoordinate_cells) != 10:
            raise AssertionError("noncoordinate cell count changed")
        for omitted_cell in noncoordinate_cells:
            clause = [
                -pool.id(P5.entry_key(mode, source, colour))
                for mode, source in noncoordinate_cells
                if (mode, source) != omitted_cell
                for colour in P5.COLOURS
            ]
            if len(clause) != 27:
                raise AssertionError(
                    "one-partial boundary clause changed"
                )
            one_partial_boundary_clauses.append(clause)
            cnf.append(clause)
        if len(one_partial_boundary_clauses) != 10:
            raise AssertionError(
                "one-partial boundary clause count changed"
            )
    if args.shape is None and args.coordinate_branch == "high":
        high_coordinate_patterns = tuple(
            pattern_index
            for pattern_index, signature in enumerate(allowed)
            if sum(
                mask in (1, 2, 4) for mask in signature[0]
            )
            >= 4
        )
        if not high_coordinate_patterns:
            raise AssertionError("local catalogue has no high-coordinate map")
        cnf.append(
            [
                pool.id(("local_pattern", mode, pattern_index))
                for mode in P5.MODES
                for pattern_index in high_coordinate_patterns
            ]
        )

    records: list[dict] = []
    if args.state is not None and args.state.exists():
        state = json.loads(args.state.read_text(encoding="utf-8"))
        if state.get("shape") != args.shape:
            raise ValueError(
                "state shape does not match requested branch"
            )
        legacy_branch = (
            state.get("shape")
            if state.get("shape") is not None
            else "max3"
        )
        state_branch = state.get(
            "coordinate_branch", legacy_branch
        )
        requested_branch = (
            args.shape
            if args.shape is not None
            else args.coordinate_branch
        )
        if state_branch != requested_branch:
            raise ValueError(
                "state coordinate branch does not match requested branch"
            )
        records = list(state.get("learned_records", []))
        for record in records:
            clause = record["clause"]
            if automorphisms:
                cnf.extend(
                    shape_clause_orbit(
                        pool, clause, allowed, automorphisms
                    )
                )
            elif args.shape is not None:
                cnf.append(clause)
            else:
                keys = [pool.obj(abs(literal)) for literal in clause]
                if all(key[0] == "local_pattern" for key in keys):
                    cnf.extend(
                        P5.local_pattern_clause_orbit(
                            pool, clause, allowed
                        )
                    )
                else:
                    cnf.extend(P5.symmetry_clause_orbit(pool, clause))

    replay_records: list[dict] = []
    if args.replay_through_state is not None:
        replay_state = json.loads(
            args.replay_through_state.read_text(encoding="utf-8")
        )
        requested_branch = (
            args.shape
            if args.shape is not None
            else args.coordinate_branch
        )
        replay_branch = replay_state.get(
            "coordinate_branch",
            replay_state.get("shape") or "max3",
        )
        if replay_state.get("shape") != args.shape:
            raise ValueError("replay state shape does not match")
        if replay_branch != requested_branch:
            raise ValueError("replay state coordinate branch does not match")
        replay_records = list(replay_state.get("learned_records", []))
        if len(replay_records) < len(records):
            raise ValueError("replay state is shorter than the loaded state")
        for index, record in enumerate(records):
            expected = replay_records[index]
            if (
                record["clause"] != expected["clause"]
                or record["supports"] != expected["supports"]
                or record["contradiction_mode"]
                != expected["contradiction_mode"]
            ):
                raise ValueError(
                    f"loaded state differs from replay state at record {index}"
                )

    def support_key(raw_supports) -> tuple[tuple[int, ...], ...]:
        return tuple(tuple(int(mask) for mask in row) for row in raw_supports)

    support_signature_units = collections.Counter(
        support_key(record["supports"])
        for record in records
        if record["contradiction_mode"] == "singular_unit_ideal"
    )
    support_only_attempted = {
        support_key(record["supports"])
        for record in records
        if record["contradiction_mode"] == "singular_support_unit_ideal"
    }

    print(
        json.dumps(
            {
                "variables": pool.top,
                "clauses": len(cnf.clauses),
                "shape": args.shape,
                "coordinate_branch": (
                    args.shape
                    if args.shape is not None
                    else args.coordinate_branch
                ),
                "shape_automorphisms": len(automorphisms),
                "shape_lex_leaders": shape_lex_leaders,
                "general_preload": general_preload,
                "global_preloads": global_preloads,
                "shape_clause_orbit_bound": (
                    len(automorphisms)
                    * len(tuple(itertools.permutations(P5.COLOURS)))
                ),
                "forbidden_patterns_per_mode": [
                    len(patterns)
                    for patterns in forbidden_patterns_by_mode
                ],
                "all_full_boundary_clause_literals": (
                    len(all_full_boundary_clause)
                    if all_full_boundary_clause is not None
                    else 0
                ),
                "one_partial_boundary_clauses": len(
                    one_partial_boundary_clauses
                ),
                "one_partial_boundary_clause_literals": (
                    len(one_partial_boundary_clauses[0])
                    if one_partial_boundary_clauses
                    else 0
                ),
                "preloaded": len(records),
            }
        ),
        flush=True,
    )

    with Solver(name="cadical195", bootstrap_with=cnf.clauses) as solver:
        for model_index in range(args.models):
            if not solver.solve():
                status = {
                    "status": "UNSAT",
                    "shape": args.shape,
                    "coordinate_branch": (
                        args.shape
                        if args.shape is not None
                        else args.coordinate_branch
                    ),
                    "shape_automorphisms": len(automorphisms),
                    "shape_lex_leaders": shape_lex_leaders,
                    "general_preload": general_preload,
                    "global_preloads": global_preloads,
                    "all_full_boundary_clause_literals": (
                        len(all_full_boundary_clause)
                        if all_full_boundary_clause is not None
                        else 0
                    ),
                    "one_partial_boundary_clauses": len(
                        one_partial_boundary_clauses
                    ),
                    "one_partial_boundary_clause_literals": (
                        len(one_partial_boundary_clauses[0])
                        if one_partial_boundary_clauses
                        else 0
                    ),
                    "after_models": model_index,
                    "learned_records": records,
                }
                print(json.dumps(status), flush=True)
                if args.state is not None:
                    args.state.write_text(
                        json.dumps(status, indent=2) + "\n",
                        encoding="utf-8",
                    )
                return

            supports = P5.supports_from_model(pool, solver.get_model())
            positive_model = {
                value for value in solver.get_model() if value > 0
            }
            selected_signature_indices = [
                next(
                    pattern_index
                    for pattern_index in range(len(allowed))
                    if pool.id(
                        ("local_pattern", mode, pattern_index)
                    )
                    in positive_model
                )
                for mode in P5.MODES
            ]
            selected_signatures = tuple(
                allowed[index] for index in selected_signature_indices
            )

            if len(records) < len(replay_records):
                expected = replay_records[len(records)]
                expected_supports = tuple(
                    tuple(int(mask) for mask in row)
                    for row in expected["supports"]
                )
                if supports != expected_supports:
                    raise AssertionError(
                        "deterministic replay support mismatch at record "
                        f"{len(records)}"
                    )
                clause = [int(literal) for literal in expected["clause"]]
                for literal in clause:
                    variable_true = abs(literal) in positive_model
                    literal_true = (
                        variable_true if literal > 0 else not variable_true
                    )
                    if literal_true:
                        raise AssertionError(
                            "replayed clause is not false on its model at "
                            f"record {len(records)}"
                        )
                keys = [pool.obj(abs(literal)) for literal in clause]
                if any(key is None for key in keys):
                    raise AssertionError(
                        "replayed clause uses an unknown variable"
                    )
                if automorphisms:
                    symmetric_clauses = shape_clause_orbit(
                        pool, clause, allowed, automorphisms
                    )
                elif args.shape is not None:
                    symmetric_clauses = [clause]
                elif all(key[0] == "local_pattern" for key in keys):
                    symmetric_clauses = P5.local_pattern_clause_orbit(
                        pool, clause, allowed
                    )
                else:
                    symmetric_clauses = P5.symmetry_clause_orbit(
                        pool, clause
                    )
                for symmetric_clause in symmetric_clauses:
                    solver.add_clause(symmetric_clause)
                records.append(expected)
                replay_mode = expected["contradiction_mode"]
                replay_support_key = support_key(expected_supports)
                if replay_mode == "singular_unit_ideal":
                    support_signature_units[replay_support_key] += 1
                elif replay_mode == "singular_support_unit_ideal":
                    support_only_attempted.add(replay_support_key)
                if len(records) % 10 == 0:
                    print(
                        json.dumps(
                            {
                                "replayed": len(records),
                                "through": len(replay_records),
                                "last_mode": replay_mode,
                                "last_clause_length": len(clause),
                            }
                        ),
                        flush=True,
                    )
                if len(records) == len(replay_records):
                    print(
                        json.dumps(
                            {
                                "status": "REPLAY_COMPLETE",
                                "records": len(records),
                            }
                        ),
                        flush=True,
                    )
                continue

            lattice = P5.signed_lattice_result(supports)
            collision = (
                None
                if lattice["inconsistent"]
                else P5.residual_collision_result(supports)
            )
            if not lattice["inconsistent"] and collision is None:
                collision = P5.factored_residual_collision_result(
                    supports
                )

            if collision is not None:
                lattice = {
                    **lattice,
                    "inconsistent": True,
                    "contradiction_mode": collision[
                        "contradiction_mode"
                    ],
                    "certificate": collision,
                }

            if not lattice["inconsistent"]:
                candidate_lists = [
                    [
                        pattern_index
                        for pattern_index, signature in enumerate(
                            allowed
                        )
                        if signature[0] == tuple(supports[mode])
                    ]
                    for mode in P5.MODES
                ]
                viable_signature_tuples = []
                for indices in itertools.product(*candidate_lists):
                    signatures = tuple(
                        allowed[index] for index in indices
                    )
                    if all(
                        sum(
                            bool(
                                signatures[mode][1][pair_index]
                                & (1 << colour)
                            )
                            for mode in P5.MODES
                        )
                        >= 2
                        for pair_index in range(10)
                        for colour in P5.COLOURS
                    ):
                        viable_signature_tuples.append(
                            (indices, signatures)
                        )
                assert viable_signature_tuples
                closure_records = []
                all_signatures_close = True
                for indices, signatures in viable_signature_tuples:
                    result = P5.binomial_closure_result(
                        supports, signatures
                    )
                    if result is None:
                        all_signatures_close = False
                        break
                    closure_records.append(
                        {
                            "signature_indices": indices,
                            "contradiction_mode": result[
                                "contradiction_mode"
                            ],
                        }
                    )
                if all_signatures_close:
                    lattice = {
                        **lattice,
                        "inconsistent": True,
                        "contradiction_mode": (
                            "local_signature_exhaustion"
                        ),
                        "certificate": {
                            "viable_signatures": len(
                                viable_signature_tuples
                            ),
                            "records": closure_records,
                        },
                    }
                else:
                    closure = P5.binomial_closure_result(
                        supports, selected_signatures
                    )
                    if closure is not None:
                        lattice = {
                            **lattice,
                            "inconsistent": True,
                            "contradiction_mode": closure[
                                "contradiction_mode"
                            ],
                            "certificate": closure,
                        }
            else:
                closure = None

            support_probe = None
            current_support_key = support_key(supports)
            if (
                not lattice["inconsistent"]
                and args.support_only_after
                and support_signature_units[current_support_key]
                >= args.support_only_after
                and current_support_key not in support_only_attempted
            ):
                support_only_attempted.add(current_support_key)
                support_probe = P5.run_singular_signature(
                    selected_signature_indices,
                    args.artifact_dir,
                    support_only=True,
                    timeout_seconds=args.support_only_timeout,
                )
                if support_probe["unit_ideal"]:
                    lattice = {
                        **lattice,
                        "inconsistent": True,
                        "contradiction_mode": (
                            "singular_support_unit_ideal"
                        ),
                        "certificate": support_probe,
                    }

            singular = None
            if not lattice["inconsistent"]:
                singular = P5.run_singular_signature(
                    selected_signature_indices, args.artifact_dir
                )
                if singular["unit_ideal"]:
                    lattice = {
                        **lattice,
                        "inconsistent": True,
                        "contradiction_mode": "singular_unit_ideal",
                        "certificate": singular,
                    }

            if (
                not lattice["inconsistent"]
                and singular is not None
                and singular.get("phase")
            ):
                print(
                    json.dumps(
                        {
                            "status": "CAS_INCONCLUSIVE",
                            "model": model_index,
                            "supports": supports,
                            "selected_signature_indices": (
                                selected_signature_indices
                            ),
                            "singular": singular,
                            "support_probe": support_probe,
                            "lattice": lattice,
                        }
                    ),
                    flush=True,
                )
                return

            if not lattice["inconsistent"]:
                print(
                    json.dumps(
                        {
                            "status": "SURVIVOR",
                            "model": model_index,
                            "supports": supports,
                            "selected_signature_indices": (
                                selected_signature_indices
                            ),
                            "lattice": lattice,
                        }
                    ),
                    flush=True,
                )
                return

            if lattice["contradiction_mode"] == (
                "residual_permanent_collision"
            ):
                clause, _, _ = P5.residual_collision_clause(
                    pool, lattice["certificate"]
                )
            elif lattice["contradiction_mode"] == (
                "factored_residual_permanent_collision"
            ):
                clause, _, _ = P5.factored_residual_collision_clause(
                    pool, supports, lattice["certificate"]
                )
            elif lattice["contradiction_mode"].startswith(
                ("binomial_closure_", "local_incidence_")
            ):
                if lattice["certificate"].get(
                    "uses_local_incidence", False
                ):
                    clause = [
                        -pool.id(
                            ("local_pattern", mode, pattern_index)
                        )
                        for mode, pattern_index in zip(
                            P5.MODES, selected_signature_indices
                        )
                    ]
                else:
                    clause = P5.exact_support_clause(pool, supports)
            elif lattice["contradiction_mode"] == "singular_unit_ideal":
                clause = [
                    -pool.id(
                        ("local_pattern", mode, pattern_index)
                    )
                    for mode, pattern_index in zip(
                        P5.MODES, selected_signature_indices
                    )
                ]
            elif lattice["contradiction_mode"] == (
                "singular_support_unit_ideal"
            ):
                clause = P5.exact_support_clause(pool, supports)
            elif lattice["contradiction_mode"] == (
                "local_signature_exhaustion"
            ):
                clause = P5.exact_support_clause(pool, supports)
            else:
                clause, _, _ = P5.conflict_cube_clause(
                    pool, supports, lattice
                )

            keys = [pool.obj(abs(literal)) for literal in clause]
            if automorphisms:
                symmetric_clauses = shape_clause_orbit(
                    pool, clause, allowed, automorphisms
                )
            elif args.shape is not None:
                symmetric_clauses = [clause]
            else:
                if all(key[0] == "local_pattern" for key in keys):
                    symmetric_clauses = P5.local_pattern_clause_orbit(
                        pool, clause, allowed
                    )
                else:
                    symmetric_clauses = P5.symmetry_clause_orbit(
                        pool, clause
                    )
            for symmetric_clause in symmetric_clauses:
                solver.add_clause(symmetric_clause)
            records.append(
                {
                    "clause": clause,
                    "supports": supports,
                    "contradiction_mode": lattice[
                        "contradiction_mode"
                    ],
                    "certificate": lattice["certificate"],
                }
            )
            if lattice["contradiction_mode"] == "singular_unit_ideal":
                support_signature_units[current_support_key] += 1
            if len(records) % 10 == 0:
                print(
                    json.dumps(
                        {
                            "learned": len(records),
                            "last_mode": lattice[
                                "contradiction_mode"
                            ],
                            "last_clause_length": len(clause),
                        }
                    ),
                    flush=True,
                )
                if args.state is not None:
                    args.state.write_text(
                        json.dumps(
                            {
                                "status": "IN_PROGRESS",
                                "shape": args.shape,
                                "coordinate_branch": (
                                    args.shape
                                    if args.shape is not None
                                    else args.coordinate_branch
                                ),
                                "shape_automorphisms": len(
                                    automorphisms
                                ),
                                "shape_lex_leaders": (
                                    shape_lex_leaders
                                ),
                                "general_preload": general_preload,
                                "global_preloads": global_preloads,
                                "all_full_boundary_clause_literals": (
                                    len(all_full_boundary_clause)
                                    if all_full_boundary_clause is not None
                                    else 0
                                ),
                                "one_partial_boundary_clauses": len(
                                    one_partial_boundary_clauses
                                ),
                                "one_partial_boundary_clause_literals": (
                                    len(one_partial_boundary_clauses[0])
                                    if one_partial_boundary_clauses
                                    else 0
                                ),
                                "learned_records": records,
                            },
                            indent=2,
                        )
                        + "\n",
                        encoding="utf-8",
                    )

    if args.state is not None:
        args.state.write_text(
            json.dumps(
                {
                    "status": "IN_PROGRESS",
                    "shape": args.shape,
                    "coordinate_branch": (
                        args.shape
                        if args.shape is not None
                        else args.coordinate_branch
                    ),
                    "shape_automorphisms": len(automorphisms),
                    "shape_lex_leaders": shape_lex_leaders,
                    "general_preload": general_preload,
                    "global_preloads": global_preloads,
                    "all_full_boundary_clause_literals": (
                        len(all_full_boundary_clause)
                        if all_full_boundary_clause is not None
                        else 0
                    ),
                    "one_partial_boundary_clauses": len(
                        one_partial_boundary_clauses
                    ),
                    "one_partial_boundary_clause_literals": (
                        len(one_partial_boundary_clauses[0])
                        if one_partial_boundary_clauses
                        else 0
                    ),
                    "learned_records": records,
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
