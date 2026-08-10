# A ninth pure `P_4` component from an embedded pure `P_3`

## Status

This is an exact characteristic-zero component theorem.

The locus of four two-planes on which the order-four permanent
restricts to a nonzero pure tensor has a generically smooth,
rational, six-dimensional irreducible component obtained by embedding
a pure `P_3` restriction in one source-coordinate hyperplane and
letting the remaining mode supply the missing coordinate.

Its generic pair-image profile is

```text
(r_01,r_02,r_03,r_12,r_13,r_23)
  =(4,4,4,2,2,2).                                  (1)
```

This profile and the component dimension separate it from all eight
previously certified symmetry orbits.  Consequently the repository's
certified lower bound is now

```text
at least nine symmetry-inequivalent pure-P_4 components.             (2)
```

A later two-rank-two-spoke mixed-star component has raised the current
repository-wide lower bound to ten in
[`P4_TWO_RANK_TWO_SPOKE_MIXED_STAR_COMPONENT.md`](../../classifications/star/two-rank-two-spoke-mixed-star-component/P4_TWO_RANK_TWO_SPOKE_MIXED_STAR_COMPONENT.md).

The theorem is at the pure-`P_4` plane level.  A later apolar
insertion theorem excludes its generic marked `H31` fibre:
[`P5_H31_EMBEDDED_P3_COMPONENT_GENERIC_OBSTRUCTION.md`](../../../p5/h31/embedded-p3/P5_H31_EMBEDDED_P3_COMPONENT_GENERIC_OBSTRUCTION.md).
The same insertion arrangement, after restoring the source-torus
slope, excludes its generic weighted `H22` fibre:
[`P5_H22_EMBEDDED_P3_COMPONENT_GENERIC_OBSTRUCTION.md`](../../../p5/h22/embedded-p3/P5_H22_EMBEDDED_P3_COMPONENT_GENERIC_OBSTRUCTION.md).
Its entire rank-two projected-line weighted boundary is excluded by
six symbolic one-marked factor covers:
[`P5_H22_EMBEDDED_P3_COMPONENT_RANK_TWO_LINE_BOUNDARY_OBSTRUCTION.md`](../../../p5/h22/embedded-p3/P5_H22_EMBEDDED_P3_COMPONENT_RANK_TWO_LINE_BOUNDARY_OBSTRUCTION.md).
The rank-one collapse is excluded by the complementary insertion
pencil:
[`P5_H22_EMBEDDED_P3_COMPONENT_RANK_ONE_COLLAPSE_OBSTRUCTION.md`](../../../p5/h22/embedded-p3/P5_H22_EMBEDDED_P3_COMPONENT_RANK_ONE_COLLAPSE_OBSTRUCTION.md).
The component theorem itself does not classify the full
pure-compression locus, analyze the remaining normalization and
projective boundaries,
produce a graph satisfying the Krenn--Gu prize conditions, or prove
the global conjecture.

## The symbolic family

Work in the squarefree Frobenius algebra

```text
R=C[X_0,X_1,X_2,X_3]/(X_0^2,X_1^2,X_2^2,X_3^2).
```

Take parameters

```text
r,s,t,u,A in C,       B in C^*,
```

and the four row planes

```text
U_0=span(
 (1,0,r,t),
 (0,1,s,u)),

U_1=span(
 (0,1,0,-1/B),
 (0,0,1,-A/B)),

U_2=span(
 (0,1,0, 1/B),
 (0,0,1,-A/B)),

U_3=span(
 (0,1,0,-1/B),
 (0,0,1, A/B)).                                   (3)
```

These lie in the Grassmann charts with pivots

```text
(01),(12),(12),(12).                               (4)
```

Let `T_abcd` be the restricted permanent coefficient obtained by
choosing the displayed row indexed by `a,b,c,d`.  Direct multilinear
expansion gives

```text
T_0010=-2/B,
T_0110=-2A/B,                                      (5)
```

and every other coefficient is zero.  Therefore

```text
P_4 restricted to U_0 tensor U_1 tensor U_2 tensor U_3
 =(-2/B) e_0 tensor (e_0+A e_1) tensor e_1 tensor e_0,  (6)
```

in the four displayed binary row bases.  It is nonzero for every
parameter point in (3).

## Why this is an embedded `P_3`, not an accidental cancellation

The last three planes in (3) lie in the source-coordinate hyperplane

```text
H_0={z_0=0}.
```

Before row reduction, they are the three planes in `C^3` with bases

```text
(-A,1,0), (-B,0,1);
( A,1,0), ( B,0,1);
( A,1,0), (-B,0,1).                                (7)
```

Their normals are

```text
(1, A, B),       (1,-A,-B),       (1,-A, B),       (8)
```

which is one of the six sign charts in
[`P3_DECOMPOSABLE_RESTRICTION_CLASSIFICATION.md`](../../../../P3_DECOMPOSABLE_RESTRICTION_CLASSIFICATION.md).
The restricted `P_3` has only

```text
T_100= 2A,       T_101=-2B.                        (9)
```

Since all three rows omit source coordinate zero, every surviving
`P_4` matching assigns coordinate zero to mode zero.  Thus

```text
P_4(z,-,-,-)=z_0 P_3(-,-,-),                       (10)
```

which proves (5)--(6) conceptually.  The four parameters of `U_0`
are completely free because only the restriction of the coordinate
functional `z_0` to that plane matters.

This is the promised translation across a mathematical fence:
component construction for `P_4` becomes the already classified pure
restriction problem for `P_3`, followed by a one-coordinate
suspension.

## The family has dimension six

The parameter space

```text
C^4 x C x C^*
```

is irreducible of dimension six.  The four parameters `r,s,t,u` are
the four affine coordinates of `U_0` in its chart.  The entries

```text
-1/B,       -A/B
```

in `U_1` recover `B,A` rationally.  Hence (3) is generically
injective and its image closure is an irreducible six-dimensional
subvariety.

Equivalently, with chart coordinates ordered by row and then by
nonpivot column, chart rows

```text
(0,1,2,3,5,7)
```

form a six-by-six parameter-Jacobian minor with determinant

```text
-1/B^3
```

and hence never vanish.

## Exact local component certificate

Use the rational point

```text
(r,s,t,u,A,B)=(3/2,1/2,1,2,2,3).                  (11)
```

In the charts (4), adjoin a target Segre point.  Use tensor anchor

```text
alpha=0010,       T_alpha=-2/3,
```

and factor ratios

```text
(z_0,z_1,z_2,z_3)=(0,2,0,0).                      (12)
```

For every binary word `w!=alpha`, the standard affine
Segre-incidence equation is

```text
T_w-T_alpha product_(i:w_i!=alpha_i) z_i=0.        (13)
```

Order the sixteen plane-chart variables mode by mode and, inside each
mode, by row and then by nonpivot column.  Append
`z_0,z_1,z_2,z_3` as columns `16,17,18,19`.  Order the fifteen
equations lexicographically by `w!=0010`.

At (11)--(12), rows

```text
0,1,...,13
```

and columns

```text
(4,5,6,7,8,9,10,11,12,13,14,16,18,19)             (14)
```

form a `14 x 14` Jacobian minor with determinant

```text
114688/2187.                                       (15)
```

Hence the incidence tangent space has dimension at most

```text
20-14=6.
```

The six-dimensional family (3) passes through the point, so the local
dimension and tangent dimension are both exactly six.  The point is
smooth and lies on a unique local irreducible component.  The
irreducible family closure must be that component.

A nonzero pure tensor has a unique projective Segre factor point.
Therefore forgetting the four target ratios is locally an
isomorphism, and the same component statement holds in
`Gr(2,4)^4`.

## Generic pair geometry and distinctness

At (11), exact multiplication in `R_2` gives (1).  For pairs involving
`U_0`, the domain has dimension four, so the sample rank four is
generic by openness.

For pairs among `U_1,U_2,U_3`, work in the three-coordinate
squarefree algebra.  Its degree-two/degree-one multiplication pairing
is perfect between two three-dimensional spaces.  The restricted
`P_3` tensor has flattening rank one and the opposite plane has
dimension two.  The same subspace-pairing inequality used elsewhere
in the repository gives

```text
dim(U_i U_j)+2-3 <= 1,
```

so every such pair image has dimension at most two.  The sample rank
two is therefore generic.  This proves (1).

The multiset of pair-image ranks is

```text
{2,2,2,4,4,4}.                                     (16)
```

It is invariant under mode permutations, source-coordinate
permutations and diagonal rescalings, and changes of basis inside the
local planes.

Seven of the previously certified component orbits are
five-dimensional, so dimension already separates them.  The only
previously certified six-dimensional component has generic profile

```text
(4,3,2,4,4,3),
```

whose rank multiset is `{2,3,3,4,4,4}`.  It differs from (16).
Thus the component (3) is not symmetry-equivalent to any of the
previous eight.

## Relation to the triangle cut reduction

The family was exposed by the cut-catalecticant analysis in
[`P4_NONRESONANT_RANK_TWO_TRIANGLE_CUT_REDUCTION.md`](../../classifications/rank-two-triangle/nonresonant/cut-reduction/P4_NONRESONANT_RANK_TWO_TRIANGLE_CUT_REDUCTION.md).
A common `1+3` cut forces three local planes into one coordinate
hyperplane.  Instead of contributing a rank-three exceptional
triangle, the pair images drop to rank two and the problem becomes
the pure `P_3` classification.  Following that boundary, rather than
discarding it as degenerate, produces the component above.

The compatible-label implication is now a theorem rather than only
the construction heuristic:
[`P4_NONRESONANT_ONE_THREE_TRIANGLE_OBSTRUCTION.md`](../../boundaries/rank-two-triangle/nonresonant/one-three/P4_NONRESONANT_ONE_THREE_TRIANGLE_OBSTRUCTION.md).
For three full-support `1+3` bridges, the factorization dichotomy
forces all singleton labels to coincide; the perfect degree
`2`/degree `1` pairing in the resulting three-variable algebra then
forces the pair-rank drop.

This also sharpens the remaining classification frontier.  Any claim
that the earlier eight components were exhaustive would miss a
structurally forced suspension component.

## Verification

Run

```text
uv run --with sympy python claims/p4/components/embedded-p3/verify_p4_embedded_p3_pure_component.py
python claims/p4/components/embedded-p3/audit_p4_embedded_p3_pure_component.py
```

The primary verifier expands all sixteen coefficients symbolically,
checks the family tangent, reconstructs the exact incidence minor
(15), and verifies the pair profile.  The independent audit uses a
dynamic-programming permanent and modular dual numbers at two primes;
it is a one-point certificate replay, not a search.

The generic marked `H31` fibre has since been excluded without a
large elimination.  Deleting source coordinate zero turns extensions
into the first variation of the pure `P_3` multiplication tensor.  Its
six-column Fitting support is three signed projective lines plus three
coordinate points, and every generic line kernel kills the required
all-alpha diagonal:

```text
P5_H31_EMBEDDED_P3_COMPONENT_GENERIC_OBSTRUCTION.md
verify_p5_h31_embedded_p3_component_generic_obstruction.py
audit_p5_h31_embedded_p3_component_generic_obstruction.py
```

The nine exceptional insertion points are now closed as well.  Five
binary survivor families remain after exact truncated-Segre
classification; small one-marked covers exclude four, and the deepest
rank-three point has stacked pure/neighbour determinant `8`:

```text
P5_H31_EMBEDDED_P3_COMPONENT_NORMALIZED_BOUNDARY_OBSTRUCTION.md
verify_p5_h31_embedded_p3_component_normalized_boundary.py
audit_p5_h31_embedded_p3_component_normalized_boundary.py
```

The normalization divisor `A=0`, `B!=0` is now closed for `H31` too.
Here the pure `P_3` sign chart degenerates from support three to
support two.  Its insertion presentation is a singular matrix pencil:
one Fitting factor forces `rho=-Cp`, generic points are killed by a
one-marked determinant, and the sole resonant coordinate fibre
`C=-1` is closed by three factored covers, a stacked determinant, and
a fixed third-contraction coefficient `4`:

```text
P5_H31_EMBEDDED_P3_COMPONENT_SUPPORT_TWO_BOUNDARY_OBSTRUCTION.md
verify_p5_h31_embedded_p3_component_support_two_boundary.py
audit_p5_h31_embedded_p3_component_support_two_boundary.py
```

The generic weighted `H22` fibre is empty at binary level as well.
One weighted direction retains source coordinate zero and therefore
has an identically zero all-alpha diagonal.  The other is the same
insertion arrangement on the slope-dependent projected mode-zero
line:

```text
P5_H22_EMBEDDED_P3_COMPONENT_GENERIC_OBSTRUCTION.md
verify_p5_h22_embedded_p3_component_generic_obstruction.py
audit_p5_h22_embedded_p3_component_generic_obstruction.py
```

The weighted boundary on which the projected mode-zero image remains
a line is now closed as well.  The arrangement intersection has four
strata and six marked binary survivor families; exact one-marked
factor covers exclude all six, including two deepest points with
stacked determinants `8` and `-8`:

```text
P5_H22_EMBEDDED_P3_COMPONENT_RANK_TWO_LINE_BOUNDARY_OBSTRUCTION.md
verify_p5_h22_embedded_p3_component_rank_two_line_boundary.py
audit_p5_h22_embedded_p3_component_rank_two_line_boundary.py
```

At the remaining rank-one projected-image collapse `rS=1,T=rU`, the
other required marked slice gives a complementary `7 x 6` insertion
pencil.  It is injective away from `S=+/-1`; the two exceptional
kernels kill one of the required nonzero diagonals:

```text
P5_H22_EMBEDDED_P3_COMPONENT_RANK_ONE_COLLAPSE_OBSTRUCTION.md
verify_p5_h22_embedded_p3_component_rank_one_collapse.py
audit_p5_h22_embedded_p3_component_rank_one_collapse.py
```

Thus the full normalized affine weighted `H22` chart is empty.  For
`H31`, the support-two divisor above is closed as well.  The remaining
`r=0`, `A B!=0` divisor is now closed by a signed-coordinate transport
and tangent--Segre insertion theorem:

```text
P5_H31_EMBEDDED_P3_COMPONENT_R_ZERO_BOUNDARY_OBSTRUCTION.md
verify_p5_h31_embedded_p3_component_r_zero_boundary.py
audit_p5_h31_embedded_p3_component_r_zero_boundary.py
```

Consequently the whole affine family (3), where `B!=0`, is empty for
`H31`.  The projective compactification is now closed intrinsically
as well: its homogeneous sign-rectangle base is `[C:A:B]`; support-one
points have zero pure restriction, and every other point enters a
`C'B'!=0` affine chart by source symmetry:

```text
P5_H31_EMBEDDED_P3_COMPONENT_PROJECTIVE_CLOSURE_OBSTRUCTION.md
verify_p5_h31_embedded_p3_component_projective_closure.py
audit_p5_h31_embedded_p3_component_projective_closure.py
```

Thus this component's complete marked `H31` fibre is empty.
