#!/usr/bin/env python3
"""Direct CANDIDATE weighted-H22 analysis of the two infinity endpoints."""

from __future__ import annotations

import hashlib
import itertools
import json
import shutil
import subprocess
from datetime import UTC, datetime
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
NOTE = (
    ROOT
    / "P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_INFINITY_ENDPOINT_CANDIDATE.md"
)
P4_BOUNDARY = ROOT / "P4_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY.md"
H31_ENDPOINT = (
    ROOT
    / "P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_INFINITY_ENDPOINT_OBSTRUCTION.md"
)
H31_PRIMARY = (
    ROOT
    / "verify_p5_h31_common_active_binary_triangle_p_plus_q_infinity_endpoint_obstruction.py"
)
H31_AUDIT = (
    ROOT
    / "audit_p5_h31_common_active_binary_triangle_p_plus_q_infinity_endpoint_obstruction.py"
)

WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED_WORDS = WORDS[1:-1]
PERMUTATIONS_3 = tuple(itertools.permutations(range(3)))
PERMUTATIONS_4 = tuple(itertools.permutations(range(4)))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_commit() -> str:
    return subprocess.run(
        ("git", "rev-parse", "HEAD"),
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
    ).stdout.strip()


def add(left, right):
    return tuple(sp.expand(a + b) for a, b in zip(left, right))


def scale(coefficient, vector):
    return tuple(sp.expand(coefficient * value) for value in vector)


def permanent3(rows, columns=(0, 1, 2)):
    return sp.expand(
        sum(
            rows[0][columns[p[0]]] * rows[1][columns[p[1]]] * rows[2][columns[p[2]]]
            for p in PERMUTATIONS_3
        )
    )


def permanent4(rows):
    return sp.expand(
        sum(
            sp.prod(rows[index][permutation[index]] for index in range(4))
            for permutation in PERMUTATIONS_4
        )
    )


def endpoint_bases(gamma):
    e = (sp.Integer(1), 0, 0, 0)
    w = (0, 1, 1, 1)
    u = (0, 1, -1, 0)
    v1 = (0, 1, 1, 0)
    v2 = (0, 0, 0, 1)
    alpha = (e, e, scale(-1, u), add(scale(2, v2), scale(-1, v1)))
    beta = (w, w, e, add(scale(gamma, e), v1))
    return alpha, beta


def shift(alpha, beta, marking):
    return tuple(
        add(beta[index], scale(marking[index], alpha[index])) for index in range(4)
    )


def contract(row, extension, direction, slope):
    if direction == "D01_finite":
        return (slope * row[0] + row[1], row[2], row[3], extension)
    if direction == "D01_infinity":
        return (row[0], row[2], row[3], extension)
    if direction == "D23_finite":
        return (row[0], row[1], slope * row[2] + row[3], extension)
    if direction == "D23_infinity":
        return (row[0], row[1], row[2], extension)
    raise ValueError(direction)


def build_model(gamma, direction, slope, marking):
    alpha, canonical_beta = endpoint_bases(sp.Integer(gamma))
    beta = shift(alpha, canonical_beta, marking)
    extensions = sp.symbols("z0:8")
    alpha_rows = tuple(
        contract(alpha[i], extensions[i], direction, slope) for i in range(4)
    )
    beta_rows = tuple(
        contract(beta[i], extensions[4 + i], direction, slope) for i in range(4)
    )
    coefficients = {}
    for word in WORDS:
        selected = tuple(beta_rows[i] if word[i] else alpha_rows[i] for i in range(4))
        coefficients[word] = sp.expand(
            sum(
                selected[i][3]
                * permanent3(tuple(selected[j] for j in range(4) if j != i))
                for i in range(4)
            )
        )
    mixed = sp.Matrix(
        [
            [coefficients[word].coeff(extension) for extension in extensions]
            for word in MIXED_WORDS
        ]
    )
    return {
        "extensions": extensions,
        "alpha_rows": alpha_rows,
        "beta_rows": beta_rows,
        "mixed": mixed,
        "A": coefficients[WORDS[0]],
        "B": coefficients[WORDS[-1]],
    }


def marked_matrix(model, mode):
    other = tuple(index for index in range(4) if index != mode)
    rows = []
    for bits in itertools.product((0, 1), repeat=3):
        selected = tuple(
            model["beta_rows"][index] if bits[position] else model["alpha_rows"][index]
            for position, index in enumerate(other)
        )
        rows.append(
            tuple(
                permanent3(
                    selected, tuple(column for column in range(4) if column != marked)
                )
                for marked in range(4)
            )
        )
    return sp.Matrix(rows)


def assert_equal(left, right, label):
    assert sp.factor(left - right) == 0, (label, sp.factor(left), right)


def assert_zero(values, label):
    assert all(sp.factor(value) == 0 for value in values), label


def substitute_vector(model, vector):
    return dict(zip(model["extensions"], vector))


def singular_command():
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    if shutil.which("wsl.exe"):
        return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")
    raise RuntimeError("Singular is required")


def singular(expression):
    return str(sp.cancel(expression)).replace("**", "^")


def projection_certificate(gamma, direction, expected, keep_slope=False):
    h = sp.symbols("h0:4")
    r = sp.Symbol("r")
    model = build_model(gamma, direction, r, h)
    inverse = sp.Symbol("winv")
    equations = [
        *tuple(model["mixed"] * sp.Matrix(model["extensions"])),
        model["A"] - 1,
        inverse * model["B"] - 1,
    ]
    eliminated = model["extensions"] + (inverse,)
    finite = direction.endswith("finite")
    if finite and not keep_slope:
        eliminated += (r,)
    retained = ((r,) if finite and keep_slope else ()) + h
    variables = eliminated + retained
    program = "\n".join(
        (
            "ring rr=0,("
            + ",".join(map(str, variables))
            + f"),(dp({len(eliminated)}),dp({len(retained)}));",
            "option(redSB);",
            "ideal ii=" + ",".join(map(singular, equations)) + "; ii=slimgb(ii);",
            "ideal jj=std(eliminate(ii," + "*".join(map(str, eliminated)) + "));",
            "ideal ee=" + ",".join(map(singular, expected)) + "; ee=std(ee);",
            "ideal lr=simplify(reduce(jj,ee),2);",
            "ideal rl=simplify(reduce(ee,jj),2);",
            '"RESULT:"+string((size(lr)==0)&&(size(rl)==0))+":"+string(size(jj));',
            "quit;",
        )
    )
    completed = subprocess.run(
        singular_command(),
        input=program,
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=30,
        check=False,
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), completed
    marker = [
        line for line in completed.stdout.splitlines() if line.startswith("RESULT:")
    ]
    assert len(marker) == 1 and marker[0].split(":")[1] == "1", (
        gamma,
        direction,
        completed.stdout,
    )
    return {
        "gamma": gamma,
        "direction": direction,
        "slope_retained": keep_slope,
        "projected_ideal": [singular(value) for value in expected],
        "bidirectional_ideal_equality": True,
        "standard_basis_size": int(marker[0].split(":")[2]),
    }


def geometry_and_projections():
    geometry = {}
    for gamma in (0, 2):
        alpha, beta = endpoint_bases(gamma)
        coefficients = {
            word: permanent4(tuple(beta[i] if word[i] else alpha[i] for i in range(4)))
            for word in WORDS
        }
        assert coefficients[WORDS[-1]] == 4
        assert all(
            value == 0 for word, value in coefficients.items() if word != WORDS[-1]
        )
        geometry[gamma] = {"sole_pure_word": "1111", "coefficient": 4}
    h0, h1, h2, h3 = sp.symbols("h0:4")
    ideals = {
        0: {
            "D01_finite": (h3, h2, h0 * h1),
            "D01_infinity": (h3, h2, h0 * h1),
            "D23_finite": (h3, h2, h0 * h1),
            "D23_infinity": (sp.Integer(1),),
        },
        2: {
            "D01_finite": (h3, h2, h0 * h1),
            "D01_infinity": (h3, h2, h0 + h1, h1**2),
            "D23_finite": (h3, h2, h0 * h1),
            "D23_infinity": (sp.Integer(1),),
        },
    }
    projections = []
    for gamma in (0, 2):
        for direction, expected in ideals[gamma].items():
            projections.append(projection_certificate(gamma, direction, expected))
            if direction.endswith("finite"):
                projections.append(
                    projection_certificate(gamma, direction, expected, keep_slope=True)
                )
    return geometry, projections


def frame_from_diagonals(model, target):
    mixed = model["mixed"]
    raw = sp.Matrix.hstack(*mixed.nullspace())
    arow = sp.Matrix([[model["A"].coeff(value) for value in model["extensions"]]])
    brow = sp.Matrix([[model["B"].coeff(value) for value in model["extensions"]]])
    restricted = sp.Matrix.vstack(arow * raw, brow * raw)
    frame = (raw * restricted.inv() * target).applyfunc(sp.cancel)
    assert_zero(mixed * frame, "normalized frame")
    assert frame.rank() == frame.cols
    return frame


def infinity_certificate(gamma, axis):
    cap_t, cap_x, cap_y = sp.symbols("T X Y")
    marking = (cap_t, 0, 0, 0) if axis == "h0" else (0, cap_t, 0, 0)
    if gamma == 2:
        assert axis == "origin"
        marking = (0, 0, 0, 0)
    model = build_model(gamma, "D01_infinity", 0, marking)
    target = sp.Matrix(((-4, 0), ((4 * cap_t if gamma == 0 else 0), 4)))
    frame = frame_from_diagonals(model, target)
    vector = frame * sp.Matrix((cap_x, cap_y))
    substitution = substitute_vector(model, vector)
    diagonal_a = sp.factor(model["A"].subs(substitution))
    diagonal_b = sp.factor(model["B"].subs(substitution))
    mode = 2
    determinant = sp.factor(
        marked_matrix(model, mode)
        .subs(substitution)
        .extract((0, 1, 2, 7), range(4))
        .det()
    )
    expected_b = 4 * (cap_t * cap_x + cap_y) if gamma == 0 else 4 * cap_y
    expected_det = (
        -32 * cap_x**2 * (cap_t * cap_x + cap_y)
        if gamma == 0
        else -32 * cap_x**2 * cap_y
    )
    assert_equal(diagonal_a, -4 * cap_x, "infinity A")
    assert_equal(diagonal_b, expected_b, "infinity B")
    assert_equal(determinant, expected_det, "infinity minor")
    assert model["mixed"].rank() == 6 and frame.cols == 2
    return {
        "gamma": gamma,
        "axis": axis,
        "mixed_rank": 6,
        "kernel_frame": [
            [str(sp.factor(frame[row, column])) for column in range(2)]
            for row in range(8)
        ],
        "A": str(diagonal_a),
        "B": str(diagonal_b),
        "marked_mode": mode,
        "minor_rows": [0, 1, 2, 7],
        "minor": str(determinant),
        "genuine_forces_rank_four": True,
    }


def no_genuine(model, diagonal, rank, label):
    assert model["mixed"].rank() == rank, (label, model["mixed"].rank())
    expression = model[diagonal]
    kernel = model["mixed"].nullspace()
    assert all(
        sp.factor(expression.subs(substitute_vector(model, vector))) == 0
        for vector in kernel
    )
    return {
        "label": label,
        "mixed_rank": rank,
        f"{diagonal}_on_complete_kernel": "zero",
    }


def wall_finite_d01(axis):
    cap_t, r, cap_x = sp.symbols("T r X", nonzero=True)
    marking = (cap_t, 0, 0, 0) if axis == "h0" else (0, cap_t, 0, 0)
    mode = 0 if axis == "h0" else 1
    model = build_model(2, "D01_finite", r, marking)
    assert model["mixed"].rank() == 7
    kernel = model["mixed"].nullspace()
    assert len(kernel) == 1
    vector = cap_x * kernel[0]
    substitution = substitute_vector(model, vector)
    diagonal_a = sp.factor(model["A"].subs(substitution))
    diagonal_b = sp.factor(model["B"].subs(substitution))
    assert_equal(diagonal_a, -2 * cap_x * r / (cap_t * r + 1), "wall finite A")
    assert_equal(diagonal_b, 2 * cap_x * (2 * r + 1), "wall finite B")
    marked = marked_matrix(model, mode).subs(substitution)
    dense = sp.factor(marked.extract((0, 4, 5, 7), range(4)).det())
    expected_dense = -16 * cap_t * cap_x**3 * r**2 * (2 * r + 1) / (cap_t * r + 1) ** 2
    assert_equal(dense, expected_dense, "wall dense minor")
    origin = sp.factor(marked.subs(cap_t, 0).extract((0, 5, 6, 7), range(4)).det())
    assert_equal(origin, -8 * cap_x**3 * r * (2 * r + 1), "wall origin minor")
    rows = (3, 4, 5, 7, 8, 12, 13)
    columns = (0, 1, 2, 3, 4, 5, 6)
    witness = sp.factor(model["mixed"].extract(rows, columns).det())
    assert_equal(witness, 64 * r**6 * (cap_t * r + 1), "wall rank witness")
    specials = [
        no_genuine(build_model(2, "D01_finite", 0, marking), "A", 1, f"{axis}:r=0"),
        no_genuine(
            build_model(2, "D01_finite", sp.Rational(-1, 2), marking),
            "B",
            7,
            f"{axis}:r=-1/2",
        ),
        no_genuine(
            build_model(2, "D01_finite", -1 / cap_t, marking), "B", 7, f"{axis}:Tr+1=0"
        ),
    ]
    return {
        "axis": axis,
        "mixed_rank": 7,
        "kernel": [str(sp.factor(value)) for value in kernel[0]],
        "rank_witness": str(witness),
        "A": str(diagonal_a),
        "B": str(diagonal_b),
        "dense_minor_rows": [0, 4, 5, 7],
        "dense_minor": str(dense),
        "origin_minor_rows": [0, 5, 6, 7],
        "origin_minor": str(origin),
        "special_fibres": specials,
        "every_genuine_finite_direction_rank_four": True,
    }


def offwall_finite_d01(axis):
    cap_t, slope, cap_c = sp.symbols("T s C")
    marking = (cap_t, 0, 0, 0) if axis == "h0" else (0, cap_t, 0, 0)
    mode = 0 if axis == "h0" else 1
    model = build_model(0, "D01_finite", slope, marking)
    vector = sp.Matrix((-1, -1, 0, -2 * cap_t, 2 * cap_t, cap_t, 1, 0))
    if axis == "h1":
        vector = sp.Matrix((-1, -1, 0, -2 * cap_t, cap_t, 2 * cap_t, 1, 0))
    assert_zero(model["mixed"] * vector, "offwall D01 kernel")
    rows = (3, 4, 5, 7, 9, 12, 13)
    columns = (0, 1, 2, 3, 4, 5, 7)
    witness = sp.factor(model["mixed"].extract(rows, columns).det())
    assert_equal(witness, -16 * slope**6, "offwall D01 witness")
    substitution = substitute_vector(model, cap_c * vector)
    diagonal_a = sp.factor(model["A"].subs(substitution))
    diagonal_b = sp.factor(model["B"].subs(substitution))
    assert_equal(diagonal_a, -4 * cap_c * slope, "offwall D01 A")
    assert_equal(diagonal_b, 4 * cap_c * (cap_t * slope + 1), "offwall D01 B")
    marked = marked_matrix(model, mode).subs(substitution)
    assert marked.rank() == 3
    specials = [
        no_genuine(build_model(0, "D01_finite", 0, marking), "A", 1, f"{axis}:s=0"),
        no_genuine(
            build_model(0, "D01_finite", -1 / cap_t, marking), "B", 7, f"{axis}:Ts+1=0"
        ),
    ]
    return {
        "axis": axis,
        "mixed_rank": 7,
        "kernel_generator": [str(value) for value in vector],
        "rank_witness": str(witness),
        "A": str(diagonal_a),
        "B": str(diagonal_b),
        "one_marked_rank": 3,
        "special_fibres": specials,
    }


def offwall_d23_factor_cover(axis):
    cap_t, r = sp.symbols("T r")
    cap_x, cap_y = sp.symbols("X Y")
    marking = (cap_t, 0, 0, 0) if axis == "h0" else (0, cap_t, 0, 0)
    mode = 0 if axis == "h0" else 1
    model = build_model(0, "D23_finite", r, marking)
    kernel = model["mixed"].nullspace()
    assert model["mixed"].rank() == 6 and len(kernel) == 2
    frame = sp.Matrix.hstack(*kernel)
    vector = frame * sp.Matrix((cap_x, cap_y))
    substitution = substitute_vector(model, vector)
    diagonal_a = sp.factor(model["A"].subs(substitution))
    diagonal_b = sp.factor(model["B"].subs(substitution))
    expected_b = (
        4 * (r + 1) * (cap_t * cap_x * (2 * r + 1) + cap_y * (r + 1)) / (4 * r + 1)
    )
    assert_equal(diagonal_a, 4 * cap_x, "offwall D23 A")
    assert_equal(diagonal_b, expected_b, "offwall D23 B")
    determinant = sp.factor(
        marked_matrix(model, mode)
        .subs(substitution)
        .extract((0, 1, 6, 7), range(4))
        .det()
    )
    expected_det = (
        32
        * cap_x
        * cap_y
        * r
        * (r + 1)
        * (2 * r - 1)
        * (cap_t * cap_x * (2 * r + 1) + cap_y * (r + 1))
        / ((2 * r + 1) * (4 * r + 1))
    )
    assert_equal(determinant, expected_det, "offwall D23 minor")
    rows = (3, 4, 5, 7, 9, 13)
    columns = (0, 1, 2, 3, 4, 5)
    witness = sp.factor(model["mixed"].extract(rows, columns).det())
    assert_equal(
        witness, -4 * (2 * r - 1) ** 2 * (2 * r + 1) * (4 * r + 1), "D23 witness"
    )
    assert marked_matrix(model, mode).subs(substitution).subs(cap_y, 0).rank() == 3

    zero_model = build_model(0, "D23_finite", 0, marking)
    zero_frame = sp.Matrix(
        (
            (-1, 0),
            (-1, 0),
            (0, 1),
            (-2 * cap_t, -1),
            (2 * cap_t, 1),
            (cap_t, 1),
            (1, 0),
            (0, 1),
        )
    )
    if axis == "h1":
        zero_frame = sp.Matrix(
            (
                (-1, 0),
                (-1, 0),
                (0, 1),
                (-2 * cap_t, -1),
                (cap_t, 1),
                (2 * cap_t, 1),
                (1, 0),
                (0, 1),
            )
        )
    assert_zero(zero_model["mixed"] * zero_frame, "D23 r0 frame")
    assert zero_model["mixed"].rank() == 6
    zero_vector = zero_frame * sp.Matrix((cap_x, cap_y))
    zero_substitution = substitute_vector(zero_model, zero_vector)
    assert_equal(zero_model["A"].subs(zero_substitution), 4 * cap_x, "D23 r0 A")
    assert_equal(
        zero_model["B"].subs(zero_substitution), 4 * (cap_t * cap_x + cap_y), "D23 r0 B"
    )
    assert marked_matrix(zero_model, mode).subs(zero_substitution).rank() == 3

    half_model = build_model(0, "D23_finite", sp.Rational(1, 2), marking)
    half_kernel = sp.Matrix.hstack(*half_model["mixed"].nullspace())
    half_vector = half_kernel * sp.Matrix((cap_x, cap_y))
    assert half_model["mixed"].rank() == 6
    assert (
        marked_matrix(half_model, mode)
        .subs(substitute_vector(half_model, half_vector))
        .rank()
        == 3
    )
    minus_half = no_genuine(
        build_model(0, "D23_finite", sp.Rational(-1, 2), marking),
        "B",
        6,
        f"{axis}:r=-1/2",
    )
    minus_one = no_genuine(
        build_model(0, "D23_finite", -1, marking), "B", 6, f"{axis}:r=-1"
    )

    quarter_model = build_model(0, "D23_finite", sp.Rational(-1, 4), marking)
    quarter_vector = sp.Matrix(
        (
            3 * cap_y / (2 * cap_t),
            3 * cap_y / (2 * cap_t),
            2 * cap_y,
            -2 * cap_x + 3 * cap_y,
            cap_x - 3 * cap_y / 2,
            cap_x,
            -3 * cap_y / (2 * cap_t),
            cap_y,
        )
    )
    if axis == "h1":
        quarter_vector = sp.Matrix(
            (
                3 * cap_y / (2 * cap_t),
                3 * cap_y / (2 * cap_t),
                2 * cap_y,
                -2 * cap_x + 3 * cap_y,
                cap_x,
                cap_x - 3 * cap_y / 2,
                -3 * cap_y / (2 * cap_t),
                cap_y,
            )
        )
    assert_zero(quarter_model["mixed"] * quarter_vector, "quarter frame")
    quarter_substitution = substitute_vector(quarter_model, quarter_vector)
    quarter_a = sp.factor(quarter_model["A"].subs(quarter_substitution))
    quarter_b = sp.factor(quarter_model["B"].subs(quarter_substitution))
    quarter_minor = sp.factor(
        marked_matrix(quarter_model, mode)
        .subs(quarter_substitution)
        .extract((0, 1, 6, 7), range(4))
        .det()
    )
    assert_equal(quarter_a, -6 * cap_y / cap_t, "quarter A")
    assert_equal(quarter_b, cap_x, "quarter B")
    assert_equal(quarter_minor, -9 * cap_x * cap_y**2 / cap_t, "quarter minor")
    quarter_zero = build_model(0, "D23_finite", sp.Rational(-1, 4), (0, 0, 0, 0))
    quarter_zero_frame = sp.Matrix.hstack(*quarter_zero["mixed"].nullspace())
    qz_vector = quarter_zero_frame * sp.Matrix((cap_x, cap_y))
    qz_sub = substitute_vector(quarter_zero, qz_vector)
    assert quarter_zero["mixed"].rank() == 6
    assert marked_matrix(quarter_zero, 0).subs(qz_sub).rank() == 3
    return {
        "axis": axis,
        "ordinary_mixed_rank": 6,
        "ordinary_kernel_frame": [
            [str(sp.factor(frame[row, column])) for column in range(2)]
            for row in range(8)
        ],
        "rank_witness": str(witness),
        "A": str(diagonal_a),
        "B": str(diagonal_b),
        "minor_rows": [0, 1, 6, 7],
        "minor": str(determinant),
        "rank_three_divisors": ["Y=0", "r=0", "r=1/2", "r=-1/4,T=0"],
        "r_zero_frame": [
            [str(value) for value in zero_frame.row(row)] for row in range(8)
        ],
        "r_half_rank": 3,
        "r_minus_quarter_T_nonzero": {
            "A": str(quarter_a),
            "B": str(quarter_b),
            "minor": str(quarter_minor),
        },
        "r_minus_quarter_T_zero_rank": 3,
        "nongenuine_specials": [minus_half, minus_one],
    }


def wall_d23_audit(axis):
    cap_t, r, cap_x = sp.symbols("T r X")
    marking = (cap_t, 0, 0, 0) if axis == "h0" else (0, cap_t, 0, 0)
    mode = 0 if axis == "h0" else 1
    model = build_model(2, "D23_finite", r, marking)
    kernel = model["mixed"].nullspace()
    assert model["mixed"].rank() == 7 and len(kernel) == 1
    vector = cap_x * kernel[0]
    substitution = substitute_vector(model, vector)
    denominator = cap_t * (2 * r + 1) + 6 * r
    diagonal_a = sp.factor(model["A"].subs(substitution))
    diagonal_b = sp.factor(model["B"].subs(substitution))
    assert_equal(diagonal_a, 12 * cap_x * r / denominator, "wall D23 A")
    assert_equal(diagonal_b, 4 * cap_x * (r + 1), "wall D23 B")
    determinant = sp.factor(
        marked_matrix(model, mode)
        .subs(substitution)
        .extract((0, 1, 5, 7), range(4))
        .det()
    )
    expected = 192 * cap_t * cap_x**3 * r**2 * (r + 1) / denominator**2
    assert_equal(determinant, expected, "wall D23 minor")
    t_zero = build_model(2, "D23_finite", r, (0, 0, 0, 0))
    t_zero_kernel = t_zero["mixed"].nullspace()
    assert len(t_zero_kernel) == 1
    tz_vector = cap_x * t_zero_kernel[0]
    assert (
        marked_matrix(t_zero, 0).subs(substitute_vector(t_zero, tz_vector)).rank() == 3
    )
    specials = [
        no_genuine(build_model(2, "D23_finite", 0, marking), "A", 7, f"{axis}:r=0"),
        no_genuine(build_model(2, "D23_finite", -1, marking), "B", 6, f"{axis}:r=-1"),
        no_genuine(
            build_model(
                2,
                "D23_finite",
                r,
                (-6 * r / (2 * r + 1), 0, 0, 0)
                if axis == "h0"
                else (0, -6 * r / (2 * r + 1), 0, 0),
            ),
            "B",
            7,
            f"{axis}:denominator=0",
        ),
    ]
    return {
        "axis": axis,
        "ordinary_mixed_rank": 7,
        "A": str(diagonal_a),
        "B": str(diagonal_b),
        "minor_rows": [0, 1, 5, 7],
        "minor": str(determinant),
        "T_zero_one_marked_rank": 3,
        "special_fibres": specials,
        "relevance": "D01 already obstructs every common marking",
    }


def surviving_pair(axis):
    cap_t, slope, cap_c, cap_u, cap_v = sp.symbols("T s C U V")
    marking = (cap_t, 0, 0, 0) if axis == "h0" else (0, cap_t, 0, 0)
    mode = 0 if axis == "h0" else 1
    d01 = build_model(0, "D01_finite", slope, marking)
    k = sp.Matrix((-1, -1, 0, -2 * cap_t, 2 * cap_t, cap_t, 1, 0))
    if axis == "h1":
        k = sp.Matrix((-1, -1, 0, -2 * cap_t, cap_t, 2 * cap_t, 1, 0))
    d23 = build_model(0, "D23_finite", 0, marking)
    f0 = k
    f1 = sp.Matrix((0, 0, 1, -1, 1, 1, 0, 1))
    assert_zero(d01["mixed"] * k, "candidate D01")
    assert_zero(d23["mixed"] * f0, "candidate D23 f0")
    assert_zero(d23["mixed"] * f1, "candidate D23 f1")
    d01_vector = cap_c * k
    d23_vector = cap_u * f0 + cap_v * f1
    d01_sub = substitute_vector(d01, d01_vector)
    d23_sub = substitute_vector(d23, d23_vector)
    assert_equal(d01["A"].subs(d01_sub), -4 * cap_c * slope, "candidate D01 A")
    assert_equal(
        d01["B"].subs(d01_sub), 4 * cap_c * (cap_t * slope + 1), "candidate D01 B"
    )
    assert_equal(d23["A"].subs(d23_sub), 4 * cap_u, "candidate D23 A")
    assert_equal(d23["B"].subs(d23_sub), 4 * (cap_t * cap_u + cap_v), "candidate D23 B")
    assert marked_matrix(d01, mode).subs(d01_sub).rank() == 3
    assert marked_matrix(d23, mode).subs(d23_sub).rank() == 3
    return {
        "axis": axis,
        "marking": [str(value) for value in marking],
        "D01": {
            "slope": "s",
            "kernel": [str(value) for value in k],
            "genuine_open": "C*s*(T*s+1)!=0",
            "one_marked_rank": 3,
        },
        "D23": {
            "slope": 0,
            "kernel_frame": [[str(f0[row]), str(f1[row])] for row in range(8)],
            "genuine_open": "U*(T*U+V)!=0",
            "one_marked_rank": 3,
        },
        "pair_status": "complete binary candidate; common ternary compatibility UNKNOWN",
    }


def main():
    geometry, projections = geometry_and_projections()
    result = {
        "status": "pass",
        "role": "proof_b",
        "date_utc": datetime.now(UTC).isoformat(),
        "git_commit": git_commit(),
        "claim_label": "CANDIDATE",
        "scope": "weighted-H22 on the two component-14 y=-r infinity endpoint faces of the verified component-20 p+q diagonal-DVR wall",
        "inputs": {
            path.name: sha256(path)
            for path in (P4_BOUNDARY, H31_ENDPOINT, H31_PRIMARY, H31_AUDIT)
        },
        "method": "direct homogeneous D01/D23 marked permanent reconstruction; exact saturated projections; complete symbolic kernels and bounded fixed minors",
        "command": "uv run --with sympy python derive_p5_h22_common_active_binary_triangle_p_plus_q_infinity_endpoint_candidate.py",
        "outputs": {
            NOTE.name: sha256(NOTE),
            Path(__file__).name: sha256(Path(__file__)),
        },
        "limitations": "CANDIDATE only; on-wall obstruction pending independent verification; off-wall finite-finite binary survivor has no proved ternary compatibility; no non-diagonal, gluing, or global claim",
        "geometry": geometry,
        "projections": projections,
        "D01_infinity": [
            infinity_certificate(0, "h0"),
            infinity_certificate(0, "h1"),
            infinity_certificate(2, "origin"),
        ],
        "wall_D01_finite": [wall_finite_d01("h0"), wall_finite_d01("h1")],
        "wall_D23_finite_audit": [wall_d23_audit("h0"), wall_d23_audit("h1")],
        "offwall_D01_finite": [offwall_finite_d01("h0"), offwall_finite_d01("h1")],
        "offwall_D23_factor_cover": [
            offwall_d23_factor_cover("h0"),
            offwall_d23_factor_cover("h1"),
        ],
        "surviving_binary_pair": [surviving_pair("h0"), surviving_pair("h1")],
        "wall_endpoint_weighted_H22_empty": "CANDIDATE",
        "offwall_endpoint_weighted_H22_status": "UNKNOWN; explicit complete binary candidate survives one-marked tests",
        "failed_or_timeout_branches": [
            {
                "attempt": "three inherited generic-component minor row sets on off-wall finite D01",
                "result": "all zero; full one-marked map rebuilt and proved rank three",
                "contributes_obstruction_evidence": False,
            }
        ],
        "finite_field_computation_used": False,
        "broad_minor_scan_used": False,
        "generic_component14_specialization_used": False,
        "global_Krenn_Gu_conjecture_resolved": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
