"""Deterministic global CNF for the P5 spanning-tree chart cover."""

from __future__ import annotations

import itertools

from pysat.formula import CNF, IDPool

import audit_p5_all_full_boundary_obstruction as ALL_FULL
import p5_pair_support_semantics as SEMANTICS


SHAPES = {
    "c10": ((0, 1), (1, 2), (2, 3), (3, 4), (0, 4)),
    "c4c6": ((0, 1), (0, 1), (2, 3), (3, 4), (2, 4)),
}


def shape_actions(
    shape: str,
) -> tuple[
    tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]],
    ...,
]:
    if shape not in SHAPES:
        raise ValueError(f"unknown shape: {shape}")
    return tuple(
        (modes, sources, colours)
        for modes, sources in ALL_FULL.automorphisms(
            ALL_FULL.full_edges(shape)
        )
        for colours in ALL_FULL.PERMUTATIONS_3
    )


def add_shape_signature_restrictions(
    cnf: CNF,
    pool: IDPool,
    allowed: tuple[tuple, ...],
    shape: str,
) -> int:
    before = len(cnf.clauses)
    for mode in SEMANTICS.MODES:
        required_noncoordinate = set(SHAPES[shape][mode])
        for pattern_index, signature in enumerate(allowed):
            observed_noncoordinate = {
                source
                for source, mask in enumerate(signature[0])
                if mask not in (1, 2, 4)
            }
            if observed_noncoordinate != required_noncoordinate:
                cnf.append(
                    [
                        -pool.id(
                            (
                                "local_pattern",
                                mode,
                                pattern_index,
                            )
                        )
                    ]
                )
    return len(cnf.clauses) - before


def add_coordinate_lex_leaders(
    cnf: CNF,
    pool: IDPool,
    shape: str,
) -> int:
    """Select the same canonical coordinate backbone as the census."""
    full = ALL_FULL.full_edges(shape)
    coordinate_cells = tuple(
        (mode, source)
        for mode in SEMANTICS.MODES
        for source in SEMANTICS.SOURCES
        if (mode, source) not in full
    )
    # A colour is encoded one-hot.  Reversing bit order makes its Boolean
    # lexicographic order agree with integer order 0 < 1 < 2.
    left = [
        pool.id(SEMANTICS.entry_key(mode, source, colour))
        for mode, source in coordinate_cells
        for colour in reversed(SEMANTICS.COLOURS)
    ]
    identity = (
        tuple(SEMANTICS.MODES),
        tuple(SEMANTICS.SOURCES),
        tuple(SEMANTICS.COLOURS),
    )
    count = 0
    for action in shape_actions(shape):
        if action == identity:
            continue
        modes, sources, colours = action
        right = [
            pool.id(
                SEMANTICS.entry_key(
                    modes[mode],
                    sources[source],
                    colours[colour],
                )
            )
            for mode, source in coordinate_cells
            for colour in reversed(SEMANTICS.COLOURS)
        ]
        SEMANTICS.add_lex_leq(
            cnf,
            pool,
            left,
            right,
            ("coordinate_backbone", shape, count),
        )
        count += 1
    return count


def coordinate_edges(
    supports: tuple[tuple[int, ...], ...],
) -> tuple[tuple[int, int, int], ...]:
    edges = tuple(
        (mode, source, mask.bit_length() - 1)
        for mode, row in enumerate(supports)
        for source, mask in enumerate(row)
        if mask in (1, 2, 4)
    )
    if len(edges) != 15:
        raise ValueError("coordinate backbone must have 15 singleton cells")
    return edges


def chart_clause(
    pool: IDPool,
    coordinate_entries: tuple[tuple[int, int, int], ...],
    connector_entries: tuple[tuple[int, int, int], ...],
) -> tuple[int, ...]:
    entries = coordinate_entries + connector_entries
    if len(entries) != len(set(entries)):
        raise ValueError("chart implication repeats an entry")
    return tuple(
        sorted(
            -pool.id(SEMANTICS.entry_key(*entry))
            for entry in entries
        )
    )


def build_cover_cnf(
    shape: str,
    chart_records: list[dict],
) -> tuple[CNF, IDPool, dict]:
    allowed = SEMANTICS.finite_field_local_signatures()
    cnf, pool = SEMANTICS.build_pair_support_cnf(allowed)
    base_variables = pool.top
    support_clauses = len(cnf.clauses)
    shape_clauses = add_shape_signature_restrictions(
        cnf,
        pool,
        allowed,
        shape,
    )
    shape_variables = pool.top
    shape_total_clauses = len(cnf.clauses)
    lex_leaders = add_coordinate_lex_leaders(cnf, pool, shape)

    clauses = set()
    for record in chart_records:
        if record.get("shape", shape) != shape:
            raise ValueError("chart shape mismatch")
        supports = tuple(
            tuple(row) for row in record["coordinate_supports"]
        )
        expected = coordinate_edges(supports)
        stored = tuple(
            tuple(edge) for edge in record["coordinate_entries"]
        )
        if expected != stored:
            raise ValueError("stored coordinate entries changed")
        connectors = tuple(
            tuple(edge) for edge in record["connector_entries"]
        )
        if any(
            supports[mode][source] != 7
            for mode, source, _colour in connectors
        ):
            raise ValueError("connector is not in a noncoordinate cell")
        clauses.add(chart_clause(pool, stored, connectors))
    cnf.extend([list(clause) for clause in sorted(clauses)])
    return cnf, pool, {
        "catalogue_signatures": len(allowed),
        "support_variables": base_variables,
        "support_clauses": support_clauses,
        "shape_variables": shape_variables,
        "shape_clauses_added": shape_clauses,
        "shape_total_clauses": shape_total_clauses,
        "coordinate_lex_leaders": lex_leaders,
        "chart_clauses": len(clauses),
        "final_variables": pool.top,
        "final_clauses": len(cnf.clauses),
    }
