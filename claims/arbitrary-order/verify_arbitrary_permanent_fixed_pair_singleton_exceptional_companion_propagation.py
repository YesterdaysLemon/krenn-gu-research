"""Exact checks for fixed-pair singleton-exceptional propagation."""

from __future__ import annotations

import json

import sympy as sp


def contraction(quadratic: sp.Expr, vector: tuple[sp.Expr, ...]) -> sp.Matrix:
    """Contract a square-free quadratic and return its residual covector."""
    return sp.Matrix([
        sp.expand(sum(vector[i] * sp.diff(quadratic, VARIABLES[i]) for i in range(4)))
        .coeff(VARIABLES[j])
        for j in range(4)
    ])


def same_space(columns: list[sp.Matrix], expected: list[sp.Matrix]) -> bool:
    """Test equality of two column spans."""
    left = sp.Matrix.hstack(*columns)
    right = sp.Matrix.hstack(*expected)
    return left.rank() == right.rank() == sp.Matrix.hstack(left, right).rank()


def common_kernel(rows: list[sp.Matrix]) -> list[sp.Matrix]:
    """Return a basis of the common kernel of residual covectors."""
    return sp.Matrix.vstack(*(row.T for row in rows)).nullspace()


x0, x1, x2, x3 = VARIABLES = sp.symbols("x0:4")
QUADRATICS = {
    "m1": x1 * (x3 - x2 - x0),
    "m2": x0 * (x3 - x2 - x1),
    "d0": (x1 + x2) * (x3 - x0),
    "d1": (x0 + x2) * (x3 - x1),
    "d2": -2 * x0 * x1,
}

VECTORS = {
    "N": sp.Matrix((0, 0, 1, 1)),
    "A0": sp.Matrix((1, 0, 0, 1)),
    "C0": sp.Matrix((1, 0, -1, 0)),
    "A1": sp.Matrix((0, 1, 0, 1)),
    "C1": sp.Matrix((0, 1, -1, 0)),
    "U0": sp.Matrix((1, 0, 0, -1)),
    "V1": sp.Matrix((1, 0, 1, 0)),
    "U1": sp.Matrix((0, 1, 0, -1)),
    "V0": sp.Matrix((0, 1, 1, 0)),
}


def residuals(vector: sp.Matrix) -> dict[str, sp.Matrix]:
    """Return all five residual covectors after contraction by vector."""
    values = tuple(vector)
    return {name: contraction(quadratic, values) for name, quadratic in QUADRATICS.items()}


def check_exceptional_table() -> dict[str, object]:
    """Check the six residual spans and common kernels."""
    h0 = sp.Matrix((-1, 1, 1, 1))
    h1 = sp.Matrix((1, -1, 1, 1))
    h2 = sp.Matrix((1, -1, -1, 1))
    h2p = sp.Matrix((-1, 1, -1, 1))
    e0 = sp.Matrix((1, 0, 0, 0))
    e1 = sp.Matrix((0, 1, 0, 0))
    s = sp.Matrix((1, 1, 0, 0))
    t = sp.Matrix((0, 0, 1, -1))

    cases = {
        "Phi1_N": ("N", [h0, h1], [s, t]),
        "Phi1_A0": ("A0", [h2, h1, e1], [VECTORS["U0"]]),
        "Phi1_C0": ("C0", [h2, h0, e1], [VECTORS["V1"]]),
        "Phi2_N": ("N", [h0, h1], [s, t]),
        "Phi2_A1": ("A1", [h2p, h0, e0], [VECTORS["U1"]]),
        "Phi2_C1": ("C1", [h2p, h1, e0], [VECTORS["V0"]]),
    }
    selected_channels = {
        "Phi1_N": ("d0", "d1"),
        "Phi1_A0": ("m2", "d1", "d2"),
        "Phi1_C0": ("m2", "d0", "d2"),
        "Phi2_N": ("d0", "d1"),
        "Phi2_A1": ("m1", "d0", "d2"),
        "Phi2_C1": ("m1", "d1", "d2"),
    }

    report: dict[str, object] = {}
    for label, (vector_name, expected_rows, expected_kernel) in cases.items():
        values = residuals(VECTORS[vector_name])
        rows = [values[name] for name in selected_channels[label]]
        assert same_space(rows, expected_rows), label
        kernel = common_kernel(rows)
        assert same_space(kernel, expected_kernel), label
        report[label] = {
            "residual_rank": sp.Matrix.hstack(*rows).rank(),
            "kernel_dimension": len(kernel),
        }
    return report


def check_forced_companion_colours() -> dict[str, object]:
    """Check the mixed/diagonal contraction identities forcing colours."""
    identities = {
        "U0_colour_0": (("m1", "d2"), ("m2", "d1")),
        "V1_colour_1": (("m1", "d2"), ("m2", "d0")),
        "U1_colour_1": (("m2", "d2"), ("m1", "d0")),
        "V0_colour_0": (("m2", "d2"), ("m1", "d1")),
    }
    report: dict[str, object] = {}
    for label, pairs in identities.items():
        vector_name = label.split("_colour_")[0]
        values = residuals(VECTORS[vector_name])
        for left, right in pairs:
            assert values[left] == values[right], (label, left, right)
            assert values[left] != sp.zeros(4, 1)
        report[label] = [f"{left}={right}" for left, right in pairs]
    return report


def check_common_line_plane() -> dict[str, object]:
    """Check the forced colour and return kernels for the N companion plane."""
    s, t = sp.symbols("s t")
    q = sp.Matrix((s, s, t, -t))
    values = residuals(q)
    ell = sp.Matrix((-1, -1, -1, 1))
    assert values["m1"] == s * ell - 2 * t * sp.Matrix((0, 1, 0, 0))
    assert values["m2"] == s * ell - 2 * t * sp.Matrix((1, 0, 0, 0))
    assert values["d0"] == values["d1"] == (s + t) * ell
    assert values["d2"] == -2 * s * sp.Matrix((1, 1, 0, 0))

    generic = [row.subs({s: 2, t: 3}) for row in values.values()]
    boundary = [row.subs({s: 1, t: 0}) for row in values.values()]
    assert sp.Matrix.hstack(*generic).rank() == 3
    assert same_space(common_kernel(generic), [VECTORS["N"]])
    boundary_kernel = [VECTORS["N"], sp.Matrix((1, -1, 0, 0))]
    assert sp.Matrix.hstack(*boundary).rank() == 2
    assert same_space(common_kernel(boundary), boundary_kernel)
    return {
        "d0_equals_d1": True,
        "forced_colour": 2,
        "forced_nonzero_parameter": "s",
        "generic_return_kernel": "K*N",
        "t_zero_return_kernel": "span{N,x0-x1}",
    }


def check_return_cycles() -> dict[str, object]:
    """Check that the four line companions return to their source lines."""
    cycles = {
        "U0": "A0",
        "V1": "C0",
        "U1": "A1",
        "V0": "C1",
    }
    report: dict[str, object] = {}
    for companion, source in cycles.items():
        rows = [row for row in residuals(VECTORS[companion]).values() if row != sp.zeros(4, 1)]
        rank = sp.Matrix.hstack(*rows).rank()
        kernel = common_kernel(rows)
        assert rank == 3
        assert same_space(kernel, [VECTORS[source]])
        report[companion] = source
    return report


def check_rank_gap_core() -> dict[str, object]:
    """Replay the dimension and orthogonal-line core of Lemma 1."""
    scalar = sp.symbols("j", nonzero=True)
    for dimension in (2, 3):
        identity = scalar * sp.eye(dimension)
        assert identity.rank() == dimension
        assert sp.factor(identity.det()) == scalar**dimension

    a0, a1 = sp.symbols("a0 a1")
    hyperbolic = sp.Matrix(((0, 1), (1, 0)))
    vector = sp.Matrix((a0, a1))
    orthogonal = sp.Matrix((a0, -a1))
    assert (vector.T * hyperbolic * orthogonal)[0] == 0
    assert sp.Matrix.hstack(orthogonal, 7 * orthogonal).rank() == 1
    return {
        "quotient_dimensions_checked": [2, 3],
        "rank_gap": "d versus at most d-1",
        "orthogonal_complement_dimension": 1,
    }


def main() -> None:
    """Run the deterministic exact replay."""
    report = {
        "exceptional_cases": check_exceptional_table(),
        "forced_companion_colours": check_forced_companion_colours(),
        "common_line_plane": check_common_line_plane(),
        "return_cycles": check_return_cycles(),
        "rank_gap_core": check_rank_gap_core(),
        "scope": "exact identity replay; written characteristic-zero proof",
        "status": "PASS",
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
