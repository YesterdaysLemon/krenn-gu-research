#!/usr/bin/env python3
"""Independent exact sign-chart audit for the q5_221 marked-middle path."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "P5_Q5_221_MARKED_MIDDLE_PATH_OBSTRUCTION.md"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_projective(vector):
    first = next((value for value in vector if value), 0)
    if first < 0:
        return tuple(-value for value in vector)
    return tuple(vector)


def support(vector):
    return tuple(index for index, value in enumerate(vector) if value)


def sign_variants(coordinate_support):
    coordinate_support = tuple(coordinate_support)
    variants = []
    for signs in itertools.product((1, -1), repeat=len(coordinate_support) - 1):
        vector = [0, 0, 0]
        vector[coordinate_support[0]] = 1
        for coordinate, sign in zip(coordinate_support[1:], signs, strict=True):
            vector[coordinate] = sign
        variants.append(tuple(vector))
    return tuple(variants)


def valid_p3_triples():
    triples = set()
    for coordinate_support in itertools.combinations(range(3), 2):
        first, second = sign_variants(coordinate_support)
        for repeated, single in ((first, second), (second, first)):
            permutations = set(
                itertools.permutations((repeated, repeated, single))
            )
            for permutation in permutations:
                triples.add(permutation)
    full = sign_variants((0, 1, 2))
    for omitted in full:
        used = tuple(vector for vector in full if vector != omitted)
        for permutation in itertools.permutations(used):
            triples.add(permutation)
    return triples


def q12_coordinates(line):
    x, y = line
    return canonical_projective((x, x, y))


def q02_coordinates(line):
    x, y = line
    return canonical_projective((x, y, y))


def main() -> None:
    triples = valid_p3_triples()
    assert len(triples) == 42
    assert all(
        len({support(normal) for normal in triple}) == 1
        and len(support(triple[0])) >= 2
        for triple in triples
    )

    # Kernel-line overlap makes the A and B Q12 normals satisfy n0=n1;
    # the h0 incidence at D imposes the same equality there.  No exact
    # P3 sign chart has this property in all three modes.
    chirality_i_survivors = tuple(
        triple
        for triple in triples
        if all(normal[0] == normal[1] for normal in triple)
    )
    assert chirality_i_survivors == ()

    # Chirality II forces h0 and h1 as the first two Q21 normal lines.
    # Their supports differ, and h1 has support one.
    q21_prefix = ((1, -1, 0), (0, 0, 1))
    chirality_ii_extensions = tuple(
        triple for triple in triples if triple[:2] == q21_prefix
    )
    assert chirality_ii_extensions == ()

    output = {
        "audited": True,
        "method": "independent exact P3 sign-chart overlap audit",
        "valid_oriented_sign_triples": len(triples),
        "ambient_row_spaces_enumerated": 0,
        "chirality_I_overlapping_chart_survivors": len(chirality_i_survivors),
        "chirality_II_Q21_chart_survivors": len(chirality_ii_extensions),
        "exact_marked_middle_path_excluded": True,
        "q5_221_excluded": False,
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "global_conjecture_resolved": False,
    }
    output_path = ROOT / "tmp" / "p5_q5_221_marked_middle_path_audited.json"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
