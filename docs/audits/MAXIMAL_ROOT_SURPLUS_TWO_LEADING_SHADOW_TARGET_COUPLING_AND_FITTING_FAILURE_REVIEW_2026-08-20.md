# Hostile review: maximum-root surplus-two leading-shadow target coupling and Fitting failure

Date: 2026-08-20

Global Krenn--Gu status: **UNRESOLVED**

## Reviewed artifacts

This review covers the LF-normalized contents with SHA-256 hashes

```text
be6940b880cd9c0e3c53bc3a3234c4b9a1e62b35512929112fbcfd25f1d951df
  claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_LEADING_SHADOW_TARGET_COUPLING_AND_FITTING_FAILURE_THEOREM.md

3c68d303a24039af6296736b2323323ba45a71603c29474ead0b599d4ab64241
  claims/arbitrary-order/verify_maximal_root_surplus_two_leading_shadow_target_coupling_and_fitting_failure.py

dbb9d06ddd016cf30dc62844884fbe7ee6189295b1ea2ce278cbe0a918fd8835
  claims/arbitrary-order/audit_maximal_root_surplus_two_leading_shadow_target_coupling_and_fitting_failure.py
```

The theorem is proposed as `GLS18`.  Its exact inputs are GLD15's complete
fixed-`Q` target equation, GLS17's partial-root quotient, and GLS5's geometric
all-rank Fitting method.  It neither changes those inputs nor imports a
source-witness coverage statement.

## Verdict

**PASS for the complete-target leading identity, response-gated quotient-rank
equivalence, universal failure criterion on all nuisance-rank fibres, and the
four-root full first-shadow consequence.**  The proof is characteristic zero,
pointwise, denominator-free before the geometric criterion, and retains every
exceptional residual contraction.

**FAIL as leading-survival forcing, simultaneous failure exclusion, selected
response activity, GLS15 foreign transport, GLS8 promoted-source integration,
or strategic-node closure.**  No such claim is made.  The theorem gives an
exact finite system for the remaining bad locus; it does not show that this
system is inconsistent on an actual witness.

## Adversarial attacks

1. **The target identity silently assumes separate `M` attachment at joint
   rank one.**  Rejected.  It is obtained by applying GLS17's induced quotient
   map to GLD15's complete two-column equation.  The map kills the `Z` class
   and sends the `M` class to `b_(A,S)`; no rank-one normalization or separate
   GLD15 selector is used.

2. **A residual contraction might kill `alpha_c`, invalidating independence.**
   Rejected.  The declared chart is the fully supported residual Laurent
   torus.  Every `alpha_c` is a Laurent unit, as are the factors suppressed in
   `d_(A,S,c)`.

3. **The left tensor can have rank two or three despite the decomposable right
   side.**  Rejected.  Flattening against the independent labelled words
   `w_(S,c)` has column span exactly the three quotient classes.  Equality
   with `b_(A,S) tensor M_S` bounds that span by one.

4. **`b!=0` and `M_S!=0` need not imply a pure leading class survives if
   `M_S` is supported only on mixed target words.**  Rejected.  The complete
   equality has no mixed word on the left.  If `b!=0`, coefficient comparison
   kills every mixed coordinate of `M_S`; nonzero `M_S` then has a nonzero
   pure coordinate and the corresponding leading class is nonzero.  The
   independent audit enumerates all five-word branches.

5. **Response zero is being mistaken for absence of a legal operator.**
   Rejected.  `M_S=0` forces the displayed leading pure classes to be
   swallowed, but the theorem does not infer that `(1,0)` is absent from the
   full operator space.  Its only operator-space contrapositive comes from
   GLS17 in the safe direction.

6. **All leading classes swallowed implies pure `M` is absent.**  False and
   not claimed.  A full-module functional can remain invisible in every
   displayed shadow.  Corollary 1.1 proves only
   `(1,0) notin C_S => all leading classes are swallowed`.

7. **The Fitting criterion checks only one generic nuisance rank.**  Rejected.
   It ranges over every minor size.  At a point of nuisance rank `j-1`, the
   `j`-minor comparison detects the rank rise.  The union covers rank zero,
   all intermediate ranks, full rank, and every exceptional rank-drop fibre.

8. **Containment (18) has the wrong direction.**  Rejected.  Emptiness requires
   `V(I_j(B))` to lie in `V(I_j([B|D]))`, which is exactly
   `I_j([B|D]) subset sqrt_geom(I_j(B))`.

9. **The principal gate in (20) requires an unspecified power of `rho`.**
   Rejected.  Set-theoretically, a minor vanishing on
   `V(I_j(B)) intersect D(rho)` means `rho` times that minor vanishes on all
   of `V(I_j(B))`, hence lies in its geometric radical.  Conversely that
   first-power containment immediately gives vanishing on `D(rho)`.

10. **Several alternative activity coordinates may be compressed to their
    product.**  False and explicitly rejected.  The active locus of an ideal
    `(p_1,...,p_m)` is the union of the principal opens `D(p_i)`.  Each member
    must be checked; their product would require all coordinates nonzero.

11. **The finite-family statement chooses a different residual point for each
    target.**  Rejected.  Every incidence locus uses one shared Laurent point
    and intersects all selected target rank-rise conditions there.  Choice
    functions handle only the finite disjunction of which partial-root shadow
    survives for each target.

12. **The finite incidence formulation proves nonemptiness or emptiness.**
    False.  It only gives an exact system whose outcome remains open.  No
    finite atlas or support cover is asserted.

13. **At four roots, swallowing the three pure four-port columns merely gives
    a three-dimensional subspace of a larger leading space.**  Rejected.  For
    `S=U,A={a}`, the leading space is exactly `V_a^*`, and the three fully
    supported colour covectors form a basis.  Their absorption makes the
    nuisance shadow the whole space.

14. **The same fullness holds for a pair target.**  False and explicitly
    rejected.  The pair leading ambient space has dimension nine; only the
    three independent diagonal pure tensors are forced into nuisance.

15. **A proper four-port first-root shadow alone supplies the GLD16 package.**
    False.  It supplies a nonzero pure-`M` row only when `M_U!=0`.  GLD16 still
    separately requires the sufficient family of pair rows and its declared
    three-colour selected-response activity.

16. **This theorem proves GLS15 foreign transport membership.**  False.  It
    works in target-local partial-root shadows.  It supplies no map from a
    foreign target's absorbed projective direction into `N_S^J`.

17. **This theorem integrates GLS8.**  False.  GLS8's promoted two-probe chart
    is a different source interface.  No source-witness coverage map between
    that chart and the original fixed-`Q` partial-root shadows is proved here.

18. **The four-root consequence closes the strategic node.**  False.  The
    simultaneous full-shadow bad locus, response/activity failures, arbitrary-
    root source coverage, and promoted GLS8 interface all remain open.

## Independence assessment

The primary verifier uses exact rational elimination, explicit quotient rank
comparisons, direct minor generation, and rational four-root bases.  It checks
all four leading/response presence branches, 625 bounded rank/minor tables,
all coordinate first-shadow masks, and the pair diagonal embedding.

The independent audit imports no project or primary code.  It uses modular
row reduction over `GF(5)`, treats target tensors as five separately labelled
word coordinates, exhausts 78,125 complete target equations, and compares
93,750 affine principal-open point sets with a separately implemented minor
vanishing test.  Its sparse four-root representation distinguishes the full
three-space from the diagonal rank-three subspace of a nine-space.  This is a
genuinely different bounded derivation and representation.

## Exact remaining boundary

For every even target, failure of the pure-`M` route now has a concrete exact
profile: every GLS17 desired leading class and every corresponding pure GHZ
class is swallowed in every partial-root shadow.  Geometrically, universal
failure is precisely the collection of radical--Fitting containments in the
theorem, with source/activity gates represented as unions of principal opens.

At `r=4`, the four-port failure branch is exactly four full root-covector
nuisance shadows; pair failure contains the three diagonal pure tensors but
need not fill the nine-dimensional pair shadow.  The next legitimate step is
to use complete mixed GHZ equations on the same graph to contradict a
sufficient simultaneous failure profile or force a useful shared residual
point.  No permanent restriction, extraction/gluing, or global-resolution
claim follows.  The global conjecture remains **UNRESOLVED**.
