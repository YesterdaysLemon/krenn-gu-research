"""Independent no-import audit of the m=3 common-shore interface.

This script uses only the Python standard library.  It reconstructs the
matching formulas with exact Fractions and checks the Latin-plane separator
with an independent sparse-polynomial determinant implementation.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import permutations, product

DIM = 3
WORDS = tuple(product(range(DIM), repeat=DIM))
ZERO_EXPONENT = (0,) * 9


def deterministic_blocks():
    """Return exact generic-looking root and cross blocks."""
    root_blocks = {
        (0, 1): tuple(
            tuple(Fraction(2 + 3 * a + 5 * b) for b in range(DIM))
            for a in range(DIM)
        ),
        (0, 2): tuple(
            tuple(Fraction(7 + 2 * a - 3 * c) for c in range(DIM))
            for a in range(DIM)
        ),
        (1, 2): tuple(
            tuple(Fraction(11 - 4 * b + 6 * c) for c in range(DIM))
            for b in range(DIM)
        ),
    }
    cross = {
        (root, nonroot, colour, coordinate): Fraction(
            1
            + 17 * root
            + 11 * nonroot
            + 7 * colour
            + 3 * coordinate
        )
        for root in range(DIM)
        for nonroot in range(DIM)
        for colour in range(DIM)
        for coordinate in range(DIM)
    }
    return root_blocks, cross


def singleton_direct(root_blocks, cross, nonroot, colour):
    """Enumerate the chosen cross root and the remaining internal edge."""
    answer = {}
    for word in WORDS:
        total = Fraction(0)
        for cross_root in range(DIM):
            remaining = tuple(root for root in range(DIM) if root != cross_root)
            left, right = remaining
            pair = (left, right)
            total += (
                cross[(cross_root, nonroot, colour, word[cross_root])]
                * root_blocks[pair][word[left]][word[right]]
            )
        answer[word] = total
    return answer


def singleton_shared_factor(root_blocks, cross, nonroot, colour):
    """Assemble the three ordered tensor-cylinder summands."""
    answer = {}
    for a, b, c in WORDS:
        answer[(a, b, c)] = (
            cross[(0, nonroot, colour, a)] * root_blocks[(1, 2)][b][c]
            + root_blocks[(0, 2)][a][c]
            * cross[(1, nonroot, colour, b)]
            + root_blocks[(0, 1)][a][b]
            * cross[(2, nonroot, colour, c)]
        )
    return answer


def permanent3(matrix):
    """Compute an exact sign-free 3 by 3 permanent."""
    return sum(
        (
            matrix[0][sigma[0]]
            * matrix[1][sigma[1]]
            * matrix[2][sigma[2]]
        )
        for sigma in permutations(range(DIM))
    )


def empty_direct(cross, nonroot_colours):
    """Enumerate the six cross perfect matchings."""
    answer = {}
    for word in WORDS:
        answer[word] = sum(
            product_value(
                cross[
                    (
                        root,
                        sigma[root],
                        nonroot_colours[sigma[root]],
                        word[root],
                    )
                ]
                for root in range(DIM)
            )
            for sigma in permutations(range(DIM))
        )
    return answer


def product_value(values):
    """Multiply an iterator of exact scalars."""
    answer = Fraction(1)
    for value in values:
        answer *= value
    return answer


def empty_by_permanent(cross, nonroot_colours):
    """Compute the same coefficient as a 3 by 3 permanent."""
    answer = {}
    for word in WORDS:
        matrix = tuple(
            tuple(
                cross[
                    (
                        root,
                        nonroot,
                        nonroot_colours[nonroot],
                        word[root],
                    )
                ]
                for nonroot in range(DIM)
            )
            for root in range(DIM)
        )
        answer[word] = permanent3(matrix)
    return answer


def polynomial_constant(value):
    """Return one sparse polynomial constant."""
    value = Fraction(value)
    return {} if not value else {ZERO_EXPONENT: value}


def polynomial_variable(index):
    """Return one of the nine coordinate variables."""
    exponent = [0] * 9
    exponent[index] = 1
    return {tuple(exponent): Fraction(1)}


def polynomial_add(left, right, scale=Fraction(1)):
    """Return left plus scale times right."""
    answer = dict(left)
    for exponent, coefficient in right.items():
        answer[exponent] = answer.get(exponent, Fraction(0)) + scale * coefficient
        if not answer[exponent]:
            del answer[exponent]
    return answer


def polynomial_multiply(left, right):
    """Multiply two sparse polynomials."""
    answer = {}
    for left_exp, left_coefficient in left.items():
        for right_exp, right_coefficient in right.items():
            exponent = tuple(
                a + b for a, b in zip(left_exp, right_exp, strict=True)
            )
            answer[exponent] = answer.get(exponent, Fraction(0)) + (
                left_coefficient * right_coefficient
            )
    return {exponent: coefficient for exponent, coefficient in answer.items() if coefficient}


def polynomial_determinant(matrix):
    """Compute a determinant by the Leibniz formula."""
    size = len(matrix)
    answer = {}
    for sigma in permutations(range(size)):
        inversions = sum(
            sigma[i] > sigma[j]
            for i in range(size)
            for j in range(i + 1, size)
        )
        term = polynomial_constant(-1 if inversions % 2 else 1)
        for row in range(size):
            term = polynomial_multiply(term, matrix[row][sigma[row]])
        answer = polynomial_add(answer, term)
    return answer


def polynomial_group_degrees(polynomial):
    """Return the three coordinate-group degrees of every monomial."""
    return {
        (
            sum(exponent[:3]),
            sum(exponent[3:6]),
            sum(exponent[6:]),
        )
        for exponent, coefficient in polynomial.items()
        if coefficient
    }


def latin_support():
    """Return the nine support points a+b+c=0 mod 3."""
    return {
        (colour, nonroot, (-colour - nonroot) % DIM)
        for nonroot in range(DIM)
        for colour in range(DIM)
    }


def audit_matching_interface() -> None:
    """Check the universal formulas on independent exact data."""
    root_blocks, cross = deterministic_blocks()
    for nonroot in range(DIM):
        for colour in range(DIM):
            assert singleton_direct(
                root_blocks, cross, nonroot, colour
            ) == singleton_shared_factor(root_blocks, cross, nonroot, colour)

    for nonroot_colours in product(range(DIM), repeat=DIM):
        assert empty_direct(cross, nonroot_colours) == empty_by_permanent(
            cross, nonroot_colours
        )


def audit_latin_separator() -> tuple[dict, set]:
    """Check the independent target, rank, and no-axis-line certificate."""
    support = latin_support()
    assert len(support) == 9
    assert all(sum(word) % DIM == 0 for word in support)

    for axis in range(DIM):
        others = tuple(index for index in range(DIM) if index != axis)
        for fixed in product(range(DIM), repeat=2):
            line = set()
            for varying in range(DIM):
                word = [0, 0, 0]
                word[axis] = varying
                word[others[0]] = fixed[0]
                word[others[1]] = fixed[1]
                line.add(tuple(word))
            assert len(line & support) == 1

    zero = polynomial_constant(0)

    def singleton_entry(word, nonroot):
        """Return the Latin singleton entry for one nonroot group."""
        colour = word[0]
        expected = (colour, nonroot, (-colour - nonroot) % DIM)
        if word != expected:
            return zero
        return polynomial_variable(3 * nonroot + colour)

    def target_entry(word):
        """Return the contracted GHZ target entry on one root word."""
        if not (word[0] == word[1] == word[2]):
            return zero
        colour = word[0]
        return polynomial_multiply(
            polynomial_multiply(
                polynomial_variable(colour),
                polynomial_variable(3 + colour),
            ),
            polynomial_variable(6 + colour),
        )

    expected_degrees = ((0, 0, 1), (0, 1, 0), (1, 0, 0), (1, 1, 1))
    gamma = {}
    for word in WORDS:
        row = (
            singleton_entry(word, 2),
            singleton_entry(word, 1),
            singleton_entry(word, 0),
            target_entry(word),
        )
        gamma[word] = row
        assert row[3] == target_entry(word)
        for column, entry in enumerate(row):
            if entry:
                assert polynomial_group_degrees(entry) == {
                    expected_degrees[column]
                }

    # The exact solution f=(0,0,0,1) selects the empty column, so verify the
    # complete target identity row by row rather than only on selected rows.
    target_solution = (Fraction(0), Fraction(0), Fraction(0), Fraction(1))
    for word, row in gamma.items():
        left = {}
        for coefficient, scalar in zip(row, target_solution, strict=True):
            left = polynomial_add(left, coefficient, scalar)
        assert left == target_entry(word)

    # Rows (021),(012),(102),(000); columns (xy,xr,yr,empty).
    selected = tuple(
        gamma[word] for word in ((0, 2, 1), (0, 1, 2), (1, 0, 2), (0, 0, 0))
    )
    determinant = polynomial_determinant(selected)
    expected_exponent = [0] * 9
    expected_exponent[0] = 1
    expected_exponent[1] = 1
    expected_exponent[3] = 2
    expected_exponent[6] = 2
    assert determinant == {tuple(expected_exponent): Fraction(1)}

    assert target_solution == (0, 0, 0, 1)
    return determinant, support


def main() -> None:
    """Run the independent exact audit."""
    audit_matching_interface()
    determinant, support = audit_latin_separator()
    print("independent singleton matching interface: AUDIT PASS")
    print("independent six-term empty permanent: AUDIT PASS")
    print(f"Latin-plane support/no-axis certificate: AUDIT PASS ({len(support)})")
    print(f"nonzero rank minor terms: {len(determinant)}")
    print("common-shore realization of Latin separator: EXCLUDED")
    print("S2M eight-control realization: NOT DECIDED")
    print("global conjecture status: UNRESOLVED")


if __name__ == "__main__":
    main()
