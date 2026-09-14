"""Replay the exact common-star resource-alignment countercontrol.

The fixture defines an actual array over Q(sqrt(3)). Exact local source
checks and the resource-locality/U4 proof in
PROTECTED_SCAFFOLD_COMMON_STAR_RESOURCE_ALIGNMENT_NO_GO.md establish the
antecedent of RCS. The actual state graph is not a union of complete
tripartite components. A literal full-source failure is replayed as well;
this is not a CSQ4 or full GHZ witness. No result is written by default.
"""

import argparse
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
import hashlib
import itertools
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, _HERE = bootstrap(__file__)
DEFAULT_FIXTURE = (
    REPO_ROOT / "tests/fixtures/common_star_resource_alignment_control.json"
)


@dataclass(frozen=True)
class E:
    a: Fraction = Fraction(0)
    b: Fraction = Fraction(0)

    def __add__(self, other):
        other = lift(other)
        return E(self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __neg__(self):
        return E(-self.a, -self.b)

    def __sub__(self, other):
        return self + (-lift(other))

    def __rsub__(self, other):
        return lift(other) + (-self)

    def __mul__(self, other):
        other = lift(other)
        return E(
            self.a * other.a + 3 * self.b * other.b, self.a * other.b + self.b * other.a
        )

    __rmul__ = __mul__

    def inverse(self):
        norm = self.a * self.a - 3 * self.b * self.b
        assert norm
        return E(self.a / norm, -self.b / norm)

    def __truediv__(self, other):
        return self * lift(other).inverse()

    def __bool__(self):
        return bool(self.a or self.b)


def lift(x):
    return x if isinstance(x, E) else E(Fraction(x))


ZERO, ONE = E(), E(Fraction(1))


def transpose(a):
    return [list(x) for x in zip(*a)]


def times(a, b):
    return [
        [sum((x * y for x, y in zip(row, col)), ZERO) for col in zip(*b)] for row in a
    ]


def inverse(a):
    n = len(a)
    rows = [list(row) + [lift(i == j) for j in range(n)] for i, row in enumerate(a)]
    for i in range(n):
        pivot = next(j for j in range(i, n) if rows[j][i])
        rows[i], rows[pivot] = rows[pivot], rows[i]
        factor = rows[i][i].inverse()
        rows[i] = [x * factor for x in rows[i]]
        for j in range(n):
            if j != i:
                factor = rows[j][i]
                rows[j] = [x - factor * y for x, y in zip(rows[j], rows[i])]
    return [row[n:] for row in rows]


def local_data(fixture):
    r = E(Fraction(fixture["r"]["rational"]), Fraction(fixture["r"]["radical"]))
    t = E(Fraction(fixture["t"]["rational"]), Fraction(fixture["t"]["radical"]))
    identity = [[lift(i == j) for j in range(3)] for i in range(3)]
    tokens = {"1": ONE, "t": t}
    a = [[tokens[value] for value in row] for row in fixture["base_a"]]
    bases = {"A": a, "A_transpose": transpose(a), "identity": identity}
    M = {
        (int(pair[0]), int(pair[1])): bases[name]
        for pair, name in fixture["pair_base_matrices"].items()
    }
    assert set(M) == {(0, 1), (0, 2), (1, 2)}
    for c, d in list(M):
        M[d, c] = transpose(M[c, d])
    N = {
        pair: [[-x for x in row] for row in transpose(inverse(matrix))]
        for pair, matrix in M.items()
    }
    Q = {
        pair: [[M[pair][i][j] * N[pair][i][j] for j in range(3)] for i in range(3)]
        for pair in M
    }
    for pair, matrix in Q.items():
        assert all(sum(row, ZERO) == -ONE for row in matrix)
        assert times(matrix, transpose(matrix)) == identity
    for c, d, e in itertools.permutations(range(3)):
        prod = times(Q[d, c], Q[c, e])
        x = times(M[d, c], N[c, e])
        y = times(N[d, c], M[c, e])
        assert Q[d, e] == [
            [2 * prod[i][j] - 3 * x[i][j] * y[i][j] for j in range(3)] for i in range(3)
        ]

    def v(c, d, f):
        return r if f == 1 and d == max(set(range(3)) - {c}) else ONE

    states = list(itertools.product(range(3), range(3), range(2)))
    edges = {}
    for u, (c, i, f) in enumerate(states):
        for w in range(u + 1, len(states)):
            d, j, h = states[w]
            if c == d or not M[c, d][i][j]:
                continue
            assert N[c, d][i][j]
            factor = v(c, d, f) * v(d, c, h)
            edges[u, w] = (M[c, d][i][j] * factor, N[c, d][i][j] / (2 * factor))
    assert len(edges) == 84
    return states, edges


def local_physical(states, edges, selected):
    chosen = list(selected)
    entries = {}
    for new, old in enumerate(chosen):
        c = states[old][0]
        for x, y in itertools.combinations(range(4), 2):
            if x ^ y == c + 1:
                entries[4 * new + x, 4 * new + y] = ONE
    for u, old_u in enumerate(chosen):
        for w in range(u + 1, len(chosen)):
            old_w = chosen[w]
            if (old_u, old_w) not in edges:
                continue
            A, B = edges[old_u, old_w]
            c, d = states[old_u][0], states[old_w][0]
            entries[4 * u, 4 * w] = A
            entries[4 * u + c + 1, 4 * w + d + 1] = B
    adjacency = [[] for _ in range(4 * len(chosen))]
    for (u, w), weight in entries.items():
        adjacency[u].append((w, weight))
        adjacency[w].append((u, weight))

    @lru_cache(maxsize=None)
    def haf(mask):
        if not mask:
            return ONE
        bit = mask & -mask
        u = bit.bit_length() - 1
        rest = mask ^ bit
        return sum(
            (
                weight * haf(rest ^ (1 << w))
                for w, weight in adjacency[u]
                if rest & (1 << w)
            ),
            ZERO,
        )

    return haf((1 << len(adjacency)) - 1)


def local_matrix_checks(states, edges):
    """Check all cloned local S1 and both S2 matrix families exactly."""
    A, B, Q = {}, {}, {}
    for c, d in itertools.permutations(range(3), 2):
        left = [i for i, state in enumerate(states) if state[0] == c]
        right = [i for i, state in enumerate(states) if state[0] == d]
        a, b = [], []
        for u in left:
            arow, brow = [], []
            for v in right:
                factors = edges.get(tuple(sorted((u, v))), (ZERO, ZERO))
                arow.append(factors[0])
                brow.append(factors[1])
            a.append(arow)
            b.append(brow)
        A[c, d], B[c, d] = a, b
        Q[c, d] = [[x * y for x, y in zip(arow, brow)] for arow, brow in zip(a, b)]
    counts = Counter()
    for c, d in itertools.permutations(range(3), 2):
        assert all(sum(row, ZERO) == -ONE for row in Q[c, d])
        assert all(sum(col, ZERO) == -ONE for col in zip(*Q[c, d]))
        counts["S1_rows_and_columns"] += 12
        x = times(A[d, c], B[c, d])
        y = times(B[d, c], A[c, d])
        h = times(Q[d, c], Q[c, d])
        for i, j in itertools.permutations(range(6), 2):
            assert x[i][j] * y[i][j] == 2 * h[i][j]
            counts["same_color_S2_entries"] += 1
    for c, d, e in itertools.permutations(range(3)):
        x = times(A[d, c], B[c, e])
        y = times(B[d, c], A[c, e])
        h = times(Q[d, c], Q[c, e])
        for i, j in itertools.product(range(6), repeat=2):
            assert Q[d, e][i][j] == 2 * h[i][j] - x[i][j] * y[i][j]
            counts["distinct_color_S2_entries"] += 1
    return dict(counts)


def cover(states, local_edges, fixture):
    p = fixture["group_prime"]
    assert p == 5 and fixture["group"] == "SL(2,F5)"
    group = [
        m
        for m in itertools.product(range(p), repeat=4)
        if (m[0] * m[3] - m[1] * m[2]) % p == 1
    ]
    index = {m: i for i, m in enumerate(group)}
    shifts = tuple(
        tuple(tuple(matrix) for matrix in row) for row in fixture["translations"]
    )
    assert len(shifts) == 2 and all(len(row) == 3 for row in shifts)
    assert all(matrix in index for row in shifts for matrix in row)

    def mul(a, b):
        return (
            (a[0] * b[0] + a[1] * b[2]) % p,
            (a[0] * b[1] + a[1] * b[3]) % p,
            (a[2] * b[0] + a[3] * b[2]) % p,
            (a[2] * b[1] + a[3] * b[3]) % p,
        )

    size = len(group)
    old_resources = [[] for _ in group]
    membership = {}
    for f in range(2):
        for g, matrix in enumerate(group):
            old_u = f * size + g
            for c in range(3):
                r = index[mul(matrix, shifts[f][c])]
                old_resources[r].append((old_u, c, f))
                membership[old_u, c] = r
    old_pairs = {}
    old_adjacency = [set() for _ in range(2 * size)]
    for r, resource in enumerate(old_resources):
        assert len({u for u, _c, _f in resource}) == 6
        for left, right in itertools.combinations(resource, 2):
            u, c, _f = left
            w, d, _h = right
            pair = tuple(sorted((u, w)))
            assert pair not in old_pairs
            old_pairs[pair] = r
            if c != d:
                old_adjacency[u].add(w)
                old_adjacency[w].add(u)
    old_triangles = 0
    for u in range(2 * size):
        for w in old_adjacency[u]:
            if w <= u:
                continue
            for z in old_adjacency[u] & old_adjacency[w]:
                if z > w:
                    assert old_pairs[u, w] == old_pairs[u, z] == old_pairs[w, z]
                    old_triangles += 1

    gadgets = {}
    gadget_resources = {}
    options = {}
    ports = Counter()
    port_sums = {}
    for r, resource in enumerate(old_resources):
        by_role = {(c, f): u for u, c, f in resource}
        actual = [3 * by_role[c, f] + i for c, i, f in states]
        assert len(set(actual)) == 18
        for old, (c, _i, _f) in zip(actual, states):
            assert (old, c) not in options
            options[old, c] = r
        for (u, w), factors in local_edges.items():
            real_u, real_w = actual[u], actual[w]
            c, d = states[u][0], states[w][0]
            if real_u > real_w:
                real_u, real_w, c, d = real_w, real_u, d, c
            assert (real_u, real_w) not in gadgets
            gadgets[real_u, real_w] = (c, d, *factors)
            gadget_resources[real_u, real_w] = r
            ports[real_u, c, d] += 1
            ports[real_w, d, c] += 1
            product = factors[0] * factors[1]
            for port in ((real_u, c, d), (real_w, d, c)):
                port_sums[port] = port_sums.get(port, ZERO) + product
    count = 6 * size
    assert len(options) == 3 * count and len(gadgets) == 84 * size
    assert Counter(ports.values()) == {2: 2 * count, 6: 4 * count}
    assert all(total == -ONE for total in port_sums.values())

    option_adjacency = {state: set() for state in options}
    component_adjacency = [set() for _ in range(count)]
    for (u, v), (c, d, _A, _B) in gadgets.items():
        option_adjacency[u, c].add((v, d))
        option_adjacency[v, d].add((u, c))
        component_adjacency[u].add(v)
        component_adjacency[v].add(u)
    pending = set(options)
    state_component_count = 0
    while pending:
        part = {next(iter(pending))}
        stack = list(part)
        while stack:
            for state in option_adjacency[stack.pop()]:
                if state not in part:
                    part.add(state)
                    stack.append(state)
        pending.difference_update(part)
        assert len(part) == 18 and Counter(c for _u, c in part) == {0: 6, 1: 6, 2: 6}
        assert len({options[state] for state in part}) == 1
        assert sum(len(option_adjacency[state]) for state in part) == 2 * 84
        state_component_count += 1

    triangle_count = 0
    for u in range(count):
        for v in component_adjacency[u]:
            if v <= u:
                continue
            for w in component_adjacency[u] & component_adjacency[v]:
                if w <= v:
                    continue
                uv, uw, vw = gadgets[u, v], gadgets[u, w], gadgets[v, w]
                assert uv[0] == uw[0] and uv[1] == vw[0] and uw[1] == vw[1]
                assert (
                    gadget_resources[u, v]
                    == gadget_resources[u, w]
                    == gadget_resources[v, w]
                )
                triangle_count += 1

    scalar = {}
    colors = [fixture["failure_colors_by_clone"][u // (3 * size)] for u in range(count)]
    for u, c in enumerate(colors):
        for x, y in itertools.combinations(range(4), 2):
            if x ^ y == c + 1:
                scalar[4 * u + x, 4 * u + y] = Fraction(1)
    for (u, w), (c, d, A, B) in gadgets.items():
        if colors[u] == c and colors[w] == d:
            assert A == ONE and B == lift(Fraction(-1, 2))
            scalar[4 * u, 4 * w] = Fraction(1)
            scalar[4 * u + c + 1, 4 * w + d + 1] = Fraction(-1, 2)
    adjacency = [[] for _ in range(4 * count)]
    for (u, w), weight in scalar.items():
        adjacency[u].append((w, weight))
        adjacency[w].append((u, weight))
    unseen = set(range(len(adjacency)))
    sizes = Counter()
    amplitude = Fraction(1)
    matching_count = 1
    while unseen:
        part = {next(iter(unseen))}
        stack = list(part)
        while stack:
            for w, _weight in adjacency[stack.pop()]:
                if w not in part:
                    part.add(w)
                    stack.append(w)
        unseen.difference_update(part)
        sizes[len(part)] += 1

        @lru_cache(maxsize=None)
        def haf(state):
            if not state:
                return Fraction(1), 1
            u = state[0]
            total = Fraction(0)
            ways = 0
            for w, weight in adjacency[u]:
                if w in state:
                    tail, tail_count = haf(tuple(v for v in state if v not in (u, w)))
                    total += weight * tail
                    ways += tail_count
            return total, ways

        local, local_count = haf(tuple(sorted(part)))
        amplitude *= local
        matching_count *= local_count
    assert sizes == {2: count, 4: 3 * size}
    assert amplitude == Fraction(1, 2 ** (3 * size))
    assert matching_count == 2 ** (3 * size)
    result = {
        "resources": size,
        "components": count,
        "physical_vertices": 4 * count,
        "gadgets": len(gadgets),
        "simple_one_label_component_graph": True,
        "ports_by_multiplicity": dict(Counter(ports.values())),
        "global_S1_port_sums_checked": len(port_sums),
        "old_coherent_triangles_checked": old_triangles,
        "physical_component_triangles": triangle_count,
        "all_physical_component_triangles_coherent": True,
        "state_components": state_component_count,
        "state_components_noncomplete": True,
        "option_resource_vertices": 18,
        "option_resource_edges": 84,
        "complete_K666_edges": 108,
        "full_failure_scalar_components": dict(sizes),
        "full_failure_amplitude": f"2^(-{3 * size})",
        "physical_failure_replayed": True,
        "full_failure_matching_count": str(matching_count),
    }
    expected = fixture["expected"]
    for key in (
        "resources",
        "components",
        "physical_vertices",
        "gadgets",
        "physical_component_triangles",
        "state_components",
    ):
        assert result[key] == expected[key]
    assert result["option_resource_vertices"] == expected["state_component_vertices"]
    assert result["option_resource_edges"] == expected["state_component_edges"]
    assert (
        result["complete_K666_edges"]
        == expected["complete_tripartite_edges_per_state_component"]
    )
    assert sizes[4] == expected["full_failure_four_cycles"]
    assert sizes[2] == expected["full_failure_isolated_edges"]
    assert 3 * size == expected["full_failure_denominator_power_of_two"]
    return result


def verify(fixture_path=DEFAULT_FIXTURE):
    """Return exact replay evidence; the owning proof supplies locality and U4 coverage."""
    fixture_bytes = Path(fixture_path).read_bytes()
    fixture = json.loads(fixture_bytes)
    assert fixture["schema"] == "common-star-resource-alignment-control-v1"
    assert fixture["field"] == "Q(sqrt(3))"
    assert fixture["index_copies"] == 3 and fixture["component_clones"] == 2
    states, edges = local_data(fixture)
    counts = Counter()
    for c in range(3):
        majority = [i for i, state in enumerate(states) if state[0] == c]
        outside = [i for i, state in enumerate(states) if state[0] != c]
        assert local_physical(states, edges, majority) == ONE
        counts["pure"] += 1
        for size in (1, 2):
            for subset in itertools.combinations(outside, size):
                active = sorted(majority + list(subset))
                assert local_physical(states, edges, active) == ZERO, (c, subset)
                counts[f"changed_{size}"] += 1
    return {
        "schema": "common-star-resource-alignment-replay-v1",
        "scope": "exact RCS countercontrol via the owning source-locality and U4 bridge; not CSQ4",
        "field": "Q(sqrt(3))",
        "fixture_sha256_lf": hashlib.sha256(
            fixture_bytes.replace(b"\r\n", b"\n")
        ).hexdigest(),
        "local_physical_target_checks": dict(counts),
        "base_modified_matrix_identities": True,
        "local_cloned_matrix_checks": local_matrix_checks(states, edges),
        "full_U4_bridge": "global S1 plus all component triangles coherent; exhaustive source classification in owning proof",
        "S2_bridge": "exact local matrix identities plus unique color-state resource membership and one label per physical pair",
        "cover": cover(states, edges, fixture),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, default=DEFAULT_FIXTURE)
    parser.add_argument("--output", type=Path, help="optional JSON receipt destination")
    args = parser.parse_args()
    encoded = json.dumps(verify(args.fixture), indent=2) + "\n"
    if args.output is not None:
        args.output.write_text(encoded, encoding="utf-8")
    print(encoded, end="")


if __name__ == "__main__":
    main()
