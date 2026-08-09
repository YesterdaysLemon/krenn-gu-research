# Exact high-coordinate partial-row frontier for `P_5`

## Status

This is an exact reduction over `C`, with a finite-assisted census of
the already covered local pair signatures.

The earlier statement that a local map with at least four coordinate
rows has only the three types

```text
q4_211, q5_311, q5_221
```

was incomplete.  Four coordinate rows can use only two target
coordinates, with multiplicities `3+1` or `2+2`, while the fifth row is
partial and supplies the missing coordinate.

After applying the complete exact-three-coordinate theorem, the
complete partial-`q4_211` theorem, the exact `q5_221` theorem, and the
two-singleton theorem, every hypothetical restriction

```text
P_5 -> Delta_3
```

must have a local map in one of exactly two normalized families:

```text
H31: e_0,e_0,e_0,e_1, a e_0+b e_1+c e_2,   b c != 0;
H22: e_0,e_0,e_1,e_1, a e_0+b e_1+c e_2,   c != 0,
                                                (a,b) != (0,0).       (1)
```

Here nonzero rescalings of individual source rows have been absorbed
by the usual simultaneous diagonal source rescaling.  This statement
is a necessary reduction, not an existence theorem.  Neither family
is excluded below.

In the 6,495-signature catalogue there are 1,680 signatures with at
least four coordinate rows.  Existing exact theorems exclude 1,170 of
them.  The two families in (1) account for the remaining 510:

| local family | target support counts | signatures | status |
| --- | ---: | ---: | --- |
| exact `q5_311` | `(3,1,1)` | 60 | two-singleton obstruction |
| exact `q5_221` | `(2,2,1)` | 90 | exact `q5_221` theorem |
| `q4_211` plus a zero row | `(2,1,1)` | 180 | two-singleton obstruction |
| partial `q4_211` | `(2,2,2)` or `(3,2,1)` or `(3,2,2)` | 720 | complete `q4_211` theorem |
| partial `3+1`, majority plus missing | `(4,1,1)` | 120 | two-singleton obstruction |
| `H31`, `a=0` | `(3,2,1)` | 120 | open |
| `H31`, `a!=0` | `(4,2,1)` | 120 | open |
| `H22`, exactly one of `a,b` nonzero | `(3,2,1)` | 180 | open |
| `H22`, `a b!=0` | `(3,3,1)` | 90 | open |

The exact-three-coordinate theorem ensures that some high-coordinate
mode exists.  An already excluded row type cannot occur in any mode
of a hypothetical restriction.  Hence (1) is the honest current
global frontier.

## The `H31` common-three pencil

Let the source coordinates be `0,...,4`, and let `Phi` denote
contraction of `P_5` followed by the other four local maps.  For `H31`
the pullbacks of the three target-coordinate covectors are

```text
u_0=e_0+e_1+e_2+a e_4,
u_1=e_3+b e_4,
u_2=c e_4.                                           (2)
```

If the diagonal coefficients are `lambda_i!=0`, then

```text
Phi(u_i)=lambda_i E_i^4.                             (3)
```

Linearity gives

```text
Phi(e_4)=(lambda_2/c)E_2^4,
Phi(e_3)=lambda_1 E_1^4-(b lambda_2/c)E_2^4.         (4)
```

Both source contractions in (4) are embedded `P_4` tensors.  They
share source rows `0,1,2`; the first maps to a nonzero pure tensor and
the second maps sharply to `Delta_2`.  Thus `H31` is a simultaneous
common-three

```text
(P_4 -> pure, P_4 -> Delta_2)
```

pencil.  This explains exactly why the old `q5_311` proof stops: its
rank-drop theorem applies to the first slice, but the second slice has
flattening rank two rather than one.

The remaining contraction is

```text
(e_0+e_1+e_2) contracted into P_5
 = Sym(e_3,e_4) tensor
   (e_0 e_1+e_0 e_2+e_1 e_2),                       (5)
```

in polynomial notation.  It maps to a pure tensor when `a=0` and to
`Delta_2` when `a!=0`.  This is the sharp support-three boundary, not
a contradiction.

## The `H22` three-normal pencil

For `H22`, put

```text
v_0=e_0+e_1,   v_1=e_2+e_3,   v_2=e_4.              (6)
```

The target pullbacks are

```text
u_0=v_0+a v_2,
u_1=v_1+b v_2,
u_2=c v_2.                                           (7)
```

Consequently

```text
Phi(v_2)=(lambda_2/c)E_2^4,
Phi(v_0)=lambda_0 E_0^4-(a lambda_2/c)E_2^4,
Phi(v_1)=lambda_1 E_1^4-(b lambda_2/c)E_2^4.         (8)
```

All three source contractions are embedded copies of `P_4`:

```text
v_0 contracted into P_5 = Sym(e_0+e_1,e_2,e_3,e_4),
v_1 contracted into P_5 = Sym(e_0,e_1,e_2+e_3,e_4),
v_2 contracted into P_5 = Sym(e_0,e_1,e_2,e_3).      (9)
```

Their source hyperplane normals are

```text
h_0=e_0^*-e_1^*,
h_1=e_2^*-e_3^*,
h_2=e_4^*.                                          (10)
```

The `h_2` slice maps to a pure tensor.  The other two map to a pure
tensor or to `Delta_2`, and at least one maps to `Delta_2`.  Thus
`H22` is a common-target-colour, partially marked analogue of
`q5_221`.  The exact `q5_221` incidence theorem cannot simply be
reused: only the pure slice forces two rank drops; the marked slices
require the `P_4 -> Delta_2` geometry.

## Current `H31` obstructions

The known five-parameter family of all-rank-two maps sending `P_4` to
a pure tensor is now known to be a dense chart in a generically smooth
five-dimensional component of the pure-compression locus:

- [`P4_PURE_RANK_TWO_COMPONENT_THEOREM.md`](claims/p4/classifications/pair-geometry/pure-rank-two/P4_PURE_RANK_TWO_COMPONENT_THEOREM.md)

That component is not exhaustive.  Recasting `P_4` as the Frobenius
intersection form of

```text
C[X_0,X_1,X_2,X_3]/(X_0^2,X_1^2,X_2^2,X_3^2)
```

identifies exceptional plane pairs with annihilator lines lying on a
common diagonal quadric.  A radical-plane normal form then produces an
irreducible `(3,3)` hypersurface in `P^2 x P^2`; its diagonal-source
orbit is a second five-dimensional pure-compression component.  An
exact tangent-cone certificate proves component status, and a
diagonal-quadric jump invariant separates it from every symmetry
translate of the first component:

- [`P4_DIAGONAL_QUADRIC_PURE_COMPONENT.md`](claims/p4/components/diagonal-quadric/P4_DIAGONAL_QUADRIC_PURE_COMPONENT.md)

The same diagonal-quadric map has now exposed three more components.
For a `1+3` block line, the radical-plane normal form reduces the pure
condition to

```text
(D-G-S+T)(D+G-S-T)(D+G+S+T)=0.
```

Each factor has a rank-five family tangent and a smooth rank-fifteen
Segre-incidence certificate.  The five known component orbits have
distinct generic jump signatures

```text
(# 2+2, # 1+3) =
(2,1), (1,0), (1,1), (0,2), (0,1).
```

Thus at least five symmetry-inequivalent components exist.  This is
not yet an exhaustive classification:

- [`P4_DIAGONAL_QUADRIC_ONE_THREE_COMPONENTS.md`](P4_DIAGONAL_QUADRIC_ONE_THREE_COMPONENTS.md)

The most natural apparent continuation, with all four annihilator
lines on one smooth diagonal quadric, is now closed away from the
block-line jump locus.  Normalize the quadric and use its two spinor
rulings.  Up to symmetry the only patterns are `LLLL`, `LLLR`, and
`LLRR`.  Exact characteristic-zero saturation gives no nonzero pure
`LLLL` point and one-dimensional normalized pure closures for each
mixed pattern; a second saturation by

```text
product_i s_i(s_i^4-1)
```

is the unit ideal.  Thus every nonzero pure common-smooth-quadric
solution has a `2+2` or `1+3` block line, and none of these loci can
be a new five-dimensional component after restoring the
three-dimensional diagonal source torus:

- [`P4_COMMON_SMOOTH_DIAGONAL_QUADRIC_OBSTRUCTION.md`](P4_COMMON_SMOOTH_DIAGONAL_QUADRIC_OBSTRUCTION.md)

There is also an exact generic classification on the directed
radical-star block locus.  A rank-one multiplication relation is
precisely a zero product in the squarefree complete intersection, so
it is supported on a source-coordinate pair.  If two such relations
point away from a common mode, their support pairs are disjoint
(`2+2`) or overlap once (`1+3`), and the common plane is forced to be
the radical of the corresponding double contraction.  The dense
normal forms are exhaustive: the `2+2` determinant is the irreducible
`(3,3)` polynomial of the second component, while the `1+3`
determinant is the three-factor split cubic.  Hence this stratum
contains exactly those four certified component closures:

- [`P4_RADICAL_STAR_COMPONENT_CLASSIFICATION.md`](claims/p4/classifications/star/radical-star/P4_RADICAL_STAR_COMPONENT_CLASSIFICATION.md)

The mixed kernel-edge orientation omitted by that radical
classification produces a sixth component.  With two fixed
coordinate-pair zero products, the seven kernel-containing
contractions reduce to a `3 x 4` matrix.  Its rank-at-most-two ideal
has five exact linear minimal primes.  One prime yields an explicit
three-parameter normalized family with

```text
T_0000=2q(d+p+q).
```

Its diagonal-source orbit has a rank-five family tangent, and a
rank-fifteen Segre-incidence Jacobian proves a smooth
five-dimensional component.  The coarse jump signature `(0,1)`
coincides with `L_3`, but the directed rank-one relation invariant
does not: the new sorted pure-kernel endpoint indegrees are
`(2,1,0,0)`, versus `(1,1,1,0)` on all three split-cubic branches.
Thus at least six symmetry-inequivalent component orbits exist:

- [`P4_MIXED_ORIENTATION_PURE_COMPONENT.md`](claims/p4/components/mixed-orientation/P4_MIXED_ORIENTATION_PURE_COMPONENT.md)

The sixth component is generically excluded from `H31`.  Exact
function-field projection leaves no marking for distinguished
coordinates zero and one and two rational sheets for each of
coordinates two and three.  Four all-extension determinant identities,
together with nonzero pure transverse entries, exclude every survivor.
Its special parameter divisors and projective boundary remain:

- [`P5_H31_MIXED_ORIENTATION_COMPONENT_GENERIC_OBSTRUCTION.md`](claims/p5/h31/mixed-orientation/P5_H31_MIXED_ORIENTATION_COMPONENT_GENERIC_OBSTRUCTION.md)

A lower-pair-rank prime of the same determinantal calculation opens
into a larger component.  Put `h=a+c-d` and take

```text
U0=span((1,0,0,-1),(0,0,1,1)),
U1=span((1,b,0,1-bh),(0,e,1,1-eh)),
U2=span((1,0,-1,0),(0,1,-a-c,-d)),
U3=span((1,0,0,1),(0,0,1,-1)).
```

Only `T_1010=2(1-b(a+c))` and
`T_1110=2(1-e(a+c))` survive.  The family-plus-source-torus map has
rank six, while a smooth Segre-incidence point has Jacobian rank
fourteen in twenty variables.  This proves a rational
six-dimensional component.  Its pair profile `(4,3,2,4,4,3)` and
dimension place it outside all six certified fivefold orbits:

- [`P4_SIX_DIMENSIONAL_PURE_COMPONENT.md`](claims/p4/components/six-dimensional/P4_SIX_DIMENSIONAL_PURE_COMPONENT.md)

The new component is also generically excluded from `H31`.  The
apolar parameters

```text
s=a+c,  u=1-sb,  v=1-se
```

reduce the normalized family to four variables.  Distinguished
coordinate one has no genuine binary marking: its ubiquitous kernel
direction merely restores the deleted coordinate and reconstructs the
pure tensor.  Each of coordinates zero, two, and three has one
rational marking, and three selected mode-zero minors generate the
unit ideal after inverting the two binary diagonals:

- [`P5_H31_SIX_DIMENSIONAL_COMPONENT_GENERIC_OBSTRUCTION.md`](claims/p5/h31/six-dimensional/P5_H31_SIX_DIMENSIONAL_COMPONENT_GENERIC_OBSTRUCTION.md)

The same component also supplies the first generic weighted `H22`
obstruction.  The relevant neighboring source bases are diagonal
rather than coordinate deletions, and the residual source torus must
be retained:

```text
D_01^r(q)=(r q_0+q_1,q_2,q_3,q_4),
D_23^r(q)=(q_0,q_1,r q_2+q_3,q_4).
```

Over `C(s,d,u,v,r)`, the first pencil has unit binary projection.  The
second leaves precisely

```text
t_0=0,
(u-v)t_1+u-1=0,
(u-v)t_2-sv=0,
t_3 free.
```

Its mixed kernel is two-dimensional, but one line has both desired
diagonals zero.  On every genuine direction, the mode-zero marked map
has rank four: the saturated ideal of its `0127` and `0137` minors is
unit.  Hence the binary sheet has no ternary lift:

- [`P5_H22_SIX_DIMENSIONAL_COMPONENT_GENERIC_OBSTRUCTION.md`](claims/p5/h22/six-dimensional/P5_H22_SIX_DIMENSIONAL_COMPONENT_GENERIC_OBSTRUCTION.md)

The mixed-orientation fivefold is now generically excluded from
weighted `H22` as well.  Over `C(d,p,q,r)`, the weighted `01`
mixed-coefficient matrix has full column rank for every marking.  An
eight-chart hierarchical cover of its projective extension kernel has
unit ideal on every chart.  For the weighted `23` pencil, five exact
low-degree marking relations cover every genuine binary point by three
closed sheets.  On each sheet, the saturated ideal of mode-three
minors `0267` and `0467` is unit, so every survivor has marked rank
four:

- [`P5_H22_MIXED_ORIENTATION_COMPONENT_GENERIC_OBSTRUCTION.md`](claims/p5/h22/mixed-orientation/P5_H22_MIXED_ORIENTATION_COMPONENT_GENERIC_OBSTRUCTION.md)

All three split-cubic `1+3` components are now generically excluded
from weighted `H22`.  Every weighted `01` binary projection is unit,
as is the `L_3` weighted `23` projection.  The `L_1` survivor scheme
has two rational points and the `L_2` scheme is covered by three
affine lines.  On all five survivor closures, the same mode-zero
`0247` minor generates a unit ideal after diagonal saturation:

- [`P5_H22_ONE_THREE_COMPONENTS_GENERIC_OBSTRUCTION.md`](claims/p5/h22/one-three-components/P5_H22_ONE_THREE_COMPONENTS_GENERIC_OBSTRUCTION.md)

The first rank-two component is now generically excluded from weighted
`H22` too.  The weighted `01` mixed matrix is injective for every
marking by an eight-chart projective cover.  The exact weighted `23`
projection has two sheets, excluded by the mode-two `0147` and `0137`
minors:

- [`P5_H22_FIRST_RANK_TWO_COMPONENT_GENERIC_OBSTRUCTION.md`](claims/p5/h22/first-rank-two/P5_H22_FIRST_RANK_TWO_COMPONENT_GENERIC_OBSTRUCTION.md)

The equal-weight specialization remains a separately verified boundary
certificate:

```text
D_01(r)=(r_0+r_1,r_2,r_3,r_4),
D_23(r)=(r_0,r_1,r_2+r_3,r_4).
```

At equal source weights, exact saturation of the fourteen
mixed binary equations by both desired diagonals gives the unit ideal
for each pencil.  The `D_23` calculation has a two-row explanation:
the `1000` equation forces the marking `t_0=1`, and then the `1110`
row is `su/(u-v)` times the required first diagonal.  Thus no binary
`Delta_2` neighbor exists before the third target row is considered:

- [`P5_H22_SIX_DIMENSIONAL_EQUAL_WEIGHT_BINARY_OBSTRUCTION.md`](claims/p5/h22/six-dimensional/P5_H22_SIX_DIMENSIONAL_EQUAL_WEIGHT_BINARY_OBSTRUCTION.md)

The generic weighted theorems close the seven previously certified
component orbits.  The final diagonal-quadric case uses the projective
Segre-join/properness obstruction rather than a generic determinantal
elimination.  The subsequently certified disjoint mixed-star eighth
component is now generically excluded from `H31`, but not yet from
weighted `H22`.  Special slope/parameter divisors, component
boundaries, and component exhaustiveness remain open.

The five minimal primes in the mixed `3 x 4` determinantal chart are
now completely identified.  The first and third are the sixth
component orbit, the second embeds in the six-dimensional component,
and the fourth and fifth are explicit source/mode symmetry charts of
`L_2` and `L_1`.  Hence that dense chart contains no eighth component:

- [`P4_MIXED_DETERMINANTAL_PRIME_CLASSIFICATION.md`](P4_MIXED_DETERMINANTAL_PRIME_CLASSIFICATION.md)

The complete marked fibre over the generic point of each of the three
new components is empty.  One branch has no neighbouring binary
`Delta_2` slice.  On the other two, function-field projection gives
two rational survivor families, and every extension satisfies

```text
det = A^2 B / c(S,D,G),
```

where `A,B` are the required nonzero binary diagonals and `c` is
nonzero on the generic chart.  Their special parameter divisors and
projective boundaries remain:

- [`P5_H31_ONE_THREE_COMPONENT_GENERIC_OBSTRUCTION.md`](claims/p5/h31/one-three/P5_H31_ONE_THREE_COMPONENT_GENERIC_OBSTRUCTION.md)

At one rational point of the second component, the complete marking
fibre has already been excluded.  Exact binary projection leaves one
marking for each of `q=0,3` and none for `q=1,2`; every extension in
the two surviving two-dimensional kernels has the uniform injective
marked minor `-8u(u-2v)^2`:

- [`P5_H31_DIAGONAL_QUADRIC_COMPONENT_POINT_OBSTRUCTION.md`](P5_H31_DIAGONAL_QUADRIC_COMPONENT_POINT_OBSTRUCTION.md)

There is now also a complete relative result on the rational curve
`A=B=E=F=H=1, C=c` in the `(3,3)` component.  Its pure coefficient is
`4(c+1)`, so the whole nonzero-pure curve is `c!=-1`.  A single
relative projection over `Q[c]`, saturated by `c+1`, proves that there
are no hidden exceptional fibres.  Its function-field part leaves only
the `q=0,2` markings; exact fibres at `c=0,1` supply the only
specialization jumps.  In every survivor
kernel, the selected marked minor factors as the product of the two
required nonzero binary diagonal factors, with one factor repeated.
Thus every marking over every point of this curve is excluded:

- [`P5_H31_DIAGONAL_QUADRIC_CURVE_MARKED_FIBRE_OBSTRUCTION.md`](P5_H31_DIAGONAL_QUADRIC_CURVE_MARKED_FIBRE_OBSTRUCTION.md)

A second relative theorem closes the transverse curve
`A=B=F=H=1,C=0,E=e` for every `e in C`.  This curve contains the
earlier isolated rational point at `e=2` and meets the first closed
curve at `e=1,c=0`.  A global projection over `Q[e]` has two uniform
survivor markings and only the jumps `e=0,+/-1`; every survivor again
has a marked minor equal to a nonzero binary diagonal product:

- [`P5_H31_DIAGONAL_QUADRIC_E_CURVE_MARKED_FIBRE_OBSTRUCTION.md`](P5_H31_DIAGONAL_QUADRIC_E_CURVE_MARKED_FIBRE_OBSTRUCTION.md)

The remaining pure-factor-direction curve `C=-1,E=e` has a different
marking chart.  Saturated relative projection leaves only one `q=2`
marking, and its marked minor is `-64e u(u-2v)^2`.  Since on
`A=B=F=H=1` the component equation factors as
`C(C+1)(1-E^2)`, and `E=-1` is source-symmetric to `E=1`, these three
curve calculations close the complete nonzero factored slice:

- [`P5_H31_DIAGONAL_QUADRIC_PURE_DIRECTION_CURVE_MARKED_FIBRE_OBSTRUCTION.md`](P5_H31_DIAGONAL_QUADRIC_PURE_DIRECTION_CURVE_MARKED_FIBRE_OBSTRUCTION.md)

They also close its full source/mode symmetry orbit.  In particular,
the source permutation `(0 1)(2 3)` and mode swap `1<->2` carry the
closed `C=c` curve to the transverse line
`A=B=C=E=F=1,H=h`.

There is also a complete interior slice away from that factorization.
On `A=B=F=1,H=0`, the component equation is
`1-C^2E^2=0`.  Exact relative projection closes the ruling
`CE=1`; the source swap `X_0<->X_3` exchanges it with `CE=-1`.
Thus the complete nonzero `H=0` slice and its source/mode orbit are
excluded:

- [`P5_H31_DIAGONAL_QUADRIC_H0_RULING_MARKED_FIBRE_OBSTRUCTION.md`](P5_H31_DIAGONAL_QUADRIC_H0_RULING_MARKED_FIBRE_OBSTRUCTION.md)

The second component now also has a generic obstruction.  On
`A=B=F=1`, put

```text
U=C+H, S=1+CH, T=H+CE^2.
```

Then `Psi=S^2-UT`.  On `U!=0`, the conic ratio `r=S/U` and coordinates
`x=1-rH,Y=rEx` give the elliptic surface

```text
Y^2=x[(1-r^2)x^2+(3r^2-2)x+(r^2-1)^2].
```

Over its function field, exact saturated binary projection returns
`(1)` for every distinguished coordinate and every marking.  Hence
the generic marked `H31` fibre is empty and every remaining survivor
lies on a proper closed subset.  The two `H=0` rulings are the sections
`(x,Y)=(1,+/-r^2)`; the factored `H=1` slice lies over the singular
fibre `r=1` or the birational base locus.  This explains the previous
slice theorems.  The minimal resolution is a K3 surface with reducible
fibre root rank 17.  The known section is non-torsion, so
Shioda--Tate forces Picard number 20; good-reduction point counts give
Mordell--Weil group `Z + Z/2`.  This
strongly constrains survivor sections but does not prove that the
known sections contain every survivor curve or multisection:

- [`P5_H31_DIAGONAL_QUADRIC_ELLIPTIC_GENERIC_OBSTRUCTION.md`](P5_H31_DIAGONAL_QUADRIC_ELLIPTIC_GENERIC_OBSTRUCTION.md)

The first proper-support refinement avoids a global elimination.  For
`q=1,2`, the mixed matrix has a marking-independent kernel line.  After
quotienting that line, one `6 x 6` pivot and its bordered minors split
the possible rank-drop locus into two elementary branches.  On the
dense pivot chart, one branch is forced to `x=1` with exactly the
already-closed `H=0` marking; the other reaches only
`x=1+/-r` or `r=+/-1`, already-closed pure-direction or singular-fibre
loci.  Thus no new survivor curve occurs on this chart:

- [`P5_H31_ELLIPTIC_MIDDLE_COORDINATE_RANK_DROP.md`](P5_H31_ELLIPTIC_MIDDLE_COORDINATE_RANK_DROP.md)

For `q=0,3`, canonical reduction in the quadratic function field exposes
equally small universal kernels.  Deleting their unit `a1` component,
one bordered minor proves that the quotient has full rank on the dense
chart `t2!=x,t3!=1`, away from the standard geometric factors:

- [`P5_H31_ELLIPTIC_END_COORDINATE_FULL_RANK_CHART.md`](P5_H31_ELLIPTIC_END_COORDINATE_FULL_RANK_CHART.md)

On the deepest end-coordinate intersection `t2=x,t3=1` for `q=0,3`,
compatibility of two quotient minors leaves a conjugate pair of
apparent trisections.  Their common normalization is the smooth
genus-two curve

```text
v^2=(s^3+3s^2+3s+5)(s^3+3s^2-s+1).
```

The marking equations force one rational marking in each endpoint
orientation, but two further full-rank minors have coprime residual
factors `s^3+2s^2-3s+2` and `s^2+1`.  Hence both apparent survivors are
empty:

- [`P5_H31_ELLIPTIC_END_GENUS_TWO_EXCEPTION_OBSTRUCTION.md`](P5_H31_ELLIPTIC_END_GENUS_TWO_EXCEPTION_OBSTRUCTION.md)

The same normalization closes the complete regular `t2=x` divisor.
A small quotient minor first forces `t3=1` or the genus-two
trisection.  On that curve, the remaining marking equations reduce to
two polynomials in `t3` with resultant

```text
-2s(s-1)^2(s+1)(s^2+2s-1)(s^3+3s^2-s+1).
```

The known `x=1` section and degree-drop factors are harmless; at the
only regular quadratic exception, a third minor reduces to
`-2^34 v(12s+29)` and is nonzero:

- [`P5_H31_ELLIPTIC_END_T2_DIVISOR_OBSTRUCTION.md`](P5_H31_ELLIPTIC_END_T2_DIVISOR_OBSTRUCTION.md)

The other complete regular marking divisor `t3=1` is empty as well.
Its apparent quadratic marking cover splits over the elliptic function
field.  On either rational branch, two quotient minors force rank drop
onto the same genus-two trisection.  Pullback to its two sheets gives
the residual factors

```text
positive sheet:  s^2+2s-1  (minus branch),  1 (plus branch);
negative sheet:  s(s-1)(s^2+1) on both branches.
```

The `s=0` factor is the closed `x=1` ruling.  At the remaining values
`s=-1+/-sqrt(2),1,+/-i`, exact mixed and binary-diagonal ranks leave
only the universal kernel line, so no genuine binary extension
survives:

- [`P5_H31_ELLIPTIC_END_T3_DIVISOR_OBSTRUCTION.md`](P5_H31_ELLIPTIC_END_T3_DIVISOR_OBSTRUCTION.md)

The remaining middle-coordinate pivot complement is empty too.  Four
small residual factors cover the three pivot divisors

```text
t0=0,  t3=1,  t2=r^2x.
```

Five terminal quotient minors reduce their only auxiliary base curve
to units.  On the regular two-torsion slice `Y=0`, one adapted
determinant is a chart unit times `t3`, and a second is a chart unit at
`t3=0`.  Hence every marked fibre in the regular elliptic chart is
excluded for all `q=0,1,2,3`:

- [`P5_H31_ELLIPTIC_MIDDLE_COORDINATE_PIVOT_COMPLEMENT.md`](P5_H31_ELLIPTIC_MIDDLE_COORDINATE_PIVOT_COMPLEMENT.md)

The boundary of the elliptic normalization is now closed as well.  On
`U!=0`,

```text
x=C(1-H^2)/U,
D=S(1-H^2)/U^2.
```

Thus `rxD=0` maps to the already closed `H=+/-1` and base-locus
strata, except for two rational curves

```text
C=-1/h, H=h, E=+h or -h.
```

Exact relative binary projection leaves one survivor marking on each
curve.  A mode-one determinant is a chart unit times the two binary
diagonals, with one repeated, and the projective endpoint has no binary
extension.  Both complete curves are therefore excluded:

- [`P5_H31_DIAGONAL_QUADRIC_NORMALIZATION_BOUNDARY_OBSTRUCTION.md`](P5_H31_DIAGONAL_QUADRIC_NORMALIZATION_BOUNDARY_OBSTRUCTION.md)

In one distinguished-source orientation, extending its three common
source entries to the neighbouring hyperplane gives a `14 x 8` linear
mixed-coefficient system.

Off the divisor `l=0`, the system has a one-dimensional kernel and the
second diagonal coefficient is identically zero.  On `l=0`, a genuine
binary `Delta_2` extension exists.  However, at one mode its one-marked
flattening is injective on the `Delta_2` hyperplane, while the
corresponding pure-hyperplane flattening has a transverse
one-dimensional kernel.  A third target row must vanish on both
hyperplanes and hence vanish globally, contradicting rank three:

- [`P5_H31_KNOWN_RANK_TWO_FAMILY_OBSTRUCTION.md`](P5_H31_KNOWN_RANK_TWO_FAMILY_OBSTRUCTION.md)

The other three possible choices of the distinguished family source
coordinate admit an exact parallel analysis.  Off `l=0`, their unique
mixed kernels kill one diagonal.  On `l=0`, one still has no binary
`Delta_2` extension; the two genuine binary survivor orientations have
injective mode-one marked maps and a transverse pure-hyperplane
coordinate.  Thus no member of any source/mode symmetry translate of
the displayed family chart lifts:

- [`P5_H31_RANK_TWO_COMPONENT_ORBIT_OBSTRUCTION.md`](P5_H31_RANK_TWO_COMPONENT_ORBIT_OBSTRUCTION.md)

These calculations exclude the displayed marked row families, not the
whole plane component.  A pure-compression component records four
planes, whereas `H31` additionally marks a kernel row and a
complementary pure-colour row in each plane.  Kernel-row shifts preserve
the pure deletion but change the neighbouring `Delta_2` equations.

The distinction is exact, not merely formal.  On the dense `L!=0`
stratum, an explicit shifted marking over the same four planes has a
genuine binary `Delta_2` extension with diagonals

```text
-2(1+LQ),  2(1+(C+L)Q)/Q.
```

Its mode-two marked determinant is

```text
8(1+LQ)^2(1+(C+L)Q),
```

so that branch still has no ternary lift:

- [`P5_H31_MARKED_BASIS_OPEN_BRANCH.md`](P5_H31_MARKED_BASIS_OPEN_BRANCH.md)

This exposed the marked-basis fibre while preserving the central
lesson that ternary conciseness adds a decisive transverse-kernel
condition.  The complete determinantal incidence has now been solved
over the finite family chart.  It finds every binary-survivor marking,
including three isolated `q=1` points on `C=-L/2`, and proves that
every extension in every survivor kernel has an injective marked map:

- [`P5_H31_MARKED_BASIS_FIBRE_CLASSIFICATION.md`](P5_H31_MARKED_BASIS_FIBRE_CLASSIFICATION.md)

Thus no marked basis over a finite member of the five-parameter family
lifts to `H31`.

The closure of the known component inside its preferred four-
Grassmannian chart has eleven elementary equations.  Its only nonzero
complement to the finite-parameter family is one four-dimensional
divisor; exact mixed-kernel and marked-map analysis excludes the
displayed marked section of that divisor in all four
distinguished-source orientations:

- [`P4_PURE_RANK_TWO_COMPONENT_CHART_CLOSURE.md`](claims/p4/classifications/pair-geometry/pure-rank-two/P4_PURE_RANK_TWO_COMPONENT_CHART_CLOSURE.md)
- [`P5_H31_COMPONENT_CHART_BOUNDARY_OBSTRUCTION.md`](claims/p5/h31/component-chart-boundary/P5_H31_COMPONENT_CHART_BOUNDARY_OBSTRUCTION.md)

The first-plane line at infinity and the coupled three-plane toric base
have also been classified at plane level.  The toric base has 12
divisors, 26 edges, and 16 vertices.  Segre intersection leaves only
five genuine divisor orbits and four edge orbits, totalling 21
all-rank plane/orientation pairs; no vertex supports a nonzero pure
slice:

- [`P5_H31_COMPONENT_FIBER_INFINITY_OBSTRUCTION.md`](claims/p5/h31/component-fiber-infinity/P5_H31_COMPONENT_FIBER_INFINITY_OBSTRUCTION.md)
- [`P4_PURE_RANK_TWO_COMPONENT_TORIC_BOUNDARY.md`](claims/p4/classifications/pair-geometry/pure-rank-two/boundaries/P4_PURE_RANK_TWO_COMPONENT_TORIC_BOUNDARY.md)
- [`P4_PURE_RANK_TWO_TORIC_SLICE_SEGRE_REDUCTION.md`](claims/p4/classifications/pair-geometry/pure-rank-two/P4_PURE_RANK_TWO_TORIC_SLICE_SEGRE_REDUCTION.md)

The 21 genuine toric plane/orientation cases now have a complete marked
incidence.  The 17 pure-direction types, both projective charts of the
first-plane fibre, every row shift, and every binary extension
direction are excluded by exact selected-minor unit ideals:

- [`P5_H31_TORIC_MARKED_FIBRE_OBSTRUCTION.md`](claims/p5/h31/toric-marked-fibre/P5_H31_TORIC_MARKED_FIBRE_OBSTRUCTION.md)

The separate nonzero divisor inside the preferred component chart,
the first-plane Schubert line at infinity, and the internal `E=0`
divisor are now closed at complete marked-fibre level:

- [`P5_H31_COMPONENT_CHART_BOUNDARY_MARKED_FIBRE_OBSTRUCTION.md`](P5_H31_COMPONENT_CHART_BOUNDARY_MARKED_FIBRE_OBSTRUCTION.md)
- [`P5_H31_COMPONENT_FIBRE_INFINITY_MARKED_FIBRE_OBSTRUCTION.md`](claims/p5/h31/component-fibre-infinity-marked-fibre/P5_H31_COMPONENT_FIBRE_INFINITY_MARKED_FIBRE_OBSTRUCTION.md)
- [`P5_H31_INTERNAL_E0_MARKED_FIBRE_OBSTRUCTION.md`](claims/p5/h31/internal-e0-marked-fibre/P5_H31_INTERNAL_E0_MARKED_FIBRE_OBSTRUCTION.md)

The complete rank-one boundary on the pure hyperplane is now excluded
as well.  A rank-one pair is a unique coordinate gate.  If the three
remaining pairs have rank two on the common source plane, their marked
`P_3` sign chart reduces binary extension to an exact four-component
projective line arrangement.  Every component either has a transverse
injective one-marked map or reaches one deepest intersection where a
forced mixed `1122` coefficient is nonzero:

- [`P5_H31_SINGLE_GATE_P3_REDUCTION.md`](claims/p5/h31/single-gate-p3/P5_H31_SINGLE_GATE_P3_REDUCTION.md)
- [`P5_H31_SINGLE_GATE_RANK_TWO_M_EXCLUSION.md`](claims/p5/h31/single-gate-rank-two-m-exclusion/P5_H31_SINGLE_GATE_RANK_TWO_M_EXCLUSION.md)

If another pair drops rank on the common plane, it becomes a unique
secondary gate.  The common-plane data is then a `P_3 -> Delta_2`
restriction.  Pair-image polarity leaves only a line/complementary-
plane stratum and a two-coordinate-plane stratum; one-marked minors and
their deepest mixed-colour coefficients exclude both:

- [`P5_H31_SECONDARY_GATE_EXCLUSION.md`](claims/p5/h31/secondary-gate-exclusion/P5_H31_SECONDARY_GATE_EXCLUSION.md)

Consequently every `H31` lift with a rank-one pair on the pure
hyperplane is impossible.  The complete marked fibre of the known
all-rank-two plane component is also excluded.  A second all-rank-two
component now exists; the complete nonzero factored slice
`A=B=F=H=1`, the complete nonzero `A=B=F=1,H=0` slice, and both
source/mode symmetry orbits are excluded.  Its generic marked fibre is
also empty by the elliptic function-field theorem, and both apparent
genus-two survivors on the deepest end-coordinate intersections are
empty, both regular end-coordinate marking divisors are closed, and
the middle-coordinate pivot complement and normalization boundary are
closed.  The outer `A B F=0` boundary is now closed as well.  A toric
stratification reduces it to four coordinate curves and one rational
conic; exact relative projections, all-extension one-marked minors,
and one stacked `5 x 5` Fitting certificate exclude every fibre:

- [`P5_H31_DIAGONAL_QUADRIC_OUTER_BOUNDARY_OBSTRUCTION.md`](P5_H31_DIAGONAL_QUADRIC_OUTER_BOUNDARY_OBSTRUCTION.md)

Thus the complete marked fibres of the first two all-rank-two
pure-compression components are empty.  Five further component orbits
are now certified and generically excluded.  The honest `H31`
remainder is the special parameter/projective boundary of the four
components not yet closed globally, together with the possible
existence of still further pure-`P_4` components.

## Geometric continuation

The remaining task is no longer an unstructured chart search.  For
`H31`, the finite marked-basis bundle and all 21 Segre-capable genuine
toric boundary orientations of the first component are closed, as are
its nonzero preferred-chart divisor, first-plane Schubert line at
infinity, and internal `E=0` divisor.  Every regular elliptic-chart
marking and the complete elliptic-normalization boundary on the second
component are closed, and the complete outer `A B F=0`
projective/gauge boundary is closed as well.  The next `H31`
compatibility problem is therefore the boundary of the three new
`1+3` components, the sixth mixed-orientation component, the new
six-dimensional component, the special boundary of the disjoint
mixed-star eighth component, and a completeness test for further
pure-compression components.  The eighth component's generic marked
fibre is now empty.  Over its irreducible function field, source
coordinates zero and one have unit genuine-neighbour projection;
coordinates two and three each leave one marking, and the same
mode-zero `0137` minor is `+/-R*A*B^2`, where
`R=f*(b*f+1)*(1-a^2*f^2)/(a^2*f+b)`:
[`P5_H31_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md`](claims/p5/h31/disjoint-mixed-star/P5_H31_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md).
The
common-smooth-quadric semisimple
case is no longer part of that completeness test: the remaining
component question is concentrated on the star/triangle exceptional
pair graphs and their block-line centers.  Within the star graph, the
directed radical orientation and one disjoint mixed orientation are
now classified; the remaining cases have other mixed kernel-edge
orientations, rank-two exceptional relations, or lower pair-image
rank.
For `H22`, it is the compatibility of one pure compression with two
marked compressions sharing target colour and three-dimensional source
data.  The generic weighted incidences on the first rank-two,
six-dimensional, mixed-orientation, and three split-cubic components
are now empty.  Their proofs combine unit binary projections,
projective-kernel covers, and one- or two-minor ternary rank
obstructions.  The diagonal-quadric component is now empty generically
as well.  Its proof identifies marked binary extension with the
intersection of an extension eight-plane and a projective Segre join;
one exact empty projective fibre and properness replace the unfinished
generic quadratic-field elimination:
[`P5_H22_DIAGONAL_QUADRIC_COMPONENT_GENERIC_OBSTRUCTION.md`](claims/p5/h22/diagonal-quadric/P5_H22_DIAGONAL_QUADRIC_COMPONENT_GENERIC_OBSTRUCTION.md).
Thus the seven previously certified component orbits are generically
closed for weighted `H22`.  A disjoint-support mixed star has since
produced an eighth component with irreducible normalized equation

```text
a^2 b f phi^2+a^2 f^2-b^2 f^2+b^2 phi^2-bf-1=0.
```

Its rank-five family tangent and rank-fifteen Segre-incidence
certificate are exact.  Its generic `H31` incidence is empty by the
function-field projection and determinantal identity above.  Its
generic weighted `H22` incidence is now empty as well: the two weighted
mixed matrices have a line and a degree-five Fitting scheme, and small
one-marked minors exclude every genuine binary direction:
[`P4_DISJOINT_MIXED_STAR_PURE_COMPONENT.md`](claims/p4/components/disjoint-mixed-star/P4_DISJOINT_MIXED_STAR_PURE_COMPONENT.md).
[`P5_H22_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md`](claims/p5/h22/disjoint-mixed-star/P5_H22_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md).
At the special slopes `r=1` and `r=-1`, a stronger binary theorem
forces respectively the first and second diagonal to vanish:
[`P5_H22_DISJOINT_MIXED_STAR_EQUAL_OPPOSITE_WEIGHT_OBSTRUCTION.md`](claims/p5/h22/disjoint-mixed-star/boundaries/P5_H22_DISJOINT_MIXED_STAR_EQUAL_OPPOSITE_WEIGHT_OBSTRUCTION.md).
Twelve generic parameter/coordinate branches and the principal coupled
slope-parameter divisor are now closed as well:
[`P5_H22_DISJOINT_MIXED_STAR_PARAMETER_PIVOT_BOUNDARY_OBSTRUCTION.md`](claims/p5/h22/disjoint-mixed-star/boundaries/P5_H22_DISJOINT_MIXED_STAR_PARAMETER_PIVOT_BOUNDARY_OBSTRUCTION.md),
[`P5_H22_DISJOINT_MIXED_STAR_COUPLED_SLOPE_BOUNDARY_OBSTRUCTION.md`](claims/p5/h22/disjoint-mixed-star/boundaries/P5_H22_DISJOINT_MIXED_STAR_COUPLED_SLOPE_BOUNDARY_OBSTRUCTION.md).
Hidden certificate denominators, other component boundaries, and
component exhaustiveness remain.

A natural non-brute-force route is:

1. classify the remaining mixed-orientation star and triangle
   exceptional-pair graphs and their lower-rank boundaries.  The
   full-support all-`1+3` nonresonant triangle is now excluded by a
   cut-label/perfect-pairing argument, and every full-support `2+2`
   bridge is excluded by an anchor/crossed-graph argument.  Thus the
   full-support nonresonant triangle is empty.  Its one-edge boundary
   forces product rank one, and its two-edge boundary suspends a pure
   `P_3` and forces pair rank at most two.  Hence the complete
   nonresonant triangle is empty; only the resonant holonomy divisor
   remains.  That divisor is now split by its additive affine
   holonomy: a nonzero class gives a tangent-Segre first jet plus a
   cyclic cut system, and the zero class gives a compressed binary
   cubic `Sym^3(C^2) -> R_3`.
   In parallel, close the boundaries of the three new `1+3`
   components, the sixth component, and the six-dimensional component;
2. intersect the resulting classification with the all-rank-two and
   alternating-gate normal forms of the marked `Delta_2` slice, using
   the weighted survivor/kernel equations as a generic model and the
   equal-weight theorem as one boundary certificate; and
3. use the second marked slice in `H22` as a compatibility condition,
   not as another independent case enumeration.

This is a smaller and more geometric problem than the previous
high-coordinate chart CEGAR.  The rank-one part, the entire finite
marked fibre of the known family, and the 21 genuine toric plane cases
are closed; the nonzero preferred-chart divisor, first-plane Schubert
boundary, and internal `E=0` divisor are closed as well.  The first
component is generically closed for weighted `H22`, and the second
component is now closed in full for `H31`.  The three new `1+3` components are
generically closed but retain special parameter/projective
boundaries; they are now generically closed for both `H31` and
weighted `H22`.  The sixth mixed-orientation component and the
six-dimensional component are also generically closed but retain
their parameter/projective boundaries; both are likewise generically
closed for `H31` and weighted `H22`.  The common smooth
diagonal-quadric locus cannot supply a new component away from its
block boundaries.  The embedded pure-`P_3` suspension raised the
component lower bound to nine.  A later two-rank-two-spoke mixed-star
component has raised the current lower bound to ten; its marked fibres are
not analyzed here.  The embedded component's generic marked `H31` fibre is
now empty already at binary level: the source-zero extension is an
apolar insertion map whose generic projected-line kernels all kill
one required diagonal.  Restoring the weighted slope closes its
generic `H22` fibre as well: one diagonal direction is structurally
zero and the other is the same insertion arrangement on a
slope-dependent line.  Its full normalized affine `H31` chart is
closed, including all nine exceptional insertion points.  Its weighted
boundary is closed whenever that projected image remains a line, and
the rank-one collapse `rS=1,T=rU` is now excluded by the complementary
marked contraction.  Thus the ninth component's entire normalized
weighted `H22` chart is empty.  The support-two normalization divisor
`A=0`, `B!=0` is now closed for `H31` by a singular insertion-pencil
argument; its sole resonance has fixed third-contraction coefficient
`4`.  The complementary `r=0`, `A B!=0` divisor is closed by signed
source transport and a tangent--Segre Fitting stratification.  Hence
the whole affine `B!=0` ninth-component chart is empty for `H31`.
The homogeneous sign-rectangle compactification is now closed by
support: coordinate points have zero restriction and every other
point enters the affine chart by symmetry.  Thus the ninth component
is closed in full for `H31`.  Exhaustiveness of those nine orbits and
the special component/slope boundary incidences in `H22` remain
unresolved.

## Verification

Run:

```text
python verify_p5_high_coordinate_partial_frontier.py
python audit_p5_high_coordinate_partial_frontier.py
```

The primary verifier derives the labelled census combinatorially,
checks the normal-form ranks and the contraction factorizations, and
pins the exact exclusion theorems.  The independent audit rebuilds the
covered 6,495-signature catalogue using its separate implementation
and reproduces every row of the census.  The catalogue is used only to
audit completeness of the local support split; the tensor identities
and the reduction are over `C`.
