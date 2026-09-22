"""Finite replay of the explicit all-order literal-triangle witness."""

from itertools import permutations, product


def construct(k, c):
    """p is i -> i+1, triangle is 0_0--1_1--2_c--0_0."""
    assert c not in (0, 1)
    return tuple(1 if i == 0 or i > c else 2 if i == c else 0
                 for i in range(k))


def independent(word, q, r):
    k = len(word)
    return (
        all(not (word[i] == 0 and word[(i + 1) % k] == 1)
            for i in range(k))
        and all(not (word[i] == 0 and word[q[i]] == 2)
                for i in range(k))
        and all(not (word[i] == 1 and word[r[i]] == 2)
                for i in range(k))
    )


def main():
    total_pairs = 0
    total_triangles = 0
    for k in range(3, 7):
        derangements = [p for p in permutations(range(k))
                        if all(p[i] != i for i in range(k))]
        pairs = triangles = 0
        for q, r in product(derangements, repeat=2):
            pairs += 1
            for c in range(2, k):
                # q(0)=c and r(1)=c is precisely the normalized triangle.
                if q[0] != c or r[1] != c:
                    continue
                triangles += 1
                word = construct(k, c)
                assert len(set(word)) == 3
                assert independent(word, q, r)
        total_pairs += pairs
        total_triangles += triangles
        print(f"k={k} permutation_pairs={pairs} triangles={triangles}")
    print(f"TRIANGLE_WITNESS_REPLAY_PASS pairs={total_pairs} "
          f"triangles={total_triangles}")


if __name__ == "__main__":
    main()
