"""Independent replay of the forced-slice factor-choice certificate.

The verifier does not import either certificate producer.  It rebuilds the
fixed skeleton, perfect matchings, activity counts, conditional cycle-fork
premise, every 10/12-term factor clause, each learned signed-lattice
conflict, and the final SAT decision.
"""

from __future__ import annotations
import sys as _bootstrap_sys
from pathlib import Path as _BootstrapPath

for _bootstrap_parent in _BootstrapPath(__file__).resolve().parents:
    if (_bootstrap_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        _bootstrap_sys.path.insert(0, str(_bootstrap_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap as _bootstrap_repository  # noqa: E402

REPO_ROOT, HERE = _bootstrap_repository(__file__)


import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path
from typing import Iterable, Sequence

import numpy as np
from pysat.solvers import Solver
from sympy import Matrix

N = 14
EQUATIONS = 3**N
Edge = tuple[int, int]
Factor = tuple[Edge, ...]
SparseRelation = tuple[tuple[int, int], ...]
ALL_EDGES = tuple(itertools.combinations(range(N), 2))
EDGE_ID = {item: position for position, item in enumerate(ALL_EDGES)}


def edge(first: int, second: int) -> Edge:
    return (
        (first, second) if first < second else (second, first)
    )


def cycle_edges(cycle: Sequence[int]) -> frozenset[Edge]:
    return frozenset(
        edge(cycle[position], cycle[(position + 1) % len(cycle)])
        for position in range(len(cycle))
    )


def contiguous_cycles(
    lengths: Sequence[int],
) -> tuple[tuple[int, ...], ...]:
    output = []
    start = 0
    for length in lengths:
        output.append(tuple(range(start, start + length)))
        start += length
    if start != N:
        raise AssertionError("cycle lengths do not cover the vertices")
    return tuple(output)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def perfect_matchings(allowed: Iterable[Edge]) -> list[Factor]:
    allowed_set = set(allowed)
    adjacency = [0] * N
    for first, second in allowed_set:
        adjacency[first] |= 1 << second
        adjacency[second] |= 1 << first
    output: list[Factor] = []

    def visit(remaining: int, chosen: Factor) -> None:
        if remaining == 0:
            output.append(chosen)
            return
        first_bit = remaining & -remaining
        first = first_bit.bit_length() - 1
        candidates = adjacency[first] & remaining
        while candidates:
            second_bit = candidates & -candidates
            candidates ^= second_bit
            second = second_bit.bit_length() - 1
            visit(
                remaining ^ first_bit ^ second_bit,
                (*chosen, edge(first, second)),
            )

    visit((1 << N) - 1, ())
    return sorted(output)


def indexed_colouring(index: int) -> tuple[int, ...]:
    return tuple(
        (index // (3**vertex)) % 3 for vertex in range(N)
    )


def local_code(
    colouring: Sequence[int], cycle: Sequence[int]
) -> int:
    return sum(
        int(colouring[vertex]) * (3**position)
        for position, vertex in enumerate(cycle)
    )


def vectorized_local_codes(
    indices: np.ndarray, cycle: Sequence[int]
) -> np.ndarray:
    output = np.zeros(len(indices), dtype=np.int64)
    for position, vertex in enumerate(cycle):
        output += (
            (indices // (3**vertex)) % 3
        ) * (3**position)
    return output


def extension_offsets(
    free: tuple[int, ...],
    cache: dict[tuple[int, ...], np.ndarray],
) -> np.ndarray:
    if free in cache:
        return cache[free]
    output = np.array([0], dtype=np.int64)
    for vertex in free:
        step = 3**vertex
        output = np.concatenate(
            (output, output + step, output + 2 * step)
        )
    cache[free] = output
    return output


def activity_counts(
    matchings: Sequence[Factor],
    labels: dict[Edge, int],
) -> tuple[np.ndarray, int]:
    counts = np.zeros(EQUATIONS, dtype=np.int16)
    cache: dict[tuple[int, ...], np.ndarray] = {}
    extensions = 0
    for matching in matchings:
        requirements = {
            vertex: labels[item]
            for item in matching
            if item in labels
            for vertex in item
        }
        base = sum(
            colour * (3**vertex)
            for vertex, colour in requirements.items()
        )
        free = tuple(
            vertex for vertex in range(N)
            if vertex not in requirements
        )
        indices = base + extension_offsets(free, cache)
        counts[indices] += 1
        extensions += len(indices)
    return counts, extensions


def matching_active(
    matching: Factor,
    colouring: Sequence[int],
    labels: dict[Edge, int],
) -> bool:
    return all(
        item not in labels
        or colouring[item[0]]
        == colouring[item[1]]
        == labels[item]
        for item in matching
    )


def checked_activity(
    equation: int,
    reported_ids: Sequence[int],
    expected_size: int,
    matchings: Sequence[Factor],
    counts: np.ndarray,
    labels: dict[Edge, int],
) -> tuple[int, ...]:
    ids = tuple(map(int, reported_ids))
    if (
        len(ids) != expected_size
        or len(set(ids)) != expected_size
        or int(counts[equation]) != expected_size
    ):
        raise AssertionError("reported activity size changed")
    colouring = indexed_colouring(equation)
    if len(set(colouring)) == 1:
        raise AssertionError("certificate uses a required colouring")
    if any(
        matching_id < 0
        or matching_id >= len(matchings)
        or not matching_active(
            matchings[matching_id], colouring, labels
        )
        for matching_id in ids
    ):
        raise AssertionError("reported activity contains an inactive term")
    return ids


def monomial_variables(
    matching: Factor,
    colouring: Sequence[int],
    labels: dict[Edge, int],
    full_edges: frozenset[Edge],
) -> tuple[int, ...]:
    output = []
    for item in matching:
        if item in full_edges:
            first_colour = int(colouring[item[0]])
            second_colour = int(colouring[item[1]])
        else:
            first_colour = second_colour = labels[item]
        output.append(
            9 * EDGE_ID[item]
            + 3 * first_colour
            + second_colour
        )
    return tuple(sorted(output))


def canonical_sparse(vector: Counter[int]) -> SparseRelation:
    direct = tuple(
        sorted(
            (int(variable), int(coefficient))
            for variable, coefficient in vector.items()
            if coefficient
        )
    )
    negative = tuple(
        (variable, -coefficient)
        for variable, coefficient in direct
    )
    return min(direct, negative)


def relation(
    first: Sequence[int], second: Sequence[int]
) -> SparseRelation:
    output: Counter[int] = Counter(first)
    output.subtract(second)
    return canonical_sparse(output)


def parallelogram_directions(
    vectors: Sequence[tuple[int, ...]],
) -> tuple[SparseRelation, ...] | None:
    if len(vectors) != 4:
        raise ValueError("four vectors are required")
    for first, second, opposite in (
        (1, 2, 3),
        (1, 3, 2),
        (2, 3, 1),
    ):
        if tuple(sorted(vectors[0] + vectors[opposite])) != tuple(
            sorted(vectors[first] + vectors[second])
        ):
            continue
        directions = tuple(
            row
            for row in (
                relation(vectors[0], vectors[first]),
                relation(vectors[0], vectors[second]),
            )
            if row
        )
        return tuple(dict.fromkeys(directions))
    return None


def parse_relation(raw: Sequence[Sequence[int]]) -> SparseRelation:
    output = tuple(tuple(map(int, item)) for item in raw)
    counter: Counter[int] = Counter()
    for variable, coefficient in output:
        counter[variable] += coefficient
    if canonical_sparse(counter) != output:
        raise AssertionError("relation signature is not canonical")
    return output


def dense(
    sparse: SparseRelation,
    positions: dict[int, int],
) -> list[int]:
    output = [0] * len(positions)
    for variable, coefficient in sparse:
        if variable not in positions:
            raise AssertionError("relation uses an unsupported variable")
        output[positions[variable]] = coefficient
    return output


def basis_coordinates(
    basis_rows: Sequence[Sequence[int]],
    vector: Sequence[int],
) -> list[int] | None:
    if not basis_rows:
        return None
    matrix = Matrix([list(map(int, row)) for row in basis_rows])
    if matrix.rank() != matrix.rows:
        raise AssertionError("reported lattice basis is dependent")
    pivots = list(matrix.rref()[1])
    if len(pivots) != matrix.rows:
        raise AssertionError("could not select basis pivot columns")
    pivot_matrix = matrix[:, pivots]
    raw = (
        Matrix([[int(vector[position]) for position in pivots]])
        * pivot_matrix.inv()
    )
    if any(value.q != 1 for value in raw):
        return None
    coordinates = [int(value) for value in raw.row(0)]
    reconstructed = Matrix([coordinates]) * matrix
    if list(map(int, reconstructed.row(0))) != list(
        map(int, vector)
    ):
        return None
    return coordinates


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "certificate",
        type=Path,
        nargs="?",
        default=Path(
            "tmp/fourteen_vertex_c4_4_6_sample93_15_"
            "forced_slice_factor_cegar.json"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_4_6_sample93_15_"
            "forced_slice_factor_cegar_verified.json"
        ),
    )
    args = parser.parse_args()
    proof = json.loads(args.certificate.read_text(encoding="utf-8"))
    if proof.get("status") != "UNSAT":
        raise AssertionError("factor-choice producer did not reach UNSAT")
    forced_path = Path(proof["forced_cycle_analysis"])
    forced = json.loads(forced_path.read_text(encoding="utf-8"))
    if sha256(forced_path) != proof["forced_cycle_analysis_sha256"]:
        raise AssertionError("forced-cycle premise hash changed")
    exploration_path = Path(proof["exploration"])
    exploration = json.loads(
        exploration_path.read_text(encoding="utf-8")
    )
    if sha256(exploration_path) != proof["exploration_sha256"]:
        raise AssertionError("support manifest hash changed")

    lengths = tuple(map(int, proof["full_cycle_type"]))
    cycles = contiguous_cycles(lengths)
    forced_cycle = tuple(map(int, proof["forced_cycle"]))
    forced_cycle_id = cycles.index(forced_cycle)
    full_edges = frozenset(
        item for cycle in cycles for item in cycle_edges(cycle)
    )
    factors = tuple(
        tuple(
            sorted(
                edge(*map(int, item))
                for item in proof["singleton_matchings"][key]
            )
        )
        for key in ("first", "second", "third")
    )
    support_row = exploration["survivors"][
        int(proof["survivor_index"])
    ]
    if {
        key: [list(item) for item in factors[position]]
        for position, key in enumerate(("first", "second", "third"))
    } != {
        key: support_row[key]
        for key in ("first", "second", "third")
    }:
        raise AssertionError("support manifest row changed")
    labels = {
        item: colour
        for colour, factor in enumerate(factors)
        for item in factor
    }
    if len(labels) != 3 * (N // 2):
        raise AssertionError("singleton factors are not edge-disjoint")
    matchings = perfect_matchings(set(full_edges) | set(labels))
    if len(matchings) != int(proof["skeleton_perfect_matchings"]):
        raise AssertionError("skeleton matching count changed")
    full_only = frozenset(
        matching_id
        for matching_id, matching in enumerate(matchings)
        if all(item in full_edges for item in matching)
    )
    baseline = 1 << len(cycles)
    if (
        len(full_only) != baseline
        or baseline != int(proof["full_only_matching_count"])
    ):
        raise AssertionError("full-factor product changed")
    counts, total_extensions = activity_counts(matchings, labels)
    if total_extensions != int(
        proof["matching_extensions_accumulated"]
    ):
        raise AssertionError("matching extension count changed")

    def extras_activity(
        equation: int,
        reported_extras: Sequence[int],
        total_size: int,
    ) -> tuple[int, ...]:
        extras = tuple(map(int, reported_extras))
        activity = tuple(sorted((*full_only, *extras)))
        checked_activity(
            equation,
            activity,
            total_size,
            matchings,
            counts,
            labels,
        )
        if (
            len(extras) != total_size - baseline
            or set(extras) & full_only
        ):
            raise AssertionError("reported extras changed")
        return extras

    # Replay every conditional fork that rules out an outer-cycle factor.
    raw_fork_rows = forced[
        "conditional_fork_certificates_by_cycle"
    ]
    if len(raw_fork_rows) != len(cycles):
        raise AssertionError("conditional fork partition changed")
    excluded_codes: list[set[int]] = []
    conditional_forks_replayed = 0
    for cycle_id, raw_rows in enumerate(raw_fork_rows):
        cycle = cycles[cycle_id]
        rows = {int(code): row for code, row in raw_rows.items()}
        if sorted(rows) != forced[
            "conditional_fork_local_codes_by_cycle"
        ][cycle_id]:
            raise AssertionError("conditional code catalogue changed")
        excluded_codes.append(set(rows))
        for code, row in rows.items():
            if (
                tuple(map(int, row["cycle"])) != cycle
                or int(row["cycle_local_code"]) != code
            ):
                raise AssertionError("conditional cycle label changed")
            pair_rows = [
                (
                    int(row["first_pair_equation_index"]),
                    tuple(map(int, row["first_pair_matchings"])),
                    parse_relation(
                        row["first_pair_relation_signature"]
                    ),
                ),
                (
                    int(row["second_pair_equation_index"]),
                    tuple(map(int, row["second_pair_matchings"])),
                    parse_relation(
                        row["second_pair_relation_signature"]
                    ),
                ),
            ]
            established = []
            for equation, pair, signature in pair_rows:
                colouring = indexed_colouring(equation)
                if local_code(colouring, cycle) != code:
                    raise AssertionError(
                        "conditional pair local code changed"
                    )
                extras_activity(
                    equation, pair, baseline + 2
                )
                vectors = tuple(
                    monomial_variables(
                        matchings[matching_id],
                        colouring,
                        labels,
                        full_edges,
                    )
                    for matching_id in pair
                )
                if relation(*vectors) != signature:
                    raise AssertionError(
                        "conditional pair relation changed"
                    )
                established.append(signature)
            rich_equation = int(row["rich_equation_index"])
            rich_activity = checked_activity(
                rich_equation,
                row["rich_activity"],
                baseline + 5,
                matchings,
                counts,
                labels,
            )
            rich_colouring = indexed_colouring(rich_equation)
            if local_code(rich_colouring, cycle) != code:
                raise AssertionError(
                    "conditional rich local code changed"
                )
            rich_extras = {
                matching_id
                for matching_id in rich_activity
                if matching_id not in full_only
            }
            survivor = int(row["rich_surviving_matching"])
            used = {survivor}
            rich_pairs = [
                tuple(map(int, pair))
                for pair in row["rich_paired_matchings"]
            ]
            if len(rich_pairs) != len(established):
                raise AssertionError(
                    "conditional rich pair count changed"
                )
            for pair, signature in zip(
                rich_pairs, established, strict=True
            ):
                pair = set(pair)
                if used & pair:
                    raise AssertionError(
                        "conditional rich pairs overlap"
                    )
                used.update(pair)
                first, second = tuple(pair)
                vectors = (
                    monomial_variables(
                        matchings[first],
                        rich_colouring,
                        labels,
                        full_edges,
                    ),
                    monomial_variables(
                        matchings[second],
                        rich_colouring,
                        labels,
                        full_edges,
                    ),
                )
                if relation(*vectors) != signature:
                    raise AssertionError(
                        "conditional relation does not transport"
                    )
            if used != rich_extras:
                raise AssertionError(
                    "conditional target lacks one survivor"
                )
            conditional_forks_replayed += 1

    # Rebuild the exact local-code slice forced by full-only equations.
    base_indices = np.flatnonzero(counts == baseline)
    base_codes = [
        vectorized_local_codes(base_indices, cycle)
        for cycle in cycles
    ]
    forcing_mask = np.ones(len(base_indices), dtype=bool)
    for cycle_id in range(len(cycles)):
        if cycle_id == forced_cycle_id:
            continue
        forcing_mask &= np.isin(
            base_codes[cycle_id],
            np.array(
                sorted(excluded_codes[cycle_id]), dtype=np.int64
            ),
        )
    forced_codes = set(
        map(
            int,
            np.unique(base_codes[forced_cycle_id][forcing_mask]),
        )
    )
    if forced_codes != set(map(int, proof["forced_local_codes"])):
        raise AssertionError("forced local-code slice changed")
    if forced_codes != set(
        map(
            int,
            forced["forced_local_codes_by_cycle"][
                forced_cycle_id
            ],
        )
    ):
        raise AssertionError("producer forced-code premise changed")
    reported_forcing = {
        int(code): int(equation)
        for code, equation in proof[
            "forcing_base_equations_by_local_code"
        ].items()
    }
    if set(reported_forcing) != forced_codes:
        raise AssertionError("forcing-equation coverage changed")
    for code, equation in reported_forcing.items():
        colouring = indexed_colouring(equation)
        if (
            int(counts[equation]) != baseline
            or local_code(colouring, forced_cycle) != code
        ):
            raise AssertionError("forcing base equation changed")
        for cycle_id, cycle in enumerate(cycles):
            if cycle_id == forced_cycle_id:
                continue
            if local_code(
                colouring, cycle
            ) not in excluded_codes[cycle_id]:
                raise AssertionError(
                    "forcing base lacks an excluded outer factor"
                )

    support_variables = sorted(
        {
            9 * EDGE_ID[item]
            + 3 * first_colour
            + second_colour
            for item in full_edges
            for first_colour in range(3)
            for second_colour in range(3)
        }
        | {
            9 * EDGE_ID[item] + 4 * colour
            for item, colour in labels.items()
        }
    )
    positions = {
        variable: position
        for position, variable in enumerate(support_variables)
    }
    relation_rows = [
        parse_relation(row["signature"])
        for row in proof["factor_relations"]
    ]
    if [
        int(row["relation_id"])
        for row in proof["factor_relations"]
    ] != list(range(len(relation_rows))):
        raise AssertionError("factor relation IDs changed")
    dense_rows = [dense(row, positions) for row in relation_rows]
    clauses = [
        tuple(map(int, row)) for row in proof["factor_clauses"]
    ]
    origins = proof["factor_clause_origins"]
    if (
        len(clauses) != len(origins)
        or len(set(clauses)) != len(clauses)
    ):
        raise AssertionError("factor clause origins are incomplete")

    unit_replays = 0
    binary_replays = 0
    for clause, origin in zip(clauses, origins, strict=True):
        if any(
            literal <= 0 or literal > len(relation_rows)
            for literal in clause
        ):
            raise AssertionError("factor clause literal out of range")
        equation = int(origin["equation_index"])
        colouring = indexed_colouring(equation)
        if local_code(colouring, forced_cycle) not in forced_codes:
            raise AssertionError("factor clause is outside forced slice")
        matching_ids = tuple(map(int, origin["matching_ids"]))
        vectors = tuple(
            monomial_variables(
                matchings[matching_id],
                colouring,
                labels,
                full_edges,
            )
            for matching_id in matching_ids
        )
        if len(clause) == 1:
            if origin["certificate_mode"] != (
                "forced_two_extra_relation"
            ):
                raise AssertionError("unit clause mode changed")
            extras_activity(
                equation, matching_ids, baseline + 2
            )
            if relation(*vectors) != relation_rows[clause[0] - 1]:
                raise AssertionError("unit relation changed")
            unit_replays += 1
        elif len(clause) == 2:
            if origin["certificate_mode"] != (
                "four_extra_parallelogram_factor"
            ):
                raise AssertionError("binary clause mode changed")
            extras_activity(
                equation, matching_ids, baseline + 4
            )
            directions = parallelogram_directions(vectors)
            if directions is None or {
                relation_rows[literal - 1] for literal in clause
            } != set(directions):
                raise AssertionError(
                    "four-extra factor clause changed"
                )
            binary_replays += 1
        else:
            raise AssertionError("unexpected factor-clause arity")
    if (
        unit_replays != int(proof["unit_clause_count"])
        or binary_replays != int(proof["binary_clause_count"])
    ):
        raise AssertionError("factor clause counts changed")

    # Replay each exact lattice no-good from raw relation vectors.
    learned = [list(map(int, row)) for row in proof["learned_clauses"]]
    branches = proof["branches"]
    if len(learned) != len(branches):
        raise AssertionError("learned branch catalogue changed")
    lattice_conflicts_replayed = 0
    for learned_clause, branch in zip(
        learned, branches, strict=True
    ):
        certificate = branch["certificate"]
        mode = certificate["certificate_mode"]
        basis_ids = list(
            map(int, certificate["basis_relation_ids"])
        )
        if len(set(basis_ids)) != len(basis_ids):
            raise AssertionError("lattice basis IDs repeat")
        basis = [dense_rows[index] for index in basis_ids]
        expected_block = set(basis_ids)
        if mode == "inconsistent_factor_sign":
            target_id = int(certificate["target_relation_id"])
            coordinates = basis_coordinates(
                basis, dense_rows[target_id]
            )
            if (
                coordinates is None
                or sum(coordinates) % 2
                or coordinates
                != list(
                    map(int, certificate["target_coordinates"])
                )
            ):
                raise AssertionError(
                    "inconsistent-sign conflict changed"
                )
            expected_block.add(target_id)
        elif mode == "isolated_factor_lattice_class":
            equation = int(certificate["target_equation_index"])
            matching_ids = tuple(
                map(int, certificate["target_matching_ids"])
            )
            extras_activity(
                equation,
                matching_ids,
                baseline + len(matching_ids),
            )
            colouring = indexed_colouring(equation)
            if local_code(
                colouring, forced_cycle
            ) not in forced_codes:
                raise AssertionError(
                    "lattice target is outside forced slice"
                )
            vectors = tuple(
                monomial_variables(
                    matchings[matching_id],
                    colouring,
                    labels,
                    full_edges,
                )
                for matching_id in matching_ids
            )
            groups: list[dict[str, object]] = []
            for matching_id, vector in zip(
                matching_ids, vectors, strict=True
            ):
                placed = False
                for group in groups:
                    signed: Counter[int] = Counter(vector)
                    signed.subtract(group["representative"])
                    coordinates = basis_coordinates(
                        basis,
                        dense(canonical_sparse(signed), positions),
                    )
                    if coordinates is None:
                        continue
                    sign = -1 if sum(coordinates) % 2 else 1
                    group["coefficient"] = (
                        int(group["coefficient"]) + sign
                    )
                    placed = True
                    break
                if not placed:
                    groups.append(
                        {
                            "representative": vector,
                            "coefficient": 1,
                        }
                    )
            coefficients = [
                int(group["coefficient"]) for group in groups
            ]
            if (
                sum(coefficient != 0 for coefficient in coefficients)
                != 1
                or coefficients
                != list(
                    map(
                        int,
                        certificate[
                            "signed_class_coefficients"
                        ],
                    )
                )
            ):
                raise AssertionError(
                    "isolated signed class changed"
                )
        else:
            raise AssertionError(
                f"unsupported lattice conflict mode: {mode}"
            )
        expected_clause = [
            -(index + 1) for index in sorted(expected_block)
        ]
        if learned_clause != expected_clause or list(
            map(int, branch["blocking_clause"])
        ) != expected_clause:
            raise AssertionError("learned blocking clause changed")
        lattice_conflicts_replayed += 1

    with Solver(name="glucose4", bootstrap_with=clauses) as solver:
        if not solver.solve():
            raise AssertionError(
                "base factor-choice CNF unexpectedly UNSAT"
            )
    with Solver(
        name="glucose4", bootstrap_with=[*clauses, *learned]
    ) as solver:
        if solver.solve():
            raise AssertionError(
                "independent final factor-choice CNF is SAT"
            )

    output = {
        "verified": True,
        "status": "forced_slice_factor_choice_unsat_verified",
        "scope": (
            "the fixed C4+C4+C6 support sample at survivor index 15; "
            "not the complete C4+C4+C6 family"
        ),
        "certificate": str(args.certificate),
        "certificate_sha256": sha256(args.certificate),
        "forced_cycle_analysis": str(forced_path),
        "forced_cycle_analysis_sha256": sha256(forced_path),
        "exploration": str(exploration_path),
        "exploration_sha256": sha256(exploration_path),
        "full_cycle_type": list(lengths),
        "survivor_index": int(proof["survivor_index"]),
        "skeleton_perfect_matchings": len(matchings),
        "matching_extensions_accumulated": total_extensions,
        "conditional_factor_forks_replayed": (
            conditional_forks_replayed
        ),
        "forced_local_codes": sorted(forced_codes),
        "unit_factor_clauses_replayed": unit_replays,
        "binary_factor_clauses_replayed": binary_replays,
        "factor_relations": len(relation_rows),
        "lattice_conflicts_replayed": lattice_conflicts_replayed,
        "final_cnf_variables": len(relation_rows),
        "final_cnf_clauses": len(clauses) + len(learned),
        "independent_solver": "glucose4",
        "independent_unsat": True,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(output, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
