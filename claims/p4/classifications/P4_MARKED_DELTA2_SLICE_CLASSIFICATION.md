# Marked `P_4 -> Delta_2` slice classification

## Status

This is an exact tensor classification over `C` for the marked
order-four permanent boundary arising in normalized `q4_211`.

Let `P_4` use source coordinates `0,1,2,3`.  At mode zero retain the
coordinate plane

```text
U_0=span(e_2^*,e_3^*).                               (1)
```

At each of the other three modes choose independent rows

```text
alpha_i,beta_i in (C^4)^*,   i=1,2,3.                (2)
```

Suppose the resulting binary restriction has exactly the two nonzero
diagonal coefficients

```text
Perm(e_2^*,alpha_1,alpha_2,alpha_3) != 0,
Perm(e_3^*,beta_1,beta_2,beta_3) != 0.               (3)
```

Then either:

1. one coordinate-deleted `P_3` slice has a rank-one local map, in
   which case

   ```text
   beta_i in C e_2^*
   ```

   for a rank-one `013`-slice mode, or

   ```text
   alpha_i in C e_3^*
   ```

   for a rank-one `012`-slice mode; or

2. all six coordinate-deleted local maps have rank two, and, after
   permuting modes `1,2,3`, interchanging the shared source coordinates
   `0,1`, and rescaling local rows, there are parameters

   ```text
   A T != 0,   B arbitrary
   ```

   for which

   ```text
   alpha_1=(0,1,T,-B)       beta_1=(1,0,0,-A)
   alpha_2=(1,0,0, A)       beta_2=(0,1,-T,B)
   alpha_3=(1,0,0, A)       beta_3=(B,A,-A T,0).      (4)
   ```

Conversely (4) gives

```text
Perm(e_2^*,alpha_1,alpha_2,alpha_3)= 2A,
Perm(e_3^*,beta_1,beta_2,beta_3)=-2AT,               (5)
```

and all fourteen mixed coefficients vanish.

Thus the all-rank-two marked boundary is a concrete three-parameter
family, while every other marked boundary has a coordinate-row gate.
This classification does **not** exclude the family, normalized
`q4_211`, `P_5 -> Delta_3`, or the global Krenn--Gu conjecture.

## The two pure cubic slices

Choosing `e_2^*` at mode zero leaves the order-three permanent on

```text
J_2=span(e_0,e_1,e_3).
```

Equation (3) and the mixed-coefficient vanishings say that its
restriction through the three row pairs in (2) is the nonzero pure
tensor supported only at `alpha_1 alpha_2 alpha_3`.

Choosing `e_3^*` similarly leaves the order-three permanent on

```text
J_3=span(e_0,e_1,e_2),
```

whose restriction is supported only at
`beta_1 beta_2 beta_3`.

If the `J_2` restriction at mode `i` has rank one, its target image
must be the `alpha_i` line.  Therefore

```text
beta_i restricted to J_2=0,
```

which gives the first coordinate-row alternative.  The `J_3` statement
is identical with `alpha,beta` interchanged.

It remains to assume that all six restrictions have rank two.

## Compatibility of two `P_3` sign charts

Apply the nonzero decomposable-`P_3` classification to the `J_2`
slice.  After permuting the three modes and the three coordinates of
`J_2`, its plane normals are the sign variants

```text
(1,A,B), (1,-A,-B), (1,-A,B).                        (6)
```

The pure-factor marking selects distinguished bases.  With canonical
coordinates `(X,Y,Z)` on `J_2`, they may be written

```text
alpha_1=(-B,0,1)       beta_1=(-A,1,0)
alpha_2=( A,1,0)       beta_2=( B,0,1)
alpha_3=( A,1,0)       beta_3=( 0,B,A).              (7)
```

Here `A != 0`; if necessary interchange `Y,Z`.  The parameter `B` may
vanish.

There are only two geometrically different positions for the common
coordinate `X` in (6):

- `X` is one of the shared coordinates `0,1`; or
- `X` is coordinate `3`, which is omitted from the other slice.

### A shared common coordinate is impossible

Take `(X,Y,Z)=(0,1,3)`; the other shared choice is symmetric.  Add
unknown coordinate-two entries

```text
x_i=alpha_i[2], y_i=beta_i[2].
```

The eight coefficients of the `J_3` slice are

```text
000: 2A x_1-Bx_2-Bx_3
001: B(Ax_1-Bx_2-y_3)
010: B(x_1-y_2)
011: B^2(x_1-y_2)
100: 2A y_1
101:-AB(x_2-y_1)
110: B(x_3+y_1)
111: B(-Ay_2+By_1+y_3).                              (8)
```

If `B=0`, the required `111` coefficient is already zero.  If
`B != 0`, vanishing of the first seven expressions forces

```text
x_1=x_2=x_3=y_1=y_2=y_3=0,
```

and again kills `111`.  Hence the common sign-chart coordinate cannot
be shared.

### The omitted common coordinate gives the family

Now take `(X,Y,Z)=(3,0,1)`.  The `J_3` coefficients become

```text
000: x_2+x_3
001: A x_1+B x_2+y_3
010: x_1+y_2
011: B(x_1+y_2)
100: 0
101: A(x_2+y_1)
110: x_3+y_1
111: A y_2+B y_1+y_3.                                (9)
```

Because `A != 0` and the field has characteristic zero, the first
seven vanish exactly when

```text
x_2=x_3=y_1=0,
y_2=-x_1,
y_3=-A x_1.                                         (10)
```

The last coefficient is `-2A x_1`, so nonvanishing sets

```text
T=x_1 != 0.
```

Substitution of (10) into (7), in the original source-coordinate
order, is exactly (4).  The other coordinate ordering only interchanges
source coordinates zero and one.  This proves completeness of the
all-rank-two family.

## Consequence for normalized `q4_211`

In the adjacent `q4_211` pencil, use the ordered source basis

```text
(e_1,e_2,w_+,w_-).
```

The restrictions of the singleton normals are

```text
h_2 restricted to H = 2c e_2^*,
h_1 restricted to H = 2b e_3^*.                     (11)
```

The hyperplane normal from the adjacent reduction is

```text
n=(0,0,0,c,b)=H^perp.
```

Therefore a rank-one slice gate in the first alternative says that a
singleton target row of another local map lies in one of the affine
normal pencils

```text
C h_2+C n
or
C h_1+C n.                                          (12)
```

If there is no such gate, the six singleton target rows on the three
remaining modes have the explicit normal form (4).  This is the new
non-brute-force frontier for coupling the marked `Delta_2` boundary to
the doubled-colour equations.

The gate branch has since been classified further.  There is exactly
one gate of each kind, at distinct modes, and the marked rows have two
explicit determinant strata.  Their full third-colour lifts are both
impossible in normalized `q4_211`.  See
[`P4_MARKED_DELTA2_ALTERNATING_GATE_CLASSIFICATION.md`](P4_MARKED_DELTA2_ALTERNATING_GATE_CLASSIFICATION.md)
and
[`P5_Q4_211_ALTERNATING_GATE_OBSTRUCTION.md`](../../../P5_Q4_211_ALTERNATING_GATE_OBSTRUCTION.md).

## Verification

Run:

```text
python claims/p4/classifications/verify_p4_marked_delta2_slice_classification.py
python claims/p4/classifications/audit_p4_marked_delta2_slice_classification.py
```

The primary verifier expands all sixteen coefficients in (4), checks
the two sign-chart compatibility systems (8)--(10), and verifies all
six slice ranks symbolically.  The independent audit uses a
row-by-row permanent implementation and checks the two linear
compatibility systems over `F_3,F_5` for every projective value of
`B/A`.  It enumerates neither ambient maps nor Grassmannians.  The
finite-field checks audit the formulas and case split; the
classification above is over `C`.
