#!/usr/bin/env python3
"""Probe affine ideals in orbit 384's coarse C10 motif class."""

from __future__ import annotations

import argparse
import json
import re
import shlex
import shutil
import subprocess
from collections import Counter
from pathlib import Path

import analyze_p5_exact_three_motifs as MOTIF
import generate_p5_exact_three_partial_support_system as GENERATOR


ROOT = Path(__file__).resolve().parent
CATALOGUE = (
    ROOT
    / "research_snapshots"
    / "2026-07-27-p5-coordinate-cegar"
    / "three_partial_c10_audit"
    / "sat_catalogue_c10.json"
)
IDEAL = re.compile(
    r"^(?P<prefix>.*?^ideal I=)(?P<equations>.*?)"
    r"(?P<suffix>;$\n^ideal G=.*)$",
    re.MULTILINE | re.DOTALL,
)
EXPECTED = {
    384: "AFFINE_UNIT_IDEAL",
    1179: "AFFINE_NONUNIT",
    2961: "AFFINE_UNIT_IDEAL",
    2966: "AFFINE_UNIT_IDEAL",
    6646: "AFFINE_NONUNIT",
    7772: "AFFINE_UNIT_IDEAL",
    9425: "AFFINE_NONUNIT",
    9518: "AFFINE_UNIT_IDEAL",
    9534: "AFFINE_UNIT_IDEAL",
    9535: "AFFINE_UNIT_IDEAL",
    9601: "AFFINE_UNIT_IDEAL",
    9608: "AFFINE_UNIT_IDEAL",
    9959: "AFFINE_UNIT_IDEAL",
    9962: "AFFINE_NONUNIT",
    9971: "AFFINE_UNIT_IDEAL",
}


def singular_command(explicit: str | None) -> list[str]:
    if explicit:
        return shlex.split(explicit)
    if shutil.which("Singular"):
        return ["Singular", "-q"]
    if shutil.which("wsl.exe"):
        return ["wsl.exe", "--exec", "Singular", "-q"]
    raise RuntimeError(
        "Singular was not found; pass --singular-command explicitly"
    )


def affine_program(program: str) -> str:
    match = IDEAL.match(program)
    if match is None:
        raise AssertionError("generated Singular source is unrecognized")
    equations = match.group("equations").split(",\n")
    if not equations[-1].startswith("z*("):
        raise AssertionError("generated saturation equation changed")
    return (
        match.group("prefix")
        + ",\n".join(equations[:-1])
        + match.group("suffix")
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--singular-command")
    parser.add_argument("--timeout", type=int, default=30)
    args = parser.parse_args()
    command = singular_command(args.singular_command)

    payload = json.loads(CATALOGUE.read_text(encoding="utf-8"))
    shape = "c10"
    components = MOTIF.cycle_components(shape)
    automorphisms = MOTIF.shape_automorphisms(shape)
    target_case = payload["cases"][384]
    target_support = tuple(
        tuple(row) for row in target_case["supports"]
    )
    target_backbone = MOTIF.coordinate_backbone(
        shape, target_support, automorphisms
    )
    target_geometry = MOTIF.coloured_partial_geometry(
        target_support, components
    )

    selected = []
    for case in payload["cases"]:
        supports = tuple(tuple(row) for row in case["supports"])
        if (
            MOTIF.coordinate_backbone(
                shape, supports, automorphisms
            )
            == target_backbone
            and MOTIF.coloured_partial_geometry(
                supports, components
            )
            == target_geometry
        ):
            selected.append(case)
    if [case["orbit_index"] for case in selected] != list(EXPECTED):
        raise AssertionError("orbit 384 coarse motif class changed")

    results = []
    for case in selected:
        supports = tuple(tuple(row) for row in case["supports"])
        signatures = tuple(case["witness_signature_indices"])
        program, metadata = GENERATOR.generate(supports, signatures)
        completed = subprocess.run(
            command,
            input=affine_program(program),
            text=True,
            capture_output=True,
            timeout=args.timeout,
            check=False,
        )
        if completed.returncode != 0 or completed.stderr.strip():
            raise AssertionError(
                f"Singular failed at orbit {case['orbit_index']}: "
                f"{completed.stdout!r} {completed.stderr!r}"
            )
        status = (
            "AFFINE_UNIT_IDEAL"
            if completed.stdout.strip() == "UNIT_IDEAL"
            else "AFFINE_NONUNIT"
        )
        if status != EXPECTED[case["orbit_index"]]:
            raise AssertionError(
                f"affine status changed at orbit {case['orbit_index']}: "
                f"{completed.stdout!r}"
            )
        results.append(
            {
                "orbit_index": case["orbit_index"],
                "mixed_equations": metadata["mixed_equations"],
                "status": status,
            }
        )

    counts = Counter(result["status"] for result in results)
    print(
        json.dumps(
            {
                "verified": True,
                "scope": (
                    "orbit 384's common coordinate-backbone and "
                    "missing-colour-geometry class"
                ),
                "cases": len(results),
                "counts": dict(sorted(counts.items())),
                "results": results,
                "interpretation": (
                    "coarse motif equality does not determine whether "
                    "the unsaturated mixed-coefficient ideal is unit"
                ),
                "saturation_checked": False,
                "global_conjecture_resolved": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
