"""Independent no-project-import audit of the GLS19 pure-Z top shadow."""

from itertools import combinations, product
from math import factorial, gcd

PRIME = 5


def matching_masks(available_mask, edge_count, answer, chosen=()):
    if edge_count == 0:
        answer.add(tuple(sorted(chosen)))
        return
    if available_mask.bit_count() < 2 * edge_count:
        return
    least = available_mask & -available_mask
    rest = available_mask ^ least
    matching_masks(rest, edge_count, answer, chosen)
    partners = rest
    while partners:
        partner = partners & -partners
        partners ^= partner
        matching_masks(
            rest ^ partner, edge_count - 1, answer, chosen + (least | partner,)
        )


def all_matchings(order, edge_count):
    answer = set()
    matching_masks((1 << order) - 1, edge_count, answer)
    return answer


def audit_top_cutoff():
    checks = 0
    records = {}
    for order in range(2, 9):
        order_record = {}
        for half_size in range(1, order // 2 + 1):
            counts = []
            for roots in combinations(range(order), half_size):
                open_mask = sum(1 << root for root in roots)
                top = [
                    matching
                    for matching in all_matchings(order, half_size)
                    if all(edge & open_mask for edge in matching)
                ]
                assert all(
                    all((edge & open_mask).bit_count() == 1 for edge in matching)
                    for matching in top
                )
                top_monomials = len(top) * factorial(order - 2 * half_size)
                assert top_monomials == factorial(order - half_size)
                for grade in range(half_size + 1, order // 2 + 1):
                    assert not [
                        matching
                        for matching in all_matchings(order, grade)
                        if all(edge & open_mask for edge in matching)
                    ]
                lower = [
                    matching
                    for matching in all_matchings(order, half_size - 1)
                    if all(edge & open_mask for edge in matching)
                ]
                assert lower
                counts.append((top_monomials, len(lower)))
                checks += len(top) + len(lower)
            order_record[half_size] = tuple(counts)
        records[order] = order_record
    return checks, records


def inverse(value):
    return pow(value % PRIME, PRIME - 2, PRIME)


def matrix_rank(rows):
    work = [[entry % PRIME for entry in row] for row in rows]
    if not work:
        return 0
    row_count = len(work)
    column_count = len(work[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, row_count) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = inverse(work[pivot_row][column])
        work[pivot_row] = [(scale * entry) % PRIME for entry in work[pivot_row]]
        for row in range(row_count):
            if row == pivot_row:
                continue
            factor = work[row][column]
            if factor:
                work[row] = [
                    (left - factor * right) % PRIME
                    for left, right in zip(work[row], work[pivot_row], strict=True)
                ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def columns_to_rows(columns, dimension):
    return [[column[row] for column in columns] for row in range(dimension)]


def audit_complete_target_words():
    alpha = (1, 2, 4)
    checked = 0
    admitted = 0
    for top in product(range(PRIME), repeat=2):
        for response in product(range(PRIME), repeat=5):
            pure_columns = [
                tuple(
                    (top[row] * response[column] * inverse(alpha[column])) % PRIME
                    for row in range(2)
                )
                for column in range(3)
            ]
            mixed = [
                tuple((top[row] * response[column]) % PRIME for row in range(2))
                for column in range(3, 5)
            ]
            equation_holds = all(not any(column) for column in mixed)
            if equation_holds:
                quotient_rank = matrix_rank(columns_to_rows(pure_columns, 2))
                assert quotient_rank <= 1
                assert (quotient_rank == 1) == (any(top) and any(response))
                if any(top):
                    assert not any(response[3:])
                admitted += 1
            checked += 1
    return checked, admitted


def primitive(delta, eta):
    divisor = gcd(abs(delta), abs(eta))
    delta //= divisor
    eta //= divisor
    if delta < 0 or (delta == 0 and eta < 0):
        delta, eta = -delta, -eta
    return delta, eta


def audit_pure_z_lines():
    lines = {
        primitive(delta, eta)
        for delta in range(-6, 7)
        for eta in range(-6, 7)
        if delta or eta
    }
    checks = 0
    for delta, eta in lines:
        contains_pure_z = delta == 0
        if contains_pure_z:
            assert (delta, eta) == (0, 1)
        checks += 1
    coefficient_spaces = (
        {(0, 1)},
        {(1, 0), (0, 1), (1, 1)},
        {(0, 1)},
    )
    assert (0, 1) in set.intersection(*coefficient_spaces)
    return checks, len(lines)


def minors(rows, size):
    if size == 1:
        return [entry % PRIME for row in rows for entry in row]
    if size == 2:
        return [
            (rows[0][left] * rows[1][right] - rows[0][right] * rows[1][left]) % PRIME
            for left in range(len(rows[0]))
            for right in range(left + 1, len(rows[0]))
        ]
    raise ValueError("bounded audit uses only one- and two-minors")


def affine(coefficients, point):
    return (coefficients[0] + coefficients[1] * point) % PRIME


def audit_gated_fitting_sets():
    checks = 0
    empty = 0
    gates = ((1, 0),) + tuple((-root % PRIME, 1) for root in range(PRIME))
    for coefficients in product(range(PRIME), repeat=4):
        first = coefficients[:2]
        second = coefficients[2:]
        for desired in product(range(PRIME), repeat=2):
            for gate in gates:
                useful = []
                containment = True
                for point in range(PRIME):
                    nuisance = [[affine(first, point)], [affine(second, point)]]
                    augmented = [
                        nuisance[0] + [desired[0]],
                        nuisance[1] + [desired[1]],
                    ]
                    gate_value = affine(gate, point)
                    if gate_value and matrix_rank(augmented) > matrix_rank(nuisance):
                        useful.append(point)
                    for size in (1, 2):
                        if (
                            not any(minors(nuisance, size))
                            and gate_value
                            and any(minors(augmented, size))
                        ):
                            containment = False
                assert (not useful) == containment
                empty += int(not useful)
                checks += 1
    return checks, empty


def audit_four_root_cross_matchings():
    order = 4
    pair_counts = {}
    for root in range(order):
        mask = 1 << root
        survivors = [
            matching
            for matching in all_matchings(order, 1)
            if all(edge & mask for edge in matching)
        ]
        pair_counts[root] = len(survivors) * factorial(2)
        assert pair_counts[root] == 6

    four_port_counts = {}
    for roots in combinations(range(order), 2):
        mask = sum(1 << root for root in roots)
        survivors = [
            matching
            for matching in all_matchings(order, 2)
            if all(edge & mask for edge in matching)
        ]
        assert all(
            all((edge & mask).bit_count() == 1 for edge in matching)
            for matching in survivors
        )
        four_port_counts[roots] = len(survivors)
        assert len(survivors) == 2

    for dimension, positions in ((27, (0, 13, 26)), (9, (0, 4, 8))):
        columns = []
        for position in positions:
            vector = [0] * dimension
            vector[position] = 1
            columns.append(tuple(vector))
        assert matrix_rank(columns_to_rows(columns, dimension)) == 3 < dimension
    return pair_counts, four_port_counts


def main():
    cutoff_checks, cutoff_records = audit_top_cutoff()
    target_words = audit_complete_target_words()
    lines = audit_pure_z_lines()
    fitting = audit_gated_fitting_sets()
    four_root = audit_four_root_cross_matchings()
    compact = {
        order: {
            half_size: (len(values), values[0]) for half_size, values in record.items()
        }
        for order, record in cutoff_records.items()
    }
    print("INDEPENDENT RESIDUAL-PRESENT TOP-SHADOW AUDIT PASS")
    print("  bitmask top/lower matching checks:", cutoff_checks)
    print("  masks and (top monomials, lower matchings):", compact)
    print("  complete five-word equations / admitted equations:", target_words)
    print("  primitive pure-Z line checks:", lines)
    print("  gated affine point sets / empty loci:", fitting)
    print("  r=4 pair / four-port cross-matching counts:", four_root)
    print("  scope: conditional pure-Z route; activity and node closure remain open")


if __name__ == "__main__":
    main()
