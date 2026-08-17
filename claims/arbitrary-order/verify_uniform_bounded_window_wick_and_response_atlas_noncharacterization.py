"""Primary exact checks for the uniform bounded-window noncharacterization."""

from fractions import Fraction
from itertools import combinations, permutations, product


def subsets_of_size(vertices: tuple[int, ...], size: int):
    return combinations(vertices, size)


def deck_value(subset: tuple[int, ...], k: int, lam: Fraction) -> Fraction:
    if not subset:
        return Fraction(1)
    return lam if len(subset) == k else Fraction(0)


def check_scalar_bound(b: int) -> None:
    k = b + 2
    lam = Fraction(7, 5)
    vertices = tuple(range(k))

    for size in range(b + 1):
        for subset in subsets_of_size(vertices, size):
            if len(subset) % 2 == 0:
                assert deck_value(subset, k, lam) == (1 if not subset else 0)

    q = vertices
    s = k // 2
    rhs = sum(
        deck_value(edge, k, lam)
        * deck_value(tuple(v for v in q if v not in edge), k, lam)
        for edge in combinations(q, 2)
    )
    assert s * deck_value(q, k, lam) != rhs
    assert rhs == 0


def matmul(left, right):
    return tuple(
        tuple(sum(left[i][t] * right[t][j] for t in range(len(right))) for j in range(len(right[0])))
        for i in range(len(left))
    )


def transpose(matrix):
    return tuple(zip(*matrix, strict=True))


def check_q2_atlas(b: int) -> None:
    k = b + 2
    core = tuple(range(b - 1))
    extras = tuple(range(b - 1, b + 2))
    charts = tuple(core + (extra,) for extra in extras)
    assert all(len(chart) == b for chart in charts)
    assert all(set(charts[i]) & set(charts[j]) == set(core) for i, j in combinations(range(3), 2))

    p = ((Fraction(1), Fraction(0), Fraction(0)), (Fraction(0), Fraction(1), Fraction(0)))
    j = ((Fraction(0), Fraction(1)), (Fraction(1), Fraction(0)))
    block = matmul(matmul(transpose(p), j), p)
    assert block == (
        (Fraction(0), Fraction(1), Fraction(0)),
        (Fraction(1), Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(0)),
    )
    assert len(core) >= 3
    assert p[0][0] * p[1][1] - p[0][1] * p[1][0] == 1

    full_support = frozenset(range(k))
    for chart in charts:
        assert not full_support.issubset(chart)

    lam = Fraction(11, 7)

    def perturbation(word):
        return lam if len(word) == k and len(set(word)) > 1 else Fraction(0)

    for word in product(range(3), repeat=k):
        value = perturbation(word)
        assert value == perturbation(tuple(reversed(word)))
        for colour_permutation in permutations(range(3)):
            assert value == perturbation(tuple(colour_permutation[colour] for colour in word))

    word = (0,) * (k - 1) + (1,)

    def m_coefficient(support):
        return Fraction(1) if not support else Fraction(0)

    def n_pair(left, right):
        return block[word[left]][word[right]]

    insertion_rhs = sum(
        n_pair(left, right)
        * m_coefficient(tuple(vertex for vertex in range(k) if vertex not in {left, right}))
        for left, right in combinations(range(k), 2)
    )
    assert perturbation(word) == lam != insertion_rhs


def main() -> None:
    for b in (2, 4, 6, 8):
        check_scalar_bound(b)
    for b in (4, 6):
        check_q2_atlas(b)
    print("uniform bounded-window primary checks: PASS")
    print("first unseen Euler and q=2 insertion defects: PASS")
    print("identifying trivial-holonomy local atlases: PASS")


if __name__ == "__main__":
    main()
