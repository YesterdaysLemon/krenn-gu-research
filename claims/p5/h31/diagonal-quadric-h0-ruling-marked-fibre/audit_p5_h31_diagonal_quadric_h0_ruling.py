#!/usr/bin/env python3
"""Independent finite-field audit of the H=0 diagonal ruling."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sys

for _parent in Path(__file__).resolve().parents:
    if (_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        sys.path.insert(0, str(_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap, expose_claim_package  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
expose_claim_package(REPO_ROOT, "claims/p5/h31/diagonal-quadric-component-point")

import audit_p5_h31_diagonal_quadric_component_point as BASE


ROOT = Path(__file__).resolve().parent
THEOREM = (
    ROOT / "P5_H31_DIAGONAL_QUADRIC_H0_RULING_MARKED_FIBRE_OBSTRUCTION.md"
)
PRIMARY = ROOT / "verify_p5_h31_diagonal_quadric_h0_ruling.py"
MODULI = (5, 7)
WORDS4 = tuple(itertools.product((0, 1), repeat=4))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def alpha_rows(
    parameter: int,
    modulus: int,
) -> tuple[tuple[int, ...], ...]:
    return (
        (
            2 * parameter,
            -parameter - 1,
            parameter - 1,
            0,
        ),
        (1, 0, 0, -1),
        (0, 1, -1, 0),
        (parameter, -1, -1, parameter),
    )


def canonical_beta(
    parameter: int,
    modulus: int,
) -> tuple[tuple[int, ...], ...]:
    return (
        (1, -1, 1, 1),
        (parameter, parameter + 1, 1 - parameter, parameter),
        (parameter, 1, 1, -parameter),
        (0, 1, 1, 0),
    )


def shifted_beta(
    parameter: int,
    shifts: tuple[int, ...],
    modulus: int,
) -> tuple[tuple[int, ...], ...]:
    alpha = alpha_rows(parameter, modulus)
    canonical = canonical_beta(parameter, modulus)
    return tuple(
        tuple(
            (
                canonical[mode][coordinate]
                + shifts[mode] * alpha[mode][coordinate]
            )
            % modulus
            for coordinate in range(4)
        )
        for mode in range(4)
    )


def expected_survivors(
    parameter: int,
    modulus: int,
) -> dict[int, list[tuple[int, ...]]]:
    inverse = pow(parameter, -1, modulus)
    survivors = {
        0: [],
        1: [(-inverse % modulus, parameter, 1, 0)],
        2: [(-inverse % modulus, parameter, -1 % modulus, 0)],
        3: [],
    }
    if parameter in (1, -1 % modulus):
        survivors[3].append(
            (
                -parameter * pow(2, -1, modulus) % modulus,
                parameter,
                parameter,
                1,
            )
        )
    return survivors


def selected_marked_mode(distinguished: int) -> int:
    return 2 if distinguished in (1, 2) else 0


def audit_modulus(modulus: int) -> dict:
    parameters = list(range(1, modulus))
    marking_points = 0
    survivor_markings: dict[tuple[int, int], list[tuple[int, ...]]] = {}

    for parameter in parameters:
        alpha = alpha_rows(parameter, modulus)
        canonical = canonical_beta(parameter, modulus)
        pure_coefficients = {
            word: BASE.permanent_dp(
                [
                    list(canonical[mode] if word[mode] else alpha[mode])
                    for mode in range(4)
                ],
                modulus,
            )
            for word in WORDS4
        }
        assert pure_coefficients[(1, 1, 1, 1)] == (
            4 * parameter
        ) % modulus
        assert all(
            value == 0
            for word, value in pure_coefficients.items()
            if word != (1, 1, 1, 1)
        )

        for distinguished in range(4):
            survivors = []
            for shifts in itertools.product(range(modulus), repeat=4):
                marking_points += 1
                beta = shifted_beta(parameter, shifts, modulus)
                mixed, diagonal_a, diagonal_b = BASE.extension_system(
                    distinguished,
                    alpha,
                    beta,
                    modulus,
                )
                kernel = BASE.nullspace_mod(mixed, modulus)
                if not kernel:
                    continue
                first_nonzero = any(
                    BASE.dot(diagonal_a, vector, modulus)
                    for vector in kernel
                )
                second_nonzero = any(
                    BASE.dot(diagonal_b, vector, modulus)
                    for vector in kernel
                )
                if first_nonzero and second_nonzero:
                    survivors.append(shifts)
            survivor_markings[(parameter, distinguished)] = survivors

        assert {
            distinguished: survivor_markings[(parameter, distinguished)]
            for distinguished in range(4)
        } == expected_survivors(parameter, modulus)

    survivor_count = 0
    extension_directions = 0
    genuine_extensions = 0
    marked_rank_tests = 0
    for parameter in parameters:
        alpha = alpha_rows(parameter, modulus)
        for distinguished, markings in expected_survivors(
            parameter,
            modulus,
        ).items():
            for shifts in markings:
                survivor_count += 1
                beta = shifted_beta(parameter, shifts, modulus)
                mixed, diagonal_a, diagonal_b = BASE.extension_system(
                    distinguished,
                    alpha,
                    beta,
                    modulus,
                )
                assert BASE.matrix_rank_mod(mixed, modulus) == 6
                kernel = BASE.nullspace_mod(mixed, modulus)
                assert len(kernel) == 2
                mode = selected_marked_mode(distinguished)
                pure_map = BASE.one_marked_map(
                    mode,
                    alpha,
                    beta,
                    modulus,
                )
                assert any(row[distinguished] for row in pure_map)

                for coefficients in BASE.projective_vectors(
                    len(kernel),
                    modulus,
                ):
                    extension_directions += 1
                    extension = BASE.combine(
                        coefficients,
                        kernel,
                        modulus,
                    )
                    first = BASE.dot(
                        diagonal_a,
                        extension,
                        modulus,
                    )
                    second = BASE.dot(
                        diagonal_b,
                        extension,
                        modulus,
                    )
                    if not first or not second:
                        continue
                    genuine_extensions += 1
                    marked = BASE.marked_extension(
                        distinguished,
                        extension,
                        alpha,
                        beta,
                        mode,
                        modulus,
                    )
                    assert BASE.matrix_rank_mod(marked, modulus) == 4
                    marked_rank_tests += 1

    expected_survivor_count = 2 * modulus
    assert survivor_count == expected_survivor_count
    assert extension_directions == survivor_count * (modulus + 1)
    assert genuine_extensions == survivor_count * (modulus - 1)
    assert marked_rank_tests == genuine_extensions

    return {
        "modulus": modulus,
        "nonzero_parameters": parameters,
        "marking_points": marking_points,
        "survivor_marking_count": survivor_count,
        "survivor_markings": {
            f"e={parameter},q={distinguished}": [
                list(marking)
                for marking in survivor_markings[(parameter, distinguished)]
            ]
            for parameter in parameters
            for distinguished in range(4)
        },
        "survivor_kernel_dimension": 2,
        "projective_extension_directions": extension_directions,
        "genuine_binary_extensions": genuine_extensions,
        "injective_marked_map_tests": marked_rank_tests,
    }


def main() -> None:
    audits = [audit_modulus(modulus) for modulus in MODULI]
    output = {
        "audited": True,
        "independent_of_primary_imports": True,
        "independent_audit_kernel": BASE.__file__,
        "method": (
            "all nonzero parameters and all-marking finite-field "
            "enumeration, DP permanent, projective kernel directions, "
            "and marked-map ranks"
        ),
        "moduli": list(MODULI),
        "audits": audits,
        "total_marking_points": sum(
            audit["marking_points"] for audit in audits
        ),
        "total_survivor_markings": sum(
            audit["survivor_marking_count"] for audit in audits
        ),
        "total_projective_extension_directions": sum(
            audit["projective_extension_directions"] for audit in audits
        ),
        "total_genuine_binary_extensions": sum(
            audit["genuine_binary_extensions"] for audit in audits
        ),
        "all_genuine_extensions_ternarily_excluded": True,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "primary": PRIMARY.name,
        "primary_sha256": sha256(PRIMARY),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = (
        REPO_ROOT / 'tmp/p5_h31_diagonal_quadric_h0_ruling_audit.json'
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
