#!/usr/bin/env python3
"""Verify the single-word quadrilateral thirteenth pure-P4 component (F13).

Consolidates the discovery snapshot's certificates (scripts s03/s04/
s08/s07 of research_snapshots/2026-08-04-p4-exhaustiveness-sweep-
census-thirteen) into one fail-closed replay:

  * the coincident-support (Z-a) gauge: the case-Z covector matrix
    M_Z has rank two identically with forced kernel plane
    span(u3, zeta_W), whose Pi-shadow is the B-conjugate of the
    U3 shadow; the free-W restriction is the four-word mode-{1,2}
    slice whose three non-anchor words all carry the branch tie
    g = 2Wbek + (b+e)(k w2 - w3) as a factor, and whose purity
    determinant factors into the three Za branches;
  * identical SINGLE-WORD purity of the tied family
    (T_0110 = -4bek), the kernels, the torus monomial scaling, and
    the exact subtorus reparametrization;
  * family tangent rank FIVE at the generic sample (eight parameter
    directions including the full projective source torus; the five
    chart parameters alone give rank four -- the (w2:w3)
    projective redundancy);
  * universal Segre-incidence Jacobian rank FOURTEEN at the sample
    (tangent dimension six: a singular incidence point), plus the
    transverse tangent direction being second-order obstructed
    (rank [J|c2] = 15);
  * the characteristic-zero slice certificate: the eleven
    ratio-eliminated multi-flip purity equations, shifted so the
    sample is the origin, cut by five fixed integer hyperplanes,
    have a Singular `ds` standard basis of local dimension ZERO --
    with the rank-five family tangent this pins the pure locus's
    local dimension at the sample to exactly five (Krull height
    bound, valid for any five forms);
  * distinctness from the twelve other certified orbits: dimension
    against the three sixfolds (with the tenth's closed triple-span
    invariant replayed as the sieve refinement), the closure-wide
    rank-sum bound 19 (all 4x4 pair minors vanish identically at
    the five rank-three edges) against the eight rank-sum-21
    fivefold samples (each re-verified), and the closed
    symmetry-stable split-plane invariant against the twelfth
    (whose family membership in the invariant set is verified
    identically);
  * generic geometry: the four rank-one relations (the u3.ybar
    quadrilateral) with orientation indegrees (0,2,2,0), the
    irreducible {12}-edge relation, no kernel-kernel relation, the
    two exact self-symmetries (including diag(1,1,1,-1), which
    PRESERVES the branch invariant Q -- the corrected reading of
    the first draft's wrong mirror claim), and the corrected
    mirror identification Za3 = (01)-source swap of F13 at the
    same parameters.

Everything is exact (sympy rationals; one Singular `ds` standard
basis over Q, run fail-closed via subprocess with a hard timeout).
"""

from __future__ import annotations

import hashlib
import itertools
import json
import subprocess
import time
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P4_SINGLE_WORD_QUADRILATERAL_PURE_COMPONENT.md"
SNAPSHOT_README = (
    ROOT
    / "research_snapshots"
    / "2026-08-04-p4-exhaustiveness-sweep-census-thirteen"
    / "README.md"
)

WORDS = tuple(itertools.product((0, 1), repeat=4))
PAIRS = tuple(itertools.combinations(range(4), 2))
PERMS4 = tuple(itertools.permutations(range(4)))
FLATTENINGS = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))
PIVOTS = ((0, 2), (0, 1), (0, 1), (0, 2))
COMPLEMENTARY_SPLITS = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))

YBAR = (1, -1, 0, 0)
U3ROW = (1, 1, 0, 0)

SAMPLE_VALUES = {
    "b": 2, "e": 3, "k": 5, "w2": 1, "w3": 7, "t0": 1, "t1": 1, "t2": 1,
}
EXPECTED_W = sp.Rational(1, 6)
EXPECTED_ZETA = (60, 0, -60, 420)
EXPECTED_COORDINATE_POINT = (
    1, 0, 1, -7,
    2, -10, 2, -10,
    3, -15, 3, -15,
    1, 0, sp.Rational(1, 6), 7,
)
RANK3_EDGES = ((0, 1), (0, 2), (1, 2), (1, 3), (2, 3))
EXPECTED_PROFILE = (3, 3, 4, 3, 3, 3)
FAMILY_MINOR_ROWS = (0, 2, 3, 4, 5)
FAMILY_MINOR_COLUMNS = (0, 1, 2, 3, 5)
EXPECTED_FAMILY_MINOR = sp.Rational(28, 15)
INCIDENCE_ANCHOR = (0, 0, 0, 0)
EXPECTED_ANCHOR_VALUE = sp.Integer(-120)
EXPECTED_RATIOS = (1, 1, 1, 0)
INCIDENCE_MINOR_ROWS = (0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14)
INCIDENCE_MINOR_COLUMNS = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 13, 17, 19)
EXPECTED_INCIDENCE_MINOR = sp.Integer(189665280000)
SLICE_COEFFS = (
    (1, 2, -1, 3, 1, -2, 1, 1, -3, 2, 1, -1, 2, 1, -2, 3),
    (2, -1, 1, 1, -2, 3, 1, -1, 1, 1, -2, 1, 3, -1, 1, -2),
    (1, 1, 2, -3, 1, 1, -1, 2, 1, -2, 3, 1, -1, 1, 1, 2),
    (3, -2, 1, 1, 1, -1, 2, 1, -2, 1, 1, 3, 1, -1, 2, 1),
    (1, 3, -2, 1, 2, 1, 1, -1, 1, 2, -1, 1, 1, 2, -3, 1),
)
SINGULAR_TIMEOUT = 3600


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalized(text: str) -> str:
    return " ".join(text.split())


def rmul(left, right):
    """Squarefree-algebra product of two degree-one rows (six coords)."""
    return tuple(
        sp.expand(left[a] * right[b] + left[b] * right[a])
        for a, b in PAIRS
    )


def perm4(rows):
    return sp.expand(
        sum(sp.prod(rows[k][pi[k]] for k in range(4)) for pi in PERMS4)
    )


def coefficients(planes):
    return {
        word: sp.cancel(
            sp.together(
                perm4(
                    tuple(
                        tuple(planes[mode].row(word[mode]))
                        for mode in range(4)
                    )
                )
            )
        )
        for word in WORDS
    }


def zeta_of(b, e, k, w2, w3):
    return (
        (b + e) * (k * w2 + w3), 0, -2 * b * e * k * w2, 2 * b * e * k * w3,
    )


def family(b, e, k, w2, w3, scales=(1, 1, 1)):
    """The F13 planes (branch tie solved for W), torus-scaled."""
    W = -(b + e) * (k * w2 - w3) / (2 * b * e * k)
    raw = (
        sp.Matrix((U3ROW, zeta_of(b, e, k, w2, w3))),
        sp.Matrix((YBAR, (0, 1, b, -b * k))),
        sp.Matrix((YBAR, (0, 1, e, -e * k))),
        sp.Matrix((U3ROW, (0, W, w2, w3))),
    )
    source = sp.diag(*scales, 1)
    return tuple(plane * source for plane in raw)


def flattening_minors(tensor):
    minors = []
    for left, right in FLATTENINGS:
        table = {}
        for word in WORDS:
            row = (word[left[0]], word[left[1]])
            column = (word[right[0]], word[right[1]])
            table[(row, column)] = tensor[word]
        row_keys = sorted({key[0] for key in table})
        column_keys = sorted({key[1] for key in table})
        for r1, r2 in itertools.combinations(row_keys, 2):
            for k1, k2 in itertools.combinations(column_keys, 2):
                minors.append(
                    sp.cancel(
                        sp.together(
                            table[(r1, k1)] * table[(r2, k2)]
                            - table[(r1, k2)] * table[(r2, k1)]
                        )
                    )
                )
    return minors


def assert_flattening_minors_vanish(tensor):
    for minor in flattening_minors(tensor):
        assert sp.simplify(minor) == 0, minor


def reduce_in_charts(planes):
    reduced = []
    coordinates = []
    for plane, pivots in zip(planes, PIVOTS, strict=True):
        chart = sp.simplify(plane[:, pivots].inv() * plane)
        nonpivots = tuple(i for i in range(4) if i not in pivots)
        reduced.append(chart)
        coordinates.extend(
            chart[row, column] for row in range(2) for column in nonpivots
        )
    return tuple(reduced), tuple(coordinates)


def universal_planes(variables):
    result = []
    for mode, pivots in enumerate(PIVOTS):
        nonpivots = tuple(i for i in range(4) if i not in pivots)
        plane = sp.zeros(2, 4)
        plane[0, pivots[0]] = 1
        plane[1, pivots[1]] = 1
        entries = variables[4 * mode: 4 * mode + 4]
        for row in range(2):
            for offset, column in enumerate(nonpivots):
                plane[row, column] = entries[2 * row + offset]
        result.append(plane)
    return tuple(result)


def point_tensor_of(planes):
    return {
        word: sp.nsimplify(
            perm4(tuple(tuple(planes[m].row(word[m])) for m in range(4)))
        )
        for word in WORDS
    }


def mode_kernels(planes, tensor):
    kernels = []
    for mode in range(4):
        flattening = sp.zeros(2, 8)
        for word in WORDS:
            rest = tuple(word[j] for j in range(4) if j != mode)
            flattening[word[mode], rest[0] * 4 + rest[1] * 2 + rest[2]] = (
                tensor[word]
            )
        assert flattening.rank() == 1
        left = sp.Matrix(flattening.T).nullspace()
        assert len(left) == 1
        combination = left[0]
        kernels.append(
            tuple(
                sp.expand(
                    combination[0] * planes[mode][0, j]
                    + combination[1] * planes[mode][1, j]
                )
                for j in range(4)
            )
        )
    return kernels


def proportional(u, w):
    return sp.Matrix((tuple(u), tuple(w))).rank() == 1


def relation_geometry(planes):
    """Profile, rank-one relations (where the coefficient 2x2 has rank
    one), irreducible relations (rank two), arrows, kernel-kernel."""
    tensor = point_tensor_of(planes)
    assert any(value != 0 for value in tensor.values())
    kernels = mode_kernels(planes, tensor)
    profile = []
    relations = {}
    irreducible = []
    for a, b in PAIRS:
        rows = []
        for i in range(2):
            for j in range(2):
                rows.append(
                    list(rmul(tuple(planes[a].row(i)), tuple(planes[b].row(j))))
                )
        matrix = sp.Matrix(rows)
        rank = matrix.rank()
        profile.append(rank)
        if rank != 3:
            continue
        null = matrix.T.nullspace()
        assert len(null) == 1
        two_by_two = sp.Matrix(2, 2, tuple(null[0]))
        if two_by_two.rank() == 2:
            irreducible.append((a, b))
            continue
        left_combination = (
            two_by_two[:, 0]
            if any(entry != 0 for entry in two_by_two[:, 0])
            else two_by_two[:, 1]
        )
        right_combination = (
            two_by_two[0, :]
            if any(entry != 0 for entry in two_by_two[0, :])
            else two_by_two[1, :]
        ).T
        u_a = tuple(
            sp.expand(
                left_combination[0] * planes[a][0, j]
                + left_combination[1] * planes[a][1, j]
            )
            for j in range(4)
        )
        u_b = tuple(
            sp.expand(
                right_combination[0] * planes[b][0, j]
                + right_combination[1] * planes[b][1, j]
            )
            for j in range(4)
        )
        assert all(value == 0 for value in rmul(u_a, u_b))
        support_a = tuple(j for j in range(4) if sp.simplify(u_a[j]) != 0)
        support_b = tuple(j for j in range(4) if sp.simplify(u_b[j]) != 0)
        in_a = proportional(u_a, kernels[a])
        in_b = proportional(u_b, kernels[b])
        relations[(a, b)] = {
            "supports": (support_a, support_b),
            "kernel_sides": (in_a, in_b),
        }
    kernel_kernel = sorted(
        edge
        for edge, data in relations.items()
        if data["kernel_sides"] == (True, True)
    )
    arrows = sorted(
        (edge[1], edge[0]) if data["kernel_sides"][0] else (edge[0], edge[1])
        for edge, data in relations.items()
        if data["kernel_sides"][0] != data["kernel_sides"][1]
    )
    return (
        tuple(profile), relations, sorted(irreducible), kernel_kernel,
        arrows, kernels,
    )


def meets_coordinate_plane(plane, pair):
    complement = tuple(i for i in range(4) if i not in pair)
    block = sp.Matrix(
        [[plane[r, c] for c in complement] for r in range(2)]
    )
    return block.rank() <= 1


def meets_two_complementary(plane):
    return any(
        meets_coordinate_plane(plane, pair)
        and meets_coordinate_plane(plane, complement)
        for pair, complement in COMPLEMENTARY_SPLITS
    )


def pair_profile(planes):
    profile = []
    for a, b in PAIRS:
        rows = []
        for i in range(2):
            for j in range(2):
                rows.append(
                    list(rmul(tuple(planes[a].row(i)), tuple(planes[b].row(j))))
                )
        profile.append(sp.Matrix(rows).rank())
    return tuple(profile)


def fivefold_samples():
    """The eight documented rank-sum-21 fivefold certificate samples."""
    samples = {}
    samples["first"] = (
        ((1, 0, -1, -2), (0, 1, 1, 0)), ((1, 1, 0, 0), (0, 0, 1, 1)),
        ((0, 1, 0, 1), (-1, 0, 1, 0)), ((1, 0, 1, 0), (0, 0, -1, 1)),
    )
    samples["dq"] = (
        ((2, -1, -1, -2), (1, -1, 1, 1)), ((1, 0, 0, -1), (1, 1, -1, 1)),
        ((3, 1, 1, -1), (0, 1, -1, 0)), ((1, 0, 0, 1), (0, 1, 1, 0)),
    )
    samples["L1"] = (
        ((2, 4, 0, 0), (0, 0, 1, 1)), ((0, 1, -1, 0), (1, 0, 1, 3)),
        ((1, 0, 4, 2), (0, 1, 0, -1)), ((0, 1, 1, 0), (0, 1, 0, 1)),
    )
    samples["L2"] = (
        ((2, 0, 4, 0), (0, 0, 1, 1)), ((0, 1, -1, 0), (1, 0, 1, 3)),
        ((1, 0, 4, 6), (0, 1, 0, -1)), ((0, 1, 1, 0), (0, 1, 0, 1)),
    )
    samples["L3"] = (
        ((2, 10, -8, 0), (0, 0, 1, 1)), ((0, 1, -1, 0), (1, 0, 1, 2)),
        ((1, 0, 3, -6), (0, 1, 0, -1)), ((0, 1, 1, 0), (0, 1, 0, 1)),
    )
    dd, pp, qq = 2, 3, 5
    n6 = qq * (dd + pp + qq)
    samples["sixth"] = (
        ((-dd * pp, dd + qq, n6, 0), (dd * pp, -dd - qq, 0, n6)),
        ((0, 0, 1, 1), (-dd, 1, -pp - qq, dd)),
        ((pp, 1, 0, qq), (-1, 0, 1, 0)), ((1, 0, 1, 0), (0, 0, -1, 1)),
    )
    a8 = sp.Integer(-12)
    b8 = sp.Integer(-10)
    f8 = sp.Rational(3, 4)
    ph8 = sp.Rational(-5, 28)
    j8 = f8 + b8 * ph8 ** 2
    kap8 = ph8 * (b8 * f8 + 1)
    eta8 = -(b8 * f8 + 1)
    samples["eighth"] = (
        ((0, 0, 1, -1), (a8 + b8, a8 - b8, 0, 2)),
        ((-a8 * f8 + 1, -a8 * f8 - 1, f8 + ph8, f8 - ph8), (1, 1, 0, 0)),
        ((-a8 * j8 + eta8, -a8 * j8 - eta8, j8 + kap8, j8 - kap8),
         (1, 1, 0, 0)),
        ((1, -1, 0, 0), (0, 0, 1, 1)),
    )
    d9, v90, v91, v92, x91, x92 = 2, 3, 5, 7, 11, -4
    x90 = sp.Rational(-(d9 * v90 * x91 + v91 * x92), d9 * v91)
    c9 = (-d9 * v91, -d9 * v90, v91, v91)
    k19 = (-c9[1], c9[0], 0, 0)
    k29 = (-c9[2], 0, c9[0], 0)
    k39 = (-c9[3], 0, 0, c9[0])
    al9, be9 = sp.Rational(2, 3), sp.Rational(-1, 2)
    samples["ninth"] = (
        (tuple(k19[j] + al9 * k39[j] for j in range(4)),
         tuple(k29[j] + be9 * k39[j] for j in range(4))),
        ((0, 0, 1, -1), (v90, v91, v92, -v92)),
        ((1, 0, -d9, 0), (x90, x91, x92, 0)),
        ((0, 0, 1, 1), (1, 0, d9, 0)),
    )
    return samples


def pluecker(plane):
    return tuple(sp.together(plane[:, pair].det()) for pair in PAIRS)


def same_projective_plane(left, right):
    left_p = pluecker(left)
    right_p = pluecker(right)
    assert any(sp.simplify(value) != 0 for value in left_p)
    assert any(sp.simplify(value) != 0 for value in right_p)
    return all(
        sp.simplify(left_p[i] * right_p[j] - left_p[j] * right_p[i]) == 0
        for i in range(6)
        for j in range(i + 1, 6)
    )


def singular_slice_dimension(shifted, slices, char="0"):
    """Run the Singular ds standard basis, fail-closed; return (dim, s)."""
    zvars = sp.symbols("Z0:16")
    varnames = ",".join(str(z) for z in zvars)
    body = ";\n".join(
        f"poly g{i}={str(polynomial).replace('**', '^')}"
        for i, polynomial in enumerate(tuple(shifted) + tuple(slices))
    )
    program = "\n".join(
        (
            f"ring R={char},({varnames}),ds;",
            body + ";",
            "ideal I="
            + ",".join(f"g{i}" for i in range(len(shifted) + len(slices)))
            + ";",
            "option(redSB);",
            "ideal J=std(I);",
            '"SLICE_LOCAL_DIM:"+string(dim(J));',
            "quit;",
        )
    )
    start = time.time()
    try:
        completed = subprocess.run(
            ("Singular", "-q"),
            input=program,
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            timeout=SINGULAR_TIMEOUT,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise AssertionError(
            "Singular slice run timed out after %ss: dimension recorded as "
            "null, certificate NOT replayed" % SINGULAR_TIMEOUT
        ) from exc
    elapsed = time.time() - start
    assert completed.returncode == 0, (
        completed.returncode,
        completed.stdout[-800:],
        completed.stderr[-800:],
    )
    markers = [
        line
        for line in completed.stdout.splitlines()
        if line.startswith("SLICE_LOCAL_DIM:")
    ]
    assert len(markers) == 1, completed.stdout[-800:]
    return int(markers[0].split(":", 1)[1].strip()), elapsed


def main() -> None:
    started = time.time()

    # ---------------- theorem text (whitespace-normalized) -----------
    theorem_text = normalized(THEOREM.read_text(encoding="utf-8"))
    assert (
        "thirteen component orbits: ten fivefolds and three sixfolds"
        in theorem_text
    )
    assert (
        "singular point of the universal Segre incidence" in theorem_text
    )
    assert "rank sum <= 19 on all of closure(F13)." in theorem_text
    assert "vanishes on every decomposable chart tensor" in theorem_text
    assert "local dimension 0 at the origin." in theorem_text
    assert "T = -4bek * e_0110" in theorem_text
    assert (
        "that reflection is a self-symmetry of each branch" in theorem_text
    )
    assert "This is not a classification." in theorem_text

    b, e, k, w2, w3, W = sp.symbols("b e k w2 w3 W")
    t0, t1, t2 = sp.symbols("t0 t1 t2")
    sample = {
        symbol: sp.Integer(SAMPLE_VALUES[str(symbol)])
        for symbol in (b, e, k, w2, w3, t0, t1, t2)
    }
    W_branch = -(b + e) * (k * w2 - w3) / (2 * b * e * k)
    assert W_branch.subs(sample) == EXPECTED_W

    # ---------------- the free-W chart: forced kernel, one tie -------
    z = sp.symbols("z0:4")
    p_row = (0, 1, b, -b * k)
    q_row = (0, 1, e, -e * k)
    w_row = (0, W, w2, w3)

    def covector_row(rows3):
        form = perm4((tuple(z),) + tuple(rows3))
        return [sp.expand(sp.diff(form, zi)) for zi in z]

    m_z = sp.Matrix(
        [
            covector_row((YBAR, YBAR, w_row)),
            covector_row((YBAR, q_row, w_row)),
            covector_row((p_row, YBAR, w_row)),
        ]
    )
    assert m_z.rank() == 2                       # identically in all params.
    zeta_free = (
        -W * (k * w2 + w3), 0,
        -w2 * (k * w2 - w3), w3 * (k * w2 - w3),
    )
    for vector in (U3ROW, zeta_free):
        assert all(
            sp.expand(sum(m_z[i, j] * vector[j] for j in range(4))) == 0
            for i in range(3)
        ), vector
    # The Pi-shadow of zeta_free lies on (0,0,-w2,w3), the B-conjugate
    # of the U3 shadow (0,0,w2,w3): B(zeta_Pi, w_Pi) = 0 identically.
    assert sp.expand(zeta_free[2] * w_row[3] + zeta_free[3] * w_row[2]) == 0

    free_planes = (
        sp.Matrix((U3ROW, zeta_free)),
        sp.Matrix((YBAR, p_row)),
        sp.Matrix((YBAR, q_row)),
        sp.Matrix((U3ROW, w_row)),
    )
    free_tensor = {
        word: perm4(
            tuple(tuple(free_planes[m].row(word[m])) for m in range(4))
        )
        for word in WORDS
    }
    tie = sp.expand(2 * W * b * e * k + (b + e) * (k * w2 - w3))
    assert sp.expand(free_tensor[(0, 1, 1, 0)] + 4 * b * e * k) == 0
    assert sp.expand(free_tensor[(0, 1, 1, 1)] + tie) == 0
    assert sp.expand(
        free_tensor[(1, 1, 1, 0)] - (k * w2 + w3) * tie
    ) == 0
    assert sp.expand(
        free_tensor[(1, 1, 1, 1)] - W * (k * w2 + w3) * tie
    ) == 0
    for word in WORDS:
        if word[1] == 1 and word[2] == 1:
            continue
        assert sp.expand(free_tensor[word]) == 0, word
    # Purity of the slice is its 2x2 determinant: the three Za branches.
    slice_det = sp.expand(
        free_tensor[(0, 1, 1, 0)] * free_tensor[(1, 1, 1, 1)]
        - free_tensor[(0, 1, 1, 1)] * free_tensor[(1, 1, 1, 0)]
    )
    za3_tie = sp.expand((b + e) * (k * w2 - w3) - 2 * W * b * e * k)
    assert sp.expand(
        slice_det - (k * w2 + w3) * tie * za3_tie
    ) == 0
    # The anchor word is 2*B(p,q).
    assert sp.expand(
        free_tensor[(0, 1, 1, 0)]
        - 2 * (p_row[2] * q_row[3] + p_row[3] * q_row[2])
    ) == 0

    # ---------------- the tied family: identical single word ---------
    planes = family(b, e, k, w2, w3)
    assert all(plane.rank() == 2 for plane in planes)
    # zeta is the cleared branch value of zeta_free.
    zeta = zeta_of(b, e, k, w2, w3)
    zeta_branch = [
        sp.cancel(sp.together(sp.sympify(value).subs(W, W_branch)))
        for value in zeta_free
    ]
    stack = sp.Matrix((zeta_branch, list(zeta)))
    assert all(
        sp.cancel(stack[0, i] * stack[1, j] - stack[0, j] * stack[1, i]) == 0
        for i in range(4)
        for j in range(4)
    )
    tensor = coefficients(planes)
    assert sp.expand(tensor[(0, 1, 1, 0)] + 4 * b * e * k) == 0
    assert all(
        sp.simplify(value) == 0
        for word, value in tensor.items()
        if word != (0, 1, 1, 0)
    )
    assert_flattening_minors_vanish(tensor)

    # Kernels (10): the four unused rows.
    generic_kernels = mode_kernels(planes, tensor)
    assert proportional(generic_kernels[0], zeta)
    assert proportional(generic_kernels[1], YBAR)
    assert proportional(generic_kernels[2], YBAR)
    assert proportional(
        generic_kernels[3],
        tuple(sp.together(value) for value in (0, W_branch, w2, w3)),
    )

    # Torus scaling and the subtorus reparametrization.
    scaled = family(b, e, k, w2, w3, (t0, t1, t2))
    scaled_tensor = coefficients(scaled)
    for word in WORDS:
        assert sp.simplify(
            scaled_tensor[word] - t0 * t1 * t2 * tensor[word]
        ) == 0
    t = sp.Symbol("t", nonzero=True)
    subtorus_image = family(b, e, k, w2, w3, (t, t, t2))
    reparametrized = family(
        t2 / t * b, t2 / t * e, k / t2, t2 * w2, w3
    )
    for mode in range(4):
        assert same_projective_plane(
            subtorus_image[mode], reparametrized[mode]
        )

    # ---------------- sample instantiation ---------------------------
    point_planes = tuple(plane.subs(sample) for plane in planes)
    assert all(plane.rank() == 2 for plane in point_planes)
    point_tensor = point_tensor_of(point_planes)
    assert point_tensor[(0, 1, 1, 0)] == EXPECTED_ANCHOR_VALUE
    assert all(
        value == 0
        for word, value in point_tensor.items()
        if word != (0, 1, 1, 0)
    )
    assert tuple(
        sp.nsimplify(value) for value in zeta_of(2, 3, 5, 1, 7)
    ) == EXPECTED_ZETA

    # ---------------- family tangent: rank five ----------------------
    reduced, chart_coordinates = reduce_in_charts(scaled)
    parameters = (b, e, k, w2, w3, t0, t1, t2)
    family_tangent = (
        sp.Matrix(chart_coordinates).jacobian(parameters).subs(sample)
    )
    family_tangent = sp.Matrix(
        [
            [sp.nsimplify(sp.cancel(entry)) for entry in row]
            for row in family_tangent.tolist()
        ]
    )
    assert family_tangent.rank() == 5
    assert family_tangent[:, :5].rank() == 4     # (w2:w3) redundancy.
    family_minor = family_tangent.extract(
        FAMILY_MINOR_ROWS, FAMILY_MINOR_COLUMNS
    ).det()
    assert family_minor == EXPECTED_FAMILY_MINOR

    # ---------------- incidence Jacobian: rank FOURTEEN --------------
    coordinate_point = tuple(
        sp.nsimplify(sp.cancel(value.subs(sample)))
        for value in chart_coordinates
    )
    assert coordinate_point == EXPECTED_COORDINATE_POINT
    plane_variables = sp.symbols("Z0:16")
    target_variables = sp.symbols("R0:4")
    universal = universal_planes(plane_variables)
    universal_tensor = {
        word: perm4(
            tuple(tuple(universal[m].row(word[m])) for m in range(4))
        )
        for word in WORDS
    }
    reduced_point = tuple(plane.subs(sample) for plane in reduced)
    chart_tensor = point_tensor_of(reduced_point)
    # The chart tensor is the full bit3=0 cube at the constant -120.
    for word in WORDS:
        expected = 0 if word[3] == 1 else -120
        assert chart_tensor[word] == expected, word
    assert chart_tensor[INCIDENCE_ANCHOR] == EXPECTED_ANCHOR_VALUE
    ratios = tuple(
        sp.nsimplify(
            chart_tensor[
                tuple(
                    (1 - INCIDENCE_ANCHOR[m] if m == mode
                     else INCIDENCE_ANCHOR[m])
                    for m in range(4)
                )
            ]
            / chart_tensor[INCIDENCE_ANCHOR]
        )
        for mode in range(4)
    )
    assert ratios == EXPECTED_RATIOS
    incidence_equations = []
    for word in WORDS:
        if word == INCIDENCE_ANCHOR:
            continue
        monomial = sp.prod(
            target_variables[mode]
            for mode in range(4)
            if word[mode] != INCIDENCE_ANCHOR[mode]
        )
        incidence_equations.append(
            sp.expand(
                universal_tensor[word]
                - universal_tensor[INCIDENCE_ANCHOR] * monomial
            )
        )
    all_variables = (*plane_variables, *target_variables)
    incidence_point = coordinate_point + ratios
    substitution = dict(zip(all_variables, incidence_point, strict=True))
    assert all(
        equation.subs(substitution) == 0 for equation in incidence_equations
    )
    incidence_jacobian = (
        sp.Matrix(incidence_equations)
        .jacobian(all_variables)
        .subs(substitution)
    )
    incidence_rank = incidence_jacobian.rank()
    assert incidence_rank == 14          # NOT fifteen: tangent dim six.
    incidence_minor = incidence_jacobian.extract(
        INCIDENCE_MINOR_ROWS, INCIDENCE_MINOR_COLUMNS
    ).det()
    assert incidence_minor == EXPECTED_INCIDENCE_MINOR
    incidence_tangent_dimension = 20 - incidence_rank
    assert incidence_tangent_dimension == 6

    # The transverse tangent direction is second-order obstructed.
    null_vectors = incidence_jacobian.nullspace()
    assert len(null_vectors) == 6
    ratio_symbols = []
    for mode in range(4):
        flipped = tuple(
            (1 - INCIDENCE_ANCHOR[m] if m == mode else INCIDENCE_ANCHOR[m])
            for m in range(4)
        )
        symbolic_tensor = {
            word: perm4(
                tuple(tuple(reduced[m].row(word[m])) for m in range(4))
            )
            for word in (flipped, INCIDENCE_ANCHOR)
        }
        ratio_symbols.append(
            sp.cancel(
                symbolic_tensor[flipped] / symbolic_tensor[INCIDENCE_ANCHOR]
            )
        )
    full_symbolic = list(chart_coordinates) + ratio_symbols
    family_tangent_20 = (
        sp.Matrix(full_symbolic).jacobian(parameters).subs(sample)
    )
    family_tangent_20 = sp.Matrix(
        [
            [sp.nsimplify(sp.cancel(entry)) for entry in row]
            for row in family_tangent_20.tolist()
        ]
    )
    assert family_tangent_20.rank() == 5
    transverse = None
    for vector in null_vectors:
        if sp.Matrix.hstack(family_tangent_20, vector).rank() > 5:
            transverse = vector
            break
    assert transverse is not None
    eps = sp.Symbol("eps")
    shift = {
        variable: substitution[variable] + eps * transverse[index]
        for index, variable in enumerate(all_variables)
    }
    second_order = []
    for equation in incidence_equations:
        polynomial = sp.Poly(sp.expand(equation.subs(shift)), eps)
        assert polynomial.coeff_monomial(1) == 0
        assert polynomial.coeff_monomial(eps) == 0
        second_order.append(
            sp.nsimplify(polynomial.coeff_monomial(eps ** 2))
        )
    obstruction_rank = sp.Matrix.hstack(
        incidence_jacobian, sp.Matrix(second_order)
    ).rank()
    assert obstruction_rank == 15

    # ---------------- the char-0 slice certificate -------------------
    slice_equations = []
    for word in WORDS:
        flips = [m for m in range(4) if word[m] != INCIDENCE_ANCHOR[m]]
        if len(flips) < 2:
            continue
        lhs = sp.expand(
            universal_tensor[word]
            * universal_tensor[INCIDENCE_ANCHOR] ** (len(flips) - 1)
        )
        rhs = sp.prod(
            universal_tensor[
                tuple(
                    (1 - INCIDENCE_ANCHOR[i] if i == m
                     else INCIDENCE_ANCHOR[i])
                    for i in range(4)
                )
            ]
            for m in flips
        )
        slice_equations.append(sp.expand(lhs - sp.expand(rhs)))
    assert len(slice_equations) == 11
    origin_substitution = dict(zip(plane_variables, coordinate_point))
    assert all(
        sp.simplify(equation.subs(origin_substitution)) == 0
        for equation in slice_equations
    )
    shifted = []
    for equation in slice_equations:
        polynomial = sp.expand(
            equation.subs(
                {z_: z_ + value for z_, value in origin_substitution.items()}
            )
        )
        denominator = sp.Integer(1)
        for coefficient in sp.Poly(polynomial, *plane_variables).coeffs():
            denominator = sp.lcm(
                denominator, sp.denom(sp.nsimplify(coefficient))
            )
        cleared = sp.expand(polynomial * denominator)
        assert all(
            sp.sympify(coefficient).is_integer
            for coefficient in sp.Poly(cleared, *plane_variables).coeffs()
        )
        shifted.append(cleared)
    slices = [
        sum(
            coefficient * z_
            for coefficient, z_ in zip(row, plane_variables, strict=True)
        )
        for row in SLICE_COEFFS
    ]
    slice_dimension, singular_seconds = singular_slice_dimension(
        shifted, slices, "0"
    )
    assert slice_dimension == 0
    # Krull height bound: dim_0(V) <= 0 + 5; family tangent rank five
    # gives >= 5; the local dimension of the pure locus at the sample
    # is EXACTLY five, so closure(F13) is an irreducible component.
    local_dimension = 5

    # ---------------- distinctness -----------------------------------
    # (a) Sample profile (3,3,4,3,3,3), sum 19; the identical vanishing
    # of ALL 4x4 pair minors at the five rank-3 edges bounds the whole
    # closure by <= 19.
    sample_profile = pair_profile(point_planes)
    assert sample_profile == EXPECTED_PROFILE
    assert sum(sample_profile) == 19
    symbolic_profile = []
    for a, b_ in PAIRS:
        rows = []
        for i in range(2):
            for j in range(2):
                rows.append(
                    [
                        sp.together(value)
                        for value in rmul(
                            tuple(planes[a].row(i)), tuple(planes[b_].row(j))
                        )
                    ]
                )
        matrix = sp.Matrix(rows)
        if (a, b_) in RANK3_EDGES:
            for rr in itertools.combinations(range(4), 4):
                for cc in itertools.combinations(range(6), 4):
                    assert sp.simplify(matrix[rr, cc].det()) == 0, (
                        (a, b_), rr, cc,
                    )
        symbolic_profile.append(matrix.rank())
    assert tuple(symbolic_profile) == EXPECTED_PROFILE

    # (b) The eight fivefold samples all have pair-rank sum 21 > 19.
    fivefold_rank_sums = {}
    for name, rows in fivefold_samples().items():
        matrices = tuple(sp.Matrix(pair) for pair in rows)
        profile = pair_profile(matrices)
        fivefold_rank_sums[name] = int(sum(profile))
        assert sum(profile) == 21, (name, profile)
    assert len(fivefold_rank_sums) == 8

    # (c) The tenth's closed triple-span invariant (sieve refinement):
    # dim(U_0+U_1+U_3) <= 3 identically on the tenth's family, while
    # every mode triple at the F13 sample spans C^4.
    bt, et, kt, mt, rt = sp.symbols("bt et kt mt rt")
    tenth_family = (
        ((1, -1, 0, 0), (0, 1, bt, -bt * kt)),
        ((1, -1, 0, 0), (0, 1, et, -et * kt)),
        ((1, 1, 0, 0), (0, 0, 1, kt)),
        ((1, mt, 0, 0), (0, rt, 1, -kt)),
    )
    tenth_stack = sp.Matrix(
        [list(row) for mode in (0, 1, 3) for row in tenth_family[mode]]
    )
    for rows in itertools.combinations(range(6), 4):
        assert sp.expand(tenth_stack[rows, :].det()) == 0
    for triple in itertools.combinations(range(4), 3):
        stack6 = sp.Matrix.vstack(
            *[point_planes[mode] for mode in triple]
        )
        assert stack6.rank() == 4, triple

    # (d) The split-plane invariant against the twelfth.  The twelfth's
    # family lies in S identically (its U0 contains the P01-line u3 and
    # the Pi-line (0,0,1,-k)); no F13 sample plane meets two
    # complementary coordinate planes.
    ks = sp.Symbol("ks")
    twelfth_u0 = sp.Matrix((U3ROW, (0, 0, 1, -ks)))
    twelfth_u3 = sp.Matrix((U3ROW, (0, 0, 1, ks)))
    for plane in (twelfth_u0, twelfth_u3):
        row0 = tuple(plane.row(0))
        row1 = tuple(plane.row(1))
        assert row0[2] == 0 and row0[3] == 0 and row0 != (0, 0, 0, 0)
        assert row1[0] == 0 and row1[1] == 0 and row1[2] == 1
    for plane in point_planes:
        assert meets_coordinate_plane(plane, (0, 1))
        assert not meets_two_complementary(plane)

    # ---------------- generic geometry -------------------------------
    (
        profile, relations, irreducible, kernel_kernel, arrows, _
    ) = relation_geometry(point_planes)
    assert profile == EXPECTED_PROFILE
    assert sorted(relations) == [(0, 1), (0, 2), (1, 3), (2, 3)]
    assert irreducible == [(1, 2)]
    for edge in ((0, 1), (0, 2), (1, 3), (2, 3)):
        assert relations[edge]["supports"] == ((0, 1), (0, 1))
    assert kernel_kernel == []
    assert arrows == [(0, 1), (0, 2), (3, 1), (3, 2)]
    indegrees = [0, 0, 0, 0]
    for _tail, head in arrows:
        indegrees[head] += 1
    assert indegrees == [0, 2, 2, 0]

    # Self-symmetry: mode-(12) swap composed with b <-> e.
    swapped_parameters = family(e, b, k, w2, w3)
    swapped_tuple = (planes[0], planes[2], planes[1], planes[3])
    for mode in range(4):
        assert same_projective_plane(
            swapped_tuple[mode], swapped_parameters[mode]
        )
    # Self-symmetry: diag(1,1,1,-1) with (k,w3) -> (-k,-w3).  The
    # branch invariant Q is -1 on the family and is PRESERVED by the
    # reflection -- the corrected reading of the wrong mirror claim.
    q_invariant = sp.cancel(
        2 * W_branch * b * e * k / ((b + e) * (k * w2 - w3))
    )
    assert q_invariant == -1
    reflection = sp.diag(1, 1, 1, -1)
    reflected = tuple(plane * reflection for plane in planes)
    reflected_parameters = family(b, e, -k, w2, -w3)
    for mode in range(4):
        assert same_projective_plane(
            reflected[mode], reflected_parameters[mode]
        )
    # The corrected mirror: the (01)-SOURCE swap carries F13 onto the
    # Za3 branch (W -> -W, i.e. Q -> +1) at the SAME parameters.
    W_mirror = -W_branch
    assert sp.cancel(
        2 * W_mirror * b * e * k / ((b + e) * (k * w2 - w3))
    ) == 1
    swap01 = sp.Matrix(((0, 1, 0, 0), (1, 0, 0, 0),
                        (0, 0, 1, 0), (0, 0, 0, 1)))
    image = tuple(plane * swap01 for plane in planes)
    mirror_w_row = (0, W_mirror, w2, w3)
    assert same_projective_plane(image[1], sp.Matrix((YBAR, p_row)))
    assert same_projective_plane(image[2], sp.Matrix((YBAR, q_row)))
    assert same_projective_plane(image[3], sp.Matrix((U3ROW, mirror_w_row)))
    # The image mode-0 plane is the Za3 configuration's forced kernel:
    # its M_Z kills u3 and the image zeta identically, and has rank two
    # at the sample (rank <= 2 identically on the Z-a gauge as above).
    m_z_mirror = sp.Matrix(
        [
            covector_row((YBAR, YBAR, mirror_w_row)),
            covector_row((YBAR, q_row, mirror_w_row)),
            covector_row((p_row, YBAR, mirror_w_row)),
        ]
    )
    image_zeta = tuple(image[0].row(1))
    for vector in (U3ROW, image_zeta):
        assert all(
            sp.simplify(
                sp.together(sum(m_z_mirror[i, j] * vector[j]
                                for j in range(4)))
            ) == 0
            for i in range(3)
        ), vector
    m_z_mirror_sample = sp.Matrix(
        [
            [sp.nsimplify(sp.cancel(entry.subs(sample)))
             for entry in row]
            for row in m_z_mirror.tolist()
        ]
    )
    assert m_z_mirror_sample.rank() == 2
    image_zeta_sample = [
        sp.nsimplify(sp.cancel(sp.sympify(value).subs(sample)))
        for value in image_zeta
    ]
    assert sp.Matrix((list(U3ROW), image_zeta_sample)).rank() == 2

    # ---------------- result -----------------------------------------
    dependencies = {THEOREM.name: sha256(THEOREM)}
    snapshot_hash = (
        sha256(SNAPSHOT_README) if SNAPSHOT_README.exists() else None
    )
    result = {
        "verified": True,
        "field": "C",
        "component": (
            "single-word quadrilateral fivefold (family F13, branch Za2)"
        ),
        "census_position": "thirteenth pure-compression component orbit",
        "method": (
            "identically pure single-word family on the Za2 tie of the "
            "coincident-support chart (forced kernel plane); rank-five "
            "family tangent; rank-fourteen (singular) incidence point "
            "with second-order-obstructed transverse direction; exact "
            "char-0 five-hyperplane slice ds standard basis pinning "
            "local dimension to five"
        ),
        "free_chart_words": {
            "0110": "-4*b*e*k",
            "0111": "-g",
            "1110": "(k*w2 + w3)*g",
            "1111": "W*(k*w2 + w3)*g",
            "g": "2*W*b*e*k + (b + e)*(k*w2 - w3)",
        },
        "purity_determinant_factors": [
            "k*w2 + w3 (Za1: tenth's wall)",
            "g (Za2: this component)",
            "(b + e)*(k*w2 - w3) - 2*W*b*e*k (Za3: mirror)",
        ],
        "tie": "W = -(b + e)*(k*w2 - w3)/(2*b*e*k)",
        "pure_coefficient": {"0110": "-4*b*e*k"},
        "single_word": True,
        "identically_pure": True,
        "forced_kernel_plane": "U0 = ker M_Z = span(u3, zeta)",
        "zeta": "((b+e)(k*w2+w3), 0, -2*b*e*k*w2, 2*b*e*k*w3)",
        "conjugate_shadows": True,
        "torus_scaling": "t0*t1*t2",
        "subtorus_reparametrization": (
            "(b,e,k,w2,w3) -> ((t2/t)b, (t2/t)e, k/t2, t2*w2, w3)"
        ),
        "sample": {key: value for key, value in SAMPLE_VALUES.items()},
        "sample_W": str(EXPECTED_W),
        "sample_zeta": [str(value) for value in EXPECTED_ZETA],
        "Grassmann_pivots": [list(pivots) for pivots in PIVOTS],
        "coordinate_point": [str(value) for value in coordinate_point],
        "family_tangent_rank": 5,
        "family_tangent_rank_parameters_only": 4,
        "family_tangent_minor_rows": list(FAMILY_MINOR_ROWS),
        "family_tangent_minor_columns": list(FAMILY_MINOR_COLUMNS),
        "family_tangent_minor": str(family_minor),
        "incidence_anchor": "0000",
        "incidence_anchor_value": str(EXPECTED_ANCHOR_VALUE),
        "incidence_target_ratios": [str(value) for value in ratios],
        "incidence_jacobian_rank": incidence_rank,
        "incidence_tangent_dimension": incidence_tangent_dimension,
        "incidence_minor_rows": list(INCIDENCE_MINOR_ROWS),
        "incidence_minor_columns": list(INCIDENCE_MINOR_COLUMNS),
        "incidence_minor": str(incidence_minor),
        "singular_incidence_point": True,
        "transverse_direction_first_order_flat": True,
        "transverse_direction_second_order_obstructed": True,
        "obstruction_rank_J_c2": obstruction_rank,
        "slice_certificate": {
            "equations": 11,
            "anchor": "0000",
            "slice_rows": [list(row) for row in SLICE_COEFFS],
            "char": "0",
            "ordering": "ds",
            "local_dimension": slice_dimension,
            "singular_seconds": round(singular_seconds, 2),
            "krull_upper_bound": 5,
        },
        "local_dimension_at_sample": local_dimension,
        "component_dimension": 5,
        "component_rational": True,
        "kernels": ["zeta", "ybar", "ybar", "(0,W,w2,w3)"],
        "pair_profile": list(EXPECTED_PROFILE),
        "rank_sum": 19,
        "closure_rank_sum_bound": 19,
        "rank3_edges_all_4x4_minors_vanish_identically": True,
        "distinct_from_sixfolds_by": (
            "dimension 5 < 6 (tenth also refuted by its triple-span "
            "invariant)"
        ),
        "tenth_triple_span_at_most_3_identically": True,
        "f13_sample_all_triples_span_C4": True,
        "distinct_from_rank21_fivefolds_by": (
            "closure-wide rank-sum bound 19 < 21 (census symmetries "
            "preserve pair-rank sums)"
        ),
        "fivefold_sample_rank_sums": fivefold_rank_sums,
        "distinct_from_twelfth_by": (
            "split-plane invariant: some plane meets two complementary "
            "coordinate planes on all of closure(F12), no plane does at "
            "the F13 sample"
        ),
        "f13_sample_no_split_plane": True,
        "relation_edges": ["01", "02", "13", "23"],
        "relation_supports_all": ["01", "01"],
        "irreducible_relation_edge": "12",
        "rank_four_edge": "03",
        "orientation_arrows": ["0->1", "0->2", "3->1", "3->2"],
        "indegrees": [0, 2, 2, 0],
        "kernel_kernel_generic": False,
        "swap_symmetry": "(12)-mode swap with b <-> e",
        "reflection_symmetry": "diag(1,1,1,-1) with (k,w3) -> (-k,-w3)",
        "branch_invariant_Q": "-1 (preserved by the reflection)",
        "Za3_identification": (
            "(01)-source swap at the SAME parameters (flips Q to +1); "
            "the first-draft diag(1,1,1,-1) mirror claim was wrong"
        ),
        "certified_pure_component_orbit_count": 13,
        "generic_H31_excluded": False,
        "generic_weighted_H22_excluded": False,
        "all_pure_components_classified": False,
        "global_problem_resolved": False,
        "elapsed_seconds": round(time.time() - started, 2),
        "dependencies": dependencies,
        "snapshot_readme_sha256": snapshot_hash,
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        ROOT / "tmp" / "p4_single_word_quadrilateral_pure_component"
                        "_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
