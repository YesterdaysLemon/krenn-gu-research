"""Pure support-cover helpers for the normalized P5 q5_311 slice."""

from __future__ import annotations

from krenn_gu import p5_pair_support_semantics as SEMANTICS


BRANCH = "q5_311"


def rare_mixed_colourings() -> tuple[tuple[int, ...], ...]:
    """Return the 160 mixed words whose mode-zero colour is rare."""
    return tuple(
        colours
        for colours in SEMANTICS.MIXED_COLOURINGS
        if colours[0] in (1, 2)
    )


def condition_closure(
    pool,
    closure: tuple[tuple[int, ...], ...],
) -> list[list[int]]:
    return [
        [-pool.id(SEMANTICS.entry_key(mode, source, colour))]
        for mode in SEMANTICS.MODES
        for source in SEMANTICS.SOURCES
        for colour in SEMANTICS.COLOURS
        if not closure[mode][source] & (1 << colour)
    ]


def general_chart_clause(
    pool,
    closure: tuple[tuple[int, ...], ...],
    pivots: tuple[tuple[int, int, int], ...],
) -> tuple[int, ...]:
    """Negate outside-zero and pivot-nonzero chart conditions."""
    pivot_set = set(pivots)
    literals = []
    for mode in SEMANTICS.MODES:
        for source in SEMANTICS.SOURCES:
            for colour in SEMANTICS.COLOURS:
                edge = mode, source, colour
                variable = pool.id(SEMANTICS.entry_key(*edge))
                if not closure[mode][source] & (1 << colour):
                    literals.append(variable)
                elif edge in pivot_set:
                    literals.append(-variable)
    clause = tuple(sorted(set(literals)))
    if len(clause) != len(literals):
        raise AssertionError("chart implication repeated a literal")
    return clause


__all__ = [
    "BRANCH",
    "condition_closure",
    "general_chart_clause",
    "rare_mixed_colourings",
]
