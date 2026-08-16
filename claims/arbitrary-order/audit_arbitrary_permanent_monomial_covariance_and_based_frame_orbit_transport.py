"""Independent no-import audit of permanent covariance and orbit transport.

This audit imports neither the primary verifier nor SymPy.  It checks the
monomial reindexing on all coordinate assignments, checks every complementary
quadratic/quartic assignment, and evaluates a separate exact rational
six-mode fixture with a dynamic-programming permanent.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from itertools import combinations, permutations, product
from pathlib import Path

RANK = 6
COLOURS = 3
FULL_COORDINATE_MASK = (1 << RANK) - 1
COORDINATE_ASSIGNMENTS = tuple(permutations(range(RANK)))
ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
THEOREM = (
    HERE
    / "ARBITRARY_PERMANENT_MONOMIAL_COVARIANCE_AND_BASED_FRAME_ORBIT_TRANSPORT_LEMMA.md"
)
PRIMARY = (
    HERE
    / "verify_arbitrary_permanent_monomial_covariance_and_based_frame_orbit_transport.py"
)

THEOREM_SHA256 = "B1762F22813E5B749FF0C81DA6C6CE5E9B8E95601662D87CB21835AAF63C3DA0"
PRIMARY_SHA256 = "E37A2E98447F6058496A3487D0A01F498B331E730CC3B01C72FC6750CEC5838E"

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
        "F1610E9BBCC4065AC24A1E0CD7F81DDAF989BCA5D4026AE2A23BD2FF7A5F680F"
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

Vector = tuple[Fraction, ...]
Triple = tuple[Vector, Vector, Vector]
Modes = tuple[Triple, ...]
Word = tuple[int, ...]


def file_sha256(path: Path) -> str:
    """Hash text after normalizing checkout CRLF to Git blob-style LF."""

    normalized = path.read_bytes().replace(b"\r\n", b"\n")
    return sha256(normalized).hexdigest().upper()


def inverse_permutation(permutation: tuple[int, ...]) -> tuple[int, ...]:
    """Invert a finite permutation."""

    inverse = [0] * len(permutation)
    for source, target in enumerate(permutation):
        inverse[target] = source
    return tuple(inverse)


def audit_permanent_reindexing() -> dict[str, object]:
    """Exhaust the universal term bijection in the covariance proof."""

    coordinate_permutation = (3, 0, 5, 2, 1, 4)
    inverse = inverse_permutation(coordinate_permutation)
    recovered_assignments: set[tuple[int, ...]] = set()

    for target_assignment in COORDINATE_ASSIGNMENTS:
        source_assignment = tuple(inverse[target] for target in target_assignment)
        assert tuple(sorted(source_assignment)) == tuple(range(RANK))
        scale_mask = 0
        for source in source_assignment:
            scale_mask |= 1 << source
        assert scale_mask == FULL_COORDINATE_MASK
        recovered_assignments.add(source_assignment)

    assert recovered_assignments == set(COORDINATE_ASSIGNMENTS)
    return {
        "target_assignments": len(COORDINATE_ASSIGNMENTS),
        "source_assignments": len(recovered_assignments),
        "full_scale_mask": FULL_COORDINATE_MASK,
    }


def audit_complement_reindexing() -> dict[str, object]:
    """Exhaust the quadratic/complement indexing behind star covariance."""

    coordinate_permutation = (1, 5, 0, 4, 2, 3)
    inverse = inverse_permutation(coordinate_permutation)
    checked = 0

    for source_pair in combinations(range(RANK), 2):
        target_pair = {
            coordinate_permutation[source_pair[0]],
            coordinate_permutation[source_pair[1]],
        }
        target_complement = tuple(
            coordinate for coordinate in range(RANK) if coordinate not in target_pair
        )
        source_complement = {
            coordinate for coordinate in range(RANK) if coordinate not in source_pair
        }
        recovered_assignments: set[tuple[int, ...]] = set()

        for target_assignment in permutations(target_complement):
            source_assignment = tuple(inverse[target] for target in target_assignment)
            assert set(source_assignment) == source_complement
            scale_mask = (1 << source_pair[0]) | (1 << source_pair[1])
            for source in source_assignment:
                scale_mask |= 1 << source
            assert scale_mask == FULL_COORDINATE_MASK
            recovered_assignments.add(source_assignment)
            checked += 1

        assert len(recovered_assignments) == 24

    assert checked == 15 * 24
    return {"quadratic_pairs": 15, "complement_assignments": checked}


def matrix_rank(rows: tuple[Vector, ...]) -> int:
    """Compute exact row rank by a standalone Fraction reducer."""

    matrix = [list(row) for row in rows]
    rank = 0
    columns = len(matrix[0]) if matrix else 0
    for column in range(columns):
        pivot = next(
            (row for row in range(rank, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        pivot_value = matrix[rank][column]
        matrix[rank] = [entry / pivot_value for entry in matrix[rank]]
        for row in range(len(matrix)):
            if row == rank or not matrix[row][column]:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                entry - factor * pivot_entry
                for entry, pivot_entry in zip(matrix[row], matrix[rank], strict=True)
            ]
        rank += 1
        if rank == len(matrix):
            break
    return rank


def permanent_dynamic(rows: tuple[Vector, ...]) -> Fraction:
    """Evaluate a square permanent by subset dynamic programming."""

    size = len(rows)
    assert all(len(row) == size for row in rows)
    states: dict[int, Fraction] = {0: Fraction(1)}
    for row_index, row in enumerate(rows):
        next_states: dict[int, Fraction] = {}
        for mask, subtotal in states.items():
            assert mask.bit_count() == row_index
            for column, entry in enumerate(row):
                if mask & (1 << column):
                    continue
                next_mask = mask | (1 << column)
                next_states[next_mask] = (
                    next_states.get(next_mask, Fraction(0)) + subtotal * entry
                )
        states = next_states
    return states[(1 << size) - 1]


def fixture_modes() -> Modes:
    """Build six deterministic, noncoordinate, independent local triples."""

    modes: list[Triple] = []
    for mode in range(RANK):
        triple: list[Vector] = []
        for colour in range(COLOURS):
            vector = tuple(
                Fraction(
                    (mode + 2) * (coordinate + 1)
                    + (colour + 1) * (coordinate * coordinate + 2)
                    + (9 + mode if coordinate == (mode + 2 * colour) % RANK else 0)
                    - 13
                )
                for coordinate in range(RANK)
            )
            triple.append(vector)
        exact_triple = tuple(triple)
        assert len(exact_triple) == COLOURS
        assert matrix_rank(exact_triple) == COLOURS
        modes.append(exact_triple)  # type: ignore[arg-type]
    return tuple(modes)


def transform_vector(
    vector: Vector,
    coordinate_permutation: tuple[int, ...],
    scales: Vector,
) -> Vector:
    """Apply the audit's independent monomial-map implementation."""

    transformed = [Fraction(0)] * RANK
    for source, target in enumerate(coordinate_permutation):
        transformed[target] = scales[source] * vector[source]
    return tuple(transformed)


def scale_vector(scale: Fraction, vector: Vector) -> Vector:
    """Scale one exact vector."""

    return tuple(scale * entry for entry in vector)


def coefficient_tensor(modes: Modes) -> dict[Word, Fraction]:
    """Evaluate all 3^6 entries of one six-mode restriction tensor."""

    tensor: dict[Word, Fraction] = {}
    for word in product(range(COLOURS), repeat=RANK):
        rows = tuple(modes[mode][word[mode]] for mode in range(RANK))
        tensor[word] = permanent_dynamic(rows)
    return tensor


def transformed_modes(
    modes: Modes,
    coordinate_permutation: tuple[int, ...],
    scales: Vector,
    colour_permutation: tuple[int, ...],
    left_scales: tuple[Fraction, ...],
    right_scales: tuple[Fraction, ...],
    *,
    swap_first_two: bool,
) -> Modes:
    """Construct the direct or omitted-mode-swapped transported fixture."""

    transformed: list[Triple] = []
    source_modes = (1, 0, *range(2, RANK)) if swap_first_two else tuple(range(RANK))
    for mode, source_mode in enumerate(source_modes):
        triple: list[Vector] = []
        for colour in range(COLOURS):
            vector = transform_vector(
                modes[source_mode][colour_permutation[colour]],
                coordinate_permutation,
                scales,
            )
            if mode == 0:
                vector = scale_vector(left_scales[colour], vector)
            elif mode == 1:
                vector = scale_vector(right_scales[colour], vector)
            triple.append(vector)
        exact_triple = tuple(triple)
        assert matrix_rank(exact_triple) == COLOURS
        transformed.append(exact_triple)  # type: ignore[arg-type]
    return tuple(transformed)


def audit_exact_tensor_fixture() -> dict[str, object]:
    """Check every coefficient of an independently evaluated rational fixture."""

    modes = fixture_modes()
    coordinate_permutation = (2, 5, 1, 4, 0, 3)
    scales = (
        Fraction(2, 3),
        Fraction(-3, 2),
        Fraction(5, 4),
        Fraction(7, 3),
        Fraction(-11, 5),
        Fraction(13, 7),
    )
    colour_permutation = (2, 0, 1)
    left_scales = (Fraction(2), Fraction(-3, 2), Fraction(5, 3))
    right_scales = (Fraction(7, 5), Fraction(11, 3), Fraction(-13, 2))
    character = Fraction(1)
    for scale in scales:
        character *= scale

    original = coefficient_tensor(modes)
    direct_modes = transformed_modes(
        modes,
        coordinate_permutation,
        scales,
        colour_permutation,
        left_scales,
        right_scales,
        swap_first_two=False,
    )
    swapped_modes = transformed_modes(
        modes,
        coordinate_permutation,
        scales,
        colour_permutation,
        left_scales,
        right_scales,
        swap_first_two=True,
    )
    direct = coefficient_tensor(direct_modes)
    swapped = coefficient_tensor(swapped_modes)

    for word in product(range(COLOURS), repeat=RANK):
        relabeled = tuple(colour_permutation[colour] for colour in word)
        expected_direct = (
            character
            * left_scales[word[0]]
            * right_scales[word[1]]
            * original[relabeled]
        )
        assert direct[word] == expected_direct

        swapped_word = (relabeled[1], relabeled[0], *relabeled[2:])
        expected_swapped = (
            character
            * left_scales[word[0]]
            * right_scales[word[1]]
            * original[swapped_word]
        )
        assert swapped[word] == expected_swapped

    return {
        "local_triples": RANK,
        "entries_each": COLOURS**RANK,
        "direct_entries_checked": len(direct),
        "swapped_entries_checked": len(swapped),
        "character": str(character),
    }


def audit_target_support_and_residual() -> dict[str, object]:
    """Independently check Delta support preservation and residual labels."""

    colour_permutation = (1, 2, 0)
    diagonal_values = (Fraction(2), Fraction(-3), Fraction(5))
    left_scales = (Fraction(7), Fraction(11), Fraction(13))
    right_scales = (Fraction(-2), Fraction(3), Fraction(-5))
    character = Fraction(17)
    nonzero_direct: list[Word] = []
    nonzero_swapped: list[Word] = []

    for word in product(range(COLOURS), repeat=RANK):
        relabeled = tuple(colour_permutation[colour] for colour in word)
        direct_source = (
            diagonal_values[relabeled[0]] if len(set(relabeled)) == 1 else 0
        )
        swapped_relabeled = (relabeled[1], relabeled[0], *relabeled[2:])
        swapped_source = (
            diagonal_values[swapped_relabeled[0]]
            if len(set(swapped_relabeled)) == 1
            else 0
        )
        direct = (
            character * left_scales[word[0]] * right_scales[word[1]] * direct_source
        )
        swapped = (
            character
            * left_scales[word[0]]
            * right_scales[word[1]]
            * swapped_source
        )
        if direct:
            nonzero_direct.append(word)
        if swapped:
            nonzero_swapped.append(word)

    diagonal_words = [(colour,) * RANK for colour in range(COLOURS)]
    assert nonzero_direct == diagonal_words
    assert nonzero_swapped == diagonal_words

    star_invariants = {"014": 3, "013": 2, "025": 1, "235": 0}
    fixed_invariants = {"013": 0, "025": 1, "024": 2}
    star_covered = {2, 3 - 2}
    star_residual = {
        label for label, invariant in star_invariants.items() if invariant not in star_covered
    }
    assert star_residual == {"014", "235"}
    assert {star_invariants[label] for label in star_residual} == {0, 3}
    star_swap_pairs = {
        label: next(
            other
            for other, other_invariant in star_invariants.items()
            if other_invariant == 3 - invariant
        )
        for label, invariant in star_invariants.items()
    }
    assert star_swap_pairs["014"] == "235"
    assert star_swap_pairs["235"] == "014"
    fixed_residual = {
        label for label, invariant in fixed_invariants.items() if invariant != 0
    }
    assert fixed_residual == {"024", "025"}
    fixed_by_invariant = {
        invariant: label for label, invariant in fixed_invariants.items()
    }
    residual_representatives = (
        min(star_residual),
        fixed_by_invariant[1],
        fixed_by_invariant[2],
    )
    assert residual_representatives == ("014", "025", "024")

    return {
        "direct_support": len(nonzero_direct),
        "swapped_support": len(nonzero_swapped),
        "residual_representatives": residual_representatives,
    }


def audit_frozen_bytes_and_boundary() -> None:
    """Reject theorem, primary, dependency, or scope drift."""

    assert file_sha256(THEOREM) == THEOREM_SHA256
    assert file_sha256(PRIMARY) == PRIMARY_SHA256
    for relative_path, expected_hash in DEPENDENCIES.items():
        actual_hash = file_sha256(ROOT / relative_path)
        assert actual_hash == expected_hash, (
            f"{relative_path}: expected {expected_hash}, got {actual_hash}"
        )

    theorem_text = THEOREM.read_text(encoding="utf-8")
    required_fragments = (
        "The pair `(u,v)` is extendible if and only if `(u',v')` is extendible",
        "These are **open extension-exclusion obligations**",
        "It does not mean feasible, extendible, or realized.",
        "nonextension of residual 014:                               NOT PROVED HERE;",
        "dimension-at-least-six co-two sensor residual:               NOT ADDRESSED;",
        "global Krenn--Gu conjecture:                                UNRESOLVED.",
    )
    for fragment in required_fragments:
        assert fragment in theorem_text


def main() -> None:
    """Run the complete independent exact audit."""

    audit_frozen_bytes_and_boundary()
    permanent_result = audit_permanent_reindexing()
    complement_result = audit_complement_reindexing()
    fixture_result = audit_exact_tensor_fixture()
    target_result = audit_target_support_and_residual()

    print("permanent monomial covariance and based-frame transport audit: PASS")
    print(f"  permanent_reindexing={permanent_result}")
    print(f"  complement_reindexing={complement_result}")
    print(f"  exact_tensor_fixture={fixture_result}")
    print(f"  target_and_residual={target_result}")
    print("  imports primary: NO")
    print("  imports SymPy: NO")
    print("  residual obligations: 014,025,024")
    print("  global Krenn-Gu conjecture: UNRESOLVED")


if __name__ == "__main__":
    main()
