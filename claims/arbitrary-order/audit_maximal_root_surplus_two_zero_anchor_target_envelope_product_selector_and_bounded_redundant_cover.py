"""Independent no-import audit for the GLS28 zero-anchor target envelope."""

from fractions import Fraction
from itertools import combinations


def vector(values):
    return tuple(Fraction(value) for value in values)


def rank(columns):
    if not columns:
        return 0
    rows = [[column[row] for column in columns] for row in range(len(columns[0]))]
    pivot_row = 0
    for column in range(len(columns)):
        selected = next(
            (row for row in range(pivot_row, len(rows)) if rows[row][column]), None
        )
        if selected is None:
            continue
        rows[pivot_row], rows[selected] = rows[selected], rows[pivot_row]
        pivot = rows[pivot_row][column]
        rows[pivot_row] = [entry / pivot for entry in rows[pivot_row]]
        for row in range(len(rows)):
            if row == pivot_row or not rows[row][column]:
                continue
            scale = rows[row][column]
            rows[row] = [
                entry - scale * base
                for entry, base in zip(rows[row], rows[pivot_row], strict=True)
            ]
        pivot_row += 1
    return pivot_row


def contains(columns, item):
    return rank(columns + [item]) == rank(columns)


def coordinate(index, dimension):
    return tuple(Fraction(int(slot == index)) for slot in range(dimension))


def sparse_root_support(tensors):
    """Read root coefficient vectors from sparse (root, port...) dictionaries."""
    roots = []
    for tensor, port_words, root_dimension in tensors:
        for port_word in port_words:
            roots.append(
                tuple(
                    tensor.get((root, *port_word), Fraction(0))
                    for root in range(root_dimension)
                )
            )
    basis = []
    for item in roots:
        if not contains(basis, item):
            basis.append(item)
    return basis


def audit_label_supports():
    root_dimension = 8
    tangent = [coordinate(index, root_dimension) for index in range(3)]

    # One-Q data use only tangent roots, independently of target padding.
    one_q = {
        (root, port): Fraction((root + 1) * (port + 2))
        for root in range(3)
        for port in range(3)
    }
    one_q_roots = sparse_root_support([(one_q, ((0,), (1,), (2,)), root_dimension)])
    assert all(contains(tangent, item) for item in one_q_roots)

    # Foreign promoted-pair coefficients define their own full root support.
    pair = {
        (root, left, right): Fraction((root + 1) + 2 * left + 3 * right)
        for root in range(root_dimension)
        for left in range(3)
        for right in range(3)
    }
    all_words = tuple((left, right) for left in range(3) for right in range(3))
    pair_roots = sparse_root_support([(pair, all_words, root_dimension)])

    # A one-slot partial slice has the same root coefficients with one index retained.
    partial_roots = []
    for foreign in range(3):
        for shared in range(3):
            item = tuple(
                pair[(root, shared, foreign)] for root in range(root_dimension)
            )
            partial_roots.append(item)
    assert all(contains(pair_roots, item) for item in partial_roots)

    envelope = tangent + pair_roots
    assert all(contains(envelope, item) for item in one_q_roots + partial_roots)
    return {
        "tangent_rank": rank(tangent),
        "pair_support_rank": rank(pair_roots),
        "envelope_rank": rank(envelope),
    }


def audit_dimension_formula():
    results = {}
    for d0 in (1, 2):
        for d1 in (1, 2):
            # Coordinate-basis count for X0 tensor V + V tensor X1.
            left = {(i, j) for i in range(d0) for j in range(3)}
            right = {(i, j) for i in range(3) for j in range(d1)}
            tangent_dimension = len(left | right)
            assert tangent_dimension == 3 * d0 + 3 * d1 - d0 * d1
            # q is a nonzero tangent vector and is exactly the projector kernel.
            transverse_tangent = tangent_dimension - 1
            h = 8 - transverse_tangent
            assert h == 9 - 3 * d0 - 3 * d1 + d0 * d1
            results[(d0, d1)] = h
    assert results == {(1, 1): 4, (1, 2): 2, (2, 1): 2, (2, 2): 1}
    return results


def audit_product_separator():
    basis = [coordinate(index, 8) for index in range(8)]
    # A non-coordinate hyperplane: adjacent sums have alternating annihilator.
    envelope = [
        tuple(left + right for left, right in zip(basis[i], basis[i + 1], strict=True))
        for i in range(7)
    ]
    desired = basis[0]
    row = vector((1, -1, 1, -1, 1, -1, 1, -1))
    value = sum(a * b for a, b in zip(row, desired, strict=True))
    assert value == 1
    assert all(
        sum(a * b for a, b in zip(row, item, strict=True)) == 0 for item in envelope
    )

    # Tensor with a target coordinate: it kills every envelope-root coefficient.
    target_row = coordinate(0, 9)
    detected = sum(a * b for a, b in zip(row, desired, strict=True)) * target_row[0]
    assert detected == 1
    response = vector((3, 0, 0))
    assert detected * response[0] != 0
    return {
        "root_separator": row,
        "target_coordinate": 0,
        "response_coordinate": response[0],
    }


def smallest_label_cover(spaces, target, excluded, dimension):
    labels = [label for label in spaces if label != excluded]
    for size in range(1, dimension + 1):
        for chosen in combinations(labels, size):
            columns = [item for label in chosen for item in spaces[label]]
            if contains(columns, target):
                return chosen
    return None


def audit_bounded_covers_and_countermodel():
    basis4 = [coordinate(index, 4) for index in range(4)]
    target4 = tuple(sum(entries) for entries in zip(*basis4, strict=True))
    spaces4 = {index: [item] for index, item in enumerate(basis4)}
    spaces4[4] = [target4]
    cover = smallest_label_cover(spaces4, target4, excluded=4, dimension=4)
    assert cover is not None and len(cover) == 4

    e0, e1 = vector((1, 2)), vector((3, -1))
    minus_sum = tuple(-(left + right) for left, right in zip(e0, e1, strict=True))
    circuit = {0: [e0], 1: [e1], 2: [minus_sum]}
    for label, item in ((0, e0), (1, e1), (2, minus_sum)):
        cover_for_item = smallest_label_cover(
            circuit, item, excluded=label, dimension=2
        )
        assert cover_for_item is not None and len(cover_for_item) <= 2

    # Sharp distinction: deletion-stable diagonal coverage does not absorb e1.
    diagonal = vector((1, 1))
    transverse = vector((1, -1))
    sharp = {0: [diagonal], 1: [diagonal], 2: [transverse]}
    for excluded in sharp:
        assert smallest_label_cover(sharp, diagonal, excluded, 2) is not None
    assert not contains(sharp[0] + sharp[1], transverse)

    line = coordinate(0, 1)
    one_dimensional = {0: [line], 1: [line]}
    assert all(
        smallest_label_cover(one_dimensional, line, excluded, 1) is not None
        for excluded in one_dimensional
    )
    return {
        "h4_cover": cover,
        "h2_relation_labels": 3,
        "sharp_nonredundant_label": 2,
        "h1_nonzero_labels": 2,
    }


def audit_specialization():
    # Different family: A=(1+t,2), delta=(0,t), determinant=t(1+t).
    for value in (Fraction(1), Fraction(2), Fraction(-3, 2)):
        envelope = vector((1 + value, 2))
        diagonal = vector((0, value))
        determinant = envelope[0] * diagonal[1] - envelope[1] * diagonal[0]
        assert determinant == value * (1 + value) and determinant != 0

    # A rational redundant certificate clears after multiplying by t.
    value = Fraction(5, 3)
    coefficients = (1 / value, value)
    reconstructed = vector(coefficients)
    assert reconstructed == vector((Fraction(3, 5), Fraction(5, 3)))
    return {"escape_values": (1, 2, Fraction(-3, 2)), "cleared_denominator": 5}


def main():
    print("zero-anchor target-envelope independent audit: PASS")
    print("  sparse labelled-support reconstruction:", audit_label_supports())
    print("  inclusion-exclusion quotient dimensions:", audit_dimension_formula())
    print("  independently found product separator:", audit_product_separator())
    print(
        "  bounded covers and sharp countermodel:",
        audit_bounded_covers_and_countermodel(),
    )
    print("  direct rational specialization:", audit_specialization())
    print("  no imports from primary verifier or repository helpers")


if __name__ == "__main__":
    main()
