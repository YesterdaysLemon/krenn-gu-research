#!/usr/bin/env python3
"""Independent modular audit of the rank-five catalecticant checkpoint."""

from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PRIMARY = ROOT / "tmp" / "p6_common_port_111_rank_five_catalecticant_verified.json"
OUTPUT = ROOT / "tmp" / "p6_common_port_111_rank_five_catalecticant_audited.json"
PAIRS = tuple(itertools.combinations(range(5), 2))
TRIPLES = tuple(itertools.combinations(range(5), 3))
PRIMES = (5, 7, 11)

VECTORS = {
    "x01": (0, -1, -1, 0, 0),
    "x02": (1, 0, 0, 0, -2),
    "x10": (0, 0, 0, -1, 1),
    "x12": (-1, 0, 1, 0, 0),
    "x20": (-1, 1, 0, 0, 0),
    "x21": (1, 0, 0, 2, 0),
}
BAD_NAMES = (
    ("x10", "x21"),
    ("x12", "x20"),
    ("x12", "x21"),
    ("x01", "x20"),
    ("x02", "x20"),
    ("x02", "x21"),
    ("x01", "x10"),
    ("x01", "x12"),
    ("x02", "x10"),
)
GOOD_NAMES = (("x10", "x20"), ("x01", "x21"), ("x02", "x12"))
ELL_FACTORS = (
    ((0, 0, 1, 0, -2), (1, 0, 0, -2, 0), (0, 1, 0, -2, 0)),
    ((1, 0, 1, 0, 0), (0, 1, 0, 0, -2), (0, 0, 0, 1, 1)),
)

Polynomial = dict[tuple[int, ...], int]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def product_two(left: tuple[int, ...], right: tuple[int, ...]) -> list[int]:
    return [left[i] * right[j] + left[j] * right[i] for i, j in PAIRS]


def product_three(factors: tuple[tuple[int, ...], ...]) -> list[int]:
    return [
        sum(
            factors[0][order[0]] * factors[1][order[1]] * factors[2][order[2]]
            for order in itertools.permutations(triple)
        )
        for triple in TRIPLES
    ]


def rank_mod(rows: list[list[int]], prime: int) -> int:
    matrix = [[value % prime for value in row] for row in rows]
    if not matrix:
        return 0
    rank = 0
    for column in range(len(matrix[0])):
        pivot = next((i for i in range(rank, len(matrix)) if matrix[i][column]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inverse = pow(matrix[rank][column], -1, prime)
        matrix[rank] = [(inverse * value) % prime for value in matrix[rank]]
        for i in range(len(matrix)):
            if i != rank and matrix[i][column]:
                scale = matrix[i][column]
                matrix[i] = [
                    (left - scale * right) % prime
                    for left, right in zip(matrix[i], matrix[rank])
                ]
        rank += 1
        if rank == len(matrix):
            break
    return rank


def pairing(quadratic: list[int], cubic: list[int]) -> int:
    return sum(
        quadratic[PAIRS.index(tuple(i for i in range(5) if i not in triple))]
        * cubic[index]
        for index, triple in enumerate(TRIPLES)
    )


def poly_add(left: Polynomial, right: Polynomial, prime: int) -> Polynomial:
    result = dict(left)
    for monomial, coefficient in right.items():
        result[monomial] = (result.get(monomial, 0) + coefficient) % prime
        if result[monomial] == 0:
            del result[monomial]
    return result


def poly_scale(poly: Polynomial, scale: int, prime: int) -> Polynomial:
    return {
        monomial: coefficient * scale % prime
        for monomial, coefficient in poly.items()
        if coefficient * scale % prime
    }


def poly_mul(left: Polynomial, right: Polynomial, prime: int) -> Polynomial:
    result: Polynomial = {}
    for first, a in left.items():
        for second, b in right.items():
            monomial = tuple(x + y for x, y in zip(first, second))
            result[monomial] = (result.get(monomial, 0) + a * b) % prime
            if result[monomial] == 0:
                del result[monomial]
    return result


def bilinear(matrix: list[list[str]], prime: int) -> Polynomial:
    result: Polynomial = {}
    for i, row in enumerate(matrix):
        for j, value in enumerate(row):
            rational = Fraction(value)
            coefficient = (
                rational.numerator * pow(rational.denominator, -1, prime) % prime
            )
            if coefficient:
                exponent = [0] * 10
                exponent[i] = 1
                exponent[5 + j] = 1
                result[tuple(exponent)] = coefficient
    return result


def catalecticant(k_basis: list[list[int]], prime: int) -> list[list[Polynomial]]:
    matrix: list[list[Polynomial]] = []
    for quadratic in k_basis:
        row: list[Polynomial] = []
        for source in range(5):
            entry: Polynomial = {}
            for b_index in range(5):
                for c_index in range(5):
                    if len({source, b_index, c_index}) < 3:
                        continue
                    triple = tuple(sorted((source, b_index, c_index)))
                    complement = tuple(i for i in range(5) if i not in triple)
                    coefficient = quadratic[PAIRS.index(complement)] % prime
                    if coefficient:
                        exponent = [0] * 10
                        exponent[b_index] = 1
                        exponent[5 + c_index] = 1
                        monomial = tuple(exponent)
                        entry[monomial] = (entry.get(monomial, 0) + coefficient) % prime
            row.append({monomial: value for monomial, value in entry.items() if value})
        matrix.append(row)
    return matrix


def determinant_three(
    matrix: list[list[Polynomial]], rows: list[int], columns: list[int], prime: int
) -> Polynomial:
    result: Polynomial = {}
    for permutation in itertools.permutations(range(3)):
        inversions = sum(
            permutation[i] > permutation[j] for i in range(3) for j in range(i + 1, 3)
        )
        term: Polynomial = {(0,) * 10: 1}
        for i in range(3):
            term = poly_mul(term, matrix[rows[i]][columns[permutation[i]]], prime)
        result = poly_add(
            result, poly_scale(term, -1 if inversions % 2 else 1, prime), prime
        )
    return result


def is_hitting(mask: int, edges: list[tuple[int, ...]]) -> bool:
    return all(any(mask & (1 << vertex) for vertex in edge) for edge in edges)


def minimal_covers(edges: list[tuple[int, ...]], vertex_count: int) -> list[int]:
    result = []
    for mask in range(1, 1 << vertex_count):
        if not is_hitting(mask, edges):
            continue
        if all(
            not is_hitting(mask ^ (1 << vertex), edges)
            for vertex in range(vertex_count)
            if mask & (1 << vertex)
        ):
            result.append(mask)
    return result


def main() -> None:
    primary = json.loads(PRIMARY.read_text(encoding="utf-8"))
    assert primary["verified"] is True
    assert primary["shared_full_mode_factorization_constructed"] is False
    assert primary["rank_five_configuration_excluded"] is False
    assert primary["p6_to_delta3_decided"] is False

    ordered = [VECTORS[name] for name in VECTORS]
    weights = (1, 1, 2, 1, 1, 1)
    assert [sum(w * v[j] for w, v in zip(weights, ordered)) for j in range(5)] == [
        0
    ] * 5
    bad = [product_two(VECTORS[left], VECTORS[right]) for left, right in BAD_NAMES]
    good = [product_two(VECTORS[left], VECTORS[right]) for left, right in GOOD_NAMES]
    ell_vectors = [product_three(factors) for factors in ELL_FACTORS]
    assert ell_vectors == primary["L_decomposable_generators"]
    assert all(pairing(q, ell) == 0 for q in bad + good for ell in ell_vectors)

    modular_rank_checks = {}
    for prime in PRIMES:
        checks = {
            "exceptional_planes": [
                rank_mod([ordered[2 * i], ordered[2 * i + 1]], prime) for i in range(3)
            ],
            "six_vectors": rank_mod(ordered, prime),
            "forbidden": rank_mod(bad, prime),
            "total": rank_mod(bad + good, prime),
            "ell_generators": rank_mod(ell_vectors, prime),
        }
        assert checks == {
            "exceptional_planes": [2, 2, 2],
            "six_vectors": 5,
            "forbidden": 5,
            "total": 8,
            "ell_generators": 2,
        }
        modular_rank_checks[str(prime)] = checks

    gates_by_prime = {
        prime: [bilinear(matrix, prime) for matrix in primary["bilinear_gate_matrices"]]
        for prime in PRIMES
    }
    identity_checks = {}
    for prime in PRIMES:
        cat = catalecticant(primary["k_basis_rows"], prime)
        for index, identity in enumerate(primary["split_minor_factorizations"]):
            left = determinant_three(cat, identity["rows"], identity["columns"], prime)
            rational = Fraction(identity["constant"])
            constant = rational.numerator * pow(rational.denominator, -1, prime) % prime
            right: Polynomial = {(0,) * 10: constant}
            for factor_id in identity["factor_ids"]:
                right = poly_mul(right, gates_by_prime[prime][factor_id], prime)
            assert left == right, (prime, index)
        identity_checks[str(prime)] = len(primary["split_minor_factorizations"])

    edges = [
        tuple(identity["factor_ids"])
        for identity in primary["split_minor_factorizations"]
    ]
    covers = minimal_covers(edges, primary["bilinear_gate_count"])
    distribution = dict(sorted(Counter(mask.bit_count() for mask in covers).items()))
    assert len(covers) == 53
    assert distribution == {4: 1, 5: 6, 6: 13, 7: 14, 8: 16, 9: 2, 10: 1}
    assert [
        [i for i in range(primary["bilinear_gate_count"]) if mask & (1 << i)]
        for mask in covers
        if mask.bit_count() == 4
    ] == [primary["unique_four_gate_cover"]]

    output = {
        "audited": True,
        "method": "independent modular ranks and sparse-polynomial identities; no sympy",
        "primes": list(PRIMES),
        "modular_rank_checks": modular_rank_checks,
        "split_minor_identity_checks": identity_checks,
        "minimal_cover_count": len(covers),
        "minimal_cover_size_distribution": {str(k): v for k, v in distribution.items()},
        "primary_artifact": PRIMARY.name,
        "primary_artifact_sha256": sha256(PRIMARY),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__).resolve()),
    }
    OUTPUT.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
