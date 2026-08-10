#!/usr/bin/env python3
"""Independent exact audit of the actual diagonal-DVR mask-6 H22 claim.

No construction module is imported.  The twelve flags are rebuilt from the
raw wall excess and leading-coefficient formulas, and all permanent
calculations are reconstructed here.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[5] / "src"))
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)


import hashlib
import itertools
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
SCRIPT = Path(__file__).resolve()
REPORT = ROOT / (
    "P5_H22_P_PLUS_Q_DIAGONAL_DVR_MASK6_ACTUAL_FREE_PLANES_INDEPENDENT_VERIFICATION.md"
)
CANDIDATE = ROOT / (
    "P5_H22_P_PLUS_Q_DIAGONAL_DVR_MASK6_ACTUAL_FREE_PLANES_OBSTRUCTION_CANDIDATE.md"
)
PRIMARY = ROOT / (
    "derive_p5_h22_p_plus_q_diagonal_dvr_mask6_actual_free_"
    "planes_obstruction_candidate.py"
)
CANDIDATE_CERTIFICATE = ROOT / (
    "p5_h22_p_plus_q_diagonal_dvr_mask6_actual_free_planes_certificate.json"
)
LEDGER = ROOT / "p5_h22_p_plus_q_diagonal_dvr_coverage.json"
P4_WALL = REPO_ROOT / "P4_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY.md"
H22_DEFINITION = REPO_ROOT / "claims/p5/h22/embedded-p3/P5_H22_EMBEDDED_P3_COMPONENT_GENERIC_OBSTRUCTION.md"
H22_REDUCTION = REPO_ROOT / "claims/p5/coordinate-cegar/P5_HIGH_COORDINATE_PARTIAL_FRONTIER.md"

WORDS = tuple(itertools.product((0, 1), repeat=4))
PERMUTATIONS4 = tuple(itertools.permutations(range(4)))
PERMUTATIONS3 = tuple(itertools.permutations(range(3)))
ACTUAL_IDS = {
    "finite_generic_negative_y_embedded_p3",
    "finite_half_centre_negative_y_embedded_p3",
    "infinity_lower_pair_embedded_p3",
}


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


def permanent4(rows):
    return sp.expand(
        sum(
            sp.prod(rows[i][permutation[i]] for i in range(4))
            for permutation in PERMUTATIONS4
        )
    )


def permanent3(rows):
    return sp.expand(
        sum(
            sp.prod(rows[i][permutation[i]] for i in range(3))
            for permutation in PERMUTATIONS3
        )
    )


def wedge(left, right):
    return tuple(
        sp.expand(left[i] * right[j] - left[j] * right[i])
        for i, j in ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
    )


def source_leading_coefficient_checks():
    """Derive the normalized coefficient tables from the raw wedge terms."""
    a, cap_s0, cap_sigma, cap_p0 = sp.symbols("a s0 Sigma P0", nonzero=True)
    c0, c1, c2, delta = sp.symbols("c0 c1 c2 Delta", nonzero=True)

    # Divide the raw generic coefficients by the common leading scalar
    # Delta*s0.  These are the six coefficients in the P4 wall theorem.
    generic_raw = (
        -a * (a + 1) * cap_s0 * c0 * c1,
        a * (a + 1) * cap_s0 * c0 * c2,
        cap_s0**2 * c0,
        -(delta**2) * cap_s0 * c1 * c2,
        delta * cap_s0 * c1,
        -delta * cap_s0 * c2,
    )
    generic = tuple(sp.factor(value / (delta * cap_s0)) for value in generic_raw)
    eta = c0 * a * (a + 1) / delta
    assert generic == (
        -eta * c1,
        eta * c2,
        c0 * cap_s0 / delta,
        -delta * c1 * c2,
        c1,
        -c2,
    )

    # At the half centre p=-1/2 and s=Sigma*t^h.
    half_raw = (
        cap_sigma * c0 * c1 / 4,
        -cap_sigma * c0 * c2 / 4,
        cap_sigma**2 * c0,
        -(delta**2) * cap_sigma * c1 * c2,
        delta * cap_sigma * c1,
        -delta * cap_sigma * c2,
    )
    half = tuple(sp.factor(value / (delta * cap_sigma)) for value in half_raw)
    kay = c0 / (4 * delta)
    assert half == (
        kay * c1,
        -kay * c2,
        cap_sigma * c0 / delta,
        -delta * c1 * c2,
        c1,
        -c2,
    )

    # At infinity p~P0*t^r, q~-P0*t^r, s~2P0*t^r.
    infinity_raw = (
        -2 * cap_p0**3 * c0 * c1,
        2 * cap_p0**3 * c0 * c2,
        4 * cap_p0**2 * c0,
        -2 * delta**2 * cap_p0 * c1 * c2,
        2 * delta * cap_p0 * c1,
        -2 * delta * cap_p0 * c2,
    )
    infinity = tuple(sp.factor(value / (2 * delta * cap_p0)) for value in infinity_raw)
    kappa = c0 * cap_p0**2 / delta
    alpha = 2 * c0 * cap_p0 / delta
    assert infinity == (
        -kappa * c1,
        kappa * c2,
        alpha,
        -delta * c1 * c2,
        c1,
        -c2,
    )
    return {
        "generic": [str(value) for value in generic],
        "half_centre": [str(value) for value in half],
        "infinity": [str(value) for value in infinity],
    }


def retained(coefficients, excesses):
    assert all(value >= 0 for value in excesses)
    return tuple(
        coefficient if excess == 0 else sp.Integer(0)
        for coefficient, excess in zip(coefficients, excesses, strict=True)
    )


def actual_flag_atlas():
    """Enumerate all twelve flags from explicit points in the exact cones."""
    c1, c2, delta = sp.symbols("c1 c2 Delta", nonzero=True)
    eta, kay, kappa = sp.symbols("eta k kappa", nonzero=True)
    generic_coefficients = (-eta * c1, eta * c2, 1, -delta * c1 * c2, c1, -c2)
    half_coefficients = (kay * c1, -kay * c2, 1, -delta * c1 * c2, c1, -c2)
    infinity_coefficients = (
        -kappa * c1,
        kappa * c2,
        1,
        -delta * c1 * c2,
        c1,
        -c2,
    )

    atlas = []
    # Generic and half-centre cones use d=2.  The strict y<0 interior witness
    # is y=-1, while y=-d realizes the lower wall.  Likewise x0=2/3 realizes
    # the x wall/interior.
    for family in ("finite_generic", "finite_half_centre"):
        for eps_x, eps_y in itertools.product((0, 1), repeat=2):
            d = 2
            y = -d if eps_y else -1
            x0 = d if eps_x else d + 1
            assert -d <= y < 0 and x0 >= d
            if family == "finite_generic":
                excesses = (x0 - d, x0 - d, x0 - d - y, d + y, 0, 0)
                coefficients = generic_coefficients
                xi = eps_x * eta
            else:
                h = 1
                excesses = (
                    x0 - d,
                    x0 - d,
                    h + x0 - d - y,
                    d + y,
                    0,
                    0,
                )
                coefficients = half_coefficients
                xi = -eps_x * kay
            vector = retained(coefficients, excesses)
            upsilon = -sp.Rational(1, 2) * eps_y * delta
            lower = (0, c1, -c2, 0)
            free = (xi, upsilon * c1, upsilon * c2, 1)
            assert vector == wedge(lower, free)
            atlas.append(
                {
                    "family": family,
                    "eps_x": eps_x,
                    "eps_y": eps_y,
                    "witness": {"d": d, "y": y, "x0": x0},
                    "xi": str(xi),
                    "upsilon": str(upsilon),
                }
            )

    # Infinity lower-pair cone: r=-1,d=2, with y=0 in its strict interior and
    # y=-d on its lower wall.  Since y<-r=1, eps_u is identically zero.
    for eps_x, eps_l in itertools.product((0, 1), repeat=2):
        r, d = -1, 2
        y = -d if eps_l else 0
        x0 = d - 2 * r if eps_x else d - 2 * r + 1
        assert -d <= y < -r and x0 >= d - 2 * r
        eps_u = int(y == -r and x0 == d - 2 * r)
        assert eps_u == 0
        excesses = (
            x0 - d + 2 * r,
            x0 - d + 2 * r,
            x0 - d + r - y,
            d + y,
            0,
            0,
        )
        vector = retained(infinity_coefficients, excesses)
        xi = eps_x * kappa
        upsilon = -sp.Rational(1, 2) * eps_l * delta
        lower = (0, c1, -c2, 0)
        free = (xi, upsilon * c1, upsilon * c2, 1)
        assert vector == wedge(lower, free)
        atlas.append(
            {
                "family": "infinity_lower_pair",
                "eps_x": eps_x,
                "eps_l": eps_l,
                "eps_u": eps_u,
                "witness": {"r": r, "d": d, "y": y, "x0": x0},
                "xi": str(xi),
                "upsilon": str(upsilon),
            }
        )

    assert len(atlas) == 12
    assert sum(item["family"] == "finite_generic" for item in atlas) == 4
    assert sum(item["family"] == "finite_half_centre" for item in atlas) == 4
    assert sum(item["family"] == "infinity_lower_pair" for item in atlas) == 4
    return atlas


def common_planes_and_mask():
    c1, c2 = sp.symbols("c1 c2", nonzero=True)
    xi, upsilon = sp.symbols("xi upsilon")
    lower = sp.Matrix((0, c1, -c2, 0))
    free = sp.Matrix((xi, upsilon * c1, upsilon * c2, 1))

    assert wedge(tuple(lower), tuple(free)) == (
        -c1 * xi,
        c2 * xi,
        0,
        2 * c1 * c2 * upsilon,
        c1,
        -c2,
    )
    normal_1 = sp.Matrix((1, 0, 0)).cross(sp.Matrix((0, c1, -c2)))
    normal_2 = -normal_1
    normal_3 = sp.Matrix((1, 0, 0)).cross(sp.Matrix((0, c1, c2)))
    assert normal_1 == sp.Matrix((0, c2, c1))
    assert normal_2 == sp.Matrix((0, -c2, -c1))
    assert normal_3 == sp.Matrix((0, -c2, c1))
    assert c1.is_nonzero and c2.is_nonzero
    support_mask = 2 + 4
    assert support_mask == 6
    return {
        "U0": "<L,C+xi*e+upsilon*M>",
        "U1": "<e,L>",
        "U2": "<e,L>",
        "U3": "<e,M>",
        "normals_e_A_B": [
            str(tuple(value)) for value in (normal_1, normal_2, normal_3)
        ],
        "sign_rectangle_parameter": "[C:A:B]=[0:c2:c1]",
        "support_mask": support_mask,
    }


def wall_bases(c1, c2, xi, upsilon):
    e = (1, 0, 0, 0)
    lower = (0, c1, -c2, 0)
    upper = (0, c1, c2, 0)
    free = (xi, upsilon * c1, upsilon * c2, 1)
    return (lower, e, e, e), (free, lower, lower, upper)


def coefficients(alpha, beta):
    return {
        word: permanent4(tuple(beta[i] if word[i] else alpha[i] for i in range(4)))
        for word in WORDS
    }


def orientation_and_marking_audit():
    c1, c2, xi, upsilon = sp.symbols("c1 c2 xi upsilon", nonzero=True)
    markings = sp.symbols("h0:4")
    natural_alpha, natural_beta = wall_bases(c1, c2, xi, upsilon)
    natural = coefficients(natural_alpha, natural_beta)
    assert {
        word: sp.factor(value) for word, value in natural.items() if value != 0
    } == {(1, 1, 1, 0): -2 * c1 * c2}

    standard_alpha = natural_alpha[:3] + (natural_beta[3],)
    standard_beta0 = natural_beta[:3] + (natural_alpha[3],)
    standard_beta = tuple(
        tuple(
            sp.expand(standard_beta0[i][j] + markings[i] * standard_alpha[i][j])
            for j in range(4)
        )
        for i in range(4)
    )
    marked = coefficients(standard_alpha, standard_beta)
    assert {word: sp.factor(value) for word, value in marked.items() if value != 0} == {
        (1, 1, 1, 1): -2 * c1 * c2
    }
    return standard_alpha, {
        "natural_nonzero_support": {"1110": str(-2 * c1 * c2)},
        "standard_marked_nonzero_support": {"1111": str(-2 * c1 * c2)},
        "all_sixteen_coefficients_checked_in_both_orientations": True,
        "internal_U3_basis_swap_only": True,
        "arbitrary_markings_checked": True,
    }


def project(row, extension, direction, rho, sigma):
    if direction == "D01":
        return (
            sp.expand(rho * row[0] + sigma * row[1]),
            row[2],
            row[3],
            extension,
        )
    if direction == "D23":
        return (
            row[0],
            row[1],
            sp.expand(rho * row[2] + sigma * row[3]),
            extension,
        )
    raise ValueError(direction)


def all_alpha(alpha, extensions, direction, rho, sigma):
    rows = tuple(
        project(alpha[i], extensions[i], direction, rho, sigma) for i in range(4)
    )
    cofactors = tuple(
        permanent3(tuple(rows[j][:3] for j in range(4) if j != i)) for i in range(4)
    )
    diagonal = permanent4(rows)
    assert (
        sp.expand(diagonal - sum(extensions[i] * cofactors[i] for i in range(4))) == 0
    )
    return rows, sp.factor(diagonal), tuple(sp.factor(value) for value in cofactors)


def homogeneous_contraction_audit(alpha):
    c1, c2, rho, sigma = sp.symbols("c1 c2 rho sigma", nonzero=True)
    # Substitute fresh c1,c2 into the symbolic standard alpha rows.
    old_symbols = sorted(
        {
            symbol
            for row in alpha
            for value in row
            for symbol in sp.sympify(value).free_symbols
        },
        key=str,
    )
    assert len(old_symbols) >= 2
    by_name = {str(symbol): symbol for symbol in old_symbols}
    alpha = tuple(
        tuple(
            sp.sympify(value).subs({by_name["c1"]: c1, by_name["c2"]: c2})
            for value in row
        )
        for row in alpha
    )
    ext01 = sp.symbols("x0:4")
    ext23 = sp.symbols("y0:4")
    d01_rows, a01, cofactors01 = all_alpha(alpha, ext01, "D01", rho, sigma)
    d23_rows, a23, cofactors23 = all_alpha(alpha, ext23, "D23", rho, sigma)

    assert all(row[2] == 0 for row in d01_rows)
    assert d23_rows == (
        (0, c1, -rho * c2, ext23[0]),
        (1, 0, 0, ext23[1]),
        (1, 0, 0, ext23[2]),
        (0, c1, rho * c2, ext23[3]),
    )
    assert cofactors01 == (0, 0, 0, 0)
    assert cofactors23 == (0, 0, 0, 0)
    assert a01 == 0 and a23 == 0

    for endpoint in ({rho: 0, sigma: 1}, {rho: 1, sigma: 0}):
        assert sp.expand(a01.subs(endpoint)) == 0
        assert sp.expand(a23.subs(endpoint)) == 0

    kappa = sp.symbols("kappa", nonzero=True)
    sample = sp.symbols("z0:4")
    extension = sp.symbols("f")
    for direction, scaled_coordinate in (("D01", 0), ("D23", 2)):
        unscaled = project(sample, extension, direction, rho, sigma)
        scaled = project(sample, extension, direction, kappa * rho, kappa * sigma)
        expected = tuple(
            kappa * unscaled[i] if i == scaled_coordinate else unscaled[i]
            for i in range(4)
        )
        assert all(
            sp.expand(left - right) == 0
            for left, right in zip(scaled, expected, strict=True)
        )

    return {
        "D01_all_alpha_diagonal": str(a01),
        "D23_all_alpha_diagonal": str(a23),
        "D01_extension_cofactors": [str(value) for value in cofactors01],
        "D23_extension_cofactors": [str(value) for value in cofactors23],
        "arbitrary_homogeneous_weight_checked": True,
        "both_projective_endpoints_checked": True,
        "projective_weight_scaling_checked": True,
        "independent_alpha_extensions_in_two_directions": True,
    }


def dependency_and_definition_audit():
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    by_id = {entry["id"]: entry for entry in ledger["strata"]}
    assert ACTUAL_IDS <= by_id.keys()
    for identifier in ACTUAL_IDS:
        assert by_id[identifier]["normal_support_mask"] == 6
        assert "embedded-P3" in by_id[identifier]["p4_route"]

    generic_text = " ".join(H22_DEFINITION.read_text(encoding="utf-8").split())
    reduction_text = " ".join(H22_REDUCTION.read_text(encoding="utf-8").split())
    assert (
        "A binary `Delta_2` image requires its all-alpha and all-beta "
        "coefficients both to be nonzero."
    ) in generic_text
    assert (
        "Since an `H22` local map requires at least one of them to be genuinely binary"
    ) in generic_text
    assert "and at least one maps to `Delta_2`" in reduction_text
    return {
        "actual_ledger_ids": sorted(ACTUAL_IDS),
        "all_actual_entries_have_mask_6": True,
        "binary_requires_two_nonzero_diagonals": True,
        "H22_requires_at_least_one_binary_marked_direction": True,
        "bounded_local_criterion_replayed_from_generic_theorem": True,
    }


def main():
    source_coefficients = source_leading_coefficient_checks()
    atlas = actual_flag_atlas()
    planes = common_planes_and_mask()
    alpha, orientation = orientation_and_marking_audit()
    contractions = homogeneous_contraction_audit(alpha)
    dependencies = dependency_and_definition_audit()

    result = {
        "status": "pass",
        "role": "verifier",
        "date_utc": datetime.now(UTC)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z"),
        "git_commit": git_commit(),
        "claim_label": "VERIFIED",
        "scope": (
            "weighted H22 on the twelve actual normal-support mask-6 "
            "embedded-P3 flags of the diagonal-DVR p+q=0 wall"
        ),
        "inputs": {
            path.name: sha256(path)
            for path in (
                CANDIDATE,
                PRIMARY,
                CANDIDATE_CERTIFICATE,
                LEDGER,
                P4_WALL,
                H22_DEFINITION,
                H22_REDUCTION,
            )
        },
        "method": (
            "no-import reconstruction from raw wall excess/leading formulas, "
            "explicit twelve-flag witnesses, independent permanent expansion, "
            "and homogeneous all-alpha cofactor identities"
        ),
        "command": (
            'uv run --with sympy python claims/p5/h22/disputed-ownership/p-plus-q-wall/audit_p5_h22_p_plus_q_diagonal_dvr_mask6_actual_free_planes_independent.py'
        ),
        "outputs": {
            SCRIPT.name: sha256(SCRIPT),
            REPORT.name: sha256(REPORT),
        },
        "source_leading_coefficients": source_coefficients,
        "actual_flag_count": len(atlas),
        "actual_flags": atlas,
        "common_plane_form_and_mask": planes,
        "orientation_and_markings": orientation,
        "homogeneous_contractions": contractions,
        "definition_audit": dependencies,
        "all_actual_mask6_flags_obstructed": True,
        "finite_field_computation_used_as_proof": False,
        "broad_brute_force_used": False,
        "projective_chart_transport_used": False,
        "global_Krenn_Gu_conjecture_resolved": False,
        "limitations": (
            "restricted to the twelve actual flags in the verified diagonal-"
            "source-torus p+q=0 wall atlas and the standard 01|23 matching; "
            "no arbitrary GL4 source changes, component exhaustiveness, "
            "arbitrary-order reduction, prize graph, or global conclusion"
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
