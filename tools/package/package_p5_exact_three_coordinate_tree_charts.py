"""Package the verified exact-three-coordinate P5 tree-chart theorem."""

from __future__ import annotations

import gzip
import hashlib
import json
import shutil
from pathlib import Path

import sys

for _parent in Path(__file__).resolve().parents:
    if (_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        sys.path.insert(0, str(_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap, expose_claim_package  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)
expose_claim_package(REPO_ROOT, "claims/p5/coordinate-cegar")

from krenn_gu import p5_support_system as GENERATOR
from krenn_gu.p5_split_saturation import convert_text
from p5_tree_chart_cover import coordinate_edges


ROOT = Path(__file__).resolve().parent
TMP = REPO_ROOT / 'tmp'
DESTINATION = (
    REPO_ROOT / 'research_snapshots/2026-07-27-p5-tree-chart-cover'
)
SHAPE_INPUTS = {
    "c10": {
        "cegar": TMP / "p5_c10_tree_cegar_full.json",
        "cover": TMP / "p5_c10_tree_chart_canonical_cover.json",
        "cnf": TMP / "p5_c10_tree_chart_canonical_cover.cnf",
        "proof": TMP / "p5_c10_tree_chart_canonical_cover.drat",
        "kissat": TMP / "p5_c10_tree_chart_kissat.json",
        "drat": TMP / "p5_c10_tree_chart_drat_trim_backward.json",
        "drat_stdout": (
            TMP / "p5_c10_tree_chart_drat_trim_backward.stdout"
        ),
        "expected_backbones": 127,
        "expected_charts": 401,
    },
    "c4c6": {
        "cegar": TMP / "p5_c4c6_tree_cegar_full.json",
        "cover": TMP / "p5_c4c6_tree_chart_canonical_cover.json",
        "cnf": TMP / "p5_c4c6_tree_chart_canonical_cover.cnf",
        "proof": TMP / "p5_c4c6_tree_chart_canonical_cover.drat",
        "kissat": TMP / "p5_c4c6_tree_chart_kissat.json",
        "drat": TMP / "p5_c4c6_tree_chart_drat_trim_backward.json",
        "drat_stdout": (
            TMP / "p5_c4c6_tree_chart_drat_trim_backward.stdout"
        ),
        "expected_backbones": 73,
        "expected_charts": 411,
    },
}
FRESH_REPLAY = TMP / "p5_tree_chart_core_fresh_replay.json"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def deterministic_gzip(source: Path, destination: Path) -> None:
    with source.open("rb") as input_handle, destination.open(
        "wb"
    ) as raw_output:
        with gzip.GzipFile(
            filename="",
            mode="wb",
            fileobj=raw_output,
            compresslevel=9,
            mtime=0,
        ) as output_handle:
            shutil.copyfileobj(input_handle, output_handle, 1 << 20)


def selected_core_charts(result: dict) -> list[dict]:
    units = [
        chart
        for chart in result["charts"]
        if chart["cas"]["unit_ideal"]
        or (
            chart.get("split_cas") is not None
            and chart["split_cas"]["unit_ideal"]
        )
    ]
    if "learned_chart_indices" in result:
        by_index = {
            chart["chart_index"]: chart
            for chart in result["charts"]
        }
        return [
            by_index[index] for index in result["core_chart_indices"]
        ]
    return [units[index] for index in result["core_chart_indices"]]


def file_descriptor(path: Path) -> dict:
    return {
        "path": str(path.relative_to(DESTINATION)),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def main() -> None:
    fresh = json.loads(FRESH_REPLAY.read_text(encoding="utf-8"))
    if (
        fresh.get("verified") is not True
        or fresh.get("status") != "COMPLETE"
        or fresh.get("charts") != 812
        or fresh.get("counts") != {"UNIT_IDEAL": 812}
    ):
        raise AssertionError("fresh Singular replay is incomplete")
    fresh_by_key = {
        (
            item["shape"],
            item["backbone_orbit_index"],
            item["chart_index"],
        ): item
        for item in fresh["results"]
    }
    if len(fresh_by_key) != 812:
        raise AssertionError("fresh replay repeats a chart")

    DESTINATION.mkdir(parents=True, exist_ok=True)
    shape_manifests = {}
    used_fresh_keys = set()
    for shape, descriptor in SHAPE_INPUTS.items():
        cegar = json.loads(
            descriptor["cegar"].read_text(encoding="utf-8")
        )
        cover = json.loads(
            descriptor["cover"].read_text(encoding="utf-8")
        )
        kissat = json.loads(
            descriptor["kissat"].read_text(encoding="utf-8")
        )
        drat = json.loads(
            descriptor["drat"].read_text(encoding="utf-8")
        )
        if (
            cegar.get("status") != "COMPLETE"
            or cegar.get("completed_backbones")
            != descriptor["expected_backbones"]
            or cegar.get("counts")
            != {"UNSAT_COVER": descriptor["expected_backbones"]}
            or cover.get("verified") is not True
            or cover.get("status") != "UNSAT"
            or cover.get("core_charts") != descriptor["expected_charts"]
            or kissat.get("status") != "UNSAT"
            or drat.get("verified") is not True
        ):
            raise AssertionError(f"{shape} proof chain is incomplete")
        if (
            cover["cnf_sha256"] != sha256(descriptor["cnf"])
            or kissat["cnf_sha256"] != cover["cnf_sha256"]
            or drat["cnf_sha256"] != cover["cnf_sha256"]
            or kissat["proof_sha256"] != sha256(descriptor["proof"])
            or drat["proof_sha256"] != kissat["proof_sha256"]
            or "s VERIFIED"
            not in descriptor["drat_stdout"].read_text(
                encoding="utf-8"
            )
        ):
            raise AssertionError(f"{shape} proof hashes do not bind")

        records = []
        direct = 0
        split = 0
        for result in cegar["results"]:
            if result.get("status") != "UNSAT_COVER":
                raise AssertionError("uncovered backbone in CEGAR result")
            supports = tuple(
                tuple(row) for row in result["coordinate_supports"]
            )
            fixed = coordinate_edges(supports)
            for chart in selected_core_charts(result):
                key = (
                    shape,
                    result["orbit_index"],
                    chart["chart_index"],
                )
                replay = fresh_by_key.get(key)
                if replay is None or replay.get("verified") is not True:
                    raise AssertionError("chart lacks a fresh replay")
                used_fresh_keys.add(key)
                tree = tuple(
                    tuple(edge) for edge in chart["gauge_tree"]
                )
                indices = tuple(chart["signature_indices"])
                program, metadata = GENERATOR.generate(
                    supports,
                    indices,
                    expected_partial_cells=0,
                    pure_saturation_only=True,
                    gauge_tree_edges=tree,
                )
                source_sha = sha256_bytes(program.encode("utf-8"))
                if (
                    source_sha != chart["source_sha256"]
                    or metadata != chart["metadata"]
                    or replay["source_sha256"] != source_sha
                ):
                    raise AssertionError("chart reconstruction changed")
                direct_unit = chart["cas"]["unit_ideal"]
                split_unit = (
                    chart.get("split_cas") is not None
                    and chart["split_cas"]["unit_ideal"]
                )
                if not (direct_unit or split_unit):
                    raise AssertionError("core chart is not a unit ideal")
                split_sha = None
                if not direct_unit:
                    split_program = convert_text(program)
                    split_sha = sha256_bytes(
                        split_program.encode("utf-8")
                    )
                    if split_sha != chart["split_cas"]["source_sha256"]:
                        raise AssertionError(
                            "split chart reconstruction changed"
                        )
                    split += 1
                else:
                    direct += 1
                connectors = tuple(
                    tuple(edge) for edge in chart["connector_edges"]
                )
                records.append(
                    {
                        "shape": shape,
                        "backbone_orbit_index": result["orbit_index"],
                        "coordinate_supports": supports,
                        "coordinate_entries": fixed,
                        "chart_index": chart["chart_index"],
                        "gauge_tree": tree,
                        "connector_entries": connectors,
                        "signature_indices": indices,
                        "source_sha256": source_sha,
                        "source_bytes": len(program.encode("utf-8")),
                        "split_source_sha256": split_sha,
                        "metadata": metadata,
                        "certificate_kind": (
                            "direct" if direct_unit else "split"
                        ),
                        "fresh_replay_seconds": replay["seconds"],
                    }
                )
        if len(records) != descriptor["expected_charts"]:
            raise AssertionError(f"{shape} core chart count changed")

        core_path = DESTINATION / f"{shape}_core_charts.json"
        core_path.write_text(
            json.dumps(
                {
                    "schema": 1,
                    "status": "EXACT_RATIONAL_UNIT_CHART_CORE",
                    "shape": shape,
                    "backbones": descriptor["expected_backbones"],
                    "charts": len(records),
                    "direct_unit_ideals": direct,
                    "split_unit_ideals": split,
                    "records": records,
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
            newline="\n",
        )

        cnf_gzip = DESTINATION / f"{shape}_cover.cnf.gz"
        proof_gzip = DESTINATION / f"{shape}_cover.drat.gz"
        deterministic_gzip(descriptor["cnf"], cnf_gzip)
        deterministic_gzip(descriptor["proof"], proof_gzip)
        drat_log = DESTINATION / f"{shape}_drat_trim.stdout"
        raw_drat_log = descriptor["drat_stdout"].read_text(
            encoding="utf-8",
            errors="replace",
        )
        normalized_drat_log = "\n".join(
            line.rstrip()
            for line in raw_drat_log.splitlines()
            if line.strip()
        )
        drat_log.write_text(
            normalized_drat_log + "\n",
            encoding="utf-8",
            newline="\n",
        )
        shape_manifests[shape] = {
            "backbones": descriptor["expected_backbones"],
            "core_charts": len(records),
            "direct_unit_ideals": direct,
            "split_unit_ideals": split,
            "cnf_variables": cover["final_variables"],
            "cnf_clauses": cover["final_clauses"],
            "cnf_raw_bytes": descriptor["cnf"].stat().st_size,
            "cnf_raw_sha256": cover["cnf_sha256"],
            "proof_raw_bytes": descriptor["proof"].stat().st_size,
            "proof_raw_sha256": drat["proof_sha256"],
            "kissat_sha256": kissat["kissat_sha256"],
            "drat_trim_sha256": drat["drat_trim_sha256"],
            "drat_verify_seconds": drat["verify_seconds"],
            "files": {
                "core": file_descriptor(core_path),
                "cnf_gzip": file_descriptor(cnf_gzip),
                "proof_gzip": file_descriptor(proof_gzip),
                "drat_log": file_descriptor(drat_log),
            },
        }

    if used_fresh_keys != set(fresh_by_key):
        raise AssertionError("packaged core does not match fresh replay")
    replay_path = DESTINATION / "fresh_singular_replay.json"
    shutil.copyfile(FRESH_REPLAY, replay_path)
    manifest = {
        "schema": 1,
        "status": "EXACT_FINITE_BRANCH_THEOREM",
        "scope": (
            "P5 to Delta3 restrictions with at most three coordinate "
            "rows in every local map"
        ),
        "conclusion": "no such complex restriction exists",
        "global_conjecture_resolved": False,
        "higher_coordinate_p5_branch_resolved": False,
        "catalogue_pair_signatures": 6495,
        "coordinate_backbone_shapes": ["c10", "c4c6"],
        "coordinate_backbone_orbits": 200,
        "core_charts": 812,
        "fresh_singular_replay": {
            **file_descriptor(replay_path),
            "jobs": fresh["jobs"],
            "timeout_seconds": fresh["timeout_seconds"],
            "elapsed_seconds": fresh["elapsed_seconds"],
        },
        "shapes": shape_manifests,
    }
    manifest_path = DESTINATION / "manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        json.dumps(
            {
                "packaged": True,
                "destination": str(DESTINATION.relative_to(REPO_ROOT)),
                "manifest_sha256": sha256(manifest_path),
                "core_charts": manifest["core_charts"],
                "shapes": {
                    shape: {
                        "cnf_gzip_bytes": data["files"][
                            "cnf_gzip"
                        ]["bytes"],
                        "proof_gzip_bytes": data["files"][
                            "proof_gzip"
                        ]["bytes"],
                    }
                    for shape, data in shape_manifests.items()
                },
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
