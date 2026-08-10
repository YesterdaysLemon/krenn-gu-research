# `P_5` all-full exact-three-coordinate obstruction

## Status

This is an exact finite-boundary theorem over `C`.

Suppose a hypothetical restriction

```text
P_5 -> Delta_3
```

has exactly three coordinate rows in each of its five local maps, and
suppose every one of the other ten rows has full three-colour support.
Then no such restriction exists.

Unlike the earlier proper-tricolour result, this theorem places no
distinctness condition on the three coordinate colours within one local
map.  It closes the entire all-full part of the exact-three-coordinate
boundary.  It does not cover partially supported non-coordinate rows or
the branch in which a local map has four or five coordinate rows, and it
does not resolve the global Krenn--Gu conjecture.

## Why the source columns are already proper

Write the five local maps as

```text
phi_i : C^3 -> C^5,  i=0,...,4.
```

The source-row tricolour cover says that, for each of the five source rows
and each of the three target colours, some `phi_i` has that source row
proportional to the corresponding coordinate covector.  These are 15
distinct requirements.

The present branch has exactly

```text
5 maps * 3 coordinate rows = 15 coordinate rows.
```

Consequently every requirement occurs exactly once.  Each source column
therefore contains the singleton support masks `1`, `2`, and `4` once
each, plus two non-coordinate cells.  The cycle dichotomy shows that the
ten non-coordinate cells form either

```text
C10
```

or

```text
C4 disjoint union C6
```

in the bipartite graph between modes and source rows.  Under the all-full
hypothesis those ten cells all have support mask `7`.

The singleton colours in one *mode* need not be distinct.  Removing that
extra assumption is the point of this theorem.

## Exact support-orbit census

Fix either full-cell graph and assign the colours `0,1,2` to the three
singleton cells in each source column.  There are

```text
6^5 = 7,776
```

labelled assignments for each graph.  Quotienting by the bipartition-
preserving automorphisms of the fixed graph and by the global `S_3`
colour action gives:

| Full-cell graph | Graph automorphisms | Support orbits | Orbit-size histogram |
| --- | ---: | ---: | --- |
| `C10` | 10 | 148 | `6:1, 30:35, 60:112` |
| `C4+C6` | 24 | 78 | `12:1, 24:2, 36:7, 48:1, 72:31, 144:36` |

Thus there are exactly 226 all-full support orbits.  Three have distinct
singleton colours in every mode and are covered by the earlier
proper-tricolour obstruction.  The other 223 are the new combinatorial
boundary.

## Pair-incidence funnel

Every complex five-row local map has a support/pair-incidence signature
in the previously certified 6,495-pattern catalogue.  Only the support
masks and the ten assertions

```text
e_c^* belongs to span(r_p,r_q)
```

are retained; no finite-field higher-rank information is imported.

For every source pair and target colour, the complex kernel Hall theorem
requires this incidence in at least two of the five modes.  Applying
those 30 quotas to the catalogue:

```text
226 support orbits
- 213 with no quota-compatible signature tuple
=  13 viable support orbits.
```

The 13 consist of the three previously excluded proper support orbits and
ten nonproper support orbits.  The ten nonproper orbits contain exactly
198 quota-compatible five-tuples of local pair signatures:

| Shape and orbit | Viable tuples |
| --- | ---: |
| `C10` 82 | 27 |
| `C10` 84 | 9 |
| `C10` 89 | 3 |
| `C10` 96 | 3 |
| `C10` 118 | 27 |
| `C10` 119 | 27 |
| `C10` 124 | 3 |
| `C10` 135 | 27 |
| `C4+C6` 39 | 45 |
| `C4+C6` 68 | 27 |

This enumeration is exhaustive, not a random sample.

## Coefficient obstruction for the final 198 cases

Each signature tuple has 45 required nonzero matrix entries.  The
row/column gauge graph is connected, so a spanning-tree normalization
sets 19 entries to one and leaves 26 gauge-free variables.

The positive pair incidences produce a rank-five binomial relation
lattice.  In all 198 cases the selected pivot determinant is `+1` or
`-1`, so exact Laurent elimination leaves 21 independent parameters.
All recorded relations are replayed after the substitution.

The verifier then expands every mixed coefficient of the pulled-back
order-five permanent, removes only common monomial factors in the
explicitly nonzero Laurent parameters, and retains every distinct
nonzero mixed polynomial.  Depending on the case there are 216, 220,
230, or 240 such equations:

```text
216 equations:   9 cases
220 equations:  18 cases
230 equations:  45 cases
240 equations: 126 cases.
```

Let these mixed polynomials be `f_alpha`, let `q_0,q_1,q_2` be the three
pure-colour coefficients, and let `u_0,...,u_20` be the Laurent
parameters.  The exact ideal is

```text
I = <
      all distinct nonzero f_alpha,
      z*u_0*...*u_20*q_0*q_1*q_2 - 1
    >
    in Q[u_0,...,u_20,z].
```

For 186 cases, exact Singular computation on this direct Rabinowitsch
encoding in the global degree order returns

```text
I = <1>.
```

For the remaining slow direct encodings, replace the single saturation
equation by the exactly equivalent split system

```text
w_j*f_j - 1 = 0
```

for each of the 21 parameters and three pure coefficients.  Singular
returns the unit ideal for 15 split systems.  Three overlap the direct
set, so the two encodings certify

```text
186 + 15 - 3 = 198 distinct cases.
```

The pair signatures also contain negative incidence assertions, but the
polynomial systems deliberately omit those non-incidence inequalities.
They therefore describe supersets of the exact signature strata.  A unit
ideal for this relaxed system safely excludes the exact stratum as well.

Combining these 198 contradictions with the 213 quota exclusions and the
three proper all-full support contradictions excludes all 226 support
orbits.

## Verification

Run from the repository root:

```text
python claims/p5/boundaries/audit_p5_all_full_boundary_obstruction.py
python claims/p5/boundaries/verify_p5_all_full_boundary_obstruction.py
```

The audit independently reconstructs:

1. both fixed full-cell graphs and their automorphism groups;
2. all `2 * 7,776` labelled source-proper singleton assignments;
3. the 226 support orbits and their size histograms;
4. the 6,495 pair-signature catalogue and all 30 Hall quotas;
5. the 13 viable supports and final 198 nonproper signature tuples; and
6. exact agreement of the three proper orbits with the prior theorem.

For every surviving case, the primary verifier rebuilds the local
incidence minors, the unimodular Laurent elimination, all permanent
coefficients, and the saturation equation.  It requires byte-for-byte
agreement with the packaged Singular source, verifies every artifact
hash, and accepts the case only with a recorded unit-ideal result.

The same split-saturation conversion to `msolve 0.10.1` is also packaged
for the 111 cases where that engine returned its unit-ideal token `[-1]:`.
Those results are corroboration; the union of the two exact Singular
encodings supplies complete coverage of the 198 cases.

The sources, outputs, audit, manifest, and replay notes are in
[`all_full_boundary/`](../../../research_snapshots/2026-07-27-p5-coordinate-cegar/all_full_boundary/README.md).

## Boundary

This theorem closes the all-full layer of both exact-three-coordinate
cycle architectures.  The remaining finite `P_5` work is:

- at least one non-coordinate row has support mask `3`, `5`, or `6`; or
- at least one local map has four or five coordinate rows.

Even a complete proof that `P_5` has subrank at most two would still need
a separate arbitrary-order argument to settle the prize conjecture.
