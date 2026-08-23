# Hostile review: zero-anchor rank-four complete-pair structural-degree, cut, and triangle localization

## Verdict

**ACCEPT after exact repair.**  The first hostile pass rejected the draft
because its reducible determinant-cubic proof invoked nonzero factorization
without first separating `L=0`.  The accepted theorem now handles that fibre
directly, states characteristic zero in the formal setup, derives the sparse
`GLS45` auxiliary-label bridge explicitly, and narrows the verifier wording
to the identities actually replayed.

The resulting `GLS46` conclusions are exact:

```text
complete pair image B=Delta direct-sum Kf
  => each global coordinate family uses <=2 labels
  => total effective domain dimension <=12;

every label cut has diagonal rank <=2
  => three diagonal directions lie on one triangle
  => every nontriangle edge is diagonal-silent
  => the fourth direction is a two-dimensional triangle edge
     or an external pure-f feeder.
```

This is a uniform characteristic-zero arbitrary-root structural reduction,
not an exclusion and not a finite atlas.  Both fourth-direction forks remain
open in `GLS46`.  Ranks five through nine, raw escape, nonzero anchor, every
response/attachment/source gate, the strategic node, and the global
Krenn--Gu conjecture remain **UNRESOLVED**.

## Reviewed artifacts

- [`GLS46 theorem`](../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_RANK_FOUR_COMPLETE_PAIR_FAMILY_STRUCTURAL_DEGREE_CUT_AND_TRIANGLE_LOCALIZATION_THEOREM.md)
- [`focused exact primary verifier`](../../claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_rank_four_complete_pair_family_structural_degree_cut_and_triangle_localization.py)
- [`independent no-import audit`](../../claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_rank_four_complete_pair_family_structural_degree_cut_and_triangle_localization.py)
- owning interfaces `GLS8`, `GLS36`, `GLS39`, and `GLS45`
- boundary interfaces `GLS40` and `GLS41`
- the current frontier, supply/target DAG, and arbitrary-order README updates.

Four bounded attacks were kept separate.  One derived the coordinate
annihilator and effective-dimension theorem.  One derived the two-block
determinant cubic and all-cut consequence.  One searched exact finite fields
and found no rank-four family, but correctly retained those results only as
finite falsification evidence.  A final hostile pass checked the integrated
claim and required the repairs above.  A separate successor attack produced
a candidate complete triangle-lock exclusion; it is not imported into
`GLS46` and requires its own theorem, verifier, audit, and publication gate.

## Owning-interface and sparse-label audit

At one fixed arbitrary residual contraction, `GLS36` gives

```text
B=B_Q^anc=im sigma_Q.
```

`GLS45` leaves two rank-four profiles on `q=p=0`.  In the residual-free
profile, the complete family consists only of the promoted labels and their
distinct-label pair maps.  In the sparse profile, adjoin one one-dimensional
label with

```text
X_(q_0)(1)=a,              Y_(q_0)(1)=t b.
```

Its pair with port `u` is exactly

```text
a tensor Y_u+t X_u tensor b,
```

the residual--port column in `GLS45`.  The other residual label is zero,
and the residual pair is `q=0`.  No self-pair is introduced.  Therefore the
sum of distinct-label pair images is exactly `im sigma_Q=B` in both
survivors.  The abstract hypothesis is neither broader nor narrower than the
owning rank-four incidence obligation.

## Coordinate structural-degree proof

Full generation of `Delta` makes each of the three global left coordinate
families independent, and likewise on the right.  For a fixed row `i`, choose
a nonzero vector in the coordinate complement of `e_i` that kills row `i` of
`f`.  The resulting rank-one functional kills both `Delta` and `f`, so it
turns the complete pair containment into a labelled zero-product identity.

The zero-product lemma is pointwise and support-free.  Two nonzero labelled
families satisfying all distinct-label polarizations have identical support
of size at most two in characteristic different from two.  It follows that
each global coordinate family uses at most two labels.  There are six
coordinate families, so at most twelve labels are active.  On each label,
the quotient by `ker X_t intersect ker Y_t` has dimension equal to the span
rank of its six local coordinate forms.  Summing those ranks is bounded by
the twelve nonzero coordinate slots.  No finite support enumeration or
selected port value appears.

The hostile review checked the singleton and two-label edge cases.  The bound
does not say every active label is one-dimensional; only the summed effective
dimension is bounded.  Characteristic two is excluded explicitly and has a
three-label sharpness failure.

## Two-block determinant-cubic proof

For any label cut, aggregate the maps on its two sides.  Every cross output
has one common off-diagonal coefficient `L` against `f`, while the three
diagonal entries are bilinear forms `D_0,D_1,D_2`.  Rank at most two of the
physical matrix gives

```text
P_f(D_0,D_1,D_2,L)=0,

P_f(x,y,z,l)
 =xyz-l^2(alpha x+beta y+gamma z)+tau l^3.
```

The proof divides only by one fixed nonzero entry of `f`.  It never divides
by `L`, a response, a rank minor, or a divisor parameter.

If `P_f` is reducible, a linear-factor substitution gives, up to colour,

```text
P_f=x(yz-alpha l^2).
```

The repaired proof first separates `L=0`, where `D_1D_2=0`.  In the remaining
nonzero case, unique factorization and bidegree `(1,1)` force
`D_1,D_2,L` proportional.  Thus the diagonal span is at most two.

If `P_f` is irreducible, a direct line parameterization proves that its cubic
surface contains finitely many projective lines.  The projective closure of a
bilinear pure image spanning at least three dimensions has dimension at least
two; the only alternative would be a rank-one matrix space with a common
factor.  A three-dimensional total span would put a plane in the irreducible
cubic.  A four-dimensional span would produce a dense family of lines, but
the finite closed union of the corresponding contraction loci covers the
dense rank-two locus and hence all projective `U`; irreducibility forces one
fixed line, contradicting four-dimensional span.  This proves the all-cut
diagonal-rank-two theorem for arbitrary block dimensions.

## Triangle and external-silence audit

Choose three actual pair outputs with independent diagonal projections.  If
their support graph were bipartite, one cut would contain all three and
contradict the cut theorem.  A loopless three-edge nonbipartite graph is one
triangle.  Intersecting the two incident cut planes makes each triangle edge
image one-dimensional.

For an edge from a triangle vertex to an outside label, three cuts place its
diagonal image in the three pairwise spans of the independent triangle lines;
their intersection is zero.  The same three-cut argument handles an edge
between two outside labels.  Therefore every nontriangle edge is exactly
diagonal-silent, not merely unsupported by the chosen basis.

If every triangle full image were one-dimensional and every nontriangle
image zero, the total image would have rank three.  Hence a rank-four family
must have either a two-dimensional triangle edge or a nonzero external image
inside `Kf`.  The fork is exhaustive, but neither side is excluded by
`GLS46`.

## Exact sharpness and rejected stronger route

Over `Q`, let

```text
p_0=(0,1,1),       p_1=(1,0,1),       p_2=(1,1,0),
```

take `X_i=Y_i=p_i`, and let `f` have all six off-diagonal entries one.  Then

```text
mu_(0,1)=f+2r_2,
mu_(0,2)=f+2r_1,
mu_(1,2)=f+2r_0.
```

The diagonal image is all of `Delta`, refuting the proposed global
diagonal-rank-two theorem.  The three matrices span only a three-space, so
this is not a full-swallow point or witness.  Exact tangent systems have
rank seven on eight variables for compatibility with two mates and rank nine
on nine variables for compatibility with all three.  This displayed normal
form is locked, but `GLS46` does not extrapolate that computation to every
triangle.

## Independent computational audit

The SymPy primary replays the determinant expansion, reducibility
substitution, bidegree constraint, line-parameter coefficients, rank-one
annihilator identity, all `680` three-edge support multigraphs, and the exact
rational locked triangle.  It is a focused identity replay; the written
proof carries the arbitrary-dimensional theorem.

The no-import audit uses only the Python standard library and a distinct
representation.  It:

- solves for every linear factor of the determinant cubic for all `364`
  projective off-diagonal lines over `F_3`, finding `156` reducible cases and
  exact agreement with the symbolic classification;
- exhausts the three-label scalar zero-product shadow over `F_3`;
- backtracks all `109,159` cut-admissible edge-subspace assignments on `K_4`
  over `F_2`, including `672` rank-three assignments, and checks the exact
  triangle/external-zero conclusion; and
- rebuilds the rational tangent ranks using custom `Fraction` elimination.

These finite calculations are independent falsification and identity audits,
not a characteristic-zero proof or a finite source cover.

## Required replay

```text
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_rank_four_complete_pair_family_structural_degree_cut_and_triangle_localization.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_rank_four_complete_pair_family_structural_degree_cut_and_triangle_localization.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_incidence_image_common_row_silence_and_labelwise_lift_sharpness.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_incidence_image_common_row_silence_and_labelwise_lift_sharpness.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_complete_pairwise_diagonal_family_rank_bound_and_minimal_raw_swallow_exclusion.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_complete_pairwise_diagonal_family_rank_bound_and_minimal_raw_swallow_exclusion.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_rank_four_silent_full_swallow_residual_shore_profile_reduction.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_rank_four_silent_full_swallow_residual_shore_profile_reduction.py
```

Focused checks, candidate-tree QA, exact-head hosted CI, safe merge, and fresh
postmerge verification remain publication gates until performed.

## Unresolved boundary

`GLS46` reduces the arbitrary-root rank-four silent family to a uniform
twelve-dimensional triangle-plus-feeder problem.  It does not exclude the
family.  The separately audited triangle-lock argument is a candidate
successor until it has its own complete artifacts and publication gate.
Regardless of that successor, ranks five through nine, raw escape, nonzero
anchor, response/activity/synchronization, nuisance survival, anchors, a
named receiver, arbitrary-root source coverage, strategic-node closure, and
global resolution remain open.
