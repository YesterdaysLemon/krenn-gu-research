"""Iterate verified partial-circuit support contradictions on one orbit."""

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

REPO_ROOT, HERE = _bootstrap_repository(__file__)


import argparse
import hashlib
import itertools
import json
import subprocess
import sys
import time
from pathlib import Path

from pysat.formula import CNF
from pysat.solvers import Solver


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def edge(first: int, second: int) -> tuple[int, int]:
    return tuple(sorted((int(first), int(second))))


def cycles_for(lengths: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    output = []
    start = 0
    for length in lengths:
        output.append(tuple(range(start, start + length)))
        start += length
    if start != 14:
        raise ValueError("partition does not sum to 14")
    return tuple(output)


def cycle_edges(cycle: tuple[int, ...]) -> set[tuple[int, int]]:
    return {
        edge(cycle[index], cycle[(index + 1) % len(cycle)])
        for index in range(len(cycle))
    }


def run(command: list[str]) -> None:
    result = subprocess.run(command, check=False)
    if result.returncode:
        raise RuntimeError(
            f"subprocess failed with code {result.returncode}: {command}"
        )


def write_chain(
    output: Path,
    *,
    status: str,
    base_cnf: Path,
    working_cnf: Path,
    partition: tuple[int, ...],
    orbit: int,
    radius: int,
    records: list[dict[str, object]],
    started: float,
) -> None:
    payload = {
        "status": status,
        "scope": (
            "one selector orbit, with every learned exact support no-good "
            "backed by an independently replayed partial-circuit "
            "amplitude contradiction"
        ),
        "base_cnf": str(base_cnf),
        "base_cnf_sha256": sha256(base_cnf),
        "working_cnf": str(working_cnf),
        "working_cnf_sha256": (
            sha256(working_cnf) if working_cnf.exists() else None
        ),
        "partition": list(partition),
        "orbit": orbit,
        "selector": 232 + orbit,
        "radius": radius,
        "verified_supports": len(records),
        "records": records,
        "global_conjecture_resolved": False,
        "elapsed_seconds": time.perf_counter() - started,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-cnf", type=Path, required=True)
    parser.add_argument("--partition", required=True)
    parser.add_argument("--orbit", type=int, required=True)
    parser.add_argument("--radius", type=int, default=2)
    parser.add_argument("--max-rounds", type=int, default=100)
    parser.add_argument("--artifact-prefix", type=Path, required=True)
    parser.add_argument("--working-cnf", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    started = time.perf_counter()
    partition = tuple(map(int, args.partition.split(",")))
    cycles = cycles_for(partition)
    full_edges = set().union(*(cycle_edges(cycle) for cycle in cycles))
    eligible = tuple(
        sorted(
            set(itertools.combinations(range(14), 2)) - full_edges
        )
    )
    if len(eligible) != 77:
        raise AssertionError("eligible edge count changed")
    edge_index = {item: index for index, item in enumerate(eligible)}
    formula = CNF(from_file=str(args.base_cnf))
    records: list[dict[str, object]] = []
    current_cnf = args.base_cnf
    selector = 232 + args.orbit

    for round_id in range(1, args.max_rounds + 1):
        with Solver(
            name="cadical195", bootstrap_with=formula.clauses
        ) as solver:
            sat = solver.solve(assumptions=[selector])
        if not sat:
            if current_cnf != args.working_cnf:
                args.working_cnf.parent.mkdir(
                    parents=True, exist_ok=True
                )
                formula.to_file(str(args.working_cnf))
            write_chain(
                args.output,
                status="orbit_closed",
                base_cnf=args.base_cnf,
                working_cnf=args.working_cnf,
                partition=partition,
                orbit=args.orbit,
                radius=args.radius,
                records=records,
                started=started,
            )
            print(
                json.dumps(
                    {
                        "status": "orbit_closed",
                        "verified_supports": len(records),
                    },
                    indent=2,
                ),
                flush=True,
            )
            return

        stem = Path(f"{args.artifact_prefix}_round{round_id:04d}")
        partial_path = stem.with_name(
            stem.name + "_partial_relations.json"
        )
        amplitude_path = stem.with_name(
            stem.name + "_amplitude_lattice.json"
        )
        verified_path = stem.with_name(
            stem.name + "_verified.json"
        )
        run(
            [
                sys.executable,
                str(HERE / "analyze_fourteen_vertex_partial_minimal_circuit_lattice.py"),
                "--cnf",
                str(current_cnf),
                "--partition",
                args.partition,
                "--orbit",
                str(args.orbit),
                "--output",
                str(partial_path),
            ]
        )
        partial = json.loads(
            partial_path.read_text(encoding="utf-8")
        )
        if not partial["distinct_forced_relations"]:
            write_chain(
                args.output,
                status="stalled_no_mandatory_relations",
                base_cnf=args.base_cnf,
                working_cnf=args.working_cnf,
                partition=partition,
                orbit=args.orbit,
                radius=args.radius,
                records=records,
                started=started,
            )
            return
        run(
            [
                sys.executable,
                str(HERE / "analyze_fourteen_vertex_partial_circuit_amplitude_lattice.py"),
                str(partial_path),
                "--radius",
                str(args.radius),
                "--output",
                str(amplitude_path),
            ]
        )
        amplitude = json.loads(
            amplitude_path.read_text(encoding="utf-8")
        )
        if amplitude.get("status") != "contradiction":
            if current_cnf != args.working_cnf:
                args.working_cnf.parent.mkdir(
                    parents=True, exist_ok=True
                )
                formula.to_file(str(args.working_cnf))
                current_cnf = args.working_cnf
            records.append(
                {
                    "round": round_id,
                    "status": "survivor",
                    "partial_analysis": str(partial_path),
                    "partial_analysis_sha256": sha256(partial_path),
                    "amplitude_analysis": str(amplitude_path),
                    "amplitude_analysis_sha256": sha256(amplitude_path),
                }
            )
            write_chain(
                args.output,
                status="stalled_radius_survivor",
                base_cnf=args.base_cnf,
                working_cnf=args.working_cnf,
                partition=partition,
                orbit=args.orbit,
                radius=args.radius,
                records=records,
                started=started,
            )
            print(
                json.dumps(
                    {
                        "status": "stalled_radius_survivor",
                        "round": round_id,
                    },
                    indent=2,
                ),
                flush=True,
            )
            return
        run(
            [
                sys.executable,
                str(HERE / "verify_fourteen_vertex_partial_circuit_amplitude_lattice.py"),
                str(partial_path),
                str(amplitude_path),
                "--output",
                str(verified_path),
            ]
        )
        verified = json.loads(
            verified_path.read_text(encoding="utf-8")
        )
        if not verified.get("verified"):
            raise AssertionError("independent verifier did not pass")
        clause = []
        for colour, factor in enumerate(
            partial["singleton_factors"]
        ):
            for raw_item in factor:
                item = edge(*map(int, raw_item))
                clause.append(
                    -(colour * len(eligible) + edge_index[item] + 1)
                )
        clause = sorted(set(clause))
        if len(clause) != 21:
            raise AssertionError("support no-good width changed")
        formula.append(clause)
        args.working_cnf.parent.mkdir(parents=True, exist_ok=True)
        formula.to_file(str(args.working_cnf))
        current_cnf = args.working_cnf
        record = {
            "round": round_id,
            "status": "verified_support_excluded",
            "partial_analysis": str(partial_path),
            "partial_analysis_sha256": sha256(partial_path),
            "amplitude_analysis": str(amplitude_path),
            "amplitude_analysis_sha256": sha256(amplitude_path),
            "verified": str(verified_path),
            "verified_sha256": sha256(verified_path),
            "support_no_good": clause,
            "working_cnf_sha256_after": sha256(args.working_cnf),
            "working_cnf_clauses_after": len(formula.clauses),
        }
        records.append(record)
        write_chain(
            args.output,
            status="in_progress",
            base_cnf=args.base_cnf,
            working_cnf=args.working_cnf,
            partition=partition,
            orbit=args.orbit,
            radius=args.radius,
            records=records,
            started=started,
        )
        print(
            json.dumps(
                {
                    "round": round_id,
                    "verified_supports": len(records),
                    "working_clauses": len(formula.clauses),
                },
                indent=2,
            ),
            flush=True,
        )

    write_chain(
        args.output,
        status="round_limit",
        base_cnf=args.base_cnf,
        working_cnf=args.working_cnf,
        partition=partition,
        orbit=args.orbit,
        radius=args.radius,
        records=records,
        started=started,
    )


if __name__ == "__main__":
    main()
