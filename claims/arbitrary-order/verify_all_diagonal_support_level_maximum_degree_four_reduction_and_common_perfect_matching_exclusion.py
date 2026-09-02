"""Primary bounded checks for the AP-prime degree-four reduction.

The all-order theorem is the written proof in the owning document.  This
script supplies exact finite checks of its common-perfect-matching lemma and
of the sharp controls used to delimit the remaining open implication.

The main check fixes a perfect matching R on six vertices.  Every graph of
maximum degree at most two containing R is R union Q for a matching Q that
uses no edge of R.  The script exhausts all 51 choices of Q for each of two
colours, finds the shore promised by the proof, and independently counts the
perfect matchings on both induced shores.
"""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path


Edge = tuple[int, int]


def edge(a: int, b: int) -> Edge:
    return (a, b) if a < b else (b, a)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def partial_matchings(vertices: tuple[int, ...], forbidden: frozenset[Edge]):
    """Yield every matching, including the empty matching."""
    if not vertices:
        yield frozenset()
        return
    a = vertices[0]
    rest = vertices[1:]
    yield from partial_matchings(rest, forbidden)
    for i, b in enumerate(rest):
        ab = edge(a, b)
        if ab in forbidden:
            continue
        tail = rest[:i] + rest[i + 1 :]
        for matching in partial_matchings(tail, forbidden):
            yield matching | {ab}


def perfect_matchings(vertices: frozenset[int], edges: frozenset[Edge]):
    """Yield every perfect matching of the specified induced graph."""
    if not vertices:
        yield frozenset()
        return
    a = min(vertices)
    for b in sorted(vertices - {a}):
        ab = edge(a, b)
        if ab not in edges:
            continue
        for tail in perfect_matchings(vertices - {a, b}, edges):
            yield tail | {ab}


def count_perfect_matchings(vertices: frozenset[int], edges: frozenset[Edge]) -> int:
    return sum(1 for _ in perfect_matchings(vertices, edges))


def components(vertices: range, edges: frozenset[Edge]):
    adjacency = {v: set() for v in vertices}
    for a, b in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
    unseen = set(vertices)
    while unseen:
        start = min(unseen)
        stack = [start]
        comp = set()
        while stack:
            v = stack.pop()
            if v in comp:
                continue
            comp.add(v)
            unseen.discard(v)
            stack.extend(adjacency[v] - comp)
        yield frozenset(comp), adjacency


def cycle_atom_blocks(
    vertices: range, graph: frozenset[Edge], reference: tuple[Edge, ...]
) -> tuple[frozenset[int], ...]:
    """Return the R-atoms lying in every alternating cycle component."""
    atom_of = {v: i for i, ab in enumerate(reference) for v in ab}
    blocks = []
    for comp, adjacency in components(vertices, graph):
        if all(len(adjacency[v]) == 2 for v in comp):
            blocks.append(frozenset(atom_of[v] for v in comp))
    return tuple(blocks)


def find_shore_mask(
    atom_count: int,
    forbidden_complete: tuple[frozenset[int], ...],
    required_hits: tuple[frozenset[int], ...],
) -> int:
    """Find nonempty proper Y hitting required blocks and containing no forbidden block."""
    for mask in range(1, (1 << atom_count) - 1):
        chosen = {i for i in range(atom_count) if mask >> i & 1}
        if any(block <= chosen for block in forbidden_complete):
            continue
        if any(not (block & chosen) for block in required_hits):
            continue
        return mask
    raise AssertionError("no shore selector exists")


def vertices_from_atoms(reference: tuple[Edge, ...], mask: int) -> frozenset[int]:
    return frozenset(
        v for i, ab in enumerate(reference) if mask >> i & 1 for v in ab
    )


def verify_common_matching_exhaustive_n6() -> dict[str, int]:
    vertices = range(6)
    all_vertices = frozenset(vertices)
    reference = (edge(0, 1), edge(2, 3), edge(4, 5))
    rset = frozenset(reference)
    residuals = tuple(partial_matchings(tuple(vertices), rset))
    if len(residuals) != 51:
        raise AssertionError(f"expected 51 residual matchings, got {len(residuals)}")

    checked = 0
    for q0 in residuals:
        g0 = rset | q0
        blocks0 = cycle_atom_blocks(vertices, g0, reference)
        for q1 in residuals:
            g1 = rset | q1
            blocks1 = cycle_atom_blocks(vertices, g1, reference)
            mask = find_shore_mask(len(reference), blocks0, blocks1)
            shore = vertices_from_atoms(reference, mask)
            complement = all_vertices - shore
            if count_perfect_matchings(shore, g0) != 1:
                raise AssertionError("first induced shore is not uniquely matchable")
            if count_perfect_matchings(complement, g1) != 1:
                raise AssertionError("complementary induced shore is not uniquely matchable")
            checked += 1
    return {"residual_matchings": len(residuals), "ordered_pairs": checked}


def colour_cycle_blocks(reference: frozenset[Edge], choice: frozenset[Edge]):
    vertices = range(2 * len(reference))
    ref = tuple(sorted(reference))
    atom_of = {v: i for i, ab in enumerate(ref) for v in ab}
    blocks = []
    for comp, adjacency in components(vertices, reference | choice):
        if all(len(adjacency[v]) == 2 for v in comp):
            blocks.append(frozenset(e for e in choice if e[0] in comp))
            if len({atom_of[v] for v in comp}) < 2:
                raise AssertionError("cycle block must contain at least two atoms")
    return tuple(blocks)


def is_blocked(matching: frozenset[Edge], block_families) -> bool:
    return any(block <= matching for blocks in block_families for block in blocks)


def verify_sharp_controls() -> dict[str, int]:
    # Pairwise-disjoint support matchings are not automatic.
    h = {edge(6, 7)}
    e0 = {edge(0, 3), edge(1, 5), edge(2, 7), edge(4, 6)}
    e1 = {
        edge(0, 2), edge(1, 3), edge(1, 7),
        edge(2, 6), edge(3, 4), edge(4, 5),
    }
    e2 = {
        edge(0, 4), edge(0, 7), edge(1, 2),
        edge(3, 5), edge(5, 6),
    }
    graphs8 = tuple(frozenset(es | h) for es in (e0, e1, e2))
    pms8 = [tuple(perfect_matchings(frozenset(range(8)), graph)) for graph in graphs8]
    if [len(pms) for pms in pms8] != [1, 1, 1]:
        raise AssertionError("the n=8 control must have three unique support matchings")
    if not (edge(6, 7) in pms8[1][0] and edge(6, 7) in pms8[2][0]):
        raise AssertionError("the n=8 collision edge was not forced")
    shore8 = frozenset({0, 3})
    if count_perfect_matchings(shore8, graphs8[0]) != 1:
        raise AssertionError("n=8 first sharp shore failed")
    if count_perfect_matchings(frozenset(range(8)) - shore8, graphs8[1]) != 1:
        raise AssertionError("n=8 complementary sharp shore failed")

    # Three colours are needed in the final cycle-avoidance step.
    r10 = frozenset({
        edge(0, 1), edge(2, 3), edge(4, 5), edge(6, 7), edge(8, 9)
    })
    choices10 = (
        frozenset({edge(0, 2), edge(1, 3), edge(4, 6), edge(5, 9), edge(7, 8)}),
        frozenset({edge(0, 3), edge(1, 2), edge(4, 7), edge(5, 8), edge(6, 9)}),
        frozenset({edge(0, 4), edge(1, 6), edge(2, 8), edge(3, 9), edge(5, 7)}),
    )
    union10 = frozenset().union(*choices10)
    pms10 = tuple(perfect_matchings(frozenset(range(10)), union10))
    blocks10 = tuple(colour_cycle_blocks(r10, pc) for pc in choices10)
    mono10 = two10 = three10 = safe_three10 = 0
    for matching in pms10:
        used = {c for c, pc in enumerate(choices10) if matching & pc}
        if len(used) == 1:
            mono10 += 1
        elif len(used) == 2:
            two10 += 1
            if not is_blocked(matching, blocks10):
                raise AssertionError("the n=10 two-colour matching should be blocked")
        else:
            three10 += 1
            if not is_blocked(matching, blocks10):
                safe_three10 += 1
    if (len(pms10), mono10, two10, three10, safe_three10) != (8, 3, 2, 3, 3):
        raise AssertionError("unexpected n=10 perfect-matching census")

    # A fixed support-matching choice can have no cycle-avoiding mixed matching.
    r12 = frozenset({
        edge(0, 1), edge(2, 3), edge(4, 5),
        edge(6, 7), edge(8, 9), edge(10, 11),
    })
    choices12 = (
        frozenset({
            edge(0, 6), edge(1, 7), edge(2, 9),
            edge(3, 10), edge(4, 8), edge(5, 11),
        }),
        frozenset({
            edge(0, 7), edge(1, 6), edge(2, 11),
            edge(3, 4), edge(5, 9), edge(8, 10),
        }),
        frozenset({
            edge(0, 5), edge(1, 2), edge(3, 8),
            edge(4, 6), edge(7, 10), edge(9, 11),
        }),
    )
    union12 = frozenset().union(*choices12)
    pms12 = tuple(perfect_matchings(frozenset(range(12)), union12))
    blocks12 = tuple(colour_cycle_blocks(r12, pc) for pc in choices12)
    if len(pms12) != 9 or any(not is_blocked(pm, blocks12) for pm in pms12):
        raise AssertionError("unexpected n=12 fixed-choice blocker census")

    replacement = (
        r12,
        choices12[1],
        choices12[2],
    )
    safe = frozenset({
        edge(0, 1), edge(2, 11), edge(3, 8),
        edge(4, 6), edge(5, 9), edge(7, 10),
    })
    if safe not in set(perfect_matchings(frozenset(range(12)), frozenset().union(*replacement))):
        raise AssertionError("replacement n=12 matching is absent")
    replacement_blocks = tuple(colour_cycle_blocks(r12, pc) for pc in replacement)
    if is_blocked(safe, replacement_blocks):
        raise AssertionError("replacement n=12 matching should avoid every cycle block")

    return {
        "n8_unique_support_matchings": 3,
        "n10_perfect_matchings": len(pms10),
        "n10_safe_three_colour_matchings": safe_three10,
        "n12_fixed_choice_perfect_matchings": len(pms12),
        "n12_repaired_safe_matchings": 1,
    }


def main() -> None:
    payload = {
        "verifier": Path(__file__).name,
        "verifier_sha256": sha256_file(Path(__file__)),
        "common_matching_n6": verify_common_matching_exhaustive_n6(),
        "sharp_controls": verify_sharp_controls(),
        "verified": True,
    }
    print(json.dumps(payload, indent=2))
    print("VERIFIED: common-matching selector and sharp controls")


if __name__ == "__main__":
    main()
