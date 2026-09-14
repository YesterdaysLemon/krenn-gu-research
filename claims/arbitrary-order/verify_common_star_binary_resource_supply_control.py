"""Replay the exact common-star binary-resource-supply countercontrol.

The fixture specifies an actual Q(sqrt(3)) array. Exact factor identities,
the finite cover, and the locality/U4 proof in
PROTECTED_SCAFFOLD_COMMON_STAR_BINARY_SUPPLY_NO_GO.md establish its S1,
both S2, and full U4 antecedent. All three binary option graphs fail to be
biclique unions. The literal nonzero full-source failure is also replayed;
this is not a CSQ4 or Krenn--Gu counterexample.

Dependency: only exact-field and elementary matrix helpers are reused from
verify_common_star_resource_alignment_control.py. This author verifier is
not an independent audit of that arithmetic or of its owning source proof.
No tracked output is written by default.
"""

import argparse
from collections import Counter
from fractions import Fraction
from functools import lru_cache
import importlib.util
import hashlib
import itertools
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, _HERE = bootstrap(__file__)
DEFAULT_FIXTURE = (
    REPO_ROOT / "tests/fixtures/common_star_binary_resource_supply_control.json"
)
ARITHMETIC_DEPENDENCY = (
    REPO_ROOT
    / "claims/arbitrary-order/verify_common_star_resource_alignment_control.py"
)
SPEC = importlib.util.spec_from_file_location("bs_exact_field", ARITHMETIC_DEPENDENCY)
FIELD = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = FIELD
SPEC.loader.exec_module(FIELD)
E, ONE, ZERO, lift = FIELD.E, FIELD.ONE, FIELD.ZERO, FIELD.lift
times, inverse, transpose = FIELD.times, FIELD.inverse, FIELD.transpose


def neg(a):
    return [[-x for x in row] for row in a]


def had(a, b):
    return [[x * y for x, y in zip(row, col)] for row, col in zip(a, b)]


def identity(n):
    return [[lift(i == j) for j in range(n)] for i in range(n)]


def kron(a, b):
    return [[x * y for x in row_a for y in row_b] for row_a in a for row_b in b]


def read_fixture(path=DEFAULT_FIXTURE):
    fixture = json.loads(Path(path).read_text(encoding="utf-8"))
    assert fixture["schema"] == "common-star-binary-resource-supply-control-v1"
    assert fixture["field"] == "Q(sqrt(3))"
    assert fixture["factor_dimension"] == 5 and fixture["index_copies"] == 25
    assert fixture["component_clones"] == 2
    assert fixture["tensor_dual_sign"] == -1
    return fixture


def base_data(fixture):
    """Exact dual product, strict cocycle, and signed tensor identities.

    The cloned S2 families follow entry by entry from these checked
    factorizations; the owning proof specifies that algebraic bridge.
    No global S2 word census is claimed here.
    """
    t = E(Fraction(fixture["t"]["rational"]), Fraction(fixture["t"]["radical"]))
    r = E(Fraction(fixture["r"]["rational"]), Fraction(fixture["r"]["radical"]))
    tokens = {"1": ONE, "t": t}
    a = [[tokens[token] for token in row] for row in fixture["seed_a"]]
    left, right = identity(5), identity(5)
    li, ri = fixture["left_seed_indices"], fixture["right_seed_indices"]
    assert len(li) == len(ri) == 3 and len(set(li) & set(ri)) == 1
    for i, j in itertools.product(range(3), repeat=2):
        left[li[i]][li[j]], right[ri[i]][ri[j]] = a[i][j], a[i][j]
    m = times(left, right)
    n = neg(transpose(inverse(m)))
    q = had(m, n)
    # Each scalar entry has at most one intermediate factor route, and
    # the inverse-transpose product has the same routes and zero support.
    il, ir = transpose(inverse(left)), transpose(inverse(right))
    assert transpose(inverse(m)) == times(il, ir)
    assert had(m, neg(n)) == times(had(left, il), had(right, ir))
    assert all(
        sum(bool(left[i][z] and right[z][j]) for z in range(5)) <= 1
        for i, j in itertools.product(range(5), repeat=2)
    )
    assert times(q, transpose(q)) == identity(5)
    assert all(sum(row, ZERO) == -ONE for row in q)
    assert times(m, transpose(n)) == neg(identity(5))
    assert all(
        bool(m[i][j]) == bool(n[i][j]) for i, j in itertools.product(range(5), repeat=2)
    )
    names = {"M": m, "M_transpose": transpose(m), "identity": identity(5)}
    f = {
        (int(pair[0]), int(pair[1])): names[name]
        for pair, name in fixture["first_pair_matrices"].items()
    }
    assert set(f) == {(0, 1), (0, 2), (1, 2)}
    for c, d in list(f):
        f[d, c] = transpose(f[c, d])
    nf = {pair: neg(transpose(inverse(matrix))) for pair, matrix in f.items()}
    qf = {pair: had(f[pair], nf[pair]) for pair in f}
    for pair in f:
        assert times(f[pair], transpose(nf[pair])) == neg(identity(5))
        assert times(qf[pair], transpose(qf[pair])) == identity(5)
    for c, d, e in itertools.permutations(range(3)):
        h = times(qf[d, c], qf[c, e])
        xy = had(times(f[d, c], nf[c, e]), times(nf[d, c], f[c, e]))
        assert h == xy == neg(qf[d, e])
    pi = fixture["second_color_permutation"]
    assert sorted(pi) == [0, 1, 2]
    matrices, duals, products = {}, {}, {}
    for c, d in f:
        matrices[c, d] = kron(f[c, d], f[pi[c], pi[d]])
        duals[c, d] = neg(kron(nf[c, d], nf[pi[c], pi[d]]))
        products[c, d] = had(matrices[c, d], duals[c, d])
        assert products[c, d] == neg(kron(qf[c, d], qf[pi[c], pi[d]]))
        assert all(sum(row, ZERO) == -ONE for row in products[c, d])
    # Exact tensor-factor identities, not an independent numerical test:
    # duality and Q-orthogonality tensor; H=K=-Q tensors with the displayed minus.
    # Clone scalar (1+r)(1+1/r)/4=3/2 converts 2H-3K to physical 2H-K.
    assert (ONE + r) * (ONE + ONE / r) / 4 == lift(Fraction(3, 2))
    return {
        "M": m,
        "N": n,
        "Q": q,
        "matrices": matrices,
        "duals": duals,
        "products": products,
        "r": r,
    }


def local_data(fixture, data=None):
    """Decode all 150 local states and 2,604 actual center/leaf factors."""
    data = base_data(fixture) if data is None else data
    matrices, duals, r = data["matrices"], data["duals"], data["r"]

    def port(c, d, clone):
        return r if clone and d == max(set(range(3)) - {c}) else ONE

    states = list(itertools.product(range(3), range(25), range(2)))
    edges = {}
    for u, (c, i, clone) in enumerate(states):
        for v in range(u + 1, len(states)):
            d, j, other_clone = states[v]
            if c == d or not matrices[c, d][i][j]:
                continue
            factor = port(c, d, clone) * port(d, c, other_clone)
            edges[u, v] = (
                matrices[c, d][i][j] * factor,
                duals[c, d][i][j] / (2 * factor),
            )
    assert len(edges) == 2604
    return states, edges


def finite_cover(states, local_edges, fixture):
    """Construct and inspect every actual gadget and scalar failure component."""
    assert fixture["group"] == "SL(2,F5)" and fixture["group_prime"] == 5
    shifts = tuple(
        tuple(tuple(matrix) for matrix in row) for row in fixture["translations"]
    )
    group = [
        m
        for m in itertools.product(range(5), repeat=4)
        if (m[0] * m[3] - m[1] * m[2]) % 5 == 1
    ]
    index = {m: i for i, m in enumerate(group)}
    assert len(group) == 120
    assert len(shifts) == 2 and all(len(row) == 3 for row in shifts)
    assert all(matrix in index for row in shifts for matrix in row)

    def mul(a, b):
        return (
            (a[0] * b[0] + a[1] * b[2]) % 5,
            (a[0] * b[1] + a[1] * b[3]) % 5,
            (a[2] * b[0] + a[3] * b[2]) % 5,
            (a[2] * b[1] + a[3] * b[3]) % 5,
        )

    resources = [[] for _ in group]
    for clone in range(2):
        for g, matrix in enumerate(group):
            for c in range(3):
                resources[index[mul(matrix, shifts[clone][c])]].append(
                    (clone * 120 + g, c, clone)
                )
    old_pairs = {}
    for resource in resources:
        assert len({u for u, _c, _f in resource}) == 6
        for x, y in itertools.combinations(resource, 2):
            pair = tuple(sorted((x[0], y[0])))
            assert pair not in old_pairs
            old_pairs[pair] = True

    gadgets, options = {}, {}
    ports = Counter()
    sums = {}
    products = {edge: a * b for edge, (a, b) in local_edges.items()}
    for resource_id, resource in enumerate(resources):
        by_role = {(c, clone): old for old, c, clone in resource}
        actual = [25 * by_role[c, clone] + i for c, i, clone in states]
        assert len(set(actual)) == 150
        for u, (c, _i, _f) in zip(actual, states):
            assert (u, c) not in options
            options[u, c] = resource_id
        for edge, (a, b) in local_edges.items():
            x, y = edge
            u, v, c, d = actual[x], actual[y], states[x][0], states[y][0]
            if u > v:
                u, v, c, d = v, u, d, c
            assert u < v and (u, v) not in gadgets
            gadgets[u, v] = (c, d, a, b, resource_id)
            for port in ((u, c, d), (v, d, c)):
                ports[port] += 1
                sums[port] = sums.get(port, ZERO) + products[edge]
    assert len(gadgets) == 312480 and len(options) == 18000
    assert len(sums) == 36000 and all(value == -ONE for value in sums.values())
    adjacency = [set() for _ in range(6000)]
    option_adj = {state: set() for state in options}
    for (u, v), (c, d, _a, _b, _r) in gadgets.items():
        adjacency[u].add(v)
        adjacency[v].add(u)
        option_adj[u, c].add((v, d))
        option_adj[v, d].add((u, c))
    triangle_count = 0
    for u in range(6000):
        for v in adjacency[u]:
            if v <= u:
                continue
            for w in adjacency[u] & adjacency[v]:
                if w <= v:
                    continue
                uv, uw, vw = gadgets[u, v], gadgets[u, w], gadgets[v, w]
                assert uv[0] == uw[0] and uv[1] == vw[0] and uw[1] == vw[1]
                assert uv[4] == uw[4] == vw[4]
                triangle_count += 1
    assert triangle_count == 423360

    def parts(allowed):
        pending = {state for state in options if state[1] in allowed}
        histogram = Counter()
        while pending:
            start = min(pending)
            part, stack = {start}, [start]
            while stack:
                for state in option_adj[stack.pop()]:
                    if state[1] in allowed and state not in part:
                        part.add(state)
                        stack.append(state)
            pending.difference_update(part)
            color_sizes = tuple(
                sum(state[1] == c for state in part) for c in sorted(allowed)
            )
            edge_count = (
                sum(sum(w[1] in allowed for w in option_adj[state]) for state in part)
                // 2
            )
            assert len({options[state] for state in part}) == 1
            if len(allowed) == 2:
                assert edge_count < color_sizes[0] * color_sizes[1]
            histogram[color_sizes, edge_count] += 1
        return [
            {"color_part_sizes": list(sizes), "edges": edges, "components": count}
            for (sizes, edges), count in sorted(histogram.items())
        ]

    all_parts = parts({0, 1, 2})
    binary_parts = {
        f"{c}{d}": parts({c, d}) for c, d in itertools.combinations(range(3), 2)
    }
    assert all_parts == [
        {"color_part_sizes": [50, 50, 50], "edges": 2604, "components": 120}
    ]
    assert binary_parts["01"] == [
        {"color_part_sizes": [50, 50], "edges": 1764, "components": 120}
    ]
    assert (
        binary_parts["02"]
        == binary_parts["12"]
        == [{"color_part_sizes": [10, 10], "edges": 84, "components": 600}]
    )

    colors = [fixture["failure_colors_by_clone"][u // 3000] for u in range(6000)]
    scalar = [[] for _ in range(24000)]

    def add(u, v, weight):
        scalar[u].append((v, weight))
        scalar[v].append((u, weight))

    for u, color in enumerate(colors):
        for x, y in itertools.combinations(range(4), 2):
            if x ^ y == color + 1:
                add(4 * u + x, 4 * u + y, ONE)
    for (u, v), (c, d, a, b, _r) in gadgets.items():
        if colors[u] == c and colors[v] == d:
            add(4 * u, 4 * v, a)
            add(4 * u + c + 1, 4 * v + d + 1, b)
    pending, scalar_sizes, signatures = set(range(24000)), Counter(), {}
    signature_count = Counter()
    while pending:
        start = min(pending)
        part, stack = {start}, [start]
        while stack:
            for v, _weight in scalar[stack.pop()]:
                if v not in part:
                    part.add(v)
                    stack.append(v)
        pending.difference_update(part)
        vertices = sorted(part)
        positions = {u: i for i, u in enumerate(vertices)}
        signature = tuple(
            (positions[u], positions[v], weight)
            for u in vertices
            for v, weight in sorted(scalar[u])
            if u < v
        )
        scalar_sizes[len(part)] += 1
        signature_count[signature] += 1
        if signature not in signatures:
            local = [[] for _ in vertices]
            for u, v, weight in signature:
                local[u].append((v, weight))
                local[v].append((u, weight))

            @lru_cache(maxsize=None)
            def haf(mask):
                if not mask:
                    return ONE, 1
                u = min(
                    (i for i in range(len(local)) if mask & (1 << i)),
                    key=lambda i: sum(bool(mask & (1 << j)) for j, _w in local[i]),
                )
                rest, total, count = mask ^ (1 << u), ZERO, 0
                for v, weight in local[u]:
                    if rest & (1 << v):
                        tail, ways = haf(rest ^ (1 << v))
                        total += weight * tail
                        count += ways
                return total, count

            signatures[signature] = haf((1 << len(vertices)) - 1)
    assert scalar_sizes == {2: 6000, 20: 600}
    values = Counter()
    for signature, multiplicity in signature_count.items():
        value, ways = signatures[signature]
        values[value, ways] += multiplicity
    expected_core = E(Fraction(-463, 2592))
    assert values == {(ONE, 1): 6000, (expected_core, 6130): 600}
    result = {
        "resources": 120,
        "components": 6000,
        "physical_vertices": 24000,
        "gadgets": len(gadgets),
        "simple_one_label_component_graph": True,
        "global_S1_port_sums_checked": len(sums),
        "ports_by_multiplicity": dict(sorted(Counter(ports.values()).items())),
        "physical_component_triangles": triangle_count,
        "all_component_triangles_coherent": True,
        "state_components": all_parts,
        "binary_components": binary_parts,
        "no_binary_pair_is_a_biclique_union": True,
        "full_failure_scalar_components": dict(scalar_sizes),
        "full_failure_scalar_edges": sum(map(len, scalar)) // 2,
        "full_failure_core_amplitude": "-463/2592",
        "full_failure_core_supported_matchings": 6130,
        "full_failure_amplitude": "(-463/2592)^600",
        "full_failure_supported_matchings": "6130^600",
        "physical_failure_replayed": True,
    }
    expected = fixture["expected"]
    for key in (
        "resources",
        "components",
        "physical_vertices",
        "gadgets",
        "global_S1_port_sums_checked",
        "physical_component_triangles",
    ):
        assert result[key] == expected[key]
    assert len(states) == expected["local_state_vertices"]
    assert len(local_edges) == expected["local_state_edges"]
    assert scalar_sizes[expected["failure_core_vertices"]] == expected["failure_cores"]
    assert scalar_sizes[2] == expected["failure_isolated_edges"]
    assert result["full_failure_scalar_edges"] == expected["failure_scalar_edges"]
    assert result["full_failure_core_amplitude"] == expected["failure_core_amplitude"]
    assert (
        result["full_failure_core_supported_matchings"]
        == expected["failure_core_supported_matchings"]
    )
    return result


def verify(fixture_path=DEFAULT_FIXTURE):
    fixture = read_fixture(fixture_path)
    data = base_data(fixture)
    states, edges = local_data(fixture, data)
    return {
        "schema": "common-star-binary-resource-supply-replay-v1",
        "scope": "exact BS countercontrol via owning source-locality/U4 proof; not CSQ4 or full GHZ",
        "field": "Q(sqrt(3))",
        "fixture_sha256_lf": hashlib.sha256(
            Path(fixture_path).read_bytes().replace(b"\r\n", b"\n")
        ).hexdigest(),
        "arithmetic_dependency": "claims/arbitrary-order/verify_common_star_resource_alignment_control.py",
        "arithmetic_dependency_sha256_lf": hashlib.sha256(
            ARITHMETIC_DEPENDENCY.read_bytes().replace(b"\r\n", b"\n")
        ).hexdigest(),
        "unambiguous_dual_product_checked": True,
        "strict_cocycle_and_signed_tensor_identities_checked": True,
        "clone_factor_exact": "3/2",
        "S2_bridge": "checked duality, Q orthogonality, strict cocycle, signed tensor, and clone factors; unique color-state resource membership",
        "full_U4_bridge": "global S1 and every actual component triangle coherent; exhaustive source classification in owning proof",
        "cover": finite_cover(states, edges, fixture),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, default=DEFAULT_FIXTURE)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = verify(args.fixture)
    encoded = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.write_text(encoded, encoding="utf-8")
    print(encoded, end="")


if __name__ == "__main__":
    main()
