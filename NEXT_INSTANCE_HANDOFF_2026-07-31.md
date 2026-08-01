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

This continuation starts on `codex/component20-special-h31` from the reviewed
component-twenty generic checkpoint:

```text
0dba8b6  Close component 20 generic H31 fibre
```

Recheck the branch and worktree before relying on those identifiers.

## Verified checkpoint

Six statements organize the current frontier.

1. **The lower-pair locus is exhausted.**  If a nonzero pure `P_4`
   compression has `min r_ij<=2`, it lies in one of four known component
   closures.  See
   [`P4_LOWER_PAIR_RANK_COMPONENT_EXHAUSTION.md`](P4_LOWER_PAIR_RANK_COMPONENT_EXHAUSTION.md).
2. **The first eighteen components are generically closed at `P_5`; components
   nineteen through twenty-one are closed for generic `H31`.**  The first eighteen
   have empty marked `H31` and weighted `H22` fibres over the generic point.
   For the first seventeen, component fifteen was the last completed case:
   [`P5_H31_DISJOINT_SECANT_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H31_DISJOINT_SECANT_COMPONENT_GENERIC_OBSTRUCTION.md)
   and
   [`P5_H22_DISJOINT_SECANT_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H22_DISJOINT_SECANT_COMPONENT_GENERIC_OBSTRUCTION.md).
   Component eighteen is closed by the common-singleton Hall deficiency:
   [`P5_H31_COMMON_SINGLETON_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H31_COMMON_SINGLETON_COMPONENT_GENERIC_OBSTRUCTION.md)
   and
   [`P5_H22_COMMON_SINGLETON_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H22_COMMON_SINGLETON_COMPONENT_GENERIC_OBSTRUCTION.md).
   Component nineteen is closed by exact open-incidence projection and
   two-minor covers, including the marking-line intersection:
   [`P5_H31_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H31_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION.md).
   Component twenty is closed by exact open-incidence projection to four
   marking points and one uniform minor/transverse certificate:
   [`P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION.md).
   Its nine principal affine special divisors are also closed over their
   generic points by exact projection and uniform marked-minor certificates:
   [`P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT_SPECIAL_DIVISOR_OBSTRUCTION.md`](P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT_SPECIAL_DIVISOR_OBSTRUCTION.md).
   Component twenty-one's exact all-marking row-module certificate closes its
   generic `H31` fibre only:
   [`P5_H31_COINCIDENT_SUPPORT_RANK_ONE_STAR_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H31_COINCIDENT_SUPPORT_RANK_ONE_STAR_COMPONENT_GENERIC_OBSTRUCTION.md).
3. **The common-singleton family is component orbit eighteen.**  An exact
   integral graph slice has local dimension zero modulo `32003`; Krull height
   lifts this to a five-dimensional characteristic-zero incidence germ.  The
   family is irreducible of dimension five, and the closed condition that all
   six pair ranks are at most three separates it from the previous seventeen
   orbits.  See
   [`P4_COMMON_SINGLETON_COMPONENT.md`](P4_COMMON_SINGLETON_COMPONENT.md).
   Its generic `H31/H22` fibres are the two cases just cited.
4. **The full `triangle-(1,1,1)` cell is now closed.**  The final
   exactly-one-kernel stratum splits among old component boundaries and three
   new orbits.  The common-kernel vertical branch is component nineteen; the
   common-active binary branch is component twenty, with its singleton sheet
   as a boundary; and the mixed-chain vertical branch lies on the new
   coincident-support rank-one star sixfold, component twenty-one.  See
   [`P4_ONE_KERNEL_RANK_ONE_TRIANGLE_NORMAL_FORM_REDUCTION.md`](P4_ONE_KERNEL_RANK_ONE_TRIANGLE_NORMAL_FORM_REDUCTION.md),
   [`P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md`](P4_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT.md),
   [`P4_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT.md`](P4_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT.md), and
   [`P4_COINCIDENT_SUPPORT_RANK_ONE_STAR_COMPONENT.md`](P4_COINCIDENT_SUPPORT_RANK_ONE_STAR_COMPONENT.md).
5. **The remaining component question is a three-cell `K_4` problem.**
   Perfect pairing forces the rank-three edges to contain a star or triangle;
   the three selected relations have matrix ranks one or two.  Five of the
   eight coarse cells are resolved and three remain.  See
   [`P4_ALL_PAIR_RANK_EXCEPTIONAL_GRAPH_REDUCTION.md`](P4_ALL_PAIR_RANK_EXCEPTIONAL_GRAPH_REDUCTION.md).
6. **All gate-cover branches are impossible for the displayed rank-five
   `P_6` model.**  The unique four-gate branch forces alternating coordinate
   planes and then violates a remaining minor.  Each of the other 52 gate
   spans contains an invertible pairing, which cannot vanish between two
   three-planes in a five-space.  This closes the displayed model, not all
   possible `dim K=5` configurations.  See
   [`P6_COMMON_PORT_111_UNIQUE_FOUR_GATE_OBSTRUCTION.md`](P6_COMMON_PORT_111_UNIQUE_FOUR_GATE_OBSTRUCTION.md)
   and
   [`P6_COMMON_PORT_111_ALL_GATE_COVERS_OBSTRUCTION.md`](P6_COMMON_PORT_111_ALL_GATE_COVERS_OBSTRUCTION.md).

The unresolved cells are:

| blocker | relation ranks | missing theorem |
|---|---:|---|
| star | `(2,1,1)` | global orientation/support closure |
| star | `(1,1,1)` | global orientation/support closure |
| triangle | `(2,1,1)` | exhaust the union of known charts |

The removed fourth row, `triangle-(1,1,1)`, is completely resolved:
tournament orientations were already classified; the common-singleton family
is component eighteen; the fully kernel--kernel stratum lies in components
sixteen or eighteen; the exactly-two-kernel stratum lies in component eleven;
and all eight residual exactly-one-kernel entries now have exact component
placements.  Components nineteen through twenty-one now have exact generic
`H31` exclusions.  Component twenty also has exact divisor-generic exclusions
on nine principal affine special loci.  Their intersections, the remaining
normalization/projective/source-torus boundaries, and weighted `H22` on all
three components remain open.

For component nineteen, exact characteristic-zero projection reduces
deletions 0 and 1 to the unit ideal and deletions 2 and 3 to

```text
<h3, (q-phi)h0+1, h1*h2>.
```

The resulting four rational marking lines and both shared endpoints are now
closed by exact two-minor and pure-transverse certificates.

For component twenty, exact characteristic-zero projection over `C(p,q)`
leaves the four isolated markings

```text
d=1: (h1,h2)=(1-q,0), (0,-q),
d=2: (h1,h2)=(-p-1,0), (0,-p),
```

with `h0=h3=0`, while deletions zero and three give the unit ideal.  On all
four points the selected mode-three `0147` minor divided by the genuine
binary diagonal is `4pq(p+q)(p-q+1)`, and the deleted pure transverse entry
is `+pq` or `-pq`.

The follow-on exact projection proves that deletion-three binary-neighbour
incidence is supported precisely on `q=p+2`, `q=p`, `2pq-p+q=0`, `p=0,-1`,
and `q=0,1`.  Deletions one and two also acquire marking axes at `q=1/2` and
`p=-1/2`.  Exact characteristic-zero minor/transverse certificates close the
generic marked `H31` fibre on all nine divisors.  This does not close their
base intersections or the remaining normalization/projective/source-torus
boundaries.

## What a global proof would still need

The dependency chain is strict:

```text
classify the three open all-pair P4 cells
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

The present work is closest to the first box.  Even a proof that the current
twenty-one-component list is exhaustive would not automatically close generic
or special fibres on components nineteen through twenty-one, or the final
local-to-global step.

There is now a second, genuinely arbitrary-order route into the same `P_5`
bottleneck:

```text
five fully supported pairwise-zero roots
  + total blocker union exactly five
                 |
                 v
             P_5 -> Delta_3
```

The first-surplus extraction is now arbitrary-order too.  For `r` fully
supported roots, total blocker union `r+1` leaves an arbitrary positive odd
residual set; its matching contribution is one linear port row, giving
`P_(r+1) -> Delta_3`.  Thus four roots and five blockers give `P_5`, while
five roots and six blockers give the genuinely separate problem
`P_6 -> Delta_3`.  See
[`FIVE_ROOT_TIGHT_BLOCKER_P5_EXTRACTION.md`](FIVE_ROOT_TIGHT_BLOCKER_P5_EXTRACTION.md),
[`ODD_RESIDUAL_PORT_PERMANENT_EXTRACTION.md`](ODD_RESIDUAL_PORT_PERMANENT_EXTRACTION.md),
and
[`FIVE_ROOT_BOUNDARY_TRANSVERSAL_BLOCKER_CLASSIFICATION.md`](FIVE_ROOT_BOUNDARY_TRANSVERSAL_BLOCKER_CLASSIFICATION.md).

The coordinate-boundary exception is sharper than the resultant envelope.
In the projective space of ten nonzero `3 x 3` blocks, the closure of the
true no-torus locus has codimension at least two.  A general point of any one
degree-108 boundary-resultant divisor has one simple boundary root and 23
simple torus roots.  The affine statement includes zero blocks separately;
each whole-zero-block locus has codimension nine.  This still does not show
that witness blocks avoid the codimension-two exception:
[`FIVE_ROOT_NO_TORUS_CODIMENSION_TWO_THEOREM.md`](FIVE_ROOT_NO_TORUS_CODIMENSION_TWO_THEOREM.md).

The resulting exact five-root alternatives are now:

```text
some induced block is zero,
no torus root on a codimension-at-least-two exceptional locus,
five blockers  -> P_5 -> Delta_3,
six blockers   -> P_6 -> Delta_3,
or at least seven blockers.
```

The unrestricted `P_6` restriction remains open.  It has an exact
simultaneous-kernel criterion: a `240 x 6` off-diagonal contraction matrix
must have rank at most three and retain diagonal rank three on its kernel.
The six-blocker incidence reduces to six common-port deletion profiles.
Coordinate-column restrictions and the natural zero-row lift of the known
support-four `P_5` family are impossible, but dense maps remain.  In the most
constrained `1+1+1` profile, the three overlapping pure-`P_5` deletions reduce
to a marked `R_2 x R_3 -> R_5` Frobenius incidence.  Its linear relaxation is
exactly consistent.  A new rank-five configuration proves that `dim K>=6`
would be false: it has `dim K=5`, marked quotient rank three, and a
two-dimensional decomposable mixed allowance.  The first nonlinear wall has
a necessary rank-two `5 x 5` bilinear catalecticant.  Twenty-two split minors
reduce to sixteen gates and 53 minimal gate covers.  The unique four-gate
cover is now exactly excluded: the cycle gates force the two alternating
coordinate planes, and a remaining catalecticant minor has value `-4` or `4`.
Every other cover is excluded by an invertible pairing in its gate span.
Thus the displayed rank-five model fails the first nonlinear condition, but
other rank-five configurations and the general `1+1+1` profile remain open:
[`P6_SIMULTANEOUS_KERNEL_AND_NATURAL_LIFT_OBSTRUCTIONS.md`](P6_SIMULTANEOUS_KERNEL_AND_NATURAL_LIFT_OBSTRUCTIONS.md),
[`P6_COMMON_PORT_111_FROBENIUS_REDUCTION.md`](P6_COMMON_PORT_111_FROBENIUS_REDUCTION.md),
[`P6_COMMON_PORT_111_RANK_FIVE_CATALYTICANT_CHECKPOINT.md`](P6_COMMON_PORT_111_RANK_FIVE_CATALYTICANT_CHECKPOINT.md),
[`P6_COMMON_PORT_111_UNIQUE_FOUR_GATE_OBSTRUCTION.md`](P6_COMMON_PORT_111_UNIQUE_FOUR_GATE_OBSTRUCTION.md), and
[`P6_COMMON_PORT_111_ALL_GATE_COVERS_OBSTRUCTION.md`](P6_COMMON_PORT_111_ALL_GATE_COVERS_OBSTRUCTION.md).

An exploratory wind-down calculation suggests a sharper next symbolic task,
but it has not been promoted to a replayable theorem.  On the dense
rank-five stratum, normalize the unique relation among the six exceptional
vectors and set `U=C^6/<(1,...,1)>`.  If `W_G` is the nine-dimensional span
of the triangular-prism forbidden products and
`D=<y1^2,...,y5^2>` is the square space of a frame, then

```text
dim K=5  <=>  dim(W_G intersect D)=4
         <=>  rank(D -> Sym^2(U)/W_G)=1.
```

Thus the five frame points must lie in one fibre of the projected Veronese
map `[y] -> [y^2 mod W_G]`.  The displayed solution appears locally rigid
modulo its ten obvious gauge directions, but its canonical fibre contains
ten rational points and many five-point bases, so its sixteen-gate
hypergraph is not a justified global normal form.  A next instance should
first make this exceptional-fibre/frame-orbit classification replayable,
then compute the gate-Chow obstruction orbit by orbit.  Do not cite this
paragraph as a proved repository result without an independent exact audit.

There is also a separate exact eight-vertex discriminant reduction.  A smooth
expected two-dimensional four-root complete intersection is connected by its
Koszul complex, hence irreducible, and its Chow class cannot be supported on
one coordinate boundary.  It therefore meets the torus, which would force
the impossible restriction `P_4 -> Delta_3`.  Any hypothetical eight-vertex
witness must consequently make all 70 induced four-root schemes singular or
excess-dimensional:
[`FOUR_ROOT_SMOOTH_TORUS_OBSTRUCTION.md`](FOUR_ROOT_SMOOTH_TORUS_OBSTRUCTION.md).

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
extension entries, source scalings, and homogeneous weights.  The
`triangle-(1,1,1)` cell is now closed by the later placement theorems.  The
remaining work is the other three all-pair graph cells, component-twenty
divisor intersections and projective/source-torus boundaries, weighted `H22`
on components nineteen through twenty-one, the corresponding remaining
special boundaries, and the universal `P_5` step.

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

python verify_five_root_no_torus_codimension_two.py
python audit_five_root_no_torus_codimension_two.py

python verify_odd_residual_port_permanent_extraction.py
python audit_odd_residual_port_permanent_extraction.py

uv run --with sympy python verify_five_root_tight_blocker_p5_extraction.py
python audit_five_root_tight_blocker_p5_extraction.py

python verify_four_root_smooth_torus_obstruction.py
python audit_four_root_smooth_torus_obstruction.py

uv run --with sympy python verify_p4_triple_kernel_rank_one_triangle_classification.py
python audit_p4_triple_kernel_rank_one_triangle_classification.py

uv run --with sympy python verify_p4_two_kernel_rank_one_triangle_classification.py
python audit_p4_two_kernel_rank_one_triangle_classification.py

uv run --with sympy python verify_p4_common_kernel_vertical_triangle_component.py
python audit_p4_common_kernel_vertical_triangle_component.py

uv run --with sympy python verify_p4_common_active_binary_triangle_component.py
uv run --with sympy python audit_p4_common_active_binary_triangle_component.py

uv run --with sympy python verify_p4_mixed_chain_transverse_component_inclusion.py
uv run --with sympy python audit_p4_mixed_chain_transverse_component_inclusion.py

uv run --with sympy python verify_p4_coincident_support_rank_one_star_component.py
python audit_p4_coincident_support_rank_one_star_component.py

python verify_p6_simultaneous_kernel_and_natural_lift.py
python audit_p6_simultaneous_kernel_and_natural_lift.py

python verify_p6_common_port_111_frobenius_reduction.py
python audit_p6_common_port_111_frobenius_reduction.py

uv run --with sympy python verify_p6_common_port_111_rank_five_catalecticant.py
python audit_p6_common_port_111_rank_five_catalecticant.py

uv run --with sympy python verify_p6_common_port_111_unique_four_gate_obstruction.py
python audit_p6_common_port_111_unique_four_gate_obstruction.py

uv run --with sympy python verify_p6_common_port_111_all_gate_covers_obstruction.py
python audit_p6_common_port_111_all_gate_covers_obstruction.py

uv run --with sympy python verify_p5_h31_coincident_support_rank_one_star_component_generic_obstruction.py
uv run --with sympy python audit_p5_h31_coincident_support_rank_one_star_component_generic_obstruction.py

uv run --with sympy python verify_p5_h31_common_kernel_vertical_triangle_component_generic_obstruction.py
python audit_p5_h31_common_kernel_vertical_triangle_component_generic_obstruction.py

uv run --with sympy python verify_p5_h31_common_active_binary_triangle_component_generic_obstruction.py
uv run --with sympy python audit_p5_h31_common_active_binary_triangle_component_generic_obstruction.py

uv run --with sympy python verify_p5_h31_common_active_binary_triangle_component_special_divisor_obstruction.py
uv run --with sympy python audit_p5_h31_common_active_binary_triangle_component_special_divisor_obstruction.py
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
- Do not call the twenty-one-component list exhaustive or promote generic fibre
  obstructions to special/projective fibres without the missing
  classifications.
- Prefer exact identities, normal forms, projective covers, and local algebra
  to broad search.
- After a meaningful theorem, update this handoff or replace it with a dated
  successor and leave the worktree clean.
