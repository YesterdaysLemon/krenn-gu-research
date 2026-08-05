# Generic weighted `H22` obstruction on the embedded-`P_3` component

## Status

This is an exact characteristic-zero theorem on the generic
diagonal-source orbit of the ninth pure-`P_4` component constructed in
[`P4_EMBEDDED_P3_PURE_COMPONENT.md`](P4_EMBEDDED_P3_PURE_COMPONENT.md).

Both weighted neighboring diagonal pencils have empty binary
`Delta_2` incidence at the generic component point.  Consequently the
generic marked weighted `H22` fibre is empty, without imposing a
ternary local-rank condition.

This generic theorem alone does not close its displayed
slope/parameter divisors.  The two later boundary theorems close them
throughout the normalized affine chart.  The combined results still
do not close the component's omitted normalization/projective
boundary, prove that the nine known pure-`P_4` components are
exhaustive, produce a prize graph, or settle the global Krenn--Gu
conjecture.

## Normalized pure component

On the dense chart used in
[`P5_H31_EMBEDDED_P3_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H31_EMBEDDED_P3_COMPONENT_GENERIC_OBSTRUCTION.md),
take

```text
alpha_0=(0, 1,S,U),       beta_0=(1, 0,1,T),

alpha_1=(0,-1,1,0),       beta_1=(0,-1,0,1),
alpha_2=(0, 1,0,1),       beta_2=(0, 1,1,0),
alpha_3=(0, 0,1,1),       beta_3=(0,-1,0,1).       (1)
```

The only nonzero restricted coefficient is

```text
T_BBBB=-2,
```

and arbitrary markings are

```text
beta_i(t_i)=beta_i+t_i alpha_i.                   (2)
```

As before, the last three planes restrict the squarefree `P_3`
Frobenius form to

```text
-2 lambda_1 tensor lambda_2 tensor lambda_3.      (3)
```

## Weighted `H22` pencils

Restoring the generic diagonal-source slope `r`, the two neighboring
four-coordinate maps are

```text
D_01^r(z,e)=(r z_0+z_1,z_2,z_3,e),
D_23^r(z,e)=(z_0,z_1,r z_2+z_3,e).                (4)
```

Here `e` is the fifth-coordinate extension.  A binary `Delta_2`
image requires its all-alpha and all-beta coefficients both to be
nonzero.

## The `23` direction has a structural zero diagonal

The first target coordinate of `D_23^r` is exactly source coordinate
zero.  Every `alpha_i` in (1) has zero there.  Thus the all-alpha
matrix has an identically zero column for every extension and every
marking:

```text
A_23^r z=0.                                        (5)
```

The `23` direction never gives a binary `Delta_2` neighbor on this
normalization, for any slope.

## The `01` direction is the same insertion arrangement

For modes `1,2,3`, the first three target coordinates of `D_01^r` are
their unchanged coordinates in

```text
W=span(X_1,X_2,X_3).
```

For mode zero they are

```text
a=(1,S,U),
b_r+t_0 a=(r,1,T)+t_0(1,S,U).                    (6)
```

Consequently Laplace expansion along the extension coordinate gives
exactly the six-column apolar insertion map `N(w)` of the generic
`H31` theorem.  Its projective rank-drop support is

```text
V(p-q-rho) union V(p-q+rho) union V(p+q+rho)
 union {[1:0:0],[0:1:0],[0:0:1]}.                (7)
```

Away from the special points of the three lines at which
`p q rho=0`, the line kernels are respectively

```text
<z_2>,        <z_3>,        <z_1>.                (8)
```

In particular every generic rank-jump kernel has

```text
x_1=x_2=x_3=0.                                    (9)
```

## The slope-dependent projected line

The projected mode-zero plane is now the projective line

```text
Lambda_r=P span((1,S,U),(r,1,T)).                 (10)
```

Let `Sigma` be the same nine exceptional points as in the `H31`
theorem:

```text
[1:0:0], [0:1:0], [0:0:1],
[1:0:1], [1:1:0], [0:1:-1],
[1:0:-1], [0:1:1], [1:-1:0].                    (11)
```

The nine point-line incidence determinants multiply to

```text
Delta_22=
 (rS-1)(rU-T)(ST-U)
 (rS-rU+T-1)(rS+rU-T-1)
 (rS-ST+U-1)(rS+ST-U-1)
 (rU-ST-T+U)(rU+ST-T-U).                         (12)
```

Thus `Delta_22!=0` is a dense open set on which `Lambda_r` avoids
`Sigma`.  It is nonempty; for example

```text
(S,T,U,r)=(2,3,4,5)
```

gives

```text
Delta_22=-1396755360.
```

## Binary exclusion

Fix arbitrary markings (2).  If all mixed coefficients in the
`beta_0(t_0)` slice of `D_01^r` vanish, the intrinsic extension
covectors in modes `1,2,3` lie in

```text
ker N((r,1,T)+t_0(1,S,U)).                        (13)
```

On the open set (12), either this kernel is zero or (8) applies.
Equation (9) holds in both cases.  The all-alpha coefficient in the
other mode-zero slice is therefore

```text
D_(1,S,U)(alpha_1,alpha_2,alpha_3)
 +x_0 P_3(alpha_1,alpha_2,alpha_3)=0.             (14)
```

The first term vanishes by (9); the second vanishes by the pure tensor
identity (3).  Hence

```text
A_01^r z=0.                                       (15)
```

Equations (5) and (15) exclude a genuine binary `Delta_2` direction
in both weighted pencils.  Since an `H22` local map requires at least
one of them to be genuinely binary, the generic weighted marked
`H22` fibre of the ninth component is empty.

## Cross-specialty interpretation

This is a small kernel-sheaf calculation on a projective line:

```text
squarefree Frobenius multiplication
 -> first-variation presentation
 -> Fitting support in P^2
 -> intersection with Lambda_r
 -> coordinate kernel kills a diagonal.
```

The algebra belongs naturally to Artinian Gorenstein/Lefschetz
theory, where multiplication-rank failures are encoded by Hessian
degeneracy loci
([Maeno--Watanabe](https://arxiv.org/abs/0903.3581)).  Its complete
linear splitting here resembles the subspace supports arising from
syzygies of hyperplane arrangements
([Denham--Steiner](https://arxiv.org/abs/2112.13462)).  The theorem
uses neither as a black box; their shared lesson is to study the
kernel sheaf over the Fitting support before eliminating all marked
variables.

## Verification

Run

```text
python verify_p5_h22_embedded_p3_component_generic_obstruction.py
python audit_p5_h22_embedded_p3_component_generic_obstruction.py
```

The primary verifier reconstructs both weighted pencils, proves the
`23` all-alpha coefficient is identically zero, identifies the `01`
projection with the apolar insertion map, and checks all nine factors
of (12) symbolically.  The independent audit rebuilds permanent
coefficients by squarefree subset multiplication and checks the
projective arrangement and the sample weighted line over two finite
fields.  Those finite-field checks are corroboration only; the theorem
is the characteristic-zero proof above.

## Honest frontier

All nine currently certified pure-`P_4` component orbits now have
empty generic marked fibres for both `H31` and weighted `H22`.
Neither component exhaustiveness nor every normalization/projective
boundary follows.  The rank-two projected-line boundary of this
ninth component has since been closed:
[`P5_H22_EMBEDDED_P3_COMPONENT_RANK_TWO_LINE_BOUNDARY_OBSTRUCTION.md`](P5_H22_EMBEDDED_P3_COMPONENT_RANK_TWO_LINE_BOUNDARY_OBSTRUCTION.md).
The remaining rank-one projection collapse

```text
rS=1,             T=rU,
```

where the two projected mode-zero rows become proportional and the
line-arrangement kernel calculation changes type, has also since been
closed by using the other required marked slice as a complementary
insertion pencil:
[`P5_H22_EMBEDDED_P3_COMPONENT_RANK_ONE_COLLAPSE_OBSTRUCTION.md`](P5_H22_EMBEDDED_P3_COMPONENT_RANK_ONE_COLLAPSE_OBSTRUCTION.md).
Thus the entire normalized affine weighted `H22` chart of the ninth
component is empty.  Its omitted normalization/projective boundary
remains open.
