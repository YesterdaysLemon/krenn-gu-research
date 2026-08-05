#!/usr/bin/env python3
"""Independent audit of the common-singleton generic H31 obstruction."""

from __future__ import annotations

import itertools
import json

PERMUTATIONS = tuple(itertools.permutations(range(4)))
WORDS = tuple(itertools.product((0, 1), repeat=4))


def permanent(rows):
    return sum(
        product(rows[index][permutation[index]] for index in range(4))
        for permutation in PERMUTATIONS
    )


def product(values):
    result = 1
    for value in values:
        result *= value
    return result


def main() -> None:
    # Independently verify the pure marked-basis convention at the exact
    # rational component point from the component theorem.
    e = (1, 0, 0, 0)
    ell = (0, 1, -3, -2)
    v1 = (0, 1, -1, -1)
    v2 = (0, 1, -1, 2)
    v3 = (0, 1, 3, -1)
    alpha = (ell, e, e, e)
    canonical_beta = (e, v1, v2, v3)
    canonical_pure = {
        word: permanent(
            tuple(
                canonical_beta[mode] if word[mode] else alpha[mode] for mode in range(4)
            )
        )
        for word in WORDS
    }
    assert canonical_pure[(1, 1, 1, 1)] == 4
    assert all(
        value == 0 for word, value in canonical_pure.items() if word != (1, 1, 1, 1)
    )

    # Exhaust the multilinear expansion beta_i -> beta_i+h_i*alpha_i.
    # Of the sum_word 2^(number of beta rows)=3^4 expansion terms, only
    # the unreplaced all-beta term can use the sole nonzero canonical word.
    shift_terms_checked = 0
    surviving_shift_terms = []
    for word in WORDS:
        beta_modes = tuple(mode for mode, bit in enumerate(word) if bit)
        for replace_bits in itertools.product((0, 1), repeat=len(beta_modes)):
            canonical_word = list(word)
            replaced = []
            for mode, replace in zip(beta_modes, replace_bits, strict=True):
                if replace:
                    canonical_word[mode] = 0
                    replaced.append(mode)
            value = canonical_pure[tuple(canonical_word)]
            shift_terms_checked += 1
            if value:
                surviving_shift_terms.append((word, tuple(replaced), value))
    assert shift_terms_checked == 3**4
    assert surviving_shift_terms == [((1, 1, 1, 1), (), 4)]

    # Rebuild the all-kernel extension diagonal directly.  The symbolic
    # support pattern makes the proof independent of all parameter values.
    alpha_supports = ({1, 2, 3}, {0}, {0}, {0})
    deletion_audit = []
    for deleted in range(4):
        retained = tuple(index for index in range(4) if index != deleted)
        row_supports = tuple(
            {
                retained.index(coordinate)
                for coordinate in alpha_supports[mode]
                if coordinate in retained
            }
            | {3}
            for mode in range(4)
        )
        surviving_permutations = tuple(
            permutation
            for permutation in PERMUTATIONS
            if all(permutation[index] in row_supports[index] for index in range(4))
        )
        assert surviving_permutations == ()
        support_union = set().union(*(row_supports[mode] for mode in (1, 2, 3)))
        expected_support_size = 1 if deleted == 0 else 2
        assert len(support_union) == expected_support_size
        deletion_audit.append(
            {
                "deleted_coordinate": deleted,
                "last_three_kernel_support_size": len(support_union),
                "surviving_permanent_monomials": 0,
                "all_kernel_diagonal": 0,
            }
        )

    print(
        json.dumps(
            {
                "status": "pass",
                "field": "C",
                "sample_marked_pure_support": {"1111": 4},
                "shift_expansion_terms_checked": shift_terms_checked,
                "permutations_per_diagonal": len(PERMUTATIONS),
                "deletions": deletion_audit,
                "generic_marked_H31_fibre_empty": True,
                "role": "independent support-and-permutation audit",
                "search_used": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
