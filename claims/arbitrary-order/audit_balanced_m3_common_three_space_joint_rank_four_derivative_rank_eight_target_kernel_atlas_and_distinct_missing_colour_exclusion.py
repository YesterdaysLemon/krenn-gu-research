#!/usr/bin/env python3
"""Independent no-import audit for the S2BR target-row atlas."""

from __future__ import annotations

from fractions import Fraction as F
from itertools import permutations

N = 3
ZERO = (F(0), F(0), F(0))


def e(i: int) -> tuple[F, F, F]:
    return tuple(F(j == i) for j in range(N))  # type: ignore[return-value]


def scale(s: F, v: tuple[F, ...]) -> tuple[F, ...]:
    return tuple(s * a for a in v)


def add(*vectors: tuple[F, ...]) -> tuple[F, ...]:
    return tuple(sum(v[i] for v in vectors) for i in range(len(vectors[0])))


def outer2(a: tuple[F, ...], b: tuple[F, ...]) -> dict[tuple[int, int], F]:
    return {(i, j): a[i] * b[j] for i in range(N) for j in range(N)}


def matrix_outer(a: tuple[F, ...], b: tuple[F, ...]) -> list[list[F]]:
    return [[a[i] * b[j] for j in range(N)] for i in range(N)]


def derivative(
    x: tuple[F, ...],
    y: tuple[F, ...],
    w: tuple[F, ...],
    C: list[list[F]],
    a: tuple[F, ...],
    b: tuple[F, ...],
    c: tuple[F, ...],
) -> dict[tuple[int, int, int], F]:
    return {
        (i, j, k): a[i] * y[j] * w[k]
        - x[i] * b[j] * w[k]
        + C[i][j] * c[k]
        for i in range(N)
        for j in range(N)
        for k in range(N)
    }


def contract_first(
    alpha: tuple[F, ...], t: dict[tuple[int, int, int], F]
) -> dict[tuple[int, int], F]:
    return {
        (j, k): sum(alpha[i] * t[i, j, k] for i in range(N))
        for j in range(N)
        for k in range(N)
    }


def contract_second(
    beta: tuple[F, ...], t: dict[tuple[int, int, int], F]
) -> dict[tuple[int, int], F]:
    return {
        (i, k): sum(beta[j] * t[i, j, k] for j in range(N))
        for i in range(N)
        for k in range(N)
    }


def contract_third(
    gamma: tuple[F, ...], t: dict[tuple[int, int, int], F]
) -> dict[tuple[int, int], F]:
    return {
        (i, j): sum(gamma[k] * t[i, j, k] for k in range(N))
        for i in range(N)
        for j in range(N)
    }


def flatten3(t: dict[tuple[int, int, int], F]) -> list[F]:
    # Deliberately use reversed factor order, unlike the primary replay.
    return [t[i, j, k] for k in range(N) for j in range(N) for i in range(N)]


def flatten2(t: dict[tuple[int, int], F]) -> list[F]:
    return [t[i, j] for j in range(N) for i in range(N)]


def rank(rows: list[list[F]]) -> int:
    a = [row[:] for row in rows]
    if not a:
        return 0
    r = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        p = a[r][col]
        a[r] = [z / p for z in a[r]]
        for i in range(len(a)):
            if i != r and a[i][col]:
                q = a[i][col]
                a[i] = [u - q * v for u, v in zip(a[i], a[r], strict=True)]
        r += 1
        if r == len(a):
            break
    return r


def column_rank(columns: list[list[F]]) -> int:
    return rank([list(row) for row in zip(*columns, strict=True)])


def derivative_columns(
    x: tuple[F, ...], y: tuple[F, ...], w: tuple[F, ...], C: list[list[F]]
) -> list[list[F]]:
    columns = []
    for i in range(N):
        columns.append(flatten3(derivative(x, y, w, C, e(i), ZERO, ZERO)))
    for i in range(N):
        columns.append(flatten3(derivative(x, y, w, C, ZERO, e(i), ZERO)))
    for i in range(N):
        columns.append(flatten3(derivative(x, y, w, C, ZERO, ZERO, e(i))))
    return columns


def tangent_columns(x: tuple[F, ...], y: tuple[F, ...]) -> list[list[F]]:
    columns = []
    for i in range(N):
        columns.append(flatten2(outer2(e(i), y)))
    for j in range(N):
        columns.append(flatten2(outer2(x, e(j))))
    return columns


def in_columns(v: list[F], columns: list[list[F]]) -> bool:
    return column_rank(columns + [v]) == column_rank(columns)


def coordinate(v: tuple[F, ...], s: int) -> bool:
    return v[s] != 0 and all(v[i] == 0 for i in range(N) if i != s)


def audit_rank_and_kernel() -> None:
    x = (F(1), F(1), F(0))
    y = (F(0), F(1), F(1))
    w = e(2)
    C = matrix_outer(e(0), e(0))
    columns = derivative_columns(x, y, w, C)
    assert column_rank(columns) == 8
    relation = list(x + y + ZERO)
    assert all(sum(c[j] * relation[j] for j in range(9)) == 0 for c in zip(*columns))


def audit_contractions() -> None:
    x = (F(1), F(2), F(0))
    y = (F(0), F(3), F(1))
    w = (F(2), F(0), F(1))
    C = [[F(2 * i - j + 1) for j in range(N)] for i in range(N)]
    a = (F(3), F(-1), F(2))
    b = (F(1), F(4), F(-2))
    c = (F(-1), F(2), F(5))
    alpha = (F(2), F(-1), F(3))
    beta = (F(-2), F(4), F(1))
    gamma = (F(1), F(3), F(-1))
    value = derivative(x, y, w, C, a, b, c)

    ax = sum(alpha[i] * x[i] for i in range(N))
    aa = sum(alpha[i] * a[i] for i in range(N))
    cy = tuple(sum(alpha[i] * C[i][j] for i in range(N)) for j in range(N))
    expected_first = add(
        scale(aa, flatten2(outer2(y, w))),
        scale(-ax, flatten2(outer2(b, w))),
        flatten2(outer2(cy, c)),
    )
    assert tuple(flatten2(contract_first(alpha, value))) == expected_first

    by = sum(beta[j] * y[j] for j in range(N))
    bb = sum(beta[j] * b[j] for j in range(N))
    cx = tuple(sum(C[i][j] * beta[j] for j in range(N)) for i in range(N))
    expected_second = add(
        scale(by, flatten2(outer2(a, w))),
        scale(-bb, flatten2(outer2(x, w))),
        flatten2(outer2(cx, c)),
    )
    assert tuple(flatten2(contract_second(beta, value))) == expected_second

    gw = sum(gamma[k] * w[k] for k in range(N))
    gc = sum(gamma[k] * c[k] for k in range(N))
    tangent = add(flatten2(outer2(a, y)), scale(F(-1), flatten2(outer2(x, b))))
    expected_third = add(scale(gw, tangent), scale(gc, flatten2({
        (i, j): C[i][j] for i in range(N) for j in range(N)
    })))
    assert tuple(flatten2(contract_third(gamma, value))) == expected_third


def audit_tangent_iff() -> None:
    vectors = [e(0), e(1), e(2), (F(1), F(1), F(0)), (F(1), F(1), F(1))]
    for x in vectors:
        for y in reversed(vectors):
            columns = tangent_columns(x, y)
            assert column_rank(columns) == 5
            for s in range(N):
                diagonal = flatten2(outer2(e(s), e(s)))
                assert in_columns(diagonal, columns) == (coordinate(x, s) or coordinate(y, s))


def audit_distinct_colours() -> None:
    count = 0
    for d, q, f in permutations(range(N)):
        kappa, lam, mu = F(d + 2), F(q + 5), F(f + 11)
        C = [[F(0) for _ in range(N)] for _ in range(N)]
        C[d][d], C[q][q], C[f][f] = kappa, lam, mu
        x, y, w = e(q), e(d), e(f)
        assert column_rank(derivative_columns(x, y, w, C)) == 8
        c_d = scale(-F(1, 1) / kappa, e(d))
        u_d = derivative(x, y, w, C, ZERO, ZERO, c_d)
        first = contract_first(e(d), u_d)
        second = contract_second(e(q), u_d)
        assert first == {k: -v for k, v in outer2(e(d), e(d)).items()}
        assert second == {
            k: -(lam / kappa) * v for k, v in outer2(e(q), e(d)).items()
        }
        assert any(second.values())
        count += 1
    assert count == 6


def audit_same_colour() -> None:
    for d in range(N):
        s, t = [i for i in range(N) if i != d]
        kappa, mu = F(d + 3), F(d + 8)
        C = [[F(0) for _ in range(N)] for _ in range(N)]
        C[d][d], C[s][s] = kappa, mu
        assert all(C[d][j] == (kappa if j == d else 0) for j in range(N))
        assert all(C[i][d] == (kappa if i == d else 0) for i in range(N))
        x, y, w = e(s), e(t), e(s)
        assert column_rank(derivative_columns(x, y, w, C)) == 8
        assert x[d] == y[d] == 0
        c_d = scale(-F(1, 1) / kappa, e(d))
        u_d = derivative(x, y, w, C, ZERO, ZERO, c_d)
        diagonal = {k: -v for k, v in outer2(e(d), e(d)).items()}
        assert contract_first(e(d), u_d) == diagonal
        assert contract_second(e(d), u_d) == diagonal


def main() -> None:
    audit_rank_and_kernel()
    audit_contractions()
    audit_tangent_iff()
    audit_distinct_colours()
    audit_same_colour()
    print(
        "S2BR independent audit passed: reversed-index Fraction derivative, "
        "contractions, tangent quotient, 6 distinct-colour contradictions, "
        "same-colour block shape."
    )


if __name__ == "__main__":
    main()
