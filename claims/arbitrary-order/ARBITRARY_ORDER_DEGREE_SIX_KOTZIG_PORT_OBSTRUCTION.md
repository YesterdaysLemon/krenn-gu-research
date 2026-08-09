# Arbitrary-order degree-six Kotzig/port obstruction

## Status

This is an arbitrary-order exclusion theorem.  For every even `n >= 6`,
there is no Krenn--Gu witness in the simultaneous balanced all-bridge
branch whose three selected monochromatic matchings are pairwise
edge-disjoint and whose essential support skeleton is exactly 6-regular.

It replaces the earlier order-eight, order-ten, and order-twelve finite
Kotzig/port exclusions.  It does not address overlapping selected
matchings, support degree at least seven, or the separate deeper-blocker
branch, so it is not a proof of the global conjecture.

## Correct exact-degree-six normal form

Use the eight normal types

```text
f(c) in {0,1,2} minus {c}.
```

The pairwise-disjoint cubic diagonal theorem gives three perfect matchings

```text
M_0, M_1, M_2
```

whose union `D` is a properly three-edge-coloured cubic graph.  Every
pairwise union is Hamiltonian.  An edge of `M_c` has a forced nonzero
unit `(c,c)` and at most one optional off-diagonal unit.

At exact support degree six, the three remaining incident support edges
at each vertex are its three distinct primary killers.  They form a cubic
physical graph `K`.  Pair the target-`c` killer task at `u` with the
target-`r` task at `v`, where

```text
r = f_u(c),  f_v(r)=c.
```

The physical singleton on the oriented edge `uv` is

```text
(r,c),                                                   (1)
```

not `(c,r)`.  It must also survive the full balanced-bridge table.  This
target/half-colour distinction is proved and audited separately in
`RECIPROCAL_PORT_ORIENTATION_CORRECTION.md`.

## Positive physical-port potential

For a normal type with bits

```text
b0 = 0 for f(0)=1,  b0 = 1 for f(0)=2,
b1 = 0 for f(1)=0,  b1 = 1 for f(1)=2,
b2 = 0 for f(2)=0,  b2 = 1 for f(2)=1,
```

put

```text
q(0) = 1 - 2 b2,
q(1) = 2 (b2 - b0),
q(2) = 2 (b0 + b1 - 1).                                (2)
```

The earlier diagonal table gives:

```text
q_u(c)+q_v(c) = 0
```

on every forced own-colour `D` unit, and strictly positive total potential
on every permitted optional off-diagonal `D` unit.

The corrected physical-port table has the same strict sign.  Across all
eight ordered normal types, every target colour, and every reciprocal
partner:

1. there are 96 reciprocal target-task transitions;
2. exactly 72 have a physical unit (1) permitted by the balanced-bridge
   table; and
3. on those 72 units,

```text
q_u(r)+q_v(c) > 0.
```

The exact value histogram is

```text
potential 1: 24 transitions
potential 2: 16 transitions
potential 3: 24 transitions
potential 4:  8 transitions.                            (3)
```

The same positivity holds for every global colour permutation of `q`.
Only one direction is needed below.

## Arbitrary-order contradiction

Regard `D` as an ordinary monochromatically edge-coloured graph, giving
every edge of `M_c` colour `c`.  It has a monochromatic perfect matching
in each of three colours.  Since `n>4`, Bogdanov's matching theorem
(reported as Theorem 1.7 by Chandran--Gajjala--Illickan) implies that
`D` also has a nonmonochromatic perfect matching `F`.

Use on every edge of `F` its forced own-colour diagonal unit, and let
`chi` be the inherited vertex colouring.  Every edge of `F` has potential
zero, so

```text
sum_v q_v(chi(v)) = 0.                                  (4)
```

Now consider any supported perfect-matching monomial inducing the same
colouring `chi`.  Its edge units partition the same vertex states, so
their total potential is also the left side of (4).  Every possible unit
in the exact-degree-six normal form has nonnegative potential:

- forced own-colour `D` units have value zero;
- optional `D` units have positive value; and
- corrected physical `K` units have positive value by (3).

Therefore a monomial inducing `chi` cannot use an optional `D` unit or a
`K` unit.  It must use only forced own-colour edges of `D`.

Such a matching is unique.  At a vertex coloured `c`, the proper
three-edge-colouring of `D` supplies exactly one incident forced edge
whose local colour is `c`, namely its `M_c` edge.  Thus `chi` determines
`F` edge by edge.

All forced units are nonzero, so the coefficient of the nonmonochromatic
colouring `chi` is the single nonzero monomial

```text
product_(e in F) W_e[colour(e),colour(e)].
```

The Krenn--Gu target requires that coefficient to be zero, a
contradiction.

## Verification

Run:

```text
python verify_arbitrary_order_degree_six_kotzig_port_obstruction.py
python audit_arbitrary_order_degree_six_kotzig_port_obstruction.py
```

The first verifier reconstructs the 48 saturated diagonal transitions,
the permitted optional-diagonal table, all 96 reciprocal target-task
transitions, the 72 admissible physical ports, and histogram (3).  The
second implementation builds the normal types from bits in a different
order and tests the six coordinate-plane restrictions directly.

The matching-existence input is a published arbitrary-order theorem, not
a finite computation:

```text
Bogdanov's theorem, reported as Theorem 1.7 in
L. Sunil Chandran, Rishikesh Gajjala, Abraham M. Illickan,
Krenn-Gu conjecture for sparse graphs, arXiv:2407.00303:
three differently coloured monochromatic perfect matchings on more than
four vertices force a nonmonochromatic perfect matching.
```

The local programs verify the new sign lemma and convention on which the
argument depends.

## Boundary

The theorem removes the complete pairwise-disjoint exact-degree-six
branch at every even order.  The next diagonal-degree-three issue is the
overlapping-matching branch.  Beyond exact support degree six, additional
support edges are not covered by the nonnegative unit table above.
