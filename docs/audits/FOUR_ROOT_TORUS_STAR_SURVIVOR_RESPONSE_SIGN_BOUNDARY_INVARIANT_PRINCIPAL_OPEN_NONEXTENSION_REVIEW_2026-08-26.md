# Review: survivor-response sign-boundary invariant principal-open nonextension

Date: 2026-08-26

## Verdict

Accept `GLD78` as an **exact all-order local exclusion of the affine response
incidence in three named sign-boundary proportionality-chart opens**.  The
result is over `Q(i)` and hence over `C`, on the fixed-star, equal-leaf,
scale-fixed `GLD75` survivor germ.  It is not the whole-survivor principal-open
theorem because boundary directions with trivial or standard raw components,
and mixtures among isotypic blocks, have not been classified.  The global
Krenn--Gu conjecture remains **UNRESOLVED**.

## Evidence checked

The invariant verifier reconstructs the exact `GLD74` raw fibre and mixed
quotient.  It checks the actual transformed `81 x 79` nuisance map, all four
complete `81 x 79` legal response maps, the target, and the diagonal target
response under every leaf permutation.  Thus the Reynolds argument uses
interface/source-response covariance, not only abstract tensor symmetry.

The fixed quotient pivot uses rows

```text
(0,1,2,3,4,5,7,8,9,11,17,27,53)
```

and has value `8(1+i)/27`.  Reynolds averaging the complete raw kernel has
rank eight.  Kernel columns `(0,7,8,9,10,12,13,16)`, restricted to fibre rows
`(0,1,8,9,10,12,13,16)`, have determinant `1008i`.  Therefore neither the
quotient nor invariant-basis open is hidden.

At slopes `(-1,1)`, `(1,-1)`, and `(-1,-1)`, the invariant proportionality
operator and its affine augmentation have ranks `(8,9)`.  The selected exact
`9 x 9` determinants are respectively

```text
6574160/27 + (1735448/9)i,
153664/9  + (44480/3)i,
-29451260/81 + (3419540/81)i.
```

They are nonzero and define regular principal opens in survivor-frame times
slope-chart space.

The independent no-import audit uses only the Python standard library,
rebuilds the permanent map and response quotient in reverse free-variable
order, independently Reynolds-averages actual raw vectors, and reproduces
the quotient pivot, invariant basis determinant, all three rank jumps, and
all three obstruction determinants.  It simultaneously replays `GLD74`'s
affine certificate and the `GLD77` sign-plane trichotomy.

## All-order argument audited

Use the original fixed-star coordinates.  The nuisance map `b`, its kernel,
and the legal response operators are fixed; only the equal-leaf survivor
tensor and an affine raw section move.  Consequently the eight invariant raw
directions above are a fixed basis, rather than a guessed moving basis.

Given any solution of the homogenized proportionality equations, average its
actual `79`-coordinate raw vector over leaf `S_3`.  The averaged vector remains
a preimage of the equal-leaf tensor and satisfies the same equations.  This
step is valid for an arbitrary raw correction: it does not assume the
35-coordinate pivot basis is equivariant.  Its kernel component is invariant,
so it is a combination of the eight certified columns.  Nonvanishing of the
corresponding augmented `9 x 9` determinant then forces the homogenizing
coefficient `s` to vanish.  Because this is column independence over the
localized coordinate ring, it also excludes formal arcs for which `s`
vanishes to positive order but is not identically zero.  The proof is thus
all-order; the separate first-jet computation is corroboration, not the
geometric bridge.

## First-strict-jet control and corrected derivation

The dual-number verifier retains the moving tensor/interface presentation,
all `35` raw corrections, all four scale-fixed survivor tangents, the moving
`13`-column quotient, and both proportionality-slope derivatives.  At every
sign point it obtains

```text
rank M=34,   rank S=36,   rank[S|r]=37.
```

Early scratch calculations for two points omitted the two slope derivatives.
Those incomplete numbers were rejected before publication.  The portable
verifier and the theorem use only the corrected `41`-column first-jet system.
The jet result by itself is explicitly not used to claim an all-order
exclusion.

## Load-bearing limits

1. Each `delta_j` depends on both the survivor frame and slope variables.
   `GLD78` does not produce a survivor-only exceptional polynomial by
   eliminating the slopes.
2. The conclusion is in the local `z_0!=0` proportional-column chart around
   each of the three `GLD77` points.  It does not cover other rank-one charts.
3. The projective points at `s=0` remain valid boundary points.  What is
   excluded is an affine branch with `s` not identically zero entering through
   the named open.
4. Boundary directions outside the pure sign plane may have trivial,
   standard, or mixed isotypic components.  They remain the next parent
   obligation.
5. Other survivor components, frame gauges, source presentations, roots,
   non-star interfaces, maximum-root/no-fifth-root certification, and global
   graph coverage remain open.
6. No raw lift, source graph, graph witness, or counterexample was found.

## Recommended successor

Exploit the `S_3` isotypic decomposition before attempting a full
35-variable blow-up.  Classify the projective rank-one scheme by the
isotypic support of a raw direction: trivial-only, standard-only, and mixed
supports.  Use Reynolds central idempotents, determinantal/Fitting ideals,
and exact saturation by the already named chart factors.  A finite exhaustive
component cover would combine with `GLD78` to reopen the properness route from
the pointwise `GLD74` certificate to a genuine survivor-open exclusion.
