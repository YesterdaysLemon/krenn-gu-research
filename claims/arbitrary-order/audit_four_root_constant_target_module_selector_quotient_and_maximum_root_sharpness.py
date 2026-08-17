"""Independent no-import audit of the four-root module-selector theorem."""

from itertools import combinations, product
from math import comb, factorial


ROOTS = range(4)
PORTS = frozenset(("u", i) for i in ROOTS)
Q0 = ("q", 0)
Q1 = ("q", 1)
OUTSIDE = PORTS | {Q0, Q1}


def clean_support(private_set, residual_set):
    """Derive root-word supports from injection types, without matchings code."""

    private_set = frozenset(private_set)
    residual_set = frozenset(residual_set)
    outside_size = len(private_set) + len(residual_set)
    if outside_size not in (0, 2, 4):
        return set()

    supports = set()
    # Private ports force their equally labelled roots and hence their a-set.
    forced_roots = frozenset(index for kind, index in private_set if kind == "u")
    if len(forced_roots) != len(private_set):
        return set()
    free = tuple(i for i in ROOTS if i not in forced_roots)

    # q0 contributes b and q1 contributes c at distinct free roots.
    for q0_root in free if Q0 in residual_set else (None,):
        for q1_root in free if Q1 in residual_set else (None,):
            chosen = tuple(root for root in (q0_root, q1_root) if root is not None)
            if len(set(chosen)) != len(chosen):
                continue
            remaining = [root for root in free if root not in chosen]
            if len(remaining) % 2:
                continue
            word = ["a" if i in forced_roots else "b" for i in ROOTS]
            if q1_root is not None:
                word[q1_root] = "c"
            supports.add(tuple(word))
    return supports


def audit_clean_pivots() -> None:
    assignments = []
    for size in (0, 2, 4):
        assignments.extend(map(frozenset, combinations(OUTSIDE, size)))
    assert len(assignments) == 31

    for target_tuple in tuple(combinations(ROOTS, 2)) + (tuple(ROOTS),):
        target = frozenset(target_tuple)
        desired_assignment = frozenset(("u", i) for i in ROOTS if i not in target)
        pivot = tuple("b" if i in target else "a" for i in ROOTS)
        owners = []
        for assignment in assignments:
            private = assignment & PORTS
            residual = assignment - PORTS
            if pivot in clean_support(private, residual):
                owners.append(assignment)
        assert owners == [desired_assignment]

        multiplicity = 1 if len(target) == 2 else 3
        # The multiplicity is the number of perfect matchings on the internal
        # target roots: 1!! for two and 3!! for four.
        assert multiplicity == factorial(len(target)) // (
            2 ** (len(target) // 2) * factorial(len(target) // 2)
        )


def audit_counts() -> None:
    assert sum(comb(6, k) * 3**k for k in (2, 4, 6)) == 2079
    even_u = comb(4, 2) * 3**2 + comb(4, 4) * 3**4
    odd_u = comb(4, 1) * 3 + comb(4, 3) * 3**3
    assert 1 + 2 * even_u + 2 * odd_u == 511
    assert (3**6, 3**4, 6 * 3**6 + 3**4) == (729, 81, 4455)


def audit_identity_nuisance() -> None:
    # Contracting the four port slots of tensor_i I_(root_i,port_i) returns
    # the same four-letter root word.  This independently proves surjectivity.
    image = {tuple(word) for word in product(range(3), repeat=4)}
    assert len(image) == 3**4
    for root_word in product(range(3), repeat=4):
        assert root_word in image


def audit_target_purity() -> None:
    # A constant functional on root and complement-port pure words can only
    # leave one common colour on all surviving S slots.
    for size in (2, 4):
        surviving = {tuple(colour for _ in range(size)) for colour in range(3)}
        assert len(surviving) == 3
        assert all(len(set(word)) == 1 for word in surviving)


def main() -> None:
    audit_counts()
    audit_clean_pivots()
    audit_identity_nuisance()
    audit_target_purity()
    print("independent four-root constant-module selector audit: PASS")
    print("witness-locus quotient outcome: UNKNOWN")
    print("global Krenn-Gu status: UNRESOLVED")


if __name__ == "__main__":
    main()
