"""Independent no-import audit of the GLS41 pure-core/excess reduction."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations

Vector = tuple[Fraction, ...]


def unit(dimension: int, index: int) -> Vector:
    return tuple(Fraction(int(position == index)) for position in range(dimension))


def add(left: Vector, right: Vector) -> Vector:
    return tuple(a + b for a, b in zip(left, right, strict=True))


def scale(scalar: Fraction, vector: Vector) -> Vector:
    return tuple(scalar * entry for entry in vector)


def rank(vectors: list[Vector]) -> int:
    if not vectors:
        return 0
    rows = [list(vector) for vector in vectors if any(vector)]
    if not rows:
        return 0
    row = 0
    columns = len(rows[0])
    for column in range(columns):
        pivot = next(
            (candidate for candidate in range(row, len(rows)) if rows[candidate][column]),
            None,
        )
        if pivot is None:
            continue
        rows[row], rows[pivot] = rows[pivot], rows[row]
        pivot_value = rows[row][column]
        rows[row] = [entry / pivot_value for entry in rows[row]]
        for other in range(len(rows)):
            if other == row or not rows[other][column]:
                continue
            factor = rows[other][column]
            rows[other] = [
                entry - factor * pivot_entry
                for entry, pivot_entry in zip(rows[other], rows[row], strict=True)
            ]
        row += 1
        if row == len(rows):
            break
    return row


def in_span(vector: Vector, spanning: list[Vector]) -> bool:
    return rank(spanning + [vector]) == rank(spanning)


def intersection_from_finite_candidates(
    nuisance: list[Vector], core_basis: list[Vector], candidates: list[Vector]
) -> list[Vector]:
    intersection: list[Vector] = []
    for candidate in candidates:
        if in_span(candidate, nuisance) and not in_span(candidate, intersection):
            intersection.append(candidate)
    assert all(in_span(vector, core_basis) for vector in intersection)
    return intersection


def canonical_quotient_profiles() -> tuple[tuple[int, ...], tuple[int, ...]]:
    q_outside = tuple(k - 4 for k in range(4, 10))
    q_inside = tuple(k - 3 for k in range(4, 10))
    assert q_outside == (0, 1, 2, 3, 4, 5)
    assert q_inside == (1, 2, 3, 4, 5, 6)
    return q_outside, q_inside


def exhaustive_small_intersections() -> dict[str, int]:
    dimension = 4
    core = [unit(dimension, 0), unit(dimension, 1)]
    excess = [unit(dimension, 2), unit(dimension, 3)]
    candidates = [
        *core,
        add(core[0], core[1]),
        add(core[0], scale(Fraction(2), core[1])),
    ]
    nuisance_pool = [
        *core,
        *excess,
        add(core[0], excess[0]),
        add(core[1], excess[1]),
    ]
    pure_columns = [core[0], add(core[0], core[1])]

    checked = 0
    for size in range(len(nuisance_pool) + 1):
        for indices in combinations(range(len(nuisance_pool)), size):
            nuisance = [nuisance_pool[index] for index in indices]
            intersection = intersection_from_finite_candidates(
                nuisance, core, candidates
            )
            expected_intersection_dimension = (
                rank(nuisance) + rank(core) - rank(nuisance + core)
            )
            assert rank(intersection) == expected_intersection_dimension
            ambient_rise = rank(nuisance + pure_columns) - rank(nuisance)
            core_rise = rank(intersection + pure_columns) - rank(intersection)
            assert ambient_rise == core_rise

            middle_dimension = dimension - rank(nuisance)
            core_quotient = rank(core) - rank(intersection)
            projected_nuisance_rank = rank(
                [vector[2:] for vector in nuisance]
            )
            excess_quotient = len(excess) - projected_nuisance_rank
            assert middle_dimension == core_quotient + excess_quotient
            checked += 1
    return {"nuisance_subsets": checked, "ambient_dimension": dimension}


def response_dichotomy_fixtures() -> dict[str, int]:
    # Coordinates are (two pure-core rows, two excess rows).
    core = [unit(4, 0), unit(4, 1)]
    nuisance = [add(core[0], unit(4, 2))]
    projection_nuisance = [vector[2:] for vector in nuisance]

    nonzero_response_target = add(core[1], nuisance[0])
    assert in_span(nonzero_response_target[2:], projection_nuisance)

    zero_response_target = unit(4, 3)
    assert not in_span(zero_response_target[2:], projection_nuisance)
    return {"nonzero_response_core_represented": 1, "zero_response_excess": 1}


def jumping_family() -> dict[str, tuple[int, int, int]]:
    e0, e1 = unit(2, 0), unit(2, 1)
    data: dict[str, tuple[int, int, int]] = {}
    for name, parameter in (("special", Fraction(0)), ("generic", Fraction(3))):
        nuisance = [e1, scale(parameter, e0)]
        intersection = [e0] if parameter else []
        projection_rank = rank([vector[1:] for vector in nuisance])
        pure_rise = rank(intersection + [e0]) - rank(intersection)
        data[name] = (projection_rank, rank(intersection), pure_rise)
    assert data == {"special": (1, 0, 1), "generic": (1, 1, 0)}
    return data


def main() -> None:
    profiles = canonical_quotient_profiles()
    intersection_checks = exhaustive_small_intersections()
    response_checks = response_dichotomy_fixtures()
    jump = jumping_family()

    print("GLS41 independent no-import pure-core/excess audit: PASS")
    print("  quotient profiles:", profiles)
    print("  exhaustive small intersections:", intersection_checks)
    print("  response dichotomy fixtures:", response_checks)
    print("  constant-projection jumping family:", jump)
    print("  no imports from the primary verifier or repository mathematics code")


if __name__ == "__main__":
    main()
