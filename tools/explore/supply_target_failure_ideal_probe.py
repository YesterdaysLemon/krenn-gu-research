"""Audit the exact r=3/r=4 supply--target failure formulation.

This is a model-equivalence and size probe, not a solver and not a universal
failure ideal.  It records the complete physical GHZ coefficient system, the
GLS2 function-field sensor sizes, and the fixed-Q GLD5 module sizes.  It also
checks two exact rational-function examples which show why neither a kernel
at one outside contraction nor generic selector failure represents the
pointwise bridge obligation.

The output deliberately stops before elimination.  In particular, it does
not replace maximum-root maximality by blocker quotas, does not replace a
K(z)-kernel by a constant vector, and does not claim that the r=3 target
module enters the existing four-root GLD attachment theorem.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from fractions import Fraction
from functools import cache
from itertools import combinations, product
from math import comb

Word = tuple[int, ...]
Edge = tuple[int, int]
Matching = tuple[Edge, ...]


def odd_double_factorial(value: int) -> int:
    """Return value!! for odd value >= -1."""
    if value in (-1, 1):
        return 1
    answer = 1
    for factor in range(value, 0, -2):
        answer *= factor
    return answer


@cache
def perfect_matchings(vertices: tuple[int, ...]) -> tuple[Matching, ...]:
    """Canonical exact matching list used by the coefficient formula."""
    if not vertices:
        return ((),)
    first = vertices[0]
    answer: list[Matching] = []
    for index in range(1, len(vertices)):
        partner = vertices[index]
        remaining = vertices[1:index] + vertices[index + 1 :]
        for tail in perfect_matchings(remaining):
            answer.append(((first, partner),) + tail)
    return tuple(answer)


def deck_module_dimension(outside_count: int) -> int:
    """Sum 3^|I| over nonempty even I in an outside set."""
    return (4**outside_count + (-2) ** outside_count) // 2 - 1


def companion_entry_terms(root_count: int, outside_order: int) -> int:
    """Expanded monomials in one generic root-word companion entry.

    At surplus two, outside_order=2+2p and the complementary companion uses
    p root--root edges and r-2p root--outside edges.  Choosing the partial
    matching, its bijection to the complementary outside set, and one of the
    three outside endpoint coordinates gives the displayed count.
    """
    p = (outside_order - 2) // 2
    partial_matchings = comb(root_count, 2 * p) * odd_double_factorial(2 * p - 1)
    remaining_roots = root_count - 2 * p
    bijections = 1
    for factor in range(2, remaining_roots + 1):
        bijections *= factor
    return partial_matchings * bijections * 3**remaining_roots


def structural_formula_hash(vertex_count: int) -> str:
    """Hash the canonical lazy specification of every GHZ equation.

    The coefficient of a word is, by definition, the sum over the returned
    ordered matching list of the product of the edge entry selected by that
    word.  Hashing the complete word/RHS ledger and matching list pins this
    Cartesian formula without materializing tens of millions of monomials.
    """
    digest = hashlib.sha256()
    digest.update(f"ternary-hafnian-ghz-v1:n={vertex_count}\n".encode())
    for matching in perfect_matchings(tuple(range(vertex_count))):
        digest.update(repr(matching).encode())
        digest.update(b"\n")
    for word in product(range(3), repeat=vertex_count):
        rhs = int(len(set(word)) == 1)
        digest.update(bytes(word))
        digest.update(bytes((rhs,)))
    return digest.hexdigest()


def deterministic_edge_entries(
    vertex_count: int,
) -> dict[tuple[int, int, int, int], int]:
    """Small exact integer graph used only to audit coefficient evaluation."""
    entries: dict[tuple[int, int, int, int], int] = {}
    for edge_index, (left, right) in enumerate(combinations(range(vertex_count), 2)):
        for left_colour, right_colour in product(range(3), repeat=2):
            value = (7 * edge_index + 5 * left_colour + 3 * right_colour + 1) % 7 - 3
            entries[(left, right, left_colour, right_colour)] = value
    return entries


def explicit_coefficient(
    word: Word,
    matchings: tuple[Matching, ...],
    entries: dict[tuple[int, int, int, int], int],
) -> int:
    total = 0
    for matching in matchings:
        monomial = 1
        for left, right in matching:
            monomial *= entries[(left, right, word[left], word[right])]
        total += monomial
    return total


def recursive_coefficient(
    word: Word, entries: dict[tuple[int, int, int, int], int]
) -> int:
    """Independent bit-mask hafnian evaluation of one physical coefficient."""
    vertex_count = len(word)

    @cache
    def recurse(mask: int) -> int:
        if mask == 0:
            return 1
        first_bit = mask & -mask
        first = first_bit.bit_length() - 1
        rest = mask ^ first_bit
        total = 0
        partners = rest
        while partners:
            partner_bit = partners & -partners
            partner = partner_bit.bit_length() - 1
            total += entries[(first, partner, word[first], word[partner])] * recurse(
                rest ^ partner_bit
            )
            partners ^= partner_bit
        return total

    return recurse((1 << vertex_count) - 1)


def audit_coefficient_formula(vertex_count: int, exhaustive: bool) -> int:
    """Compare the matching expansion with a separate recurrence over Z."""
    matchings = perfect_matchings(tuple(range(vertex_count)))
    entries = deterministic_edge_entries(vertex_count)
    if exhaustive:
        words = product(range(3), repeat=vertex_count)
    else:
        selected = {(colour,) * vertex_count for colour in range(3)}
        selected.update(
            {
                tuple((index + shift) % 3 for index in range(vertex_count))
                for shift in range(3)
            }
        )
        selected.update(
            {
                tuple((index // 2 + shift) % 3 for index in range(vertex_count))
                for shift in range(3)
            }
        )
        words = iter(sorted(selected))
    checked = 0
    for word in words:
        assert explicit_coefficient(word, matchings, entries) == recursive_coefficient(
            word, entries
        )
        checked += 1
    return checked


@dataclass(frozen=True)
class CaseLedger:
    root_count: int
    vertex_count: int
    outside_count: int
    physical_graph_entries: int
    root_vector_coordinates: int
    root_pair_equations: int
    maximum_root_laurent_tests: int
    ghz_equations: int
    ghz_pure_equations: int
    ghz_mixed_equations: int
    coefficient_degree: int
    perfect_matchings_per_equation: int
    expanded_ghz_monomial_occurrences: int
    sensor_rows_over_function_field: int
    sensor_pair_columns: int
    sensor_higher_columns: int
    sensor_total_columns: int
    pair_failure_rank_branches: int
    fixed_q_coordinate_columns: int
    fixed_q_nuisance_columns: int
    fixed_q_failure_rank_branches: int
    residual_pair_choices: int
    companion_expanded_monomial_occurrences: int
    full_deck_tensor_dimension: int
    fixed_q_open_target_dimension: int
    selector_pair_targets_per_q: int
    selector_pair_ambient_rows: int
    selector_pair_rank_branches: int
    selector_pair_nuisance_generators: int
    selector_all_port_ambient_rows: int
    selector_all_port_rank_branches: int
    selector_all_port_nuisance_generators: int
    all_q_all_selector_naive_auxiliaries: int
    structural_formula_sha256: str


def build_case(root_count: int) -> CaseLedger:
    outside_count = root_count + 2
    vertex_count = 2 * root_count + 2
    matching_count = odd_double_factorial(vertex_count - 1)
    pair_columns = comb(outside_count, 2)
    total_columns = 2 ** (root_count + 1) - 1
    higher_columns = total_columns - pair_columns
    q_choices = pair_columns
    fixed_q_columns = 2**root_count - 1
    nuisance_columns = total_columns - fixed_q_columns
    companion_occurrences = 0
    for outside_order in range(2, outside_count + 1, 2):
        label_count = comb(outside_count, outside_order)
        companion_occurrences += (
            3**root_count
            * label_count
            * companion_entry_terms(root_count, outside_order)
        )
    deck_dimension = deck_module_dimension(outside_count)
    selector_pair_targets = comb(root_count, 2)
    pair_generators = deck_dimension * 3**2
    all_port_generators = deck_dimension * 3**root_count
    all_selector_auxiliaries = q_choices * (
        selector_pair_targets * pair_generators + all_port_generators
    )
    return CaseLedger(
        root_count=root_count,
        vertex_count=vertex_count,
        outside_count=outside_count,
        physical_graph_entries=comb(vertex_count, 2) * 9,
        root_vector_coordinates=3 * root_count,
        root_pair_equations=comb(root_count, 2),
        maximum_root_laurent_tests=comb(vertex_count, root_count + 1),
        ghz_equations=3**vertex_count,
        ghz_pure_equations=3,
        ghz_mixed_equations=3**vertex_count - 3,
        coefficient_degree=vertex_count // 2,
        perfect_matchings_per_equation=matching_count,
        expanded_ghz_monomial_occurrences=3**vertex_count * matching_count,
        sensor_rows_over_function_field=3**root_count,
        sensor_pair_columns=pair_columns,
        sensor_higher_columns=higher_columns,
        sensor_total_columns=total_columns,
        pair_failure_rank_branches=higher_columns + 1,
        fixed_q_coordinate_columns=fixed_q_columns,
        fixed_q_nuisance_columns=nuisance_columns,
        fixed_q_failure_rank_branches=nuisance_columns + 1,
        residual_pair_choices=q_choices,
        companion_expanded_monomial_occurrences=companion_occurrences,
        full_deck_tensor_dimension=deck_dimension,
        fixed_q_open_target_dimension=3 ** (2 * root_count),
        selector_pair_targets_per_q=selector_pair_targets,
        selector_pair_ambient_rows=3 ** (2 * root_count - 2),
        selector_pair_rank_branches=3 ** (2 * root_count - 2) + 1,
        selector_pair_nuisance_generators=pair_generators,
        selector_all_port_ambient_rows=3**root_count,
        selector_all_port_rank_branches=3**root_count + 1,
        selector_all_port_nuisance_generators=all_port_generators,
        all_q_all_selector_naive_auxiliaries=all_selector_auxiliaries,
        structural_formula_sha256=structural_formula_hash(vertex_count),
    )


def audit_function_field_quantifiers() -> dict[str, object]:
    """Exact counterexamples to two tempting but invalid ideal encodings."""
    # The row [1,t] has the K(t)-kernel vector (-t,1), but a constant kernel
    # vector (a,b) would satisfy a+t*b=0 and hence a=b=0 coefficientwise.
    t = Fraction(5, 7)
    rational_kernel = (-t, Fraction(1))
    assert Fraction(1) * rational_kernel[0] + t * rational_kernel[1] == 0
    constant_kernel_dimension = 0

    # Put t=s-1 for a Laurent (torus) coordinate s.  Then
    # N(s)=span((s-1)e_1), g=e_1.  At the generic point
    # g=(1/(s-1))*((s-1)e_1), while at the allowed torus point s=1 the
    # nuisance generator vanishes and g survives.  Thus generic selector
    # failure does not mean failure at every fully supported contraction.
    generic_t = Fraction(3, 11)
    generic_multiplier = 1 / generic_t
    assert generic_multiplier * generic_t == 1
    special_nuisance_rank = 0
    special_augmented_rank = 1

    # Over any field, a projected vector v is nonzero exactly when some dual
    # vector a has a.v=1.  This is a valid projective normalization, but over
    # K(z) both v and a are rational functions; a scalar polynomial witness
    # at one z remains insufficient.
    projected = (Fraction(2), Fraction(-3))
    dual = (Fraction(1, 2), Fraction(0))
    assert sum(a * v for a, v in zip(dual, projected, strict=True)) == 1

    return {
        "function_field_kernel_example": "[1,t] * (-t,1)^T = 0",
        "constant_kernel_dimension": constant_kernel_dimension,
        "generic_selector_membership_example": (
            "e1=(1/(s-1))*((s-1)e1), but s=1 is a torus survival point"
        ),
        "radical_rank_profile_example": (
            "A=[(s-1)^2], g=s-1 fails pointwise everywhere although g is not "
            "in the polynomial column module"
        ),
        "special_t_zero_nuisance_rank": special_nuisance_rank,
        "special_t_zero_augmented_rank": special_augmented_rank,
        "conclusion": (
            "one-contraction kernels and generic selector membership are not "
            "equivalent to the required function-field/pointwise statements"
        ),
    }


def main() -> None:
    matchings_r3 = perfect_matchings(tuple(range(8)))
    matchings_r4 = perfect_matchings(tuple(range(10)))
    assert len(matchings_r3) == 105
    assert len(matchings_r4) == 945
    assert deck_module_dimension(5) == 495
    assert deck_module_dimension(6) == 2079
    assert companion_entry_terms(3, 2) == 162
    assert companion_entry_terms(3, 4) == 9
    assert companion_entry_terms(4, 2) == 1944
    assert companion_entry_terms(4, 4) == 108
    assert companion_entry_terms(4, 6) == 3

    coefficient_audit = {
        "r3_all_words_checked": audit_coefficient_formula(8, exhaustive=True),
        "r4_selected_words_checked": audit_coefficient_formula(10, exhaustive=False),
    }
    report = {
        "status": "equivalence_gate_stops_before_locus_elimination",
        "cases": [asdict(build_case(root_count)) for root_count in (3, 4)],
        "coefficient_encoder_audit": coefficient_audit,
        "quantifier_audit": audit_function_field_quantifiers(),
        "not_encoded": [
            "maximum-root nonexistence certificates for every (r+1)-set",
            "K(z)-rational sensor kernels with a proved polynomial degree bound",
            "for-all-torus-contractions selector failure including exceptional ranks",
            "a uniform r=3 legal target package entering the existing GLD chain",
            "GLD2 augmented-weight, alignment, response, and pure-anchor alternatives",
        ],
        "locus_classification": "not_determined",
        "global_conjecture": "UNRESOLVED",
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
