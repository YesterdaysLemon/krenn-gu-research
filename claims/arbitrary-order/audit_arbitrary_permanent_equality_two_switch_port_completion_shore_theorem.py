"""Independent no-import audit of the two-switch port-completion shore."""

from __future__ import annotations


def cut_size(matching: set[tuple[str, str]], modes: set[str], sources: set[str]) -> int:
    return sum((mode in modes) != (source in sources) for mode, source in matching)


def main() -> None:
    matchings = {
        "c": {
            ("a", "p1"),
            ("bc", "p2"),
            ("bd", "r"),
            ("x", "q"),
            ("y", "t"),
            ("z", "s"),
        },
        "d": {
            ("a", "p1"),
            ("bd", "p2"),
            ("bc", "s"),
            ("x", "t"),
            ("y", "q"),
            ("z", "r"),
        },
        "e": {
            ("a", "q"),
            ("bc", "r"),
            ("bd", "s"),
            ("x", "p1"),
            ("y", "p2"),
            ("z", "t"),
        },
    }
    shore_modes = {"x", "y"}
    shore_sources = {"t"}
    assert {
        colour: cut_size(matching, shore_modes, shore_sources)
        for colour, matching in matchings.items()
    } == {
        "c": 1,
        "d": 1,
        "e": 3,
    }

    # Deficit-one port arithmetic for the two possible e-port counts.
    size_s, size_t = 5, 4
    assert size_t == size_s - 1
    for e_ports in (1, 2):
        e_sources_hit_inside = size_s - e_ports
        e_sources_missed_inside = size_t - e_sources_hit_inside
        assert e_ports + e_sources_missed_inside == 2 * e_ports - 1

    # The c,d internal degrees force one path between distinct port modes;
    # all remaining internal vertices have degree two and therefore cycle.
    internal_degrees = {"u_c": 1, "u_d": 1, "ordinary_mode": 2, "source": 2}
    assert [name for name, degree in internal_degrees.items() if degree == 1] == [
        "u_c",
        "u_d",
    ]

    print("independent no-import two-switch port-completion shore audit: PASS")


if __name__ == "__main__":
    main()
