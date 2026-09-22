#!/usr/bin/env python3
"""Finite port replay for the same-component C8+split q1 obstruction.

The proof is the matching-sector argument in RESULT.md.  This checker only
replays the F_2^2 port identities for every affine lift/orientation; it is not
the proof of the all-order statement.
"""

from itertools import permutations


A, B, C = 1, 2, 3
V = range(4)


def edges(vector):
    return {frozenset((u, u ^ vector)) for u in V}


MATCHING = {d: edges(d) for d in (A, B, C)}


def matching_action(port_map, vector):
    image = {
        frozenset((port_map[u], port_map[v]))
        for u, v in (tuple(edge) for edge in MATCHING[vector])
    }
    return next(d for d in (A, B, C) if image == MATCHING[d])


def main():
    lifts = []
    cases = 0
    for pi in permutations(V):
        action = tuple(matching_action(pi, d) for d in (A, B, C))
        if action != (B, C, A):
            continue
        lifts.append(pi)
        sigma = tuple(pi[u ^ B] for u in V)

        # The C8 and split use opposite endpoints of the same target M_c
        # resource on every source M_b edge.
        assert all(pi[u] != sigma[u] for u in V)
        assert matching_action(sigma, B) == C

        for u in V:
            v = u ^ A
            x = pi[u]
            y = sigma[v]

            # The direct mixed q1 targets form one M_a edge.
            assert x ^ y == A

            # If y takes its alternative c--a lane, it returns to the
            # M_b-mate of v, in the complementary source M_a edge.
            source_of_y = pi.index(y)
            assert source_of_y == (v ^ B)
            assert source_of_y not in (u, v)
            stranded = source_of_y ^ A
            assert stranded not in (u, v, source_of_y)
            cases += 1

    assert len(lifts) == 4
    assert cases == 16
    print("affine_lifts=4 oriented_Ma_cases=16")
    print("direct_targets_Ma=PASS alternative_strands_source_port=PASS")
    print("SAME_COMPONENT_C8_REPAIR_Q1_PORT_REPLAY_PASS")


if __name__ == "__main__":
    main()
