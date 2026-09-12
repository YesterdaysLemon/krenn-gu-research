"""Independent experimental encoding of recursive hafnian zero patterns.

This audit intentionally does not import the primary CNF builder.  It uses
integer subset masks, ordered Laplace-term variables, ordered partitions from
disjoint submasks, and Glucose 4.1.  Agreement remains same-author evidence;
it is not a socially independent review or a checked UNSAT certificate.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

from pysat.formula import CNF, IDPool
from pysat.solvers import Glucose4


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def even_masks(n: int, minimum_size: int = 0):
    for mask in range(1 << n):
        size = mask.bit_count()
        if size >= minimum_size and size % 2 == 0:
            yield mask


def vertices(mask: int, n: int) -> list[int]:
    return [vertex for vertex in range(n) if mask & (1 << vertex)]


def ordered_even_partitions(n: int):
    whole = (1 << n) - 1
    for first in even_masks(n):
        remaining = whole ^ first
        second = remaining
        while True:
            if second.bit_count() % 2 == 0:
                yield first, second, remaining ^ second
            if second == 0:
                break
            second = (second - 1) & remaining


def fixed_matching_pair(
    n: int,
    cycle_type: tuple[int, ...],
) -> tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]]:
    if not cycle_type or any(part < 1 for part in cycle_type):
        raise ValueError("cycle type must have positive parts")
    if sum(cycle_type) != n // 2:
        raise ValueError("cycle type must partition n/2")
    first = tuple((vertex, vertex + 1) for vertex in range(0, n, 2))
    second = []
    offset = 0
    for part in cycle_type:
        atoms = list(range(offset, offset + part))
        if part == 1:
            atom = atoms[0]
            second.append((2 * atom, 2 * atom + 1))
        else:
            for position, atom in enumerate(atoms):
                next_atom = atoms[(position + 1) % part]
                second.append(
                    tuple(sorted((2 * atom + 1, 2 * next_atom)))
                )
        offset += part
    return first, tuple(sorted(second))


def build(
    n: int,
    cycle_type: tuple[int, ...] | None = None,
    third_cycle_type: tuple[int, ...] | None = None,
) -> tuple[CNF, IDPool, dict[str, int]]:
    if n < 4 or n % 2:
        raise ValueError("n must be even and at least four")

    pool = IDPool()
    cnf = CNF()
    whole = (1 << n) - 1
    large_even_masks = tuple(even_masks(n, minimum_size=4))
    edge = {
        (colour, u, v): pool.id(("E", colour, u, v))
        for colour in range(3)
        for u in range(n)
        for v in range(u + 1, n)
    }
    hafnian = {
        (colour, mask): pool.id(("H", colour, mask))
        for colour in range(3)
        for mask in large_even_masks
    }

    def edge_lit(colour: int, u: int, v: int) -> int:
        return edge[(colour, min(u, v), max(u, v))]

    def hafnian_lit(colour: int, mask: int) -> int | None:
        size = mask.bit_count()
        if size == 0:
            return None
        if size == 2:
            u, v = vertices(mask, n)
            return edge_lit(colour, u, v)
        return hafnian[(colour, mask)]

    product_definition = 0
    accessibility = 0
    singleton_cancellation = 0
    for colour in range(3):
        for mask in large_even_masks:
            result = hafnian[(colour, mask)]
            members = vertices(mask, n)
            for vertex in members:
                terms = []
                for partner in members:
                    if partner == vertex:
                        continue
                    term = pool.id(("T", colour, mask, vertex, partner))
                    terms.append(term)
                    remainder = mask ^ (1 << vertex) ^ (1 << partner)
                    remainder_lit = hafnian_lit(colour, remainder)
                    if remainder_lit is None:
                        raise AssertionError("large sets have nonempty remainder")
                    incident_edge = edge_lit(colour, vertex, partner)
                    cnf.append([-term, incident_edge])
                    cnf.append([-term, remainder_lit])
                    cnf.append([term, -incident_edge, -remainder_lit])
                    product_definition += 3
                cnf.append([-result, *terms])
                accessibility += 1
                for position, term in enumerate(terms):
                    cnf.append(
                        [-term, result, *terms[:position], *terms[position + 1 :]]
                    )
                    singleton_cancellation += 1

    for colour in range(3):
        cnf.append([hafnian[(colour, whole)]])

    symmetry = 0
    if third_cycle_type is not None:
        if cycle_type != (1,) * (n // 2):
            raise ValueError(
                "third cycle split requires coincident first matchings"
            )
    if cycle_type is not None:
        first, second = fixed_matching_pair(n, cycle_type)
        for u, v in first:
            cnf.append([edge_lit(0, u, v)])
            symmetry += 1
        for u, v in second:
            cnf.append([edge_lit(1, u, v)])
            symmetry += 1
    if third_cycle_type is not None:
        _first, third = fixed_matching_pair(n, third_cycle_type)
        for u, v in third:
            cnf.append([edge_lit(2, u, v)])
            symmetry += 1

    rainbow = 0
    for parts in ordered_even_partitions(n):
        if sum(mask != 0 for mask in parts) < 2:
            continue
        clause = []
        for colour, mask in enumerate(parts):
            literal = hafnian_lit(colour, mask)
            if literal is not None:
                clause.append(-literal)
        cnf.append(clause)
        rainbow += 1

    counts = {
        "product_definition": product_definition,
        "nonzero_accessibility": accessibility,
        "singleton_cancellation": singleton_cancellation,
        "rainbow": rainbow,
        "constant_words": 3,
        "matching_symmetry": symmetry,
    }
    return cnf, pool, counts


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--dimacs", type=Path, required=True)
    parser.add_argument("--cycle-type")
    parser.add_argument("--third-cycle-type")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cycle_type = (
        tuple(int(part) for part in args.cycle_type.split("+"))
        if args.cycle_type
        else None
    )
    third_cycle_type = (
        tuple(int(part) for part in args.third_cycle_type.split("+"))
        if args.third_cycle_type
        else None
    )
    started = time.perf_counter()
    cnf, pool, counts = build(
        args.n,
        cycle_type=cycle_type,
        third_cycle_type=third_cycle_type,
    )
    build_seconds = time.perf_counter() - started
    args.dimacs.parent.mkdir(parents=True, exist_ok=True)
    cnf.to_file(str(args.dimacs))
    solve_started = time.perf_counter()
    with Glucose4(bootstrap_with=cnf.clauses) as solver:
        satisfiable = solver.solve()
    solve_seconds = time.perf_counter() - solve_started
    payload = {
        "audit": "independent_ordered_term_encoding",
        "independence": "same_author_different_representation_and_solver",
        "n": args.n,
        "cycle_type": list(cycle_type) if cycle_type else None,
        "third_cycle_type": (
            list(third_cycle_type) if third_cycle_type else None
        ),
        "result": "SAT" if satisfiable else "UNSAT",
        "evidence": (
            "explicit_boolean_model"
            if satisfiable
            else "solver_status_without_independently_checked_proof_trace"
        ),
        "solver": "Glucose 4.1 via python-sat",
        "variables": pool.top,
        "clauses": len(cnf.clauses),
        "clause_families": counts,
        "build_seconds": round(build_seconds, 6),
        "solve_seconds": round(solve_seconds, 6),
        "dimacs": str(args.dimacs.resolve()),
        "dimacs_sha256": sha256_file(args.dimacs),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
