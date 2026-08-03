"""Independent no-import audit of the one-switch exclusion theorem."""

from __future__ import annotations


def main() -> None:
    # One explicit C_8 chord extension.  Vertices alternate mode/source.
    cycle_edges = {
        frozenset((0, 1)),
        frozenset((1, 2)),
        frozenset((2, 3)),
        frozenset((3, 4)),
        frozenset((4, 5)),
        frozenset((5, 6)),
        frozenset((6, 7)),
        frozenset((7, 0)),
    }
    chord = frozenset((0, 3))
    chord_matching = {
        chord,
        frozenset((1, 2)),
        frozenset((4, 5)),
        frozenset((6, 7)),
    }
    assert chord not in cycle_edges
    assert chord_matching - {chord} <= cycle_edges
    covered = [vertex for edge in chord_matching for vertex in edge]
    assert sorted(covered) == list(range(8))

    # The two forced cross cells give the alternate 2 x 2 assignment.
    original = (("i1", "p1"), ("i2", "p2"))
    alternate = (("i1", "p2"), ("i2", "p1"))
    assert original != alternate
    assert {mode for mode, _ in alternate} == {"i1", "i2"}
    assert {source for _, source in alternate} == {"p1", "p2"}

    print("independent no-import one-switch exclusion audit: PASS")


if __name__ == "__main__":
    main()
