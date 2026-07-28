# `P_5` exact-one-partial boundary obstruction

## Status

This is an exact finite-boundary theorem over `C`.

Suppose a hypothetical restriction

```text
P_5 -> Delta_3
```

has exactly three coordinate rows in each of its five local maps.  Among
the other ten rows, suppose exactly one has two-colour support and the
remaining nine have full three-colour support.  Then no such restriction
exists.

Together with the all-full theorem, this shows that every hypothetical
restriction in the exact-three-coordinate branch must have at least two
partially supported non-coordinate rows.  It does not exclude that
remaining branch, the four/five-coordinate-row branch, or the global
Krenn--Gu conjecture.

## Exact support census

The source-row tricolour cover uses all 15 coordinate rows in this branch.
Each source column therefore has singleton masks `1`, `2`, and `4`
exactly once.  The ten non-coordinate cells form either `C10` or
`C4+C6` in the mode--source bipartite graph.

For each graph, choose the singleton colours, the unique partial cell,
and one of its three masks `3`, `5`, or `6`.  This gives

```text
6^5 * 10 * 3 = 233,280
```

labelled supports per graph.  Quotienting by the automorphisms of the
fixed graph and the global `S_3` colour action gives:

| Shape | Support orbits | Locally invalid | Locally valid |
| --- | ---: | ---: | ---: |
| `C10` | 3,888 | 144 | 3,744 |
| `C4+C6` | 1,788 | 80 | 1,708 |
| **Total** | **5,676** | **224** | **5,452** |

“Locally invalid” means that one of the five row supports is absent from
the independently certified 6,495-pattern complex local-signature
catalogue.

## Pair-incidence funnel

For every source pair and target colour, the complex kernel Hall theorem
requires the corresponding coordinate covector to lie in that pair span
in at least two of the five modes.  Applying these 30 quotas to every
locally valid support orbit gives:

```text
5,452 locally valid support orbits
-5,133 with no quota-compatible signature tuple
=  319 viable support orbits.
```

There are 6,575 viable five-tuples of local pair signatures across those
319 supports.  The final coefficient calculation deliberately forgets
the pair incidences and works on the larger exact-support stratum, so one
coefficient system per support orbit suffices.

## Coefficient obstruction for the final 319 supports

Every exact-one-partial support has 44 required nonzero matrix entries.
Its row/column gauge graph is connected.  Normalizing a spanning tree
sets 19 entries to one and leaves 25 independent Laurent parameters.

For each support, the verifier expands all 243 coefficients of the
pulled-back order-five permanent.  It retains every distinct nonzero
mixed-colour coefficient and the three pure-colour coefficients.  The
mixed-equation histogram is:

```text
216:  20 supports
218:  15 supports
219:   6 supports
220:  21 supports
222:  47 supports
223:  83 supports
224: 127 supports.
```

Let the mixed coefficients be `f_alpha`, the pure coefficients be
`q_0,q_1,q_2`, and the Laurent parameters be `u_0,...,u_24`.  The exact
support stratum can contain a restriction only if the ideal

```text
I = <
      all distinct nonzero f_alpha,
      z*u_0*...*u_24*q_0*q_1*q_2 - 1
    >
    in Q[u_0,...,u_24,z]
```

is proper.  Exact Singular `slimgb` computation in the global `dp` order
returns the unit ideal for 307 supports.  For the remaining 12, replacing
the single product saturation equation by the exactly equivalent inverse
equations

```text
w_j*g_j - 1 = 0
```

for all 25 parameters and three pure coefficients also returns the unit
ideal.  Thus all 319 exact-support strata are empty over `C`.

Because these systems omit every positive and negative pair-incidence
constraint, they are supersets of all 6,575 compatible signature strata.
A contradiction on the relaxed support-only system safely excludes every
signature tuple on that support.

## Verification

Run from the repository root:

```text
python audit_p5_one_partial_boundary_obstruction.py
python verify_p5_one_partial_boundary_obstruction.py
```

The audit independently reconstructs both graph automorphism groups, all
466,560 labelled supports, the symmetry quotient, the local catalogue,
all 30 Hall quotas, and the exact 319-case support list.

For each surviving support, the verifier independently rebuilds the
gauge normalization and every permanent coefficient, requires
byte-for-byte equality with the packaged Singular source, checks all
artifact hashes, and requires an exact unit-ideal result.  It also
reconstructs each split-saturation source from its direct source and
checks their exact algebraic equivalence.

The sources, outputs, audit, manifest, and replay notes are in
[`one_partial_boundary/`](research_snapshots/2026-07-27-p5-coordinate-cegar/one_partial_boundary/README.md).

## Boundary

Combining this theorem with the prior all-full theorem gives the sharper
necessary condition:

> In the exact-three-coordinate `P_5 -> Delta_3` branch, at least two of
> the ten non-coordinate rows have support mask `3`, `5`, or `6`.

The next finite layer therefore has at least two partial cells.  A local
map with four or five coordinate rows remains a separate branch, and an
arbitrary-order lift remains necessary even after all `P_5` branches are
closed.
