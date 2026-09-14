"""Substitute physical Laurent entries into the complete shared source.

Unlike the independent word-first physical matching audit, this replay uses the
full 96-variable polynomials and combines Laurent terms after substitution.
"""
from __future__ import annotations

from collections import Counter
import itertools
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))
from krenn_gu.bootstrap import bootstrap  # noqa: E402

ROOT, _ = bootstrap(__file__)
from krenn_gu.scaffold_source import VARIABLES, polynomials  # noqa: E402

FIXTURE = ROOT / "tests/fixtures/eight_vertex_scaffold_subsystem_controls.json"


def replay(certificate):
    if certificate["schema"] != "n8-protected-scaffold-laurent-controls-v1":
        raise ValueError("wrong schema")
    pairs = tuple(tuple(pair) for pair in certificate["parameter_order"])
    if pairs != tuple((c, d) for c in range(3) for d in range(3) if c != d):
        raise ValueError("wrong parameter order")
    if certificate["entry_weights"] != ["r_cd", "-1/r_cd"]:
        raise ValueError("wrong Laurent entry convention")
    rows = polynomials()
    identifiers = {key: i + 1 for i, key in enumerate(VARIABLES)}
    results = []
    for family in certificate["families"]:
        live = {}
        for p, ((c, d), positions) in enumerate(zip(pairs, family["supports"], strict=True)):
            if len(positions) != 2 or positions[0] == positions[1]:
                raise ValueError("two distinct support entries required")
            for sign, (i, j) in zip((1, -1), positions, strict=True):
                live[identifiers[c, d, i, j]] = (sign, p)
        errors = {}
        selected = 0
        for word in itertools.product(range(3), repeat=8):
            residual = Counter()
            for monomial, coefficient in rows.get(word, {}).items():
                exponent = [0] * 6
                for variable in monomial:
                    if variable not in live:
                        coefficient = 0
                        break
                    sign, p = live[variable]
                    coefficient *= sign
                    exponent[p] += sign
                residual[tuple(exponent)] += coefficient
            residual = {e: v for e, v in residual.items() if v}
            shore = len(set(word[:4])) == 1 or len(set(word[4:])) == 1
            subsystem = family["subsystem"]
            if subsystem not in ("monochromatic_shores", "binary_and_monochromatic_shores",
                                 "component_constant_and_independent_minority"):
                raise ValueError("unknown subsystem")
            if subsystem == "component_constant_and_independent_minority":
                selected_word = (
                    (len(set(word[:4])) == 1 and len(set(word[4:])) == 1)
                    or any(all(word[u] == c or word[u ^ (c + 1)] == c
                               for u in range(8)) for c in range(3))
                )
            else:
                selected_word = shore or (subsystem.startswith("binary_") and len(set(word)) <= 2)
            if selected_word:
                selected += 1
                if residual:
                    raise ValueError(f"subsystem failure {family['name']} {word}: {residual}")
            if residual:
                if len(residual) != 1:
                    raise ValueError("full residual is not a single Laurent monomial")
                errors["".join(map(str, word))] = residual
        if selected != family["subsystem_word_count"] or len(errors) != family["full_error_count"]:
            raise ValueError("enumeration count mismatch")
        shown = family["displayed_error"]
        if errors.get(shown["word"]) != {tuple(shown["exponent"]): shown["coefficient"]}:
            raise ValueError("displayed full-target failure mismatch")
        results.append({
            "family": family["name"],
            "exact_subsystem_words": selected,
            "nonzero_monomial_full_errors": len(errors),
            "displayed_error": shown,
        })
    return {"status": "EXACT_LAURENT_SUBSYSTEM_CONTROLS_PASS", "families": results,
            "scope": "proper subsystem countermodels; no full GHZ source"}


if __name__ == "__main__":
    print(json.dumps(replay(json.loads(FIXTURE.read_text(encoding="utf-8"))), indent=2))
