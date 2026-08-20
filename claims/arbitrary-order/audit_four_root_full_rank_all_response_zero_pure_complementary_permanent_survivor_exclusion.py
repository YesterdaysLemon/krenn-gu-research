"""Independent no-import audit for the GLS9 pure-Pi survivor exclusion.

This audit deliberately imports no repository module and does not share a
representation with the focused verifier.  It uses exact dual annihilators
instead of quotient spaces, reconstructs the labelled pair deck directly,
and compares the GLS9 fixture deck with the full ten-vertex matching sum.

The bounded rational-line census and finite coefficient replays below are
audits, not proofs of the arbitrary-field or arbitrary-point theorem.  The
written annihilator/quotient argument carries that mathematical burden.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from functools import cache
from itertools import combinations, permutations, product
from math import gcd, prod

COLOURS = (0, 1, 2)
ROOTS = ("r0", "r1", "r2", "r3")
Q0 = "q0"
Q1 = "q1"
PORTS = ("u0", "u1", "u2", "u3")
OUTSIDE = (Q0, Q1, *PORTS)
ALL_VERTICES = (*ROOTS, *OUTSIDE)
Q_PAIR = (Q0, Q1)
ACTIVE_PORTS = frozenset(("u0", "u1"))


def coordinate_vector(colour: int, dimension: int = 3) -> tuple[int, ...]:
    """Return a standard basis vector."""

    return tuple(int(index == colour) for index in range(dimension))


def dot(left: tuple[int, ...], right: tuple[int, ...]) -> int:
    """Exact integer pairing."""

    assert len(left) == len(right)
    return sum(a * b for a, b in zip(left, right, strict=True))


def normalize_projective_line(vector: tuple[int, int, int]) -> tuple[int, int, int]:
    """Choose the primitive representative whose first nonzero entry is positive."""

    assert any(vector)
    divisor = gcd(gcd(abs(vector[0]), abs(vector[1])), abs(vector[2]))
    primitive = tuple(entry // divisor for entry in vector)
    first = next(entry for entry in primitive if entry)
    if first < 0:
        primitive = tuple(-entry for entry in primitive)
    return primitive


def rational_projective_lines(height: int) -> tuple[tuple[int, int, int], ...]:
    """Enumerate exact rational lines having a primitive point in a height box."""

    representatives = {
        normalize_projective_line(vector)
        for vector in product(range(-height, height + 1), repeat=3)
        if any(vector)
    }
    return tuple(sorted(representatives))


def annihilator_basis(line: tuple[int, int, int]) -> tuple[tuple[int, int, int], ...]:
    """Construct two independent covectors annihilating a projective line."""

    pivot = next(index for index, entry in enumerate(line) if entry)
    answer = []
    for other in COLOURS:
        if other == pivot:
            continue
        covector = [0, 0, 0]
        covector[pivot] = -line[other]
        covector[other] = line[pivot]
        answer.append(tuple(covector))
    basis = tuple(answer)
    assert len(basis) == 2
    assert all(dot(covector, line) == 0 for covector in basis)
    return basis


def line_contains_colour(line: tuple[int, int, int], colour: int) -> bool:
    """Test coordinate-line incidence through the full dual annihilator."""

    return all(covector[colour] == 0 for covector in annihilator_basis(line))


def separating_annihilator(
    line: tuple[int, int, int], colour: int
) -> tuple[int, int, int]:
    """Return an annihilator nonzero on a coordinate excluded from the line."""

    assert not line_contains_colour(line, colour)
    for covector in annihilator_basis(line):
        if covector[colour]:
            return covector
    raise AssertionError("annihilator incidence test was inconsistent")


def add_tensors(
    *tensors: dict[tuple[int, ...], Fraction],
) -> dict[tuple[int, ...], Fraction]:
    """Add sparse exact coordinate tensors."""

    answer: Counter[tuple[int, ...]] = Counter()
    for tensor in tensors:
        answer.update(tensor)
    return {word: value for word, value in answer.items() if value}


def pure_tensor(
    colour: int, coefficient: Fraction, order: int = 4
) -> dict[tuple[int, ...], Fraction]:
    """Return one pure coordinate tensor."""

    return {(colour,) * order: coefficient}


def pure_insertion(
    slot: int,
    local_line: tuple[int, int, int],
    rest_colour: int,
    coefficient: Fraction,
    order: int = 4,
) -> dict[tuple[int, ...], Fraction]:
    """Insert a local covector against a pure tensor on all other slots."""

    answer = {}
    for local_colour, local_coefficient in enumerate(local_line):
        if not local_coefficient:
            continue
        word = [rest_colour] * order
        word[slot] = local_colour
        answer[tuple(word)] = coefficient * local_coefficient
    return answer


def audit_dual_line_incidence() -> dict[str, int]:
    """Audit the one-, two-, and three-site gates using dual annihilators."""

    lines = rational_projective_lines(height=2)
    coordinate_lines = tuple(coordinate_vector(colour) for colour in COLOURS)
    assert all(line in lines for line in coordinate_lines)

    singleton_cases = 0
    singleton_sharpness = 0
    two_site_cases = 0
    two_site_sharp_cases = 0

    for first_colour, second_colour in combinations(COLOURS, 2):
        for line in lines:
            singleton_cases += 1
            covered = {
                colour
                for colour in (first_colour, second_colour)
                if line_contains_colour(line, colour)
            }
            assert len(covered) <= 1
            missed_colour = next(
                colour
                for colour in (first_colour, second_colour)
                if colour not in covered
            )
            separator = separating_annihilator(line, missed_colour)
            assert dot(separator, line) == 0
            assert separator[missed_colour] != 0

        one_term = pure_insertion(
            0,
            coordinate_lines[first_colour],
            first_colour,
            Fraction(7, 5),
        )
        assert one_term == pure_tensor(first_colour, Fraction(7, 5))
        singleton_sharpness += 1

        sharp_ordered_pairs = set()
        for first_line in lines:
            for second_line in lines:
                two_site_cases += 1
                covered = {
                    colour
                    for colour in (first_colour, second_colour)
                    if line_contains_colour(first_line, colour)
                    or line_contains_colour(second_line, colour)
                }
                if len(covered) < 2:
                    missed_colour = next(
                        colour
                        for colour in (first_colour, second_colour)
                        if colour not in covered
                    )
                    first_separator = separating_annihilator(first_line, missed_colour)
                    second_separator = separating_annihilator(
                        second_line, missed_colour
                    )
                    # Pair the untouched slots with the missed-colour dual
                    # coordinate.  It kills the other pure term and leaves
                    # this exact nonzero product, while both insertion terms
                    # are killed by the two local annihilators.
                    assert (
                        first_separator[missed_colour] * second_separator[missed_colour]
                        != 0
                    )
                    continue

                first_is_first = line_contains_colour(first_line, first_colour)
                first_is_second = line_contains_colour(first_line, second_colour)
                second_is_first = line_contains_colour(second_line, first_colour)
                second_is_second = line_contains_colour(second_line, second_colour)
                assert (first_is_first and second_is_second) or (
                    first_is_second and second_is_first
                )
                sharp_ordered_pairs.add((first_line, second_line))

        expected_sharp_pairs = {
            (coordinate_lines[first_colour], coordinate_lines[second_colour]),
            (coordinate_lines[second_colour], coordinate_lines[first_colour]),
        }
        assert sharp_ordered_pairs == expected_sharp_pairs
        two_site_sharp_cases += len(sharp_ordered_pairs)

        left = pure_insertion(
            0,
            coordinate_lines[first_colour],
            first_colour,
            Fraction(2),
        )
        right = pure_insertion(
            1,
            coordinate_lines[second_colour],
            second_colour,
            Fraction(-3),
        )
        assert add_tensors(left, right) == add_tensors(
            pure_tensor(first_colour, Fraction(2)),
            pure_tensor(second_colour, Fraction(-3)),
        )

    two_line_triple_covers = 0
    for first_line in lines:
        for second_line in lines:
            covered = {
                colour
                for colour in COLOURS
                if line_contains_colour(first_line, colour)
                or line_contains_colour(second_line, colour)
            }
            if len(covered) == 3:
                two_line_triple_covers += 1
    assert two_line_triple_covers == 0

    # Three local lines are a sharp abstract boundary: one pair of insertion
    # tensors can use colours 0,2 and another can use colours 1,2.
    three_site_first = add_tensors(
        pure_insertion(0, coordinate_lines[0], 0, Fraction(2)),
        pure_insertion(2, coordinate_lines[2], 2, Fraction(-5)),
    )
    three_site_second = add_tensors(
        pure_insertion(1, coordinate_lines[1], 1, Fraction(3)),
        pure_insertion(2, coordinate_lines[2], 2, Fraction(-7)),
    )
    assert three_site_first == add_tensors(
        pure_tensor(0, Fraction(2)), pure_tensor(2, Fraction(-5))
    )
    assert three_site_second == add_tensors(
        pure_tensor(1, Fraction(3)), pure_tensor(2, Fraction(-7))
    )

    return {
        "projective_lines": len(lines),
        "singleton_cases": singleton_cases,
        "singleton_sharpness": singleton_sharpness,
        "two_site_cases": two_site_cases,
        "two_site_sharp_cases": two_site_sharp_cases,
        "two_line_triple_covers": two_line_triple_covers,
        "three_site_fibres": 2,
    }


def permutation_sign(permutation: tuple[int, ...]) -> int:
    """Return the sign of a permutation."""

    inversions = sum(
        permutation[left] > permutation[right]
        for left in range(len(permutation))
        for right in range(left + 1, len(permutation))
    )
    return -1 if inversions % 2 else 1


def determinant_three(matrix: tuple[tuple[Fraction, ...], ...]) -> Fraction:
    """Compute a 3 by 3 determinant exactly."""

    return sum(
        Fraction(permutation_sign(permutation))
        * prod(matrix[row][permutation[row]] for row in range(3))
        for permutation in permutations(range(3))
    )


def audit_determinant_pivot() -> dict[str, int]:
    """Verify the symbolic monomial and exact rational pivot implications."""

    symbolic_matrix = (
        ("H_ii", "H_ij", "H_ik"),
        (None, "H_jj", None),
        (None, "H_kj", "lambda"),
    )
    determinant_terms: Counter[tuple[str, ...]] = Counter()
    for permutation in permutations(range(3)):
        selected = tuple(symbolic_matrix[row][permutation[row]] for row in range(3))
        if any(entry is None for entry in selected):
            continue
        monomial = tuple(sorted(entry for entry in selected if entry is not None))
        determinant_terms[monomial] += permutation_sign(permutation)
    determinant_terms = Counter(
        {
            monomial: coefficient
            for monomial, coefficient in determinant_terms.items()
            if coefficient
        }
    )
    assert determinant_terms == Counter({("H_ii", "H_jj", "lambda"): 1})

    values = (
        Fraction(-2, 3),
        Fraction(-1),
        Fraction(0),
        Fraction(1, 2),
        Fraction(2),
    )
    specializations = 0
    full_rank_specializations = 0
    for h_ii, h_ij, h_ik, h_jj, h_kj, lam in product(values, repeat=6):
        matrix = (
            (h_ii, h_ij, h_ik),
            (Fraction(0), h_jj, Fraction(0)),
            (Fraction(0), h_kj, lam),
        )
        determinant = determinant_three(matrix)
        assert determinant == h_ii * h_jj * lam
        assert (determinant != 0) == (h_ii != 0 and h_jj != 0 and lam != 0)
        specializations += 1
        full_rank_specializations += int(determinant != 0)

    return {
        "symbolic_monomials": len(determinant_terms),
        "rational_specializations": specializations,
        "full_rank_specializations": full_rank_specializations,
    }


def zero_matrix() -> tuple[tuple[int, ...], ...]:
    """Return a 3 by 3 zero matrix."""

    return tuple(tuple(0 for _ in COLOURS) for _ in COLOURS)


def matrix_unit(
    row: int, column: int, coefficient: int = 1
) -> tuple[tuple[int, ...], ...]:
    """Return one exact 3 by 3 matrix unit."""

    return tuple(
        tuple(coefficient if (i, j) == (row, column) else 0 for j in COLOURS)
        for i in COLOURS
    )


def identity_matrix() -> tuple[tuple[int, ...], ...]:
    """Return the 3 by 3 identity."""

    return tuple(tuple(int(row == column) for column in COLOURS) for row in COLOURS)


def fixture_incidence() -> dict[str, tuple[tuple[int, ...], ...]]:
    """Reconstruct the GLS9 fixture's contracted root-incidence columns."""

    f0 = (1, 0, 0, 0)
    f1 = (0, 1, 0, 0)
    f2 = (0, 0, 1, 0)
    f3 = (0, 0, 0, 1)
    zero = (0, 0, 0, 0)
    return {
        "u0": (f1, f2, f0),
        "u1": (f2, f3, f1),
        "u2": (f3, zero, f2),
        "u3": (zero, zero, f3),
        Q0: (f0, f1, zero),
        Q1: (f2, f0, zero),
    }


def fixture_outside_blocks() -> dict[tuple[str, str], tuple[tuple[int, ...], ...]]:
    """Reconstruct the nonzero outside blocks of the GLS9 fixture."""

    return {
        Q_PAIR: identity_matrix(),
        (Q0, "u0"): matrix_unit(0, 0),
        (Q1, "u0"): matrix_unit(1, 0),
        (Q0, "u1"): matrix_unit(0, 1),
        (Q1, "u1"): matrix_unit(1, 1, -1),
    }


INCIDENCE = fixture_incidence()
OUTSIDE_BLOCKS = fixture_outside_blocks()
OUTSIDE_INDEX = {vertex: index for index, vertex in enumerate(OUTSIDE)}
ROOT_INDEX = {vertex: index for index, vertex in enumerate(ROOTS)}


def ordered_outside_pair(left: str, right: str) -> tuple[str, str]:
    """Order an outside pair in the fixed labelled-slot order."""

    if OUTSIDE_INDEX[left] < OUTSIDE_INDEX[right]:
        return left, right
    return right, left


def outside_block_value(
    left: str, right: str, left_colour: int, right_colour: int
) -> int:
    """Evaluate an oriented outside block coefficient."""

    pair = ordered_outside_pair(left, right)
    block = OUTSIDE_BLOCKS.get(pair, zero_matrix())
    if pair == (left, right):
        return block[left_colour][right_colour]
    return block[right_colour][left_colour]


def permanent_of_columns(columns: tuple[tuple[int, ...], ...]) -> int:
    """Compute the permanent of four labelled root-incidence columns."""

    assert len(columns) == 4
    assert all(len(column) == 4 for column in columns)
    return sum(
        prod(columns[permutation[row]][row] for row in range(4))
        for permutation in permutations(range(4))
    )


def complementary_permanent_coefficient(
    pair: tuple[str, str], colours: dict[str, int]
) -> int:
    """Evaluate one actual fixture complementary permanent coefficient."""

    complement = tuple(vertex for vertex in OUTSIDE if vertex not in pair)
    assert len(complement) == 4
    columns = tuple(INCIDENCE[vertex][colours[vertex]] for vertex in complement)
    return permanent_of_columns(columns)


def pair_deck_terms(word: tuple[int, ...]) -> dict[tuple[str, str], int]:
    """Return all fifteen labelled contracted-deck summands."""

    assert len(word) == len(OUTSIDE)
    colours = dict(zip(OUTSIDE, word, strict=True))
    answer = {}
    for pair in combinations(OUTSIDE, 2):
        edge_value = outside_block_value(
            pair[0], pair[1], colours[pair[0]], colours[pair[1]]
        )
        answer[pair] = edge_value * complementary_permanent_coefficient(pair, colours)
    assert len(answer) == 15
    return answer


def classify_pair_in_diagonal_fibre(pair: tuple[str, str], diagonal_colour: int) -> str:
    """Classify one of the fifteen labels before companion evaluation."""

    if pair == Q_PAIR:
        return "Q"
    if pair[0] in PORTS and pair[1] in PORTS:
        return "direct-zero"
    if Q0 in pair:
        port = pair[1] if pair[0] == Q0 else pair[0]
        if diagonal_colour != 0:
            return "q0-residual-zero"
        return "q0-insertion" if port in ACTIVE_PORTS else "q0-inactive"
    if Q1 in pair:
        port = pair[1] if pair[0] == Q1 else pair[0]
        if diagonal_colour != 1:
            return "q1-residual-zero"
        return "q1-insertion" if port in ACTIVE_PORTS else "q1-inactive"
    raise AssertionError(f"unclassified pair: {pair}")


def expected_diagonal_fibre_coefficient(
    diagonal_colour: int, port_word: tuple[int, ...]
) -> int:
    """Expand only the pair classes that survive one diagonal fibre."""

    assert diagonal_colour in (0, 1)
    assert len(port_word) == 4
    colours = {
        Q0: diagonal_colour,
        Q1: diagonal_colour,
        **dict(zip(PORTS, port_word, strict=True)),
    }
    q_value = outside_block_value(
        Q0, Q1, diagonal_colour, diagonal_colour
    ) * complementary_permanent_coefficient(Q_PAIR, colours)
    if diagonal_colour == 0:
        surviving_pairs = tuple((Q0, port) for port in ACTIVE_PORTS)
    else:
        surviving_pairs = tuple((Q1, port) for port in ACTIVE_PORTS)
    insertion_value = sum(
        outside_block_value(pair[0], pair[1], colours[pair[0]], colours[pair[1]])
        * complementary_permanent_coefficient(pair, colours)
        for pair in surviving_pairs
    )
    return q_value + insertion_value


@cache
def perfect_matchings(
    vertices: tuple[str, ...],
) -> tuple[tuple[tuple[str, str], ...], ...]:
    """Enumerate labelled perfect matchings recursively."""

    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for partner_index in range(1, len(vertices)):
        partner = vertices[partner_index]
        remainder = vertices[1:partner_index] + vertices[partner_index + 1 :]
        for tail in perfect_matchings(remainder):
            answer.append(((first, partner), *tail))
    return tuple(answer)


def contracted_edge_value(left: str, right: str, colours: dict[str, int]) -> int:
    """Evaluate one fixture edge after contracting all four root vectors."""

    left_is_root = left in ROOT_INDEX
    right_is_root = right in ROOT_INDEX
    if left_is_root and right_is_root:
        return 0
    if left_is_root:
        return INCIDENCE[right][colours[right]][ROOT_INDEX[left]]
    if right_is_root:
        return INCIDENCE[left][colours[left]][ROOT_INDEX[right]]
    return outside_block_value(left, right, colours[left], colours[right])


def full_matching_terms(
    word: tuple[int, ...],
) -> tuple[int, tuple[tuple[tuple[tuple[str, str], ...], int], ...]]:
    """Evaluate the full contracted ten-vertex matching sum."""

    colours = dict(zip(OUTSIDE, word, strict=True))
    nonzero_terms = []
    total = 0
    for matching in perfect_matchings(ALL_VERTICES):
        value = prod(
            contracted_edge_value(left, right, colours) for left, right in matching
        )
        if value:
            nonzero_terms.append((matching, value))
            total += value
    return total, tuple(nonzero_terms)


def audit_labelled_deck_and_fixture() -> dict[str, object]:
    """Audit both diagonal fibres and the exact off-target fixture coefficient."""

    pairs = tuple(combinations(OUTSIDE, 2))
    assert len(pairs) == 15
    assert len(set(pairs)) == 15

    first_classes = Counter(classify_pair_in_diagonal_fibre(pair, 0) for pair in pairs)
    second_classes = Counter(classify_pair_in_diagonal_fibre(pair, 1) for pair in pairs)
    assert first_classes == Counter(
        {
            "Q": 1,
            "direct-zero": 6,
            "q0-insertion": 2,
            "q0-inactive": 2,
            "q1-residual-zero": 4,
        }
    )
    assert second_classes == Counter(
        {
            "Q": 1,
            "direct-zero": 6,
            "q0-residual-zero": 4,
            "q1-insertion": 2,
            "q1-inactive": 2,
        }
    )

    diagonal_port_words = 0
    for diagonal_colour in (0, 1):
        for port_word in product(COLOURS, repeat=4):
            word = (diagonal_colour, diagonal_colour, *port_word)
            deck_value = sum(pair_deck_terms(word).values())
            assert deck_value == expected_diagonal_fibre_coefficient(
                diagonal_colour, port_word
            )
            diagonal_port_words += 1

    pi_q = {}
    for port_word in product(COLOURS, repeat=4):
        colours = dict(zip(PORTS, port_word, strict=True))
        value = complementary_permanent_coefficient(Q_PAIR, colours)
        if value:
            pi_q[port_word] = value
    assert pi_q == {(2, 2, 2, 2): 1}

    matchings = perfect_matchings(ALL_VERTICES)
    assert len(matchings) == 945
    complete_words = 0
    for word in product(COLOURS, repeat=6):
        deck_value = sum(pair_deck_terms(word).values())
        matching_value, _ = full_matching_terms(word)
        assert deck_value == matching_value
        complete_words += 1

    mixed_word = (0, 0, 2, 2, 2, 2)
    mixed_deck_terms = pair_deck_terms(mixed_word)
    nonzero_deck_terms = {
        pair: value for pair, value in mixed_deck_terms.items() if value
    }
    mixed_matching_value, nonzero_matching_terms = full_matching_terms(mixed_word)
    assert nonzero_deck_terms == {Q_PAIR: 1}
    assert mixed_matching_value == 1
    assert len(nonzero_matching_terms) == 1
    assert nonzero_matching_terms[0][1] == 1
    assert len(set(mixed_word)) > 1  # Its GHZ target coefficient is zero.

    return {
        "pair_labels": len(pairs),
        "first_fibre_classes": dict(sorted(first_classes.items())),
        "second_fibre_classes": dict(sorted(second_classes.items())),
        "diagonal_port_words": diagonal_port_words,
        "pi_q_words": 3**4,
        "complete_outside_words": complete_words,
        "full_matchings": len(matchings),
        "mixed_deck_nonzeros": len(nonzero_deck_terms),
        "mixed_full_nonzeros": len(nonzero_matching_terms),
        "mixed_coefficient": mixed_matching_value,
    }


def main() -> None:
    """Run every exact finite audit."""

    line_checks = audit_dual_line_incidence()
    pivot_checks = audit_determinant_pivot()
    deck_checks = audit_labelled_deck_and_fixture()

    print("four-root pure-Pi survivor independent no-import audit: PASS")
    print(f"  dual rational-line controls: {line_checks}")
    print(f"  determinant pivot controls: {pivot_checks}")
    print(f"  labelled deck and fixture controls: {deck_checks}")
    print("  exact bounded replay only; the written arbitrary-point proof is decisive")
    print("  no primary verifier or repository module imported")
    print("  open: det(H_Q)=0 and all weaker/nonzero-response attachment leaves")


if __name__ == "__main__":
    main()
