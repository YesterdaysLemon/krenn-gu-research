#!/usr/bin/env python3
"""Replay the exact chart identities of the in-out path stratum note.

All computations are exact (sympy rationals plus one Singular
factorization).  This is an exploratory checkpoint verifier: it
certifies the chart identities and sample-point invariants, not a
component classification.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import subprocess
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
NOTE = ROOT / "P4_INOUT_PATH_STRATUM_WORKING_NOTE.md"

d = sp.Symbol("d")
v = sp.symbols("v0:4")
x = sp.symbols("x0:4")

U1_A = (0, 0, 1, -1)
Y3 = (0, 0, 1, 1)
U3_B = (1, 0, d, 0)
Y2 = (1, 0, -d, 0)

COORD_PAIRS = tuple(itertools.combinations(range(4), 2))
COMPLEMENT = {ab: tuple(sorted(set(range(4)) - set(ab)))
              for ab in COORD_PAIRS}
PERMS4 = tuple(itertools.permutations(range(4)))

F1 = -d*v[1]*x[0] + d*v[0]*x[1] - (v[2]+v[3])*x[1] - v[1]*x[2] + v[1]*x[3]
F2 = -d*v[1]*x[0] - d*v[0]*x[1] + (v[2]+v[3])*x[1] - v[1]*x[2] + v[1]*x[3]
F3 = d*v[1]*x[0] - d*v[0]*x[1] + (v[2]+v[3])*x[1] + v[1]*x[2] + v[1]*x[3]
F4 = d*v[1]*x[0] + d*v[0]*x[1] + (v[2]+v[3])*x[1] + v[1]*x[2] + v[1]*x[3]

SAMPLES = {
    "F1": {"v": (5, 8, 5, 5), "x": (7, 9, -3, sp.Rational(143, 8)),
           "d": 7,
           "profile": (4, 4, 3, 4, 3, 3),
           "relations": (((0, 3), 1), ((1, 3), 1), ((2, 3), 1))},
    "F2": {"v": (6, -4, -6, 5), "x": (0, -5, -7, sp.Rational(-263, 4)),
           "d": -8,
           "profile": (4, 4, 3, 4, 3, 3),
           "relations": (((0, 3), 1), ((1, 3), 1), ((2, 3), 1))},
    "F4": {"v": (3, 5, -4, -9), "x": (7, -7, -8, sp.Rational(-9, 5)),
           "d": -3,
           "profile": (4, 3, 2, 4, 3, 3),
           "relations": (((0, 2), 1), ((1, 3), 1), ((2, 3), 1))},
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rmul(u, w):
    return {ab: sp.expand(u[ab[0]] * w[ab[1]] + u[ab[1]] * w[ab[0]])
            for ab in COORD_PAIRS}


def pairing(P, Q):
    return sp.expand(sum(P[ab] * Q[COMPLEMENT[ab]]
                         for ab in COORD_PAIRS))


def perm4(rows):
    return sp.expand(sum(
        sp.prod(rows[k][pi[k]] for k in range(4)) for pi in PERMS4
    ))


def covector_matrix():
    zsym = sp.symbols("z0:4")
    rows = []
    # the u_1-side conditions vanish identically by associativity
    for w_row, is_u1 in ((U1_A, True), (tuple(v), False)):
        for c in (rmul(Y2, Y3), rmul(list(x), Y3)):
            zw = rmul(list(zsym), list(w_row))
            form = pairing(zw, c)
            row = [sp.expand(sp.diff(form, zi)) for zi in zsym]
            if is_u1:
                assert all(e == 0 for e in row)
            else:
                rows.append(row)
    return sp.Matrix(rows)


def cramer_identity(M):
    minors = {}
    for a_, b_ in itertools.combinations(range(4), 2):
        minors[(a_, b_)] = sp.expand(
            M[0, a_] * M[1, b_] - M[0, b_] * M[1, a_]
        )
    pivot = minors[(0, 1)]
    assert sp.expand(pivot + (v[2]+v[3]) * F3) == 0
    w2 = (minors[(1, 2)], -minors[(0, 2)], minors[(0, 1)], 0)
    w3 = (minors[(1, 3)], -minors[(0, 3)], 0, minors[(0, 1)])
    for w in (w2, w3):
        assert all(
            sp.expand(sum(M[r_, c_] * w[c_] for c_ in range(4))) == 0
            for r_ in range(2)
        )
    B = sp.zeros(2, 2)
    for i0, u0row in enumerate((w2, w3)):
        for i1, u1row in enumerate((U1_A, tuple(v))):
            B[i0, i1] = perm4((tuple(u0row), u1row, tuple(x), U3_B))
    det = sp.expand(B.det())
    return det, pivot


def factor_in_singular(det):
    program = "\n".join((
        "ring R=0,(d,v0,v1,v2,v3,x0,x1,x2,x3),dp;",
        f"poly f={str(det).replace('**', '^')};",
        f"poly g={str(sp.expand((v[2]+v[3])*F1*F2*F3*F4)).replace('**', '^')};",
        "poly q=f/g;",
        "poly check=f-q*g;",
        "int ok=(check==0)&&(q!=0)&&(deg(q)==0);",
        '"CODEX_RESULT:"+string(ok)+":"+string(q);',
        "quit;",
    ))
    completed = subprocess.run(
        ("Singular", "-q"), input=program, text=True,
        encoding="utf-8", errors="replace",
        capture_output=True, timeout=600, check=False,
    )
    if completed.returncode != 0 or completed.stderr.strip():
        raise AssertionError((completed.returncode, completed.stdout,
                              completed.stderr))
    markers = [line for line in completed.stdout.splitlines()
               if line.startswith("CODEX_RESULT:")]
    assert len(markers) == 1
    _tag, ok, content = markers[0].split(":", 2)
    assert ok == "1", completed.stdout
    return content


def analyse_point(point):
    subs = {**dict(zip(v, point["v"])), **dict(zip(x, point["x"])),
            d: point["d"]}
    zsym = sp.symbols("z0:4")
    rows = []
    for c in (rmul(Y2, Y3), rmul(list(x), Y3)):
        zw = rmul(list(zsym), list(v))
        form = pairing(zw, c)
        rows.append([sp.expand(sp.diff(form, zi)).subs(subs)
                     for zi in zsym])
    M = sp.Matrix(rows)
    kernel = M.nullspace()
    assert len(kernel) == 2
    def sub_row(row):
        return [sp.nsimplify(sp.sympify(c_).subs(subs)) for c_ in row]
    planes = [
        [[sp.nsimplify(c_) for c_ in vec] for vec in kernel],
        [sub_row(U1_A), sub_row(v)],
        [sub_row(Y2), sub_row(x)],
        [sub_row(Y3), sub_row(U3_B)],
    ]
    T = {}
    for bits in itertools.product((0, 1), repeat=4):
        rows_sel = tuple(tuple(planes[m][bits[m]]) for m in range(4))
        T[bits] = perm4(rows_sel)
    assert any(value != 0 for value in T.values())
    for left, right in (((0, 1), (2, 3)), ((0, 2), (1, 3)),
                        ((0, 3), (1, 2))):
        m = sp.zeros(4, 4)
        for bits in itertools.product((0, 1), repeat=4):
            r_ = 2 * bits[left[0]] + bits[left[1]]
            c_ = 2 * bits[right[0]] + bits[right[1]]
            m[r_, c_] = T[bits]
        assert m.rank() == 1
    profile = []
    relations = []
    for a_, b_ in itertools.combinations(range(4), 2):
        rows_ = []
        for pa in planes[a_]:
            for pb in planes[b_]:
                prod = rmul(pa, pb)
                rows_.append([prod[ab] for ab in COORD_PAIRS])
        mm = sp.Matrix(rows_)
        r = mm.rank()
        profile.append(r)
        if r == 3:
            k = [sp.simplify(c_) for c_ in mm.T.nullspace()[0]]
            M2 = sp.Matrix([[k[0], k[1]], [k[2], k[3]]])
            relations.append(((a_, b_), M2.rank()))
    return tuple(profile), tuple(relations)


def sheet_and_deep_stratum():
    # sheet v3=-v2, sub-pivot columns (0,2)
    M = covector_matrix().subs({v[3]: -v[2]})
    M = sp.Matrix([[sp.expand(e) for e in row] for row in M.tolist()])
    piv = sp.expand(M[0, 0] * M[1, 2] - M[0, 2] * M[1, 0])
    G4 = sp.expand(F4.subs({v[3]: -v[2]}))
    quotient = sp.simplify(piv / (v[1] * G4))
    assert quotient.is_Rational and quotient != 0
    # deep stratum: additionally G4=0 via x0
    x0_val = -(d * v[0] * x[1] + v[1] * (x[2] + x[3])) / (d * v[1])
    deep = covector_matrix().subs({v[3]: -v[2], x[0]: x0_val})
    deep = sp.Matrix([[sp.cancel(e) for e in row]
                      for row in deep.tolist()])
    assert deep.rank() == 1
    # first-component embedding
    l_, i_ = sp.symbols("l i")
    fam = {d: i_, v[0]: l_, v[1]: 1, v[2]: -i_ * l_, v[3]: i_ * l_,
           x[0]: 0, x[1]: 1, x[2]: 0, x[3]: -i_ * l_}
    assert sp.simplify((v[2] + v[3]).subs(fam)) == 0
    assert sp.simplify(F4.subs(fam)) == 0
    assert sp.simplify(F1.subs(fam)) == 0


def main() -> None:
    note_text = " ".join(NOTE.read_text(encoding="utf-8").split())
    assert "not a component theorem" in note_text
    assert "matches no recorded component profile" in note_text

    M = covector_matrix()
    det, pivot = cramer_identity(M)
    content = factor_in_singular(det)
    sheet_and_deep_stratum()

    branch_results = {}
    for label, point in SAMPLES.items():
        expr = {"F1": F1, "F2": F2, "F4": F4}[label]
        subs = {**dict(zip(v, point["v"])),
                **dict(zip(x, point["x"])), d: point["d"]}
        assert sp.simplify(expr.subs(subs)) == 0
        assert sp.simplify(((v[2]+v[3]) * F3).subs(subs)) != 0
        others = [e for lab, e in
                  (("F1", F1), ("F2", F2), ("F4", F4)) if lab != label]
        assert all(sp.simplify(e.subs(subs)) != 0 for e in others)
        profile, relations = analyse_point(point)
        assert profile == point["profile"], (label, profile)
        assert relations == point["relations"], (label, relations)
        branch_results[label] = {
            "profile": list(profile),
            "rank3_relations": [
                [list(edge), rank] for edge, rank in relations
            ],
        }

    result = {
        "verified": True,
        "checkpoint_only": True,
        "chart": "in-out path, overlap-one supports",
        "active_determinant_content": content,
        "open_chart_pure_locus": "F1*F2*F4=0",
        "sheet_v2_plus_v3": "pure locus restricts to F1*F2=0",
        "deep_stratum_rank_drop": True,
        "first_component_embeds_in_deep_stratum": True,
        "branches": branch_results,
        "f4_profile_matches_no_recorded_component": True,
        "component_classification_completed": False,
        "component_exhaustiveness_resolved": False,
        "global_problem_resolved": False,
        "note": {"path": NOTE.name, "sha256": sha256(NOTE)},
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        ROOT / "tmp" / "p4_inout_path_stratum_working_note_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
