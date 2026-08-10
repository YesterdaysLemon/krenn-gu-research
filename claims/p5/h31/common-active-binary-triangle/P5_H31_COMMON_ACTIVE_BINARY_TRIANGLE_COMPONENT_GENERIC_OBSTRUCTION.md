# Generic `H31` exclusion for component twenty

## Status

**Exact characteristic-zero generic-fibre theorem.**  The complete marked
`H31` fibre over the generic point of the common-active binary-triangle
component is empty.

The proof treats every marked basis, all four distinguished source
coordinates, and every projective extension direction.  Exact projection of
the genuine-binary incidence leaves four isolated markings.  On each one, a
fixed mode-three one-marked minor is nonzero throughout the genuine-binary
open, and a fixed pure transverse entry closes the final source coordinate.
No parameter grid or ambient graph search is used.

This is a generic theorem.  It does not close special or projective component
boundaries, weighted `H22`, pure-`P_4` component exhaustiveness, or the global
Krenn--Gu conjecture.

## Intrinsic pure bases

Work over `K=C(p,q)`, put

```text
e=X0,   A=X1,   B=X2,   C=X3,   s=p-q+1,
v=pA+qB+C,       u=v+A-B.                            (1)
```

For the normalized family in
[`P4_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT.md`](../../../p4/classifications/triangle-211/common-active-binary-triangle/P4_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT.md),
write the two rows of `U0` as

```text
r0=-(s/(p+q))e-A+B,
r1=(q(q-1)/(p+q))e-(p+q)A+C.                       (2)
```

An intrinsic pure orientation is

```text
alpha0=q(q-1)r0+s r1
      =-p(p+1)A+q(q-1)B+sC,       beta0=(p+q)r0,
alpha1=e,                          beta1=u,
alpha2=e,                          beta2=v,
alpha3=e+A+B,                      beta3=e.          (3)
```

Direct permanent expansion gives

```text
T_w=0 for w!=1111,       T_1111=2(p+q)s.            (4)
```

Thus the `alpha_i` are the four intrinsic pure-kernel rows.  Every marked
basis over the same generic four-plane point is, after harmless nonzero row
rescaling,

```text
beta_i(h)=beta_i+h_i alpha_i,       i=0,1,2,3.       (5)
```

The omitted source-diagonal torus only rescales retained source columns after
a deletion, so it preserves the mixed kernels, diagonal open conditions,
one-marked ranks, and transverse nonvanishing used below.

## Exact projection to four markings

For distinguished source coordinate `d`, delete `d`, append the fifth-source
extension column, and write its eight entries as

```text
z=(x0,x1,x2,x3;y0,y1,y2,y3)^T.                     (6)
```

Let `M_d(h)` be the `14 x 8` mixed-coefficient matrix and let `A_d(h),B_d(h)`
be its all-`alpha` and all-`beta(h)` diagonal rows.  A genuine binary
neighbour requires

```text
M_d(h)z=0,       A_d(h)z B_d(h)z !=0.               (7)
```

Normalize `A_dz=1`, invert `B_dz`, and eliminate the eight entries of `z`
and the inverse over `K`.  Bidirectional exact standard-basis reduction gives

```text
d=0:  <1>,

d=1:  <h0,h3,
       h2(h2+q),
       q h1+(q-1)h2+q(q-1)>,

d=2:  <h0,h3,
       h2(h2+p),
       p h1+(p+1)h2+p(p+1)>,

d=3:  <1>.                                           (8)
```

Since `p,q` are units in `K`, the two nonunit ideals are reduced and split
into exactly four points:

```text
C1: d=1,  h=(0,1-q,0,0),
C2: d=1,  h=(0,0,-q,0),
C3: d=2,  h=(0,-p-1,0,0),
C4: d=2,  h=(0,0,-p,0).                             (9)
```

There are no hidden affine marking sheets or extension directions.

## Complete kernels on the four residual points

Use the coordinate order in (6).  On each point in (9), `M_d` has rank six.
The following two displayed vectors form its complete kernel.  The second
vector is normalized so that its all-`alpha` diagonal is nonzero:

```text
C1:
 v0=(-p(p+1),0,0,1; -(p+q),p+1,p,0),
 v1=(pq,-1,-1,0; 2q-1,-q,0,1),

C2:
 v0=(-p(p+1),0,0,1; -(p+q),p+1,p,0),
 v1=(0,-1,-1,(q-1)/p; qs/p,(p+1)(q-1)/p,0,1),

C3:
 v0=(q(q-1),0,0,1; p+q,q-1,q,0),
 v1=(-pq,-1,-1,0; -2p-1,-p,0,1),

C4:
 v0=(q(q-1),0,0,1; p+q,q-1,q,0),
 v1=(0,-1,-1,(p+1)/q; ps/q,(p+1)(q-1)/q,0,1).
                                                               (10)
```

Every genuine extension has a nonzero `v1` coefficient, because the
all-`alpha` diagonal vanishes on `v0`.  Projectively normalize that coefficient
to one and write

```text
z=T v0+v1.                                           (11)
```

The two binary diagonals are

```text
             A_d z                 B_d z /(2s)
C1:          -2s              T(p+q)-2q+1
C2:          -2s              T(p+q)-qs/p
C3:          -2s              T(p+q)-2p-1
C4:          -2s              T(p+q)+ps/q.          (12)
```

## One fixed minor and one fixed transverse entry

Let `N_3(z)` be the neighbouring mode-three one-marked map.  Its rows are
numbered by the mode-`0,1,2` words `000,001,...,111`.  In every one of the
four cases, the same row set `0147` gives the exact identity

```text
det N_3(z)[0147] / (B_d z)
       =4pq(p+q)s.                                  (13)
```

All factors on the right are nonzero in `K`.  Hence (7) makes this determinant
nonzero for every residual extension, including the unique value of `T` that
would make any unrelated minor vanish.  The neighbouring one-marked map is
therefore injective.

For the pure mode-three one-marked map `P_3`, row `001` has the following
entry in the deleted source column:

```text
d=1:  (P_3)_(001,1)= pq,
d=2:  (P_3)_(001,2)=-pq.                            (14)
```

Both are nonzero in `K`.

## The `H31` contradiction

In a hypothetical `H31` lift, let `G_3` be the third target-coordinate row
in mode three.  All coefficients containing one `G_3` vanish on the binary
`Delta_2` slice.  Injectivity of `N_3(z)` forces `G_3` to vanish on the
neighbouring hyperplane, so it can be supported only on the distinguished
pure coordinate `d`.  The nonzero pure transverse entry (14) kills that final
coefficient.  Thus `G_3=0` globally, contradicting target rank three.

Together with the exact projection (8), this proves

```text
generic marked H31 fibre(component 20)=empty.        (15)
```

## Exact replay

```text
uv run --with sympy python \
  claims/p5/h31/common-active-binary-triangle/verify_p5_h31_common_active_binary_triangle_component_generic_obstruction.py

uv run --with sympy python \
  claims/p5/h31/common-active-binary-triangle/audit_p5_h31_common_active_binary_triangle_component_generic_obstruction.py
```

The verifier reconstructs (1)--(5), checks all sixteen pure coefficients,
proves the four projected ideals in (8) in both directions, rebuilds every
rank-six mixed kernel in (10), and verifies the diagonal, determinant, and
pure-transverse identities (12)--(14) over characteristic zero.  It is a
fixed-size symbolic certificate, not a parameter search.

The independent audit rebuilds the permanent maps without importing the
primary verifier, exhausts every marking over two generic finite-field
specializations, and independently rechecks the four exact residual
certificates.  Its finite-field enumerations are regression checks only; the
bidirectional characteristic-zero elimination in the primary verifier is the
projection proof.
