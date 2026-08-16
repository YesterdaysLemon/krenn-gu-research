#!/usr/bin/env python3
"""Generate exact certificates for the two-supported diagonal endpoint.

The generator requires Singular 4.x, either directly on PATH or through the
default WSL distribution.  Replay does not require Singular: the generated
JSON is checked by a SymPy verifier and a no-import ``Fraction`` audit which
independently rebuild every permanent equation.

Every certificate is an identity in an ordinary characteristic-zero
polynomial ring.  No saturation, denominator, generic-point specialization,
or hidden nonzero assumption is used.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUTPUT = HERE / (
    "balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_"
    "fully_injective_diagonal_monomial_residual_two_supported_endpoint_"
    "certificates.json"
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
    "g",
    "h",
)

Row = tuple[str, str, str, str]
ZERO: Row = ("0", "0", "0", "0")
Q0: Row = ("0", "0", "1", "0")
Q1: Row = ("0", "0", "0", "1")


@dataclass(frozen=True)
class Case:
    key: str
    r: tuple[Row, Row]
    p: tuple[Row, Row]
    q: tuple[Row, Row]
    physical: bool = False
    u: Row = ZERO
    v: Row = ZERO

    @property
    def generator_count(self) -> int:
        return 128 if self.physical else 64


def add_rows(left: Row, right: Row) -> Row:
    output = []
    for a, b in zip(left, right, strict=True):
        if a == "0":
            output.append(b)
        elif b == "0":
            output.append(a)
        else:
            output.append(f"({a})+({b})")
    return tuple(output)  # type: ignore[return-value]


def projection_rows(kind: str, l0: Row, l1: Row) -> tuple[Row, Row]:
    if kind == "diag":
        return add_rows(("1", "0", "0", "0"), l0), add_rows(
            ("0", "1", "0", "0"), l1
        )
    if kind == "cross":
        return add_rows(("0", "1", "0", "0"), l0), add_rows(
            ("1", "0", "0", "0"), l1
        )
    if kind == "diag_shear":
        return add_rows(("1", "0", "0", "0"), l0), (
            "1",
            "1",
            "g",
            "h",
        )
    if kind == "cross_shear":
        return add_rows(("0", "1", "0", "0"), l0), (
            "1",
            "1",
            "g",
            "h",
        )
    raise AssertionError(kind)


def all_cases() -> list[Case]:
    r = (("1", "0", "0", "0"), ("0", "1", "0", "0"))
    q = (Q0, Q1)
    cases: list[Case] = []

    table_orbits: dict[str, tuple[Row, Row]] = {
        "zero_zero": (ZERO, ZERO),
        "zero_q1": (ZERO, Q1),
        "zero_q0": (ZERO, Q0),
        "prop_q0": (Q0, ("0", "0", "tau", "0")),
    }
    for kind in ("diag", "cross"):
        for orbit, (l0, l1) in table_orbits.items():
            cases.append(Case(f"{kind}_{orbit}", r, projection_rows(kind, l0, l1), q))

    # The diagonal projection has a particularly short table-only identity
    # on this independent boundary.  Its cross analogue needs the physical
    # common rows and is included below with all four assignments.
    cases.append(
        Case(
            "diag_ind_q1_q0",
            r,
            projection_rows("diag", Q1, Q0),
            q,
        )
    )

    for kind in ("diag", "cross"):
        p = projection_rows(kind, Q1, ("0", "0", "0", "tau"))
        cases.append(Case(f"{kind}_prop_q1", r, p, q, True, Q1, Q1))

    independent_orbits: dict[str, tuple[Row, Row]] = {
        "ind_q1_q0": (Q1, Q0),
        "ind_affine": (Q0, ("0", "0", "1", "1")),
    }
    # The diagonal q1/q0 chart is already excluded without the extra rows.
    # The remaining three independent charts retain both choices for each
    # common physical row: u and v lie on one of the two graph lines.
    for kind, orbit in (
        ("diag", "ind_affine"),
        ("cross", "ind_q1_q0"),
        ("cross", "ind_affine"),
    ):
        l0, l1 = independent_orbits[orbit]
        p = projection_rows(kind, l0, l1)
        for u_index in range(2):
            for v_index in range(2):
                cases.append(
                    Case(
                        f"{kind}_{orbit}_u{u_index}_v{v_index}",
                        r,
                        p,
                        q,
                        True,
                        (l0, l1)[u_index],
                        (l0, l1)[v_index],
                    )
                )

    for kind in ("diag_shear", "cross_shear"):
        for orbit, l0 in (("zero", ZERO), ("q0", Q0)):
            cases.append(Case(f"{kind}_{orbit}", r, projection_rows(kind, l0, ZERO), q))
        cases.append(
            Case(
                f"{kind}_q1",
                r,
                projection_rows(kind, Q1, ZERO),
                q,
                True,
                Q1,
                Q1,
            )
        )

    assert len(cases) == 29
    assert len({case.key for case in cases}) == len(cases)
    assert sum(case.physical for case in cases) == 16
    return cases


def singular_prelude() -> str:
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

proc endpoint_ideal(matrix rows,int physical)
{{
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
              value=polarized_product(1+a,3+b,5+c,1+i,3+j,5+k,rows);
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
              if (generator_count==0) {{ I=value; }} else {{ I=I,value; }}
              generator_count++;
            }}
          }}
        }}
      }}
    }}
  }}
  if (physical)
  {{
    // per(R,v,Q)=0, with v=rows[8].
    for (a=0;a<=1;a++)
    {{
      for (b=0;b<=1;b++)
      {{
        for (c=0;c<=1;c++)
        {{
          for (i=0;i<=1;i++)
          {{
            for (k=0;k<=1;k++)
            {{
              value=polarized_product(1+a,3+b,5+c,1+i,8,5+k,rows);
              I=I,value;
              generator_count++;
            }}
          }}
        }}
      }}
    }}
    // per(u,P,Q)=0, with u=rows[7].
    for (a=0;a<=1;a++)
    {{
      for (b=0;b<=1;b++)
      {{
        for (c=0;c<=1;c++)
        {{
          for (j=0;j<=1;j++)
          {{
            for (k=0;k<=1;k++)
            {{
              value=polarized_product(1+a,3+b,5+c,7,3+j,5+k,rows);
              I=I,value;
              generator_count++;
            }}
          }}
        }}
      }}
    }}
  }}
  return(I);
}}

proc emit_case(string key,matrix rows,int physical)
{{
  ideal I=endpoint_ideal(rows,physical);
  ideal G=slimgb(I);
  matrix transform=lift(I,G);
  int unit_column=0;
  int gi;
  for (gi=1;gi<=size(G);gi++)
  {{
    if ((G[gi]!=0)&&(deg(G[gi])==0)) {{ unit_column=gi; }}
  }}
  if (unit_column==0) {{ print("ERROR|nonunit|"+key); }}
  if (nrows(transform)!=size(I))
  {{
    print("ERROR|bad_transform_rows|"+key+"|"+string(size(I))
          +"|"+string(nrows(transform)));
  }}
  poly unit_value=G[unit_column];
  poly check=0;
  for (gi=1;gi<=size(I);gi++)
  {{
    check=check+I[gi]*transform[gi,unit_column]/unit_value;
  }}
  if (simplify(check-1,2)!=0) {{ print("ERROR|bad_lift|"+key); }}

  print("CASE|"+key+"|"+string(size(I)));
  intvec exponent;
  poly multiplier;
  for (gi=1;gi<=size(I);gi++)
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

option(redSB);
"""


def case_block(index: int, case: Case) -> str:
    rows = (*case.r, *case.p, *case.q, case.u, case.v)
    assignments = []
    matrix_name = f"rows{index}"
    for row_index, row in enumerate(rows, start=1):
        for coordinate, value in enumerate(row, start=1):
            if value != "0":
                assignments.append(f"{matrix_name}[{row_index},{coordinate}]={value};")
    assignments.append(
        f'emit_case("{case.key}",{matrix_name},{int(case.physical)});'
    )
    return f"matrix {matrix_name}[8][4];\n" + "\n".join(assignments) + "\n"


def singular_program() -> str:
    return singular_prelude() + "\n".join(
        case_block(index, case) for index, case in enumerate(all_cases())
    )


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
    try:
        completed = subprocess.run(
            command,
            input=program,
            text=True,
            capture_output=True,
            check=False,
            timeout=1800,
        )
    except subprocess.TimeoutExpired as error:
        raise SystemExit("Singular certificate generation exceeded 30 minutes") from error
    if completed.returncode:
        raise SystemExit(
            f"Singular failed with code {completed.returncode}:\n"
            f"{completed.stdout}\n{completed.stderr}"
        )
    if "ERROR|" in completed.stdout or "   ?" in completed.stdout:
        raise SystemExit(completed.stdout)
    return completed.stdout


def parse_output(stdout: str) -> dict[str, object]:
    specifications = {case.key: case for case in all_cases()}
    cases: dict[str, list[list[list[object]]]] = {}
    current: list[list[list[object]]] | None = None
    for raw_line in stdout.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        fields = line.split("|")
        if fields[0] == "CASE":
            key = fields[1]
            if key not in specifications:
                raise SystemExit(f"unexpected certificate case {key}")
            count = int(fields[2])
            expected_count = specifications[key].generator_count
            if count != expected_count:
                raise SystemExit(f"bad generator count for {key}: {count}")
            current = [[] for _ in range(count)]
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
                [index, value] for index, value in enumerate(exponent) if value
            ]
            current[generator_index].append([coefficient, sparse_exponent])

    if set(cases) != set(specifications):
        missing = sorted(set(specifications) - set(cases))
        extra = sorted(set(cases) - set(specifications))
        raise SystemExit(f"certificate case mismatch: missing={missing}, extra={extra}")
    return {
        "format": "sparse-nullstellensatz-v1",
        "variable_order": list(VARIABLES),
        "generator_order": (
            "RPQ_source_bits_then_row_bits; physical_tail_RvQ_then_uPQ_"
            "each_source_bits_then_two_row_bits; all_lexicographic"
        ),
        "case_kinds": {
            key: ("physical_128" if case.physical else "table_64")
            for key, case in specifications.items()
        },
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
    print(f"cases=29 terms={term_count}")


if __name__ == "__main__":
    main()
