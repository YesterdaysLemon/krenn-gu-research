"""Verify the border-GHZ dimension and single-flip transversality theorem."""

from __future__ import annotations

from itertools import product

from sympy import Matrix, zeros

WORDS = tuple(product(range(3), repeat=5))
WORD_INDEX = {word: index for index, word in enumerate(WORDS)}
PURE_WORDS = tuple((colour,) * 5 for colour in range(3))


def coordinate_column(word: tuple[int, ...]) -> Matrix:
    column = zeros(len(WORDS), 1)
    column[WORD_INDEX[word], 0] = 1
    return column


def single_flip_words(active_colours: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    words = []
    for colour in active_colours:
        for root in range(5):
            for replacement in range(3):
                if replacement != colour:
                    word = [colour] * 5
                    word[root] = replacement
                    words.append(tuple(word))
    return tuple(words)


def column_matrix(words: tuple[tuple[int, ...], ...]) -> Matrix:
    return Matrix.hstack(*(coordinate_column(word) for word in words))


def main() -> None:
    pure_matrix = column_matrix(PURE_WORDS)
    all_flips = single_flip_words((0, 1, 2))
    assert len(all_flips) == len(set(all_flips)) == 30
    flip_matrix = column_matrix(all_flips)
    assert pure_matrix.row_join(flip_matrix).rank() == 33

    # Secant parameter upper bound and tangent lower bound coincide.
    segre_dimension = 5 * (3 - 1)
    secant_upper_bound = 3 * segre_dimension + (3 - 1)
    secant_tangent_dimension = 33 - 1
    assert segre_dimension == 10
    assert secant_upper_bound == secant_tangent_dimension == 32

    projective_sensor_dimension = 219 - 1
    projective_ambient_dimension = 3**5 - 1
    forced_intersection_dimension = (
        projective_sensor_dimension
        + secant_tangent_dimension
        - projective_ambient_dimension
    )
    assert forced_intersection_dimension == 8

    # Fixed ambient simple-incidence model.  Let tau be the sum of the three
    # pure words.  W is spanned by tau and 218 nonpure coordinate words.  We
    # omit exactly 22 single-flip words, so W+Delta has dimension 221 and the
    # local-orbit normal image is all of its 22-dimensional quotient.
    tau = sum((coordinate_column(word) for word in PURE_WORDS), zeros(243, 1))
    omitted_flips = set(all_flips[:22])
    nonpure_words = tuple(word for word in WORDS if word not in PURE_WORDS)
    included_nonpure = tuple(word for word in nonpure_words if word not in omitted_flips)
    assert len(included_nonpure) == 240 - 22 == 218
    sensor = Matrix.hstack(tau, column_matrix(included_nonpure))
    assert sensor.shape == (243, 219)
    assert sensor.rank() == 219
    assert sensor.row_join(pure_matrix).rank() == 221
    assert sensor.row_join(pure_matrix).row_join(flip_matrix).rank() == 243

    intersection_rank = (
        sensor.rank()
        + pure_matrix.rank()
        + flip_matrix.rank()
        - sensor.row_join(pure_matrix).row_join(flip_matrix).rank()
    )
    # This expression includes Delta separately.  Directly compute the
    # intersection of F with W+Delta from the rank formula.
    w_plus_delta_rank = sensor.row_join(pure_matrix).rank()
    flip_intersection_dimension = (
        flip_matrix.rank()
        + w_plus_delta_rank
        - sensor.row_join(pure_matrix).row_join(flip_matrix).rank()
    )
    assert intersection_rank >= 0
    assert flip_intersection_dimension == 8
    assert 30 - flip_intersection_dimension == 22

    # One- and two-term diagonal targets have only 10 and 20 flip directions.
    for active_colours, expected_dimension in (((0,), 10), ((0, 1), 20)):
        flips = single_flip_words(active_colours)
        assert len(flips) == len(set(flips)) == expected_dimension
        assert column_matrix(flips).rank() == expected_dimension < 22

    # A fixed 3 x 3 basis change audits contraction covariance exactly.
    g = Matrix([[1, 1, 0], [0, 1, 1], [1, 0, 1]])
    assert g.det() == 2
    x = Matrix([1, 1, 1])
    h = Matrix([2, -1, 3])
    transformed_h = g * h
    transformed_x = g.T.inv() * x
    assert (transformed_h.T * transformed_x)[0] == (h.T * x)[0]

    left = Matrix([[1, 0, -1], [0, 1, -1], [1, -1, 0]])
    transformed_left = g * left * g.T
    assert (transformed_x.T * transformed_left * transformed_x)[0] == (
        x.T * left * x
    )[0]

    print("PASS: the diagonal secant tangent has 3 + 30 coordinate directions")
    print("PASS: sigma_3 dimension = 32 and forced sensor intersection >= 8")
    print("PASS: fixed simple-incidence model attains single-flip normal rank 22")
    print("PASS: one/two-term local-basis normal ranks are bounded by 10/20")
    print("PASS: root-local covariance preserves linear and bilinear contractions")
    print("searches=0")
    print("SCOPE: no legal full-rank target-incidence point is constructed")
    print("SCOPE: physical realization and global Krenn-Gu remain UNRESOLVED")


if __name__ == "__main__":
    main()
