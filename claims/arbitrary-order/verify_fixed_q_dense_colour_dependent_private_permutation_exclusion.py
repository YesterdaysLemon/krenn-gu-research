"""Primary exact replay for the GLD23 private-permutation exclusion.

The dense-cell normalization leaves the dead-colour private permutation equal
to the identity and two ordered active permutations in S4.  This verifier
constructs the complete affine coefficient system directly from all 945
perfect matchings of the ten-vertex graph.  It reduces the 576 permutation
pairs to simultaneous-conjugacy/active-swap orbits and produces an exact
characteristic-zero contradiction certificate for every orbit.
"""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import permutations, product


ROOTS = tuple(range(4))
Q0, Q1 = 4, 5
PORTS = tuple(range(6, 10))
VERTICES = ROOTS + (Q0, Q1) + PORTS
COLOURS = tuple(range(3))
DEAD = 2
PERMS = tuple(permutations(ROOTS))

P0_BASE = 0
P1_BASE = 12
W_BASE = 24
ALPHA_BASE = 78
NVARIABLES = 81

EDGES = tuple((left, right) for left in ROOTS for right in ROOTS if left < right)
EDGE_INDEX = {edge: index for index, edge in enumerate(EDGES)}


def p_index(which: int, root: int, colour: int) -> int:
    return (P0_BASE if which == 0 else P1_BASE) + 3 * root + colour


def w_index(left: int, right: int, lc: int, rc: int) -> int:
    if left > right:
        left, right, lc, rc = right, left, rc, lc
    return W_BASE + 9 * EDGE_INDEX[(left, right)] + 3 * lc + rc


def add(row: dict[int, int], index: int, value: int) -> None:
    if not value:
        return
    updated = row.get(index, 0) + value
    if updated:
        row[index] = updated
    else:
        row.pop(index, None)


@lru_cache(maxsize=None)
def perfect_matchings(
    vertices: tuple[int, ...],
) -> tuple[tuple[tuple[int, int], ...], ...]:
    if not vertices:
        return ((),)
    first = vertices[0]
    output: list[tuple[tuple[int, int], ...]] = []
    for index in range(1, len(vertices)):
        second = vertices[index]
        remainder = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(remainder):
            output.append(((first, second),) + tail)
    return tuple(output)


MATCHINGS = perfect_matchings(VERTICES)
assert len(MATCHINGS) == 945


EquationKey = tuple[tuple[int, ...], tuple[int, ...]]
Equation = tuple[EquationKey, dict[int, int], int]


def direct_system(
    first_perm: tuple[int, ...], second_perm: tuple[int, ...]
) -> list[Equation]:
    """Build all nontrivial equations by an actual perfect-matching sum."""

    colour_perms = (first_perm, second_perm, ROOTS)
    x = (1, 1, 0)
    y = (1, -1, 0)
    output: list[Equation] = []

    for port_word in product(COLOURS, repeat=4):
        equations: dict[tuple[int, ...], list[object]] = {}

        def equation(root_word: tuple[int, ...]) -> list[object]:
            return equations.setdefault(root_word, [{}, 0])

        for matching in MATCHINGS:
            fixed_root_colours: dict[int, int] = {}
            variable: tuple[object, ...] | None = None
            scalar = 1
            valid = True

            for raw_left, raw_right in matching:
                left, right = sorted((raw_left, raw_right))
                if left in PORTS:
                    valid = False
                    break
                if left in ROOTS and right in ROOTS:
                    if variable is not None:
                        valid = False
                        break
                    variable = ("w", left, right)
                elif left in ROOTS and right in (Q0, Q1):
                    if variable is not None:
                        valid = False
                        break
                    variable = ("p", right - Q0, left)
                elif left in ROOTS and right in PORTS:
                    port = right - PORTS[0]
                    colour = port_word[port]
                    if left != colour_perms[colour][port]:
                        valid = False
                        break
                    fixed_root_colours[left] = colour
                elif left == Q0 and right == Q1:
                    pass
                elif left in (Q0, Q1) and right in PORTS:
                    port = right - PORTS[0]
                    shore = x if left == Q0 else y
                    scalar *= shore[port_word[port]]
                    if not scalar:
                        valid = False
                        break
                else:
                    valid = False
                    break

            if not valid:
                continue
            free_roots = tuple(root for root in ROOTS if root not in fixed_root_colours)
            if variable is None:
                if free_roots:
                    continue
                root_word = tuple(fixed_root_colours[root] for root in ROOTS)
                equation(root_word)[1] -= scalar
            elif variable[0] == "p":
                _, which, root = variable
                if free_roots != (root,):
                    continue
                for colour in COLOURS:
                    values = dict(fixed_root_colours)
                    values[root] = colour
                    root_word = tuple(values[item] for item in ROOTS)
                    row = equation(root_word)[0]
                    assert isinstance(row, dict)
                    add(row, p_index(which, root, colour), scalar)
            else:
                _, left, right = variable
                if free_roots != (left, right):
                    continue
                for left_colour in COLOURS:
                    for right_colour in COLOURS:
                        values = dict(fixed_root_colours)
                        values[left] = left_colour
                        values[right] = right_colour
                        root_word = tuple(values[item] for item in ROOTS)
                        row = equation(root_word)[0]
                        assert isinstance(row, dict)
                        add(
                            row,
                            w_index(
                                left,
                                right,
                                left_colour,
                                right_colour,
                            ),
                            scalar,
                        )

        if len(set(port_word)) == 1:
            colour = port_word[0]
            row = equation(port_word)[0]
            assert isinstance(row, dict)
            add(row, ALPHA_BASE + colour, -1)

        for root_word, raw_equation in equations.items():
            row, rhs = raw_equation
            assert isinstance(row, dict)
            assert isinstance(rhs, int)
            if row or rhs:
                output.append(((port_word, root_word), row, rhs))

    return output


def inverse(perm: tuple[int, ...]) -> tuple[int, ...]:
    answer = [0] * 4
    for source, target in enumerate(perm):
        answer[target] = source
    return tuple(answer)


def compose(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(left[right[item]] for item in ROOTS)


def conjugate(perm: tuple[int, ...], relabel: tuple[int, ...]) -> tuple[int, ...]:
    return compose(compose(relabel, perm), inverse(relabel))


def canonical_pair(
    first: tuple[int, ...], second: tuple[int, ...]
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    images = []
    for relabel in PERMS:
        left = conjugate(first, relabel)
        right = conjugate(second, relabel)
        images.extend(((left, right), (right, left)))
    return min(images)


def contradiction_certificate(
    equations: list[Equation],
) -> dict[int, Fraction]:
    """Return lambda with lambda*A=0 and lambda*b=1."""

    pivots: dict[int, tuple[dict[int, Fraction], Fraction, dict[int, Fraction]]] = {}
    for equation_index, (_, integer_row, integer_rhs) in enumerate(equations):
        row = {key: Fraction(value) for key, value in integer_row.items()}
        rhs = Fraction(integer_rhs)
        combination = {equation_index: Fraction(1)}
        while row:
            pivot = min(row)
            if pivot not in pivots:
                inverse_pivot = 1 / row[pivot]
                row = {key: value * inverse_pivot for key, value in row.items()}
                rhs *= inverse_pivot
                combination = {
                    key: value * inverse_pivot for key, value in combination.items()
                }
                pivots[pivot] = (row, rhs, combination)
                break
            basis, basis_rhs, basis_combination = pivots[pivot]
            factor = row[pivot]
            for key, value in basis.items():
                updated = row.get(key, Fraction(0)) - factor * value
                if updated:
                    row[key] = updated
                else:
                    row.pop(key, None)
            rhs -= factor * basis_rhs
            for key, value in basis_combination.items():
                updated = combination.get(key, Fraction(0)) - factor * value
                if updated:
                    combination[key] = updated
                else:
                    combination.pop(key, None)
        else:
            if rhs:
                return {key: value / rhs for key, value in combination.items()}
    raise AssertionError("unexpected consistent private-permutation system")


def verify_certificate(
    equations: list[Equation], certificate: dict[int, Fraction]
) -> None:
    combined_row: dict[int, Fraction] = {}
    combined_rhs = Fraction(0)
    for equation_index, multiplier in certificate.items():
        _, row, rhs = equations[equation_index]
        for variable, coefficient in row.items():
            updated = combined_row.get(variable, Fraction(0)) + (
                multiplier * coefficient
            )
            if updated:
                combined_row[variable] = updated
            else:
                combined_row.pop(variable, None)
        combined_rhs += multiplier * rhs
    assert not combined_row
    assert combined_rhs == 1


def certificate_digest(
    representative: tuple[tuple[int, ...], tuple[int, ...]],
    equations: list[Equation],
    certificate: dict[int, Fraction],
) -> str:
    pieces = [repr(representative)]
    for equation_index, multiplier in sorted(certificate.items()):
        key = equations[equation_index][0]
        pieces.append(f"{key}:{multiplier.numerator}/{multiplier.denominator}")
    return "\n".join(pieces)


EXPECTED_ORBIT_SIZES = (
    1,
    12,
    16,
    6,
    12,
    6,
    24,
    48,
    6,
    12,
    48,
    48,
    24,
    24,
    8,
    8,
    48,
    24,
    48,
    48,
    24,
    3,
    24,
    6,
    12,
    6,
    24,
    6,
)
EXPECTED_CERTIFICATE_SIZES = (
    20,
    11,
    5,
    9,
    8,
    20,
    6,
    10,
    9,
    10,
    9,
    7,
    8,
    5,
    16,
    5,
    7,
    7,
    11,
    10,
    12,
    20,
    9,
    5,
    8,
    9,
    9,
    11,
)
EXPECTED_CERTIFICATE_DIGEST = (
    "8f3fe93c3b04efb8cd9cb9b13dde681bcd2b0d3ba738162453070497302f6dce"
)


def main() -> None:
    orbit_sizes: dict[tuple[tuple[int, ...], tuple[int, ...]], int] = {}
    for first_perm, second_perm in product(PERMS, repeat=2):
        representative = canonical_pair(first_perm, second_perm)
        orbit_sizes[representative] = orbit_sizes.get(representative, 0) + 1

    representatives = tuple(sorted(orbit_sizes))
    assert len(representatives) == 28
    assert tuple(orbit_sizes[rep] for rep in representatives) == EXPECTED_ORBIT_SIZES
    assert sum(orbit_sizes.values()) == 24**2 == 576

    certificate_sizes = []
    digest_pieces = []
    equation_counts = []
    for representative in representatives:
        equations = direct_system(*representative)
        assert all(
            0 <= variable < NVARIABLES for _, row, _ in equations for variable in row
        )
        certificate = contradiction_certificate(equations)
        verify_certificate(equations, certificate)
        equation_counts.append(len(equations))
        certificate_sizes.append(len(certificate))
        digest_pieces.append(certificate_digest(representative, equations, certificate))

    digest = sha256("\n---\n".join(digest_pieces).encode()).hexdigest()
    assert digest == EXPECTED_CERTIFICATE_DIGEST
    assert tuple(certificate_sizes) == EXPECTED_CERTIFICATE_SIZES
    assert min(equation_counts) == 757
    assert max(equation_counts) == 945
    print(
        "PASS: 945-match expansion gives exact contradictions for all "
        "28 symmetry orbits covering 576 active private-permutation pairs"
    )


if __name__ == "__main__":
    main()
