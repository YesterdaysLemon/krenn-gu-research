"""Add exact support no-goods from verified partial-circuit contradictions."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from pathlib import Path

from pysat.formula import CNF


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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-cnf", type=Path, required=True)
    parser.add_argument(
        "--verified-certificate",
        type=Path,
        action="append",
        required=True,
    )
    parser.add_argument("--output-cnf", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    started = time.perf_counter()

    certificate_records = []
    partition = None
    support_clauses = []
    for certificate_path in args.verified_certificate:
        verified = json.loads(
            certificate_path.read_text(encoding="utf-8")
        )
        if not verified.get("verified"):
            raise ValueError(f"{certificate_path} is not verified")
        partial_path = Path(verified["partial_analysis"])
        amplitude_path = Path(verified["amplitude_analysis"])
        if sha256(partial_path) != verified["partial_analysis_sha256"]:
            raise ValueError("verified partial-analysis hash changed")
        if sha256(amplitude_path) != verified["amplitude_analysis_sha256"]:
            raise ValueError("verified amplitude-analysis hash changed")
        partial = json.loads(partial_path.read_text(encoding="utf-8"))
        amplitude = json.loads(
            amplitude_path.read_text(encoding="utf-8")
        )
        local_partition = tuple(map(int, partial["partition"]))
        if partition is None:
            partition = local_partition
        elif partition != local_partition:
            raise ValueError("certificates use different partitions")
        if amplitude.get("status") != "contradiction":
            raise ValueError("source analysis no longer claims contradiction")
        certificate_records.append(
            {
                "verified_certificate": str(certificate_path),
                "verified_certificate_sha256": sha256(certificate_path),
                "partial_analysis": str(partial_path),
                "partial_analysis_sha256": sha256(partial_path),
                "amplitude_analysis": str(amplitude_path),
                "amplitude_analysis_sha256": sha256(amplitude_path),
                "orbit": int(partial["orbit"]),
            }
        )
        support_clauses.append(partial["singleton_factors"])
    if partition is None:
        raise AssertionError("no certificates loaded")

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
    clauses = []
    for factors in support_clauses:
        clause = []
        for colour, factor in enumerate(factors):
            if len(factor) != 7:
                raise AssertionError("certified role stopped being a factor")
            for raw_item in factor:
                item = edge(*map(int, raw_item))
                clause.append(
                    -(colour * len(eligible) + edge_index[item] + 1)
                )
        if len(set(clause)) != 21:
            raise AssertionError("support no-good width changed")
        clauses.append(tuple(sorted(clause)))
    clauses = sorted(set(clauses))

    formula = CNF(from_file=str(args.base_cnf))
    existing = {tuple(map(int, clause)) for clause in formula.clauses}
    new_clauses = [clause for clause in clauses if clause not in existing]
    formula.extend(new_clauses)
    args.output_cnf.parent.mkdir(parents=True, exist_ok=True)
    formula.to_file(str(args.output_cnf))
    payload = {
        "status": "verified_partial_circuit_support_no_goods_augmented",
        "partition": list(partition),
        "base_cnf": str(args.base_cnf),
        "base_cnf_sha256": sha256(args.base_cnf),
        "base_variables": CNF(from_file=str(args.base_cnf)).nv,
        "base_clauses": len(CNF(from_file=str(args.base_cnf)).clauses),
        "certificate_records": certificate_records,
        "candidate_support_no_goods": len(clauses),
        "new_support_no_goods": len(new_clauses),
        "support_no_good_widths": sorted(
            {len(clause) for clause in new_clauses}
        ),
        "support_no_goods": [list(clause) for clause in new_clauses],
        "output_cnf": str(args.output_cnf),
        "output_cnf_sha256": sha256(args.output_cnf),
        "output_variables": formula.nv,
        "output_clauses": len(formula.clauses),
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
