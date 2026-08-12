"""Exact replay of the S2O binary pullback reduction."""

from __future__ import annotations

from itertools import permutations

import sympy as sp

Word = tuple[int, int, int]
Tensor = dict[Word, sp.Expr]


def add_entry(tensor: Tensor, word: Word, value: sp.Expr) -> None:
    """Add one sparse tensor coefficient."""
    value = sp.expand(value)
    tensor[word] = sp.expand(tensor.get(word, sp.Integer(0)) + value)
    if tensor[word] == 0:
        del tensor[word]


def project_nonzero_colours(tensor: Tensor, a: int) -> Tensor:
    """Kill every root word containing colour zero."""
    q = 3 - a
    allowed = {a, q}
    return {word: value for word, value in tensor.items() if set(word) <= allowed}


def empty_and_singletons(
    kind: str, a: int, b: int | None
) -> tuple[Tensor, dict[tuple[str, int], Tensor]]:
    """Reconstruct the coefficient tensors of one displayed S2M control."""
    x = sp.symbols("x0:3")
    y = sp.symbols("y0:3")
    r = sp.symbols("r0:3")
    empty: Tensor = {(c, c, c): x[c] * y[c] * r[c] for c in range(3)}
    singletons: dict[tuple[str, int], Tensor] = {
        (u, c): {} for u in ("x", "y", "r") for c in range(3)
    }

    if kind == "outside":
        assert b is None
        empty.pop((a, a, a))
        add_entry(empty, (0, 0, 1), x[a] * y[a] * r[a])
        add_entry(singletons[("r", 0)], (a, a, a), 1)
        add_entry(singletons[("r", 0)], (0, 0, 1), -1)
        add_entry(singletons[("y", 0)], (0, 1, 0), 1)
        add_entry(singletons[("x", 0)], (1, 0, 0), 1)
    elif kind == "x":
        assert b is not None
        empty.pop((a, a, a))
        add_entry(singletons[("r", a)], (0, 0, 1), 1)
        add_entry(singletons[("x", b)], (0, 0, 1), -1)
        add_entry(singletons[("x", 0)], (a, a, a), 1)
        add_entry(singletons[("y", 0)], (0, 1, 0), 1)
    elif kind == "y":
        assert b is not None
        empty.pop((a, a, a))
        add_entry(singletons[("r", a)], (0, 0, 1), 1)
        add_entry(singletons[("y", b)], (0, 0, 1), -1)
        add_entry(singletons[("y", 0)], (a, a, a), 1)
        add_entry(singletons[("x", 0)], (0, 1, 0), 1)
    else:  # pragma: no cover - internal caller fixes the three cases
        raise ValueError(kind)
    return empty, singletons


def permanent(matrix: list[list[sp.Expr]]) -> sp.Expr:
    """Ordinary sign-free 3 by 3 permanent."""
    return sp.expand(
        sum(
            (
                matrix[0][sigma[0]] * matrix[1][sigma[1]] * matrix[2][sigma[2]]
                for sigma in permutations(range(3))
            ),
            sp.Integer(0),
        )
    )


def main() -> None:
    """Check all eight pullbacks and the sharp false-inference boundary."""
    controls = [("outside", a, None) for a in (1, 2)]
    controls += [
        (kind, a, b) for kind in ("x", "y") for a, b in ((1, 1), (1, 2), (2, 2))
    ]

    for kind, a, b in controls:
        q = 3 - a
        empty, singletons = empty_and_singletons(kind, a, b)
        projected_empty = project_nonzero_colours(empty, a)
        projected_singletons = {
            key: project_nonzero_colours(value, a) for key, value in singletons.items()
        }
        projected_singletons = {
            key: value for key, value in projected_singletons.items() if value
        }

        assert projected_singletons == {
            next(iter(projected_singletons)): {(a, a, a): 1}
        }
        assert projected_empty == {
            (q, q, q): sp.symbols(f"x{q}") * sp.symbols(f"y{q}") * sp.symbols(f"r{q}")
        }
        assert all(
            not project_nonzero_colours(singletons[(u, q)], a) for u in ("x", "y", "r")
        )

    # Sharpness for the rejected shortcut: all three columns lie in
    # u_1+u_2+u_3=0, yet their permanent is nonzero.
    rows = [
        [sp.Integer(0), sp.Integer(3), sp.Integer(3)],
        [sp.Integer(1), sp.Integer(3), sp.Integer(2)],
        [sp.Integer(-1), sp.Integer(-6), sp.Integer(-5)],
    ]
    assert all(sum(rows[i][j] for i in range(3)) == 0 for j in range(3))
    assert permanent(rows) == -48

    print("S2O exact binary pullback: PASS (8/8)")
    print("binary syzygy-permanent residual: OPEN")
    print("zero-singleton-implies-zero-empty shortcut: REFUTED")
    print("global Krenn-Gu status: UNRESOLVED")


if __name__ == "__main__":
    main()
