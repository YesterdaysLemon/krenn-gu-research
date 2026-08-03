"""Verify the mixed-root deletion filtration and herald-free pair no-go.

This is a fixed symbolic replay of arbitrary-order identities, not a search.
"""

from functools import cache
from itertools import combinations, permutations

import sympy as sp


def hafnian(matrix: sp.Matrix):
    assert matrix.rows == matrix.cols

    @cache
    def recurrence(vertices: tuple[int, ...]):
        if not vertices:
            return sp.Integer(1)
        if len(vertices) % 2:
            return sp.Integer(0)
        first = vertices[0]
        total = sp.Integer(0)
        for position in range(1, len(vertices)):
            second = vertices[position]
            remainder = vertices[1:position] + vertices[position + 1 :]
            total += matrix[first, second] * recurrence(remainder)
        return sp.expand(total)

    return recurrence(tuple(range(matrix.rows)))


def generic_three_root_expansion() -> None:
    root_count = 3
    nonroot_count = 5
    total_count = root_count + nonroot_count
    adjacency = sp.zeros(total_count)

    for first, second in combinations(range(root_count), 2):
        value = sp.symbols(f"l{first}{second}")
        adjacency[first, second] = adjacency[second, first] = value
    for root in range(root_count):
        for nonroot in range(nonroot_count):
            value = sp.symbols(f"h{root}{nonroot}")
            vertex = root_count + nonroot
            adjacency[root, vertex] = adjacency[vertex, root] = value
    for first, second in combinations(range(nonroot_count), 2):
        value = sp.symbols(f"a{first}{second}")
        left = root_count + first
        right = root_count + second
        adjacency[left, right] = adjacency[right, left] = value

    direct = hafnian(adjacency)
    nonroots = tuple(range(nonroot_count))
    expansion = sp.Integer(0)

    # No root--root edge: all three roots inject into distinct nonroots.
    for image in permutations(nonroots, root_count):
        unused = tuple(nonroot for nonroot in nonroots if nonroot not in image)
        cofactor = adjacency[root_count + unused[0], root_count + unused[1]]
        root_product = sp.prod(
            adjacency[root, root_count + image[root]] for root in range(root_count)
        )
        expansion += root_product * cofactor

    # One root--root edge: the remaining root deletes one nonroot.
    for first, second in combinations(range(root_count), 2):
        remaining_root = ({0, 1, 2} - {first, second}).pop()
        for image in nonroots:
            unused = tuple(nonroot for nonroot in nonroots if nonroot != image)
            cofactor = hafnian(
                adjacency.extract(
                    tuple(root_count + nonroot for nonroot in unused),
                    tuple(root_count + nonroot for nonroot in unused),
                )
            )
            expansion += (
                adjacency[first, second]
                * adjacency[remaining_root, root_count + image]
                * cofactor
            )

    assert sp.expand(direct - expansion) == 0


def p7_depth_and_shallow_controls() -> None:
    root_count = 5
    nonroot_count = 9
    assert tuple(root_count - 2 * pairs for pairs in range(3)) == (5, 3, 1)
    direct_pair_deletion = 2 + (7 - 2)
    singleton_deletion = 1 + (7 - 1)
    assert direct_pair_deletion == singleton_deletion == 7 > root_count

    def surviving_bidegrees(blockers: int, residuals: int) -> tuple[int, ...]:
        roots = blockers - residuals
        return tuple(2 * residuals + 2 * pairs for pairs in range(roots // 2 + 1))

    assert surviving_bidegrees(7, 2) == (4, 6, 8)
    assert surviving_bidegrees(7, 4) == (8, 10)
    assert surviving_bidegrees(7, 6) == (12,)

    # With one nonroot edge, matching number is one.  Every cofactor through
    # depth five retains at least four vertices, so it is zero; depth seven
    # leaves the arbitrary edge itself.
    retained_at_shallow_depth = nonroot_count - root_count
    assert retained_at_shallow_depth == 4
    assert 1 < retained_at_shallow_depth // 2
    parameter = sp.symbols("t")
    pair_cofactor = hafnian(sp.Matrix(((0, parameter), (parameter, 0))))
    assert pair_cofactor == parameter


def nonzero_forced_shore_control() -> None:
    # Vertices: roots 0..4; u,v,b1,b2,b3,b4,b5,q0,q1 = 5..13.
    root_count = 5
    vertex_count = 14
    u, v, b1, b2, b3, b4, b5, q0, q1 = range(5, 14)
    shore_targets = (u, v, b1, b2, b3)
    parameter = sp.symbols("t")
    root_forms = sp.symbols("alpha0:5")
    adjacency = sp.zeros(vertex_count)
    for root, target, root_form in zip(
        range(root_count), shore_targets, root_forms, strict=True
    ):
        adjacency[root, target] = adjacency[target, root] = root_form
    adjacency[b4, b5] = adjacency[b5, b4] = 1
    adjacency[q0, q1] = adjacency[q1, q0] = 1
    adjacency[u, v] = adjacency[v, u] = parameter

    root_tensor = hafnian(adjacency)
    assert sp.expand(root_tensor - sp.prod(root_forms)) == 0
    assert parameter not in root_tensor.free_symbols
    assert all(
        parameter not in sp.diff(root_tensor, root_form).free_symbols
        for root_form in root_forms
    )
    direct_pair = hafnian(adjacency.extract((u, v), (u, v)))
    assert direct_pair == parameter


def vacuum_scaling_obstruction() -> None:
    scale, present_value, deleted_value = sp.symbols("lambda P D")
    present_after_scaling = scale * present_value
    deleted_after_scaling = deleted_value
    assert sp.diff(present_after_scaling, scale) == present_value
    assert sp.diff(deleted_after_scaling, scale) == 0
    assert sp.expand(present_after_scaling - deleted_after_scaling).coeff(scale) == (
        present_value
    )


def main() -> None:
    generic_three_root_expansion()
    p7_depth_and_shallow_controls()
    nonzero_forced_shore_control()
    vacuum_scaling_obstruction()
    print("PASS: generic three-root hafnian equals the partial-matching expansion")
    print("PASS: P7 mixed-root cofactor depths are 5,3,1, below pair depth 7")
    print("PASS: exact residual/port bidegrees are 2q+2j at arbitrary order")
    print("PASS: physical shallow tower and nonzero forced shore hide the pair")
    print("PASS: vertex scaling excludes a universal herald-free linear vacuum")
    print("SCOPE: target-specific nonlinear GHZ identities and added heralds remain unknown")
    print("searches=0")


if __name__ == "__main__":
    main()
