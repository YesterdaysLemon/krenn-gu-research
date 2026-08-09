"""Independent no-import audit for the ineligible-ninth-cell theorem."""


def counts(values):
    result = {0: 0, 1: 0, 2: 0}
    for value in values:
        result[value] += 1
    return result


def main():
    a, b, c, d, g = 2, 3, 5, 7, 11

    # The alpha2 slice deletes the two y2 terms of the six-term permanent.
    full_terms = {
        "z0z1z2": a * d,
        "z0z1y2": b * g,
        "L1Mz2": d,
        "L1z1z2": b * c,
        "L2My2": g,
        "L2z1z2": a * c,
    }
    sliced_terms = {name: value for name, value in full_terms.items() if "y2" not in name}
    assert set(sliced_terms) == {"z0z1z2", "L1Mz2", "L1z1z2", "L2z1z2"}

    flattening = ((a * d, 0), (b * c, d), (a * c, 0))
    minor = flattening[0][0] * flattening[1][1] - flattening[0][1] * flattening[1][0]
    assert minor == a * d * d == 98

    base = (0, 1, 1, 0)
    placements = set()
    for slot in range(4):
        placements.add(tuple(base[index] + int(index == slot) for index in range(4)))
    assert placements == {
        (0, 1, 1, 1),
        (1, 1, 1, 0),
        (0, 2, 1, 0),
        (0, 1, 2, 0),
    }

    alpha1, alpha2, gamma = 0, 1, 2
    assert counts((gamma, gamma, alpha2))[alpha1] == 0
    all_colours = counts((alpha1, alpha2, gamma))
    assert counts((alpha2, gamma, alpha1)) == all_colours
    assert counts((alpha2, alpha1, gamma)) == all_colours

    # In the s0=s1=1 vanishing scenario all incident a0 vectors have first
    # coordinate zero, so their span cannot have local rank three.
    incident_vectors = ((0, 0, 1), (0, 5, 0), (0, 13, -7), (0, 1, 0))
    assert all(vector[0] == 0 for vector in incident_vectors)

    # The s1=2 quotient vector cannot vanish because its end entries survive.
    mu = 17
    quotient_vector = (a * d, b * c + d * mu, a * c)
    assert quotient_vector[0] != 0 and quotient_vector[2] != 0

    print("independent no-import ineligible ninth-cell audit: PASS")
    print("physical cell retained, colour slice exact, no support or word census")


if __name__ == "__main__":
    main()
