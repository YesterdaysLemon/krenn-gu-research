"""Reproduce the frozen pure-zero-root necessary-support CNF, without a solver."""

from itertools import combinations, product
from pathlib import Path
import argparse
import hashlib
import json


CNF_SHA256 = "4415ea3d243603910729098d104240ca2d6fd2fa1d2843098e3131b4088ac1ac"


def build_instance():
    identifiers = {}
    clauses = []

    def variable(label):
        if label not in identifiers:
            identifiers[label] = len(identifiers) + 1
        return identifiers[label]

    colours = range(3)
    edges = list(combinations(range(6), 2))
    entry = {
        (u, v, a, b): variable(("entry", u, v, a, b))
        for u, v in edges
        for a, b in product(colours, repeat=2)
    }
    # AA and BB edges are nonzero matrix units; cross edges may be zero.
    for u, v in edges:
        if (u < 3) == (v < 3):
            choices = [entry[u, v, a, b] for a, b in product(colours, repeat=2)]
            clauses.append(choices)
            clauses.extend([[-x, -y] for x, y in combinations(choices, 2)])

    # All nine full four-vertex cofactors, each with all 81 colour words.
    for i, j in product(colours, repeat=2):
        remainder = [v for v in range(6) if v not in (i, j + 3)]
        u, v, w, z = remainder
        matchings = [((u, v), (w, z)), ((u, w), (v, z)), ((u, z), (v, w))]
        for word in product(colours, repeat=4):
            colour = dict(zip(remainder, word))
            terms = []
            for k, matching in enumerate(matchings):
                factors = [entry[p, q, colour[p], colour[q]] for p, q in matching]
                term = variable(("term", i, j, word, k))
                terms.append(term)
                clauses.extend(
                    (
                        [-term, factors[0]],
                        [-term, factors[1]],
                        [term, -factors[0], -factors[1]],
                    )
                )
            if i == j and word == (i,) * 4:
                clauses.append(terms)
            else:
                # A zero coefficient cannot contain exactly one nonzero term.
                for k in range(3):
                    clauses.append([-terms[k]] + [terms[l] for l in range(3) if l != k])

    # Re-rooting excludes rank >= 2 cross blocks. Rank-one supports are
    # Cartesian products. Preserve duplicate/tautological clauses to reproduce
    # the exact frozen instance; the checker normalizes them logically.
    for u, v in product(range(3), range(3, 6)):
        for a, b, c, d in product(colours, repeat=4):
            clauses.append([-entry[u, v, a, b], -entry[u, v, c, d], entry[u, v, a, d]])
            clauses.append([-entry[u, v, a, b], -entry[u, v, c, d], entry[u, v, c, b]])

    # The full P2 pure-tensor lemma supplies a row-anchor disjunction and an
    # independent column-anchor disjunction for each off-diagonal rectangle.
    for i, j in product(colours, repeat=2):
        if i == j:
            continue
        aa = [v for v in range(3) if v != i]
        bb = [v for v in range(3, 6) if v != j + 3]
        row_anchor, column_anchor = {}, {}
        for u, a in product(aa, colours):
            selector = variable(("rowanchor", i, j, u, a))
            row_anchor[u, a] = selector
            for v, p, q in product(bb, colours, colours):
                if p != a:
                    clauses.append([-selector, -entry[u, v, p, q]])
        for v, b in product(bb, colours):
            selector = variable(("colanchor", i, j, v, b))
            column_anchor[v, b] = selector
            for u, p, q in product(aa, colours, colours):
                if q != b:
                    clauses.append([-selector, -entry[u, v, p, q]])
        for a, b in product(colours, repeat=2):
            clauses.append(
                [-entry[aa[0], aa[1], a, b], row_anchor[aa[0], a], row_anchor[aa[1], b]]
            )
            clauses.append(
                [
                    -entry[bb[0], bb[1], a, b],
                    column_anchor[bb[0], a],
                    column_anchor[bb[1], b],
                ]
            )
    return len(identifiers), clauses


def instance_bytes():
    variables, clauses = build_instance()
    # Explicit CRLF is a portable byte-format choice preserving the audited
    # frozen hash. No platform-dependent text-mode newline conversion is used.
    lines = [f"p cnf {variables} {len(clauses)}"]
    lines.extend(" ".join(map(str, clause)) + " 0" for clause in clauses)
    raw = ("\r\n".join(lines) + "\r\n").encode("ascii")
    if variables != 2394 or len(clauses) != 11394:
        raise RuntimeError("frozen instance dimensions changed")
    if hashlib.sha256(raw).hexdigest() != CNF_SHA256:
        raise RuntimeError("frozen instance hash changed")
    return raw


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    raw = instance_bytes()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(raw)
    print(
        json.dumps(
            {
                "variables": 2394,
                "clauses": 11394,
                "sha256": CNF_SHA256,
                "bytes": len(raw),
            }
        )
    )


if __name__ == "__main__":
    main()
