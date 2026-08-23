"""Independent standard-library audit for GLS37.

This audit deliberately imports neither SymPy nor either GLS35/GLS37 primary
verifier.  It uses Fraction row reduction, a sparse matching-state expansion,
and an independently reconstructed physical control.
"""

from __future__ import annotations

from fractions import Fraction as F
from itertools import combinations, product


def rank(rows: list[list[F]]) -> int:
    work = [row[:] for row in rows]
    if not work:
        return 0
    pivot_row = 0
    for column in range(len(work[0])):
        pivot = next(
            (index for index in range(pivot_row, len(work)) if work[index][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [entry / scale for entry in work[pivot_row]]
        for index, row in enumerate(work):
            if index != pivot_row and row[column]:
                multiple = row[column]
                work[index] = [
                    left - multiple * right
                    for left, right in zip(row, work[pivot_row], strict=True)
                ]
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def column_rank(columns: list[tuple[F, ...]]) -> int:
    if not columns:
        return 0
    return rank([list(row) for row in zip(*columns, strict=True)])


def nullspace(rows: list[list[F]], width: int) -> list[tuple[F, ...]]:
    work = [row[:] for row in rows]
    pivot_columns: list[int] = []
    pivot_row = 0
    for column in range(width):
        pivot = next(
            (index for index in range(pivot_row, len(work)) if work[index][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [entry / scale for entry in work[pivot_row]]
        for index, row in enumerate(work):
            if index != pivot_row and row[column]:
                multiple = row[column]
                work[index] = [
                    left - multiple * right
                    for left, right in zip(row, work[pivot_row], strict=True)
                ]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == len(work):
            break
    free = [column for column in range(width) if column not in pivot_columns]
    answer: list[tuple[F, ...]] = []
    for free_column in free:
        vector = [F(0) for _ in range(width)]
        vector[free_column] = F(1)
        for row_index, pivot_column in reversed(list(enumerate(pivot_columns))):
            vector[pivot_column] = -sum(
                work[row_index][column] * vector[column]
                for column in free
            )
        answer.append(tuple(vector))
    return answer


def inverse_2(matrix: tuple[tuple[F, F], tuple[F, F]]) -> tuple[tuple[F, F], tuple[F, F]]:
    a, b = matrix[0]
    c, d = matrix[1]
    determinant = a * d - b * c
    assert determinant
    return ((d / determinant, -b / determinant), (-c / determinant, a / determinant))


def audit_two_shore_support() -> tuple[int, tuple[int, ...]]:
    """Audit the missing-colour support argument on many exact shore charts."""

    checked = 0
    channel_dimensions: set[int] = set()
    diagonal = ((F(2), F(0)), (F(0), F(3)))
    exchange = ((F(0), F(1)), (F(1), F(0)))
    for entries in product(range(-2, 3), repeat=4):
        left = ((F(entries[0]), F(entries[1])), (F(entries[2]), F(entries[3])))
        determinant = left[0][0] * left[1][1] - left[0][1] * left[1][0]
        if not determinant:
            continue
        inverse = inverse_2(left)
        # right^T = J left^{-1} diagonal, independently reconstructing
        # left J right^T = diagonal.
        right_t = tuple(
            tuple(
                sum(exchange[i][k] * inverse[k][j] * diagonal[j][j] for k in range(2))
                for j in range(2)
            )
            for i in range(2)
        )
        right = tuple(tuple(right_t[j][i] for j in range(2)) for i in range(2))

        # Variables are (p_0,p_1,p_2,y_0,y_1,y_2).  For s=0,1 impose every
        # off-diagonal coefficient of a_s tensor y+p tensor b_s to be zero.
        rows: list[list[F]] = []
        for s in range(2):
            a = (left[0][s], left[1][s], F(0))
            b = (right[0][s], right[1][s], F(0))
            for i in range(3):
                for j in range(3):
                    if i == j:
                        continue
                    row = [F(0) for _ in range(6)]
                    row[i] = b[j]
                    row[3 + j] = a[i]
                    rows.append(row)
        kernel = nullspace(rows, 6)
        assert all(vector[2] == vector[5] == 0 for vector in kernel)
        channel_dimensions.add(len(kernel))

        # Every tensor formed from the two port halves is supported on the
        # upper-left two-colour plane.  Its intersection with the diagonal
        # has only the two coordinates 00 and 11.
        for first in kernel:
            p, y = first[:3], first[3:]
            for second in kernel:
                p2, y2 = second[:3], second[3:]
                pair = tuple(
                    p[i] * y2[j] + p2[i] * y[j]
                    for i in range(3)
                    for j in range(3)
                )
                assert all(
                    value == 0
                    for index, value in enumerate(pair)
                    if index // 3 == 2 or index % 3 == 2
                )
                if all(pair[index] == 0 for index in (1, 2, 3, 5, 6, 7)):
                    assert column_rank([
                        tuple(F(1) if index == 0 else F(0) for index in range(9)),
                        tuple(F(1) if index == 4 else F(0) for index in range(9)),
                        pair,
                    ]) <= 2
        checked += 1
    assert channel_dimensions == {0, 1, 2}
    return checked, tuple(sorted(channel_dimensions))


Matrix = tuple[tuple[F, ...], ...]


def zero_matrix() -> Matrix:
    return tuple(tuple(F(0) for _ in range(3)) for _ in range(3))


def outer(left: tuple[F, ...], right: tuple[F, ...], scale: F = F(1)) -> Matrix:
    return tuple(tuple(scale * left[i] * right[j] for j in range(3)) for i in range(3))


def transpose(matrix: Matrix) -> Matrix:
    return tuple(tuple(matrix[j][i] for j in range(3)) for i in range(3))


def edge(edges: dict[tuple[int, int], Matrix], left: int, right: int) -> Matrix:
    if left < right:
        return edges.get((left, right), zero_matrix())
    return transpose(edges.get((right, left), zero_matrix()))


def put(edges: dict[tuple[int, int], Matrix], left: int, right: int, matrix: Matrix) -> None:
    edges[(left, right)] = matrix if left < right else transpose(matrix)


def kron(left: tuple[F, ...], right: tuple[F, ...]) -> tuple[F, ...]:
    return tuple(left[i] * right[j] for i in range(3) for j in range(3))


def add(left: tuple[F, ...], right: tuple[F, ...]) -> tuple[F, ...]:
    return tuple(a + b for a, b in zip(left, right, strict=True))


def matrix_column(matrix: Matrix, column: int) -> tuple[F, ...]:
    return tuple(matrix[row][column] for row in range(3))


def matchings(vertices: tuple[int, ...]) -> tuple[tuple[tuple[int, int], ...], ...]:
    if not vertices:
        return ((),)
    first = vertices[0]
    answer: list[tuple[tuple[int, int], ...]] = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        rest = vertices[1:index] + vertices[index + 1 :]
        for tail in matchings(rest):
            answer.append(((first, second),) + tail)
    return tuple(answer)


def matching_state(edges: dict[tuple[int, int], Matrix], vertices: tuple[int, ...]) -> dict[tuple[int, ...], F]:
    position = {vertex: index for index, vertex in enumerate(vertices)}
    state: dict[tuple[int, ...], F] = {}
    for matching in matchings(vertices):
        choices: list[list[tuple[int, int, F]]] = []
        for left, right in matching:
            matrix = edge(edges, left, right)
            entries = [
                (i, j, matrix[i][j])
                for i in range(3)
                for j in range(3)
                if matrix[i][j]
            ]
            if not entries:
                break
            choices.append(entries)
        else:
            for selected in product(*choices):
                word = [0 for _ in vertices]
                value = F(1)
                for (left, right), (i, j, coefficient) in zip(matching, selected, strict=True):
                    word[position[left]] = i
                    word[position[right]] = j
                    value *= coefficient
                key = tuple(word)
                state[key] = state.get(key, F(0)) + value
    return {word: value for word, value in state.items() if value}


def audit_mixed_only_control() -> dict[str, object]:
    a0, a1, q0, q1, u0, u1, u2, u3 = range(8)
    ports = (u0, u1, u2, u3)
    e = tuple(tuple(F(1) if i == j else F(0) for i in range(3)) for j in range(3))
    w0: Matrix = ((F(0), F(1), F(-1)), (F(1), F(0), F(0)), (F(-1), F(0), F(1)))
    w1: Matrix = ((F(1), F(1), F(-1)), (F(0), F(-1), F(2)), (F(-1), F(0), F(0)))
    edges: dict[tuple[int, int], Matrix] = {}
    xis = ((e[1], e[2]), (e[2], e[1]))
    for root, root_xis in ((a0, xis[0]), (a1, xis[1])):
        put(edges, root, q0, outer(root_xis[0], e[0]))
        put(edges, root, q1, outer(root_xis[1], e[0]))
    for port in ports:
        put(edges, a0, port, w0)
        put(edges, a1, port, w1)
    put(edges, u0, u1, outer(e[0], e[0]))
    put(edges, u2, u3, outer(e[0], e[0], F(1, 2)))

    xi0 = (e[1], e[2])
    xi1 = (e[2], e[1])
    q = add(kron(xi0[0], xi1[1]), kron(xi0[1], xi1[0]))
    nuisance: list[tuple[F, ...]] = []
    for s in range(2):
        for port in ports:
            for colour in range(3):
                nuisance.append(add(
                    kron(xi0[s], matrix_column(edge(edges, a1, port), colour)),
                    kron(matrix_column(edge(edges, a0, port), colour), xi1[s]),
                ))
    for left, right in combinations(ports, 2):
        for left_colour in range(3):
            for right_colour in range(3):
                nuisance.append(add(
                    kron(
                        matrix_column(edge(edges, a0, left), left_colour),
                        matrix_column(edge(edges, a1, right), right_colour),
                    ),
                    kron(
                        matrix_column(edge(edges, a0, right), right_colour),
                        matrix_column(edge(edges, a1, left), left_colour),
                    ),
                ))
    assert len(nuisance) == 78
    pure = [kron(e[colour], e[colour]) for colour in range(3)]
    assert q == add(pure[1], pure[2])
    p = sum(q)
    assert p == 2
    raw_rank = column_rank(nuisance)
    assert raw_rank == column_rank(nuisance + [q]) == 8
    assert tuple(column_rank(nuisance + [vector]) for vector in pure) == (9, 9, 9)

    full_state = matching_state(edges, tuple(range(8)))
    assert full_state == {
        (1, 1, 0, 0, 0, 0, 0, 0): F(1, 2),
        (2, 2, 0, 0, 0, 0, 0, 0): F(1, 2),
    }
    port_state = matching_state(edges, ports)
    assert port_state == {(0, 0, 0, 0): F(1, 2)}
    assert p * port_state[(0, 0, 0, 0)] == 1

    contracted: dict[tuple[int, ...], list[list[F]]] = {}
    for word, coefficient in full_state.items():
        port_word = word[4:]
        matrix = contracted.setdefault(port_word, [[F(0) for _ in range(3)] for _ in range(3)])
        matrix[word[0]][word[1]] += coefficient
    assert set(contracted) == {(0, 0, 0, 0)}
    expected_contracted = [
        [F(0), F(0), F(0)],
        [F(0), F(1, 2), F(0)],
        [F(0), F(0), F(1, 2)],
    ]
    assert contracted[(0, 0, 0, 0)] == expected_contracted
    assert rank(expected_contracted) == 2
    mixed_words = [word for word in product(range(3), repeat=4) if len(set(word)) > 1]
    assert len(mixed_words) == 78
    assert not any(word in contracted for word in mixed_words)

    pure_defect_ranks: list[int] = []
    for colour in range(3):
        word = (colour,) * 4
        matrix = [row[:] for row in contracted.get(word, [[F(0) for _ in range(3)] for _ in range(3)])]
        matrix[colour][colour] -= 1
        pure_defect_ranks.append(rank(matrix))
    assert tuple(pure_defect_ranks) == (3, 1, 1)

    # Every non-Q complement contains an isolated residual, so rho_Q=0.
    assert all(edge(edges, q0, vertex) == zero_matrix() for vertex in (q1, *ports))
    assert all(edge(edges, q1, vertex) == zero_matrix() for vertex in ports)
    return {
        "raw_ranks": (raw_rank, column_rank(nuisance + [q])),
        "pure_augmentation_ranks": tuple(column_rank(nuisance + [vector]) for vector in pure),
        "full_support": len(full_state),
        "port_support": len(port_state),
        "mixed_port_words_zero": len(mixed_words),
        "q_contracted_pure_port_rank": 2,
        "pure_defect_ranks": tuple(pure_defect_ranks),
        "pH_kernel_value": p * port_state[(0, 0, 0, 0)],
    }


def main() -> None:
    shore_charts, channel_dimensions = audit_two_shore_support()
    control = audit_mixed_only_control()
    print("GLS37 independent no-import audit: PASS")
    print("  exact shore charts:", shore_charts)
    print("  channel dimensions:", channel_dimensions)
    print("  two-shore rank-three full-swallow fibre: excluded by support rank 2 < 3")
    print("  independently reconstructed mixed-only control:", control)


if __name__ == "__main__":
    main()
