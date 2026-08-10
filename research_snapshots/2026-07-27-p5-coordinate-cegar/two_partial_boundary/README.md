# Exact-two-partial `P_5` boundary

## Status

This directory contains exact computer-algebra replay evidence for the
entire exact-two-partial part of the `P_5 -> Delta_3`
exact-three-coordinate boundary.

All 76,098 support orbits are impossible over `C`:

```text
11,614 are absent from the complex-valid local catalogue;
59,911 fail the complex pair-incidence Hall quotas;
 1,265 fail direct necessary support semantics;
 3,308 have support-only coefficient ideals equal to the unit ideal.
```

This is a genuine finite theorem.  Combined with the all-full and
exact-one-partial theorems, it forces at least three partial
non-coordinate cells in any remaining exact-three-coordinate model.  It
does not exclude that deeper partial layer, the
four/five-coordinate-row branch, or the global Krenn--Gu conjecture.

The mathematical statement and proof boundary are in
[`P5_EXACT_TWO_PARTIAL_BOUNDARY_OBSTRUCTION.md`](../../../claims/p5/boundaries/P5_EXACT_TWO_PARTIAL_BOUNDARY_OBSTRUCTION.md).

## Package layout

```text
audit_c10.json
audit_c4c6.json
    Independent fixed-shape support-orbit and pair-signature censuses.

manifest.json
    Case keys, supports, hashes, solver outcomes, and aggregate counts.

systems/*.sing
    Exact regenerated Singular systems for all 3,308 final supports.

systems/*.singular.out
    The `UNIT_IDEAL` result for 3,307 directly certified supports.

systems/*.split.sing
systems/*.split.singular.out
    The equivalent split-saturation source and result for one slow
    direct encoding.
```

Every system has 24 Laurent parameters and one Rabinowitsch variable.  It
contains every distinct nonzero mixed permanent coefficient, plus one
equation saturating all 24 parameters and the three required pure
coefficients.  The coefficient systems impose no pair-incidence
relations, so they exclude a superset of every exact local-signature
stratum represented by that support.

The package contains 6,622 files.  The SHA-256 of `manifest.json` is:

```text
cb3edbd224dead82542099f07712410c0e9a841214592437ab91b356c595c621
```

## Replay

From the repository root, run:

```text
python claims/p5/boundaries/verify_p5_exact_two_partial_boundary_obstruction.py
```

The verifier does not trust the manifest's aggregate counts.  It checks
both audit hashes, reconstructs both fixed-shape actions, compares the
independent audit and SAT support catalogues canonically, replays every
signature witness and pair Hall quota, and semantically regenerates
every polynomial system from its support.  It then checks exact source
equality, all SHA-256 hashes, the one split-saturation conversion, and a
unit-ideal result for all 3,308 supports.

The committed one-line outputs are replay evidence.  A fresh solver run,
like any computer-algebra proof, still trusts the selected exact CAS
implementation.

## Solver provenance

The Singular sources use characteristic zero, a global `dp` order, and
`slimgb`; no local-order result is accepted.  The one split system
replaces the single product saturation equation by 27 separate inverse
equations.  This is exactly equivalent to requiring all 24 parameters
and three pure coefficients to be nonzero.

## Boundary

The remaining finite `P_5` work is:

1. exact-three-coordinate models with at least three partial
   non-coordinate cells; and
2. models with four or five coordinate rows in at least one local map.

An arbitrary-order lift remains separate even if both finite branches
are completed.
