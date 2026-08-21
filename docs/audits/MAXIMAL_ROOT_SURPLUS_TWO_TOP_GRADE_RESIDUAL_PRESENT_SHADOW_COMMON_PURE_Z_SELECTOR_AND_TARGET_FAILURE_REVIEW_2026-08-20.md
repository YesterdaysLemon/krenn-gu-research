# Hostile review: maximum-root surplus-two residual-present top shadow and common pure-Z selector

Date: 2026-08-20

Global Krenn--Gu status: **UNRESOLVED**

## Reviewed artifacts

This review covers the LF-normalized contents with SHA-256 hashes

```text
185b7425f67fe09d21f5c99bca7edd4660bf1e8c22833b25fe3bff1c1880c41c
  claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_TOP_GRADE_RESIDUAL_PRESENT_SHADOW_COMMON_PURE_Z_SELECTOR_AND_TARGET_FAILURE_THEOREM.md

7a9acb5c9ce24551cc789efbc0f58f531add59a16dcd0b2e443150f90c8b32ef
  claims/arbitrary-order/verify_maximal_root_surplus_two_top_grade_residual_present_shadow_common_pure_z_selector_and_target_failure.py

4ba7859bd9f1b39ae7730cce0a08767510ff07d1cfc96879955978298fc0eab0
  claims/arbitrary-order/audit_maximal_root_surplus_two_top_grade_residual_present_shadow_common_pure_z_selector_and_target_failure.py
```

The theorem is proposed as `GLS19`.  Its load-bearing inputs are GLS2's grade
rule and maximum-root vanishing, GLD15's exact individual-`Z` nuisance and
complete target equation, GLS5's all-rank Fitting method, and GLD16 only for
the final conditional four-root detector.

## Verdict

**PASS for the `t`-open-root grade cutoff, explicit residual-present top
tensor, legal common pure-`Z` selector consequence, complete-target response
coupling, and all-rank geometric failure profile.**  The argument is
pointwise and denominator-free through the module theorem, and its Fitting
form retains every exceptional residual/rank-drop fibre.

**FAIL as top-survival forcing, simultaneous pure-`M`/pure-`Z` failure
exclusion, response activity, foreign transport, GLS8 integration, or
strategic-node closure.**  No such claim is made.  This theorem adds the
second synchronized projective axis and an exact failure system; it does not
show that any useful top shadow exists on every witness.

## Adversarial attacks

1. **Leaving `t` roots open kills every grade-`t` term.**  Rejected.  A
   grade-`t` matching survives exactly when each of its `t` disjoint root
   edges has one open and one closed endpoint.  The closed endpoints form an
   injection `A -> R-A`, giving formula (14).

2. **A surviving top matching may contain an edge internal to `A`.**
   Rejected.  Such an edge consumes two open roots, leaving only `t-2` open
   roots for the other `t-1` disjoint edges.  At least one edge would then be
   closed--closed and vanish at the maximum root.

3. **Formula (14) misses assignment multiplicities.**  Rejected.  After the
   injection, exactly `r-2t=|C|` closed roots remain, and `Per_(tau;C)` is the
   full bijection sum to the labelled complement ports.  The primary compares
   exact matching/assignment signatures; the independent audit verifies the
   falling-factorial count.

4. **Grades above `t` can survive because an open root meets several edges.**
   Rejected.  Matching edges are vertex-disjoint.  Each open root meets at
   most one, so `t` open roots cannot cover more than `t` root edges.

5. **The residual-absent `M` column is silently killed by the top shadow.**
   False and explicitly rejected.  Its grade is `t-1` and it generally
   survives.  GLD15 proves that the individual-`Z` nuisance is exactly
   `N_S^J+K g_S^M`; GLS19 deliberately includes its shadow in
   `N_(A,S)^Ztop`.

6. **Survival gives separate `Z` attachment at joint rank one without
   controlling `M`.**  Rejected.  The quotient functional annihilates both
   the complete joint nuisance and `g_S^M`, so its coefficient row is exactly
   `(0,1)`.  This is the one-target GLD15 quotient, not a separation inferred
   from joint rank alone.

7. **Top survival forces joint rank one.**  False and not claimed.  At rank
   one it orients the line to pure `Z`; at rank two the whole coefficient
   plane contains the same pure-`Z` row.

8. **Different target functionals prevent synchronization.**  Rejected.
   The functionals may vary with the target, but every supplied coefficient
   vector is `(0,1)` in the same physical `M/Z` plane.  That is precisely the
   coefficient synchronization used by GLD16.

9. **All displayed top classes swallowed implies no pure-`Z` functional.**
   False and not claimed.  The safe direction is absence of pure `Z` implies
   all top classes are swallowed.  A full-module functional can remain
   invisible in every displayed partial-root shadow.

10. **The target identity assumes `Z_S` is already diagonal.**  Rejected.  It
    is obtained by applying the induced quotient to the complete GLD15
    equation.  If the top class is nonzero, comparison itself forces all mixed
    coordinates of `Z_S` to vanish.  The independent audit enumerates five
    labelled output words, including two mixed controls.

11. **Response zero is confused with lack of a legal operator.**  Rejected.
    `Z_S=0` swallows the three displayed pure top classes through the witness
    equation, but the theorem does not infer that the full operator space
    lacks `(0,1)`.

12. **The Fitting criterion omits nuisance-rank drops.**  Rejected.  It ranges
    over every minor size.  The `j`-minor comparison detects rank rise exactly
    on the nuisance-rank-`j-1` fibre, and their union includes rank zero and
    every exceptional drop.

13. **The radical containment direction is reversed.**  Rejected.  Emptiness
    requires `V(I_j(B))` to lie inside `V(I_j([B|D]))`, hence
    `I_j([B|D]) subset sqrt_geom(I_j(B))`.

14. **A response/activity ideal can be replaced by the product of its
    coordinates.**  False and explicitly rejected.  At least one active
    coordinate is a union of principal opens; every generator must be checked
    separately.

15. **Finite-family usefulness may choose a different residual contraction
    per target.**  Rejected.  Every incidence component uses one shared
    Laurent point; the finite choice is only which root subset `A_S` exposes
    the target.

16. **At four roots the absorbed pure columns fill the whole top space.**
    False.  They span dimension three inside dimension 27 for a pair target
    and inside dimension nine for the four-port target.  No fullness claim is
    made.

17. **The four-port top tensor has a third matching term.**  Rejected.  With
    two open and two closed roots, survival requires a perfect bipartite
    matching.  There are exactly two.  The internal-open/internal-closed
    perfect matching vanishes because its closed--closed edge is evaluated at
    the maximum root.

18. **Pure `Z` leaves an untreated divisor `h=0` in GLD16.**  Rejected.  Its
    effective scalar is `a=h`.  GLD16's polynomial identity treats both
    branches: `h=0` gives the three-active rank contradiction, while `h!=0`
    gives the nine-word mixed detector.  Activity remains load-bearing.

19. **Nonzero selected responses imply three-colour pair-depth activity.**
    False and not claimed.  Activity requires particular complementary pure
    pair entries for all three colours at one port.  Seven nonzero tensors do
    not establish it.

20. **The new chart is the promoted GLS8 module.**  False.  GLS19 stays in the
    original `r`-root, `r`-port chart and uses the adjacent labels
    `S,Q union S`.  GLS8 has two probe roots and a distinct promoted target.

## Independence assessment

The primary verifier represents matchings as explicit edge tuples and outside
assignments.  It compares the top survivors with a separately generated
injection formula through root order seven, checks 92,742 exact top/lower
signatures, rational quotient/response ranks, 625 minor tables, and both
four-root formulas.

The independent audit imports no project or primary code.  It recursively
enumerates unoriented bitmask matchings through root order eight, proves the
top monomial count `(r-t)!`, uses primitive integer projective lines, exhausts
78,125 five-word target equations and 93,750 gated affine finite-field point
sets, and derives the two four-port cross-matchings from bipartite bitmasks.
This is a genuinely different bounded derivation and representation.

## Exact remaining boundary

GLS18 and GLS19 now give two synchronized axis routes on the same original
fixed-`Q` chart.  A useful leading shadow supplies pure `M`; a useful top
shadow supplies pure `Z`.  Each route has an exact response-gated all-rank
failure profile.  What remains is to force a sufficient target family onto
one common axis at one shared residual point, or to contradict simultaneous
failure of both profiles with complete mixed GHZ coefficients.  Oblique and
unequal lines, activity, GLS15 foreign transport, and GLS8 source integration
remain independent obligations.

No permanent restriction, extraction/gluing, or global-resolution statement
follows.  The global conjecture remains **UNRESOLVED**.
