# Marked `H31` obstruction on the eleventh (equal-support sixfold) component

## Status

This is an exact characteristic-zero theorem on the eleventh certified
pure-`P_4` component orbit, the equal-support sixfold of
[`P4_EQUAL_SUPPORT_SIXFOLD_PURE_COMPONENT.md`](claims/p4/components/equal-support-sixfold/P4_EQUAL_SUPPORT_SIXFOLD_PURE_COMPONENT.md).

The complete marked-basis `H31` fibre over the generic point of that
component is empty, and the theorem goes one step past the generic
statement: the parameter locus that could carry a genuine binary
survivor is computed **exactly** as an elimination ideal, it is a union
of five explicit strata, and every sheet of every one of those five
strata is then closed by a single-minor ternary Fitting certificate.
So no open interior parameter divisor is left behind on the live
frames.

What is *not* claimed: the component's projective boundary, component
exhaustiveness for the pure-`P_4` locus, the `H31` census as a whole,
and the global prize problem all remain open.  The companion weighted
`H22` theorem is
[`P5_H22_EQUAL_SUPPORT_SIXFOLD_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H22_EQUAL_SUPPORT_SIXFOLD_COMPONENT_GENERIC_OBSTRUCTION.md).

## Gauge and normal form

Write the eleventh component's family as in the component theorem,

```text
U_0=span((v_0,-v_1,0,0),(0,0,1,-c_0)),
U_1=span((0,0,1,-c_1),v),
U_2=span((0,0,1,-c_2),(t v_0,t v_1,x_2,x_3)),
U_3=Pi=span(X_2,X_3).
```

Row operations inside the planes, the diagonal source torus, and the
substitution

```text
d=(x_3+c_2 x_2)/(t(v_3+c_1 v_2))
```

normalize

```text
(v_0,v_1,t,v_2,x_2,v_3)=(1,1,1,0,0,1),                (1)
```

leaving the function field `C(c_0,c_1,c_2,d)`.  In this gauge the
restriction is the **single word**

```text
T_1111=2,                                              (2)
```

a unit: the component carries no pure-coefficient divisor, and the
marked tensor is identically (2) for *every* marking `t`.

## Two identity-dead frames

For the coordinate deletions `q=2` and `q=3` the entire `0000`-diagonal
row vanishes identically over
`Z[c_0,c_1,c_2,t,v_0..v_3,x_2,x_3,t_0..t_3]`.  The mechanism is
structural: the three kernel rows

```text
alpha_1=w_{c_1},   alpha_2=w_{c_2},   alpha_3=(0,0,1,c_0)
```

all lie in `Pi=span(X_2,X_3)`; deleting column `2` or `3` confines them
to a single common column, and every `0000` coefficient is a `3x3`
permanent containing at least two of them.  Hence no genuine binary
`Delta_2` neighbour exists in these frames, for any marking, at any
chart point.

## The two live frames

For `q=0,1` the diagonal `A`-row is `t`-free,

```text
A^{(0)}=(0, c_2-c_0, c_1-c_0, c_1+c_2)  on (x_0,x_1,x_2,x_3),
A^{(1)}=-A^{(0)},                                       (3)
```

and restoring the deleted column produces a **reconstruction kernel**

```text
M z_rec=0,   A z_rec=0,   B z_rec=2                     (4)
```

identically in `t`.  The mixed rank is exactly seven, witnessed by the
words `0001,0010,0011,0100,0101,0110,1010` against the column sets
`x_0..x_3,y_0,y_2,y_3` (`q=0`) and `x_0..x_3,y_0,y_1,y_3` (`q=1`).

The source transposition `(01)` fixes the family and carries the `q=0`
frame to the `q=1` frame verbatim (all sixteen word forms equal, same
marking), so the two live frames are one statement.  The mode-`(12)`
swap composed with `diag(1,1,1/d,1/d)` acts on parameters by
`(c_0,c_1,c_2,d) -> (c_0,c_2,c_1,1/d)`.

Over the generic point both live frames give **unit marking
projections**: the projection ideal is `(1)` for `q=0,1`.

## The exact interior survivor locus

Eliminating `(z,w,t_0..t_3)` from the fourteen mixed words together
with `w A B - 1`, with the parameters kept as ring variables, gives
exactly

```text
( a^2 b c e (e+1),  a^2 b c e (b-c) ),
a=c_0, b=c_1, c=c_2, e=d.                               (5)
```

Therefore every parameter point carrying a genuine binary survivor in a
live frame lies on one of the five strata

```text
{c_0=0}, {c_1=0}, {c_2=0}, {d=0}, {c_1=c_2, d=-1}.      (6)
```

This is an exact statement about the whole parameter space, not a
generic one: off (6) the binary level is already empty.

## Ternary closure of all five strata

On each stratum the marking ideal factors into explicit sheets, e.g.

```text
c_1=0:  ( c_0 t_3+1, t_2, c_0 t_1+1, t_0 ),
c_2=0:  ( c_0 t_3+1, c_0 t_2+d, t_1, t_0 ),
d=0:    ( (c_0^2-c_1 c_2) t_3+c_0, t_2, (c_0-c_1) t_1+1, t_0 ),
```

with the `c_0=0` stratum carrying three marking sheets and the coupled
stratum `{c_1=c_2, d=-1}` its own two.  On every sheet the mode-`0`
one-marked contraction has rank four, certified by a single `4x4` minor
whose Rabinowitsch ideal is the unit ideal — minor rows `(0,2,4,7)`,
with `(0,2,5,7)` and `(0,2,3,7)` on the two extra `c_0=0` sheets.

A rank-four one-marked contraction admits no ternary lift.  Hence no
`H31` incidence exists over any point of any of the five strata either,
and combining with the unit projections off (6):

**the complete marked `H31` fibre of the eleventh component is empty
over its generic point, with the interior survivor divisors closed
rather than excluded.**

## Verification

Run

```text
python verify_p5_h31_equal_support_sixfold_component_generic_obstruction.py
```

The verifier is self-contained (sympy + Singular).  It checks the raw
support and concentration, the gauge (1) and the forcing that follows
it, the identity-dead frames `q=2,3`, the live-frame `A`-rows (3), the
reconstruction kernel (4), the rank-seven witness, both swap
symmetries, the unit marking projections for `q=0,1`, the exact
elimination (5), each sheet ideal of (6), and each per-sheet Fitting
unit certificate.  Every Singular call is fail-closed: a timeout or a
mismatch raises rather than downgrading a claim.

## Honest frontier

The theorem covers the interior of the component's parameter space in
the gauge (1).  The projective boundary of the component, the strata
where the gauge itself degenerates, component exhaustiveness, the rest
of the `H31` census, and the global prize conjecture are all untouched
and open.
