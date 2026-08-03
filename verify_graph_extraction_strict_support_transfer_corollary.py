"""Primary arithmetic checks for the graph-extraction support transfer."""

from __future__ import annotations


def strict_support(permanent_order: int) -> int:
    return 3 * permanent_order + 3


def main() -> None:
    assert strict_support(5) == 18
    assert strict_support(6) == 21
    assert strict_support(7) == 24

    for roots in range(2, 20):
        one_port_order = roots + 1
        two_port_order = roots + 2
        assert strict_support(one_port_order) == 3 * roots + 6
        assert strict_support(two_port_order) == 3 * roots + 9

    named = {
        "P5": (5, 18, 17),
        "P6": (6, 21, 20),
        "P7": (7, 24, 23),
    }
    for order, lower_bound, excluded_shell in named.values():
        assert strict_support(order) == lower_bound
        assert excluded_shell == lower_bound - 1

    print("graph-extraction strict-support transfer: PASS")
    print("arithmetic transfer only; no graph or matching census was performed")


if __name__ == "__main__":
    main()
