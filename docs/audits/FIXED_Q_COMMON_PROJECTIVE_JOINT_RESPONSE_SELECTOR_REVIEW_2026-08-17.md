# Fixed-Q common projective joint-response selector hostile review -- 2026-08-17

## Verdict

**Accepted at the frozen theorem and script hashes recorded below.**  No P0
or P1 defect remains.  The result is an exact characteristic-zero
common-projective operator-supply criterion and a conditional shifted `GLD3`
detector.  It does not force a common line or three-colour activity on a
hypothetical witness, integrate a formal response package into a graph fibre,
or imply a permanent restriction.  The global Krenn--Gu conjecture remains
**UNRESOLVED**.

## Common coefficient space

For each of the six pair targets and the four-port target, `GLD15` supplies an
exact coefficient space `C_S subset K^2` of constant operator combinations
`alpha M_S+beta Z_S`.  Their intersection is nonzero exactly when no target
space is zero and all rank-one target spaces have the same projective line;
rank-two spaces impose no restriction.  A vector in the intersection gives
seven target-specific functionals with the same coefficients on one graph,
one residual pair, one contraction, and one fixed `M/Z` normalization.

This is strictly weaker than demanding joint rank two at all seven targets.
The proof does not mix contractions, graphs, windows, or target-dependent
coefficient axes.  Separate nonzero rank-one rows with different slopes do
not form a common package.

## Homogeneous shifted detector

On the physical `h=0` branch, a common vector defines

```text
D_e=alpha B_e+beta K_e,
T'=alpha C(B)+beta X(B,K).
```

Direct expansion proves the homogeneous identity

```text
alpha T'=C(D)-C(beta K).
```

The corrected channel `beta K` retains the physical two-shore form, so every
one-port flattening of `C(beta K)` has rank at most two.  The inherited `GLD3`
nine-word determinant therefore applies without division by either
coefficient.  When `alpha=0`, three-colour activity would make an invertible
diagonal matrix have rank at most two.  When `alpha!=0`, activity forces one
of nine displayed mixed coefficients of `T'` to be nonzero.  Either conclusion
contradicts the pure GHZ target after legal selection.

## Sharpness controls

The unequal-slope physical response control was independently enumerated on
all `3^4=81` four-port words.  Its six pair rows have slope `[1:2]`, its
four-port row has slope `[1:1]`, and

```text
T'(0000)=-12,
T'(1111)=1,
T'(2222)=1,
all mixed coefficients=0,
activity products=(2,2,2).
```

Thus target shape and full three-colour activity do not replace slope
synchronization.  The written proof correctly separates mixed zero/colour
words of multiplicity `2+2`, which have the unique cancelling diagonal
matching, from odd multiplicities, which have no diagonal matching.

The rational common `[1:1]` camouflage has pure values `(3,4/3,1)` and only
two active colours.  Hence activity remains load-bearing even when the common
line and target shape are present.  Both controls are response-algebra
fixtures, not legal module-selector or witness realizations.

## Independent checks and frozen hashes

The primary uses exact SymPy symbolic and matrix arithmetic.  The independent
audit imports neither SymPy nor the primary; it separately uses sparse
polynomial dictionaries, elementary two-dimensional constraint ranks,
`Fraction` tensor coefficients, and direct complementary-matching
enumeration.  Both focused commands pass, as do Ruff check, Ruff format
check, conflict-marker scanning, and `git diff --check`.

Frozen at base HEAD `342531ec2e00a652c641231b467960b9cb501a21`:

```text
theorem  3639526ee77f51e9071ac3fe715f0273c8354fcfe968bf819c9923a4ca7146e0
primary  d381d954def8881d9a17de771fe9425db71a6dd41e423825e09157f665adb688
audit    f5295fc1a63c6eeba206fff3ec11dc00569f4523b2f2616849de03927c1b22e0
```

The scripts replay the bounded homogeneous identity, all `4^7` canonical
subspace intersections, pure axes, and both sharpness controls.  The complete
module-operator criterion and determinant argument remain the load-bearing
mathematical proofs.

## Exact remainder

Still **UNKNOWN**: forcing a nonzero common coefficient line on any required
witness window; excluding zero spaces or differently sloped rank-one spaces;
forcing three-colour pair-depth activity for the common selected package;
physical integration beyond the fixed companion equation; and every
weighted-permanent consequence.
