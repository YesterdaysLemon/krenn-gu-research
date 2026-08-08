#!/usr/bin/env python3
"""Independent modular audit of the tenth-component generic H31 obstruction.

Imports nothing from the primary verifier.  Rebuilds the concentrated bases
import sys

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap, expose_claim_package  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
ROOT = REPO_ROOT

from the raw working-note planes with its own dynamic-programming permanent,
then, at two finite-field parameter samples:

  * frames q=0,1: checks the 0000-diagonal row vanishes at every marking
    (t-free identity checked on the full t-grid via the multilinear table);
  * frames q=2,3: exhausts all p^4 markings, computes the mixed kernel by
    Gaussian elimination, and confirms NO marking has a genuine binary
    survivor (both diagonals nonzero on a common kernel vector); also
    confirms the reconstruction direction lies in every kernel with
    A=0, B=-2P.

Corroboration only; the theorem is the characteristic-zero calculation of
the primary verifier.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
THEOREM = HERE / "P5_H31_COINCIDENT_SUPPORT_COMPONENT_GENERIC_OBSTRUCTION.md"

WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED = tuple(w for w in WORDS if w not in ((0, 0, 0, 0), (1, 1, 1, 1)))

SAMPLES = (
    (13, (2, 3, 7, 5)),
    (17, (3, 5, 2, 9)),
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dp_permanent(rows, p):
    """Dynamic-programming permanent over F_p (column-subset DP)."""
    n = len(rows)
    full = (1 << n) - 1
    state = {0: 1}
    for row in rows:
        nxt = {}
        for mask, value in state.items():
            for col in range(n):
                if not (mask >> col) & 1 and row[col] % p:
                    new = mask | (1 << col)
                    nxt[new] = (nxt.get(new, 0) + value * row[col]) % p
        state = nxt
    return state.get(full, 0) % p


class Frame:
    """Marked H31 frame data mod p with multilinear t-tables."""

    def __init__(self, q, p, sample):
        bb, ee, mm, cc = sample
        PP = (bb * ee * cc + bb + ee) % p
        QQ = (bb * ee * (mm + 1)) % p
        alpha = ((1, -1, 0, 0), (1, -1, 0, 0), (0, 0, 1, 1),
                 (PP, (PP * mm - QQ * cc) % p, -QQ % p, QQ))
        beta = ((0, 1, bb, -bb % p), (0, 1, ee, -ee % p), (1, 1, 0, 0),
                (0, cc, 1, p - 1))
        self.p = p
        self.q = q
        self.P = PP
        common = tuple(j for j in range(4) if j != q)
        self.alpha_c = tuple(tuple(alpha[i][j] % p for j in common) for i in range(4))
        self.beta_c = tuple(tuple(beta[i][j] % p for j in common) for i in range(4))
        self.alpha_q = tuple(alpha[i][q] % p for i in range(4))
        self.beta_q = tuple(beta[i][q] % p for i in range(4))
        # coefficient tables: coeff[w][i] = {subset S of marked modes != i: value}
        self.tables = {}
        for wd in WORDS:
            entry = []
            for i in range(4):
                others = tuple(j for j in range(4) if j != i)
                marked = tuple(j for j in others if wd[j])
                table = {}
                for subset in itertools.chain.from_iterable(
                        itertools.combinations(marked, size)
                        for size in range(len(marked) + 1)):
                    rows = []
                    for j in others:
                        if wd[j]:
                            rows.append(self.alpha_c[j] if j in subset
                                        else self.beta_c[j])
                        else:
                            rows.append(self.alpha_c[j])
                    value = dp_permanent(rows, self.p)
                    if value:
                        table[subset] = value
                entry.append(table)
            self.tables[wd] = entry

    def coefficient(self, wd, i, t):
        total = 0
        for subset, value in self.tables[wd][i].items():
            term = value
            for j in subset:
                term = term * t[j] % self.p
            total = (total + term) % self.p
        return total

    def rows(self, t, word_list):
        out = []
        for wd in word_list:
            row = [0] * 8
            for i in range(4):
                row[i + (4 if wd[i] else 0)] = self.coefficient(wd, i, t)
            out.append(row)
        return out

    def reconstruction(self, t):
        return tuple(self.alpha_q) + tuple(
            (self.beta_q[i] + t[i] * self.alpha_q[i]) % self.p for i in range(4))


def kernel_mod_p(rows, p):
    mat = [row[:] for row in rows]
    pivots = []
    rank = 0
    for col in range(8):
        sel = None
        for i in range(rank, len(mat)):
            if mat[i][col] % p:
                sel = i
                break
        if sel is None:
            continue
        mat[rank], mat[sel] = mat[sel], mat[rank]
        inv = pow(mat[rank][col], p - 2, p)
        mat[rank] = [(x * inv) % p for x in mat[rank]]
        for i in range(len(mat)):
            if i != rank and mat[i][col] % p:
                factor = mat[i][col]
                mat[i] = [(x - factor * y) % p for x, y in zip(mat[i], mat[rank])]
        pivots.append(col)
        rank += 1
    kernel = []
    for free in (colx for colx in range(8) if colx not in pivots):
        vec = [0] * 8
        vec[free] = 1
        for row_index, pivot in enumerate(pivots):
            vec[pivot] = (-mat[row_index][free]) % p
        kernel.append(vec)
    return rank, kernel


def functional_nonzero_on(vectors, functional, p):
    return any(sum(f * v for f, v in zip(functional, vec)) % p for vec in vectors)


def audit_sample(p, sample):
    report = {}
    for q in (0, 1):
        frame = Frame(q, p, sample)
        for i in range(4):
            assert not frame.tables[(0, 0, 0, 0)][i], (q, i)
        report[f"q{q}"] = "A row identically zero (all markings): no genuine survivor"
    for q in (2, 3):
        frame = Frame(q, p, sample)
        genuine = 0
        kernel_histogram = {}
        for t in itertools.product(range(p), repeat=4):
            mixed = frame.rows(t, MIXED)
            rank, kernel = kernel_mod_p(mixed, p)
            kernel_histogram[8 - rank] = kernel_histogram.get(8 - rank, 0) + 1
            arow = frame.rows(t, [(0, 0, 0, 0)])[0]
            brow = frame.rows(t, [(1, 1, 1, 1)])[0]
            zrec = frame.reconstruction(t)
            assert all(sum(rv * zv for rv, zv in zip(row, zrec)) % p == 0
                       for row in mixed)
            assert sum(rv * zv for rv, zv in zip(arow, zrec)) % p == 0
            assert sum(rv * zv for rv, zv in zip(brow, zrec)) % p == (-2 * frame.P) % p
            if kernel and functional_nonzero_on(kernel, arow, p) \
                    and functional_nonzero_on(kernel, brow, p):
                genuine += 1
        assert genuine == 0, (q, p, sample, genuine)
        report[f"q{q}"] = {
            "markings": p ** 4,
            "genuine_survivors": genuine,
            "kernel_dimension_histogram": kernel_histogram,
        }
    return report


DIVISOR_SAMPLES = (
    (13, (4, -4, 3, 7), "b+e=0"),
    (13, (2, 5, 3, 0), "c=0"),
)
MINOR_ROWS = ((0, 1, 2, 7), (0, 1, 3, 7))


def rank_mod_p(mat, ncols, p):
    rank = 0
    for col in range(ncols):
        sel = None
        for i in range(rank, len(mat)):
            if mat[i][col] % p:
                sel = i
                break
        if sel is None:
            continue
        mat[rank], mat[sel] = mat[sel], mat[rank]
        inv = pow(mat[rank][col], p - 2, p)
        mat[rank] = [(x * inv) % p for x in mat[rank]]
        for i in range(len(mat)):
            if i != rank and mat[i][col] % p:
                factor = mat[i][col]
                mat[i] = [(x - factor * y) % p
                          for x, y in zip(mat[i], mat[rank])]
        rank += 1
    return rank


def on_sheet(divisor, p, sample, t):
    bb, ee, mm, cc = sample
    if divisor == "b+e=0":
        return (t[2] % p == 0
                and (t[0] + t[1] - 1) % p == 0
                and (t[1] * t[1] - t[1]) % p == 0
                and (2 * bb * bb * t[3] + 1) % p == 0)
    if divisor == "c=0":
        lin = (ee * ee * (mm + 1) * t[0] + bb * bb * (mm + 1) * t[1]
               - bb * bb + bb * ee * (mm - 1) - ee * ee) % p
        quad = (bb * bb * (mm * mm - 1) * t[1] * t[1]
                + (2 * bb * bb + bb * ee * (mm - 1) ** 2 - 2 * ee * ee * mm) * t[1]
                - bb * bb + bb * ee * (mm - 1) + ee * ee * mm) % p
        return t[3] % p == 0 and t[2] % p == 0 and lin == 0 and quad == 0
    raise ValueError(divisor)


def one_marked_rank_and_minors(frame, t, z, p):
    """Mode-2 one-marked 8x4 map at extension z, via dp_permanent probes."""
    mode = 2
    alpha_x = tuple(frame.alpha_c[i] + (z[i],) for i in range(4))
    beta_x = tuple(
        tuple((frame.beta_c[i][j] + t[i] * frame.alpha_c[i][j]) % p
              for j in range(3)) + (z[4 + i],)
        for i in range(4))
    rows = []
    for bits in itertools.product((0, 1), repeat=3):
        selected = []
        bit_index = 0
        for other in range(4):
            if other == mode:
                selected.append(None)
            else:
                selected.append(beta_x[other] if bits[bit_index] else alpha_x[other])
                bit_index += 1
        row = []
        for coordinate in range(4):
            basis = tuple(int(idx == coordinate) for idx in range(4))
            row.append(dp_permanent(
                tuple(basis if other == mode else selected[other]
                      for other in range(4)), p))
        rows.append(row)
    rank = rank_mod_p([r[:] for r in rows], 4, p)

    def minor(rowset):
        sub = [rows[i][:] for i in rowset]
        det = 0
        for perm in itertools.permutations(range(4)):
            sign = 1
            seen = list(perm)
            for i in range(4):
                for j in range(i + 1, 4):
                    if seen[i] > seen[j]:
                        sign = -sign
            term = sign
            for i in range(4):
                term = term * sub[i][perm[i]] % p
            det = (det + term) % p
        return det

    minors = [minor(rowset) for rowset in MINOR_ROWS]
    return rank, minors


def audit_divisor_sample(p, sample, divisor):
    report = {}
    for q in (2, 3):
        frame = Frame(q, p, sample)
        survivors = []
        for t in itertools.product(range(p), repeat=4):
            mixed = frame.rows(t, MIXED)
            rank, kernel = kernel_mod_p(mixed, p)
            if not kernel:
                continue
            arow = frame.rows(t, [(0, 0, 0, 0)])[0]
            brow = frame.rows(t, [(1, 1, 1, 1)])[0]
            if not (functional_nonzero_on(kernel, arow, p)
                    and functional_nonzero_on(kernel, brow, p)):
                continue
            assert on_sheet(divisor, p, sample, t), (divisor, sample, t)
            assert len(kernel) == 2, (divisor, t, len(kernel))
            checked = 0
            for coeffs in itertools.product(range(p), repeat=2):
                if coeffs == (0, 0):
                    continue
                first = next(i for i, x in enumerate(coeffs) if x)
                if coeffs[first] != 1:
                    continue
                z = [0] * 8
                for coefficient, vector in zip(coeffs, kernel):
                    for j in range(8):
                        z[j] = (z[j] + coefficient * vector[j]) % p
                az = sum(a * v for a, v in zip(arow, z)) % p
                bz = sum(a * v for a, v in zip(brow, z)) % p
                if az and bz:
                    rank4, minors = one_marked_rank_and_minors(frame, t, z, p)
                    assert rank4 == 4, (divisor, t, z, rank4)
                    assert any(minors), (divisor, t, z, minors)
                    checked += 1
            assert checked > 0, (divisor, t)
            survivors.append(t)
        assert len(survivors) == 2, (divisor, q, survivors)
        report[f"q{q}"] = {
            "survivor_markings": [list(t) for t in survivors],
            "all_on_predicted_sheet": True,
            "kernel_dimension": 2,
            "all_genuine_directions_mode2_rank4": True,
        }
    return report


def main() -> None:
    results = {}
    for p, sample in SAMPLES:
        results[f"p={p} sample={sample}"] = audit_sample(p, sample)
        print(f"p={p} sample={sample}: PASS")
    divisor_results = {}
    for p, sample, divisor in DIVISOR_SAMPLES:
        divisor_results[f"p={p} sample={sample} on {divisor}"] = \
            audit_divisor_sample(p, sample, divisor)
        print(f"p={p} sample={sample} on {divisor}: PASS")
    output = {
        "audited": True,
        "independent_of_primary": True,
        "method": (
            "dynamic-programming permanent, multilinear marking tables, "
            "finite-field kernel census; genuineness via the two-functional "
            "kernel criterion (valid for p>2)"
        ),
        "samples": results,
        "divisor_samples": divisor_results,
        "conclusion": (
            "no genuine binary Delta_2 neighbour in any frame at any marking "
            "at the sampled generic component points; on the divisor samples "
            "the survivors sit exactly on the predicted sheets with rank-four "
            "mode-2 one-marked maps; corroborates the characteristic-zero "
            "theorem and its divisor closures"
        ),
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    out_path = HERE / "tmp" / "p5_h31_coincident_support_component_generic_audit.json"
    out_path.parent.mkdir(exist_ok=True)
    out_path.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
