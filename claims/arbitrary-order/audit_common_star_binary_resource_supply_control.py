"""Independent exact audit of the common-star binary-supply countercontrol.

This portable checker imports no primary verifier or project scientific code.
It reconstructs the field arithmetic, tensor matrices, finite cover and full
source failure from explicit formulas.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
import itertools
import json
from pathlib import Path


@dataclass(frozen=True)
class Q3:
    a: Fraction = Fraction(0)
    b: Fraction = Fraction(0)

    def __add__(self, other):
        other = q3(other)
        return Q3(self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __neg__(self):
        return Q3(-self.a, -self.b)

    def __sub__(self, other):
        return self + -q3(other)

    def __rsub__(self, other):
        return q3(other) - self

    def __mul__(self, other):
        other = q3(other)
        return Q3(self.a * other.a + 3 * self.b * other.b, self.a * other.b + self.b * other.a)

    __rmul__ = __mul__

    def inverse(self):
        norm = self.a**2 - 3 * self.b**2
        if not norm:
            raise ZeroDivisionError
        return Q3(self.a / norm, -self.b / norm)

    def __truediv__(self, other):
        return self * q3(other).inverse()

    def __pow__(self, exponent):
        if exponent < 0:
            return self.inverse() ** (-exponent)
        result = ONE
        factor = self
        while exponent:
            if exponent & 1:
                result *= factor
            factor *= factor
            exponent //= 2
        return result

    def __bool__(self):
        return bool(self.a or self.b)

    def text(self):
        if not self.b:
            return str(self.a)
        return f"({self.a})+({self.b})*sqrt(3)"


def q3(value):
    if isinstance(value, Q3):
        return value
    return Q3(Fraction(value))


ZERO = Q3()
ONE = q3(1)
T = Q3(Fraction(-1, 2), Fraction(1, 2))
R_CLONE = Q3(Fraction(2), Fraction(1))


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def matmul(left, right):
    columns = tuple(zip(*right))
    return [[sum((x * y for x, y in zip(row, column)), ZERO) for column in columns] for row in left]


def identity(size):
    return [[ONE if i == j else ZERO for j in range(size)] for i in range(size)]


def inverse(matrix):
    size = len(matrix)
    rows = [list(row) + [ONE if i == j else ZERO for j in range(size)] for i, row in enumerate(matrix)]
    for column in range(size):
        pivot = next(row for row in range(column, size) if rows[row][column])
        rows[column], rows[pivot] = rows[pivot], rows[column]
        scale = rows[column][column].inverse()
        rows[column] = [entry * scale for entry in rows[column]]
        for row in range(size):
            if row == column or not rows[row][column]:
                continue
            factor = rows[row][column]
            rows[row] = [x - factor * y for x, y in zip(rows[row], rows[column])]
    return [row[size:] for row in rows]


def hadamard(left, right):
    return [[x * y for x, y in zip(a, b)] for a, b in zip(left, right)]


def kronecker(left, right):
    return [[left[i][j] * right[k][ell] for j in range(len(left[0])) for ell in range(len(right[0]))] for i in range(len(left)) for k in range(len(right))]


def embed(block, indices, size):
    result = identity(size)
    for i, row_index in enumerate(indices):
        for j, column_index in enumerate(indices):
            result[row_index][column_index] = block[i][j]
    return result


def clone_vector(own, other):
    alternatives = sorted(set(range(3)) - {own})
    return (ONE, ONE if other == alternatives[0] else R_CLONE)


def build_matrices():
    a3 = [[ONE, T, ONE], [ONE, ONE, T], [T, ONE, ONE]]
    m5 = matmul(embed(a3, (0, 1, 2), 5), embed(a3, (2, 3, 4), 5))
    n5 = [[-entry for entry in row] for row in inverse(transpose(m5))]
    q5 = hadamard(m5, n5)
    assert [sum(row, ZERO) for row in q5] == [-ONE] * 5
    assert matmul(q5, transpose(q5)) == identity(5)
    assert [[bool(entry) for entry in row] for row in m5] == [[bool(entry) for entry in row] for row in n5]
    assert sum(bool(entry) for row in m5 for entry in row) == 21

    first = {(0, 1): transpose(m5), (1, 2): m5, (0, 2): identity(5)}
    for c, d in list(first):
        first[d, c] = transpose(first[c, d])
    color_swap = {0: 1, 1: 0, 2: 2}
    base = {
        (c, d): kronecker(first[c, d], first[color_swap[c], color_swap[d]])
        for c, d in itertools.permutations(range(3), 2)
    }
    base_n = {(c, d): [[-entry for entry in row] for row in inverse(transpose(base[c, d]))] for c, d in itertools.permutations(range(3), 2)}
    base_q = {pair: hadamard(base[pair], base_n[pair]) for pair in base}
    for pair in base:
        assert [sum(row, ZERO) for row in base_q[pair]] == [-ONE] * 25
        assert matmul(base_q[pair], transpose(base_q[pair])) == identity(25)
        assert [[bool(x) for x in row] for row in base[pair]] == [[bool(x) for x in row] for row in base_n[pair]]

    # Check both strict tensor identities and their coefficient-three
    # consequence before cloning.
    base_distinct = 0
    for c, d, e in itertools.permutations(range(3)):
        h = matmul(base_q[d, c], base_q[c, e])
        x = matmul(base[d, c], base_n[c, e])
        y = matmul(base_n[d, c], base[c, e])
        for i in range(25):
            for j in range(25):
                assert h[i][j] == -base_q[d, e][i][j]
                assert x[i][j] * y[i][j] == -base_q[d, e][i][j]
                assert base_q[d, e][i][j] == 2 * h[i][j] - 3 * x[i][j] * y[i][j]
                base_distinct += 1

    cloned = {}
    for c, d in itertools.permutations(range(3), 2):
        a50 = [[ZERO for _ in range(50)] for _ in range(50)]
        b50 = [[ZERO for _ in range(50)] for _ in range(50)]
        z_cd, z_dc = clone_vector(c, d), clone_vector(d, c)
        for i, f, j, g in itertools.product(range(25), range(2), range(25), range(2)):
            scale = z_cd[f] * z_dc[g]
            row, column = 2 * i + f, 2 * j + g
            a50[row][column] = base[c, d][i][j] * scale
            b50[row][column] = base_n[c, d][i][j] / (2 * scale)
        cloned["A", c, d] = a50
        cloned["B", c, d] = b50
        cloned["Q", c, d] = hadamard(a50, b50)
    return m5, n5, q5, base, base_n, base_q, cloned, base_distinct


def binary_components(support):
    size = len(support)
    adjacency = defaultdict(set)
    for i in range(size):
        for j in range(size):
            if support[i][j]:
                adjacency[0, i].add((1, j))
                adjacency[1, j].add((0, i))
    unseen = {(part, i) for part in range(2) for i in range(size)}
    out = []
    while unseen:
        root = next(iter(unseen))
        component = {root}
        queue = deque([root])
        unseen.remove(root)
        while queue:
            state = queue.popleft()
            for neighbor in adjacency[state]:
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    component.add(neighbor)
                    queue.append(neighbor)
        left = sum(part == 0 for part, _index in component)
        right = len(component) - left
        edges = sum(len(adjacency[state]) for state in component) // 2
        out.append({"left": left, "right": right, "edges": edges, "complete": edges == left * right})
    return sorted(out, key=lambda item: (item["left"], item["right"], item["edges"]))


def check_cloned_identities(cloned):
    counts = Counter()
    for c, d in itertools.permutations(range(3), 2):
        q_cd = cloned["Q", c, d]
        assert all(sum(row, ZERO) == -ONE for row in q_cd)
        assert all(sum((q_cd[i][j] for i in range(50)), ZERO) == -ONE for j in range(50))
        counts["S1_rows_and_columns"] += 100

        x = matmul(cloned["A", d, c], cloned["B", c, d])
        y = matmul(cloned["B", d, c], cloned["A", c, d])
        h = matmul(cloned["Q", d, c], cloned["Q", c, d])
        for i in range(50):
            for j in range(50):
                if i != j:
                    assert x[i][j] * y[i][j] == 2 * h[i][j]
                    counts["same_S2_off_diagonal"] += 1

        e = 3 - c - d
        x = matmul(cloned["A", d, c], cloned["B", c, e])
        y = matmul(cloned["B", d, c], cloned["A", c, e])
        h = matmul(cloned["Q", d, c], cloned["Q", c, e])
        for i in range(50):
            for j in range(50):
                assert cloned["Q", d, e][i][j] == 2 * h[i][j] - x[i][j] * y[i][j]
                counts["distinct_S2"] += 1
    return dict(counts)


def residual_block_source(m5, n5):
    vertex_count = 20
    adjacency = defaultdict(list)
    for component in range(10):
        adjacency[2 * component].append((2 * component + 1, ONE))
        adjacency[2 * component + 1].append((2 * component, ONE))
    for i in range(5):
        for j in range(5):
            if not m5[i][j]:
                continue
            center_u, center_v = 2 * i, 2 * (5 + j)
            leaf_u, leaf_v = center_u + 1, center_v + 1
            adjacency[center_u].append((center_v, m5[i][j]))
            adjacency[center_v].append((center_u, m5[i][j]))
            adjacency[leaf_u].append((leaf_v, n5[i][j] / 2))
            adjacency[leaf_v].append((leaf_u, n5[i][j] / 2))

    @lru_cache(maxsize=None)
    def haf(mask):
        if not mask:
            return ONE, 1
        bit = mask & -mask
        u = bit.bit_length() - 1
        rest = mask ^ bit
        total = ZERO
        ways = 0
        for v, weight in adjacency[u]:
            if rest & (1 << v):
                tail, tail_ways = haf(rest ^ (1 << v))
                total += weight * tail
                ways += tail_ways
        return total, ways

    physical, ways = haf((1 << vertex_count) - 1)

    # The residual graph is bipartite.  In the order
    # (left centers,right leaves) x (right centers,left leaves), its matrix is
    # [[M,I],[I,(-D/2)^T]].  A separate subset DP computes its permanent and
    # the permanent of its Boolean support.
    bipartite = [[ZERO for _ in range(10)] for _ in range(10)]
    for i in range(5):
        for j in range(5):
            bipartite[i][j] = m5[i][j]
            bipartite[5 + j][5 + i] = n5[i][j] / 2
        bipartite[i][5 + i] = ONE
        bipartite[5 + i][i] = ONE

    def permanent(matrix):
        dp = {0: ONE}
        for row in matrix:
            next_dp = {}
            for used, value in dp.items():
                for column, entry in enumerate(row):
                    if entry and not used & (1 << column):
                        state = used | (1 << column)
                        next_dp[state] = next_dp.get(state, ZERO) + value * entry
            dp = next_dp
        return dp.get((1 << len(matrix)) - 1, ZERO)

    permanent_value = permanent(bipartite)
    permanent_count = permanent(
        [[ONE if entry else ZERO for entry in row] for row in bipartite]
    )

    center = [[ZERO for _ in range(10)] for _ in range(10)]
    leaf = [[ZERO for _ in range(10)] for _ in range(10)]
    for i in range(5):
        for j in range(5):
            center[i][5 + j] = center[5 + j][i] = m5[i][j]
            leaf[i][5 + j] = leaf[5 + j][i] = n5[i][j] / 2

    def haf_matrix(matrix, mask):
        @lru_cache(maxsize=None)
        def recurse(state):
            if not state:
                return ONE
            bit = state & -state
            u = bit.bit_length() - 1
            rest = state ^ bit
            return sum((matrix[u][v] * recurse(rest ^ (1 << v)) for v in range(10) if rest & (1 << v)), ZERO)

        return recurse(mask)

    doubled = sum((haf_matrix(center, mask) * haf_matrix(leaf, mask) for mask in range(1 << 10) if mask.bit_count() % 2 == 0), ZERO)

    def principal_permanent(matrix, rows, columns):
        if not rows:
            return ONE
        square = [[matrix[i][j] for j in columns] for i in rows]
        return permanent(square)

    coefficients = []
    indices = range(5)
    for size in range(6):
        coefficient = ZERO
        for rows in itertools.combinations(indices, size):
            for columns in itertools.combinations(indices, size):
                coefficient += principal_permanent(m5, rows, columns) * principal_permanent(
                    [[-entry for entry in row] for row in n5], rows, columns
                )
        coefficients.append(coefficient)
    generating_value = sum(
        (coefficient * q3(Fraction(-1, 2)) ** size for size, coefficient in enumerate(coefficients)),
        ZERO,
    )
    assert physical == doubled == permanent_value == q3(Fraction(-463, 2592))
    assert generating_value == physical
    assert ways == 6130
    assert permanent_count == q3(6130), (ways, permanent_count.text())
    return {
        "physical_hafnian": physical.text(),
        "double_hafnian_minor_sum": doubled.text(),
        "bipartite_permanent": permanent_value.text(),
        "supported_perfect_matchings": ways,
        "boolean_support_permanent": permanent_count.text(),
        "minor_generating_coefficients": [value.text() for value in coefficients],
        "residual_vertices": vertex_count,
    }


def mutation_controls(m5, n5, base):
    wrong_sign = hadamard(m5, [[-entry for entry in row] for row in n5])
    wrong_sign_row_sums = [sum(row, ZERO) for row in wrong_sign]
    assert wrong_sign_row_sums == [ONE] * 5

    first = {(0, 1): transpose(m5), (1, 2): m5, (0, 2): identity(5)}
    for c, d in list(first):
        first[d, c] = transpose(first[c, d])
    no_swap = {
        (c, d): kronecker(first[c, d], first[c, d])
        for c, d in itertools.permutations(range(3), 2)
    }
    no_swap_02 = binary_components(
        [[bool(value) for value in row] for row in no_swap[0, 2]]
    )
    assert all(component["complete"] for component in no_swap_02)
    assert any(not component["complete"] for component in binary_components(
        [[bool(value) for value in row] for row in base[0, 2]]
    ))

    # Insert the forbidden ABB triangle and expand its literal 12-vertex U4
    # source. Components u,v carry minority centers 1,2, while component w
    # carries the corresponding minority leaves over background color 0.
    word = [0] * 12
    word[0] = 1
    word[4] = 2
    word[8 + 2] = 1
    word[8 + 3] = 2
    scalar_edges = {}
    for component in range(3):
        for x, y in ((0, 1), (2, 3)):
            if word[4 * component + x] == word[4 * component + y] == 0:
                scalar_edges[4 * component + x, 4 * component + y] = ONE
    scalar_edges[0, 4] = ONE
    scalar_edges[1, 8 + 2] = ONE
    scalar_edges[5, 8 + 3] = ONE
    adjacency = defaultdict(list)
    for (u, v), weight in scalar_edges.items():
        adjacency[u].append((v, weight))
        adjacency[v].append((u, weight))

    @lru_cache(maxsize=None)
    def triangle_haf(mask):
        if not mask:
            return ONE
        bit = mask & -mask
        u = bit.bit_length() - 1
        rest = mask ^ bit
        return sum(
            (
                weight * triangle_haf(rest ^ (1 << v))
                for v, weight in adjacency[u]
                if rest & (1 << v)
            ),
            ZERO,
        )

    incoherent_triangle_coefficient = triangle_haf((1 << 12) - 1)
    assert incoherent_triangle_coefficient == ONE
    return {
        "wrong_dual_sign_breaks_S1": {
            "mutated_Q_row_sums": [value.text() for value in wrong_sign_row_sums],
            "expected": "+1 rather than -1",
        },
        "omitting_second_factor_color_swap": {
            "pair_02_components": no_swap_02,
            "BS_conclusion_restored": True,
        },
        "incoherent_triangle_breaks_U4_bridge": {
            "physical_word": "".join(map(str, word)),
            "literal_triangle_source_coefficient": incoherent_triangle_coefficient.text(),
            "nonzero": True,
        },
    }


def mul2(left, right):
    a, b, c, d = left
    e, f, g, h = right
    return ((a * e + b * g) % 5, (a * f + b * h) % 5, (c * e + d * g) % 5, (c * f + d * h) % 5)


def inv2(matrix):
    a, b, c, d = matrix
    assert (a * d - b * c) % 5 == 1
    return (d % 5, -b % 5, -c % 5, a % 5)


def check_cover(base):
    group = tuple(matrix for matrix in itertools.product(range(5), repeat=4) if (matrix[0] * matrix[3] - matrix[1] * matrix[2]) % 5 == 1)
    assert len(group) == 120
    transforms = {
        0: ((1, 0, 0, 1), (1, 1, 0, 1), (3, 2, 4, 3)),
        1: ((1, 0, 0, 1), (2, 4, 4, 1), (4, 2, 1, 2)),
    }
    inverses = {(f, c): inv2(transforms[f][c]) for f in range(2) for c in range(3)}
    components = tuple((index, f, g) for g in group for f in range(2) for index in range(25))
    component_index = {component: i for i, component in enumerate(components)}

    old_components = tuple((f, g) for g in group for f in range(2))
    memberships = {(f, g): {mul2(g, transforms[f][c]) for c in range(3)} for f, g in old_components}
    shared = Counter(len(memberships[u] & memberships[v]) for u, v in itertools.combinations(old_components, 2))
    assert max(shared) <= 1

    pair_seen = set()
    port_degrees = Counter()
    gadget_count = 0
    for resource in group:
        occupants = {(c, index, f): component_index[index, f, mul2(resource, inverses[f, c])] for c in range(3) for index in range(25) for f in range(2)}
        assert len(set(occupants.values())) == 150
        for c, d in itertools.combinations(range(3), 2):
            for i, j in itertools.product(range(25), repeat=2):
                if not base[c, d][i][j]:
                    continue
                for f, h in itertools.product(range(2), repeat=2):
                    u, v = occupants[c, i, f], occupants[d, j, h]
                    pair = tuple(sorted((u, v)))
                    assert pair not in pair_seen
                    pair_seen.add(pair)
                    port_degrees[u, c, d] += 1
                    port_degrees[v, d, c] += 1
                    gadget_count += 1
    assert gadget_count == 312480
    assert len(pair_seen) == gadget_count
    assert len(port_degrees) == len(components) * 6

    base_triangles = 0
    for i, j, k in itertools.product(range(25), repeat=3):
        if base[0, 1][i][j] and base[0, 2][i][k] and base[1, 2][j][k]:
            base_triangles += 1
    assert base_triangles == 441
    actual_triangles = len(group) * base_triangles * 8
    return {
        "resources": len(group),
        "components": len(components),
        "physical_vertices": 4 * len(components),
        "gadgets": gadget_count,
        "crossing_entries": 2 * gadget_count,
        "port_degree_histogram": dict(sorted(Counter(port_degrees.values()).items())),
        "old_pair_shared_resource_histogram": dict(sorted(shared.items())),
        "local_base_triangles": base_triangles,
        "actual_coherent_triangles": actual_triangles,
        "one_label_per_component_pair": True,
    }


def build_result():
    m5, n5, _q5, base, _base_n, _base_q, cloned, base_distinct = build_matrices()
    base_supports = {}
    for c, d in ((0, 1), (0, 2), (1, 2)):
        components = binary_components([[bool(x) for x in row] for row in base[c, d]])
        assert all(not component["complete"] for component in components)
        base_supports[f"{c}{d}"] = components
    local_counts = check_cloned_identities(cloned)
    residual = residual_block_source(m5, n5)
    cover = check_cover(base)
    controls = mutation_controls(m5, n5, base)
    return {
        "schema": "binary-resource-supply-tensor-independent-audit-v1",
        "status": "PASS",
        "field": "Q(sqrt(3)) subset C",
        "five_state": {
            "M_support_entries": 21,
            "row_degrees": [sum(bool(x) for x in row) for row in m5],
            "column_degrees": [sum(bool(m5[i][j]) for i in range(5)) for j in range(5)],
            "Q_row_sums_minus_one": True,
            "Q_orthogonal": True,
        },
        "tensor_base": {
            "states_per_color": 25,
            "binary_components": base_supports,
            "all_binary_components_noncomplete": True,
            "coefficient_three_distinct_identities": base_distinct,
        },
        "two_clone": {"states_per_color": 50, "identity_counts": local_counts},
        "cover": cover,
        "u4_bridge": "all actual component triangles are coherent; use exhaustive <=4-minority classification",
        "global_failure": {
            "residual_block": residual,
            "blocks_per_resource": 5,
            "global_blocks": 600,
            "source": "(-463/2592)^600 != 0",
            "target": "0",
        },
        "mutation_controls": controls,
        "conclusion": "candidate exact BS refutation only; not CSQ4 or Krenn-Gu",
        "global_status_changed": False,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = build_result()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n"
        )
        print(json.dumps({"status": "PASS", "output": args.output.as_posix()}))
    else:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
