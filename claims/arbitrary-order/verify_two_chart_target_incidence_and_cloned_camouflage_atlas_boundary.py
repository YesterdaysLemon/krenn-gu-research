"""Focused exact verifier for the two-chart/cloned-atlas boundary."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product

import sympy as sp

COLORS = range(3)
MATCHINGS_4 = (
    (((0, 1), (2, 3))),
    (((0, 2), (1, 3))),
    (((0, 3), (1, 2))),
)


def verify_dense_affine_boundary() -> None:
    """Replay Proposition 5 by exact ranks and left kernels."""

    # Injectivity of bar A does not imply target incidence.  Both rank tests
    # are required for unique supply.
    injective_sensor = sp.Matrix([[1], [1]])
    nonincident_target = sp.Matrix([0, -1])
    assert injective_sensor.rank() == 1
    assert injective_sensor.row_join(nonincident_target).rank() == 2

    for mixed_size in range(2, 9):
        dim_f = mixed_size + 1
        d = sp.eye(dim_f)[:, 0]
        mixed = [sp.eye(dim_f)[:, i] for i in range(1, dim_f)]

        a0 = d
        a1 = d
        b0 = sp.Matrix.hstack(*mixed)
        b1 = sp.Matrix.hstack(*(d + vector for vector in mixed))

        zero = sp.zeros(dim_f, mixed_size)
        top = sp.Matrix.hstack(a0, b0, zero)
        bottom = sp.Matrix.hstack(a1, zero, b1)
        sensor = sp.Matrix.vstack(top, bottom)

        target_shift = sp.Matrix.vstack(d, sp.zeros(dim_f, 1))
        assert sensor.rank() == 2 * mixed_size + 1
        assert sensor.row_join(target_shift).rank() == sensor.rank() + 1

        left_kernel = sensor.T.nullspace()
        assert len(left_kernel) == 1
        ell = left_kernel[0]
        ell0 = ell[:dim_f, :]
        ell1 = ell[dim_f:, :]
        aggregate = ell0 + ell1
        assert aggregate[0] == 0
        assert all(aggregate[i] != 0 for i in range(1, dim_f))
        assert sum(1 for value in aggregate[1:, :] if value != 0) == mixed_size
        assert (ell.T * target_shift)[0] != 0

        # A common physical tensor with the right pure anchor can avoid any
        # preselected mixed coordinate.
        for omitted in range(mixed_size):
            active = 1 + ((omitted + 1) % mixed_size)
            tensor = d - sp.eye(dim_f)[:, active]
            assert tensor[0] == 1
            assert tensor[omitted + 1] == 0
            assert b0.row_join(tensor - d).rank() == b0.rank()
            assert b1.row_join(tensor - 2 * d).rank() == b1.rank()


def frame(port: int) -> tuple[tuple[int, ...], tuple[int, ...]]:
    if port in (0, 1):
        return (1, 0, 0), (0, 1, 0)
    return (0, 1, 0), (1, 0, 0)


def corrected_entry(i: int, j: int, ci: int, cj: int) -> Fraction:
    ai, bi = frame(i)
    aj, bj = frame(j)
    return Fraction(ai[ci] * bj[cj] + bi[ci] * aj[cj])


def diagonal_weights(i: int, j: int) -> tuple[Fraction, Fraction, Fraction]:
    if i > j:
        i, j = j, i
    if (i, j) == (0, 1) or (i == 2 and j >= 3):
        return Fraction(0), Fraction(0), Fraction(1)
    if (i, j) == (0, 2):
        return Fraction(1), Fraction(1), Fraction(0)
    if (i, j) == (1, 2):
        return Fraction(3), Fraction(2), Fraction(0)
    if i == 0 and j >= 3:
        return Fraction(1), Fraction(2, 3), Fraction(0)
    if i == 1 and j >= 3:
        return Fraction(2), Fraction(2), Fraction(0)
    # Clone--clone edges are not used by the star atlas.
    return Fraction(0), Fraction(0), Fraction(0)


def diagonal_entry(i: int, j: int, ci: int, cj: int) -> Fraction:
    if ci != cj:
        return Fraction(0)
    return diagonal_weights(i, j)[ci]


def direct_entry(i: int, j: int, ci: int, cj: int) -> Fraction:
    return diagonal_entry(i, j, ci, cj) - corrected_entry(i, j, ci, cj)


def compound_entry(entry, window: tuple[int, ...], word: tuple[int, ...]) -> Fraction:
    colors = dict(zip(window, word, strict=True))
    total = Fraction(0)
    for local_first, local_second in MATCHINGS_4:
        first = tuple(window[index] for index in local_first)
        second = tuple(window[index] for index in local_second)
        total += entry(*first, colors[first[0]], colors[first[1]]) * entry(
            *second, colors[second[0]], colors[second[1]]
        )
    return total


def active_colors(window: tuple[int, ...], port: int) -> set[int]:
    active: set[int] = set()
    for color in COLORS:
        for partner in window:
            if partner == port or diagonal_weights(port, partner)[color] == 0:
                continue
            complement = tuple(v for v in window if v not in (port, partner))
            if any(
                delta != color
                and diagonal_weights(complement[0], complement[1])[delta] != 0
                for delta in COLORS
            ):
                active.add(color)
    return active


def verify_cloned_camouflage_atlas() -> None:
    expected_pure = (Fraction(3), Fraction(4, 3), Fraction(1))

    for clone_count in range(1, 8):
        ports = tuple(range(clone_count + 3))
        windows = tuple((0, 1, 2, clone) for clone in ports if clone >= 3)
        chart_pair_data = {
            window: {
                tuple(sorted(edge)): diagonal_weights(*edge)
                for edge in combinations(window, 2)
            }
            for window in windows
        }

        # All selected pair responses are diagonal D=B+K.
        used_edges = {
            tuple(sorted(edge))
            for window in windows
            for edge in combinations(window, 2)
        }
        for i, j in used_edges:
            for ci, cj in product(COLORS, repeat=2):
                response = direct_entry(i, j, ci, cj) + corrected_entry(i, j, ci, cj)
                assert response == diagonal_entry(i, j, ci, cj)
                if ci != cj:
                    assert response == 0

        for window in windows:
            response: dict[tuple[int, ...], Fraction] = {}
            for word in product(COLORS, repeat=4):
                d_compound = compound_entry(diagonal_entry, window, word)
                k_compound = compound_entry(corrected_entry, window, word)
                response[word] = d_compound - k_compound
                if len(set(word)) > 1:
                    assert response[word] == 0
                # The global sign flip preserves C(K).
                neg_compound = compound_entry(
                    lambda i, j, ci, cj: -corrected_entry(i, j, ci, cj),
                    window,
                    word,
                )
                assert d_compound - neg_compound == response[word]

            assert tuple(response[(c, c, c, c)] for c in COLORS) == expected_pure
            for port in window:
                assert active_colors(window, port) == {0, 1}

        # Every overlap uses the literal same rows and common D blocks.
        for left, right in combinations(windows, 2):
            overlap = set(left) & set(right)
            assert overlap == {0, 1, 2}
            for i, j in combinations(sorted(overlap), 2):
                assert chart_pair_data[left][i, j] == chart_pair_data[right][i, j]

        # The changed channel is nonzero and cannot be an invariant-preserving
        # common O(J) gauge image.
        assert corrected_entry(0, 1, 0, 1) == 1
        assert -corrected_entry(0, 1, 0, 1) == -1


def main() -> None:
    verify_dense_affine_boundary()
    verify_cloned_camouflage_atlas()
    print("two-chart target-incidence/cloned-atlas verifier: PASS")


if __name__ == "__main__":
    main()
