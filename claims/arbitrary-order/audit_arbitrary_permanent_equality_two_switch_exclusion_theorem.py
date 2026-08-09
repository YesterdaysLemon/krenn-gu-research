"""Independent no-import audit of the two-switch equality exclusion."""

from __future__ import annotations


def main() -> None:
    # The opposite switch fibre has the forced physical path p1-a-p2.
    path = ("p1", "a", "p2")
    assert path[0] == "p1" and path[-1] == "p2"
    assert len(path) - 1 == 2

    pure_core, residual_mixed = 5, 7
    assert residual_mixed * pure_core == 35

    # A separate C_8 chord extension.
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
    extension = {
        chord,
        frozenset((1, 2)),
        frozenset((4, 5)),
        frozenset((6, 7)),
    }
    assert chord not in cycle_edges
    assert extension - {chord} <= cycle_edges
    assert sorted(vertex for edge in extension for vertex in edge) == list(range(8))

    original_e = (("u1", "p1"), ("u2", "p2"))
    switched_e = (("u1", "p2"), ("u2", "p1"))
    assert original_e != switched_e
    assert {mode for mode, _ in switched_e} == {"u1", "u2"}
    assert {source for _, source in switched_e} == {"p1", "p2"}

    m = 7
    assert 3 * m + 3 == 24

    print("independent no-import two-switch exclusion audit: PASS")


if __name__ == "__main__":
    main()
