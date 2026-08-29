# Hostile review: all-`T_0` Family-B endpoint mixed coefficient and complete key exclusion

## Verdict

**PASS for the complete Family-B `S_0^3T_0^3` key.**  `GLS76` uses all
complete mixed endpoint coefficients to close the P-common and Q-common
outside charts retained by `GLS75`.  Together with the earlier nonendpoint
exclusion, this removes the sixty labelled Family-B `r=3` profiles and their
one key.  The six-deficient residual changes from `98,355 / 81` to
`98,295 / 80`.

The result is a kernel-restriction and common-physical-edge theorem, not an
injectivity statement for the full endpoint parent map.  Genuine internal
row-plane coboundaries and pure endpoint target-line directions survive.
They already obey the kernel restrictions used by the final support
argument.  Family A `r=1,2,3`, all other deficient-map branches, and the
global Krenn--Gu conjecture remain **UNRESOLVED**.

## Artifacts reviewed

- [`GLS76` theorem](../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_SIX_DEFICIENT_ALL_T0_FAMILY_B_ENDPOINT_MIXED_COEFFICIENT_AND_COMPLETE_KEY_EXCLUSION_THEOREM.md)
- [primary verifier](../../claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_six_deficient_all_t0_family_b_endpoint_mixed_coefficient_and_complete_key_exclusion.py)
- [independent audit](../../claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_six_deficient_all_t0_family_b_endpoint_mixed_coefficient_and_complete_key_exclusion.py)
- [`GLS75` nonendpoint parent](../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_SIX_DEFICIENT_ALL_T0_FAMILY_B_ONE_SIDED_KOSZUL_AND_COMPLETE_NONENDPOINT_EXCLUSION_THEOREM.md)
- [`GLS71` endpoint classification](../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_SIX_DEFICIENT_SINGLE_BINARY_STRICT_PARENT_EDGE_CHART_AND_ATTACHMENT_ACTIVITY_THEOREM.md)

## 1. Exact endpoint coefficient provenance

At a P-common endpoint, normalize

```text
p_u=P_0U_u,
q_u(t)=A_u(t)U_u+B_u(t)V_u,             B_u!=0.
```

The complete `P_0Q_t` coefficient after fixing the other two central `S_0`
labels at their colour-zero rows is exactly

```text
Phi_t(D_i)+p_i^0 K_t(C_i)+q_i(t)K_U(C_i)=0.
```

The three outside pairs give `Phi_t(D_i)`.  The three pairs from the retained
central label to an outside label give the two Koszul sums.  Pairs meeting a
contracted central label vanish on its colour-zero row, and the diagonal
target vanishes on the retained nonzero central word.  No face deck or
endpoint-kernel term is chosen independently.

If some central `p_i^r`, `r=1,2`, is nonzero, the `P_rQ_s` coefficient has no
outside--outside contribution because every outside `p` shore is `P_0`-only.
The same contracted-central and target vanishings leave only the three
`{i,u}` pairs.  Factoring the selected nonzero central covector gives
`K_t(C_i)=0` for every `t`, and the accepted `GLS75` one-sided lemma yields
the required kernel restrictions after choosing one `t` transverse at all
outside ports.

## 2. Root-only mixed coefficient lemma

For `p_i=P_0a` with `a!=0`, choose a central basis `(a,b)` and write

```text
q_i(t)=alpha(t)a+beta(t)b,              beta!=0.
```

The two central components are

```text
Phi_t(D_b)+beta K_U=0,
Phi_t(D_a)+K_t+alpha K_U=0.
```

Evaluating the second equation on `K_v tensor K_w` leaves

```text
(q_u(t)+alpha(t)U_u)
 C_i^u|_(K_v tensor K_w)=0.
```

Its transverse coefficient is `B_u!=0`, so every two-kernel restriction
vanishes.  After projecting slot `u` modulo `L_u`, write

```text
pi_u C_i^v=N_u tensor (xU_w+yV_w),
pi_u C_i^w=N_u tensor (zU_v+dV_v).
```

If `delta_b` is the projected `D_b^u` coefficient, the first component gives

```text
delta_b B_v+beta d=0,
delta_b B_w+beta y=0,
delta_b(A_v+A_w)+beta(x+z)=0.
```

The `V_vV_w` word of the second component is `yB_v+dB_w=0`.  A nonzero
`delta_b` would make `B_v,B_w` nonzero multiples of `beta`, after which that
last identity is a nonzero multiple of `2yd beta`.  Characteristic zero
therefore gives `delta_b=0`, then `y=d=0` and `x+z=0`.  The remaining two
mixed words give `x=z=-delta_a`, hence `delta_a=0`.  Thus

```text
C_i^u|_(K_v tensor K_w)=0,
D_i^u(z)|_(K_u)=0.
```

This proof does not split synchronized from nonsynchronized projective
incidences; it covers both.

If the central `p` shore is literally zero, joint rank two makes `q_i`
supply two independent central coefficient forms.  Applying the projected
equations to both forms forces both projected `D` coefficients to vanish:
one nonzero coefficient would synchronize its central form with both
`B_v,B_w`, while the independent second component kills all pair terms and
then the first coefficient.  The same two-kernel conclusion holds.

## 3. Sharp surviving endpoint kernel

The first draft risked overstating the preceding calculation as full
endpoint injectivity.  The corrected theorem explicitly retains a simple
coboundary:

```text
D_a^3=-U_3,              D_a^4=U_4,              D_a^5=0,
C^3=-U_4 tensor U_5,     C^4=U_3 tensor U_5,      C^5=0.
```

For every opposite shore `q(t)`, this satisfies

```text
Phi_t(D_a)+K_t(C)=0,                 K_U(C)=0.
```

More generally, when a central transverse functional is synchronized with
an outside `B_u`, the corresponding block can retain the pure endpoint line
with `V_u` in that port and `U` in the other two.  These are genuine full
row-plane directions.  They are not divided away or called zero.  Every one
of them is already invisible on the outside kernel restrictions, which is
the exact scope used below.

## 4. Selected-port support-one closure

The support-three, support-two, and support-zero cases use only the common
restricted physical system proved in `GLS75` and transfer unchanged.

For the remaining support-one case, take `A_1!=0` and `A_0=A_2=0`.  The
outside endpoint normal form gives

```text
rho_1u=0,
R_13=-lambda U_3,       R_14=lambda U_4,
R_15=lambda U_5,        lambda!=0.
```

For inactive central label `0`, a mixed non-root `p_0` coefficient gives
`K_t(C_0)=0`; choosing `B_4(t)!=0` and evaluating at `K_3` forces
`rho_23=0`.  If `p_0` is root-axis-only, contract the appropriate central
component of the complete mixed equation at `K_3`.  Every `Phi_t` term dies
by the already proved one-port restriction, leaving

```text
K_U(C_0)|_(K_3)=0.
```

The physical expansion is

```text
rho_23(U_4 tensor R_15+R_14 tensor U_5)
 =2lambda rho_23 U_4 tensor U_5=0.
```

This includes a literal zero `p_0` shore by using either nonzero component
of its rank-two `q_0` shore.  Hence `rho_23=0`; central label `2` similarly
gives `rho_03=0`.

The active central pair equation now kills both outside kernel edges meeting
the selected port:

```text
b_34=b_35=0.
```

The active one-port restriction at port `3` gives `sigma_13(z)=0`.  Thus the
only possibly surviving outside edge `b_45` multiplies a zero spoke, and the
complete binary-target flattening at central label `1` vanishes.  This
contradicts both nonzero target colours.  Central permutations and probe
exchange cover the other support choices and the Q-common endpoint.

## 5. Computational and scope audit

The primary exact script expands the canonical endpoint tensor to
`2 V_3U_4U_5`, checks the characteristic-zero projection elimination,
replays `1,372` root-only and `6,174` zero-shore rational incidence systems,
checks the selected-port sign, and verifies the residual subtraction.

The no-import audit uses a separate modular row reduction over `F_3`.  It
enumerates all thirteen projective functional lines, all `2,197` root-only
incidences, and all `26,364` zero-shore incidences with independent central
forms.  It independently rebuilds the endpoint tensor and count delta.  The
odd-characteristic computation audits the displayed algebra; the written
proof owns the characteristic-zero implication and arbitrary longitudinal
coefficients.

No verifier proves a full endpoint map injective, constructs a global graph
witness, closes a Family-A or other typed key, or resolves Krenn--Gu.  The
global status remains **UNRESOLVED**.
