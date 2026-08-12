"""Independent exact audit of the bounded A7 sign-character mechanism.

This standard-library audit starts *after* two theorem-level assumptions:

1. the free rank-three A6 difference lattice ``L_A6`` is contained in the
   relevant binomial lattice ``L_bin``; and
2. one common nonzero fixed completion injects the four A6 terms into the
   complete mixed fibre.

It does not try to prove either assumption.  Instead it models ``L_A6`` as
``Z^3``, enumerates all eight possible restrictions to ``L_A6`` of a
``{+1,-1}``-valued binomial character ``rho``, and evaluates the four-term group-
algebra block independently with bitmask characters.  The Q/C^2 doubleton
partition and the Q/Q singleton boundary are then checked term by term.

Each enumerated row is only a *possible restriction* of ``rho`` from
``L_bin``.  One fixed binomial core has one such restriction, not eight
simultaneous sheets; the enumeration is an exhaustive case split and is not
a U7F torsion-sheet decomposition.  This file neither proves that any listed
restriction extends to the ambient lattice nor that a binomial core, fixed
completion, or witness exists.  The result is conditional on whichever one
restriction is realized, and the global Krenn--Gu conjecture is UNRESOLVED.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import product

Exponent = tuple[int, int, int]
Polynomial = dict[Exponent, Fraction]

ZERO: Exponent = (0, 0, 0)
E_X: Exponent = (1, 0, 0)
E_Y: Exponent = (0, 1, 0)
E_Z: Exponent = (0, 0, 1)

# This labelling is the A6 Q/C^2 labelling after choosing M_x1 as reference.
# Its use is conditional on the assumed A6 block and fixed completion; it is
# not reconstructed from, or imported from, the primary verifier.
TERM_ORDER = ("M_x1", "M_x2", "M_y1", "M_y2")
TERM_EXPONENTS: dict[str, Exponent] = {
    "M_x1": ZERO,
    "M_x2": E_X,
    "M_y1": E_Y,
    "M_y2": E_Z,
}
BLOCK: Polynomial = {exponent: Fraction(1) for exponent in TERM_EXPONENTS.values()}

# In Q/C^2 the even-route endpoint at y uses the two x-labelled matchings,
# while the endpoint at x uses the two y-labelled matchings.  These are ports
# restricted to the four-term fixed-completion block.
QC2_Y_PORT = ("M_x1", "M_x2")
QC2_X_PORT = ("M_y1", "M_y2")

# The three ways to partition four terms into complementary unordered pairs.
PAIR_PARTITIONS = (
    (("M_x1", "M_x2"), ("M_y1", "M_y2")),
    (("M_x1", "M_y1"), ("M_x2", "M_y2")),
    (("M_x1", "M_y2"), ("M_x2", "M_y1")),
)


def add_exponents(left: Exponent, right: Exponent) -> Exponent:
    """Add two exponent vectors in the free lattice Z^3."""

    return tuple(a + b for a, b in zip(left, right, strict=True))  # type: ignore[return-value]


@dataclass(frozen=True)
class SignCharacter:
    """A homomorphism Z^3 -> {+1,-1}, encoded by a three-bit dual mask."""

    dual_mask: int

    def __post_init__(self) -> None:
        if not 0 <= self.dual_mask < 8:
            raise ValueError("a rank-three sign character needs a mask in [0, 8)")

    def __call__(self, exponent: Exponent) -> Fraction:
        parity = (
            sum(
                ((self.dual_mask >> index) & 1) * coordinate
                for index, coordinate in enumerate(exponent)
            )
            % 2
        )
        return Fraction(-1 if parity else 1)

    @property
    def basis_values(self) -> tuple[Fraction, Fraction, Fraction]:
        """Return the character values on the displayed A6 basis."""

        return (self(E_X), self(E_Y), self(E_Z))

    @property
    def bit_label(self) -> str:
        """Display dual bits in X,Y,Z basis order, not integer print order."""

        return "".join(str((self.dual_mask >> index) & 1) for index in range(3))


@dataclass(frozen=True)
class CommonUnitMultiple:
    """A scalar times the common assumed nonzero reference/completion unit.

    Under one character restriction every matching monomial is ``+U`` or ``-U``.
    The formal symbol U absorbs both the reference matching monomial and the
    fixed nonzero completion.  Consequently a sum is zero exactly when its
    rational coefficient is zero; no numerical value of U is assumed.
    """

    coefficient: Fraction

    def __add__(self, other: CommonUnitMultiple) -> CommonUnitMultiple:
        return CommonUnitMultiple(self.coefficient + other.coefficient)

    def __neg__(self) -> CommonUnitMultiple:
        return CommonUnitMultiple(-self.coefficient)

    @property
    def is_zero(self) -> bool:
        return self.coefficient == 0


@dataclass(frozen=True)
class RestrictionResult:
    """Exact restriction data for one rank-three sign character."""

    character: SignCharacter
    term_signs: tuple[Fraction, Fraction, Fraction, Fraction]
    block_scalar: Fraction
    scalar_inverse: Fraction | None
    qc2_y_port: CommonUnitMultiple
    qc2_x_port: CommonUnitMultiple
    aligned_partition_count: int

    @property
    def is_scalar_unit(self) -> bool:
        return self.scalar_inverse is not None

    @property
    def is_balanced(self) -> bool:
        return self.block_scalar == 0

    @property
    def qc2_alignment(self) -> str:
        if not self.is_balanced:
            return "not-balanced"
        if not self.qc2_y_port.is_zero and not self.qc2_x_port.is_zero:
            return "aligned-nonzero"
        return "imbalanced-zero"


def evaluate(polynomial: Polynomial, character: SignCharacter) -> Fraction:
    """Evaluate a finite group-algebra polynomial under one character."""

    return sum(
        (
            coefficient * character(exponent)
            for exponent, coefficient in polynomial.items()
        ),
        Fraction(0),
    )


def term_values(character: SignCharacter) -> dict[str, Fraction]:
    """Evaluate the four normalized A6 matching monomials."""

    return {label: character(exponent) for label, exponent in TERM_EXPONENTS.items()}


def port_multiple(
    values: dict[str, Fraction], port: tuple[str, str]
) -> CommonUnitMultiple:
    """Add a two-term port after restoring its common nonzero unit."""

    return CommonUnitMultiple(sum((values[label] for label in port), Fraction(0)))


def aligned_partitions(values: dict[str, Fraction]) -> tuple[int, ...]:
    """Find pair partitions whose two sums are nonzero exact negatives."""

    output: list[int] = []
    for index, (first, second) in enumerate(PAIR_PARTITIONS):
        first_sum = port_multiple(values, first)
        second_sum = port_multiple(values, second)
        if (
            not first_sum.is_zero
            and not second_sum.is_zero
            and first_sum == -second_sum
        ):
            output.append(index)
    return tuple(output)


def analyse(character: SignCharacter) -> RestrictionResult:
    """Compute exact scalar and port data for one possible rho restriction."""

    values = term_values(character)
    signs = tuple(values[label] for label in TERM_ORDER)
    block_scalar = evaluate(BLOCK, character)
    assert block_scalar == sum(signs, Fraction(0))

    scalar_inverse = None if block_scalar == 0 else Fraction(1, block_scalar)
    if scalar_inverse is not None:
        # Over characteristic zero a nonzero rational scalar is a unit on the
        # evaluated quotient.  It is conditional on this one restriction.
        assert block_scalar * scalar_inverse == 1

    qc2_y = port_multiple(values, QC2_Y_PORT)
    qc2_x = port_multiple(values, QC2_X_PORT)
    if block_scalar == 0:
        assert qc2_y == -qc2_x

    partitions = aligned_partitions(values)
    return RestrictionResult(
        character=character,
        term_signs=signs,
        block_scalar=block_scalar,
        scalar_inverse=scalar_inverse,
        qc2_y_port=qc2_y,
        qc2_x_port=qc2_x,
        aligned_partition_count=len(partitions),
    )


def audit_character_space() -> tuple[RestrictionResult, ...]:
    """Exhaust all homomorphisms from the displayed free lattice to signs."""

    characters = tuple(SignCharacter(mask) for mask in range(8))
    assert len({character.basis_values for character in characters}) == 8
    assert {character.basis_values for character in characters} == set(
        product((Fraction(1), Fraction(-1)), repeat=3)
    )

    # Check the bitmask implementation is multiplicative on an exact box of
    # positive and negative exponent vectors.  Freeness then explains why the
    # three basis values determine each character globally.
    box = tuple(product(range(-2, 3), repeat=3))
    for character in characters:
        assert character(ZERO) == 1
        for left in box:
            for right in box:
                assert character(add_exponents(left, right)) == (
                    character(left) * character(right)
                )

    results = tuple(analyse(character) for character in characters)
    assert tuple(result.block_scalar for result in results) == (
        Fraction(4),
        Fraction(2),
        Fraction(2),
        Fraction(0),
        Fraction(2),
        Fraction(0),
        Fraction(0),
        Fraction(-2),
    )

    unit_results = tuple(result for result in results if result.is_scalar_unit)
    balanced_results = tuple(result for result in results if result.is_balanced)
    assert len(unit_results) == 5
    assert len(balanced_results) == 3
    assert all(
        sum(value == 1 for value in result.term_signs) == 2
        for result in balanced_results
    )
    assert all(
        sum(value == -1 for value in result.term_signs) == 2
        for result in balanced_results
    )
    return results


def audit_qc2_port_alignment(
    results: tuple[RestrictionResult, ...],
) -> dict[str, object]:
    """Classify Q/C^2 doubletons for every possible rho restriction."""

    balanced = tuple(result for result in results if result.is_balanced)
    aligned = tuple(
        result for result in balanced if result.qc2_alignment == "aligned-nonzero"
    )
    imbalanced = tuple(
        result for result in balanced if result.qc2_alignment == "imbalanced-zero"
    )

    # Every balanced sign pattern aligns with exactly one of the three pair
    # partitions.  The *fixed* Q/C^2 even-route partition is partition zero,
    # so only one pattern retains its imported nonzero doubleton sums.
    assert all(result.aligned_partition_count == 1 for result in balanced)
    assert len(aligned) == 1
    assert len(imbalanced) == 2

    aligned_control = aligned[0]
    assert aligned_control.character.bit_label == "011"
    assert aligned_control.term_signs == (1, 1, -1, -1)
    assert aligned_control.qc2_y_port.coefficient == 2
    assert aligned_control.qc2_x_port.coefficient == -2
    assert aligned_control.qc2_y_port == -aligned_control.qc2_x_port

    # Sharp imbalanced controls: the four-term scalar is still balanced, but
    # each chosen complementary doubleton cancels internally.  Thus total
    # balance alone cannot recover the A5 nonvanishing condition.
    assert {result.character.bit_label for result in imbalanced} == {"110", "101"}
    assert {result.term_signs for result in imbalanced} == {
        (1, -1, -1, 1),
        (1, -1, 1, -1),
    }
    assert all(result.qc2_y_port.is_zero for result in imbalanced)
    assert all(result.qc2_x_port.is_zero for result in imbalanced)

    # Restoring any common nonzero reference/completion unit U preserves the
    # zero/nonzero and exact-negative conclusions because all port values are
    # represented as their exact coefficient times that same formal U.
    assert not aligned_control.qc2_y_port.is_zero
    assert not aligned_control.qc2_x_port.is_zero

    return {
        "balanced_restrictions": tuple(
            result.character.bit_label for result in balanced
        ),
        "aligned_nonzero": aligned_control.character.bit_label,
        "aligned_port_coefficients_times_U": (
            aligned_control.qc2_y_port.coefficient,
            aligned_control.qc2_x_port.coefficient,
        ),
        "sharp_imbalanced_zero_controls": tuple(
            result.character.bit_label for result in imbalanced
        ),
    }


def audit_qq_boundary(
    results: tuple[RestrictionResult, ...],
) -> dict[str, object]:
    """Show why Q/Q singleton ports do not select one balanced character."""

    balanced = tuple(result for result in results if result.is_balanced)
    surviving_labels: list[str] = []
    for result in balanced:
        # Each odd Q/Q route has the same singleton matching at both ends.
        # Its restored value is +U or -U, hence nonzero in every restriction.
        paired_endpoint_singletons = tuple(
            (
                CommonUnitMultiple(sign),
                CommonUnitMultiple(sign),
            )
            for sign in result.term_signs
        )
        assert all(left == right for left, right in paired_endpoint_singletons)
        assert all(not left.is_zero for left, _ in paired_endpoint_singletons)
        surviving_labels.append(result.character.bit_label)

    # Q/Q supplies no complementary doubleton nonvanishing condition, so its
    # paired singleton data leaves all three balanced restrictions possible.
    assert len(surviving_labels) == 3
    return {
        "balanced_restrictions_not_separated": tuple(surviving_labels),
        "boundary": "paired nonzero singletons select no balanced restriction",
    }


def print_restriction_table(results: tuple[RestrictionResult, ...]) -> None:
    """Print a compact exhaustive character table."""

    print("bits(XYZ)  term signs              block  case           Q/C2 ports")
    for result in results:
        signs = "".join("+" if value == 1 else "-" for value in result.term_signs)
        case = "scalar-unit" if result.is_scalar_unit else "balanced"
        ports = (
            f"({result.qc2_y_port.coefficient:+},{result.qc2_x_port.coefficient:+})*U"
        )
        print(
            f"{result.character.bit_label:>9}  {signs:^22}  "
            f"{result.block_scalar!s:>5}  {case:<11}  {ports}"
        )


def main() -> None:
    """Run the independent bounded A7 sign-character audit."""

    results = audit_character_space()
    qc2 = audit_qc2_port_alignment(results)
    qq = audit_qq_boundary(results)

    print("PASS: independent A7 binomial-sublattice port-sign audit")
    print_restriction_table(results)
    print(f"Q/C^2 alignment: {qc2}")
    print(f"Q/Q boundary: {qq}")
    print("ASSUMED: injective lattice inclusion L_A6 subset L_bin")
    print("ASSUMED: one common nonzero fixed completion of the four A6 terms")
    print("SCOPE: exhaustive alternatives for the one realized rho restriction")
    print("NOT a simultaneous family of restrictions or a U7F torsion-sheet census")
    print("NO universal binomial core, completion, witness, or exclusion is inferred")
    print("GLOBAL KRENN-GU STATUS: UNRESOLVED")


if __name__ == "__main__":
    main()
