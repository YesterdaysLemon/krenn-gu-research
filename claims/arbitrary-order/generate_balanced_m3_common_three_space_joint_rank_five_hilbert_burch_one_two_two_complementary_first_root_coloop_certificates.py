#!/usr/bin/env python3
"""Generate exact certificates for the complementary first-root coloop.

The actual common-degeneration geometry has five normal forms: the two
inactive partner lines in the coloop plane agree or differ, and the in-plane
first row has two or three residual support types respectively.
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
    "one_two_two_complementary_first_root_coloop_certificates.json"
)


def load_base_generator() -> ModuleType:
    spec = importlib.util.spec_from_file_location("common_middle_generator", BASE_GENERATOR)
    if spec is None or spec.loader is None:
        raise SystemExit(f"cannot load {BASE_GENERATOR}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def variable_order(base: ModuleType) -> tuple[str, ...]:
    return tuple(base.VARIABLES[:-2]) + ("c0", "c1")


def singular_program(base: ModuleType) -> str:
    variables = variable_order(base)
    definitions = base.singular_program().split("proc common_middle_ideal", 1)[0]
    old_ring = f"ring R=0,({','.join(base.VARIABLES)}),dp;"
    new_ring = f"ring R=0,({','.join(variables)}),dp;"
    if definitions.count(old_ring) != 1:
        raise SystemExit("base generator no longer has the expected ring declaration")
    definitions = definitions.replace(old_ring, new_ring)
    return definitions + r"""
proc complementary_alpha_ideal(int incidence,int rtype)
{
  matrix rows[6][4];

  // C=<e0,e1>, S=C+<e2>.  The first indexed row r0 escapes S.
  rows[1,4]=1;

  // The inactive middle and third lines in C agree or are distinct.
  rows[3,1]=1;
  if (incidence==0) { rows[5,1]=1; }
  if (incidence==1) { rows[5,2]=1; }

  // The in-space indexed first row has the residual support type rtype.
  if (rtype==0) { rows[2,1]=1; }
  if (rtype==1) { rows[2,2]=1; }
  if (rtype==2) { rows[2,1]=1; rows[2,2]=1; }

  // Normalize the active middle quotient to e2.  Its third-row mate has
  // opposite quotient and arbitrary sum c0*e0+c1*e1 in C.
  rows[4,3]=1;
  rows[6,1]=c0;
  rows[6,2]=c1;
  rows[6,3]=-1;

  ideal I;
  int generator_count=0;
  int a,b,c,i,j,k;
  poly value;
  for (a=0;a<=1;a++)
  {
    for (b=0;b<=1;b++)
    {
      for (c=0;c<=1;c++)
      {
        for (i=0;i<=1;i++)
        {
          for (j=0;j<=1;j++)
          {
            for (k=0;k<=1;k++)
            {
              value=polarized_product(1+a,3+b,5+c,1+i,3+j,5+k,rows);
              if ((a==0)&&(b==0)&&(c==0)
                  &&(i==0)&&(j==1)&&(k==1)) { value=value-1; }
              if ((a==1)&&(b==1)&&(c==1)
                  &&(i==1)&&(j==1)&&(k==1)) { value=value-1; }
              if (generator_count==0) { I=value; } else { I=I,value; }
              generator_count++;
            }
          }
        }
      }
    }
  }
  return(I);
}

proc emit_case(int incidence,int rtype)
{
  ideal I=complementary_alpha_ideal(incidence,rtype);
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
    print("ERROR|nonunit|"+string(incidence)+"|"+string(rtype));
  }
  if ((size(I)!=64)||(nrows(transform)!=64))
  {
    print("ERROR|bad_transform_rows|"+string(incidence)+"|"
          +string(rtype)+"|"+string(size(I))+"|"+string(nrows(transform)));
  }
  poly unit_value=G[unit_column];
  poly check=0;
  for (gi=1;gi<=64;gi++)
  {
    check=check+I[gi]*transform[gi,unit_column]/unit_value;
  }
  if (simplify(check-1,2)!=0)
  {
    print("ERROR|bad_lift|"+string(incidence)+"|"+string(rtype));
  }

  print("CASE|"+string(incidence)+"|"+string(rtype));
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
emit_case(0,0);
emit_case(0,1);
emit_case(1,0);
emit_case(1,1);
emit_case(1,2);
"""


def parse_output(base: ModuleType, stdout: str) -> dict[str, object]:
    variables = variable_order(base)
    cases: dict[str, list[list[list[object]]]] = {}
    current: list[list[list[object]]] | None = None
    for raw_line in stdout.splitlines():
        fields = raw_line.strip().split("|")
        if not fields[0]:
            continue
        if fields[0] == "CASE":
            key = f"{fields[1]}-{fields[2]}"
            current = [[] for _ in range(64)]
            cases[key] = current
        elif fields[0] == "TERM":
            if current is None:
                raise SystemExit("TERM appeared before CASE")
            generator_index = int(fields[1]) - 1
            exponent = [int(value) for value in fields[3].split(",")]
            if len(exponent) != len(variables):
                raise SystemExit(f"bad exponent length in {raw_line}")
            sparse = [[i, power] for i, power in enumerate(exponent) if power]
            current[generator_index].append([fields[2], sparse])
    expected = {"0-0", "0-1", "1-0", "1-1", "1-2"}
    if set(cases) != expected:
        raise SystemExit(
            "certificate case mismatch: "
            f"missing={sorted(expected-set(cases))}, "
            f"extra={sorted(set(cases)-expected)}"
        )
    return {
        "format": "sparse-nullstellensatz-v1",
        "variable_order": list(variables),
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
