"""Independent no-import audit of the co-two pure-star exclusion.

This audit imports neither the primary verifier nor SymPy.  It rebuilds the
frame with rational linear algebra, uses a small independent polynomial ring
for every determinant and deletion minor, and separately stress-tests the
rank-one-free slice obstruction over two odd finite fields.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from itertools import combinations, permutations, product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
THEOREM = HERE / "ARBITRARY_PERMANENT_COTWO_R4_PURE_STAR_FULL_EXTENSION_EXCLUSION_THEOREM.md"
PRIMARY = HERE / "verify_arbitrary_permanent_cotwo_r4_pure_star_full_extension_exclusion.py"

THEOREM_SHA256 = "E0B069B11107F006650954D339EF8E6E9465C2B492059450236F5238B2567CBC"
PRIMARY_SHA256 = "36C285C44BFA4D4C61FC084773F1604E398EBAC94E1AA8FD72E6BF5A8E1E6D49"

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

RationalMatrix = list[list[Fraction]]
Polynomial = dict[tuple[int, int], int]


def lf_sha256(path: Path) -> str:
    """Hash text after normalizing checkout CRLF to Git-blob LF."""

    return sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest().upper()


def verify_hashes() -> None:
    """Check the frozen theorem, primary replay, and predecessor interfaces."""

    expected = {THEOREM: THEOREM_SHA256, PRIMARY: PRIMARY_SHA256}
    expected.update({ROOT / relative: digest for relative, digest in DEPENDENCIES.items()})
    for path, digest in expected.items():
        actual = lf_sha256(path)
        assert actual == digest, (
            f"hash mismatch for {path}: expected {digest}, got {actual}"
        )


def as_fraction_matrix(rows: list[list[int | Fraction]]) -> RationalMatrix:
    """Convert a row-major matrix to exact fractions."""

    return [[Fraction(entry) for entry in row] for row in rows]


def transpose(matrix: RationalMatrix) -> RationalMatrix:
    """Transpose a nonempty row-major matrix."""

    return [list(column) for column in zip(*matrix, strict=True)]


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
    pivot_columns: list[int] = []
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
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == rows:
            break
    return work, pivot_columns


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
    """Apply edge complementation without using the primary representation."""

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

    if scalar == 0:
        return {}
    return {monomial: scalar * coefficient for monomial, coefficient in polynomial.items()}


def poly_multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    """Multiply two bivariate integer polynomials."""

    result: Polynomial = {}
    for (left_a, left_b), left_coefficient in left.items():
        for (right_a, right_b), right_coefficient in right.items():
            monomial = (left_a + right_a, left_b + right_b)
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

    size = len(matrix)
    result: Polynomial = {}
    for permutation in permutations(range(size)):
        term: Polynomial = {(0, 0): permutation_sign(permutation)}
        for row, column in enumerate(permutation):
            term = poly_multiply(term, matrix[row][column])
        result = poly_add(result, term)
    return result


def poly_linear(first: int, second: int) -> Polynomial:
    """Return first*u + second*v."""

    result: Polynomial = {}
    if first:
        result[(1, 0)] = first
    if second:
        result[(0, 1)] = second
    return result


def polynomial_contraction_matrix(
    core_names: tuple[str, ...], point: tuple[Polynomial, ...]
) -> list[list[Polynomial]]:
    """Build a row-major contraction matrix over the small polynomial ring."""

    columns: list[list[Polynomial]] = []
    for name in core_names:
        output: list[Polynomial] = [{}, {}, {}, {}]
        for coefficient, (left, right) in zip(CORES[name], EDGES, strict=True):
            output[right] = poly_add(output[right], poly_scale(point[left], coefficient))
            output[left] = poly_add(output[left], poly_scale(point[right], coefficient))
        columns.append(output)
    return [[columns[column][row] for column in range(len(columns))] for row in range(4)]


def verify_frame_independently() -> dict[str, int]:
    """Rebuild all nine products and the five Hodge-complement cores."""

    products = {(i, j): squarefree_product(U[i], V[j]) for i in range(3) for j in range(3)}
    mixed_columns = [products[i, j] for i in range(3) for j in range(3) if i != j]
    full_columns = [products[i, j] for i in range(3) for j in range(3)]
    assert rank(columns_matrix(mixed_columns)) == 2
    assert rank(columns_matrix(full_columns)) == 5
    assert products[0, 1] == SOURCE["m1"]
    assert products[1, 0] == SOURCE["m2"]
    assert products[0, 0] == SOURCE["d0"]
    assert products[1, 1] == SOURCE["d1"]
    assert products[2, 2] == SOURCE["d2"]
    for name in CHANNELS:
        assert edge_complement(SOURCE[name]) == CORES[name]
    return {"mixed_rank": 2, "product_rank": 5}


def verify_symbolic_determinants() -> Polynomial:
    """Recompute both generic determinants with a custom bivariate ring."""

    u = poly_linear(1, 0)
    v = poly_linear(0, 1)
    p1 = (u, u, v, v)
    p2 = (u, v, v, u)
    first = polynomial_contraction_matrix(("m2", "d0", "d1", "d2"), p1)
    second = polynomial_contraction_matrix(("m1", "d0", "d1", "d2"), p2)
    expected = {(3, 1): -64, (2, 2): 64}
    assert polynomial_determinant(first) == expected
    assert polynomial_determinant(second) == expected
    return expected


def verify_kernel_and_common_line() -> dict[str, int]:
    """Check exceptional ranks, support filters, and the impossible common line."""

    expected_ranks = {"A": 2, "B": 3, "C": 2, "D": 3, "N": 3}
    for name, expected in expected_ranks.items():
        assert rank(columns_matrix(contraction_columns(LINES[name]))) == expected

    relations = {
        "A": ((0, 1, 0, 1, 0), (0, 1, 0, 0, 1)),
        "B": ((0, 0, 1, 0, 0),),
        "C": ((1, 0, 1, 0, 0), (1, 0, 0, 0, 1)),
        "D": ((0, 0, 0, 1, 0),),
        "H": ((-1, 1, -1, 1, 0), (0, 1, -1, 0, 1)),
    }
    for name, rows in relations.items():
        for coefficients in rows:
            assert relation(LINES[name], coefficients)

    n_columns = contraction_columns(LINES["N"])
    assert all(dot(LINES["H"], column) == 0 for column in n_columns)
    assert rank(columns_matrix(n_columns)) + 1 == 4
    return expected_ranks


def restricted_core_row(
    core: tuple[int, ...], first: tuple[Fraction, ...], second: tuple[Fraction, ...]
) -> tuple[Fraction, Fraction, Fraction]:
    """Restrict one quadratic core to a two-dimensional rational plane."""

    uu = Fraction(0)
    uv = Fraction(0)
    vv = Fraction(0)
    for coefficient, (left, right) in zip(core, EDGES, strict=True):
        uu += coefficient * first[left] * first[right]
        uv += coefficient * (
            first[left] * second[right] + second[left] * first[right]
        )
        vv += coefficient * second[left] * second[right]
    return uu, uv, vv


def verify_common_cells_independently() -> tuple[int, int, int, int]:
    """Solve the four common cells with rational row reduction."""

    forms = {
        "A": (1, -1, 0, 0),
        "B": (0, 0, 1, -1),
        "C": (1, 0, 0, -1),
        "D": (0, 1, -1, 0),
    }
    results: list[int] = []
    for first_name, second_name in (("A", "C"), ("A", "D"), ("B", "C"), ("B", "D")):
        basis = nullspace(as_fraction_matrix([list(forms[first_name]), list(forms[second_name])]))
        assert len(basis) == 2
        rows = [
            list(restricted_core_row(CORES[name], basis[0], basis[1]))
            for name in ("d0", "d1", "d2")
        ]
        results.append(rank(rows))
    assert tuple(results) == (2, 2, 2, 1)
    return tuple(results)  # type: ignore[return-value]


def verify_annihilator(
    low_name: str, expected_basis_names: tuple[str, ...]
) -> None:
    """Check one companion annihilator by dimension and direct pairing."""

    columns = contraction_columns(LINES[low_name])
    expected = [LINES[name] for name in expected_basis_names]
    assert rank(columns_matrix(columns)) + len(expected) == 4
    assert rank(columns_matrix(expected)) == len(expected)
    for point in expected:
        assert all(dot(point, column) == 0 for column in columns)


def verify_deletion_monomials(
    point_coefficients: tuple[tuple[int, int], ...],
    deleted_channel: int,
    expected_monomial: tuple[int, int],
) -> None:
    """Check that every nonzero deletion minor is one expected monomial."""

    point = tuple(poly_linear(first, second) for first, second in point_coefficients)
    matrix = polynomial_contraction_matrix(CHANNELS, point)
    kept = [column for column in range(5) if column != deleted_channel]
    nonzero: list[Polynomial] = []
    for rows in combinations(range(4), 3):
        for columns in combinations(kept, 3):
            minor = polynomial_determinant(
                [[matrix[row][column] for column in columns] for row in rows]
            )
            if minor:
                nonzero.append(minor)
    assert nonzero
    for minor in nonzero:
        assert set(minor) == {expected_monomial}
        assert minor[expected_monomial] != 0


def verify_companions_independently() -> tuple[str, ...]:
    """Rebuild every annihilator, deletion locus, filter, and common covector."""

    verify_annihilator("A", ("C", "E"))
    verify_annihilator("B", ("F",))
    verify_annihilator("C", ("A", "E"))
    verify_annihilator("D", ("G",))

    # q=uC+vE; delete d1 and d2.
    verify_deletion_monomials(((0, 0), (1, 1), (1, 0), (0, 1)), 3, (1, 2))
    verify_deletion_monomials(((0, 0), (1, 1), (1, 0), (0, 1)), 4, (2, 1))
    # q=uA+vE; delete d0 and d2.
    verify_deletion_monomials(((0, 0), (0, 1), (1, 0), (1, 1)), 2, (1, 2))
    verify_deletion_monomials(((0, 0), (0, 1), (1, 0), (1, 1)), 4, (2, 1))

    filters = {
        "A": ((1, 0, 0, 0, 0), (0, 1, 0, 1, 0), (0, 1, 0, 0, 1)),
        "C": ((0, 1, 0, 0, 0), (1, 0, 1, 0, 0), (1, 0, 0, 0, 1)),
        "E": ((-1, 1, 0, 0, 0), (-1, 0, 1, 0, 0), (-1, 0, 0, 1, 0)),
        "F": ((0, -1, 0, 1, 0), (1, -1, 0, 0, 1)),
        "G": ((-1, 0, 1, 0, 0), (-1, 1, 0, 0, 1)),
    }
    for name, rows in filters.items():
        for coefficients in rows:
            assert relation(LINES[name], coefficients)

    cycles = {
        "A-C": ("A", "C", (0, -2, 1, 0, 0), (-2, 0, 0, 1, 0), (-4, 0, 0, 0)),
        "A-E": ("A", "E", (0, -2, 1, 0, 0), (2, 0, 0, 0, 1), (-4, 0, 0, 0)),
        "C-A": ("C", "A", (-2, 0, 0, 1, 0), (0, -2, 1, 0, 0), (-4, 0, 0, 0)),
        "C-E": ("C", "E", (-2, 0, 0, 1, 0), (2, 0, 0, 0, 1), (-4, 0, 0, 0)),
        "B-F": ("B", "F", (0, 2, 0, -1, -1), (0, 0, 2, 0, 0), (0, 0, 4, 4)),
        "D-G": ("D", "G", (2, 0, -1, 0, -1), (0, 0, 0, 2, 0), (0, 4, 4, 0)),
    }
    for low, companion, low_coefficients, companion_coefficients, expected in cycles.values():
        assert combine_columns(contraction_columns(LINES[low]), low_coefficients) == expected
        assert combine_columns(contraction_columns(LINES[companion]), companion_coefficients) == expected
    return tuple(cycles)


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
        source = next(
            (row for row in range(pivot_row, rows) if work[row][column]),
            None,
        )
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


def verify_factor_gates_and_finite_slice_audit() -> dict[int, int]:
    """Check exact factor gates and audit the rank-one-free slice over F_p."""

    assert linear_combination_of_cores((0, 0, 1, 1, 1)) == (-2, -2, -2, 0, 0, 0)
    assert linear_combination_of_cores((-1, 2, -2, -1, -1)) == (0, 4, 4, 0, 0, 0)
    assert linear_combination_of_cores((2, -1, -1, -2, -1)) == (4, 4, 0, 0, 0, 0)

    counts: dict[int, int] = {}
    for prime in (5, 7):
        checked = 0
        for a, b, c in product(range(prime), repeat=3):
            if (a, b, c) == (0, 0, 0):
                continue
            slice_matrix = [[0, c, b], [c, 0, a], [b, a, 0]]
            assert rank_mod(slice_matrix, prime) >= 2
            contraction_matrix_xuv = [[0, c, b], [c, 0, a], [b, a, 0]]
            assert rank_mod(contraction_matrix_xuv, prime) >= 2
            checked += 1
        counts[prime] = checked
    assert counts == {5: 124, 7: 342}
    return counts


def main() -> None:
    """Run the independent exact audit."""

    verify_hashes()
    frame = verify_frame_independently()
    determinant = verify_symbolic_determinants()
    exceptional = verify_kernel_and_common_line()
    common_cells = verify_common_cells_independently()
    cycles = verify_companions_independently()
    finite_counts = verify_factor_gates_and_finite_slice_audit()

    print("co-two r=4 pure-star full-extension no-import audit: PASS")
    print(f"  frame={frame}")
    print(f"  generic determinant={determinant}")
    print(f"  exceptional ranks={exceptional}")
    print(f"  common-cell diagonal ranks={common_cells}")
    print(f"  companion cycles={cycles}")
    print(f"  finite rank-one slice audit counts={finite_counts} (AUDIT ONLY)")
    print("  pure-star representative 014 extension: EXCLUDED")
    print("  fixed representatives 025 and 024: OPEN")
    print("  unrestricted P6 -> Delta3: UNKNOWN")
    print("  global Krenn-Gu conjecture: UNRESOLVED")


if __name__ == "__main__":
    main()
