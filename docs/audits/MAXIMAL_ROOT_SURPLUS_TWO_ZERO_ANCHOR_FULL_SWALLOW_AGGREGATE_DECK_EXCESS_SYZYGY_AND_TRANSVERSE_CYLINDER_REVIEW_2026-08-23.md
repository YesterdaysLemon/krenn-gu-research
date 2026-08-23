# Hostile review: zero-anchor full-swallow aggregate deck, excess syzygies, and transverse cylinders

## Verdict

**ACCEPT after mathematical, interface, independence, and scope audit.**  At
one fixed residual contraction, the full target equation has aggregate
incidence/deck image in `Delta+Kq`.  The pulled-back rows canonically dual to
`B/(Delta+Kq)` are exact labelwise syzygies killed by deck aggregation, not
legal selectors.  On `D(p)`, every promoted pair target is confined to the exact
rank-stratified transverse cylinder claimed in the theorem.

The rank-six control is only an abstract labelled deck interface: its decks
are not proved to be principal permanents of one graph.  The rank-five
control is a literal full-swallow incidence family and satisfies every mixed
lift, but its pure target fails by a rank-one/rank-three flattening gap.  No
remaining rank-four-through-nine fibre is excluded.  Target survival,
response, synchronization, activity, nuisance survival, silent-source
coverage, and raw-escape attachment remain open.  The strategic node and
the global Krenn--Gu conjecture remain **UNRESOLVED**.

## Reviewed artifacts

- [`GLS40 theorem`](../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_FULL_SWALLOW_AGGREGATE_DECK_EXCESS_SYZYGY_AND_TRANSVERSE_CYLINDER_THEOREM.md)
- [`focused primary verifier`](../../claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_full_swallow_aggregate_deck_excess_syzygy_and_transverse_cylinder.py)
- [`independent no-import audit`](../../claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_full_swallow_aggregate_deck_excess_syzygy_and_transverse_cylinder.py)
- owning interfaces `GLS8`, `GLS22`, `GLS23`, `GLS35`, `GLS36`, and `GLS39`
- the `GLS40` current-frontier, supply/target DAG, and arbitrary-order README
  entries.

Two read-only hostile-review passes replayed the theorem and scripts.  One
concentrated on the aggregate/excess/cylinder typing; their combined checks
covered the rank-five and rank-six controls and every physical-boundary
sentence.  Independence is claimed for the separately implemented no-import
audit below, not merely for these review passes.

## Aggregate identity and all-test lift audit

Fix one `GLS8`-eligible `(Q,A)` chart and one fully supported residual
contraction.  On `omega=0`, `GLS36` gives

```text
q tensor H_Uhat+sigma_Q rho_Q
 =sum_c alpha_c r_c tensor ell_c.                    (1)
```

The theorem renames `sigma_Q rho_Q` as `J_Q`; it does not reuse `A_Q`, which
already denotes the formal residual-absent deck projection in `GLS35`.
Under full swallow,

```text
S=Delta+Kq subset B=im sigma_Q.
```

Equation (1) therefore proves `im J_Q subset S` without division, a rank
minor, or a response assumption.  For arbitrary lifts

```text
sigma_Q(v)=q,             sigma_Q(v_c)=r_c,
```

applying `sigma_Q` to

```text
rho_Q(z)+H_Uhat(z)v-sum_c alpha_c ell_c(z)v_c
```

gives zero by (1).  The formula is valid for every port test.  On the mixed
subspace the three pure evaluations vanish and it reduces exactly to
`GLS36` equation (19).  Changing a lift changes the expression by a
`ker sigma_Q`-valued map, so no hidden choice is used.

The aggregate-rank formulas are also exact.  If `q notin Delta`, the outputs
`q,r_0,r_1,r_2` are independent, so the rank is the dimension of
`span{H_Uhat,ell_0,ell_1,ell_2}`, namely three or four.  If
`q=sum beta_c r_c`, the three coefficient rows are

```text
alpha_c ell_c-beta_c H_Uhat.
```

They form a rank-three diagonal map minus a rank-at-most-one map, hence have
rank two or three.  This includes `q=0`, `H_Uhat=0`, and every exceptional
rank/divisor fibre.

## Excess-module audit

The canonical module is

```text
E_Q^exc=sigma_Q^*(Ann(Delta+Kq)).                    (2)
```

Because `S subset B=im sigma_Q`, the kernel of the restricted pullback is
exactly `Ann(B)`.  Thus

```text
dim E_Q^exc
 =dim Ann(S)-dim Ann(B)
 =dim B-dim S.                                       (3)
```

This is `k-3` for `q in Delta` and `k-4` otherwise.  Every representing
coefficient row `lambda` kills `S`, while `lambda J_Q=0` proves
`sigma_Q^*(lambda) rho_Q=0`.  A nonzero pullback is nonzero on some direct
label summand, but it kills `q` and every `r_c`.  The theorem therefore calls
these rows aggregate-cancelling labelwise syzygies, not normalized selectors,
responses, or target attachment.

Together with `GLS39`, the only zero-excess full-swallow possibility is
`k=4` with `q notin Delta`.  The theorem explicitly leaves that branch open.
For `q in Delta`, every surviving rank has at least one excess direction;
this is a reduction, not a contradiction.

## Transverse-cylinder audit

On `D(p)`, `GLS22` gives

```text
ker P_Q=Kq.
```

Full swallow puts this line in `B`, while `GLS35` gives

```text
C_Q=P_Q(B)=N_empty^tr.
```

Hence `dim C_Q=k-1` on every rank/divisor fibre.  For a promoted pair target
`C`, complete coefficient slicing gives:

- `t_C=(P_Q tensor id)g_C` has all coefficient slices in `P_Q(B)`;
- the `GLS23` nuisance formula has zero top-anchor term because `omega=0`,
  zero `D=Q` term because `P_Q(q)=0`, and every remaining slice in `P_Q(B)`;
- each pure column has coefficient `P_Q(r_c) in P_Q(B)` by full swallow.

Thus desired, nuisance, and pure columns all lie in

```text
C_Q tensor V_C^*.
```

Because both a desired tensor and its nuisance are contained in the same
cylinder, survival there is equivalent to survival in the full transverse
space.  Since a pair target has `dim V_C^*=9`, the cylinder dimensions are
exactly `27,36,45,54,63,72` for `k=4,...,9`.

If `q notin Delta`, `P_Q` is injective on `Delta`; if `q in Delta`, its
restriction has kernel `Kq`.  This proves the respective residual cylinder
dimensions `k-4` and `k-3`.  The rank-four 27-row cylinder is not the
`GLS25` double-transverse module: `GLS25` assumes `omega!=0`, whereas this
theorem is on `omega=0`.  No cross-chart bridge to `GLD15/16` is asserted.

## Rank-six full-equation interface control

The six labels have colours

```text
q_0,u_0:0;       q_1,u_1:1;       u_2,u_3:2,
```

and each incidence map is its colour-coordinate projector.  Excluding the
residual pair from `sigma_Q` still leaves every symmetric matrix unit:

```text
B=Sym_3,             rank B=6,
q=E_01+E_10,         dim(Delta+Kq)=4.
```

The four nonzero assigned complementary decks contribute, respectively,

```text
-q tensor H_Uhat,
r_0 tensor ell_0,
r_1 tensor ell_1,
r_2 tensor ell_2.
```

The factors `1/2` exactly cancel the doubled same-colour polarizations.  The
primary and audit separately check all `81` port words, rank `J_Q=4`, excess
dimension two, `p=2`, and transverse rank five.

The scope boundary is load-bearing.  The complementary forms are assigned
independently after the residual contraction.  No principal-permanent graph,
all-residual compatibility, maximum-root source package, response, or
downstream gate is supplied.  The control proves only that the fixed
label/deck interface and equation (1) are algebraically consistent.

## Rank-five mixed/pure boundary control

Direct multiplication of the two displayed ternary label maps gives

```text
B=Delta+K(E_12-E_10)+K(E_20-E_21),       rank B=5.
```

The three diagonal witnesses are `-r_0,r_1,r_2`; `q=0`.  The independent
annihilator reconstruction is

```text
span{E_01,E_02,E_10+E_12,E_20+E_21}.
```

For a third-label vector with six coordinates, compatibility with bases of
both active three-dimensional label spaces gives `24` linear equations of
rank six.  Both scripts recover a unimodular `6 x 6` subsystem with
determinant `-1`; therefore every compatible third-label map is zero over
every field.

With all internal `Bhat` edges zero, every complementary deck and `rho_Q`
vanishes.  The mixed equation holds for every residual choice, but the pure
target does not.  Allowing one arbitrary deck cannot fix it: the sole raw
tensor is a pure product across `(A,u,v)|(rest)` and has flattening rank one,
whereas ternary GHZ has rank three.  This exact control refutes the tempting
claim that polarization, full swallow, and the mixed lift alone exclude rank
five.  It does not prove that every rank-five family has two active labels.

## Rejected stronger attacks

An exploratory claim that `Delta subset B` forces `dim B>=6` is **false**.
The exact rank-five control above is a characteristic-zero countermodel to
that abstract incidence claim.  It is not a witness counterexample because
its pure target fails.

No universal rank-four exclusion was proved.  Exact modular searches found
no rank-four model and reduce some normalized charts to rank-one/rank-two
off-diagonal forms, but those searches do not cover arbitrary preimages,
domains, or multi-label families.  They are not retained as theorem evidence.
The determinant of one decomposable matrix pencil is also insufficient to
exclude a four-dimensional combined image.  `GLS40` makes no rank-four claim.

## Exact computational audits

The SymPy primary replays:

- aggregate ranks `(3,4)` for `q notin Delta` and `(2,3)` for
  `q in Delta`;
- excess profiles `(0,1,2,3,4,5)` and `(1,2,3,4,5,6)`;
- all six cylinder dimensions;
- the rank-six control on all `81` port words, including ranks `6/4/5`; and
- the rank-five image, annihilator, `24 x 6` compatibility system,
  determinant `-1`, and flattening ranks `1/3`.

The no-import audit uses only `Fraction`, independent Gaussian elimination,
dense rational tuples with sparse word-by-word evaluation, direct
annihilator pullbacks, and separately entered control data.  It imports no
project module or third-party package.
Its representation and derivation are genuinely independent of the SymPy
primary.

## Verification replay

The following pass on the candidate tree:

```text
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_full_swallow_aggregate_deck_excess_syzygy_and_transverse_cylinder.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_full_swallow_aggregate_deck_excess_syzygy_and_transverse_cylinder.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_promoted_two_probe_one_target_attachment_and_pointwise_failure_reduction.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_promoted_two_probe_one_target_attachment_and_pointwise_failure_reduction.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_promoted_all_port_transverse_quotient_and_projective_synchronization_failure.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_promoted_all_port_transverse_quotient_and_projective_synchronization_failure.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_promoted_transverse_complete_nuisance_decomposition_and_top_anchor_dichotomy.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_promoted_transverse_complete_nuisance_decomposition_and_top_anchor_dichotomy.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_raw_root_deck_quotient_and_output_coefficient_separation_nogo.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_raw_root_deck_quotient_and_output_coefficient_separation_nogo.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_complete_pairwise_diagonal_family_rank_bound_and_minimal_raw_swallow_exclusion.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_complete_pairwise_diagonal_family_rank_bound_and_minimal_raw_swallow_exclusion.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_incidence_image_common_row_silence_and_labelwise_lift_sharpness.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_incidence_image_common_row_silence_and_labelwise_lift_sharpness.py
```

The focused scripts, Ruff checks, and all six owning primary/audit pairs pass.
Candidate-tree hygiene compiles `2304` Python files and resolves all `1437`
Markdown files; the mandatory unit suites pass `191+14` tests.  Link rewrite
is idempotent with zero changes, and cached diff checking passes.  Exact-head
hosted CI and merged-main replay remain publication gates to be recorded
before and after merge.

## Unresolved boundary

The smallest remaining load-bearing obligation is same-graph physical
compatibility, not another aggregate rank bound.  One must use the principal
permanents over the full residual family to contradict every excess branch or
force target-specific survival and nonzero response in one cylinder, then
supply synchronization, activity, nuisance survival, and a named downstream
receiver.  The zero-excess rank-four `q notin Delta` fibre requires separate
analysis.  Silent `p=0` source coverage and raw escape remain separate.

Nothing in this tranche starts permanent restriction, extraction/gluing, or
global-conjecture resolution.
