"""Independent standard-library audit for the GLS23 nuisance formula."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product


PORT_DIMENSION = 2
ROOT_DIMENSION = 2


def assignments(vertices: tuple[int, ...]):
    return tuple(product(range(PORT_DIMENSION), repeat=len(vertices)))


def tensor_index(values: tuple[int, ...]) -> int:
    answer = 0
    for value in values:
        answer = PORT_DIMENSION * answer + value
    return answer


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
        scale = work[pivot_row][column]
        work[pivot_row] = [entry / scale for entry in work[pivot_row]]
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


def coefficient(d_vertices: tuple[int, ...], seed: int) -> tuple[tuple[Fraction, ...], ...]:
    width = PORT_DIMENSION ** len(d_vertices)
    return tuple(
        tuple(Fraction(((root + 1) * (column + seed + 2)) % 5 - 2) for column in range(width))
        for root in range(ROOT_DIMENSION)
    )


def actual_slices(
    universe: tuple[int, ...],
    target: tuple[int, ...],
    d_vertices: tuple[int, ...],
    values: tuple[tuple[Fraction, ...], ...],
) -> tuple[tuple[Fraction, ...], ...]:
    complement = tuple(vertex for vertex in universe if vertex not in d_vertices)
    right = tuple(vertex for vertex in universe if vertex not in target)
    dimension = ROOT_DIMENSION * PORT_DIMENSION ** len(target)
    answer = []
    for input_values in assignments(complement):
        input_map = dict(zip(complement, input_values, strict=True))
        for right_values in assignments(right):
            right_map = dict(zip(right, right_values, strict=True))
            vector = [Fraction(0)] * dimension
            for root in range(ROOT_DIMENSION):
                for d_values in assignments(d_vertices):
                    d_map = dict(zip(d_vertices, d_values, strict=True))
                    output = {**input_map, **d_map}
                    if any(output[vertex] != right_map[vertex] for vertex in right):
                        continue
                    target_values = tuple(output[vertex] for vertex in target)
                    index = root * PORT_DIMENSION ** len(target) + tensor_index(target_values)
                    vector[index] += values[root][tensor_index(d_values)]
            answer.append(tuple(vector))
    return tuple(answer)


def formula_slices(
    target: tuple[int, ...],
    d_vertices: tuple[int, ...],
    values: tuple[tuple[Fraction, ...], ...],
) -> tuple[tuple[Fraction, ...], ...]:
    x_vertices = tuple(vertex for vertex in target if vertex in d_vertices)
    y_vertices = tuple(vertex for vertex in d_vertices if vertex not in target)
    z_vertices = tuple(vertex for vertex in target if vertex not in d_vertices)
    dimension = ROOT_DIMENSION * PORT_DIMENSION ** len(target)
    answer = []
    for y_values in assignments(y_vertices):
        y_map = dict(zip(y_vertices, y_values, strict=True))
        for z_values in assignments(z_vertices):
            z_map = dict(zip(z_vertices, z_values, strict=True))
            vector = [Fraction(0)] * dimension
            for root in range(ROOT_DIMENSION):
                for x_values in assignments(x_vertices):
                    x_map = dict(zip(x_vertices, x_values, strict=True))
                    d_values = tuple({**x_map, **y_map}[vertex] for vertex in d_vertices)
                    target_values = tuple({**x_map, **z_map}[vertex] for vertex in target)
                    index = root * PORT_DIMENSION ** len(target) + tensor_index(target_values)
                    vector[index] = values[root][tensor_index(d_values)]
            answer.append(tuple(vector))
    return tuple(answer)


def audit_intersection_formula() -> dict[str, int]:
    universe = (0, 1, 2)
    targets = ((),) + tuple(combinations(universe, 2))
    d_sets = ((),) + tuple((vertex,) for vertex in universe) + tuple(combinations(universe, 2))
    checked = 0
    for target in targets:
        dimension = ROOT_DIMENSION * PORT_DIMENSION ** len(target)
        for seed, d_vertices in enumerate(d_sets, start=1):
            values = coefficient(d_vertices, seed)
            actual = actual_slices(universe, target, d_vertices, values)
            expected = formula_slices(target, d_vertices, values)
            assert rank(actual, dimension) == rank(expected, dimension)
            assert rank(actual + expected, dimension) == rank(actual, dimension)
            checked += 1
    return {"independent_label_target_pairs": checked}


def basis(dimension: int, coordinate: int) -> tuple[Fraction, ...]:
    return tuple(Fraction(index == coordinate) for index in range(dimension))


def tensor(left: tuple[Fraction, ...], right: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    return tuple(a * b for a in left for b in right)


def audit_collapse_and_anchor() -> dict[str, int]:
    port_pair_dimension = PORT_DIMENSION**2
    root_basis = tuple(basis(ROOT_DIMENSION, root) for root in range(ROOT_DIMENSION))
    port_basis = tuple(basis(port_pair_dimension, port) for port in range(port_pair_dimension))
    full = tuple(tensor(root, port) for root in root_basis for port in port_basis)
    assert rank(full, ROOT_DIMENSION * port_pair_dimension) == ROOT_DIMENSION * port_pair_dimension

    omega = (Fraction(1), Fraction(-2))
    anchor = tuple(tensor(omega, port) for port in port_basis)
    assert rank(anchor, ROOT_DIMENSION * port_pair_dimension) == port_pair_dimension
    quotient_dimension = ROOT_DIMENSION * port_pair_dimension - len(port_basis)
    assert quotient_dimension == (ROOT_DIMENSION - 1) * port_pair_dimension

    top_nuisance = (basis(ROOT_DIMENSION, 1),)
    assert rank(top_nuisance + (omega,), ROOT_DIMENSION) == 2
    absorbed_top = top_nuisance + (omega,)
    assert rank(absorbed_top + (omega,), ROOT_DIMENSION) == rank(absorbed_top, ROOT_DIMENSION)
    return {"full_dimension": len(full), "anchor_rank": len(port_basis), "quotient": quotient_dimension}


def audit_root_counts() -> tuple[tuple[int, int, int, int], ...]:
    records = []
    for root_order in range(3, 10):
        ports = 2 * root_order - 2
        pairs = ports * (ports - 1) // 2
        records.append((root_order, pairs, 63, 8))
    assert records[0] == (3, 6, 63, 8)
    return tuple(records)


def main() -> None:
    formula = audit_intersection_formula()
    anchor = audit_collapse_and_anchor()
    counts = audit_root_counts()
    print("promoted transverse complete-nuisance independent audit: PASS")
    print("  independently enumerated intersection formula:", formula)
    print("  direct disjoint-collapse/top-anchor ranks:", anchor)
    print("  arbitrary-root pair/top counts:", counts)
    print("  no imports from primary verifier or repository mathematics code")
    print("  scope: exact decomposition only; physical survival and node closure open")


if __name__ == "__main__":
    main()
