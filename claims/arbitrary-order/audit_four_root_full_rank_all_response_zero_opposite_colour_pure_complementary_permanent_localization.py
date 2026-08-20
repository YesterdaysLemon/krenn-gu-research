"""Independent exact audit of the four-root full-rank response-zero theorem.

This script uses only the Python standard library and imports no repository
code.  It was derived from the theorem statement, not from the focused primary
verifier.  Its representations deliberately differ from the written proof:

* ``Fraction`` Gaussian elimination checks the rank-three and projected-rank
  mechanisms;
* labelled perfect matchings reconstruct the four- and six-vertex hafnians;
* Boolean support masks and signed-incidence matrices check the support/sign
  classification;
* explicit torus-zero searches audit the maximum-root coordinate forcing;
* a root-to-port permanent and a separate ten-vertex matching recurrence
  reconstruct the off-target fixture.

The finite tables below are an independent replay, not a proof of the
arbitrary-point theorem, not an ideal saturation, and not evidence that the
surviving opposite-colour pure-permanent locus meets or misses the witness
locus.  The written coordinate-free arguments and the complete GHZ identity
remain load-bearing.  The determinant-zero divisor and every nonzero-response
absorption branch remain unaudited and open.
"""

from fractions import Fraction
from itertools import combinations, permutations, product

Scalar = Fraction
Vector = tuple[Scalar, ...]
Matrix = tuple[tuple[Scalar, ...], ...]
Matching = tuple[tuple[str, str], ...]

COLORS = range(3)
PORTS = range(4)
ZERO = Fraction(0)
ONE = Fraction(1)


def vector(*entries: int | Fraction) -> Vector:
    """Return an exact rational vector."""
    return tuple(Fraction(entry) for entry in entries)


def zero_matrix(rows: int = 3, columns: int = 3) -> Matrix:
    """Return a zero matrix."""
    return tuple(tuple(ZERO for _ in range(columns)) for _ in range(rows))


def identity_matrix(size: int = 3) -> Matrix:
    """Return the exact identity matrix."""
    return tuple(
        tuple(ONE if row == column else ZERO for column in range(size))
        for row in range(size)
    )


def matrix_unit(
    row: int,
    column: int,
    coefficient: int | Fraction = 1,
) -> Matrix:
    """Return a three-by-three matrix unit."""
    value = Fraction(coefficient)
    return tuple(
        tuple(value if (i, j) == (row, column) else ZERO for j in COLORS)
        for i in COLORS
    )


def transpose(matrix: Matrix) -> Matrix:
    """Transpose a matrix."""
    return tuple(
        tuple(matrix[i][j] for i in range(len(matrix))) for j in range(len(matrix[0]))
    )


def matrix_add(*matrices: Matrix) -> Matrix:
    """Add equally sized matrices."""
    rows = len(matrices[0])
    columns = len(matrices[0][0])
    return tuple(
        tuple(sum((matrix[i][j] for matrix in matrices), ZERO) for j in range(columns))
        for i in range(rows)
    )


def matrix_scale(coefficient: int | Fraction, matrix: Matrix) -> Matrix:
    """Scale a matrix exactly."""
    scalar = Fraction(coefficient)
    return tuple(tuple(scalar * entry for entry in row) for row in matrix)


def outer(left: Vector, right: Vector) -> Matrix:
    """Return an exact outer product."""
    return tuple(tuple(a * b for b in right) for a in left)


def dot(left: Vector, right: Vector) -> Scalar:
    """Return an exact dot product."""
    return sum((a * b for a, b in zip(left, right, strict=True)), ZERO)


def bilinear(matrix: Matrix, left: Vector, right: Vector) -> Scalar:
    """Evaluate a labelled bilinear block."""
    return sum(
        (
            left[i] * matrix[i][j] * right[j]
            for i in range(len(left))
            for j in range(len(right))
        ),
        ZERO,
    )


def matrix_rank(matrix: Matrix | tuple[Vector, ...]) -> int:
    """Compute rank by independently implemented Fraction row reduction."""
    if not matrix:
        return 0
    work = [list(map(Fraction, row)) for row in matrix]
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
        work[pivot_row] = [entry / pivot_value for entry in work[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                entry - factor * pivot_entry
                for entry, pivot_entry in zip(work[row], work[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def perfect_matchings(vertices: tuple[str, ...]) -> tuple[Matching, ...]:
    """Enumerate labelled perfect matchings by a vertex-deletion recurrence."""
    if not vertices:
        return ((),)
    first = vertices[0]
    result: list[Matching] = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        remainder = vertices[1:index] + vertices[index + 1 :]
        for matching in perfect_matchings(remainder):
            result.append(((first, second),) + matching)
    return tuple(result)


def block_for(
    blocks: dict[tuple[str, str], Matrix],
    left: str,
    right: str,
) -> Matrix:
    """Read an oriented labelled edge block, transposing on reversal."""
    if (left, right) in blocks:
        return blocks[left, right]
    if (right, left) in blocks:
        return transpose(blocks[right, left])
    return zero_matrix()


def response_tensor(
    h_block: Matrix,
    b_block: Matrix,
    a_u: Matrix,
    a_v: Matrix,
    c_u: Matrix,
    c_v: Matrix,
) -> tuple[Scalar, ...]:
    """Evaluate the labelled coefficient formula in slot order q0,q1,u,v."""
    return tuple(
        h_block[a][b] * b_block[s][t] + a_u[a][s] * c_v[b][t] + a_v[a][t] * c_u[b][s]
        for a, b, s, t in product(COLORS, repeat=4)
    )


def response_by_matchings(
    h_block: Matrix,
    b_block: Matrix,
    a_u: Matrix,
    a_v: Matrix,
    c_u: Matrix,
    c_v: Matrix,
) -> tuple[Scalar, ...]:
    """Reconstruct the same four-slot tensor from its three matchings."""
    blocks = {
        ("q0", "q1"): h_block,
        ("q0", "u"): a_u,
        ("q0", "v"): a_v,
        ("q1", "u"): c_u,
        ("q1", "v"): c_v,
        ("u", "v"): b_block,
    }
    vertices = ("q0", "q1", "u", "v")
    matchings = perfect_matchings(vertices)
    assert len(matchings) == 3
    coefficients: list[Scalar] = []
    for word in product(COLORS, repeat=4):
        colors = dict(zip(vertices, word, strict=True))
        coefficients.append(
            sum(
                (
                    product_of(
                        block_for(blocks, left, right)[colors[left]][colors[right]]
                        for left, right in matching
                    )
                    for matching in matchings
                ),
                ZERO,
            )
        )
    return tuple(coefficients)


def product_of(values) -> Scalar:
    """Multiply an iterable of exact scalars."""
    result = ONE
    for value in values:
        result *= value
    return result


def all_pair_responses(
    h_block: Matrix,
    a_blocks: tuple[Matrix, ...],
    c_blocks: tuple[Matrix, ...],
    b_blocks: dict[tuple[int, int], Matrix],
) -> tuple[tuple[Scalar, ...], ...]:
    """Return the six labelled pair responses."""
    return tuple(
        response_tensor(
            h_block,
            b_blocks.get((u, v), zero_matrix()),
            a_blocks[u],
            a_blocks[v],
            c_blocks[u],
            c_blocks[v],
        )
        for u, v in combinations(PORTS, 2)
    )


def check_rank_three_slice_obstruction() -> int:
    """Stress the exact rank-three-versus-two response-slice mechanism."""
    full_rank_blocks = (
        identity_matrix(),
        (
            vector(1, 1, 0),
            vector(0, 1, 1),
            vector(1, 0, 1),
        ),
        (
            vector(2, -1, 1),
            vector(1, 1, 0),
            vector(0, 1, 1),
        ),
        (
            vector(1, 2, 3),
            vector(0, 1, 4),
            vector(0, 0, 2),
        ),
    )
    test_vectors = (
        vector(1, 0, 0),
        vector(0, 1, 0),
        vector(0, 0, 1),
        vector(1, 1, 0),
        vector(1, -1, 1),
        vector(2, 1, -1),
    )
    checks = 0
    for h_block in full_rank_blocks:
        assert matrix_rank(h_block) == 3
        for a_u, c_v, a_v, c_u in product(test_vectors, repeat=4):
            two_outer = matrix_add(outer(a_u, c_v), outer(a_v, c_u))
            assert matrix_rank(two_outer) <= 2
            for b_value in (-2, -1, 1, 3):
                rank_three = matrix_scale(b_value, h_block)
                assert matrix_rank(rank_three) == 3
                assert rank_three != matrix_scale(-1, two_outer)
                checks += 1
    return checks


def check_support_and_sign_classification() -> dict[str, int]:
    """Audit the exact mask comparison and characteristic-zero sign graph."""
    valid_masks: list[tuple[int, int]] = []
    for x_mask in range(1, 1 << 4):
        for y_mask in range(1, 1 << 4):
            if all(
                (bool(x_mask & (1 << u)) and bool(y_mask & (1 << v)))
                == (bool(x_mask & (1 << v)) and bool(y_mask & (1 << u)))
                for u, v in combinations(PORTS, 2)
            ):
                valid_masks.append((x_mask, y_mask))
    assert valid_masks == [(mask, mask) for mask in range(1, 1 << 4)]

    expected_ranks = {1: 0, 2: 1, 3: 3, 4: 4}
    for size, expected in expected_ranks.items():
        rows = tuple(
            tuple(ONE if index in pair else ZERO for index in range(size))
            for pair in combinations(range(size), 2)
        )
        assert matrix_rank(rows) == expected
        nullity = size - expected
        assert nullity == (1 if size <= 2 else 0)

    scalar_solutions = 0
    values = (-1, 0, 1)
    for a_values in product(values, repeat=4):
        for c_values in product(values, repeat=4):
            x_support = {u for u, value in enumerate(a_values) if value}
            y_support = {u for u, value in enumerate(c_values) if value}
            if not x_support or not y_support:
                continue
            if all(
                a_values[u] * c_values[v] + a_values[v] * c_values[u] == 0
                for u, v in combinations(PORTS, 2)
            ):
                assert x_support == y_support
                assert len(x_support) <= 2
                scalar_solutions += 1

    return {
        "mask_pairs": len(valid_masks),
        "signed_sizes": len(expected_ranks),
        "scalar_solutions": scalar_solutions,
    }


def check_response_normal_forms() -> dict[str, int]:
    """Reconstruct singleton, two-port, determinant, and characteristic controls."""
    h_identity = identity_matrix()
    no_b = {pair: zero_matrix() for pair in combinations(PORTS, 2)}
    zero = zero_matrix()

    singleton_a = (matrix_unit(0, 0), zero, zero, zero)
    singleton_c = (matrix_unit(1, 1), zero, zero, zero)
    singleton = all_pair_responses(h_identity, singleton_a, singleton_c, no_b)
    assert all(not any(response) for response in singleton)
    for u, v in combinations(PORTS, 2):
        direct = response_by_matchings(
            h_identity,
            zero,
            singleton_a[u],
            singleton_a[v],
            singleton_c[u],
            singleton_c[v],
        )
        formula = response_tensor(
            h_identity,
            zero,
            singleton_a[u],
            singleton_a[v],
            singleton_c[u],
            singleton_c[v],
        )
        assert direct == formula

    covectors = (
        vector(1, 0, 0),
        vector(0, 1, 0),
        vector(1, 1, 0),
        vector(1, -2, 1),
    )
    two_port_checks = 0
    for alpha_s, alpha_t in product(covectors, repeat=2):
        for tau in (Fraction(-3), Fraction(1, 2), Fraction(1), Fraction(2)):
            a_blocks = (
                outer(vector(1, 0, 0), alpha_s),
                outer(vector(1, 0, 0), alpha_t),
                zero,
                zero,
            )
            c_blocks = (
                matrix_scale(tau, outer(vector(0, 1, 0), alpha_s)),
                matrix_scale(-tau, outer(vector(0, 1, 0), alpha_t)),
                zero,
                zero,
            )
            responses = all_pair_responses(h_identity, a_blocks, c_blocks, no_b)
            assert all(not any(response) for response in responses)
            direct = response_by_matchings(
                h_identity,
                zero,
                a_blocks[0],
                a_blocks[1],
                c_blocks[0],
                c_blocks[1],
            )
            assert direct == responses[0]
            assert c_blocks[0] == matrix_scale(tau, outer(vector(0, 1, 0), alpha_s))
            assert c_blocks[1] == matrix_scale(-tau, outer(vector(0, 1, 0), alpha_t))
            two_port_checks += 1

    alphas = (
        vector(1, 1, 0),
        vector(1, -1, 1),
        vector(2, 1, 1),
        vector(1, 2, -1),
    )
    betas = (
        vector(1, 0, 1),
        vector(0, 1, -1),
        vector(1, 1, 1),
        vector(2, -1, 1),
    )
    h_rank_one = matrix_unit(0, 0)
    determinant_a = tuple(outer(vector(1, 0, 0), alpha) for alpha in alphas)
    determinant_c = tuple(outer(vector(1, 0, 0), beta) for beta in betas)
    determinant_b: dict[tuple[int, int], Matrix] = {}
    for u, v in combinations(PORTS, 2):
        determinant_b[u, v] = matrix_scale(
            -1,
            matrix_add(outer(alphas[u], betas[v]), outer(betas[u], alphas[v])),
        )
    assert matrix_rank(h_rank_one) == 1
    divisor_responses = all_pair_responses(
        h_rank_one,
        determinant_a,
        determinant_c,
        determinant_b,
    )
    assert all(not any(response) for response in divisor_responses)
    assert all(block != zero for block in determinant_b.values())
    assert all(block != zero for block in determinant_a + determinant_c)

    char_two_checks = 0
    for active_count in (3, 4):
        alpha_family = covectors[:active_count]
        for u, v in combinations(range(active_count), 2):
            for s, t in product(COLORS, repeat=2):
                value = (
                    alpha_family[u][s] * alpha_family[v][t]
                    + alpha_family[v][t] * alpha_family[u][s]
                )
                assert value.numerator % 2 == 0
                char_two_checks += 1

    return {
        "singleton_pairs": len(singleton),
        "two_port_forms": two_port_checks,
        "determinant_divisor_pairs": len(divisor_responses),
        "characteristic_two_entries": char_two_checks,
    }


def torus_kernel(covector: Vector) -> Vector | None:
    """Construct a rational torus point in a noncoordinate covector kernel."""
    support = [index for index, entry in enumerate(covector) if entry]
    if len(support) < 2:
        return None
    pivot = support[0]
    other = [index for index in COLORS if index != pivot]
    choices = tuple(Fraction(value) for value in (-3, -2, -1, 1, 2, 3))
    for selected in product(choices, repeat=2):
        result = [ONE, ONE, ONE]
        for index, value in zip(other, selected, strict=True):
            result[index] = value
        subtotal = sum((covector[index] * result[index] for index in other), ZERO)
        if not subtotal:
            continue
        result[pivot] = -subtotal / covector[pivot]
        candidate = tuple(result)
        if all(candidate) and not dot(covector, candidate):
            return candidate
    raise AssertionError("finite construction table missed a torus kernel")


def bilinear_torus_zero(matrix: Matrix) -> tuple[Vector, Vector] | None:
    """Find a rational torus zero for the bounded bilinear audit table."""
    choices = tuple(Fraction(value) for value in (-3, -2, -1, 1, 2, 3))
    for right in product(choices, repeat=3):
        row_values = tuple(
            sum((matrix[i][j] * right[j] for j in COLORS), ZERO) for i in COLORS
        )
        if not any(row_values):
            return vector(1, 1, 1), tuple(right)
        left = torus_kernel(row_values)
        if left is not None and not bilinear(matrix, left, tuple(right)):
            return left, tuple(right)
    return None


def check_torus_coordinate_forcing() -> dict[str, int]:
    """Audit the torus-kernel and five-root extension mechanisms exactly."""
    covector_checks = 0
    for entries in product(range(-2, 3), repeat=3):
        if entries == (0, 0, 0):
            continue
        covector = tuple(Fraction(entry) for entry in entries)
        support_size = sum(bool(entry) for entry in covector)
        root = torus_kernel(covector)
        assert (root is None) == (support_size == 1)
        if root is not None:
            assert all(root)
            assert not dot(covector, root)
        covector_checks += 1

    bilinear_checks = 0
    positions = tuple(product(COLORS, repeat=2))
    for support_size in (1, 2, 3):
        for selected in combinations(positions, support_size):
            for signs in product((-1, 1), repeat=support_size):
                rows = [[ZERO for _ in COLORS] for _ in COLORS]
                for (row, column), sign in zip(selected, signs, strict=True):
                    rows[row][column] = Fraction(sign)
                matrix = tuple(tuple(row) for row in rows)
                zero = bilinear_torus_zero(matrix)
                assert (zero is None) == (support_size == 1)
                if zero is not None:
                    left, right = zero
                    assert all(left) and all(right)
                    assert not bilinear(matrix, left, right)
                bilinear_checks += 1

    noncoordinate = (vector(1, 1, 0), vector(1, -2, 1))
    fifth_root_checks = 0
    q0 = vector(1, 1, 1)
    for alpha_s, alpha_t in product(noncoordinate, repeat=2):
        z_s = torus_kernel(alpha_s)
        z_t = torus_kernel(alpha_t)
        assert z_s is not None and z_t is not None
        a_s = outer(vector(1, 0, 0), alpha_s)
        a_t = outer(vector(1, 0, 0), alpha_t)
        assert not bilinear(a_s, q0, z_s)
        assert not bilinear(a_t, q0, z_t)
        fifth_root_checks += 1

    return {
        "covectors": covector_checks,
        "bilinear_blocks": bilinear_checks,
        "forbidden_five_roots": fifth_root_checks,
    }


def flatten_target_projection(
    blocked_q0: int,
    blocked_q1: int,
    weights: tuple[Scalar, Scalar, Scalar],
) -> tuple[Vector, ...]:
    """Build the projected GHZ tensor as a Q|U flattening."""
    rows = [[ZERO for _ in range(3**4)] for _ in range(3**2)]
    for color in COLORS:
        if color in (blocked_q0, blocked_q1):
            continue
        q_index = 3 * color + color
        u_index = sum(color * 3 ** (3 - power) for power in range(4))
        rows[q_index][u_index] = weights[color]
    return tuple(tuple(row) for row in rows)


def projected_block(h_block: Matrix, blocked_q0: int, blocked_q1: int) -> Matrix:
    """Apply the two coordinate-killing projections to H."""
    return tuple(
        tuple(
            ZERO if row == blocked_q0 or column == blocked_q1 else h_block[row][column]
            for column in COLORS
        )
        for row in COLORS
    )


def check_target_projection_dichotomy() -> dict[str, int]:
    """Check the exact Q|U ranks and the denominator-free pure factorization."""
    weights = (Fraction(2), Fraction(-3), Fraction(5))
    equal_cases = 0
    opposite_cases = 0
    for blocked_q0 in COLORS:
        for blocked_q1 in COLORS:
            target = flatten_target_projection(blocked_q0, blocked_q1, weights)
            expected_rank = 2 if blocked_q0 == blocked_q1 else 1
            assert matrix_rank(target) == expected_rank
            if blocked_q0 == blocked_q1:
                equal_cases += 1
                reduced_weights = list(weights)
                reduced_weights[(blocked_q0 + 1) % 3] = ZERO
                reduced = flatten_target_projection(
                    blocked_q0, blocked_q1, tuple(reduced_weights)
                )
                assert matrix_rank(reduced) <= 1
                continue

            remaining = ({0, 1, 2} - {blocked_q0, blocked_q1}).pop()
            q_pivot = 3 * remaining + remaining
            u_pivot = sum(remaining * 3 ** (3 - power) for power in range(4))
            nonzero_entries = [
                (row, column, value)
                for row, values in enumerate(target)
                for column, value in enumerate(values)
                if value
            ]
            assert nonzero_entries == [(q_pivot, u_pivot, weights[remaining])]
            for lambda_value in (Fraction(-2), Fraction(1), Fraction(3, 2)):
                h_vector = [ZERO for _ in range(9)]
                pi_vector = [ZERO for _ in range(81)]
                h_vector[q_pivot] = lambda_value
                pi_vector[u_pivot] = weights[remaining] / lambda_value
                factored = tuple(
                    tuple(h_entry * pi_entry for pi_entry in pi_vector)
                    for h_entry in h_vector
                )
                assert factored == target
                assert lambda_value * pi_vector[u_pivot] == weights[remaining]
            opposite_cases += 1

    supported_rank_checks = 0
    for blocked_q0 in COLORS:
        for blocked_q1 in COLORS:
            for row_values, column_values in product(
                (
                    vector(1, 0, 0),
                    vector(1, 1, -1),
                    vector(2, -1, 3),
                ),
                repeat=2,
            ):
                supported = matrix_add(
                    outer(
                        tuple(ONE if index == blocked_q0 else ZERO for index in COLORS),
                        row_values,
                    ),
                    outer(
                        column_values,
                        tuple(ONE if index == blocked_q1 else ZERO for index in COLORS),
                    ),
                )
                assert (
                    projected_block(supported, blocked_q0, blocked_q1) == zero_matrix()
                )
                assert matrix_rank(supported) <= 2
                supported_rank_checks += 1

    coordinate_cover = [ZERO for _ in range(81)]
    coordinate_cover[17] = Fraction(7)
    assert any(coordinate_cover)
    assert [index for index, entry in enumerate(coordinate_cover) if entry] == [17]

    return {
        "equal_colour_rank_two": equal_cases,
        "opposite_colour_rank_one": opposite_cases,
        "rank_two_support_patterns": supported_rank_checks,
        "tensor_coordinate_opens": len(coordinate_cover),
    }


def check_top_response_matching_structure() -> dict[str, int]:
    """Show every six-vertex matching contains a direct U-to-U edge."""
    vertices = ("q0", "q1", "u0", "u1", "u2", "u3")
    matchings = perfect_matchings(vertices)
    assert len(matchings) == 15
    direct_counts = []
    for matching in matchings:
        direct_count = sum(
            left.startswith("u") and right.startswith("u") for left, right in matching
        )
        assert direct_count >= 1
        direct_counts.append(direct_count)
    assert sorted(direct_counts).count(2) == 3
    assert sorted(direct_counts).count(1) == 12
    return {"six_vertex_matchings": len(matchings), "direct_edges": sum(direct_counts)}


ROOTS = ("r0", "r1", "r2", "r3")
QNAMES = ("q0", "q1")
UNAMES = ("u0", "u1", "u2", "u3")
OUTSIDE = QNAMES + UNAMES
ALL_VERTICES = ROOTS + OUTSIDE


def add_edge(
    blocks: dict[tuple[str, str], Matrix],
    left: str,
    right: str,
    block: Matrix,
) -> None:
    """Add one oriented block to the fixture."""
    assert (left, right) not in blocks and (right, left) not in blocks
    blocks[left, right] = block


def build_off_target_fixture() -> dict[tuple[str, str], Matrix]:
    """Construct the ten-vertex fixture without repository dependencies."""
    blocks: dict[tuple[str, str], Matrix] = {}
    root_u = {
        ("r0", "u0"): 2,
        ("r1", "u0"): 0,
        ("r2", "u0"): 1,
        ("r1", "u1"): 2,
        ("r2", "u1"): 0,
        ("r3", "u1"): 1,
        ("r2", "u2"): 2,
        ("r3", "u2"): 0,
        ("r3", "u3"): 2,
    }
    root_q = {
        ("r0", "q0"): 0,
        ("r1", "q0"): 1,
        ("r2", "q1"): 0,
        ("r0", "q1"): 1,
    }
    for (root, outside), outside_color in root_u.items() | root_q.items():
        add_edge(blocks, root, outside, matrix_unit(0, outside_color))

    add_edge(blocks, "q0", "q1", identity_matrix())
    add_edge(blocks, "q0", "u0", matrix_unit(0, 0))
    add_edge(blocks, "q1", "u0", matrix_unit(1, 0))
    add_edge(blocks, "q0", "u1", matrix_unit(0, 1))
    add_edge(blocks, "q1", "u1", matrix_unit(1, 1, -1))
    return blocks


def root_contracted_column(
    blocks: dict[tuple[str, str], Matrix],
    outside: str,
    outside_color: int,
) -> Vector:
    """Evaluate one L-column at the all-ones root vectors."""
    return tuple(
        sum(
            block_for(blocks, root, outside)[root_color][outside_color]
            for root_color in COLORS
        )
        for root in ROOTS
    )


def complementary_permanent_coefficient(
    blocks: dict[tuple[str, str], Matrix],
    complement: tuple[str, str, str, str],
    colors: tuple[int, int, int, int],
) -> Scalar:
    """Compute a complementary permanent through root-to-port bijections."""
    color_by_vertex = dict(zip(complement, colors, strict=True))
    return sum(
        (
            product_of(
                root_contracted_column(blocks, outside, color_by_vertex[outside])[
                    root_index
                ]
                for root_index, outside in enumerate(assignment)
            )
            for assignment in permutations(complement)
        ),
        ZERO,
    )


def contracted_edge_value(
    blocks: dict[tuple[str, str], Matrix],
    left: str,
    right: str,
    outside_colors: dict[str, int],
) -> Scalar:
    """Evaluate an edge after root contraction and outside color fixing."""
    block = block_for(blocks, left, right)
    left_is_root = left in ROOTS
    right_is_root = right in ROOTS
    if left_is_root and right_is_root:
        return sum((entry for row in block for entry in row), ZERO)
    if left_is_root:
        return sum((block[color][outside_colors[right]] for color in COLORS), ZERO)
    if right_is_root:
        return sum((block[outside_colors[left]][color] for color in COLORS), ZERO)
    return block[outside_colors[left]][outside_colors[right]]


def contracted_full_matching_coefficient(
    blocks: dict[tuple[str, str], Matrix],
    word: tuple[int, ...],
) -> Scalar:
    """Compute a contracted ten-vertex coefficient from 945 matchings."""
    outside_colors = dict(zip(OUTSIDE, word, strict=True))
    return sum(
        (
            product_of(
                contracted_edge_value(blocks, left, right, outside_colors)
                for left, right in matching
            )
            for matching in perfect_matchings(ALL_VERTICES)
        ),
        ZERO,
    )


def contracted_deck_coefficient(
    blocks: dict[tuple[str, str], Matrix],
    word: tuple[int, ...],
) -> Scalar:
    """Recompute the same coefficient through the shuffled pair deck."""
    color_by_vertex = dict(zip(OUTSIDE, word, strict=True))
    total = ZERO
    for pair in combinations(OUTSIDE, 2):
        complement = tuple(vertex for vertex in OUTSIDE if vertex not in pair)
        pair_value = block_for(blocks, *pair)[color_by_vertex[pair[0]]][
            color_by_vertex[pair[1]]
        ]
        complement_colors = tuple(color_by_vertex[vertex] for vertex in complement)
        total += pair_value * complementary_permanent_coefficient(
            blocks, complement, complement_colors
        )
    return total


def fixture_response_blocks(
    blocks: dict[tuple[str, str], Matrix],
) -> tuple[
    Matrix, tuple[Matrix, ...], tuple[Matrix, ...], dict[tuple[int, int], Matrix]
]:
    """Extract H,A,C,B from the labelled fixture."""
    h_block = block_for(blocks, "q0", "q1")
    a_blocks = tuple(block_for(blocks, "q0", port) for port in UNAMES)
    c_blocks = tuple(block_for(blocks, "q1", port) for port in UNAMES)
    b_blocks = {
        (u, v): block_for(blocks, UNAMES[u], UNAMES[v])
        for u, v in combinations(PORTS, 2)
    }
    return h_block, a_blocks, c_blocks, b_blocks


def audit_fixture_incidence_and_permanent(
    blocks: dict[tuple[str, str], Matrix],
) -> dict[str, int]:
    """Audit the L-table, corank, Pi_Q, raw p, and h independently."""
    expected_columns = {
        "u0": (vector(0, 1, 0, 0), vector(0, 0, 1, 0), vector(1, 0, 0, 0)),
        "u1": (vector(0, 0, 1, 0), vector(0, 0, 0, 1), vector(0, 1, 0, 0)),
        "u2": (vector(0, 0, 0, 1), vector(0, 0, 0, 0), vector(0, 0, 1, 0)),
        "u3": (vector(0, 0, 0, 0), vector(0, 0, 0, 0), vector(0, 0, 0, 1)),
        "q0": (vector(1, 0, 0, 0), vector(0, 1, 0, 0), vector(0, 0, 0, 0)),
        "q1": (vector(0, 0, 1, 0), vector(1, 0, 0, 0), vector(0, 0, 0, 0)),
    }
    ranks = []
    for outside in OUTSIDE:
        columns = tuple(
            root_contracted_column(blocks, outside, color) for color in COLORS
        )
        assert columns == expected_columns[outside]
        matrix_by_rows = tuple(
            tuple(columns[column][row] for column in COLORS) for row in range(4)
        )
        ranks.append(matrix_rank(matrix_by_rows))
    assert ranks == [2, 2, 3, 3, 2, 1]
    assert sum(3 - rank for rank in ranks) == 5

    pi_nonzero: dict[tuple[int, ...], Scalar] = {}
    for word in product(COLORS, repeat=4):
        value = complementary_permanent_coefficient(blocks, UNAMES, word)
        if value:
            pi_nonzero[word] = value
    assert pi_nonzero == {(2, 2, 2, 2): ONE}

    q0_at_ones = tuple(
        sum(
            (root_contracted_column(blocks, "q0", color)[row] for color in COLORS), ZERO
        )
        for row in range(4)
    )
    q1_at_ones = tuple(
        sum(
            (root_contracted_column(blocks, "q1", color)[row] for color in COLORS), ZERO
        )
        for row in range(4)
    )
    raw_p = q0_at_ones[1] * q1_at_ones[2] + q0_at_ones[2] * q1_at_ones[1]
    assert raw_p == ONE
    h_at_ones = sum((entry for row in identity_matrix() for entry in row), ZERO)
    assert h_at_ones == 3

    return {
        "outside_modes": len(OUTSIDE),
        "corank": sum(3 - rank for rank in ranks),
        "permanent_words": 3**4,
        "raw_p": int(raw_p),
        "h": int(h_at_ones),
    }


def audit_fixture_maximum_root(
    blocks: dict[tuple[str, str], Matrix],
) -> dict[str, int]:
    """Enumerate the monomial-edge independence bound for every vertex set."""
    monomial_edges: set[frozenset[str]] = set()
    for left, right in combinations(ALL_VERTICES, 2):
        block = block_for(blocks, left, right)
        nonzero = [entry for row in block for entry in row if entry]
        if len(nonzero) == 1:
            monomial_edges.add(frozenset((left, right)))

    cliques = (
        ("r2", "u2"),
        ("r3", "u3"),
        ("r0", "q1", "u0"),
        ("r1", "q0", "u1"),
    )
    assert {vertex for clique in cliques for vertex in clique} == set(ALL_VERTICES)
    for clique in cliques:
        assert all(
            frozenset(pair) in monomial_edges for pair in combinations(clique, 2)
        )

    independent_sets: list[tuple[str, ...]] = []
    for size in range(len(ALL_VERTICES) + 1):
        for selected in combinations(ALL_VERTICES, size):
            if all(
                frozenset(pair) not in monomial_edges
                for pair in combinations(selected, 2)
            ):
                independent_sets.append(selected)
    maximum_size = max(map(len, independent_sets))
    maximum_sets = [
        selected for selected in independent_sets if len(selected) == maximum_size
    ]
    assert maximum_size == 4
    assert ROOTS in maximum_sets
    assert all(
        block_for(blocks, *pair) == zero_matrix() for pair in combinations(ROOTS, 2)
    )

    return {
        "vertex_subsets": 2 ** len(ALL_VERTICES),
        "monomial_edges": len(monomial_edges),
        "maximum_independent_sets": len(maximum_sets),
        "maximum_root_order": maximum_size,
    }


def audit_fixture_responses_and_target(
    blocks: dict[tuple[str, str], Matrix],
) -> dict[str, int]:
    """Audit all response tensors, the projected line, and mixed failure."""
    h_block, a_blocks, c_blocks, b_blocks = fixture_response_blocks(blocks)
    assert matrix_rank(h_block) == 3
    responses = all_pair_responses(h_block, a_blocks, c_blocks, b_blocks)
    assert all(not any(response) for response in responses)
    for (u, v), formula in zip(combinations(PORTS, 2), responses, strict=True):
        direct = response_by_matchings(
            h_block,
            b_blocks[u, v],
            a_blocks[u],
            a_blocks[v],
            c_blocks[u],
            c_blocks[v],
        )
        assert direct == formula

    projected_h = projected_block(h_block, 0, 1)
    assert projected_h == matrix_unit(2, 2)
    projected_coefficients: dict[tuple[int, ...], Scalar] = {}
    for word in product(COLORS, repeat=6):
        if word[0] == 0 or word[1] == 1:
            continue
        value = contracted_deck_coefficient(blocks, word)
        if value:
            projected_coefficients[word] = value
    assert projected_coefficients == {(2, 2, 2, 2, 2, 2): ONE}

    mixed_word = (0, 0, 2, 2, 2, 2)
    deck_value = contracted_deck_coefficient(blocks, mixed_word)
    matching_value = contracted_full_matching_coefficient(blocks, mixed_word)
    assert deck_value == matching_value == ONE
    assert len(perfect_matchings(ALL_VERTICES)) == 945

    q_u_vertices = QNAMES + UNAMES
    q_u_matchings = perfect_matchings(q_u_vertices)
    for word in product(COLORS, repeat=6):
        colors = dict(zip(q_u_vertices, word, strict=True))
        coefficient = sum(
            (
                product_of(
                    block_for(blocks, left, right)[colors[left]][colors[right]]
                    for left, right in matching
                )
                for matching in q_u_matchings
            ),
            ZERO,
        )
        assert coefficient == 0

    return {
        "pair_response_coefficients": len(responses) * 3**4,
        "projected_outside_words": 2 * 2 * 3**4,
        "six_port_coefficients": 3**6,
        "ten_vertex_matchings": len(perfect_matchings(ALL_VERTICES)),
        "mixed_failure": int(matching_value),
    }


def main() -> None:
    """Run the complete independent exact audit."""
    rank_checks = check_rank_three_slice_obstruction()
    support_checks = check_support_and_sign_classification()
    normal_form_checks = check_response_normal_forms()
    torus_checks = check_torus_coordinate_forcing()
    projection_checks = check_target_projection_dichotomy()
    top_checks = check_top_response_matching_structure()

    fixture = build_off_target_fixture()
    incidence_checks = audit_fixture_incidence_and_permanent(fixture)
    maximum_root_checks = audit_fixture_maximum_root(fixture)
    fixture_target_checks = audit_fixture_responses_and_target(fixture)

    print("four-root full-rank all-response-zero no-import audit: PASS")
    print(f"  rank-three Fraction slices: {rank_checks}")
    print(f"  support/sign tables: {support_checks}")
    print(f"  exact normal-form/divisor controls: {normal_form_checks}")
    print(f"  torus coordinate-forcing tables: {torus_checks}")
    print(f"  target-projection ranks: {projection_checks}")
    print(f"  top-response matching structure: {top_checks}")
    print(f"  fixture incidence/permanent: {incidence_checks}")
    print(f"  fixture maximum-root enumeration: {maximum_root_checks}")
    print(f"  fixture responses/target failure: {fixture_target_checks}")
    print("  scope: finite independent replay only; arbitrary-point proof is written")
    print("  open: det(H_Q)=0, surviving pure-Pi witness locus, absorption leaves")


if __name__ == "__main__":
    main()
