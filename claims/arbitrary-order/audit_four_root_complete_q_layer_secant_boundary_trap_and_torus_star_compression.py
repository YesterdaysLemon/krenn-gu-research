"""Independent no-import audit of the GLD70 complete-Q-layer reduction."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations, permutations, product

Q = Fraction
MODES = (0, 1, 2, 3)
WORDS = tuple(product(range(3), repeat=4))
WORD_OFFSET = {word: offset for offset, word in enumerate(WORDS)}


def vec(*entries: int) -> tuple[Q, ...]:
    return tuple(Q(entry) for entry in entries)


def permanent_dp(columns: tuple[tuple[Q, ...], ...]) -> Q:
    """Permanent by a subset dynamic program, not permutation expansion."""

    states = {0: Q(1)}
    for column in columns:
        following: dict[int, Q] = {}
        for mask, value in states.items():
            for row, entry in enumerate(column):
                if mask & (1 << row):
                    continue
                next_mask = mask | (1 << row)
                following[next_mask] = following.get(next_mask, Q(0)) + value * entry
        states = following
    return states[(1 << len(columns)) - 1]


def rank(rows: list[list[Q]]) -> int:
    matrix = [row[:] for row in rows]
    pivot_row = 0
    for column in range(len(matrix[0]) if matrix else 0):
        pivot = next(
            (row for row in range(pivot_row, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        for row in range(pivot_row + 1, len(matrix)):
            if not matrix[row][column]:
                continue
            left = matrix[pivot_row][column]
            right = matrix[row][column]
            matrix[row] = [
                left * entry - right * pivot_entry
                for entry, pivot_entry in zip(
                    matrix[row], matrix[pivot_row], strict=True
                )
            ]
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return pivot_row


def span_rank(columns: list[list[Q]]) -> int:
    return rank([[column[row] for column in columns] for row in range(81)])


def flatten_layers(
    layers: tuple[list[list[Q]], list[list[Q]], list[list[Q]]],
) -> list[list[Q]]:
    return [column for layer in layers for column in layer]


def sign(sigma: tuple[int, ...]) -> int:
    return (-1) ** sum(
        sigma[left] > sigma[right]
        for left in range(len(sigma))
        for right in range(left + 1, len(sigma))
    )


def epsilon_full(tensor: list[Q]) -> Q:
    total = Q(0)
    permutations_3 = tuple(permutations(range(3)))
    for sigmas in product(permutations_3, repeat=4):
        term = Q(sign(sigmas[0]) * sign(sigmas[1]) * sign(sigmas[2]) * sign(sigmas[3]))
        for copy in range(3):
            word = tuple(sigmas[mode][copy] for mode in MODES)
            term *= tensor[WORD_OFFSET[word]]
        total += term
    return total


def build_layers(
    xi: tuple[Q, ...],
    eta: tuple[Q, ...],
    ports: tuple[tuple[tuple[Q, ...], ...], ...],
) -> tuple[list[list[Q]], list[list[Q]], list[list[Q]]]:
    """Rebuild raw columns by scanning tensor words in reverse label order."""

    q = [
        [
            permanent_dp(tuple(ports[mode][word[mode]] for mode in MODES))
            for word in WORDS
        ]
    ]

    residual: list[list[Q]] = []
    for residual_vector in (eta, xi):
        for labelled_mode in reversed(MODES):
            others = tuple(mode for mode in MODES if mode != labelled_mode)
            for labelled_index in reversed(range(3)):
                column = []
                for word in WORDS:
                    if word[labelled_mode] != labelled_index:
                        column.append(Q(0))
                        continue
                    column.append(
                        permanent_dp(
                            (residual_vector,)
                            + tuple(ports[mode][word[mode]] for mode in others)
                        )
                    )
                residual.append(column)

    pair: list[list[Q]] = []
    for labelled_modes in reversed(tuple(combinations(MODES, 2))):
        others = tuple(mode for mode in MODES if mode not in labelled_modes)
        for labelled_indices in reversed(tuple(product(range(3), repeat=2))):
            column = []
            for word in WORDS:
                if any(
                    word[mode] != index
                    for mode, index in zip(
                        labelled_modes, labelled_indices, strict=True
                    )
                ):
                    column.append(Q(0))
                    continue
                column.append(
                    permanent_dp(
                        (
                            xi,
                            eta,
                            ports[others[0]][word[others[0]]],
                            ports[others[1]][word[others[1]]],
                        )
                    )
                )
            pair.append(column)
    assert (len(q), len(residual), len(pair)) == (1, 24, 54)
    return q, residual, pair


def torus_star(
    slope: int,
) -> tuple[tuple[Q, ...], tuple[Q, ...], tuple[tuple[tuple[Q, ...], ...], ...]]:
    radical = (vec(1, -1, 0, 0), vec(1, 0, -1, 0))
    centre = radical + (vec(1, 0, 0, slope),)
    leaf = radical + (vec(1, 0, 0, -slope),)
    return vec(1, 1, 1, -1), vec(1, 1, 1, 1), (centre, leaf, leaf, leaf)


def scalar_zero_star() -> tuple[
    tuple[Q, ...], tuple[Q, ...], tuple[tuple[tuple[Q, ...], ...], ...]
]:
    r0 = vec(0, 0, 1, 0)
    r1 = vec(0, 0, 0, 1)
    centre = vec(1, 1, 0, 0)
    leaf = vec(1, -1, 0, 0)
    ports = (
        (r0, r1, centre),
        (r0, r1, leaf),
        (leaf, r0, r1),
        (r0, leaf, r1),
    )
    return vec(0, 0, 0, 1), vec(0, 0, 1, 0), ports


def triangle() -> tuple[
    tuple[Q, ...], tuple[Q, ...], tuple[tuple[tuple[Q, ...], ...], ...]
]:
    sibling = (vec(1, -1, 0, 0), vec(0, 0, 1, 0), vec(0, 0, 0, 1))
    centre = (vec(1, 0, 1, 0), vec(0, 1, 0, 0), vec(0, 0, 0, 1))
    return (
        vec(0, 0, 1, 1),
        vec(1, 1, 0, 0),
        (
            centre,
            sibling,
            sibling,
            sibling,
        ),
    )


def diagonal() -> list[list[Q]]:
    return [
        [Q(all(entry == colour for entry in word)) for word in WORDS]
        for colour in range(3)
    ]


def audit_layer_ranks() -> dict[str, tuple[int, ...]]:
    expected = {
        "scalar": (16, 21, 21, 24),
        "torus": (24, 21, 44, 46),
        "triangle": (22, 19, 35, 38),
    }
    answer = {}
    target_space = diagonal()
    for name, data in (
        ("scalar", scalar_zero_star()),
        ("torus", torus_star(1)),
        ("triangle", triangle()),
    ):
        q, residual, pair = build_layers(*data)
        nuisance = q + residual + pair
        ranks = (
            span_rank(q + residual),
            span_rank(pair),
            span_rank(nuisance),
            span_rank(nuisance + target_space),
        )
        assert ranks == expected[name]
        answer[name] = ranks
    return answer


def audit_epsilon() -> tuple[Q, Q, tuple[Q, Q, Q]]:
    target_space = diagonal()
    delta = [sum(column[row] for column in target_space) for row in range(81)]
    sigma_2 = [target_space[0][row] + target_space[1][row] for row in range(81)]
    assert epsilon_full(delta) == 6
    assert epsilon_full(sigma_2) == 0

    q, _residual, _pair = build_layers(*torus_star(1))
    q_value = epsilon_full(q[0])
    assert q_value == -288

    basis = (vec(1, 0, 0), vec(0, 1, 0), vec(0, 0, 1))

    def tensor(terms: list[tuple[tuple[Q, ...], ...]]) -> list[Q]:
        return [
            sum(
                factors[0][word[0]]
                * factors[1][word[1]]
                * factors[2][word[2]]
                * factors[3][word[3]]
                for factors in terms
            )
            for word in WORDS
        ]

    type_ii = []
    for mode in MODES:
        factors = [basis[0]] * 4
        factors[mode] = basis[1]
        type_ii.append(tuple(factors))
    type_ii.append((basis[2],) * 4)

    type_iii = []
    for left, right in combinations(MODES, 2):
        factors = [basis[0]] * 4
        factors[left] = factors[right] = basis[1]
        type_iii.append(tuple(factors))
    for mode in MODES:
        factors = [basis[0]] * 4
        factors[mode] = basis[2]
        type_iii.append(tuple(factors))

    type_iv = []
    for mode in (1, 2, 3):
        factors = [basis[0]] * 4
        factors[0] = factors[mode] = basis[1]
        type_iv.append(tuple(factors))
    for mode in MODES:
        factors = [basis[0]] * 4
        factors[mode] = basis[2]
        type_iv.append(tuple(factors))

    boundary = tuple(
        epsilon_full(tensor(terms)) for terms in (type_ii, type_iii, type_iv)
    )
    assert boundary == (Q(0), Q(0), Q(0))
    return epsilon_full(delta), q_value, boundary


def audit_star_family() -> tuple[int, int, int, int]:
    reference = flatten_layers(build_layers(*torus_star(1)))
    ranks = []
    for slope in (-3, -2, -1, 1, 2, 3):
        columns = flatten_layers(build_layers(*torus_star(slope)))
        assert span_rank(columns) == 44
        assert span_rank(reference + columns) == 44
        ranks.append(span_rank(columns))
    return min(ranks), max(ranks), len(ranks), span_rank(reference)


def rank_mod_prime(matrix: list[list[int]], prime: int) -> int:
    rows = [[entry % prime for entry in row] for row in matrix]
    pivot_row = 0
    for column in range(len(rows[0])):
        pivot = next(
            (row for row in range(pivot_row, len(rows)) if rows[row][column]),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        inverse = pow(rows[pivot_row][column], -1, prime)
        rows[pivot_row] = [(entry * inverse) % prime for entry in rows[pivot_row]]
        for row in range(len(rows)):
            if row == pivot_row or not rows[row][column]:
                continue
            scale = rows[row][column]
            rows[row] = [
                (entry - scale * pivot_entry) % prime
                for entry, pivot_entry in zip(rows[row], rows[pivot_row], strict=True)
            ]
        pivot_row += 1
    return pivot_row


def audit_torus_ratio_classification() -> tuple[int, int]:
    prime = 7
    rank_two = 0
    canonical = 0
    for ratios in product(range(1, prime), repeat=4):
        form = [[0] * 4 for _ in range(4)]
        for left, right in combinations(MODES, 2):
            other = [mode for mode in MODES if mode not in (left, right)]
            form[left][right] = form[right][left] = (
                ratios[other[0]] + ratios[other[1]]
            ) % prime
        if rank_mod_prime(form, prime) != 2:
            continue
        rank_two += 1
        is_canonical = any(
            all(
                ratios[mode] == (-ratios[singleton]) % prime
                for mode in MODES
                if mode != singleton
            )
            for singleton in MODES
        )
        assert is_canonical
        canonical += 1
    assert rank_two == canonical == 24
    return rank_two, canonical


def main() -> None:
    ranks = audit_layer_ranks()
    epsilon_values = audit_epsilon()
    family = audit_star_family()
    ratio_census = audit_torus_ratio_classification()
    print("independent GLD70 complete-Q-layer audit: PASS")
    print("  layer ranks:", ranks)
    print("  epsilon target / Q / boundary:", epsilon_values)
    print("  torus-star sampled fixed-space ranks:", family)
    print("  F7 rank-two / canonical ratio patterns:", ratio_census)


if __name__ == "__main__":
    main()
