# Hostile review: zero-anchor nonzero-root-companion minimal raw-swallow exclusion

## Verdict

**ACCEPT after scope and implementation audit.**  The rank-one-shore collapse
is type-correct, pointwise, and division-free.  Together with the independently
audited `GLS37` two-rank-two-shore exclusion, it proves that a nonzero
root-companion coefficient `q` cannot lie on a rank-three full-swallow fibre.
Here `q=G_Q^A(z_Q)` is the raw coefficient of the physical residual-absent
deck `H_Uhat`, not that physical deck itself.  On `GLS35`'s declared
complete-target non-silent branch, `p!=0` supplies `q!=0`, so full swallow
forces nuisance rank at least four.

This does not exclude ranks four through nine or rank-three full swallow with
`q=0`; those open fibres include `p=0` and diagonal-silent cases.  It also
does not exclude raw escape, any nonzero-anchor branch, or any original-target
attachment gate.  It does not close the source cover or strategic node.
The global Krenn--Gu conjecture remains **UNRESOLVED**.

## Reviewed artifacts

- [`GLS38 theorem`](../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_NONZERO_ROOT_DECK_MINIMAL_RAW_SWALLOW_EXCLUSION_THEOREM.md)
- [`focused primary verifier`](../../claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_nonzero_root_deck_minimal_raw_swallow_exclusion.py)
- [`independent no-import audit`](../../claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_nonzero_root_deck_minimal_raw_swallow_exclusion.py)
- owning theorems `GLS35`, `GLS36`, and `GLS37`
- the `GLS38` entries in [`current frontier`](../current-frontier.md), the
  [`supply/target node DAG`](../history/handoffs/MAXIMUM_ROOT_SURPLUS_TWO_SUPPLY_TARGET_NODE_DAG_2026-08-20.md),
  and the arbitrary-order claim README.

The hostile mathematical, dependency/scope, and implementation reviews were
read-only and separate from the primary derivation.  The no-import audit is a
separate standard-library support-containment derivation rather than another
coefficient-chart implementation.

## Mathematical audit

### Source of the nonzero root companion

`GLS35` Theorem 2 assumes the complete target and the non-silent `GLS34`
branch.  Its gate is explicitly

```text
H_Uhat!=0,       p=epsilon_A(q)!=0.
```

Thus `q!=0`.  If raw escape fails, the same theorem supplies

```text
q,r_0,r_1,r_2 in B_Q^anc.
```

No `p=0` point is imported into GLS38's live non-silent corollary.  Theorem 2
itself assumes only `q!=0`, so it also excludes any rank-three `p=0` or
diagonal-silent fibre on which `q` remains nonzero.

### Rank three makes the nuisance exactly diagonal

The three `r_c` are independent.  Full swallow and nuisance rank three
therefore imply

```text
B_Q^anc=Delta=span{r_0,r_1,r_2}.
```

The corrected `GLS36` incidence theorem supplies
`B_Q^anc=im sigma_Q` at zero anchor.  Hence every individual one-residual and
promoted-pair incidence column is diagonal.

### Low-shore collapse

If the left residual shore has rank at most one, nonzero `q` makes its rank
exactly one.  Write

```text
a_s=lambda_s a,
q=a tensor (lambda_0 b_1+lambda_1 b_0)=a tensor d.
```

This is a nonzero rank-one diagonal tensor, so `a` and `d` lie on the two
probe coordinate lines for one colour `c`.  For a port slice
`x=X_u(z),y=Y_u(z)`, each tensor

```text
a_s tensor y+x tensor b_s
```

is diagonal.  If `x(i)!=0` for `i!=c`, its off-diagonal row-`i` entries force
both `b_s` to be supported on coordinate `i`.  Their combination `d` would
then be supported on `i`, contradicting nonzero `d` on coordinate `c`.
Therefore every `X_u(V_u)` lies on the `c`-axis.  Every one-residual and pair
column is supported in row `c`; because it is diagonal, it lies in `K r_c`.
This contradicts `im sigma_Q=Delta`.

Transposition proves the right-shore case.  Thus a rank-three point would have
both shore ranks two, exactly the fibre excluded by `GLS37`.  The proof uses
no complementary-deck value, response, blocker, minor, or normalized
coordinate and therefore retains zero, proportional, and cancelling deck
components and every rank/divisor fibre.

## Independent computational audit

The exact primary generates bounded exact rational representatives: `648`
left-shore and `648` right-shore charts sampling `(1,1)`, `(1,2)`, and `(2,1)`.
It computes the complete one-residual off-diagonal kernel with SymPy and
confirms on those representatives that every allowed low-shore incidence
slice lies on the root-companion coordinate axis.  These grids are not an
exhaustive coefficient-space cover.

The no-import audit uses neither arithmetic charts nor row reduction.  It
exhausts the finite support-containment proof: all `49` nonzero decomposable
support pairs, the `384` missing-row and `384` missing-column masks, `768`
one-residual and `768` pair-generator support bounds on each shore, and all
nine discrete shore-rank profiles.  Exactly three decomposable supports are
diagonal coordinate lines; each side has `24` forced missing-axis support
patterns and all `24` contradict the pinned nonzero coordinate; every actual
diagonal generator after the collapse has support in the single pure line.
This is a different representation and derivation from the SymPy primary.

The arbitrary-parameter and arbitrary-root exhaustiveness comes from the
symbolic row-support proof above.  Nonzero `q` rules out zero shores, the new
argument excludes `(1,1)`, `(1,2)`, and `(2,1)`, and the independently audited
`GLS37` theorem excludes `(2,2)`.

## Verification replay

The following passed on the candidate tree:

```text
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_nonzero_root_deck_minimal_raw_swallow_exclusion.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_nonzero_root_deck_minimal_raw_swallow_exclusion.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_promoted_two_probe_one_target_attachment_and_pointwise_failure_reduction.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_promoted_two_probe_one_target_attachment_and_pointwise_failure_reduction.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_minimal_raw_swallow_incidence_classification_and_mixed_only_faithfulness_nogo.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_minimal_raw_swallow_incidence_classification_and_mixed_only_faithfulness_nogo.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_incidence_image_common_row_silence_and_labelwise_lift_sharpness.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_incidence_image_common_row_silence_and_labelwise_lift_sharpness.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_raw_root_deck_quotient_and_output_coefficient_separation_nogo.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_raw_root_deck_quotient_and_output_coefficient_separation_nogo.py
```

The focused GLS38 scripts and their Python/Ruff checks pass.  The index-complete
candidate tree also passes `check_hygiene.py`, all `191` migration-tool tests,
all `14` fourteen-vertex cycle-cover-lattice tests, link-rewrite idempotence,
and `git diff --exit-code`.  Exact-head hosted CI and merged-main replay remain
publication gates to be recorded outside this candidate commit before and
after merge, respectively.

## Unresolved boundary

The smallest continuation on the same zero-anchor non-silent full-swallow
branch is nuisance rank at least four.  Rank/Fitting membership alone remains
insufficient, and a fixed common annihilator row is silent after full swallow.
A successful continuation must use additional same-graph complete-target
information or produce a named legal downstream package, including every
selector, response/activity, synchronization, nuisance-survival, anchor, and
source-coverage gate.

The theorem neither starts permanent restriction/extraction/gluing nor
changes the global status.
