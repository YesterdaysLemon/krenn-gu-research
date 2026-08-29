# Hostile review: all-`T_0` Family-B nonendpoint full-parent boundary

## Verdict

**PASS for the stated central-mixed-support nonendpoint theorem.**  `GLS74`
excludes the nonendpoint outside pure-`P_3` chart of the last Family-B
single-binary key when, at each central `S_0` label, both probe shores have a
non-root coefficient.  The proof is exact in characteristic zero and uses
complete tensors on the common physical edge array.

This is not an exclusion of the Family-B `r=3` key.  A central shore may be
root-axis-only, and the outside pure-`P_3` equation may lie on a P-common or
Q-common endpoint.  Those charts remain open.  No typed profile is removed;
the inherited six-deficient residual remains `98,355 / 81`, and the global
Krenn--Gu conjecture remains **UNRESOLVED**.

## Artifacts reviewed

- [`GLS74` theorem](../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_SIX_DEFICIENT_ALL_T0_FAMILY_B_NONENDPOINT_FULL_PARENT_TRANSVERSE_INJECTIVITY_AND_ENDPOINT_ACTIVITY_BOUNDARY_THEOREM.md)
- [primary verifier](../../claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_six_deficient_all_t0_family_b_nonendpoint_full_parent_transverse_injectivity.py)
- [independent audit](../../claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_six_deficient_all_t0_family_b_nonendpoint_full_parent_transverse_injectivity.py)
- [`GLS71` strict-parent theorem](../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_SIX_DEFICIENT_SINGLE_BINARY_STRICT_PARENT_EDGE_CHART_AND_ATTACHMENT_ACTIVITY_THEOREM.md)
- [`GLS70` binary-triangle taxonomy](../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_SIX_DEFICIENT_BINARY_TRIANGLE_PARENT_TAXONOMY_AND_PROPER_FACE_DECK_KERNEL_THEOREM.md)

## 1. Rejected overclaim and repaired coefficient provenance

An earlier draft claimed the whole nonendpoint chart.  That was not legal:
for a fixed central label `i`, the `P_0Q_r` strict-parent coefficient supplies
the `U`-shore Koszul identity only when some `q_i^r`, `r=1,2`, is nonzero,
and the `P_rQ_0` coefficient supplies the `V`-shore identity only when some
`p_i^r` is nonzero.  The complete `P_0Q_0` row combines a missing identity
with the one-port corrections and cannot manufacture it separately.

The final theorem adds exactly the needed central mixed-support condition.
After contracting the other two central labels at their `S_0` colour-zero
kernels, each mixed coefficient has only the three source pairs joining `i`
to an outside label.  Outside--outside pairs have bidegree `P_0Q_0`, and a
pair meeting either contracted central label vanishes.  Retaining the `i`
slot gives a nonzero local covector tensored with the relevant outside sum;
tensor-factor cancellation is therefore legal and yields both complete
Koszul identities.  No scalar coordinate or physical edge is divided by.

## 2. Alternating camouflage and full-parent injectivity

For each central label, the two Koszul identities on the three full pair
decks have a one-dimensional common kernel.  In outside bases `(U_u,V_u)` it
is the alternating triple

```text
(U_4V_5-V_4U_5,
 V_3U_5-U_3V_5,
 U_3V_4-V_3U_4).
```

The full coefficient matrix has rank `26/27`.  Its alternating generator
vanishes after restricting both pair slots to their kernel lines, explaining
why the strict-parent kernel equations alone do not see it.

On a mixed central local word, the complete `P_0Q_0` coefficient also has
three one-port corrections.  The only triangle--outside nuisance terms are
the two Koszul sums and therefore vanish.  The remaining outside map

```text
(D_3,D_4,D_5) -> G_34D_5+G_35D_4+G_45D_3
```

is injective at a nonendpoint: transverse projection first puts each `D_u`
in `span(U_u,V_u)`, and the six binary coefficients then force all six row
coordinates to zero in characteristic zero.  Thus every full one-port
correction vanishes, not merely its kernel restriction.

## 3. Coupling back to the physical edges

Restricting the common physical edges to the three outside kernel lines gives
the central relation

```text
A_0 rho_0u+A_1 rho_1u+A_2 rho_2u=0
```

and, on each outside pair, three equations coupling the same scalar edge
`b_vw` to the cross-products of the `rho` rows.  The four support sizes of
`(A_0,A_1,A_2)` are exhaustive.

- With all three `A_i` nonzero, a nonzero `b_vw` forces the two endpoint
  ratios to be the distinct roots of `r^2+r+1`; the complementary outside
  column is zero and the other two `b` values vanish.  The full-parent
  one-port equation then kills the sole spoke that could use the surviving
  edge, so the binary triangle is zero.
- With exactly two nonzero `A_i`, the two surviving pair equations differ by
  a nonzero factor `2` and force every `b_vw` to vanish.
- With exactly one nonzero `A_i`, the corresponding full rows lie in the
  outside row planes.  The complete alternating forms for the other two
  central labels confine their kernel rows to at most one common outside
  port.  Their cross-term therefore vanishes on every distinct pair, and the
  remaining equation kills every `b_vw`.
- With all `A_i` zero, the pure `P_0Q_0` outside equation has zero left side.

In every case the two-colour binary target is impossible.

## 4. Sharp retained boundaries

If either central shore is root-axis-only, one Koszul identity used above is
absent.  The `P_0Q_0` row contains the missing sum and the one-port map
together, so the reviewed proof makes no conclusion on that chart.

At a P-common or Q-common outside endpoint, the full-parent map has a genuine
kernel.  In the row-basis activity model its ranks are `6`, `4`, and `3` when
three, two, or one opposite-shore coefficients are active.  These ranks are
a boundary control, not an exhaustive endpoint classification.  An exact
cube-root assignment also realizes all restricted scalar equations with one
nonzero outside edge, confirming that full-parent injectivity is load-bearing.

## 5. Computational evidence

The primary verifier checks over the rationals:

- the `26/27` Koszul rank and alternating generator;
- the `9/9` complete and `6/6` row-plane parent ranks;
- the all-three- and exactly-two-`A` eliminations;
- every nonempty one-`A` activity support; and
- the endpoint activity ranks and cube-root boundary control.

The no-import audit reconstructs the matrices over `F_101`, exhausts the
all-`A` scalar system over `F_7`, rechecks the one-`A` support logic, and
independently verifies the cube-root control.  These programs replay the
displayed algebra.  The source-pair provenance, common-edge expansions,
conditional scope, and retained open charts remain written mathematics.
