# Maximum-root surplus-two promoted base-shadow all-port collapse hostile review -- 2026-08-20

## Verdict

**PASS for the exact arbitrary-root no-go.  The strategic node remains OPEN.**

The theorem correctly identifies one complete `GLS8` nuisance label that was
not exploited in `GLS20`: for a source target `S_C=Uhat-C`, the complement pair
`D=Q` gives the residual-absent all-port input `H_Uhat`.  Maximum-root
contraction turns its coefficient into `p_(A,Q)`, so its coefficient slices
are `p I_9`.  On the mandatory `p!=0` source gate, the base nuisance is all of
`V_C^*` for every source pair.

This closes only the factor-through maximum-root base-shadow route.  It does
not prove absorption in the full `81`-dimensional promoted quotient and does
not exclude upstairs selectors, responses, or a witness.  Global status is
**UNRESOLVED**.

## Scope audited

The review checked

- [`GLS21` owning theorem](../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_BASE_SHADOW_ALL_PORT_NUISANCE_COLLAPSE_THEOREM.md);
- [`GLS8` complete promoted module](../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_TWO_PROBE_ONE_TARGET_ATTACHMENT_AND_POINTWISE_FAILURE_REDUCTION_THEOREM.md);
- [`GLS20` base quotient](../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_SOURCE_ALIGNED_BASE_SHADOW_AND_TARGET_FAILURE_THEOREM.md);
- the focused primary verifier; and
- the independent standard-library no-import audit.

No external literature claim is used.

## Exact derivation

The promoted identity contains, for every pair `D subset Bhat`,

```text
G_D^A tensor H_(Bhat-D).
```

For a source target with desired complement `C subset U`, `D=Q` is a distinct
active same-grade nuisance label and contributes

```text
G_Q^A tensor H_Uhat.
```

After `Q` evaluation this is `G_Q^A(z_Q)` times the identity on the all-port
input.  The source contraction obeys

```text
epsilon_A(G_Q^A(z_Q))=p_(A,Q)(z_Q).
```

Factoring `W_Uhat=V_C^* tensor W_(S_C)` and slicing the identity over the right
factor produces all nine vectors `p e_i` in the base nuisance.  Thus
`pV_C^* subset N_C^base`.  At `p!=0` the nuisance has rank nine and there is no
nonzero annihilator.

For every minor size `j`, the nuisance presentation contains a `pI_9` block,
so `p^j` is a `j`-minor and `p` belongs to the geometric radical of the
nuisance-minor ideal.  Every `GLS20` response-gated augmented minor is already
multiplied by `hp`, proving its Fitting containment automatically.

## Hostile assertions

1. **`D=Q` is not an active label.**  False.  Its deck complement has size
   `|Bhat-Q|=2r-2`, exactly the promoted active order.

2. **`D=Q` is the desired source label.**  False.  The desired complement is
   `C subset U`, disjoint from and unequal to `Q`.

3. **Residual-absent inputs may be omitted from the nuisance.**  False.  The
   legal `GLS8` module explicitly retains every active labelled summand.

4. **The all-port input supplies only one nuisance vector.**  False.  It is an
   arbitrary tensor input.  Coefficient slicing the identity over the target
   factor supplies all nine left coordinate vectors.

5. **The coefficient after contraction is merely proportional to `p`.**
   False.  By the owning GLS8 definition it is exactly `p_(A,Q)(z_Q)`.

6. **The proof silently divides by `p`.**  False.  The module inclusion
   `pV_C^* subset N_C^base` is polynomial.  Invertibility is used only for the
   explicitly stated pointwise corollary on `D(p)`.

7. **Exceptional nuisance-rank fibres survive on `D(p)`.**  False for this
   base quotient: `pI_9` has rank nine at every such point, independently of
   all other columns.

8. **A nonzero physical response repairs the base quotient.**  False.  The
   coefficient quotient is already zero before the response is considered.

9. **A legal factor-through selector can annihilate `pI_9`.**  False.  Its
   base functional must vanish on every coordinate, hence is zero and cannot
   normalize the desired coefficient.

10. **This contradicts GLS20.**  False.  GLS20 proved a conditional
    equivalence and an exact failure criterion; it did not prove that its base
    class survives.  GLS21 proves that the failure branch is universal on the
    source gate.

11. **This proves full `GLS8` absorption.**  False.  The implication from full
    absorption to base absorption is one-way.  A full selector may use probe-
    root covectors not factoring through `epsilon_A`.

12. **Deleting `H_Uhat` restores a legal selector.**  Irrelevant and illegal.
    Deleting the active nuisance label changes the target projection problem.

13. **The Laplace nuisance circuit contradicts `Pi_Q!=0`.**  False.  The
    nonzero source tensor is represented inside an explicit nuisance sum; no
    target equation makes that sum zero.

14. **The Fitting proof covers only full generic rank.**  False.  The
    polynomial `p^j` minor witnesses every radical containment before fibre
    specialization.

15. **The result supplies a downstream detector.**  False.  It is a route
    no-go.  Full upstairs selection, common-package gates, activity, and
    downstream shape remain open.

16. **The result changes the global conjecture status.**  False.  It neither
    proves nor refutes a witness and explicitly retains **UNRESOLVED**.

## Verification independence

The primary verifier uses exact SymPy operator/Kronecker matrices, symbolic
`pI_9` minors, and explicit coefficient slicing.  The audit imports no SymPy,
repository code, or primary-verifier functions; it reconstructs scalar
identity slices, ranks, and diagonal determinants with `Fraction` arithmetic
and a hand-written elimination routine.

Both pass.  The bounded scripts audit the implementation and edge cases; the
arbitrary-root result is the written label/operator proof.

## Corrected live boundary

Future work must not attempt to force `GLS20` base survival on the same
`p!=0` gate.  It must remain in the full `81`-row promoted quotient, find a
legal joint multi-target construction retaining the all-port label, or
contradict full upstairs failure with complete mixed GHZ coefficients.

Strategic node: **OPEN**.  Global conjecture: **UNRESOLVED**.
