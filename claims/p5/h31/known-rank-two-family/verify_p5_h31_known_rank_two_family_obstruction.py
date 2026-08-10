#!/usr/bin/env python3
"""Verify the H31 no-lift theorem for the known rank-two P4 family."""

from __future__ import annotations

import hashlib
import itertools
import json
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
THEOREM = ROOT / "P5_H31_KNOWN_RANK_TWO_FAMILY_OBSTRUCTION.md"
PURE_FAMILY = REPO_ROOT / 'claims/p4/classifications/pair-geometry/decomposable-rank-two-family/P4_DECOMPOSABLE_RANK_TWO_FAMILY.md'
BITS = tuple(itertools.product((0, 1), repeat=4))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def permanent(rows: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    return sp.factor(
        sum(
            sp.prod(
                rows[row][permutation[row]]
                for row in range(4)
            )
            for permutation in itertools.permutations(range(4))
        )
    )


def binary_coefficients(
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
) -> dict[str, sp.Expr]:
    return {
        "".join(map(str, bits)): permanent(
            tuple(
                beta[mode] if bits[mode] else alpha[mode]
                for mode in range(4)
            )
        )
        for bits in BITS
    }


def one_marked_map(
    mode: int,
    alpha: tuple[tuple[sp.Expr, ...], ...],
    beta: tuple[tuple[sp.Expr, ...], ...],
) -> sp.Matrix:
    rows = []
    for bits in itertools.product((0, 1), repeat=3):
        selected = []
        bit_index = 0
        for other in range(4):
            if other == mode:
                selected.append(None)
            else:
                selected.append(
                    beta[other]
                    if bits[bit_index]
                    else alpha[other]
                )
                bit_index += 1
        coefficient_row = []
        for coordinate in range(4):
            basis = tuple(
                int(index == coordinate)
                for index in range(4)
            )
            coefficient_row.append(
                permanent(
                    tuple(
                        basis if other == mode else selected[other]
                        for other in range(4)
                    )
                )
            )
        rows.append(coefficient_row)
    return sp.Matrix(rows)


def main() -> None:
    epsilon, iota = sp.symbols("epsilon iota", nonzero=True)
    ell, jay, chi = sp.symbols("ell jay chi")
    gamma = epsilon * iota * ell
    x = sp.symbols("x0:4")
    y = sp.symbols("y0:4")
    variables = x + y

    beta_shared = (
        (0, 1, (chi + gamma) / epsilon),
        (0, 0, 1),
        (0, 1, 0),
        (1, 0, iota),
    )
    alpha_shared = (
        (1, jay, 0),
        (ell, 1, -iota * ell),
        (-1 / iota, 0, 1),
        (0, 0, -1 / epsilon),
    )
    alpha_p = tuple(
        alpha_shared[mode] + (x[mode],)
        for mode in range(4)
    )
    beta_p = tuple(
        beta_shared[mode] + (y[mode],)
        for mode in range(4)
    )
    coefficients = binary_coefficients(alpha_p, beta_p)
    mixed_words = tuple(
        word for word in coefficients if word not in ("0000", "1111")
    )
    mixed_matrix = sp.Matrix(
        [
            [
                sp.diff(coefficients[word], variable)
                for variable in variables
            ]
            for word in mixed_words
        ]
    )
    alpha_diagonal = sp.Matrix(
        [[
            sp.diff(coefficients["0000"], variable)
            for variable in variables
        ]]
    )
    beta_diagonal = sp.Matrix(
        [[
            sp.diff(coefficients["1111"], variable)
            for variable in variables
        ]]
    )

    generic_rows = tuple(
        mixed_words.index(word)
        for word in (
            "0001",
            "0010",
            "0011",
            "0110",
            "1000",
            "1010",
            "1011",
        )
    )
    generic_columns = (0, 1, 2, 3, 4, 5, 7)
    generic_minor = sp.factor(
        mixed_matrix[
            list(generic_rows),
            list(generic_columns),
        ].det()
    )
    assert generic_minor == (
        -4
        * iota**2
        * ell**4
        * (chi + epsilon * iota * ell)
        / epsilon**4
    )
    generic_kernel = sp.Matrix(
        [
            -(jay * ell + 1) / ell,
            -1,
            0,
            1 / (epsilon * iota * ell),
            chi / (epsilon * iota * ell),
            1 / (iota * ell),
            1,
            0,
        ]
    )
    assert (mixed_matrix * generic_kernel).applyfunc(
        sp.simplify
    ) == sp.zeros(14, 1)
    assert sp.factor((alpha_diagonal * generic_kernel)[0]) == 0
    assert sp.simplify(
        (beta_diagonal * generic_kernel)[0]
        - 2
        * (chi + epsilon * iota * ell)
        / (epsilon * iota * ell)
    ) == 0

    zero_substitution = {ell: 0}
    zero_matrix = mixed_matrix.subs(zero_substitution)
    zero_alpha_diagonal = alpha_diagonal.subs(zero_substitution)
    zero_beta_diagonal = beta_diagonal.subs(zero_substitution)
    zero_rows = tuple(
        mixed_words.index(word)
        for word in ("0001", "0010", "0110", "0111", "1000", "1001")
    )
    zero_columns = (0, 1, 2, 3, 4, 7)
    zero_minor = sp.factor(
        zero_matrix[list(zero_rows), list(zero_columns)].det()
    )
    assert zero_minor == 2 * chi / (epsilon**3 * iota)

    first_kernel = sp.Matrix(
        [
            -iota,
            0,
            0,
            1 / epsilon,
            chi / epsilon,
            1,
            0,
            0,
        ]
    )
    second_kernel = sp.Matrix(
        [-jay, -1, 0, 0, 1, 0, 1, 0]
    )
    assert (zero_matrix * first_kernel).applyfunc(
        sp.simplify
    ) == sp.zeros(14, 1)
    assert (zero_matrix * second_kernel).applyfunc(
        sp.simplify
    ) == sp.zeros(14, 1)
    assert (zero_alpha_diagonal * first_kernel)[0] == 0
    assert sp.simplify(
        (zero_alpha_diagonal * second_kernel)[0]
        + 2 * jay / (epsilon * iota)
    ) == 0
    assert sp.simplify(
        (zero_beta_diagonal * first_kernel)[0]
        - 2 * chi / epsilon
    ) == 0
    assert sp.simplify(
        (zero_beta_diagonal * second_kernel)[0] - 2
    ) == 0

    tau, upsilon = sp.symbols("tau upsilon")
    extension = tau * first_kernel + upsilon * second_kernel
    alpha_s = (
        (1, jay, 0, -epsilon * iota),
        (0, 1, 0, 0),
        (-1 / iota, 0, 1, 0),
        (0, 0, -1 / epsilon, 1),
    )
    beta_s = (
        (0, 1, chi / epsilon, chi),
        (0, 0, 1, epsilon),
        (0, 1, 0, 0),
        (1, 0, iota, 0),
    )
    alpha_p_exceptional = tuple(
        tuple(
            entry.subs(zero_substitution)
            if isinstance(entry, sp.Basic)
            else entry
            for entry in alpha_shared[mode]
        ) + (extension[mode],)
        for mode in range(4)
    )
    beta_p_exceptional = tuple(
        tuple(
            entry.subs(zero_substitution)
            if isinstance(entry, sp.Basic)
            else entry
            for entry in beta_shared[mode]
        ) + (extension[4 + mode],)
        for mode in range(4)
    )

    marked_p = one_marked_map(
        1,
        alpha_p_exceptional,
        beta_p_exceptional,
    )
    marked_p_minor = sp.factor(marked_p[[0, 2, 6, 7], :].det())
    assert marked_p_minor == (
        8
        * jay
        * upsilon**2
        * (chi * tau + epsilon * upsilon)
        / (epsilon**4 * iota)
    )

    marked_s = one_marked_map(1, alpha_s, beta_s)
    marked_s_minor = sp.factor(
        marked_s[[0, 2, 7], [0, 2, 3]].det()
    )
    assert marked_s_minor == 4 * chi * jay / epsilon
    source_one = sp.Matrix([0, 1, 0, 0])
    assert (marked_s * source_one).applyfunc(
        sp.simplify
    ) == sp.zeros(8, 1)

    output = {
        "verified": True,
        "field": "C",
        "pure_family_parameters": ["e", "i", "l", "j", "c"],
        "generic_l_nonzero_mixed_rank": 7,
        "generic_l_nonzero_alpha_diagonal": 0,
        "exceptional_l_zero_mixed_rank": 6,
        "exceptional_binary_Delta2_conditions": [
            "j",
            "u",
            "c*t+e*u",
        ],
        "exceptional_Hp_one_marked_rank": 4,
        "exceptional_Hs_one_marked_rank": 3,
        "exceptional_Hs_kernel": "span(e_1^*)",
        "forced_third_target_row": "zero",
        "known_rank_two_family_H31_lift_possible": False,
        "dependency": {
            "file": PURE_FAMILY.name,
            "sha256": sha256(PURE_FAMILY),
        },
        "H31_excluded": False,
        "P5_to_Delta3_resolved": False,
        "global_conjecture_resolved": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
    }
    output_path = REPO_ROOT / 'tmp/p5_h31_known_rank_two_family_verified.json'
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
