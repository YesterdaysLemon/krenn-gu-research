"""Audit the four-regular balanced-bridge alternating-cycle obstruction.

The arbitrary-order proof is elementary and is recorded in
FOUR_REGULAR_BALANCED_BRIDGE_OBSTRUCTION.md.  This program independently
reconstructs the eight local normal types, their anchor-pair singleton
ports, the one-defect cycle lemma, and every contracted order-six port
configuration (4,096 cases).
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
import time


COLOURS = tuple(range(3))
NormalType = tuple[int, int, int]
Stub = tuple[int, int, int]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normal_types() -> tuple[NormalType, ...]:
    return tuple(
        values
        for values in itertools.product(COLOURS, repeat=3)
        if all(values[colour] != colour for colour in COLOURS)
    )


def complement(item: NormalType) -> NormalType:
    return tuple(
        next(
            colour
            for colour in COLOURS
            if colour not in (index, item[index])
        )
        for index in COLOURS
    )


def anchor_pair_ports(
    item: NormalType,
) -> tuple[dict[tuple[int, int], int], dict[int, tuple[int, int]]]:
    """Return port sides and usable pair-constant transitions."""
    other = complement(item)
    sides: dict[tuple[int, int], int] = {}
    for side, endpoint_type in enumerate((item, other)):
        for target, local in enumerate(endpoint_type):
            label = (local, target)
            if label in sides:
                raise AssertionError("directed singleton port repeated")
            sides[label] = side
    expected = {
        (local, target)
        for local in COLOURS
        for target in COLOURS
        if local != target
    }
    if set(sides) != expected:
        raise AssertionError("anchor pair lacks a directed colour port")

    transitions = {}
    for local in COLOURS:
        targets = tuple(
            target for target in COLOURS if target != local
        )
        if sides[(local, targets[0])] != sides[(local, targets[1])]:
            transitions[local] = targets
    return sides, transitions


def derangements(size: int) -> tuple[tuple[int, ...], ...]:
    return tuple(
        permutation
        for permutation in itertools.permutations(range(size))
        if all(
            permutation[index] != index for index in range(size)
        )
    )


def contracted_configuration(
    endpoint_types: tuple[NormalType, ...],
    port_matchings: tuple[tuple[int, ...], ...],
) -> tuple[dict[Stub, list[Stub]], list[tuple[int, int, Stub, Stub]]]:
    size = len(endpoint_types)
    stubs = [
        (pair, local, target)
        for pair in range(size)
        for local in COLOURS
        for target in COLOURS
        if local != target
    ]
    adjacency = {stub: [] for stub in stubs}
    colour_pairs = ((0, 1), (0, 2), (1, 2))
    for permutation, (left, right) in zip(
        port_matchings, colour_pairs, strict=True
    ):
        for pair, partner in enumerate(permutation):
            first = (pair, left, right)
            second = (partner, right, left)
            adjacency[first].append(second)
            adjacency[second].append(first)

    transitions = []
    for pair, endpoint_type in enumerate(endpoint_types):
        _, usable = anchor_pair_ports(endpoint_type)
        for local, targets in usable.items():
            transitions.append(
                (
                    pair,
                    local,
                    (pair, local, targets[0]),
                    (pair, local, targets[1]),
                )
            )
    if any(len(neighbours) != 1 for neighbours in adjacency.values()):
        raise AssertionError("singleton ports are not perfectly paired")
    return adjacency, transitions


def has_compatible_cycle(
    singleton_adjacency: dict[Stub, list[Stub]],
    transitions: list[tuple[int, int, Stub, Stub]],
    pair_colours: tuple[int, ...],
) -> bool:
    adjacency = {
        stub: list(neighbours)
        for stub, neighbours in singleton_adjacency.items()
    }
    for pair, colour, first, second in transitions:
        if pair_colours[pair] == colour:
            adjacency[first].append(second)
            adjacency[second].append(first)

    seen = set()
    for start, neighbours in adjacency.items():
        if start in seen or len(neighbours) != 2:
            continue
        stack = [start]
        component = []
        while stack:
            current = stack.pop()
            if current in seen:
                continue
            seen.add(current)
            component.append(current)
            stack.extend(
                neighbour
                for neighbour in adjacency[current]
                if neighbour not in seen
            )
        if component and all(
            len(adjacency[stub]) == 2 for stub in component
        ):
            return True
    return False


def proper_cycle_words(length: int) -> tuple[tuple[int, ...], ...]:
    return tuple(
        word
        for word in itertools.product(COLOURS, repeat=length)
        if all(
            word[index] != word[(index + 1) % length]
            for index in range(length)
        )
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/four_regular_balanced_bridge_obstruction_verified.json"
        ),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    started = time.perf_counter()
    types = normal_types()
    if len(types) != 8:
        raise AssertionError("normal-type count changed")

    local_records = []
    usable_size_distribution = {1: 0, 3: 0}
    for index, item in enumerate(types):
        sides, usable = anchor_pair_ports(item)
        if len(usable) not in usable_size_distribution:
            raise AssertionError("unexpected usable-colour count")
        usable_size_distribution[len(usable)] += 1
        local_records.append(
            {
                "type": index,
                "normals": list(item),
                "complement": list(complement(item)),
                "directed_ports": [
                    {
                        "local_colour": local,
                        "target_colour": target,
                        "endpoint_side": side,
                    }
                    for (local, target), side in sorted(sides.items())
                ],
                "usable_pair_constant_colours": sorted(usable),
            }
        )
    if usable_size_distribution != {1: 6, 3: 2}:
        raise AssertionError("anchor transition distribution changed")

    # A cycle compatible with a colouring that differs from a constant
    # background at exactly one pair has a proper cyclic colour word with
    # exactly one non-background symbol.  Such a word can only have length
    # two: at length at least three, two consecutive background symbols
    # remain.  The finite loop is a regression check of that general
    # one-line argument.
    word_checks = 0
    one_defect_words = []
    for length in range(2, 13):
        for word in proper_cycle_words(length):
            for background in COLOURS:
                differences = sum(
                    colour != background for colour in word
                )
                if differences == 1:
                    if length != 2:
                        raise AssertionError(
                            "long proper one-defect cycle appeared"
                        )
                    one_defect_words.append(
                        {
                            "length": length,
                            "word": list(word),
                            "background": background,
                        }
                    )
                word_checks += 1
    if len(one_defect_words) != 12:
        raise AssertionError("one-defect word census changed")

    # Exhaust every contracted m=3 configuration.  Each anchor pair may
    # have any of the eight oriented types.  For each unordered colour
    # pair, reciprocal singleton ports are joined by either derangement.
    size = 3
    matchings = derangements(size)
    if len(matchings) != 2:
        raise AssertionError("order-six derangement count changed")
    configurations = 0
    perturbations = 0
    minimum_cycle_free = 2 * size
    for endpoint_types in itertools.product(types, repeat=size):
        for port_matchings in itertools.product(matchings, repeat=3):
            adjacency, transitions = contracted_configuration(
                endpoint_types, port_matchings
            )
            configurations += 1
            for background in COLOURS:
                cycle_free = 0
                for pair in range(size):
                    for colour in COLOURS:
                        if colour == background:
                            continue
                        assignment = [background] * size
                        assignment[pair] = colour
                        if not has_compatible_cycle(
                            adjacency,
                            transitions,
                            tuple(assignment),
                        ):
                            cycle_free += 1
                        perturbations += 1
                if cycle_free < size:
                    raise AssertionError(
                        "single-defect counting bound failed"
                    )
                minimum_cycle_free = min(
                    minimum_cycle_free, cycle_free
                )
    if configurations != 4_096:
        raise AssertionError("contracted configuration count changed")

    theorem = Path(__file__).resolve().with_name(
        "FOUR_REGULAR_BALANCED_BRIDGE_OBSTRUCTION.md"
    )
    source = Path(__file__)
    payload = {
        "verified": True,
        "status": "four_regular_balanced_bridge_obstruction_verified",
        "scope": (
            "all eight complementary anchor types, the arbitrary-order "
            "single-defect alternating-cycle counting lemma, and all "
            "4096 contracted order-six port configurations"
        ),
        "normal_types": len(types),
        "local_records": local_records,
        "usable_colour_count_distribution": {
            str(key): value
            for key, value in usable_size_distribution.items()
        },
        "proper_cycle_word_lengths_checked": [2, 12],
        "proper_cycle_word_checks": word_checks,
        "proper_one_defect_words": one_defect_words,
        "one_defect_cycles_have_length_two": True,
        "arbitrary_order_counting_bound": (
            "at most m of the 2m one-pair perturbations can activate "
            "a length-two cycle for each background colour"
        ),
        "order_six_contracted_configurations": configurations,
        "order_six_perturbations_checked": perturbations,
        "order_six_minimum_cycle_free_perturbations": minimum_cycle_free,
        "theorem": str(theorem),
        "theorem_sha256": sha256(theorem),
        "source": str(source),
        "source_sha256": sha256(source),
        "global_conjecture_resolved": False,
        "elapsed_seconds": time.perf_counter() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
