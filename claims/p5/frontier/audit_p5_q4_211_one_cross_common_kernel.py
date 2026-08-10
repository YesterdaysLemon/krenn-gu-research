#!/usr/bin/env python3
"""Independent audit of the adjacent common-kernel obstruction."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q4_211_ONE_CROSS_COMMON_KERNEL_OBSTRUCTION.md"
PRIMARY = ROOT / "verify_p5_q4_211_one_cross_common_kernel.py"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dynamic_contraction(
    p: int,
    directions: tuple[tuple[int, ...], ...],
) -> dict[tuple[int, ...], int]:
    tensor = {
        permutation: 1
        for permutation in itertools.permutations(range(5))
    }
    for direction in directions:
        result: dict[tuple[int, ...], int] = {}
        for word, coefficient in tensor.items():
            value = coefficient * direction[word[0]]
            tail = word[1:]
            result[tail] = (result.get(tail, 0) + value) % p
        tensor = {word: value for word, value in result.items() if value}
    return tensor


def projective_points(p: int) -> list[tuple[int, int]]:
    points = {(1, value) for value in range(p)}
    points.add((0, 1))
    return sorted(points)


def permanent_mod(rows: list[tuple[int, ...]], p: int) -> int:
    return sum(
        _product(rows[index][permutation[index]] for index in range(5))
        for permutation in itertools.permutations(range(5))
    ) % p


def permanent3_mod(rows: list[tuple[int, ...]], p: int) -> int:
    return sum(
        _product(rows[index][permutation[index]] for index in range(3))
        for permutation in itertools.permutations(range(3))
    ) % p


def _product(values) -> int:
    result = 1
    for value in values:
        result *= value
    return result


def rank_mod(columns: tuple[tuple[int, ...], ...], p: int) -> int:
    matrix = [
        [columns[column][row] % p for column in range(len(columns))]
        for row in range(len(columns[0]))
    ]
    rank = 0
    for column in range(len(columns)):
        pivot = next(
            (
                row
                for row in range(rank, len(matrix))
                if matrix[row][column] % p
            ),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inverse = pow(matrix[rank][column], -1, p)
        matrix[rank] = [(entry * inverse) % p for entry in matrix[rank]]
        for row in range(len(matrix)):
            if row == rank:
                continue
            factor = matrix[row][column] % p
            if factor:
                matrix[row] = [
                    (left - factor * right) % p
                    for left, right in zip(
                        matrix[row], matrix[rank], strict=True
                    )
                ]
        rank += 1
    return rank


def audit_field(p: int) -> dict[str, object]:
    a, b, c = 3 % p, 1, 2
    u0 = (a, 1, 1, 0, 0)
    u1 = (b, 0, 0, 1, 0)
    u2 = (c, 0, 0, 0, 1)
    h1 = (b, 0, 0, -1 % p, 0)
    h2 = (c, 0, 0, 0, -1 % p)
    n = (0, 0, 0, c, b)
    s = (0, 1, 1, 0, 0)
    w_minus = (1, 0, 0, -b % p, c)
    w_plus = (1, 0, 0, b, -c % p)

    contractions = {
        "u1_h2_h2": dynamic_contraction(p, (u1, h2, h2)),
        "u2_h1_h1": dynamic_contraction(p, (u2, h1, h1)),
        "u0_h1_h2_n": dynamic_contraction(p, (u0, h1, h2, n)),
        "u0_h2_h2_n": dynamic_contraction(p, (u0, h2, h2, n)),
        "u2_h1": dynamic_contraction(p, (u2, h1)),
        "u1_h2": dynamic_contraction(p, (u1, h2)),
    }
    assert contractions["u1_h2_h2"] == {
        (1, 2): -2 * c % p,
        (2, 1): -2 * c % p,
    }
    assert contractions["u2_h1_h1"] == {
        (1, 2): -2 * b % p,
        (2, 1): -2 * b % p,
    }
    assert contractions["u0_h1_h2_n"] == {
        (1,): -2 * b * c % p,
        (2,): -2 * b * c % p,
    }
    assert contractions["u0_h2_h2_n"] == {
        (1,): -2 * c * c % p,
        (2,): -2 * c * c % p,
    }

    polar_pairs = []
    for ell_y in projective_points(p):
        for ell_d in projective_points(p):
            zero_pairing = (
                ell_y[0] * ell_d[1] + ell_y[1] * ell_d[0]
            ) % p == 0
            d_kills_s = (ell_d[0] + ell_d[1]) % p == 0
            if zero_pairing and d_kills_s:
                polar_pairs.append((ell_y, ell_d))
    assert polar_pairs == [((1, 1), (1, -1 % p))]

    assert rank_mod((s, w_minus, w_plus), p) == 3

    # Audit the e0 coefficient factor on deterministic nonzero rows.
    factor_checks = 0
    for seed in range(1, p):
        row_a = ((seed + 1) % p, 0, 0, 1, seed)
        row_y = ((seed + 2) % p, 0, 0, 2, seed + 1)
        row_d = ((seed + 3) % p, 0, 0, 3, seed + 2)
        row_c = (
            seed,
            seed + 1,
            seed + 2,
            seed + 3,
            seed + 4,
        )
        rows = [u0, row_a, row_y, row_c, row_d]
        value = permanent_mod(rows, p)
        x_factor = permanent3_mod(
            [
                (row_a[0], row_a[3], row_a[4]),
                (row_y[0], row_y[3], row_y[4]),
                (row_d[0], row_d[3], row_d[4]),
            ],
            p,
        )
        expected = (row_c[1] + row_c[2]) * x_factor % p
        assert value == expected
        factor_checks += 1

    # Directly audit the six P3 assignments under the propagated
    # sigma/delta kernel pattern.
    def vector_add(left, right):
        return tuple((x + y) % p for x, y in zip(left, right, strict=True))

    def vector_scale(scale, vector):
        return tuple(scale * value % p for value in vector)

    def outer(left, middle, right):
        return {
            (i, j, k): left[i] * middle[j] * right[k] % p
            for i, j, k in itertools.product(range(3), repeat=3)
        }

    e1_target = (0, 1, 0)
    e2_target = (0, 0, 1)
    v_y = e1_target
    v_d = e2_target
    c_s = (1, 0, 2)
    c_d = e2_target
    inverse_two = pow(2, -1, p)
    c_e1 = vector_scale(inverse_two, vector_add(c_s, c_d))
    c_e2 = vector_scale(
        inverse_two, vector_add(c_s, vector_scale(-1, c_d))
    )
    y_w = (2, 3, 4)
    c_w = (3, 4, 1)
    d_w = (4, 2, 3)
    terms = [
        outer(v_y, c_e2, d_w),
        outer(v_y, c_w, vector_scale(-1, v_d)),
        outer(v_y, c_e1, d_w),
        outer(v_y, c_w, v_d),
        outer(y_w, c_e1, vector_scale(-1, v_d)),
        outer(y_w, c_e2, v_d),
    ]
    total = {
        index: sum(term[index] for term in terms) % p
        for index in itertools.product(range(3), repeat=3)
    }
    reduced_left = outer(y_w, c_d, v_d)
    reduced_right = outer(v_y, c_s, d_w)
    reduced = {
        index: (-reduced_left[index] + reduced_right[index]) % p
        for index in itertools.product(range(3), repeat=3)
    }
    assert total == reduced

    return {
        "field": f"F_{p}",
        "contraction_term_counts": {
            name: len(value) for name, value in contractions.items()
        },
        "polar_kernel_pairs": len(polar_pairs),
        "kernel_triple_rank": 3,
        "e0_factor_checks": factor_checks,
        "p3_six_term_identity": True,
    }


def main() -> None:
    fields = [audit_field(5), audit_field(7)]
    output = {
        "audited": True,
        "method": (
            "independent squarefree contraction, binary polarity, "
            "and polarized-chart audit"
        ),
        "fields": fields,
        "common_kernel_gate_excluded": True,
        "adjacent_one_cross_excluded": True,
        "ambient_maps_enumerated": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "primary": PRIMARY.name,
        "primary_sha256": sha256(PRIMARY),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT / "tmp" / "p5_q4_211_one_cross_common_kernel_audit.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
