# Hostile review: zero-anchor minimal raw swallow and mixed-only faithfulness no-go

## Verdict

**ACCEPT after required corrections.**  The arbitrary-root minimal-rank
two-shore exclusion is type-correct, pointwise, and division-free.  The
four-port no-go is exactly replayed by independent implementations.  This
tranche excludes only the full-swallow nuisance-rank-three fibre with both
residual shores of rank two.  It neither excludes the shore-rank-drop or
rank-at-least-four alternatives nor supplies an original target selector,
response/activity, synchronization, nuisance survival, arbitrary-root source
cover, downstream attachment, or strategic-node closure.

The global Krenn--Gu conjecture remains **UNRESOLVED**.

## Reviewed artifacts

- [`GLS37 theorem`](../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_MINIMAL_RAW_SWALLOW_INCIDENCE_CLASSIFICATION_AND_MIXED_ONLY_FAITHFULNESS_NO_GO_THEOREM.md)
- [`focused primary verifier`](../../claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_minimal_raw_swallow_incidence_classification_and_mixed_only_faithfulness_nogo.py)
- [`independent no-import audit`](../../claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_minimal_raw_swallow_incidence_classification_and_mixed_only_faithfulness_nogo.py)
- the corrected [`GLS36 theorem`](../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_INCIDENCE_IMAGE_COMMON_ROW_SILENCE_AND_LABELWISE_LIFT_SHARPNESS_THEOREM.md)
  and its amended [hostile review](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_INCIDENCE_IMAGE_COMMON_ROW_SILENCE_AND_LABELWISE_LIFT_SHARPNESS_REVIEW_2026-08-22.md)
- the `GLS37` entries in [`current frontier`](../current-frontier.md) and the
  [`supply/target node DAG`](../history/handoffs/MAXIMUM_ROOT_SURPLUS_TWO_SUPPLY_TARGET_NODE_DAG_2026-08-20.md)
- owning interfaces `GLS8`, `GLS35`, and `GLS36`.

The hostile mathematical, scope, and implementation reviews were read-only
and separate from the primary derivation.  The computational audit is an
additional standard-library implementation, not an import or wrapper around
the primary.

## Required corrections found and resolved

### 1. Root-companion grade correction

The first merged `GLS36` proof described a pair companion `G_D^A` as the
three perfect matchings on `A union D`, then killed the internal-label term by
`omega=0`.  The owning `GLS8` definition instead makes this a grade-zero
two-root/two-label companion containing only the two root-to-label
bijections.  The internal-label matching is not part of that companion; the
top raw summand is separately `K omega`.

The corrected `GLS36` proof now derives

```text
a_s tensor Y_u(x)+X_u(x) tensor b_s,
X_u(x) tensor Y_v(y)+X_v(y) tensor Y_u(x)
```

directly from the owning grade.  On `omega=0`, its formula
`B_Q^anc=im sigma_Q` and every rank, lift, and sharpness conclusion are
unchanged.  No nonzero-anchor consequence is inferred from the old
pre-vanishing expression.

### 2. Full-swallow quantifier correction

The first GLS37 status paragraph said only that the three pure probes were
swallowed, while the proof also uses `q in B_Q^anc`.  The accepted statement
defines full swallow explicitly as

```text
q,r_0,r_1,r_2 in B_Q^anc.
```

The formal theorem already contained all four hypotheses.  Navigation and
scope prose now use the same definition and state the eligible promoted root
range `r>=3` explicitly.

### 3. Independent finite-leaf coverage

The first no-import audit reconstructed the exact graph and its support but
left several named consequences implicit.  The accepted audit now directly
asserts, using only its own `Fraction` data,

```text
q=r_1+r_2,             p=2,
H_Uhat(0000)=1/2,      pH_Uhat(0000)=1,
Q-contracted coefficient at 0000=diag(0,1/2,1/2),
all 78 mixed port words vanish,
normalized pure-port defect ranks=(3,1,1).
```

## Mathematical audit

### Minimal-rank two-shore exclusion

Full swallow and `dim B_Q^anc=3` force

```text
B_Q^anc=Delta=span{r_0,r_1,r_2}.
```

If the residual shore matrices `A=(a_0,a_1)` and `C=(b_0,b_1)` both have
rank two, then

```text
q=A [[0,1],[1,0]] C^T
```

has rank two.  Because `q` is diagonal, its column and row spaces are the same
two-colour coordinate plane on their respective shores.  In every one-Q
incidence column, the missing-colour row and column equations force both port
incidence vectors into those shore planes.  Pair columns are then supported
there as well.  Since every incidence column also belongs to `Delta`, the
entire image lies in a two-dimensional diagonal intersection.  This
contradicts `B_Q^anc=im sigma_Q` of rank three.

The argument selects no minor, divides by no shore coordinate, and does not
assume a generic residual, response, or nuisance rank.  It applies pointwise
at every promoted root order `r>=3`.  Since each residual shore has rank at
most two, the remaining full-swallow cover is exhaustive:

```text
rank B_Q^anc=3 with at least one shore rank <=1,
or rank B_Q^anc>=4.
```

### Channel refinement

On the hypothetical intermediate two-colour plane, the one-Q off-diagonal
equations split into two two-by-two kernels.  Each has dimension at most one,
and a nonzero kernel vector has both entries nonzero.  Exact charts realize
total channel dimensions zero, one, and two.  Pair-label diagonality prevents
one nonzero channel from occurring at two distinct ports in characteristic
zero.  This local description is correct but is superseded, on the complete
rank-three full-swallow fibre, by the image-rank contradiction above.

### Mixed-only no-go

Independent exact replay of the GLS35 graph confirms

```text
rank B=rank[B|q]=8,
rank[B|r_c]=9 for c=0,1,2,
rho_Q=0,
H_Uhat=(1/2)(e_0^*)^tensor4.
```

Thus `q` is swallowed but full swallow fails.  On `Z_mix`, both `rho_Q` and
`H_Uhat` vanish, so the GLS36 kernel lift holds for every swallowing
certificate.  The complete state is exactly

```text
(1/2)|11000000>+(1/2)|22000000>,
```

and the only contracted port word is the pure word `0000`, with probe matrix
`diag(0,1/2,1/2)`.  The control therefore proves that q-swallow, a nonzero
local residual-absent output anchor, and every mixed-port lift do not imply a
complete target.  It does not show that a full-swallow hypothetical witness
exists or that the pure-port equation is the only possible additional gate.

## Verification replay

The following focused commands passed on the candidate tree:

```text
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_minimal_raw_swallow_incidence_classification_and_mixed_only_faithfulness_nogo.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_minimal_raw_swallow_incidence_classification_and_mixed_only_faithfulness_nogo.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_incidence_image_common_row_silence_and_labelwise_lift_sharpness.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_incidence_image_common_row_silence_and_labelwise_lift_sharpness.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_raw_root_deck_quotient_and_output_coefficient_separation_nogo.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_raw_root_deck_quotient_and_output_coefficient_separation_nogo.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_promoted_two_probe_one_target_attachment_and_pointwise_failure_reduction.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_promoted_two_probe_one_target_attachment_and_pointwise_failure_reduction.py
```

The primary uses exact SymPy matrices and direct perfect-matching
coefficients.  The no-import audit uses only the standard library, exact
`Fraction` row reduction over `496` independently reconstructed shore charts,
and sparse matching-state expansion of an independently rebuilt graph.

## Unresolved boundary

The smallest zero-anchor full-swallow obligation is to exclude or attach both
surviving alternatives: nuisance rank three with a residual shore rank at
most one, and nuisance rank at least four.  A continuation of this
full-swallow route must use additional full-witness information absent from
the control and should retain the complete pure-port and mixed GHZ equations
on the same graph while covering all residual/divisor/rank fibres.  Before
entering a named downstream theorem it
must separately prove legal selector survival, nonzero physical response and
selected activity, synchronization, complete labelled nuisance survival,
the required anchor, and the arbitrary-root source interface.

Nothing in this tranche changes the nonzero-anchor marginal or
double-transverse branches, closes the source-to-attachment node, begins
permanent restriction/extraction/gluing, or resolves the global conjecture.
