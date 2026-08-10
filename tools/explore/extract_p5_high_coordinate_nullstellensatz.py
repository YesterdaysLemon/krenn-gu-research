#!/usr/bin/env python3
"""Extract one zero-forest P5 Nullstellensatz certificate profile."""

from __future__ import annotations

import argparse
import json
import subprocess
import time
from pathlib import Path

import sys

for _parent in Path(__file__).resolve().parents:
    if (_parent / "src" / "krenn_gu" / "bootstrap.py").is_file():
        sys.path.insert(0, str(_parent / "src"))
        break
else:  # pragma: no cover - checkout contract failure
    raise RuntimeError("cannot locate repository bootstrap")

from krenn_gu.bootstrap import bootstrap  # noqa: E402

REPO_ROOT, HERE = bootstrap(__file__)

from krenn_gu import p5_support_system as GENERATOR
from krenn_gu.p5_split_saturation import convert_text
from krenn_gu import p5_high_coordinate as HIGH
from krenn_gu import singular_runtime


def certificate_program(
    split_program: str,
    print_entries: bool,
) -> str:
    marker = "ideal G=slimgb(I);"
    if split_program.count(marker) != 1:
        raise ValueError("unexpected split-system basis command")
    prefix, _suffix = split_program.split(marker)
    entry_output = (
        '  print("ENTRY_POLYNOMIAL"); print(T[row,1]);'
        if print_entries
        else ""
    )
    return prefix + "\n".join(
        [
            "matrix T;",
            "timer=1;",
            "ideal G=liftstd(I,T);",
            'print("LIFT_SECONDS");',
            "timer;",
            'print("GB_SIZE");',
            "size(G);",
            'print("GB_FIRST");',
            "G[1];",
            'print("CERTIFICATE_SHAPE");',
            "nrows(T);",
            "ncols(T);",
            "int certificate_support=0;",
            "int certificate_terms=0;",
            "int certificate_max_degree=-1;",
            "int entry_degree=0;",
            "int entry_terms=0;",
            "for (int row=1; row<=nrows(T); row++)",
            "{",
            "  if (T[row,1] != 0)",
            "  {",
            "    certificate_support=certificate_support+1;",
            "    entry_degree=deg(T[row,1]);",
            "    entry_terms=size(T[row,1]);",
            "    certificate_terms=certificate_terms+entry_terms;",
            "    if (entry_degree>certificate_max_degree)",
            "    {",
            "      certificate_max_degree=entry_degree;",
            "    }",
            '    print("ENTRY");',
            "    row;",
            "    entry_degree;",
            "    entry_terms;",
            entry_output,
            "  }",
            "}",
            'print("CERTIFICATE_SUPPORT");',
            "certificate_support;",
            'print("CERTIFICATE_TERMS");',
            "certificate_terms;",
            'print("CERTIFICATE_MAX_DEGREE");',
            "certificate_max_degree;",
            'print("CERTIFICATE_CHECK");',
            "print(matrix(I)*T-matrix(G));",
            "quit;",
            "",
        ]
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--branch",
        choices=tuple(HIGH.BRANCH_BACKBONES),
        required=True,
    )
    parser.add_argument("--state", type=Path, required=True)
    parser.add_argument("--record-index", type=int, required=True)
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--print-entries", action="store_true")
    parser.add_argument(
        "--profile-basis-only",
        action="store_true",
        help="print Singular protocol data without carrying a lift matrix",
    )
    parser.add_argument(
        "--min-available-percent",
        type=float,
        default=20.0,
    )
    args = parser.parse_args()
    if (
        args.record_index < 0
        or args.timeout <= 0
        or not 15 <= args.min_available_percent < 100
    ):
        raise ValueError("invalid extraction arguments")
    if (
        HIGH.available_memory_percent()
        < args.min_available_percent
    ):
        raise MemoryError(
            "available host memory fell below the requested floor"
        )

    state = json.loads(args.state.read_bytes())
    if state.get("branch") != args.branch:
        raise ValueError("state branch changed")
    records = state.get("records", [])
    if args.record_index >= len(records):
        raise IndexError("record index is outside the source ledger")
    record = records[args.record_index]
    closure = tuple(
        tuple(map(int, row))
        for row in record["closure_supports"]
    )
    indices = tuple(map(int, record["signature_indices"]))
    program, _metadata = GENERATOR.generate(
        closure,
        indices,
        expected_partial_cells=0,
        pure_saturation_only=True,
        gauge_tree_edges=(),
        allow_arbitrary_support=True,
    )
    split = convert_text(program)
    extraction = (
        split.replace(
            "option(redSB);",
            "option(redSB);\noption(prot);",
        )
        if args.profile_basis_only
        else certificate_program(split, args.print_entries)
    )

    started = time.monotonic()
    try:
        completed = subprocess.run(
            singular_runtime.singular_command_with_timeout(args.timeout),
            input=extraction,
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            timeout=args.timeout + 5,
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        print(
            json.dumps(
                {
                    "status": "TIMEOUT",
                    "branch": args.branch,
                    "record_index": args.record_index,
                    "seconds": round(
                        time.monotonic() - started, 6
                    ),
                    "stdout_tail": (
                        error.stdout[-2000:]
                        if isinstance(error.stdout, str)
                        else ""
                    ),
                },
                indent=2,
            )
        )
        return
    output = completed.stdout + completed.stderr
    print(output)
    print(
        json.dumps(
            {
                "status": (
                    (
                        "BASIS_PROFILED"
                        if "UNIT_IDEAL" in output
                        else "INCONCLUSIVE"
                    )
                    if args.profile_basis_only
                    else (
                        "EXTRACTED"
                        if "CERTIFICATE_CHECK\n0" in output
                        else "INCONCLUSIVE"
                    )
                ),
                "branch": args.branch,
                "record_index": args.record_index,
                "seconds": round(
                    time.monotonic() - started, 6
                ),
                "returncode": completed.returncode,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
