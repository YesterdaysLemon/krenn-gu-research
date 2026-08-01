# Future-instance handoff: symbolic `P_4/P_5` frontier

## Read this first

The Krenn--Gu prize conjecture is **UNRESOLVED globally**.  Nothing in this
repository is a proof or disproof for every even `n>=6` and `d>=3`.

This checkpoint closes a coherent local chapter.  It uses exact symbolic
algebra, projective geometry, Frobenius duality, and a small graph-theoretic
reduction.  Finite-field censuses remain audits and are never substitutes for
characteristic-zero arguments.  The new common-singleton theorem does use an
exact modular local standard basis, but only as a height certificate in an
integral local model; an explicit Krull-height argument supplies the
characteristic-zero conclusion.

The active branch at wind-down is `codex/h22-disjoint-mixed-star`.  The most
recent mathematical commits before this documentation pass are:

```text
96a6c92  Refresh lower-pair fibre status
ae70348  Reduce P4 exhaustion to eight graph cells
431a517  Exclude H22 lifts on disjoint-secant component
819558d  Exclude H31 lifts on disjoint-secant component
```

Recheck the branch and worktree before relying on those identifiers.

## Verified checkpoint

Four statements organize the current frontier.

1. **The lower-pair locus is exhausted.**  If a nonzero pure `P_4`
   compression has `min r_ij<=2`, it lies in one of four known component
   closures.  See
   [`P4_LOWER_PAIR_RANK_COMPONENT_EXHAUSTION.md`](P4_LOWER_PAIR_RANK_COMPONENT_EXHAUSTION.md).
2. **All eighteen certified components are generically closed at `P_5`.**
   Their marked `H31` and weighted `H22` fibres are empty over the generic
   point.  For the first seventeen, component fifteen was the last completed
   case:
   [`P5_H31_DISJOINT_SECANT_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H31_DISJOINT_SECANT_COMPONENT_GENERIC_OBSTRUCTION.md)
   and
   [`P5_H22_DISJOINT_SECANT_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H22_DISJOINT_SECANT_COMPONENT_GENERIC_OBSTRUCTION.md).
   Component eighteen is closed by the common-singleton Hall deficiency:
   [`P5_H31_COMMON_SINGLETON_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H31_COMMON_SINGLETON_COMPONENT_GENERIC_OBSTRUCTION.md)
   and
   [`P5_H22_COMMON_SINGLETON_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H22_COMMON_SINGLETON_COMPONENT_GENERIC_OBSTRUCTION.md).
3. **The common-singleton family is component orbit eighteen.**  An exact
   integral graph slice has local dimension zero modulo `32003`; Krull height
   lifts this to a five-dimensional characteristic-zero incidence germ.  The
   family is irreducible of dimension five, and the closed condition that all
   six pair ranks are at most three separates it from the previous seventeen
   orbits.  See
   [`P4_COMMON_SINGLETON_COMPONENT.md`](P4_COMMON_SINGLETON_COMPONENT.md).
   Its generic `H31/H22` fibres are the two cases just cited.
4. **The remaining component question is an eight-cell `K_4` problem.**
   Perfect pairing forces the rank-three edges to contain a star or triangle;
   the three selected relations have matrix ranks one or two.  Four of the
   eight coarse cells are resolved and four remain.  See
   [`P4_ALL_PAIR_RANK_EXCEPTIONAL_GRAPH_REDUCTION.md`](P4_ALL_PAIR_RANK_EXCEPTIONAL_GRAPH_REDUCTION.md).

The unresolved cells are:

| blocker | relation ranks | missing theorem |
|---|---:|---|
| star | `(2,1,1)` | global orientation/support closure |
| star | `(1,1,1)` | global orientation/support closure |
| triangle | `(2,1,1)` | exhaust the union of known charts |
| triangle | `(1,1,1)` | exhaust the residual strata around component eighteen |

## What a global proof would still need

The dependency chain is strict:

```text
classify the four open all-pair P4 cells
                 |
                 v
prove all special/boundary P5 fibres empty
                 |
                 v
justify the local P5 reduction and gluing at arbitrary graph order
                 |
                 v
global Krenn--Gu nonexistence theorem
```

The present work is closest to the first box.  Even a proof that the
eighteen-component list is exhaustive would not automatically close special
fibres or the final local-to-global step.

There is now a second, genuinely arbitrary-order route into the same `P_5`
bottleneck:

```text
five fully supported pairwise-zero roots
  + total blocker union exactly five
                 |
                 v
             P_5 -> Delta_3
```

At order ten, four fully supported roots and a five-vertex blocker union also
extract `P_5 -> Delta_3`; six blockers are the exact surplus alternative.
For a transverse five-root intersection point, zero coordinates are exactly
internal blocker flags.  None of these statements yet proves that the
degree-24 five-root intersection meets the coordinate torus, excludes a
nonreduced intersection, rules out blocker surplus at least six, or excludes
`P_5 -> Delta_3`.  See
[`FIVE_ROOT_TIGHT_BLOCKER_P5_EXTRACTION.md`](FIVE_ROOT_TIGHT_BLOCKER_P5_EXTRACTION.md),
[`ONE_NONBLOCKER_SURPLUS_PERMANENT_EXTRACTION.md`](ONE_NONBLOCKER_SURPLUS_PERMANENT_EXTRACTION.md),
and
[`FIVE_ROOT_BOUNDARY_TRANSVERSAL_BLOCKER_CLASSIFICATION.md`](FIVE_ROOT_BOUNDARY_TRANSVERSAL_BLOCKER_CLASSIFICATION.md).

The coordinate-boundary exception is now contained in a finite union of
explicit algebraic hypersurfaces.
For every vertex/colour boundary, an irreducible multihomogeneous resultant
has incident-edge degree `12`, nonincident-edge degree `10`, and total degree
`108`.  Avoiding all fifteen resultants forces a fully supported five-root
zero.  This is a genericity criterion, not a proof that witness blocks avoid
the exceptional hypersurfaces:
[`FIVE_ROOT_TORUS_RESULTANT_DICHOTOMY.md`](FIVE_ROOT_TORUS_RESULTANT_DICHOTOMY.md).

## Why these translations were useful

This is a research decision record, not a transcript of private reasoning.

- Replace permanent restrictions by the squarefree Frobenius algebra
  `R=C[X0,X1,X2,X3]/(Xi^2)`.  Multiplication and annihilators expose geometry
  that is almost invisible in raw graph coordinates.
- Treat a rank-two pair image as a projective line in the ambient Segre
  quadric.  Secant and tangent lines lead to finite geometric normal forms.
- Regard the six pair ranks as labels on `E(K_4)`.  Perfect pairing turns
  their exceptional set into a blocker of the three perfect matchings;
  minimal blockers are exactly stars and triangles.
- Read rank-one relations as directed zero-product or gain-graph data and
  rank-two relations as synchronizer edges.  The remaining continuous
  problem is a small quiver-stratum classification, not a graph census.
- For `P_5`, project the extension incidence to the base with Fitting ideals,
  then cover the projective extension line by explicit marked minors.  This
  is the source of the generic `H31/H22` obstructions.

These moves reduced large polynomial systems to symbolic identities with
small independent audits.  Broad support enumeration and disk-heavy brute
force are not the recommended continuation.

## Certified component eighteen: the common-singleton `K_4` family

Let `e=X0`.  In `V=span(X1,X2,X3)`, choose `ell` and three lines
`v1,v2,v3` that are pairwise orthogonal for the ternary polar form

```text
B_ell(u,v)=P3(ell,u,v).
```

Set

```text
U0=<ell,e>,                 alpha0=ell, beta0=e,
Ui=<e,vi>  (i=1,2,3),       alphai=e,  betai=vi.
```

All mixed `P_4` coefficients then vanish and the only possible pure
coefficient is `P3(v1,v2,v3)`.  Every pair can have image rank three, while
all six unique relations can have matrix rank one because every plane shares
the singleton zero product `e^2=0`.  This lands directly in the unresolved
`triangle-(1,1,1)` degeneracy rather than either tournament normal form.

A rational five-parameter chart is obtained from

```text
ell=(1,L,M),       v1=(1,a,b),       v2=(1,c,d),

B=[[0,M,L],[M,0,1],[L,1,0]],

d=-(L*b+M*a+M*c+b*c)/(L+a),
v3=((B*v1) cross (B*v2))/(((B*v1) cross (B*v2))_0).
```

At `(L,M,a,b,c)=(-3,-2,-1,-1,-1)`, exact arithmetic gives

```text
d=2,       v3=(1,3,-1),       P3(v1,v2,v3)=4,
(r01,r02,r03,r12,r13,r23)=(3,3,3,3,3,3).
```

In the `pivot01` Grassmann chart the corresponding sixteen coordinates were

```text
(0,0,-3,-2, 0,0,-1,-1, 0,0,-1,2, 0,0,3,-1).
```

The family tangent rank is five, with a selected minor `1`.  The universal
twenty-variable incidence has fifteen equations and tangent rank ten at the
sample, but the proof does not infer dimension from that tangent space.  It
preconditions the local ideal, imposes five explicit graph hyperplanes, and
clears only `32003`-unit denominators.  Exact Singular local algebra over
`F_32003` returns standard-basis size `36`, vector-space dimension `56`, and
local dimension zero.  A mixed-characteristic height argument then proves
that the characteristic-zero graph slice is locally zero-dimensional, so the
unsliced incidence germ has dimension exactly five.

Every pair product in this family lies in
`span(e*vi,e*vj,vi*vj)`, so all six ranks are at most three on its closure.
Every one of the seventeen older components has a certified point with a
rank-four pair.  The new component is therefore genuinely orbit eighteen.

Its generic marked fibres are now closed by the shared singleton itself.  In
the intrinsic pure basis the kernel rows are `(ell,e,e,e)`.  After every
`H31` deletion and both weighted `H22` merge directions, the final three
extended rows use at most two columns.  Their all-kernel permanent is
identically zero by Hall deficiency, simultaneously in all affine markings,
extension entries, source scalings, and homogeneous weights.  The remaining
work is the rest of the `triangle-(1,1,1)` cell, projective/special component
boundaries, and special universal `P_5` fibres.

## Focused replay

From the repository root:

```text
uv run --with sympy python verify_p5_h31_disjoint_secant_component_generic_obstruction.py
python audit_p5_h31_disjoint_secant_component_generic_obstruction.py

uv run --with sympy python verify_p5_h22_disjoint_secant_component_generic_obstruction.py
python audit_p5_h22_disjoint_secant_component_generic_obstruction.py

uv run --with sympy python verify_p4_all_pair_rank_exceptional_graph_reduction.py
python audit_p4_all_pair_rank_exceptional_graph_reduction.py

uv run --with sympy python verify_p4_common_singleton_component.py
python audit_p4_common_singleton_component.py

uv run --with sympy python verify_p5_h31_common_singleton_component_generic_obstruction.py
python audit_p5_h31_common_singleton_component_generic_obstruction.py

uv run --with sympy python verify_p5_h22_common_singleton_component_generic_obstruction.py
python audit_p5_h22_common_singleton_component_generic_obstruction.py

uv run --with sympy python verify_five_root_boundary_transversal_blocker_classification.py
python audit_five_root_boundary_transversal_blocker_classification.py

python verify_five_root_torus_resultant_dichotomy.py
python audit_five_root_torus_resultant_dichotomy.py

python verify_one_nonblocker_surplus_permanent_extraction.py
python audit_one_nonblocker_surplus_permanent_extraction.py

uv run --with sympy python verify_five_root_tight_blocker_p5_extraction.py
python audit_five_root_tight_blocker_p5_extraction.py
```

If plain `python` lacks a dependency, use the repository's isolated verifier
environment documented by the earlier checkpoint; do not silently change
the algebra system or claim a replay that did not finish.

## Claim and stopping rules

- Keep `UNRESOLVED globally` at the top of the README until the full chain is
  actually proved.
- Label a finite-field census as an audit.  A modular standard basis may be
  used in a characteristic-zero proof only with a written integral
  height/flatness argument and pinned source metadata.
- Label a timeout or failed elimination as unresolved, not empty.
- Do not call the eighteen-component list exhaustive or promote generic fibre
  obstructions to special/projective fibres without the missing
  classifications.
- Prefer exact identities, normal forms, projective covers, and local algebra
  to broad search.
- After a meaningful theorem, update this handoff or replace it with a dated
  successor and leave the worktree clean.
