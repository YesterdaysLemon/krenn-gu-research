"""Generate necessary support clauses from actual protected-scaffold Q4 sources.

Every crossing physical entry is retained. No SAT-to-weights converse or
arbitrary-order conclusion is claimed. This generator uses no SAT library;
solver/proof outputs belong in the selected ignored output directory.
"""
from __future__ import annotations

import argparse
from collections import Counter
from functools import lru_cache
import hashlib
import itertools
import json
from pathlib import Path
import shutil
import time


def physical_keys(components):
    return tuple(
        (u, v, a, b)
        for u in range(4 * components)
        for v in range(u + 1, 4 * components)
        if u // 4 != v // 4
        for a in range(3) for b in range(3) if a != b
    )


def selected_words(components, radius=4):
    n = 4 * components
    words = set()
    for c in range(3):
        alternatives = [d for d in range(3) if d != c]
        for size in range(min(radius, n) + 1):
            for places in itertools.combinations(range(n), size):
                for colors in itertools.product(alternatives, repeat=size):
                    word = [c] * n
                    for v, d in zip(places, colors):
                        word[v] = d
                    words.add(tuple(word))
    for colors in itertools.product(range(3), repeat=components):
        words.add(tuple(c for c in colors for _ in range(4)))
    return sorted(words)


def source_polynomial(word, identifiers):
    """Exact word-first recursion through all supported physical matchings."""
    n = len(word)
    scalars = {}
    for u in range(n):
        for v in range(u + 1, n):
            a, b = word[u], word[v]
            if u // 4 == v // 4:
                if a == b and (u ^ v) == a + 1:
                    scalars[u, v] = ()
            elif a != b:
                scalars[u, v] = (identifiers[u, v, a, b],)

    @lru_cache(maxsize=None)
    def expand(mask):
        if not mask:
            return ((),)
        first = (mask & -mask).bit_length() - 1
        rest = mask ^ (1 << first)
        choices = rest
        terms = []
        while choices:
            bit = choices & -choices
            choices ^= bit
            second = bit.bit_length() - 1
            factor = scalars.get((first, second))
            if factor is None:
                continue
            for monomial in expand(rest ^ bit):
                terms.append(tuple(sorted(monomial + factor)))
        return tuple(terms)

    result = Counter(expand((1 << n) - 1))
    if len(set(word)) == 1:
        result[()] -= 1
    result = {m: c for m, c in result.items() if c}
    if any(c != 1 for c in result.values()):
        raise ValueError("unexpected combined coefficient; bridge needs review")
    return result


def generate(components, output):
    output.mkdir(parents=True, exist_ok=False)
    started = time.monotonic()
    keys = physical_keys(components)
    identifiers = {key: i + 1 for i, key in enumerate(keys)}
    words = selected_words(components)
    products = {}
    variable_count = len(keys)
    clause_count = 0
    term_histogram = Counter()
    degree_histogram = Counter()
    equation_hash = hashlib.sha256()
    body = output / "clauses.body"
    with body.open("wb") as stream:
        def clause(literals):
            nonlocal clause_count
            stream.write((" ".join(map(str, literals)) + " 0\n").encode("ascii"))
            clause_count += 1

        def active(monomial):
            nonlocal variable_count
            if len(monomial) == 1:
                return monomial[0]
            if monomial not in products:
                variable_count += 1
                z = variable_count
                products[monomial] = z
                for factor in monomial:
                    clause((-z, factor))
                clause((z, *(-v for v in monomial)))
            return products[monomial]

        for number, word in enumerate(words, 1):
            polynomial = source_polynomial(word, identifiers)
            ordered = sorted(polynomial.items())
            equation_hash.update(
                (json.dumps((word, ordered), separators=(",", ":")) + "\n").encode()
            )
            term_histogram[len(ordered)] += 1
            degree_histogram.update(len(m) for m, _ in ordered)
            support = [active(m) for m, _ in ordered if m]
            if () in polynomial:
                clause(support)
            else:
                for z in support:
                    clause((-z, *(other for other in support if other != z)))
            if number % 5000 == 0:
                print(json.dumps({"words_done": number, "variables": variable_count,
                                  "clauses": clause_count,
                                  "seconds": time.monotonic() - started}), flush=True)
    cnf = output / "instance.cnf"
    with cnf.open("wb") as stream, body.open("rb") as source:
        stream.write(f"p cnf {variable_count} {clause_count}\n".encode("ascii"))
        shutil.copyfileobj(source, stream)
    # Only a generated spool in this newly created output directory is removed.
    body.unlink()
    with cnf.open("rb") as stream:
        cnf_hash = hashlib.file_digest(stream, "sha256").hexdigest()
    result = {
        "status": "GENERATED_NECESSARY_Q4_MODEL_NOT_SOLVED",
        "components": components, "physical_vertices": 4 * components,
        "physical_variables": len(keys), "source_words": len(words),
        "variables": variable_count, "clauses": clause_count,
        "distinct_product_flags": len(products),
        "term_count_histogram": dict(sorted(term_histogram.items())),
        "term_degree_histogram": dict(sorted(degree_histogram.items())),
        "equation_sha256": equation_hash.hexdigest(), "cnf_lf_sha256": cnf_hash,
        "elapsed_seconds": time.monotonic() - started,
        "scope": "fixed order and necessary support only; global UNRESOLVED",
    }
    (output / "physical-entries.json").write_text(json.dumps(keys) + "\n", encoding="utf-8")
    (output / "result.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--components", type=int, default=3)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    if not 2 <= args.components <= 4:
        parser.error("initial bounded probe supports 2 through 4 components")
    print(json.dumps(generate(args.components, args.output_dir), indent=2))


if __name__ == "__main__":
    main()
