"""Primary exact checks for permanent covariance and based-frame transport."""

from __future__ import annotations

from hashlib import sha256
from itertools import permutations, product
from pathlib import Path

import sympy as sp

RANK = 6
COLOURS = 3
COORDINATE_PERMUTATIONS = tuple(permutations(range(RANK)))
ROOT = Path(__file__).resolve().parents[2]
THEOREM = (
    ROOT
    / "claims/arbitrary-order/"
    "ARBITRARY_PERMANENT_MONOMIAL_COVARIANCE_AND_BASED_FRAME_ORBIT_TRANSPORT_LEMMA.md"
)

DEPENDENCIES = {
    "claims/arbitrary-order/"
    "ARBITRARY_PERMANENT_COTWO_EQUALITY_FIVE_ACTIVE_SUPPORT_ORBIT_SYNTHESIS_THEOREM.md": (
        "9399CCB4286583A1F1E90BD7025E706B3DE47C652214BB1E8B7C8F6BA986A6D5"
    ),
    "docs/audits/"
    "ARBITRARY_PERMANENT_COTWO_EQUALITY_FIVE_ACTIVE_SUPPORT_ORBIT_SYNTHESIS_REVIEW_2026-08-15.md": (
        "BE13F69678F36B6DB79277AF66A85144E0B334C14535DCDD29573AB10FB53F03"
    ),
    "claims/arbitrary-order/"
    "ARBITRARY_PERMANENT_COTWO_R4_BASED_FRAME_ORBIT_CLASSIFICATION_THEOREM.md": (
        "CFF044EA8E89D504F4ECF9C62CA55DFD5361CD54F5CB85083B09AED8B834D677"
    ),
    "docs/audits/"
    "ARBITRARY_PERMANENT_COTWO_R4_BASED_FRAME_ORBIT_CLASSIFICATION_REVIEW_2026-08-15.md": (
        "1C4C0368CA05F68058556823A40E6C0EBD00EC0F5CE706885133626F4645B1AE"
    ),
    "claims/arbitrary-order/"
    "ARBITRARY_PERMANENT_TRIANGLE_PAIR_FULL_EXTENSION_EXCLUSION_THEOREM.md": (
        "02C87A0811777B0A833598D9217FBF117613F8B7089A21C0AE6D4ED6964648B9"
    ),
    "docs/audits/"
    "ARBITRARY_PERMANENT_TRIANGLE_PAIR_FULL_EXTENSION_EXCLUSION_REVIEW_2026-08-15.md": (
        "3D30A06354EA4F929DDD015436B5FD94AC3E05F133743019FB87A1783FADAFCD"
    ),
    "claims/arbitrary-order/"
    "ARBITRARY_PERMANENT_STAR_PAIR_FULL_EXTENSION_EXCLUSION_THEOREM.md": (
        "C9DAABB0C288F6FB54C9FB209FD5D2E341118EFE0C181442899757063EA0B66D"
    ),
    "docs/audits/"
    "ARBITRARY_PERMANENT_STAR_PAIR_FULL_EXTENSION_EXCLUSION_REVIEW_2026-08-15.md": (
        "35ECE859D0DA216D3E60008410FEB109EEA531DCECEFF442A53E1F3C8AC2480D"
    ),
    "claims/arbitrary-order/"
    "ARBITRARY_PERMANENT_FIXED_PAIR_FULL_EXTENSION_EXCLUSION_THEOREM.md": (
        "8AE57E0032B046303260BCEF9DC0AE56635DC9AEAA9AF096D609079523D65DDE"
    ),
    "docs/audits/"
    "ARBITRARY_PERMANENT_FIXED_PAIR_FULL_EXTENSION_EXCLUSION_REVIEW_2026-08-15.md": (
        "BE668BE16F2A9DF74A122CE34D8ADF5F177A35D4ACC9A1596ADF558BCCBDA5F5"
    ),
}


def file_sha256(path: Path) -> str:
    """Return an uppercase SHA-256 digest."""

    return sha256(path.read_bytes()).hexdigest().upper()


def permanent(rows: tuple[tuple[sp.Expr, ...], ...]) -> sp.Expr:
    """Return the exact permanent polynomial of a square row matrix."""

    return sp.Add(
        *(
            sp.prod(rows[row][assignment[row]] for row in range(RANK))
            for assignment in COORDINATE_PERMUTATIONS
        )
    )


def transform_vector(
    vector: tuple[sp.Expr, ...],
    coordinate_permutation: tuple[int, ...],
    scales: tuple[sp.Expr, ...],
) -> tuple[sp.Expr, ...]:
    """Apply (g z)_(pi(i))=d_i z_i."""

    transformed: list[sp.Expr] = [sp.Integer(0)] * RANK
    for source, target in enumerate(coordinate_permutation):
        transformed[target] = scales[source] * vector[source]
    return tuple(transformed)


def verify_symbolic_permanent_covariance() -> dict[str, object]:
    """Check the full six-linear covariance as a symbolic identity."""

    rows = tuple(
        tuple(sp.symbols(f"z{row}_0:{RANK}")) for row in range(RANK)
    )
    scales = tuple(sp.symbols(f"d0:{RANK}", nonzero=True))
    coordinate_permutation = (2, 5, 1, 4, 0, 3)
    transformed_rows = tuple(
        transform_vector(row, coordinate_permutation, scales) for row in rows
    )
    character = sp.prod(scales)
    residual = sp.expand(permanent(transformed_rows) - character * permanent(rows))
    assert residual == 0
    return {
        "rank": RANK,
        "permanent_terms": len(COORDINATE_PERMUTATIONS),
        "coordinate_permutation": coordinate_permutation,
        "character": str(character),
    }


def complementary_polarization(
    quadratic: dict[tuple[int, int], sp.Expr],
    rows: tuple[tuple[sp.Expr, ...], ...],
) -> sp.Expr:
    """Polarize the complementary quartic of a square-free quadratic."""

    assert len(rows) == RANK - 2
    total = sp.Integer(0)
    for pair, coefficient in quadratic.items():
        complement = tuple(index for index in range(RANK) if index not in pair)
        for assignment in permutations(complement):
            total += coefficient * sp.prod(
                rows[row][assignment[row]] for row in range(RANK - 2)
            )
    return total


def transform_quadratic(
    quadratic: dict[tuple[int, int], sp.Expr],
    coordinate_permutation: tuple[int, ...],
    scales: tuple[sp.Expr, ...],
) -> dict[tuple[int, int], sp.Expr]:
    """Apply the induced square-free quadratic coordinate action."""

    transformed: dict[tuple[int, int], sp.Expr] = {}
    for (left, right), coefficient in quadratic.items():
        target = tuple(
            sorted((coordinate_permutation[left], coordinate_permutation[right]))
        )
        transformed[target] = scales[left] * scales[right] * coefficient
    return transformed


def verify_symbolic_complement_covariance() -> dict[str, object]:
    """Check the quartic star-covariance identity with generic coefficients."""

    pairs = tuple(
        (left, right)
        for left in range(RANK)
        for right in range(left + 1, RANK)
    )
    coefficients = sp.symbols(f"q0:{len(pairs)}")
    quadratic = dict(zip(pairs, coefficients, strict=True))
    rows = tuple(
        tuple(sp.symbols(f"y{row}_0:{RANK}")) for row in range(RANK - 2)
    )
    scales = tuple(sp.symbols(f"s0:{RANK}", nonzero=True))
    coordinate_permutation = (4, 1, 5, 0, 3, 2)
    transformed_quadratic = transform_quadratic(
        quadratic, coordinate_permutation, scales
    )
    transformed_rows = tuple(
        transform_vector(row, coordinate_permutation, scales) for row in rows
    )
    character = sp.prod(scales)
    residual = sp.expand(
        complementary_polarization(transformed_quadratic, transformed_rows)
        - character * complementary_polarization(quadratic, rows)
    )
    assert residual == 0
    return {
        "quadratic_basis_size": len(pairs),
        "complement_assignments": len(pairs) * 24,
        "coordinate_permutation": coordinate_permutation,
    }


def delta_value(
    word: tuple[int, ...], diagonal_values: tuple[sp.Expr, ...]
) -> sp.Expr:
    """Evaluate a weighted three-colour diagonal tensor."""

    return diagonal_values[word[0]] if len(set(word)) == 1 else sp.Integer(0)


def verify_colour_and_mode_transport() -> dict[str, object]:
    """Exhaust all colour words in the direct and swapped transport formulas."""

    diagonal_values = tuple(sp.symbols("lambda0:3", nonzero=True))
    left_scales = tuple(sp.symbols("a0:3", nonzero=True))
    right_scales = tuple(sp.symbols("b0:3", nonzero=True))
    character = sp.symbols("chi", nonzero=True)
    colour_permutation = (2, 0, 1)
    direct_nonzero = 0
    swapped_nonzero = 0

    for word in product(range(COLOURS), repeat=RANK):
        direct_source = tuple(colour_permutation[colour] for colour in word)
        direct = (
            left_scales[word[0]]
            * right_scales[word[1]]
            * character
            * delta_value(direct_source, diagonal_values)
        )

        swapped_source = (
            direct_source[1],
            direct_source[0],
            *direct_source[2:],
        )
        swapped = (
            left_scales[word[0]]
            * right_scales[word[1]]
            * character
            * delta_value(swapped_source, diagonal_values)
        )

        if len(set(word)) == 1:
            colour = word[0]
            expected = (
                left_scales[colour]
                * right_scales[colour]
                * character
                * diagonal_values[colour_permutation[colour]]
            )
            assert direct == expected
            assert swapped == expected
            direct_nonzero += 1
            swapped_nonzero += 1
        else:
            assert direct == 0
            assert swapped == 0

    assert direct_nonzero == swapped_nonzero == COLOURS
    return {
        "colour_words": COLOURS**RANK,
        "direct_nonzero": direct_nonzero,
        "swapped_nonzero": swapped_nonzero,
    }


def verify_orbit_residual() -> dict[str, object]:
    """Replay the exact residual-orbit bookkeeping from the frozen census."""

    triangle_orbits = {"012"}
    star_ordered_orbits = {"014": 3, "013": 2, "025": 1, "235": 0}
    fixed_ordered_orbits = {"013": 0, "025": 1, "024": 2}

    triangle_covered = {"012"}
    assert triangle_covered == triangle_orbits

    displayed_star_invariant = star_ordered_orbits["013"]
    star_covered_invariants = {
        displayed_star_invariant,
        3 - displayed_star_invariant,
    }
    assert star_covered_invariants == {1, 2}
    star_residual = {
        representative
        for representative, invariant in star_ordered_orbits.items()
        if invariant not in star_covered_invariants
    }
    assert star_residual == {"014", "235"}
    assert {star_ordered_orbits[item] for item in star_residual} == {0, 3}
    star_residual_swap_representative = "014"

    displayed_fixed_invariant = fixed_ordered_orbits["013"]
    fixed_covered_invariants = {displayed_fixed_invariant}
    fixed_residual = {
        representative
        for representative, invariant in fixed_ordered_orbits.items()
        if invariant not in fixed_covered_invariants
    }
    assert fixed_residual == {"024", "025"}

    residual = (
        star_residual_swap_representative,
        "025",
        "024",
    )
    assert residual == ("014", "025", "024")
    return {
        "triangle_residual": (),
        "star_residual_after_mode_swap": (star_residual_swap_representative,),
        "fixed_residual": ("025", "024"),
        "combined": residual,
    }


def verify_frozen_inputs_and_boundary() -> None:
    """Pin corollary inputs and the theorem's deliberately narrow boundary."""

    for relative_path, expected_hash in DEPENDENCIES.items():
        assert file_sha256(ROOT / relative_path) == expected_hash

    theorem_text = THEOREM.read_text(encoding="utf-8")
    required_fragments = (
        "These are **open extension-exclusion obligations**",
        "remaining pure (4,1) orbit k=0,3:",
        "remaining (4,2) orbit e=1:",
        "remaining (4,2) orbit e=2:",
        "dimension-at-least-six co-two sensor residual:               NOT ADDRESSED;",
        "global Krenn--Gu conjecture:                                UNRESOLVED.",
    )
    for fragment in required_fragments:
        assert fragment in theorem_text


def main() -> None:
    """Run the complete exact primary verification."""

    verify_frozen_inputs_and_boundary()
    permanent_result = verify_symbolic_permanent_covariance()
    complement_result = verify_symbolic_complement_covariance()
    colour_result = verify_colour_and_mode_transport()
    orbit_result = verify_orbit_residual()

    print("permanent monomial covariance and based-frame transport primary: PASS")
    print(f"  permanent_covariance={permanent_result}")
    print(f"  complement_covariance={complement_result}")
    print(f"  colour_and_mode_transport={colour_result}")
    print(f"  orbit_residual={orbit_result}")
    print("  residual obligations: 014,025,024")
    print("  global Krenn-Gu conjecture: UNRESOLVED")


if __name__ == "__main__":
    main()
