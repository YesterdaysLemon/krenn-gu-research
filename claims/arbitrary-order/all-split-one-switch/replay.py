"""Exact replay for the k=5 all-split forward-one-switch obstruction.

Standard-library only.  This proves the displayed finite mechanism control;
it is not an all-order source verifier or a Krenn--Gu resolution.
"""

from itertools import product

K = 5
N = 20
R = 10
LOCAL = {"A": ((0, 1), (2, 3)), "B": ((0, 2), (1, 3)), "C": ((0, 3), (1, 2))}
LETTERS = "ABC"
P = {
    0: 13,
    1: 15,
    2: 19,
    3: 17,
    4: 18,
    5: 16,
    6: 11,
    7: 9,
    8: 3,
    9: 1,
    10: 5,
    11: 7,
    12: 10,
    13: 8,
    14: 2,
    15: 0,
    16: 14,
    17: 12,
    18: 6,
    19: 4,
}
Q = {
    0: 12,
    1: 15,
    2: 6,
    3: 5,
    4: 1,
    5: 2,
    6: 11,
    7: 8,
    8: 3,
    9: 0,
    10: 14,
    11: 13,
    12: 18,
    13: 17,
    14: 19,
    15: 16,
    16: 9,
    17: 10,
    18: 7,
    19: 4,
}
FAB = (7, 9, 8, 5, 1, 3, 4, 0, 6, 2)
FAC = (6, 3, 1, 4, 0, 7, 9, 8, 5, 2)
A_CYCLE = (0, 1, 2, 3, 6, 5, 4, 8, 9, 7)


def resources(x):
    return tuple((4 * c + u, 4 * c + v) for c in range(K) for u, v in LOCAL[x])


RES = {x: resources(x) for x in LETTERS}


def mate(x, u):
    c, z = divmod(u, 4)
    for a, b in LOCAL[x]:
        if z == a:
            return 4 * c + b
        if z == b:
            return 4 * c + a
    raise AssertionError


def cycles(out):
    done = set()
    ans = []
    for s in sorted(out):
        if s in done:
            continue
        at = {}
        path = []
        u = s
        while u not in done and u not in at:
            at[u] = len(path)
            path.append(u)
            u = out[u]
        if u in at:
            ans.append(tuple(path[at[u] :]))
        done.update(path)
    return ans


def hamilton(out):
    return len(cycles(out)) == 1 and len(cycles(out)[0]) == N


def assignment(out, source, target):
    lookup = {frozenset(x): i for i, x in enumerate(target)}
    return tuple(lookup[frozenset((out[u], out[v]))] for u, v in source)


def build(bits):
    succ = {A_CYCLE[i]: A_CYCLE[(i + 1) % R] for i in range(R)}
    tau = {}
    # tau_AB=P m_A and tau_AC=Q m_A.
    tab = {u: P[mate("A", u)] for u in range(N)}
    tac = {u: Q[mate("A", u)] for u in range(N)}
    tau[("A", "B")] = tab
    tau[("B", "A")] = {v: u for u, v in tab.items()}
    tau[("A", "C")] = tac
    tau[("C", "A")] = {v: u for u, v in tac.items()}
    tbc = {}
    for p in range(R):
        j = succ[p]
        x, y = RES["B"][FAB[p]]
        z, w = RES["C"][FAC[j]]
        if bits[p]:
            z, w = w, z
        tbc[x] = z
        tbc[y] = w
    tau[("B", "C")] = tbc
    tau[("C", "B")] = {v: u for u, v in tbc.items()}
    D = {
        (a, b): {u: tau[(a, b)][mate(a, u)] for u in range(N)}
        for a in LETTERS
        for b in LETTERS
        if a != b
    }
    return tau, D


def f_cycle():
    out = []
    for p in A_CYCLE:
        j = A_CYCLE[(A_CYCLE.index(p) + 1) % R]
        out.extend((("A", p), ("B", FAB[p]), ("C", FAC[j])))
    assert len(set(out)) == 3 * R
    return tuple(out)


FC = f_cycle()


def one_switch_all(base, D):
    base_positions = [i for i, x in enumerate(FC) if x[0] == base]
    base_labels = [FC[i] for i in base_positions]
    receipts = []
    for idx, current in enumerate(base_labels):
        pred = base_labels[(idx - 1) % R]
        pos = FC.index(current)
        forward = FC[(pos + 1) % len(FC)][0]
        backward = FC[(pos - 1) % len(FC)][0]
        out = dict(D[(base, forward)])
        for u in RES[base][current[1]]:
            out[u] = D[(base, backward)][u]
        cs = cycles(out)
        required = set(RES[base][current[1]] + RES[base][pred[1]])
        if not all(required <= set(c) for c in cs):
            return False, (
                current,
                pred,
                forward,
                backward,
                cs,
                tuple(sorted(required)),
            )
        receipts.append((current, pred, tuple(map(len, cs))))
    return True, receipts


def switched_root_rows(X, Y):
    rows = []
    for j, (u, v) in enumerate(RES["A"]):
        out = dict(X)
        out[u] = Y[u]
        out[v] = Y[v]
        cs = cycles(out)
        rows.append(
            (j, len(cs), any({u, v} <= set(c) for c in cs), tuple(map(len, cs)))
        )
    return tuple(rows)


def compose(left, right):
    return {u: left[right[u]] for u in right}


def inverse(out):
    return {v: u for u, v in out.items()}


def conjugate(out, matching):
    return compose(compose(out, matching), inverse(out))


def abstract_no_klein_control():
    matching = {0: 1, 1: 0, 2: 3, 3: 2, 4: 5, 5: 4}

    def cycle_map(order):
        return {order[i]: order[(i + 1) % len(order)] for i in range(len(order))}

    x = cycle_map((0, 1, 2, 3, 4, 5))
    y = cycle_map((0, 1, 4, 5, 2, 3))
    for first, second in ((x, y), (y, x)):
        for u in (0, 2, 4):
            v = matching[u]
            out = dict(first)
            out[u] = second[u]
            out[v] = second[v]
            assert any({u, v} <= set(c) for c in cycles(out))
    b = conjugate(x, matching)
    c = conjugate(y, matching)
    assert compose(b, c) != compose(c, b)


def first_A_boundary_failure():
    pred = {A_CYCLE[(i + 1) % R]: A_CYCLE[i] for i in range(R)}
    for labels in product((0, 1), repeat=R):
        if len(set(labels)) == 1:
            continue
        out = {}
        for j, (u, v) in enumerate(RES["A"]):
            source = P if labels[j] == 0 else Q
            out[u] = source[u]
            out[v] = source[v]
        transitions = [j for j in range(R) if labels[pred[j]] == 0 and labels[j] == 1]
        for c in cycles(out):
            S = set(c)
            if not any(set(RES["A"][j] + RES["A"][pred[j]]) <= S for j in transitions):
                return labels, c, tuple(transitions)
    return None


def cycle_physical_word(labels, cycle):
    resource_of = {u: j for j, pair in enumerate(RES["A"]) for u in pair}
    out = {}
    for j, (u, v) in enumerate(RES["A"]):
        source = P if labels[j] == 0 else Q
        out[u] = source[u]
        out[v] = source[v]
    word = [0] * N
    for source in cycle:
        word[out[source]] = 1 if labels[resource_of[source]] == 0 else 2
    return tuple(word)


def reverse_mixed_witness():
    root = 1
    u, v = RES["A"][root]
    out = dict(Q)
    out[u] = P[u]
    out[v] = P[v]
    cs = cycles(out)
    assert cs == [(0, 12, 18, 7, 8, 3, 17, 10, 14, 19, 4, 1, 15, 16, 9)]
    word = [0] * N
    for source in cs[0]:
        word[out[source]] = 1 if source in (u, v) else 2
    return root, cs[0], tuple(word)


def main():
    abstract_no_klein_control()
    assert assignment(P, RES["A"], RES["B"]) == FAB
    assert assignment(Q, RES["A"], RES["C"]) == FAC
    assert hamilton(P) and hamilton(Q)
    assert all(i // 2 != FAB[i] // 2 and i // 2 != FAC[i] // 2 for i in range(R))
    assert len(set(FC)) == 3 * R
    assert all(
        RES[FC[i][0]][FC[i][1]][0] // 4
        != RES[FC[(i + 1) % len(FC)][0]][FC[(i + 1) % len(FC)][1]][0] // 4
        for i in range(len(FC))
    )
    forward_rows = switched_root_rows(P, Q)
    reverse_rows = switched_root_rows(Q, P)
    assert tuple(row[3] for row in forward_rows) == tuple(
        (x,) for x in (16, 14, 13, 15, 18, 13, 11, 11, 11, 18)
    )
    assert all(row[2] for row in forward_rows)
    assert tuple(row[0] for row in reverse_rows if row[2]) == (0, 9)
    mixed_failure = first_A_boundary_failure()
    assert mixed_failure == (
        (0, 0, 0, 0, 0, 0, 0, 1, 0, 1),
        (16, 14, 19, 4, 18, 7, 9, 1, 15),
        (9,),
    )
    mixed_word = cycle_physical_word(mixed_failure[0], mixed_failure[1])
    assert mixed_word == (
        0,
        1,
        0,
        0,
        2,
        0,
        0,
        2,
        0,
        1,
        0,
        0,
        0,
        0,
        1,
        1,
        2,
        0,
        1,
        2,
    )
    reverse_witness = reverse_mixed_witness()
    assert reverse_witness == (
        1,
        (0, 12, 18, 7, 8, 3, 17, 10, 14, 19, 4, 1, 15, 16, 9),
        (2, 2, 0, 2, 2, 0, 0, 2, 2, 2, 2, 0, 2, 0, 2, 2, 2, 1, 2, 2),
    )
    hbc = 0
    all_bases = []
    base_counts = {a: 0 for a in LETTERS}
    pair_counts = {}
    for bits in product((0, 1), repeat=R):
        tau, D = build(bits)
        if not hamilton(D[("B", "C")]):
            continue
        assert all(hamilton(D[(a, b)]) for a in LETTERS for b in LETTERS if a != b)
        hbc += 1
        results = {a: one_switch_all(a, D) for a in LETTERS}
        assert results["A"][0]
        good = tuple(a for a in LETTERS if results[a][0])
        for a in good:
            base_counts[a] += 1
        pair_counts[good] = pair_counts.get(good, 0) + 1
        if all(x[0] for x in results.values()):
            all_bases.append((bits, D, results))
            break
    assert hbc == 160
    assert base_counts == {"A": 160, "B": 0, "C": 0}
    assert pair_counts == {("A",): 160}
    assert not all_bases
    print(
        {
            "resource_cycle": FC,
            "A_forward_root_rows": forward_rows,
            "A_reverse_root_rows": reverse_rows,
            "first_A_full_boundary_failure": mixed_failure,
            "first_A_failure_physical_word": mixed_word,
            "reverse_mixed_witness": reverse_witness,
            "Hamilton_BC_orientations": hbc,
            "base_counts": base_counts,
            "good_base_profiles": pair_counts,
            "all_bases_control": all_bases[:1],
        }
    )


if __name__ == "__main__":
    main()
