"""Independent exact audit of the P5 pair-signature coverage records."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path

from sympy import Matrix, ZZ
from sympy.polys.matrices import DomainMatrix
from sympy.polys.matrices.normalforms import smith_normal_decomp


ROOT = Path(__file__).resolve().parent
NORMAL_PATH = ROOT / "audit_five_row_projective_normal_forms.py"
SPEC = importlib.util.spec_from_file_location("normal_audit", NORMAL_PATH)
NORMAL = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(NORMAL)

SOURCES = tuple(range(5))
COLOURS = tuple(range(3))
PAIRS = tuple(itertools.combinations(SOURCES, 2))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def support(row: tuple[int, ...]) -> int:
    return sum(
        (value != 0) << index for index, value in enumerate(row)
    )


def coordinate_mask(rows: tuple[tuple[int, ...], ...]) -> int:
    rank = NORMAL.rank_mod(rows)
    return sum(
        (
            NORMAL.rank_mod(rows + (coordinate,)) == rank
        )
        << colour
        for colour, coordinate in enumerate(NORMAL.COORDINATES)
    )


def pair_signature(rows: tuple[tuple[int, ...], ...]) -> tuple:
    return (
        tuple(support(row) for row in rows),
        tuple(
            coordinate_mask((rows[first], rows[second]))
            for first, second in PAIRS
        ),
    )


def permute_pair_signature(
    signature: tuple, permutation: tuple[int, ...]
) -> tuple:
    supports, incidences = signature
    pair_index = {pair: index for index, pair in enumerate(PAIRS)}
    return (
        tuple(supports[permutation[index]] for index in SOURCES),
        tuple(
            incidences[
                pair_index[
                    tuple(
                        sorted(
                            (
                                permutation[first],
                                permutation[second],
                            )
                        )
                    )
                ]
            ]
            for first, second in PAIRS
        ),
    )


def permute_colours(mask: int, permutation: tuple[int, ...]) -> int:
    return sum(
        ((mask >> colour) & 1) << permutation[colour]
        for colour in COLOURS
    )


def canonical_signature(signature: tuple) -> tuple:
    supports, incidences = signature
    pair_index = {pair: index for index, pair in enumerate(PAIRS)}
    images = []
    for source_permutation in itertools.permutations(SOURCES):
        for colour_permutation in itertools.permutations(COLOURS):
            new_supports = [0] * len(SOURCES)
            for old_source in SOURCES:
                new_supports[source_permutation[old_source]] = (
                    permute_colours(
                        supports[old_source], colour_permutation
                    )
                )
            new_incidences = [0] * len(PAIRS)
            for old_index, (first, second) in enumerate(PAIRS):
                new_pair = tuple(
                    sorted(
                        (
                            source_permutation[first],
                            source_permutation[second],
                        )
                    )
                )
                new_incidences[pair_index[new_pair]] = permute_colours(
                    incidences[old_index], colour_permutation
                )
            images.append(
                (tuple(new_supports), tuple(new_incidences))
            )
    return min(images)


def catalogue_pair_patterns() -> set[tuple]:
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
    patterns = set()
    retained = 0
    for indices in itertools.combinations_with_replacement(
        range(len(points)), 5
    ):
        if any(
            not pair_condition[indices[first]][indices[second]]
            for first, second in PAIRS
        ):
            continue
        rows = tuple(points[index] for index in indices)
        if NORMAL.rank_mod(rows) != 3:
            continue
        retained += 1
        base = pair_signature(rows)
        for permutation in itertools.permutations(SOURCES):
            patterns.add(permute_pair_signature(base, permutation))
    if retained != 2556 or len(patterns) != 6495:
        raise AssertionError(
            f"catalogue changed: retained={retained}, "
            f"patterns={len(patterns)}"
        )
    return patterns


class RowLattice:
    """Independent Smith-form membership for a row lattice."""

    def __init__(self, rows: list[list[int]], width: int) -> None:
        self.width = width
        self.rows = rows
        if not rows:
            self.rank = 0
            return
        transposed = [list(column) for column in zip(*rows, strict=True)]
        matrix = DomainMatrix.from_list_sympy(
            width, len(rows), transposed
        ).convert_to(ZZ)
        smith, left, right = smith_normal_decomp(matrix)
        if smith != left * matrix * right:
            raise AssertionError("Smith decomposition did not replay")
        self.smith = smith.to_Matrix()
        self.left = left.to_Matrix()
        self.rank = sum(
            self.smith[index, index] != 0
            for index in range(min(self.smith.shape))
        )

    def contains(self, vector: list[int]) -> bool:
        if not self.rows:
            return not any(vector)
        transformed = self.left * Matrix(vector)
        for index in range(self.rank):
            if int(transformed[index]) % int(
                self.smith[index, index]
            ):
                return False
        return not any(
            transformed[index]
            for index in range(self.rank, self.width)
        )


def exponent_vector(
    selected: tuple[tuple[int, int], ...],
    positions: dict[tuple[int, int], int],
) -> list[int]:
    vector = [0] * len(positions)
    for variable in selected:
        vector[positions[variable]] += 1
    return vector


def subtract(left: list[int], right: list[int]) -> list[int]:
    return [a - b for a, b in zip(left, right, strict=True)]


def independent_contradiction(
    supports: tuple[int, ...], incidences: tuple[int, ...]
) -> str | None:
    variables = tuple(
        (source, colour)
        for source in SOURCES
        for colour in COLOURS
        if supports[source] & (1 << colour)
    )
    positions = {
        variable: index for index, variable in enumerate(variables)
    }
    relation_rows = []
    for pair_index, (first, second) in enumerate(PAIRS):
        for coordinate in COLOURS:
            if not (incidences[pair_index] & (1 << coordinate)):
                continue
            other = tuple(
                colour
                for colour in COLOURS
                if colour != coordinate
            )
            first_term = (
                (first, other[0]),
                (second, other[1]),
            )
            second_term = (
                (first, other[1]),
                (second, other[0]),
            )
            active = (
                all(variable in positions for variable in first_term),
                all(variable in positions for variable in second_term),
            )
            if active[0] != active[1]:
                return "singleton_minor"
            if active[0]:
                relation_rows.append(
                    subtract(
                        exponent_vector(first_term, positions),
                        exponent_vector(second_term, positions),
                    )
                )
    lattice = RowLattice(relation_rows, len(variables))

    for pair_index, (first, second) in enumerate(PAIRS):
        for coordinate in COLOURS:
            if not (incidences[pair_index] & (1 << coordinate)):
                continue
            coordinate_mask_value = 1 << coordinate
            if (
                supports[first] == coordinate_mask_value
                or supports[second] == coordinate_mask_value
            ):
                continue
            can_be_nonzero = False
            for other in COLOURS:
                if other == coordinate:
                    continue
                terms = (
                    ((first, coordinate), (second, other)),
                    ((first, other), (second, coordinate)),
                )
                active = tuple(
                    all(variable in positions for variable in term)
                    for term in terms
                )
                if active[0] != active[1]:
                    can_be_nonzero = True
                elif active[0]:
                    difference = subtract(
                        exponent_vector(terms[0], positions),
                        exponent_vector(terms[1], positions),
                    )
                    if not lattice.contains(difference):
                        can_be_nonzero = True
            if not can_be_nonzero:
                return "forced_rank_one_pair"

    for source_triple in itertools.combinations(SOURCES, 3):
        groups: list[dict] = []
        for permutation in itertools.permutations(COLOURS):
            selected = tuple(
                (source, permutation[index])
                for index, source in enumerate(source_triple)
            )
            if not all(variable in positions for variable in selected):
                continue
            vector = exponent_vector(selected, positions)
            inversions = sum(
                permutation[left] > permutation[right]
                for left in range(3)
                for right in range(left + 1, 3)
            )
            sign = -1 if inversions % 2 else 1
            for group in groups:
                if lattice.contains(
                    subtract(vector, group["representative"])
                ):
                    group["coefficient"] += sign
                    break
            else:
                groups.append(
                    {"representative": vector, "coefficient": sign}
                )
        if any(group["coefficient"] for group in groups):
            return None
    return "forced_rank_two_map"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--records",
        type=Path,
        default=Path(
            "tmp/p5_pair_signature_catalogue_coverage_verified.json"
        ),
    )
    parser.add_argument(
        "--drat-result",
        type=Path,
        default=Path(
            "tmp/p5_pair_signature_catalogue_coverage_drat_verified.json"
        ),
    )
    args = parser.parse_args()
    payload = json.loads(args.records.read_text(encoding="utf-8"))
    catalogue = catalogue_pair_patterns()
    seen = set()
    reason_counts: dict[str, int] = {}
    orbit_counts: dict[tuple, int] = {}
    for index, record in enumerate(payload["outside_exclusions"]):
        supports = tuple(map(int, record["supports"]))
        incidences = tuple(map(int, record["pair_incidences"]))
        pattern = (supports, incidences)
        if pattern in catalogue or pattern in seen:
            raise AssertionError(
                f"record {index} is catalogued or duplicated"
            )
        seen.add(pattern)
        if (
            len(set(incidences)) != 1
            or incidences[0] not in (1, 2, 4)
        ):
            raise AssertionError(
                f"record {index} is not an all-one-axis pattern"
            )
        canonical = canonical_signature(pattern)
        orbit_counts[canonical] = orbit_counts.get(canonical, 0) + 1
        reason = independent_contradiction(supports, incidences)
        if reason != record["contradiction"]:
            raise AssertionError(
                f"record {index}: {reason} != "
                f"{record['contradiction']}"
            )
        reason_counts[reason] = reason_counts.get(reason, 0) + 1

    drat = json.loads(args.drat_result.read_text(encoding="utf-8"))
    if not drat.get("verified"):
        raise AssertionError("DRAT replay is not verified")
    cnf = ROOT / drat["cnf"]
    proof = ROOT / drat["proof"]
    if sha256(cnf) != drat["cnf_sha256"]:
        raise AssertionError("CNF hash changed")
    if sha256(proof) != drat["proof_sha256"]:
        raise AssertionError("DRAT hash changed")
    result = {
        "verified": True,
        "catalogue_pair_patterns": len(catalogue),
        "outside_exclusions": len(seen),
        "outside_orbits": len(orbit_counts),
        "outside_orbit_sizes": sorted(orbit_counts.values()),
        "all_outside_patterns_share_one_axis": True,
        "reason_counts": reason_counts,
        "records_sha256": sha256(args.records),
        "cnf_sha256": drat["cnf_sha256"],
        "proof_sha256": drat["proof_sha256"],
        "drat_forward_verified": True,
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
