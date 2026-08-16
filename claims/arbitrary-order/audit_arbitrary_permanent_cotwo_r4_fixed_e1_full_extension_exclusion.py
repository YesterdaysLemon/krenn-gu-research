"""Independent no-import audit of the co-two fixed-e=1 exclusion.

This audit imports neither the primary verifier nor SymPy.  It rebuilds the
frame with rational linear algebra, uses a small independent polynomial ring
for the generic and deletion determinants, and separately stress-tests both
rank-one-free slice obstructions over two odd finite fields.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from itertools import combinations, permutations, product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
THEOREM = (
    HERE / "ARBITRARY_PERMANENT_COTWO_R4_FIXED_E1_FULL_EXTENSION_EXCLUSION_THEOREM.md"
)
PRIMARY = (
    HERE / "verify_arbitrary_permanent_cotwo_r4_fixed_e1_full_extension_exclusion.py"
)

THEOREM_SHA256 = "A7EE294986E79C7F1BC38E0B2CE0DC1A5EE09D230F2FD06796846D677A361ACF"
PRIMARY_SHA256 = "24A84558C6D842BC5D034DFCC6494C60A03C75CF8E5F47E2E63A6C3CCFEED2F8"

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

EDGES = tuple(combinations(range(4), 2))
CHANNELS = ("m1", "m2", "d0", "d1", "d2")

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


def columns_matrix(columns: list[tuple[int | Fraction, ...]]) -> RationalMatrix:
    """Build a row-major matrix from column vectors."""

    return as_fraction_matrix([list(row) for row in zip(*columns, strict=True)])


def rref(matrix: RationalMatrix) -> tuple[RationalMatrix, list[int]]:
    """Return exact reduced row-echelon form and pivot columns."""

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
    """Apply edge complementation in an independently rebuilt representation."""

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
    """Rebuild all nine products and five complement cores."""

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
    assert products[0, 2] == SOURCE["m1"]
    assert products[1, 2] == tuple(-entry for entry in SOURCE["m1"])
    assert products[2, 0] == SOURCE["m2"]
    assert products[2, 1] == tuple(-entry for entry in SOURCE["m2"])
    for name in CHANNELS:
        assert edge_complement(SOURCE[name]) == CORES[name]
    return {"mixed_rank": 2, "product_rank": 5}


def verify_symbolic_determinants() -> tuple[Polynomial, Polynomial]:
    """Recompute both generic determinants with a custom bivariate ring."""

    zero: Polynomial = {}
    p1 = (poly_linear(1, -1), poly_linear(1, 0), poly_linear(0, 1), zero)
    p2 = (poly_linear(1, 1), poly_linear(1, 0), zero, poly_linear(0, 1))
    first = polynomial_contraction_matrix(("m2", "d0", "d1", "d2"), p1)
    second = polynomial_contraction_matrix(("m1", "d0", "d1", "d2"), p2)
    first_expected = {(2, 2): -8, (1, 3): 8}
    second_expected = {(2, 2): 8, (1, 3): 8}
    assert polynomial_determinant(first) == first_expected
    assert polynomial_determinant(second) == second_expected
    return first_expected, second_expected


def verify_annihilator(low_name: str, expected_names: tuple[str, ...]) -> None:
    """Check one companion annihilator by dimension and direct pairing."""

    columns = contraction_columns(LINES[low_name])
    expected = [LINES[name] for name in expected_names]
    assert rank(columns_matrix(columns)) + len(expected) == 4
    assert rank(columns_matrix(expected)) == len(expected)
    for point in expected:
        assert all(dot(point, column) == 0 for column in columns)


def verify_kernel_and_annihilators() -> dict[str, int]:
    """Check all exceptional ranks, support relations, and annihilators."""

    expected_ranks = {"A": 3, "B": 3, "C": 3, "D": 3, "N": 2}
    for name, expected in expected_ranks.items():
        assert rank(columns_matrix(contraction_columns(LINES[name]))) == expected

    relations = {
        "A": ((1, 0, 0, 0, 0), (0, 0, 0, 0, 1)),
        "B": ((1, 0, 0, 0, 0), (0, 0, 1, 0, 0)),
        "C": ((0, 1, 0, 0, 0), (0, 0, 0, 0, 1)),
        "D": ((0, 1, 0, 0, 0), (0, 0, 1, 0, 0)),
        "N": ((1, 0, 0, 0, 0), (0, 1, 0, 0, 0), (0, 0, 0, 1, 0)),
    }
    for name, rows in relations.items():
        for coefficients in rows:
            assert relation(LINES[name], coefficients)

    verify_annihilator("A", ("A'",))
    verify_annihilator("B", ("B'",))
    verify_annihilator("C", ("C'",))
    verify_annihilator("D", ("D'",))
    verify_annihilator("N", ("R1", "R2"))
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


def diagonal_rank_on_cell(first_form: tuple[int, ...], second_form: tuple[int, ...]) -> int:
    """Compute the diagonal-core rank on one codimension-two cell."""

    basis = nullspace(as_fraction_matrix([list(first_form), list(second_form)]))
    assert len(basis) == 2
    rows = [
        list(restricted_core_row(CORES[name], basis[0], basis[1]))
        for name in ("d0", "d1", "d2")
    ]
    return rank(rows)


def verify_projection_drop_data() -> dict[str, object]:
    """Independently audit the common cells, dangerous square, and N identities."""

    h1 = (1, -1, 1, 0)
    h2 = (-1, 1, 0, 1)
    ranks = {
        "h1-x2": diagonal_rank_on_cell(h1, (0, 0, 1, 0)),
        "h1-h2": diagonal_rank_on_cell(h1, h2),
        "h2-x3": diagonal_rank_on_cell(h2, (0, 0, 0, 1)),
    }
    assert ranks == {"h1-x2": 2, "h1-h2": 3, "h2-x3": 2}

    s_basis = (1, 1, 0, 0)
    t_basis = (-1, 0, 1, -1)
    dangerous_rows = tuple(
        restricted_core_row(CORES[name], s_basis, t_basis)
        for name in ("d0", "d1", "d2")
    )
    assert dangerous_rows == (
        (Fraction(-1), Fraction(3), Fraction(-2)),
        (Fraction(0), Fraction(0), Fraction(2)),
        (Fraction(-1), Fraction(-1), Fraction(0)),
    )
    combined = tuple(
        4 * dangerous_rows[0][index]
        + 3 * dangerous_rows[1][index]
        + 4 * dangerous_rows[2][index]
        for index in range(3)
    )
    assert combined == (Fraction(-8), Fraction(8), Fraction(-2))

    n_columns = contraction_columns(LINES["N"])
    n_double = tuple(dot(LINES["N"], column) for column in n_columns)
    assert n_double == (0, 0, -2, 0, -2)
    return {"common_cell_ranks": ranks, "N_double_contractions": n_double}


def matrix_minor(
    matrix: list[list[Polynomial]], rows: tuple[int, ...], columns: tuple[int, ...]
) -> Polynomial:
    """Extract one polynomial minor."""

    return polynomial_determinant(
        [[matrix[row][column] for column in columns] for row in rows]
    )


def verify_common_companion_deletion() -> dict[str, tuple[int, int]]:
    """Audit the full and deleted rank loci for q=(-u,u,v,v)."""

    u = poly_linear(1, 0)
    v = poly_linear(0, 1)
    q = (poly_scale(u, -1), u, v, v)
    matrix = polynomial_contraction_matrix(CHANNELS, q)
    kept = (0, 1, 2, 4)
    nonzero: list[Polynomial] = []
    for rows in combinations(range(4), 3):
        for local_columns in combinations(range(4), 3):
            columns = tuple(kept[index] for index in local_columns)
            minor = matrix_minor(matrix, rows, columns)
            if minor:
                nonzero.append(minor)

    expected = poly_scale(
        poly_multiply(u, poly_multiply(poly_add(u, poly_scale(v, -1)), poly_add(u, v))),
        4,
    )
    assert len(nonzero) == 4
    assert all(minor in (expected, poly_scale(expected, -1)) for minor in nonzero)

    full_u_v2 = matrix_minor(matrix, (0, 2, 3), (0, 1, 3))
    full_u_u2_minus_v2 = matrix_minor(matrix, (0, 2, 3), (0, 1, 2))
    assert full_u_v2 == {(1, 2): -8}
    assert full_u_u2_minus_v2 == {(3, 0): -4, (1, 2): 4}

    def ranks_at(point: tuple[int, ...]) -> tuple[int, int]:
        columns = contraction_columns(point)
        return rank(columns_matrix(columns)), rank(
            columns_matrix([column for index, column in enumerate(columns) if index != 3])
        )

    rank_table = {
        "u0": ranks_at((0, 0, 1, 1)),
        "plus": ranks_at(LINES["Q+"]),
        "minus": ranks_at(LINES["Q-"]),
        "generic": ranks_at((-2, 2, 1, 1)),
    }
    assert rank_table == {
        "u0": (2, 2),
        "plus": (3, 2),
        "minus": (3, 2),
        "generic": (3, 3),
    }
    return rank_table


def verify_companions_and_residuals() -> tuple[str, ...]:
    """Check every endpoint filter and common residual covector."""

    filters = {
        "A'": ((0, 1, 1, 0, 0), (1, 0, 0, 1, 0)),
        "B'": ((1, 0, 0, 1, 0), (0, 1, 0, 0, 1)),
        "C'": ((1, 0, 1, 0, 0), (0, 1, 0, 1, 0)),
        "D'": ((0, 1, 0, 1, 0), (1, 0, 0, 0, 1)),
        "Q+": ((1, 0, 1, 0, 0), (1, 0, 0, 0, 1)),
        "Q-": ((0, 1, 1, 0, 0), (0, 1, 0, 0, 1)),
    }
    for name, rows in filters.items():
        for coefficients in rows:
            assert relation(LINES[name], coefficients)

    residuals = {
        "A-A'": ("A", "A'", (0, -1, -1, -1, 0), (0, 0, 0, 0, 1), (0, -2, 0, 0)),
        "B-B'": ("B", "B'", (0, -1, 0, -1, -1), (0, 0, 1, 0, 0), (2, 0, 0, 0)),
        "C-C'": ("C", "C'", (-1, 0, -1, -1, 0), (0, 0, 0, 0, 1), (0, 2, 0, 0)),
        "D-D'": ("D", "D'", (-1, 0, 0, -1, -1), (0, 0, -1, 0, 0), (2, 0, 0, 0)),
        "N-Q+": ("N", "Q+", (0, 0, -1, 0, 1), (-1, -1, 0, -1, 0), (0, 0, -2, 2)),
        "N-Q-": ("N", "Q-", (0, 0, -1, 0, 1), (-1, -1, 0, -1, 0), (0, 0, -2, 2)),
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


def verify_factor_gates_and_finite_slice_audits() -> dict[int, tuple[int, int]]:
    """Check exact gates and independently stress-test both slice arguments."""

    assert linear_combination_of_cores((1, 1, 1, 1, 0)) == (-1, 0, 0, 1, -1, 0)
    assert linear_combination_of_cores((1, 1, 0, 1, 1)) == (-1, -1, 1, 0, 0, 0)
    assert linear_combination_of_cores((0, 0, -1, 0, 1)) == (0, -1, 1, -1, 1, 0)

    counts: dict[int, tuple[int, int]] = {}
    for prime in (5, 7):
        matrix_checked = 0
        cube_checked = 0
        for a, b, c in product(range(prime), repeat=3):
            if (a, b, c) == (0, 0, 0):
                continue
            slice_matrix = [[0, c, b], [c, 0, a], [b, a, 0]]
            assert rank_mod(slice_matrix, prime) >= 2
            matrix_checked += 1

            pure_cube_coefficients = (pow(a, 3, prime), pow(b, 3, prime), pow(c, 3, prime))
            assert pure_cube_coefficients != (0, 0, 0)
            cube_checked += 1
        counts[prime] = (matrix_checked, cube_checked)
    assert counts == {5: (124, 124), 7: (342, 342)}
    return counts


def main() -> None:
    """Run the independent exact audit."""

    verify_hashes()
    frame = verify_frame_independently()
    determinants = verify_symbolic_determinants()
    exceptional = verify_kernel_and_annihilators()
    projection = verify_projection_drop_data()
    deletion = verify_common_companion_deletion()
    residuals = verify_companions_and_residuals()
    finite_counts = verify_factor_gates_and_finite_slice_audits()

    print("co-two r=4 fixed-e=1 full-extension no-import audit: PASS")
    print(f"  frame={frame}")
    print(f"  generic determinants={determinants}")
    print(f"  exceptional ranks={exceptional}")
    print(f"  projection-drop data={projection}")
    print(f"  common-companion deletion ranks={deletion}")
    print(f"  companion residuals={residuals}")
    print(f"  finite slice audit counts={finite_counts} (AUDIT ONLY)")
    print("  fixed-e=1 representative 025 extension: EXCLUDED")
    print("  fixed-e=2 representative 024: OPEN")
    print("  unrestricted P6 -> Delta3: UNKNOWN")
    print("  global Krenn-Gu conjecture: UNRESOLVED")


if __name__ == "__main__":
    main()
