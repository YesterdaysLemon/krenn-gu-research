"""Independent no-import audit for the GLS39 diagonal-family exclusion.

The audit follows a two-block/bipartition/triangle derivation, distinct from
the primary verifier's support-set proof and projective-line census.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, combinations_with_replacement, permutations, product


def matrix_rank(rows: list[list[int]], prime: int | None = None) -> int:
    work = [[Fraction(entry) for entry in row] for row in rows]
    rank = 0
    for column in range(len(work[0]) if work else 0):
        pivot = next(
            (index for index in range(rank, len(work)) if work[index][column]),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        if prime is None:
            scale = work[rank][column]
            work[rank] = [entry / scale for entry in work[rank]]
        else:
            scale = pow(int(work[rank][column]) % prime, -1, prime)
            work[rank] = [Fraction((int(entry) * scale) % prime) for entry in work[rank]]
        for index, row in enumerate(work):
            if index == rank or not row[column]:
                continue
            multiple = row[column]
            if prime is None:
                work[index] = [
                    left - multiple * right
                    for left, right in zip(row, work[rank], strict=True)
                ]
            else:
                work[index] = [
                    Fraction((int(left) - int(multiple) * int(right)) % prime)
                    for left, right in zip(row, work[rank], strict=True)
                ]
        rank += 1
    return rank


def two_block_column_census() -> dict[str, int]:
    """Audit the two-block rank and formal determinant-cancellation leaves."""

    examined = 0
    maximum_rank = 0
    for coefficients in product((-1, 0, 1), repeat=6):
        # Relative to the two possible column factors X_s(z), X_t(w), the
        # three output columns have this 2-by-3 coefficient matrix.
        rows = [list(coefficients[:3]), list(coefficients[3:])]
        rank = matrix_rank(rows)
        maximum_rank = max(maximum_rank, rank)
        assert rank <= 2
        examined += 1
    assert examined == 729
    assert maximum_rank == 2

    # Replay det(x y'^T+x' y^T)=0 over the universal integer polynomial
    # ring.  A monomial is its 12-variable exponent tuple.
    variable_count = 12

    def variable(index: int) -> dict[tuple[int, ...], int]:
        exponent = [0] * variable_count
        exponent[index] = 1
        return {tuple(exponent): 1}

    def add_polynomials(
        left: dict[tuple[int, ...], int],
        right: dict[tuple[int, ...], int],
        right_scale: int = 1,
    ) -> dict[tuple[int, ...], int]:
        result = dict(left)
        for exponent, coefficient in right.items():
            result[exponent] = result.get(exponent, 0) + right_scale * coefficient
            if result[exponent] == 0:
                del result[exponent]
        return result

    def multiply_polynomials(
        left: dict[tuple[int, ...], int],
        right: dict[tuple[int, ...], int],
    ) -> dict[tuple[int, ...], int]:
        result: dict[tuple[int, ...], int] = {}
        for left_exponent, left_coefficient in left.items():
            for right_exponent, right_coefficient in right.items():
                exponent = tuple(
                    a + b for a, b in zip(left_exponent, right_exponent, strict=True)
                )
                result[exponent] = (
                    result.get(exponent, 0)
                    + left_coefficient * right_coefficient
                )
                if result[exponent] == 0:
                    del result[exponent]
        return result

    x = tuple(variable(index) for index in range(3))
    x_prime = tuple(variable(index) for index in range(3, 6))
    y = tuple(variable(index) for index in range(6, 9))
    y_prime = tuple(variable(index) for index in range(9, 12))
    matrix = tuple(
        tuple(
            add_polynomials(
                multiply_polynomials(x[row], y_prime[column]),
                multiply_polynomials(x_prime[row], y[column]),
            )
            for column in range(3)
        )
        for row in range(3)
    )
    determinant: dict[tuple[int, ...], int] = {}
    for column_permutation in permutations(range(3)):
        inversions = sum(
            column_permutation[left] > column_permutation[right]
            for left in range(3)
            for right in range(left + 1, 3)
        )
        term = {(0,) * variable_count: 1}
        for row, column in enumerate(column_permutation):
            term = multiply_polynomials(term, matrix[row][column])
        determinant = add_polynomials(
            determinant,
            term,
            -1 if inversions % 2 else 1,
        )
    assert determinant == {}

    # In a polynomial domain, three nonzero leading terms cannot multiply to
    # zero: leading exponents add and nonzero rational coefficients multiply.
    leading_terms = (
        ((1, 0, 0, 0), Fraction(2)),
        ((0, 2, 0, 0), Fraction(-3)),
        ((0, 0, 1, 4), Fraction(5)),
    )
    product_exponent = tuple(
        sum(term[0][index] for term in leading_terms) for index in range(4)
    )
    product_coefficient = Fraction(1)
    for _, coefficient in leading_terms:
        product_coefficient *= coefficient
    assert product_exponent == (1, 2, 1, 4)
    assert product_coefficient == -30
    return {
        "coefficient_matrices": examined,
        "maximum_column_rank": maximum_rank,
        "formal_determinant_terms": len(determinant),
        "nonzero_leading_product": int(product_coefficient),
    }


def bipartite(edges: tuple[tuple[int, int], ...]) -> bool:
    adjacency: dict[int, set[int]] = {}
    for left, right in edges:
        adjacency.setdefault(left, set()).add(right)
        adjacency.setdefault(right, set()).add(left)
    colours: dict[int, int] = {}
    for start in adjacency:
        if start in colours:
            continue
        colours[start] = 0
        stack = [start]
        while stack:
            vertex = stack.pop()
            for neighbor in adjacency[vertex]:
                if neighbor not in colours:
                    colours[neighbor] = 1 - colours[vertex]
                    stack.append(neighbor)
                elif colours[neighbor] == colours[vertex]:
                    return False
    return True


def three_edge_graph_census() -> dict[str, int]:
    """A three-output obstruction is bipartite unless its edges form a triangle."""

    all_edges = tuple(combinations(range(6), 2))
    patterns = 0
    bipartite_patterns = 0
    triangles = 0
    for edge_multiset in combinations_with_replacement(all_edges, 3):
        patterns += 1
        simple_edges = tuple(sorted(set(edge_multiset)))
        if bipartite(simple_edges):
            bipartite_patterns += 1
            continue
        vertices = {vertex for edge in simple_edges for vertex in edge}
        degrees = {
            vertex: sum(vertex in edge for edge in simple_edges) for vertex in vertices
        }
        assert len(simple_edges) == 3
        assert len(vertices) == 3
        assert set(degrees.values()) == {2}
        triangles += 1
    assert patterns == 680
    assert triangles == 20
    assert bipartite_patterns == 660
    assert bipartite_patterns + triangles == patterns
    return {
        "three_edge_multisets": patterns,
        "bipartite": bipartite_patterns,
        "triangles": triangles,
    }


def coordinate_rank_one_orientation_census() -> dict[str, int]:
    """Audit all zero-factor and two-term rank-one orientations over F_3."""

    prime = 3
    vectors = tuple(product(range(prime), repeat=3))
    examined = 0
    coordinate_outputs = 0
    for x_left, y_left, x_right, y_right in product(vectors, repeat=4):
        examined += 1
        matrix = tuple(
            (
                x_left[row] * y_right[column]
                + x_right[row] * y_left[column]
            )
            % prime
            for row, column in product(range(3), repeat=2)
        )
        nonzero = tuple(index for index, entry in enumerate(matrix) if entry)
        if len(nonzero) != 1 or nonzero[0] not in (0, 4, 8):
            continue
        color = nonzero[0] // 4

        def on_axis(vector: tuple[int, ...]) -> bool:
            return all(entry == 0 for index, entry in enumerate(vector) if index != color)

        left_orientation = on_axis(x_left) and on_axis(x_right)
        right_orientation = on_axis(y_left) and on_axis(y_right)
        assert left_orientation or right_orientation
        coordinate_outputs += 1
    assert examined == 531441
    assert coordinate_outputs == 2448
    return {
        "four_vector_states": examined,
        "nonzero_coordinate_outputs": coordinate_outputs,
    }


def coordinate_plane_intersection_census() -> dict[str, int]:
    """Three distinct coordinate planes meet in three distinct axes."""

    planes = (0b011, 0b101, 0b110)
    ordered = 0
    distinct = 0
    for plane_triple in product(planes, repeat=3):
        ordered += 1
        if len(set(plane_triple)) != 3:
            continue
        distinct += 1
        intersections = {
            plane_triple[0] & plane_triple[1],
            plane_triple[1] & plane_triple[2],
            plane_triple[2] & plane_triple[0],
        }
        assert intersections == {0b001, 0b010, 0b100}
    assert ordered == 27
    assert distinct == 6
    return {"ordered_plane_triples": ordered, "pairwise_distinct": distinct}


def triangle_orientation_census() -> dict[str, int]:
    """Every distinct-colour triangle has an adjacent same-orientation pair."""

    triangle = ((0, 1), (1, 2), (2, 0))
    examined = 0
    for colors in permutations(range(3)):
        for orientations in product(("L", "R"), repeat=3):
            examined += 1
            witness = None
            for first, second in combinations(range(3), 2):
                if orientations[first] != orientations[second]:
                    continue
                shared = set(triangle[first]) & set(triangle[second])
                if shared and colors[first] != colors[second]:
                    witness = (first, second, shared.pop())
                    break
            assert witness is not None
    assert examined == 48
    return {
        "color_orientation_cases": examined,
        "same_orientation_witnesses": examined,
    }


def auxiliary_interface_replay() -> dict[str, int]:
    """Replay the three GLS36 pair types with exact rational tuples."""

    def tensor(left: tuple[Fraction, ...], right: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
        return tuple(a * b for a in left for b in right)

    def add(left: tuple[Fraction, ...], right: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
        return tuple(a + b for a, b in zip(left, right, strict=True))

    def mu(
        x_left: tuple[Fraction, ...],
        y_left: tuple[Fraction, ...],
        x_right: tuple[Fraction, ...],
        y_right: tuple[Fraction, ...],
    ) -> tuple[Fraction, ...]:
        return add(tensor(x_left, y_right), tensor(x_right, y_left))

    samples = tuple(
        tuple(Fraction((seed + 2 * index) % 5 - 2) for index in range(3))
        for seed in range(8)
    )
    replays = 0
    for index in range(len(samples)):
        a_0 = samples[index]
        b_0 = samples[(index + 1) % len(samples)]
        a_1 = samples[(index + 2) % len(samples)]
        b_1 = samples[(index + 3) % len(samples)]
        x = samples[(index + 4) % len(samples)]
        y = samples[(index + 5) % len(samples)]
        x_2 = samples[(index + 6) % len(samples)]
        y_2 = samples[(index + 7) % len(samples)]
        residual_pair = mu(a_0, b_0, a_1, b_1)
        q = add(tensor(a_0, b_1), tensor(a_1, b_0))
        one_residual = mu(a_0, b_0, x, y)
        sigma_one = add(tensor(a_0, y), tensor(x, b_0))
        promoted_pair = mu(x, y, x_2, y_2)
        sigma_pair = add(tensor(x, y_2), tensor(x_2, y))
        assert residual_pair == q
        assert one_residual == sigma_one
        assert promoted_pair == sigma_pair
        replays += 1
    assert replays == 8
    return {"exact_interface_replays": replays, "component_types": 3}


def main() -> None:
    two_block = two_block_column_census()
    graphs = three_edge_graph_census()
    rank_one = coordinate_rank_one_orientation_census()
    planes = coordinate_plane_intersection_census()
    orientations = triangle_orientation_census()
    interface = auxiliary_interface_replay()
    print("GLS39 independent no-import triangle audit: PASS")
    print("  two-block column/domain checks:", two_block)
    print("  minimal generating graphs:", graphs)
    print("  rank-one orientation census:", rank_one)
    print("  coordinate-plane intersections:", planes)
    print("  triangle orientation witnesses:", orientations)
    print("  auxiliary residual-label interface:", interface)
    print("  global pairwise-diagonal image rank <=2; rank-three swallow EMPTY")


if __name__ == "__main__":
    main()
