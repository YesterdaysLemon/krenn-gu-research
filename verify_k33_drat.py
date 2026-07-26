"""Check all 48 K3,3 DRAT traces with the independent drat-trim binary."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from rankone_support_sat import windows_to_wsl


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", type=Path, default=Path("."))
    parser.add_argument(
        "--checker",
        type=Path,
        default=Path("tmp/drat-trim/drat-trim"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("tmp/k33_drat_trim_audit.json"),
    )
    args = parser.parse_args()
    base = args.base.resolve()
    checker = (
        args.checker
        if args.checker.is_absolute()
        else base / args.checker
    )
    rows = []
    for orbit in range(48):
        cnf = base / "tmp" / f"k33_orbit_{orbit}.cnf"
        proof = base / "tmp" / f"k33_orbit_{orbit}.drat"
        completed = subprocess.run(
            [
                "wsl",
                "-e",
                windows_to_wsl(checker),
                windows_to_wsl(cnf),
                windows_to_wsl(proof),
            ],
            check=False,
            capture_output=True,
            text=True,
            timeout=60,
        )
        verified = (
            completed.returncode == 0
            and "s VERIFIED" in completed.stdout
        )
        if not verified:
            raise AssertionError(
                f"DRAT check failed for orbit {orbit}: "
                f"{completed.stdout}\n{completed.stderr}"
            )
        rows.append(
            {
                "orbit": orbit,
                "cnf_bytes": cnf.stat().st_size,
                "proof_bytes": proof.stat().st_size,
                "verified": True,
            }
        )
    result = {
        "verified": True,
        "checker": str(checker),
        "orbits": len(rows),
        "rows": rows,
    }
    output = (
        args.output
        if args.output.is_absolute()
        else base / args.output
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(result, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {output}: orbits=48 verified=True")


if __name__ == "__main__":
    main()
