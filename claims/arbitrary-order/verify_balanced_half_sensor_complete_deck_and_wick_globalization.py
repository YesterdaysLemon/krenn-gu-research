"""Focused exact checks for the balanced half-sensor theorem.

The arbitrary-order proof is the matching bijection in the owning note.  This
script checks its conventions on fixed small integer instances and checks the
explicit rank and target-disjoint charts without enumerating graph families.
"""

from fractions import Fraction
from itertools import combinations, permutations, product


def double_factorial_odd(size: int) -> int:
    """Return (size-1)!! for an even nonnegative size."""
    assert size >= 0 and size % 2 == 0
    answer = 1
    for value in range(1, size, 2):
        answer *= value
    return answer


def hafnian(vertices: tuple[int, ...], edge) -> int:
    if not vertices:
        return 1
    first = vertices[0]
    total = 0
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        total += edge(first, second) * hafnian(rest, edge)
    return total


def block_entry(u: int, v: int, a: int, b: int) -> int:
    """One deterministic integral physical block, with u<v."""
    assert u < v
    return (u + 2) * (a + 1) + (v + 3) * (b + 2) + (a + 1) * (b + 1)


def bilinear(u: int, v: int, x: tuple[int, ...], y: tuple[int, ...]) -> int:
    if u > v:
        return bilinear(v, u, y, x)
    return sum(
        x[a] * y[b] * block_entry(u, v, a, b)
        for a in range(3)
        for b in range(3)
    )


def basis(colour: int) -> tuple[int, int, int]:
    return tuple(int(index == colour) for index in range(3))


def subset_tuples(items: tuple[int, ...], size: int):
    yield from combinations(items, size)


def companion_value(
    roots: tuple[int, ...],
    nonroots: tuple[int, ...],
    deletion: tuple[int, ...],
    root_word: tuple[int, ...],
    local_vectors: dict[int, tuple[int, ...]],
) -> int:
    """Evaluate G_D by its U/bijection/root-matching definition."""
    root_vector = {root: basis(root_word[pos]) for pos, root in enumerate(roots)}
    total = 0
    for unmatched in subset_tuples(roots, len(deletion)):
        unmatched_set = set(unmatched)
        remaining = tuple(root for root in roots if root not in unmatched_set)

        def root_edge(left: int, right: int) -> int:
            return bilinear(left, right, root_vector[left], root_vector[right])

        root_hafnian = hafnian(remaining, root_edge)
        for targets in permutations(deletion):
            cross = 1
            for root, target in zip(unmatched, targets, strict=True):
                cross *= bilinear(
                    root,
                    target,
                    root_vector[root],
                    local_vectors[target],
                )
            total += cross * root_hafnian
    return total


def check_matching_partition() -> None:
    for m in range(1, 5):
        roots = tuple(range(m))
        nonroots = tuple(range(m, 2 * m))
        local_vectors = {
            vertex: (vertex + 1, 2 * vertex + 1, vertex * vertex + 1)
            for vertex in nonroots
        }
        for root_word in product(range(3), repeat=m):
            vectors = {
                **local_vectors,
                **{root: basis(root_word[pos]) for pos, root in enumerate(roots)},
            }

            def full_edge(
                left: int,
                right: int,
                current_vectors=vectors,
            ) -> int:
                return bilinear(
                    left,
                    right,
                    current_vectors[left],
                    current_vectors[right],
                )

            direct = hafnian(tuple(range(2 * m)), full_edge)
            reconstructed = 0
            for size in range(0, m + 1, 2):
                for present in combinations(nonroots, size):
                    present_set = set(present)
                    deletion = tuple(v for v in nonroots if v not in present_set)

                    def nonroot_edge(
                        left: int,
                        right: int,
                        current_vectors=local_vectors,
                    ) -> int:
                        return bilinear(
                            left,
                            right,
                            current_vectors[left],
                            current_vectors[right],
                        )

                    deck = hafnian(present, nonroot_edge)
                    companion = companion_value(
                        roots,
                        nonroots,
                        deletion,
                        root_word,
                        local_vectors,
                    )
                    reconstructed += companion * deck
            assert reconstructed == direct, (m, root_word, direct, reconstructed)


def check_rank_and_target_charts() -> None:
    for m in range(1, 8):
        parity_words = {
            tuple(int(index in deletion) for index in range(m))
            for size in range(m % 2, m + 1, 2)
            for deletion in combinations(range(m), size)
        }
        assert len(parity_words) == 2 ** (m - 1)
        for word in parity_words:
            coefficient = double_factorial_odd(m - sum(word))
            assert coefficient != 0

    coordinate_pairs = ((0, 1), (1, 2), (2, 0))
    for m in range(3, 9):
        words = set()
        for size in range(m % 2, m + 1, 2):
            for deletion in combinations(range(m), size):
                deletion_set = set(deletion)
                word = tuple(
                    coordinate_pairs[index % 3][int(index not in deletion_set)]
                    for index in range(m)
                )
                words.add(word)
        assert len(words) == 2 ** (m - 1)
        for colour in range(3):
            assert (colour,) * m not in words


def square_zero_product(left, right):
    answer: dict[int, Fraction] = {}
    for left_mask, left_value in left.items():
        for right_mask, right_value in right.items():
            if left_mask & right_mask:
                continue
            mask = left_mask | right_mask
            answer[mask] = answer.get(mask, Fraction()) + left_value * right_value
    return answer


def check_scalar_wick_convention() -> None:
    size = 6

    def scalar_edge(left: int, right: int) -> int:
        if left > right:
            left, right = right, left
        return (left + 2) * (right + 3) - 1

    moment: dict[int, Fraction] = {0: Fraction(1)}
    for mask in range(1, 1 << size):
        vertices = tuple(index for index in range(size) if mask & (1 << index))
        if len(vertices) % 2 == 0:
            moment[mask] = Fraction(hafnian(vertices, scalar_edge))

    positive = {mask: value for mask, value in moment.items() if mask}
    logarithm: dict[int, Fraction] = {}
    power = positive
    for exponent in range(1, size + 1):
        sign = 1 if exponent % 2 else -1
        for mask, value in power.items():
            logarithm[mask] = logarithm.get(mask, Fraction()) + sign * value / exponent
        power = square_zero_product(power, positive)

    for mask, value in logarithm.items():
        degree = mask.bit_count()
        if degree == 2:
            left, right = (index for index in range(size) if mask & (1 << index))
            assert value == scalar_edge(left, right)
        else:
            assert value == 0, (mask, value)


def main() -> None:
    check_matching_partition()
    check_rank_and_target_charts()
    check_scalar_wick_convention()
    print("balanced half-sensor focused verification: PASS")
    print("matching identity checked through n=8 with exact integer arithmetic")
    print("rank words through m=7; target-disjoint words through m=8")
    print("global conjecture status: UNRESOLVED")


if __name__ == "__main__":
    main()
