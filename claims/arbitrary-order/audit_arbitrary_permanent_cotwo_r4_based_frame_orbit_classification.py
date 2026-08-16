"""Independent no-import audit of the co-two r=4 based-frame theorem.

This audit imports neither the primary verifier nor SymPy.  It reconstructs
the rational product tables and spanning tests with a standalone Fraction
row reducer, replays the finite permutation actions, checks every integral
frame, and independently enumerates the rank-one loci over F_5 and F_7.
The finite fields audit conventions only; the theorem's projective-chart
argument owns characteristic-zero completeness.
"""

from __future__ import annotations

from hashlib import sha256
from fractions import Fraction
from itertools import combinations, product as cartesian_product
from pathlib import Path

Vector = tuple[int, ...]
Basis = tuple[Vector, ...]
Point = tuple[Vector, Vector]
Permutation = tuple[int, ...]

HERE = Path(__file__).resolve().parent
THEOREM = HERE / "ARBITRARY_PERMANENT_COTWO_R4_BASED_FRAME_ORBIT_CLASSIFICATION_THEOREM.md"
PRIMARY = HERE / "verify_arbitrary_permanent_cotwo_r4_based_frame_orbit_classification.py"

THEOREM_SHA256 = "CFF044EA8E89D504F4ECF9C62CA55DFD5361CD54F5CB85083B09AED8B834D677"
PRIMARY_SHA256 = "8560C80C85ABC643A7591161295C22BF052589BCFC0529CA2A067A452CB1BAF1"

EDGES = tuple(combinations(range(4), 2))


def lf_normalized_sha256(path: Path) -> str:
    """Hash text after normalizing checkout CRLF to Git blob-style LF."""

    normalized = path.read_bytes().replace(b"\r\n", b"\n")
    return sha256(normalized).hexdigest().upper()


DATA = {
    "(3,1)": {
        "normals": ((1, 1, 1, 0), (1, -1, -1, 0)),
        "canonical": (
            ((0, 1, -1, 0), (0, 0, 0, 1), (-1, 0, 1, 0)),
            ((0, -1, 1, 0), (1, 1, 0, 0), (0, 0, 0, 1)),
        ),
        "equations": (
            (0, 0, 1, 1, 0, 0, 0, 0, 0),
            (0, 0, 0, 0, 0, 1, 0, 0, 0),
            (0, -1, 0, 0, 0, 0, 1, 0, 0),
            (0, 1, 0, 0, 0, 0, 0, 1, 0),
        ),
        "points": (
            ((0, 0, 1), (0, 0, 1)),
            ((0, 1, 0), (0, 1, 0)),
            ((1, 0, 0), (1, 0, 0)),
            ((1, 0, -1), (1, -1, 0)),
        ),
        "valid": ((0, 1, 2), (0, 1, 3)),
        "generators": ((0, 1, 3, 2),),
        "ordered_reps": ((0, 1, 2),),
        "ordered_sizes": (2,),
        "swap": (1, 0, 3, 2),
        "swap_reps": ((0, 1, 2),),
        "swap_sizes": (2,),
    },
    "(4,1)": {
        "normals": ((1, 1, 1, 1), (1, -1, -1, -1)),
        "canonical": (
            ((-1, 0, 1, 0), (1, 0, 0, -1), (0, 1, -1, 0)),
            ((1, 1, -1, 1), (1, 1, 0, 0), (0, -1, 1, 0)),
        ),
        "equations": (
            (0, 1, 1, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, 1, 0, 1, 0, 0, 0),
            (0, 2, 0, 1, 0, 0, 1, 0, 0),
            (0, 1, 0, 0, 0, 0, 0, 1, 0),
        ),
        "points": (
            ((0, 0, 1), (0, 0, 1)),
            ((0, 1, 0), (0, 1, 0)),
            ((0, 1, -1), (1, 0, -1)),
            ((1, 0, 0), (1, 0, 0)),
            ((1, 0, -1), (2, 1, -1)),
            ((1, -1, -1), (1, 1, -1)),
        ),
        "valid": (
            (0, 1, 3),
            (0, 1, 4),
            (0, 1, 5),
            (0, 2, 4),
            (0, 2, 5),
            (0, 3, 5),
            (0, 4, 5),
            (1, 2, 3),
            (1, 2, 4),
            (1, 3, 4),
            (1, 3, 5),
            (2, 3, 4),
            (2, 3, 5),
            (2, 4, 5),
        ),
        "generators": ((4, 1, 5, 3, 0, 2), (0, 4, 3, 2, 1, 5)),
        "ordered_reps": ((0, 1, 4), (0, 1, 3), (0, 2, 5), (2, 3, 5)),
        "ordered_sizes": (1, 6, 6, 1),
        "swap": (5, 3, 4, 1, 2, 0),
        "swap_reps": ((0, 1, 4), (0, 1, 3)),
        "swap_sizes": (2, 12),
    },
    "(4,2)": {
        "normals": ((1, 1, 1, 1), (1, 1, -1, -1)),
        "canonical": (
            ((1, 0, 0, -1), (0, 1, 0, -1), (0, 0, 1, -1)),
            ((0, 1, 1, 0), (1, 0, 1, 0), (0, 0, 1, -1)),
        ),
        "equations": (
            (0, -1, 1, 0, 0, 0, 0, 0, 0),
            (0, 0, 0, -1, 0, 1, 0, 0, 0),
            (0, 0, 0, 1, 0, 0, -1, 0, 0),
            (0, 1, 0, 0, 0, 0, 0, -1, 0),
        ),
        "points": (
            ((0, 0, 1), (0, 0, 1)),
            ((0, 1, 0), (0, 1, 0)),
            ((0, 1, 1), (1, 0, 1)),
            ((1, 0, 0), (1, 0, 0)),
            ((1, 0, 1), (0, 1, 1)),
            ((1, 1, 1), (1, 1, 1)),
        ),
        "valid": (
            (0, 1, 3),
            (0, 1, 5),
            (0, 2, 4),
            (0, 2, 5),
            (0, 3, 5),
            (0, 4, 5),
            (1, 2, 3),
            (1, 2, 4),
            (1, 3, 4),
            (1, 3, 5),
            (2, 3, 4),
            (2, 4, 5),
        ),
        "generators": (
            (0, 3, 4, 1, 2, 5),
            (5, 1, 4, 3, 2, 0),
            (3, 5, 2, 0, 4, 1),
        ),
        "ordered_reps": ((0, 1, 3), (0, 2, 5), (0, 2, 4)),
        "ordered_sizes": (4, 4, 4),
        "swap": (5, 3, 4, 1, 2, 0),
        "swap_reps": ((0, 1, 3), (0, 2, 5), (0, 2, 4)),
        "swap_sizes": (4, 4, 4),
    },
}


FRAMES = (
    (
        "(3,1)",
        "unique",
        (0, 1, 2),
        ((0, 1, -1, 0), (0, 0, 0, 1), (-1, 0, 1, 0)),
        ((0, -1, 1, 0), (1, 1, 0, 0), (0, 0, 0, 1)),
    ),
    (
        "(4,1)",
        "k=3",
        (0, 1, 4),
        ((1, -1, 0, 0), (1, 0, 0, -1), (1, 0, -1, 0)),
        ((1, -1, 1, 1), (1, 1, 1, -1), (1, 1, -1, 1)),
    ),
    (
        "(4,1)",
        "k=2 displayed",
        (0, 1, 3),
        ((-1, 0, 1, 0), (1, 0, 0, -1), (0, 1, -1, 0)),
        ((1, 1, -1, 1), (1, 1, 0, 0), (0, -1, 1, 0)),
    ),
    (
        "(4,1)",
        "k=1",
        (0, 2, 5),
        ((1, -1, -1, 1), (0, 0, 1, -1), (1, 0, -1, 0)),
        ((1, 0, 0, 1), (0, 0, 1, -1), (1, 1, 0, 0)),
    ),
    (
        "(4,1)",
        "k=0",
        (2, 3, 5),
        ((1, -1, 1, -1), (1, -1, -1, 1), (1, 1, -1, -1)),
        ((1, 0, 1, 0), (1, 0, 0, 1), (1, 1, 0, 0)),
    ),
    (
        "(4,2)",
        "e=0 displayed",
        (0, 1, 3),
        ((1, 0, 0, -1), (0, 1, 0, -1), (0, 0, 1, -1)),
        ((0, 1, 1, 0), (1, 0, 1, 0), (0, 0, 1, -1)),
    ),
    (
        "(4,2)",
        "e=1",
        (0, 2, 5),
        ((0, 1, -1, 0), (1, -1, 0, 0), (1, 0, 0, -1)),
        ((0, 1, 0, 1), (1, -1, 0, 0), (1, 0, 1, 0)),
    ),
    (
        "(4,2)",
        "e=2",
        (0, 2, 4),
        ((1, 1, -1, -1), (0, 1, 0, -1), (1, 0, 0, -1)),
        ((1, 1, 1, 1), (0, 1, 1, 0), (1, 0, 1, 0)),
    ),
)


def rational_rref(rows: list[list[Fraction]]) -> tuple[list[list[Fraction]], list[int]]:
    """Return standalone exact reduced row echelon form and pivot columns."""

    matrix = [row[:] for row in rows]
    if not matrix:
        return matrix, []
    pivot_row = 0
    pivots: list[int] = []
    for column in range(len(matrix[0])):
        selected = next(
            (row for row in range(pivot_row, len(matrix)) if matrix[row][column]),
            None,
        )
        if selected is None:
            continue
        matrix[pivot_row], matrix[selected] = matrix[selected], matrix[pivot_row]
        scale = matrix[pivot_row][column]
        matrix[pivot_row] = [value / scale for value in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row:
                continue
            coefficient = matrix[row][column]
            if coefficient:
                matrix[row] = [
                    value - coefficient * pivot
                    for value, pivot in zip(
                        matrix[row], matrix[pivot_row], strict=True
                    )
                ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return matrix, pivots


def rank(rows: list[Vector] | tuple[Vector, ...]) -> int:
    """Return exact rational row rank without third-party libraries."""

    if not rows:
        return 0
    _, pivots = rational_rref(
        [[Fraction(value) for value in row] for row in rows]
    )
    return len(pivots)


def solve_unique(rows: list[list[Fraction]], rhs: list[Fraction]) -> list[Fraction]:
    """Solve an exact overdetermined full-column-rank linear system."""

    augmented = [
        [*row, value] for row, value in zip(rows, rhs, strict=True)
    ]
    reduced, pivots = rational_rref(augmented)
    variables = len(rows[0])
    assert set(range(variables)).issubset(pivots)
    for row in reduced:
        if all(value == 0 for value in row[:variables]):
            assert row[-1] == 0
    solution = [Fraction(0) for _ in range(variables)]
    for row in reduced:
        pivot = next((index for index, value in enumerate(row[:variables]) if value), None)
        if pivot is not None:
            solution[pivot] = row[-1]
    return solution


def inverse(matrix: list[list[Fraction]]) -> list[list[Fraction]]:
    """Invert a three-by-three matrix by independent exact solves."""

    columns = [
        solve_unique(matrix, [Fraction(int(row == column)) for row in range(3)])
        for column in range(3)
    ]
    return [[columns[column][row] for column in range(3)] for row in range(3)]


def coordinates(frame: Basis, basis: Basis) -> list[list[Fraction]]:
    """Express the rows of one hyperplane basis in another."""

    system = [[Fraction(basis[column][row]) for column in range(3)] for row in range(4)]
    return [
        solve_unique(system, [Fraction(value) for value in frame_row])
        for frame_row in frame
    ]


def normalize_fraction(vector: list[Fraction] | tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    """Normalize a rational projective vector."""

    pivot = next(value for value in vector if value)
    return tuple(value / pivot for value in vector)


def square_free_product(left: Vector, right: Vector) -> Vector:
    """Multiply two linear forms in square-free degree two."""

    return tuple(
        left[i] * right[j] + left[j] * right[i] for i, j in EDGES
    )


def product_table(left: Basis, right: Basis) -> tuple[tuple[Vector, ...], ...]:
    """Return a three-by-three square-free product table."""

    return tuple(
        tuple(square_free_product(left_row, right_row) for right_row in right)
        for left_row in left
    )


def flatten(table: tuple[tuple[Vector, ...], ...]) -> list[Vector]:
    """Flatten a product table."""

    return [table[row][column] for row in range(3) for column in range(3)]


def group_closure(size: int, generators: tuple[Permutation, ...]) -> set[Permutation]:
    """Generate a finite permutation group."""

    identity = tuple(range(size))
    group = {identity}
    frontier = [identity]
    while frontier:
        current = frontier.pop()
        for generator in generators:
            composite = tuple(generator[current[index]] for index in range(size))
            if composite not in group:
                group.add(composite)
                frontier.append(composite)
    return group


def triple_orbit(triple: tuple[int, ...], group: set[Permutation]) -> set[frozenset[int]]:
    """Return an unordered colour-triple orbit."""

    return {frozenset(action[index] for index in triple) for action in group}


def finite_projective_points(prime: int) -> tuple[Vector, ...]:
    """Enumerate P^2(F_p) once in first-pivot normalization."""

    points: list[Vector] = []
    for pivot in range(3):
        for tail in cartesian_product(range(prime), repeat=2 - pivot):
            points.append((*(0 for _ in range(pivot)), 1, *tail))
    return tuple(points)


def normalize_mod(vector: Vector, prime: int) -> Vector:
    """Normalize a nonzero finite-field projective vector."""

    reduced = tuple(value % prime for value in vector)
    pivot = next(value for value in reduced if value)
    inverse_pivot = pow(pivot, -1, prime)
    return tuple(value * inverse_pivot % prime for value in reduced)


def finite_rank_one_locus(data: dict[str, object], prime: int) -> set[Point]:
    """Enumerate the bilinear zero locus over one audit field."""

    points = finite_projective_points(prime)
    equations = data["equations"]
    assert isinstance(equations, tuple)
    solutions: set[Point] = set()
    for left in points:
        for right in points:
            values = (
                sum(
                    equation[3 * i + j] * left[i] * right[j]
                    for i in range(3)
                    for j in range(3)
                )
                for equation in equations
            )
            if all(value % prime == 0 for value in values):
                solutions.add((left, right))
    return solutions


def audit_catalog(name: str, data: dict[str, object]) -> dict[str, object]:
    """Independently replay one catalog, its groups, and finite-field loci."""

    points = data["points"]
    valid_expected = data["valid"]
    assert isinstance(points, tuple)
    assert isinstance(valid_expected, tuple)
    equations = data["equations"]
    assert isinstance(equations, tuple)
    for left, right in points:
        assert all(
            sum(
                equation[3 * i + j] * left[i] * right[j]
                for i in range(3)
                for j in range(3)
            )
            == 0
            for equation in equations
        )

    valid = {
        indices
        for indices in combinations(range(len(points)), 3)
        if rank([points[index][0] for index in indices]) == 3
        and rank([points[index][1] for index in indices]) == 3
    }
    assert valid == set(valid_expected)

    generators = data["generators"]
    assert isinstance(generators, tuple)
    ordered_group = group_closure(len(points), generators)
    ordered_reps = data["ordered_reps"]
    ordered_sizes = data["ordered_sizes"]
    assert isinstance(ordered_reps, tuple)
    assert isinstance(ordered_sizes, tuple)
    ordered_orbits = [triple_orbit(rep, ordered_group) for rep in ordered_reps]
    assert tuple(map(len, ordered_orbits)) == ordered_sizes
    assert set().union(*ordered_orbits) == {frozenset(item) for item in valid}

    swap = data["swap"]
    assert isinstance(swap, tuple)
    swap_group = group_closure(len(points), (*generators, swap))
    swap_reps = data["swap_reps"]
    swap_sizes = data["swap_sizes"]
    assert isinstance(swap_reps, tuple)
    assert isinstance(swap_sizes, tuple)
    swap_orbits = [triple_orbit(rep, swap_group) for rep in swap_reps]
    assert tuple(map(len, swap_orbits)) == swap_sizes
    assert set().union(*swap_orbits) == {frozenset(item) for item in valid}

    finite_counts: dict[int, int] = {}
    for prime in (5, 7):
        observed = finite_rank_one_locus(data, prime)
        expected = {
            (normalize_mod(left, prime), normalize_mod(right, prime))
            for left, right in points
        }
        assert observed == expected
        finite_counts[prime] = len(observed)

    return {
        "type": name,
        "rank_one_points": len(points),
        "valid_triples": len(valid),
        "ordered_orbits": ordered_sizes,
        "swap_orbits": swap_sizes,
        "finite_audit_counts": finite_counts,
    }


def audit_frame(frame: tuple[object, ...]) -> dict[str, object]:
    """Replay one integral frame and recover its paired dual points."""

    name, label, expected_indices, left, right = frame
    assert isinstance(name, str)
    assert isinstance(label, str)
    assert isinstance(expected_indices, tuple)
    assert isinstance(left, tuple)
    assert isinstance(right, tuple)
    data = DATA[name]
    normals = data["normals"]
    canonical = data["canonical"]
    points = data["points"]
    assert isinstance(normals, tuple)
    assert isinstance(canonical, tuple)
    assert isinstance(points, tuple)
    assert rank(left) == rank(right) == 3
    assert all(sum(a * b for a, b in zip(row, normals[0], strict=True)) == 0 for row in left)
    assert all(sum(a * b for a, b in zip(row, normals[1], strict=True)) == 0 for row in right)

    table = product_table(left, right)
    mixed = [table[i][j] for i in range(3) for j in range(3) if i != j]
    diagonal = [table[i][i] for i in range(3)]
    assert rank(mixed) == 2
    assert rank(flatten(table)) == 5
    assert rank([*mixed, *diagonal]) == 5

    left_change = coordinates(left, canonical[0])
    right_change = coordinates(right, canonical[1])
    left_duals = inverse(left_change)
    right_duals = inverse(right_change)
    observed_indices: list[int] = []
    for colour in range(3):
        paired = (
            normalize_fraction([left_duals[row][colour] for row in range(3)]),
            normalize_fraction([right_duals[row][colour] for row in range(3)]),
        )
        observed_indices.append(
            next(
                index
                for index, point in enumerate(points)
                if paired
                == (
                    normalize_fraction(tuple(map(Fraction, point[0]))),
                    normalize_fraction(tuple(map(Fraction, point[1]))),
                )
            )
        )
    assert frozenset(observed_indices) == frozenset(expected_indices)
    return {
        "type": name,
        "label": label,
        "points": tuple(sorted(observed_indices)),
    }


def audit_theorem_boundary() -> None:
    """Require the theorem to preserve the exact nontransport boundary."""

    assert lf_normalized_sha256(THEOREM) == THEOREM_SHA256
    assert lf_normalized_sha256(PRIMARY) == PRIMARY_SHA256
    text = THEOREM.read_text(encoding="utf-8")
    required = (
        "ordered-pair based-frame orbit counts:                  1,4,3;",
        "counts after optional omitted-mode exchange:            1,2,3;",
        "every (3,1) frame transports to its displayed frame:    YES;",
        "every (4,1) frame transports to its displayed frame:    NO;",
        "every (4,2) frame transports to its displayed frame:    NO;",
        "global Krenn--Gu conjecture:                            UNRESOLVED.",
    )
    assert all(marker in text for marker in required)


def main() -> None:
    """Run the independent exact and finite-field audits."""

    audit_theorem_boundary()
    catalogs = [audit_catalog(name, data) for name, data in DATA.items()]
    frames = [audit_frame(frame) for frame in FRAMES]
    print("co-two r=4 based-frame orbit classification no-import audit: PASS")
    print(f"  catalogs={catalogs}")
    print(f"  frames={frames}")
    print("  finite fields: AUDIT ONLY")
    print("  full-extension transport: NOT CLAIMED")
    print("  global Krenn-Gu conjecture: UNRESOLVED")


if __name__ == "__main__":
    main()
