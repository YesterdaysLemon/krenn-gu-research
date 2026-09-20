"""Independent exact audit of common-star binary cycle localization.

This portable checker imports no primary verifier or project scientific code.
It reconstructs the five-component control over Q[s]/(3*s^2+3*s+1),
evaluates the literal 20-vertex protected-K4 source, and separately checks
the component permanent formula and the directed-cycle sharp case.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
import itertools
import json
from pathlib import Path


@dataclass(frozen=True)
class Quadratic:
    """Element a+b*s with 3*s^2+3*s+1=0."""

    a: Fraction = Fraction(0)
    b: Fraction = Fraction(0)

    def __add__(self, other):
        other = quadratic(other)
        return Quadratic(self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __neg__(self):
        return Quadratic(-self.a, -self.b)

    def __sub__(self, other):
        return self + -quadratic(other)

    def __rsub__(self, other):
        return quadratic(other) - self

    def __mul__(self, other):
        other = quadratic(other)
        # s^2=-s-1/3.
        return Quadratic(
            self.a * other.a - self.b * other.b / 3,
            self.a * other.b + self.b * other.a - self.b * other.b,
        )

    __rmul__ = __mul__

    def __pow__(self, exponent):
        if exponent < 0:
            return self.inverse() ** (-exponent)
        result = ONE
        factor = self
        while exponent:
            if exponent & 1:
                result *= factor
            factor *= factor
            exponent //= 2
        return result

    def inverse(self):
        # The conjugate root is -1-s, so
        # (a+b*s)(a-b-b*s)=a^2-a*b+b^2/3.
        norm = self.a * self.a - self.a * self.b + self.b * self.b / 3
        if not norm:
            raise ZeroDivisionError
        return Quadratic((self.a - self.b) / norm, -self.b / norm)

    def __truediv__(self, other):
        return self * quadratic(other).inverse()

    def __bool__(self):
        return bool(self.a or self.b)

    def text(self):
        if not self.b:
            return str(self.a)
        return f"({self.a})+({self.b})*s"


def quadratic(value):
    if isinstance(value, Quadratic):
        return value
    if isinstance(value, (int, Fraction)):
        return Quadratic(Fraction(value))
    raise TypeError(value)


ZERO = Quadratic()
ONE = quadratic(1)
S = Quadratic(Fraction(0), Fraction(1))
Q = -ONE - S
W = S / 2

CYCLE = (0, 1, 2)
OUTSIDE = (3, 4)
MATCHINGS = {
    0: ((0, 1), (2, 3)),
    1: ((0, 2), (1, 3)),
}


def subsets(values):
    values = tuple(values)
    for size in range(len(values) + 1):
        yield from itertools.combinations(values, size)


def permanent(matrix, rows, columns):
    rows = tuple(rows)
    columns = tuple(columns)
    assert len(rows) == len(columns)
    return sum(
        (
            product(matrix[row][column] for row, column in zip(rows, order))
            for order in itertools.permutations(columns)
        ),
        ZERO,
    )


def product(values):
    result = ONE
    for value in values:
        result *= value
    return result


def local_source(a_matrix, b_matrix, rows, columns):
    rows = tuple(rows)
    columns = tuple(columns)
    return sum(
        (
            permanent(a_matrix, chosen_rows, chosen_columns)
            * permanent(b_matrix, chosen_rows, chosen_columns)
            for size in range(min(len(rows), len(columns)) + 1)
            for chosen_rows in itertools.combinations(rows, size)
            for chosen_columns in itertools.combinations(columns, size)
        ),
        ZERO,
    )


def control_matrices():
    a_matrix = [[ZERO for _ in range(5)] for _ in range(5)]
    b_matrix = [[ZERO for _ in range(5)] for _ in range(5)]
    arcs = []
    for source in CYCLE:
        target = (source + 1) % 3
        a_matrix[source][target] = ONE
        b_matrix[source][target] = Q
        arcs.append((source, target))
    for source in OUTSIDE:
        for target in CYCLE:
            a_matrix[source][target] = ONE
            b_matrix[source][target] = W
            arcs.append((source, target))
    return a_matrix, b_matrix, tuple(arcs)


def component_amplitude(a_matrix, b_matrix, word):
    rows = [component for component, color in enumerate(word) if color == 0]
    columns = [component for component, color in enumerate(word) if color == 1]
    return local_source(a_matrix, b_matrix, rows, columns)


def physical_graph(word, arcs):
    """Build the literal selected scalar graph on five protected K4s."""

    adjacency = [dict() for _ in range(20)]

    def add_edge(left, right, weight):
        assert left != right and weight
        assert right not in adjacency[left]
        adjacency[left][right] = weight
        adjacency[right][left] = weight

    for component, color in enumerate(word):
        for left, right in MATCHINGS[color]:
            add_edge(4 * component + left, 4 * component + right, ONE)

    for source, target in arcs:
        if word[source] != 0 or word[target] != 1:
            continue
        leaf_weight = Q if source in CYCLE else W
        add_edge(4 * source, 4 * target, ONE)
        add_edge(4 * source + 1, 4 * target + 2, leaf_weight)
    return adjacency


def physical_matching_source(adjacency):
    """Return exact weighted source and Boolean supported-matching count."""

    @lru_cache(maxsize=None)
    def recurse(remaining):
        if not remaining:
            return ONE, 1
        first = remaining[0]
        total = ZERO
        count = 0
        for position, second in enumerate(remaining[1:], 1):
            weight = adjacency[first].get(second, ZERO)
            if not weight:
                continue
            rest = remaining[1:position] + remaining[position + 1 :]
            subvalue, subcount = recurse(rest)
            total += weight * subvalue
            count += subcount
        return total, count

    return recurse(tuple(range(len(adjacency))))


def state_resources(arcs):
    vertices = {(shore, component) for shore in "LR" for component in range(5)}
    neighbors = {vertex: set() for vertex in vertices}
    for source, target in arcs:
        left = ("L", source)
        right = ("R", target)
        neighbors[left].add(right)
        neighbors[right].add(left)

    resources = []
    while vertices:
        root = min(vertices)
        vertices.remove(root)
        component = {root}
        stack = [root]
        while stack:
            current = stack.pop()
            for neighbor in neighbors[current]:
                if neighbor in vertices:
                    vertices.remove(neighbor)
                    component.add(neighbor)
                    stack.append(neighbor)
        resources.append(component)
    return resources


def fixed_column_coefficient(a_matrix, b_matrix, rows, columns):
    columns = tuple(columns)
    return sum(
        (
            permanent(a_matrix, chosen_rows, columns)
            * permanent(b_matrix, chosen_rows, columns)
            for chosen_rows in itertools.combinations(rows, len(columns))
        ),
        ZERO,
    )


def audit_face_control():
    assert 3 * S**2 + 3 * S + ONE == ZERO
    assert Q and W
    a_matrix, b_matrix, arcs = control_matrices()
    assert len(arcs) == 9
    assert all(bool(a_matrix[u][v]) == bool(b_matrix[u][v]) for u in range(5) for v in range(5))
    assert all(not (a_matrix[u][v] and a_matrix[v][u]) for u in range(5) for v in range(5))

    # Literal physical matching and the independent component-minor formula
    # agree for every binary word, not just the claimed face.
    amplitudes = {}
    support_counts = {}
    for word in itertools.product(range(2), repeat=5):
        component_value = component_amplitude(a_matrix, b_matrix, word)
        physical_value, support_count = physical_matching_source(physical_graph(word, arcs))
        assert physical_value == component_value
        key = "".join(map(str, word))
        amplitudes[key] = physical_value
        support_counts[key] = support_count

    face = {}
    for cycle_word in itertools.product(range(2), repeat=3):
        word = cycle_word + (0, 0)
        expected = ONE if cycle_word == (0, 0, 0) else ZERO
        assert amplitudes["".join(map(str, word))] == expected
        face["".join(map(str, cycle_word))] = expected.text()
    assert amplitudes["00010"] == ONE
    assert amplitudes["00001"] == ONE
    assert amplitudes["11111"] == ONE

    resources = state_resources(arcs)
    cycle_resource = next(resource for resource in resources if ("L", 0) in resource)
    assert {("L", vertex) for vertex in range(5)} <= cycle_resource
    assert {("R", vertex) for vertex in CYCLE} <= cycle_resource
    assert all(("R", vertex) not in cycle_resource for vertex in OUTSIDE)
    assert all({("L", vertex), ("R", vertex)} <= cycle_resource for vertex in CYCLE)
    assert all(
        (source, target) in arcs
        for source, target in ((0, 1), (1, 2), (2, 0))
    )
    assert not any(
        source in CYCLE and target in CYCLE and target != (source + 1) % 3
        for source, target in arcs
    )

    exterior_values = {}
    fixed_coefficients = {}
    deletion_cases = 0
    predecessor = {0: 2, 1: 0, 2: 1}
    for selected in subsets(CYCLE):
        selected_set = set(selected)
        value = local_source(a_matrix, b_matrix, OUTSIDE, selected)
        expected = (-ONE) ** len(selected) * Q ** len(selected) if len(selected) < 3 else ZERO
        assert value == expected
        exterior_values["".join(map(str, selected)) or "empty"] = value.text()

        coefficient = fixed_column_coefficient(a_matrix, b_matrix, OUTSIDE, selected)
        if len(selected) < 3:
            expected_coefficient = (-ONE - Q) ** len(selected)
        else:
            expected_coefficient = (-ONE - Q) ** 3 + Q**3
        assert coefficient == expected_coefficient
        fixed_coefficients["".join(map(str, selected)) or "empty"] = coefficient.text()

        if not selected or len(selected) == 3:
            continue
        entering_rows = tuple(
            predecessor[column]
            for column in selected
            if predecessor[column] not in selected_set
        )
        assert entering_rows
        left = local_source(a_matrix, b_matrix, OUTSIDE + entering_rows, selected)
        right = ZERO
        for chosen_rows in subsets(entering_rows):
            removed_columns = {((row + 1) % 3) for row in chosen_rows}
            surviving_columns = tuple(column for column in selected if column not in removed_columns)
            right += Q ** len(chosen_rows) * local_source(
                a_matrix,
                b_matrix,
                OUTSIDE,
                surviving_columns,
            )
        assert left == right == ZERO
        deletion_cases += 1

    return {
        "field_relation": "3*s^2+3*s+1=0",
        "components": 5,
        "physical_vertices": 20,
        "gadgets": len(arcs),
        "physical_words_checked": len(amplitudes),
        "component_physical_mismatches": 0,
        "face_amplitudes": face,
        "face_supported_matching_counts": {
            word[:3]: support_counts[word] for word in amplitudes if word.endswith("00")
        },
        "exterior_values": exterior_values,
        "fixed_column_coefficients": fixed_coefficients,
        "deletion_recurrences_checked": deletion_cases,
        "resource_sizes": sorted(len(resource) for resource in resources),
        "cycle_resource_shore_overlap": list(CYCLE),
        "outside_singleton_failures": {"00010": "1", "00001": "1"},
        "status": "ONE_FACE_CONTROL_NOT_FB",
    }


def cycle_matrices(order):
    a_matrix = [[ZERO for _ in range(order)] for _ in range(order)]
    b_matrix = [[ZERO for _ in range(order)] for _ in range(order)]
    arcs = []
    for source in range(order):
        target = (source + 1) % order
        a_matrix[source][target] = ONE
        b_matrix[source][target] = -ONE
        arcs.append((source, target))
    return a_matrix, b_matrix, tuple(arcs)


def audit_directed_cycle_sharp_case():
    checked = 0
    for order in (3, 4, 5):
        a_matrix, b_matrix, arcs = cycle_matrices(order)
        resources = state_resources_for_order(order, arcs)
        assert all(
            {component for shore, component in resource if shore == "L"}.isdisjoint(
                {component for shore, component in resource if shore == "R"}
            )
            for resource in resources
        )
        for word in itertools.product(range(2), repeat=order):
            actual = component_amplitude(a_matrix, b_matrix, word)
            expected = ONE if len(set(word)) == 1 else ZERO
            assert actual == expected
            checked += 1

        # A unique cycle product different from -1 fails its singleton cut.
        b_matrix[0][1] = quadratic(-2)
        singleton_word = (0,) + (1,) * (order - 1)
        assert component_amplitude(a_matrix, b_matrix, singleton_word) != ZERO
    return {"orders": [3, 4, 5], "binary_words_checked": checked, "q_mutations_rejected": 3}


def state_resources_for_order(order, arcs):
    vertices = {(shore, component) for shore in "LR" for component in range(order)}
    neighbors = {vertex: set() for vertex in vertices}
    for source, target in arcs:
        left, right = ("L", source), ("R", target)
        neighbors[left].add(right)
        neighbors[right].add(left)
    resources = []
    while vertices:
        root = min(vertices)
        vertices.remove(root)
        resource = {root}
        stack = [root]
        while stack:
            current = stack.pop()
            for neighbor in neighbors[current]:
                if neighbor in vertices:
                    vertices.remove(neighbor)
                    resource.add(neighbor)
                    stack.append(neighbor)
        resources.append(resource)
    return resources


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = {
        "face_control": audit_face_control(),
        "directed_cycle_sharp_case": audit_directed_cycle_sharp_case(),
        "independence": "standard library only; literal physical matcher",
        "global_status": "UNRESOLVED",
    }
    encoded = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8", newline="\n")
        print(json.dumps({"status": "PASS", "output": str(args.output)}))
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
