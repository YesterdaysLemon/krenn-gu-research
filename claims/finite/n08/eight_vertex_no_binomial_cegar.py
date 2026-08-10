"""Search the dense n=8 support relaxation with all binomials forbidden.

The ordinary support CNF only excludes a forbidden amplitude with exactly
one active perfect-matching monomial.  This CEGAR adds the stronger
exploratory hypothesis that a forbidden amplitude may not have exactly two
active monomials either.

The amplitude indicators are already present in the base CNF.  If a SAT
model makes exactly indicators ``i`` and ``j`` true in one forbidden
colouring, the single clause

    -i OR -j OR (OR over all other matching indicators)

excludes precisely that active pair.  Clauses learned this way are global:
they express the no-binomial hypothesis and may be reused for every
skeleton role.

UNSAT from this program is a finite combinatorial result about the stronger
support relaxation, not a proof of the Krenn--Gu conjecture.  A SAT model
with no violated clause is equally useful: it is an explicit support that
avoids every two-term forbidden amplitude.
"""

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
import hashlib
import json
import subprocess
import time
from collections import Counter
import itertools
from pathlib import Path
from typing import Iterable

from eight_vertex_native_kissat_laurent_batch import (
    run_kissat,
)
from eight_vertex_skeleton_batch import (
    canonical_normalized_killer_skeletons,
    ordered_role_skeletons,
)
from krenn_gu.eight_vertex_sparse_exact import (
    local_allowed_edges,
    positive_model_literals,
)
from krenn_gu.search_witness import EquationSystem
from enumerate_double_c4_singleton_family import (
    skeleton_automorphisms,
    transform_pattern,
)


HEADER_WIDTH = 12


def first_skeleton_isomorphism(
    source: frozenset[tuple[int, int]],
    target: frozenset[tuple[int, int]],
    n: int,
) -> tuple[int, ...] | None:
    """Return one vertex permutation carrying ``source`` to ``target``."""
    if len(source) != len(target):
        return None
    source_degrees = sorted(
        sum(vertex in edge for edge in source) for vertex in range(n)
    )
    target_degrees = sorted(
        sum(vertex in edge for edge in target) for vertex in range(n)
    )
    if source_degrees != target_degrees:
        return None
    for permutation in itertools.permutations(range(n)):
        image = frozenset(
            tuple(sorted((permutation[first], permutation[second])))
            for first, second in source
        )
        if image == target:
            return tuple(map(int, permutation))
    return None


def expanded_family_catalogue(
    family: dict[str, object],
    system: EquationSystem,
) -> list[
    tuple[
        frozenset[tuple[int, int]],
        tuple[tuple[int, ...], ...],
    ]
]:
    """Expand every stored orbit on its reference skeleton."""
    catalogue: list[
        tuple[
            frozenset[tuple[int, int]],
            tuple[tuple[int, ...], ...],
        ]
    ] = []
    expanded_count = 0
    for family_type in family.get("types", [family]):
        family_edges = sorted(
            tuple(map(int, edge))
            for edge in family_type["skeleton_edges"]
        )
        source = frozenset(family_edges)
        positions = {
            edge: index for index, edge in enumerate(family_edges)
        }
        automorphisms = skeleton_automorphisms(system.n, source)
        patterns: set[tuple[int, ...]] = set()
        for orbit in family_type["orbits"]:
            canonical = tuple(
                map(int, orbit["canonical_edge_labels"])
            )
            for automorphism in automorphisms:
                for colour_permutation in itertools.permutations(
                    range(system.d)
                ):
                    patterns.add(
                        transform_pattern(
                            canonical,
                            family_edges,
                            positions,
                            automorphism,
                            colour_permutation,
                        )
                    )
        expected = int(family_type["labelled_supports"])
        if len(patterns) != expected:
            raise AssertionError(
                f"family orbit expansion produced {len(patterns)} "
                f"supports, expected {expected}"
            )
        expanded_count += len(patterns)
        catalogue.append((source, tuple(sorted(patterns))))
    if expanded_count != int(family["labelled_supports"]):
        raise AssertionError(
            f"aggregate family expansion produced {expanded_count} "
            f"supports, expected {family['labelled_supports']}"
        )
    return catalogue


def transported_family_supports(
    catalogues: Iterable[
        tuple[
            frozenset[tuple[int, int]],
            tuple[tuple[int, ...], ...],
        ]
    ],
    target: frozenset[tuple[int, int]],
    system: EquationSystem,
) -> set[frozenset[int]]:
    """Transport every isomorphic family support to one skeleton role."""
    target_edges = sorted(target)
    target_positions = {
        edge: index for index, edge in enumerate(target_edges)
    }
    supports: set[frozenset[int]] = set()
    for source, patterns in catalogues:
        isomorphism = first_skeleton_isomorphism(
            source,
            target,
            system.n,
        )
        if isomorphism is None:
            continue
        source_edges = sorted(source)
        for pattern in patterns:
            transported = [-1] * len(target_edges)
            for edge, label in zip(
                source_edges,
                pattern,
                strict=True,
            ):
                image = tuple(
                    sorted(
                        (
                            isomorphism[edge[0]],
                            isomorphism[edge[1]],
                        )
                    )
                )
                transported[target_positions[image]] = label
            if any(label < 0 for label in transported):
                raise AssertionError(
                    "family transport missed a target edge"
                )
            selected: set[int] = set()
            for edge, label in zip(
                target_edges,
                transported,
                strict=True,
            ):
                base = system.d**2 * system.edge_index[edge]
                if label == system.d:
                    selected.update(
                        range(base, base + system.d**2)
                    )
                else:
                    selected.add(
                        base + (system.d + 1) * label
                    )
            supports.add(frozenset(selected))
    return supports


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_header(path: Path) -> tuple[int, int]:
    with path.open("r", encoding="ascii") as handle:
        fields = handle.readline().split()
    if len(fields) != 4 or fields[:2] != ["p", "cnf"]:
        raise ValueError(f"{path} has no DIMACS header")
    return int(fields[2]), int(fields[3])


def fixed_header(variables: int, clauses: int) -> str:
    return (
        f"p cnf {variables:{HEADER_WIDTH}d} "
        f"{clauses:{HEADER_WIDTH}d}\n"
    )


def checkpoint(path: Path, payload: dict[str, object]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def materialize_role(
    base_cnf: Path,
    output_cnf: Path,
    variables: int,
    base_clauses: int,
    learned: Iterable[tuple[int, ...]],
    units: Iterable[int],
) -> int:
    learned_rows = list(learned)
    unit_rows = list(units)
    clause_count = base_clauses + len(learned_rows) + len(unit_rows)
    with base_cnf.open("r", encoding="ascii") as reader, output_cnf.open(
        "w", encoding="ascii", newline="\n"
    ) as writer:
        next(reader)
        writer.write(fixed_header(variables, clause_count))
        for line in reader:
            writer.write(line)
        for clause in learned_rows:
            writer.write(" ".join(map(str, clause)) + " 0\n")
        for literal in unit_rows:
            writer.write(f"{literal} 0\n")
    return clause_count


def append_clauses(
    cnf: Path,
    variables: int,
    old_clause_count: int,
    clauses: Iterable[tuple[int, ...]],
) -> int:
    rows = list(clauses)
    if not rows:
        return old_clause_count
    new_clause_count = old_clause_count + len(rows)
    with cnf.open("ab") as handle:
        for clause in rows:
            handle.write(
                (" ".join(map(str, clause)) + " 0\n").encode("ascii")
            )
    header = fixed_header(variables, new_clause_count).encode("ascii")
    with cnf.open("r+b") as handle:
        old_header = handle.readline()
        if len(old_header) != len(header):
            raise AssertionError("fixed-width DIMACS header changed length")
        handle.seek(0)
        handle.write(header)
    return new_clause_count


def indicator_layout(
    system: EquationSystem,
    indicator_last_variable: int,
) -> tuple[int, int]:
    indicator_count = len(system.colourings) * len(system.matchings)
    first = indicator_last_variable - indicator_count + 1
    if first <= 0:
        raise ValueError("invalid amplitude-indicator range")
    return first, indicator_count


def indicator_variable(
    first: int,
    matching_count: int,
    colouring_index: int,
    matching_index: int,
) -> int:
    return (
        first
        + colouring_index * matching_count
        + matching_index
    )


def violated_no_binomial_clauses(
    system: EquationSystem,
    positive: set[int],
    indicator_first: int,
) -> tuple[list[tuple[int, ...]], list[dict[str, object]]]:
    matching_count = len(system.matchings)
    clauses: list[tuple[int, ...]] = []
    records: list[dict[str, object]] = []
    for colouring_index, raw_colouring in enumerate(system.colourings):
        if system.target[colouring_index]:
            continue
        variables = tuple(
            indicator_variable(
                indicator_first,
                matching_count,
                colouring_index,
                matching_index,
            )
            for matching_index in range(matching_count)
        )
        active = [
            matching_index
            for matching_index, variable in enumerate(variables)
            if variable in positive
        ]
        if len(active) != 2:
            continue
        first_matching, second_matching = active
        first_variable = variables[first_matching]
        second_variable = variables[second_matching]
        clause = (
            -first_variable,
            -second_variable,
            *(
                variable
                for matching_index, variable in enumerate(variables)
                if matching_index not in active
            ),
        )
        clauses.append(clause)
        records.append(
            {
                "certificate_mode": "two_term_forbidden_amplitude",
                "colouring_index": colouring_index,
                "colouring": list(map(int, raw_colouring)),
                "matching_indices": active,
                "indicator_variables": [
                    first_variable,
                    second_variable,
                ],
            }
        )
    return clauses, records


def is_monomial_parallelogram(
    system: EquationSystem,
    colouring_index: int,
    matching_indices: Iterable[int],
) -> bool:
    matchings = list(map(int, matching_indices))
    if len(matchings) != 4:
        return False
    exponents = [
        Counter(
            map(
                int,
                system.variable_ids[
                    matching,
                    colouring_index,
                    :,
                ],
            )
        )
        for matching in matchings
    ]
    for first, second, opposite in (
        (1, 2, 3),
        (1, 3, 2),
        (2, 3, 1),
    ):
        if exponents[0] + exponents[opposite] == (
            exponents[first] + exponents[second]
        ):
            return True
    return False


def violated_factorable_four_clauses(
    system: EquationSystem,
    positive: set[int],
    indicator_first: int,
) -> tuple[list[tuple[int, ...]], list[dict[str, object]]]:
    """Exclude exact four-term Laurent parallelogram amplitudes."""
    matching_count = len(system.matchings)
    clauses: list[tuple[int, ...]] = []
    records: list[dict[str, object]] = []
    for colouring_index, raw_colouring in enumerate(system.colourings):
        if system.target[colouring_index]:
            continue
        variables = tuple(
            indicator_variable(
                indicator_first,
                matching_count,
                colouring_index,
                matching_index,
            )
            for matching_index in range(matching_count)
        )
        active = [
            matching_index
            for matching_index, variable in enumerate(variables)
            if variable in positive
        ]
        if not is_monomial_parallelogram(
            system,
            colouring_index,
            active,
        ):
            continue
        active_set = set(active)
        clause = (
            *(-variables[matching] for matching in active),
            *(
                variable
                for matching, variable in enumerate(variables)
                if matching not in active_set
            ),
        )
        clauses.append(clause)
        records.append(
            {
                "certificate_mode": "four_term_laurent_parallelogram",
                "colouring_index": colouring_index,
                "colouring": list(map(int, raw_colouring)),
                "matching_indices": active,
            }
        )
    return clauses, records


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--graph6", type=Path, required=True)
    parser.add_argument("--target-edges", type=int, required=True)
    parser.add_argument("--base-cnf", type=Path, required=True)
    parser.add_argument("--kissat", type=Path, required=True)
    parser.add_argument(
        "--indicator-last-variable",
        type=int,
        required=True,
        help=(
            "last amplitude-indicator variable in the original local CNF; "
            "later CNF augmentations may allocate variables after it"
        ),
    )
    parser.add_argument(
        "--configuration",
        choices=("default", "sat", "unsat"),
        default="sat",
    )
    parser.add_argument("--work-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--resume-manifest",
        action="append",
        type=Path,
        default=[],
        help=(
            "reconstruct previously learned no-binomial clauses from all "
            "SAT logs in an earlier run; may be repeated"
        ),
    )
    parser.add_argument(
        "--blocked-support-manifest",
        action="append",
        type=Path,
        default=[],
        help=(
            "factor-lattice manifest whose exact selected support should "
            "be blocked before continuing"
        ),
    )
    parser.add_argument(
        "--blocked-family-manifest",
        action="append",
        type=Path,
        default=[],
        help=(
            "enumerated double-C4/singleton family whose complete orbit "
            "of labelled entry supports should be blocked"
        ),
    )
    parser.add_argument(
        "--max-models",
        type=int,
        default=0,
        help="optional global SAT-model limit; zero means unlimited",
    )
    parser.add_argument(
        "--forbid-factorable-four",
        action="store_true",
        help=(
            "also explore the stronger relaxation with every exact "
            "four-term Laurent parallelogram forbidden"
        ),
    )
    args = parser.parse_args()

    started = time.perf_counter()
    system = EquationSystem(8, 3)
    indicator_first, indicator_count = indicator_layout(
        system, args.indicator_last_variable
    )
    base_variables, base_clauses = read_header(args.base_cnf)
    if args.indicator_last_variable > base_variables:
        raise ValueError("indicator range extends past the base CNF")

    roles, catalogue = canonical_normalized_killer_skeletons(
        args.graph6, target_edges=args.target_edges
    )
    ordered_roles = ordered_role_skeletons(roles)
    allowed = local_allowed_edges(center_degree=1)
    first_block_variable = 1 + 9 * len(allowed)

    learned: set[tuple[int, ...]] = set()
    resumed_logs = 0
    for resume_manifest in args.resume_manifest:
        resume_source = json.loads(
            resume_manifest.read_text(encoding="utf-8")
        )
        if (
            int(resume_source["indicator_first_variable"])
            != indicator_first
            or int(resume_source["indicator_last_variable"])
            != args.indicator_last_variable
        ):
            raise ValueError("resume manifest indicator layout changed")
        for row in resume_source["rows"]:
            for run in row["solver_runs"]:
                if run["status"] != "SAT":
                    continue
                log = Path(run["log"])
                if sha256(log) != run["log_sha256"]:
                    raise AssertionError(f"resume SAT log changed: {log}")
                positive = positive_model_literals(log)
                clauses, _records = violated_no_binomial_clauses(
                    system,
                    positive,
                    indicator_first,
                )
                if args.forbid_factorable_four:
                    factor_clauses, _factor_records = (
                        violated_factorable_four_clauses(
                            system,
                            positive,
                            indicator_first,
                        )
                    )
                    clauses.extend(factor_clauses)
                learned.update(clauses)
                resumed_logs += 1

    allowed_index = {
        edge: index for index, edge in enumerate(allowed)
    }
    support_blockers: list[tuple[int, ...]] = []

    def support_blocking_clause(
        selected_flat: set[int],
    ) -> tuple[int, ...]:
        clause: list[int] = []
        for edge in system.edges:
            local_edge = allowed_index.get(edge)
            global_edge = system.edge_index[edge]
            for row in range(system.d):
                for column in range(system.d):
                    flat = (
                        system.d**2 * global_edge
                        + system.d * row
                        + column
                    )
                    if local_edge is None:
                        if flat in selected_flat:
                            raise AssertionError(
                                "blocked support uses a structural-zero entry"
                            )
                        continue
                    variable = (
                        1
                        + system.d**2 * local_edge
                        + system.d * row
                        + column
                    )
                    clause.append(
                        -variable if flat in selected_flat else variable
                    )
        return tuple(clause)

    for manifest_path in args.blocked_support_manifest:
        source = json.loads(
            manifest_path.read_text(encoding="utf-8")
        )
        source_model = Path(source["model"])
        if sha256(source_model) != source["model_sha256"]:
            raise AssertionError(
                f"blocked-support source model changed: {source_model}"
            )
        selected_flat = set(
            map(int, source["selected_flat_indices"])
        )
        support_blockers.append(
            support_blocking_clause(selected_flat)
        )

    family_catalogues: list[
        tuple[
            frozenset[tuple[int, int]],
            tuple[tuple[int, ...], ...],
        ]
    ] = []
    for family_path in args.blocked_family_manifest:
        family = json.loads(family_path.read_text(encoding="utf-8"))
        family_catalogues.extend(
            expanded_family_catalogue(family, system)
        )

    family_support_blockers_by_role: list[
        tuple[tuple[int, ...], ...]
    ] = []
    for skeleton in ordered_roles:
        selected_supports = transported_family_supports(
            family_catalogues,
            frozenset(skeleton),
            system,
        )
        family_support_blockers_by_role.append(
            tuple(
                sorted(
                    support_blocking_clause(set(selected))
                    for selected in selected_supports
                )
            )
        )
    learned.update(support_blockers)

    args.work_dir.mkdir(parents=True, exist_ok=True)
    work_cnf = args.work_dir / "current_role_no_binomial.cnf"
    rows: list[dict[str, object]] = []
    witnesses: list[dict[str, object]] = []
    total_models = 0
    terminal_status = "complete"

    def payload(status: str) -> dict[str, object]:
        return {
            "status": status,
            "scope": (
                "n=8 normalized-killer support relaxation with no "
                "two-term forbidden amplitude"
            ),
            "necessary_conditions_only": True,
            "stronger_than_prize_hypothesis": True,
            "forbid_factorable_four": args.forbid_factorable_four,
            **catalogue,
            "target_edges": args.target_edges,
            "base_cnf": str(args.base_cnf),
            "base_cnf_sha256": sha256(args.base_cnf),
            "base_variables": base_variables,
            "base_clauses": base_clauses,
            "indicator_first_variable": indicator_first,
            "indicator_last_variable": args.indicator_last_variable,
            "indicator_count": indicator_count,
            "perfect_matchings": len(system.matchings),
            "colourings": len(system.colourings),
            "processed": len(rows),
            "support_models": total_models,
            "learned_no_binomial_clauses": len(learned),
            "resume_manifests": [
                str(path) for path in args.resume_manifest
            ],
            "resumed_sat_logs": resumed_logs,
            "blocked_support_manifests": [
                str(path) for path in args.blocked_support_manifest
            ],
            "blocked_family_manifests": [
                str(path) for path in args.blocked_family_manifest
            ],
            "blocked_family_manifest_sha256": [
                sha256(path) for path in args.blocked_family_manifest
            ],
            "family_support_blocking_clauses_by_role": [
                len(blockers)
                for blockers in family_support_blockers_by_role
            ],
            "family_support_blocking_clauses": sum(
                len(blockers)
                for blockers in family_support_blockers_by_role
            ),
            "support_blocking_clauses": (
                len(support_blockers)
                + sum(
                    len(blockers)
                    for blockers in family_support_blockers_by_role
                )
            ),
            "rows": rows,
            "witnesses": witnesses,
            "solve_seconds": time.perf_counter() - started,
        }

    for role_index, skeleton in enumerate(ordered_roles):
        present = set(skeleton)
        role_family_blockers = family_support_blockers_by_role[
            role_index
        ]
        units = [
            (
                first_block_variable + edge_index
                if edge in present
                else -(first_block_variable + edge_index)
            )
            for edge_index, edge in enumerate(allowed)
        ]
        clause_count = materialize_role(
            args.base_cnf,
            work_cnf,
            base_variables,
            base_clauses,
            [*sorted(learned), *role_family_blockers],
            units,
        )
        role_started = time.perf_counter()
        role_models = 0
        role_new_clauses = 0
        runs: list[dict[str, object]] = []
        role_status = "UNSAT"

        while True:
            run_index = len(runs)
            log = args.work_dir / (
                f"role_{role_index:04d}_run_{run_index:03d}.log"
            )
            stderr = log.with_suffix(".stderr.log")
            solver_status, elapsed = run_kissat(
                args.kissat,
                work_cnf,
                log,
                stderr,
                args.configuration,
            )
            run: dict[str, object] = {
                "run_index": run_index,
                "status": solver_status,
                "clauses": clause_count,
                "log": str(log),
                "log_sha256": sha256(log),
                "stderr": str(stderr),
                "stderr_sha256": sha256(stderr),
                "solve_seconds": elapsed,
            }
            runs.append(run)
            if solver_status == "UNSAT":
                break

            total_models += 1
            role_models += 1
            positive = positive_model_literals(log)
            clauses, records = violated_no_binomial_clauses(
                system, positive, indicator_first
            )
            if args.forbid_factorable_four:
                factor_clauses, factor_records = (
                    violated_factorable_four_clauses(
                        system,
                        positive,
                        indicator_first,
                    )
                )
                clauses.extend(factor_clauses)
                records.extend(factor_records)
            new_clauses = [
                clause for clause in clauses if clause not in learned
            ]
            run["violated_binomial_amplitudes"] = len(clauses)
            run["violated_low_factor_amplitudes"] = len(clauses)
            run["violated_two_term_amplitudes"] = sum(
                record["certificate_mode"]
                == "two_term_forbidden_amplitude"
                for record in records
            )
            run["violated_factorable_four_amplitudes"] = sum(
                record["certificate_mode"]
                == "four_term_laurent_parallelogram"
                for record in records
            )
            run["new_no_binomial_clauses"] = len(new_clauses)
            if not clauses:
                role_status = "NO_BINOMIAL_SUPPORT_FOUND"
                witnesses.append(
                    {
                        "role_index": role_index,
                        "skeleton_edges": [
                            list(edge) for edge in skeleton
                        ],
                        "log": str(log),
                        "log_sha256": sha256(log),
                        "positive_literals": sorted(positive),
                    }
                )
                terminal_status = "survivor"
                break
            if not new_clauses:
                raise AssertionError(
                    "SAT model violated only already-learned clauses"
                )
            learned.update(new_clauses)
            role_new_clauses += len(new_clauses)
            clause_count = append_clauses(
                work_cnf,
                base_variables,
                clause_count,
                new_clauses,
            )
            print(
                f"role={role_index + 1}/{len(ordered_roles)} "
                f"model={role_models} binomials={len(clauses)} "
                f"new={len(new_clauses)} learned={len(learned)}",
                flush=True,
            )
            if args.max_models and total_models >= args.max_models:
                role_status = "MODEL_LIMIT"
                terminal_status = "limit"
                break

        rows.append(
            {
                "role_index": role_index,
                "skeleton_edges": [list(edge) for edge in skeleton],
                "status": role_status,
                "support_models": role_models,
                "new_no_binomial_clauses": role_new_clauses,
                "family_support_blocking_clauses": len(
                    role_family_blockers
                ),
                "solver_runs": runs,
                "solve_seconds": time.perf_counter() - role_started,
            }
        )
        checkpoint(args.output, payload("running"))
        print(
            f"processed={role_index + 1}/{len(ordered_roles)} "
            f"status={role_status} models={total_models} "
            f"learned={len(learned)}",
            flush=True,
        )
        if role_status in {
            "NO_BINOMIAL_SUPPORT_FOUND",
            "MODEL_LIMIT",
        }:
            break

    result = payload(terminal_status)
    checkpoint(args.output, result)
    print(
        f"{terminal_status} processed={len(rows)}/{len(ordered_roles)} "
        f"models={total_models} learned={len(learned)}",
        flush=True,
    )


if __name__ == "__main__":
    main()
