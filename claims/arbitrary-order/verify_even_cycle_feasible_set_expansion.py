"""Exhaustively verify the even-cycle deletion/completion formula through 14."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def brute_count(length: int, deleted_mask: int) -> int:
    remaining = ((1 << length) - 1) ^ deleted_mask

    def recurse(mask: int) -> int:
        if not mask:
            return 1
        first_bit = mask & -mask
        first = first_bit.bit_length() - 1
        total = 0
        for second in ((first - 1) % length, (first + 1) % length):
            second_bit = 1 << second
            if mask & second_bit:
                total += recurse(mask ^ first_bit ^ second_bit)
        return total

    return recurse(remaining)


def predicted_count(length: int, deleted_mask: int) -> int:
    deleted = [
        vertex
        for vertex in range(length)
        if deleted_mask & (1 << vertex)
    ]
    if not deleted:
        return 2
    for index, first in enumerate(deleted):
        second = deleted[(index + 1) % len(deleted)]
        distance = (second - first) % length
        if distance % 2 == 0:
            return 0
    return 1


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/even_cycle_feasible_set_expansion_verified.json"
        ),
    )
    args = parser.parse_args()

    cases = 0
    distributions: dict[str, dict[str, int]] = {}
    for length in range(4, 15, 2):
        counts = {0: 0, 1: 0, 2: 0}
        for deleted_mask in range(1 << length):
            brute = brute_count(length, deleted_mask)
            predicted = predicted_count(length, deleted_mask)
            if brute != predicted:
                raise AssertionError(
                    f"C{length}, mask {deleted_mask}: "
                    f"brute={brute}, predicted={predicted}"
                )
            counts[brute] += 1
            cases += 1
        distributions[str(length)] = {
            str(value): count for value, count in counts.items()
        }

    payload = {
        "verified": True,
        "status": "even_cycle_feasible_set_expansion_verified",
        "cycle_lengths": list(range(4, 15, 2)),
        "deleted_vertex_sets_checked": cases,
        "completion_count_distributions": distributions,
        "product_extension": (
            "counts multiply over vertex-disjoint cycle components"
        ),
        "global_conjecture_resolved": False,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
