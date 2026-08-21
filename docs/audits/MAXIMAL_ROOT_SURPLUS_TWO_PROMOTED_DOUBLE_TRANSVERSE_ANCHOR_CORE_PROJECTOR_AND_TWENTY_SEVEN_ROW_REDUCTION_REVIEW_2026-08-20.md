# Maximum-root surplus-two promoted double-transverse anchor-core hostile review -- 2026-08-20

## Verdict

**PASS for the exact double-transverse projector, `27/4` factor-through modules, and conditional root-order-three detector edge.  Strategic node closure remains OPEN.**

The theorem correctly uses the retained all-port tensor `q` and its nonzero
root evaluation `p` to construct a denominator-free scaled projector from the
eight-dimensional transverse probe-root space onto the four-dimensional
double-transverse core.  On the nonzero double-transverse anchor branch,
exterior multiplication by the anchor has a three-dimensional image and
produces exact physical `27`-row pair modules.  The top target cannot use that
exterior quotient because its desired tensor is the anchor; its separate core
image has four rows and desired coefficient `p^2 omega`.

Survival in a reduced module supplies a legal full selector through that
factorization.  Failure in a reduced module does not imply failure in the full
module.  No survival, response, activity, or witness exclusion is claimed
outside the stated conditional `r=3` leaf.  The global conjecture remains
**UNRESOLVED**.

## Scope audited

The review checked

- [`GLS25` owning theorem](../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_DOUBLE_TRANSVERSE_ANCHOR_CORE_PROJECTOR_AND_TWENTY_SEVEN_ROW_REDUCTION_THEOREM.md);
- [`GLS22` transverse projector and target identity](../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_ALL_PORT_TRANSVERSE_QUOTIENT_AND_PROJECTIVE_SYNCHRONIZATION_FAILURE_THEOREM.md);
- [`GLS23` exact physical nuisance](../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_TRANSVERSE_COMPLETE_NUISANCE_DECOMPOSITION_AND_TOP_ANCHOR_DICHOTOMY_THEOREM.md);
- [`GLS24` anchor-marginal trichotomy](../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_ONE_PROBE_ANCHOR_MARGINAL_NINE_ROW_REDUCTION_AND_DOUBLE_TRANSVERSE_BOUNDARY_THEOREM.md);
- [`GLD3` attachment/activity contract](../../claims/arbitrary-order/TWO_RESIDUAL_PAIR_FOUR_PORT_DIAGONAL_INTERFERENCE_AND_CAMOUFLAGE_BOUNDARY_THEOREM.md);
- the focused exact primary verifier; and
- the independent standard-library no-import audit.

No external literature claim is used.

## Load-bearing identities

Let

```text
s_0=q(-,x_(a_1)),       s_1=q(x_(a_0),-),
s_0(x_(a_0))=s_1(x_(a_1))=p!=0.
```

For transverse `v`, define

```text
Xi_Q(v)=p v-s_0 tensor rho_0(v)-rho_1(v) tensor s_1.
```

Both actual-root marginals of this tensor vanish.  On the double-transverse
core, both correction terms vanish and `Xi_Q=p id`.  Consequently its image
is the whole four-space, its kernel is the direct sum of the two marginal
two-spaces, and `Xi_Q^2=p Xi_Q`.

On branch `0!=omega in E_A^dbl`, the map

```text
chi_Q(v)=omega wedge Xi_Q(v)
```

has rank three and kills `omega`.  Applied label by label to the exact `GLS23`
nuisance, it gives the complete pair-target image.  Applied without the wedge,
`Xi_Q` gives the complete top-target core image and sends
`t_empty=p omega` to `p^2 omega`.

## Hostile assertions

1. **The construction divides by `p`.**  False.  The proofs may describe the
   induced splitting on `D(p)`, but every load-bearing formula uses `Xi_Q` and
   the scaled identity `Xi_Q^2=pXi_Q`.

2. **The two partial tensors `s_0,s_1` may lie in the annihilators.**  False.
   Their evaluations at the actual roots are both `p!=0`.

3. **The correction formula does not land in the double-transverse core.**
   False.  Contracting either probe root cancels the first two relevant terms;
   the remaining marginal vanishes because `v` is transverse.

4. **The core image may be proper.**  False.  `Xi_Q` restricts to `p id` on
   the whole core.

5. **The two kernel summands intersect.**  False.  A nonzero intersection
   would make `s_i` proportional to an annihilator covector, contradicting its
   nonzero root evaluation.

6. **Scaled idempotence holds only after choosing coordinates.**  False.  Once
   the image is in the core, applying `Xi_Q` again multiplies it by `p`.

7. **The theorem applies to a nonzero anchor with a nonzero actual-root
   marginal.**  It could algebraically, but its declared branch is the
   complementary `GLS24` double-transverse branch.  The branch partition is
   preserved rather than conflated.

8. **A nonzero core anchor always has matrix rank one.**  False.  The core is
   `2 x 2`; rank one and rank two are both retained.

9. **Exterior multiplication by the anchor has rank four.**  False.  On a
   four-space its kernel is the anchor line, so its rank is three.

10. **The pair module has 36 rows.**  The unwedged core would.  Quotienting the
    already-nuisance anchor line by exterior multiplication gives exactly
    `3*9=27` rows.

11. **The pair exterior map may be used for the top target.**  False.  It would
    kill the desired anchor.  The theorem uses the unwedged four-row core map
    for the top target.

12. **The top desired coefficient is `p omega`.**  Before the new core map it
    is.  Applying `Xi_Q` multiplies the core anchor by another `p`, giving
    `p^2 omega`.

13. **The exact pair nuisance omits the top label without justification.**
    False.  That label is exactly the anchor nuisance and is killed by
    `omega wedge Xi_Q(omega)=0`.

14. **The top nuisance should contain the top label.**  False.  At the top
    target that label is desired, exactly as in `GLS23`.

15. **An unwanted pair label is silently discarded.**  False.  Every active
    `D!=C` is retained; `D=Q` was already zero after the GLS22 projection.

16. **Port coefficient slicing may not commute with the core maps.**  False.
    The new maps act only on the disjoint probe-root factor.

17. **Reduced survival is an unrestricted recovery statement.**  False.  A
    reduced separating functional pulls back to a constant decomposable
    coefficient selector annihilating every labelled nuisance operator.

18. **Reduced failure proves full absorption.**  False and explicitly
    disclaimed for both pair and top targets.

19. **Raw nonzero `27`-row aggregate proves quotient survival.**  False.  It
    gives only one raw nonzero summand; the complete reduced nuisance may
    absorb every such summand.

20. **Vanishing of the aggregate is termwise synchronization.**  False.  It
    puts only the core-projected aggregate on the anchor line.  Termwise
    synchronization is stated separately.

21. **The radical--Fitting criterion selects a generic minor.**  False.  It
    quantifies over all ranks and uses geometric radical containments with the
    common `hp` gate.

22. **The `r=3` pair and top modules automatically satisfy `GLD3`.**  False.
    All six reduced pair ranks, the separate top rank, and three-colour
    activity are explicit hypotheses.

23. **The 27 coefficient rows are the nine output words of `GLD3`.**  False.
    They are a selector module.  The existing detector exposes its separate
    nine mixed response coefficients only after legal attachment and activity.

24. **GLS24 and GLS25 exhaust full nonzero-anchor selector failure.**  False.
    They exhaust bounded factor-through routes on the anchor branches, not all
    possible full selectors.

25. **The arbitrary-root response depths now enter a named detector.**  False.
    Only the `r=3` shapes match `GLD3`; `r>=4` remains open.

26. **The strategic node is closed.**  False.  No theorem here forces a
    reduced useful row or excludes its failure profile.

## Verification independence

The primary verifier uses exact SymPy matrices at fully supported root
vectors.  It constructs `Xi_Q` from a physical `q`, checks the exact
image/kernel, scaled idempotence, both anchor ranks, the exterior quotient,
slice commutation, `72/63/27` and `8/4` dimensions, rank-rise examples,
aggregate synchronization, and the `r=3` response count.

The audit imports neither SymPy nor repository code.  It uses `Fraction`
arithmetic, a hand-written Gaussian rank and exact solve routine, independently
chosen root and `q` data, explicit annihilator/core bases, direct tensor
slicing, and a separate response-complement enumeration.

Both pass.  The arbitrary-root content is the written coordinate-free
projector and labelled-operator proof.

## Open boundary

The nonzero anchor is now covered by bounded physical factor-through tests,
but no test is forced to survive.  The next proof must use complete mixed GHZ
equations to exclude the simultaneous reduced/full Fitting failures, zero
anchor, top absorption, response zero, and low activity, or derive a different
named downstream package.  Generic core rank is insufficient.

Strategic node: **OPEN**.  Global conjecture: **UNRESOLVED**.
