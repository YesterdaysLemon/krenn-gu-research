# A twenty-second pure `P_4` component from the unequal common-kernel sheet

## Status

**Exact characteristic-zero component and projective classification theorem.**  In the
active/active common-kernel orientation of the triangle cell with relation
ranks `(2,1,1)`, allow the two complementary binary directions to be
unequal.  On the genuine support-two chart, the apolar rank equations split
into four linear sheets.  The four sheets are exchanged by source and mode
permutations, and a dense open of each is a smooth five-dimensional
irreducible component of the pure `P_4` incidence.

The remaining complementary-direction boundaries are component thirteen,
lower-pair, embedded `P_3`, or zero.  Thus this closes the complete
common-kernel active/active (`CC`) orientation, not merely its affine dense
chart.

This is a new symmetry orbit, component twenty-two.  It meets the
Eisenstein-norm component (component thirteen) on the equal-complement
divisor, but it is not contained in that component: independence of the two
intrinsic complementary directions is preserved by the diagonal source
torus and is generic here.

The theorem classifies this unequal-complement `CC` chart.  It does not close
the two star cells, special or projective `P_5` fibres, or the global
local-to-global step.  In particular, the Krenn--Gu conjecture remains
**UNRESOLVED**.

## The common-kernel chart

Work in the squarefree Frobenius algebra

```text
R=C[X_0,X_1,X_2,X_3]/(X_0^2,X_1^2,X_2^2,X_3^2).
```

Normalize

```text
a=X_0+X_1,                 c=X_0-X_1,
b=X_2+X_3,                 ac=0,
t=((1-D)/2)X_2+((1+D)/2)X_3.                    (1)
```

Thus `D!=0` says that `b` and `t` are unequal, while the normalization
`t_2+t_3=1` is legal precisely on the nonzero-sum chart.  Put

```text
m=Aa+Bc+b,       m_r=m+Rc,       d=Ga+t,
U_1=<m,a>,       U_2=<m_r,a>,    U_3=<c,d>.       (2)
```

The exceptional relations are identically

```text
m*a-a*m_r=0,       a*c=0,       a*c=0,            (3)
```

so their coefficient ranks are `(2,1,1)` wherever the first relation is
unique.

## Exact factorization of the cubic rank locus

The seven kernel-rich cubics span the same space as

```text
C_0=m*m_r*c,       C_1=m*m_r*d,       C_2=m*a*d.  (4)
```

Define

```text
H=A^2+B^2+BR+2AG,
Q=A^2+2AG-3B^2-3BR+4G^2-R^2.                     (5)
```

The four maximal minors of `[C_0 C_1 C_2]`, in the missing-coordinate
basis, are

```text
-4(Q+D H),
-4(Q-D H),
-4D(A-B)(A-B-R)(2B-2G+R),
-4D(A+B)(A+B+R)(2B+2G+R),                         (6)
```

up to the harmless sign determined by row order.  Hence `D!=0` forces
`H=Q=0` and one factor from each of the last two products.  The nine cases
reduce exactly to the following four linear sheets:

```text
L_1: A=B,       2G+2A+R=0,
L_2: A=-B,      2G+2A-R=0,
L_3: R=A-B,     2G+A+B=0,
L_4: R=-A-B,    2G+A-B=0.                         (7)
```

Conversely every sheet in (7) kills all four minors.  The alternatives have
a transparent meaning: respectively `m` loses `X_1`, `m` loses `X_0`,
`m_r` loses `X_1`, or `m_r` loses `X_0`.  Swapping `X_0,X_1` exchanges
`L_1,L_2`; swapping modes one and two exchanges the first pair with the
second.  Thus (7) is one symmetry orbit.

The case reduction is set-theoretic over characteristic zero.  Squared
generators such as `G^2` in two corner cases introduce no extra points.

## Intrinsic completion of the direction charts

For completeness, before the normalization in (1), write

```text
s=uX_2+vX_3,       t=pX_2+qX_3,
U=uv,               S=pv+qu,       Q=pv-qu,
k=2 beta+r,         K=3 beta^2+3 beta r+r^2.       (8)
```

Here the parameters in `m=alpha*a+beta*c+s`, `m_r=m+r*c`, and
`d=gamma*a+t` are lower-case to avoid confusing `S` with the earlier affine
coordinate `A`.  Put

```text
E=S^2(K-alpha^2)-2SU alpha gamma-4U^2 gamma^2,
J=S(alpha^2+beta(beta+r))+2U alpha gamma.           (9)
```

The same four maximal minors, without choosing a chart on either binary
direction, are

```text
4v(E+QJ),
4u(E-QJ),
4Q(alpha-beta)(alpha-beta-r)(kS-2gamma U),
4Q(alpha+beta)(alpha+beta+r)(kS+2gamma U).         (10)
```

Assume first `uv!=0`.

- If `Q=0`, the two projective complementary directions agree.  After
  scaling `d`, the remaining equation is precisely the component-thirteen
  Eisenstein norm quadric.
- If `S*Q!=0`, (10) gives exactly the four sheets already listed in (7), in
  the invariant form

  ```text
  2gamma U/S=k,   alpha=-beta or -beta-r,
  2gamma U/S=-k,  alpha= beta or  beta+r.           (11)
  ```

- If `S=0,Q!=0`, the first two minors force `gamma=0`.  With `t` the split
  polar partner of `s`, direct multiplication gives

  ```text
  C_1=(alpha^2-beta(beta+r))X,       C_2=alpha X.   (12)
  ```

  Thus `X` lies in the kernel-rich span except when
  `alpha=0` and `beta(beta+r)=0`.  In either exceptional case one leaf pair
  has the two independent relations `ac=0` and `st=0`, so its product rank
  is at most two.  This is already in the certified lower-pair locus.

It remains to let `s` become a coordinate direction.  By symmetry take
`s=uX_2`, `u!=0`, and `t=pX_2+qX_3`.  For `q!=0`, the four minors become

```text
0,
4q^2u^3(2beta+r)^2,
4q^2u^2(alpha-beta)(2beta+r)(-alpha+beta+r),
-4q^2u^2(alpha+beta)(2beta+r)(alpha+beta+r).       (13)
```

Hence `r=-2beta`.  On this sheet

```text
C_1-2alpha C_2+(alpha^2-beta^2)X=0.               (14)
```

If `alpha^2!=beta^2`, the active cubic lies in the forbidden span.  If
`alpha=+/-beta`, the synchronized pair `U_1U_2` has rank exactly two.  If
`q=0`, all three displayed triangle planes live in a three-coordinate source
subspace and any survivor is an embedded-`P_3` suspension.  Finally `s=0`
is lower-pair, while `t=0` makes `X=a^2d` a multiple of `a^3=0`.

Equations (8)--(14) therefore exhaust every projective complementary
direction in the `CC` orientation.

## A pure family on the first sheet

It suffices by symmetry to use `L_1`.  Thus

```text
B=A,                 G=-(2A+R)/2.                 (15)
```

Set `u=(1-D)/2`, `v=(1+D)/2` and define

```text
y_0=(0, D(2A+R), -u, v),
x_0=(-Av, A(u+1)+R, 1, 0),
U_0=<y_0,x_0>.                                    (16)
```

Direct expansion gives

```text
P_4|_(U_0,U_1,U_2,U_3)=(D+1)e_1^*e_1^*e_1^*e_1^*. (17)
```

On `D!=-1` this is a nonzero pure tensor.  The apparent collapse of the
displayed basis at `D=-1` is only a basis-chart failure: every Pluecker
coordinate of `y_0 wedge x_0` contains `D+1`, and after removing it the
six coordinates are

```text
( A D(2A+R)/2,
  A(D-1)/4,
  A(D+1)/4,
  (AD+3A+2R)/4,
  (AD-3A-2R)/4,
  -1/2 ).                                         (18)
```

They extend regularly and never vanish simultaneously.  This supplies the
projective `D=-1` boundary of the same family.  The condition needed for the
active cubic to escape the kernel-rich span is exactly the already assumed
nonzero sum of the coefficients of `t`.  The coordinate values `D=+/-1`
may lower a rank-four pair to rank three but stay on the all-pair locus.

At

```text
(A,R,D)=(1,1,2)                                   (19)
```

the pair profile in order `01,02,03,12,13,23` is

```text
(4,4,4,3,3,3),                                    (20)
```

and the exceptional relation ranks are `(2,1,1)`.

## Component certificate and separation

Restore the projective diagonal source torus

```text
diag(t_0,t_1,t_2,1).                              (21)
```

In the ordered Grassmann chart with pivot `(01)` on all four planes, the
six columns `(A,R,D,t_0,t_1,t_2)` have tangent rank five at (12).  One exact
minor is

```text
-1/5184.                                          (22)
```

The universal twenty-variable Segre-incidence Jacobian has rank fifteen at
the same point, with exact minor

```text
1/23328.                                          (23)
```

Thus the incidence is smooth of dimension five, and the irreducible
parameter-torus image supplies all local directions.  Its closure is an
irreducible component.

Dimension and pair profile eliminate the lower-pair, all-pair-three, and
six-dimensional components.  The relation-rank word eliminates the
rank-one-triangle components.  Among the older `(2,1,1)` triangle
fivefolds, component one has adjacent rather than coincident exact-pair
support labels, component eleven has the opposite kernel/active incidence,
and component thirteen has proportional complementary directions.  Here
the two rank-one edges have the same exact-pair label `{0,1}`, the leaves are
active, and `[b,t]=D!=0`.  These intrinsic properties separate the dense
family from all twenty-one previously certified orbits.

## Replay

```text
uv run --with sympy python claims/p4/classifications/verify_p4_unequal_complement_common_kernel_component.py
uv run --with sympy python claims/p4/classifications/audit_p4_unequal_complement_common_kernel_component.py
```

Both replays use exact characteristic-zero arithmetic.  The audit rebuilds
the tensor independently after a source permutation and unequal diagonal
scaling.  No finite-field sample is used as proof.
