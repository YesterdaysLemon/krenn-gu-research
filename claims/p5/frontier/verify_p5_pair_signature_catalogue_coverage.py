"""Compare abstract complex-valid pair axioms with the F5 pattern catalogue."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import pathlib
import sys
from fractions import Fraction

from pysat.formula import CNF, IDPool
from pysat.solvers import Solver


for _p in pathlib.Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402
from krenn_gu.p5_pair_catalogue import (  # noqa: E402
    finite_field_local_signatures,
)

REPO_ROOT, ROOT = bootstrap(__file__)
from krenn_gu.integer_constant_lattice import IntegerConstantLattice  # noqa: E402

SOURCES = tuple(range(5))
COLOURS = tuple(range(3))
PAIRS = tuple(itertools.combinations(SOURCES, 2))
PAIR_INDEX = {pair: index for index, pair in enumerate(PAIRS)}


def add_and_equivalence(
    cnf: CNF, output: int, factors: list[int]
) -> None:
    for factor in factors:
        cnf.append([-output, factor])
    cnf.append([output] + [-factor for factor in factors])


def x(pool: IDPool, source: int, colour: int) -> int:
    return pool.id(("x", source, colour))


def y(pool: IDPool, pair_index: int, colour: int) -> int:
    return pool.id(("y", pair_index, colour))


def singleton(pool: IDPool, source: int, colour: int) -> int:
    return pool.id(("singleton", source, colour))


def exact_mask_escape(
    pool: IDPool, source: int, mask: int
) -> list[int]:
    return [
        -x(pool, source, colour)
        if mask & (1 << colour)
        else x(pool, source, colour)
        for colour in COLOURS
    ]


def build_local_cnf() -> tuple[CNF, IDPool]:
    cnf = CNF()
    pool = IDPool()

    for source in SOURCES:
        for colour in COLOURS:
            witness = singleton(pool, source, colour)
            selected = x(pool, source, colour)
            others = [
                x(pool, source, other)
                for other in COLOURS
                if other != colour
            ]
            cnf.append([-witness, selected])
            cnf.extend([[-witness, -other] for other in others])
            cnf.append([witness, -selected, *others])

    # Structural rank three.
    witnesses = []
    for injection in itertools.permutations(SOURCES, 3):
        witness = pool.id(("rank", injection))
        factors = [
            x(pool, injection[colour], colour)
            for colour in COLOURS
        ]
        add_and_equivalence(cnf, witness, factors)
        witnesses.append(witness)
    cnf.append(witnesses)

    for pair_index, (first, second) in enumerate(PAIRS):
        incidences = [
            y(pool, pair_index, colour) for colour in COLOURS
        ]
        cnf.append(incidences)
        cnf.append([-value for value in incidences])

        same = []
        for colour, incidence in enumerate(incidences):
            first_singleton = singleton(pool, first, colour)
            second_singleton = singleton(pool, second, colour)
            cnf.append([-first_singleton, incidence])
            cnf.append([-second_singleton, incidence])
            both = pool.id(("same", pair_index, colour))
            same.append(both)
            cnf.extend(
                [
                    [-both, first_singleton],
                    [-both, second_singleton],
                    [both, -first_singleton, -second_singleton],
                ]
            )

            coordinate = 1 << colour
            other_mask = 7 ^ coordinate
            for first_mask in range(8):
                for second_mask in range(8):
                    possible = (
                        first_mask == coordinate
                        or second_mask == coordinate
                        or (
                            (first_mask & other_mask) != 0
                            and (first_mask & other_mask)
                            == (second_mask & other_mask)
                            and bool(
                                (first_mask | second_mask)
                                & coordinate
                            )
                        )
                    )
                    if possible:
                        continue
                    cnf.append(
                        [
                            -incidence,
                            *exact_mask_escape(
                                pool, first, first_mask
                            ),
                            *exact_mask_escape(
                                pool, second, second_mask
                            ),
                        ]
                    )

        for left, right in itertools.combinations(COLOURS, 2):
            plane = (1 << left) | (1 << right)
            plane_supports = (1 << left, 1 << right, plane)
            for first_mask in plane_supports:
                for second_mask in plane_supports:
                    if first_mask | second_mask != plane:
                        continue
                    antecedent = [
                        *exact_mask_escape(pool, first, first_mask),
                        *exact_mask_escape(pool, second, second_mask),
                    ]
                    cnf.append([*antecedent, incidences[left]])
                    cnf.append([*antecedent, incidences[right]])

            excluded = next(
                colour
                for colour in COLOURS
                if colour not in (left, right)
            )
            for source in (first, second):
                cnf.append(
                    [
                        -incidences[left],
                        -incidences[right],
                        -x(pool, source, excluded),
                    ]
                )
            for colour in (left, right):
                cnf.append(
                    [
                        -incidences[left],
                        -incidences[right],
                        x(pool, first, colour),
                        x(pool, second, colour),
                    ]
                )

    for centre in SOURCES:
        others = tuple(source for source in SOURCES if source != centre)
        for first, second in itertools.combinations(others, 2):
            centre_first = PAIR_INDEX[tuple(sorted((centre, first)))]
            centre_second = PAIR_INDEX[
                tuple(sorted((centre, second)))
            ]
            outer = tuple(sorted((first, second)))
            outer_index = PAIR_INDEX[outer]
            for colour in COLOURS:
                cnf.append(
                    [
                        -y(pool, centre_first, colour),
                        -y(pool, centre_second, colour),
                        singleton(pool, centre, colour),
                        y(pool, outer_index, colour),
                        *[
                            pool.id(
                                (
                                    "same",
                                    outer_index,
                                    coordinate,
                                )
                            )
                            for coordinate in COLOURS
                        ],
                    ]
                )
    return cnf, pool


def local_geometry_contradiction(
    supports: tuple[int, ...], incidences: tuple[int, ...]
) -> str | None:
    variables = tuple(
        (source, colour)
        for source in SOURCES
        for colour in COLOURS
        if supports[source] & (1 << colour)
    )
    positions = {
        variable: index for index, variable in enumerate(variables)
    }
    rows = []
    for pair_index, (first, second) in enumerate(PAIRS):
        for coordinate in COLOURS:
            if not (incidences[pair_index] & (1 << coordinate)):
                continue
            other = tuple(
                colour
                for colour in COLOURS
                if colour != coordinate
            )
            first_term = (
                (first, other[0]),
                (second, other[1]),
            )
            second_term = (
                (first, other[1]),
                (second, other[0]),
            )
            first_active = all(
                variable in positions for variable in first_term
            )
            second_active = all(
                variable in positions for variable in second_term
            )
            if first_active != second_active:
                return "singleton_minor"
            if not first_active:
                continue
            first_vector = [0] * len(variables)
            second_vector = [0] * len(variables)
            for variable in first_term:
                first_vector[positions[variable]] += 1
            for variable in second_term:
                second_vector[positions[variable]] += 1
            rows.append(
                [
                    left - right
                    for left, right in zip(first_vector, second_vector)
                ]
            )
    lattice = IntegerConstantLattice(
        rows, [Fraction(1)] * len(rows)
    )

    for pair_index, (first, second) in enumerate(PAIRS):
        for coordinate in COLOURS:
            if not (incidences[pair_index] & (1 << coordinate)):
                continue
            coordinate_mask = 1 << coordinate
            if (
                supports[first] == coordinate_mask
                or supports[second] == coordinate_mask
            ):
                continue
            possible = False
            for other in COLOURS:
                if other == coordinate:
                    continue
                first_term = (
                    (first, coordinate),
                    (second, other),
                )
                second_term = (
                    (first, other),
                    (second, coordinate),
                )
                first_active = all(
                    variable in positions for variable in first_term
                )
                second_active = all(
                    variable in positions for variable in second_term
                )
                if first_active != second_active:
                    possible = True
                    continue
                if not first_active:
                    continue
                first_vector = [0] * len(variables)
                second_vector = [0] * len(variables)
                for variable in first_term:
                    first_vector[positions[variable]] += 1
                for variable in second_term:
                    second_vector[positions[variable]] += 1
                difference = [
                    left - right
                    for left, right in zip(
                        first_vector, second_vector
                    )
                ]
                if lattice.transported_constant(difference) != 1:
                    possible = True
            if not possible:
                return "forced_rank_one_pair"

    for source_triple in itertools.combinations(SOURCES, 3):
        groups: list[dict] = []
        for permutation in itertools.permutations(COLOURS):
            selected = tuple(
                (source, permutation[index])
                for index, source in enumerate(source_triple)
            )
            if not all(variable in positions for variable in selected):
                continue
            vector = [0] * len(variables)
            for variable in selected:
                vector[positions[variable]] += 1
            inversions = sum(
                permutation[left] > permutation[right]
                for left in range(3)
                for right in range(left + 1, 3)
            )
            sign = Fraction(-1 if inversions % 2 else 1)
            for group in groups:
                difference = [
                    left - right
                    for left, right in zip(
                        vector, group["representative"]
                    )
                ]
                transported = lattice.transported_constant(difference)
                if transported is None:
                    continue
                group["coefficient"] += sign * transported
                break
            else:
                groups.append(
                    {"representative": vector, "coefficient": sign}
                )
        if any(group["coefficient"] for group in groups):
            return None
    return "forced_rank_two_map"


def pattern_block_clause(
    pool: IDPool,
    supports: tuple[int, ...],
    incidences: tuple[int, ...],
) -> list[int]:
    clause = []
    for source in SOURCES:
        clause.extend(exact_mask_escape(pool, source, supports[source]))
    for pair_index, mask in enumerate(incidences):
        for colour in COLOURS:
            variable = y(pool, pair_index, colour)
            clause.append(
                -variable if mask & (1 << colour) else variable
            )
    return clause


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--records", type=pathlib.Path)
    parser.add_argument("--cnf", type=pathlib.Path)
    args = parser.parse_args()
    cnf, pool = build_local_cnf()
    catalogue = finite_field_local_signatures()
    pair_patterns = {
        (signature[0], signature[1][: len(PAIRS)])
        for signature in catalogue
    }
    for supports, incidences in pair_patterns:
        cnf.append(pattern_block_clause(pool, supports, incidences))

    with Solver(name="cadical195", bootstrap_with=cnf.clauses) as solver:
        excluded = 0
        exclusion_records = []
        while solver.solve():
            positive = {
                literal
                for literal in solver.get_model()
                if literal > 0
            }
            supports = tuple(
                sum(
                    (x(pool, source, colour) in positive) << colour
                    for colour in COLOURS
                )
                for source in SOURCES
            )
            incidences = tuple(
                sum(
                    (y(pool, pair_index, colour) in positive)
                    << colour
                    for colour in COLOURS
                )
                for pair_index in range(len(PAIRS))
            )
            contradiction = local_geometry_contradiction(
                supports, incidences
            )
            if contradiction is None:
                print(
                    {
                        "variables": pool.top,
                        "clauses": len(cnf.clauses),
                        "catalogue_pair_patterns": len(pair_patterns),
                        "locally_contradictory_outside_patterns": excluded,
                        "algebraically_viable_pattern_outside_catalogue": True,
                        "supports": supports,
                        "pair_incidences": incidences,
                    }
                )
                return
            solver.add_clause(
                pattern_block_clause(pool, supports, incidences)
            )
            clause = pattern_block_clause(pool, supports, incidences)
            cnf.append(clause)
            exclusion_records.append(
                {
                    "supports": supports,
                    "pair_incidences": incidences,
                    "contradiction": contradiction,
                    "clause": clause,
                }
            )
            excluded += 1
            if excluded % 1000 == 0:
                print(
                    {
                        "locally_contradictory_outside_patterns": excluded,
                        "last_contradiction": contradiction,
                    },
                    flush=True,
                )
        if args.records is not None:
            args.records.parent.mkdir(parents=True, exist_ok=True)
            args.records.write_text(
                json.dumps(
                    {
                        "catalogue_pair_patterns": len(pair_patterns),
                        "outside_exclusions": exclusion_records,
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
        if args.cnf is not None:
            args.cnf.parent.mkdir(parents=True, exist_ok=True)
            cnf.to_file(args.cnf)
        print(
            {
                "variables": pool.top,
                "clauses": len(cnf.clauses),
                "catalogue_pair_patterns": len(pair_patterns),
                "locally_contradictory_outside_patterns": excluded,
                "algebraically_viable_pattern_outside_catalogue": False,
                "records": (
                    None if args.records is None else str(args.records)
                ),
                "records_sha256": (
                    None
                    if args.records is None
                    else hashlib.sha256(args.records.read_bytes()).hexdigest()
                ),
                "cnf": None if args.cnf is None else str(args.cnf),
                "cnf_sha256": (
                    None
                    if args.cnf is None
                    else hashlib.sha256(args.cnf.read_bytes()).hexdigest()
                ),
            }
        )


if __name__ == "__main__":
    main()
