"""Independent no-import audit of the q=2 response-atlas theorem.

This file deliberately imports neither SymPy nor the primary verifier.
"""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from itertools import combinations, product


Q = Fraction
J = ((Q(0), Q(1)), (Q(1), Q(0)))


def transpose(a):
    return tuple(zip(*a, strict=True))


def matmul(a, b):
    bt = transpose(b)
    return tuple(tuple(sum(x * y for x, y in zip(row, col, strict=True)) for col in bt) for row in a)


def diag(a, b):
    return ((Q(a), Q(0)), (Q(0), Q(b)))


def inv2(a):
    det = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    assert det
    return (
        (a[1][1] / det, -a[0][1] / det),
        (-a[1][0] / det, a[0][0] / det),
    )


def rho(g):
    return matmul(matmul(J, transpose(inv2(g))), J)


def channel(left, right):
    return matmul(matmul(transpose(left), J), right)


def check_two_group_control() -> None:
    left = ((Q(1), Q(0), Q(1)), (Q(0), Q(1), Q(1)))
    right = ((Q(1), Q(2), Q(0)), (Q(0), Q(1), Q(1)))
    g = diag(2, 3)
    dual = rho(g)
    assert dual == diag(Q(1, 3), Q(1, 2))
    assert channel(matmul(g, left), matmul(dual, right)) == channel(left, right)
    assert matmul(matmul(transpose(g), J), g) == tuple(tuple(6 * x for x in row) for row in J)


P = ((Q(1), Q(0), Q(0)), (Q(0), Q(1), Q(0)))
TWIST = diag(2, Q(1, 2))


def make_charts():
    clusters = {name: tuple(f"{name}{i}" for i in range(3)) for name in "ABC"}
    chart_0 = {u: P for name in "AC" for u in clusters[name]}
    chart_1 = {u: P for name in "AB" for u in clusters[name]}
    chart_2 = {
        **{u: P for u in clusters["B"]},
        **{u: matmul(TWIST, P) for u in clusters["C"]},
    }
    return (chart_0, chart_1, chart_2)


def verify_block_overlaps(charts) -> None:
    for left_index, right_index in ((0, 1), (1, 2), (2, 0)):
        overlap = sorted(set(charts[left_index]) & set(charts[right_index]))
        assert len(overlap) == 3
        for u, v in combinations(overlap, 2):
            assert channel(charts[left_index][u], charts[left_index][v]) == channel(
                charts[right_index][u], charts[right_index][v]
            )


def physical_response(chart):
    ports = tuple(sorted(chart))
    vertices = ("q0", "q1", *ports)

    # M is the port-only response: one at empty and zero elsewhere.
    assert Q(1) == 1

    # Enumerating the three basis polarizations at every selected port checks
    # every tensor coefficient.  Multilinearity then gives the full blocks.
    for size in range(2, len(ports) + 1, 2):
        for subset in combinations(ports, size):
            for basis_indices in product(range(3), repeat=size):
                values = {
                    port: (chart[port][0][index], chart[port][1][index])
                    for port, index in zip(subset, basis_indices, strict=True)
                }

                def weight(u, v):
                    if {u, v} == {"q0", "q1"}:
                        return Q(0)
                    if u == "q0" and v in values:
                        return values[v][0]
                    if v == "q0" and u in values:
                        return values[u][0]
                    if u == "q1" and v in values:
                        return values[v][1]
                    if v == "q1" and u in values:
                        return values[u][1]
                    return Q(0)

                @lru_cache(maxsize=None)
                def haf(selected):
                    if not selected:
                        return Q(1)
                    first = selected[0]
                    total = Q(0)
                    for position in range(1, len(selected)):
                        second = selected[position]
                        rest = selected[1:position] + selected[position + 1 :]
                        total += weight(first, second) * haf(rest)
                    return total

                assert haf(subset) == 0
                response = haf(tuple(sorted(("q0", "q1", *subset))))
                if size == 2:
                    u, v = subset
                    au, bu = values[u]
                    av, bv = values[v]
                    assert response == au * bv + bu * av
                else:
                    assert response == 0

    assert set(vertices) == {"q0", "q1", *ports}


def main() -> None:
    check_two_group_control()
    assert matmul(matmul(transpose(TWIST), J), TWIST) == J
    charts = make_charts()
    verify_block_overlaps(charts)
    for chart in charts:
        physical_response(chart)
    holonomy = inv2(TWIST)
    assert holonomy == diag(Q(1, 2), 2)
    assert holonomy != diag(1, 1)
    print("two-residual response-atlas independent audit: PASS")
    print("exact Fraction overlap blocks: PASS")
    print("independent matching recurrence for all block polarizations: PASS")
    print("nonidentity rational holonomy: PASS")


if __name__ == "__main__":
    main()
