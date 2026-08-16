"""Primary exact replay for the co-two fixed-e=1 frame exclusion."""

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
    "claims/arbitrary-order/"
    "ARBITRARY_PERMANENT_FIXED_PAIR_TWO_SIDED_PROJECTION_DROP_THEOREM.md": (
        "A383731E094E0D0E45482AAB889FB8B202FC7A2CF452D8534D5035E737089F36"
    ),
    "docs/audits/"
    "ARBITRARY_PERMANENT_FIXED_PAIR_TWO_SIDED_PROJECTION_DROP_REVIEW_2026-08-15.md": (
        "9488F5B766EFCFCBB3E5EEEF4867D8604FD068B1A38B25D86E4C03EED98B51F4"
    ),
}

U = (
    (0, 1, -1, 0),
    (1, -1, 0, 0),
    (1, 0, 0, -1),
)
V = (
    (0, 1, 0, 1),
    (1, -1, 0, 0),
    (1, 0, 1, 0),
)

SOURCE = {
    "m1": (1, -1, 0, 1, 0, 0),
    "m2": (1, 0, 1, 0, -1, 0),
    "d0": (0, 0, 0, -1, 1, -1),
    "d1": (-2, 0, 0, 0, 0, 0),
    "d2": (0, 1, -1, 0, 0, -1),
}

CORES = {
    "m1": (0, 0, 1, 0, -1, 1),
    "m2": (0, -1, 0, 1, 0, 1),
    "d0": (-1, 1, -1, 0, 0, 0),
    "d1": (0, 0, 0, 0, 0, -2),
    "d2": (-1, 0, 0, -1, 1, 0),
}

LINES = {
    "A": (-1, 0, 1, 0),
    "B": (0, 1, 1, 0),
    "C": (1, 0, 0, 1),
    "D": (0, 1, 0, -1),
    "N": (1, 1, 0, 0),
    "A'": (1, 0, 1, 0),
    "B'": (0, -1, 1, 0),
    "C'": (-1, 0, 0, 1),
    "D'": (0, 1, 0, 1),
    "Q+": (-1, 1, 1, 1),
    "Q-": (-1, 1, -1, -1),
    "R1": (-1, 1, 0, 0),
    "R2": (0, 0, 1, 1),
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

    by_edge = {edge: coefficients[index] for index, edge in enumerate(EDGES)}
    vertices = frozenset(range(4))
    return tuple(
        sp.expand(by_edge[tuple(sorted(vertices - frozenset(edge)))])
        for edge in EDGES
    )


def contraction(
    core: tuple[int | sp.Expr, ...], point: tuple[int | sp.Expr, ...]
) -> sp.Matrix:
    """Contract a square-free quadratic core with one vector."""

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


def nonzero_minor_gcd(matrix: sp.Matrix, size: int) -> sp.Expr:
    """Return the gcd of every nonzero exact minor of a fixed size."""

    minors: list[sp.Expr] = []
    for rows in combinations(range(matrix.rows), size):
        for columns in combinations(range(matrix.cols), size):
            determinant = sp.factor(matrix.extract(rows, columns).det())
            if determinant != 0:
                minors.append(determinant)
    assert minors
    return sp.factor(sp.gcd_list(minors))


def same_up_to_nonzero_constant(left: sp.Expr, right: sp.Expr) -> bool:
    """Test equality up to a nonzero rational unit."""

    quotient = sp.cancel(left / right)
    return not quotient.free_symbols and quotient != 0


def restricted_diagonal_rank(forms: tuple[sp.Matrix, sp.Matrix]) -> int:
    """Rank of the three diagonal quadratics on a codimension-two cell."""

    x = sp.symbols("x0:4")
    s, t = sp.symbols("s t")
    equations = sp.Matrix.vstack(*(form.T for form in forms))
    basis = equations.nullspace()
    assert len(basis) == 2
    substitution = {
        x[index]: basis[0][index] * s + basis[1][index] * t for index in range(4)
    }
    rows = []
    for name in ("d0", "d1", "d2"):
        restricted = sp.Poly(
            sp.expand(polynomial(CORES[name], x).subs(substitution)), s, t
        )
        rows.append(
            (
                restricted.coeff_monomial(s**2),
                restricted.coeff_monomial(s * t),
                restricted.coeff_monomial(t**2),
            )
        )
    return sp.Matrix(rows).rank()


def verify_dependencies() -> None:
    """Pin the exact upstream based-frame and product-geometry interfaces."""

    for relative, expected in DEPENDENCIES.items():
        path = ROOT / relative
        actual = lf_sha256(path)
        assert actual == expected, (
            f"dependency hash mismatch for {relative}: "
            f"expected {expected}, got {actual}"
        )


def verify_frame_and_cores() -> dict[str, object]:
    """Rebuild the pair product, complement cores, and mixed projections."""

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
    assert products[0, 2] == SOURCE["m1"]
    assert vector(products[1, 2]) == -vector(SOURCE["m1"])
    assert products[2, 0] == SOURCE["m2"]
    assert vector(products[2, 1]) == -vector(SOURCE["m2"])

    for name in CHANNELS:
        assert edge_complement(SOURCE[name]) == CORES[name]

    x = sp.symbols("x0:4")
    expected_factors = {
        "m1": x[3] * (x[0] - x[1] + x[2]),
        "m2": x[2] * (-x[0] + x[1] + x[3]),
        "d0": -x[0] * (x[1] - x[2] + x[3]),
        "d1": -2 * x[2] * x[3],
        "d2": -x[1] * (x[0] + x[2] - x[3]),
    }
    for name, expected in expected_factors.items():
        assert sp.expand(polynomial(CORES[name], x) - expected) == 0

    return {"mixed_rank": mixed.rank(), "product_rank": full.rank()}


def verify_kernel_boundary() -> dict[str, object]:
    """Check generic determinants, exceptional ranks, relations, and annihilators."""

    a, b = sp.symbols("a b")
    p1 = (a - b, a, b, 0)
    p2 = (a + b, a, 0, b)
    first = sp.Matrix.hstack(
        *(contraction(CORES[name], p1) for name in ("m2", "d0", "d1", "d2"))
    )
    second = sp.Matrix.hstack(
        *(contraction(CORES[name], p2) for name in ("m1", "d0", "d1", "d2"))
    )
    first_expected = -8 * a * b**2 * (a - b)
    second_expected = 8 * a * b**2 * (a + b)
    assert sp.factor(first.det()) == first_expected
    assert sp.factor(second.det()) == second_expected

    expected_ranks = {"A": 3, "B": 3, "C": 3, "D": 3, "N": 2}
    for name, expected in expected_ranks.items():
        assert contraction_matrix(LINES[name]).rank() == expected

    exceptional_relations = {
        "A": ((1, 0, 0, 0, 0), (0, 0, 0, 0, 1)),
        "B": ((1, 0, 0, 0, 0), (0, 0, 1, 0, 0)),
        "C": ((0, 1, 0, 0, 0), (0, 0, 0, 0, 1)),
        "D": ((0, 1, 0, 0, 0), (0, 0, 1, 0, 0)),
        "N": (
            (1, 0, 0, 0, 0),
            (0, 1, 0, 0, 0),
            (0, 0, 0, 1, 0),
        ),
    }
    for name, relations in exceptional_relations.items():
        for coefficients in relations:
            assert relation(LINES[name], coefficients)

    expected_annihilators = {
        "A": (LINES["A'"],),
        "B": (LINES["B'"],),
        "C": (LINES["C'"],),
        "D": (LINES["D'"],),
        "N": (LINES["R1"], LINES["R2"]),
    }
    for name, expected in expected_annihilators.items():
        actual = tuple(contraction_matrix(LINES[name]).T.nullspace())
        assert same_span(actual, tuple(vector(point) for point in expected))

    return {
        "determinants": (sp.factor(first.det()), sp.factor(second.det())),
        "exceptional_ranks": expected_ranks,
    }


def verify_projection_drop_data() -> dict[str, object]:
    """Replay common-cell ranks, the dangerous square, and N contractions."""

    h1 = vector((1, -1, 1, 0))
    h2 = vector((-1, 1, 0, 1))
    x2 = vector((0, 0, 1, 0))
    x3 = vector((0, 0, 0, 1))
    ranks = {
        "h1-x2": restricted_diagonal_rank((h1, x2)),
        "h1-h2": restricted_diagonal_rank((h1, h2)),
        "h2-x3": restricted_diagonal_rank((h2, x3)),
    }
    assert ranks == {"h1-x2": 2, "h1-h2": 3, "h2-x3": 2}

    x = sp.symbols("x0:4")
    s, t = sp.symbols("s t")
    substitution = {x[0]: s - t, x[1]: s, x[2]: t, x[3]: -t}
    restricted = tuple(
        sp.factor(polynomial(CORES[name], x).subs(substitution))
        for name in ("d0", "d1", "d2")
    )
    expected_restrictions = (-(s - 2 * t) * (s - t), 2 * t**2, -s * (s + t))
    assert all(
        sp.expand(actual - expected) == 0
        for actual, expected in zip(restricted, expected_restrictions, strict=True)
    )
    dangerous = sp.expand(4 * restricted[0] + 3 * restricted[1] + 4 * restricted[2])
    assert sp.expand(dangerous + 2 * (2 * s - t) ** 2) == 0

    n_values = {
        name: sp.expand((contraction(CORES[name], LINES["N"]).T * vector(LINES["N"]))[0])
        for name in CHANNELS
    }
    assert n_values == {"m1": 0, "m2": 0, "d0": -2, "d1": 0, "d2": -2}

    X, U_symbol, V_symbol = sp.symbols("X U V")
    quartic = X**2 * U_symbol * V_symbol
    cubic_slices = (
        sp.diff(quartic, X),
        sp.diff(quartic, U_symbol),
        sp.diff(quartic, V_symbol),
    )
    monomials = (X * U_symbol * V_symbol, X**2 * V_symbol, X**2 * U_symbol)
    coefficient_matrix = sp.Matrix(
        [
            [sp.Poly(cubic, X, U_symbol, V_symbol).coeff_monomial(m) for m in monomials]
            for cubic in cubic_slices
        ]
    )
    assert coefficient_matrix.rank() == 3
    aa, bb, cc = sp.symbols("aa bb cc")
    cube = sp.Poly((aa * X + bb * U_symbol + cc * V_symbol) ** 3, X, U_symbol, V_symbol)
    assert (
        cube.coeff_monomial(X**3),
        cube.coeff_monomial(U_symbol**3),
        cube.coeff_monomial(V_symbol**3),
    ) == (aa**3, bb**3, cc**3)

    return {"common_cell_ranks": ranks, "N_double_contractions": n_values}


def verify_companions() -> dict[str, object]:
    """Check every companion relation, the N deletion locus, and residual table."""

    endpoint_relations = {
        "A'": ((0, 1, 1, 0, 0), (1, 0, 0, 1, 0)),
        "B'": ((1, 0, 0, 1, 0), (0, 1, 0, 0, 1)),
        "C'": ((1, 0, 1, 0, 0), (0, 1, 0, 1, 0)),
        "D'": ((0, 1, 0, 1, 0), (1, 0, 0, 0, 1)),
        "Q+": ((1, 0, 1, 0, 0), (1, 0, 0, 0, 1)),
        "Q-": ((0, 1, 1, 0, 0), (0, 1, 0, 0, 1)),
    }
    for name, relations in endpoint_relations.items():
        for coefficients in relations:
            assert relation(LINES[name], coefficients)

    u, v = sp.symbols("u v")
    q = (-u, u, v, v)
    q_matrix = contraction_matrix(q)
    assert q_matrix * vector((0, 0, 1, 0, -1)) == sp.zeros(4, 1)
    assert same_up_to_nonzero_constant(nonzero_minor_gcd(q_matrix, 3), u)
    without_d1 = q_matrix[:, (0, 1, 2, 4)]
    assert same_up_to_nonzero_constant(
        nonzero_minor_gcd(without_d1, 3), u * (u - v) * (u + v)
    )
    rank_table = {
        "u0": (q_matrix.subs({u: 0, v: 1}).rank(), without_d1.subs({u: 0, v: 1}).rank()),
        "plus": (
            q_matrix.subs({u: 1, v: 1}).rank(),
            without_d1.subs({u: 1, v: 1}).rank(),
        ),
        "minus": (
            q_matrix.subs({u: 1, v: -1}).rank(),
            without_d1.subs({u: 1, v: -1}).rank(),
        ),
        "generic": (
            q_matrix.subs({u: 2, v: 1}).rank(),
            without_d1.subs({u: 2, v: 1}).rank(),
        ),
    }
    assert rank_table == {
        "u0": (2, 2),
        "plus": (3, 2),
        "minus": (3, 2),
        "generic": (3, 3),
    }

    residuals = {
        "A-A'": ("A", "A'", (0, -1, -1, -1, 0), (0, 0, 0, 0, 1), (0, -2, 0, 0)),
        "B-B'": ("B", "B'", (0, -1, 0, -1, -1), (0, 0, 1, 0, 0), (2, 0, 0, 0)),
        "C-C'": ("C", "C'", (-1, 0, -1, -1, 0), (0, 0, 0, 0, 1), (0, 2, 0, 0)),
        "D-D'": ("D", "D'", (-1, 0, 0, -1, -1), (0, 0, -1, 0, 0), (2, 0, 0, 0)),
        "N-Q+": ("N", "Q+", (0, 0, -1, 0, 1), (-1, -1, 0, -1, 0), (0, 0, -2, 2)),
        "N-Q-": ("N", "Q-", (0, 0, -1, 0, 1), (-1, -1, 0, -1, 0), (0, 0, -2, 2)),
    }
    for low_name, companion_name, low_coefficients, companion_coefficients, ell in residuals.values():
        low = contraction_matrix(LINES[low_name]) * vector(low_coefficients)
        companion = contraction_matrix(LINES[companion_name]) * vector(companion_coefficients)
        assert low == vector(ell)
        assert companion == vector(ell)

    return {"N_deletion_ranks": rank_table, "residuals": tuple(residuals)}


def verify_factor_gates_and_slice_obstructions() -> dict[str, object]:
    """Check all endpoint factors and both rank-one-free slice spaces."""

    x = sp.symbols("x0:4")
    channel_polynomials = {name: polynomial(CORES[name], x) for name in CHANNELS}
    coefficients = (
        (1, 1, 1, 1, 0),
        (1, 1, 0, 1, 1),
        (0, 0, -1, 0, 1),
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
    assert sp.expand(gates[0] + x[1] * (x[0] - x[2] + x[3])) == 0
    assert sp.expand(gates[1] + x[0] * (x[1] + x[2] - x[3])) == 0
    assert sp.expand(gates[2] - (x[0] + x[1]) * (x[3] - x[2])) == 0

    X, U_symbol, V_symbol = sp.symbols("X U V")
    contraction_xuv = sp.Matrix(
        (
            (0, V_symbol, U_symbol),
            (V_symbol, 0, X),
            (U_symbol, X, 0),
        )
    )
    principal_minors = tuple(
        sp.factor(contraction_xuv.extract(indices, indices).det())
        for indices in ((0, 1), (0, 2), (1, 2))
    )
    assert principal_minors == (-V_symbol**2, -U_symbol**2, -X**2)

    aa, bb, cc = sp.symbols("aa bb cc")
    rank_one_slice = sp.Matrix(((0, cc, bb), (cc, 0, aa), (bb, aa, 0)))
    rank_one_minors = tuple(
        sp.factor(rank_one_slice.extract(indices, indices).det())
        for indices in ((0, 1), (0, 2), (1, 2))
    )
    assert rank_one_minors == (-cc**2, -bb**2, -aa**2)

    return {"factor_gates": gates, "slice_minors": principal_minors}


def main() -> None:
    """Run the complete primary replay."""

    verify_dependencies()
    frame = verify_frame_and_cores()
    kernel = verify_kernel_boundary()
    projection = verify_projection_drop_data()
    companions = verify_companions()
    gates = verify_factor_gates_and_slice_obstructions()

    print("co-two r=4 fixed-e=1 full-extension primary: PASS")
    print(f"  frame={frame}")
    print(f"  kernel={kernel}")
    print(f"  projection-drop data={projection}")
    print(f"  companion residuals={companions['residuals']}")
    print(f"  factor gates={gates['factor_gates']}")
    print("  fixed-e=1 representative 025 extension: EXCLUDED")
    print("  fixed-e=2 representative 024: OPEN")
    print("  unrestricted P6 -> Delta3: UNKNOWN")
    print("  global Krenn-Gu conjecture: UNRESOLVED")


if __name__ == "__main__":
    main()
