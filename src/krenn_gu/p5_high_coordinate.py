"""Reusable P5 high-coordinate support, chart, and CEGAR primitives.

Operator checkpoint orchestration remains in tools.  This module exposes only
shared deterministic construction and bounded chart-checking operations.
"""

from __future__ import annotations

import ctypes
import hashlib
import itertools
import os
from pathlib import Path

from krenn_gu import p5_pair_support_semantics as SEMANTICS
from krenn_gu import p5_support_system as GENERATOR
from krenn_gu.p5_split_saturation import convert_text
from krenn_gu.singular_runtime import run_singular

BRANCH_BACKBONES = {
    # Zero denotes the unique noncoordinate cell in the normalized row.
    "q4_211": (0, 1, 1, 2, 4),
    "q5_311": (1, 1, 1, 2, 4),
    "q5_221": (1, 1, 2, 2, 4),
}

def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def available_memory_percent() -> float:
    if os.name != "nt":
        values = {}
        for line in Path("/proc/meminfo").read_text(
            encoding="utf-8"
        ).splitlines():
            key, raw_value = line.split(":", 1)
            values[key] = int(raw_value.strip().split()[0])
        return 100.0 * values["MemAvailable"] / values["MemTotal"]

    class MemoryStatus(ctypes.Structure):
        _fields_ = [
            ("length", ctypes.c_ulong),
            ("memory_load", ctypes.c_ulong),
            ("total_physical", ctypes.c_ulonglong),
            ("available_physical", ctypes.c_ulonglong),
            ("total_page_file", ctypes.c_ulonglong),
            ("available_page_file", ctypes.c_ulonglong),
            ("total_virtual", ctypes.c_ulonglong),
            ("available_virtual", ctypes.c_ulonglong),
            ("available_extended_virtual", ctypes.c_ulonglong),
        ]

    status = MemoryStatus()
    status.length = ctypes.sizeof(status)
    if not ctypes.windll.kernel32.GlobalMemoryStatusEx(
        ctypes.byref(status)
    ):
        raise OSError("GlobalMemoryStatusEx failed")
    return (
        100.0
        * status.available_physical
        / status.total_physical
    )

def transform_backbone(
    backbone: tuple[int, ...],
    sources: tuple[int, ...],
    colours: tuple[int, ...],
) -> tuple[int, ...]:
    transformed = [0] * len(backbone)
    for old_source, mask in enumerate(backbone):
        if mask == 0:
            new_mask = 0
        else:
            old_colour = mask.bit_length() - 1
            new_mask = 1 << colours[old_colour]
        transformed[sources[old_source]] = new_mask
    return tuple(transformed)

def source_colour_stabilizer(
    branch: str,
) -> tuple[tuple[tuple[int, ...], tuple[int, ...]], ...]:
    backbone = BRANCH_BACKBONES[branch]
    actions = tuple(
        (sources, colours)
        for sources in itertools.permutations(SEMANTICS.SOURCES)
        for colours in itertools.permutations(SEMANTICS.COLOURS)
        if transform_backbone(backbone, sources, colours) == backbone
    )
    expected = {
        "q4_211": 4,
        "q5_311": 12,
        "q5_221": 8,
    }[branch]
    if len(actions) != expected:
        raise AssertionError(
            f"{branch} stabilizer changed: {len(actions)} != {expected}"
        )
    return actions

def branch_signature_indices(
    allowed: tuple[tuple, ...],
    branch: str,
) -> tuple[int, ...]:
    backbone = BRANCH_BACKBONES[branch]
    indices = []
    for index, signature in enumerate(allowed):
        support = signature[0]
        observed = tuple(
            mask if mask in (1, 2, 4) else 0
            for mask in support
        )
        if observed == backbone:
            indices.append(index)
    if not indices:
        raise AssertionError(f"{branch} has no local signature witnesses")
    return tuple(indices)

def coordinate_type(support: tuple[int, ...]) -> str:
    colours = [
        mask.bit_length() - 1
        for mask in support
        if mask in (1, 2, 4)
    ]
    multiplicities = tuple(
        sorted(
            (
                colours.count(colour)
                for colour in SEMANTICS.COLOURS
                if colour in colours
            ),
            reverse=True,
        )
    )
    if len(colours) == 5 and multiplicities == (3, 1, 1):
        return "q5_311"
    if len(colours) == 5 and multiplicities == (2, 2, 1):
        return "q5_221"
    if len(colours) == 4 and multiplicities == (2, 1, 1):
        return "q4_211"
    return "other"

def add_branch_restriction(
    cnf,
    pool,
    allowed: tuple[tuple, ...],
    branch: str,
) -> dict:
    indices = branch_signature_indices(allowed, branch)
    cnf.append(
        [
            pool.id(("local_pattern", 0, pattern_index))
            for pattern_index in indices
        ]
    )
    forbidden_types = {
        # Branches are a disjoint priority partition:
        # q5_221 exists; else q5_311 exists; else maximum q is four.
        "q5_221": (),
        "q5_311": ("q5_221",),
        "q4_211": ("q5_221", "q5_311"),
    }[branch]
    forbidden_clauses = 0
    for mode in SEMANTICS.MODES[1:]:
        for pattern_index, signature in enumerate(allowed):
            if coordinate_type(signature[0]) in forbidden_types:
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
                forbidden_clauses += 1
    return {
        "normalized_mode_zero_signatures": len(indices),
        "forbidden_coordinate_types": forbidden_types,
        "forbidden_local_pattern_clauses": forbidden_clauses,
    }

def add_stabilizer_lex_leaders(
    cnf,
    pool,
    branch: str,
) -> int:
    """Canonicalize the coordinate backbone after normalizing mode zero."""
    mode_actions = tuple(
        (0,) + permutation
        for permutation in itertools.permutations((1, 2, 3, 4))
    )
    source_colour_actions = source_colour_stabilizer(branch)
    left = [
        pool.id(("singleton", mode, source, colour))
        for mode in SEMANTICS.MODES
        for source in SEMANTICS.SOURCES
        for colour in reversed(SEMANTICS.COLOURS)
    ]
    identity = (
        tuple(SEMANTICS.MODES),
        tuple(SEMANTICS.SOURCES),
        tuple(SEMANTICS.COLOURS),
    )
    count = 0
    for modes in mode_actions:
        for sources, colours in source_colour_actions:
            if (modes, sources, colours) == identity:
                continue
            right = [
                pool.id(
                    (
                        "singleton",
                        modes[mode],
                        sources[source],
                        colours[colour],
                    )
                )
                for mode in SEMANTICS.MODES
                for source in SEMANTICS.SOURCES
                for colour in reversed(SEMANTICS.COLOURS)
            ]
            SEMANTICS.add_lex_leq(
                cnf,
                pool,
                left,
                right,
                ("high_coordinate", branch, count),
            )
            count += 1
    expected = 24 * len(source_colour_actions) - 1
    if count != expected:
        raise AssertionError("stabilizer lex-leader count changed")
    return count

def selected_signature_indices(
    pool,
    model: list[int],
    allowed: tuple[tuple, ...],
) -> tuple[int, ...]:
    positive = {literal for literal in model if literal > 0}
    return tuple(
        next(
            pattern_index
            for pattern_index in range(len(allowed))
            if pool.id(("local_pattern", mode, pattern_index))
            in positive
        )
        for mode in SEMANTICS.MODES
    )

def closure_supports(
    supports: tuple[tuple[int, ...], ...],
) -> tuple[tuple[int, ...], ...]:
    return tuple(
        tuple(
            mask if mask in (0, 1, 2, 4) else 7
            for mask in row
        )
        for row in supports
    )

def support_edges(
    supports: tuple[tuple[int, ...], ...],
) -> tuple[tuple[int, int, int], ...]:
    return tuple(
        (mode, source, colour)
        for mode in SEMANTICS.MODES
        for source in SEMANTICS.SOURCES
        for colour in SEMANTICS.COLOURS
        if supports[mode][source] & (1 << colour)
    )

def gauge_tree(
    supports: tuple[tuple[int, ...], ...],
    preferred_supports: tuple[tuple[int, ...], ...] | None = None,
) -> tuple[tuple[int, int, int], ...]:
    preferred = supports if preferred_supports is None else preferred_supports
    nodes = [
        *(("r", source) for source in SEMANTICS.SOURCES),
        *(
            ("c", mode, colour)
            for mode in SEMANTICS.MODES
            for colour in SEMANTICS.COLOURS
        ),
    ]
    union_find = GENERATOR.UnionFind(nodes)
    edges = support_edges(supports)
    ordered = tuple(
        edge
        for edge in edges
        if (
            preferred[edge[0]][edge[1]] in (1, 2, 4)
            and preferred[edge[0]][edge[1]]
            & (1 << edge[2])
        )
    ) + tuple(
        edge
        for edge in edges
        if not (
            preferred[edge[0]][edge[1]] in (1, 2, 4)
            and preferred[edge[0]][edge[1]]
            & (1 << edge[2])
        )
    )
    tree = []
    for mode, source, colour in ordered:
        if union_find.union(
            ("r", source),
            ("c", mode, colour),
        ):
            tree.append((mode, source, colour))
    return tuple(tree)

def gauge_tree_variants(
    supports: tuple[tuple[int, ...], ...],
    preferred_supports: tuple[tuple[int, ...], ...],
    alternatives: int,
) -> tuple[tuple[tuple[int, int, int], ...], ...]:
    """Return deterministic maximal-forest gauge alternatives."""
    if alternatives < 0:
        raise ValueError("gauge-tree alternative count is negative")
    nodes = [
        *(("r", source) for source in SEMANTICS.SOURCES),
        *(
            ("c", mode, colour)
            for mode in SEMANTICS.MODES
            for colour in SEMANTICS.COLOURS
        ),
    ]
    edges = support_edges(supports)
    variants = [gauge_tree(supports, preferred_supports)]
    seen = {variants[0]}
    for seed in range(alternatives):
        ordered = sorted(
            edges,
            key=lambda edge: hashlib.sha256(
                (
                    f"{seed}:"
                    f"{edge[0]},{edge[1]},{edge[2]}"
                ).encode("ascii")
            ).digest(),
        )
        union_find = GENERATOR.UnionFind(nodes)
        forest = []
        for mode, source, colour in ordered:
            if union_find.union(
                ("r", source),
                ("c", mode, colour),
            ):
                forest.append((mode, source, colour))
        candidate = tuple(forest)
        if candidate not in seen:
            variants.append(candidate)
            seen.add(candidate)
    return tuple(variants)

def chart_clause(
    pool,
    closure: tuple[tuple[int, ...], ...],
    tree: tuple[tuple[int, int, int], ...],
    branch: str | None,
) -> tuple[int, ...]:
    """Negate the exact applicability conditions of a gauge chart.

    A free coefficient permitted by ``closure`` may vanish: pure-only
    saturation does not require it to be nonzero.  Thus the antecedent
    only forbids entries outside the closure and requires the gauge
    pivots.  For a singleton cell whose sole entry is a pivot, the
    existing singleton auxiliary variable compactly expresses both.
    """
    literals = []
    tree_set = set(tree)
    for mode in SEMANTICS.MODES:
        for source in SEMANTICS.SOURCES:
            mask = closure[mode][source]
            branch_fixed_singleton = (
                branch is not None
                and mode == 0
                and BRANCH_BACKBONES[branch][source]
                in (1, 2, 4)
            )
            if branch_fixed_singleton:
                # The branch restriction already supplies both presence
                # and absence conditions for this normalized cell.
                continue
            if mask == 0:
                literals.extend(
                    pool.id(
                        SEMANTICS.entry_key(
                            mode,
                            source,
                            colour,
                        )
                    )
                    for colour in SEMANTICS.COLOURS
                )
            elif mask in (1, 2, 4):
                colour = mask.bit_length() - 1
                pivot = (mode, source, colour)
                if pivot in tree_set:
                    literals.append(
                        -pool.id(
                            ("singleton", mode, source, colour)
                        )
                    )
                else:
                    literals.extend(
                        pool.id(
                            SEMANTICS.entry_key(
                                mode,
                                source,
                                other_colour,
                            )
                        )
                        for other_colour in SEMANTICS.COLOURS
                        if other_colour != colour
                    )
            else:
                literals.extend(
                    -pool.id(SEMANTICS.entry_key(*edge))
                    for edge in tree
                    if edge[0] == mode and edge[1] == source
                )
    clause = tuple(sorted(set(literals)))
    if len(clause) != len(literals):
        raise AssertionError("chart implication repeated a literal")
    return clause

def certify_chart(
    closure: tuple[tuple[int, ...], ...],
    indices: tuple[int, ...],
    tree: tuple[tuple[int, int, int], ...],
    timeout: float,
    try_split: bool = True,
    prefer_split: bool = False,
    split_only: bool = False,
) -> dict:
    program, metadata = GENERATOR.generate(
        closure,
        indices,
        expected_partial_cells=0,
        pure_saturation_only=True,
        gauge_tree_edges=tree,
        allow_arbitrary_support=True,
    )
    split_program = None
    if try_split and prefer_split:
        split_program = convert_text(program)
        split = run_singular(split_program, timeout)
        if split["status"] == "UNIT_IDEAL":
            return {
                "status": "UNIT_IDEAL",
                "method": "split",
                "source_sha256": sha256_text(program),
                "split_source_sha256": sha256_text(split_program),
                "metadata": metadata,
                "cas": split,
            }
        if split_only:
            return {
                "status": "INCONCLUSIVE",
                "source_sha256": sha256_text(program),
                "split_source_sha256": sha256_text(split_program),
                "metadata": metadata,
                "split_cas": split,
            }
    elif split_only:
        raise ValueError("split-only certification requires prefer_split")
    direct = run_singular(program, timeout)
    if direct["status"] == "UNIT_IDEAL":
        return {
            "status": "UNIT_IDEAL",
            "method": "direct",
            "source_sha256": sha256_text(program),
            "metadata": metadata,
            "cas": direct,
        }
    if not try_split:
        return {
            "status": "INCONCLUSIVE",
            "source_sha256": sha256_text(program),
            "metadata": metadata,
            "direct_cas": direct,
        }
    if split_program is None:
        split_program = convert_text(program)
        split = run_singular(split_program, timeout)
    if split["status"] == "UNIT_IDEAL":
        return {
            "status": "UNIT_IDEAL",
            "method": "split",
            "source_sha256": sha256_text(program),
            "split_source_sha256": sha256_text(split_program),
            "metadata": metadata,
            "direct_cas": direct,
            "cas": split,
        }
    return {
        "status": "INCONCLUSIVE",
        "source_sha256": sha256_text(program),
        "split_source_sha256": sha256_text(split_program),
        "metadata": metadata,
        "direct_cas": direct,
        "split_cas": split,
    }

def transform_mask(
    mask: int,
    colours: tuple[int, ...],
) -> int:
    return sum(
        1 << colours[colour]
        for colour in SEMANTICS.COLOURS
        if mask & (1 << colour)
    )

def transform_support_array(
    supports: tuple[tuple[int, ...], ...],
    modes: tuple[int, ...],
    sources: tuple[int, ...],
    colours: tuple[int, ...],
) -> tuple[tuple[int, ...], ...]:
    transformed = [
        [0 for _source in SEMANTICS.SOURCES]
        for _mode in SEMANTICS.MODES
    ]
    for old_mode in SEMANTICS.MODES:
        for old_source in SEMANTICS.SOURCES:
            transformed[modes[old_mode]][sources[old_source]] = (
                transform_mask(
                    supports[old_mode][old_source],
                    colours,
                )
            )
    return tuple(tuple(row) for row in transformed)

def chart_symmetry_orbit_clauses(
    closure: tuple[tuple[int, ...], ...],
    tree: tuple[tuple[int, int, int], ...],
    branch: str,
    pool,
) -> tuple[tuple[int, ...], ...]:
    """Transport one exact chart through all branch symmetries."""
    clauses = set()
    for modes in (
        (0,) + permutation
        for permutation in itertools.permutations((1, 2, 3, 4))
    ):
        for sources, colours in source_colour_stabilizer(branch):
            transformed_closure = transform_support_array(
                closure,
                modes,
                sources,
                colours,
            )
            transformed_tree = tuple(
                (
                    modes[mode],
                    sources[source],
                    colours[colour],
                )
                for mode, source, colour in tree
            )
            clauses.add(
                chart_clause(
                    pool,
                    transformed_closure,
                    transformed_tree,
                    branch,
                )
            )
    return tuple(sorted(clauses))


def normalized_supports(value) -> tuple[tuple[int, ...], ...]:
    supports = tuple(tuple(int(mask) for mask in row) for row in value)
    if len(supports) != 5 or any(len(row) != 5 for row in supports):
        raise ValueError("support array is not 5 by 5")
    return supports


def normalized_tree(value) -> tuple[tuple[int, int, int], ...]:
    return tuple(tuple(map(int, edge)) for edge in value)


def validate_forest(
    supports: tuple[tuple[int, ...], ...],
    closure: tuple[tuple[int, ...], ...],
    tree: tuple[tuple[int, int, int], ...],
) -> tuple[int, int]:
    if any(
        actual & ~allowed
        for actual_row, closure_row in zip(
            supports, closure, strict=True
        )
        for actual, allowed in zip(
            actual_row, closure_row, strict=True
        )
    ):
        raise AssertionError("actual support is not inside its closure")
    if any(
        mask not in (0, 1, 2, 4, 7)
        for row in closure
        for mask in row
    ):
        raise AssertionError("closure uses an unsupported mask")

    nodes = [
        *(("r", source) for source in SEMANTICS.SOURCES),
        *(("c", mode, colour)
          for mode in SEMANTICS.MODES
          for colour in SEMANTICS.COLOURS),
    ]

    def components(
        edges: tuple[tuple[int, int, int], ...],
        reject_cycle: bool,
    ) -> int:
        parent = {node: node for node in nodes}

        def find(node):
            while parent[node] != node:
                parent[node] = parent[parent[node]]
                node = parent[node]
            return node

        for mode, source, colour in edges:
            if (
                mode not in SEMANTICS.MODES
                or source not in SEMANTICS.SOURCES
                or colour not in SEMANTICS.COLOURS
                or not supports[mode][source] & (1 << colour)
            ):
                raise AssertionError(
                    "forest edge is absent from the actual support"
                )
            left = find(("r", source))
            right = find(("c", mode, colour))
            if left == right:
                if reject_cycle:
                    raise AssertionError("gauge forest contains a cycle")
                continue
            parent[left] = right
        return len({find(node) for node in nodes})

    actual_edges = support_edges(supports)
    actual_components = components(actual_edges, False)
    forest_components = components(tree, True)
    if len(tree) != len(nodes) - forest_components:
        raise AssertionError(
            "gauge forest edge/component count is inconsistent"
        )
    if forest_components < actual_components:
        raise AssertionError(
            "gauge forest connects distinct actual-support components"
        )
    return actual_components, forest_components


__all__ = [
    "BRANCH_BACKBONES",
    "add_branch_restriction",
    "add_stabilizer_lex_leaders",
    "available_memory_percent",
    "branch_signature_indices",
    "certify_chart",
    "chart_clause",
    "chart_symmetry_orbit_clauses",
    "closure_supports",
    "coordinate_type",
    "gauge_tree",
    "gauge_tree_variants",
    "normalized_supports",
    "normalized_tree",
    "run_singular",
    "selected_signature_indices",
    "sha256_text",
    "source_colour_stabilizer",
    "support_edges",
    "transform_backbone",
    "transform_mask",
    "transform_support_array",
    "validate_forest",
]
