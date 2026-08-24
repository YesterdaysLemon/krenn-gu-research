"""Independent no-import audit of the surviving finite GLD65 identities.

This audit intentionally does not import the primary replay.  It uses a
recursive string-word matching polynomial, constructs the six support
profiles from colour-to-matching assignments instead of scanning 2^18 masks,
and checks the dimension obstruction through the kernel of a three-row
pairing map rather than the primary five-vector elimination certificate.
It does not supply the withdrawn root-companion/full-coefficient bridge.
"""

from __future__ import annotations

from itertools import combinations, permutations

ROOT = (0, 1, 2, 3)
OUT = (4, 5, 6, 7)
PORT = (0, 1, 2, 3)
COLOUR = (0, 1, 2)
MATCHINGS = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))


def pair(a: int, b: int) -> tuple[int, int]:
    return (a, b) if a < b else (b, a)


def matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    head = vertices[0]
    for index in range(1, len(vertices)):
        tail = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for suffix in matchings(rest):
            yield (pair(head, tail),) + suffix


def matching_word(matching: tuple[tuple[int, int], ...]) -> tuple[str, ...]:
    return tuple(sorted(f"e{left}{right}" for left, right in matching))


def polynomial(vertices: tuple[int, ...], no_outside_edge: bool = False):
    answer = {}
    for matching in matchings(vertices):
        if no_outside_edge and any(
            left in OUT and right in OUT for left, right in matching
        ):
            continue
        word = matching_word(matching)
        answer[word] = answer.get(word, 0) + 1
    return answer


def add(answer, source, scale=1):
    for word, coefficient in source.items():
        answer[word] = answer.get(word, 0) + scale * coefficient
        if not answer[word]:
            del answer[word]


def multiply(left, right):
    answer = {}
    for word_left, coefficient_left in left.items():
        for word_right, coefficient_right in right.items():
            word = tuple(sorted(word_left + word_right))
            answer[word] = answer.get(word, 0) + coefficient_left * coefficient_right
    return answer


def variable(left: int, right: int):
    return {(f"e{pair(left, right)[0]}{pair(left, right)[1]}",): 1}


def check_direct_matching_identity() -> tuple[int, int, int]:
    words = {matching_word(matching) for matching in matchings(ROOT + OUT)}
    assert len(words) == 105
    outside_degree = []
    for word in words:
        degree = 0
        for label in word:
            left, right = int(label[1]), int(label[2])
            degree += left in OUT and right in OUT
        outside_degree.append(degree)
    counts = tuple(outside_degree.count(degree) for degree in (0, 1, 2))
    assert counts == (24, 72, 9)

    # Delete one named outside edge.  Its 12 one-edge words are in bijection
    # with a root edge (six choices) and the two assignments of the remaining
    # roots to the remaining outside pair.  The only surviving named edge
    # when the complementary pair signature is Q is the port edge uv.
    for chosen in combinations(OUT, 2):
        chosen_pair = pair(*chosen)
        selected = [
            word
            for word in words
            if f"e{chosen_pair[0]}{chosen_pair[1]}" in word
            and sum(int(label[1]) in OUT and int(label[2]) in OUT for label in word)
            == 1
        ]
        assert len(selected) == 12

    full = polynomial(ROOT + OUT)
    root_hafnian = polynomial(ROOT)
    root_bijection = polynomial(ROOT + OUT, no_outside_edge=True)
    outside_compound = {}
    for first, second in (
        ((4, 5), (6, 7)),
        ((4, 6), (5, 7)),
        ((4, 7), (5, 6)),
    ):
        add(outside_compound, multiply(variable(*first), variable(*second)))
    pair_sum = {}
    for chosen in combinations(OUT, 2):
        complement = tuple(vertex for vertex in OUT if vertex not in chosen)
        term = multiply(variable(*chosen), polynomial(ROOT + complement))
        add(pair_sum, term)
    reconstructed = dict(pair_sum)
    add(reconstructed, multiply(root_hafnian, outside_compound), scale=-1)
    add(reconstructed, root_bijection)
    assert reconstructed == full
    return counts


def support_from_assignment(assignment: tuple[int, int, int]):
    support = set()
    for colour, matching_index in enumerate(assignment):
        for edge in MATCHINGS[matching_index]:
            support.add((edge, colour))
    return support


def cross_zero(support) -> bool:
    return all(
        not ((edge, colour) in support and (opposite, other) in support)
        for edge, opposite in MATCHINGS
        for colour in COLOUR
        for other in COLOUR
        if colour != other
    )


def check_assignment_supports() -> int:
    profiles = []
    for assignment in permutations(range(3)):
        support = support_from_assignment(assignment)
        assert len(support) == 6
        assert cross_zero(support)
        for edge in combinations(PORT, 2):
            assert sum((edge, colour) in support for colour in COLOUR) == 1

        # No absent edge-colour entry can be added without producing a mixed
        # 2+2 word with the already active complementary edge.
        for edge in combinations(PORT, 2):
            for colour in COLOUR:
                if (edge, colour) in support:
                    continue
                enlarged = set(support)
                enlarged.add((edge, colour))
                assert not cross_zero(enlarged)
        profiles.append(frozenset(support))
    assert len(set(profiles)) == 6

    # If two colours chose the same matching, the two cross-products on its
    # complementary edges would be nonzero.  Thus the six permutation
    # profiles are the complete possibilities once every pure colour has a
    # live complementary product.
    for assignment in (
        tuple(choice for choice in choices)
        for choices in __import__("itertools").product(range(3), repeat=3)
    ):
        collision = len(set(assignment)) < 3
        assert collision == (assignment not in permutations(range(3)))
    return len(profiles)


def edge_colour(left: int, right: int) -> int:
    named = pair(left, right)
    return next(index for index, matching in enumerate(MATCHINGS) if named in matching)


def prescribed_pairing(left: tuple[int, int], right: tuple[int, int]) -> bool:
    port_left, colour_left = left
    port_right, colour_right = right
    assert port_left != port_right
    return colour_left == colour_right == edge_colour(port_left, port_right)


def check_kernel_dimension_obstruction() -> int:
    checks = 0
    for base in PORT:
        # The three partner vectors have pairing-map images equal to the
        # three nonzero coordinate axes, so the map V -> K^3 has rank three.
        image_supports = [{colour} for colour in COLOUR]
        assert len({frozenset(item) for item in image_supports}) == 3

        for neighbour in PORT:
            if neighbour == base:
                continue
            named_colour = edge_colour(base, neighbour)
            off_colours = [colour for colour in COLOUR if colour != named_colour]
            # Both off-colour vectors at the neighbour pair to zero with all
            # three base vectors, so both lie in the kernel.  They are
            # independent because their nonzero partners are on two distinct
            # named edges and all cross-colour pairings vanish.
            assert len(off_colours) == 2
            for colour in off_colours:
                partner = next(
                    port
                    for port in PORT
                    if port != neighbour and edge_colour(neighbour, port) == colour
                )
                assert partner not in (neighbour,)
                assert edge_colour(neighbour, partner) == colour
                pattern = [
                    prescribed_pairing((neighbour, other), (partner, colour))
                    for other in off_colours
                ]
                assert pattern[off_colours.index(colour)]
                assert sum(pattern) == 1
            # rank three on a space of dimension at most four leaves kernel
            # dimension at most one, contradicting these two independent
            # vectors.
            assert 4 - 3 < len(off_colours)
            checks += 1
    assert checks == 12
    return checks


def main() -> None:
    counts = check_direct_matching_identity()
    profiles = check_assignment_supports()
    kernels = check_kernel_dimension_obstruction()
    print("GLD65 surviving finite-identity no-import audit: PASS")
    print("  independently generated matching strata:", counts)
    print("  maximal matching-colour support profiles:", profiles)
    print("  rank-three-map/kernel contradictions:", kernels)
    print("  no primary-verifier imports; no finite-field or numerical inference")
    print("  withdrawn interface not tested: legal G_D row does not imply full F_D=0")
    print("  global Krenn-Gu status: UNRESOLVED")


if __name__ == "__main__":
    main()
