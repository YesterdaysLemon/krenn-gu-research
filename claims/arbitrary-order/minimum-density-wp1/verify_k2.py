#!/usr/bin/env python3
"""Independent replay of the k=2 minimum-density witness table.

This checker reconstructs each support and counts perfect matchings of the
supplied word by a direct recursive graph algorithm.  It does not reproduce
the generator's enumeration of scalar terms over the 105 complete-graph
matchings.
"""

import struct
import sys
from pathlib import Path


M = (
    ((0, 1), (2, 3)),
    ((0, 2), (1, 3)),
    ((0, 3), (1, 2)),
)
TOTAL = 4**6 * 2**6


def foreign_rank(color, other):
    return [x for x in range(3) if x != color].index(other)


def allocation_digit(code, side, color):
    return (code // (4 ** (3 * side + color))) % 4


def pair_choice(code, side, color, other):
    digit = allocation_digit(code, side, color)
    return (digit >> 1) & 1 if foreign_rank(color, other) == 0 else digit & 1


def decode_word(code):
    word = []
    for _ in range(8):
        word.append(code % 3)
        code //= 3
    return tuple(word)


def low_q_mixed(word):
    if len(set(word)) == 1:
        return False
    for c in range(3):
        q = 0
        for side in range(2):
            off = 4 * side
            for x, y in M[c]:
                q += word[off + x] != c and word[off + y] != c
        if q <= 1:
            return True
    return False


def word_graph(allocation, orientation, word):
    adjacency = [set() for _ in range(8)]
    for side in range(2):
        off = 4 * side
        for c in range(3):
            for x, y in M[c]:
                u, v = off + x, off + y
                if word[u] == c and word[v] == c:
                    adjacency[u].add(v)
                    adjacency[v].add(u)

    gadget = 0
    for a in range(3):
        for b in range(3):
            if a == b:
                continue
            lp = pair_choice(allocation, 0, a, b)
            rp = pair_choice(allocation, 1, b, a)
            left = list(M[a][lp])
            right = [4 + x for x in M[b][rp]]
            if (orientation >> gadget) & 1:
                right.reverse()
            for u, v in zip(left, right):
                if word[u] == a and word[v] == b:
                    adjacency[u].add(v)
                    adjacency[v].add(u)
            gadget += 1
    return adjacency


def matching_count_capped_two(adjacency):
    def rec(remaining):
        if not remaining:
            return 1
        u = min(remaining, key=lambda x: len(adjacency[x] & remaining))
        count = 0
        for v in adjacency[u] & remaining:
            count += rec(remaining - {u, v})
            if count >= 2:
                return 2
        return count

    return rec(set(range(8)))


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("k2-witness-table.bin")
    data = path.read_bytes()
    assert data[:4] == b"K2W1"
    (count,) = struct.unpack_from("<I", data, 4)
    assert count == TOTAL
    assert len(data) == 8 + 2 * TOTAL

    for index in range(TOTAL):
        (word_code,) = struct.unpack_from("<H", data, 8 + 2 * index)
        assert word_code != 0xFFFF
        assert word_code < 3**8
        word = decode_word(word_code)
        assert low_q_mixed(word)
        allocation, orientation = index >> 6, index & 63
        adjacency = word_graph(allocation, orientation, word)
        assert matching_count_capped_two(adjacency) == 1, (
            index,
            allocation,
            orientation,
            word,
        )
        if (index + 1) % 65536 == 0:
            print(f"verified={index + 1}")
    print(f"INDEPENDENT_K2_COVER_PASS supports={TOTAL}")


if __name__ == "__main__":
    main()
