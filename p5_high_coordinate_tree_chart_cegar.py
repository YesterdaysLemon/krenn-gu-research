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
        tuple(mask if mask in (1, 2, 4) else 7 for mask in row)
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
            if mask in (1, 2, 4):
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


def run_singular(program: str, timeout: int) -> dict:
    started = time.monotonic()
    try:
        completed = subprocess.run(
            SINGULAR_COMMAND,
            input=program,
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return {
            "status": "TIMEOUT",
            "elapsed_seconds": round(time.monotonic() - started, 6),
        }
    output = completed.stdout + completed.stderr
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
    }


def certify_chart(
    closure: tuple[tuple[int, ...], ...],
    indices: tuple[int, ...],
    tree: tuple[tuple[int, int, int], ...],
    timeout: int,
    try_split: bool = True,
    prefer_split: bool = False,
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
    os.replace(temporary, path)


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
        "--transformed-seed-state",
        action="append",
        default=[],
        type=Path,
        help=(
            "reuse pure-only unit-ideal records after upgrading their "
            "clauses to exact chart applicability"
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
        or args.checkpoint_every <= 0
    ):
        raise ValueError(
            "models and both CAS timeouts must be positive"
        )
    if args.skip_relax and args.relax_rows_only:
        raise ValueError(
            "skip-relax and relax-rows-only are mutually exclusive"
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
    seed_clauses, seed_sources = transformed_seed_clauses(
        args.transformed_seed_state,
        args.branch,
        pool,
    )
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
        "closure_relaxation": {
            "strategy": "recursive-row-greedy-v1",
            "trial_timeout_seconds": args.relax_timeout,
            "modes": [1, 2, 3, 4],
        },
        "branch_restriction": branch_restriction,
        "stabilizer_size": len(
            source_colour_stabilizer(args.branch)
        ),
        "lex_leaders": lex_leaders,
        "variables": pool.top,
        "base_clauses": base_clauses,
        "transformed_seed_sources": seed_sources,
        "transformed_seed_clauses": len(seed_clauses),
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
            cnf.append(record["clause"])

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
            initial_tree = gauge_tree(supports, initial_closure)
            profile = tuple(
                sum(mask in (1, 2, 4) for mask in row)
                for row in supports
            )
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
            solver.add_clause(list(clause))
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
                    "certificate": certificate,
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
                        "support_components": 20 - len(tree),
                        "relaxed_cells": len(
                            relaxation["accepted_cells"]
                        ),
                        "relaxation_trials": len(
                            relaxation["trials"]
                        ),
                        "connectors": len(connectors),
                        "clause_literals": len(clause),
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
