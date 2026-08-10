#!/usr/bin/env python3
"""Independent finite-field audit of the decomposable P3 classification."""

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


import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
THEOREM = HERE / "P3_DECOMPOSABLE_RESTRICTION_CLASSIFICATION.md"
PERMUTATIONS = tuple(itertools.permutations(range(3)))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rref(
    rows: list[list[int]],
    columns: int,
    prime: int,
) -> tuple[tuple[int, ...], ...]:
    matrix = [
        [value % prime for value in row]
        for row in rows
        if any(value % prime for value in row)
    ]
    pivot_row = 0
    for column in range(columns):
        pivot = next(
            (
                row
                for row in range(pivot_row, len(matrix))
                if matrix[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = (
            matrix[pivot],
            matrix[pivot_row],
        )
        inverse = pow(matrix[pivot_row][column], -1, prime)
        matrix[pivot_row] = [
            value * inverse % prime for value in matrix[pivot_row]
        ]
        for row in range(len(matrix)):
            if row == pivot_row or not matrix[row][column]:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                (left - factor * right) % prime
                for left, right in zip(
                    matrix[row],
                    matrix[pivot_row],
                    strict=True,
                )
            ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return tuple(tuple(row) for row in matrix[:pivot_row])


def planes(prime: int) -> tuple[tuple[tuple[int, ...], ...], ...]:
    result = []
    for pivots in itertools.combinations(range(3), 2):
        free_positions = [
            (row, column)
            for row, pivot in enumerate(pivots)
            for column in range(pivot + 1, 3)
            if column not in pivots
        ]
        for values in itertools.product(
            range(prime),
            repeat=len(free_positions),
        ):
            basis = [[0] * 3 for _ in range(2)]
            for row, pivot in enumerate(pivots):
                basis[row][pivot] = 1
            for (row, column), value in zip(
                free_positions,
                values,
                strict=True,
            ):
                basis[row][column] = value
            result.append(tuple(tuple(row) for row in basis))
    return tuple(result)


def rank(
    rows: list[list[int]],
    columns: int,
    prime: int,
) -> int:
    return len(rref(rows, columns, prime))


def permanent_three(
    first: tuple[int, ...],
    second: tuple[int, ...],
    third: tuple[int, ...],
    prime: int,
) -> int:
    return sum(
        first[permutation[0]]
        * second[permutation[1]]
        * third[permutation[2]]
        for permutation in PERMUTATIONS
    ) % prime


def tensor(
    first: tuple[tuple[int, ...], ...],
    second: tuple[tuple[int, ...], ...],
    third: tuple[tuple[int, ...], ...],
    prime: int,
) -> tuple[int, ...]:
    return tuple(
        permanent_three(
            first[first_index],
            second[second_index],
            third[third_index],
            prime,
        )
        for first_index in range(len(first))
        for second_index in range(len(second))
        for third_index in range(len(third))
    )


def flattening_ranks(
    values: tuple[int, ...],
    dimensions: tuple[int, int, int],
    prime: int,
) -> tuple[int, int, int]:
    first_dimension, second_dimension, third_dimension = dimensions
    first = [
        list(
            values[
                index
                * second_dimension
                * third_dimension : (index + 1)
                * second_dimension
                * third_dimension
            ]
        )
        for index in range(first_dimension)
    ]
    second = [
        [
            values[
                first_index * second_dimension * third_dimension
                + second_index * third_dimension
                + third_index
            ]
            for first_index in range(first_dimension)
            for third_index in range(third_dimension)
        ]
        for second_index in range(second_dimension)
    ]
    third = [
        [
            values[
                first_index * second_dimension * third_dimension
                + second_index * third_dimension
                + third_index
            ]
            for first_index in range(first_dimension)
            for second_index in range(second_dimension)
        ]
        for third_index in range(third_dimension)
    ]
    return (
        rank(first, len(first[0]), prime),
        rank(second, len(second[0]), prime),
        rank(third, len(third[0]), prime),
    )


def plane_normal(
    plane: tuple[tuple[int, ...], ...],
    prime: int,
) -> tuple[int, ...]:
    first, second = plane
    normal = [
        first[1] * second[2] - first[2] * second[1],
        first[2] * second[0] - first[0] * second[2],
        first[0] * second[1] - first[1] * second[0],
    ]
    normal = [value % prime for value in normal]
    pivot = next(index for index, value in enumerate(normal) if value)
    inverse = pow(normal[pivot], -1, prime)
    return tuple(value * inverse % prime for value in normal)


def validate_sign_family(
    normals: tuple[tuple[int, ...], ...],
    prime: int,
) -> int:
    supports = [
        tuple(index for index, value in enumerate(normal) if value)
        for normal in normals
    ]
    assert supports[0] == supports[1] == supports[2]
    support = supports[0]
    assert len(support) in (2, 3)
    anchor = support[0]
    normalized = []
    for normal in normals:
        inverse = pow(normal[anchor], -1, prime)
        normalized.append(
            tuple(value * inverse % prime for value in normal)
        )
    reference = normalized[0]
    for normal in normalized[1:]:
        for coordinate in support[1:]:
            assert normal[coordinate] in (
                reference[coordinate],
                -reference[coordinate] % prime,
            )
    distinct = len(set(normalized))
    assert distinct == (2 if len(support) == 2 else 3)
    return len(support)


def validate_sign_rectangle(
    normals: tuple[tuple[int, ...], ...],
    prime: int,
) -> int:
    supports = [
        tuple(index for index, value in enumerate(normal) if value)
        for normal in normals
    ]
    assert supports[0] == supports[1] == supports[2] == supports[3]
    support = supports[0]
    assert len(support) in (2, 3)
    anchor = support[0]
    normalized = []
    for normal in normals:
        inverse = pow(normal[anchor], -1, prime)
        normalized.append(
            tuple(value * inverse % prime for value in normal)
        )
    reference = normalized[0]
    for normal in normalized[1:]:
        for coordinate in support[1:]:
            assert normal[coordinate] in (
                reference[coordinate],
                -reference[coordinate] % prime,
            )
    multiplicities = Counter(normalized)
    if len(support) == 2:
        assert sorted(multiplicities.values()) == [2, 2]
    else:
        assert sorted(multiplicities.values()) == [1, 1, 1, 1]
    return len(support)


def audit_prime(prime: int) -> dict[str, object]:
    all_planes = planes(prime)
    expected_planes = (prime**3 - 1) // (prime - 1)
    assert len(all_planes) == expected_planes
    full = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
    subspaces = all_planes + (full,)

    profile_counts: Counter[str] = Counter()
    normal_support_counts: Counter[int] = Counter()
    zero_count = 0
    checked = 0
    for first in subspaces:
        for second in subspaces:
            for third in subspaces:
                checked += 1
                values = tensor(first, second, third, prime)
                if not any(values):
                    zero_count += 1
                    continue
                dimensions = (len(first), len(second), len(third))
                ranks = flattening_ranks(values, dimensions, prime)
                if ranks != (1, 1, 1):
                    continue
                profile = "".join(str(value) for value in dimensions)
                profile_counts[profile] += 1
                assert dimensions == (2, 2, 2)
                support = validate_sign_family(
                    (
                        plane_normal(first, prime),
                        plane_normal(second, prime),
                        plane_normal(third, prime),
                    ),
                    prime,
                )
                normal_support_counts[support] += 1

    assert zero_count == 3
    assert profile_counts == Counter(
        {"222": 9 * (prime - 1) + 6 * (prime - 1) ** 2}
    )
    assert normal_support_counts == Counter(
        {
            2: 9 * (prime - 1),
            3: 6 * (prime - 1) ** 2,
        }
    )

    triple_kinds = {}
    for first_index, first in enumerate(all_planes):
        for second_index, second in enumerate(all_planes):
            for third_index, third in enumerate(all_planes):
                values = tensor(first, second, third, prime)
                key = (first_index, second_index, third_index)
                if not any(values):
                    triple_kinds[key] = "zero"
                elif flattening_ranks(values, (2, 2, 2), prime) == (
                    1,
                    1,
                    1,
                ):
                    triple_kinds[key] = "pure"
                else:
                    triple_kinds[key] = "other"

    quadruple_kind_counts: Counter[str] = Counter()
    quadruple_support_counts: Counter[int] = Counter()
    quadruples_checked = 0
    for first in range(len(all_planes)):
        for second in range(len(all_planes)):
            for third in range(len(all_planes)):
                for fourth in range(len(all_planes)):
                    quadruples_checked += 1
                    kinds = (
                        triple_kinds[(second, third, fourth)],
                        triple_kinds[(first, third, fourth)],
                        triple_kinds[(first, second, fourth)],
                        triple_kinds[(first, second, third)],
                    )
                    if "other" in kinds:
                        continue
                    pattern = ",".join(kinds)
                    quadruple_kind_counts[pattern] += 1
                    if pattern == "pure,pure,pure,pure":
                        support = validate_sign_rectangle(
                            tuple(
                                plane_normal(all_planes[index], prime)
                                for index in (
                                    first,
                                    second,
                                    third,
                                    fourth,
                                )
                            ),
                            prime,
                        )
                        quadruple_support_counts[support] += 1

    assert quadruple_kind_counts == Counter(
        {
            "zero,zero,zero,zero": 3,
            "pure,pure,pure,pure": (
                9 * (prime - 1) + 6 * (prime - 1) ** 2
            ),
        }
    )
    assert quadruple_support_counts == Counter(
        {
            2: 9 * (prime - 1),
            3: 6 * (prime - 1) ** 2,
        }
    )
    return {
        "planes": len(all_planes),
        "rank_at_least_two_subspaces": len(subspaces),
        "ordered_subspace_triples_checked": checked,
        "zero_restrictions": zero_count,
        "decomposable_rank_profiles": dict(profile_counts),
        "normal_support_counts": dict(normal_support_counts),
        "ordered_plane_quadruples_checked": quadruples_checked,
        "admissible_quadruple_kind_counts": dict(
            quadruple_kind_counts
        ),
        "pure_quadruple_normal_support_counts": dict(
            quadruple_support_counts
        ),
    }


def main() -> None:
    audits = {str(prime): audit_prime(prime) for prime in (3, 5)}
    output = {
        "audited": True,
        "finite_fields": ["F_3", "F_5"],
        "audits": audits,
        "allowed_rank_profile": "222",
        "support_two_formula": "9*(p-1)",
        "support_three_formula": "6*(p-1)^2",
        "four_plane_allowed_kind_patterns": [
            "all_zero",
            "all_nonzero_decomposable",
        ],
        "theorem": THEOREM.name,
        "theorem_sha256": sha256(THEOREM),
        "source": Path(__file__).name,
        "source_sha256": sha256(Path(__file__)),
        "scope": "finite-field audit; written theorem is over C",
        "global_conjecture_resolved": False,
    }
    output_path = (
        ROOT
        / "tmp"
        / "p3_decomposable_restriction_classification_audited.json"
    )
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(
        json.dumps(output, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
