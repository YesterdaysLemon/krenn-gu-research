"""Fail-closed audit of the no-mixed-singleton SAT countermodels.

These models refute only a proposed consequence of the finite support
relaxation.  They are not Krenn-Gu witnesses: each still has an exact
elementary cancellation conflict.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from augment_forbid_mixed_singleton_matching import (
    mixed_singleton_clauses,
)
from cancellation_transport import (
    cube_cancellation_transport_certificates,
    cube_two_monomial_rectangle_certificates,
    support_cancellation_transport_conflict,
    support_two_monomial_rectangle_conflict,
)
from eight_vertex_skeleton_laurent_batch import local_positive_to_flat
from eight_vertex_sparse_exact import positive_model_literals
from search_witness import EquationSystem
from singleton_slice_minors import singleton_edges


CASES = (
    {
        "branch": "same",
        "manifest": Path(
            "tmp/eight_vertex_normalized_killers_reciprocal_"
            "same_min4_no_mixed_singleton_max20.json"
        ),
        "log": Path(
            "tmp/eight_vertex_same_no_mixed_singleton_kissat.log"
        ),
    },
    {
        "branch": "different",
        "manifest": Path(
            "tmp/eight_vertex_normalized_killers_reciprocal_"
            "different_min4_no_mixed_singleton_max20.json"
        ),
        "log": Path(
            "tmp/eight_vertex_different_no_mixed_singleton_kissat.log"
        ),
    },
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def header(path: Path) -> tuple[int, int]:
    with path.open("r", encoding="ascii") as handle:
        prefix, kind, variables, clauses = handle.readline().split()
    if (prefix, kind) != ("p", "cnf"):
        raise AssertionError(f"{path} is not DIMACS")
    return int(variables), int(clauses)


def verify_extension(
    base: Path,
    output: Path,
    singleton_base: int,
) -> None:
    old_variables, old_clauses = header(base)
    new_variables, new_clauses = header(output)
    expected = mixed_singleton_clauses(singleton_base)
    if (new_variables, new_clauses) != (
        old_variables,
        old_clauses + len(expected),
    ):
        raise AssertionError("extension header changed")
    with base.open("r", encoding="ascii") as old, output.open(
        "r",
        encoding="ascii",
    ) as new:
        next(old)
        next(new)
        for index, old_line in enumerate(old, start=1):
            if new.readline() != old_line:
                raise AssertionError(
                    f"base prefix changed at clause {index}"
                )
        for index, clause in enumerate(expected):
            expected_line = " ".join(map(str, clause)) + " 0\n"
            if new.readline() != expected_line:
                raise AssertionError(
                    f"mixed-singleton tail changed at {index}"
                )
        if new.readline():
            raise AssertionError("unexpected clauses after extension")


def verify_model(path: Path, positive: set[int]) -> int:
    variables, expected_clauses = header(path)
    if not positive or max(positive) > variables:
        raise AssertionError("model variable exceeds CNF header")
    checked = 0
    with path.open("r", encoding="ascii") as handle:
        next(handle)
        for checked, line in enumerate(handle, start=1):
            clause = [int(token) for token in line.split()[:-1]]
            if not any(
                literal in positive
                if literal > 0
                else -literal not in positive
                for literal in clause
            ):
                raise AssertionError(
                    f"model falsifies clause {checked}"
                )
    if checked != expected_clauses:
        raise AssertionError("CNF clause count changed")
    return checked


def replay_elementary_conflicts(
    system: EquationSystem,
    selected: set[int],
) -> dict[str, object]:
    transport = support_cancellation_transport_conflict(
        system,
        selected,
        set(),
    )
    rectangle = support_two_monomial_rectangle_conflict(
        system,
        selected,
        set(),
    )
    if rectangle is None:
        raise AssertionError("countermodel lost its rectangle conflict")
    rectangle_positive, rectangle_negative, rectangle_certificate = (
        rectangle
    )
    rectangle_replay = cube_two_monomial_rectangle_certificates(
        system,
        rectangle_certificate["corner_equation_indices"],
        rectangle_positive,
        rectangle_negative,
    )
    if rectangle_certificate not in rectangle_replay:
        raise AssertionError("rectangle replay failed")
    payload: dict[str, object] = {
        "rectangle_mode": rectangle_certificate[
            "certificate_mode"
        ],
        "rectangle_cube_size": (
            len(rectangle_positive) + len(rectangle_negative)
        ),
    }
    if transport is None:
        payload["transport"] = False
    else:
        positive, negative, certificate = transport
        replay = cube_cancellation_transport_certificates(
            system,
            [
                certificate["source_equation_index"],
                certificate["transport_equation_index"],
            ],
            positive,
            negative,
        )
        if certificate not in replay:
            raise AssertionError("transport replay failed")
        payload.update(
            {
                "transport": True,
                "transport_cube_size": len(positive) + len(negative),
            }
        )
    return payload


def main() -> None:
    system = EquationSystem(8, 3)
    rows: list[dict[str, object]] = []
    for case in CASES:
        manifest_path = case["manifest"]
        log = case["log"]
        manifest = json.loads(
            manifest_path.read_text(encoding="utf-8")
        )
        base = Path(str(manifest["base_cnf"]))
        output = Path(str(manifest["output_cnf"]))
        if manifest["base_cnf_sha256"] != sha256(base):
            raise AssertionError("base hash changed")
        if manifest["output_cnf_sha256"] != sha256(output):
            raise AssertionError("extension hash changed")
        verify_extension(
            base,
            output,
            int(manifest["singleton_base"]),
        )
        text = log.read_text(encoding="ascii")
        if "s SATISFIABLE" not in text:
            raise AssertionError("Kissat SAT terminal missing")
        positive = set(positive_model_literals(log))
        checked_clauses = verify_model(output, positive)
        selected = local_positive_to_flat(
            system,
            sorted(positive),
            1,
        )
        singletons = singleton_edges(system, selected)
        singleton_matchings = [
            matching
            for matching in system.matchings
            if all(edge in singletons for edge in matching)
        ]
        mixed = [
            matching
            for matching in singleton_matchings
            if len({singletons[edge] for edge in matching}) > 1
        ]
        if mixed:
            raise AssertionError(
                "model unexpectedly has a mixed singleton matching"
            )
        rows.append(
            {
                "branch": case["branch"],
                "manifest": str(manifest_path),
                "manifest_sha256": sha256(manifest_path),
                "cnf": str(output),
                "cnf_sha256": sha256(output),
                "log": str(log),
                "log_sha256": sha256(log),
                "clauses_checked": checked_clauses,
                "selected_entries": len(selected),
                "singleton_edges": len(singletons),
                "singleton_perfect_matchings": len(
                    singleton_matchings
                ),
                "mixed_singleton_perfect_matchings": len(mixed),
                **replay_elementary_conflicts(system, selected),
            }
        )
    payload = {
        "verified": True,
        "scope": (
            "SAT countermodels to the proposed mixed-singleton "
            "consequence of the n=8 support relaxation"
        ),
        "not_complex_witnesses": True,
        "cases": rows,
    }
    output = Path(
        "tmp/eight_vertex_no_mixed_singleton_"
        "countermodels_audit.json"
    )
    output.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
