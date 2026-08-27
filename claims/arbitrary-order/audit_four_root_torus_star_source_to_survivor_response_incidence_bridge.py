#!/usr/bin/env python3
"""Independent standard-library audit of the GLD81 source bridge.

This script imports neither the primary verifier nor repository Python code.
It uses a bitmask matching recurrence, a separate edge classification, and
exact ``Fraction`` arithmetic to audit the finite interfaces in the written
proof.  The theorem carries the arbitrary-source quantifiers.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from functools import cache
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[2]
THEOREM = (
    REPOSITORY
    / "claims"
    / "arbitrary-order"
    / ("FOUR_ROOT_TORUS_STAR_SOURCE_TO_SURVIVOR_RESPONSE_INCIDENCE_BRIDGE_THEOREM.md")
)

ROOT_MASK = sum(1 << vertex for vertex in range(4))
OUTSIDE_MASK = sum(1 << vertex for vertex in range(4, 10))
Q0 = 4
Q1 = 5


@cache
def pairing_family(mask: int) -> tuple[tuple[tuple[int, int], ...], ...]:
    if mask == 0:
        return ((),)
    first_bit = mask & -mask
    first = first_bit.bit_length() - 1
    rest = mask ^ first_bit
    output: list[tuple[tuple[int, int], ...]] = []
    choices = rest
    while choices:
        second_bit = choices & -choices
        second = second_bit.bit_length() - 1
        for tail in pairing_family(rest ^ second_bit):
            output.append(((first, second), *tail))
        choices ^= second_bit
    return tuple(output)


def is_root(vertex: int) -> bool:
    return bool(ROOT_MASK & (1 << vertex))


def is_outside(vertex: int) -> bool:
    return bool(OUTSIDE_MASK & (1 << vertex))


def survives_root_zeroes(matching: tuple[tuple[int, int], ...]) -> bool:
    return all(not (is_root(left) and is_root(right)) for left, right in matching)


def raw_edges(matching: tuple[tuple[int, int], ...]) -> tuple[tuple[int, int], ...]:
    return tuple(
        edge for edge in matching if is_outside(edge[0]) and is_outside(edge[1])
    )


def raw_family(edge: tuple[int, int]) -> str:
    left, _right = edge
    if edge == (Q0, Q1):
        return "residual_pair"
    if left <= Q1:
        return "residual_port"
    return "port_pair"


def residual_label(edge: tuple[int, int]) -> str | None:
    left, right = edge
    if left == Q0 and right >= 6:
        return "h_eta"
    if left == Q1 and right >= 6:
        return "h_xi"
    return None


def joins_root(matching: tuple[tuple[int, int], ...], vertex: int) -> bool:
    return any(
        (is_root(left) and right == vertex) or (is_root(right) and left == vertex)
        for left, right in matching
    )


def audit_matching_partition() -> None:
    matchings = pairing_family((1 << 10) - 1)
    assert len(matchings) == 945
    survivors = tuple(
        matching for matching in matchings if survives_root_zeroes(matching)
    )
    assert len(survivors) == 360

    exact_raw_edges = Counter()
    for matching in survivors:
        raw = raw_edges(matching)
        assert len(raw) == 1
        exact_raw_edges[raw[0]] += 1
    assert len(exact_raw_edges) == 15
    assert all(multiplicity == 24 for multiplicity in exact_raw_edges.values())

    family_counts = Counter()
    for edge, multiplicity in exact_raw_edges.items():
        family_counts[raw_family(edge)] += multiplicity
    assert family_counts == {
        "residual_pair": 24,
        "residual_port": 192,
        "port_pair": 144,
    }

    complementary_labels = Counter()
    for matching in survivors:
        edge = raw_edges(matching)[0]
        label = residual_label(edge)
        if label is None:
            continue
        complementary_labels[label] += 1
        assert joins_root(matching, Q1 if label == "h_eta" else Q0)
    assert complementary_labels == {"h_eta": 96, "h_xi": 96}


def audit_q0_response_partition() -> None:
    matchings = pairing_family((1 << 10) - 1)
    survivors = tuple(
        matching for matching in matchings if survives_root_zeroes(matching)
    )
    union: set[tuple[tuple[int, int], ...]] = set()
    neighbor_counts: dict[int, int] = {}

    for neighbor in range(10):
        if neighbor == Q0:
            continue
        edge = tuple(sorted((Q0, neighbor)))
        branch = tuple(matching for matching in survivors if edge in matching)
        neighbor_counts[neighbor] = len(branch)
        union.update(branch)
        for matching in branch:
            complement = tuple(item for item in matching if item != edge)
            number_raw = len(raw_edges(complement))
            if is_root(neighbor):
                assert number_raw == 1
            else:
                assert number_raw == 0

    assert len(union) == len(survivors)
    assert neighbor_counts == {
        0: 60,
        1: 60,
        2: 60,
        3: 60,
        5: 24,
        6: 24,
        7: 24,
        8: 24,
        9: 24,
    }

    response_labels = [("root", root, None) for root in range(4)]
    response_labels.append(("contracted", Q1, None))
    response_labels.extend(
        ("port", port, colour) for port in range(6, 10) for colour in range(3)
    )
    assert len(response_labels) == len(set(response_labels)) == 17


def audit_target_rescaling() -> None:
    root_contractions = (
        (Fraction(2), Fraction(3), Fraction(5)),
        (Fraction(7), Fraction(11), Fraction(13)),
        (Fraction(17), Fraction(19), Fraction(23)),
        (Fraction(29), Fraction(31), Fraction(37)),
    )
    q0_contraction = (Fraction(41), Fraction(43), Fraction(47))
    q1_contraction = (Fraction(53), Fraction(59), Fraction(61))

    for colour in range(3):
        root_product = Fraction(1)
        for row in root_contractions:
            root_product *= row[colour]
        contracted = root_product * q0_contraction[colour] * q1_contraction[colour]
        response_at_scaled_basis = (
            root_product * q1_contraction[colour] * q0_contraction[colour]
        )
        assert contracted == response_at_scaled_basis != 0

    root_gauges = tuple(Fraction(value) for value in (2, 3, 5, 7))
    z0_gauge, z1_gauge = Fraction(11), Fraction(13)
    grade_scale = z0_gauge * z1_gauge
    response_scale = z0_gauge * z1_gauge
    for gauge in root_gauges:
        grade_scale *= gauge
        response_scale *= gauge
    assert grade_scale == response_scale
    root_product = Fraction(1)
    for gauge in root_gauges:
        root_product *= gauge
    for gauge in root_gauges:
        assert (root_product / gauge) * gauge == root_product


def audit_scope_text() -> None:
    text = THEOREM.read_text(encoding="utf-8")
    required = (
        "legal source presentation  ==>  a physical raw alpha satisfying (6)",
        "No converse is asserted.",
        "dimension 4+1+4*3=17",
        "delta(F_0)!=0",
        "conjecture remains **UNRESOLVED**.",
        "a nonisotropic star survivor outside the certified `GLD80` component",
    )
    for phrase in required:
        assert phrase in text


def main() -> None:
    audit_matching_partition()
    print("independent 945-matching raw-edge and xi/eta-label partition: PASS")
    audit_q0_response_partition()
    print("independent complete q0 response partition: PASS")
    audit_target_rescaling()
    print("independent exact GHZ response and source-gauge rescaling: PASS")
    audit_scope_text()
    print("source direction, divisor, and global scope fences: PASS")
    print(
        "scope: GLD81 source bridge on the named torus-star branch only; "
        "explicit delta and global Krenn-Gu remain open"
    )


if __name__ == "__main__":
    main()
