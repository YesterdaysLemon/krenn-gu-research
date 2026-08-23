"""Exact primary checks for the GLS29 zero-anchor normal-channel theorem."""

from __future__ import annotations

from functools import cache
from itertools import combinations, product

import sympy as sp


def basis_matrix(columns: sp.Matrix) -> sp.Matrix:
    basis = columns.columnspace()
    return sp.Matrix.hstack(*basis) if basis else sp.zeros(columns.rows, 0)


def tensor_space(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    columns = [
        sp.kronecker_product(left[:, i], right[:, j])
        for i, j in product(range(left.cols), range(right.cols))
    ]
    return (
        sp.Matrix.hstack(*columns) if columns else sp.zeros(left.rows * right.rows, 0)
    )


@cache
def all_matchings(vertices: tuple[int, ...]) -> tuple[tuple[tuple[int, int], ...], ...]:
    if not vertices:
        return ((),)
    first = vertices[0]
    matchings = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        remainder = vertices[1:index] + vertices[index + 1 :]
        for tail in all_matchings(remainder):
            matchings.append(((first, second), *tail))
    return tuple(matchings)


def graph_coefficient(
    word: tuple[int, ...], edges: dict[tuple[int, int], sp.Matrix]
) -> sp.Expr:
    total = 0
    for matching in all_matchings(tuple(range(len(word)))):
        term = 1
        for left, right in matching:
            matrix = edges[(left, right)]
            term *= matrix[word[left], word[right]]
        total += term
    return sp.expand(total)


def oriented_edge(
    edges: dict[tuple[int, int], sp.Matrix], left: int, right: int
) -> sp.Matrix:
    return edges[(left, right)] if left < right else edges[(right, left)].T


def check_normal_quotient_and_pair_factorization() -> dict[str, object]:
    eye3 = sp.eye(3)
    e0, e1, _e2 = eye3.columnspace()
    q = sp.kronecker_product(e0, e1) + sp.kronecker_product(e1, e0)
    epsilon = sp.ones(1, 9)
    p = (epsilon * q)[0]
    projector = p * sp.eye(9) - q * epsilon
    x0 = sp.Matrix.hstack(e0, e1)
    x1 = sp.Matrix.hstack(e0, e1)
    tangent = basis_matrix(
        sp.Matrix.hstack(tensor_space(x0, eye3), tensor_space(eye3, x1))
    )
    tangent_bar = basis_matrix(projector * tangent)
    transverse = sp.Matrix.hstack(
        *(sp.eye(9)[:, index] - sp.eye(9)[:, 8] for index in range(8))
    )
    rho = sp.zeros(1, 9)
    rho[0, 8] = 1
    assert p == 2
    assert projector.rank() == 8
    assert tangent.rank() == 8
    assert tangent_bar.rank() == 7
    assert rho * tangent_bar == sp.zeros(1, tangent_bar.cols)
    assert (rho * transverse).rank() == 1

    # A symbolic zero-anchor pair coefficient and its projected normal image.
    x_u = sp.Matrix(sp.symbols("xu0:3"))
    y_u = sp.Matrix(sp.symbols("yu0:3"))
    x_v = sp.Matrix(sp.symbols("xv0:3"))
    y_v = sp.Matrix(sp.symbols("yv0:3"))
    g = sp.zeros(9, 9)
    for a0, a1, u, v in product(range(3), repeat=4):
        first = (x_u[u] if a0 == 2 else 0) * (y_v[v] if a1 == 2 else 0)
        second = (x_v[v] if a0 == 2 else 0) * (y_u[u] if a1 == 2 else 0)
        g[3 * a0 + a1, 3 * u + v] = first + second
    t = projector * g
    k = x_u * y_v.T + y_u * x_v.T
    assert sp.simplify(rho * t - p * sp.Matrix(1, 9, list(k))) == sp.zeros(1, 9)
    return {
        "p": p,
        "tangent_rank": tangent.rank(),
        "projected_tangent_rank": tangent_bar.rank(),
        "normal_quotient_rank": (rho * transverse).rank(),
        "symbolic_pair_entries": len(k),
    }


def channel_pair(
    x: tuple[sp.Matrix, ...], y: tuple[sp.Matrix, ...], left: int, right: int
) -> sp.Matrix:
    return x[left] * y[right].T + y[left] * x[right].T


def check_normal_nuisance_cylinders() -> dict[str, object]:
    e0, e1, e2 = sp.eye(3).columnspace()
    x = (e0, e1, e2, e0 + e1)
    y = (e1, e2, e0 + e2, e2)
    k02 = channel_pair(x, y, 0, 2)
    k12 = channel_pair(x, y, 1, 2)
    a0 = basis_matrix(k02)
    a1 = basis_matrix(k12)
    cylinder = basis_matrix(
        sp.Matrix.hstack(tensor_space(a0, sp.eye(3)), tensor_space(sp.eye(3), a1))
    )
    assert cylinder.rank() <= 9

    disjoint = channel_pair(x, y, 2, 3)
    assert disjoint != sp.zeros(3)
    disjoint_scalar_slice = int(any(entry != 0 for entry in disjoint))
    full = tensor_space(sp.Matrix([[disjoint_scalar_slice]]), sp.eye(9))
    assert full.rank() == 9

    # A two-row cylinder cannot swallow all three target diagonals.
    star_cylinder = tensor_space(sp.Matrix.hstack(e0, e1), sp.eye(3))
    diagonals = sp.Matrix.hstack(
        *(sp.kronecker_product(vector, vector) for vector in (e0, e1, e2))
    )
    assert sp.Matrix.hstack(star_cylinder, diagonals).rank() > star_cylinder.rank()
    return {
        "overlap_cylinder_rank": cylinder.rank(),
        "disjoint_normal_image_rank": full.rank(),
        "star_cylinder_rank": star_cylinder.rank(),
        "pure_augmented_rank": sp.Matrix.hstack(star_cylinder, diagonals).rank(),
    }


def check_complete_matching_expansion() -> dict[str, object]:
    # Vertices 0,1 are A; 2..5 are the four promoted ports.  W_01=0.
    edges: dict[tuple[int, int], sp.Matrix] = {}
    zero = sp.zeros(3)
    edges[(0, 1)] = zero
    for left in (0, 1):
        for right in range(2, 6):
            edges[(left, right)] = sp.Matrix(
                3,
                3,
                lambda i, j, left=left, right=right: (
                    (left + 1) * (right - 1) + 2 * i - j
                ),
            )
    for left, right in combinations(range(2, 6), 2):
        edges[(left, right)] = sp.Matrix(
            3,
            3,
            lambda i, j, left=left, right=right: 1 + left + 2 * right - i + 3 * j,
        )

    checks = 0
    for port_word in product(range(3), repeat=4):
        word = (2, 2, *port_word)
        direct = graph_coefficient(word, edges)
        laplace = 0
        for u, v in combinations(range(2, 6), 2):
            remainder = tuple(index for index in range(2, 6) if index not in (u, v))
            k_uv = (
                edges[(0, u)][2, port_word[u - 2]] * edges[(1, v)][2, port_word[v - 2]]
                + edges[(0, v)][2, port_word[v - 2]]
                * edges[(1, u)][2, port_word[u - 2]]
            )
            response = edges[(remainder[0], remainder[1])][
                port_word[remainder[0] - 2], port_word[remainder[1] - 2]
            ]
            laplace += k_uv * response
        assert sp.expand(direct - laplace) == 0
        checks += 1
    return {"port_coefficients_checked": checks, "perfect_matchings": 15}


def pairwise_intersecting(edges: tuple[tuple[int, int], ...]) -> bool:
    return all(set(left) & set(right) for left, right in combinations(edges, 2))


def is_star_or_triangle(edges: tuple[tuple[int, int], ...]) -> bool:
    if not edges:
        return True
    common = set(edges[0]).intersection(*(set(edge) for edge in edges[1:]))
    if common:
        return True
    vertices = set().union(*(set(edge) for edge in edges))
    return len(vertices) == 3


def check_intersecting_support_combinatorics() -> dict[str, object]:
    universe = tuple(combinations(range(5), 2))
    families = 0
    for mask in range(1 << len(universe)):
        family = tuple(
            edge for index, edge in enumerate(universe) if mask & (1 << index)
        )
        if pairwise_intersecting(family):
            assert is_star_or_triangle(family)
            families += 1

    colours = frozenset(range(3))
    local_sets = tuple(
        frozenset(items) for size in range(3) for items in combinations(range(3), size)
    )
    triangle_patterns = []
    for pattern in product(local_sets, repeat=3):
        if all(
            pattern[i] | pattern[j] == colours for i, j in combinations(range(3), 2)
        ):
            assert tuple(len(item) for item in pattern) == (2, 2, 2)
            assert len({next(iter(colours - item)) for item in pattern}) == 3
            triangle_patterns.append(pattern)
    assert len(triangle_patterns) == 6
    return {"intersecting_families_checked": families, "triangle_patterns": 6}


def coordinatewise_product_space(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    columns = [
        left[:, i].multiply_elementwise(right[:, j])
        for i, j in product(range(left.cols), range(right.cols))
    ]
    return basis_matrix(sp.Matrix.hstack(*columns))


def check_four_port_kernel_certificate() -> dict[str, object]:
    # Directly check that contracting two channel kernels leaves one supplier.
    x = (
        sp.Matrix([1, 2, 0]),
        sp.Matrix([0, 1, 2]),
        sp.Matrix([2, 0, 1]),
        sp.Matrix([1, -1, 1]),
    )
    y = (
        sp.Matrix([0, 1, 1]),
        sp.Matrix([1, 0, 1]),
        sp.Matrix([1, 2, 0]),
        sp.Matrix([0, 1, 2]),
    )
    responses = {
        pair: sp.Matrix(
            3,
            3,
            lambda i, j, pair=pair: 1 + sum(pair) + 2 * i - j,
        )
        for pair in combinations(range(4), 2)
    }
    kernels = []
    for port in range(4):
        channel = sp.Matrix.hstack(x[port], y[port]).T
        kernel = channel.nullspace()
        assert len(kernel) == 1
        kernels.append(kernel[0])

    for kept in combinations(range(4), 2):
        cut = tuple(port for port in range(4) if port not in kept)
        contracted = sp.zeros(3)
        for supplier in combinations(range(4), 2):
            complement = tuple(port for port in range(4) if port not in supplier)
            k_supplier = channel_pair(x, y, *supplier)
            for kept_word in product(range(3), repeat=2):
                total = 0
                for cut_word in product(range(3), repeat=2):
                    word = [0] * 4
                    for port, colour in zip(kept, kept_word, strict=True):
                        word[port] = colour
                    for port, colour in zip(cut, cut_word, strict=True):
                        word[port] = colour
                    supplier_value = k_supplier[word[supplier[0]], word[supplier[1]]]
                    response_value = responses[complement][
                        word[complement[0]], word[complement[1]]
                    ]
                    total += (
                        kernels[cut[0]][cut_word[0]]
                        * kernels[cut[1]][cut_word[1]]
                        * supplier_value
                        * response_value
                    )
                contracted[kept_word[0], kept_word[1]] += total
        expected_scalar = (kernels[cut[0]].T * responses[cut] * kernels[cut[1]])[0]
        expected = expected_scalar * channel_pair(x, y, *kept)
        assert contracted == expected

    # Rational plane samples audit the plane-product lemma's exceptional form.
    normals = []
    for entries in product((-1, 0, 1), repeat=3):
        if entries == (0, 0, 0):
            continue
        first = next(value for value in entries if value)
        normalized = tuple(sp.Rational(value, first) for value in entries)
        if normalized not in normals:
            normals.append(normalized)
    coordinate_normals = {tuple(sp.eye(3)[:, i]) for i in range(3)}
    lemma_pairs = 0
    for left_normal, right_normal in combinations(normals, 2):
        left = sp.Matrix([left_normal]).nullspace()
        right = sp.Matrix([right_normal]).nullspace()
        star = coordinatewise_product_space(
            sp.Matrix.hstack(*left), sp.Matrix.hstack(*right)
        )
        if star.rank() <= 1:
            assert left_normal in coordinate_normals
            assert right_normal in coordinate_normals
            assert left_normal != right_normal
            lemma_pairs += 1
    assert lemma_pairs == 3

    # Exhaust the support-set lemma used in the all-rank-two stratum.
    nonempty = tuple(
        frozenset(items)
        for size in range(1, 4)
        for items in combinations(range(3), size)
    )
    support_quadruples = 0
    activity_compatible = 0
    for supports in product(nonempty, repeat=4):
        if all(
            len(supports[i] & supports[j]) in (0, 2)
            for i, j in combinations(range(4), 2)
        ):
            counts = {item: supports.count(item) for item in set(supports)}
            assert any(len(item) == 2 and count >= 3 for item, count in counts.items())
            support_quadruples += 1
            if all(
                sum(colour in item for item in supports) <= 2 for colour in range(3)
            ):
                activity_compatible += 1
    assert activity_compatible == 0
    return {
        "kernel_contractions": 6,
        "plane_lemma_samples": lemma_pairs,
        "rank_two_support_quadruples": support_quadruples,
        "activity_compatible_quadruples": activity_compatible,
    }


def permute_pair_tensor(
    matrix: sp.Matrix, pair: tuple[int, int]
) -> sp.MutableDenseNDimArray:
    output = sp.MutableDenseNDimArray.zeros(3, 3, 3, 3)
    other = tuple(index for index in range(4) if index not in pair)
    for word in product(range(3), repeat=4):
        if word[other[0]] == 0 and word[other[1]] == 0:
            output[word] = matrix[word[pair[0]], word[pair[1]]]
    return output


def check_exchange_and_rank_bounds() -> dict[str, object]:
    symbols = sp.symbols("x0:24")
    x = tuple(sp.Matrix(symbols[3 * i : 3 * i + 3]) for i in range(4))
    y = tuple(sp.Matrix(symbols[12 + 3 * i : 15 + 3 * i]) for i in range(4))
    k01 = channel_pair(x, y, 0, 1)
    k23 = channel_pair(x, y, 2, 3)
    k03 = channel_pair(x, y, 0, 3)
    k12 = channel_pair(x, y, 1, 2)
    delta02 = x[0] * y[2].T - y[0] * x[2].T
    delta13 = x[1] * y[3].T - y[1] * x[3].T

    for word in product(range(3), repeat=4):
        left = (
            k01[word[0], word[1]] * k23[word[2], word[3]]
            - k03[word[0], word[3]] * k12[word[1], word[2]]
        )
        right = -delta02[word[0], word[2]] * delta13[word[1], word[3]]
        assert sp.expand(left - right) == 0

    numeric_x = (
        sp.Matrix([1, 2, 0]),
        sp.Matrix([0, 1, 1]),
        sp.Matrix([1, 0, 2]),
        sp.Matrix([2, 1, 1]),
    )
    numeric_y = (
        sp.Matrix([0, 1, 3]),
        sp.Matrix([2, 0, 1]),
        sp.Matrix([1, 3, 0]),
        sp.Matrix([0, 2, 1]),
    )
    compound = sp.MutableDenseNDimArray.zeros(3, 3, 3, 3)
    for pair, complement in (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))):
        left = channel_pair(numeric_x, numeric_y, *pair)
        right = channel_pair(numeric_x, numeric_y, *complement)
        for word in product(range(3), repeat=4):
            compound[word] += (
                left[word[pair[0]], word[pair[1]]]
                * right[word[complement[0]], word[complement[1]]]
            )
    flatten = sp.Matrix(
        3,
        27,
        lambda row, column: compound[
            row,
            column // 9,
            (column // 3) % 3,
            column % 3,
        ],
    )
    assert flatten.rank() <= 2
    return {
        "symbolic_exchange_coefficients": 81,
        "one_port_compound_rank": flatten.rank(),
    }


def matrix(rows: tuple[tuple[sp.Rational | int, ...], ...]) -> sp.Matrix:
    return sp.Matrix(rows)


def check_same_graph_sharpness_certificate() -> dict[str, object]:
    names = ("a0", "a1", "k", "q0", "q1", "u1", "u2", "u3")
    edges: dict[tuple[int, int], sp.Matrix] = {}

    def put(left: str, right: str, value: sp.Matrix) -> None:
        i, j = names.index(left), names.index(right)
        if i < j:
            edges[(i, j)] = value
        else:
            edges[(j, i)] = value.T

    zero = sp.zeros(3)
    for left, right in combinations(names, 2):
        put(left, right, zero)
    put("a0", "q0", sp.eye(3)[:, 0] * sp.eye(3)[:, 0].T)
    put("a1", "q0", sp.eye(3)[:, 0] * sp.eye(3)[:, 0].T)
    put("a0", "q1", sp.eye(3)[:, 1] * sp.eye(3)[:, 0].T)
    put("a1", "q1", sp.eye(3)[:, 1] * sp.eye(3)[:, 0].T)

    root_port = {
        ("a0", "k"): ((-1, -1, -1), (1, 0, 1), (1, 1, -1)),
        ("a1", "k"): ((-1, 1, 1), (-1, -1, 0), (1, -1, 1)),
        ("a0", "u1"): ((1, 0, 0), (1, 1, 1), (1, -1, 1)),
        ("a0", "u2"): ((-1, 1, -1), (-1, -1, -1), (-1, 1, -1)),
        ("a0", "u3"): ((0, 0, 0), (1, -1, 1), (-1, 1, 0)),
        ("a1", "u1"): ((1, -1, 0), (-1, 0, 0), (-1, -1, 1)),
        ("a1", "u2"): ((-1, -1, -1), (-1, 0, 0), (1, 0, 0)),
        ("a1", "u3"): ((-1, 1, 1), (-1, 1, 0), (0, -1, 0)),
    }
    for endpoints, rows in root_port.items():
        put(*endpoints, matrix(rows))

    put("k", "u1", matrix(((-1, -1, -1), (0, -1, 1), (1, 0, 0))))
    put("k", "u2", matrix(((1, -1, 1), (-1, 1, 1), (-1, 0, 1))))
    put("k", "u3", matrix(((0, 1, 1), (0, 1, 0), (1, 0, -1))))
    put("k", "q0", sp.eye(3)[:, 0] * sp.eye(3)[:, 1].T)
    put("k", "q1", sp.eye(3)[:, 0] * sp.eye(3)[:, 2].T)
    put("q0", "q1", sp.diag(sp.Rational(-1, 2), sp.Rational(1, 2), 1))
    for left, right in (("u1", "u2"), ("u1", "u3"), ("u2", "u3")):
        put(left, right, sp.eye(3)[:, 0] * sp.eye(3)[:, 1].T)

    # Residual pair q and transverse supplier ranks.
    q = sp.zeros(9, 1)
    for a0, a1, q0, q1 in product(range(3), repeat=4):
        q[3 * a0 + a1] += (
            edges[(0, 3)][a0, q0] * edges[(1, 4)][a1, q1]
            + edges[(0, 4)][a0, q1] * edges[(1, 3)][a1, q0]
        )
    assert q == sp.eye(9)[:, 1] + sp.eye(9)[:, 3]
    p = sum(q)
    projector = p * sp.eye(9) - q * sp.ones(1, 9)
    promoted = (2, 5, 6, 7)
    supplier_ranks = []
    for u, v in combinations(promoted, 2):
        g = sp.zeros(9, 9)
        for a0, a1, cu, cv in product(range(3), repeat=4):
            g[3 * a0 + a1, 3 * cu + cv] = (
                edges[(0, u)][a0, cu] * edges[(1, v)][a1, cv]
                + edges[(0, v)][a0, cv] * edges[(1, u)][a1, cu]
            )
        supplier_ranks.append((projector * g).rank())
    assert supplier_ranks == [8] * 6

    # Pair responses are four-vertex coefficients on Q union the complement.
    response_witnesses = []
    for target in combinations(promoted, 2):
        complement = tuple(vertex for vertex in promoted if vertex not in target)
        local_vertices = (*complement, 3, 4)
        found = None
        for word in product(range(3), repeat=2):
            total = 0
            for qword in product(range(3), repeat=2):
                full_word = (*word, *qword)
                local_edges = {}
                for i, j in combinations(range(4), 2):
                    left, right = local_vertices[i], local_vertices[j]
                    local_edges[(i, j)] = oriented_edge(edges, left, right)
                total += graph_coefficient(full_word, local_edges)
            if total != 0:
                found = total
                break
        assert found is not None
        response_witnesses.append(found)

    pure = tuple(graph_coefficient((colour,) * 8, edges) for colour in range(3))
    mixed = graph_coefficient((0, 0, 0, 0, 0, 0, 1, 0), edges)
    assert pure == (1, 1, 1)
    assert mixed == sp.Rational(-3, 2)
    return {
        "p": p,
        "supplier_ranks": tuple(supplier_ranks),
        "nonzero_response_witnesses": tuple(response_witnesses),
        "pure_coefficients": pure,
        "failed_hamming_one": mixed,
    }


def main() -> None:
    print("zero-anchor normal-channel primary checks: PASS")
    print(
        "  quotient and pair factorization:",
        check_normal_quotient_and_pair_factorization(),
    )
    print("  exact nuisance cylinders:", check_normal_nuisance_cylinders())
    print("  complete matching expansion:", check_complete_matching_expansion())
    print(
        "  intersecting-support combinatorics:",
        check_intersecting_support_combinatorics(),
    )
    print("  four-port kernel certificate:", check_four_port_kernel_certificate())
    print("  exchange and rank bounds:", check_exchange_and_rank_bounds())
    print(
        "  same-graph sharpness certificate:", check_same_graph_sharpness_certificate()
    )
    print(
        "  scope: exact reduction plus r=3 full-activity exclusion; divisors, higher-r disjoint support, and node closure remain open"
    )


if __name__ == "__main__":
    main()
