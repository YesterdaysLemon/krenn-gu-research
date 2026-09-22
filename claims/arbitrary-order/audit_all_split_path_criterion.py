"""Exhaust short canonical signed resource paths against the closed criterion."""

from __future__ import annotations

from functools import lru_cache
from itertools import product


FULL = 2


def z_value(length):
    z0, z1 = 1, 1
    if length == 0:
        return z0
    for _ in range(2, length + 1):
        z0, z1 = z1, z1 - z0
    return z1


def criterion(occupancy, twists):
    """Exact predicted coefficient; occupancy entries are rail 0, rail 1, or FULL."""
    singletons = [i for i, value in enumerate(occupancy) if value != FULL]
    if len(singletons) % 2:
        return 0
    if not singletons:
        return z_value(len(occupancy))

    value = 1
    # Full runs before singleton 0, between singleton pairs, and after the last.
    boundaries = [(-1, singletons[0])]
    for pair in range(1, len(singletons) - 1, 2):
        boundaries.append((singletons[pair], singletons[pair + 1]))
    boundaries.append((singletons[-1], len(occupancy)))
    for left, right in boundaries:
        run_length = right - left - 1
        value *= z_value(run_length)
        if value == 0:
            return 0

    # Consecutive singleton pairs are joined by one forced alternating chain.
    for pair in range(0, len(singletons), 2):
        start, finish = singletons[pair], singletons[pair + 1]
        rail = occupancy[start]
        for edge in range(start, finish):
            # Canonical edge has weight +1 from rail 0 and -1 from rail 1.
            value *= 1 if rail == 0 else -1
            arrived = rail ^ twists[edge]
            if edge + 1 == finish:
                if arrived != occupancy[finish]:
                    return 0
            else:
                # The arrived state is consumed; the other state of this full
                # resource is the unique state available for the next lane.
                rail = 1 - arrived
    return value


def direct_coefficient(occupancy, twists):
    selected = []
    for i, value in enumerate(occupancy):
        rails = (0, 1) if value == FULL else (value,)
        selected.extend((i, rail) for rail in rails)
    index = {state: j for j, state in enumerate(selected)}
    adjacency = [[] for _ in selected]

    def add(left, right, weight):
        if left not in index or right not in index:
            return
        u, v = index[left], index[right]
        adjacency[u].append((v, weight))
        adjacency[v].append((u, weight))

    for i, value in enumerate(occupancy):
        if value == FULL:
            add((i, 0), (i, 1), 1)
    for i, twist in enumerate(twists):
        add((i, 0), (i + 1, twist), 1)
        add((i, 1), (i + 1, 1 ^ twist), -1)

    @lru_cache(maxsize=None)
    def rec(mask):
        if mask == 0:
            return 1
        u = (mask & -mask).bit_length() - 1
        total = 0
        for v, weight in adjacency[u]:
            if mask & (1 << v):
                total += weight * rec(mask ^ (1 << u) ^ (1 << v))
        return total

    return rec((1 << len(selected)) - 1)


def main():
    checked = 0
    zeros = 0
    nonzeros = 0
    max_length = 8
    for length in range(1, max_length + 1):
        for twists in product((0, 1), repeat=max(0, length - 1)):
            for occupancy in product((0, 1, FULL), repeat=length):
                predicted = criterion(occupancy, twists)
                actual = direct_coefficient(occupancy, twists)
                assert actual == predicted, (length, twists, occupancy, actual, predicted)
                checked += 1
                if actual:
                    nonzeros += 1
                else:
                    zeros += 1

    print("maximum_path_length", max_length)
    print("twist_occupancy_patterns_checked", checked)
    print("zero_coefficients", zeros)
    print("nonzero_coefficients", nonzeros)
    print("RESOURCE_PATH_CRITERION_PASS")


if __name__ == "__main__":
    main()
