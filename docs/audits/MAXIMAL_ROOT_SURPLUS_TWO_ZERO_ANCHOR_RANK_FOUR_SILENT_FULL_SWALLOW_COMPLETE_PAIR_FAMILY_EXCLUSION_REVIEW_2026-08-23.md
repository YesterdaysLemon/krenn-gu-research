# Hostile review: zero-anchor rank-four silent full-swallow complete-pair exclusion

## Verdict

**ACCEPT after a dedicated proof audit, independent finite quotient census,
owning-interface review, and dependency replay.**  The `GLS47` argument
excludes both complete-pair cores left by `GLS45`.  Combined with
`GLS43`--`GLS44`, every zero-anchor rank-four full-swallow fibre is pointwise
empty and the full-swallow nuisance-rank floor is five.

The theorem does not force silent full swallow, exclude ranks five through
nine, attach raw escape, cover nonzero anchor, or supply any original
response/activity/synchronization/nuisance/anchor/receiver/source gate.  The
strategic node and the global Krenn--Gu conjecture remain **UNRESOLVED**.

## Reviewed artifacts

- [`GLS47 theorem`](../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_RANK_FOUR_SILENT_FULL_SWALLOW_COMPLETE_PAIR_FAMILY_EXCLUSION_THEOREM.md)
- [`focused exact primary verifier`](../../claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_rank_four_silent_full_swallow_complete_pair_family_exclusion.py)
- [`independent no-import audit`](../../claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_rank_four_silent_full_swallow_complete_pair_family_exclusion.py)
- owning interfaces `GLS36`, `GLS39`, and `GLS43`--`GLS46`
- the current-frontier, supply/target DAG, and arbitrary-order README updates.

One bounded attack first found the complete triangle lock after `GLS46` had
isolated the two fourth-direction mechanisms.  A separate dedicated audit
independently rederived the proof and checked for same-label use, algebraic-
closure dependence, cut mismatch, and exact countermodels.  The artifact
review then checked the written quantifiers and both verifier boundaries.

## Triangle synchronization audit

`GLS46` supplies one triangle of pair maps whose diagonal images are three
independent lines.  On edge `ij`, write its physical diagonal projection as

```text
beta_(i,j)(v_i,v_j)d_(i,j).
```

Each `beta_(i,j)` is a nonzero bilinear polynomial.  Their product is nonzero
in the polynomial ring on the direct sum of the three triangle domains.
Because a characteristic-zero field is infinite, one `K`-rational triple
makes all three factors nonzero.  This argument does not pass to an algebraic
closure and does not select a generic divisor or invert a coefficient.

The synchronized outputs have independent physical diagonal projections, so
their span is a graph over `Delta`, not necessarily `Delta` itself.  This
distinction is retained throughout the proof.

## Invertibility and normalization audit

Let `X=[x_0|x_1|x_2]` and `Y=[y_0|y_1|y_2]` be the selected factor matrices.
If `h^T X=0`, left multiplication kills the entire graph

```text
{D+ell(D)f:D in Delta}.
```

The map `D |-> h^T D` has image dimension equal to the number of nonzero
coordinates of `h`, but the graph equation confines it to one line.  Thus
`h` has at most one nonzero coordinate.  Testing the corresponding diagonal
matrix contradicts `f_(k,k)=0`.  Hence `X` is invertible; transposition gives
`Y`.

The change `M |-> X^(-1)MY^(-T)` sends the three synchronized outputs to
the symmetric zero-diagonal basis `S_(0,1),S_(0,2),S_(1,2)`.  Therefore

```text
B'=Sym_0 direct-sum K G.
```

It also sends the physical diagonal tensors to three rank-one matrices whose
left factors and right factors are independently bases.  No physical
diagonal meaning is inferred from the transformed ordinary diagonal until
the complement is normalized below.

## Rank-one complement audit

`Sym_0` contains no nonzero rank-one matrix: its three principal `2 by 2`
minors are the negatives of the squares of its off-diagonal coordinates.
Thus every transformed physical rank-one matrix has nonzero quotient
coefficient.  Normalize those coefficients to obtain three rank-one matrices

```text
C_k=G+S_k,          S_k in Sym_0.
```

They share the skew part `K_0=G-G^T`.  If `K_0` were nonzero and
`C_k=u_kv_k^T`, then

```text
col K_0=span{u_k,v_k}
```

for every `k`.  This traps all three independent left factors in one fixed
two-plane, a contradiction.  Hence `G` is symmetric.  Subtracting its
symmetric off-diagonal part changes only its representative modulo `Sym_0`
and yields

```text
B'=Sym_0 direct-sum K diag(d_0,d_1,d_2).
```

Each normalized `C_k` is now symmetric rank one with this common diagonal.
If one `d_i` vanished, the `i`th coordinate of all three left factors would
vanish, contradicting their independence.  Thus all `d_i` are nonzero.

## External and multiplicity locking

After the complement normalization, every matrix in `B'` is symmetric and
its standard diagonal lies on the full-support line `Kd`.  For an arbitrary
external vector with transformed factors `(a,b)`, pairing it with selected
triangle coordinate `e_i` gives

```text
N_i=a e_i^T+e_i b^T in B'.
```

Symmetry for all three `i` gives `a=b`; the standard diagonal of `N_i` is
`2a_i e_i`, which cannot lie on `Kd` unless it is zero.  Hence every external
vector is effectively zero.

For an extra vector inside triangle label `i`, only the two distinct-label
mates `j,k` are used.  Their symmetry equations give `a=b`; their two
diagonal gates give `a_j=a_k=0`.  Thus `(a,b)=c(e_i,e_i)`.  No same-label
self-pair is introduced.  Every surviving pair output consequently lies in
`Sym_0`, so the total image has dimension at most three, contradicting the
rank-four premise.

This handles arbitrary label-domain dimensions, different initially chosen
vectors at one triangle vertex, parallel outputs, external pure-excess
feeders, internal two-dimensional triangle edges, and all rank/support/divisor
fibres.

## Owning-interface application

`GLS43` and `GLS44` exclude rank-four `q!=0`.  On rank-four `q=0`, `GLS45`
leaves exactly the residual-free and sparse same-label cores.  `GLS46`
derives the complete-label hypotheses for both: in the sparse case the one
active residual label has maps `(a,tb)`, its cross maps are the exact
residual--port columns, its missing self-pair is never added, and `q=0`.
`GLS47` therefore exhausts the whole surviving rank-four full-swallow
boundary rather than only the residual-free subcase.

The conclusion is conditional on full swallow.  It does not prove that every
silent zero-anchor source point is fully swallowed.

## Independent computational audit

The SymPy primary replays the nonzero synchronized product, exact left--right
normalization, the `Sym_0` rank-one minors, the common-skew factorization, the
full-support diagonal gate, and the external/block linear systems.  It is an
identity replay; the written proof carries the arbitrary-dimensional theorem.

The no-import audit uses only custom `F_3` arithmetic and a different
representation.  Modulo `Sym_0`, a complement is encoded by its three
diagonal and three skew coordinates.  The audit exhausts all `364` projective
quotient classes and all `40` projective matrices in each four-space.  Only
one quotient class admits three rank-one points whose left and right factors
both span; it has zero skew and full diagonal support.  The maximum number of
rank-one points is four.

For all four full-support diagonal lines over `F_3`, the audit then exhausts
all `3^6` factor pairs.  Exactly the zero factor pair is compatible with all
three external tests, and the triangle-block-compatible pairs are exactly
the scalar coordinate pairs.  These finite computations are independent
corroboration, not the characteristic-zero proof.

## Required replay

```text
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_rank_four_silent_full_swallow_complete_pair_family_exclusion.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_rank_four_silent_full_swallow_complete_pair_family_exclusion.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_rank_four_complete_pair_family_structural_degree_cut_and_triangle_localization.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_rank_four_complete_pair_family_structural_degree_cut_and_triangle_localization.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_rank_four_silent_full_swallow_residual_shore_profile_reduction.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_rank_four_silent_full_swallow_residual_shore_profile_reduction.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_rank_four_full_swallow_nonzero_diagonal_root_deck_complete_exclusion.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_rank_four_full_swallow_nonzero_diagonal_root_deck_complete_exclusion.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_rank_four_full_swallow_off_diagonal_root_deck_complete_exclusion.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_rank_four_full_swallow_off_diagonal_root_deck_complete_exclusion.py
```

Focused checks, candidate-tree QA, exact-head hosted CI, safe merge, and fresh
postmerge verification remain publication gates until performed.

## Unresolved boundary

Rank four is closed only inside zero-anchor full swallow.  The smallest next
full-swallow rank is five, where the excess over `Delta` has dimension two
and the one-line complement locking used here no longer applies.  Silent
source-to-swallow coverage, ranks five through nine, raw escape, nonzero
anchor, all legal attachment gates, source coverage, strategic-node closure,
and global resolution remain open.
