"""Exact n=8 four-probe source decomposition for arbitrary protected filling.

Finite exact companion, not an all-order exclusion. It keeps all 96 hollow crossing
entries as a formal variable and classifies physical perfect matchings by
the local crossing mechanism omitted by the common-star AB formula.
"""
from collections import Counter, defaultdict
from functools import lru_cache
from itertools import product
import json
from pathlib import Path


MATCH = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))
INTERNAL_COLOUR = {
    tuple(sorted(edge)): colour
    for colour, matching in enumerate(MATCH)
    for edge in matching
}
R = ((1, -1, 0), (1, 0, -1))


@lru_cache(maxsize=None)
def perfect_matchings(vertices):
    if not vertices:
        return ((),)
    first = vertices[0]
    output = []
    for index, second in enumerate(vertices[1:], 1):
        remainder = vertices[1:index] + vertices[index + 1:]
        for tail in perfect_matchings(remainder):
            output.append(((first, second), *tail))
    return tuple(output)


def matching_class(matching):
    crossing = [(u, v) for u, v in matching if (u < 4) != (v < 4)]
    if not crossing:
        return "internal_component"
    if len(crossing) == 4:
        return "degree4"
    assert len(crossing) == 2
    crossed = {
        0: {u for edge in crossing for u in edge if u < 4},
        1: {u - 4 for edge in crossing for u in edge if u >= 4},
    }
    local_types = tuple("AB" if 0 in crossed[side] else "BB" for side in (0, 1))
    if local_types != ("AB", "AB"):
        return "degree2_" + "_".join(local_types)
    if all((u == 0) == (v == 4) for u, v in crossing):
        return "separated_AB"
    return "mixed_center_leaf_AB"


def term_for_word(matching, word):
    monomial = []
    for u, v in matching:
        if (u < 4) == (v < 4):
            side = 0 if u < 4 else 4
            pair = tuple(sorted((u - side, v - side)))
            colour = INTERNAL_COLOUR[pair]
            if word[u] != colour or word[v] != colour:
                return None
        else:
            if u >= 4:
                u, v = v, u
            left_colour, right_colour = word[u], word[v]
            if left_colour == right_colour:
                return None
            monomial.append((left_colour, right_colour, u, v - 4))
    return tuple(sorted(monomial))


def add(counter, key, value):
    if value:
        counter[key] += value
        if counter[key] == 0:
            del counter[key]


def raw_projection():
    matrices = defaultdict(lambda: [[Counter() for _ in range(2)] for _ in range(2)])
    for matching in perfect_matchings(tuple(range(8))):
        kind = matching_class(matching)
        for x0, y0, x1, y1 in product(range(3), repeat=4):
            word = (x0, y0, y0, y0, x1, y1, y1, y1)
            monomial = term_for_word(matching, word)
            if monomial is None:
                continue
            for p in range(2):
                for q in range(2):
                    add(matrices[kind][p][q], monomial, R[p][x0] * R[q][y1])
    # An internal component is enough for local r.s cancellation.  Verify it
    # happened after summing colors, rather than deleting those matchings.
    assert all(not entry for row in matrices["internal_component"] for entry in row)
    return matrices


def laurent_substitute(matrix, supports):
    variables = tuple(sorted(supports))
    output = [[Counter() for _ in range(2)] for _ in range(2)]
    for p in range(2):
        for q in range(2):
            for monomial, coefficient in matrix[p][q].items():
                exponent = [0] * len(variables)
                for c, d, i, j in monomial:
                    positions = supports.get((c, d))
                    if positions is None or (i, j) not in positions:
                        coefficient = 0
                        break
                    index = positions.index((i, j))
                    exponent[variables.index((c, d))] += 1 if index == 0 else -1
                    if index == 1:
                        coefficient *= -1
                add(output[p][q], tuple(exponent), coefficient)
    return output


def specialize_monomial(monomial, supports, variables):
    coefficient = 1
    exponent = [0] * len(variables)
    for c, d, i, j in monomial:
        positions = supports.get((c, d))
        if positions is None or (i, j) not in positions:
            return None
        index = positions.index((i, j))
        exponent[variables.index((c, d))] += 1 if index == 0 else -1
        if index == 1:
            coefficient *= -1
    return coefficient, tuple(exponent)


def ab_residuals(supports):
    variables = tuple(sorted(supports))
    zero = (0,) * len(variables)
    errors = []
    for x0, y0, x1, y1 in product(range(3), repeat=4):
        word = (x0, y0, y0, y0, x1, y1, y1, y1)
        amplitude = Counter()
        for matching in perfect_matchings(tuple(range(8))):
            monomial = term_for_word(matching, word)
            if monomial is None:
                continue
            specialized = specialize_monomial(monomial, supports, variables)
            if specialized is not None:
                add(amplitude, specialized[1], specialized[0])
        if len(set(word)) == 1:
            add(amplitude, zero, -1)
        if amplitude:
            errors.append(("".join(map(str, word)), dict(amplitude)))
    return errors


def active_specialized_terms(word, supports):
    variables = tuple(sorted(supports))
    records = []
    for matching in perfect_matchings(tuple(range(8))):
        monomial = term_for_word(matching, word)
        if monomial is None:
            continue
        specialized = specialize_monomial(monomial, supports, variables)
        if specialized is not None:
            records.append((matching_class(matching), matching, specialized))
    return records


def evaluate_one(matrix):
    return [[sum(matrix[p][q].values()) for q in range(2)] for p in range(2)]


def format_entry(entry):
    return sorted((coefficient, exponent) for exponent, coefficient in entry.items())


def matrix_sum(matrices):
    output = [[Counter() for _ in range(2)] for _ in range(2)]
    for matrix in matrices:
        for p in range(2):
            for q in range(2):
                for monomial, coefficient in matrix[p][q].items():
                    add(output[p][q], monomial, coefficient)
    return output


def check_frozen_crossing_cover(supports):
    """All twelve supported entries occur in component-constant matchings."""
    covered = set()
    for a, b in supports:
        word = (a,) * 4 + (b,) * 4
        records = active_specialized_terms(word, supports)
        assert len(records) == 2
        assert sorted(record[2][0] for record in records) == [-1, 1]
        assert all(record[2][1] == (0,) * 6 for record in records)
        for _kind, matching, _coefficient in records:
            monomial = term_for_word(matching, word)
            assert monomial is not None
            covered.update(monomial)
    actual = {(a, b, u, v) for (a, b), positions in supports.items()
              for u, v in positions}
    assert len(actual) == 12 and covered == actual


def main():
    matrices = raw_projection()
    print("raw nonzero monomials by matching class and entry")
    for kind, matrix in matrices.items():
        print(kind, [[len(matrix[p][q]) for q in range(2)] for p in range(2)])

    fixture = json.loads((Path(__file__).resolve().parents[2] /
                          "tests/fixtures/eight_vertex_scaffold_subsystem_controls.json").read_text(encoding="utf-8"))
    for family in fixture["families"]:
        supports = {
            tuple(pair): [tuple(position) for position in positions]
            for pair, positions in zip(fixture["parameter_order"], family["supports"], strict=True)
        }
        specialized = {
            kind: laurent_substitute(matrix, supports)
            for kind, matrix in matrices.items()
        }
        total = matrix_sum(specialized.values())
        separated = specialized["separated_AB"]
        remainder = matrix_sum(
            matrix for kind, matrix in specialized.items()
            if kind not in ("internal_component", "separated_AB")
        )
        print("family", family["name"])
        for kind, matrix in specialized.items():
            if kind == "internal_component":
                continue
            print(" ", kind, "at all parameters=1", evaluate_one(matrix))
        print(" separated_AB at all parameters=1", evaluate_one(separated))
        print(" non-common-star remainder at all parameters=1", evaluate_one(remainder))
        print(" total projected source at all parameters=1", evaluate_one(total))
        print(" total Laurent term counts", [[len(total[p][q]) for q in range(2)] for p in range(2)])
        print(" total Laurent entries", [[format_entry(total[p][q]) for q in range(2)] for p in range(2)])
        errors = ab_residuals(supports)
        print(" AB-word residual count", len(errors), errors[:4])
        if family["name"] in (
            "binary_and_monochromatic_shores_v2",
            "independent_minorities_and_component_constants_v3",
        ):
            zero = (0,) * 6
            expected = ((2, 1), (1, 2))
            assert errors == []
            assert all(total[p][q] == Counter({zero: expected[p][q]})
                       for p in range(2) for q in range(2))
            check_frozen_crossing_cover(supports)
            print(" frozen component-matching cover: all 12 crossing entries")
        if family["name"] == "binary_and_monochromatic_shores_v2":
            detectors = {
                (0, 0, 0, 2, 0, 0, 1, 1): ("degree2_BB_BB", -1, (1, 0, 0, 0, 0, -1)),
                (0, 1, 0, 0, 0, 0, 0, 2): ("degree2_AB_BB", 1, (0, 1, 1, 0, 0, 0)),
            }
            for word, expected_detector in detectors.items():
                records = active_specialized_terms(word, supports)
                assert len(records) == 1
                kind, matching, specialized_term = records[0]
                assert (kind, specialized_term[0], specialized_term[1]) == expected_detector
                print(" split-leaf detector", "".join(map(str, word)), kind,
                      matching, specialized_term)
    print("exact projected-source and AB-control checks passed")


if __name__ == "__main__":
    main()
