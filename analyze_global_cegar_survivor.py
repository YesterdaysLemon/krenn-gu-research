"""Generate the exact reduced ideal for a global CEGAR survivor."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from killer_union_stratum import union_orbit_equations
from prism_laurent_reduction import primitive_binomial_reduction
from prism_orbit_screen import clean_polynomial, singular_program
from search_witness import EquationSystem


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cegar-result", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--characteristic", type=int, default=0)
    parser.add_argument("--saturate", action="store_true")
    args = parser.parse_args()

    payload = json.loads(args.cegar_result.read_text(encoding="utf-8"))
    error_payload = json.loads(payload["rows"][-1]["error"])
    pattern = error_payload["pattern"]
    nonzero_flat_entries = set(error_payload["nonzero_flat_entries"])
    system = EquationSystem(6, 3)
    names, equations, variable_names = union_orbit_equations(
        system, pattern
    )
    nonzero_names = {
        name
        for flat_index, name in variable_names.items()
        if flat_index in nonzero_flat_entries
    }
    restricted = []
    for equation in equations:
        surviving = type(equation)(
            {
                monomial: coefficient
                for monomial, coefficient in equation.items()
                if all(variable in nonzero_names for variable in monomial)
            }
        )
        surviving = clean_polynomial(surviving)
        if surviving:
            restricted.append(surviving)
    active_names = [name for name in names if name in nonzero_names]
    reduced_names, reduced, metadata = primitive_binomial_reduction(
        restricted, active_names
    )
    if args.saturate:
        saturation_variable = "sat"
        saturation_equation = Counter(
            {
                tuple(sorted([*reduced_names, saturation_variable])): 1,
                (): -1,
            }
        )
        reduced_names = [*reduced_names, saturation_variable]
        reduced = [*reduced, saturation_equation]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        singular_program(
            -1,
            reduced_names,
            reduced,
            args.characteristic,
            "full",
            "slimgb",
        ),
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "pattern": pattern,
                "support_variables": len(active_names),
                "reduced_variables": len(reduced_names),
                "reduced_equations": len(reduced),
                "saturated": args.saturate,
                "metadata": metadata,
                "output": str(args.output),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
