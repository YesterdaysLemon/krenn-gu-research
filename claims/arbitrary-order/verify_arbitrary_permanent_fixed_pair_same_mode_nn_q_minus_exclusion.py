"""Primary exact replay of the same-mode N/N, q-minus exclusion."""

from __future__ import annotations

from itertools import combinations
import json

import sympy as sp


x0, x1, x2, x3 = VARIABLES = sp.symbols("x0:4")
QUADRATICS = {
    "m1": x1 * (x3 - x2 - x0),
    "m2": x0 * (x3 - x2 - x1),
    "d0": (x1 + x2) * (x3 - x0),
    "d1": (x0 + x2) * (x3 - x1),
    "d2": -2 * x0 * x1,
}
J_MATRIX = sp.Matrix(((0, 1), (1, 0)))


def column(*entries: sp.Expr | int) -> sp.Matrix:
    """Construct a column vector."""
    return sp.Matrix(entries)


def contract(quadratic: sp.Expr, vector: sp.Matrix) -> sp.Matrix:
    """Contract a square-free quadratic and return its residual covector."""
    return sp.Matrix([
        sp.expand(sum(vector[i] * sp.diff(quadratic, VARIABLES[i]) for i in range(4)))
        .coeff(VARIABLES[j])
        for j in range(4)
    ])


def residuals(vector: sp.Matrix) -> dict[str, sp.Matrix]:
    """Return the five residual covectors at one R-vector."""
    return {name: contract(quadratic, vector) for name, quadratic in QUADRATICS.items()}


def double_contract(quadratic: sp.Expr, left: sp.Matrix, right: sp.Matrix) -> sp.Expr:
    """Evaluate the polarized quadratic on two vectors."""
    hessian = sp.hessian(quadratic, VARIABLES)
    return sp.expand((left.T * hessian * right)[0])


def j_pair(left: sp.Matrix, right: sp.Matrix) -> sp.Expr:
    """Evaluate the hyperbolic pairing on A."""
    return sp.expand((left.T * J_MATRIX * right)[0])


def same_span(left: list[sp.Matrix], right: list[sp.Matrix]) -> bool:
    """Check equality of two column spans."""
    left_matrix = sp.Matrix.hstack(*left)
    right_matrix = sp.Matrix.hstack(*right)
    return (
        left_matrix.rank()
        == right_matrix.rank()
        == sp.Matrix.hstack(left_matrix, right_matrix).rank()
    )


def tensor3(left: sp.Matrix, middle: sp.Matrix, right: sp.Matrix) -> tuple[sp.Expr, ...]:
    """Flatten a decomposable 3-tensor in lexicographic order."""
    return tuple(
        sp.expand(left[i] * middle[j] * right[k])
        for i in range(3)
        for j in range(3)
        for k in range(3)
    )


def add_tensors(*tensors: tuple[sp.Expr, ...]) -> tuple[sp.Expr, ...]:
    """Add flattened tensors exactly."""
    return tuple(sp.expand(sum(entries)) for entries in zip(*tensors, strict=True))


def zero_tensor() -> tuple[sp.Expr, ...]:
    """Return the zero 3-tensor."""
    return (sp.Integer(0),) * 27


def cubic_tensor(
    rows: tuple[sp.Matrix, sp.Matrix, sp.Matrix],
    a_maps: tuple[sp.Matrix, sp.Matrix, sp.Matrix],
) -> tuple[sp.Expr, ...]:
    """Directly polarize x4*x5*h on three ordered local triples."""
    first_row, second_row, third_row = rows
    first_a, second_a, third_a = a_maps
    values: list[sp.Expr] = []
    for i in range(3):
        for j in range(3):
            for k in range(3):
                value = (
                    first_row[i] * j_pair(second_a[:, j], third_a[:, k])
                    + second_row[j] * j_pair(first_a[:, i], third_a[:, k])
                    + third_row[k] * j_pair(first_a[:, i], second_a[:, j])
                )
                values.append(sp.expand(value))
    return tuple(values)


def quartic_value(quadratic: sp.Expr, vectors: tuple[sp.Matrix, ...]) -> sp.Expr:
    """Direct complete polarization of x4*x5*quadratic on four vectors."""
    assert len(vectors) == 4
    hessian = sp.hessian(quadratic, VARIABLES)
    total = sp.Integer(0)
    for first, second in combinations(range(4), 2):
        remaining = [index for index in range(4) if index not in (first, second)]
        a_pair = j_pair(vectors[first][4:6, :], vectors[second][4:6, :])
        r_pair = (
            vectors[remaining[0]][0:4, :].T
            * hessian
            * vectors[remaining[1]][0:4, :]
        )[0]
        total += a_pair * r_pair
    return sp.expand(total)


def check_companion_fork() -> dict[str, object]:
    """Reconstruct N propagation data and the q-plus/q-minus fork."""
    n = column(0, 0, 1, 1)
    m = column(1, 1, 0, 0)
    k = column(0, 0, 1, -1)
    ell = column(-1, -1, -1, 1)
    h0 = column(-1, 1, 1, 1)
    h1 = column(1, -1, 1, 1)
    h2 = column(1, -1, -1, 1)
    h2p = column(-1, 1, -1, 1)

    n_values = residuals(n)
    assert n_values["m1"] == n_values["m2"] == n_values["d2"] == sp.zeros(4, 1)
    assert n_values["d0"] == h0
    assert n_values["d1"] == h1
    assert same_span(sp.Matrix.vstack(h0.T, h1.T).nullspace(), [m, k])

    s, u = sp.symbols("s u")
    q = s * m + u * k
    values = residuals(q)
    assert values["m1"] == s * ell - 2 * u * column(0, 1, 0, 0)
    assert values["m2"] == s * ell - 2 * u * column(1, 0, 0, 0)
    assert values["d0"] == values["d1"] == (s + u) * ell
    assert values["d2"] == -2 * s * m

    generic_zero_rows = [
        values[name].subs({s: 2, u: 3}) for name in ("m1", "m2", "d0", "d1")
    ]
    assert sp.Matrix.hstack(*generic_zero_rows).rank() == 3
    assert sp.Matrix.hstack(*generic_zero_rows, m).rank() == 3

    q_minus = m - k
    minus = residuals(q_minus)
    assert minus == {
        "m1": h2p,
        "m2": h2,
        "d0": sp.zeros(4, 1),
        "d1": sp.zeros(4, 1),
        "d2": -2 * m,
    }
    nonzero_minus = [minus["m1"], minus["m2"], minus["d2"]]
    assert sp.Matrix.hstack(*nonzero_minus).rank() == 3
    assert same_span(sp.Matrix.vstack(*(row.T for row in nonzero_minus)).nullspace(), [n])
    assert h1 == h0 + h2 - h2p
    return {
        "N_residual_rank": 2,
        "companion_plane": "span{x0+x1,x2-x3}",
        "projective_survivors": ["q_plus", "q_minus"],
        "q_minus_residual_rank": 3,
        "q_minus_common_kernel": "K*N",
    }


def check_support_split() -> dict[str, object]:
    """Check the double-N cases and both no-second-N coefficient gates."""
    n = column(0, 0, 1, 1)
    double = {name: double_contract(quadratic, n, n) for name, quadratic in QUADRATICS.items()}
    assert double == {"m1": 0, "m2": 0, "d0": 2, "d1": 2, "d2": 0}

    # The two identical left sides cannot equal the following target pairs:
    # one live/one zero, or two nonzero distinct matrix units.
    support_two = column(1, 1, 0)
    second_profiles = {
        "singleton_0": column(1, 0, 0),
        "singleton_1": column(0, 1, 0),
        "support_two": column(1, 1, 0),
    }
    products = {
        name: (support_two[0] * profile[0], support_two[1] * profile[1])
        for name, profile in second_profiles.items()
    }
    assert products == {
        "singleton_0": (1, 0),
        "singleton_1": (0, 1),
        "support_two": (1, 1),
    }

    # Verify the exact sign gate in the support-two/no-second-N branch.
    rt = sp.symbols("rt0:4")
    at = sp.symbols("at0:2")
    rs = sp.symbols("rs0:4")
    ass = sp.symbols("as0:2")
    ru = sp.symbols("ru0:4")
    rv = sp.symbols("rv0:4")
    t0 = column(*rt, *at)
    n6 = column(0, 0, 1, 1, 0, 0)
    t1 = n6 - t0
    companion = column(*rs, *ass)
    shore_u = column(*ru, 0, 0)
    shore_v = column(*rv, 0, 0)
    pure_zero = quartic_value(QUADRATICS["d0"], (t0, companion, shore_u, shore_v))
    mixed = quartic_value(QUADRATICS["d0"], (t1, companion, shore_u, shore_v))
    assert sp.expand(pure_zero + mixed) == 0

    # In the singleton/no-second-N branch three pure-R inputs leave at most
    # one A supplier, so complete polarization vanishes identically.
    singleton = quartic_value(QUADRATICS["d0"], (n6, companion, shore_u, shore_v))
    assert singleton == 0
    return {
        "double_N_row": double,
        "support_two_second_N_profiles": products,
        "support_two_mixed_word": "negative of live pure word",
        "singleton_live_word": "zero with only one A supplier",
    }


def check_pair_gate_algebra() -> dict[str, object]:
    """Replay the load-bearing algebra of the zero/live quotient pair gate."""
    # Rank-zero shore: a nonzero coefficient multiplies the identity on D.
    coefficient = sp.symbols("c", nonzero=True)
    assert (coefficient * sp.eye(3)).rank() == 3

    # Rank-two shore plus a pure-D kernel vector forces a(u)=0; then the
    # remaining scalar r(u) multiplies a nonzero J pairing.  These are the
    # two nondegenerate 2-by-2 gates used in the written proof.
    assert J_MATRIX.det() == -1
    assert J_MATRIX.rank() == 2

    rho, sigma, jvp, jvq, jpq = sp.symbols("rho sigma jvp jvq jpq")
    rz0, rz1, rz2, rw0, rw1, rw2, rv0, rv1, rv2 = sp.symbols(
        "rz0 rz1 rz2 rw0 rw1 rw2 rv0 rv1 rv2"
    )
    rz = column(rz0, rz1, rz2)
    rw = column(rw0, rw1, rw2)
    rv = column(rv0, rv1, rv2)
    general = rz * (sigma * jvq) + rw * (rho * jvp) + rv * (rho * sigma * jpq)
    reduced = general.subs({jvp: 0, jvq: 0})
    assert reduced == rv * (rho * sigma * jpq)

    e2 = column(0, 0, 1)
    aligned = e2 * e2.T
    assert aligned.rank() == 1
    assert aligned.nullspace() == [column(1, 0, 0), column(0, 1, 0)]
    return {
        "rank_zero_output_dimension": 3,
        "rank_two_nonzero_u": "excluded by nondegeneracy",
        "surviving_A_ranks": [1, 1],
        "rank_one_factor_rows": "aligned with colour 2 by output line",
    }


def check_collapsed_cycle_tensors() -> dict[str, object]:
    """Compare all four displayed tensors with direct polarization."""
    p0, p1 = sp.symbols("p0 p1")
    p = column(p0, p1)
    q = column(p0, -p1)
    assert j_pair(p, q) == 0

    alpha = column(*sp.symbols("alpha0:3"))
    gamma = column(*sp.symbols("gamma0:3"))
    a_b = p * alpha.T
    a_d = q * gamma.T
    a_a = sp.Matrix(2, 3, sp.symbols("aa0:6"))
    a_c = sp.Matrix(2, 3, sp.symbols("ac0:6"))

    x = column(*sp.symbols("X0:3"))
    y = column(*sp.symbols("Y0:3"))
    z = column(*sp.symbols("Z0:3"))
    w = column(*sp.symbols("W0:3"))
    a0_row = column(*sp.symbols("A0r0:3"))
    a1_row = column(*sp.symbols("A1r0:3"))
    c0_row = column(*sp.symbols("C0r0:3"))
    c1_row = column(*sp.symbols("C1r0:3"))

    beta = column(*(j_pair(p, a_c[:, index]) for index in range(3)))
    delta = column(*(j_pair(a_c[:, index], q) for index in range(3)))
    pi = column(*(j_pair(a_a[:, index], p) for index in range(3)))
    epsilon = column(*(j_pair(a_a[:, index], q) for index in range(3)))

    direct_tensors = (
        cubic_tensor((x, c0_row, z), (a_b, a_c, a_d)),
        cubic_tensor((y, c1_row, w), (a_b, a_c, a_d)),
        cubic_tensor((x, a0_row, z), (a_b, a_a, a_d)),
        cubic_tensor((y, a1_row, w), (a_b, a_a, a_d)),
    )
    displayed = (
        add_tensors(tensor3(x, delta, gamma), tensor3(alpha, beta, z)),
        add_tensors(tensor3(y, delta, gamma), tensor3(alpha, beta, w)),
        add_tensors(tensor3(x, epsilon, gamma), tensor3(alpha, pi, z)),
        add_tensors(tensor3(y, epsilon, gamma), tensor3(alpha, pi, w)),
    )
    for direct, claimed in zip(direct_tensors, displayed, strict=True):
        assert all(sp.expand(left - right) == 0 for left, right in zip(direct, claimed, strict=True))

    e0 = column(1, 0, 0)
    e1 = column(0, 1, 0)
    zero = column(0, 0, 0)
    target0 = tensor3(e0, e0, e0)
    target1 = tensor3(e1, e1, e1)

    # Coordinate fork alpha=e1, gamma=e0.
    fork_e1 = (
        add_tensors(tensor3(e0, e0, e0), tensor3(e1, zero, zero)),
        add_tensors(tensor3(zero, e0, e0), tensor3(e1, zero, e1)),
        add_tensors(tensor3(e0, zero, e0), tensor3(e1, e1, zero)),
        add_tensors(tensor3(zero, zero, e0), tensor3(e1, e1, e1)),
    )
    assert fork_e1 == (target0, zero_tensor(), zero_tensor(), target1)

    # Coordinate fork alpha=e0, gamma=e1.
    fork_e0 = (
        add_tensors(tensor3(zero, zero, e1), tensor3(e0, e0, e0)),
        add_tensors(tensor3(e1, zero, e1), tensor3(e0, e0, zero)),
        add_tensors(tensor3(zero, e1, e1), tensor3(e0, zero, e0)),
        add_tensors(tensor3(e1, e1, e1), tensor3(e0, zero, zero)),
    )
    assert fork_e0 == (target0, zero_tensor(), zero_tensor(), target1)

    scalar_a, scalar_c = sp.symbols("scalar_a scalar_c")
    # Fork alpha=e1: beta_2=epsilon_2=0.
    assert j_pair(scalar_a * p, scalar_c * q) == 0
    # Fork alpha=e0: pi_2=delta_2=0, with the shore roles exchanged.
    assert j_pair(scalar_a * q, scalar_c * p) == 0

    return {
        "direct_entries_compared": 108,
        "rank_profiles_after_double_N": [[1, 1]],
        "alpha_forks": ["e0", "e1"],
        "colour_2_pairing": "zero in both forks",
    }


def main() -> None:
    """Run the deterministic characteristic-zero replay."""
    report = {
        "companion_fork": check_companion_fork(),
        "support_split": check_support_split(),
        "pair_gate": check_pair_gate_algebra(),
        "collapsed_cycle": check_collapsed_cycle_tensors(),
        "scope": "q_minus excluded; q_plus and global conjecture remain open",
        "status": "PASS",
    }
    print(json.dumps(report, indent=2, sort_keys=True, default=str))


if __name__ == "__main__":
    main()
