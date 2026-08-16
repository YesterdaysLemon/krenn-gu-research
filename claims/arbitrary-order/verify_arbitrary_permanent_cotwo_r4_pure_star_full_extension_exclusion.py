"""Primary exact replay for the co-two pure-star frame exclusion."""

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
    (1, -1, 0, 0),
    (1, 0, 0, -1),
    (1, 0, -1, 0),
)
V = (
    (1, -1, 1, 1),
    (1, 1, 1, -1),
    (1, 1, -1, 1),
)

SOURCE = {
    "m1": (0, 1, -1, -1, 1, 0),
    "m2": (-1, 1, 0, 0, 1, -1),
    "d0": (-2, 1, 1, -1, -1, 0),
    "d1": (1, 1, -2, 0, -1, -1),
    "d2": (1, -2, 1, -1, 0, -1),
}

CORES = {
    "m1": (0, 1, -1, -1, 1, 0),
    "m2": (-1, 1, 0, 0, 1, -1),
    "d0": (0, -1, -1, 1, 1, -2),
    "d1": (-1, -1, 0, -2, 1, 1),
    "d2": (-1, 0, -1, 1, -2, 1),
}

LINES = {
    "A": (0, 0, 1, 1),
    "B": (1, 1, 0, 0),
    "C": (0, 1, 1, 0),
    "D": (1, 0, 0, 1),
    "N": (1, 1, 1, 1),
    "E": (0, 1, 0, 1),
    "F": (-1, 1, 0, 0),
    "G": (-1, 0, 0, 1),
    "H": (-1, 1, 1, 1),
}


def lf_sha256(path: Path) -> str:
    """Hash text after normalizing checkout CRLF to Git-blob LF."""

    return sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest().upper()


def vector(values: tuple[int | sp.Expr, ...]) -> sp.Matrix:
    """Return a column vector over the exact SymPy domain."""

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
    """Contract a square-free quadratic core with a first-slot vector."""

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


def verify_dependencies() -> None:
    """Pin the exact upstream based-frame and hyperplane-product interfaces."""

    for relative, expected in DEPENDENCIES.items():
        path = ROOT / relative
        actual = lf_sha256(path)
        assert actual == expected, (
            f"dependency hash mismatch for {relative}: "
            f"expected {expected}, got {actual}"
        )


def verify_frame_and_cores() -> dict[str, object]:
    """Rebuild the pair product, complement cores, and mixed factorizations."""

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
    assert vector(products[0, 2]) == -vector(SOURCE["m1"])
    assert vector(products[1, 2]) == -vector(SOURCE["m2"])
    assert vector(products[2, 0]) == -vector(SOURCE["m1"]) + vector(SOURCE["m2"])
    assert vector(products[2, 1]) == vector(SOURCE["m1"]) - vector(SOURCE["m2"])

    for name in CHANNELS:
        assert edge_complement(SOURCE[name]) == CORES[name]

    xs = sp.symbols("x0:4")
    assert sp.expand(
        polynomial(CORES["m1"], xs) - (xs[0] - xs[1]) * (xs[2] - xs[3])
    ) == 0
    assert sp.expand(
        polynomial(CORES["m2"], xs) + (xs[0] - xs[3]) * (xs[1] - xs[2])
    ) == 0
    return {"mixed_rank": mixed.rank(), "product_rank": full.rank()}


def verify_kernel_boundary() -> dict[str, object]:
    """Check both generic determinants and every exceptional support relation."""

    a, b = sp.symbols("a b")
    p1 = (a, a, b, b)
    p2 = (a, b, b, a)
    first = sp.Matrix.hstack(
        contraction(CORES["m2"], p1),
        contraction(CORES["d0"], p1),
        contraction(CORES["d1"], p1),
        contraction(CORES["d2"], p1),
    )
    second = sp.Matrix.hstack(
        contraction(CORES["m1"], p2),
        contraction(CORES["d0"], p2),
        contraction(CORES["d1"], p2),
        contraction(CORES["d2"], p2),
    )
    expected = -64 * a**2 * b * (a - b)
    assert sp.factor(first.det()) == expected
    assert sp.factor(second.det()) == expected

    exceptional_relations = {
        "A": ((0, 1, 0, 1, 0), (0, 1, 0, 0, 1)),
        "B": ((0, 0, 1, 0, 0),),
        "C": ((1, 0, 1, 0, 0), (1, 0, 0, 0, 1)),
        "D": ((0, 0, 0, 1, 0),),
    }
    for name, relations in exceptional_relations.items():
        for coefficients in relations:
            assert relation(LINES[name], coefficients)

    n_matrix = contraction_matrix(LINES["N"])
    assert n_matrix.rank() == 3
    n_annihilator = tuple(n_matrix.T.nullspace())
    assert same_span(n_annihilator, (vector(LINES["H"]),))
    assert relation(LINES["H"], (-1, 1, -1, 1, 0))
    assert relation(LINES["H"], (0, 1, -1, 0, 1))

    ranks = {name: contraction_matrix(point).rank() for name, point in LINES.items()}
    assert {name: ranks[name] for name in ("A", "B", "C", "D", "N")} == {
        "A": 2,
        "B": 3,
        "C": 2,
        "D": 3,
        "N": 3,
    }
    return {"generic_determinant": sp.factor(expected), "exceptional_ranks": ranks}


def verify_common_cells() -> tuple[int, int, int, int]:
    """Recompute the four common-missing-factor diagonal sensor ranks."""

    forms = {
        "A": vector((1, -1, 0, 0)),
        "B": vector((0, 0, 1, -1)),
        "C": vector((1, 0, 0, -1)),
        "D": vector((0, 1, -1, 0)),
    }
    x = sp.symbols("x0:4")
    s, t = sp.symbols("s t")
    diagonal_polynomials = [polynomial(CORES[name], x) for name in ("d0", "d1", "d2")]
    results: list[int] = []
    for first_name, second_name in (("A", "C"), ("A", "D"), ("B", "C"), ("B", "D")):
        equations = sp.Matrix.vstack(forms[first_name].T, forms[second_name].T)
        basis = equations.nullspace()
        assert len(basis) == 2
        substitution = {
            x[index]: basis[0][index] * s + basis[1][index] * t for index in range(4)
        }
        rows = []
        for source in diagonal_polynomials:
            restricted = sp.Poly(sp.expand(source.subs(substitution)), s, t)
            rows.append(
                (
                    restricted.coeff_monomial(s**2),
                    restricted.coeff_monomial(s * t),
                    restricted.coeff_monomial(t**2),
                )
            )
        results.append(sp.Matrix(rows).rank())
    assert tuple(results) == (2, 2, 2, 1)
    return tuple(results)  # type: ignore[return-value]


def verify_companions() -> dict[str, object]:
    """Check the four-line annihilators, deletion loci, filters, and cycles."""

    expected_annihilators = {
        "A": (LINES["C"], LINES["E"]),
        "B": (LINES["F"],),
        "C": (LINES["A"], LINES["E"]),
        "D": (LINES["G"],),
    }
    for name, expected in expected_annihilators.items():
        actual = tuple(contraction_matrix(LINES[name]).T.nullspace())
        assert same_span(actual, tuple(vector(point) for point in expected))

    u, v = sp.symbols("u v")
    q_ac = tuple(u * LINES["C"][index] + v * LINES["E"][index] for index in range(4))
    matrix_ac = contraction_matrix(q_ac)
    assert matrix_ac.rank() == 3
    without_d1 = matrix_ac[:, (0, 1, 2, 4)]
    without_d2 = matrix_ac[:, (0, 1, 2, 3)]
    assert same_up_to_nonzero_constant(nonzero_minor_gcd(without_d1, 3), u * v**2)
    assert same_up_to_nonzero_constant(nonzero_minor_gcd(without_d2, 3), u**2 * v)

    q_ca = tuple(u * LINES["A"][index] + v * LINES["E"][index] for index in range(4))
    matrix_ca = contraction_matrix(q_ca)
    assert matrix_ca.rank() == 3
    without_d0 = matrix_ca[:, (0, 1, 3, 4)]
    without_d2 = matrix_ca[:, (0, 1, 2, 3)]
    assert same_up_to_nonzero_constant(nonzero_minor_gcd(without_d0, 3), u * v**2)
    assert same_up_to_nonzero_constant(nonzero_minor_gcd(without_d2, 3), u**2 * v)

    endpoint_relations = {
        "A": ((1, 0, 0, 0, 0), (0, 1, 0, 1, 0), (0, 1, 0, 0, 1)),
        "C": ((0, 1, 0, 0, 0), (1, 0, 1, 0, 0), (1, 0, 0, 0, 1)),
        "E": ((-1, 1, 0, 0, 0), (-1, 0, 1, 0, 0), (-1, 0, 0, 1, 0)),
        "F": ((0, -1, 0, 1, 0), (1, -1, 0, 0, 1)),
        "G": ((-1, 0, 1, 0, 0), (-1, 1, 0, 0, 1)),
    }
    for name, relations in endpoint_relations.items():
        for coefficients in relations:
            assert relation(LINES[name], coefficients)

    cycles = {
        "A-C": {
            "p": "A",
            "q": "C",
            "rp": (0, -2, 1, 0, 0),
            "rq": (-2, 0, 0, 1, 0),
            "ell": (-4, 0, 0, 0),
        },
        "A-E": {
            "p": "A",
            "q": "E",
            "rp": (0, -2, 1, 0, 0),
            "rq": (2, 0, 0, 0, 1),
            "ell": (-4, 0, 0, 0),
        },
        "C-A": {
            "p": "C",
            "q": "A",
            "rp": (-2, 0, 0, 1, 0),
            "rq": (0, -2, 1, 0, 0),
            "ell": (-4, 0, 0, 0),
        },
        "C-E": {
            "p": "C",
            "q": "E",
            "rp": (-2, 0, 0, 1, 0),
            "rq": (2, 0, 0, 0, 1),
            "ell": (-4, 0, 0, 0),
        },
        "B-F": {
            "p": "B",
            "q": "F",
            "rp": (0, 2, 0, -1, -1),
            "rq": (0, 0, 2, 0, 0),
            "ell": (0, 0, 4, 4),
        },
        "D-G": {
            "p": "D",
            "q": "G",
            "rp": (2, 0, -1, 0, -1),
            "rq": (0, 0, 0, 2, 0),
            "ell": (0, 4, 4, 0),
        },
    }
    for data in cycles.values():
        low = contraction_matrix(LINES[str(data["p"])]) * vector(data["rp"])  # type: ignore[arg-type]
        companion = contraction_matrix(LINES[str(data["q"])]) * vector(data["rq"])  # type: ignore[arg-type]
        expected = vector(data["ell"])  # type: ignore[arg-type]
        assert low == expected
        assert companion == expected

    return {
        "annihilators": {name: tuple(point for point in points) for name, points in expected_annihilators.items()},
        "cycles": tuple(cycles),
    }


def verify_factor_gates_and_slice_obstruction() -> dict[str, object]:
    """Check the unused-colour factors and the rank-one-free slice space."""

    x = sp.symbols("x0:4")
    channel_polynomials = {name: polynomial(CORES[name], x) for name in CHANNELS}

    first = sum(channel_polynomials[name] for name in ("d0", "d1", "d2"))
    assert sp.expand(first + 2 * x[0] * (x[1] + x[2] + x[3])) == 0

    second_coefficients = (-1, 2, -2, -1, -1)
    second = sum(
        coefficient * channel_polynomials[name]
        for coefficient, name in zip(second_coefficients, CHANNELS, strict=True)
    )
    assert sp.expand(second - 4 * x[0] * (x[2] + x[3])) == 0

    third_coefficients = (2, -1, -1, -2, -1)
    third = sum(
        coefficient * channel_polynomials[name]
        for coefficient, name in zip(third_coefficients, CHANNELS, strict=True)
    )
    assert sp.expand(third - 4 * x[0] * (x[1] + x[2])) == 0

    X, U_symbol, V_symbol = sp.symbols("X U V")
    contraction_matrix_xuv = sp.Matrix(
        (
            (0, V_symbol, U_symbol),
            (V_symbol, 0, X),
            (U_symbol, X, 0),
        )
    )
    principal_minors = tuple(
        sp.factor(contraction_matrix_xuv.extract(indices, indices).det())
        for indices in ((0, 1), (0, 2), (1, 2))
    )
    assert principal_minors == (-V_symbol**2, -U_symbol**2, -X**2)

    a, b, c = sp.symbols("a b c")
    slice_matrix = sp.Matrix(((0, c, b), (c, 0, a), (b, a, 0)))
    slice_principal_minors = tuple(
        sp.factor(slice_matrix.extract(indices, indices).det())
        for indices in ((0, 1), (0, 2), (1, 2))
    )
    assert slice_principal_minors == (-c**2, -b**2, -a**2)
    return {
        "factor_gates": (
            sp.factor(first),
            sp.factor(second),
            sp.factor(third),
        ),
        "slice_principal_minors": slice_principal_minors,
    }


def main() -> None:
    """Run the complete primary replay."""

    verify_dependencies()
    frame = verify_frame_and_cores()
    kernel = verify_kernel_boundary()
    common_cells = verify_common_cells()
    companions = verify_companions()
    gates = verify_factor_gates_and_slice_obstruction()

    print("co-two r=4 pure-star full-extension primary: PASS")
    print(f"  frame={frame}")
    print(f"  kernel={kernel}")
    print(f"  common-cell diagonal ranks={common_cells}")
    print(f"  companion cycles={companions['cycles']}")
    print(f"  factor gates={gates['factor_gates']}")
    print("  pure-star representative 014 extension: EXCLUDED")
    print("  fixed representatives 025 and 024: OPEN")
    print("  unrestricted P6 -> Delta3: UNKNOWN")
    print("  global Krenn-Gu conjecture: UNRESOLVED")


if __name__ == "__main__":
    main()
