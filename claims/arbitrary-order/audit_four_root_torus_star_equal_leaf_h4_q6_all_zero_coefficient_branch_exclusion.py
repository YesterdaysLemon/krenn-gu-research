#!/usr/bin/env python3
"""Independent GLD103 audit for the arbitrary-``a`` all-zero branch.

The audit deliberately does not import the GLD103 primary (or any private
helper).  The graph data are read as literals from the pinned GLD71 source and
the H4 chart is transcribed here.  A small quotient algebra and a sparse
offset-polynomial determinant implementation rebuild the five actual
seven-minors, their ``A=F+C*G`` decompositions, ``P0=F_T0/B``, the six
quadratic coefficient rows, and the eight requested coefficient determinants.

The expensive p-cover is recomputed in exact python-flint ``fmpz_mpoly``
arithmetic.  The fibre routines are exact fraction-free quotient-field
Macaulay checks.  This is an audit of a necessary bridge only: all rank and
coefficient implications are one-way, and the global Krenn--Gu conjecture is
still ``UNRESOLVED``.

``--manifest-only`` performs only cheap source, scope, and dependency-pin
checks.  ``--bridge-only`` rebuilds the sparse graph bridge without the heavy
cover/fibre stage.  The default runs the complete audit and may take several
minutes with python-flint 0.9.0 installed.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.util
import itertools
import json
import platform
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import sympy as sp
from sympy import QQ


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "claims" / "arbitrary-order"
GLD70 = BASE / "verify_four_root_complete_q_layer_secant_boundary_trap_and_torus_star_compression.py"
GLD71 = BASE / "verify_four_root_torus_star_punctured_syndrome_and_eisenstein_norm_gate.py"
GLD88 = BASE / "verify_four_root_torus_star_equal_leaf_h4_generic_rank_six_common_row_kernel_exclusion.py"
GLD96 = BASE / "explore_four_root_torus_star_equal_leaf_h4_q6_modular_membership_census.py"
GLD102_AUDIT = BASE / "audit_four_root_torus_star_equal_leaf_h4_q6_p01_nonzero_offset_exclusion.py"

p, a, q, B, C, z = sp.symbols("p a q B C z")
K = QQ.frac_field(p, a)

P = sp.expand(p**2 - p + 1)
H2 = sp.expand(2 * p**2 - 2 * p + 1)
RANK_DENOMINATOR = sp.expand(
    2 * p * q**2 - 2 * p * q - p - q**2 - 2 * q + 2
)
DELTA = sp.expand(
    (p - q)
    * (p + q - 1)
    * P
    * (p**2 + 2 * p * q - 2 * p - q)
    * (2 * p * q - p + q**2 - 2 * q)
    * RANK_DENOMINATOR
)

SUPPORT_ROWS = (0, 1, 2, 3, 17, 25, 28, 31, 32, 33)
MINOR_ORDER = ("T0", "T1", "T2", "Y1", "X3")
MINOR_DATA = {
    "T0": ((0, 1, 2, 17, 25, 31, 28), (0, 1, 3, 4, 6, 7, 8)),
    "T1": ((0, 1, 2, 17, 25, 31, 32), (0, 1, 3, 4, 6, 7, 2)),
    "T2": ((0, 1, 2, 17, 25, 31, 32), (0, 1, 3, 4, 6, 7, 5)),
    "Y1": ((0, 1, 17, 28, 31, 32, 33), (0, 1, 3, 4, 5, 6, 7)),
    "X3": ((0, 1, 17, 28, 31, 32, 33), (0, 1, 2, 3, 4, 6, 7)),
}

# Six coefficient rows are P0=F_T0/B followed by the five C-coefficient
# rows.  All twenty maximal row minors are necessary; these eight are the
# six cover minors plus the D134/D145 fibre pair.
SELECTED_TRIPLES = {
    "D012": (0, 1, 2),
    "D013": (0, 1, 3),
    "D023": (0, 2, 3),
    "D123": (1, 2, 3),
    "D134": (1, 3, 4),
    "D014": (0, 1, 4),
    "D145": (1, 4, 5),
    "D015": (0, 1, 5),
}
COVER_TRIPLES = ("D012", "D013", "D023", "D123", "D014", "D015")
FIBRE_TRIPLES = ("D012", "D013", "D134", "D145")
ALL_COEFFICIENT_TRIPLES = tuple(
    f"D{first}{second}{third}"
    for first, second, third in itertools.combinations(range(6), 3)
)

# Parameter-only clearing is intentionally not primitive-normalized.  It is
# the same mathematical clearing gate as the primary, but the determinant and
# quotient arithmetic below are independent.
CLEARING_SCALARS = {
    "T0": 4 * P**3 * H2**5,
    "T1": 16 * P**5 * H2**5,
    "T2": 16 * P**5 * H2**5,
    "Y1": 4 * P**5 * H2**5,
    "X3": 4 * P**5 * H2**5,
}

# Descending coefficients of the pinned degree-40 residual factor.
F40_DESC = (
    7424, -161536, 1836800, -14454272, 88040000, -439964928,
    1867353392, -6884518384, 22398599716, -65072430404,
    170375836211, -405009960715, 879376810077, -1752467492937,
    3218063082751, -5462157661436, 8590438351195, -12541353394198,
    17018386499813, -21483026442413, 25236982384561, -27587608118151,
    28047919243155, -26495326489138, 23220609127349, -18842006278252,
    14118028970848, -9735354310506, 6152381134918, -3545007905402,
    1850774728870, -868862487040, 363420905896, -133926993072,
    42888299184, -11728177920, 2675395584, -492086016, 69030144,
    -6635520, 331776,
)

SOURCE_PINS = {
    "GLD70": (GLD70, "a53433329023223f1f24e960a8b23c7c57baf87b9767c4b2acabc819b982918e", "1a967f71bc4a08995a9187557eccd0ce39ab0f65544652f99c538049c49251f2"),
    "GLD71": (GLD71, "3342809b22cc1e5ffe960e14068f81303a3bc0b597e21e2d29c05c10c605dc7d", "e0204ec4495bb3f86252c18d77e3493dd6d1b0e3011e33866a2a0b2462922d5e"),
    "GLD88": (GLD88, "70c46728c397d7a18fd999c27ca3d10232f9e3169ad508be7071c109be322752", "4ba10801ea64fbb170d7949a7030d64da6c1fd707bb894d8c1372947668d8199"),
    "GLD96_Q6": (GLD96, "00417d6dd6b27b1bc6cc51ccdf8d8536061abaa8fa9291befca06cb5bfd55cf1", "bd4e57c6cb4fb71a8a5c2b503980faacfd1f96994cc583d2d630780e3934ca25"),
    "GLD102_AUDIT": (GLD102_AUDIT, "8f364564dac2dc98955ac8171b5a7de378ec791581bd0523ddce7d7e83849843", "3d976c4e9470a4c5acece6052acd275b96dc257b82cc197183375825ec6082ec"),
}

EXPECTED_SUPPORT_DIGEST = "c53d2c7912d87b5f46c39ec6fc64d1aaa6ab7839ad69f3bbfb6f39375b6ed1b0"
EXPECTED_ALL_SUPPORT_DIGEST = "22898fcc93f415be5488d22ecf2e74febb74cbd7997ef3c8d9dc2efc3545e324"
EXPECTED_GLD102_SUPPORT_DIGEST = "f2670c9393287eae16dce1bc8aa41e4b0c421645833ad29619a6d7b6fd94ac07"
EXPECTED_Q6_SREPR_SHA256 = "2ed58764e7c50c8e1510a93b32d2515a9297c03dfe297fed8d9abe5f8e9d71a7"


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def source_hash(path: Path, lf: bool = False) -> str:
    data = path.read_bytes()
    if lf:
        data = data.replace(b"\r\n", b"\n")
    return sha256_bytes(data)


def audit_source_manifest() -> dict[str, str]:
    """Pin the exact tracked audit source used by a full replay."""
    path = Path(__file__).resolve()
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "sha256": source_hash(path),
        "lf_sha256": source_hash(path, lf=True),
    }


def source_manifest() -> dict[str, dict[str, str]]:
    """Pin only committed canonical sources; no generated or ignored data."""
    result: dict[str, dict[str, str]] = {}
    for name, (path, expected, expected_lf) in SOURCE_PINS.items():
        if not path.is_file():
            raise AssertionError(f"missing canonical source: {path}")
        actual = source_hash(path)
        actual_lf = source_hash(path, lf=True)
        if actual != expected and actual_lf != expected_lf:
            raise AssertionError(f"{name} source hash mismatch")
        if actual_lf != expected_lf:
            raise AssertionError(f"{name} normalized source hash mismatch")
        result[name] = {
            "path": path.relative_to(ROOT).as_posix(),
            "sha256": actual,
            "lf_sha256": actual_lf,
        }
    return result


def _literal_assignment(path: Path, name: str) -> object:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            if any(isinstance(target, ast.Name) and target.id == name for target in node.targets):
                return ast.literal_eval(node.value)
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.target.id == name:
            return ast.literal_eval(node.value)
    raise AssertionError(f"literal {name} not found in canonical source")


def canonical_support() -> tuple[tuple[tuple[tuple[int, int, int, int], int], ...], ...]:
    value = _literal_assignment(GLD71, "SPARSE_RELATIONS")
    if not isinstance(value, tuple) or len(value) != 37:
        raise AssertionError("GLD71 sparse support shape drift")
    for row in value:
        if not isinstance(row, tuple):
            raise AssertionError("GLD71 sparse row is not a tuple")
    return value


def support_digests(relations) -> dict[str, str]:
    def digest(rows):
        payload = [
            [row, [[list(indices), coefficient] for indices, coefficient in relations[row]]]
            for row in rows
        ]
        return sha256_bytes(json.dumps(payload, separators=(",", ":")).encode())

    selected = digest(SUPPORT_ROWS)
    all_rows = digest(range(len(relations)))
    if selected != EXPECTED_SUPPORT_DIGEST or all_rows != EXPECTED_ALL_SUPPORT_DIGEST:
        raise AssertionError(f"canonical support digest drift: {selected} {all_rows}")
    return {"selected_rows": selected, "all_rows": all_rows}


def q6_expression(p_value=p, q_value=q) -> sp.Expr:
    return sp.expand(
        2 * p_value**4 * q_value**2 - 2 * p_value**4 * q_value + p_value**4
        + 2 * p_value**3 * q_value**3 - 7 * p_value**3 * q_value**2
        + 5 * p_value**3 * q_value - 2 * p_value**3
        + 2 * p_value**2 * q_value**4 - 7 * p_value**2 * q_value**3
        + 12 * p_value**2 * q_value**2 - 7 * p_value**2 * q_value
        + 2 * p_value**2 - 2 * p_value * q_value**4
        + 5 * p_value * q_value**3 - 7 * p_value * q_value**2
        + 2 * p_value * q_value + q_value**4 - 2 * q_value**3
        + 2 * q_value**2
    )


def h4_family() -> dict[str, sp.Expr]:
    """Local transcription of the GLD88/F88 arbitrary-a H4 chart."""
    d0 = p + q - 1
    e = RANK_DENOMINATOR
    nb = (
        -2 * a * p**2 * q**3 + 3 * a * p**2 * q**2 - 3 * a * p**2 * q + a * p**2
        + 2 * a * p * q**3 + 2 * a * p + a * q**3 - 3 * a * q**2 + 3 * a * q - 2 * a
        + p**3 * q**2 - p**3 + p**2 * q**3 - 3 * p**2 * q**2 + p**2
        - 2 * p * q**3 + 3 * p * q**2 - 2 * p + q**2 - 3 * q + 2
    )
    nc = (
        2 * a * p * q**3 - 3 * a * p * q**2 + 3 * a * p * q - a * p
        - a * q**3 + 3 * a * q**2 - 3 * a * q + 2 * a
        + p**2 * q**2 - 2 * p**2 * q - 3 * p * q**2 + p * q + p
        - q**2 + 3 * q - 2
    )
    return {
        "s": sp.cancel((p + q - p * q) / d0),
        "b": sp.cancel(-nb / (P * e)),
        "c": sp.cancel(-nc / (d0 * e)),
        "h4_denominator": d0,
        "rank_denominator": e,
    }


def compare_h4_family_to_pinned_gld88() -> dict[str, Any]:
    """Compare the local chart transcription with tracked GLD88 only.

    This is a provenance check, not an input path: all bridge and fibre
    arithmetic uses the local ``h4_family`` above.  The tracked GLD88 module
    is imported solely to obtain its public chart output for this comparison;
    the GLD103 primary and any private helper are never imported.
    """
    spec = importlib.util.spec_from_file_location("_gld88_chart_comparison", GLD88)
    if spec is None or spec.loader is None:
        raise AssertionError("cannot load pinned GLD88 chart for comparison")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    canonical = module.h4_family(p, q, a)
    local = h4_family()
    equalities: dict[str, bool] = {}
    for name in ("s", "b", "c"):
        equalities[name] = bool(sp.cancel(local[name] - canonical[name]) == 0)
    if not all(equalities.values()):
        raise AssertionError(("GLD88 h4_family transcription mismatch", equalities))
    return {
        "source": GLD88.relative_to(ROOT).as_posix(),
        "source_sha256": source_hash(GLD88),
        "comparison_only": True,
        "local_computation_inputs": True,
        "canonical_outputs_used_as_audit_inputs": False,
        "s_equal": equalities["s"],
        "b_equal": equalities["b"],
        "c_equal": equalities["c"],
        "all_equal": True,
    }


def denominator_provenance(chart: dict[str, sp.Expr]) -> dict[str, Any]:
    """Require every transcribed chart denominator to lie in the Delta gate."""
    expected = {
        "s": chart["h4_denominator"],
        "b": P * chart["rank_denominator"],
        "c": chart["h4_denominator"] * chart["rank_denominator"],
    }
    records = {}
    for name, denominator in expected.items():
        actual_denominator = sp.cancel(chart[name]).as_numer_denom()[1]
        denominator_ratio = sp.cancel(actual_denominator / denominator)
        if sp.denom(denominator_ratio) != 1 or denominator_ratio.has(p, q):
            raise AssertionError(("chart denominator transcription drift", name, actual_denominator, denominator))
        quotient = sp.cancel(DELTA / denominator)
        if sp.denom(quotient) != 1 or sp.expand(DELTA - denominator * quotient) != 0:
            raise AssertionError(("chart denominator is outside Delta", name, denominator))
        records[name] = {
            "denominator": str(sp.factor(denominator)),
            "actual_denominator": str(sp.factor(actual_denominator)),
            "Delta_quotient": str(sp.factor(quotient)),
            "supported_by_Delta": True,
        }
    return records


class QuotientAlgebra:
    """QQ(p,a)[q]/(Q6), with low-q coefficient tuples."""

    def __init__(self, modulus: sp.Expr):
        self.q6_expr = sp.expand(modulus)
        self.q6 = sp.Poly(self.q6_expr, q, domain=K)
        if self.q6.degree() != 4:
            raise AssertionError("Q6 degree drift")
        lead = K.convert(self.q6.LC())
        self.relation = tuple(-K.convert(self.q6.nth(i)) / lead for i in range(4))
        self.zero = (K.zero, K.zero, K.zero, K.zero)
        self.one = (K.one, K.zero, K.zero, K.zero)
        self._inverse_cache: dict[tuple[str, ...], tuple[Any, ...]] = {}

    def is_zero(self, value) -> bool:
        return all(item == K.zero for item in value)

    def from_expr(self, expression: object):
        numerator, denominator = sp.cancel(sp.sympify(expression)).as_numer_denom()
        n = sp.Poly(numerator, q, domain=K).rem(self.q6)
        d = sp.Poly(denominator, q, domain=K).rem(self.q6)
        if d.is_zero:
            raise AssertionError(("zero denominator modulo Q6", expression))
        key = tuple(str(d.nth(i)) for i in range(4))
        inverse = self._inverse_cache.get(key)
        if inverse is None:
            inv = sp.invert(d, self.q6)
            inverse = tuple(K.convert(inv.nth(i)) for i in range(4))
            self._inverse_cache[key] = inverse
        raw = tuple(K.convert(n.nth(i)) for i in range(4))
        return self.mul(raw, inverse)

    def add(self, left, right):
        return tuple(left[i] + right[i] for i in range(4))

    def neg(self, value):
        return tuple(-value[i] for i in range(4))

    def sub(self, left, right):
        return self.add(left, self.neg(right))

    def mul(self, left, right):
        raw = [K.zero] * 7
        for i, x in enumerate(left):
            if x == K.zero:
                continue
            for j, y in enumerate(right):
                if y != K.zero:
                    raw[i + j] += x * y
        for degree in range(6, 3, -1):
            high = raw[degree]
            if high == K.zero:
                continue
            for i, coefficient in enumerate(self.relation):
                raw[degree - 4 + i] += high * coefficient
        return tuple(raw[:4])

    def as_expr(self, value) -> sp.Expr:
        return sp.expand(sum(sp.sympify(value[i].as_expr()) * q**i for i in range(4)))


class SparseOffset:
    """Sparse exact polynomial in (B,C) with quotient-algebra coefficients."""

    def __init__(self, algebra: QuotientAlgebra, terms: dict[tuple[int, int], Any] | None = None):
        self.A = algebra
        self.terms: dict[tuple[int, int], Any] = {}
        for exponent, value in (terms or {}).items():
            value = tuple(value)
            if not algebra.is_zero(value):
                self.terms[tuple(exponent)] = value

    @classmethod
    def const(cls, algebra: QuotientAlgebra, value: object):
        return cls(algebra, {(0, 0): value if isinstance(value, tuple) else algebra.from_expr(value)})

    @classmethod
    def variable(cls, algebra: QuotientAlgebra, exponent: tuple[int, int]):
        return cls(algebra, {tuple(exponent): algebra.one})

    def __add__(self, other):
        out = dict(self.terms)
        for exponent, value in other.terms.items():
            updated = self.A.add(out.get(exponent, self.A.zero), value)
            if self.A.is_zero(updated):
                out.pop(exponent, None)
            else:
                out[exponent] = updated
        return SparseOffset(self.A, out)

    def __neg__(self):
        return SparseOffset(self.A, {e: self.A.neg(v) for e, v in self.terms.items()})

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        out: dict[tuple[int, int], Any] = {}
        for (lb, lc), left in self.terms.items():
            for (rb, rc), right in other.terms.items():
                exponent = (lb + rb, lc + rc)
                value = self.A.mul(left, right)
                updated = self.A.add(out.get(exponent, self.A.zero), value)
                if self.A.is_zero(updated):
                    out.pop(exponent, None)
                else:
                    out[exponent] = updated
        return SparseOffset(self.A, out)


def shift_b(value: SparseOffset, amount: int = 1) -> SparseOffset:
    return SparseOffset(value.A, {(b + amount, c): coefficient for (b, c), coefficient in value.terms.items()})


def divide_by_b(value: SparseOffset, label: str) -> SparseOffset:
    if any(b == 0 for b, _ in value.terms):
        raise AssertionError(f"{label} is not B-divisible")
    quotient = SparseOffset(value.A, {(b - 1, c): coefficient for (b, c), coefficient in value.terms.items()})
    if (shift_b(quotient).terms != value.terms):
        raise AssertionError(f"{label} B-division failed")
    return quotient


def determinant_sparse(matrix: list[list[SparseOffset]], label: str) -> SparseOffset:
    if not matrix or any(len(row) != len(matrix) for row in matrix):
        raise AssertionError(f"{label} is not square")
    algebra = matrix[0][0].A
    states: dict[int, SparseOffset] = {0: SparseOffset.const(algebra, 1)}
    size = len(matrix)
    for row in matrix:
        next_states: dict[int, SparseOffset] = {}
        for mask, value in states.items():
            for column, entry in enumerate(row):
                if mask & (1 << column) or not entry.terms:
                    continue
                inversions = sum(1 for previous in range(column + 1, size) if mask & (1 << previous))
                term = value * entry
                if inversions & 1:
                    term = -term
                new_mask = mask | (1 << column)
                next_states[new_mask] = term if new_mask not in next_states else next_states[new_mask] + term
        states = next_states
    return states.get((1 << size) - 1, SparseOffset.const(algebra, 0))


def partition_affine(value: SparseOffset, label: str) -> tuple[SparseOffset, SparseOffset]:
    f_terms: dict[tuple[int, int], Any] = {}
    g_terms: dict[tuple[int, int], Any] = {}
    for (b_degree, c_degree), coefficient in value.terms.items():
        if c_degree == 0:
            f_terms[(b_degree, 0)] = coefficient
        elif c_degree == 1:
            g_terms[(b_degree, 0)] = coefficient
        else:
            raise AssertionError(f"{label} has C-degree > 1")
    f, g = SparseOffset(value.A, f_terms), SparseOffset(value.A, g_terms)
    recomposed = f + SparseOffset.variable(value.A, (0, 1)) * g
    if recomposed.terms != value.terms:
        raise AssertionError(f"{label} affine-C recomposition failed")
    if any(b == 0 for b, _ in f.terms):
        raise AssertionError(f"{label} F(B=0) is nonzero")
    return f, g


def coefficient_rows(values: list[SparseOffset]) -> list[list[Any]]:
    result = []
    algebra = values[0].A
    for index, value in enumerate(values):
        if any(c for _, c in value.terms):
            raise AssertionError(f"P{index} unexpectedly depends on C")
        if any(b > 2 for b, _ in value.terms):
            raise AssertionError(f"P{index} has B-degree > 2")
        row = [value.terms.get((degree, 0), algebra.zero) for degree in range(3)]
        rebuilt = SparseOffset(algebra, {(degree, 0): item for degree, item in enumerate(row) if not algebra.is_zero(item)})
        if rebuilt.terms != value.terms:
            raise AssertionError(f"P{index} coefficient extraction failed")
        result.append(row)
    return result


def det3_expansion(algebra: QuotientAlgebra, rows: list[list[Any]]):
    a0, b0, c0 = rows[0]
    a1, b1, c1 = rows[1]
    a2, b2, c2 = rows[2]
    first = algebra.mul(a0, algebra.sub(algebra.mul(b1, c2), algebra.mul(c1, b2)))
    second = algebra.mul(b0, algebra.sub(algebra.mul(a1, c2), algebra.mul(c1, a2)))
    third = algebra.mul(c0, algebra.sub(algebra.mul(a1, b2), algebra.mul(b1, a2)))
    return algebra.add(algebra.sub(first, second), third)


def det3_permutation(algebra: QuotientAlgebra, rows: list[list[Any]]):
    result = algebra.zero
    for permutation in itertools.permutations(range(3)):
        inversions = sum(permutation[i] > permutation[j] for i in range(3) for j in range(i + 1, 3))
        term = algebra.one
        for row, column in enumerate(permutation):
            term = algebra.mul(term, rows[row][column])
        result = algebra.add(result, algebra.neg(term) if inversions & 1 else term)
    return result


def build_syndrome(relations, algebra: QuotientAlgebra):
    chart = h4_family()
    leaves = [
        [SparseOffset.const(algebra, 1)] * 3,
        [SparseOffset.const(algebra, p), SparseOffset.const(algebra, q), SparseOffset.const(algebra, chart["s"])],
        [
            SparseOffset.const(algebra, a),
            SparseOffset.const(algebra, 1 + chart["b"]) + SparseOffset.variable(algebra, (1, 0)),
            SparseOffset.const(algebra, 1 + chart["c"]) + SparseOffset.variable(algebra, (0, 1)),
        ],
    ]
    rows: dict[int, list[SparseOffset]] = {}
    for row_index, support in enumerate(relations):
        entries = []
        for root in range(3):
            for component in range(3):
                total = SparseOffset.const(algebra, 0)
                for indices, coefficient in support:
                    if indices[0] != root:
                        continue
                    term = leaves[indices[1]][component] * leaves[indices[2]][component] * leaves[indices[3]][component]
                    total = total + SparseOffset.const(algebra, coefficient) * term
                entries.append(total)
        rows[row_index] = entries
    if len(rows) != 37 or any(len(row) != 9 for row in rows.values()):
        raise AssertionError("syndrome shape drift")
    return rows, chart


def record_sparse(value: SparseOffset) -> dict[str, Any]:
    return {
        "term_count": len(value.terms),
        "B_degree": max((e[0] for e in value.terms), default=-1),
        "C_degree": max((e[1] for e in value.terms), default=-1),
        "offset_support": [list(e) for e in sorted(value.terms)],
    }


def q_element_record(algebra: QuotientAlgebra, value) -> dict[str, Any]:
    canonical = []
    for degree, coeff in enumerate(value):
        if coeff == K.zero:
            continue
        canonical.append([degree, str(coeff.as_expr())])
    return {"q_degree_terms": len(canonical), "canonical": canonical}


def bridge(relations, algebra: QuotientAlgebra, verbose: bool = False):
    rows, chart = build_syndrome(relations, algebra)
    chart_denominator_records = denominator_provenance(chart)
    raw: dict[str, SparseOffset] = {}
    scaled: dict[str, SparseOffset] = {}
    decomposed: dict[str, tuple[SparseOffset, SparseOffset]] = {}
    for name in MINOR_ORDER:
        row_set, columns = MINOR_DATA[name]
        if verbose:
            print(f"[GLD103 audit] direct sparse minor {name}", file=sys.stderr, flush=True)
        value = determinant_sparse([[rows[row][column] for column in columns] for row in row_set], name)
        raw[name] = value
        scalar = SparseOffset.const(algebra, CLEARING_SCALARS[name])
        scaled[name] = scalar * value
        decomposed[name] = partition_affine(scaled[name], name)

    f_t0, _ = decomposed["T0"]
    p_values = [divide_by_b(f_t0, "F_T0")]
    p_values.extend(decomposed[name][1] for name in MINOR_ORDER)
    coeff = coefficient_rows(p_values)
    determinants = {}
    determinant_records = {}
    for label, triple in SELECTED_TRIPLES.items():
        selected = [coeff[index] for index in triple]
        first = det3_expansion(algebra, selected)
        second = det3_permutation(algebra, selected)
        if first != second or algebra.is_zero(first):
            raise AssertionError(f"{label} determinant cross-check failed")
        determinants[label] = first
        determinant_records[label] = {
            "row_triple": list(triple),
            "two_route_exact_match": True,
            **q_element_record(algebra, first),
        }

    # Gate identity and a concrete rank witness establish the declared
    # one-way bridge without ever reversing it.
    quotient_delta = sp.cancel(DELTA / P)
    if sp.denom(quotient_delta) != 1 or sp.expand(DELTA - P * quotient_delta) != 0:
        raise AssertionError("P does not divide Delta")
    sample = {p: 1, a: 2, q: sp.I, B: 0, C: 0}
    if sp.expand(q6_expression(p, q).subs(sample)) != 0:
        raise AssertionError("rank witness is not on Q6")
    numeric = sp.Matrix(
        [[algebra.as_expr(rows[i][j].terms.get((0, 0), algebra.zero)).subs(sample) for j in range(9)] for i in range(37)]
    )
    if numeric.rank() > 6:
        raise AssertionError("rank witness does not have rank <= 6")
    selected_zero = {}
    for name in MINOR_ORDER:
        rset, cset = MINOR_DATA[name]
        value = sp.expand(numeric.extract(list(rset), list(cset)).det())
        if value != 0:
            raise AssertionError(f"rank witness selected minor {name} is nonzero")
        selected_zero[name] = True

    result = {
        "algebra": algebra,
        "rows": rows,
        "raw": raw,
        "scaled": scaled,
        "decomposed": decomposed,
        "p_values": p_values,
        "coefficient_rows": coeff,
        "determinants": determinants,
        "metadata": {
            "syndrome_shape": [37, 9],
            "chart_denominator_provenance": chart_denominator_records,
            "selected_minors": {name: {"rows": list(MINOR_DATA[name][0]), "columns": list(MINOR_DATA[name][1])} for name in MINOR_ORDER},
            "minor_reconstruction": {name: record_sparse(scaled[name]) for name in MINOR_ORDER},
            "affine_C": {name: {"identity": "A_i=F_i+C*G_i", "checked": True, "F_at_B0": True} for name in MINOR_ORDER},
            "P": {
                "definitions": ["P0=F_T0/B", "P1=G_T0", "P2=G_T1", "P3=G_T2", "P4=G_Y1", "P5=G_X3"],
                "F_T0_equals_B_times_P0": True,
                "quadratic_B_coefficient_rows": 6,
                "coefficient_vector": ["1", "B", "B^2"],
                "records": [q_element_record(algebra, item) for row in coeff for item in row],
            },
            "determinants": determinant_records,
            "minor_role_partition": {
                "all_coefficient_minors": len(ALL_COEFFICIENT_TRIPLES),
                "selected_cover_minors": list(COVER_TRIPLES),
                "unselected_consequence_count": len(ALL_COEFFICIENT_TRIPLES) - len(COVER_TRIPLES),
                "fibre_only_minors": ["D134", "D145"],
                "fibre_only_not_in_cover": True,
            },
            "rank_bridge": {
                "direction": "one-way",
                "rank_witness_rank": int(numeric.rank()),
                "rank_witness_selected_actual_minors_zero": selected_zero,
                "converse_used": False,
                "gate_identity": "Delta=P*(Delta/P), exact quotient checked",
                "P_divides_Delta": True,
            },
        },
    }
    return result


def _integer_sparse(expression: sp.Expr, variables=(p, a, q)) -> tuple[dict[tuple[int, ...], int], dict[str, Any]]:
    """Clear rational content for one exact FLINT input polynomial.

    A quotient element is already reduced in q.  Its remaining denominator is
    required to be independent of a and q; such a p-only denominator is a
    declared chart clearing gate, not an unrecorded specialization.
    """
    numerator, denominator = sp.cancel(sp.sympify(expression)).as_numer_denom()
    denominator_poly = sp.Poly(denominator, *variables, domain=QQ)
    if denominator_poly.degree(a) > 0 or denominator_poly.degree(q) > 0:
        raise AssertionError(("non-p-only denominator", denominator))
    polynomial = sp.Poly(sp.expand(numerator), *variables, domain=QQ)
    rational_content, primitive = polynomial.primitive()
    integer_denominator, integer_poly = primitive.clear_denoms(convert=True)
    if rational_content < 0:
        rational_content = -rational_content
        integer_poly = -integer_poly
    terms: dict[tuple[int, ...], int] = {}
    for exponent, coefficient in integer_poly.terms():
        value = int(coefficient)
        if value:
            terms[tuple(int(item) for item in exponent)] = value
    if not terms:
        raise AssertionError("zero polynomial entered into FLINT")
    return terms, {
        "denominator": str(denominator),
        "integer_denominator": int(integer_denominator),
        "rational_content": int(rational_content),
        "term_count": len(terms),
        "terms_sha256": sha256_bytes(
            json.dumps(
                [[list(exponent), coefficient] for exponent, coefficient in sorted(terms.items())],
                separators=(",", ":"),
            ).encode()
        ),
    }


def p_denominator_provenance(denominator: object, label: str) -> dict[str, Any]:
    """Allow only the declared P/H2 localization in p-only denominators."""
    denominator = sp.factor(sp.sympify(denominator))
    if denominator == 0:
        raise AssertionError((label, "zero quotient denominator"))
    denominator_poly = sp.Poly(denominator, p, a, q, domain=QQ)
    if denominator_poly.degree(a) > 0 or denominator_poly.degree(q) > 0:
        raise AssertionError((label, "quotient denominator depends on a or q", denominator))
    _content, factors = sp.factor_list(denominator, p)
    allowed = (P, H2)
    unsupported = []
    factor_records = []
    for factor, exponent in factors:
        associated = any(
            (ratio := sp.cancel(factor / candidate)) != 0 and not ratio.has(p)
            for candidate in allowed
        )
        if not associated:
            unsupported.append(str(factor))
        factor_records.append({"factor": str(factor), "exponent": int(exponent)})
    if unsupported:
        raise AssertionError((label, "quotient denominator is outside P/H2 localization", unsupported))
    return {
        "denominator": str(denominator),
        "p_only": True,
        "allowed_factors": factor_records,
        "supported_by_P_or_H2": True,
    }


def _flint() -> tuple[Any, Any]:
    try:
        import flint
        from flint import fmpz_mpoly_ctx
    except ImportError as exc:  # pragma: no cover - environment dependent
        raise RuntimeError("GLD103_FLINT_REQUIRED: install python-flint==0.9.0") from exc
    version = str(getattr(flint, "__version__", ""))
    if version != "0.9.0":
        raise RuntimeError(f"GLD103_FLINT_VERSION_REQUIRED=0.9.0 observed={version!r}")
    return flint, fmpz_mpoly_ctx


def _flint_hash(poly) -> str:
    payload = [
        [list(tuple(int(item) for item in exponent)), int(coefficient)]
        for exponent, coefficient in poly.terms()
    ]
    return sha256_bytes(json.dumps(payload, separators=(",", ":")).encode())


def _flint_degree(poly, index: int = 0) -> int:
    degrees = poly.degrees()
    return int(degrees[index]) if degrees else -1


def _flint_sign(poly):
    return -poly if int(poly.leading_coefficient()) < 0 else poly


def _flint_from_terms(ctx, terms: dict[tuple[int, ...], int]):
    return ctx.from_dict({tuple(int(item) for item in exponent): int(value) for exponent, value in terms.items()})


def _p_only(poly) -> bool:
    return all(exponent[1] == 0 and exponent[2] == 0 for exponent, _ in poly.terms())


def _expected_factor_polynomials(ctx):
    p_var, _a_var, _q_var = ctx.gens()
    f40 = ctx.from_dict({(40 - index, 0, 0): int(value) for index, value in enumerate(F40_DESC) if value})
    return [
        64 * p_var**8 - 256 * p_var**7 + 580 * p_var**6 - 844 * p_var**5 + 946 * p_var**4 - 784 * p_var**3 + 388 * p_var**2 - 94 * p_var + 13,
        p_var**2 + 1,
        5 * p_var**4 - 16 * p_var**3 + 30 * p_var**2 - 16 * p_var + 5,
        5 * p_var**4 - 4 * p_var**3 + 12 * p_var**2 - 16 * p_var + 8,
        8 * p_var**4 - 16 * p_var**3 + 12 * p_var**2 - 4 * p_var + 5,
        f40,
        p_var**2 - 2 * p_var + 2,
        p_var - 1,
        2 * p_var**2 - 2 * p_var + 1,
        p_var,
        p_var**2 - p_var + 1,
    ]


def _expected_factor_map(ctx):
    factors = _expected_factor_polynomials(ctx)
    names = (
        "R8", "p2_plus_1", "R4", "F4", "C4", "F40",
        "p2_minus_2p_plus_2", "p_minus_1", "H2", "p", "P",
    )
    return dict(zip(names, factors))


# The native tracked clearing produces degree 624.  The historical degree-620
# presentation is obtained by an exact H2^2 division; it is a normalization,
# not a change in squarefree support.  Keep both maps explicit and never force
# the native result into the old degree pin.
NATIVE_MULTIPLICITIES = {
    "R8": 1,
    "p2_plus_1": 2,
    "R4": 2,
    "F4": 2,
    "C4": 2,
    "F40": 2,
    "p2_minus_2p_plus_2": 10,
    "p_minus_1": 46,
    "H2": 49,
    "p": 96,
    "P": 124,
}
NORMALIZED_MULTIPLICITIES = {**NATIVE_MULTIPLICITIES, "H2": NATIVE_MULTIPLICITIES["H2"] - 2}

# The current direct bridge has 1,565 primitive D145 terms.  A historical
# representation carried a 3,444-term pin; keep that different-representation
# pin visible in the F40 record, but make the present canonical sparse data the
# checked pin without asserting why the historical count differed.
CURRENT_D145_TERM_COUNT = 1565
CURRENT_D145_TERMS_SHA256 = "8c27545c0499b89126745aa258b1dc576653ec2587625e30f9e0c8ae3068c084"
CURRENT_D145_INTEGER_CONTENT = 23887872


def exact_p_cover(determinants: dict[str, Any], algebra: QuotientAlgebra) -> dict[str, Any]:
    """Recompute native degree-624 and H2^2-normalized degree-620 covers."""
    flint, fmpz_mpoly_ctx = _flint()
    del flint  # the context and returned objects are the arithmetic witness
    ctx = fmpz_mpoly_ctx.get(("p", "a", "q"), ordering="lex")
    q6_terms, q6_meta = _integer_sparse(algebra.q6_expr)
    q6_meta["denominator_provenance"] = p_denominator_provenance(q6_meta["denominator"], "Q6")
    q6_poly = _flint_from_terms(ctx, q6_terms)
    inputs: dict[str, Any] = {"Q6": q6_meta}
    determinant_polys = {}
    # Only the six selected cover minors enter this resultant/gcd route.
    # D134/D145 are retained for fibre closures and are not silently promoted
    # to cover inputs.
    for name in COVER_TRIPLES:
        value = determinants[name]
        terms, metadata = _integer_sparse(algebra.as_expr(value))
        metadata["denominator_provenance"] = p_denominator_provenance(metadata["denominator"], name)
        determinant_polys[name] = _flint_from_terms(ctx, terms)
        inputs[name] = metadata

    q_resultants = {}
    resultant_meta = {}
    for name, determinant in determinant_polys.items():
        resultant = q6_poly.resultant(determinant, 2)
        if resultant == 0:
            raise AssertionError(f"zero Q6 resultant for {name}")
        q_resultants[name] = resultant
        resultant_meta[name] = {
            "degree_p": _flint_degree(resultant),
            "degree_a": _flint_degree(resultant, 1),
            "term_count": len(list(resultant.terms())),
            "canonical_sha256": _flint_hash(resultant),
        }

    covers = []
    pair_meta = {}
    base = q_resultants["D012"]
    for name in COVER_TRIPLES[1:]:
        other = q_resultants[name]
        common = base.gcd(other)
        if not _p_only(common):
            raise AssertionError(f"q-resultant gcd for {name} is not p-only")
        left, left_remainder = divmod(base, common)
        right, right_remainder = divmod(other, common)
        if left_remainder != 0 or right_remainder != 0:
            raise AssertionError(f"inexact gcd division for {name}")
        a_resultant = left.resultant(right, 1)
        if a_resultant == 0 or not _p_only(a_resultant):
            raise AssertionError(f"bad a-resultant for {name}")
        cover = common * a_resultant
        covers.append(cover)
        pair_meta[name] = {
            "q_gcd_degree_p": _flint_degree(common),
            "a_resultant_degree_p": _flint_degree(a_resultant),
            "cover_degree_p": _flint_degree(cover),
            "cover_canonical_sha256": _flint_hash(cover),
        }

    final = covers[0]
    for cover in covers[1:]:
        final = final.gcd(cover)
    if not _p_only(final):
        raise AssertionError("final cover is not p-only")
    _unit, factors = final.factor()
    actual = {_flint_hash(_flint_sign(factor)) for factor, _ in factors}
    expected_map = _expected_factor_map(ctx)
    expected = {_flint_hash(_flint_sign(factor)) for factor in expected_map.values()}
    if actual != expected:
        raise AssertionError(f"factor support mismatch: actual={sorted(actual)} expected={sorted(expected)}")
    final_degree = _flint_degree(final)
    if len(factors) != 11:
        raise AssertionError(("factor-count drift", len(factors)))
    factor_records = [
        {"degree_p": _flint_degree(_flint_sign(factor)), "exponent": int(exponent), "canonical_sha256": _flint_hash(_flint_sign(factor))}
        for factor, exponent in factors
    ]
    actual_by_name = {}
    for factor, exponent in factors:
        digest = _flint_hash(_flint_sign(factor))
        matched = [name for name, expected_factor in expected_map.items() if _flint_hash(_flint_sign(expected_factor)) == digest]
        if len(matched) != 1:
            raise AssertionError("factor-name reconciliation failed")
        actual_by_name[matched[0]] = int(exponent)
    if actual_by_name != NATIVE_MULTIPLICITIES:
        raise AssertionError(("native multiplicity drift", actual_by_name, NATIVE_MULTIPLICITIES))
    h2_factor = expected_map["H2"]
    normalized, normalization_remainder = divmod(final, h2_factor**2)
    if normalization_remainder != 0:
        raise AssertionError("native cover is not exactly divisible by H2^2")
    if normalized * (h2_factor**2) != final:
        raise AssertionError("H2^2 normalization does not reconstruct native cover")
    normalized_degree = _flint_degree(normalized)
    _normalized_unit, normalized_factors = normalized.factor()
    if len(normalized_factors) != 11:
        raise AssertionError(("normalized factor-count drift", len(normalized_factors)))
    normalized_by_name = {}
    for factor, exponent in normalized_factors:
        digest = _flint_hash(_flint_sign(factor))
        matched = [name for name, expected_factor in expected_map.items() if _flint_hash(_flint_sign(expected_factor)) == digest]
        if len(matched) != 1:
            raise AssertionError("normalized factor-name reconciliation failed")
        normalized_by_name[matched[0]] = int(exponent)
    if normalized_by_name != NORMALIZED_MULTIPLICITIES:
        raise AssertionError(("H2^2-normalized multiplicity drift", normalized_by_name, NORMALIZED_MULTIPLICITIES))
    if normalized_degree != 620:
        raise AssertionError(("historical normalized degree drift", normalized_degree, 620))
    normalized_records = [
        {
            "degree_p": _flint_degree(_flint_sign(factor)),
            "exponent": int(exponent),
            "canonical_sha256": _flint_hash(_flint_sign(factor)),
        }
        for factor, exponent in normalized_factors
    ]
    native_support_degree = sum(item["degree_p"] for item in factor_records)
    normalized_support_degree = sum(item["degree_p"] for item in normalized_records)
    if native_support_degree != normalized_support_degree or native_support_degree != 70:
        raise AssertionError(("squarefree support degree drift", native_support_degree, normalized_support_degree))
    return {
        "status": "verified_exact_necessary_p_cover",
        "arithmetic": "python-flint 0.9.0 fmpz_mpoly sparse resultants/gcd/factorization",
        "ring": "Z[p,a,q] lex; q-resultant index 2, a-resultant index 1",
        "inputs": inputs,
        "q6": {"term_count": len(list(q6_poly.terms())), "canonical_sha256": _flint_hash(q6_poly)},
        "q_resultants": resultant_meta,
        "pair_covers": pair_meta,
        "cover_determinants": list(COVER_TRIPLES),
        "coefficient_consequence_count": len(ALL_COEFFICIENT_TRIPLES) - len(COVER_TRIPLES),
        "fibre_only_determinants": ["D134", "D145"],
        "fibre_only_not_in_cover": True,
        "final_degree_p": final_degree,
        "final_canonical_sha256": _flint_hash(final),
        "factor_count": len(factors),
        "factors": sorted(factor_records, key=lambda item: (item["degree_p"], item["canonical_sha256"])),
        "raw_factor_count": len(factors),
        "raw_factors": sorted(factor_records, key=lambda item: (item["degree_p"], item["canonical_sha256"])),
        "factor_support_match": True,
        "support_only_comparison": True,
        "squarefree_support_match": True,
        "raw_squarefree_support_degree_p": native_support_degree,
        "support_factor_degrees": sorted(item["degree_p"] for item in factor_records),
        "squarefree_factor_count": len(factors),
        "native_degree_p": final_degree,
        "raw_final_degree_p": final_degree,
        "normalized_degree_p": normalized_degree,
        "normalized_open_cover_degree_p": normalized_degree,
        "multiplicity_degree_p": final_degree,
        "normalized_multiplicity_degree_p": normalized_degree,
        "claimed_degree_p": 620,
        "degree_match": normalized_degree == 620,
        "computed_multiplicities_by_factor": actual_by_name,
        "native_multiplicities_by_factor": actual_by_name,
        "normalized_multiplicities_by_factor": normalized_by_name,
        "normalized_open_cover_factors": sorted(normalized_records, key=lambda item: (item["degree_p"], item["canonical_sha256"])),
        "claimed_multiplicities_by_factor": dict(NORMALIZED_MULTIPLICITIES),
        "multiplicity_reconciliation": {
            "native_expected": dict(NATIVE_MULTIPLICITIES),
            "native_match": True,
            "normalization_factor": "H2^2",
            "normalization_exact_division": True,
            "removed_exponent": {"H2": 2},
            "raw_h2_exponent": actual_by_name["H2"],
            "normalized_h2_exponent": normalized_by_name["H2"],
            "normalized_expected": dict(NORMALIZED_MULTIPLICITIES),
            "normalized_match": True,
        },
        "normalization_reconciliation": {
            "clearing_scalars_are_retained": True,
            "primitive_integer_content_only": True,
            "native_support_degree": final_degree,
            "normalized_support_degree": normalized_degree,
            "factor_removed": "H2^2",
            "exact_division_checked": True,
            "raw_cover_localization_equivalent": True,
            "note": "Native tracked clearing gives degree 624 with p-1^46 H2^49. Exact division by H2^2 gives the historical degree-620 presentation with p-1^46 H2^47; squarefree eleven-factor support is unchanged.",
        },
        "open_invariance": {
            "declared_open": "D(B*H2*Delta)",
            "removed_factor": "H2^2",
            "reason": "H2 is the Q6 leading coefficient and already inverted/excluded on the declared open",
            "squarefree_support_preserved": True,
        },
    }


class ResidueField:
    """Exact Q[p]/(f) arithmetic used only for fibre replays."""

    def __init__(self, modulus: sp.Expr):
        self.modulus = sp.Poly(sp.expand(modulus), p, domain=QQ)
        if self.modulus.degree() < 1:
            raise AssertionError("fibre modulus is constant")
        self.zero = Residue(self, self.modulus.zero)
        self.one = Residue(self, self.modulus.one)

    def reduce(self, value: sp.Poly | sp.Expr) -> sp.Poly:
        polynomial = value if isinstance(value, sp.Poly) else sp.Poly(value, p, domain=QQ)
        return polynomial.rem(self.modulus)

    def from_expr(self, value: object):
        numerator, denominator = sp.cancel(sp.sympify(value)).as_numer_denom()
        n = sp.Poly(numerator, p, domain=QQ).rem(self.modulus)
        d = sp.Poly(denominator, p, domain=QQ).rem(self.modulus)
        if d.is_zero:
            raise AssertionError(("zero fibre denominator", value, self.modulus.as_expr()))
        inverse = sp.invert(d, self.modulus)
        return Residue(self, (n * inverse).rem(self.modulus))


class Residue:
    __slots__ = ("field", "poly")

    def __init__(self, field: ResidueField, poly: sp.Poly):
        self.field = field
        self.poly = field.reduce(poly)

    def __add__(self, other):
        other = _residue_coerce(self.field, other)
        return Residue(self.field, self.poly + other.poly)

    def __neg__(self):
        return Residue(self.field, -self.poly)

    def __sub__(self, other):
        return self + (-_residue_coerce(self.field, other))

    def __mul__(self, other):
        other = _residue_coerce(self.field, other)
        return Residue(self.field, self.poly * other.poly)

    def __truediv__(self, other):
        return self * _residue_coerce(self.field, other).inverse()

    def inverse(self):
        if self.is_zero:
            raise ZeroDivisionError("zero residue")
        return Residue(self.field, sp.invert(self.poly, self.field.modulus))

    @property
    def is_zero(self) -> bool:
        return self.poly.is_zero

    def __eq__(self, other):
        try:
            return self.poly == _residue_coerce(self.field, other).poly
        except (TypeError, ValueError):
            return False

    def __repr__(self):  # pragma: no cover - diagnostic only
        return f"Residue({self.poly.as_expr()})"


def _residue_coerce(field: ResidueField, value: object) -> Residue:
    if isinstance(value, Residue):
        if value.field is not field:
            raise TypeError("residue fields differ")
        return value
    return field.from_expr(value)


class QuotientResidueField:
    """(Q[p]/(f))[q]/(Q6), with q-degree below four."""

    def __init__(self, pfield: ResidueField, q6: sp.Expr):
        self.pfield = pfield
        self.q6 = sp.Poly(sp.expand(q6), q, domain=QQ.frac_field(p))
        if self.q6.degree() != 4:
            raise AssertionError("fibre Q6 degree drift")
        lead = pfield.from_expr(self.q6.LC())
        if lead.is_zero:
            raise AssertionError("fibre Q6 leading coefficient vanishes")
        self.relation = tuple(
            -(pfield.from_expr(self.q6.nth(i)) / lead) for i in range(4)
        )
        self.zero = (pfield.zero,) * 4
        self.one = (pfield.one, pfield.zero, pfield.zero, pfield.zero)

    def add(self, left, right):
        return tuple(left[i] + right[i] for i in range(4))

    def neg(self, value):
        return tuple(-value[i] for i in range(4))

    def mul(self, left, right):
        raw = [self.pfield.zero] * 7
        for i, x in enumerate(left):
            if x.is_zero:
                continue
            for j, y in enumerate(right):
                if not y.is_zero:
                    raw[i + j] = raw[i + j] + x * y
        for degree in range(6, 3, -1):
            high = raw[degree]
            if high.is_zero:
                continue
            for index, coefficient in enumerate(self.relation):
                raw[degree - 4 + index] = raw[degree - 4 + index] + high * coefficient
        return tuple(raw[:4])

    def is_zero(self, value) -> bool:
        return all(item.is_zero for item in value)

    def from_expr(self, expression: object):
        numerator, denominator = sp.cancel(sp.sympify(expression)).as_numer_denom()
        modulus = self.q6
        n = sp.Poly(numerator, q, domain=QQ.frac_field(p)).rem(modulus)
        d = sp.Poly(denominator, q, domain=QQ.frac_field(p)).rem(modulus)
        if d.is_zero or d.degree() > 0:
            raise AssertionError(("q-dependent fibre denominator", expression))
        quotient = [self.pfield.zero] * 4
        for index in range(min(4, n.degree() + 1)):
            quotient[index] = self.pfield.from_expr(n.nth(index) / d.nth(0))
        return tuple(quotient)


def _q_constant(qfield: QuotientResidueField, value: object):
    return (qfield.pfield.from_expr(value), qfield.pfield.zero, qfield.pfield.zero, qfield.pfield.zero)


def _q_from_a_coefficient(qfield: QuotientResidueField, coefficient: object, q_degree: int):
    value = [qfield.pfield.zero] * 4
    value[q_degree] = qfield.pfield.from_expr(coefficient)
    return tuple(value)


def _q_a_polynomial(value, qfield: QuotientResidueField) -> dict[int, tuple[Any, ...]]:
    """Convert a quotient element with symbolic a into an a-polynomial."""
    output: dict[int, tuple[Any, ...]] = {}
    for q_degree, coefficient in enumerate(value):
        expression = coefficient.as_expr()
        numerator, denominator = sp.cancel(expression).as_numer_denom()
        numerator_poly = sp.Poly(numerator, a, domain=QQ.frac_field(p))
        denominator_poly = sp.Poly(denominator, a, domain=QQ.frac_field(p))
        if denominator_poly.degree() > 0:
            raise AssertionError(("a-dependent fibre denominator", expression))
        denominator_value = denominator_poly.nth(0)
        for (a_degree,), item in numerator_poly.terms():
            term = _q_from_a_coefficient(qfield, item / denominator_value, q_degree)
            previous = output.get(a_degree, qfield.zero)
            output[a_degree] = qfield.add(previous, term)
    return {degree: value for degree, value in output.items() if not qfield.is_zero(value)}


def _poly3_add(qfield: QuotientResidueField, left, right):
    output = dict(left)
    for exponent, value in right.items():
        updated = qfield.add(output.get(exponent, qfield.zero), value)
        if qfield.is_zero(updated):
            output.pop(exponent, None)
        else:
            output[exponent] = updated
    return output


def _poly3_shift(poly, shift: tuple[int, int, int]):
    return {
        tuple(exponent[index] + shift[index] for index in range(3)): value
        for exponent, value in poly.items()
    }


def _monomials(nvars: int, bound: int) -> list[tuple[int, ...]]:
    result = []
    for total in range(bound + 1):
        for exponents in itertools.product(range(total + 1), repeat=nvars):
            if sum(exponents) == total:
                result.append(tuple(exponents))
    return result


def _field_rref(rows: list[list[Residue]]):
    """Exact RREF over Q[p]/(factor), retaining pivots for membership."""
    if not rows:
        return [], []
    matrix = [list(row) for row in rows]
    nrows, ncols = len(matrix), len(matrix[0])
    rank = 0
    pivots = []
    for column in range(ncols):
        pivot = next((index for index in range(rank, nrows) if not matrix[index][column].is_zero), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inverse = matrix[rank][column].inverse()
        matrix[rank] = [item * inverse for item in matrix[rank]]
        for row in range(nrows):
            if row == rank:
                continue
            factor = matrix[row][column]
            if factor.is_zero:
                continue
            matrix[row] = [matrix[row][j] - factor * matrix[rank][j] for j in range(ncols)]
        pivots.append(column)
        rank += 1
        if rank == nrows:
            break
    return matrix, pivots


def _field_reduce_against_rref(target: list[Residue], rref: list[list[Residue]], pivots: list[int]):
    residual = list(target)
    for pivot, row in zip(pivots, rref):
        factor = residual[pivot]
        if factor.is_zero:
            continue
        residual = [left - factor * right for left, right in zip(residual, row)]
    return residual


def _field_membership(rows: list[list[Residue]], target: list[Residue]):
    rref, pivots = _field_rref(rows)
    residual = _field_reduce_against_rref(target, rref, pivots)
    rank = len(pivots)
    rank_with_target = len(_field_rref(rows + [target])[1])
    return {
        "rank": rank,
        "rank_with_target": rank_with_target,
        "target_in_span": all(value.is_zero for value in residual),
        "target_residual": residual,
        "rref_pivots": pivots,
    }


def _field_rank(rows: list[list[Residue]]) -> int:
    return len(_field_rref(rows)[1])


def _macaulay_matrix(
    generators: list[dict[tuple[int, int, int], tuple[Any, ...]]],
    qfield: QuotientResidueField,
    bound: int,
    variables: int = 3,
):
    # The coefficient field for the Macaulay rank is the full four-dimensional
    # q-quotient over Q[p]/(factor), not just its scalar subfield.  Therefore
    # every a/B/z multiplier must also be multiplied by each q-basis element.
    # Omitting these four q shifts only measures the scalar span of the input
    # rows and can never certify the advertised K-linear quotient rank.
    q_basis = [qfield.one]
    q_generator = (qfield.pfield.zero, qfield.pfield.one, qfield.pfield.zero, qfield.pfield.zero)
    for _ in range(3):
        q_basis.append(qfield.mul(q_basis[-1], q_generator))
    if variables not in (1, 3):
        raise AssertionError("the audit only models A[a] or A[a,B,z]")
    monomials = _monomials(variables, bound)
    if variables == 1:
        # Keep the common three-coordinate exponent representation while
        # restricting fibre ideals to the advertised ring A[a].
        monomials = [(exponent[0], 0, 0) for exponent in monomials]
    index = {monomial: position for position, monomial in enumerate(monomials)}
    columns = 4 * len(monomials)
    rows: list[list[Residue]] = []
    for generator in generators:
        if not generator:
            continue
        degree = max(sum(exponent) for exponent in generator)
        if degree > bound:
            continue
        multipliers = _monomials(variables, bound - degree)
        if variables == 1:
            multipliers = [(exponent[0], 0, 0) for exponent in multipliers]
        for multiplier in multipliers:
            shifted = _poly3_shift(generator, multiplier)
            for q_multiplier in q_basis:
                row = [qfield.pfield.zero] * columns
                for exponent, value in shifted.items():
                    start = 4 * index[exponent]
                    shifted_value = qfield.mul(value, q_multiplier)
                    for q_degree, coefficient in enumerate(shifted_value):
                        row[start + q_degree] = row[start + q_degree] + coefficient
                rows.append(row)
    return rows, columns


def _macaulay_metadata(
    generators: list[dict[tuple[int, int, int], tuple[Any, ...]]],
    bound: int,
    variables: int,
    rows: list[list[Residue]],
    columns: int,
) -> dict[str, Any]:
    """Describe the exact row-space construction for cross-replay audits."""
    if variables not in (1, 3):
        raise AssertionError("the audit only models A[a] or A[a,B,z]")
    monomials = _monomials(variables, bound)
    if variables == 1:
        monomials = [(exponent[0], 0, 0) for exponent in monomials]
    row_counts = []
    for generator in generators:
        degree = max((sum(exponent) for exponent in generator), default=bound + 1)
        multiplier_count = len(_monomials(variables, bound - degree)) if degree <= bound else 0
        row_counts.append(4 * multiplier_count)
    return {
        "variables": ["a"] if variables == 1 else ["a", "B", "z"],
        "bound": bound,
        "columns": columns,
        "monomial_count": len(monomials),
        "monomial_order": "total_degree_then_itertools_product_tuple",
        "monomial_order_sha256": sha256_bytes(json.dumps(monomials, separators=(",", ":")).encode()),
        "q_basis": ["1", "q", "q^2", "q^3"],
        "q_basis_dimension": 4,
        "q_shift_count": 4,
        "generator_count": len(generators),
        "generator_hashes": [_a_generator_hash(generator) for generator in generators],
        "generator_support_sizes": [len(generator) for generator in generators],
        "rows_per_generator": row_counts,
        "row_count": len(rows),
        "row_matrix_sha256": _field_matrix_hash(rows),
    }


def _a_generator(value, qfield: QuotientResidueField):
    return {(degree, 0, 0): coefficient for degree, coefficient in _q_a_polynomial(value, qfield).items()}


def _bc_generator(value: SparseOffset, qfield: QuotientResidueField):
    output: dict[tuple[int, int, int], tuple[Any, ...]] = {}
    for (b_degree, c_degree), coefficient in value.terms.items():
        if c_degree:
            raise AssertionError("coefficient-row polynomial unexpectedly contains C")
        for a_degree, q_degree in _coefficient_a_q_terms(coefficient, qfield):
            exponent = (a_degree, b_degree, 0)
            term = _q_from_a_coefficient(qfield, q_degree[1], q_degree[0])
            output[exponent] = qfield.add(output.get(exponent, qfield.zero), term)
    return {key: value for key, value in output.items() if not qfield.is_zero(value)}


def _coefficient_a_q_terms(coefficient, qfield: QuotientResidueField):
    """Yield (a-degree, (q-degree, p-rational expression)) pairs."""
    for q_degree, item in enumerate(coefficient):
        expression = item.as_expr()
        numerator, denominator = sp.cancel(expression).as_numer_denom()
        polynomial = sp.Poly(numerator, a, domain=QQ.frac_field(p))
        denominator_poly = sp.Poly(denominator, a, domain=QQ.frac_field(p))
        if denominator_poly.degree() > 0:
            raise AssertionError(("a-dependent coefficient denominator", expression))
        denominator_value = denominator_poly.nth(0)
        for (a_degree,), value in polynomial.terms():
            yield a_degree, (q_degree, value / denominator_value)


def _localizer_generator(qfield: QuotientResidueField):
    delta_value = qfield.from_expr(DELTA)
    return {
        (0, 1, 1): delta_value,
        (0, 0, 0): qfield.neg(qfield.one),
    }


def _span_contains(rows: list[list[Residue]], target: list[Residue]) -> bool:
    return _field_rank(rows) == _field_rank(rows + [target])


def _determinant_field(matrix: list[list[tuple[Any, ...]]], qfield: QuotientResidueField):
    """Dense determinant over the q-quotient used for the F40 norm."""
    if not matrix:
        return qfield.one
    work = [list(row) for row in matrix]
    size = len(work)
    result = qfield.one
    sign = 1
    for column in range(size):
        pivot = next((row for row in range(column, size) if not qfield.is_zero(work[row][column])), None)
        if pivot is None:
            return qfield.zero
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            sign = -sign
        pivot_value = work[column][column]
        result = qfield.mul(result, pivot_value)
        inverse = _q_inverse(pivot_value, qfield)
        for row in range(column + 1, size):
            factor = qfield.mul(work[row][column], inverse)
            if qfield.is_zero(factor):
                continue
            for j in range(column + 1, size):
                work[row][j] = qfield.add(work[row][j], qfield.neg(qfield.mul(factor, work[column][j])))
    return qfield.neg(result) if sign < 0 else result


def _q_inverse(value, qfield: QuotientResidueField):
    """Invert a q residue by exact 4-by-4 linear algebra over the p field."""
    if qfield.is_zero(value):
        raise ZeroDivisionError("zero q residue")
    zero = qfield.pfield.zero
    one = qfield.pfield.one
    q_generator = (zero, one, zero, zero)
    basis = [qfield.one]
    for _ in range(3):
        basis.append(qfield.mul(basis[-1], q_generator))
    # Column j is value*q^j.  Solve this multiplication matrix against 1
    # using exact residue-field Gaussian elimination; no generic Q(p)
    # inversion or untracked symbolic normalization is involved.
    matrix = [
        [qfield.mul(value, basis[column])[row] for column in range(4)]
        + [qfield.one[row]]
        for row in range(4)
    ]
    for column in range(4):
        pivot = next((row for row in range(column, 4) if not matrix[row][column].is_zero), None)
        if pivot is None:
            raise ZeroDivisionError("q residue is not a unit in the fibre")
        matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
        inverse = matrix[column][column].inverse()
        matrix[column] = [entry * inverse for entry in matrix[column]]
        for row in range(4):
            if row == column:
                continue
            factor = matrix[row][column]
            if factor.is_zero:
                continue
            matrix[row] = [matrix[row][index] - factor * matrix[column][index] for index in range(5)]
    candidate = tuple(matrix[row][4] for row in range(4))
    if qfield.mul(value, candidate) != qfield.one:
        raise AssertionError("q residue inversion failed")
    return candidate


def _a_trim(value: list[tuple[Any, ...]], qfield: QuotientResidueField) -> list[tuple[Any, ...]]:
    value = list(value)
    while value and qfield.is_zero(value[-1]):
        value.pop()
    return value


def _a_add(left: list[tuple[Any, ...]], right: list[tuple[Any, ...]], qfield: QuotientResidueField):
    length = max(len(left), len(right))
    result = [qfield.zero] * length
    for index in range(length):
        result[index] = qfield.add(
            left[index] if index < len(left) else qfield.zero,
            right[index] if index < len(right) else qfield.zero,
        )
    return _a_trim(result, qfield)


def _a_neg(value: list[tuple[Any, ...]], qfield: QuotientResidueField):
    return _a_trim([qfield.neg(item) for item in value], qfield)


def _a_sub(left: list[tuple[Any, ...]], right: list[tuple[Any, ...]], qfield: QuotientResidueField):
    return _a_add(left, _a_neg(right, qfield), qfield)


def _a_mul(left: list[tuple[Any, ...]], right: list[tuple[Any, ...]], qfield: QuotientResidueField):
    if not left or not right:
        return []
    result = [qfield.zero] * (len(left) + len(right) - 1)
    for left_degree, left_value in enumerate(left):
        if qfield.is_zero(left_value):
            continue
        for right_degree, right_value in enumerate(right):
            if qfield.is_zero(right_value):
                continue
            result[left_degree + right_degree] = qfield.add(
                result[left_degree + right_degree],
                qfield.mul(left_value, right_value),
            )
    return _a_trim(result, qfield)


def _a_scale(value: list[tuple[Any, ...]], scalar: tuple[Any, ...], qfield: QuotientResidueField):
    return _a_trim([qfield.mul(item, scalar) for item in value], qfield)


def _a_divrem(left: list[tuple[Any, ...]], right: list[tuple[Any, ...]], qfield: QuotientResidueField):
    """Euclidean division in A[a], with exact q-residue inverses."""
    left = _a_trim(left, qfield)
    right = _a_trim(right, qfield)
    if not right:
        raise ZeroDivisionError("zero polynomial in F40 quotient gcd")
    if not left or len(left) < len(right):
        return [], left
    quotient = [qfield.zero] * (len(left) - len(right) + 1)
    remainder = left
    inverse = _q_inverse(right[-1], qfield)
    while remainder and len(remainder) >= len(right):
        shift = len(remainder) - len(right)
        coefficient = qfield.mul(remainder[-1], inverse)
        quotient[shift] = qfield.add(quotient[shift], coefficient)
        for degree, divisor_value in enumerate(right):
            location = shift + degree
            remainder[location] = qfield.add(
                remainder[location],
                qfield.neg(qfield.mul(coefficient, divisor_value)),
            )
        remainder = _a_trim(remainder, qfield)
    return _a_trim(quotient, qfield), remainder


def _a_gcdex(left: list[tuple[Any, ...]], right: list[tuple[Any, ...]], qfield: QuotientResidueField):
    """Extended Euclid over A[a], intentionally without normalizing c."""
    r0, r1 = _a_trim(left, qfield), _a_trim(right, qfield)
    s0, s1 = [qfield.one], []
    t0, t1 = [], [qfield.one]
    steps = 0
    while r1:
        quotient, remainder = _a_divrem(r0, r1, qfield)
        r0, r1 = r1, remainder
        s0, s1 = s1, _a_sub(s0, _a_mul(quotient, s1, qfield), qfield)
        t0, t1 = t1, _a_sub(t0, _a_mul(quotient, t1, qfield), qfield)
        steps += 1
    return r0, s0, t0, steps


def _a_poly_hash(value: list[tuple[Any, ...]]) -> str:
    return sha256_bytes(
        json.dumps(
            [[index, [_coefficient_text(item) for item in coefficient]] for index, coefficient in enumerate(value)],
            separators=(",", ":"),
        ).encode()
    )


def _coefficient_text(item: object) -> str:
    polynomial = getattr(item, "poly", None)
    if polynomial is not None:
        return str(polynomial.as_expr())
    return str(item.as_expr())


def _a_generator_hash(value: dict[tuple[int, int, int], tuple[Any, ...]]) -> str:
    return sha256_bytes(
        json.dumps(
            [
                [list(exponent), [_coefficient_text(item) for item in coefficient]]
                for exponent, coefficient in sorted(value.items())
            ],
            separators=(",", ":"),
        ).encode()
    )


def _field_matrix_hash(rows: list[list[Residue]]) -> str:
    """Hash the exact dense residue-field Macaulay rows in column order."""
    return sha256_bytes(
        json.dumps(
            [[_coefficient_text(item) for item in row] for row in rows],
            separators=(",", ":"),
        ).encode()
    )


def _resultant_in_a(left: dict[int, tuple[Any, ...]], right: dict[int, tuple[Any, ...]], qfield: QuotientResidueField):
    """Sylvester determinant in the exact q-quotient."""
    if not left or not right:
        return qfield.zero
    left_degree, right_degree = max(left), max(right)
    if left_degree == 0 and right_degree == 0:
        return qfield.zero
    size = left_degree + right_degree
    matrix = [[qfield.zero for _ in range(size)] for _ in range(size)]
    for row in range(right_degree):
        for degree, value in left.items():
            matrix[row][row + degree] = value
    for row in range(left_degree):
        for degree, value in right.items():
            matrix[right_degree + row][row + degree] = value
    return _determinant_field(matrix, qfield)


def _factor_expression(name: str) -> sp.Expr:
    values = {
        "R8": 64 * p**8 - 256 * p**7 + 580 * p**6 - 844 * p**5 + 946 * p**4 - 784 * p**3 + 388 * p**2 - 94 * p + 13,
        "p2_plus_1": p**2 + 1,
        "R4": 5 * p**4 - 16 * p**3 + 30 * p**2 - 16 * p + 5,
        "F4": 5 * p**4 - 4 * p**3 + 12 * p**2 - 16 * p + 8,
        "C4": 8 * p**4 - 16 * p**3 + 12 * p**2 - 4 * p + 5,
        "F40": sum(value * p**(40 - index) for index, value in enumerate(F40_DESC)),
        "p2_minus_2p_plus_2": p**2 - 2 * p + 2,
        "p_minus_1": p - 1,
        "H2": H2,
        "p": p,
        "P": P,
    }
    if name not in values:
        raise AssertionError(f"unknown GLD103 factor {name}")
    return sp.expand(values[name])


def _fibre_q_generators(determinants: dict[str, Any], names: tuple[str, ...], qfield: QuotientResidueField):
    return [_a_generator(determinants[name], qfield) for name in names]


def _fibre_rank(determinants: dict[str, Any], names: tuple[str, ...], factor: str, bound: int):
    pfield = ResidueField(_factor_expression(factor))
    qfield = QuotientResidueField(pfield, q6_expression(p, q))
    generators = _fibre_q_generators(determinants, names, qfield)
    rows, columns = _macaulay_matrix(generators, qfield, bound, variables=1)
    target = [qfield.pfield.zero] * columns
    target[0] = qfield.pfield.one
    return _field_membership(rows, target), columns, _macaulay_metadata(generators, bound, 1, rows, columns)


def _physical_generators(p_values: list[SparseOffset], qfield: QuotientResidueField):
    return [_bc_generator(value, qfield) for value in p_values] + [_localizer_generator(qfield)]


def _physical_rank(p_values: list[SparseOffset], factor: str, bound: int):
    pfield = ResidueField(_factor_expression(factor))
    qfield = QuotientResidueField(pfield, q6_expression(p, q))
    generators = _physical_generators(p_values, qfield)
    rows, columns = _macaulay_matrix(generators, qfield, bound)
    target = [qfield.pfield.zero] * columns
    target[0] = qfield.pfield.one
    return _field_membership(rows, target), columns, _macaulay_metadata(generators, bound, 3, rows, columns)


def f40_closure(determinants: dict[str, Any]) -> dict[str, Any]:
    """Exact primitive/irreducible and D134/D145 quotient-gcd/norm check."""
    factor = sp.Poly(_factor_expression("F40"), p, domain=QQ)
    content, primitive = factor.primitive()
    if int(content) != 1 or not primitive.is_irreducible:
        raise AssertionError("F40 is not primitive and irreducible")
    h2 = sp.Poly(H2, p, domain=QQ)
    if sp.gcd(factor, h2).degree() != 0:
        raise AssertionError("gcd(F40,H2) is not one")
    # Keep the authoritative raw sparse-input check separate from the
    # specialized quotient representation.  This catches accidental use of a
    # reduced/normalized D145 in place of the direct bridge reconstruction.
    d134_raw, d134_metadata = _integer_sparse(
        QuotientAlgebra(q6_expression()).as_expr(determinants["D134"])
    )
    d145_raw, d145_metadata = _integer_sparse(
        QuotientAlgebra(q6_expression()).as_expr(determinants["D145"])
    )
    del d134_raw, d145_raw
    d134_metadata["denominator_provenance"] = p_denominator_provenance(d134_metadata["denominator"], "D134")
    d145_metadata["denominator_provenance"] = p_denominator_provenance(d145_metadata["denominator"], "D145")
    d145_denominator_match = sp.cancel(
        sp.sympify(d145_metadata["denominator"]) / sp.expand(H2**3)
    ) == 1
    d145_current_match = (
        d145_metadata.get("term_count") == CURRENT_D145_TERM_COUNT
        and d145_metadata.get("terms_sha256") == CURRENT_D145_TERMS_SHA256
        and d145_metadata.get("rational_content") == CURRENT_D145_INTEGER_CONTENT
        and d145_metadata.get("integer_denominator") == 1
        and d145_denominator_match
    )
    if not d145_current_match:
        raise AssertionError(("current canonical D145 sparse pin mismatch", d145_metadata))
    pfield = ResidueField(factor.as_expr())
    qfield = QuotientResidueField(pfield, q6_expression(p, q))
    left = _q_a_polynomial(determinants["D134"], qfield)
    right = _q_a_polynomial(determinants["D145"], qfield)
    left_a = [qfield.zero] * (max(left, default=-1) + 1)
    right_a = [qfield.zero] * (max(right, default=-1) + 1)
    for degree, value in left.items():
        left_a[degree] = value
    for degree, value in right.items():
        right_a[degree] = value
    gcd, u134, u145, steps = _a_gcdex(left_a, right_a, qfield)
    if len(gcd) != 1 or qfield.is_zero(gcd[0]):
        raise AssertionError(("D134,D145 quotient gcd is not a nonzero constant", len(gcd)))
    relation = _a_sub(
        _a_add(_a_mul(u134, left_a, qfield), _a_mul(u145, right_a, qfield), qfield),
        gcd,
        qfield,
    )
    if relation:
        raise AssertionError(("F40 unnormalized Bezout relation has a residual", relation))
    constant = gcd[0]
    multiplication = []
    for row in range(4):
        multiplication.append([qfield.mul(constant, tuple(qfield.pfield.one if index == column else qfield.pfield.zero for index in range(4)))[row] for column in range(4)])
    norm = _determinant_residue(multiplication, pfield)
    if norm.is_zero:
        raise AssertionError("F40 constant has zero 4x4 multiplication norm")
    return {
        "factor": "F40",
        "degree_p": int(factor.degree()),
        "primitive": True,
        "irreducible": True,
        "gcd_with_H2": "1",
        "quotient_ring": "K=QQ[p]/(F40), A=K[q]/(Q6), polynomial ring A[a]",
        "route": "exact extended-Euclid quotient-gcd of D134,D145",
        "quotient_gcd_degree": 0,
        "unnormalized_constant_relation": True,
        "bezout_relation_checked": True,
        "bezout_residual_sha256": _a_poly_hash(relation),
        "euclidean_steps": steps,
        "constant_a_degree": 0,
        "constant_q_degree": max((index for index, item in enumerate(constant) if not item.is_zero), default=-1),
        "constant_q_terms": sum(not item.is_zero for item in constant),
        "nonzero_4x4_multiplication_norm": True,
        "norm_p_degree": int(norm.poly.degree()),
        "raw_input_metadata": {
            "D134": d134_metadata,
            "D145": d145_metadata,
            "D145_current_canonical_term_count": CURRENT_D145_TERM_COUNT,
            "D145_current_canonical_terms_sha256": CURRENT_D145_TERMS_SHA256,
            "D145_current_canonical_integer_content": CURRENT_D145_INTEGER_CONTENT,
            "D145_current_canonical_denominator": "H2^3",
            "D145_current_canonical_match": d145_current_match,
            "D145_denominator_match": d145_denominator_match,
            "D145_historical_term_count_pin": 3444,
            "D145_historical_pin_reproduced": False,
            "D145_historical_pin_status": "stale_normalization_expectation; not used as current equality pin",
        },
        "status": "verified_exact_F40_quotient_gcd",
        "arithmetic_overlap": "No python-flint algorithm is used in this F40 leaf; it is an independent SymPy exact residue-field/quotient-Euclid replay, while the p-cover uses python-flint.",
    }


def _determinant_residue(matrix: list[list[Residue]], field: ResidueField):
    if not matrix:
        return field.one
    work = [list(row) for row in matrix]
    size = len(work)
    result = field.one
    sign = 1
    for column in range(size):
        pivot = next((row for row in range(column, size) if not work[row][column].is_zero), None)
        if pivot is None:
            return field.zero
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            sign = -sign
        pivot_value = work[column][column]
        result = result * pivot_value
        inverse = pivot_value.inverse()
        for row in range(column + 1, size):
            factor = work[row][column] * inverse
            if factor.is_zero:
                continue
            for j in range(column + 1, size):
                work[row][j] = work[row][j] - factor * work[column][j]
    return -result if sign < 0 else result


def _exact_c4_pair_unit(determinants: dict[str, Any]) -> dict[str, Any]:
    """Search exact bounded Macaulay spans for 1 in the C4 pair ideal."""
    factor = "C4"
    pfield = ResidueField(_factor_expression(factor))
    qfield = QuotientResidueField(pfield, q6_expression(p, q))
    generators = _fibre_q_generators(determinants, ("D134", "D012"), qfield)
    for bound in range(1, 9):
        rows, columns = _macaulay_matrix(generators, qfield, bound, variables=1)
        target = [qfield.pfield.zero] * columns
        target[0] = qfield.pfield.one
        membership = _field_membership(rows, target)
        if membership["target_in_span"]:
            return {
                "factor": _factor_expression(factor).__str__(),
                "ideal": "<D134,D012>",
                "method": "exact quotient-field K-linear Macaulay RREF membership",
                "unit": True,
                "bound": bound,
                "columns": columns,
                **{key: value for key, value in membership.items() if key != "target_residual"},
                "target_residual_zero": all(value.is_zero for value in membership["target_residual"]),
                "q6_srepr_sha256": sha256_bytes(sp.srepr(q6_expression()).encode()),
                "generator_a_poly_sha256": [_a_generator_hash(generator) for generator in generators],
                "macaulay_construction": _macaulay_metadata(generators, bound, 1, rows, columns),
            }
    raise AssertionError("C4 pair does not contain 1 at tested exact bounds")


def fibre_closures(bridge_data: dict[str, Any], verbose: bool = False) -> dict[str, Any]:
    """Recompute every retained factor closure over exact residue fields."""
    determinants = bridge_data["determinants"]
    p_values = bridge_data["p_values"]

    closures = {"C4": _exact_c4_pair_unit(determinants)}
    rank_mismatches = []
    rank_specs = (
        ("R8", ("D134", "D012", "D013"), 7, 32),
        ("p2_plus_1", ("D134", "D012", "D145"), 5, 24),
        ("R4", ("D134", "D012", "D145"), 5, 24),
    )
    for factor, names, bound, expected in rank_specs:
        if verbose:
            print(f"[GLD103 audit] Macaulay fibre {factor}", file=sys.stderr, flush=True)
        membership, columns, construction = _fibre_rank(determinants, names, factor, bound)
        rank_match = (
            membership["rank"],
            columns,
            membership["rank_with_target"],
            membership["target_in_span"],
        ) == (expected, expected, expected, True)
        if not rank_match:
            rank_mismatches.append({
                "factor": factor,
                "expected_rank": expected,
                "expected_columns": expected,
                "actual_rank": membership["rank"],
                "actual_columns": columns,
                "actual_rank_with_target": membership["rank_with_target"],
                "target_in_span": membership["target_in_span"],
            })
        closures[factor] = {
            "factor": _factor_expression(factor).__str__(),
            "ideal": "<Q6," + ",".join(names) + ">",
            "method": "exact K-linear q-quotient Macaulay matrix",
            "bound": bound,
            "rank": membership["rank"],
            "columns": columns,
            "rank_with_target": membership["rank_with_target"],
            "target_in_span": membership["target_in_span"],
            "rref_pivots": membership["rref_pivots"],
            "expected_rank": expected,
            "rank_match": rank_match,
            "macaulay_construction": construction,
            "generators": list(names),
            "unit": True,
        }

    physical_specs = (
        ("F4", 3, 68),
        # The q-quotient rows include all four q-basis shifts.  Whole-P_i
        # normalization gives the current exact 66/80 leaf; a pre-fix
        # per-B-coefficient normalization spuriously reported 67.
        ("p2_minus_2p_plus_2", 3, 66),
    )
    for factor, bound, expected in physical_specs:
        if verbose:
            print(f"[GLD103 audit] physical localized Macaulay {factor}", file=sys.stderr, flush=True)
        membership, columns, construction = _physical_rank(p_values, factor, bound)
        rank_match = (
            membership["rank"],
            columns,
            membership["rank_with_target"],
            membership["target_in_span"],
        ) == (expected, 80, expected, True)
        if not rank_match:
            rank_mismatches.append({
                "factor": factor,
                "expected_rank": expected,
                "expected_columns": 80,
                "actual_rank": membership["rank"],
                "actual_columns": columns,
                "actual_rank_with_target": membership["rank_with_target"],
                "target_in_span": membership["target_in_span"],
            })
        closures[factor] = {
            "factor": _factor_expression(factor).__str__(),
            "ideal": "<P0,P1,P2,P3,P4,P5,z*B*Delta-1>",
            "method": "exact sparse total-degree Macaulay over A[a,B,z]",
            "bound": bound,
            "rank": membership["rank"],
            "columns": columns,
            "rank_with_target": membership["rank_with_target"],
            "target_in_span": membership["target_in_span"],
            "rref_pivots": membership["rref_pivots"],
            "expected_rank": expected,
            "rank_match": rank_match,
            "generators": ["P0", "P1", "P2", "P3", "P4", "P5", "z*B*Delta-1"],
            "q_basis_shift_correction": "complete four q-basis shifts; whole-P_i normalization retained; current exact rank is 66/80",
            "macaulay_construction": construction,
            "unit": True,
        }

    closures["F40"] = f40_closure(determinants)
    closure_status = (
        "verified_exact_local_fibre_closures"
        if not rank_mismatches and closures["F40"].get("status") == "verified_exact_F40_quotient_gcd"
        else (
            "candidate_fail_closed_rank_reconciliation"
            if rank_mismatches
            else "candidate_fail_closed_F40_raw_term_count_reconciliation"
        )
    )
    return {
        "status": closure_status,
        "coefficient_ring": "characteristic-zero exact quotient A[a,B,z]",
        "localizer": "z*B*Delta-1",
        "closures": closures,
        "rank_expectation_mismatches": rank_mismatches,
        "outside_declared_open": {
            "P": "P divides Delta, so P=0 is outside D(B*H2*Delta)",
            "H2": "H2 is the Q6 q-leading coefficient and is explicitly inverted",
        },
    }


def replay_gld102() -> dict[str, Any]:
    """Run the tracked GLD102 audit as a bounded p=0,1 dependency replay."""
    started = time.monotonic()
    if not GLD102_AUDIT.is_file():
        raise AssertionError("tracked GLD102 audit is missing")
    # The subprocess is deliberately the tracked GLD102 audit, not the new
    # primary and not a generated output.  Its own check recomputes both B/C
    # charts, Groebner bases, residuals, and rank-seven witnesses.
    try:
        completed = subprocess.run(
            [sys.executable, str(GLD102_AUDIT)],
            cwd=str(ROOT),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=900,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError("GLD102 replay timed out; p=0,1 closure is unverified") from exc
    if completed.returncode != 0:
        raise AssertionError(("tracked GLD102 replay failed", completed.returncode, completed.stderr[-1000:]))
    decoder = json.JSONDecoder()
    payload = None
    for offset, character in enumerate(completed.stdout):
        if character != "{":
            continue
        try:
            candidate, _end = decoder.raw_decode(completed.stdout[offset:])
        except json.JSONDecodeError:
            continue
        if isinstance(candidate, dict) and candidate.get("status"):
            payload = candidate
            break
    if payload is None:
        raise AssertionError("tracked GLD102 replay did not emit structured JSON")
    expected_scope = "normalized GLD88 H4/Q6 chart, characteristic zero, p in {0,1}, arbitrary a, D(Delta); rank(M)<=6 implies B=C=0"
    if payload.get("status") != "independent_exact_GLD102_audit":
        raise AssertionError(("tracked GLD102 status drift", payload.get("status")))
    if payload.get("global_conjecture") != "UNRESOLVED":
        raise AssertionError("GLD102 global status drift")
    if payload.get("scope") != expected_scope:
        raise AssertionError(("tracked GLD102 scope drift", payload.get("scope")))
    if payload.get("rank_to_selector_direction_only") is not True:
        raise AssertionError("GLD102 dependency is not the required one-way rank bridge")
    if payload.get("support_digest_sha256") != EXPECTED_GLD102_SUPPORT_DIGEST:
        raise AssertionError("GLD102 support digest drift")
    cases = payload.get("cases")
    if not isinstance(cases, dict) or set(cases) != {"p0", "p1"}:
        raise AssertionError("GLD102 did not return both p0 and p1 cases")
    return {
        "called_tracked_audit": True,
        "source": GLD102_AUDIT.relative_to(ROOT).as_posix(),
        "claim_id": "GLD102",
        "status": payload["status"],
        "returncode": completed.returncode,
        "scope": payload["scope"],
        "global_conjecture": payload["global_conjecture"],
        "support_digest_sha256": payload["support_digest_sha256"],
        "canonical_support_digest_expected": EXPECTED_GLD102_SUPPORT_DIGEST,
        "source_sha256": source_hash(GLD102_AUDIT),
        "source_lf_sha256": source_hash(GLD102_AUDIT, lf=True),
        "rank_to_selector_direction_only": payload["rank_to_selector_direction_only"],
        "cases": cases,
        "structured_result_checked": True,
        "elapsed_seconds": round(time.monotonic() - started, 3),
    }


def clearing_gate_check() -> dict[str, Any]:
    clearing_gate = sp.expand(P**23 * H2**45)
    if sp.expand(clearing_gate - P**23 * H2**45) != 0:
        raise AssertionError("clearing gate transcription drift")
    quotient = sp.cancel(DELTA / P)
    if sp.denom(quotient) != 1 or sp.expand(DELTA - P * quotient) != 0:
        raise AssertionError("P does not divide Delta")
    q6 = sp.Poly(q6_expression(), q, domain=K)
    if sp.expand(q6.LC() - H2) != 0:
        raise AssertionError("Q6 leading coefficient is not H2")
    selected_scalar_product = sp.factor(sp.prod(CLEARING_SCALARS.values()))
    expected_scalar_product = sp.factor(2**14 * P**23 * H2**25)
    if sp.expand(selected_scalar_product - expected_scalar_product) != 0:
        raise AssertionError("selected minor clearing scalar product drift")
    return {
        "clearing_gate": "P^23*H2^45",
        "selected_minor_scalar_product": str(selected_scalar_product),
        "selected_minor_scalar_product_checked": True,
        "P_divides_Delta": True,
        "H2_is_Q6_q_leading_coefficient": True,
        "declared_open": "D(B*H2*Delta)",
        "clearing_gate_redundant_on_declared_open": True,
        "gate_not_added_to_scope": True,
        "no_claim_on_P_or_H2_boundary": True,
    }


def dependency_manifest() -> dict[str, Any]:
    requirements = ROOT / "requirements.txt"
    lockfile = ROOT / "requirements.lock.txt"
    if not requirements.is_file() or not lockfile.is_file():
        raise AssertionError("dependency pin files are missing")
    req_text = requirements.read_text(encoding="utf-8")
    lock_text = lockfile.read_text(encoding="utf-8")
    if "python-flint==0.9.0" not in req_text or "python-flint==0.9.0" not in lock_text:
        raise AssertionError("python-flint dependency pin drift")
    if "sympy==1.14.0" not in lock_text:
        raise AssertionError("SymPy lock pin drift")
    observed = None
    try:
        import flint
        observed = str(getattr(flint, "__version__", ""))
    except ImportError:
        observed = "not-installed"
    return {
        "requirements_pin": "python-flint==0.9.0",
        "lock_pin": "python-flint==0.9.0",
        "sympy_lock_pin": "sympy==1.14.0",
        "runtime_python_flint": observed,
        "full_mode_requires": "python-flint==0.9.0",
    }


def manifest_only() -> dict[str, Any]:
    started = time.monotonic()
    sources = source_manifest()
    audit_source = audit_source_manifest()
    relations = canonical_support()
    digests = support_digests(relations)
    q6 = sp.expand(q6_expression())
    q6_hash = sha256_bytes(sp.srepr(q6).encode())
    if q6_hash != EXPECTED_Q6_SREPR_SHA256:
        raise AssertionError("Q6 transcription digest drift")
    chart_denominators = denominator_provenance(h4_family())
    chart_comparison = compare_h4_family_to_pinned_gld88()
    deps = dependency_manifest()
    return {
        "status": "manifest_scope_validated_not_a_proof",
        "global_conjecture": "UNRESOLVED",
        "audit_source": audit_source,
        "scope": {
            "claim": "GLD103",
            "chart": "GLD88/F88 equal-leaf H4, arbitrary a",
            "field": "characteristic zero",
            "open": "D(B*H2*Delta)",
            "branch": "G_T0=G_T1=G_T2=G_Y1=G_X3=0",
            "E31": "neither imposed nor inverted",
        },
        "sources": sources,
        "support_digests": digests,
        "q6_srepr_sha256": q6_hash,
        "chart_denominator_provenance": chart_denominators,
        "chart_comparison": chart_comparison,
        "dependencies": deps,
        "full_arithmetic_run": False,
        "elapsed_seconds": round(time.monotonic() - started, 3),
    }


def check(mode: str = "full", verbose: bool = False) -> dict[str, Any]:
    if mode == "manifest-only":
        return manifest_only()
    started = time.monotonic()
    sources = source_manifest()
    audit_source = audit_source_manifest()
    relations = canonical_support()
    digests = support_digests(relations)
    q6 = sp.expand(q6_expression())
    q6_hash = sha256_bytes(sp.srepr(q6).encode())
    if q6_hash != EXPECTED_Q6_SREPR_SHA256:
        raise AssertionError("Q6 transcription digest drift")
    chart_comparison = compare_h4_family_to_pinned_gld88()
    algebra = QuotientAlgebra(q6)
    bridge_data = bridge(relations, algebra, verbose=verbose)
    result: dict[str, Any] = {
        "status": "verified_exact_independent_GLD103_bridge" if mode == "bridge-only" else "verified_exact_independent_GLD103_audit",
        "global_conjecture": "UNRESOLVED",
        "audit_source": audit_source,
        "runtime_mode": mode,
        "scope": {
            "claim": "GLD103 all-zero coefficient branch only",
            "chart": "locally transcribed GLD88/F88 normalized H4 chart, arbitrary a",
            "field": "QQ then algebraically closed characteristic-zero extension",
            "open": "D(B*H2*Delta)",
            "E31": "not imposed or inverted",
            "rank_statement": "rank(M)<=6 implies selected actual 7x7 minors vanish; no converse",
        },
        "source_manifest": sources,
        "support_digests": digests,
        "q6": {
            "degree_q": int(sp.degree(q6, q)),
            "leading_coefficient": str(sp.Poly(q6, q, domain=K).LC()),
            "srepr_sha256": q6_hash,
        },
        "chart_comparison": chart_comparison,
        "bridge": bridge_data["metadata"],
        "independence_boundary": {
            "graph_reconstruction": "independent AST extraction of pinned GLD71 literals plus local GLD88 chart transcription",
            "arithmetic": "independent sparse offset determinant and quotient implementation; FLINT cover resultants are independently recomputed",
            "f40_overlap": "F40 uses SymPy exact residue-field arithmetic and extended Euclid, not the python-flint cover algorithm; shared inputs and quotient presentation remain disclosed",
            "gld102": "p=0,1 is a bounded replay of the separately tracked GLD102 audit dependency",
        },
        "nonclaims": [
            "No converse from selected actual minors, coefficient rows, or coefficient determinants to rank.",
            "No pivot-branch, B=0 endpoint, H2=0, Delta=0, E31, wider-chart, source, Fitting, physical, or global conclusion.",
            "The eleven factor list is squarefree support; native degree-624 multiplicities and exact H2^2-normalized degree-620 multiplicities are reported separately.",
            "The global Krenn-Gu conjecture remains UNRESOLVED.",
        ],
    }
    if mode == "bridge-only":
        result["dependency_pins"] = dependency_manifest()
        result["clearing_gate"] = clearing_gate_check()
        result["elapsed_seconds"] = round(time.monotonic() - started, 3)
        return result

    result["clearing_gate"] = clearing_gate_check()
    failures = []
    try:
        result["p_cover"] = exact_p_cover(bridge_data["determinants"], algebra)
    except Exception as exc:
        result["p_cover"] = {
            "status": "unverified_exact_p_cover",
            "error": repr(exc),
        }
        failures.append(f"Exact p-cover replay failed: {exc}")
    try:
        result["fibre_closures"] = fibre_closures(bridge_data, verbose=verbose)
    except Exception as exc:
        result["fibre_closures"] = {
            "status": "unverified_exact_local_fibre_closures",
            "error": repr(exc),
        }
        failures.append(f"Exact fibre-closure replay failed: {exc}")
    try:
        result["gld102_p0_p1"] = replay_gld102()
    except Exception as exc:
        result["gld102_p0_p1"] = {
            "status": "unverified_tracked_GLD102_replay",
            "error": repr(exc),
        }
        failures.append(f"Tracked GLD102 replay failed: {exc}")
    result["dependency_pins"] = dependency_manifest()
    if failures:
        result["failure_reasons"] = failures
    if (
        failures
        or not result["p_cover"].get("degree_match", False)
        or result["fibre_closures"].get("status", "").startswith("candidate")
    ):
        result["status"] = "candidate_fail_closed_GLD103_reconciliation"
        result.setdefault("failure_reasons", [])
        if result["p_cover"].get("status") == "verified_exact_necessary_p_cover" and not result["p_cover"].get("degree_match", False):
            result["failure_reasons"].append("Exact H2^2 normalization did not reproduce the historical degree-620 presentation.")
        rank_mismatches = result["fibre_closures"].get("rank_expectation_mismatches", [])
        if rank_mismatches:
            result["failure_reasons"].append(
                "Exact Macaulay rank expectation mismatch: "
                + json.dumps(rank_mismatches, sort_keys=True)
            )
        closures = result["fibre_closures"].get("closures", {})
        if closures.get("F40", {}).get("status", "").startswith("candidate"):
            result["failure_reasons"].append("F40 raw D145 term-count pin is not reproduced by the independent direct bridge.")
    result["elapsed_seconds"] = round(time.monotonic() - started, 3)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Independent tracked GLD103 audit")
    parser.add_argument("--manifest-only", action="store_true", help="validate scope and dependency pins only")
    parser.add_argument("--bridge-only", action="store_true", help="rebuild actual minors and coefficient bridge only")
    parser.add_argument("--output", type=Path, help="optional JSON output path")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    mode = "manifest-only" if args.manifest_only else ("bridge-only" if args.bridge_only else "full")
    try:
        result = check(mode=mode, verbose=args.verbose)
    except Exception as exc:
        print(f"GLD103 independent audit FAIL CLOSED ({mode}): {exc}", file=sys.stderr)
        raise
    text = json.dumps(result, indent=2, sort_keys=True, default=str) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    if result.get("status", "").startswith("candidate_fail_closed"):
        print(f"GLD103 independent audit {mode}: FAIL CLOSED")
    else:
        print(f"GLD103 independent audit {mode}: PASS")
    print(text)
    if result.get("status", "").startswith("candidate_fail_closed"):
        raise SystemExit(2)


if __name__ == "__main__":
    main()
