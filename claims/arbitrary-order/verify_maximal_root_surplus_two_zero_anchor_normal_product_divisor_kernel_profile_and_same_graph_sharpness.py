"""Exact primary checks for the GLS30 normal-product divisor theorem."""

from __future__ import annotations

from functools import cache
from itertools import combinations, product

import sympy as sp

COLOURS = range(3)
PORTS = tuple(range(4))
PAIRS = tuple(combinations(PORTS, 2))


@cache
def matchings(vertices: tuple[int, ...]) -> tuple[tuple[tuple[int, int], ...], ...]:
    if not vertices:
        return ((),)
    first = vertices[0]
    output = []
    for position in range(1, len(vertices)):
        second = vertices[position]
        remainder = vertices[1:position] + vertices[position + 1 :]
        for tail in matchings(remainder):
            output.append(((first, second), *tail))
    return tuple(output)


def edge_block(
    edges: dict[tuple[int, int], sp.Matrix], left: int, right: int
) -> sp.Matrix:
    if left < right:
        return edges.get((left, right), sp.zeros(3))
    return edges.get((right, left), sp.zeros(3)).T


def put_edge(
    edges: dict[tuple[int, int], sp.Matrix],
    left: int,
    right: int,
    matrix: sp.Matrix,
) -> None:
    if left < right:
        edges[(left, right)] = matrix
    else:
        edges[(right, left)] = matrix.T


def graph_coefficient(
    word: tuple[int, ...], edges: dict[tuple[int, int], sp.Matrix]
) -> sp.Expr:
    total = sp.Integer(0)
    for matching in matchings(tuple(range(len(word)))):
        term = sp.Integer(1)
        for left, right in matching:
            term *= edge_block(edges, left, right)[word[left], word[right]]
        total += term
    return sp.expand(total)


def contracted_coefficient(
    fixed: dict[int, int],
    weights: dict[int, sp.Matrix],
    edges: dict[tuple[int, int], sp.Matrix],
    vertices: tuple[int, ...],
) -> sp.Expr:
    """Sum a matching coefficient over independently weighted free vertices."""
    total = sp.Integer(0)
    local_index = {vertex: index for index, vertex in enumerate(vertices)}
    for local_matching in matchings(tuple(range(len(vertices)))):
        term = sp.Integer(1)
        for local_left, local_right in local_matching:
            left = vertices[local_left]
            right = vertices[local_right]
            block = edge_block(edges, left, right)
            if left in fixed and right in fixed:
                factor = block[fixed[left], fixed[right]]
            elif left in fixed:
                factor = (block[fixed[left], :] * weights[right])[0]
            elif right in fixed:
                factor = (weights[left].T * block[:, fixed[right]])[0]
            else:
                factor = (weights[left].T * block * weights[right])[0]
            term *= factor
        total += term
    assert len(local_index) == len(vertices)
    return sp.expand(total)


def outer(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return left * right.T


def channel_pair(
    x: tuple[sp.Matrix, ...], y: tuple[sp.Matrix, ...], pair: tuple[int, int]
) -> sp.Matrix:
    left, right = pair
    return outer(x[left], y[right]) + outer(y[left], x[right])


def complement(pair: tuple[int, int]) -> tuple[int, int]:
    return tuple(port for port in PORTS if port not in pair)  # type: ignore[return-value]


def tensor4_from_pair_terms(
    suppliers: dict[tuple[int, int], sp.Matrix],
    responses: dict[tuple[int, int], sp.Matrix],
) -> sp.MutableDenseNDimArray:
    output = sp.MutableDenseNDimArray.zeros(3, 3, 3, 3)
    for pair in PAIRS:
        other = complement(pair)
        for word in product(COLOURS, repeat=4):
            output[word] += (
                suppliers[pair][word[pair[0]], word[pair[1]]]
                * responses[other][word[other[0]], word[other[1]]]
            )
    return output


def diagonal_tensor(beta: tuple[sp.Expr, ...]) -> sp.MutableDenseNDimArray:
    output = sp.MutableDenseNDimArray.zeros(3, 3, 3, 3)
    for colour, value in enumerate(beta):
        output[(colour,) * 4] = value
    return output


def check_arbitrary_port_supplier_isolation() -> dict[str, object]:
    # Five ports test the arbitrary-root statement beyond the four-port fibre.
    port_count = 5
    x = tuple(sp.Matrix((1 + u, 2 - u, u % 2)) for u in range(port_count))
    y = tuple(sp.Matrix((u - 1, 1, 3 - u)) for u in range(port_count))
    kernels = []
    for u in range(port_count):
        nullspace = sp.Matrix.hstack(x[u], y[u]).T.nullspace()
        assert len(nullspace) == 1
        kernels.append(nullspace[0])

    def response_value(complement_ports: tuple[int, ...], word: tuple[int, ...]) -> int:
        return 1 + sum((port + 1) * (word[port] + 1) for port in complement_ports)

    checks = 0
    for kept in combinations(range(port_count), 2):
        cut = tuple(port for port in range(port_count) if port not in kept)
        observed = sp.zeros(3)
        for kept_word in product(COLOURS, repeat=2):
            value = sp.Integer(0)
            for full_cut_word in product(COLOURS, repeat=len(cut)):
                word = [0] * port_count
                for port, colour in zip(kept, kept_word, strict=True):
                    word[port] = colour
                for port, colour in zip(cut, full_cut_word, strict=True):
                    word[port] = colour
                contraction = sp.prod(kernels[port][word[port]] for port in cut)
                full_tensor_value = sp.Integer(0)
                for supplier_pair in combinations(range(port_count), 2):
                    response_ports = tuple(
                        port for port in range(port_count) if port not in supplier_pair
                    )
                    supplier = channel_pair(x, y, supplier_pair)
                    full_tensor_value += supplier[
                        word[supplier_pair[0]], word[supplier_pair[1]]
                    ] * response_value(response_ports, tuple(word))
                value += contraction * full_tensor_value
            observed[kept_word[0], kept_word[1]] = sp.expand(value)

        response_contraction = sp.Integer(0)
        for cut_word in product(COLOURS, repeat=len(cut)):
            word = [0] * port_count
            for port, colour in zip(cut, cut_word, strict=True):
                word[port] = colour
            response_contraction += sp.prod(
                kernels[port][word[port]] for port in cut
            ) * response_value(cut, tuple(word))
        expected = response_contraction * channel_pair(x, y, kept)
        assert observed == expected
        checks += 1
    return {"ports": port_count, "isolated_pairs": checks}


def one_active_control() -> tuple[
    tuple[sp.Matrix, ...],
    tuple[sp.Matrix, ...],
    dict[tuple[int, int], sp.Matrix],
]:
    e0 = sp.eye(3)[:, 0]
    x = (e0,) * 4
    y = (e0,) * 4
    scalars = (1, 1, 1, 1, 1, sp.Rational(-9, 2))
    responses = {
        pair: scalar * outer(e0, e0)
        for pair, scalar in zip(PAIRS, scalars, strict=True)
    }
    return x, y, responses


def two_active_control() -> tuple[
    tuple[sp.Matrix, ...],
    tuple[sp.Matrix, ...],
    dict[tuple[int, int], sp.Matrix],
]:
    e0, e1, _e2 = sp.eye(3).columnspace()
    x = (e0, e0, e1, e1)
    y = x
    responses: dict[tuple[int, int], sp.Matrix] = {
        (0, 1): outer(e1, e1),
        (2, 3): sp.Rational(1, 2) * outer(e0, e0),
    }
    lambdas = (1, 1, 1, -3)
    for pair, scalar in zip(((0, 2), (0, 3), (1, 2), (1, 3)), lambdas, strict=True):
        responses[pair] = scalar * outer(e0, e1)
    return x, y, responses


def check_divisor_controls() -> dict[str, object]:
    results = {}
    for label, data, beta in (
        ("one_active", one_active_control(), (sp.Integer(1), 0, 0)),
        ("two_active", two_active_control(), (sp.Integer(1), 2, 0)),
    ):
        x, y, responses = data
        suppliers = {pair: channel_pair(x, y, pair) for pair in PAIRS}
        assert all(response != sp.zeros(3) for response in responses.values())
        assert all(supplier != sp.zeros(3) for supplier in suppliers.values())
        assert tensor4_from_pair_terms(suppliers, responses) == diagonal_tensor(beta)
        # Every target has a unique nonzero disjoint supplier, so its normal
        # nuisance image is the full nine-dimensional target space.
        full_normal_images = sum(
            suppliers[complement(target)] != sp.zeros(3) for target in PAIRS
        )
        assert full_normal_images == 6
        results[label] = {
            "nonzero_suppliers": 6,
            "nonzero_responses": 6,
            "full_normal_images": full_normal_images,
        }
    return results


def hadamard_space(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    columns = [
        left[:, i].multiply_elementwise(right[:, j])
        for i, j in product(range(left.cols), range(right.cols))
    ]
    basis = sp.Matrix.hstack(*columns).columnspace()
    return sp.Matrix.hstack(*basis) if basis else sp.zeros(left.rows, 0)


def check_projected_kernel_rules() -> dict[str, object]:
    e0, e1 = sp.eye(2).columnspace()
    lines = (sp.Matrix.hstack(e0), sp.Matrix.hstack(e1), sp.Matrix.hstack(e0 + e1))
    plane = sp.eye(2)
    zero = sp.zeros(2, 0)
    spaces = (zero, *lines, plane)
    accepted = 0
    for left, right in product(spaces, repeat=2):
        star = hadamard_space(left, right)
        if star.rank() <= 1:
            if left.rank() == 2 and right.rank():
                assert right in (lines[0], lines[1])
            if right.rank() == 2 and left.rank():
                assert left in (lines[0], lines[1])
            accepted += 1
    assert hadamard_space(plane, plane).rank() == 2
    assert hadamard_space(plane, lines[2]).rank() == 2
    return {"sampled_projected_pairs": len(spaces) ** 2, "accepted": accepted}


def build_response_deck_graph(
    x: tuple[sp.Matrix, ...],
    y: tuple[sp.Matrix, ...],
    responses: dict[tuple[int, int], sp.Matrix],
    active_count: int,
) -> tuple[dict[tuple[int, int], sp.Matrix], sp.Matrix, sp.Matrix, sp.Expr]:
    # Vertex order a0,a1,q0,q1,u0,u1,u2,u3.
    edges: dict[tuple[int, int], sp.Matrix] = {}
    e0 = sp.eye(3)[:, 0]
    n0 = sp.Matrix((1, 1, 0))
    xi00 = sp.Matrix((0, 0, 1))
    xi01 = sp.Matrix((1, -1, 1))
    if active_count == 1:
        n1 = sp.Matrix((1, 0, 1))
        xi10 = sp.Matrix((0, 1, 0))
        xi11 = sp.Matrix((1, 1, -1))
    else:
        n1 = sp.Matrix((1, 2, 1))
        xi10 = sp.Matrix((0, 1, -2))
        xi11 = sp.Matrix((1, 1, -3))

    put_edge(edges, 0, 2, outer(xi00, e0))
    put_edge(edges, 0, 3, outer(xi01, e0))
    put_edge(edges, 1, 2, outer(xi10, e0))
    put_edge(edges, 1, 3, outer(xi11, e0))
    for port in PORTS:
        put_edge(edges, 0, 4 + port, outer(e0, x[port]))
        put_edge(edges, 1, 4 + port, outer(e0, y[port]))
    put_edge(edges, 2, 3, outer(e0, e0))
    for pair, response in responses.items():
        put_edge(edges, 4 + pair[0], 4 + pair[1], response)

    q = outer(xi00, xi11) + outer(xi01, xi10)
    p = sum(q)
    assert n0.dot(xi00) == n0.dot(xi01) == 0
    assert n1.dot(xi10) == n1.dot(xi11) == 0
    assert p == (2 if active_count == 1 else -2)
    return edges, n0, n1, p


def check_same_graph_response_decks() -> dict[str, object]:
    results = {}
    ones = sp.ones(3, 1)
    for label, data, beta, active_count in (
        ("one_active", one_active_control(), (1, 0, 0), 1),
        ("two_active", two_active_control(), (1, 2, 0), 2),
    ):
        x, y, responses = data
        edges, n0, n1, p = build_response_deck_graph(x, y, responses, active_count)
        weights = {0: n0, 1: n1, 2: ones, 3: ones}
        observed = sp.MutableDenseNDimArray.zeros(3, 3, 3, 3)
        for word in product(COLOURS, repeat=4):
            fixed = {4 + port: word[port] for port in PORTS}
            observed[word] = contracted_coefficient(
                fixed, weights, edges, tuple(range(8))
            )
        assert observed == diagonal_tensor(tuple(map(sp.Integer, beta)))

        response_checks = 0
        for pair in PAIRS:
            vertices = (2, 3, 4 + pair[0], 4 + pair[1])
            for word in product(COLOURS, repeat=2):
                value = contracted_coefficient(
                    {vertices[2]: word[0], vertices[3]: word[1]},
                    {2: ones, 3: ones},
                    edges,
                    vertices,
                )
                assert value == responses[pair][word]
                response_checks += 1
        results[label] = {
            "p": p,
            "normal_coefficients": 81,
            "physical_response_coefficients": response_checks,
        }
    return results


def matrix_unit(row: int, column: int, value: sp.Expr = 1) -> sp.Matrix:
    output = sp.zeros(3)
    output[row, column] = value
    return output


def build_maximum_root_control() -> dict[tuple[int, int], sp.Matrix]:
    # Vertex order a0,a1,k,q0,q1,u1,u2,u3.
    edges: dict[tuple[int, int], sp.Matrix] = {}
    e00 = matrix_unit(0, 0)
    root_cancel = e00 - matrix_unit(1, 0)
    put_edge(edges, 0, 2, root_cancel)
    put_edge(edges, 1, 2, root_cancel)
    put_edge(edges, 0, 3, matrix_unit(1, 1))
    put_edge(edges, 0, 4, matrix_unit(2, 2))
    put_edge(edges, 1, 3, matrix_unit(2, 2))
    put_edge(edges, 1, 4, matrix_unit(1, 1))
    put_edge(edges, 0, 5, e00)
    put_edge(edges, 1, 5, e00)
    for port in (6, 7):
        put_edge(edges, 0, port, matrix_unit(1, 0))
        put_edge(edges, 1, port, matrix_unit(2, 1))
    put_edge(edges, 3, 4, e00)
    put_edge(edges, 2, 5, matrix_unit(0, 1))
    put_edge(edges, 2, 6, matrix_unit(1, 1))
    put_edge(edges, 2, 7, matrix_unit(2, 2))
    put_edge(edges, 5, 6, matrix_unit(2, 2))
    put_edge(edges, 5, 7, matrix_unit(1, 1))
    put_edge(edges, 6, 7, matrix_unit(0, 0, sp.Rational(1, 2)))
    return edges


def check_maximum_root_pure_control() -> dict[str, object]:
    edges = build_maximum_root_control()
    ones = sp.ones(3, 1)
    roots = (0, 1, 2)
    outside = (3, 4, 5, 6, 7)
    for left, right in combinations(roots, 2):
        assert (ones.T * edge_block(edges, left, right) * ones)[0] == 0

    # These three nowhere-zero monomial cliques cover all eight vertices.
    cliques = ((0, 3, 4), (1, 6, 7), (2, 5))
    for clique in cliques:
        for pair in combinations(clique, 2):
            assert sum(entry != 0 for entry in edge_block(edges, *pair)) == 1
    monomial_edges = {
        pair
        for pair in combinations(range(8), 2)
        if sum(entry != 0 for entry in edge_block(edges, *pair)) == 1
    }
    independent = []
    for mask in range(1 << 8):
        subset = tuple(vertex for vertex in range(8) if mask & (1 << vertex))
        if all(pair not in monomial_edges for pair in combinations(subset, 2)):
            independent.append(subset)
    assert max(map(len, independent)) == 3
    assert roots in independent

    incidence = {}
    for vertex in outside:
        incidence[vertex] = sp.Matrix(
            3,
            3,
            lambda root, colour, vertex=vertex: (
                ones.T * edge_block(edges, root, vertex)
            )[0, colour],
        )
    incidence_ranks = tuple(incidence[vertex].rank() for vertex in outside)
    assert incidence_ranks == (2, 2, 2, 2, 3)
    assert sum(3 - rank for rank in incidence_ranks) == 4

    q = sp.zeros(3)
    for a0, a1, q0, q1 in product(COLOURS, repeat=4):
        q[a0, a1] += (
            edge_block(edges, 0, 3)[a0, q0] * edge_block(edges, 1, 4)[a1, q1]
            + edge_block(edges, 0, 4)[a0, q1] * edge_block(edges, 1, 3)[a1, q0]
        )
    assert q == matrix_unit(1, 1) + matrix_unit(2, 2)
    assert sum(q) == 2

    pure = tuple(graph_coefficient((colour,) * 8, edges) for colour in COLOURS)
    assert pure == (1, 1, 1)
    failed = {
        word: graph_coefficient(word, edges)
        for word in ((0, 1, 0, 0, 0, 0, 0, 0), (1, 0, 0, 0, 0, 0, 0, 0))
    }
    assert tuple(failed.values()) == (sp.Rational(-1, 2),) * 2

    # Pair responses on q0,q1 plus each promoted pair are exactly W_D.
    promoted = (2, 5, 6, 7)
    response_checks = 0
    for pair in combinations(promoted, 2):
        vertices = (3, 4, *pair)
        for word in product(COLOURS, repeat=2):
            observed = contracted_coefficient(
                {pair[0]: word[0], pair[1]: word[1]},
                {3: ones, 4: ones},
                edges,
                vertices,
            )
            assert observed == edge_block(edges, *pair)[word]
            response_checks += 1
        assert edge_block(edges, *pair) != sp.zeros(3)

    # Residual shores are <e1,e2>, normal e0, and q=e11+e22 has p=2.
    e0 = sp.eye(3)[:, 0]
    weights = {0: e0, 1: e0, 3: ones, 4: ones}
    normal_tensor = sp.MutableDenseNDimArray.zeros(3, 3, 3, 3)
    for word in product(COLOURS, repeat=4):
        fixed = {promoted[index]: word[index] for index in range(4)}
        normal_tensor[word] = contracted_coefficient(
            fixed, weights, edges, tuple(range(8))
        )
    assert normal_tensor == diagonal_tensor((sp.Integer(1), 0, 0))
    return {
        "maximum_torus_root_size": 3,
        "incidence_ranks": incidence_ranks,
        "defect_sum": 4,
        "pure_coefficients": pure,
        "nonzero_pair_responses": 6,
        "response_coefficients": response_checks,
        "normal_coefficients": 81,
        "failed_mixed_coefficients": failed,
    }


def main() -> None:
    print("GLS30 normal-product divisor primary verifier: PASS")
    print("  arbitrary-port isolation:", check_arbitrary_port_supplier_isolation())
    print("  projected-kernel rules:", check_projected_kernel_rules())
    print("  exact divisor controls:", check_divisor_controls())
    print("  physical response decks:", check_same_graph_response_decks())
    print("  maximum-root pure control:", check_maximum_root_pure_control())
    print(
        "  scope: normal identity plus six responses and full normal images is insufficient; combined maximum-root absorption, full mixed GHZ, and node closure remain open"
    )


if __name__ == "__main__":
    main()
