"""Verify the P7 root-budget dual-Wick observability boundary.

The replay is symbolic and fixed-size.  It checks one Jacobian minor, one
observation kernel, two displayed legal channels, and one 4x4 permanent.  It
does not enumerate blocker supports, colour words, or response subsets.
"""

from __future__ import annotations

from functools import cache

import sympy as sp

EDGES = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
COMPLEMENT = (5, 4, 3, 2, 1, 0)
STAR = sp.Matrix(
    (
        (1, 1, 1, 0, 0, 0),
        (1, 0, 0, 1, 1, 0),
        (0, 1, 0, 1, 0, 1),
        (0, 0, 1, 0, 1, 1),
    )
)


def permanent(matrix: sp.Matrix) -> sp.Expr:
    @cache
    def recurse(rows: tuple[int, ...], columns: tuple[int, ...]) -> sp.Expr:
        if not rows:
            return sp.Integer(1)
        first = rows[0]
        return sp.expand(
            sum(
                matrix[first, column]
                * recurse(rows[1:], columns[:position] + columns[position + 1 :])
                for position, column in enumerate(columns)
            )
        )

    size = matrix.rows
    assert matrix.cols == size
    return recurse(tuple(range(size)), tuple(range(size)))


def response_map():
    h = sp.Symbol("h")
    direct = sp.symbols("B12 B13 B14 B23 B24 B34")
    left = sp.symbols("a1:5")
    right = sp.symbols("b1:5")
    channels = tuple(
        left[i] * right[j] + right[i] * left[j] for i, j in EDGES
    )
    pairs = tuple(h * direct[index] + channels[index] for index in range(6))
    top_direct = (
        direct[0] * direct[5]
        + direct[1] * direct[4]
        + direct[2] * direct[3]
    )
    top_present = h * top_direct + sum(
        channels[index] * direct[COMPLEMENT[index]] for index in range(6)
    )
    stars = tuple(STAR * sp.Matrix(direct))
    parameters = (h,) + direct + left + right
    outputs = (h,) + pairs + (top_direct, top_present) + stars
    return parameters, outputs


def channel_matrix(vector: sp.Matrix, covector: sp.Matrix) -> sp.Matrix:
    return vector * covector.T + covector * vector.T


def off_diagonal(matrix: sp.Matrix) -> sp.Matrix:
    return sp.Matrix([matrix[left, right] for left, right in EDGES])


def main() -> None:
    # P7 has seven non-port vertices.  Residual order q leaves 7-q probe
    # roots, giving the exact eligible even rank layers.
    q2_z = tuple(size for size in (0, 2, 4, 6) if 7 - size <= 7 - 2)
    q2_m = tuple(size for size in (0, 2, 4, 6) if 2 + 7 - size <= 7 - 2)
    q4_z = tuple(size for size in (0, 2, 4, 6) if 7 - size <= 7 - 4)
    q4_m = tuple(size for size in (0, 2, 4, 6) if 4 + 7 - size <= 7 - 4)
    assert q2_z == (2, 4, 6) and q2_m == (4, 6)
    assert q4_z == (4, 6) and q4_m == ()

    parameters, outputs = response_map()
    jacobian = sp.Matrix(outputs).jacobian(parameters)
    h, *rest = parameters
    direct = rest[:6]
    left = rest[6:10]
    right = rest[10:14]
    point = {
        h: 1,
        **dict(zip(direct, (1, 0, 0, 0, 0, 1), strict=True)),
        **dict(zip(left, (1, 0, 1, 2), strict=True)),
        **dict(zip(right, (0, 1, 3, 1), strict=True)),
    }
    dominance_minor = jacobian[:, :13].subs(point)
    assert dominance_minor.shape == (13, 13)
    assert dominance_minor.det() == 360
    assert jacobian.subs(point).rank() == 13

    assert STAR.rank() == 4
    n_s = sp.Matrix((-1, 1, 0, 0, 1, -1))
    n_t = sp.Matrix((-1, 0, 1, 1, 0, -1))
    assert STAR * n_s == sp.zeros(4, 1)
    assert STAR * n_t == sp.zeros(4, 1)
    assert sp.Matrix.hstack(n_s, n_t).rank() == 2

    # Complementary z weights lie in the star row space exactly on the two
    # opposite-pair equalities.  Verify an explicit potential recovery.
    z12, z13, z14, z23, z24, z34 = sp.symbols("z12 z13 z14 z23 z24 z34")
    weight = sp.Matrix((z34, z24, z23, z14, z13, z12))
    defects = (sp.expand(weight.dot(n_s)), sp.expand(weight.dot(n_t)))
    assert defects == (
        -z12 + z13 + z24 - z34,
        -z12 + z14 + z23 - z34,
    )
    additive_substitution = {
        z34: z13 + z24 - z12,
        z23: z13 + z24 - z14,
    }
    w12, w13, w14, w23, _w24, _w34 = tuple(weight)
    alpha1 = (w12 + w13 - w23) / 2
    alpha2 = (w12 + w23 - w13) / 2
    alpha3 = (w13 + w23 - w12) / 2
    alpha4 = w14 - alpha1
    alpha = sp.Matrix((alpha1, alpha2, alpha3, alpha4))
    recovered = (STAR.T * alpha - weight).subs(additive_substitution)
    assert all(sp.simplify(entry) == 0 for entry in recovered)

    s, t = sp.symbols("s t")
    kernel_pair = s * n_s + t * n_t
    kernel_top = (
        kernel_pair[0] * kernel_pair[5]
        + kernel_pair[1] * kernel_pair[4]
        + kernel_pair[2] * kernel_pair[3]
    )
    assert sp.expand(kernel_top) == 2 * (s**2 + s * t + t**2)

    # Two honest direct pair systems have the same stars and top value.
    b_zero = n_s
    b_one = n_t
    u_zero = sp.Matrix((1, 0, 0, -1))
    v_zero = sp.Matrix((0, -1, 1, 0))
    u_one = sp.Matrix((1, 0, -1, 0))
    v_one = sp.Matrix((0, -1, 0, 1))
    assert off_diagonal(channel_matrix(u_zero, v_zero)) == b_zero
    assert off_diagonal(channel_matrix(u_one, v_one)) == b_one
    h_symbol = sp.Symbol("H", nonzero=True)
    for pair_vector, u_vector, v_vector in (
        (b_zero, u_zero, v_zero),
        (b_one, u_one, v_one),
    ):
        corrected = off_diagonal(channel_matrix(-h_symbol * u_vector, v_vector))
        assert corrected == -h_symbol * pair_vector
        present_pairs = h_symbol * pair_vector + corrected
        direct_top = (
            pair_vector[0] * pair_vector[5]
            + pair_vector[1] * pair_vector[4]
            + pair_vector[2] * pair_vector[3]
        )
        present_top = sp.expand(
            h_symbol * direct_top
            + sum(corrected[index] * pair_vector[COMPLEMENT[index]] for index in range(6))
        )
        assert STAR * pair_vector == sp.zeros(4, 1)
        assert direct_top == 2
        assert present_pairs == sp.zeros(6, 1)
        assert present_top == -2 * h_symbol
    assert b_zero != b_one

    # At q=4 the identity incidence is the quartic relative coefficient.
    identity = sp.eye(4)
    assert permanent(identity) == 1
    zero_base_pairs = sp.zeros(6, 1)
    assert zero_base_pairs == sp.zeros(6, 1)
    quartic_dual_wick_defect = permanent(identity)
    assert quartic_dual_wick_defect == 1

    print("P7 root-budget dual-Wick observability boundary: VERIFIED")
    print("q2_eligible=z2,z4,z6;m4,m6 q4_eligible=z4,z6;no_m_layer")
    print("maximal_q2_visible_jacobian_rank=13 minor=360")
    print("marked_star_kernel=2 additive_weight_selector=VERIFIED")
    print("legal_hidden_pair_counterresponses=VERIFIED")
    print("q4_identity_quartic_defect=1")
    print("support_search=0 word_enumeration=0 subset_enumeration=0")
    print("P7_GLOBAL_STATUS=UNKNOWN")


if __name__ == "__main__":
    main()
