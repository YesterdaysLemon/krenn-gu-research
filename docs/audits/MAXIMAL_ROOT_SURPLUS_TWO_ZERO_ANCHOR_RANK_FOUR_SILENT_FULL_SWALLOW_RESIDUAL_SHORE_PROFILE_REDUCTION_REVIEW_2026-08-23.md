# Hostile review: zero-anchor rank-four silent full-swallow residual-shore profile reduction

## Verdict

**ACCEPT after three bounded independent attacks, owning-interface review,
exact primary replay, and a genuinely independent no-import audit.**  In
characteristic zero, every zero-anchor rank-four full-swallow point has
`q=p=0` by `GLS44`, and its residual shore profile is exactly one of the two
unexcluded cases

```text
(dim A,dim C)=(0,0),

(dim A,dim C)=(1,1) with one common active residual label.
```

The second profile can be written, after exchanging residual labels and
choosing generators of the two shore lines, as

```text
a_0=a, b_0=t b, a_1=b_1=0,       t!=0.
```

This does not rescale a physical residual vector.  The scalar `t` only records
the chosen generator of the abstract right shore line.

Neither survivor is excluded and neither is proved realizable.  Ranks five
through nine, raw escape, nonzero anchor, response/activity/synchronization,
complete nuisance survival, anchors, a named receiver, arbitrary-root source
coverage, and strategic-node closure remain open.  The global Krenn--Gu
conjecture remains **UNRESOLVED**.

## Reviewed artifacts

- [`GLS45 theorem`](../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_RANK_FOUR_SILENT_FULL_SWALLOW_RESIDUAL_SHORE_PROFILE_REDUCTION_THEOREM.md)
- [`focused exact primary verifier`](../../claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_rank_four_silent_full_swallow_residual_shore_profile_reduction.py)
- [`independent no-import audit`](../../claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_rank_four_silent_full_swallow_residual_shore_profile_reduction.py)
- owning interfaces `GLS8`, `GLS35`, `GLS36`, `GLS39`, and `GLS44`
- boundary interfaces `GLS40` and `GLS41`
- the current-frontier, supply/target DAG, and arbitrary-order README updates.

One read-only pass independently re-derived the full profile theorem and
tested `14,641` exact rational dense systems.  A second designed and checked a
different finite-geometry audit, including the complete `F_3` residual atlas
and abstract Grassmannian endgame.  A third attacked the two survivors,
unified them as one complete pair-family problem, and deliberately stopped
without promoting sampled negative evidence.  No pass found a counterexample
to GLS45.

## Owning-interface and quantifier audit

`GLS36` gives, at each fixed but arbitrary residual contraction,

```text
B=B_Q^anc=im sigma_Q,

sigma_(s,u)(v)=a_s tensor Y_u(v)+X_u(v) tensor b_s,
sigma_(u,v)(x tensor y)
 =X_u(x) tensor Y_v(y)+X_v(y) tensor Y_u(x).
```

The complete image lies in `(A+X) tensor (C+Y)`.  Since full swallow gives
`Delta subset B`, the three coordinate diagonal tensors force

```text
A+X=C+Y=K^3.
```

This is an aggregate whole-domain conclusion.  The proof never chooses one
nonzero port vector, assumes a same-label port self-pair, or replaces a map by
one generic value.  It is pointwise on every incidence-rank, shore-rank,
deck, divisor, and residual fibre.

`GLS44` is used only to make `q=0` automatic for the integrated rank-four
corollary.  `GLS40` still supplies the one-dimensional aggregate excess, but
its transverse-cylinder theorem and `GLS41` live on `D(p)` and cannot be
applied on the surviving `q=p=0` fibre.

## Zero-deck profile atlas

Write

```text
q=A_0 J C_0^T,       J=[[0,1],[1,0]].
```

If `rank A_0=2`, injectivity and `q=0` force `C_0=0`; transposition gives the
mate.  Thus the complete initial atlas is

```text
(2,0),(0,2),(1,1),(1,0),(0,1),(0,0).
```

In rank `(1,1)`, write `a_s=lambda_s a`, `b_s=mu_s b`.  The single equation

```text
lambda_0 mu_1+lambda_1 mu_0=0
```

has two support types.  If all coefficients are nonzero, the profile is
dense.  If one coefficient vanishes, the equation forces the matching
coefficient on the other shore to vanish, leaving exactly one common active
label.  There is no opposite-label sparse branch.

## Fixed-factor exclusions

For nonzero `a`, a fixed-left-factor space meets the three-colour diagonal in
dimension at most one:

```text
dim((K a tensor V) intersect Delta)<=1.
```

A nonzero diagonal tensor in that space has rank one, so it is one coordinate
axis and forces `a` onto the same axis.  This elementary observation gives
both one-shore-zero exclusions:

- rank `(2,0)` contains `A tensor K^3`, dimension six;
- rank `(1,0)` contains `K a tensor K^3`, whose sum with `Delta` has dimension
  at least five.

Transposition excludes `(0,2)` and `(0,1)`.  No characteristic or divisor
open is used here.

## Dense rank-one/rank-one attack

Name the actual physical residual vectors `a=a_0`, `b=b_0`.  Density and
`q=0` give one `t!=0` with

```text
a_1=t a,                b_1=-t b.
```

For every port value `(x,y)`, its two residual columns are

```text
m_0=a tensor y+x tensor b,
m_1=t(a tensor y-x tensor b).
```

Their sum and difference isolate both channels because `2t!=0`:

```text
K a tensor Y subset B,        X tensor K b subset B.
```

Full generation makes `dim X,dim Y>=2`.  A three-dimensional shore would
already give dimension at least five with `Delta`, so both have dimension
two.  The fixed-factor intersection lemma then forces `a=e_i`, `b=e_j`, with
each fixed-factor space contributing the same unique non-diagonal line in
`B/Delta`.  Choosing zero-diagonal representatives gives a literal equality

```text
e_i tensor y' = c x' tensor e_j.
```

It follows that `y'` is proportional to `e_j` and `x'` to `e_i`; hence

```text
X=Y=span{e_i,e_j}.
```

Both residual shore lines are already in those planes, contradicting
`A+X=C+Y=K^3`.  The only new characteristic gate is `2!=0`; characteristic
zero is sufficient.

The dimension-five lower bound is sharp as an ambient statement.  Over
`Q`, taking

```text
a=e_2, b=e_1,
X=span{e_0,e_1}, Y=span{e_0,e_2}
```

makes `span(Delta,a tensor Y,X tensor b)` have dimension exactly five.  GLS45
therefore claims no rank-six bound.

## Independent computational audit

The SymPy primary verifies the factorization and polarization identities,
fixed-factor intersection ranks, the quotient-line support endgame, both
surviving zero-deck boundaries, and the sharp rank-five ambient fixture.

The no-import audit imports no repository module or third-party package.  Its
separate `F_3` Gaussian elimination exhausts all `3^12` residual quadruples.
Exactly `4,161` have `q=0`, with profile counts

```text
(0,0):1, (0,1):104, (0,2):624,
(1,0):104, (1,1):2704, (2,0):624.
```

It separately checks all projective fixed factors and quotient row/column
lines.  Finally it forgets the port maps and exhausts all `13` projective
shore lines and all `13` planes plus `K^3` for both aggregate port shores.
Among `16,900` full-generation dense cases, the exact span-rank histogram is

```text
rank 5: 54, rank 6: 2490, rank 7: 12684, rank 8: 1672.
```

This finite census is an independent implementation and falsification audit,
not the characteristic-zero proof.  The written dimension/intersection proof
carries the theorem.

## Survivor attack and exact next obligation

The two survivors unify without a support atlas.  Adjoin the residual labels
as in the `GLS39` auxiliary-label interface.  The residual-free profile adds
two zero labels.  The sparse profile adds one nonzero label with paired
incidence `(a,tb)` and one zero label; its cross polarization with a port is
exactly the residual--port column

```text
a tensor Y_u+tX_u tensor b.
```

Thus both reduce to the same complete distinct-label problem: can arbitrary
label maps have all cross polarizations in, and together span,

```text
B=Delta direct-sum K f?
```

The excess representative `f` may be chosen purely off-diagonal, so membership
is exactly `offdiag(mu_(s,t)) in K f` for every distinct label pair.  The
sparse auxiliary self-pair `2t a tensor b` is not a GLS36 label and supplies
no extra equation.

Exact `F_3` sampling found no rank-four control in one million `(2,2)`, half
a million `(2,3)`, three hundred thousand `(3,3)`, or one million full
compatibility-kernel trials.  Those are experiments only.  The smallest next
load-bearing obligation is a support-free rank-four pair-family theorem, or
an exact rational countermodel.

## Verification replay

The candidate-tree publication replay includes:

```text
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_rank_four_silent_full_swallow_residual_shore_profile_reduction.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_rank_four_silent_full_swallow_residual_shore_profile_reduction.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_incidence_image_common_row_silence_and_labelwise_lift_sharpness.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_incidence_image_common_row_silence_and_labelwise_lift_sharpness.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_complete_pairwise_diagonal_family_rank_bound_and_minimal_raw_swallow_exclusion.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_complete_pairwise_diagonal_family_rank_bound_and_minimal_raw_swallow_exclusion.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_rank_four_full_swallow_nonzero_diagonal_root_deck_complete_exclusion.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_rank_four_full_swallow_nonzero_diagonal_root_deck_complete_exclusion.py
```

Focused checks, dependency replays, repository QA, exact-head hosted CI,
merge verification, and a fresh postmerge replay are publication gates, not
assumed facts.

## Unresolved boundary

The surviving rank-four incidence problem is the unified complete
pair-family above.  Even its exclusion would leave ranks five through nine,
raw escape, nonzero anchor, response/activity/synchronization, complete
nuisance survival, anchors, a receiver, source cover, and strategic closure
open.  No global-resolution claim is made.
