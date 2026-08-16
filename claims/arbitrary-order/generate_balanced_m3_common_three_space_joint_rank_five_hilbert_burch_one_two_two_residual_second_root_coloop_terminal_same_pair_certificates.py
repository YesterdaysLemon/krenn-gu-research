#!/usr/bin/env python3
"""Generate exact certificates for the terminal residual-coloop same-pair table.

The actual coloop geometry reduces the broad intersecting-plane problem to
15 polynomial families.  In branch A the active middle and third rows have a
sum in R.  In branch B the inactive middle row lies in R.  The equal Q=R
case is excluded analytically and is not a certificate case.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from types import ModuleType

HERE = Path(__file__).resolve().parent
BASE_GENERATOR = HERE / (
    "generate_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_"
    "one_two_two_residual_second_root_coloop_common_middle_row_certificates.py"
)
OUTPUT = HERE / (
    "balanced_m3_common_three_space_joint_rank_five_hilbert_burch_"
    "one_two_two_residual_second_root_coloop_terminal_same_pair_certificates.json"
)


def load_base_generator() -> ModuleType:
    spec = importlib.util.spec_from_file_location("common_middle_generator", BASE_GENERATOR)
    if spec is None or spec.loader is None:
        raise SystemExit(f"cannot load {BASE_GENERATOR}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def singular_program(base: ModuleType) -> str:
    program = base.singular_program()
    old_target = "&&(i==1)&&(j==0)&&(k==1))"
    new_target = "&&(i==1)&&(j==0)&&(k==0))"
    if program.count(old_target) != 1:
        raise SystemExit("base generator no longer has the expected target cell")
    program = program.replace(old_target, new_target)
    marker = "option(redSB);\n"
    if program.count(marker) != 1:
        raise SystemExit("base generator no longer has the expected execution marker")
    definitions = program.split(marker, 1)[0]
    return definitions + r"""
proc actual_terminal_ideal(int qtype,int branch,int patch)
{
  int plane_case=1+3*qtype;
  ideal I;
  if (branch==0)
  {
    // Selected residual colour j=s.  The active rows p0,q0 have opposite
    // evaluation pairs, hence p0+q0 lies in R.
    if (patch==0)
    {
      // p0=e0+tau*e1-e2; covers every sum with nonzero e0 coordinate.
      I=subst(common_middle_ideal(plane_case,1,0),sigma,-1);
    }
    if (patch==1)
    {
      // p0=e1-e2.
      I=subst(common_middle_ideal(plane_case,1,1),tau,-1);
    }
    if (patch==2)
    {
      // p0 and q0 are proportional.  Row rescaling normalizes both to e2.
      I=common_middle_ideal(plane_case,1,2);
    }
  }
  else
  {
    // Selected residual colour j=u.  The inactive middle row p1 lies in R.
    if (patch==0)
    {
      // p1=e0+tau*e1.
      I=subst(common_middle_ideal(plane_case,0,0),sigma,0);
    }
    if (patch==1)
    {
      // p1=e1.
      I=subst(common_middle_ideal(plane_case,0,1),tau,0);
    }
  }
  return(I);
}

proc emit_actual(int qtype,int branch,int patch)
{
  ideal I=actual_terminal_ideal(qtype,branch,patch);
  matrix transform;
  ideal G=liftstd(I,transform);
  int unit_column=0;
  int gi;
  for (gi=1;gi<=size(G);gi++)
  {
    if ((G[gi]!=0)&&(deg(G[gi])==0)) { unit_column=gi; }
  }
  if (unit_column==0)
  {
    print("ERROR|nonunit|"+string(qtype)+"|"
          +string(branch)+"|"+string(patch));
  }
  if ((size(I)!=64)||(nrows(transform)!=64))
  {
    print("ERROR|bad_transform_rows|"+string(qtype)+"|"
          +string(branch)+"|"+string(patch)+"|"
          +string(size(I))+"|"+string(nrows(transform)));
  }
  poly unit_value=G[unit_column];
  poly check=0;
  for (gi=1;gi<=64;gi++)
  {
    check=check+I[gi]*transform[gi,unit_column]/unit_value;
  }
  if (simplify(check-1,2)!=0)
  {
    print("ERROR|bad_lift|"+string(qtype)+"|"
          +string(branch)+"|"+string(patch));
  }

  print("CASE|"+string(qtype)+"|"
        +string(branch)+"|"+string(patch));
  intvec exponent;
  poly multiplier;
  for (gi=1;gi<=64;gi++)
  {
    multiplier=transform[gi,unit_column]/unit_value;
    while (multiplier!=0)
    {
      exponent=leadexp(multiplier);
      print(
        "TERM|"+string(gi)+"|"+string(leadcoef(multiplier))
        +"|"+string(exponent)
      );
      multiplier=multiplier-lead(multiplier);
    }
  }
}

option(redSB);
int qtype,patch;
for (qtype=0;qtype<=2;qtype++)
{
  for (patch=0;patch<=2;patch++) { emit_actual(qtype,0,patch); }
  for (patch=0;patch<=1;patch++) { emit_actual(qtype,1,patch); }
}
"""


def parse_output(base: ModuleType, stdout: str) -> dict[str, object]:
    cases: dict[str, list[list[list[object]]]] = {}
    current: list[list[list[object]]] | None = None
    for raw_line in stdout.splitlines():
        fields = raw_line.strip().split("|")
        if not fields[0]:
            continue
        if fields[0] == "CASE":
            key = f"{fields[1]}-{fields[2]}-{fields[3]}"
            current = [[] for _ in range(64)]
            cases[key] = current
        elif fields[0] == "TERM":
            if current is None:
                raise SystemExit("TERM appeared before CASE")
            generator_index = int(fields[1]) - 1
            exponent = [int(value) for value in fields[3].split(",")]
            if len(exponent) != len(base.VARIABLES):
                raise SystemExit(f"bad exponent length in {raw_line}")
            sparse = [[i, power] for i, power in enumerate(exponent) if power]
            current[generator_index].append([fields[2], sparse])
    expected = {
        f"{qtype}-0-{patch}" for qtype in range(3) for patch in range(3)
    } | {f"{qtype}-1-{patch}" for qtype in range(3) for patch in range(2)}
    if set(cases) != expected:
        raise SystemExit(
            "certificate case mismatch: "
            f"missing={sorted(expected-set(cases))}, "
            f"extra={sorted(set(cases)-expected)}"
        )
    return {
        "format": "sparse-nullstellensatz-v1",
        "variable_order": list(base.VARIABLES),
        "generator_order": "source_bits_then_row_bits_lexicographic",
        "cases": cases,
    }


def main() -> None:
    base = load_base_generator()
    data = parse_output(base, base.run_singular(singular_program(base)))
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
    print(f"cases={len(data['cases'])} terms={term_count}")


if __name__ == "__main__":
    main()
