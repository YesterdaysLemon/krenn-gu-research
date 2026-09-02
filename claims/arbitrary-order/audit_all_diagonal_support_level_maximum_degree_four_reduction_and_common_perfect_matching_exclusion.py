"""Independent abstract audit of the common-perfect-matching selector.

Unlike the primary graph enumerator, this script never constructs a graph or
counts graph matchings.  It enumerates the two disjoint cycle-block families
on m matching atoms and constructs the required transversal with a small
capacitated max-flow implementation.  The written Hall argument is the
all-order proof; this is a bounded, representation-independent audit.
"""

from __future__ import annotations

import hashlib
import json
from collections import deque
from pathlib import Path


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def block_families(m: int):
    """Every disjoint family of blocks of size at least two on range(m)."""
    seen = set()

    def rec(atom: int, partition: list[list[int]]):
        if atom == m:
            family = tuple(
                sorted(
                    (tuple(block) for block in partition if len(block) >= 2),
                    key=lambda block: block[0],
                )
            )
            if family not in seen:
                seen.add(family)
                yield tuple(frozenset(block) for block in family)
            return
        for i in range(len(partition)):
            partition[i].append(atom)
            yield from rec(atom + 1, partition)
            partition[i].pop()
        partition.append([atom])
        yield from rec(atom + 1, partition)
        partition.pop()

    yield from rec(0, [])


def add_arc(capacity, adjacency, u, v, cap):
    capacity[(u, v)] = capacity.get((u, v), 0) + cap
    capacity.setdefault((v, u), 0)
    adjacency.setdefault(u, set()).add(v)
    adjacency.setdefault(v, set()).add(u)


def capacitated_selector(m: int, forbidden_complete, required_hits):
    if not required_hits:
        return frozenset({0})

    source = ("source",)
    sink = ("sink",)
    capacity = {}
    adjacency = {}
    atom_group = {}
    for i, block in enumerate(forbidden_complete):
        for atom in block:
            atom_group[atom] = i

    choice_arcs = []
    for i, block in enumerate(required_hits):
        dnode = ("required", i)
        add_arc(capacity, adjacency, source, dnode, 1)
        for atom in block:
            anode = ("atom", atom)
            add_arc(capacity, adjacency, dnode, anode, 1)
            choice_arcs.append((dnode, anode, atom))

    for atom in range(m):
        anode = ("atom", atom)
        if atom in atom_group:
            cnode = ("forbidden", atom_group[atom])
            add_arc(capacity, adjacency, anode, cnode, 1)
        else:
            add_arc(capacity, adjacency, anode, sink, 1)
    for i, block in enumerate(forbidden_complete):
        add_arc(capacity, adjacency, ("forbidden", i), sink, len(block) - 1)

    residual = dict(capacity)
    flow = 0
    while True:
        parent = {source: None}
        queue = deque([source])
        while queue and sink not in parent:
            u = queue.popleft()
            for v in adjacency.get(u, ()):
                if v not in parent and residual.get((u, v), 0) > 0:
                    parent[v] = u
                    queue.append(v)
        if sink not in parent:
            break
        v = sink
        while parent[v] is not None:
            u = parent[v]
            residual[(u, v)] -= 1
            residual[(v, u)] = residual.get((v, u), 0) + 1
            v = u
        flow += 1

    if flow != len(required_hits):
        raise AssertionError("capacitated Hall selector failed")
    chosen = frozenset(
        atom for dnode, anode, atom in choice_arcs
        if capacity[(dnode, anode)] == 1 and residual[(dnode, anode)] == 0
    )
    return chosen


def main() -> None:
    records = []
    for m in range(3, 7):
        families = tuple(block_families(m))
        checked = 0
        atoms = frozenset(range(m))
        for forbidden in families:
            for required in families:
                chosen = capacitated_selector(m, forbidden, required)
                if not chosen or chosen == atoms:
                    raise AssertionError("selector must give two nonempty shores")
                if any(block <= chosen for block in forbidden):
                    raise AssertionError("selector contains a forbidden block")
                if any(not (block & chosen) for block in required):
                    raise AssertionError("selector misses a required block")
                checked += 1
        records.append({
            "atoms": m,
            "block_families": len(families),
            "ordered_pairs": checked,
        })
    payload = {
        "audit": Path(__file__).name,
        "audit_sha256": sha256_file(Path(__file__)),
        "method": "abstract disjoint block families plus independent max flow",
        "records": records,
        "verified": True,
    }
    print(json.dumps(payload, indent=2))
    print("AUDIT VERIFIED: capacitated selector for every block-family pair through six atoms")


if __name__ == "__main__":
    main()
