# Hostile review: GLD85 rank-eight full intrinsic Fitting nonzero point

## Verdict

**Accept as a scoped exact point/proper-open theorem, with the stated
boundaries.** GLD85 proves that the full `GLD83` intrinsic quadratic Fitting
ideal is not the zero ideal on one named `GLD84` rank-eight Schur chart.  It
does not prove that the residual `V(I_Pl)` is empty, and it does not resolve
the Krenn--Gu conjecture.

The claim is properly weaker than a unit-ideal or residual-exclusion result:
the pinned point lies in `D(I_Pl)`, so it only proves that the residual is a
proper closed subset of that chart.  No residual point is supplied, and no
nonemptiness claim is inferred.

## Exact claim under review

The chart is the `GLD84` rank-eight Schur chart with rows
`R_8=(0,1,2,3,4,5,6,7)`.  It has six leaf variables and two survivor
equations.  GLD85 pins

```text
z=(1,0,0,0,-2/3,0),
c=(4/5-8i/5, 2/5-4i/5, -6/5+12i/5, -12/5-36i/5,
   -12/5-6i/5, 6/5-12i/5, -6/5-18i/5, -2+4i),
x_8=0.
```

The exact chart values are `mu_R=-140/9-20i/9`, both Schur residuals zero,
`det(G)=-1-i/3`, `det(A_center)=1584/25+3312i/25`, and
`d(F)=256/3-448i/3`; the normalized gauge factor is one.  These values put
the point in the named Schur chart and `D(Omega)`.

At the point, the transported constant block has rank thirteen.  Its exact
row pivot and quotient rows are pinned, and the quotient representation of
the full intrinsic map has shape `45 x 6240`.  The forty-five selected
columns are pinned in both the theorem and certificate.

## Proof and certificate checks

The primary verifier reconstructs the point from the committed moving
response builder.  It checks the ten survivor generators, the Schur
equations, frame values, exact rank of `C_F`, and all transported constant
and response entries.  It reduces the resulting exact Gaussian-rational
coefficient data at `p=1000000007` and `p=10000019`.  Both primes are `3 mod
4`, so the adjoined `i` remains a field element.  There are `6240` real or
imaginary rational denominator slots, and the primary explicitly checks that
every one is a unit at each prime.

The selected determinant residues are

```text
p=1000000007:  9639769 + 249939722 i,
p=10000019:    1610829 + 5232695 i.
```

Both are nonzero.  Since a zero exact determinant reduces to zero under any
valid denominator-preserving reduction, this is a characteristic-zero
nonvanishing proof.  The argument is exact modular reduction, not a
floating-point rank estimate.

The independent audit is genuinely no-import: it does not import the
primary, SymPy, or the moving builder.  It decodes the packed selected
matrices from the certificate, checks the hashes and all pinned indexing
metadata, and recomputes both determinants with an independently written
Gaussian-extension implementation.  Its scope is the finite-field witness
arithmetic; it is not represented as a second derivation of the transport
matrices.  The primary/certificate equality is the bridge from the exact
construction to that audit witness.

## Hostile controls

1. **Selected versus full intrinsic map.** The old GLD83 pivot rows
   `I_old=(0,1,2,3,4,5,7,8,9,11,17,27,53)` have exact determinant zero at the
   point.  The exact old selected `45 x 45` matrix `M_Pl` is also zero: 18
   descriptor row sets are already constant-rank deficient and the remaining
   27 exact Schur coefficient vectors vanish.  This does not force the full
   exterior-coordinate family to vanish; the new full map has a nonzero
   maximal minor.
2. **No hidden quotient inversion.** The full-map witness uses the exact
   pointwise row RREF pivot
   `P=(0,1,2,3,4,5,7,8,12,17,19,26,52)`.  The old `gamma_old` pivot is not
   inverted and is recorded as zero.
3. **No residual claim.** A point outside `V(I_Pl)` proves only that this
   residual is not the whole named chart.  It does not produce a point on
   `V(I_Pl)`, prove the ideal unit, or exclude the residual.
4. **No chart extrapolation.** No assertion is made for the other 44
   rank-eight charts, the 960 rank-seven charts, the rank-at-most-six branch,
   other gauges/components, or source branches.
5. **No global upgrade.** GLD85 leaves the global Krenn--Gu conjecture
   **UNRESOLVED**.  The preceding GLD83 response obstruction can use the new
   nonempty principal open, but the remaining residual and all unexamined
   branches still require proof.

## Reproducibility

```powershell
python claims/arbitrary-order/verify_four_root_torus_star_equal_leaf_survivor_rank_eight_full_intrinsic_fitting_nonzero.py
python -I claims/arbitrary-order/audit_four_root_torus_star_equal_leaf_survivor_rank_eight_full_intrinsic_fitting_nonzero.py
```

The packed certificate is
`claims/arbitrary-order/four_root_torus_star_equal_leaf_survivor_rank_eight_full_intrinsic_fitting_certificate.json`.
No temporary path, generated run log, or external solver is required by
either checker.

## Required successor

The load-bearing next step is an exact ideal computation on this six-variable,
two-equation chart: determine whether the pulled-back `I_Pl` is unit, has
additional components, or leaves a residual.  Any later result must preserve
the rank-seven and lower-rank branches and the other finite charts rather
than treating this point as an exhaustive chart computation.
