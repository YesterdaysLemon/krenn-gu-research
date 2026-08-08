#!/usr/bin/env python3
"""Verify the generic marked-H31 obstruction on the sixth component."""

from __future__ import annotations

import hashlib
import itertools
import json
import subprocess
from pathlib import Path

import sympy as sp

import sys

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap, expose_claim_package  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
ROOT = REPO_ROOT

from p5_high_coordinate_tree_chart_cegar import singular_command_with_timeout
from verify_p5_h31_marked_basis_open_branch import (
    marked_extension,
    mixed_matrix,
    one_marked_map,
)


ROOT = REPO_ROOT
THEOREM = (
    HERE / "P5_H31_MIXED_ORIENTATION_COMPONENT_GENERIC_OBSTRUCTION.md"
)
COMPONENT = (
    ROOT / "claims" / "p4" / "components" / "mixed-orientation"
    / "P4_MIXED_ORIENTATION_PURE_COMPONENT.md")
COMPONENT_PRIMARY = (
    ROOT / "claims" / "p4" / "components" / "mixed-orientation"
    / "verify_p4_mixed_orientation_pure_component.py")
WORDS = tuple(itertools.product((0, 1), repeat=4))
PERMUTATIONS = tuple(itertools.permutations(range(4)))

EXPECTED_PROJECTIONS = {
    0: ("1",),
    1: ("1",),
    2: (
        "t3",
        "(d*p^2+d*p*q)*t1+(-d-p-q)*t2+(p^2+p*q)",
        "t0-1",
        (
            "(d^2+d*p+2*d*q+p*q+q^2)*t2^2"
            "+(-d*p^2-2*d*p*q-2*p^2*q-2*p*q^2)*t2"
            "+(p^3*q+p^2*q^2)"
        ),
    ),
    3: (
        "(d+p+q)*t2+(d*p)*t3+(-d*p-p^2-p*q)",
        "t1",
        "t0-1",
        "(d)*t3^2+(-2*d-p-q)*t3+(d+p+q)",
    ),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent(rows) -> sp.Expr:
    return sp.factor(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(4))
            for permutation in PERMUTATIONS
        )
    )


def canonical_basis(
    d: sp.Expr, p: sp.Expr, q: sp.Expr
) -> tuple[tuple[tuple[sp.Expr, ...], ...], ...]:
    N = q * (d + p + q)
    planes = (
        sp.Matrix(((-d * p, d + q, N, 0), (d * p, -d - q, 0, N))),
        sp.Matrix(((0, 0, 1, 1), (-d, 1, -p - q, d))),
        sp.Matrix(((p, 1, 0, q), (-1, 0, 1, 0))),
        sp.Matrix(((1, 0, 1, 0), (0, 0, -1, 1))),
    )
    alpha = tuple(tuple(plane.row(1)) for plane in planes)
    beta = tuple(tuple(plane.row(0)) for plane in planes)
    return alpha, beta


def shifted_basis(alpha, beta, shifts):
    return tuple(
        tuple(
            sp.factor(
                beta[mode][coordinate]
                + shifts[mode] * alpha[mode][coordinate]
            )
            for coordinate in range(4)
        )
        for mode in range(4)
    )


def singular(expression: sp.Expr) -> str:
    return str(sp.cancel(expression)).replace("**", "^")


def run_projection(distinguished: int, alpha, beta) -> tuple[str, ...]:
    extensions = sp.symbols("x0:4") + sp.symbols("y0:4")
    shifts = sp.symbols("t0:4")
    inverse = sp.Symbol("ub")
    marked_beta = shifted_basis(alpha, beta, shifts)
    mixed, diagonal_a, diagonal_b = mixed_matrix(
        distinguished, alpha, marked_beta
    )
    extension = sp.Matrix(extensions)
    equations = list(mixed * extension)
    equations.extend(
        (
            (diagonal_a * extension)[0] - 1,
            inverse * (diagonal_b * extension)[0] - 1,
        )
    )
    eliminated = extensions + (inverse,)
    variables = eliminated + shifts
    program = "\n".join(
        (
            "ring r=(0,d,p,q),("
            + ",".join(map(str, variables))
            + "),(dp(9),dp(4));",
            "option(redSB);",
            "ideal incidence="
            + ",".join(map(singular, equations))
            + ";",
            "ideal basis=std(incidence);",
            "ideal marking=eliminate(basis,"
            + "*".join(map(str, eliminated))
            + ");",
            "marking=std(marking);",
            '"MARKING";',
            "marking;",
            "quit;",
        )
    )
    completed = subprocess.run(
        singular_command_with_timeout(180),
        input=program,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=185,
        check=False,
    )
    if completed.returncode != 0 or completed.stderr.strip():
        raise AssertionError(
            (
                "Singular projection failure",
                distinguished,
                completed.returncode,
                completed.stdout,
                completed.stderr,
            )
        )
    return tuple(
        line.split("=", 1)[1].replace(" ", "")
        for line in completed.stdout.replace("\r\n", "\n").splitlines()
        if line.startswith("marking[")
    )


def extension_identity(
    distinguished: int,
    alpha,
    beta,
    mode: int,
    rows: tuple[int, ...],
    expected_ratio: sp.Expr,
) -> dict[str, object]:
    extensions = sp.symbols("x0:4") + sp.symbols("y0:4")
    extension = sp.Matrix(extensions)
    mixed, diagonal_a, diagonal_b = mixed_matrix(
        distinguished, alpha, beta
    )
    first = (diagonal_a * extension)[0]
    second = (diagonal_b * extension)[0]
    marked = marked_extension(
        distinguished, extension, alpha, beta, mode
    )
    determinant = sp.expand(marked[list(rows), :].det())
    linear_equations = list(mixed * extension)
    program = "\n".join(
        (
            "ring r=(0,d,p,q),("
            + ",".join(map(str, extensions))
            + "),dp;",
            "ideal L="
            + ",".join(map(singular, linear_equations))
            + ";",
            "ideal J=std(L);",
            f"poly rd=reduce({singular(determinant)},J);",
            f"poly rb=reduce({singular(first * second**2)},J);",
            "number ratio=leadcoef(rd)/leadcoef(rb);",
            "poly check=reduce(rd-ratio*rb,J);",
            "int good=0;",
            (
                f"if ((check==0) && (ratio-({singular(expected_ratio)})==0))"
                " { good=1; }"
            ),
            (
                '"CODEX_RESULT:"+string(dim(J))+":"'
                '+string(good)+":"+string(ratio);'
            ),
        )
    )
    completed = subprocess.run(
        singular_command_with_timeout(120),
        input=program,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=125,
        check=False,
    )
    if completed.returncode != 0 or completed.stderr.strip():
        raise AssertionError(
            (
                "Singular extension identity failure",
                distinguished,
                completed.returncode,
                completed.stdout,
                completed.stderr,
            )
        )
    lines = [
        line.strip()
        for line in completed.stdout.splitlines()
        if line.startswith("CODEX_RESULT:")
    ]
    assert len(lines) == 1, completed.stdout
    fields = lines[0].split(":", 3)
    assert fields[1:3] == ["2", "1"], completed.stdout
    return {
        "mixed_kernel_dimension": 2,
        "marked_mode": mode,
        "marked_rows": list(rows),
        "factor_identity_ratio": fields[3],
    }


def main() -> None:
    d, p, q = sp.symbols("d p q", nonzero=True)
    alpha, beta = canonical_basis(d, p, q)
    tensor = {
        word: permanent(
            tuple(
                beta[mode] if word[mode] else alpha[mode]
                for mode in range(4)
            )
        )
        for word in WORDS
    }
    assert tensor[(1, 1, 1, 1)] == 2 * q * (d + p + q)
    assert all(
        value == 0
        for word, value in tensor.items()
        if word != (1, 1, 1, 1)
    )

    t = sp.symbols("t0:4")
    shifted = shifted_basis(alpha, beta, t)
    shifted_tensor = {
        word: permanent(
            tuple(
                shifted[mode] if word[mode] else alpha[mode]
                for mode in range(4)
            )
        )
        for word in WORDS
    }
    assert shifted_tensor == tensor

    projections = {
        distinguished: run_projection(distinguished, alpha, beta)
        for distinguished in range(4)
    }
    assert projections == EXPECTED_PROJECTIONS

    quadratic_two = sp.factor(
        (d + q) * (d + p + q) * t[2] ** 2
        - p
        * (d * p + 2 * d * q + 2 * p * q + 2 * q**2)
        * t[2]
        + p**2 * q * (p + q)
    )
    assert sp.factor(
        quadratic_two
        - ((d + q) * t[2] - p * q)
        * ((d + p + q) * t[2] - p * (p + q))
    ) == 0
    quadratic_three = sp.factor(
        d * t[3] ** 2
        - (2 * d + p + q) * t[3]
        + d
        + p
        + q
    )
    assert sp.factor(
        quadratic_three
        - (t[3] - 1) * (d * t[3] - (d + p + q))
    ) == 0

    markings = {
        "2A": (
            2,
            (
                1,
                -p / ((d + q) * (p + q)),
                p * q / (d + q),
                0,
            ),
            1,
            (0, 2, 3, 7),
            -p**2 * q / (d + p + q),
            (0, d + q),
        ),
        "2B": (
            2,
            (1, 0, p * (p + q) / (d + p + q), 0),
            2,
            (0, 1, 3, 7),
            d * (d + q) / q,
            (0, d * (d + p + q)),
        ),
        "3A": (
            3,
            (1, 0, p * (p + q) / (d + p + q), 1),
            3,
            (0, 2, 6, 7),
            -(d + q),
            (2, d + q),
        ),
        "3B": (
            3,
            (1, 0, 0, (d + p + q) / d),
            3,
            (0, 2, 6, 7),
            -(d + q),
            (2, d + q),
        ),
    }
    certificates = {}
    for name, (
        distinguished,
        marking,
        mode,
        rows,
        ratio,
        transverse,
    ) in markings.items():
        marked_beta = shifted_basis(alpha, beta, marking)
        certificate = extension_identity(
            distinguished,
            alpha,
            marked_beta,
            mode,
            rows,
            ratio,
        )
        pure_marked = one_marked_map(mode, alpha, marked_beta)
        transverse_row, expected_entry = transverse
        assert sp.factor(
            pure_marked[transverse_row, distinguished] - expected_entry
        ) == 0
        certificate["pure_transverse_row"] = transverse_row
        certificate["pure_transverse_entry"] = str(expected_entry)
        certificates[name] = certificate

    output = {
        "verified": True,
        "field": "C(d,p,q)",
        "method": (
            "function-field marked projection and characteristic-zero "
            "all-extension determinant identities"
        ),
        "pure_coefficient": str(2 * q * (d + p + q)),
        "projections": {
            str(key): list(value) for key, value in projections.items()
        },
        "surviving_marking_sheets": 4,
        "certificates": certificates,
        "generic_marked_fibre_excluded": True,
        "complete_boundary_marked_fibre_excluded": False,
        "all_pure_components_classified": False,
        "H31_excluded": False,
        "H22_excluded": False,
        "global_conjecture_resolved": False,
        "dependencies": {
            COMPONENT.name: sha256(COMPONENT),
            COMPONENT_PRIMARY.name: sha256(COMPONENT_PRIMARY),
        },
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        ROOT
        / "tmp"
        / "p5_h31_mixed_orientation_component_generic_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
