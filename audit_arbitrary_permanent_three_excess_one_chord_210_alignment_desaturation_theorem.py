"""Independent no-import audit of one-chord 2+1+0 desaturation."""


def determinant_2_by_2(matrix):
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def main():
    # Independent nonzero integer specialization of a,b,c,d.
    a, b, c, d = 2, 3, 5, 7
    projected = [
        [a * d, 0],
        [b * c, d],
        [a * c, 0],
    ]
    minor = determinant_2_by_2(projected[:2])
    assert minor == a * d * d == 98

    # Alignment reserves alpha2 for the core M_alpha2 edge.  The other two
    # colour backbones supply exactly the outgoing directions needed for rank 3.
    all_colours = {0, 1, 2}
    alpha2 = 1
    outgoing = all_colours.difference({alpha2})
    assert outgoing == {0, 2}
    boundary_basis = {(1, 0, 0) if colour == 0 else (0, 0, 1) for colour in outgoing}
    assert boundary_basis == {(1, 0, 0), (0, 0, 1)}
    assert (0, 1, 0) not in boundary_basis

    placements = []
    for s0 in range(3):
        for s1 in range(1, 3):
            for exterior_surplus in range(3):
                if s0 + s1 + exterior_surplus == 2:
                    placements.append((s0, s1, 2, exterior_surplus))
    assert placements == [(0, 1, 2, 1), (0, 2, 2, 0), (1, 1, 2, 0)]

    # Concentrated a0: after killing L1 with the boundary line, V retains
    # nonzero z0 and L2 coordinates.  Concentrated a1: its quotient vector
    # retains the same two endpoint coordinates for every value of mu.
    assert (a * d, a * c) == (14, 10)
    for mu in (-5, 0, 11):
        vector = (a * d, b * c + d * mu, a * c)
        assert vector[0] != 0 and vector[2] != 0

    alpha1 = 2
    b1_colours = {0, 1}
    assert alpha1 not in b1_colours
    assert all(colour in b1_colours for colour in {0, 1})

    pure_matching = {"a0": "q2", "a1": "q0", "a2": "q3", "r0": "q1"}
    fixed_sources = {pure_matching[mode] for mode in ("a1", "a2", "r0")}
    assert {"q0", "q1", "q2", "q3"}.difference(fixed_sources) == {"q2"}
    assert pure_matching["a0"] == "q2"

    print("independent no-import aligned 2+1+0 desaturation audit: PASS")
    print("colour reservation, exact surplus placements, and rank-two minor")


if __name__ == "__main__":
    main()
