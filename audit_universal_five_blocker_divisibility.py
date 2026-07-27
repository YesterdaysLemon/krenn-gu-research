#!/usr/bin/env python3
"""Independent finite-field audit of the compression implication."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "UNIVERSAL_FIVE_BLOCKER_DIVISIBILITY_LEMMA.md"
PRIME = 3


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rank_two_column_matrix(entries: tuple[int, ...]) -> int:
    """Rank over F_3 of a row-major 3x2 matrix."""
    first = entries[0::2]
    second = entries[1::2]
    if not any(first) and not any(second):
        return 0
    if not any(first) or not any(second):
        return 1
    return (
        1
        if all(
            (first[i] * second[j] - first[j] * second[i]) % PRIME == 0
            for i in range(3)
            for j in range(i + 1, 3)
        )
        else 2
    )


def outer_difference_zero(
    a_entries: tuple[int, ...],
    c_entries: tuple[int, ...],
) -> bool:
    """Check A0*C1^T - A1*C0^T = 0 over F_3."""
    a0 = a_entries[0::2]
    a1 = a_entries[1::2]
    c0 = c_entries[0::2]
    c1 = c_entries[1::2]
    return all(
        (a0[row] * c1[column] - a1[row] * c0[column]) % PRIME
        == 0
        for row in range(3)
        for column in range(3)
    )


def main() -> None:
    matrices = tuple(itertools.product(range(PRIME), repeat=6))
    checked = 0
    zero_differences = 0
    rank_profile_counts: dict[str, int] = {}
    violations = []
    for a_entries in matrices:
        rank_a = rank_two_column_matrix(a_entries)
        for c_entries in matrices:
            checked += 1
            if not outer_difference_zero(a_entries, c_entries):
                continue
            zero_differences += 1
            rank_c = rank_two_column_matrix(c_entries)
            key = f"{rank_a},{rank_c}"
            rank_profile_counts[key] = rank_profile_counts.get(key, 0) + 1
            if rank_a > 1 and rank_c > 1:
                violations.append((a_entries, c_entries))

    assert checked == PRIME**12
    assert not violations
    assert sum(rank_profile_counts.values()) == zero_differences

    output = {
        "audited": True,
        "field": f"F_{PRIME}",
        "matrix_pairs_checked": checked,
        "zero_outer_differences": zero_differences,
        "rank_profile_counts": dict(sorted(rank_profile_counts.items())),
        "both_column_pairs_rank_two": 0,
        "compression_implication_verified": True,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "scope": "independent formula audit; written theorem is over C",
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT / "tmp" / "universal_five_blocker_divisibility_audited.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
