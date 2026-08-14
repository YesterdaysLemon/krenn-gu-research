# Self-review: same-colour `(2,2,3)` rank-four/rank-eight complete exclusion

Date: 2026-08-13

Claim reviewed:
[same-missing-colour third-row-rank-three complete exclusion](../../claims/arbitrary-order/BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_SAME_MISSING_COLOUR_THIRD_ROW_RANK_THREE_COMPLETE_EXCLUSION_THEOREM.md).

## Verdict

The stated characteristic-zero `(2,2,3)` exclusion is supported.  The new
argument closes exactly the injective-third-row continuation of S2BR's
same-missing-colour involved-row cell.  It does not close the mixed or
injective involved-row profiles, other derivative ranks, other physical
components, higher orders, or the global conjecture.

## Load-bearing checks

### 1. Is the correction expansion complete?

Yes.  Third-row rank three makes `ker(pr_3|K)` one-dimensional.  The known
derivative syzygy already occupies that kernel, so three graph lifts over
`e_d,e_s,e_t` complement it in `K`.  Their derivative images are therefore
a basis of `U`.  The expansion `G_N-J=sum S_c U_c` loses no singleton
direction.

### 2. Do the two missing rows determine all three source coefficients?

Yes.  First-`d` contraction of every `U_c` is exactly
`kappa e_d tensor e_c`; the tangent contribution vanishes because all first
components of `K` and `x` lie in `e_d^perp`.  The three last-root coordinate
vectors are independent, forcing `S_d=-kappa^(-1)T_d` and `S_s=S_t=0`.
No selected source slice or generic specialization is substituted for the
complete identity.

### 3. Is the tensor-rank contradiction pointwise legitimate?

Yes.  If the remaining `T_d` root coefficient is nonzero, its product with
the two complementary coordinate products is a nonzero polynomial.  An
infinite characteristic-zero field supplies one simultaneous nonzero root
evaluation.  The resulting three-term diagonal has all flattening ranks
three.  Hence all three local maps from `P_3` are invertible and preserve its
tensor rank four, contradicting diagonal rank three.  The verifier replays
the four-cube upper decomposition, the no-rank-one slice lower certificate,
and all flattenings exactly.

### 4. Does the binary-frame obstruction apply to shifted planes?

Yes.  The inherited S2BF lemma is an abstract characteristic-zero tensor
obstruction; it does not require the middle plane or its basis to arise from
a new physical derivative.  Since `q_d` is a common zero of `R x P`, adding
any multiple of it to either binary third row preserves every one of the
eight table entries and both nonzero target tensors.

### 5. Is pairwise transversality proved rather than assumed?

Yes.  If any two binary row planes met, their sum would fit in a three-space.
The remaining two-plane necessarily meets that three-space in the ambient
four-space.  This is precisely S2BF's intersecting-middle-plane forbidden
configuration.  Symmetry of the polarized permanent covers all three plane
pairs.

### 6. Is the shift trap exhaustive?

Yes.  A two-plane meets the three-plane `Q` in a line.  Disjointness from
`Q_0` makes the line unique and gives it a nonzero `q_d` coefficient.  If
either binary coefficient is nonzero, one linear equation chooses a shifted
plane containing the line, contradicting transversality.  The only remaining
line is `span(q_d)`.  Applying this to both involved planes puts the nonzero
`q_d` in their zero intersection.

## Verification independence

The primary replay uses SymPy matrices and dense tensors.  The audit imports
no repository module and no third-party package; it reverses tensor indices,
uses a separate sparse tensor representation and `Fraction` elimination,
and independently checks every one- and two-supported rational shift mask.
Both scripts replay identities and rank interfaces.  The infinite-field
evaluation and inherited S2BF case exhaustion remain written mathematics,
as stated in the theorem.

## Status boundary

```text
same-colour (2,2,3) cell:                           IMPOSSIBLE;
complete same-colour (2,2,q) involved-row profile: CLOSED;
mixed / injective involved-row profiles:            OPEN;
other lower-rank cells, components, poles, higher m: OPEN;
global Krenn--Gu conjecture:                         UNRESOLVED.
```
