"""Independent no-import audit for the GLS22 transverse quotient."""

from __future__ import annotations

from fractions import Fraction
from itertools import product


def dot(left: tuple[Fraction, ...], right: tuple[Fraction, ...]) -> Fraction:
    return sum((a * b for a, b in zip(left, right, strict=True)), Fraction(0))


def add(left: tuple[Fraction, ...], right: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    return tuple(a + b for a, b in zip(left, right, strict=True))


def scale(value: Fraction, vector: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    return tuple(value * entry for entry in vector)


def transverse(
    epsilon: tuple[Fraction, ...], q: tuple[Fraction, ...], vector: tuple[Fraction, ...]
) -> tuple[Fraction, ...]:
    p = dot(epsilon, q)
    return add(scale(p, vector), scale(-dot(epsilon, vector), q))


def rank(columns: tuple[tuple[Fraction, ...], ...], dimension: int) -> int:
    if not columns:
        return 0
    work = [[column[row] for column in columns] for row in range(dimension)]
    pivot_row = 0
    for column in range(len(columns)):
        pivot = next(
            (row for row in range(pivot_row, dimension) if work[row][column]), None
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        pivot_value = work[pivot_row][column]
        work[pivot_row] = [entry / pivot_value for entry in work[pivot_row]]
        for row in range(dimension):
            if row == pivot_row or work[row][column] == 0:
                continue
            factor = work[row][column]
            work[row] = [
                left - factor * right
                for left, right in zip(work[row], work[pivot_row], strict=True)
            ]
        pivot_row += 1
        if pivot_row == dimension:
            break
    return pivot_row


def audit_projector() -> dict[str, int]:
    epsilon = (Fraction(1), Fraction(2), Fraction(-1))
    q = (Fraction(2), Fraction(1), Fraction(3))
    p = dot(epsilon, q)
    assert p != 0
    assert transverse(epsilon, q, q) == (Fraction(0),) * 3
    images = tuple(
        transverse(
            epsilon,
            q,
            tuple(Fraction(index == coordinate) for index in range(3)),
        )
        for coordinate in range(3)
    )
    assert rank(images, 3) == 2
    assert all(dot(epsilon, image) == 0 for image in images)
    for image in images:
        assert transverse(epsilon, q, image) == scale(p, image)
    return {"p": int(p), "rank": rank(images, 3), "kernel": 1}


def audit_quotient_equivalence() -> dict[str, int]:
    epsilon = (Fraction(1), Fraction(2), Fraction(-1))
    q = (Fraction(2), Fraction(1), Fraction(3))
    all_vectors = tuple(
        tuple(Fraction(value) for value in entries)
        for entries in product((0, 1), repeat=3)
    )
    checked = 0
    survival = 0
    for extra in all_vectors:
        nuisance = (q, extra)
        projected_nuisance = tuple(transverse(epsilon, q, vector) for vector in nuisance)
        for desired in all_vectors:
            upstairs = rank(nuisance + (desired,), 3) > rank(nuisance, 3)
            projected = transverse(epsilon, q, desired)
            downstairs = rank(projected_nuisance + (projected,), 3) > rank(
                projected_nuisance, 3
            )
            assert upstairs == downstairs
            checked += 1
            survival += int(upstairs)
    assert survival
    return {"states": checked, "surviving": survival}


def tensor(left: tuple[Fraction, ...], right: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    return tuple(a * b for a in left for b in right)


def audit_source_aggregate() -> dict[str, int]:
    epsilon = (Fraction(1), Fraction(2), Fraction(-1))
    q = (Fraction(2), Fraction(1), Fraction(3))
    p = dot(epsilon, q)
    desired = (
        (Fraction(1), Fraction(0), Fraction(2)),
        (Fraction(0), Fraction(3), Fraction(-1)),
        (Fraction(2), Fraction(1), Fraction(1)),
    )
    tails = (
        (Fraction(1), Fraction(0)),
        (Fraction(0), Fraction(1)),
        (Fraction(1), Fraction(-1)),
    )
    f_q = (Fraction(0),) * 6
    pi_q = (Fraction(0),) * 2
    aggregate = (Fraction(0),) * 6
    for vector, tail in zip(desired, tails, strict=True):
        f_q = add(f_q, tensor(vector, tail))
        pi_q = add(pi_q, scale(dot(epsilon, vector), tail))
        aggregate = add(aggregate, tensor(transverse(epsilon, q, vector), tail))
    expected = add(scale(p, f_q), scale(-1, tensor(q, pi_q)))
    assert aggregate == expected
    contracted = tuple(
        sum(epsilon[root] * aggregate[2 * root + port] for root in range(3))
        for port in range(2)
    )
    assert contracted == (Fraction(0), Fraction(0))
    assert any(aggregate)

    synchronized = tuple(scale(value / p, q) for value in (Fraction(2), Fraction(-3), Fraction(5)))
    assert all(transverse(epsilon, q, vector) == (Fraction(0),) * 3 for vector in synchronized)
    return {"terms": len(desired), "aggregate_nonzero": int(any(aggregate))}


def audit_target_rank() -> tuple[int, int]:
    cases = 0
    useful = 0
    for survives, response_nonzero in product((False, True), repeat=2):
        left = (Fraction(2), Fraction(-1)) if survives else (Fraction(0),) * 2
        response = (
            (Fraction(3), Fraction(5), Fraction(7))
            if response_nonzero
            else (Fraction(0),) * 3
        )
        columns = tuple(
            tuple(left[row] * response[column] for row in range(2))
            for column in range(3)
        )
        observed = rank(columns, 2)
        assert observed == int(survives and response_nonzero)
        cases += 1
        useful += observed
    return cases, useful


def audit_target_counts() -> tuple[tuple[int, int, int, int], ...]:
    records = []
    for root_order in range(3, 10):
        ports = 2 * root_order - 2
        target_count = ports * (ports - 1) // 2 + 1
        records.append((root_order, target_count, 72, 8))
    assert records[0] == (3, 7, 72, 8)
    assert records[1] == (4, 16, 72, 8)
    return tuple(records)


def main() -> None:
    algebra = audit_projector()
    quotient = audit_quotient_equivalence()
    source = audit_source_aggregate()
    target = audit_target_rank()
    counts = audit_target_counts()
    print("promoted transverse-quotient independent audit: PASS")
    print("  coordinate-free projector identities:", algebra)
    print("  exhaustive small quotient states:", quotient)
    print("  independently assembled source aggregate:", source)
    print("  decomposable target states:", target)
    print("  arbitrary-root target dimensions:", counts)
    print("  no imports from primary verifier or repository mathematics code")
    print("  scope: equivalence/failure reduction only; no survival or node closure")


if __name__ == "__main__":
    main()
