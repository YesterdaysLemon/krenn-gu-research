"""Independent no-import audit of the one-switch cut normal form."""

from __future__ import annotations


def balanced(vertex_count: int, edges: list[tuple[int, int, int]]) -> bool:
    """Solve k_u xor k_v = label by exact parity propagation."""
    adjacency: list[list[tuple[int, int]]] = [[] for _ in range(vertex_count)]
    for left, right, label in edges:
        adjacency[left].append((right, label))
        adjacency[right].append((left, label))

    values: list[int | None] = [None] * vertex_count
    for root in range(vertex_count):
        if values[root] is not None:
            continue
        values[root] = 0
        stack = [root]
        while stack:
            current = stack.pop()
            assert values[current] is not None
            for neighbor, label in adjacency[current]:
                required = values[current] ^ label
                if values[neighbor] is None:
                    values[neighbor] = required
                    stack.append(neighbor)
                elif values[neighbor] != required:
                    return False
    return True


def main() -> None:
    # The pure and mixed coefficients have one common nonzero bracket.
    a, b, c, d = 2, 3, 5, 7
    pure_residual, mixed_residual = 11, 13
    bracket = a * d + b * c
    assert bracket != 0
    assert pure_residual * bracket != 0
    assert mixed_residual * bracket != 0

    # Both marked edges bridges: the two labels are a coboundary.
    assert balanced(4, [(0, 1, 1), (2, 3, 1)])

    # Both marked edges in the same two-edge cut: a balanced four-cycle.
    assert balanced(4, [(0, 2, 1), (0, 3, 0), (1, 2, 0), (1, 3, 1)])

    # Marked and unmarked parallel edges: the straddling two-cycle fails.
    assert not balanced(2, [(0, 1, 1), (0, 1, 0)])

    # One marked edge on a longer cycle avoiding the other also fails.
    assert not balanced(4, [(0, 1, 1), (1, 2, 0), (2, 3, 0), (3, 0, 0)])

    print("independent no-import one-switch cut normal-form audit: PASS")


if __name__ == "__main__":
    main()
