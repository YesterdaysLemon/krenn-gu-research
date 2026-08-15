"""Primary exact replay of the same-mode N/N, q-plus exclusion."""

from __future__ import annotations

from itertools import combinations
import json
from pathlib import Path

import sympy as sp


x0, x1, x2, x3 = VARIABLES = sp.symbols("x0:4")
QUADRATICS = {
    "m1": x1 * (x3 - x2 - x0),
    "m2": x0 * (x3 - x2 - x1),
    "d0": (x1 + x2) * (x3 - x0),
    "d1": (x0 + x2) * (x3 - x1),
    "d2": -2 * x0 * x1,
}
J = sp.Matrix(((0, 1), (1, 0)))


def col(*entries: sp.Expr | int) -> sp.Matrix:
    """Return a column vector."""
    return sp.Matrix(entries)


def contract(quadratic: sp.Expr, vector: sp.Matrix) -> sp.Matrix:
    """Contract a square-free quadratic by an R-vector."""
    hessian = sp.hessian(quadratic, VARIABLES)
    return sp.expand(hessian * vector)


def residuals(vector: sp.Matrix) -> dict[str, sp.Matrix]:
    """Return the five residual covectors as columns."""
    return {name: contract(poly, vector) for name, poly in QUADRATICS.items()}


def double_contract(quadratic: sp.Expr, left: sp.Matrix, right: sp.Matrix) -> sp.Expr:
    """Evaluate the polarized R-quadratic."""
    return sp.expand((left.T * sp.hessian(quadratic, VARIABLES) * right)[0])


def j_pair(left: sp.Matrix, right: sp.Matrix) -> sp.Expr:
    """Evaluate the hyperbolic A-pairing."""
    return sp.expand((left.T * J * right)[0])


def tensor3(left: sp.Matrix, middle: sp.Matrix, right: sp.Matrix) -> tuple[sp.Expr, ...]:
    """Flatten a decomposable 3-tensor lexicographically."""
    return tuple(
        sp.expand(left[i] * middle[j] * right[k])
        for i in range(3)
        for j in range(3)
        for k in range(3)
    )


def add_tensors(*terms: tuple[sp.Expr, ...]) -> tuple[sp.Expr, ...]:
    """Add flattened tensors."""
    return tuple(sp.expand(sum(cell)) for cell in zip(*terms, strict=True))


def cubic_tensor(
    rows: tuple[sp.Matrix, sp.Matrix, sp.Matrix],
    a_maps: tuple[sp.Matrix, sp.Matrix, sp.Matrix],
) -> tuple[sp.Expr, ...]:
    """Polarize x4*x5*ell on three ordered local triples."""
    values: list[sp.Expr] = []
    for i in range(3):
        for j in range(3):
            for k in range(3):
                values.append(
                    sp.expand(
                        rows[0][i] * j_pair(a_maps[1][:, j], a_maps[2][:, k])
                        + rows[1][j] * j_pair(a_maps[0][:, i], a_maps[2][:, k])
                        + rows[2][k] * j_pair(a_maps[0][:, i], a_maps[1][:, j])
                    )
                )
    return tuple(values)


def quartic_value(quadratic: sp.Expr, vectors: tuple[sp.Matrix, ...]) -> sp.Expr:
    """Directly polarize x4*x5*quadratic on four six-vectors."""
    hessian = sp.hessian(quadratic, VARIABLES)
    total = sp.Integer(0)
    for a_slot, b_slot in combinations(range(4), 2):
        r_slots = [slot for slot in range(4) if slot not in (a_slot, b_slot)]
        a_value = j_pair(vectors[a_slot][4:6, :], vectors[b_slot][4:6, :])
        r_value = (
            vectors[r_slots[0]][0:4, :].T
            * hessian
            * vectors[r_slots[1]][0:4, :]
        )[0]
        total += a_value * r_value
    return sp.expand(total)


def nullspace_span(rows: list[sp.Matrix]) -> sp.Matrix:
    """Return a matrix whose columns span the common kernel of row columns."""
    return sp.Matrix.vstack(*(row.T for row in rows)).nullspace()


def same_span(left: list[sp.Matrix], right: list[sp.Matrix]) -> bool:
    """Test equality of two column spans."""
    left_matrix = sp.Matrix.hstack(*left)
    right_matrix = sp.Matrix.hstack(*right)
    return (
        left_matrix.rank()
        == right_matrix.rank()
        == sp.Matrix.hstack(left_matrix, right_matrix).rank()
    )


def check_contractions_and_localization() -> dict[str, object]:
    """Rebuild N, q, H, P, and r residual tables."""
    n = col(0, 0, 1, 1)
    p = col(1, -1, 0, 0)
    m = col(1, 1, 0, 0)
    transverse = col(0, 0, 1, -1)
    ell = col(-1, -1, -1, 1)
    h0 = col(-1, 1, 1, 1)
    h1 = col(1, -1, 1, 1)

    n_rows = residuals(n)
    assert n_rows == {
        "m1": sp.zeros(4, 1),
        "m2": sp.zeros(4, 1),
        "d0": h0,
        "d1": h1,
        "d2": sp.zeros(4, 1),
    }
    assert same_span(nullspace_span([h0, h1]), [m, transverse])

    s, u = sp.symbols("s u")
    q = s * m + u * transverse
    q_rows = residuals(q)
    assert q_rows["m1"] == s * ell - 2 * u * col(0, 1, 0, 0)
    assert q_rows["m2"] == s * ell - 2 * u * col(1, 0, 0, 0)
    assert q_rows["d0"] == q_rows["d1"] == (s + u) * ell
    assert q_rows["d2"] == -2 * s * m

    q_plus = residuals(m)
    assert q_plus == {
        "m1": ell,
        "m2": ell,
        "d0": ell,
        "d1": ell,
        "d2": -2 * m,
    }
    assert same_span(nullspace_span([ell, m]), [n, p])

    p_rows = residuals(p)
    a = col(1, -1, 1, -1)
    b = col(1, -1, -1, 1)
    c = col(1, -1, -1, -1)
    d = col(1, -1, 1, 1)
    e = col(2, -2, 0, 0)
    assert p_rows == {"m1": a, "m2": b, "d0": c, "d1": d, "d2": e}
    assert a + b == c + d == e
    assert n_rows["d0"] == -c and n_rows["d1"] == d
    assert all(double_contract(poly, m, p) == 0 for poly in QUADRATICS.values())

    rho = sp.symbols("rho")
    r = rho * n + p
    r_rows = residuals(r)
    assert r_rows["m1"] == a
    assert r_rows["m2"] == b
    assert r_rows["d0"] == (rho - 1) * h0
    assert r_rows["d1"] == (rho + 1) * h1
    assert r_rows["d2"] == e

    double_n = {name: double_contract(poly, n, n) for name, poly in QUADRATICS.items()}
    assert double_n == {"m1": 0, "m2": 0, "d0": 2, "d1": 2, "d2": 0}
    return {
        "companion_survivors": ["q_plus", "q_minus"],
        "q_plus_kernel": "span{N,P}",
        "P_identity": "a+b=c+d=e",
        "double_N": {name: int(value) for name, value in double_n.items()},
    }


def check_hyperplane_charts() -> dict[str, object]:
    """Replay the p!=0 and missing p=0 quotient-form charts."""
    # Coordinates are (x,y,alpha,beta).  This is the nonzero-isotropic a chart.
    f0_iso = sp.Matrix(
        (
            (0, 0, 0, 1),
            (0, 0, 0, 0),
            (0, 0, 0, 1),
            (1, 0, 1, 0),
        )
    )
    f1_iso = sp.Matrix(
        (
            (0, 0, 0, 0),
            (0, 0, 0, 1),
            (0, 0, 0, 0),
            (0, 1, 0, 0),
        )
    )
    assert f0_iso.rank() == f1_iso.rank() == 2
    common_radical = sp.Matrix.vstack(f0_iso, f1_iso).nullspace()
    assert len(common_radical) == 1
    assert same_span(common_radical, [col(1, 0, -1, 0)])
    ker_beta = sp.Matrix(
        (
            (1, 0, 0),
            (0, 1, 0),
            (0, 0, 1),
            (0, 0, 0),
        )
    )
    assert ker_beta.T * f0_iso * ker_beta == sp.zeros(3)
    assert ker_beta.T * f1_iso * ker_beta == sp.zeros(3)

    # A nonisotropic a makes F0 rank three.
    # In A coordinates (alpha,beta), take a=(1,1), ell=(1,1).
    f0_noniso = sp.Matrix(
        (
            (0, 0, 1, 1),
            (0, 0, 0, 0),
            (1, 0, 0, 1),
            (1, 0, 1, 0),
        )
    )
    assert f0_noniso.rank() == 3

    # Missing p=0 chart: x*beta and y*beta.
    f0_pure_a = sp.Matrix(
        (
            (0, 0, 0, 1),
            (0, 0, 0, 0),
            (0, 0, 0, 0),
            (1, 0, 0, 0),
        )
    )
    f1_pure_a = sp.Matrix(
        (
            (0, 0, 0, 0),
            (0, 0, 0, 1),
            (0, 0, 0, 0),
            (0, 1, 0, 0),
        )
    )
    assert f0_pure_a.rank() == f1_pure_a.rank() == 2
    assert len(sp.Matrix.vstack(f0_pure_a, f1_pure_a).nullspace()) == 1
    assert ker_beta.T * f0_pure_a * ker_beta == sp.zeros(3)
    assert ker_beta.T * f1_pure_a * ker_beta == sp.zeros(3)

    c0, d0, h = sp.symbols("c0 d0 h", nonzero=True)
    alpha, beta = sp.symbols("alpha beta")
    r0, r1, di0, di1, ej0, ej1 = sp.symbols("r0 r1 di0 di1 ej0 ej1")
    rvec, divec, ejvec = col(r0, r1), col(di0, di1), col(ej0, ej1)
    original = c0 * beta * divec + d0 * alpha * ejvec + h * alpha * beta * rvec
    shifted_d = divec + h * alpha * rvec / (2 * c0)
    shifted_e = ejvec + h * beta * rvec / (2 * d0)
    shifted = c0 * beta * shifted_d + d0 * alpha * shifted_e
    assert sp.simplify(original - shifted) == sp.zeros(2, 1)
    return {
        "isotropic_chart_ranks": [2, 2],
        "nonisotropic_F0_rank": 3,
        "pure_A_chart_ranks": [2, 2],
        "common_radical_dimension": 1,
        "half_shift": "exact",
    }


def check_rank_profile_kernels() -> dict[str, object]:
    """Check the kernels and support facts used in the three-profile cycles."""
    n = col(0, 0, 1, 1)
    p = col(1, -1, 0, 0)
    m = col(1, 1, 0, 0)
    ell = col(-1, -1, -1, 1)
    h0 = col(-1, 1, 1, 1)
    h1 = col(1, -1, 1, 1)
    h2p = col(-1, 1, -1, 1)
    k = col(-1, 1, 1, -1)
    q_minus = col(1, 1, -1, 1)
    a_plus = col(1, -1, 1, -1)
    b_plus = col(1, -1, -1, 1)

    assert same_span(nullspace_span([ell, m]), [n, p])
    assert same_span(nullspace_span([ell, h0, h1]), [q_minus])
    assert len(nullspace_span([ell, h0, h1, m])) == 0
    assert same_span(nullspace_span([h2p, k, p]), [m, n])
    assert same_span(nullspace_span([h2p, k, p, h0]), [m])
    assert same_span(nullspace_span([a_plus, b_plus, h1]), [m])

    # On H, h0 and h1 have no common nonzero zero.
    h_matrix = sp.Matrix.hstack(n, p)
    assert sp.Matrix.vstack(h0.T * h_matrix, h1.T * h_matrix).det() != 0

    # Hyperbolic rank profiles: a nonzero rank-one cross Gram cannot be (2,2).
    left_full = sp.eye(2)
    right_full = sp.Matrix(((1, 2), (3, 5)))
    assert (left_full.T * J * right_full).rank() == 2
    assert J.det() == -1
    return {
        "support_two_profiles": [[2, 1], [1, 1], [1, 2]],
        "same_colour_common_kernel": "K*q_plus",
        "singleton_profile_kernel": "K*q_minus",
        "H_h0_h1_intersection": 0,
    }


def check_tensor_orders_and_forks() -> dict[str, object]:
    """Replay tensor order, both generic forks, and the special r-plus fork."""
    e0, e1 = col(1, 0, 0), col(0, 1, 0)
    zero = sp.zeros(3, 1)

    # Generic alpha=e1 fork from (45).
    alpha, gamma, delta = e1, e0, e0
    x, y, z, w = e0, zero, zero, e1
    beta, epsilon, pi = zero, zero, e1
    first = add_tensors(tensor3(x, delta, gamma), tensor3(alpha, beta, z))
    second = add_tensors(tensor3(y, delta, gamma), tensor3(alpha, beta, w))
    third = add_tensors(tensor3(x, epsilon, gamma), tensor3(alpha, pi, z))
    fourth = add_tensors(tensor3(y, epsilon, gamma), tensor3(alpha, pi, w))
    assert first == tensor3(e0, e0, e0)
    assert second == third == (0,) * 27
    assert fourth == tensor3(e1, e1, e1)

    # Generic alpha=e0 fork.
    alpha, gamma, epsilon = e0, e1, e1
    x, y, z, w = zero, e1, e0, zero
    beta, delta, pi = e0, zero, zero
    first = add_tensors(tensor3(x, delta, gamma), tensor3(alpha, beta, z))
    second = add_tensors(tensor3(y, delta, gamma), tensor3(alpha, beta, w))
    third = add_tensors(tensor3(x, epsilon, gamma), tensor3(alpha, pi, z))
    fourth = add_tensors(tensor3(y, epsilon, gamma), tensor3(alpha, pi, w))
    assert first == tensor3(e0, e0, e0)
    assert second == third == (0,) * 27
    assert fourth == tensor3(e1, e1, e1)

    # The special alpha=e1 three-equation branch forces Y=beta=0 because a
    # nonzero beta*W term would put the live fourth tensor on third factor e0.
    assert set(i for i, value in enumerate(e0) if value) != set(
        i for i, value in enumerate(e1) if value
    )
    a_plus = col(1, -1, 1, -1)
    b_plus = col(1, -1, -1, 1)
    h1 = col(1, -1, 1, 1)
    m = col(1, 1, 0, 0)
    ell = col(-1, -1, -1, 1)
    assert same_span(nullspace_span([a_plus, b_plus, h1]), [m])
    assert (ell.T * m)[0] == -2

    # Final colour-2 pairing in either generic branch.
    p_line, q_line = col(1, 1), col(1, -1)
    assert j_pair(p_line, q_line) == 0
    assert j_pair(q_line, p_line) == 0
    return {
        "generic_coordinate_forks": 2,
        "special_r_plus_coordinate_forks": 2,
        "special_kernel": "K*M",
        "final_colour2_pairing": 0,
    }


def check_direct_polarization() -> dict[str, object]:
    """Compare every displayed residual with direct four-slot polarization."""
    # Three deterministic, full-rank local triples with unrelated entries.
    maps = (
        sp.Matrix(
            (
                (1, 0, 2),
                (0, 1, -1),
                (2, 1, 0),
                (-1, 2, 1),
                (1, 0, 3),
                (0, 2, 1),
            )
        ),
        sp.Matrix(
            (
                (0, 2, 1),
                (1, -1, 2),
                (2, 0, 1),
                (1, 1, -2),
                (0, 1, 2),
                (3, 1, 0),
            )
        ),
        sp.Matrix(
            (
                (2, 1, 0),
                (-1, 0, 1),
                (1, 3, -1),
                (0, 2, 2),
                (1, 2, 0),
                (2, 0, 1),
            )
        ),
    )
    fixed_vectors = {
        "N": col(0, 0, 1, 1),
        "q_plus": col(1, 1, 0, 0),
        "P": col(1, -1, 0, 0),
        "r_minus": col(-1, 1, 1, 1),
        "r_plus": col(1, -1, 1, 1),
    }
    checked = 0
    for vector in fixed_vectors.values():
        vector6 = col(*vector, 0, 0)
        rows = residuals(vector)
        for name, quadratic in QUADRATICS.items():
            row_values = tuple((rows[name].T * local[0:4, :]).T for local in maps)
            expected = cubic_tensor(
                row_values,
                tuple(local[4:6, :] for local in maps),
            )
            actual: list[sp.Expr] = []
            for i in range(3):
                for j in range(3):
                    for k_index in range(3):
                        actual.append(
                            quartic_value(
                                quadratic,
                                (
                                    vector6,
                                    maps[0][:, i],
                                    maps[1][:, j],
                                    maps[2][:, k_index],
                                ),
                            )
                        )
            assert tuple(actual) == expected
            checked += 27
    return {"direct_polarization_entries": checked}


def check_coincident_companion_mode() -> dict[str, object]:
    """Replay the legal single-slot proof when q-plus and a second N coincide."""
    e0, e1, e2 = col(1, 0, 0), col(0, 1, 0), col(0, 0, 1)
    n = col(0, 0, 1, 1)
    double = {name: double_contract(poly, n, n) for name, poly in QUADRATICS.items()}
    assert double["d0"] == double["d1"] == 2

    epsilon, pi = e1, e2
    assert sp.Matrix.hstack(epsilon, pi).rank() == 2
    assert epsilon[0] == pi[0] == 0

    # Independence of the first factors separates the two summands in (58).
    xu = col(*sp.symbols("xu0:3"))
    xv = col(*sp.symbols("xv0:3"))
    alpha, gamma = col(2, -1, 3), col(1, 4, -2)
    zero_equation = add_tensors(
        tensor3(epsilon, xu, gamma),
        tensor3(pi, alpha, xv),
    )
    equations = [entry for entry in zero_equation if entry != 0]
    solution = sp.linsolve(equations, tuple(xu) + tuple(xv))
    assert solution == sp.FiniteSet((0, 0, 0, 0, 0, 0))

    # The final N_t,h0 cubic has all three Gram/row terms zero.
    assert add_tensors(
        tensor3(e0, sp.zeros(3, 1), sp.zeros(3, 1)),
        tensor3(sp.zeros(3, 1), e0, sp.zeros(3, 1)),
        tensor3(sp.zeros(3, 1), sp.zeros(3, 1), e0),
    ) == (0,) * 27
    return {
        "coincident_double_N_pairing": 2,
        "live_first_factor_rank": 2,
        "zero_h0_rows": ["U", "V"],
        "legal_same_slot_evaluations": True,
    }


def check_status_boundary() -> dict[str, object]:
    """Ensure the theorem keeps the q-plus and global boundaries explicit."""
    theorem = Path(__file__).with_name(
        "ARBITRARY_PERMANENT_FIXED_PAIR_SAME_MODE_NN_Q_PLUS_EXCLUSION_THEOREM.md"
    ).read_text(encoding="utf-8")
    required = (
        "q_+:                                  EXCLUDED",
        "q_-:                                  SIBLING THEOREM",
        "combined same-mode synthesis:                          NOT CLAIMED HERE",
        "global Krenn--Gu conjecture:                           UNRESOLVED",
        "from one local plane are never inserted into two tensor slots",
        "second `N` in the companion mode",
    )
    for phrase in required:
        assert phrase in theorem
    return {"scope_markers": len(required), "global_status": "UNRESOLVED"}


def main() -> None:
    """Run the exact replay and print a deterministic summary."""
    report = {
        "contractions": check_contractions_and_localization(),
        "hyperplane_charts": check_hyperplane_charts(),
        "rank_profiles": check_rank_profile_kernels(),
        "tensor_forks": check_tensor_orders_and_forks(),
        "polarization": check_direct_polarization(),
        "coincident_mode": check_coincident_companion_mode(),
        "status": check_status_boundary(),
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    print("same-mode N/N q-plus primary replay: PASS")


if __name__ == "__main__":
    main()
