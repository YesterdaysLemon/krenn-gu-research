"""Independent no-import audit of the minimal pure-cofactor core theorem."""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from itertools import combinations
from math import gcd

Edge = tuple[int, int]

VERTEX_COUNT = 8
EDGES = tuple(combinations(range(VERTEX_COUNT), 2))
EDGE_INDEX = {item: index for index, item in enumerate(EDGES)}
EDGE_ENDPOINT_MASK = tuple((1 << left) | (1 << right) for left, right in EDGES)


@lru_cache(maxsize=None)
def matching_masks(vertices: int) -> tuple[int, ...]:
    """Enumerate perfect matchings as edge-bit masks."""
    if not vertices:
        return (0,)
    first_bit = vertices & -vertices
    first = first_bit.bit_length() - 1
    remainder = vertices ^ first_bit
    partners = remainder
    records = []
    while partners:
        partner_bit = partners & -partners
        partner = partner_bit.bit_length() - 1
        partners ^= partner_bit
        item = (first, partner)
        item_bit = 1 << EDGE_INDEX[item]
        for matching in matching_masks(remainder ^ partner_bit):
            records.append(item_bit | matching)
    return tuple(records)


def encoded_weights(records: dict[Edge, Fraction]) -> tuple[Fraction, ...]:
    """Encode sparse edge weights in the fixed edge order."""
    return tuple(records.get(item, Fraction(0)) for item in EDGES)


def matching_weight(matching: int, weights: tuple[Fraction, ...]) -> Fraction:
    """Multiply the selected edge weights."""
    result = Fraction(1)
    bits = matching
    while bits:
        low = bits & -bits
        index = low.bit_length() - 1
        result *= weights[index]
        bits ^= low
    return result


def supported_matchings(vertices: int, weights: tuple[Fraction, ...]) -> tuple[int, ...]:
    """Return all nonzero matching terms."""
    return tuple(
        matching
        for matching in matching_masks(vertices)
        if matching_weight(matching, weights)
    )


def hafnian(vertices: int, weights: tuple[Fraction, ...]) -> Fraction:
    """Evaluate a principal hafnian from bitmask matchings."""
    return sum(
        (matching_weight(matching, weights) for matching in matching_masks(vertices)),
        Fraction(0),
    )


def minimal_cancellation(vertices: int, weights: tuple[Fraction, ...]) -> int:
    """Find a least supported cancelling even vertex mask."""
    available = tuple(index for index in range(VERTEX_COUNT) if vertices & (1 << index))
    for size in range(2, len(available) + 1, 2):
        for subset in combinations(available, size):
            mask = sum(1 << vertex for vertex in subset)
            if supported_matchings(mask, weights) and hafnian(mask, weights) == 0:
                return mask
    raise AssertionError("no supported cancellation")


def allowed_mask(vertices: int, weights: tuple[Fraction, ...]) -> int:
    """Return the union of all supported perfect matchings."""
    result = 0
    for matching in supported_matchings(vertices, weights):
        result |= matching
    return result


def flow(vertices: int, weights: tuple[Fraction, ...]) -> dict[int, Fraction]:
    """Compute nonzero edge-cofactor flow in edge-index coordinates."""
    result = {}
    for index, endpoint_mask in enumerate(EDGE_ENDPOINT_MASK):
        if endpoint_mask & vertices != endpoint_mask or not weights[index]:
            continue
        value = weights[index] * hafnian(vertices ^ endpoint_mask, weights)
        if value:
            result[index] = value
    return result


def graph_components(vertices: int, edge_mask: int) -> tuple[int, ...]:
    """Return connected-component vertex masks."""
    unseen = vertices
    records = []
    while unseen:
        start = unseen & -unseen
        seen = start
        changed = True
        while changed:
            changed = False
            for index, endpoint_mask in enumerate(EDGE_ENDPOINT_MASK):
                if not edge_mask & (1 << index) or not endpoint_mask & seen:
                    continue
                expanded = seen | endpoint_mask
                if expanded != seen:
                    seen = expanded
                    changed = True
        unseen &= ~seen
        records.append(seen)
    return tuple(records)


def incidence_rank(vertices: int, edge_mask: int) -> int:
    """Compute exact rank of the unsigned vertex-edge incidence matrix."""
    vertex_list = [index for index in range(VERTEX_COUNT) if vertices & (1 << index)]
    edge_list = [index for index in range(len(EDGES)) if edge_mask & (1 << index)]
    matrix = [
        [Fraction(int(vertex in EDGES[index])) for index in edge_list]
        for vertex in vertex_list
    ]
    pivot_row = 0
    for column in range(len(edge_list)):
        pivot = next(
            (row for row in range(pivot_row, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = matrix[pivot_row][column]
        matrix[pivot_row] = [value / scale for value in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                value - factor * pivot_value
                for value, pivot_value in zip(matrix[row], matrix[pivot_row], strict=True)
            ]
        pivot_row += 1
    return pivot_row


def row_sums(vertices: int, values: dict[int, Fraction]) -> tuple[Fraction, ...]:
    """Return cofactor-flow row sums."""
    return tuple(
        sum(
            (value for index, value in values.items() if vertex in EDGES[index]),
            Fraction(0),
        )
        for vertex in range(VERTEX_COUNT)
        if vertices & (1 << vertex)
    )


def audit_eight_cycle() -> dict[str, object]:
    """Audit a rational eight-cycle with one structurally inactive chord."""
    vertices = (1 << 8) - 1
    weights = encoded_weights(
        {
            (0, 1): Fraction(2),
            (1, 2): Fraction(11),
            (2, 3): Fraction(3),
            (3, 4): Fraction(13),
            (4, 5): Fraction(5),
            (5, 6): Fraction(17),
            (6, 7): Fraction(7),
            (0, 7): Fraction(-210, 2431),
            (0, 2): Fraction(19),
        }
    )
    assert hafnian(vertices, weights) == 0
    assert minimal_cancellation(vertices, weights) == vertices
    matchings = supported_matchings(vertices, weights)
    assert len(matchings) == 2
    assert {matching_weight(item, weights) for item in matchings} == {Fraction(-210), Fraction(210)}

    allowed = allowed_mask(vertices, weights)
    active = sum(1 << index for index in flow(vertices, weights))
    chord_bit = 1 << EDGE_INDEX[(0, 2)]
    support = sum(1 << index for index, value in enumerate(weights) if value)
    assert allowed == active == support ^ chord_bit
    assert graph_components(vertices, active) == (vertices,)
    assert row_sums(vertices, flow(vertices, weights)) == (Fraction(0),) * 8
    assert incidence_rank(vertices, active) == 7

    unique_cofactors = 0
    for index in range(len(EDGES)):
        if not active & (1 << index):
            continue
        complement = vertices ^ EDGE_ENDPOINT_MASK[index]
        assert len(supported_matchings(complement, weights)) == 1
        unique_cofactors += 1
    chord_complement = vertices ^ EDGE_ENDPOINT_MASK[EDGE_INDEX[(0, 2)]]
    assert not supported_matchings(chord_complement, weights)

    relation = []
    for index in range(len(EDGES)):
        coefficient = int(bool(matchings[0] & (1 << index))) - int(
            bool(matchings[1] & (1 << index))
        )
        if coefficient:
            relation.append(coefficient)
    assert gcd(*[abs(value) for value in relation]) == 1

    return {
        "cycle_length": 8,
        "matching_products": (-210, 210),
        "inactive_chord": (0, 2),
        "unique_first_cofactors": unique_cofactors,
        "unsigned_incidence_rank": 7,
        "primitive_relation": True,
    }


def audit_branching_core() -> dict[str, object]:
    """Audit a differently weighted K4 branching core."""
    vertices = (1 << 4) - 1
    weights = encoded_weights(
        {
            (0, 1): Fraction(2),
            (2, 3): Fraction(3),
            (0, 2): Fraction(5),
            (1, 3): Fraction(7),
            (0, 3): Fraction(1),
            (1, 2): Fraction(-41),
        }
    )
    assert hafnian(vertices, weights) == 6 + 35 - 41 == 0
    assert minimal_cancellation(vertices, weights) == vertices
    matchings = supported_matchings(vertices, weights)
    assert len(matchings) == 3
    allowed = allowed_mask(vertices, weights)
    active = sum(1 << index for index in flow(vertices, weights))
    assert active == allowed
    assert active.bit_count() == 6
    assert graph_components(vertices, active) == (vertices,)
    assert row_sums(vertices, flow(vertices, weights)) == (Fraction(0),) * 4
    assert incidence_rank(vertices, active) == 4
    beta = active.bit_count() - vertices.bit_count() + 1
    assert beta == 3
    return {
        "matching_products": (6, 35, -41),
        "perfect_matchings": len(matchings),
        "cyclomatic_rank": beta,
        "unsigned_flow_kernel_dimension": active.bit_count() - 4,
    }


def audit_minimal_component_selection() -> dict[str, object]:
    """Audit a disconnected nonminimal zero before least-residual selection."""
    vertices = (1 << 6) - 1
    weights = encoded_weights(
        {
            (0, 1): Fraction(5),
            (0, 2): Fraction(7),
            (1, 3): Fraction(-5),
            (2, 3): Fraction(7),
            (4, 5): Fraction(11),
        }
    )
    assert hafnian(vertices, weights) == 0
    allowed = allowed_mask(vertices, weights)
    pieces = graph_components(vertices, allowed)
    assert pieces == ((1 << 4) - 1, (1 << 4) | (1 << 5))
    factors = tuple(hafnian(piece, weights) for piece in pieces)
    assert factors == (0, 11)
    assert hafnian(vertices, weights) == factors[0] * factors[1]
    selected = minimal_cancellation(vertices, weights)
    assert selected == pieces[0]
    selected_allowed = allowed_mask(selected, weights)
    assert graph_components(selected, selected_allowed) == (selected,)
    return {
        "preminimal_components": len(pieces),
        "factor_hafnians": factors,
        "least_residual_vertices": selected.bit_count(),
    }


def main() -> None:
    """Run the independent exact audit."""
    cycle = audit_eight_cycle()
    branch = audit_branching_core()
    minimality = audit_minimal_component_selection()
    print("minimal pure-cofactor matching-covered core no-import audit: PASS")
    print(f"  independent primitive cycle: {cycle}")
    print(f"  independent branching core: {branch}")
    print(f"  independent component selection: {minimality}")


if __name__ == "__main__":
    main()
