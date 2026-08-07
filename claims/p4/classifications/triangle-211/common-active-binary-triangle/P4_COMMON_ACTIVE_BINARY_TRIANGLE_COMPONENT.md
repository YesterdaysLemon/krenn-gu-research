# A twentieth component from the common-active binary triangle

## Status

**Exact characteristic-zero component theorem.**  The genuine-binary
`tau!=0` common-active residual in equations (9)--(10) of
[`P4_ONE_KERNEL_RANK_ONE_TRIANGLE_NORMAL_FORM_REDUCTION.md`](../../../../../P4_ONE_KERNEL_RANK_ONE_TRIANGLE_NORMAL_FORM_REDUCTION.md)
is a five-dimensional irreducible component of the pure `P_4` compression
locus.  Its generic pair profile is

```text
(4,4,4,3,3,3),
```

and the intrinsic pure-kernel endpoint signature of its three rank-one
triangle relations is `(2,2,0,0)`.  This separates it from the nineteen
previously certified component orbits.

The singleton `tau!=0` common-active family is an explicit boundary of this
component.  Together with the component-eleven inclusion for `tau=0`, the
whole common-active orientation in the exactly-one-kernel residual ledger is
therefore classified.  This theorem does not close the remaining
common-kernel or mixed-chain fibres, special marked `P_5` fibres, or the
global Krenn--Gu conjecture.

The component certificate is computer-assisted but exact.  A local standard
basis modulo `101` proves a height statement in an integral graph slice;
Krull's height theorem then gives the characteristic-zero local dimension.

## Normalized binary family

Work in

```text
R=C[X_0,X_1,X_2,X_3]/(X_0^2,X_1^2,X_2^2,X_3^2)
```

and put

```text
e=X_0,       A=X_1,       B=X_2,       C=X_3,
h=A-B,       w=A+B.                                    (1)
```

The binary branch of the preceding reduction has

```text
v=pA+qB+C,       u=lambda*v+h,
U_1=span(e,u),   U_2=span(e,v),
U_3=span(gamma*e+w,e).                                (2)
```

On the dense open `lambda*gamma!=0`, a source diagonal map
`diag(a_0,b,b,a_3)` changes the parameters by

```text
p'=(b/a_3)p,       q'=(b/a_3)q,
lambda'=(a_3/b)lambda,
gamma'=(a_0/b)gamma.                                  (3)
```

Hence every such tuple is source-diagonally equivalent to `lambda=gamma=1`,
with new parameters `(lambda*p,lambda*q)`.  The divisor `gamma=0` is included
by closure.  For an exact replay before normalization, the unique opposite
plane from (9) of the preceding reduction is

```text
U_0^un=span(
 -gamma*(lambda*p-lambda*q+1)/(lambda*(p+q))*e-A+B,
  gamma*(lambda*q^2-q)/(lambda*(p+q))*e-(p+q)A+C).
```

Applying (3) to this display gives the plane in (4) exactly; it also makes
the regular `gamma -> 0` closure explicit.  It is therefore enough to use

```text
v=pA+qB+C,       u=v+h,

U_0=span(
  -(p-q+1)/(p+q)*e-A+B,
   (q^2-q)/(p+q)*e-(p+q)A+C),

U_1=span(e,u),
U_2=span(e,v),
U_3=span(e+w,e),                 p+q!=0.             (4)
```

The two rows of `U_0` annihilate the forbidden cubic covectors

```text
(0,1,1,p+q),
(2(p+q),2q-1,2p+1,2pq-p+q).                         (5)
```

Direct permanent expansion leaves exactly

```text
T_0111=2(p-q+1),       T_1111=-2q(q-1).             (6)
```

Thus (4) is a nonzero pure family off the simultaneous zero locus of the two
displayed coefficients.

## Pair geometry and the new discrete invariant

At `(p,q)=(2,4)`, the pair profile in edge order is

```text
(4,4,4,3,3,3).                                      (7)
```

The three triangle relations are identically

```text
y_1y_2=0,       y_1x_3=0,       y_2x_3=0.           (8)
```

All three relation matrices have rank one.  The pure tensor (6) has kernel
rows `y_1,y_2,y_3`; hence (8) has kernel endpoints

```text
edge 12: modes 1 and 2,
edge 13: mode 1,
edge 23: mode 2.                                    (9)
```

The sorted endpoint counts on the four modes are therefore

```text
(2,2,0,0).                                          (10)
```

This signature is intrinsic: the pure kernel line in each local plane is
unique for a nonzero pure tensor, and a rank-one multiplication relation has
two intrinsic factor lines.

## Five-dimensional irreducible family

Apply the projective source torus

```text
D=diag(t_0,t_1,t_2,1)                               (11)
```

to (4).  The parameter space `(p,q,t_0,t_1,t_2)` is irreducible and
five-dimensional.  In four Grassmann charts with pivots `(01)`, at

```text
(p,q,t_0,t_1,t_2)=(2,4,1,1,1),                     (12)
```

the sixteen affine chart coordinates are

```text
(-6,1,-2,1/6, 0,0,1,1/3,
  0,0,2,1/2,   0,0,1,0).                           (13)
```

The family Jacobian has rank five.  Rows `(0,1,2,3,6)` give the exact minor

```text
-1/6.                                               (14)
```

The family image closure is consequently an irreducible fivefold.

## The integral graph slice

In the same `(01)^4` charts, let `g_0,...,g_15` be the plane coordinates.
At (13), use tensor anchor `alpha=0110`.  The normalized tensor has anchor
coefficient `-2` and target Segre ratios

```text
(z_0,z_1,z_2,z_3)=(0,0,0,-1).                      (15)
```

For each `beta!=alpha`, impose

```text
F_beta=T_beta-T_alpha product_(i: beta_i!=alpha_i) z_i=0.  (16)
```

The fifteen equations have Jacobian rank twelve at (13),(15), so the tangent
space alone does not prove component status.

Now fix the five affine coordinates

```text
g_0,g_1,g_2,g_3,g_6                                  (17)
```

at their values in (13).  Their restriction to the explicit family has
determinant `-1/6` by (14), so this is a transverse five-hyperplane slice.
Translate the remaining fifteen coordinates to the origin.  Clearing the
denominator `6` from each equation gives fifteen primitive integer
polynomials in fifteen variables.  No denominator is divisible by `101`.

With local degree order `ds`, exact Singular arithmetic over `F_101` gives

```text
standard-basis size = 18,
local dimension     = 0,
vector-space dim.   = 9.                            (18)
```

Independent reconstruction gives the same triple `(18,0,9)` over `F_103`
and `F_107`; only one prime is needed for the proof.

## Why the modular calculation proves the characteristic-zero dimension

Let `p_0=101` and let

```text
S=Z_(p_0)[x_1,...,x_15]_(p_0,x_1,...,x_15),
n=(p_0,x_1,...,x_15),       q=(x_1,...,x_15).       (19)
```

Let `J` be the ideal generated by the fifteen integer slice equations.  They
vanish at the origin, so `J` is contained in `q`.  Equation (18) says

```text
rad(J+(p_0))=n,       height(J+(p_0))=16.           (20)
```

Choose a minimal prime `P` of `J` contained in `q`.  Since `J` has fifteen
generators, the generalized principal ideal theorem gives `height(P)<=15`.
Thus `P` cannot contain `p_0`, because the only prime over `J+(p_0)` is the
height-sixteen maximal ideal `n`.  The unique minimal prime over `P+(p_0)`
is `n`, and the principal ideal theorem gives

```text
16=height(n)<=height(P)+1.                           (21)
```

Therefore `height(P)=15`; since `P` is contained in the height-fifteen prime
`q`, one has `P=q`.  Localizing at `q` inverts `p_0` and proves that the
characteristic-zero graph slice is zero-dimensional at the rational origin.
This is an integral height argument, not a finite-field point census and not
an assumption of flatness.

Five hyperplanes can lower local dimension by at most five.  Hence the full
twenty-variable incidence has local dimension at most five at the sample.
Its fifteen defining equations give the reverse bound, as does the explicit
fivefold.  The local dimension is exactly five, and the irreducible family
closure is an irreducible component.  Uniqueness of the Segre factor point
for a nonzero pure tensor preserves the statement after projection to the
four-plane locus.

## Why this is component orbit twenty

Dimension separates this fivefold from every known sixfold.  A lower pair
rank, a star rather than a triangle of exceptional modes, or a relation-rank
word `(2,1,1)` separates all earlier fivefolds except the known rank-one
triangle families.  Those remaining cases have:

```text
components 16 and 17: kernel signature (1,1,1,0),
component 18:         all six pair ranks equal three,
component 19:         kernel signature (2,1,1,0).   (22)
```

The signature (10) is different.  Pair ranks, relation-matrix ranks, the
exceptional mode graph, and kernel endpoint counts are invariant under all
allowed source, mode, and row-basis symmetries.  Thus (4) is inequivalent to
all nineteen earlier component orbits and raises the certified lower bound
to twenty.

## The singleton sheet is a boundary

The singleton common-active normal form is

```text
v=rho*A+B+C,       u=lambda*v+A,

U_0=span(A-gamma*e,C-B),
U_1=span(e,u),
U_2=span(e,v),
U_3=span(gamma*e+A,e).                              (23)
```

It has the single coefficient `T_0111=2lambda`.  To obtain it from the
binary sheet, retain arbitrary `rho,lambda,gamma`, set

```text
p=rho,       q=epsilon^(-1),
D_epsilon=diag(1,1,epsilon,1),                      (24)
```

and apply `D_epsilon` to (2) and the displayed pre-normalization plane
`U_0^un`.  Over the punctured formal disc (equivalently, at the generic
`epsilon!=0` point) this lies in component twenty.  In Pluecker order
`(01,02,03,12,13,23)`, the four limits are

```text
U_0: (0,-gamma,gamma,1,-1,0)
       ~ (0,gamma,-gamma,-1,1,0),
U_1: (lambda*rho+1,lambda,lambda,0,0,0),
U_2: (rho,1,1,0,0,0),
U_3: (-1,0,0,0,0,0).                               (25)
```

These are exactly the Pluecker vectors of (23).  Hence the complete
singleton residual is contained in the same component closure.

## Consequence and replay

The common-active ledger is now complete:

```text
tau=0, independent products   -> component 18,
tau=0, dependent products     -> component 11,
tau!=0, singleton exact pair  -> component 20 boundary,
tau!=0, binary exact pair     -> component 20.       (26)
```

Run:

```text
uv run --with sympy python claims/p4/classifications/triangle-211/common-active-binary-triangle/verify_p4_common_active_binary_triangle_component.py
uv run --with sympy python claims/p4/classifications/triangle-211/common-active-binary-triangle/audit_p4_common_active_binary_triangle_component.py
```

The primary verifier regenerates the characteristic-zero identities and the
integral graph slice before invoking Singular.  The independent audit uses a
separate subset-algebra permanent, rebuilds the slice over `F_103`, and
checks the singleton Pluecker degeneration.  Neither script searches a
parameter grid.
