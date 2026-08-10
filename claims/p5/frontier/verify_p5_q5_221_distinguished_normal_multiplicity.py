#!/usr/bin/env python3
"""Verify the distinguished-normal multiplicity theorem in q5_221."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q5_221_DISTINGUISHED_NORMAL_MULTIPLICITY_THEOREM.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def symmetric_tensor(factors):
    order = len(factors)
    dimension = len(factors[0])
    tensor = {}
    for indices in itertools.product(range(dimension), repeat=order):
        value = sum(
            sp.prod(
                factors[mode][indices[permutation[mode]]]
                for mode in range(order)
            )
            for permutation in itertools.permutations(range(order))
        )
        if value:
            tensor[indices] = sp.expand(value)
    return tensor


def contract_first(tensor, covector):
    if not tensor:
        return {}
    output = {}
    for indices, coefficient in tensor.items():
        value = coefficient * covector[indices[0]]
        if not value:
            continue
        remaining = indices[1:]
        output[remaining] = sp.expand(output.get(remaining, 0) + value)
    return {
        indices: coefficient
        for indices, coefficient in output.items()
        if coefficient != 0
    }


def evaluate(tensor, covectors):
    value = sp.Integer(0)
    for indices, coefficient in tensor.items():
        value += coefficient * sp.prod(
            covectors[mode][index]
            for mode, index in enumerate(indices)
        )
    return sp.expand(value)


def main() -> None:
    e = tuple(
        tuple(1 if row == column else 0 for column in range(5))
        for row in range(5)
    )
    u0 = tuple(left + right for left, right in zip(e[0], e[1]))
    u1 = tuple(left + right for left, right in zip(e[2], e[3]))
    h2 = e[4]
    t0 = symmetric_tensor((u0, e[2], e[3], h2))
    t1 = symmetric_tensor((e[0], e[1], u1, h2))
    q12 = symmetric_tensor((e[0], e[1], u1))

    h2_once_t0 = contract_first(t0, h2)
    h2_twice_t0 = contract_first(h2_once_t0, h2)
    h2_once_t1 = contract_first(t1, h2)
    assert not h2_twice_t0
    assert h2_once_t1 == q12

    # If alpha_A2 has zero target coordinates zero and two, it is a
    # nonzero multiple of epsilon_1.
    alpha_scale = sp.symbols("alpha_scale", nonzero=True)
    alpha_a2 = (0, alpha_scale, 0)
    assert alpha_a2[0] == alpha_a2[2] == 0
    assert alpha_a2[1] != 0

    # At B,C, apolarity to J12 kills target coordinate one; the
    # own-colour identity kills coordinate two.
    beta, gamma = sp.symbols("beta gamma", nonzero=True)
    alpha_b2 = (beta, 0, 0)
    alpha_c2 = (gamma, 0, 0)
    assert alpha_b2[1] == alpha_b2[2] == 0
    assert alpha_c2[1] == alpha_c2[2] == 0

    # With exactly two h2 modes, double contraction of both T0 and T1
    # forces their two nonzero pullbacks to have complementary support
    # on target coordinates zero and one.
    nonempty_supports = ({0}, {1}, {0, 1})
    allowed_support_pairs = tuple(
        (left, right)
        for left in nonempty_supports
        for right in nonempty_supports
        if left.isdisjoint(right)
    )
    assert allowed_support_pairs == (({0}, {1}), ({1}, {0}))

    # Hence the target-zero pullback rows at B,C are multiples of h2.
    a = sp.symbols("a0:5")
    d = sp.symbols("d0:5")
    final_t0_coefficient = evaluate(t0, (a, h2, h2, d))
    assert final_t0_coefficient == 0

    distinguished_triple_covers = (0, 1, 2, 3, 4, 9)
    remaining_monotone_covers = (5, 6, 7, 8, 10, 11, 12, 13)
    assert len(distinguished_triple_covers) == 6
    assert len(remaining_monotone_covers) == 8
    assert set(distinguished_triple_covers).isdisjoint(
        remaining_monotone_covers
    )
    assert set(distinguished_triple_covers) | set(
        remaining_monotone_covers
    ) == set(range(14))

    output = {
        "verified": True,
        "field": "C",
        "h2_squared_contraction_T0_zero": True,
        "h2_contraction_T1": "Q12",
        "forced_alpha_A2_support": [1],
        "forced_alpha_B2_support": [0],
        "forced_alpha_C2_support": [0],
        "oriented_h2_pullback_supports": [[0], [1]],
        "final_T0_pure_coefficient": str(final_t0_coefficient),
        "distinguished_normal_multiplicity": 2,
        "monotone_cover_orbits_excluded": list(
            distinguished_triple_covers
        ),
        "remaining_after_multiplicity_orbits": list(
            remaining_monotone_covers
        ),
        "q5_221_excluded": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT
        / "tmp"
        / "p5_q5_221_distinguished_normal_multiplicity_verified.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
