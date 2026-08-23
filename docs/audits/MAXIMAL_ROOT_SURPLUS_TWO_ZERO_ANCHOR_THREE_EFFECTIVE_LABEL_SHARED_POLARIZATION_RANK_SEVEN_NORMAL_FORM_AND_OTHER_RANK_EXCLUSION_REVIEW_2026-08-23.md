# Hostile review: zero-anchor three-effective-label shared polarization and rank-seven normal form

## Verdict

**ACCEPT after owning-interface reconstruction, exact primary replay,
genuinely independent no-import audit, and three hostile mathematical
reviews.**

`GLS51` classifies the exactly-three-effective-label part of the zero-anchor
fully swallowed fixed-residual target locus pointwise in characteristic zero
and at arbitrary root order.  Two residual labels plus one port are excluded
by `GLS49`.  Three promoted ports are excluded by a deck-hyperplane reduction
to `GLS39`.  One residual plus two ports force a separated normal form whose
complete incidence image has rank exactly seven.

Thus exactly three effective labels can occur only in the one-residual,
two-port rank-seven normal form.  Existence is not asserted.  The exact
rational shared-interface control does not realize the displayed decks as
principal complementary permanents of one physical graph.  The strategic
node and global Krenn--Gu conjecture remain **UNRESOLVED**.

## Reviewed artifacts

- [`GLS51 theorem`](../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_THREE_EFFECTIVE_LABEL_SHARED_POLARIZATION_RANK_SEVEN_NORMAL_FORM_AND_OTHER_RANK_EXCLUSION_THEOREM.md)
- [`focused exact primary verifier`](../../claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_three_effective_label_shared_polarization_rank_seven_normal_form_and_other_rank_exclusion.py)
- [`independent no-import audit`](../../claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_three_effective_label_shared_polarization_rank_seven_normal_form_and_other_rank_exclusion.py)
- owning interfaces `GLS21`, `GLS36`, `GLS39`, and `GLS48`--`GLS50`
- the current-frontier, supply/target DAG, and arbitrary-order README updates.

Three read-only hostile attacks were separated by purpose.  One reconstructed
the arbitrary-root source interface and searched for a hidden rank-five
hypothesis.  One attacked the determinant, zero graph, crossed square,
injectivity, and both directions of the rank-seven image equality.  One
reconstructed the three-port deck-hyperplane restriction directly against
the exact `GLS39` hypotheses.  No attack found an omitted fibre or a stronger
conclusion than the owning equations support.

## Owning-interface and support audit

For every auxiliary label `t`, effectiveness means that at least one of the
whole-domain maps `X_t,Y_t` is nonzero.  The `GLS21` raw decomposition and
`GLS36` target equation therefore leave only pairs inside `Act`.  Evaluating
each inactive promoted port at `1=e_0+e_1+e_2` preserves all three nonzero
target coefficients and turns every surviving complementary deck into its
exact form or scalar.  It does not choose a nonzero deck fibre.

Exactly three labels have the exhaustive support counts

```text
two residuals and one port,
one residual and two ports,
three promoted ports.
```

`GLS49` excludes the first even when `q=0`.  In each other support at least
one residual label is ineffective, so both shore vectors of that label
vanish and `q=p=0`.  The contracted equations used by GLS51 are therefore
exact arbitrary-root consequences.  The rank-five assumption in GLS50 is
used only for its profile reduction; GLS51 repeats the nonzero-deck and
coordinate-cover proofs from the target equations and does not import that
rank hypothesis.

## One-residual determinant and coordinate-lock audit

The exact equation is

```text
G_u(z)lambda_v(w)+G_v(w)lambda_u(z)+gamma M_uv(z,w)
 =sum_c alpha_c z_c w_c r_c.
```

The same two-hyperplane argument as GLS50 forces `gamma!=0`, including zero
or proportional `lambda` fibres.  With

```text
Xtilde_t=gamma X_t+a lambda_t,
Ytilde_t=gamma Y_t+b lambda_t,
```

direct expansion gives the denominator-free shifted polarization.  Its
matrix value is a sum of two rank-one matrices.  Expanding its determinant
as a polynomial, without inverting a coordinate, gives one full diagonal
monomial plus the three rank-one correction cofactors.

If `a_c b_c!=0`, restriction to `z_c=0` forces `lambda_u` to vanish on that
whole coordinate hyperplane, and restriction to `w_c=0` does the same for
`lambda_v`.  At least one such product exists or the full diagonal monomial
cannot cancel.  Two cannot exist because one nonzero covector cannot occupy
two coordinate lines.  This proves the common coordinate deck and scalar
lock on every fibre; no minor or response is divided out.

## Zero graph, crossed square, and exact incidence rank

The four shifted vectors at the two off-deck colours are nonzero because
their matched polarizations are nonzero pure diagonal matrices.  If either
shifted deck-coordinate vector were nonzero, the unmatched zero graph on the
remaining nonzero vertices would be connected.  The exact zero-polarization
classification gives one broad type on that graph.  A one-sided type kills
the mandatory matched outputs; the two-sided type has a length-three path
between a matched pair and kills that output by sign propagation.  Hence both
deck-coordinate vectors vanish.

Their matched equation, together with the scalar lock, gives the full matrix
identity `a tensor b=a_c b_c r_c`; thus both residual shores are pure on the
common coordinate.  On the crossed square at the other two colours, the
two-sided/two-sided case makes the matched matrices proportional, a mixed
two-sided/one-sided case shares a nonzero factor between two distinct
diagonal lines, and equal one-sided types kill the outputs.  Only the two
transposed separated orientations survive.

Each original port joint map then has three independent coordinate values:
one X-only off-deck value, one Y-only off-deck value, and one nonzero
two-sided common-coordinate value.  The four residual--port images provide
the four independent off-diagonal star units modulo `Delta`, so the incidence
rank is at least seven.  Conversely, purity of the residual shores puts both
residual--port images in the diagonal-plus-star space, and the nonzero
`gamma` target equation puts the whole port-pair image there too.  Since
these are every effective raw pair image and `q=0`, `GLS36` gives equality
and rank exactly seven.

## Three-port deck-hyperplane audit

The three-port target quotient forces the three opposite deck lines to be
the coordinate-line permutation before any kernel or nuisance rank is
considered.  Put `H_t=ker lambda_t`.  Restricting the `uv` inputs to
`H_u times H_v` kills the other two source summands.  Choosing a `w` input
with nonzero `lambda_w` shows that the restricted `M_uv` image lies in
`Delta`; choosing the coordinate-two inputs shows that it contains `Kr_2`.
Cyclically the other restricted pair images contain `Kr_1` and `Kr_0`.

The restricted whole-domain maps `(X_t|H_t,Y_t|H_t)` are literal inputs to
`GLS39`: every distinct-label polarization lands in `Delta`, while their
combined image contains all three independent diagonal lines.  This
contradicts GLS39's characteristic-not-two rank-at-most-two theorem.  The
argument uses no joint-kernel profile, selected nonzero minor, nuisance-rank
hypothesis, or genericity condition.

## Computational independence

The SymPy primary expands the shifted identity and determinant over symbolic
rational matrices, replays the common-coordinate scalar lock, checks the
zero-graph connectivity and crossed-square type table, verifies all nine
coefficients of the exact rational rank-seven control, computes both port
joint ranks and the complete incidence rank, and checks the three
deck-hyperplane target colours.

The no-import audit shares no project code or algebra package.  It implements
the `3 by 3` determinant with custom sparse-polynomial arithmetic and obtains
the same full expression.  It enumerates all `364` projective joint-vector
classes over `F_3`, classifies every zero-polarization pair, and exhausts the
crossed-square constraints with two distinct pure diagonal outputs; only the
two separated orientations occur.  Separate `Fraction` matrices replay the
rank-seven control and custom Gaussian elimination computes both port ranks
and the seven-dimensional pair-image span.  The written proof, not the finite
field census, carries the characteristic-zero theorem.

## Required replay

```text
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_three_effective_label_shared_polarization_rank_seven_normal_form_and_other_rank_exclusion.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_three_effective_label_shared_polarization_rank_seven_normal_form_and_other_rank_exclusion.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_complete_pairwise_diagonal_family_rank_bound_and_minimal_raw_swallow_exclusion.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_complete_pairwise_diagonal_family_rank_bound_and_minimal_raw_swallow_exclusion.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_rank_five_three_effective_label_kernel_profile_and_mandatory_deck_reduction.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_rank_five_three_effective_label_kernel_profile_and_mandatory_deck_reduction.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_residual_pair_plus_one_port_three_effective_label_q_cylinder_exclusion.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_residual_pair_plus_one_port_three_effective_label_q_cylinder_exclusion.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_two_effective_label_adaptive_cut_pure_target_exclusion.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_two_effective_label_adaptive_cut_pure_target_exclusion.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_incidence_image_common_row_silence_and_labelwise_lift_sharpness.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_incidence_image_common_row_silence_and_labelwise_lift_sharpness.py
```

The package must still pass full candidate-tree validation, exact-head hosted
CI, safe merge, and fresh merged-main replay before publication is complete.

## Unresolved boundary and hostile no-go

The exact rational control proves that the rank-seven conclusion is sharp at
the contracted shared-`X/Y` interface.  It does not show that its deck
covectors and scalar are complementary principal permanents of one symmetric
edge matrix, nor that inactive-port all-ones evaluations lift to one complete
uncontracted target point.  Promoting it to an existence statement, witness,
or counterexample would be invalid.

The profile-by-profile kernel attack from GLS50 is now unnecessary for the
three-port branch; the deck-hyperplane reduction closes every profile at
once.  Conversely, further abstract shared-polarization algebra cannot by
itself exclude the retained rank-seven normal form because the exact control
satisfies that interface.  The smallest same-locus obligation is therefore
principal-deck physical compatibility, not another joint-kernel atlas.

Four-or-more effective labels at every rank, source-to-full-swallow coverage,
raw escape, nonzero anchor, every named response/selector/synchronization/
nuisance-survival/anchor gate, strategic-node closure, and global resolution
remain open.
