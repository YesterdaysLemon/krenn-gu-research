# Hostile review: multi-`T_0` Family-A proper-face repair and source-integrability boundary

## Verdict

**PASS as a scoped parent-boundary theorem; neither remaining key is
excluded.**  `GLS78` proves that the direct proper-face and `GLS77`-style
kernel-difference mechanisms do not separate the live Family-A `r=2,3`
charts.  The exact restricted systems have common physical-edge controls,
and every active-`T_0` off-kernel row tested exactly retains legal repair
channels.

The theorem removes no profile.  Family A `r=2` (`1,080 / 1`) and `r=3`
(`360 / 1`) remain **OPEN**; the six-deficient residual stays
`97,215 / 79`, and global Krenn--Gu remains **UNRESOLVED**.

## Artifacts reviewed

- [`GLS78` theorem](../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_SIX_DEFICIENT_MULTI_T0_FAMILY_A_PROPER_FACE_REPAIR_AND_SOURCE_INTEGRABILITY_BOUNDARY_THEOREM.md)
- [primary verifier](../../claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_six_deficient_multi_t0_family_a_proper_face_repair_and_source_integrability_boundary.py)
- [independent audit](../../claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_six_deficient_multi_t0_family_a_proper_face_repair_and_source_integrability_boundary.py)
- [active-T leakage row-span verifier](../../claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_six_deficient_multi_t0_family_a_active_t_leakage_row_span_boundary.py)
- [`GLS77` one-T0 complete-key parent](../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_SIX_DEFICIENT_ONE_T0_FULL_SOURCE_KERNEL_DIFFERENCE_AND_COMPLETE_KEY_EXCLUSION_THEOREM.md)
- [`GLS71` crossed strict-parent normalization](../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_SIX_DEFICIENT_SINGLE_BINARY_STRICT_PARENT_EDGE_CHART_AND_ATTACHMENT_ACTIVITY_THEOREM.md)

## 1. Exact charts and restriction maps

The `GLS70` taxonomy gives exactly

```text
r=2: S_0 R_2 R_1 R_0 T_0^2,       1,080 profiles,
r=3: S_0 R_2 R_1 T_0^3,              360 profiles.
```

With the `R_0` port of the first chart at `3`, the kernel and row-plane
dimensions are

```text
r=2: dim K=(2,1,1),       dim J=(1,2,2),
r=3: dim K=(1,1,1),       dim J=(2,2,2).
```

Let `r_u:E_u -> K_u^*` be restriction and let `R_u` apply it in outside
slot `u`.  Direct basis decomposition verifies

```text
intersection ker R_u = J_3 tensor J_4 tensor J_5,
```

with dimensions `4,8`.  This is not the kernel of
`r_3 tensor r_4 tensor r_5`, whose dimensions are `25,26`; the latter is
the sum of all tensor spaces having at least one `J_u` factor.

The theorem's physical four-deck carries an additional central `E_2`
factor.  The audited statement correctly uses `id_(E_2) tensor R_u`, or
equivalently says that its outside factor lies in the product of the three
`J` spaces.

## 2. Nonzero physical blind direction

Choose

```text
W_23=a_2 tensor j_3,       W_45=j_4 tensor j_5,
W_24=W_25=W_34=W_35=0,
```

with every factor nonzero and `j_u in J_u`.  The actual four-vertex
hafnian is

```text
H_2345=a_2 tensor j_3 tensor j_4 tensor j_5!=0.
```

Every outside single-slot restriction kills it.  This proves a nonzero
physical intersection with the blind subspace, not realization of that
whole subspace and not a complete source.

The edgewise restriction maps defining `A,Y,Z,B` are surjective linear
maps.  Therefore the displayed restricted controls below lift
simultaneously, edge by edge, to one physical edge array.  Surjectivity does
not supply probe-source rows or solve the complete eight-vertex identity.

## 3. Exact restricted controls

For `r=2`, take `K_3^*` basis `x,y`, kernel-line generators `z_4,z_5`, and

```text
k_3=x, l_3=y,       (k_4,l_4)=(1,0),
(k_5,l_5)=(0,1),
B_45=-1, B_35=-x, B_34=-y, alpha=1.
```

All three selector equations vanish and the two attachments are `-2x` and
`-2y`.  For `r=3`,

```text
k=(1,1,1),       l=(0,1,1),
B_45=-2, B_35=-1, B_34=-1
```

gives zero selectors and attachments `-4,-2`.

The stronger conditional one-silent `r=2` system also admits

```text
alpha=m=p=b=c=1,
r=(mu y_3-lambda x_3)/4,       s=-r,
B_45=-2,       B_35=0,
B_34=(lambda x_3+mu y_3)/2.
```

Direct substitution gives both selectors, both nonzero attachments, and
`C=rp+sm=0`.  Thus the outer-product relation that was contradictory with
two active `R_0` ports in `GLS77` is compatible after one active target
factor has synchronized on a `T_0` kernel.  At `r=3`, all outside kernel
factors are synchronized and the system is weaker still.

## 4. Surviving repair hierarchy

Contraction at a `T_0` kernel structurally removes source-pair classes
containing that port.  It does not imply that every other class is nonzero
at a particular source.

For `r=2`, contraction at port `4` leaves the ten possible pairs among
`{0,1,2,3,5}`.  Besides the three central and three port-`3` pairs, the
surviving port-`5` repairs are

```text
g_05, g_15, g_25, g_35.
```

A second contraction at port `5` leaves the six pairs among
`{0,1,2,3}`, exactly the accepted strict parent.  For `r=3`, the analogous
single/double/triple counts are `10,6,3`; an uncontracted `T_0` port always
retains its repairs.

The target is contracted too.  Its two colours remain nonzero, but their
outside factors become proportional at every `T_0` kernel.  After all
outside contractions the target is the already-known synchronized binary
central triangle, not zero.

## 5. Complete-row leakage audit

The supplementary verifier reconstructs all `105` perfect matchings, keeps
independent `kappa_3,kappa_4,kappa_5`, and retains every nonmissing-colour
row at each `T_0` port.  Its representative exact identity is

```text
F_2112-kappa_4 F_2109
=P_30 [
 Q_520 { I_0122 (I_2402-kappa_4 I_2401)
        +I_0220 (I_1422-kappa_4 I_1421)
        +I_1220 (I_0422-kappa_4 I_0421) }
 +I_1220 (I_4520-kappa_4 I_4510)
 +I_2500 (I_1422-kappa_4 I_1421)
 +I_1520 (I_2402-kappa_4 I_2401) ].
```

The desired off-kernel `I_2500` term is accompanied by `Q_520`, `W_15`,
and `W_45` repair channels.  The `r=3` formula replaces `P_30` by `P_300`.

Over `QQ(kappa_4)`, all `28` leakage-bearing `r=2` three-row blocks have no
slope-field linear leakage separator.  Over `QQ(kappa_3,kappa_4)`, the same is true
for all `78` `r=3` blocks.  All `81` nine-row `(c_3,c_4)` blocks in each
chart are likewise nonseparating; the exact nonleak-nullity sums/maxima are
`173/7` and `100/5`.

An earlier exploratory implementation accidentally specialized all `T_0`
slopes to one `kappa`.  That version was not promoted.  The retained
verifier uses independent slopes and reruns the exact rational-function
nullspaces.

The exhaustive `c_5=0` row spans have zero leakage-rank increment at two
large-prime specializations with distinct slope triples.  These global
ranks are explicitly **modular evidence only**.  The exact theorem is
generic over the independent-slope rational-function fields and covers
linear combinations only within each named block.  It does not exclude
exceptional slope specializations, cross-block combinations, nonlinear
syzygies, or a different complete-source coupling.

## 6. Verification and scope

The primary and no-import scripts independently check the key counts,
restriction dimensions, restricted controls, one-silent control, and both
`r=2/r=3` repair hierarchies.  The no-import script additionally checks the
physical ordered-slot direction, while the primary script checks its scalar
symbolic model.  The leakage verifier separately owns the `105`-matching
expansion and exact block nullspaces.

No script constructs a complete source, proves that every repair is
nonzero, excludes either key, or resolves the conjecture.  The proved next
obligation is to retain an off-kernel active-`T_0` coordinate while coupling
the repairs from every other active `T_0` port through their common physical
decks.  The residual remains `97,215 / 79`; global Krenn--Gu remains
**UNRESOLVED**.
