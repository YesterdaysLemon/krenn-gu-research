"""Exact protected two-K4 source expansion and necessary support CNF.

All 96 hollow crossing entries remain free.  The source is expanded matching
first.  No SAT solver is needed for generation or exact certificate replay.
"""
from __future__ import annotations

from collections import Counter, defaultdict
import hashlib
import itertools
import json


class ScaffoldCNF:
    """Minimal deterministic DIMACS carrier; logical semantics live in build."""

    def __init__(self):
        self.clauses = []
        self.nv = 0

    def append(self, clause):
        self.clauses.append(list(clause))
        self.nv = max(self.nv, max(map(abs, clause), default=0))

    def extend(self, clauses):
        for clause in clauses:
            self.append(clause)

    def dimacs(self):
        lines = [f"p cnf {self.nv} {len(self.clauses)}"]
        lines.extend(" ".join(map(str, clause)) + " 0" if clause else "0"
                     for clause in self.clauses)
        return ("\n".join(lines) + "\n").encode("ascii")


MATCH = (((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2)))
VARIABLES = tuple((c, d, i, j) for c in range(3) for d in range(3) if c != d
                  for i in range(4) for j in range(4))


def polynomials():
    edges = defaultdict(list)
    for side in (0, 4):
        for c, matching in enumerate(MATCH):
            for u, v in matching:
                edges[u + side, v + side].append((c, c, ()))
    for identifier, (c, d, i, j) in enumerate(VARIABLES, 1):
        edges[i, j + 4].append((c, d, (identifier,)))
    matchings = sorted({tuple(sorted(tuple(sorted(p[i:i + 2])) for i in (0, 2, 4, 6)))
                        for p in itertools.permutations(range(8))})
    assert len(matchings) == 105
    result = defaultdict(Counter)
    for matching in matchings:
        for choices in itertools.product(*(edges[pair] for pair in matching)):
            word = [0] * 8
            monomial = []
            for (u, v), (a, b, factors) in zip(matching, choices):
                word[u], word[v] = a, b
                monomial.extend(factors)
            result[tuple(word)][tuple(sorted(monomial))] += 1
    for c in range(3):
        result[(c,) * 8][()] -= 1
    return {w: {m: coefficient for m, coefficient in p.items() if coefficient}
            for w, p in result.items()}


def build(mode):
    if mode not in ("pair", "binary", "binary-shores", "binary-shores-minority",
                    "four-minority", "full"):
        raise ValueError("unknown scaffold equation subsystem")
    rows = polynomials()
    words = [w for w in itertools.product(range(3), repeat=8)
             if (mode == "pair" and set(w) <= {0, 1})
             or (mode != "pair" and len(set(w)) <= 2)
             or (mode.startswith("binary-shores") and (len(set(w[:4])) == 1 or len(set(w[4:])) == 1))
             or (mode == "binary-shores-minority" and max(w.count(c) for c in range(3)) >= 6)
             or (mode == "four-minority" and max(w.count(c) for c in range(3)) >= 4)
             or mode == "full"]
    cnf = ScaffoldCNF()
    monomials = {}
    next_id = len(VARIABLES) + 1

    def active(m):
        nonlocal next_id
        if len(m) == 1:
            return m[0]
        if m not in monomials:
            z = next_id
            next_id += 1
            monomials[m] = z
            cnf.extend([[-z, v] for v in m])
            cnf.append([z, *(-v for v in m)])
        return monomials[m]

    histogram = Counter()
    equation_digest = hashlib.sha256()
    for word in words:
        row = rows.get(word, {})
        histogram[len(row)] += 1
        record = (word, sorted(row.items()))
        equation_digest.update((json.dumps(record, separators=(",", ":")) + "\n").encode())
        constant = () in row
        support = [active(m) for m in sorted(row) if m]
        if constant:
            # The fixed nonzero constant forbids all other terms vanishing.
            cnf.append(support)
        else:
            # A zero sum cannot have exactly one nonzero monomial.
            for z in support:
                cnf.append([-z, *(other for other in support if other != z)])
    return cnf, words, histogram, equation_digest.hexdigest(), len(monomials)

