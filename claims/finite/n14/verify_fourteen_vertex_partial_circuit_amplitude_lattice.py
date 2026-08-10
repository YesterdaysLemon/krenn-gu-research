"""Independently replay one partial-circuit amplitude contradiction."""

from __future__ import annotations
import sys as _bootstrap_sys
from pathlib import Path as _BootstrapPath

for _bootstrap_parent in _BootstrapPath(__file__).resolve().parents:
    if (_bootstrap_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        _bootstrap_sys.path.insert(0, str(_bootstrap_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap as _bootstrap_repository  # noqa: E402

REPO_ROOT, HERE = _bootstrap_repository(__file__)


import argparse
import hashlib
import itertools
import json
from collections import Counter
from functools import lru_cache
from pathlib import Path
from typing import Sequence


N = 14
Edge = tuple[int, int]
Factor = tuple[Edge, ...]
ALL_EDGES = tuple(itertools.combinations(range(N), 2))
EDGE_INDEX = {item: index for index, item in enumerate(ALL_EDGES)}


def edge(first: int, second: int) -> Edge:
    return tuple(sorted((int(first), int(second))))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def cycles_for(lengths: Sequence[int]) -> tuple[tuple[int, ...], ...]:
    output = []
    start = 0
    for raw_length in lengths:
        length = int(raw_length)
        output.append(tuple(range(start, start + length)))
        start += length
    if start != N:
        raise AssertionError("partition stopped covering 14 vertices")
    return tuple(output)


def cycle_edges(cycle: Sequence[int]) -> frozenset[Edge]:
    return frozenset(
        edge(cycle[index], cycle[(index + 1) % len(cycle)])
        for index in range(len(cycle))
    )


def perfect_matchings(allowed: set[Edge]) -> list[Factor]:
    adjacency = {vertex: set() for vertex in range(N)}
    for first, second in allowed:
        adjacency[first].add(second)
        adjacency[second].add(first)

    @lru_cache(maxsize=None)
    def visit(remaining: int) -> tuple[Factor, ...]:
        if not remaining:
            return ((),)
        first_bit = remaining & -remaining
        first = first_bit.bit_length() - 1
        candidates = remaining ^ first_bit
        output = []
        while candidates:
            second_bit = candidates & -candidates
            candidates ^= second_bit
            second = second_bit.bit_length() - 1
            item = edge(first, second)
            if item not in allowed:
                continue
            for suffix in visit(
                remaining ^ first_bit ^ second_bit
            ):
                output.append((item, *suffix))
        return tuple(output)

    return sorted(visit((1 << N) - 1))


def feasible_on_cycle(cycle: Sequence[int], deleted: set[int]) -> bool:
    positions = [
        index for index, vertex in enumerate(cycle) if vertex in deleted
    ]
    if not positions:
        return True
    return all(
        (
            positions[(index + 1) % len(positions)] - positions[index]
        )
        % len(cycle)
        % 2
        for index in range(len(positions))
    )


def active_singleton_edges(
    colouring: Sequence[int], labels: dict[Edge, int]
) -> frozenset[Edge]:
    return frozenset(
        item
        for item, colour in labels.items()
        if colouring[item[0]] == colouring[item[1]] == colour
    )


def active_matching_ids(
    matchings: Sequence[Factor],
    colouring: Sequence[int],
    full_edges: set[Edge],
    labels: dict[Edge, int],
) -> tuple[int, ...]:
    return tuple(
        matching_id
        for matching_id, matching in enumerate(matchings)
        if all(
            item in full_edges
            or (
                colouring[item[0]]
                == colouring[item[1]]
                == labels[item]
            )
            for item in matching
        )
    )


def monomial(
    matching: Factor,
    colouring: Sequence[int],
    full_edges: set[Edge],
    labels: dict[Edge, int],
) -> Counter[int]:
    output: Counter[int] = Counter()
    for item in matching:
        if item in full_edges:
            first_colour = int(colouring[item[0]])
            second_colour = int(colouring[item[1]])
        else:
            first_colour = second_colour = labels[item]
        output[
            9 * EDGE_INDEX[item]
            + 3 * first_colour
            + second_colour
        ] += 1
    return output


def canonical(counter: Counter[int]) -> tuple[tuple[int, int], ...]:
    direct = tuple(
        sorted(
            (variable, coefficient)
            for variable, coefficient in counter.items()
            if coefficient
        )
    )
    negative = tuple(
        (variable, -coefficient)
        for variable, coefficient in direct
    )
    return min(direct, negative)


def direct_sparse(counter: Counter[int]) -> tuple[tuple[int, int], ...]:
    return tuple(
        sorted(
            (variable, coefficient)
            for variable, coefficient in counter.items()
            if coefficient
        )
    )


def reported_relation(
    raw: Sequence[Sequence[object]],
) -> tuple[tuple[int, int], ...]:
    counter: Counter[int] = Counter()
    for raw_variable, raw_coefficient in raw:
        text = str(raw_variable)
        prefix, colours = text.rsplit(":a", 1)
        raw_edge = prefix.removeprefix("W:")
        first, second = map(int, raw_edge.split("-"))
        first_colour, second_colour = map(
            int, colours.split(":b")
        )
        variable = (
            9 * EDGE_INDEX[edge(first, second)]
            + 3 * first_colour
            + second_colour
        )
        counter[variable] += int(raw_coefficient)
    return canonical(counter)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("partial_analysis", type=Path)
    parser.add_argument("amplitude_analysis", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    partial = json.loads(
        args.partial_analysis.read_text(encoding="utf-8")
    )
    amplitude = json.loads(
        args.amplitude_analysis.read_text(encoding="utf-8")
    )
    if amplitude.get("status") != "contradiction":
        raise AssertionError("amplitude analysis claims no contradiction")
    if Path(amplitude["partial_analysis"]) != args.partial_analysis:
        raise AssertionError("amplitude analysis is bound elsewhere")
    certificate = amplitude["certificate"]
    if (
        certificate.get("certificate_mode")
        != "isolated_partial_circuit_lattice_class"
    ):
        raise AssertionError("unsupported certificate mode")

    partition = tuple(map(int, partial["partition"]))
    cycles = cycles_for(partition)
    full_edges = set().union(
        *(cycle_edges(cycle) for cycle in cycles)
    )
    factors = tuple(
        tuple(edge(*map(int, item)) for item in factor)
        for factor in partial["singleton_factors"]
    )
    if len(factors) != 3:
        raise AssertionError("singleton factor count changed")
    singleton_edges: set[Edge] = set()
    for factor in factors:
        if len(factor) != N // 2:
            raise AssertionError("singleton factor size changed")
        if {
            vertex for item in factor for vertex in item
        } != set(range(N)):
            raise AssertionError("singleton factor stopped perfect")
        if singleton_edges & set(factor):
            raise AssertionError("singleton factors overlap")
        singleton_edges.update(factor)
    if singleton_edges & full_edges:
        raise AssertionError("singleton factor overlaps full factor")
    labels = {
        item: colour
        for colour, factor in enumerate(factors)
        for item in factor
    }
    matchings = perfect_matchings(full_edges | singleton_edges)
    if len(matchings) != int(amplitude["skeleton_perfect_matchings"]):
        raise AssertionError("skeleton matching census changed")
    full_only_ids = {
        matching_id
        for matching_id, matching in enumerate(matchings)
        if set(matching) <= full_edges
    }
    if len(full_only_ids) != 2 ** len(cycles):
        raise AssertionError("full-only matching count changed")

    basis_ids = list(map(int, amplitude["basis_relation_ids"]))
    if not basis_ids:
        raise AssertionError("certificate uses no mandatory relation")
    used_basis_ids = list(
        map(int, certificate["basis_relation_ids"])
    )
    if not set(used_basis_ids) <= set(basis_ids):
        raise AssertionError("certificate used an unknown basis relation")
    basis_vectors = []
    activation_corners_checked = 0
    for relation_id in basis_ids:
        origin = partial["relation_origins"][relation_id]
        colour = int(origin["colour"])
        chosen = tuple(
            edge(*map(int, item))
            for item in origin["minimal_subset"]
        )
        if not chosen or not set(chosen) <= set(factors[colour]):
            raise AssertionError("minimal subset left its factor")
        endpoints = {
            vertex for item in chosen for vertex in item
        }
        if not all(
            feasible_on_cycle(cycle, endpoints) for cycle in cycles
        ):
            raise AssertionError("reported subset stopped feasible")
        for size in range(1, len(chosen)):
            for subchosen in itertools.combinations(chosen, size):
                deleted = {
                    vertex for item in subchosen for vertex in item
                }
                if all(
                    feasible_on_cycle(cycle, deleted)
                    for cycle in cycles
                ):
                    raise AssertionError(
                        "reported subset stopped positive-minimal"
                    )
        touched = tuple(
            cycle_id
            for cycle_id, cycle in enumerate(cycles)
            if set(cycle) & endpoints
        )
        untouched = tuple(
            cycle_id
            for cycle_id in range(len(cycles))
            if cycle_id not in touched
        )
        if len(untouched) != 1:
            raise AssertionError("forced relation lost unique untouched cycle")
        if list(touched) != list(map(int, origin["touched_cycles"])):
            raise AssertionError("touched cycle record changed")
        if untouched[0] != int(origin["forced_cycle"]):
            raise AssertionError("forced cycle record changed")
        adjacent_ports = True
        for cycle_id in touched:
            deleted = tuple(
                vertex
                for vertex in cycles[cycle_id]
                if vertex in endpoints
            )
            if (
                len(deleted) != 2
                or edge(*deleted) not in cycle_edges(cycles[cycle_id])
            ):
                adjacent_ports = False
                break
        if adjacent_ports:
            component_of = {
                vertex: cycle_id
                for cycle_id, cycle in enumerate(cycles)
                for vertex in cycle
            }
            degrees = Counter()
            adjacency = {cycle_id: set() for cycle_id in touched}
            loop = False
            for first, second in chosen:
                left = component_of[first]
                right = component_of[second]
                if left == right:
                    loop = True
                    break
                degrees[left] += 1
                degrees[right] += 1
                adjacency[left].add(right)
                adjacency[right].add(left)
            connected = False
            if not loop and all(
                degrees[cycle_id] == 2 for cycle_id in touched
            ):
                seen = set()
                stack = [touched[0]]
                while stack:
                    current = stack.pop()
                    if current in seen:
                        continue
                    seen.add(current)
                    stack.extend(adjacency[current] - seen)
                connected = seen == set(touched)
            if connected:
                raise AssertionError(
                    "reported forced relation became a port exception"
                )

        base = tuple(map(int, origin["base_colouring"]))
        target = tuple(map(int, origin["target_colouring"]))
        other_colours = {item for item in range(3) if item != colour}
        if set(base) - other_colours:
            raise AssertionError("base uses the activated colour")
        for other in other_colours:
            if any(
                base[item[0]] == base[item[1]]
                for item in factors[other]
            ):
                raise AssertionError("base stopped properly 2-coloured")
        expected_target = list(base)
        for vertex in endpoints:
            expected_target[vertex] = colour
        if tuple(expected_target) != target:
            raise AssertionError("target recolouring changed")
        if active_singleton_edges(base, labels):
            raise AssertionError("base activated a singleton edge")
        if active_singleton_edges(target, labels) != frozenset(chosen):
            raise AssertionError("target activation changed")
        endpoint_list = sorted(endpoints)
        for mask in range(1 << len(endpoint_list)):
            corner = list(base)
            for position, vertex in enumerate(endpoint_list):
                if mask & (1 << position):
                    corner[vertex] = colour
            active = active_singleton_edges(corner, labels)
            active_ids = active_matching_ids(
                matchings, corner, full_edges, labels
            )
            if mask == (1 << len(endpoint_list)) - 1:
                if active != frozenset(chosen):
                    raise AssertionError("target cube corner changed")
                expected_count = (
                    len(full_only_ids) + 2 ** len(untouched)
                )
                if len(active_ids) != expected_count:
                    raise AssertionError(
                        "target completion count changed"
                    )
                for matching_id in set(active_ids) - full_only_ids:
                    used_singletons = (
                        set(matchings[matching_id]) & singleton_edges
                    )
                    if used_singletons != set(chosen):
                        raise AssertionError(
                            "target gained an unexpected completion"
                        )
            else:
                for subset_size in range(1, len(chosen) + 1):
                    for subset in itertools.combinations(
                        active, subset_size
                    ):
                        deleted = {
                            vertex for item in subset for vertex in item
                        }
                        if all(
                            feasible_on_cycle(cycle, deleted)
                            for cycle in cycles
                        ):
                            raise AssertionError(
                                "proper cube corner gained a feasible set"
                            )
                if set(active_ids) != full_only_ids:
                    raise AssertionError(
                        "proper cube corner gained a non-full matching"
                    )
            activation_corners_checked += 1
        forced_cycle = cycles[untouched[0]]
        alternating = (
            tuple(
                edge(
                    forced_cycle[index],
                    forced_cycle[(index + 1) % len(forced_cycle)],
                )
                for index in range(0, len(forced_cycle), 2)
            ),
            tuple(
                edge(
                    forced_cycle[index],
                    forced_cycle[(index + 1) % len(forced_cycle)],
                )
                for index in range(1, len(forced_cycle), 2)
            ),
        )
        difference = monomial(
            alternating[0], target, full_edges, labels
        )
        difference.subtract(
            monomial(alternating[1], target, full_edges, labels)
        )
        observed = canonical(difference)
        expected = reported_relation(
            partial["relation_vectors"][relation_id]
        )
        if observed != expected:
            raise AssertionError("forced relation signature changed")
        basis_vectors.append(Counter(dict(expected)))

    target_colouring = tuple(
        map(int, certificate["target_colouring"])
    )
    if len(set(target_colouring)) == 1:
        raise AssertionError("target amplitude became monochromatic")
    activity = active_matching_ids(
        matchings, target_colouring, full_edges, labels
    )
    if list(activity) != list(
        map(int, certificate["target_matching_ids"])
    ):
        raise AssertionError("target activity changed")
    target_monomials = {
        matching_id: monomial(
            matchings[matching_id],
            target_colouring,
            full_edges,
            labels,
        )
        for matching_id in activity
    }
    seen = set()
    nonzero_classes = 0
    for signed_class in certificate["signed_classes"]:
        coefficient = 0
        representative = None
        for member in signed_class["members"]:
            matching_id = int(member["matching_id"])
            if matching_id not in activity or matching_id in seen:
                raise AssertionError("signed class membership changed")
            seen.add(matching_id)
            sign = int(member["sign"])
            coordinates = list(map(int, member["coordinates"]))
            if len(coordinates) != len(basis_vectors):
                raise AssertionError("basis coordinate width changed")
            if representative is None:
                representative = target_monomials[matching_id]
                if sign != 1 or any(coordinates):
                    raise AssertionError(
                        "class representative convention changed"
                    )
            else:
                difference = target_monomials[matching_id].copy()
                difference.subtract(representative)
                reconstructed: Counter[int] = Counter()
                for scalar, vector in zip(
                    coordinates, basis_vectors, strict=True
                ):
                    for variable, value in vector.items():
                        reconstructed[variable] += scalar * value
                if direct_sparse(difference) != direct_sparse(
                    reconstructed
                ):
                    raise AssertionError(
                        "signed lattice coordinate replay changed"
                    )
                expected_sign = -1 if sum(coordinates) % 2 else 1
                if sign != expected_sign:
                    raise AssertionError("signed class parity changed")
            coefficient += sign
        if coefficient != int(signed_class["coefficient"]):
            raise AssertionError("signed class coefficient changed")
        nonzero_classes += coefficient != 0
    if seen != set(activity):
        raise AssertionError("signed classes do not cover target activity")
    if nonzero_classes != 1:
        raise AssertionError("target no longer has one surviving class")

    payload = {
        "verified": True,
        "status": "partial_circuit_amplitude_lattice_contradiction_verified",
        "scope": (
            "independent factor, minimality, activation-cube, forced "
            "cycle relation, target activity, and signed-class replay"
        ),
        "partial_analysis": str(args.partial_analysis),
        "partial_analysis_sha256": sha256(args.partial_analysis),
        "amplitude_analysis": str(args.amplitude_analysis),
        "amplitude_analysis_sha256": sha256(args.amplitude_analysis),
        "partition": list(partition),
        "orbit": int(partial["orbit"]),
        "skeleton_perfect_matchings": len(matchings),
        "basis_relations_replayed": len(basis_vectors),
        "activation_corners_checked": activation_corners_checked,
        "target_active_matchings": len(activity),
        "target_nonzero_signed_classes": nonzero_classes,
        "global_conjecture_resolved": False,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
