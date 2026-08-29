# Hostile review: one-`T_0` single-binary activity localization and transverse full-deck sharpness

## Verdict

**PASS after two load-bearing repairs, for the stated localization and
sharpness boundary.**  `GLS72` is accepted as an exact
characteristic-zero refinement of the Family-A `r=1` single-binary key.

The accepted conclusions are:

- activity at the rank-two `T_0` port must be defined by its whole row
  covector, not by one presumed `e_0` scalar;
- the unique-source-pair strict-parent coefficients nevertheless make all
  direction-appropriate `E/F/G` selectors legal;
- the all-three-active cell is empty;
- a one-silent source cannot be silent at either `R_0` port;
- with the `T_0` port silent, every `alpha!=0` branch and the
  `alpha=0,ab!=0` branch are empty;
- the remaining `alpha=a=b=0` branch is not excluded: one common physical
  edge array realizes every selector, attachment, zero-triangle, and full
  deck equation used in the argument; and
- no typed profile is removed, so the live six-deficient residual remains
  `98,355` profiles in `81` keys.

The theorem does not prove that the displayed control extends to every
open-set source coefficient or to a complete graph witness.  Family A
`r=1,2,3`, Family B `r=3`, every pure/zero-triangle profile, both
five-deficient residuals, all other frontier branches, and the global
Krenn--Gu conjecture remain **OPEN / UNRESOLVED**.

## Artifacts reviewed

- [`GLS72` theorem](../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_SIX_DEFICIENT_ONE_T0_SINGLE_BINARY_ACTIVITY_LOCALIZATION_AND_TRANSVERSE_FULL_DECK_SHARPNESS_THEOREM.md)
- [primary verifier](../../claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_six_deficient_one_t0_single_binary_activity_localization_and_transverse_full_deck_sharpness.py)
- [independent audit](../../claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_six_deficient_one_t0_single_binary_activity_localization_and_transverse_full_deck_sharpness.py)
- [`GLS71` parent theorem](../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_SIX_DEFICIENT_SINGLE_BINARY_STRICT_PARENT_EDGE_CHART_AND_ATTACHMENT_ACTIVITY_THEOREM.md)
- [`GLS70` taxonomy](../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_SIX_DEFICIENT_BINARY_TRIANGLE_PARENT_TAXONOMY_AND_PROPER_FACE_DECK_KERNEL_THEOREM.md)

## 1. Scope repair: no false key removal

The first draft tried to remove the complete Family-A `r=1` key and claimed

```text
98,355 / 81 -> 97,275 / 80.
```

That claim was false.  The draft's `alpha=0` split treated exactly one of
`a,b` being zero but silently omitted `a=b=0`.  On the omitted branch, the
leading `Y_5,Z_5` kernel coordinates both vanish and the two attachments
decouple:

```text
u_3L_4+L_3u_4=lambda X,
v_3L_4+L_3v_4=mu Y.
```

These equations are compatible.  More importantly, vanishing of the
restricted `W_15,W_25` coordinates on `K_5` says nothing about their
transverse values at `e_(5,0)`.  The initial attempted repair tried to infer
such a transport and was rejected.

This does not invalidate `GLS71` Theorem 6.3.  A separate hostile objection
there initially confused the restricted factors `beta_5,delta_5` with the
off-kernel factors in its full coefficient (64a).  The decisive re-audit
showed that `F_45` and `G_35` instead kill the unrestricted central scalars
`U_00=[e_(0,0)e_(1,0)]W_01` and
`V_00=[e_(0,0)e_(2,0)]W_02`: after the restricted beta/delta terms vanish,
the nonzero decks `B_45,B_35` force `U_00=V_00=0`.  Every arbitrary
off-kernel factor in (64a) is therefore multiplied by zero.  `GLS72` uses
that valid parent contradiction only when the silent port is `R_0`; its
silent-`T_0` sharpness branch has different surviving central data and is
not covered by that argument.

The final theorem retains `alpha=a=b=0` as an open cell and leaves the
profile/key census unchanged.  Both independent programs reproduce

```text
post-GLS72 residual:             98,355 / 81,
Family A r=1 localized:          1,080 / 1 key,
profiles removed by GLS72:             0.
```

## 2. Whole-row activity at a `T_0` port

A second hostile pass caught that `GLS71` equation (25) was written only
for `R_0` ports, whose row is `K e_0`.  A `T_0` port has a two-dimensional
row plane

```text
row J=Ann(K)=K e_0 direct-sum K r.
```

Thus its `P_0,Q_0` coefficients need not be pure multiples of `e_0`.  The
final Lemma 0.1 repairs this without choosing a line in that plane.  It
defines whole row covectors

```text
P_u=[P_0]p_u,              Q_u=[Q_0]q_u.
```

For `P_u!=0`, the `P_0Q_2` and `P_0Q_1` coefficients of the strict parent
on `T union {u}` have the unique source pairs `{0,u}` and `{2,u}`.  Their
mixed target coefficients are zero, so tensoring by any nonzero `P_u`
forces the corresponding `E` and `F` decks to vanish.  The `Q_u` argument
uses the unique pairs `{0,u}` and `{1,u}` and forces `E/G`.  No purity of
the activity covector is used.

If one port `s` is silent, silence means `P_s=Q_s=0` as whole covectors.
The full `P_0Q_0` coefficient has one active pair and factors as

```text
(P_v tensor Q_w+Q_v tensor P_w) tensor H_(012s)
 =mu_0 e_0^tensor6.
```

Both factors are therefore pure across that cut, and at least one nonzero
crossed summand supplies the required mixed selector pair.  This validates
the activity fork, the silent-`R_0` transfer, and the silent-`T_0` selector
table at source level.

## 3. All-active and silent-`R_0` cells

The alternating argument still gives `A=alpha e_1e_2`.  On `D(alpha)`, put
`k_5=a z,l_5=b z`.  The two pure attachment matrices at the two `R_0`
ports are

```text
[[b,a],[a,0]],              [[0,b],[b,a]].
```

Rank-one targets force `a=b=0`, contradicting their nonzero values.  For
`alpha=0`, the independent/proportional/one-sided split is exhaustive.  Two
doubly active ports give a rank-one/rank-two flattening contradiction at an
`R_0` port; three ratios contradict characteristic zero; the remaining
supports kill one attachment.

If the silent port is `R_0`, its target lines remain independent, and the
active `R_0/T_0` pair still has independent products `x_Rz_T,y_Rz_T`.
Every use of independence in `GLS71` equations (53)--(64a) survives after
putting `x_T=y_T=z_T`.  In particular the projected attachment words still
kill the four scalar parameters, while the `alpha=0` flattening is taken at
the silent `R_0` port.  The complete `GLS71` full-deck contradiction
therefore transfers legally.

## 4. Silent-`T_0` excluded branches

With the silent port at `5`, write

```text
B_45=L_4z,              B_35=L_3z,
u_5=az,                 v_5=bz.
```

For `alpha!=0,ab!=0`, set `p_i=bu_i,q_i=av_i`.  The difference of the two
attachments is a nonzero diagonal rank-two tensor, so `p_i,q_i` are bases.
The two zero-central attachment matrices have determinants

```text
-4(d/b)^2,                    -4(c/a)^2.
```

Rank comparison gives `d=r=c=s=0`; the remaining `E` coordinate gives
`t=0`, and `F/G` kill the full central multipliers of the arbitrary
off-kernel coefficients.

At an endpoint, say `a!=0,b=0`, `L_i` lies on the `y_i` line.  The delta
equation has a nonzero `X` coefficient outside the tangent space at `Y`,
forcing `d=r=0`; the beta equation similarly gives `c=s=0`.  If the one
remaining full central scalar is nonzero, the selectors and restricted
full deck give

```text
aV_02+alpha c_0=2alpha c_0!=0,
```

contradicting the zero restriction of the pure `e_(5,0)` target.  The other
endpoint is symmetric with the same legal selector pair.

For `alpha=0,ab!=0`, the two attachments give a rank-two difference and
sum.  The delta and beta equations reduce to

```text
2rbL_3L_4=ad mu Y,
2saL_3L_4=bc lambda X.
```

If either side were nonzero, the attachment difference would lie in the
tangent space at `Y` or `X` while retaining the opposite diagonal
coefficient.  Hence all central parameters vanish and the full coefficient
is zero.  Exactly one of `a,b` being nonzero kills one attachment.

## 5. Exact transverse sharpness control

On `alpha=a=b=0`, the final theorem gives one explicit common edge array.
The primary verifier enumerates its physical perfect matchings rather than
checking independently chosen decks.  Exact expansion gives

```text
E_45=E_35=F_45=G_35=0,
H_(1345)|=e_(1,1)x_3x_4z,
H_(2345)|=e_(2,2)y_3y_4z,
H_(0345)|=0,
H_(0125)=e_(0,0)e_(1,0)e_(2,0)e_(5,0).
```

The cancellation in `F_45` uses the same `W_01,W_05,W_14,W_45` edges as
the rest of the array.  The nonzero full deck comes from

```text
W_01W_25,
W_25=e_(2,0)e_(5,0),
```

whose restriction to `K_5` is zero.  This is exactly the transverse
source-integrability obstruction claimed by the theorem.  It is not a full
source: the remaining endpoint-map coefficients and open-set equations are
not asserted.

## 6. Computational evidence

At review time the primary rational verifier and no-import modular audit
both pass.  They independently reproduce the census and check:

- the all-active determinant identities;
- both silent-`T_0` central determinant identities;
- an exact `alpha=0,ab!=0` restricted control;
- the tangent-space support exclusions;
- the endpoint characteristic-zero sign identity; and
- the surviving `alpha=a=b=0` full/restricted common-edge control.

The selector provenance, whole-row activity factorization, alternating
argument, exhaustive support splits, and silent-`R_0` transfer remain
written mathematics.

## Final scope

`GLS72` is a genuine top-down localization, but it closes no type-profile
key.  Its useful output is the exact first transverse coefficient that the
kernel-only strict parents cannot see.  The next Family-A `r=1` theorem must
derive another legal same-source coefficient involving `e_(5,0)` or prove a
source-integrability transport law.  Repeating proper-face restrictions on
`K_5` cannot exclude the displayed control.
