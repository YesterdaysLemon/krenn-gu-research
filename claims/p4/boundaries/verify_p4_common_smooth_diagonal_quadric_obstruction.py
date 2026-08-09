#!/usr/bin/env python3
"""Verify the spinor obstruction on the common smooth diagonal-quadric locus."""

from __future__ import annotations

import hashlib
import itertools
import json
import shutil
import subprocess
import sys
from pathlib import Path

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)


import sympy as sp


ROOT = HERE
THEOREM = HERE / "P4_COMMON_SMOOTH_DIAGONAL_QUADRIC_OBSTRUCTION.md"
WORDS = tuple(itertools.product((0, 1), repeat=4))
PERMUTATIONS = tuple(itertools.permutations(range(4)))
PATTERNS = ("LLLL", "LLLR", "LLRR")
S = sp.symbols("s0:4")
I = sp.I

EXPECTED_SATURATED_BASES = {
    "LLLL": ("1",),
    "LLLR": (
        "s0*s1+s0*s2+s1*s2+s3^2",
        "s0*s2^2+s1*s2^2-s0*s3^2-s1*s3^2",
        "s1^2*s2^2-s1^2*s3^2-s2^2*s3^2+s3^4",
        "s0*s3^4+s1*s3^4+s2*s3^4-s0-s1-s2",
        (
            "s1^2*s3^4+s1*s2*s3^4+s2^2*s3^4-s3^6"
            "-s1^2-s1*s2-s2^2+s3^2"
        ),
        "s2^3*s3^4-s2*s3^6-s2^3+s2*s3^2",
    ),
    "LLRR": (
        "s0*s2+s1*s2+s0*s3+s1*s3",
        "s0*s1+s2^2+2*s2*s3+s3^2",
        "s0^2+s1^2-2*s2^2-3*s2*s3-2*s3^2",
        "s2^2*s3+s2*s3^2",
        (
            "s1^2*s2-s2^3+s1^2*s3-3*s2^2*s3"
            "-3*s2*s3^2-s3^3"
        ),
        "s1^3-s1*s2^2-s1*s2*s3-s1*s3^2",
    ),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def spinor_line(kind: str, parameter: sp.Expr) -> sp.Matrix:
    if kind == "L":
        return sp.Matrix(
            (
                (1, -I, -parameter, -I * parameter),
                (parameter, I * parameter, 1, -I),
            )
        )
    if kind == "R":
        return sp.Matrix(
            (
                (1, -I, parameter, -I * parameter),
                (parameter, I * parameter, -1, -I),
            )
        )
    raise ValueError(kind)


def annihilator_plane(kind: str, parameter: sp.Expr) -> sp.Matrix:
    if kind == "L":
        first = (
            parameter**2 - 1,
            I * (parameter**2 + 1),
            2 * parameter,
            0,
        )
    elif kind == "R":
        first = (
            1 - parameter**2,
            -I * (parameter**2 + 1),
            2 * parameter,
            0,
        )
    else:
        raise ValueError(kind)
    second = (
        -(parameter**2 + 1),
        I * (1 - parameter**2),
        0,
        2 * I * parameter,
    )
    return sp.Matrix((first, second))


def permanent(rows: tuple[sp.Matrix, ...]) -> sp.Expr:
    return sp.expand(
        sum(
            sp.prod(rows[row][permutation[row]] for row in range(4))
            for permutation in PERMUTATIONS
        )
    )


def tensor(pattern: str) -> dict[tuple[int, ...], sp.Expr]:
    planes = tuple(
        annihilator_plane(kind, parameter)
        for kind, parameter in zip(pattern, S, strict=True)
    )
    result = {
        word: sp.expand(
            permanent(
                tuple(planes[mode].row(word[mode]) for mode in range(4))
            )
        )
        for word in WORDS
    }
    assert all(not value.has(I) for value in result.values())
    return result


def canonical_polynomial(expression: sp.Expr) -> sp.Expr:
    polynomial = sp.Poly(sp.expand(expression), *S, domain=sp.QQ)
    _, primitive = polynomial.primitive()
    if primitive.LC() < 0:
        primitive = -primitive
    return sp.expand(primitive.as_expr())


def flattening_minors(
    coefficients: dict[tuple[int, ...], sp.Expr],
) -> tuple[sp.Expr, ...]:
    result: list[sp.Expr] = []
    seen: set[str] = set()
    for mode in range(4):
        other_modes = tuple(index for index in range(4) if index != mode)
        columns = tuple(itertools.product((0, 1), repeat=3))

        def word(bit: int, column: tuple[int, ...]) -> tuple[int, ...]:
            entries = [0] * 4
            entries[mode] = bit
            for other_mode, value in zip(
                other_modes, column, strict=True
            ):
                entries[other_mode] = value
            return tuple(entries)

        for left, right in itertools.combinations(columns, 2):
            minor = sp.expand(
                coefficients[word(0, left)] * coefficients[word(1, right)]
                - coefficients[word(0, right)]
                * coefficients[word(1, left)]
            )
            if minor == 0:
                continue
            minor = canonical_polynomial(minor)
            key = str(minor)
            if key not in seen:
                seen.add(key)
                result.append(minor)
    return tuple(result)


def distinct_nonzero_entries(
    coefficients: dict[tuple[int, ...], sp.Expr],
) -> tuple[sp.Expr, ...]:
    result: list[sp.Expr] = []
    seen: set[str] = set()
    for value in coefficients.values():
        if value == 0:
            continue
        value = canonical_polynomial(value)
        key = str(value)
        if key not in seen:
            seen.add(key)
            result.append(value)
    return tuple(result)


def diagonal_quadric_vector(line: sp.Matrix) -> tuple[sp.Expr, ...]:
    pluecker = {
        (left, right): sp.expand(
            line[0, left] * line[1, right]
            - line[0, right] * line[1, left]
        )
        for left, right in itertools.combinations(range(4), 2)
    }
    result = []
    for omitted in range(4):
        remaining = tuple(index for index in range(4) if index != omitted)
        result.append(
            sp.factor(
                (-1) ** omitted
                * sp.prod(
                    pluecker[pair]
                    for pair in itertools.combinations(remaining, 2)
                )
            )
        )
    return tuple(result)


def singular_expression(expression: sp.Expr) -> str:
    return str(sp.expand(expression)).replace("**", "^")


def singular_command() -> list[str]:
    native = shutil.which("Singular")
    if native:
        return [native, "-q"]
    wsl = shutil.which("wsl.exe")
    if wsl:
        return [wsl, "--exec", "/usr/bin/Singular", "-q"]
    raise RuntimeError("Singular is required for the exact saturation replay")


def saturation_source(
    pattern: str,
    minors: tuple[sp.Expr, ...],
    entries: tuple[sp.Expr, ...],
) -> str:
    expected = EXPECTED_SATURATED_BASES[pattern]
    base_product = "*".join(
        f"s{index}*(s{index}^4-1)" for index in range(4)
    )
    lines = [
        'LIB "elim.lib";',
        "ring r=0,(s0,s1,s2,s3),dp;",
        "option(redSB);",
        "ideal Pure=0;",
    ]
    lines.extend(
        f"Pure=Pure,{singular_expression(minor)};" for minor in minors
    )
    lines.append("ideal Tensor=0;")
    lines.extend(
        f"Tensor=Tensor,{singular_expression(entry)};" for entry in entries
    )
    lines.extend(
        (
            "ideal Sat=sat(Pure,Tensor);",
            "Sat=std(Sat);",
            f"ideal Expected={','.join(expected)};",
            "Expected=std(Expected);",
            "ideal left_remainder=simplify(reduce(Sat,Expected),2);",
            "ideal right_remainder=simplify(reduce(Expected,Sat),2);",
            "int basis_equal=0;",
            (
                "if ((size(left_remainder)==0)"
                " && (size(right_remainder)==0)) { basis_equal=1; }"
            ),
            f"ideal Block={base_product};",
            "ideal Open=sat(Sat,Block);",
            "int open_unit=0;",
            "if (reduce(1,Open)==0) { open_unit=1; }",
            (
                f'"CODEX_RESULT:{pattern}:"'
                '+string(dim(Sat))+":"+string(size(Sat))+":"'
                '+string(basis_equal)+":"+string(open_unit);'
            ),
        )
    )
    return "\n".join(lines) + "\n"


def replay_saturation(
    pattern: str,
    minors: tuple[sp.Expr, ...],
    entries: tuple[sp.Expr, ...],
) -> dict[str, int | bool]:
    completed = subprocess.run(
        singular_command(),
        input=saturation_source(pattern, minors, entries),
        text=True,
        capture_output=True,
        timeout=300,
        check=False,
    )
    if completed.returncode != 0 or completed.stderr.strip():
        raise AssertionError(
            f"Singular failed for {pattern}: "
            f"rc={completed.returncode}, stderr={completed.stderr!r}"
        )
    if "?" in completed.stdout:
        raise AssertionError(
            f"Singular reported an error for {pattern}:\n{completed.stdout}"
        )
    prefix = f"CODEX_RESULT:{pattern}:"
    lines = [
        line.strip()
        for line in completed.stdout.splitlines()
        if line.strip().startswith(prefix)
    ]
    assert len(lines) == 1, completed.stdout
    dimension, basis_size, basis_equal, open_unit = (
        int(value) for value in lines[0][len(prefix) :].split(":")
    )
    assert dimension == (-1 if pattern == "LLLL" else 1)
    assert basis_size == len(EXPECTED_SATURATED_BASES[pattern])
    assert basis_equal == 1
    assert open_unit == 1
    return {
        "saturated_dimension": dimension,
        "saturated_basis_size": basis_size,
        "displayed_basis_verified": True,
        "nonblock_open_unit_ideal": True,
    }


def main() -> None:
    parameter = sp.symbols("s")
    common_factor = 2 * parameter * (parameter**4 - 1)
    cubic_data = {}
    for kind in ("L", "R"):
        line = spinor_line(kind, parameter)
        plane = annihilator_plane(kind, parameter)
        assert sp.simplify(plane * line.T) == sp.zeros(2, 2)
        assert line.rank() == 2
        assert plane.rank() == 2
        for left in range(2):
            for right in range(left, 2):
                quadratic_pairing = sp.expand(
                    sum(
                        line[left, coordinate] * line[right, coordinate]
                        for coordinate in range(4)
                    )
                )
                assert quadratic_pairing == 0
        cubic = diagonal_quadric_vector(line)
        assert all(
            sp.factor(entry - common_factor) == 0
            for entry in cubic
        )
        cubic_data[kind] = [str(entry) for entry in cubic]

    pattern_data = {}
    expected_counts = {
        "LLLL": (14, 7, 52),
        "LLLR": (14, 13, 88),
        "LLRR": (14, 13, 88),
    }
    for pattern in PATTERNS:
        coefficients = tensor(pattern)
        minors = flattening_minors(coefficients)
        entries = distinct_nonzero_entries(coefficients)
        counts = (
            sum(value != 0 for value in coefficients.values()),
            len(entries),
            len(minors),
        )
        assert counts == expected_counts[pattern]
        pattern_data[pattern] = {
            "nonzero_tensor_positions": counts[0],
            "distinct_tensor_entries": counts[1],
            "distinct_flattening_minors": counts[2],
            **replay_saturation(pattern, minors, entries),
        }

    output = {
        "verified": True,
        "field": "C",
        "method": (
            "spinor rulings on a smooth quadric, cubic diagonal-quadric "
            "map, Segre-minor ideals, and characteristic-zero saturation"
        ),
        "spinor_line_plane_duality_verified": True,
        "common_smooth_quadric_verified": True,
        "cubic_diagonal_quadric_vectors": cubic_data,
        "finite_block_parameter_equation": "s*(s^4-1)=0",
        "infinite_parameter_is_block_line": True,
        "ruling_patterns_exhaustive_up_to_symmetry": list(PATTERNS),
        "patterns": pattern_data,
        "all_unique_common_smooth_quadric_pure_locus_empty": True,
        "all_pure_components_classified": False,
        "H31_excluded": False,
        "H22_excluded": False,
        "global_conjecture_resolved": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        ROOT
        / "tmp"
        / "p4_common_smooth_diagonal_quadric_obstruction_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
