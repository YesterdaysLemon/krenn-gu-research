"""Independent audit of the GHZ closure / matching-polytope face theorem.

Differences from the primary verifier: perfect matchings are enumerated by a
bitmask dynamic programme instead of recursion; the truncation family is
rebuilt from an independent implementation; the potentials are recomputed
and compared against the face condition using an exact linear-programming
certificate check (every extra matching, integer arithmetic); and the full
3^n perfect-matching tensor is evaluated numerically with einsum for
n = 6, 8, 10 at eps = 1e-1, 1e-2, 1e-3 to confirm the limit behaviour.

The numerical part is a floating-point control; the exact part is the audit.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import sys
from functools import lru_cache
from pathlib import Path

import numpy as np


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def matchings_bitmask(n, edge_set):
    """Enumerate perfect matchings of the graph on 0..n-1 by bitmask DP."""
    edge_set = {tuple(sorted(e)) for e in edge_set}

    @lru_cache(maxsize=None)
    def rec(mask):
        if mask == (1 << n) - 1:
            return [()]
        first = (~mask & (mask + 1)).bit_length() - 1
        result = []
        for partner in range(first + 1, n):
            if mask >> partner & 1:
                continue
            if (first, partner) not in edge_set:
                continue
            for tail in rec(mask | 1 << first | 1 << partner):
                result.append(((first, partner),) + tail)
        return result

    return rec(0)


def build_family(max_n):
    """Independent reimplementation of the canonical truncation family."""
    colour = {
        (0, 1): 0, (2, 3): 0, (0, 2): 1, (1, 3): 1, (0, 3): 2, (1, 2): 2,
    }
    potential = {edge: 0 for edge in colour}
    n = 4
    yield n, dict(colour), dict(potential)
    while n + 2 <= max_n:
        v = n - 1
        t = {0: n - 1, 1: n, 2: n + 1}
        incident = {colour[e]: e for e in colour if v in e}
        partners = {c: (e[0] if e[1] == v else e[1]) for c, e in incident.items()}
        closed = {v, *partners.values()}
        rest_vertices = [u for u in range(n) if u not in closed]
        relabel = {u: i for i, u in enumerate(rest_vertices)}
        rest_edges = {
            (relabel[a], relabel[b]) for (a, b) in colour if a not in closed and b not in closed
        }
        inner = [
            sum(potential[tuple(sorted((rest_vertices[a], rest_vertices[b])))] for (a, b) in m)
            for m in matchings_bitmask(len(rest_vertices), rest_edges)
        ] if rest_vertices else [0]
        attach = sum(potential[e] for e in incident.values())
        needed = 1 - attach - min(inner)
        shift = max(1, (needed + 2) // 3) if inner else 1
        new_colour, new_potential = {}, {}
        for e, c in colour.items():
            if v not in e:
                new_colour[e] = c
                new_potential[e] = potential[e]
        for c, u in partners.items():
            e = tuple(sorted((u, t[c])))
            new_colour[e] = c
            new_potential[e] = potential[incident[c]] + shift
        for a, b in ((0, 1), (0, 2), (1, 2)):
            e = (t[a], t[b])
            new_colour[e] = 3 - a - b
            new_potential[e] = -shift
        colour, potential = new_colour, new_potential
        n += 2
        yield n, dict(colour), dict(potential)


def exact_face_check(n, colour, potential):
    matchings = matchings_bitmask(n, set(colour))
    classes = {
        c: frozenset(e for e in colour if colour[e] == c) for c in range(3)
    }
    class_set = set(classes.values())
    extra_values = []
    for m in matchings:
        fm = frozenset(m)
        value = sum(potential[e] for e in m)
        if fm in class_set:
            if value != 0:
                raise AssertionError(f"n={n}: colour class has nu={value}")
        else:
            extra_values.append(value)
    if any(v < 1 for v in extra_values):
        raise AssertionError(f"n={n}: face condition fails")
    for c, cls in classes.items():
        covered = sorted(x for e in cls for x in e)
        if covered != list(range(n)):
            raise AssertionError(f"n={n}: colour class {c} not a PM")
    return len(matchings), len(extra_values), (min(extra_values) if extra_values else None)


def numeric_tensor(n, colour, potential, eps):
    letters = "abcdefghijklmnop"
    W = {}
    for e, c in colour.items():
        block = np.zeros((3, 3))
        block[c, c] = eps ** potential[e]
        W[e] = block
    tensor = np.zeros((3,) * n)
    complete = {(i, j) for i in range(n) for j in range(i + 1, n)}
    for m in matchings_bitmask(n, complete):
        if not all(e in W for e in m):
            continue
        sub = ",".join(letters[i] + letters[j] for (i, j) in m)
        tensor += np.einsum(sub + "->" + letters[:n], *[W[e] for e in m])
    return tensor


def main() -> None:
    report = []
    for n, colour, potential in build_family(16):
        count, extras, min_extra = exact_face_check(n, colour, potential)
        row = {"n": n, "perfect_matchings": count, "extra_matchings": extras,
               "min_extra_potential": min_extra}
        if n in (6, 8, 10):
            controls = []
            for eps in (1e-1, 1e-2, 1e-3):
                tensor = numeric_tensor(n, colour, potential, eps)
                constants = [tensor[(c,) * n] for c in range(3)]
                mixed = tensor.copy()
                for c in range(3):
                    mixed[(c,) * n] = 0.0
                worst = float(np.abs(mixed).max())
                if max(abs(x - 1.0) for x in constants) > 1e-9:
                    raise AssertionError(f"n={n}: constant coefficient drifted")
                bound = extras * eps ** min_extra
                if worst > bound * (1 + 1e-9) or worst < eps ** min_extra * (1 - 1e-9):
                    raise AssertionError(f"n={n}: mixed coefficients off scale at eps={eps}")
                controls.append({"eps": eps, "max_mixed": worst})
            row["numeric_controls"] = controls
        report.append(row)
        print(json.dumps(row))
    if [r["n"] for r in report] != list(range(4, 17, 2)):
        raise AssertionError("audit family incomplete")
    out_dir = Path("tmp")
    out_dir.mkdir(exist_ok=True)
    out = out_dir / "ghz_closure_face_family_audit.json"
    out.write_text(json.dumps({
        "audit": Path(__file__).name,
        "audit_sha256": sha256_file(Path(__file__)),
        "rows": report,
        "verified": True,
    }, indent=2), encoding="utf-8")
    print(f"wrote {out}")
    print("AUDIT PASS: independent enumeration confirms face potentials and eps-scaling")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as error:
        print(f"AUDIT FAILED: {error}")
        sys.exit(1)
