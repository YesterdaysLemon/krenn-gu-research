#!/usr/bin/env python3
"""Independent audit of the component-20 p+q valuative boundary note.

The symbolic identities are exact.  The integer scans are bounded regression
audits and are not used as proof of any characteristic-zero classification.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P4_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY.md"
COMPONENT = ROOT / "P4_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT.md"
WORDS = tuple(itertools.product((0, 1), repeat=4))
PERMUTATIONS = tuple(itertools.permutations(range(4)))
PAIRS = tuple(itertools.combinations(range(4), 2))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent(rows: tuple[sp.Matrix, ...]) -> sp.Expr:
    return sp.factor(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(4))
            for permutation in PERMUTATIONS
        )
    )


def wedge(left: sp.Matrix, right: sp.Matrix) -> tuple[sp.Expr, ...]:
    return tuple(sp.factor(left[i] * right[j] - left[j] * right[i]) for i, j in PAIRS)


def symmetric_product(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [sp.expand(left[i] * right[j] + left[j] * right[i]) for i, j in PAIRS]
    )


def product_matrix(
    left: tuple[sp.Matrix, sp.Matrix], right: tuple[sp.Matrix, sp.Matrix]
) -> sp.Matrix:
    return sp.Matrix.hstack(
        *(
            symmetric_product(left_row, right_row)
            for left_row in left
            for right_row in right
        )
    )


def tensor(
    planes: tuple[tuple[sp.Matrix, sp.Matrix], ...],
) -> dict[tuple[int, ...], sp.Expr]:
    return {
        word: permanent(tuple(planes[i][word[i]] for i in range(4))) for word in WORDS
    }


def normalized_family_audit() -> dict[str, object]:
    p, q = sp.symbols("p q")
    delta = p + q
    s = p - q + 1
    e = sp.Matrix((1, 0, 0, 0))
    alpha = (
        sp.Matrix((0, -p * (p + 1), q * (q - 1), s)),
        e,
        e,
        sp.Matrix((1, 1, 1, 0)),
    )
    beta = (
        sp.Matrix((-s, -delta, delta, 0)),
        sp.Matrix((0, p + 1, q - 1, 1)),
        sp.Matrix((0, p, q, 1)),
        e,
    )
    expected_wedge = (
        -p * (p + 1) * s,
        q * (q - 1) * s,
        s**2,
        -(delta**2) * s,
        delta * s,
        -delta * s,
    )
    actual_wedge = wedge(alpha[0], beta[0])
    assert all(
        sp.factor(actual - expected) == 0
        for actual, expected in zip(actual_wedge, expected_wedge)
    )
    coefficients = tensor(tuple(zip(alpha, beta)))
    nonzero = {word: value for word, value in coefficients.items() if value != 0}
    assert tuple(nonzero) == ((1, 1, 1, 1),)
    assert sp.factor(nonzero[(1, 1, 1, 1)] - 2 * delta * s) == 0
    return {
        "mode_zero_wedge": [str(value) for value in actual_wedge],
        "only_nonzero_pure_coefficient": "T1111=2*(p+q)*(p-q+1)",
    }


def chart_audit() -> dict[str, object]:
    e = sp.Matrix((1, 0, 0, 0))
    cap_a = sp.Matrix((0, 1, 0, 0))
    cap_b = sp.Matrix((0, 0, 1, 0))
    cap_c = sp.Matrix((0, 0, 0, 1))
    ell = cap_a - cap_b
    em = cap_a + cap_b
    a, lam = sp.symbols("a lambda", nonzero=True)
    mu = -a * (a + 1) / (2 * a + 1)

    full = (
        (e + lam * ell, cap_c + mu * ell),
        (e, (a + 1) * ell + cap_c),
        (e, a * ell + cap_c),
        (e, em),
    )
    drop = (
        (cap_c, ell),
        (e, (a + 1) * ell + cap_c),
        (e, a * ell + cap_c),
        (e, em),
    )
    full_tensor = {word: value for word, value in tensor(full).items() if value != 0}
    drop_tensor = {word: value for word, value in tensor(drop).items() if value != 0}
    assert tuple(full_tensor) == ((0, 1, 1, 0),)
    assert sp.factor(full_tensor[(0, 1, 1, 0)] + 2 * lam * (2 * a + 1)) == 0
    assert tuple(drop_tensor) == ((0, 1, 1, 0), (1, 1, 1, 0))
    assert sp.factor(drop_tensor[(0, 1, 1, 0)] + 2 * a * (a + 1)) == 0
    assert sp.factor(drop_tensor[(1, 1, 1, 0)] + 2 * (2 * a + 1)) == 0

    def pair_profile(
        planes: tuple[tuple[sp.Matrix, sp.Matrix], ...],
    ) -> tuple[int, ...]:
        return tuple(
            product_matrix(planes[left], planes[right]).rank() for left, right in PAIRS
        )

    assert pair_profile(full) == (4, 4, 4, 3, 3, 3)
    assert pair_profile(drop) == (4, 4, 3, 3, 3, 3)

    c1, c2, k = sp.symbols("c1 c2 k", nonzero=True)
    residue_ell = c1 * cap_a - c2 * cap_b
    residue_em = c1 * cap_a + c2 * cap_b
    half = (
        (residue_ell, cap_c - k * e),
        (e, sp.Rational(1, 2) * residue_ell + cap_c),
        (e, -sp.Rational(1, 2) * residue_ell + cap_c),
        (e, residue_em),
    )
    half_tensor = {word: value for word, value in tensor(half).items() if value != 0}
    assert tuple(half_tensor) == ((1, 1, 1, 0),)
    assert pair_profile(half) == (4, 4, 3, 3, 3, 3)
    assert wedge(*half[0]) == (k * c1, -k * c2, 0, 0, c1, -c2)

    kappa, delta_lead, alpha_lead = sp.symbols("kappa Delta alpha", nonzero=True)
    infinity_planes = {
        "interior_baseline": (residue_ell, cap_c),
        "interior_x0_wall": (residue_ell, cap_c + kappa * e),
        "lower_y_wall": (
            residue_ell,
            cap_c - sp.Rational(1, 2) * delta_lead * residue_em,
        ),
        "lower_y_and_x0_wall": (
            residue_ell,
            cap_c + kappa * e - sp.Rational(1, 2) * delta_lead * residue_em,
        ),
        "upper_y_and_x0_wall": (
            residue_ell + alpha_lead * e,
            cap_c + kappa * e,
        ),
    }
    infinity_wedges = {label: wedge(*plane) for label, plane in infinity_planes.items()}
    expected = {
        "interior_baseline": (0, 0, 0, 0, c1, -c2),
        "interior_x0_wall": (-kappa * c1, kappa * c2, 0, 0, c1, -c2),
        "lower_y_wall": (0, 0, 0, -delta_lead * c1 * c2, c1, -c2),
        "lower_y_and_x0_wall": (
            -kappa * c1,
            kappa * c2,
            0,
            -delta_lead * c1 * c2,
            c1,
            -c2,
        ),
        "upper_y_and_x0_wall": (
            -kappa * c1,
            kappa * c2,
            alpha_lead,
            0,
            c1,
            -c2,
        ),
    }
    assert infinity_wedges == expected
    support_pair_rank = product_matrix((e, residue_ell), (e, residue_ell)).rank()
    full_pair_rank = product_matrix(
        (e, residue_ell + cap_c), (e, residue_ell + cap_c)
    ).rank()
    assert support_pair_rank == full_pair_rank == 2
    return {
        "B_full_nonzero_tensor": {
            "".join(map(str, word)): str(value) for word, value in full_tensor.items()
        },
        "B_full_pair_profile": list(pair_profile(full)),
        "B_drop_nonzero_tensor": {
            "".join(map(str, word)): str(value) for word, value in drop_tensor.items()
        },
        "B_drop_pair_profile": list(pair_profile(drop)),
        "a=-1/2_nonzero_tensor": {
            "".join(map(str, word)): str(value) for word, value in half_tensor.items()
        },
        "a=-1/2_pair_profile": list(pair_profile(half)),
        "infinity_mode_zero_wedges": {
            label: [str(value) for value in values]
            for label, values in infinity_wedges.items()
        },
        "infinity_repeated_pair_ranks": [support_pair_rank, full_pair_rank],
    }


def audit_scan(
    label: str,
    parameters: tuple[tuple[int, ...], ...],
    weight_range: range,
    expression,
    target,
) -> dict[str, object]:
    checked = 0
    zero_cases = 0
    target_cases = 0
    for parameter_values in parameters:
        for x0 in weight_range:
            for x1 in weight_range:
                for x2 in weight_range:
                    value = expression(*parameter_values, x0, x1, x2)
                    expected = target(*parameter_values, x0, x1, x2)
                    checked += 1
                    zero_cases += value == 0
                    target_cases += expected
                    assert value >= 0
                    assert (value == 0) == expected
    return {
        "label": label,
        "integer_points_checked": checked,
        "zero_cases": zero_cases,
        "target_cases": target_cases,
        "mismatches": 0,
        "scope": "bounded integer regression audit only",
    }


def bounded_scans() -> list[dict[str, object]]:
    weights = range(-5, 10)

    def common_terms(d: int, x0: int, x1: int, x2: int):
        n = min(x1, x2)
        z = min(x0, x1, x2)
        ell = min(x1 + x2 + d, x1, x2)
        return n, z, ell

    def generic_e(d: int, x0: int, x1: int, x2: int) -> int:
        m = min(x1, x2, 0)
        n, _, ell = common_terms(d, x0, x1, x2)
        return d + x1 + x2 - m + min(x0, n) - n - min(x0 + m, d + ell)

    def generic_target(d: int, x0: int, x1: int, x2: int) -> bool:
        return x1 == x2 and -d <= x1 <= 0 and x0 >= d

    scans = [
        audit_scan(
            "generic finite centre",
            tuple((d,) for d in range(1, 5)),
            weights,
            generic_e,
            generic_target,
        )
    ]

    exceptional_parameters = []
    for cap_p in range(1, 4):
        for cap_q in range(1, 4):
            if cap_p == cap_q:
                exceptional_parameters.extend(
                    (cap_p, cap_q, d) for d in range(cap_p, cap_p + 3)
                )
            else:
                exceptional_parameters.append((cap_p, cap_q, min(cap_p, cap_q)))

    def exceptional_e(
        cap_p: int,
        cap_q: int,
        d: int,
        x0: int,
        x1: int,
        x2: int,
    ) -> int:
        n, z, ell = common_terms(d, x0, x1, x2)
        g = min(x1 + cap_p, x2 + cap_q, 0)
        m = min(x1, x2, 0)
        return d + x1 + x2 - m + z - n - min(x0 + g, d + ell)

    def exceptional_target(
        cap_p: int,
        cap_q: int,
        d: int,
        x0: int,
        x1: int,
        x2: int,
    ) -> bool:
        cap_r = min(cap_p, cap_q)
        return x1 == x2 and -d <= x1 <= 0 and x0 >= max(d - cap_r, d + x1)

    scans.append(
        audit_scan(
            "a=0 and a=-1 raw A0 schema",
            tuple(exceptional_parameters),
            weights,
            exceptional_e,
            exceptional_target,
        )
    )

    def half_e(d: int, h: int, x0: int, x1: int, x2: int) -> int:
        n, z, ell = common_terms(d, x0, x1, x2)
        g = min(x1, x2, h)
        m = min(x1, x2, 0)
        return d + x1 + x2 + g - 2 * m + z - n - min(x0 + g, d + ell)

    def half_target(d: int, h: int, x0: int, x1: int, x2: int) -> bool:
        del h
        return x1 == x2 and -d <= x1 <= 0 and x0 >= d

    scans.append(
        audit_scan(
            "a=-1/2 raw AH schema",
            tuple((d, h) for d in range(1, 4) for h in range(1, 4)),
            weights,
            half_e,
            half_target,
        )
    )

    def infinity_e(d: int, r: int, x0: int, x1: int, x2: int) -> int:
        n, z, ell = common_terms(d, x0, x1, x2)
        g = min(x1 + 2 * r, x2 + 2 * r, r)
        b = min(x1 + r, x2 + r, 0)
        return d + x1 + x2 + g - 2 * b + z - n - min(x0 + g, d + ell)

    def infinity_target(d: int, r: int, x0: int, x1: int, x2: int) -> bool:
        return x1 == x2 and -d <= x1 <= -r and x0 >= d - 2 * r

    scans.append(
        audit_scan(
            "infinity raw INF schema",
            tuple((d, r) for d in range(1, 4) for r in range(-3, 0)),
            weights,
            infinity_e,
            infinity_target,
        )
    )
    return scans


def git_commit() -> str:
    completed = subprocess.run(
        ("git", "rev-parse", "HEAD"),
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
    )
    return completed.stdout.strip()


def main() -> None:
    family = normalized_family_audit()
    charts = chart_audit()
    scans = bounded_scans()
    print(
        json.dumps(
            {
                "status": "pass",
                "claim_label": "DERIVED",
                "role": "verifier",
                "date_utc": datetime.now(UTC).isoformat(),
                "git_commit": git_commit(),
                "scope": (
                    "independent exact reconstruction and bounded audit of the "
                    "component-20 p+q diagonal-source-torus boundary"
                ),
                "inputs": {
                    THEOREM.name: sha256(THEOREM),
                    COMPONENT.name: sha256(COMPONENT),
                },
                "method": (
                    "fresh SymPy exterior/permanent/rank reconstruction plus "
                    "bounded integer min-plus regression scans"
                ),
                "command": (
                    "uv run --with sympy python "
                    "audit_p4_common_active_binary_triangle_p_plus_q_boundary.py"
                ),
                "outputs": {},
                "limitations": (
                    "bounded scans are audit-only; no arbitrary GL4, H31, H22, "
                    "older-component placement, local-to-global, or global closure"
                ),
                "normalized_family": family,
                "boundary_charts": charts,
                "bounded_integer_scans": scans,
                "imports_primary_verifier": False,
                "classification_proof_independently_replayed": False,
                "bounded_scan_used_as_proof": False,
                "finite_field_computation_used": False,
                "arbitrary_GL4_used": False,
                "older_component_intersection_placement_closed": False,
                "H31_closed": False,
                "H22_closed": False,
                "global_Krenn_Gu_conjecture_resolved": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
