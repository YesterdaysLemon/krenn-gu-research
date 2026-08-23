# Hostile review: zero-anchor three-effective-label uncontracted complementary-deck separation

## Verdict

**ACCEPT after exact source-interface reconstruction, focused symbolic replay,
genuinely independent no-import audit, and three hostile derivations.**

`GLS52` excludes the conditional one-residual/two-port rank-seven normal form
left by `GLS51`.  The same uncontracted physical deck complementary to the
two ports is forced by two off-common-coordinate diagonal rows to equal two
distinct pure inactive-port words.  Together with `GLS49` and the three-port
part of `GLS51`, the entire exactly-three-effective-label zero-anchor full-
swallow target locus is empty.  `GLS48` therefore raises the pointwise
activity floor to four.

This is not source-to-full-swallow coverage or a legal attachment theorem.
Four-or-more labels and every source/response/selector/synchronization gate
remain open.  The strategic node and global Krenn--Gu conjecture remain
**UNRESOLVED**.

## Reviewed artifacts

- [`GLS52 theorem`](../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_THREE_EFFECTIVE_LABEL_UNCONTRACTED_COMPLEMENTARY_DECK_TWO_COLOUR_SEPARATION_EXCLUSION_THEOREM.md)
- [`focused exact primary verifier`](../../claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_three_effective_label_uncontracted_complementary_deck_two_colour_separation_exclusion.py)
- [`independent no-import audit`](../../claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_three_effective_label_uncontracted_complementary_deck_two_colour_separation_exclusion.py)
- owning interfaces `GLS21`, `GLS36`, `GLS39`, `GLS48`, `GLS49`, and `GLS51`
- the current-frontier, supply/target DAG, and arbitrary-order README updates.

The three hostile reviews used different routes.  The first reconstructed
every raw label before inactive-port contraction.  The second projected the
full equation directly at the two pure off-coordinate port inputs.  The
third varied the inactive-port contraction over the dense product torus and
recovered the same raw deck factorization by multilinearity.  All three
agreed on the contradiction and its exact boundary.

## Complete raw-label audit

At the fixed residual point suppose

```text
Act={q_s,u,v}.
```

For every inactive promoted label `x`, both whole-domain maps `X_x,Y_x`
vanish.  Hence the root companion of every pair incident with `x` is zero.
For the other residual label `q_(1-s)`, both evaluated shore vectors vanish,
so every pair companion incident with it is zero and the residual-pair
coefficient `q` is zero.  The top coefficient is `omega=0`.

Therefore the exact fixed-residual equation before any inactive promoted
port is evaluated contains precisely

```text
{q_s,u},       {q_s,v},       {u,v}.
```

Put `I=Uhat-{u,v}`.  In the notation of the theorem, the third deck is
literally

```text
h_uv=H_(Bhat-{u,v})(z_Q,-_I)
     in tensor_(x in I) V_x^*.
```

It is not an arbitrary rowwise coefficient.  Evaluating every `I` port at
`1=e_0+e_1+e_2` gives the single scalar `gamma=h_uv(1_I)` used by GLS51.
Since `|Uhat|=2r-2`, one has `|I|=2r-4>=2`.

## Common-coordinate and projection audit

GLS51 is applied only after the exact all-ones contraction.  Its determinant
identity forces a common coordinate `c`, nonzero `gamma`, and residual shores

```text
a,b in K e_c.
```

Consequently every residual--port coefficient lies in

```text
e_c tensor K^3+K^3 tensor e_c
```

before or after inactive-port contraction.  The coefficient rows selecting
`E_ii` and `E_jj`, where `{i,j}` is the complement of `{c}`, kill those
terms identically.  This conclusion uses the fixed residual shore vectors,
not the evaluated deck covectors, and therefore does not require extending a
generic deck-line statement off the all-ones point.

The contracted row equations are

```text
gamma rho_i(M_uv)=alpha_i e_i^* tensor e_i^*,
gamma rho_j(M_uv)=alpha_j e_j^* tensor e_j^*.
```

The full rows are the same left factors tensored with `h_uv`, while the
target right factors are the pure inactive words `t_i,t_j`.  Substitution
gives

```text
h_uv=gamma t_i,          h_uv=gamma t_j.
```

No value of `u` or `v` is divided out: the equality follows by cancellation
of a nonzero pure tensor factor in a tensor product over a field.  The target
coefficients and `gamma` are pointwise nonzero consequences already stated
in the owning theorem.  Since `I` is nonempty, `t_i,t_j` are linearly
independent.  This is the contradiction.

## Independent torus derivation

As a separate check, contract the inactive ports at any tuple whose three
coordinates are all nonzero.  The target remains fully supported and `Act`
is unchanged.  GLS51 applies at every such point.  Its common coordinate is
fixed because the residual products `a_d b_d` do not depend on the inactive
ports and exactly one is nonzero.  Thus both evaluated residual--port decks
vanish on either off-coordinate input throughout the product torus.
Characteristic zero makes that torus Zariski dense, so multilinearity gives
the same raw row isolation.  The two pure target fibres again force `h_uv`
onto two distinct pure word lines.

This derivation is corroborating only; the written proof needs just the
all-ones GLS51 conclusion and the exact uncontracted equation.

## Why contracted principal-deck identities are insufficient

The hostile reconstruction also checked the tempting Jacobi/Wick route.
For the odd internal set left after removing `q_s,u,v`, pointed hafnian
recurrence expresses `gamma,lambda_u,lambda_v` through one cofactor vector.
Choosing one internal vertex and a fixed matching on the remaining inactive
ports realizes arbitrary prescribed contracted `gamma,lambda_u,lambda_v` by
the three incident edge rows.  Probe-incidence edges are disjoint parameters.

Thus the GLS51 contracted control can be made a literal same-graph
principal-deck control at one contraction.  It still fails the full target,
because one uncontracted `h_uv` cannot carry both off-coordinate pure words.
The load-bearing new information is the common uncontracted target deck, not
a polynomial identity among the three contracted observables.  No existence
claim about a full target point or hypothetical witness follows from that
control.

## Computational independence

The SymPy primary enumerates the complete live raw-label set, symbolically
checks that the two off-coordinate diagonal rows annihilate the whole common
star, verifies pure-word independence for inactive sets of several sizes,
and replays the two isolated rows of the exact GLS51 rank-seven control.  It
also confirms that all-ones contraction sends both incompatible pure words
to the same scalar, explaining why GLS51 alone could not see the conflict.

The no-import audit shares no project code or algebra package.  It uses
direct rational `3 by 3` matrices and sparse dictionaries keyed by inactive
colour words.  Evaluating the two forced deck identities at the all-`i` word
makes one demand `gamma` and the other zero.  The audit repeats this for
inactive lengths one through eight and independently reconstructs the live
pair-label census.  The written proof carries the arbitrary-root result.

## Required replay

```text
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_three_effective_label_uncontracted_complementary_deck_two_colour_separation_exclusion.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_three_effective_label_uncontracted_complementary_deck_two_colour_separation_exclusion.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_three_effective_label_shared_polarization_rank_seven_normal_form_and_other_rank_exclusion.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_three_effective_label_shared_polarization_rank_seven_normal_form_and_other_rank_exclusion.py
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

The theorem excludes only exactly three effective labels inside the
zero-anchor fully swallowed fixed-residual target locus.  Four-or-more labels
can contribute several pair maps to the same off-coordinate target rows, so
the one-deck separation argument does not extend by counting alone.

Source-to-full-swallow coverage, raw escape, nonzero anchor, all response/
selector/activity/synchronization/nuisance-survival/target-anchor gates,
strategic-node closure, permanent restriction, extraction/gluing, and global
resolution remain open.
