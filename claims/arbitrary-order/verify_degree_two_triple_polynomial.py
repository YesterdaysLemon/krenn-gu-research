"""Enumerate the six-state prism/K3,3 local matching polynomials."""

from itertools import combinations

PROTECTED = ((0, 1, "pA"), (2, 3, "pB"), (4, 5, "pC"))
AB = ((0, 2, "ab0"), (1, 3, "ab1"))
AC = ((0, 4, "ac0"), (1, 5, "ac1"))
BC_DIAG = ((2, 4, "bc0"), (3, 5, "bc1"))
BC_ANTI = ((2, 5, "bc0"), (3, 4, "bc1"))


def perfect_matching_monomials(edges, vertices):
    vertices = set(vertices)
    out = []
    for chosen in combinations(edges, len(vertices) // 2):
        endpoints = [v for u, w, _ in chosen for v in (u, w)]
        if len(endpoints) == len(vertices) and set(endpoints) == vertices:
            out.append(tuple(sorted(name for _, _, name in chosen)))
    return tuple(sorted(out))


def closure_failures(edges):
    adjacency = {u: set() for u in range(6)}
    for u, v, _ in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    failures = 0
    for resource in ((0, 1), (2, 3), (4, 5)):
        u, v = resource
        for x in adjacency[u] - {v}:
            for y in adjacency[v] - {u}:
                if x != y and y not in adjacency[x]:
                    failures += 1
    return failures


def main():
    base = PROTECTED + AB + AC
    prism = base + BC_DIAG
    k33 = base + BC_ANTI
    prism_terms = perfect_matching_monomials(prism, range(6))
    k33_terms = perfect_matching_monomials(k33, range(6))
    assert prism_terms == (
        ("ab0", "ab1", "pC"),
        ("ac0", "ac1", "pB"),
        ("bc0", "bc1", "pA"),
        ("pA", "pB", "pC"),
    )
    assert len(k33_terms) == 6
    crossing_only = [term for term in k33_terms if not any(x.startswith("p") for x in term)]
    assert len(crossing_only) == 2
    assert closure_failures(prism) > 0
    assert closure_failures(k33) == 0
    print("DEGREE2_TRIPLE_LOCAL_PASS")
    print("prism_terms", prism_terms)
    print("k33_terms", k33_terms)
    print("closure_failures", closure_failures(prism), closure_failures(k33))


if __name__ == "__main__":
    main()
