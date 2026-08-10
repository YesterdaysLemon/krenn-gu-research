"""Exact Boolean support semantics for the P5 pair-signature boundary.

The 6,495 local signatures are covered over C by
``P5_PAIR_SIGNATURE_CATALOGUE_COVERAGE.md``.  This module combines five
selected signatures with the global pair quota, the three supported
pure permanents, and the necessary condition that no mixed permanent
coefficient has exactly one supported monomial.
"""

from __future__ import annotations

import itertools

from pysat.card import CardEnc, EncType
from pysat.formula import CNF, IDPool

from krenn_gu.p5_pair_catalogue import finite_field_local_signatures


MODES = tuple(range(5))
SOURCES = tuple(range(5))
COLOURS = tuple(range(3))
PERMUTATIONS = tuple(itertools.permutations(SOURCES))
MIXED_COLOURINGS = tuple(
    colours
    for colours in itertools.product(COLOURS, repeat=5)
    if len(set(colours)) > 1
)


def entry_key(mode: int, source: int, colour: int) -> tuple:
    return ("x", mode, source, colour)


def add_and_equivalence(
    cnf: CNF,
    output: int,
    factors: list[int],
) -> None:
    for factor in factors:
        cnf.append([-output, factor])
    cnf.append([output] + [-factor for factor in factors])


def add_lex_leq(
    cnf: CNF,
    pool: IDPool,
    left: list[int],
    right: list[int],
    label: tuple,
) -> None:
    """Encode the exact Boolean lexicographic constraint left <= right."""
    if len(left) != len(right):
        raise ValueError("lexicographic vectors have different lengths")
    prefix = pool.id(("lex_prefix", *label, 0))
    cnf.append([prefix])
    for index, (left_bit, right_bit) in enumerate(
        zip(left, right, strict=True)
    ):
        cnf.append([-prefix, -left_bit, right_bit])
        equal = pool.id(("lex_equal", *label, index))
        cnf.extend(
            [
                [-equal, -left_bit, right_bit],
                [-equal, left_bit, -right_bit],
                [equal, left_bit, right_bit],
                [equal, -left_bit, -right_bit],
            ]
        )
        next_prefix = pool.id(("lex_prefix", *label, index + 1))
        cnf.extend(
            [
                [-next_prefix, prefix],
                [-next_prefix, equal],
                [next_prefix, -prefix, -equal],
            ]
        )
        prefix = next_prefix


def build_pair_support_cnf(
    allowed_local_signatures: tuple[tuple, ...] | None = None,
    mixed_colourings: tuple[tuple[int, ...], ...] | None = None,
) -> tuple[CNF, IDPool]:
    """Build the deterministic pair-signature support CNF.

    Variable allocation and clause order are deliberately stable because
    packaged DRAT traces bind to the exact DIMACS bytes.
    """
    allowed = (
        finite_field_local_signatures()
        if allowed_local_signatures is None
        else allowed_local_signatures
    )
    retained_mixed_colourings = (
        MIXED_COLOURINGS
        if mixed_colourings is None
        else mixed_colourings
    )
    if (
        len(set(retained_mixed_colourings))
        != len(retained_mixed_colourings)
        or any(
            colours not in MIXED_COLOURINGS
            for colours in retained_mixed_colourings
        )
    ):
        raise ValueError("retained mixed colourings are invalid")
    if len(allowed) != 6495:
        raise ValueError("expected the covered 6,495-signature catalogue")

    pool = IDPool()
    cnf = CNF()

    # Every source row exposes each target coordinate in one local map.
    for source in SOURCES:
        for colour in COLOURS:
            singletons = []
            for mode in MODES:
                singleton = pool.id(
                    ("singleton", mode, source, colour)
                )
                selected = pool.id(entry_key(mode, source, colour))
                others = [
                    pool.id(entry_key(mode, source, other_colour))
                    for other_colour in COLOURS
                    if other_colour != colour
                ]
                cnf.append([-singleton, selected])
                for other in others:
                    cnf.append([-singleton, -other])
                cnf.append([singleton, -selected, *others])
                singletons.append(singleton)
            cnf.append(singletons)

    # Structural rank three is necessary for each local map.
    injections = tuple(itertools.permutations(SOURCES, 3))
    for mode in MODES:
        witnesses = []
        for injection in injections:
            witness = pool.id(("local_rank", mode, injection))
            factors = [
                pool.id(
                    entry_key(mode, injection[colour], colour)
                )
                for colour in COLOURS
            ]
            add_and_equivalence(cnf, witness, factors)
            witnesses.append(witness)
        cnf.append(witnesses)

    local_pattern_variables: list[list[int]] = []
    for mode in MODES:
        witnesses = []
        for pattern_index, signature in enumerate(allowed):
            support = signature[0]
            witness = pool.id(
                ("local_pattern", mode, pattern_index)
            )
            witnesses.append(witness)
            for source in SOURCES:
                for colour in COLOURS:
                    entry = pool.id(entry_key(mode, source, colour))
                    cnf.append(
                        [-witness, entry]
                        if support[source] & (1 << colour)
                        else [-witness, -entry]
                    )
        cnf.append(witnesses)
        local_pattern_variables.append(witnesses)
        cnf.extend(
            CardEnc.atmost(
                witnesses,
                bound=1,
                vpool=pool,
                encoding=EncType.seqcounter,
            ).clauses
        )

    # Pair level of the complex kernel-Hall hierarchy.
    source_pairs = tuple(itertools.combinations(SOURCES, 2))
    for pair_index, _pair in enumerate(source_pairs):
        for colour in COLOURS:
            containing_modes = []
            for mode in MODES:
                incidence = pool.id(
                    (
                        "hierarchy_incidence",
                        mode,
                        pair_index,
                        colour,
                    )
                )
                supporting_patterns = [
                    local_pattern_variables[mode][pattern_index]
                    for pattern_index, signature in enumerate(allowed)
                    if signature[1][pair_index] & (1 << colour)
                ]
                for witness in supporting_patterns:
                    cnf.append([-witness, incidence])
                cnf.append([-incidence, *supporting_patterns])
                containing_modes.append(incidence)
            cnf.extend(
                CardEnc.atleast(
                    containing_modes,
                    bound=2,
                    vpool=pool,
                    encoding=EncType.seqcounter,
                ).clauses
            )

    # Each of the three pure target coefficients is nonzero, hence has a
    # supported perfect-matching monomial.
    for colour in COLOURS:
        witnesses = []
        for permutation in PERMUTATIONS:
            witness = pool.id(("pure", colour, permutation))
            add_and_equivalence(
                cnf,
                witness,
                [
                    pool.id(
                        entry_key(
                            mode,
                            permutation[mode],
                            colour,
                        )
                    )
                    for mode in MODES
                ],
            )
            witnesses.append(witness)
        cnf.append(witnesses)

    # A zero mixed coefficient cannot have exactly one supported monomial.
    for colours in retained_mixed_colourings:
        witnesses = []
        for permutation in PERMUTATIONS:
            witness = pool.id(("mixed", colours, permutation))
            add_and_equivalence(
                cnf,
                witness,
                [
                    pool.id(
                        entry_key(
                            mode,
                            permutation[mode],
                            colours[mode],
                        )
                    )
                    for mode in MODES
                ],
            )
            witnesses.append(witness)
        for index, witness in enumerate(witnesses):
            cnf.append(
                [-witness]
                + witnesses[:index]
                + witnesses[index + 1 :]
            )
    return cnf, pool


def supports_from_model(
    pool: IDPool,
    model: list[int],
) -> tuple[tuple[int, ...], ...]:
    positive = {literal for literal in model if literal > 0}
    return tuple(
        tuple(
            sum(
                (
                    pool.id(entry_key(mode, source, colour))
                    in positive
                )
                << colour
                for colour in COLOURS
            )
            for source in SOURCES
        )
        for mode in MODES
    )
