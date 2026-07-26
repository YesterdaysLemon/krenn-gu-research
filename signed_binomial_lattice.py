"""Exact signed-lattice certificates for hafnian support contradictions.

Every forbidden amplitude with two active monomials gives a Laurent relation
whose exponent-difference vector has value ``-1``.  A unimodular independent
basis of such relations assigns an exact sign to every monomial ratio in its
integer lattice.

Two contradiction modes follow.

* A dependent binomial may demand sign ``-1`` while the basis forces ``+1``.
* In a larger forbidden amplitude, basis relations may cancel all monomial
  classes except one nonzero signed class.

The certificates below retain the integer coordinates, so replay requires
only exact vector arithmetic over the integers.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from prism_laurent_reduction import modular_independent_indices
from search_witness import EquationSystem

SparseVector = tuple[tuple[int, int], ...]


def _dense_monomial_vector(
    system: EquationSystem,
    equation_index: int,
    matching_index: int,
    variable_positions: dict[int, int],
) -> list[int]:
    vector = [0] * len(variable_positions)
    for raw_entry in system.variable_ids[
        matching_index, equation_index, :
    ]:
        entry = int(raw_entry)
        vector[variable_positions[entry]] += 1
    return vector


def _difference(first: Sequence[int], second: Sequence[int]) -> list[int]:
    return [
        int(left) - int(right)
        for left, right in zip(first, second, strict=True)
    ]


def _canonical_dense(vector: Sequence[int]) -> list[int]:
    output = list(map(int, vector))
    negative = [-value for value in output]
    return min(output, negative)


def _sparse(vector: Sequence[int], variables: Sequence[int]) -> SparseVector:
    return tuple(
        (int(variables[position]), int(coefficient))
        for position, coefficient in enumerate(vector)
        if coefficient
    )


def _basis_data(
    rows: list[list[int]],
) -> tuple[list[int], list[int], Any, Any] | None:
    """Return independent rows, unimodular pivots, matrix and inverse."""
    from sympy import Matrix

    if not rows:
        return None
    independent = modular_independent_indices(rows)
    basis = Matrix([rows[index] for index in independent])
    pivots = modular_independent_indices(
        [list(column) for column in zip(*basis.tolist(), strict=True)]
    )
    pivot_matrix = basis[:, pivots]
    determinant = int(pivot_matrix.det())
    if abs(determinant) != 1:
        exact_matrix = Matrix(rows)
        independent = list(exact_matrix.T.rref()[1])
        basis = exact_matrix[independent, :]
        pivots = list(basis.rref()[1])
        pivot_matrix = basis[:, pivots]
        determinant = int(pivot_matrix.det())
        if abs(determinant) != 1:
            return None
    inverse = pivot_matrix.inv()
    if any(value.q != 1 for value in inverse):
        return None
    return independent, pivots, basis, inverse


def _coordinates(
    vector: Sequence[int],
    pivots: Sequence[int],
    basis: Any,
    inverse: Any,
) -> list[int] | None:
    from sympy import Matrix

    pivot_part = Matrix(
        [[int(vector[position]) for position in pivots]]
    )
    raw = pivot_part * inverse
    if any(value.q != 1 for value in raw):
        return None
    coordinates = [int(value) for value in raw.row(0)]
    reconstructed = Matrix([coordinates]) * basis
    if list(map(int, reconstructed.row(0))) != list(map(int, vector)):
        return None
    return coordinates


def _coordinate_record(
    coordinates: Sequence[int],
    basis_records: Sequence[dict[str, object]],
) -> list[dict[str, int]]:
    return [
        {
            "basis_equation_index": int(
                basis_records[position]["equation_index"]
            ),
            "coefficient": int(coefficient),
        }
        for position, coefficient in enumerate(coordinates)
        if coefficient
    ]


def signed_binomial_lattice_certificates(
    system: EquationSystem,
    equation_indices: Sequence[int],
    active_matchings: Sequence[set[int]],
    maximum_certificates: int | None = None,
) -> list[dict[str, object]]:
    """Find exact sign-lattice contradictions in decided equations."""
    if len(equation_indices) != len(active_matchings):
        raise ValueError("equation/activity collections have different sizes")
    if maximum_certificates is not None and maximum_certificates < 1:
        raise ValueError("maximum_certificates must be positive")

    activity_by_equation = {
        int(equation): set(map(int, activity))
        for equation, activity in zip(
            equation_indices,
            active_matchings,
            strict=True,
        )
    }
    active_entries = sorted(
        {
            int(entry)
            for equation, activity in activity_by_equation.items()
            for matching in activity
            for entry in system.variable_ids[matching, equation, :]
        }
    )
    positions = {
        entry: position for position, entry in enumerate(active_entries)
    }
    monomial_vectors: dict[tuple[int, int], list[int]] = {}

    def monomial(equation: int, matching: int) -> list[int]:
        key = (equation, matching)
        if key not in monomial_vectors:
            monomial_vectors[key] = _dense_monomial_vector(
                system,
                equation,
                matching,
                positions,
            )
        return monomial_vectors[key]

    relations: list[dict[str, object]] = []
    rows: list[list[int]] = []
    for equation in sorted(activity_by_equation):
        activity = activity_by_equation[equation]
        if bool(system.target[equation]) or len(activity) != 2:
            continue
        first, second = sorted(activity)
        vector = _canonical_dense(
            _difference(
                monomial(equation, first),
                monomial(equation, second),
            )
        )
        rows.append(vector)
        relations.append(
            {
                "equation_index": equation,
                "matching_indices": [first, second],
                "vector": vector,
            }
        )
    basis_data = _basis_data(rows)
    if basis_data is None:
        return []
    independent, pivots, basis, inverse = basis_data
    basis_records = [relations[index] for index in independent]
    certificates: list[dict[str, object]] = []

    # A dependent two-term equation with even coordinate parity is already
    # inconsistent: the basis gives ratio +1 but the equation requires -1.
    for relation, vector in zip(relations, rows, strict=True):
        coordinates = _coordinates(vector, pivots, basis, inverse)
        if coordinates is None or sum(coordinates) % 2:
            continue
        used_basis = _coordinate_record(coordinates, basis_records)
        certificates.append(
            {
                "certificate_mode": "inconsistent_binomial_sign",
                "target_equation_index": int(
                    relation["equation_index"]
                ),
                "target_matching_indices": list(
                    map(int, relation["matching_indices"])
                ),
                "basis_relations": [
                    {
                        "equation_index": int(
                            record["equation_index"]
                        ),
                        "matching_indices": list(
                            map(int, record["matching_indices"])
                        ),
                    }
                    for record in basis_records
                    if any(
                        int(item["basis_equation_index"])
                        == int(record["equation_index"])
                        for item in used_basis
                    )
                ],
                "coordinates": used_basis,
            }
        )
        if (
            maximum_certificates is not None
            and len(certificates) >= maximum_certificates
        ):
            return certificates

    # Reduce larger forbidden amplitudes and required nonzero amplitudes into
    # signed lattice cosets.
    for equation in sorted(activity_by_equation):
        activity = sorted(activity_by_equation[equation])
        required_target = bool(system.target[equation])
        if (
            (required_target and not activity)
            or (not required_target and len(activity) < 3)
        ):
            continue
        groups: list[dict[str, Any]] = []
        all_coordinates: list[list[int]] = []
        for matching in activity:
            vector = monomial(equation, matching)
            placed = False
            for group_index, group in enumerate(groups):
                representative = int(group["representative_matching"])
                difference = _difference(
                    vector,
                    monomial(equation, representative),
                )
                coordinates = _coordinates(
                    difference,
                    pivots,
                    basis,
                    inverse,
                )
                if coordinates is None:
                    continue
                sign = -1 if sum(coordinates) % 2 else 1
                group["terms"].append(
                    {
                        "matching_index": matching,
                        "sign": sign,
                        "coordinates": coordinates,
                    }
                )
                group["signed_coefficient"] += sign
                all_coordinates.append(coordinates)
                placed = True
                break
            if placed:
                continue
            groups.append(
                {
                    "representative_matching": matching,
                    "signed_coefficient": 1,
                    "terms": [
                        {
                            "matching_index": matching,
                            "sign": 1,
                            "coordinates": [0] * len(basis_records),
                        }
                    ],
                }
            )
            all_coordinates.append([0] * len(basis_records))

        nonzero_groups = [
            group for group in groups if group["signed_coefficient"]
        ]
        if required_target:
            if nonzero_groups:
                continue
            certificate_mode = "annihilated_nonzero_target"
        elif len(nonzero_groups) == 1:
            certificate_mode = "isolated_signed_monomial_class"
        else:
            continue
        used_positions = {
            position
            for coordinates in all_coordinates
            for position, coefficient in enumerate(coordinates)
            if coefficient
        }
        certificate_groups = []
        for group in groups:
            certificate_groups.append(
                {
                    "representative_matching": int(
                        group["representative_matching"]
                    ),
                    "signed_coefficient": int(
                        group["signed_coefficient"]
                    ),
                    "terms": [
                        {
                            "matching_index": int(term["matching_index"]),
                            "sign": int(term["sign"]),
                            "coordinates": _coordinate_record(
                                term["coordinates"],
                                basis_records,
                            ),
                        }
                        for term in group["terms"]
                    ],
                }
            )
        certificates.append(
            {
                "certificate_mode": certificate_mode,
                "target_equation_index": equation,
                "target_matching_indices": activity,
                **(
                    {}
                    if required_target
                    else {
                        "surviving_coefficient": int(
                            nonzero_groups[0][
                                "signed_coefficient"
                            ]
                        )
                    }
                ),
                "basis_relations": [
                    {
                        "equation_index": int(
                            basis_records[position]["equation_index"]
                        ),
                        "matching_indices": list(
                            map(
                                int,
                                basis_records[position][
                                    "matching_indices"
                                ],
                            )
                        ),
                    }
                    for position in sorted(used_positions)
                ],
                "groups": certificate_groups,
            }
        )
        if (
            maximum_certificates is not None
            and len(certificates) >= maximum_certificates
        ):
            return certificates
    return certificates


def _flat_exponents(
    system: EquationSystem,
    equation: int,
    matching: int,
) -> dict[int, int]:
    output: dict[int, int] = {}
    for raw_entry in system.variable_ids[matching, equation, :]:
        entry = int(raw_entry)
        output[entry] = output.get(entry, 0) + 1
    return output


def _flat_difference(
    first: dict[int, int],
    second: dict[int, int],
) -> dict[int, int]:
    output = dict(first)
    for entry, coefficient in second.items():
        output[entry] = output.get(entry, 0) - coefficient
        if not output[entry]:
            del output[entry]
    return output


def _canonical_flat(vector: dict[int, int]) -> dict[int, int]:
    direct = tuple(sorted(vector.items()))
    negative = tuple(
        (entry, -coefficient) for entry, coefficient in direct
    )
    return dict(min(direct, negative))


def verify_signed_binomial_lattice_certificate(
    system: EquationSystem,
    activity_by_equation: dict[int, set[int]],
    certificate: dict[str, object],
) -> None:
    """Replay one certificate using exact sparse integer arithmetic."""
    basis_vectors: dict[int, dict[int, int]] = {}
    for raw_relation in certificate["basis_relations"]:
        relation = dict(raw_relation)
        equation = int(relation["equation_index"])
        pair = list(map(int, relation["matching_indices"]))
        if bool(system.target[equation]) or len(pair) != 2:
            raise AssertionError("basis relation is not a forbidden binomial")
        if activity_by_equation.get(equation) != set(pair):
            raise AssertionError("basis relation activity changed")
        basis_vectors[equation] = _canonical_flat(
            _flat_difference(
                _flat_exponents(system, equation, pair[0]),
                _flat_exponents(system, equation, pair[1]),
            )
        )

    def coordinate_sum(
        records: Sequence[dict[str, int]],
    ) -> tuple[dict[int, int], int]:
        vector: dict[int, int] = {}
        parity_sum = 0
        seen: set[int] = set()
        for record in records:
            equation = int(record["basis_equation_index"])
            coefficient = int(record["coefficient"])
            if equation in seen:
                raise AssertionError("basis coordinate is repeated")
            seen.add(equation)
            if equation not in basis_vectors or not coefficient:
                raise AssertionError("basis coordinate is invalid")
            parity_sum += coefficient
            for entry, value in basis_vectors[equation].items():
                vector[entry] = (
                    vector.get(entry, 0) + coefficient * value
                )
                if not vector[entry]:
                    del vector[entry]
        return vector, parity_sum

    mode = str(certificate["certificate_mode"])
    target = int(certificate["target_equation_index"])
    target_activity = set(
        map(int, certificate["target_matching_indices"])
    )
    target_is_required = bool(system.target[target])
    if mode == "annihilated_nonzero_target":
        if not target_is_required:
            raise AssertionError("annihilated target is not required")
    elif target_is_required:
        raise AssertionError("lattice contradiction target is not forbidden")
    if activity_by_equation.get(target) != target_activity:
        raise AssertionError("lattice target activity changed")

    if mode == "inconsistent_binomial_sign":
        if len(target_activity) != 2:
            raise AssertionError("sign target is not binomial")
        first, second = map(
            int, certificate["target_matching_indices"]
        )
        target_vector = _canonical_flat(
            _flat_difference(
                _flat_exponents(system, target, first),
                _flat_exponents(system, target, second),
            )
        )
        reconstructed, parity_sum = coordinate_sum(
            certificate["coordinates"]
        )
        if reconstructed != target_vector:
            raise AssertionError("binomial sign coordinates changed")
        if parity_sum % 2:
            raise AssertionError("binomial sign relation is consistent")
        return

    if mode not in {
        "isolated_signed_monomial_class",
        "annihilated_nonzero_target",
    }:
        raise AssertionError(f"unknown lattice certificate mode {mode}")
    seen_matchings: set[int] = set()
    nonzero_coefficients: list[int] = []
    for raw_group in certificate["groups"]:
        group = dict(raw_group)
        representative = int(group["representative_matching"])
        if representative not in target_activity:
            raise AssertionError("group representative is not active")
        signed_coefficient = 0
        for raw_term in group["terms"]:
            term = dict(raw_term)
            matching = int(term["matching_index"])
            if matching in seen_matchings or matching not in target_activity:
                raise AssertionError("group term partition changed")
            seen_matchings.add(matching)
            reconstructed, parity_sum = coordinate_sum(
                term["coordinates"]
            )
            expected = _flat_difference(
                _flat_exponents(system, target, matching),
                _flat_exponents(system, target, representative),
            )
            if reconstructed != expected:
                raise AssertionError("group coordinates changed")
            sign = int(term["sign"])
            if sign not in (-1, 1) or sign != (
                -1 if parity_sum % 2 else 1
            ):
                raise AssertionError("group term sign changed")
            signed_coefficient += sign
        if signed_coefficient != int(group["signed_coefficient"]):
            raise AssertionError("group signed coefficient changed")
        if signed_coefficient:
            nonzero_coefficients.append(signed_coefficient)
    if seen_matchings != target_activity:
        raise AssertionError("group terms do not partition target activity")
    if mode == "annihilated_nonzero_target":
        if nonzero_coefficients:
            raise AssertionError("required target is not annihilated")
    else:
        if len(nonzero_coefficients) != 1:
            raise AssertionError("certificate does not isolate one class")
        if nonzero_coefficients[0] != int(
            certificate["surviving_coefficient"]
        ):
            raise AssertionError("surviving coefficient changed")


def signed_lattice_used_equations(
    certificate: dict[str, object],
) -> list[int]:
    return sorted(
        {
            int(certificate["target_equation_index"]),
            *(
                int(relation["equation_index"])
                for relation in certificate["basis_relations"]
            ),
        }
    )


def cube_verify_signed_binomial_lattice_certificate(
    system: EquationSystem,
    equation_indices: Sequence[int],
    positive_entries: set[int],
    zero_entries: set[int],
    certificate: dict[str, object],
) -> None:
    """Verify that a support cube decides and proves one lattice conflict."""
    from cancellation_transport import decided_cube_activity

    retained, _colourings, activities = decided_cube_activity(
        system,
        equation_indices,
        positive_entries,
        zero_entries,
    )
    activity = {
        equation: active
        for equation, active in zip(retained, activities, strict=True)
    }
    used = signed_lattice_used_equations(certificate)
    if any(equation not in activity for equation in used):
        raise AssertionError("lattice certificate equation is not cube-decided")
    verify_signed_binomial_lattice_certificate(
        system,
        {equation: activity[equation] for equation in used},
        certificate,
    )


def support_signed_binomial_lattice_conflict(
    system: EquationSystem,
    selected_entries: set[int],
    structural_zero_entries: set[int],
) -> tuple[set[int], set[int], dict[str, object]] | None:
    """Return one exact signed-lattice no-good for a complete support."""
    import numpy as np

    if selected_entries & structural_zero_entries:
        raise ValueError("selected support contains a structural zero")
    selected_mask = np.zeros(system.variable_count, dtype=bool)
    selected_mask[list(selected_entries)] = True
    active_matrix = np.all(selected_mask[system.variable_ids], axis=2)
    equations = list(range(len(system.colourings)))
    activities = [
        set(map(int, np.flatnonzero(active_matrix[:, equation])))
        for equation in equations
    ]
    certificates = signed_binomial_lattice_certificates(
        system,
        equations,
        activities,
        maximum_certificates=1,
    )
    if not certificates:
        return None
    certificate = certificates[0]
    used = signed_lattice_used_equations(certificate)
    active_by_equation = {
        equation: activities[equation] for equation in used
    }
    verify_signed_binomial_lattice_certificate(
        system,
        active_by_equation,
        certificate,
    )

    positive: set[int] = set()
    negative: set[int] = set()
    for equation in used:
        active = active_by_equation[equation]
        for matching, raw_factors in enumerate(
            system.variable_ids[:, equation, :]
        ):
            factors = list(map(int, raw_factors))
            if matching in active:
                if not all(
                    factor in selected_entries for factor in factors
                ):
                    raise AssertionError(
                        "recorded active lattice monomial is zero"
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
                    "recorded inactive lattice monomial is nonzero"
                )
            if not any(
                factor in structural_zero_entries
                for factor in zero_factors
            ):
                negative.add(min(zero_factors))
    if positive & negative:
        raise AssertionError("lattice cube has contradictory entry signs")
    return positive, negative, certificate
