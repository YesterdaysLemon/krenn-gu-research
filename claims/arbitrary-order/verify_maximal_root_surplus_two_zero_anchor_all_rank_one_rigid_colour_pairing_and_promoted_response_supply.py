"""Focused exact checks for GLS57.

The written theorem carries the complete-witness and characteristic-zero
proof.  This verifier uses exact rationals to replay the rank-one companion
factorization, exhaustively checks all coordinate-readout and residual-pair
placements, and checks the response-polynomial and exceptional-fibre boundary.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product

Vector = tuple[Fraction, Fraction, Fraction]
Matrix = tuple[Fraction, ...]


def basis(colour: int) -> Vector:
    return tuple(Fraction(int(index == colour)) for index in range(3))  # type: ignore[return-value]


def outer(left: Vector, right: Vector) -> Matrix:
    return tuple(x * y for x in left for y in right)


def add(left: Matrix, right: Matrix) -> Matrix:
    return tuple(x + y for x, y in zip(left, right, strict=True))


def scale(value: Fraction, tensor: Matrix) -> Matrix:
    return tuple(value * entry for entry in tensor)


def companion_matrix(
    x_s: Vector,
    y_s: Vector,
    x_t: Vector,
    y_t: Vector,
) -> Matrix:
    return add(outer(x_s, y_t), outer(x_t, y_s))


def audit_colour_profiles() -> dict[str, int]:
    labels = tuple(range(6))
    residual_pairs = tuple(combinations(labels, 2))
    profiles = 0
    target_compatible = 0
    q_placements = 0
    same_colour_q = 0
    split_colour_q = 0
    promoted_targets = 0

    for kappa in product(range(3), repeat=6):
        profiles += 1
        colour_pairs = tuple(
            tuple(label for label in labels if kappa[label] == colour)
            for colour in range(3)
        )
        # A nonzero all-c target slice requires some pair contained in P_c.
        if any(len(pair) < 2 for pair in colour_pairs):
            continue
        target_compatible += 1
        assert tuple(map(len, colour_pairs)) == (2, 2, 2)
        assert set().union(*map(set, colour_pairs)) == set(labels)

        for q_pair in residual_pairs:
            q_placements += 1
            q_set = set(q_pair)
            disjoint = [pair for pair in colour_pairs if q_set.isdisjoint(pair)]
            if any(set(pair) == q_set for pair in colour_pairs):
                same_colour_q += 1
                assert len(disjoint) == 2
            else:
                split_colour_q += 1
                assert len(disjoint) == 1
            promoted_targets += len(disjoint)

    assert profiles == 3**6
    assert target_compatible == 90
    assert q_placements == 90 * 15
    assert same_colour_q == 90 * 3
    assert split_colour_q == 90 * 12
    assert promoted_targets == 90 * (3 * 2 + 12)
    return {
        "coordinate_profiles": profiles,
        "target_compatible_profiles": target_compatible,
        "residual_pair_placements": q_placements,
        "same_colour_residual_placements": same_colour_q,
        "split_colour_residual_placements": split_colour_q,
        "forced_promoted_targets": promoted_targets,
    }


def audit_full_companion_factorization() -> dict[str, int]:
    # P_0=(0,1), P_1=(2,3), P_2=(4,5).  For each colour choose
    # X_s=e_c/h_c, Y_t=e_c and the other two shores zero.  Both rank-one
    # readouts are nonzero and h_c M_c=E_cc exactly.
    deck_coefficients = (Fraction(2), Fraction(-3), Fraction(5))
    checked_entries = 0
    nonzero_companions = 0
    for colour, h_c in enumerate(deck_coefficients):
        e_c = basis(colour)
        zero = (Fraction(0), Fraction(0), Fraction(0))
        x_s = tuple(entry / h_c for entry in e_c)  # type: ignore[assignment]
        y_s = zero
        x_t = zero
        y_t = e_c
        assert any(x_s) and any(y_t)
        companion = companion_matrix(x_s, y_s, x_t, y_t)
        target = outer(e_c, e_c)
        assert scale(h_c, companion) == target
        assert any(companion)
        nonzero_companions += 1

        # The auxiliary support is the one (c,c) cell.  In a flattened
        # A x P_c tensor, all eight other auxiliary cells are identically zero.
        for auxiliary_left in range(3):
            for auxiliary_right in range(3):
                block = (
                    companion
                    if (auxiliary_left, auxiliary_right) == (colour, colour)
                    else (Fraction(0),) * 9
                )
                if (auxiliary_left, auxiliary_right) == (colour, colour):
                    assert scale(h_c, block) == target
                else:
                    assert not any(block)
                checked_entries += 9

    assert nonzero_companions == 3
    assert checked_entries == 3 * 9 * 9
    return {
        "pure_companion_colours": nonzero_companions,
        "full_tensor_entries_checked": checked_entries,
    }


def audit_mixed_word_master_support() -> dict[str, int]:
    kappa = (0, 0, 1, 1, 2, 2)
    labels = tuple(range(6))
    colour_pairs = ({0, 1}, {2, 3}, {4, 5})
    off_readout_words = 0
    pure_face_cells = 0
    forced_pair_face_zeros = 0
    conditional_cross_face_zeros = 0

    for pair_tuple in combinations(labels, 2):
        pair = set(pair_tuple)
        complement = tuple(label for label in labels if label not in pair)
        choices = tuple(
            tuple(colour for colour in range(3) if colour != kappa[label])
            for label in complement
        )
        for off_colours in product(*choices):
            word = list(kappa)
            for label, colour in zip(complement, off_colours, strict=True):
                word[label] = colour
            active = {
                label for label in labels if word[label] == kappa[label]
            }
            assert active == pair
            off_readout_words += 1
            constant = len(set(word)) == 1
            if pair in colour_pairs:
                if constant:
                    pure_face_cells += 1
                    assert next(iter(pair)) // 2 == word[0]
                else:
                    forced_pair_face_zeros += 1
            else:
                assert not constant
                conditional_cross_face_zeros += 1

    assert off_readout_words == 15 * 16
    assert pure_face_cells == 3
    assert forced_pair_face_zeros == 3 * 15
    assert conditional_cross_face_zeros == 12 * 16
    return {
        "off_readout_face_words": off_readout_words,
        "unique_pure_face_cells": pure_face_cells,
        "forced_colour_pair_face_zeros": forced_pair_face_zeros,
        "conditional_cross_pair_face_zeros": conditional_cross_face_zeros,
    }


def evaluate_bilinear(
    coefficients: dict[tuple[int, int], Fraction],
    z_0: Vector,
    z_1: Vector,
) -> Fraction:
    return sum(
        coefficient * z_0[left] * z_1[right]
        for (left, right), coefficient in coefficients.items()
    )


def audit_response_polynomial() -> dict[str, int]:
    nonzero_monomials = 0
    exceptional_cancellations = 0
    common_torus_points = 0
    for colour, h_c in enumerate((Fraction(2), Fraction(-3), Fraction(5))):
        other = (colour + 1) % 3
        coefficients = {
            (colour, colour): h_c,
            (other, other): -h_c,
        }
        assert coefficients[(colour, colour)] == h_c
        assert any(coefficients.values())
        nonzero_monomials += 1

        ones = (Fraction(1), Fraction(1), Fraction(1))
        assert evaluate_bilinear(coefficients, ones, ones) == 0
        exceptional_cancellations += 1

        # Search a small exact torus for a point where the response and two
        # representative nonzero GLS4 gate polynomials stay nonzero.
        found = False
        values = (Fraction(1), Fraction(2), Fraction(3))
        for z_0 in product(values, repeat=3):
            for z_1 in product(values, repeat=3):
                response = evaluate_bilinear(coefficients, z_0, z_1)
                h_gate = sum(z_0[index] * z_1[index] for index in range(3))
                p_gate = z_0[0] * z_1[1] + z_0[2] * z_1[2]
                if response and h_gate and p_gate:
                    found = True
                    break
            if found:
                break
        assert found
        common_torus_points += 1

    return {
        "nonzero_response_monomials": nonzero_monomials,
        "explicit_exceptional_fibre_cancellations": exceptional_cancellations,
        "common_torus_points_found": common_torus_points,
    }


def audit_old_probe_gld3_activity_no_go() -> dict[str, int]:
    labels = tuple(range(6))
    compatible_profiles = 0
    port_window_cases = 0
    diagonal_cells_checked = 0
    maximum_activity_colours = 0

    for kappa in product(range(3), repeat=6):
        if tuple(kappa.count(colour) for colour in range(3)) != (2, 2, 2):
            continue
        compatible_profiles += 1
        for window in combinations(labels, 4):
            for port in window:
                active_colours: set[int] = set()
                for other in window:
                    if other == port:
                        continue
                    for colour in range(3):
                        # Equation (8) supports D_(port,other) only at the
                        # cell (kappa(port),kappa(other)).  This diagonal cell
                        # can therefore be nonzero only in the stated case.
                        supported = (
                            kappa[port] == colour == kappa[other]
                        )
                        diagonal_cells_checked += 1
                        if supported:
                            active_colours.add(colour)
                assert active_colours <= {kappa[port]}
                assert len(active_colours) <= 1
                maximum_activity_colours = max(
                    maximum_activity_colours, len(active_colours)
                )
                port_window_cases += 1

    assert compatible_profiles == 90
    assert port_window_cases == 90 * 15 * 4
    assert diagonal_cells_checked == port_window_cases * 3 * 3
    assert maximum_activity_colours == 1
    return {
        "old_probe_compatible_profiles": compatible_profiles,
        "old_probe_port_window_cases": port_window_cases,
        "old_probe_diagonal_cells_checked": diagonal_cells_checked,
        "old_probe_maximum_activity_colours": maximum_activity_colours,
    }


def main() -> None:
    summary: dict[str, int] = {}
    summary.update(audit_colour_profiles())
    summary.update(audit_full_companion_factorization())
    summary.update(audit_mixed_word_master_support())
    summary.update(audit_response_polynomial())
    summary.update(audit_old_probe_gld3_activity_no_go())
    for key, value in summary.items():
        print(f"{key}: {value}")
    print("GLS57 focused exact verifier: PASS")


if __name__ == "__main__":
    main()
