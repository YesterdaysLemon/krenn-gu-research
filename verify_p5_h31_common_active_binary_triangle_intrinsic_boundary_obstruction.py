#!/usr/bin/env python3
"""Verify component twenty's generic p-q+1=0 marked-H31 obstruction."""

from __future__ import annotations

import hashlib
import itertools
import json
import shutil
import subprocess
from pathlib import Path

import sympy as sp

from verify_p5_h31_marked_basis_open_branch import mixed_matrix

ROOT = Path(__file__).resolve().parent
THEOREM = (
    ROOT / "P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_INTRINSIC_BOUNDARY_OBSTRUCTION.md"
)
COMPONENT = ROOT / "P4_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT.md"
WORDS = tuple(itertools.product((0, 1), repeat=4))
PERMUTATIONS = tuple(itertools.permutations(range(4)))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent(rows: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(4))
            for permutation in PERMUTATIONS
        )
    )


def shifted_basis(
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
    shifts: tuple[sp.Expr, ...],
) -> tuple[tuple[sp.Expr, ...], ...]:
    return tuple(
        tuple(
            sp.factor(beta[mode][coordinate] + shifts[mode] * alpha[mode][coordinate])
            for coordinate in range(4)
        )
        for mode in range(4)
    )


def singular_command() -> tuple[str, ...]:
    native = shutil.which("Singular")
    if native:
        return (native, "-q")
    if shutil.which("wsl.exe"):
        return ("wsl.exe", "--exec", "/usr/bin/Singular", "-q")
    raise RuntimeError("Singular is required for the exact boundary replay")


def singular_polynomial(expression: sp.Expr) -> str:
    numerator = sp.together(expression).as_numer_denom()[0]
    return str(sp.expand(numerator)).replace("**", "^")


def projection_certificate(
    distinguished: int,
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
) -> dict[str, object]:
    extensions = sp.symbols("x0:4") + sp.symbols("y0:4")
    inverse = sp.Symbol("w")
    shifts = sp.symbols("h0:4")
    marked_beta = shifted_basis(alpha, beta, shifts)
    mixed, diagonal_alpha, diagonal_beta = mixed_matrix(
        distinguished, alpha, marked_beta
    )
    extension = sp.Matrix(extensions)
    equations = (
        *tuple(mixed * extension),
        (diagonal_alpha * extension)[0] - 1,
        inverse * (diagonal_beta * extension)[0] - 1,
    )
    eliminated = extensions + (inverse,)
    variables = eliminated + shifts
    program = "\n".join(
        (
            "ring R=(0,p),(" + ",".join(map(str, variables)) + "),(dp(9),dp(4));",
            "option(redSB);",
            "ideal I=" + ",".join(map(singular_polynomial, equations)) + ";",
            "I=slimgb(I);",
            "ideal J=eliminate(I," + "*".join(map(str, eliminated)) + ");",
            "J=std(J);",
            "ideal E=1;",
            "E=std(E);",
            "ideal JE=reduce(J,E);",
            "ideal EJ=reduce(E,J);",
            "JE=simplify(JE,2);",
            "EJ=simplify(EJ,2);",
            "int same=((size(JE)==0)&&(size(EJ)==0));",
            '"CODEX_RESULT:"+string(same)+":"+string(size(J));',
            "quit;",
        )
    )
    completed = subprocess.run(
        singular_command(),
        input=program,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=300,
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
    markers = [
        line.strip()
        for line in completed.stdout.splitlines()
        if line.startswith("CODEX_RESULT:")
    ]
    assert len(markers) == 1, completed.stdout
    _, same, size = markers[0].split(":")
    assert same == "1", completed.stdout
    return {
        "distinguished_coordinate": distinguished,
        "projected_ideal": ["1"],
        "bidirectional_ideal_equality": True,
        "standard_basis_size": int(size),
    }


def main() -> None:
    p = sp.Symbol("p")
    one, zero = sp.Integer(1), sp.Integer(0)
    e = (one, zero, zero, zero)
    alpha = ((zero, -one, one, zero), e, e, (one, one, one, zero))
    beta = (
        (p * (p + 1) / (2 * p + 1), -2 * p - 1, zero, one),
        (zero, p + 1, p, one),
        (zero, p, p + 1, one),
        e,
    )
    assert all(sp.Matrix((alpha[mode], beta[mode])).rank() == 2 for mode in range(4))
    tensor = {
        word: sp.factor(
            permanent(
                tuple(beta[mode] if word[mode] else alpha[mode] for mode in range(4))
            )
        )
        for word in WORDS
    }
    assert sp.factor(tensor[(1, 1, 1, 1)] + 2 * p * (p + 1)) == 0
    assert all(value == 0 for word, value in tensor.items() if word != (1, 1, 1, 1))
    projections = [projection_certificate(d, alpha, beta) for d in range(4)]
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "C(p)",
                "base_divisor": "q=p+1",
                "pure_support": {"1111": "-2*p*(p+1)"},
                "replacement_intrinsic_basis_used": True,
                "projection_certificates": projections,
                "binary_neighbour_fibre_empty": True,
                "marked_H31_fibre_empty": True,
                "divisor_intersections_closed": False,
                "projective_boundaries_closed": False,
                "weighted_H22_closed": False,
                "finite_field_inference_used": False,
                "theorem": THEOREM.name,
                "theorem_sha256": sha256(THEOREM),
                "component": COMPONENT.name,
                "component_sha256": sha256(COMPONENT),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
