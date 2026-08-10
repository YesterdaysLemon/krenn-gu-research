"""Verify the exact rational unit-ideal logs for closed prism orbits."""

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
import json
import re
from pathlib import Path


BATCH_DIRECTORIES = (
    Path("tmp/prism_batch_core"),
    Path("tmp/prism_batch_size18"),
    Path("tmp/prism_batch_587"),
    Path("tmp/prism_batch_size36a"),
)

ROOT_GROUPS = {
    168: ("generic", "lambda0_scalar", "lambda0_column", "lambda0_row"),
    300: ("generic", "lambda0_scalar", "lambda0_column", "lambda0_row"),
    508: ("generic", "lambda0_scalar", "lambda0_column", "lambda0_row"),
    420: ("generic", "lambda0_scalar", "lambda0_column", "lambda0_row"),
    686: ("generic", "lambda0_scalar", "lambda0_column", "lambda0_row"),
    703: (
        "generic",
        "b0_scalar",
        "b0_column",
        "b0_row",
        "b1_scalar",
        "b1_column",
        "b1_row",
    ),
    717: (
        "generic",
        "b0_scalar",
        "b0_column",
        "b0_row",
        "b1_scalar",
        "b1_column",
        "b1_row",
    ),
}

EXPECTED_CLOSED_ORBITS = frozenset(
    {
        0,
        7,
        36,
        41,
        47,
        50,
        54,
        55,
        62,
        92,
        109,
        146,
        168,
        170,
        268,
        295,
        300,
        326,
        408,
        420,
        503,
        508,
        587,
        686,
        703,
        717,
    }
)


def is_exact_unit_log(text: str) -> bool:
    return (
        "Auf Wiedersehen." in text
        and re.search(r"(?m)^GB_SIZE\r?\n1$", text) is not None
        and re.search(r"(?m)^REDUCE_ONE\r?\nr\r?\n0$", text) is not None
    )


def job_paths(directory: Path, singular_name: str) -> tuple[Path, Path]:
    singular = directory / singular_name
    return singular, singular.with_suffix(".log")


def manifest_jobs(
    base: Path, relative_directory: Path
) -> tuple[set[int], list[tuple[Path, Path]]]:
    directory = base / relative_directory
    rows = json.loads(
        (directory / "prism_orbit_batch_manifest.json").read_text(
            encoding="utf-8"
        )
    )
    orbits: set[int] = set()
    jobs: list[tuple[Path, Path]] = []
    for row in rows:
        orbits.add(int(row["orbit"]))
        jobs.append(job_paths(directory, str(row["generic"])))
        for branch in row["branches"]:
            jobs.append(job_paths(directory, str(branch["file"])))
    return orbits, jobs


def root_jobs(base: Path) -> tuple[set[int], list[tuple[Path, Path]]]:
    jobs: list[tuple[Path, Path]] = []
    for orbit, labels in ROOT_GROUPS.items():
        for label in labels:
            name = f"prism_orbit_{orbit}_{label}_q.sing"
            jobs.append(job_paths(base, name))
    return set(ROOT_GROUPS), jobs


def verify_job(singular: Path, log: Path) -> str | None:
    if not singular.is_file():
        return f"missing Singular input: {singular}"
    if not log.is_file():
        return f"missing Singular log: {log}"
    first_line = singular.read_text(encoding="utf-8").splitlines()[0]
    if not first_line.startswith("ring r=0,"):
        return f"not a rational job: {singular}"
    if not is_exact_unit_log(log.read_text(encoding="utf-8")):
        return f"log does not certify the unit ideal: {log}"
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", type=Path, default=Path("."))
    args = parser.parse_args()
    base = args.base.resolve()

    closed_orbits, jobs = root_jobs(base)
    for directory in BATCH_DIRECTORIES:
        batch_orbits, batch_jobs = manifest_jobs(base, directory)
        closed_orbits |= batch_orbits
        jobs.extend(batch_jobs)

    errors = [
        error
        for singular, log in jobs
        if (error := verify_job(singular, log)) is not None
    ]
    if closed_orbits != EXPECTED_CLOSED_ORBITS:
        errors.append(
            "closed orbit mismatch: "
            f"observed={sorted(closed_orbits)} "
            f"expected={sorted(EXPECTED_CLOSED_ORBITS)}"
        )
    if len(jobs) != 200:
        errors.append(f"expected 200 exact jobs, found {len(jobs)}")
    if errors:
        raise SystemExit("\n".join(errors))
    print(
        json.dumps(
            {
                "status": "verified",
                "field": "Q",
                "unit_ideal_jobs": len(jobs),
                "closed_prism_orbits": len(closed_orbits),
                "orbit_indices": sorted(closed_orbits),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
