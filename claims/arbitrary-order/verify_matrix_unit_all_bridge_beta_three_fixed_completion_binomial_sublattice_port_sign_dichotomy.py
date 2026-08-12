"""Exact primary checks for the A7 binomial-sublattice port-sign dichotomy.

The checker works in the explicitly assumed rank-three block basis from A6.
It enumerates all eight sign characters of that basis and evaluates the
normalized four-term block ``1 + X + Y + Z`` exactly over ``Fraction``.

This is a finite algebra/port QA, not a proof that an A6 fixed completion
exists, that the block lattice lies in any binomial-core lattice, or that a
complete target block is binomial.  No theorem, audit, or repository module is
imported.  The global Krenn--Gu conjecture remains UNRESOLVED.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import product
from typing import TypeAlias

Character: TypeAlias = tuple[int, int, int]
TermSigns: TypeAlias = tuple[int, int, int, int]
LatticeVector: TypeAlias = tuple[int, int, int]


@dataclass(frozen=True)
class SignRestriction:
    """One possible restricted sign character and its exact scalar data."""

    character: Character
    term_signs: TermSigns
    scalar: Fraction
    positive_terms: frozenset[int]
    negative_terms: frozenset[int]

    @property
    def is_balanced(self) -> bool:
        """Return whether the four-term scalar vanishes under this restriction."""

        return self.scalar == 0

    @property
    def combined_ideal_is_unit(self) -> bool:
        """Decide whether adjoining the block makes the quotient ideal a unit."""

        return self.scalar != 0


def build_restriction(character: Character) -> SignRestriction:
    """Evaluate ``1 + X + Y + Z`` at one exact sign character."""

    assert len(character) == 3
    assert all(value in (-1, 1) for value in character)
    term_signs: TermSigns = (1, *character)
    scalar = sum((Fraction(value) for value in term_signs), start=Fraction(0))
    return SignRestriction(
        character=character,
        term_signs=term_signs,
        scalar=scalar,
        positive_terms=frozenset(
            index for index, value in enumerate(term_signs) if value == 1
        ),
        negative_terms=frozenset(
            index for index, value in enumerate(term_signs) if value == -1
        ),
    )


def all_sign_restrictions() -> tuple[SignRestriction, ...]:
    """Enumerate all eight possible restrictions to the rank-three basis."""

    restrictions = tuple(
        build_restriction(character) for character in product((-1, 1), repeat=3)
    )
    assert len(restrictions) == 8
    assert len({item.character for item in restrictions}) == 8
    return restrictions


def assert_scalar_ideal_logic(restrictions: tuple[SignRestriction, ...]) -> None:
    """Check exact quotient scalars and unit/survival alternatives."""

    scalar_counts = {
        scalar: sum(item.scalar == scalar for item in restrictions)
        for scalar in (Fraction(-2), Fraction(0), Fraction(2), Fraction(4))
    }
    assert scalar_counts == {
        Fraction(-2): 1,
        Fraction(0): 3,
        Fraction(2): 3,
        Fraction(4): 1,
    }

    for item in restrictions:
        if item.combined_ideal_is_unit:
            # Modulo the assumed binomial core J_bin, p_B restricts to the
            # scalar s.  If s is nonzero, s^{-1}p_B=1 in the quotient, so
            # (J_bin,p_B)=A in the full group algebra for this restriction.
            inverse = Fraction(1, 1) / item.scalar
            assert item.scalar * inverse == 1
            assert not item.is_balanced
        else:
            # The block adds zero modulo J_bin.  This block alone therefore
            # does not make the combined ideal a unit.
            assert item.scalar == 0
            assert item.is_balanced

    assert sum(item.combined_ideal_is_unit for item in restrictions) == 5
    assert sum(item.is_balanced for item in restrictions) == 3


def assert_balanced_partitions(
    restrictions: tuple[SignRestriction, ...],
) -> tuple[SignRestriction, ...]:
    """Check that zero restrictions are exactly three balanced partitions."""

    balanced = tuple(item for item in restrictions if item.is_balanced)
    assert len(balanced) == 3
    for item in balanced:
        assert len(item.positive_terms) == len(item.negative_terms) == 2
        assert item.positive_terms | item.negative_terms == frozenset(range(4))
        assert item.positive_terms.isdisjoint(item.negative_terms)

    expected_positive_parts = {
        frozenset((0, 1)),
        frozenset((0, 2)),
        frozenset((0, 3)),
    }
    assert {item.positive_terms for item in balanced} == expected_positive_parts
    return balanced


def signed_subtotal(term_signs: TermSigns, indices: frozenset[int]) -> Fraction:
    """Sum the character values on one fixed port doubleton."""

    assert indices <= frozenset(range(4))
    return sum((Fraction(term_signs[index]) for index in indices), Fraction(0))


def character_value(character: Character, vector: LatticeVector) -> int:
    """Evaluate a sign character on one integer lattice vector."""

    value = 1
    for basis_sign, exponent in zip(character, vector, strict=True):
        value *= basis_sign**exponent
    assert value in (-1, 1)
    return value


def determinant_three(rows: tuple[LatticeVector, LatticeVector, LatticeVector]) -> int:
    """Return the exact determinant of three integer lattice generators."""

    (a, b, c), (d, e, f), (g, h, i) = rows
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)


def assert_qc2_port_filter(
    balanced: tuple[SignRestriction, ...],
) -> SignRestriction:
    """Apply the inherited Q/C2 complementary-doubleton nonvanishing rule."""

    # Term order is (M_x1, M_x2, M_y1, M_y2).  A5/A6 give
    # P_B(y,g_y)={M_x1,M_x2} and P_B(x,g_x)={M_y1,M_y2}.
    y_doubleton = frozenset((0, 1))
    x_doubleton = frozenset((2, 3))
    assert y_doubleton.isdisjoint(x_doubleton)
    assert y_doubleton | x_doubleton == frozenset(range(4))

    aligned: list[SignRestriction] = []
    rejected: list[SignRestriction] = []
    for item in balanced:
        y_sum = signed_subtotal(item.term_signs, y_doubleton)
        x_sum = signed_subtotal(item.term_signs, x_doubleton)
        assert y_sum == -x_sum
        if y_sum != 0 and x_sum != 0:
            aligned.append(item)
            assert {y_sum, x_sum} == {Fraction(-2), Fraction(2)}
            assert item.positive_terms in (y_doubleton, x_doubleton)
        else:
            rejected.append(item)
            assert y_sum == x_sum == 0
            assert len(item.positive_terms & y_doubleton) == 1
            assert len(item.positive_terms & x_doubleton) == 1

    assert len(aligned) == 1
    assert len(rejected) == 2
    aligned_restriction = aligned[0]
    assert aligned_restriction.term_signs == (1, 1, -1, -1)
    assert aligned_restriction.character == (1, -1, -1)
    return aligned_restriction


def assert_qq_retains_all_balanced(balanced: tuple[SignRestriction, ...]) -> None:
    """Check that Q/Q has no even-route doubleton restriction to remove one."""

    qq_admissible = tuple(item for item in balanced)
    assert len(qq_admissible) == 3
    assert {item.positive_terms for item in qq_admissible} == {
        frozenset((0, 1)),
        frozenset((0, 2)),
        frozenset((0, 3)),
    }


def assert_sharp_controls(
    aligned: SignRestriction,
    restrictions: tuple[SignRestriction, ...],
) -> None:
    """Replay one aligned restriction and one unit-producing imbalance."""

    # Aligned Q/C2 control: the two fixed doubletons have exact nonzero totals
    # +2 and -2, while the full scalar is zero.
    physical_values = tuple(Fraction(value) for value in (1, 1, -1, -1))
    assert aligned.term_signs == tuple(int(value) for value in physical_values)
    assert sum(physical_values, Fraction(0)) == 0
    assert sum(physical_values[:2], Fraction(0)) == 2
    assert sum(physical_values[2:], Fraction(0)) == -2

    # Explicit aligned parity-consistent binomial core.  In the u-basis take
    # r_1=u_2, r_2=u_3, and r_3=u_1+u_2.  Their determinant is +1, so they are
    # an integer basis: they span the full A6 lattice and have no nonzero
    # integer dependency.  The aligned restriction rho(u)=(+,-,-) assigns
    # rho(r_i)=-1 to all three selected binomial generators.
    aligned_generators: tuple[LatticeVector, LatticeVector, LatticeVector] = (
        (0, 1, 0),
        (0, 0, 1),
        (1, 1, 0),
    )
    aligned_determinant = determinant_three(aligned_generators)
    assert aligned_determinant == 1
    assert abs(aligned_determinant) == 1
    assert aligned.character == (1, -1, -1)
    assert tuple(
        character_value(aligned.character, generator)
        for generator in aligned_generators
    ) == (-1, -1, -1)
    assert signed_subtotal(aligned.term_signs, frozenset((0, 1))) == 2
    assert signed_subtotal(aligned.term_signs, frozenset((2, 3))) == -2

    # Imbalanced sharp binomial-core control: take the three selected binomial
    # generators to be r_i=u_i.  Their sign rule rho(r_i)=-1 therefore forces
    # rho(u_i)=-1 for all i.  The block restricts to 1-1-1-1=-2, and the
    # explicit inverse -1/2 witnesses the scalar unit ideal without assuming
    # any larger ambient binomial lattice.
    all_negative = next(item for item in restrictions if item.character == (-1, -1, -1))
    selected_generators = (
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1),
    )
    assert tuple(
        character_value(all_negative.character, generator)
        for generator in selected_generators
    ) == (
        -1,
        -1,
        -1,
    )
    assert all_negative.term_signs == (1, -1, -1, -1)
    assert all_negative.scalar == -2
    assert all_negative.scalar * Fraction(-1, 2) == 1
    assert all_negative.combined_ideal_is_unit


def main() -> None:
    """Run the exact A7 rank-three sign and port-filter checks."""

    restrictions = all_sign_restrictions()
    assert_scalar_ideal_logic(restrictions)
    balanced = assert_balanced_partitions(restrictions)
    aligned = assert_qc2_port_filter(balanced)
    assert_qq_retains_all_balanced(balanced)
    assert_sharp_controls(aligned, restrictions)

    print("A7 beta-three binomial-sublattice port-sign verifier: PASS")
    print("  rank-three sign characters: 8 total")
    print("  imbalanced restrictions: 5; each makes (J_bin,p_B) the unit ideal")
    print("  balanced restrictions: 3; exactly the three two-plus/two-minus partitions")
    print(
        "  Q/C2: exactly 1 aligned nonzero-doubleton partition; 2 split partitions rejected"
    )
    print("  Q/Q: all 3 balanced partitions remain admissible")
    print("  sharp controls: unimodular aligned core (+2,-2) and r_i=u_i scalar -2")
    print(
        "  scope: conditional on A6 block containment in an assumed binomial sublattice"
    )
    print(
        "  no containment, completion existence, or complete-block binomiality is inferred"
    )
    print("  global Krenn--Gu status: UNRESOLVED")


if __name__ == "__main__":
    main()
