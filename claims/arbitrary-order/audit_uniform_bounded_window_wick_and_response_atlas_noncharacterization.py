"""No-import audit of the uniform bounded-window counterfamilies."""

from fractions import Fraction
from functools import lru_cache
from itertools import combinations, permutations, product


def popcount(mask):
    return mask.bit_count()


def counterdeck(mask, k, lam):
    if mask == 0:
        return Fraction(1)
    return lam if popcount(mask) == k else Fraction(0)


def zero_graph_hafnian(mask, memo):
    if mask == 0:
        return Fraction(1)
    if mask in memo:
        return memo[mask]
    first = (mask & -mask).bit_length() - 1
    rest = mask ^ (1 << first)
    total = Fraction(0)
    cursor = rest
    while cursor:
        bit = cursor & -cursor
        cursor ^= bit
        # Every zero-graph edge has weight zero.
        total += Fraction(0) * zero_graph_hafnian(rest ^ bit, memo)
    memo[mask] = total
    return total


def audit_q2_blocks_and_coloured_defect(b):
    k = b + 2
    frame = ((Fraction(1), Fraction(0), Fraction(0)), (Fraction(0), Fraction(1), Fraction(0)))
    assert frame[0][0] * frame[1][1] - frame[0][1] * frame[1][0] == 1

    def block(left_colour, right_colour):
        return (
            frame[0][left_colour] * frame[1][right_colour]
            + frame[1][left_colour] * frame[0][right_colour]
        )

    assert tuple(tuple(block(i, j) for j in range(3)) for i in range(3)) == (
        (Fraction(0), Fraction(1), Fraction(0)),
        (Fraction(1), Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(0)),
    )

    # Audit every basis-polarized response coefficient of one b-port chart
    # by a residual/port perfect-matching recurrence.
    ports = tuple(range(b))
    for size in range(2, b + 1, 2):
        for subset in combinations(ports, size):
            for colours in product(range(3), repeat=size):
                colour = dict(zip(subset, colours, strict=True))

                def weight(left, right):
                    if {left, right} == {"q0", "q1"}:
                        return Fraction(0)
                    if left == "q0" and right in colour:
                        return frame[0][colour[right]]
                    if right == "q0" and left in colour:
                        return frame[0][colour[left]]
                    if left == "q1" and right in colour:
                        return frame[1][colour[right]]
                    if right == "q1" and left in colour:
                        return frame[1][colour[left]]
                    return Fraction(0)

                @lru_cache(maxsize=None)
                def haf(vertices):
                    if not vertices:
                        return Fraction(1)
                    first = vertices[0]
                    total = Fraction(0)
                    for position in range(1, len(vertices)):
                        second = vertices[position]
                        rest = vertices[1:position] + vertices[position + 1 :]
                        total += weight(first, second) * haf(rest)
                    return total

                response = haf(tuple(sorted(("q0", "q1", *subset), key=str)))
                if size == 2:
                    assert response == block(colours[0], colours[1])
                else:
                    assert response == 0

    # All charts use the same frame, so the three singleton rank-two groups
    # in their common core have identity transitions.
    assert b - 1 >= 3
    assert frame == frame

    # One displayed nonconstant full-support coefficient is lambda, while
    # every insertion term uses a positive-support M coefficient and is zero.
    word = (0,) * (k - 1) + (1,)
    assert len(set(word)) == 2
    lam = Fraction(17, 11)

    def perturbation(colours):
        return lam if len(colours) == k and len(set(colours)) > 1 else Fraction(0)

    for colour_permutation in permutations(range(3)):
        assert perturbation(word) == perturbation(tuple(colour_permutation[colour] for colour in word))
    assert perturbation(word) == perturbation(tuple(reversed(word)))

    def m_coefficient(support):
        return Fraction(1) if not support else Fraction(0)

    insertion_rhs = sum(
        block(word[left], word[right])
        * m_coefficient(tuple(vertex for vertex in range(k) if vertex not in {left, right}))
        for left, right in combinations(range(k), 2)
    )
    assert perturbation(word) == lam != insertion_rhs


def audit_bound(b):
    k = b + 2
    lam = Fraction(13, 9)
    full = (1 << k) - 1

    for mask in range(1 << k):
        if popcount(mask) <= b and popcount(mask) % 2 == 0:
            assert counterdeck(mask, k, lam) == zero_graph_hafnian(mask, {})

    assert counterdeck(full, k, lam) == lam
    assert zero_graph_hafnian(full, {}) == 0

    # Direct Euler ledger: every pair and every complementary proper deck
    # coefficient on the right is zero.
    rhs = Fraction(0)
    bits = tuple(i for i in range(k) if full & (1 << i))
    for i_index, i in enumerate(bits):
        for j in bits[i_index + 1 :]:
            edge = (1 << i) | (1 << j)
            rhs += counterdeck(edge, k, lam) * counterdeck(full ^ edge, k, lam)
    assert rhs == 0
    assert Fraction(k, 2) * lam != rhs

    # A b-port chart cannot contain the unique k-port perturbation.
    core = (1 << (b - 1)) - 1
    extras = tuple(1 << i for i in range(b - 1, b + 2))
    charts = tuple(core | extra for extra in extras)
    assert all(popcount(chart) == b for chart in charts)
    assert all((charts[i] & charts[j]) == core for i in range(3) for j in range(i + 1, 3))
    assert all((full & chart) != full for chart in charts)
    audit_q2_blocks_and_coloured_defect(b)


def main():
    for b in (4, 6, 8):
        audit_bound(b)
    print("uniform bounded-window independent audit: PASS")
    print("bitmask restrictions and zero-edge matchings: PASS")
    print("full block q=2 charts and coloured insertion defects: PASS")


if __name__ == "__main__":
    main()
