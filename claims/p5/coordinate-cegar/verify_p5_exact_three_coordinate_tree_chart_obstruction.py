#!/usr/bin/env python3
"""Verify the packaged exact-three-coordinate P5 tree-chart theorem."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import itertools
import json
import shutil
import subprocess
import sys
import tempfile
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from pysat.solvers import Solver

for _p in Path(__file__).resolve().parents:
    if (_p / "src" / "krenn_gu" / "bootstrap.py").exists():
        sys.path.insert(0, str(_p / "src"))
        break
from krenn_gu.bootstrap import bootstrap, expose_claim_package  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__, also=["."])
expose_claim_package(REPO_ROOT, "claims/p5/boundaries")

import audit_p5_all_full_boundary_obstruction as ALL_FULL
from krenn_gu import p5_support_system as GENERATOR
from krenn_gu.p5_split_saturation import convert_text
from krenn_gu import p5_pair_support_semantics as SEMANTICS
import p5_tree_chart_cover as COVER


ROOT = Path(__file__).resolve().parent
PACKAGE = (
    REPO_ROOT
    / "research_snapshots"
    / "2026-07-27-p5-tree-chart-cover"
)
EXPECTED_MANIFEST_SHA256 = (
    "08aa37b99d5e66c28a15ea13c124d02c556dc3c64b4b975783a8d1980612d97d"
)
EXPECTED = {
    "c10": {
        "backbones": 127,
        "charts": 401,
        "direct": 399,
        "split": 2,
        "variables": 100254,
        "clauses": 1293318,
        "cnf_sha256": (
            "70cfd3cc8046bea6eec2e312f3deb98c108e7854cc8f999bcb0438d7112a5537"
        ),
        "proof_sha256": (
            "0b6c5b4b4f756ff7cc9520627e2c3f64f42ff49d4a6fe41ba09334901b079287"
        ),
    },
    "c4c6": {
        "backbones": 73,
        "charts": 411,
        "direct": 399,
        "split": 12,
        "variables": 107898,
        "clauses": 1323652,
        "cnf_sha256": (
            "b80d7560e1522e7f5133b20490de79b10290bc515bd460aff7da8dbcb01220d0"
        ),
        "proof_sha256": (
            "1d660717418d218a90d390c1ae1438db71b7bf4e3460e6962203614d519abe2e"
        ),
    },
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def gzip_raw_descriptor(path: Path) -> tuple[int, str]:
    digest = hashlib.sha256()
    size = 0
    with gzip.open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            size += len(chunk)
            digest.update(chunk)
    return size, digest.hexdigest()


def wsl_path(path: Path) -> str:
    resolved = path.resolve()
    drive = resolved.drive.rstrip(":").lower()
    return (
        f"/mnt/{drive}/"
        + str(resolved)[len(resolved.drive) :]
        .lstrip("\\/")
        .replace("\\", "/")
    )


def validate_file(path: Path, descriptor: dict) -> None:
    if (
        str(path.relative_to(PACKAGE)) != descriptor["path"]
        or path.stat().st_size != descriptor["bytes"]
        or sha256(path) != descriptor["sha256"]
    ):
        raise AssertionError(f"packaged file changed: {path.name}")


def canonical_backbone_audit(
    shape: str,
    records: list[dict],
) -> int:
    group = ALL_FULL.automorphisms(ALL_FULL.full_edges(shape))
    observed = set()
    for record in records:
        supports = tuple(
            tuple(row) for row in record["coordinate_supports"]
        )
        pattern = ALL_FULL.support_pattern(supports)
        if ALL_FULL.canonical(pattern, group) != pattern:
            raise AssertionError("stored backbone is not canonical")
        observed.add(pattern)
    return len(observed)


def validate_chart(
    shape: str,
    record: dict,
    catalogue: tuple[tuple, ...],
) -> tuple[str, str, dict]:
    supports = tuple(
        tuple(row) for row in record["coordinate_supports"]
    )
    fixed = COVER.coordinate_edges(supports)
    if fixed != tuple(
        tuple(edge) for edge in record["coordinate_entries"]
    ):
        raise AssertionError("coordinate entries changed")
    connectors = tuple(
        tuple(edge) for edge in record["connector_entries"]
    )
    tree = tuple(tuple(edge) for edge in record["gauge_tree"])
    if tuple(
        edge
        for edge in tree
        if supports[edge[0]][edge[1]] == 7
    ) != connectors:
        raise AssertionError("connector/tree binding changed")
    indices = tuple(record["signature_indices"])
    signatures = tuple(catalogue[index] for index in indices)
    for mode, signature in enumerate(signatures):
        for source, backbone_mask in enumerate(supports[mode]):
            signature_mask = signature[0][source]
            if (
                signature_mask != backbone_mask
                if backbone_mask in (1, 2, 4)
                else signature_mask in (1, 2, 4)
            ):
                raise AssertionError(
                    "signature witness does not refine the backbone"
                )
    if not all(
        sum(
            bool(
                signatures[mode][1][pair_index]
                & (1 << colour)
            )
            for mode in SEMANTICS.MODES
        )
        >= 2
        for pair_index in range(10)
        for colour in SEMANTICS.COLOURS
    ):
        raise AssertionError("signature witness misses a pair quota")

    program, metadata = GENERATOR.generate(
        supports,
        indices,
        expected_partial_cells=0,
        pure_saturation_only=True,
        gauge_tree_edges=tree,
    )
    source_data = program.encode("utf-8")
    source_sha = sha256_bytes(source_data)
    if (
        source_sha != record["source_sha256"]
        or len(source_data) != record["source_bytes"]
        or metadata != record["metadata"]
        or metadata
        != {
            "nonzero_entries": 45,
            "gauge_free_variables": 26,
            "laurent_parameters": 26,
            "saturated_parameters": 0,
            "mixed_equations": 240,
            "pure_coefficients": 3,
        }
    ):
        raise AssertionError("Singular chart reconstruction changed")
    certificate_kind = record["certificate_kind"]
    if certificate_kind == "split":
        split_program = convert_text(program)
        split_sha = sha256_bytes(split_program.encode("utf-8"))
        if split_sha != record["split_source_sha256"]:
            raise AssertionError("split source reconstruction changed")
    elif certificate_kind == "direct":
        split_program = ""
        if record["split_source_sha256"] is not None:
            raise AssertionError("direct chart unexpectedly stores split hash")
    else:
        raise AssertionError("unknown chart certificate kind")
    return program, split_program, metadata


def rerun_singular(task: tuple, timeout: int) -> dict:
    shape, record, program, split_program = task
    selected = (
        split_program
        if record["certificate_kind"] == "split"
        else program
    )
    started = time.monotonic()
    try:
        result = subprocess.run(
            [
                "wsl.exe",
                "--exec",
                "/usr/bin/Singular",
                "-q",
            ],
            input=selected,
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
            cwd=ROOT,
        )
    except subprocess.TimeoutExpired:
        return {
            "shape": shape,
            "backbone_orbit_index": record[
                "backbone_orbit_index"
            ],
            "chart_index": record["chart_index"],
            "verified": False,
            "status": "TIMEOUT",
            "seconds": round(time.monotonic() - started, 3),
        }
    verified = (
        result.returncode == 0
        and not result.stderr.strip()
        and result.stdout.strip() == "UNIT_IDEAL"
    )
    return {
        "shape": shape,
        "backbone_orbit_index": record["backbone_orbit_index"],
        "chart_index": record["chart_index"],
        "verified": verified,
        "status": "UNIT_IDEAL" if verified else "FAILED",
        "seconds": round(time.monotonic() - started, 3),
    }


def rerun_drat(
    drat_trim: Path,
    cnf_gzip: Path,
    proof_gzip: Path,
    timeout: int,
) -> dict:
    with tempfile.TemporaryDirectory(prefix="p5_tree_drat_") as raw:
        temporary = Path(raw)
        cnf = temporary / "cover.cnf"
        proof = temporary / "cover.drat"
        with gzip.open(cnf_gzip, "rb") as source, cnf.open(
            "wb"
        ) as destination:
            shutil.copyfileobj(source, destination, 1 << 20)
        with gzip.open(proof_gzip, "rb") as source, proof.open(
            "wb"
        ) as destination:
            shutil.copyfileobj(source, destination, 1 << 20)
        started = time.monotonic()
        result = subprocess.run(
            [
                "wsl.exe",
                "--exec",
                wsl_path(drat_trim),
                wsl_path(cnf),
                wsl_path(proof),
                "-w",
            ],
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
            cwd=ROOT,
        )
        return {
            "verified": (
                result.returncode == 0
                and "s VERIFIED" in result.stdout
            ),
            "returncode": result.returncode,
            "seconds": round(time.monotonic() - started, 3),
            "stdout_tail": result.stdout.splitlines()[-4:],
            "stderr": result.stderr.strip(),
        }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rerun-singular", action="store_true")
    parser.add_argument("--jobs", type=int, default=4)
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--step", type=int, default=1)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--singular-timeout", type=int, default=60)
    parser.add_argument("--rerun-drat", action="store_true")
    parser.add_argument(
        "--drat-trim",
        type=Path,
        default=ROOT / "tmp" / "drat-trim" / "drat-trim",
    )
    parser.add_argument("--drat-timeout", type=int, default=1800)
    args = parser.parse_args()
    if (
        args.jobs <= 0
        or args.start < 0
        or args.step <= 0
        or args.singular_timeout <= 0
        or args.drat_timeout <= 0
    ):
        raise ValueError("invalid replay arguments")

    manifest_path = PACKAGE / "manifest.json"
    if sha256(manifest_path) != EXPECTED_MANIFEST_SHA256:
        raise AssertionError("packaged manifest hash changed")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if (
        manifest.get("status") != "EXACT_FINITE_BRANCH_THEOREM"
        or manifest.get("global_conjecture_resolved") is not False
        or manifest.get("higher_coordinate_p5_branch_resolved")
        is not False
        or manifest.get("core_charts") != 812
    ):
        raise AssertionError("manifest scope or status changed")

    replay_descriptor = manifest["fresh_singular_replay"]
    replay_path = PACKAGE / replay_descriptor["path"]
    validate_file(replay_path, replay_descriptor)
    replay = json.loads(replay_path.read_text(encoding="utf-8"))
    if (
        replay.get("verified") is not True
        or replay.get("charts") != 812
        or replay.get("counts") != {"UNIT_IDEAL": 812}
    ):
        raise AssertionError("recorded fresh Singular replay changed")
    replay_keys = {
        (
            item["shape"],
            item["backbone_orbit_index"],
            item["chart_index"],
        )
        for item in replay["results"]
        if item.get("verified") is True
    }
    if len(replay_keys) != 812:
        raise AssertionError("recorded replay key set changed")

    catalogue = SEMANTICS.finite_field_local_signatures()
    all_tasks = []
    shape_results = {}
    for shape, expected in EXPECTED.items():
        descriptor = manifest["shapes"][shape]
        if (
            descriptor["backbones"] != expected["backbones"]
            or descriptor["core_charts"] != expected["charts"]
            or descriptor["direct_unit_ideals"] != expected["direct"]
            or descriptor["split_unit_ideals"] != expected["split"]
            or descriptor["cnf_variables"] != expected["variables"]
            or descriptor["cnf_clauses"] != expected["clauses"]
            or descriptor["cnf_raw_sha256"] != expected["cnf_sha256"]
            or descriptor["proof_raw_sha256"]
            != expected["proof_sha256"]
        ):
            raise AssertionError(f"{shape} manifest counts changed")
        files = descriptor["files"]
        for file_descriptor in files.values():
            validate_file(
                PACKAGE / file_descriptor["path"],
                file_descriptor,
            )
        if "s VERIFIED" not in (
            PACKAGE / files["drat_log"]["path"]
        ).read_text(encoding="utf-8"):
            raise AssertionError("packaged DRAT replay log changed")
        cnf_gzip = PACKAGE / files["cnf_gzip"]["path"]
        proof_gzip = PACKAGE / files["proof_gzip"]["path"]
        cnf_raw = gzip_raw_descriptor(cnf_gzip)
        proof_raw = gzip_raw_descriptor(proof_gzip)
        if cnf_raw != (
            descriptor["cnf_raw_bytes"],
            expected["cnf_sha256"],
        ) or proof_raw != (
            descriptor["proof_raw_bytes"],
            expected["proof_sha256"],
        ):
            raise AssertionError("compressed proof artifact changed")

        core_path = PACKAGE / files["core"]["path"]
        core = json.loads(core_path.read_text(encoding="utf-8"))
        records = core["records"]
        if (
            core.get("status") != "EXACT_RATIONAL_UNIT_CHART_CORE"
            or len(records) != expected["charts"]
            or core.get("backbones") != expected["backbones"]
        ):
            raise AssertionError(f"{shape} chart core changed")
        if canonical_backbone_audit(shape, records) != expected[
            "backbones"
        ]:
            raise AssertionError("canonical backbone coverage changed")

        kinds = Counter()
        for record in records:
            program, split_program, _metadata = validate_chart(
                shape,
                record,
                catalogue,
            )
            key = (
                shape,
                record["backbone_orbit_index"],
                record["chart_index"],
            )
            if key not in replay_keys:
                raise AssertionError("chart missing from fresh replay")
            kinds[record["certificate_kind"]] += 1
            all_tasks.append(
                (shape, record, program, split_program)
            )
        if kinds != Counter(
            {"direct": expected["direct"], "split": expected["split"]}
        ):
            raise AssertionError("chart certificate histogram changed")

        cnf, pool, metadata = COVER.build_cover_cnf(shape, records)
        if (
            pool.top != expected["variables"]
            or len(cnf.clauses) != expected["clauses"]
        ):
            raise AssertionError("reconstructed CNF dimensions changed")
        with tempfile.NamedTemporaryFile(
            prefix=f"p5_{shape}_",
            suffix=".cnf",
            delete=False,
        ) as handle:
            cnf_path = Path(handle.name)
        try:
            cnf.to_file(cnf_path)
            cnf_hash = sha256(cnf_path)
            cnf_bytes = cnf_path.stat().st_size
        finally:
            cnf_path.unlink()
        if (
            cnf_hash != expected["cnf_sha256"]
            or cnf_bytes != descriptor["cnf_raw_bytes"]
        ):
            raise AssertionError("reconstructed CNF bytes changed")
        solver_results = {}
        for solver_name in ("cadical195", "glucose4"):
            with Solver(
                name=solver_name,
                bootstrap_with=cnf.clauses,
            ) as solver:
                solver_results[solver_name] = not solver.solve()
        if not all(solver_results.values()):
            raise AssertionError("independent SAT replay found a model")
        drat_result = None
        if args.rerun_drat:
            if not args.drat_trim.is_file():
                raise FileNotFoundError(args.drat_trim)
            drat_result = rerun_drat(
                args.drat_trim,
                cnf_gzip,
                proof_gzip,
                args.drat_timeout,
            )
            if not drat_result["verified"]:
                raise AssertionError("fresh DRAT replay failed")
        shape_results[shape] = {
            "backbones": expected["backbones"],
            "charts": expected["charts"],
            "cnf_sha256": cnf_hash,
            "cnf_metadata": metadata,
            "solver_results": solver_results,
            "fresh_drat_replay": drat_result,
        }

    if len(all_tasks) != 812:
        raise AssertionError("total chart count changed")
    singular_results = []
    if args.rerun_singular:
        selected = all_tasks[args.start :: args.step]
        if args.limit is not None:
            selected = selected[: args.limit]
        with ThreadPoolExecutor(max_workers=args.jobs) as executor:
            singular_results = list(
                executor.map(
                    lambda task: rerun_singular(
                        task, args.singular_timeout
                    ),
                    selected,
                )
            )
        if not all(item["verified"] for item in singular_results):
            raise AssertionError("fresh Singular replay failed")

    print(
        json.dumps(
            {
                "verified": True,
                "scope": manifest["scope"],
                "conclusion": manifest["conclusion"],
                "catalogue_pair_signatures": len(catalogue),
                "coordinate_backbone_orbits": 200,
                "regenerated_chart_sources": len(all_tasks),
                "recorded_fresh_unit_ideals": len(replay_keys),
                "fresh_singular_reruns": len(singular_results),
                "fresh_singular_counts": dict(
                    Counter(
                        item["status"] for item in singular_results
                    )
                ),
                "fresh_drat_replays": sum(
                    result["fresh_drat_replay"] is not None
                    for result in shape_results.values()
                ),
                "shapes": shape_results,
                "higher_coordinate_p5_branch_resolved": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
