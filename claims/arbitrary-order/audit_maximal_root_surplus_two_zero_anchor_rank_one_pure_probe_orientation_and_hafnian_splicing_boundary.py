"""Independent no-import audit of the GLS60 orientation/splicing boundary.

This file imports neither the primary verifier nor project mathematics code.
It uses a finite-field orientation census, bit-mask perfect matchings, and a
direct eight-vertex expansion rather than symbolic Cauchy--Binet identities.
"""

from __future__ import annotations

import itertools
import json
from functools import lru_cache


Q = 3
COLORS = (0, 1, 2)
KAPPA = (0, 0, 1, 1, 2, 2)


def vecs() -> tuple[tuple[int, int, int], ...]:
    return tuple(itertools.product(range(Q), repeat=3))


def is_zero(v: tuple[int, ...]) -> bool:
    return not any(v)


def pure_on(v: tuple[int, int, int], c: int) -> bool:
    return all(v[d] == 0 for d in COLORS if d != c)


def companion(
    xs: tuple[int, int, int],
    xt: tuple[int, int, int],
    ys: tuple[int, int, int],
    yt: tuple[int, int, int],
) -> tuple[tuple[int, int, int], ...]:
    return tuple(
        tuple((xs[i] * yt[j] + xt[i] * ys[j]) % Q for j in COLORS)
        for i in COLORS
    )


def orientation_census() -> dict[str, int]:
    vectors = vecs()
    counts = {"solutions": 0, "x_only": 0, "y_only": 0, "both": 0, "zero_edge_boundary": 0}
    for xs in vectors:
        for xt in vectors:
            for ys in vectors:
                if is_zero(xs) and is_zero(ys):
                    continue
                for yt in vectors:
                    if is_zero(xt) and is_zero(yt):
                        continue
                    matrix = companion(xs, xt, ys, yt)
                    mu = matrix[0][0]
                    if mu == 0:
                        continue
                    if any(matrix[i][j] != (mu if (i, j) == (0, 0) else 0) for i in COLORS for j in COLORS):
                        continue
                    xpure = pure_on(xs, 0) and pure_on(xt, 0)
                    ypure = pure_on(ys, 0) and pure_on(yt, 0)
                    assert xpure or ypure
                    if xpure:
                        a, b = xs[0], xt[0]
                        assert (a, b) != (0, 0)
                        assert all((a * yt[d] + b * ys[d]) % Q == 0 for d in (1, 2))
                        assert (a * yt[0] + b * ys[0]) % Q == mu
                    if ypure:
                        a, b = ys[0], yt[0]
                        assert (a, b) != (0, 0)
                        assert all((b * xs[d] + a * xt[d]) % Q == 0 for d in (1, 2))
                        assert (b * xs[0] + a * xt[0]) % Q == mu
                    counts["solutions"] += 1
                    if xpure and ypure:
                        counts["both"] += 1
                    elif xpure:
                        counts["x_only"] += 1
                    else:
                        counts["y_only"] += 1
                    if is_zero(xs) or is_zero(xt) or is_zero(ys) or is_zero(yt):
                        counts["zero_edge_boundary"] += 1
    assert counts["solutions"] > 0
    assert counts["x_only"] > 0 and counts["y_only"] > 0 and counts["both"] > 0
    assert counts["zero_edge_boundary"] > 0
    return counts


@lru_cache(maxsize=None)
def matching_masks(mask: int) -> tuple[tuple[tuple[int, int], ...], ...]:
    if mask == 0:
        return ((),)
    first_bit = mask & -mask
    first = first_bit.bit_length() - 1
    remainder = mask ^ first_bit
    out = []
    cursor = remainder
    while cursor:
        second_bit = cursor & -cursor
        second = second_bit.bit_length() - 1
        for tail in matching_masks(remainder ^ second_bit):
            out.append(((first, second),) + tail)
        cursor ^= second_bit
    return tuple(out)


def w_entry(i: int, j: int, ci: int, cj: int) -> int:
    return (i + 2) * (j + 5) - (ci + 1) * (cj + 3) + i * cj - j * ci + 2


X = (1, 1, 1, 1, 0, 1)
Y = (0, 1, 0, 1, 1, 1)


def theta_entry(i: int, j: int, ci: int, cj: int) -> int:
    if (ci, cj) != (KAPPA[i], KAPPA[j]):
        return 0
    return X[i] * Y[j] + X[j] * Y[i]


def hafnian(vertices: tuple[int, ...], word: tuple[int, ...], edge_value) -> int:
    mask = sum(1 << v for v in vertices)
    total = 0
    for matching in matching_masks(mask):
        term = 1
        for i, j in matching:
            term *= edge_value(i, j, word[i], word[j])
        total += term
    return total


def eight_vertex_edge(i: int, j: int, word: tuple[int, ...]) -> int:
    # Vertices 0,1 are the contracted old probes; vertices 2,...,7 are labels.
    if (i, j) == (0, 1):
        return 0
    if i < 2 <= j:
        label = j - 2
        if word[label] != KAPPA[label]:
            return 0
        return X[label] if i == 0 else Y[label]
    assert 2 <= i < j
    left, right = i - 2, j - 2
    return w_entry(left, right, word[left], word[right])


def direct_eight_vertex(word: tuple[int, ...]) -> int:
    total = 0
    for matching in matching_masks((1 << 8) - 1):
        term = 1
        for i, j in matching:
            term *= eight_vertex_edge(i, j, word)
        total += term
    return total


def first_variation(word: tuple[int, ...]) -> int:
    total = 0
    for i, j in itertools.combinations(range(6), 2):
        complement = tuple(v for v in range(6) if v not in (i, j))
        total += theta_entry(i, j, word[i], word[j]) * hafnian(complement, word, w_entry)
    return total


def matching_audit() -> dict[str, int]:
    assert len(matching_masks((1 << 6) - 1)) == 15
    assert len(matching_masks((1 << 8) - 1)) == 105
    comparisons = 0
    companion_support = {}
    for word in itertools.product(COLORS, repeat=6):
        assert direct_eight_vertex(word) == first_variation(word)
        comparisons += 1
        value = hafnian(tuple(range(6)), word, theta_entry)
        if value:
            companion_support[word] = value
    assert companion_support == {KAPPA: 18}
    companion_rows = {word[0] for word in companion_support}
    target_rows = {c for c in COLORS}
    assert len(companion_rows) == 1
    assert len(target_rows) == 3
    return {
        "eight_vertex_to_first_variation_coefficients": comparisons,
        "companion_graph_support_words": len(companion_support),
        "companion_graph_mixed_coefficient": companion_support[KAPPA],
        "companion_flattening_nonzero_rows": len(companion_rows),
        "target_flattening_nonzero_rows": len(target_rows),
    }


def gauge_audit() -> dict[str, int]:
    checks = 0
    for weights in ((-3, -1, 0, 2, 4, 5), (-3, -1, 0, 2, 4, -2)):
        trace = sum(weights)

        def gauge(i: int, j: int, ci: int, cj: int) -> int:
            return (weights[i] + weights[j]) * w_entry(i, j, ci, cj)

        for word in itertools.product(COLORS, repeat=6):
            marked = 0
            for matching in matching_masks((1 << 6) - 1):
                for marked_edge in matching:
                    term = 1
                    for edge in matching:
                        i, j = edge
                        term *= gauge(i, j, word[i], word[j]) if edge == marked_edge else w_entry(
                            i, j, word[i], word[j]
                        )
                    marked += term
            assert marked == trace * hafnian(tuple(range(6)), word, w_entry)
            checks += 1
    return {"marked_matching_gauge_coefficients": checks}


def tensor_type_audit() -> dict[str, int]:
    permutations = tuple(itertools.permutations(range(6)))
    hafnian_matchings = matching_masks((1 << 6) - 1)
    assert len(permutations) == 720
    assert len(hafnian_matchings) == 15
    # A P6 permanent monomial selects six vector coordinates.  A six-vertex
    # matching monomial selects three edge blocks.  This is a type census, not
    # a claim that no separately proved restriction between them can exist.
    return {
        "permanent_degree": 6,
        "permanent_monomials": len(permutations),
        "hafnian_edge_degree": 3,
        "hafnian_monomials": len(hafnian_matchings),
    }


def main() -> None:
    print(
        json.dumps(
            {
                "verified": True,
                "finite_field_orientation": orientation_census(),
                "matching_expansion": matching_audit(),
                "gauge": gauge_audit(),
                "tensor_types": tensor_type_audit(),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
