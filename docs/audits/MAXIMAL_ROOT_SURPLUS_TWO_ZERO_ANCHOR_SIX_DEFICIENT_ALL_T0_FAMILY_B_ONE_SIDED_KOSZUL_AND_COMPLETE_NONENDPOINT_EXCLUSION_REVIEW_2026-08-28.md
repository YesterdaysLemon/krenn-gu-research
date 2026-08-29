# Hostile review: all-`T_0` Family-B one-sided Koszul and complete nonendpoint exclusion

## Verdict

**PASS for the complete outside nonendpoint chart.**  `GLS75` removes the
central mixed-support hypothesis of `GLS74` and proves that no Family-B
`S_0^3T_0^3` source can lie on any outside nonendpoint pure-`P_3` chart.

This does not exclude the typed key.  P-common and Q-common outside endpoint
charts have genuine full-parent kernels and remain open.  No profile is
removed; the inherited six-deficient residual remains `98,355 / 81`, and the
global Krenn--Gu conjecture remains **UNRESOLVED**.

## Artifacts reviewed

- [`GLS75` theorem](../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_SIX_DEFICIENT_ALL_T0_FAMILY_B_ONE_SIDED_KOSZUL_AND_COMPLETE_NONENDPOINT_EXCLUSION_THEOREM.md)
- [primary verifier](../../claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_six_deficient_all_t0_family_b_one_sided_koszul_and_complete_nonendpoint_exclusion.py)
- [independent audit](../../claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_six_deficient_all_t0_family_b_one_sided_koszul_and_complete_nonendpoint_exclusion.py)
- [`GLS74` parent boundary](../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_SIX_DEFICIENT_ALL_T0_FAMILY_B_NONENDPOINT_FULL_PARENT_TRANSVERSE_INJECTIVITY_AND_ENDPOINT_ACTIVITY_BOUNDARY_THEOREM.md)
- [`GLS71` pure-`P_3` chart theorem](../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_SIX_DEFICIENT_SINGLE_BINARY_STRICT_PARENT_EDGE_CHART_AND_ATTACHMENT_ACTIVITY_THEOREM.md)

## 1. Exhaustive central-shore cover

For a central label `i`, suppose both probe shores are root-axis-only.  In
the full `P_aQ_a` coefficient, `a=1,2`, every source pair meeting `i`
vanishes.  Every pair meeting an outside label also vanishes because the
outside nonendpoint shores have only bidegree `P_0Q_0`.  The complementary
central pair is therefore the sole survivor:

```text
(p_j^a q_k^a+q_j^a p_k^a) tensor H_({i} union O)
 =mu_a tensor_(ell=0)^5 e_(ell,a).
```

The same probe-independent physical four-port deck would have to lie on the
pure colour-1 and pure colour-2 lines.  Since both target coefficients are
nonzero, this is impossible.  Hence every central label has at least one
non-root shore and supplies at least one legal mixed-root Koszul row.

## 2. One-sided block lemma

In outside bases `(U_u,V_u,N_u)`, let `K_U(C)` and `K_V(C)` be the two
three-pair Koszul sums and let `Phi(D)` be the complete three-one-port map.
After the available Koszul sum is killed, the full `P_0Q_0` row has the exact
form

```text
K_U(C)=0,                 Phi(D)+lambda K_V(C)=0,
```

or its shore exchange.  The scalar `lambda` is the relevant root-axis local
coefficient and may vanish.

Evaluating the first row on two outside kernel lines directly gives
`C^u|_(K_v tensor K_w)=0`.  For the one-port row, project one outside slot
modulo `L_u`.  The first equation makes the two projected pair components
opposite multiples of `X_v tensor X_w`.  In the second equation their
`X_vY_w` and `Y_vX_w` coefficients have opposite signs, while the projected
parent term has equal signs.  Characteristic zero forces the projected
`D^u` coefficient to vanish.  Thus `D^u in L_u` and `D^u|K_u=0`.

The exact block calculation sharpens the statement:

- if `lambda=0`, `Phi` is injective and `D=0`, while the one-row Koszul
  kernel has dimension eight;
- if `lambda!=0`, scaling gives a `54 x 36` matrix of rank `31` and nullity
  five.  One dimension is the alternating pair-deck camouflage and four are
  row coboundaries satisfying

  ```text
  sum_u c_u=sum_u d_u=0
  ```

  for `D^u=c_uU_u+d_uV_u`.

The theorem uses only the kernel restrictions, so these full-row
coboundaries are a sharp retained feature rather than an omitted case.

## 3. Common-edge support elimination

The one-sided lemma recovers all three restricted physical equations used by
`GLS74`: the central row relation, the three pair-edge relations, and the
kernel restriction of each one-port correction.  The support-three,
support-two, and support-zero central-edge cases therefore transfer without
change.

The support-one case requires a new argument.  If only `A_1` is nonzero,
the outside pure equation has `h_u=A_1R_1u`.  In a representative
nonendpoint chart the exact `GLS71` normal form is

```text
2h_3=-rU_3+sV_3,
2h_4= rU_4-sV_4,
2h_5= rU_5+sV_5,                 rs!=0.
```

Thus every `R_1u` has nonzero coordinates on both shore lines.  Restricting
the single available identity for `C_0` at `K_v` gives

```text
rho_2v (X_u tensor R_1w+R_1u tensor X_w)=0,
```

where `X` is uniformly the `U` or `V` shore.  The bracket cannot vanish
because `R_1u` is proportional to neither shore, so every `rho_2v=0`.
The `C_2` identity similarly kills `rho_0`; the `C_1` pair restriction then
forces every outside kernel edge to vanish.  This kills the binary triangle.

## 4. Retained endpoint boundary

The proof uses two genuinely nonendpoint facts: `(U_u,V_u)` is a basis at
every outside port, and each `h_u` has nonzero coordinates on both shore
lines.  At a P-common or Q-common endpoint, the selected shore activity can
drop to two or one ports.  The row-basis parent ranks are then `4` and `3`,
with kernel dimensions `2` and `3`; the nonendpoint bracket can also vanish.

Therefore the next Family-B theorem must use additional mixed complete
coefficients to detect the endpoint kernel directions.  Reusing `P_0Q_0`
injectivity or the nonendpoint transverse row without this extra provenance
would be invalid.

## 5. Computational evidence

The primary rational verifier checks the `31/36` one-sided rank, its
four-dimensional `D` projection, every transverse forced-zero coordinate,
the pair-kernel restrictions, the `lambda=0` injective case, the binary
source-pair support, nonendpoint row transversality, the inherited central
support algebra, and the endpoint rank drop.

The no-import audit reconstructs the maps over `F_101`, proves forced-zero
coordinates by row-space membership, exhausts `1,296` one-central-edge
transverse brackets and the all-central-edge scalar system over `F_7`, and
independently rechecks the endpoint ranks.  The exact source-pair provenance,
physical deck factorization, and endpoint scope remain written mathematics.
