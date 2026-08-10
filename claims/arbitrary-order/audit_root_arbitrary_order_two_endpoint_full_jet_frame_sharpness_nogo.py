"""No-import audit of the arbitrary-order two-endpoint sharpness graph."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from functools import cache

# Use a different coordinate permutation from the primary verifier.
P = 2
Q = 0
C = 1
BASIS = tuple(tuple(int(i == j) for i in range(3)) for j in range(3))
ONE = (1, 1, 1)
PHI = {
    P: tuple(BASIS[P][i] - BASIS[C][i] for i in range(3)),
    Q: tuple(BASIS[Q][i] - BASIS[C][i] for i in range(3)),
}


def outer(left, right):
    return tuple(tuple(left[i] * right[j] for j in range(3)) for i in range(3))


def transpose(matrix):
    return tuple(tuple(matrix[j][i] for j in range(3)) for i in range(3))


def bilinear(left, matrix, right):
    return sum(left[i] * matrix[i][j] * right[j] for i in range(3) for j in range(3))


def left_row(left, matrix):
    return tuple(sum(left[i] * matrix[i][j] for i in range(3)) for j in range(3))


def rational_rank(rows):
    work = [[Fraction(value) for value in row] for row in rows]
    if not work:
        return 0
    row_count = len(work)
    column_count = len(work[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next((i for i in range(pivot_row, row_count) if work[i][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [value / scale for value in work[pivot_row]]
        for i in range(row_count):
            if i == pivot_row or not work[i][column]:
                continue
            multiple = work[i][column]
            work[i] = [work[i][j] - multiple * work[pivot_row][j] for j in range(column_count)]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def anchored_permanent(matrix):
    size = len(matrix)

    @cache
    def recurse(row, available):
        if row == size:
            return int(available == 0)
        total = 0
        for column in range(size):
            bit = 1 << column
            if available & bit:
                total += matrix[row][column] * recurse(row + 1, available ^ bit)
        return total

    return recurse(0, (1 << size) - 1)


def construct(r):
    m = r + 2
    roots = tuple(range(r))
    blockers = tuple(range(r, r + m))
    endpoint_a = r + m
    endpoint_b = endpoint_a + 1
    endpoints = (endpoint_a, endpoint_b)
    vertices = roots + blockers + endpoints
    matrices = {}
    colours = {}

    def add_matrix(u, v, matrix):
        assert u != v and (u, v) not in matrices and (v, u) not in matrices
        matrices[u, v] = matrix
        matrices[v, u] = transpose(matrix)

    def add_colour(u, v, colour):
        key = tuple(sorted((u, v)))
        assert key not in colours
        colours[key] = colour

    # A different cyclic row ledger still gives every root rank three.
    for i, root in enumerate(roots):
        for u, blocker in enumerate(blockers):
            row = BASIS[(2 * i + u) % 3]
            add_matrix(root, blocker, outer(BASIS[C], row))

    def root_edge(i, colour):
        u, v = roots[i], roots[i + 1]
        value = outer(PHI[colour], PHI[colour])
        if colour == P:
            left = outer(PHI[P], BASIS[C])
            right = outer(BASIS[C], PHI[P])
            value = tuple(
                tuple(value[i][j] + left[i][j] + right[i][j] for j in range(3))
                for i in range(3)
            )
        add_matrix(u, v, value)
        add_colour(u, v, colour)

    def root_port(root, endpoint, colour):
        add_matrix(root, endpoint, outer(PHI[colour], BASIS[C]))
        add_colour(root, endpoint, colour)

    def blocker_edge(i, colour):
        u, v = blockers[i], blockers[i + 1]
        add_matrix(u, v, outer(BASIS[colour], BASIS[colour]))
        add_colour(u, v, colour)

    def blocker_port(blocker, endpoint, colour):
        add_matrix(blocker, endpoint, outer(BASIS[colour], BASIS[C]))
        add_colour(blocker, endpoint, colour)

    if r & 1:
        for i in range(r - 1):
            root_edge(i, Q if not (i & 1) else P)
        root_port(roots[0], endpoint_a, P)
        root_port(roots[-1], endpoint_b, Q)
        for i in range(m - 1):
            blocker_edge(i, Q if not (i & 1) else P)
        blocker_port(blockers[0], endpoint_b, P)
        blocker_port(blockers[-1], endpoint_a, Q)
    else:
        for i in range(r - 1):
            root_edge(i, P if not (i & 1) else Q)
        root_port(roots[0], endpoint_a, Q)
        root_port(roots[-1], endpoint_b, Q)
        for i in range(m - 1):
            blocker_edge(i, Q if not (i & 1) else P)
        blocker_port(blockers[0], endpoint_a, P)
        blocker_port(blockers[-1], endpoint_b, P)

    return roots, blockers, endpoints, vertices, matrices, colours


def matching_polynomial(roots, blockers, endpoints, vertices, colours):
    position = {vertex: i for i, vertex in enumerate(roots + blockers)}
    vertex_index = {vertex: i for i, vertex in enumerate(vertices)}
    endpoint_bit = {endpoints[0]: 1, endpoints[1]: 2}
    adjacency = {vertex: [] for vertex in vertices}
    for (u, v), colour in colours.items():
        adjacency[u].append((v, colour))
        adjacency[v].append((u, colour))

    @cache
    def recurse(mask):
        if not mask:
            return Counter({(0, 0): 1})
        # Anchor at the largest remaining vertex, unlike the primary.
        i = mask.bit_length() - 1
        u = vertices[i]
        rest = mask ^ (1 << i)
        answer = Counter()
        for v, colour in adjacency[u]:
            bit = 1 << vertex_index[v]
            if not (rest & bit):
                continue
            contribution = 0
            for vertex in (u, v):
                if vertex in position:
                    contribution += colour * (3 ** position[vertex])
            used = 0
            if u in endpoint_bit and v in roots:
                used |= endpoint_bit[u]
            if v in endpoint_bit and u in roots:
                used |= endpoint_bit[v]
            for (code, endpoint_mask), coefficient in recurse(rest ^ bit).items():
                answer[code + contribution, endpoint_mask | used] += coefficient
        return answer

    return recurse((1 << len(vertices)) - 1)


def constant_word_code(colour, length):
    return sum(colour * (3**i) for i in range(length))


def decode(code, length):
    word = []
    for _ in range(length):
        word.append(code % 3)
        code //= 3
    assert code == 0
    return tuple(word)


def audit(r):
    roots, blockers, endpoints, vertices, matrices, colours = construct(r)
    m = len(blockers)
    zero = tuple(tuple(0 for _ in range(3)) for _ in range(3))

    def matrix(u, v):
        return matrices.get((u, v), zero)

    for (u, v), value in matrices.items():
        assert u != v and matrix(v, u) == transpose(value)

    # Pairwise-zero roots and zero root-to-endpoint base contractions.
    for i, u in enumerate(roots):
        for v in roots[i + 1 :]:
            assert bilinear(ONE, matrix(u, v), ONE) == 0
        for endpoint in endpoints:
            assert left_row(ONE, matrix(u, endpoint)) == (0, 0, 0)

    # Independently reconstruct all projectively constant blocker rows.
    for i, root in enumerate(roots):
        rows = []
        for u, blocker in enumerate(blockers):
            expected = BASIS[(2 * i + u) % 3]
            value = matrix(root, blocker)
            assert left_row(ONE, value) == expected
            assert left_row(BASIS[P], value) == (0, 0, 0)
            assert left_row(BASIS[Q], value) == (0, 0, 0)
            rows.append(expected)
        assert rational_rank(rows) == 3

    # Each root sees both tangent companion classes, and they frame x^perp.
    incident = {root: set() for root in roots}
    for (u, v), colour in colours.items():
        if u in incident:
            incident[u].add(colour)
        if v in incident:
            incident[v].add(colour)
    for root in roots:
        assert incident[root] == {P, Q}
    assert rational_rank([PHI[P], PHI[Q]]) == 2
    assert rational_rank([BASIS[C], PHI[P], PHI[Q]]) == 3
    assert sum(PHI[P]) == sum(PHI[Q]) == 0

    # Audit every root subset using the stabilized p matching.  This ledger
    # reconstructs actual chosen edges and checks vertex-disjointness.
    if r & 1:
        skeleton = [(endpoints[0], roots[0])]
        skeleton += [(roots[i], roots[i + 1]) for i in range(1, r - 1, 2)]
    else:
        skeleton = [(roots[i], roots[i + 1]) for i in range(0, r - 1, 2)]
    assert len(skeleton) == (r + (r & 1)) // 2
    for u, v in skeleton:
        if u in roots and v in roots:
            value = matrix(u, v)
            assert bilinear(BASIS[P], value, BASIS[P]) == 1
            assert bilinear(BASIS[P], value, ONE) == 1
            assert bilinear(ONE, value, BASIS[P]) == 1
        else:
            root = v if v in roots else u
            endpoint = u if u in endpoints else v
            assert bilinear(BASIS[P], matrix(root, endpoint), ONE) == 1
    for subset_mask in range(1 << r):
        subset = {roots[i] for i in range(r) if subset_mask & (1 << i)}
        chosen = [edge for edge in skeleton if set(edge) & subset]
        used_vertices = []
        for edge in chosen:
            used_vertices.extend(edge)
        assert len(used_vertices) == len(set(used_vertices))
        for root in roots:
            incidence = sum(root in edge for edge in chosen)
            if root in subset:
                assert incidence == 1
            else:
                assert incidence <= 1

    # Independently reconstruct a positive nonconstant base-slice word.
    base_word = [-1] * m
    if r & 1:
        base_word[0], base_word[-1] = P, Q
    else:
        base_word[0] = base_word[-1] = P
    for i in range(r):
        local_u = i + 1
        base_word[local_u] = (2 * i + local_u) % 3
    assert -1 not in base_word and len(set(base_word)) > 1
    base_matrix = [
        [int(base_word[local_u] == (2 * i + local_u) % 3) for local_u in range(1, r + 1)]
        for i in range(r)
    ]
    mixed_coefficient = anchored_permanent(base_matrix)
    assert mixed_coefficient >= 1

    polynomial = matching_polynomial(roots, blockers, endpoints, vertices, colours)
    length = r + m
    expected_p_mask = 1 if r & 1 else 0
    expected_q_mask = 2 if r & 1 else 3
    expected = Counter(
        {
            (constant_word_code(P, length), expected_p_mask): 1,
            (constant_word_code(Q, length), expected_q_mask): 1,
        }
    )
    assert polynomial == expected

    for (code, endpoint_mask), coefficient in polynomial.items():
        word = decode(code, length)
        assert coefficient == 1
        assert len(set(word[:r])) == len(set(word[r:])) == 1
        assert word[0] == word[r]
        assert endpoint_mask.bit_count() % 2 == r % 2

    return len(colours), len(polynomial), 1 << r, mixed_coefficient


def main():
    totals = [audit(r) for r in range(2, 17)]
    assert all(term_count == 2 for _, term_count, _, _ in totals)
    assert all(mixed_coefficient >= 1 for _, _, _, mixed_coefficient in totals)
    print("PASS: independent exact audit of two-endpoint full-jet sharpness")
    print("checked root counts: 2..16")
    print("coordinate permutation: (p,q,c)=(2,0,1)")
    print("restricted matching/cofactor classes per case: 2")
    print("all root subsets matching-saturated: yes")
    print("undifferentiated mixed coefficient: positive")
    print("global Krenn-Gu status: UNRESOLVED")


if __name__ == "__main__":
    main()
