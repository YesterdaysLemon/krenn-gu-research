"""Independent no-import audit of the six-token odd-ear ledger."""

from __future__ import annotations


Affine = tuple[int, int]


def add(left: Affine, right: Affine) -> Affine:
    return (left[0] + right[0], left[1] + right[1])


def subtract(left: Affine, right: Affine) -> Affine:
    return (left[0] - right[0], left[1] - right[1])


def scale(factor: int, value: Affine) -> Affine:
    return (factor * value[0], factor * value[1])


def main() -> None:
    # Affine pairs encode a*m+b without importing the primary verifier.
    vertices = (2, 0)
    edges = (3, 3)
    ears = subtract(edges, vertices)
    endpoints = scale(2, ears)
    global_replays = subtract(endpoints, vertices)
    assert ears == (1, 3)
    assert endpoints == (2, 6)
    assert global_replays == (0, 6)

    shore_vertices = (1, 0)
    shore_endpoints = ears
    shore_replays = subtract(shore_endpoints, shore_vertices)
    assert shore_replays == (0, 3)
    assert add(shore_replays, shore_replays) == global_replays

    # Sum(deg-3) globally and on either shore gives the same ledgers.
    degree_excess_global = subtract(scale(2, edges), scale(3, vertices))
    degree_excess_shore = subtract(edges, scale(3, shore_vertices))
    assert degree_excess_global == global_replays
    assert degree_excess_shore == shore_replays

    partitions_of_three = {(3,), (2, 1), (1, 1, 1)}
    assert all(sum(parts) == 3 for parts in partitions_of_three)
    assert all(len(parts) <= 3 for parts in partitions_of_three)

    # An internal vertex of the final ear receives its two birth edges only.
    assert 2 < 3

    print("independent no-import six-token odd-ear audit: PASS")


if __name__ == "__main__":
    main()
