"""Primary exact replay for the GLD65 product-selector exclusion.

The proof has three finite interfaces:

1. the eight-vertex matching expansion that turns a product four-port
   selector into one common four-dimensional cross-Gram form for the six
   direct port blocks;
2. the complete support classification of diagonal pair blocks whose
   four-port compound is pure with three nonzero colours; and
3. the five-vector dimension obstruction for the resulting one-factorization
   support.

The arbitrary-field implications are proved in the accompanying theorem.
"""

from __future__ import annotations

from itertools import combinations

from sympy import Symbol, expand

ROOTS = tuple(f"r{i}" for i in range(4))
OUTSIDE = ("q0", "q1", "u", "v")
ALL_VERTICES = ROOTS + OUTSIDE
COLOURS = range(3)
PORTS = range(4)
EDGES = tuple(combinations(PORTS, 2))
COMPLEMENTS = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))


def edge(left: str, right: str) -> tuple[str, str]:
    return tuple(sorted((left, right)))


def perfect_matchings(vertices: tuple[str, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        remaining = vertices[1:index] + vertices[index + 1 :]
        for rest in perfect_matchings(remaining):
            yield (edge(first, second),) + rest


WEIGHTS = {
    edge(left, right): Symbol(f"w_{left}_{right}")
    for left, right in combinations(ALL_VERTICES, 2)
}


def matching_polynomial(vertices: tuple[str, ...]):
    return sum(
        __import__("math").prod(WEIGHTS[pair] for pair in matching)
        for matching in perfect_matchings(vertices)
    )


def no_outside_edge_polynomial(vertices: tuple[str, ...]):
    return sum(
        __import__("math").prod(WEIGHTS[pair] for pair in matching)
        for matching in perfect_matchings(vertices)
        if not any(pair[0] in OUTSIDE and pair[1] in OUTSIDE for pair in matching)
    )


def check_matching_expansion() -> dict[int, int]:
    """Audit the 105-term expansion by its number of outside edges."""

    matchings = tuple(perfect_matchings(ALL_VERTICES))
    assert len(matchings) == 105
    counts = {0: 0, 1: 0, 2: 0}
    one_edge_counts = {edge(left, right): 0 for left, right in combinations(OUTSIDE, 2)}
    zero_edge_terms = set()
    for matching in matchings:
        outside_edges = tuple(
            pair for pair in matching if pair[0] in OUTSIDE and pair[1] in OUTSIDE
        )
        counts[len(outside_edges)] += 1
        if len(outside_edges) == 1:
            one_edge_counts[outside_edges[0]] += 1
        if not outside_edges:
            assignment = tuple(
                sorted(
                    (root, outside)
                    for pair in matching
                    for root, outside in (pair, pair[::-1])
                    if root in ROOTS and outside in OUTSIDE
                )
            )
            zero_edge_terms.add(assignment)

    assert counts == {0: 24, 1: 72, 2: 9}
    assert set(one_edge_counts.values()) == {12}
    assert len(zero_edge_terms) == 24

    # Exact generic polynomial identity, before imposing any selector
    # equation.  If F_D is the matching polynomial on roots union D, then
    # F_OUT = sum_e B_e F_(OUT-e) - H C(B_OUT) + R_OUT.
    full = matching_polynomial(ALL_VERTICES)
    root_hafnian = matching_polynomial(ROOTS)
    root_bijection = no_outside_edge_polynomial(ALL_VERTICES)
    outside_compound = sum(
        WEIGHTS[edge(*first)] * WEIGHTS[edge(*second)]
        for first, second in (
            (("q0", "q1"), ("u", "v")),
            (("q0", "u"), ("q1", "v")),
            (("q0", "v"), ("q1", "u")),
        )
    )
    pair_sum = 0
    for left, right in combinations(OUTSIDE, 2):
        complement = tuple(vertex for vertex in OUTSIDE if vertex not in (left, right))
        pair_sum += WEIGHTS[edge(left, right)] * matching_polynomial(ROOTS + complement)
    assert (
        expand(full - (pair_sum - root_hafnian * outside_compound + root_bijection))
        == 0
    )

    # With H=F_empty=0, each two-outside coefficient is its root-only
    # 12-term part.  A pure-M U selector makes F_Q=m and every other
    # two-outside coefficient zero.  Therefore the 72 one-outside-edge
    # terms retain exactly B_uv * m, while the 24 zero-edge terms are the
    # common four-linear form J(l_u,l_v).
    q_edge = edge("q0", "q1")
    uv_edge = edge("u", "v")
    surviving_one_edge = {
        outside_edge
        for outside_edge in one_edge_counts
        if set(OUTSIDE) - set(outside_edge) == set(q_edge)
    }
    assert surviving_one_edge == {uv_edge}
    return counts


def bit(mask: int, pair: tuple[int, int], colour: int) -> bool:
    return bool(mask & (1 << (3 * EDGES.index(pair) + colour)))


def mixed_support_zero(mask: int) -> bool:
    return all(
        not (bit(mask, first, colour) and bit(mask, second, other))
        for first, second in COMPLEMENTS
        for colour in COLOURS
        for other in COLOURS
        if colour != other
    )


def every_pure_colour_active(mask: int) -> bool:
    return all(
        any(
            bit(mask, first, colour) and bit(mask, second, colour)
            for first, second in COMPLEMENTS
        )
        for colour in COLOURS
    )


def matching_colour(mask: int, pair_index: int) -> int | None:
    first, second = COMPLEMENTS[pair_index]
    common = [
        colour
        for colour in COLOURS
        if bit(mask, first, colour) and bit(mask, second, colour)
    ]
    return common[0] if len(common) == 1 else None


def check_support_classification() -> tuple[int, tuple[tuple[int, int, int], ...]]:
    valid = []
    for mask in range(1 << (3 * len(EDGES))):
        if not mixed_support_zero(mask) or not every_pure_colour_active(mask):
            continue
        colours = tuple(matching_colour(mask, index) for index in range(3))
        assert None not in colours
        assert set(colours) == set(COLOURS)
        for index, colour in enumerate(colours):
            first, second = COMPLEMENTS[index]
            assert all(bit(mask, pair, colour) for pair in (first, second))
            assert all(
                not bit(mask, pair, other)
                for pair in (first, second)
                for other in COLOURS
                if other != colour
            )
        valid.append(colours)
    assert len(valid) == 6
    assert len(set(valid)) == 6
    return len(valid), tuple(valid)


def standard_colour(first: int, second: int) -> int:
    pair = tuple(sorted((first, second)))
    for colour, matching in enumerate(COMPLEMENTS):
        if pair in matching:
            return colour
    raise AssertionError(pair)


def cross_pairing(left: tuple[int, int], right: tuple[int, int]) -> bool:
    """Whether the prescribed camouflage cross pairing is nonzero."""

    port_left, colour_left = left
    port_right, colour_right = right
    if port_left == port_right:
        raise ValueError("within-port pairings are deliberately unspecified")
    return colour_left == colour_right == standard_colour(port_left, port_right)


def check_five_vector_obstruction() -> int:
    checks = 0
    for base_port in PORTS:
        for neighbour in PORTS:
            if neighbour == base_port:
                continue
            edge_colour = standard_colour(base_port, neighbour)
            off_colours = tuple(colour for colour in COLOURS if colour != edge_colour)
            relation_vectors = (
                *((base_port, colour) for colour in COLOURS),
                *((neighbour, colour) for colour in off_colours),
            )
            assert len(relation_vectors) == 5

            isolated = []
            base_off_vectors = tuple(
                (base_port, colour) for colour in COLOURS if colour != edge_colour
            )
            neighbour_off_vectors = tuple((neighbour, colour) for colour in off_colours)
            for vector in base_off_vectors + neighbour_off_vectors:
                port, colour = vector
                partner = next(
                    (other, colour)
                    for other in PORTS
                    if other != port and standard_colour(port, other) == colour
                )
                pattern = tuple(
                    cross_pairing(candidate, partner) for candidate in relation_vectors
                )
                assert sum(pattern) == 1
                assert pattern[relation_vectors.index(vector)]
                isolated.append(vector)

            assert len(set(isolated)) == 4
            remaining = (base_port, edge_colour)
            partner = (neighbour, edge_colour)
            assert cross_pairing(remaining, partner)
            checks += 1
    assert checks == 12
    return checks


def main() -> None:
    matching_counts = check_matching_expansion()
    support_count, support_profiles = check_support_classification()
    dimension_checks = check_five_vector_obstruction()
    print("GLD65 primary exact replay: PASS")
    print("  exact generic matching identity and outside-edge counts:", matching_counts)
    print("  exhaustive diagonal pure-three support profiles:", support_count)
    print("  matching-colour permutations:", support_profiles)
    print("  five-vector dimension certificates:", dimension_checks)
    print("  scope: product four-port selector and pure-three M response only")
    print("  global Krenn-Gu status: UNRESOLVED")


if __name__ == "__main__":
    main()
