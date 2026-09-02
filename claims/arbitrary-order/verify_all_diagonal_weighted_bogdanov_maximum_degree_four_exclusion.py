"""Primary verifier for the all-diagonal weighted-Bogdanov degree-four exclusion.

Exact rational checks of the lemmas used by the written proof:
  (F)  all-diagonal factorization T_W(a) = prod_c haf(Z^c[V_c(a)])  (n = 6);
  (NC) noncancellation for a perfect matching plus a partial matching (n = 6, 8);
  (OC) an odd colour-c component forces f_c(V) = 0 and zero cycle cofactors;
  (DG) degree bookkeeping: E-degree triples under Delta(D) <= 4;
  (BG) Bogdanov: every simple cubic graph formed by three pairwise disjoint
       perfect matchings of K_6 or K_8 has a non-monochromatic perfect matching.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import random
import sys
from fractions import Fraction
from pathlib import Path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def perfect_matchings(vertices):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    first, rest = vertices[0], vertices[1:]
    for k, partner in enumerate(rest):
        remaining = rest[:k] + rest[k + 1:]
        for matching in perfect_matchings(remaining):
            yield ((first, partner),) + matching


def haf(Z, vertices):
    """Hafnian of the principal submatrix on `vertices` by matching enumeration."""
    vertices = tuple(sorted(vertices))
    if len(vertices) % 2:
        return Fraction(0)
    total = Fraction(0)
    for matching in perfect_matchings(vertices):
        term = Fraction(1)
        for (i, j) in matching:
            term *= Z[i][j]
            if term == 0:
                break
        total += term
    return total


def zero_matrix(n):
    return [[Fraction(0)] * n for _ in range(n)]


def random_nonzero(rng):
    value = 0
    while value == 0:
        value = rng.randint(-5, 5)
    return Fraction(value, rng.randint(1, 4))


def check_factorization(rng, n=6, trials=3):
    """(F): full all-diagonal tensor equals the product of colour hafnians."""
    words_checked = 0
    for _ in range(trials):
        Z = [zero_matrix(n) for _ in range(3)]
        for c in range(3):
            for i in range(n):
                for j in range(i + 1, n):
                    if rng.random() < 0.6:
                        Z[c][i][j] = Z[c][j][i] = random_nonzero(rng)
        for word in itertools.product(range(3), repeat=n):
            direct = Fraction(0)
            for matching in perfect_matchings(range(n)):
                term = Fraction(1)
                for (i, j) in matching:
                    if word[i] != word[j]:
                        term = Fraction(0)
                        break
                    term *= Z[word[i]][i][j]
                    if term == 0:
                        break
                direct += term
            product = Fraction(1)
            for c in range(3):
                cls = [v for v in range(n) if word[v] == c]
                product *= haf(Z[c], cls) if cls else Fraction(1)
            if direct != product:
                raise AssertionError("factorization (F) failed")
            words_checked += 1
    return words_checked


def check_noncancellation(rng, n, trials):
    """(NC): perfect + partial matching, haf(V) != 0 => haf(A) != 0 on matched A."""
    verified = 0
    for _ in range(trials):
        verts = list(range(n))
        rng.shuffle(verts)
        P = [tuple(sorted((verts[2 * k], verts[2 * k + 1]))) for k in range(n // 2)]
        # random partial matching disjoint from P
        R = []
        pool = list(range(n))
        rng.shuffle(pool)
        while len(pool) >= 2:
            a, b = pool.pop(), pool.pop()
            e = tuple(sorted((a, b)))
            if e not in P and rng.random() < 0.7:
                R.append(e)
        Z = zero_matrix(n)
        for (i, j) in P + R:
            Z[i][j] = Z[j][i] = random_nonzero(rng)
        if haf(Z, range(n)) == 0:
            continue  # hypothesis fails (a cycle factor cancelled); not a test case
        support = set(P + R)
        for size in range(2, n + 1, 2):
            for A in itertools.combinations(range(n), size):
                sub = {e for e in support if e[0] in A and e[1] in A}
                has_pm = any(all(e in sub for e in m) for m in perfect_matchings(A))
                if has_pm and haf(Z, A) == 0:
                    raise AssertionError("noncancellation lemma failed")
        verified += 1
    if verified == 0:
        raise AssertionError("no noncancellation instance with nonzero total hafnian")
    return verified


def check_odd_component(rng, n=8, trials=5):
    """(OC): odd cycle component of supp(Z) => haf(V) = 0 and zero cycle cofactors."""
    for _ in range(trials):
        Z = zero_matrix(n)
        cycle = [0, 1, 2]  # triangle component
        for k in range(3):
            i, j = cycle[k], cycle[(k + 1) % 3]
            Z[i][j] = Z[j][i] = random_nonzero(rng)
        rest = list(range(3, n))
        for i in rest:
            for j in rest:
                if i < j and rng.random() < 0.7:
                    Z[i][j] = Z[j][i] = random_nonzero(rng)
        if haf(Z, range(n)) != 0:
            raise AssertionError("odd component did not kill haf(V)")
        for k in range(3):
            e = {cycle[k], cycle[(k + 1) % 3]}
            if haf(Z, [v for v in range(n) if v not in e]) != 0:
                raise AssertionError("odd component did not kill a cycle cofactor")
        # control: replace the triangle by a 4-cycle on {0,1,2,3}; total may be nonzero
    return trials


def check_degree_patterns():
    """(DG): E-degree triples with each >= 1 and sum <= 4."""
    patterns = sorted({
        tuple(sorted(t, reverse=True))
        for t in itertools.product(range(1, 5), repeat=3) if sum(t) <= 4
    })
    if patterns != [(1, 1, 1), (2, 1, 1)]:
        raise AssertionError(f"unexpected degree patterns {patterns}")
    return patterns


def check_bogdanov(n):
    """(BG): every union of three pairwise disjoint perfect matchings of K_n
    (n = 6, 8) has a perfect matching other than the three colour classes."""
    pms = [frozenset(m) for m in perfect_matchings(range(n))]
    triples = 0
    for a in range(len(pms)):
        for b in range(a + 1, len(pms)):
            if pms[a] & pms[b]:
                continue
            for c in range(b + 1, len(pms)):
                if (pms[a] | pms[b]) & pms[c]:
                    continue
                edges = pms[a] | pms[b] | pms[c]
                triples += 1
                extra = [m for m in pms if m <= edges and m not in (pms[a], pms[b], pms[c])]
                if not extra:
                    raise AssertionError(f"n={n}: a cubic three-matching graph has only monochromatic PMs")
    if triples == 0:
        raise AssertionError("no disjoint triples enumerated")
    return triples


def main() -> None:
    rng = random.Random(20260901)
    report = {}
    report["factorization_words_checked_n6"] = check_factorization(rng)
    report["noncancellation_instances_n6"] = check_noncancellation(rng, 6, 40)
    report["noncancellation_instances_n8"] = check_noncancellation(rng, 8, 8)
    report["odd_component_trials_n8"] = check_odd_component(rng)
    report["degree_patterns"] = check_degree_patterns()
    report["bogdanov_disjoint_triples_n6"] = check_bogdanov(6)
    report["bogdanov_disjoint_triples_n8"] = check_bogdanov(8)
    for key, value in report.items():
        print(f"{key}: {value}")
    out_dir = Path("tmp")
    out_dir.mkdir(exist_ok=True)
    out = out_dir / "all_diagonal_degree_four_verified.json"
    out.write_text(json.dumps({
        "verifier": Path(__file__).name,
        "verifier_sha256": sha256_file(Path(__file__)),
        "report": report,
        "verified": True,
    }, indent=2), encoding="utf-8")
    print(f"wrote {out}")
    print("VERIFIED: lemmas (F), (NC), (OC), (DG), (BG) hold on the checked ranges")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as error:
        print(f"FAILED: {error}")
        sys.exit(1)
