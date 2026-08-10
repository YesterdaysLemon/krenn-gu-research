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
from fractions import Fraction
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P4_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY.md"
COMPONENT = ROOT / "claims/p4/classifications/triangle-211/common-active-binary-triangle/P4_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT.md"
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


def pluecker_relation(coordinates: tuple[sp.Expr, ...]) -> sp.Expr:
    p01, p02, p03, p12, p13, p23 = coordinates
    return sp.factor(p01 * p23 - p02 * p13 + p03 * p12)


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


def refuted_candidate_arc_audit_not_replayed() -> dict[str, object]:
    """Retained REFUTED attempt: it copied face sets and is never invoked."""

    e = sp.Matrix((1, 0, 0, 0))
    cap_a = sp.Matrix((0, 1, 0, 0))
    cap_b = sp.Matrix((0, 0, 1, 0))
    cap_c = sp.Matrix((0, 0, 0, 1))
    c1, c2, delta_lead = sp.symbols("c1 c2 Delta", nonzero=True)
    ell = c1 * cap_a - c2 * cap_b
    em = c1 * cap_a + c2 * cap_b

    eta = sp.symbols("eta", nonzero=True)
    generic_faces = {}
    for eps_x, eps_y in itertools.product((0, 1), repeat=2):
        actual = wedge(
            ell,
            cap_c + eps_x * eta * e - eps_y * delta_lead * em / 2,
        )
        expected = (
            -eps_x * eta * c1,
            eps_x * eta * c2,
            0,
            -eps_y * delta_lead * c1 * c2,
            c1,
            -c2,
        )
        assert actual == expected
        assert pluecker_relation(actual) == 0
        generic_faces[(eps_x, eps_y)] = actual

    # Independently take the rational Grassmann limit from B_full to H_k.
    u, k = sp.symbols("u k", nonzero=True)
    moving_a = -sp.Rational(1, 2) + u
    mu = -moving_a * (moving_a + 1) / (2 * moving_a + 1)
    lam = mu / k
    scaled_wedge = tuple(
        sp.factor(value / lam) for value in wedge(e + lam * ell, cap_c + mu * ell)
    )
    half_limit = tuple(sp.factor(sp.limit(value, u, 0)) for value in scaled_wedge)
    assert half_limit == (k * c1, -k * c2, 0, 0, c1, -c2)

    # Complete exceptional residue-wall signatures.  The relation checked is
    # p01*p23-p02*p13+p03*p12 after its common nonzero factor is removed.
    pi, theta = sp.symbols("pi theta", nonzero=True)
    exceptional = {
        "P<Q": (
            {(1, 0, 1, 1), (0, 0, 0, 1), (0, 0, 1, 0), (0, 0, 0, 0)},
            {delta_lead: pi},
        ),
        "Q<P": (
            {(0, 1, 1, 1), (0, 0, 0, 1), (0, 0, 1, 0), (0, 0, 0, 0)},
            {delta_lead: theta},
        ),
        "P=Q=R=d": (
            {(1, 1, 1, 1), (0, 0, 0, 1), (0, 0, 1, 0), (0, 0, 0, 0)},
            {delta_lead: pi + theta},
        ),
        "P=Q=R<d": (
            {
                (1, 1, 0, 1),
                (0, 0, 0, 1),
                (1, 1, 0, 0),
                (0, 0, 0, 0),
                (1, 1, 1, 0),
                (0, 0, 1, 0),
            },
            {theta: -pi},
        ),
    }
    exceptional_output = {}
    for label, (signatures, substitutions) in exceptional.items():
        for eps_p, eps_q, eps_c, eps_12 in signatures:
            relation = (
                eps_p * pi / delta_lead
                + eps_q * theta / delta_lead
                - eps_c * eps_12
            )
            assert sp.factor(relation.subs(substitutions)) == 0
            assert sp.factor((-relation).subs(substitutions)) == 0
        exceptional_output[label] = [list(signature) for signature in sorted(signatures)]

    assert symmetric_product(e, e) == sp.zeros(6, 1)
    assert symmetric_product(ell, em) == sp.zeros(6, 1)
    exceptional_rank = product_matrix((e, ell), (e, em)).rank()
    assert exceptional_rank == 2

    infinity_signatures = {(0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 1, 0), (1, 0, 1)}
    kappa, alpha = sp.symbols("kappa alpha", nonzero=True)
    infinity_vectors = {}
    for eps_x, eps_l, eps_u in sorted(infinity_signatures):
        vector = (
            -eps_x * kappa * c1,
            eps_x * kappa * c2,
            eps_u * alpha,
            -eps_l * delta_lead * c1 * c2,
            c1,
            -c2,
        )
        assert pluecker_relation(vector) == 0
        infinity_vectors[(eps_x, eps_l, eps_u)] = vector

    p0 = 2 * kappa / alpha
    c0_over_delta = alpha**2 / (4 * kappa)
    assert sp.factor(c0_over_delta * p0**2 - kappa) == 0
    assert sp.factor(2 * c0_over_delta * p0 - alpha) == 0
    full_direction = p0 * ell + cap_c
    assert product_matrix((e, full_direction), (e, full_direction)).rank() == 2
    return {
        "claim_label": "REFUTED",
        "finite_generic_face_count": len(generic_faces),
        "a=-1/2_B_full_closure_limit": [str(value) for value in half_limit],
        "exceptional_complete_wall_signatures": exceptional_output,
        "exceptional_lower_pair_rank": exceptional_rank,
        "exceptional_zero_products": ["e^2", "L*M"],
        "infinity_complete_face_signatures": [list(value) for value in sorted(infinity_signatures)],
        "infinity_mode_zero_vectors": {
            str(key): [str(value) for value in vector]
            for key, vector in infinity_vectors.items()
        },
        "arbitrary_nonzero_kappa_alpha_realized": True,
        "bounded_scan_used": False,
        "finite_field_computation_used": False,
    }


def raw_mode_zero_wedge(
    p: sp.Expr,
    q: sp.Expr,
    tau: tuple[sp.Expr, sp.Expr, sp.Expr, sp.Expr],
) -> tuple[sp.Expr, ...]:
    """Reconstruct (3a) without importing the primary verifier."""

    delta = p + q
    s = p - q + 1
    factored = (
        -p * (p + 1) * s,
        q * (q - 1) * s,
        s**2,
        -(delta**2) * s,
        delta * s,
        -delta * s,
    )
    return tuple(
        sp.expand(factored[index] * tau[left] * tau[right])
        for index, (left, right) in enumerate(PAIRS)
    )


def first_laurent_vector(
    expressions: tuple[sp.Expr, ...], t: sp.Symbol
) -> tuple[int, tuple[sp.Expr, ...]]:
    """Extract the first common Laurent degree and its six coefficients."""

    term_lists: list[list[tuple[int, sp.Expr]]] = []
    all_powers = []
    for expression in expressions:
        terms = []
        for term in sp.Add.make_args(sp.expand(expression)):
            if term == 0:
                continue
            power = term.as_powers_dict().get(t, sp.Integer(0))
            assert power.is_Integer, (term, power)
            integer_power = int(power)
            coefficient = sp.factor(term / t**integer_power)
            terms.append((integer_power, coefficient))
            all_powers.append(integer_power)
        term_lists.append(terms)
    common_power = min(all_powers)
    coefficients = tuple(
        sp.factor(sum(coefficient for power, coefficient in terms if power == common_power))
        for terms in term_lists
    )
    return common_power, coefficients


def critical_interval_samples(
    lower: Fraction, upper: Fraction, walls: tuple[Fraction, ...]
) -> tuple[Fraction, ...]:
    """One exact sample from every point/open cell of a one-dimensional fan."""

    points = sorted({lower, upper, *(wall for wall in walls if lower <= wall <= upper)})
    samples = set(points)
    samples.update(
        (left + right) / 2 for left, right in itertools.pairwise(points)
    )
    return tuple(sorted(samples))


def independently_enumerate_exceptional_signatures(
    cap_p: int, cap_q: int, d: int
) -> dict[tuple[int, int, int, int], tuple[int, int]]:
    cap_r = min(cap_p, cap_q)
    signatures = {}
    for y_value in critical_interval_samples(
        Fraction(-d), Fraction(0), (Fraction(-cap_r),)
    ):
        lower_x0 = max(Fraction(d - cap_r), Fraction(d) + y_value)
        for x0_value in (lower_x0, lower_x0 + 1):
            signature = (
                int(cap_p == cap_r and x0_value == d - cap_r),
                int(cap_q == cap_r and x0_value == d - cap_r),
                int(x0_value == d + y_value),
                int(y_value == -d),
            )
            assert y_value.denominator == x0_value.denominator == 1
            signatures.setdefault(signature, (int(y_value), int(x0_value)))
    return signatures


def independently_enumerate_infinity_signatures(
    d: int, r: int
) -> dict[tuple[int, int, int], tuple[int, int]]:
    signatures = {}
    for y_value in critical_interval_samples(
        Fraction(-d), Fraction(-r), ()
    ):
        lower_x0 = Fraction(d - 2 * r)
        for x0_value in (lower_x0, lower_x0 + 1):
            signature = (
                int(x0_value == d - 2 * r),
                int(y_value == -d),
                int(y_value == -r and x0_value == d - 2 * r),
            )
            assert y_value.denominator == x0_value.denominator == 1
            signatures.setdefault(signature, (int(y_value), int(x0_value)))
    return signatures


def repaired_actual_arc_realization_audit() -> dict[str, object]:
    """Extract every claimed vector from explicit raw Laurent wedges."""

    t = sp.symbols("t", positive=True)
    a = sp.symbols("a")
    c0, c1, c2 = sp.symbols("c0 c1 c2", nonzero=True)
    delta_lead, sigma = sp.symbols("Delta Sigma", nonzero=True)
    pi, theta, p0 = sp.symbols("pi theta P0", nonzero=True)
    e = sp.Matrix((1, 0, 0, 0))
    cap_a = sp.Matrix((0, 1, 0, 0))
    cap_b = sp.Matrix((0, 0, 1, 0))
    cap_c = sp.Matrix((0, 0, 0, 1))
    ell = c1 * cap_a - c2 * cap_b
    em = c1 * cap_a + c2 * cap_b

    def check(
        p: sp.Expr,
        q: sp.Expr,
        d: int,
        y: int,
        x0: int,
        expected: tuple[sp.Expr, ...],
        normalizer: sp.Expr,
        base_weight: int,
    ) -> list[str]:
        raw = raw_mode_zero_wedge(
            p,
            q,
            (c0 * t**x0, c1 * t**y, c2 * t**y, sp.Integer(1)),
        )
        actual_weight, actual = first_laurent_vector(raw, t)
        assert actual_weight == base_weight
        assert all(
            sp.factor(left - normalizer * right) == 0
            for left, right in zip(actual, expected)
        ), (p, q, d, y, x0, actual, expected)
        return [str(sp.factor(value / normalizer)) for value in actual]

    # Six finite-generic strata: two y=0 charts and four negative-y faces.
    generic_witnesses = {
        "B_full": (0, 4),
        "B_drop": (0, 5),
        "negative_interior": (-2, 5),
        "negative_x0_wall": (-2, 4),
        "negative_lower_wall": (-4, 5),
        "negative_both_walls": (-4, 4),
    }
    generic_output = {}
    d_generic = 4
    s0 = 2 * a + 1
    eta = c0 * a * (a + 1) / delta_lead
    p_generic = a
    q_generic = -a + delta_lead * t**d_generic
    for label, (y_value, x0_value) in generic_witnesses.items():
        eps_x = int(x0_value == d_generic)
        eps_c = int(x0_value == d_generic + y_value)
        eps_y = int(y_value == -d_generic)
        expected = (
            -eps_x * eta * c1,
            eps_x * eta * c2,
            eps_c * c0 * s0 / delta_lead,
            -eps_y * delta_lead * c1 * c2,
            c1,
            -c2,
        )
        generic_output[label] = check(
            p_generic,
            q_generic,
            d_generic,
            y_value,
            x0_value,
            expected,
            delta_lead * s0,
            d_generic + y_value,
        )

    # Derive exceptional signatures from fan walls, then extract every one at
    # both a=0 and a=-1 from the raw wedge.
    exceptional_parameters = {
        "P<Q": (2, 4, 2),
        "Q<P": (4, 2, 2),
        "P=Q=R=d": (2, 2, 2),
        "P=Q=R<d": (2, 2, 4),
    }
    exceptional_output = {}
    for label, (cap_p, cap_q, d_value) in exceptional_parameters.items():
        signatures = independently_enumerate_exceptional_signatures(
            cap_p, cap_q, d_value
        )
        if label == "P<Q":
            small_p = pi * t**cap_p
            small_q = theta * t**cap_q
            lead_delta = pi
            lead_theta = theta
        elif label == "Q<P":
            small_p = pi * t**cap_p
            small_q = theta * t**cap_q
            lead_delta = theta
            lead_theta = theta
        elif label == "P=Q=R=d":
            small_p = pi * t**cap_p
            small_q = theta * t**cap_q
            lead_delta = pi + theta
            lead_theta = theta
        else:
            small_p = pi * t**cap_p
            small_q = -pi * t**cap_q + delta_lead * t**d_value
            lead_delta = delta_lead
            lead_theta = -pi
        extracted = {}
        for signature, (y_value, x0_value) in signatures.items():
            eps_p, eps_q, eps_c, eps_12 = signature
            expected_a0 = (
                -eps_p * c0 * c1 * pi / lead_delta,
                -eps_q * c0 * c2 * lead_theta / lead_delta,
                eps_c * c0 / lead_delta,
                -eps_12 * lead_delta * c1 * c2,
                c1,
                -c2,
            )
            expected_a_minus1 = (
                eps_p * c0 * c1 * pi / lead_delta,
                eps_q * c0 * c2 * lead_theta / lead_delta,
                -eps_c * c0 / lead_delta,
                -eps_12 * lead_delta * c1 * c2,
                c1,
                -c2,
            )
            key = "".join(map(str, signature))
            extracted[key] = {
                "witness_y_x0": [y_value, x0_value],
                "a=0": check(
                    small_p,
                    small_q,
                    d_value,
                    y_value,
                    x0_value,
                    expected_a0,
                    lead_delta,
                    d_value + y_value,
                ),
                "a=-1": check(
                    -1 + small_p,
                    1 + small_q,
                    d_value,
                    y_value,
                    x0_value,
                    expected_a_minus1,
                    -lead_delta,
                    d_value + y_value,
                ),
            }
        exceptional_output[label] = extracted

    # Half-centre extraction, including H_k, k=0, and all negative-y walls.
    half_output = {}
    d_half, h_half = 4, 1
    p_half = (delta_lead * t**d_half + sigma * t**h_half - 1) / 2
    q_half = (delta_lead * t**d_half - sigma * t**h_half + 1) / 2
    k = c0 / (4 * delta_lead)
    for label, (y_value, x0_value) in generic_witnesses.items():
        eps_x = int(x0_value == d_half)
        eps_y = int(y_value == -d_half)
        expected = (
            eps_x * k * c1,
            -eps_x * k * c2,
            0,
            -eps_y * delta_lead * c1 * c2,
            c1,
            -c2,
        )
        half_output[label] = check(
            p_half,
            q_half,
            d_half,
            y_value,
            x0_value,
            expected,
            delta_lead * sigma,
            d_half + h_half + y_value,
        )

    # Infinity signatures are independently enumerated from its two y walls
    # and one x0 wall, then each is extracted from one Laurent arc.
    d_infinity, r_infinity = 4, -2
    infinity_signatures = independently_enumerate_infinity_signatures(
        d_infinity, r_infinity
    )
    p_infinity = p0 * t**r_infinity
    q_infinity = -p0 * t**r_infinity + delta_lead * t**d_infinity
    kappa = c0 * p0**2 / delta_lead
    alpha = 2 * c0 * p0 / delta_lead
    infinity_output = {}
    for signature, (y_value, x0_value) in infinity_signatures.items():
        eps_x, eps_l, eps_u = signature
        expected = (
            -eps_x * kappa * c1,
            eps_x * kappa * c2,
            eps_u * alpha,
            -eps_l * delta_lead * c1 * c2,
            c1,
            -c2,
        )
        infinity_output["".join(map(str, signature))] = {
            "witness_y_x0": [y_value, x0_value],
            "vector": check(
                p_infinity,
                q_infinity,
                d_infinity,
                y_value,
                x0_value,
                expected,
                2 * delta_lead * p0,
                d_infinity + r_infinity + y_value,
            ),
        }

    assert symmetric_product(e, e) == sp.zeros(6, 1)
    assert symmetric_product(ell, em) == sp.zeros(6, 1)
    assert product_matrix((e, ell), (e, em)).rank() == 2
    full_direction = p0 * ell + cap_c
    assert product_matrix((e, full_direction), (e, full_direction)).rank() == 2
    return {
        "claim_label": "VERIFIED",
        "field": "characteristic zero; 2 invertible",
        "opens": {
            "finite_generic": "a*(a+1)*(2*a+1)*c0*c1*c2*Delta != 0",
            "exceptional": "all displayed leading coefficients and Delta != 0",
            "a=-1/2": "Sigma*c0*c1*c2*Delta != 0",
            "infinity": "P0*c0*c1*c2*Delta != 0",
        },
        "method": "independent exact fan-cell enumeration plus first Laurent coefficient extraction from raw wedge",
        "finite_generic_extractions": generic_output,
        "exceptional_signature_extractions": exceptional_output,
        "half_centre_extractions": half_output,
        "infinity_signature_extractions": infinity_output,
        "exceptional_signature_sets_copied_from_primary": False,
        "infinity_signature_set_copied_from_primary": False,
        "imports_primary_verifier": False,
        "bounded_scan_used": False,
        "finite_field_computation_used": False,
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
    arcs = repaired_actual_arc_realization_audit()
    scans = bounded_scans()
    print(
        json.dumps(
            {
                "status": "pass",
                "claim_label": "VERIFIED",
                "role": "verifier",
                "date_utc": datetime.now(UTC).isoformat(),
                "git_commit": git_commit(),
                "scope": (
                    "separate exact reconstruction and bounded audit of the "
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
                "actual_arc_realization_audit": arcs,
                "fresh_independent_verifier_complete": True,
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
