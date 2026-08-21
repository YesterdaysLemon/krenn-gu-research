# Hostile review: maximum-root surplus-two partial-root grade shadow and common pure-M selector

Date: 2026-08-20

Global Krenn--Gu status: **UNRESOLVED**

## Reviewed artifacts

The review covers the LF-normalized contents with SHA-256 hashes

```text
6b2d16e06b5959cb34122853208fe94094b0abc5683153588abf7a34ac797072
  claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_PARTIAL_ROOT_GRADE_SHADOW_AND_COMMON_PURE_M_SELECTOR_THEOREM.md

ee7581d331fb455f45e54019675b81fc0b871184e159f9c27e7b8c9336c61282
  claims/arbitrary-order/verify_maximal_root_surplus_two_partial_root_grade_shadow_and_common_pure_m_selector.py

1487e8fed4cc044c18f876a19ab1a82f7cc344f13fcb85a0d6d0b1f4cf2cfb43
  claims/arbitrary-order/audit_maximal_root_surplus_two_partial_root_grade_shadow_and_common_pure_m_selector.py
```

The theorem is proposed as `GLS17`.  It depends on GLS2 and the complete
GLD15 quotient; GLS16 is its `t=1` specialization.  Its four-root conditional
detector consequence invokes GLD16 without altering any GLD16 gate.

## Verdict

**PASS for the arbitrary-grade partial-root cutoff, explicit leading tensor,
complete lower-grade nuisance shadow, and common pure-`M` operator
consequence.**  The proof is pointwise and denominator-free.  It gives a new
four-port synchronization gate at root order four and extends the same
filtration to every nonempty even target in the original fixed-`Q` chart.

**FAIL as survival forcing, response activity, foreign transport membership,
GLS8 integration, or strategic-node closure.**  No such claim is made.  The
theorem gives a sufficient leading-survival condition and a necessary
all-leading-swallowed condition when pure `M` is absent.  Those leading
classes may all be swallowed on an actual witness unless a further complete
mixed-target argument excludes that branch.

## Adversarial attacks

1. **Leaving `t-1` roots open might allow a grade-`t` matching to survive by
   using one open root in several root edges.**  Rejected.  Root--root edges
   in a matching are vertex-disjoint.  Each open root meets at most one such
   edge, so `t-1` open roots can cover at most `t-1` of the `t` edges.  One
   edge remains evaluated at `(x_i,x_j)` and vanishes.

2. **A grade-`t-1` survivor may contain an edge internal to the open set.**
   Rejected.  Such an edge consumes two of the `t-1` open roots, leaving only
   `t-3` open roots to meet the remaining `t-2` disjoint edges.  At least one
   of those edges is then closed--closed and vanishes.  Every surviving edge
   has exactly one open endpoint.

3. **Formula (13) overcounts a root matching by orienting its edges.**
   Rejected.  Each surviving edge has a unique endpoint in `A`, so it has a
   unique orientation `a -> tau(a)`.  The partners are distinct because the
   edges form a matching.  The remaining root-to-outside bijection is also
   unique.  The primary signature comparison checks equality as sets, not
   merely counts.

4. **Formula (13) misses a factor from the two residual assignments.**
   Rejected.  Those assignments are part of the permanent
   `Per_(tau;Q,C)`.  At `r=4,t=2`, each of three closed-root partners leaves
   two assignments to `Q`, producing exactly six monomials for each open
   root in both audits.

5. **The partial-root shadow kills every nuisance label, making the quotient
   artificially strong.**  Rejected.  It kills only grades at least `t`.
   All labels of order `2,...,2t`, including every lower grade and every
   other order-`2t` label, remain in the exact shadow.  Only the desired label
   `S` is removed by the joint quotient definition.

6. **The residual-present desired label is improperly counted as nuisance.**
   Rejected.  `I=Q union S` is removed from the joint nuisance.  Independently,
   it has order `2t+2` and its grade-`t` companion is killed by the partial-
   root contraction, so including it would not change the shadow.

7. **GLD15 was stated initially with four roots, so the operator-rank
   trichotomy is unavailable at arbitrary `r,S`.**  Rejected.  GLS17 defines
   the complete joint nuisance and coefficient space directly.  The equality
   between operator-space rank and the span of the two quotient classes is
   the transpose of `(u,v) |-> u bar g_M+v bar g_Z`; it is finite-dimensional
   linear algebra independent of root or target count.  The written theorem
   includes this derivation explicitly.

8. **Leading survival forces joint rank one.**  False and not claimed.  It
   excludes rank zero.  At rank one it orients the line to pure `M`; at rank
   two the whole coefficient plane is available.

9. **Rank-two targets obstruct a common projective row.**  Rejected.  A
   rank-two operator space is all of `K^2` and contains `(1,0)`.  Therefore a
   family of rank-one pure-`M` and rank-two targets still has common
   coefficient direction `(1,0)`.

10. **Different target functionals violate synchronization.**  Rejected.
    GLD16 synchronizes the coefficient direction in the common `M/Z` plane;
    its target functionals may vary.  Corollary 2.1 keeps the graph, `Q`,
    contraction, and coefficient direction fixed while allowing the legal
    functional to depend on the target, exactly as GLD15 permits.

11. **A legal pure-`M` operator forces a nonzero physical response.**  False
    and explicitly rejected.  The output is `M_S=H_S`, target-diagonal on a
    witness, but may vanish.  Nonzero response and three-colour activity stay
    separate.

12. **All leading classes swallowed implies no pure-`M` selector.**  False and
    not claimed.  The proved direction is
    `(1,0) notin C_S => b_(A,S)=0 for every A`.  The converse may fail because
    a full-module functional can exist even when every displayed shadow is
    swallowed.

13. **The four-port first-root covector is a generic jet requiring a
    denominator or deformation.**  Rejected.  It is the literal partial
    contraction of the same physical companion tensor, leaving one labelled
    root slot open.  No deformation, derivative, incidence inverse, or minor
    is used.

14. **The four-root seven-target branch is excluded without activity.**
    False.  GLS17 supplies only the common pure-`M` legal package under the
    seven leading-survival gates.  The final contradiction is imported from
    GLD16 only under GLD16's unchanged three-colour pair-depth activity.

15. **The residual scalar `h` creates an exceptional divisor in the pure-`M`
    branch.**  Rejected.  For `(delta,eta)=(1,0)`, GLD16's effective scalar is
    `a=delta+h eta=1` for every `h`.  Activity remains load-bearing, but no
    `h` divisor remains in this conditional branch.

16. **The theorem integrates the GLS8 promoted targets.**  False.  GLS17
    concerns adjacent residual-absent/present labels `S,Q union S` in the
    original `r`-root, `r`-port surplus-two chart.  GLS8 has two probe roots,
    `2r-2` promoted ports, a top-minus-two desired label, and no adjacent
    residual-absent label of the required order.

17. **Finite enumeration proves arbitrary-root exhaustiveness.**  False.  The
    arbitrary-root proof is the disjoint-edge covering argument, the matching
    bijection in (13), the exact labelled nuisance definition, and quotient
    duality.  The bounded scripts independently audit conventions and counts.

## Independence assessment

The primary verifier constructs root partial matchings as explicit edge tuples,
attaches all outside permutations, and compares the surviving signature set
with a separately generated injection/permanent formula through root order
seven.  It additionally checks exact grade survivor profiles and rational
projective ranks.

The independent audit imports no project or primary code.  It represents
vertices and edges by bitmasks, recursively enumerates unoriented matching
masks through order eight, proves the survivor count by a falling-factorial
transversal formula, and uses primitive integer projective lines plus explicit
coefficient-space intersections.  This is a genuinely different derivation
and representation for the bounded identities.

## Exact remaining boundary

At every even target `|S|=2t`, absence of a pure-`M` operator now forces the
finite family of exact absorptions

```text
b_(A,S)=0,             A in binom(R,t-1).
```

At `r=4`, failure of the conditional seven-row synchronization route is
therefore localized to at least one swallowed pair base class, all four
swallowed four-port first-root classes, or the separate GLD16 activity/rank/
response branches.  Excluding those absorptions requires complete mixed GHZ
coefficients on the same graph.  The theorem supplies no permanent
restriction and authorizes no extraction/gluing or global-resolution claim.
