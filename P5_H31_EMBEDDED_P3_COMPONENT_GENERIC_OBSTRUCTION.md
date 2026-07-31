# Generic `H31` obstruction on the embedded-`P_3` component

## Status

This is an exact characteristic-zero theorem on a dense open subset of
the ninth pure-`P_4` component constructed in
[`P4_EMBEDDED_P3_PURE_COMPONENT.md`](P4_EMBEDDED_P3_PURE_COMPONENT.md).

The complete marked `H31` fibre over the generic point of that
component is empty.  In fact, no marked binary neighbour exists: the
obstruction occurs before the third target row is imposed.

The theorem does not close the component's special parameter or
projective boundary, analyze its weighted `H22` fibre, prove that the
nine known pure-`P_4` components are exhaustive, produce a prize
graph, or settle the global Krenn--Gu conjecture.

## Dense normalization

On the dense chart where the parameters called `A,r` in the component
theorem are nonzero (and `B` is already nonzero), diagonal source
scaling and independent row scaling put the pure-factor bases into

```text
alpha_0=(0, 1,S,U),       beta_0=(1, 0,1,T),

alpha_1=(0,-1,1,0),       beta_1=(0,-1,0,1),
alpha_2=(0, 1,0,1),       beta_2=(0, 1,1,0),
alpha_3=(0, 0,1,1),       beta_3=(0,-1,0,1).       (1)
```

For example, the source diagonal

```text
diag(Ar,1,A,B)
```

followed by row rescaling gives (1), with

```text
S=As,          U=Bu,          T=Bt/(Ar).
```

Every restricted coefficient vanishes except

```text
T_BBBB=-2.                                      (2)
```

Every marking of the same four planes is represented by

```text
beta_i(t_i)=beta_i+t_i alpha_i.                 (3)
```

## Three source deletions die immediately

If the distinguished source coordinate is any of `1,2,3`, then the
retained source coordinates include coordinate zero.  All four
`alpha_i` in (1) have zero in that coordinate.  Even after adding an
extension column, their `4 x 4` matrix still has an identically zero
source-coordinate column.  Hence its permanent is zero:

```text
A_q z=0,                 q=1,2,3.               (4)
```

A genuine binary `Delta_2` neighbour requires both diagonal
coefficients to be nonzero.  Thus only deletion of source coordinate
zero can possibly contribute to `H31`.

## The insertion tensor

Put

```text
W=span(X_1,X_2,X_3),
f(u,v,w)=[X_1 X_2 X_3] uvw
```

in the squarefree Frobenius algebra

```text
C[X_1,X_2,X_3]/(X_1^2,X_2^2,X_3^2).
```

The last three row pairs in (1), now viewed in `W`, are

```text
a_1=(-1,1,0),     b_1=(-1,0,1),
a_2=( 1,0,1),     b_2=( 1,1,0),
a_3=( 0,1,1),     b_3=(-1,0,1).                 (5)
```

They obey

```text
f restricted to U_1 tensor U_2 tensor U_3
  =-2 lambda_1 tensor lambda_2 tensor lambda_3,  (6)
```

where `lambda_i(a_i)=0` and `lambda_i(b_i)=1`.

After deleting source coordinate zero, adjoining a new coordinate is
Laplace expansion along that coordinate.  If

```text
ell_i(a_i)=x_i,          ell_i(b_i)=z_i,
```

then for a projected mode-zero row `w=(p,q,rho)` the contribution from
extensions in modes `1,2,3` is the trilinear tensor

```text
D_w(u_1,u_2,u_3)
 =sum_i ell_i(u_i) f(w,u_j,u_k).                 (7)
```

This is an apolar insertion map, or equivalently the first variation
of multiplication in the squarefree complete intersection.  It is
intrinsic: under (3), the marked extension coordinate `y_i` is merely

```text
y_i=z_i+t_i x_i.
```

The covectors `lambda_i` and the rank-one line in (6) do not change.

## A six-column degeneracy arrangement

Let

```text
L_1=p-q-rho,       L_2=p-q+rho,
L_3=p+q-rho,       L_4=p+q+rho.                  (8)
```

In the binary order `000,001,...,111`, direct Frobenius multiplication
turns (7) into

```text
D_000=L_4 x_1+L_1 x_2+L_2 x_3,
D_001=L_1 x_2+L_2 z_3,
D_010=L_4 x_1+L_1 z_2,
D_011=L_3 x_1+L_1 z_2,
D_100=L_1 x_2+L_4 z_1,
D_101=-2q x_2,
D_110=L_3 x_3+L_4 z_1+L_1 z_2,
D_111=L_3(z_1+z_3)-2qz_2.                       (9)
```

Let `N(w)` be the `7 x 6` coefficient matrix of the first
seven equations in (9), in column order

```text
(x_1,x_2,x_3,z_1,z_2,z_3).
```

The seven maximal minors, indexed by the omitted row, are

```text
omit 000: -4 q rho L_1 L_2 L_3 L_4,
omit 001:  0,
omit 010:  4 q(p+rho)L_1 L_2 L_3 L_4,
omit 011:  4 p q L_1 L_2 L_4^2,
omit 100: -4 q rho L_1 L_2^2 L_4,
omit 101:  4 p rho L_1^2 L_2 L_4,
omit 110:  4 q rho L_1 L_2^2 L_4.               (10)
```

Consequently the projective rank-drop locus is exactly

```text
V(L_1) union V(L_2) union V(L_4)
 union {[1:0:0],[0:1:0],[0:0:1]}.               (11)
```

Here is a computation-free check of necessity in (11).  Suppose
`L_1 L_2 L_4!=0` and all minors vanish.  The `011` minor gives
`pq=0`.  If `q=0`, the `101` minor gives `p rho=0`, leaving the first
or third coordinate point.  If `p=0` and `q!=0`, the `000` minor gives
`rho L_3=0`.  The alternative `L_3=0` would force `L_2=0`, so only the
second coordinate point remains.  Sufficiency is visible directly in
(10).

Away from finitely many special points on the three lines, their
kernels are even simpler:

```text
L_1=0:   ker N=<z_2>,
L_2=0:   ker N=<z_3>,
L_4=0:   ker N=<z_1>.                             (12)
```

For example, after deleting the displayed kernel column, the following
five-by-five minors certify rank five:

```text
L_1=0:  -32 q^3 rho(q+rho),
L_2=0:   32 q rho^3(q-rho),
L_4=0:   32 q^3 rho(q+rho).                       (13)
```

Thus the only generic rank-jump syzygies are the three coordinate
covectors `lambda_2,lambda_3,lambda_1`.  This is the useful geometry
hidden behind the failed large elimination: a Fitting scheme has
become a three-line arrangement.

## The projected mode-zero line is generic

The two projected rows of mode zero span the projective line

```text
Lambda=P span((1,S,U),(0,1,T)) in P(W).           (14)
```

Let `Sigma` consist of the three coordinate points in (11) together
with the points of `V(L_1) union V(L_2) union V(L_4)` at which
`p q rho=0`.  Its nine distinct points are

```text
[1:0:0], [0:1:0], [0:0:1],
[1:0:1], [1:1:0], [0:1:-1],
[1:0:-1], [0:1:1], [1:-1:0].                    (15)
```

The line (14) avoids `Sigma` precisely on the dense open set where

```text
Delta=
-T(T-1)(T+1)
 (ST-U)
 (ST-T-U)(ST+T-U)
 (ST-U-1)(ST-U+1)
 !=0.                                             (16)
```

This open set is nonempty: at `(S,T,U)=(2,3,4)`, `Delta=720`.

## Why every possible binary neighbour loses a diagonal

Fix arbitrary markings (3).  In the slice containing
`beta_0(t_0)`, the projected mode-zero row is

```text
w=(0,1,T)+t_0(1,S,U) in Lambda.                  (17)
```

The extension of mode zero itself contributes only to the `111`
coefficient because of (6).  Therefore all mixed coefficients in this
slice can vanish only if

```text
N(w)(x_1,x_2,x_3,z_1,z_2,z_3)^T=0.               (18)
```

If `N(w)` has full rank, all six variables vanish.  If it drops rank,
(11), (14), and (16) put `w` at a generic point of exactly one of the
three arrangement lines.  Equation (12) then says that the extension
covectors are proportional to one `lambda_i`.  In either case,

```text
x_1=x_2=x_3=0.                                   (19)
```

Now inspect the other mode-zero slice, containing `alpha_0`.  Its
all-alpha diagonal is

```text
A_0 z
 =D_(1,S,U)(a_1,a_2,a_3)
  +x_0 f(a_1,a_2,a_3).                           (20)
```

The first term is zero by (9) and (19); the second is zero by the pure
identity (6).  Hence

```text
A_0 z=0.                                         (21)
```

This argument used only a necessary subset of the mixed equations, so
it also covers rank jumps and special values of all four marking
parameters.  Together with (4), it proves that no distinguished
coordinate admits a genuine binary `Delta_2` neighbour.  A fortiori,
the generic marked `H31` fibre of the ninth component is empty.

## Literature bridge

Three neighboring subjects explain why this reduction is natural:

1. The squarefree algebra is an Artinian Gorenstein complete
   intersection.  Lefschetz theory studies maximal-rank multiplication
   maps in precisely such algebras, and higher Hessians describe their
   exceptional loci:
   [Maeno--Watanabe](https://arxiv.org/abs/0903.3581).
2. The maximal minors in (10) are the Fitting equations of a linear
   presentation.  Here their support is much smaller than a generic
   determinantal curve and splits into a line arrangement plus three
   points.
3. Arrangement theory often converts syzygies of products of linear
   forms into subspace arrangements indexed by combinatorial data:
   [Denham--Steiner](https://arxiv.org/abs/2112.13462).  No theorem from
   that paper is needed here, but its viewpoint correctly predicts
   that the kernel support and its syzygies should be studied before
   attempting elimination.

The exact theorem above remains elementary: Frobenius multiplication,
six maximal minors, and a projective line avoiding nine points.

## Verification

Run

```text
python verify_p5_h31_embedded_p3_component_generic_obstruction.py
python audit_p5_h31_embedded_p3_component_generic_obstruction.py
```

The primary verifier reconstructs the pure tensors, the insertion
table, all maximal minors, the three kernel lines, the rank-five
certificates, and the discriminant (16) symbolically.  The independent
audit rebuilds the insertion map by squarefree multiplication, checks
the projective degeneracy locus over two finite fields, and verifies
the diagonal obstruction.  The finite-field checks are corroboration
only; the theorem is the characteristic-zero argument above.

## Honest frontier

All nine currently certified pure-`P_4` component orbits now have
empty generic marked `H31` fibres.  This does not prove that the list
is exhaustive and does not close any component's exceptional
parameter/projective boundary.  For the ninth component specifically,
the finite set `Sigma` in (15) has since been closed throughout the
normalized affine chart:
[`P5_H31_EMBEDDED_P3_COMPONENT_NORMALIZED_BOUNDARY_OBSTRUCTION.md`](P5_H31_EMBEDDED_P3_COMPONENT_NORMALIZED_BOUNDARY_OBSTRUCTION.md).
The normalization boundary `Ar=0` and projective boundary remain open.
Its generic weighted `H22` fibre is closed separately in
[`P5_H22_EMBEDDED_P3_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H22_EMBEDDED_P3_COMPONENT_GENERIC_OBSTRUCTION.md).
