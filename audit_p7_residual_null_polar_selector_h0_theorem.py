"""Independent no-import audit of the P7 residual-null polar selector.

The audit uses only exact integer arithmetic.  It checks the termwise
annihilation mechanism, the surviving rank-two matrix, and the rank-three
diagonal target on a torus contraction.  It performs no support search.
"""


def dot(left: tuple[int, ...], right: tuple[int, ...]) -> int:
    return sum(x * y for x, y in zip(left, right, strict=True))


def corrected_pair(
    a_left: tuple[int, ...],
    b_left: tuple[int, ...],
    a_right: tuple[int, ...],
    b_right: tuple[int, ...],
) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(
            a_left[i] * b_right[j] + b_left[i] * a_right[j]
            for j in range(3)
        )
        for i in range(3)
    )


def evaluate_pair(
    a_rows: tuple[tuple[int, ...], ...],
    b_rows: tuple[tuple[int, ...], ...],
    vectors: tuple[tuple[int, ...], ...],
    left: int,
    right: int,
) -> int:
    return (
        dot(a_rows[left], vectors[left]) * dot(b_rows[right], vectors[right])
        + dot(b_rows[left], vectors[left]) * dot(a_rows[right], vectors[right])
    )


def determinant(matrix: tuple[tuple[int, ...], ...]) -> int:
    a, b, c = matrix[0]
    d, e, f = matrix[1]
    g, h, i = matrix[2]
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)


def main() -> None:
    # Select ports 0,1.  Each contracted port uses the torus vector
    # kappa=(1,2,3); both displayed residual covectors annihilate it.
    kappa = (1, 2, 3)
    null_a = (2, -1, 0)
    null_b = (3, 0, -1)
    assert dot(null_a, kappa) == dot(null_b, kappa) == 0

    a_rows = ((1, 0, 2), (0, 1, 1)) + (null_a,) * 5
    b_rows = ((0, 1, 3), (2, -1, 0)) + (null_b,) * 5
    vectors = ((2, 1, -1), (1, -2, 1)) + (kappa,) * 5

    surviving = []
    killed = 0
    for left in range(7):
        for right in range(left + 1, 7):
            value = evaluate_pair(a_rows, b_rows, vectors, left, right)
            if (left, right) == (0, 1):
                assert value != 0
                surviving.append((left, right))
            else:
                assert value == 0
                killed += 1
    assert surviving == [(0, 1)]
    assert killed == 20

    # The surviving open response is a sum of two outer products.  Its
    # determinant vanishes, while a 2 x 2 minor confirms that rank two is
    # genuinely attained in this exact sample.
    response = corrected_pair(a_rows[0], b_rows[0], a_rows[1], b_rows[1])
    assert determinant(response) == 0
    assert response[0][0] * response[1][1] - response[0][1] * response[1][0] != 0

    # Five torus contractions leave a concise diagonal target of rank three.
    # The exact diagonal entries include arbitrary nonzero target weights.
    weights = (2, 3, 5)
    diagonal = tuple(weights[color] * kappa[color] ** 5 for color in range(3))
    target = (
        (diagonal[0], 0, 0),
        (0, diagonal[1], 0),
        (0, 0, diagonal[2]),
    )
    assert determinant(target) == diagonal[0] * diagonal[1] * diagonal[2]
    assert determinant(target) != 0

    # The selector's set-theoretic core is exact for every choice of open
    # pair: a different two-set must meet its five-element complement.
    ports = frozenset(range(7))
    for u in range(7):
        for v in range(u + 1, 7):
            selected = frozenset((u, v))
            contracted = ports - selected
            assert len(contracted) == 5
            for i in range(7):
                for j in range(i + 1, 7):
                    competitor = frozenset((i, j))
                    if competitor != selected:
                        assert competitor & contracted

    assert 7 - 4 == 3
    print("PASS: independent exact residual-null polar-selector audit")
    print("PASS: twenty competing Laplace terms die termwise")
    print("PASS: rank-two selected block versus rank-three torus target")
    print("SCOPE: h!=0 and global Krenn--Gu remain UNRESOLVED")


if __name__ == "__main__":
    main()
