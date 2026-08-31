#!/usr/bin/env python3
"""Replay the scoped GLD101 a=0 six-selector norm cover.

This is a proof-obligation verifier, not a resolution of Krenn--Gu.  It
reconstructs the authoritative GLD71 syndrome rows and the GLD88 H4 chart,
forms the named actual seven-by-seven minors as sparse polynomials in the
offset variables B,C, and computes the six-selector determinant in
QQ(p)[q]/(Q6).  Its exact norm and resultant are checked against pinned
factor signatures.  Ignored Singular replays are inspected only in an
explicit opt-in provenance mode; the exact GLD101 result is invariant under
their presence or absence and remains runnable from a clean clone.

The rank-to-selector implication is intentionally one-way: rank at most six
and a nonzero offset imply the selected minors and then the selectors vanish.
The norm/factor computation therefore does not, by itself, prove the global
conjecture.  Every scope and gate is reported explicitly.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
import time
from pathlib import Path

import sympy as sp
from sympy import QQ


ROOT = Path(__file__).resolve().parents[2]
GLD71 = ROOT / "claims" / "arbitrary-order" / (
    "verify_four_root_torus_star_punctured_syndrome_and_eisenstein_norm_gate.py"
)
GLD88 = ROOT / "claims" / "arbitrary-order" / (
    "verify_four_root_torus_star_equal_leaf_h4_generic_rank_six_common_row_kernel_exclusion.py"
)
GLD99 = ROOT / "claims" / "arbitrary-order" / (
    "verify_four_root_torus_star_equal_leaf_h4_q6_h2_degree_drop_six_minor_offset_exclusion.py"
)
CERTIFICATE_PAYLOAD = ROOT / "claims" / "arbitrary-order" / "certificates" / (
    "GLD101_A0_NORM_COVER_CERTIFICATE.json"
)

p, q, B, C = sp.symbols("p q B C")
K = QQ.frac_field(p)

SUPPORT_ROWS = (0, 1, 2, 3, 17, 25, 28, 31, 32, 33)
RSTAR = (0, 1, 17, 28, 31, 32, 33)
NAMED = {
    "T0": ((0, 1, 2, 17, 25, 31, 28), (0, 1, 3, 4, 6, 7, 8)),
    "T1": ((0, 1, 2, 17, 25, 31, 32), (0, 1, 3, 4, 6, 7, 2)),
    "T2": ((0, 1, 2, 17, 25, 31, 32), (0, 1, 3, 4, 6, 7, 5)),
    "T3": ((0, 1, 2, 17, 25, 31, 33), (0, 1, 3, 4, 6, 7, 8)),
    "D0": ((1, 17, 28, 0, 25, 31, 32), (0, 1, 2, 3, 4, 5, 6)),
    "D2": ((1, 17, 28, 0, 31, 32, 3), (0, 1, 2, 3, 4, 5, 6)),
}
EXTRA = {
    "Y0": (0, 1, 2, 3, 4, 5, 6),
    "Y1": (0, 1, 3, 4, 5, 6, 7),
    "X3": (0, 1, 2, 3, 4, 6, 7),
}
SIX_NAMES = ("T0", "T1", "T2", "T3", "Y1", "X3")
SIX_COLUMNS = ((0, 1), (1, 0), (1, 1), (2, 0), (2, 1), (3, 0))
# The pinned eight-selector payload is the nonzero alternate block; D2 is
# identically zero on this a=0 branch and is intentionally not inserted into
# the determinant.
EIGHT_NAMES = ("T0", "T1", "T2", "T3", "D0", "Y0", "Y1", "X3")
EIGHT_COLUMNS = (
    (0, 1),
    (1, 0),
    (0, 2),
    (1, 1),
    (2, 0),
    (1, 2),
    (2, 1),
    (3, 0),
)

# The source files are pinned by both repository bytes and a line-ending
# normalized digest.  A checkout may use CRLF or LF, but any other content
# fails closed before it is imported.
EXPECTED_SOURCE_PINS = {
    "GLD71": {
        "path": GLD71,
        "sha256": "3342809b22cc1e5ffe960e14068f81303a3bc0b597e21e2d29c05c10c605dc7d",
        "lf_sha256": "e0204ec4495bb3f86252c18d77e3493dd6d1b0e3011e33866a2a0b2462922d5e",
    },
    "GLD88": {
        "path": GLD88,
        "sha256": "70c46728c397d7a18fd999c27ca3d10232f9e3169ad508be7071c109be322752",
        "lf_sha256": "4ba10801ea64fbb170d7949a7030d64da6c1fd707bb894d8c1372947668d8199",
    },
    "GLD99": {
        "path": GLD99,
        "sha256": None,
        "lf_sha256": "8626e875bc162e79a6abe5ddfffa2a3dcf7f09b21e4de8df25fe146d9f5a2347",
    },
}

EXPECTED_SUPPORT_DIGEST = (
    "c53d2c7912d87b5f46c39ec6fc64d1aaa6ab7839ad69f3bbfb6f39375b6ed1b0"
)
EXPECTED_Q6_SREPR_SHA256 = (
    "2ed58764e7c50c8e1510a93b32d2515a9297c03dfe297fed8d9abe5f8e9d71a7"
)

# Hashes are sha256(str(expand(factor)).encode()).  Keeping the degree-110
# expression out of this file avoids a second, unpinned polynomial copy while
# still checking its exact factor signature.
EXPECTED_SIX_NORM = {
    "expression_sha256": (
        "c8b675268458576454cf3eeab5fe38c4ef468a2113c94febfd471c0cfc6d6431"
    ),
    "norm_numerator_degree_p": 548,
    "norm_numerator_terms_p": 451,
    "norm_numerator_sha256": (
        "582f782b1fb1a1824e5d22d8374f52cb25075aab1372f7d06b9607269add79e3"
    ),
    "primitive_content": "1",
    "factors": (
        (1, 36, "fba95ee7da505d8883744a06a8933df8d8d7c4ac2cca316e4990626e92a17fed"),
        (1, 98, "148de9c5a7a44d19e56cd9ae1a554bf67847afb0c58f6e12fa29ac7ddfca9940"),
        (2, 2, "fae3e839d66db547d5697d6fa1a88aa81dfecd3e360d46204801b3b420f3d40b"),
        (2, 43, "ace5cff9ef6fef5a8a62e0a4bd98c3482a066949f3970663a5e446dae97247ca"),
        (2, 99, "eeba65c990e66c56329c3f9ddd1b7623f5b84b11683828352e0cd96b0a928bf9"),
        (4, 2, "59d876136007e0f768ece9df63d326ef21471d26d69a676013fb0eedab51c9eb"),
        (8, 1, "19e8048b6aa1a654dd24c889b7c6aea895c31bb5bba60e3a038dbcbc961ad06d"),
        (110, 1, "1ae5a3e502f686d484b757db27d6f70b3ff535792edb65ceb40c2bd455410016"),
    ),
}
EXPECTED_EIGHT_NORM = {
    "expression_sha256": (
        "2d2671c061b5d11195c9286a6bc09fabec5f0fa7426446da84ce29053c447a46"
    ),
    "norm_numerator_degree_p": 698,
    "norm_numerator_terms_p": 575,
    "norm_numerator_sha256": (
        "855d130705161221baa7b29f83489f1bbb8c17bdeba9b923f705e4b5e66eeec0"
    ),
    "factors": (
        (1, 52, "fba95ee7da505d8883744a06a8933df8d8d7c4ac2cca316e4990626e92a17fed"),
        (1, 124, "148de9c5a7a44d19e56cd9ae1a554bf67847afb0c58f6e12fa29ac7ddfca9940"),
        (2, 4, "fae3e839d66db547d5697d6fa1a88aa81dfecd3e360d46204801b3b420f3d40b"),
        (2, 57, "ace5cff9ef6fef5a8a62e0a4bd98c3482a066949f3970663a5e446dae97247ca"),
        (2, 120, "eeba65c990e66c56329c3f9ddd1b7623f5b84b11683828352e0cd96b0a928bf9"),
        (4, 2, "59d876136007e0f768ece9df63d326ef21471d26d69a676013fb0eedab51c9eb"),
        (8, 1, "3abacc55b8f1b00b38341edf1e84ed6f5e49496eae91da7f5cb19259657c6053"),
        (8, 1, "19e8048b6aa1a654dd24c889b7c6aea895c31bb5bba60e3a038dbcbc961ad06d"),
        (12, 1, "f658669b3cc193bdbf898c1db814d664b5648be155df8f33a8881b84f7f1da2b"),
        (14, 1, "c8d548e594172eca1f24ba7231c50e97db2c2596dc56c3f1cfd35140a914e8bd"),
        (110, 1, "1ae5a3e502f686d484b757db27d6f70b3ff535792edb65ceb40c2bd455410016"),
    ),
}

EXPECTED_DELTA_RESULTANT = (
    "27648*p**6*(p - 1)**6*(p**2 - p + 1)**19*(2*p**2 - 2*p + 1)"
)
EXPECTED_DELTA_RESULTANT_SREPR_SHA256 = (
    "73f9ddbc2342851b2bfd79edc880a0c089172ae7b7d6e97a37076eba94420459"
)
EXPECTED_CERTIFICATE_PAYLOAD_SHA256 = "9213a50f96bf6bffa7a8f8fefbd8cca99317f00a1b1863b19e83d1330f79518e"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def lf_sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes().replace(b"\r\n", b"\n"))


def pinned_source_manifest() -> dict[str, dict[str, object]]:
    """Validate canonical source bytes before importing either module."""
    result = {}
    for name, expected in EXPECTED_SOURCE_PINS.items():
        path = expected["path"]
        if not path.exists():
            raise AssertionError(f"missing pinned source: {path}")
        raw = sha256_bytes(path.read_bytes())
        normalized = lf_sha256(path)
        if raw != expected["sha256"] and normalized != expected["lf_sha256"]:
            raise AssertionError(
                f"{name} source pin mismatch: raw={raw}, lf={normalized}"
            )
        if normalized != expected["lf_sha256"]:
            raise AssertionError(f"{name} LF-normalized source pin mismatch")
        result[name] = {
            "path": str(path),
            "sha256": raw,
            "lf_sha256": normalized,
        }
    return result


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def load_certificate_payload() -> dict[str, object]:
    """Load the tracked norm-cover manifest and validate its pinned fields."""
    if not CERTIFICATE_PAYLOAD.exists():
        raise AssertionError(f"missing tracked certificate payload: {CERTIFICATE_PAYLOAD}")
    digest = lf_sha256(CERTIFICATE_PAYLOAD)
    if digest != EXPECTED_CERTIFICATE_PAYLOAD_SHA256:
        raise AssertionError(f"certificate payload pin mismatch: {digest}")
    payload = json.loads(CERTIFICATE_PAYLOAD.read_text(encoding="utf-8"))
    if payload.get("schema_version") != 1:
        raise AssertionError("unsupported certificate payload schema")
    if payload.get("certificate_id") != "GLD101-A0-six-selector-norm-cover":
        raise AssertionError("certificate payload id mismatch")
    if payload.get("status") != "scoped_norm_cover_evidence_manifest":
        raise AssertionError("certificate payload status mismatch")
    if payload.get("global_conjecture") != "UNRESOLVED":
        raise AssertionError("certificate payload global status mismatch")
    selector = payload.get("six_selector", {})
    if selector.get("names") != list(SIX_NAMES):
        raise AssertionError("certificate payload selector names mismatch")
    if selector.get("columns") != [list(exp) for exp in SIX_COLUMNS]:
        raise AssertionError("certificate payload selector columns mismatch")
    guards = payload.get("r110_hardchecks", {}).get("required_guards", [])
    if len(guards) < 10:
        raise AssertionError("certificate payload omitted R110 guards")
    charts = payload.get("r110_hardchecks", {}).get("charts", {})
    if set(charts) != {"B", "C"}:
        raise AssertionError("certificate payload must contain both R110 charts")
    for chart_name, inverse in (("B", "z*B-1"), ("C", "z*C-1")):
        if charts[chart_name].get("inverse_equation") != inverse:
            raise AssertionError(f"R110 {chart_name} inverse guard mismatch")
        if not charts[chart_name].get("source_sha256"):
            raise AssertionError(f"R110 {chart_name} source pin missing")
        if not charts[chart_name].get("run_json_sha256"):
            raise AssertionError(f"R110 {chart_name} run pin missing")
        if not charts[chart_name].get("run_log_sha256"):
            raise AssertionError(f"R110 {chart_name} log pin missing")
    return payload


def q6_expression() -> sp.Expr:
    return (
        2 * p**4 * q**2 - 2 * p**4 * q + p**4
        + 2 * p**3 * q**3 - 7 * p**3 * q**2 + 5 * p**3 * q - 2 * p**3
        + 2 * p**2 * q**4 - 7 * p**2 * q**3 + 12 * p**2 * q**2
        - 7 * p**2 * q + 2 * p**2 - 2 * p * q**4 + 5 * p * q**3
        - 7 * p * q**2 + 2 * p * q + q**4 - 2 * q**3 + 2 * q**2
    )


class Algebra:
    """Exact arithmetic in A=QQ(p)[q]/(Q6)."""

    def __init__(self):
        self.q6_expr = sp.expand(q6_expression())
        self.q6 = sp.Poly(self.q6_expr, q, domain=K)
        if self.q6.degree() != 4:
            raise AssertionError(self.q6.degree())
        self.zero = (K.zero, K.zero, K.zero, K.zero)
        self.one = (K.one, K.zero, K.zero, K.zero)
        self._inverse = {}

    def from_expr(self, expr: object):
        num, den = sp.cancel(sp.sympify(expr)).as_numer_denom()
        n = sp.Poly(num, q, domain=K).rem(self.q6)
        d = sp.Poly(den, q, domain=K).rem(self.q6)
        if d.is_zero:
            raise AssertionError(("zero denominator modulo Q6", expr))
        key = tuple(K.convert(d.nth(i)) for i in range(4))
        inverse = self._inverse.get(key)
        if inverse is None:
            inverse_poly = sp.invert(d, self.q6)
            inverse = tuple(K.convert(inverse_poly.nth(i)) for i in range(4))
            self._inverse[key] = inverse
        raw = tuple(K.convert(n.nth(i)) for i in range(4))
        return self.mul(raw, inverse)

    def add(self, x, y):
        return tuple(x[i] + y[i] for i in range(4))

    def neg(self, x):
        return tuple(-x[i] for i in range(4))

    def mul(self, x, y):
        raw = [K.zero] * 7
        for i, xi in enumerate(x):
            if xi == K.zero:
                continue
            for j, yj in enumerate(y):
                if yj != K.zero:
                    raw[i + j] += xi * yj
        lead = K.convert(self.q6.LC())
        relation = tuple(-K.convert(self.q6.nth(i)) / lead for i in range(4))
        for degree in range(6, 3, -1):
            high = raw[degree]
            if high == K.zero:
                continue
            for i, coefficient in enumerate(relation):
                raw[degree - 4 + i] += high * coefficient
        return tuple(raw[:4])

    def as_expr(self, x):
        return sp.expand(sum(sp.sympify(x[i].as_expr()) * q**i for i in range(4)))

    def is_zero(self, x):
        return all(item == K.zero for item in x)


class BC:
    """Sparse B,C polynomial with coefficients in Algebra."""

    def __init__(self, algebra: Algebra, terms=None):
        self.A = algebra
        self.terms = {}
        for exp, value in (terms or {}).items():
            value = tuple(value)
            if not algebra.is_zero(value):
                self.terms[tuple(exp)] = value

    @classmethod
    def const(cls, algebra: Algebra, value):
        if not isinstance(value, tuple):
            value = algebra.from_expr(value)
        return cls(algebra, {(0, 0): value})

    @classmethod
    def var(cls, algebra: Algebra, exp):
        return cls(algebra, {tuple(exp): algebra.one})

    def __add__(self, other):
        out = dict(self.terms)
        for exp, value in other.terms.items():
            old = out.get(exp, self.A.zero)
            new = self.A.add(old, value)
            if self.A.is_zero(new):
                out.pop(exp, None)
            else:
                out[exp] = new
        return BC(self.A, out)

    def __neg__(self):
        return BC(self.A, {exp: self.A.neg(value) for exp, value in self.terms.items()})

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        out = {}
        for (bi, ci), x in self.terms.items():
            for (bj, cj), y in other.terms.items():
                exp = (bi + bj, ci + cj)
                value = self.A.mul(x, y)
                old = out.get(exp, self.A.zero)
                new = self.A.add(old, value)
                if self.A.is_zero(new):
                    out.pop(exp, None)
                else:
                    out[exp] = new
        return BC(self.A, out)


def det_bc(matrix, label: str) -> BC:
    """Compute a square determinant by sparse row/subset dynamic programming."""
    algebra = matrix[0][0].A
    states = {0: BC.const(algebra, 1)}
    n = len(matrix)
    for row_index, row in enumerate(matrix):
        nxt = {}
        for mask, value in states.items():
            for column, entry in enumerate(row):
                if mask & (1 << column) or not entry.terms:
                    continue
                before = sum(
                    1 for i in range(column) if not (mask & (1 << i))
                )
                term = value * entry
                if before & 1:
                    term = -term
                newmask = mask | (1 << column)
                nxt[newmask] = (
                    term if newmask not in nxt else nxt[newmask] + term
                )
        states = nxt
        print(
            f"[GLD101 primary] {label} row={row_index + 1}/{n} states={len(states)}",
            file=sys.stderr,
            flush=True,
        )
    return states.get((1 << n) - 1, BC.const(algebra, 0))


def q6_and_source():
    gld71 = load_module(GLD71, "gld71_for_gld101_primary")
    gld88 = load_module(GLD88, "gld88_for_gld101_primary")
    supports = {index: gld71.SPARSE_RELATIONS[index] for index in SUPPORT_ROWS}
    if tuple(sorted(supports)) != SUPPORT_ROWS:
        raise AssertionError("support rows drift")
    payload = [
        [index, [[list(indices), coefficient] for indices, coefficient in supports[index]]]
        for index in SUPPORT_ROWS
    ]
    support_digest = hashlib.sha256(
        json.dumps(payload, separators=(",", ":")).encode()
    ).hexdigest()
    if support_digest != EXPECTED_SUPPORT_DIGEST:
        raise AssertionError(f"support digest mismatch: {support_digest}")

    algebra = Algebra()
    q6_sha = hashlib.sha256(sp.srepr(algebra.q6_expr).encode()).hexdigest()
    if q6_sha != EXPECTED_Q6_SREPR_SHA256:
        raise AssertionError(f"Q6 pin mismatch: {q6_sha}")
    chart = gld88.h4_family(p, q, sp.Integer(0))
    leaves = [
        [BC.const(algebra, 1), BC.const(algebra, 1), BC.const(algebra, 1)],
        [BC.const(algebra, p), BC.const(algebra, q), BC.const(algebra, chart["s"])],
        [
            BC.const(algebra, 0),
            BC.const(algebra, 1 + chart["b"]) + BC.var(algebra, (1, 0)),
            BC.const(algebra, 1 + chart["c"]) + BC.var(algebra, (0, 1)),
        ],
    ]
    rows = {}
    for row in SUPPORT_ROWS:
        entries = []
        for root in range(3):
            for component in range(3):
                total = BC.const(algebra, 0)
                for indices, coefficient in supports[row]:
                    if indices[0] != root:
                        continue
                    term = (
                        leaves[indices[1]][component]
                        * leaves[indices[2]][component]
                        * leaves[indices[3]][component]
                    )
                    total = total + BC.const(algebra, coefficient) * term
                entries.append(total)
        rows[row] = entries
    return algebra, rows, chart, support_digest


def build_generators(algebra: Algebra, rows: dict[int, list]) -> dict[str, BC]:
    result = {}
    for name in ("T0", "T1", "T2", "T3", "D0", "D2", "Y0", "Y1", "X3"):
        rowset, columns = (
            NAMED[name] if name in NAMED else (RSTAR, EXTRA[name])
        )
        matrix = [[rows[row][column] for column in columns] for row in rowset]
        result[name] = det_bc(matrix, name)
        if (0, 0) in result[name].terms:
            raise AssertionError(f"{name} has a constant offset term")
        if name in SIX_NAMES:
            unexpected = sorted(set(result[name].terms) - set(SIX_COLUMNS))
            if unexpected:
                raise AssertionError(
                    f"{name} has unexpected offset monomials: {unexpected}"
                )
    return result


def det_tuple(algebra: Algebra, matrix, label: str):
    states = {0: algebra.one}
    n = len(matrix)
    for row_index, row in enumerate(matrix):
        nxt = {}
        for mask, value in states.items():
            for column, entry in enumerate(row):
                if mask & (1 << column) or algebra.is_zero(entry):
                    continue
                term = algebra.mul(value, entry)
                before = sum(
                    1 for i in range(column) if not (mask & (1 << i))
                )
                if before & 1:
                    term = algebra.neg(term)
                newmask = mask | (1 << column)
                nxt[newmask] = (
                    term if newmask not in nxt else algebra.add(nxt[newmask], term)
                )
        states = nxt
        print(
            f"[GLD101 primary] {label} row={row_index + 1}/{n} states={len(states)}",
            file=sys.stderr,
            flush=True,
        )
    return states.get((1 << n) - 1, algebra.zero)


def selector_det(algebra: Algebra, generators, names, columns, label):
    matrix = [
        [generators[name].terms.get(exp, algebra.zero) for name in names]
        for exp in columns
    ]
    return det_tuple(algebra, matrix, label)


def norm_record(algebra: Algebra, value) -> dict[str, object]:
    expr = sp.cancel(algebra.as_expr(value))
    numerator, denominator = expr.as_numer_denom()
    numerator_poly = sp.Poly(numerator, p, q, domain=QQ)
    denominator_poly = sp.Poly(denominator, p, q, domain=QQ)
    result = sp.cancel(
        sp.resultant(algebra.q6_expr, numerator_poly.as_expr(), q)
    )
    result_num, result_den = result.as_numer_denom()
    result_poly = sp.Poly(result_num, p, domain=QQ)
    if result_poly.is_zero:
        raise AssertionError("selector determinant norm is zero")
    _rational_content, primitive = result_poly.primitive()
    content, factors = sp.factor_list(primitive.as_expr(), p)
    return {
        "expression_sha256": hashlib.sha256(sp.srepr(expr).encode()).hexdigest(),
        "numerator_terms_pq": len(numerator_poly.terms()),
        "denominator": str(denominator_poly.as_expr()),
        "q6_degree": 4,
        "norm_numerator_degree_p": int(result_poly.degree()),
        "norm_numerator_terms_p": len(result_poly.terms()),
        "norm_numerator_sha256": hashlib.sha256(
            str(result_poly.as_expr()).encode()
        ).hexdigest(),
        "norm_denominator": str(result_den),
        "primitive_content": str(content),
        "primitive_factorization": [
            {
                "factor": str(factor),
                "degree": int(sp.degree(factor, p)),
                "exponent": int(exponent),
                "sha256": hashlib.sha256(
                    str(sp.expand(factor)).encode()
                ).hexdigest(),
            }
            for factor, exponent in factors
        ],
    }


def assert_norm(actual: dict[str, object], expected: dict[str, object], label: str):
    for key in (
        "expression_sha256",
        "norm_numerator_degree_p",
        "norm_numerator_terms_p",
        "norm_numerator_sha256",
    ):
        if actual[key] != expected[key]:
            raise AssertionError(
                f"{label} {key} mismatch: {actual[key]} != {expected[key]}"
            )
    if actual["primitive_content"] != expected.get("primitive_content", "1"):
        raise AssertionError(f"{label} primitive content mismatch")
    actual_factors = [
        (item["degree"], item["exponent"], item["sha256"])
        for item in actual["primitive_factorization"]
    ]
    if actual_factors != list(expected["factors"]):
        raise AssertionError(f"{label} factor signature mismatch")


def delta_expression(chart) -> sp.Expr:
    return sp.expand(
        (p - q)
        * (p + q - 1)
        * (p**2 - p + 1)
        * (p**2 + 2 * p * q - 2 * p - q)
        * (2 * p * q - p + q**2 - 2 * q)
        * chart["rank_denominator"]
    )


def assert_delta_resultant(algebra: Algebra, chart) -> dict[str, object]:
    delta = delta_expression(chart)
    resultant = sp.factor(sp.resultant(algebra.q6_expr, delta, q))
    expected = sp.sympify(EXPECTED_DELTA_RESULTANT)
    if sp.cancel(resultant - expected) != 0:
        raise AssertionError(f"Delta resultant mismatch: {resultant}")
    # Pin a canonical expanded representation.  The displayed resultant stays
    # factored, but SymPy's factored expression tree is not the payload whose
    # digest was recorded.
    srepr_sha = hashlib.sha256(sp.srepr(sp.expand(resultant)).encode()).hexdigest()
    if srepr_sha != EXPECTED_DELTA_RESULTANT_SREPR_SHA256:
        raise AssertionError(f"Delta resultant hash mismatch: {srepr_sha}")
    return {
        "delta": str(delta),
        "resultant": str(resultant),
        "resultant_srepr_sha256": srepr_sha,
        "resultant_degree_p": int(sp.degree(resultant, p)),
        "resultant_terms_p": len(sp.Poly(resultant, p).terms()),
    }


def _find_run_json(base: Path, expected_sha: str) -> Path | None:
    if not base.exists():
        return None
    matches = [
        path
        for path in base.rglob("run.json")
        if sha256_bytes(path.read_bytes()) == expected_sha
    ]
    if len(matches) != 1:
        raise AssertionError(
            f"run JSON pin mismatch under {base}: {len(matches)} matches"
        )
    return matches[0]


def _replay(
    label: str,
    source_name: str,
    source_sha: str,
    run_id: str,
    run_json_sha: str,
    run_log_sha: str,
    markers: tuple[str, ...],
    require: bool,
    load_bearing: bool = True,
) -> dict[str, object]:
    source = ROOT / ".research-runs" / source_name
    base = ROOT / ".research-runs" / run_id
    if not source.exists() or not base.exists():
        if require and load_bearing:
            raise AssertionError(f"required replay missing: {label}")
        return {
            "label": label,
            "required": load_bearing,
            "present": False,
            "reason": "ignored source or run directory absent",
        }
    actual_source_sha = sha256_bytes(source.read_bytes())
    if actual_source_sha != source_sha:
        raise AssertionError(
            f"{label} source pin mismatch: {actual_source_sha} != {source_sha}"
        )
    run_json = _find_run_json(base, run_json_sha)
    assert run_json is not None
    run_log = run_json.parent / "run.log"
    if not run_log.exists() or sha256_bytes(run_log.read_bytes()) != run_log_sha:
        raise AssertionError(f"{label} run log pin mismatch")
    metadata = json.loads(run_json.read_text(encoding="utf-8"))
    if metadata.get("status") != "succeeded":
        raise AssertionError(f"{label} is not a succeeded run")
    log_text = run_log.read_text(encoding="utf-8", errors="replace")
    absent = [marker for marker in markers if marker not in log_text]
    if absent:
        raise AssertionError(f"{label} missing log markers: {absent}")
    return {
        "label": label,
        "required": load_bearing,
        "present": True,
        "source": str(source),
        "source_sha256": actual_source_sha,
        "run_json": str(run_json),
        "run_json_sha256": run_json_sha,
        "run_log": str(run_log),
        "run_log_sha256": run_log_sha,
        "status": metadata.get("status"),
        "markers": list(markers),
    }


def check_external_offset_evidence(require: bool) -> dict[str, object]:
    """Optionally check ignored provenance for a stronger offset claim.

    The scoped GLD101 norm-cover theorem must be invariant under whatever
    stale or partial exploratory files happen to exist in ``.research-runs``.
    Therefore the default mode does not inspect that directory at all.
    """
    if not require:
        return {
            "checked": False,
            "strict_evidence": False,
            "reason": "external offset-fibre replays are not inputs to GLD101",
            "certificate_payload": str(CERTIFICATE_PAYLOAD),
            "certificate_payload_sha256": EXPECTED_CERTIFICATE_PAYLOAD_SHA256,
        }
    certificate_payload = load_certificate_payload()
    entries = []
    p0p1 = ROOT / ".research-runs" / "e31_p0_p1_exact_audit_v10.json"
    p0p1_sha = (
        "1d6bd26f22b875a6a024e8c9d357e4cc5c862efc66e61371dc22b98ec10aaf9f"
    )
    if not p0p1.exists():
        if require:
            raise AssertionError("required p=0,1 exact package missing")
        entries.append(
            {
                "label": "p=0,1 exact scoped package",
                "required": True,
                "present": False,
                "reason": "ignored artifact absent",
            }
        )
    else:
        actual = sha256_bytes(p0p1.read_bytes())
        if actual != p0p1_sha:
            raise AssertionError(f"p=0,1 package pin mismatch: {actual}")
        payload = json.loads(p0p1.read_text(encoding="utf-8"))
        if payload.get("status") != "verified_exact_scoped_local_certificate":
            raise AssertionError("p=0,1 package status mismatch")
        entries.append(
            {
                "label": "p=0,1 exact scoped package",
                "required": True,
                "present": True,
                "sha256": actual,
                "status": payload.get("status"),
            }
        )

    # GLD99 is tracked and its normalized source pin was checked before
    # import.  It is a separate H2=0 theorem leaf, not a consequence of this
    # norm computation.
    entries.append(
        {
            "label": "H2=0 GLD99 tracked leaf",
            "required": True,
            "present": True,
            "source": str(GLD99),
            "lf_sha256": EXPECTED_SOURCE_PINS["GLD99"]["lf_sha256"],
            "status": "tracked_exact_scoped_leaf",
        }
    )

    replay_specs = (
        (
            "p^2+1, B chart",
            "e31_a0_fibre_d2_fae3e839d66d_B_char0.sing",
            "f7e46add8faf31fd372efb61877fffedd135bc08154ed1c1aba1a97b9bd4a5b0",
            "e31-a0-fibre-d2-B-char0-root-v1",
            "1eb8ad8b7e664637d6e5bc70e729cb4295da7e097d338303a47f8389d2784496",
            "90ec29c7ef4be149f72eb1be1a1b1a868f9ae200526a0098147b308ae53aa29e",
        ),
        (
            "p^2+1, C chart",
            "e31_a0_fibre_d2_fae3e839d66d_C_char0.sing",
            "5907c00333f3839f28d9269611866ddb200f868e3db88cad63a4f643a77d35e8",
            "e31-a0-fibre-d2-C-char0-root-v1",
            "1f3f83d62dc657cad74a601aba119966680d632a487e6ef281112f141b0368c2",
            "90ec29c7ef4be149f72eb1be1a1b1a868f9ae200526a0098147b308ae53aa29e",
        ),
        (
            "R4, B chart",
            "e31_a0_fibre_d4_59d876136007_B_char0.sing",
            "e4cb61031df2185b0fd6f260295fc9e1fc041e5f785f286c71de8e78ec57887d",
            "e31-a0-fibre-d4-B-char0-root-v1",
            "f01cbeee30dda06f87d6d17af36d5d4ee36b06dca7fe4af694c486e0d71630a9",
            "90ec29c7ef4be149f72eb1be1a1b1a868f9ae200526a0098147b308ae53aa29e",
        ),
        (
            "R4, C chart",
            "e31_a0_fibre_d4_59d876136007_C_char0.sing",
            "d4714da5eabbed1e1e3f8db3b926becbcc581046f6309a7b550e14d0f6ada1f0",
            "e31-a0-fibre-d4-C-char0-root-v1",
            "11a058289c47171ed392bb5db6d5ccb2bcb82dc2934b01d10ec2754b161aef4a",
            "90ec29c7ef4be149f72eb1be1a1b1a868f9ae200526a0098147b308ae53aa29e",
        ),
        (
            "R8, B chart",
            "e31_a0_fibre_d8_19e8048b6aa1_B_char0.sing",
            "d72331f80fdc90a5be611defed4b04e7d1c631aa14973795f8a3c9e7cf44edcb",
            "e31-a0-fibre-d8-B-char0-root-v1",
            "64ec369db5d0275e1a4b32022d5973ac1e8bbf4bde9ff2a02185dc8736eb6c63",
            "90ec29c7ef4be149f72eb1be1a1b1a868f9ae200526a0098147b308ae53aa29e",
        ),
        (
            "R8, C chart",
            "e31_a0_fibre_d8_19e8048b6aa1_C_char0.sing",
            "a359e08897e5b1a40d8c9a072ebba8292f92997c7844dfcfcd4c7746204eaebb",
            "e31-a0-fibre-d8-C-char0-root-v1",
            "74c2d0d081442665b7008a39c50ea28d91aee6526b2fa994cbc407566c07c5e",
            "90ec29c7ef4be149f72eb1be1a1b1a868f9ae200526a0098147b308ae53aa29e",
        ),
    )
    for spec in replay_specs:
        entries.append(
            _replay(
                spec[0],
                spec[1],
                spec[2],
                spec[3],
                spec[4],
                spec[5],
                ("BASIS_SIZE=1", "UNIT_IDEAL=1"),
                require,
            )
        )

    # The two R110 guarded identities are load-bearing.  Older linear-q UNIT
    # logs are deliberately not substituted for these checks.
    guard_markers = tuple(certificate_payload["r110_hardchecks"]["required_guards"])
    for chart_name in ("B", "C"):
        chart = certificate_payload["r110_hardchecks"]["charts"][chart_name]
        entries.append(
            _replay(
                f"R110 {chart_name} guarded q-substitution certificate",
                Path(chart["source"]).name,
                chart["source_sha256"],
                chart["run_id"],
                chart["run_json_sha256"],
                chart["run_log_sha256"],
                guard_markers,
                require,
                load_bearing=True,
            )
        )
    required = [entry for entry in entries if entry["required"]]
    return {
        "checked": True,
        "strict_evidence": bool(required) and all(
            entry["present"] for entry in required
        ),
        "required_entry_count": len(required),
        "present_required_entry_count": sum(
            bool(entry["present"]) for entry in required
        ),
        "entries": entries,
        "certificate_payload": str(CERTIFICATE_PAYLOAD),
        "certificate_payload_sha256": EXPECTED_CERTIFICATE_PAYLOAD_SHA256,
        "caveats": [
            "Ignored Singular replays are optional provenance for a stronger offset-closure claim, not inputs to GLD101.",
            "R110 B and C are guarded identity replays; both are required only in strict external-evidence mode.",
            "Older linear-q UNIT logs are retained as history but are not counted.",
            "No direct d110 full-source timeout is counted as evidence.",
        ],
    }


def check(require_external_fibre_evidence: bool = False, include_eight: bool = False):
    started = time.monotonic()
    source_manifest = pinned_source_manifest()
    certificate_payload = load_certificate_payload()
    algebra, rows, chart, support_digest = q6_and_source()
    generators = build_generators(algebra, rows)

    six_det = selector_det(
        algebra, generators, SIX_NAMES, SIX_COLUMNS, "six-selector"
    )
    six_norm = norm_record(algebra, six_det)
    assert_norm(six_norm, EXPECTED_SIX_NORM, "six-selector norm")

    eight_norm = None
    if include_eight:
        eight_det = selector_det(
            algebra, generators, EIGHT_NAMES, EIGHT_COLUMNS, "eight-selector"
        )
        eight_norm = norm_record(algebra, eight_det)
        assert_norm(eight_norm, EXPECTED_EIGHT_NORM, "eight-selector norm")

    delta = assert_delta_resultant(algebra, chart)
    external = check_external_offset_evidence(require_external_fibre_evidence)
    return {
        "status": "exact_scoped_GLD101_a0_six_selector_norm_cover_reduction",
        "global_conjecture": "UNRESOLVED",
        "scope": {
            "branch": "a=0",
            "chart": "GLD88 equal-leaf H4 family",
            "quotient": "QQ(p)[q]/(Q6)",
            "upstream_open": "D(H2*Delta) plus the named pivot/chart gates",
            "conclusion": "necessary-selector norm cover only",
        },
        "source_pins": source_manifest,
        "certificate_payload": {
            "path": str(CERTIFICATE_PAYLOAD),
            "sha256": EXPECTED_CERTIFICATE_PAYLOAD_SHA256,
        },
        "support_rows": list(SUPPORT_ROWS),
        "support_digest": support_digest,
        "q6": {
            "expression": str(algebra.q6_expr),
            "degree_q": int(algebra.q6.degree()),
            "srepr_sha256": EXPECTED_Q6_SREPR_SHA256,
            "leading_coefficient": str(algebra.q6.LC()),
        },
        "actual_minors": {
            "named": {
                name: {
                    "rows": list(NAMED[name][0]),
                    "columns": list(NAMED[name][1]),
                    "bc_terms": len(generators[name].terms),
                }
                for name in NAMED
            },
            "extra": {
                name: {
                    "rows": list(RSTAR),
                    "columns": list(EXTRA[name]),
                    "bc_terms": len(generators[name].terms),
                }
                for name in EXTRA
            },
        },
        "six_selector": {
            "names": list(SIX_NAMES),
            "columns": [list(exp) for exp in SIX_COLUMNS],
            "norm": six_norm,
        },
        "eight_selector": (
            {
                "names": list(EIGHT_NAMES),
                "columns": [list(exp) for exp in EIGHT_COLUMNS],
                "norm": eight_norm,
            }
            if include_eight
            else {"skipped": True}
        ),
        "delta_resultant": delta,
        "external_offset_evidence": external,
        "one_way_bridge": [
            "rank(M)<=6 makes each selected actual seven-minor vanish",
            "a nonzero (B,C) gives a nonzero BC support vector, hence selector determinants vanish",
            "selector/norm vanishing is not sufficient for physical rank",
        ],
        "nonclaims": [
            "This does not prove the global conjecture.",
            "Modular or ignored solver evidence is not promoted to QQ ideal membership.",
            "External fibre replays are not composed into an offset-closure theorem.",
            "The exact conclusion is only the necessary norm-factor support cover.",
        ],
        "elapsed_seconds": round(time.monotonic() - started, 3),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--require-external-fibre-evidence",
        action="store_true",
        help="also require ignored offset-fibre provenance replays",
    )
    parser.add_argument(
        "--include-eight",
        action="store_true",
        help="also replay the non-load-bearing eight-selector control norm",
    )
    args = parser.parse_args()
    result = check(
        require_external_fibre_evidence=args.require_external_fibre_evidence,
        include_eight=args.include_eight,
    )
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print("GLD101 a=0 six-selector norm-cover primary replay: PASS")
    print(text)


if __name__ == "__main__":
    main()
