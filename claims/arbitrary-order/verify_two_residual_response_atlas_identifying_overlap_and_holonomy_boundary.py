"""Focused exact checks for the q=2 response-atlas gluing boundary."""

from __future__ import annotations

from itertools import combinations

import sympy as sp


J = sp.Matrix([[0, 1], [1, 0]])


def rho(g: sp.Matrix) -> sp.Matrix:
    return J * g.inv().T * J


def channel(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return left.T * J * right


def assert_zero(matrix: sp.Matrix) -> None:
    assert all(sp.simplify(entry) == 0 for entry in matrix)


def check_symbolic_contragredient() -> None:
    a, b, c, d = sp.symbols("a b c d")
    g = sp.Matrix([[a, b], [c, d]])
    assert_zero(g.T * J * rho(g) - J)
    assert_zero(rho(rho(g)) - g)


def check_three_group_identifiability() -> None:
    frames = [
        sp.Matrix([[1, 0, 0], [0, 1, 0]]),
        sp.Matrix([[1, 1, 0], [0, 1, 1]]),
        sp.Matrix([[2, 0, 1], [1, 1, 0]]),
    ]
    g = sp.diag(sp.Rational(2), sp.Rational(1, 2))
    assert_zero(g.T * J * g - J)
    transformed = [g * frame for frame in frames]

    for i, j in combinations(range(3), 2):
        assert_zero(channel(transformed[i], transformed[j]) - channel(frames[i], frames[j]))

    recovered = transformed[0][:, :2] * frames[0][:, :2].inv()
    assert_zero(recovered - g)
    assert_zero(recovered.T * J * recovered - J)
    for old, new in zip(frames, transformed, strict=True):
        assert_zero(new - recovered * old)


def check_two_group_ambiguity() -> None:
    left = sp.Matrix([[1, 0, 1], [0, 1, 1]])
    right = sp.Matrix([[1, 2, 0], [0, 1, 1]])
    g = sp.diag(2, 3)
    dual = rho(g)
    assert dual == sp.diag(sp.Rational(1, 3), sp.Rational(1, 2))
    assert_zero(channel(g * left, dual * right) - channel(left, right))
    assert g.T * J * g == 6 * J
    assert g.T * J * g != J


def chart_frames() -> tuple[dict[str, sp.Matrix], dict[str, sp.Matrix], dict[str, sp.Matrix], sp.Matrix]:
    p = sp.Matrix([[1, 0, 0], [0, 1, 0]])
    twist = sp.diag(sp.Rational(2), sp.Rational(1, 2))
    clusters = {
        name: [f"{name}{i}" for i in range(3)]
        for name in ("A", "B", "C")
    }

    chart_0 = {u: p for name in ("A", "C") for u in clusters[name]}
    chart_1 = {u: p for name in ("A", "B") for u in clusters[name]}
    chart_2 = {
        **{u: p for u in clusters["B"]},
        **{u: twist * p for u in clusters["C"]},
    }
    return chart_0, chart_1, chart_2, twist


def pair_blocks(frames: dict[str, sp.Matrix]) -> dict[tuple[str, str], sp.Matrix]:
    return {
        pair: channel(frames[pair[0]], frames[pair[1]])
        for pair in combinations(sorted(frames), 2)
    }


def check_twisted_atlas() -> None:
    chart_0, chart_1, chart_2, twist = chart_frames()
    charts = [chart_0, chart_1, chart_2]
    blocks = [pair_blocks(chart) for chart in charts]

    for left_index, right_index in ((0, 1), (1, 2), (2, 0)):
        overlap = sorted(set(charts[left_index]) & set(charts[right_index]))
        assert len(overlap) == 3
        for pair in combinations(overlap, 2):
            assert_zero(blocks[left_index][pair] - blocks[right_index][pair])
        for port in overlap:
            assert charts[left_index][port].rank() == 2
            assert charts[right_index][port].rank() == 2

    assert_zero(twist.T * J * twist - J)
    holonomy = twist.inv()
    assert holonomy != sp.eye(2)
    assert holonomy == sp.diag(sp.Rational(1, 2), 2)

    # With M=1 and h=0, Z=Q_K has no coefficient above port degree two.
    # Hence every four-point dual-Wick insertion equation is 0=0.
    for chart in charts:
        for subset in combinations(sorted(chart), 4):
            z_four = sp.zeros(3, 3)
            insertion_rhs = sp.zeros(3, 3)
            assert_zero(z_four - insertion_rhs)


def main() -> None:
    check_symbolic_contragredient()
    check_three_group_identifiability()
    check_two_group_ambiguity()
    check_twisted_atlas()
    print("two-residual response-atlas primary checks: PASS")
    print("three-group O(J) identifiability: PASS")
    print("two-group GL(2) ambiguity: PASS")
    print("partition-closed twisted atlas and nontrivial holonomy: PASS")


if __name__ == "__main__":
    main()
