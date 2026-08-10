# `P_5` exact-two-partial boundary obstruction

## Status

This is an exact finite-boundary theorem over `C`.

Suppose a hypothetical restriction

```text
P_5 -> Delta_3
```

has exactly three coordinate rows in each of its five local maps.  Among
the other ten rows, suppose exactly two have two-colour support and the
remaining eight have full three-colour support.  Then no such
restriction exists.

Together with the all-full and exact-one-partial theorems, this proves
that every hypothetical restriction in the exact-three-coordinate
branch must have at least three partially supported non-coordinate
rows.  It does not exclude that remaining branch, the
four/five-coordinate-row branch, or the global Krenn--Gu conjecture.

## Exact support census

The 15 coordinate rows have singleton masks `1`, `2`, and `4` exactly
once in each source column.  The ten non-coordinate cells form either
`C10` or `C4+C6` in the mode--source bipartite graph.

For either graph, choose the singleton colours, the two partial cells,
and one of the three masks `3`, `5`, or `6` for each partial cell.  This
gives

```text
6^5 * binomial(10,2) * 3^2 = 3,149,280
```

labelled supports per graph.  Independent packed-array enumeration and
quotienting by the fixed-graph automorphisms and global `S_3` colour
action gives:

| Shape | Support orbits | Locally invalid | Locally valid |
| --- | ---: | ---: | ---: |
| `C10` | 52,758 | 7,884 | 44,874 |
| `C4+C6` | 23,340 | 3,730 | 19,610 |
| **Total** | **76,098** | **11,614** | **64,484** |

“Locally invalid” means that one of the five row supports is absent from
the independently certified 6,495-pattern complex local-signature
catalogue.

## Pair-incidence and support-semantic funnel

For every source pair and target colour, the complex kernel Hall theorem
requires the corresponding coordinate covector to lie in that pair span
in at least two of the five modes.  Applying these 30 quotas gives:

```text
64,484 locally valid support orbits
-59,911 with no quota-compatible signature tuple
= 4,573 pair-quota-viable support orbits.
```

There are 50,109 viable five-tuples of local pair signatures across
those supports.

Two further necessary conditions depend only on the support:

- every pure-colour coefficient must contain a perfect matching; and
- no mixed-colour coefficient may have exactly one supported perfect
  matching.

They exclude 14 and 1,251 support orbits respectively, leaving 3,308
support-semantic survivors.  The two exclusion sets are disjoint in
this census.

## Coefficient obstruction for the final 3,308 supports

Every exact-two-partial support has 43 required nonzero matrix entries.
Its row/column gauge graph is connected.  Normalizing a spanning tree
sets 19 entries to one and leaves 24 independent Laurent parameters.

For each support, the verifier expands all 243 coefficients of the
pulled-back order-five permanent.  It retains every distinct nonzero
mixed-colour coefficient and the three pure-colour coefficients.  The
number of distinct mixed equations ranges from 184 to 216; the exact
histogram is pinned in the package manifest.

Let the mixed coefficients be `f_alpha`, the pure coefficients be
`q_0,q_1,q_2`, and the Laurent parameters be `u_0,...,u_23`.  The exact
support stratum can contain a restriction only if the ideal

```text
I = <
      all distinct nonzero f_alpha,
      z*u_0*...*u_23*q_0*q_1*q_2 - 1
    >
    in Q[u_0,...,u_23,z]
```

is proper.  Exact Singular `slimgb` computation in a global `dp` order
returns the unit ideal directly for 3,307 supports.  For the remaining
support, replacing the product saturation equation by the exactly
equivalent 27 inverse equations

```text
w_j*g_j - 1 = 0
```

for the 24 parameters and three pure coefficients also returns the unit
ideal.  Thus all 3,308 exact-support strata are empty over `C`.

The coefficient systems deliberately omit every positive and negative
pair-incidence constraint.  They are therefore supersets of all 50,109
compatible signature strata, and a support-only contradiction safely
excludes every signature tuple on that support.

## Independent replay

Run from the repository root:

```text
python verify_p5_exact_two_partial_boundary_obstruction.py
```

The verifier checks both committed audits and their pinned SHA-256
hashes, reconstructs the fixed-shape symmetry actions, matches the
independent audit and SAT catalogues orbit by orbit, replays every
signature witness and Hall quota, and semantically regenerates all 3,308
coefficient systems.  It requires byte-for-byte source equality, checks
every artifact hash and exact unit-ideal output, and reconstructs the
one split-saturation source from its direct source.

The independently rerun audit commands are:

```text
python audit_p5_exact_two_partial_boundary.py \
  --shape c10 \
  --output tmp/p5_c10_exact_two_audit.json

python audit_p5_exact_two_partial_boundary.py \
  --shape c4c6 \
  --output tmp/p5_c4c6_exact_two_audit.json
```

Both audit commands enforce a 20-percent host-available-memory floor by
default.

The sources, outputs, audits, manifest, and replay notes are in
[`two_partial_boundary/`](research_snapshots/2026-07-27-p5-coordinate-cegar/two_partial_boundary/README.md).

## Boundary

Combining the all-full, exact-one-partial, and exact-two-partial
theorems gives:

> In the exact-three-coordinate `P_5 -> Delta_3` branch, at least three
> of the ten non-coordinate rows have support mask `3`, `5`, or `6`.

The next exact layer has 50,388,480 labelled supports.  The
symmetry-broken enumerator
`enumerate_p5_exact_k_partial_supports.py` avoids materializing that
labelled set and directly enumerates only the support-semantic survivors.
A local map with four or five coordinate rows remains a separate branch,
and an arbitrary-order lift remains necessary even after every `P_5`
branch is closed.
