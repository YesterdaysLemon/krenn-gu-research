"""Run the exhaustive degree-three e=19 reciprocal-orbit case split.

Each case fixes one representative from the independently enumerated
residual symmetry orbits.  Laurent and exact Singular no-goods learned in
one case are globally valid, so the learned CNF is carried into the next
case while the representative assumptions themselves are not.
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

REPO_ROOT, HERE = _bootstrap_repository(__file__)


import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def checkpoint(path: Path, payload: dict[str, object]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
    )
    temporary.replace(path)


def run(arguments: list[str]) -> None:
    print("+", " ".join(arguments), flush=True)
    result = subprocess.run(arguments, check=False)
    if result.returncode:
        raise RuntimeError(
            f"{arguments[0]} failed with code {result.returncode}"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--orbit-manifest",
        type=Path,
        default=Path(
            "tmp/degree3_e19_second_reciprocal_orbits.json"
        ),
    )
    parser.add_argument(
        "--graph6",
        type=Path,
        default=Path("tmp/n8_mindeg3_e12_28.g6"),
    )
    parser.add_argument("--base-cnf", type=Path, required=True)
    parser.add_argument("--start-orbit", type=int)
    parser.add_argument("--end-orbit", type=int, default=12)
    parser.add_argument(
        "--orbit-index",
        type=int,
        action="append",
        help=(
            "explicit orbit order; repeat as needed instead of using the "
            "inclusive start/end range"
        ),
    )
    parser.add_argument(
        "--prefix",
        type=Path,
        default=Path("tmp/degree3_e19_orbit"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("tmp/degree3_e19_orbit_cases.json"),
    )
    parser.add_argument(
        "--role-index",
        type=int,
        action="append",
        default=None,
    )
    parser.add_argument("--max-rounds", type=int, default=100)
    args = parser.parse_args()

    manifest = json.loads(
        args.orbit_manifest.read_text(encoding="utf-8")
    )
    orbits = list(manifest["orbits"])
    if args.orbit_index:
        orbit_indices = list(map(int, args.orbit_index))
        if len(set(orbit_indices)) != len(orbit_indices):
            raise ValueError("explicit orbit indices contain a duplicate")
        if min(orbit_indices) < 0 or max(orbit_indices) >= len(orbits):
            raise ValueError("explicit orbit index is out of range")
    else:
        if args.start_orbit is None:
            raise ValueError(
                "--start-orbit is required without --orbit-index"
            )
        if not 0 <= args.start_orbit <= args.end_orbit < len(orbits):
            raise ValueError("invalid inclusive orbit range")
        orbit_indices = list(
            range(args.start_orbit, args.end_orbit + 1)
        )
    roles = args.role_index or [144, 189, 216]
    current_cnf = args.base_cnf
    if not current_cnf.is_file():
        raise FileNotFoundError(current_cnf)

    payload: dict[str, object] = {
        "status": "running",
        "scope": (
            "sequential exact closure of residual reciprocal orbits"
        ),
        "orbit_manifest": str(args.orbit_manifest),
        "orbit_manifest_sha256": sha256(args.orbit_manifest),
        "orbit_indices": orbit_indices,
        "selected_role_indices": roles,
        "initial_cnf": str(current_cnf),
        "initial_cnf_sha256": sha256(current_cnf),
        "cases": [],
    }
    checkpoint(args.output, payload)

    cases: list[dict[str, object]] = []
    for orbit_index in orbit_indices:
        orbit = orbits[orbit_index]
        assumptions = [
            int(orbit["forward_candidate"]),
            int(orbit["reverse_candidate"]),
        ]
        stem = Path(f"{args.prefix}{orbit_index:02d}")
        batch = Path(f"{stem}_batch.json")
        learned_cnf = Path(f"{stem}_laurent.cnf")
        learned_manifest = Path(f"{stem}_laurent.json")
        chain_prefix = Path(f"{stem}_auto")
        chain = Path(f"{stem}_auto_chain.json")
        input_cnf = current_cnf

        batch_arguments = [
            sys.executable,
            str(HERE / "eight_vertex_skeleton_laurent_batch.py"),
            "--graph6",
            str(args.graph6),
            "--target-edges",
            "19",
            "--center-degree",
            "3",
            "--cnf",
            str(input_cnf),
            "--output",
            str(batch),
            "--learned-cnf",
            str(learned_cnf),
            "--learned-manifest",
            str(learned_manifest),
        ]
        for role_index in roles:
            batch_arguments.extend(
                ["--role-index", str(role_index)]
            )
        for literal in assumptions:
            batch_arguments.extend(["--assumption", str(literal)])
        run(batch_arguments)

        chain_arguments = [
            sys.executable,
            str(HERE / "iterate_eight_vertex_singular_cegar.py"),
            "--batch",
            str(batch),
            "--graph6",
            str(args.graph6),
            "--prefix",
            str(chain_prefix),
            "--start-round",
            "1",
            "--max-rounds",
            str(args.max_rounds),
            "--output",
            str(chain),
        ]
        for role_index in roles:
            chain_arguments.extend(
                ["--role-index", str(role_index)]
            )
        run(chain_arguments)

        result = json.loads(chain.read_text(encoding="utf-8"))
        if result["status"] != "subset_complete":
            raise AssertionError(
                f"orbit {orbit_index} did not close as a subset"
            )
        if list(map(int, result["fixed_assumptions"])) != assumptions:
            raise AssertionError(
                f"orbit {orbit_index} assumptions changed"
            )
        current_cnf = Path(str(result["final_learned_cnf"]))
        if sha256(current_cnf) != result[
            "final_learned_cnf_sha256"
        ]:
            raise AssertionError(
                f"orbit {orbit_index} final CNF hash mismatch"
            )
        cases.append(
            {
                "orbit_index": orbit_index,
                "representative": orbit["representative"],
                "orbit_size": int(orbit["orbit_size"]),
                "fixed_assumptions": assumptions,
                "input_cnf": str(input_cnf),
                "input_cnf_sha256": sha256(input_cnf),
                "initial_batch": str(batch),
                "initial_batch_sha256": sha256(batch),
                "chain": str(chain),
                "chain_sha256": sha256(chain),
                "exact_rounds": len(result["rounds"]),
                "final_cnf": str(current_cnf),
                "final_cnf_sha256": sha256(current_cnf),
            }
        )
        payload["cases"] = cases
        checkpoint(args.output, payload)
        print(
            f"orbit={orbit_index} closed "
            f"rounds={len(result['rounds'])}",
            flush=True,
        )

    payload["status"] = "subset_complete"
    payload["final_cnf"] = str(current_cnf)
    payload["final_cnf_sha256"] = sha256(current_cnf)
    checkpoint(args.output, payload)
    print(
        f"complete orbits={orbit_indices} "
        f"final_cnf={current_cnf}",
        flush=True,
    )


if __name__ == "__main__":
    main()
