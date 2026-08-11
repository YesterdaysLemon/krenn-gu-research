"""Verify the projectively constant single-open permanent lift."""

from __future__ import annotations

from functools import cache
from itertools import permutations
from math import factorial

import sympy as sp


def permanent(matrix: list[list[sp.Expr]]) -> sp.Expr:
    """Return the permanent by a direct labelled-row expansion."""
    size = len(matrix)
    return sp.Add(
        *(
            sp.prod(matrix[row][assignment[row]] for row in range(size))
            for assignment in permutations(range(size))
        )
    )


def matching_sum(
    vertices: tuple[int, ...], edge: dict[tuple[int, int], sp.Expr]
) -> sp.Expr:
    """Return the perfect-matching polynomial on a labelled graph."""

    @cache
    def recurse(remaining: tuple[int, ...]) -> sp.Expr:
        if not remaining:
            return sp.Integer(1)
        first = remaining[0]
        terms = []
        for offset in range(1, len(remaining)):
            second = remaining[offset]
            rest = remaining[1:offset] + remaining[offset + 1 :]
            terms.append(edge[tuple(sorted((first, second)))] * recurse(rest))
        return sp.Add(*terms)

    return recurse(vertices)


def symbolic_case(r: int, q: int) -> None:
    """Check the graph, Laplace sectors, and contraction for one cell."""
    m = r + 2 * q
    root_j = 0
    roots = tuple(range(r))
    pinned = tuple(root for root in roots if root != root_j)
    outside = tuple(range(r, r + m))
    vertices = roots + outside

    eta = sp.Symbol("eta")
    ell = {root: sp.Symbol(f"ell_{root}") for root in pinned}
    a = {mode: sp.Symbol(f"a_{mode-r}") for mode in outside}
    b = {mode: sp.Symbol(f"b_{mode-r}") for mode in outside}
    h = {
        (root, mode): sp.Symbol(f"h_{root}_{mode-r}")
        for root in pinned
        for mode in outside
    }

    edge: dict[tuple[int, int], sp.Expr] = {}
    for first in vertices:
        for second in vertices:
            if first >= second:
                continue
            pair = (first, second)
            if first == root_j and second in pinned:
                edge[pair] = ell[second]
            elif first == root_j and second in outside:
                edge[pair] = eta * b[second]
            elif first in pinned and second in pinned:
                edge[pair] = sp.Integer(0)
            elif first in pinned and second in outside:
                edge[pair] = h[(first, second)]
            else:
                edge[pair] = a[first] * b[second] + b[first] * a[second]

    graph = matching_sum(vertices, edge)

    new_rows: list[list[sp.Expr]] = []
    for root in pinned:
        new_rows.append([ell[root], *(h[(root, mode)] for mode in outside)])
    for _ in range(q + 1):
        new_rows.append([eta, *(a[mode] for mode in outside)])
    for _ in range(q + 1):
        new_rows.append([sp.Integer(0), *(b[mode] for mode in outside)])
    assert len(new_rows) == m + 1
    lifted = permanent(new_rows)
    assert sp.expand(lifted - factorial(q + 1) * graph) == 0

    fixed_rows: list[list[sp.Expr]] = []
    for root in pinned:
        fixed_rows.append([h[(root, mode)] for mode in outside])
    for _ in range(q):
        fixed_rows.append([a[mode] for mode in outside])
    for _ in range(q + 1):
        fixed_rows.append([b[mode] for mode in outside])
    assert len(fixed_rows) == m
    fixed_permanent = permanent(fixed_rows)

    outside_sector = sp.Integer(0)
    companion_sector = {root: sp.Integer(0) for root in pinned}
    for partner in vertices[1:]:
        rest = tuple(vertex for vertex in vertices if vertex not in (0, partner))
        term = edge[(0, partner)] * matching_sum(rest, edge)
        if partner in outside:
            outside_sector += term
        else:
            companion_sector[partner] += term

    assert sp.expand(
        factorial(q) * outside_sector - eta * fixed_permanent
    ) == 0

    laplace = outside_sector
    for root in pinned:
        companion_rows: list[list[sp.Expr]] = []
        for other in pinned:
            if other != root:
                companion_rows.append([h[(other, mode)] for mode in outside])
        for _ in range(q + 1):
            companion_rows.append([a[mode] for mode in outside])
        for _ in range(q + 1):
            companion_rows.append([b[mode] for mode in outside])
        assert len(companion_rows) == m
        companion_permanent = permanent(companion_rows)
        assert sp.expand(
            factorial(q + 1) * companion_sector[root]
            - ell[root] * companion_permanent
        ) == 0
        laplace += companion_sector[root]

    assert sp.expand(graph - laplace) == 0
    contraction = lifted.subs({eta: 1, **{value: 0 for value in ell.values()}})
    assert sp.expand(contraction - (q + 1) * fixed_permanent) == 0


def check_companion_frame() -> None:
    """Audit the exact rank-two quotient-frame linear algebra."""
    root = sp.Matrix((1, 2, 3))
    eta = sp.Matrix(((1, 0, 0),))
    companions = sp.Matrix(((-2, 1, 0), (-3, 0, 1)))
    diagonal = sp.diag(2, 3, 5)
    fixed = diagonal * root
    cofactor_columns = sp.Matrix(((0, 0), (3, 0), (0, 5)))

    assert eta * root == sp.Matrix(((1,),))
    assert companions * root == sp.zeros(2, 1)
    assert companions.rank() == 2
    assert diagonal == fixed * eta + cofactor_columns * companions

    kernel_eta = sp.Matrix(((0, 0), (1, 0), (0, 1)))
    effective = companions * kernel_eta
    assert effective == sp.eye(2)
    assert (cofactor_columns * effective).rank() == 2
    assert cofactor_columns.row_join(fixed).rank() == 3


def check_support_and_hall_arithmetic() -> None:
    """Check exact source-cell counting and the recovered Hall inequality."""
    for r in range(2, 11):
        for q in range(6):
            m = r + 2 * q
            order = m + 1
            assert (r - 1) + (q + 1) + (q + 1) == order
            assert 3 * (q + 1) <= m if r >= q + 3 else 3 * (q + 1) > m

            i_without_j = (r - 1) * max(0, m - 2)
            companion_count = min(r - 1, 2)
            p_a = max(0, m - 1)
            p_b = m
            formula = (
                i_without_j
                + companion_count
                + (q + 1) * (p_a + 1)
                + (q + 1) * p_b
            )

            row_supports = [max(0, m - 2)] * (r - 1)
            if companion_count:
                for index in range(companion_count):
                    row_supports[index] += 1
            row_supports.extend([p_a + 1] * (q + 1))
            row_supports.extend([p_b] * (q + 1))
            assert len(row_supports) == order
            assert sum(row_supports) == formula


def main() -> None:
    for r, q in ((2, 0), (3, 0), (2, 1), (3, 1)):
        symbolic_case(r, q)
        print(f"PASS: symbolic graph/permanent lift r={r} q={q}")

    check_companion_frame()
    check_support_and_hall_arithmetic()
    print("PASS: fixed P_m is the normalized x_j contraction of P_(m+1)")
    print("PASS: effective companion plane and diagonal quotient both have rank two")
    print("PASS: lifted source-cell ledger and r>=q+3 arithmetic")
    print("SCOPE: arbitrary-order proof is the written matching/Laplace bijection")
    print("SCOPE: two-open cross-depth transport and arbitrary P_M remain UNKNOWN")
    print("searches=0")


if __name__ == "__main__":
    main()
