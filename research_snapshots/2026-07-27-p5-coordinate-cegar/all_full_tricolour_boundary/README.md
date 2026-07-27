# Proper all-full `P_5` tricolour boundary

## Status

This directory contains exact computer-algebra certificates for a finite
subboundary of the exploratory `P_5 -> Delta_3` search.

All three proper-colour, all-full, exact-three-coordinate support orbits
are impossible over `C`.  This is a genuine finite theorem, but it does
not exhaust either active coordinate-support branch and does not resolve
the global Krenn--Gu conjecture.

The mathematical statement and proof boundary are in
[`P5_ALL_FULL_TRICOLOUR_OBSTRUCTION.md`](../../../P5_ALL_FULL_TRICOLOUR_OBSTRUCTION.md).

## Packaged systems

| Case | Full-cell graph | Singular source | `msolve` input | Outputs |
| --- | --- | --- | --- | --- |
| `c10_orbit_126` | `C10` | `c10_orbit_126.sing` | `c10_orbit_126.ms` | `UNIT_IDEAL`, `[-1]:` |
| `c10_orbit_122` | `C10` | `c10_orbit_122.sing` | `c10_orbit_122.ms` | `UNIT_IDEAL`, `[-1]:` |
| `c4c6_orbit_56` | `C4+C6` | `c4c6_orbit_56.sing` | `c4c6_orbit_56.ms` | `UNIT_IDEAL`, `[-1]:` |

Every source represents the same construction for its support orbit.
Common monomial factors are removed from coefficient equations; this is
equivalent on the explicitly saturated coefficient torus.

```text
26 gauge-free nonzero entry variables
150 tricolour mixed-coefficient equations
3 required nonzero pure coefficients
1 Rabinowitsch saturation equation
```

Thus each ideal has 151 equations in 27 variables over `Q`.  None of the
90 two-colour mixed-coefficient equations is included.

## Replay

From the repository root, run:

```text
python audit_p5_all_full_tricolour_obstruction.py
python verify_p5_all_full_tricolour_obstruction.py
```

The audit reconstructs the orbit census independently.  The verifier
rebuilds all permanent coefficients from the support arrays, checks exact
source and conversion equality, checks every artifact hash, and accepts a
case only when both committed solver outputs certify the unit ideal.

The output token `UNIT_IDEAL` comes from Singular `slimgb`.
The `msolve 0.6.5` convention `[-1]:` is its one-element Gröbner basis for
the unit ideal.  The committed outputs are replay evidence; as with any
computer-algebra proof, a fresh computation still trusts the chosen exact
CAS implementations.

## Boundary

This package does not exclude partial support in a non-coordinate row,
non-proper singleton-colour assignments, or the branch with four or five
coordinate rows in a local map.  The parent snapshot ledgers remain
work-in-progress searches rather than exhaustive certificates.
