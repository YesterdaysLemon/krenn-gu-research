#!/usr/bin/env python3
"""Independent no-import audit of the two-residual port factorisation."""

from __future__ import annotations

import itertools
import json
import math
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
THEOREM = ROOT / "TWO_RESIDUAL_NONBLOCKER_TWO_PORT_FACTORISATION.md"


def hafnian_terms(vertices: tuple[int, ...]):
    if not vertices:
        return [()]
    anchor = vertices[-1]
    terms = []
    for index, partner in enumerate(vertices[:-1]):
        rest = vertices[:index] + vertices[index + 1 : -1]
        for tail in hafnian_terms(rest):
            terms.append(tail + ((partner, anchor),))
    return terms


def audit_four_vertex() -> list[tuple[tuple[int, int], ...]]:
    terms = [
        tuple(sorted(tuple(sorted(edge)) for edge in term))
        for term in hafnian_terms((0, 1, 2, 3))
    ]
    expected = {
        ((0, 1), (2, 3)),
        ((0, 2), (1, 3)),
        ((0, 3), (1, 2)),
    }
    assert set(terms) == expected
    return sorted(terms)


def audit_laplace(max_roots: int = 6) -> list[dict[str, int]]:
    records = []
    for roots in range(2, max_roots + 1):
        modes = roots + 2
        signatures = Counter()
        for permutation in itertools.permutations(range(modes)):
            port_pair = tuple(permutation[-2:])
            root_assignment = tuple(permutation[:-2])
            signatures[(frozenset(port_pair), root_assignment)] += 1
        assert set(signatures.values()) == {2}
        assert len(signatures) == math.comb(modes, 2) * math.factorial(roots)
        assert sum(signatures.values()) == math.factorial(modes)
        records.append(
            {
                "roots": roots,
                "modes": modes,
                "cofactor_terms": len(signatures),
                "port_assignments_per_term": 2,
                "permanent_assignments": math.factorial(modes),
            }
        )
    return records


def audit_boundary_logic() -> dict[str, bool]:
    # A rank-one coordinate monomial is nonzero on the coordinate torus.
    torus_samples = tuple(itertools.product((-2, -1, 1, 2), repeat=6))
    coordinate_nonzero = all(sample[0] * sample[5] != 0 for sample in torus_samples)
    assert coordinate_nonzero

    # A representative irreducible rank-two bilinear has many torus zeros.
    rank_two_zero = False
    for sample in torus_samples:
        x0, x1, _x2, y0, y1, _y2 = sample
        if x0 * y0 + x1 * y1 == 0:
            rank_two_zero = True
            break
    assert rank_two_zero
    return {
        "coordinate_monomial_nonzero_on_sampled_torus": coordinate_nonzero,
        "rank_two_sample_has_torus_zero": rank_two_zero,
        "written_irreducibility_argument_required": True,
    }


def main() -> None:
    theorem = THEOREM.read_text(encoding="utf-8")
    for phrase in (
        "There are exactly three perfect matchings",
        "bilinear polynomial is irreducible",
        "Every monomial occurs exactly once",
        "arbitrary-order local-to-global reduction: UNKNOWN",
    ):
        assert phrase in theorem

    print(
        json.dumps(
            {
                "status": "pass",
                "audit": "independent no-import matching recurrence and assignment ledger",
                "field": "integer/rational audit of characteristic-zero proof",
                "four_vertex_matchings": audit_four_vertex(),
                "laplace": audit_laplace(),
                "boundary_logic": audit_boundary_logic(),
                "repository_imports_used": False,
                "finite_field_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
