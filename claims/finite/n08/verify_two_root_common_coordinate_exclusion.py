"""Exact displayed-identity replay for the two-root coordinate-column proof.

The written proof, not this finite replay, establishes the quantified
eight-vertex exclusion. No GHZ witness or generic specialization is tested.
"""

from itertools import combinations, product
import json

import sympy as sp


def matchings(vertices):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for partner in vertices[1:]:
        rest = tuple(v for v in vertices[1:] if v != partner)
        for tail in matchings(rest):
            yield ((first, partner),) + tail


def haf(vertices, edges):
    return sum(
        sp.prod(edges[tuple(sorted(edge))] for edge in matching)
        for matching in matchings(tuple(vertices))
    )


def zero(expression):
    assert sp.expand(expression) == 0


def source_identity():
    outside = tuple(range(2, 8))
    edges = {
        edge: sp.Symbol(f"w{edge[0]}{edge[1]}") for edge in combinations(outside, 2)
    }
    active = sp.symbols("z0:6")
    aa = sp.symbols("a0:6")
    bb = sp.symbols("b0:6")
    q = sp.Symbol("q")
    whole = dict(edges)
    whole[0, 1] = q
    for i, u in enumerate(outside):
        whole[0, u] = aa[i] * active[i]
        whole[1, u] = bb[i] * active[i]
    expected = q * haf(outside, edges)
    for i, j in combinations(range(6), 2):
        rest = tuple(u for u in outside if u not in (outside[i], outside[j]))
        expected += (
            active[i] * active[j] * (aa[i] * bb[j] + aa[j] * bb[i]) * haf(rest, edges)
        )
    zero(haf(range(8), whole) - expected)
    return len(list(matchings(tuple(range(8)))))


def cofactor_identities():
    xx = sp.Matrix(2, 2, sp.symbols("x0:4"))
    yy = sp.Matrix(2, 2, sp.symbols("y0:4"))
    zz = sp.Matrix(2, 2, sp.symbols("z0:4"))
    swap = sp.Matrix([[0, 1], [1, 0]])
    edges = {edge: sp.Integer(0) for edge in combinations(range(6), 2)}
    for i, j in product(range(2), repeat=2):
        edges[i, 2 + j] = xx[i, j]
        edges[i, 4 + j] = yy[i, j]
        edges[2 + i, 4 + j] = zz[i, j]
    full = haf(range(6), edges)
    expanded = sum(
        xx[i, j] * yy[1 - i, k] * zz[1 - j, 1 - k]
        for i, j, k in product(range(2), repeat=3)
    )
    zero(full - expanded)
    for block, formula in (
        (xx, swap * yy * swap * zz.T * swap),
        (yy, swap * xx * swap * zz * swap),
        (zz, swap * xx.T * swap * yy * swap),
    ):
        for i, j in product(range(2), repeat=2):
            zero(sp.diff(full, block[i, j]) - formula[i, j])
    for pair, block in (((0, 1), zz), ((2, 3), yy), ((4, 5), xx)):
        rest = tuple(v for v in range(6) if v not in pair)
        zero(haf(rest, edges) - block[0, 0] * block[1, 1] - block[0, 1] * block[1, 0])


def stress_and_flattening():
    t0, t1, t2 = sp.symbols("t0:3")
    triangle = sp.Matrix([[1, 1, 0], [1, 0, 1], [0, 1, 1]])
    assert triangle.det() == -2
    solution = triangle.inv() * sp.Matrix([-t0, -t1, -t2])
    for actual, expected in zip(
        solution, ((-t0 - t1 + t2) / 2, (-t0 + t1 - t2) / 2, (t0 - t1 - t2) / 2)
    ):
        zero(actual - expected)
    alpha, beta = sp.symbols("alpha beta", nonzero=True)
    for other_left, other_right in product(range(2), repeat=2):
        # Rows are (A_j, B_k), columns (A_k, B_j).
        matrix = sp.zeros(4)
        matrix[0, 0] = alpha
        row, col = 2 + other_right, 2 * other_left + 1
        matrix[row, col] = -beta
        zero(matrix.extract([0, row], [0, col]).det() + alpha * beta)
        assert matrix.rank() == 2


def rank_two_root_identity():
    left = sp.Matrix(3, 2, sp.symbols("l0:6"))
    right = sp.Matrix(3, 2, sp.symbols("r0:6"))
    root = left * right.T
    gamma, delta = sp.symbols("gamma delta")
    for c in range(3):
        unit = sp.zeros(3)
        unit[c, c] = 1
        zero(
            (gamma * root + delta * unit).det()
            - gamma**2 * delta * root.adjugate()[c, c]
        )
    example = sp.eye(3) - sp.ones(3) / 3
    assert example.rank() == 2
    assert example * sp.ones(3, 1) == sp.zeros(3, 1)
    assert example.T * sp.ones(3, 1) == sp.zeros(3, 1)
    for c in range(3):
        assert example.adjugate()[c, c] == sp.Rational(1, 3)
        assert example.row_join(sp.eye(3)[:, c]).rank() == 3
        assert example.T.row_join(sp.eye(3)[:, c]).rank() == 3
    boundary = sp.Matrix([[0, 0, 0], [1, 1, -1], [1, 2, -2]])
    assert boundary.rank() == 2
    left_null = boundary.T.nullspace()[0]
    right_null = boundary.nullspace()[0]
    assert all(left_null[c] != 0 or right_null[c] != 0 for c in range(3))
    assert all(boundary.adjugate()[c, c] == 0 for c in range(3))


def dependent_channel_triangle():
    lam = sp.Symbol("lam", nonzero=True)
    s, t, p, q, mu, nu = variables = sp.symbols("s t p q mu nu")
    equations = [p - mu, lam * t - mu, q + lam * s, lam * s - nu, q - nu, p + lam * t]
    matrix, rhs = sp.linear_eq_to_matrix(equations, variables)
    assert rhs == sp.zeros(6, 1)
    determinant = sp.factor(matrix.det())
    terms = sp.Poly(determinant, lam).terms()
    assert len(terms) == 1 and terms[0][1] != 0
    return str(determinant)


def graph_bound_and_cycles():
    cross = [edge for edge in combinations(range(6), 2) if edge[0] // 2 != edge[1] // 2]
    equality_cases = 0
    for mask in range(1 << len(cross)):
        chosen = {edge for index, edge in enumerate(cross) if mask >> index & 1}
        adjacency = {u: set() for u in range(6)}
        for u, v in chosen:
            adjacency[u].add(v)
            adjacency[v].add(u)
        unseen, components = set(range(6)), []
        while unseen:
            todo, component = [next(iter(unseen))], set()
            while todo:
                u = todo.pop()
                if u in component:
                    continue
                component.add(u)
                todo.extend(adjacency[u] - component)
            unseen -= component
            components.append(component)
        if max(map(len, components)) > 3:
            continue
        assert len(chosen) <= 6
        if len(chosen) != 6:
            continue
        assert sorted(map(len, components)) == [3, 3]
        assert all(len(adjacency[u]) == 2 for u in range(6))
        physical = set(cross) - chosen
        surviving = [m for m in matchings(tuple(range(6))) if set(m) <= physical]
        assert len(surviving) == 2
        words = []
        for matching in surviving:
            word = [None] * 6
            for u, v in matching:
                colour = 3 - u // 2 - v // 2
                word[u] = word[v] = colour
            words.append(word)
        assert all(a != b for a, b in zip(*words))
        equality_cases += 1
    assert equality_cases == 4
    return equality_cases


def four_vertex_component_cover():
    cross = [e for e in combinations(range(6), 2) if e[0] // 2 != e[1] // 2]
    counts = {"two_full_groups": 0, "one_full_group": 0}
    for mask in range(1 << len(cross)):
        edges = {e for index, e in enumerate(cross) if mask >> index & 1}
        adjacency = {v: set() for v in range(6)}
        for u, v in edges:
            adjacency[u].add(v)
            adjacency[v].add(u)
        unseen, squares, admissible = set(range(6)), [], True
        while unseen and admissible:
            start = next(iter(unseen))
            component, todo = set(), [start]
            while todo:
                v = todo.pop()
                if v not in component:
                    component.add(v)
                    todo.extend(adjacency[v] - component)
            unseen -= component
            if len(component) > 4:
                admissible = False
                break
            if len(component) == 3 and all(len(adjacency[v]) == 2 for v in component):
                continue
            side, todo, bipartite = {start: 0}, [start], True
            while todo:
                v = todo.pop()
                for u in adjacency[v]:
                    if u not in side:
                        side[u] = 1 - side[v]
                        todo.append(u)
                    elif side[u] == side[v]:
                        bipartite = False
            if not bipartite or any(
                ((u in adjacency[v]) != (side[u] != side[v]))
                or (u // 2 == v // 2 and side[u] != side[v])
                for u, v in combinations(component, 2)
            ):
                admissible = False
                break
            if len(component) == 4 and sum(side.values()) == 2:
                squares.append(component)
        if not admissible:
            continue
        if not squares:
            assert len(edges) <= 6
            if len(edges) == 6:
                assert all(len(adjacency[v]) == 2 for v in range(6))
            continue
        assert len(squares) == 1
        square = squares[0]
        group_counts = [sum(v // 2 == c for v in square) for c in range(3)]
        if sorted(group_counts) == [0, 2, 2]:
            counts["two_full_groups"] += 1
            assert len({tuple(sorted((u // 2, v // 2))) for u, v in edges}) == 1
            continue
        assert sorted(group_counts) == [1, 1, 2]
        counts["one_full_group"] += 1
        full = group_counts.index(2)
        others = [c for c in range(3) if c != full]
        for other in others:
            touching = [e for e in edges if {e[0] // 2, e[1] // 2} == {full, other}]
            assert len(touching) == 2
            assert len({v for e in touching for v in e if v // 2 == other}) == 1
        remaining = [e for e in edges if {e[0] // 2, e[1] // 2} == set(others)]
        assert len(remaining) <= 1
        for u, v in remaining:
            assert u not in square and v not in square
            assert len(adjacency[u]) == len(adjacency[v]) == 1
    assert counts == {"two_full_groups": 3, "one_full_group": 24}
    return counts


if __name__ == "__main__":
    count = source_identity()
    cofactor_identities()
    stress_and_flattening()
    rank_two_root_identity()
    triangle_determinant = dependent_channel_triangle()
    cycles = graph_bound_and_cycles()
    square_cover = four_vertex_component_cover()
    print(
        json.dumps(
            {
                "status": "PASS",
                "scope": "displayed identities and finite graph algebra; written proof remains load-bearing",
                "eight_vertex_matching_terms": count,
                "cross_gradient_identities": 12,
                "flattening_cases": 4,
                "rank_two_determinant_identities": 3,
                "dependent_channel_triangle_determinant": triangle_determinant,
                "two_triangle_complements": cycles,
                "four_cycle_cover": square_cover,
            },
            indent=2,
        )
    )
