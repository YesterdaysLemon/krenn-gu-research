#!/usr/bin/env python3
"""Independent modular audit of the tenth-component generic weighted H22
obstruction.  Imports nothing from the primary verifier.

At finite-field parameter samples and slopes (generic and special):

  * D_01 pencil: the 0000 word has an empty coefficient table — it vanishes
    for every marking and extension (the identity of the theorem);
  * D_23 pencil: all p^4 markings are exhausted; no marking has a genuine
    binary survivor; the universal kernel direction
    z* = (r*row[3] + row[2]) lies in every kernel with A=0, B=-2P(r-1)^2.

Corroboration only; the theorem is the characteristic-zero calculation of
the primary verifier.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
THEOREM = HERE / "P5_H22_COINCIDENT_SUPPORT_COMPONENT_GENERIC_OBSTRUCTION.md"

WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED = tuple(w for w in WORDS if w not in ((0, 0, 0, 0), (1, 1, 1, 1)))

CENSUS = (
    (13, (2, 3, 7, 5), (3, 1, -1, 0)),
    (17, (3, 5, 2, 9), (5,)),
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dp_permanent(rows, p):
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


class PencilFrame:
    def __init__(self, pencil, p, sample, slope):
        bb, ee, mm, cc = sample
        PP = (bb * ee * cc + bb + ee) % p
        QQ = (bb * ee * (mm + 1)) % p
        alpha = ((1, -1, 0, 0), (1, -1, 0, 0), (0, 0, 1, 1),
                 (PP, (PP * mm - QQ * cc) % p, -QQ % p, QQ))
        beta = ((0, 1, bb, -bb % p), (0, 1, ee, -ee % p), (1, 1, 0, 0),
                (0, cc, 1, p - 1))
        self.p = p
        self.P = PP
        self.slope = slope % p

        def transform(row):
            if pencil == "01":
                return ((self.slope * row[0] + row[1]) % p, row[2] % p, row[3] % p)
            return (row[0] % p, row[1] % p, (self.slope * row[2] + row[3]) % p)

        self.alpha_c = tuple(transform(alpha[i]) for i in range(4))
        self.beta_c = tuple(transform(beta[i]) for i in range(4))
        # extension values of the universal kernel z* (for D_23)
        self.alpha_star = tuple((self.slope * alpha[i][3] + alpha[i][2]) % p
                                for i in range(4))
        self.beta_star = tuple((self.slope * beta[i][3] + beta[i][2]) % p
                               for i in range(4))
        self.alpha_raw = alpha
        self.beta_raw = beta
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
                    value = dp_permanent(rows, p)
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

    def universal_kernel(self, t):
        return tuple(self.alpha_star) + tuple(
            (self.beta_star[i] + t[i] * self.alpha_star[i]) % self.p
            for i in range(4))


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


def audit(p, sample, slopes):
    report = {}
    for slope in slopes:
        frame01 = PencilFrame("01", p, sample, slope)
        for i in range(4):
            assert not frame01.tables[(0, 0, 0, 0)][i], (slope, i)
        frame = PencilFrame("23", p, sample, slope)
        genuine = 0
        histogram = {}
        expected_b = (-2 * frame.P * (slope - 1) ** 2) % p
        for t in itertools.product(range(p), repeat=4):
            mixed = frame.rows(t, MIXED)
            rank, kernel = kernel_mod_p(mixed, p)
            histogram[8 - rank] = histogram.get(8 - rank, 0) + 1
            arow = frame.rows(t, [(0, 0, 0, 0)])[0]
            brow = frame.rows(t, [(1, 1, 1, 1)])[0]
            zstar = frame.universal_kernel(t)
            assert all(sum(rv * zv for rv, zv in zip(row, zstar)) % p == 0
                       for row in mixed)
            assert sum(rv * zv for rv, zv in zip(arow, zstar)) % p == 0
            assert sum(rv * zv for rv, zv in zip(brow, zstar)) % p == expected_b
            if kernel and functional_nonzero_on(kernel, arow, p) \
                    and functional_nonzero_on(kernel, brow, p):
                genuine += 1
        assert genuine == 0, (p, sample, slope, genuine)
        report[f"slope={slope}"] = {
            "D01_0000_word_identically_zero": True,
            "D23_markings": p ** 4,
            "D23_genuine_survivors": genuine,
            "D23_kernel_dimension_histogram": histogram,
        }
        print(f"p={p} sample={sample} slope={slope}: PASS")
    return report


DIVISOR_CENSUS = ((13, (4, -4, 3, 7), 3, "b+e=0"),)
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
    bb = sample[0]
    if divisor == "b+e=0":
        return (t[2] % p == 0
                and (t[0] + t[1] - 1) % p == 0
                and (t[1] * t[1] - t[1]) % p == 0
                and (2 * bb * bb * t[3] + 1) % p == 0)
    raise ValueError(divisor)


def one_marked_rank_and_minors(frame, t, z, p):
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

    return rank, [minor(rowset) for rowset in MINOR_ROWS]


def audit_divisor(p, sample, slope, divisor):
    frame = PencilFrame("23", p, sample, slope)
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
        checked = 0
        for coeffs in itertools.product(range(p), repeat=len(kernel)):
            if all(x == 0 for x in coeffs):
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
    assert len(survivors) == 2, (divisor, survivors)
    print(f"p={p} sample={sample} slope={slope} on {divisor}: PASS "
          f"(survivors {survivors})")
    return {
        "survivor_markings": [list(t) for t in survivors],
        "all_on_predicted_sheet": True,
        "all_genuine_directions_mode2_rank4": True,
    }


def main() -> None:
    results = {}
    for p, sample, slopes in CENSUS:
        results[f"p={p} sample={sample}"] = audit(p, sample, slopes)
    divisor_results = {}
    for p, sample, slope, divisor in DIVISOR_CENSUS:
        divisor_results[f"p={p} sample={sample} slope={slope} on {divisor}"] = \
            audit_divisor(p, sample, slope, divisor)
    output = {
        "audited": True,
        "independent_of_primary": True,
        "method": (
            "dynamic-programming permanent, multilinear marking tables, "
            "finite-field kernel census over generic and special slopes; "
            "genuineness via the two-functional kernel criterion"
        ),
        "census": results,
        "divisor_census": divisor_results,
        "conclusion": (
            "the 01 pencil is identically non-sharp and the 23 pencil has no "
            "genuine binary survivor at any sampled marking/slope; on the "
            "divisor sample the survivors sit exactly on the predicted "
            "sheets with rank-four mode-2 one-marked maps; corroborates the "
            "characteristic-zero theorem and its divisor closures"
        ),
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    out_path = HERE / "tmp" / "p5_h22_coincident_support_component_generic_audit.json"
    out_path.parent.mkdir(exist_ok=True)
    out_path.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
