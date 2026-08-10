"""Independently audit exact Singular fallback certificates.

The fallback generator starts from a SAT support stratum, restricts the
original amplitude equations to its torus, eliminates a unimodular basis of
binomials, and writes a saturated Singular program.  The clause learner then
blocks the whole support after Singular proves that the saturated ideal is
the unit ideal.

This verifier repeats those transformations from the original batch and
amplitude equations.  It checks the generated program byte-for-byte, checks
the Singular terminal and empty stderr, reconstructs every symmetry image of
the full-support no-good, and checks the learned CNF as an exact prefix plus
tail extension.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

from eight_vertex_degree4_cegar import (
    full_equations,
    symmetry_clauses,
)
from eight_vertex_sparse_exact import (
    exact_equations,
    local_allowed_edges,
    singular_program,
)
from learn_singular_fallback_clauses import singular_unit
from prism_laurent_reduction import primitive_binomial_reduction
from search_witness import EquationSystem
import sys

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)

from krenn_gu.verify_laurent_batch_manifest import audit_cnf


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def allowed_flat_indices(
    system: EquationSystem, center_degree: int
) -> set[int]:
    return {
        9 * system.edge_index[edge] + 3 * row + column
        for edge in local_allowed_edges(center_degree)
        for row in range(3)
        for column in range(3)
    }


def wsl_path(path: Path) -> str:
    resolved = str(path.resolve())
    if len(resolved) < 3 or resolved[1:3] != ":\\":
        raise ValueError(f"cannot map path into WSL: {resolved}")
    return (
        f"/mnt/{resolved[0].lower()}/"
        + resolved[3:].replace("\\", "/")
    )


def require_equal(
    recorded: dict[str, object],
    expected: dict[str, object],
    keys: tuple[str, ...],
    context: str,
) -> None:
    for key in keys:
        if recorded.get(key) != expected.get(key):
            raise AssertionError(
                f"{context} field changed: {key}: "
                f"{recorded.get(key)!r} != {expected.get(key)!r}"
            )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--fallback-manifest", type=Path, required=True
    )
    parser.add_argument(
        "--learned-manifest", type=Path, required=True
    )
    parser.add_argument(
        "--rerun-singular-wsl",
        action="store_true",
        help="rerun every generated source with Singular under WSL",
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    fallback = json.loads(
        args.fallback_manifest.read_text(encoding="utf-8")
    )
    learned = json.loads(
        args.learned_manifest.read_text(encoding="utf-8")
    )
    batch_path = Path(str(fallback["batch"]))
    batch = json.loads(batch_path.read_text(encoding="utf-8"))
    if sha256(batch_path) != fallback["batch_sha256"]:
        raise AssertionError("fallback batch hash mismatch")

    center_degree = int(fallback["center_degree"])
    target_edges = fallback.get("target_edges")
    characteristic = int(fallback["characteristic"])
    if int(batch.get("center_degree", 4)) != center_degree:
        raise AssertionError("batch and fallback center degrees differ")
    if batch.get("target_edges") != target_edges:
        raise AssertionError("batch and fallback edge counts differ")

    fallback_rows: list[
        tuple[dict[str, object], dict[str, object]]
    ] = []
    for row in batch["rows"]:
        if "fallback" in row:
            fallback_rows.append((row, row["fallback"]))
        for row_fallback in row.get("fallbacks", []):
            fallback_rows.append((row, row_fallback))
    programs = list(fallback["programs"])
    if (
        int(fallback["fallbacks"]),
        int(batch["fallback_count"]),
        len(fallback_rows),
        len(programs),
    ) != (len(programs),) * 4:
        raise AssertionError("fallback counts are inconsistent")

    system = EquationSystem(8, 3)
    full, flat_names, _ = full_equations(system)
    allowed = allowed_flat_indices(system, center_degree)
    clause_union: set[tuple[int, ...]] = set()
    expected_certificates: list[dict[str, object]] = []

    for fallback_index, ((row, row_fallback), recorded) in enumerate(
        zip(fallback_rows, programs, strict=True)
    ):
        selected = tuple(
            map(int, row_fallback["selected_flat_indices"])
        )
        if selected != tuple(sorted(set(selected))):
            raise AssertionError(
                "batch fallback support is not canonical"
            )
        if not set(selected) <= allowed:
            raise AssertionError(
                "batch fallback selects a structural zero"
            )
        if (
            int(recorded["fallback_index"]) != fallback_index
            or int(recorded["role_index"]) != int(row["role_index"])
            or recorded["skeleton_edges"] != row["skeleton_edges"]
            or list(map(int, recorded["selected_flat_indices"]))
            != list(selected)
            or int(recorded["selected_entries"]) != len(selected)
        ):
            raise AssertionError(
                f"fallback {fallback_index} no longer matches its batch row"
            )

        input_names = [flat_names[index] for index in selected]
        mode = str(recorded["mode"])
        if mode == "raw":
            names = [f"x{index}" for index in range(len(selected))]
            variable_names = dict(
                zip(selected, names, strict=True)
            )
            equations = exact_equations(system, variable_names)
            expected_metadata: dict[str, object] = {
                "mode": "raw",
                "restricted_equations": len(equations),
                "binomial_equations": None,
                "binomial_rank": None,
            }
            metadata_keys = (
                "mode",
                "restricted_equations",
                "binomial_equations",
                "binomial_rank",
            )
        elif mode == "unimodular_laurent":
            nonzero_names = set(input_names)
            restricted = []
            for polynomial in full:
                surviving = type(polynomial)(
                    {
                        monomial: coefficient
                        for monomial, coefficient in polynomial.items()
                        if all(
                            variable in nonzero_names
                            for variable in monomial
                        )
                    }
                )
                if surviving:
                    restricted.append(surviving)
            names, equations, metadata = primitive_binomial_reduction(
                restricted, input_names
            )
            if metadata["unit_equation_indices"]:
                raise AssertionError(
                    "fallback has an immediate Laurent-unit conflict"
                )
            expected_metadata = {
                "mode": "unimodular_laurent",
                "restricted_equations": len(restricted),
                "binomial_equations": metadata[
                    "binomial_equations"
                ],
                "binomial_rank": metadata["binomial_rank"],
                "unimodular_determinant": metadata[
                    "unimodular_determinant"
                ],
                "free_laurent_variables": metadata[
                    "free_laurent_variables"
                ],
                "active_polynomial_variables": metadata[
                    "active_polynomial_variables"
                ],
                "identically_eliminated_equations": metadata[
                    "identically_eliminated_equations"
                ],
            }
            metadata_keys = tuple(expected_metadata)
        else:
            raise AssertionError(f"unknown fallback mode: {mode}")
        require_equal(
            recorded,
            expected_metadata,
            metadata_keys,
            f"fallback {fallback_index}",
        )

        expected_program = singular_program(
            names, equations, characteristic
        )
        program_path = Path(str(recorded["program"]))
        if (
            int(recorded["output_variables"]) != len(names)
            or int(recorded["output_equations"]) != len(equations)
        ):
            raise AssertionError(
                f"fallback {fallback_index} output dimensions changed"
            )
        if program_path.read_text(encoding="utf-8") != expected_program:
            raise AssertionError(
                f"fallback {fallback_index} Singular source changed"
            )
        if sha256(program_path) != recorded["program_sha256"]:
            raise AssertionError(
                f"fallback {fallback_index} program hash mismatch"
            )

        log_path = program_path.with_suffix(".log")
        stderr_path = program_path.with_suffix(".stderr.log")
        log = log_path.read_text(encoding="utf-8")
        stderr = stderr_path.read_text(encoding="utf-8")
        if stderr.strip():
            raise AssertionError(
                f"Singular wrote errors for fallback {fallback_index}"
            )
        if not singular_unit(log):
            raise AssertionError(
                f"Singular unit terminal missing for fallback "
                f"{fallback_index}"
            )
        if args.rerun_singular_wsl:
            rerun = subprocess.run(
                [
                    "wsl.exe",
                    "-d",
                    "Ubuntu",
                    "--",
                    "bash",
                    "--noprofile",
                    "--norc",
                    "-lc",
                    f"Singular -q '{wsl_path(program_path)}'",
                ],
                check=False,
                capture_output=True,
            )
            rerun_log = rerun.stdout.decode(
                "utf-8", errors="strict"
            )
            rerun_stderr = rerun.stderr.decode(
                "utf-8", errors="strict"
            )
            if rerun.returncode or rerun_stderr.strip():
                raise AssertionError(
                    f"Singular rerun failed for fallback "
                    f"{fallback_index}"
                )
            if not singular_unit(rerun_log):
                raise AssertionError(
                    f"Singular rerun did not reproduce the unit ideal "
                    f"for fallback {fallback_index}"
                )

        images = symmetry_clauses(
            system,
            set(selected),
            allowed - set(selected),
            center_degree=center_degree,
        )
        clause_union.update(images)
        expected_certificates.append(
            {
                "fallback_index": fallback_index,
                "role_index": int(row["role_index"]),
                "program": str(program_path),
                "program_sha256": sha256(program_path),
                "log": str(log_path),
                "log_sha256": sha256(log_path),
                "stderr": str(stderr_path),
                "stderr_sha256": sha256(stderr_path),
                "selected_entries": len(selected),
                "zero_entries": len(allowed - set(selected)),
                "symmetry_images": len(images),
            }
        )

    if (
        learned["fallback_manifest"]
        != str(args.fallback_manifest)
        or learned["fallback_manifest_sha256"]
        != sha256(args.fallback_manifest)
    ):
        raise AssertionError("learned manifest points to another fallback")
    if int(learned["center_degree"]) != center_degree:
        raise AssertionError("learned manifest center degree changed")
    if learned["certificates"] != expected_certificates:
        raise AssertionError(
            "learned Singular certificate records changed"
        )

    ordered_clauses = sorted(clause_union)
    recorded_clauses = [
        tuple(map(int, clause))
        for clause in learned["learned_clauses"]
    ]
    if (
        int(learned["distinct_learned_clauses"])
        != len(ordered_clauses)
        or recorded_clauses != ordered_clauses
    ):
        raise AssertionError("learned support clause union changed")

    base_cnf = Path(str(learned["base_cnf"]))
    output_cnf = Path(str(learned["output_cnf"]))
    if sha256(base_cnf) != learned["base_cnf_sha256"]:
        raise AssertionError("Singular-clause base CNF hash mismatch")
    if sha256(output_cnf) != learned["output_cnf_sha256"]:
        raise AssertionError("Singular-clause output CNF hash mismatch")
    audit_cnf(base_cnf, output_cnf, ordered_clauses)

    payload = {
        "verified": True,
        "center_degree": center_degree,
        "target_edges": target_edges,
        "fallbacks": len(programs),
        "singular_unit_ideals": len(programs),
        "singular_rerun": args.rerun_singular_wsl,
        "learned_clauses": len(ordered_clauses),
        "batch_sha256": fallback["batch_sha256"],
        "fallback_manifest_sha256": sha256(
            args.fallback_manifest
        ),
        "base_cnf_sha256": learned["base_cnf_sha256"],
        "output_cnf_sha256": learned["output_cnf_sha256"],
    }
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(payload, indent=2) + "\n",
            encoding="utf-8",
        )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
