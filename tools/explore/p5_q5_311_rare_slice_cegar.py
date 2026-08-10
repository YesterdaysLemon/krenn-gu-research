#!/usr/bin/env python3
"""Learn exact rare-slice chart orbits across the q5_311 branch."""

from __future__ import annotations

import argparse
import gc
import hashlib
import json
import sqlite3
import struct
import time
from collections import defaultdict
from pathlib import Path

from pysat.card import CardEnc, EncType
from pysat.solvers import Solver

import sys

for _parent in Path(__file__).resolve().parents:
    if (_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        sys.path.insert(0, str(_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__, also=["."])

from krenn_gu import p5_q5_311_support as COVER
from krenn_gu import p5_support_system as GENERATOR
from krenn_gu import atomic_json as MINIMIZE
from krenn_gu import p5_high_coordinate as HIGH
from krenn_gu import p5_pair_support_semantics as SEMANTICS
from krenn_gu import p5_q5_311_program as RARE


BRANCH = "q5_311"
STRONG_SUBSUMER_MAX_LITERALS = 10


def run_singular_with_error_retry(
    program: str,
    timeout: float,
) -> dict:
    """Retry one fail-closed CAS infrastructure error."""
    first = HIGH.run_singular(program, timeout)
    if first["status"] != "ERROR":
        return first
    second = HIGH.run_singular(program, timeout)
    second["driver_error_retry"] = {
        "first_status": first["status"],
        "first_returncode": first.get("returncode"),
        "first_output_tail": first.get("output_tail"),
    }
    return second


def terminal_cas_result(certificate_data: dict) -> dict:
    return (
        certificate_data.get("cas")
        or certificate_data.get("split_cas")
        or certificate_data.get("direct_cas")
        or {}
    )


def add_coordinate_profile_restriction(
    cnf,
    pool,
    profile: tuple[int, ...],
) -> int:
    """Restrict discovery to one exact singleton-count profile.

    The learned chart certificates remain valid without this restriction,
    so a completed profile run can be reused as a globally valid seed set.
    """
    clauses_before = len(cnf.clauses)
    for mode, bound in enumerate(profile):
        literals = [
            pool.id(("singleton", mode, source, colour))
            for source in SEMANTICS.SOURCES
            for colour in SEMANTICS.COLOURS
        ]
        cnf.extend(
            CardEnc.equals(
                lits=literals,
                bound=bound,
                vpool=pool,
                encoding=EncType.seqcounter,
            ).clauses
        )
    return len(cnf.clauses) - clauses_before


def certificate(
    record: dict,
    direct_timeout: float,
    split_timeout: float,
) -> dict:
    program, split_program, metadata = RARE.build_program(
        record,
        include_majority_pure=True,
    )
    direct = run_singular_with_error_retry(program, direct_timeout)
    if direct["status"] == "UNIT_IDEAL":
        return {
            "status": "UNIT_IDEAL",
            "method": "direct",
            "source_sha256": HIGH.sha256_text(program),
            "split_source_sha256": HIGH.sha256_text(split_program),
            "metadata": metadata,
            "cas": direct,
        }
    split = run_singular_with_error_retry(
        split_program,
        split_timeout,
    )
    if split["status"] == "UNIT_IDEAL":
        return {
            "status": "UNIT_IDEAL",
            "method": "split",
            "source_sha256": HIGH.sha256_text(program),
            "split_source_sha256": HIGH.sha256_text(split_program),
            "metadata": metadata,
            "direct_cas": direct,
            "cas": split,
        }
    return {
        "status": "INCONCLUSIVE",
        "source_sha256": HIGH.sha256_text(program),
        "split_source_sha256": HIGH.sha256_text(split_program),
        "metadata": metadata,
        "direct_cas": direct,
        "split_cas": split,
    }


def split_certificate(
    record: dict,
    timeout: float,
) -> dict:
    program, split_program, metadata = RARE.build_program(
        record,
        include_majority_pure=True,
    )
    split = run_singular_with_error_retry(split_program, timeout)
    if split["status"] == "UNIT_IDEAL":
        return {
            "status": "UNIT_IDEAL",
            "method": "split",
            "source_sha256": HIGH.sha256_text(program),
            "split_source_sha256": HIGH.sha256_text(split_program),
            "metadata": metadata,
            "cas": split,
        }
    return {
        "status": "INCONCLUSIVE",
        "source_sha256": HIGH.sha256_text(program),
        "split_source_sha256": HIGH.sha256_text(split_program),
        "metadata": metadata,
        "split_cas": split,
    }


class DiskClauseStore:
    """Exact temporary clause set without a large Python-object heap."""

    def __init__(self) -> None:
        # An empty SQLite filename creates a private temporary on-disk
        # database which disappears when the connection closes.
        self.connection = sqlite3.connect("")
        self.connection.execute("PRAGMA journal_mode=OFF")
        self.connection.execute("PRAGMA synchronous=OFF")
        self.connection.execute("PRAGMA temp_store=FILE")
        self.connection.execute(
            "CREATE TABLE clauses (payload BLOB PRIMARY KEY) WITHOUT ROWID"
        )
        self.count = 0

    @staticmethod
    def encode(clause: tuple[int, ...]) -> bytes:
        if not clause:
            raise AssertionError("empty chart clause")
        return struct.pack(f"<{len(clause)}i", *clause)

    @staticmethod
    def decode(payload: bytes) -> tuple[int, ...]:
        if not payload or len(payload) % 4:
            raise AssertionError("invalid stored chart clause")
        return struct.unpack(f"<{len(payload) // 4}i", payload)

    def add(self, clause: tuple[int, ...]) -> bool:
        before = self.connection.total_changes
        self.connection.execute(
            "INSERT OR IGNORE INTO clauses(payload) VALUES (?)",
            (sqlite3.Binary(self.encode(clause)),),
        )
        added = self.connection.total_changes != before
        if added:
            self.count += 1
        return added

    def contains(self, clause: tuple[int, ...]) -> bool:
        row = self.connection.execute(
            "SELECT 1 FROM clauses WHERE payload=?",
            (sqlite3.Binary(self.encode(clause)),),
        ).fetchone()
        return row is not None

    def clauses(self):
        for (payload,) in self.connection.execute(
            "SELECT payload FROM clauses"
        ):
            yield self.decode(payload)

    def commit(self) -> None:
        self.connection.commit()

    def close(self) -> None:
        self.connection.close()


def seed_clause_store(
    paths: list[Path],
    pool,
) -> tuple[DiskClauseStore, list[dict], tuple[tuple[int, ...], ...]]:
    store = DiskClauseStore()
    strong_clauses = set()
    sources = []
    try:
        for path in paths:
            raw = path.read_bytes()
            state = json.loads(raw)
            if state.get("branch") != BRANCH:
                raise ValueError(f"rare seed branch mismatch in {path}")
            records = state.get("records", [])
            before = store.count
            for index, record in enumerate(records):
                certificate_data = record.get("certificate", {})
                metadata = certificate_data.get("metadata", {})
                equation_scope = record.get("equation_scope", "rare")
                common_valid = (
                    certificate_data.get("status") != "UNIT_IDEAL"
                    or certificate_data.get("cas", {}).get("status")
                    != "UNIT_IDEAL"
                )
                rare_invalid = (
                    equation_scope == "rare"
                    and (
                        metadata.get("majority_mixed_equations") != 0
                        or tuple(
                            metadata.get("saturated_pure_colours", ())
                        )
                        != (0, 1, 2)
                    )
                )
                full_invalid = (
                    equation_scope == "full"
                    and metadata.get("pure_coefficients") != 3
                )
                if (
                    common_valid
                    or equation_scope not in ("rare", "full")
                    or rare_invalid
                    or full_invalid
                ):
                    raise ValueError(
                        f"{path} record {index} is not an exact chart seed"
                    )
                closure = tuple(
                    tuple(map(int, row))
                    for row in record["closure_supports"]
                )
                tree = tuple(
                    tuple(map(int, edge))
                    for edge in record["gauge_tree"]
                )
                for clause in HIGH.chart_symmetry_orbit_clauses(
                    closure,
                    tree,
                    BRANCH,
                    pool,
                ):
                    if not store.add(clause):
                        continue
                    if len(clause) <= STRONG_SUBSUMER_MAX_LITERALS:
                        strong_clauses.add(clause)
            store.commit()
            sources.append(
                {
                    "path": path.as_posix(),
                    "sha256": hashlib.sha256(raw).hexdigest(),
                    "status": state.get("status"),
                    "representative_records": len(records),
                    "new_transported_clauses": store.count - before,
                }
            )
    except BaseException:
        store.close()
        raise
    return (
        store,
        sources,
        tuple(sorted(strong_clauses)),
    )


def strong_subsumption_index(
    strong_clauses: tuple[tuple[int, ...], ...],
) -> dict[int, tuple[frozenset[int], ...]]:
    by_first_literal = defaultdict(list)
    for clause in strong_clauses:
        if not clause:
            raise AssertionError("empty chart clause")
        by_first_literal[clause[0]].append(frozenset(clause))
    return {
        literal: tuple(clause_sets)
        for literal, clause_sets in by_first_literal.items()
    }


def is_strongly_subsumed(
    clause: tuple[int, ...],
    by_first_literal: dict[int, tuple[frozenset[int], ...]],
) -> bool:
    if len(clause) <= STRONG_SUBSUMER_MAX_LITERALS:
        return False
    clause_set = frozenset(clause)
    return any(
        strong_clause.issubset(clause_set)
        for literal in clause
        for strong_clause in by_first_literal.get(literal, ())
    )


def seed_subsumption_metadata(
    store: DiskClauseStore,
    strong_clauses: tuple[tuple[int, ...], ...],
) -> tuple[dict[int, tuple[frozenset[int], ...]], dict]:
    by_first_literal = strong_subsumption_index(strong_clauses)
    removed = sum(
        is_strongly_subsumed(clause, by_first_literal)
        for clause in store.clauses()
    )
    return (
        by_first_literal,
        {
            "max_subsumer_literals": STRONG_SUBSUMER_MAX_LITERALS,
            "strong_clauses": len(strong_clauses),
            "removed_clauses": removed,
            "retained_clauses": store.count - removed,
        },
    )


def remove_strongly_subsumed_clauses(
    clauses: tuple[tuple[int, ...], ...],
) -> tuple[tuple[tuple[int, ...], ...], dict]:
    """Compatibility helper used by focused tests."""
    strong_clauses = tuple(
        clause
        for clause in clauses
        if len(clause) <= STRONG_SUBSUMER_MAX_LITERALS
    )
    by_first_literal = strong_subsumption_index(strong_clauses)
    retained = tuple(
        clause
        for clause in clauses
        if not is_strongly_subsumed(clause, by_first_literal)
    )
    return retained, {
        "max_subsumer_literals": STRONG_SUBSUMER_MAX_LITERALS,
        "strong_clauses": len(strong_clauses),
        "removed_clauses": len(clauses) - len(retained),
        "retained_clauses": len(retained),
    }


def checkpoint(
    path: Path | None,
    metadata: dict,
    records: list[dict],
    status: str,
) -> None:
    if path is None:
        return
    MINIMIZE.atomic_write(
        path,
        {
            "status": status,
            "branch": BRANCH,
            "metadata": metadata,
            "records": records,
        },
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--models", type=int, default=10_000)
    parser.add_argument("--direct-timeout", type=float, default=2)
    parser.add_argument("--split-timeout", type=float, default=10)
    parser.add_argument(
        "--full-fallback-timeout",
        type=float,
        default=30,
        help=(
            "direct full-equation deadline per gauge after the rare "
            "subsystem is inconclusive"
        ),
    )
    parser.add_argument(
        "--full-split-timeout",
        type=float,
        default=60,
        help=(
            "one split-saturation fallback deadline after every direct "
            "full-equation gauge is inconclusive"
        ),
    )
    parser.add_argument(
        "--gauge-tree-alternatives",
        type=int,
        default=16,
    )
    parser.add_argument(
        "--try-empty-forest-first",
        action="store_true",
    )
    parser.add_argument(
        "--empty-forest-timeout",
        type=float,
        default=1,
    )
    parser.add_argument(
        "--seed-state",
        action="append",
        type=Path,
        default=[],
    )
    parser.add_argument(
        "--coordinate-profile",
        nargs=5,
        type=int,
        metavar=("Q0", "Q1", "Q2", "Q3", "Q4"),
        help=(
            "discover globally valid charts inside one exact per-mode "
            "singleton-count profile"
        ),
    )
    parser.add_argument("--state", type=Path)
    parser.add_argument("--checkpoint-every", type=int, default=20)
    parser.add_argument(
        "--min-available-percent",
        type=float,
        default=20.0,
    )
    parser.add_argument(
        "--bootstrap-reserve-percent",
        type=float,
        default=10.0,
        help=(
            "additional host-memory headroom required before building "
            "and copying the large SAT bootstrap"
        ),
    )
    parser.add_argument(
        "--startup-wait-seconds",
        type=float,
        default=0,
        help=(
            "wait for bootstrap headroom instead of exiting "
            "immediately; checks every 15 seconds"
        ),
    )
    args = parser.parse_args()
    if (
        args.models <= 0
        or args.direct_timeout <= 0
        or args.split_timeout <= 0
        or args.full_fallback_timeout <= 0
        or args.full_split_timeout <= 0
        or args.empty_forest_timeout <= 0
        or args.gauge_tree_alternatives < 0
        or args.checkpoint_every <= 0
        or not 15 <= args.min_available_percent < 100
        or args.bootstrap_reserve_percent < 0
        or args.startup_wait_seconds < 0
        or (
            args.min_available_percent
            + args.bootstrap_reserve_percent
            >= 100
        )
        or (
            args.coordinate_profile is not None
            and (
                args.coordinate_profile[0] != 5
                or any(
                    value < 0 or value > len(SEMANTICS.SOURCES)
                    for value in args.coordinate_profile
                )
            )
        )
    ):
        raise ValueError("invalid rare-slice CEGAR arguments")
    coordinate_profile = (
        tuple(args.coordinate_profile)
        if args.coordinate_profile is not None
        else None
    )
    startup_floor = (
        args.min_available_percent
        + args.bootstrap_reserve_percent
    )
    startup_available = HIGH.available_memory_percent()
    wait_deadline = (
        time.monotonic() + args.startup_wait_seconds
    )
    while (
        startup_available < startup_floor
        and time.monotonic() < wait_deadline
    ):
        print(
            json.dumps(
                {
                    "status": "WAITING_MEMORY_FLOOR_STARTUP",
                    "available_percent": round(
                        startup_available,
                        3,
                    ),
                    "required_percent": startup_floor,
                }
            ),
            flush=True,
        )
        time.sleep(
            min(
                15.0,
                max(0.0, wait_deadline - time.monotonic()),
            )
        )
        startup_available = HIGH.available_memory_percent()
    if startup_available < startup_floor:
        print(
            json.dumps(
                {
                    "status": "PAUSED_MEMORY_FLOOR_STARTUP",
                    "available_percent": round(
                        startup_available,
                        3,
                    ),
                    "required_percent": startup_floor,
                }
            ),
            flush=True,
        )
        return

    allowed = SEMANTICS.finite_field_local_signatures()
    retained_mixed = COVER.rare_mixed_colourings()
    cnf, pool = SEMANTICS.build_pair_support_cnf(
        allowed,
        mixed_colourings=retained_mixed,
    )
    branch_metadata = HIGH.add_branch_restriction(
        cnf,
        pool,
        allowed,
        BRANCH,
    )
    lex_leaders = HIGH.add_stabilizer_lex_leaders(
        cnf,
        pool,
        BRANCH,
    )
    profile_clauses = (
        add_coordinate_profile_restriction(
            cnf,
            pool,
            coordinate_profile,
        )
        if coordinate_profile is not None
        else 0
    )
    base_clauses = len(cnf.clauses)
    clause_store, seed_sources, strong_clauses = seed_clause_store(
        args.seed_state,
        pool,
    )
    subsumption_index, subsumption = seed_subsumption_metadata(
        clause_store,
        strong_clauses,
    )
    transported_count = clause_store.count
    effective_transported_count = subsumption["retained_clauses"]
    print(
        json.dumps(
            {
                "status": "SEED_STORE_READY",
                "transported_seed_clauses": transported_count,
                "effective_transported_seed_clauses": (
                    effective_transported_count
                ),
                "strong_seed_subsumption": subsumption,
                "available_percent": round(
                    HIGH.available_memory_percent(),
                    3,
                ),
            }
        ),
        flush=True,
    )
    metadata = {
        "scope": (
            "rare q5_311 mixed slices plus all pure nonvanishing; "
            "global prize conjecture unresolved"
        ),
        "catalogue_signatures": len(allowed),
        "rare_mixed_colourings": len(retained_mixed),
        "majority_mixed_colourings": 0,
        "pure_colour_nonvanishing": [0, 1, 2],
        "branch_restriction": branch_metadata,
        "lex_leaders": lex_leaders,
        "coordinate_profile_restriction": coordinate_profile,
        "coordinate_profile_clauses": profile_clauses,
        "base_variables": pool.top,
        "base_clauses": base_clauses,
        "seed_sources": seed_sources,
        "transported_seed_clauses": transported_count,
        "effective_transported_seed_clauses": (
            effective_transported_count
        ),
        "strong_seed_subsumption": subsumption,
        "gauge_tree_alternatives": args.gauge_tree_alternatives,
        "empty_forest_probe": {
            "enabled": args.try_empty_forest_first,
            "timeout_seconds": args.empty_forest_timeout,
            "strategy": "split-only",
        },
        "direct_timeout_seconds": args.direct_timeout,
        "split_timeout_seconds": args.split_timeout,
        "full_fallback": {
            "enabled": True,
            "direct_timeout_seconds": args.full_fallback_timeout,
            "split_timeout_seconds": args.full_split_timeout,
            "strategy": (
                "all deterministic gauges by full mixed-equation "
                "count, then one split retry"
            ),
        },
        "resource_guard": {
            "minimum_available_percent": (
                args.min_available_percent
            ),
            "bootstrap_reserve_percent": (
                args.bootstrap_reserve_percent
            ),
            "bootstrap_required_percent": startup_floor,
            "bootstrap_strategy": (
                "base-cnf-first then exact temporary-disk seed stream"
            ),
        },
        "learn_chart_orbits": True,
        "global_conjecture_resolved": False,
    }
    metadata = json.loads(json.dumps(metadata))
    records = []
    # The exact temporary SQLite set handles the 800k+ immutable clauses.
    # Keep a Python set only for the much smaller dynamic continuation.
    dynamic_clause_set = set()

    def clause_is_accounted(clause: tuple[int, ...]) -> bool:
        return (
            clause in dynamic_clause_set
            or clause_store.contains(clause)
        )

    if args.state is not None and args.state.exists():
        state = json.loads(args.state.read_text(encoding="utf-8"))
        if (
            state.get("branch") != BRANCH
            or state.get("metadata") != metadata
        ):
            raise ValueError("rare CEGAR state metadata changed")
        records = list(state.get("records", []))
        for record in records:
            for clause in HIGH.chart_symmetry_orbit_clauses(
                tuple(
                    tuple(map(int, row))
                    for row in record["closure_supports"]
                ),
                tuple(
                    tuple(map(int, edge))
                    for edge in record["gauge_tree"]
                ),
                BRANCH,
                pool,
            ):
                if clause_is_accounted(clause):
                    continue
                cnf.append(list(clause))
                dynamic_clause_set.add(clause)

    prebootstrap_available = HIGH.available_memory_percent()
    if prebootstrap_available < startup_floor:
        checkpoint(
            args.state,
            metadata,
            records,
            "PAUSED_MEMORY_FLOOR_BOOTSTRAP",
        )
        print(
            json.dumps(
                {
                    "status": "PAUSED_MEMORY_FLOOR_BOOTSTRAP",
                    "charts": len(records),
                    "available_percent": round(
                        prebootstrap_available,
                        3,
                    ),
                    "required_percent": startup_floor,
                }
            ),
            flush=True,
        )
        clause_store.close()
        return

    with Solver(
        name="cadical195",
        bootstrap_with=cnf.clauses,
    ) as solver:
        # The native solver has copied the base and resumed dynamic clauses.
        # Release that Python CNF before streaming immutable seed clauses
        # out of the exact disk-backed set.
        del cnf
        gc.collect()
        seeded = 0
        scanned = 0
        for clause in clause_store.clauses():
            scanned += 1
            if is_strongly_subsumed(clause, subsumption_index):
                continue
            solver.add_clause(list(clause))
            seeded += 1
            if scanned % 10_000:
                continue
            available = HIGH.available_memory_percent()
            if available < args.min_available_percent:
                checkpoint(
                    args.state,
                    metadata,
                    records,
                    "PAUSED_MEMORY_FLOOR_SEED_STREAM",
                )
                print(
                    json.dumps(
                        {
                            "status": (
                                "PAUSED_MEMORY_FLOOR_SEED_STREAM"
                            ),
                            "charts": len(records),
                            "available_percent": round(available, 3),
                            "seed_clauses_streamed": seeded,
                            "seed_clauses_total": (
                                effective_transported_count
                            ),
                        }
                    ),
                    flush=True,
                )
                return
        if seeded != effective_transported_count:
            raise AssertionError("effective seed-clause count changed")
        print(
            json.dumps(
                {
                    "status": "SEED_STREAM_READY",
                    "seed_clauses_streamed": seeded,
                    "available_percent": round(
                        HIGH.available_memory_percent(),
                        3,
                    ),
                }
            ),
            flush=True,
        )

        for _ in range(args.models):
            available = HIGH.available_memory_percent()
            if available < args.min_available_percent:
                checkpoint(
                    args.state,
                    metadata,
                    records,
                    "PAUSED_MEMORY_FLOOR",
                )
                print(
                    json.dumps(
                        {
                            "status": "PAUSED_MEMORY_FLOOR",
                            "charts": len(records),
                            "available_percent": round(available, 3),
                        }
                    ),
                    flush=True,
                )
                return
            if not solver.solve():
                checkpoint(args.state, metadata, records, "UNSAT")
                print(
                    json.dumps(
                        {
                            "status": "UNSAT",
                            "charts": len(records),
                            "seed_clauses": transported_count,
                        }
                    ),
                    flush=True,
                )
                return

            model = solver.get_model()
            supports = SEMANTICS.supports_from_model(pool, model)
            signatures = HIGH.selected_signature_indices(
                pool,
                model,
                allowed,
            )
            closure = HIGH.closure_supports(supports)
            trials = []
            selected_tree = None
            selected_certificate = None
            selected_scope = None
            if args.try_empty_forest_first:
                empty_candidate = {
                    "supports": supports,
                    "closure_supports": closure,
                    "gauge_tree": (),
                }
                empty_result = split_certificate(
                    empty_candidate,
                    args.empty_forest_timeout,
                )
                empty_cas = terminal_cas_result(empty_result)
                trials.append(
                    {
                        "equation_scope": "rare",
                        "tree": (),
                        "rare_mixed_equations": empty_result[
                            "metadata"
                        ]["rare_mixed_equations"],
                        "status": empty_result["status"],
                        "cas_status": empty_cas.get("status"),
                        "method": empty_result.get("method"),
                        "seconds": empty_cas.get("elapsed_seconds"),
                        "error_tail": (
                            empty_cas.get("output_tail")
                            if empty_cas.get("status") == "ERROR"
                            else None
                        ),
                    }
                )
                if empty_result["status"] == "UNIT_IDEAL":
                    selected_tree = ()
                    selected_certificate = empty_result
                    selected_scope = "rare"

            variants = (
                ()
                if selected_certificate is not None
                else HIGH.gauge_tree_variants(
                    supports,
                    closure,
                    args.gauge_tree_alternatives,
                )
            )
            scored = []
            for tree in variants:
                candidate = {
                    "supports": supports,
                    "closure_supports": closure,
                    "gauge_tree": tree,
                }
                _program, _split, chart_metadata = (
                    RARE.build_program(
                        candidate,
                        include_majority_pure=True,
                    )
                )
                scored.append(
                    (
                        chart_metadata["rare_mixed_equations"],
                        tree,
                    )
                )

            for mixed_count, tree in sorted(scored):
                candidate = {
                    "supports": supports,
                    "closure_supports": closure,
                    "gauge_tree": tree,
                }
                result = certificate(
                    candidate,
                    args.direct_timeout,
                    args.split_timeout,
                )
                result_cas = terminal_cas_result(result)
                trials.append(
                    {
                        "equation_scope": "rare",
                        "tree": tree,
                        "rare_mixed_equations": mixed_count,
                        "status": result["status"],
                        "cas_status": result_cas.get("status"),
                        "method": result.get("method"),
                        "seconds": result_cas.get(
                            "elapsed_seconds"
                        ),
                        "error_tail": (
                            result_cas.get("output_tail")
                            if result_cas.get("status") == "ERROR"
                            else None
                        ),
                    }
                )
                if result["status"] == "UNIT_IDEAL":
                    selected_tree = tree
                    selected_certificate = result
                    selected_scope = "rare"
                    break

            if selected_certificate is None:
                full_scored = []
                for tree in variants:
                    _program, full_metadata = GENERATOR.generate(
                        closure,
                        signatures,
                        expected_partial_cells=0,
                        pure_saturation_only=True,
                        gauge_tree_edges=tree,
                        allow_arbitrary_support=True,
                    )
                    full_scored.append(
                        (
                            full_metadata["mixed_equations"],
                            tree,
                        )
                    )
                ordered_full = sorted(full_scored)
                for mixed_count, tree in ordered_full:
                    result = HIGH.certify_chart(
                        closure,
                        signatures,
                        tree,
                        args.full_fallback_timeout,
                        try_split=False,
                    )
                    if (
                        terminal_cas_result(result).get("status")
                        == "ERROR"
                    ):
                        result = HIGH.certify_chart(
                            closure,
                            signatures,
                            tree,
                            args.full_fallback_timeout,
                            try_split=False,
                        )
                    direct_cas = (
                        result.get("cas")
                        or result.get("direct_cas")
                        or {}
                    )
                    trials.append(
                        {
                            "equation_scope": "full",
                            "tree": tree,
                            "mixed_equations": mixed_count,
                            "status": result["status"],
                            "cas_status": direct_cas.get("status"),
                            "method": result.get("method"),
                            "seconds": direct_cas.get(
                                "elapsed_seconds"
                            ),
                            "error_tail": (
                                direct_cas.get("output_tail")
                                if direct_cas.get("status")
                                == "ERROR"
                                else None
                            ),
                        }
                    )
                    if result["status"] == "UNIT_IDEAL":
                        selected_tree = tree
                        selected_certificate = result
                        selected_scope = "full"
                        break

                if (
                    selected_certificate is None
                    and ordered_full
                ):
                    mixed_count, tree = ordered_full[0]
                    result = HIGH.certify_chart(
                        closure,
                        signatures,
                        tree,
                        args.full_split_timeout,
                        try_split=True,
                        prefer_split=True,
                        split_only=True,
                    )
                    if (
                        terminal_cas_result(result).get("status")
                        == "ERROR"
                    ):
                        result = HIGH.certify_chart(
                            closure,
                            signatures,
                            tree,
                            args.full_split_timeout,
                            try_split=True,
                            prefer_split=True,
                            split_only=True,
                        )
                    split_cas = (
                        result.get("cas")
                        or result.get("split_cas")
                        or {}
                    )
                    trials.append(
                        {
                            "equation_scope": "full",
                            "tree": tree,
                            "mixed_equations": mixed_count,
                            "status": result["status"],
                            "cas_status": split_cas.get("status"),
                            "method": result.get("method"),
                            "seconds": split_cas.get(
                                "elapsed_seconds"
                            ),
                            "error_tail": (
                                split_cas.get("output_tail")
                                if split_cas.get("status")
                                == "ERROR"
                                else None
                            ),
                            "split_retry": True,
                        }
                    )
                    if result["status"] == "UNIT_IDEAL":
                        selected_tree = tree
                        selected_certificate = result
                        selected_scope = "full"
            if selected_certificate is None:
                checkpoint(
                    args.state,
                    metadata,
                    records,
                    "CAS_INCONCLUSIVE",
                )
                print(
                    json.dumps(
                        {
                            "status": "CAS_INCONCLUSIVE",
                            "charts": len(records),
                            "supports": supports,
                            "signature_indices": signatures,
                            "trials": trials,
                        }
                    ),
                    flush=True,
                )
                return

            orbit = HIGH.chart_symmetry_orbit_clauses(
                closure,
                selected_tree,
                BRANCH,
                pool,
            )
            new_clauses = 0
            for clause in orbit:
                if clause_is_accounted(clause):
                    continue
                solver.add_clause(list(clause))
                dynamic_clause_set.add(clause)
                new_clauses += 1
            representative_clause = HIGH.chart_clause(
                pool,
                closure,
                selected_tree,
                BRANCH,
            )
            records.append(
                {
                    "clause": representative_clause,
                    "supports": supports,
                    "closure_supports": closure,
                    "signature_indices": signatures,
                    "equation_scope": selected_scope,
                    "coordinate_profile": tuple(
                        sum(mask in (1, 2, 4) for mask in row)
                        for row in supports
                    ),
                    "gauge_tree": selected_tree,
                    "portfolio_trials": trials,
                    "transported_orbit_clauses": len(orbit),
                    "new_transported_orbit_clauses": new_clauses,
                    "certificate": selected_certificate,
                }
            )
            selected_metadata = selected_certificate["metadata"]
            selected_mixed_equations = (
                selected_metadata.get("rare_mixed_equations")
                if selected_scope == "rare"
                else selected_metadata.get("mixed_equations")
            )
            print(
                json.dumps(
                    {
                        "status": "LEARNED",
                        "charts": len(records),
                        "equation_scope": selected_scope,
                        "mixed_equations": selected_mixed_equations,
                        "gauge_forest_edges": len(selected_tree),
                        "clause_literals": len(representative_clause),
                        "orbit_clauses": len(orbit),
                        "new_orbit_clauses": new_clauses,
                        "method": selected_certificate["method"],
                        "seconds": selected_certificate["cas"][
                            "elapsed_seconds"
                        ],
                    }
                ),
                flush=True,
            )
            if len(records) % args.checkpoint_every == 0:
                checkpoint(
                    args.state,
                    metadata,
                    records,
                    "IN_PROGRESS",
                )

    clause_store.close()
    checkpoint(args.state, metadata, records, "MODEL_LIMIT")
    print(
        json.dumps(
            {
                "status": "MODEL_LIMIT",
                "charts": len(records),
            }
        )
    )


if __name__ == "__main__":
    main()
