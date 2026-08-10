#!/usr/bin/env python3
"""Exact certificate for component 21's vertical-U0 projective boundary."""

from __future__ import annotations

import hashlib
import itertools
import json
import shutil
import subprocess
import time
from pathlib import Path

import sympy as sp
import sys

for _parent in Path(__file__).resolve().parents:
    if (_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        sys.path.insert(0, str(_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_COMPONENT21_VERTICAL_U0_PROJECTIVE_BOUNDARY_COMPLETE_OBSTRUCTION.md"
WORDS = tuple(itertools.product((0, 1), repeat=4))
MIXED = WORDS[1:-1]
PERMUTATIONS3 = tuple(itertools.permutations(range(3)))
PERMUTATIONS4 = tuple(itertools.permutations(range(4)))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def add(*rows: tuple[sp.Expr, ...]) -> tuple[sp.Expr, ...]:
    return tuple(sp.expand(sum(row[index] for row in rows)) for index in range(4))


def scale(value: sp.Expr, row: tuple[sp.Expr, ...]) -> tuple[sp.Expr, ...]:
    return tuple(sp.expand(value * entry) for entry in row)


def permanent3(rows: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[i][permutation[i]] for i in range(3))
            for permutation in PERMUTATIONS3
        )
    )


def permanent4(rows: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[i][permutation[i]] for i in range(4))
            for permutation in PERMUTATIONS4
        )
    )


def finite_basis(
    alpha_parameter: sp.Expr,
    kappa: sp.Expr,
    ell: sp.Expr,
) -> tuple[tuple[tuple[sp.Expr, ...], ...], tuple[tuple[sp.Expr, ...], ...]]:
    cap_a = (sp.Integer(1), sp.Integer(1), sp.Integer(0), sp.Integer(0))
    cap_c = (sp.Integer(1), sp.Integer(-1), sp.Integer(0), sp.Integer(0))
    cap_b = (sp.Integer(0), sp.Integer(0), sp.Integer(1), sp.Integer(1))
    cap_d = (sp.Integer(0), sp.Integer(0), sp.Integer(1), sp.Integer(-1))
    alpha = (
        add(cap_a, scale(-alpha_parameter, cap_c)),
        add(scale(ell, cap_a), cap_c),
        cap_c,
        cap_d,
    )
    beta = (
        cap_b,
        cap_a,
        add(cap_b, scale(kappa, cap_a)),
        add(cap_a, scale(ell, cap_c)),
    )
    return alpha, beta


def infinity_basis(
    alpha_parameter: sp.Expr,
    kappa: sp.Expr,
) -> tuple[tuple[tuple[sp.Expr, ...], ...], tuple[tuple[sp.Expr, ...], ...]]:
    cap_a = (sp.Integer(1), sp.Integer(1), sp.Integer(0), sp.Integer(0))
    cap_c = (sp.Integer(1), sp.Integer(-1), sp.Integer(0), sp.Integer(0))
    cap_b = (sp.Integer(0), sp.Integer(0), sp.Integer(1), sp.Integer(1))
    cap_d = (sp.Integer(0), sp.Integer(0), sp.Integer(1), sp.Integer(-1))
    return (
        (add(cap_a, scale(-alpha_parameter, cap_c)), cap_a, cap_c, cap_d),
        (cap_b, cap_c, add(cap_b, scale(kappa, cap_a)), cap_c),
    )


def shifted(
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
    shifts: tuple[sp.Expr, ...],
) -> tuple[tuple[sp.Expr, ...], ...]:
    return tuple(add(beta[i], scale(shifts[i], alpha[i])) for i in range(4))


def extension_coefficients(
    distinguished: int,
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
    extension: sp.Matrix,
) -> dict[tuple[int, ...], sp.Expr]:
    retained = tuple(index for index in range(4) if index != distinguished)
    alpha_p = tuple(
        tuple(alpha[mode][index] for index in retained) + (extension[mode],)
        for mode in range(4)
    )
    beta_p = tuple(
        tuple(beta[mode][index] for index in retained) + (extension[4 + mode],)
        for mode in range(4)
    )
    return {
        word: permanent4(
            tuple(beta_p[i] if word[i] else alpha_p[i] for i in range(4))
        )
        for word in WORDS
    }


def mixed_matrix(
    distinguished: int,
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
) -> tuple[sp.Matrix, sp.Matrix, sp.Matrix]:
    extension = sp.Matrix(sp.symbols("z0:8"))
    coefficients = extension_coefficients(distinguished, alpha, beta, extension)
    mixed = sp.Matrix(
        [
            [sp.diff(coefficients[word], value) for value in extension]
            for word in MIXED
        ]
    )
    diagonal_alpha = sp.Matrix(
        [[sp.diff(coefficients[WORDS[0]], value) for value in extension]]
    )
    diagonal_beta = sp.Matrix(
        [[sp.diff(coefficients[WORDS[-1]], value) for value in extension]]
    )
    return mixed, diagonal_alpha, diagonal_beta


def one_marked_map(
    mode: int,
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
) -> sp.Matrix:
    rows = []
    for word in itertools.product((0, 1), repeat=3):
        selected: list[tuple[sp.Expr, ...] | None] = []
        bit = 0
        for other in range(4):
            if other == mode:
                selected.append(None)
            else:
                selected.append(beta[other] if word[bit] else alpha[other])
                bit += 1
        coefficient_row = []
        for coordinate in range(4):
            basis = tuple(sp.Integer(index == coordinate) for index in range(4))
            coefficient_row.append(
                permanent4(
                    tuple(
                        basis if other == mode else selected[other]  # type: ignore[arg-type]
                        for other in range(4)
                    )
                )
            )
        rows.append(coefficient_row)
    return sp.Matrix(rows)


def marked_extension(
    distinguished: int,
    extension: sp.Matrix,
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
    mode: int,
) -> sp.Matrix:
    retained = tuple(index for index in range(4) if index != distinguished)
    alpha_p = tuple(
        tuple(alpha[row][index] for index in retained) + (extension[row],)
        for row in range(4)
    )
    beta_p = tuple(
        tuple(beta[row][index] for index in retained) + (extension[4 + row],)
        for row in range(4)
    )
    return one_marked_map(mode, alpha_p, beta_p)


def project(
    row: tuple[sp.Expr, ...],
    extension: sp.Expr,
    direction: str,
    chart: str,
    slope: sp.Expr,
) -> tuple[sp.Expr, ...]:
    if direction == "D01" and chart == "finite":
        return (slope * row[0] + row[1], row[2], row[3], extension)
    if direction == "D23" and chart == "finite":
        return (row[0], row[1], slope * row[2] + row[3], extension)
    if direction == "D01" and chart == "infinity":
        return (row[0], row[2], row[3], extension)
    if direction == "D23" and chart == "infinity":
        return (row[0], row[1], row[2], extension)
    raise ValueError((direction, chart))


def contraction_model(
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
    direction: str,
    chart: str,
    slope: sp.Expr,
) -> dict[str, object]:
    extension = sp.symbols("z0:8")
    alpha_p = tuple(
        project(alpha[i], extension[i], direction, chart, slope) for i in range(4)
    )
    beta_p = tuple(
        project(beta[i], extension[4 + i], direction, chart, slope)
        for i in range(4)
    )
    coefficients: dict[tuple[int, ...], sp.Expr] = {}
    for word in WORDS:
        selected = tuple(beta_p[i] if word[i] else alpha_p[i] for i in range(4))
        coefficients[word] = sp.expand(
            sum(
                selected[i][3]
                * permanent3(tuple(selected[j][:3] for j in range(4) if j != i))
                for i in range(4)
            )
        )
    mixed = sp.Matrix(
        [[sp.diff(coefficients[word], value) for value in extension] for word in MIXED]
    )
    return {
        "alpha_rows": alpha_p,
        "beta_rows": beta_p,
        "coefficients": coefficients,
        "mixed": mixed,
        "A": coefficients[WORDS[0]],
        "B": coefficients[WORDS[-1]],
    }


def contraction_one_marked(model: dict[str, object], mode: int) -> sp.Matrix:
    alpha_rows = model["alpha_rows"]
    beta_rows = model["beta_rows"]
    assert isinstance(alpha_rows, tuple) and isinstance(beta_rows, tuple)
    rows = []
    for word in itertools.product((0, 1), repeat=3):
        others = tuple(index for index in range(4) if index != mode)
        selected = tuple(
            beta_rows[index] if word[position] else alpha_rows[index]
            for position, index in enumerate(others)
        )
        rows.append(
            tuple(
                permanent3(
                    tuple(tuple(row[j] for j in range(4) if j != omitted) for row in selected)
                )
                for omitted in range(4)
            )
        )
    return sp.Matrix(rows)


def singular_command() -> tuple[str, ...]:
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    if shutil.which("wsl.exe"):
        return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")
    raise RuntimeError("Singular is required")


def singular(expression: sp.Expr) -> str:
    return str(sp.cancel(expression)).replace("**", "^")


FINITE_PRIMES = (
    "h3,h2,h1,kappa,alpha+ell",
    "h3,h2,h1,ell+1,kappa",
    "h3,h2,h1,ell-1,kappa",
    (
        "kappa*ell-h2,(2*alpha*ell+ell^2+1)*h1+alpha+ell,"
        "2*alpha*h1*h2+ell*h1*h2+alpha*kappa+kappa*h1+h2,h3,h0"
    ),
    "h3,h0,ell+1,kappa+h2",
    "h3,h0,ell-1,kappa-h2",
    "(ell-1)*h1+1,h3,h0,alpha+1",
    "(ell+1)*h1+1,h3,h0,alpha-1",
    "(alpha-1)*h1+1,h3,h0,ell+1",
    "(alpha+1)*h1+1,h3,h0,ell-1",
)

INFINITY_PRIMES = (
    "h3,h1+1,h0,alpha+h1",
    "h3,h1-1,h0,alpha+h1",
    "h3,h0,kappa,alpha+h1",
)


def decomposition_tail(
    source_ring: str,
    target_variables: tuple[str, ...],
    primes: tuple[str, ...],
) -> list[str]:
    lines = [
        "ring S=0,(" + ",".join(target_variables) + "),dp;",
        f"ideal J=imap({source_ring},J);",
        'LIB "primdec.lib";',
        "list L=minAssGTZ(J);",
    ]
    for index, generators in enumerate(primes, start=1):
        lines.extend(
            (
                f"ideal E{index}={generators};",
                f"ideal A{index}=L[{index}];",
                f"ideal X{index}=simplify(reduce(A{index},E{index}),2);",
                f"ideal Y{index}=simplify(reduce(E{index},A{index}),2);",
            )
        )
    checks = "+".join(
        f'string((size(X{index})==0)&&(size(Y{index})==0))+":"'
        for index in range(1, len(primes) + 1)
    )
    lines.append(
        '"CODEX_RESULT:"+string(size(J))+":"+string(size(L))+":"+'
        + checks
        + '+"END";'
    )
    lines.append("quit;")
    return lines


def run_singular(program: str, timeout: int = 300) -> tuple[int, int]:
    completed = subprocess.run(
        singular_command(),
        input=program,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=timeout,
        check=False,
    )
    assert completed.returncode == 0 and not completed.stderr.strip(), (
        completed.stdout,
        completed.stderr,
    )
    markers = [
        line for line in completed.stdout.splitlines() if line.startswith("CODEX_RESULT:")
    ]
    assert len(markers) == 1, completed.stdout
    fields = markers[0].split(":")
    assert fields[-1] == "END"
    assert all(field == "1" for field in fields[3:-1]), markers[0]
    return int(fields[1]), int(fields[2])


def h31_global_decomposition(
    distinguished: int,
    at_infinity: bool,
) -> tuple[int, int]:
    alpha_parameter, kappa, ell = sp.symbols("alpha kappa ell")
    shifts = sp.symbols("h0:4")
    extension = sp.symbols("z0:8")
    inverse = sp.Symbol("v")
    if at_infinity:
        alpha, canonical_beta = infinity_basis(alpha_parameter, kappa)
        retained_symbols = (alpha_parameter, kappa) + shifts
        retained_names = ("alpha", "kappa", "h0", "h1", "h2", "h3")
        primes = INFINITY_PRIMES
    else:
        alpha, canonical_beta = finite_basis(alpha_parameter, kappa, ell)
        retained_symbols = (alpha_parameter, kappa, ell) + shifts
        retained_names = ("alpha", "kappa", "ell", "h0", "h1", "h2", "h3")
        primes = FINITE_PRIMES
    beta = shifted(alpha, canonical_beta, shifts)
    mixed, diagonal_alpha, diagonal_beta = mixed_matrix(distinguished, alpha, beta)
    vector = sp.Matrix(extension)
    equations = tuple(mixed * vector) + (
        sp.expand((diagonal_alpha * vector)[0] - 1),
        sp.expand(inverse * (diagonal_beta * vector)[0] - 1),
    )
    eliminated = extension + (inverse,)
    variables = eliminated + retained_symbols
    lines = [
        "ring R=0,("
        + ",".join(map(str, variables))
        + f"),(dp({len(eliminated)}),dp({len(retained_symbols)}));",
        "option(redSB);",
        "ideal I=" + ",".join(map(singular, equations)) + ";",
        "I=slimgb(I);",
        "ideal J=std(eliminate(I," + "*".join(map(str, eliminated)) + "));",
    ]
    lines.extend(decomposition_tail("R", retained_names, primes))
    return run_singular("\n".join(lines))


def h22_global_decomposition(chart: str, at_infinity: bool) -> tuple[int, int]:
    alpha_parameter, kappa, ell, slope = sp.symbols("alpha kappa ell lambda")
    shifts = sp.symbols("h0:4")
    extension = sp.symbols("z0:8")
    inverse_a, inverse_b = sp.symbols("u v")
    if at_infinity:
        alpha, canonical_beta = infinity_basis(alpha_parameter, kappa)
        retained_symbols = (alpha_parameter, kappa) + shifts
        primes = INFINITY_PRIMES
        retained_names = ("alpha", "kappa", "h0", "h1", "h2", "h3")
    else:
        alpha, canonical_beta = finite_basis(alpha_parameter, kappa, ell)
        retained_symbols = (alpha_parameter, kappa, ell) + shifts
        primes = FINITE_PRIMES
        retained_names = ("alpha", "kappa", "ell", "h0", "h1", "h2", "h3")
    if chart == "finite":
        retained_symbols += (slope,)
        retained_names += ("lambda",)
    beta = shifted(alpha, canonical_beta, shifts)
    d01 = contraction_model(alpha, beta, "D01", chart, slope)
    d23 = contraction_model(alpha, beta, "D23", chart, slope)
    d01_coefficients = d01["coefficients"]
    d23_mixed = d23["mixed"]
    assert isinstance(d01_coefficients, dict) and isinstance(d23_mixed, sp.Matrix)
    equations = (
        *(d01_coefficients[word] for word in WORDS[:-1]),
        sp.expand(d01["B"] - 1),  # type: ignore[operator]
        *tuple(d23_mixed * sp.Matrix(extension)),
        sp.expand(inverse_a * d23["A"] - 1),  # type: ignore[operator]
        sp.expand(inverse_b * d23["B"] - 1),  # type: ignore[operator]
    )
    eliminated = extension + (inverse_a, inverse_b)
    variables = eliminated + retained_symbols
    lines = [
        "ring R=0,("
        + ",".join(map(str, variables))
        + f"),(dp({len(eliminated)}),dp({len(retained_symbols)}));",
        "option(redSB);",
        "ideal I=" + ",".join(map(singular, equations)) + ";",
        "I=slimgb(I);",
        "ideal J=std(eliminate(I," + "*".join(map(str, eliminated)) + "));",
    ]
    lines.extend(decomposition_tail("R", retained_names, primes))
    return run_singular("\n".join(lines))


def assert_frame(matrix: sp.Matrix, frame: sp.Matrix, rank: int) -> None:
    assert frame.rank() == frame.cols
    assert all(sp.factor(value) == 0 for value in matrix * frame)
    assert matrix.rank() == rank


def h31_branch_certificates() -> dict[str, object]:
    a, k, ell, parameter = sp.symbols("alpha kappa ell T")
    c0, c1, c2 = sp.symbols("c0 c1 c2")
    results: dict[str, object] = {}

    def check(
        label: str,
        substitutions: dict[sp.Symbol, sp.Expr],
        shifts: tuple[sp.Expr, ...],
        frames: dict[int, tuple[sp.Matrix, ...]],
        rows: dict[int, tuple[int, ...]],
        expected_minors: dict[int, sp.Expr],
        expected_diagonals: dict[int, tuple[sp.Expr, sp.Expr]],
        rank: int = 6,
    ) -> None:
        alpha, canonical_beta = finite_basis(a, k, ell)
        alpha = tuple(
            tuple(sp.factor(value.subs(substitutions)) for value in row) for row in alpha
        )
        canonical_beta = tuple(
            tuple(sp.factor(value.subs(substitutions)) for value in row)
            for row in canonical_beta
        )
        marked = shifted(
            alpha,
            canonical_beta,
            tuple(
                sp.factor(sp.sympify(value).subs(substitutions)) for value in shifts
            ),
        )
        for distinguished in (2, 3):
            mixed, diagonal_alpha, diagonal_beta = mixed_matrix(
                distinguished, alpha, marked
            )
            frame = sp.Matrix.hstack(*frames[distinguished])
            assert_frame(mixed, frame, rank)
            coefficients = (c0, c1, c2)[: frame.cols]
            extension = frame * sp.Matrix(coefficients)
            actual_diagonals = (
                sp.factor((diagonal_alpha * extension)[0]),
                sp.factor((diagonal_beta * extension)[0]),
            )
            assert all(
                sp.factor(actual_diagonals[index] - expected_diagonals[distinguished][index])
                == 0
                for index in range(2)
            )
            marked_map = marked_extension(
                distinguished, extension, alpha, marked, 3
            )
            determinant = sp.factor(
                marked_map.extract(rows[distinguished], range(4)).det()
            )
            assert sp.factor(determinant - expected_minors[distinguished]) == 0
            pure_column = one_marked_map(3, alpha, marked)[:, distinguished]
            assert any(sp.factor(value) != 0 for value in pure_column)
        results[label] = {"rank": rank, "kernel_dimension": len(frames[2])}

    # Prime 1.
    q1 = parameter * c0 * (ell**2 - 1) - 2 * c1
    p1_frames = {
        2: (
            sp.Matrix((ell**2 - 1, 0, ell, 0, 0, 1, 0, 0)),
            sp.Matrix((0, 0, 0, 1, 1, 0, 1, 0)),
        ),
        3: (
            sp.Matrix((ell**2 - 1, 0, ell, 0, 0, 1, 0, 0)),
            sp.Matrix((0, 0, 0, -1, 1, 0, 1, 0)),
        ),
    }
    check(
        "prime_1",
        {a: -ell, k: 0},
        (parameter, 0, 0, 0),
        p1_frames,
        {2: (0, 4, 6, 7), 3: (0, 4, 6, 7)},
        {2: 8 * c0**2 * (ell**2 - 1) * q1, 3: 8 * c0**2 * (ell**2 - 1) * q1},
        {
            2: (2 * c0 * (ell**2 - 1), -2 * q1),
            3: (-2 * c0 * (ell**2 - 1), -2 * q1),
        },
    )

    # Prime 3; prime 2 is its source swap.
    q3 = -parameter * a * c1 + parameter * c1 + 2 * c0
    p3_frames = {
        2: (
            sp.Matrix((0, 0, 0, 1, 1, 0, 1, 0)),
            sp.Matrix((-1, -1, 0, 0, -parameter * a, 0, 0, 1)),
        ),
        3: (
            sp.Matrix((0, 0, 0, -1, 1, 0, 1, 0)),
            sp.Matrix((-1, -1, 0, 0, -parameter * a, 0, 0, 1)),
        ),
    }
    check(
        "prime_3",
        {ell: 1, k: 0},
        (parameter, 0, 0, 0),
        p3_frames,
        {2: (0, 3, 4, 7), 3: (0, 3, 4, 7)},
        {2: -8 * c1**2 * (a - 1) * q3, 3: -8 * c1**2 * (a - 1) * q3},
        {2: (2 * c1 * (a - 1), 2 * q3), 3: (-2 * c1 * (a - 1), 2 * q3)},
    )

    # Prime 4, the dense branch.
    e = 2 * a * ell + ell**2 + 1
    q4 = k * (ell**2 - 1) * c0 - 2 * c1
    p4_frames = {
        2: (
            sp.Matrix((-a * ell - 1, 0, ell, 0, 0, 1, 0, 0)),
            sp.Matrix((0, 0, 0, 1, 1, 0, 1, 0)),
        ),
        3: (
            sp.Matrix((-a * ell - 1, 0, ell, 0, 0, 1, 0, 0)),
            sp.Matrix((0, 0, 0, -1, 1, 0, 1, 0)),
        ),
    }
    alpha, canonical_beta = finite_basis(a, k, ell)
    marked = shifted(alpha, canonical_beta, (0, -(a + ell) / e, k * ell, 0))
    for distinguished in (2, 3):
        mixed, diagonal_alpha, diagonal_beta = mixed_matrix(
            distinguished, alpha, marked
        )
        frame = sp.Matrix.hstack(*p4_frames[distinguished])
        assert_frame(mixed, frame, 6)
        extension = frame * sp.Matrix((c0, c1))
        da = sp.factor((diagonal_alpha * extension)[0])
        db = sp.factor((diagonal_beta * extension)[0])
        expected_da = (-2 if distinguished == 2 else 2) * e * c0
        assert sp.factor(da - expected_da) == 0
        assert sp.factor(db + 2 * q4) == 0
        determinant = sp.factor(
            marked_extension(distinguished, extension, alpha, marked, 3)
            .extract((0, 4, 6, 7), range(4))
            .det()
        )
        expected = (-2 if distinguished == 2 else 2) * c0 * da * db
        assert sp.factor(determinant - expected) == 0
    results["prime_4"] = {"rank": 6, "kernel_dimension": 2}

    # Prime 6; prime 5 is its source swap.  Two minors cover T=0 and 2T+1=0.
    p6_e1 = sp.Matrix(
        (
            -(a + 1) * (parameter * a + parameter + 1),
            -(2 * parameter + 1) * (a + 1),
            parameter * (a - 1),
            -k * (2 * parameter + 1) * (a + 1),
            -k * (2 * parameter + 1) * (a + 1),
            -2 * parameter * (parameter * a + parameter + 1),
            0,
            (2 * parameter + 1) * (a + 1),
        )
    )
    alpha6, canonical6 = finite_basis(a, k, sp.Integer(1))
    marked6 = shifted(alpha6, canonical6, (0, parameter, k, 0))
    for distinguished, sign in ((2, 1), (3, -1)):
        e0 = sp.Matrix((0, 0, 0, sign, 1, 0, 1, 0))
        e1 = p6_e1.copy()
        if distinguished == 3:
            e1[3] = -e1[3]
        frame = sp.Matrix.hstack(e0, e1)
        mixed, da_row, db_row = mixed_matrix(distinguished, alpha6, marked6)
        assert_frame(mixed, frame, 6)
        extension = frame * sp.Matrix((c0, c1))
        assert sp.factor((da_row * extension)[0] - sign * 2 * c1 * (a**2 - 1)) == 0
        assert sp.factor((db_row * extension)[0] - 4 * c0) == 0
        marked_map = marked_extension(distinguished, extension, alpha6, marked6, 3)
        minor_a = sp.factor(marked_map.extract((0, 1, 4, 7), range(4)).det())
        minor_b = sp.factor(marked_map.extract((0, 4, 6, 7), range(4)).det())
        assert sp.factor(
            minor_a
            + 32
            * c0
            * c1**2
            * (2 * parameter + 1)
            * (a - 1)
            * (a + 1) ** 2
        ) == 0
        assert sp.factor(
            minor_b
            + 16 * parameter * c0 * c1**2 * (a - 1) ** 2 * (a + 1)
        ) == 0
    results["prime_6"] = {"rank": 6, "kernel_dimension": 2, "minor_cover": 2}

    # Prime 7; prime 8 is its source swap.
    alpha7, canonical7 = finite_basis(sp.Integer(-1), k, ell)
    marked7 = shifted(alpha7, canonical7, (0, -1 / (ell - 1), parameter, 0))
    q7 = (parameter - k) * (ell + 1) * c0 - 2 * c1
    for distinguished, sign in ((2, 1), (3, -1)):
        e0 = sp.Matrix(
            (
                ell - 1,
                0,
                ell,
                sign * (-parameter + ell * k),
                -parameter + ell * k,
                1,
                0,
                0,
            )
        )
        e1 = sp.Matrix((0, 0, 0, sign, 1, 0, 1, 0))
        frame = sp.Matrix.hstack(e0, e1)
        mixed, da_row, db_row = mixed_matrix(distinguished, alpha7, marked7)
        assert_frame(mixed, frame, 6)
        extension = frame * sp.Matrix((c0, c1))
        assert sp.factor((da_row * extension)[0] + sign * 2 * c0 * (ell - 1) ** 2) == 0
        assert sp.factor((db_row * extension)[0] + 2 * q7) == 0
        determinant = sp.factor(
            marked_extension(distinguished, extension, alpha7, marked7, 3)
            .extract((0, 4, 6, 7), range(4))
            .det()
        )
        assert sp.factor(determinant + 8 * c0**2 * (ell - 1) ** 2 * q7) == 0
    results["prime_7"] = {"rank": 6, "kernel_dimension": 2}

    # Prime 10; prime 9 is its source swap.
    alpha10, canonical10 = finite_basis(a, k, sp.Integer(1))
    marked10 = shifted(alpha10, canonical10, (0, -1 / (a + 1), parameter, 0))
    q10 = -parameter * a * c1 + parameter * c1 + a * k * c1 + 2 * c0 - k * c1
    for distinguished, sign in ((2, 1), (3, -1)):
        e0 = sp.Matrix((0, 0, 0, sign, 1, 0, 1, 0))
        e1 = sp.Matrix(
            (
                0,
                -a - 1,
                -1,
                sign * (-parameter * a - k),
                -parameter * a - k,
                0,
                0,
                a + 1,
            )
        )
        frame = sp.Matrix.hstack(e0, e1)
        mixed, da_row, db_row = mixed_matrix(distinguished, alpha10, marked10)
        assert_frame(mixed, frame, 6)
        extension = frame * sp.Matrix((c0, c1))
        assert sp.factor((da_row * extension)[0] - sign * 2 * c1 * (a + 1) ** 2) == 0
        assert sp.factor((db_row * extension)[0] - 2 * q10) == 0
        determinant = sp.factor(
            marked_extension(distinguished, extension, alpha10, marked10, 3)
            .extract((0, 4, 6, 7), range(4))
            .det()
        )
        assert sp.factor(determinant - 8 * c1**2 * (a + 1) ** 2 * q10) == 0
    results["prime_10"] = {"rank": 6, "kernel_dimension": 2}

    # Rank-drop collision (alpha,ell)=(-1,1), including kappa=0.
    alpha_c, canonical_c = finite_basis(sp.Integer(-1), k, sp.Integer(1))
    marked_c = shifted(alpha_c, canonical_c, (0, 0, k, 0))
    for distinguished, sign in ((2, 1), (3, -1)):
        e0 = sp.Matrix((0, 0, 1, 0, 0, 1, 0, 0))
        e1 = sp.Matrix((0, 0, 0, sign, 1, 0, 1, 0))
        e2 = sp.Matrix((-1, -1, 0, -sign * k, -k, 0, 0, 1))
        frame = sp.Matrix.hstack(e0, e1, e2)
        mixed, da_row, db_row = mixed_matrix(distinguished, alpha_c, marked_c)
        assert_frame(mixed, frame, 5)
        extension = frame * sp.Matrix((c0, c1, c2))
        da = sp.factor((da_row * extension)[0])
        db = sp.factor((db_row * extension)[0])
        assert sp.factor(da + sign * 4 * c2) == 0
        assert sp.factor(db - 4 * c1) == 0
        rows = (0, 1, 3, 7) if distinguished == 2 else (0, 1, 4, 7)
        determinant = sp.factor(
            marked_extension(distinguished, extension, alpha_c, marked_c, 3)
            .extract(rows, range(4))
            .det()
        )
        assert sp.factor(determinant - 4 * c2 * da * db) == 0
    results["collision"] = {"rank": 5, "kernel_dimension": 3}
    return results


def h22_branch_certificates() -> dict[str, object]:
    a, k, ell, parameter, slope, scalar = sp.symbols(
        "alpha kappa ell T lambda C"
    )
    results: dict[str, object] = {}

    def verify_line(
        label: str,
        alpha: tuple[tuple[sp.Expr, ...], ...],
        canonical_beta: tuple[tuple[sp.Expr, ...], ...],
        shifts: tuple[sp.Expr, ...],
        frame_vector: sp.Matrix,
        expected: dict[str, tuple[sp.Expr, sp.Expr, sp.Expr, sp.Expr]],
    ) -> None:
        marked = shifted(alpha, canonical_beta, shifts)
        for chart in ("finite", "infinity"):
            d01 = contraction_model(alpha, marked, "D01", chart, slope)
            d23 = contraction_model(alpha, marked, "D23", chart, slope)
            d01_coefficients = d01["coefficients"]
            d23_coefficients = d23["coefficients"]
            assert isinstance(d01_coefficients, dict) and isinstance(
                d23_coefficients, dict
            )
            expressions = tuple(d01_coefficients[word] for word in WORDS[:-1]) + tuple(
                d23_coefficients[word] for word in MIXED
            )
            extension_symbols = sp.symbols("z0:8")
            combined = sp.Matrix(
                [
                    [sp.diff(expression, value) for value in extension_symbols]
                    for expression in expressions
                ]
            )
            frame = sp.Matrix.hstack(frame_vector)
            assert_frame(combined, frame, 7)
            extension = scalar * frame_vector
            values = dict(zip(extension_symbols, extension, strict=True))
            actual = (
                sp.factor(d01["B"].subs(values)),  # type: ignore[union-attr]
                sp.factor(d23["A"].subs(values)),  # type: ignore[union-attr]
                sp.factor(d23["B"].subs(values)),  # type: ignore[union-attr]
                sp.factor(
                    contraction_one_marked(d23, 3)
                    .subs(values)
                    .extract((0, 4, 6, 7), range(4))
                    .det()
                ),
            )
            assert all(
                sp.factor(actual[index] - expected[chart][index]) == 0
                for index in range(4)
            )
        results[label] = {"rank": 7, "kernel_dimension": 1}

    # Prime 1.
    alpha1, canonical1 = finite_basis(-ell, sp.Integer(0), ell)
    verify_line(
        "prime_1",
        alpha1,
        canonical1,
        (parameter, 0, 0, 0),
        sp.Matrix((ell**2 - 1, 0, ell, 0, 0, 1, 0, 0)),
        {
            "finite": (
                2 * scalar * ((ell + 1) * slope + 1 - ell),
                -2 * scalar * (ell**2 - 1) * (slope - 1),
                -2 * scalar * parameter * (ell**2 - 1) * (slope + 1),
                8
                * parameter
                * scalar**3
                * (ell**2 - 1) ** 2
                * (slope + 1) ** 3,
            ),
            "infinity": (
                2 * scalar * (ell + 1),
                -2 * scalar * (ell**2 - 1),
                -2 * scalar * parameter * (ell**2 - 1),
                8 * parameter * scalar**3 * (ell**2 - 1) ** 2,
            ),
        },
    )

    # Prime 4.
    e = 2 * a * ell + ell**2 + 1
    alpha4, canonical4 = finite_basis(a, k, ell)
    verify_line(
        "prime_4",
        alpha4,
        canonical4,
        (0, -(a + ell) / e, k * ell, 0),
        sp.Matrix((-a * ell - 1, 0, ell, 0, 0, 1, 0, 0)),
        {
            "finite": (
                2 * scalar * ((ell + 1) * slope + 1 - ell),
                2 * scalar * (slope - 1) * e,
                -2 * scalar * k * (ell**2 - 1) * (slope + 1),
                -8
                * scalar**3
                * k
                * (ell**2 - 1)
                * (slope + 1) ** 3
                * e,
            ),
            "infinity": (
                2 * scalar * (ell + 1),
                2 * scalar * e,
                -2 * scalar * k * (ell**2 - 1),
                -8 * scalar**3 * k * (ell**2 - 1) * e,
            ),
        },
    )

    # Prime 6.
    alpha6, canonical6 = finite_basis(a, k, sp.Integer(1))
    vector6 = sp.Matrix(
        (
            -(a + 1) * (a * parameter + parameter + 1),
            -(a + 1) * (2 * parameter + 1),
            parameter * (a - 1),
            0,
            0,
            -2 * parameter * (a * parameter + parameter + 1),
            k * (a + 1) * (2 * parameter + 1),
            (a + 1) * (2 * parameter + 1),
        )
    )
    marked6 = shifted(alpha6, canonical6, (0, parameter, k, 0))
    for chart in ("finite", "infinity"):
        d01 = contraction_model(alpha6, marked6, "D01", chart, slope)
        d23 = contraction_model(alpha6, marked6, "D23", chart, slope)
        d01_coefficients = d01["coefficients"]
        d23_coefficients = d23["coefficients"]
        assert isinstance(d01_coefficients, dict) and isinstance(
            d23_coefficients, dict
        )
        combined = sp.Matrix(
            [
                [sp.diff(expression, value) for value in sp.symbols("z0:8")]
                for expression in tuple(
                    d01_coefficients[word] for word in WORDS[:-1]
                )
                + tuple(d23_coefficients[word] for word in MIXED)
            ]
        )
        assert_frame(combined, sp.Matrix.hstack(vector6), 7)
        values = dict(zip(sp.symbols("z0:8"), scalar * vector6, strict=True))
        determinant = sp.factor(
            contraction_one_marked(d23, 3)
            .subs(values)
            .extract((0, 1, 4, 7), range(4))
            .det()
        )
        weight = (slope + 1) ** 3 if chart == "finite" else 1
        assert sp.factor(
            determinant
            + 32
            * scalar**3
            * k
            * (a - 1)
            * (a + 1) ** 3
            * (2 * parameter + 1) ** 2
            * weight
        ) == 0
    results["prime_6"] = {"rank": 7, "kernel_dimension": 1}

    # Prime 7.
    alpha7, canonical7 = finite_basis(sp.Integer(-1), k, ell)
    verify_line(
        "prime_7",
        alpha7,
        canonical7,
        (0, -1 / (ell - 1), parameter, 0),
        sp.Matrix((ell - 1, 0, ell, 0, 0, 1, parameter - ell * k, 0)),
        {
            "finite": (
                2 * scalar * ((ell + 1) * slope + 1 - ell),
                2 * scalar * (ell - 1) ** 2 * (slope - 1),
                -2 * scalar * (parameter + k) * (ell - 1) * (slope + 1),
                -8
                * scalar**3
                * (parameter + k)
                * (ell - 1) ** 3
                * (slope + 1) ** 3,
            ),
            "infinity": (
                2 * scalar * (ell + 1),
                2 * scalar * (ell - 1) ** 2,
                -2 * scalar * (parameter + k) * (ell - 1),
                -8 * scalar**3 * (parameter + k) * (ell - 1) ** 3,
            ),
        },
    )

    # Prime 10.
    alpha10, canonical10 = finite_basis(a, k, sp.Integer(1))
    verify_line(
        "prime_10",
        alpha10,
        canonical10,
        (0, -1 / (a + 1), parameter, 0),
        sp.Matrix((0, -a - 1, -1, 0, 0, 0, a * parameter + k, a + 1)),
        {
            "finite": (
                2 * scalar * ((a - 1) * slope + a + 1),
                -2 * scalar * (a + 1) ** 2 * (slope - 1),
                2 * scalar * (a + 1) * (k + parameter) * (slope + 1),
                8
                * scalar**3
                * (a + 1) ** 3
                * (k + parameter)
                * (slope + 1) ** 3,
            ),
            "infinity": (
                2 * scalar * (a - 1),
                -2 * scalar * (a + 1) ** 2,
                2 * scalar * (a + 1) * (k + parameter),
                8 * scalar**3 * (a + 1) ** 3 * (k + parameter),
            ),
        },
    )
    return results


def infinity_branch_certificates() -> dict[str, object]:
    a, k, parameter, c0, c1, slope, scalar = sp.symbols(
        "alpha kappa T c0 c1 lambda C"
    )
    results: dict[str, object] = {}

    # H31 prime kappa=0.
    alpha, canonical = infinity_basis(a, sp.Integer(0))
    marked = shifted(alpha, canonical, (0, -a, parameter, 0))
    for distinguished, sign in ((2, 1), (3, -1)):
        e0 = sp.Matrix((a, 0, -1, 0, 0, 1, 0, 0))
        e1 = sp.Matrix((0, 0, 0, sign, 1, 0, 1, 0))
        frame = sp.Matrix.hstack(e0, e1)
        mixed, da_row, db_row = mixed_matrix(distinguished, alpha, marked)
        assert_frame(mixed, frame, 6)
        extension = frame * sp.Matrix((c0, c1))
        q = parameter * c0 + 2 * c1
        assert sp.factor((da_row * extension)[0] - sign * 2 * c0) == 0
        assert sp.factor((db_row * extension)[0] + 2 * q) == 0
        determinant = sp.factor(
            marked_extension(distinguished, extension, alpha, marked, 3)
            .extract((0, 1, 4, 7), range(4))
            .det()
        )
        assert sp.factor(determinant - 8 * c0**2 * q) == 0
    results["H31_kappa_zero"] = {"rank": 6, "kernel_dimension": 2}

    # H31 alpha=1; alpha=-1 is its source swap.
    alpha1, canonical1 = infinity_basis(sp.Integer(1), k)
    marked1 = shifted(alpha1, canonical1, (0, -1, parameter, 0))
    for distinguished, sign in ((2, 1), (3, -1)):
        e0 = sp.Matrix((1, 0, -1, sign * k, k, 1, 0, 0))
        e1 = sp.Matrix((0, 0, 0, sign, 1, 0, 1, 0))
        frame = sp.Matrix.hstack(e0, e1)
        mixed, da_row, db_row = mixed_matrix(distinguished, alpha1, marked1)
        assert_frame(mixed, frame, 6)
        extension = frame * sp.Matrix((c0, c1))
        q = (parameter + k) * c0 + 2 * c1
        assert sp.factor((da_row * extension)[0] - sign * 2 * c0) == 0
        assert sp.factor((db_row * extension)[0] + 2 * q) == 0
        determinant = sp.factor(
            marked_extension(distinguished, extension, alpha1, marked1, 3)
            .extract((0, 1, 4, 7), range(4))
            .det()
        )
        assert sp.factor(determinant - 8 * c0**2 * q) == 0
    results["H31_alpha_endpoint"] = {"rank": 6, "kernel_dimension": 2}

    # H22 kappa=0.
    alpha0, canonical0 = infinity_basis(a, sp.Integer(0))
    marked0 = shifted(alpha0, canonical0, (0, -a, parameter, 0))
    for chart in ("finite", "infinity"):
        d01 = contraction_model(alpha0, marked0, "D01", chart, slope)
        d23 = contraction_model(alpha0, marked0, "D23", chart, slope)
        vector = sp.Matrix((a, 0, -1, 0, 0, 1, 0, 0))
        values = dict(zip(sp.symbols("z0:8"), scalar * vector, strict=True))
        actual = (
            sp.factor(d01["B"].subs(values)),  # type: ignore[union-attr]
            sp.factor(d23["A"].subs(values)),  # type: ignore[union-attr]
            sp.factor(d23["B"].subs(values)),  # type: ignore[union-attr]
            sp.factor(
                contraction_one_marked(d23, 3)
                .subs(values)
                .extract((0, 1, 4, 7), range(4))
                .det()
            ),
        )
        if chart == "finite":
            expected = (
                2 * scalar * (slope - 1),
                -2 * scalar * (slope - 1),
                -2 * scalar * parameter * (slope + 1),
                8 * scalar**3 * parameter * (slope + 1) ** 3,
            )
        else:
            expected = (2 * scalar, -2 * scalar, -2 * scalar * parameter, 8 * scalar**3 * parameter)
        assert all(sp.factor(actual[i] - expected[i]) == 0 for i in range(4))
    results["H22_kappa_zero"] = {"kernel_dimension": 1}

    # H22 alpha=1.
    alpha_e, canonical_e = infinity_basis(sp.Integer(1), k)
    marked_e = shifted(alpha_e, canonical_e, (0, -1, parameter, 0))
    vector_e = sp.Matrix((-1, 0, 1, 0, 0, -1, k, 0))
    for chart in ("finite", "infinity"):
        d01 = contraction_model(alpha_e, marked_e, "D01", chart, slope)
        d23 = contraction_model(alpha_e, marked_e, "D23", chart, slope)
        values = dict(zip(sp.symbols("z0:8"), scalar * vector_e, strict=True))
        actual = (
            sp.factor(d01["B"].subs(values)),  # type: ignore[union-attr]
            sp.factor(d23["A"].subs(values)),  # type: ignore[union-attr]
            sp.factor(d23["B"].subs(values)),  # type: ignore[union-attr]
            sp.factor(
                contraction_one_marked(d23, 3)
                .subs(values)
                .extract((0, 1, 4, 7), range(4))
                .det()
            ),
        )
        if chart == "finite":
            expected = (
                -2 * scalar * (slope - 1),
                2 * scalar * (slope - 1),
                2 * scalar * (parameter - k) * (slope + 1),
                -8 * scalar**3 * (parameter - k) * (slope + 1) ** 3,
            )
        else:
            expected = (
                -2 * scalar,
                2 * scalar,
                2 * scalar * (parameter - k),
                -8 * scalar**3 * (parameter - k),
            )
        assert all(sp.factor(actual[i] - expected[i]) == 0 for i in range(4))
    results["H22_alpha_endpoint"] = {"kernel_dimension": 1}
    return results


def main() -> None:
    started = time.perf_counter()
    a, k, ell = sp.symbols("alpha kappa ell")
    finite_alpha, finite_beta = finite_basis(a, k, ell)
    finite_pure = {
        word: sp.factor(
            permanent4(
                tuple(finite_beta[i] if word[i] else finite_alpha[i] for i in range(4))
            )
        )
        for word in WORDS
    }
    assert finite_pure[WORDS[-1]] == 4
    assert all(value == 0 for word, value in finite_pure.items() if word != WORDS[-1])

    infinity_alpha, infinity_beta = infinity_basis(a, k)
    infinity_pure = {
        word: sp.factor(
            permanent4(
                tuple(
                    infinity_beta[i] if word[i] else infinity_alpha[i]
                    for i in range(4)
                )
            )
        )
        for word in WORDS
    }
    assert infinity_pure[WORDS[-1]] == -4
    assert all(value == 0 for word, value in infinity_pure.items() if word != WORDS[-1])

    shifts = sp.symbols("h0:4")
    for basis in ((finite_alpha, finite_beta), (infinity_alpha, infinity_beta)):
        marked = shifted(*basis, shifts)
        for distinguished in (0, 1):
            _, diagonal_alpha, _ = mixed_matrix(distinguished, basis[0], marked)
            assert diagonal_alpha == sp.zeros(1, 8)

    decomposition_results = {
        "H31_finite_d2": h31_global_decomposition(2, False),
        "H31_finite_d3": h31_global_decomposition(3, False),
        "H22_finite_weight": h22_global_decomposition("finite", False),
        "H22_infinity_weight": h22_global_decomposition("infinity", False),
        "H31_ell_infinity_d2": h31_global_decomposition(2, True),
        "H31_ell_infinity_d3": h31_global_decomposition(3, True),
        "H22_ell_infinity_finite_weight": h22_global_decomposition("finite", True),
        "H22_ell_infinity_infinity_weight": h22_global_decomposition(
            "infinity", True
        ),
    }
    assert all(result == (13, 10) for result in list(decomposition_results.values())[:4])
    assert all(result == (4, 3) for result in list(decomposition_results.values())[4:])

    h31_branches = h31_branch_certificates()
    h22_branches = h22_branch_certificates()
    infinity_branches = infinity_branch_certificates()
    elapsed = time.perf_counter() - started
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "characteristic zero",
                "theorem": THEOREM.name,
                "theorem_sha256": sha256(THEOREM),
                "pure_support": {"finite_ell": {"1111": "4"}, "ell_infinity": {"1111": "-4"}},
                "global_decompositions": decomposition_results,
                "finite_ell_minimal_primes": 10,
                "ell_infinity_minimal_primes": 3,
                "H31_branch_certificates": h31_branches,
                "H22_branch_certificates": h22_branches,
                "ell_infinity_branch_certificates": infinity_branches,
                "complete_marked_H31_boundary_empty": True,
                "complete_weighted_H22_boundary_empty": True,
                "finite_field_proof_used": False,
                "arbitrary_source_projective_boundary_closed": False,
                "global_conjecture_resolved": False,
                "elapsed_seconds": round(elapsed, 3),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
