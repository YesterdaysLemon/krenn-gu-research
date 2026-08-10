"""Exact verifier for a six-vertex, four-colour Question-2 witness.

The first four vertices are outputs.  Vertices 5 and 6 are heralds and
must be red.  All edge weights and all arithmetic in this verifier are
exact rational numbers.
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

REPO_ROOT, HERE = _bootstrap_repository(__file__)


import argparse
import json
from collections import defaultdict
from fractions import Fraction
from itertools import product
from pathlib import Path
from typing import Iterator


Vertex = int
Colour = str
Pair = tuple[Vertex, Vertex]
Matching = tuple[Pair, ...]
ColourWord = tuple[Colour, ...]


# A key (u, v, c) denotes a monochromatic edge of colour c at both
# endpoints.  Distinct colours on the same pair are parallel edge modes.
EDGE_MODES: dict[tuple[Vertex, Vertex, Colour], Fraction] = {
    (1, 2, "r"): Fraction(-1, 2),
    (1, 3, "r"): Fraction(-1, 2),
    (2, 4, "r"): Fraction(1, 2),
    (3, 4, "r"): Fraction(1, 2),
    (1, 5, "r"): Fraction(1),
    (1, 6, "r"): Fraction(1),
    (2, 6, "r"): Fraction(1),
    (3, 6, "r"): Fraction(1),
    (4, 6, "r"): Fraction(1),
    (4, 5, "r"): Fraction(-1),
    (5, 6, "r"): Fraction(2),
    (1, 3, "c1"): Fraction(1, 2),
    (2, 4, "c1"): Fraction(1),
    (1, 2, "c2"): Fraction(1, 2),
    (3, 4, "c2"): Fraction(1),
    (1, 4, "c3"): Fraction(1, 2),
    (2, 3, "c3"): Fraction(1),
}


EXPECTED_NONZERO: dict[ColourWord, Fraction] = {
    ("r", "r", "r", "r", "r", "r"): Fraction(1),
    ("c1", "c1", "c1", "c1", "r", "r"): Fraction(1),
    ("c2", "c2", "c2", "c2", "r", "r"): Fraction(1),
    ("c3", "c3", "c3", "c3", "r", "r"): Fraction(1),
}


def perfect_matchings(vertices: tuple[Vertex, ...]) -> Iterator[Matching]:
    """Generate every perfect matching once."""

    if not vertices:
        yield ()
        return
    first = vertices[0]
    for index in range(1, len(vertices)):
        second = vertices[index]
        remainder = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(remainder):
            yield ((first, second),) + tail


def fraction_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def matching_text(matching: Matching) -> str:
    return ",".join(f"{u}{v}" for u, v in matching)


def enumerate_terms() -> tuple[
    list[Matching],
    dict[ColourWord, list[tuple[Matching, Fraction]]],
]:
    by_pair: dict[Pair, list[tuple[Colour, Fraction]]] = defaultdict(list)
    for (u, v, colour), weight in EDGE_MODES.items():
        assert 1 <= u < v <= 6
        assert weight
        by_pair[(u, v)].append((colour, weight))

    matchings = list(perfect_matchings((1, 2, 3, 4, 5, 6)))
    terms: dict[ColourWord, list[tuple[Matching, Fraction]]] = defaultdict(list)
    for matching in matchings:
        choices = [by_pair.get(pair, []) for pair in matching]
        if not all(choices):
            continue
        for selected in product(*choices):
            word: list[Colour | None] = [None] * 6
            term_weight = Fraction(1)
            for (u, v), (colour, edge_weight) in zip(
                matching, selected, strict=True
            ):
                word[u - 1] = colour
                word[v - 1] = colour
                term_weight *= edge_weight
            assert all(colour is not None for colour in word)
            terms[tuple(word)].append((matching, term_weight))  # type: ignore[arg-type]
    return matchings, terms


def verify() -> dict[str, object]:
    matchings, terms = enumerate_terms()
    assert len(matchings) == 15
    assert len(EDGE_MODES) == 17
    assert sum(len(group) for group in terms.values()) == 19
    assert len(terms) == 9

    coefficients = {
        word: sum((weight for _, weight in group), Fraction())
        for word, group in terms.items()
    }
    nonzero = {
        word: coefficient
        for word, coefficient in coefficients.items()
        if coefficient
    }
    assert nonzero == EXPECTED_NONZERO

    groups = []
    for word in sorted(terms):
        group = terms[word]
        groups.append(
            {
                "word": list(word),
                "terms": [
                    {
                        "matching": matching_text(matching),
                        "weight": fraction_text(weight),
                    }
                    for matching, weight in group
                ],
                "coefficient": fraction_text(coefficients[word]),
            }
        )

    return {
        "verified": True,
        "arithmetic": "fractions.Fraction",
        "parameters": {
            "n": 6,
            "k": 4,
            "d": 4,
            "output_vertices": [1, 2, 3, 4],
            "red_herald_vertices": [5, 6],
        },
        "counts": {
            "perfect_matchings_of_K6": len(matchings),
            "nonzero_edge_modes": len(EDGE_MODES),
            "raw_nonzero_coloured_matching_terms": sum(
                len(group) for group in terms.values()
            ),
            "supported_colour_words_before_cancellation": len(terms),
            "nonzero_coefficients_after_cancellation": len(nonzero),
        },
        "coefficient_groups": groups,
        "conclusion": (
            "Exactly the four k-monochromatic colourings have coefficient "
            "one; every other inherited vertex colouring has coefficient zero."
        ),
        "global_question_1_resolved": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        help="Optionally write the exact audit result as JSON.",
    )
    args = parser.parse_args()
    payload = verify()
    text = json.dumps(payload, indent=2)
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
