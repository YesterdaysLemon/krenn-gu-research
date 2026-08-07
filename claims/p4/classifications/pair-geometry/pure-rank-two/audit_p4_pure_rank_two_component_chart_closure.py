#!/usr/bin/env python3
"""Independent finite-field audit of the component chart closure."""

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
THEOREM = HERE / "P4_PURE_RANK_TWO_COMPONENT_CHART_CLOSURE.md"
PRIMARY = HERE / "verify_p4_pure_rank_two_component_chart_closure.py"
WORDS = tuple(itertools.product((0, 1), repeat=4))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inverse(value: int, prime: int) -> int:
    return pow(value % prime, -1, prime)


def permanent_dp(rows: tuple[tuple[int, ...], ...], prime: int) -> int:
    table = {0: 1}
    for row in rows:
        next_table: dict[int, int] = {}
        for mask, subtotal in table.items():
            for column in range(4):
                if mask & (1 << column):
                    continue
                new_mask = mask | (1 << column)
                next_table[new_mask] = (
                    next_table.get(new_mask, 0)
                    + subtotal * row[column]
                ) % prime
        table = next_table
    return table[15]


def audit_prime(prime: int) -> dict[str, int]:
    points = 0
    family_points = 0
    nonzero_boundary_points = 0
    zero_tensor_points = 0
    for h in range(1, prime):
        for n in range(1, prime):
            for a, d, e in itertools.product(range(prime), repeat=3):
                points += 1
                D = (d + h * n * e) % prime
                coordinates = (
                    a, h * (a - n), D * inverse(h, prime), d,
                    e, 0, 0, h,
                    0, h * n * e, -inverse(n, prime), 0,
                    0, n, 0, -inverse(h, prime),
                )
                (
                    aa, b, c, dd, ee, f, g, hh,
                    i, j, k, ell, m, nn, o, p,
                ) = tuple(value % prime for value in coordinates)
                rows = (
                    ((1, 0, aa, b), (0, 1, c, dd)),
                    ((ee, 1, 0, f), (g, 0, 1, hh)),
                    ((i, 1, 0, j), (k, 0, 1, ell)),
                    ((1, m, nn, 0), (0, o, p, 1)),
                )
                coefficients = {
                    word: permanent_dp(
                        tuple(rows[mode][word[mode]] for mode in range(4)),
                        prime,
                    )
                    for word in WORDS
                }
                expected = {word: 0 for word in WORDS}
                expected[(0, 0, 0, 0)] = 2 * a * e * h * n % prime
                expected[(0, 1, 0, 0)] = 2 * a * h % prime
                expected[(1, 0, 0, 0)] = 2 * e * n * D % prime
                expected[(1, 1, 0, 0)] = 2 * D % prime
                assert coefficients == expected
                is_zero = not any(coefficients.values())
                assert is_zero == (a == 0 and D == 0)
                if D:
                    family_points += 1
                    Q = -a * h * inverse(D, prime) % prime
                    assert (
                        -Q * D * inverse(h, prime) % prime
                    ) == a
                elif a:
                    nonzero_boundary_points += 1
                else:
                    zero_tensor_points += 1
    assert points == (prime - 1) ** 2 * prime**3
    assert (
        family_points + nonzero_boundary_points + zero_tensor_points
        == points
    )
    return {
        "component_chart_points": points,
        "family_open_points": family_points,
        "nonzero_boundary_points": nonzero_boundary_points,
        "zero_tensor_points": zero_tensor_points,
    }


def main() -> None:
    audits = {
        str(prime): audit_prime(prime)
        for prime in (5, 7)
    }
    output = {
        "audited": True,
        "independent_of_primary_imports": True,
        "method": "complete free-chart audit with DP permanent",
        "finite_fields": ["F_5", "F_7"],
        "audits": audits,
        "ambient_grassmannians_enumerated": 0,
        "all_components_classified": False,
        "scope": "finite-field audit; written identities are over C",
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "primary": PRIMARY.name,
        "primary_sha256": sha256(PRIMARY),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        REPO_ROOT / "tmp" / "p4_pure_rank_two_component_chart_closure_audit.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
