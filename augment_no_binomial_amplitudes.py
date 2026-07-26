"""Forbid every exactly-two-term forbidden amplitude in an existing CNF.

The dense support encodings already allocate one Boolean indicator for
every (vertex colouring, perfect matching) pair.  For each forbidden
colouring this augmentation introduces a selector ``z``.  Every matching
indicator implies ``z``, and a guarded sequential-counter encoding imposes
at least three indicators whenever ``z`` is true.  Thus zero active
monomials are allowed, while one or two are forbidden.

This is a stronger exploratory support hypothesis.  UNSAT proves that the
specified support relaxation must expose a binomial amplitude; it does not
by itself prove the Krenn--Gu conjecture.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path

from pysat.card import CardEnc, EncType

from search_witness import EquationSystem


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def header(path: Path) -> tuple[int, int]:
    with path.open("rb") as handle:
        fields = handle.readline().split()
    if len(fields) != 4 or fields[:2] != [b"p", b"cnf"]:
        raise ValueError("input is not a DIMACS CNF")
    return int(fields[2]), int(fields[3])


def indicator_layout(
    system: EquationSystem,
    indicator_last_variable: int,
) -> tuple[int, int]:
    count = len(system.colourings) * len(system.matchings)
    first = indicator_last_variable - count + 1
    if first <= 0:
        raise ValueError("invalid amplitude-indicator range")
    return first, count


def colouring_indicators(
    first: int,
    matching_count: int,
    colouring_index: int,
) -> list[int]:
    start = first + colouring_index * matching_count
    return list(range(start, start + matching_count))


def no_binomial_extension(
    indicators: list[int],
    top_id: int,
) -> tuple[list[list[int]], int, int]:
    selector = top_id + 1
    at_least_three = CardEnc.atleast(
        lits=indicators,
        bound=3,
        top_id=selector,
        encoding=EncType.seqcounter,
    )
    clauses = [
        *([-indicator, selector] for indicator in indicators),
        *(
            [-selector, *map(int, clause)]
            for clause in at_least_three.clauses
        ),
    ]
    return clauses, int(at_least_three.nv), selector


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-cnf", type=Path, required=True)
    parser.add_argument("--output-cnf", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument(
        "--indicator-last-variable",
        type=int,
        required=True,
        help=(
            "last amplitude-indicator variable in the original support "
            "CNF; later augmentations may allocate variables after it"
        ),
    )
    args = parser.parse_args()

    system = EquationSystem(8, 3)
    old_variables, old_clauses = header(args.base_cnf)
    if args.indicator_last_variable > old_variables:
        raise ValueError("indicator range extends past the base CNF")
    first, indicator_count = indicator_layout(
        system, args.indicator_last_variable
    )
    matching_count = len(system.matchings)
    forbidden = [
        index
        for index, required in enumerate(system.target)
        if not required
    ]

    # First pass determines the exact DIMACS header without retaining
    # millions of clauses in memory.
    next_variable = old_variables
    counter_clauses = 0
    for colouring_index in forbidden:
        clauses, next_variable, _ = no_binomial_extension(
            colouring_indicators(
                first, matching_count, colouring_index
            ),
            next_variable,
        )
        counter_clauses += len(clauses)
    new_variables = next_variable
    new_clauses = old_clauses + counter_clauses

    args.output_cnf.parent.mkdir(parents=True, exist_ok=True)
    with args.base_cnf.open("rb") as reader, args.output_cnf.open(
        "wb"
    ) as writer:
        reader.readline()
        writer.write(
            f"p cnf {new_variables} {new_clauses}\n".encode("ascii")
        )
        shutil.copyfileobj(reader, writer, length=8 * 1024 * 1024)

        next_variable = old_variables
        buffer: list[bytes] = []
        for colouring_index in forbidden:
            clauses, next_variable, _ = no_binomial_extension(
                colouring_indicators(
                    first, matching_count, colouring_index
                ),
                next_variable,
            )
            for clause in clauses:
                buffer.append(
                    (
                        " ".join(map(str, clause)) + " 0\n"
                    ).encode("ascii")
                )
                if len(buffer) >= 10_000:
                    writer.writelines(buffer)
                    buffer.clear()
        if buffer:
            writer.writelines(buffer)

    observed_variables, observed_clauses = header(args.output_cnf)
    if (observed_variables, observed_clauses) != (
        new_variables,
        new_clauses,
    ):
        raise AssertionError("written DIMACS header is inconsistent")
    payload = {
        "scope": (
            "static no-binomial extension of the n=8 support "
            "relaxation"
        ),
        "stronger_than_prize_hypothesis": True,
        "base_cnf": str(args.base_cnf),
        "base_cnf_sha256": sha256(args.base_cnf),
        "output_cnf": str(args.output_cnf),
        "output_cnf_sha256": sha256(args.output_cnf),
        "old_variables": old_variables,
        "old_clauses": old_clauses,
        "new_variables": new_variables,
        "new_clauses": new_clauses,
        "indicator_first_variable": first,
        "indicator_last_variable": args.indicator_last_variable,
        "indicator_count": indicator_count,
        "perfect_matchings": matching_count,
        "colourings": len(system.colourings),
        "forbidden_colourings": len(forbidden),
        "conditional_counter_clauses": counter_clauses,
    }
    args.manifest.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
