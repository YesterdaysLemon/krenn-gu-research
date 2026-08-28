#!/usr/bin/env python3
"""Independent audit of the GLD91 exact two-leaf slice certificate.

This audit imports neither SymPy nor the primary verifier nor the moving
builder.  It parses the committed sparse Q(i) polynomial artifact, implements
its own Gaussian-rational sparse arithmetic, and rechecks the affine Q5
substitution and all four exact quotient remainders.  It also re-evaluates the
six linear residual fibres and pins the upstream GLD85 full-map witness.

The audit therefore checks the exact polynomial identities and metadata in the
certificate by a separate route.  It does not pretend to independently derive
the SymPy Groebner basis; completeness of the projection is the primary's
Groebner obligation, while the certificate/audit bridge is independently
replayed here.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CERTIFICATE = ROOT / "claims" / "arbitrary-order" / "four_root_torus_star_equal_leaf_survivor_rank_eight_two_leaf_slice_fitting_certificate.json"
CERTIFICATE_SHA256 = "6b3fb7fbd0b62e88b9027f8d94fcf31d86331e67a3d439dc4ef9bb0d03bbf82f"
GLD75_CERTIFICATE = ROOT / "claims" / "arbitrary-order" / "four_root_torus_star_survivor_locus_symmetry_and_local_germ_certificates.json"
GLD75_CERTIFICATE_SHA256 = "05a2540431023b7add3d3ae60189cac31ebd375609911cfdc66b8c4028346b57"
GLD85_CERTIFICATE = ROOT / "claims" / "arbitrary-order" / "four_root_torus_star_equal_leaf_survivor_rank_eight_full_intrinsic_fitting_certificate.json"
GLD85_CERTIFICATE_SHA256 = "b037dc23ceebfdbce3db3ee9a48eda1e981d627c044eef45d7d87b86414adf59"

Pair = tuple[Fraction, Fraction]
Poly = dict[tuple[int, ...], Pair]
ZERO: Pair = (Fraction(0), Fraction(0))
ONE: Pair = (Fraction(1), Fraction(0))
EXPECTED_PIVOTS = (0, 1, 2, 3, 4, 5, 7, 8, 12, 17, 19, 26, 52)
EXPECTED_SELECTED_COLUMNS = (
    252, 257, 259, 260, 261, 263, 264, 267, 272, 275,
    284, 285, 286, 288, 289, 431, 433, 434, 435, 437, 438,
    441, 446, 449, 458, 459, 460, 462, 703, 704, 705, 707,
    708, 711, 716, 719, 728, 729, 805, 806, 808, 809, 812,
    855, 2784,
)
EXPECTED_MINOR_RESIDUES = {
    "1000000007": [[9_639_769, 249_939_722]],
    "10000019": [[1_610_829, 5_232_695]],
}


def _pair(raw: list[int]) -> Pair:
    assert len(raw) == 4 and raw[1] and raw[3]
    return Fraction(raw[0], raw[1]), Fraction(raw[2], raw[3])


def _pair_raw(value: Pair) -> list[int]:
    return [value[0].numerator, value[0].denominator, value[1].numerator, value[1].denominator]


def _add(left: Pair, right: Pair) -> Pair:
    return left[0] + right[0], left[1] + right[1]


def _neg(value: Pair) -> Pair:
    return -value[0], -value[1]


def _sub(left: Pair, right: Pair) -> Pair:
    return _add(left, _neg(right))


def _mul(left: Pair, right: Pair) -> Pair:
    return left[0] * right[0] - left[1] * right[1], left[0] * right[1] + left[1] * right[0]


def _inv(value: Pair) -> Pair:
    norm = value[0] * value[0] + value[1] * value[1]
    assert norm
    return value[0] / norm, -value[1] / norm


def _div(left: Pair, right: Pair) -> Pair:
    return _mul(left, _inv(right))


def _is_zero(value: Pair) -> bool:
    return value == ZERO


def _clean(poly: Poly) -> Poly:
    return {exponents: coefficient for exponents, coefficient in poly.items() if not _is_zero(coefficient)}


def _poly_add(left: Poly, right: Poly) -> Poly:
    result = dict(left)
    for exponents, coefficient in right.items():
        result[exponents] = _add(result.get(exponents, ZERO), coefficient)
    return _clean(result)


def _poly_sub(left: Poly, right: Poly) -> Poly:
    return _poly_add(left, {exponents: _neg(coefficient) for exponents, coefficient in right.items()})


def _poly_mul(left: Poly, right: Poly) -> Poly:
    result: Poly = {}
    for left_exponents, left_coefficient in left.items():
        for right_exponents, right_coefficient in right.items():
            exponents = tuple(a + b for a, b in zip(left_exponents, right_exponents, strict=True))
            result[exponents] = _add(result.get(exponents, ZERO), _mul(left_coefficient, right_coefficient))
    return _clean(result)


def _poly_pow(poly: Poly, exponent: int) -> Poly:
    result = {(0,) * len(next(iter(poly))): ONE}
    base = poly
    while exponent:
        if exponent & 1:
            result = _poly_mul(result, base)
        base = _poly_mul(base, base)
        exponent >>= 1
    return result


def _univariate_remainder(poly: Poly, modulus: Poly) -> Poly:
    remainder = _clean(poly)
    modulus = _clean(modulus)
    assert modulus
    modulus_degree = max(exponents[0] for exponents in modulus)
    modulus_lead = modulus[(modulus_degree,)]
    while remainder:
        degree = max(exponents[0] for exponents in remainder)
        if degree < modulus_degree:
            break
        factor = _div(remainder[(degree,)], modulus_lead)
        shift = degree - modulus_degree
        multiple = {(exponent + shift,): _mul(factor, coefficient) for (exponent,), coefficient in modulus.items()}
        remainder = _poly_sub(remainder, multiple)
    return remainder


def _univariate_gcd(left: Poly, right: Poly) -> Poly:
    first = _clean(left)
    second = _clean(right)
    while second:
        first, second = second, _univariate_remainder(first, second)
    if not first:
        return {}
    degree = max(exponents[0] for exponents in first)
    lead = first[(degree,)]
    return {exponents: _div(coefficient, lead) for exponents, coefficient in first.items()}


def _derivative(poly: Poly) -> Poly:
    result: Poly = {}
    for (degree,), coefficient in poly.items():
        if degree:
            result[(degree - 1,)] = (coefficient[0] * degree, coefficient[1] * degree)
    return _clean(result)


def _compose_u(poly: Poly, u_poly: Poly) -> Poly:
    result: Poly = {}
    for (t_degree, u_degree), coefficient in poly.items():
        t_power = {(t_degree,): ONE}
        term = _poly_mul(t_power, _poly_pow(u_poly, u_degree))
        result = _poly_add(result, {exponents: _mul(coefficient, value) for exponents, value in term.items()})
    return result


def _evaluate(poly: Poly, t_value: Pair, u_value: Pair) -> Pair:
    result = ZERO
    for exponents, coefficient in poly.items():
        t_degree = exponents[0]
        u_degree = exponents[1] if len(exponents) == 2 else 0
        value = _mul(coefficient, _pair_power(t_value, t_degree))
        value = _mul(value, _pair_power(u_value, u_degree))
        result = _add(result, value)
    return result


def _pair_power(value: Pair, exponent: int) -> Pair:
    result = ONE
    base = value
    while exponent:
        if exponent & 1:
            result = _mul(result, base)
        base = _mul(base, base)
        exponent >>= 1
    return result


def _decode_poly(payload: dict[str, Any], variables: tuple[str, ...]) -> Poly:
    assert tuple(payload["variables"]) == variables
    result: Poly = {}
    for term in payload["terms"]:
        exponents = tuple(int(value) for value in term["exponents"])
        assert len(exponents) == len(variables) and all(value >= 0 for value in exponents)
        coefficient = _pair(term["coefficient"])
        result[exponents] = _add(result.get(exponents, ZERO), coefficient)
    result = _clean(result)
    total_degree = max((sum(exponents) for exponents in result), default=0)
    assert int(payload["degree"]) == total_degree
    assert int(payload["term_count"]) == len(payload["terms"])
    return result


def _constant(value: Pair) -> Poly:
    return {(0,): value}


def _linear(value: Pair) -> Poly:
    return {(1,): ONE, (0,): value}


def _canonical_file_hash(path: Path) -> tuple[str, int]:
    raw = path.read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(raw).hexdigest(), len(raw)


def _load() -> dict[str, Any]:
    raw = CERTIFICATE.read_bytes().replace(b"\r\n", b"\n")
    assert hashlib.sha256(raw).hexdigest() == CERTIFICATE_SHA256
    payload = json.loads(raw)
    assert payload["format"] == "gld91-rank-eight-two-leaf-slice-q-i-v1"
    assert payload["theorem_id"] == "GLD91"
    assert payload["field"] == "Q(i)"
    return payload


def _check_source_files(payload: dict[str, Any]) -> None:
    expected = {
        "gld75_certificate": (GLD75_CERTIFICATE, GLD75_CERTIFICATE_SHA256.upper()),
        "gld85_certificate": (GLD85_CERTIFICATE, GLD85_CERTIFICATE_SHA256.upper()),
    }
    for key, (path, digest) in expected.items():
        record = payload["source_files"][key]
        assert record["path"] == str(path.relative_to(ROOT)).replace("\\", "/")
        actual_digest, byte_count = _canonical_file_hash(path)
        assert actual_digest.upper() == digest
        assert record["sha256"] == digest
        assert record["bytes"] == byte_count


def _check_factorization(polynomials: dict[str, Poly], payload: dict[str, Any]) -> None:
    one = {(0,): ONE}
    t = {(1,): ONE}
    factors = [
        t,
        _linear((Fraction(2, 3), ZERO[1])),
        _linear((Fraction(1, 5), Fraction(3, 5))),
        _linear((Fraction(6, 13), Fraction(4, 13))),
        _linear((Fraction(1), Fraction(-1))),
        polynomials["q5"],
    ]
    product = one
    for factor in factors:
        product = _poly_mul(product, factor)
    assert product == polynomials["residual_eliminant"]
    assert _poly_mul(product, _linear((Fraction(2, 3), ZERO[1]))) == polynomials["residual_resultant"]
    assert polynomials["frame_eliminant"] == product
    q5 = polynomials["q5"]
    assert _univariate_gcd(q5, _derivative(q5)) == {(0,): ONE}
    q5_at_pole = _evaluate(q5, (Fraction(-2, 3), Fraction(0)), ZERO)
    assert _pair_raw(q5_at_pole) == payload["groebner"]["q5_at_minus_two_thirds"]


def _check_q5_reductions(polynomials: dict[str, Poly], payload: dict[str, Any]) -> None:
    q5 = polynomials["q5"]
    u_q5 = polynomials["u_q5"]
    affine = polynomials["affine_relation"]
    # The relation has a constant term as well as its t-polynomial terms.
    expected_affine = {(1, 0): ONE}
    for (degree,), coefficient in u_q5.items():
        expected_affine[(0, degree)] = _neg(coefficient)
    assert affine == _clean(expected_affine)
    for name in ("rho8", "rho9", "mu", "centre_det_numerator"):
        remainder = _univariate_remainder(_compose_u(polynomials[name], u_q5), q5)
        stored = _decode_poly(payload["q5_reductions"][name], ("t",))
        assert remainder == stored == {}


def _check_fibres(polynomials: dict[str, Poly], payload: dict[str, Any]) -> None:
    fibres = payload["fibre_classification"]
    assert len(fibres) == 6
    open_count = 0
    for item in fibres:
        t_value = _pair(item["t"])
        u_value = _pair(item["u"])
        assert _evaluate(polynomials["rho8"], t_value, u_value) == ZERO
        assert _evaluate(polynomials["rho9"], t_value, u_value) == ZERO
        mu_value = _evaluate(polynomials["mu"], t_value, u_value)
        centre_value = _evaluate(polynomials["centre_det_numerator"], t_value, u_value)
        leaf_value = _evaluate(polynomials["leaf_det"], t_value, u_value)
        assert _pair_raw(mu_value) == item["mu"]
        assert _pair_raw(centre_value) == item["centre_det_numerator"]
        assert _pair_raw(leaf_value) == item["leaf_det"]
        assert item["schur_open"] == (mu_value != ZERO)
        assert item["centre_frame_open"] == (mu_value != ZERO and centre_value != ZERO)
        assert item["leaf_frame_open"] == (leaf_value != ZERO)
        if item["schur_open"] and item["centre_frame_open"] and item["leaf_frame_open"]:
            open_count += 1
            assert item["reason"] == "pinned_full_intrinsic_rank_point"
            assert item["full_intrinsic_rank"] == 45
        elif not item["schur_open"]:
            assert item["reason"] == "schur_boundary"
        else:
            assert item["reason"] == "centre_frame_boundary"
    assert open_count == payload["open_slice"]["schur_frame_open_count"] == 1
    assert payload["q5_component"]["mu_reduction_is_zero"] is True


def _check_upstream(payload: dict[str, Any]) -> dict[str, Any]:
    raw = GLD85_CERTIFICATE.read_bytes().replace(b"\r\n", b"\n")
    assert hashlib.sha256(raw).hexdigest() == GLD85_CERTIFICATE_SHA256
    upstream = payload["upstream_gld85"]
    assert tuple(upstream["selected_columns"]) == EXPECTED_SELECTED_COLUMNS
    assert upstream["full_intrinsic_rank"] == 45
    assert upstream["denominator_slots_checked"] == {
        "1000000007": 6240,
        "10000019": 6240,
    }
    assert upstream["minor_residues"] == {
        "1000000007": [9_639_769, 249_939_722],
        "10000019": [1_610_829, 5_232_695],
    }
    certificate = json.loads(raw)
    assert certificate["selected_columns"] == list(EXPECTED_SELECTED_COLUMNS)
    for record in certificate["primes"]:
        prime = str(record["prime"])
        assert record["pivot_rows"] == list(EXPECTED_PIVOTS)
        assert record["denominator_count"] == 6240
        assert record["denominator_nonzero_count"] == 6240
        assert record["selected_minor_residue"] == upstream["minor_residues"][prime]
    return {
        "certificate_sha256": GLD85_CERTIFICATE_SHA256.upper(),
        "full_intrinsic_rank": 45,
        "selected_columns": list(EXPECTED_SELECTED_COLUMNS),
        "minor_residues": upstream["minor_residues"],
    }


def check() -> dict[str, Any]:
    payload = _load()
    _check_source_files(payload)
    polynomials = {
        "rho8": _decode_poly(payload["polynomials"]["rho8"], ("t", "u")),
        "rho9": _decode_poly(payload["polynomials"]["rho9"], ("t", "u")),
        "mu": _decode_poly(payload["polynomials"]["mu"], ("t", "u")),
        "centre_det_numerator": _decode_poly(payload["polynomials"]["centre_det_numerator"], ("t", "u")),
        "leaf_det": _decode_poly(payload["polynomials"]["leaf_det"], ("t", "u")),
        "residual_eliminant": _decode_poly(payload["polynomials"]["residual_eliminant"], ("t",)),
        "residual_resultant": _decode_poly(payload["polynomials"]["residual_resultant"], ("t",)),
        "frame_eliminant": _decode_poly(payload["polynomials"]["frame_eliminant"], ("t",)),
        "q5": _decode_poly(payload["polynomials"]["q5"], ("t",)),
        "affine_relation": _decode_poly(payload["polynomials"]["affine_relation"], ("u", "t")),
        "u_q5": _decode_poly(payload["polynomials"]["u_q5"], ("t",)),
    }
    assert len(polynomials["rho8"]) == 9
    assert len(polynomials["rho9"]) == 13
    assert len(polynomials["mu"]) == 9
    assert len(polynomials["centre_det_numerator"]) == 54
    assert len(polynomials["q5"]) == 6
    _check_factorization(polynomials, payload)
    _check_q5_reductions(polynomials, payload)
    _check_fibres(polynomials, payload)
    upstream = _check_upstream(payload)
    scope = payload["scope"]
    assert scope["slice_residual_fitting_zero_locus_empty_on_schur_frame_open"] is True
    assert scope["full_chart_unit_ideal_proved"] is False
    assert scope["full_chart_residual_proved_empty"] is False
    assert scope["omitted_offset_bug_corrected"] is True
    assert scope["global_conjecture_resolved"] is False
    return {
        "status": "independent_no_import_gld91_sparse_qi_slice_audit_pass",
        "theorem_id": "GLD91",
        "field": "Q(i)",
        "polynomial_terms": {name: len(value) for name, value in polynomials.items()},
        "q5_remainders_checked": ["rho8", "rho9", "mu", "centre_det_numerator"],
        "linear_fibres_checked": len(payload["fibre_classification"]),
        "schur_frame_open_fibres": payload["open_slice"]["schur_frame_open_count"],
        "upstream_gld85": upstream,
        "full_chart_unit_ideal_proved": False,
        "global_conjecture": "UNRESOLVED",
    }


def main() -> None:
    print("four-root rank-eight two-leaf slice GLD91 independent audit: PASS")
    print(json.dumps(check(), indent=2))


if __name__ == "__main__":
    main()
