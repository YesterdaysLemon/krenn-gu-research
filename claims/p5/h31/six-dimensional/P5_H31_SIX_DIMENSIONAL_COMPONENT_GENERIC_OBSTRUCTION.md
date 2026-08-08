# Generic marked `H31` obstruction on the six-dimensional `P_4` component

## Status

This is an exact characteristic-zero theorem on a dense open subset of
the six-dimensional component proved in
[`P4_SIX_DIMENSIONAL_PURE_COMPONENT.md`](../../../p4/components/six-dimensional/P4_SIX_DIMENSIONAL_PURE_COMPONENT.md).

The complete marked-basis fibre over the generic point of that
component has no `H31` lift.  The theorem does not close special
parameter divisors or projective boundary points, classify every pure
`P_4` component, settle `H22`, or resolve the global prize problem.

## Apolar coordinates

The component normal form depends on `a,c` only through their sum.
On the dense chart `s=a+c!=0`, put

```text
u=1-sb,              v=1-se,              h=s-d.
```

After multiplying both rows of the second plane by `s`, use

```text
U_0=span(
 (1,0,0,-1),
 (0,0,1, 1)),

U_1=span(
 (s,1-u,0,d+uh),
 (0,1-v,s,d+vh)),

U_2=span(
 (1,0,-1, 0),
 (0,1,-s,-d)),

U_3=span(
 (1,0,0, 1),
 (0,0,1,-1)).                                    (1)
```

Choose pure-factor bases `(alpha_i,beta_i)` as

```text
alpha_0=(1,0,0,-1),
 beta_0=(0,0,1, 1),

alpha_1=(sv,v-u,-su,d(v-u)),
 beta_1=(s,1-u,0,d+u(s-d)),

alpha_2=(1,0,-1,0),
 beta_2=(0,1,-s,-d),

alpha_3=(0,0,1,-1),
 beta_3=(1,0,0, 1).                              (2)
```

The middle kernel row in (2) is simply

```text
v U_1[0]-u U_1[1].
```

Every restricted coefficient vanishes except

```text
T_BBBB=2su.                                       (3)
```

Every marking of the same four planes is therefore represented, up to
irrelevant row scalings, by

```text
beta_i(t)=beta_i+t_i alpha_i.                     (4)
```

## Exact marked projection

For distinguished source coordinate `q`, let `M_q(t)` be the
`14 x 8` mixed-coefficient matrix of a neighbouring binary slice, and
let `A_q,B_q` be its two diagonal coefficient rows.  A genuine
neighbouring `Delta_2` direction `z` requires

```text
M_q(t)z=0,             A_qz B_qz !=0.             (5)
```

Eliminate `z` over `C(s,d,u,v)`, normalizing `A_qz=1` and inverting
`B_qz`.  For `q=1`, the projected marking ideal is the unit ideal.

For each of `q=0,2,3`, there is exactly one rational marking.  Put

```text
tau=(1-u)/(u-v),       sigma=sv/(u-v).             (6)
```

The three markings are

```text
q=0:  (t_0,t_1,t_2,t_3)=(1,tau,sigma,0),
q=2:  (t_0,t_1,t_2,t_3)=(0,tau,sigma,1),
q=3:  (t_0,t_1,t_2,t_3)=(0,tau,sigma,0).          (7)
```

There are no hidden marking sheets over the function field.

The special role of `q=1` has a geometric explanation.  For every
marking, the vector obtained by restoring the deleted coordinate,

```text
z=(alpha_i[1], beta_i(t)[1])_{i=0}^3,
```

lies in `ker M_1(t)`.  It reconstructs the original pure restriction,
so

```text
A_1z=0,              B_1z=2su.                    (8)
```

Thus the ubiquitous kernel line is a pure reconstruction direction,
not a binary `Delta_2` direction.  The exact unit projection proves
that every possible rank jump retains this obstruction on the generic
component; exceptional parameter specializations are deliberately
left to the boundary problem.

## Three small Fitting certificates

It remains to exclude every extension direction over the three
markings in (7).  For each marking, adjoin the fourteen equations
`M_qz=0`, three selected `4 x 4` minors of the mode-zero one-marked
map, and

```text
w(A_qz)(B_qz)-1.
```

Over `C(s,d,u,v)` the resulting ideal is `(1)` in all three cases.
The selected row sets are

```text
q=0:  0127, 0137, 0147,
q=2:  0267, 0367, 0467,
q=3:  0127, 0137, 0147.                            (9)
```

Consequently, whenever both binary diagonal coefficients are nonzero,
at least one minor in (9) is nonzero.  The corresponding marked local
map has rank four, whereas an `H31` lift has only three target
coordinates.  Every genuine binary extension is therefore
incompatible with a ternary lift.

Combining the unit projection for `q=1`, the complete projection (7),
and the unit Fitting ideals (9) proves that the generic marked `H31`
fibre is empty.

## Verification

Run

```text
python claims/p5/h31/six-dimensional/verify_p5_h31_six_dimensional_component_generic_obstruction.py
python claims/p5/h31/six-dimensional/audit_p5_h31_six_dimensional_component_generic_obstruction.py
```

The primary verifier checks (1)--(4), performs the four exact
function-field projections, verifies the reconstruction direction
(8), and rebuilds all three characteristic-zero Fitting certificates.
The independent audit uses a separate dynamic-programming permanent
and finite-field linear algebra.  It exhausts every marked basis at
two generic modular samples and every genuine projective extension
direction, then replays the three-minor obstruction.  The modular
audit is corroboration only; the theorem is the characteristic-zero
calculation.

## Honest frontier

All seven currently certified pure-component orbits now have empty
generic marked `H31` fibre.  This does not make the component list
exhaustive and does not close the boundary of the new component.  The
remaining `H31` work is the special parameter/projective boundary of
the incompletely closed components together with completeness of the
pure-`P_4` component classification.
