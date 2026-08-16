"""Primary exact replay for the co-two fixed-e=2 frame exclusion."""

from __future__ import annotations

from hashlib import sha256
from itertools import combinations
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
EDGES = tuple(combinations(range(4), 2))
CHANNELS = ("m1", "m2", "d0", "d1", "d2")

DEPENDENCIES = {
    "claims/arbitrary-order/"
    "ARBITRARY_PERMANENT_COTWO_R4_BASED_FRAME_ORBIT_CLASSIFICATION_THEOREM.md": (
        "CFF044EA8E89D504F4ECF9C62CA55DFD5361CD54F5CB85083B09AED8B834D677"
    ),
    "docs/audits/"
    "ARBITRARY_PERMANENT_COTWO_R4_BASED_FRAME_ORBIT_CLASSIFICATION_REVIEW_2026-08-15.md": (
        "F1610E9BBCC4065AC24A1E0CD7F81DDAF989BCA5D4026AE2A23BD2FF7A5F680F"
    ),
    "claims/arbitrary-order/"
    "ARBITRARY_PERMANENT_FIXED_PAIR_DIMENSION_FIVE_FULL_PROJECTION_BOUNDARY.md": (
        "727F39246FA64C899D1F51377FCB3C58640174C044510F727C796C888798F7C2"
    ),
    "docs/audits/"
    "ARBITRARY_PERMANENT_FIXED_PAIR_DIMENSION_FIVE_FULL_PROJECTION_BOUNDARY_REVIEW_2026-08-15.md": (
        "C3C31070155A975B115EEEFE59990E551169D54A9767298F2A13EDDE5992114F"
    ),
}

U = (
    (1, 1, -1, -1),
    (0, 1, 0, -1),
    (1, 0, 0, -1),
)
V = (
    (1, 1, 1, 1),
    (0, 1, 1, 0),
    (1, 0, 1, 0),
)

SOURCE = {
    "m1": (1, 1, 0, 0, -1, -1),
    "m2": (1, 0, -1, 1, 0, -1),
    "d0": (2, 0, 0, 0, 0, -2),
    "d1": (0, 0, 0, 1, -1, -1),
    "d2": (0, 1, -1, 0, 0, -1),
}

CORES = {
    "m1": (-1, -1, 0, 0, 1, 1),
    "m2": (-1, 0, 1, -1, 0, 1),
    "d0": (-2, 0, 0, 0, 0, 2),
    "d1": (-1, -1, 1, 0, 0, 0),
    "d2": (-1, 0, 0, -1, 1, 0),
}

LINES = {
    "A": (0, 1, -1, 0),
    "B": (1, 0, 0, 1),
    "C": (1, -1, 1, 1),
    "D": (0, 1, 0, 1),
    "E": (1, 0, -1, 0),
    "F": (1, -1, -1, -1),
    "N": (1, 1, -1, 1),
    "A'": (0, 1, 1, 0),
    "B'": (-1, 0, 0, 1),
    "C'": (1, 1, 0, 0),
    "D'": (0, -1, 0, 1),
    "E'": (1, 0, 1, 0),
    "G": (0, 0, 1, 1),
}


def lf_sha256(path: Path) -> str:
    """Hash text after normalizing checkout CRLF to Git-blob LF."""

    return sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest().upper()


def vector(values: tuple[int | sp.Expr, ...]) -> sp.Matrix:
    """Return an exact column vector."""

    return sp.Matrix(values)


def squarefree_product(
    left: tuple[int, ...], right: tuple[int, ...]
) -> tuple[sp.Expr, ...]:
    """Multiply two linear forms in the four-variable square-free algebra."""

    return tuple(
        sp.expand(left[i] * right[j] + left[j] * right[i]) for i, j in EDGES
    )


def edge_complement(coefficients: tuple[int | sp.Expr, ...]) -> tuple[sp.Expr, ...]:
    """Apply four-coordinate edge complementation."""

    lookup = {edge: coefficients[index] for index, edge in enumerate(EDGES)}
    vertices = frozenset(range(4))
    return tuple(
        sp.expand(lookup[tuple(sorted(vertices - frozenset(edge)))]) for edge in EDGES
    )


def contraction(
    core: tuple[int | sp.Expr, ...], point: tuple[int | sp.Expr, ...]
) -> sp.Matrix:
    """Contract one square-free quadratic core with a vector."""

    result: list[sp.Expr] = [sp.Integer(0)] * 4
    for coefficient, (left, right) in zip(core, EDGES, strict=True):
        result[right] += coefficient * point[left]
        result[left] += coefficient * point[right]
    return sp.Matrix([sp.expand(entry) for entry in result])


def contraction_matrix(point: tuple[int | sp.Expr, ...]) -> sp.Matrix:
    """Return the five contraction covectors in channel order."""

    return sp.Matrix.hstack(*(contraction(CORES[name], point) for name in CHANNELS))


def polynomial(core: tuple[int | sp.Expr, ...], xs: tuple[sp.Symbol, ...]) -> sp.Expr:
    """Return the ordinary square-free quadratic represented by a core."""

    return sp.expand(
        sum(coefficient * xs[i] * xs[j] for coefficient, (i, j) in zip(core, EDGES))
    )


def same_span(left: tuple[sp.Matrix, ...], right: tuple[sp.Matrix, ...]) -> bool:
    """Test equality of two exact column spaces."""

    left_matrix = sp.Matrix.hstack(*left)
    right_matrix = sp.Matrix.hstack(*right)
    joined = sp.Matrix.hstack(left_matrix, right_matrix)
    return joined.rank() == left_matrix.rank() == right_matrix.rank()


def relation(point: tuple[int, ...], coefficients: tuple[int, ...]) -> bool:
    """Check one exact relation among the five contraction columns."""

    return contraction_matrix(point) * vector(coefficients) == sp.zeros(4, 1)


def restricted_diagonal_rank(first: sp.Matrix, second: sp.Matrix) -> int:
    """Rank of the three diagonal quadratics on a codimension-two cell."""

    x = sp.symbols("x0:4")
    r, s = sp.symbols("r s")
    basis = sp.Matrix.vstack(first.T, second.T).nullspace()
    assert len(basis) == 2
    substitution = {
        x[index]: basis[0][index] * r + basis[1][index] * s for index in range(4)
    }
    rows = []
    for name in ("d0", "d1", "d2"):
        restricted = sp.Poly(
            sp.expand(polynomial(CORES[name], x).subs(substitution)), r, s
        )
        rows.append(
            (
                restricted.coeff_monomial(r**2),
                restricted.coeff_monomial(r * s),
                restricted.coeff_monomial(s**2),
            )
        )
    return sp.Matrix(rows).rank()


def verify_dependencies() -> None:
    """Pin the based-frame and hyperplane-product interfaces."""

    for relative, expected in DEPENDENCIES.items():
        actual = lf_sha256(ROOT / relative)
        assert actual == expected, (
            f"dependency hash mismatch for {relative}: expected {expected}, got {actual}"
        )


def verify_frame_and_cores() -> dict[str, int]:
    """Rebuild all products, complement cores, and mixed factorizations."""

    products = {
        (i, j): squarefree_product(U[i], V[j]) for i in range(3) for j in range(3)
    }
    mixed = sp.Matrix.hstack(
        *(vector(products[i, j]) for i in range(3) for j in range(3) if i != j)
    )
    full = sp.Matrix.hstack(*(vector(products[i, j]) for i in range(3) for j in range(3)))
    assert mixed.rank() == 2
    assert full.rank() == 5
    assert products[0, 1] == SOURCE["m1"]
    assert products[1, 0] == SOURCE["m2"]
    assert products[0, 0] == SOURCE["d0"]
    assert products[1, 1] == SOURCE["d1"]
    assert products[2, 2] == SOURCE["d2"]
    assert products[0, 2] == SOURCE["m2"]
    assert products[1, 2] == SOURCE["m2"]
    assert products[2, 0] == SOURCE["m1"]
    assert products[2, 1] == SOURCE["m1"]
    for name in CHANNELS:
        assert edge_complement(SOURCE[name]) == CORES[name]

    x = sp.symbols("x0:4")
    expected = {
        "m1": -(x[0] - x[3]) * (x[1] + x[2]),
        "m2": -(x[0] + x[2]) * (x[1] - x[3]),
        "d0": -2 * (x[0] * x[1] - x[2] * x[3]),
        "d1": -x[0] * (x[1] + x[2] - x[3]),
        "d2": -x[1] * (x[0] + x[2] - x[3]),
    }
    for name, factor in expected.items():
        assert sp.expand(polynomial(CORES[name], x) - factor) == 0
    return {"mixed_rank": mixed.rank(), "product_rank": full.rank()}


def verify_kernel_and_common_line() -> dict[str, object]:
    """Check generic determinants and remove the common support-three line."""

    r, s = sp.symbols("r s")
    p1 = (r, s, -s, r)
    p2 = (r, s, -r, s)
    first = sp.Matrix.hstack(
        *(contraction(CORES[name], p1) for name in ("m2", "d0", "d1", "d2"))
    )
    second = sp.Matrix.hstack(
        *(contraction(CORES[name], p2) for name in ("m1", "d0", "d1", "d2"))
    )
    expected = 8 * r * s * (r - s) * (r + s)
    assert sp.factor(first.det()) == expected
    assert sp.factor(second.det()) == -expected

    expected_ranks = {name: 3 for name in ("A", "B", "C", "D", "E", "F", "N")}
    for name, rank_value in expected_ranks.items():
        assert contraction_matrix(LINES[name]).rank() == rank_value

    assert relation(LINES["N"], (1, 0, 0, 0, 0))
    assert relation(LINES["N"], (0, 1, 0, 0, 0))
    actual = tuple(contraction_matrix(LINES["N"]).T.nullspace())
    assert same_span(actual, (vector(LINES["G"]),))
    for row in ((-1, -1, 1, 0, 0), (0, 0, 0, 1, 0), (0, 0, 0, 0, 1)):
        assert relation(LINES["G"], row)

    return {"determinants": (sp.factor(first.det()), sp.factor(second.det())), "ranks": expected_ranks}


def verify_ordinary_lines_and_projection_drop() -> dict[str, object]:
    """Check all ordinary relations, annihilators, and common-cell ranks."""

    relations = {
        "A": ((1, 0, 0, 0, 0), (0, 0, 0, 1, 0)),
        "B": ((1, 0, 0, 0, 0), (0, 0, 0, 0, 1)),
        "C": ((1, 0, 0, 0, 0), (0, -1, 1, 0, 0)),
        "D": ((0, 1, 0, 0, 0), (0, 0, 0, 1, 0)),
        "E": ((0, 1, 0, 0, 0), (0, 0, 0, 0, 1)),
        "F": ((0, 1, 0, 0, 0), (-1, 0, 1, 0, 0)),
    }
    for name, rows in relations.items():
        for row in rows:
            assert relation(LINES[name], row)

    expected_annihilators = {
        "A": (LINES["A'"],),
        "B": (LINES["B'"],),
        "C": (LINES["C'"],),
        "D": (LINES["D'"],),
        "E": (LINES["E'"],),
        "F": (LINES["C'"],),
    }
    for name, expected in expected_annihilators.items():
        actual = tuple(contraction_matrix(LINES[name]).T.nullspace())
        assert same_span(actual, tuple(vector(point) for point in expected))

    forms = {
        "a": vector((1, 0, 0, -1)),
        "b": vector((0, 1, 1, 0)),
        "c": vector((1, 0, 1, 0)),
        "d": vector((0, 1, 0, -1)),
    }
    cell_ranks = tuple(
        restricted_diagonal_rank(forms[first_name], forms[second_name])
        for first_name, second_name in (("a", "c"), ("a", "d"), ("b", "c"), ("b", "d"))
    )
    assert cell_ranks == (2, 2, 2, 2)
    return {"ordinary_annihilators": tuple(expected_annihilators), "common_cell_ranks": cell_ranks}


def verify_companions_and_residuals() -> tuple[str, ...]:
    """Check every forced companion colour and common residual covector."""

    companion_relations = {
        "A'": ((-1, 0, 1, 0, 0), (0, -1, 0, 0, 1)),
        "B'": ((-1, 0, 1, 0, 0), (0, -1, 0, 1, 0)),
        "C'": ((-1, 1, 0, 0, 0), (-1, 0, 0, 1, 0), (-1, 0, 0, 0, 1)),
        "D'": ((0, -1, 1, 0, 0), (-1, 0, 0, 0, 1)),
        "E'": ((0, -1, 1, 0, 0), (-1, 0, 0, 1, 0)),
    }
    for name, rows in companion_relations.items():
        for row in rows:
            assert relation(LINES[name], row)

    residuals = {
        "A-A'": ("A", "A'", (0, -1, 1, 0, 1), (0, 0, 0, 1, 0), (-2, 0, 0, 0)),
        "B-B'": ("B", "B'", (0, -1, 1, 1, 0), (0, 0, 0, 0, -1), (0, -2, 0, 0)),
        "C-C'": ("C", "C'", (0, 0, 0, -1, 1), (-2, 0, 1, 0, 0), (0, 0, 2, -2)),
        "D-D'": ("D", "D'", (-1, 0, 1, 0, 1), (0, 0, 0, -1, 0), (-2, 0, 0, 0)),
        "E-E'": ("E", "E'", (-1, 0, 1, 1, 0), (0, 0, 0, 0, 1), (0, -2, 0, 0)),
        "F-C'": ("F", "C'", (0, 0, 0, -1, 1), (-2, 0, 1, 0, 0), (0, 0, 2, -2)),
    }
    for low, companion, low_coefficients, companion_coefficients, ell in residuals.values():
        assert contraction_matrix(LINES[low]) * vector(low_coefficients) == vector(ell)
        assert contraction_matrix(LINES[companion]) * vector(companion_coefficients) == vector(ell)
    return tuple(residuals)


def verify_gates_and_slice_obstruction() -> dict[str, object]:
    """Check all endpoint gates and the rank-one-free cubic slice space."""

    x = sp.symbols("x0:4")
    channel_polynomials = {name: polynomial(CORES[name], x) for name in CHANNELS}
    coefficients = (
        (-1, -1, 1, 0, 1),
        (-1, -1, 1, 1, 0),
        (0, 0, 0, -1, 1),
    )
    gates = tuple(
        sp.factor(
            sum(
                coefficient * channel_polynomials[name]
                for coefficient, name in zip(row, CHANNELS, strict=True)
            )
        )
        for row in coefficients
    )
    assert sp.expand(gates[0] + x[0] * (x[1] - x[2] + x[3])) == 0
    assert sp.expand(gates[1] + x[1] * (x[0] - x[2] + x[3])) == 0
    assert sp.expand(gates[2] - (x[0] - x[1]) * (x[2] - x[3])) == 0

    X, U_symbol, V_symbol = sp.symbols("X U V")
    contraction_xuv = sp.Matrix(
        ((0, V_symbol, U_symbol), (V_symbol, 0, X), (U_symbol, X, 0))
    )
    principal_minors = tuple(
        sp.factor(contraction_xuv.extract(indices, indices).det())
        for indices in ((0, 1), (0, 2), (1, 2))
    )
    assert principal_minors == (-V_symbol**2, -U_symbol**2, -X**2)
    return {"gates": gates, "slice_minors": principal_minors}


def main() -> None:
    """Run the complete primary replay."""

    verify_dependencies()
    frame = verify_frame_and_cores()
    kernel = verify_kernel_and_common_line()
    ordinary = verify_ordinary_lines_and_projection_drop()
    residuals = verify_companions_and_residuals()
    gates = verify_gates_and_slice_obstruction()

    print("co-two r=4 fixed-e=2 full-extension primary: PASS")
    print(f"  frame={frame}")
    print(f"  kernel/common-line={kernel}")
    print(f"  ordinary/projection-drop={ordinary}")
    print(f"  companion residuals={residuals}")
    print(f"  factor gates={gates['gates']}")
    print("  fixed-e=2 representative 024 extension: EXCLUDED")
    print("  equality-five synthesis audit: PENDING")
    print("  unrestricted P6 -> Delta3: UNKNOWN")
    print("  global Krenn-Gu conjecture: UNRESOLVED")


if __name__ == "__main__":
    main()
