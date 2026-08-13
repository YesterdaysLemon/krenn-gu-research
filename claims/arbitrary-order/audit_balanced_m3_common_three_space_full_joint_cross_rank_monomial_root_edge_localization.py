"""Independent stdlib audit of the full-joint-rank monomial-edge theorem."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, permutations, product


def row_rank(rows: list[list[Fraction]]) -> int:
    work = [row[:] for row in rows]
    if not work:
        return 0
    pivot_row = 0
    for col in range(len(work[0])):
        pivot = next(
            (index for index in range(pivot_row, len(work)) if work[index][col]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][col]
        work[pivot_row] = [entry / scale for entry in work[pivot_row]]
        for index, row in enumerate(work):
            if index == pivot_row or not row[col]:
                continue
            multiple = row[col]
            work[index] = [
                left - multiple * right
                for left, right in zip(row, work[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def tensor_index(word: tuple[int, int, int]) -> int:
    return 9 * word[0] + 3 * word[1] + word[2]


def assemble(
    blocks: dict[str, tuple[int, int] | None],
) -> list[list[Fraction]]:
    columns = [[Fraction(0) for _ in range(27)] for _ in range(9)]
    for h in range(3):
        if blocks["23"] is not None:
            b, c = blocks["23"]
            columns[h][tensor_index((h, b, c))] = Fraction(1)
        if blocks["13"] is not None:
            a, c = blocks["13"]
            columns[3 + h][tensor_index((a, h, c))] = Fraction(1)
        if blocks["12"] is not None:
            a, b = blocks["12"]
            columns[6 + h][tensor_index((a, b, h))] = Fraction(1)
    return columns


def audit_root_blocks() -> None:
    slots = ("12", "13", "23")
    ranks: dict[int, int] = {}
    for first, second in combinations(slots, 2):
        for pos_first in product(range(3), repeat=2):
            for pos_second in product(range(3), repeat=2):
                blocks = {slot: None for slot in slots}
                blocks[first] = pos_first
                blocks[second] = pos_second
                rank = row_rank(assemble(blocks))
                assert rank >= 5
                ranks[rank] = ranks.get(rank, 0) + 1
    assert ranks == {5: 81, 6: 162}

    one = {"12": None, "13": None, "23": (2, 0)}
    assert row_rank(assemble(one)) == 3
    print("independent root-block rank census: PASS (3; 81 rank-five; 162 rank-six)")


def audit_torus_cancellation() -> None:
    # Use coefficients 5 and -7 and cancel with a variable belonging only to
    # the first monomial.  This is intentionally distinct from the primary.
    positions = list(product(range(3), repeat=2))
    for first, second in combinations(positions, 2):
        s = [Fraction(1) for _ in range(3)]
        t = [Fraction(1) for _ in range(3)]
        first_variables = ((0, first[0]), (1, first[1]))
        second_variables = {(0, second[0]), (1, second[1])}
        family, index = next(item for item in first_variables if item not in second_variables)
        if family == 0:
            s[index] = Fraction(7, 5)
        else:
            t[index] = Fraction(7, 5)
        value = 5 * s[first[0]] * t[first[1]] - 7 * s[second[0]] * t[second[1]]
        assert value == 0
        assert 0 not in (*s, *t)
    print("independent two-term torus cancellation: PASS (36/36)")


def audit_quotient_support() -> None:
    for p, q in product(range(3), repeat=2):
        quotient_words = [
            word
            for word in product(range(3), repeat=3)
            if (word[1], word[2]) != (p, q)
        ]
        assert len(quotient_words) == 24
        surviving_diagonal = [c for c in range(3) if (c, c) != (p, q)]
        assert len(surviving_diagonal) == (2 if p == q else 3)
    print("independent GHZ quotient support: PASS (9/9)")


def audit_pair_grouping() -> None:
    def entry(i: int, u: int, a: int, c: int) -> Fraction:
        return Fraction(1 + ((29 * i + 19 * u + 7 * a + 5 * c) % 17))

    count = 0
    for a, p, q, x, y, r in product(range(3), repeat=6):
        output = (x, y, r)
        expanded = Fraction(0)
        for matching in permutations(range(3)):
            term = Fraction(1)
            for i, root_colour in enumerate((a, p, q)):
                u = matching[i]
                term *= entry(i, u, root_colour, output[u])
            expanded += term

        grouped = Fraction(0)
        for u in range(3):
            remaining = [value for value in range(3) if value != u]
            v, w = remaining
            pair = (
                entry(1, v, p, output[v]) * entry(2, w, q, output[w])
                + entry(1, w, p, output[w]) * entry(2, v, q, output[v])
            )
            grouped += entry(0, u, a, output[u]) * pair
        assert expanded == grouped
        count += 1
    assert count == 729
    print("independent exceptional-line pair grouping: PASS (729/729)")


def audit_latin_monomial_floor() -> None:
    permutations3 = tuple(permutations(range(3)))
    counts: dict[int, int] = {}
    total = 0
    for first in product(range(4), repeat=3):
        if sum(first) != 3:
            continue
        for second in product(range(4), repeat=3):
            if sum(second) != 3:
                continue
            third = tuple(3 - first[j] - second[j] for j in range(3))
            if min(third) < 0 or sum(third) != 3:
                continue
            matrix = (first, second, third)
            value = sum(
                matrix[0][sigma[0]] * matrix[1][sigma[1]] * matrix[2][sigma[2]]
                for sigma in permutations3
            )
            counts[value] = counts.get(value, 0) + 1
            total += 1
    assert total == 55
    assert min(counts) == 6
    assert counts[6] == 1

    latin = [[Fraction(0) for _ in range(9)] for _ in range(9)]
    for root in range(3):
        for colour in range(3):
            nonroot = (root + colour) % 3
            latin[3 * root + colour][3 * nonroot + colour] = Fraction(1)

    output_rows: list[list[Fraction]] = []
    for colours in product(range(3), repeat=3):
        row: list[Fraction] = []
        for output in product(range(3), repeat=3):
            value = Fraction(0)
            for matching in permutations3:
                term = Fraction(1)
                for root in range(3):
                    column = 3 * matching[root] + output[matching[root]]
                    term *= latin[3 * root + colours[root]][column]
                value += term
            row.append(value)
        output_rows.append(row)
    assert row_rank(output_rows) == 6
    print("independent Latin monomial floor: PASS (55 counts; equality rank 6)")


def main() -> None:
    audit_root_blocks()
    audit_torus_cancellation()
    audit_pair_grouping()
    audit_quotient_support()
    audit_latin_monomial_floor()
    print("independent m=3 full-joint-rank monomial-edge audit: PASS")


if __name__ == "__main__":
    main()
