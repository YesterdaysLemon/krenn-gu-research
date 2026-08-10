# Full admissible local-potential cone lemma

## Status

This is an arbitrary-order strengthening of
`SIX_PERMUTED_POTENTIALS_LEMMA.md`.  It applies in the same simultaneous
balanced all-bridge, pairwise-disjoint exact-cubic diagonal branch.  It
determines every additive local potential that is neutral on forced
diagonal units and positive on all permitted optional diagonal units.
It does not by itself prove the Krenn--Gu conjecture.

The local cone theorem remains valid.  Its earlier order-twelve
port-residual application is withdrawn because that finite pipeline
confused target-task labels with physical half-colours.  The corrected
physical ports are all strictly positive under the original base
potential, and the complete pairwise-disjoint exact-degree-six branch is
now excluded by the simpler arbitrary-order argument in
`ARBITRARY_ORDER_DEGREE_SIX_KOTZIG_PORT_OBSTRUCTION.md`.  The cone can
still be useful for higher-support continuations.

## Local potential space

There are 24 local states `(f,c)`, where `f` is one of the eight normal
types and `c` is one of three local colours.  Write a potential as

```text
p(f,c) in R.
```

For every oriented saturated own-colour diagonal transition
`(c,f,g)`, impose

```text
p(f,c) + p(g,c) = 0.                                  (1)
```

There are 48 oriented transitions.  Their exact integer constraint
matrix has rank 18, so the solution space of (1) has dimension six.
The six colour-permuted potentials in
`SIX_PERMUTED_POTENTIALS_LEMMA.md` are linearly independent and satisfy
(1).  They are therefore a basis of the complete neutral potential
space, not merely six examples.

Let

```text
lambda = (lambda_0,...,lambda_5)
```

be coordinates in that permuted-potential basis.  The 42 permitted
optional off-diagonal transitions give only nine distinct strict
inequalities

```text
w lambda > 0.                                         (2)
```

Their coefficient rows, with multiplicities suppressed, are

```text
(1,1,1,2,3,2)   (1,1,2,1,2,3)   (1,3,1,2,1,2)
(2,2,1,3,1,1)   (2,2,3,1,1,1)   (3,1,2,1,2,1)
(3,3,3,4,3,4)   (3,3,4,3,4,3)   (4,4,3,3,3,3).
```

## Complete cone theorem

The closure of the admissible cone is simplicial.  In the
`lambda`-coordinates above, its six extreme rays are

```text
r0 = (-4, 1, 1, 1, 6,-4)
r1 = (-4, 1, 6, 1, 1,-4)
r2 = ( 1,-4, 1, 1,-4, 6)
r3 = ( 1,-4, 1, 6,-4, 1)
r4 = ( 1, 6,-4,-4, 1, 1)
r5 = ( 6, 1,-4,-4, 1, 1).                             (3)
```

These directions have a much simpler form than their coordinates
suggest.  Put `s_i=(-1)^b_i`.  After dividing all local values by five,
the six extreme potentials on colours `(0,1,2)` are

```text
r0: ( s1,  s2, -s1)
r1: ( s1, -s0, -s1)
r2: ( s2, -s2,  s1)
r3: ( s2, -s2,  s0)
r4: (-s2,  s0, -s0)
r5: (-s1,  s0, -s0).                                  (4)
```

Thus every extreme direction is a Boolean `+5/-5` grading.  A forced
own-colour diagonal edge always joins opposite signs.  A permitted
optional transition has endpoint sum either zero or ten, never negative.
This Boolean form is useful when seeking an arbitrary-order combinatorial
interpretation of the cone.

Thus every neutral potential nonnegative on all optional transitions
has a unique expression

```text
lambda = mu_0 r0 + ... + mu_5 r5,  mu_i >= 0.          (5)
```

It is strictly positive on every optional transition exactly when

```text
mu_i > 0 for all i.                                   (6)
```

In particular, negative coefficients in the original six-potential
basis are not only possible but necessary near every extreme direction.
The earlier nonnegative `lambda` orthant is a proper subcone of the full
admissible cone.

## Exact cone certificate

Let `R` be the matrix whose columns are the six rays in (3), and let `W`
be the nine-row inequality matrix above.  Exact integer multiplication
has two decisive properties:

1. every entry of `W R` is nonnegative;
2. among its nine rows are the six rows

```text
10 e0, 10 e1, ..., 10 e5.
```

The matrix `R` has rank six.  Hence any `lambda` can be written uniquely
as `R mu`.  If `W lambda >= 0`, the six coordinate rows force
`mu_i >= 0`; conversely nonnegative `mu` makes every row of `W R mu`
nonnegative.  This proves (5).  The same coordinate rows, together with
nonnegativity of all other rows, prove the strict statement (6).

The rays also satisfy

```text
r0 + r1 + r2 + r3 + r4 + r5 = (1,1,1,1,1,1).          (7)
```

The right side is an interior admissible direction.  Therefore each
boundary ray has a valid lexicographic refinement: minimize `r_i` first,
then the interior direction in (7).  On any finite architecture this is
realized by

```text
M r_i + (1,1,1,1,1,1)
```

for a sufficiently large positive integer `M`.  Optional transitions
with zero `r_i`-weight remain strictly positive because of the second
term.

## Consequence for minimum layers

Every argument in the original potential lemma used only:

1. zero weight on each forced own-colour diagonal unit;
2. strict positive weight on each optional diagonal unit; and
3. finiteness of the matching expansion.

It therefore applies to every interior point of the complete cone.
A hypothetical witness in this branch must avoid a unique guaranteed
matching on every full-cone-exposed minimum colouring, including each of
the six extreme-ray/interior lexicographic refinements above.

## Verification

Run

```text
python claims/arbitrary-order/verify_full_admissible_potential_cone.py
python claims/arbitrary-order/audit_full_admissible_potential_cone.py
```

The verifier reconstructs the 24 local states, all 48 saturated
transitions, all 42 optional transitions, both exact ranks, the nine
inequality rows, and the `W R` cone certificate using integer and
rational arithmetic.  The audit independently enumerates all
five-facet intersections with exact symbolic nullspaces and regenerates
the same six extreme rays.  Their outputs are

```text
tmp/full_admissible_potential_cone_verified.json
tmp/full_admissible_potential_cone_audited.json
```

The theorem is arbitrary-order, but it remains conditional on reaching
the pairwise-disjoint exact-cubic diagonal normal form.  The
overlapping-matching and other global branches are not resolved here.
