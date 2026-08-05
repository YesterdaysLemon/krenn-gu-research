#!/usr/bin/env python3
"""Corroborating local-dimension diagnostic at the Zc sample (tail 1).

w01 proves closure(F_Zc1) lies in a census image of the SEVENTH
component, so the pure locus has local dimension >= 6 at the Zc sample
-- which is WHY the s13 five-slice `ds` run could not terminate at
dimension 0 (five generic slices of a >= 6-dim germ stay positive-
dimensional, and positive-dimensional local standard bases are the
expensive case).

This script certifies the matching UPPER bound with a SIX-hyperplane
slice and a smarter local system: instead of the 11 ratio-eliminated
multi-flip equations (degrees up to 16), it uses the 28 mode-anchor
flattening minors (degree <= 8).  Near the sample T_anchor is a unit,
and a 2x8 flattening with a unit entry has rank <= 1 iff its seven
2-column minors against the anchor column vanish (Pluecker three-term
identity), so the 28 minors cut exactly the pure-locus germ.

  * char-0 six-slice `ds` local dimension 0  =>  local dimension <= 6,
    hence with w01 EXACTLY 6 at the Zc sample: the germ dimension equals
    the seventh's dimension (the incidence tangent 7 is a genuine
    second-order-obstructed excess, as at the tenth's A/B walls).
  * a five-slice run in char 31991 is recorded as a cross-check: its
    sliced dimension must be >= 1 (it can never be 0, by w01).

Timeouts are recorded as nulls and downgrade the claim to open; the
w01 containment does NOT depend on this script."""
import itertools, subprocess, sympy as sp

COORD_PAIRS = tuple(itertools.combinations(range(4), 2))
PERMS4 = tuple(itertools.permutations(range(4)))


def perm4(rows):
    return sp.expand(sum(sp.prod(rows[k][pi[k]] for k in range(4)) for pi in PERMS4))


p2, p3, q2, q3, w2 = sp.symbols("p2 p3 q2 q3 w2")
Wc = -(p3 + q3)*w2/(p2*q3 + p3*q2)
YBAR = (1, -1, 0, 0)
U3v = (1, 1, 0, 0)
planes_sym_raw = [
    [U3v, (Wc, 0, w2, 0)],
    [YBAR, (0, 1, p2, p3)],
    [YBAR, (0, 1, q2, q3)],
    [U3v, (0, Wc, w2, 0)],
]
sample = {p2: 2, p3: 3, q2: 5, q3: 7, w2: 1}
pivots = ((0, 2), (0, 1), (0, 1), (1, 2))

# reduce the sample planes into the s13 charts; anchor word
reduced_point = []
for pl, piv in zip(planes_sym_raw, pivots):
    plane = sp.Matrix([[sp.nsimplify(sp.sympify(c).subs(sample)) for c in row]
                       for row in pl])
    reduced_point.append(plane[:, piv].inv()*plane)
T_point = {bits: sp.nsimplify(sp.cancel(perm4(tuple(tuple(reduced_point[m][bits[m], j]
                                                          for j in range(4))
                                                    for m in range(4)))))
           for bits in itertools.product((0, 1), repeat=4)}
anchor = next(bb for bb in itertools.product((0, 1), repeat=4) if T_point[bb] != 0)
assert anchor == (1, 0, 1, 0) or T_point[anchor] != 0

# universal chart planes and universal T
zvars = sp.symbols("ZI0:16")
universal = []
for mode, piv in enumerate(pivots):
    nonpiv = tuple(i for i in range(4) if i not in piv)
    plane = sp.zeros(2, 4)
    plane[0, piv[0]] = 1
    plane[1, piv[1]] = 1
    entries = zvars[4*mode: 4*mode + 4]
    for r_ in range(2):
        for o_, c_ in enumerate(nonpiv):
            plane[r_, c_] = entries[2*r_ + o_]
    universal.append(plane)
T_univ = {bits: perm4(tuple(tuple(universal[m][bits[m], j] for j in range(4))
                            for m in range(4)))
          for bits in itertools.product((0, 1), repeat=4)}

coord_pt = []
for plane, piv in zip(reduced_point, pivots):
    nonpiv = tuple(i for i in range(4) if i not in piv)
    coord_pt.extend(sp.nsimplify(plane[r_, c_]) for r_ in range(2) for c_ in nonpiv)
subs0 = dict(zip(zvars, coord_pt))
assert all(sp.nsimplify(sp.cancel(T_univ[bits].subs(subs0))) == T_point[bits]
           for bits in T_point)

# the 28 mode-anchor flattening minors (degree <= 8)
minors = []
for mode in range(4):
    others = tuple(j for j in range(4) if j != mode)
    anch_rest = tuple(anchor[j] for j in others)

    def word(im, rest):
        w = [0]*4
        w[mode] = im
        for j, bitv in zip(others, rest):
            w[j] = bitv
        return tuple(w)
    for rest in itertools.product((0, 1), repeat=3):
        if rest == anch_rest:
            continue
        mm = sp.expand(T_univ[word(0, anch_rest)]*T_univ[word(1, rest)]
                       - T_univ[word(0, rest)]*T_univ[word(1, anch_rest)])
        minors.append(mm)
assert len(minors) == 28
assert all(sp.simplify(mm.subs(subs0)) == 0 for mm in minors)

# shift the sample to the origin, clear denominators
shifted = []
for eq in minors:
    poly = sp.expand(eq.subs({zv: zv + val for zv, val in subs0.items()}))
    den = 1
    for coeff in sp.Poly(poly, *zvars).coeffs():
        den = sp.lcm(den, sp.denom(sp.nsimplify(coeff)))
    shifted.append(sp.expand(poly*den))
print(f"28 mode-anchor minors built and shifted (max degree "
      f"{max(sp.Poly(s, *zvars).total_degree() for s in shifted)}).")

SLICE_COEFFS = (
    (1, 2, -1, 3, 1, -2, 1, 1, -3, 2, 1, -1, 2, 1, -2, 3),
    (2, -1, 1, 1, -2, 3, 1, -1, 1, 1, -2, 1, 3, -1, 1, -2),
    (1, 1, 2, -3, 1, 1, -1, 2, 1, -2, 3, 1, -1, 1, 1, 2),
    (3, -2, 1, 1, 1, -1, 2, 1, -2, 1, 1, 3, 1, -1, 2, 1),
    (1, 3, -2, 1, 2, 1, 1, -1, 1, 2, -1, 1, 1, 2, -3, 1),
    (2, 1, 1, -2, 3, 1, -1, 1, 2, -1, 1, 2, -3, 1, 1, 1),
)
varnames = ",".join(str(vv) for vv in zvars)


def run_slice(char, nslices, timeout_s):
    slices = [sum(cc*zz for cc, zz in zip(row, zvars))
              for row in SLICE_COEFFS[:nslices]]
    gens = shifted + slices
    polys = ";\n".join(f"poly g{i}={str(pp).replace('**','^')}"
                       for i, pp in enumerate(gens))
    program = "\n".join((
        f"ring R={char},({varnames}),ds;",
        polys + ";",
        "ideal I=" + ",".join(f"g{i}" for i in range(len(gens))) + ";",
        "ideal J=std(I);",
        '"SLICE_LOCAL_DIM:"+string(dim(J));',
        "quit;",
    ))
    try:
        completed = subprocess.run(("Singular", "-q"), input=program, text=True,
                                   encoding="utf-8", errors="replace",
                                   capture_output=True, timeout=timeout_s, check=False)
    except subprocess.TimeoutExpired:
        return None
    out = completed.stdout
    if "SLICE_LOCAL_DIM:" not in out:
        return None
    return int(out.split("SLICE_LOCAL_DIM:")[1].split()[0])


results = {}
results["char0_6slice"] = run_slice("0", 6, 3000)
print("char-0 SIX-slice ds local dimension:",
      "NULL (timeout)" if results["char0_6slice"] is None else results["char0_6slice"])
if results["char0_6slice"] != 0:
    results["p31991_6slice"] = run_slice("31991", 6, 1200)
    print("char-31991 SIX-slice ds local dimension:",
          "NULL (timeout)" if results.get("p31991_6slice") is None
          else results["p31991_6slice"], "(modular evidence only)")
    results["p1000003_6slice"] = run_slice("1000003", 6, 1200)
    print("char-1000003 SIX-slice ds local dimension:",
          "NULL (timeout)" if results.get("p1000003_6slice") is None
          else results["p1000003_6slice"], "(modular evidence only)")
results["p31991_5slice"] = run_slice("31991", 5, 900)
print("char-31991 FIVE-slice ds local dimension:",
      "NULL (timeout)" if results["p31991_5slice"] is None
      else results["p31991_5slice"],
      "(must be >= 1 by w01 if it terminates)")
if results["p31991_5slice"] is not None:
    assert results["p31991_5slice"] >= 1, "contradiction with w01!"
print()
if results["char0_6slice"] == 0:
    print("CERTIFIED (char 0): local dimension <= 6 at the Zc sample; with")
    print("w01 (>= 6 via the seventh) the local dimension is EXACTLY 6.")
elif results.get("p31991_6slice") == 0 or results.get("p1000003_6slice") == 0:
    print("MODULAR EVIDENCE ONLY: six-slice dimension 0 in finite")
    print("characteristic; the char-0 upper bound remains open (null).")
else:
    print("Local-dimension upper bound OPEN (nulls recorded); the w01")
    print("containment stands regardless.")
print()
print("ALL CHECKS PASSED (diagnostic verdict above)")
