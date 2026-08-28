# Hostile review: GLD94 H4 `e=0` determinant safety

Review date: 2026-08-27
Review target: GLD94 exact equal-leaf H4 `e=0` boundary package
Global status: **UNRESOLVED**

## Scope actually supported

The primary verifier reconstructs the fixed 37-row GLD71 syndrome matrix on
the normalized H4 chart, parameterises the complete affine `e=0` boundary by
`q=t` and `p=(t^2+2t-2)/(2t^2-2t-1)`, and checks all identities over `Q`.
The collision-free parameter open is exactly the complement of
`t(t-1)(t-2)(t+1)(2t-1)(t^2-t+1)`.  The omitted values are recorded rather
than divided away and are delegated to the published GLD87/GLD89 cases.

The old and alternate raw pivots split the proof.  On a one-pivot branch, the
two bordered residuals force the displayed `a,b` family.  All three complete
37-row blocks then kill the displayed `K(t)`, while a direct block minor is
nonzero on the same open; hence the syndrome rank is six and all compatible
centres have proportional rows.  On the simultaneous-pivot branch, the two
auxiliary six-pivot charts have coprime residual numerators on the generic
open.  Their exact resultants force the GLD90 residual curve, whose `e=0`
restriction is a nonzero product on that open.  This is a determinant-safe
low-rank exclusion on `D(Omega)`.

The exact sample `(p,q,a,b,c)=(13/11,3,8/11,13/9,0)` has leaf determinant
`24/11` and syndrome ranks `(6,6)` for the full map and its first eight
columns.  It demonstrates that the unsaturated low-rank leaf family is
nonempty; the centre is nevertheless singular, so the sample is outside the
centre frame open.

## Adversarial checks

- `D(t)=2t^2-2t-1` is not silently inverted over a common zero: `gcd(D,N)=1`
  proves that `D=0` supplies no affine `e=0` point.
- The simultaneous-pivot branch is not discarded by assuming an old pivot.
  Both auxiliary charts are computed, their numerator gcd is recorded, and
  at least one is active on the collision-free open.
- The all-block kernel is checked before the rank conclusion.  The direct
  block minor supplies the lower bound, so a rank-drop artefact is not being
  used as a centre argument.
- The `C_8=1` scale is safe on the generic family because the third coordinate
  of `K(t)` is nonzero there.  The leaf determinant is separately displayed,
  so nonemptiness of the unsaturated family is not confused with membership
  in `D(Omega)`.
- The independent audit does not import the primary, GLD71, GLD86, or GLD90.
  It directly contracts a separately transcribed nine-row sparse subset and
  rederives the raw pivots, bordered residuals, auxiliary resultants, and
  rational sample.  It explicitly does not claim an independent 37-row
  kernel replay.

## Remaining objections / non-claims

1. The theorem is a low-rank syndrome/determinant statement.  It is not a
   proof that the full GLD83 intrinsic Fitting pullback is a unit, and it does
   not address `C_F` rank-drop components by itself.
2. The proof relies on the GLD75/GLD86 bridge from `B` and `rank(A)<=6` to the
   full syndrome rank condition.  That bridge remains an upstream dependency,
   not a re-proved assertion inside this package.
3. The exceptional `H1/H2/H3`, `d0`, and `P` intersections are delegated to
   GLD87/GLD89.  If those theorem scopes or their exact audits change, this
   dependency must be revisited; GLD94 does not silently absorb them.
4. The leaf family has a free `c` and is nonempty on the leaf frame open, but
   the compatible centre family is singular.  Calling this an empty
   unsaturated family or a unit-ideal result would be an overclaim.
5. `Q6=0`, `L1=0`, `L2=0` outside the exceptional values, other H4 charts,
   other survivor components and ranks, source branches, and the global
   Krenn--Gu conjecture remain open.

## Review verdict

**Accepted as GLD94, with the stated scope and limitations.**  The package is
an exact characteristic-zero exclusion of the rank-at-most-six H4 `e=0`
boundary inside `D(Omega)` after the named GLD87/GLD89 exceptional cases.  It
must not be cited as full-chart intrinsic-Fitting unitness or global
resolution.
