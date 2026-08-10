"""Find a direct factor-choice fork for one two-even-cycle support."""

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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("exploration", type=Path)
    parser.add_argument("--survivor-index", type=int, default=0)
    parser.add_argument(
        "--candidate-bases",
        type=int,
        default=10000,
        help=(
            "score this many viable bases and keep the certificate with "
            "the smallest transported activation footprint"
        ),
    )
    parser.add_argument(
        "--target-policy",
        choices=("first", "first-min", "pareto"),
        default="first",
        help=(
            "retain only the first target for each local code, or also "
            "the target with the smallest standalone activation mask"
        ),
    )
    parser.add_argument(
        "--targets-per-code",
        type=int,
        default=8,
        help=(
            "maximum subset-nondominated targets retained for each "
            "cycle code under --target-policy pareto"
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
            "tmp/fourteen_vertex_two_even_cycle_fork.json"
        ),
    )
    args = parser.parse_args()
    if args.candidate_bases < 1:
        raise ValueError("--candidate-bases must be positive")
    if args.targets_per_code < 1:
        raise ValueError("--targets-per-code must be positive")
    if args.certificates_per_support < 1:
        raise ValueError("--certificates-per-support must be positive")
    exploration = json.loads(
        args.exploration.read_text(encoding="utf-8")
    )
    survivor = exploration["survivors"][args.survivor_index]
    lengths = tuple(map(int, exploration["partition"]))
    if len(lengths) != 2 or any(length % 2 for length in lengths):
        raise ValueError("full factor must consist of two even cycles")
    cycles = contiguous_cycles(lengths)
    full_edges = {
        item for cycle in cycles for item in cycle_edges(cycle)
    }
    eligible_edges = tuple(
        item
        for item in itertools.combinations(range(N), 2)
        if item not in full_edges
    )
    singleton_matchings = [
        tuple(tuple(map(int, item)) for item in survivor[key])
        for key in ("first", "second", "third")
    ]
    labels = {
        item: colour
        for colour, matching in enumerate(singleton_matchings)
        for item in matching
    }
    matchings = perfect_matchings(N, full_edges | set(labels))
    full_only = tuple(
        matching_id
        for matching_id, matching in enumerate(matchings)
        if all(item in full_edges for item in matching)
    )
    if len(full_only) != 4:
        raise AssertionError("two even cycles need four full matchings")
    started = time.perf_counter()
    counts = np.zeros(EQUATIONS, dtype=np.int16)
    slots = [
        np.full(EQUATIONS, -1, dtype=np.int16) for _ in range(5)
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
        for position in range(5):
            slots[position][indices[old == position]] = matching_id
        counts[indices] = old + 1
        total_extensions += len(indices)
    all_indices = np.arange(EQUATIONS, dtype=np.int64)
    monochromatic = np.zeros(EQUATIONS, dtype=bool)
    for colour in range(3):
        monochromatic[
            sum(colour * (3**vertex) for vertex in range(N))
        ] = True
    base_mask = (counts == 4) & ~monochromatic
    for position, matching_id in enumerate(sorted(full_only)):
        base_mask &= slots[position] == matching_id
    base_indices = np.flatnonzero(base_mask)
    target_mask = (counts == 5) & ~monochromatic
    for matching_id in full_only:
        target_mask &= np.logical_or.reduce(
            [slot == matching_id for slot in slots]
        )
    target_indices = np.flatnonzero(target_mask)

    def activation_constraint_mask(equation: int) -> int:
        colouring = indexed_colouring(equation)
        output = 0
        for role in (1, 2):
            offset = (role - 1) * len(eligible_edges)
            for edge_id, (first, second) in enumerate(eligible_edges):
                if colouring[first] == colouring[second] == role:
                    output |= 1 << (offset + edge_id)
        return output

    target_by_cycle_code: list[dict[int, list[tuple[int, int]]]] = []
    for cycle in cycles:
        codes = local_codes(target_indices, cycle)
        first_by_code: dict[int, tuple[int, int]] = {}
        minimum_by_code: dict[int, tuple[int, int]] = {}
        all_by_code: dict[int, dict[int, int]] = {}
        for code, target in zip(codes, target_indices, strict=True):
            code = int(code)
            target = int(target)
            if code not in first_by_code:
                first_by_code[code] = (
                    target,
                    activation_constraint_mask(target),
                )
                if args.target_policy == "first":
                    continue
            if args.target_policy == "first":
                continue
            mask = activation_constraint_mask(target)
            if args.target_policy == "pareto":
                all_by_code.setdefault(code, {}).setdefault(mask, target)
                continue
            previous = minimum_by_code.get(code)
            if previous is None or mask.bit_count() < previous[1].bit_count():
                minimum_by_code[code] = (target, mask)
        mapping = {}
        for code, first in first_by_code.items():
            if args.target_policy == "pareto":
                candidates = []
                rows = sorted(
                    (
                        (target, mask)
                        for mask, target in all_by_code[code].items()
                    ),
                    key=lambda row: (
                        row[1].bit_count(),
                        row[0],
                    ),
                )
                for target, mask in rows:
                    if any(
                        kept_mask & ~mask == 0
                        for _kept_target, kept_mask in candidates
                    ):
                        continue
                    candidates.append((target, mask))
                    if len(candidates) == args.targets_per_code:
                        break
            else:
                candidates = [first]
            if args.target_policy == "first-min":
                minimum = minimum_by_code[code]
                if minimum[0] != first[0]:
                    candidates.append(minimum)
            mapping[code] = candidates
        target_by_cycle_code.append(mapping)
    retained_certificates: dict[
        str, tuple[int, dict[str, object]]
    ] = {}
    viable_bases_scored = 0
    for base in base_indices:
        choices = []
        for cycle, mapping in zip(
            cycles, target_by_cycle_code, strict=True
        ):
            code = int(local_codes(np.array([base]), cycle)[0])
            if code not in mapping:
                break
            choices.append(mapping[code])
        if len(choices) != 2:
            continue
        viable_bases_scored += 1
        base_mask = activation_constraint_mask(int(base))
        for selected in itertools.product(*choices):
            score = (
                base_mask | selected[0][1] | selected[1][1]
            ).bit_count()
            if retained_certificates:
                worst_score = max(
                    row[0] for row in retained_certificates.values()
                )
            else:
                worst_score = None
            if (
                len(retained_certificates)
                >= args.certificates_per_support
                and worst_score is not None
                and (
                    score > worst_score
                    or (
                        args.certificates_per_support == 1
                        and score == worst_score
                    )
                )
            ):
                continue
            alternatives = []
            for cycle, (target, _mask) in zip(
                cycles, selected, strict=True
            ):
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
                "base_equation_index": int(base),
                "base_colouring": list(
                    indexed_colouring(int(base))
                ),
                "base_activity": list(full_only),
                "alternatives": alternatives,
            }
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
            "two_even_cycle_factor_fork"
            if certificate is not None
            else "factor_fork_absent"
        ),
        "necessary_conditions_only": certificate is None,
        "exploration": str(args.exploration),
        "survivor_index": args.survivor_index,
        "full_cycle_type": list(lengths),
        "skeleton_perfect_matchings": len(matchings),
        "colourings_scanned": EQUATIONS,
        "matching_extensions_accumulated": total_extensions,
        "full_only_base_colourings": len(base_indices),
        "five_term_targets_with_full_baseline": len(target_indices),
        "candidate_bases_requested": args.candidate_bases,
        "target_policy": args.target_policy,
        "targets_per_code": args.targets_per_code,
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
        "viable_bases_scored": viable_bases_scored,
        "certificate_activation_constraint_score": certificate_score,
        "certificate": certificate,
        "elapsed_seconds": time.perf_counter() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
