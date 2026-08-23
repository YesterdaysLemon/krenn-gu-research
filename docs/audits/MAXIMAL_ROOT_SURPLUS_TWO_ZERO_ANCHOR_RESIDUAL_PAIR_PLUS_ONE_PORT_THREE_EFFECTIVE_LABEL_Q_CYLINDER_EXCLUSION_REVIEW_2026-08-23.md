# Hostile review: zero-anchor residual-pair-plus-one-port three-effective-label q-cylinder exclusion

## Verdict

**ACCEPT after exact proof audit, independent quotient census, owning-interface
reconstruction, and hostile scope review.**  The `GLS49` proof excludes every
fully supported fixed-residual zero-anchor
target point on `D(p)` with exactly three effective `GLS39` auxiliary labels.
Combined with `GLS48`, the pointwise `D(p)` activity floor is four.

The theorem excludes the displayed support even at `p=0`, but not the other
three-label types then possible, four-or-more labels, ranks five through
nine, raw escape, or any source/selector/response/synchronization/nuisance/
anchor/receiver branch.  The scalar `p` is a root-deck coefficient
evaluation, not a physical response.  The strategic node and global
Krenn--Gu conjecture remain **UNRESOLVED**.

## Reviewed artifacts

- [`GLS49 theorem`](../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_RESIDUAL_PAIR_PLUS_ONE_PORT_THREE_EFFECTIVE_LABEL_Q_CYLINDER_EXCLUSION_THEOREM.md)
- [`focused exact primary verifier`](../../claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_residual_pair_plus_one_port_three_effective_label_q_cylinder_exclusion.py)
- [`independent no-import audit`](../../claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_residual_pair_plus_one_port_three_effective_label_q_cylinder_exclusion.py)
- owning interfaces `GLS8`, `GLS21`, `GLS23`, `GLS35`, `GLS36`, `GLS39`,
  and `GLS48`
- the current-frontier, supply/target DAG, and arbitrary-order README updates.

Three read-only attacks were used.  One derived the `q`-cylinder proof, one
independently reconstructed the quotient and both shore orientations, and one
attacked possible determinant/cut strengthenings.  Unretained attack ideas
are not proof evidence and no claim about them is used in this package.

## Support and raw-label audit

On `D(p)`, `q!=0`.  If residual auxiliary label `q_s` were ineffective, both
of its factors `a_s,b_s` would be zero, which kills both terms in

```text
q=a_0 tensor b_1+a_1 tensor b_0.
```

Thus both residual labels are active.  There is only one possible type of
three-label support: `Q disjoint-union {u}`.

The cut argument actually excludes that support even if `q=0`: then the
source has only the two `G_s` left generators, while the target has three
independent left columns.  The `D(p)` premise is used only to show that every
three-element support must have this residual-pair-plus-one-port type.

Across `(A union {u})|(Uhat-{u})`, the complete raw labels are exactly `Q`,
`{q_0,u}`, and `{q_1,u}`.  Labels involving an ineffective endpoint have
zero root coefficient, and `omega=0` removes the top term.  The `Q` deck may
be arbitrarily entangled across `u` and the opposite shore; this enlarges its
left column space only to the complete cylinder `Kq tensor V_u^*`.  Each
residual--port label contributes one fixed left tensor `G_s` times an
arbitrary right deck.  Therefore

```text
col(source) subset K G_0+K G_1+(Kq tensor V_u^*).
```

No deck is assumed nonzero.  Zero, proportional, or cancelling decks only
shrink this space.

The opposite shore has `2r-3>=3` promoted ports.  Its three constant-colour
target words are independent and every residual-torus scalar is nonzero, so
all three left target columns `d_i=r_i tensor e_i^*` lie in the displayed
source space.

## Quotient audit

A relation among the target columns modulo the `q`-cylinder is

```text
sum_i gamma_i r_i tensor e_i^*=q tensor ell.
```

Evaluating the port at `e_k` gives `gamma_k r_k=ell(e_k)q`.  For nonzero `q`
off the three pure diagonal lines, every scalar vanishes and the quotient
rank is three.  If `q` lies on `Kr_j`, precisely `d_j` dies and the quotient
rank is two.  The two residual--port generators have quotient span at most
two; target containment therefore forces `q` pure.

This step uses the full `q`-cylinder.  Replacing it by one selected `Q` deck
would be unjustified, while deleting it would incorrectly strengthen the
source quotient.  No response or cylinder basis is selected.

## Residual-shore audit

Write `q=A C^T`, with `A=[a_0|a_1]` and `C=[b_1|b_0]`.  Pure nonzero `q` has
rank one.  If both `A` and `C` had rank two, `C^T` would be surjective and
`A` injective, so their composition would have rank two.  Hence one shore has
rank at most one.

Suppose first `rank A<=1` and `q` is on `Kr_j`.  Nonzero `q` gives

```text
span(a_0,a_1)=Ke_j,          e_j in span(b_0,b_1).
```

Represent either other target column by `G_0,G_1` and the `q`-cylinder.
Projection of the first probe factor away from `e_j` kills the residual-left
and cylinder terms and leaves

```text
(P_j X(z)) tensor B_i=e_i^*(z)e_i tensor e_i,
B_i in span(b_0,b_1).
```

At `z=e_i`, simple-tensor equality forces `B_i` onto the nonzero line `Ke_i`.
The two colours different from `j`, together with the already present
`e_j`, put three independent vectors in `span(b_0,b_1)`, a contradiction.
Transposition gives the same contradiction when `rank C<=1`.

The review checked rank-zero residual shores as well: they are impossible
because `q!=0`.  No hidden full-rank minor, shore normalization, or algebraic-
closure point is used.

## Computational independence

The SymPy primary enumerates the four minimal support placements, constructs
the exact `27`-coordinate cylinders and target columns, checks quotient rank
two on all three pure `q` lines and rank three on nine non-pure hostile
representatives, and symbolically verifies that a `3 by 2` shore times a
`2 by 3` coefficient matrix has zero determinant.

The no-import audit shares no primary code or algebra package.  It implements
projective normalization and Gaussian elimination over `F_3`, exhausts all
`9,841` projective lines in the nine-dimensional root coefficient space, and
finds quotient dimension two for exactly the three pure lines and dimension
three for the remaining `9,838`.  It separately enumerates the four support
placements and every pure-`q`-conditioned two-column residual shore in both
orientations, checking that none contains the other two coordinate axes.
This is independent finite corroboration; the written proof carries the
characteristic-zero statement.

## Required replay

```text
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_residual_pair_plus_one_port_three_effective_label_q_cylinder_exclusion.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_residual_pair_plus_one_port_three_effective_label_q_cylinder_exclusion.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_two_effective_label_adaptive_cut_pure_target_exclusion.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_two_effective_label_adaptive_cut_pure_target_exclusion.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_incidence_image_common_row_silence_and_labelwise_lift_sharpness.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_incidence_image_common_row_silence_and_labelwise_lift_sharpness.py
```

The package must still pass full candidate-tree validation, exact-head hosted
CI, safe merge, and fresh merged-main replay before publication is complete.

## Unresolved boundary

The theorem is an activity-floor exclusion, not a legal attachment theorem.
On `D(p)`, four or more effective labels leave at least three non-cylinder
left generators, so the quotient-dimension contradiction no longer follows.
On `p=0`, the residual labels need not be active and other three-label types
can support exact rank-five incidence families; the complete physical target
still has to be used.  These cells, ranks six through nine, raw escape,
nonzero anchor, source coverage, every downstream gate, strategic closure,
and global resolution remain open.
