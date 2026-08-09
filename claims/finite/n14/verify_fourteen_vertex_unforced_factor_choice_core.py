"""Independent replay of a compact unforced factor-choice core.

The verifier does not import the certificate producer.  It reconstructs the
fixed order-14 support, its perfect matchings, every reported factor relation,
the small dual-Horn clause core from the recorded source equations, and the
terminal exact signed-lattice contradiction.

This proves only that the fixed support named by the certificate is impossible.
It does not resolve the complete graph-theory conjecture.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter, deque
from pathlib import Path
from typing import Iterable, Sequence

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
    return (first, second) if first < second else (second, first)


def cycle_edges(cycle: Sequence[int]) -> tuple[Edge, ...]:
    return tuple(
        edge(cycle[index], cycle[(index + 1) % len(cycle)])
        for index in range(len(cycle))
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
    if index < 0 or index >= EQUATIONS:
        raise AssertionError("equation index is outside the order-14 cube")
    return tuple(
        (index // (3**vertex)) % 3 for vertex in range(N)
    )


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


def active_matching_ids(
    equation: int,
    matchings: Sequence[Factor],
    labels: dict[Edge, int],
) -> tuple[int, ...]:
    colouring = indexed_colouring(equation)
    return tuple(
        matching_id
        for matching_id, matching in enumerate(matchings)
        if matching_active(matching, colouring, labels)
    )


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


def cycle_relation(
    cycle: Sequence[int],
    colouring: Sequence[int],
    labels: dict[Edge, int],
    full_edges: frozenset[Edge],
) -> SparseRelation:
    edges = cycle_edges(cycle)
    vectors = tuple(
        monomial_variables(
            matching, colouring, labels, full_edges
        )
        for matching in (edges[0::2], edges[1::2])
    )
    output = relation(*vectors)
    if not output:
        raise AssertionError("cycle alternatings became one monomial")
    return output


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


def exact_activity(
    equation: int,
    matchings: Sequence[Factor],
    labels: dict[Edge, int],
    full_only: frozenset[int],
    expected_size: int,
) -> tuple[int, ...]:
    active = active_matching_ids(equation, matchings, labels)
    if (
        len(active) != expected_size
        or not full_only.issubset(active)
        or len(set(indexed_colouring(equation))) == 1
    ):
        raise AssertionError("source equation activity changed")
    return tuple(
        matching_id
        for matching_id in active
        if matching_id not in full_only
    )


def dual_horn_forces(
    clauses: Sequence[Sequence[int]], target: int
) -> bool:
    if target < 1:
        raise AssertionError("target variable must be positive")
    if any(
        sum(int(literal) < 0 for literal in clause) > 1
        for clause in clauses
    ):
        raise AssertionError("reported core is not dual-Horn")
    false_variables = {target}
    changed = True
    while changed:
        changed = False
        for clause in clauses:
            positives = {
                int(literal)
                for literal in clause
                if int(literal) > 0
            }
            if not positives.issubset(false_variables):
                continue
            negatives = [
                -int(literal)
                for literal in clause
                if int(literal) < 0
            ]
            if not negatives:
                return True
            antecedent = negatives[0]
            if antecedent not in false_variables:
                false_variables.add(antecedent)
                changed = True
    return False


def dual_horn_unsat(clauses: Sequence[Sequence[int]]) -> bool:
    """Check a dual-Horn contradiction by independent false propagation."""

    if any(
        sum(int(literal) < 0 for literal in clause) > 1
        for clause in clauses
    ):
        raise AssertionError("reported core is not dual-Horn")
    false_variables: set[int] = set()
    changed = True
    while changed:
        changed = False
        for clause in clauses:
            positives = {
                int(literal)
                for literal in clause
                if int(literal) > 0
            }
            if not positives.issubset(false_variables):
                continue
            negatives = [
                -int(literal)
                for literal in clause
                if int(literal) < 0
            ]
            if not negatives:
                return True
            antecedent = negatives[0]
            if antecedent not in false_variables:
                false_variables.add(antecedent)
                changed = True
    return False


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "certificate",
        type=Path,
        nargs="?",
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_orbit3_support0_"
            "unforced_factor_choice_core_r100.json"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_c4_c4_c6_orbit3_support0_"
            "unforced_factor_choice_core_r100_verified.json"
        ),
    )
    args = parser.parse_args()
    proof = json.loads(args.certificate.read_text(encoding="utf-8"))
    if (
        proof.get("status") != "UNSAT"
        or proof.get("necessary_conditions_only")
        or not proof.get("compact_output")
    ):
        raise AssertionError("producer did not report compact UNSAT")

    lengths = tuple(map(int, proof["full_cycle_type"]))
    cycles = contiguous_cycles(lengths)
    if len(cycles) < 2 or any(len(cycle) % 2 for cycle in cycles):
        raise AssertionError("certificate is not an all-even support")
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
    if any(
        len(factor) != N // 2
        or len({vertex for item in factor for vertex in item}) != N
        for factor in factors
    ):
        raise AssertionError(
            "an embedded singleton factor is not a perfect matching"
        )
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
    total_extensions = sum(
        3
        ** (
            N
            - len(
                {
                    vertex
                    for item in matching
                    if item in labels
                    for vertex in item
                }
            )
        )
        for matching in matchings
    )
    if total_extensions != int(
        proof["matching_extensions_accumulated"]
    ):
        raise AssertionError("matching extension count changed")

    relation_records = proof["factor_relations"]
    if [
        int(row["relation_id"]) for row in relation_records
    ] != list(range(len(relation_records))):
        raise AssertionError("factor relation IDs changed")
    relations = [
        parse_relation(row["signature"]) for row in relation_records
    ]
    if len(set(relations)) != len(relations):
        raise AssertionError("factor relation catalogue has duplicates")
    if len(relations) != int(proof["factor_relation_count"]):
        raise AssertionError("factor relation count changed")
    relation_ids = {
        signature: relation_id
        for relation_id, signature in enumerate(relations)
    }

    def relation_id(signature: SparseRelation) -> int:
        if signature not in relation_ids:
            raise AssertionError(
                "semantic relation is absent from the catalogue"
            )
        return relation_ids[signature]

    def cycle_ids_at(equation: int) -> tuple[int, ...]:
        colouring = indexed_colouring(equation)
        return tuple(
            relation_id(
                cycle_relation(
                    cycle, colouring, labels, full_edges
                )
            )
            for cycle in cycles
        )

    # Recompute all reported relation signatures from their first origins.
    relation_origins_replayed = 0
    for relation_id_value, row in enumerate(relation_records):
        origin = row["origin"]
        mode = origin["certificate_mode"]
        equation = int(origin["equation_index"])
        colouring = indexed_colouring(equation)
        if mode == "full_cycle_binomial":
            cycle_id = int(origin["cycle_id"])
            if (
                cycle_id < 0
                or cycle_id >= len(cycles)
                or tuple(map(int, origin["cycle"]))
                != cycles[cycle_id]
            ):
                raise AssertionError("cycle relation origin changed")
            reconstructed = cycle_relation(
                cycles[cycle_id],
                colouring,
                labels,
                full_edges,
            )
        elif mode == "two_extra_relation":
            extras = exact_activity(
                equation,
                matchings,
                labels,
                full_only,
                baseline + 2,
            )
            if extras != tuple(map(int, origin["matching_ids"])):
                raise AssertionError("two-extra origin changed")
            vectors = tuple(
                monomial_variables(
                    matchings[matching_id],
                    colouring,
                    labels,
                    full_edges,
                )
                for matching_id in extras
            )
            reconstructed = relation(*vectors)
        elif mode == "four_extra_parallelogram_factor":
            extras = exact_activity(
                equation,
                matchings,
                labels,
                full_only,
                baseline + 4,
            )
            if extras != tuple(map(int, origin["matching_ids"])):
                raise AssertionError("four-extra origin changed")
            vectors = tuple(
                monomial_variables(
                    matchings[matching_id],
                    colouring,
                    labels,
                    full_edges,
                )
                for matching_id in extras
            )
            directions = parallelogram_directions(vectors)
            if (
                directions is None
                or relations[relation_id_value] not in directions
            ):
                raise AssertionError(
                    "parallelogram relation origin changed"
                )
            reconstructed = relations[relation_id_value]
        else:
            raise AssertionError(
                f"unknown factor relation mode: {mode}"
            )
        if reconstructed != relations[relation_id_value]:
            raise AssertionError("factor relation signature changed")
        relation_origins_replayed += 1

    def semantic_clauses_at(equation: int) -> set[tuple[int, ...]]:
        if len(set(indexed_colouring(equation))) == 1:
            raise AssertionError(
                "required monochromatic amplitude used as a zero equation"
            )
        active = active_matching_ids(equation, matchings, labels)
        if not full_only.issubset(active):
            raise AssertionError("source lost a full-only matching")
        extras = tuple(
            matching_id
            for matching_id in active
            if matching_id not in full_only
        )
        cycle_ids = cycle_ids_at(equation)
        if not extras:
            return {
                tuple(
                    sorted(
                        {
                            cycle_id + 1
                            for cycle_id in cycle_ids
                        }
                    )
                )
            }
        colouring = indexed_colouring(equation)
        vectors = tuple(
            monomial_variables(
                matchings[matching_id],
                colouring,
                labels,
                full_edges,
            )
            for matching_id in extras
        )
        if len(extras) == 1:
            return {
                (-(cycle_id + 1),)
                for cycle_id in cycle_ids
            }
        if len(extras) == 2:
            extra_id = relation_id(relation(*vectors))
            return {
                (-(cycle_id + 1), extra_id + 1)
                for cycle_id in cycle_ids
            }
        if len(extras) == 4:
            directions = parallelogram_directions(vectors)
            if directions is None:
                return set()
            direction_ids = tuple(
                sorted(
                    {
                        relation_id(direction)
                        for direction in directions
                    }
                )
            )
            return {
                (
                    -(cycle_id + 1),
                    *(item_id + 1 for item_id in direction_ids),
                )
                for cycle_id in cycle_ids
            }
        raise AssertionError(
            "core source is not a full-only, ten-, or twelve-term row"
        )

    core = proof["dual_horn_core"]
    if (
        core.get("status")
        not in {
            "UNSAT_dual_horn_base_core",
            "UNSAT_dual_horn_forcing_core",
        }
        or not core.get("core_plus_blocking_unsat")
    ):
        raise AssertionError("dual-Horn core status changed")
    core_clauses = [
        tuple(map(int, clause))
        for clause in core["core_factor_clauses"]
    ]
    core_equations = list(
        map(int, core["core_factor_clause_equations"])
    )
    core_indices = list(
        map(int, core["core_factor_clause_indices"])
    )
    if (
        len(core_clauses)
        != int(core["core_factor_clause_count"])
        or len(core_clauses) != len(core_equations)
        or len(core_clauses) != len(core_indices)
        or len(set(core_clauses)) != len(core_clauses)
        or core_indices != sorted(set(core_indices))
    ):
        raise AssertionError("dual-Horn core catalogue changed")
    for clause, equation in zip(
        core_clauses, core_equations, strict=True
    ):
        if clause not in semantic_clauses_at(equation):
            raise AssertionError(
                "core clause does not follow from its source equation"
            )

    branches = proof["branches"]
    learned = [
        list(map(int, clause)) for clause in proof["learned_clauses"]
    ]
    if core["status"] == "UNSAT_dual_horn_base_core":
        if (
            branches
            or learned
            or list(map(int, core["blocking_clause"]))
            or len(core["forcing_proofs"]) != 1
            or not dual_horn_unsat(core_clauses)
        ):
            raise AssertionError(
                "base dual-Horn contradiction structure changed"
            )
        # PySAT's constructor does not uniformly accept an explicit empty
        # clause.  An independently reconstructed empty clause is already
        # an immediate contradiction; otherwise retain the separate
        # Glucose replay.
        if not any(not clause for clause in core_clauses):
            with Solver(
                name="glucose4", bootstrap_with=core_clauses
            ) as solver:
                if solver.solve():
                    raise AssertionError(
                        "independently replayed base core became SAT"
                    )
        output = {
            "verified": True,
            "status": (
                "unforced_factor_choice_dual_horn_base_core_verified"
            ),
            "scope": (
                "one fixed all-even order-14 support at the "
                "certificate's survivor index; not the complete family"
            ),
            "certificate": str(args.certificate),
            "certificate_sha256": sha256(args.certificate),
            "recorded_exploration": str(proof["exploration"]),
            "recorded_exploration_sha256": proof[
                "exploration_sha256"
            ],
            "full_cycle_type": list(lengths),
            "survivor_index": int(proof["survivor_index"]),
            "skeleton_perfect_matchings": len(matchings),
            "full_only_matching_count": len(full_only),
            "matching_extensions_accumulated": total_extensions,
            "factor_relations_replayed": relation_origins_replayed,
            "core_factor_clauses_replayed": len(core_clauses),
            "core_source_equations_replayed": len(core_equations),
            "independent_dual_horn_base_propagation": True,
            "independent_core_unsat": True,
            "independent_solver": "glucose4",
            "global_conjecture_resolved": False,
        }
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(output, indent=2) + "\n",
            encoding="utf-8",
        )
        print(json.dumps(output, indent=2))
        return

    if len(branches) != 1 or len(learned) != 1:
        raise AssertionError("terminal branch catalogue changed")
    branch = branches[0]
    certificate = branch["certificate"]
    if (
        certificate["certificate_mode"]
        != "isolated_factor_lattice_class"
    ):
        raise AssertionError("unexpected lattice certificate mode")
    basis_ids = list(
        map(int, certificate["basis_relation_ids"])
    )
    if (
        not basis_ids
        or len(set(basis_ids)) != len(basis_ids)
        or any(
            relation_id_value < 0
            or relation_id_value >= len(relations)
            for relation_id_value in basis_ids
        )
    ):
        raise AssertionError("lattice basis IDs changed")

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
    dense_rows = [
        dense(signature, positions) for signature in relations
    ]
    basis = [dense_rows[relation_id_value] for relation_id_value in basis_ids]

    target_equation = int(
        certificate["target_equation_index"]
    )
    target_matching_ids = tuple(
        map(int, certificate["target_matching_ids"])
    )
    target_active = active_matching_ids(
        target_equation, matchings, labels
    )
    target_extras = tuple(
        matching_id
        for matching_id in target_active
        if matching_id not in full_only
    )
    if (
        target_matching_ids != target_extras
        or len(set(indexed_colouring(target_equation))) == 1
    ):
        raise AssertionError("target amplitude activity changed")
    trigger_id = int(
        certificate["target_trigger_relation_id"]
    )
    if trigger_id not in cycle_ids_at(target_equation):
        raise AssertionError(
            "target trigger is not a cycle cancellation at the target"
        )

    colouring = indexed_colouring(target_equation)
    vectors = tuple(
        monomial_variables(
            matchings[matching_id],
            colouring,
            labels,
            full_edges,
        )
        for matching_id in target_matching_ids
    )
    groups: list[dict[str, object]] = []
    for vector in vectors:
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
            break
        else:
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
        sum(coefficient != 0 for coefficient in coefficients) != 1
        or coefficients
        != list(
            map(
                int,
                certificate["signed_class_coefficients"],
            )
        )
    ):
        raise AssertionError(
            "target no longer has one isolated signed lattice class"
        )

    expected_block = [
        -(relation_id_value + 1)
        for relation_id_value in sorted(
            {*basis_ids, trigger_id}
        )
    ]
    blocking_clause = list(
        map(int, branch["blocking_clause"])
    )
    if (
        blocking_clause != expected_block
        or learned != [expected_block]
        or list(map(int, core["blocking_clause"]))
        != expected_block
    ):
        raise AssertionError("terminal lattice blocking clause changed")
    forcing_proofs = core["forcing_proofs"]
    if sorted(
        int(item["target_variable"])
        for item in forcing_proofs
    ) != sorted(-literal for literal in expected_block):
        raise AssertionError("dual-Horn forcing targets changed")
    if any(
        not dual_horn_forces(core_clauses, -literal)
        for literal in expected_block
    ):
        raise AssertionError(
            "independent dual-Horn propagation did not close"
        )
    with Solver(
        name="glucose4", bootstrap_with=core_clauses
    ) as solver:
        if not solver.solve():
            raise AssertionError(
                "factor core alone unexpectedly became UNSAT"
            )
    blocked_formula = [*core_clauses, expected_block]
    if not any(not clause for clause in blocked_formula):
        with Solver(
            name="glucose4",
            bootstrap_with=blocked_formula,
        ) as solver:
            if solver.solve():
                raise AssertionError(
                    "factor core plus exact lattice block became SAT"
                )

    output = {
        "verified": True,
        "status": (
            "unforced_factor_choice_dual_horn_lattice_core_verified"
        ),
        "scope": (
            "one fixed C4+C4+C6 order-14 support at the certificate's "
            "survivor index; not the complete C4+C4+C6 family"
        ),
        "certificate": str(args.certificate),
        "certificate_sha256": sha256(args.certificate),
        "recorded_exploration": str(proof["exploration"]),
        "recorded_exploration_sha256": proof[
            "exploration_sha256"
        ],
        "full_cycle_type": list(lengths),
        "survivor_index": int(proof["survivor_index"]),
        "skeleton_perfect_matchings": len(matchings),
        "full_only_matching_count": len(full_only),
        "matching_extensions_accumulated": total_extensions,
        "factor_relations_replayed": relation_origins_replayed,
        "core_factor_clauses_replayed": len(core_clauses),
        "core_source_equations_replayed": len(core_equations),
        "target_equation_replayed": target_equation,
        "target_extra_matching_count": len(target_matching_ids),
        "lattice_basis_size": len(basis_ids),
        "isolated_signed_class_coefficients": coefficients,
        "independent_dual_horn_forcing": True,
        "independent_core_sat": True,
        "independent_core_plus_lattice_block_unsat": True,
        "independent_solver": "glucose4",
        "global_conjecture_resolved": False,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
