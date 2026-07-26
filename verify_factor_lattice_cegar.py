"""Independent exact replay for a factor-lattice CEGAR certificate."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from typing import Sequence

import numpy as np

from eight_vertex_skeleton_laurent_batch import local_positive_to_flat
from eight_vertex_sparse_exact import positive_model_literals
from factor_lattice_cegar import (
    active_matching_data,
    factor_relations,
)
from search_witness import EquationSystem
from signed_binomial_lattice import _basis_data


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def exact_classes(
    basis_rows: Sequence[Sequence[int]],
    activity: Sequence[int],
    monomials: Sequence[Sequence[int]],
) -> list[dict[str, object]]:
    basis_data = _basis_data([list(map(int, row)) for row in basis_rows])
    if basis_data is None:
        raise AssertionError("certificate basis has no unimodular minor")
    independent, pivots, raw_basis, raw_inverse = basis_data
    if independent != list(range(len(basis_rows))):
        raise AssertionError("certificate basis rows are dependent")
    basis = np.asarray(raw_basis.tolist(), dtype=np.int64)
    inverse = np.asarray(raw_inverse.tolist(), dtype=np.int64)
    pivot_array = np.asarray(pivots, dtype=np.int64)

    classes: dict[
        tuple[int, ...],
        list[tuple[int, int, list[int]]],
    ] = defaultdict(list)
    for matching, raw_vector in zip(activity, monomials, strict=True):
        vector = np.asarray(raw_vector, dtype=np.int64)
        coordinates = vector[pivot_array] @ inverse
        residual = vector - coordinates @ basis
        sign = -1 if int(coordinates.sum()) % 2 else 1
        classes[tuple(map(int, residual))].append(
            (
                int(matching),
                sign,
                list(map(int, coordinates)),
            )
        )
    return [
        {
            "signed_coefficient": sum(item[1] for item in members),
            "members": [
                {
                    "matching_index": item[0],
                    "sign": item[1],
                    "coordinates": item[2],
                }
                for item in members
            ],
        }
        for _residual, members in sorted(classes.items())
    ]


def replay_certificate(
    system: EquationSystem,
    relations: Sequence[tuple[int, ...]],
    activities: Sequence[Sequence[int]],
    monomials: Sequence[Sequence[tuple[int, ...]]],
    certificate: dict[str, object],
) -> list[int]:
    mode = str(certificate["certificate_mode"])
    basis_ids = list(map(int, certificate["basis_relation_ids"]))
    if len(set(basis_ids)) != len(basis_ids):
        raise AssertionError("duplicate factor relation in certificate basis")
    if any(index < 0 or index >= len(relations) for index in basis_ids):
        raise AssertionError("factor relation id outside manifest range")
    basis_rows = [relations[index] for index in basis_ids]

    if mode == "inconsistent_factor_sign":
        target = int(certificate["target_relation_id"])
        basis_data = _basis_data(
            [list(map(int, row)) for row in basis_rows]
        )
        if basis_data is None:
            raise AssertionError("inconsistent-sign basis is invalid")
        independent, pivots, raw_basis, raw_inverse = basis_data
        if independent != list(range(len(basis_rows))):
            raise AssertionError("inconsistent-sign basis is dependent")
        basis = np.asarray(raw_basis.tolist(), dtype=np.int64)
        inverse = np.asarray(raw_inverse.tolist(), dtype=np.int64)
        vector = np.asarray(relations[target], dtype=np.int64)
        coordinates = vector[np.asarray(pivots)] @ inverse
        residual = vector - coordinates @ basis
        if np.any(residual) or int(coordinates.sum()) % 2:
            raise AssertionError("factor sign is not inconsistent")
        if list(map(int, coordinates)) != list(
            map(int, certificate["target_coordinates"])
        ):
            raise AssertionError("inconsistent-sign coordinates changed")
        return sorted({*basis_ids, target})

    if mode not in {
        "isolated_factor_lattice_class",
        "annihilated_required_amplitude",
    }:
        raise AssertionError(f"unknown certificate mode {mode}")
    equation = int(certificate["target_equation_index"])
    if list(map(int, activities[equation])) != list(
        map(int, certificate["target_matching_indices"])
    ):
        raise AssertionError("target amplitude activity changed")
    classes = exact_classes(
        basis_rows,
        activities[equation],
        monomials[equation],
    )
    if classes != certificate["signed_classes"]:
        raise AssertionError("signed factor-lattice classes changed")
    nonzero = [
        item
        for item in classes
        if int(item["signed_coefficient"]) != 0
    ]
    if mode == "isolated_factor_lattice_class":
        if bool(system.target[equation]) or len(nonzero) != 1:
            raise AssertionError("target is not an isolated forbidden class")
    else:
        if not bool(system.target[equation]) or nonzero:
            raise AssertionError("required amplitude is not annihilated")
    return sorted(basis_ids)


def parse_dimacs(path: Path) -> tuple[int, list[list[int]]]:
    variables = -1
    declared_clauses = -1
    clauses: list[list[int]] = []
    pending: list[int] = []
    with path.open("r", encoding="ascii") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line or line.startswith("c"):
                continue
            if line.startswith("p "):
                fields = line.split()
                if len(fields) != 4 or fields[1] != "cnf":
                    raise AssertionError("invalid DIMACS header")
                variables = int(fields[2])
                declared_clauses = int(fields[3])
                continue
            for token in map(int, line.split()):
                if token == 0:
                    clauses.append(pending)
                    pending = []
                else:
                    pending.append(token)
    if pending:
        raise AssertionError("unterminated DIMACS clause")
    if variables < 0 or len(clauses) != declared_clauses:
        raise AssertionError("DIMACS clause count mismatch")
    return variables, clauses


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--drat", type=Path, required=True)
    parser.add_argument("--cadical-log", type=Path, required=True)
    parser.add_argument("--drat-trim-log", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    source = json.loads(args.manifest.read_text(encoding="utf-8"))
    if source["status"] != "UNSAT":
        raise AssertionError("factor-lattice search did not finish UNSAT")
    model = Path(source["model"])
    if sha256(model) != source["model_sha256"]:
        raise AssertionError("source SAT model hash changed")
    system = EquationSystem(8, 3)
    selected = local_positive_to_flat(
        system,
        sorted(positive_model_literals(model)),
        center_degree=1,
    )
    if sorted(map(int, selected)) != list(
        map(int, source["selected_flat_indices"])
    ):
        raise AssertionError("selected support changed")
    activities, monomials = active_matching_data(system, selected)
    clauses, relations, origins = factor_relations(
        system,
        activities,
        monomials,
        include_direct_binomials=bool(
            source.get("include_direct_binomials", False)
        ),
        include_eight_term_cubes=bool(
            source.get("include_eight_term_cubes", False)
        ),
    )
    expected_relations = [
        {
            "relation_id": index,
            "vector": list(map(int, vector)),
            "origin": origins[index],
        }
        for index, vector in enumerate(relations)
    ]
    if expected_relations != source["factor_relations"]:
        raise AssertionError("factor relation reconstruction changed")
    if [list(map(int, clause)) for clause in clauses] != source[
        "factor_clauses"
    ]:
        raise AssertionError("factor clause reconstruction changed")

    learned: list[list[int]] = []
    modes: dict[str, int] = defaultdict(int)
    for branch in source["branches"]:
        certificate = dict(branch["certificate"])
        blocking_ids = replay_certificate(
            system,
            relations,
            activities,
            monomials,
            certificate,
        )
        expected_clause = [-(index + 1) for index in blocking_ids]
        if expected_clause != list(map(int, branch["blocking_clause"])):
            raise AssertionError("learned no-good does not match certificate")
        learned.append(expected_clause)
        modes[str(certificate["certificate_mode"])] += 1
    if learned != source["learned_clauses"]:
        raise AssertionError("learned clause list changed")

    cnf = Path(source["final_cnf"])
    if sha256(cnf) != source["final_cnf_sha256"]:
        raise AssertionError("final factor CNF hash changed")
    variables, parsed_clauses = parse_dimacs(cnf)
    expected_cnf = [
        *[list(map(int, clause)) for clause in clauses],
        *learned,
    ]
    if variables != len(relations) or parsed_clauses != expected_cnf:
        raise AssertionError("final factor CNF bytes encode wrong clauses")
    cadical_text = args.cadical_log.read_text(
        encoding="utf-8", errors="replace"
    )
    if "s UNSATISFIABLE" not in cadical_text:
        raise AssertionError("CaDiCaL log is not UNSAT")
    drat_trim_text = args.drat_trim_log.read_text(
        encoding="utf-8", errors="replace"
    )
    if "s VERIFIED" not in drat_trim_text:
        raise AssertionError("DRAT replay is not verified")

    payload = {
        "verified": True,
        "scope": (
            "fixed 84-entry n=8 support; exact four-term factor "
            "branches and signed-lattice reductions"
        ),
        "claim_scope": (
            "excludes this support stratum only; it is not the global "
            "Krenn-Gu conjecture"
        ),
        "manifest": str(args.manifest),
        "manifest_sha256": sha256(args.manifest),
        "source_model": str(model),
        "source_model_sha256": sha256(model),
        "selected_entries": len(selected),
        "factor_relations": len(relations),
        "factor_clauses": len(clauses),
        "learned_clauses": len(learned),
        "certificate_modes": dict(sorted(modes.items())),
        "final_cnf": str(cnf),
        "final_cnf_sha256": sha256(cnf),
        "drat": str(args.drat),
        "drat_sha256": sha256(args.drat),
        "cadical_log": str(args.cadical_log),
        "cadical_log_sha256": sha256(args.cadical_log),
        "drat_trim_log": str(args.drat_trim_log),
        "drat_trim_log_sha256": sha256(args.drat_trim_log),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
