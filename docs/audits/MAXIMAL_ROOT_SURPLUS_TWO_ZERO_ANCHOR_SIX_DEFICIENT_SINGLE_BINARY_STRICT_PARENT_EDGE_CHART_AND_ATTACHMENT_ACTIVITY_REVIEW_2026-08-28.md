# Hostile review: six-deficient single-binary strict-parent edge chart and attachment activity

## Verdict

**PASS, after scope and degeneracy repairs.**  `GLS71` is accepted as an
exact characteristic-zero same-source parent theorem on the zero-anchor,
root-order-three, all-six-rigid, six-deficient branch.

The accepted conclusions are:

- Family B `S_0^3R_0^(3-r)T_0^r` is empty for `r=0,1,2`;
- Family A at `r=0` has the stated crossed pair/triangle normalization;
- its three-active-selector cell is empty;
- in its one-silent cell, the full missing-colour coefficient and the two
  activity-specific strict-parent selectors are incompatible, so the
  complete Family-A `r=0` key is empty;
- the four removed keys contain exactly `420+360=780` labelled profiles;
  and
- the live six-deficient residual is therefore `98,355` profiles in `81`
  keys.

This does not close Family A `r=1,2,3`, the all-`T_0` Family B `r=3` key,
any pure/zero-triangle profile, either five-deficient residual, another
deficient-count branch, the unique-nonrigid branch, arbitrary root order,
nonzero anchor, or the global conjecture.  The global Krenn--Gu conjecture
remains **UNRESOLVED**.

## Artifacts reviewed

- [`GLS71` theorem](../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_SIX_DEFICIENT_SINGLE_BINARY_STRICT_PARENT_EDGE_CHART_AND_ATTACHMENT_ACTIVITY_THEOREM.md)
- [primary verifier](../../claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_six_deficient_single_binary_strict_parent_edge_chart_and_attachment_activity.py)
- [independent audit](../../claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_six_deficient_single_binary_strict_parent_edge_chart_and_attachment_activity.py)
- [`GLS70` parent taxonomy](../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_SIX_DEFICIENT_BINARY_TRIANGLE_PARENT_TAXONOMY_AND_PROPER_FACE_DECK_KERNEL_THEOREM.md)
- [`GLS69` open-set hierarchy](../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_FIVE_SIX_DEFICIENT_OPEN_SET_SUPPORT_TOWER_AND_OVERLAP_INTEGRABILITY_BOUNDARY_THEOREM.md)
- [decomposable `P_3` classification](../../claims/p3/restrictions/P3_DECOMPOSABLE_RESTRICTION_CLASSIFICATION.md)

## 1. Independent census replay

The primary object/set implementation and the no-import integer-mask audit
independently reproduce

```text
531,441 -> 276,750 -> 99,855 -> 99,180,
```

followed by the `GLS70` pair-class removal

```text
99,180 / 86 -> 99,135 / 85.
```

Both recover the eight single-binary keys with counts

```text
Family A: 360, 1,080, 1,080, 360 for r=0,1,2,3;
Family B:  60,   180,   180,  60 for r=0,1,2,3.
```

Deleting Family B `r<=2` and Family A `r=0` gives

```text
99,135 / 85 -> 98,355 / 81.
```

The surviving single-binary stratum is exactly `2,580` profiles in four
keys: Family A `r=1,2,3` and Family B `r=3`.

## 2. Family B strict-parent quotient

For `r<=2`, choose an outside `R_0` port.  Its strict four-open parent is an
actual member of the `GLS69` hierarchy.  Quotienting that port by its
rank-one row kills every incident source pair and preserves two independent
target-coordinate classes.  Taking those coordinates gives two pure `P_3`
equations with:

- the same old-probe shores `p_i(P),q_i(Q)`;
- different components of the same physical decks; and
- deck rows independent of the old probes.

The review found no illicit division by a physical edge and no replacement
of one physical deck by independently chosen tensors.

## 3. Six-edge and endpoint audit

At each triangle mode, the joint shore rank is two.  The accepted
decomposable-`P_3` classification excludes a zero source column, generic
shore collinearity, and local rank three.  Therefore

```text
h_i=a_i p_i+b_i q_i.
```

In the local binary bases, only the six weight-one/weight-two cube
coefficients can be nonzero.  A nonzero decomposable tensor with corners
`000,111` zero lies on one of the six oriented edges, including a one-vertex
endpoint when one edge coefficient vanishes.  The theorem's representative
edge formulas replay exactly over `Q` and independently over `F_101`.

On a nonendpoint, transverse coefficient separation and
`K(P) intersection K(Q)=K` force one common `P` form and one common `Q`
form.  Unique factorization identifies them with the target forms.  At an
endpoint, one whole shore and one selected form on the other shore are
fixed.  Every pairing for two independent target colours conflicts on at
least one common or selected form.  Thus the Family-B exclusion is complete
for `r<=2`.  The quotient at `r=3` is one-dimensional and does not satisfy
this hypothesis; that key remains open.

The review changed “exactly one alternative” to “at least one”: an endpoint
can accidentally satisfy a stronger common-form description.  This is a
presentation correction, not a change to the exhaustive chart cover.

## 4. Family A crossed normalization and activity

Expanding the two coordinates of the common `S_0` label turns the two pure
pair equations into four separated old-probe equations.  If all four
rank-one endpoint scalars were nonzero, the two zero equations would make
the two diagonal expressions proportional, contradicting their independent
target monomials.  One zero endpoint scalar propagates to the crossed normal
form; the other possibility is its probe exchange.

The binary triangle then has complementary rows

```text
d_0=0,       d_1 on e_1,       d_2 on e_2.
```

For outside activity sets `A_P,A_Q`, the pure missing-colour coefficient
requires a crossed active pair, hence at least two active ports.  If all
three ports lie in `A_P union A_Q`, the strict parents legally supply all
three `E` decks.  They are not inferred from target shape alone.

## 5. Three-selector obstruction

Alternating the three `Y E` equations kills the symmetric `YYZ` terms and
forces the first factor of `A=W_12` onto `e_1`.  The symmetric `Z E`
calculation forces its second factor onto `e_2`, so

```text
A=alpha e_1 tensor e_2.
```

For `alpha!=0`, elimination gives the two exact cubic tensors in the
theorem.  Their pure flattenings force the local `k,l` pairs to be
independent, then force `k_4,k_5` onto the `x` lines and `l_4,l_5` onto the
`y` lines.  The remaining mixed coefficient would have to be zero but is a
sum of two independent words.

For `alpha=0`, the pair equations exhaust independent, doubly active,
one-sided, and zero supports.  A one-sided port cannot coexist with a
doubly active or opposite one-sided port.  Two doubly active ports give a
rank-one/rank-two flattening contradiction, and three ratios contradict
characteristic zero.  Thus the full-union activity cell is empty.

## 6. Reduced two-E control and its scope

The displayed array on `{1,2,3,4,5}` is one common restricted physical edge
array.  Exact expansion gives

```text
E_45=E_35=0,       E_34!=0,
H_(1O)=-2e_1x_3x_4x_5,
H_(2O)=-2e_2y_3y_4y_5.
```

It is not a six-label GHZ witness, does not enforce the activity-specific
`H_01/H_02` selectors, and does not realize the full pure `H_(012s)` deck.
The review therefore replaced the broader phrase “physically realizable”
with “realizable by one common restricted physical edge array.”  Its role is
sharpness: the reduced two-E attachment subsystem alone is compatible.

## 7. One-silent full-parent exclusion

Let `5` be silent and `3,4` active.  The nonzero coefficient

```text
c_34=a_3b_4+b_3a_4
```

has a nonzero ordered summand.  For `a_3b_4!=0`, exact strict-parent
coefficient separation gives

| activity | monomial | selector |
|---|---|---|
| `a_3` | `P_0Q_2` | `E_45=H_(1245)|_(K_4K_5)=0` |
| `a_3` | `P_0Q_1` | `F_45=H_(0145)|_(K_4K_5)=0` |
| `b_4` | `P_1Q_0` | `E_35=H_(1235)|_(K_3K_5)=0` |
| `b_4` | `P_2Q_0` | `G_35=H_(0235)|_(K_3K_5)=0` |

The other ordered summand is obtained by exchanging active labels `3,4`.

Project the two `E` equations to the attachment target coordinates and put
`alpha=[e_1e_2]A`.  For `alpha!=0`, eliminating `B_45,B_35` gives two
equations with one common tensor `C`.  Independence at port `5` forces the
crossed form, including every nonzero scalar stratum.  The zero central
coordinates of the two attachments then kill the four remaining parameters
`r,s,q,tau`, and the `e_0e_0` part of an `E` equation kills `A_00`.

For `alpha=0`, independent, zero, and proportional `u_5,v_5` are exhaustive.
The proportional case makes a rank-one separated term equal the sum of the
two independent target cubes.  Hence `u_5=v_5=0`.  The remaining projected
`E` equations force `r=s=0`, then the nonzero attachments force the silent
central projections to vanish, and the two `B` decks force `A_00=0`.

The hostile audit caught an omitted zero stratum in the last factor step.
It is repaired explicitly: if exactly one of `beta_3,beta_4` is nonzero,
its equation forces `B_45=0` or `B_35=0`, already impossible; if both are
nonzero, the two decks share one `K_5` factor, incompatible with the
independent attachment targets.  The same split applies to `delta_3,delta_4`.

The legal selectors now kill the pure coefficients of `W_01,W_02`, while
`A_00=0` kills the third matching.  Therefore

```text
[e_0^tensor4]H_(0125)=0,
```

without restricting the off-kernel parts of `W_15,W_25`.  This contradicts
the nonzero pure full deck isolated by the missing-colour coefficient.  The
one-silent cell, and hence the complete Family-A `r=0` key, is empty.

One hostile pass briefly raised the off-kernel `e_(5,0)` values as a possible
gap, then withdrew the objection after expanding the selectors.  The proof
does not infer those values from `K_5`: `F_45,G_35` instead kill the full
central-edge scalars `W_01[e_0,e_0]` and `W_02[e_0,e_0]`, which multiply the
arbitrary off-kernel values in the first two terms.  The third term vanishes
because `A_00=0`.

## 8. Replays and evidence boundary

Run from repository root:

```powershell
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_six_deficient_single_binary_strict_parent_edge_chart_and_attachment_activity.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_six_deficient_single_binary_strict_parent_edge_chart_and_attachment_activity.py
python -m py_compile claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_six_deficient_single_binary_strict_parent_edge_chart_and_attachment_activity.py claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_six_deficient_single_binary_strict_parent_edge_chart_and_attachment_activity.py
```

At review time all commands pass.  The programs audit the independent finite
census, six-edge coefficients, endpoint supports, displayed attachment
identities, projection ranks, and restricted control.  The function-field
intersection, UFD step, same-source selector provenance, alternating proof,
and exhaustive tensor-factor cases remain written mathematics.

## Final scope

`GLS71` is a genuine top-down same-source closure of four complete
single-binary type-profile keys.  It does not establish source integrability
for the surviving profiles and is not a resolution audit.  The smallest
remaining single-binary work is Family A `r=1,2,3` and the all-`T_0` Family B
`r=3`; pure/zero triangles and both five-deficient branches require separate
parent arguments.
