#!/usr/bin/env python3
"""Verify the equal-support sixfold eleventh pure-P4 component (family C10).

Consolidates the discovery snapshot's certificates (steps 22/23/24/25/
28/29 of research_snapshots/2026-08-04-p4-equal-support-rank-two-strata)
into one fail-closed replay:

  * identical purity of the ten-parameter family, symbolically, with
    the apolar factorization and the torus monomial scaling;
  * family tangent rank six at the generic sample (thirteen parameter
    directions including the full projective source torus);
  * universal Segre-incidence Jacobian rank THIRTEEN at the sample
    (tangent dimension seven: a singular incidence point), plus the
    explicit first-order-pure, second-order-obstructed U3-direction;
  * the characteristic-zero slice certificate: the eleven
    ratio-eliminated multi-flip purity equations, shifted so the
    sample is the origin, cut by six fixed integer hyperplanes, have
    a Singular `ds` standard basis of local dimension ZERO — with the
    rank-six family tangent this pins the pure locus's local
    dimension at the sample to exactly six (Krull height bound, valid
    for any six forms);
  * distinctness: the closed symmetry-stable coordinate-plane
    invariant against the tenth component (whose certificate point is
    re-grounded here), rank-sum monotonicity 21 > 20 against the
    seventh (whose generic sample is re-grounded here), dimension
    against the eight fivefolds;
  * generic geometry: equal supports {2,3} on all three rank-one
    relations, star orientation with indegrees (1,1,1,0), the
    kernel-kernel W-wall c0=c1, and the mode-(12) swap symmetry.

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

import sys

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
THEOREM = HERE / "P4_EQUAL_SUPPORT_SIXFOLD_PURE_COMPONENT.md"
SNAPSHOT_README = (
    REPO_ROOT
    / "research_snapshots"
    / "2026-08-04-p4-equal-support-rank-two-strata"
    / "README.md"
)

WORDS = tuple(itertools.product((0, 1), repeat=4))
PAIRS = tuple(itertools.combinations(range(4), 2))
PERMS4 = tuple(itertools.permutations(range(4)))
FLATTENINGS = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))
PIVOTS = ((0, 2), (0, 2), (0, 2), (2, 3))

SAMPLE_VALUES = {
    "c0": 3, "c1": -2, "c2": 5, "t": 2,
    "v0": 3, "v1": -7, "v2": 2, "v3": 5,
    "x2": -1, "x3": 4,
    "t0": 1, "t1": 1, "t2": 1,
}
EXPECTED_COORDINATE_POINT = (
    sp.Rational(7, 3), 0, 0, -3,
    sp.Rational(-7, 3), sp.Rational(1, 3), 0, 2,
    sp.Rational(-7, 3), sp.Rational(-1, 6), 0, -5,
    0, 0, 0, 0,
)
FAMILY_MINOR_ROWS = (0, 3, 5, 7, 9, 11)
FAMILY_MINOR_COLUMNS = (0, 1, 2, 3, 4, 5)
EXPECTED_FAMILY_MINOR = sp.Rational(1, 324)
INCIDENCE_ANCHOR = (1, 0, 0, 0)
EXPECTED_ANCHOR_VALUE = sp.Integer(14)
EXPECTED_RATIOS = (0, 0, 0, sp.Rational(-1, 3))
INCIDENCE_MINOR_ROWS = tuple(range(13))
INCIDENCE_MINOR_COLUMNS = (0, 1, 2, 3, 4, 6, 10, 12, 13, 14, 15, 16, 17)
EXPECTED_INCIDENCE_MINOR = sp.Rational(16866160640, 6561)
SLICE_COEFFS = (
    (1, 2, -1, 3, 1, -2, 1, 1, -3, 2, 1, -1, 2, 1, -2, 3),
    (2, -1, 1, 1, -2, 3, 1, -1, 1, 1, -2, 1, 3, -1, 1, -2),
    (1, 1, 2, -3, 1, 1, -1, 2, 1, -2, 3, 1, -1, 1, 1, 2),
    (3, -2, 1, 1, 1, -1, 2, 1, -2, 1, 1, 3, 1, -1, 2, 1),
    (1, 3, -2, 1, 2, 1, 1, -1, 1, 2, -1, 1, 1, 2, -3, 1),
    (2, 1, 1, -1, 3, -2, 1, 1, 2, -1, 1, 1, -2, 3, 1, 1),
)
SINGULAR_TIMEOUT = 3600
TENTH_POINT = (2, 3, 5, 7, 11)
SEVENTH_POINT = (1, 2, 4, 1, 2)


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


def family(c0, c1, c2, t, v, x2, x3, scales=(1, 1, 1)):
    """The C10 planes; v is a length-four sequence, x=(t*v0,t*v1,x2,x3)."""
    raw = (
        sp.Matrix(((v[0], -v[1], 0, 0), (0, 0, 1, -c0))),
        sp.Matrix(((0, 0, 1, -c1), tuple(v))),
        sp.Matrix(((0, 0, 1, -c2), (t * v[0], t * v[1], x2, x3))),
        sp.Matrix(((0, 0, 1, 1), (0, 0, 1, -1))),
    )
    source = sp.diag(*scales, 1)
    return tuple(plane * source for plane in raw)


def assert_flattening_minors_vanish(tensor):
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
                minor = sp.expand(
                    table[(r1, k1)] * table[(r2, k2)]
                    - table[(r1, k2)] * table[(r2, k1)]
                )
                assert minor == 0, (left, right, r1, r2, k1, k2, minor)


def nonzero_flattening_minors(tensor):
    found = []
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
                minor = sp.expand(
                    table[(r1, k1)] * table[(r2, k2)]
                    - table[(r1, k2)] * table[(r2, k1)]
                )
                if minor != 0:
                    found.append(minor)
    return found


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


def is_coordinate_plane(plane, pair):
    complement = tuple(i for i in range(4) if i not in pair)
    off = sp.Matrix([[plane[r, c] for c in complement] for r in range(2)])
    on = sp.Matrix([[plane[r, c] for c in pair] for r in range(2)])
    return off.is_zero_matrix and on.det() != 0


def coordinate_plane_count(planes):
    return sum(
        1
        for plane in planes
        if any(is_coordinate_plane(plane, pair) for pair in PAIRS)
    )


def tenth_planes():
    b, e, k, m, r = TENTH_POINT
    ybar = (1, -1, 0, 0)
    u3 = (1, 1, 0, 0)
    return (
        sp.Matrix((ybar, (0, 1, b, -b * k))),
        sp.Matrix((ybar, (0, 1, e, -e * k))),
        sp.Matrix((u3, (0, 0, 1, k))),
        sp.Matrix(((1, m, 0, 0), (0, r, 1, -k))),
    )


def seventh_planes():
    a, c, d, b, e = SEVENTH_POINT
    h = a + c - d
    return (
        sp.Matrix(((1, 0, 0, -1), (0, 0, 1, 1))),
        sp.Matrix(((1, b, 0, 1 - b * h), (0, e, 1, 1 - e * h))),
        sp.Matrix(((1, 0, -1, 0), (0, 1, -a - c, -d))),
        sp.Matrix(((1, 0, 0, 1), (0, 0, 1, -1))),
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
        "eleven component orbits: eight fivefolds and three sixfolds"
        in theorem_text
    )
    assert (
        "the first component certified at a singular incidence point"
        in theorem_text
    )
    assert "This is not a classification" in theorem_text
    assert "vanishes on every decomposable chart tensor" in theorem_text
    assert "local dimension 0 at the origin" in theorem_text

    c0, c1, c2, t = sp.symbols("c0 c1 c2 t")
    v = sp.symbols("v0:4")
    x2, x3 = sp.symbols("x2 x3")
    t0, t1, t2 = sp.symbols("t0 t1 t2")
    sample = {
        symbol: sp.Integer(SAMPLE_VALUES[str(symbol)])
        for symbol in (c0, c1, c2, t, *v, x2, x3, t0, t1, t2)
    }

    # ---------------- identical purity, symbolically -----------------
    planes = family(c0, c1, c2, t, v, x2, x3)
    assert all(plane.rank() == 2 for plane in planes)
    tensor = coefficients(planes)
    assert sp.expand(
        tensor[(1, 1, 1, 0)] + 2 * t * v[0] * v[1] * (c0 - 1)
    ) == 0
    assert sp.expand(
        tensor[(1, 1, 1, 1)] + 2 * t * v[0] * v[1] * (c0 + 1)
    ) == 0
    assert all(
        value == 0
        for word, value in tensor.items()
        if word not in ((1, 1, 1, 0), (1, 1, 1, 1))
    )
    assert_flattening_minors_vanish(tensor)

    # The apolar mechanism: (5) the U0 off-Pi row is B01-apolar to the
    # common {01}-head of v and x, and (6) the survivor factors as
    # perm2_{01}(v,x) * B(w_{c0}, p3).
    def perm2(u, w, columns):
        return sp.expand(
            u[columns[0]] * w[columns[1]] + u[columns[1]] * w[columns[0]]
        )

    u0_row = (v[0], -v[1], 0, 0)
    x_row = (t * v[0], t * v[1], x2, x3)
    assert perm2(u0_row, tuple(v), (0, 1)) == 0
    assert perm2(u0_row, x_row, (0, 1)) == 0
    w_c0 = (0, 0, 1, -c0)
    for bit3, p3 in ((0, (0, 0, 1, 1)), (1, (0, 0, 1, -1))):
        assert sp.expand(
            tensor[(1, 1, 1, bit3)]
            - perm2(tuple(v), x_row, (0, 1)) * perm2(w_c0, p3, (2, 3))
        ) == 0
    # The three exceptional relations (21) are B-conjugacies inside Pi.
    for c in (c0, c1, c2):
        assert all(
            value == 0 for value in rmul((0, 0, 1, -c), (0, 0, 1, c))
        )
    # Mode-3 kernel: the B-conjugate of U0's Pi-line kills the slice.
    assert sp.expand(
        (1 + c0) * tensor[(1, 1, 1, 0)] + (1 - c0) * tensor[(1, 1, 1, 1)]
    ) == 0

    # Torus: diag(t0,t1,t2,1) scales every coefficient by t0*t1*t2 and
    # the family is torus-saturated.
    scaled = family(c0, c1, c2, t, v, x2, x3, (t0, t1, t2))
    scaled_tensor = coefficients(scaled)
    for word in WORDS:
        assert sp.expand(
            scaled_tensor[word] - t0 * t1 * t2 * tensor[word]
        ) == 0

    # ---------------- sample instantiation ---------------------------
    point_planes = tuple(plane.subs(sample) for plane in scaled)
    assert all(plane.rank() == 2 for plane in point_planes)
    point_tensor = point_tensor_of(point_planes)
    assert point_tensor[(1, 1, 1, 0)] == 168
    assert point_tensor[(1, 1, 1, 1)] == 336
    kernels = mode_kernels(point_planes, point_tensor)
    expected_kernels = (
        (3, 7, 0, 0),        # (v0,-v1,0,0)
        (0, 0, 1, 2),        # w_{c1}
        (0, 0, 1, -5),       # w_{c2}
        (0, 0, 1, 3),        # (0,0,1,c0): B-conjugate of U0 cap Pi
    )
    for kernel, expected in zip(kernels, expected_kernels, strict=True):
        assert proportional(kernel, expected)

    # ---------------- family tangent: rank six -----------------------
    reduced, chart_coordinates = reduce_in_charts(scaled)
    parameters = (c0, c1, c2, t, v[0], v[1], v[2], v[3], x2, x3, t0, t1, t2)
    family_tangent = (
        sp.Matrix(chart_coordinates).jacobian(parameters).subs(sample)
    )
    family_tangent = sp.Matrix(
        [
            [sp.nsimplify(sp.cancel(entry)) for entry in row]
            for row in family_tangent.tolist()
        ]
    )
    assert family_tangent.rank() == 6
    family_minor = family_tangent.extract(
        FAMILY_MINOR_ROWS, FAMILY_MINOR_COLUMNS
    ).det()
    assert family_minor == EXPECTED_FAMILY_MINOR
    # Mode-3 chart coordinates are frozen along the family (U3 == Pi).
    assert all(
        family_tangent[row, column] == 0
        for row in range(12, 16)
        for column in range(13)
    )

    # ---------------- incidence Jacobian: rank THIRTEEN --------------
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
    assert incidence_rank == 13          # NOT fourteen: tangent dim seven.
    incidence_minor = incidence_jacobian.extract(
        INCIDENCE_MINOR_ROWS, INCIDENCE_MINOR_COLUMNS
    ).det()
    assert incidence_minor == EXPECTED_INCIDENCE_MINOR
    incidence_tangent_dimension = 20 - incidence_rank
    assert incidence_tangent_dimension == 7

    # The tangent excess beyond the family is exactly one dimension.
    null_vectors = incidence_jacobian.nullspace()
    assert len(null_vectors) == 7
    z_projections = [
        sp.Matrix([vector[i] for i in range(16)]) for vector in null_vectors
    ]
    family_columns = sp.Matrix.hstack(
        *[family_tangent[:, j] for j in range(13)]
    )
    assert family_columns.rank() == 6
    augmented = sp.Matrix.hstack(family_columns, *z_projections)
    assert augmented.rank() == 7

    # The excess direction: U3 off Pi with a3 : b3 = -c0 : 1 is
    # first-order pure identically, second-order obstructed at the
    # sample.  (Steps 24/25 of the snapshot.)
    a3, b3, eps = sp.symbols("a3 b3 eps")
    extended = (
        planes[0],
        planes[1],
        planes[2],
        sp.Matrix(
            ((a3 * v[0], a3 * v[1], 1, 0), (b3 * v[0], b3 * v[1], 0, 1))
        ),
    )
    extended_tensor = coefficients(extended)
    extended_minors = nonzero_flattening_minors(extended_tensor)
    assert len(extended_minors) == 12
    direction = {a3: -c0 * eps, b3: eps}
    second_order = []
    for minor in extended_minors:
        expansion = sp.expand(minor.subs(direction))
        polynomial = sp.Poly(expansion, eps)
        table = dict(zip(polynomial.monoms(), polynomial.coeffs()))
        assert sp.expand(table.get((0,), 0)) == 0
        assert sp.expand(table.get((1,), 0)) == 0
        quadratic = table.get((2,))
        if quadratic is not None and sp.expand(quadratic) != 0:
            second_order.append(sp.expand(quadratic))
    assert len(second_order) == 8
    c_sample = {key: sample[key] for key in (c0, c1, c2, t, *v, x2, x3)}
    assert all(
        sp.expand(coefficient.subs(c_sample)) != 0
        for coefficient in second_order
    )

    # ---------------- the char-0 slice certificate -------------------
    # Eleven multi-flip equations G_w (16): vanish on every decomposable
    # chart tensor, no anchor-nonvanishing hypothesis needed.
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
    # Krull height bound: dim_0(V) <= 0 + 6; family tangent rank six
    # gives >= 6; the local dimension of the pure locus at the sample
    # is EXACTLY six, so closure(C10) is an irreducible component.
    local_dimension = 6

    # ---------------- distinctness -----------------------------------
    # (a) Coordinate-plane invariant against the tenth.  U3 is the
    # coordinate plane span(e2,e3) for ALL parameter values.
    u3_plane = planes[3]
    assert all(
        sp.simplify(u3_plane[row, column]) == 0
        for row in range(2)
        for column in (0, 1)
    )
    assert u3_plane[:, (2, 3)].det() != 0
    plain_point_planes = tuple(
        plane.subs(sample) for plane in planes
    )
    for mode in range(3):
        assert not any(
            is_coordinate_plane(plain_point_planes[mode], pair)
            for pair in PAIRS
        )
    assert coordinate_plane_count(plain_point_planes) == 1

    # Re-ground the tenth's certificate point as a nonzero pure tuple.
    tenth = tenth_planes()
    b, e, k, m, r = TENTH_POINT
    tenth_tensor = point_tensor_of(tenth)
    tenth_support = {
        word for word, value in tenth_tensor.items() if value != 0
    }
    assert tenth_support == {(1, 1, 0, 0), (1, 1, 0, 1)}
    assert tenth_tensor[(1, 1, 0, 0)] == -2 * b * e * k * (m + 1)
    assert tenth_tensor[(1, 1, 0, 1)] == -2 * k * (b * e * r + b + e)
    assert_flattening_minors_vanish(tenth_tensor)
    assert coordinate_plane_count(tenth) == 0

    # (b) Rank-sum monotonicity against the seventh.
    c10_profile = pair_profile(plain_point_planes)
    assert c10_profile == (4, 4, 3, 4, 3, 3)
    assert sum(c10_profile) == 21
    seventh_profile = pair_profile(seventh_planes())
    assert seventh_profile == (4, 3, 2, 4, 4, 3)
    assert sum(seventh_profile) == 20
    assert sum(c10_profile) > sum(seventh_profile)

    # (c) The tenth's profile multiset AGREES: profiles cannot separate,
    # the coordinate-plane invariant is what does.
    tenth_profile = pair_profile(tenth)
    assert tenth_profile == (3, 3, 4, 3, 4, 4)
    assert sorted(tenth_profile) == sorted(c10_profile)
    assert sum(tenth_profile) == 21

    # ---------------- generic geometry -------------------------------
    profile, relations, kernel_kernel, arrows, _ = relation_geometry(
        plain_point_planes
    )
    assert profile == (4, 4, 3, 4, 3, 3)
    assert sorted(relations) == [(0, 3), (1, 3), (2, 3)]
    for edge, data in relations.items():
        assert data["supports"] == ((2, 3), (2, 3))   # equal supports.
    assert kernel_kernel == []
    assert arrows == [(0, 3), (3, 1), (3, 2)]
    indegrees = [0, 0, 0, 0]
    for _tail, head in arrows:
        indegrees[head] += 1
    assert sorted(indegrees, reverse=True) == [1, 1, 1, 0]

    # W-wall c0=c1: the {13}-relation becomes kernel-kernel; the swap
    # image wall c0=c2 does the same on {23}.
    wall_sample = dict(sample)
    wall_sample[c1] = wall_sample[c0]
    wall_planes = tuple(
        plane.subs(wall_sample) for plane in planes
    )
    wall_profile, _, wall_kk, wall_arrows, _ = relation_geometry(wall_planes)
    assert wall_profile == (4, 4, 3, 4, 3, 3)
    assert wall_kk == [(1, 3)]
    assert wall_arrows == [(0, 3), (3, 2)]
    swap_wall_sample = dict(sample)
    swap_wall_sample[c2] = swap_wall_sample[c0]
    swap_wall_planes = tuple(
        plane.subs(swap_wall_sample) for plane in planes
    )
    _, _, swap_wall_kk, swap_wall_arrows, _ = relation_geometry(
        swap_wall_planes
    )
    assert swap_wall_kk == [(2, 3)]
    assert swap_wall_arrows == [(0, 3), (3, 1)]

    # Swap symmetry (23): the mode-(12) swap of the family equals the
    # family at (v,x,t,c1,c2) -> (x,v,1/t,c2,c1), identically.
    x_of_v = (t * v[0], t * v[1], x2, x3)
    swapped_parameters = family(
        c0, c2, c1, 1 / t, x_of_v, v[2], v[3]
    )
    swapped_tuple = (planes[0], planes[2], planes[1], planes[3])
    for mode in range(4):
        assert same_projective_plane(
            swapped_tuple[mode], swapped_parameters[mode]
        )

    # ---------------- result -----------------------------------------
    dependencies = {THEOREM.name: sha256(THEOREM)}
    snapshot_hash = (
        sha256(SNAPSHOT_README) if SNAPSHOT_README.exists() else None
    )
    result = {
        "verified": True,
        "field": "C",
        "component": "equal-support sixfold (family C10)",
        "census_position": "eleventh pure-compression component orbit",
        "method": (
            "identically pure free family with apolar factorization; "
            "rank-six family tangent; rank-thirteen (singular) "
            "incidence point; exact char-0 six-hyperplane slice ds "
            "standard basis pinning local dimension to six"
        ),
        "pure_coefficients": {
            "1110": "-2*t*v0*v1*(c0 - 1)",
            "1111": "-2*t*v0*v1*(c0 + 1)",
        },
        "identically_pure": True,
        "family_free": True,
        "torus_scaling": "t0*t1*t2",
        "sample": {key: value for key, value in SAMPLE_VALUES.items()},
        "Grassmann_pivots": [list(pivots) for pivots in PIVOTS],
        "coordinate_point": [str(value) for value in coordinate_point],
        "family_tangent_rank": 6,
        "family_tangent_minor_rows": list(FAMILY_MINOR_ROWS),
        "family_tangent_minor_columns": list(FAMILY_MINOR_COLUMNS),
        "family_tangent_minor": str(family_minor),
        "incidence_anchor": "1000",
        "incidence_anchor_value": str(EXPECTED_ANCHOR_VALUE),
        "incidence_target_ratios": [str(value) for value in ratios],
        "incidence_jacobian_rank": incidence_rank,
        "incidence_tangent_dimension": incidence_tangent_dimension,
        "incidence_minor_columns": list(INCIDENCE_MINOR_COLUMNS),
        "incidence_minor": str(incidence_minor),
        "singular_incidence_point": True,
        "first_component_certified_at_singular_incidence_point": True,
        "excess_direction": "U3 off Pi, a3:b3 = -c0:1",
        "excess_direction_first_order_pure": True,
        "excess_direction_second_order_obstructed_at_sample": True,
        "slice_certificate": {
            "equations": 11,
            "anchor": "1000",
            "slice_rows": [list(row) for row in SLICE_COEFFS],
            "char": "0",
            "ordering": "ds",
            "local_dimension": slice_dimension,
            "singular_seconds": round(singular_seconds, 2),
            "krull_upper_bound": 6,
        },
        "local_dimension_at_sample": local_dimension,
        "component_dimension": 6,
        "component_rational": True,
        "kernels": [
            "(v0,-v1,0,0)",
            "(0,0,1,-c1)",
            "(0,0,1,-c2)",
            "(0,0,1,c0)",
        ],
        "pair_profile": list(c10_profile),
        "rank_sum": 21,
        "relation_supports_all_equal": "23",
        "orientation_arrows": ["0->3", "3->1", "3->2"],
        "indegrees": [1, 1, 1, 0],
        "kernel_kernel_generic": False,
        "W_wall": "c0=c1 (kernel-kernel on edge 13)",
        "swap_symmetry": "(12)-swap with (v,x,t,c1,c2)->(x,v,1/t,c2,c1)",
        "swap_exchanges_walls": True,
        "distinct_from_tenth_by": "coordinate-plane invariant",
        "tenth_certificate_point": list(TENTH_POINT),
        "tenth_coordinate_plane_count": 0,
        "c10_coordinate_plane_count_at_sample": 1,
        "tenth_profile": list(tenth_profile),
        "profile_multisets_agree_with_tenth": True,
        "distinct_from_seventh_by": "rank-sum monotonicity 21 > 20",
        "seventh_profile": list(seventh_profile),
        "distinct_from_fivefolds_by": "dimension 6 > 5",
        "certified_pure_component_orbit_count": 11,
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
        REPO_ROOT / "tmp" / "p4_equal_support_sixfold_pure_component_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
