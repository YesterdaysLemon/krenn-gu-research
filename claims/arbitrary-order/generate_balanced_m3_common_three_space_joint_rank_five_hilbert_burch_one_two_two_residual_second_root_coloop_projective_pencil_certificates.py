#!/usr/bin/env python3
"""Generate exact certificates for a generic in-space middle-plane line.

The generator is not needed to replay the proof.  It requires Singular 4.x,
either directly on PATH or through WSL.  The primary verifier and independent
audit reconstruct every generator before checking the durable output.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUTPUT = HERE / (
    "balanced_m3_common_three_space_joint_rank_five_hilbert_burch_"
    "one_two_two_residual_second_root_coloop_projective_pencil_certificates.json"
)

VARIABLES = (
    "x10", "x11", "x12", "x13",
    "y10", "y11", "y12", "y13",
    "z10", "z11", "z12", "z13",
    "x00", "x01", "x02", "x03",
    "y00", "y01", "y02", "y03",
    "z00", "z01", "z02", "z03",
)


def singular_program() -> str:
    variables = ",".join(VARIABLES)
    return rf"""
ring R=0,({variables}),dp;
matrix C[6][4]=
  x00,x01,x02,x03,
  x10,x11,x12,x13,
  y00,y01,y02,y03,
  y10,y11,y12,y13,
  z00,z01,z02,z03,
  z10,z11,z12,z13;

proc ev(int ff,intvec vv)
{{
  return(
    C[ff,1]*vv[1]+C[ff,2]*vv[2]
   +C[ff,3]*vv[3]+C[ff,4]*vv[4]
  );
}}

proc polarized_product(int xx,int yy,int zz,intvec rv,intvec pv,intvec qv)
{{
  return(
    ev(xx,rv)*ev(yy,pv)*ev(zz,qv)
   +ev(xx,rv)*ev(zz,pv)*ev(yy,qv)
   +ev(yy,rv)*ev(xx,pv)*ev(zz,qv)
   +ev(yy,rv)*ev(zz,pv)*ev(xx,qv)
   +ev(zz,rv)*ev(xx,pv)*ev(yy,qv)
   +ev(zz,rv)*ev(yy,pv)*ev(xx,qv)
  );
}}

proc generic_line_ideal(int re,int qe,int sm)
{{
  intvec R0,R1,Q0,Q1,P0,P1;
  if (re==0)
  {{
    R0=1,0,0,0;
    R1=0,1,0,0;
  }}
  else
  {{
    R1=1,0,0,0;
    R0=0,1,0,0;
  }}
  if (qe==0)
  {{
    Q0=1,0,0,0;
    Q1=0,0,1,0;
  }}
  else
  {{
    Q1=1,0,0,0;
    Q0=0,0,1,0;
  }}
  P0=0,0,0,1;
  // P0+P1 is the non-coordinate line P intersect S.
  P1=(sm%2),((sm div 2)%2),((sm div 4)%2),-1;

  ideal I;
  int a,b,c,i,j,k,generator_count;
  intvec RV,PV,QV;
  poly value;
  for (a=0;a<=1;a++)
  {{
    for (b=0;b<=1;b++)
    {{
      for (c=0;c<=1;c++)
      {{
        for (i=0;i<=1;i++)
        {{
          if (i==0) {{ RV=R0; }} else {{ RV=R1; }}
          for (j=0;j<=1;j++)
          {{
            if (j==0) {{ PV=P0; }} else {{ PV=P1; }}
            for (k=0;k<=1;k++)
            {{
              if (k==0) {{ QV=Q0; }} else {{ QV=Q1; }}
              value=polarized_product(1+a,3+b,5+c,RV,PV,QV);
              if ((a==0)&&(b==0)&&(c==0)
                  &&(i==0)&&(j==0)&&(k==0))
              {{
                value=value-1;
              }}
              if ((a==1)&&(b==1)&&(c==1)
                  &&(i==1)&&(j==1)&&(k==1))
              {{
                value=value-1;
              }}
              if (generator_count==0) {{ I=value; }} else {{ I=I,value; }}
              generator_count++;
            }}
          }}
        }}
      }}
    }}
  }}
  return(I);
}}

option(redSB);
int re,qe,mask,gi,unit_column;
ideal I,G;
matrix transform;
poly check,multiplier,unit_value;
intvec exponent;
for (re=0;re<=1;re++)
{{
  for (qe=0;qe<=1;qe++)
  {{
    for (mask=1;mask<=7;mask++)
    {{
      I=generic_line_ideal(re,qe,mask);
      G=liftstd(I,transform);
      unit_column=0;
      for (gi=1;gi<=size(G);gi++)
      {{
        if ((G[gi]!=0)&&(deg(G[gi])==0)) {{ unit_column=gi; }}
      }}
      if (unit_column==0)
      {{
        print("ERROR|nonunit|"+string(re)+"|"+string(qe)+"|"+string(mask));
      }}
      unit_value=G[unit_column];
      if ((size(I)!=64)||(nrows(transform)!=64))
      {{
        print("ERROR|bad_transform_rows|"+string(re)+"|"+string(qe)
              +"|"+string(mask)+"|"+string(size(I))
              +"|"+string(nrows(transform)));
      }}
      check=0;
      for (gi=1;gi<=64;gi++)
      {{
        check=check+I[gi]*transform[gi,unit_column]/unit_value;
      }}
      if (simplify(check-1,2)!=0)
      {{
        print("ERROR|bad_lift|"+string(re)+"|"+string(qe)+"|"+string(mask));
      }}
      print("CASE|"+string(re)+"|"+string(qe)+"|"+string(mask));
      for (gi=1;gi<=64;gi++)
      {{
        multiplier=transform[gi,unit_column]/unit_value;
        while (multiplier!=0)
        {{
          exponent=leadexp(multiplier);
          print("TERM|"+string(gi)+"|"+string(leadcoef(multiplier))
                +"|"+string(exponent));
          multiplier=multiplier-lead(multiplier);
        }}
      }}
    }}
  }}
}}
"""


def run_singular(program: str) -> str:
    direct = shutil.which("Singular")
    if direct:
        command = [direct, "-q"]
    elif shutil.which("wsl"):
        command = [
            "wsl", "bash", "--noprofile", "--norc", "-lc", "Singular -q"
        ]
    else:
        raise SystemExit("Singular was not found directly or through WSL")
    completed = subprocess.run(
        command, input=program, text=True, capture_output=True, check=False
    )
    if completed.returncode:
        raise SystemExit(
            f"Singular failed with code {completed.returncode}:\n"
            f"{completed.stdout}\n{completed.stderr}"
        )
    if "ERROR|" in completed.stdout:
        raise SystemExit(completed.stdout)
    return completed.stdout


def parse_output(stdout: str) -> dict[str, object]:
    cases: dict[str, list[list[list[object]]]] = {}
    current: list[list[list[object]]] | None = None
    for raw_line in stdout.splitlines():
        fields = raw_line.strip().split("|")
        if not fields[0]:
            continue
        if fields[0] == "CASE":
            key = f"{fields[1]}{fields[2]}-{fields[3]}"
            current = [[] for _ in range(64)]
            cases[key] = current
        elif fields[0] == "TERM":
            if current is None:
                raise SystemExit("TERM appeared before CASE")
            generator_index = int(fields[1]) - 1
            exponent = [int(value) for value in fields[3].split(",")]
            if len(exponent) != len(VARIABLES):
                raise SystemExit(f"bad exponent length in {raw_line}")
            sparse = [[i, power] for i, power in enumerate(exponent) if power]
            current[generator_index].append([fields[2], sparse])
    expected = {
        f"{a}{b}-{mask}"
        for a in range(2)
        for b in range(2)
        for mask in range(1, 8)
    }
    if set(cases) != expected:
        raise SystemExit(
            "certificate case mismatch: "
            f"missing={sorted(expected-set(cases))}, extra={sorted(set(cases)-expected)}"
        )
    return {
        "format": "sparse-nullstellensatz-v1",
        "variable_order": list(VARIABLES),
        "generator_order": "source_bits_then_row_bits_lexicographic",
        "cases": cases,
    }


def main() -> None:
    data = parse_output(run_singular(singular_program()))
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
    print(f"cases=28 terms={term_count}")


if __name__ == "__main__":
    main()
