"""Independent no-import audit of aggregate active-cycle defects."""

from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations
from math import comb, prod

Edge = tuple[int, int]
Matching = frozenset[Edge]
Word = tuple[int, ...]
Entry = tuple[int, int, Fraction]
Table = dict[Edge, Entry]

WORDS: tuple[Word, ...] = (
    (0, 0, 0, 0, 1, 1, 1, 1),
    (0, 0, 1, 1, 0, 0, 1, 1),
    (0, 1, 0, 1, 0, 1, 0, 1),
)

CROSS: tuple[tuple[Edge, ...], ...] = (
    ((2, 4), (3, 5)),
    ((1, 2), (5, 6)),
    ((1, 4), (3, 6)),
)

BRIDGES: tuple[tuple[Edge, ...], ...] = (
    ((2, 3), (4, 5)),
    ((1, 5), (2, 6)),
    ((4, 6), (1, 3)),
)

RESIDUAL: tuple[tuple[Edge, ...], ...] = (
    ((0, 1), (6, 7)),
    ((0, 4), (3, 7)),
    ((0, 2), (5, 7)),
)


def build_fraction_table(parameter: Fraction) -> tuple[Table, Fraction]:
    """Build the sharpness table directly at one exact rational parameter."""

    selected_weight = -(1 + 2 * parameter) / 2
    assert parameter and selected_weight
    table: Table = {}
    cross_weights = (
        (selected_weight, Fraction(1)),
        (Fraction(-1), Fraction(1)),
        (Fraction(-1), Fraction(1)),
    )
    for index, old_word in enumerate(WORDS):
        new_word = WORDS[(index + 1) % 3]
        for position, item in enumerate(CROSS[index]):
            table[item] = old_word[item[0]], old_word[item[1]], cross_weights[index][position]
        for item in BRIDGES[index]:
            table[item] = new_word[item[0]], new_word[item[1]], Fraction(1)
        for item in RESIDUAL[index]:
            table[item] = old_word[item[0]], old_word[item[1]], Fraction(1)

    table.update(
        {
            (0, 3): (0, 0, Fraction(1)),
            (1, 6): (0, 1, Fraction(1)),
            (2, 5): (0, 1, Fraction(1)),
            (4, 7): (1, 1, parameter),
            (0, 5): (1, 2, Fraction(1)),
            (0, 6): (2, 2, Fraction(1)),
            (0, 7): (1, 0, Fraction(1)),
            (1, 7): (2, 2, Fraction(1)),
            (2, 7): (2, 0, Fraction(1)),
            (3, 4): (2, 2, Fraction(1)),
        }
    )
    assert len(table) == 28
    return table, selected_weight


def disjoint_edge_census(table: Table) -> dict[Word, list[tuple[Matching, Fraction]]]:
    """Enumerate all full matchings by four-edge mask combinations."""

    fibres: dict[Word, list[tuple[Matching, Fraction]]] = defaultdict(list)
    for selected in combinations(tuple(table), 4):
        vertex_mask = 0
        valid = True
        for left, right in selected:
            pair_mask = (1 << left) | (1 << right)
            if vertex_mask & pair_mask:
                valid = False
                break
            vertex_mask |= pair_mask
        if not valid or vertex_mask != 255:
            continue

        word = [-1] * 8
        value = Fraction(1)
        for item in selected:
            left_label, right_label, weight = table[item]
            word[item[0]] = left_label
            word[item[1]] = right_label
            value *= weight
        fibres[tuple(word)].append((frozenset(selected), value))
    return fibres


def product_weight(edges: tuple[Edge, ...], table: Table) -> Fraction:
    """Return an exact edge-product weight."""

    return prod(table[item][2] for item in edges)


def character(matching: Matching, table: Table) -> Counter[tuple[int, int]]:
    """Return the endpoint-label incidence character."""

    result: Counter[tuple[int, int]] = Counter()
    for left, right in matching:
        left_label, right_label, _ = table[(left, right)]
        result[(left, left_label)] += 1
        result[(right, right_label)] += 1
    return result


def scaled_table(table: Table) -> Table:
    """Apply a deterministic exact endpoint-coordinate gauge."""

    beta = {
        (vertex, colour): vertex - 2 * colour + ((vertex + colour) % 3)
        for vertex in range(8)
        for colour in range(3)
    }

    def power_of_two(exponent: int) -> Fraction:
        if exponent >= 0:
            return Fraction(2**exponent)
        return Fraction(1, 2 ** (-exponent))

    result = {}
    for item, (left_label, right_label, weight) in table.items():
        exponent = beta[(item[0], left_label)] + beta[(item[1], right_label)]
        result[item] = left_label, right_label, weight * power_of_two(exponent)
    return result


def cycle_quantities(
    table: Table, fibres: dict[Word, list[tuple[Matching, Fraction]]]
) -> tuple[Fraction, Fraction, tuple[int, int, int]]:
    """Compute selected holonomy, first defect, and fibre sizes."""

    full_cross = tuple(tuple(sorted(CROSS[i] + RESIDUAL[i])) for i in range(3))
    full_bridge = tuple(tuple(sorted(BRIDGES[i] + RESIDUAL[i])) for i in range(3))
    incoming = frozenset(full_bridge[2])
    outgoing = frozenset(full_cross[0])
    extras = [record for record in fibres[WORDS[0]] if record[0] not in {incoming, outgoing}]

    outgoing_weight = product_weight(full_cross[0], table)
    defect = sum((value for _, value in extras), Fraction(0)) / outgoing_weight
    holonomy = prod(product_weight(item, table) for item in full_bridge) / prod(
        product_weight(item, table) for item in full_cross
    )
    assert holonomy == -1 * (1 + defect)
    assert all(character(matching, table) == character(outgoing, table) for matching, _ in extras)
    return holonomy, defect, tuple(len(fibres[word]) for word in WORDS)


def audit_exact_specializations() -> list[dict[str, object]]:
    """Audit split, nonsplit, and additional rational members independently."""

    summaries = []
    for parameter in (Fraction(1, 2), Fraction(1), Fraction(2), Fraction(-1)):
        table, selected_weight = build_fraction_table(parameter)
        assert all(entry[2] for entry in table.values())
        local_labels = {
            vertex: {
                entry[0] if item[0] == vertex else entry[1]
                for item, entry in table.items()
                if vertex in item
            }
            for vertex in range(8)
        }
        assert all(labels == {0, 1, 2} for labels in local_labels.values())

        fibres = disjoint_edge_census(table)
        holonomy, defect, sizes = cycle_quantities(table, fibres)
        assert sizes == (5, 2, 2)
        assert all(sum((value for _, value in fibres[word]), Fraction(0)) == 0 for word in WORDS)
        assert holonomy == Fraction(-2, 1 + 2 * parameter)
        assert not fibres.get((0,) * 8)
        assert not fibres.get((1,) * 8)
        assert not fibres.get((2,) * 8)

        gauged = scaled_table(table)
        gauged_fibres = disjoint_edge_census(gauged)
        gauged_holonomy, gauged_defect, gauged_sizes = cycle_quantities(gauged, gauged_fibres)
        assert gauged_sizes == sizes
        assert gauged_holonomy == holonomy
        assert gauged_defect == defect

        if parameter == Fraction(1, 2):
            extra_values = sorted(
                value
                for matching, value in fibres[WORDS[0]]
                if matching
                not in {
                    frozenset(BRIDGES[2] + RESIDUAL[2]),
                    frozenset(CROSS[0] + RESIDUAL[0]),
                }
            )
            assert extra_values == [Fraction(-1), Fraction(1, 2), Fraction(1, 2)]
            assert defect == 0 and holonomy == -1
        if parameter == 1:
            assert selected_weight == Fraction(-3, 2)
            assert defect == Fraction(-1, 3)
            assert holonomy == Fraction(-2, 3)

        summaries.append(
            {
                "t": parameter,
                "x": selected_weight,
                "sizes": sizes,
                "defect": defect,
                "holonomy": holonomy,
                "gauge_invariant": True,
            }
        )
    return summaries


def rational_rank(matrix: list[list[Fraction]]) -> int:
    """Compute row rank by exact elimination."""

    work = [row[:] for row in matrix]
    rows = len(work)
    columns = len(work[0]) if work else 0
    pivot_row = 0
    for column in range(columns):
        pivot = next((row for row in range(pivot_row, rows) if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [value / scale for value in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                value - factor * pivot_value
                for value, pivot_value in zip(work[row], work[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def audit_holonomy_substitution_injectivity(max_degree: int = 10) -> dict[str, object]:
    """Audit p(H)->p(-2/(1+2t)) by a triangular coefficient matrix."""

    ranks = []
    for degree in range(max_degree + 1):
        matrix = []
        for power_t in range(degree + 1):
            row = []
            for power_h in range(degree + 1):
                residual_degree = degree - power_h
                coefficient = Fraction(0)
                if power_t <= residual_degree:
                    coefficient = Fraction(
                        (-2) ** power_h
                        * comb(residual_degree, power_t)
                        * 2**power_t
                    )
                row.append(coefficient)
            matrix.append(row)
        rank = rational_rank(matrix)
        assert rank == degree + 1
        ranks.append(rank)
    return {
        "degrees": tuple(range(max_degree + 1)),
        "ranks": tuple(ranks),
        "triangular_injective": True,
    }


def main() -> None:
    specializations = audit_exact_specializations()
    injectivity = audit_holonomy_substitution_injectivity()
    print("independent aggregate-cycle specializations:", specializations)
    print("independent holonomy substitution audit:", injectivity)
    print("aggregate active-cycle defect factorisation no-import audit: PASS")


if __name__ == "__main__":
    main()
