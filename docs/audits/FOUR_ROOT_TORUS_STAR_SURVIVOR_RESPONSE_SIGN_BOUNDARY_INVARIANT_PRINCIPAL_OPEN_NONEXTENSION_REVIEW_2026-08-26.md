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

**Coordinate-repair addendum (2026-08-26).**  Hostile review during `GLD80`
found that the first edition described the moving `65 x 3` quotient in the
untransformed fixed coordinates.  That is not a legal necessary condition:
the moving GHZ response has mixed coordinates there, and `GLD76` correctly
keeps all four columns of its `68 x 4` quotient.  The theorem now constructs
the `65 x 3` system only after transporting the complete nuisance and legal
response interface by the moving frame to literal `Delta_4`.  The accepted
verdict applies to that repaired formulation.

The failure is visible exactly, not only conceptually.  Along the `GLD75`
`x_6` survivor tangent, in fixed Gaussian literal-Delta output coordinates,

```text
d(U_(F_0)R(F))[(0,1,1,1),1]/dx_6=(1-i)/4,
d(U_(F_0)R(F))[(2,0,0,0),0]/dx_6=1.
```

Thus the moving target immediately acquires mixed entries if the output
coordinate change is frozen at `F_0`.

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

They are nonzero.  The repaired theorem defines their regular continuations
in survivor-frame times slope-chart space using the moving literal-Delta
kernel frame and quotient.  The verifier evaluates their exact Gaussian
specializations; it does not expand the universal moving polynomials.

The independent no-import audit uses only the Python standard library,
rebuilds the permanent map and response quotient in reverse free-variable
order, independently Reynolds-averages actual raw vectors, and reproduces
the quotient pivot, invariant basis determinant, all three rank jumps, and
all three obstruction determinants.  It simultaneously replays `GLD74`'s
affine certificate and the `GLD77` sign-plane trichotomy.

## All-order argument audited

For each frame `F`, apply the tensor intertwiner `U_F` and raw intertwiner
`S_F`.  The target becomes literal `Delta_4`; the transformed nuisance map,
complete response, kernel frame, mixed quotient, and invariant columns all
move regularly after inverting the named frame, rank-44, rank-13, and rank-8
pivots.  A matching partition gives the signed four-root relation in this
presentation, so the `GLD74` dimension count again makes rank at most one a
necessary legal-response condition.  This step repairs the missing bridge;
it is not implied merely by abstract GHZ covariance.

Because the leaf frames are equal, the transported system is leaf-`S_3`
equivariant.  Given a solution of its homogenized proportionality equations,
average the actual moving raw vector.  Its kernel component belongs to the
regular eight-dimensional invariant kernel subbundle.  Nonvanishing of the
corresponding augmented `9 x 9` determinant forces the homogenizing
coefficient `s` to vanish.  Column independence over the localized coordinate
ring excludes formal arcs even when `s` has positive valuation.  The proof is
all-order; the separate first-jet computation is corroboration, not the
geometric bridge.

## First-strict-jet control and corrected derivation

The dual-number verifier retains all `35` raw corrections, all four
scale-fixed survivor tangents, a selected moving `13`-column quotient, and
both proportionality-slope derivatives.  At every
sign point it obtains

```text
rank M=34,   rank S=36,   rank[S|r]=37.
```

Early scratch calculations for two points omitted the two slope derivatives.
Those incomplete numbers were rejected before publication.  The portable
verifier and the theorem use only the corrected `41`-column first-jet system.
The jet result by itself neither proves legal necessity in moving coordinates
nor an all-order exclusion; both bridges come from the repaired transported
argument above.

## Load-bearing limits

1. Each repaired `delta_j` depends on both the survivor frame and slope variables.
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
7. The exact verifier certifies the Gaussian values and intertwiners.  The
   regular moving continuation and matching-partition identity are proved in
   the theorem; they are not a symbolic four-parameter CAS expansion.

## Recommended successor

**Completed by `GLD79` (2026-08-26).**  Central idempotents and Schur
compression reduce the full Gaussian projective boundary to exact trivial,
sign, and standard determinant systems.  The trivial and standard systems
are empty in every slope and `K_0` is injective, so the complete boundary is
exactly the three reduced `GLD77` sign points.  `GLD80` then completes the
proper-image bridge with an intrinsic `s`-saturated projective incidence and
an algebraic DVR-selection lemma, proving an existential survivor-open
theorem.  The explicit base divisor and source/interface bridge remain open.
