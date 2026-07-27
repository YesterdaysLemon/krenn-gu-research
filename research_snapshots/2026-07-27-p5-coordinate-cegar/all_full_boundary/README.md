# Entire all-full `P_5` boundary

## Status

This directory contains exact computer-algebra replay evidence for the
entire all-full part of the `P_5 -> Delta_3` exact-three-coordinate
boundary.

All 226 support orbits are impossible over `C`:

```text
213 fail the complex-valid pair-incidence quotas;
  3 are covered by the prior proper-tricolour support theorem;
 10 reduce to 198 pair-signature tuples, all with unit coefficient ideals.
```

This is a genuine finite theorem.  It does not exclude partial
non-coordinate support, the four/five-coordinate-row branch, or the
global Krenn--Gu conjecture.

The mathematical statement and proof boundary are in
[`P5_ALL_FULL_BOUNDARY_OBSTRUCTION.md`](../../../P5_ALL_FULL_BOUNDARY_OBSTRUCTION.md).

## Package layout

```text
audit.json
    Exhaustive support-orbit and pair-signature census.

manifest.json
    Case keys, supports, hashes, solver outcomes, and aggregate counts.

systems/*.sing
    Exact regenerated Singular systems for all 198 final cases.

systems/*.singular.out
    The `UNIT_IDEAL` result for every Singular-certified case.

systems/*.ms
systems/*.msolve.out
    Independently converted split-saturation systems and `[-1]:` outputs
    for the subset also certified by msolve 0.10.1.
```

Each Singular system has 21 Laurent parameters and one Rabinowitsch
variable.  It contains every distinct nonzero mixed permanent
coefficient, plus one equation saturating all 21 parameters and the three
required pure coefficients.  The mixed-equation histogram is:

```text
216:   9 cases
220:  18 cases
230:  45 cases
240: 126 cases
```

The `msolve` inputs replace the one high-degree saturation equation with
24 separate inverse equations.  The verifier reconstructs that conversion
from the Singular source; it is exactly equivalent to requiring the 21
parameters and three pure coefficients to be nonzero.

## Replay

From the repository root, run:

```text
python audit_p5_all_full_boundary_obstruction.py
python verify_p5_all_full_boundary_obstruction.py
```

The audit does not trust the committed orbit list.  It reconstructs both
graph automorphism groups, enumerates the labelled assignments, rebuilds
the local pair-signature catalogue, reapplies all Hall quotas, and checks
the resulting 198 case keys.

The verifier semantically regenerates every polynomial system from its
five signature indices, checks exact source equality and all SHA-256
hashes, and requires at least one exact unit-ideal solver result for every
case.  Singular covers all 198.  The msolve results are a partial
independent cross-check because that engine can conservatively classify
some overdetermined split-saturation systems as positive-dimensional
before completing the basis.

The committed one-line outputs are replay evidence.  A fresh solver run,
like any computer-algebra proof, still trusts the selected exact CAS
implementation.

## Solver provenance

The Singular sources use a global `dp` order and `slimgb`; no local-order
result is accepted.

The second-engine inputs were run with the official static
`msolve 0.10.1` Linux x86-64 binary.  Its SHA-256 is recorded in
`manifest.json`; the binary itself is not committed.

## Boundary

The parent coordinate-CEGAR ledgers remain exploratory.  After importing
this theorem as a single all-full blocking clause, they still must exhaust:

1. exact-three-coordinate models containing a support mask `3`, `5`, or
   `6`; and
2. models with four or five coordinate rows in at least one local map.

An arbitrary-order lift remains a separate obligation even if those
finite branches are completed.
