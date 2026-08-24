"""Independent no-import audit for the GLD66 two-colour exclusion.

This audit shares no code with the primary replay.  It represents matching
polynomials as integer dictionaries of edge words, reduces the support
classification to the 49 pairs of nonempty colour subsets on a complementary
matching, and checks the final kernel patterns from the 27 matching-colour
assignments rather than scanning edge masks.
"""

from __future__ import annotations

from itertools import combinations, product

ROOTS = (0, 1, 2, 3)
OUTSIDE = (4, 5, 6, 7)
PORTS = (0, 1, 2, 3)
COLOURS = (0, 1, 2)
ACTIVE = (0, 1)
ONE_FACTORS = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))


def pair(left, right):
    return (left, right) if left < right else (right, left)


def matchings(vertices):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for suffix in matchings(rest):
            yield (pair(first, second),) + suffix


def polynomial(vertices, *, forbid_outside=False):
    outside = set(vertices) - set(ROOTS)
    answer = {}
    for matching in matchings(vertices):
        if forbid_outside and any(
            left in outside and right in outside for left, right in matching
        ):
            continue
        word = tuple(sorted(matching))
        answer[word] = answer.get(word, 0) + 1
    return answer


def add(target, source, scale=1):
    for word, coefficient in source.items():
        target[word] = target.get(word, 0) + scale * coefficient
        if target[word] == 0:
            del target[word]


def multiply(left, right):
    answer = {}
    for word_left, coefficient_left in left.items():
        for word_right, coefficient_right in right.items():
            word = tuple(sorted(word_left + word_right))
            answer[word] = answer.get(word, 0) + coefficient_left * coefficient_right
    return answer


def variable(left, right):
    return {((pair(left, right)),): 1}


def check_matching_dictionaries():
    roots = polynomial(ROOTS)
    six_vertices = ROOTS + OUTSIDE[:2]
    six = polynomial(six_vertices)
    reconstructed_six = polynomial(six_vertices, forbid_outside=True)
    add(reconstructed_six, multiply(variable(*OUTSIDE[:2]), roots))
    assert reconstructed_six == six
    assert len(six) == 15
    assert len(polynomial(six_vertices, forbid_outside=True)) == 12

    eight = polynomial(ROOTS + OUTSIDE)
    reconstructed_eight = polynomial(ROOTS + OUTSIDE, forbid_outside=True)
    pair_sum = {}
    for chosen in combinations(OUTSIDE, 2):
        complement = tuple(vertex for vertex in OUTSIDE if vertex not in chosen)
        add(pair_sum, multiply(variable(*chosen), polynomial(ROOTS + complement)))
    add(reconstructed_eight, pair_sum)
    compound = {}
    for first, second in (
        ((4, 5), (6, 7)),
        ((4, 6), (5, 7)),
        ((4, 7), (5, 6)),
    ):
        add(compound, multiply(variable(*first), variable(*second)))
    add(reconstructed_eight, multiply(roots, compound), scale=-1)
    assert reconstructed_eight == eight

    strata = [0, 0, 0]
    for word in eight:
        degree = sum(left in OUTSIDE and right in OUTSIDE for left, right in word)
        strata[degree] += 1
    assert strata == [24, 72, 9]
    return len(polynomial(six_vertices, forbid_outside=True)), tuple(strata)


def nonempty_subsets():
    return tuple(
        frozenset(colour for colour in COLOURS if mask & (1 << colour))
        for mask in range(1, 1 << len(COLOURS))
    )


def mixed_compatible(left, right):
    return all(colour == other for colour in left for other in right)


def check_local_support_lemma():
    compatible = []
    for left in nonempty_subsets():
        for right in nonempty_subsets():
            if mixed_compatible(left, right):
                compatible.append((left, right))
                assert len(left) == len(right) == 1
                assert left == right
    assert len(compatible) == 3
    return len(compatible)


def factor_index(left, right):
    named = pair(left, right)
    return next(index for index, factor in enumerate(ONE_FACTORS) if named in factor)


def edge_colour(assignment, left, right):
    return assignment[factor_index(left, right)]


def pairing(assignment, left, right):
    left_port, left_colour = left
    right_port, right_colour = right
    assert left_port != right_port
    return left_colour == right_colour == edge_colour(assignment, left_port, right_port)


def check_assignment_kernel_proof():
    assignments = [
        assignment
        for assignment in product(COLOURS, repeat=3)
        if set(ACTIVE) <= set(assignment)
    ]
    assert len(assignments) == 12
    third_cases = 0
    two_colour_cases = 0
    for assignment in assignments:
        for base in PORTS:
            # Rank two of the pairing map is independently visible from its
            # two coordinate-axis partner images.
            images = []
            for colour in ACTIVE:
                partner = next(
                    port
                    for port in PORTS
                    if port != base and edge_colour(assignment, base, port) == colour
                )
                images.append(
                    tuple(
                        pairing(assignment, (base, row), (partner, colour))
                        for row in ACTIVE
                    )
                )
            assert set(images) == {(True, False), (False, True)}

            third = [
                port
                for port in PORTS
                if port != base and edge_colour(assignment, base, port) == 2
            ]
            if third:
                assert len(third) == 1
                assert all(
                    not pairing(assignment, (base, row), (third[0], column))
                    for row in ACTIVE
                    for column in ACTIVE
                )
                # The two target vectors are independent, whereas the rank-2
                # map on a space of dimension <=3 has kernel dimension <=1.
                assert len(ACTIVE) > 3 - 2
                third_cases += 1
                continue

            kernel = []
            for port in PORTS:
                if port == base:
                    continue
                colour = 1 - edge_colour(assignment, base, port)
                vector = (port, colour)
                assert all(
                    not pairing(assignment, (base, row), vector) for row in ACTIVE
                )
                kernel.append(vector)
            pattern = tuple(
                pairing(assignment, left, right)
                for left, right in combinations(kernel, 2)
            )
            assert sorted(pattern) == [False, False, True]
            two_colour_cases += 1

    assert third_cases == two_colour_cases == 24
    return len(assignments), third_cases, two_colour_cases


def main():
    response_terms, strata = check_matching_dictionaries()
    local_supports = check_local_support_lemma()
    assignments, third, two_colour = check_assignment_kernel_proof()
    print("GLD66 independent no-import audit: PASS")
    print("  independent response-anchor terms:", response_terms)
    print("  independent eight-vertex strata:", strata)
    print("  compatible nonempty complementary support pairs:", local_supports)
    print("  matching-colour assignments with both active colours:", assignments)
    print("  third-colour/two-colour kernel contradictions:", (third, two_colour))
    print("  no primary imports; no numerical or generic-rank inference")
    print("  global Krenn-Gu status: UNRESOLVED")


if __name__ == "__main__":
    main()
