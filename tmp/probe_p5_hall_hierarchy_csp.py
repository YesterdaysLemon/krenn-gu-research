"""Finite-field signature CSP for the exact P_5 Hall hierarchy.

Exploratory only: a surviving F_5 incidence/support architecture is not a
complex tensor restriction, while a null random search is not a proof.
"""

from __future__ import annotations

import importlib.util
import itertools
import pathlib
import random
from collections import Counter


ROOT = pathlib.Path(__file__).resolve().parents[1]
AUDIT_PATH = ROOT / "audit_five_row_projective_normal_forms.py"
SPEC = importlib.util.spec_from_file_location("normal_audit", AUDIT_PATH)
NORMAL = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(NORMAL)

SOURCES = tuple(range(5))
PERMUTATIONS = tuple(itertools.permutations(SOURCES))
SUBSETS = tuple(
    subset
    for size in (2, 3, 4)
    for subset in itertools.combinations(SOURCES, size)
)
SUBSET_INDEX = {subset: index for index, subset in enumerate(SUBSETS)}


def support(row: tuple[int, ...]) -> int:
    return sum((value != 0) << index for index, value in enumerate(row))


def coordinate_mask(rows: tuple[tuple[int, ...], ...]) -> int:
    rank = NORMAL.rank_mod(rows)
    return sum(
        (
            NORMAL.rank_mod(rows + (coordinate,)) == rank
        )
        << colour
        for colour, coordinate in enumerate(NORMAL.COORDINATES)
    )


def base_signature(rows: tuple[tuple[int, ...], ...]) -> tuple:
    supports = tuple(support(row) for row in rows)
    incidences = tuple(
        coordinate_mask(tuple(rows[index] for index in subset))
        for subset in SUBSETS
    )
    return supports, incidences


def permute_signature(signature: tuple, permutation: tuple[int, ...]) -> tuple:
    supports, incidences = signature
    new_supports = tuple(supports[permutation[index]] for index in SOURCES)
    new_incidences = []
    for subset in SUBSETS:
        old_subset = tuple(sorted(permutation[index] for index in subset))
        new_incidences.append(incidences[SUBSET_INDEX[old_subset]])
    return new_supports, tuple(new_incidences)


def local_signatures() -> tuple[tuple, ...]:
    points = (NORMAL.ZERO,) + tuple(
        sorted(
            {
                NORMAL.canonical(vector)
                for vector in itertools.product(
                    range(NORMAL.PRIME), repeat=3
                )
                if any(vector)
            }
        )
    )
    pair_condition = tuple(
        tuple(
            NORMAL.pair_contains_coordinate(left, right)
            for right in points
        )
        for left in points
    )
    result = set()
    retained = 0
    for indices in itertools.combinations_with_replacement(
        range(len(points)), 5
    ):
        if any(
            not pair_condition[indices[first]][indices[second]]
            for first, second in itertools.combinations(range(5), 2)
        ):
            continue
        rows = tuple(points[index] for index in indices)
        if NORMAL.rank_mod(rows) != 3:
            continue
        retained += 1
        base = base_signature(rows)
        for permutation in PERMUTATIONS:
            result.add(permute_signature(base, permutation))
    assert retained == 2556
    return tuple(sorted(result))


def pure_colour_hall(chosen: tuple[tuple, ...]) -> bool:
    for colour in range(3):
        if not any(
            all(
                chosen[mode][0][permutation[mode]] & (1 << colour)
                for mode in range(5)
            )
            for permutation in PERMUTATIONS
        ):
            return False
    return True


def matching_condition(chosen: tuple[tuple, ...]) -> bool:
    for colours in itertools.product(range(3), repeat=5):
        count = 0
        for permutation in PERMUTATIONS:
            if all(
                chosen[mode][0][permutation[mode]]
                & (1 << colours[mode])
                for mode in range(5)
            ):
                count += 1
                if len(set(colours)) > 1 and count >= 2:
                    break
        if len(set(colours)) == 1:
            if count == 0:
                return False
        elif count == 1:
            return False
    return True


def hierarchy_holds(chosen: tuple[tuple, ...]) -> bool:
    for subset_index, subset in enumerate(SUBSETS):
        required = len(subset)
        for colour in range(3):
            count = sum(
                bool(signature[1][subset_index] & (1 << colour))
                for signature in chosen
            )
            if count < required:
                return False
    return True


def score(signature: tuple) -> int:
    return sum(mask.bit_count() for mask in signature[1])


def main() -> None:
    signatures = local_signatures()
    print(f"local signatures: {len(signatures)}", flush=True)
    score_distribution = Counter(score(signature) for signature in signatures)
    print(
        f"incidence-score distribution: {dict(sorted(score_distribution.items()))}",
        flush=True,
    )
    ordered = tuple(sorted(signatures, key=score, reverse=True))
    rng = random.Random(20260726)
    pools = (ordered[:500], ordered[:2000], ordered)
    best = None
    trials = 0
    for pool in pools:
        for _ in range(200000):
            trials += 1
            chosen = tuple(rng.choice(pool) for _ in range(5))
            if (
                hierarchy_holds(chosen)
                and pure_colour_hall(chosen)
                and matching_condition(chosen)
            ):
                coordinate_rows = sum(
                    sum(mask in (1, 2, 4) for mask in signature[0])
                    for signature in chosen
                )
                candidate = (coordinate_rows, chosen)
                if best is None or candidate[0] < best[0]:
                    best = candidate
                    print(
                        f"new best coordinate-row total: {coordinate_rows}",
                        flush=True,
                    )
    print(f"random trials: {trials}", flush=True)
    if best is not None:
        print("hierarchy/support survivor:")
        for supports, incidences in best[1]:
            print(
                {
                    "row_supports": supports,
                    "incidence_score": sum(
                        mask.bit_count() for mask in incidences
                    ),
                    "coordinate_rows": sum(
                        mask in (1, 2, 4) for mask in supports
                    ),
                    "zero_rows": supports.count(0),
                }
            )
    else:
        print("no survivor in randomized hierarchy search")


if __name__ == "__main__":
    main()
