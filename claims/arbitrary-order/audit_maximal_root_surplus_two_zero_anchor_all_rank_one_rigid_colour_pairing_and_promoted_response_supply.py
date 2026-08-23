"""Independent no-project-import audit for GLS57.

This script does not import the primary verifier or repository code.  It uses
an F_7 incidence census, bit-mask pair/deck labels, and an independent sparse
polynomial representation to audit the theorem's load-bearing claims.
"""

from __future__ import annotations

from itertools import combinations, product

PRIME = 7


def colour_mask(code: int, colour: int) -> int:
    mask = 0
    for label in range(6):
        if (code // (3**label)) % 3 == colour:
            mask |= 1 << label
    return mask


def audit_bitmask_partition() -> dict[str, int]:
    compatible = 0
    pure_slice_pair_terms = 0
    q_same = 0
    q_split = 0
    response_labels = 0
    full_mask = (1 << 6) - 1

    for code in range(3**6):
        masks = tuple(colour_mask(code, colour) for colour in range(3))
        assert masks[0] ^ masks[1] ^ masks[2] == full_mask
        if any(mask.bit_count() < 2 for mask in masks):
            continue
        compatible += 1
        assert all(mask.bit_count() == 2 for mask in masks)
        # The only pair label surviving the all-c auxiliary slice is P_c.
        for mask in masks:
            surviving = [
                (1 << left) | (1 << right)
                for left, right in combinations(range(6), 2)
                if ((1 << left) | (1 << right)) & ~mask == 0
            ]
            assert surviving == [mask]
            pure_slice_pair_terms += len(surviving)

        for left, right in combinations(range(6), 2):
            q_mask = (1 << left) | (1 << right)
            disjoint = sum(not (mask & q_mask) for mask in masks)
            if q_mask in masks:
                assert disjoint == 2
                q_same += 1
            else:
                assert disjoint == 1
                q_split += 1
            response_labels += disjoint

    assert compatible == 90
    assert pure_slice_pair_terms == 270
    assert q_same == 270
    assert q_split == 1080
    assert response_labels == 1620
    return {
        "F7_compatible_readout_codes": compatible,
        "bitmask_unique_pure_pair_terms": pure_slice_pair_terms,
        "bitmask_same_Q_cases": q_same,
        "bitmask_split_Q_cases": q_split,
        "bitmask_promoted_response_labels": response_labels,
    }


def matrix_add(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple((x + y) % PRIME for x, y in zip(left, right, strict=True))


def matrix_outer(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple((x * y) % PRIME for x in left for y in right)


def audit_incidence_factorization() -> dict[str, int]:
    tested = 0
    forced_nonzero = 0

    # Use a representation unrelated to the primary construction: enumerate
    # shore quadruples and retain those whose symmetric companion is supported
    # on E_cc.  Whenever h*M=E_cc, both h and M must be nonzero.
    sample = (
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1),
        (1, 1, 0),
        (1, 0, 1),
        (0, 1, 1),
        (1, 1, 1),
        (1, 2, 3),
    )
    for colour in range(3):
        target = tuple(
            int(row == colour and column == colour)
            for row in range(3)
            for column in range(3)
        )
        for x_s, y_s, x_t, y_t in product(sample, repeat=4):
            companion = matrix_add(
                matrix_outer(x_s, y_t), matrix_outer(x_t, y_s)
            )
            for h_value in range(1, PRIME):
                tested += 1
                scaled = tuple((h_value * entry) % PRIME for entry in companion)
                if scaled != target:
                    continue
                assert any(companion)
                assert h_value
                forced_nonzero += 1

    # The census need not hit every solution but must hit non-vacuous examples.
    assert forced_nonzero > 0
    return {
        "F7_incidence_factorizations_tested": tested,
        "F7_exact_target_factorizations_found": forced_nonzero,
    }


def audit_off_readout_faces() -> dict[str, int]:
    # Encode the 2+2+2 readout as base-three digits but test the face using
    # bit membership, independently of the primary list-based implementation.
    readout = (0, 0, 1, 1, 2, 2)
    all_pairs = tuple((1 << left) | (1 << right) for left, right in combinations(range(6), 2))
    colour_masks = (0b000011, 0b001100, 0b110000)
    face_cells = 0
    pure_cells = 0
    forced_zeros = 0
    conditional_zeros = 0

    for pair_mask in all_pairs:
        pair_labels = tuple(label for label in range(6) if pair_mask & (1 << label))
        complement = tuple(label for label in range(6) if not pair_mask & (1 << label))
        options = tuple(
            tuple(colour for colour in range(3) if colour != readout[label])
            for label in complement
        )
        for tail in product(*options):
            word = list(readout)
            for label, colour in zip(complement, tail, strict=True):
                word[label] = colour
            active_mask = sum(
                1 << label
                for label in range(6)
                if word[label] == readout[label]
            )
            assert active_mask == pair_mask
            face_cells += 1
            constant = all(colour == word[0] for colour in word)
            if pair_mask in colour_masks:
                pure_cells += int(constant)
                forced_zeros += int(not constant)
            else:
                assert readout[pair_labels[0]] != readout[pair_labels[1]]
                assert not constant
                conditional_zeros += 1

    assert (face_cells, pure_cells, forced_zeros, conditional_zeros) == (
        240,
        3,
        45,
        192,
    )
    return {
        "independent_off_readout_face_cells": face_cells,
        "independent_unique_pure_cells": pure_cells,
        "independent_forced_pair_face_zeros": forced_zeros,
        "independent_conditional_cross_face_zeros": conditional_zeros,
    }


def evaluate_support_polynomial(
    terms: dict[int, int], left: tuple[int, ...], right: tuple[int, ...]
) -> int:
    total = 0
    for monomial, coefficient in terms.items():
        row, column = divmod(monomial, 3)
        total += coefficient * left[row] * right[column]
    return total % PRIME


def audit_polynomial_support() -> dict[str, int]:
    checked = 0
    cancellations = 0
    nonzero_points = 0
    torus = tuple(product(range(1, PRIME), repeat=3))
    for colour in range(3):
        diagonal = 3 * colour + colour
        other = (colour + 1) % 3
        other_diagonal = 3 * other + other
        terms = {diagonal: 1, other_diagonal: PRIME - 1}
        assert terms[diagonal]
        checked += 1

        ones = (1, 1, 1)
        assert evaluate_support_polynomial(terms, ones, ones) == 0
        cancellations += 1

        values = {
            evaluate_support_polynomial(terms, left, right)
            for left in torus
            for right in torus
        }
        assert 0 in values and any(values)
        nonzero_points += 1

    return {
        "independent_response_support_checks": checked,
        "independent_exceptional_cancellations": cancellations,
        "F7_torus_nonzero_response_families": nonzero_points,
    }


def main() -> None:
    summary: dict[str, int] = {}
    summary.update(audit_bitmask_partition())
    summary.update(audit_incidence_factorization())
    summary.update(audit_off_readout_faces())
    summary.update(audit_polynomial_support())
    for key, value in summary.items():
        print(f"{key}: {value}")
    print("GLS57 independent no-import audit: PASS")


if __name__ == "__main__":
    main()
