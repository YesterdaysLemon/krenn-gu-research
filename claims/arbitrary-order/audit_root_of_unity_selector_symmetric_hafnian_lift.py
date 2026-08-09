"""Independent exact audit of the four-row selector's symmetric lift."""

from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def poly_mul(left: Counter[tuple[int, ...]], right: Counter[tuple[int, ...]]):
    result: Counter[tuple[int, ...]] = Counter()
    for left_exp, left_coefficient in left.items():
        for right_exp, right_coefficient in right.items():
            exponent = tuple(a + b for a, b in zip(left_exp, right_exp))
            result[exponent] += left_coefficient * right_coefficient
    for exponent in tuple(result):
        if result[exponent] == 0:
            del result[exponent]
    return result


def scalar(value: int) -> Counter[tuple[int, ...]]:
    return Counter({(0,) * 8: value}) if value else Counter()


def variable(index: int) -> Counter[tuple[int, ...]]:
    exponent = [0] * 8
    exponent[index] = 1
    return Counter({tuple(exponent): 1})


def add(target: Counter[tuple[int, ...]], source: Counter[tuple[int, ...]]):
    target.update(source)
    for exponent in tuple(target):
        if target[exponent] == 0:
            del target[exponent]
    return target


def enumerate_matchings(vertices: tuple[int, ...]):
    if not vertices:
        yield ()
        return
    first = vertices[0]
    for position in range(1, len(vertices)):
        second = vertices[position]
        rest = vertices[1:position] + vertices[position + 1 :]
        for matching in enumerate_matchings(rest):
            yield ((first, second),) + matching


def main() -> None:
    # Variable order: u,v,w,z,p,q,r,s.  This audit deliberately avoids
    # importing the primary verifier and uses sparse integer polynomials.
    u, v, w, z, p, q, r, s = (variable(index) for index in range(8))
    one, two, minus_two, zero = scalar(1), scalar(2), scalar(-2), Counter()
    matrix = [
        [u, v, one, one],
        [w, z, one, one],
        [p, q, two, minus_two],
        [r, s, two, minus_two],
    ]

    permanent = Counter()
    for permutation in itertools.permutations(range(4)):
        term = scalar(1)
        for row in range(4):
            term = poly_mul(term, matrix[row][permutation[row]])
        permanent = add(permanent, term)

    adjacency = [[zero for _ in range(8)] for _ in range(8)]
    for row in range(4):
        for column in range(4):
            adjacency[row][4 + column] = matrix[row][column]
            adjacency[4 + column][row] = matrix[row][column]

    hafnian = Counter()
    matchings = list(enumerate_matchings(tuple(range(8))))
    nonzero_terms = 0
    for matching in matchings:
        term = scalar(1)
        for left, right in matching:
            term = poly_mul(term, adjacency[left][right])
        if term:
            nonzero_terms += 1
        hafnian = add(hafnian, term)

    expected = Counter()
    for coefficient, first, second in (
        (-8, u, z),
        (-8, v, w),
        (2, p, s),
        (2, q, r),
    ):
        expected = add(expected, poly_mul(scalar(coefficient), poly_mul(first, second)))

    assert len(matchings) == 105
    assert nonzero_terms == 24
    assert permanent == expected
    assert hafnian == expected

    # Independently reconstruct the four local column maps.  A variable
    # column is I_4.  Each constant column is U_j e_0^T and has rank one;
    # the latter fact is checked by its nonzero-row support rather than CAS.
    constants = ((1, 1, 2, 2), (1, 1, -2, -2))
    constant_map_ranks = []
    for column in constants:
        local_map = [
            [column[row] if coordinate == 0 else 0 for coordinate in range(4)]
            for row in range(4)
        ]
        nonzero_columns = [
            coordinate
            for coordinate in range(4)
            if any(local_map[row][coordinate] for row in range(4))
        ]
        assert nonzero_columns == [0]
        assert any(local_map[row][0] for row in range(4))
        constant_map_ranks.append(1)

    primary_path = (
        ROOT / "tmp" / "root_of_unity_selector_symmetric_hafnian_lift_verified.json"
    )
    primary = json.loads(primary_path.read_text(encoding="utf-8"))
    assert primary["matching_count"] == 105
    assert primary["nonzero_bipartite_matching_count"] == 24
    assert primary["right_mode_map_ranks_before_herald_contraction"] == [4, 4, 1, 1]

    output = {
        "status": "exact_symmetric_hafnian_lift_independently_audited",
        "method": "sparse integer polynomial arithmetic and fresh matching enumeration",
        "matching_count": len(matchings),
        "nonzero_matching_count": nonzero_terms,
        "polynomial_term_count": len(hafnian),
        "constant_mode_map_ranks": constant_map_ranks,
        "boundary": "heralded contraction only; no Question-1 realization",
    }
    destination = (
        ROOT / "tmp" / "root_of_unity_selector_symmetric_hafnian_lift_audited.json"
    )
    destination.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
