"""Independent exact audit of the two-depth interference boundary.

This file imports neither SymPy nor the primary verifier.  It uses only
standard-library exact arithmetic.  The physical controls are evaluated by a
bitmask enumeration of perfect matchings on the actual six vertices, while
the corrected-compound check uses sparse four-port words and independent row
reduction.

The finite rational replays below are not proofs over an arbitrary field and
do not supply a synchronized target window from a hypothetical witness.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from functools import cache
from itertools import combinations, product

Q = Fraction
Vector = tuple[Q, Q, Q]
Matrix = tuple[tuple[Q, Q, Q], tuple[Q, Q, Q], tuple[Q, Q, Q]]
Word = tuple[int, int, int, int]
Edge = tuple[int, int]

PORTS = tuple(range(4))
COLORS = tuple(range(3))
PORT_EDGES = tuple(combinations(PORTS, 2))
PORT_PARTITIONS: tuple[tuple[Edge, Edge], ...] = (
    ((0, 1), (2, 3)),
    ((0, 2), (1, 3)),
    ((0, 3), (1, 2)),
)

# Physical-graph vertex labels.  Port u is represented by vertex u + 2.
Q0 = 0
Q1 = 1


def qvector(values: tuple[int | Q, int | Q, int | Q]) -> Vector:
    return tuple(Q(value) for value in values)  # type: ignore[return-value]


def zero_matrix() -> Matrix:
    return tuple(tuple(Q(0) for _ in COLORS) for _ in COLORS)  # type: ignore[return-value]


def diagonal_matrix(values: tuple[int | Q, int | Q, int | Q]) -> Matrix:
    return tuple(
        tuple(Q(values[i]) if i == j else Q(0) for j in COLORS) for i in COLORS
    )  # type: ignore[return-value]


def add_matrix(left: Matrix, right: Matrix) -> Matrix:
    return tuple(tuple(left[i][j] + right[i][j] for j in COLORS) for i in COLORS)  # type: ignore[return-value]


def scale_matrix(scalar: Q, matrix: Matrix) -> Matrix:
    return tuple(tuple(scalar * matrix[i][j] for j in COLORS) for i in COLORS)  # type: ignore[return-value]


def outer(left: Vector, right: Vector) -> Matrix:
    return tuple(tuple(left[i] * right[j] for j in COLORS) for i in COLORS)  # type: ignore[return-value]


def corrected_blocks(
    a: tuple[Vector, ...], b: tuple[Vector, ...]
) -> dict[Edge, Matrix]:
    return {
        edge: add_matrix(outer(a[edge[0]], b[edge[1]]), outer(b[edge[0]], a[edge[1]]))
        for edge in PORT_EDGES
    }


@cache
def bitmask_matchings(mask: int) -> tuple[tuple[Edge, ...], ...]:
    """Enumerate perfect matchings by deleting two bits at a time."""

    if mask == 0:
        return ((),)
    if mask.bit_count() % 2:
        return ()
    anchor_bit = mask & -mask
    anchor = anchor_bit.bit_length() - 1
    remainder = mask ^ anchor_bit
    matchings: list[tuple[Edge, ...]] = []
    cursor = remainder
    while cursor:
        partner_bit = cursor & -cursor
        partner = partner_bit.bit_length() - 1
        smaller = remainder ^ partner_bit
        for tail in bitmask_matchings(smaller):
            matchings.append((((anchor, partner)), *tail))
        cursor ^= partner_bit
    return tuple(matchings)


def physical_response(
    selected_ports: tuple[int, ...],
    word: tuple[int, ...],
    h: Q,
    a: tuple[Vector, ...],
    b: tuple[Vector, ...],
    direct: dict[Edge, Matrix],
) -> Q:
    """Evaluate one contracted response directly on the physical graph."""

    assert len(selected_ports) == len(word)
    port_colors = dict(zip(selected_ports, word, strict=True))
    active_vertices = (1 << Q0) | (1 << Q1)
    for port in selected_ports:
        active_vertices |= 1 << (port + 2)

    def edge_value(i: int, j: int) -> Q:
        if (i, j) == (Q0, Q1):
            return h
        if i == Q0:
            port = j - 2
            return a[port][port_colors[port]]
        if i == Q1:
            port = j - 2
            return b[port][port_colors[port]]
        left = i - 2
        right = j - 2
        return direct[left, right][port_colors[left]][port_colors[right]]

    total = Q(0)
    for matching in bitmask_matchings(active_vertices):
        term = Q(1)
        for i, j in matching:
            term *= edge_value(i, j)
        total += term
    return total


def sparse_compound(blocks: dict[Edge, Matrix]) -> dict[Word, Q]:
    """Build C(blocks) by sparse products on the three port partitions."""

    result: defaultdict[Word, Q] = defaultdict(Q)
    for first, second in PORT_PARTITIONS:
        i, j = first
        k, ell = second
        for ci, cj, ck, cell in product(COLORS, repeat=4):
            coefficient = blocks[first][ci][cj] * blocks[second][ck][cell]
            if coefficient:
                word_list = [0, 0, 0, 0]
                word_list[i] = ci
                word_list[j] = cj
                word_list[k] = ck
                word_list[ell] = cell
                result[tuple(word_list)] += coefficient  # type: ignore[index]
    return {word: value for word, value in result.items() if value}


def sparse_assignment_compound(
    a: tuple[Vector, ...], b: tuple[Vector, ...]
) -> dict[Word, Q]:
    """Build the six-term assignment expansion without pair blocks."""

    result: dict[Word, Q] = {}
    for word in product(COLORS, repeat=4):
        value = Q(0)
        for a_ports_tuple in combinations(PORTS, 2):
            a_ports = frozenset(a_ports_tuple)
            term = Q(2)
            for port, color in enumerate(word):
                term *= a[port][color] if port in a_ports else b[port][color]
            value += term
        if value:
            result[word] = value
    return result


def row_rank(matrix: tuple[tuple[Q, ...], ...]) -> int:
    rows = [list(row) for row in matrix]
    if not rows:
        return 0
    rank = 0
    for column in range(len(rows[0])):
        pivot = next((r for r in range(rank, len(rows)) if rows[r][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        pivot_value = rows[rank][column]
        rows[rank] = [value / pivot_value for value in rows[rank]]
        for r, row in enumerate(rows):
            if r == rank or not row[column]:
                continue
            multiplier = row[column]
            rows[r] = [
                value - multiplier * pivot_entry
                for value, pivot_entry in zip(row, rows[rank], strict=True)
            ]
        rank += 1
        if rank == len(rows):
            break
    return rank


def flatten(tensor: dict[Word, Q], mode: int) -> tuple[tuple[Q, ...], ...]:
    other_modes = tuple(port for port in PORTS if port != mode)
    columns = tuple(product(COLORS, repeat=3))
    rows: list[tuple[Q, ...]] = []
    for row_color in COLORS:
        row: list[Q] = []
        for column in columns:
            word_list = [0, 0, 0, 0]
            word_list[mode] = row_color
            for port, color in zip(other_modes, column, strict=True):
                word_list[port] = color
            row.append(tensor.get(tuple(word_list), Q(0)))  # type: ignore[arg-type]
        rows.append(tuple(row))
    return tuple(rows)


def audit_interference_on_exact_physical_graph() -> None:
    """Replay hT=C(D)-C(K) on a nondegenerate rational six-vertex graph."""

    h = Q(-2, 3)
    a = tuple(
        qvector(values) for values in ((1, 2, 0), (1, 0, 1), (2, -1, 1), (1, 1, -1))
    )
    b = tuple(
        qvector(values) for values in ((0, 1, 1), (1, -1, 0), (1, 2, 0), (0, 1, 2))
    )
    direct: dict[Edge, Matrix] = {}
    for i, j in PORT_EDGES:
        direct[i, j] = tuple(
            tuple(Q((i + 2) * (r + 1) - (j + 1) * (c - 1), r + c + 2) for c in COLORS)
            for r in COLORS
        )  # type: ignore[assignment]

    k_blocks = corrected_blocks(a, b)
    d_blocks = {
        edge: add_matrix(scale_matrix(h, direct[edge]), k_blocks[edge])
        for edge in PORT_EDGES
    }
    c_d = sparse_compound(d_blocks)
    c_k = sparse_compound(k_blocks)

    assert len(bitmask_matchings((1 << 6) - 1)) == 15
    for edge in PORT_EDGES:
        assert (
            len(
                bitmask_matchings(
                    (1 << Q0) | (1 << Q1) | (1 << (edge[0] + 2)) | (1 << (edge[1] + 2))
                )
            )
            == 3
        )
        for colors in product(COLORS, repeat=2):
            observed = physical_response(edge, colors, h, a, b, direct)
            assert observed == d_blocks[edge][colors[0]][colors[1]]

    for word in product(COLORS, repeat=4):
        response = physical_response(PORTS, word, h, a, b, direct)
        assert h * response == c_d.get(word, Q(0)) - c_k.get(word, Q(0))


def audit_corrected_compound_by_sparse_words() -> None:
    """Derive the compound separately from assignments and audit row ranks."""

    # Count abstract a/b assignments before substituting any coordinates.
    assignment_counts: Counter[tuple[str, str, str, str]] = Counter()
    for first, second in PORT_PARTITIONS:
        for first_orientation, second_orientation in product((0, 1), repeat=2):
            labels = ["", "", "", ""]
            for edge, orientation in (
                (first, first_orientation),
                (second, second_orientation),
            ):
                labels[edge[orientation]] = "a"
                labels[edge[1 - orientation]] = "b"
            assignment_counts[tuple(labels)] += 1  # type: ignore[arg-type]
    expected_assignments = {
        tuple("a" if port in a_ports else "b" for port in PORTS)
        for a_ports in map(frozenset, combinations(PORTS, 2))
    }
    assert set(assignment_counts) == expected_assignments
    assert set(assignment_counts.values()) == {2}

    a = tuple(
        qvector(values) for values in ((1, 2, 0), (1, 0, 1), (2, -1, 1), (1, 1, -1))
    )
    b = tuple(
        qvector(values) for values in ((0, 1, 1), (1, -1, 0), (1, 2, 0), (0, 1, 2))
    )
    paired = sparse_compound(corrected_blocks(a, b))
    assigned = sparse_assignment_compound(a, b)
    assert paired == assigned
    assert len(paired) > 0
    for mode in PORTS:
        assert row_rank(flatten(paired, mode)) == 2


def equal_colour_partitions(word: Word) -> tuple[tuple[Edge, Edge], ...]:
    return tuple(
        partition
        for partition in PORT_PARTITIONS
        if all(word[i] == word[j] for edge in partition for i, j in (edge,))
    )


def canonical_partition(first: Edge, second: Edge) -> frozenset[Edge]:
    return frozenset((tuple(sorted(first)), tuple(sorted(second))))


def audit_all_216_grid_supports() -> None:
    """Exhaust the structural support calculation for one fixed port."""

    fixed_port = 0
    other_ports = tuple(port for port in PORTS if port != fixed_port)
    choices = {
        color: tuple(
            (partner, delta)
            for partner in other_ports
            for delta in COLORS
            if delta != color
        )
        for color in COLORS
    }
    checked_grids = 0
    checked_mixed_entries = 0
    for witnesses in product(*(choices[color] for color in COLORS)):
        columns: dict[int, tuple[int, int, int]] = {}
        expected_partitions: dict[int, frozenset[Edge]] = {}
        for color, (partner, delta) in zip(COLORS, witnesses, strict=True):
            columns[color] = tuple(
                color if port == partner else delta for port in other_ports
            )
            complement = tuple(
                port for port in PORTS if port not in (fixed_port, partner)
            )
            expected_partitions[color] = canonical_partition(
                (fixed_port, partner), (complement[0], complement[1])
            )
        assert len(set(columns.values())) == 3

        for row_color in COLORS:
            for column_color in COLORS:
                word_list = [0, 0, 0, 0]
                word_list[fixed_port] = row_color
                for port, color in zip(other_ports, columns[column_color], strict=True):
                    word_list[port] = color
                word = tuple(word_list)  # type: ignore[assignment]
                assert len(set(word)) > 1
                support = equal_colour_partitions(word)
                if row_color == column_color:
                    assert len(support) == 1
                    assert (
                        canonical_partition(*support[0])
                        == expected_partitions[column_color]
                    )
                else:
                    assert support == ()
                checked_mixed_entries += 1
        checked_grids += 1

    assert checked_grids == 216
    assert checked_mixed_entries == 216 * 9


def camouflage_frames(sign: int) -> tuple[tuple[Vector, ...], tuple[Vector, ...]]:
    e0 = qvector((1, 0, 0))
    e1 = qvector((0, 1, 0))
    a = (e0, e0, e1, e1)
    b = (e1, e1, e0, e0)
    return tuple(tuple(Q(sign) * value for value in row) for row in a), b  # type: ignore[return-value]


def camouflage_diagonals() -> dict[Edge, Matrix]:
    return {
        (0, 1): diagonal_matrix((0, 0, 1)),
        (2, 3): diagonal_matrix((0, 0, 1)),
        (0, 2): diagonal_matrix((1, 1, 0)),
        (1, 3): diagonal_matrix((2, 2, 0)),
        (0, 3): diagonal_matrix((1, Q(2, 3), 0)),
        (1, 2): diagonal_matrix((3, 2, 0)),
    }


def active_colors(diagonals: dict[Edge, Matrix], fixed_port: int) -> set[int]:
    active: set[int] = set()
    for color in COLORS:
        for partner in PORTS:
            if partner == fixed_port:
                continue
            edge = tuple(sorted((fixed_port, partner)))
            complement = tuple(port for port in PORTS if port not in edge)
            other_edge = tuple(sorted(complement))
            edge_value = diagonals[edge][color][color]
            if any(
                edge_value * diagonals[other_edge][delta][delta]
                for delta in COLORS
                if delta != color
            ):
                active.add(color)
    return active


def audit_six_vertex_camouflage() -> None:
    """Replay both inequivalent rational channels on all target words."""

    diagonals = camouflage_diagonals()
    channels: list[tuple[dict[Edge, Matrix], dict[Word, Q]]] = []
    for sign in (1, -1):
        a, b = camouflage_frames(sign)
        assert all(row_rank((a[port], b[port])) == 2 for port in PORTS)
        k_blocks = corrected_blocks(a, b)
        direct = {
            edge: add_matrix(diagonals[edge], scale_matrix(Q(-1), k_blocks[edge]))
            for edge in PORT_EDGES
        }

        pair_coefficients_checked = 0
        for edge in PORT_EDGES:
            for colors in product(COLORS, repeat=2):
                observed = physical_response(edge, colors, Q(1), a, b, direct)
                expected = diagonals[edge][colors[0]][colors[1]]
                assert observed == expected
                if colors[0] != colors[1]:
                    assert observed == 0
                pair_coefficients_checked += 1
        assert pair_coefficients_checked == 54

        response = {
            word: physical_response(PORTS, word, Q(1), a, b, direct)
            for word in product(COLORS, repeat=4)
        }
        pure = (Q(3), Q(4, 3), Q(1))
        assert tuple(response[(color,) * 4] for color in COLORS) == pure
        mixed_words = tuple(word for word in response if len(set(word)) > 1)
        assert len(mixed_words) == 78
        assert all(response[word] == 0 for word in mixed_words)

        c_d = sparse_compound(diagonals)
        c_k = sparse_compound(k_blocks)
        assert all(
            response[word] == c_d.get(word, Q(0)) - c_k.get(word, Q(0))
            for word in response
        )
        assert k_blocks[(0, 1)][0][1] == sign
        assert k_blocks[(2, 3)][1][0] == sign
        channels.append((k_blocks, response))

    assert channels[0][1] == channels[1][1]
    assert channels[0][0] != channels[1][0]
    for fixed_port in PORTS:
        assert active_colors(diagonals, fixed_port) == {0, 1}


def audit_zero_h_deck_ambiguity() -> None:
    """Replay two different direct decks with identical h=0 target data."""

    a_row = qvector((1, 1, 0))
    b_row = qvector((1, -1, 0))
    a = (a_row,) * 4
    b = (b_row,) * 4
    assert all(row_rank((a[port], b[port])) == 2 for port in PORTS)
    k_blocks = corrected_blocks(a, b)
    expected_k = diagonal_matrix((2, -2, 0))
    assert all(block == expected_k for block in k_blocks.values())

    zero_deck = {edge: zero_matrix() for edge in PORT_EDGES}
    signed_deck = dict(zero_deck)
    signed_deck[(0, 1)] = expected_k
    signed_deck[(2, 3)] = scale_matrix(Q(-1), expected_k)
    assert signed_deck != zero_deck
    assert sparse_compound(zero_deck) == {}
    assert sparse_compound(signed_deck).get((0, 0, 0, 0)) == -4

    pair_checks = 0
    for edge in PORT_EDGES:
        for colors in product(COLORS, repeat=2):
            first = physical_response(edge, colors, Q(0), a, b, zero_deck)
            second = physical_response(edge, colors, Q(0), a, b, signed_deck)
            assert first == second == expected_k[colors[0]][colors[1]]
            pair_checks += 1
    assert pair_checks == 54

    for word in product(COLORS, repeat=4):
        first = physical_response(PORTS, word, Q(0), a, b, zero_deck)
        second = physical_response(PORTS, word, Q(0), a, b, signed_deck)
        assert first == second == 0


def main() -> None:
    audit_interference_on_exact_physical_graph()
    audit_corrected_compound_by_sparse_words()
    audit_all_216_grid_supports()
    audit_six_vertex_camouflage()
    audit_zero_h_deck_ambiguity()
    print("independent two-residual pair/four-port boundary audit: PASS")


if __name__ == "__main__":
    main()
