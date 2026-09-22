"""Independent word-first audit of the k=3 C9 residual receipt.

No code is imported from the primary enumerator.  This checker reconstructs
the gauge-fixed allocation and every scalar support directly from the two
receipt bit fields.  It independently exhausts the isolated/aligned filter,
then counts compatible physical perfect matchings for each supplied word by
a vertex-mask recursion.
"""

from __future__ import annotations

import gzip
import sys
import hashlib
import json
from collections import defaultdict
from functools import lru_cache
from pathlib import Path


HERE = Path(__file__).resolve().parent
RECEIPT = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "k3-witnesses.jsonl.gz"

# Fixed representative in the owning report, ordered lexicographically.
F = ((0, 7), (0, 8), (1, 3), (1, 8), (2, 3), (2, 4),
     (4, 6), (5, 6), (5, 7))
INC = tuple(tuple(i for i, edge in enumerate(F) if t in edge) for t in range(9))
LOCAL_PAIRS = (
    ((0, 1), (2, 3)),
    ((0, 2), (1, 3)),
    ((0, 3), (1, 2)),
)


def allocation(code):
    """Decode the component gauge representative directly from its bits."""
    out = {}
    for component in range(3):
        literals = tuple(3 * component + color for color in range(3))
        t0, t1, t2 = literals
        out[t0, INC[t0][0]] = 0
        out[t0, INC[t0][1]] = (code >> (3 * component)) & 1
        out[t1, INC[t1][0]] = 0
        out[t1, INC[t1][1]] = 1
        out[t2, INC[t2][0]] = (code >> (3 * component + 1)) & 1
        out[t2, INC[t2][1]] = (code >> (3 * component + 2)) & 1
    return out


def resource(literal, pair_index):
    component, color = divmod(literal, 3)
    return tuple(4 * component + port for port in LOCAL_PAIRS[color][pair_index])


def crossing_maps(choice, code):
    """Return maps in both literal directions, derived edge by edge."""
    maps = {}
    for edge_index, (left, right) in enumerate(F):
        source = resource(left, choice[left, edge_index])
        target = resource(right, choice[right, edge_index])
        if (code >> edge_index) & 1:
            target = target[::-1]
        forward = dict(zip(source, target))
        maps[left, edge_index] = forward
        maps[right, edge_index] = {y: x for x, y in forward.items()}
    return maps


def transit(choice, literal):
    e0, e1 = INC[literal]
    return choice[literal, e0] == choice[literal, e1]


def isolated(choice):
    return not any(transit(choice, left) and transit(choice, right) for left, right in F)


def aligned(choice, maps):
    for literal in range(9):
        _component, color = divmod(literal, 3)
        if color == 1 or not transit(choice, literal):
            continue
        e0, e1 = INC[literal]
        n0 = F[e0][0] if F[e0][1] == literal else F[e0][1]
        n1 = F[e1][0] if F[e1][1] == literal else F[e1][1]
        pair0 = set(resource(n0, choice[n0, e0]))
        pair1 = set(resource(n1, choice[n1, e1]))
        common = pair0 & pair1
        if len(common) != 1:
            raise AssertionError((literal, n0, n1, pair0, pair1))
        lone0 = next(iter(pair0 - common))
        lone1 = next(iter(pair1 - common))
        inverse0 = {target: root for root, target in maps[literal, e0].items()}
        inverse1 = {target: root for root, target in maps[literal, e1].items()}
        if inverse0[lone0] != inverse1[lone1]:
            return False
    return True


def scalar_support(choice, maps):
    edges = []
    for component in range(3):
        for color in range(3):
            for p, q in LOCAL_PAIRS[color]:
                edges.append((4 * component + p, 4 * component + q, color, color))
    for edge_index, (left, right) in enumerate(F):
        color_left = left % 3
        color_right = right % 3
        for p, q in maps[left, edge_index].items():
            if p < q:
                edges.append((p, q, color_left, color_right))
            else:
                edges.append((q, p, color_right, color_left))
    edges.sort()
    if len(edges) != 36 or len(set(edges)) != 36:
        raise AssertionError("scalar entries are not distinct")
    return edges


def support_digest(edges):
    payload = json.dumps(edges, separators=(",", ":"), ensure_ascii=True).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def q_counts(word):
    answer = []
    for color in range(3):
        total = 0
        for component in range(3):
            for p, q in LOCAL_PAIRS[color]:
                if word[4 * component + p] != color and word[4 * component + q] != color:
                    total += 1
        answer.append(total)
    return tuple(answer)


def compatible_matching_count(edges, word):
    adjacency = defaultdict(list)
    for index, (p, q, cp, cq) in enumerate(edges):
        if word[p] == cp and word[q] == cq:
            adjacency[p].append((q, index))
            adjacency[q].append((p, index))

    @lru_cache(maxsize=None)
    def count(mask):
        if mask == (1 << 12) - 1:
            return 1
        p = next(vertex for vertex in range(12) if not ((mask >> vertex) & 1))
        total = 0
        for q, _edge_index in adjacency[p]:
            if not ((mask >> q) & 1):
                total += count(mask | (1 << p) | (1 << q))
        return total

    return count(0)


def matching_is_exact(edges, word, matching):
    chosen = [tuple(item) for item in matching]
    if len(chosen) != 6 or len(set(chosen)) != 6:
        return False
    if not all(edge in edges for edge in chosen):
        return False
    used = []
    for p, q, cp, cq in chosen:
        if word[p] != cp or word[q] != cq:
            return False
        used.extend((p, q))
    return sorted(used) == list(range(12))


def expected_configurations():
    expected = set()
    allocation_count = 0
    for pair_bits in range(1 << 9):
        choice = allocation(pair_bits)
        if not isolated(choice):
            continue
        allocation_count += 1
        for map_bits in range(1 << 9):
            maps = crossing_maps(choice, map_bits)
            if aligned(choice, maps):
                expected.add((pair_bits, map_bits))
    if allocation_count != 216 or len(expected) != 32768:
        raise AssertionError((allocation_count, len(expected)))
    return expected


def main():
    expected = expected_configurations()
    seen = set()
    q_histogram = defaultdict(int)
    with (gzip.open if RECEIPT.suffix == ".gz" else open)(RECEIPT, "rt", encoding="utf-8") as stream:
        meta = json.loads(next(stream))
        if meta != {
            "expected_rows": 32768,
            "kind": "meta",
            "primary_sha256": "5aff9e47d5d775f7fb446cc2cb610d6c62cd40dff041a4b1715607885d792b7c",
            "schema": 1,
        }:
            raise AssertionError(meta)
        for line in stream:
            row = json.loads(line)
            if row.pop("kind") != "row":
                raise AssertionError(row)
            config = (row["pair_bits"], row["map_bits"])
            if config in seen or config not in expected:
                raise AssertionError(config)
            seen.add(config)
            choice = allocation(config[0])
            maps = crossing_maps(choice, config[1])
            edges = scalar_support(choice, maps)
            if support_digest(edges) != row["support_sha256"]:
                raise AssertionError((config, "support digest"))
            word = tuple(row["word"])
            if len(word) != 12 or any(type(color) is not int or color not in (0, 1, 2)
                                      for color in word):
                raise AssertionError((config, "physical word must have twelve colors in {0,1,2}"))
            q = q_counts(word)
            if list(q) != row["q"] or len(set(word)) == 1 or min(q) > 1:
                raise AssertionError((config, word, q, row["q"]))
            if not matching_is_exact(edges, word, row["matching"]):
                raise AssertionError((config, "claimed matching"))
            count = compatible_matching_count(edges, word)
            if count != 1:
                raise AssertionError((config, word, count))
            q_histogram[q] += 1
    if seen != expected:
        raise AssertionError((len(seen), len(expected), sorted(expected - seen)[:5]))
    raw = RECEIPT.read_bytes()
    if RECEIPT.suffix == ".gz":
        raw = gzip.decompress(raw)
    receipt_sha = hashlib.sha256(raw).hexdigest()
    print("independently_exhausted_configs", len(expected))
    print("independently_checked_unique_words", len(seen))
    print("q_histogram", dict(sorted(q_histogram.items())))
    print("receipt_sha256", receipt_sha)
    print("K3_WORD_FIRST_INDEPENDENT_AUDIT_PASS")


if __name__ == "__main__":
    main()
