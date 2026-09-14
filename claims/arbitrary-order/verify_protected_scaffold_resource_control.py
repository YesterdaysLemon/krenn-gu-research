"""Exact finite control for the protected-scaffold exterior resource boundary.

This standalone replay checks one n=12 rational array, not arbitrary-order
nonexistence. The general cycle and resource formulas have written proofs
in PROTECTED_SCAFFOLD_MINORITY_CYCLE_AND_RESOURCE_BOUNDARY.md.

Run directly with Python; the JSON receipt goes to stdout and no file is
written. No project scientific constructor or verifier is imported.
"""

import itertools
import json
from collections import Counter


PARTNER_XOR = (1, 2, 3)
CROSSINGS = {(0, 4, 1, 0): 1, (2, 5, 1, 0): -1}


def weight(u, v, a, b):
    """Return the literal oriented physical edge entry."""
    if u > v:
        u, v, a, b = v, u, b, a
    if u // 4 == v // 4:
        return int(a == b and (u ^ v) == PARTNER_XOR[a])
    return CROSSINGS.get((u, v, a, b), 0)


def source(word, vertices):
    """Sum all supported physical matchings, with empty source equal to one."""
    if not vertices:
        return 1
    u, *rest = vertices
    return sum(
        entry * source(word, rest[:j] + rest[j + 1 :])
        for j, v in enumerate(rest)
        if (entry := weight(u, v, word[u], word[v]))
    )


def verify():
    checked = 0
    word_multiplicities = Counter()
    for c in range(3):
        pairs = [
            (u, u ^ PARTNER_XOR[c])
            for u in range(12)
            if u < (u ^ PARTNER_XOR[c])
        ]
        alternatives = [d for d in range(3) if d != c]
        choices = [
            [None] + [(v, d) for v in pair for d in alternatives]
            for pair in pairs
        ]
        for pattern in itertools.product(*choices):
            word = [c] * 12
            for item in pattern:
                if item is not None:
                    v, d = item
                    word[v] = d
            target = int(all(a == c for a in word))
            actual = source(word, list(range(12)))
            assert actual == target, (word, actual, target)
            checked += 1
            word_multiplicities[tuple(word)] += 1
    assert checked == 3 * 5**6
    assert len(word_multiplicities) == 46851
    assert Counter(word_multiplicities.values()) == {1: 46827, 2: 24}

    mixed = [1] * 4 + [0] * 8
    full = source(mixed, list(range(12)))
    restricted = source(mixed, [0, 1, 2, 3, 8, 9, 10, 11])
    assert full == 0 and restricted == 1

    # A failing full coefficient preserves the exact subsystem boundary.
    failure = [2] * 4 + [0] * 8
    assert source(failure, list(range(12))) == 1
    return {
        "status": "verified_exact_finite_control",
        "scope": "n12 exterior-resource control; not full GHZ",
        "independent_minority_assignments_including_three_pures": checked,
        "distinct_independent_minority_words": len(word_multiplicities),
        "word_multiplicity_histogram": dict(Counter(word_multiplicities.values())),
        "mixed_word": "".join(map(str, mixed)),
        "full_source": full,
        "literal_AC_source": restricted,
        "explicit_full_GHZ_failure": "".join(map(str, failure)),
        "failure_amplitude": 1,
        "crossings": [list(key) + [value] for key, value in CROSSINGS.items()],
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
