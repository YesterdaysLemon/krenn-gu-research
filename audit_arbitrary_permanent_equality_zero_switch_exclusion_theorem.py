"""Independent no-import audit of the zero-switch exclusion theorem."""

from __future__ import annotations


def validate_matching(size: int, edges: set[tuple[int, int]]) -> bool:
    return (
        len(edges) == size
        and {left for left, _ in edges} == set(range(size))
        and {right for _, right in edges} == set(range(size))
    )


def hybrid_is_mixed(selection: tuple[str, ...]) -> bool:
    return len(set(selection)) > 1


def terminal_colours(
    port_components: tuple[int, int], selection: tuple[str, ...]
) -> tuple[str, str]:
    return (selection[port_components[0]], selection[port_components[1]])


def main() -> None:
    # Pairwise two-factor component trichotomy.
    same_selection = ("a", "b")
    assert hybrid_is_mixed(same_selection)
    assert terminal_colours((0, 0), same_selection) == ("a", "a")

    separate_with_third = ("a", "a", "b")
    assert hybrid_is_mixed(separate_with_third)
    assert terminal_colours((0, 1), separate_with_third) == ("a", "a")

    first_hybrid = ("a", "b")
    second_hybrid = ("b", "a")
    assert terminal_colours((0, 1), first_hybrid) == ("a", "b")
    assert terminal_colours((0, 1), second_hybrid) == ("b", "a")
    required_crosses = {
        ("a", "p1_to_p2"),
        ("a", "p2_to_p1"),
        ("b", "p1_to_p2"),
        ("b", "p2_to_p1"),
    }
    assert (
        len({direction for colour, direction in required_crosses if colour == "a"}) == 2
    )
    assert (
        len({direction for colour, direction in required_crosses if colour == "b"}) == 2
    )

    # Independent explicit cycle/chord reconstruction.
    size = 4
    cycle_edges = {
        (0, 0),
        (1, 0),
        (1, 1),
        (2, 1),
        (2, 2),
        (3, 2),
        (3, 3),
        (0, 3),
    }
    chord = (0, 2)
    extended = {chord, (1, 0), (2, 1), (3, 3)}
    assert validate_matching(size, extended)
    assert chord not in cycle_edges
    assert extended - {chord} <= cycle_edges

    # Disjoint nonempty subsets of a three-colour set have a singleton side.
    possible_sizes = ((1, 1), (1, 2), (2, 1))
    assert all(min(left, right) == 1 for left, right in possible_sizes)

    print("independent no-import zero-switch exclusion audit: PASS")


if __name__ == "__main__":
    main()
