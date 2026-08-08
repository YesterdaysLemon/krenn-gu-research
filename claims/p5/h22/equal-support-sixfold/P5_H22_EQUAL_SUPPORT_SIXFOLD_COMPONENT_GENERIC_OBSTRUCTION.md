# Weighted `H22` obstruction on the eleventh (equal-support sixfold) component

## Status

This is an exact characteristic-zero theorem on the eleventh certified
pure-`P_4` component orbit
([`P4_EQUAL_SUPPORT_SIXFOLD_PURE_COMPONENT.md`](../../../p4/components/equal-support-sixfold/P4_EQUAL_SUPPORT_SIXFOLD_PURE_COMPONENT.md)),
companion to the marked `H31` theorem
[`P5_H31_EQUAL_SUPPORT_SIXFOLD_COMPONENT_GENERIC_OBSTRUCTION.md`](../../h31/equal-support-sixfold/P5_H31_EQUAL_SUPPORT_SIXFOLD_COMPONENT_GENERIC_OBSTRUCTION.md)
and using its gauge.

The generic weighted `H22` incidence of the component is empty — and
unlike the earlier `H22` theorems in this repository, **no slope
divisor is left open at the covered points**: the slope is eliminated
as a ring variable in the marking projections, and the finitely many
slopes where that elimination degenerates (`r=1,-1,0,infinity`) are each
closed by a separate exact argument.

Not claimed: the component's projective boundary, component
exhaustiveness, the `H22` census as a whole, and the global prize
problem.

## Pencils and the dead one

With the `H31` gauge `(v_0,v_1,t,v_2,x_2,v_3)=(1,1,1,0,0,1)` over
`C(c_0,c_1,c_2,d)`, the restriction is the single unit word `T_1111=2`.
The two weighted pencils are

```text
D_01^r(u)=(r u_0+u_1, u_2, u_3, ext),
D_23^r(u)=(u_0, u_1, r u_2+u_3, ext).                   (1)
```

**The `D_23` pencil is identity-dead.**  Its word-`0000` coefficient
vanishes identically over
`Z[c_0,c_1,c_2,t,v,x_2,x_3,r,t,z]`: there is no sharp `Delta_2`
extension at *any* slope, marking, or chart point — the same
`Pi`-confinement mechanism that kills the `H31` frames `q=2,3`.

## The `D_01` pencil interpolates the two live `H31` frames

All sixteen words satisfy the identity

```text
D_01^r word = r*(H31 q=1 word) + (H31 q=0 word),        (2)
```

so `r=0` and `r=infinity` are exactly the two live `H31` frames and are
closed by the companion theorem.  The diagonal `A`-row is

```text
(r-1)*(0, c_0-c_2, c_0-c_1, -(c_1+c_2))  on (x_0..x_3),  (3)
```

`t`-free and **dead at the equal-weight slope `r=1`**.  The doubled
column satisfies `D0_w + D1_w = 0` for `w != 1111` and `= 4` at
`w = 1111`, and the extension `ext_i = row_i[0] + r*row_i[1]` gives a
universal kernel

```text
M z*=0,   A z*=0,   B z*=2(r+1)^2,                      (4)
```

degenerate exactly at `r=-1`.  The source transposition `(01)` maps
`D_01^r` to `r*D_01^{1/r}`, so the slope line is covered by its own
symmetry.

## All-slope marking projections and the survivor locus

The marking projections are computed with the slope kept as a **ring
variable** and come out as unit ideals, so they cover every slope at
once rather than a generic one.  With the parameters as ring variables,
the `(z,w,t)`-elimination of the genuine pencil incidence over `C(r)` —
and, independently, at the fixed rational slopes `2` and `1/2` — equals
the `H31` survivor locus

```text
( a^2 b c e (e+1),  a^2 b c e (b-c) ),
a=c_0, b=c_1, c=c_2, e=d,                               (5)
```

that is, the same five strata

```text
{c_0=0}, {c_1=0}, {c_2=0}, {d=0}, {c_1=c_2, d=-1}.      (6)
```

At `r=-1` the elimination gives the **unit ideal** (empty); at `r=1` the
pencil is identity-dead by (3); at `r=0,infinity` it is the `H31` loci
by the interpolation identity (2).

## Ternary closure and the support split

Each stratum of (6) splits into the same explicit marking sheets as in
the `H31` theorem, and on every sheet the mode-`0` one-marked
contraction has rank four by a single-minor unit certificate (rows
`(0,2,4,7)`, with `(0,2,5,7)` and `(0,2,3,7)` on the extra `c_0=0`
sheets) — these certificates are again run with the slope eliminated,
so they hold at all slopes on the sheet.

Finally the `H22` subfamily bookkeeping: a subfamily with `b != 0`
requires a sharp `D_23` image, which is impossible identically; one
with `a != 0` requires a sharp `D_01` image, which is empty by the
all-slope unit projection; and `(a,b) != (0,0)` always.  Hence

**the generic weighted `H22` incidence of the eleventh component is
empty, with no open slope divisor at the covered points.**

## Verification

Run

```text
python claims/p5/h22/equal-support-sixfold/verify_p5_h22_equal_support_sixfold_component_generic_obstruction.py
```

(after the `H31` companion, whose theorem file it hashes as a
dependency).  The verifier checks the `D_23` identity, the
interpolation identity (2), the `A`-row (3), the doubled-column
identity, the universal kernel (4) and its `r=-1` degeneration, the
swap covariance, the rank-seven witness, the all-slope unit marking
projections, the pencil survivor-locus eliminations over `C(r)` and at
fixed slopes, the `r=-1` unit ideal, each sheet ideal, and each
all-slope Fitting certificate.  Fail-closed throughout: a Singular
timeout or mismatch raises.

## Honest frontier

Closed slopes: all of them at the covered parameter points — the
elimination covers the generic slope, and `1`, `-1`, `0`, `infinity`
are closed individually.  Open: the component's projective boundary,
the degeneration strata of the gauge itself, component exhaustiveness,
the rest of the `H22` census, and the global prize conjecture.
