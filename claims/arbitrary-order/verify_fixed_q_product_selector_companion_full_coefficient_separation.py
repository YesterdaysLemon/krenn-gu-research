"""Primary exact replay for the product-selector interface correction.

The replay builds one physical ternary graph, evaluates the complete GLD15
four-port companion table, and separates the root companion G_D from the full
matching coefficient F_D used incorrectly by GLD65/GLD66.
"""

from __future__ import annotations

from itertools import combinations, permutations, product
from math import prod

ROOTS = tuple(f"r{i}" for i in range(4))
Q = ("q0", "q1")
PORTS = tuple(f"u{i}" for i in range(4))
OUTSIDE = Q + PORTS
COLOURS = range(3)

X = (1, 1, 1)
Y = (1, 0, 0)
Z = (1, 1, 1)
RHO = {root: (Y if root == "r3" else X) for root in ROOTS}

E0 = (1, 0, 0)
E1 = (0, 1, 0)
E2 = (0, 0, 1)
ALPHA = (1, -1, 0)
ZERO = tuple(tuple(0 for _ in COLOURS) for _ in COLOURS)


def edge(left: str, right: str) -> tuple[str, str]:
    return tuple(sorted((left, right)))


def matchings(vertices: tuple[str, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        remaining = vertices[1:index] + vertices[index + 1 :]
        for rest in matchings(remaining):
            yield (edge(first, second),) + rest


def outer(left: tuple[int, ...], right: tuple[int, ...]):
    return tuple(tuple(a * b for b in right) for a in left)


def transpose(matrix):
    return tuple(tuple(row) for row in zip(*matrix, strict=True))


BLOCKS = {}


def put(left: str, right: str, matrix) -> None:
    if left < right:
        BLOCKS[(left, right)] = matrix
    else:
        BLOCKS[(right, left)] = transpose(matrix)


# The only root--root block vanishes at X tensor X but is one at X tensor Y.
put("r2", "r3", outer(E0, ALPHA))

# Residual anchors and one common isotropic port-incidence line.
put("r0", "q0", outer(E0, E0))
put("r1", "q1", outer(E0, E0))
for port in PORTS:
    put("r2", port, outer(E0, E0))

# The three complementary port matchings carry the three pure colours.
for left, right, colour in (
    ("u0", "u1", 0),
    ("u2", "u3", 0),
    ("u0", "u2", 1),
    ("u1", "u3", 1),
    ("u0", "u3", 2),
    ("u1", "u2", 2),
):
    basis = (E0, E1, E2)[colour]
    put(left, right, outer(basis, basis))

# Make every remaining outside--outside block a nonzero coordinate monomial.
for left, right in combinations(OUTSIDE, 2):
    if edge(left, right) not in BLOCKS:
        put(left, right, outer(E0, E0))


def block(left: str, right: str):
    if left < right:
        return BLOCKS.get((left, right), ZERO)
    return transpose(BLOCKS.get((right, left), ZERO))


def local_vector(vertex: str, colours: dict[str, int], *, maximum=False):
    if vertex in ROOTS:
        return X if maximum else RHO[vertex]
    if vertex in Q:
        return Z
    return (E0, E1, E2)[colours[vertex]]


def weight(
    left: str,
    right: str,
    colours: dict[str, int],
    *,
    maximum=False,
) -> int:
    matrix = block(left, right)
    left_vector = local_vector(left, colours, maximum=maximum)
    right_vector = local_vector(right, colours, maximum=maximum)
    return sum(
        left_vector[row] * matrix[row][column] * right_vector[column]
        for row in COLOURS
        for column in COLOURS
    )


def coefficient(
    vertices: tuple[str, ...],
    colours: dict[str, int],
    *,
    root_companion=False,
) -> int:
    return sum(
        prod(weight(left, right, colours) for left, right in matching)
        for matching in matchings(vertices)
        if not root_companion
        or all(left in ROOTS or right in ROOTS for left, right in matching)
    )


def colourings(vertices: tuple[str, ...]):
    ports = tuple(vertex for vertex in vertices if vertex in PORTS)
    for values in product(COLOURS, repeat=len(ports)):
        yield dict(zip(ports, values, strict=True))


def check_maximum_root() -> None:
    for left, right in combinations(ROOTS, 2):
        assert weight(left, right, {}, maximum=True) == 0

    named_root = {
        "q0": "r0",
        "q1": "r1",
        "u0": "r2",
        "u1": "r2",
        "u2": "r2",
        "u3": "r2",
    }
    for outside, root in named_root.items():
        colours = {outside: 0} if outside in PORTS else {}
        assert weight(root, outside, colours, maximum=True) == 1
    assert all(block(left, right) != ZERO for left, right in combinations(OUTSIDE, 2))


def check_complete_companion_row() -> int:
    checked = 0
    for size in (0, 2, 4):
        for subset in combinations(OUTSIDE, size):
            for colours in colourings(subset):
                value = coefficient(ROOTS + subset, colours, root_companion=True)
                expected = 1 if subset == Q else 0
                assert value == expected, (subset, colours, value, expected)
                checked += 1
    return checked


def check_direct_response() -> dict[tuple[int, ...], int]:
    nonzero = {}
    for colours in colourings(PORTS):
        word = tuple(colours[port] for port in PORTS)
        value = coefficient(PORTS, colours)
        if value:
            nonzero[word] = value
    expected = {
        (0, 0, 0, 0): 1,
        (1, 1, 1, 1): 1,
        (2, 2, 2, 2): 1,
    }
    assert nonzero == expected
    return nonzero


def check_interface_separation() -> tuple[int, int, int]:
    colours = {"u0": 0, "u1": 0}
    vertices = ROOTS + Q + ("u0", "u1")
    companion = coefficient(vertices, colours, root_companion=True)
    full = coefficient(vertices, colours)
    direct_times_anchor = weight("u0", "u1", colours) * coefficient(ROOTS + Q, {})
    assert companion == 0
    assert direct_times_anchor == full == 1
    return companion, direct_times_anchor, full


def check_not_global_witness() -> int:
    vertices = ROOTS + OUTSIDE
    pure_one = sum(
        prod(block(left, right)[1][1] for left, right in matching)
        for matching in matchings(vertices)
    )
    assert pure_one == 0
    return pure_one


def check_permanent_convention() -> None:
    columns = ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 1, 0))
    permanent = sum(
        prod(columns[column][row] for column, row in enumerate(permutation))
        for permutation in permutations(range(4))
    )
    assert permanent == 0


def main() -> None:
    check_maximum_root()
    checked = check_complete_companion_row()
    response = check_direct_response()
    separation = check_interface_separation()
    pure_one = check_not_global_witness()
    check_permanent_convention()
    print("fixed-Q product-selector companion/full-coefficient correction: PASS")
    print(f"  complete evaluated companion entries: {checked}")
    print(f"  nonzero direct four-port words: {response}")
    print(f"  G_Q01, B_01*G_Q, F_Q01: {separation}")
    print(f"  global all-one coefficient (GHZ target is 1): {pure_one}")


if __name__ == "__main__":
    main()
