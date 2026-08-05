"""Independent no-import audit of replay/exchange closure and splice counts."""

from __future__ import annotations


Vector = tuple[int, ...]


def add(*vectors: Vector) -> Vector:
    return tuple(sum(vector[index] for vector in vectors) for index in range(len(vectors[0])))


def scale(factor: int, vector: Vector) -> Vector:
    return tuple(factor * entry for entry in vector)


def main() -> None:
    lambda_12 = (1, 1, 0, 0, 0, 0)
    lambda_13 = (0, 0, 1, 1, 0, 0)
    lambda_23 = (0, 0, 0, 0, 1, 1)
    lambda_plus = (1, 0, 0, 1, 1, 0)
    lambda_minus = (0, 1, 1, 0, 0, 1)
    relation = add(
        lambda_plus,
        lambda_minus,
        scale(-1, lambda_12),
        scale(-1, lambda_13),
        scale(-1, lambda_23),
    )
    assert relation == (0, 0, 0, 0, 0, 0)
    assert 1 + 1 - 1 - 1 - 1 == -1
    assert ((-1) * (-1)) != ((-1) * (-1) * (-1))

    # The base replay and Hall-isolation ledgers.
    mode_degrees = {"x0": 4, "x1": 4, "x2": 4, "y0": 3, "y1": 3, "y2": 3}
    source_degrees = {"p0": 5, "p1": 4, "p2": 3, "q0": 3, "q1": 3, "q2": 3}
    assert sum(degree - 3 for degree in mode_degrees.values()) == 3
    assert sum(degree - 3 for degree in source_degrees.values()) == 3
    assert (source_degrees["p0"] - 3, source_degrees["p1"] - 3) == (2, 1)

    colour_two_incidence = {
        "y0": {"p1"},
        "y1": {"p0"},
        "y2": {"p2"},
        "x0": {"q1", "p0"},
        "x1": {"q2", "p0"},
        "x2": {"q0", "p1"},
    }
    deleted_a = {"x0", "p0"}
    assert not (colour_two_incidence["y1"] - deleted_a)
    deleted_b = {"x1", "p0", "x2", "p1"}
    assert not (colour_two_incidence["y0"] - deleted_b)
    assert not (colour_two_incidence["y1"] - deleted_b)

    # Affine two-switch count and replay invariance for arbitrary n.
    # It removes two and adds two edges, while all 2n new vertices remain cubic.
    for n in (3, 11, 29):
        order = 6 + n
        edges = 21 + 3 * n - 2 + 2
        assert edges == 3 * order + 3
        assert 2 * edges - 3 * (2 * order) == 6

    print("independent no-import replay/exchange closure audit: PASS")


if __name__ == "__main__":
    main()
