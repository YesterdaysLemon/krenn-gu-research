#!/usr/bin/env python3
"""Search the three normalized high-coordinate P5 tree-chart branches."""

from __future__ import annotations

import argparse
import ctypes
import hashlib
import itertools
import json
import os
import subprocess
import time
from pathlib import Path

from pysat.solvers import Solver

import generate_p5_one_partial_support_system as GENERATOR
from generate_p5_split_saturation_system import convert_text
import p5_pair_support_semantics as SEMANTICS


ROOT = Path(__file__).resolve().parent
SINGULAR_COMMAND = (
    "wsl.exe",
    "--exec",
    "/usr/bin/Singular",
    "-q",
)
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


def certify_gauge_tree_portfolio(
    supports: tuple[tuple[int, ...], ...],
    closure: tuple[tuple[int, ...], ...],
    indices: tuple[int, ...],
    alternatives: int,
    timeout: float,
) -> tuple[
    tuple[tuple[int, int, int], ...],
    dict | None,
    dict,
]:
    """Try short exact direct certificates across gauge forests."""
    variants = gauge_tree_variants(
        supports,
        closure,
        alternatives,
    )
    original = variants[0]
    scored = []
    for tree in variants:
        _program, metadata = GENERATOR.generate(
            closure,
            indices,
            expected_partial_cells=0,
            pure_saturation_only=True,
            gauge_tree_edges=tree,
            allow_arbitrary_support=True,
        )
        scored.append(
            (
                metadata["mixed_equations"],
                tree != original,
                tree,
            )
        )
    # Prefer fewer distinct equations, retaining the historical tree
    # first on a tie.
    ordered = tuple(tree for _count, _alternate, tree in sorted(scored))
    trials = []
    for tree in ordered:
        certificate = certify_chart(
            closure,
            indices,
            tree,
            timeout,
            try_split=False,
        )
        cas = (
            certificate.get("cas")
            or certificate.get("direct_cas")
            or {}
        )
        trials.append(
            {
                "tree": tree,
                "mixed_equations": certificate["metadata"][
                    "mixed_equations"
                ],
                "status": certificate["status"],
                "seconds": cas.get("elapsed_seconds"),
            }
        )
        if certificate["status"] == "UNIT_IDEAL":
            return tree, certificate, {
                "strategy": "deterministic-min-equations-v1",
                "alternative_count": alternatives,
                "trial_timeout_seconds": timeout,
                "trials": trials,
                "selected_tree": tree,
            }
    return original, None, {
        "strategy": "deterministic-min-equations-v1",
        "alternative_count": alternatives,
        "trial_timeout_seconds": timeout,
        "trials": trials,
        "selected_tree": None,
    }


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


def singular_command_with_timeout(
    timeout: float,
) -> tuple[str, ...]:
    if timeout <= 0:
        raise ValueError("Singular timeout must be positive")
    if os.name != "nt":
        return SINGULAR_COMMAND
    # Put the deadline around Singular inside WSL.  Killing only the
    # Windows wsl.exe wrapper can leave its Linux child holding the
    # captured pipes for several extra seconds.
    return (
        "wsl.exe",
        "--exec",
        "/usr/bin/timeout",
        "--signal=KILL",
        f"{timeout:.6f}s",
        "/usr/bin/Singular",
        "-q",
    )


def run_singular(program: str, timeout: float) -> dict:
    started = time.monotonic()
    infrastructure_attempts = []
    for attempt in range(3):
        try:
            completed = subprocess.run(
                singular_command_with_timeout(timeout),
                input=program,
                text=True,
                encoding="utf-8",
                errors="replace",
                capture_output=True,
                timeout=timeout + 5,
                check=False,
            )
        except subprocess.TimeoutExpired:
            return {
                "status": "TIMEOUT",
                "elapsed_seconds": round(
                    time.monotonic() - started, 6
                ),
                "infrastructure_attempts": infrastructure_attempts,
            }
        output = completed.stdout + completed.stderr
        normalized_output = output.replace("\x00", "")
        infrastructure_attempts.append(
            {
                "returncode": completed.returncode,
                "wsl_service_unexpected": (
                    "WSL/Service/E_UNEXPECTED"
                    in normalized_output
                ),
            }
        )
        if (
            os.name != "nt"
            or "WSL/Service/E_UNEXPECTED"
            not in normalized_output
            or attempt == 2
        ):
            break
        # A killed WSL client can briefly leave the service unable to
        # accept the next launch.  Retry only this explicit transport
        # failure; algebraic timeouts and CAS output remain fail-closed.
        time.sleep(1.5 * (attempt + 1))
    status = (
        "UNIT_IDEAL"
        if "UNIT_IDEAL" in output
        else "SURVIVOR"
        if "SURVIVOR" in output
        else "ERROR"
    )
    return {
        "status": status,
        "returncode": completed.returncode,
        "elapsed_seconds": round(time.monotonic() - started, 6),
        "output_tail": output[-2000:],
        "infrastructure_attempts": infrastructure_attempts,
    }


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


def relax_chart_closure(
    supports: tuple[tuple[int, ...], ...],
    indices: tuple[int, ...],
    initial_closure: tuple[tuple[int, ...], ...],
    timeout: int,
    min_available_percent: float,
    recursive: bool = True,
    prefer_split: bool = False,
) -> tuple[
    tuple[tuple[int, ...], ...],
    tuple[tuple[int, int, int], ...],
    dict,
]:
    """Greedily enlarge a chart by recursive row-wise group trials."""
    current = [list(row) for row in initial_closure]
    trials = []
    accepted = []
    paused_for_memory = False

    def attempt(cells: tuple[tuple[int, int], ...]) -> None:
        nonlocal current, paused_for_memory
        if not cells or paused_for_memory:
            return
        available = available_memory_percent()
        if available < min_available_percent:
            paused_for_memory = True
            return
        proposed = [row[:] for row in current]
        for mode, source in cells:
            proposed[mode][source] = 7
        proposed_closure = tuple(tuple(row) for row in proposed)
        proposed_tree = gauge_tree(supports, proposed_closure)
        certificate = certify_chart(
            proposed_closure,
            indices,
            proposed_tree,
            timeout,
            try_split=prefer_split,
            prefer_split=prefer_split,
        )
        trial = {
            "cells": cells,
            "status": certificate["status"],
            "direct_cas": (
                certificate.get("cas")
                or certificate.get("direct_cas")
            ),
        }
        trials.append(trial)
        if certificate["status"] == "UNIT_IDEAL":
            current = proposed
            accepted.extend(cells)
            return
        if len(cells) == 1 or not recursive:
            return
        midpoint = len(cells) // 2
        attempt(cells[:midpoint])
        attempt(cells[midpoint:])

    # Mode zero is fixed by branch normalization.  Enlarging it adds
    # algebraic difficulty without increasing coverage inside the branch.
    for mode in SEMANTICS.MODES[1:]:
        attempt(
            tuple(
                (mode, source)
                for source in SEMANTICS.SOURCES
                if current[mode][source] in (1, 2, 4)
            )
        )

    closure = tuple(tuple(row) for row in current)
    tree = gauge_tree(supports, closure)
    return closure, tree, {
        "strategy": (
            "recursive-row-greedy-v1"
            if recursive
            else "whole-row-greedy-v1"
        ),
        "trial_timeout_seconds": timeout,
        "trials": trials,
        "accepted_cells": tuple(accepted),
        "paused_for_memory": paused_for_memory,
    }


def checkpoint(
    path: Path | None,
    branch: str,
    metadata: dict,
    records: list[dict],
    status: str,
) -> None:
    if path is None:
        return
    payload = {
        "status": status,
        "branch": branch,
        "metadata": metadata,
        "records": records,
    }
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    # OneDrive and virus scanners can momentarily open the destination
    # without delete sharing on Windows.  Preserve the atomic replace
    # contract, but tolerate that transient lock instead of losing the
    # completed checkpoint batch.
    for attempt in range(50):
        try:
            os.replace(temporary, path)
            break
        except PermissionError:
            if os.name != "nt" or attempt == 49:
                raise
            time.sleep(0.1)


def transformed_seed_clauses(
    paths: list[Path],
    branch: str,
    pool,
) -> tuple[tuple[tuple[int, ...], ...], list[dict]]:
    """Upgrade prior pure-only chart records to exact applicability."""
    clauses = []
    sources = []
    for path in paths:
        raw = path.read_bytes()
        state = json.loads(raw)
        if state.get("branch") != branch:
            raise ValueError(f"seed branch mismatch: {path}")
        records = state.get("records", [])
        for index, record in enumerate(records):
            certificate = record.get("certificate", {})
            certificate_metadata = certificate.get("metadata", {})
            if (
                certificate.get("status") != "UNIT_IDEAL"
                or certificate_metadata.get(
                    "saturated_parameters"
                )
                != 0
            ):
                raise ValueError(
                    "seed chart is not a pure-only unit ideal: "
                    f"{path} record {index}"
                )
            closure = tuple(
                tuple(row) for row in record["closure_supports"]
            )
            tree = tuple(
                tuple(edge) for edge in record["gauge_tree"]
            )
            clauses.append(
                chart_clause(pool, closure, tree, branch)
            )
        sources.append(
            {
                "path": path.as_posix(),
                "sha256": hashlib.sha256(raw).hexdigest(),
                "status": state.get("status"),
                "records": len(records),
            }
        )
    return tuple(sorted(set(clauses))), sources


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


def chart_orbit_seed_clauses(
    paths: list[Path],
    branch: str,
    pool,
) -> tuple[tuple[tuple[int, ...], ...], list[dict]]:
    """Transport every exact pure-only chart in prior ledgers."""
    clauses = set()
    sources_metadata = []
    for path in paths:
        raw = path.read_bytes()
        state = json.loads(raw)
        if state.get("branch") != branch:
            raise ValueError(f"chart-orbit seed branch mismatch: {path}")
        records = state.get("records", [])
        source_clauses = set()
        for index, record in enumerate(records):
            certificate = record.get("certificate", {})
            if (
                certificate.get("status") != "UNIT_IDEAL"
                or certificate.get("metadata", {}).get(
                    "saturated_parameters"
                )
                != 0
            ):
                raise ValueError(
                    "chart-orbit seed is not a pure-only unit ideal: "
                    f"{path} record {index}"
                )
            closure = tuple(
                tuple(map(int, row))
                for row in record["closure_supports"]
            )
            tree = tuple(
                tuple(map(int, edge))
                for edge in record["gauge_tree"]
            )
            source_clauses.update(
                chart_symmetry_orbit_clauses(
                    closure,
                    tree,
                    branch,
                    pool,
                )
            )
        clauses.update(source_clauses)
        sources_metadata.append(
            {
                "path": path.as_posix(),
                "sha256": hashlib.sha256(raw).hexdigest(),
                "status": state.get("status"),
                "representative_records": len(records),
                "transported_clauses": len(source_clauses),
            }
        )
    return tuple(sorted(clauses)), sources_metadata


def zero_forest_orbit_clauses(
    paths: list[Path],
    branch: str,
    pool,
) -> tuple[tuple[tuple[int, ...], ...], list[dict]]:
    """Transport exact zero-forest closures through branch symmetries."""
    clauses = []
    sources_metadata = []
    source_colour_actions = source_colour_stabilizer(branch)
    for path in paths:
        raw = path.read_bytes()
        state = json.loads(raw)
        if state.get("branch") != branch:
            raise ValueError(f"orbit seed branch mismatch: {path}")
        records = state.get("records", [])
        source_clauses = set()
        source_closures = set()
        for index, record in enumerate(records):
            certificate = record.get("certificate", {})
            if (
                record.get("gauge_tree") not in ([], ())
                or certificate.get("status") != "UNIT_IDEAL"
                or certificate.get("metadata", {}).get(
                    "saturated_parameters"
                )
                != 0
            ):
                raise ValueError(
                    "orbit seed is not a zero-forest pure-only "
                    f"unit ideal: {path} record {index}"
                )
            closure = tuple(
                tuple(map(int, row))
                for row in record["closure_supports"]
            )
            for modes in (
                (0,) + permutation
                for permutation in itertools.permutations((1, 2, 3, 4))
            ):
                for sources, colours in source_colour_actions:
                    transformed = transform_support_array(
                        closure,
                        modes,
                        sources,
                        colours,
                    )
                    source_closures.add(transformed)
                    source_clauses.add(
                        chart_clause(
                            pool,
                            transformed,
                            (),
                            branch,
                        )
                    )
        clauses.extend(source_clauses)
        sources_metadata.append(
            {
                "path": path.as_posix(),
                "sha256": hashlib.sha256(raw).hexdigest(),
                "status": state.get("status"),
                "representative_records": len(records),
                "transported_closures": len(source_closures),
                "transported_clauses": len(source_clauses),
                "mode_actions": 24,
                "source_colour_actions": len(
                    source_colour_actions
                ),
            }
        )
    return tuple(sorted(set(clauses))), sources_metadata


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--branch",
        choices=tuple(BRANCH_BACKBONES),
        required=True,
    )
    parser.add_argument("--models", type=int, default=10)
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument(
        "--relax-timeout",
        type=int,
        default=2,
        help="direct Singular timeout for each closure-enlargement trial",
    )
    parser.add_argument(
        "--skip-relax",
        action="store_true",
        help="learn the initial closure without enlargement trials",
    )
    parser.add_argument(
        "--relax-rows-only",
        action="store_true",
        help="try at most one whole-cell-group relaxation per row",
    )
    parser.add_argument(
        "--prefer-split",
        action="store_true",
        help="try the equivalent split-saturation system first",
    )
    parser.add_argument(
        "--gauge-tree-alternatives",
        type=int,
        default=0,
        help=(
            "try this many deterministic alternative maximal gauge "
            "forests before the long historical-tree calculation"
        ),
    )
    parser.add_argument(
        "--gauge-tree-portfolio-timeout",
        type=float,
        default=6.0,
        help="exact direct-Singular deadline per gauge-tree candidate",
    )
    parser.add_argument(
        "--try-empty-forest-first",
        action="store_true",
        help=(
            "probe a zero-pivot support-closure certificate before "
            "falling back to the maximal gauge forest"
        ),
    )
    parser.add_argument(
        "--empty-forest-timeout",
        type=float,
        default=0.75,
        help="split-Singular timeout for the zero-pivot probe",
    )
    parser.add_argument(
        "--transformed-seed-state",
        action="append",
        default=[],
        type=Path,
        help=(
            "reuse pure-only unit-ideal records after upgrading their "
            "clauses to exact chart applicability"
        ),
    )
    parser.add_argument(
        "--zero-forest-orbit-state",
        action="append",
        default=[],
        type=Path,
        help=(
            "transport exact zero-forest representative closures "
            "through branch-preserving mode/source/colour symmetries"
        ),
    )
    parser.add_argument(
        "--chart-orbit-state",
        action="append",
        default=[],
        type=Path,
        help=(
            "transport all exact pure-only charts in a prior ledger "
            "through branch-preserving symmetries"
        ),
    )
    parser.add_argument(
        "--learn-chart-orbits",
        action="store_true",
        help=(
            "add the full branch-symmetry orbit of every newly "
            "certified chart"
        ),
    )
    parser.add_argument("--state", type=Path)
    parser.add_argument(
        "--checkpoint-every",
        type=int,
        default=1,
        help="persist the full ledger after this many learned charts",
    )
    parser.add_argument(
        "--min-available-percent",
        type=float,
        default=20.0,
    )
    args = parser.parse_args()
    if (
        args.models <= 0
        or args.timeout <= 0
        or args.relax_timeout <= 0
        or args.empty_forest_timeout <= 0
        or args.gauge_tree_alternatives < 0
        or args.gauge_tree_portfolio_timeout <= 0
        or args.checkpoint_every <= 0
    ):
        raise ValueError(
            "models and both CAS timeouts must be positive"
        )
    if args.skip_relax and args.relax_rows_only:
        raise ValueError(
            "skip-relax and relax-rows-only are mutually exclusive"
        )
    if args.try_empty_forest_first and not args.skip_relax:
        raise ValueError(
            "the empty-forest probe currently requires --skip-relax"
        )
    if not 15 <= args.min_available_percent < 100:
        raise ValueError(
            "memory floor must be at least 15 and below 100"
        )

    allowed = SEMANTICS.finite_field_local_signatures()
    cnf, pool = SEMANTICS.build_pair_support_cnf(allowed)
    branch_restriction = add_branch_restriction(
        cnf,
        pool,
        allowed,
        args.branch,
    )
    lex_leaders = add_stabilizer_lex_leaders(
        cnf,
        pool,
        args.branch,
    )
    base_clauses = len(cnf.clauses)
    transformed_clauses, seed_sources = transformed_seed_clauses(
        args.transformed_seed_state,
        args.branch,
        pool,
    )
    zero_orbit_clauses, zero_orbit_sources = (
        zero_forest_orbit_clauses(
            args.zero_forest_orbit_state,
            args.branch,
            pool,
        )
    )
    chart_orbit_clauses, chart_orbit_sources = (
        chart_orbit_seed_clauses(
            args.chart_orbit_state,
            args.branch,
            pool,
        )
    )
    seed_clause_set = (
        set(transformed_clauses)
        | set(zero_orbit_clauses)
        | set(chart_orbit_clauses)
    )
    seed_clauses = tuple(sorted(seed_clause_set))
    cnf.extend([list(clause) for clause in seed_clauses])
    metadata = {
        "catalogue_signatures": len(allowed),
        "chart_clause_schema": (
            "no entries outside closure plus present gauge pivots; "
            "normalized branch-fixed singleton conditions omitted"
        ),
        "gauge_schema": (
            "maximal acyclic actual-support forest prioritizing "
            "remaining closure-singleton pivots"
        ),
        "gauge_tree_portfolio": {
            "alternative_count": args.gauge_tree_alternatives,
            "trial_timeout_seconds": (
                args.gauge_tree_portfolio_timeout
            ),
            "ordering": "deterministic-min-equations-v1",
        },
        "closure_relaxation": {
            "strategy": "recursive-row-greedy-v1",
            "trial_timeout_seconds": args.relax_timeout,
            "modes": [1, 2, 3, 4],
        },
        "empty_forest_probe": {
            "enabled": args.try_empty_forest_first,
            "strategy": "split-only-v1",
            "timeout_seconds": args.empty_forest_timeout,
        },
        "branch_restriction": branch_restriction,
        "stabilizer_size": len(
            source_colour_stabilizer(args.branch)
        ),
        "lex_leaders": lex_leaders,
        "variables": pool.top,
        "base_clauses": base_clauses,
        "transformed_seed_sources": seed_sources,
        "transformed_seed_clauses": len(transformed_clauses),
        "zero_forest_orbit_sources": zero_orbit_sources,
        "zero_forest_orbit_clauses": len(zero_orbit_clauses),
        "chart_orbit_sources": chart_orbit_sources,
        "chart_orbit_clauses": len(chart_orbit_clauses),
        "combined_seed_clauses": len(seed_clauses),
        "learn_chart_orbits": args.learn_chart_orbits,
    }
    # Checkpoints round-trip through JSON; normalize tuples now so resume
    # comparisons are stable across processes.
    metadata = json.loads(json.dumps(metadata))
    records = []
    if args.state is not None and args.state.exists():
        state = json.loads(args.state.read_text(encoding="utf-8"))
        if (
            state.get("branch") != args.branch
            or state.get("metadata") != metadata
        ):
            raise ValueError("state metadata does not match this branch")
        records = list(state.get("records", []))
        for record in records:
            if args.learn_chart_orbits:
                resumed_clauses = chart_symmetry_orbit_clauses(
                    tuple(
                        tuple(map(int, row))
                        for row in record["closure_supports"]
                    ),
                    tuple(
                        tuple(map(int, edge))
                        for edge in record["gauge_tree"]
                    ),
                    args.branch,
                    pool,
                )
            else:
                resumed_clauses = (tuple(record["clause"]),)
            for resumed_clause in resumed_clauses:
                if resumed_clause not in seed_clause_set:
                    cnf.append(list(resumed_clause))
                    seed_clause_set.add(resumed_clause)

    with Solver(
        name="cadical195",
        bootstrap_with=cnf.clauses,
    ) as solver:
        for _model_index in range(args.models):
            available = available_memory_percent()
            if available < args.min_available_percent:
                checkpoint(
                    args.state,
                    args.branch,
                    metadata,
                    records,
                    "PAUSED_MEMORY_FLOOR",
                )
                print(
                    json.dumps(
                        {
                            "status": "PAUSED_MEMORY_FLOOR",
                            "branch": args.branch,
                            "charts": len(records),
                            "available_percent": round(available, 3),
                            "min_available_percent": (
                                args.min_available_percent
                            ),
                        }
                    ),
                    flush=True,
                )
                return
            if not solver.solve():
                checkpoint(
                    args.state,
                    args.branch,
                    metadata,
                    records,
                    "UNSAT",
                )
                print(
                    json.dumps(
                        {
                            "status": "UNSAT",
                            "branch": args.branch,
                            "charts": len(records),
                            "seed_charts": len(seed_clauses),
                            "metadata": metadata,
                        }
                    ),
                    flush=True,
                )
                return
            model = solver.get_model()
            supports = SEMANTICS.supports_from_model(pool, model)
            indices = selected_signature_indices(
                pool,
                model,
                allowed,
            )
            initial_closure = closure_supports(supports)
            maximal_tree = gauge_tree(supports, initial_closure)
            initial_tree = maximal_tree
            gauge_portfolio = {
                "strategy": "disabled",
                "alternative_count": 0,
                "trial_timeout_seconds": (
                    args.gauge_tree_portfolio_timeout
                ),
                "trials": [],
                "selected_tree": initial_tree,
            }
            profile = tuple(
                sum(mask in (1, 2, 4) for mask in row)
                for row in supports
            )
            empty_forest_trial = None
            if args.try_empty_forest_first:
                empty_certificate = certify_chart(
                    initial_closure,
                    indices,
                    (),
                    args.empty_forest_timeout,
                    prefer_split=True,
                    split_only=True,
                )
                empty_forest_trial = {
                    "status": empty_certificate["status"],
                    "method": empty_certificate.get("method"),
                    "seconds": (
                        empty_certificate.get("cas")
                        or empty_certificate.get("split_cas")
                        or {}
                    ).get("elapsed_seconds"),
                }
                if empty_certificate["status"] == "UNIT_IDEAL":
                    initial_tree = ()
                    certificate = empty_certificate
                    gauge_portfolio = {
                        "strategy": "zero-forest-selected",
                        "alternative_count": 0,
                        "trial_timeout_seconds": (
                            args.empty_forest_timeout
                        ),
                        "trials": [],
                        "selected_tree": (),
                    }
                else:
                    if args.gauge_tree_alternatives:
                        (
                            portfolio_tree,
                            portfolio_certificate,
                            gauge_portfolio,
                        ) = certify_gauge_tree_portfolio(
                            supports,
                            initial_closure,
                            indices,
                            args.gauge_tree_alternatives,
                            args.gauge_tree_portfolio_timeout,
                        )
                        if portfolio_certificate is not None:
                            initial_tree = portfolio_tree
                            certificate = portfolio_certificate
                        else:
                            certificate = certify_chart(
                                initial_closure,
                                indices,
                                initial_tree,
                                args.timeout,
                                prefer_split=args.prefer_split,
                            )
                    else:
                        certificate = certify_chart(
                            initial_closure,
                            indices,
                            initial_tree,
                            args.timeout,
                            prefer_split=args.prefer_split,
                        )
            else:
                certificate = certify_chart(
                    initial_closure,
                    indices,
                    initial_tree,
                    args.timeout,
                    prefer_split=args.prefer_split,
                )
            if certificate["status"] != "UNIT_IDEAL":
                print(
                    json.dumps(
                        {
                            "status": "CAS_INCONCLUSIVE",
                            "branch": args.branch,
                            "coordinate_profile": profile,
                            "supports": supports,
                            "signature_indices": indices,
                            "gauge_tree": initial_tree,
                            "certificate": certificate,
                        }
                    ),
                    flush=True,
                )
                checkpoint(
                    args.state,
                    args.branch,
                    metadata,
                    records,
                    "CAS_INCONCLUSIVE",
                )
                return
            if args.skip_relax:
                closure = initial_closure
                tree = initial_tree
                relaxation = {
                    "strategy": "skipped",
                    "trial_timeout_seconds": args.relax_timeout,
                    "trials": [],
                    "accepted_cells": (),
                    "paused_for_memory": False,
                }
            else:
                closure, tree, relaxation = relax_chart_closure(
                    supports,
                    indices,
                    initial_closure,
                    args.relax_timeout,
                    args.min_available_percent,
                    recursive=not args.relax_rows_only,
                    prefer_split=args.prefer_split,
                )
            if closure != initial_closure:
                certificate = certify_chart(
                    closure,
                    indices,
                    tree,
                    args.timeout,
                    prefer_split=args.prefer_split,
                )
                if certificate["status"] != "UNIT_IDEAL":
                    raise AssertionError(
                        "accepted relaxed closure did not recertify"
                    )
            clause = chart_clause(
                pool,
                closure,
                tree,
                args.branch,
            )
            positive = {literal for literal in model if literal > 0}
            if any(
                (
                    abs(literal) in positive
                    if literal > 0
                    else abs(literal) not in positive
                )
                for literal in clause
            ):
                raise AssertionError(
                    "learned chart clause is not false on its model"
                )
            if args.learn_chart_orbits:
                learned_clauses = chart_symmetry_orbit_clauses(
                    closure,
                    tree,
                    args.branch,
                    pool,
                )
                if clause not in learned_clauses:
                    raise AssertionError(
                        "chart symmetry orbit lost its representative"
                    )
            else:
                learned_clauses = (clause,)
            new_learned_clauses = tuple(
                candidate
                for candidate in learned_clauses
                if candidate not in seed_clause_set
            )
            for learned_clause in new_learned_clauses:
                solver.add_clause(list(learned_clause))
                seed_clause_set.add(learned_clause)
            connectors = tuple(
                edge
                for edge in tree
                if closure[edge[0]][edge[1]] not in (1, 2, 4)
            )
            records.append(
                {
                    "clause": clause,
                    "supports": supports,
                    "initial_closure_supports": initial_closure,
                    "closure_supports": closure,
                    "signature_indices": indices,
                    "coordinate_profile": profile,
                    "gauge_tree": tree,
                    "connector_entries": connectors,
                    "relaxation": relaxation,
                    "empty_forest_trial": empty_forest_trial,
                    "gauge_tree_portfolio": gauge_portfolio,
                    "certificate": certificate,
                    "transported_orbit_clauses": len(
                        learned_clauses
                    ),
                    "new_transported_orbit_clauses": len(
                        new_learned_clauses
                    ),
                }
            )
            if len(records) % args.checkpoint_every == 0:
                checkpoint(
                    args.state,
                    args.branch,
                    metadata,
                    records,
                    "IN_PROGRESS",
                )
            print(
                json.dumps(
                    {
                        "status": "LEARNED",
                        "branch": args.branch,
                        "charts": len(records),
                        "seed_charts": len(seed_clauses),
                        "coordinate_profile": profile,
                        "support_components": 20 - len(maximal_tree),
                        "gauge_forest_edges": len(tree),
                        "relaxed_cells": len(
                            relaxation["accepted_cells"]
                        ),
                        "relaxation_trials": len(
                            relaxation["trials"]
                        ),
                        "connectors": len(connectors),
                        "clause_literals": len(clause),
                        "transported_orbit_clauses": len(
                            learned_clauses
                        ),
                        "new_transported_orbit_clauses": len(
                            new_learned_clauses
                        ),
                        "cas_method": certificate["method"],
                        "cas_seconds": certificate["cas"][
                            "elapsed_seconds"
                        ],
                    }
                ),
                flush=True,
            )

    checkpoint(
        args.state,
        args.branch,
        metadata,
        records,
        "IN_PROGRESS",
    )


if __name__ == "__main__":
    main()
