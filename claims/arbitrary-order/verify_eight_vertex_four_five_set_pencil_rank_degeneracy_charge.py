#!/usr/bin/env python3
"""Exact finite audit of the fixed-pencil rank-degeneracy charge lemma.

This verifier checks only the integer bookkeeping in equations (8)--(11) of
``EIGHT_VERTEX_FOUR_FIVE_SET_PENCIL_RANK_DEGENERACY_COMPONENT_LEDGER_WORKING_NOTE.md``.
It does not prove the geometric circuit, incidence, or cross-ratio lemmas and
does not change the candidate status of that working note.

The six labels below are the six repeated chart pairs.  A ruling-pair circuit
occurs exactly between complementary labels.  The exhaustive search counts
active--active and active--structural edges, but deliberately excludes
structural--structural edges because those are already present in the generic
predecessor rank.
"""

from __future__ import annotations

from collections import Counter
from itertools import product
import json


LABELS = tuple(range(6))
COMPLEMENTARY_LABEL_PAIRS = ((0, 5), (1, 4), (2, 3))
COMPLEMENT = {
    left: right
    for pair in COMPLEMENTARY_LABEL_PAIRS
    for left, right in (pair, pair[::-1])
}

EXPECTED_RULING_MAXIMA = {
    (0, 0): 0,
    (0, 1): 0,
    (0, 2): 0,
    (0, 3): 0,
    (0, 4): 0,
    (1, 0): 0,
    (1, 1): 1,
    (1, 2): 2,
    (1, 3): 3,
    (2, 0): 1,
    (2, 1): 2,
    (2, 2): 4,
    (3, 0): 2,
    (3, 1): 4,
    (4, 0): 4,
}

EXPECTED_FIXED_ACTIVE_MAXIMA = {0: 3, 1: 2, 2: 3, 3: 2, 4: 0}
EXPECTED_GLOBAL_EXTREMALS = {
    (0, 0, 0, 0, 4, 0),
    (2, 2, 0, 0, 0, 2),
}


def ruling_edge_count(
    active_labels: tuple[int, ...], structural_labels: tuple[int, ...]
) -> int:
    """Count new complementary edges, excluding structural--structural edges."""

    active = Counter(active_labels)
    structural = Counter(structural_labels)
    formula_count = sum(
        active[left] * active[right]
        + active[left] * structural[right]
        + active[right] * structural[left]
        for left, right in COMPLEMENTARY_LABEL_PAIRS
    )

    direct_active_active = sum(
        active_labels[j] == COMPLEMENT[active_labels[i]]
        for i in range(len(active_labels))
        for j in range(i + 1, len(active_labels))
    )
    direct_active_structural = sum(
        structural_label == COMPLEMENT[active_label]
        for active_label in active_labels
        for structural_label in structural_labels
    )
    direct_count = direct_active_active + direct_active_structural
    assert formula_count == direct_count
    return formula_count


def ruling_maximum(r: int, u: int) -> tuple[int, tuple[int, ...], int]:
    """Return R(r,u), a lexicographically first witness, and witness count."""

    maximum = -1
    first_witness: tuple[int, ...] | None = None
    witness_count = 0
    for labels in product(LABELS, repeat=r + u):
        score = ruling_edge_count(labels[:r], labels[r:])
        if score > maximum:
            maximum = score
            first_witness = labels
            witness_count = 1
        elif score == maximum:
            witness_count += 1
    assert first_witness is not None
    return maximum, first_witness, witness_count


def integer_partitions(total: int, ceiling: int | None = None):
    """Yield nonincreasing integer partitions of ``total``."""

    if total == 0:
        yield ()
        return
    bound = total if ceiling is None else min(total, ceiling)
    for first in range(bound, 0, -1):
        for tail in integer_partitions(total - first, first):
            yield (first,) + tail


def class_gain(size: int) -> int:
    """Net pairwise rank loss after the size-1 compatibility equations."""

    return 0 if size <= 1 else size * (size - 1) // 2 - (size - 1)


def cross_ratio_maximum(k: int) -> tuple[int, tuple[int, ...]]:
    """Audit that splitting k vertices into classes never beats one class."""

    scored = tuple(
        (sum(class_gain(size) for size in partition), partition)
        for partition in integer_partitions(k)
    )
    return max(scored, key=lambda item: (item[0], item[1]))


def verify() -> dict[str, object]:
    ruling_table: dict[tuple[int, int], int] = {}
    ruling_witnesses: dict[str, object] = {}
    for r in range(5):
        for u in range(5 - r):
            maximum, witness, witness_count = ruling_maximum(r, u)
            ruling_table[r, u] = maximum
            ruling_witnesses[f"{r},{u}"] = {
                "first_label_witness": witness,
                "labelled_witness_count": witness_count,
            }
    assert ruling_table == EXPECTED_RULING_MAXIMA

    cross_ratio_table = {}
    for k in range(5):
        maximum, partition = cross_ratio_maximum(k)
        expected = class_gain(k)
        assert maximum == expected
        cross_ratio_table[str(k)] = {
            "maximum": maximum,
            "first_maximizing_partition": partition,
        }

    # Tuple order: (a, r, u, f, s, p).
    charge_rows: list[tuple[int, tuple[int, int, int, int, int, int]]] = []
    for a in range(5):
        for r in range(a + 1):
            for f in range(a - r + 1):
                for u in range(5 - a):
                    for s in range(5 - a - u):
                        for p in range(5 - a - u - s):
                            gain = (
                                a * p
                                - a
                                + ruling_table[r, u]
                                + class_gain(f + s)
                            )
                            charge_rows.append((gain, (a, r, u, f, s, p)))

    fixed_active_maxima = {
        a: max(gain for gain, parameters in charge_rows if parameters[0] == a)
        for a in range(5)
    }
    assert fixed_active_maxima == EXPECTED_FIXED_ACTIVE_MAXIMA

    global_maximum = max(gain for gain, _ in charge_rows)
    global_extremals = {
        parameters for gain, parameters in charge_rows if gain == global_maximum
    }
    assert global_maximum == 3
    assert global_extremals == EXPECTED_GLOBAL_EXTREMALS

    return {
        "scope": "integer charge bookkeeping only",
        "ruling_maxima": {
            f"{r},{u}": ruling_table[r, u] for r, u in sorted(ruling_table)
        },
        "ruling_witnesses": ruling_witnesses,
        "cross_ratio_maxima": cross_ratio_table,
        "fixed_active_maxima": {
            str(a): fixed_active_maxima[a] for a in range(5)
        },
        "global_maximum": global_maximum,
        "global_extremals_a_r_u_f_s_p": sorted(global_extremals),
        "status": "PASS",
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
