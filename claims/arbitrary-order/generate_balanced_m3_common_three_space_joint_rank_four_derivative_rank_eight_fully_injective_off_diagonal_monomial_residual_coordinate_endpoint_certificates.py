#!/usr/bin/env python3
"""Generate exact sparse-edge certificates for the off-diagonal endpoint.

The proof atlas has three parts: a parallel-edge plane-separation cover,
physical common-row refinements of eight lift-hard leaves, and a nine-chart
terminal graph cover.  Every Singular leaf is independently time- and
address-space-bounded and is cached only after its emitted identity parses.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUTPUT = HERE / (
    "balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_"
    "fully_injective_off_diagonal_monomial_residual_coordinate_endpoint_"
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
    "p00",
    "p01",
    "p02",
    "p03",
    "p10",
    "p11",
    "p12",
    "p13",
    "q00",
    "q01",
    "q10",
    "q11",
)

Row = tuple[str, str, str, str]
R0: Row = ("1", "0", "0", "0")
R1: Row = ("0", "1", "0", "0")
E2: Row = ("0", "0", "1", "0")
E3: Row = ("0", "0", "0", "1")


@dataclass(frozen=True)
class Case:
    key: str
    edge: str
    rows: tuple[Row, Row, Row, Row, Row, Row]
    physical_v: Row | None = None
    stage: str = "separation_table"
    parent: str | None = None

    @property
    def generator_count(self) -> int:
        return 80 if self.physical_v is not None else 48


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


def subtract_rows(left: Row, right: Row) -> Row:
    output = []
    for a, b in zip(left, right, strict=True):
        if b == "0":
            output.append(a)
        elif a == "0":
            output.append(f"-({b})")
        else:
            output.append(f"({a})-({b})")
    return tuple(output)  # type: ignore[return-value]


def incidence_cases() -> list[Case]:
    cases = []
    intersection_lines = {"r0": R0, "r1": R1, "generic": add_rows(R0, R1)}
    for edge in ("parallel",):
        for line_key, ell in intersection_lines.items():
            q_orbits = {
                "q0_intersection": (ell, E2),
                "q1_intersection": (E2, ell),
                "affine": (E2, add_rows(ell, E2)),
            }
            for q_key, (q0, q1) in q_orbits.items():
                # The intersection line P cap S is projective.  These three
                # affine charts cover it without a redundant common scalar.
                line_charts = {
                    "s0": ("1", "p00", "p01", "0"),
                    "s1": ("0", "1", "p00", "0"),
                    "s2": ("0", "0", "1", "0"),
                }
                for s_key, intersection in line_charts.items():
                    p_orbits = {
                        "p0_in": (intersection, E3),
                        "p1_in": (E3, intersection),
                        "generic_line": (
                            E3,
                            subtract_rows(intersection, E3),
                        )
                    }
                    for p_key, (p0, p1) in p_orbits.items():
                        cases.append(
                            Case(
                                f"{edge}_line_{line_key}_{q_key}_{p_key}_{s_key}",
                                edge,
                                (R0, R1, p0, p1, q0, q1),
                            )
                        )
                p0_charts = {
                    "a0": ("1", "p00", "p01", "0"),
                    "a1": ("0", "1", "p00", "0"),
                    "a2": ("0", "0", "1", "0"),
                }
                p1_charts = {
                    "b0": ("1", "p10", "p11", "0"),
                    "b1": ("0", "1", "p10", "0"),
                    "b2": ("0", "0", "1", "0"),
                }
                for p0_key, p0 in p0_charts.items():
                    for p1_key, p1 in p1_charts.items():
                        cases.append(
                            Case(
                                f"{edge}_line_{line_key}_{q_key}_inside_"
                                f"{p0_key}_{p1_key}",
                                edge,
                                (R0, R1, p0, p1, q0, q1),
                            )
                        )
        # Equal intersecting planes R=Q.  Ordered bases in one two-plane have
        # seven diagonal-torus support orbits: two monomial, four with one
        # zero entry, and one full-support parameter family.  The third plane
        # is disjoint, meets R in a line, or equals R.
        q_equal_orbits = {
            "diagonal": (R0, R1),
            "cross": (R1, R0),
            "missing_a": (R1, add_rows(R0, R1)),
            "missing_b": (R0, add_rows(R0, R1)),
            "missing_c": (add_rows(R0, R1), R1),
            "missing_d": (add_rows(R0, R1), R0),
            "full": (add_rows(R0, R1), ("1", "q00", "0", "0")),
        }
        for q_key, (q0, q1) in q_equal_orbits.items():
            cases.append(
                Case(
                    f"{edge}_equal_{q_key}_disjoint",
                    edge,
                    (R0, R1, E2, E3, q0, q1),
                )
            )
            equal_line_charts = {
                "s0": ("1", "p00", "0", "0"),
                "s1": ("0", "1", "0", "0"),
            }
            for s_key, intersection in equal_line_charts.items():
                p_orbits = {
                    "p0_in": (intersection, E2),
                    "p1_in": (E2, intersection),
                    "generic_line": (E2, subtract_rows(intersection, E2)),
                }
                for p_key, (p0, p1) in p_orbits.items():
                    cases.append(
                        Case(
                            f"{edge}_equal_{q_key}_{p_key}_{s_key}",
                            edge,
                            (R0, R1, p0, p1, q0, q1),
                        )
                    )
            cases.append(
                Case(
                    f"{edge}_equal_{q_key}_equal",
                    edge,
                    (
                        R0,
                        R1,
                        ("p00", "p01", "0", "0"),
                        ("p10", "p11", "0", "0"),
                        q0,
                        q1,
                    ),
                )
            )
    assert len(cases) == 218
    assert len({case.key for case in cases}) == 218
    return cases


HARD_LINE_KEYS = {
    "parallel_line_r0_q1_intersection_p0_in_s0",
    "parallel_line_r1_q1_intersection_p0_in_s0",
    "parallel_line_generic_q1_intersection_p0_in_s0",
    "parallel_line_generic_affine_p1_in_s1",
    "parallel_line_generic_affine_generic_line_s1",
}

HARD_INSIDE_KEYS = {
    "parallel_line_generic_q1_intersection_inside_a0_b0",
    "parallel_line_generic_affine_inside_a0_b0",
    "parallel_line_generic_affine_inside_a0_b1",
}


def pivot_flag_rows() -> dict[str, tuple[Row, Row]]:
    """Six affine charts for a line inside a plane in a three-space.

    The first row is the distinguished line.  Adding it to the second row
    is allowed in every use below, so ordinary row elimination gives these
    denominator-free representatives.
    """

    charts: dict[str, tuple[Row, Row]] = {}
    for first_pivot in range(3):
        for second_pivot in range(3):
            if second_pivot == first_pivot:
                continue
            remaining = next(
                index
                for index in range(3)
                if index not in {first_pivot, second_pivot}
            )
            first_values = ["0", "0", "0", "0"]
            first_values[first_pivot] = "1"
            free_coordinates = [
                index for index in range(3) if index != first_pivot
            ]
            first_values[free_coordinates[0]] = "p00"
            first_values[free_coordinates[1]] = "p01"
            second_values = ["0", "0", "0", "0"]
            second_values[second_pivot] = "1"
            second_values[remaining] = "p10"
            charts[f"f{first_pivot}{second_pivot}"] = (
                tuple(first_values),  # type: ignore[arg-type]
                tuple(second_values),  # type: ignore[arg-type]
            )
    assert len(charts) == 6
    return charts


def outside_middle_flags(case: Case) -> dict[str, tuple[Row, Row]]:
    """Six charts for the ordered middle-plane flag when ``v`` is outside.

    The generic affine and generic ``q1`` parents admit smaller boundary
    charts than three of the unrestricted pivots.  The displayed unions are
    still complete: eliminate the first pivot from the second row, use the
    three retained pivot charts whenever their named coordinate is nonzero,
    and normalize the remaining one-dimensional boundary.
    """

    pivots = pivot_flag_rows()
    if "_generic_affine_" in case.key:
        return {
            "f02": pivots["f02"],
            "f20": pivots["f20"],
            # The f20 chart already covers f21 whenever the second row has
            # nonzero e0-coordinate.  Only its p10=0 wall is additional.
            "f21_p10_zero": (pivots["f21"][0], R1),
            "b10_affine": (R1, ("1", "0", "p00", "0")),
            "b12_fixed": (R1, E2),
            "b01_affine": (("1", "p00", "0", "0"), R1),
        }
    if "_generic_q1_intersection_" in case.key:
        return {
            "f01": pivots["f01"],
            "f02": pivots["f02"],
            "f20": pivots["f20"],
            "f21": pivots["f21"],
            "b10_affine": (R1, ("1", "0", "p00", "0")),
            "b12_fixed": (R1, E2),
        }
    return pivots


def inner_line_flags(case: Case) -> dict[str, tuple[Row, Row]]:
    """A parent-adapted finite cover of ``v`` and an independent line."""

    pivots = pivot_flag_rows()
    common = {
        "f20": pivots["f20"],
        "f21": pivots["f21"],
        "r01": (("1", "p00", "0", "0"), R1),
        "r10": (R1, R0),
    }
    if "_generic_affine_" in case.key:
        return {
            "f12": pivots["f12"],
            **common,
            "r02_fixed": (R0, E2),
            "r02_affine": (R0, ("0", "1", "p00", "0")),
        }
    if "_generic_q1_intersection_" in case.key:
        return {
            "f12_v2_zero": (
                ("p00", "1", "0", "0"),
                ("p10", "0", "1", "0"),
            ),
            **common,
            "r02": (R0, ("0", "p00", "1", "0")),
        }
    return {
        "f12": pivots["f12"],
        **common,
        "r02": (R0, ("0", "p00", "1", "0")),
    }


def full_flag_rows() -> dict[str, tuple[Row, Row, Row]]:
    """Six affine charts for ``span(v) < span(v,p0) < S``."""

    charts: dict[str, tuple[Row, Row, Row]] = {}
    for key, (v, p0) in pivot_flag_rows().items():
        first_pivot = int(key[1])
        second_pivot = int(key[2])
        remaining = next(
            index
            for index in range(3)
            if index not in {first_pivot, second_pivot}
        )
        p1_values = ["0", "0", "0", "0"]
        p1_values[remaining] = "1"
        charts[key] = (v, p0, tuple(p1_values))  # type: ignore[arg-type]
    return charts


def line_row_and_orientation(case: Case) -> tuple[Row, str]:
    p0, p1 = case.rows[2:4]
    if "_p0_in_" in case.key:
        return p0, "p0_in"
    if "_p1_in_" in case.key:
        return p1, "p1_in"
    if "_generic_line_" in case.key:
        return add_rows(p0, p1), "generic_line"
    raise AssertionError(case.key)


def oriented_line_plane(line: Row, outside: Row, orientation: str) -> tuple[Row, Row]:
    if orientation == "p0_in":
        return line, outside
    if orientation == "p1_in":
        return outside, line
    if orientation == "generic_line":
        return outside, subtract_rows(line, outside)
    raise AssertionError(orientation)


def hard_line_refinements(case: Case) -> list[Case]:
    r0, r1, _p0, _p1, q0, q1 = case.rows
    _line, orientation = line_row_and_orientation(case)
    refinements: list[Case] = []

    # If v is outside S=R+Q, use v as the fourth basis vector and shift both
    # middle rows into S.  The exceptional row admits the additional shear
    # p1 -> p1+lambda*p0, so the resulting ordered plane has six flag charts.
    for chart, (p0, p1) in outside_middle_flags(case).items():
        refinements.append(
            Case(
                f"{case.key}__v_outside_{chart}",
                "parallel",
                (r0, r1, p0, p1, q0, q1),
                E3,
                "separation_refinement",
                case.key,
            )
        )

    # If v lies in S, v and the intersection line form a flag.  The retained
    # pivots and their explicit projective boundaries cover every flag.
    for chart, (v, pivot_line) in inner_line_flags(case).items():
        p0, p1 = oriented_line_plane(pivot_line, E3, orientation)
        refinements.append(
            Case(
                f"{case.key}__v_inside_{chart}",
                "parallel",
                (r0, r1, p0, p1, q0, q1),
                v,
                "separation_refinement",
                case.key,
            )
        )
    expected = 13 if "_generic_affine_" in case.key else 12
    assert len(refinements) == expected
    return refinements


def hard_inside_refinements(case: Case) -> list[Case]:
    r0, r1, _p0, _p1, q0, q1 = case.rows
    refinements = []
    for chart, (p0, p1) in outside_middle_flags(case).items():
        refinements.append(
            Case(
                f"{case.key}__v_outside_{chart}",
                "parallel",
                (r0, r1, p0, p1, q0, q1),
                E3,
                "separation_refinement",
                case.key,
            )
        )
    for chart, (v, p0, p1) in full_flag_rows().items():
        refinements.append(
            Case(
                f"{case.key}__v_inside_{chart}",
                "parallel",
                (r0, r1, p0, p1, q0, q1),
                v,
                "separation_refinement",
                case.key,
            )
        )
    assert len(refinements) == 12
    return refinements


def endpoint_cases() -> list[Case]:
    quotient_orbits: dict[str, tuple[Row, Row]] = {
        "diagonal": (R0, R1),
        "cross": (R1, R0),
        "missing_d": (add_rows(R0, R1), R0),
    }
    v_orbits = {
        "q0": (E2, E3),
        "q1": (E3, E2),
        "generic": (add_rows(E2, E3), E3),
    }
    cases = []
    for quotient_key, (a0, a1) in quotient_orbits.items():
        for v_key, (v, complement) in v_orbits.items():
            p0 = add_rows(a0, tuple(
                "p00" if value == "1" else "0" for value in complement
            ))
            p1 = add_rows(a1, tuple(
                "p01" if value == "1" else "0" for value in complement
            ))
            cases.append(
                Case(
                    f"endpoint_{quotient_key}_{v_key}",
                    "parallel",
                    (R0, R1, p0, p1, E2, E3),
                    v,
                    "endpoint_graph",
                )
            )
    assert len(cases) == 9
    return cases


def all_cases() -> list[Case]:
    base = incidence_cases()
    by_key = {case.key: case for case in base}
    hard_keys = HARD_LINE_KEYS | HARD_INSIDE_KEYS
    cases = [case for case in base if case.key not in hard_keys]
    for key in sorted(HARD_LINE_KEYS):
        cases.extend(hard_line_refinements(by_key[key]))
    for key in sorted(HARD_INSIDE_KEYS):
        cases.extend(hard_inside_refinements(by_key[key]))
    cases.extend(endpoint_cases())
    assert len(cases) == 317
    assert len({case.key for case in cases}) == len(cases)
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
  return(C[ff,1]*rows[rr,1]+C[ff,2]*rows[rr,2]
        +C[ff,3]*rows[rr,3]+C[ff,4]*rows[rr,4]);
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

proc sparse_edge_ideal(matrix rows,int edge_type)
{{
  ideal I;
  int first=1;
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
              // parallel: free edge (i,j)=(0,1), varying k.
              // transverse: free edge (i,k)=(0,1), varying j.
              if (((edge_type==0)&&((i!=0)||(j!=1)))
                  ||((edge_type==1)&&((i!=0)||(k!=1))))
              {{
                value=polarized_product(1+a,3+b,5+c,1+i,3+j,5+k,rows);
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
                if (first) {{ I=value; first=0; }} else {{ I=I,value; }}
              }}
            }}
          }}
        }}
      }}
    }}
  }}
  return(I);
}}

proc emit_case(string key,matrix rows,int edge_type,int tracked)
{{
  ideal I=sparse_edge_ideal(rows,edge_type);
  ideal G;
  matrix transform;
  if (tracked)
  {{
    G=liftstd(I,transform);
  }}
  else
  {{
    G=slimgb(I);
    transform=lift(I,G);
  }}
  int unit_column=0;
  int gi;
  for (gi=1;gi<=size(G);gi++)
  {{
    if ((G[gi]!=0)&&(deg(G[gi])==0)) {{ unit_column=gi; }}
  }}
  if (unit_column==0) {{ print("ERROR|nonunit|"+key); }}
  if ((size(I)!=48)||(nrows(transform)!=48))
  {{
    print("ERROR|bad_transform_rows|"+key+"|"+string(size(I))
          +"|"+string(nrows(transform)));
  }}
  poly unit_value=G[unit_column];
  poly check=0;
  for (gi=1;gi<=48;gi++)
  {{
    check=check+I[gi]*transform[gi,unit_column]/unit_value;
  }}
  if (simplify(check-1,2)!=0) {{ print("ERROR|bad_lift|"+key); }}

  print("CASE|"+key);
  intvec exponent;
  poly multiplier;
  for (gi=1;gi<=48;gi++)
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


def physical_singular_extension() -> str:
    return r"""
proc physical_sparse_edge_ideal(matrix rows)
{
  ideal I=sparse_edge_ideal(rows,0);
  int a,b,c,i,k;
  poly value;
  // The seventh row is the nonzero physical middle row v.  Its complete
  // selected-source contraction per(R,v,Q) vanishes coefficientwise.
  for (a=0;a<=1;a++)
  {
    for (b=0;b<=1;b++)
    {
      for (c=0;c<=1;c++)
      {
        for (i=0;i<=1;i++)
        {
          for (k=0;k<=1;k++)
          {
            value=polarized_product(1+a,3+b,5+c,1+i,7,5+k,rows);
            I=I,value;
          }
        }
      }
    }
  }
  return(I);
}

proc emit_physical_case(string key,matrix rows)
{
  ideal I=physical_sparse_edge_ideal(rows);
  ideal G=slimgb(I);
  matrix transform=lift(I,G);
  int unit_column=0;
  int gi;
  for (gi=1;gi<=size(G);gi++)
  {
    if ((G[gi]!=0)&&(deg(G[gi])==0)) { unit_column=gi; }
  }
  if (unit_column==0) { print("ERROR|nonunit|"+key); }
  if ((size(I)!=80)||(nrows(transform)!=80))
  {
    print("ERROR|bad_transform_rows|"+key+"|"+string(size(I))
          +"|"+string(nrows(transform)));
  }
  poly unit_value=G[unit_column];
  poly check=0;
  for (gi=1;gi<=80;gi++)
  {
    check=check+I[gi]*transform[gi,unit_column]/unit_value;
  }
  if (simplify(check-1,2)!=0) { print("ERROR|bad_lift|"+key); }

  print("CASE|"+key);
  intvec exponent;
  poly multiplier;
  for (gi=1;gi<=80;gi++)
  {
    multiplier=transform[gi,unit_column]/unit_value;
    while (multiplier!=0)
    {
      exponent=leadexp(multiplier);
      print("TERM|"+string(gi)+"|"+string(leadcoef(multiplier))
            +"|"+string(exponent));
      multiplier=multiplier-lead(multiplier);
    }
  }
}
"""


def case_block(index: int, case: Case) -> str:
    del index
    matrix_name = "rows"
    rows = case.rows if case.physical_v is None else (*case.rows, case.physical_v)
    lines = [f"matrix {matrix_name}[6][4];"]
    if case.physical_v is not None:
        lines[0] = f"matrix {matrix_name}[7][4];"
    for row_index, row in enumerate(rows, start=1):
        for coordinate, value in enumerate(row, start=1):
            if value != "0":
                lines.append(f"{matrix_name}[{row_index},{coordinate}]={value};")
    if case.physical_v is None:
        edge_type = 0 if case.edge == "parallel" else 1
        tracked = int(case.key.endswith("_equal"))
        lines.append(
            f'emit_case("{case.key}",{matrix_name},{edge_type},{tracked});'
        )
    else:
        lines.append(f'emit_physical_case("{case.key}",{matrix_name});')
    lines.append(f"kill {matrix_name};")
    return "\n".join(lines) + "\n"


def singular_program(cases: list[Case] | None = None) -> str:
    selected = all_cases() if cases is None else cases
    kinds = {case.physical_v is not None for case in selected}
    if len(kinds) != 1:
        raise ValueError("Singular leaves must not mix table and physical cases")
    extension = physical_singular_extension() if True in kinds else ""
    return singular_prelude() + extension + "\n".join(
        case_block(index, case) for index, case in enumerate(selected)
    )


class LeafFailure(RuntimeError):
    """A bounded Singular leaf did not produce a checked certificate."""


def singular_command(timeout_seconds: int, memory_gib: int) -> list[str]:
    direct = shutil.which("Singular")
    if direct:
        command = [direct, "-q"]
        prlimit = shutil.which("prlimit")
        timeout = shutil.which("timeout")
        if memory_gib and not prlimit:
            raise SystemExit(
                "a native Singular was found, but prlimit is unavailable; "
                "pass --memory-gib 0 only after arranging an external RSS cap"
            )
        if timeout:
            command = [timeout, "--signal=KILL", str(timeout_seconds), *command]
        if memory_gib:
            command = [
                prlimit,
                f"--as={memory_gib * 1024**3}",
                "--",
                *command,
            ]
        return command
    if shutil.which("wsl"):
        if memory_gib:
            return [
                "wsl",
                "--exec",
                "/usr/bin/prlimit",
                f"--as={memory_gib * 1024**3}",
                "--",
                "/usr/bin/timeout",
                "--signal=KILL",
                str(timeout_seconds),
                "/usr/bin/Singular",
                "-q",
            ]
        return [
            "wsl",
            "--exec",
            "/usr/bin/timeout",
            "--signal=KILL",
            str(timeout_seconds),
            "/usr/bin/Singular",
            "-q",
        ]
    raise SystemExit("Singular was not found directly or through WSL")


def run_singular(program: str, timeout_seconds: int, memory_gib: int) -> str:
    command = singular_command(timeout_seconds, memory_gib)
    try:
        completed = subprocess.run(
            command,
            input=program,
            text=True,
            capture_output=True,
            check=False,
            timeout=timeout_seconds + 15,
        )
    except subprocess.TimeoutExpired as error:
        raise LeafFailure(
            f"Singular wrapper exceeded {timeout_seconds + 15} seconds"
        ) from error
    if completed.returncode:
        raise LeafFailure(
            f"Singular failed with code {completed.returncode}:\n"
            f"{completed.stdout}\n{completed.stderr}"
        )
    if "ERROR|" in completed.stdout or "   ?" in completed.stdout:
        raise LeafFailure(completed.stdout)
    return completed.stdout


def parse_output(
    stdout: str,
    selected_cases: list[Case] | None = None,
) -> dict[str, object]:
    selected = all_cases() if selected_cases is None else selected_cases
    specifications = {case.key: case for case in selected}
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
                raise SystemExit(f"unexpected case {key}")
            current = [[] for _ in range(specifications[key].generator_count)]
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
        raise SystemExit(f"case mismatch: missing={missing}, extra={extra}")
    return {
        "format": "sparse-nullstellensatz-v1",
        "variable_order": list(VARIABLES),
        "generator_order": (
            "first_48_source_bits_then_nonexceptional_row_bits_lexicographic;"
            " physical_tail_source_bits_then_RQ_row_bits_lexicographic"
        ),
        "case_kinds": {
            key: ("physical_80" if case.physical_v is not None else "table_48")
            for key, case in specifications.items()
        },
        "case_stages": {key: case.stage for key, case in specifications.items()},
        "refinement_parents": {
            key: case.parent
            for key, case in specifications.items()
            if case.parent is not None
        },
        "cases": cases,
    }


def checked_leaf_output(stdout: str, case: Case) -> str:
    parse_output(stdout, [case])
    return stdout


SPECIFICATION_KEY = "__SPECIFICATION__"


def normalized_singular_program(case: Case) -> str:
    """Render one leaf with a key-free display label before hashing.

    Rendering first is essential: the table solver strategy is already
    frozen into the emitted call and must not accidentally change when the
    display key is replaced.
    """

    program = singular_program([case])
    quoted_key = f'"{case.key}"'
    if program.count(quoted_key) != 1:
        raise AssertionError(f"display key did not occur exactly once: {case.key}")
    return program.replace(quoted_key, f'"{SPECIFICATION_KEY}"', 1)


def specification_case(case: Case) -> Case:
    return Case(
        SPECIFICATION_KEY,
        case.edge,
        case.rows,
        case.physical_v,
        case.stage,
        case.parent,
    )


def checked_specification_output(stdout: str, case: Case) -> str:
    parse_output(stdout, [specification_case(case)])
    return stdout


def legacy_cache_path(cache_dir: Path, case: Case, digest: str) -> Path:
    return cache_dir / f"{case.key}-{digest[:20]}.out"


def specification_cache_path(cache_dir: Path, digest: str) -> Path:
    return cache_dir / f"spec-{digest}.out"


def normalized_legacy_output(stdout: str, case: Case) -> str:
    checked_leaf_output(stdout, case)
    marker = f"CASE|{case.key}"
    if stdout.count(marker) != 1:
        raise ValueError(f"legacy output has a bad case marker: {case.key}")
    normalized = stdout.replace(marker, f"CASE|{SPECIFICATION_KEY}", 1)
    return checked_specification_output(normalized, case)


def write_atomic(path: Path, value: str) -> None:
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(value, encoding="utf-8", newline="\n")
    temporary.replace(path)


def argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cache-dir",
        type=Path,
        default=Path(tempfile.gettempdir()) / "krenn_gu_s2ce_offdiag_v1",
        help="durable per-leaf cache (default: system temporary directory)",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=120,
        help="hard wall-clock limit passed to each Singular leaf",
    )
    parser.add_argument(
        "--memory-gib",
        type=int,
        default=8,
        help="per-leaf address-space ceiling; zero requires an external cap",
    )
    parser.add_argument(
        "--only",
        action="append",
        default=[],
        help="run only case keys containing this substring (repeatable)",
    )
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        help="exclude case keys containing this substring (repeatable)",
    )
    parser.add_argument(
        "--max-cases",
        type=int,
        help="stop after this many selected leaves (exploration only)",
    )
    parser.add_argument(
        "--keep-going",
        action="store_true",
        help="continue after bounded leaf failures and report them together",
    )
    return parser


def main() -> None:
    arguments = argument_parser().parse_args()
    if arguments.timeout_seconds <= 0 or arguments.memory_gib < 0:
        raise SystemExit("timeout must be positive and memory cap nonnegative")

    coverage_cases = all_cases()
    if arguments.only:
        coverage_cases = [
            case
            for case in coverage_cases
            if any(fragment in case.key for fragment in arguments.only)
        ]
    if arguments.exclude:
        coverage_cases = [
            case
            for case in coverage_cases
            if not any(fragment in case.key for fragment in arguments.exclude)
        ]
    if arguments.max_cases is not None:
        if arguments.max_cases <= 0:
            raise SystemExit("--max-cases must be positive")
        coverage_cases = coverage_cases[: arguments.max_cases]
    if not coverage_cases:
        raise SystemExit("no cases matched the requested filters")

    specifications: dict[str, Case] = {}
    programs: dict[str, str] = {}
    coverage_to_specification: dict[str, str] = {}
    for case in coverage_cases:
        program = normalized_singular_program(case)
        digest = hashlib.sha256(program.encode("utf-8")).hexdigest()
        coverage_to_specification[case.key] = digest
        if digest in specifications:
            if programs[digest] != program:
                raise AssertionError("SHA-256 collision between leaf programs")
            continue
        specifications[digest] = case
        programs[digest] = program

    arguments.cache_dir.mkdir(parents=True, exist_ok=True)
    certificates: dict[str, list[list[list[object]]]] = {}
    failures: list[tuple[str, str]] = []
    total = len(specifications)
    for index, (digest, case) in enumerate(specifications.items(), start=1):
        program = programs[digest]
        cached = specification_cache_path(arguments.cache_dir, digest)
        started = time.monotonic()
        try:
            if cached.exists():
                stdout = checked_specification_output(
                    cached.read_text(encoding="utf-8"), case
                )
                source = "cache"
            else:
                legacy_program = singular_program([case])
                legacy_digest = hashlib.sha256(
                    legacy_program.encode("utf-8")
                ).hexdigest()
                legacy = legacy_cache_path(
                    arguments.cache_dir, case, legacy_digest
                )
                if legacy.exists():
                    stdout = normalized_legacy_output(
                        legacy.read_text(encoding="utf-8"), case
                    )
                    source = "legacy cache"
                else:
                    stdout = checked_specification_output(
                        run_singular(
                            program,
                            arguments.timeout_seconds,
                            arguments.memory_gib,
                        ),
                        case,
                    )
                    source = "Singular"
                write_atomic(cached, stdout)
            parsed = parse_output(stdout, [specification_case(case)])
            parsed_cases = parsed["cases"]
            if not isinstance(parsed_cases, dict):
                raise ValueError("parsed cases are not a dictionary")
            certificates[digest] = parsed_cases[SPECIFICATION_KEY]
            elapsed = time.monotonic() - started
            print(
                f"[{index}/{total}] {case.key} [{digest[:12]}]: "
                f"PASS via {source} "
                f"({elapsed:.2f}s)",
                flush=True,
            )
        except (LeafFailure, OSError, ValueError) as error:
            elapsed = time.monotonic() - started
            message = str(error).strip().replace("\n", " | ")
            failures.append((case.key, message))
            print(
                f"[{index}/{total}] {case.key}: FAIL ({elapsed:.2f}s): "
                f"{message}",
                flush=True,
            )
            if not arguments.keep_going:
                raise SystemExit(1) from error

    if failures:
        print("bounded leaf failures:")
        for key, message in failures:
            print(f"  {key}: {message}")
        raise SystemExit(1)

    term_count = sum(
        len(multiplier)
        for case_data in certificates.values()
        for multiplier in case_data
    )
    if {case.key for case in coverage_cases} != {
        case.key for case in all_cases()
    }:
        print(
            f"selected_coverage_cases={len(coverage_cases)} "
            f"unique_specifications={len(specifications)} terms={term_count}; "
            "no JSON written"
        )
        return
    data = {
        "format": "sparse-nullstellensatz-atlas-v2",
        "variable_order": list(VARIABLES),
        "generator_order": (
            "first_48_source_bits_then_nonexceptional_row_bits_lexicographic;"
            " physical_tail_source_bits_then_RQ_row_bits_lexicographic"
        ),
        "coverage_case_count": len(coverage_cases),
        "certificate_specification_count": len(specifications),
        "coverage_case_to_specification": coverage_to_specification,
        "coverage_case_kinds": {
            case.key: (
                "physical_80" if case.physical_v is not None else "table_48"
            )
            for case in coverage_cases
        },
        "coverage_case_stages": {
            case.key: case.stage for case in coverage_cases
        },
        "coverage_refinement_parents": {
            case.key: case.parent
            for case in coverage_cases
            if case.parent is not None
        },
        "specifications": {
            digest: {
                "representative": case.key,
                "program_sha256": digest,
                "kind": (
                    "physical_80"
                    if case.physical_v is not None
                    else "table_48"
                ),
                "edge": case.edge,
                "rows": case.rows,
                "physical_v": case.physical_v,
            }
            for digest, case in specifications.items()
        },
        "cases": certificates,
    }
    write_atomic(
        OUTPUT,
        json.dumps(data, sort_keys=True, separators=(",", ":")) + "\n",
    )
    print(f"wrote {OUTPUT}")
    print(
        f"coverage_cases={len(coverage_cases)} "
        f"unique_specifications={len(specifications)} terms={term_count}"
    )


if __name__ == "__main__":
    main()
