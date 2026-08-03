"""Independent no-import audit of the backbone-colouring glue theorem."""

from __future__ import annotations


def propagate(labels: list[int]) -> tuple[bool, list[int]]:
    values = [0]
    for label in labels:
        values.append(values[-1] ^ label)
    return values[-1] == values[0], values


def main() -> None:
    balanced, values = propagate([0, 1, 1])
    assert balanced
    assert values == [0, 0, 1, 0]

    unbalanced, values = propagate([0, 0, 1])
    assert not unbalanced
    assert values == [0, 0, 0, 1]

    # Parallel overlap edges with labels 0 and 1 are an unbalanced two-cycle.
    assert (0 ^ 0) == 0
    assert (0 ^ 1) == 1

    # Exactly one source-side flip reverses relative parity.
    before = (0, 1)
    after = (1, 1)
    assert (before[0] ^ before[1]) != (after[0] ^ after[1])

    print("independent no-import backbone-colouring glue audit: PASS")


if __name__ == "__main__":
    main()
