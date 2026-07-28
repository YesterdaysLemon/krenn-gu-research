# Exact-one-partial `P_5` boundary

## Status

This directory contains exact computer-algebra replay evidence for the
entire exact-one-partial part of the `P_5 -> Delta_3`
exact-three-coordinate boundary.

All 5,676 support orbits are impossible over `C`:

```text
  224 are absent from the complex-valid local catalogue;
5,133 fail the complex pair-incidence Hall quotas;
  319 have support-only coefficient ideals equal to the unit ideal.
```

This is a genuine finite theorem.  Combined with the all-full theorem, it
forces at least two partial non-coordinate cells in any remaining
exact-three-coordinate model.  It does not exclude that deeper partial
layer, the four/five-coordinate-row branch, or the global Krenn--Gu
conjecture.

The mathematical statement and proof boundary are in
[`P5_ONE_PARTIAL_BOUNDARY_OBSTRUCTION.md`](../../../P5_ONE_PARTIAL_BOUNDARY_OBSTRUCTION.md).

## Package layout

```text
audit.json
    Exhaustive support-orbit and pair-signature census.

manifest.json
    Case keys, supports, hashes, solver outcomes, and aggregate counts.

systems/*.sing
    Exact regenerated Singular systems for all 319 final supports.

systems/*.singular.out
    The `UNIT_IDEAL` result for every directly certified support.

systems/*.split.sing
systems/*.split.singular.out
    Equivalent split-saturation sources and results for 12 slow direct
    encodings.
```

Every system has 25 Laurent parameters and one Rabinowitsch variable.  It
contains every distinct nonzero mixed permanent coefficient, plus one
equation saturating all 25 parameters and the three required pure
coefficients.  The coefficient systems impose no pair-incidence
relations, so they exclude a superset of every exact local-signature
stratum represented by that support.

## Replay

From the repository root, run:

```text
python audit_p5_one_partial_boundary_obstruction.py
python verify_p5_one_partial_boundary_obstruction.py
```

The audit does not trust the committed orbit list.  It reconstructs both
graph automorphism groups, enumerates all labelled supports, rebuilds the
6,495-pattern local pair-signature catalogue, reapplies all Hall quotas,
and checks the resulting 319 support keys.

The verifier semantically regenerates every polynomial system from its
support, checks exact source equality and every SHA-256 hash, reconstructs
the split-saturation conversion, and requires an exact unit-ideal result
for all 319 supports.

The committed one-line outputs are replay evidence.  A fresh solver run,
like any computer-algebra proof, still trusts the selected exact CAS
implementation.

## Solver provenance

The Singular sources use characteristic zero, a global `dp` order, and
`slimgb`; no local-order result is accepted.  The 12 split systems replace
the one product saturation equation by 28 separate inverse equations.
This is exactly equivalent to requiring all 25 parameters and three pure
coefficients to be nonzero.

## Boundary

The remaining finite `P_5` work is:

1. exact-three-coordinate models with at least two partial
   non-coordinate cells; and
2. models with four or five coordinate rows in at least one local map.

An arbitrary-order lift remains separate even if both finite branches are
completed.
