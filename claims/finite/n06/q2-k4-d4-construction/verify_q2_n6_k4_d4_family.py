"""Symbolically verify the full-support family behind the d=4 Q2 witness.

Requires SymPy.  The calculation independently enumerates the 15 perfect
matchings and every supported parallel-colour choice before simplifying the
resulting rational functions.
"""

from __future__ import annotations
import sys as _bootstrap_sys
from pathlib import Path as _BootstrapPath

for _bootstrap_parent in _BootstrapPath(__file__).resolve().parents:
    if (_bootstrap_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        _bootstrap_sys.path.insert(0, str(_bootstrap_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap as _bootstrap_repository  # noqa: E402

REPO_ROOT, HERE = _bootstrap_repository(__file__, also=["."])


import json
from collections import defaultdict
from itertools import product

from sympy import Expr, factor, simplify, symbols

from verify_q2_n6_k4_d4_construction import (
    ColourWord,
    Matching,
    perfect_matchings,
)


def symbolic_coefficients(
    edge_modes: dict[tuple[int, int, str], Expr],
) -> tuple[int, dict[ColourWord, Expr]]:
    by_pair: dict[tuple[int, int], list[tuple[str, Expr]]] = defaultdict(list)
    for (left, right, colour), weight in edge_modes.items():
        by_pair[(left, right)].append((colour, weight))

    coefficients: dict[ColourWord, Expr] = defaultdict(lambda: simplify(0))
    raw_terms = 0
    for matching in perfect_matchings((1, 2, 3, 4, 5, 6)):
        choices = [by_pair.get(pair, []) for pair in matching]
        if not all(choices):
            continue
        for selected in product(*choices):
            word: list[str | None] = [None] * 6
            term = simplify(1)
            for (left, right), (colour, weight) in zip(
                matching, selected, strict=True
            ):
                word[left - 1] = colour
                word[right - 1] = colour
                term *= weight
            assert all(colour is not None for colour in word)
            coefficients[tuple(word)] += term  # type: ignore[arg-type]
            raw_terms += 1
    return raw_terms, dict(coefficients)


def main() -> None:
    # Eight arbitrary nonzero parameters.
    h, p, s, t, u, alpha1, alpha2, alpha3 = symbols(
        "h p s t u alpha1 alpha2 alpha3",
        nonzero=True,
    )
    lambda_r, lambda1, lambda2, lambda3 = symbols(
        "lambda_r lambda1 lambda2 lambda3",
        nonzero=True,
    )

    edge_modes = {
        # Red output and output--herald modes.
        (1, 2, "r"): -p * s / h,
        (1, 3, "r"): -p * t / h,
        (2, 4, "r"): lambda_r / (2 * p * t),
        (3, 4, "r"): lambda_r / (2 * p * s),
        (1, 5, "r"): p,
        (1, 6, "r"): 2 * p**2 * s * t * u / (lambda_r * h),
        (2, 6, "r"): s,
        (3, 6, "r"): t,
        (4, 6, "r"): u,
        (4, 5, "r"): -lambda_r * h / (2 * p * s * t),
        (5, 6, "r"): h,
        # Three output colours.  Only each pair product is constrained.
        (1, 3, "c1"): alpha1,
        (2, 4, "c1"): lambda1 / (h * alpha1),
        (1, 2, "c2"): alpha2,
        (3, 4, "c2"): lambda2 / (h * alpha2),
        (1, 4, "c3"): alpha3,
        (2, 3, "c3"): lambda3 / (h * alpha3),
    }

    raw_terms, coefficients = symbolic_coefficients(edge_modes)
    assert raw_terms == 19
    assert len(coefficients) == 9
    targets = {
        ("r", "r", "r", "r", "r", "r"): lambda_r,
        ("c1", "c1", "c1", "c1", "r", "r"): lambda1,
        ("c2", "c2", "c2", "c2", "r", "r"): lambda2,
        ("c3", "c3", "c3", "c3", "r", "r"): lambda3,
    }
    simplified = {
        word: factor(simplify(coefficient))
        for word, coefficient in coefficients.items()
    }
    for word, coefficient in simplified.items():
        assert coefficient == targets.get(word, 0)

    # Converse derivation on this fixed support, assuming every displayed
    # edge mode is nonzero.  The five mixed-word equations solve the six
    # dependent red variables; the red target then becomes 2*p*t*c.
    a, b, c, d, q, v = symbols("a b c d q v", nonzero=True)
    reconstructed = {
        a: -p * s / h,
        b: -p * t / h,
        d: t * c / s,
        v: -c * h / s,
        q: p * u * s / (c * h),
    }
    mixed_equations = [
        c * h + s * v,
        b * h + p * t,
        d * h + t * v,
        a * h + p * s,
        p * u + q * v,
    ]
    assert all(
        simplify(equation.subs(reconstructed)) == 0
        for equation in mixed_equations
    )
    red_coefficient = (
        a * d * h
        + a * t * v
        + b * c * h
        + b * s * v
        + p * c * t
        + p * s * d
    )
    assert factor(simplify(red_coefficient.subs(reconstructed))) == 2 * p * t * c
    assert simplify((2 * p * t * c).subs(c, 1 / (2 * p * t))) == 1
    assert (
        simplify(
            (2 * p * t * c).subs(c, lambda_r / (2 * p * t))
        )
        == lambda_r
    )

    payload = {
        "verified": True,
        "scope": "all nonzero weightings on the displayed 17-mode support",
        "free_nonzero_parameters": [
            "h",
            "p",
            "s",
            "t",
            "u",
            "alpha1",
            "alpha2",
            "alpha3",
        ],
        "unit_target_family_dimension": 8,
        "arbitrary_nonzero_target_amplitudes": [
            "lambda_r",
            "lambda1",
            "lambda2",
            "lambda3",
        ],
        "weighted_family_dimension": 12,
        "raw_nonzero_coloured_matching_terms": raw_terms,
        "supported_colour_words": len(coefficients),
        "target_coefficients": 4,
        "zero_mixed_coefficients": 5,
        "complete_full_support_parameterization": True,
        "concrete_tweet_point": {
            "h": 2,
            "p": 1,
            "s": 1,
            "t": 1,
            "u": 1,
            "alpha1": "1/2",
            "alpha2": "1/2",
            "alpha3": "1/2",
            "lambda_r": 1,
            "lambda1": 1,
            "lambda2": 1,
            "lambda3": 1,
        },
        "global_question_1_resolved": False,
    }
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
