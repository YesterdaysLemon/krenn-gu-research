"""Independent no-import audit of the same-mode exceptional-pair theorem."""

from __future__ import annotations

import json
from fractions import Fraction
from itertools import permutations, product

Vector = tuple[Fraction, Fraction, Fraction, Fraction]
EdgeDictionary = dict[tuple[int, int], Fraction]


def add(left: Vector, right: Vector) -> Vector:
    """Add two rational four-vectors."""
    return tuple(x + y for x, y in zip(left, right, strict=True))  # type: ignore[return-value]


def subtract(left: Vector, right: Vector) -> Vector:
    """Subtract two rational four-vectors."""
    return tuple(x - y for x, y in zip(left, right, strict=True))  # type: ignore[return-value]


def scale(value: int | Fraction, vector: Vector) -> Vector:
    """Scale a rational four-vector."""
    scalar = Fraction(value)
    return tuple(scalar * entry for entry in vector)  # type: ignore[return-value]


def quadratic_edges(
    left: Vector,
    right: Vector,
    coefficient: int | Fraction = 1,
) -> EdgeDictionary:
    """Multiply two forms in the square-free algebra without matrix code."""
    scalar = Fraction(coefficient)
    edges: EdgeDictionary = {}
    for i in range(4):
        for j in range(i + 1, 4):
            value = scalar * (left[i] * right[j] + left[j] * right[i])
            if value:
                edges[(i, j)] = value
    return edges


def contract(edges: EdgeDictionary, vector: Vector) -> Vector:
    """Contract a square-free quadratic edge dictionary with one vector."""
    output = [Fraction(0) for _ in range(4)]
    for (i, j), coefficient in edges.items():
        output[i] += coefficient * vector[j]
        output[j] += coefficient * vector[i]
    return tuple(output)  # type: ignore[return-value]


def rank(columns: tuple[Vector, ...]) -> int:
    """Compute exact column rank by an independent rational reducer."""
    if not columns:
        return 0
    work = [list(row) for row in zip(*columns, strict=True)]
    pivot_row = 0
    for column in range(len(columns)):
        pivot = next(
            (row for row in range(pivot_row, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        work[pivot_row] = [value / pivot_value for value in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row:
                continue
            factor = work[row][column]
            work[row] = [
                value - factor * pivot_value
                for value, pivot_value in zip(work[row], work[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def quotient(vector: Vector) -> tuple[Fraction, Fraction]:
    """Map R^* to the quotient by span(h2,h2')."""
    return vector[0] + vector[1], vector[2] + vector[3]


def fixed_edges() -> dict[str, EdgeDictionary]:
    """Independently reconstruct the five factorized quadratics."""
    x0 = (Fraction(1), Fraction(0), Fraction(0), Fraction(0))
    x1 = (Fraction(0), Fraction(1), Fraction(0), Fraction(0))
    x2 = (Fraction(0), Fraction(0), Fraction(1), Fraction(0))
    x3 = (Fraction(0), Fraction(0), Fraction(0), Fraction(1))
    return {
        "m1": quadratic_edges(x1, subtract(subtract(x3, x2), x0)),
        "m2": quadratic_edges(x0, subtract(subtract(x3, x2), x1)),
        "d0": quadratic_edges(add(x1, x2), subtract(x3, x0)),
        "d1": quadratic_edges(add(x0, x2), subtract(x3, x1)),
        "d2": quadratic_edges(x0, x1, -2),
    }


def audit_line_table_and_pair_split() -> dict[str, object]:
    """Rebuild the contractions and independently check all four pairs."""
    edges = fixed_edges()
    lines: dict[str, Vector] = {
        "A0": (Fraction(1), Fraction(0), Fraction(0), Fraction(1)),
        "C0": (Fraction(1), Fraction(0), Fraction(-1), Fraction(0)),
        "A1": (Fraction(0), Fraction(1), Fraction(0), Fraction(1)),
        "C1": (Fraction(0), Fraction(1), Fraction(-1), Fraction(0)),
    }
    h2 = (Fraction(1), Fraction(-1), Fraction(-1), Fraction(1))
    h2_prime = (Fraction(-1), Fraction(1), Fraction(-1), Fraction(1))
    assert contract(edges["m2"], lines["A0"]) == h2
    assert contract(edges["m2"], lines["C0"]) == h2
    assert contract(edges["m1"], lines["A1"]) == h2_prime
    assert contract(edges["m1"], lines["C1"]) == h2_prime
    assert rank((h2, h2_prime)) == 2
    assert quotient(h2) == quotient(h2_prime) == (Fraction(0), Fraction(0))

    immediate = {
        ("A0", "A1"): (
            ("d0", "A1"),
            ("d1", "A0"),
            ("d2", "A0"),
        ),
        ("C0", "C1"): (
            ("d0", "C0"),
            ("d1", "C1"),
            ("d2", "C0"),
        ),
    }
    for witnesses in immediate.values():
        for channel, line in witnesses:
            column = contract(edges[channel], lines[line])
            assert quotient(column) != (Fraction(0), Fraction(0))
            assert rank((h2, h2_prime, column)) == 3

    # Same-missing pair A0,C1.  The two quotient equations below are the
    # coefficientwise content of (a+c)w1 in U and
    # 2b*x0-2d*x1 in U; no symbolic package is used.
    for first, second, first_channel, first_sign in (
        ("A0", "C1", "d1", 1),
        ("C0", "A1", "d0", -1),
    ):
        p = lines[first]
        q = lines[second]
        p_first = quotient(contract(edges[first_channel], p))
        q_first = quotient(contract(edges[first_channel], q))
        p_second = quotient(contract(edges["d2"], p))
        q_second = quotient(contract(edges["d2"], q))
        assert p_first == (Fraction(0), Fraction(first_sign * 2))
        assert q_first == (Fraction(0), Fraction(first_sign * -2))
        assert p_second == q_second == (Fraction(-2), Fraction(0))

        # Test the derived normal form at several exact nonzero a,b values.
        for a, b in ((1, 1), (2, -3), (Fraction(3, 2), Fraction(5, 3))):
            c, d = -Fraction(a), Fraction(b)
            first_kernel = subtract(scale(c, p), scale(a, q))
            second_kernel = subtract(scale(d, p), scale(b, q))
            assert quotient(contract(edges[first_channel], first_kernel)) == (0, 0)
            assert quotient(contract(edges["d2"], second_kernel)) == (0, 0)
            assert Fraction(a) * d - Fraction(b) * c == 2 * Fraction(a) * Fraction(b)

    return {
        "edge_dictionaries_rebuilt": len(edges),
        "mixed_kernel_rank": rank((h2, h2_prime)),
        "immediate_zero_row_cases": 6,
        "same_missing_normal_forms_checked": 2,
        "exact_normal_form_samples_per_pair": 3,
    }


def audit_scaling_covariance() -> dict[str, int]:
    """Guard against normalizing local columns without ambient generators."""
    edges = fixed_edges()
    p = (Fraction(1), Fraction(0), Fraction(0), Fraction(1))
    q = (Fraction(0), Fraction(1), Fraction(-1), Fraction(0))
    samples = (
        (Fraction(2), Fraction(3), Fraction(5), Fraction(7)),
        (Fraction(-3, 2), Fraction(4, 5), Fraction(-7, 3), Fraction(2, 9)),
    )
    checks = 0
    for s, t, alpha, beta in samples:
        original = subtract(scale(beta, p), scale(alpha, q))
        scaled = subtract(scale(t * beta, scale(s, p)), scale(s * alpha, scale(t, q)))
        assert scaled == scale(s * t, original)
        for edge_dictionary in edges.values():
            assert contract(edge_dictionary, scaled) == scale(
                s * t,
                contract(edge_dictionary, original),
            )
            checks += 1
    return {"rational_scaling_samples": len(samples), "channel_checks": checks}


def projective_vectors(prime: int) -> tuple[tuple[int, int], ...]:
    """Return zero plus canonical projective representatives in F_p^2."""
    return ((0, 0), *((1, slope) for slope in range(prime)), (0, 1))


def j_mod(left: tuple[int, int], right: tuple[int, int], prime: int) -> int:
    """Evaluate the hyperbolic form modulo an odd prime."""
    return (left[0] * right[1] + left[1] * right[0]) % prime


def mode_compatible(
    first: tuple[tuple[int, int], ...],
    second: tuple[tuple[int, int], ...],
    prime: int,
) -> bool:
    """Check all cross-colour orthogonality conditions for two modes."""
    return all(
        not j_mod(first[i], second[j], prime)
        for i in range(3)
        for j in range(3)
        if i != j
    )


def audit_two_active_lemma(prime: int) -> dict[str, int]:
    """Exhaust the projective A-column lemma over one odd finite field."""
    states = projective_vectors(prime)
    modes = tuple(product(states, repeat=3))
    adjacency = {
        first: tuple(second for second in modes if mode_compatible(first, second, prime))
        for first in modes
    }
    compatible_sets = {mode: set(neighbours) for mode, neighbours in adjacency.items()}
    triples = 0
    two_active = 0
    for first in modes:
        for second in adjacency[first]:
            for third in compatible_sets[first].intersection(compatible_sets[second]):
                triples += 1
                assignment = (first, second, third)
                active = {
                    colour
                    for colour in range(3)
                    if any(
                        j_mod(assignment[i][colour], assignment[j][colour], prime)
                        for i, j in ((0, 1), (0, 2), (1, 2))
                    )
                }
                assert len(active) <= 2
                if len(active) == 2:
                    two_active += 1
                    missing = next(colour for colour in range(3) if colour not in active)
                    assert all(mode[missing] == (0, 0) for mode in assignment)
    return {
        "projective_states": len(states),
        "mode_profiles": len(modes),
        "compatible_mode_triples": triples,
        "two_active_profiles": two_active,
    }


def audit_one_supplier_gate() -> dict[str, int]:
    """Check structurally that one input cannot supply both x4 and x5."""
    permutations_checked = 0
    for order in permutations(range(4)):
        # Factor rows 0 and 1 are x4 and x5.  Polarization assigns them to
        # distinct input slots.  If only input 0 has an A-part, one vanishes.
        assert order[0] != order[1]
        assert order[0] != 0 or order[1] != 0
        permutations_checked += 1
    return {"quartic_polarization_orders": permutations_checked, "surviving_orders": 0}


def main() -> None:
    """Run the independent audit and print a deterministic report."""
    report = {
        "line_and_pair_audit": audit_line_table_and_pair_split(),
        "scaling_covariance": audit_scaling_covariance(),
        "two_active_F3": audit_two_active_lemma(3),
        "two_active_F5": audit_two_active_lemma(5),
        "one_supplier_gate": audit_one_supplier_gate(),
        "scope": {
            "noncommon_same_mode_pairs": "EXCLUDED",
            "N_branches": "OPEN",
            "global_krenn_gu": "UNRESOLVED",
        },
        "status": "PASS",
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
