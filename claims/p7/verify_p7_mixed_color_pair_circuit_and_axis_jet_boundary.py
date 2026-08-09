"""Primary symbolic replay for the mixed-colour P7 pair circuit."""

from __future__ import annotations

from itertools import combinations

import sympy as sp


def check_generic_pair_circuit() -> None:
    a_u = sp.Matrix(sp.symbols("au0:3"))
    b_u = sp.Matrix(sp.symbols("bu0:3"))
    a_v = sp.Matrix(sp.symbols("av0:3"))
    b_v = sp.Matrix(sp.symbols("bv0:3"))
    response = a_u * b_v.T + b_u * a_v.T
    assert sp.expand(response.det()) == 0

    sample = {
        **dict(zip(a_u, (1, 0, 1), strict=True)),
        **dict(zip(b_u, (0, 1, 1), strict=True)),
        **dict(zip(a_v, (1, 1, 0), strict=True)),
        **dict(zip(b_v, (1, -1, 1), strict=True)),
    }
    evaluated = response.subs(sample)
    assert evaluated.rank() == 2
    assert evaluated[:2, :2].det() != 0

    parameters = list(a_u) + list(b_u) + list(a_v) + list(b_v)
    jacobian = sp.Matrix(list(response)).jacobian(parameters)
    assert jacobian.subs(sample).rank() == 8


def check_coordinate_circuit_minimality() -> None:
    entries = sp.symbols("x0:9")
    matrix = sp.Matrix(3, 3, entries)
    determinant = sp.expand(matrix.det())
    assert determinant != 0
    for entry in entries:
        cofactor = sp.diff(determinant, entry)
        assert cofactor != 0
        assert entry not in cofactor.free_symbols


def check_diagonal_chart_interpolation() -> None:
    beta = sp.symbols("beta0:3")
    a_u = sp.symbols("a0:3")
    b_u = sp.symbols("b0:3")
    a_v = sp.symbols("c0:3")
    b_v = sp.symbols("d0:3")
    direct_block = sp.diag(*beta)
    residual_block = sp.Matrix(a_u) * sp.Matrix(b_v).T + sp.Matrix(b_u) * sp.Matrix(a_v).T
    assert [direct_block[i, i] for i in range(3)] == list(beta)
    assert [
        residual_block[i, i] for i in range(3)
    ] == [a_u[i] * b_v[i] + b_u[i] * a_v[i] for i in range(3)]

    outputs = sp.Matrix(
        list(beta) + [residual_block[i, i] for i in range(3)]
    )
    parameters = list(beta) + list(a_u) + list(b_u) + list(a_v) + list(b_v)
    specialization = {
        **dict(zip(a_u, (1, 1, 1), strict=True)),
        **dict(zip(b_u, (0, 0, 0), strict=True)),
        **dict(zip(a_v, (0, 0, 0), strict=True)),
        **dict(zip(b_v, (2, 3, 5), strict=True)),
    }
    assert outputs.jacobian(parameters).subs(specialization).rank() == 6


def check_pair_top_dominance() -> None:
    x, p, y, q = sp.symbols("x p y q")
    outputs = sp.Matrix([x, p, x * y, p * y + q * x])
    jacobian = outputs.jacobian([x, p, y, q])
    assert sp.factor(jacobian.det()) == x**2


def deletion_state_labels(axis_types: tuple[int, ...]) -> dict[frozenset[str], int]:
    roots = tuple(f"r{i}" for i in range(len(axis_types)))
    residuals = ("q0", "q1")
    assigned: dict[frozenset[str], int] = {}
    for size in range(1, len(roots) + 1):
        for indices in combinations(range(len(roots)), size):
            root_set = frozenset(roots[index] for index in indices)
            surviving = sorted(set(range(3)) - {axis_types[index] for index in indices})
            tags = (
                (frozenset(), frozenset(residuals))
                if size % 2 == 0
                else (frozenset({residuals[0]}), frozenset({residuals[1]}))
            )
            for color, tag in zip(surviving, tags, strict=False):
                label = root_set | tag
                assert label not in assigned
                assigned[label] = color
    return assigned


def check_axis_state_models() -> None:
    patterns = (
        (0, 0, 0, 0, 1),
        (0, 0, 0, 1, 2),
        (0, 0, 1, 1, 2),
    )
    for pattern in patterns:
        assigned = deletion_state_labels(pattern)
        assert assigned
        assert set(assigned.values()).issubset({0, 1, 2})
        for label in assigned:
            root_count = sum(name.startswith("r") for name in label)
            residual_count = sum(name.startswith("q") for name in label)
            assert root_count % 2 == residual_count % 2


def assert_matching_saturates(
    target: set[str], matching: tuple[tuple[str, str], ...]
) -> None:
    endpoints = [vertex for edge in matching for vertex in edge]
    assert len(endpoints) == len(set(endpoints))
    assert target.issubset(endpoints)


def check_axis_companion_topologies() -> None:
    global_matching = (("a1", "a2"), ("a3", "a4"), ("b", "q0"))
    assert_matching_saturates({"a1", "a2", "a3", "a4", "b"}, global_matching)

    shores_311 = (
        {"b", "c"},
        {"a1", "a2", "a3", "b"},
        {"a1", "a2", "a3", "c"},
    )
    matchings_311 = (
        (("b", "a1"), ("c", "a3")),
        (("b", "a1"), ("a2", "a3")),
        (("a1", "a2"), ("a3", "c")),
    )
    for shore, matching in zip(shores_311, matchings_311, strict=True):
        assert_matching_saturates(shore, matching)

    shores_221 = (
        {"b1", "b2", "c"},
        {"a1", "a2", "c"},
        {"a1", "a2", "b1", "b2"},
    )
    matchings_221 = (
        (("b1", "b2"), ("c", "a1")),
        (("a1", "a2"), ("c", "b1")),
        (("a1", "a2"), ("b1", "b2")),
    )
    for shore, matching in zip(shores_221, matchings_221, strict=True):
        assert_matching_saturates(shore, matching)


def main() -> None:
    check_generic_pair_circuit()
    check_coordinate_circuit_minimality()
    check_diagonal_chart_interpolation()
    check_pair_top_dominance()
    check_axis_state_models()
    check_axis_companion_topologies()
    print("PASS: generic mixed-colour corrected-pair determinant and rank")
    print("PASS: nine-coordinate circuit minimality")
    print("PASS: common-block diagonal-chart interpolation and dominance")
    print("PASS: exact all-axis deletion-state label compatibility")
    print("PASS: explicit singleton-axis companion-shore matchings")
    print("SCOPE: mixed-entry exposure, P7, and global Krenn-Gu remain UNRESOLVED")


if __name__ == "__main__":
    main()
