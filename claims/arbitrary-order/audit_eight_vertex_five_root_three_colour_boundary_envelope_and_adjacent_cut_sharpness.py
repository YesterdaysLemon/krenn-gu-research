"""Independent no-import audit of the five-root boundary-envelope package."""

from __future__ import annotations

from fractions import Fraction
from functools import cache
from itertools import combinations, permutations, product

Matrix = tuple[tuple[Fraction, ...], ...]
Vertices = tuple[int, ...]
Matching = tuple[tuple[int, int], ...]


@cache
def matchings(vertices: Vertices) -> tuple[Matching, ...]:
    """Generate labelled perfect matchings by an independent recursion."""
    if not vertices:
        return ((),)
    pivot = vertices[-1]
    result: list[Matching] = []
    for index, partner in enumerate(vertices[:-1]):
        remainder = vertices[:index] + vertices[index + 1 : -1]
        for tail in matchings(remainder):
            edge = (partner, pivot) if partner < pivot else (pivot, partner)
            result.append(tail + (edge,))
    return tuple(result)


def audit_majority_and_degree() -> dict[str, object]:
    """Audit the matching inequality and the degree-24 five-root intersection."""
    roots = set(range(5))
    sectors: dict[tuple[int, int], int] = {}
    for matching in matchings(tuple(range(8))):
        inside = sum(left in roots and right in roots for left, right in matching)
        outside = sum(left not in roots and right not in roots for left, right in matching)
        assert inside - outside == 1
        sectors[(inside, outside)] = sectors.get((inside, outside), 0) + 1
    assert sectors == {(1, 0): 60, (2, 1): 45}

    edges = tuple(combinations(range(5), 2))

    @cache
    def endpoint_count(index: int, remaining: tuple[int, ...]) -> int:
        if index == len(edges):
            return int(not any(remaining))
        total = 0
        for endpoint in edges[index]:
            if remaining[endpoint] == 0:
                continue
            updated = list(remaining)
            updated[endpoint] -= 1
            total += endpoint_count(index + 1, tuple(updated))
        return total

    degree = endpoint_count(0, (2, 2, 2, 2, 2))
    assert degree == 24
    return {"matching_sectors": sectors, "five_root_degree": degree}


def audit_cover_and_dimensions() -> dict[str, object]:
    """Audit the coordinate cover by direct per-factor dimension arithmetic."""
    profile: dict[tuple[int, ...], int] = {}
    empty = 0
    for selector in product(range(5), repeat=3):
        loads = [0] * 5
        for vertex in selector:
            loads[vertex] += 1
        if 3 in loads:
            empty += 1
            continue
        dimension = sum(2 - load for load in loads)
        assert dimension == 7
        key = tuple(sorted((load for load in loads if load), reverse=True))
        profile[key] = profile.get(key, 0) + 1
    assert empty == 5
    assert profile == {(2, 1): 60, (1, 1, 1): 60}

    projective_ambient = 10 * 8
    incidence = 7 + 10 * 7
    affine_ambient = 10 * 9
    affine_projective_lift = incidence + 10
    zero_block = affine_ambient - 9
    assert projective_ambient - incidence == 3
    assert affine_ambient - max(affine_projective_lift, zero_block) == 3
    return {
        "nonempty_selectors": sum(profile.values()),
        "empty_selectors": empty,
        "profiles": profile,
        "projective_dimensions": (projective_ambient, incidence),
        "affine_dimensions": (affine_ambient, affine_projective_lift, zero_block),
        "codimension_at_least": 3,
    }


def parity_signature(labels: tuple[int, ...]) -> tuple[int, int, int]:
    """Return the parity of three latent-label multiplicities."""
    return tuple(sum(label == colour for label in labels) % 2 for colour in range(3))


def audit_monomial_shell_cases() -> dict[str, int]:
    """Audit all local permutation cases without enumerating global tables."""
    tables = tuple(permutations(range(3)))
    h1 = 0
    h2 = 0
    h2_good = {1: 0, 2: 0}
    for left in tables:
        for colour in range(3):
            for replacement in range(3):
                if replacement == colour:
                    continue
                old = (left[colour],)
                new = (left[replacement],)
                assert parity_signature(old + new) != (0, 0, 0)
                h1 += 1
        for right in tables:
            for colour in range(3):
                alternatives = tuple(value for value in range(3) if value != colour)
                old = (left[colour], right[colour])
                count = 0
                for left_new, right_new in product(alternatives, repeat=2):
                    new = (left[left_new], right[right_new])
                    count += parity_signature(old + new) == (0, 0, 0)
                expected = 2 if old[0] == old[1] else 1
                assert count == expected
                h2_good[count] += 1
                h2 += 1
    assert (h1, h2, h2_good) == (36, 108, {1: 72, 2: 36})
    return {"hamming_one_cases": h1, "hamming_two_cases": h2, **h2_good}


def matrix(rows: list[list[int | Fraction]]) -> Matrix:
    """Convert a list of rows to an exact immutable matrix."""
    return tuple(tuple(Fraction(entry) for entry in row) for row in rows)


def transpose(value: Matrix) -> Matrix:
    return tuple(tuple(row) for row in zip(*value, strict=True))


def multiply(left: Matrix, right: Matrix) -> Matrix:
    return tuple(
        tuple(
            sum(
                (left[row][middle] * right[middle][column] for middle in range(3)),
                Fraction(0),
            )
            for column in range(3)
        )
        for row in range(3)
    )


def determinant(value: Matrix) -> Fraction:
    size = len(value)
    if size == 1:
        return value[0][0]
    total = Fraction(0)
    for column in range(size):
        minor = tuple(
            tuple(value[row][other] for other in range(size) if other != column)
            for row in range(1, size)
        )
        total += (-1) ** column * value[0][column] * determinant(minor)
    return total


IDENTITY = matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])


def gauges() -> tuple[Matrix, ...]:
    third = Fraction(1, 3)
    return (
        IDENTITY,
        matrix([[-1, 0, 0], [0, 0, -1], [0, -1, 0]]),
        matrix([[-1, 0, 0], [0, -1, 0], [0, 0, 1]]),
        matrix([[0, 1, 0], [0, 0, -1], [1, 0, 0]]),
        matrix([[0, -1, 0], [-1, 0, 0], [0, 0, -1]]),
        matrix([[-1, 0, 0], [0, -1, 0], [0, 0, -1]]),
        matrix([[0, 0, -1], [-1, 0, 0], [0, -1, 0]]),
        matrix([[0, 0, -third], [0, -third, 0], [-third, 0, 0]]),
    )


def coefficient(word: tuple[int, ...], blocks: dict[tuple[int, int], Matrix]) -> Fraction:
    total = Fraction(0)
    for matching in matchings(tuple(range(len(word)))):
        term = Fraction(1)
        for left, right in matching:
            term *= blocks[(left, right)][word[left]][word[right]]
        total += term
    return total


def quadratic_column(block: Matrix) -> tuple[Fraction, ...]:
    return (
        block[0][0],
        block[1][1],
        block[2][2],
        block[0][1] + block[1][0],
        block[0][2] + block[2][0],
        block[1][2] + block[2][1],
    )


def quadric_matrix(
    roots: tuple[int, ...], blocks: dict[tuple[int, int], Matrix]
) -> Matrix:
    columns = [quadratic_column(blocks[edge]) for edge in combinations(roots, 2)]
    return tuple(tuple(columns[column][row] for column in range(6)) for row in range(6))


def audit_fixture() -> dict[str, object]:
    local_gauges = gauges()
    blocks = {
        (left, right): multiply(transpose(local_gauges[left]), local_gauges[right])
        for left in range(8)
        for right in range(left + 1, 8)
    }
    assert all(determinant(value) for value in local_gauges)
    assert all(determinant(value) for value in blocks.values())

    pure = tuple(coefficient((colour,) * 8, blocks) for colour in range(3))
    assert pure == (1, 1, 1)
    h1 = []
    for colour in range(3):
        for vertex in range(8):
            for replacement in range(3):
                if replacement == colour:
                    continue
                word = [colour] * 8
                word[vertex] = replacement
                h1.append(coefficient(tuple(word), blocks))
    assert len(h1) == 48 and not any(h1)
    h2 = coefficient((0, 0, 0, 2, 2, 0, 0, 0), blocks)
    assert h2 == -1

    first = quadric_matrix((0, 1, 2, 3), blocks)
    second = quadric_matrix((0, 1, 2, 4), blocks)
    assert (determinant(first), determinant(second)) == (4, -8)
    return {
        "pure_coefficients": pure,
        "hamming_one_zeros": len(h1),
        "mixed_00022000": h2,
        "adjacent_root_quadric_determinants": (determinant(first), determinant(second)),
        "invertible_blocks": len(blocks),
    }


def main() -> None:
    majority = audit_majority_and_degree()
    cover = audit_cover_and_dimensions()
    shells = audit_monomial_shell_cases()
    fixture = audit_fixture()
    print("eight-vertex five-root boundary envelope independent audit: PASS")
    print(f"  majority and intersection: {majority}")
    print(f"  coordinate cover and dimensions: {cover}")
    print(f"  independent monomial shell cases: {shells}")
    print(f"  exact adjacent-cut fixture: {fixture}")


if __name__ == "__main__":
    main()
