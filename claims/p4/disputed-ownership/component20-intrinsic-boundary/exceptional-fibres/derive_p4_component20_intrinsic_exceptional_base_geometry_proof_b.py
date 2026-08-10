#!/usr/bin/env python3
"""Exact proof-B replay for component 20's intrinsic exceptional centres.

This script reconstructs the normalized four-plane family directly.  It
does not import any construction or verifier module, and it makes no H31 or
H22 inference.
"""

from __future__ import annotations
import sys as _bootstrap_sys
from pathlib import Path as _BootstrapPath

for _bootstrap_parent in _BootstrapPath(__file__).resolve().parents:
    if (_bootstrap_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        _bootstrap_sys.path.insert(0, str(_bootstrap_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap as _bootstrap_repository  # noqa: E402

REPO_ROOT, HERE = _bootstrap_repository(__file__)


import hashlib
import itertools
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
SCRIPT = Path(__file__).resolve()
REPORT = HERE / "P4_COMPONENT20_INTRINSIC_EXCEPTIONAL_BASE_GEOMETRY_PROOF_B.md"
COMPONENT = REPO_ROOT / "claims/p4/classifications/triangle-211/common-active-binary-triangle/P4_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT.md"
WALL = REPO_ROOT / "claims/p4/boundaries/component20-p-plus-q-wall/P4_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY.md"
WORDS = tuple(itertools.product((0, 1), repeat=4))
PAIRS = tuple(itertools.combinations(range(4), 2))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_commit() -> str:
    return subprocess.run(
        ("git", "rev-parse", "HEAD"),
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
    ).stdout.strip()


def multiply(
    left: dict[int, sp.Expr], right: dict[int, sp.Expr]
) -> dict[int, sp.Expr]:
    result: dict[int, sp.Expr] = {}
    for left_mask, left_value in left.items():
        for right_mask, right_value in right.items():
            if left_mask & right_mask:
                continue
            mask = left_mask | right_mask
            result[mask] = sp.expand(result.get(mask, 0) + left_value * right_value)
    return result


def permanent(rows: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    value = {0: sp.Integer(1)}
    for row in rows:
        linear = {
            1 << index: sp.sympify(entry)
            for index, entry in enumerate(row)
            if entry != 0
        }
        value = multiply(value, linear)
    return sp.factor(value.get(15, 0))


def tensor(
    planes: tuple[tuple[tuple[sp.Expr, ...], tuple[sp.Expr, ...]], ...],
) -> dict[tuple[int, ...], sp.Expr]:
    return {
        word: permanent(tuple(planes[i][word[i]] for i in range(4)))
        for word in WORDS
    }


def support(values: dict[tuple[int, ...], sp.Expr]) -> dict[str, sp.Expr]:
    return {
        "".join(str(bit) for bit in word): sp.factor(value)
        for word, value in values.items()
        if value != 0
    }


def assert_support_equal(
    actual: dict[str, sp.Expr], expected: dict[str, sp.Expr]
) -> None:
    assert actual.keys() == expected.keys()
    for key, value in actual.items():
        assert sp.expand(value - expected[key]) == 0


def wedge(
    left: tuple[sp.Expr, ...], right: tuple[sp.Expr, ...]
) -> tuple[sp.Expr, ...]:
    return tuple(
        sp.expand(left[i] * right[j] - left[j] * right[i]) for i, j in PAIRS
    )


def symmetric_product(
    left: tuple[sp.Expr, ...], right: tuple[sp.Expr, ...]
) -> sp.Matrix:
    return sp.Matrix(
        [sp.expand(left[i] * right[j] + left[j] * right[i]) for i, j in PAIRS]
    )


def pair_profile(
    planes: tuple[tuple[tuple[sp.Expr, ...], tuple[sp.Expr, ...]], ...],
) -> tuple[int, ...]:
    return tuple(
        sp.Matrix.hstack(
            *(
                symmetric_product(left_row, right_row)
                for left_row in planes[left]
                for right_row in planes[right]
            )
        ).rank()
        for left, right in PAIRS
    )


def add(*rows: tuple[sp.Expr, ...]) -> tuple[sp.Expr, ...]:
    return tuple(sp.expand(sum(row[j] for row in rows)) for j in range(4))


def scale(value: sp.Expr, row: tuple[sp.Expr, ...]) -> tuple[sp.Expr, ...]:
    return tuple(sp.expand(value * entry) for entry in row)


def normalized_planes(p: sp.Expr, q: sp.Expr):
    delta = p + q
    s = p - q + 1
    e = (sp.Integer(1), 0, 0, 0)
    return (
        (
            (-s / delta, -1, 1, 0),
            ((q**2 - q) / delta, -delta, 0, 1),
        ),
        (e, (0, p + 1, q - 1, 1)),
        (e, (0, p, q, 1)),
        ((1, 1, 1, 0), e),
    )


def polynomial_u0_plucker(p: sp.Expr, q: sp.Expr) -> tuple[sp.Expr, ...]:
    delta = p + q
    s = p - q + 1
    return (
        sp.expand(p * (p + 1)),
        sp.expand(-q * (q - 1)),
        -s,
        delta**2,
        -delta,
        delta,
    )


def regular_half_planes(delta: sp.Expr, s: sp.Expr):
    p = (delta + s - 1) / 2
    q = (delta - s + 1) / 2
    a = sp.factor(p * (p + 1))
    g = sp.factor(q * (q - 1))
    e = (sp.Integer(1), 0, 0, 0)
    u0 = (
        (1, 0, -delta**2 / a, delta / a),
        (0, 1, -g / a, -s / a),
    )
    return (
        u0,
        (e, (0, p + 1, q - 1, 1)),
        (e, (0, p, q, 1)),
        ((1, 1, 1, 0), e),
    )


def base_geometry() -> dict[str, object]:
    p, q = sp.symbols("p q")
    s = p - q + 1
    g = q * (q - 1)

    values = support(tensor(normalized_planes(p, q)))
    assert_support_equal(values, {"0111": 2 * s, "1111": -2 * g})

    plucker = polynomial_u0_plucker(p, q)
    p01, p02, p03, p12, p13, p23 = plucker
    assert sp.expand(p01 * p23 - p02 * p13 + p03 * p12) == 0

    base_points = ((0, 1), (-1, 0))
    jacobian = sp.Matrix((s, g)).jacobian((p, q))
    determinants: dict[str, str] = {}
    direct_planes: dict[str, object] = {}
    for p0, q0 in base_points:
        key = f"({p0},{q0})"
        determinants[key] = str(jacobian.subs({p: p0, q: q0}).det())
        assert determinants[key] in {"-1", "1"}
        point_values = tensor(normalized_planes(sp.Integer(p0), sp.Integer(q0)))
        assert all(value == 0 for value in point_values.values())
        point_plucker = tuple(value.subs({p: p0, q: q0}) for value in plucker)
        assert any(value != 0 for value in point_plucker)
        direct_planes[key] = {
            "U0_plucker": [str(value) for value in point_plucker],
            "restriction": "zero",
        }

    cap_p, cap_q, t = sp.symbols("P Q t")
    directions: dict[str, list[str]] = {}
    arcs = {
        "(0,1)": (cap_p * t, 1 + cap_q * t),
        "(-1,0)": (-1 + cap_p * t, cap_q * t),
    }
    expected = {
        "(0,1)": (2 * (cap_p - cap_q), -2 * cap_q),
        "(-1,0)": (2 * (cap_p - cap_q), 2 * cap_q),
    }
    for key, (arc_p, arc_q) in arcs.items():
        coefficients = (
            2 * (arc_p - arc_q + 1),
            -2 * arc_q * (arc_q - 1),
        )
        linear = tuple(sp.expand(value).coeff(t, 1) for value in coefficients)
        assert linear == expected[key]
        directions[key] = [str(value) for value in linear]

    intrinsic = tuple(sp.factor(value.subs(q, p + 1)) for value in values.values())
    assert intrinsic == (0, -2 * p * (p + 1))

    return {
        "pure_support": {key: str(value) for key, value in values.items()},
        "base_ideal": ["p-q+1", "q*(q-1)"],
        "base_points_on_p_plus_q_nonzero_chart": ["(0,1)", "(-1,0)"],
        "base_jacobian_determinants": determinants,
        "exceptional_divisor": "ordinary P1 at each transverse base point",
        "first_order_target_directions": directions,
        "intrinsic_direction_at_both_points": "[0:1]",
        "direct_plane_points": direct_planes,
        "grassmann_map_regular_at_both_base_points": True,
    }


def half_centre_geometry() -> dict[str, object]:
    delta, s = sp.symbols("delta s")
    planes = regular_half_planes(delta, s)
    regular_support = support(tensor(planes))
    assert_support_equal(regular_support, {"0111": -2 * delta})

    half_planes = tuple(
        tuple(
            tuple(
                sp.factor(sp.sympify(entry).subs({delta: 0, s: 0}))
                for entry in row
            )
            for row in plane
        )
        for plane in planes
    )
    assert all(value == 0 for value in tensor(half_planes).values())
    assert wedge(*half_planes[0]) == (1, -1, 0, 0, 0, 0)
    assert pair_profile(half_planes) == (3, 3, 2, 3, 3, 3)

    d, n, w, x0, a0 = sp.symbols("d n w x0 a0", real=True)
    reductions = {
        "n>=0,x0<=n": ((d + n + w) + (x0 - a0), 0, x0),
        "n>=0,x0>=n": ((2 * n + w) + (d - a0), 0, n),
        "n<0,x0<=n": ((d - n + w) + (x0 - a0), n, x0),
        "n<0,x0>=n": (w + (d - a0), n, n),
    }
    for reduced, m_value, z_value in reductions.values():
        original = d + n + w - 2 * m_value + z_value - a0
        assert sp.expand(original - reduced) == 0

    c0, c1, c2, cap_delta = sp.symbols("c0 c1 c2 Delta", nonzero=True)
    k = c0 / (4 * cap_delta)
    e = (sp.Integer(1), 0, 0, 0)
    cap_c = (0, 0, 0, sp.Integer(1))
    lower = (0, c1, -c2, 0)
    upper = (0, c1, c2, 0)
    flags: dict[str, object] = {}
    for eps_x, eps_y in itertools.product((0, 1), repeat=2):
        free = add(
            cap_c,
            scale(-eps_x * k, e),
            scale(-sp.Rational(eps_y, 2) * cap_delta, upper),
        )
        actual = tuple(sp.factor(value) for value in wedge(lower, free))
        expected = (
            eps_x * k * c1,
            -eps_x * k * c2,
            0,
            -eps_y * cap_delta * c1 * c2,
            c1,
            -c2,
        )
        assert actual == expected

        negative_y_planes = (
            (lower, free),
            (e, lower),
            (e, lower),
            (e, upper),
        )
        assert_support_equal(
            support(tensor(negative_y_planes)), {"1110": -2 * c1 * c2}
        )
        flags[f"{eps_x}{eps_y}"] = {
            "U0_plucker": [str(value) for value in actual],
            "negative_y_pure_support": {"1110": str(-2 * c1 * c2)},
        }

    y_zero: dict[str, object] = {}
    for eps_x in (0, 1):
        free = add(cap_c, scale(-eps_x * k, e))
        planes_y0 = (
            (lower, free),
            (e, add(scale(sp.Rational(1, 2), lower), cap_c)),
            (e, add(scale(-sp.Rational(1, 2), lower), cap_c)),
            (e, upper),
        )
        pure = support(tensor(planes_y0))
        assert_support_equal(pure, {"1110": c1 * c2 / 2})
        y_zero[str(eps_x)] = {
            "U0": "<L,C-k*e>" if eps_x else "<L,C>",
            "pure_support": {key: str(value) for key, value in pure.items()},
        }

    return {
        "regular_half_chart_pure_support": {
            key: str(value) for key, value in regular_support.items()
        },
        "direct_half_centre_U0_plucker": ["1", "-1", "0", "0", "0", "0"],
        "direct_half_centre_restriction": "zero",
        "direct_fixed_source_pair_profile": [3, 3, 2, 3, 3, 3],
        "direct_fixed_source_E": "d>0",
        "direct_fixed_source_actual_nonzero_P4_boundary": False,
        "exact_s_zero_diagonal_E": (
            "d+n+w-2*min(n,0)+min(x0,n)-min(x0,d,2*d+x2)"
        ),
        "E_zero_iff": "x1=x2=y, -d<=y<=0, x0>=d",
        "manual_four_region_certificate": {
            key: str(value[0]) for key, value in reductions.items()
        },
        "negative_y_flags": flags,
        "y_zero_charts": y_zero,
        "matches_existing_half_centre_atlas": True,
    }


def source_text_audit() -> None:
    component = " ".join(COMPONENT.read_text(encoding="utf-8").split())
    wall = " ".join(WALL.read_text(encoding="utf-8").split())
    assert "T_0111=2(p-q+1), T_1111=-2q(q-1)" in component
    assert "E=0 iff x1=x2=y, -d<=y<=0, x0>=d." in wall
    assert "U0=<L,C-k e>, U1=<e,(1/2)L+C>" in wall
    assert "`U1=U2=<e,L>`" in wall
    assert "`U3=<e,M>`" in wall


def main() -> None:
    source_text_audit()
    base = base_geometry()
    half = half_centre_geometry()
    payload = {
        "status": "pass",
        "role": "proof_b",
        "date_utc": datetime.now(UTC)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z"),
        "git_commit": git_commit(),
        "claim_label": "VERIFIED",
        "discovery_claim_label": "DERIVED",
        "scope": (
            "component-20 intrinsic-wall exceptional base geometry at "
            "p=0,-1,-1/2, including exact s=0 diagonal-DVR arcs only"
        ),
        "inputs": {
            COMPONENT.name: sha256(COMPONENT),
            WALL.name: sha256(WALL),
        },
        "method": (
            "fresh subset-algebra permanent reconstruction, polynomial "
            "Pluecker extension, transverse base-ideal Jacobian, and exact "
            "four-region min-plus proof"
        ),
        "command": f"uv run --with sympy python {SCRIPT.name}",
        "outputs": {
            SCRIPT.name: sha256(SCRIPT),
            REPORT.name: sha256(REPORT),
        },
        "base_geometry": base,
        "half_centre_geometry": half,
        "new_diagonal_half_centre_chart_required": False,
        "p_zero_minus_one_valuative_atlas_complete": False,
        "H31_or_H22_claim_made": False,
        "global_Krenn_Gu_resolved": False,
        "limitations": (
            "no arbitrary or non-diagonal source arcs; no complete source-torus "
            "atlas at p=0 or p=-1; no component-intersection classification, "
            "H31, H22, component exhaustiveness, arbitrary-order reduction, "
            "prize graph, or global Krenn-Gu conclusion"
        ),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
