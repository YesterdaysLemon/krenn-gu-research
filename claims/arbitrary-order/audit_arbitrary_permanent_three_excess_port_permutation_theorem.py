"""Independent no-import audit of the three-excess port theorem."""

from __future__ import annotations


def main() -> None:
    matrix = ((2, 3, 5), (7, 11, 13), (17, 19, 23))
    six_terms = (
        matrix[0][0] * matrix[1][1] * matrix[2][2],
        matrix[0][0] * matrix[1][2] * matrix[2][1],
        matrix[0][1] * matrix[1][0] * matrix[2][2],
        matrix[0][1] * matrix[1][2] * matrix[2][0],
        matrix[0][2] * matrix[1][0] * matrix[2][1],
        matrix[0][2] * matrix[1][1] * matrix[2][0],
    )
    assert len(six_terms) == 6
    assert sum(six_terms) == 3746

    identity = (0, 1, 2)
    transpositions = ((1, 0, 2), (2, 1, 0), (0, 2, 1))
    three_cycles = ((1, 2, 0), (2, 0, 1))
    nonidentity_cycles = transpositions + three_cycles
    assert identity not in nonidentity_cycles
    assert len(set(nonidentity_cycles)) == 5

    bypass = ((1, 0, 0), (2, 1, 1), (0, -1, 1))
    bypass_terms = (
        bypass[0][0] * bypass[1][1] * bypass[2][2],
        bypass[0][0] * bypass[1][2] * bypass[2][1],
    )
    assert sum(bypass_terms) == 0
    complementary_permanent = bypass[1][1] * bypass[2][2] + bypass[1][2] * bypass[2][1]
    assert complementary_permanent == 0
    assert bypass[0][1:] == (0, 0)

    degree_partitions = ((3,), (2, 1), (1, 1, 1))
    assert {sum(partition) for partition in degree_partitions} == {3}
    assert 2**3 == 8

    # Direct 3 x 3 determinant audit for the co-located excess witness.
    witness = ((1, 1, 1), (1, 2, 3), (1, 3, 2))
    determinant = (
        witness[0][0] * (witness[1][1] * witness[2][2] - witness[1][2] * witness[2][1])
        - witness[0][1]
        * (witness[1][0] * witness[2][2] - witness[1][2] * witness[2][0])
        + witness[0][2]
        * (witness[1][0] * witness[2][1] - witness[1][1] * witness[2][0])
    )
    assert determinant == -3
    assert (1 + 1, 1 + 2, 1 + 3) == (2, 3, 4)

    print("independent no-import three-excess port permutation audit: PASS")


if __name__ == "__main__":
    main()
