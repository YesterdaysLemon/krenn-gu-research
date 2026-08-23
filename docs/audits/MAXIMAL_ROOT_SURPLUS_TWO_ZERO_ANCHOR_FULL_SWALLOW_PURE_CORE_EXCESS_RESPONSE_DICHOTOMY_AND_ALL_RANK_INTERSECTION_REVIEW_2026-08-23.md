# Hostile review: zero-anchor full-swallow pure core, excess response, and all-rank intersection

## Verdict

**ACCEPT after mathematical, interface, all-fibre, independence, and scope
audit.**  On every declared `D(p)` full-swallow fibre, `P_Q` canonically
identifies the root excess quotient with the quotient of the `GLS40` cylinder
root factor by its projected diagonal core.  The resulting cylinder exact
sequence is generally nonsplit; no complement is claimed or chosen.

Projecting the complete `GLS22` target equation to the excess quotient kills
all three pure columns.  A surviving desired excess class therefore forces
zero physical response.  Every useful nonzero-response desired class is
represented in the projected pure core, and its exact pointwise obstruction
is the intersection of that core with the complete labelled nuisance.  The
core has `27` rows when `q notin Delta` and `18` when `q in Delta`, independently
of the nuisance rank `k`.

Nothing proves that a core class survives or that a response is nonzero.
Synchronization, selected activity, additional/common downstream nuisance
gates, a named receiver, `p=0` source coverage, raw-escape attachment, and
node closure remain open.  The global Krenn--Gu conjecture remains
**UNRESOLVED**.

## Reviewed artifacts

- [`GLS41 theorem`](../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_FULL_SWALLOW_PURE_CORE_EXCESS_RESPONSE_DICHOTOMY_AND_ALL_RANK_INTERSECTION_THEOREM.md)
- [`focused primary verifier`](../../claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_full_swallow_pure_core_excess_response_dichotomy_and_all_rank_intersection.py)
- [`independent no-import audit`](../../claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_full_swallow_pure_core_excess_response_dichotomy_and_all_rank_intersection.py)
- owning interfaces `GLS5`, `GLS8`, `GLS22`, `GLS23`, and `GLS40`
- the `GLS41` current-frontier, supply/target DAG, and arbitrary-order README
  entries.

Three read-only hostile-review passes checked the tranche.  Two
non-originating reviewers independently rederived the quotient, exact
sequence, tensor-zero dichotomy, and intersection criterion.  The originating
construction lane separately cross-checked the written source/target
interfaces and scope.  Genuine implementation independence is supplied by
the separately entered no-import audit, not merely by review labels.

## Root quotient and canonical-dual audit

Retain

```text
B=B_Q^anc,              S=Delta+Kq,
C_Q=P_Q(B),             R_Q=P_Q(Delta),
P_Q=p id-q tensor epsilon_A,       p!=0.               (1)
```

On `D(p)`, `ker P_Q=Kq`.  Full swallow puts `q` in `B`, so
`P_Q:B->C_Q` is surjective with that kernel.  More strongly,

```text
(P_Q|B)^(-1)(R_Q)=Delta+Kq=S.                         (2)
```

Indeed, `P_Q(b)=P_Q(d)` for some `d in Delta` exactly when
`b-d in Kq`.  Thus the induced map is the canonical isomorphism

```text
B/S isomorphic to C_Q/R_Q.                            (3)
```

There is no chosen complement in (3).  The two pointwise strata are exact:

```text
q notin Delta: dim R_Q=3, dim C_Q/R_Q=k-4;
q in Delta:     dim R_Q=2, dim C_Q/R_Q=k-3.           (4)
```

The second line is still on `D(p)`, so `q!=0`.  `GLS40` identifies

```text
E_Q^exc=sigma_Q^*(Ann(S)) isomorphic to (B/S)^*.      (5)
```

Combining (3)--(5) proves the claimed canonical duality.  The theorem types
this as a dual quotient, not as primal coefficient directions outside `S`.

## Cylinder exact-sequence audit

For a promoted pair target, set

```text
L=L_C^cyl=C_Q tensor V_C^*,
R=R_C^pure=R_Q tensor V_C^*,
N=N_C^tr subset L.                                    (6)
```

The nuisance containment is exactly `GLS40` and retains all labelled nuisance
summands.  For any three finite-dimensional spaces as in (6), the quotient
map gives

```text
0 -> R/(N intersect R)
  -> L/N
  -> (L/R)/pi(N)
  -> 0.                                               (7)
```

The first map is injective because its kernel is `N intersect R`; the last
map is surjective; and the middle kernel is `(R+N)/N`.  This proves exactness
without splitting (7).

All three pure columns lie in `R`.  The complete `GLS22` identity is

```text
sum_c alpha_c[d_(C,c)^tr] tensor w_(S_C,c)
  =[t_C] tensor P_(S_C)(H;z_Q)                        (8)
```

in `L/N`.  Projecting (8) through the right map in (7) gives

```text
[pi(t_C)] tensor P_(S_C)(H;z_Q)=0.                   (9)
```

Over the declared field, a pure tensor is zero exactly when one factor is
zero.  Hence a nonzero desired excess class forces zero response.  Conversely,
a nonzero response makes `[t_C]` lie in the image of `R/(N intersect R)`.

The selector sentence was checked carefully.  A cylinder functional which
kills `N` and `R` but is nonzero on `t_C` factors through the right quotient.
It extends linearly to the full `K_C^tr` because `N subset L`, continues to
kill the complete nuisance, and can be rescaled to the exact `GLS22`
normalization.  Equation (9) makes the resulting legal selector
response-zero.  No receiver, synchronization, or activity conclusion is
drawn.

## Pure-core rank and all-fibre audit

Since

```text
im D_C^tr subset R,                                   (10)
```

the injection on the left of (7) identifies the span of the pure columns
modulo `N` with their span modulo `N intersect R`.  Therefore

```text
rank[N|D_C^tr]-rank N
 =rank[(N intersect R)|D_C^tr]-rank(N intersect R)    (11)
```

on every point, with no constant-rank assumption.  Because
`dim V_C^*=9`, (4) gives the exact core sizes `27` and `18`.

The all-fibre implementation uses the canonical possibly rank-dropping map

```text
A_C=(P_Q|Delta) tensor id_(V_C^*):
    Delta tensor V_C^* -> K_C^tr.                     (12)
```

Its fixed domain has dimension `27`, while its image rank is `27` or `18`.
For any complete nuisance presentation `B_C`, the kernel

```text
ker[B_C|-A_C]                                         (13)
```

projects to exactly the `A_C`-preimage of `N intersect R`, and applying
`A_C` gives the intersection.  Thus the rank drop is retained literally;
there is no transported generic image basis.  Over a parameter family the
kernel projection can jump, so a complete module/saturated Fitting encoding
is required for a universal locus claim.

## Sharp projection/intersection boundary

The exact family

```text
L=K e_0 direct-sum K e_1,
R=K e_0,
N_t=span{e_1,t e_0},
D=e_0                                                (14)
```

has the same full projection `pi(N_t)=K[e_1]` on every fibre.  At `t!=0`,
`N_t intersect R=R` and `D` is swallowed; at `t=0`, the intersection is zero
and `D` survives.  This is a sharp abstract module boundary: a generic
excess projection does not determine pointwise core survival.

The inherited `GLS40` rank-six interface supplies the complementary warning.
Its excess rows are labelwise active, but every detected label has zero
assigned deck.  It is not proved physical.  Neither control is a witness or
counterexample.

## Corrections required by hostile review

The review required and verified these publication corrections:

1. replace language suggesting a canonical cylinder splitting by a canonical
   core subspace and associated quotient;
2. identify `p!=0` as the `GLS22` localization, not the entire common source
   gate;
3. type, extend, and normalize the cylinder functional before calling it a
   legal full selector;
4. use `im D_C^tr` rather than treating the pure-column matrix as a subspace;
5. retain the common source condition `H_Q(z_Q)p(z_Q)!=0` in the remaining
   source-level obligation; and
6. replace a per-fibre injective core basis by the canonical rank-dropping map
   (12).

All corrections are present in the accepted artifacts.

## Exact computational audits

The SymPy primary replays both root strata for every `k=4,...,9`, including
the `C_Q`, pure-core, and excess ranks.  Twelve deterministic cylinder
fixtures verify exact-sequence dimensions and ambient/core pure-rank equality.
It also checks the constant-projection jumping family.

The no-import audit uses only `Fraction` row reduction.  It independently
checks the two quotient profiles, all `64` subsets of a separate small
nuisance-column family, response-dichotomy fixtures, and a separately entered
jumping family.  It imports neither the primary verifier nor repository
mathematics code.

## Verification replay

The following pass on the candidate tree:

```text
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_full_swallow_pure_core_excess_response_dichotomy_and_all_rank_intersection.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_full_swallow_pure_core_excess_response_dichotomy_and_all_rank_intersection.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_pointwise_selector_failure_and_decomposable_retraction_boundary.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_pointwise_selector_failure_and_decomposable_retraction_boundary.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_promoted_two_probe_one_target_attachment_and_pointwise_failure_reduction.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_promoted_two_probe_one_target_attachment_and_pointwise_failure_reduction.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_promoted_all_port_transverse_quotient_and_projective_synchronization_failure.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_promoted_all_port_transverse_quotient_and_projective_synchronization_failure.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_promoted_transverse_complete_nuisance_decomposition_and_top_anchor_dichotomy.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_promoted_transverse_complete_nuisance_decomposition_and_top_anchor_dichotomy.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_full_swallow_aggregate_deck_excess_syzygy_and_transverse_cylinder.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_full_swallow_aggregate_deck_excess_syzygy_and_transverse_cylinder.py
```

The focused scripts, Ruff, and all five owning primary/audit pairs pass.
Candidate-tree hygiene compiles `2306` Python files and resolves all `1439`
Markdown files; the mandatory unit suites pass `191+14` tests.  Link rewrite
is idempotent with zero changes, and cached diff checking passes.  Exact-head
hosted CI and merged-main replay remain publication gates to be recorded
before and after merge.

## Unresolved boundary

At a common contraction retaining `H_Q(z_Q)p(z_Q)!=0`, force

```text
im D_C^tr not subset N_C^tr intersect R_C^pure       (15)
```

for one eligible pair, or contradict simultaneous containment using the
complete same-graph pure/mixed and principal-deck equations.  A rank rise
already supplies that chosen row's complete-nuisance selector, but every
additional/common downstream nuisance gate, response synchronization,
selected activity, and named receiver remains.  The zero-anchor top target is
dead.  Silent `p=0` source coverage and raw escape are separate.
