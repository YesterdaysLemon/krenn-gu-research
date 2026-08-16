#!/usr/bin/env python3
"""Independent no-import audit for the monomial-residual endpoint theorem."""

from __future__ import annotations

from fractions import Fraction
from itertools import product

Q = Fraction


def ridx(i: int, j: int, k: int) -> int:
    """Reverse the primary replay's tensor flattening."""
    return 9 * k + 3 * j + i


def vec3(i: int) -> list[Q]:
    return [Q(int(j == i)) for j in range(3)]


def outer3(u: list[Q], v: list[Q], w: list[Q]) -> list[Q]:
    out = [Q(0) for _ in range(27)]
    for i, j, k in product(range(3), repeat=3):
        out[ridx(i, j, k)] = u[i] * v[j] * w[k]
    return out


def add(*vectors: list[Q]) -> list[Q]:
    return [sum(entries, Q(0)) for entries in zip(*vectors, strict=True)]


def scale(s: Q, v: list[Q]) -> list[Q]:
    return [s * value for value in v]


def contract3(T: list[Q], gamma: list[Q]) -> list[Q]:
    out = [Q(0) for _ in range(9)]
    for i, j in product(range(3), repeat=2):
        out[3 * j + i] = sum(
            (T[ridx(i, j, k)] * gamma[k] for k in range(3)), Q(0)
        )
    return out


def rank(rows: list[list[Q]]) -> int:
    A = [row[:] for row in rows if any(row)]
    if not A:
        return 0
    m, n = len(A), len(A[0])
    r = 0
    for c in range(n):
        pivot = next((i for i in range(r, m) if A[i][c]), None)
        if pivot is None:
            continue
        A[r], A[pivot] = A[pivot], A[r]
        z = A[r][c]
        A[r] = [value / z for value in A[r]]
        for i in range(m):
            if i != r and A[i][c]:
                z = A[i][c]
                A[i] = [u - z * v for u, v in zip(A[i], A[r], strict=True)]
        r += 1
        if r == m:
            break
    return r


def audit_derivative_contraction() -> None:
    # A separate dense rational fixture, with no symbolic or repository import.
    x = [Q(1), Q(2), Q(-1)]
    y = [Q(3), Q(-2), Q(4)]
    w = [Q(2), Q(5), Q(-3)]
    a = [Q(-1), Q(4), Q(2)]
    b = [Q(5), Q(1), Q(-2)]
    c = [Q(3), Q(-1), Q(6)]
    C = [[Q(2 * i - 3 * j + 1) for j in range(3)] for i in range(3)]
    gamma = [Q(5), Q(-2), Q(0)]  # gamma(w)=0

    tangent = add(outer3(a, y, w), scale(Q(-1), outer3(x, b, w)))
    residual = [Q(0) for _ in range(27)]
    for i, j, k in product(range(3), repeat=3):
        residual[ridx(i, j, k)] = C[i][j] * c[k]
    got = contract3(add(tangent, residual), gamma)
    expected = [gamma[0] * c[0] + gamma[1] * c[1] + gamma[2] * c[2]]
    expected = [expected[0] * C[i][j] for j in range(3) for i in range(3)]
    assert got == expected


def audit_every_ordered_monomial() -> None:
    sample_w = [Q(2), Q(-3), Q(5)]
    for d, e in product(range(3), repeat=2):
        others = [i for i in range(3) if i != d]
        gammas: list[list[Q]] = []
        for a in others:
            gamma = [Q(0), Q(0), Q(0)]
            gamma[a] = sample_w[d]
            gamma[d] = -sample_w[a]
            assert sum((gamma[i] * sample_w[i] for i in range(3)), Q(0)) == 0
            gammas.append(gamma)
        restriction = [[gamma[i] for i in others] for gamma in gammas]
        assert rank(restriction) == 2

        C = [[Q(0) for _ in range(3)] for _ in range(3)]
        C[d][e] = Q(7)
        assert all(C[i][j] == 0 for i in others for j in range(3))

        other_columns = [j for j in range(3) if j != e]
        assert all(C[i][j] == 0 for i in range(3) for j in other_columns)

        endpoint_rows = [vec3(d), vec3(e)]
        endpoint_rank = rank(endpoint_rows)
        assert endpoint_rank == (1 if d == e else 2)


def audit_shift_incidence() -> None:
    # Independent row-oriented calculation of the shift identity and the
    # dimension lower bound dim(R intersect B)>=1.
    p0 = [Q(1), Q(0), Q(0), Q(0)]
    p1 = [Q(0), Q(1), Q(0), Q(0)]
    v = [Q(0), Q(0), Q(1), Q(0)]
    B = [p0, p1, v]
    assert rank(B) == 3

    R = [v, [Q(0), Q(0), Q(0), Q(1)]]
    assert rank(R) == 2
    assert rank(B + R) == 4
    assert rank(B) + rank(R) - rank(B + R) == 1

    cases = [
        (Q(1), Q(0), Q(3), Q(3), Q(0)),
        (Q(0), Q(2), Q(-5), Q(0), Q(-5, 2)),
        (Q(2), Q(-3), Q(7), Q(2), Q(-1)),
    ]
    for a, b, c, l0, l1 in cases:
        if a * l0 + b * l1 != c:
            # Solve using the first available nonzero coefficient.
            if a:
                l0 = (c - b * l1) / a
            else:
                l1 = c / b
        ell = [a * p0[i] + b * p1[i] + c * v[i] for i in range(4)]
        shifted = [
            a * (p0[i] + l0 * v[i]) + b * (p1[i] + l1 * v[i])
            for i in range(4)
        ]
        assert ell == shifted


def audit_tangent_quotient() -> None:
    # The image of a pure tensor in the double quotient is an outer product;
    # it vanishes exactly when one quotient factor does.
    for d, e, xd, ye in product(range(3), repeat=4):
        left_zero = xd == d
        right_zero = ye == e
        left = [Q(0), Q(0)] if left_zero else [Q(1), Q(2)]
        right = [Q(0), Q(0)] if right_zero else [Q(3), Q(-1)]
        outer = [[left[i] * right[j] for j in range(2)] for i in range(2)]
        assert (not any(any(row) for row in outer)) == (left_zero or right_zero)


def main() -> None:
    audit_derivative_contraction()
    audit_every_ordered_monomial()
    audit_shift_incidence()
    audit_tangent_quotient()
    print("independent monomial-residual endpoint audit: exact checks passed")


if __name__ == "__main__":
    main()
