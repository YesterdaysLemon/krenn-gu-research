"""Scan a generic order-14 equality survivor for exact transport."""

from __future__ import annotations

import sys as _bootstrap_sys
from pathlib import Path as _BootstrapPath

for _bootstrap_parent in _BootstrapPath(__file__).resolve().parents:
    if (_bootstrap_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        _bootstrap_sys.path.insert(0, str(_bootstrap_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap as _bootstrap_repository  # noqa: E402

REPO_ROOT, HERE = _bootstrap_repository(__file__, also=["."])

import argparse
import json
import time
from pathlib import Path

import numpy as np

import analyze_fourteen_vertex_cancellation_transport as transport
from krenn_gu.explore_random_even_cycle_forks import cycle_edges
from explore_random_minimal_singleton_sets import contiguous_cycles


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("exploration", type=Path)
    parser.add_argument("--survivor-index", type=int, default=0)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "tmp/fourteen_vertex_equality_survivor_"
            "cancellation_transport.json"
        ),
    )
    args = parser.parse_args()
    exploration = json.loads(
        args.exploration.read_text(encoding="utf-8")
    )
    survivor = exploration["survivors"][args.survivor_index]
    lengths = tuple(map(int, exploration["partition"]))
    cycles = contiguous_cycles(lengths)
    full_edges = frozenset(
        item for cycle in cycles for item in cycle_edges(cycle)
    )
    transport.FULL_EDGES = full_edges
    singleton_matchings = [
        tuple(
            transport.edge(*map(int, item))
            for item in survivor[key]
        )
        for key in ("first", "second", "third")
    ]
    labels = {
        item: colour
        for colour, matching in enumerate(singleton_matchings)
        for item in matching
    }
    matchings = transport.perfect_matchings(
        set(full_edges) | set(labels)
    )
    started = time.perf_counter()
    bitsets, counts, total_extensions = transport.active_bitsets(
        matchings, labels
    )
    certificate = transport.find_transport(
        bitsets, counts, matchings
    )
    payload = {
        "status": (
            "cancellation_transport_contradiction"
            if certificate is not None
            else "cancellation_transport_absent"
        ),
        "necessary_conditions_only": certificate is None,
        "exploration": str(args.exploration),
        "survivor_index": args.survivor_index,
        "full_cycle_type": list(lengths),
        "singleton_matchings": {
            key: survivor[key]
            for key in ("first", "second", "third")
        },
        "skeleton_perfect_matchings": len(matchings),
        "colourings_scanned": transport.EQUATIONS,
        "matching_extensions_accumulated": total_extensions,
        "zero_term_colourings": int(np.count_nonzero(counts == 0)),
        "one_term_forbidden_colourings": int(
            np.count_nonzero(counts == 1)
        ),
        "certificate": certificate,
        "elapsed_seconds": time.perf_counter() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
