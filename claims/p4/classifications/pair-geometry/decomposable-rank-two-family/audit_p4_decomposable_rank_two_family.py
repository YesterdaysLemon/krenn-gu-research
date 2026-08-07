#!/usr/bin/env python3
"""Independent exact-integer audit of the rank-two P4 family."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


import sys

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
THEOREM = HERE / "P4_DECOMPOSABLE_RANK_TWO_FAMILY.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent_dynamic(rows: tuple[tuple[int, ...], ...]) -> int:
    states = {0: 1}
    for row in rows:
        next_states: dict[int, int] = {}
        for mask, coefficient in states.items():
            for column, value in enumerate(row):
                if mask & (1 << column):
                    continue
                new_mask = mask | (1 << column)
                next_states[new_mask] = (
                    next_states.get(new_mask, 0) + coefficient * value
                )
        states = next_states
    return states[(1 << len(rows)) - 1]


def has_rank_two(
    upper: tuple[int, ...],
    lower: tuple[int, ...],
) -> bool:
    return any(
        upper[first] * lower[second]
        - upper[second] * lower[first]
        for first, second in itertools.combinations(range(4), 2)
    )


def main() -> None:
    upper = (
        (0, 1, 1, 0),
        (0, 0, 1, 1),
        (0, 1, 0, 1),
        (1, 0, 1, 0),
    )
    lower = (
        (1, 0, 0, -1),
        (1, 1, -1, -1),
        (-1, 0, 1, 0),
        (0, 0, -1, 1),
    )

    coefficients = {}
    for bits in itertools.product((0, 1), repeat=4):
        rows = tuple(
            lower[index] if bit else upper[index]
            for index, bit in enumerate(bits)
        )
        coefficients["".join(map(str, bits))] = permanent_dynamic(rows)

    expected = {word: 0 for word in coefficients}
    expected["0000"] = 2
    assert coefficients == expected
    assert all(
        has_rank_two(upper[index], lower[index])
        for index in range(4)
    )

    prime_reductions = {}
    for prime in (3, 5, 7):
        reduced = {
            word: value % prime for word, value in coefficients.items()
        }
        assert reduced["0000"] == 2 % prime
        assert all(
            value == 0
            for word, value in reduced.items()
            if word != "0000"
        )
        prime_reductions[str(prime)] = reduced["0000"]

    output = {
        "audited": True,
        "domain": "Z",
        "algorithm": "row-by-row subset dynamic programming",
        "target_words_checked": len(coefficients),
        "pure_coefficient": coefficients["0000"],
        "mixed_coefficients_nonzero": 0,
        "local_ranks": [2, 2, 2, 2],
        "prime_reductions_of_pure_coefficient": prime_reductions,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "scope": "exact integer point auditing the symbolic family",
        "global_conjecture_resolved": False,
    }
    output_path = (
        REPO_ROOT / "tmp" / "p4_decomposable_rank_two_family_audited.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
