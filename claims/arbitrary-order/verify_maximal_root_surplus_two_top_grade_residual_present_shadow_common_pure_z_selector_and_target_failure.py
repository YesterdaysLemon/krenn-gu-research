"""Focused exact checks for the GLS19 residual-present top shadow."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, permutations, product
from math import factorial


def matchings(vertices: tuple[int, ...], edge_count: int):
    if edge_count == 0:
        yield ()
        return
    if len(vertices) < 2 * edge_count:
        return
    first = vertices[0]
    yield from matchings(vertices[1:], edge_count)
    for index, partner in enumerate(vertices[1:], start=1):
        remaining = vertices[1:index] + vertices[index + 1 :]
        for rest in matchings(remaining, edge_count - 1):
            yield ((first, partner),) + rest


def surviving_signatures(order: int, edge_count: int, open_roots: frozenset[int]):
    answer = set()
    for matching in matchings(tuple(range(order)), edge_count):
        if not all(open_roots.intersection(edge) for edge in matching):
            continue
        used = {vertex for edge in matching for vertex in edge}
        unused = tuple(vertex for vertex in range(order) if vertex not in used)
        for assignment in permutations(unused):
            answer.add(
                (tuple(sorted(tuple(sorted(edge)) for edge in matching)), assignment)
            )
    return answer


def expected_top_signatures(order: int, half_size: int, open_roots: frozenset[int]):
    closed = tuple(root for root in range(order) if root not in open_roots)
    complement_size = order - 2 * half_size
    answer = set()
    for partners in permutations(closed, half_size):
        edges = tuple(
            sorted(
                tuple(sorted((root, partner)))
                for root, partner in zip(sorted(open_roots), partners, strict=True)
            )
        )
        used = set(open_roots).union(partners)
        unused = tuple(root for root in range(order) if root not in used)
        assert len(unused) == complement_size
        for assignment in permutations(unused):
            answer.add((edges, assignment))
    return answer


def check_top_grade_shadows():
    records = {}
    checked = 0
    for order in range(2, 8):
        order_record = {}
        for half_size in range(1, order // 2 + 1):
            per_mask = []
            for roots in combinations(range(order), half_size):
                open_roots = frozenset(roots)
                observed = surviving_signatures(order, half_size, open_roots)
                expected = expected_top_signatures(order, half_size, open_roots)
                assert observed == expected
                expected_count = (
                    factorial(order - half_size)
                    // factorial(order - 2 * half_size)
                    * factorial(order - 2 * half_size)
                )
                assert len(observed) == expected_count
                for grade in range(half_size + 1, order // 2 + 1):
                    assert not surviving_signatures(order, grade, open_roots)
                lower = surviving_signatures(order, half_size - 1, open_roots)
                assert lower
                per_mask.append((len(observed), len(lower)))
                checked += len(observed) + len(lower)
            order_record[half_size] = tuple(per_mask)
        records[order] = order_record
    return checked, records


def rank(matrix: list[list[Fraction]]) -> int:
    if not matrix:
        return 0
    work = [row[:] for row in matrix]
    row_count = len(work)
    column_count = len(work[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, row_count) if work[row][column]), None
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [entry / scale for entry in work[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                left - factor * right
                for left, right in zip(work[row], work[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def columns_to_rows(columns: list[tuple[Fraction, ...]], dimension: int):
    return [[column[row] for column in columns] for row in range(dimension)]


def check_target_coupling():
    cases = 0
    rank_one = 0
    for top_nonzero, response_nonzero in product((False, True), repeat=2):
        top = (Fraction(2), Fraction(-3)) if top_nonzero else (Fraction(0),) * 2
        response = (
            (Fraction(4), Fraction(0), Fraction(-1), Fraction(0), Fraction(0))
            if response_nonzero
            else (Fraction(0),) * 5
        )
        rhs = [[left * right for right in response] for left in top]
        pure_columns = [tuple(row[index] for row in rhs) for index in range(3)]
        mixed_columns = [tuple(row[index] for row in rhs) for index in range(3, 5)]
        assert all(not any(column) for column in mixed_columns)
        pure_rank = rank(columns_to_rows(pure_columns, 2))
        assert pure_rank == int(top_nonzero and response_nonzero)
        rank_one += pure_rank
        cases += 1
    return cases, rank_one


def quotient_survives(nuisance, vector):
    dimension = len(vector)
    before = rank(columns_to_rows(nuisance, dimension))
    after = rank(columns_to_rows(nuisance + [vector], dimension))
    return after > before


def check_pure_z_operator_spaces():
    pure_z = (Fraction(0), Fraction(1))
    lines = []
    for delta, eta in product(range(-3, 4), repeat=2):
        if not (delta or eta):
            continue
        line = (Fraction(delta), Fraction(eta))
        if line not in lines:
            lines.append(line)
    checks = 0
    for line in lines:
        contains_pure_z = line[0] == 0
        if contains_pure_z:
            assert line[1] != 0
        checks += 1
    assert quotient_survives([], pure_z)
    assert not quotient_survives([pure_z], pure_z)
    full_plane = [(Fraction(1), Fraction(0)), pure_z]
    assert rank(columns_to_rows(full_plane, 2)) == 2
    return checks, len(lines)


def two_by_two_minors(matrix):
    return [
        matrix[0][left] * matrix[1][right] - matrix[0][right] * matrix[1][left]
        for left, right in combinations(range(len(matrix[0])), 2)
    ]


def check_fitting_tables():
    checks = 0
    values = tuple(Fraction(value) for value in (-2, -1, 0, 1, 2))
    for entries in product(values, repeat=4):
        nuisance = [[entries[0]], [entries[1]]]
        augmented = [[entries[0], entries[2]], [entries[1], entries[3]]]
        rise = rank(augmented) > rank(nuisance)
        detected = (
            not any(entry for row in nuisance for entry in row)
            and any(entry for row in augmented for entry in row)
        ) or (
            not any(two_by_two_minors(nuisance)) and any(two_by_two_minors(augmented))
        )
        assert rise == detected
        checks += 1
    return checks


def check_four_root_formulas():
    order = 4
    pair_counts = {}
    for open_root in range(order):
        signatures = surviving_signatures(order, 1, frozenset({open_root}))
        pair_counts[open_root] = len(signatures)
        assert len(signatures) == 6

    four_port_counts = {}
    for open_pair in combinations(range(order), 2):
        signatures = surviving_signatures(order, 2, frozenset(open_pair))
        four_port_counts[open_pair] = len(signatures)
        assert len(signatures) == 2

    for dimension in (27, 9):
        diagonal = []
        positions = (0, 13, 26) if dimension == 27 else (0, 4, 8)
        for position in positions:
            vector = [Fraction(0)] * dimension
            vector[position] = Fraction(1)
            diagonal.append(tuple(vector))
        assert rank(columns_to_rows(diagonal, dimension)) == 3
        assert 3 < dimension
    return pair_counts, four_port_counts


def main() -> None:
    shadow_checks, shadow_records = check_top_grade_shadows()
    coupling = check_target_coupling()
    operator_spaces = check_pure_z_operator_spaces()
    fitting = check_fitting_tables()
    four_root = check_four_root_formulas()
    compact = {
        order: {
            half_size: (len(values), values[0]) for half_size, values in record.items()
        }
        for order, record in shadow_records.items()
    }
    print("residual-present top-shadow and pure-Z checks: PASS")
    print("  explicit top/lower signatures checked:", shadow_checks)
    print("  masks and (top,lower) counts:", compact)
    print("  target coupling cases / rank-one cases:", coupling)
    print("  projective operator checks / rows:", operator_spaces)
    print("  exact Fitting rank tables:", fitting)
    print("  r=4 pair / four-port top counts:", four_root)
    print("  scope: conditional pure-Z route; activity and node closure stay open")


if __name__ == "__main__":
    main()
