"""Independent no-import audit of the synchronized-top shore boundary."""

from __future__ import annotations

from fractions import Fraction

Polynomial = dict[int, Fraction]


def multiply_square_zero(left: Polynomial, right: Polynomial) -> Polynomial:
    """Multiply port polynomials encoded by square-free bit masks."""

    answer: Polynomial = {}
    for left_mask, left_value in left.items():
        for right_mask, right_value in right.items():
            if left_mask & right_mask:
                continue
            mask = left_mask | right_mask
            answer[mask] = answer.get(mask, Fraction(0)) + left_value * right_value
    return {mask: value for mask, value in answer.items() if value}


def determinant_2(matrix: tuple[tuple[Fraction, Fraction], ...]) -> Fraction:
    """Return an exact two-by-two determinant."""

    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def multiply_2(
    left: tuple[tuple[Fraction, Fraction], ...],
    right: tuple[tuple[Fraction, Fraction], ...],
) -> tuple[tuple[Fraction, Fraction], ...]:
    """Multiply exact two-by-two matrices."""

    return tuple(
        tuple(
            sum(left[i][k] * right[k][j] for k in range(2))
            for j in range(2)
        )
        for i in range(2)
    )


def transpose_2(
    matrix: tuple[tuple[Fraction, Fraction], ...],
) -> tuple[tuple[Fraction, Fraction], ...]:
    """Transpose an exact two-by-two matrix."""

    return tuple(tuple(matrix[j][i] for j in range(2)) for i in range(2))


def audit_endpoint_rank() -> None:
    """Audit the exchange-rank transfer independently."""

    left = ((Fraction(1), Fraction(2)), (Fraction(3), Fraction(5)))
    right = ((Fraction(2), Fraction(-1)), (Fraction(1), Fraction(3)))
    exchange = ((Fraction(0), Fraction(1)), (Fraction(1), Fraction(0)))
    response = multiply_2(multiply_2(left, exchange), transpose_2(right))

    assert determinant_2(left) != 0
    assert determinant_2(right) != 0
    assert determinant_2(response) == -determinant_2(left) * determinant_2(right)
    assert determinant_2(response) != 0


def audit_line_observation() -> None:
    """Audit one visible and eight invisible matrix coordinates."""

    visible = (0, 0)
    coordinates = [(row, column) for row in range(3) for column in range(3)]
    invisible = [coordinate for coordinate in coordinates if coordinate != visible]

    assert len(coordinates) == 9
    assert len(invisible) == 8
    assert all(coordinate != visible for coordinate in invisible)


def audit_response_fibre() -> None:
    """Audit the exact square-zero response for several rational fibres."""

    empty = 0
    pair_12 = (1 << 0) | (1 << 1)
    pair_34 = (1 << 2) | (1 << 3)
    top = pair_12 | pair_34
    h = Fraction(5, 3)

    observed_top_pairs: set[tuple[Fraction, Fraction, Fraction]] = set()
    hidden_pairs: set[tuple[Fraction, Fraction]] = set()
    for a in (Fraction(2), Fraction(-3, 2), Fraction(7, 5)):
        direct = {empty: Fraction(1), pair_34: a}
        relative = {empty: h, pair_12: 1 / a}
        residual_present = multiply_square_zero(direct, relative)

        m_top = direct.get(top, Fraction(0))
        z_top = residual_present.get(top, Fraction(0))
        corrected_top = z_top - h * m_top
        corrected_pair = residual_present[pair_12] - h * direct.get(
            pair_12, Fraction(0)
        )

        assert residual_present[empty] == h
        assert residual_present[pair_34] == h * a
        assert corrected_pair == 1 / a
        assert direct[pair_34] * corrected_pair == 1
        observed_top_pairs.add((m_top, z_top, corrected_top))
        hidden_pairs.add((direct[pair_34], corrected_pair))

    assert observed_top_pairs == {(Fraction(0), Fraction(1), Fraction(1))}
    assert len(hidden_pairs) == 3


def main() -> None:
    audit_endpoint_rank()
    audit_line_observation()
    audit_response_fibre()
    print("PASS: independent synchronized-top shore-line boundary audit")
    print("strict endpoint transfer rank: 2")
    print("shore-line visible coordinates: 1 of 9")
    print("shore-line invisible coordinates: 8 of 9")
    print("exact rational response fibres: 3")
    print("support searches: 0")
    print("full corrected determinant activated: no")
    print("global Krenn-Gu status: UNRESOLVED")


if __name__ == "__main__":
    main()
