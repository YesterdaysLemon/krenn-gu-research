# Degree-one Macaulay obstructions in 1,960 new `C10` orbits

## Status

This is an exact finite theorem inside the `P_5` exact-three-coordinate,
exact-three-partial `C10` boundary.  Rational identities with linear
polynomial multipliers exclude 1,960 orbits not covered by the
binary-fork, triangle, five-cycle, or scalar-span certificates.

The certified union therefore grows from 1,690 to 3,650 of the 11,751
audited `C10` support orbits.  The remaining 8,101 are not covered by
these certificate layers.

This does **not** close the remaining `C10` cases, the other `P_5`
branches, an arbitrary-order lift, or the global Krenn--Gu conjecture.

## The certificate space

Let `F_i` be the normalized forbidden mixed-colour coefficient
polynomials and let `u_0,...,u_22` be the free supported edge
parameters after the spanning-tree gauge.  The degree-one Macaulay
space searches for an identity

```text
sum_i (a_i + sum_j b_ij*u_j) F_i = 1
```

with rational `a_i,b_ij`.  This is ordinary sparse linear algebra on
the coefficient vectors of the rows `F_i` and `u_j*F_i`.  Such an
identity immediately contradicts the simultaneous vanishing of all
forbidden coefficients.

No Laurent saturation equation or pure-amplitude nonzero assumption
appears in these certificates.  Normalization uses only the nonzero
supported-edge semantics already built into the support catalogue.

## Exact search and reconstruction

After removing the 1,690 previously certified orbits, the search scans
all 10,061 remaining systems.  Sparse Gaussian elimination modulo
`1,000,003` finds 1,960 degree-one hits.  Wang reconstruction lifts
every hit to rational coefficients, and direct rational arithmetic
checks every polynomial identity in characteristic zero.

A modular miss is not treated as a rational non-membership proof.
Thus 1,960 is a certified lower bound, not a completeness theorem for
the degree-one certificate space.

The maximum certificate denominators are:

```text
denominator 1:    2
denominator 2: 1,842
denominator 4:  109
denominator 6:    2
denominator 8:    5
```

Certificate supports range from 3 to 165 Macaulay rows.  The two
three-row certificates have the unary affine-fork form

```text
Q = 1 + L*P,
```

giving `Q-L*P=1`.  Twenty-four four-row certificates have the split
affine-fork form

```text
P=A+B,  Q=1+L*A,  R=1+L*B,
```

giving `Q+R-L*P=2`.  Here `L` is affine-linear rather than the single
monomial used in the earlier binary-fork rule.

The remaining sixteen four-row certificates split into eleven
translated-fork identities

```text
Q+R-U-m*T = 2
```

and five two-multiplier grid identities

```text
P+Q-x*R-y*S = 2.
```

Thus all 42 certificates with at most four Macaulay rows already have
human-scale forms.

Twenty more elimination certificates have the six-row
difference-rectangle form

```text
Q1-P1 = 1 + (y-x)A,
Q2-P2 = 1 + (y-x)B,
T = A+B,
```

which gives

```text
Q1+Q2-P1-P2+(x-y)T = 2.
```

An exact detector finds only two such rectangles in the first 200
catalogue orbits, so this attractive template does not explain most of
the broader Macaulay coverage.

The ordered rational certificate list has SHA-256

```text
ec7413fa10dfd4acaba533e2f6ff1e2c645fcaeea877d1362826955bb9ca47bd.
```

The verifier regenerates every selected polynomial through both the
fast integer-bitmask implementation and the repository's original
SymPy generator, checks termwise agreement, and replays every rational
identity.

Run:

```text
PYTHONPATH=tmp/python_deps python \
  verify_p5_c10_degree_one_macaulay_obstruction.py
```

## What is and is not sustainable

Degree one is practical: two memory-bounded shards scanned the 10,061
previously uncovered systems in about fifteen minutes on this host,
while each worker stayed near 120 MiB.

A guarded degree-two dictionary-Gaussian probe is not practical.  On
one degree-one miss it processed 13,194 of roughly 57,600 rows in 120
seconds, accumulated 1,669,740 basis nonzeros, and reached no decision.
The next computational layer should use sparse-core extraction, an
F4-style solver, or a black-box finite-field linear solver rather than
scaling this implementation directly.
