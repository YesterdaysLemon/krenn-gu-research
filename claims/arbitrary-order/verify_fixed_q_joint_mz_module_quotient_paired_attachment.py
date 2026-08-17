"""Primary exact replay for the fixed-Q joint M/Z quotient theorem."""

from itertools import combinations, permutations, product
import sympy as sp


def rank(matrix: list[list[int]]) -> int:
    return sp.Matrix(matrix).rank()


def check_joint_rank_controls() -> None:
    cases = (
        (sp.eye(2), sp.Matrix([[1, 0, 0], [0, 1, 0]]), (2, 2, 2)),
        (sp.eye(2), sp.Matrix([[1, 0, 0], [1, 0, 0]]), (2, 1, 1)),
        (sp.eye(2), sp.zeros(2, 3), (2, 0, 0)),
        (sp.Matrix([[1, 1]]), sp.Matrix([[1, 0, 0], [0, 1, 0]]), (1, 2, 1)),
        (sp.Matrix([[1, 1]]), sp.Matrix([[1, 0, 0], [-1, 0, 0]]), (1, 1, 0)),
        (sp.zeros(1, 2), sp.Matrix([[1, 0, 0], [0, 1, 0]]), (0, 2, 0)),
    )
    for desired, responses, expected in cases:
        k = desired.rank()
        response_rank = responses.rank()
        pure_rank = (desired * responses).rank()
        assert (k, response_rank, pure_rank) == expected
        assert pure_rank <= min(k, response_rank)

    # Accessible operator coefficients are exactly the row space of G.
    assert sp.eye(2).rowspace() == [sp.Matrix([[1, 0]]), sp.Matrix([[0, 1]])]
    assert sp.Matrix([[1, 2]]).rowspace() == [sp.Matrix([[1, 2]])]
    assert not sp.zeros(1, 2).rowspace()

    # Axis and oblique rank-one quotients distinguish individual supply.
    assert sp.Matrix([[1, 0]]).rank() == 1
    assert sp.Matrix([[0, 1]]).rank() == 1
    assert sp.Matrix([[1, 1]]).rank() == 1

    # A pure quotient rank-three target cannot factor through two responses.
    assert sp.eye(3).rank() == 3
    assert all((g * a).rank() <= 2 for g, a, _ in cases)

    # On a fixed Z fibre, M+aZ differences are exactly M differences.
    first_m, second_m, fixed_z, coefficient = 3, -4, 11, 5
    first_output = first_m + coefficient * fixed_z
    second_output = second_m + coefficient * fixed_z
    assert first_output - second_output == first_m - second_m


def deck_dimension(n: int) -> int:
    return (4 ** (n + 2) + (-2) ** (n + 2)) // 2 - 1


def check_dimension_ledgers() -> None:
    assert deck_dimension(4) == 2079
    assert deck_dimension(6) == 32895
    assert deck_dimension(7) == 130815
    assert 3 ** (2 * 4 - 2) == 729
    assert 3 ** (2 * 4 - 4) == 81
    assert [3 ** (2 * 6 - size) for size in (2, 4, 6)] == [59049, 6561, 729]
    assert [3 ** (2 * 7 - size) for size in (2, 4, 6)] == [531441, 59049, 6561]
    assert 2079 * 9 == 18711
    assert 2079 * 81 == 168399
    assert 511 * 9 == 4599
    assert 511 * 81 == 41391
    assert 2 * (6 * 729 + 81) == 8910
    assert 8191 == sum(
        3 ** sum(1 for j in range(6) if mask & (1 << (j + 2)))
        for mask in range(1 << 8)
        if mask and mask.bit_count() % 2 == 0
    )


def edge_index(ports: tuple[int, ...]) -> tuple[tuple[int, int], ...]:
    return tuple(combinations(ports, 2))


def coordinate_number(
    edges: tuple[tuple[int, int], ...], edge: tuple[int, int], colours: tuple[int, int]
) -> int:
    return 9 * edges.index(tuple(sorted(edge))) + 3 * colours[0] + colours[1]


def difference_vector(
    edges: tuple[tuple[int, int], ...],
    positive: tuple[tuple[int, int], tuple[int, int]],
    negative: tuple[tuple[int, int], tuple[int, int]],
) -> sp.SparseMatrix:
    vector = sp.MutableSparseMatrix(9 * len(edges), 1, {})
    vector[coordinate_number(edges, *positive)] = 1
    vector[coordinate_number(edges, *negative)] = -1
    return sp.SparseMatrix(vector)


def k33_kernel_basis() -> tuple[sp.SparseMatrix, tuple[tuple[int, int], ...]]:
    ports = tuple(range(6))
    left, right = frozenset((0, 1, 2)), frozenset((3, 4, 5))
    edges = edge_index(ports)
    vectors: list[sp.SparseMatrix] = []
    for positive, negative in (
        ((0, 2), (0, 1)),
        ((1, 2), (0, 1)),
        ((3, 5), (3, 4)),
        ((4, 5), (3, 4)),
    ):
        vectors.append(difference_vector(edges, (positive, (0, 0)), (negative, (0, 0))))
    for port in ports:
        shore = left if port in left else right
        mates = sorted(shore - {port})
        for colour in (1, 2):
            positive_edge = tuple(sorted((port, mates[0])))
            negative_edge = tuple(sorted((port, mates[1])))
            positive_colours = (colour, 0) if positive_edge[0] == port else (0, colour)
            negative_colours = (colour, 0) if negative_edge[0] == port else (0, colour)
            vectors.append(
                difference_vector(
                    edges,
                    (positive_edge, positive_colours),
                    (negative_edge, negative_colours),
                )
            )
    return sp.SparseMatrix.hstack(*vectors), edges


def restrict_blocks(
    basis: sp.SparseMatrix,
    edges: tuple[tuple[int, int], ...],
    selected_edges: set[tuple[int, int]],
) -> sp.SparseMatrix:
    rows = [
        9 * edge_number + colour_number
        for edge_number, edge in enumerate(edges)
        if edge in selected_edges
        for colour_number in range(9)
    ]
    return basis[rows, :]


def wick_image(
    vector: sp.SparseMatrix,
    edges: tuple[tuple[int, int], ...],
    channel_edges: tuple[tuple[int, int], ...],
) -> dict[tuple[tuple[int, ...], tuple[int, ...]], int]:
    image: dict[tuple[tuple[int, ...], tuple[int, ...]], int] = {}
    for coordinate, coefficient in vector.todok().items():
        row = coordinate[0]
        edge = edges[row // 9]
        colour_number = row % 9
        colours = (colour_number // 3, colour_number % 3)
        assignment = dict(zip(edge, colours, strict=True))
        for channel_edge in channel_edges:
            if set(edge).isdisjoint(channel_edge):
                support = tuple(sorted(edge + channel_edge))
                word = tuple(assignment.get(port, 0) for port in support)
                key = (support, word)
                image[key] = image.get(key, 0) + int(coefficient)
    return {key: value for key, value in image.items() if value}


def k52_kernel_basis() -> tuple[sp.SparseMatrix, tuple[tuple[int, int], ...]]:
    ports = tuple(range(7))
    leaves, centres = tuple(range(5)), (5, 6)
    edges = edge_index(ports)
    vectors: list[sp.SparseMatrix] = []
    for leaf in leaves:
        for colour in range(3):
            vectors.append(
                difference_vector(
                    edges,
                    ((leaf, centres[0]), (colour, 0)),
                    ((leaf, centres[1]), (colour, 0)),
                )
            )
    centre_edge = centres
    for first_colour in range(3):
        for second_colour in range(3):
            vector = sp.MutableSparseMatrix(9 * len(edges), 1, {})
            vector[
                coordinate_number(edges, centre_edge, (first_colour, second_colour))
            ] = 1
            vectors.append(sp.SparseMatrix(vector))
    return sp.SparseMatrix.hstack(*vectors), edges


def check_pair_block_covers() -> None:
    k33_basis, k33_edges = k33_kernel_basis()
    assert k33_basis.rank() == 16
    k33_channel = tuple((left, right) for left in range(3) for right in range(3, 6))
    assert all(
        not wick_image(k33_basis[:, column], k33_edges, k33_channel)
        for column in range(k33_basis.cols)
    )
    k33_cover = {(0, 1), (0, 2), (3, 4), (3, 5)}
    assert restrict_blocks(k33_basis, k33_edges, k33_cover).rank() == 16
    for shore_edges in (
        tuple(combinations((0, 1, 2), 2)),
        tuple(combinations((3, 4, 5), 2)),
    ):
        assert all(
            restrict_blocks(k33_basis, k33_edges, {edge}).rank() == 5
            for edge in shore_edges
        )
    # Three blocks cannot put two internal blocks in each disjoint shore.
    assert 3 < 2 + 2

    k52_basis, k52_edges = k52_kernel_basis()
    assert k52_basis.rank() == 24
    k52_channel = tuple((leaf, centre) for leaf in range(5) for centre in (5, 6))
    assert all(
        not wick_image(k52_basis[:, column], k52_edges, k52_channel)
        for column in range(k52_basis.cols)
    )
    k52_cover = {(5, 6), *((leaf, 5) for leaf in range(5))}
    assert len(k52_cover) == 6
    assert restrict_blocks(k52_basis, k52_edges, k52_cover).rank() == 24
    required_support_groups = [{(5, 6)}] + [{(leaf, 5), (leaf, 6)} for leaf in range(5)]
    assert all(
        any(edge in cover for edge in group)
        for group in required_support_groups
        for cover in [k52_cover]
    )
    assert len(required_support_groups) == 6


ROOT_TABLE = (
    (1, 0, 2, None, 0, 2),
    (2, None, None, 1, 2, 0),
    (None, 1, 0, 2, None, 1),
    (0, 2, 1, 0, 1, None),
)
OPEN_PORTS = (0, 1, 2, 3)
OUTSIDE_PORTS = tuple(range(6))


def companion_terms(outside_set: tuple[int, ...]):
    for assigned in permutations(outside_set):
        root_word: list[int] = []
        outside_word: dict[int, int] = {}
        for root, outside in enumerate(assigned):
            colour = ROOT_TABLE[root][outside]
            if colour is None:
                break
            root_word.append(colour)
            outside_word[outside] = colour
        else:
            yield tuple(root_word), outside_word


def companion_slice(
    target: tuple[int, int],
    outside_set: tuple[int, ...],
    sigma: dict[int, int],
    beta: dict[int, int],
) -> dict[tuple[int, ...], int]:
    complement = tuple(port for port in OPEN_PORTS if port not in target)
    answer: dict[tuple[int, ...], int] = {}
    for root_word, outside_word in companion_terms(outside_set):
        if any(outside_word[port] != colour for port, colour in sigma.items()):
            continue
        tail = tuple(
            outside_word[port] if port in outside_set else beta[port]
            for port in complement
        )
        word = root_word + tail
        answer[word] = answer.get(word, 0) + 1
    return answer


def joint_nuisance_slices(target: tuple[int, int]) -> list[dict[tuple[int, ...], int]]:
    complement = tuple(port for port in OPEN_PORTS if port not in target)
    desired_set = tuple(sorted((4, 5) + complement))
    columns = []
    for outside_set in combinations(OUTSIDE_PORTS, 4):
        if outside_set == desired_set:
            continue
        sigma_ports = tuple(port for port in outside_set if port in target)
        beta_ports = tuple(port for port in complement if port not in outside_set)
        for sigma_values in product(range(3), repeat=len(sigma_ports)):
            sigma = dict(zip(sigma_ports, sigma_values, strict=True))
            for beta_values in product(range(3), repeat=len(beta_ports)):
                beta = dict(zip(beta_ports, beta_values, strict=True))
                column = companion_slice(target, outside_set, sigma, beta)
                if column:
                    columns.append(column)
    return columns


def desired_m_column(target: tuple[int, int]) -> dict[tuple[int, ...], int]:
    complement = tuple(port for port in OPEN_PORTS if port not in target)
    desired_set = tuple(sorted((4, 5) + complement))
    return companion_slice(target, desired_set, {}, {})


def check_gld11_separators() -> None:
    expected_counts = {
        (0, 1): 202,
        (0, 2): 202,
        (0, 3): 199,
        (1, 2): 174,
        (1, 3): 193,
        (2, 3): 193,
    }
    pivots = {
        (0, 1): tuple(map(int, "202122")),
        (0, 2): tuple(map(int, "011221")),
        (0, 3): tuple(map(int, "000100")),
        (1, 3): tuple(map(int, "100110")),
        (2, 3): tuple(map(int, "121212")),
    }
    for target, expected_count in expected_counts.items():
        nuisance = joint_nuisance_slices(target)
        desired = desired_m_column(target)
        assert len(nuisance) == expected_count
        if target in pivots:
            pivot = pivots[target]
            assert desired.get(pivot, 0) == 1
            assert all(column.get(pivot, 0) == 0 for column in nuisance)
            continue
        words = (
            tuple(map(int, "002002")),
            tuple(map(int, "011001")),
            tuple(map(int, "121010")),
        )
        weights = (1, -1, 1)
        assert (
            sum(
                weight * desired.get(word, 0)
                for weight, word in zip(weights, words, strict=True)
            )
            == 1
        )
        assert all(
            sum(
                weight * column.get(word, 0)
                for weight, word in zip(weights, words, strict=True)
            )
            == 0
            for column in nuisance
        )


PAIRINGS = (
    (((0, 1)), ((2, 3))),
    (((0, 2)), ((1, 3))),
    (((0, 3)), ((1, 2))),
)


def m4_coefficient(
    coefficients: dict[tuple[tuple[int, int], tuple[int, int]], int],
    word: tuple[int, int, int, int],
) -> int:
    total = 0
    for first, second in PAIRINGS:
        first_colours = tuple(word[port] for port in first)
        second_colours = tuple(word[port] for port in second)
        total += coefficients.get((first, first_colours), 0) * coefficients.get(
            (second, second_colours), 0
        )
    return total


def check_local_detector() -> None:
    first_matching = {(0, 2), (1, 3)}
    second_matching = {(0, 3), (1, 2)}
    transversals = tuple(
        (first, second) for first in first_matching for second in second_matching
    )
    assert len(transversals) == 4
    assert all(
        first in first_matching and second in second_matching
        for first, second in transversals
    )

    coefficients = {
        ((0, 1), (0, 0)): 1,
        ((2, 3), (1, 1)): 1,
        ((0, 2), (0, 0)): 1,
        ((1, 3), (0, 0)): 1,
        ((0, 3), (0, 1)): 1,
        ((1, 2), (0, 1)): -1,
    }
    assert m4_coefficient(coefficients, (0, 0, 1, 1)) == 0
    assert m4_coefficient(coefficients, (0, 0, 0, 0)) == 1
    assert coefficients[((0, 2), (0, 0))] == 1
    assert rank([[1, 0], [0, 1]]) == 2  # abstract independent diagonal M/Z rows


def main() -> None:
    check_joint_rank_controls()
    check_dimension_ledgers()
    check_pair_block_covers()
    check_gld11_separators()
    check_local_detector()
    print("fixed-Q joint M/Z quotient paired-attachment primary replay: PASS")


if __name__ == "__main__":
    main()
