"""Independent exact replay of the finite k=5 forward-only control.

This checker reconstructs the protected involutions by local XOR masks and
derives every resource assignment from the literal permutations.  It does
not import the primary verifier or its helpers.
"""

from itertools import product

K, N, NR = 5, 20, 10
P = (13, 15, 19, 17, 18, 16, 11, 9, 3, 1, 5, 7, 10, 8, 2, 0, 14, 12, 6, 4)
Q = (12, 15, 6, 5, 1, 2, 11, 8, 3, 0, 14, 13, 18, 17, 19, 16, 9, 10, 7, 4)
SUCCESSOR_ORDER = (0, 1, 2, 3, 6, 5, 4, 8, 9, 7)
EXPECTED_LENGTHS = (16, 14, 13, 15, 18, 13, 11, 11, 11, 18)
EXPECTED_OTHER = (
    {2, 3, 5, 7, 9},
    {0, 3, 4, 7},
    {0, 1, 6},
    {1, 2, 5, 8, 9},
    {1, 2, 3, 5, 6, 8, 9},
    {1, 6, 9},
    {0, 3},
    {3, 9},
    {0, 4},
    {0, 1, 2, 4, 6, 7, 8},
)


def mate(color, u):
    return 4 * (u // 4) + ((u % 4) ^ {"A": 1, "B": 2, "C": 3}[color])


def resources(color):
    unseen = set(range(N))
    out = []
    while unseen:
        u = min(unseen)
        v = mate(color, u)
        out.append((u, v))
        unseen.remove(u)
        unseen.remove(v)
    return tuple(out)


RES = {c: resources(c) for c in "ABC"}
LOOKUP = {c: {frozenset(e): i for i, e in enumerate(RES[c])} for c in "ABC"}


def assert_permutation(f):
    assert len(f) == N and set(f) == set(range(N))


def orbit_partition(f):
    """Canonical directed cycles of a functional graph, via fresh orbit traces."""
    assigned = set()
    answer = []
    for seed in range(N):
        if seed in assigned:
            continue
        trace = []
        first = {}
        u = seed
        while u not in first and u not in assigned:
            first[u] = len(trace)
            trace.append(u)
            u = f[u]
        if u in first:
            cyc = trace[first[u] :]
            pivot = min(range(len(cyc)), key=cyc.__getitem__)
            answer.append(tuple(cyc[pivot:] + cyc[:pivot]))
        assigned.update(trace)
    return tuple(sorted(answer))


def is_hamilton(f):
    return len(orbit_partition(f)) == 1 and len(orbit_partition(f)[0]) == N


def induced_assignment(f, source, target):
    return tuple(LOOKUP[target][frozenset((f[u], f[v]))] for u, v in RES[source])


def switched(base, alternate, resource_index):
    f = list(base)
    for u in RES["A"][resource_index]:
        f[u] = alternate[u]
    return tuple(f)


def full_A_resources(nodes):
    S = set(nodes)
    return {j for j, e in enumerate(RES["A"]) if set(e) <= S}


def build_all_D(fab, fac, successor, bits):
    tau = [None] * N
    for p in range(NR):
        j = successor[p]
        b0, b1 = RES["B"][fab[p]]
        c0, c1 = RES["C"][fac[j]]
        if bits[p]:
            c0, c1 = c1, c0
        tau[b0], tau[b1] = c0, c1
    assert_permutation(tuple(tau))
    # D_BC = tau_BC o m_B.
    tbc = tuple(tau)
    tab = tuple(P[mate("A", u)] for u in range(N))
    tac = tuple(Q[mate("A", u)] for u in range(N))
    def inv(f):
        return tuple(f.index(u) for u in range(N))
    taus = {
        ("A", "B"): tab,
        ("B", "A"): inv(tab),
        ("A", "C"): tac,
        ("C", "A"): inv(tac),
        ("B", "C"): tbc,
        ("C", "B"): inv(tbc),
    }
    D = {(x, y): tuple(t[mate(x, u)] for u in range(N)) for (x, y), t in taus.items()}
    return D, taus


def boundary_holds_for_A(p, q, predecessor):
    for j in range(NR):
        cycles = orbit_partition(switched(p, q, j))
        required = set(RES["A"][j] + RES["A"][predecessor[j]])
        if not cycles or any(not required <= set(cyc) for cyc in cycles):
            return False
    return True


def base_forward_holds(base, D, resource_cycle):
    base_labels = [x for x in resource_cycle if x[0] == base]
    for i, current in enumerate(base_labels):
        pred = base_labels[(i - 1) % NR]
        pos = resource_cycle.index(current)
        forward = resource_cycle[(pos + 1) % len(resource_cycle)][0]
        backward = resource_cycle[(pos - 1) % len(resource_cycle)][0]
        f = list(D[(base, forward)])
        for u in RES[base][current[1]]:
            f[u] = D[(base, backward)][u]
        required = set(RES[base][current[1]] + RES[base][pred[1]])
        cycles = orbit_partition(tuple(f))
        if not cycles or any(not required <= set(cyc) for cyc in cycles):
            return False
    return True


def first_multiswitch_failure(p, q, predecessor):
    for labels in product((0, 1), repeat=NR):
        if len(set(labels)) == 1:
            continue
        f = [None] * N
        for j, edge in enumerate(RES["A"]):
            source = q if labels[j] else p
            for u in edge:
                f[u] = source[u]
        transitions = [
            j for j in range(NR) if labels[predecessor[j]] == 0 and labels[j] == 1
        ]
        for cyc in orbit_partition(tuple(f)):
            S = set(cyc)
            if not any(
                set(RES["A"][j] + RES["A"][predecessor[j]]) <= S for j in transitions
            ):
                return labels, cyc, tuple(transitions)
    return None


def perfect_matching_count(word, taus):
    """Count literal perfect matchings on the selected physical-color states."""
    adjacency = [set() for _ in range(N)]
    letters = "ABC"
    for u in range(N):
        cu = letters[word[u]]
        v = mate(cu, u)
        if word[v] == word[u]:
            adjacency[u].add(v)
            adjacency[v].add(u)
        for cv in letters:
            if cv == cu:
                continue
            v = taus[(cu, cv)][u]
            if word[v] == letters.index(cv):
                adjacency[u].add(v)
                adjacency[v].add(u)

    memo = {}

    def count(mask):
        if not mask:
            return 1
        if mask in memo:
            return memo[mask]
        u = (mask & -mask).bit_length() - 1
        total = 0
        for v in adjacency[u]:
            if mask & (1 << v):
                total += count(mask & ~(1 << u) & ~(1 << v))
        memo[mask] = total
        return total

    return count((1 << N) - 1)


def check_abstract_no_klein_control():
    """Independent six-vertex replay showing cyclic orders alone are weaker."""

    def cycle_map(order):
        return {order[i]: order[(i + 1) % len(order)] for i in range(len(order))}

    def small_cycles(f):
        unseen = set(f)
        ans = []
        while unseen:
            seed = min(unseen)
            path = []
            at = {}
            u = seed
            while u not in at and u in unseen:
                at[u] = len(path)
                path.append(u)
                u = f[u]
            if u in at:
                ans.append(tuple(path[at[u] :]))
            unseen.difference_update(path)
        return ans

    def inverse(f):
        return {v: u for u, v in f.items()}

    def compose(f, g):
        return {u: f[g[u]] for u in g}

    m = {0: 1, 1: 0, 2: 3, 3: 2, 4: 5, 5: 4}
    p = cycle_map((0, 1, 2, 3, 4, 5))
    q = cycle_map((0, 1, 4, 5, 2, 3))
    for base, alt in ((p, q), (q, p)):
        for u, v in ((0, 1), (2, 3), (4, 5)):
            f = dict(base)
            f[u], f[v] = alt[u], alt[v]
            assert any({u, v} <= set(cyc) for cyc in small_cycles(f))
    b = compose(compose(p, m), inverse(p))
    c = compose(compose(q, m), inverse(q))
    assert compose(b, c) != compose(c, b)


def main():
    check_abstract_no_klein_control()
    assert_permutation(P)
    assert_permutation(Q)
    assert is_hamilton(P) and is_hamilton(Q)

    # Independently check the conjugation equations and hollowness.
    for u in range(N):
        assert P[mate("A", u)] == mate("B", P[u])
        assert Q[mate("A", u)] == mate("C", Q[u])
        assert P[u] // 4 != u // 4 and Q[u] // 4 != u // 4

    fab = induced_assignment(P, "A", "B")
    fac = induced_assignment(Q, "A", "C")
    assert fab == (7, 9, 8, 5, 1, 3, 4, 0, 6, 2)
    assert fac == (6, 3, 1, 4, 0, 7, 9, 8, 5, 2)

    # Literal forward switches, without relying on cyclic-order inequalities.
    for j in range(NR):
        cycles = orbit_partition(switched(P, Q, j))
        assert len(cycles) == 1
        assert len(cycles[0]) == EXPECTED_LENGTHS[j]
        assert set(RES["A"][j]) <= set(cycles[0])
        assert full_A_resources(cycles[0]) - {j} == EXPECTED_OTHER[j]

    successor = {SUCCESSOR_ORDER[i]: SUCCESSOR_ORDER[(i + 1) % NR] for i in range(NR)}
    predecessor = {v: u for u, v in successor.items()}
    assert all(predecessor[j] in EXPECTED_OTHER[j] for j in range(NR))

    # The 30 resource vertices A_p-B_fab[p]-C_fac[succ(p)] form one cycle,
    # and each edge is hollow at physical-component level.
    resource_cycle = []
    for p in SUCCESSOR_ORDER:
        j = successor[p]
        resource_cycle.extend((("A", p), ("B", fab[p]), ("C", fac[j])))
    assert len(resource_cycle) == len(set(resource_cycle)) == 30
    for x, y in zip(resource_cycle, resource_cycle[1:] + resource_cycle[:1]):
        assert x[1] // 2 != y[1] // 2

    hamilton_bits = []
    for bits in product((0, 1), repeat=NR):
        D, taus = build_all_D(fab, fac, successor, bits)
        assert all(taus[("B", "C")][u] // 4 != u // 4 for u in range(N))
        if is_hamilton(D[("B", "C")]):
            hamilton_bits.append(bits)
            assert boundary_holds_for_A(P, Q, predecessor)
            assert base_forward_holds("A", D, resource_cycle)
            assert not base_forward_holds("B", D, resource_cycle)
            assert not base_forward_holds("C", D, resource_cycle)
    assert len(hamilton_bits) == 160
    assert (0,) * NR in hamilton_bits

    # Direct support-level validation of the explicit mixed physical word on
    # the canonical all-straight B--C orientation.  This bypasses the switched
    # cycle coefficient formula: the selected 20-state graph itself has one
    # perfect matching, whose monomial is nonzero because every support entry
    # in the control is nonzero.
    _, straight_taus = build_all_D(fab, fac, successor, (0,) * NR)
    explicit_word = tuple(map(int, "01002002010000112012"))
    assert len(explicit_word) == N and set(explicit_word) == {0, 1, 2}
    assert perfect_matching_count(explicit_word, straight_taus) == 1

    # Reverse direction already fails at the root condition: exactly roots
    # 0 and 9 have a cycle containing both root endpoints.
    reverse_good = []
    for j in range(NR):
        cycles = orbit_partition(switched(Q, P, j))
        if any(set(RES["A"][j]) <= set(cyc) for cyc in cycles):
            reverse_good.append(j)
    assert reverse_good == [0, 9]

    # Literal reverse failure at root 1 gives a mixed physical word: outside
    # the selected directed cycle use base A=0; cycle targets reached from the
    # exceptional root receive B=1 and all other cycle targets receive C=2.
    reverse_cycles = orbit_partition(switched(Q, P, 1))
    assert reverse_cycles == ((0, 12, 18, 7, 8, 3, 17, 10, 14, 19, 4, 1, 15, 16, 9),)
    reverse_word = [0] * N
    root_nodes = set(RES["A"][1])
    reverse_map = switched(Q, P, 1)
    for source in reverse_cycles[0]:
        reverse_word[reverse_map[source]] = 1 if source in root_nodes else 2
    assert tuple(reverse_word) == (
        2,
        2,
        0,
        2,
        2,
        0,
        0,
        2,
        2,
        2,
        2,
        0,
        2,
        0,
        2,
        2,
        2,
        1,
        2,
        2,
    )
    assert set(reverse_word) == {0, 1, 2}

    failure = first_multiswitch_failure(P, Q, predecessor)
    assert failure is not None
    print(
        {
            "FAB": fab,
            "FAC": fac,
            "forward_cycle_lengths": EXPECTED_LENGTHS,
            "predecessor_cycle": SUCCESSOR_ORDER,
            "Hamilton_BC_orientations": len(hamilton_bits),
            "explicit_word_matching_count": 1,
            "reverse_root_successes": tuple(reverse_good),
            "reverse_mixed_word": tuple(reverse_word),
            "first_multiswitch_failure": failure,
        }
    )


if __name__ == "__main__":
    main()
