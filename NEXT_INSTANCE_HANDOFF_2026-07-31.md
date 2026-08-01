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
2. **All twenty-one certified components are generically closed at `P_5` for
   both marked `H31` and weighted `H22`.**  The first eighteen have empty
   fibres over the generic point by the earlier componentwise theorems.
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
   Its weighted-`H22` shared incidence leaves one exact finite branch, whose
   complete common kernel has a fixed nonzero rank-four transverse minor:
   [`P5_H22_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION_CANDIDATE.md`](P5_H22_COMMON_KERNEL_VERTICAL_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION_CANDIDATE.md).
   Its finite special divisor `q=0` is also closed on the component torus
   `p*phi!=0`, including the separately reconstructed rank-jump endpoints
   `phi=+1` and `phi=-1`.  Direct specialization adds the essential finite
   `D23` generator `h1^2*h2`; the endpoint shared kernel has dimension three,
   but fixed complementary one-marked minors remain rank four:
   [`P5_H22_COMPONENT19_Q0_SPECIAL_DIVISOR_OBSTRUCTION_VERIFICATION.md`](P5_H22_COMPONENT19_Q0_SPECIAL_DIVISOR_OBSTRUCTION_VERIFICATION.md),
   [`P5_H22_COMPONENT19_Q0_PHI_ENDPOINTS_OBSTRUCTION_VERIFICATION.md`](P5_H22_COMPONENT19_Q0_PHI_ENDPOINTS_OBSTRUCTION_VERIFICATION.md).
   The singular-basis divisor `q=phi` is likewise closed on `p*phi!=0` after
   replacing the generic basis by a regular row swap.  All eight function-field
   incidence ideals are unit; the only parameter-aware closure occurs at
   `phi=0`, where pair `23` has rank exactly two:
   [`P5_H22_COMPONENT19_Q_EQUALS_PHI_OBSTRUCTION_VERIFICATION.md`](P5_H22_COMPONENT19_Q_EQUALS_PHI_OBSTRUCTION_VERIFICATION.md).
   On the ordinary `p=0` divisor, the tensor is `T1111=4(q-phi)` rather than
   zero.  A regular-basis proof, direct exceptional-divisor certificates, and
   an eight-replay aggregate close the complete projective weighted-`H22`
   fibre over the entire nonzero all-pair-open locus
   `q*phi*(q-phi)!=0`.  This includes `q=+/-1`, `phi=+/-1`, both
   `q*phi=+/-1` divisors, all of their crossings, and the reciprocal
   weight-at-infinity chart.  The `q=phi` zero base has a verified smooth
   codimension-two zero ideal with normal fibre `P1`; exact construction and
   a 16-chart no-import audit close weighted `H22` on the full
   associated-graded first-normal `P1`, including `phi=+/-1`.  Proof B closes
   every exact linear DVR ray.  Arbitrary higher-order or ramified marked arcs
   remain `UNKNOWN`:
   [`P5_H22_COMPONENT19_P0_FINITE_BOUNDARY_GEOMETRY_RECONNAISSANCE.md`](P5_H22_COMPONENT19_P0_FINITE_BOUNDARY_GEOMETRY_RECONNAISSANCE.md),
   [`P5_H22_COMPONENT19_P0_ORDINARY_OBSTRUCTION_OPEN_VERIFICATION.md`](P5_H22_COMPONENT19_P0_ORDINARY_OBSTRUCTION_OPEN_VERIFICATION.md),
   [`P5_H22_COMPONENT19_P0_QPHIM1_INFINITY_NO_IMPORT_VERIFICATION.md`](P5_H22_COMPONENT19_P0_QPHIM1_INFINITY_NO_IMPORT_VERIFICATION.md),
   [`P5_H22_COMPONENT19_P0_FINITE_ORDINARY_AGGREGATE_VERIFICATION.md`](P5_H22_COMPONENT19_P0_FINITE_ORDINARY_AGGREGATE_VERIFICATION.md),
   [`P5_H22_COMPONENT19_Q_EQ_PHI_FIRST_NORMAL_NO_IMPORT_VERIFICATION.md`](P5_H22_COMPONENT19_Q_EQ_PHI_FIRST_NORMAL_NO_IMPORT_VERIFICATION.md).
   Component twenty is closed by exact open-incidence projection to four
   marking points and one uniform minor/transverse certificate:
   [`P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION.md).
   Its generic weighted-`H22` fibre is empty by an exhaustive shared
   orientation split and four exact finite/infinity unit ideals:
   [`P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION_CANDIDATE.md`](P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT_GENERIC_OBSTRUCTION_CANDIDATE.md).
   Its nine principal affine special divisors are also closed over their
   generic points by exact projection and uniform marked-minor certificates:
   [`P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT_SPECIAL_DIVISOR_OBSTRUCTION.md`](P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT_SPECIAL_DIVISOR_OBSTRUCTION.md).
   A single saturated all-minors certificate strengthens this to the entire
   finite normalized `(p+q)(p-q+1)!=0` sheet, including every special-divisor
   intersection inside the open:
   [`P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_NORMALIZED_AFFINE_OBSTRUCTION.md`](P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_NORMALIZED_AFFINE_OBSTRUCTION.md).
   The intrinsic `p-q+1=0` basis boundary has no binary neighbour over its
   generic point after replacing the collapsed generic basis, and the same
   replacement chart has empty weighted-`H22` fibre:
   [`P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_INTRINSIC_BOUNDARY_OBSTRUCTION.md`](P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_INTRINSIC_BOUNDARY_OBSTRUCTION.md),
   [`P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_INTRINSIC_BOUNDARY_OBSTRUCTION_CANDIDATE.md`](P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_INTRINSIC_BOUNDARY_OBSTRUCTION_CANDIDATE.md).
   At the excluded finite points `p=0,-1`, the plane tuples have zero
   restriction, but the transverse base ideal gives a full compactified
   Segre-direction `P1`; exact no-import replays close every direction for
   marked `H31` and shared weighted `H22`.  At `p=-1/2`, the straight
   fixed-source limit is only a zero-tensor `k=infinity` edge in component
   fifteen's closure, while every actual nonzero diagonal arc is already in
   the half-centre atlas:
   [`COMPONENT20_INTRINSIC_WALL_EXCEPTIONAL_FIBRES_CANDIDATE.md`](COMPONENT20_INTRINSIC_WALL_EXCEPTIONAL_FIBRES_CANDIDATE.md),
   [`P4_COMPONENT20_INTRINSIC_EXCEPTIONAL_BASE_GEOMETRY_PROOF_B.md`](P4_COMPONENT20_INTRINSIC_EXCEPTIONAL_BASE_GEOMETRY_PROOF_B.md).
   The complete diagonal source-torus DVR/Puiseux atlases over those two zero
   bases are also independently verified.  Their exact nonzero cone is
   `x1=x2=0,x0<=-min(val(u),val(v))`; the sixteen leading charts lie in
   components 18 and 16, with six rank-two interiors additionally in
   component 15.  The intrinsic kernel rows `(K0,e,e,e)` give pointwise Hall
   obstructions to every marked-`H31` deletion and both homogeneous
   weighted-`H22` directions:
   [`COMPONENT20_INTRINSIC_ZERO_DIAGONAL_DVR_ATLAS_CANDIDATE.md`](COMPONENT20_INTRINSIC_ZERO_DIAGONAL_DVR_ATLAS_CANDIDATE.md),
   [`COMPONENT20_INTRINSIC_ZERO_DIAGONAL_DVR_ATLAS_VERIFICATION.md`](COMPONENT20_INTRINSIC_ZERO_DIAGONAL_DVR_ATLAS_VERIFICATION.md),
   [`P4_COMPONENT20_TRANSVERSE_BASE_DIAGONAL_FAN_PROOF_B.md`](P4_COMPONENT20_TRANSVERSE_BASE_DIAGONAL_FAN_PROOF_B.md).
   The whole `p+q=0` diagonal-source-torus DVR wall is now closed for marked
   `H31`: a verified arc exhaustion reduces it to the displayed charts,
   embedded-`P_3` projective strata, and two directly verified special
   lower-pair families:
   [`P4_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY.md`](P4_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY.md),
   [`P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY_OBSTRUCTION.md`](P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY_OBSTRUCTION.md),
   [`P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_EXCEPTIONAL_LOWER_PAIR_OBSTRUCTION.md`](P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_EXCEPTIONAL_LOWER_PAIR_OBSTRUCTION.md), and
   [`P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_INFINITY_ENDPOINT_OBSTRUCTION.md`](P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_INFINITY_ENDPOINT_OBSTRUCTION.md).
   The same exact wall is now closed for weighted `H22`: a fresh independent
   aggregate audit checks all nine strata and the twelve wall-specific mask-6
   flags without claiming the full projective embedded-`P_3` component:
   [`P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY_OBSTRUCTION.md`](P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY_OBSTRUCTION.md).
   Component twenty-one's exact all-marking row-module certificate closes its
   generic `H31` fibre, while homogeneous Hall deficiency plus finite
   beta-diagonal and infinity row-module identities close weighted `H22`:
   [`P5_H31_COINCIDENT_SUPPORT_RANK_ONE_STAR_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H31_COINCIDENT_SUPPORT_RANK_ONE_STAR_COMPONENT_GENERIC_OBSTRUCTION.md),
   [`P5_H22_COINCIDENT_SUPPORT_RANK_ONE_STAR_COMPONENT_GENERIC_OBSTRUCTION_CANDIDATE.md`](P5_H22_COINCIDENT_SUPPORT_RANK_ONE_STAR_COMPONENT_GENERIC_OBSTRUCTION_CANDIDATE.md).
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
`H31` and weighted-`H22` exclusions.  Component twenty is now closed on its
entire finite normalized `(p+q)(p-q+1)!=0` sheet, including all special-divisor
intersections in that open.  The intrinsic `p-q+1=0` chart wall is closed
over its generic point, and its two finite zero-restriction base points have
closed compactified Segre-direction `P1` incidences and complete verified
diagonal source-torus atlases.  The `p+q=0` wall is now
verified for diagonal-torus DVR/Puiseux arcs for both marked `H31` and
weighted `H22`, including every actual nonzero half-centre arc.  Parameter
infinity, non-diagonal or arbitrary `GL_4` source changes, and the remaining
special/projective weighted-`H22` fibres of components nineteen through
twenty-one remain open, except for component nineteen's verified finite
`q=0,p*phi!=0` and `q=phi,p*phi!=0` divisors and its complete ordinary
`p=0`, `q*phi*(q-phi)!=0` projective weight fibre.  On the `q=phi` zero
base, the entire associated-graded first-normal `P1` and every exact linear
DVR ray are also closed.  Only arbitrary higher-order or ramified marked
arcs, the `q=0` or `phi=0` lower-pair boundaries, and
parameter-compactification directions remain outside those theorems.

A `VERIFIED` valuative analysis of diagonal source-torus arcs with
`p+q -> 0` has exact replays for the corrected mode-zero wedge, the generic
and exceptional min-plus equivalences, and the two surviving charts.  All
negative equal-weight and infinity strata are assigned to the lower-pair
frontier; the higher-rank charts are `B_full` with profile
`(4,4,4,3,3,3)` and `B_drop` with profile `(4,4,3,3,3,3)`.  A fresh audit
independently extracts the Laurent first coefficients in every valuation
regime and verifies the exhaustion for DVR/Puiseux arcs under the diagonal
source torus.  Exact placement in older component intersections and
non-diagonal source changes are not claimed:
[`P4_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY.md`](P4_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY.md).

Their complete marked `H31` fibres are closed by exact characteristic-zero
certificates.  `B_full` has one
doubled geometric marking, `B_drop` has two marking lines, and the
`a=-1/2` replacement family has no binary neighbour.  Uniform fixed-minor
identities, direct `a=0,-1` rank-five kernels, and pure transverse entries
close every actual normalized stratum on the charts.  The remaining
component-fifteen support-one fibres at `a=0,-1`, `y<0` and both
component-fourteen faces at the infinity endpoint `y=-r` have separate
direct obstruction certificates and fresh audits.  Together with the
complete embedded-`P_3` projective closure, this verifies the whole
diagonal-DVR wall for marked `H31`:
[`P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY_OBSTRUCTION.md`](P5_H31_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY_OBSTRUCTION.md).

Weighted `H22` is now also `VERIFIED` on the whole diagonal-DVR wall.  A fresh
aggregate audit reconstructs the exact `3+1+2+3=9` stratum partition, replays
the six previously closed rows, and matches the historical three-row
`UNKNOWN` set exactly to twelve direct normal-support-mask-6 flags.  On those
flags both all-alpha weighted diagonals vanish for arbitrary homogeneous
weight in the original wall coordinates.  Separate exact certificates close
both component-fourteen infinity endpoints.  Thus no actual diagonal-DVR
`H22` stratum remains open:
[`P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY_OBSTRUCTION.md`](P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY_OBSTRUCTION.md).

Two boundaries must not be conflated with this wall theorem.  The original
component-fourteen rank-exactness sentence and the original embedded-`P_3`
weight-endpoint transport remain `REFUTED`; later independent certificates,
not silent repairs, supply the needed wall coverage.  The full projective
embedded-`P_3` weighted-`H22` component remains `UNKNOWN` on unrelated
normal-mask, Grassmann-pivot, and orientation-endpoint strata, as do
non-diagonal source changes and the global conjecture.

For component nineteen, exact characteristic-zero projection reduces
deletions 0 and 1 to the unit ideal and deletions 2 and 3 to

```text
<h3, (q-phi)h0+1, h1*h2>.
```

The resulting four rational marking lines and both shared endpoints are now
closed by exact two-minor and pure-transverse certificates.

For weighted `H22`, `D01` has no binary fibre on either homogeneous chart.
Shared `D01`-pure/`D23`-binary compatibility leaves only
`lambda=1,h=(-1/(q-phi),0,t,0)`.  Its complete two-dimensional shared kernel
has mode-three determinant `-64 C p(pD-phi t C)^2`, nonzero on the common
genuine open.  A fresh no-import replay verifies the generic obstruction.

On `q=0`, fresh specialization over `Q(p,phi)` gives pair profile
`(3,4,4,3,3,3)` and the direct finite `D23` ideal

```text
<h3,phi*h0-1,h1*h2*(lambda-1),h1^2*h2>.
```

The last generator is essential and is absent from naive specialization of
the generic theorem.  The unique shared branch is
`lambda=1,h=(1/phi,0,t,0)`; a complete two-frame and fixed mode-three minor
close it on `p*phi*(phi^2-1)!=0`.  At `phi=+/-1` the kernel jumps from
dimension two to three.  Separate construction, structural proof, and
no-import verification reconstruct both signs and close their full genuine
opens with complementary fixed rank-four minors.  Thus the whole finite
`q=0` divisor is verified on the component torus `p*phi!=0`.  The `p=0`
zero-tensor boundary and `phi=0` chart boundary are not promoted.

On `q=phi`, the generic intrinsic marking is singular, so it cannot be
specialized.  A regular row-swap basis has determinant `-1`, pure support
`T1111=4p`, and pair profile `(4,4,3,3,3,3)` on `p*phi!=0`.  Independent
construction, structural proof, and no-import audit all close the complete
finite/infinity weighted incidence.  Proof B makes the mechanism explicit:
`D23` has identically zero all-alpha binary diagonal, while the only possible
reverse-orientation finite marking has an invertible `8 x 8` extension minor.
Parameter-aware elimination finds only a direct-`D01` closure at `phi=0`,
where pair `23` has rank two and hence lies outside the all-pair-open frontier.

On `p=0`, the ordinary restriction is not zero: the regular basis
`alpha0=Abar,beta0=Bbar+qB` gives only `T1111=4(q-phi)`.  Its exact nonzero
all-pair-open locus is `q*phi*(q-phi)!=0`, with profile `(3,3,4,3,3,3)`
off `q*phi=1` and `(3,3,3,3,3,3)` on that divisor.  Off the compatibility
divisor, shared incidence leaves `lambda=1,h=(0,0,t,0)` and a complete
three-dimensional extension kernel.  Complementary mode-zero and mode-three
minors verify emptiness on
`q*phi*(q-phi)*(q^2-1)*(phi^2-1)*((q*phi)^2-1)!=0`.

The excluded ordinary divisors are now closed separately.  Direct no-import
reconstructions handle `q=+/-1` and `phi=+/-1`.  On `q*phi=1`, a regular
row rescaling, complete three-frame, and complementary minors close the full
projective weight fibre away from the zero intersections.  On `q*phi=-1`,
the individual rank test first leaves two coordinate axes; full two-slice
compatibility obstructs them.  At `phi^2=1` the survivor jumps to the full
non-axis sheet `Y=0`, but a uniform mode-one stacked determinant closes it.
The reciprocal weight-at-infinity chart is independently empty because its
required `D23` all-alpha diagonal lies in the `D01` mixed ideal.  An aggregate
audit replays all eight certificates and verifies the exact divisor ledger.
Consequently the complete projective weighted-`H22` fibre is empty over every
ordinary nonzero all-pair-open point `q*phi*(q-phi)!=0`.

At the zero/projective `q=phi` base, the zero ideal is exactly `<p,q-phi>`,
smooth of codimension two, and its first normal tensor directions form `P1`.
Two normalized normal charts, finite/infinite homogeneous weights, and four
genuine-diagonal orientation opens give 16 exact incidence cases; a no-import
audit over `Q[phi]`, saturated only by `phi`, makes all 16 ideals unit.  Thus
the complete associated-graded first-normal `P1` is verified empty for every
`phi!=0`, including `phi=+/-1`.  Proof B independently obstructs every exact
linear DVR ray and records the missing endpoint algebra.  This does not prove
that arbitrary higher-order or ramified marking/extension valuations depend
only on the leading normal direction; those formal arcs remain `UNKNOWN`.
The `q=0` and `phi=0` loci are lower-pair boundaries, while parameter-chart
infinity and other projectivized base directions remain outside the aggregate
theorem.
The direct and aggregate replays are:
[`P5_H22_COMPONENT19_P0_QPHI_ONE_INDEPENDENT_VERIFICATION.md`](P5_H22_COMPONENT19_P0_QPHI_ONE_INDEPENDENT_VERIFICATION.md),
[`P5_H22_COMPONENT19_P0_QPHI_MINUS_ONE_TERNARY_COMPATIBILITY_OBSTRUCTION_VERIFICATION.md`](P5_H22_COMPONENT19_P0_QPHI_MINUS_ONE_TERNARY_COMPATIBILITY_OBSTRUCTION_VERIFICATION.md),
[`P5_H22_COMPONENT19_P0_QPHI_MINUS_ONE_PHI_ENDPOINTS_VERIFICATION.md`](P5_H22_COMPONENT19_P0_QPHI_MINUS_ONE_PHI_ENDPOINTS_VERIFICATION.md),
[`P5_H22_COMPONENT19_P0_Q_ENDPOINTS_NO_IMPORT_VERIFICATION.md`](P5_H22_COMPONENT19_P0_Q_ENDPOINTS_NO_IMPORT_VERIFICATION.md),
[`P5_H22_COMPONENT19_P0_PHI_ENDPOINTS_NO_IMPORT_VERIFICATION.md`](P5_H22_COMPONENT19_P0_PHI_ENDPOINTS_NO_IMPORT_VERIFICATION.md),
[`P5_H22_COMPONENT19_P0_QPHIM1_INFINITY_NO_IMPORT_VERIFICATION.md`](P5_H22_COMPONENT19_P0_QPHIM1_INFINITY_NO_IMPORT_VERIFICATION.md),
[`P5_H22_COMPONENT19_P0_FINITE_ORDINARY_AGGREGATE_VERIFICATION.md`](P5_H22_COMPONENT19_P0_FINITE_ORDINARY_AGGREGATE_VERIFICATION.md),
[`P5_H22_COMPONENT19_ZERO_BASE_NORMAL_CONE_PROOF_B.md`](P5_H22_COMPONENT19_ZERO_BASE_NORMAL_CONE_PROOF_B.md),
and
[`P5_H22_COMPONENT19_Q_EQ_PHI_FIRST_NORMAL_NO_IMPORT_VERIFICATION.md`](P5_H22_COMPONENT19_Q_EQ_PHI_FIRST_NORMAL_NO_IMPORT_VERIFICATION.md).

The historical stronger construction package claiming the larger open
without the `q*phi=+/-1` exclusions is `REFUTED` as a replayable certificate:
its frozen `D23` minor used the wrong linear factor, and after that correction
its advertised `phi=1` stacked witness is identically zero.  The smaller
proof-B/no-import theorem above is not affected.

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

The generic weighted-`H22` incidence on component twenty is also empty.
Finite individual `D01` projection gives the exact necessary marking ideal
`<h3,h0,F>`; the shared system is unit on that whole closed locus.  The
opposite finite orientation and both projective-infinity orientations are
unit directly.  This function-field theorem is separate from every special
divisor and from the diagonal-DVR `p+q=0` wall.

The follow-on exact projection proves that deletion-three binary-neighbour
incidence is supported precisely on `q=p+2`, `q=p`, `2pq-p+q=0`, `p=0,-1`,
and `q=0,1`.  Deletions one and two also acquire marking axes at `q=1/2` and
`p=-1/2`.  Exact characteristic-zero minor/transverse certificates close the
generic marked `H31` fibre on all nine divisors.  This does not close their
base intersections or the remaining normalization/projective/source-torus
boundaries.

The global normalized-affine replay saturates simultaneously by the genuine
binary diagonals and `(p+q)(p-q+1)`.  For all four deletions, the locus where
every maximal mode-three minor vanishes is the unit ideal, as is the locus
where the deleted pure transverse column vanishes.  Deletion zero projects
to the unit ideal, while the other three exact marking projections have
`6,6,7` primary components.  This closes every finite special-divisor
intersection inside the normalized open and supersedes the intersection
limitation of the divisor-generic theorem there.

On `q=p+1`, the generic intrinsic mode-zero basis collapses.  Returning to
the two actual rows of `U0` gives a replacement basis whose only pure
coefficient is `T_1111=-2p(p+1)`.  For each of the four source deletions, the
normalized genuine-binary incidence projects to the unit ideal over `C(p)`.
Thus even the binary neighbour is absent over the generic point of this
boundary.  Independently implemented weighted-`H22` replays also give the
unit ideal for all four individual and all four complete shared finite/infinity
orientation projections.  Thus the generic weighted-`H22` fibre on this wall
is empty as well.

The finite exceptions `p=0,-1` are not ordinary nonzero-`P4` fibres: their
complete restricted tensors vanish and all six pair ranks equal three.  The
base ideal `<p-q+1,q(q-1)>` is transverse at `(0,1)` and `(-1,0)`, so its
compactified tensor-direction fibre is exactly `P1` at each point.  With the
finite direction coordinate retained polynomially, independent replays make
all `16/16` marked-`H31` and `16/16` complete shared weighted-`H22`
projections unit.  Exactly two individual finite-`D01` neighbour schemes
survive, and both disappear under same-extension compatibility.

Their complete diagonal source-torus DVR/Puiseux atlases are now also
`VERIFIED`.  For local deviations `u,v`, the nonzero cone is exactly
`x1=x2=0,x0<=-min(val(u),val(v))`.  Four ultrametric residue branches and two
torus faces give sixteen charts across the two centres.  The interiors lie
in component eighteen, six lower-pair interiors also lie in component
fifteen, and the walls lie in component sixteen.  Every chart has intrinsic
kernel rows `(K0,e,e,e)`, so direct Hall deficiency closes all four marked
`H31` deletions and both homogeneous weighted-`H22` directions, including
weight infinity.  The independent verifier reconstructed the min-plus fan,
leading planes, residue-stable ranks, closure hypotheses, and Hall identities
without importing either discovery implementation.

At `p=-1/2`, the straight fixed-source limit has zero restriction and pair
profile `(3,3,2,3,3,3)`.  It is the formal `k=infinity` edge of the
half-centre family and lies in component fifteen's closure by an explicit
support-one secant arc.  It is not a missing genuine wall stratum: an exact
min-plus audit proves that every nonzero-`P4` diagonal `s=0` arc is one of the
already verified finite-`k` or embedded-`P3` half-centre charts.  Parameter
infinity and non-diagonal or arbitrary source limits are not included.

For component twenty-one, three alpha rows have a two-column Hall
neighbourhood after every homogeneous `D01` contraction.  Finite `D23`
all-alpha incidence survives only at `lambda=-1`, where its all-beta diagonal
is identically zero in the complete normalized mixed ideal; at infinity the
all-alpha row belongs to the mixed row module.  Thus its generic weighted
`H22` fibre is empty, while its special/projective fibres remain open.

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
twenty-one-component list is exhaustive would not automatically close the
special/projective fibres on components nineteen through twenty-one or the
final local-to-global step.

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
remaining work is the other three all-pair graph cells, the remaining
non-diagonal or arbitrary `GL_4` source boundaries for component twenty,
the remaining special/projective weighted-`H22` fibres on components
nineteen through twenty-one, and the universal `P_5`
step.

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

uv run --with sympy python verify_p5_h31_common_active_binary_triangle_normalized_affine_obstruction.py
uv run --with sympy python audit_p5_h31_common_active_binary_triangle_normalized_affine_obstruction.py

uv run --with sympy python verify_p5_h31_common_active_binary_triangle_intrinsic_boundary_obstruction.py
uv run --with sympy python audit_p5_h31_common_active_binary_triangle_intrinsic_boundary_obstruction.py

uv run --with sympy --with z3-solver python verify_p4_common_active_binary_triangle_p_plus_q_boundary.py
uv run --with sympy --with z3-solver python audit_p4_common_active_binary_triangle_p_plus_q_boundary.py

uv run --with sympy python verify_p5_h31_common_active_binary_triangle_p_plus_q_boundary_obstruction.py
uv run --with sympy python audit_p5_h31_common_active_binary_triangle_p_plus_q_boundary_obstruction.py

uv run --with sympy python verify_p5_h31_common_active_binary_triangle_p_plus_q_exceptional_lower_pair_obstruction.py
uv run --with sympy python audit_p5_h31_common_active_binary_triangle_p_plus_q_exceptional_lower_pair_obstruction.py

uv run --with sympy python verify_p5_h31_common_active_binary_triangle_p_plus_q_infinity_endpoint_obstruction.py
uv run --with sympy python audit_p5_h31_common_active_binary_triangle_p_plus_q_infinity_endpoint_obstruction.py

uv run --with sympy python verify_p5_h22_common_active_binary_triangle_p_plus_q_boundary_partial.py
uv run --with sympy python audit_p5_h22_common_active_binary_triangle_p_plus_q_boundary_partial.py

uv run --with sympy python verify_p5_h22_common_active_binary_triangle_p_plus_q_generic_d01_infinity_obstruction.py
uv run --with sympy python audit_p5_h22_common_active_binary_triangle_p_plus_q_b_full_infinity_finite_pair_verifier.py
uv run --with sympy python audit_p5_h22_common_active_binary_triangle_p_plus_q_generic_d01_infinity_b_drop.py

uv run --with sympy python verify_p5_h22_common_active_binary_triangle_p_plus_q_exceptional_fibres_obstruction.py
uv run --with sympy python audit_p5_h22_common_active_binary_triangle_p_plus_q_exceptional_fibres_independent.py

uv run --with sympy python verify_p5_h22_common_active_binary_triangle_p_plus_q_boundary_obstruction.py
uv run --with z3-solver python audit_p5_h22_common_active_binary_triangle_p_plus_q_boundary_obstruction.py

uv run --with sympy python derive_p5_h22_p_plus_q_diagonal_dvr_mask6_actual_free_planes_obstruction_candidate.py
uv run --with sympy python audit_p5_h22_p_plus_q_diagonal_dvr_mask6_actual_free_planes_independent.py

uv run --with sympy python derive_p5_h22_common_kernel_vertical_triangle_component_generic_obstruction_candidate.py
uv run --with sympy python audit_p5_h22_common_kernel_vertical_triangle_component_generic_obstruction_candidate.py

uv run --with sympy python derive_p5_h22_component19_q0_special_divisor_obstruction_candidate.py
uv run --with sympy python derive_p5_h22_component19_q0_special_divisor_proof_b.py
uv run --with sympy python audit_p5_h22_component19_q0_special_divisor_obstruction_candidate.py

uv run --with sympy python derive_p5_h22_component19_q0_phi_endpoints_obstruction_candidate.py
uv run --with sympy python derive_p5_h22_component19_q0_phi_endpoints_proof_b.py
uv run --with sympy python audit_p5_h22_component19_q0_phi_endpoints_obstruction_candidate.py

uv run --with sympy python derive_p5_h22_component19_q_eq_phi_special_divisor_obstruction_candidate.py
uv run --with sympy python derive_p5_h22_component19_q_equals_phi_divisor_proof_b.py
uv run --with sympy python audit_p5_h22_component19_q_equals_phi_obstruction_candidate.py

uv run --with sympy python audit_p4_component19_p0_finite_boundary_geometry.py
uv run --with sympy python derive_p5_h22_component19_p0_ordinary_open_proof_b.py
uv run --with sympy python audit_p5_h22_component19_p0_ordinary_obstruction_open.py

uv run --with sympy python derive_p5_h22_component19_p0_qphi_one_ordinary_obstruction_candidate.py
uv run --with sympy python derive_p5_h22_component19_p0_qphi1_proof_b.py
uv run --with sympy python audit_p5_h22_component19_p0_qphi_equals_one.py

uv run --with sympy python audit_p5_h22_component19_p0_qphi_minus_one_axes.py
uv run --with sympy python derive_p5_h22_component19_p0_qphi_minus_one_axes_compatibility_obstruction.py
uv run --with sympy python audit_p5_h22_component19_p0_qphi_minus_one_ternary_compatibility.py
uv run --with sympy python audit_p5_h22_component19_p0_qphi_minus_one_phi_endpoints.py
uv run --with sympy python derive_p5_h22_component19_p0_qphi_minus_one_weight_infinity_obstruction_candidate.py
uv run --with sympy python audit_p5_h22_component19_p0_qphim1_infinity_no_import.py

uv run --with sympy python audit_p5_h22_component19_p0_q_endpoints_no_import.py
uv run --with sympy python audit_p5_h22_component19_p0_phi_endpoints_no_import.py
uv run --with sympy python audit_p5_h22_component19_p0_finite_ordinary_aggregate.py

uv run --with sympy python derive_p5_h22_component19_zero_base_first_normal_candidate.py
uv run --with sympy python derive_p5_h22_component19_zero_base_normal_cone_proof_b.py
uv run --with sympy python audit_p5_h22_component19_q_eq_phi_first_normal_no_import.py

# Expected assertion failure; retained REFUTED construction package:
uv run --with sympy python derive_p5_h22_component19_p0_ordinary_boundary_candidate.py

uv run --with sympy python derive_p5_h22_common_active_binary_triangle_component_generic_obstruction_candidate.py
uv run --with sympy python audit_p5_h22_common_active_binary_triangle_component_generic_obstruction_candidate.py

uv run --with sympy python derive_p5_h22_common_active_binary_triangle_intrinsic_boundary_obstruction_candidate.py
uv run --with sympy python audit_p5_h22_common_active_binary_triangle_intrinsic_boundary_obstruction_candidate.py

uv run --with sympy python derive_component20_intrinsic_wall_exceptional_fibres_candidate.py
uv run --with sympy python derive_p4_component20_intrinsic_exceptional_base_geometry_proof_b.py
uv run --with sympy --with z3-solver python audit_component20_intrinsic_wall_exceptional_fibres_candidate.py

uv run --with sympy --with z3-solver python derive_component20_intrinsic_zero_diagonal_dvr_atlas_candidate.py
uv run --with sympy --with z3-solver python derive_p4_component20_transverse_base_diagonal_fan_proof_b.py
uv run --with sympy --with z3-solver python audit_component20_intrinsic_zero_diagonal_dvr_atlas_candidate.py

uv run --with sympy python derive_p5_h22_coincident_support_rank_one_star_component_generic_obstruction_candidate.py
uv run --with sympy python audit_p5_h22_coincident_support_rank_one_star_component_generic_obstruction_candidate.py
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
