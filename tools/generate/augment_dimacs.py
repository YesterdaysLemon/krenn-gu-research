"""Append explicitly supplied clauses to a DIMACS CNF with a hash manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_clause(raw: str) -> tuple[int, ...]:
    clause = tuple(int(token) for token in raw.split())
    if not clause:
        raise argparse.ArgumentTypeError("a clause cannot be empty")
    if 0 in clause:
        raise argparse.ArgumentTypeError(
            "omit the terminating zero from --clause"
        )
    return clause


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-cnf", type=Path, required=True)
    parser.add_argument("--output-cnf", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument(
        "--clause",
        type=parse_clause,
        action="append",
        required=True,
        help='space-separated DIMACS literals, for example --clause "17 -23"',
    )
    parser.add_argument("--scope", required=True)
    args = parser.parse_args()

    with args.base_cnf.open("r", encoding="ascii") as reader:
        prefix, kind, raw_variables, raw_clauses = reader.readline().split()
    if (prefix, kind) != ("p", "cnf"):
        raise ValueError("base file is not a DIMACS CNF")
    variables = int(raw_variables)
    clauses = int(raw_clauses)
    for clause in args.clause:
        if max(abs(literal) for literal in clause) > variables:
            raise ValueError("appended clause references an unknown variable")

    args.output_cnf.parent.mkdir(parents=True, exist_ok=True)
    with args.base_cnf.open("r", encoding="ascii") as reader, (
        args.output_cnf.open("w", encoding="ascii", newline="\n")
    ) as writer:
        next(reader)
        writer.write(
            f"p cnf {variables} {clauses + len(args.clause)}\n"
        )
        for line in reader:
            writer.write(line)
        for clause in args.clause:
            writer.write(
                " ".join(str(literal) for literal in clause) + " 0\n"
            )

    payload = {
        "scope": args.scope,
        "base_cnf": str(args.base_cnf),
        "base_cnf_sha256": sha256(args.base_cnf),
        "appended_clauses": [list(clause) for clause in args.clause],
        "variables": variables,
        "clauses": clauses + len(args.clause),
        "output_cnf": str(args.output_cnf),
        "output_cnf_sha256": sha256(args.output_cnf),
    }
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
