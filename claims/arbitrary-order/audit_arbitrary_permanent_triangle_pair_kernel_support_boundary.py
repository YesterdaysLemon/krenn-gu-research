"""Independent no-import audit of the triangle-pair kernel boundary."""

from __future__ import annotations

import json
from itertools import product

Vector = tuple[int, ...]
Polynomial = dict[tuple[int, ...], int]


def quartics() -> dict[str, Polynomial]:
    """Build the five expanded square-free quartics independently."""
    return {
        "f1": {(2, 3, 4, 5): 1, (1, 3, 4, 5): -1, (0, 3, 4, 5): -1},
        "f2": {(0, 2, 4, 5): 1, (0, 1, 4, 5): -1},
        "d0": {(0, 3, 4, 5): 2},
        "d1": {(0, 2, 4, 5): 1, (1, 2, 4, 5): 1},
        "d2": {(0, 1, 4, 5): 1, (1, 2, 4, 5): -1},
    }


def contract_to_residual(poly: Polynomial, vector: Vector, prime: int) -> Vector:
    """Contract once and extract the residual linear form beside x4*x5."""
    answer = [0, 0, 0, 0]
    for monomial, coefficient in poly.items():
        for position, index in enumerate(monomial):
            remaining = monomial[:position] + monomial[position + 1:]
            if len(remaining) == 3 and 4 in remaining and 5 in remaining:
                residual_index = next(i for i in remaining if i not in (4, 5))
                answer[residual_index] += coefficient * vector[index]
    return tuple(value % prime for value in answer)


def rank_mod(columns: list[Vector], prime: int) -> int:
    """Compute column rank using a small independent modular reducer."""
    if not columns:
        return 0
    matrix = [[column[row] % prime for column in columns] for row in range(len(columns[0]))]
    rank = 0
    for column in range(len(columns)):
        pivot = next((row for row in range(rank, len(matrix)) if matrix[row][column]), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inverse = pow(matrix[rank][column], -1, prime)
        matrix[rank] = [(entry * inverse) % prime for entry in matrix[rank]]
        for row in range(len(matrix)):
            if row == rank or not matrix[row][column]:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                (entry - factor * pivot_entry) % prime
                for entry, pivot_entry in zip(matrix[row], matrix[rank], strict=True)
            ]
        rank += 1
        if rank == len(matrix):
            break
    return rank


def projective_pairs(prime: int) -> list[tuple[int, int]]:
    """Enumerate P^1 with a deterministic first-nonzero normalization."""
    pairs: list[tuple[int, int]] = []
    for a, b in product(range(prime), repeat=2):
        if not (a or b):
            continue
        first = a if a else b
        inverse = pow(first, -1, prime)
        normalized = ((a * inverse) % prime, (b * inverse) % prime)
        if normalized not in pairs:
            pairs.append(normalized)
    return pairs


def audit_prime(prime: int) -> dict[str, object]:
    """Exhaust both projective kernel pencils over one odd field."""
    polys = quartics()
    first_generic = 0
    first_exceptional: list[tuple[int, int]] = []
    second_generic = 0
    second_exceptional: list[tuple[int, int]] = []

    for a, b in projective_pairs(prime):
        p1 = (a, b, (a + b) % prime, 0, 0, 0)
        p2 = (0, a, a, b, 0, 0)
        r1 = {name: contract_to_residual(poly, p1, prime) for name, poly in polys.items()}
        r2 = {name: contract_to_residual(poly, p2, prime) for name, poly in polys.items()}

        assert r1["f1"] == (0, 0, 0, 0)
        assert r2["f2"] == (0, 0, 0, 0)

        if a and b and (a + b) % prime:
            assert rank_mod([r1[name] for name in ("f2", "d0", "d1", "d2")], prime) == 4
            first_generic += 1
        else:
            first_exceptional.append((a, b))
            if not a:
                assert r1["d0"] == (0, 0, 0, 0)
            if not b:
                assert r1["d2"] == (0, 0, 0, 0)
            if not (a + b) % prime:
                assert r1["d1"] == (0, 0, 0, 0)

        if a and b:
            relation = tuple(
                (-a * r2["d0"][i] + b * r2["d1"][i] + b * r2["d2"][i]) % prime
                for i in range(4)
            )
            assert relation == (0, 0, 0, 0)
            assert rank_mod([r2[name] for name in ("d0", "d1", "d2")], prime) == 2
            second_generic += 1
        else:
            second_exceptional.append((a, b))
            if not a:
                assert r2["d1"] == r2["d2"] == (0, 0, 0, 0)
            if not b:
                assert r2["d0"] == (0, 0, 0, 0)

    expected_first = {(0, 1), (1, 0), (1, prime - 1)}
    expected_second = {(0, 1), (1, 0)}
    assert set(first_exceptional) == expected_first
    assert set(second_exceptional) == expected_second

    # The relation coefficients at a,b != 0 are all nonzero, so the three
    # independent diagonal target supports force all three local coefficients
    # to vanish.  This is a support check, not a finite-field proof of the
    # characteristic-zero theorem.
    for a, b in projective_pairs(prime):
        if a and b:
            coefficients = ((-a * pow(b, -1, prime)) % prime, 1, 1)
            assert all(coefficients)

    return {
        "field": f"F_{prime}",
        "projective_directions": prime + 1,
        "phi1_generic_directions": first_generic,
        "phi1_exceptional_directions": sorted(first_exceptional),
        "phi2_generic_directions": second_generic,
        "phi2_exceptional_directions": sorted(second_exceptional),
    }


def main() -> None:
    """Run the independent audit and print a deterministic report."""
    report = {
        "audits": [audit_prime(prime) for prime in (5, 7)],
        "independent_from_primary": True,
        "status": "PASS",
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
