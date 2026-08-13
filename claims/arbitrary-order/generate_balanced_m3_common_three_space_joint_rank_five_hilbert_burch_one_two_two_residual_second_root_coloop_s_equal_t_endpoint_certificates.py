#!/usr/bin/env python3
"""Generate exact certificates for the residual-coloop ``s=t`` endpoints.

The orbit and Singular emitter are inherited from the predecessor
same-third-row generator.  The sole row-space change is exact: the in-space
middle row ``P1`` is replaced by the escaping row ``P1-e3``, so ``P0+P1``
is the arbitrary nonzero intersection line.  Replay does not import either
generator.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from types import ModuleType

HERE = Path(__file__).resolve().parent
BASE_GENERATOR = HERE / (
    "generate_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_"
    "one_two_two_residual_second_root_coloop_same_third_row_certificates.py"
)
OUTPUT = HERE / (
    "balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_"
    "residual_second_root_coloop_s_equal_t_endpoint_certificates.json"
)


def load_base_generator() -> ModuleType:
    spec = importlib.util.spec_from_file_location("same_third_row_generator", BASE_GENERATOR)
    if spec is None or spec.loader is None:
        raise SystemExit(f"cannot load {BASE_GENERATOR}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    base = load_base_generator()
    program = base.singular_program()
    marker = "  ideal I;\n"
    if program.count(marker) != 1:
        raise SystemExit("base Singular program no longer has the expected row marker")
    program = program.replace(marker, "  rows[4,4]=-1;\n  ideal I;\n")
    data = base.parse_output(base.run_singular(program))
    OUTPUT.write_text(
        json.dumps(data, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    term_count = sum(
        len(multiplier)
        for case in data["cases"].values()  # type: ignore[union-attr]
        for multiplier in case
    )
    print(f"wrote {OUTPUT}")
    print(f"cases=21 terms={term_count}")


if __name__ == "__main__":
    main()
