"""Find a factor-choice fork for a support with all-even full cycles."""

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

REPO_ROOT, HERE = _bootstrap_repository(__file__, also=["."])

import argparse
import itertools
import json
import time
from pathlib import Path

import numpy as np

from analyze_fourteen_vertex_full_direct_motifs import (
    EQUATIONS,
    extension_offsets,
)
from krenn_gu.explore_random_even_cycle_forks import cycle_edges, perfect_matchings
from explore_random_minimal_singleton_sets import contiguous_cycles

N = 14


def indexed_colouring(index: int) -> tuple[int, ...]:
    return tuple((index // (3**vertex)) % 3 for vertex in range(N))


def local_codes(
    indices: np.ndarray, cycle: tuple[int, ...]
) -> np.ndarray:
    output = np.zeros(len(indices), dtype=np.int64)
    for position, vertex in enumerate(cycle):
        output += (
            (indices // (3**vertex)) % 3
        ) * (3**position)
    return output


def local_code_value(index: int, cycle: tuple[int, ...]) -> int:
    return sum(
        ((index // (3**vertex)) % 3) * (3**position)
        for position, vertex in enumerate(cycle)
    )


def activation_constraint_mask(
    index: int, eligible_edges: tuple[tuple[int, int], ...]
) -> int:
    colouring = indexed_colouring(index)
    output = 0
    edge_count = len(eligible_edges)
    for role in (1, 2):
        offset = (role - 1) * edge_count
        for edge_id, (first, second) in enumerate(eligible_edges):
            if colouring[first] == colouring[second] == role:
                output |= 1 << (offset + edge_id)
    return output


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("exploration", type=Path)
    parser.add_argument("--survivor-index", type=int, default=0)
    parser.add_argument("--survivor-key", default="survivors")
    parser.add_argument(
        "--candidate-bases",
        type=int,
        default=1,
        help=(
            "score this many viable base colourings and retain the "
            "certificate imposing the fewest role-1/role-2 activation "
            "constraints (default: first viable base only)"
        ),
    )
    parser.add_argument(
        "--certificates-per-support",
        type=int,
        default=1,
        help=(
            "retain this many distinct low-footprint factor-fork "
            "certificates for the same support"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_even_cycle_factor_fork.json"
        ),
    )
    args = parser.parse_args()
    if args.candidate_bases < 1:
        raise ValueError("--candidate-bases must be positive")
    if args.certificates_per_support < 1:
        raise ValueError("--certificates-per-support must be positive")
    exploration = json.loads(
        args.exploration.read_text(encoding="utf-8")
    )
    survivor = exploration[args.survivor_key][args.survivor_index]
    lengths = tuple(map(int, exploration["partition"]))
    if any(length % 2 for length in lengths):
        raise ValueError("every full-factor cycle must be even")
    cycles = contiguous_cycles(lengths)
    full_edges = {
        item for cycle in cycles for item in cycle_edges(cycle)
    }
    singleton_matchings = [
        tuple(tuple(map(int, item)) for item in survivor[key])
        for key in ("first", "second", "third")
    ]
    labels = {
        item: colour
        for colour, matching in enumerate(singleton_matchings)
        for item in matching
    }
    skeleton_edges = set(full_edges) | set(labels)
    unseen = set(range(N))
    components = []
    while unseen:
        reached = {min(unseen)}
        changed = True
        while changed:
            changed = False
            for first, second in skeleton_edges:
                if first in reached and second not in reached:
                    reached.add(second)
                    changed = True
                elif second in reached and first not in reached:
                    reached.add(first)
                    changed = True
        components.append(tuple(sorted(reached)))
        unseen.difference_update(reached)
    if len(components) > 1:
        payload = {
            "status": "disconnected_factorization_contradiction",
            "necessary_conditions_only": False,
            "exploration": str(args.exploration),
            "survivor_index": args.survivor_index,
            "full_cycle_type": list(lengths),
            "singleton_matchings": {
                key: survivor[key]
                for key in ("first", "second", "third")
            },
            "skeleton_components": [
                list(component) for component in components
            ],
            "certificate": {
                "certificate_mode": (
                    "disconnected_tensor_factorization"
                ),
                "logical_check": (
                    "same-colour component coefficients are nonzero, "
                    "so assigning different constant colours to two "
                    "components gives a forbidden nonzero coefficient"
                ),
            },
        }
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(payload, indent=2) + "\n",
            encoding="utf-8",
        )
        print(json.dumps(payload, indent=2))
        return
    matchings = perfect_matchings(N, full_edges | set(labels))
    full_only = tuple(
        matching_id
        for matching_id, matching in enumerate(matchings)
        if all(item in full_edges for item in matching)
    )
    expected_full = 1 << len(cycles)
    if len(full_only) != expected_full:
        raise AssertionError("full-only matching count changed")
    target_activity_size = expected_full + 1
    started = time.perf_counter()
    counts = np.zeros(EQUATIONS, dtype=np.int16)
    slots = [
        np.full(EQUATIONS, -1, dtype=np.int16)
        for _ in range(target_activity_size)
    ]
    offset_cache: dict[tuple[int, ...], np.ndarray] = {}
    total_extensions = 0
    for matching_id, matching in enumerate(matchings):
        requirements = {
            vertex: labels[item]
            for item in matching
            if item in labels
            for vertex in item
        }
        base = sum(
            colour * (3**vertex)
            for vertex, colour in requirements.items()
        )
        free = tuple(
            vertex for vertex in range(N) if vertex not in requirements
        )
        indices = base + extension_offsets(free, offset_cache)
        old = counts[indices].copy()
        for position in range(target_activity_size):
            slots[position][indices[old == position]] = matching_id
        counts[indices] = old + 1
        total_extensions += len(indices)

    monochromatic = np.zeros(EQUATIONS, dtype=bool)
    for colour in range(3):
        monochromatic[
            sum(colour * (3**vertex) for vertex in range(N))
        ] = True
    base_mask = (counts == expected_full) & ~monochromatic
    for position, matching_id in enumerate(sorted(full_only)):
        base_mask &= slots[position] == matching_id
    base_indices = np.flatnonzero(base_mask)
    target_mask = (counts == target_activity_size) & ~monochromatic
    for matching_id in full_only:
        target_mask &= np.logical_or.reduce(
            [slot == matching_id for slot in slots]
        )
    target_indices = np.flatnonzero(target_mask)
    eligible_edges = tuple(
        item
        for item in itertools.combinations(range(N), 2)
        if item not in full_edges
    )
    target_constraint_masks = {
        int(target): activation_constraint_mask(
            int(target), eligible_edges
        )
        for target in target_indices
    }
    target_by_cycle_code = []
    for cycle in cycles:
        codes = local_codes(target_indices, cycle)
        first_by_code: dict[int, int] = {}
        best_by_code: dict[int, int] = {}
        for code, target in zip(codes, target_indices, strict=True):
            code_value = int(code)
            target_value = int(target)
            first_by_code.setdefault(code_value, target_value)
            previous = best_by_code.get(code_value)
            if previous is None or (
                target_constraint_masks[target_value].bit_count(),
                target_value,
            ) < (
                target_constraint_masks[previous].bit_count(),
                previous,
            ):
                best_by_code[code_value] = target_value
        mapping = {
            code: tuple(
                dict.fromkeys(
                    (first_by_code[code], best_by_code[code])
                )
            )
            for code in first_by_code
        }
        target_by_cycle_code.append(mapping)

    retained_certificates: dict[
        str, tuple[int, dict[str, object]]
    ] = {}
    viable_bases_scored = 0
    for base in base_indices:
        base_constraint_mask = activation_constraint_mask(
            int(base), eligible_edges
        )
        target_choices = []
        for cycle, mapping in zip(
            cycles, target_by_cycle_code, strict=True
        ):
            code = local_code_value(int(base), cycle)
            if code not in mapping:
                break
            target_choices.append(mapping[code])
        if len(target_choices) != len(cycles):
            continue

        def choice_score(choices: tuple[int, ...]):
            mask = base_constraint_mask
            for target in choices:
                mask |= target_constraint_masks[target]
            return mask.bit_count(), choices

        targets = min(
            itertools.product(*target_choices),
            key=choice_score,
        )
        constrained_mask = base_constraint_mask
        alternatives = []
        for cycle, target in zip(cycles, targets, strict=True):
            constrained_mask |= target_constraint_masks[target]
            activity = [int(slot[target]) for slot in slots]
            extra = next(
                matching_id
                for matching_id in activity
                if matching_id not in full_only
            )
            alternatives.append(
                {
                    "cycle": list(cycle),
                    "target_equation_index": target,
                    "target_colouring": list(
                        indexed_colouring(target)
                    ),
                    "target_activity": activity,
                    "surviving_matching": extra,
                }
            )
        candidate = {
            "certificate_mode": "even_cycle_factor_choice_fork",
            "base_equation_index": int(base),
            "base_colouring": list(indexed_colouring(int(base))),
            "base_activity": list(full_only),
            "alternatives": alternatives,
        }
        score = constrained_mask.bit_count()
        viable_bases_scored += 1
        signature = json.dumps(
            candidate, sort_keys=True, separators=(",", ":")
        )
        retained_certificates.setdefault(
            signature, (score, candidate)
        )
        if (
            len(retained_certificates)
            > args.certificates_per_support
        ):
            worst_signature = max(
                retained_certificates,
                key=lambda item: (
                    retained_certificates[item][0],
                    item,
                ),
            )
            del retained_certificates[worst_signature]
        if viable_bases_scored >= args.candidate_bases:
            break
    certificate_rows = sorted(
        retained_certificates.values(),
        key=lambda row: (
            row[0],
            json.dumps(
                row[1], sort_keys=True, separators=(",", ":")
            ),
        ),
    )
    certificate_score = (
        certificate_rows[0][0] if certificate_rows else None
    )
    certificate = (
        certificate_rows[0][1] if certificate_rows else None
    )

    payload = {
        "status": (
            "even_cycle_factor_fork"
            if certificate is not None
            else "factor_fork_absent"
        ),
        "necessary_conditions_only": certificate is None,
        "exploration": str(args.exploration),
        "survivor_index": args.survivor_index,
        "full_cycle_type": list(lengths),
        "singleton_matchings": {
            key: survivor[key]
            for key in ("first", "second", "third")
        },
        "skeleton_perfect_matchings": len(matchings),
        "full_only_matching_count": expected_full,
        "target_activity_size": target_activity_size,
        "colourings_scanned": EQUATIONS,
        "matching_extensions_accumulated": total_extensions,
        "full_only_base_colourings": len(base_indices),
        "one_extra_targets_with_full_baseline": len(target_indices),
        "viable_bases_scored": viable_bases_scored,
        "certificates_per_support_requested": (
            args.certificates_per_support
        ),
        "certificate_candidates": [
            {
                "activation_constraint_score": score,
                "certificate": row,
            }
            for score, row in certificate_rows
        ],
        "certificate_activation_constraint_score": certificate_score,
        "certificate": certificate,
        "elapsed_seconds": time.perf_counter() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
