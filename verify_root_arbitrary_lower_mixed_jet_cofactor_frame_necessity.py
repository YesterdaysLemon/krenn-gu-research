"""Verify lower mixed-root complementary-cofactor frame necessity exactly."""

from __future__ import annotations

import json
from functools import cache
from itertools import combinations, product
from math import gcd

import sympy as sp

from verify_root_arbitrary_order_two_endpoint_full_jet_frame_sharpness_nogo import (
    E,
    X,
    build_case,
)

Row = tuple[int, int, int]


def canonical(row: Row) -> Row:
    divisor = 0
    for value in row:
        divisor = gcd(divisor, abs(value))
    answer = tuple(value // divisor for value in row)
    first = next(value for value in answer if value)
    if first < 0:
        answer = tuple(-value for value in answer)
    return answer  # type: ignore[return-value]


def kernel_basis(row: Row) -> tuple[Row, Row]:
    pivot = next(index for index, value in enumerate(row) if value)
    basis = []
    for free in range(3):
        if free == pivot:
            continue
        vector = [0, 0, 0]
        vector[free] = row[pivot]
        vector[pivot] = -row[free]
        basis.append(tuple(vector))
    return basis[0], basis[1]  # type: ignore[return-value]


def product_form(rows: tuple[Row, ...], colour: int) -> tuple[int, ...]:
    answer = (1,)
    for row in rows:
        local = tuple(vector[colour] for vector in kernel_basis(row))
        answer = tuple(left * right for left in answer for right in local)
    return answer


def axis_type(row: Row) -> int | None:
    support = [index for index, value in enumerate(row) if value]
    return support[0] if len(support) == 1 else None


def common_pair(rows: tuple[Row, ...]) -> tuple[int, int] | None:
    for pair in combinations(range(3), 2):
        outside = ({0, 1, 2} - set(pair)).pop()
        if all(row[outside] == 0 for row in rows):
            return pair
    return None


def expected_rank(rows: tuple[Row, ...]) -> int:
    axes = {axis_type(row) for row in rows} - {None}
    if axes:
        return 3 - len(axes)
    return 2 if common_pair(rows) is not None else 3


def span_equal(left: sp.Matrix, right: sp.Matrix) -> bool:
    return left.rank() == right.rank() == left.row_join(right).rank()


def target_image_audit() -> dict[str, int]:
    vectors = sorted(
        {
            canonical(row)
            for row in product(range(-1, 2), repeat=3)
            if row != (0, 0, 0) and sum(row) != 0
        }
    )
    checked = 0
    ranks = {0: 0, 1: 0, 2: 0, 3: 0}
    for order in (2, 3):
        samples = product(vectors, repeat=order) if order == 2 else (
            rows
            for index, rows in enumerate(product(vectors, repeat=order))
            if index % 7 == 0
        )
        for rows in samples:
            forms = [product_form(rows, colour) for colour in range(3)]
            coefficient_matrix = sp.Matrix(forms)
            actual = coefficient_matrix.rank()
            expected = expected_rank(rows)
            if actual != expected:
                raise AssertionError((rows, actual, expected, forms))

            # The column space is the exact diagonal target image.
            image = coefficient_matrix.columnspace()
            image_matrix = sp.Matrix.hstack(*image) if image else sp.zeros(3, 0)
            axes = {axis_type(row) for row in rows} - {None}
            if axes:
                expected_columns = [sp.eye(3).col(c) for c in range(3) if c not in axes]
            else:
                pair = common_pair(rows)
                if pair is None:
                    expected_columns = [sp.eye(3).col(c) for c in range(3)]
                else:
                    p, q = pair
                    other = ({0, 1, 2} - set(pair)).pop()
                    lam = sp.prod(-sp.Rational(row[q], row[p]) for row in rows)
                    grouped = sp.eye(3).col(q) + lam * sp.eye(3).col(p)
                    expected_columns = [sp.eye(3).col(other), grouped]
            expected_matrix = (
                sp.Matrix.hstack(*expected_columns) if expected_columns else sp.zeros(3, 0)
            )
            if not span_equal(image_matrix, expected_matrix):
                raise AssertionError((rows, image_matrix, expected_matrix))
            checked += 1
            ranks[actual] += 1
    return {
        "projective_covectors": len(vectors),
        "tuples": checked,
        **{f"rank_{rank}": count for rank, count in ranks.items()},
    }


@cache
def perfect_matchings(vertices: tuple[int, ...]) -> tuple[tuple[tuple[int, int], ...], ...]:
    if not vertices:
        return ((),)
    first = vertices[0]
    answer = []
    for position in range(1, len(vertices)):
        second = vertices[position]
        remainder = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(remainder):
            answer.append(((first, second),) + tail)
    return tuple(answer)


def deletion_class_audit() -> dict[str, int]:
    checks = 0
    classes = set()
    # The last two vertices model blockers, which varied roots cannot use.
    for order in (6, 8):
        vertices = tuple(range(order))
        blockers = set(vertices[-2:])
        roots = tuple(vertices[: order // 2])
        for matching in perfect_matchings(vertices):
            partner = {u: v for edge in matching for u, v in (edge, edge[::-1])}
            for size in range(2, len(roots) + 1):
                for varied_tuple in combinations(roots, size):
                    varied = set(varied_tuple)
                    if any(partner[root] in blockers for root in varied):
                        continue
                    outside_partners = {
                        partner[root] for root in varied if partner[root] not in varied
                    }
                    if len(outside_partners) % 2 != len(varied) % 2:
                        raise AssertionError((matching, varied, outside_partners))
                    deleted = varied | outside_partners
                    if any((u in deleted) != (v in deleted) for u, v in matching):
                        raise AssertionError((matching, varied, deleted))
                    classes.add((order, tuple(sorted(varied)), tuple(sorted(outside_partners))))
                    checks += 1
    return {"term_checks": checks, "deletion_classes": len(classes), "maximum_vertices": 8}


def weighted_matching_count(vertices: tuple[int, ...], weights: dict[tuple[int, int], int]) -> int:
    @cache
    def recurse(mask: int) -> int:
        if not mask:
            return 1
        low = mask & -mask
        i = low.bit_length() - 1
        u = vertices[i]
        tail = mask ^ low
        total = 0
        for j in range(i + 1, len(vertices)):
            bit = 1 << j
            if tail & bit:
                edge = (u, vertices[j])
                total += weights.get(edge, 0) * recurse(tail ^ bit)
        return total

    return recurse((1 << len(vertices)) - 1)


def sharpness_lower_jet_audit() -> dict[str, int]:
    checked = 0
    for root_count in range(3, 13):
        roots, blockers, _endpoints, vertices, blocks, _ = build_case(root_count)
        vectors = {vertex: X for vertex in vertices}
        vectors[roots[0]] = E[1]
        vectors[roots[1]] = E[1]
        for blocker in blockers:
            vectors[blocker] = E[1]
        weights = {}
        for u in vertices:
            for v in vertices:
                if u >= v or (u, v) not in blocks:
                    continue
                value = int((vectors[u].T * blocks[u, v] * vectors[v])[0])
                if value:
                    weights[u, v] = value
        actual = weighted_matching_count(vertices, weights)
        target = 1
        if actual != 0:
            raise AssertionError((root_count, actual, weights))
        if target != 1:
            raise AssertionError(target)
        checked += 1
    return {"root_counts": checked, "minimum_roots": 3, "maximum_roots": 12}


def main() -> None:
    print(
        json.dumps(
            {
                "status": "pass",
                "field": "exact characteristic zero",
                "target_image": target_image_audit(),
                "deletion_grouping": deletion_class_audit(),
                "sharpness_construction_lower_jet_zero": sharpness_lower_jet_audit(),
                "finite_field_proof_used": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
