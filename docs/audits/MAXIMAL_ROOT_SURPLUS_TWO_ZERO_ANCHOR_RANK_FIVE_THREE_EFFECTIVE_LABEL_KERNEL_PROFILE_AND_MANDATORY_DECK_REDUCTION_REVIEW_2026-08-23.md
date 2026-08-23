# Hostile review: zero-anchor rank-five three-effective-label kernel profiles and mandatory decks

## Verdict

**ACCEPT after three independent derivations, owning-interface reconstruction,
exact primary replay, no-import finite audit, and hostile scope review.**

`GLS50` classifies the complete exactly-three-effective-label part of the
zero-anchor rank-five full-swallow target cell.  `GLS49` excludes the
two-residual support.  One residual plus two ports forces a nonzero evaluated
port-pair deck scalar and leaves profiles `(1,2,3)` and `(1,3,3)`.  Three
ports force the opposite-pair deck lines to be the three coordinate lines,
make every joint kernel at most one-dimensional, and leave profiles
`(2,2,3)`, `(2,3,3)`, and `(3,3,3)`.

The five profiles are reductions, not existence or exclusion theorems.  The
deck statements are contracted physical-deck consequences, not named
responses, legal selectors, or downstream synchronization gates.  The
strategic node and global Krenn--Gu conjecture remain **UNRESOLVED**.

## Reviewed artifacts

- [`GLS50 theorem`](../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_RANK_FIVE_THREE_EFFECTIVE_LABEL_KERNEL_PROFILE_AND_MANDATORY_DECK_REDUCTION_THEOREM.md)
- [`focused exact primary verifier`](../../claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_rank_five_three_effective_label_kernel_profile_and_mandatory_deck_reduction.py)
- [`independent no-import audit`](../../claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_rank_five_three_effective_label_kernel_profile_and_mandatory_deck_reduction.py)
- owning interfaces `GLS21`, `GLS36`, `GLS39`, `GLS48`, and `GLS49`
- the current-frontier, supply/target DAG, and arbitrary-order README updates.

Three read-only attacks were retained.  One used direct target-kernel
restriction, one independently used flattening rank and adaptive deck cuts,
and one reconstructed the full support cover and triple quotient.  They
agreed on the kernel profiles.  The third attack strengthened the three-port
result from mere deck nonvanishing to a complete coordinate-line
permutation.  Suggestions about excess rows alone were not used as proof.

## Owning-interface and support audit

For every promoted label `t`, the theorem uses the whole-domain joint kernel

```text
K_t=ker X_t intersect ker Y_t.
```

It does not select one value of `t`.  If a label is ineffective, both maps
vanish, so every pair coefficient incident with it vanishes.  The `GLS21`
raw pair-labelled decomposition and `GLS36` target equation therefore leave
only pairs inside the three-element effective support.

There are exactly three support types:

```text
two residuals plus one port,
one residual plus two ports,
three promoted ports.
```

`GLS49` excludes the first.  In either remaining type at least one residual
label is ineffective.  Both of its residual shore vectors vanish, hence
`q=0` and `p=epsilon_A(q)=0`.  This is why the new theorem is a `p=0`
successor rather than an extension of the `D(p)` argument.

The proof evaluates only inactive promoted ports at
`1=e_0+e_1+e_2`.  Every target pure word evaluates to one, preserving all
three nonzero residual-torus coefficients.  Every surviving raw physical
deck becomes exactly the scalar or covector shown in the theorem.  Zero,
proportional, and cancelling decks are retained; no contracted equation is
used in the reverse direction.

## One-residual/two-port audit

The exact consequence is

```text
G_u(z)lambda_v(w)+G_v(w)lambda_u(z)+gamma M_uv(z,w)
 =sum_c alpha_c z_c w_c r_c.
```

If `gamma=0`, restricting to `ker lambda_u x ker lambda_v` kills the source.
Independence of the `r_c` would make each coordinate product vanish on that
kernel product.  For a fixed colour this requires one deck form to be the
matching coordinate form.  Two projective lines cover at most two of the
three coordinate lines, including the cases where either deck form is zero.
Thus `gamma!=0`.  The review rejected wording that called `gamma` a physical
response: it is an evaluated complementary physical deck scalar.

On `K_u`, both pair coefficients incident with `u` vanish, leaving

```text
lambda_u(z)G_v(w)=sum_c alpha_c z_c w_c r_c.
```

The target slice is injective in `z`, so `lambda_u|K_u` is injective and
`dim K_u<=1`.  A nonzero kernel line puts the whole opposite tensor `G_v` in
`Delta`; it need not put it on one pure-colour line.  If both port kernels
were lines, both residual--port tensors would be diagonal, and the
nonzero-`gamma` equation would make `M_uv` diagonal too.  Then
`B_Q^anc subset Delta`, contradicting rank five.  This proves precisely the
two profiles stated, without a rank-open minor.

## Three-port deck and kernel audit

The contracted equation is

```text
M_uv lambda_w+M_uw lambda_v+M_vw lambda_u
 =sum_c alpha_c r_c e_c^u e_c^v e_c^w.
```

Select one diagonal root coefficient `r_c` and quotient all three port
covector spaces by the corresponding deck lines.  Every source term dies.
The target pure tensor dies only if at least one of the three deck lines is
`K e_c^*`.  This must hold for each colour.  Three slots can cover three
distinct coordinate lines only by a permutation, so all deck covectors are
nonzero and their lines are exactly the coordinate lines.  This conclusion
is independent of the kernel profile.

Restricting to `K_u` kills `M_uv` and `M_uw`, leaving the denominator-free
opposite-pair identity

```text
lambda_u(k_u)M_vw
 =sum_c alpha_c k_(u,c) r_c e_c^v e_c^w.
```

As above, the target slice is injective, `dim K_u<=1`, and a nonzero kernel
puts `im M_vw` in `Delta`.  If all three kernels were lines, all pair-map
images would lie in `Delta`, contradicting rank five.  This proves exactly
the three profiles in the theorem and no existence statement.

## Computational independence

The SymPy primary uses rational sparse matrices.  It checks that the one-
and two-opposite-port diagonal target-slice maps both have rank three,
enumerates the eight hostile assignments of three colours to two deck lines,
finds no cover, finds the six permutations in the three-line cover, and
replays both profile flags and the terminal diagonal-rank-three contradiction.

The no-import audit shares no primary code or algebra package.  It implements
projective normalization, kernels, and evaluation directly over `F_5`.  It
exhausts all `31` projective lines and zero forms; refutes all `1,024`
gamma-zero deck pairs by an explicit surviving target word; finds exactly six
triple deck covers; refutes all `1,024` dimension-at-least-two kernel/deck
pairs; and separately counts hostile and admissible kernel-line deck
evaluations.  This is independent finite corroboration.  The written proof
carries the characteristic-zero theorem.

## Required replay

```text
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

The theorem does not exclude the five surviving profiles.  An attack based
only on abstract excess-row/Koszul cancellation was rejected as a closure
route because it supplied no bridge to the shared `X/Y` polarization or to
principal decks of one physical graph.  No existence claim about that
exploratory interface is part of this package.  The next load-bearing step
must use the shared polarization, principal-deck coupling, or a stronger
same-graph target identity.

Four-or-more labels, ranks six through nine, source-to-full-swallow coverage,
raw escape, nonzero anchor, every downstream attachment gate, strategic-node
closure, and global resolution remain open.
