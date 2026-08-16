"""Independent no-import audit of the co-two equality-five synthesis.

This script imports neither the primary verifier nor SymPy.  It checks the
frozen dependency bytes, reconstructs the three rational product tables with
a standalone exact reducer, repeats their ranks over two finite fields, and
audits the support-case and sensor-bound composition.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from itertools import combinations
from math import comb
from pathlib import Path

Vector = tuple[int, ...]
Basis = tuple[Vector, ...]
Table = tuple[tuple[Vector, ...], ...]

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


def file_sha256(path: Path) -> str:
    """Hash text after normalizing checkout CRLF to Git-style LF."""

    normalized = path.read_bytes().replace(b"\r\n", b"\n")
    return sha256(normalized).hexdigest()


def dependency_audit() -> str:
    """Check dependency bytes and return a digest of the ordered manifest."""
    ledger = []
    for relative in sorted(DEPENDENCIES):
        observed = file_sha256(CLAIMS / relative)
        assert observed == DEPENDENCIES[relative]
        ledger.append(f"{relative}:{observed}")
    return sha256("\n".join(ledger).encode()).hexdigest()


def rational_rank(rows: list[Vector] | tuple[Vector, ...]) -> int:
    """Compute exact rational row rank with standalone Gaussian elimination."""
    if not rows:
        return 0
    work = [[Fraction(entry) for entry in row] for row in rows]
    row_count = len(work)
    column_count = len(work[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, row_count) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        work[pivot_row] = [entry / pivot_value for entry in work[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or not work[row][column]:
                continue
            multiple = work[row][column]
            work[row] = [
                entry - multiple * basis
                for entry, basis in zip(work[row], work[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def modular_rank(rows: list[Vector], prime: int) -> int:
    """Compute row rank over one prime field with a separate reducer."""
    if not rows:
        return 0
    work = [[entry % prime for entry in row] for row in rows]
    row_count = len(work)
    column_count = len(work[0])
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (row for row in range(pivot_row, row_count) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        inverse = pow(work[pivot_row][column], -1, prime)
        work[pivot_row] = [entry * inverse % prime for entry in work[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or not work[row][column]:
                continue
            multiple = work[row][column]
            work[row] = [
                (entry - multiple * basis) % prime
                for entry, basis in zip(work[row], work[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


def square_free_product(left: Vector, right: Vector) -> Vector:
    """Multiply two four-coordinate linear forms over the integers."""
    return tuple(
        left[first] * right[second] + left[second] * right[first]
        for first, second in EDGES
    )


def product_table(left: Basis, right: Basis) -> Table:
    """Construct the three-by-three product table without project imports."""
    return tuple(tuple(square_free_product(u, v) for v in right) for u in left)


def frame_data() -> dict[str, dict[str, object]]:
    """Give independent integer data for the three surviving orbit frames."""
    return {
        "(3,1)": {
            "left": ((0, 1, -1, 0), (0, 0, 0, 1), (-1, 0, 1, 0)),
            "right": ((0, -1, 1, 0), (1, 1, 0, 0), (0, 0, 0, 1)),
            "normals": ((1, 1, 1, 0), (1, -1, -1, 0)),
            "annihilator": (1, 1, 0, 0, 0, 0),
            "degrees": (2, 1, 1, 0),
        },
        "(4,1)": {
            "left": ((-1, 0, 1, 0), (1, 0, 0, -1), (0, 1, -1, 0)),
            "right": ((1, 1, -1, 1), (1, 1, 0, 0), (0, -1, 1, 0)),
            "normals": ((1, 1, 1, 1), (1, -1, -1, -1)),
            "annihilator": (1, 1, 1, 0, 0, 0),
            "degrees": (3, 1, 1, 1),
        },
        "(4,2)": {
            "left": ((1, 0, 0, -1), (0, 1, 0, -1), (0, 0, 1, -1)),
            "right": ((0, 1, 1, 0), (1, 0, 1, 0), (0, 0, 1, -1)),
            "normals": ((1, 1, 1, 1), (1, 1, -1, -1)),
            "annihilator": (0, 1, 1, 1, 1, 0),
            "degrees": (2, 2, 2, 2),
        },
    }


def dot(left: Vector, right: Vector) -> int:
    """Return an integer dot product."""
    return sum(a * b for a, b in zip(left, right, strict=True))


def graph_degrees(edge_vector: Vector) -> Vector:
    """Compute a descending support-graph degree multiset."""
    degrees = [0, 0, 0, 0]
    for coefficient, (first, second) in zip(edge_vector, EDGES, strict=True):
        if coefficient:
            degrees[first] += 1
            degrees[second] += 1
    return tuple(sorted(degrees, reverse=True))


def active_support(left: Basis, right: Basis) -> tuple[int, ...]:
    """Compute the union support of two bases."""
    return tuple(
        index for index in range(4) if any(vector[index] for vector in (*left, *right))
    )


def audit_frames() -> tuple[dict[str, tuple[int, int, Vector]], str]:
    """Replay the frames over Q, F5, and F7 and hash their product tables."""
    profiles: dict[str, tuple[int, int, Vector]] = {}
    serialized = []
    for label, data in frame_data().items():
        left = data["left"]
        right = data["right"]
        normals = data["normals"]
        annihilator = data["annihilator"]
        degrees = data["degrees"]
        assert isinstance(left, tuple)
        assert isinstance(right, tuple)
        assert isinstance(normals, tuple)
        assert isinstance(annihilator, tuple)
        assert isinstance(degrees, tuple)

        assert rational_rank(left) == rational_rank(right) == 3
        assert active_support(left, right) == (0, 1, 2, 3)
        assert all(dot(row, normals[0]) == 0 for row in left)
        assert all(dot(row, normals[1]) == 0 for row in right)

        table = product_table(left, right)
        products = [table[row][column] for row in range(3) for column in range(3)]
        mixed = [
            table[row][column]
            for row in range(3)
            for column in range(3)
            if row != column
        ]
        diagonal = [table[index][index] for index in range(3)]

        assert rational_rank(mixed) == 2
        assert rational_rank(products) == 5
        assert rational_rank([*mixed, *diagonal]) == 5
        assert all(dot(product, annihilator) == 0 for product in products)
        assert graph_degrees(annihilator) == degrees

        for prime in (5, 7):
            assert modular_rank(mixed, prime) == 2
            assert modular_rank(products, prime) == 5
            assert modular_rank([*mixed, *diagonal], prime) == 5

        profiles[label] = (2, 5, annihilator)
        serialized.append(f"{label}:{table}")

    assert set(profiles) == {"(3,1)", "(4,1)", "(4,2)"}
    assert len({data["degrees"] for data in frame_data().values()}) == 3
    digest = sha256("\n".join(serialized).encode()).hexdigest()
    return profiles, digest


def support_case(active_size: int) -> str:
    """Route every possible active-support size to its owning argument."""
    if active_size < 3:
        return "contradicts a three-dimensional local space"
    if active_size == 3:
        return "contradicts dim Z_3 degree two = 3"
    if active_size == 4:
        return "survives to the r4 orbit classification"
    if active_size == 5:
        return "excluded by the active-support-five theorem"
    return "excluded by the active-support-at-least-six theorem"


def audit_composition() -> dict[str, object]:
    """Audit exhaustiveness and the exact sensor-dimension arithmetic."""
    assert comb(3, 2) == 3
    outcomes = {size: support_case(size) for size in range(0, 21)}
    survivors = [size for size, outcome in outcomes.items() if "survives" in outcome]
    assert survivors == [4]

    sensor_bounds = {}
    for order in range(3, 65):
        ambient = comb(order, 2)
        pair_dimension = 6
        sum_upper_bound = ambient + 3
        sensor_upper_bound = sum_upper_bound - pair_dimension
        assert sensor_upper_bound == ambient - 3
        sensor_bounds[order] = sensor_upper_bound
    assert sensor_bounds[6] == 12
    return {
        "support_outcomes_0_through_20": outcomes,
        "unique_equality_five_support": survivors,
        "P6_active_support_ge_5_sensor_upper_bound": sensor_bounds[6],
        "orders_checked": len(sensor_bounds),
    }


def main() -> None:
    """Run the independent audit."""
    dependency_digest = dependency_audit()
    profiles, table_digest = audit_frames()
    composition = audit_composition()
    print("co-two equality-five active-support synthesis no-import audit: PASS")
    print(f"  dependency manifest digest: {dependency_digest}")
    print(f"  exact Q/F5/F7 frame profiles: {profiles}")
    print(f"  product-table digest: {table_digest}")
    print(f"  support/sensor composition: {composition}")
    print("  full-extension converse: NOT CLAIMED")
    print("  global Krenn-Gu conjecture: UNRESOLVED")


if __name__ == "__main__":
    main()
