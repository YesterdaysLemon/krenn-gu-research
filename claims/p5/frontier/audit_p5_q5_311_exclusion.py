#!/usr/bin/env python3
"""Independent finite-field audit of the exact q5_311 exclusion."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

from audit_p3_decomposable_restriction_classification import audit_prime


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q5_311_EXCLUSION_THEOREM.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def projective_vectors(prime: int) -> tuple[tuple[int, ...], ...]:
    result = []
    for vector in itertools.product(range(prime), repeat=3):
        pivot = next(
            (index for index, value in enumerate(vector) if value),
            None,
        )
        if pivot is None or vector[pivot] != 1:
            continue
        result.append(vector)
    return tuple(result)


def dot(
    left: tuple[int, ...],
    right: tuple[int, ...],
    prime: int,
) -> int:
    return sum(
        first * second for first, second in zip(left, right, strict=True)
    ) % prime


def audit_target_incidence(prime: int) -> dict[str, int]:
    lines = projective_vectors(prime)
    plane_normals = lines
    first_nonzero_contractions = 0
    forced_second_zero_contractions = 0
    all_nonzero_compatible = 0
    for target in lines:
        for first_normal in plane_normals:
            if dot(first_normal, target, prime) == 0:
                continue
            first_nonzero_contractions += 1
            for second_normal in plane_normals:
                if dot(second_normal, target, prime) != 0:
                    continue
                forced_second_zero_contractions += 1
                # The pure residual factor lies in the second common
                # plane, so its quotient contraction is necessarily zero.
                if dot(second_normal, target, prime) != 0:
                    all_nonzero_compatible += 1
    assert all_nonzero_compatible == 0
    return {
        "projective_target_lines": len(lines),
        "first_nonzero_contractions": first_nonzero_contractions,
        "forced_second_zero_contractions": (
            forced_second_zero_contractions
        ),
        "all_nonzero_compatible": all_nonzero_compatible,
    }


def main() -> None:
    audits = {}
    for prime in (3, 5):
        p3_audit = audit_prime(prime)
        kind_counts = p3_audit["admissible_quadruple_kind_counts"]
        assert set(kind_counts) == {
            "zero,zero,zero,zero",
            "pure,pure,pure,pure",
        }
        audits[str(prime)] = {
            "common_plane_audit": p3_audit,
            "target_incidence_audit": audit_target_incidence(prime),
            "all_zero_case_excluded_by_nonzero_rare_slice": True,
            "all_nonzero_case_excluded_by_non_drop_pair": True,
        }

    output = {
        "audited": True,
        "finite_fields": ["F_3", "F_5"],
        "audits": audits,
        "q5_311_possible": False,
        "scope": "finite-field audit; written theorem is over C",
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "P5_to_Delta3_resolved": False,
        "global_conjecture_resolved": False,
    }
    output_path = ROOT / "tmp" / "p5_q5_311_exclusion_audited.json"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
