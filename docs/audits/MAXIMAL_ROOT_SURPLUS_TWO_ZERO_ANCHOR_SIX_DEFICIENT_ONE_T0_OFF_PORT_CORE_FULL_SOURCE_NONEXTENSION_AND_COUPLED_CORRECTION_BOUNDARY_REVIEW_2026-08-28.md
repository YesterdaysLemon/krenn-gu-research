# Hostile review: one-`T_0` off-port-core full-source nonextension

## Verdict

**PASS for the stated fixed-core nonextension theorem.**  `GLS73` proves
that the exact `GLS72` common-edge control cannot be extended to the complete
six-open GHZ source identity by changing only the five edges incident to its
silent `T_0` port.  Those five edges are completely arbitrary in the
theorem, not merely transverse or kernel-invisible corrections.

The result does **not** exclude the Family-A `r=1` key.  It fixes one
off-port physical core, and a hypothetical source may change that core while
opening an additional cancelling deck channel.  No typed profile is removed;
the live six-deficient residual remains `98,355 / 81`, and the global
Krenn--Gu conjecture remains **UNRESOLVED**.

## Artifacts reviewed

- [`GLS73` theorem](../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_SIX_DEFICIENT_ONE_T0_OFF_PORT_CORE_FULL_SOURCE_NONEXTENSION_AND_COUPLED_CORRECTION_BOUNDARY_THEOREM.md)
- [primary verifier](../../claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_six_deficient_one_t0_off_port_core_full_source_nonextension.py)
- [independent audit](../../claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_six_deficient_one_t0_off_port_core_full_source_nonextension.py)
- [`GLS72` parent theorem](../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_SIX_DEFICIENT_ONE_T0_SINGLE_BINARY_ACTIVITY_LOCALIZATION_AND_TRANSVERSE_FULL_DECK_SHARPNESS_THEOREM.md)
- [`GLS72` hostile review](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_SIX_DEFICIENT_ONE_T0_SINGLE_BINARY_ACTIVITY_LOCALIZATION_AND_TRANSVERSE_FULL_DECK_SHARPNESS_REVIEW_2026-08-28.md)

## 1. Diagonal coefficient

In the Family-A crossed normalization, the only source pair contributing to
the `P_0Q_0` all-colour-zero word is `{3,4}`.  Its probe factor is

```text
c_34=AD+BC!=0.
```

With the ten off-port edges fixed, the complete complementary deck is

```text
H_(0125)=W_01W_25+W_02W_15+W_05W_12.
```

The last two matchings vanish because `W_02=W_12=0`; the first contributes
exactly

```text
xi=[e_(2,0)e_(5,0)]W_25.
```

The nonzero colour-zero target therefore forces `c_34 xi=mu_0`, hence
`xi!=0`.  Every other entry of every incident edge cancels structurally from
this row.

## 2. Mixed coefficient and complete source-pair support

Choose the `P_0Q_2` word

```text
e_(0,2)e_(1,0)e_(2,0)e_(3,0)x_4e_(5,0).
```

Its GHZ target coefficient is zero.  The `{0,3}` source pair exposes
`H_(1245)`.  Of its three matchings, `W_12W_45` vanishes, `W_15W_24` has the
wrong slot-2 and slot-4 colours, and `W_14W_25` contributes `-xi`.  The
direct contribution is therefore `-Axi`.

The apparent nuisance channels are exhausted, not assumed away:

- every pair using port `4` as a probe endpoint supplies `e_(4,0)`, not
  `x_4`;
- silence removes port `5` as a `P_0` endpoint; and
- the sole remaining pair `{3,5}` has complementary deck `H_(0124)`, whose
  requested coefficient vanishes in all three matchings of the fixed core.

Thus the complete mixed coefficient is `-Axi=0`.  The accepted activity
orientation has `A!=0`, contradicting the diagonal row.

## 3. Scope and source-integrability boundary

The proof uses complete six-open coefficients, so it genuinely goes beyond
the `K_5`-restricted selector equations of `GLS72`.  It also allows arbitrary
values of `W_05,W_15,W_25,W_35,W_45`, including changes visible on `K_5`.
Consequently it rules out every port-5-only repair of this physical core.

It does not prove that every point of the localized `alpha=a=b=0` branch is
equivalent to the displayed core.  The next load-bearing obligation is a
coupled correction theorem: vary at least one off-port edge, preserve the
proved kernel restrictions, and classify the additional full-deck channel
that must cancel the mixed row.

## 4. Computational evidence

The primary verifier independently symbolizes all entries of the five
incident edges, enumerates every source pair and every four-deck perfect
matching, and recovers

```text
(AD+BC)xi-mu_0,             -Axi,
resultant_XI=-A mu_0.
```

The no-import audit uses a separate sparse matching representation over
`F_101`.  It checks that the only nonzero matching supports are
`(01)(25)` in `H_(0125)` and `(14)(25)` in `H_(1245)`, that the possible
`H_(0124)` repair coefficient is zero, and that the two equations conflict
for several nondegenerate substitutions.  Selector provenance, activity
orientation, and the fixed-core scope remain written mathematics.
