# `P_5` proper all-full tricolour obstruction

## Status

This is an exact finite-boundary theorem over `C`.

Suppose a hypothetical restriction

```text
P_5 -> Delta_3
```

has exactly three coordinate rows in each of its five local maps.  Assume
also that:

1. the other two rows in every map have full three-colour support; and
2. for every source row, its three coordinate occurrences use the three
   target colours exactly once.

Then no such restriction exists.

The theorem excludes all three support orbits satisfying these hypotheses.
It does not exclude partially supported non-coordinate rows, an unbalanced
assignment of coordinate colours, or the branch with four or five
coordinate rows in a local map.  It is therefore not a proof of the full
Krenn--Gu conjecture.

## Setup

Write the five local maps as

```text
phi_i : C^3 -> C^5,  i=0,...,4,
```

and let `r_(i,p)` be source row `p` of `phi_i`.  A coordinate row has
support mask `1`, `2`, or `4`; a fully supported row has mask `7`.

The earlier source-row tricolour cover and cycle dichotomy show that in
the exact-three-coordinate branch, the ten non-coordinate cells form a
two-regular bipartite graph on the five modes and five source rows.  Its
shape is either

```text
C10
```

or

```text
C4 disjoint union C6.
```

This theorem addresses the proper all-full subboundary: every
non-coordinate cell has mask `7`, while the singleton colours form a
proper three-colouring at both sides of that bipartite incidence array.

## Exact orbit census

Up to independent permutations of the five modes, five source rows, and
three target colours, there are exactly three support orbits:

```text
C10 orbit 126
((7,7,4,2,1),
 (1,7,7,4,2),
 (2,1,7,7,4),
 (4,2,1,7,7),
 (7,4,2,1,7))

C10 orbit 122
((7,7,4,2,1),
 (4,7,7,1,2),
 (2,1,7,7,4),
 (1,4,2,7,7),
 (7,2,1,4,7))

C4+C6 orbit 56
((7,7,4,2,1),
 (7,7,2,1,4),
 (4,1,7,7,2),
 (2,4,1,7,7),
 (1,2,7,4,7))
```

For the fixed `C10` full-support graph, direct enumeration gives 36
labelled proper singleton-colour assignments.  Its automorphism group has
order 10, and the assignments split into two orbits of sizes 6 and 30.

For the fixed `C4+C6` graph, there are 24 labelled assignments.  Its
automorphism group has order 24, and all assignments form one orbit.
Thus the three displayed representatives are exhaustive.

## Coefficient obstruction

Each representative contains 45 required nonzero matrix entries.  The
associated row/column gauge graph is connected.  Fixing a spanning tree
normalizes 19 entries to one and leaves 26 coefficient variables

```text
u0,...,u25.
```

Expand the pullback of the order-five permanent.  Among the 240 mixed
target colourings, exactly 150 use all three colours:

```text
 60 have multiplicities 3+1+1;
 90 have multiplicities 2+2+1.
```

On the coefficient torus, divide each coefficient by any common monomial
factor in the nonzero `u_j`; this does not change its zero set.  Let
`f_alpha` be the resulting normalized permanent coefficient for each of
those 150 tricolour target words, and let `q_0,q_1,q_2` be the three
normalized pure coefficients.  A restriction to `Delta_3` would require

```text
f_alpha = 0                     for all 150 tricolour words,
u0*...*u25*q_0*q_1*q_2 != 0.
```

Introduce a Rabinowitsch variable `z` and form the ideal

```text
I = <
      all 150 f_alpha,
      z*u0*...*u25*q_0*q_1*q_2 - 1
    >
    in Q[u0,...,u25,z].
```

For each of the three orbit representatives,

```text
I = <1>.
```

Hence the required coefficient torus is empty over the algebraic closure
of `Q`, and therefore over `C`.  Notice that none of the 90 mixed
coefficients using only two colours is needed.

## Verification

Run:

```text
python claims/p5/frontier/audit_p5_all_full_tricolour_obstruction.py
python claims/p5/frontier/verify_p5_all_full_tricolour_obstruction.py
```

The independent combinatorial audit reconstructs the two bipartite
automorphism groups, enumerates every proper singleton-colour assignment,
partitions them into orbits, checks that the three packaged
representatives cover those orbits, and verifies the `60+90=150`
tricolour count.

The primary verifier semantically reconstructs all 150 permanent
coefficients, removes only their common nonzero monomial factors, and
reconstructs the saturation equation directly from each displayed support
array.  It then:

1. checks that the committed Singular source encodes exactly that ideal;
2. converts the source independently to the committed `msolve` input;
3. checks SHA-256 hashes for every artifact; and
4. requires both Singular `slimgb` to report `UNIT_IDEAL` and
   `msolve 0.6.5` to report `[-1]:`.

The source systems have 151 equations in 27 variables over `Q`.
The two exact computer-algebra engines use different implementations;
their one-element bases independently certify the unit ideal.

The complete sources, inputs, outputs, and package notes are in
[`all_full_tricolour_boundary/`](../../../research_snapshots/2026-07-27-p5-coordinate-cegar/all_full_tricolour_boundary/README.md).

## Boundary

This result closes the most symmetric all-full, properly coloured part of
both cycle architectures.  It does not cover:

- a non-coordinate row with support mask `3`, `5`, or `6`;
- repeated singleton colours down a source column;
- any exact-three-coordinate support pattern outside the proper all-full
  subboundary; or
- a local map with four or five coordinate rows.

Those cases remain in the finite `P_5` coordinate-support search.  Even a
complete proof that `P_5` has subrank at most two would still need a
separate arbitrary-order argument to resolve the prize conjecture.
