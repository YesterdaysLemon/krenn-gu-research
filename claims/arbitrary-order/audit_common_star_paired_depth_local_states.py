#!/usr/bin/env python3
"""Enumerate the literal local states of one protected common-star K4.

This is a finite corroboration of the local taxonomy used in the owning theorem. The
global triangle-free and one-label arguments remain analytic.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, product


CENTER = 0
LEAVES = (1, 2, 3)  # L_c is physical vertex c+1.
COLORS = (0, 1, 2)


def leaf(color: int) -> int:
    return color + 1


def protected_edges(color: int) -> tuple[frozenset[int], frozenset[int]]:
    other = tuple(x for x in COLORS if x != color)
    return (
        frozenset((CENTER, leaf(color))),
        frozenset((leaf(other[0]), leaf(other[1]))),
    )


EDGE_COLOR = {
    edge: color
    for color in COLORS
    for edge in protected_edges(color)
}
assert len(EDGE_COLOR) == 6


def q_value(word: tuple[int, ...], background: int) -> int:
    return sum(
        all(word[vertex] != background for vertex in edge)
        for edge in protected_edges(background)
    )


def complete_minority_edges(
    word: tuple[int, ...], background: int
) -> tuple[frozenset[int], ...]:
    return tuple(
        edge
        for edge in protected_edges(background)
        if all(word[vertex] != background for vertex in edge)
    )


def local_states() -> list[dict[str, object]]:
    states: list[dict[str, object]] = []
    vertices = frozenset(range(4))
    for crossing_count in (0, 2, 4):
        for crossed_tuple in combinations(range(4), crossing_count):
            crossed = frozenset(crossed_tuple)
            internal = vertices - crossed
            if len(internal) == 4:
                internal_colors = COLORS
            elif len(internal) == 2 and internal in EDGE_COLOR:
                internal_colors = (EDGE_COLOR[internal],)
            elif not internal:
                internal_colors = (None,)
            else:
                continue

            # A crossed leaf L_j necessarily has endpoint color j.  A crossed
            # center may carry any endpoint color of an incident gadget.
            center_colors = COLORS if CENTER in crossed else (None,)
            for internal_color, center_color in product(
                internal_colors, center_colors
            ):
                word: list[int | None] = [None] * 4
                if internal_color is not None:
                    for vertex in internal:
                        word[vertex] = internal_color
                for vertex in crossed:
                    word[vertex] = (
                        center_color if vertex == CENTER else vertex - 1
                    )
                assert all(color is not None for color in word)
                literal_word = tuple(int(color) for color in word)

                if crossing_count == 0:
                    kind = "uniform"
                elif crossing_count == 2 and CENTER in crossed:
                    kind = "AB"
                elif crossing_count == 2:
                    kind = "BB"
                else:
                    kind = "degree4"

                states.append(
                    {
                        "kind": kind,
                        "crossed": tuple(sorted(crossed)),
                        "internal_color": internal_color,
                        "center_crossing_color": center_color,
                        "word": literal_word,
                        "q": tuple(q_value(literal_word, c) for c in COLORS),
                    }
                )
    return states


def verify() -> dict[str, object]:
    states = local_states()
    kinds = Counter(state["kind"] for state in states)
    assert len(states) == 18
    assert kinds == Counter({"AB": 9, "uniform": 3, "BB": 3, "degree4": 3})

    per_background: dict[int, dict[str, object]] = {}
    for c in COLORS:
        q_hist = Counter(state["q"][c] for state in states)
        assert q_hist == Counter({1: 8, 2: 6, 0: 4})

        q0 = [state for state in states if state["q"][c] == 0]
        assert all(
            state["kind"] == "uniform" and state["word"] == (c, c, c, c)
            or state["kind"] == "AB" and state["word"][1:] == (c, c, c)
            for state in q0
        )

        q1 = [state for state in states if state["q"][c] == 1]
        ab = [state for state in q1 if state["kind"] == "AB"]
        bb = [state for state in q1 if state["kind"] == "BB"]
        degree4 = [state for state in q1 if state["kind"] == "degree4"]
        assert len(ab) == 2 and len(bb) == 3 and len(degree4) == 3
        assert all(
            state["word"][0] == c
            and len(set(state["word"][1:])) == 1
            and state["word"][1] != c
            for state in ab
        )
        assert {state["internal_color"] for state in bb} == set(COLORS)
        assert sum(state["internal_color"] == c for state in bb) == 1
        assert {state["center_crossing_color"] for state in degree4} == set(COLORS)

        expected_root = protected_edges(c)[1]
        for state in q1:
            roots = complete_minority_edges(state["word"], c)
            assert roots == (expected_root,)
            assert frozenset((CENTER, leaf(c))) not in roots

        per_background[c] = {
            "q_histogram": dict(sorted(q_hist.items())),
            "q1_by_kind": dict(Counter(state["kind"] for state in q1)),
            "bb_internal_colors": sorted(state["internal_color"] for state in bb),
            "degree4_center_colors": sorted(
                state["center_crossing_color"] for state in degree4
            ),
            "unique_root_pair": sorted(expected_root),
        }

    return {
        "state_count": len(states),
        "kind_histogram": dict(kinds),
        "per_background": per_background,
    }


def main() -> None:
    receipt = verify()
    print(f"state_count={receipt['state_count']}")
    print(f"kind_histogram={receipt['kind_histogram']}")
    for background, record in receipt["per_background"].items():
        print(
            f"background={background} q_histogram={record['q_histogram']} "
            f"q1_by_kind={record['q1_by_kind']} "
            f"bb_internal_colors={record['bb_internal_colors']} "
            f"degree4_center_colors={record['degree4_center_colors']} "
            f"unique_root_pair={record['unique_root_pair']}"
        )
    print("common_star_local_state_taxonomy=PASS")


if __name__ == "__main__":
    main()
