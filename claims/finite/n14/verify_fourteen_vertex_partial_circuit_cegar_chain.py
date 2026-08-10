"""Independently replay and reconstruct a partial-circuit CEGAR chain."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Sequence

from pysat.formula import CNF
from pysat.solvers import Solver


N = 14


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def edge(first: int, second: int) -> tuple[int, int]:
    return tuple(sorted((int(first), int(second))))


def cycles_for(lengths: Sequence[int]) -> tuple[tuple[int, ...], ...]:
    output = []
    start = 0
    for raw_length in lengths:
        length = int(raw_length)
        output.append(tuple(range(start, start + length)))
        start += length
    if start != N:
        raise AssertionError("partition stopped covering 14 vertices")
    return tuple(output)


def cycle_edges(cycle: Sequence[int]) -> set[tuple[int, int]]:
    return {
        edge(cycle[index], cycle[(index + 1) % len(cycle)])
        for index in range(len(cycle))
    }


def support_data(
    factors: Sequence[Sequence[Sequence[int]]],
    eligible: Sequence[tuple[int, int]],
    selector: int,
) -> tuple[list[int], list[int]]:
    edge_index = {item: index for index, item in enumerate(eligible)}
    selected = set()
    clause = []
    seen_edges = set()
    for colour, raw_factor in enumerate(factors):
        factor = tuple(edge(*map(int, item)) for item in raw_factor)
        if len(factor) != N // 2:
            raise AssertionError("singleton role stopped being a factor")
        if {vertex for item in factor for vertex in item} != set(range(N)):
            raise AssertionError("singleton role stopped covering vertices")
        if seen_edges & set(factor):
            raise AssertionError("singleton roles stopped being edge-disjoint")
        seen_edges.update(factor)
        for item in factor:
            if item not in edge_index:
                raise AssertionError("singleton edge is not eligible")
            variable = colour * len(eligible) + edge_index[item] + 1
            selected.add(variable)
            clause.append(-variable)
    if len(selected) != 3 * (N // 2):
        raise AssertionError("support no-good width changed")
    assumptions = [selector]
    assumptions.extend(
        variable if variable in selected else -variable
        for variable in range(1, 3 * len(eligible) + 1)
    )
    return sorted(clause), assumptions


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("chain", type=Path)
    parser.add_argument("--previous-chain", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    started = time.perf_counter()

    chain = json.loads(args.chain.read_text(encoding="utf-8"))
    base_cnf = Path(chain["base_cnf"])
    working_cnf = Path(chain["working_cnf"])
    if sha256(base_cnf) != chain["base_cnf_sha256"]:
        raise AssertionError("base CNF hash changed")
    if sha256(working_cnf) != chain["working_cnf_sha256"]:
        raise AssertionError("working CNF hash changed")
    if args.previous_chain is not None:
        previous = json.loads(
            args.previous_chain.read_text(encoding="utf-8")
        )
        if Path(previous["working_cnf"]) != base_cnf:
            raise AssertionError("previous chain does not feed this base CNF")
        if previous["working_cnf_sha256"] != chain["base_cnf_sha256"]:
            raise AssertionError("previous-chain hash binding changed")

    partition = tuple(map(int, chain["partition"]))
    cycles = cycles_for(partition)
    full_edges = set().union(*(cycle_edges(cycle) for cycle in cycles))
    eligible = tuple(
        sorted(set(itertools.combinations(range(N), 2)) - full_edges)
    )
    if len(eligible) != 77:
        raise AssertionError("eligible edge count changed")
    orbit = int(chain["orbit"])
    selector = int(chain["selector"])
    if selector != 232 + orbit:
        raise AssertionError("selector/orbit binding changed")
    records = chain["records"]
    if int(chain["verified_supports"]) != len(records):
        raise AssertionError("verified-support count changed")

    formula = CNF(from_file=str(base_cnf))
    fresh_algebra_replays = 0
    support_model_checks = 0
    intermediate_cnf_hashes_checked = 0
    with tempfile.TemporaryDirectory(
        prefix="partial-circuit-chain-audit-"
    ) as raw_directory:
        directory = Path(raw_directory)
        reconstructed_cnf = directory / "reconstructed.cnf"
        for expected_round, record in enumerate(records, start=1):
            if int(record["round"]) != expected_round:
                raise AssertionError("round numbering changed")
            if record["status"] != "verified_support_excluded":
                raise AssertionError("chain contains a non-exclusion record")
            partial_path = Path(record["partial_analysis"])
            amplitude_path = Path(record["amplitude_analysis"])
            verified_path = Path(record["verified"])
            for path, key in (
                (partial_path, "partial_analysis_sha256"),
                (amplitude_path, "amplitude_analysis_sha256"),
                (verified_path, "verified_sha256"),
            ):
                if sha256(path) != record[key]:
                    raise AssertionError(f"record hash changed: {path}")
            partial = json.loads(partial_path.read_text(encoding="utf-8"))
            verified = json.loads(
                verified_path.read_text(encoding="utf-8")
            )
            if not verified.get("verified"):
                raise AssertionError("stored algebra verifier did not pass")
            if tuple(map(int, partial["partition"])) != partition:
                raise AssertionError("record partition changed")
            if int(partial["orbit"]) != orbit:
                raise AssertionError("record orbit changed")
            if int(partial["selector"]) != selector:
                raise AssertionError("record selector changed")

            replay_path = directory / f"replay-{expected_round:04d}.json"
            replay = subprocess.run(
                [
                    sys.executable,
                    "verify_fourteen_vertex_partial_circuit_amplitude_lattice.py",
                    str(partial_path),
                    str(amplitude_path),
                    "--output",
                    str(replay_path),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            if replay.returncode:
                raise AssertionError(
                    "fresh algebra replay failed: "
                    + (replay.stderr or replay.stdout)
                )
            if sha256(replay_path) != sha256(verified_path):
                raise AssertionError("fresh algebra replay output changed")
            fresh_algebra_replays += 1

            clause, assumptions = support_data(
                partial["singleton_factors"], eligible, selector
            )
            if clause != list(map(int, record["support_no_good"])):
                raise AssertionError("support no-good reconstruction changed")
            with Solver(
                name="cadical195", bootstrap_with=formula.clauses
            ) as solver:
                if not solver.solve(assumptions=assumptions):
                    raise AssertionError(
                        "recorded support was not a model before exclusion"
                    )
            support_model_checks += 1

            formula.append(clause)
            if len(formula.clauses) != int(
                record["working_cnf_clauses_after"]
            ):
                raise AssertionError("intermediate clause count changed")
            formula.to_file(str(reconstructed_cnf))
            if sha256(reconstructed_cnf) != record[
                "working_cnf_sha256_after"
            ]:
                raise AssertionError("intermediate CNF hash changed")
            intermediate_cnf_hashes_checked += 1

        if not records:
            formula.to_file(str(reconstructed_cnf))
        if sha256(reconstructed_cnf) != chain["working_cnf_sha256"]:
            raise AssertionError("final reconstructed CNF hash changed")

    with Solver(
        name="cadical195", bootstrap_with=formula.clauses
    ) as solver:
        selector_sat = solver.solve(assumptions=[selector])
    if chain["status"] == "orbit_closed":
        if selector_sat:
            raise AssertionError("claimed closed selector is SAT")
    elif chain["status"] in {
        "round_limit",
        "in_progress",
        "stalled_no_mandatory_relations",
        "stalled_radius_survivor",
    }:
        if not selector_sat:
            raise AssertionError("non-closure chain unexpectedly closed orbit")
    else:
        raise AssertionError("unsupported chain status")

    payload = {
        "verified": True,
        "status": "partial_circuit_cegar_chain_verified",
        "scope": (
            "fresh algebra replays, exact support-model checks, sequential "
            "support no-good reconstruction, every intermediate CNF hash, "
            "the final CNF hash, and the terminal selector decision"
        ),
        "chain": str(args.chain),
        "chain_sha256": sha256(args.chain),
        "previous_chain": (
            str(args.previous_chain)
            if args.previous_chain is not None
            else None
        ),
        "base_cnf_sha256": chain["base_cnf_sha256"],
        "working_cnf_sha256": chain["working_cnf_sha256"],
        "partition": list(partition),
        "orbit": orbit,
        "chain_status": chain["status"],
        "verified_supports": len(records),
        "fresh_algebra_replays": fresh_algebra_replays,
        "support_model_checks": support_model_checks,
        "intermediate_cnf_hashes_checked": intermediate_cnf_hashes_checked,
        "selector_sat_after_chain": selector_sat,
        "global_conjecture_resolved": False,
        "elapsed_seconds": time.perf_counter() - started,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
