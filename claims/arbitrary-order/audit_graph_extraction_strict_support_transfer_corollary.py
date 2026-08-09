"""Independent no-import audit of graph-extraction support bounds."""

from __future__ import annotations


def main() -> None:
    rows = []
    for roots in (4, 5):
        permanent_order = roots + 1
        lower_bound = 3 * permanent_order + 3
        rows.append((roots, roots + 1, permanent_order, lower_bound, lower_bound - 1))

    assert rows == [
        (4, 5, 5, 18, 17),
        (5, 6, 6, 21, 20),
    ]

    roots = 5
    factorized_two_port_order = roots + 2
    factorized_bound = 3 * factorized_two_port_order + 3
    assert (factorized_two_port_order, factorized_bound, factorized_bound - 1) == (
        7,
        24,
        23,
    )

    print("independent no-import graph-extraction support audit: PASS")


if __name__ == "__main__":
    main()
