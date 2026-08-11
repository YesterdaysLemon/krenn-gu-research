"""Verify the transverse q=0, r=4 two-open detector ingredients."""

from __future__ import annotations

from itertools import permutations, product

import sympy as sp

Word = tuple[int, int, int, int]


def collision_matrix(
    a: tuple[sp.Matrix, ...], b: tuple[sp.Matrix, ...]
) -> tuple[sp.Matrix, tuple[Word, ...]]:
    """Return the matrix h -> P4(h,a,a,b) in standard coordinates."""
    words = tuple(product(range(3), repeat=4))
    columns: list[list[sp.Expr]] = []
    for active_mode in range(4):
        for component in range(3):
            h = [sp.zeros(3, 1) for _ in range(4)]
            h[active_mode][component] = 1
            column: list[sp.Expr] = []
            for word in words:
                rows = (tuple(h), a, a, b)
                value = sp.Integer(0)
                for assignment in permutations(range(4)):
                    value += sp.prod(
                        rows[row][mode][word[mode]]
                        for row, mode in enumerate(assignment)
                    )
                column.append(sp.expand(value))
            columns.append(column)
    return sp.Matrix.hstack(*(sp.Matrix(column) for column in columns)), words


def check_selected_minor() -> None:
    """Check the twelve coefficient selectors from the written proof."""
    e0, e1 = sp.eye(3).row(0).T, sp.eye(3).row(1).T
    matrix, words = collision_matrix((e0,) * 4, (e1,) * 4)

    z_words = []
    for mode in range(4):
        word = [0, 0, 0, 0]
        word[mode] = 2
        word[(mode + 1) % 4] = 1
        z_words.append(tuple(word))
    y_words = []
    for first, second in ((0, 1), (0, 2), (0, 3), (1, 2)):
        word = [0, 0, 0, 0]
        word[first] = word[second] = 1
        y_words.append(tuple(word))
    x_words = []
    for mode in range(4):
        word = [0, 0, 0, 0]
        word[mode] = 1
        x_words.append(tuple(word))

    selected_rows = [words.index(word) for word in z_words + y_words + x_words]
    selected_columns = (
        [3 * mode + 2 for mode in range(4)]
        + [3 * mode + 1 for mode in range(4)]
        + [3 * mode for mode in range(4)]
    )
    minor = matrix.extract(selected_rows, selected_columns)
    assert matrix.shape == (81, 12)
    assert matrix.rank() == 12
    assert abs(int(minor.det())) == 24576


def check_exact_transverse_charts() -> None:
    """Replay injectivity after deterministic local coordinate changes."""
    charts = (
        (
            sp.Matrix(((1, 1, 0), (0, 1, 1), (1, 0, 1))),
            sp.Matrix(((2, 0, 1), (1, 1, 0), (0, 1, 1))),
            sp.Matrix(((1, 2, 0), (0, 1, 1), (1, 0, 2))),
            sp.Matrix(((1, 0, 1), (2, 1, 0), (0, 1, 2))),
        ),
        (
            sp.Matrix(((1, 0, 2), (1, 1, 0), (0, 1, 1))),
            sp.Matrix(((1, 2, 1), (0, 1, 1), (1, 0, 1))),
            sp.Matrix(((2, 1, 0), (0, 1, 2), (1, 0, 1))),
            sp.Matrix(((1, 1, 0), (1, 0, 2), (0, 1, 1))),
        ),
    )
    for local_matrices in charts:
        assert all(matrix.det() != 0 for matrix in local_matrices)
        a = tuple(matrix[:, 0] for matrix in local_matrices)
        b = tuple(matrix[:, 1] for matrix in local_matrices)
        matrix, _ = collision_matrix(a, b)
        assert matrix.rank() == 12


def check_dependent_boundary() -> None:
    """Check that dependence is a boundary, not an exact kernel criterion."""
    e0, e1 = sp.eye(3).row(0).T, sp.eye(3).row(1).T
    a = (e0,) * 4

    one_dependent, _ = collision_matrix(a, (e0, e1, e1, e1))
    assert one_dependent.rank() == 12

    b = (e0, e0, e1, e1)
    matrix, _ = collision_matrix(a, b)
    kernel_vector = sp.Matrix((-1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0))
    assert matrix.rank() == 10
    assert kernel_vector != sp.zeros(12, 1)
    assert matrix * kernel_vector == sp.zeros(81, 1)


def check_companion_basis_deletion() -> None:
    """Check every small rank-two 2x3 companion frame has a basis pair."""
    checked = 0
    pairwise_frames = 0
    for entries in product((-1, 0, 1), repeat=6):
        frame = sp.Matrix(2, 3, entries)
        if frame.rank() != 2:
            continue
        checked += 1
        nonzero_minors = []
        for first, second in ((0, 1), (0, 2), (1, 2)):
            nonzero_minors.append(frame[:, (first, second)].det() != 0)
        assert any(nonzero_minors)
        if all(nonzero_minors):
            pairwise_frames += 1
    assert checked == 624
    assert pairwise_frames > 0


def main() -> None:
    check_selected_minor()
    check_exact_transverse_charts()
    check_dependent_boundary()
    check_companion_basis_deletion()
    print("PASS: normalized four-mode collision matrix has rank 12 of 12")
    print("PASS: selector minor has absolute determinant 24576")
    print("PASS: deterministic exact transverse charts retain rank 12")
    print("PASS: one dependent pair can retain rank 12")
    print("PASS: two dependent pairs can produce an explicit nonzero kernel")
    print("PASS: every audited rank-two companion triple has a basis deletion")
    print("SCOPE: q=0 r=4 aligned projective cell with local transversality")
    print("SCOPE: detector nonzero, not proved injective and not a witness exclusion")
    print("searches=0")


if __name__ == "__main__":
    main()
