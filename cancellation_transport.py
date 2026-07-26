"""Exact cancellation-transport certificates for matching tensors.

Suppose two forbidden colourings differ only at a vertex ``x``.  If every
active matching of the second colouring is also active at the first and all
of those matchings pair ``x`` with the same neighbour ``y``, their monomials
are multiplied by one common nonzero edge-entry ratio when the colour at
``x`` changes.  Hence their partial sum vanishes at both colourings.  If the
first colouring has exactly one further active matching, its nonzero
monomial is forced to vanish, a contradiction.

This module also detects a two-monomial rectangle certificate.  If the same
two nonzero, vertex-separable matching monomials are the only survivors at
four colourings obtained by independently changing two vertices, then the
four amplitudes form a sum of two full-support rank-one 2 by 2 matrices.
Vanishing at three corners forces the fourth corner to vanish.  This
contradicts a nonzero monochromatic target.

Both certificates are exact and use no numerical approximations.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Sequence

import numpy as np

from search_witness import EquationSystem

Matching = tuple[tuple[int, int], ...]


def matching_partner(matching: Matching, vertex: int) -> int:
    """Return the unique vertex paired with ``vertex`` in ``matching``."""
    for first, second in matching:
        if first == vertex:
            return second
        if second == vertex:
            return first
    raise ValueError(f"vertex {vertex} is absent from the matching")


def matching_difference_components(
    first: Matching,
    second: Matching,
) -> list[set[int]]:
    """Return the alternating-cycle vertex sets in ``first triangle second``."""
    difference = set(first) ^ set(second)
    adjacency: dict[int, set[int]] = {}
    for left, right in difference:
        adjacency.setdefault(left, set()).add(right)
        adjacency.setdefault(right, set()).add(left)
    components: list[set[int]] = []
    unseen = set(adjacency)
    while unseen:
        root = min(unseen)
        stack = [root]
        component: set[int] = set()
        while stack:
            vertex = stack.pop()
            if vertex in component:
                continue
            component.add(vertex)
            stack.extend(adjacency[vertex] - component)
        unseen -= component
        components.append(component)
    return sorted(
        components,
        key=lambda component: (len(component), min(component)),
    )


def cancellation_transport_certificates(
    colourings: Sequence[Sequence[int]],
    active_matchings: Sequence[set[int]],
    matchings: Sequence[Matching],
    zero_targets: Sequence[bool] | None = None,
    maximum_certificates: int | None = None,
) -> list[dict[str, object]]:
    """Find all directed one-vertex cancellation-transport certificates."""
    if len(colourings) != len(active_matchings):
        raise ValueError("colourings and active_matchings have different sizes")
    if zero_targets is None:
        zero_targets = [True] * len(colourings)
    if len(zero_targets) != len(colourings):
        raise ValueError("zero_targets has the wrong size")
    if maximum_certificates is not None and maximum_certificates < 1:
        raise ValueError("maximum_certificates must be positive")
    canonical_colourings = [tuple(map(int, row)) for row in colourings]
    if len(set(canonical_colourings)) != len(canonical_colourings):
        raise ValueError("colourings must be distinct")
    width = len(canonical_colourings[0]) if canonical_colourings else 0
    if any(len(row) != width for row in canonical_colourings):
        raise ValueError("colourings have different widths")
    position_by_colouring = {
        colouring: position
        for position, colouring in enumerate(canonical_colourings)
    }
    values_by_vertex = [
        sorted({colouring[vertex] for colouring in canonical_colourings})
        for vertex in range(width)
    ]

    certificates: list[dict[str, object]] = []
    for source_index, source in enumerate(canonical_colourings):
        if not zero_targets[source_index]:
            continue
        source_active = active_matchings[source_index]
        for vertex in range(width):
            for transported_value in values_by_vertex[vertex]:
                if transported_value == source[vertex]:
                    continue
                transported = (
                    source[:vertex]
                    + (transported_value,)
                    + source[vertex + 1 :]
                )
                transport_index = position_by_colouring.get(transported)
                if transport_index is None or not zero_targets[transport_index]:
                    continue
                transported_active = active_matchings[transport_index]
                if (
                    not transported_active
                    or not transported_active < source_active
                ):
                    continue
                remainder = source_active - transported_active
                if len(remainder) != 1:
                    continue
                partners = {
                    matching_partner(matchings[index], vertex)
                    for index in transported_active
                }
                if len(partners) != 1:
                    continue
                certificates.append(
                    {
                        "source_position": source_index,
                        "transport_position": transport_index,
                        "changed_vertex": vertex,
                        "common_neighbour": next(iter(partners)),
                        "shared_matching_indices": sorted(
                            map(int, transported_active)
                        ),
                        "isolated_matching_index": int(
                            next(iter(remainder))
                        ),
                    }
                )
                if (
                    maximum_certificates is not None
                    and len(certificates) >= maximum_certificates
                ):
                    return certificates
    return certificates


def decided_cube_activity(
    system: EquationSystem,
    equation_indices: Iterable[int],
    positive_entries: set[int],
    zero_entries: set[int],
) -> tuple[list[int], list[tuple[int, ...]], list[set[int]]]:
    """Reconstruct exact active matching sets fixed by a support cube.

    An equation is retained only when every matching monomial is decided:
    it either contains a known-zero entry or all of its entries are known
    nonzero.  Sound learned Laurent cubes have this property for every
    equation they record.
    """
    retained: list[int] = []
    colourings: list[tuple[int, ...]] = []
    activities: list[set[int]] = []
    for raw_index in equation_indices:
        equation_index = int(raw_index)
        active: set[int] = set()
        decided = True
        for matching_index, factors in enumerate(
            system.variable_ids[:, equation_index, :]
        ):
            factor_set = {int(factor) for factor in factors}
            if factor_set & zero_entries:
                continue
            if factor_set <= positive_entries:
                active.add(matching_index)
                continue
            decided = False
            break
        if decided:
            retained.append(equation_index)
            colourings.append(
                tuple(int(value) for value in system.colourings[equation_index])
            )
            activities.append(active)
    return retained, colourings, activities


def cube_cancellation_transport_certificates(
    system: EquationSystem,
    equation_indices: Iterable[int],
    positive_entries: set[int],
    zero_entries: set[int],
) -> list[dict[str, object]]:
    """Find transport certificates whose entry statuses are fixed by a cube."""
    retained, colourings, activities = decided_cube_activity(
        system,
        equation_indices,
        positive_entries,
        zero_entries,
    )
    target_zero = [
        not bool(system.target[equation_index]) for equation_index in retained
    ]
    certificates = cancellation_transport_certificates(
        colourings,
        activities,
        system.matchings,
        target_zero,
    )
    for certificate in certificates:
        source_position = int(certificate.pop("source_position"))
        transport_position = int(certificate.pop("transport_position"))
        source_equation = retained[source_position]
        transport_equation = retained[transport_position]
        vertex = int(certificate["changed_vertex"])
        neighbour = int(certificate["common_neighbour"])
        shared = list(map(int, certificate["shared_matching_indices"]))

        source_factors: set[int] = set()
        transport_factors: set[int] = set()
        edge = (min(vertex, neighbour), max(vertex, neighbour))
        for matching_index in shared:
            matching = system.matchings[matching_index]
            pair_position = matching.index(edge)
            source_factors.add(
                int(
                    system.variable_ids[
                        matching_index, source_equation, pair_position
                    ]
                )
            )
            transport_factors.add(
                int(
                    system.variable_ids[
                        matching_index, transport_equation, pair_position
                    ]
                )
            )
        if len(source_factors) != 1 or len(transport_factors) != 1:
            raise AssertionError("transport ratio is not common")
        source_entry = next(iter(source_factors))
        transport_entry = next(iter(transport_factors))
        if (
            source_entry not in positive_entries
            or transport_entry not in positive_entries
        ):
            raise AssertionError("transport ratio is not explicitly nonzero")
        certificate.update(
            {
                "source_equation_index": source_equation,
                "transport_equation_index": transport_equation,
                "source_colouring": list(colourings[source_position]),
                "transport_colouring": list(colourings[transport_position]),
                "source_ratio_entry": source_entry,
                "transport_ratio_entry": transport_entry,
            }
        )
    return certificates


def _rectangle_certificates_on_decided_equations(
    system: EquationSystem,
    equation_indices: Sequence[int],
    active_matchings: Sequence[set[int]],
    maximum_certificates: int | None = None,
    accept_certificate: Callable[[dict[str, object]], bool] | None = None,
) -> list[dict[str, object]]:
    """Find two-monomial rectangles in a decided equation collection."""
    if len(equation_indices) != len(active_matchings):
        raise ValueError("equation/activity collections have different sizes")
    if maximum_certificates is not None and maximum_certificates < 1:
        raise ValueError("maximum_certificates must be positive")
    positions = {
        tuple(
            int(value) for value in system.colourings[equation_index]
        ): position
        for position, equation_index in enumerate(equation_indices)
    }
    certificates: list[dict[str, object]] = []
    # Rectangle transport: three forbidden corners have the same two active
    # separable monomials.  Their cancellations force those two monomials
    # to cancel at the fourth forbidden corner too, where one additional
    # active monomial is then isolated.
    for source_position, source_equation in enumerate(equation_indices):
        if bool(system.target[source_equation]):
            continue
        source_colouring = tuple(
            int(value) for value in system.colourings[source_equation]
        )
        source_active = active_matchings[source_position]
        if len(source_active) != 3:
            continue
        for first_vertex in range(system.n):
            for second_vertex in range(first_vertex + 1, system.n):
                changed_edge = (first_vertex, second_vertex)
                for first_colour in range(system.d):
                    if first_colour == source_colouring[first_vertex]:
                        continue
                    first_changed = list(source_colouring)
                    first_changed[first_vertex] = first_colour
                    first_position = positions.get(tuple(first_changed))
                    if first_position is None:
                        continue
                    first_equation = equation_indices[first_position]
                    if bool(system.target[first_equation]):
                        continue
                    for second_colour in range(system.d):
                        if second_colour == source_colouring[second_vertex]:
                            continue
                        second_changed = list(source_colouring)
                        second_changed[second_vertex] = second_colour
                        second_position = positions.get(
                            tuple(second_changed)
                        )
                        if second_position is None:
                            continue
                        both_changed = list(first_changed)
                        both_changed[second_vertex] = second_colour
                        both_position = positions.get(
                            tuple(both_changed)
                        )
                        if both_position is None:
                            continue
                        second_equation = equation_indices[
                            second_position
                        ]
                        both_equation = equation_indices[both_position]
                        if bool(system.target[second_equation]) or bool(
                            system.target[both_equation]
                        ):
                            continue
                        shared = active_matchings[first_position]
                        if (
                            len(shared) != 2
                            or active_matchings[second_position] != shared
                            or active_matchings[both_position] != shared
                            or not shared < source_active
                            or len(source_active - shared) != 1
                            or any(
                                changed_edge
                                in system.matchings[matching_index]
                                for matching_index in shared
                            )
                        ):
                            continue
                        positions_in_order = (
                            source_position,
                            first_position,
                            second_position,
                            both_position,
                        )
                        candidate = {
                            "certificate_mode": "isolated_forbidden",
                            "source_equation_index": int(
                                source_equation
                            ),
                            "corner_equation_indices": [
                                int(equation_indices[position])
                                for position in positions_in_order
                            ],
                            "source_colouring": list(source_colouring),
                            "changed_vertices": [
                                first_vertex,
                                second_vertex,
                            ],
                            "alternative_colours": [
                                first_colour,
                                second_colour,
                            ],
                            "matching_indices": sorted(map(int, shared)),
                            "isolated_matching_index": int(
                                next(iter(source_active - shared))
                            ),
                        }
                        if (
                            accept_certificate is not None
                            and not accept_certificate(candidate)
                        ):
                            continue
                        certificates.append(candidate)
                        if (
                            maximum_certificates is not None
                            and len(certificates)
                            >= maximum_certificates
                        ):
                            return certificates

    # Nonzero-target rectangle: all four corners have the same two active
    # separable monomials.  Three forbidden zeros force the required
    # monochromatic corner to vanish.
    for target_position, target_equation in enumerate(equation_indices):
        if not bool(system.target[target_equation]):
            continue
        target_colouring = tuple(
            int(value) for value in system.colourings[target_equation]
        )
        if len(set(target_colouring)) != 1:
            continue
        base_colour = target_colouring[0]
        target_active = active_matchings[target_position]
        if len(target_active) != 2:
            continue
        for first_vertex in range(system.n):
            for second_vertex in range(first_vertex + 1, system.n):
                changed_edge = (first_vertex, second_vertex)
                if any(
                    changed_edge in system.matchings[matching_index]
                    for matching_index in target_active
                ):
                    continue
                for first_colour in range(system.d):
                    if first_colour == base_colour:
                        continue
                    first_changed = list(target_colouring)
                    first_changed[first_vertex] = first_colour
                    first_position = positions.get(tuple(first_changed))
                    if first_position is None:
                        continue
                    first_equation = equation_indices[first_position]
                    if bool(system.target[first_equation]):
                        continue
                    for second_colour in range(system.d):
                        if second_colour == base_colour:
                            continue
                        second_changed = list(target_colouring)
                        second_changed[second_vertex] = second_colour
                        second_position = positions.get(
                            tuple(second_changed)
                        )
                        if second_position is None:
                            continue
                        both_changed = list(first_changed)
                        both_changed[second_vertex] = second_colour
                        both_position = positions.get(
                            tuple(both_changed)
                        )
                        if both_position is None:
                            continue
                        second_equation = equation_indices[
                            second_position
                        ]
                        both_equation = equation_indices[both_position]
                        if bool(system.target[second_equation]) or bool(
                            system.target[both_equation]
                        ):
                            continue
                        positions_in_order = (
                            target_position,
                            first_position,
                            second_position,
                            both_position,
                        )
                        if any(
                            active_matchings[position] != target_active
                            for position in positions_in_order[1:]
                        ):
                            continue
                        candidate = {
                            "certificate_mode": "nonzero_target",
                            "target_equation_index": int(
                                target_equation
                            ),
                            "corner_equation_indices": [
                                int(equation_indices[position])
                                for position in positions_in_order
                            ],
                            "target_colouring": list(target_colouring),
                            "changed_vertices": [
                                first_vertex,
                                second_vertex,
                            ],
                            "alternative_colours": [
                                first_colour,
                                second_colour,
                            ],
                            "matching_indices": sorted(
                                map(int, target_active)
                            ),
                        }
                        if (
                            accept_certificate is not None
                            and not accept_certificate(candidate)
                        ):
                            continue
                        certificates.append(candidate)
                        if (
                            maximum_certificates is not None
                            and len(certificates)
                            >= maximum_certificates
                        ):
                            return certificates
    return certificates


def cube_two_monomial_rectangle_certificates(
    system: EquationSystem,
    equation_indices: Iterable[int],
    positive_entries: set[int],
    zero_entries: set[int],
) -> list[dict[str, object]]:
    """Replay rectangle certificates whose four amplitudes are cube-decided."""
    retained, _colourings, activities = decided_cube_activity(
        system,
        equation_indices,
        positive_entries,
        zero_entries,
    )
    return _rectangle_certificates_on_decided_equations(
        system,
        retained,
        activities,
    )


def support_two_monomial_rectangle_conflict(
    system: EquationSystem,
    selected_entries: set[int],
    structural_zero_entries: set[int],
) -> tuple[set[int], set[int], dict[str, object]] | None:
    """Return one exact two-monomial rectangle no-good for a full support."""
    if selected_entries & structural_zero_entries:
        raise ValueError("selected support contains a structural zero")
    selected_mask = np.zeros(system.variable_count, dtype=bool)
    selected_mask[list(selected_entries)] = True
    active_matrix = np.all(selected_mask[system.variable_ids], axis=2)
    activities = [
        set(map(int, np.flatnonzero(active_matrix[:, equation_index])))
        for equation_index in range(len(system.colourings))
    ]

    def is_singleton_exchange(
        certificate: dict[str, object],
    ) -> bool:
        if certificate["certificate_mode"] != "isolated_forbidden":
            return False
        changed_vertices = list(
            map(int, certificate["changed_vertices"])
        )
        changed_edge = tuple(sorted(changed_vertices))
        isolated_index = int(certificate["isolated_matching_index"])
        isolated_matching = system.matchings[isolated_index]
        if changed_edge not in isolated_matching:
            return False
        source_colouring = list(
            map(int, certificate["source_colouring"])
        )
        left, right = changed_edge
        if source_colouring[left] != source_colouring[right]:
            return False
        block_offset = (
            system.edge_index[changed_edge] * system.d * system.d
        )
        block_support = {
            entry - block_offset
            for entry in selected_entries
            if block_offset
            <= entry
            < block_offset + system.d * system.d
        }
        source_entry = (
            source_colouring[left] * system.d
            + source_colouring[right]
        )
        if block_support != {source_entry}:
            return False
        shared_indices = list(map(int, certificate["matching_indices"]))
        shared_matchings = [
            system.matchings[index] for index in shared_indices
        ]
        shared_components = matching_difference_components(
            shared_matchings[0],
            shared_matchings[1],
        )
        if len(shared_components) != 1:
            return False
        changed_set = set(changed_vertices)
        return any(
            len(components) == 1
            and len(components[0]) == 4
            and changed_set <= components[0]
            for components in (
                matching_difference_components(
                    isolated_matching,
                    shared_matchings[0],
                ),
                matching_difference_components(
                    isolated_matching,
                    shared_matchings[1],
                ),
            )
        )

    certificate_list = _rectangle_certificates_on_decided_equations(
        system,
        list(range(len(system.colourings))),
        activities,
        maximum_certificates=1,
        accept_certificate=is_singleton_exchange,
    )
    if not certificate_list:
        certificate_list = _rectangle_certificates_on_decided_equations(
            system,
            list(range(len(system.colourings))),
            activities,
            maximum_certificates=1,
        )
    if not certificate_list:
        return None
    certificate = certificate_list[0]
    used_equations = set(
        map(int, certificate["corner_equation_indices"])
    )
    shared = set(map(int, certificate["matching_indices"]))
    isolated = certificate.get("isolated_matching_index")
    source_equation = certificate.get("source_equation_index")

    positive: set[int] = set()
    negative: set[int] = set()
    for equation_index in used_equations:
        active = set(shared)
        if (
            isolated is not None
            and source_equation is not None
            and equation_index == int(source_equation)
        ):
            active.add(int(isolated))
        for matching_index, raw_factors in enumerate(
            system.variable_ids[:, equation_index, :]
        ):
            factors = list(map(int, raw_factors))
            if matching_index in active:
                if not all(
                    factor in selected_entries for factor in factors
                ):
                    raise AssertionError(
                        "recorded rectangle monomial is zero"
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
                    "recorded inactive rectangle monomial is nonzero"
                )
            if not any(
                factor in structural_zero_entries
                for factor in zero_factors
            ):
                negative.add(min(zero_factors))
    if positive & negative:
        raise AssertionError("rectangle cube has contradictory entry signs")
    return positive, negative, certificate


def support_cancellation_transport_conflict(
    system: EquationSystem,
    selected_entries: set[int],
    structural_zero_entries: set[int],
) -> tuple[set[int], set[int], dict[str, object]] | None:
    """Return one small exact transport no-good for a complete support.

    ``selected_entries`` is the full set of nonzero entries in a SAT model.
    Structural zeros are omitted from the learned cube because they are
    already fixed by the base formula.
    """
    if selected_entries & structural_zero_entries:
        raise ValueError("selected support contains a structural zero")
    selected_mask = np.zeros(system.variable_count, dtype=bool)
    selected_mask[list(selected_entries)] = True
    active_matrix = np.all(selected_mask[system.variable_ids], axis=2)
    activities = [
        set(map(int, np.flatnonzero(active_matrix[:, equation_index])))
        for equation_index in range(len(system.colourings))
    ]
    colourings = [
        tuple(map(int, colouring)) for colouring in system.colourings
    ]
    certificates = cancellation_transport_certificates(
        colourings,
        activities,
        system.matchings,
        [not bool(value) for value in system.target],
        maximum_certificates=1,
    )
    if not certificates:
        return None
    certificate = certificates[0]
    source_equation = int(certificate.pop("source_position"))
    transport_equation = int(certificate.pop("transport_position"))
    shared = set(map(int, certificate["shared_matching_indices"]))
    isolated = int(certificate["isolated_matching_index"])
    active_by_equation = {
        source_equation: shared | {isolated},
        transport_equation: shared,
    }

    positive: set[int] = set()
    negative: set[int] = set()
    for equation_index, active in active_by_equation.items():
        for matching_index, raw_factors in enumerate(
            system.variable_ids[:, equation_index, :]
        ):
            factors = list(map(int, raw_factors))
            if matching_index in active:
                if not all(factor in selected_entries for factor in factors):
                    raise AssertionError("recorded active monomial is zero")
                positive.update(factors)
                continue
            zero_factors = [
                factor
                for factor in factors
                if factor not in selected_entries
            ]
            if not zero_factors:
                raise AssertionError("recorded inactive monomial is nonzero")
            if not any(
                factor in structural_zero_entries for factor in zero_factors
            ):
                negative.add(min(zero_factors))
    if positive & negative:
        raise AssertionError("transport cube has contradictory entry signs")

    vertex = int(certificate["changed_vertex"])
    neighbour = int(certificate["common_neighbour"])
    edge = (min(vertex, neighbour), max(vertex, neighbour))
    source_ratio_entries: set[int] = set()
    transport_ratio_entries: set[int] = set()
    for matching_index in shared:
        pair_position = system.matchings[matching_index].index(edge)
        source_ratio_entries.add(
            int(
                system.variable_ids[
                    matching_index, source_equation, pair_position
                ]
            )
        )
        transport_ratio_entries.add(
            int(
                system.variable_ids[
                    matching_index, transport_equation, pair_position
                ]
            )
        )
    if (
        len(source_ratio_entries) != 1
        or len(transport_ratio_entries) != 1
    ):
        raise AssertionError("transport ratio is not common")
    source_ratio = next(iter(source_ratio_entries))
    transport_ratio = next(iter(transport_ratio_entries))
    if source_ratio not in positive or transport_ratio not in positive:
        raise AssertionError("transport ratio is not fixed nonzero")

    certificate.update(
        {
            "source_equation_index": source_equation,
            "transport_equation_index": transport_equation,
            "source_colouring": list(colourings[source_equation]),
            "transport_colouring": list(colourings[transport_equation]),
            "source_ratio_entry": source_ratio,
            "transport_ratio_entry": transport_ratio,
        }
    )
    return positive, negative, certificate
