"""Independent finite audit of same-pair survival and permanent dominance.

This standard-library-only program does not import the primary verifier,
project code, or a computer-algebra package.  It uses sparse tensor-word
dictionaries and direct injection/permutation enumeration to replay the
finite identities behind equations (6), (16)--(20), and (21)--(27) of the
owning theorem.  It also uses separately written ``Fraction`` Gaussian
elimination to check all asserted ranks.

The runs below are bounded exact audits.  They do not prove the theorem for
arbitrary root size, do not establish source-locus coverage, and do not
provide a legal downstream GLD target selector.
"""

from __future__ import annotations

import itertools
import json
from fractions import Fraction

Scalar = Fraction
Word = tuple[int, ...]
SparseTensor = dict[Word, Scalar]
Matrix = list[list[Scalar]]

COLOURS = tuple(range(3))
LOW_NAMES = ("a", "b", "c")


def add_sparse(left: SparseTensor, right: SparseTensor) -> SparseTensor:
    """Add two sparse tensors and remove exact zero entries."""
    result = left.copy()
    for word, coefficient in right.items():
        result[word] = result.get(word, Fraction(0)) + coefficient
        if result[word] == 0:
            del result[word]
    return result


def scale_sparse(coefficient: Scalar, tensor: SparseTensor) -> SparseTensor:
    """Scale a sparse tensor exactly."""
    if coefficient == 0:
        return {}
    return {
        word: coefficient * value
        for word, value in tensor.items()
        if coefficient * value != 0
    }


def pure_tensor(colour: int, port_count: int) -> SparseTensor:
    """Return the pure coordinate tensor on ``port_count`` ports."""
    return {(colour,) * port_count: Fraction(1)}


def dense_columns(tensors: list[SparseTensor]) -> Matrix:
    """Put sparse tensors into columns in a canonical union-of-words basis."""
    words = sorted(set().union(*(tensor.keys() for tensor in tensors)))
    return [[tensor.get(word, Fraction(0)) for tensor in tensors] for word in words]


def sparse_flattening_rank(tensor: SparseTensor, left_port_count: int) -> int:
    """Compute the exact rank of one tensor flattening from its word support."""
    left_words = sorted({word[:left_port_count] for word in tensor})
    right_words = sorted({word[left_port_count:] for word in tensor})
    matrix = [
        [tensor.get(left + right, Fraction(0)) for right in right_words]
        for left in left_words
    ]
    return fraction_rank(matrix)


def fraction_rank(matrix: Matrix) -> int:
    """Compute matrix rank by exact rational row reduction."""
    if not matrix:
        return 0
    work = [row[:] for row in matrix]
    row_count = len(work)
    column_count = len(work[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, row_count) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        work[pivot_row] = [value / pivot_value for value in work[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or work[row][column] == 0:
                continue
            multiplier = work[row][column]
            work[row] = [
                value - multiplier * pivot_entry
                for value, pivot_entry in zip(work[row], work[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def fraction_determinant(matrix: Matrix) -> Scalar:
    """Compute a square determinant by a distinct exact elimination pass."""
    size = len(matrix)
    assert all(len(row) == size for row in matrix)
    work = [row[:] for row in matrix]
    determinant = Fraction(1)
    for column in range(size):
        pivot = next((row for row in range(column, size) if work[row][column]), None)
        if pivot is None:
            return Fraction(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            determinant = -determinant
        pivot_value = work[column][column]
        determinant *= pivot_value
        for row in range(column + 1, size):
            if work[row][column] == 0:
                continue
            multiplier = work[row][column] / pivot_value
            for entry in range(column, size):
                work[row][entry] -= multiplier * work[column][entry]
    return determinant


def nullspace_basis(matrix: Matrix) -> list[list[Scalar]]:
    """Return an exact basis for the right kernel by rational RREF."""
    if not matrix:
        return []
    work = [row[:] for row in matrix]
    row_count = len(work)
    column_count = len(work[0])
    pivot_columns: list[int] = []
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, row_count) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        work[pivot_row] = [value / pivot_value for value in work[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or work[row][column] == 0:
                continue
            multiplier = work[row][column]
            work[row] = [
                value - multiplier * pivot_entry
                for value, pivot_entry in zip(work[row], work[pivot_row])
            ]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == row_count:
            break

    free_columns = [
        column for column in range(column_count) if column not in pivot_columns
    ]
    basis: list[list[Scalar]] = []
    for free in free_columns:
        vector = [Fraction(0) for _ in range(column_count)]
        vector[free] = Fraction(1)
        for row, pivot in reversed(list(enumerate(pivot_columns))):
            vector[pivot] = -sum(
                work[row][column] * vector[column] for column in free_columns
            )
        basis.append(vector)
    return basis


def permanent(matrix: Matrix) -> Scalar:
    """Evaluate a permanent by direct permutation enumeration."""
    size = len(matrix)
    assert all(len(row) == size for row in matrix)
    total = Fraction(0)
    for permutation in itertools.permutations(range(size)):
        term = Fraction(1)
        for row, column in enumerate(permutation):
            term *= matrix[row][column]
        total += term
    return total


def permanent_derivative(matrix: Matrix, direction: Matrix) -> Scalar:
    """Differentiate a permanent by the product rule in each permutation."""
    size = len(matrix)
    assert len(direction) == size
    assert all(len(row) == size for row in matrix)
    assert all(len(row) == size for row in direction)
    total = Fraction(0)
    for permutation in itertools.permutations(range(size)):
        for changed_row in range(size):
            term = direction[changed_row][permutation[changed_row]]
            for row in range(size):
                if row != changed_row:
                    term *= matrix[row][permutation[row]]
            total += term
    return total


def tensor_product_on_ports(
    factors: dict[int, SparseTensor], port_count: int
) -> SparseTensor:
    """Multiply one-port or consecutive-port sparse factors into a word tensor."""
    partial: dict[tuple[int, ...], Scalar] = {(): Fraction(1)}
    consumed = 0
    for start in sorted(factors):
        assert start == consumed
        factor = factors[start]
        next_partial: SparseTensor = {}
        for prefix, left_value in partial.items():
            for suffix, right_value in factor.items():
                word = prefix + suffix
                next_partial[word] = next_partial.get(word, Fraction(0)) + (
                    left_value * right_value
                )
        partial = next_partial
        consumed = len(next(iter(partial))) if partial else port_count
    assert consumed == port_count
    return partial


def triangle_source_words(modes: tuple[int, int, int]) -> dict[Word, list[str]]:
    """Enumerate the low-word sources in the three summands of (16)."""
    sources: dict[Word, list[str]] = {}
    for fixed_vertex in range(3):
        moving_vertices = [vertex for vertex in range(3) if vertex != fixed_vertex]
        for pair_colours in itertools.product(COLOURS, repeat=2):
            word = [0, 0, 0]
            word[fixed_vertex] = modes[fixed_vertex]
            for vertex, colour in zip(moving_vertices, pair_colours):
                word[vertex] = colour
            label = f"K_{LOW_NAMES[fixed_vertex]}:{pair_colours[0]}{pair_colours[1]}"
            sources.setdefault(tuple(word), []).append(label)
    return sources


def audit_triangle_forcing() -> dict[str, object]:
    """Replay the coordinate-line cover and pure-word isolation in (16)--(18)."""
    line_assignments = itertools.product(range(len(COLOURS) + 1), repeat=3)
    covers = [
        assignment
        for assignment in line_assignments
        if all(colour in assignment for colour in COLOURS)
    ]
    expected_covers = list(itertools.permutations(COLOURS))
    assert sorted(covers) == sorted(expected_covers)

    for modes in expected_covers:
        sources = triangle_source_words(modes)
        for colour in COLOURS:
            word = (colour, colour, colour)
            fixed_vertex = modes.index(colour)
            moving_pair = "".join(str(colour) for _ in range(2))
            expected = [f"K_{LOW_NAMES[fixed_vertex]}:{moving_pair}"]
            assert sources[word] == expected

    target_flattening_ranks: dict[int, int] = {}
    for high_port_count in range(2, 5):
        modes = (0, 1, 2)
        mu = (Fraction(2), Fraction(3), Fraction(5))
        h_values = (Fraction(7), Fraction(11), Fraction(13))
        high_tensors = [
            scale_sparse(
                mu[colour] / h_values[colour],
                pure_tensor(colour, high_port_count),
            )
            for colour in COLOURS
        ]

        assembled: SparseTensor = {}
        for fixed_vertex, colour in enumerate(modes):
            pair_vertices = [vertex for vertex in range(3) if vertex != fixed_vertex]
            pair_factor = {(colour, colour): h_values[colour]}
            low_factor: SparseTensor = {}
            for pair_word, coefficient in pair_factor.items():
                low_word = [0, 0, 0]
                low_word[fixed_vertex] = colour
                for vertex, entry in zip(pair_vertices, pair_word):
                    low_word[vertex] = entry
                low_factor[tuple(low_word)] = coefficient
            summand = tensor_product_on_ports(
                {0: low_factor, 3: high_tensors[fixed_vertex]},
                3 + high_port_count,
            )
            assembled = add_sparse(assembled, summand)

        target: SparseTensor = {}
        for colour in COLOURS:
            target = add_sparse(
                target,
                scale_sparse(mu[colour], pure_tensor(colour, 3 + high_port_count)),
            )
        assert assembled == target
        assert (
            fraction_rank(
                dense_columns(
                    [pure_tensor(colour, high_port_count) for colour in COLOURS]
                )
            )
            == 3
        )
        flattening_rank = sparse_flattening_rank(target, 3)
        assert flattening_rank == 3
        target_flattening_ranks[high_port_count] = flattening_rank

    return {
        "coordinate_line_covers": len(covers),
        "coordinate_line_covers_are_permutations": True,
        "pure_words_have_one_triangle_source": True,
        "sparse_equation_6_control": "exact",
        "high_pure_tensor_rank": 3,
        "target_flattening_ranks_by_high_port_count": target_flattening_ranks,
    }


def symmetric_kernel_matrix(vector: list[Scalar]) -> Matrix:
    """Build the equations defining S_b in (10)."""
    rows: Matrix = []
    for left, right in itertools.combinations(range(len(vector)), 2):
        row = [Fraction(0) for _ in vector]
        row[left] = vector[right]
        row[right] = vector[left]
        rows.append(row)
    return rows


def matrix_vector(matrix: Matrix, vector: list[Scalar]) -> list[Scalar]:
    """Multiply an exact matrix by a vector."""
    return [sum(entry * value for entry, value in zip(row, vector)) for row in matrix]


def cofactor_tensors(high_columns: list[list[list[Scalar]]]) -> list[SparseTensor]:
    """Enumerate the common cofactor tensors D_i in (19)."""
    root_count = len(high_columns[0])
    high_count = len(high_columns)
    result = [{} for _ in range(root_count)]
    for word in itertools.product(COLOURS, repeat=high_count):
        rectangular = [
            [high_columns[port][row][word[port]] for port in range(high_count)]
            for row in range(root_count)
        ]
        for deleted_row in range(root_count):
            square = [
                row[:]
                for row_index, row in enumerate(rectangular)
                if row_index != deleted_row
            ]
            result[deleted_row][word] = permanent(square)
    return result


def common_cofactor_image(
    alpha: list[Scalar], cofactors: list[SparseTensor]
) -> SparseTensor:
    """Evaluate Psi(alpha)=sum_i alpha_i D_i coefficientwise."""
    image: SparseTensor = {}
    for coefficient, cofactor in zip(alpha, cofactors):
        image = add_sparse(image, scale_sparse(coefficient, cofactor))
    return image


def rank_one_companion(
    alpha: list[Scalar],
    ell: list[Scalar],
    high_columns: list[list[list[Scalar]]],
) -> SparseTensor:
    """Directly enumerate the rank-one-column permanent in (16)."""
    root_count = len(alpha)
    high_count = len(high_columns)
    output: SparseTensor = {}
    for low_colour in COLOURS:
        low_column = [alpha[row] * ell[low_colour] for row in range(root_count)]
        for high_word in itertools.product(COLOURS, repeat=high_count):
            matrix = [
                [low_column[row]]
                + [
                    high_columns[port][row][high_word[port]]
                    for port in range(high_count)
                ]
                for row in range(root_count)
            ]
            output[(low_colour, *high_word)] = permanent(matrix)
    return output


def deterministic_high_columns(root_count: int) -> list[list[list[Scalar]]]:
    """Supply nonspecial exact high-mode columns for the finite replay."""
    return [
        [
            [
                Fraction(
                    (port + 2) * (row + 1) + (colour + 1) ** 2,
                    colour + 1,
                )
                for colour in COLOURS
            ]
            for row in range(root_count)
        ]
        for port in range(root_count - 1)
    ]


def audit_common_cofactor_and_kernel(root_count: int) -> dict[str, object]:
    """Replay (16), (19), (20), and the common-map rank contradiction."""
    high_columns = deterministic_high_columns(root_count)
    cofactors = cofactor_tensors(high_columns)
    alpha = [Fraction((-1) ** row * (row + 2), row + 1) for row in range(root_count)]
    ell = [Fraction(0), Fraction(1), Fraction(0)]
    direct = rank_one_companion(alpha, ell, high_columns)
    factored_image = common_cofactor_image(alpha, cofactors)
    factored = {
        (colour, *word): ell[colour] * coefficient
        for colour in COLOURS
        for word, coefficient in factored_image.items()
    }
    factored = {word: value for word, value in factored.items() if value}
    direct = {word: value for word, value in direct.items() if value}
    assert direct == factored

    support_audits = 0
    one_dimensional_cases = 0
    zero_dimensional_cases = 0
    for support_size in range(1, root_count + 1):
        for support in itertools.combinations(range(root_count), support_size):
            alpha_a = [Fraction(0) for _ in range(root_count)]
            for position in support:
                alpha_a[position] = Fraction((-1) ** position * (position + 1))
            kernel_matrix = symmetric_kernel_matrix(alpha_a)
            basis = nullspace_basis(kernel_matrix)
            expected_nullity = 1 if support_size <= 2 else 0
            assert len(basis) == expected_nullity
            assert fraction_rank(kernel_matrix) == root_count - expected_nullity
            support_audits += 1
            if not basis:
                zero_dimensional_cases += 1
                continue

            one_dimensional_cases += 1
            alpha_b = [Fraction(2) * entry for entry in basis[0]]
            alpha_c = [Fraction(-3) * entry for entry in basis[0]]
            assert matrix_vector(kernel_matrix, alpha_b) == [
                Fraction(0) for _ in kernel_matrix
            ]
            assert matrix_vector(kernel_matrix, alpha_c) == [
                Fraction(0) for _ in kernel_matrix
            ]
            k_b = common_cofactor_image(alpha_b, cofactors)
            k_c = common_cofactor_image(alpha_c, cofactors)
            assert fraction_rank(dense_columns([k_b, k_c])) <= 1

            high_port_count = root_count - 1
            pure_one = pure_tensor(1, high_port_count)
            pure_two = pure_tensor(2, high_port_count)
            assert fraction_rank(dense_columns([pure_one, pure_two])) == 2

    return {
        "root_count": root_count,
        "rank_one_companion_factorization": "exact on all high words",
        "symmetric_kernel_supports_checked": support_audits,
        "kernel_dimension_one_cases": one_dimensional_cases,
        "kernel_dimension_zero_cases": zero_dimensional_cases,
        "common_map_image_rank_bound": 1,
        "forced_distinct_pure_rank": 2,
    }


def delete_columns(matrix: Matrix, deleted: tuple[int, int]) -> Matrix:
    """Delete a complementary pair of columns from a rectangular matrix."""
    return [
        [entry for column, entry in enumerate(row) if column not in deleted]
        for row in matrix
    ]


def unit_direction(root_count: int, row: int, column: int) -> Matrix:
    """Return one coordinate tangent direction in Mat_(r x (r+2))."""
    return [
        [
            Fraction(1)
            if (current_row, current_column) == (row, column)
            else Fraction(0)
            for current_column in range(root_count + 2)
        ]
        for current_row in range(root_count)
    ]


def add_directions(*directions: tuple[Scalar, Matrix]) -> Matrix:
    """Form an exact linear combination of tangent directions."""
    row_count = len(directions[0][1])
    column_count = len(directions[0][1][0])
    return [
        [
            sum(
                coefficient * direction[row][column]
                for coefficient, direction in directions
            )
            for column in range(column_count)
        ]
        for row in range(row_count)
    ]


def phi_value(matrix: Matrix, pair: tuple[int, int]) -> Scalar:
    """Evaluate one complementary permanent coordinate of Phi_r."""
    return permanent(delete_columns(matrix, pair))


def phi_derivative(matrix: Matrix, pair: tuple[int, int], direction: Matrix) -> Scalar:
    """Evaluate one coordinate of d Phi_r by direct permutation enumeration."""
    return permanent_derivative(
        delete_columns(matrix, pair), delete_columns(direction, pair)
    )


def audit_phi(root_count: int) -> dict[str, object]:
    """Replay (21)--(27) and compute the exact differential rank."""
    column_a = root_count
    column_b = root_count + 1
    a_zero = [
        [
            Fraction(1)
            if column == row or column in (column_a, column_b)
            else Fraction(0)
            for column in range(root_count + 2)
        ]
        for row in range(root_count)
    ]
    all_outputs = list(itertools.combinations(range(root_count + 2), 2))

    assert phi_value(a_zero, (column_a, column_b)) == 1
    for row in range(root_count):
        assert phi_value(a_zero, (row, column_a)) == 1
        assert phi_value(a_zero, (row, column_b)) == 1
    for left, right in itertools.combinations(range(root_count), 2):
        assert phi_value(a_zero, (left, right)) == 2

    d_directions: dict[tuple[int, int], Matrix] = {}
    for left, right in itertools.combinations(range(root_count), 2):
        dx = unit_direction(root_count, left, right)
        da = unit_direction(root_count, left, column_a)
        db = unit_direction(root_count, left, column_b)
        d_directions[(left, right)] = add_directions(
            (Fraction(1), dx), (Fraction(-1), da), (Fraction(-1), db)
        )

    for intended_pair, direction in d_directions.items():
        for output in all_outputs:
            value = phi_derivative(a_zero, output, direction)
            expected = Fraction(-2) if output == intended_pair else Fraction(0)
            assert value == expected

    core_pairs = list(itertools.combinations(range(root_count), 2))
    ordered_outputs = (
        core_pairs
        + [(row, column_b) for row in range(root_count)]
        + [(row, column_a) for row in range(root_count)]
        + [(column_a, column_b)]
    )
    ordered_directions = (
        [d_directions[pair] for pair in core_pairs]
        + [unit_direction(root_count, row, column_a) for row in range(root_count)]
        + [unit_direction(root_count, row, column_b) for row in range(root_count)]
        + [unit_direction(root_count, 0, 0)]
    )
    minor = [
        [phi_derivative(a_zero, output, direction) for direction in ordered_directions]
        for output in ordered_outputs
    ]
    expected_size = len(all_outputs)
    assert len(minor) == expected_size
    assert all(len(row) == expected_size for row in minor)
    determinant = fraction_determinant(minor)
    expected_absolute = Fraction(2 ** len(core_pairs))
    assert abs(determinant) == expected_absolute
    assert fraction_rank(minor) == expected_size

    coordinate_directions = [
        unit_direction(root_count, row, column)
        for row in range(root_count)
        for column in range(root_count + 2)
    ]
    full_differential = [
        [
            phi_derivative(a_zero, output, direction)
            for direction in coordinate_directions
        ]
        for output in all_outputs
    ]
    full_rank = fraction_rank(full_differential)
    assert full_rank == expected_size

    return {
        "root_count": root_count,
        "source_dimension": root_count * (root_count + 2),
        "target_dimension": expected_size,
        "differential_rank": full_rank,
        "D_ij_isolation_count": len(core_pairs),
        "selected_minor_determinant": str(determinant),
        "selected_minor_absolute_determinant": str(abs(determinant)),
        "expected_absolute_determinant": str(expected_absolute),
    }


def main() -> None:
    """Run the independent bounded exact audit and emit a machine-readable ledger."""
    result = {
        "status": "AUDIT_PASS",
        "method": (
            "standard-library sparse tensor words, direct injection/permanent "
            "enumeration, and Fraction Gaussian elimination"
        ),
        "imports_primary_or_project_code": False,
        "imports_sympy": False,
        "triangle": audit_triangle_forcing(),
        "common_cofactor_and_kernel": [
            audit_common_cofactor_and_kernel(root_count) for root_count in range(2, 6)
        ],
        "complementary_permanent_differentials": [
            audit_phi(root_count) for root_count in range(2, 6)
        ],
        "arbitrary_r_proved_by_this_audit": False,
        "source_locus_coverage_proved_by_this_audit": False,
        "legal_GLD_target_selector_supplied": False,
        "global_conjecture_resolved": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
