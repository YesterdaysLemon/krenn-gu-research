# Generic marked `H31` obstruction on the sixth pure `P_4` component

## Status

This is an exact characteristic-zero theorem on a dense open subset of
the mixed-orientation component proved in
[`P4_MIXED_ORIENTATION_PURE_COMPONENT.md`](claims/p4/components/mixed-orientation/P4_MIXED_ORIENTATION_PURE_COMPONENT.md).

The complete marked-basis fibre over the generic point of that
component has no `H31` lift.  The theorem does not close special
parameter divisors or projective boundary points, classify all pure
`P_4` components, settle `H22`, or resolve the global prize problem.

## Canonical marked bases

Put

```text
N=q(d+p+q)
```

and use the component planes

```text
U_0=span(
 (-dp, d+q, N,0),
 ( dp,-d-q, 0,N)),

U_1=span(
 (0,0,1,1),
 (-d,1,-p-q,d)),

U_2=span(
 (p,1,0,q),
 (-1,0,1,0)),

U_3=span(
 (1,0,1,0),
 (0,0,-1,1)).                                     (1)
```

Take `alpha_i` to be the second row and `beta_i` the first row of
each plane.  The only nonzero restricted coefficient is

```text
T_BBBB=2N.                                         (2)
```

Every marked basis over the same plane tuple is uniquely represented,
up to irrelevant row scalings, by

```text
beta_i(t)=beta_i+t_i alpha_i.                       (3)
```

## Exact marked projection

Let `r` be the source coordinate removed from the pure hyperplane and
replaced by the fifth source coordinate.  Write the eight extension
entries as `e`, the fourteen mixed binary coefficients as

```text
M_r(t)e,
```

and the two binary diagonal coefficients as `A_r(e),B_r(e)`.  A
genuine neighbouring `Delta_2` slice requires

```text
M_r(t)e=0,       A_r(e)B_r(e) != 0.                (4)
```

Eliminate `e` over `C(d,p,q)`, normalize `A_r(e)=1`, and invert
`B_r(e)`.  For `r=0,1`, the projected marking ideal is the unit ideal.

For `r=2`, the projection is

```text
t_3=0,
d p(p+q)t_1-(d+p+q)t_2+p(p+q)=0,
t_0=1,

((d+q)t_2-pq)
((d+p+q)t_2-p(p+q))=0.                             (5)
```

Thus it has two rational sheets:

```text
2A:
(t_0,t_1,t_2,t_3)
 =(1,-p/((d+q)(p+q)),pq/(d+q),0);

2B:
(t_0,t_1,t_2,t_3)
 =(1,0,p(p+q)/(d+p+q),0).                          (6)
```

For `r=3`, the projection is

```text
(d+p+q)t_2+dp t_3-p(d+p+q)=0,
t_1=0,
t_0=1,

(t_3-1)(d t_3-(d+p+q))=0.                          (7)
```

Its two rational sheets are:

```text
3A:
(t_0,t_1,t_2,t_3)
 =(1,0,p(p+q)/(d+p+q),1);

3B:
(t_0,t_1,t_2,t_3)
 =(1,0,0,(d+p+q)/d).                               (8)
```

Equations (5)--(8) classify the complete function-field marked fibre.

## All-extension determinant identities

On every sheet, the mixed matrix has rank six and hence a
two-dimensional extension kernel.  The following selected
one-marked maps and row minors obey identities modulo the complete
linear ideal `M_r(t)e=0`:

```text
sheet   marked mode   rows        determinant / (A_r B_r^2)

2A          1         0,2,3,7     -p^2 q/(d+p+q)
2B          2         0,1,3,7      d(d+q)/q
3A          3         0,2,6,7     -(d+q)
3B          3         0,2,6,7     -(d+q).           (9)
```

All factors in the last column are nonzero on the stated dense open
set.  Condition (4) therefore makes the selected determinant nonzero
for every genuine extension, so the neighbouring one-marked map is
injective.

The corresponding pure-hyperplane one-marked maps have the following
nonzero entries in source column `r`:

```text
sheet   marked mode   row   entry

2A          1          0    d+q
2B          2          0    d(d+p+q)
3A          3          2    d+q
3B          3          2    d+q.                   (10)
```

Injectivity on the neighbouring hyperplane forces the third target
row at the marked mode to be supported only on the removed coordinate
`r`.  Equation (10) then forces that row to vanish on the pure
hyperplane as well, contradicting the rank-three local map required by
conciseness of `Delta_3`.

Hence:

```text
the complete marked H31 fibre over the generic point of the
mixed-orientation component is empty.               (11)
```

## Exact frontier

All six currently certified pure-`P_4` component orbits now have empty
generic marked fibres; the first two are closed including their
boundaries.  The remaining `H31` work is:

1. close parameter and projective boundaries of `L_1,L_2,L_3`;
2. close the parameter and projective boundary of the
   mixed-orientation component; and
3. determine whether further pure-`P_4` components exist.

The separate `H22` case remains open.

## Verification

Run:

```text
python \
  verify_p5_h31_mixed_orientation_component_generic_obstruction.py

python audit_p5_h31_mixed_orientation_component_generic_obstruction.py
```

The primary verifier reconstructs (1)--(3), performs all four exact
function-field projections, checks the factorization into the four
marking sheets, and uses fresh characteristic-zero reductions modulo
the mixed linear ideals to prove every identity in (9)--(10).

The independent audit imports nothing from the primary verifier.  At
`F_7,F_11` it exhausts every affine marked basis at a nondegenerate
component point, recovers exactly the four projected markings, and
checks every genuine projective extension direction against the
selected injective minor and transverse pure entry.  This finite-field
census is independent QA; the function-field eliminations and
characteristic-zero identities prove the generic theorem over `C`.
