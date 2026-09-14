"""No-import audit of the n=8 physical boundary-quotient limitation."""

from __future__ import annotations

import argparse
import itertools
import json
import sys as _bootstrap_sys
from collections import Counter
from functools import lru_cache
from pathlib import Path as _BootstrapPath

import sympy as sp

for _bootstrap_parent in _BootstrapPath(__file__).resolve().parents:
    if (_bootstrap_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        _bootstrap_sys.path.insert(0, str(_bootstrap_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap as _bootstrap_repository  # noqa: E402

REPO_ROOT, HERE = _bootstrap_repository(__file__)

ZEROS = (
    19,
    73,
    92,
    109,
    163,
    181,
    182,
    190,
    199,
    200,
    208,
    209,
    217,
    229,
    230,
    235,
    238,
)
NONZEROS = (38, 55, 82, 118, 121, 247)
LEFT = (226, 247)
RIGHT = (227, 244)
WORDS = ("00000010", "00000110", "00100000", "00100100")


def pair_index(u: int, v: int) -> int:
    if not 0 <= u < v < 8:
        raise ValueError("pair must be increasing and in range")
    return u * (15 - u) // 2 + v - u - 1


def physical_id(u: int, v: int, a: int, b: int) -> int:
    if u > v:
        u, v, a, b = v, u, b, a
    return 9 * pair_index(u, v) + 3 * a + b + 1


def decode(identifier: int) -> tuple[int, int, int, int]:
    block, colour_offset = divmod(identifier - 1, 9)
    pairs = tuple(itertools.combinations(range(8), 2))
    u, v = pairs[block]
    a, b = divmod(colour_offset, 3)
    return u, v, a, b


def mapped_id(
    identifier: int,
    vertex_map: tuple[int, ...],
    colour_map: tuple[int, ...],
) -> int:
    u, v, a, b = decode(identifier)
    return physical_id(vertex_map[u], vertex_map[v], colour_map[a], colour_map[b])


@lru_cache(maxsize=None)
def recursive_matchings(mask: int) -> tuple[tuple[tuple[int, int], ...], ...]:
    if mask == 0:
        return ((),)
    first_bit = mask & -mask
    first = first_bit.bit_length() - 1
    remaining = mask ^ first_bit
    output = []
    other_mask = remaining
    while other_mask:
        second_bit = other_mask & -other_mask
        second = second_bit.bit_length() - 1
        for tail in recursive_matchings(remaining ^ second_bit):
            output.append(((first, second), *tail))
        other_mask ^= second_bit
    return tuple(output)


def reconstruct_boundary_identity() -> None:
    symbols = {identifier: sp.Symbol(f"g{identifier}") for identifier in range(1, 253)}
    zero_set = frozenset(ZEROS)

    @lru_cache(maxsize=None)
    def hafnian(vertices: tuple[int, ...], word: tuple[int, ...]):
        if not vertices:
            return sp.S.One
        first = vertices[0]
        terms = []
        for position in range(1, len(vertices)):
            second = vertices[position]
            identifier = physical_id(first, second, word[0], word[position])
            if identifier in zero_set:
                continue
            remaining_vertices = vertices[1:position] + vertices[position + 1 :]
            remaining_word = word[1:position] + word[position + 1 :]
            terms.append(symbols[identifier] * hafnian(remaining_vertices, remaining_word))
        return sp.expand(sum(terms, sp.S.Zero))

    full = [hafnian(tuple(range(8)), tuple(map(int, word))) for word in WORDS]
    h_value = hafnian((0, 1, 4, 5), (0, 0, 0, 0))
    k0 = hafnian((0, 1, 2, 4, 6, 7), (0, 0, 0, 0, 1, 0))
    k1 = hafnian((0, 1, 2, 4, 6, 7), (0, 0, 1, 0, 0, 0))
    a, b, c, d, x, y, z0, z1, s, t, e = (
        symbols[identifier]
        for identifier in (118, 121, 172, 173, 38, 82, 244, 247, 226, 55, 227)
    )
    expected = (
        a * z1 * h_value + c * k0 + a * e * t * y,
        a * x * y * z1 + d * k0,
        b * (s * t * y + z0 * h_value) + c * k1,
        b * x * y * z0 + d * k1,
    )
    if any(sp.expand(actual - wanted) != 0 for actual, wanted in zip(full, expected)):
        raise AssertionError("one complete source expansion differs")
    boundary = s * z1 - e * z0
    n_value = a * b * t * y * boundary
    f1, f2, f3, f4 = full
    r_value = a * z1 * (d * f3 - c * f4) - b * z0 * (d * f1 - c * f2)
    if sp.expand(r_value - d * n_value) != 0:
        raise AssertionError("R=d*N failed")
    if sp.expand(n_value * f2 - k0 * r_value - a**2 * b * t * x * y**2 * z1 * boundary) != 0:
        raise AssertionError("boundary certificate failed")


def audit_orbit(support: set[int]) -> dict[str, object]:
    categories = Counter()
    live_relations = set()
    for vertex_map in itertools.permutations(range(8)):
        for colour_map in itertools.permutations(range(3)):
            if any(mapped_id(i, vertex_map, colour_map) in support for i in ZEROS):
                continue
            if any(mapped_id(i, vertex_map, colour_map) not in support for i in NONZEROS):
                continue
            left = tuple(sorted(mapped_id(i, vertex_map, colour_map) for i in LEFT))
            right = tuple(sorted(mapped_id(i, vertex_map, colour_map) for i in RIGHT))
            left_live = set(left) <= support
            right_live = set(right) <= support
            if left_live != right_live:
                categories["one_live"] += 1
            elif left_live:
                categories["both_live"] += 1
                live_relations.add(tuple(sorted((left, right))))
            else:
                categories["both_zero"] += 1
    return {
        "applicable": sum(categories.values()),
        "both_live": categories["both_live"],
        "both_zero": categories["both_zero"],
        "one_live": categories["one_live"],
        "live_relations": live_relations,
    }


def audit_full_fibres(support: set[int]) -> tuple[Counter[int], dict[str, int], int]:
    histogram = Counter()
    pure = {}
    related_pairs = 0
    relation = Counter({88: 1, 91: 1, 82: -1, 97: -1})
    reverse = Counter({identifier: -coefficient for identifier, coefficient in relation.items()})
    for word in itertools.product(range(3), repeat=8):
        live = []
        for matching in recursive_matchings((1 << 8) - 1):
            term = tuple(sorted(physical_id(u, v, word[u], word[v]) for u, v in matching))
            if set(term) <= support:
                live.append(term)
        word_text = "".join(map(str, word))
        if len(set(word)) == 1:
            pure[word_text] = len(live)
            continue
        histogram[len(live)] += 1
        for index, left_term in enumerate(live):
            for right_term in live[index + 1 :]:
                difference = Counter(left_term)
                difference.subtract(right_term)
                difference = Counter(
                    {identifier: coefficient for identifier, coefficient in difference.items() if coefficient}
                )
                if difference == relation or difference == reverse:
                    related_pairs += 1
    return histogram, pure, related_pairs


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--support",
        type=_BootstrapPath,
        default=REPO_ROOT
        / "tests"
        / "fixtures"
        / "recursive_physical_support_n8_four_cut_survivor_134.json",
    )
    parser.add_argument(
        "--expected",
        type=_BootstrapPath,
        default=REPO_ROOT
        / "tests"
        / "fixtures"
        / "eight_vertex_physical_boundary_quotient_134.json",
    )
    args = parser.parse_args()
    support = set(json.loads(args.support.read_text(encoding="utf-8"))["nonzero_entry_ids"])
    expected = json.loads(args.expected.read_text(encoding="utf-8"))
    if len(support) != 134:
        raise AssertionError("support size differs")

    reconstruct_boundary_identity()
    orbit = audit_orbit(support)
    histogram, pure, related_pairs = audit_full_fibres(support)
    expected_orbit = expected["boundary_orbit"]
    expected_census = expected["full_word_census"]
    if orbit != {
        "applicable": expected_orbit["applicable_placements"],
        "both_live": expected_orbit["both_sides_live_placements"],
        "both_zero": expected_orbit["both_sides_zero_placements"],
        "one_live": len(expected_orbit["one_side_live_contradictions"]),
        "live_relations": {((82, 97), (88, 91))},
    }:
        raise AssertionError("orbit audit differs")
    if dict(sorted(histogram.items())) != {
        int(size): count for size, count in expected_census["mixed_fibre_size_histogram"].items()
    }:
        raise AssertionError("mixed-fibre census differs")
    if pure != expected_census["pure_fibre_sizes"] or related_pairs:
        raise AssertionError("pure census or direct relation-pair audit differs")
    if expected["outcome"] != "NO_EXCLUSION_BY_THIS_BOUNDARY_QUOTIENT_MECHANISM":
        raise AssertionError("unexpected promoted outcome")

    print(
        json.dumps(
            {
                "status": "PASS",
                "source_identity_reconstructed": True,
                "applicable_boundary_placements": orbit["applicable"],
                "distinct_live_relation": "g88*g91 = g82*g97",
                "mixed_full_word_fibres": sum(histogram.values()),
                "directly_related_matching_monomial_pairs": related_pairs,
                "exact_support_exclusion_claimed": False,
                "weight_realization_claimed": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
