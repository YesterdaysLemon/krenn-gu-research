#!/usr/bin/env python3
"""Generate exact one-row-escape same-third-row certificates.

This generator is not needed for replay.  It requires Singular 4.x, either
directly on PATH or through the default WSL distribution.  The generated
JSON is checked by two implementations that reconstruct every generator.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUTPUT = HERE / (
    "balanced_m3_common_three_space_joint_rank_five_hilbert_burch_"
    "one_two_two_residual_second_root_coloop_same_third_row_certificates.json"
)

VARIABLES = (
    "x10",
    "x11",
    "x12",
    "x13",
    "y10",
    "y11",
    "y12",
    "y13",
    "z10",
    "z11",
    "z12",
    "z13",
    "x00",
    "x01",
    "x02",
    "x03",
    "y00",
    "y01",
    "y02",
    "y03",
    "z00",
    "z01",
    "z02",
    "z03",
    "tau",
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

proc ev(int ff,int rr,matrix rows)
{{
  return(
    C[ff,1]*rows[rr,1]
   +C[ff,2]*rows[rr,2]
   +C[ff,3]*rows[rr,3]
   +C[ff,4]*rows[rr,4]
  );
}}

proc polarized_product(int xx,int yy,int zz,int ri,int pi,int qi,matrix rows)
{{
  return(
    ev(xx,ri,rows)*ev(yy,pi,rows)*ev(zz,qi,rows)
   +ev(xx,ri,rows)*ev(zz,pi,rows)*ev(yy,qi,rows)
   +ev(yy,ri,rows)*ev(xx,pi,rows)*ev(zz,qi,rows)
   +ev(yy,ri,rows)*ev(zz,pi,rows)*ev(xx,qi,rows)
   +ev(zz,ri,rows)*ev(xx,pi,rows)*ev(yy,qi,rows)
   +ev(zz,ri,rows)*ev(yy,pi,rows)*ev(xx,qi,rows)
  );
}}

proc same_third_ideal(int family,int endpoint,int support_mask)
{{
  matrix rows[6][4];

  // R0,R1,P0,Q0 are the four fixed basis rows e0,e1,e3,e2.
  rows[1,1]=1;
  rows[2,2]=1;
  rows[3,4]=1;
  rows[5,3]=1;

  if (family==0)
  {{
    // The zero third row Q1 is one coordinate endpoint of R.
    rows[6,1+endpoint]=1;
    rows[4,1]=(support_mask%2);
    rows[4,2]=((support_mask div 2)%2);
    rows[4,3]=((support_mask div 4)%2);
  }}
  else
  {{
    // The zero third row is generic in R and is normalized to R0+R1.
    rows[6,1]=1;
    rows[6,2]=1;
    if (family==1)
    {{
      rows[4,1]=(support_mask%2);
      rows[4,2]=((support_mask div 2)%2);
      rows[4,3]=((support_mask div 4)%2);
    }}
    else
    {{
      // When P1 uses both R coordinates, their residual ratio is tau.
      // The certificate is polynomial in tau and needs no localization.
      rows[4,1]=1;
      rows[4,2]=tau;
      rows[4,3]=(support_mask==7);
    }}
  }}

  ideal I;
  int generator_count=0;
  int a,b,c,i,j,k;
  poly value;
  for (a=0;a<=1;a++)
  {{
    for (b=0;b<=1;b++)
    {{
      for (c=0;c<=1;c++)
      {{
        for (i=0;i<=1;i++)
        {{
          for (j=0;j<=1;j++)
          {{
            for (k=0;k<=1;k++)
            {{
              value=polarized_product(
                1+a,3+b,5+c,1+i,3+j,5+k,rows
              );
              if ((a==0)&&(b==0)&&(c==0)
                  &&(i==0)&&(j==0)&&(k==0))
              {{
                value=value-1;
              }}
              if ((a==1)&&(b==1)&&(c==1)
                  &&(i==1)&&(j==1)&&(k==0))
              {{
                value=value-1;
              }}
              if (generator_count==0)
              {{
                I=value;
              }}
              else
              {{
                I=I,value;
              }}
              generator_count++;
            }}
          }}
        }}
      }}
    }}
  }}
  return(I);
}}

proc emit_case(int family,int endpoint,int support_mask)
{{
  ideal I=same_third_ideal(family,endpoint,support_mask);
  matrix transform;
  ideal G=liftstd(I,transform);
  int unit_column=0;
  int gi;
  for (gi=1;gi<=size(G);gi++)
  {{
    if ((G[gi]!=0)&&(deg(G[gi])==0))
    {{
      unit_column=gi;
    }}
  }}
  if (unit_column==0)
  {{
    print("ERROR|nonunit|"+string(family)+"|"+string(endpoint)
          +"|"+string(support_mask));
  }}
  if ((size(I)!=64)||(nrows(transform)!=64))
  {{
    print("ERROR|bad_transform_rows|"+string(family)+"|"
          +string(endpoint)+"|"+string(support_mask)+"|"
          +string(size(I))+"|"+string(nrows(transform)));
  }}
  poly unit_value=G[unit_column];
  poly check=0;
  for (gi=1;gi<=64;gi++)
  {{
    check=check+I[gi]*transform[gi,unit_column]/unit_value;
  }}
  if (simplify(check-1,2)!=0)
  {{
    print("ERROR|bad_lift|"+string(family)+"|"+string(endpoint)
          +"|"+string(support_mask));
  }}

  print("CASE|"+string(family)+"|"+string(endpoint)
        +"|"+string(support_mask));
  intvec exponent;
  poly multiplier;
  for (gi=1;gi<=64;gi++)
  {{
    multiplier=transform[gi,unit_column]/unit_value;
    while (multiplier!=0)
    {{
      exponent=leadexp(multiplier);
      print(
        "TERM|"+string(gi)+"|"
        +string(leadcoef(multiplier))+"|"+string(exponent)
      );
      multiplier=multiplier-lead(multiplier);
    }}
  }}
}}

option(redSB);
int endpoint,support_mask;
for (endpoint=0;endpoint<=1;endpoint++)
{{
  for (support_mask=1;support_mask<=7;support_mask++)
  {{
    emit_case(0,endpoint,support_mask);
  }}
}}
intvec fixed_masks=1,2,4,5,6;
for (endpoint=1;endpoint<=size(fixed_masks);endpoint++)
{{
  emit_case(1,0,fixed_masks[endpoint]);
}}
emit_case(2,0,3);
emit_case(2,0,7);
"""


def run_singular(program: str) -> str:
    direct = shutil.which("Singular")
    if direct:
        command = [direct, "-q"]
    elif shutil.which("wsl"):
        command = [
            "wsl",
            "bash",
            "--noprofile",
            "--norc",
            "-lc",
            "Singular -q",
        ]
    else:
        raise SystemExit("Singular was not found directly or through WSL")
    completed = subprocess.run(
        command,
        input=program,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode:
        raise SystemExit(
            f"Singular failed with code {completed.returncode}:\n"
            f"{completed.stdout}\n{completed.stderr}"
        )
    if "ERROR|" in completed.stdout or "   ?" in completed.stdout:
        raise SystemExit(completed.stdout)
    return completed.stdout


def case_key(family: int, endpoint: int, support_mask: int) -> str:
    if family == 0:
        return f"endpoint-{endpoint}-{support_mask}"
    if family == 1:
        return f"generic-fixed-{support_mask}"
    if family == 2:
        return f"generic-parameter-{support_mask}"
    raise SystemExit(f"unexpected family {family}")


def parse_output(stdout: str) -> dict[str, object]:
    cases: dict[str, list[list[list[object]]]] = {}
    current: list[list[list[object]]] | None = None
    for raw_line in stdout.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        fields = line.split("|")
        if fields[0] == "CASE":
            key = case_key(int(fields[1]), int(fields[2]), int(fields[3]))
            current = [[] for _ in range(64)]
            cases[key] = current
        elif fields[0] == "TERM":
            if current is None:
                raise SystemExit("TERM appeared before CASE")
            generator_index = int(fields[1]) - 1
            coefficient = fields[2]
            exponent = [int(value) for value in fields[3].split(",")]
            if len(exponent) != len(VARIABLES):
                raise SystemExit(f"bad exponent length in {line}")
            sparse_exponent = [
                [index, value]
                for index, value in enumerate(exponent)
                if value
            ]
            current[generator_index].append([coefficient, sparse_exponent])

    expected = {
        f"endpoint-{endpoint}-{support_mask}"
        for endpoint in range(2)
        for support_mask in range(1, 8)
    }
    expected.update(
        f"generic-fixed-{support_mask}"
        for support_mask in (1, 2, 4, 5, 6)
    )
    expected.update(
        f"generic-parameter-{support_mask}" for support_mask in (3, 7)
    )
    if set(cases) != expected:
        missing = sorted(expected - set(cases))
        extra = sorted(set(cases) - expected)
        raise SystemExit(
            f"certificate case mismatch: missing={missing}, extra={extra}"
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
    print(f"cases=21 terms={term_count}")


if __name__ == "__main__":
    main()
