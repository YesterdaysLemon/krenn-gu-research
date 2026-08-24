"""Independent no-import audit of the product-selector interface correction.

This audit uses bitmask hafnian recursion and sparse evaluated edge tables.  It
does not import the primary replay or any project implementation.
"""

from __future__ import annotations

from functools import cache
from itertools import combinations, product

ROOTS = (0, 1, 2, 3)
Q = (4, 5)
PORTS = (6, 7, 8, 9)
OUTSIDE = Q + PORTS


# Evaluated at rho=(x0,x1,x2,y3).  Entries involving a port include its colour.
ROOT_EDGE = {(2, 3): 1}
ROOT_OUTSIDE = {
    (0, 4, None): 1,
    (1, 5, None): 1,
    **{(2, port, 0): 1 for port in PORTS},
}

PORT_EDGE_COLOUR = {
    (6, 7): 0,
    (8, 9): 0,
    (6, 8): 1,
    (7, 9): 1,
    (6, 9): 2,
    (7, 8): 2,
}


def pair(left: int, right: int) -> tuple[int, int]:
    return (left, right) if left < right else (right, left)


def scalar_weight(
    left: int,
    right: int,
    colours: dict[int, int],
    *,
    allow_outside=True,
) -> int:
    left, right = pair(left, right)
    if left in ROOTS and right in ROOTS:
        return ROOT_EDGE.get((left, right), 0)
    if left in ROOTS:
        colour = colours.get(right) if right in PORTS else None
        return ROOT_OUTSIDE.get((left, right, colour), 0)
    if not allow_outside:
        return 0
    if left in PORTS and right in PORTS:
        required = PORT_EDGE_COLOUR[(left, right)]
        return int(colours[left] == colours[right] == required)
    # The remaining outside blocks are nonzero colour-zero monomials.
    left_ok = left not in PORTS or colours[left] == 0
    right_ok = right not in PORTS or colours[right] == 0
    return int(left_ok and right_ok)


def hafnian(
    vertices: tuple[int, ...],
    colours: dict[int, int],
    *,
    allow_outside=True,
) -> int:
    @cache
    def visit(mask: int) -> int:
        if mask == 0:
            return 1
        first_bit = mask & -mask
        first_index = first_bit.bit_length() - 1
        first = vertices[first_index]
        remaining = mask ^ first_bit
        total = 0
        cursor = remaining
        while cursor:
            second_bit = cursor & -cursor
            second_index = second_bit.bit_length() - 1
            second = vertices[second_index]
            total += scalar_weight(
                first,
                second,
                colours,
                allow_outside=allow_outside,
            ) * visit(remaining ^ second_bit)
            cursor ^= second_bit
        return total

    return visit((1 << len(vertices)) - 1)


def assignments(vertices: tuple[int, ...]):
    ports = tuple(vertex for vertex in vertices if vertex in PORTS)
    for values in product(range(3), repeat=len(ports)):
        yield dict(zip(ports, values, strict=True))


def audit_companion_table() -> int:
    checked = 0
    for size in (0, 2, 4):
        for subset in combinations(OUTSIDE, size):
            for colours in assignments(subset):
                value = hafnian(ROOTS + subset, colours, allow_outside=False)
                assert value == int(subset == Q), (subset, colours, value)
                checked += 1
    return checked


def audit_response() -> None:
    found = {}
    for colours in assignments(PORTS):
        word = tuple(colours[port] for port in PORTS)
        value = hafnian(PORTS, colours)
        if value:
            found[word] = value
    assert found == {
        (0, 0, 0, 0): 1,
        (1, 1, 1, 1): 1,
        (2, 2, 2, 2): 1,
    }


def audit_separation() -> None:
    colours = {6: 0, 7: 0}
    vertices = ROOTS + Q + (6, 7)
    root_only = hafnian(vertices, colours, allow_outside=False)
    full = hafnian(vertices, colours, allow_outside=True)
    anchor = hafnian(ROOTS + Q, {}, allow_outside=True)
    direct = scalar_weight(6, 7, colours)
    assert (root_only, direct * anchor, full) == (0, 1, 1)


def audit_maximum_root_argument() -> None:
    # The sole root edge evaluates to zero at the maximum vectors, rather than
    # the rho-evaluation stored in ROOT_EDGE.  Each outside has one fixed
    # nonzero coordinate-monomial root incidence, and all outside pairs are
    # nonzero coordinate monomials, so at most one outside can enter a torus
    # zero set and it displaces at least one root.
    designated = {4: 0, 5: 1, 6: 2, 7: 2, 8: 2, 9: 2}
    assert len(designated) == len(OUTSIDE)
    assert all(
        ROOT_OUTSIDE[(root, outside, 0 if outside in PORTS else None)]
        for outside, root in designated.items()
    )


def main() -> None:
    checked = audit_companion_table()
    audit_response()
    audit_separation()
    audit_maximum_root_argument()
    print("independent product-selector interface audit: PASS")
    print(f"  bitmask companion entries: {checked}")


if __name__ == "__main__":
    main()
