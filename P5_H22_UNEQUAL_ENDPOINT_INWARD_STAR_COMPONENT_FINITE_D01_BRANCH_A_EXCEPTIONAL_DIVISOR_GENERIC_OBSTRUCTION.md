# Generic obstruction on component twenty-five's exceptional finite-`D01` `A` divisor

## Status

**Exact characteristic-zero divisor-generic theorem.**  The rational terminal
section on

```text
d_A=(js-1)lambda-(js+1)=0                         (1)
```

does not give a genuine weighted-`H22` neighbour.  Its unique normalized
marking makes the finite-`D01` all-beta diagonal identically zero over the
component function field.  Independently, a fixed paired finite-`D23`
one-marked minor is nonzero on a dense open subset of the divisor.

This closes the **divisor-generic terminal section**, not every special or
projective fibre in its closure.  The parallel `B=0` branch is untouched.
The global Krenn--Gu conjecture remains **UNRESOLVED**.

## Section and forced marking

Put

```text
P=ej+k^2,       Q=e+j,       R=1+ejs^2,
F=PR-Q^2,
K=C(e,j,s)[k]/(F).
```

The preceding exact section begins

```text
lambda=(js+1)/(js-1),
w=-(js-1)^2R/[16s(e-j)Q^2k],
z_3=-(js-1)/[4(e^2-k^2)P],
z_6=-j(js-1)R/[8kQ^2(e-j)],                       (2)
```

with `z_5,z_1,z_7,z_0` recovered by its four linear equations.  Normalize
the unmarked finite-`D01` coefficient `C_0000=1`.  The four singleton
equations uniquely force

```text
h_0=0,
h_1=-e/(e^2-k^2),
h_2=-js,
h_3=-j(2e^2j^2s^2-e^2-j^2)/[k(e-j)R].            (3)
```

Here marking acts on each complete projected row, including its extension
entry:

```text
beta'_i -> beta'_i+h_i alpha'_i.                  (4)
```

Forgetting the extension term in (4) gives an incorrect rank calculation.

## Uniform nongenuine diagonal

Substitute (2)--(4) into the marked finite-`D01` all-beta coefficient.  Exact
reduction of its numerator modulo `F` gives

```text
NF_F(C_1111^marked)=0.                             (5)
```

Thus the opposite pure diagonal vanishes identically in `K`.  The populated
terminal ideal found previously is the closure obtained by leaving that
opposite coordinate free; its rational section is not a genuine binary
neighbour.  Equation (5), rather than a finite specialization, is the primary
divisor-generic obstruction.

## Independent paired-`D23` minor

Project the same completely marked lifted rows through finite `D23` at the
weight (2).  For marked mode one, take lexicographic ternary rows
`0,4,5,6`, or words `000,100,101,110`.  Exact quotient reduction gives

```text
det N^D23_1[0456]

 = (jks-e)(js-1)(js+1)R^2
   -----------------------------------------------                 (6)
   4k^3s^2(e-j)^2Q^4(e^2-k^2)
```

as an equality in `K`.  At the rational point

```text
(e,j,k,s)=(-5,2,3,-1)
```

equation (6) is `-1/28224`, recovering the point certificate.

On the standing ordinary chart, `js`, `js-1`, `R`, `k`, `e-j`, `Q`, and
`e^2-k^2` are units.  Consequently the selected minor is nonzero away from
the exact internal factor divisor

```text
(js+1)(jks-e)=0.                                  (7)
```

The two pieces of (7) are boundaries of this chosen ternary minor, not
residual survivors of the theorem: the uniform diagonal identity (5) still
excludes the rational section wherever formulas (2)--(4) remain defined.

## Boundaries and replay

The coefficient field localizes base parameters.  The original component
chart assumes

```text
P R k Q (e-j)(e^2-k^2)(lambda^2-1) != 0.
```

Its omitted base divisors, projective component limits, and the `B=0` branch
remain outside this theorem.  In particular, this package does not upgrade
the full component-twenty-five weighted-`H22` fibre to closed.  No
finite-field computation is used.

Run:

```text
uv run --with sympy python \
  verify_p5_h22_unequal_endpoint_inward_star_component_finite_d01_branch_a_exceptional_divisor_generic_obstruction.py

uv run --with sympy python \
  audit_p5_h22_unequal_endpoint_inward_star_component_finite_d01_branch_a_exceptional_divisor_generic_obstruction.py
```

Both replays work directly in the quadratic component field using
`P=Q^2/R` and `k^2=Q^2/R-ej`.  The primary uses the certified component basis
to verify `C_0000=1`, all four marking formulas, and the paired `D23` minor
(6).  The audit imports no project code and independently rebuilds the basis,
section, normalization, marking, and uniform `D01` diagonal identity (5).
All computations are exact over characteristic zero.
