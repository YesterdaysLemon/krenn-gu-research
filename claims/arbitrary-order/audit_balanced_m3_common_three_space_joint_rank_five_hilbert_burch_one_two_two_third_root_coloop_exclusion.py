#!/usr/bin/env python3
"""Independent exact audit of the (1,2,2) third-root-coloop exclusion.

This audit imports no repository module and no third-party package.
"""

from __future__ import annotations

import hashlib
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
PINS = {
    (
        "balanced_m3_common_three_space_joint_rank_five_hilbert_burch_"
        "one_two_two_residual_second_root_coloop_projective_pencil_"
        "certificates.json"
    ): "0a92e61cef0b3db7940c68ea6e24bab4befb5dc1bd137ada581d0dbde4b9e0ca",
    (
        "balanced_m3_common_three_space_joint_rank_five_hilbert_burch_"
        "one_two_two_residual_second_root_coloop_common_middle_row_"
        "certificates.json"
    ): "a56242675744f848fc4f747045ce9b2a18c7b32ae2152ca800bd6c654d29e8d1",
}


Vector = tuple[Fraction, ...]


def unit(index: int, size: int) -> Vector:
    return tuple(Fraction(int(i == index)) for i in range(size))


def add(*vectors: Vector) -> Vector:
    return tuple(sum((vector[i] for vector in vectors), Fraction(0)) for i in range(len(vectors[0])))


def scale(value: Fraction, vector: Vector) -> Vector:
    return tuple(value * entry for entry in vector)


def dot(left: Vector, right: Vector) -> Fraction:
    return sum((a * b for a, b in zip(left, right)), Fraction(0))


def linear_combination(coefficients: Vector, rows: tuple[Vector, ...]) -> Vector:
    return tuple(
        sum((coefficients[j] * rows[j][i] for j in range(len(rows))), Fraction(0))
        for i in range(len(rows[0]))
    )


def rank(rows: list[Vector]) -> int:
    if not rows:
        return 0
    matrix = [list(row) for row in rows]
    row = 0
    for column in range(len(matrix[0])):
        pivot = next((i for i in range(row, len(matrix)) if matrix[i][column]), None)
        if pivot is None:
            continue
        matrix[row], matrix[pivot] = matrix[pivot], matrix[row]
        pivot_value = matrix[row][column]
        matrix[row] = [value / pivot_value for value in matrix[row]]
        for i in range(len(matrix)):
            if i == row or not matrix[i][column]:
                continue
            factor = matrix[i][column]
            matrix[i] = [a - factor * b for a, b in zip(matrix[i], matrix[row])]
        row += 1
    return row


def canonical_rows(s: int, t: int, selected: int, y: Vector, z: Vector, w: Vector) -> tuple[tuple[Vector, ...], tuple[Vector, ...], tuple[Vector, ...]]:
    r_basis = [index for index in range(3) if index != s]
    r_rows: list[Vector] = [unit(0, 5)] * 3
    r_rows[s] = unit(2, 5)
    for slot, index in enumerate(r_basis):
        r_rows[index] = unit(slot, 5)

    middle = [index for index in range(3) if index != t]
    p_rows: list[Vector] = [unit(0, 5)] * 3
    p_rows[t] = unit(3, 5)
    for slot, index in enumerate(middle):
        p_rows[index] = add(scale(y[index], unit(2, 5)), unit(slot, 5))

    third_other = [index for index in range(3) if index != selected]
    q_rows: list[Vector] = [unit(0, 5)] * 3
    for slot, index in enumerate(third_other):
        q_rows[index] = add(
            scale(z[index], unit(2, 5)),
            scale(w[index], unit(3, 5)),
            unit(slot, 5),
        )
    q_rows[selected] = add(
        scale(z[selected], unit(2, 5)),
        scale(w[selected], unit(3, 5)),
        unit(4, 5),
    )
    return tuple(r_rows), tuple(p_rows), tuple(q_rows)


def audit_row_geometry() -> None:
    for s in range(3):
        for t in range(3):
            y_list = [Fraction(2), Fraction(3), Fraction(5)]
            y_list[t] = Fraction(0)
            y = tuple(y_list)
            z = (Fraction(7), Fraction(11), Fraction(13))
            for selected in range(3):
                for w in (
                    (Fraction(17), Fraction(19), Fraction(23)),
                    tuple(Fraction(0) if i == t else Fraction(29 + i) for i in range(3)),
                ):
                    r_rows, p_rows, q_rows = canonical_rows(s, t, selected, y, z, w)
                    assert rank(list(r_rows)) == 3
                    assert rank(list(p_rows)) == 3
                    assert rank(list(q_rows)) == 3
                    other = [index for index in range(3) if index != t]
                    assert rank([r_rows[i] for i in other]) == 2
                    assert rank([p_rows[i] for i in other]) == 2
                    assert all(row[3] == row[4] == 0 for row in [r_rows[i] for i in other])
                    assert all(row[3] == row[4] == 0 for row in [p_rows[i] for i in other])

                    # cross(w,e_selected) lies in w^perp intersect e_selected^perp.
                    basis_selected = unit(selected, 3)
                    normal = (
                        w[1] * basis_selected[2] - w[2] * basis_selected[1],
                        w[2] * basis_selected[0] - w[0] * basis_selected[2],
                        w[0] * basis_selected[1] - w[1] * basis_selected[0],
                    )
                    if not any(normal):
                        candidates = [unit(i, 3) for i in range(3) if i != selected]
                        normal = next(candidate for candidate in candidates if dot(candidate, w) == 0)
                    assert dot(normal, w) == 0 and normal[selected] == 0
                    q_normal = linear_combination(normal, q_rows)
                    assert q_normal[3] == 0 and q_normal[4] == 0
    print("independent gamma-coloop row-space audit: PASS")


def target_values(alpha: Vector, beta: Vector, gamma: Vector) -> Vector:
    return tuple(alpha[i] * beta[i] * gamma[i] for i in range(3))


def audit_faces() -> None:
    for t in range(3):
        other = [index for index in range(3) if index != t]

        w_nonzero_t = tuple(Fraction(value) for value in (2, 3, 5))
        lifts: dict[int, Vector] = {}
        for index in other:
            lift = add(unit(index, 3), scale(-w_nonzero_t[index] / w_nonzero_t[t], unit(t, 3)))
            assert dot(lift, w_nonzero_t) == 0
            lifts[index] = lift
        for i in other:
            for j in other:
                for k in other:
                    values = target_values(unit(i, 3), unit(j, 3), lifts[k])
                    expected = unit(k, 3) if i == j == k else (Fraction(0),) * 3
                    assert values == expected

        a, b = other
        wa, wb = Fraction(7), Fraction(11)
        w_zero_t = add(scale(wa, unit(a, 3)), scale(wb, unit(b, 3)))
        normal = add(scale(wb, unit(a, 3)), scale(-wa, unit(b, 3)))
        assert dot(normal, w_zero_t) == 0
        for i in other:
            for j in other:
                active = target_values(unit(i, 3), unit(j, 3), normal)
                inactive = target_values(unit(i, 3), unit(j, 3), unit(t, 3))
                expected = scale(normal[i], unit(i, 3)) if i == j else (Fraction(0),) * 3
                assert active == expected
                assert inactive == (Fraction(0),) * 3
        for selected in range(3):
            witness = normal if selected == t else unit(t, 3)
            assert witness[selected] == 0 and dot(witness, w_zero_t) == 0
    print("independent binary-face audit: PASS")


def outer(left: Vector, right: Vector) -> tuple[Fraction, ...]:
    return tuple(a * b for a in left for b in right)


def block_triple(y: Vector, z: Vector, w: Vector, s: int, t: int, lam: Fraction, mu: Fraction) -> tuple[tuple[Fraction, ...], ...]:
    first = tuple(a - b for a, b in zip(outer(y, w), scale(mu, outer(unit(t, 3), z))))
    second = scale(-lam, outer(unit(s, 3), w))
    third = scale(lam * mu, outer(unit(s, 3), unit(t, 3)))
    return first, second, third


def audit_root_exchange() -> None:
    lam, mu, nu = Fraction(2), Fraction(3), Fraction(5)
    for s in range(3):
        for t in range(3):
            y_list = [Fraction(7), Fraction(11), Fraction(13)]
            y_list[t] = Fraction(0)
            y = tuple(y_list)
            z = (Fraction(17), Fraction(19), Fraction(23))
            for v in range(3):
                y_prime = z
                z_prime = y
                w_prime = scale(mu, unit(t, 3))
                shift = y_prime[v] / nu
                gauged_y = add(y_prime, scale(-shift * nu, unit(v, 3)))
                gauged_z = add(z_prime, scale(-shift, w_prime))
                assert gauged_y[v] == 0
                assert block_triple(y_prime, z_prime, w_prime, s, v, lam, nu) == block_triple(
                    gauged_y, gauged_z, w_prime, s, v, lam, nu
                )
                assert rank([gauged_y, unit(v, 3)]) == 2
                assert rank([gauged_z, w_prime]) == 2
    print("independent coordinate-w root-exchange audit: PASS")


def audit_pins() -> None:
    for name, expected in PINS.items():
        assert hashlib.sha256((HERE / name).read_bytes()).hexdigest() == expected
    print("independent dependency-pin audit: PASS")


def main() -> None:
    audit_row_geometry()
    audit_faces()
    audit_root_exchange()
    audit_pins()
    print("independent third-root-coloop exclusion audit: PASS")


if __name__ == "__main__":
    main()
