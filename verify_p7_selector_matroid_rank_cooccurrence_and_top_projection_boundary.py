"""Primary symbolic replay for the P7 selector-matroid boundary."""

from __future__ import annotations

from itertools import combinations

import sympy as sp


def permanent_dp(matrix: sp.Matrix) -> sp.Expr:
    rows, cols = matrix.shape
    assert rows == cols
    states: dict[int, sp.Expr] = {0: sp.Integer(1)}
    for row in range(rows):
        nxt: dict[int, sp.Expr] = {}
        for mask, value in states.items():
            for col in range(cols):
                if mask & (1 << col) == 0:
                    new_mask = mask | (1 << col)
                    nxt[new_mask] = nxt.get(new_mask, 0) + value * matrix[row, col]
        states = nxt
    return sp.expand(states[(1 << cols) - 1])


def submatrix(
    matrix: sp.Matrix, rows: tuple[int, ...], cols: tuple[int, ...]
) -> sp.Matrix:
    return sp.Matrix([[matrix[row, col] for col in cols] for row in rows])


def check_pair_selector_matroid() -> None:
    incidence = sp.Matrix(
        [
            [1, 1, 1, 0, 0, 0],
            [1, 0, 0, 1, 1, 0],
            [0, 1, 0, 1, 0, 1],
            [0, 0, 1, 0, 1, 1],
        ]
    )
    assert incidence.rank() == 4
    s, t = sp.symbols("s t")
    kernel = sp.Matrix([-s - t, s, t, t, s, -s - t])
    assert incidence * kernel == sp.zeros(4, 1)

    b = sp.symbols("b12 b13 b14 b23 b24 b34")
    row = sp.Matrix(1, 6, b)
    basis = sp.Matrix.hstack(
        sp.Matrix([-1, 1, 0, 0, 1, -1]),
        sp.Matrix([-1, 0, 1, 1, 0, -1]),
    )
    assert row * basis == sp.Matrix(
        [[-b[0] + b[1] + b[4] - b[5], -b[0] + b[2] + b[3] - b[5]]]
    )

    lam = sp.symbols("lambda")
    residual_a = sp.Matrix([lam, -lam, 0, 0])
    residual_b = sp.Matrix([0, 0, 1, -1])
    pair_response = []
    for i, j in combinations(range(4), 2):
        pair_response.append(
            residual_a[i] * residual_b[j] + residual_b[i] * residual_a[j]
        )
    pair_vector = sp.Matrix(pair_response)
    assert pair_vector == sp.Matrix([0, lam, -lam, -lam, lam, 0])
    assert incidence * pair_vector == sp.zeros(4, 1)

    for port_count in (5, 6):
        pairs = list(combinations(range(port_count), 2))
        rows = []
        for window in combinations(range(port_count), 4):
            window_set = set(window)
            for vertex in window:
                rows.append(
                    [
                        int(vertex in edge and set(edge).issubset(window_set))
                        for edge in pairs
                    ]
                )
        global_observation = sp.Matrix(rows)
        assert global_observation.rank() == len(pairs)


def canonical_matrices() -> list[sp.Matrix]:
    return [
        sp.Matrix(
            [
                [-1, 1, 0, 0, 0],
                [0, 0, 1, 0, 0],
                [-1, 0, 0, 1, 0],
                [0, 0, 0, 0, 1],
                [1, 1, 0, 1, 0],
            ]
        ),
        sp.Matrix(
            [
                [0, 1, 0, 0, 0],
                [-1, 0, 1, 0, 0],
                [0, 0, 0, 1, 0],
                [-1, 0, 0, 0, 1],
                [1, 0, 1, 0, 1],
            ]
        ),
        sp.Matrix(
            [
                [-1, 1, 0, 0, 0],
                [-1, 0, 1, 0, 0],
                [-1, 0, 0, 1, 0],
                [1, 0, 0, 0, 1],
                [1, 1, 0, 1, 0],
            ]
        ),
    ]


def marked_shore_products(matrix: sp.Matrix, pair: tuple[int, int]) -> list[sp.Expr]:
    roots = tuple(range(5))
    cols = tuple(range(5))
    other_roots = tuple(root for root in roots if root not in pair)
    products = []
    for shore in combinations(cols, 3):
        if 0 not in shore:
            continue
        complement = tuple(col for col in cols if col not in shore)
        products.append(
            sp.expand(
                permanent_dp(submatrix(matrix, other_roots, shore))
                * permanent_dp(submatrix(matrix, pair, complement))
            )
        )
    return products


def check_rank_cooccurrence_countermodel() -> None:
    matrices = canonical_matrices()
    for matrix in matrices:
        assert permanent_dp(matrix) == -1
        pure_p7 = sp.diag(matrix, sp.eye(2))
        assert permanent_dp(pure_p7) == -1
        assert all(value == 0 for value in marked_shore_products(matrix, (0, 1)))
        assert all(value == 0 for value in marked_shore_products(matrix, (2, 3)))
        bad_pair_values = [
            value
            for pair in combinations(range(5), 2)
            if pair not in {(0, 1), (2, 3)}
            for value in marked_shore_products(matrix, pair)
        ]
        assert any(value != 0 for value in bad_pair_values)

    h0, h1, h2 = matrices
    blocker_rows: dict[str, list[list[sp.Expr]]] = {}
    blocker_rows["t"] = [[h0[i, 0], h1[i, 0], h2[i, 0]] for i in range(5)]
    blocker_rows["u01"] = [[h0[i, 1], h1[i, 3], 0] for i in range(5)]
    blocker_rows["v01"] = [[h0[i, 2], h1[i, 4], 0] for i in range(5)]
    blocker_rows["u02"] = [[h0[i, 3], 0, h2[i, 1]] for i in range(5)]
    blocker_rows["v02"] = [[h0[i, 4], 0, h2[i, 2]] for i in range(5)]
    blocker_rows["u12"] = [[0, h1[i, 1], h2[i, 3]] for i in range(5)]
    blocker_rows["v12"] = [[0, h1[i, 2], h2[i, 4]] for i in range(5)]
    assert sp.Matrix(blocker_rows["t"]).rank() == 3
    for name in ("u01", "v01", "u02", "v02", "u12", "v12"):
        assert sp.Matrix(blocker_rows[name]).rank() == 2
    assert all(row[2] == 0 for name in ("u01", "v01") for row in blocker_rows[name])
    assert all(row[1] == 0 for name in ("u02", "v02") for row in blocker_rows[name])
    assert all(row[0] == 0 for name in ("u12", "v12") for row in blocker_rows[name])


def marked_sum(matrix: sp.Matrix, pair: tuple[int, int]) -> sp.Expr:
    return sp.expand(sum(marked_shore_products(matrix, pair), sp.Integer(0)))


def check_balanced_weighted_laplace() -> None:
    symbols = sp.symbols("h0:25")
    matrix = sp.Matrix(5, 5, symbols)
    # Unit weights on the five-cycle have common weighted degree d=2.
    cycle = ((0, 1), (1, 2), (2, 3), (3, 4), (0, 4))
    weighted = sp.expand(sum((marked_sum(matrix, pair) for pair in cycle), sp.Integer(0)))
    assert sp.Poly(weighted - 3 * permanent_dp(matrix), *symbols).is_zero


def check_pure_cofactor_isolation() -> None:
    full = sp.zeros(5, 7)
    for i in range(5):
        full[i, i + 2] = 1
    cofactors: dict[tuple[int, int], sp.Expr] = {}
    for omitted in combinations(range(7), 2):
        retained = tuple(col for col in range(7) if col not in omitted)
        cofactors[omitted] = permanent_dp(submatrix(full, tuple(range(5)), retained))
    assert cofactors[(0, 1)] == 1
    assert all(value == 0 for pair, value in cofactors.items() if pair != (0, 1))


def check_six_window_dominance() -> None:
    gamma = sp.symbols("gamma", nonzero=True)
    m34, m35, m36, m45, m46, m56 = sp.symbols(
        "m34 m35 m36 m45 m46 m56", nonzero=True
    )
    nu34, nu35, nu36, nu45, nu46, nu56 = sp.symbols(
        "nu34 nu35 nu36 nu45 nu46 nu56"
    )
    m = {
        (3, 4): m34,
        (3, 5): m35,
        (3, 6): m36,
        (4, 5): m45,
        (4, 6): m46,
        (5, 6): m56,
    }
    nu = {
        (3, 4): nu34,
        (3, 5): nu35,
        (3, 6): nu36,
        (4, 5): nu45,
        (4, 6): nu46,
        (5, 6): nu56,
    }
    u: dict[int, sp.Expr] = {3: sp.Integer(1)}
    v: dict[int, sp.Expr] = {3: sp.Integer(0), 4: m34, 5: m35, 6: m36}
    system = sp.Matrix([[v[5], v[4], 0], [v[6], 0, v[4]], [0, v[6], v[5]]])
    assert sp.factor(system.det()) == -2 * m34 * m35 * m36
    solution = system.inv() * sp.Matrix([m45, m46, m56])
    u.update({4: solution[0], 5: solution[1], 6: solution[2]})
    for pair in combinations(range(3, 7), 2):
        direct_top = sp.factor(u[pair[0]] * v[pair[1]] + u[pair[1]] * v[pair[0]])
        assert sp.factor(direct_top - m[pair]) == 0
        tail_edge = (nu[pair] - m[pair]) / gamma
        residual_top = sp.factor(direct_top + gamma * tail_edge)
        assert sp.factor(residual_top - nu[pair]) == 0


def main() -> None:
    check_pair_selector_matroid()
    check_rank_cooccurrence_countermodel()
    check_balanced_weighted_laplace()
    check_pure_cofactor_isolation()
    check_six_window_dominance()
    print("PASS: selector-matroid ranks, defect signatures, and legal kernel family")
    print("PASS: simultaneous canonical pure-P7 rank-cooccurrence countermodel")
    print("PASS: generic balanced marked-Laplace identity")
    print("PASS: six-window top-projection rational dominance")
    print("SCOPE: mixed-colour P7 and global Krenn-Gu remain UNRESOLVED")


if __name__ == "__main__":
    main()
