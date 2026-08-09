#!/usr/bin/env python3
"""Independent finite-field audit of the common-smooth-quadric obstruction."""

from __future__ import annotations

import hashlib
import itertools
import json
import sys
from pathlib import Path

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)

ROOT = HERE
THEOREM = HERE / "P4_COMMON_SMOOTH_DIAGONAL_QUADRIC_OBSTRUCTION.md"
PRIMARY = HERE / "verify_p4_common_smooth_diagonal_quadric_obstruction.py"
MODULI = (13, 17)
PATTERNS = ("LLLL", "LLLR", "LLRR")
WORDS = tuple(itertools.product((0, 1), repeat=4))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def square_root_minus_one(modulus: int) -> int:
    roots = [
        value
        for value in range(modulus)
        if value * value % modulus == modulus - 1
    ]
    assert len(roots) == 2
    return min(roots)


def spinor_line(
    kind: str, parameter: int, imaginary: int, modulus: int
) -> tuple[tuple[int, ...], ...]:
    s = parameter % modulus
    if kind == "L":
        rows = (
            (1, -imaginary, -s, -imaginary * s),
            (s, imaginary * s, 1, -imaginary),
        )
    else:
        rows = (
            (1, -imaginary, s, -imaginary * s),
            (s, imaginary * s, -1, -imaginary),
        )
    return tuple(
        tuple(entry % modulus for entry in row) for row in rows
    )


def annihilator_plane(
    kind: str, parameter: int, imaginary: int, modulus: int
) -> tuple[tuple[int, ...], ...]:
    s = parameter % modulus
    if kind == "L":
        first = (s * s - 1, imaginary * (s * s + 1), 2 * s, 0)
    else:
        first = (1 - s * s, -imaginary * (s * s + 1), 2 * s, 0)
    second = (
        -(s * s + 1),
        imaginary * (1 - s * s),
        0,
        2 * imaginary * s,
    )
    return tuple(
        tuple(entry % modulus for entry in row)
        for row in (first, second)
    )


def dot(
    left: tuple[int, ...], right: tuple[int, ...], modulus: int
) -> int:
    return sum(a * b for a, b in zip(left, right, strict=True)) % modulus


def permanent_dp(
    rows: tuple[tuple[int, ...], ...], modulus: int
) -> int:
    values = [0] * 16
    values[0] = 1
    for row in rows:
        updated = [0] * 16
        for mask, value in enumerate(values):
            if value == 0:
                continue
            for column in range(4):
                bit = 1 << column
                if mask & bit == 0:
                    updated[mask | bit] = (
                        updated[mask | bit] + value * row[column]
                    ) % modulus
        values = updated
    return values[15]


def tensor(
    planes: tuple[tuple[tuple[int, ...], ...], ...], modulus: int
) -> dict[tuple[int, ...], int]:
    return {
        word: permanent_dp(
            tuple(planes[mode][word[mode]] for mode in range(4)),
            modulus,
        )
        for word in WORDS
    }


def is_nonzero_decomposable(
    coefficients: dict[tuple[int, ...], int], modulus: int
) -> bool:
    if not any(coefficients.values()):
        return False
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
            minor = (
                coefficients[word(0, left)] * coefficients[word(1, right)]
                - coefficients[word(0, right)]
                * coefficients[word(1, left)]
            ) % modulus
            if minor != 0:
                return False
    return True


def diagonal_quadric_vector(
    line: tuple[tuple[int, ...], ...], modulus: int
) -> tuple[int, ...]:
    pluecker = {
        (left, right): (
            line[0][left] * line[1][right]
            - line[0][right] * line[1][left]
        )
        % modulus
        for left, right in itertools.combinations(range(4), 2)
    }
    result = []
    for omitted in range(4):
        remaining = tuple(index for index in range(4) if index != omitted)
        value = (-1) ** omitted
        for pair in itertools.combinations(remaining, 2):
            value *= pluecker[pair]
        result.append(value % modulus)
    return tuple(result)


def audit_modulus(modulus: int) -> dict[str, object]:
    imaginary = square_root_minus_one(modulus)
    for kind in ("L", "R"):
        for parameter in range(modulus):
            line = spinor_line(kind, parameter, imaginary, modulus)
            plane = annihilator_plane(
                kind, parameter, imaginary, modulus
            )
            assert all(
                dot(plane_row, line_row, modulus) == 0
                for plane_row in plane
                for line_row in line
            )
            assert all(
                dot(line[left], line[right], modulus) == 0
                for left in range(2)
                for right in range(left, 2)
            )
            cubic = diagonal_quadric_vector(line, modulus)
            block = parameter == 0 or pow(parameter, 4, modulus) == 1
            if block:
                assert cubic == (0, 0, 0, 0)
            else:
                assert cubic[0] != 0
                assert cubic == (cubic[0],) * 4

        infinite_line = (
            ((0, 0, -1, -imaginary), (1, imaginary, 0, 0))
            if kind == "L"
            else ((0, 0, 1, -imaginary), (1, imaginary, 0, 0))
        )
        assert diagonal_quadric_vector(
            infinite_line, modulus
        ) == (0, 0, 0, 0)

    allowed = tuple(
        value
        for value in range(modulus)
        if value != 0 and pow(value, 4, modulus) != 1
    )
    plane_cache = {
        (kind, parameter): annihilator_plane(
            kind, parameter, imaginary, modulus
        )
        for kind in ("L", "R")
        for parameter in allowed
    }
    pattern_results = {}
    for pattern in PATTERNS:
        tested = 0
        pure = 0
        for parameters in itertools.product(allowed, repeat=4):
            planes = tuple(
                plane_cache[kind, parameter]
                for kind, parameter in zip(
                    pattern, parameters, strict=True
                )
            )
            tested += 1
            pure += int(
                is_nonzero_decomposable(tensor(planes, modulus), modulus)
            )
        assert tested == len(allowed) ** 4
        assert pure == 0
        pattern_results[pattern] = {
            "nonblock_parameter_tuples": tested,
            "nonzero_pure_tuples": pure,
        }

    boundary_samples = {
        "LLLR": (-2, 0, 2, 2),
        "LLRR": (1, 0, -1, 1),
    }
    for pattern, parameters in boundary_samples.items():
        planes = tuple(
            annihilator_plane(
                kind, parameter % modulus, imaginary, modulus
            )
            for kind, parameter in zip(
                pattern, parameters, strict=True
            )
        )
        assert is_nonzero_decomposable(tensor(planes, modulus), modulus)
        assert any(
            parameter % modulus == 0
            or pow(parameter % modulus, 4, modulus) == 1
            for parameter in parameters
        )

    return {
        "modulus": modulus,
        "sqrt_minus_one": imaginary,
        "allowed_nonblock_parameters": len(allowed),
        "line_plane_dot_checks": 8 * modulus,
        "quadric_pairing_checks": 6 * modulus,
        "cubic_map_checks": 2 * (modulus + 1),
        "patterns": pattern_results,
        "boundary_samples_nonzero_and_pure": True,
    }


def main() -> None:
    audits = [audit_modulus(modulus) for modulus in MODULI]
    output = {
        "audited": True,
        "independent_of_primary_imports": True,
        "method": (
            "dynamic-programming permanent, direct modular spinor duality, "
            "cubic-map replay, and exhaustive finite-field nonblock atlases"
        ),
        "moduli": list(MODULI),
        "audits": audits,
        "all_nonblock_spinor_tuples_excluded_modularly": True,
        "boundary_strata_replayed": True,
        "finite_field_results_are_corroboration_only": True,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "primary": PRIMARY.name,
        "primary_sha256": sha256(PRIMARY),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        ROOT
        / "tmp"
        / "p4_common_smooth_diagonal_quadric_obstruction_audit.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
