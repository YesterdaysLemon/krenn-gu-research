#!/usr/bin/env python3
"""Independent exact audit of the component-14 weighted-H22 endpoint note."""

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
TARGET = (
    ROOT
    / "P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_INFINITY_ENDPOINT_CANDIDATE.md"
)
REPORT = (
    ROOT
    / "P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_INFINITY_ENDPOINT_INDEPENDENT_VERIFICATION.md"
)

WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED_WORDS = WORDS[1:-1]


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


def permanent(rows: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    """Squarefree subset-DP permanent, independent of permutation expansion."""
    size = len(rows)
    state = {0: sp.Integer(1)}
    for row_index in range(size):
        updated: dict[int, sp.Expr] = {}
        for mask, value in state.items():
            for column in range(size):
                if mask & (1 << column):
                    continue
                new_mask = mask | (1 << column)
                updated[new_mask] = sp.expand(
                    updated.get(new_mask, 0) + value * rows[row_index][column]
                )
        state = updated
    return sp.expand(state[(1 << size) - 1])


def add(left, right):
    return tuple(sp.expand(a + b) for a, b in zip(left, right, strict=True))


def scale(coefficient, vector):
    return tuple(sp.expand(coefficient * value) for value in vector)


def endpoint_bases(gamma):
    e = (sp.Integer(1), 0, 0, 0)
    w = (0, 1, 1, 1)
    u = (0, 1, -1, 0)
    v1 = (0, 1, 1, 0)
    v2 = (0, 0, 0, 1)
    alpha = (e, e, scale(-1, u), add(scale(2, v2), scale(-1, v1)))
    beta = (w, w, e, add(scale(gamma, e), v1))
    return alpha, beta


def marked_bases(gamma, markings):
    alpha, beta = endpoint_bases(gamma)
    marked = tuple(
        add(beta[index], scale(markings[index], alpha[index])) for index in range(4)
    )
    return alpha, marked


def contract(row, extension, direction, slope=None):
    if direction == "D01_finite":
        return (slope * row[0] + row[1], row[2], row[3], extension)
    if direction == "D01_infinity":
        return (row[0], row[2], row[3], extension)
    if direction == "D23_finite":
        return (row[0], row[1], slope * row[2] + row[3], extension)
    if direction == "D23_infinity":
        return (row[0], row[1], row[2], extension)
    raise ValueError(direction)


def build_model(gamma, markings, direction, slope=None):
    alpha, beta = marked_bases(gamma, markings)
    z = sp.symbols("z0:8")
    alpha_rows = tuple(
        contract(alpha[index], z[index], direction, slope) for index in range(4)
    )
    beta_rows = tuple(
        contract(beta[index], z[4 + index], direction, slope) for index in range(4)
    )
    coefficients = {}
    for word in WORDS:
        rows = tuple(
            beta_rows[index] if word[index] else alpha_rows[index] for index in range(4)
        )
        coefficients[word] = permanent(rows)
    mixed = sp.Matrix(
        [[coefficients[word].coeff(variable) for variable in z] for word in MIXED_WORDS]
    )
    return {
        "z": z,
        "alpha_rows": alpha_rows,
        "beta_rows": beta_rows,
        "coefficients": coefficients,
        "mixed": mixed,
        "A": coefficients[WORDS[0]],
        "B": coefficients[WORDS[-1]],
    }


def one_marked_map(model, mode):
    other = tuple(index for index in range(4) if index != mode)
    rows = []
    for word in itertools.product((0, 1), repeat=3):
        selected = tuple(
            model["beta_rows"][index] if word[position] else model["alpha_rows"][index]
            for position, index in enumerate(other)
        )
        entries = []
        for coordinate in range(4):
            minor_rows = tuple(
                tuple(row[column] for column in range(4) if column != coordinate)
                for row in selected
            )
            entries.append(permanent(minor_rows))
        rows.append(tuple(entries))
    return sp.Matrix(rows)


def singular_command():
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    if shutil.which("wsl.exe"):
        return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")
    raise RuntimeError("Singular is required for exact projection replay")


def singular(expression):
    return str(sp.cancel(expression)).replace("**", "^")


def exact_projection(gamma, direction, expected, keep_slope):
    h = sp.symbols("h0:4")
    r = sp.Symbol("r")
    model = build_model(gamma, h, direction, r)
    ainv, binv = sp.symbols("ainv binv")
    equations = [
        *tuple(model["mixed"] * sp.Matrix(model["z"])),
        ainv * model["A"] - 1,
        binv * model["B"] - 1,
    ]
    eliminated = model["z"] + (ainv, binv)
    retained = h
    if direction.endswith("finite") and keep_slope:
        retained += (r,)
    elif direction.endswith("finite"):
        eliminated += (r,)
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
        timeout=45,
        check=False,
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), completed
    marker = [
        line for line in completed.stdout.splitlines() if line.startswith("RESULT:")
    ]
    assert len(marker) == 1 and marker[0].split(":")[1] == "1", (
        gamma,
        direction,
        keep_slope,
        completed.stdout,
    )
    return int(marker[0].split(":")[2])


def projection_audit():
    h0, h1, h2, h3, _r = sp.symbols("h0 h1 h2 h3 r")
    axis = (h3, h2, h0 * h1)
    cases = {
        (0, "D01_finite"): axis,
        (0, "D01_infinity"): axis,
        (0, "D23_finite"): axis,
        (0, "D23_infinity"): (sp.Integer(1),),
        (2, "D01_finite"): axis,
        (2, "D01_infinity"): (h3, h2, h0 + h1, h1**2),
        (2, "D23_finite"): axis,
        (2, "D23_infinity"): (sp.Integer(1),),
    }
    results = {}
    for (gamma, direction), expected in cases.items():
        sizes = [exact_projection(gamma, direction, expected, False)]
        if direction.endswith("finite"):
            expected_with_slope = expected
            sizes.append(exact_projection(gamma, direction, expected_with_slope, True))
        results[f"gamma{gamma}_{direction}"] = sizes
    return results


def assert_kernel(matrix, vectors, expected_nullity):
    assert all(
        all(sp.factor(entry) == 0 for entry in matrix * vector) for vector in vectors
    )
    assert matrix.cols - matrix.rank() == expected_nullity


def diagonal(model, name, vector):
    return sp.factor(model[name].subs(dict(zip(model["z"], vector, strict=True))))


def minor(matrix, rows, columns=range(4)):
    return sp.factor(matrix.extract(rows, columns).det(method="domain-ge"))


def assert_equal(actual, expected):
    assert sp.factor(actual - expected) == 0, (sp.factor(actual), sp.factor(expected))


def all_maximal_minors_zero(matrix):
    return all(
        sp.factor(minor(matrix, rows)) == 0
        for rows in itertools.combinations(range(matrix.rows), matrix.cols)
    )


def pure_tensor_audit():
    result = {}
    for gamma in (0, 2):
        alpha, beta = endpoint_bases(gamma)
        coefficients = {
            word: permanent(tuple(beta[i] if word[i] else alpha[i] for i in range(4)))
            for word in WORDS
        }
        assert coefficients[WORDS[-1]] == 4
        assert all(
            value == 0 for word, value in coefficients.items() if word != WORDS[-1]
        )
        result[str(gamma)] = str(coefficients[WORDS[-1]])
    return result


def axis_symmetry_audit():
    T, r = sp.symbols("T r")
    swap = {0: 1, 1: 0, 2: 2, 3: 3}
    checked = []
    for gamma in (0, 2):
        for direction in (
            "D01_finite",
            "D01_infinity",
            "D23_finite",
            "D23_infinity",
        ):
            left = build_model(gamma, (T, 0, 0, 0), direction, r)
            right = build_model(gamma, (0, T, 0, 0), direction, r)
            substitution = {
                right["z"][0]: left["z"][1],
                right["z"][1]: left["z"][0],
                right["z"][4]: left["z"][5],
                right["z"][5]: left["z"][4],
            }
            for index in (2, 3, 6, 7):
                substitution[right["z"][index]] = left["z"][index]
            for word in WORDS:
                swapped_word = tuple(word[swap[index]] for index in range(4))
                difference = sp.factor(
                    right["coefficients"][word].subs(substitution, simultaneous=True)
                    - left["coefficients"][swapped_word]
                )
                assert difference == 0, (gamma, direction, word, difference)
            checked.append(f"gamma{gamma}_{direction}")
    return checked


def covector_kills_complete_kernel(matrix, covector):
    return (
        matrix.col_join(
            sp.Matrix([[covector.coeff(variable) for variable in sp.symbols("z0:8")]])
        ).rank()
        == matrix.rank()
    )


def on_wall_d01_audit():
    T, r, X, Y = sp.symbols("T r X Y")
    model = build_model(2, (T, 0, 0, 0), "D01_finite", r)
    matrix = model["mixed"]
    denominator = T * r + 1
    kernel = sp.Matrix(
        (
            -1 / (2 * denominator),
            -1 / (2 * denominator),
            -T * r / denominator,
            -T * (r + 1) / denominator,
            T * (r + 1) / denominator,
            T * (2 * r + 1) / (2 * denominator),
            1 / (2 * denominator),
            1,
        )
    )
    assert all(sp.factor(entry) == 0 for entry in matrix * kernel)
    witness_rows = (3, 4, 5, 7, 8, 12, 13)
    witness_columns = (0, 1, 2, 3, 4, 5, 6)
    witness = sp.factor(
        matrix.extract(witness_rows, witness_columns).det(method="domain-ge")
    )
    assert_equal(witness, 64 * r**6 * denominator)
    assert_equal(diagonal(model, "A", kernel), -2 * r / denominator)
    assert_equal(diagonal(model, "B", kernel), 2 * (2 * r + 1))

    marked = one_marked_map(model, 0).subs(
        dict(zip(model["z"], X * kernel, strict=True))
    )
    first_minor = minor(marked, (0, 4, 5, 7))
    assert_equal(first_minor, -16 * T * X**3 * r**2 * (2 * r + 1) / denominator**2)
    second_minor = sp.factor(minor(marked, (0, 5, 6, 7)).subs(T, 0))
    assert_equal(second_minor, -8 * X**3 * r * (2 * r + 1))

    # Directly retain every divisor suppressed by the generic frame.
    special = {}
    zero = build_model(2, (T, 0, 0, 0), "D01_finite", 0)
    assert covector_kills_complete_kernel(zero["mixed"], zero["A"])
    special["r=0"] = {"rank": zero["mixed"].rank(), "killed": "A"}

    half = build_model(2, (T, 0, 0, 0), "D01_finite", -sp.Rational(1, 2))
    assert covector_kills_complete_kernel(half["mixed"], half["B"])
    half_intersection = half["mixed"].subs(T, 2)
    assert covector_kills_complete_kernel(half_intersection, half["B"].subs(T, 2))
    special["r=-1/2"] = {"rank": half["mixed"].rank(), "killed": "B"}

    pole = build_model(2, (-1 / r, 0, 0, 0), "D01_finite", r)
    assert covector_kills_complete_kernel(pole["mixed"], pole["B"])
    special["Tr+1=0"] = {"rank": pole["mixed"].rank(), "killed": "B"}

    infinity = build_model(2, (0, 0, 0, 0), "D01_infinity")
    v0 = sp.Matrix((-1, -1, 2, 2, -2, -2, 1, 0))
    v1 = sp.Matrix((0, 0, -1, -1, 1, 1, 0, 1))
    assert_kernel(infinity["mixed"], (v0, v1), 2)
    vector = X * v0 + Y * v1
    assert_equal(diagonal(infinity, "A", vector), -4 * X)
    assert_equal(diagonal(infinity, "B", vector), 4 * Y)
    infinity_marked = one_marked_map(infinity, 2).subs(
        dict(zip(infinity["z"], vector, strict=True))
    )
    infinity_minor = minor(infinity_marked, (0, 1, 2, 7))
    assert_equal(infinity_minor, -32 * X**2 * Y)
    return {
        "generic_rank_witness": str(witness),
        "generic_minors": [str(first_minor), str(second_minor)],
        "special_fibres": special,
        "infinity_rank": infinity["mixed"].rank(),
        "infinity_minor": str(infinity_minor),
        "every_projective_D01_direction_obstructed": True,
    }


def off_wall_d01_audit():
    T, s, C, X, Y = sp.symbols("T s C X Y")

    infinity = build_model(0, (T, 0, 0, 0), "D01_infinity")
    v0 = sp.Matrix((-1, -1, 0, -2 * T, 2 * T, T, 1, 0))
    v1 = sp.Matrix((0, 0, -1, -1, 1, 1, 0, 1))
    assert_kernel(infinity["mixed"], (v0, v1), 2)
    vector = X * v0 + Y * v1
    assert_equal(diagonal(infinity, "A", vector), -4 * X)
    assert_equal(diagonal(infinity, "B", vector), 4 * (T * X + Y))
    marked_infinity = one_marked_map(infinity, 2).subs(
        dict(zip(infinity["z"], vector, strict=True))
    )
    infinity_minor = minor(marked_infinity, (0, 1, 2, 7))
    assert_equal(infinity_minor, -32 * X**2 * (T * X + Y))

    finite = build_model(0, (T, 0, 0, 0), "D01_finite", s)
    kernel = sp.Matrix((-1, -1, 0, -2 * T, 2 * T, T, 1, 0))
    assert all(sp.factor(entry) == 0 for entry in finite["mixed"] * kernel)
    witness_rows = (3, 4, 5, 7, 9, 12, 13)
    witness_columns = (0, 1, 2, 3, 4, 5, 7)
    witness = sp.factor(
        finite["mixed"].extract(witness_rows, witness_columns).det(method="domain-ge")
    )
    assert_equal(witness, -16 * s**6)
    assert_equal(diagonal(finite, "A", kernel), -4 * s)
    assert_equal(diagonal(finite, "B", kernel), 4 * (T * s + 1))

    zero = build_model(0, (T, 0, 0, 0), "D01_finite", 0)
    assert covector_kills_complete_kernel(zero["mixed"], zero["A"])
    pole = build_model(0, (-1 / s, 0, 0, 0), "D01_finite", s)
    assert covector_kills_complete_kernel(pole["mixed"], pole["B"])

    marked_finite = one_marked_map(finite, 0).subs(
        dict(zip(finite["z"], C * kernel, strict=True))
    )
    assert all_maximal_minors_zero(marked_finite)
    rank_three_minor = sp.factor(
        marked_finite.extract((0, 6, 7), (0, 1, 2)).det(method="domain-ge")
    )
    assert_equal(rank_three_minor, -16 * C**3 * (T * s + 1))
    return {
        "infinity_minor": str(infinity_minor),
        "finite_rank_witness": str(witness),
        "finite_kernel": tuple(map(str, kernel)),
        "finite_diagonals": [str(-4 * C * s), str(4 * C * (T * s + 1))],
        "finite_one_marked_rank": 3,
        "finite_rank_three_minor": str(rank_three_minor),
    }


def off_wall_d23_audit():
    T, r, X, Y = sp.symbols("T r X Y")
    model = build_model(0, (T, 0, 0, 0), "D23_finite", r)
    matrix = model["mixed"]
    v0 = sp.Matrix(
        (
            -1,
            -1,
            0,
            2 * T * (2 * r - 1) / (4 * r + 1),
            2 * T * (r + 1) / (4 * r + 1),
            -T * (2 * r - 1) / (4 * r + 1),
            1,
            0,
        )
    )
    v1 = sp.Matrix(
        (
            0,
            0,
            1 / (2 * r + 1),
            -((2 * r - 1) ** 2) / ((2 * r + 1) * (4 * r + 1)),
            -(r + 1) * (2 * r - 1) / ((2 * r + 1) * (4 * r + 1)),
            -(r + 1) * (2 * r - 1) / ((2 * r + 1) * (4 * r + 1)),
            0,
            1,
        )
    )
    assert all(sp.factor(entry) == 0 for entry in matrix * v0)
    assert all(sp.factor(entry) == 0 for entry in matrix * v1)
    witness_rows = (3, 4, 5, 7, 9, 13)
    witness_columns = (0, 1, 2, 3, 4, 5)
    witness = sp.factor(
        matrix.extract(witness_rows, witness_columns).det(method="domain-ge")
    )
    expected_witness = -4 * (2 * r - 1) ** 2 * (2 * r + 1) * (4 * r + 1)
    assert_equal(witness, expected_witness)
    vector = X * v0 + Y * v1
    alpha = diagonal(model, "A", vector)
    beta = diagonal(model, "B", vector)
    expected_beta = 4 * (r + 1) * (T * X * (2 * r + 1) + Y * (r + 1)) / (4 * r + 1)
    assert_equal(alpha, 4 * X)
    assert_equal(beta, expected_beta)
    marked = one_marked_map(model, 0).subs(dict(zip(model["z"], vector, strict=True)))
    generic_minor = minor(marked, (0, 1, 6, 7))
    expected_minor = (
        32
        * X
        * Y
        * r
        * (r + 1)
        * (2 * r - 1)
        * (T * X * (2 * r + 1) + Y * (r + 1))
        / ((2 * r + 1) * (4 * r + 1))
    )
    assert_equal(generic_minor, expected_minor)

    # Ordinary Y=0 family: all 4-minors vanish and a 3-minor is nonzero on
    # the genuine ordinary open.
    y_zero = sp.factor(marked.subs(Y, 0))
    assert all_maximal_minors_zero(y_zero)
    y_zero_minor = sp.factor(
        y_zero.extract((0, 6, 7), (0, 2, 3)).det(method="domain-ge")
    )
    assert_equal(
        y_zero_minor,
        16 * T * X**2 * (r + 1) * (2 * r - 1) / (4 * r + 1),
    )

    # r=0: the exact complete frame is the displayed shared-pair frame.
    zero = build_model(0, (T, 0, 0, 0), "D23_finite", 0)
    f0 = sp.Matrix((-1, -1, 0, -2 * T, 2 * T, T, 1, 0))
    f1 = sp.Matrix((0, 0, 1, -1, 1, 1, 0, 1))
    assert_kernel(zero["mixed"], (f0, f1), 2)
    zero_vector = X * f0 + Y * f1
    assert_equal(diagonal(zero, "A", zero_vector), 4 * X)
    assert_equal(diagonal(zero, "B", zero_vector), 4 * (T * X + Y))
    zero_marked = one_marked_map(zero, 0).subs(
        dict(zip(zero["z"], zero_vector, strict=True))
    )
    assert all_maximal_minors_zero(zero_marked)
    zero_three = sp.factor(
        zero_marked.extract((0, 6, 7), (0, 2, 3)).det(method="domain-ge")
    )
    assert_equal(zero_three, -16 * X * (T * X + Y))

    # r=1/2: all candidates survive the rank-four test, but the claimed
    # "rank exactly three throughout" has a genuine rank-two subfamily Y=0.
    half = build_model(0, (T, 0, 0, 0), "D23_finite", sp.Rational(1, 2))
    g0 = sp.Matrix((-1, -1, 0, 0, T, 0, 1, 0))
    g1 = sp.Matrix((0, 0, sp.Rational(1, 2), 0, 0, 0, 0, 1))
    assert_kernel(half["mixed"], (g0, g1), 2)
    half_vector = X * g0 + Y * g1
    assert_equal(diagonal(half, "A", half_vector), 4 * X)
    assert_equal(diagonal(half, "B", half_vector), 4 * T * X + 3 * Y)
    half_marked = one_marked_map(half, 0).subs(
        dict(zip(half["z"], half_vector, strict=True))
    )
    assert all_maximal_minors_zero(half_marked)
    assert half_marked.subs(Y, 0).rank() == 2
    assert_equal(diagonal(half, "A", g0), 4)
    assert_equal(diagonal(half, "B", g0), 4 * T)
    half_three = sp.factor(
        half_marked.extract((0, 1, 7), (1, 2, 3)).det(method="domain-ge")
    )
    assert_equal(half_three, -3 * Y**2)

    # r=-1/4, T!=0: direct local frame and unique rank-four obstruction.
    minus_quarter = build_model(0, (T, 0, 0, 0), "D23_finite", -sp.Rational(1, 4))
    q0 = sp.Matrix((0, 0, 0, -2, 1, 1, 0, 0))
    q1 = sp.Matrix(
        (3 / (2 * T), 3 / (2 * T), 2, 3, -sp.Rational(3, 2), 0, -3 / (2 * T), 1)
    )
    assert_kernel(minus_quarter["mixed"], (q0, q1), 2)
    quarter_vector = X * q0 + Y * q1
    assert_equal(diagonal(minus_quarter, "A", quarter_vector), -6 * Y / T)
    assert_equal(diagonal(minus_quarter, "B", quarter_vector), X)
    quarter_marked = one_marked_map(minus_quarter, 0).subs(
        dict(zip(minus_quarter["z"], quarter_vector, strict=True))
    )
    quarter_minor = minor(quarter_marked, (0, 1, 6, 7))
    assert_equal(quarter_minor, -9 * X * Y**2 / T)

    quarter_zero = build_model(0, (0, 0, 0, 0), "D23_finite", -sp.Rational(1, 4))
    qz0 = sp.Matrix((0, 0, 0, -2, 1, 1, 0, 0))
    qz1 = sp.Matrix((-1, -1, 0, 0, 0, 0, 1, 0))
    assert_kernel(quarter_zero["mixed"], (qz0, qz1), 2)
    quarter_zero_vector = X * qz0 + Y * qz1
    assert_equal(diagonal(quarter_zero, "A", quarter_zero_vector), 4 * Y)
    assert_equal(diagonal(quarter_zero, "B", quarter_zero_vector), X)
    quarter_zero_marked = one_marked_map(quarter_zero, 0).subs(
        dict(zip(quarter_zero["z"], quarter_zero_vector, strict=True))
    )
    assert all_maximal_minors_zero(quarter_zero_marked)
    quarter_zero_three = sp.factor(
        quarter_zero_marked.extract((0, 6, 7), (1, 2, 3)).det(method="domain-ge")
    )
    assert_equal(quarter_zero_three, -3 * X**2)

    nongenuine = {}
    for label, value in (("r=-1/2", -sp.Rational(1, 2)), ("r=-1", -1)):
        special = build_model(0, (T, 0, 0, 0), "D23_finite", value)
        assert covector_kills_complete_kernel(special["mixed"], special["B"])
        nongenuine[label] = {"rank": special["mixed"].rank(), "killed": "B"}

    return {
        "generic_rank_witness": str(witness),
        "generic_diagonals": [str(alpha), str(beta)],
        "generic_factor_minor": str(generic_minor),
        "ordinary_Y_zero_rank": 3,
        "ordinary_Y_zero_minor": str(y_zero_minor),
        "r_zero_rank": 3,
        "r_zero_frame": [tuple(map(str, f0)), tuple(map(str, f1))],
        "r_half_generic_rank": 3,
        "r_half_Y_zero_rank": 2,
        "r_half_Y_zero_is_genuine_when": "T!=0",
        "r_minus_quarter_T_nonzero_minor": str(quarter_minor),
        "r_minus_quarter_T_zero_rank": 3,
        "nongenuine_special_fibres": nongenuine,
        "complete_rank_at_most_three_survivors": [
            "r=0",
            "r=1/2",
            "ordinary Y=0 with T!=0 and B!=0",
            "r=-1/4,T=0",
        ],
    }


def shared_extension_slope_audit():
    T, r = sp.symbols("T r")
    axis_data = (
        ((T, 0, 0, 0), sp.Matrix((-1, -1, 0, -2 * T, 2 * T, T, 1, 0))),
        ((0, T, 0, 0), sp.Matrix((-1, -1, 0, -2 * T, T, 2 * T, 1, 0))),
    )
    results = []
    for markings, kernel in axis_data:
        model = build_model(0, markings, "D23_finite", r)
        mixed_values = tuple(sp.factor(value) for value in model["mixed"] * kernel)
        nonzero = tuple(
            (index, str(value))
            for index, value in enumerate(mixed_values)
            if value != 0
        )
        assert nonzero == ((13, "-12*T*r"),)
        assert_equal(diagonal(model, "A", kernel), 4)
        assert_equal(diagonal(model, "B", kernel), 4 * T * (2 * r + 1))
        results.append(
            {
                "marking_axis": str(markings),
                "sole_nonzero_mixed_row": nonzero[0],
                "D23_diagonals": ["4", "4*T*(2*r+1)"],
            }
        )
    return {
        "axes": results,
        "common_genuineness_forces_T_nonzero": True,
        "shared_extension_forces_r_zero": True,
        "reduced_shared_extension_type": "D23(r=0)",
    }


def main():
    pure = pure_tensor_audit()
    projections = projection_audit()
    symmetry = axis_symmetry_audit()
    on_wall = on_wall_d01_audit()
    off_wall_d01 = off_wall_d01_audit()
    off_wall_d23 = off_wall_d23_audit()
    shared_slope = shared_extension_slope_audit()
    assert off_wall_d01["finite_kernel"] == off_wall_d23["r_zero_frame"][0]
    output = {
        "role": "verifier",
        "date_utc": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "git_commit": git_commit(),
        "claim_label": "REFUTED",
        "scope": "independent audit of original component-14 endpoint one-neighbour analysis only",
        "inputs": {TARGET.name: sha256(TARGET)},
        "method": "independent subset-DP permanents, exact characteristic-zero elimination, complete kernels, and one-marked minors",
        "command": "uv run --with sympy python audit_p5_h22_common_active_binary_triangle_p_plus_q_infinity_endpoint_candidate_verifier.py",
        "outputs": {
            REPORT.name: sha256(REPORT),
            Path(__file__).name: sha256(Path(__file__)),
        },
        "limitations": "later two-neighbour compatibility theorem excluded; no global or local-to-global claim",
        "pure_tensor": pure,
        "projection_standard_basis_sizes": projections,
        "mode_axis_symmetry_cases": symmetry,
        "on_wall_D01": on_wall,
        "off_wall_D01": off_wall_d01,
        "off_wall_D23": off_wall_d23,
        "shared_extension_slope": shared_slope,
        "on_wall_weighted_H22_fibre_empty_verified": True,
        "off_wall_factor_cover_verified_up_to_rank_at_most_three": True,
        "shared_pair_type_verified": True,
        "refuted_statement": (
            "at off-wall D23 slope r=1/2 every genuine kernel point has "
            "marked rank exactly three"
        ),
        "counterexample_family": (
            "h=(T,0,0,0), r=1/2, extension=(-1,-1,0,0,T,0,1,0), "
            "T!=0: A=4, B=4T, marked-mode-0 rank=2"
        ),
        "survivor_boundary_changed_by_refutation": False,
        "target": TARGET.name,
        "target_sha256": sha256(TARGET),
        "report": REPORT.name,
        "report_sha256": sha256(REPORT),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
