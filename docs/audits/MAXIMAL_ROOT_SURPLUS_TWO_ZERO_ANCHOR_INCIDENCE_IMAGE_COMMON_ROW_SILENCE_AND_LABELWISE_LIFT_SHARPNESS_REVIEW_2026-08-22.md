# Hostile review: zero-anchor incidence image, fixed-common-row silence, and labelwise-lift sharpness

## Verdict

**ACCEPT after required corrections.**  The corrected `GLS36` theorem is
type-correct, quantifier-correct, and appropriately scoped.  The arbitrary-
root incidence-image formula and fixed-residual labelwise-lift reduction are
exact.  The four-root maximum-root sharpness leaf is independently replayed
by two implementations.  Nothing in this tranche excludes the swallowed
branch on the witness locus, supplies a downstream target package, closes the
strategic node, or resolves the global conjecture.

The global Krenn--Gu conjecture remains **UNRESOLVED**.

## Reviewed artifacts

- [`GLS36 theorem`](../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_INCIDENCE_IMAGE_COMMON_ROW_SILENCE_AND_LABELWISE_LIFT_SHARPNESS_THEOREM.md)
- [`focused primary verifier`](../../claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_incidence_image_common_row_silence_and_labelwise_lift_sharpness.py)
- [`independent no-import audit`](../../claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_incidence_image_common_row_silence_and_labelwise_lift_sharpness.py)
- the `GLS36` entries in [`current frontier`](../current-frontier.md) and the
  [`supply/target node DAG`](../history/handoffs/MAXIMUM_ROOT_SURPLUS_TWO_SUPPLY_TARGET_NODE_DAG_2026-08-20.md)
- owning interfaces `GLS21`, `GLS23`, `GLS35`, and the exact `GLD11` control.

The hostile review was read-only and separate from the primary derivation.
It checked definitions, types, quantifiers, finite certificates, and claimed
boundaries.  It is not itself the independent computational audit; that role
belongs to the standard-library no-import script.

## Required corrections found and resolved

### 1. Primal/dual type correction

The first draft reused `W_Uhat`, which `GLS35` uses for a dual deck space, as
a primal test space.  It also left the one-residual components of `rho_Q`
under-specified.  The accepted statement instead defines

```text
Z_Uhat=tensor_u V_u,
h_D=H_(Bhat-D)(z_(Q-D)),
rho_D(tensor_u z_u)
 =h_D(tensor_(u notin D_0) z_u) tensor_(u in D_0) z_u.
```

Thus every residual slot outside `D` is evaluated, `rho_D` lands in the
correct `D_0` summand of `L_Q`, and the map extends canonically from pure
tensors.

### 2. Residual-contraction quantifier correction

The first draft called one fixed residual contraction equivalent to the
complete uncontracted GHZ equation.  The accepted theorem states the exact
scope:

- at fixed residual vectors, equations (17)--(19) encode the residual-
  evaluated `Q`-contracted target and all its mixed `Uhat` coefficients;
- a complete hypothetical witness implies these equations for every residual
  choice, or coefficientwise over the formal residual family;
- one fixed contraction does not imply the uncontracted target equation.

### 3. Common-row/Fitting scope correction

The first draft overextended fixed-row silence to tangent and Fitting
arguments generally.  The accepted theorem proves only that, after full
swallow, every fixed `lambda in (B_Q^anc)^perp` kills every labelled source
coefficient, `q`, and the three pure target rows.  Hence that common row gives
`0=0` and cannot be normalized on `q`.  Incidence-rank/Fitting membership
alone does not manufacture a separating row.  The theorem and navigation
documents now explicitly preserve the possibility that tangent or Fitting
equations constrain which parameter-locus fibres occur.

## Mathematical audit

### Incidence-image theorem

At `omega=0`, the two kinds of non-`Q` four-vertex matching coefficient are

```text
xi_0^s tensor Y_u x+X_u x tensor xi_1^s,
X_u x tensor Y_v y+X_v y tensor Y_u x.
```

The third matching in each case is multiplied by `omega`.  Complete slicing
therefore gives exactly `B_Q^anc=im sigma_Q` without a rank-open assumption or
division.  The all-rank augmentation test for swallowing is ordinary finite-
dimensional column membership and retains every exceptional fibre.

### Fixed-common-row theorem

If `q,r_0,r_1,r_2` all lie in `im sigma_Q`, every annihilator row kills the
whole image and those four declared columns.  The raw promoted source and the
pure target are both zero after that row.  This is exact but deliberately
narrow: it does not cover label-dependent operators.

### Fixed-residual labelwise lift

After evaluation of the remaining residual slots, `rho_Q(z)` records one
partial contraction for each label.  The raw matching decomposition gives

```text
q H_Uhat(z)+sigma_Q(rho_Q(z))
```

as the probe coefficient of the contracted state.  On primal mixed tests the
diagonal target vanishes.  Substituting any certificate
`sigma_Q(v)=q` yields

```text
rho_Q(z)+H_Uhat(z)v in ker sigma_Q.
```

Two certificates differ by the kernel, so the condition is certificate-
independent.  This is a reformulation, not the missing faithfulness theorem.

### Maximum-root sharpness leaf

For the `GLD11` retyping `A=(r_1,r_2)`, `Q=(q_0,q_1)`, exact replay confirms:

```text
omega=0, q=e_21, p=1,
rank B_Q^anc=8,
B_Q^anc=span{e_00,e_01,e_02,e_10,e_11,e_20,e_21,e_22},
im Flat_A(G)=B_Q^anc.
```

All eight named single-slice certificates pass.  The missing coordinate is
`e_12`.  The residual-absent deck has nine unit words.  The already owned
maximum-root, triple-blocker, pure/Hamming-shell, local-concision, and seven-
response gates remain valid.  The diagonal anchor is silent.  The full state
has `119` supported words from `124` nonzero matchings and exactly `116` mixed
GHZ failures (`111` of coefficient one and five of coefficient two).  Thus
the graph is a sharp physical control, not a witness.

## Verification replay

The following passed on the candidate tree:

```text
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_incidence_image_common_row_silence_and_labelwise_lift_sharpness.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_incidence_image_common_row_silence_and_labelwise_lift_sharpness.py
python claims/arbitrary-order/verify_four_root_simultaneous_swallowed_pure_nonzero_response_physical_control.py
python -I claims/arbitrary-order/audit_four_root_simultaneous_swallowed_pure_nonzero_response_physical_control.py
```

The focused primary uses exact SymPy matrices, explicit perfect-matchings,
and a probe flattening.  The no-import audit uses standard-library rational
elimination, direct coordinate columns, and a vertex-deletion recurrence.  It
does not import the primary or the `GLD11` implementation.

## Unresolved boundary

The smallest remaining load-bearing obligation is a deck-coupled,
label-dependent theorem.  For every swallowing certificate
`v in sigma_Q^(-1)(q)`, it must use the same graph's full mixed equations to
force some residual contraction and primal mixed test `z` for which

```text
rho_Q(z)+H_Uhat(z)v notin ker sigma_Q,
```

or derive an equivalent contradiction.  It must handle zero complementary-
deck components, proportional/cancelling labels, every exceptional fibre,
and the separate response, activity, synchronization, nuisance-survival,
anchor, downstream-interface, and arbitrary-root source-coverage gates.

The accepted theorem proves none of those obligations and makes no permanent,
extraction/gluing, or global-resolution claim.
