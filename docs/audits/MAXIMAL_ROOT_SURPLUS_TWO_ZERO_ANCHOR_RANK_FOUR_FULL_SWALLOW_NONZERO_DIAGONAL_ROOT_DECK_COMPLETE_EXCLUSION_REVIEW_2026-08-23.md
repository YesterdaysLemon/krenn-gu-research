# Hostile review: zero-anchor rank-four full-swallow nonzero diagonal root-deck exclusion

## Verdict

**ACCEPT after three bounded independent mathematical attacks, owning-interface
review, exact primary replay, and a genuinely independent no-import audit.**
In characteristic zero, on every fixed-residual zero-anchor full-swallow
fibre,

```text
rank B_Q^anc=4
  => q=0 and p=epsilon_A(q)=0.
```

The new proof excludes `0!=q in Delta`; `GLS43` independently excludes
`q notin Delta`.  Hence the full-swallow branch on `D(p)` has nuisance rank
at least five.  The conclusion is pointwise at the evaluated contraction: it
does not assert that the polynomial family `q` vanishes identically.

The surviving rank-four `q=0` fibre, ranks five through nine, raw escape,
pure-core survival, every response/activity/synchronization/nuisance/anchor/
receiver gate, arbitrary-root source coverage, and strategic-node closure
remain open.  The global Krenn--Gu conjecture remains **UNRESOLVED**.

## Reviewed artifacts

- [`GLS44 theorem`](../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_RANK_FOUR_FULL_SWALLOW_NONZERO_DIAGONAL_ROOT_DECK_COMPLETE_EXCLUSION_THEOREM.md)
- [`focused exact primary verifier`](../../claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_rank_four_full_swallow_nonzero_diagonal_root_deck_complete_exclusion.py)
- [`independent no-import audit`](../../claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_rank_four_full_swallow_nonzero_diagonal_root_deck_complete_exclusion.py)
- owning interfaces `GLS8`, `GLS35`, `GLS36`, `GLS39`, `GLS40`, and `GLS43`
- downstream boundary interfaces `GLS41` and `GLS42`
- the current-frontier, supply/target DAG, and arbitrary-order README updates.

Three read-only research passes attacked distinct risks.  One re-derived the
new theorem with dual cross-block and quotient functionals and audited
transpose symmetry.  A second classified the complete `q=0` residual-shore
boundary and checked that the proof did not claim a selector on `p=0`.  A
third ran exact finite-field and rational searches for missed rank-four
families.  Those searches found no counterexample but remain sampled
calibration evidence, not a proof.  The written argument and no-import audit
are independent of them.

## Owning-interface and quantifier audit

`GLS36` gives the whole-domain incidence presentation

```text
B_Q^anc=im sigma_Q,

sigma_(s,u)(v)=a_s tensor Y_u(v)+X_u(v) tensor b_s,
sigma_(u,v)(x tensor y)
 =X_u(x) tensor Y_v(y)+X_v(y) tensor Y_u(x).
```

Full swallow and rank four put every complete labelled component in one
space `B=Delta+K w`.  Since `Delta subset B`, the total left and right
factor spans are both `K^3`.  The proof uses all vectors of every promoted
domain.  It does not introduce a same-label port--port component, choose an
incidence minor, assume selected activity, or replace the family by one
generic vector.  The residual contraction is arbitrary, so rank-drop and
divisor fibres are included.

`GLS40` is used only to identify the rank-four diagonal stratum and its
one-dimensional excess.  `GLS41` and the transverse-cylinder part of
`GLS40` live on `D(p)` and cannot be applied to the surviving `q=0`, `p=0`
fibre.

## Rank-two diagonal attack

Write

```text
q=[a_0|a_1] J [b_0|b_1]^T,   J=[[0,1],[1,0]].
```

If `rank q=2`, both residual shore maps are injective and their images equal
the row and column support plane `P` of `q`.  Let `c` be the missing colour.
The dual cross-block map

```text
T(M)=((id_P tensor e_c^*)M,(e_c^* tensor id_P)M)
```

kills `Delta`, hence has image dimension at most one on `B`.  For a fixed
port value `(x,y)`, however, the two residual-label combinations map as

```text
t -> (y_c A t,x_c C t).
```

Injectivity of both shore maps makes this a rank-two map whenever `x_c` or
`y_c` is nonzero.  Thus both missing-colour coordinates vanish for every
value in every promoted domain.  All residual--port and port--port columns
then lie in `P tensor P`, contradicting `E_cc in B`.

This is a whole-family rank argument.  No nonzero port coordinate is selected
or divided out, and the zero-port fibre is included.

## Rank-one diagonal attack

If `q=kappa E_cc` has rank one, at least one residual shore is a line.
Transposition preserves `Delta`, rank, full swallow, and the GLS36 family, so
take `A=K e_c`.  For the quotient `pi:K^3 -> W=K^3/A`, full left generation
gives

```text
span pi(X)=W,             dim W=2,
W tensor K b_s subset (pi tensor id)(B)
```

for each residual label `s`.  Applying `id_W tensor e_c^*` kills the
projected diagonal, and the sole excess line contributes at most one
dimension.  If `(b_s)_c` were nonzero, the displayed two-dimensional tensor
space would map onto all of `W`, a contradiction.  Hence both right residual
vectors have zero `c` coordinate, contradicting the nonzero `(c,c)` entry of

```text
q=e_c tensor (lambda_0 b_1+lambda_1 b_0).
```

No `b_s` is assumed nonzero, and zero or cancelling residual slices are
covered.

## Exhaustion and successor boundary

Every root companion has rank at most two.  A nonzero diagonal root deck has
rank one or two, both excluded above.  `GLS43` excludes the complementary
off-diagonal stratum, so rank-four full swallow forces `q=0`, then `p=0`.
Together with the `GLS39` rank floor, `D(p)` begins at rank five.

The review also independently derived, but GLS44 does not publish, the next
`q=0` shore-profile reduction.  The profiles `(2,0)`, `(0,2)`, `(1,0)`,
`(0,1)`, and dense `(1,1)` are dimensionally impossible.  The honest
survivors are `(0,0)` and sparse `(1,1)`, the latter normalizable after label
exchange to

```text
a_0=a, b_0=t b, a_1=b_1=0,       t!=0.
```

This is recorded only as the smallest candidate successor obligation until
it receives its own theorem statement, focused verifier, independent audit,
frontier integration, and publication replay.  It neither proves that a
surviving rank-four family exists nor supplies a target receiver.

## Exact computational audits

The SymPy primary verifies the symbolic cross-block minors, exact rank-two
and rank-one fixtures, residual factorization profiles, and representative
zero-boundary fibres.

The no-import audit imports neither repository code nor a third-party
package.  It uses a separate `Fraction` elimination routine, dual-functional
representations of both obstructions, and exhausts all `3^12` residual
factorizations over `F_3` to check the rank/drop classifications.  That finite
census is an implementation audit of the structural cases; the
characteristic-zero result rests on the written proof.

## Verification replay

The candidate-tree publication replay includes:

```text
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_rank_four_full_swallow_nonzero_diagonal_root_deck_complete_exclusion.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_rank_four_full_swallow_nonzero_diagonal_root_deck_complete_exclusion.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_incidence_image_common_row_silence_and_labelwise_lift_sharpness.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_incidence_image_common_row_silence_and_labelwise_lift_sharpness.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_complete_pairwise_diagonal_family_rank_bound_and_minimal_raw_swallow_exclusion.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_complete_pairwise_diagonal_family_rank_bound_and_minimal_raw_swallow_exclusion.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_full_swallow_aggregate_deck_excess_syzygy_and_transverse_cylinder.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_full_swallow_aggregate_deck_excess_syzygy_and_transverse_cylinder.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_rank_four_full_swallow_off_diagonal_root_deck_complete_exclusion.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_rank_four_full_swallow_off_diagonal_root_deck_complete_exclusion.py
```

Focused checks, dependency replays, repository QA, exact-head hosted CI,
merge verification, and a fresh postmerge replay are publication gates, not
assumed facts.

## Unresolved boundary

The smallest rank-four branch is `q=0`, hence `p=0`.  Even after the candidate
shore reduction, the `(0,0)` and sparse `(1,1)` complete pair-family cores
remain.  They lie outside the current transverse selector receiver.  Ranks
five through nine, raw escape, response/activity/synchronization, complete
nuisance survival, anchors, a named receiver, arbitrary-root source cover,
strategic-node closure, and global resolution all remain open.
