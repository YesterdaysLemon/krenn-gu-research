# Future-instance handoff: symbolic `P_4/P_5` frontier

## Read this first

The Krenn--Gu prize conjecture is **UNRESOLVED globally**.  Nothing in this
repository is a proof or disproof for every even `n>=6` and `d>=3`.

This checkpoint closes a coherent local chapter.  It uses exact symbolic
algebra, projective geometry, Frobenius duality, and a small graph-theoretic
reduction.  Finite-field programs are independent audits, never substitutes
for the characteristic-zero arguments.

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

Three statements organize the current frontier.

1. **The lower-pair locus is exhausted.**  If a nonzero pure `P_4`
   compression has `min r_ij<=2`, it lies in one of four known component
   closures.  See
   [`P4_LOWER_PAIR_RANK_COMPONENT_EXHAUSTION.md`](P4_LOWER_PAIR_RANK_COMPONENT_EXHAUSTION.md).
2. **Every known component is generically closed at `P_5`.**  The marked
   `H31` and weighted `H22` fibres are empty over the generic point of all
   seventeen currently known pure-`P_4` components.  Component fifteen is
   the last completed case:
   [`P5_H31_DISJOINT_SECANT_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H31_DISJOINT_SECANT_COMPONENT_GENERIC_OBSTRUCTION.md)
   and
   [`P5_H22_DISJOINT_SECANT_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H22_DISJOINT_SECANT_COMPONENT_GENERIC_OBSTRUCTION.md).
3. **The remaining component question is an eight-cell `K_4` problem.**
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
| triangle | `(1,1,1)` | close kernel--kernel and doubly oriented degeneracies |

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
seventeen-component list is exhaustive would not automatically settle the
special fibres or the final local-to-global step.

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

## Unverified lead: the common-singleton `K_4` family

**Everything in this section is a scratch lead, not a theorem and not yet a
replayable repository result.**  It may describe a new five-dimensional
component, or merely a boundary of a known component.

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
v3=(B*v1) cross (B*v2).
```

At `(L,M,a,b,c)=(2,3,2,4,1)`, scratch exact arithmetic gives

```text
d=-21/4,       v3=(30,-72,21) ~ (10,-24,7),
P3(v1,v2,v3)=-42,
(r01,r02,r03,r12,r13,r23)=(3,3,3,3,3,3).
```

In the `pivot01` Grassmann chart the corresponding sixteen coordinates were

```text
(0,0,2,3, 0,0,2,4, 0,0,1,-21/4, 0,0,-12/5,7/10).
```

The family map had tangent rank five at the sample (one selected `5 x 5`
minor was `1`).  A universal `pivot01`, anchor-`(0,1,1,1)` incidence
Jacobian had rank ten at the same point; one selected `10 x 10` minor was
`-6176008608/15625`.  That rank is **not** a dimension certificate because
the displayed incidence equations may be nonreduced.

The best next symbolic test is local, not enumerative:

1. compute a local standard basis or local Krull dimension at the rational
   sample in the universal incidence;
2. if the local dimension is five, prove irreducibility of the chart and
   certify that it is an actual component;
3. if the local dimension is at least six, construct an explicit deformation
   or arc into a known component (component eleven is the first candidate);
4. only if a new component is certified, derive its generic `H31/H22` marked
   fibre obstruction.

A simple toric degeneration attempted from component eleven forced one
limiting line to have support at most two and did not cover generic
full-support `ell`.  This null result is weak evidence only.

## Focused replay

From the repository root:

```text
uv run --with sympy python verify_p5_h31_disjoint_secant_component_generic_obstruction.py
python audit_p5_h31_disjoint_secant_component_generic_obstruction.py

uv run --with sympy python verify_p5_h22_disjoint_secant_component_generic_obstruction.py
python audit_p5_h22_disjoint_secant_component_generic_obstruction.py

uv run --with sympy python verify_p4_all_pair_rank_exceptional_graph_reduction.py
python audit_p4_all_pair_rank_exceptional_graph_reduction.py
```

If plain `python` lacks a dependency, use the repository's isolated verifier
environment documented by the earlier checkpoint; do not silently change
the algebra system or claim a replay that did not finish.

## Claim and stopping rules

- Keep `UNRESOLVED globally` at the top of the README until the full chain is
  actually proved.
- Label a finite-field census as an audit, not a characteristic-zero proof.
- Label a timeout or failed elimination as unresolved, not empty.
- Do not call the common-singleton family a component without a local
  dimension/height certificate and a containment analysis.
- Prefer exact identities, normal forms, projective covers, and local algebra
  to broad search.
- After a meaningful theorem, update this handoff or replace it with a dated
  successor and leave the worktree clean.
