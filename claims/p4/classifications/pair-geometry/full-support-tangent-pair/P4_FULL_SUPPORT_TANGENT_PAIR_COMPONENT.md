# A fourteenth pure `P_4` component from a tangent pair

## Status

**Exact characteristic-zero component theorem.**  The nonzero pure
`P_4` compression locus has a five-dimensional irreducible component whose
generic pair profile is

```text
(r_01,r_02,r_03,r_12,r_13,r_23)=(2,3,4,3,4,4).     (1)
```

The rank-two edge has a kernel line tangent to the Segre quadric at a
support-one zero product.  Its tangent direction has full complementary
three-coordinate support.  The component is generically described by a
polar-plane graph for a nondegenerate ternary quadratic form.

At a rational point, the Segre-incidence Jacobian has rank thirteen, leaving
two excess first-order directions.  Their exact quadratic obstructions are

```text
tau_4 tau_5,
(tau_4-tau_5)^2.                                    (2)
```

They are coprime and form a regular sequence.  Thus the local dimension is
five, matching the family tangent rank.  This proves component status even
though the certificate point has a misleading seven-dimensional first-order
tangent space.

The sorted profile `(2,3,3,4,4,4)` separates it from every earlier
five-dimensional component.  The only earlier component with that sorted
profile is six-dimensional, so dimension separates the two.  The certified
lower bound is therefore fourteen symmetry-inequivalent pure-`P_4`
component orbits.

This is a `P_4` component theorem, not a `P_5` extension or a solution of the
global Krenn--Gu conjecture.  Its marked `H31/H22` fibres and special
support-two tangent boundary remain open.

## The polar-graph family

Work on the affine chart

```text
w=X_1+aX_2+bX_3,
u=X_1+cX_2+dX_3.                                    (3)
```

Put

```text
f_1=ad+bc,       f_2=b+d,       f_3=a+c,
L_1=2b^2(a-c),   L_2=2a^2(b-d),
E=2(ab+bc+ad).                                       (4)
```

For a fifth parameter `t`, take

```text
U_0=U_1=span(
 (1,0,0,0),
 (0,1,a,b)),

U_2=span(
 (1,0,0,0),
 (0,1,c,d)),

U_3=span(
 (tL_1,f_2,-f_1,0),
 (tL_2,f_3,0,-f_1)).                                (5)
```

The last two ternary parts are

```text
v_1=(f_2,-f_1,0),       v_2=(f_3,0,-f_1).           (6)
```

For the ternary polar form of `X_0w`, the functional defined by `u` is
`(f_1,f_2,f_3)`, so both vectors in (6) lie in `u^perp`.  The linear form
defined by `w^2` takes the values `L_1,L_2` on them.  Thus (5) is precisely
the dense graph `phi=t ell_w|u^perp` from the tangent-pair classification.

Direct multilinear expansion gives only

```text
T_1100=L_1,              T_1101=L_2,
T_1110=t E L_1,          T_1111=t E L_2.             (7)
```

Therefore

```text
P_4|U=(y_0 y_1)(x_2+tE y_2)(L_1x_3+L_2y_3).         (8)
```

It is nonzero and pure whenever `(L_1,L_2)!=(0,0)`.

## A rational certificate point

Take

```text
(a,b,c,d,t)=(1,1,2,3,1).                            (9)
```

Then

```text
U_0=U_1=span((1,0,0,0),(0,1,1,1)),
U_2=span((1,0,0,0),(0,1,2,3)),
U_3=span((-2,4,-5,0),(-4,3,0,-5)),                 (10)
```

and

```text
P_4|U=-2 y_0y_1(x_2+12y_2)(x_3+2y_3).              (11)
```

The six pair ranks are exactly (1).  The kernel of edge `01` is spanned by

```text
e tensor e,
e tensor w-w tensor e,                              (12)
```

so its projective line is tangent to the rank-one Segre quadric at
`[e tensor e]`.  Edges `02` and `12` have the single rank-one relation
`e tensor e`; the other three pair maps are injective.

## The family really has dimension five

All four planes at (9) lie in the pivot-`01` Grassmann chart.  Row reduction
of the last plane in (5) gives

```text
[1 0  -(a+c)/(2t(ad-bc))   (b+d)/(2t(ad-bc))]
[0 1   a^2(b-d)/(ad-bc)    b^2(c-a)/(ad-bc) ].      (13)
```

The chart coordinates `a,b,c,d` themselves recover the first four
parameters.  The derivative of the first free entry in (13) with respect to
`t` is `3/2` at (9).  Equivalently, the family Jacobian rows

```text
(2,3,10,11,12)
```

form a five-by-five minor of determinant `3/2`.  The irreducible rational
family therefore has five-dimensional image.

## Two quadratic obstructions give the local upper bound

Use the same four pivot-`01` charts and the target Segre chart anchored at
`1100`.  Let `z_0,...,z_3` be the four target ratios.  The fifteen incidence
equations are

```text
F_beta=T_beta-T_1100 product_{i:beta_i!=(1100)_i} z_i,
beta!=(1100).                                       (14)
```

At (9), after row reduction of `U_3`, the twenty chart/target coordinates are

```text
(0,0,1,1, 0,0,1,1, 0,0,2,3,
 -3/2,2,-2,1, 0,0,12,0).                           (15)
```

The Jacobian of (14) has rank thirteen.  Rows `2,...,14` and columns
`0,...,11,19` give the exact minor

```text
-34560.                                             (16)
```

Solve those thirteen equations formally by the implicit-function theorem,
leaving seven tangent coordinates `tau_0,...,tau_6`.  A rational nullspace
basis and the two-dimensional equation cokernel give the two residual
quadratic initial forms

```text
q_0=-tau_4 tau_5,
q_1=-(tau_4-tau_5)^2.                               (17)
```

Their greatest common divisor is one.  In the regular local ring on the seven
free coordinates they form a regular sequence of height two.  Hence the
formal local incidence has dimension at most `7-2=5`.  The five-dimensional
family supplies the reverse inequality, so its closure is an irreducible
component.

This second-order step is essential: the raw tangent-space dimension seven
would otherwise make the component look two dimensions too large.

## Why the component is new

The generic sorted pair profile is

```text
(2,3,3,4,4,4).                                      (18)
```

Every earlier five-dimensional component has either sorted profile
`(3,3,3,4,4,4)` or `(3,3,3,3,3,4)`.  The earlier six-dimensional lower-pair
component has profile (18), but component dimension is invariant under all
allowed source/mode symmetries.  The embedded-`P_3` sixfold has three
rank-two edges.  Therefore the component in this note is inequivalent to all
thirteen earlier orbits.

Its exceptional graph is shown in
[`research_figures/P4_FULL_SUPPORT_TANGENT_PAIR_COMPONENT_GRAPH.svg`](../../../../../research_figures/P4_FULL_SUPPORT_TANGENT_PAIR_COMPONENT_GRAPH.svg).

## Across the mathematical fence

This component is a meeting point of three small geometries:

```text
Kronecker geometry:       a kernel line tangent to the Segre quadric,
Witt geometry:            a polar plane in a ternary quadratic space,
singularity theory:       two coprime quadratic initial obstructions.
```

The first-order excess is not a numerical accident.  Tangency creates two
infinitesimal directions that do not integrate; the doubled diagonal
`(tau_4-tau_5)^2` and the crossing `tau_4tau_5` kill them
scheme-theoretically.  This is precisely why a symbolic tangent-cone
argument sees the component while a point search or raw Jacobian count would
misclassify it.

## Verification

Run:

```text
uv run --with sympy python claims/p4/classifications/pair-geometry/full-support-tangent-pair/verify_p4_full_support_tangent_pair_component.py
python claims/p4/classifications/pair-geometry/full-support-tangent-pair/audit_p4_full_support_tangent_pair_component.py
```

The primary verifier proves (7), (13), the family minor, (16), (17), the
coprimality, and the pair-kernel data.  The independent audit uses a
separately implemented subset-DP permanent and exact truncated second-order
jets to
replay the tangent and obstruction certificates without importing the
primary code.  Neither verifier searches for points.
