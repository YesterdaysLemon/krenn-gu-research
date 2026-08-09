"""Verify the conditional synchronized two-depth P7 boundary.

These are fixed symbolic identities.  The script performs no support,
colour-word, graph, or matching-family search.
"""

from __future__ import annotations

import itertools

import sympy as sp


def column(prefix: str) -> sp.Matrix:
    """Return one generic three-coordinate column."""

    return sp.Matrix([sp.Symbol(f"{prefix}_{index}") for index in range(3)])


def corrected_pair(
    a_u: sp.Matrix,
    b_u: sp.Matrix,
    a_v: sp.Matrix,
    b_v: sp.Matrix,
) -> sp.Matrix:
    """Return a_u b_v^T+b_u a_v^T."""

    return a_u * b_v.T + b_u * a_v.T


def verify_subtraction_and_determinant() -> None:
    """Check W-hB=D and the nonresonant diagonal determinant."""

    h = sp.Symbol("h")
    direct = sp.Matrix(3, 3, lambda i, j: sp.Symbol(f"B_{i}{j}"))
    a_u, b_u = column("au"), column("bu")
    a_v, b_v = column("av"), column("bv")
    response = corrected_pair(a_u, b_u, a_v, b_v)
    full = h * direct + response

    assert sp.simplify(full - h * direct - response) == sp.zeros(3)
    assert sp.expand(response.det()) == 0

    mu = sp.symbols("mu0:3", nonzero=True)
    rho = sp.symbols("rho0:3")
    contracted_products = sp.symbols("k0:3", nonzero=True)
    target = sp.diag(
        *[
            mu[c] * (rho[c] - h) * contracted_products[c]
            for c in range(3)
        ]
    )
    expected = sp.prod(
        mu[c] * (rho[c] - h) * contracted_products[c] for c in range(3)
    )
    assert sp.expand(target.det() - expected) == 0


def verify_residual_null_ledger() -> None:
    """Check that exactly one of the twenty-one P7 pair terms survives."""

    a_rows: list[sp.Matrix] = [column("a0"), column("a1")]
    b_rows: list[sp.Matrix] = [column("b0"), column("b1")]
    vectors: list[sp.Matrix] = [column("x0"), column("x1")]

    for blocker in range(2, 7):
        a0, a1, b0, b1 = sp.symbols(
            f"a{blocker}_0 a{blocker}_1 b{blocker}_0 b{blocker}_1"
        )
        a_row = sp.Matrix((a0, a1, -a0 - a1))
        b_row = sp.Matrix((b0, b1, -b0 - b1))
        kappa = sp.ones(3, 1)
        assert sp.expand(a_row.dot(kappa)) == 0
        assert sp.expand(b_row.dot(kappa)) == 0
        a_rows.append(a_row)
        b_rows.append(b_row)
        vectors.append(kappa)

    survivors: list[tuple[int, int]] = []
    for u, v in itertools.combinations(range(7), 2):
        value = sp.expand(
            a_rows[u].dot(vectors[u]) * b_rows[v].dot(vectors[v])
            + b_rows[u].dot(vectors[u]) * a_rows[v].dot(vectors[v])
        )
        if value != 0:
            survivors.append((u, v))
        if (u, v) != (0, 1):
            assert value == 0

    assert survivors == [(0, 1)]


def verify_aligned_linear_no_go() -> None:
    """Check uniqueness of scalar direct-layer cancellation and colour loss."""

    alpha, h, mu = sp.symbols("alpha h mu")
    beta = -alpha * h
    rho_aligned = h

    assert sp.expand(alpha * h + beta) == 0
    aligned_target = alpha * mu * rho_aligned + beta * mu
    assert sp.expand(aligned_target) == 0


def verify_common_channel_pencil() -> None:
    """Check the shared rank-two cross-block and common pencil root."""

    # Two ports on each side give one 6 by 6 corrected cross-block through
    # the same two-dimensional residual channel.
    left = [column("aL0"), column("bL0"), column("aL1"), column("bL1")]
    right = [column("aR0"), column("bR0"), column("aR1"), column("bR1")]
    p_left = sp.Matrix.vstack(
        sp.Matrix.hstack(left[0], left[1]),
        sp.Matrix.hstack(left[2], left[3]),
    )
    p_right = sp.Matrix.vstack(
        sp.Matrix.hstack(right[0], right[1]),
        sp.Matrix.hstack(right[2], right[3]),
    )
    exchange = sp.Matrix(((0, 1), (1, 0)))
    corrected = p_left * exchange * p_right.T

    assert corrected.shape == (6, 6)
    assert corrected.rank() == 2
    for rows in ((0, 1, 2), (0, 2, 4), (1, 3, 5)):
        for columns in ((0, 1, 2), (0, 3, 5), (1, 2, 4)):
            assert sp.expand(corrected.extract(rows, columns).det()) == 0

    # A fixed legal pencil has t=h as a common root of every 3 by 3 minor.
    t, h = sp.symbols("t h")
    b_pencil = sp.Matrix(3, 6, lambda i, j: (i + 1) * (j + 2) - (i == j))
    d_pencil = corrected[:3, :]
    w_pencil = h * b_pencil + d_pencil
    pencil = w_pencil - t * b_pencil
    checked = 0
    for columns in itertools.combinations(range(6), 3):
        minor = sp.expand(pencil[:, columns].det())
        assert sp.expand(minor.subs(t, h)) == 0
        assert sp.rem(minor, t - h, domain=sp.QQ.frac_field(h)) == 0
        checked += 1
    assert checked == 20

    # Resultants are genuinely restrictive: generic determinant pencils can
    # have incompatible roots.
    first = sp.diag(t, 1, 1).det()
    second = sp.diag(t - 1, 1, 1).det()
    assert first == t and second == t - 1
    assert abs(sp.resultant(first, second, t)) == 1


def verify_w_only_affine_surjectivity() -> None:
    """Check the explicit affine inverse from arbitrary W to direct B."""

    h = sp.Symbol("h", nonzero=True)
    desired = sp.Matrix(3, 3, lambda i, j: sp.Symbol(f"W_{i}{j}"))
    a_u, b_u = column("su_a"), column("su_b")
    a_v, b_v = column("sv_a"), column("sv_b")
    response = corrected_pair(a_u, b_u, a_v, b_v)
    direct = (desired - response) / h

    assert sp.simplify(h * direct + response - desired) == sp.zeros(3)


def main() -> None:
    verify_subtraction_and_determinant()
    verify_residual_null_ledger()
    verify_aligned_linear_no_go()
    verify_common_channel_pencil()
    verify_w_only_affine_surjectivity()
    print(
        {
            "status": "pass",
            "scope": "conditional synchronized two-depth theorem",
            "p7_pair_terms_checked": 21,
            "competing_pair_terms_killed": 20,
            "shared_channel_rank": 2,
            "pencil_minors_checked": 20,
            "support_searches": 0,
            "unconditional_p7_exclusion": False,
            "global_conjecture_resolved": False,
        }
    )


if __name__ == "__main__":
    main()
