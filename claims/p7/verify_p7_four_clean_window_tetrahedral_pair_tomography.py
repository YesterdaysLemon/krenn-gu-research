"""Verify four-window tetrahedral pair tomography exactly."""

from itertools import combinations

import sympy as sp

PORTS = tuple(range(1, 7))
EDGES = tuple(combinations(PORTS, 2))
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}
WINDOWS = (
    frozenset((1, 2, 3, 4)),
    frozenset((1, 2, 5, 6)),
    frozenset((1, 3, 5, 6)),
    frozenset((1, 4, 5, 6)),
)
TARGET = frozenset((1, 2, 3, 4))
NUISANCE_COLUMNS = tuple(
    index for index, edge in enumerate(EDGES) if not set(edge) <= TARGET
)


def edge(a: int, b: int) -> tuple[int, int]:
    return tuple(sorted((a, b)))


def observation_matrix() -> sp.Matrix:
    return sp.Matrix(
        [
            [int(vertex in pair and set(pair) <= window) for pair in EDGES]
            for window in WINDOWS
            for vertex in sorted(window)
        ]
    )


def main() -> None:
    variables = sp.symbols("x12 x13 x14 x15 x16 x23 x24 x25 x26 x34 x35 x36 x45 x46 x56")
    x = {pair: variables[index] for index, pair in enumerate(EDGES)}

    def star(window: frozenset[int], vertex: int):
        return sum(x[edge(vertex, other)] for other in window if other != vertex)

    def shore(a: int, b: int):
        window = frozenset((a, b, 5, 6))
        return sp.expand(
            (
                star(window, a)
                + star(window, b)
                - star(window, 5)
                - star(window, 6)
            )
            / 2
        )

    d12 = shore(1, 2)
    d13 = shore(1, 3)
    d14 = shore(1, 4)
    assert sp.expand(d12 - (x[(1, 2)] - x[(5, 6)])) == 0
    assert sp.expand(d13 - (x[(1, 3)] - x[(5, 6)])) == 0
    assert sp.expand(d14 - (x[(1, 4)] - x[(5, 6)])) == 0

    p = sp.expand(d12 - d13)
    q = sp.expand(d12 - d14)
    s = {vertex: star(TARGET, vertex) for vertex in TARGET}
    recovered = {}
    recovered[(1, 2)] = sp.expand((s[1] + p + q) / 3)
    recovered[(1, 3)] = sp.expand(recovered[(1, 2)] - p)
    recovered[(1, 4)] = sp.expand(recovered[(1, 2)] - q)
    a_value = sp.expand(s[2] - recovered[(1, 2)])
    b_value = sp.expand(s[3] - recovered[(1, 3)])
    c_value = sp.expand(s[4] - recovered[(1, 4)])
    recovered[(2, 3)] = sp.expand((a_value + b_value - c_value) / 2)
    recovered[(2, 4)] = sp.expand((a_value + c_value - b_value) / 2)
    recovered[(3, 4)] = sp.expand((b_value + c_value - a_value) / 2)
    for pair, expression in recovered.items():
        assert sp.expand(expression - x[pair]) == 0

    matrix = observation_matrix()
    nuisance = matrix[:, NUISANCE_COLUMNS]
    assert matrix.rank() == 14
    assert nuisance.rank() == 8
    assert matrix.rank() - nuisance.rank() == 6

    total_rows = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14)
    total_columns = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14)
    nuisance_rows = (4, 5, 6, 7, 9, 10, 13, 14)
    nuisance_local_columns = (0, 1, 2, 3, 4, 5, 6, 8)
    assert matrix.extract(total_rows, total_columns).det() == -12
    assert nuisance.extract(nuisance_rows, nuisance_local_columns).det() == 2

    print("four-window shore identities: VERIFIED")
    print("all six target pair coordinates: RECONSTRUCTED")
    print("recovery rank 14-8=6; certificate minors -12 and 2")
    print("graph_search=0 support_search=0 colour_word_search=0")


if __name__ == "__main__":
    main()
