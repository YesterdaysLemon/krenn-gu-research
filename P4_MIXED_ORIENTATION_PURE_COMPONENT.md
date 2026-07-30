# A sixth pure `P_4` component from a mixed zero-product orientation

## Status

This is an exact algebraic-geometric component theorem over `C`.

The all-rank-two locus on which `P_4` restricts to a nonzero
decomposable tensor has at least six symmetry-inequivalent irreducible
components.  The new component has dimension five and is generically
smooth.  It is distinguished from the five previously certified
components by the directed pure-kernel orientation of its rank-one
pair-product relations.

This is a lower bound, not a classification.  The generic marked
`H31` fibre has since been excluded in
[`P5_H31_MIXED_ORIENTATION_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H31_MIXED_ORIENTATION_COMPONENT_GENERIC_OBSTRUCTION.md);
the generic weighted `H22` incidence has since been excluded in
[`P5_H22_MIXED_ORIENTATION_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H22_MIXED_ORIENTATION_COMPONENT_GENERIC_OBSTRUCTION.md).
Its special parameter/projective boundary remains.  Nothing here
settles all of `H22` or the global prize problem.

## Mixed coordinate-pair zero products

Use active/kernel row order in modes one through three and normalize
two rank-one exceptional relations to

```text
x_1=(0,0,1,1),        y_1=(a,1,c,d),
x_2=(p,1,0,q),        y_2=(-1,0,1,0),
x_3=(1,0,1,0),        y_3=(0,0,-1,1).              (1)
```

The fixed zero products are

```text
x_1 y_3=0,       y_2 x_3=0                         (2)
```

in

```text
R=C[X_0,X_1,X_2,X_3]/(X_0^2,X_1^2,X_2^2,X_3^2).
```

The first relation in (2) points toward the common mode three, while
the second points away from it.  This mixed orientation is not the
double-contraction radical orientation classified in
[`P4_RADICAL_STAR_COMPONENT_CLASSIFICATION.md`](P4_RADICAL_STAR_COMPONENT_CLASSIFICATION.md).

For every nonzero word in the three kernel bits of modes one, two, and
three, contract `P_4` to a covector on mode zero.  Four of the seven
covectors vanish identically because of (2).  Let `C(a,c,d,p,q)` be
the `3 x 4` matrix of the remaining covectors.  A mode-zero plane on
which all kernel-containing coefficients vanish exists exactly when

```text
rank C <= 2.                                        (3)
```

The exact radical of the four `3 x 3` minors of `C` has five linear
minimal primes:

```text
P_1=(c+p+q, a+d),
P_2=(d+q, a+c+p),
P_3=(c, a+d+p+q),
P_4=(c-d+p-q, a),
P_5=(c-d, a+p-q).                                  (4)
```

This small determinantal decomposition replaces a search through
sixteen plane coordinates.

## The new family

Take `P_1` in (4), so

```text
a=-d,       c=-p-q,
N=q(d+p+q).                                        (5)
```

Define

```text
U_0=span(
 (-dp, d+q, N,0),
 ( dp,-d-q, 0,N)),

U_1=span(
 (0,0,1,1),
 (-d,1,-p-q,d)),

U_2=span(
 (p,1,0,q),
 (-1,0,1,0)),

U_3=span(
 (1,0,1,0),
 (0,0,-1,1)).                                     (6)
```

Direct permanent expansion gives the single nonzero coefficient

```text
T_0000=2q(d+p+q)=2N.                               (7)
```

Thus (6) is a nonzero pure restriction whenever `N != 0` and the four
planes have rank two.

All three exceptional edges form the star

```text
03, 13, 23,
```

and all three one-dimensional multiplication kernels have rank-one
coefficient matrices.  At a generic point,

```text
(r_01,r_02,r_03,r_12,r_13,r_23)
  =(4,4,3,4,3,3).                                  (8)
```

The component has one generic `1+3` diagonal-quadric jump line, so its
coarser jump signature is `(0,1)`.  That signature is shared with the
previous `L_3` component and is therefore not sufficient for
classification.

## Dimension and smoothness

Apply the projective diagonal source torus

```text
diag(t_0,t_1,t_2,1)
```

to all four planes in (6).  Use Grassmann pivots

```text
(02),(02),(01),(02).                               (9)
```

At

```text
(d,p,q,t_0,t_1,t_2)=(1,2,3,1,1,1),
```

the Jacobian of the sixteen chart coordinates has rank five.  Its
rows `(0,1,3,4,5)` and parameter columns
`(d,p,q,t_0,t_2)` form a minor with determinant

```text
-9/2.                                              (10)
```

In the Segre-incidence chart, use tensor anchor `1010`.  The target
ratios are

```text
(z_0,z_1,z_2,z_3)=(0,-1/5,0,0).                    (11)
```

The fifteen incidence equations have Jacobian rank fifteen in twenty
variables.  In the order consisting of the sixteen plane-chart
variables followed by the four target ratios, columns

```text
(0,1,2,3,4,5,6,7,8,9,12,14,16,18,19)
```

form a square minor of determinant

```text
-737280.                                           (12)
```

Hence the incidence locus is smooth of dimension five at the sample.
The irreducible family (5)--(6) already has dimension five by (10), so
its closure is the unique local irreducible component.  A nonzero
decomposable tensor has unique projective factors, making the
incidence projection locally an isomorphism to the plane locus.

## A finer symmetry invariant

For a rank-three pair image, write its unique multiplication relation
in active/kernel bases.  If the relation matrix has rank one, its
zero active-active entry forces at least one factor to be the pure
kernel line at an endpoint.  Direct each relation toward every such
kernel endpoint and record the four indegrees.

At a generic point of the new component:

```text
number of rank-one exceptional edges = 3,
sorted kernel-endpoint indegrees      = (2,1,0,0).  (13)
```

For the first and second known components, only two exceptional
relations have rank one; the third has rank two.  For each of
`L_1,L_2,L_3`, all three relations have rank one but the sorted
indegrees are

```text
(1,1,1,0).                                         (14)
```

Relation-matrix rank and the pure kernel lines are intrinsic to the
plane tuple and its unique nonzero pure tensor.  The data (13)--(14)
are preserved by source-coordinate permutations, diagonal source
rescaling, and mode permutations.  Therefore the component (6) is
inequivalent to all five previously certified component orbits.

The prime `P_3` in (4) gives a symmetry translate of the same orbit.
Indeed swapping modes zero and one sends `P_1(d,p,q)` birationally to
`P_3(d',p,q)`, where

```text
d'=-q(d+p+q)/(d+q).                                (15)
```

All remaining primes in (4) have since been identified in
[`P4_MIXED_DETERMINANTAL_PRIME_CLASSIFICATION.md`](P4_MIXED_DETERMINANTAL_PRIME_CLASSIFICATION.md).
The prime `(d+q,a+c+p)` is a proper subfamily of the six-dimensional
component, while the last two primes are symmetry charts of `L_2` and
`L_1`.

## Consequences for `H31` and `H22`

The generic marked fibre of (6) is empty by exact function-field
projection and all-extension determinant identities.  Its parameter
and projective boundaries remain.  The lower-rank prime noted above
also opens into a seventh, six-dimensional component; its generic
marked fibre is empty as well.  Thus `H31` still requires the
incomplete component boundaries and a proof that no further pure
components exist.

The two generic weighted diagonal pencils required by `H22` are also
closed.  The `01` mixed matrix has full column rank for every marking;
the `23` binary survivor locus is covered by three marking closures,
each excluded by a two-minor rank-four obstruction.  Parameter/slope
divisors, the component's projective boundary, and the other
components' `H22` incidences remain open.

## Verification

Run:

```text
tmp/codex_verify_env/Scripts/python.exe \
  verify_p4_mixed_orientation_pure_component.py

python audit_p4_mixed_orientation_pure_component.py
```

The primary verifier reconstructs the contraction matrix and the five
minimal primes (4), expands every permanent in (6), verifies the
pair-relation and directed-kernel invariants, proves the birational
mode-swap identity (15), and checks the exact family and incidence
minors (10)--(12).

The independent audit imports nothing from the primary verifier.  It
uses modular dual numbers, a dynamic-programming permanent, and
independent row reduction at `101,103` to replay the family tangent,
incidence Jacobian, pair profile, jump signature, and directed
rank-one relations.  These modular calculations are corroboration;
the displayed rational identities and exact smooth-point argument
prove the theorem over `C`.
