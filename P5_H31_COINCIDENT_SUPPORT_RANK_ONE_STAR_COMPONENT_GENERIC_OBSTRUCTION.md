# Generic `H31` exclusion for component twenty-one

## Status

**Exact characteristic-zero generic-fibre theorem.**  The complete marked
`H31` fibre over the generic point of the coincident-support rank-one-star
component is empty.

The proof treats every marked basis, every distinguished source coordinate,
and every projective extension direction.  Two deletions fail by Hall
deficiency.  For the other two, the all-kernel diagonal is an exact member of
the fourteen-row mixed module over the component function field.  Thus it
vanishes on every mixed kernel before any ternary rank condition is imposed.
No parameter grid or broad elimination is used.

This is a generic theorem.  It does not classify special parameter or
projective component boundaries, close weighted `H22`, prove component
exhaustiveness, or settle the global Krenn--Gu conjecture.

## Intrinsic pure bases

Use the family from
[`P4_COINCIDENT_SUPPORT_RANK_ONE_STAR_COMPONENT.md`](claims/p4/classifications/star/coincident-support-rank-one-star/P4_COINCIDENT_SUPPORT_RANK_ONE_STAR_COMPONENT.md):

```text
A=X0+X1,   C=X0-X1,   B=X2+X3,   D=X2-X3,

U0=span(A+pB,C+qB),
U1=span(A,C),
U2=span(C,B+kappa A),
U3=span(A+ell C,D).                                  (1)
```

Over `K=C(p,q,kappa,ell)`, orient the four planes by

```text
alpha0=q(A+pB)-p(C+qB)=qA-pC,   beta0=A+pB,
alpha1=ell A+C,                  beta1=A,
alpha2=C,                        beta2=B+kappa A,
alpha3=D,                        beta3=A+ell C.        (2)
```

Direct permanent expansion gives

```text
T_w=0 for w!=1111,       T_1111=4p.                 (3)
```

Thus the `alpha_i` are the intrinsic pure-kernel rows.  Every marked basis
over the same generic four-plane point is, after harmless nonzero row
rescaling,

```text
beta_i(t)=beta_i+t_i alpha_i,       i=0,1,2,3.       (4)
```

The source-diagonal torus omitted from (1) does not change the argument.  On
deleting one coordinate, its nonzero scalings act by invertible scalings of
the three retained columns; every permanent uses all retained columns once.
They therefore preserve the mixed kernel and diagonal zero/nonzero tests.

## The marked binary extension

For distinguished source coordinate `d`, delete `d`, append the fifth-source
extension column, and write its eight entries as

```text
z=(x0,x1,x2,x3;y0,y1,y2,y3)^T.                     (5)
```

Let `M_d(t)` be the `14 x 8` matrix of mixed binary coefficients, and let
`a_d(t),b_d(t)` be the all-`alpha` and all-`beta(t)` diagonal rows.  A genuine
binary neighbour requires

```text
M_d(t)z=0,       a_d(t)z != 0,       b_d(t)z != 0.  (6)
```

This condition is necessary for an `H31` lift.

## Deleting `X0` or `X1`: Hall deficiency

The first three kernel rows in (2) are all supported on `{X0,X1}`.  After
deleting either `X0` or `X1` and adjoining the extension column, those three
rows have a common two-column neighbourhood.  Three permanent rows cannot be
matched injectively into two columns.  Consequently

```text
a_0(t)=a_1(t)=0                                      (7)
```

as polynomial row identities, independently of all markings and extension
entries.

## Deleting `X2` or `X3`: a seven-generator row module

For the two remaining deletions, work in the polynomial ring

```text
S=K[t0,t1,t2,t3].                                   (8)
```

Regard the fourteen rows of `M_d` as generators of a submodule of `S^8`.
Exact standard-basis reduction gives

```text
                    d=2          d=3
rank_K(t)(M_d)       7            7
size(std(rows M_d))  7            7
NF(a_d | rows M_d)   0            0
NF(b_d | rows M_d)   nonzero      nonzero.          (9)
```

The zero normal forms in (9) are the needed characteristic-zero identities:

```text
a_d is in rowspan_S(M_d),       d=2,3.              (10)
```

If `M_d(t)z=0`, equation (10) forces `a_d(t)z=0`, including at every special
marking where a rational kernel formula could acquire a pole.  This
contradicts (6).  Together with (7), all four distinguished coordinates are
excluded, so the generic marked `H31` fibre of component twenty-one is empty.

At the exact point `(p,q,kappa,ell)=(2,3,1,2)`, the mixed ranks are
`(2,2,7,7)` and adjoining `b_d` raises them to `(3,3,8,8)`, independently
checking that the certificate is not caused by a zero all-pure diagonal.

## Replay

```text
uv run --with sympy python \
  verify_p5_h31_coincident_support_rank_one_star_component_generic_obstruction.py

uv run --with sympy python \
  audit_p5_h31_coincident_support_rank_one_star_component_generic_obstruction.py
```

The primary verifier reconstructs (1)--(4), checks all sixteen pure
coefficients, constructs all four mixed matrices, and performs the exact
row-module reductions over `C(p,q,kappa,ell)`.  The independent audit uses a
separate permanent implementation and repeats the symbolic marking-module
calculation over `F_101` and `F_103`; those modular checks corroborate but are
not used to infer the characteristic-zero theorem.
