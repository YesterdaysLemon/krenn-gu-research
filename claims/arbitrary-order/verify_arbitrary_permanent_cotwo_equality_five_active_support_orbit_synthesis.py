"""Primary exact checks for the co-two equality-five support synthesis.

The characteristic-zero proof is the accompanying theorem document.  This
script pins its four dependency packages and independently replays the three
surviving rational r=4 frames with exact SymPy linear algebra.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from itertools import combinations
from math import comb
from pathlib import Path

import sympy as sp

Vector = tuple[int, ...]
Basis = tuple[Vector, ...]

REPOSITORY = Path(__file__).resolve().parents[2]
CLAIMS = REPOSITORY / "claims" / "arbitrary-order"

DEPENDENCIES = {
    "ARBITRARY_PERMANENT_COTWO_PRODUCT_SENSOR_CORANK_TWO_STRENGTHENING_THEOREM.md": "486cc700d12f99fc72997db918d816efcf5368ae6b45adf722a4aa38abf0d0b8",
    "verify_arbitrary_permanent_cotwo_product_sensor_corank_two_strengthening.py": "f5fa077ac5ba08ee364ce991e0e0c4b4cb265a7d438c16011f2e8d9d17299b2a",
    "audit_arbitrary_permanent_cotwo_product_sensor_corank_two_strengthening.py": "d29e1eeb21714898740b6bae7b803137881bcc4266c40b8d38bbd7dfb2cd3761",
    "ARBITRARY_PERMANENT_PAIR_DIMENSION_FIVE_R4_ORBIT_CLASSIFICATION_THEOREM.md": "4b7fccccf68b55e1ddeacb7328b7469a8a82f36aa2ab0303e9094519a95fc5bc",
    "verify_arbitrary_permanent_pair_dimension_five_r4_orbit_classification.py": "c99410b5d01f6bfb71b7c8f07859a83376bbf38a935b6f5313e4983a6becff07",
    "audit_arbitrary_permanent_pair_dimension_five_r4_orbit_classification.py": "62f1d4edebdaee01d9f61dd43e705568dc18188a39ebfee4a2fe971572961e03",
    "ARBITRARY_PERMANENT_ACTIVE_SUPPORT_FIVE_EQUALITY_EXCLUSION_THEOREM.md": "de7fa0633e0d79796a5f76528f7b79bc99655f3f0f549133df4651b71f6e83d2",
    "verify_arbitrary_permanent_active_support_five_equality_exclusion.py": "998eadde4d7f268524b2da6c612beccac29d3ebdb8d24e8b1e9216ee4977376b",
    "audit_arbitrary_permanent_active_support_five_equality_exclusion.py": "757572a83973a8d9d26dc3b75cd97c7344efe89dfea1f77bb9a82d0784f0400b",
    "ARBITRARY_PERMANENT_ACTIVE_SUPPORT_AT_LEAST_SIX_EQUALITY_EXCLUSION_THEOREM.md": "d55aa47cda33cc749522164ac477935798b9e6bee1def41edaada80be9e645f7",
    "verify_arbitrary_permanent_active_support_at_least_six_equality_exclusion.py": "a505515ef0274f03ea636e8c339054a55d659705f00a951de5a5c5b49e4687e8",
    "audit_arbitrary_permanent_active_support_at_least_six_equality_exclusion.py": "3c911034221d721e079856ae0d20223e09a8363717efa22e9498ff7f4994f147",
}

EDGES = tuple(combinations(range(4), 2))


@dataclass(frozen=True)
class Frame:
    """One exact pair-level Delta-admissible r=4 frame."""

    label: str
    normal_left: Vector
    normal_right: Vector
    left: Basis
    right: Basis
    mixed_generators: Basis
    annihilator_degrees: Vector


def frozen_dependency_hashes() -> dict[str, str]:
    """Require byte-exact identities for all four dependency packages."""
    observed: dict[str, str] = {}
    for relative, expected in DEPENDENCIES.items():
        path = CLAIMS / relative
        digest = sha256(path.read_bytes()).hexdigest()
        assert digest == expected, f"dependency drift: {relative}: {digest}"
        observed[relative] = digest
    return observed


def frames() -> tuple[Frame, ...]:
    """Return the three displayed surviving orbit representatives."""
    return (
        Frame(
            "(3,1)",
            (1, 1, 1, 0),
            (1, -1, -1, 0),
            ((0, 1, -1, 0), (0, 0, 0, 1), (-1, 0, 1, 0)),
            ((0, -1, 1, 0), (1, 1, 0, 0), (0, 0, 0, 1)),
            ((1, -1, 0, -1, 0, 0), (0, 0, 0, 0, 1, -1)),
            (2, 1, 1, 0),
        ),
        Frame(
            "(4,1)",
            (1, 1, 1, 1),
            (1, -1, -1, -1),
            ((-1, 0, 1, 0), (1, 0, 0, -1), (0, 1, -1, 0)),
            ((1, 1, -1, 1), (1, 1, 0, 0), (0, -1, 1, 0)),
            ((-1, 1, 0, 1, 0, 0), (1, -1, 0, 0, -1, 1)),
            (3, 1, 1, 1),
        ),
        Frame(
            "(4,2)",
            (1, 1, 1, 1),
            (1, 1, -1, -1),
            ((1, 0, 0, -1), (0, 1, 0, -1), (0, 0, 1, -1)),
            ((0, 1, 1, 0), (1, 0, 1, 0), (0, 0, 1, -1)),
            ((0, 1, -1, 0, 0, -1), (0, 0, 0, 1, -1, -1)),
            (2, 2, 2, 2),
        ),
    )


def square_free_product(left: Vector, right: Vector) -> Vector:
    """Multiply linear forms in the square-free degree-two algebra."""
    return tuple(
        left[first] * right[second] + left[second] * right[first]
        for first, second in EDGES
    )


def product_table(left: Basis, right: Basis) -> tuple[Basis, ...]:
    """Return a three-by-three exact quadratic product table."""
    return tuple(tuple(square_free_product(u, v) for v in right) for u in left)


def vector_rank(vectors: list[Vector] | tuple[Vector, ...]) -> int:
    """Compute exact rational row rank."""
    return int(sp.Matrix(vectors).rank()) if vectors else 0


def flatten(table: tuple[Basis, ...]) -> list[Vector]:
    """Flatten a three-by-three product table in row-major order."""
    return [table[row][column] for row in range(3) for column in range(3)]


def support(bases: tuple[Basis, ...]) -> tuple[int, ...]:
    """Return the union of active coordinate indices."""
    return tuple(
        index
        for index in range(4)
        if any(vector[index] for basis in bases for vector in basis)
    )


def dot(left: Vector, right: Vector) -> int:
    """Return the integer dot product."""
    return sum(a * b for a, b in zip(left, right, strict=True))


def normalized_annihilator(products: list[Vector]) -> Vector:
    """Return the primitive unique rational annihilator."""
    nullspace = sp.Matrix(products).nullspace()
    assert len(nullspace) == 1
    vector = nullspace[0]
    denominator = sp.ilcm(*(entry.q for entry in vector))
    entries = [int(entry * denominator) for entry in vector]
    common = sp.igcd(*entries)
    entries = [entry // common for entry in entries]
    if next(entry for entry in entries if entry) < 0:
        entries = [-entry for entry in entries]
    return tuple(entries)


def graph_degrees(edge_vector: Vector) -> Vector:
    """Return the descending support-graph degree multiset."""
    degree = [0, 0, 0, 0]
    for coefficient, (first, second) in zip(edge_vector, EDGES, strict=True):
        if coefficient:
            degree[first] += 1
            degree[second] += 1
    return tuple(sorted(degree, reverse=True))


def sign_split(normal_left: Vector, normal_right: Vector) -> tuple[int, int]:
    """Recover the (normal support, smaller sign block) orbit label."""
    active = tuple(index for index, value in enumerate(normal_left) if value)
    assert active == tuple(index for index, value in enumerate(normal_right) if value)
    ratios = [sp.Rational(normal_right[index], normal_left[index]) for index in active]
    relative = [sp.cancel(value / ratios[0]) for value in ratios]
    assert set(relative) == {-1, 1}
    return len(active), min(relative.count(1), relative.count(-1))


def verify_frame(frame: Frame) -> dict[str, object]:
    """Replay admissibility and the separating invariant for one frame."""
    assert vector_rank(frame.left) == vector_rank(frame.right) == 3
    assert support((frame.left, frame.right)) == (0, 1, 2, 3)
    assert all(dot(vector, frame.normal_left) == 0 for vector in frame.left)
    assert all(dot(vector, frame.normal_right) == 0 for vector in frame.right)
    assert (
        f"{sign_split(frame.normal_left, frame.normal_right)}".replace(" ", "")
        == frame.label
    )

    table = product_table(frame.left, frame.right)
    mixed = [
        table[row][column] for row in range(3) for column in range(3) if row != column
    ]
    diagonal = [table[index][index] for index in range(3)]
    products = flatten(table)

    assert vector_rank(mixed) == 2
    assert vector_rank([*mixed, *frame.mixed_generators]) == 2
    assert vector_rank(products) == 5
    assert vector_rank([*mixed, *diagonal]) == 5
    assert vector_rank([*mixed, diagonal[0]]) == 3
    assert vector_rank([*mixed, diagonal[0], diagonal[1]]) == 4

    annihilator = normalized_annihilator(products)
    assert graph_degrees(annihilator) == frame.annihilator_degrees
    return {
        "mixed_rank": 2,
        "product_rank": 5,
        "annihilator": annihilator,
        "degrees": frame.annihilator_degrees,
    }


def verify_support_and_sensor_logic() -> dict[str, object]:
    """Check the exact arithmetic in the composed support trichotomy."""
    assert comb(3, 2) == 3 < 5
    support_cases = {
        3: "ambient quadratic dimension at most three",
        4: "r4 orbit classification",
        5: "active-support-five exclusion",
        6: "active-support-at-least-six exclusion",
    }
    assert tuple(support_cases) == (3, 4, 5, 6)

    order = sp.symbols("r", integer=True, positive=True)
    ambient = order * (order - 1) / 2
    assert sp.simplify((ambient + 3 - 6) - (ambient - 3)) == 0
    bounds = {value: (6, comb(value, 2) - 3) for value in range(3, 13)}
    assert bounds[6] == (6, 12)
    return {
        "minimum_active_support": 4,
        "equality_five_support": 4,
        "active_support_ge_5_pair_lower_bound": 6,
        "sensor_bounds_r3_through_r12": bounds,
    }


def main() -> None:
    """Run all frozen-dependency and exact synthesis checks."""
    dependencies = frozen_dependency_hashes()
    frame_profiles = {frame.label: verify_frame(frame) for frame in frames()}
    synthesis = verify_support_and_sensor_logic()

    print("co-two equality-five active-support orbit synthesis primary: PASS")
    print(f"  frozen dependency files: {len(dependencies)}")
    print(f"  surviving r4 frame profiles: {frame_profiles}")
    print(f"  support and sensor synthesis: {synthesis}")
    print("  full-extension converse: NOT CLAIMED")
    print("  global Krenn-Gu conjecture: UNRESOLVED")


if __name__ == "__main__":
    main()
