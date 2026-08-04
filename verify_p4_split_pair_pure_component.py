#!/usr/bin/env python3
"""Verify the split-pair twelfth pure-P4 component (family F12).

Consolidates the discovery snapshot's certificates (scripts s03/s04/
s06/s07 of research_snapshots/2026-08-04-p4-exhaustiveness-sweep-
census-thirteen) into one fail-closed replay:

  * the free coincident-support (Z-b) chart: three-word restriction
    with closed forms, thirteen identically vanishing words, the
    three-conjugacy mechanism, and the purity binomial
    T_1110*T_0111 = 0 whose Zb1 branch (the tie) is the family;
  * identical purity of the tied family (two adjacent words), the
    kernels, the torus monomial scaling, and the exact subtorus
    reparametrization;
  * family tangent rank FIVE at the generic sample (seven parameter
    directions including the full projective source torus; the four
    chart parameters alone give rank four);
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
    against the three sixfolds, the closure-wide rank-sum bound 19
    (all 4x4 pair minors vanish identically at the five rank-three
    edges) against the eight rank-sum-21 fivefold samples (each
    re-verified), and the closed symmetry-stable split-plane
    invariant against the thirteenth (whose certificate sample is
    re-grounded here);
  * generic geometry: the five rank-one relations (the u3.ybar
    quadrilateral plus the B-conjugate diagonal), orientation with
    indegrees (0,2,2,1), no kernel-kernel relation, the two exact
    self-symmetries, and Zb2 = (03)-mode swap at k -> -k.

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
THEOREM = ROOT / "P4_SPLIT_PAIR_PURE_COMPONENT.md"
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

SAMPLE_VALUES = {"p2": 3, "p3": -1, "q2": 5, "k": 2, "t0": 1, "t1": 1, "t2": 1}
EXPECTED_Q3 = -15
EXPECTED_COORDINATE_POINT = (
    1, 0, 0, -2,
    3, -1, 3, -1,
    5, -15, 5, -15,
    1, 0, 0, 2,
)
RANK3_EDGES = ((0, 1), (0, 2), (0, 3), (1, 3), (2, 3))
EXPECTED_PROFILE = (3, 3, 3, 4, 3, 3)
FAMILY_MINOR_ROWS = (0, 3, 4, 5, 8)
FAMILY_MINOR_COLUMNS = (0, 1, 2, 3, 4)
EXPECTED_FAMILY_MINOR = sp.Integer(-1)
INCIDENCE_ANCHOR = (0, 0, 0, 0)
EXPECTED_ANCHOR_VALUE = sp.Integer(-100)
EXPECTED_RATIOS = (sp.Rational(8, 25), 1, 1, 0)
INCIDENCE_MINOR_ROWS = (0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14)
INCIDENCE_MINOR_COLUMNS = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 13, 14, 19)
EXPECTED_INCIDENCE_MINOR = sp.Integer(28311552000)
SLICE_COEFFS = (
    (1, 2, -1, 3, 1, -2, 1, 1, -3, 2, 1, -1, 2, 1, -2, 3),
    (2, -1, 1, 1, -2, 3, 1, -1, 1, 1, -2, 1, 3, -1, 1, -2),
    (1, 1, 2, -3, 1, 1, -1, 2, 1, -2, 3, 1, -1, 1, 1, 2),
    (3, -2, 1, 1, 1, -1, 2, 1, -2, 1, 1, 3, 1, -1, 2, 1),
    (1, 3, -2, 1, 2, 1, 1, -1, 1, 2, -1, 1, 1, 2, -3, 1),
)
SINGULAR_TIMEOUT = 3600
THIRTEENTH_SAMPLE = (
    ((1, 1, 0, 0), (1, 0, -1, 7)),
    ((1, -1, 0, 0), (0, 1, 2, -10)),
    ((1, -1, 0, 0), (0, 1, 3, -15)),
    ((1, 1, 0, 0), (0, sp.Rational(1, 6), 1, 7)),
)


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
        word: perm4(
            tuple(tuple(planes[mode].row(word[mode])) for mode in range(4))
        )
        for word in WORDS
    }


def free_planes(p2, p3, q2, q3, k):
    """The Z-b chart BEFORE the tie: q3 an independent parameter."""
    return (
        sp.Matrix((U3ROW, (0, 0, 1, -k))),
        sp.Matrix((YBAR, (0, 1, p2, p3))),
        sp.Matrix((YBAR, (0, 1, q2, q3))),
        sp.Matrix((U3ROW, (0, 0, 1, k))),
    )


def family(p2, p3, q2, k, scales=(1, 1, 1)):
    """The F12 planes on the tie q3 = -k(p2+q2)-p3, torus-scaled."""
    q3 = -k * (p2 + q2) - p3
    source = sp.diag(*scales, 1)
    return tuple(plane * source for plane in free_planes(p2, p3, q2, q3, k))


def flattening_minors(tensor):
    """All 2x2 minors of the three 4x4 pair flattenings, expanded."""
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
                    sp.expand(
                        table[(r1, k1)] * table[(r2, k2)]
                        - table[(r1, k2)] * table[(r2, k1)]
                    )
                )
    return minors


def assert_flattening_minors_vanish(tensor):
    for minor in flattening_minors(tensor):
        assert minor == 0, minor


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
    """Kernel row of every mode from the rank-one 2x8 mode flattenings."""
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
    """Pair profile, rank-one relation factors, arrows, kernel-kernel."""
    tensor = point_tensor_of(planes)
    assert any(value != 0 for value in tensor.values())
    kernels = mode_kernels(planes, tensor)
    profile = []
    relations = {}
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
        assert two_by_two.rank() == 1
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
            "factors": (u_a, u_b),
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
    return tuple(profile), relations, kernel_kernel, arrows, kernels


def meets_coordinate_plane(plane, pair):
    """U cap span(e_pair) != 0: the complement-column 2x2 has rank <= 1."""
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
    assert "rank sum <= 19 on all of closure(F12)." in theorem_text
    assert "vanishes on every decomposable chart tensor" in theorem_text
    assert "local dimension 0 at the origin." in theorem_text
    assert "This is not a classification." in theorem_text

    p2, p3, q2, q3, k = sp.symbols("p2 p3 q2 q3 k")
    t0, t1, t2 = sp.symbols("t0 t1 t2")
    sample = {
        symbol: sp.Integer(SAMPLE_VALUES[str(symbol)])
        for symbol in (p2, p3, q2, k, t0, t1, t2)
    }
    assert (-k * (p2 + q2) - p3).subs(sample) == EXPECTED_Q3

    # ---------------- the free chart: three words, one binomial ------
    free = free_planes(p2, p3, q2, q3, k)
    assert all(plane.rank() == 2 for plane in free)
    free_tensor = coefficients(free)
    t_0110 = sp.expand(2 * (p2 * q3 + p3 * q2))
    t_1110 = sp.expand((p3 + q3) - k * (p2 + q2))
    t_0111 = sp.expand((p3 + q3) + k * (p2 + q2))
    assert sp.expand(free_tensor[(0, 1, 1, 0)] - t_0110) == 0
    assert sp.expand(free_tensor[(1, 1, 1, 0)] - t_1110) == 0
    assert sp.expand(free_tensor[(0, 1, 1, 1)] - t_0111) == 0
    for word in WORDS:
        if word not in ((0, 1, 1, 0), (1, 1, 1, 0), (0, 1, 1, 1)):
            assert free_tensor[word] == 0, word
    # Purity of the free chart is the single binomial T_1110*T_0111:
    # every 2x2 flattening minor is 0 or +- that product.
    binomial = sp.expand(t_1110 * t_0111)
    for minor in flattening_minors(free_tensor):
        assert minor in (0, binomial, sp.expand(-binomial)), minor

    # The three-conjugacy mechanism behind the thirteen dead words.
    def b01(u, w):
        return sp.expand(u[0] * w[1] + u[1] * w[0])

    def b_pi(u, w):
        return sp.expand(u[2] * w[3] + u[3] * w[2])

    w_minus = (0, 0, 1, -k)
    w_plus = (0, 0, 1, k)
    p_row = (0, 1, p2, p3)
    q_row = (0, 1, q2, q3)
    assert b01(U3ROW, YBAR) == 0            # kills the mixed P01 frames
    assert b_pi(w_minus, w_plus) == 0       # kills the double-w slice
    assert sp.expand(t_0110 - 2 * b_pi(p_row, q_row)) == 0
    assert sp.expand(t_1110 - b_pi(w_minus, tuple(
        pi + qi for pi, qi in zip(p_row, q_row)))) == 0
    assert sp.expand(t_0111 - b_pi(w_plus, tuple(
        pi + qi for pi, qi in zip(p_row, q_row)))) == 0

    # ---------------- the tied family: identical purity --------------
    planes = family(p2, p3, q2, k)
    assert all(plane.rank() == 2 for plane in planes)
    tensor = coefficients(planes)
    assert sp.expand(
        tensor[(0, 1, 1, 0)]
        - 2 * (p2 * (-k * (p2 + q2) - p3) + p3 * q2)
    ) == 0
    assert sp.expand(tensor[(1, 1, 1, 0)] + 2 * k * (p2 + q2)) == 0
    assert all(
        value == 0
        for word, value in tensor.items()
        if word not in ((0, 1, 1, 0), (1, 1, 1, 0))
    )
    assert_flattening_minors_vanish(tensor)

    # Kernels (7): K0 ~ k(p2+q2)u3 + B(p,q)w_-, K1=K2=ybar, K3=w_+.
    tied = {q3: -k * (p2 + q2) - p3}
    b_pq = sp.expand(b_pi(p_row, q_row).subs(tied))
    expected_k0 = tuple(
        sp.expand(k * (p2 + q2) * U3ROW[j] + b_pq * w_minus[j])
        for j in range(4)
    )
    generic_kernels = mode_kernels(planes, tensor)
    assert proportional(generic_kernels[0], expected_k0)
    assert proportional(generic_kernels[1], YBAR)
    assert proportional(generic_kernels[2], YBAR)
    assert proportional(generic_kernels[3], w_plus)

    # Torus: diag(t0,t1,t2,1) scales every coefficient by t0*t1*t2.
    scaled = family(p2, p3, q2, k, (t0, t1, t2))
    scaled_tensor = coefficients(scaled)
    for word in WORDS:
        assert sp.expand(
            scaled_tensor[word] - t0 * t1 * t2 * tensor[word]
        ) == 0
    # Subtorus reparametrization (8): diag(t,t,t2,1) preserves the
    # normal form with (p2,p3,q2,k) -> ((t2/t)p2, p3/t, (t2/t)q2, k/t2).
    t = sp.Symbol("t", nonzero=True)
    subtorus_image = family(p2, p3, q2, k, (t, t, t2))
    reparametrized = family(
        t2 / t * p2, p3 / t, t2 / t * q2, k / t2
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
    assert point_tensor[(1, 1, 1, 0)] == -32

    # ---------------- family tangent: rank five ----------------------
    reduced, chart_coordinates = reduce_in_charts(scaled)
    parameters = (p2, p3, q2, k, t0, t1, t2)
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
    assert family_tangent[:, :4].rank() == 4     # chart parameters alone.
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
    # The chart tensor is the full cube on bit3=0 with head (-100,-32).
    for word in WORDS:
        expected = 0 if word[3] == 1 else (-100 if word[0] == 0 else -32)
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
                {z: z + value for z, value in origin_substitution.items()}
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
            coefficient * z
            for coefficient, z in zip(row, plane_variables, strict=True)
        )
        for row in SLICE_COEFFS
    ]
    slice_dimension, singular_seconds = singular_slice_dimension(
        shifted, slices, "0"
    )
    assert slice_dimension == 0
    # Krull height bound: dim_0(V) <= 0 + 5; family tangent rank five
    # gives >= 5; the local dimension of the pure locus at the sample
    # is EXACTLY five, so closure(F12) is an irreducible component.
    local_dimension = 5

    # ---------------- distinctness -----------------------------------
    # (a) Sample profile (3,3,3,4,3,3), sum 19; the identical vanishing
    # of ALL 4x4 pair minors at the five rank-3 edges bounds the whole
    # closure by <= 19.
    sample_profile = pair_profile(point_planes)
    assert sample_profile == EXPECTED_PROFILE
    assert sum(sample_profile) == 19
    symbolic_profile = []
    for a, b in PAIRS:
        rows = []
        for i in range(2):
            for j in range(2):
                rows.append(
                    list(rmul(tuple(planes[a].row(i)), tuple(planes[b].row(j))))
                )
        matrix = sp.Matrix(rows)
        if (a, b) in RANK3_EDGES:
            for rr in itertools.combinations(range(4), 4):
                for cc in itertools.combinations(range(6), 4):
                    assert sp.expand(matrix[rr, cc].det()) == 0, ((a, b), rr, cc)
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

    # (c) The split-plane invariant.  U0 and U3 lie in S identically:
    # each contains the P01-line u3 and a nonzero Pi-line.
    for mode in (0, 3):
        row0 = tuple(planes[mode].row(0))
        row1 = tuple(planes[mode].row(1))
        assert row0 == U3ROW                    # the P01 line
        assert row1[0] == 0 and row1[1] == 0    # the Pi line
        assert row1[2] == 1                     # nonzero even at k=0
    # The middle planes never contribute a Pi-line: at the sample they
    # meet P01 only.
    for mode in (1, 2):
        assert meets_coordinate_plane(point_planes[mode], (0, 1))
        assert not meets_two_complementary(point_planes[mode])
    assert meets_two_complementary(point_planes[0])
    assert meets_two_complementary(point_planes[3])

    # Re-ground the thirteenth's certificate sample: a nonzero pure
    # tuple in which NO plane meets two complementary coordinate planes.
    thirteenth = tuple(
        sp.Matrix([list(row) for row in plane])
        for plane in THIRTEENTH_SAMPLE
    )
    thirteenth_tensor = point_tensor_of(thirteenth)
    thirteenth_support = {
        word for word, value in thirteenth_tensor.items() if value != 0
    }
    assert thirteenth_support == {(0, 1, 1, 0)}
    assert thirteenth_tensor[(0, 1, 1, 0)] == -120
    assert_flattening_minors_vanish(thirteenth_tensor)
    for plane in thirteenth:
        assert meets_coordinate_plane(plane, (0, 1))
        assert not meets_two_complementary(plane)

    # ---------------- generic geometry -------------------------------
    profile, relations, kernel_kernel, arrows, _ = relation_geometry(
        point_planes
    )
    assert profile == EXPECTED_PROFILE
    assert sorted(relations) == [(0, 1), (0, 2), (0, 3), (1, 3), (2, 3)]
    for edge in ((0, 1), (0, 2), (1, 3), (2, 3)):
        assert relations[edge]["supports"] == ((0, 1), (0, 1))
    assert relations[(0, 3)]["supports"] == ((2, 3), (2, 3))
    assert kernel_kernel == []
    assert arrows == [(0, 1), (0, 2), (0, 3), (3, 1), (3, 2)]
    indegrees = [0, 0, 0, 0]
    for _tail, head in arrows:
        indegrees[head] += 1
    assert indegrees == [0, 2, 2, 1]

    # Swap symmetry: mode-(12) swap composed with p <-> q.
    swapped_parameters = family(q2, -k * (p2 + q2) - p3, p2, k)
    swapped_tuple = (planes[0], planes[2], planes[1], planes[3])
    for mode in range(4):
        assert same_projective_plane(
            swapped_tuple[mode], swapped_parameters[mode]
        )
    # Reflection symmetry: diag(1,1,1,-1) with (p3,q3,k) -> (-p3,-q3,-k).
    reflection = sp.diag(1, 1, 1, -1)
    reflected = tuple(plane * reflection for plane in planes)
    reflected_parameters = family(p2, -p3, q2, -k)
    for mode in range(4):
        assert same_projective_plane(
            reflected[mode], reflected_parameters[mode]
        )
    # Zb2 = (03)-mode swap of F12 at k -> -k: one census orbit.
    kM = sp.Symbol("kM")
    zb2 = (
        sp.Matrix((U3ROW, (0, 0, 1, -kM))),
        sp.Matrix((YBAR, (0, 1, p2, p3))),
        sp.Matrix((YBAR, (0, 1, q2, kM * (p2 + q2) - p3))),
        sp.Matrix((U3ROW, (0, 0, 1, kM))),
    )
    f12_at = family(p2, p3, q2, -kM)
    swapped_modes = (f12_at[3], f12_at[1], f12_at[2], f12_at[0])
    for mode in range(4):
        assert same_projective_plane(zb2[mode], swapped_modes[mode])

    # ---------------- result -----------------------------------------
    dependencies = {THEOREM.name: sha256(THEOREM)}
    snapshot_hash = (
        sha256(SNAPSHOT_README) if SNAPSHOT_README.exists() else None
    )
    result = {
        "verified": True,
        "field": "C",
        "component": "split-pair fivefold (family F12, branch Zb1)",
        "census_position": "twelfth pure-compression component orbit",
        "method": (
            "identically pure two-word family on the Zb1 tie of the "
            "coincident-support chart; rank-five family tangent; "
            "rank-fourteen (singular) incidence point with "
            "second-order-obstructed transverse direction; exact "
            "char-0 five-hyperplane slice ds standard basis pinning "
            "local dimension to five"
        ),
        "free_chart_words": {
            "0110": "2*(p2*q3 + p3*q2)",
            "1110": "(p3 + q3) - k*(p2 + q2)",
            "0111": "(p3 + q3) + k*(p2 + q2)",
        },
        "purity_binomial": "T_1110*T_0111",
        "tie": "k*(p2 + q2) + (p3 + q3) = 0",
        "pure_coefficients_on_tie": {
            "0110": "2*(p2*q3 + p3*q2)",
            "1110": "-2*k*(p2 + q2)",
        },
        "identically_pure": True,
        "torus_scaling": "t0*t1*t2",
        "subtorus_reparametrization": (
            "(p2,p3,q2,k) -> ((t2/t)p2, p3/t, (t2/t)q2, k/t2)"
        ),
        "sample": {key: value for key, value in SAMPLE_VALUES.items()},
        "sample_q3": EXPECTED_Q3,
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
        "kernels": [
            "k*(p2+q2)*u3 + B(p,q)*(0,0,1,-k)",
            "ybar",
            "ybar",
            "(0,0,1,k)",
        ],
        "pair_profile": list(EXPECTED_PROFILE),
        "rank_sum": 19,
        "closure_rank_sum_bound": 19,
        "rank3_edges_all_4x4_minors_vanish_identically": True,
        "distinct_from_sixfolds_by": "dimension 5 < 6",
        "distinct_from_rank21_fivefolds_by": (
            "closure-wide rank-sum bound 19 < 21 (census symmetries "
            "preserve pair-rank sums)"
        ),
        "fivefold_sample_rank_sums": fivefold_rank_sums,
        "distinct_from_thirteenth_by": (
            "split-plane invariant: some plane meets two complementary "
            "coordinate planes on all of closure(F12), no plane does at "
            "the thirteenth's sample"
        ),
        "thirteenth_sample_support": ["0110"],
        "thirteenth_sample_value": "-120",
        "thirteenth_sample_no_split_plane": True,
        "relation_edges": ["01", "02", "03", "13", "23"],
        "relation_supports": {
            "01": ["01", "01"], "02": ["01", "01"],
            "13": ["01", "01"], "23": ["01", "01"],
            "03": ["23", "23"],
        },
        "orientation_arrows": ["0->1", "0->2", "0->3", "3->1", "3->2"],
        "indegrees": [0, 2, 2, 1],
        "kernel_kernel_generic": False,
        "rank_four_edge": "12",
        "swap_symmetry": "(12)-mode swap with p <-> q",
        "reflection_symmetry": (
            "diag(1,1,1,-1) with (p3,q3,k) -> (-p3,-q3,-k)"
        ),
        "Zb2_identification": "(03)-mode swap at k -> -k",
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
    output_path = ROOT / "tmp" / "p4_split_pair_pure_component_verified.json"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
