# Hostile review: zero-anchor complete pairwise-diagonal rank bound and minimal raw-swallow exclusion

## Verdict

**ACCEPT after mathematical, type, independence, and scope audit.**  For whole
label-domain maps, distinct-label diagonal polarization has combined image
rank at most two in characteristic not two.  The auxiliary one-dimensional
residual labels exactly recover `q` and every component of the `GLS36`
incidence map.  Therefore a rank-three full-swallow point would make one
pairwise-diagonal family have image both `Delta` and rank at most two.

This proves that every zero-anchor full-swallow fibre has
`rank B_Q^anc>=4`, including conditional `q=0`, `p=0`, and diagonal-silent
points.  It does **not** force a silent `p=0` source point into full swallow,
exclude ranks four through nine, turn raw escape into an original target,
or supply any legal downstream attachment gate.  The maximum-root
supply-and-target-attachment node and the global Krenn--Gu conjecture remain
**UNRESOLVED**.

## Reviewed artifacts

- [`GLS39 theorem`](../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_COMPLETE_PAIRWISE_DIAGONAL_FAMILY_RANK_BOUND_AND_MINIMAL_RAW_SWALLOW_EXCLUSION_THEOREM.md)
- [`focused primary verifier`](../../claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_complete_pairwise_diagonal_family_rank_bound_and_minimal_raw_swallow_exclusion.py)
- [`independent no-import audit`](../../claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_complete_pairwise_diagonal_family_rank_bound_and_minimal_raw_swallow_exclusion.py)
- owning theorems `GLS8`, `GLS35`, and `GLS36`
- predecessor exclusions `GLS37` and `GLS38`
- the `GLS39` entries in [`current frontier`](../current-frontier.md), the
  [`supply/target node DAG`](../history/handoffs/MAXIMUM_ROOT_SURPLUS_TWO_SUPPLY_TARGET_NODE_DAG_2026-08-20.md),
  and the arbitrary-order claim README.

The theorem proof uses the label-support route.  The independent audit uses a
different two-block/bipartition/triangle derivation and representation.  Both
hostile reviews were read-only and separate from the theorem drafting.

## Owning-interface and quantifier audit

Fix one `GLS8`-eligible `(Q,A)` chart and one residual contraction in the
declared `GLS36` scope.  For a promoted port `u`, retain the whole linear maps

```text
X_u:V_u -> V_(a_0)^*,       Y_u:V_u -> V_(a_1)^*.
```

For each residual label `q_s`, use an auxiliary one-dimensional domain and

```text
X_(q_s)(1)=a_s,             Y_(q_s)(1)=b_s.
```

Polarization is required only between **distinct labels**, exactly as in the
owning grade-zero companion family.  No same-port or same-slice pair is added.
Direct substitution gives

```text
mu_(q_0,q_1)=q,
mu_(q_s,u)=sigma_(s,u),
mu_(u,v)=sigma_(u,v).
```

Consequently,

```text
sum_(s<t) im mu_(s,t)=im sigma_Q+Kq.                 (1)
```

At zero anchor, `GLS36` gives `B_Q^anc=im sigma_Q` pointwise on every
residual, shore, incidence, nuisance, and divisor fibre.  Rank-three full
swallow gives `B_Q^anc=Delta` and `q in B_Q^anc`; hence (1) equals `Delta`.
Every extended pair map lands in `Delta`, exactly matching the abstract
lemma's hypotheses.

No complete mixed/pure deck equation beyond the already declared
full-swallow premise is imported.  In particular, `p!=0 => q!=0` was already
covered by `GLS38`; `GLS39` newly removes conditional `q=0` full swallow, but
does not assert that the silent source branch is swallowed.

## Primary mathematical derivation

Write the coordinate functionals of each whole-domain map as `x_(t,i)` and
`y_(t,j)`.  For `i!=j`, diagonal polarization gives

```text
x_(s,i) tensor y_(t,j)+y_(s,j) tensor x_(t,i)=0.     (2)
```

If the supports `A_i={t:x_(t,i)!=0}` and
`B_j={t:y_(t,j)!=0}` are nonempty, (2) forces `A_i=B_j`: an element in one
set but not the other paired with any element of the other set would leave
one nonzero simple tensor equal to zero.  For distinct labels in the common
support, simple-tensor proportionality produces nonzero scalars with
`rho_s+rho_t=0`.  Three supported labels would give `2rho_s=0`, impossible
in characteristic not two.  Thus every nonempty off-diagonal support has at
most two labels.

If all three diagonal colours were active, all six coordinate supports would
be nonempty.  The off-diagonal support graph is connected, so they would be
one common set `S` of size at most two.  Labels outside `S` have both maps
zero.  If `S` has two labels, their single pair matrix is diagonal and is a
sum of two rank-one matrices.  Its determinant is zero.  The product of its
three diagonal bilinear forms is therefore zero in a polynomial domain, so
one form is identically zero.  Hence at most two colours are active and the
combined image has rank at most two.

## Genuinely independent derivation

The independent route begins with a two-block lemma.  Aggregate any two
disjoint groups of labels by direct sum.  Their cross-polarization matrix is
diagonal and a sum of two rank-one matrices, so it misses one fixed diagonal
coordinate by the same polynomial-domain determinant argument.

Suppose three pair-image vectors were independent and record their label
pairs as a three-edge multigraph.  If the underlying graph is bipartite, put
its two parts into the two aggregate blocks.  All three vectors then lie in
one cross image of rank at most two, a contradiction.  With at most three
edges, the only nonbipartite possibility is a triangle.

For a triangle, aggregate the two neighbors of each vertex.  The two-block
lemma places the two incident edge spaces in one coordinate plane.  Their
chosen vectors are independent, so that vertex plane is exactly their span.
If two vertex planes were equal, their three selected incident-edge vectors
would all lie in that common two-plane, contradicting the assumed
independence.  Thus the three vertex planes are pairwise distinct.  Each edge
space lies in both endpoint planes and hence in their intersection.  The
intersections of three distinct coordinate planes are the three distinct
pure coordinate lines, so the three edge spaces occupy different coordinate
lines.

Each edge is now a nonzero bilinear polynomial times its coordinate tensor.
Pass to the fraction field of the joint polynomial ring and evaluate at the
three generic label vectors.  Each nonzero edge polynomial is then a nonzero
field element simultaneously, so the next orientation argument applies over
this extension in every characteristic other than two.  This step does not
specialize a physical source point or divide by a physical coefficient.  A
nonzero rank-one sum

```text
x_s y_t^T+x_t y_s^T
```

has either dependent column factors or dependent row factors.  Indeed, if
both factor pairs were independent, contractions dual to the two column
factors would expose two independent row factors, giving tensor rank two.
This also covers zero factors.  Because the output is a nonzero multiple of
`e_c tensor e_c`, a dependent nonzero column span is exactly `K e_c`, or,
in the transposed orientation, the corresponding row span is `K e_c`.

Two of the three triangle edges have the same orientation.  They share a
vertex but have distinct colours.  In the column orientation, the shared
evaluated `X` vector lies in two distinct coordinate axes and is therefore
zero.  Each of the two edge tensors then reduces to one nonzero pure tensor,
and their shared evaluated `Y` vector would have to lie in those same two
distinct axes, hence also be zero, a contradiction.  The row orientation is
the transpose.  This proves the rank bound without the support-set argument.

## Exact computational audits

The primary uses SymPy to replay:

- connectivity of the six support nodes;
- the three-label sign determinant `-2`;
- the identically zero determinant of a two-label pair matrix;
- exact auxiliary residual-label typing; and
- a bounded `F_3` scalar falsification census with `364` projective families,
  `700` compatible pairs, and `9,343` cliques through six labels, whose
  maximum diagonal rank is two.

The no-import audit uses only the standard library and the independent route:

- `729` supporting two-block column-span coefficient matrices, together with
  exact formal determinant cancellation for the universal sum of two
  rank-one `3x3` matrices and an integral-domain leading-term check;
- all `680` three-edge multigraphs on six labels, of which the `20`
  nonbipartite cases are exactly triangles;
- all `531,441` four-vector states over `F_3`, including `2,448` nonzero
  coordinate rank-one outputs, to audit the orientation lemma and its zero
  factors;
- all `27` ordered coordinate-plane triples, including the `6` pairwise
  distinct triples and their three distinct coordinate-axis intersections;
  and
- all `48` distinct-colour triangle orientation cases, each with an adjacent
  same-orientation pair; the written argument supplies the ensuing
  shared-factor contradiction.

These finite systems are supporting proof-leaf audits.  The arbitrary-domain,
arbitrary-root theorem is the written proof, not a finite scalar census.

## Verification replay

The following pass on the candidate tree:

```text
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_complete_pairwise_diagonal_family_rank_bound_and_minimal_raw_swallow_exclusion.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_complete_pairwise_diagonal_family_rank_bound_and_minimal_raw_swallow_exclusion.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_nonzero_root_deck_minimal_raw_swallow_exclusion.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_nonzero_root_deck_minimal_raw_swallow_exclusion.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_minimal_raw_swallow_incidence_classification_and_mixed_only_faithfulness_nogo.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_minimal_raw_swallow_incidence_classification_and_mixed_only_faithfulness_nogo.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_incidence_image_common_row_silence_and_labelwise_lift_sharpness.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_incidence_image_common_row_silence_and_labelwise_lift_sharpness.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_promoted_two_probe_one_target_attachment_and_pointwise_failure_reduction.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_promoted_two_probe_one_target_attachment_and_pointwise_failure_reduction.py
```

The focused GLS39 scripts, their Ruff checks, and every displayed dependency
replay pass.  On the index-complete candidate tree, repository hygiene passes,
the migration suite passes all `191` tests, the cycle-cover lattice suite
passes all `14` tests, and link rewriting is idempotent with zero files
touched.  Exact-head hosted CI and merged-main replay remain publication gates
to be recorded before and after merge.

## Unresolved boundary

The zero-anchor **full-swallow** remainder now starts at nuisance rank four.
The complete labelwise physical deck equations, not another rank/common-row
criterion, must either contradict ranks four through nine or produce an
alternative legal same-graph attachment with every response, activity,
synchronization, nuisance-survival, anchor, and source gate.  Silent `p=0`
source coverage, raw escape, and nonzero-anchor branches remain separate.

The theorem neither starts permanent restriction/extraction/gluing nor
changes the global status.
