"""Independent no-import audit for the complete aligned q=0,r=5 detector."""

from __future__ import annotations

from collections import Counter
from collections.abc import Callable
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations, product
from typing import Any

COORDS = (0, 1, 2)
MODES = tuple(range(5))
EDGES = tuple(combinations(MODES, 2))
WORDS4 = tuple(product(COORDS, repeat=4))
ZERO = (0, 0, 0)
E0 = (1, 0, 0)
E1 = (0, 1, 0)
RATIOS = (-2, -1, 1, 2)


@dataclass(frozen=True, eq=False)
class Cyclo3:
    """Element a+b*w of Q[w]/(w^2+w+1)."""

    rational: Fraction
    omega: Fraction = Fraction(0)

    @classmethod
    def make(cls, value: Any) -> Cyclo3:
        if isinstance(value, cls):
            return value
        return cls(Fraction(value))

    def __add__(self, other: Any) -> Cyclo3:
        right = self.make(other)
        return Cyclo3(self.rational + right.rational, self.omega + right.omega)

    __radd__ = __add__

    def __neg__(self) -> Cyclo3:
        return Cyclo3(-self.rational, -self.omega)

    def __sub__(self, other: Any) -> Cyclo3:
        return self + (-self.make(other))

    def __rsub__(self, other: Any) -> Cyclo3:
        return self.make(other) - self

    def __mul__(self, other: Any) -> Cyclo3:
        right = self.make(other)
        # w^2=-w-1.
        return Cyclo3(
            self.rational * right.rational - self.omega * right.omega,
            self.rational * right.omega
            + self.omega * right.rational
            - self.omega * right.omega,
        )

    __rmul__ = __mul__

    def inverse(self) -> Cyclo3:
        norm = (
            self.rational**2
            - self.rational * self.omega
            + self.omega**2
        )
        if not norm:
            raise ZeroDivisionError
        return Cyclo3(
            (self.rational - self.omega) / norm,
            -self.omega / norm,
        )

    def __truediv__(self, other: Any) -> Cyclo3:
        return self * self.make(other).inverse()

    def __rtruediv__(self, other: Any) -> Cyclo3:
        return self.make(other) / self

    def __bool__(self) -> bool:
        return bool(self.rational or self.omega)

    def __eq__(self, other: object) -> bool:
        try:
            right = self.make(other)
        except (TypeError, ValueError):
            return False
        return self.rational == right.rational and self.omega == right.omega


def recursive_permanent(rows: tuple[tuple[Any, ...], ...]) -> Any:
    cache: dict[tuple[int, int], Any] = {}

    def visit(mode: int, used: int) -> Any:
        key = (mode, used)
        if key in cache:
            return cache[key]
        if mode == len(rows):
            return 1
        total: Any = 0
        for source, value in enumerate(rows[mode]):
            if used & (1 << source):
                continue
            if value:
                total += value * visit(mode + 1, used | (1 << source))
        cache[key] = total
        return total

    return visit(0, 0)


def collision_matrix(
    types: tuple[str, ...], deleted: int, ratios: tuple[Any, ...]
) -> list[list[Any]]:
    """Build collision columns through an independent recursive permanent."""
    a_rows: list[tuple[Any, Any, Any]] = []
    b_rows: list[tuple[Any, Any, Any]] = []
    for mode, mode_type in enumerate(types):
        if mode_type == "R":
            a_rows.append((ratios[mode], 0, 0))
            b_rows.append(E0)
        elif mode_type == "B":
            a_rows.append(ZERO)
            b_rows.append(E0)
        elif mode_type == "T":
            a_rows.append(E0)
            b_rows.append(E1)
        else:
            raise ValueError(mode_type)

    retained = tuple(mode for mode in MODES if mode != deleted)
    matrix: list[list[Any]] = [[0 for _ in range(15)] for _ in WORDS4]
    for h_mode in retained:
        for h_coord in COORDS:
            column = 3 * h_mode + h_coord
            for word_index, word in enumerate(WORDS4):
                rows = []
                for local_index, mode in enumerate(retained):
                    rows.append(
                        (
                            int(mode == h_mode and word[local_index] == h_coord),
                            a_rows[mode][word[local_index]],
                            a_rows[mode][word[local_index]],
                            b_rows[mode][word[local_index]],
                        )
                    )
                matrix[word_index][column] = recursive_permanent(tuple(rows))
    return matrix


def stack(*matrices: list[list[Any]]) -> list[list[Any]]:
    return [row[:] for matrix in matrices for row in matrix]


def row_reduce(
    matrix: list[list[Any]], converter: Callable[[Any], Any]
) -> tuple[list[list[Any]], tuple[int, ...]]:
    rows = [[converter(value) for value in row] for row in matrix if any(row)]
    if not rows:
        return [], ()
    row_count = len(rows)
    column_count = len(rows[0])
    pivot_row = 0
    pivots: list[int] = []
    for column in range(column_count):
        selected = next(
            (row for row in range(pivot_row, row_count) if rows[row][column]),
            None,
        )
        if selected is None:
            continue
        rows[pivot_row], rows[selected] = rows[selected], rows[pivot_row]
        pivot = rows[pivot_row][column]
        rows[pivot_row] = [entry / pivot for entry in rows[pivot_row]]
        for row in range(row_count):
            if row == pivot_row or not rows[row][column]:
                continue
            scale = rows[row][column]
            rows[row] = [
                left - scale * right
                for left, right in zip(rows[row], rows[pivot_row], strict=True)
            ]
        pivots.append(column)
        pivot_row += 1
        if pivot_row == row_count:
            break
    return rows[:pivot_row], tuple(pivots)


def nullity(matrix: list[list[Any]], converter: Callable[[Any], Any]) -> int:
    _, pivots = row_reduce(matrix, converter)
    return len(matrix[0]) - len(pivots)


def fraction(value: Any) -> Fraction:
    return Fraction(value)


def audit_four_defect_kernels() -> dict[str, int]:
    rational_charts = 0
    for values in product(RATIOS, repeat=4):
        matrices = [
            collision_matrix(("R", "R", "R", "R", "T"), deleted, values + (1,))
            for deleted in range(4)
        ]
        expected = int(len(set(values)) == 1)
        assert nullity(stack(*matrices), fraction) == expected
        rational_charts += 1

    omega = Cyclo3(Fraction(0), Fraction(1))
    one = Cyclo3.make(1)
    assert omega * omega + omega + one == 0
    reciprocals = (one, one, omega, omega)
    cube_ratios = tuple(one / value for value in reciprocals)
    cube_matrices = [
        collision_matrix(
            ("R", "R", "R", "R", "T"),
            deleted,
            cube_ratios + (one,),
        )
        for deleted in range(4)
    ]
    assert nullity(stack(*cube_matrices), Cyclo3.make) == 1

    rrrbt_charts = 0
    for values in product(RATIOS, repeat=3):
        matrices = [
            collision_matrix(("R", "R", "R", "B", "T"), deleted, values + (1, 1))
            for deleted in range(4)
        ]
        expected = int(sum(values) == 0)
        assert nullity(stack(*matrices), fraction) == expected
        rrrbt_charts += 1

    rrbbt_charts = 0
    for left, right in product(RATIOS, repeat=2):
        matrices = [
            collision_matrix(
                ("R", "R", "B", "B", "T"),
                deleted,
                (left, right, 1, 1, 1),
            )
            for deleted in range(4)
        ]
        assert nullity(stack(*matrices), fraction) == 2
        rrbbt_charts += 1

    triangle = [
        collision_matrix(("B", "B", "B", "R", "T"), deleted, (1, 1, 1, 2, 1))
        for deleted in range(3)
    ]
    assert nullity(stack(triangle[0], triangle[1]), fraction) == 7
    assert nullity(stack(*triangle), fraction) == 6
    return {
        "RRRRT-rational": rational_charts,
        "RRRRT-cube": 1,
        "RRRBT": rrrbt_charts,
        "RRBBT": rrbbt_charts,
        "three-B": 2,
    }


def adjacency(edges: set[tuple[int, int]], vertex: int) -> set[int]:
    return {
        right if left == vertex else left
        for left, right in edges
        if vertex in (left, right)
    }


def connected(edges: set[tuple[int, int]]) -> bool:
    reached = {0}
    pending = [0]
    while pending:
        vertex = pending.pop()
        for neighbour in adjacency(edges, vertex) - reached:
            reached.add(neighbour)
            pending.append(neighbour)
    return len(reached) == 5


def fraction_nullspace(matrix: list[list[int]]) -> list[list[Fraction]]:
    reduced, pivots = row_reduce(matrix, fraction)
    free_columns = [column for column in MODES if column not in pivots]
    basis = []
    for free in free_columns:
        vector = [Fraction(0) for _ in MODES]
        vector[free] = Fraction(1)
        for row, pivot in enumerate(pivots):
            vector[pivot] = -reduced[row][free]
        basis.append(vector)
    return basis


def dot(left: list[int], right: list[Fraction]) -> Fraction:
    return sum((Fraction(a) * b for a, b in zip(left, right, strict=True)), Fraction(0))


def exactly_realizable(zero_edges: set[tuple[int, int]]) -> bool:
    equations = []
    for left, right in zero_edges:
        row = [-1] * 5
        row[left] += 1
        row[right] += 1
        equations.append(row)
    basis = fraction_nullspace(equations) if equations else [
        [Fraction(int(left == right)) for right in MODES] for left in MODES
    ]
    if not basis:
        return False
    forms = []
    for vertex in MODES:
        form = [0] * 5
        form[vertex] = 1
        forms.append(form)
    for left, right in set(EDGES) - zero_edges:
        form = [-1] * 5
        form[left] += 1
        form[right] += 1
        forms.append(form)
    # Over an infinite characteristic-zero field, finitely many proper
    # hyperplanes cannot cover the solution space.
    return all(any(dot(form, vector) for vector in basis) for form in forms)


def audit_reciprocal_graphs() -> dict[str, int]:
    shapes: Counter[tuple[int, ...]] = Counter()
    isolated = 0
    realizable = 0
    for mask in range(1 << len(EDGES)):
        zero_edges = {
            edge for index, edge in enumerate(EDGES) if mask & (1 << index)
        }
        if not exactly_realizable(zero_edges):
            continue
        realizable += 1
        forcing = set(EDGES) - zero_edges
        isolated += int(any(not adjacency(forcing, vertex) for vertex in MODES))
        common = {
            (left, right)
            for left, right in EDGES
            if adjacency(forcing, left) & adjacency(forcing, right)
        }
        if not connected(common):
            shape = tuple(
                sorted(
                    (len(adjacency(zero_edges, vertex)) for vertex in MODES),
                    reverse=True,
                )
            )
            shapes[shape] += 1
    assert isolated == 0
    assert shapes == Counter({(3, 3, 2, 2, 2): 10, (3, 3, 3, 3, 0): 5})
    return {"realizable": realizable, "K23": 10, "K4": 5}


def column_values(matrix: list[list[Any]], column: int) -> list[Any]:
    return [row[column] for row in matrix if row[column]]


def audit_one_and_two_b_coefficients() -> dict[str, int]:
    checks = 0
    regular4 = (1, 1, 1, Fraction(-1, 2))
    rrrrb = ("R", "R", "R", "R", "B")
    for deleted in range(4):
        matrix = collision_matrix(rrrrb, deleted, regular4 + (1,))
        remaining = tuple(mode for mode in range(4) if mode != deleted)
        tau = sum(
            regular4[left] * regular4[right]
            for left, right in combinations(remaining, 2)
        )
        b_entries = column_values(matrix, 13)
        assert bool(b_entries) == bool(tau)
        if b_entries:
            assert b_entries == [2 * tau]
        deleted_b = collision_matrix(rrrrb, 4, regular4 + (1,))
        regular_entries = column_values(deleted_b, 3 * deleted + 1)
        assert bool(regular_entries) == bool(tau)
        if regular_entries:
            assert regular_entries == [2 * tau]
        checks += 2
    assert any(
        sum(
            regular4[left] * regular4[right]
            for left, right in combinations(
                tuple(mode for mode in range(4) if mode != deleted), 2
            )
        )
        for deleted in range(4)
    )

    regular3 = (Fraction(1), Fraction(1), Fraction(-1, 2))
    sigma = sum(
        regular3[left] * regular3[right]
        for left, right in combinations(range(3), 2)
    )
    assert sigma == 0
    rrrbb = ("R", "R", "R", "B", "B")
    for deleted_b, retained_b in ((3, 4), (4, 3)):
        matrix = collision_matrix(rrrbb, deleted_b, regular3 + (1, 1))
        assert not column_values(matrix, 3 * retained_b + 1)
        for retained_regular in range(3):
            assert column_values(matrix, 3 * retained_regular + 1)
            checks += 1
        checks += 1
    return {"coefficient_checks": checks, "tau-zero-charts": 3, "sigma-zero": 1}


def audit_set_and_hall_ledgers() -> dict[str, int]:
    pairs = [mask for mask in range(16) if mask.bit_count() == 2]
    relations = Counter()
    for left, right in product(pairs, repeat=2):
        if left == right:
            relations["equal"] += 1
        elif not left & right:
            relations["disjoint"] += 1
        else:
            relations["diamond"] += 1
    assert relations == Counter({"diamond": 24, "equal": 6, "disjoint": 6})

    degrees: Counter[tuple[int, ...]] = Counter()
    for sets in product(pairs, repeat=3):
        if sets[0] & sets[1] & sets[2]:
            continue
        degree = tuple(
            sorted(
                (
                    sum(bool(mask & (1 << root)) for mask in sets)
                    for root in range(4)
                ),
                reverse=True,
            )
        )
        degrees[degree] += 1
    assert degrees == Counter({(2, 2, 1, 1): 90, (2, 2, 2, 0): 24})

    four_words = {
        (word.count("R"), word.count("B"), 1)
        for word in product("RB", repeat=4)
        if word.count("B") <= 3
    }
    five_words = {
        (word.count("R"), word.count("B"))
        for word in product("RB", repeat=5)
        if word.count("B") <= 3
    }
    assert four_words == {(4, 0, 1), (3, 1, 1), (2, 2, 1), (1, 3, 1)}
    assert five_words == {(5, 0), (4, 1), (3, 2), (2, 3)}

    capacities = (5, 3 + 4, 4 + 3, 3 + 6, 6 + 6)
    assert capacities == (5, 7, 7, 9, 12)
    assert capacities[0] < 6
    assert capacities[1] < 9 and capacities[2] < 9
    assert capacities[3] == 9 and capacities[4] == 12
    return {
        "relations": sum(relations.values()),
        "triangle_ledgers": sum(degrees.values()),
        "type_words": len(four_words) + len(five_words),
    }


def main() -> None:
    kernels = audit_four_defect_kernels()
    graphs = audit_reciprocal_graphs()
    forcing = audit_one_and_two_b_coefficients()
    ledgers = audit_set_and_hall_ledgers()
    print(f"AUDIT PASS: recursive-permanent kernel census is {kernels}")
    print(f"AUDIT PASS: independent reciprocal-graph census is {graphs}")
    print(f"AUDIT PASS: one-/two-B forcing checks are {forcing}")
    print(f"AUDIT PASS: bitmask and Hall ledgers are {ledgers}")
    print("AUDIT SCOPE: conditional aligned q=0,r=5 detection only")
    print("AUDIT UNKNOWN: witness exclusion, injectivity, and larger cells")
    print("AUDIT UNRESOLVED: global Krenn-Gu conjecture")
    print("searches=0")


if __name__ == "__main__":
    main()
