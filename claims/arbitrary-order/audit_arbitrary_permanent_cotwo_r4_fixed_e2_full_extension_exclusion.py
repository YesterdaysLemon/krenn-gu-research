"""Independent no-import audit of the co-two fixed-e=2 exclusion.

This audit imports neither the primary verifier nor SymPy.  It rebuilds the
frame with rational linear algebra, expands the generic determinants in a
small polynomial ring, and independently checks every exceptional incidence,
common cell, residual covector, factor gate, and finite-field slice stress test.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from itertools import combinations, permutations, product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
THEOREM = (
    HERE / "ARBITRARY_PERMANENT_COTWO_R4_FIXED_E2_FULL_EXTENSION_EXCLUSION_THEOREM.md"
)
PRIMARY = (
    HERE / "verify_arbitrary_permanent_cotwo_r4_fixed_e2_full_extension_exclusion.py"
)

THEOREM_SHA256 = "CF79C02D6C45359F1F26AEFAD4E4C0AB9715A57ADA26B1E57D18A772022B764E"
PRIMARY_SHA256 = "A4F68FB8AE8D5D977C99875C2E2298C2417E29A408B81F1345C9BDE990477A91"

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

EDGES = tuple(combinations(range(4), 2))
CHANNELS = ("m1", "m2", "d0", "d1", "d2")

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

RationalMatrix = list[list[Fraction]]
Polynomial = dict[tuple[int, int], int]


def lf_sha256(path: Path) -> str:
    """Hash text after normalizing checkout CRLF to Git-blob LF."""

    return sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest().upper()


def verify_hashes() -> None:
    """Check the frozen theorem, primary, and predecessor interfaces."""

    expected = {THEOREM: THEOREM_SHA256, PRIMARY: PRIMARY_SHA256}
    expected.update({ROOT / relative: digest for relative, digest in DEPENDENCIES.items()})
    for path, digest in expected.items():
        actual = lf_sha256(path)
        assert actual == digest, f"hash mismatch for {path}: expected {digest}, got {actual}"


def as_fraction_matrix(rows: list[list[int | Fraction]]) -> RationalMatrix:
    """Convert a row-major matrix to exact fractions."""

    return [[Fraction(entry) for entry in row] for row in rows]


def columns_matrix(columns: list[tuple[int | Fraction, ...]]) -> RationalMatrix:
    """Build a row-major matrix from column vectors."""

    return as_fraction_matrix([list(row) for row in zip(*columns, strict=True)])


def rref(matrix: RationalMatrix) -> tuple[RationalMatrix, list[int]]:
    """Return an exact reduced row-echelon form and pivot columns."""

    work = [row[:] for row in matrix]
    if not work:
        return work, []
    rows = len(work)
    columns = len(work[0])
    pivots: list[int] = []
    pivot_row = 0
    for column in range(columns):
        source = next(
            (row for row in range(pivot_row, rows) if work[row][column] != 0),
            None,
        )
        if source is None:
            continue
        work[pivot_row], work[source] = work[source], work[pivot_row]
        pivot = work[pivot_row][column]
        work[pivot_row] = [entry / pivot for entry in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row:
                continue
            scale = work[row][column]
            if scale:
                work[row] = [
                    left - scale * right
                    for left, right in zip(work[row], work[pivot_row], strict=True)
                ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == rows:
            break
    return work, pivots


def rank(matrix: RationalMatrix) -> int:
    """Return exact rational matrix rank."""

    return len(rref(matrix)[1])


def nullspace(matrix: RationalMatrix) -> list[tuple[Fraction, ...]]:
    """Return an exact basis of the right nullspace."""

    reduced, pivots = rref(matrix)
    columns = len(matrix[0])
    free = [column for column in range(columns) if column not in pivots]
    basis: list[tuple[Fraction, ...]] = []
    for free_column in free:
        vector = [Fraction(0) for _ in range(columns)]
        vector[free_column] = Fraction(1)
        for row, pivot in enumerate(pivots):
            vector[pivot] = -reduced[row][free_column]
        basis.append(tuple(vector))
    return basis


def dot(left: tuple[int | Fraction, ...], right: tuple[int | Fraction, ...]) -> Fraction:
    """Return an exact dot product."""

    return sum(
        (Fraction(a) * Fraction(b) for a, b in zip(left, right, strict=True)),
        start=Fraction(0),
    )


def squarefree_product(
    left: tuple[int, ...], right: tuple[int, ...]
) -> tuple[int, ...]:
    """Multiply two integer linear forms in the square-free algebra."""

    return tuple(left[i] * right[j] + left[j] * right[i] for i, j in EDGES)


def edge_complement(coefficients: tuple[int, ...]) -> tuple[int, ...]:
    """Apply edge complementation in an independent tuple representation."""

    lookup = {edge: coefficients[index] for index, edge in enumerate(EDGES)}
    vertices = frozenset(range(4))
    return tuple(lookup[tuple(sorted(vertices - frozenset(edge)))] for edge in EDGES)


def contraction(core: tuple[int, ...], point: tuple[int, ...]) -> tuple[int, ...]:
    """Contract one quadratic core with one integer vector."""

    output = [0, 0, 0, 0]
    for coefficient, (left, right) in zip(core, EDGES, strict=True):
        output[right] += coefficient * point[left]
        output[left] += coefficient * point[right]
    return tuple(output)


def contraction_columns(point: tuple[int, ...]) -> list[tuple[int, ...]]:
    """Return the five integer contraction columns."""

    return [contraction(CORES[name], point) for name in CHANNELS]


def combine_columns(
    columns: list[tuple[int, ...]], coefficients: tuple[int, ...]
) -> tuple[int, ...]:
    """Take an exact integer combination of equal-length columns."""

    return tuple(
        sum(coefficients[column] * columns[column][row] for column in range(len(columns)))
        for row in range(len(columns[0]))
    )


def relation(point: tuple[int, ...], coefficients: tuple[int, ...]) -> bool:
    """Check an exact contraction relation."""

    return combine_columns(contraction_columns(point), coefficients) == (0, 0, 0, 0)


def poly_add(left: Polynomial, right: Polynomial) -> Polynomial:
    """Add two bivariate integer polynomials."""

    result = dict(left)
    for monomial, coefficient in right.items():
        result[monomial] = result.get(monomial, 0) + coefficient
        if result[monomial] == 0:
            del result[monomial]
    return result


def poly_scale(polynomial: Polynomial, scalar: int) -> Polynomial:
    """Scale a bivariate integer polynomial."""

    return {} if scalar == 0 else {
        monomial: scalar * coefficient for monomial, coefficient in polynomial.items()
    }


def poly_multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    """Multiply two bivariate integer polynomials."""

    result: Polynomial = {}
    for (left_r, left_s), left_coefficient in left.items():
        for (right_r, right_s), right_coefficient in right.items():
            monomial = (left_r + right_r, left_s + right_s)
            result[monomial] = result.get(monomial, 0) + left_coefficient * right_coefficient
            if result[monomial] == 0:
                del result[monomial]
    return result


def permutation_sign(permutation: tuple[int, ...]) -> int:
    """Return the sign of a permutation."""

    inversions = sum(
        permutation[left] > permutation[right]
        for left in range(len(permutation))
        for right in range(left + 1, len(permutation))
    )
    return -1 if inversions % 2 else 1


def polynomial_determinant(matrix: list[list[Polynomial]]) -> Polynomial:
    """Compute a small determinant in the independent polynomial ring."""

    result: Polynomial = {}
    for permutation in permutations(range(len(matrix))):
        term: Polynomial = {(0, 0): permutation_sign(permutation)}
        for row, column in enumerate(permutation):
            term = poly_multiply(term, matrix[row][column])
        result = poly_add(result, term)
    return result


def poly_linear(first: int, second: int) -> Polynomial:
    """Return first*r + second*s."""

    result: Polynomial = {}
    if first:
        result[(1, 0)] = first
    if second:
        result[(0, 1)] = second
    return result


def polynomial_contraction_matrix(
    core_names: tuple[str, ...], point: tuple[Polynomial, ...]
) -> list[list[Polynomial]]:
    """Build a contraction matrix over the custom polynomial ring."""

    columns: list[list[Polynomial]] = []
    for name in core_names:
        output: list[Polynomial] = [{}, {}, {}, {}]
        for coefficient, (left, right) in zip(CORES[name], EDGES, strict=True):
            output[right] = poly_add(output[right], poly_scale(point[left], coefficient))
            output[left] = poly_add(output[left], poly_scale(point[right], coefficient))
        columns.append(output)
    return [[columns[column][row] for column in range(len(columns))] for row in range(4)]


def verify_frame_and_determinants() -> dict[str, object]:
    """Rebuild the frame, all cores, and both generic determinants."""

    products = {(i, j): squarefree_product(U[i], V[j]) for i in range(3) for j in range(3)}
    mixed = [products[i, j] for i in range(3) for j in range(3) if i != j]
    full = [products[i, j] for i in range(3) for j in range(3)]
    assert rank(columns_matrix(mixed)) == 2
    assert rank(columns_matrix(full)) == 5
    assert products[0, 1] == SOURCE["m1"]
    assert products[1, 0] == SOURCE["m2"]
    assert products[0, 0] == SOURCE["d0"]
    assert products[1, 1] == SOURCE["d1"]
    assert products[2, 2] == SOURCE["d2"]
    assert products[0, 2] == products[1, 2] == SOURCE["m2"]
    assert products[2, 0] == products[2, 1] == SOURCE["m1"]
    for name in CHANNELS:
        assert edge_complement(SOURCE[name]) == CORES[name]

    r = poly_linear(1, 0)
    s = poly_linear(0, 1)
    p1 = (r, s, poly_scale(s, -1), r)
    p2 = (r, s, poly_scale(r, -1), s)
    first = polynomial_contraction_matrix(("m2", "d0", "d1", "d2"), p1)
    second = polynomial_contraction_matrix(("m1", "d0", "d1", "d2"), p2)
    expected = {(3, 1): 8, (1, 3): -8}
    assert polynomial_determinant(first) == expected
    assert polynomial_determinant(second) == poly_scale(expected, -1)
    return {"mixed_rank": 2, "product_rank": 5, "determinant": expected}


def verify_annihilator(low_name: str, expected_name: str) -> None:
    """Check a one-dimensional companion annihilator."""

    columns = contraction_columns(LINES[low_name])
    assert rank(columns_matrix(columns)) == 3
    assert all(dot(LINES[expected_name], column) == 0 for column in columns)


def verify_lines_common_and_ordinary() -> dict[str, int]:
    """Check the common-line contradiction and all six ordinary lines."""

    expected_ranks = {name: 3 for name in ("A", "B", "C", "D", "E", "F", "N")}
    for name, expected in expected_ranks.items():
        assert rank(columns_matrix(contraction_columns(LINES[name]))) == expected

    for row in ((1, 0, 0, 0, 0), (0, 1, 0, 0, 0)):
        assert relation(LINES["N"], row)
    verify_annihilator("N", "G")
    for row in ((-1, -1, 1, 0, 0), (0, 0, 0, 1, 0), (0, 0, 0, 0, 1)):
        assert relation(LINES["G"], row)

    ordinary_relations = {
        "A": ((1, 0, 0, 0, 0), (0, 0, 0, 1, 0)),
        "B": ((1, 0, 0, 0, 0), (0, 0, 0, 0, 1)),
        "C": ((1, 0, 0, 0, 0), (0, -1, 1, 0, 0)),
        "D": ((0, 1, 0, 0, 0), (0, 0, 0, 1, 0)),
        "E": ((0, 1, 0, 0, 0), (0, 0, 0, 0, 1)),
        "F": ((0, 1, 0, 0, 0), (-1, 0, 1, 0, 0)),
    }
    for name, rows in ordinary_relations.items():
        for row in rows:
            assert relation(LINES[name], row)

    for low, companion in {
        "A": "A'",
        "B": "B'",
        "C": "C'",
        "D": "D'",
        "E": "E'",
        "F": "C'",
    }.items():
        verify_annihilator(low, companion)
    return expected_ranks


def restricted_core_row(
    core: tuple[int, ...], first: tuple[Fraction, ...], second: tuple[Fraction, ...]
) -> tuple[Fraction, Fraction, Fraction]:
    """Restrict one quadratic core to a rational two-plane."""

    rr = Fraction(0)
    rs = Fraction(0)
    ss = Fraction(0)
    for coefficient, (left, right) in zip(core, EDGES, strict=True):
        rr += coefficient * first[left] * first[right]
        rs += coefficient * (
            first[left] * second[right] + second[left] * first[right]
        )
        ss += coefficient * second[left] * second[right]
    return rr, rs, ss


def diagonal_rank_on_cell(first_form: tuple[int, ...], second_form: tuple[int, ...]) -> int:
    """Compute diagonal-core rank on one codimension-two cell."""

    basis = nullspace(as_fraction_matrix([list(first_form), list(second_form)]))
    assert len(basis) == 2
    rows = [
        list(restricted_core_row(CORES[name], basis[0], basis[1]))
        for name in ("d0", "d1", "d2")
    ]
    return rank(rows)


def verify_common_cells() -> tuple[int, int, int, int]:
    """Independently solve and rank the four common projection cells."""

    forms = {
        "a": (1, 0, 0, -1),
        "b": (0, 1, 1, 0),
        "c": (1, 0, 1, 0),
        "d": (0, 1, 0, -1),
    }
    results = tuple(
        diagonal_rank_on_cell(forms[first], forms[second])
        for first, second in (("a", "c"), ("a", "d"), ("b", "c"), ("b", "d"))
    )
    assert results == (2, 2, 2, 2)
    return results


def verify_companions_and_residuals() -> tuple[str, ...]:
    """Check all forced-colour relations and common residual covectors."""

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
    for low, companion, low_coefficients, companion_coefficients, expected in residuals.values():
        assert combine_columns(contraction_columns(LINES[low]), low_coefficients) == expected
        assert combine_columns(
            contraction_columns(LINES[companion]), companion_coefficients
        ) == expected
    return tuple(residuals)


def linear_combination_of_cores(coefficients: tuple[int, ...]) -> tuple[int, ...]:
    """Combine the five core coefficient vectors."""

    return tuple(
        sum(coefficients[channel] * CORES[name][edge] for channel, name in enumerate(CHANNELS))
        for edge in range(6)
    )


def rank_mod(matrix: list[list[int]], prime: int) -> int:
    """Return matrix rank over one prime field."""

    work = [[entry % prime for entry in row] for row in matrix]
    rows = len(work)
    columns = len(work[0])
    pivot_row = 0
    for column in range(columns):
        source = next((row for row in range(pivot_row, rows) if work[row][column]), None)
        if source is None:
            continue
        work[pivot_row], work[source] = work[source], work[pivot_row]
        inverse = pow(work[pivot_row][column], -1, prime)
        work[pivot_row] = [(entry * inverse) % prime for entry in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row:
                continue
            scale = work[row][column]
            if scale:
                work[row] = [
                    (left - scale * right) % prime
                    for left, right in zip(work[row], work[pivot_row], strict=True)
                ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def verify_gates_and_finite_slice_audit() -> dict[int, int]:
    """Check exact gates and stress-test the rank-one-free slice space."""

    assert linear_combination_of_cores((-1, -1, 1, 0, 1)) == (-1, 1, -1, 0, 0, 0)
    assert linear_combination_of_cores((-1, -1, 1, 1, 0)) == (-1, 0, 0, 1, -1, 0)
    assert linear_combination_of_cores((0, 0, 0, -1, 1)) == (0, 1, -1, -1, 1, 0)

    counts: dict[int, int] = {}
    for prime in (5, 7):
        checked = 0
        for a, b, c in product(range(prime), repeat=3):
            if (a, b, c) == (0, 0, 0):
                continue
            assert rank_mod([[0, c, b], [c, 0, a], [b, a, 0]], prime) >= 2
            checked += 1
        counts[prime] = checked
    assert counts == {5: 124, 7: 342}
    return counts


def main() -> None:
    """Run the independent exact audit."""

    verify_hashes()
    frame = verify_frame_and_determinants()
    lines = verify_lines_common_and_ordinary()
    cells = verify_common_cells()
    residuals = verify_companions_and_residuals()
    finite_counts = verify_gates_and_finite_slice_audit()

    print("co-two r=4 fixed-e=2 full-extension no-import audit: PASS")
    print(f"  frame/determinants={frame}")
    print(f"  exceptional ranks={lines}")
    print(f"  common-cell diagonal ranks={cells}")
    print(f"  companion residuals={residuals}")
    print(f"  finite slice audit counts={finite_counts} (AUDIT ONLY)")
    print("  fixed-e=2 representative 024 extension: EXCLUDED")
    print("  equality-five synthesis audit: PENDING")
    print("  unrestricted P6 -> Delta3: UNKNOWN")
    print("  global Krenn-Gu conjecture: UNRESOLVED")


if __name__ == "__main__":
    main()
