"""Exact odd-cycle contradictions among two-monomial hafnian equations.

If a forbidden colouring has exactly two active matching monomials ``A,B``,
then, on the support torus,

    A + B = 0,  hence  A / B = -1.

Associate to it the exponent-difference vector ``v = exp(A)-exp(B)``.
Reversing ``v`` does not change the right-hand side.  Three such equations
are inconsistent whenever their unoriented vectors satisfy

    +/- v1 +/- v2 +/- v3 = 0:

the product of the three ratio equations has left-hand side one and
right-hand side ``(-1)^3 = -1``.  This module detects that exact signed
triangle and extracts/replays a support no-good.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence

import numpy as np

from cancellation_transport import decided_cube_activity
from search_witness import EquationSystem

SparseVector = tuple[tuple[int, int], ...]


def _canonical_sparse_vector(coefficients: dict[int, int]) -> SparseVector:
    vector = tuple(
        sorted(
            (int(entry), int(coefficient))
            for entry, coefficient in coefficients.items()
            if coefficient
        )
    )
    negative = tuple((entry, -coefficient) for entry, coefficient in vector)
    return min(vector, negative)


def _add_sparse_vectors(
    first: SparseVector,
    second: SparseVector,
    second_sign: int = 1,
) -> SparseVector | None:
    coefficients: dict[int, int] = dict(first)
    for entry, coefficient in second:
        coefficients[entry] = (
            coefficients.get(entry, 0) + second_sign * coefficient
        )
        if not coefficients[entry]:
            del coefficients[entry]
    if not coefficients:
        return None
    return _canonical_sparse_vector(coefficients)


def matching_ratio_vector(
    system: EquationSystem,
    equation_index: int,
    first_matching: int,
    second_matching: int,
) -> SparseVector:
    """Return a canonically oriented monomial exponent difference."""
    coefficients: dict[int, int] = {}
    for entry in system.variable_ids[first_matching, equation_index, :]:
        flat = int(entry)
        coefficients[flat] = coefficients.get(flat, 0) + 1
    for entry in system.variable_ids[second_matching, equation_index, :]:
        flat = int(entry)
        coefficients[flat] = coefficients.get(flat, 0) - 1
    vector = _canonical_sparse_vector(coefficients)
    if not vector:
        raise AssertionError("distinct matchings have identical monomials")
    return vector


def _choose_distinct_equations(
    first: tuple[int, int, int],
    second: tuple[int, int, int],
    candidates: Sequence[tuple[int, int, int]],
) -> tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]] | None:
    for third in candidates:
        if len({first[0], second[0], third[0]}) == 3:
            return first, second, third
    return None


def odd_binomial_triangle_certificates(
    system: EquationSystem,
    equation_indices: Sequence[int],
    active_matchings: Sequence[set[int]],
    maximum_certificates: int | None = None,
) -> list[dict[str, object]]:
    """Find signed three-cycles among decided forbidden binomials."""
    if len(equation_indices) != len(active_matchings):
        raise ValueError("equation/activity collections have different sizes")
    if maximum_certificates is not None and maximum_certificates < 1:
        raise ValueError("maximum_certificates must be positive")

    by_vector: dict[SparseVector, list[tuple[int, int, int]]] = {}
    for equation_index, active in zip(
        equation_indices,
        active_matchings,
        strict=True,
    ):
        equation = int(equation_index)
        if bool(system.target[equation]) or len(active) != 2:
            continue
        first, second = sorted(map(int, active))
        vector = matching_ratio_vector(
            system,
            equation,
            first,
            second,
        )
        by_vector.setdefault(vector, []).append((equation, first, second))

    certificates: list[dict[str, object]] = []
    seen_equation_sets: set[tuple[int, int, int]] = set()
    vectors = sorted(by_vector)
    for first_position, first_vector in enumerate(vectors):
        for second_vector in vectors[first_position:]:
            for second_sign in (1, -1):
                target = _add_sparse_vectors(
                    first_vector,
                    second_vector,
                    second_sign,
                )
                if target is None or target not in by_vector:
                    continue
                for first_record in by_vector[first_vector]:
                    for second_record in by_vector[second_vector]:
                        if first_record[0] == second_record[0]:
                            continue
                        chosen = _choose_distinct_equations(
                            first_record,
                            second_record,
                            by_vector[target],
                        )
                        if chosen is None:
                            continue
                        records = list(chosen)
                        equations = [record[0] for record in records]
                        equation_key = tuple(sorted(equations))
                        if equation_key in seen_equation_sets:
                            continue
                        seen_equation_sets.add(equation_key)
                        certificates.append(
                            {
                                "certificate_mode": (
                                    "odd_binomial_triangle"
                                ),
                                "equation_indices": equations,
                                "colourings": [
                                    list(
                                        map(
                                            int,
                                            system.colourings[equation],
                                        )
                                    )
                                    for equation in equations
                                ],
                                "matching_indices": [
                                    [record[1], record[2]]
                                    for record in records
                                ],
                                "relation_second_sign": second_sign,
                            }
                        )
                        if (
                            maximum_certificates is not None
                            and len(certificates)
                            >= maximum_certificates
                        ):
                            return certificates
                        break
                    else:
                        continue
                    break
    return certificates


def cube_odd_binomial_triangle_certificates(
    system: EquationSystem,
    equation_indices: Iterable[int],
    positive_entries: set[int],
    zero_entries: set[int],
) -> list[dict[str, object]]:
    """Replay odd signed triangles whose equations are cube-decided."""
    retained, _colourings, activities = decided_cube_activity(
        system,
        equation_indices,
        positive_entries,
        zero_entries,
    )
    return odd_binomial_triangle_certificates(
        system,
        retained,
        activities,
    )


def support_odd_binomial_triangle_conflict(
    system: EquationSystem,
    selected_entries: set[int],
    structural_zero_entries: set[int],
) -> tuple[set[int], set[int], dict[str, object]] | None:
    """Return one exact odd-triangle no-good for a complete support."""
    if selected_entries & structural_zero_entries:
        raise ValueError("selected support contains a structural zero")
    selected_mask = np.zeros(system.variable_count, dtype=bool)
    selected_mask[list(selected_entries)] = True
    active_matrix = np.all(selected_mask[system.variable_ids], axis=2)
    activities = [
        set(map(int, np.flatnonzero(active_matrix[:, equation_index])))
        for equation_index in range(len(system.colourings))
    ]
    certificates = odd_binomial_triangle_certificates(
        system,
        list(range(len(system.colourings))),
        activities,
        maximum_certificates=1,
    )
    if not certificates:
        return None
    certificate = certificates[0]
    equation_indices = list(map(int, certificate["equation_indices"]))
    matching_pairs = [
        set(map(int, pair))
        for pair in certificate["matching_indices"]
    ]

    positive: set[int] = set()
    negative: set[int] = set()
    for equation_index, active in zip(
        equation_indices,
        matching_pairs,
        strict=True,
    ):
        for matching_index, raw_factors in enumerate(
            system.variable_ids[:, equation_index, :]
        ):
            factors = list(map(int, raw_factors))
            if matching_index in active:
                if not all(
                    factor in selected_entries for factor in factors
                ):
                    raise AssertionError(
                        "recorded active triangle monomial is zero"
                    )
                positive.update(factors)
                continue
            zero_factors = [
                factor
                for factor in factors
                if factor not in selected_entries
            ]
            if not zero_factors:
                raise AssertionError(
                    "recorded inactive triangle monomial is nonzero"
                )
            if not any(
                factor in structural_zero_entries
                for factor in zero_factors
            ):
                negative.add(min(zero_factors))
    if positive & negative:
        raise AssertionError("triangle cube has contradictory entry signs")
    return positive, negative, certificate
