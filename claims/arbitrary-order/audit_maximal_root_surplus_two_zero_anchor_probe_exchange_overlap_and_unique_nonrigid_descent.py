"""Independent no-project-import audit for GLS59.

This script imports neither the primary verifier nor repository code.  It
uses an F_5 covector census, bit-mask perfect matchings, finite injection
tables, custom modular row reduction, and a separately written sparse-cell
reconstruction of the mono/binary controls.
"""

from __future__ import annotations

from collections import Counter
from functools import cache
from itertools import permutations, product

PRIME = 5
Vector = tuple[int, int, int]
Matrix = tuple[Vector, Vector, Vector]
Edge = tuple[int, int]

ZERO_VECTOR: Vector = (0, 0, 0)
ZERO_MATRIX: Matrix = (ZERO_VECTOR, ZERO_VECTOR, ZERO_VECTOR)


def dot(left: tuple[int, ...], right: tuple[int, ...]) -> int:
    return sum(x * y for x, y in zip(left, right, strict=True))


def basis(colour: int) -> Vector:
    return tuple(int(index == colour) for index in range(3))  # type: ignore[return-value]


def cell(row: int, column: int) -> Matrix:
    return tuple(
        tuple(int((i, j) == (row, column)) for j in range(3))
        for i in range(3)
    )  # type: ignore[return-value]


def transpose(matrix: Matrix) -> Matrix:
    return tuple(
        tuple(matrix[row][column] for row in range(3))
        for column in range(3)
    )  # type: ignore[return-value]


def edge_matrix(edges: dict[Edge, Matrix], left: int, right: int) -> Matrix:
    if left < right:
        return edges.get((left, right), ZERO_MATRIX)
    return transpose(edges.get((right, left), ZERO_MATRIX))


def matvec(matrix: Matrix, vector: Vector) -> Vector:
    return tuple(dot(row, vector) for row in matrix)  # type: ignore[return-value]


def left_contract(vector: Vector, matrix: Matrix) -> Vector:
    return tuple(
        sum(vector[row] * matrix[row][column] for row in range(3))
        for column in range(3)
    )  # type: ignore[return-value]


def bilinear(left: Vector, matrix: Matrix, right: Vector) -> int:
    return dot(left, matvec(matrix, right))


def outer(left: Vector, right: Vector) -> Matrix:
    return tuple(tuple(x * y for y in right) for x in left)  # type: ignore[return-value]


def add_matrices(*matrices: Matrix) -> Matrix:
    return tuple(
        tuple(sum(matrix[row][column] for matrix in matrices) for column in range(3))
        for row in range(3)
    )  # type: ignore[return-value]


@cache
def matching_masks(vertex_mask: int) -> tuple[tuple[Edge, ...], ...]:
    if not vertex_mask:
        return ((),)
    first_bit = vertex_mask & -vertex_mask
    first = first_bit.bit_length() - 1
    rest = vertex_mask ^ first_bit
    result: list[tuple[Edge, ...]] = []
    partners = rest
    while partners:
        partner_bit = partners & -partners
        partner = partner_bit.bit_length() - 1
        for tail in matching_masks(rest ^ partner_bit):
            result.append(((first, partner),) + tail)
        partners ^= partner_bit
    return tuple(result)


def coefficient(
    vertex_mask: int, vectors: dict[int, Vector], edges: dict[Edge, Matrix]
) -> int:
    total = 0
    for matching in matching_masks(vertex_mask):
        value = 1
        for left, right in matching:
            value *= bilinear(vectors[left], edge_matrix(edges, left, right), vectors[right])
        total += value
    return total


def rank_mod_prime(rows: tuple[Vector, ...]) -> int:
    matrix = [list(entry % PRIME for entry in row) for row in rows if any(entry % PRIME for entry in row)]
    rank = 0
    for column in range(3):
        pivot = next((index for index in range(rank, len(matrix)) if matrix[index][column]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inverse = pow(matrix[rank][column], -1, PRIME)
        matrix[rank] = [(inverse * value) % PRIME for value in matrix[rank]]
        for index in range(len(matrix)):
            if index == rank:
                continue
            multiple = matrix[index][column]
            if multiple:
                matrix[index] = [
                    (value - multiple * pivot_value) % PRIME
                    for value, pivot_value in zip(matrix[index], matrix[rank], strict=True)
                ]
        rank += 1
    return rank


def audit_covectors_and_matching_partition() -> dict[str, int]:
    vectors = tuple(product(range(PRIME), repeat=3))
    cases = 0
    witness_count = 0
    pure_axes = 0
    for colour in range(3):
        for covector in vectors:
            cases += 1
            witnesses = [
                vector
                for vector in vectors
                if dot(covector, vector) % PRIME == 0 and vector[colour]
            ]
            pure = covector[colour] != 0 and all(
                covector[index] == 0 for index in range(3) if index != colour
            )
            assert bool(witnesses) == (not pure)
            witness_count += len(witnesses)
            pure_axes += int(pure)

    partner_counts: Counter[int] = Counter()
    matchings = matching_masks((1 << 8) - 1)
    for matching in matchings:
        root_edge = next(edge for edge in matching if 0 in edge)
        partner = root_edge[1] if root_edge[0] == 0 else root_edge[0]
        partner_counts[partner] += 1
    assert len(matchings) == 105
    assert partner_counts == Counter({label: 15 for label in range(1, 8)})
    return {
        "independent_F5_covector_cases": cases,
        "independent_F5_pure_axes": pure_axes,
        "independent_F5_coordinate_survivors": witness_count,
        "independent_eight_vertex_matchings": len(matchings),
        "independent_matchings_per_root_partner": min(partner_counts.values()),
    }


def audit_overlap_table() -> dict[str, int]:
    injections = tuple(permutations(range(5), 3))
    intersection_sizes: Counter[int] = Counter()
    overlap_types: Counter[str] = Counter()
    rank_types: Counter[int] = Counter()
    for first in injections:
        for second in injections:
            shared = set(first) & set(second)
            assert shared
            intersection_sizes[len(shared)] += 1
            for label in shared:
                left_colour = first.index(label)
                right_colour = second.index(label)
                rank = rank_mod_prime((basis(left_colour), basis(right_colour)))
                rank_types[rank] += 1
                overlap_types["same" if left_colour == right_colour else "cross"] += 1
                assert rank == (1 if left_colour == right_colour else 2)
    assert sum(intersection_sizes.values()) == 3600
    assert set(intersection_sizes) == {1, 2, 3}
    assert overlap_types == Counter(same=2160, cross=4320)
    assert rank_types == Counter({1: 2160, 2: 4320})
    return {
        "independent_star_pair_cases": sum(intersection_sizes.values()),
        "independent_overlap_size_one_cases": intersection_sizes[1],
        "independent_overlap_size_two_cases": intersection_sizes[2],
        "independent_overlap_size_three_cases": intersection_sizes[3],
        "independent_same_axis_overlaps": overlap_types["same"],
        "independent_cross_axis_overlaps": overlap_types["cross"],
    }


def control(kind: str) -> tuple[dict[Edge, Matrix], Vector, Vector, set[int]]:
    edges: dict[Edge, Matrix] = {}
    k = (1, 1, 1)
    if kind == "same":
        ell = (0, 1, 1)
        entries = {
            (0, 3): (0, 0), (1, 3): (0, 0),
            (0, 4): (1, 1), (1, 5): (1, 1),
            (1, 6): (2, 2), (0, 7): (2, 2),
            (2, 3): (0, 0), (2, 4): (0, 2), (2, 6): (0, 1),
            (3, 5): (1, 2), (3, 7): (1, 1),
        }
        target = {1, 2}
    else:
        ell = (0, 0, 1)
        entries = {
            (0, 3): (0, 0), (1, 3): (1, 1),
            (0, 4): (1, 1), (0, 5): (2, 2),
            (1, 6): (0, 0), (1, 7): (2, 2),
            (2, 3): (0, 0), (2, 4): (0, 2), (2, 6): (0, 1),
            (3, 6): (2, 2),
        }
        target = {2}
    edges.update({edge: cell(*position) for edge, position in entries.items()})
    return edges, k, ell, target


def effective_edges(edges: dict[Edge, Matrix], k: Vector, ell: Vector) -> dict[Edge, Matrix]:
    result: dict[Edge, Matrix] = {}
    ports = (4, 5, 6, 7)
    for root in (0, 1):
        for port in ports:
            result[(root, port)] = edge_matrix(edges, root, port)
    h = bilinear(k, edge_matrix(edges, 2, 3), ell)
    a = {port: left_contract(k, edge_matrix(edges, 2, port)) for port in ports}
    b = {port: left_contract(ell, edge_matrix(edges, 3, port)) for port in ports}
    for index, left in enumerate(ports):
        for right in ports[index + 1 :]:
            raw = edge_matrix(edges, left, right)
            result[(left, right)] = add_matrices(
                tuple(tuple(h * value for value in row) for row in raw),  # type: ignore[arg-type]
                outer(a[left], b[right]),
                outer(b[left], a[right]),
            )
    return result


def image_axis(matrix: Matrix) -> int | None:
    columns = {column for row in range(3) for column in range(3) if matrix[row][column]}
    return next(iter(columns)) if len(columns) == 1 else None


def vector_axis(vector: Vector) -> int | None:
    support = [index for index, value in enumerate(vector) if value]
    return support[0] if len(support) == 1 else None


def audit_sparse_control(kind: str) -> dict[str, int]:
    edges, k, ell, target = control(kind)
    effective = effective_edges(edges, k, ell)
    open_vertices = (0, 1, 4, 5, 6, 7)
    full_mask = (1 << 8) - 1
    open_mask = sum(1 << vertex for vertex in open_vertices)

    ranks = {}
    for label in range(2, 8):
        rows = edge_matrix(edges, 0, label) + edge_matrix(edges, 1, label)
        ranks[label] = rank_mod_prime(rows)
    assert ranks[2] == 0
    assert ranks[3] == (1 if kind == "same" else 2)
    assert all(ranks[label] == 1 for label in range(4, 8))

    probe_stars = []
    for root in (0, 1):
        axes = {
            image_axis(edge_matrix(edges, root, label))
            for label in range(3, 8)
            if image_axis(edge_matrix(edges, root, label)) is not None
        }
        assert axes == {0, 1, 2}
        probe_stars.append(len(axes))
    n_axes = {
        vector_axis(left_contract(k, edge_matrix(edges, 2, label)))
        for label in range(3, 8)
        if vector_axis(left_contract(k, edge_matrix(edges, 2, label))) is not None
    }
    assert n_axes == {0, 1, 2}

    supported: Counter[tuple[int, ...]] = Counter()
    checks = 0
    for word in product(range(3), repeat=6):
        vectors = {vertex: basis(colour) for vertex, colour in zip(open_vertices, word, strict=True)}
        full_vectors = dict(vectors)
        full_vectors[2] = k
        full_vectors[3] = ell
        left = coefficient(full_mask, full_vectors, edges)
        right = coefficient(open_mask, vectors, effective)
        assert left == right
        wanted = int(len(set(word)) == 1 and word[0] in target)
        assert right == wanted
        if right:
            supported[word] += right
        checks += 1
    assert supported == Counter({(colour,) * 6: 1 for colour in target})
    return {
        f"independent_{kind}_coefficient_checks": checks,
        f"independent_{kind}_rigid_labels": sum(ranks[label] > 0 for label in range(3, 8)),
        f"independent_{kind}_probe_stars": sum(probe_stars),
        f"independent_{kind}_nonrigid_star_colours": len(n_axes),
        f"independent_{kind}_target_words": len(supported),
    }


def audit_silence_shortage() -> dict[str, int]:
    labels = tuple(range(5))
    triples = tuple(permutations(labels, 3))
    cases = 0
    for silent in triples:
        survivors = set(labels) - set(silent)
        assert len(survivors) == 2
        for proposed in triples:
            assert not set(proposed) <= survivors
        cases += 1
    return {
        "independent_silent_star_cases": cases,
        "independent_surviving_labels": 2,
    }


def main() -> None:
    results: dict[str, int] = {}
    results.update(audit_covectors_and_matching_partition())
    results.update(audit_overlap_table())
    results.update(audit_sparse_control("same"))
    results.update(audit_sparse_control("cross"))
    results.update(audit_silence_shortage())
    for key in sorted(results):
        print(f"{key}={results[key]}")
    print("GLS59 independent no-project-import audit: PASS")


if __name__ == "__main__":
    main()
