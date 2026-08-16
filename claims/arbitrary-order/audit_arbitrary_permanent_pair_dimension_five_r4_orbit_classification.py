"""Independent no-import audit of the r=4 pair orbit classification.

This script intentionally does not import the primary verifier and does not
use SymPy.  It combines exact integer table checks with a complete finite
field audit over F_5 of all projective hyperplane-normal pairs and all
projective rank-one members of the five canonical multiplication-dual
spaces.  The finite-field exhaustion audits the case split; the theorem
document supplies the characteristic-zero proof.
"""

from __future__ import annotations

from itertools import combinations, permutations, product

Vector = tuple[int, ...]
Table = tuple[tuple[Vector, ...], ...]

PRIME = 5
EDGES = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))


def modular_rank(rows: list[list[int]] | list[Vector], prime: int = PRIME) -> int:
    """Compute row rank with a standalone modular Gaussian reducer."""
    matrix = [[entry % prime for entry in row] for row in rows]
    if not matrix:
        return 0
    row_count = len(matrix)
    column_count = len(matrix[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, row_count) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        inverse = pow(matrix[pivot_row][column], -1, prime)
        matrix[pivot_row] = [(value * inverse) % prime for value in matrix[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or not matrix[row][column]:
                continue
            multiple = matrix[row][column]
            matrix[row] = [
                (value - multiple * pivot_value) % prime
                for value, pivot_value in zip(
                    matrix[row], matrix[pivot_row], strict=True
                )
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def bareiss_determinant(matrix: list[list[int]]) -> int:
    """Compute an integer determinant by fraction-free elimination."""
    size = len(matrix)
    if size == 0:
        return 1
    work = [row[:] for row in matrix]
    sign = 1
    previous = 1
    for pivot_index in range(size - 1):
        pivot_row = next(
            (
                row
                for row in range(pivot_index, size)
                if work[row][pivot_index] != 0
            ),
            None,
        )
        if pivot_row is None:
            return 0
        if pivot_row != pivot_index:
            work[pivot_index], work[pivot_row] = work[pivot_row], work[pivot_index]
            sign *= -1
        pivot = work[pivot_index][pivot_index]
        for row in range(pivot_index + 1, size):
            for column in range(pivot_index + 1, size):
                numerator = (
                    work[row][column] * pivot
                    - work[row][pivot_index] * work[pivot_index][column]
                )
                if numerator % previous:
                    raise AssertionError("Bareiss division was not exact")
                work[row][column] = numerator // previous
        previous = pivot
        for row in range(pivot_index + 1, size):
            work[row][pivot_index] = 0
    return sign * work[-1][-1]


def integer_rank(rows: list[Vector] | tuple[Vector, ...]) -> int:
    """Compute rational rank by finding a nonzero integer minor."""
    if not rows:
        return 0
    row_count = len(rows)
    column_count = len(rows[0])
    for size in range(min(row_count, column_count), 0, -1):
        for row_indices in combinations(range(row_count), size):
            for column_indices in combinations(range(column_count), size):
                minor = [
                    [rows[row][column] for column in column_indices]
                    for row in row_indices
                ]
                if bareiss_determinant(minor):
                    return size
    return 0


def normalize_projective(vector: Vector, prime: int = PRIME) -> Vector:
    """Normalize a nonzero finite-field vector at its first nonzero entry."""
    first = next(value % prime for value in vector if value % prime)
    inverse = pow(first, -1, prime)
    return tuple((value * inverse) % prime for value in vector)


def projective_vectors(dimension: int, prime: int = PRIME) -> tuple[Vector, ...]:
    """List every projective point exactly once."""
    points = {
        normalize_projective(tuple(vector), prime)
        for vector in product(range(prime), repeat=dimension)
        if any(vector)
    }
    return tuple(sorted(points))


def hyperplane_basis(normal: Vector, prime: int = PRIME) -> tuple[Vector, ...]:
    """Construct a basis of the kernel of one projective covector."""
    pivot = next(index for index, value in enumerate(normal) if value % prime)
    inverse = pow(normal[pivot] % prime, -1, prime)
    basis = []
    for free in range(4):
        if free == pivot:
            continue
        vector = [0, 0, 0, 0]
        vector[free] = 1
        vector[pivot] = (-normal[free] * inverse) % prime
        basis.append(tuple(vector))
    assert modular_rank([list(row) for row in basis], prime) == 3
    return tuple(basis)


def quadratic_product(left: Vector, right: Vector, modulus: int | None = None) -> Vector:
    """Multiply degree-one forms in the square-free algebra."""
    entries = tuple(
        left[first] * right[second] + left[second] * right[first]
        for first, second in EDGES
    )
    if modulus is None:
        return entries
    return tuple(value % modulus for value in entries)


def product_table(
    left: tuple[Vector, ...],
    right: tuple[Vector, ...],
    modulus: int | None = None,
) -> Table:
    """Return a three-by-three quadratic product table."""
    return tuple(
        tuple(quadratic_product(u, v, modulus) for v in right) for u in left
    )


def flatten_table(table: Table) -> list[Vector]:
    """Flatten a three-by-three product table."""
    return [table[row][column] for row in range(3) for column in range(3)]


def classify_normal_pair(alpha: Vector, beta: Vector) -> str:
    """Classify a finite-field equality-five normal pair from its ratios."""
    support_alpha = tuple(index for index, value in enumerate(alpha) if value)
    support_beta = tuple(index for index, value in enumerate(beta) if value)
    if alpha == beta:
        assert len(support_alpha) == 3
        return "P3"
    assert support_alpha == support_beta
    ratios = [
        beta[index] * pow(alpha[index], -1, PRIME) % PRIME
        for index in support_alpha
    ]
    base_inverse = pow(ratios[0], -1, PRIME)
    relative = [(ratio * base_inverse) % PRIME for ratio in ratios]
    assert all(value in (1, PRIME - 1) for value in relative)
    plus = relative.count(1)
    minus = relative.count(PRIME - 1)
    assert plus and minus
    size = len(relative)
    split = min(plus, minus)
    return f"({size},{split})"


def audit_all_normal_pairs() -> dict[str, int]:
    """Exhaust every ordered pair of projective hyperplane normals over F_5."""
    normals = projective_vectors(4)
    assert len(normals) == 156
    counts = {"P3": 0, "(2,1)": 0, "(3,1)": 0, "(4,1)": 0, "(4,2)": 0}
    equality_pairs = 0
    for alpha in normals:
        left = hyperplane_basis(alpha)
        for beta in normals:
            right = hyperplane_basis(beta)
            table = product_table(left, right, PRIME)
            if modular_rank(flatten_table(table)) != 5:
                continue
            label = classify_normal_pair(alpha, beta)
            counts[label] += 1
            equality_pairs += 1
    expected = {"P3": 64, "(2,1)": 24, "(3,1)": 192, "(4,1)": 256, "(4,2)": 192}
    assert counts == expected
    assert equality_pairs == 728
    return counts


def independent_matrix_basis(table: Table) -> list[Vector]:
    """Extract a basis of the multiplication-dual space over F_5."""
    edge_matrices = [
        tuple(table[row][column][edge] for row in range(3) for column in range(3))
        for edge in range(6)
    ]
    basis: list[Vector] = []
    for matrix in edge_matrices:
        if modular_rank([*basis, matrix]) > len(basis):
            basis.append(matrix)
    assert len(basis) == 5
    return basis


def matrix_from_combination(coefficients: Vector, basis: list[Vector]) -> Vector:
    """Form one flattened dual matrix over F_5."""
    return tuple(
        sum(coefficient * matrix[index] for coefficient, matrix in zip(
            coefficients, basis, strict=True
        ))
        % PRIME
        for index in range(9)
    )


def rank_one_factors(matrix: Vector) -> tuple[Vector, Vector]:
    """Factor a nonzero rank-one 3 by 3 matrix over F_5."""
    rows = [list(matrix[3 * row : 3 * row + 3]) for row in range(3)]
    assert modular_rank(rows) == 1
    pivot_column = next(
        column for column in range(3) if any(rows[row][column] for row in range(3))
    )
    left = tuple(rows[row][pivot_column] for row in range(3))
    pivot_row = next(row for row in range(3) if left[row])
    inverse = pow(left[pivot_row], -1, PRIME)
    right = tuple(rows[pivot_row][column] * inverse % PRIME for column in range(3))
    reconstructed = tuple(
        left[row] * right[column] % PRIME
        for row in range(3)
        for column in range(3)
    )
    assert reconstructed == matrix
    return normalize_projective(left), normalize_projective(right)


def enumerate_rank_one_locus(table: Table) -> tuple[tuple[Vector, Vector], ...]:
    """Enumerate every projective rank-one point in a five-space L."""
    basis = independent_matrix_basis(table)
    points = []
    for coefficients in projective_vectors(5):
        matrix = matrix_from_combination(coefficients, basis)
        rows = [list(matrix[3 * row : 3 * row + 3]) for row in range(3)]
        if modular_rank(rows) == 1:
            points.append(rank_one_factors(matrix))
    return tuple(points)


def has_bispanning_triple(points: tuple[tuple[Vector, Vector], ...]) -> bool:
    """Test the rank-one criterion by exhaustive triples."""
    for triple in combinations(points, 3):
        left = [point[0] for point in triple]
        right = [point[1] for point in triple]
        if modular_rank(left) == modular_rank(right) == 3:
            return True
    return False


def canonical_frames() -> dict[str, tuple[tuple[Vector, ...], tuple[Vector, ...]]]:
    """Return independent explicit frames for the five orbit representatives."""
    return {
        "P3": (
            ((-1, 1, 0, 0), (-1, 0, 1, 0), (0, 0, 0, 1)),
            ((-1, 1, 0, 0), (-1, 0, 1, 0), (0, 0, 0, 1)),
        ),
        "(2,1)": (
            ((-1, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)),
            ((1, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)),
        ),
        "(3,1)": (
            ((0, 1, -1, 0), (0, 0, 0, 1), (-1, 0, 1, 0)),
            ((0, -1, 1, 0), (1, 1, 0, 0), (0, 0, 0, 1)),
        ),
        "(4,1)": (
            ((-1, 0, 1, 0), (1, 0, 0, -1), (0, 1, -1, 0)),
            ((1, 1, -1, 1), (1, 1, 0, 0), (0, -1, 1, 0)),
        ),
        "(4,2)": (
            ((1, 0, 0, -1), (0, 1, 0, -1), (0, 0, 1, -1)),
            ((0, 1, 1, 0), (1, 0, 1, 0), (0, 0, 1, -1)),
        ),
    }


def audit_rank_one_criterion() -> dict[str, int]:
    """Independently exhaust each canonical rank-one locus over F_5."""
    expected = {
        "P3": False,
        "(2,1)": False,
        "(3,1)": True,
        "(4,1)": True,
        "(4,2)": True,
    }
    sizes: dict[str, int] = {}
    for label, (left, right) in canonical_frames().items():
        table = product_table(left, right, PRIME)
        points = enumerate_rank_one_locus(table)
        sizes[label] = len(points)
        assert has_bispanning_triple(points) is expected[label]
    return sizes


def graph_degrees(edge_vector: Vector) -> Vector:
    """Compute a support graph degree multiset."""
    degrees = [0, 0, 0, 0]
    for coefficient, (first, second) in zip(edge_vector, EDGES, strict=True):
        if coefficient:
            degrees[first] += 1
            degrees[second] += 1
    return tuple(sorted(degrees, reverse=True))


def dot(left: Vector, right: Vector) -> int:
    """Return an integer dot product."""
    return sum(a * b for a, b in zip(left, right, strict=True))


def audit_integer_tables() -> dict[str, Vector]:
    """Replay all exact product ranks and graph separators over the integers."""
    expected_annihilators = {
        "P3": (0, 0, 1, 0, 1, 1),
        "(2,1)": (1, 0, 0, 0, 0, 0),
        "(3,1)": (1, 1, 0, 0, 0, 0),
        "(4,1)": (1, 1, 1, 0, 0, 0),
        "(4,2)": (0, 1, 1, 1, 1, 0),
    }
    expected_degrees = {
        "P3": (3, 1, 1, 1),
        "(2,1)": (1, 1, 0, 0),
        "(3,1)": (2, 1, 1, 0),
        "(4,1)": (3, 1, 1, 1),
        "(4,2)": (2, 2, 2, 2),
    }
    for label, (left, right) in canonical_frames().items():
        table = product_table(left, right)
        products = flatten_table(table)
        annihilator = expected_annihilators[label]
        assert integer_rank(products) == 5
        assert all(dot(vector, annihilator) == 0 for vector in products)
        assert graph_degrees(annihilator) == expected_degrees[label]
        if label in {"(3,1)", "(4,1)", "(4,2)"}:
            mixed = [
                table[row][column]
                for row, column in permutations(range(3), 2)
            ]
            diagonal = [table[index][index] for index in range(3)]
            assert integer_rank(mixed) == 2
            assert integer_rank([*mixed, *diagonal]) == 5
    return expected_annihilators


def main() -> None:
    """Run the independent finite-field and integer audits."""
    counts = audit_all_normal_pairs()
    rank_one_sizes = audit_rank_one_criterion()
    annihilators = audit_integer_tables()
    print("PASS: independent no-import r=4 pair orbit audit")
    print("F5_projective_normal_pairs=24336")
    print(f"F5_equality_five_counts={counts}")
    print(f"F5_rank_one_locus_sizes={rank_one_sizes}")
    print("F5_bispanning_types=(3,1),(4,1),(4,2)")
    print(f"integer_annihilators={annihilators}")


if __name__ == "__main__":
    main()
