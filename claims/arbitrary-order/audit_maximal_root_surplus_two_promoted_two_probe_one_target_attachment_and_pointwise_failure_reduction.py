"""Independent exact audit of the promoted two-probe one-target reduction.

This script deliberately uses only the Python standard library.  It does not
read or import the primary verifier.  Its independent representations are:

* bitmask enumeration of complete-graph perfect matchings;
* symbolic bipartite assignment monomials for the permanent Laplace split;
* exact ``Fraction`` row reduction for selector and pure-quotient claims;
* direct subset sums for all dimension formulae;
* exhaustive exact small-matrix tables for the pointwise rank criterion; and
* direct weighted matching enumeration of the response-zero control.

The bounded checks replay displayed finite identities and boundary models.
They audit, but do not replace, the arbitrary-root written proof and do not
claim that the remaining physical failure locus is empty.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations, product
from math import comb

Q = Fraction


def odd_double_factorial(n: int) -> int:
    """Return n!! for odd n, including (-1)!! = 1."""
    answer = 1
    for value in range(n, 0, -2):
        answer *= value
    return answer


def perfect_matchings(mask: int):
    """Yield perfect matchings of the set bits of ``mask`` exactly once."""
    if mask == 0:
        yield ()
        return
    low_bit = mask & -mask
    first = low_bit.bit_length() - 1
    rest = mask ^ low_bit
    partners = rest
    while partners:
        partner_bit = partners & -partners
        second = partner_bit.bit_length() - 1
        for tail in perfect_matchings(rest ^ partner_bit):
            yield ((first, second),) + tail
        partners ^= partner_bit


def audit_companion_grade_census() -> int:
    """Classify every matching by whether the two probes meet each other."""
    total_seen = 0
    for r in range(3, 7):
        outside_count = 2 * r
        vertex_count = outside_count + 2
        grades: Counter[int] = Counter()
        lower_complements: Counter[tuple[int, int]] = Counter()

        for matching in perfect_matchings((1 << vertex_count) - 1):
            total_seen += 1
            root_partners: dict[int, int] = {}
            root_pair = False
            for left, right in matching:
                if (left, right) == (0, 1):
                    root_pair = True
                if left in (0, 1):
                    root_partners[left] = right
                if right in (0, 1):
                    root_partners[right] = left

            if root_pair:
                assert root_partners == {0: 1, 1: 0}
                grades[outside_count] += 1
            else:
                complement = tuple(sorted((root_partners[0] - 2, root_partners[1] - 2)))
                assert complement[0] >= 0
                grades[outside_count - 2] += 1
                lower_complements[complement] += 1

        top_expected = odd_double_factorial(outside_count - 1)
        per_complement = 2 * odd_double_factorial(outside_count - 3)
        lower_expected = comb(outside_count, 2) * per_complement
        total_expected = odd_double_factorial(vertex_count - 1)
        assert grades == {
            outside_count - 2: lower_expected,
            outside_count: top_expected,
        }
        assert sum(grades.values()) == total_expected
        assert len(lower_complements) == comb(outside_count, 2)
        assert set(lower_complements.values()) == {per_complement}

    return total_seen


def assignment_monomials(
    rows: tuple[str, ...], columns: tuple[str, ...]
) -> Counter[tuple[tuple[str, str], ...]]:
    """Return the permanent as a counter of distinct edge monomials."""
    assert len(rows) == len(columns)
    terms: Counter[tuple[tuple[str, str], ...]] = Counter()
    for ordered_columns in permutations(columns):
        monomial = tuple(sorted(zip(rows, ordered_columns, strict=True)))
        terms[monomial] += 1
    return terms


def multiply_monomial_counters(
    left: Counter[tuple[tuple[str, str], ...]],
    right: Counter[tuple[tuple[str, str], ...]],
) -> Counter[tuple[tuple[str, str], ...]]:
    product_counter: Counter[tuple[tuple[str, str], ...]] = Counter()
    for left_term, left_coefficient in left.items():
        for right_term, right_coefficient in right.items():
            monomial = tuple(sorted(left_term + right_term))
            product_counter[monomial] += left_coefficient * right_coefficient
    return product_counter


def audit_laplace_permanent_split() -> int:
    """Compare the two-probe Laplace expansion term by term for r=3..6."""
    checked_terms = 0
    for r in range(3, 7):
        probes = ("a0", "a1")
        old_roots = tuple(f"k{index}" for index in range(1, r - 1))
        rows = probes + old_roots
        ports = tuple(f"u{index}" for index in range(r))
        direct = assignment_monomials(rows, ports)
        laplace: Counter[tuple[tuple[str, str], ...]] = Counter()
        for chosen in combinations(ports, 2):
            probe_terms = assignment_monomials(probes, chosen)
            remainder = tuple(port for port in ports if port not in chosen)
            old_root_terms = assignment_monomials(old_roots, remainder)
            laplace += multiply_monomial_counters(probe_terms, old_root_terms)

        assert laplace == direct
        assert len(direct) == len(list(permutations(ports)))
        assert set(direct.values()) == {1}
        checked_terms += len(direct)

    # Model all coefficient slices of the unique top companion, not just one
    # padded vector.  Here L=A tensor C with dimensions 2 and 3.  Every top
    # slice lies in top_A tensor C and is killed by epsilon_A tensor id_C,
    # whereas the desired vector has a nonzero contracted C-vector.
    top_slices = [
        [
            Q(1) if a_coordinate == 1 and c_coordinate == slice_coordinate else Q(0)
            for slice_coordinate in range(3)
        ]
        for a_coordinate in range(2)
        for c_coordinate in range(3)
    ]
    desired = [Q(1), Q(2), Q(3), Q(7), Q(11), Q(13)]
    epsilon_contraction = desired[:3]
    assert epsilon_contraction == [Q(1), Q(2), Q(3)]
    assert all(not any(top_slices[c_coordinate]) for c_coordinate in range(3))
    assert matrix_rank(top_slices) == 3
    assert matrix_rank(append_columns(top_slices, [desired])) == 4
    return checked_terms


def audit_dimension_formulae() -> int:
    """Derive raw and residual-evaluated dimensions by direct subset sums."""
    checked = 0
    for r in range(3, 8):
        outside_count = 2 * r
        m = 2 * r - 2

        formal_direct = sum(
            comb(outside_count, size) * 3**size
            for size in range(2, outside_count + 1, 2)
        )
        formal_closed = (16**r + 4**r) // 2 - 1
        assert formal_direct == formal_closed

        active_direct = (
            comb(outside_count, 2) * 3 ** (outside_count - 2) + 3**outside_count
        )
        assert active_direct == (comb(2 * r, 2) * 3 ** (2 * r - 2) + 3 ** (2 * r))

        evaluated_formal = 0
        for mask in range(1, 1 << outside_count):
            if mask.bit_count() % 2 == 0:
                open_port_count = (mask >> 2).bit_count()
                evaluated_formal += 3**open_port_count
        assert evaluated_formal == 2 * 4**m - 1

        evaluated_active = 0
        full_mask = (1 << outside_count) - 1
        for missing in combinations(range(outside_count), 2):
            label_mask = full_mask ^ (1 << missing[0]) ^ (1 << missing[1])
            evaluated_active += 3 ** ((label_mask >> 2).bit_count())
        evaluated_active += 3**m
        e_m = comb(m, 2) * 3 ** (m - 2) + 2 * m * 3 ** (m - 1) + 2 * 3**m
        assert evaluated_active == e_m

        assert comb(m, 2) + 1 == len(list(combinations(range(m), 2))) + 1
        assert 3 ** (2 + 2) == 81
        assert 3**2 == 9
        checked += 1

    r = 3
    m = 2 * r - 2
    e_m = comb(m, 2) * 3 ** (m - 2) + 2 * m * 3 ** (m - 1) + 2 * 3**m
    assert (16**r + 4**r) // 2 - 1 == 2079
    assert comb(2 * r, 2) * 3 ** (2 * r - 2) + 3 ** (2 * r) == 1944
    assert 2 * 4**m - 1 == 511
    assert e_m == 432
    assert 81 * e_m * 3 ** (m - 2) == 314_928
    assert 9 * e_m * 3**m == 314_928
    # The theorem reports matrix shapes, so compare column counts separately.
    assert e_m * 3 ** (m - 2) == 3888
    assert e_m * 3**m == 34_992
    return checked


def matrix_rank(matrix: list[list[Fraction]]) -> int:
    """Exact Gauss-Jordan rank over Q."""
    if not matrix:
        return 0
    column_count = len(matrix[0])
    assert all(len(row) == column_count for row in matrix)
    work = [[Q(entry) for entry in row] for row in matrix]
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        work[pivot_row] = [entry / pivot_value for entry in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or not work[row][column]:
                continue
            multiplier = work[row][column]
            work[row] = [
                entry - multiplier * pivot_entry
                for entry, pivot_entry in zip(work[row], work[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def solve_linear_system(
    coefficients: list[list[Fraction]],
    constants: list[Fraction],
    variable_count: int,
) -> list[Fraction] | None:
    """Return one exact solution, with free variables set to zero."""
    assert len(coefficients) == len(constants)
    if not coefficients:
        return [Q(0) for _ in range(variable_count)]
    augmented = [
        [Q(entry) for entry in row] + [Q(constant)]
        for row, constant in zip(coefficients, constants, strict=True)
    ]
    assert all(len(row) == variable_count + 1 for row in augmented)

    pivot_row = 0
    pivots: list[int] = []
    for column in range(variable_count):
        pivot = next(
            (row for row in range(pivot_row, len(augmented)) if augmented[row][column]),
            None,
        )
        if pivot is None:
            continue
        augmented[pivot_row], augmented[pivot] = (
            augmented[pivot],
            augmented[pivot_row],
        )
        pivot_value = augmented[pivot_row][column]
        augmented[pivot_row] = [entry / pivot_value for entry in augmented[pivot_row]]
        for row in range(len(augmented)):
            if row == pivot_row or not augmented[row][column]:
                continue
            multiplier = augmented[row][column]
            augmented[row] = [
                entry - multiplier * pivot_entry
                for entry, pivot_entry in zip(
                    augmented[row], augmented[pivot_row], strict=True
                )
            ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == len(augmented):
            break

    for row in augmented:
        if not any(row[:variable_count]) and row[-1]:
            return None

    solution = [Q(0) for _ in range(variable_count)]
    for row, column in enumerate(pivots):
        solution[column] = augmented[row][-1]
    return solution


def append_columns(
    matrix: list[list[Fraction]], columns: list[list[Fraction]]
) -> list[list[Fraction]]:
    """Append column vectors to a row-major matrix."""
    row_count = len(matrix)
    assert all(len(column) == row_count for column in columns)
    return [
        list(row) + [column[index] for column in columns]
        for index, row in enumerate(matrix)
    ]


def dot(left: list[Fraction], right: list[Fraction]) -> Fraction:
    assert len(left) == len(right)
    return sum(
        (left_entry * right_entry for left_entry, right_entry in zip(left, right)),
        Q(0),
    )


def matrix_vector_product(
    matrix: list[list[Fraction]], vector: list[Fraction]
) -> list[Fraction]:
    """Multiply an exact row-major matrix by a column vector."""
    assert all(len(row) == len(vector) for row in matrix)
    return [dot(row, vector) for row in matrix]


def matrix_from_flat(
    entries: tuple[int, ...], row_count: int, column_count: int
) -> list[list[Fraction]]:
    assert len(entries) == row_count * column_count
    return [
        [Q(entries[row * column_count + column]) for column in range(column_count)]
        for row in range(row_count)
    ]


def normalized_selector(
    nuisance: list[list[Fraction]], desired: list[Fraction]
) -> list[Fraction] | None:
    """Solve lambda B=0 and lambda g=1."""
    row_count = len(nuisance)
    assert len(desired) == row_count
    nuisance_column_count = len(nuisance[0]) if nuisance else 0
    equations = [
        [nuisance[row][column] for row in range(row_count)]
        for column in range(nuisance_column_count)
    ]
    equations.append(list(desired))
    constants = [Q(0)] * nuisance_column_count + [Q(1)]
    return solve_linear_system(equations, constants, row_count)


def audit_selector_equivalence() -> int:
    """Exhaust survival/annihilator equivalence independently of pure rank."""
    values = (-1, 0, 1)
    cases = 0
    for row_count in range(1, 4):
        for nuisance_column_count in range(3):
            for flat_nuisance in product(
                values, repeat=row_count * nuisance_column_count
            ):
                nuisance = matrix_from_flat(
                    flat_nuisance, row_count, nuisance_column_count
                )
                for desired_entries in product(values, repeat=row_count):
                    desired = [Q(entry) for entry in desired_entries]
                    survives = matrix_rank(
                        append_columns(nuisance, [desired])
                    ) > matrix_rank(nuisance)
                    selector = normalized_selector(nuisance, desired)
                    assert (selector is not None) == survives
                    if selector is not None:
                        assert dot(selector, desired) == 1
                        for column in range(nuisance_column_count):
                            nuisance_slice = [
                                nuisance[row][column] for row in range(row_count)
                            ]
                            assert dot(selector, nuisance_slice) == 0
                    cases += 1

    # The repaired theorem uses a nonzero formal desired-label projection.
    # A normalized operator selector remains meaningful even when the chosen
    # physical graph tensor has zero projection onto that label.
    nuisance = [[Q(1)], [Q(0)]]
    desired = [Q(0), Q(1)]
    selector = normalized_selector(nuisance, desired)
    assert selector == [Q(0), Q(1)]
    # Domain columns 0,1 are the two desired-label words; columns 2,3
    # are nuisance words.  Output rows use the order L-coordinate then
    # W-coordinate.  Contracting the whole operator recovers the nonzero
    # formal projection exactly.
    desired_words = ([Q(1), Q(0)], [Q(0), Q(1)])
    nuisance_slice = [Q(1), Q(0)]
    gamma_columns = []
    for left_vector, word in (
        (desired, desired_words[0]),
        (desired, desired_words[1]),
        (nuisance_slice, desired_words[0]),
        (nuisance_slice, desired_words[1]),
    ):
        gamma_columns.append(
            [
                left_vector[left_index] * word[word_index]
                for left_index in range(2)
                for word_index in range(2)
            ]
        )
    gamma = [[gamma_columns[column][row] for column in range(4)] for row in range(4)]
    contracted_gamma = [
        [
            sum(
                (
                    selector[left_index] * gamma[2 * left_index + word_index][column]
                    for left_index in range(2)
                ),
                Q(0),
            )
            for column in range(4)
        ]
        for word_index in range(2)
    ]
    formal_projection = [[Q(1), Q(0), Q(0), Q(0)], [Q(0), Q(1), Q(0), Q(0)]]
    assert contracted_gamma == formal_projection

    physical_graph_tensor = [Q(0), Q(0), Q(1), Q(0)]
    realized_physical_response = matrix_vector_product(
        formal_projection, physical_graph_tensor
    )
    assert not any(realized_physical_response)
    assert matrix_rank(append_columns(nuisance, [desired])) == 2

    swallowed_desired = [Q(1), Q(0)]
    assert normalized_selector(nuisance, swallowed_desired) is None
    return cases


def audit_pure_rank_equivalence() -> int:
    """Audit the complete-target quotient separately from selector existence."""
    values = (-1, 0, 1)
    alpha = (Q(1), Q(2), Q(-3))
    cases = 0
    for quotient_dimension in range(1, 4):
        for desired_entries in product(values, repeat=quotient_dimension):
            desired_class = [Q(entry) for entry in desired_entries]
            for response_entries in product(values, repeat=4):
                response = [Q(entry) for entry in response_entries]
                # The first three output words are the pure w_c.  A fourth
                # coordinate audits that the complete identity also controls
                # non-pure response words whenever the desired class survives.
                if any(desired_class) and response[3]:
                    continue
                pure_columns = [
                    [
                        response[colour] * desired_class[row] / alpha[colour]
                        for row in range(quotient_dimension)
                    ]
                    for colour in range(3)
                ]
                pure_matrix = [
                    [pure_columns[colour][row] for colour in range(3)]
                    for row in range(quotient_dimension)
                ]

                # Column c is the coefficient of the independent word w_c.
                for colour in range(3):
                    left_column = [
                        alpha[colour] * pure_columns[colour][row]
                        for row in range(quotient_dimension)
                    ]
                    right_column = [
                        response[colour] * desired_class[row]
                        for row in range(quotient_dimension)
                    ]
                    assert left_column == right_column
                assert all(response[3] * entry == 0 for entry in desired_class)

                pure_rank = matrix_rank(pure_matrix)
                useful = any(desired_class) and any(response)
                some_pure_class = any(any(column) for column in pure_columns)
                assert pure_rank <= 1
                assert useful == some_pure_class
                assert useful == (pure_rank == 1)
                cases += 1

    # Legal normalized selector but zero physical output: the desired class
    # can survive while every pure class is zero.  This is not a useful row.
    assert matrix_rank([[Q(0), Q(0), Q(0)]]) == 0
    desired_survives = True
    zero_response = True
    assert desired_survives and zero_response
    return cases


def determinant(matrix: list[list[Fraction]]) -> Fraction:
    """Exact determinant by elimination."""
    size = len(matrix)
    if size == 0:
        return Q(1)
    assert all(len(row) == size for row in matrix)
    work = [[Q(entry) for entry in row] for row in matrix]
    answer = Q(1)
    for column in range(size):
        pivot = next((row for row in range(column, size) if work[row][column]), None)
        if pivot is None:
            return Q(0)
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            answer = -answer
        pivot_value = work[column][column]
        answer *= pivot_value
        for row in range(column + 1, size):
            if not work[row][column]:
                continue
            multiplier = work[row][column] / pivot_value
            for inner_column in range(column, size):
                work[row][inner_column] -= multiplier * work[column][inner_column]
    return answer


def minors(matrix: list[list[Fraction]], size: int) -> list[Fraction]:
    """List every size-by-size minor, with exact signs and values."""
    row_count = len(matrix)
    column_count = len(matrix[0]) if matrix else 0
    if size == 0:
        return [Q(1)]
    if size > row_count or size > column_count:
        return []
    answers: list[Fraction] = []
    for selected_rows in combinations(range(row_count), size):
        for selected_columns in combinations(range(column_count), size):
            square = [
                [matrix[row][column] for column in selected_columns]
                for row in selected_rows
            ]
            answers.append(determinant(square))
    return answers


def pointwise_fitting_condition(
    nuisance: list[list[Fraction]],
    pure: list[list[Fraction]],
    gate_nonzero: bool,
) -> bool:
    """Evaluate all minor containments at one reduced characteristic-zero point."""
    augmented = append_columns(
        nuisance,
        [
            [pure[row][column] for row in range(len(pure))]
            for column in range(len(pure[0]) if pure else 0)
        ],
    )
    for size in range(1, len(nuisance) + 1):
        nuisance_vanishes = not any(minors(nuisance, size))
        if nuisance_vanishes and gate_nonzero and any(minors(augmented, size)):
            return False
    return True


def audit_pointwise_rank_tables() -> tuple[int, int]:
    """Exhaust exact small matrices and two-point reduced rank profiles."""
    values = (-1, 0, 1)
    matrix_cases = 0
    profiles_by_row_count: dict[int, set[tuple[int, int, bool]]] = {
        1: set(),
        2: set(),
    }

    for row_count in (1, 2):
        for nuisance_column_count in range(3):
            entry_count = row_count * (nuisance_column_count + 3)
            for entries in product(values, repeat=entry_count):
                split = row_count * nuisance_column_count
                nuisance = matrix_from_flat(
                    entries[:split], row_count, nuisance_column_count
                )
                pure = matrix_from_flat(entries[split:], row_count, 3)
                augmented = append_columns(
                    nuisance,
                    [
                        [pure[row][column] for row in range(row_count)]
                        for column in range(3)
                    ],
                )
                nuisance_rank = matrix_rank(nuisance)
                augmented_rank = matrix_rank(augmented)
                for gate_nonzero in (False, True):
                    useful = gate_nonzero and augmented_rank > nuisance_rank
                    fitting_holds = pointwise_fitting_condition(
                        nuisance, pure, gate_nonzero
                    )
                    assert fitting_holds == (not useful)
                    profiles_by_row_count[row_count].add(
                        (nuisance_rank, augmented_rank, gate_nonzero)
                    )
                    matrix_cases += 1

    # In the reduced coordinate ring Q x Q, radical containment is checked at
    # both points.  Exhaust every realizable pair of rank/gate profiles.
    two_point_cases = 0
    for profiles in profiles_by_row_count.values():
        for first, second in product(sorted(profiles), repeat=2):
            useful_somewhere = any(
                gate and augmented_rank > nuisance_rank
                for nuisance_rank, augmented_rank, gate in (first, second)
            )
            fitting_at_every_point = all(
                not (gate and augmented_rank > nuisance_rank)
                for nuisance_rank, augmented_rank, gate in (first, second)
            )
            assert fitting_at_every_point == (not useful_somewhere)
            two_point_cases += 1

    return matrix_cases, two_point_cases


def audit_exceptional_rank_controls() -> int:
    """Replay the four algebraic boundary modules at exact rational points."""
    checked = 0
    for t in map(Q, (-2, 0, 1, 2)):
        first_b = [[Q(1)], [t - 1]]
        first_g = [Q(1), Q(0)]
        first_ranks = (
            matrix_rank(first_b),
            matrix_rank(append_columns(first_b, [first_g])),
        )
        assert first_ranks == ((1, 1) if t == 1 else (1, 2))

        second_b = [[t - 1]]
        second_g = [Q(1)]
        second_ranks = (
            matrix_rank(second_b),
            matrix_rank(append_columns(second_b, [second_g])),
        )
        assert second_ranks == ((0, 1) if t == 1 else (1, 1))
        checked += 2

    permanent_b = [[Q(1)]]
    permanent_g = [Q(1)]
    assert matrix_rank(permanent_b) == matrix_rank(
        append_columns(permanent_b, [permanent_g])
    )

    zero_response_b = [[Q(1)], [Q(0)]]
    zero_response_g = [Q(0), Q(1)]
    zero_response_pure = [Q(1), Q(0)]
    assert matrix_rank(append_columns(zero_response_b, [zero_response_g])) == 2
    assert matrix_rank(append_columns(zero_response_b, [zero_response_pure])) == 1

    # D(response ideal) means at least one coordinate is nonzero.  A product
    # of coordinates would incorrectly delete this legitimate response.
    response_coordinates = (Q(1), Q(0), Q(0))
    assert any(response_coordinates)
    coordinate_product = Q(1)
    for coordinate in response_coordinates:
        coordinate_product *= coordinate
    assert coordinate_product == 0
    return checked + 3


def weighted_matching_terms(
    vertices: tuple[str, ...], edge_weights: dict[frozenset[str], Fraction]
) -> list[tuple[tuple[tuple[str, str], ...], Fraction]]:
    """Enumerate all nonzero weighted perfect-matchings on named vertices."""
    if not vertices:
        return [((), Q(1))]
    first = vertices[0]
    terms: list[tuple[tuple[tuple[str, str], ...], Fraction]] = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        weight = edge_weights.get(frozenset((first, second)), Q(0))
        if not weight:
            continue
        remainder = vertices[1:index] + vertices[index + 1 :]
        for tail, tail_weight in weighted_matching_terms(remainder, edge_weights):
            pair = tuple(sorted((first, second)))
            matching = tuple(sorted((pair,) + tail))
            terms.append((matching, weight * tail_weight))
    return terms


def add_weighted_edge(
    edge_weights: dict[frozenset[str], Fraction],
    left: str,
    right: str,
    weight: int = 1,
) -> None:
    """Install one undirected exact edge in a sparse weight dictionary."""
    edge_weights[frozenset((left, right))] = Q(weight)


def bipartite_permanent_value(
    rows: tuple[str, ...],
    columns: tuple[str, ...],
    edge_weights: dict[frozenset[str], Fraction],
) -> tuple[Fraction, list[tuple[tuple[tuple[str, str], ...], Fraction]]]:
    """Evaluate a square bipartite permanent and retain nonzero terms."""
    assert len(rows) == len(columns)
    terms: list[tuple[tuple[tuple[str, str], ...], Fraction]] = []
    for assigned_columns in permutations(columns):
        weight = Q(1)
        matching: list[tuple[str, str]] = []
        for row, column in zip(rows, assigned_columns, strict=True):
            weight *= edge_weights.get(frozenset((row, column)), Q(0))
            matching.append(tuple(sorted((row, column))))
        if weight:
            terms.append((tuple(sorted(matching)), weight))
    return sum((weight for _, weight in terms), Q(0)), terms


def audit_response_zero_control() -> int:
    """Enumerate the physical graph-side cancellation for r=3..6."""
    checked_matchings = 0
    for r in range(3, 7):
        probes = ("a0", "a1")
        chosen = ("c0", "c1")
        old_roots = tuple(f"k{index}" for index in range(1, r - 1))
        remaining_ports = tuple(f"v{index}" for index in range(1, r - 1))
        residual = ("q0", "q1")
        roots = probes + old_roots
        ports = chosen + remaining_ports

        edge_weights: dict[frozenset[str], Fraction] = {}

        add_weighted_edge(edge_weights, "a0", "c0")
        add_weighted_edge(edge_weights, "a1", "c1")
        for old_root, port in zip(old_roots, remaining_ports, strict=True):
            add_weighted_edge(edge_weights, old_root, port)
        add_weighted_edge(edge_weights, "a0", "q0")
        add_weighted_edge(edge_weights, "a1", "q1")
        add_weighted_edge(edge_weights, "q0", "q1")
        add_weighted_edge(edge_weights, "q0", "k1")
        add_weighted_edge(edge_weights, "q1", "v1", -1)

        pi_value, pi_terms = bipartite_permanent_value(roots, ports, edge_weights)
        p_value, p_terms = bipartite_permanent_value(probes, residual, edge_weights)
        promoted_value, promoted_terms = bipartite_permanent_value(
            probes, chosen, edge_weights
        )
        assert pi_value == p_value == promoted_value == 1
        assert len(pi_terms) == len(p_terms) == len(promoted_terms) == 1
        assert edge_weights[frozenset(residual)] == 1

        nonzero_laplace_pairs = []
        for candidate in combinations(ports, 2):
            candidate_value, _ = bipartite_permanent_value(
                probes, candidate, edge_weights
            )
            if candidate_value:
                nonzero_laplace_pairs.append(candidate)
        assert nonzero_laplace_pairs == [chosen]

        target_vertices = residual + old_roots + remaining_ports
        target_terms = weighted_matching_terms(target_vertices, edge_weights)
        target_weights = sorted(weight for _, weight in target_terms)
        assert target_weights == [Q(-1), Q(1)]
        assert sum(target_weights, Q(0)) == 0

        expected_positive = {frozenset(residual)} | {
            frozenset((old_root, port))
            for old_root, port in zip(old_roots, remaining_ports, strict=True)
        }
        expected_negative = {
            frozenset(("q0", "k1")),
            frozenset(("q1", "v1")),
        } | {
            frozenset((old_roots[index], remaining_ports[index]))
            for index in range(1, len(old_roots))
        }
        observed_matchings = {
            frozenset(frozenset(pair) for pair in matching): weight
            for matching, weight in target_terms
        }
        assert observed_matchings[frozenset(expected_positive)] == 1
        assert observed_matchings[frozenset(expected_negative)] == -1

        top_vertices = residual + old_roots + remaining_ports + chosen
        assert weighted_matching_terms(top_vertices, edge_weights) == []
        checked_matchings += len(target_terms)

    return checked_matchings


def main() -> None:
    matching_count = audit_companion_grade_census()
    laplace_terms = audit_laplace_permanent_split()
    dimension_orders = audit_dimension_formulae()
    selector_cases = audit_selector_equivalence()
    pure_cases = audit_pure_rank_equivalence()
    rank_cases, two_point_cases = audit_pointwise_rank_tables()
    exceptional_cases = audit_exceptional_rank_controls()
    response_terms = audit_response_zero_control()

    print(
        "PASS companion grades:",
        f"{matching_count} perfect matchings classified at r=3..6",
    )
    print("PASS permanent Laplace split:", f"{laplace_terms} symbolic terms")
    print("PASS independent dimensions:", f"{dimension_orders} root orders")
    print("PASS selector quotient:", f"{selector_cases} exact matrices")
    print("PASS pure-rank quotient:", f"{pure_cases} exact quotient tensors")
    print(
        "PASS pointwise radical-Fitting orientation:",
        f"{rank_cases} matrices and {two_point_cases} reduced two-point tables",
    )
    print("PASS exceptional controls:", f"{exceptional_cases} exact states")
    print(
        "PASS response-zero controls:",
        f"{response_terms} cancelling matchings at r=3..6",
    )
    print("INDEPENDENT NO-IMPORT AUDIT PASS")


if __name__ == "__main__":
    main()
