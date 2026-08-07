# No `H31` lift of the known rank-two pure-`P_4` family

## Status

This is an exact characteristic-zero obstruction for the complete
five-parameter family constructed in
[`P4_DECOMPOSABLE_RANK_TWO_FAMILY.md`](claims/p4/classifications/pair-geometry/decomposable-rank-two-family/P4_DECOMPOSABLE_RANK_TWO_FAMILY.md).

No member of that family can simultaneously be:

1. a binary `P_4 -> pure` restriction on one four-dimensional source
   hyperplane;
2. a binary `P_4 -> Delta_2` restriction on a second hyperplane sharing
   three source coordinates; and
3. the binary projection of rank-three five-dimensional local maps
   satisfying the corresponding ternary `H31` slice equations.

This excludes the displayed dense family chart in one distinguished-
source orientation of a natural all-rank-two component.  The other
three orientations, and hence the full source/mode symmetry orbit of
the family chart, are excluded in
[`P5_H31_RANK_TWO_COMPONENT_ORBIT_OBSTRUCTION.md`](P5_H31_RANK_TWO_COMPONENT_ORBIT_OBSTRUCTION.md).
Neither result automatically excludes all boundary points of the
component closures.  This theorem also does **not** classify every
rank-two pure compression of `P_4`, exclude all of `H31`, prove
`P_5 -> Delta_3` impossible, or settle the global conjecture.

The proof is linear algebra on the two hyperplane extensions.  It
enumerates neither ambient local maps nor Grassmannians.

## The pure family and a second hyperplane

Use source coordinates

```text
M={0,1,2},   s=3,   p=4.
```

On `H_s=span(M,s)`, write the two binary rows at mode `r` as

```text
B_r=U_r,   A_r=V_r,
```

where `U_r,V_r` are the rows in the known pure family.  Its parameters
are

```text
e i != 0,   l,j,c arbitrary,   C=c+e i l != 0.       (1)
```

The restriction on `H_s` has only the nonzero coefficient `BBBB`.

Keep the three entries on `M` and extend the rows to the neighbouring
hyperplane `H_p=span(M,p)` by new entries

```text
A_r[p]=x_r,   B_r[p]=y_r.                            (2)
```

All `14` mixed binary coefficients on `H_p` are linear in the eight
variables

```text
x_0,...,x_3,y_0,...,y_3.
```

Let `N(e,i,l,j,c)` be their `14 x 8` coefficient matrix.

## Generic stratum `l!=0`

When `l!=0`, the minor of `N` with mixed-word rows

```text
0001,0010,0011,0110,1000,1010,1011
```

and columns

```text
x_0,x_1,x_2,x_3,y_0,y_1,y_3
```

is

```text
-4 i^2 l^4 (c+e i l)/e^4,                           (3)
```

which is nonzero by (1).  Direct substitution gives the kernel vector

```text
x=t (-(j l+1)/l, -1, 0, 1/(e i l)),
y=t (c/(e i l), 1/(i l), 1, 0).                     (4)
```

Hence (3) proves that (4) spans the whole kernel.

The two diagonal coefficients on `H_p` evaluate on (4) to

```text
AAAA=0,
BBBB=2t(c+e i l)/(e i l).                           (5)
```

Thus the second hyperplane remains pure; it cannot be `Delta_2`.

## Exceptional stratum `l=0`

Now (1) gives `c!=0`.  A `6 x 6` minor of `N` is

```text
2c/(e^3 i),                                          (6)
```

and the following two vectors lie in its kernel:

```text
x=t(-i,0,0,1/e)+u(-j,-1,0,0),
y=t(c/e,1,0,0)+u(1,0,1,0).                          (7)
```

The minor (6) makes them a basis.  The two diagonal coefficients are

```text
AAAA=-2 j u/(e i),
BBBB= 2(c t+e u)/e.                                  (8)
```

There is therefore a genuine binary `Delta_2` extension exactly on the
open part

```text
j u (c t+e u) != 0.                                 (9)
```

This is an important sharpness check: binary compatibility alone does
not exclude `H31`.

## The third-colour lift is impossible

Let `G_r` be the putative third target-coordinate row of the full local
map.  Because the `H31` images on both `H_s` and `H_p` use only the
`A,B` target coordinates, every coefficient with one `G_r` and binary
rows at the other three modes must vanish.

Consider mode `r=1`.  On `H_p`, the map from a candidate row
`G_1|H_p` to its eight one-`G_1` coefficients has the `4 x 4` minor

```text
8 j u^2(c t+e u)/(e^4 i).                            (10)
```

It is nonzero by (1) and (9).  Hence

```text
G_1|H_p=0.                                           (11)
```

On `H_s`, the analogous eight-coefficient map has rank three.  Its
kernel is exactly

```text
C e_1^* subset H_s^*.                                (12)
```

For example, a rank-three witness minor is `4cj/e`, again nonzero by
(1) and (9).

Equation (11) says that the five-dimensional row `G_1` is supported
only on source coordinate `s`.  Its restriction to `H_s` is therefore
a multiple of `e_s^*`, whose intersection with (12) is zero.  Thus

```text
G_1=0.
```

The full local map at mode one then has only the two rows `A_1,B_1` and
has rank at most two.  This contradicts the rank-three requirement
forced by conciseness of `Delta_3`.

Both `l!=0` and `l=0` are impossible, proving the theorem.

## Verification

Run:

```text
python verify_p5_h31_known_rank_two_family_obstruction.py
python audit_p5_h31_known_rank_two_family_obstruction.py
```

The primary verifier reconstructs all binary permanent coefficients,
the two kernel normal forms, and the three displayed minors
symbolically.  The independent audit performs the same compatibility
test over every admissible parameter value in `F_5` and `F_7`, using a
separate modular permanent and row-reduction implementation.  It
checks every binary `Delta_2` extension and verifies the transverse
third-row kernel contradiction.  The finite-field census audits the
case boundary; the proof above is over characteristic zero.
