#!/usr/bin/env python3
"""Independent audit of the exact q5_221 marked-end path obstruction."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q5_221_MARKED_END_PATH_OBSTRUCTION.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rank_mod(rows, prime: int) -> int:
    if not rows:
        return 0
    matrix = [[value % prime for value in row] for row in rows]
    pivot_row = 0
    for column in range(len(matrix[0])):
        pivot = next(
            (
                row
                for row in range(pivot_row, len(matrix))
                if matrix[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        inverse = pow(matrix[pivot_row][column], -1, prime)
        matrix[pivot_row] = [
            value * inverse % prime for value in matrix[pivot_row]
        ]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                (left - factor * right) % prime
                for left, right in zip(matrix[row], matrix[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row


def rref_planes(prime: int):
    for pivots in itertools.combinations(range(4), 2):
        free_positions = tuple(
            (row, column)
            for column in range(4)
            if column not in pivots
            for row, pivot in enumerate(pivots)
            if pivot < column
        )
        for values in itertools.product(range(prime), repeat=len(free_positions)):
            rows = [[0] * 4 for _ in range(2)]
            for row, pivot in enumerate(pivots):
                rows[row][pivot] = 1
            for (row, column), value in zip(
                free_positions, values, strict=True
            ):
                rows[row][column] = value
            yield tuple(tuple(row) for row in rows)


def contains(rows, vector, prime: int) -> bool:
    return rank_mod(rows + (vector,), prime) == len(rows)


def pair_vector(left, right, prime: int):
    return tuple(
        (left[i] * right[j] + left[j] * right[i]) % prime
        for i, j in itertools.combinations(range(4), 2)
    )


def pair_image_rank(left_basis, right_basis, prime: int) -> int:
    return rank_mod(
        tuple(
            pair_vector(left, right, prime)
            for left in left_basis
            for right in right_basis
        ),
        prime,
    )


def audit_pair_lemma(prime: int):
    h0 = (1, -1, 0, 0)
    u1 = (0, 0, 1, 1)
    h1 = (0, 0, 1, -1)
    admissible = tuple(
        plane
        for plane in rref_planes(prime)
        if not contains(plane, h0, prime)
        and not contains(plane, h1, prime)
    )
    ranks = tuple(
        pair_image_rank(plane, (h0, u1), prime)
        for plane in admissible
    )
    assert min(ranks) >= 3
    return {
        "prime": prime,
        "admissible_planes": len(admissible),
        "minimum_pair_image_rank": min(ranks),
        "rank_histogram": {
            str(rank): ranks.count(rank) for rank in sorted(set(ranks))
        },
    }


def clean(poly):
    return {
        monomial: coefficient
        for monomial, coefficient in poly.items()
        if coefficient
    }


def constant(value: int):
    return {} if value == 0 else {(): value}


def variable(name: str):
    return {(name,): 1}


def add(*polynomials):
    result = {}
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            result[monomial] = result.get(monomial, 0) + coefficient
    return clean(result)


def scale(coefficient: int, polynomial):
    return clean(
        {
            monomial: coefficient * value
            for monomial, value in polynomial.items()
        }
    )


def multiply(*polynomials):
    result = constant(1)
    for polynomial in polynomials:
        product = {}
        for left_monomial, left_coefficient in result.items():
            for right_monomial, right_coefficient in polynomial.items():
                monomial = tuple(sorted(left_monomial + right_monomial))
                product[monomial] = (
                    product.get(monomial, 0)
                    + left_coefficient * right_coefficient
                )
        result = clean(product)
    return result


def vector_add(*vectors):
    return tuple(
        add(*(vector[index] for vector in vectors))
        for index in range(len(vectors[0]))
    )


def vector_scale(polynomial, vector):
    return tuple(multiply(polynomial, coordinate) for coordinate in vector)


def tensor_coefficient(rows, factors):
    result = {}
    for permutation in itertools.permutations(range(len(rows))):
        term = constant(1)
        for mode, factor_index in enumerate(permutation):
            evaluation = {}
            for coordinate in range(len(rows[mode])):
                evaluation = add(
                    evaluation,
                    multiply(
                        rows[mode][coordinate],
                        factors[factor_index][coordinate],
                    ),
                )
            term = multiply(term, evaluation)
        result = add(result, term)
    return result


def format_polynomial(poly) -> str:
    if not poly:
        return "0"
    pieces = []
    for monomial, coefficient in sorted(poly.items()):
        factor = "*".join(monomial)
        pieces.append(f"{coefficient}*{factor}" if factor else str(coefficient))
    return " + ".join(pieces)


def main() -> None:
    finite_fields = [audit_pair_lemma(prime) for prime in (3, 5)]

    zero = constant(0)
    one = constant(1)
    minus_one = constant(-1)
    e = tuple(
        tuple(one if row == column else zero for column in range(5))
        for row in range(5)
    )
    u0 = vector_add(e[0], e[1])
    h0 = vector_add(e[0], vector_scale(minus_one, e[1]))
    u1 = vector_add(e[2], e[3])
    h1 = vector_add(e[2], vector_scale(minus_one, e[3]))
    h2 = e[4]
    t1_factors = (e[0], e[1], u1, h2)
    t2_factors = e[:4]

    a1 = variable("a1")
    a2 = variable("a2")
    beta = variable("beta")
    gamma = variable("gamma")
    delta = variable("delta")
    bu = variable("bu")
    bh = variable("bh")
    du = variable("du")
    dh = variable("dh")
    cu = variable("cu")
    ch = variable("ch")
    q02_a1 = vector_scale(a1, h2)
    q02_a2 = vector_scale(
        a2, vector_add(u1, vector_scale(beta, h0))
    )
    q02_b1 = vector_add(vector_scale(bu, u0), vector_scale(bh, h0))
    q02_d1 = vector_add(vector_scale(du, u0), vector_scale(dh, h0))
    q02_c1 = vector_add(
        vector_scale(gamma, u1),
        vector_scale(delta, h1),
        vector_scale(cu, u0),
        vector_scale(ch, h0),
    )
    q02_required = tensor_coefficient(
        (q02_a1, q02_b1, q02_c1, q02_d1), t1_factors
    )
    q02_forbidden = tensor_coefficient(
        (q02_a2, q02_b1, q02_c1, q02_d1), t2_factors
    )
    pair_permanent = add(
        scale(2, multiply(bu, du)),
        scale(-2, multiply(bh, dh)),
    )
    assert q02_required == multiply(
        constant(2), a1, gamma, pair_permanent
    )
    assert q02_forbidden == multiply(
        constant(2), a2, gamma, pair_permanent
    )

    aa = variable("aa")
    ab = variable("ab")
    d0 = variable("d0")
    d1 = variable("d1")
    b0 = variable("b0")
    b1 = variable("b1")
    b2 = variable("b2")
    b3 = variable("b3")
    b4 = variable("b4")
    rank_one_a1 = vector_add(
        vector_scale(aa, u0), vector_scale(ab, h2)
    )
    rank_one_b1 = vector_add(
        vector_scale(b0, h0),
        vector_scale(b1, h1),
        vector_scale(b2, u0),
        vector_scale(b3, u1),
        vector_scale(b4, h2),
    )
    rank_one_d1 = vector_add(
        vector_scale(d0, h0), vector_scale(d1, h1)
    )
    rank_one_required = tensor_coefficient(
        (rank_one_a1, rank_one_b1, h2, rank_one_d1), t1_factors
    )
    assert rank_one_required == {}

    r = variable("r")
    s = variable("s")
    b = variable("b")
    k = variable("k")
    sigma = variable("sigma")
    c = variable("c")
    cap_c = variable("C")
    d = variable("d")
    cap_a = variable("A")
    rank_two_a1 = vector_add(
        vector_scale(r, h2),
        vector_scale(s, vector_add(u1, vector_scale(b, u0))),
    )
    rank_two_b1 = vector_add(
        h0, vector_scale(k, h2), vector_scale(sigma, u0)
    )
    rank_two_c1 = vector_scale(c, h2)
    rank_two_d0 = vector_add(
        vector_scale(cap_c, vector_add(u0, vector_scale(d, h2))),
        vector_scale(cap_a, h0),
    )
    rank_two_required = tensor_coefficient(
        (rank_two_a1, rank_two_b1, rank_two_c1, h0), t1_factors
    )
    rank_two_forbidden = tensor_coefficient(
        (rank_two_a1, u0, rank_two_c1, rank_two_d0), t1_factors
    )
    assert rank_two_required == scale(-4, multiply(c, s))
    assert rank_two_forbidden == scale(4, multiply(cap_c, c, s))

    output = {
        "audited": True,
        "method": (
            "finite-field pair-image census plus independent "
            "exact polynomial expansion"
        ),
        "finite_fields": finite_fields,
        "Q02_required_T1_coefficient": format_polynomial(q02_required),
        "Q02_forbidden_T2_coefficient": format_polynomial(q02_forbidden),
        "Q20_rank_one_required_T1_coefficient": format_polynomial(
            rank_one_required
        ),
        "Q20_rank_two_required_T1_coefficient": format_polynomial(
            rank_two_required
        ),
        "Q20_rank_two_forbidden_T1_coefficient": format_polynomial(
            rank_two_forbidden
        ),
        "exact_marked_end_path_excluded": True,
        "q5_221_excluded": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "global_conjecture_resolved": False,
    }
    output_path = ROOT / "tmp" / "p5_q5_221_marked_end_path_audited.json"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
