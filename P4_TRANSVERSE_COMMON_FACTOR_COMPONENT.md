# A twelfth pure `P_4` component from transverse binary polarity

## Status

**Exact component theorem over `C`.**  The pure restriction locus of the
order-four permanent has a five-dimensional irreducible component which is
inequivalent to the eleven previously certified component orbits.  It has a
two-parameter common-factor normal form whose diagonal-source orbit already
has dimension five.  The universal incidence has one excess tangent
direction along this family, but an exact quadratic coefficient obstructs
that direction; the displayed family therefore fills a component rather
than lying in a sixfold.

On a dense open of the component the pair-image profile, in edge order
`01,02,03,12,13,23`, is

```text
(3,3,4,3,3,3).                                      (1)
```

The unique relation on edge `12` has coefficient rank two.  The four
relations on `01,02,13,23` have coefficient rank one, and `03` has full pair
rank four.  The resulting five-edge exceptional graph is pictured in
[`P4_TRANSVERSE_COMMON_FACTOR_COMPONENT_GRAPH.svg`](P4_TRANSVERSE_COMMON_FACTOR_COMPONENT_GRAPH.svg).

This raises the certified lower bound from eleven to twelve symmetry-
inequivalent pure-`P_4` component orbits.  It is not component exhaustiveness,
does not prove component exhaustiveness or the global Krenn--Gu conjecture.
The new component's generic `H31` and weighted `H22` fibres are open.

## The orientation collapses to one exact pair

Work in the squarefree Frobenius algebra

```text
R=C[X_0,X_1,X_2,X_3]/(X_0^2,X_1^2,X_2^2,X_3^2).   (2)
```

In a marked pure restriction, `y_i` is the kernel row and `x_i` the active
row.  A pair relation cannot contain a nonzero `x_i x_j` coefficient: after
multiplication by the other two active rows and evaluation against the pure
tensor, that coefficient would kill the sole nonzero all-active entry.
Consequently a rank-one zero product can never use active rows at both ends.

Suppose two rank-one edges share the same nonkernel row at their common mode,
and that row has genuine two-coordinate support.  Normalize its exact
zero-divisor pair to

```text
a=X_0+X_1,                 c=X_0-X_1,
a c=0,                     Ann_R1(c)=C a.            (3)
```

Both leaf factors must be kernel rows, and the one-dimensional annihilator in
(3) forces

```text
y_1=y_2=a,                 x_3=c.                    (4)
```

The rank-two edge may then be Borel-normalized to

```text
y_1x_2-x_1y_2=0.
```

Writing `x_1=m`, the annihilator identity gives the synchronization law

```text
x_2=m+r c.                                             (5)
```

Thus the entire common-active, support-two orientation reduces to one exact
pair and one synchronized partner.  No enumeration of graphs or finite
fields is involved.

## Two binary bilinear invariants

Split off the complementary binary block and, modulo the irrelevant `a`
component of `m`, write

```text
m=beta*c+s,                  s=u X_2+v X_3,
y_3=gamma*a+delta*c+t,       t=p X_2+q X_3.          (6)
```

There are two natural bilinear invariants of the ordered pair `(s,t)`:

```text
A=<s,t>=u q+v p,             Q=[s,t]=u q-v p.        (7)
```

Here `Q=0` is the diagonal in `P^1 x P^1`: the two binary directions are
proportional.  The equation `A=0` is the graph of the split-polar involution:
`t` is the exact-zero-divisor partner of `s`.  The transverse chart is
`AQ!=0`.

Let `W` be the span of the three kernel-containing cubics

```text
a^2 y_3,                 a m y_3,
m(m+r c)y_3.                                         (8)
```

The opposite plane can annihilate them only if `dim W<=2`.  Put
`E=(2 beta+r)A`.  In the degree-three basis indexed by the missing source
coordinate, the four maximal minors of (8) are

```text
 4q A (E+2 delta u v),
 4p A (E+2 delta u v),
-4(gamma-delta) Q (E-2 gamma u v),
 4(gamma+delta) Q (E+2 gamma u v).                  (9)
```

Formula (9) is the promised change of shape.  A three-cubic apolarity
condition has become the intersection of the diagonal and polarity graphs
inside `P^1 x P^1`, plus two coordinate-polar transverse sheets.

- On `A=0`, nonzero purity removes the residual `c` part of `y_3`; this is
  the exact-partner sheet that opens into the eleventh component.
- On `Q=0`, (9) forces one affine synchronization equation.  Its apolar
  plane is `span(c,s_bar)`, and after exchanging the opposite modes it is the
  `q=0` boundary of the eleventh component.
- On `AQ!=0`, equations (9) reduce to `gamma^2=delta^2`.  Thus the
  `a,c` projection of `y_3` is supported on exactly one of `X_0,X_1`.
  These are the two source-symmetric transverse `1+3` polarity sheets.  One
  of them produces the new component below.

For completeness, these reductions use only cancellation on the indicated
dense binary chart.  If `A=0`, then `Q!=0` and the last two minors first give
`gamma=0`.  Writing `y_3=delta*c+t`, the third cubic in (8) is `delta` times
the all-active cubic modulo the line `C*a^2t`; nonzero purity therefore forces
`delta=0`.  If `Q=0`, rescale to `t=s`.  The first two minors give
`delta=-(2*beta+r)`, and (8) spans exactly
`{a^2s,a s^2}`.  Its annihilator is `span(c,s_bar)`, which becomes the
`q=0` eleventh-component boundary after exchanging the two opposite modes.
Finally, on `AQ!=0`, the first two minors give
`E=-2*delta*u*v`; substituting this into the last two leaves
`gamma^2-delta^2=0`.  No ideal decomposition is needed.

The split is the degree-one shadow of a quadratic involution on binary
forms.  Abdesselam and Chipalkatti study quadratic-form-induced involutions
through transvectants in a far more general setting
([arXiv:1008.3117](https://arxiv.org/abs/1008.3117)).  Kustin--Striuli--Vraciu
give the neighboring commutative-algebra language of exact homogeneous zero
divisors ([arXiv:1304.0411](https://arxiv.org/abs/1304.0411)), while Shafiei
studies apolar ideals of generic permanents
([arXiv:1212.0515](https://arxiv.org/abs/1212.0515)).  None of those papers
states (9) or the component below; the useful synthesis here is

```text
exact annihilator line -> binary polarity involution
                       -> three-cubic apolar compression
                       -> permanent component.                    (10)
```

## The transverse pure sheet

Put `b=X_2+X_3`.  On one transverse sheet define, for parameters `r,k`,

```text
m =b+c,
m_r=b+(1+r)c,
d =(r+2)(k+1)X_1+X_2+kX_3,
n =-(k-1)(r+2)X_0-X_2+kX_3,                         (11)

U_0=span(n,c),
U_1=span(a,m),
U_2=span(a,m_r),
U_3=span(d,c).                                      (12)
```

Use the displayed row order `(y_i,x_i)`.  Substitution in (9) has

```text
s=X_2+X_3,       t=X_2+kX_3,
A=k+1,           Q=k-1,                            (13)
```

and the single-coordinate term in `d` is exactly the transverse solution.
The row `n` spans the common annihilator of the kernel-rich cubics together
with `c`.  Direct Frobenius pairing gives the strikingly rigid identity

```text
P_4|_(U_0 x U_1 x U_2 x U_3)=-4 x_0x_1x_2x_3.      (14)
```

Thus every one of the other fifteen binary coefficients vanishes
identically, while the pure coefficient is the constant `-4`.

On a dense open of `(r,k)`, the unique relations are

```text
x_0y_1=0,        x_0y_2=0,
y_1x_2-x_1y_2=0,
y_1x_3=0,        y_2x_3=0.                         (15)
```

The edge `03` has rank four.  Explicit nonzero pair minors are recorded by
the verifier; at

```text
(r,k)=(-4/3,2)                                      (16)
```

they give exactly the profile (1) and relation-rank multiset
`{1,1,1,1,2}`.

## Five component directions and one obstructed tangent

Restore the projective diagonal source torus

```text
diag(t_0,t_1,t_2,1).                                (17)
```

Use Grassmann pivot charts

```text
(21),(02),(02),(20)                                 (18)
```

for modes zero through three.  At (16) and `t_0=t_1=t_2=1`, the family
Jacobian with respect to `(r,k,t_0,t_1,t_2)` has rank five.  The rows

```text
g_0,g_1,g_2,g_6,g_7
```

give determinant

```text
2.                                                   (19)
```

This is the five-dimensional common-factor sheet promised above.

For the universal pure-Segre incidence on the same Grassmann charts, use the
all-active target chart.  At (16), the normalized restriction has only
`T_1111=4`.  Fourteen incidence rows, namely all rows except `1111` and the
row indexed by `1001`, against columns

```text
g_0,...,g_9,g_15,z_0,z_1,z_3
```

have determinant

```text
-131072.                                             (20)
```

Hence the incidence Jacobian has rank fourteen in twenty variables.  This
leaves a six-dimensional Zariski tangent space, one dimension larger than the
family.  Rank alone therefore does **not** prove a six-dimensional component.

To decide the excess direction, use the fourteen rows in (20) as regular
local equations and take the omitted pure-factor ratio `z_2=h` as the sixth
implicit coordinate.  Hold the other five free coordinates at (16), and
solve those fourteen equations through order two.  The omitted `1001`
incidence equation then has expansion

```text
12 h^2+O(h^3).                                      (21)
```

Thus it is a nonzero function in the regular six-dimensional local ring cut
out by the selected equations.  The full incidence has local dimension at
most five.  The five independent family directions in (19) give the reverse
inequality.  Since the parameter space is irreducible, its five-dimensional
image closure is an irreducible component of the incidence.  A nonzero pure
tensor has unique projective factors, so projection to the plane locus
preserves that component.  The apparent sixth direction is quadratically
obstructed, and (12) is a dense normal form for a fivefold.

## Why this component is new

Dimension separates it from the three previously certified sixfolds.  Every
one of the eight earlier fivefolds has generic sorted pair profile

```text
(3,3,3,4,4,4),
```

whereas (1) sorts to

```text
(3,3,3,3,3,4).                                      (22)
```

Pair-image rank and component dimension are invariant under source
permutations, diagonal source scaling, and mode permutations.  Since (12)
is dense in its component, (22) separates it from every earlier fivefold.
As an additional local invariant, at (16) the seven kernel-containing
cubics span dimension exactly two for each of the four three-mode subsets;
the equal-support sixfold has a distinguished span of dimension at most one.

This proves that the new component is a twelfth symmetry orbit.

## Verification

Run:

```text
uv run --with sympy python verify_p4_transverse_common_factor_component.py
python audit_p4_transverse_common_factor_component.py
```

The primary verifier checks (3)--(22) over `Q`, including the four factored
binary-polarity minors, the complete symbolic family, all six pair ranks,
all four mixed-cubic span ranks, the exact tangent minors, and the quadratic
transverse coefficient `12`.  The independent
audit reconstructs permanents by subset dynamic programming and replays the
pair, triple-span, family-tangent, incidence, and second-order implicit
certificates over two unrelated
finite fields.  These are fixed-size exact certificates for the displayed
symbolic theorem, not searches.
