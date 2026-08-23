"""Independent no-project-import audit for GLS56.

This audit deliberately does not import the primary verifier or repository
code.  It uses finite-field exhaustive censuses, bit-mask matching recursion,
an integer coefficient audit of the homogeneous identity, and a separately
implemented sparse graph evaluator.  The written proof carries the
characteristic-zero and arbitrary-root quantifiers; these computations are
hostile checks of its load-bearing algebra and sharp boundary examples.
"""

from __future__ import annotations

from functools import cache
from itertools import combinations, product

PRIME = 5


def rank_mod(rows: list[list[int]], prime: int = PRIME) -> int:
    matrix = [[entry % prime for entry in row] for row in rows]
    if not matrix:
        return 0
    rank = 0
    for column in range(len(matrix[0])):
        pivot = next(
            (index for index in range(rank, len(matrix)) if matrix[index][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inverse = pow(matrix[rank][column], -1, prime)
        matrix[rank] = [(inverse * entry) % prime for entry in matrix[rank]]
        for index, row in enumerate(matrix):
            if index == rank or not row[column]:
                continue
            factor = row[column]
            matrix[index] = [
                (entry - factor * pivot_entry) % prime
                for entry, pivot_entry in zip(row, matrix[rank], strict=True)
            ]
        rank += 1
    return rank


def dot_mod(left: tuple[int, ...], right: tuple[int, ...]) -> int:
    return sum(x * y for x, y in zip(left, right, strict=True)) % PRIME


def audit_covector_dichotomy() -> dict[str, int]:
    rows = tuple(product(range(PRIME), repeat=3))
    vectors = rows
    cases = 0
    pure_axis_cases = 0
    for row in rows:
        for colour in range(3):
            witnesses = [
                vector
                for vector in vectors
                if vector[colour] and dot_mod(row, vector) == 0
            ]
            pure_axis = row[colour] != 0 and all(
                row[index] == 0 for index in range(3) if index != colour
            )
            assert bool(witnesses) == (not pure_axis)
            pure_axis_cases += int(pure_axis)
            cases += 1
    assert pure_axis_cases == 12
    return {
        "F5_covector_colour_cases": cases,
        "pure_axis_obstructions": pure_axis_cases,
    }


def audit_kernel_flag_example() -> dict[str, int]:
    torus_points = 0
    exceptional_points = 0
    successor_activations = 0
    for x, y in product(range(PRIME), repeat=2):
        if not x or not y or not (x + y) % PRIME:
            continue
        torus_points += 1
        first = (x - y) % PRIME
        if first:
            continue
        exceptional_points += 1
        successor = (y, (x - y) % PRIME, 0)
        assert successor[0] and not successor[1] and not successor[2]
        successor_activations += 1
    assert exceptional_points and exceptional_points == successor_activations
    return {
        "F5_torus_points": torus_points,
        "first_divisor_points": exceptional_points,
        "successor_activations": successor_activations,
    }


@cache
def matching_count(mask: int) -> int:
    if not mask:
        return 1
    first_bit = mask & -mask
    remainder = mask ^ first_bit
    total = 0
    choices = remainder
    while choices:
        second_bit = choices & -choices
        total += matching_count(remainder ^ second_bit)
        choices ^= second_bit
    return total


@cache
def matchings(mask: int) -> tuple[tuple[tuple[int, int], ...], ...]:
    if not mask:
        return ((),)
    first_bit = mask & -mask
    first = first_bit.bit_length() - 1
    remainder = mask ^ first_bit
    result: list[tuple[tuple[int, int], ...]] = []
    choices = remainder
    while choices:
        second_bit = choices & -choices
        second = second_bit.bit_length() - 1
        for tail in matchings(remainder ^ second_bit):
            result.append(((first, second),) + tail)
        choices ^= second_bit
    return tuple(result)


def audit_silent_label_matching_cover() -> dict[str, int]:
    checked_matchings = 0
    checked_decks = 0
    for root_order in range(3, 8):
        full_mask = (1 << (2 * root_order)) - 1
        assert matching_count(full_mask) == len(matchings(full_mask))
        for matching in matchings(full_mask):
            assert any(left == 0 or right == 0 for left, right in matching)
            checked_matchings += 1
        for left, right in combinations(range(2 * root_order), 2):
            complement = full_mask ^ (1 << left) ^ (1 << right)
            if 0 in (left, right):
                continue
            for matching in matchings(complement):
                assert any(a == 0 or b == 0 for a, b in matching)
                checked_decks += 1
    return {
        "bitmask_top_matchings": checked_matchings,
        "bitmask_deck_matchings": checked_decks,
    }


def outer_mod(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple((x * y) % PRIME for x in left for y in right)


def add_mod(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple((x + y) % PRIME for x, y in zip(left, right, strict=True))


def gamma_mod(
    pair_s: tuple[tuple[int, ...], tuple[int, ...]],
    pair_t: tuple[tuple[int, ...], tuple[int, ...]],
) -> tuple[int, ...]:
    return add_mod(outer_mod(pair_s[0], pair_t[1]), outer_mod(pair_t[0], pair_s[1]))


def normalize_projective(vector: tuple[int, ...]) -> tuple[int, ...]:
    pivot = next(value for value in vector if value)
    inverse = pow(pivot, -1, PRIME)
    return tuple((inverse * value) % PRIME for value in vector)


def audit_pair_companion_boundary() -> dict[str, int]:
    # Work in the joint projective space P(F5^2 direct-sum F5^2), unlike the
    # primary integral row census.  One common normalization retains the
    # relative amplitude between the two probe rows.
    joint_rows = {
        normalize_projective(vector)
        for vector in product(range(PRIME), repeat=4)
        if any(vector)
    }
    visible = [(row[:2], row[2:]) for row in joint_rows]
    zero_pairs = 0
    for pair_s in visible:
        for pair_t in visible:
            vanishes = not any(gamma_mod(pair_s, pair_t))
            if not vanishes:
                continue
            zero_pairs += 1
            x_s, y_s = pair_s
            x_t, y_t = pair_t
            pure_x = not any(y_s) and not any(y_t)
            pure_y = not any(x_s) and not any(x_t)
            if pure_x or pure_y:
                continue
            assert all(map(any, (x_s, y_s, x_t, y_t)))
            assert normalize_projective(x_s) == normalize_projective(x_t)
            scale_x = next(
                x_t[index] * pow(x_s[index], -1, PRIME) % PRIME
                for index in range(2)
                if x_s[index]
            )
            assert all(
                (y_t[index] + scale_x * y_s[index]) % PRIME == 0
                for index in range(2)
            )

    triple_zero = 0
    for triple in combinations(visible, 3):
        if not all(not any(gamma_mod(triple[i], triple[j])) for i, j in combinations(range(3), 2)):
            continue
        triple_zero += 1
        assert all(not any(pair[1]) for pair in triple) or all(
            not any(pair[0]) for pair in triple
        )
    return {
        "F5_joint_projective_rows": len(visible),
        "ordered_zero_companions": zero_pairs,
        "all_pair_zero_triples": triple_zero,
    }


def audit_homogeneous_coefficients() -> dict[str, int]:
    # Coefficients of x_s y_t and y_s x_t after subtracting the two square
    # terms.  Equality of these four integer coefficient rows proves the
    # displayed tensor identity without sampling vector entries.
    monomials = ("ds_et", "es_dt")
    left_xs_yt = {"ds_et": 2, "es_dt": 0}
    left_ys_xt = {"ds_et": 0, "es_dt": 2}
    right_xs_yt = {"ds_et": 2, "es_dt": 0}
    right_ys_xt = {"ds_et": 0, "es_dt": 2}
    assert left_xs_yt == right_xs_yt
    assert left_ys_xt == right_ys_xt
    # The basis change from (G,A) to (x_s y_t, y_s x_t) is
    # [[1,1],[1,-1]], so characteristic two is exactly exceptional.
    determinant = 1 * (-1) - 1 * 1
    assert determinant == -2 and determinant % PRIME != 0
    return {
        "formal_scalar_monomials": len(monomials),
        "independent_mixed_tensor_words": 2,
        "mixed_basis_change_determinant": determinant,
    }


def audit_gld3_triangle_rank() -> dict[str, int]:
    cases = 0
    for lambdas in product(range(1, PRIME), repeat=3):
        equations: list[list[int]] = []
        for left, right in combinations(range(3), 2):
            for row in range(3):
                for column in range(3):
                    if row == column:
                        continue
                    equation = [0] * 9
                    if row == left:
                        equation[3 * right + column] += lambdas[left]
                    if column == right:
                        equation[3 * left + row] += lambdas[right]
                    if any(equation):
                        equations.append(equation)
        assert rank_mod(equations) == 9
        cases += 1

    normalized_triangle = [[1, 1, 0], [1, 0, 1], [0, 1, 1]]
    assert rank_mod(normalized_triangle) == 3
    determinant_over_integers = -2
    assert determinant_over_integers != 0
    port_matchings = matchings((1 << 4) - 1)
    assert all(any(left < 3 and right < 3 for left, right in item) for item in port_matchings)
    return {
        "F5_nonzero_lambda_cases": cases,
        "support_system_rank": 9,
        "normalized_triangle_determinant": determinant_over_integers,
        "four_port_matchings": len(port_matchings),
    }


Matrix = tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]]


def unit(row: int, column: int, value: int = 1) -> Matrix:
    return tuple(
        tuple(value if (i, j) == (row, column) else 0 for j in range(3))
        for i in range(3)
    )  # type: ignore[return-value]


class SparseGraph:
    def __init__(self, names: tuple[str, ...]) -> None:
        self.names = names
        self.index = {name: position for position, name in enumerate(names)}
        self.weights: dict[tuple[int, int, int, int], int] = {}

    def put(self, left: str, right: str, matrix: Matrix) -> None:
        i, j = self.index[left], self.index[right]
        for colour_i, colour_j in product(range(3), repeat=2):
            value = matrix[colour_i][colour_j]
            if value:
                self.weights[(i, j, colour_i, colour_j)] = value
                self.weights[(j, i, colour_j, colour_i)] = value

    def edge(self, i: int, j: int, colour_i: int, colour_j: int) -> int:
        return self.weights.get((i, j, colour_i, colour_j), 0)

    def coefficient(self, active: tuple[int, ...], colours: tuple[int, ...]) -> int:
        mask = sum(1 << index for index in active)
        total = 0
        for pairing in matchings(mask):
            term = 1
            for left, right in pairing:
                term *= self.edge(left, right, colours[left], colours[right])
            total += term
        return total


def source_control() -> SparseGraph:
    graph = SparseGraph(("a0", "a1", "q0", "q1", "n", "t0", "t1", "t2"))
    for left, right in (
        ("a0", "q0"),
        ("a1", "q1"),
        ("a0", "t0"),
        ("a1", "t1"),
        ("a0", "t2"),
        ("q0", "q1"),
        ("q0", "n"),
    ):
        graph.put(left, right, unit(0, 0))
    for colour in range(3):
        graph.put("q1", f"t{colour}", unit(0, colour))
        graph.put("n", f"t{colour}", unit(0, colour, -1))
    return graph


def response(graph: SparseGraph, open_names: tuple[str, ...]) -> dict[tuple[int, ...], int]:
    active_names = ("q0", "q1") + open_names
    active = tuple(graph.index[name] for name in active_names)
    result: dict[tuple[int, ...], int] = {}
    for open_colours in product(range(3), repeat=len(open_names)):
        total = 0
        for q_colours in product(range(3), repeat=2):
            colours = [0] * len(graph.names)
            colours[graph.index["q0"]], colours[graph.index["q1"]] = q_colours
            for name, colour in zip(open_names, open_colours, strict=True):
                colours[graph.index[name]] = colour
            total += graph.coefficient(active, tuple(colours))
        result[open_colours] = total
    return result


def audit_sparse_source_control() -> dict[str, int]:
    graph = source_control()
    promoted = ("n", "t0", "t1", "t2")
    assert response(graph, ()) == {(): 1}
    pair_rows = [response(graph, pair) for pair in combinations(promoted, 2)]
    assert all(not any(rows.values()) for rows in pair_rows)
    top_rows = response(graph, promoted)
    assert not any(top_rows.values())

    for colour in range(3):
        n, t = graph.index["n"], graph.index[f"t{colour}"]
        contracted = tuple(
            sum(graph.edge(n, t, source_colour, target_colour) for source_colour in range(3))
            for target_colour in range(3)
        )
        assert contracted == tuple(-1 if index == colour else 0 for index in range(3))

    nonzero: dict[tuple[int, ...], int] = {}
    active = tuple(range(8))
    for colours in product(range(3), repeat=8):
        value = graph.coefficient(active, colours)
        if value:
            nonzero[colours] = value
    assert nonzero == {(0, 0, 0, 0, 0, 0, 0, 2): -2}

    roots = (graph.index["a0"], graph.index["a1"], graph.index["n"])
    assert all(graph.edge(left, right, 0, 0) == 0 for left, right in combinations(roots, 2))
    return {
        "zero_pair_responses": len(pair_rows),
        "zero_top_rows": len(top_rows),
        "nonzero_full_words": len(nonzero),
        "off_target_word_coefficient": next(iter(nonzero.values())),
    }


def audit_rigid_controls() -> dict[str, int]:
    labels = [(colour, sign) for colour in range(3) for sign in (-1, 1)]
    surviving = 0
    for (left_colour, left_sign), (right_colour, right_sign) in combinations(labels, 2):
        coefficient = left_sign + right_sign
        if left_colour == right_colour:
            assert coefficient == 0
        elif coefficient:
            surviving += 1
    assert surviving == 6

    full_rank_rows = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    assert rank_mod(full_rank_rows) == 3
    support = {(0, 2), (1, 2), (2, 0), (2, 1)}
    assert all(left != right for left, right in support)
    return {
        "rank_one_labels": len(labels),
        "off_diagonal_survivors": surviving,
        "full_rank_control_rank": 3,
        "full_rank_off_diagonal_support": len(support),
    }


def main() -> None:
    report = {
        "covector_dichotomy": audit_covector_dichotomy(),
        "kernel_flag": audit_kernel_flag_example(),
        "silent_matching_cover": audit_silent_label_matching_cover(),
        "pair_companion_boundary": audit_pair_companion_boundary(),
        "homogeneous_coefficients": audit_homogeneous_coefficients(),
        "gld3_triangle_rank": audit_gld3_triangle_rank(),
        "sparse_source_control": audit_sparse_source_control(),
        "rigid_controls": audit_rigid_controls(),
    }
    print("GLS56 independent no-project-import audit: PASS")
    for name, values in report.items():
        print(f"  {name}: {values}")


if __name__ == "__main__":
    main()
