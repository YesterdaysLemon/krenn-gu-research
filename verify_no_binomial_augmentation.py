"""Byte-replay a static no-binomial DIMACS augmentation."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from augment_no_binomial_amplitudes import (
    colouring_indicators,
    header,
    indicator_layout,
    no_binomial_extension,
)
from search_witness import EquationSystem


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    payload = json.loads(args.manifest.read_text(encoding="utf-8"))
    base = Path(payload["base_cnf"])
    augmented = Path(payload["output_cnf"])
    if sha256(base) != payload["base_cnf_sha256"]:
        raise AssertionError("base-CNF hash changed")
    if sha256(augmented) != payload["output_cnf_sha256"]:
        raise AssertionError("augmented-CNF hash changed")
    if header(base) != (
        int(payload["old_variables"]),
        int(payload["old_clauses"]),
    ):
        raise AssertionError("base-CNF header changed")
    if header(augmented) != (
        int(payload["new_variables"]),
        int(payload["new_clauses"]),
    ):
        raise AssertionError("augmented-CNF header is incorrect")

    # Check that the entire base body is preserved byte-for-byte.
    with base.open("rb") as base_reader, augmented.open("rb") as reader:
        base_reader.readline()
        reader.readline()
        while True:
            expected = base_reader.read(8 * 1024 * 1024)
            if not expected:
                break
            observed = reader.read(len(expected))
            if observed != expected:
                raise AssertionError("base-CNF body prefix changed")

        system = EquationSystem(8, 3)
        first, count = indicator_layout(
            system, int(payload["indicator_last_variable"])
        )
        if (
            first != int(payload["indicator_first_variable"])
            or count != int(payload["indicator_count"])
        ):
            raise AssertionError("amplitude-indicator layout changed")
        forbidden = [
            index
            for index, required in enumerate(system.target)
            if not required
        ]
        if len(forbidden) != int(payload["forbidden_colourings"]):
            raise AssertionError("forbidden-colouring count changed")

        next_variable = int(payload["old_variables"])
        clause_count = 0
        for colouring_index in forbidden:
            clauses, next_variable, _ = no_binomial_extension(
                colouring_indicators(
                    first,
                    len(system.matchings),
                    colouring_index,
                ),
                next_variable,
            )
            for clause in clauses:
                expected = (
                    " ".join(map(str, clause)) + " 0\n"
                ).encode("ascii")
                if reader.readline() != expected:
                    raise AssertionError(
                        "no-binomial extension clause changed"
                    )
                clause_count += 1
        if reader.read(1):
            raise AssertionError("augmented CNF has an unverified suffix")

    if next_variable != int(payload["new_variables"]):
        raise AssertionError("extension variable count changed")
    if clause_count != int(payload["conditional_counter_clauses"]):
        raise AssertionError("extension clause count changed")
    if int(payload["old_clauses"]) + clause_count != int(
        payload["new_clauses"]
    ):
        raise AssertionError("total clause count is inconsistent")

    result = {
        "verified": True,
        "manifest": str(args.manifest),
        "manifest_sha256": sha256(args.manifest),
        "output_cnf_sha256": payload["output_cnf_sha256"],
        "variables": next_variable,
        "extension_clauses": clause_count,
    }
    if args.output is not None:
        args.output.write_text(
            json.dumps(result, indent=2) + "\n",
            encoding="utf-8",
        )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
