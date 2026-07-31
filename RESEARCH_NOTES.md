# Krenn-Gu prize problem: attack log

Status: **the prize conjecture is not solved**, but the six-vertex case is
closed by a computer-assisted proof, and every eight-vertex 4-regular
skeleton is now excluded by independently checked SAT certificates.  More
generally, an essential eight-vertex skeleton with a degree-four vertex is
excluded through 17 edges, and an exact-19-edge skeleton with a degree-three
vertex is excluded.  No finite counterexample was found.  The
repaired exact reductions exclude
every six-vertex killer selection with 9, 10, 11, or 12 union edges, and the
global support CNF excludes every larger minimum cover.  Hence
`(n,d)=(6,3)` has no complex solution; restriction to three colours gives
the same conclusion for `n=6`, `d>=3`.  The arbitrary even-`n` lift remains
open.  The authoritative six-vertex proof map is
`SIX_VERTEX_CERTIFICATE.md`.

## 31 July 2026: the corrected projective flat sheet

The Borel-generic flat rank-three-relation triangle is now closed on its
entire synchronized projective-partner pencil, not only the finite chart.
For the true marked-kernel normal form

```text
y=(1,1,1,1),              x=(0,1,p,q),
```

putting one of the other two planes at the pencil point `A^#` leaves three
and only three pure curves.  In terms of the four affine ratios
`(0,1,p,q)`, they say that one of the three disjoint pair sums agrees.  The
projective sheet has therefore exposed an additive parallelogram, or weak
Sidon failure, inside the osculating binary-cubic problem.

This is not a counterexample.  On every one of the three curves the product
image of `(A^#,A+uA^#)` has rank exactly two, so the point leaves the
rank-three-relation triangle and enters the lower-pair-rank
Segre/Kronecker boundary.  When both partners equal `A^#` projectively,
compression forces one quadratic factor while the escape condition forces
two incompatible affine differences.  That sheet is empty.  Exact primary
and independent subset-product replays are in
[`P4_RESONANT_FLAT_PROJECTIVE_PARTNER_CLASSIFICATION.md`](P4_RESONANT_FLAT_PROJECTIVE_PARTNER_CLASSIFICATION.md).

The full-support affine-ratio collisions have since been closed as well.
The honest resonant frontier is now smaller kernel supports, their collision
intersections, and compatibility with the other exceptional graphs.  The
global Krenn--Gu conjecture remains open.

At order 14, the equality-architecture factor types
`C3+C3+C8`, `C3+C4+C7`, `C3+C5+C6`, `C4+C5+C5`,
`C3+C3+C4+C4`, and `C14` are closed.  The remaining types are
`C4+C10`, `C6+C8`, and `C4+C4+C6`.  A fresh 425-selector reconstruction
now closes first-factor orbit 0 of `C4+C10`; its 1.63 MB DRAT proof
independently replays.  The exact local scope and hashes are recorded in
`FOURTEEN_VERTEX_C4_C10_ORBIT0_CERTIFICATE.md`.

A second fresh reconstruction closes first-factor orbit 1 of `C4+C10`.
It independently replays 882 minimized certificates to 19,632 new clauses,
audits all 425 selectors, and verifies a 1,673,263-byte DRAT proof.  Orbit
2 remains SAT in that reconstruction.  See
`FOURTEEN_VERTEX_C4_C10_ORBIT1_CERTIFICATE.md`.

A separate fresh 328-selector reconstruction now closes first-factor
orbits 0, 1, and 2 of `C6+C8`.  It independently replays 400 minimized
factor-fork certificates to 794 new clauses, then verifies one 375,964-byte
DRAT proof for the three-orbit selector disjunction.  The other 325
`C6+C8` selectors remain SAT, so this too is a local finite theorem only.
The exact hashes and one-command replay are recorded in
`FOURTEEN_VERTEX_C6_C8_ORBITS0_2_CERTIFICATE.md`.

That three-orbit result is now subsumed by a fresh global merge of 2,019
independently audited certificates.  It adds 36,080 deduplicated clauses
to the original base and closes exactly 108 of 328 selectors:
`0--4`, `100--143`, `200--218`, `220--225`, `227`, `232`, `233`,
`238`, `247`, `269`, and `300--327`.  A single 400,169-byte DRAT proof
for their selector disjunction independently verifies.  The other 220
selectors remain SAT.  See
`FOURTEEN_VERTEX_C6_C8_108_ORBITS_CERTIFICATE.md`.

An additional independently reconstructed layer replays 800 audited
minimum-activity certificates and adds 25,290 clauses.  It closes nine
more selectors: `171--173`, `179`, `182`, `185`, and `187--189`.
The resulting exact frontier is 117 UNSAT and 211 SAT selectors.  One
296,782-byte DRAT proof for the 117-selector disjunction independently
replays, and the full predecessor-to-extension chain is checked by
`verify_fourteen_vertex_c6_8_117_orbits.py`.  See
`FOURTEEN_VERTEX_C6_C8_117_ORBITS_CERTIFICATE.md`.

A subsequent colour-role reorientation experiment added 2,718 further
independently reconstructed clauses but closed no additional selector.
That negative result is exploratory evidence that this transport symmetry
alone does not strengthen the 117-orbit frontier.

Nine later independently reconstructed layers add 4,562 clauses from
1,334 audited certificates to the 117-orbit checkpoint.  The decisive
last layer consists of eleven full-only/one-extra cycle-factor cores
whose three-connected activation premises have size two or three.  Their
22 width-three or width-four clauses make first-factor orbit 5 UNSAT.
The exact all-selector audit is now 118 UNSAT and 210 SAT, with excluded
set `0--5`, `100--143`, `171--173`, `179`, `182`, `185`, `187--189`,
`200--218`, `220--225`, `227`, `232`, `233`, `238`, `247`, `269`, and
`300--327`.

The resulting 124,511-clause global CNF has SHA-256
`2c348a4e45478109a5453f55132b2b3ab78f579221a67e7970033d3380abc51f`.
Conditioning on the 118-selector disjunction gives SHA-256
`1214b396fe6a51b78ffa066a18cda5ef4699d492826dce89d709fdbd0900c33f`.
Kissat's 304,305-byte proof has SHA-256
`820ed6b38b69f76a8388d608a6dc122f1de490761838b10ce0cd2bd3547b5052`
and independently returns `s VERIFIED` under forward `drat-trim`.
`verify_fourteen_vertex_c6_8_118_orbits.py` replays the complete
predecessor, all nine extension layers, the 328 selector decisions, the
conditioned DIMACS sequence, and the raw proof.  See
`FOURTEEN_VERTEX_C6_C8_118_ORBITS_CERTIFICATE.md`.

The next selector closes as well.  Thirty-eight independently replayed
one-extra cycle cores on first-factor orbit 6 minimize to premise sizes
one through four.  Their stabilizer images add 152 clauses of width two
through five.  A separate targeted factor-fork run also reaches UNSAT,
while the promoted proof uses the smaller direct-core chain.

The new 124,663-clause global CNF has SHA-256
`5162bd3a83a0f730f2860059d39731ae439fe8dc085be3498339ba1c843ce300`.
The exact 328-selector audit is now 119 UNSAT and 209 SAT, with the first
excluded range extended from `0--5` to `0--6`.  The 119-selector
conditioned CNF has SHA-256
`8ca5d7cf43a81fe2d102e00ddf4e3f779fd0c8f55091fe749775bd23aa712b88`.
Kissat's 307,363-byte proof has SHA-256
`9e9e20ae8b271ac5caea452f90cef99ffcbdebd0eb5c036966dcb014e5d85bc4`
and independently returns `s VERIFIED`.  The complete predecessor,
augmentation, selector, DIMACS, and DRAT replay is
`verify_fourteen_vertex_c6_8_119_orbits.py`; see
`FOURTEEN_VERTEX_C6_C8_119_ORBITS_CERTIFICATE.md`.

Audit correction: the 118- and 119-orbit files exactly reconstruct their
stored clauses and DRAT proofs, but their final CNFs did not explicitly
contain the three-connectivity clauses required by their late minimized
activation certificates. Their unqualified finite-family wording was
therefore too strong.

The repaired chain appends and independently reconstructs all 1,947
vertex-connectivity-at-least-three quotient-cut clauses to the v18 rule
base. This alone closes orbit 144. A targeted orbit-7 continuation then
replays 184 independently audited minimum-activity certificates and adds
292 clauses. The resulting 559-variable, 126,902-clause CNF has SHA-256
`39e3770c6feaf67a58c873bc0d3dfc10f1f809b010389971dd51be8a256f89e6`.
Its exact selector audit is 121 UNSAT and 207 SAT, with excluded set
`0--7`, `100--144`, `171--173`, `179`, `182`, `185`, `187--189`,
`200--218`, `220--225`, `227`, `232`, `233`, `238`, `247`, `269`, and
`300--327`.

The 121-selector conditioned CNF has SHA-256
`784fa389c5503c6958f0661c6013aca87dfb62fdfa7a3918997117d564524424`.
Kissat's 3,328,458-byte proof has SHA-256
`59020245f2b7c9633cdc9ebf705af01fc09ec20c413eee0c2cfebae0ee4a43d2`
and independently returns `s VERIFIED` under forward `drat-trim`.
`verify_fourteen_vertex_c6_8_121_orbits_kappa3.py` replays the full
56.95-second chain and returns `"verified": true`. This is a theorem only
for support skeletons of vertex connectivity at least three, but that
scope covers every minimal counterexample because such a counterexample
is known to be 4-connected. See
`FOURTEEN_VERTEX_C6_C8_121_ORBITS_KAPPA3_CERTIFICATE.md`.

A subsequent targeted orbit-8 continuation produced 208 independently
audited minimum-activity certificates across 26 SAT iterations. Their
independent transports add exactly 238 clauses to the certified v20
predecessor. The v21 CNF has 559 variables, 127,140 clauses, and SHA-256
`8a03d170099f2dea4fe8fd8457dbbad4f85fdc1fc2811bb6559a1d01c0a9822d`.
Its exact selector audit is 122 UNSAT and 206 SAT, extending the first
excluded range to `0--8`.

The 122-selector conditioned CNF has SHA-256
`3b6b497fedfcb80433c9292b6a9def1654effdd1f923c257c8e64e80e6284819`.
Kissat's 2,847,347-byte proof has SHA-256
`06f33bde596365061a444ae4b0be6eab9b5091fb347aee1919ae2b6043013fff`
and independently returns `s VERIFIED` under forward `drat-trim`.
`verify_fourteen_vertex_c6_8_122_orbits_kappa3.py` recursively replays
the certified 121-orbit predecessor, independently reconstructs the
orbit-8 augmentation, re-audits all selectors, and returns
`"verified": true`. See
`FOURTEEN_VERTEX_C6_C8_122_ORBITS_KAPPA3_CERTIFICATE.md`.

Orbit 9 is now excluded by two independent certificate sequences. The
primary targeted route uses 136 audited certificates from 17 SAT
residuals and adds 360 clauses. Its v22 CNF has 127,500 clauses and
SHA-256
`af8b29041e787e9d59ff88bb1fa442276caf4df4b9494dbaa534df14914bc986`.
A separate direct one-extra-cycle-core route uses 61 certificates, adds
244 clauses to the same predecessor, and independently reports the same
123-UNSAT, 205-SAT selector frontier.

The 123-selector conditioned CNF has SHA-256
`ac5ddf9af8608ea01da65c87758dab087c867d5c8cfd6fdeca4859c2d7f2f7bc`.
Kissat's 1,418,915-byte proof has SHA-256
`f7fe06a37effeb6f58d18795b271efda00af0944d7216ab5852b0147e8426141`
and independently returns `s VERIFIED` under forward `drat-trim`.
`verify_fourteen_vertex_c6_8_123_orbits_kappa3.py` recursively replays
the predecessor and both orbit-9 routes and returns `"verified": true`.
See `FOURTEEN_VERTEX_C6_C8_123_ORBITS_KAPPA3_CERTIFICATE.md`.

In the `C4+C4+C6` family, a targeted three-connected structural-minimum
run on first-factor orbit 2 produced 168 independently audited
minimum-activity certificates.  Their 3,712 transported clauses were
reconstructed directly on top of the global checkpoint.  The resulting
952,108-clause global CNF has SHA-256
`c389a52cf9a2472a4caf5ddc193bc33ac611b7111f2f6aadede5e94189845b01`.
Imposing selector 2 gives a 952,109-clause UNSAT formula; its
54,151,092-byte DRAT proof independently replays.  The complete
predecessor-to-extension audit returns `"verified": true` in
`tmp/fourteen_vertex_c4_c4_c6_orbit2_final_verified.json`.  See
`FOURTEEN_VERTEX_C4_C4_C6_ORBIT2_CERTIFICATE.md`.  This is a finite
orbit theorem, not a solution of the complete family or global conjecture.

First-factor orbit 3 of `C4+C4+C6` is now excluded as well.  The verified
connectivity prerequisite contributes 2,576 quotient-cut clauses covering
all deletions of at most two vertices.  Independent symmetry transport of
272 audited structural-minimum certificates adds 5,856 clauses.  Imposing
selector 235 on the resulting 960,540-clause global CNF is UNSAT, and the
56,073,606-byte DRAT proof independently returns `s VERIFIED`.  An
independent algebraic verifier also reconstructs a four-clause dual-Horn
forcing core and one-relation lattice obstruction for one encountered
support.  See `FOURTEEN_VERTEX_C4_C4_C6_ORBIT3_CERTIFICATE.md`.  The full
family and global conjecture remain unresolved.

Two older range-audit artifacts are superseded:
`fourteen_vertex_c6_8_rule_sat_incremental_mid200_299_orbit_audit.json`
and the analogous `high300_326`/`orbit327` files used the orbit-zero
selector variable while only relabelling the output orbit offset.  The
corrected audits shift both the label and DIMACS selector.  They find 28
local closures in 200--299, all 27 in 300--326, and orbit 327.  A fresh
global reconstruction is authoritative over all of these range-local
counts.  The audit tool now supports `--selector-zero`, which derives the
selector start from the orbit offset and prevents this mismatch.

Two earlier algebraic checkpoints in this log are superseded.  Independent
replay found (1) an exact-fallback loop that stopped after one torus chart
without resuming boundary supports, and (2) a row/column reversal in the
old prism fixed singleton.  The repaired calculation continues every
fallback until support UNSAT, fixes the singleton orientation, audits the
vertex-colour gauge rank, and leaves every gauge-deficient singleton weight
as a Laurent variable.  Only artifacts explicitly named in
`SIX_VERTEX_CERTIFICATE.md` should be used for the final six-vertex claim.

## Exact target

For even `n`, `d` colours, and a `d x d` complex matrix `W_ij` on every
unordered vertex pair, define

```text
T_W(a_1,...,a_n)
  = sum over perfect matchings M
      product over {i,j} in M of W_ij[a_i,a_j].
```

The prize conjecture says `T_W` cannot equal the diagonal GHZ tensor

```text
Delta_n,d = sum_(c=1)^d e_c tensor ... tensor e_c
```

when `n >= 6` and `d >= 3`.  Restricting a hypothetical solution to any three
colours shows it is enough to rule out `d=3`.

As of 23 July 2026, the public frontier includes:

- a proof for arbitrary complex weights when `d >= n`;
- the full four-vertex obstruction (`d >= 4`);
- the conjecture for skeletons of vertex connectivity at most two and for
  maximum degree at most three.

Primary links:

- <https://mariokrenn.wordpress.com/graph-theory-question/>
- <https://github.com/google-deepmind/alphaproof-nexus-results>
- <https://github.com/google-deepmind/formal-conjectures/blob/af88acbf9da0f26e3e934743a819e986e02f6875/FormalConjectures/Paper/MonochromaticQuantumGraph.lean>
- <https://arxiv.org/abs/2407.00303>
- <https://github.com/bafflingbits/graph_n4_solution>

### July 2026 external cross-check

The problem page was updated on 23 July 2026 with AlphaProof Nexus's
machine-checked obstruction for `d >= n`.  The pinned Lean source proves the
explicit `d=n`, even-`n >= 4` theorem by constructing local vectors that
annihilate every edge incident with a selected vertex while leaving the GHZ
diagonal evaluation nonzero.  Its pigeonhole step uses `n` colours but only
`n-1` other vertices.  That step does not apply to the hard `d=3<n` regime.

The same current formalization explicitly continues to mark
`eqSystem8_no_solution_d3` and the general even-`n`, `d>=3` statement as
open.  Thus the external update neither supersedes nor completes the
finite certificates below.  Conceptually, its local-annihilator mechanism
is the large-colour counterpart of the distinct generic killer proposition
used here.

## Necessary rank-one edge proposition for the three-colour core

The following proposition falls out of the same contraction idea as the
recent `d >= n` proof, but exposes more local structure.

**Proposition.** If `T_W = Delta_n,3` and `n >= 4`, then for every vertex `v`
and every colour `c` in `{1,2,3}`, there is a distinct neighbour `u_c` such that
the block `W_(v,u_c)`, viewed with `v` as its row endpoint, is nonzero and has
all columns except column `c` equal to zero.  In particular:

1. `rank(W_(v,u_c)) = 1`;
2. the graph formed by nonzero rank-one blocks has minimum degree at least 3.

This is enough for the prize reduction because a solution with any `d >= 3`
restricts to a solution on any chosen three colours.  The proposition must
then be applied to that restricted `3 x 3` block system.  It does **not**, by
itself, prove the stronger published `d >= n` result: with four or more
nonzero summands, the linear-dependence circuits of decomposable tensors are
more complicated than the three-term Segre lemma used below.

### Proof

Fix a vertex `v` and contract its local factor against a generic vector `x`.
For every other vertex `u`, let

```text
l_u(x) = transpose(W_(v,u)) x.
```

Choose vectors `y_u` with `l_u(x)(y_u)=0`.  Every perfect matching contains
exactly one edge incident to `v`, so every perfect-matching term vanishes.
Because `T_W=Delta`, this forces

```text
sum_c x_c product_u y_(u,c) = 0.                         (1)
```

Let `q_u` be the quotient map on covectors modulo the line spanned by
`l_u(x)`.  Equation (1), for every choice of the `y_u` in the corresponding
hyperplanes, is equivalent to

```text
sum_c x_c tensor_u q_u(e_c) = 0.                         (2)
```

For generic `x`, absorb each nonzero `x_c` into one factor.  A standard
three-term Segre lemma says that if three nonzero decomposable tensors sum to
zero, then their factors are collinear in every tensor mode except possibly
one.  That is impossible here: in every two-dimensional quotient, the
classes of `e_1,e_2,e_3` span the quotient.

Nor can exactly one summand in (2) vanish.  If, for example, the first
summand vanishes at mode `u`, then `l_u(x)` is proportional to `e_1`.
The other two classes, `q_u(e_2)` and `q_u(e_3)`, are independent, whereas
the remaining two decomposable tensors would have to be proportional in
every mode.  Exactly two vanishing summands leave one nonzero summand, also
impossible.  Consequently every summand vanishes separately.

Thus, for each `c` and every generic `x`, some `u` satisfies
`transpose(W_(v,u)) x` proportional to `e_c`.  A finite union of proper
linear subspaces cannot contain a Zariski-open subset of a complex vector
space.  Hence, for each `c`, one fixed nonzero block satisfies

```text
image(transpose(W_(v,u_c))) subset span(e_c).
```

The neighbours `u_c` are distinct because the nonzero image of one matrix
cannot lie in two different coordinate lines.  This proves the proposition
for exactly three colours.

The remaining prize case is therefore already forced to contain a spanning
minimum-degree-three subgraph of rank-one edge blocks.  For `(n,d)=(6,3)`,
at least nine of the fifteen pair blocks are rank one.

### Reciprocal-killer counting lemma

The generic killers also give a useful density dichotomy.  Choose one
colour-`c` killer edge `K(v,c)` for every ordered pair `(v,c)`.  The three
chosen edges at one vertex are distinct, so there are exactly `3n` directed
killer incidences.  An undirected skeleton edge can receive at most one
chosen incidence from each endpoint.  Consequently, if the skeleton has
fewer than `3n` edges, some edge `uv` is chosen from both endpoints.

More precisely, let `r` selected edges receive incidences from both
endpoints and let `s` receive one.  Then

```text
2r+s = 3n,        r+s <= m,
```

where `m` is the number of nonzero pair blocks.  Hence

```text
r >= 3n-m.                                             (RK)
```

Orient its matrix with `v` on the row side.  If it is a colour-`c` killer
from `v` and a colour-`d` killer from `u`, then

```text
W_uv = a outer(e_c)
transpose(W_uv) = b outer(e_d).
```

The first display permits only column `c`, while the second permits only
row `d`.  Since a killer block is nonzero, their intersection is exactly

```text
W_uv = lambda e_d outer(e_c),   lambda != 0.
```

Thus every hypothetical witness satisfies the sharp alternative

```text
number of nonzero blocks >= 3n
```

or it contains a reciprocal-killer one-entry block.  In fact, (RK) supplies
at least `3n-m` distinct reciprocal singleton blocks.  Each may be
bichromatic; it is monochromatic precisely when `c=d`.  At the boundary
`m=3n`, either a reciprocal singleton still occurs or every skeleton edge
is one of the selected rank-one killers.

For `n=8`, every 20-, 21-, 22-, or 23-block dense case therefore has such
an edge.  Vertex and common-colour relabelling reduce it to two cases:
`(c,d)=(0,0)` and `(c,d)=(0,1)`.  In the normalized-killer CNF, the
already fixed incidence `K(0,0)=01` is variable `905`; the two reciprocal
incidences are variables `968` and `989`, respectively.  Their defining
clauses independently show that the surviving entry of `W_01` is
`W_01[0,0]` in the first case and `W_01[1,0]` in the second.  This is a
search reduction, not yet an exclusion of either case.

The exact CNF prefix/tail split and those candidate definitions are replayed
by:

```text
python verify_reciprocal_killer_partition.py
```

For the exact 20-block slice, (RK) forces at least four reciprocal
singletons.  `augment_reciprocal_cardinality.py` introduces all 252 possible
reciprocal candidate conjunctions and a sequential-counter lower bound of
four in each normalized colour case.  The byte-exact extensions, all 168
killer-candidate definitions, and the counting identity are independently
replayed by:

```text
python verify_reciprocal_cardinality.py \
  --manifest tmp/eight_vertex_normalized_killers_reciprocal_same_min4_max20.json
python verify_reciprocal_cardinality.py \
  --manifest tmp/eight_vertex_normalized_killers_reciprocal_different_min4_max20.json
```

The same count sharpens the exact 19-block degree-three frontier.  After
normalizing the singleton star at vertex 0, choose the reverse killer at
vertices 1, 2, and 3 to be the corresponding star edge.  These are three
reciprocal edges.  The other 18 directed killer incidences use at most the
16 non-star skeleton blocks, so at least two more reciprocal singleton
edges lie among vertices 1 through 7.

The residual symmetry is `S_3 x S_4`: `S_3` acts diagonally on the three
star leaves and the three colours, while `S_4` acts on vertices 4 through
7.  One further reciprocal edge has 189 labelled edge/endpoint-colour
descriptors and exactly 13 orbits under this group.  The enumeration,
candidate-variable translation, disjointness, and exhaustive orbit cover
are independently replayed by:

```text
python enumerate_degree3_reciprocal_orbits.py
python verify_degree3_reciprocal_orbits.py

verified: true
descriptors: 189
group order: 144
orbits: 13
```

This is an exhaustive case reduction, not yet an exclusion of all 13
cases.  The exact CEGAR runner accepts fixed DIMACS assumptions so each
representative can be closed without weakening the globally valid
Laurent and Singular no-goods.

There is a sharper anchor-sensitive dichotomy inside this split.  Orient a
chosen killer incidence toward its other endpoint.  If an edge is a
bichromatic reciprocal killer, then at either endpoint it cannot be a
diagonal anchor for any colour: its one surviving entry is off-diagonal
for its own killer colour, and every other diagonal entry vanishes.
Likewise, an incoming-only killer can be an anchor only if its block is
already a monochromatic singleton.

Assume that the normalized degree-three star supplies the only
monochromatic singleton blocks.  At a vertex touched by a bichromatic
reciprocal, the anchor for that outgoing killer colour must therefore use
an edge outside the union of the three outgoing killer edges and all
incoming killer edges.  Let `t_v` be the number of incoming chosen killers,
`q_v` the number of reciprocal chosen killers, and let `N_b` be the number
of vertices touched by a bichromatic reciprocal.  Summing

```text
deg(v) >= 3 + t_v - q_v + 1_(v touched bichromatically)
```

and using `sum t_v=3n` and `sum q_v=2r` gives

```text
2m >= 6n - 2r + N_b.                                  (RA)
```

For the normalized `(n,m)=(8,19)` degree-three case, the three star edges
are monochromatic reciprocals.  If there is no additional monochromatic
singleton, write `r=3+r_b`.  Then (RA) says

```text
r_b >= 2 + N_b/2.
```

Two or three distinct bichromatic core edges touch at least three vertices,
so neither value can satisfy the inequality; four can.  Consequently every
hypothetical witness obeys the stronger exhaustive alternative:

```text
an additional monochromatic singleton exists among vertices 1..7,
or at least four additional core reciprocals are bichromatic.
```

Equivalently, the second branch has at least seven reciprocal selected
edges in total, not merely five.  This refinement is useful only when the
monochromatic-singleton branch is kept separately; the forced star itself
prevents applying a blanket no-singleton count.

### Failure-hyperplane backup theorem

The generic killer has a useful second-order consequence at every skeleton
degree.  Write the selected colour-`c` killer at `v` as

```text
K_c = a_c outer(e_c).
```

If `a_c` is not proportional to `e_c`, then some different incident block
`B` satisfies

```text
B[:,j] in span(a_c)       for every j != c,
B[:,c] not in span(a_c).
```

In particular, `B[:,c]` is nonzero.  Call `B` a failure-hyperplane backup
for `K_c`.

To prove this, put `x` at a generic point of the hyperplane
`a_c perpendicular`.  Because `a_c` is non-coordinate, one may also require
`x_c != 0`.  Any other primary killer whose failure hyperplane does not
contain `a_c perpendicular` can be kept active, so it annihilates its own
target term.  If another killer vector is parallel to `a_c`, its term may
survive too.  At the disabled `K_c` mode, however, the surviving terms have
the linearly independent coordinate factors `e_j`; flattening (2) at that
mode forces every surviving rest tensor to vanish separately.  In
particular, the colour-`c` term must vanish in some other quotient mode.
Thus another incident block `B` obeys

```text
transpose(B) x in span(e_c), nonzero,
```

for each generic `x` in `a_c perpendicular`.  There are finitely many
incident blocks, so irreducibility of the hyperplane makes one fixed `B`
work on a dense subset and hence throughout the hyperplane.  Its
non-`c` columns annihilate `a_c perpendicular` and therefore lie in
`span(a_c)`; its `c` column cannot lie there because its contraction is
generically nonzero.

At support level this is already restrictive: each nonzero non-`c` column
of `B` has exactly the same zero pattern as `a_c`.  The strengthened
eight-vertex CNF encodes this necessary condition with explicit backup
indicators.  The theorem subsumes the proportionality part of the earlier
degree-four analysis and, unlike that special case, remains valid at
degrees five and above.

The argument iterates to a complete local flag.  For every `(v,c)` there
are distinct incident edges `E_1,...,E_k`, with `1 <= k <= 3`.  Write
`b_i=E_i[:,c]` on the `v` side and
`A_i=span(b_1,...,b_i)`, with `A_0=0`.  They can be chosen so that

```text
b_i not in A_(i-1),
E_i[:,j] in A_(i-1) for every j != c,
e_c in A_k.
```

Indeed, after `i-1` choices the common failure space is
`S=A_(i-1) perpendicular`.  If `e_c` is not yet in `A_(i-1)`, then `S`
is not contained in `x_c=0`.  At the first disabled flag edge the quotient
factors of the surviving colour terms are independent coordinate vectors,
so the colour-`c` rest tensor must vanish separately.  A fixed new incident
edge therefore kills it generically on `S`; its non-`c` columns lie in
`S perpendicular=A_(i-1)`, while its `c` column enlarges that span.  The
dimension rises at each step, so the process stops within three steps.

This **local killer-flag theorem** is stronger than the one-backup support
encoding.  It supplies a systematic next strengthening: length-two flags
force a vanishing `2 x 2` determinant, and length-three flags force a
nonzero `3 x 3` determinant, in addition to the triangular column-span
conditions.

### Diagonal-anchor refinement

There is a second local consequence that does not require a generic
contraction.  For every vertex `v` and colour `c`, some neighbour `u` has

```text
W_vu[c,c] != 0
W_vu[c,b]  = 0 for every b != c
```

when `v` is the row endpoint (with the transposed statement under the other
orientation).

Indeed, contract `v` against `e_c`.  For each `u`, let `l_u` be row `c` of
the corresponding block and independently choose `y_u` in `ker(l_u)`.
Every perfect-matching channel vanishes, whereas the target contraction is
`product_u y_(u,c)`.  If no `l_u` were a nonzero multiple of `e_c`, each
kernel would contain a vector with nonzero `c` coordinate; choosing those
vectors independently would make the product nonzero, a contradiction.

Thus every `(vertex,colour)` has both a generic rank-one column killer and
a (possibly different) nonzero diagonal anchor.  This refinement has not
yet produced the arbitrary-`n` reduction, but it is a concrete additional
constraint on any hypothetical minimal counterexample.

There is also a useful incidence restriction.  At `v`, let `K_c` be the
distinct generic killer neighbour for colour `c`, and let `A_c` be a
diagonal-anchor neighbour.  If `A_c=K_b`, then necessarily `b=c`: the
`K_b` block is supported only on column `b`, while an anchor for `c`
contains the nonzero entry `(c,c)`.  Therefore every anchor either coincides
with its same-colour killer or uses a neighbour outside
`{K_1,K_2,K_3}`.  In particular, vertices of skeleton degree four have only
one possible extra neighbour on which all noncoincident anchors must
concentrate.

The sparse-graph paper states that a minimal counterexample is
4-connected, but its displayed reduction theorem can reduce a graph to the
exceptional four-vertex dimension-three witness.  The precise consequence
needed here is:

```text
a vertex-minimal counterexample either is 4-connected
or has a degree-three vertex.
```

Indeed, in the three-cut reduction the smaller graph has
`|V_1|+3` vertices, with `|V_1|` odd.  The exceptional four-vertex output
occurs only when `|V_1|=1`; that isolated component of the cut has all its
neighbours in the three-vertex separator and hence has degree at most
three (and exactly three in the matching-covered, 3-connected case).  If
the minimum degree is at least four, then `|V_1|>=3`, so the reduction
produces a smaller graph on at least six vertices and really contradicts
vertex minimality.  The degree-three singleton-star theorem is therefore
attacking exactly the escape case, not merely a convenient sparse slice.

The eight-vertex calculations below still do not rely on the stronger
published slogan: the one 4-regular class with a three-vertex cut was
screened and certified directly.

### Degree-three singleton-star theorem

The degree-three case is even more rigid than degree four.

**Proposition.**  If `v` has exactly three nonzero block neighbours in a
three-colour solution, then its incident blocks are, after labelling those
neighbours by colour,

```text
W_(v,u_c) = alpha_c e_c outer(e_c),   alpha_c != 0,
```

one singleton of each colour.

The three distinct generic killers exhaust the neighbourhood, so write

```text
W_(v,u_c) = a_c outer(e_c).
```

The diagonal-anchor lemma has no spare neighbour available.  Its
colour-`c` anchor must therefore be the same `c`-killer, giving
`a_c[c] != 0`.  Let `P_c` be the perfect-matching tensor after deleting
`v,u_c`.  In the all-colour-`c` amplitude, the other two killer edges vanish
at their leaf endpoints, so

```text
a_c[c] P_c(c,...,c) = 1.                              (5)
```

If `a_c[b] != 0` for some `b != c`, colour `v` by `b` and every other
vertex by `c`.  The `c`-killer channel contributes the nonzero value
`a_c[b] P_c(c,...,c)`, while each other killer channel still vanishes at
its leaf.  This is a forbidden nonmonochromatic amplitude with one nonzero
channel, a contradiction.  Hence `a_c` is proportional to `e_c` for every
`c`.

Comparing the full slice with `v` coloured `c` gives the stronger identity

```text
P_c = alpha_c^(-1) e_c tensor ... tensor e_c.          (6)
```

Thus three overlapping `(n-2)`-vertex subhafnians are forced to be pure
monomials of three different colours.  This is the current analytic target
for eliminating degree-three vertices inside otherwise higher-degree
skeletons.

There is a further local consequence inside each pure minor.  Delete `v`
and the colour-`c` leaf `u_c`, and fix any remaining vertex `x`.  Contract
`x` against a generic vector `z`; for every other remaining vertex `y`,
write `l_y=W_xy^T z` and choose its local vector in `ker(l_y)`.  Every
matching channel vanishes, while the pure target evaluates to

```text
alpha_c^(-1) z_c product_y q_(y,c).
```

For generic `z` with `z_c != 0`, one of the finitely many hyperplanes
`ker(l_y)` must be contained in `q_(y,c)=0`.  Irreducibility makes one
fixed `y` work generically.  Hence every vertex of the deleted minor has a
nonzero colour-`c` killer whose other endpoint also lies in that minor.
The basis-vector version of the same argument gives a colour-`c` diagonal
anchor there as well.

For `n=8`, the three pure six-vertex minors therefore add 18 restricted
killer clauses and 18 restricted anchor clauses.  In particular, a core
vertex may not use the deleted colour-`c` star leaf as its only
colour-`c` killer or anchor.  The exact CNF prefix, all 144 underlying
candidate/anchor definitions, and the 36-clause tail are independently
checked by:

```text
python verify_degree3_pure_minor_constraints.py \
  --manifest tmp/degree3_e19_after_orbit01_pure.json

verified: true
killer clauses: 18
anchor clauses: 18
```

The exact support/torus computation now closes the 18-edge slice of this
case.  Nauty gives 332 unlabeled matching-covered graphs and 466 canonical
choices of the degree-three singleton star.  A symmetry-complete CEGAR chain
uses 21 signed Laurent-unit conflicts and seven exact characteristic-zero
Singular unit ideals; its final catalogue pass is UNSAT on all 466 roles
with no fallback.  The independent final audit is:

```text
python verify_eight_vertex_degree3_e18.py --rerun-singular-wsl

verified: true
target edges: 18
canonical roles: 466
fallbacks: 0
```

Every intermediate Laurent cube, CNF prefix/tail extension, reduced
Singular source, unit terminal, and full-support symmetry clause has also
been replayed independently.  This proves the finite statement only: an
eight-vertex complex witness with exactly 18 nonzero blocks cannot have a
degree-three vertex.

The clean exact-19 computation now closes the next slice as well.  The
complete catalogue contains 198 unlabeled connected matching-covered
skeletons and 235 canonical degree-three singleton-star roles.  A
theorem-level checkpoint supplies 112 exact Laurent conflicts and 15,912
learned symmetry clauses.  A fresh exhaustive pass supplies 252 further
conflicts and 35,496 clauses; 236 are Laurent-unit derivations and 16 use
exact rational linear-monomial relations.  Every one of the 235 roles is
UNSAT with no Singular fallback.

One selector CNF compiles the complete case split into 327,225 variables
and 2,465,388 clauses.  Kissat and CaDiCaL 1.9.5 independently return
UNSAT.  CaDiCaL's 186,169,429-byte DRAT proof is independently replayed by
`drat-trim`, which uses 64,029,123 resolution steps and returns
`s VERIFIED`.  The fail-closed audit,

```text
python verify_eight_vertex_degree3_e19.py
tmp/eight_vertex_degree3_e19_final_audit.json: "verified": true
```

replays all 364 exact conflicts, regenerates the complete graph and role
catalogue, checks the selector compilation and artifact hash chain, and
also recognizes 12 of the 252 fresh conflicts as elementary
cancellation-transport certificates and 35 more as two-monomial rectangle
or rectangle-transport certificates.  Therefore no eight-vertex,
three-colour, exact-19-edge
complex witness has a degree-three vertex.  The authoritative certificate
map is
`EIGHT_VERTEX_DEGREE3_E19_CERTIFICATE.md`.  This remains a finite theorem,
not an arbitrary-order exclusion.

### Cancellation transport between adjacent colourings

The exact Laurent conflicts expose a small but useful value-free
obstruction that is not part of the elementary support relaxation.

**Cancellation-transport lemma.**  Let `a` and `b` be two
non-monochromatic colourings that differ only at vertex `x`.  Suppose the
active perfect matchings at `b` form a nonempty set `S`, the active
matchings at `a` are exactly `S union {Q}`, and every matching in `S` pairs
`x` with one common neighbour `y`.  Then this support pattern is
impossible.

Indeed, all factors away from `x` are unchanged.  For every `M in S`, the
factor on `{x,y}` changes from the same nonzero entry `p` to the same
nonzero entry `q`.  Thus

```text
T_W(b) = (q/p) * sum_(M in S) m_M(a) = 0.
```

Since `q/p` is nonzero, the partial sum over `S` vanishes.  But
`T_W(a)=0` then forces the remaining monomial `m_Q(a)` to vanish, contrary
to every one of its factors being nonzero.  The argument works over every
field and uses no positivity or genericity.

`cancellation_transport.py` implements this exact criterion.
`verify_cancellation_transport_manifest.py` independently reconstructs
the active matching sets from a learned support cube and checks that both
ratio entries are explicitly nonzero.  On the clean 19-edge degree-three
batch it gives:

```text
conflicts checked                    252
conflicts with transport certificate  12
certified conflict indices
  1, 3, 4, 5, 77, 84, 142, 156, 202, 228, 229, 230
```

So this elementary lemma explains a genuine subset of the exact torus
contradictions, but not the other 224 Laurent-unit conflicts or the 16
new rational linear-monomial relations.  Its main prospective use is as a
cheap CEGAR rule and as the first local model for more general signed
transport circuits.

That CEGAR use is already concrete.  Scanning 66 full support models from
the two normalized 20-edge reciprocal branches found a transport
certificate in 58 of them.  On one fixed 19-edge degree-three catalogue
role, a transport-first rerun closed the role with five conflicts, versus
seven in the general Laurent-first run; every one of the five smaller cubes
was independently replayed and their 648 distinct symmetry clauses were
checked byte-for-byte.  This is a search acceleration and proof
simplification, not additional catalogue coverage by itself.

### Two-monomial rectangle obstruction

Some supports without a one-vertex transport certificate have an equally
small four-equation obstruction.  Start at a monochromatic colouring and
independently change the colours at two vertices `x,y`.  Suppose the same
two perfect matchings `M,N` are the only active matchings at all four
corners, and neither matching contains the edge `{x,y}`.  The four
amplitudes then have the form

```text
A_(i,j) = u_i v_j + p_i q_j,    i,j in {0,1},
```

where all eight displayed factors are nonzero.  Each matching monomial
separates in `i,j` because `x,y` lie on different matching edges.

If the three changed colourings are forbidden, then

```text
A_(0,1) = A_(1,0) = A_(1,1) = 0.
```

Division by the explicitly nonzero factors shows first that
`u_0/p_0=u_1/p_1`, and then that the cancellation ratio at the remaining
column is the same.  Hence `A_(0,0)=0`, contradicting the required nonzero
monochromatic amplitude.  This argument is exact over every field and is a
rank-one rectangle identity, not a numerical test.

There is a stronger rectangle-transport form.  All four corners may be
forbidden, with the same two matching monomials active at three corners and
those two plus one extra monomial active at the fourth.  The three
two-monomial equations again transport their cancellation to the fourth
corner, where the forbidden amplitude then forces the extra explicitly
nonzero monomial to vanish.  This form needs no monochromatic corner.

`support_two_monomial_rectangle_conflict` in
`cancellation_transport.py` detects the pattern and learns only the entries
needed to decide the four active matching sets.
`cube_two_monomial_rectangle_certificates` independently reconstructs it
from a saved cube, and `verify_laurent_batch_manifest.py` now dispatches
this certificate kind without invoking Laurent reduction.

The first 79 normalized 20-edge reciprocal support models split as:

```text
direct cancellation transport       72
two-monomial rectangle                7
Laurent fallback                      0
```

On a fixed survivor lacking direct transport, the rectangle check took
0.078 seconds and produced a 28-literal cube.  The older Laurent route took
1.65 seconds and produced a 50-literal cube.  Across seven such survivors,
independent replay accepted every rectangle and its 72 or 144 stabilizer
images.

A later exhaustive census used the stronger rectangle-transport form on a
pinned snapshot of 123 completed dense support logs: 89 from the
same-colour branch, 24 from the first different-colour run, and ten from
its recovered continuation.  It enumerated 716,994 rectangle certificates,
not merely the first lexicographic hit.  Every one of the 123 supports had
the following sharper **singleton-exchange motif** in one certificate:

1. a forbidden source colouring has exactly three active matchings
   `M,N,Q`;
2. `Q` contains the changed edge `{x,y}`, whose full `3 x 3` block support
   is one monochromatic singleton at the source colour;
3. changing the colour at `x`, at `y`, or at both leaves exactly `M,N`
   active;
4. `Q` differs from one of `M,N` by a single alternating four-cycle
   containing `x,y`; and
5. `M` and `N` differ on one alternating cycle.

The fourth and fifth features are matching-theoretically natural.  If two
perfect matchings are active at the same colouring, every matching obtained
by independently flipping a component of their symmetric difference is
active too.  Thus a cancellation partner may always be reduced to one
alternating component.  What remains unproved is the much stronger
existence of the singleton perfect-matching edge, the four-cycle flip
through it, and one common cancellation partner across the other three
corners.

The exploratory census is regenerated by
`analyze_rectangle_transport_census.py`.  Its fixed output is:

```text
tmp/eight_vertex_rectangle_transport_census.json
bytes  33,972,999
SHA-256
  5c5cddb5fe3c769d34ec37481cbe89543c624828941bd96aa1c87213f6248b31
```

Every source solver log is pinned by SHA-256 inside the census.  This is
exhaustive only for those 123 logged support models, not for the full SAT
relaxation.  Most models also have the smaller direct transport
certificate.

The singleton part of that pattern is an enumeration-order artefact, not a
consequence of the base relaxation.  Appending the exact negation of every
mixed singleton perfect matching adds 8,190 clauses to each reciprocal
branch.  Kissat found a SAT model in both branches.  A fail-closed audit
checks all 5,176,375 clauses against each full assignment, verifies the
extension byte-for-byte, and independently replays the elementary
conflicts:

```text
python verify_mixed_singleton_countermodels.py
tmp/eight_vertex_no_mixed_singleton_countermodels_audit.json:
  "verified": true

same-colour branch:
  singleton perfect matchings  1
  mixed singleton matchings    0
  direct transport             yes
  rectangle                    isolated-forbidden

different-colour branch:
  singleton perfect matchings  0
  mixed singleton matchings    0
  direct transport             no
  rectangle                    nonzero-target
```

The two models are not complex witnesses: their exact rectangle/transport
proofs exclude them.  They do refute the proposed finite lemma that the
local support theory forces a mixed singleton perfect matching.  Their
elementary no-goods, together with all completed live logs, were folded into
two independently replayed diverse recovery seeds.  The same-colour seed
contains 99 conflicts (88 direct, 11 rectangle); the resumed
different-colour seed adds 12 conflicts (11 direct, one rectangle).  Both
recovery audits return `"verified": true`.

There is a broader exact identity around any singleton edge `{x,y}`.  Fix a
nonmonochromatic colouring of the other vertices and sum only matchings
avoiding `{x,y}` into a `3 x 3` matrix `R` indexed by the colours at `x,y`.
The target slice is zero, while every matching using `{x,y}` is supported
at one coordinate, so

```text
R = -H W_xy
```

for a scalar minor amplitude `H`; hence `rank(R) <= 1`.  Therefore every
`2 x 2` minor of `R` vanishes.  `singleton_slice_minors.py` gives an exact
characteristic-zero certificate when such a minor has exactly one supported
monomial.  The detector is regression-tested, but three representative
dense survivors had no such unique minor, so this is currently a proved
identity rather than a new coverage result.

The full regression suite now has 36 passing tests.

This is more than a search heuristic: it identifies a second
characteristic-free cancellation mechanism that recurs in dense supports.
It is not yet a global proof because an arbitrary hypothetical support need
not expose a two-monomial rectangle.

### Odd binomial triangles and the signed-lattice normal form

The rectangle is one instance of a more general exact invariant.  If a
forbidden colouring has exactly two active matching monomials `A,B`, then
on the support torus

```text
A/B = -1.
```

Write `v=exp(A)-exp(B)` for its integer exponent-difference vector.
Reversing `v` leaves the value `-1` unchanged.  Three two-monomial
equations are therefore inconsistent whenever

```text
plus-or-minus v1 plus-or-minus v2 plus-or-minus v3 = 0:
```

multiplying their ratio equations gives `1=-1`.  The smallest previously
unexplained six-vertex example is exactly such an odd triangle.  In entry
variables its three reduced equations have the form

```text
x30*x39 + x33*x36 = 0
x3*x33  + x30*x6  = 0
x3*x39  + x36*x6  = 0.
```

The first two make the two terms in the third equal rather than opposite.
`odd_binomial_cycle.py` detects this signed circuit directly and replays it
from a support cube.

The full abstraction is a partial character on an exponent lattice.  Let
`L` be generated by the two-monomial difference vectors and assign each
generator the character value `-1`.  Exact integer coordinates give three
contradiction modes:

1. a dependent binomial is assigned `+1` by `L` but demands `-1`;
2. a forbidden amplitude reduces in the quotient group algebra to one
   nonzero signed monomial class; or
3. every signed class of a required monochromatic amplitude cancels, so
   that required amplitude is identically zero.

The proof is just exact character arithmetic.  Terms in different cosets
of `Z^E/L` are linearly independent; terms in one coset differ by the
recorded sign character.  This is the Laurent-binomial/partial-character
framework of Eisenbud and Sturmfels:
<https://eisenbud.github.io/papers/pdfs/1996-002.pdf>.

`signed_binomial_lattice.py` records every integer coordinate and has a
second replay path using only sparse integer-vector arithmetic.  It
subsumes both two-monomial rectangle modes and odd triangles whenever the
exposed relation basis has a unimodular pivot; it also subsumes the
two-shared-monomial instances of direct transport.  Transport with a larger
shared sum remains a separate elementary rule.

On the old 18-orbit six-vertex global residual:

```text
Laurent cubes audited                    146
signed-lattice certificates             146
inconsistent-binomial sign               85
isolated signed monomial class            61
covered by transport/rectangle/triangle  112
```

Thus the 34 cubes not explained by the earlier local detectors are all
the same phenomenon: binomial cancellations leave one nonzero class in a
three-, four-, or six-term forbidden amplitude.  The independently
generated coverage audit is

```text
tmp/global_pattern_orbits_elementary_coverage.json
SHA-256
  47be7fc873b80bfd73e884188d9a77506693279da484703e0b73714e133af51f
```

Two disjoint pinned dense-support censuses contain 136 and 52 models,
respectively.  Only 15 and 9 expose the literal odd triangle, but every one
of the 188 models has an independently replayed signed-lattice
certificate.  A later combined pass deduplicated all then-available source
logs and the two explicit no-mixed witnesses, giving 193 distinct models.
All 193 verify, with certificate modes

```text
isolated forbidden signed class          124
annihilated required nonzero target       44
inconsistent binomial sign character      25
```

The source logs are hash-pinned in:

```text
tmp/eight_vertex_odd_binomial_triangle_census.json
SHA-256
  b24704b4c06090b08e658def7ef2c5a6055498837e565962a6884016b2c17013

tmp/eight_vertex_diverse_signed_lattice_census.json
SHA-256
  91d427894d5a6c99e9358221d2df6fc3b3455e1eac5b3e750d9781170b4c49dc

tmp/eight_vertex_signed_lattice_combined_census.json
SHA-256
  a0366bf07062492dbb74c866de6d8efac1d1cc4b09000edb44963247db476e76
```

This is still finite evidence, not the prize proof.  The sharpened global
target is now precise: prove that every hypothetical three-colour support
induces an inconsistent partial character, an isolated forbidden class,
or an annihilated required class.  A counter-support avoiding all three
would be equally valuable because it would identify the genuinely
non-binomial obstruction that remains.

### Toric degeneration to balanced support

There is a global support-minimality reduction that does not depend on
`n=6` or `n=8`.  Give every local vertex-colour coordinate `(v,c)` an
integer potential `h_(v,c)` and scale a supported entry by

```text
W_uv[a,b](t)
  = t^(h_(u,a) + h_(v,b)) W_uv[a,b].
```

For a fixed vertex colouring `alpha`, every perfect matching acquires the
same exponent

```text
sum_v h_(v,alpha_v).
```

Therefore forbidden amplitudes remain zero for every nonzero `t`.  If

```text
sum_v h_(v,c) = 0                         for c=0,1,2
```

and every supported entry exponent is nonnegative, all three required
monochromatic amplitudes are unchanged and the limit `t -> 0` is finite.
If one supported exponent is positive, the limit is another exact witness
with strictly smaller entry support.

Choose a hypothetical witness with minimum entry support.  Let `A` be the
unsigned incidence matrix of its lifted support graph on the `3n` vertices
`(v,c)`, and let `B` record the three monochromatic coordinate sums.
Minimality says there is no `h` with

```text
B h = 0,     A h >= 0,     A h != 0.
```

The Gordan--Stiemke alternative is exact and gives strictly positive
weights `y_e` on **every** supported entry and numbers `mu_c` such that

```text
A^T y = B^T mu.
```

Equivalently, the `y`-weighted degree of every lifted vertex `(v,c)` is
`mu_c`, independent of `v`.  Each `mu_c` is positive because a required
monochromatic perfect matching meets every `(v,c)`.  Hence the prize
problem may be reduced, without loss of generality, to these **balanced
supports**.

There is an equivalent purely discrete form.  Add a nonnegative multiple
of one supported colour-`c` monochromatic perfect matching to `y` for each
`c`, raising all three `mu_c` to their maximum.  After rescaling, every
lifted vertex has weighted degree one and every lifted edge still has
strictly positive weight.  Thus the lifted support graph has a strictly
positive fractional perfect matching.  By the half-integrality theorem for
the fractional perfect-matching polytope, every supported entry is
contained in a spanning perfect 2-matching (a disjoint union of single
edges and odd cycles), and conversely averaging those 2-matchings gives a
strictly positive fractional perfect matching.  A general reference for
the vertex structure of fractional perfect `b`-matching polytopes is
<https://arxiv.org/abs/1301.7356>.  This converts the minimal support
condition into a finite combinatorial property.

This is a normal-form theorem, not the final contradiction.  It does,
however, discard nonminimal SAT strata rigorously.  On the combined 193
dense eight-vertex models, exact integer certificates give:

```text
supports with a shrinking toric direction       78
already balanced supports                       115

entries deleted in one step
  1:15, 2:9, 3:20, 4:14, 5:1, 6:18, 7:1
```

The discovery manifest and a separate sparse-integer replay are:

```text
tmp/eight_vertex_support_toric_census.json
SHA-256
  5a9ec5598fd1abef05fecaf0f2a4db0e13e5f902973b6fe2e128a7ff7869b659

tmp/eight_vertex_support_toric_census_verified.json
SHA-256
  3b105463a8918aac551e077f61854d34d712eae31e07d94bdd3261745eaf9cdf
```

The exact replay does not call the numerical LP solver: it checks either
the integer potentials and all supported exponents, or the positive
integer entry weights and all `3n` weighted degrees directly.

### Beyond literal binomials: exact factor-lattice CEGAR

Forbidding every two-term forbidden amplitude is not a universal support
principle, even at the current dense eight-vertex frontier.  A lazy exact
SAT search in the normalized same-colour reciprocal branch found an
exact-20-edge support after 22 models with the following active-monomial
counts:

```text
forbidden amplitudes
  4 active matchings: 5648
  5 active matchings:  748
  6 active matchings:  160
  7 active matchings:    2

required monochromatic amplitudes: 9, 7, 7 active matchings
```

The support has 84 selected matrix entries.  Its twenty nonzero pair
blocks consist of eight full `3 x 3` blocks and twelve one-entry diagonal
blocks:

```text
full:       04 05 14 15 23 26 37 67
colour 0:  01 27 36 45
colour 1:  02 13 47 56
colour 2:  03 12 46 57
```

Exact checks find no two-term forbidden amplitude, no odd binomial
triangle, and no direct signed-binomial-lattice certificate.  The toric
alternative classifies it as balanced, with a positive integer lifted
degree certificate of common degree seven.  This is a support model only:
the SAT variables record which entries and perfect-matching monomials are
nonzero, not complex values satisfying the amplitude sums.

The absence of literal binomials hides a stronger exact structure.  Every
four-term forbidden polynomial has exponent vectors at the corners of a
parallelogram:

```text
x^a + x^b + x^c + x^d
  = x^g (1 + x^r) (1 + x^s).
```

All selected entries are nonzero, so the amplitude equation implies the
disjunction `x^r=-1 or x^s=-1`.  The 5,648 amplitudes use 160 distinct
signed relations; their factor-choice graph is a connected bipartite graph
on two classes of 80 relations.  `factor_lattice_cegar.py` encodes one
two-literal clause per factorization and reduces each chosen relation set
over its exact integer exponent lattice.  Thirteen learned no-goods suffice
to close the factor CNF.  In every case the selected lattice cancels four
terms of a five-term forbidden amplitude and leaves one isolated nonzero
signed monomial class.

The factor step is not specific to eight vertices.  In any order, if four
active matching monomials in a forbidden amplitude have exponent vectors
`a,b,c,d` with `a+d=b+c`, then on the nonzero support torus

```text
x^a+x^b+x^c+x^d
  = x^a (1+x^(b-a)) (1+x^(c-a)).
```

Thus every such parallelogram forces a choice of one signed character value
`-1`.  A hypothetical witness must make all those choices consistently:
an integer dependency among chosen exponent differences may not have odd
coefficient sum, and reduction modulo the chosen lattice may not isolate a
nonzero class in any forbidden amplitude or annihilate a required one.
This gives an arbitrary-`n` **disjunctive signed-character calculus**.  What
remains unproved globally is that killer, anchor, flag, and balance
constraints force enough parallelograms to make that calculus
inconsistent.

The factor step extends one level further without changing the lattice
logic.  If eight active exponent vectors form an affine Boolean cube

```text
{a + epsilon_1 r + epsilon_2 s + epsilon_3 t :
   epsilon_i in {0,1}},
```

then the forbidden amplitude factors on the support torus as

```text
x^a (1+x^r) (1+x^s) (1+x^t).
```

Its vanishing forces the exact three-way clause
`x^r=-1 or x^s=-1 or x^t=-1`.  The new detector reconstructs the exponent
cube combinatorially and is regression-tested.  It is opt-in through
`factor_lattice_cegar.py --include-eight-term-cubes`, so all pinned
four-term manifests retain byte-identical semantics.  More generally, a
full affine `k`-cube would give a `k`-way signed-character clause; forcing
or detecting those higher cubes is another route beyond literal
binomials.

The final factor CNF has 160 variables and 5,661 clauses.  CaDiCaL 1.9.5
returns UNSAT; the 2,044-byte proof independently replays with
`drat-trim`:

```text
c parsing input formula with 160 variables and 5661 clauses
c 44 of 124 lemmas in core using 829 resolution steps
s VERIFIED
```

The independently reconstructed hashes are:

```text
tmp/eight_vertex_no_binomial_same_e20_factor_lattice.json
SHA-256
  13015d6b641b8bce648816c03f9e5ecf3fa04bc964fa504882671cb1110166b8

tmp/eight_vertex_no_binomial_same_e20_factor_lattice.cnf
SHA-256
  f95fbe55cf92e93816d25b1c77e5cee7a432e2b552aced8bfd27f80f3443e51b

tmp/eight_vertex_no_binomial_same_e20_factor_lattice_cadical195.drat
SHA-256
  d6c8f5947161e82e03b59e71c55b4940cec8b2ff78ec3e8fe23ac2956e31e260

tmp/eight_vertex_no_binomial_same_e20_factor_lattice_verified.json
SHA-256
  cfa66217b9b1ecd777df008dcf6372730d3f5a4d5e8837fc4ec650f43a2a19f1
```

This proves that particular 84-entry stratum empty over `C`; it does not
exclude every no-binomial support.  The support-level CEGAR has therefore
been resumed with this exact support blocked.

The next survivor is not isomorphic to the first under arbitrary vertex and
global-colour permutations.  It is again balanced with 84 entries, eight
full blocks, and twelve diagonal singletons, but its forbidden activity
histogram is `4:5240, 5:1026, 6:288, 9:4`.  The same factor-lattice engine
finds 160 relations and closes the 5,240 factor clauses with 72 isolated
class no-goods.  CaDiCaL's 10,001-byte proof for the resulting 5,312-clause
CNF also replays as `s VERIFIED`:

```text
tmp/eight_vertex_no_binomial_same_e20_factor_lattice_02.json
SHA-256
  67e1b7af34d40710db919d017b66d3e5cf2c6352fb574fe1a26b2385c5f0634f

tmp/eight_vertex_no_binomial_same_e20_factor_lattice_02.cnf
SHA-256
  de61502982d7e852a6b6c292fa0ae408d4727fd464e1b2637fe57ca90b1d88c5

tmp/eight_vertex_no_binomial_same_e20_factor_lattice_02_cadical195.drat
SHA-256
  a3de8c4185472ba322b6421f50eabf83011db8ccf9c23d3068fdac05fd8205b7

tmp/eight_vertex_no_binomial_same_e20_factor_lattice_02_verified.json
SHA-256
  76112967034f4ab6288ff41f30568539f1d6abf9da0436781a5c21b5e9cb1166
```

### Exhaustive 5-regular double-C4/singleton-factor macro-family

The two non-isomorphic binomial-free survivors have the same block-level
architecture:

```text
8 full 3 x 3 blocks
  = a spanning 2-factor with components C4 + C4

12 diagonal singleton blocks
  = a one-factorization of the complementary cubic graph,
    with one perfect matching assigned to each colour.
```

This observation can be exhausted without a SAT solver on every 5-regular
eight-vertex skeleton.  The complement of such a skeleton is a simple
2-regular graph, hence a disjoint union of cycles of length at least three.
The only partitions of eight into such cycle lengths are `8`, `5+3`, and
`4+4`.  Thus the three complement types `C8`, `C5+C3`, and `C4+C4` exhaust
the unlabelled skeletons.

`enumerate_five_regular_double_c4_singleton_family.py` lists every 8-edge
spanning two-`C4` factor, recursively finds every perfect matching of its
cubic complement, and retains every partition of that complement into
three perfect matchings.  The exact census is:

```text
complement   automorphisms   C4+C4 factors   factorizations   labelled   orbits
C8                     16              23              43        258       12
C5+C3                  60              15              30        180        1
C4+C4                 128              34             108        648       10
total                                   72             181      1,086       23
```

The factorization count is colour-unlabelled: assigning its three perfect
matchings to colours gives six distinct labelled entry supports.  This is
why 181 factorizations represent 1,086 labelled supports.  All 1,086 have
84 selected entries, satisfy the support relaxation, and have neither a
one-term nor a two-term forbidden amplitude.

The exact factor-lattice CEGAR was run on one representative of each of the
23 orbits.  Every final CNF is UNSAT, and every CaDiCaL 1.9.5 proof replays
with `drat-trim` returning `s VERIFIED`.  Across the audits there are 3,704
factor-relation variables, 126,044 four-term factor clauses, and 1,378
exact isolated-class lattice no-goods.

`verify_five_regular_double_c4_singleton_family.py` is a separate aggregate
verifier.  It independently proves the three-type complement
classification, reconstructs the two-`C4` factors by choosing all 8-edge
subgraphs rather than enumerating cycles, recursively regenerates all
complement matchings and one-factorizations, brute-forces all 40,320 vertex
permutations for each type, recomputes all 23 canonical orbits under global
colour permutations, checks every emitted model and amplitude-activity
histogram, and binds each orbit to its semantic factor-lattice audit and
replayed DRAT hash chain.  Its verified claim is:

**Finite theorem.**  None of the 1,086 labelled supports in the 5-regular
eight-vertex double-`C4`/singleton-factor macro-family can be the support
of a complex Krenn--Gu witness.

Pinned aggregate artifacts:

```text
tmp/eight_vertex_five_regular_double_c4_singleton_family.json
SHA-256
  6162df4f1feb5b8d82b9bd791bbc7d2e751515db5ddfad017431c5f447589c99

tmp/eight_vertex_five_regular_double_c4_singleton_family_verified.json
SHA-256
  92a571802b271df98e4b2c8cb7a100c96095bfeadfb5461dc2d45d28aa97b37f

enumerate_five_regular_double_c4_singleton_family.py
SHA-256
  b9c18d5a491ed9bcb52684e15149acd13b2389d30b68930f8815545f07f9588b

verify_five_regular_double_c4_singleton_family.py
SHA-256
  8b5eb5939a39542cced99f7baac8ff9273d6a7652325b210b3d02046ca9d6209
```

#### Removing the double-C4 assumption inside the architecture

The full blocks need not be assumed to form `C4+C4`.  Exhausting every
spanning 2-factor of every 5-regular skeleton gives:

```text
skeleton  full factor  factors  factorizations  labelled  binomial-free  orbits
C8        C5+C3             48             80       480              0       7
C8        C4+C4             23             43       258            258      12
C8        C8               177            294     1,764              0      35
C5+C3     C5+C3             60             60       360              0       1
C5+C3     C4+C4             15             30       180            180       1
C5+C3     C8               180            300     1,800              0       7
C4+C4     C5+C3             32             64       384              0       1
C4+C4     C4+C4             34            108       648            648      10
C4+C4     C8               184            344     2,064              0      12
total                      753          1,323     7,938          1,086      86
```

This yields a clean conditional support statement: within the
full-2-factor/singleton architecture, no-binomiality forces the full factor
to have type `C4+C4`.  Every `C8` or `C5+C3` full factor exposes a literal
two-term forbidden amplitude.

The binomial-bearing cases are not discarded merely for having a
binomial.  `factor_lattice_cegar.py --include-direct-binomials` treats every
such amplitude as a mandatory signed relation and combines it with all
four-term factor clauses.  All 63 additional graph/colour orbits are UNSAT,
each after one exact lattice branch.  Their 63 CaDiCaL proofs independently
replay as `s VERIFIED`, and their semantic verifiers reconstruct every
relation and conflict.  Combining those with the 23 double-`C4` audits
gives:

```text
factor relations      183,673
factor clauses        313,813
lattice no-goods        1,441
```

The 23 binomial-free `C4+C4` orbits admit a much smaller certificate than
the original factor-lattice CEGAR traces.  For each orbit, some four-term
full-only amplitude factors into two alternating-cycle choices, and each
choice is separately impossible in a five-term amplitude: two monomial
pairs cancel under the chosen relation and one supported monomial remains.
Thus three amplitudes close an orbit.  Independent reconstruction verifies
all 23 forks and binds them through the orbit census to the 1,086 labelled
binomial-free supports.  The redundant proof-producing versions of the 23
tiny CNFs total only 6,574 DRAT bytes.

**Stronger finite theorem.**  None of the 7,938 labelled supports in the
5-regular eight-vertex full-spanning-2-factor/singleton family can support
a complex Krenn--Gu witness.

Pinned aggregate artifacts:

```text
tmp/eight_vertex_five_regular_full_singleton_family.json
SHA-256
  546e63334dacddfb899beffbb8536e0c6983f9ae6710d1a6bfac8a9ea96b2d96

tmp/eight_vertex_five_regular_full_singleton_family_verified.json
SHA-256
  add0fb4e6cb8aca04a1a143e87a5383db28a86f9e276aa1ad1a3bbdd6490499a

enumerate_five_regular_full_singleton_family.py
SHA-256
  615c41f7fb19262c1bffb0c055ca5cbe51ba8d10e4a8641e457d80027d282c59

verify_five_regular_full_singleton_family.py
SHA-256
  a45705274d781a79e82f19595d3bfbe7846b51eefaadd1c27abed33d2d0b0b26
```

#### Closing the 84-entry equality boundary

The full-2-factor/singleton architecture is now forced at the entry-count
maximum in the 5-regular exact-20 branch.

Choose the three generic killer blocks at each of the eight vertices.  Let
`r,s,t` count skeleton edges chosen from two endpoints, one endpoint, and
neither endpoint.  The 24 directed choices and 20 skeleton edges give

```text
2r+s=24,       r+s+t=20.
```

A reciprocal selected block has at most one entry, a one-way selected block
at most three, and an unused block at most nine.  Hence

```text
E <= r+3s+9t = 36+4r <= 84.
```

Equality forces `(r,s,t)=(12,0,8)`, with twelve reciprocal singleton blocks
and eight full blocks.

More generally, the identical count for any even `n` and `m` nonzero
blocks gives

```text
E <= 9m-12n.
```

Equality forces `r=3n/2`, `s=0`, and `t=m-3n/2`.  Thus the equality
architecture below is an arbitrary-`n` three-colour structural lemma, even
though the current algebraic exclusion of that architecture is finite at
`n=8`.

There is a further exact support consequence.  At a vertex, write its
colour-`c` singleton as `(a,c)`.  If `a != c`, the failure-hyperplane theorem
requires another incident backup block whose `c`-column is independent of
`e_a`, while every nonzero non-`c` column is supported exactly on `e_a`.
A full equality block violates the second condition.  Either other
singleton has a column different from `c`, so it violates the first.
Thus no backup exists and `a=c`.  Every equality singleton is diagonal.

The singleton subgraph is therefore cubic and its three colour classes are
perfect matchings.  On a 5-regular skeleton the eight full blocks have
degree two at every vertex, so they form a spanning 2-factor.  The equality
support is one of the 7,938 labelled supports closed above.  Consequently:

**Finite theorem.**  A hypothetical witness in the 5-regular,
eight-vertex, three-colour, exact-20-edge branch has at most 83 supported
entries.

`verify_eight_vertex_entry84_boundary.py` exhausts the nine integer
incidence decompositions and all 27 local singleton-row assignments at
each possible full degree zero through four.  Only the diagonal assignment
survives.  Its pinned audit is
`tmp/eight_vertex_entry84_boundary_verified.json` (SHA-256
`60950aadbed74aaf97cb5ecff9ad0b49d8bf7133fc77db495f886d0041419eb4`).

This does **not** exclude supports with at most 83 entries, and it does not
make the eight full blocks a 2-factor on a non-5-regular exact-20 skeleton.
Those are the new precise structural boundaries.

There is also a useful cycle-factor interpretation of the equality family.
If the full-block 2-factor has `k` even cycle components, then every vertex
colouring has at least `2^k` active full-only perfect matchings.  Their
contribution factors as

```text
product over full cycles C of
  (alternating product A_C + alternating product B_C).
```

For `C4+C4`, this supplies four active monomials before any singleton edge
is used, so one- and two-term support obstructions are impossible
automatically.  The 160 relations in each eight-vertex factor-lattice
problem are the 80 nonconstant local colourings on each of the two full
`C4` components.  Exploratory samples at `n=10` and `n=12` show the same
baseline phenomenon for two or more even full cycles.  This is not an
arbitrary-`n` algebraic exclusion: it identifies why equality families with
multiple even full cycles remain the hard signed-factor boundary.

All 1,086 macro-family supports are now blocked in a resumed support search,
in addition to the two original exact cubes.  The next global analytic
target is to force either this architecture, a literal signed relation, or
a factorizable four-term parallelogram whose branch lattice has an isolated
class.

### Fallback-free upgrade of the six-vertex residual

The four old exact Singular charts are not genuinely higher-degree
obstructions.  Greedy deletion of their reduced saturation systems leaves
two non-saturation equations in every case.  A rational sum or difference
of the pair is one explicitly nonzero Laurent monomial.  For example, the
first core is

```text
-z10*z15*z9 + z11*z15*z5 - z11*z17*z4 = 0
 z10*z15*z9 + z11*z15*z5 - z11*z17*z4 = 0,
```

whose difference is `2*z10*z15*z9`.

After teaching the whole-pattern certifier to recognize rational
linear-monomial units, a fresh exhaustive run closes the same 18 pattern
orbits with:

```text
primitive Laurent-unit cubes       145
rational linear-monomial cubes       1
Singular fallbacks                    0
```

The one broader linear cube subsumes all four old fallback supports.
Glucose independently replays all 146 cubes and proves every pattern
support CNF UNSAT:

```text
tmp/global_pattern_orbits_unnormalized_linear_certified.json
SHA-256
  8faeef5759e71bc84b7c279bb5273b1c108e1bcfdb5f6a88132c1f127612d123

tmp/global_pattern_orbits_unnormalized_linear_verified_glucose.json
SHA-256
  b921677171b5948802305e5850fe7af1e5e0a14b4a561b5b399c5d925a67b106
```

The top-level six-vertex verifier now uses this fallback-free pattern
chain, checks that its orbit set is identical to the old one, and retains
the same final selector CNF and independently replayed DRAT proof.  This
strengthens and simplifies the finite theorem; it does not extend it to
arbitrary even `n`.

### Degree-four singleton theorem

The generic-killer argument sharpens substantially at a vertex of skeleton
degree exactly four.

**Proposition.**  Let `v` have four nonzero block neighbours in a
three-colour solution.  Then at least one incident block is a nonzero
monochromatic singleton

```text
W_vu = alpha e_c outer(e_c),   alpha != 0.
```

More precisely, choose the three distinct killer neighbours `k_c` and write

```text
W_(v,k_c) = a_c outer(e_c),    a_c != 0,
```

with the colour at `v` indexing the entries of `a_c`.  Let `x` be the sole
remaining neighbour and let `B=W_(v,x)`, with columns `b_1,b_2,b_3`.
Whenever `a_c` is not proportional to `e_c`,

```text
b_j is proportional to a_c for every j != c.            (4)
```

To prove (4), take a vector `z` in `ker(a_c^T)` with `z_c != 0`.
In the contraction identity, the `c`-killer has disappeared.  At each other
killer mode choose a kernel vector that kills that mode's own target colour
but retains colour `c`.  All zero-block modes are free.  If
`B^T z` were not a nonzero multiple of `e_c`, its kernel would also contain
a vector with nonzero `c` coordinate, leaving one nonzero target product and
giving a contradiction.  Hence

```text
B^T ker(a_c^T) subset span(e_c).
```

The points with `z_c != 0` are dense in that hyperplane precisely when
`a_c` is not proportional to `e_c`; linearity then gives (4).

Suppose all three `a_c` were non-coordinate.  If they are pairwise
nonparallel, (4) gives

```text
b_1 in span(a_2) intersect span(a_3) = 0
b_2 in span(a_1) intersect span(a_3) = 0
b_3 in span(a_1) intersect span(a_2) = 0,
```

so `B=0`, contradicting that it is the fourth skeleton edge.  If exactly
two vectors are parallel, say `a_1 || a_2` but `a_3` is independent, then
(4) gives `b_1=b_2=0` and `b_3 in span(a_1)`.  Every block incident with
`v` consequently has its `v`-side column space in
`span(a_1,a_3)`, of dimension two.  If all three vectors are parallel, the
same span has dimension one.  In either case the `v | rest` flattening of
the perfect-matching tensor has rank at most two, whereas the corresponding
flattening of `Delta_(n,3)` has rank three.  This is impossible.

Some `a_c` is therefore proportional to `e_c`, and its killer block is
exactly the claimed monochromatic singleton.

So a minimal counterexample, if it has a degree-four vertex, has a
structurally indispensable-looking diagonal singleton at that vertex.  In
particular, every 4-regular counterexample would have a spanning edge cover
formed by monochromatic singleton blocks.  This still falls short of
excluding degree four: the singleton need not be known to occur in a
nonzero monochromatic matching monomial, and cancellations through the
fourth edge remain possible.

### Degree-five local alternative

The local killer-flag theorem also gives a sharp normal form one degree
higher.

**Proposition.**  At a degree-five vertex, either one of the three primary
killer blocks is a monochromatic singleton, or one of the other two
incident blocks is an exact two-colour swap.  More explicitly, for two
different colours `c,d` and linearly independent primary vectors
`a_c,a_d`, that block has

```text
B[:,c] = lambda a_d,   B[:,d] = mu a_c,
B[:,e] = 0,
lambda,mu != 0,
```

where `e` is the third colour.

To see this, assume none of the primary killers
`K_c=a_c outer(e_c)` is a singleton.  Every colour then needs a distinct
failure-hyperplane backup.  Another primary `K_d` cannot back up colour
`c`: its column `c` is zero, whereas a backup's `c` column must lie outside
`span(a_c)`.  Thus all three backups use the two spare incident blocks, and
one spare `B` backs up two colours `c,d`.  The two backup conditions say

```text
B[:,d], B[:,e] in span(a_c),   B[:,c] not in span(a_c),
B[:,c], B[:,e] in span(a_d),   B[:,d] not in span(a_d).
```

Hence `a_c,a_d` are independent, the third column lies in the intersection
of their two distinct lines and is zero, and the other two columns have
the displayed nonzero swap form.  Moreover,

```text
e_c in span(a_c,a_d)  or  e_d in span(a_c,a_d).
```

Otherwise the local flag for colour `c` and the local flag for colour `d`
would both require a third edge after the shared backup `B`.  The primary
killers for the other colours have zero `c` or `d` column and cannot enlarge
the corresponding flag.  The only candidate is the other spare block `C`.
Serving as the third flag edge for `c` requires `C[:,d]` to lie in
`span(a_c,a_d)` and `C[:,c]` to lie outside it; serving for `d` requires the
opposite two containments.  These are incompatible.

The other spare also completes the flag for the third colour.  If the
shared primary plane contains both `e_c` and `e_d`, it is exactly their
coordinate plane, while the other spare is a rank-at-most-two backup whose
new third-colour column spans `e_e` together with `a_e`.  If the plane
contains `e_c` but not `e_d`, the other spare must simultaneously be the
third flag edge for `d` and the backup for `e`.  Its column `c` is then
zero, its column `d` is a nonzero multiple of `a_e` outside the shared
plane, its column `e` is a nonzero vector inside the shared plane, and that
last vector together with `a_e` spans `e_e`.  The case with `c,d` reversed
is symmetric.  Thus every nonsingleton degree-five neighbourhood falls
into two explicit local flag types.

This is not yet a degree-five exclusion.  It reduces every nonsingleton
degree-five neighbourhood to a rank-two, two-column bridge, which is a
more rigid target for the next global incidence or cancellation argument.

The coordinate-plane alternative has a nontrivial support shadow.  Each
condition

```text
e_c in span(a_c,a_d)
```

is a two-term determinant equation.  A vanishing determinant cannot have
exactly one structurally nonzero monomial.  Therefore, conditional on an
exact degree-five neighbourhood, no incident monochromatic singleton, and
one block backing up two primary colours `c,d`, the two determinants for
`e_c` and `e_d` cannot both be structurally unbalanced.

`eight_vertex_local_degree4_support.py --degree-five-plane` adds this
necessary condition as a clause-only extension.  The independent verifier
reconstructs all 483,840 clauses and proves that no old variable or clause
changed:

```text
python verify_degree_five_plane_extension.py \
  --base-cnf tmp/eight_vertex_normalized_killers_shared_backup_flag_max20.cnf \
  --extended-cnf tmp/eight_vertex_normalized_killers_shared_backup_degree5_plane_flag_max20.cnf \
  --extended-manifest tmp/eight_vertex_normalized_killers_shared_backup_degree5_plane_flag_max20.json \
  --output tmp/eight_vertex_normalized_killers_shared_backup_degree5_plane_flag_max20_audit.json

verified: true
clauses: 483840
extended SHA-256:
  85cf01aed3438604ccbca624e8b338da29e895dacd3536a6381b68ffabad6df3
```

This strengthening did not prune any of the first 64 transport-first
20-edge support models.  All 64 skeletons were 5-regular, and every one of
their 512 degree-five neighbourhoods already contained a monochromatic
singleton.  Thus those survivors take the other branch of the local
alternative.  Their singleton subgraphs cover all eight vertices and each
contains a mixed-colour singleton perfect matching, but the induced
forbidden colouring still has at least three active perfect matchings.
The next dense obstruction must therefore control cancellation around the
singleton branch rather than further refine the nonsingleton swap branch.

### Eight-vertex degree-four frontier

For a 4-regular graph on eight vertices, the complement is cubic but need
not be connected.  The official House of Graphs list and an initial
`nauty geng -cd3D3 8` run contain the five connected cubic classes.  The
complete repaired classification uses both

```text
nauty geng -d3D3 8      : six cubic classes
nauty geng -c -d4D4 8   : six 4-regular classes directly
```

The omitted complement is `K4 disjoint-union K4`, whose 4-regular
complement is `K4,4`.  Brute-force isomorphism gives bijections between the
six complements and the six directly generated regular graphs.

For every complement skeleton, `eight_vertex_degree4_support.py` encodes
only necessary conditions:

1. every skeleton block is nonzero;
2. every monochromatic amplitude has a nonzero matching monomial;
3. a forbidden amplitude cannot have exactly one nonzero matching monomial;
4. every `(vertex,colour)` has an eligible generic killer;
5. the degree-four singleton theorem holds at every vertex.

All six CNFs are UNSAT.  This includes `K4,4` and the catalogue class of
connectivity three, which was run directly rather than dismissed using the
published reduction.  Glucose 4.2 independently agrees on all six.  CaDiCaL 1.9.5
proofs were checked by `drat-trim`; the resolution-step counts are

```text
class 0: 2,907,449
class 1: 2,450,274
class 2: 2,175,560
class 3: 2,877,918
class 4: 2,414,474
class 5: 10,052,726
```

The fail-closed audit is

```text
python verify_eight_vertex_4regular.py
tmp/eight_vertex_4regular_final_audit.json: "verified": true
```

This proves that no eight-vertex complex witness has a 4-regular skeleton.
It does not exclude nonregular eight-vertex skeletons.

The stronger canonical encoding
`eight_vertex_local_degree4_support.py` fixes one degree-four vertex, its
guaranteed singleton, and its other two selected killers.  It also encodes
the diagonal anchors, the degree-three singleton-star theorem, and the
degree-four proportionality relation for every exact local neighbourhood.
With at most 15 nonzero skeleton blocks it has

```text
variables       394,797
clauses       2,849,737
```

(The precise generated header should be treated as authoritative if these
development counts change.)  MiniSat and CaDiCaL independently return
UNSAT for the materialized at-most-15 CNF.  CaDiCaL produced a
225,486,354-byte DRAT trace; independent `drat-trim` replay used 46,200,153
resolution steps and returned `s VERIFIED`.  The fail-closed audit is

```text
python verify_eight_vertex_degree4_frontier.py
tmp/eight_vertex_degree4_frontier_audit.json: "verified": true
```

At 16 edges the support relaxation is SAT.  Its first 34-entry torus
stratum is nevertheless impossible: after repairing a signed-`Counter`
cleanup bug that had dropped the three required `-1` constants, 59
binomial equations have rank 16 and three amplitude equations yield an
exact Laurent unit.  The resulting 48-literal conflict and its 12 canonical
symmetries were then combined with a complete nauty catalogue.

The catalogue contains 364 unlabeled connected matching-covered exact-16
skeletons with a degree-four vertex and 10,241 canonical singleton/killer
roles.  One selector CNF covers every role.  MiniSat and CaDiCaL return
UNSAT; independent `drat-trim` replay uses 211,119,420 resolution steps and
returns `s VERIFIED`.  The fail-closed audit,

```text
python verify_eight_vertex_16edge.py
tmp/eight_vertex_16edge_audit.json: "verified": true
```

reconstructs the Laurent conflict and role catalogue and line-checks the
selector compilation.  Thus no essential eight-vertex solution with a
degree-four vertex has at most 16 edges.

At exactly 17 edges, a complete nauty catalogue contains 420 unlabeled
connected matching-covered skeletons with a degree-four vertex and 11,051
canonical singleton/killer roles.  The exact Laurent CEGAR chain eliminates
all roles using 57 independently replayed algebraic conflicts and 666
learned support clauses.  The portable selector CNF has 439,322 variables
and 3,349,145 clauses.  CaDiCaL 1.9.5 returns UNSAT, and independent
`drat-trim` backward replay checks its 853,663,837-byte proof using
1,153,827,131 resolution steps and returns `s VERIFIED`.  The fail-closed
audit,

```text
python verify_eight_vertex_degree4_e17.py
tmp/eight_vertex_degree4_e17_final_audit.json: "verified": true
```

reconstructs the local algebraic-conflict chain, the skeleton and canonical
role coverage, the selector compilation, every artifact hash, and both
terminal proof decisions.  Thus no essential eight-vertex solution with a
degree-four vertex has at most 17 edges.  The exact certificate map is
`EIGHT_VERTEX_17EDGE_CERTIFICATE.md`; the 18-edge frontier remains open.

## Two-vertex contraction condition

Fix vertices `p,q` and local vectors `x,y`.  For each remaining vertex `r`,
put

```text
l_r = transpose(W_(p,r)) x
m_r = transpose(W_(q,r)) y
z_r = l_r cross m_r.
```

All edges from `p` or `q` to a remaining vertex vanish on `z_r`.  Therefore,
whenever the bilinear form `B_pq(x,y)` is zero,

```text
F_pq(x,y) = sum_c x_c y_c product_(r != p,q) z_(r,c) = 0.
```

If `B_pq` is irreducible (matrix rank at least two), it follows that the
polynomial `B_pq` divides `F_pq`.  For `(6,3)`, `F_pq` has bidegree `(5,5)`.

The generic-killer theorem shows that this divisibility condition is
actually vacuous for an exact witness.  If `B_pq` has rank at least two,
then `{p,q}` cannot be any selected rank-one killer edge at `p`.  For each
colour `c`, choose the selected `c`-killer neighbour `r != q`.  Its
covector `l_r` is proportional to `e_c`, so the `c` coordinate of
`z_r=l_r cross m_r` is identically zero.  Consequently the product in the
`c` summand of `F_pq` is zero for every colour, and `F_pq` is the zero
polynomial before divisibility is used.  When `B_pq` has rank at most one,
the irreducible-divisor premise fails.  Thus this scalar cross-product
test cannot strengthen the killer constraints at any order.

The implementation in `two_vertex_divisibility.py` verifies this condition
exactly by sparse polynomial division.  It also exposed a serious limitation:
all fifteen tests vanish identically on the triangular-prism boundary family.
The cross product is zero when the two defining covectors are dependent, so
it discards the larger simultaneous kernel.

`two_vertex_quotient.py` therefore retains the full quotient at every
remaining vertex:

```text
sum_c x_c y_c tensor_(r != p,q)
  [e_c in V_r^* / span(l_r,m_r)] = 0.                   (3)
```

This stronger numerical test is validated on the exact four-vertex,
three-colour witness.  However, the prism degeneration satisfies (3) as
well.  Conceptually this is unavoidable: the same local kernels annihilate
every perfect-matching channel, including the prism's extra maverick channel.
Thus annihilation identities that treat all matching channels uniformly do
not distinguish `GHZ` from `GHZ + maverick`.

## Killer-pattern zero certificates

Write a forced killer condition as a directed arc

```text
v --c--> u.
```

It means that an edge block on `{v,u}` can be nonzero only when the colour at
the *leaf* `u` is `c`.  This gives a purely combinatorial obstruction.

For each colour `c`, the nonzero monochromatic amplitude guarantees at least
one perfect matching `M_c` whose diagonal edge entries are all nonzero.  Once
one such matching is selected for each of the three colours, recombine their
known-nonzero edges into mixed perfect matchings.  If a resulting
non-monochromatic colouring has exactly one structurally allowed perfect
matching, its nonzero product has no cancellation partner.  The killer
pattern is impossible over any field.

`killer_pattern_certificates.py` implements this certificate.  It is a proof
for every pattern/triple it labels as `combinatorially_eliminated`; sampling
it is only a way to measure coverage.  In a deterministic 100,000-pattern
sample:

```text
82,849  had no structurally possible monochromatic matching triple
14,686  were eliminated by a unique mixed-matching certificate
 2,465  still required algebraic analysis
```

Thus the new certificate eliminated about 85.8% of the patterns that passed
the elementary monochromatic feasibility filter.  It also eliminated two of
the three best patterns found by the constrained numerical search.

The three selected monochromatic perfect matchings on six vertices have only
eight orbits under vertex and global-colour permutations.  Every orbit still
has some patterns not removed by the uniqueness certificate, so this is not
yet a complete proof.

## The normalized triangular-prism stratum

The hardest orbit contains three edge-disjoint perfect matchings whose union
is the triangular prism.  The observed boundary family lies in this orbit.
Independent half-edge scalings normalize the nine selected nonzero diagonal
entries to `1`.  The six unused edges, forming the complementary six-cycle,
remain unrestricted `3 x 3` blocks: only 54 variables.

With the nine prism entries fixed to `1`, the 726 forbidden equations have a
particularly rigid form:

```text
458 equations: two cubic monomials
189 equations: one quadratic plus two cubic monomials
 54 equations: one linear plus two cubic monomials
 24 equations: two quadratics plus two cubic monomials
  1 equation : 1 + three quadratics + two cubics
```

Each of the 54 variables occurs as the unique linear term of exactly one
equation.  Their Jacobian at the zero six-cycle point is therefore a
permutation matrix.  `solve_prism_core.py` uses these equations as a square
Newton system.  Across 500 starts it found many nonzero roots of that square
core, but none satisfied the remaining forbidden equations; the best full
maximum residual was still `1`.

`search_prism_stratum.py` directly minimizes all forbidden amplitudes in the
generalized-GHZ formulation.  Twenty-four larger random restarts converged
to the same symmetric finite stationary point with maximum forbidden
amplitude about `0.653456`, not to zero.

`generate_prism_singular.py` emits the exact integer ideal for Singular.
An exact Gröbner computation is the current route to either a unit-ideal
certificate for this stratum or an exact component that the numerical
searches missed.

### The 54-equation core is six rank-one matrix identities

The apparent 54-variable core has much more structure.  Write the six
unrestricted complement blocks as

```text
X04, X05, X12, X13, X25, X34.
```

Its nine equations for `X04`, for example, are exactly the entries of

```text
(1 + X13[2,0] X25[0,2]) X04
  + X12[2,0] outer(X05[:,2], X34[0,:]) = 0.
```

The other five blocks satisfy cyclically analogous identities.
`prism_matrix_core.py` states all six and verifies them entry-by-entry
against the matching amplitudes.  Therefore, on every core solution,

```text
lambda_e != 0  ==>  rank(X_e) <= 1,
```

where each `lambda_e` is `1` plus an explicit quadratic monomial.  Equivalently,
`lambda_e^2` times every `2 x 2` minor of `X_e` vanishes on the core.

This explains why the unsplit Gröbner calculation grew to 4.6 GB: it was
implicitly resolving as many as `2^6` branches according to which
`lambda_e` vanish.  That run was stopped after an hour without a result.
The exact computation is now branch-aware: the generic branch includes the
54 rank-one minors explicitly, while the exceptional branches set selected
`lambda_e` to zero.  The normalized fixed tensor has 12 vertex/colour
automorphisms, acting transitively on the six complement edges, so all six
exceptional branches are isomorphic.

The representative exceptional branch is now exactly eliminated.  Setting
`lambda_04=0` makes its matrix identity

```text
X12[2,0] outer(X05[:,2], X34[0,:]) = 0,
```

so every solution lies in one of three subcases: the scalar is zero, the
column is zero, or the row is zero.  For each subcase, the ideal generated
by all forbidden amplitudes plus these branch equations has rational
Gröbner basis `[1]` (the scalar case took 51 seconds; the vector cases took
under 10 seconds).  Transitivity eliminates every `lambda_e=0` branch over
`C`.

The generic branch is also exactly empty.  Adding the 54 rank-one minors to
all 726 nonzero forbidden-amplitude equations gives a 780-generator ideal.
Over `Q`, Singular's rational `slimgb` computes a one-element Gröbner basis
and reduces `1` to `0` in 124 seconds.  Thus this ideal is the unit ideal.
Together with the exceptional branches, this proves:

> The normalized fully mutual triangular-prism stratum has no finite complex
> solution.

In particular, the familiar six entries of size `t`, three entries of size
`t^-2`, and residual `t^-6` describe a point at infinity of this stratum,
not a finite counterexample.

This scope matters.  The cubic prism has 718 half-edge-label orbits that
survive the elementary and support filters.  The calculation above treats
the canonical orbit in which the nine mutual singleton edges are the three
selected monochromatic perfect matchings.  It does not eliminate the other
717 orbits, whose required monochromatic matchings may use unrestricted
complement edges.

### Extension to the other prism labelings

At each vertex, the three prism edges can receive the three killer colours
in any order, giving `(3!)^6 = 46,656` half-edge labelings.  They reduce to
718 orbits under the 12 prism automorphisms and 6 global colour
permutations.  Every orbit passes the elementary and zero/nonzero support
filters.

For each orbit, the nine mutual killer blocks are singleton matrices.  Their
nonzero entries can again be normalized independently to `1`, while the six
complement blocks remain unrestricted.  `prism_orbit_screen.py` constructs
the resulting exact 54-variable forbidden-amplitude ideal.

An exact symbolic audit reveals that 571 of the 718 orbits retain a
generalized version of the six-matrix core.  Every free variable is the
unique linear term of one forbidden equation, and for each free block
`X_e` the corresponding nine equations assemble as

```text
lambda_e X_e + Y_e = 0,
```

where all formal `2 x 2` polynomial minors of `Y_e` vanish identically.
Consequently

```text
lambda_e != 0  ==>  rank(X_e) <= 1
```

for all six blocks in all 571 orbits.  The audit checks the polynomial
identities coefficient-by-coefficient; it is not a numerical rank test.
The remaining 147 orbits have only 51, 52, or 53 distinct linear variables,
so this particular argument does not cover every complement entry.  Across
all 718 orbits there are only 26 coarse equation-shape signatures, although
equal shape counts do not prove algebraic equivalence.

The exceptional branches also have a uniform exact shape.  Up to the
stabilizer of each half-edge pattern, there are 3,142 representative
`lambda_e=0` matrices among the 571 reduced orbits.  Every one has monomial
entries and exactly three minimal variable covers: a scalar factor, a
three-entry column, or a three-entry row.  Hence exhausting all reduced
orbits is a finite list of

```text
  571 generic rank-one ideals
9,426 exceptional cover ideals
-----
9,997 exact rational jobs.
```

This count is generated from the patterns and polynomial matrices, not
estimated.

One noncanonical orbit is now completely excluded.  In canonical ordering it
has half-edge neighbour rows

```text
[1,2,3] [0,4,5] [0,3,4] [0,2,5] [1,2,5] [1,3,4].
```

Its generic ideal consists of all 726 forbidden equations plus the 54
rank-one minors.  Singular computes the rational Gröbner basis `[1]` in 86
seconds.  The pattern stabilizer has four orbits on complement edges.  For a
representative of each, the rank-one remainder factors as a scalar times a
three-entry column times a three-entry row.  Thus `lambda_e=0` splits into
three subcases.  All twelve rational branch ideals have Gröbner basis `[1]`
(the slowest took 17 seconds).  This exhausts both the generic and
exceptional branches, proving:

> The normalized prism half-edge orbit 0 has no finite complex solution.

The exact batch has now closed 26 of the 718 fully mutual prism orbits.  It
contains:

- all 4 orbits of symmetry size 6;
- all 4 orbits of symmetry size 12;
- all 6 orbits of symmetry size 18;
- the unique orbit of symmetry size 24;
- 11 orbits of symmetry size 36.

For these 26 orbits, all generic and symmetry-reduced exceptional branches
have been exhausted: 200 rational Singular jobs, each with Gröbner basis
`[1]`.  `verify_prism_certificates.py` reads the generated manifests, checks
that every input ring has characteristic zero, verifies the exact unit-ideal
markers in all 200 logs, and checks the closed-orbit set.  The certified
indices are

```text
0, 7, 36, 41, 47, 50, 54, 55, 62, 92, 109, 146, 168, 170,
268, 295, 300, 326, 408, 420, 503, 508, 587, 686, 703, 717.
```

Thus 692 prism orbits remain.  Of these, 545 retain the six-block generic
rank-one reduction but have not had every branch certified; the other 147
need a different core argument.

### Authoritative signed completion of all 718 prism orbits

The preceding 26-orbit Singular batch was an intermediate checkpoint.  A
later partial-core construction covers every orbit, including the 147 that
do not retain all six rank-one blocks.  The exact distribution is:

```text
orbits   linear pivots   rank-one blocks   binomial rank   parameters
 571          54               6                13             36
 130          53               5                17             39
  16          52               4                21             42
   1          51               3                25             45
```

For every orbit, the generic branch forces all 54 complement-block entries
to be nonzero.  The retained rank-one blocks give an outer-product
parameterization, and the remaining two-term amplitudes contain a
unimodular Laurent-binomial basis.  Exact signed substitution produces
between 240 and 243 constant nonzero equations per orbit.  Hence all 718
generic branches are empty on the complex torus.

There are six exceptional `lambda_e=0` branches per orbit.  Direct exact
support encodings are UNSAT for all

```text
718 * 6 = 4,308
```

branches.  Therefore:

> Every normalized triangular-prism killer labeling is impossible over
> `C`; all 718 half-edge-label orbits are excluded.

`verify_all_prism_orbits.py` reconstructs the 718 patterns, the partial
linear cores, the generic support formulas, the signed Laurent reductions,
and all 4,308 exceptional support formulas.  The authoritative manifest is
`tmp/all_prism_orbits_verification_signed.json`; it has no failures.

This rerun follows a signed-coefficient audit.  Python's unary `+Counter`
drops nonpositive counts and therefore cannot be used to remove only zero
coefficients from a polynomial.  Every algebraic path now calls
`clean_polynomial`, which preserves negative coefficients.  Unsuffixed
manifests made by the affected Laurent pipeline are superseded by their
`*_signed.json` reruns.  A dedicated unit test now guards this failure mode.

## Exact result: the fully mutual K3,3 stratum is empty

The other edge-disjoint matching orbit has union `K3,3`; its six unused
edges form two disjoint triangles.  Under the same *fully mutual* assumption
as above, the nine selected matching blocks again normalize to single
diagonal entries equal to `1`, leaving 54 variables.  Of the 726 forbidden
colourings, 570 give nonzero equations:

- 423 are single quadratic monomials;
- 144 are sums of two quadratic monomials;
- 3 are `1` plus three quadratic monomials.

Over the rational numbers, both Singular's `slimgb` and its independent
`std` implementation compute the reduced Gröbner basis `[1]` for this
570-generator ideal.  Thus the ideal is the unit ideal and this normalized
stratum has no solution over any extension of `Q`, in particular none over
`C`.

In fact the CAS result collapses to an elementary 11-equation certificate.
Order the six unused edges as

```
(03), (04), (12), (15), (25), (34)
```

and write `x_(9k+3a+b)` for entry `(a,b)` of unused edge block `k`.
Two forbidden colourings give

```
1 + x43*x50 + x1*x28  + x11*x20 = 0,   (A)
1 + x33*x51 + x5*x25  + x12*x39 = 0.   (B)
```

Call the three quadratic terms in the first row `A0,A1,A2`, and those in
the second row `B0,B1,B2`.  Nine other forbidden colourings each have a
unique surviving matching and therefore give the following monomial-zero
table:

```
             B0          B1          B2
A0       x43*x51     x43*x5      x12*x43
A1       x1*x33      x1*x25      x1*x39
A2       x11*x33     x11*x25     x11*x39
```

Equation `(A)` forces at least one `Ai` to be nonzero, and `(B)` forces at
least one `Bj` to be nonzero.  If `Ai` and `Bj` are both nonzero, all four
of their factors are nonzero.  But the corresponding table entry is a
product of one factor from `Ai` and one from `Bj`, and is required to be
zero: a contradiction.  This proof works over every field and uses only
support, not the values of the weights.  `k33_support_analysis.py`
reconstructs all equations from the matching model and verifies the table.

This elementary exclusion has a deliberately narrow scope.  It assumes that every
one of the nine edges in the three selected monochromatic perfect matchings
is a mutual killer edge carrying only its selected diagonal entry.  It does
not by itself eliminate other `K3,3` half-edge labelings or the
triangular-prism orbit; the exhaustive extension below removes the former.

### Extension: every cubic K3,3 killer labeling is impossible

The elementary certificate above is only one labeling, but the whole cubic
`K3,3` killer graph is finite.  At every vertex, its three incident edges
receive the three killer colours in some order.  There are therefore

```text
(3!)^6 = 46,656
```

half-edge labelings.  `enumerate_cubic_rankone.py` exhausts them.  The
elementary filters give:

```text
20,724  have no structurally possible monochromatic matching triple
10,872  have a unique nonzero forbidden matching certificate
15,060  need the stronger support test
```

The 15,060 survivors collapse to 48 orbits under the 72 automorphisms of
`K3,3` and the 6 global colour permutations.  `rankone_support_sat.py`
introduces a Boolean for every structurally allowed edge entry, meaning
"this complex weight is nonzero."  It then uses only necessary facts:

1. a matching monomial is nonzero exactly when all three factors are;
2. a nonzero monochromatic amplitude has at least one nonzero monomial;
3. a zero forbidden amplitude cannot have exactly one nonzero monomial.

All 48 orbit CNFs are UNSAT.  MiniSat and CaDiCaL independently return
UNSAT; CaDiCaL's internal proof checking was enabled, and explicit DRAT
traces were also generated.  Thus the following computer-assisted lemma is
exact over every field:

> A six-vertex, three-colour witness cannot admit a choice of one killer
> neighbour for every `(vertex, colour)` pair whose nine undirected edges
> form `K3,3`.

This removes *all* half-edge labelings and leaves the triangular prism as
the only nine-edge (fully mutual cubic) killer graph.

## Global support classification of killer-edge unions

`global_support_sat.py` simultaneously encodes the 135 unknown entry
supports and the 18 unknown killer-neighbour choices.  Besides the amplitude
support rules above, it enforces:

- exactly one chosen killer neighbour for each `(vertex, colour)`;
- three distinct chosen neighbours at every vertex;
- the selected block is nonzero and has only the required leaf-colour
  row or column.

If the 18 arcs use `m` undirected edges, then `9 <= m <= 15`.  The support
CNF is UNSAT for `m=15`, for the unique `m=14` missing-edge orbit, and for
both `m=13` missing-edge orbits.  A support model exists for `m=12`, so the
sharp support-level bound is

```text
9 <= m <= 12.
```

Because the selected union has minimum degree three, its complement has
maximum degree two.  For `m=9,10,11,12`, there are only fifteen complement
graphs up to isomorphism.  `classify_killer_union_support.py` checks one
exact CNF for each.  The support-feasible complements are:

```text
m=12: C3, P4
m=11: C4, P5, 2 P3
m=10: C4 + K2
m= 9: C6
```

The other eight types are support-impossible:

```text
m=12: P3 + K2, 3 K2
m=11: C3 + K2, P4 + K2
m=10: C5, C3 + P3, P6
m= 9: 2 C3
```

Here the last line is the cubic `K3,3` killer graph; the feasible `C6`
complement is the cubic triangular prism.  This classification is a
necessary-support theorem, not an existence result for the seven surviving
types: SAT means only that zero/nonzero cancellation is not ruled out.

### Exact signed completion of the ten-edge case

For `m=10`, the only support-feasible complement is `C4 + K2`.
`enumerate_killer_union_orbits.py` reduces 746,496 valid half-edge patterns
on this skeleton to 7,932 orbits.  For each orbit,
`certify_union_orbit_supports.py` projects the exact support CNF by CEGAR.
Every projected support chart contains a signed Laurent unit contradiction.
The complete census is:

```text
orbits certified                 7,932 / 7,932
signed Laurent conflict cubes         25,233
cubes per orbit                    1 through 23
failures                                    0
```

The authoritative manifest is
`tmp/m10_all_orbits_verification_signed.json`.  Together with the all-prism
and all-`K3,3` results, this excludes every feasible killer selection using
9 or 10 undirected edges.

### Superseded checkpoint: eleven and twelve edges

`candidate_killer_cover_sat.py` derives every eligible killer arc directly
from the entry support.  The global CEGAR in
`global_candidate_laurent_cegar.py` starts from supports having no eligible
cover on at most ten edges.  For each model it chooses a minimum 11- or
12-edge selection, normalizes the resulting stratum, and learns a clause
from either a signed Laurent unit or an exact rational torus saturation.

There is a useful exact reformulation of the minimum-cover step.  Make a
graph on the 18 `(vertex, colour)` tasks, joining two tasks when their two
oppositely directed candidate arcs can use the same undirected edge.  A
selection of all 18 arcs can share an edge only in such a pair.  Therefore,
if `nu` is the maximum matching size of this compatibility graph, then

```text
minimum killer-edge cover size = 18 - nu.
```

In particular, the structural 12-edge conjecture is equivalent to forcing a
matching of size at least 6.  The CEGAR now computes this matching directly;
its result was cross-checked against exhaustive edge-subset minimization on
independent SAT models.

Tutte-Berge gives a finite dual attack on this matching statement.  If the
maximum matching has size at most 5, there is a separator `S`, with
`s=|S|` in `0..5`, for which at least `s+8` odd components remain.  It is
enough to encode `s+8` pairwise isolated odd vertex groups.  Their possible
sorted size patterns number:

```text
s                     0   1   2   3   4   5
odd-size patterns     19  12   7   4   2   1
```

The `s=5` pattern consists of thirteen singletons, so it says exactly that
the compatibility graph has a five-task vertex cover.  A five-task separator
is a `6 x 3` binary matrix with five marked entries.  There are 18 such
matrices modulo all vertex and global-colour permutations.
`verify_candidate_separator_orbits.py` fixes each representative and asks
the global support CNF whether every compatibility edge can meet it.  All 18
CNFs are UNSAT under both CaDiCaL 1.9.5 and MapleChrono.  The independent
manifests are:

```text
tmp/candidate_separator_s5_cadical.json
tmp/candidate_separator_s5_maple.json
```

Thus the `s=5` Tutte obstruction is excluded at support level.  The other 44
fixed odd-size cases for `s=0..4` remain; closing only `s=5` does not yet
prove the global 12-edge bound.

The signed 5,000-stratum checkpoint contains:

```text
minimum cover size 11                3,307
minimum cover size 12                1,693
direct signed Laurent contradictions 4,920
exact Q torus-saturation contradictions 80
algebraic survivors                       0
```

`verify_global_candidate_cegar.py` independently reconstructs every
support-local equation set, rederives each Laurent unit and required
killer-arc cube, regenerates every fallback Singular input, and checks its
exact characteristic-zero `[1]` log.  All 5,000 rows in
`tmp/global_candidate_cegar_signed_5000.json` verify.  The manifest status is
still `limit`, not `certified`: the remaining global SAT space has not yet
been exhausted, so the `m=11`, `m=12`, and arbitrary-`n` problem remain open.

The 5,000 labeled rows contain only 18 killer-pattern orbits under all vertex
and global-colour permutations: 8 have 11-edge unions and 10 have 12-edge
unions.  Exhausting *all* support charts for each fixed pattern gives:

```text
17 pattern orbits: exact support/Laurent exhaustion
 1 pattern orbit:  13 Laurent cubes, then one full-nonzero torus chart
```

For the last chart, 62 binomials of rank 27 reduce the 45 variables to 43
equations in 15 active Laurent variables.  Rational Singular saturation
returns `[1]`.  Thus all 18 exposed whole-pattern orbits are impossible,
independently of any extra eligible killer arcs.  The authoritative manifest
and fallback logs are:

```text
tmp/global_pattern_orbits_from_5000_certified.json
tmp/global_pattern_orbits_from_5000_fallback/
```

Their 40,680 symmetry-distinct whole-pattern blocking clauses were added to
the global residual.  The first fallback-based whole-pattern manifest was
not exhaustive and is superseded by the repaired unnormalized manifest
described below.

### Repaired completion of the six-vertex case

Every normalization was audited as a torus action on the 18 vertex-colour
half-edge gauges.  A set of mutual singleton weights is normalized only
when its unsigned incidence matrix has full row rank.  The corrected exact
partition is:

```text
triangular prism: 652 normalized + 66 unnormalized = 718
ten-edge case:   7605 normalized + 327 unnormalized = 7932
```

The 18 exposed eleven/twelve-edge patterns were conservatively rerun with
no mutual singleton normalized.  The original chain used 146 Laurent cubes
and four exact rational torus saturations.  The later fallback-free upgrade
replaces those four charts by one broader rational linear-monomial cube:
145 primitive units plus one linear unit, with Glucose independently
replaying all 146 cubes.  Both chains prove the same pattern support CNFs
UNSAT; the top-level audit now uses the simpler one.

The final residual starts from every support whose minimum killer cover is
larger than ten, adds all 40,680 symmetry images of those 18 now-valid
whole-pattern blockers, and adds seven sound lexicographic symmetry
comparisons.  Its 339,096-clause DIMACS has SHA-256

```text
154b1a64a70b10eef5bd7cb3ddb929033d408b65f26ff2704eacc610030154c7
```

CaDiCaL 1.9.5, Glucose 4.2, and MapleChrono all return UNSAT.  Together
with the repaired 9- and 10-edge partitions, this proves the six-vertex
three-colour exclusion over `C`.  See `SIX_VERTEX_CERTIFICATE.md` for the
authoritative chain and exact artifacts.  This finite result does not imply
the conjecture for `n>=8`.

As an exploratory check, a numerical solve inside a support-feasible
`m=12`, missing-`C3` mask again ran to infinity.  After 2,600 polishing
steps its largest forbidden amplitude was about `5.7e-5`, while the norm
grew to `12.5`.  The only asymptotically significant entries were precisely
six triangle entries scaling as `t` and three rungs scaling as `t^-2`:
the same triangular-prism boundary family in a different labeling.  The
optimizer did not enforce a positive lower bound on every selected killer
block, so this is evidence about the closure, not an exclusion of the
`m=12` stratum.

## Certified ten-vertex `C4+C6` equality support

The entry-count equality architecture extends naturally to `n=10`: three
diagonal singleton perfect matchings contribute 15 entries and a full-block
2-factor contributes 90, for 105 entries on a 5-regular 25-edge skeleton.
The first deterministic example uses a `C4+C6` full factor.

There are 68 skeleton perfect matchings and four full-only matchings.
Enumerating all `3^10=59,049` colourings gives 34,001 exact four-term
full-only amplitudes.  Each factors into a two-way choice between the signed
alternating-product relations on the two even cycles.  There are 656
distinct relation variables.

The initial exact-lattice CEGAR run required 208 blocking branches.  Greedy
semantic minimization reduced the same proof to eleven no-goods: six unary
cores and five three-relation cores.  Inspecting the final monotone CNF then
found a still smaller core: one factor clause and two of the unary no-goods.
This is a direct three-amplitude proof.  A four-full-matching amplitude
forces either the alternating `C4` relation or the alternating `C6`
relation.  A seven-term amplitude cancels in three pairs under the first
relation and leaves one nonzero monomial; a five-term amplitude cancels in
two pairs under the second and likewise leaves one nonzero monomial.

An independent verifier rebuilt the support, activities, relations,
clauses, and quotient contradictions using separate exact arithmetic.  The
redundant exhaustive 656-variable, 34,012-clause CNF has
SHA-256

```text
3540268a767a04d3f42413f9150dd190bcb22da470d2bf3f2dbe557d2adb2e42
```

Kissat returned UNSAT and emitted a 2,275-byte binary DRAT trace with
SHA-256

```text
5cf109f5c4d5b7784bbc30e627df683ab07f7483deda4b7f79228a1a0f6e0ea2
```

Independent `drat-trim` replay returned `s VERIFIED`.  This proves that one
explicit 105-entry support is empty over `C`; it is not an exhaustive
ten-vertex theorem.  The authoritative description is
`TEN_VERTEX_C4_C6_SUPPORT_CERTIFICATE.md`.

### Exhaustive `C4+C6` equality family

The three-amplitude fork generalizes across the entire ten-vertex
`C4+C6` equality architecture.  Fixing a labelled factor leaves 292
eligible singleton perfect matchings and 446,592 unordered pairwise
edge-disjoint triples.  Quotienting by the factor's 96 automorphisms and
global colour permutation gives 4,903 support orbits.  Every orbit has a
fork, with at least 17,954 valid fork base colourings.

An independent verifier recounts the raw factorizations, validates every
canonical representative and orbit size, checks total orbit coverage, and
replays one exact three-amplitude contradiction per orbit.  Across every
labelled `C4+C6` factor and colour assignment this excludes
101,287,065,600 labelled coloured supports.

This is an exhaustive theorem for the `C4+C6` equality family, not all
ten-vertex equality supports.  `C10`, `C3+C7`, `C5+C5`, and `C3+C3+C4`
full factors remain separate cases, as do supports below the equality-entry
boundary.
See `TEN_VERTEX_C4_C6_FAMILY_CERTIFICATE.md`.

### Odd-component equality factors

The `C3+C7`, `C5+C5`, and `C3+C3+C4` families are simpler.  Exhaustive
catalogues have 458,094, 460,690, and 458,352 raw colour-unlabelled
factorizations, reducing to 5,558, 2,536, and 906 support orbits.  Every
orbit exposes a forbidden one-term amplitude: the unique active matching
is a product of five supported nonzero entries and therefore cannot vanish.
Independent verifiers reconstruct all three orbit catalogues and replay
every activity certificate.

The minimum number of one-term forbidden colourings in any orbit is 20,102
for `C3+C7`, 14,325 for `C5+C5`, and 3,204 for `C3+C3+C4`.  Across labelled
factors and colour assignments the three results exclude 186,216,226,560
supports.  See
`TEN_VERTEX_ODD_FACTOR_EQUALITY_CERTIFICATE.md`.

### The `C10` transport family and complete equality boundary

The remaining `C10` equality family has 451,751 raw colour-unlabelled
factorizations and 23,204 cycle-symmetry orbits.  Every orbit exposes three
binomial forbidden amplitudes on one matching pair and a trinomial target.
The exact Laurent identity `r_target=r1-r2+r3` transports the three signs
`(-1,-1,-1)` to `x^r_target=-1`; the target pair cancels and its third
supported nonzero monomial survives.  The hardened verifier reconstructs
all perfect-matching masks, colourings, activities, and exponent identities.
Across labelled ten-cycles and colour assignments this excludes
491,794,208,640 supports.  See
`TEN_VERTEX_C10_EQUALITY_CERTIFICATE.md`.

There are exactly five cycle partitions of ten with every part at least
three: `C10`, `C4+C6`, `C5+C5`, `C3+C7`, and `C3+C3+C4`.  They are now all
closed.  The general entry bound specializes to 105 at `(n,m)=(10,25)`,
and equality uniquely forces fifteen diagonal singleton blocks forming
three perfect matchings plus ten full blocks forming a spanning 2-factor
on a 5-regular skeleton.  The five family audits therefore exclude the
entire 105-entry boundary: 37,107 support orbits representing
779,297,500,800 labelled coloured supports.  The branch below 105 entries,
non-5-regular exact-25 supports, and the global conjecture remain open.  See
`TEN_VERTEX_FIVE_REGULAR_EQUALITY_BOUNDARY.md`.

### Arbitrary-order all-odd equality factors

The one-term obstruction extends analytically whenever every component of
the full 2-factor is odd.  Let `M` minimize the number of singleton edges
among skeleton perfect matchings and let `T` be its singleton part.  Any
matching `T` can be activated exactly: precolour its endpoints by their
singleton labels, then properly 2-colour the remaining induced
`S1 union S2` paths and cycles with colours 1 and 2.

If `|T|<n/2`, every odd full cycle is cut by `T`.  The remaining full graph
is a union of even paths with unique perfect matchings.  A second matching
in `F union T` would either omit a singleton edge, contradicting
minimality, or use all of `T` and coincide on every path.

If the minimum is `n/2`, the cubic singleton graph supplies a mixed-colour
perfect matching.  In the connected case it is bridgeless, and the
Král--Sereni--Stiebitz lower bound gives at least `n/2 >= 4` perfect
matchings; in the disconnected case different colour matchings can be
chosen on different components.  Activating that mixed matching again
leaves one nonzero monomial.  This proves every all-odd full-factor
equality support impossible for arbitrary even `n>=8`.  See
`ODD_FULL_FACTOR_ONE_TERM_THEOREM.md`.

The same proof does not extend unchanged to mixed odd/even factors.  A
two-edge-switch search reached an explicit `C3+C4+C7` equality support at
order 14 whose feasible-singleton-set poset has 242 members but only nine
inclusion-minimal members.  All nine are single edges joining the odd
components and miss the `C4`.  The independent audit constructs an
alternative for every one of the 267 skeleton perfect matchings: 249 have
a proper feasible singleton subset, and the remaining 18 flip the untouched
even cycle.  Hence this support has no one-term forbidden amplitude.

This is not a complex witness.  The next algebraic layer closes the explicit
support with only two amplitudes.  Forbidden equation 118 is binomial; its
four-entry Laurent relation agrees up to orientation with the ratio between
matchings 30 and 40 in forbidden trinomial equation 112.  The binomial
forces those two target terms to cancel, leaving matching 32 as one nonzero
survivor.  An independent verifier rebuilds both equation colourings,
activities, and exponent vectors exactly.  This result is support-specific,
not a theorem for all `C3+C4+C7` factorizations.  See
`FOURTEEN_VERTEX_NO_ONE_TERM_SUPPORT.md`.

### Matching-fork transport without a colour-cube scan

The order-14 direct motifs admit a stronger arbitrary-order formulation.
Let the full blocks form a 2-factor `F` and the diagonal singleton blocks
form three colour-labelled perfect matchings `S0,S1,S2`.  Suppose `U` is a
matching of singleton edges and `f=xz` is in `U`.  If

```text
PM(F union (U-{f})) = A != empty,
PM(F union U)       = A union {Q},
```

and every member of `A` pairs `x` to one common full-edge neighbour `y`,
then the support is impossible, provided the constructed rich colouring is
nonmonochromatic.

The key point is that the two required colourings always exist.  If `f`
has colour `c`, precolour the endpoints of `U-{f}` by their edge labels,
precolour `z` by `c`, and properly 2-colour every remaining vertex along
the union of the other two singleton factors.  This activates exactly
`U-{f}`.  Changing only `x` to `c` activates exactly `U`.  The old
monomials all change by the same nonzero entry ratio on `xy`; their first
forbidden equation therefore transports to the second, leaving the new
monomial `Q` nonzero.

`certify_fourteen_vertex_matching_fork.py` searches only the skeleton
perfect matchings and constructs the adjacent colourings.  An independent
bitmask matching enumerator in
`verify_fourteen_vertex_cancellation_transport.py` replays the result.  It
finds verified two-to-three forks in all four adversarial supports tested:

```text
support                                           skeleton perfect matchings
no-canonical-three-extension candidate                                  248
100,000-prefix direct-free candidate                                     254
200,000-prefix direct-free candidate                                     260
500,000-prefix best candidate                                            236
```

The completed 500,000-prefix search had reduced the broader direct-Laurent
score to two relation signatures, but the matching fork survives.

The full `C3+C4+C7` equality family is now exhausted.  There are 44,226
eligible singleton colour factors.  Exact 128-subset tables leave 9,114
individually safe factors: 8,694 send all triangle vertices to the
7-cycle, while 420 exceptional factors form four full-factor automorphism
orbits.  A catalogue of 168 two-edge one-term sets leaves respectively
108, 100, 104, and 116 compatible safe second factors for those exceptional
orbits, and zero compatible thirds.

For the 8,694 remaining factors, an exact catalogue of 4,368 matching-fork
triples leaves 3,654 fork-free factors in 18 orbits.  Only 36 second-factor
choices survive the simultaneous one-term/fork compatibility tests, and
again zero third factors survive.  The independent verifier uses a separate
bitmask matching recursion, reconstructs both catalogues, expands all 22
orbits, and returns `"verified": true`.  This proves the complete finite
family theorem, not the other order-14 factor types or the global
conjecture.  See `MATCHING_FORK_TRANSPORT_LEMMA.md` and
`FOURTEEN_VERTEX_C3_C4_C7_FAMILY_CERTIFICATE.md`.

### Full `C3+C5+C6` equality family

The next mixed factor type is now exhausted as well.  Fixing the labelled
`C3+C5+C6` full factor leaves 44,220 eligible singleton perfect matchings.
Exact 128-subset completion tables leave 2,820 individually one-term-free
factors.  The obstruction catalogue contains 270 two-edge one-term sets
and respectively 5,310, 73,350, and 160,920 matching forks of sizes three,
four, and five.

After the one-term and size-three tests, 1,020 factors in five full-factor
orbits remain.  There are 960 compatible seconds and 47,936 compatible
ordered thirds before the larger forks.  The size-four and size-five
catalogues leave 156 ordered supports, 78 after forgetting the order of
the singleton colours, and nine orbits under the 720 full-factor
automorphisms and colour permutation.

These nine supports expose a genuinely stronger boundary: a full `3^14`
activity scan on the first representative finds no adjacent one-vertex
cancellation transport of any set size.  Nevertheless, its 458 distinct
binomial relations generate an exact signed lattice of rank 37.  Three
basis relations with coordinates `(+1,+1,-1)` force a pair in a forbidden
trinomial to cancel, leaving the third supported monomial.  The same
rank-37, three-relation mechanism closes all nine orbits.

`verify_fourteen_vertex_c3_c5_c6_family.py` independently regenerates all
239,580 fork masks using a vertex-subset pairing enumeration, reconstructs
the `47,936 -> 156 -> 9` coverage, and checks the nine independent
algebraic replays and their hash chain.  Its final audit is
`tmp/fourteen_vertex_c3_c5_c6_family_verified.json` and contains
`"verified": true`.  This proves the complete finite `C3+C5+C6` family,
not the other order-14 factor types or the global conjecture.  See
`FOURTEEN_VERTEX_C3_C5_C6_FAMILY_CERTIFICATE.md`.

### Single `4k+2` cycle rectangle theorem

The all-even `C14` census initially looks hostile to elementary support
obstructions: all 44,189 eligible singleton factors are individually
one-term-free, and there are zero two-edge one-term sets and zero
size-three matching forks.  A sparse transport probe nevertheless exposed
the same three-binomial `(+1,-1,+1)` identity as the certified `C10`
family, and it has a direct arbitrary-order explanation.

For a single full cycle `C_(4k+2)`, both bipartition classes have odd
cardinality.  Every singleton perfect matching therefore contains a
non-cycle chord `f=xz` crossing the bipartition.  Properly 2-colour the
union of the other two singleton factors.  Changing neither, one, or both
of `x,z` to the colour of `f` gives a four-corner colouring rectangle.
The first three corners activate no singleton edge and hence have only the
two alternating full-cycle matchings.  The fourth activates exactly `f`
and has those two matchings plus the unique matching through `f`.

Because `x,z` are nonadjacent on the full cycle, the alternating exponent
vector has zero mixed discrete derivative:

```text
r_11 = r_10 + r_01 - r_00.
```

The three binomial relations all have value `-1`, so the odd signed
combination forces the alternating pair to cancel at the target, leaving
the chord matching nonzero.  This excludes every single-cycle equality
factor of length `2 mod 4`, including the complete order-14 `C14` family.

`verify_fourteen_vertex_c14_rectangle_theorem.py` enumerates all 44,189
eligible order-14 first factors, checks their crossing-chord histogram,
and independently replays the exact activation and exponent rectangle on
three support samples.  Its output
`tmp/fourteen_vertex_c14_rectangle_theorem_verified.json` contains
`"verified": true`.  See
`SINGLE_EVEN_CYCLE_RECTANGLE_THEOREM.md`.

### Full `C3+C3+C8` equality family

The mixed factor census exposes a disconnected terminal case.  Fixing
`C3+C3+C8` leaves 44,250 eligible singleton perfect matchings.  A fresh
exact enumeration of the perfect matchings in `F union S`, followed by a
128-subset zeta transform, eliminates 44,064 singleton factors by a
forbidden one-term amplitude.  Their minimum witness sizes have histogram
`2:40032, 3:3312, 5:720`.

The remaining 186 factors are exactly the Cartesian product of the six
perfect matchings between the two triangles and the 31 perfect matchings
inside `K8-C8`.  Consequently all three singleton colour classes, as well
as the full factor, preserve the same split
`{0,...,5}|{6,...,13}`.  Every candidate skeleton is disconnected.

For a disconnected support, coefficients factor as
`T(a_L,a_R)=T_L(a_L)T_R(a_R)`.  The required coefficient
`T_L(c^6)T_R(c^8)=1` makes both factors nonzero for every colour `c`.
Using distinct constant colours `c` and `d` on the two components therefore
produces the forbidden nonzero coefficient
`T_L(c^6)T_R(d^8)`, a contradiction.

`verify_fourteen_vertex_c3_c3_c8_family.py` independently reconstructs all
44,250 factors and all activation counts, checks the exact `6 x 31`
survivor product, and writes
`tmp/fourteen_vertex_c3_c3_c8_family_verified.json` with
`"verified": true`.  This closes the complete finite `C3+C3+C8` equality
family, not the remaining order-14 factor types or the global conjecture.
See `FOURTEEN_VERTEX_C3_C3_C8_FAMILY_CERTIFICATE.md`.

### Full `C4+C5+C5` equality family

The exact factor-family explorer starts from 44,195 singleton perfect
matchings in the complement of `C4+C5+C5`.  One-term activation tests leave
4,495 individually safe factors.  The obstruction catalogues contain 200
two-edge one-term sets and respectively 5,600, 63,600, and 114,600
matching forks of sizes three, four, and five.

Size-three forks leave 3,295 factors in 13 full-factor orbits.  Twelve
representatives admit no compatible second factor.  The remaining
representative admits four seconds, but size-four and size-five forks
eliminate every ordered third factor.  Hence the exact residual support
count is zero.

`verify_fourteen_vertex_c4_c5_c5_family.py` independently reconstructs all
44,195 factors and their activation counts, semantically checks all 183,800
fork certificates, regenerates the 1,600 automorphisms and 13 factor
orbits, and reproduces the exact `4 -> 0` compatibility boundary.  Its
output `tmp/fourteen_vertex_c4_c5_c5_family_verified.json` contains
`"verified": true`.  This closes the complete finite `C4+C5+C5` equality
family, not the remaining order-14 factor types or the global conjecture.
See `FOURTEEN_VERTEX_C4_C5_C5_FAMILY_CERTIFICATE.md`.

### Full `C3+C3+C4+C4` equality family

The exact complement census has 44,262 singleton perfect matchings.
Proper-subset activation removes all but 7,974 individually admissible
factors, which form 14 orbits under the 9,216 automorphisms of the fixed
`C3+C3+C4+C4` full factor.

Every matching of singleton edges is exactly activatable: precolour its
endpoints by their edge labels, then properly 2-colour the remaining
factor-1/factor-2 paths and even cycles.  This makes the size-three through
size-five one-term catalogues sound for arbitrary mixtures of the three
singleton colour classes.  The exact funnel is:

```text
compatible second-factor prefixes                 12,172
size-three-compatible thirds                   2,911,352
larger-one-term-free thirds                    2,863,992
connected thirds                               2,862,996
disconnected thirds                                  996
```

The disconnected cases close by tensor factorization.  For the connected
cases, 5,039 exact binomial-to-trinomial transports generate 21,837
deduplicated replacement rules and leave 394,068 candidates.  A catalogue
of 395,784 stable `C4` two-to-three matching forks supplies one exact
certificate for every residual candidate.  Four shards each replay 98,517
supports, with zero survivors.

`verify_fourteen_vertex_c3_c3_c4_c4_family.py` independently regenerates
the factor and one-term catalogues, automorphism orbits, pair/triple
filters, all direct transports, every compact stable-fork certificate, and
the complete shard partition.  Its output
`tmp/fourteen_vertex_c3_c3_c4_c4_family_verified.json` contains
`"verified": true`, reports 394,068 replayed stable forks and zero residual
supports.  This closes the complete finite `C3+C3+C4+C4` equality family,
not the remaining order-14 factor types or the global conjecture.  See
`FOURTEEN_VERTEX_C3_C3_C4_C4_FAMILY_CERTIFICATE.md`.

### `C4+C4+C6` hard-sample factor-choice closure

The 93 deterministic first-orbit samples split into 87 direct even-cycle
factor forks, three disconnected supports, and three initially hard
supports at indices 12, 14, and 15.  Corrected source/target-pair
certificates now independently close indices 12 and 14 by a conditional
`8 -> (10,10) -> 13` fork.

Index 15 needs a larger exact disjunction.  Eighty conditional forks rule
out 17 local colour codes on the first `C4` and 63 codes on the `C6`.
Full-only product equations then force the middle-`C4` binomial on 72 of
its 81 local codes.  On this forced slice:

```text
full-containing ten-term equations                 345,042
distinct forced signed relations                       522
full-containing twelve-term equations            1,042,464
exact four-extra parallelograms                  1,042,464
deduplicated binary factor clauses                  52,059
total factor relations                                  692
```

Exact signed-lattice CEGAR needs only three no-goods.  The resulting
692-variable, 52,584-clause CNF is UNSAT.  The independent verifier
reconstructs the skeleton and all activity counts, semantically replays
all 80 conditional forks, the 72-code forcing premise, all 52,581 original
clauses, and the three lattice conflicts, then obtains an independent
Glucose UNSAT decision.  Its output is
`tmp/fourteen_vertex_c4_4_6_sample93_15_forced_slice_factor_cegar_verified.json`
with `"verified": true`.

This is a theorem for that fixed support only.  It is not yet the complete
`C4+C4+C6` family.  The exact family census has 25,584,375,956 ordered
third-factor candidates after first-factor orbit reduction, of which 996
are disconnected.  A stabilizer-closed transport calculation was then
iterated on exact residuals:

```text
simple sources     rule-closed connected     residual connected
270                      9,828,212,226          15,756,162,734
360                     11,127,431,556          14,456,943,404
449                     12,211,714,856          13,372,660,104
```

At the 360-source checkpoint, first-factor orbit 64 is completely closed.
The third scan retains eight residuals with distinct second factors per
remaining orbit (736 total) rather than only the lexicographically first
support.  The three non-simple residuals in each deterministic round again
occur at sample indices 12, 14, and 15.  The corrected double-pair verifier
independently closes 12 and 14, and the independent factor-choice verifier
reconstructs a 692-variable, 52,584-clause UNSAT certificate for 15 in
every round.

The same transport semantics now has a second, independently cross-checked
enumeration route.  Three edge-disjoint singleton perfect matchings are
encoded with 231 edge variables; 93 selectors symmetry-break the first
factor; three quotient-cut clauses require connectedness.  Preserving the
active singleton mask in every equation of a validated fork is a
conjunction of edge literals, so negating it gives one exact SAT no-good.
The first SAT residual was separately tested against the 44,196-factor
bitset engine, confirmed residual, and then yielded a new semantic fork.

The current globally reconstructed SAT checkpoint semantically replays
2,998 simple source certificates and deduplicates them to 847,118
transport no-goods.  The matching, disjointness, selector, and connectivity
encoding contributes 7,516 base clauses, giving 854,634 clauses before
rich proofs.  Sixty-four exact-mask no-goods from eight independently
verified rich proofs give 854,698 clauses.  A further 152 no-goods from the
minimized factor-CEGAR cores below give 854,850.

`verify_fourteen_vertex_c4_c4_c6_rule_cnf.py` is independent of the
compiler, incremental driver, transport scanner, and augmenter.  At this
checkpoint it freshly enumerates all 44,196 eligible factors, reconstructs
their 93 orbits under 1,536 full-factor automorphisms, replays all 2,998
simple sources and both augmentation layers, and reports exact
clause-by-clause agreement on all 854,850 clauses.  Its output is
`tmp/fourteen_vertex_c4_c4_c6_rule_sat_shared_base31_hard_core12_reconstructed_verified.json`
with `"verified": true`.

The large forced-slice proofs also admit a much stronger transport form.
Every one of the 12 independently verified factor-CEGAR certificates
tested so far has a deletion-irredundant UNSAT core with six original
factor-choice clauses and two exact-lattice blocking clauses.  The core
uses seven factor relations at one forced local code and needs only 14
colouring equations after the two conditional forcing forks are included.
`extract_fourteen_vertex_forced_slice_factor_cegar_core.py` extracts the
guarded-clause core with CaDiCaL, and
`verify_fourteen_vertex_forced_slice_factor_cegar_core.py` independently
checks its source hashes, full-certificate audit, exact clauses,
deletion-irredundancy, forcing premises, equation set, and Glucose UNSAT.
At the reconstructed checkpoint these cores add 152 distinct transported
no-goods of length 9--27, instead of the roughly 141--153 literals required
by the full proof masks.

Range-local CEGAR after that checkpoint has independently solved each
first-factor selector and additionally closed orbits 17, 19, 20, 21, 53,
and 69.  Together with the prior closed set
`23--34, 52, 58--62, 64--66, 70--92`, this leaves 43 of 93 selectors open
in the latest local frontier.  These later clauses still need a global
merge and independent reconstruction before promotion.

Simple-fork selection now improves both sides of the activation search.
For each cycle-local code it retains the first valid target and the target
with the smallest standalone activation mask, then chooses the best of
their eight combinations for each base.  The incremental driver initially
scores 10,000 viable bases and automatically rescans 100,000 when the
activation score exceeds eight.  On a fixed development residual the old
first-target/10,000-base rule required 18 edge conditions; the combined
target search at 100,000 bases requires 6.  Fixed supports without a
simple fork still route fail-closed to the independently replayed
double-pair or minimized forced-slice factor certificate.

The checkpoint and all later range CNFs remain SAT on their stated open
selectors.  The `C4+C4+C6` family and the global conjecture therefore
remain unresolved.

### Later global reconstruction and orbit 5

A later source merge supersedes the range-local checkpoint for theorem
work.  It independently reconstructs 5,800 simple sources, 982,563 simple
transport no-goods, all 37 rich fixed-support certificates, 2,357 global
minimum-activity certificates, the orbit-2 layer, all 2,576
vertex-connectivity-at-least-three quotient cuts, and the orbit-3 layer.
The resulting global CNF has 324 variables and 1,094,961 clauses.

A targeted orbit-5 continuation produced 96 additional independently
audited three-connected minimum-activity certificates.  Independent
transport adds exactly 4,720 fresh clauses.  Selector 237 makes the
1,099,682-clause conditioned formula UNSAT; Kissat's 57,680,258-byte DRAT
trace independently replays as `s VERIFIED`.  Thus first-factor orbit 5 is
excluded.  See `FOURTEEN_VERTEX_C4_C4_C6_ORBIT5_CERTIFICATE.md`.

The same work exposed a compact direct mechanism for two-even-cycle
supports.  A forbidden full-only amplitude gives `r1 or r2`.  Two
forbidden amplitudes with exactly one extra matching separately give
`not r1` and `not r2`, because cancelling that cycle factor would leave
one supported nonzero monomial.  Independent replays validate this
three-amplitude core on tested residuals in both `C4+C10` and `C6+C8`.
Required monochromatic amplitudes are explicitly excluded from the search;
the mechanism currently proves fixed supports and transported SAT rules,
not either complete family.

### Aggregate 58-orbit proof and 59-orbit frontier

The exact per-orbit audit of the 1,094,961-clause later global CNF reports
58 UNSAT selectors and 35 SAT selectors.  Conditioning on the disjunction
of precisely those 58 selectors produces a 1,094,962-clause CNF with
SHA-256
`3c2f44ab2f9e0d7b31666a36006757d999ffa89382530b5c327a80ef14726f4a`.
Kissat's 169,361,294-byte proof has SHA-256
`dd9df6fd8473556eccf3042dbd6068642b8276cf823aa6a7efeaf83f25a9615c`;
independent forward `drat-trim` verification returns `s VERIFIED`.
Together with the distinct orbit-5 proof, this excludes 59 of the 93
first-factor orbits:
`0--5, 12, 17--21, 23--35, 52--53, 58--62, 64--66, 69--92`.
The 34 not excluded are
`6--11, 13--16, 22, 36--51, 54--57, 63, 67--68`.
See `FOURTEEN_VERTEX_C4_C4_C6_59_ORBITS_CERTIFICATE.md`.

### Connectivity-scope correction and orbit-6 closure

The aggregate 58-orbit CNF, and the orbit-5 extension built from it,
explicitly contain vertex-connectivity-at-least-three quotient cuts.
Their theorem scope is therefore conditional on that connectivity
hypothesis. The older verifier payloads and 59-orbit checkpoint omitted
that qualification in prose; they have been corrected. This frontier
remains directly relevant to the prize conjecture because a minimal
counterexample is known to be 4-connected.

A targeted continuation on the next distinct selector, first-factor
orbit 6, closed after 50 SAT residual supports. It produced 400
independently audited minimum-activity factor-fork certificates and
5,824 deduplicated transported clauses. The resulting 324-variable,
1,094,929-clause connectivity-at-least-three CNF has SHA-256
`2207a51d06e4a9b89d6062933c2195838295eed1c18b21da2d7727341945b318`.

Conditioning on orbit 6 gives a 1,094,930-clause CNF with SHA-256
`4bd437f90a55ddeaf8bf8a6386aa7083005149fc2a98cb1d828d61dbd287665b`.
Kissat's 58,660,074-byte DRAT trace has SHA-256
`5052aa97e3fb07a88701b96582662c599e8c0e851f3c07abef3c8db0803ee1a4`;
independent forward `drat-trim` replay returned `s VERIFIED`.
`verify_fourteen_vertex_c4_c4_c6_orbit6.py` independently reconstructs
all 400 certificates, checks the exact DIMACS sequence, and reruns the
proof checker. The combined connectivity-at-least-three frontier is now
60 of 93 first-factor orbits:
`0--6, 12, 17--21, 23--35, 52--53, 58--62, 64--66, 69--92`.
The other 33 remain open. See
`FOURTEEN_VERTEX_C4_C4_C6_60_ORBITS_KAPPA3_CERTIFICATE.md`.

### `C6+C8` orbit-11 closure and 125-orbit frontier

Starting from the independently certified 124-orbit v23 checkpoint, a
targeted orbit-11 continuation closed after 28 SAT residual supports. Its
216 independently audited minimum-activity factor-fork certificates
reconstruct exactly 524 new clauses. The resulting 559-variable,
128,222-clause v24 CNF has SHA-256
`22e9925fb1a222ad36e35e5e9b449dcc799ed684838ed8748c4c26bc6a0b1125`.

A fresh all-328-selector audit classifies exactly 125 orbits as UNSAT:
`0--11, 100--144, 171--173, 179, 182, 185, 187--189, 200--218,
220--225, 227, 232--233, 238, 247, 269, 300--327`. Conditioning on
their exact selector disjunction gives a 128,223-clause CNF with SHA-256
`0497216c436226302016dd8d54a9bb4c2a13aa8a43d3c9906183e2334a9239ef`.
Kissat's 3,196,439-byte DRAT trace has SHA-256
`1e0558fbadf896d2cf4acef4945e3ac43c443a5a75dcbc5bebd0506f9bb78d10`;
independent forward `drat-trim` replay returned `s VERIFIED`.

`verify_fourteen_vertex_c6_8_125_orbits_kappa3.py` recursively reruns the
complete 124-orbit predecessor, independently reconstructs all 216 new
certificates, audits all selectors, checks the exact DIMACS sequence, and
reruns the proof checker. A complete replay returned `"verified": true`
in 84.30 seconds. The theorem explicitly assumes skeleton vertex
connectivity at least three; 203 first-factor orbits and the global
conjecture remain open. See
`FOURTEEN_VERTEX_C6_C8_125_ORBITS_KAPPA3_CERTIFICATE.md`.

As a structural probe, the 524 orbit-11 clauses reduce to an
84-clause deletion-irredundant core over the v23 checkpoint when selector
11 is asserted. Its reduced-width distribution is
`{1: 16, 2: 39, 3: 15, 4: 4, 5: 6, 7: 4}`. Unlike the much smaller
orbit-10 obstruction, this core mixes many edge-role conditions and does
not yet yield a clean reusable graph-theoretic lemma. It is therefore
recorded only as exploratory evidence.

### `C6+C8` orbit-12 and orbit-13 closures

The same fail-closed chain advanced twice more. Orbit 12 closed after 70
SAT residual supports. Its 552 independently audited minimum-activity
certificates reconstruct exactly 1,632 new clauses. The resulting
559-variable, 129,854-clause v25 CNF has SHA-256
`cad473ce07b2b77de2485b27deea93cc9b17d5630b045179339c3625a12942b7`.
A fresh all-328-selector audit reports exactly 126 UNSAT orbits. The
129,855-clause conditioned CNF has SHA-256
`e33044982230a3c75070db53f948abe20f59dc2480c5aa6e94dde53861a0f251`;
its 2,876,653-byte DRAT proof has SHA-256
`2f0f484e8b250316c0e7f8f8ae42a946e730142f53bd98c6cd89bda978571361`.
The full recursive verifier returned `"verified": true` in 128.22
seconds.

Orbit 13 then closed after only seven SAT residuals. Its 56 independently
audited certificates reconstruct 212 new clauses. The resulting
559-variable, 130,066-clause v26 CNF has SHA-256
`66e250a13ff9241ed9809a8855a78a15896aefa5893a9926ebadcbc175acbec9`.
The exact UNSAT set is now
`0--13, 100--144, 171--173, 179, 182, 185, 187--189, 200--218,
220--225, 227, 232--233, 238, 247, 269, 300--327`, leaving 201 SAT
selectors in this rule layer. The 130,067-clause aggregate conditioned
CNF has SHA-256
`188d8d1fc56dc2ae51a02c55f1b9eee1c42fb710d91bdf096c8eafec3b0390d2`.
Its 1,611,777-byte DRAT proof has SHA-256
`495c83209f87efeaf79c4ef588a9f656f74ea5420d95b17e8791130282e15664`
and passes forward `drat-trim`. See
the recursive 127-orbit verifier.

Orbit 14 closed next after 20 SAT residuals. Its 160 audited certificates
reconstruct 296 clauses. The 559-variable, 130,362-clause v27 CNF has
SHA-256
`9dccfdc03f3449ecb843401304b0689da27e1907db19f2c106752f905482310c`.
The exact UNSAT set is now the preceding set with `0--14` in place of
`0--13`, leaving 200 SAT selectors. The 130,363-clause aggregate
conditioned CNF has SHA-256
`86ad71596e6438b6d1aa14d8261348a5e81538adebbb3219b0e1e6cec4973d6f`.
Its 4,445,382-byte DRAT proof has SHA-256
`4ebdfacc7b3061db3ad5647b27c065b5f01f837228ffb171406895d215a8a64d`
and passes forward `drat-trim`. This checkpoint is subsumed by
`FOURTEEN_VERTEX_C6_C8_130_ORBITS_KAPPA3_CERTIFICATE.md`.

### `C6+C8` orbit-15 and orbit-16 closures

Orbit 15 closed after 15 SAT residual supports. Its 120 independently
audited minimum-activity certificates reconstruct exactly 288 clauses.
The resulting 559-variable, 130,650-clause v28 CNF has SHA-256
`691b58cf5e7190113938e8f5467619cfb16b116c93b0848743a125c1f615fb28`.
The 130,651-clause 129-selector conditioned CNF has SHA-256
`d59faa49f5f0932f03131720874dfe08ff41177d92d251bc20e64d7e91aaa108`;
its 1,453,436-byte DRAT proof has SHA-256
`993070712f566208f1cdef1079697e297af4f3dd3d2e15f10971f50f7398f2a7`.
The full recursive verifier returned `"verified": true` in 109.24 seconds.

Orbit 16 then closed after only eight residual supports. Its 64 audited
certificates reconstruct exactly 268 clauses. The resulting 559-variable,
130,918-clause v29 CNF has SHA-256
`6bef527f14379520ecdfa595d51e0d8cad8563014fe9fe09968a5d8901fb1d6a`.
The exact UNSAT set now has initial range `0--16`, 130 selectors in total,
and 198 SAT selectors. The 130,919-clause aggregate conditioned CNF has
SHA-256
`dc65e77dcf468af1caade3f95efa867a37bc76127c6336d73a02df08402fa64a`.
Its 1,634,179-byte DRAT proof has SHA-256
`448d413ab444582edc793984c2bbba143b4e8257d73747626ef4eec2ba71208a`
and passes forward `drat-trim`. The full recursive verifier returned
`"verified": true` in 145.61 seconds. See
`FOURTEEN_VERTEX_C6_C8_130_ORBITS_KAPPA3_CERTIFICATE.md`.

The new generic one-step replay module
`verify_fourteen_vertex_c6_8_kappa3_extension_step.py` keeps later
frontier wrappers small while still recursively replaying the predecessor,
reconstructing every learned clause, auditing all selectors, comparing the
conditioned DIMACS sequence exactly, and checking the raw DRAT proof.

### Exploratory extension-core semantics

Deletion-irredundant clause cores for the orbit-12 through orbit-15
extensions have respectively 320, 58, 53, and 59 clauses. After removing
the asserted target selector, their width distributions are
`{1:16, 2:254, 3:47, 4:3}`, `{1:28, 2:12, 3:18}`,
`{1:25, 2:17, 3:11}`, and `{1:32, 2:11, 3:16}`.

`decode_fourteen_vertex_two_even_cycle_extension_core.py` maps every
DIMACS literal back to a singleton-factor role, skeleton edge, and Boolean
value. All unit rows in these four cores forbid edge inclusion in one of
the two unpinned singleton perfect matchings. The orbit-13 and orbit-15
unit sets are exactly role-symmetric; the deletion-irredundant orbit-12
and orbit-14 cores differ by only one redundant role copy. This identifies
a common allowed-edge-pruning layer, followed by a small collection of
binary and ternary compatibility rules.

Quotienting by the stabilizer of the pinned factor and by interchange of
the other two singleton roles leaves 11 clause types for orbit 13, 22 for
orbit 14, and 19 for orbit 15. This is useful theorem-discovery scaffolding,
but it is not yet a human alternating-cycle lemma: the cores still depend
on the recursively accumulated predecessor rule CNF.

### Gaussian-moment contraction boundary

The defining tensor is exactly a Wick moment tensor: introduce formal
centered Gaussian variables `X_(v,c)` with covariance blocks `W_uv`; then
`T_W(a_1,...,a_n)` is
`E product_v X_(v,a_v)` by Isserlis' formula. The prize target is therefore
a three-term GHZ tensor inside the one-variable-per-vertex slice of a
Gaussian moment tensor.

This suggests contracting a hypothetical order-`n` identity down to six
vertices and invoking the certified six-vertex theorem. The direct
induction has a precise obstruction: pairing eliminated variables to kept
variables produces monomer terms. Equivalently, the contraction is a
multivariate Hermite/loop-hafnian tensor, not the loop-free six-vertex
model already excluded. A global proof along this route needs either a
six-party theorem allowing those induced monomers or killer covectors that
annihilate every cross-pairing term.

The July 2026 structural characterization of graphs whose edges lie in
exactly one or two perfect matchings
<https://arxiv.org/abs/2607.06921> is adjacent but does not remove this
weighted-cancellation boundary. An equality skeleton with no extra perfect
matchings would lie in that unweighted class; the hard SAT residuals
instead rely precisely on additional matchings whose complex monomials
must cancel.

### Even-cycle feasible-set expansion

There is an exact arbitrary-order description underneath the current
factor-fork SAT rules. Let `F` be a union of even cycles and `U` a matching
of singleton edges. Perfect matchings of `F union U` split according to
their used subset `T subset U`. On each cycle, deleting the endpoints of
`T` leaves a perfect matching exactly when consecutive deleted vertices
have odd cyclic distance. The completion is unique on every touched cycle
and has two alternating choices on every untouched cycle.

Consequently, a feasible `T` has exactly `2^k` completions, where `k` is
the number of untouched cycles. The weighted amplitude at an
exactly-`U`-activated colouring is a sum over feasible subsets, and every
summand is a nonzero monomial times one binomial for each untouched cycle.
This simultaneously contains the one-term, one-extra-cycle, and
factor-fork expansions. The proof and precise formula are in
`EVEN_CYCLE_FEASIBLE_SET_EXPANSION.md`.

This does not finish the all-even case. The sharpened global target is to
prove that the feasible-subset poset of three edge-disjoint singleton
perfect matchings always forces an inconsistent family of cycle-binomial
choices.

### `C4+C4+C6` orbit-7 closure and 61-orbit frontier

Starting from the recursively verified orbit-6 CNF, the targeted orbit-7
continuation closed after 68 SAT residual supports. Its 536 independently
audited minimum-activity certificates reconstruct exactly 13,600 clauses.
The resulting 324-variable, 1,108,529-clause CNF has SHA-256
`d7875f904203aa311718d265cd1e14012c3abc9270f1557140c231ebd2713f97`.

Conditioning on selector 239 gives a 1,108,530-clause CNF with SHA-256
`00a08e9f6830ffe05a8ccdb3b5a9c1be6c6651e87601cd1e2a021372bcab7199`.
Kissat's 57,156,850-byte DRAT proof has SHA-256
`3d4a5fc812beb3b166bcfd4f338e9a7b01e57d71e0f1b54a3e75dd883dd5994f`;
independent forward `drat-trim` replay returned `s VERIFIED`. Together
with the aggregate 58-orbit certificate and the distinct orbit-5 and
orbit-6 certificates, the connectivity-at-least-three frontier is now 61
of 93:
`0--7, 12, 17--21, 23--35, 52--53, 58--62, 64--66, 69--92`.
The full recursive orbit-7 verifier returned `"verified": true` in 453.38
seconds. The other 32 remain open. See
`FOURTEEN_VERTEX_C4_C4_C6_61_ORBITS_KAPPA3_CERTIFICATE.md`.

### Four-connectivity and hard-orbit probes

The exact vertex-cut augmentation was generalized from minimum
connectivity three to minimum connectivity four and independently
reconstructed in all three unresolved order-14 families. It added 16,923
clauses to the 125-orbit `C6+C8` checkpoint, 28,313 clauses to the
`C4+C10` checkpoint, and 13,248 clauses to the orbit-6 `C4+C4+C6`
checkpoint. Fresh selector audits produced no additional UNSAT orbits.
This is a rigorous null result for those particular rule checkpoints, not
evidence that four-connectivity is irrelevant and not a classification of
the remaining supports.

For `C4+C10` orbit 2, a separate structural-minimum factor-fork run
examined 100 successive SAT residual supports and learned 6,528
deduplicated clauses without closing the selector. That run is
exploratory only. It shows that simply increasing residual diversity is
not enough on this branch; the next attack must add a genuinely different
semantic obstruction or a stronger higher-order compatibility layer.

The one-extra-cycle transport was also tightened.  Its three source
amplitudes do not require preservation of their complete active matching
masks.  A minimum hitting-set computation, restricted only by the
independently necessary three-connected, edge-disjoint perfect-matching
support conditions, gives independently replayable partial activation
assignments.  On audited residuals the full masks of 10--44 edge
conditions shrink to 2--5.  Ten `C4+C10` cores reconstruct 160 clauses of
width 4--5; thirteen `C6+C8` cores reconstruct 26 clauses of width 3--6.
Both augmented rule CNFs remain SAT, so this is a stronger continuation
mechanism rather than a family theorem.

The mechanism also transfers to the three-cycle family.  On the first
tested residual of still-open `C4+C4+C6` selector 6, eight independently
replayed four-amplitude cores minimize to activation scores 5--8.
Independent symmetry transport reconstructs 192 fresh clauses and exactly
matches the incremental driver's 1,099,873-clause DIMACS file, including
its SHA-256.  The augmented selector remains SAT.  This is the first
cross-family validation of the same full-only/one-extra lemma on all three
unresolved order-14 factor types, but it does not yet exclude orbit 6.

### Minimal singleton-circuit theorem and aggregate order-14 frontiers

The even-cycle feasible-set expansion has been sharpened at
positive-minimal feasible singleton subsets.  If such a subset touches
every full cycle, the proper activation corners force a two-monomial
rectangle contradiction unless each touched cycle has exactly one
adjacent port pair and the contracted singleton subset is one connected
2-regular multigraph.  If some cycles are untouched, the target amplitude
factors as

```text
product_(C untouched) P_C
  * (product_(C touched) P_C + m_T).
```

Therefore either an untouched cycle binomial vanishes or the same
adjacent-port exception occurs on every touched component.  In a
two-cycle full factor, any positive-minimal subset confined to one cycle
forces the other cycle's binomial relation.  The combinatorial verifier
exhausted 38,083 matching subsets, including 1,053 positive-minimal and
878 proper partial cases, with no single-touched port exception.  See
`MINIMAL_SINGLETON_CIRCUIT_RECTANGLE_THEOREM.md` and
`PARTIAL_MINIMAL_SINGLETON_CIRCUIT_DICHOTOMY.md`.

The resulting rule layer has three independently replayed aggregate
order-14 frontiers.  It excludes 365 of 425 pinned `C4+C10` first-factor
orbits, 292 of 328 `C6+C8` orbits under minimum connectivity three, and
65 of 93 `C4+C4+C6` orbits under the same connectivity hypothesis.  The
remaining counts are respectively 60, 36, and 28.  The largest proof is
the 114,637,425-byte `C4+C4+C6` DRAT trace; independent forward replay
returned `s VERIFIED` in 1,752.58 seconds.  Exact CNF/proof hashes,
selector complements, prior-union gates, and the one-command cross-audit
are recorded in
`FOURTEEN_VERTEX_MINIMAL_CIRCUIT_FRONTIERS_CERTIFICATE.md`.

### Adjacent-port determinant transport and support-local continuation

The adjacent-port exception is not algebraically free.  For a proper
base colouring `b` and singleton colour `c`, each exceptional full-cycle
component supplies the nonzero local Schur complement

```text
Delta_C(b,c)
  = W_h[c,c] - W_h[c,d] W_h[a,c] / W_h[a,d].
```

The exact target cancellation forces

```text
product_C Delta_C(b,c) = -product_(e in T) W_e[c,c].
```

The symbolic identity, its cleared-denominator form, 1,200 exact rational
component cases, 12,600 proper-corner checks, and 2,400 global
compositions all passed independent replay.  This converts the rigid
port boundary into signed determinant-lattice relations, but no general
odd dependency has yet been proved.  See
`ADJACENT_PORT_DETERMINANT_TRANSPORT_LEMMA.md`.

On the support-local side, the first sampled residual of `C6+C8` orbit 17
has 18 mandatory partial-circuit relations and a verified five-term
amplitude contradiction: two relation cancellations leave one nonzero
signed monomial class.  A second support has 12 relations but survives an
exhaustive radius-three search over 38,940 candidates, so that result is a
finite null boundary rather than an orbit theorem.

For `C4+C10` orbit 3, the same exact factor, activation-cube, and
signed-class verifier repeatedly finds five-term contradictions and
learns support no-goods.  Two consecutive CEGAR chains add 70 such
no-goods after the four manually audited supports.  Independent chain
audits freshly replay all 70 algebra certificates, confirm that every
support satisfies the immediately preceding CNF, reconstruct every
intermediate DIMACS hash, and recover the final 294,390-clause SHA-256
`9187a1975ef10ea7f69d824d1c87894f88f9278324636067deb39c021459a0f5`.
Orbit 3 remains SAT, so the 74 support exclusions are an audited
continuation frontier rather than an orbit theorem.

For `C4+C4+C6` orbit 8, the first two support certificates require exact
relation-selection CEGAR.  Their 128 and 32 inclusion-minimal branches
all close after two rounds of signed binomial propagation.  Fresh chain
audits replay all 160 branches and produce two exact width-21 support
no-goods.  The twice-augmented 1,220,595-clause CNF has SHA-256
`44e5ed260e04e0cd7207691209038d5f44d0d601b02d2030f91ec8a0ca08fb3f`.

The next six sampled witnesses revealed a smaller invariant core.  Four
mandatory unit relations generate four equal-magnitude two-coset
relations; the resulting rank-eight signed lattice isolates one nonzero
class in a forbidden 13-matching amplitude.  This closes each support
without enumerating any optional relation selection.

Quotienting those supports by the stabilizer of the pinned first factor
shows three residual types.  The full `C4+C4+C6` factor has 1,536
automorphisms, the orbit-8 pinned matching has stabilizer size 8, and
colour 1 can be swapped with colour 2.  The pinned-factor support
symmetry lemma therefore transports each certified obstruction to 16
distinct support images.  Independent augmentation replays add 16, 15,
and 15 fresh no-goods and reproduce the final 1,220,641-clause CNF with
SHA-256
`3c5b2cc66ebc198d3a27fa6a323ea4a4ce4aa0f9c9825ae83007a9b2b13912c7`.

Conditioning on selector 240 gives SHA-256
`edbdd2cc6151a3d831c08cc6825ee9f64e59befc67956d45a0cedb9a25d51a15`.
Kissat generated a 58,902,708-byte DRAT trace with SHA-256
`5555d2f3fbd3f116a05f08d50fbfefbf7a3239822a1081360c4f5c737ee98074`;
independent forward `drat-trim` replay returned `"verified": true` in
702.50 seconds.  Orbit 8 is therefore excluded in the
minimum-connectivity-three equality architecture.  Together with the
prior union this closes 66 of 93 `C4+C4+C6` selectors and leaves 27:
`9--11, 13--16, 22, 36--41, 44--51, 54--55, 57, 63, 68`.
See `FOURTEEN_VERTEX_C4_C4_C6_ORBIT8_CERTIFICATE.md` and
`PINNED_FACTOR_SUPPORT_SYMMETRY_LEMMA.md`.

The same closure census on the second `C6+C8` orbit-17 support is a
sharper null boundary.  All 12 relations are mandatory, but an independent
radius-three replay over 63,809 colourings (maximum activity 22) finds no
one-class forbidden amplitude, no two-class amplitude at all, and no
monochromatic rational anchor.  Thus neither signed nor arbitrary
rational two-coset closure can advance that sampled support within the
audited radius-three source census.

The July 2026 characterization of graphs whose edges lie in exactly one
or two perfect matchings does not directly cover these hard residuals:
the sampled `C6+C8`, `C4+C10`, and `C4+C4+C6` skeletons have hundreds of
perfect matchings and every edge occurs in dozens of them.  Its ear and
tight-cut structure may still be useful inspiration, but it is not a
certificate for the weighted-cancellation cases here.

The earlier PMValid characterization was also rechecked against the new
balanced bridge normal form.  Its weighted theorem proves
`bar(mu)(G)=mu(G)` when the unweighted matching index is not one.  This is
powerful for the characterized matching-index-two class, but it does not
close the present branch: a dense physical skeleton may have unweighted
matching index one even though restricted weighted two-colour slices are
valid.  Applying that theorem to a restricted entry support would also
discard other colour entries on the same physical edges.  Thus it
motivates the complementary-minor analysis but cannot be used as a
shortcut to a three-colour exclusion.

### Three-colour hyperplane annihilation

The contraction argument behind the local killer theorem has a concise
exact classification.  If `H_1,...,H_m` are subspaces of `C^3`, each of
dimension at least two, then

```text
sum_(c=0)^2 product_u y_u[c]
```

vanishes identically on `H_1 x ... x H_m` if and only if every coordinate
term is killed outright: for each `c`, some `H_u` is the coordinate
hyperplane `y[c]=0`.

The proof uses only the rank-one fact that a sum of two nonzero
decomposable tensors can be decomposable only when the summands are
proportional in all but at most one mode.  Three nonzero coordinate terms
would force the restricted coordinate functionals to span dimension one
in some mode, contradicting `dim(H_u)>=2`; one or two zero terms are also
impossible unless all three vanish separately.

Applied after contracting one vertex against a generic vector, this
shows without a positivity assumption that each vertex and colour has an
incident block supported on precisely that leaf-colour column.  A finite
union of proper linear subspaces cannot cover the generic contraction
space, so the killer neighbour can be fixed independently of the
contraction.  See
`THREE_COLOUR_HYPERPLANE_ANNIHILATION_THEOREM.md`.  This shortens the local
structural reduction but does not solve the remaining global compatibility
problem among the killer edges.

## Numerical result: the boundary, not a witness

The full `(6,3)` system has 135 complex variables and 729 cubic equations.
Independent random restarts with complex Adam and Levenberg-Marquardt did
not produce a finite solution.  Once vertex-scaling gauge was removed, every
successful basin collapsed to the same sparse pattern:

- six triangle-edge weights of magnitude `x`;
- three rung weights of magnitude `x^-2`;
- one forbidden colouring of amplitude `x^-6`.

This is the triangular-prism degeneration already noted in discussions of
the problem.  It approaches GHZ as `x` tends to infinity but is never exact
at finite `x`.  Run:

```powershell
python prism_boundary.py --x 10
```

The independent verifier intentionally rejects all saved approximate
candidates unless every one of the 729 equations is below the requested
tolerance.  Approximation is not reported as a counterexample.

## Reproduction

```powershell
python -m unittest -v test_search_witness.py
python search_witness.py --n 6 --d 3 --restarts 8 --steps 20000
python verify_witness.py best_candidate.json --tolerance 1e-10
```

`search_witness.py` contains:

- exact perfect-matching enumeration;
- the full complex equation system;
- an analytically checked Wirtinger gradient;
- complex Adam;
- Levenberg-Marquardt polishing;
- vertex-gauge balancing;
- optional upweighting of the three required monochromatic equations.

Additional focused commands:

```powershell
python killer_pattern_certificates.py --pattern killer_101_pattern.json
python two_vertex_quotient.py --prism-x 3 --samples 100
python search_prism_stratum.py --restarts 20 --steps 20000
python solve_prism_core.py --restarts 100 --scale 1
python generate_prism_singular.py `
  --output prism_core_constant_32003.sing `
  --mode core-and-constant
python prism_orbit_screen.py --summary
python prism_orbit_screen.py `
  --index 0 `
  --output prism_orbit_0_generic_q.sing `
  --characteristic 0 `
  --add-rank-one-minors
python prism_orbit_batch.py `
  --indices 41 92 295 326 408 503 `
  --output-directory tmp/prism_batch_size18 `
  --characteristic 0
python verify_prism_certificates.py
python verify_all_prism_orbits.py `
  --output tmp/all_prism_orbits_verification_signed.json
python verify_killer_union_orbits.py `
  --orbits tmp/m10_c4_k2_orbits.json `
  --missing-edges 01,03,12,23,45 `
  --output tmp/m10_all_orbits_verification_signed.json
python verify_global_candidate_cegar.py `
  tmp/global_candidate_cegar_signed_5000.json
python verify_candidate_separator_orbits.py `
  --solver cadical195 --jobs 2 `
  --output tmp/candidate_separator_s5_cadical.json
```

## Full-colour factor and support transport

The three-colour target is invariant under a common `S3` permutation of
the colour coordinates.  Two finite transfer principles follow.

First, a proved first-factor orbit exclusion holds in every singleton
role.  Transporting the 66 proved `C4+C4+C6` factor-orbit exclusions to all
three roles adds 115,500 width-seven no-goods.  The independent verifier
freshly enumerates all 44,196 eligible factors, reconstructs all 93
full-factor automorphism orbits, binds the predecessor theorem audits, and
rebuilds the augmented DIMACS byte-for-byte.  The resulting CNF is

```text
tmp/fourteen_vertex_c4_c4_c6_colour_symmetric_orbit_exclusions.cnf
clauses  1,336,141
SHA-256 f7b2b2628e65abccfa2ccb7798ac51b2fcb31682ced01a534750d31094459ea8
```

Second, one support obstruction transports under
`Aut(F) x S3`.  Here `|Aut(C4+C4+C6)|=1536`, so a support orbit has at
most 9,216 images.  The new clause-set audit independently reconstructs
that orbit and the exact width-21 no-goods without repeatedly parsing and
rewriting a two-million-clause DIMACS.  The full DIMACS is still
materialized and independently replayed every ten support certificates
and at every terminal checkpoint.

The first bounded orbit-9 run certified 97 fresh supports on top of two
earlier full-colour supports.  All mandatory-unit algebra certificates and
all clause-set audits passed.  Ten batched DIMACS checkpoints add 716,544
fresh no-goods during the deferred run, or 730,368 including the two
predecessor supports.  The final exact checkpoint is

```text
tmp/fourteen_vertex_c4_c4_c6_fullcolour_deferred_orbit9_symbinomial100.cnf
clauses  2,066,509
SHA-256 113d712f100c3d44705ce801f546c419ead18d1b3ab0780b00d7c68058368fc1
```

A fresh CaDiCaL assumption audit leaves all 27 frontier selectors SAT.
Thus the run is a finite null result and orbit 9 remains open.  A separate
orbit-16 scout closes from six mandatory relations plus 218 independently
replayed derived relations; an orbit-49 scout survives its mandatory unit
core.  These scouts guide the next selector order but do not themselves
change the proved 66-of-93 factor-orbit count.

The first full orbit-16 run then certified 100 fresh supports.  Every
mandatory-unit closure, symmetry clause-set reconstruction, and one of ten
batched DIMACS materializations passed its independent verifier.  The run
adds 898,560 fresh no-goods and ends at

```text
tmp/fourteen_vertex_c4_c4_c6_fullcolour_deferred_orbit16_symbinomial100.cnf
clauses  2,965,069
SHA-256 33bd2e02cb0b5ea885dd4207b6c260159ef3beea2317c22157580b34c3431faf
```

A new CaDiCaL assumption audit of the exact final CNF again leaves all 27
frontier selectors SAT.  This is another finite null result, not an
orbit-16 exclusion, so the proved count remains 66 of 93.  The certified
search therefore continues beyond support 100 rather than treating the
absence of an early core as evidence of satisfiability over the complex
weights.

Supports 101 through 104 again close under the mandatory-unit calculus,
but support 105 is the first orbit-16 model whose mandatory core survives.
Its partial-circuit relation system has six unit and six binary clauses,
so there are exactly 64 inclusion-minimal relation selections.  Radius-two
binomial closure leaves the first branch open; radius three exposes the
same isolated nine-term forbidden class in every one of the 64 branches.
The top-level verifier independently rebuilds all relation clauses,
replays all 64 branch certificates, checks minimality and prior-model
binding, and proves the terminal relation-selection CNF UNSAT:

```text
tmp/fourteen_vertex_c4_c4_c6_fullcolour_deferred_orbit16_support105_partial_binomial_selection_cegar_r3_full_verified.json
verified branches  64
contradiction mode isolated_nonzero_lattice_class (64 of 64)
```

This support has a nontrivial stabilizer, so its full
`Aut(C4+C4+C6) x S3` orbit contains 4,608 rather than 9,216 no-goods.
Reconstructing supports 101 through 105 from the support-100 base gives
the independently byte-verified checkpoint

```text
tmp/fourteen_vertex_c4_c4_c6_fullcolour_deferred_orbit16_symbinomial105.cnf
clauses  3,006,541
SHA-256 f17e26b01725ac70d5d46471c577d5fd2ea9318ce6606d6b61ae6a3568bda02c
```

A fresh 27-selector CaDiCaL audit is still SAT in every case.  Thus the
deeper branch certificate is a real support exclusion and reusable
scaffolding, but it does not yet exclude orbit 16 or change the 66-of-93
frontier.

The continuation through support 200 is now complete.  Supports 106
through 200 all close under the mandatory-unit calculus; there is no
second surviving relation-selection core.  All 95 per-support
certificates, all symmetry clause sets, and all ten batched
materializations pass their independent verifiers.  Ninety-three supports
have full orbit size 9,216, while supports 174 and 191 have orbit size
4,608.  The continuation adds exactly 866,304 fresh no-goods and ends at

```text
tmp/fourteen_vertex_c4_c4_c6_fullcolour_deferred_orbit16_symbinomial200.cnf
clauses  3,872,845
SHA-256 00f43c0a6cac2d444f0c82d26e8719180942f7efef5f89a14209c23158b4ebb2
```

The support-200 batch verifier independently reproduces the final bytes.
A fresh CaDiCaL audit performs 27 assumption solves against that exact
hash and again returns SAT for every unresolved selector:
`9--11, 13--16, 22, 36--41, 44--51, 54--55, 57, 63, 68`.
This is an exact finite null result.  It does not exclude orbit 16 and the
proved frontier remains 66 of 93.

An attempted shortcut selected all 18 possible relations simultaneously;
the same forbidden class survives that enlarged lattice.  This does
**not** replace the 64-branch proof.  Optional relations can identify and
cancel monomials that an actual smaller relation selection does not
identify, so nonvanishing after such a coarsening is not monotone in the
direction required here.  The experimental support-closure code and its
four invalid derived artifacts were removed.  Only the exhaustive,
independently replayed 64-branch certificate is authoritative.

### Double-star annihilation and bilinear blockers

The contraction argument can be strengthened without introducing the
monomer terms that obstruct a many-party Gaussian contraction.  Fix two
roots `p,r`, local vectors `x,y` with `x^T W_pr y=0`, and allow one
exceptional partner `q` for `p`.  Put every other local vector in the
intersection of the kernels of its contractions toward `p` and `r`.
Every matching is then killed: either `p` does not use `q`, or the
surviving `pq` branch leaves `r` to use one of its killed edges.

For the GHZ contraction to vanish as well, each colour supported by both
`x` and `y` must have at least two distinct blocker vertices; one is
insufficient because it can be chosen as the exceptional `q`.  If
`rank(W_pr)>=2`, the orthogonality hypersurface
`x^T W_pr y=0` is irreducible.  Multiplicity-two covering then forces two
fixed blocker determinants to vanish on the whole hypersurface, hence to
be scalar multiples of `x^T W_pr y`.  For a rank-three root edge the
scalar is zero by rank, yielding two exact column-wedge identities for
each colour, six around the edge in total.

This is an arbitrary-order necessary condition, not a prize proof.
The same multiplicity argument gives componentwise factor identities for
rank-one root edges and identically vanishing blocker determinants for a
zero root edge.  It remains to combine these identities with the existing
killer flags and anchors and force either a global rank collapse or a
forbidden amplitude.  The exact statement and proof are in
`DOUBLE_STAR_ANNIHILATION_LEMMA.md`.

For a non-coordinate killer `W_pr=a e_c^T`, the rank-one component
identity has a useful local shadow.  At two distinct vertices `u`, either
both non-`c` columns of `W_pu` lie in `span(a)`, or the corresponding two
columns of `W_ru` are linearly dependent.  This upgrades the former
one-backup picture to a two-witness backup-or-rank-defect dichotomy.

Retaining the constructible blocker loci, rather than only their
determinant closures, makes both conclusions sharper.  Multiplicity two
forces one fixed pair of vertices to be actual blockers on a dense subset
of the root hypersurface.  At a rank-three root edge, each such vertex
either carries a nonzero column-`c` incident block on one side or the two
incident blocks share an exact kernel vector supported on the other two
colours.  On the non-coordinate-killer component, the projected non-`c`
row spaces must lie in one common line unless the head-side block is
itself a nonzero column-`c` killer.  Thus the second witness is not merely
an unnamed rank defect: it is a reciprocal killer, a tail backup, or an
aligned quotient defect.

The two automatic primary blockers can also be disabled simultaneously.
For non-coordinate colour-`c` killers `A e_c^T` at `p` and `B e_c^T` at
`r`, restrict the root block to `A^perp x B^perp`.  Either this restriction
is the exceptional pure product `lambda x_c y_c`, equivalently

```text
W_pr = lambda e_c e_c^T + A s^T + t B^T,
```

or its zero locus contains a coordinate-open component on which two fixed
blockers persist densely.  On a rank-two restricted root form, the old
primary neighbour of one root can persist only by serving as a
failure-hyperplane backup for the other root.  Without those cross-backups,
two genuinely new blocker vertices are forced.  This gives a new
coordinate-bridge-or-deeper-flag dichotomy for the non-coordinate killer
branch; it still needs a global incidence argument to become an
arbitrary-order exclusion.

There is now also an exact boundary for the extreme case in which every
pair is a coordinate-product bridge for one fixed colour.  Restricting
all vertices to their primary failure planes collapses the matching side
to `haf(lambda) product_i x_i[c]`.  The three-term tensor classification
then forces `haf(lambda)=1` and one of only two exceptions: either the two
other colour-product tensors are both killed by coordinate primary
vectors at some vertices, or every primary vector has zero `c` coordinate
and the two remaining product tensors are proportional with global ratio
`-1`.  Away from those explicit boundaries, at least one vertex pair must
produce deeper blockers.  The remaining task is to exclude the two
all-bridge boundary patterns using the other colours' flags and anchors.

Two normal-slice arguments sharpen this boundary further.  The phase
exception in which every primary vector has zero `c` coordinate and the
two other restricted colour products cancel is impossible.  Leave one
failure plane unrestricted.  After expanding at that vertex, every
non-coordinate matching term has only one exceptional restricted mode,
whereas the normal derivative of the two cancelling GHZ products is a
nonzero product over all remaining modes.  Setting the `c` coordinate to
zero at two of those modes kills the matching side but not the target.

For the coordinate-primary exception, let `r` vertices have primary
vector `e_alpha`.  Leaving those `r` modes unrestricted shows that the
restricted matching tensor differs from the pure `c` product in at most
`r` modes.  Hence at most `r` other failure planes can have independent
restricted `alpha` and `c` coordinates.  Every `e_beta` primary supplies
one such plane, and the symmetric inequality reverses the count.  The two
coordinate-primary sets therefore have equal size.  Any remaining primary
vector would have to lie in both `span(e_alpha,e_c)` and
`span(e_beta,e_c)`, hence be proportional to `e_c`, which was excluded.
Thus the sole all-bridge boundary is a balanced partition: exactly half
the vertices have primary vector `e_alpha` and half `e_beta`.  This is
proved in `DOUBLE_STAR_ANNIHILATION_LEMMA.md`; excluding that final normal
form, or forcing another colour into the deeper-blocker branch, is the
remaining analytic step.

The balanced form also forces two cross-partition diagonal matrices, for
colours `alpha` and `beta`, to have permanent one, while the full
coordinate-`c` diagonal matrix has hafnian one.  Colouring one cross pair
`c` and every other vertex `alpha` shows that each nonzero cross
coordinate-`c` edge lies at a zero of the `alpha` permanental cofactor
matrix; the same edge lies at a zero of the `beta` cofactor matrix.  When
`n=2 mod 4`, every coordinate-`c` perfect matching has a cross edge, so the
two cofactor matrices must have a common zero.  The balanced branch is
therefore confined to an exact cofactor-degenerate stratum in the orders
`6,10,14,...`; this is a new necessary condition, not yet an exclusion.
More generally, choose equally sized subsets `S` and `T` in the two
halves, colour them `alpha`, and colour the complement `c`.  The zero
pattern forces all selected vertices to match across the partition, so
the amplitude is exactly
`per(P[S,T]) haf(L[V-(S union T)])`.  It is one at the two endpoints
`|S|=0,n/2` and zero at every intermediate size.  The same statement
holds for the `beta` cross matrix `Q`.  The three monochromatic matching
polynomials therefore obey a complete complementary-minor orthogonality
system; the two cofactor identities are its extreme intermediate layers.
Combining this with the permanent Laplace expansion strengthens the
degeneracy at every layer.  Since `per(P)=1`, for each intermediate `k`
there are `S,T` of size `k` for which both the selected and complementary
`P` subpermanents are nonzero.  The two corresponding mixed-colour
equations force both complementary induced hafnians of `L` to vanish.
In particular, the zero pattern of the cross hafnian-cofactor matrix
contains a perfect matching.  The same conclusions follow from `Q`,
possibly on different cuts.
The condition is nonempty: for a three-by-three partition, `P=Q=I_3` and
a cyclic-derangement cross matrix `L` satisfy the two permanent-one,
hafnian-one, and all complementary-minor equations.  They do not satisfy
the remaining mixed-colour amplitudes, so this is a boundary sanity check
and not a candidate witness.

A tempting three-colour extension of this factorization was checked and
rejected.  Equal `alpha` and `beta` counts in the two halves do not force
both colours to use only cross edges: an internal `alpha-beta` edge in
the first half can be balanced by an internal `alpha-beta` edge in the
second.  For three vertices per half, the colouring
`(alpha,alpha,beta)` on each half already has such a matching.  Therefore
no joint product of an `alpha` subpermanent, a `beta` subpermanent, and a
`c` subhafnian is claimed.  Only the asymmetric `alpha/c` and `beta/c`
complementary-minor systems above are authoritative.

The corrected balanced `alpha/beta` equation is still exact.  If
`S subset X` and `T subset Y` are the equally sized sets coloured
`alpha`, matching-type balance eliminates the triangular cross edges and
the internal same-colour edges.  The only survivors are `P` edges between
`S,T`, `Q` edges between their complements, and equal numbers of internal
`alpha-beta` edges in the two halves.  They are precisely the perfect
matchings of the artificial bipartite block matrix

```text
[ P[S,T]       V[S,X-S]       ]
[ U[T,Y-T]^T   Q[X-S,Y-T]^T   ].
```

Its permanent is one at the all-`alpha` and all-`beta` endpoints and zero
at every intermediate layer.  This replaces the rejected product
shortcut and identifies the paired internal-transition matrices `U,V` as
the genuine remaining mixed-colour obstruction.

At the first intermediate layer the zero block permanent expands as
`P_xy cof(Q)_xy` plus a sum of products
`V_xb U_yd per(Q without x,b,y,d)`.  Hence any nonzero
`P_xy cof(Q)_xy` requires both internal transition matrices.  If either
`U` or `V` vanishes, every intermediate block permanent factors and
`P,Q` themselves obey a third complementary-minor orthogonality system.
This is a sharp transition-free/coupled dichotomy, not yet an exclusion
of either branch.

As a finite sanity check of the matching-type bookkeeping, a deterministic
nonzero integer assignment on the full balanced order-six zero pattern
was enumerated over all 20 equally sized choices of `S,T`.  Direct
perfect-matching sums agreed with the corresponding block permanents in
all 20 cases.  The arbitrary-order statement itself follows from the
displayed vertex-count equations, not from this finite check.

### Orbit-16 supports 201--300 and the first orbit-49 radius-three support

The full-colour orbit-16 support CEGAR has now reached support 300.  Every
one of supports 201--300 had a mandatory-unit binomial contradiction and
was independently verified before its full factor-automorphism and
six-colour orbit was admitted.  The ten deferred batches contributed
834,048 fresh width-21 no-goods in total.  The terminal materialization is

```text
tmp/fourteen_vertex_c4_c4_c6_fullcolour_deferred_orbit16_symbinomial300.cnf
```

with 324 variables, 4,706,893 clauses, and SHA-256
`95db7b12bcd7ead4f9076ff973db1cd9c9957c28d83918ce248b5a65c2b68df7`.
The run manifest has SHA-256
`c01e28ed9e0dc09922192de3614f9af29424d13015f50c4661da645273b9d7a2`.
A fresh 27-selector CaDiCaL audit still finds all 27 frontier selectors
SAT; the audit artifact has SHA-256
`ba1d6f9bd961d18cb0cca1dbb84b14e4701296e8c1f20f72662f91e975270006`.
This is an exact null result for this CNF layer, not a graph construction.

A different orbit-49 model exposed a support whose mandatory core
survived, so it was not closed by the mandatory-unit shortcut.  Its exact
relation CNF has 18 relation variables and 64 inclusion-minimal
selections.  The radius-three search excluded all 64 selections.  A
standalone chain verifier then:

1. checked every relation clause and every selection's minimality;
2. confirmed that each selection was still feasible before its learned
   block;
3. freshly replayed all 64 algebraic branch certificates; and
4. independently solved the terminal relation-selection CNF as UNSAT.

All 64 contradictions isolate a nonzero lattice class supported on 15
active matchings.  Selection sizes are 10 in 16 branches, 11 in 32
branches, and 12 in 16 branches.  The terminal chain

```text
tmp/fourteen_vertex_c4_c4_c6_fullcolour_orbit49_scout1_partial_binomial_selection_cegar_r3_complete.json
```

has SHA-256
`96fa261086a8397486d0b1e210974642642405eb63b63b8c26c663edd4711407`;
its independent verifier has SHA-256
`6a8e9d6d56be85f57c04e2551cd4200e30ffc2fd056c2f666e5a076e0433f0b5`.
This certifies one exact support no-good, not all of selector 49.

Full factor and colour symmetry expands this theorem to 9,216 distinct
width-21 clauses.  The independently reconstructed clause set has
SHA-256
`28106e110c9e7aa84742ee5b50eb39f08f798166c216f89f00de6d477f88ded0`.
Because the support was originally selected from an older CNF, the
certificate retains that source hash.  The separate streaming
materializer `materialize_verified_dimacs_clause_set.py` binds the
verified theorem clause set to the newer target without rewriting its
provenance, and `verify_materialized_dimacs_clause_set.py` reconstructs
the 453 MB result byte for byte.  None of the 9,216 clauses was already
present.  The resulting CNF is

```text
tmp/fourteen_vertex_c4_c4_c6_fullcolour_orbit16_symbinomial300_orbit49support1.cnf
```

with 4,716,109 clauses and SHA-256
`e9482392e9c6568190ba6a1a4cd6c23025e7c8fd5a17fc5ff0c582cf864adb35`.
A fresh audit again leaves all 27 frontier selectors SAT.  Orbit 49
therefore remains open, and its next inequivalent support also has an
open mandatory core; the sound radius-three relation-selection search is
continuing there.  The global conjecture remains unresolved.

### Simultaneous three-colour balanced-bridge intersection

The all-bridge boundary of the double-star lemma can now be intersected
across all three colours.  In the balanced coordinate normal form, each
vertex `i` has one of eight types

```text
f_i = (f_i(0),f_i(1),f_i(2)),
f_i(c) != c.
```

For an edge `ij`, the colour-`c` bridge condition restricts the block on
the two coordinate failure planes to `lambda x[c]y[c]`.  Testing matrix
units gives the exact entry criterion

```text
W_ij[r,s] can be nonzero only if, for every c,
(r,s)=(c,c) or r=f_i(c) or s=f_j(c).
```

The 64 ordered endpoint-type pairs have at most four allowed entries.
The exact entry-count distribution is `0:2, 2:12, 3:44, 4:6`; the
structural-rank distribution is `0:2, 1:12, 2:42, 3:8`.  Rank three is
possible exactly when the two types are bitwise complementary.  Such a
pattern contains all three diagonal entries and at most one additional
off-diagonal entry.  The two cyclic types `120` and `201` have zero blocks
within their own type.

There is also a useful reciprocity consequence.  If the primary singleton
entry `(f_i(c),c)` is permitted on `ij`, then applying the criterion with
colour `f_i(c)` forces

```text
f_j(f_i(c))=c.
```

Thus the transposed singleton is automatically a killer for the paired
colour at the other endpoint.

At support degree four, the three coordinate primary killers use distinct
neighbours and none can be a diagonal anchor.  All three anchors therefore
use the fourth neighbour.  Its block is diagonal with all three entries
nonzero, and the endpoint types are complementary.  If the entire skeleton
is 4-regular, those diagonal edges form a perfect matching and the other
three incident edges at every vertex form a reciprocal-singleton cubic
subgraph.  This is a new normal form, not yet a contradiction.

The generator/verifier artifact

```text
tmp/three_colour_balanced_bridge_intersection_verified.json
```

has SHA-256
`c99df4a42d4f4066ebf05ad78ce7cd4f74ec9b2479a41049f0ce4606756a4820`.
An independent program rebuilds the eight types from three binary choices,
restricts all nine matrix units directly to the coordinate planes, and
checks the complete 64-record table.  Its output

```text
tmp/three_colour_balanced_bridge_intersection_audited.json
```

has SHA-256
`41015b2cd28cacec7f61639efcda1af31ac3a0984e5caa16191cde823ab79944`
and reports `"verified": true`.  The theorem and its exact remaining
boundary are in
`THREE_COLOUR_BALANCED_BRIDGE_INTERSECTION_THEOREM.md`.

### Four-regular balanced all-bridge branch excluded at every order

The degree-four normal form above is now a contradiction, not merely a
classification.  Let `A` be its diagonal-anchor perfect matching and
contract the `m=n/2` anchor pairs.  Across the two complementary endpoint
types of each pair, the six primary singleton edges have exactly the six
directed colour labels

```text
0->1, 0->2, 1->0, 1->2, 2->0, 2->1.
```

Reciprocity pairs `a->c` only with `c->a`.  A pair-constant colour `d`
can replace its anchor only when the two outgoing `d` ports lie at
different physical endpoints.  The two cyclic types allow all three such
transitions; each of the other six types allows exactly one.

The singleton edges together with all usable transitions form a
maximum-degree-two contracted port graph.  Its cyclic components alternate
between the two edge kinds, and adjacent transition colours differ.  Fix
a constant background colour `d` and change the colour at just one anchor
pair.  Any compatible alternating cycle would have a proper cyclic colour
word with exactly one symbol different from `d`, so it must have length
two.  Each of the at most `m` colour-`d` transitions belongs to at most one
such component.  Therefore at most `m` of the `2m` one-pair perturbations
have a compatible cycle; at least `m` do not.

For any cycle-free perturbation, the anchor matching is the unique perfect
matching supporting that nonconstant vertex colouring.  Its contribution
is the product of one nonzero diagonal anchor entry per pair, hence cannot
vanish.  The GHZ target requires the amplitude to be zero.  This excludes
the entire 4-regular simultaneous balanced all-bridge branch for every
even `n >= 6`.

`verify_four_regular_balanced_bridge_obstruction.py` reconstructs all
eight local types, the port and transition tables, the single-defect cycle
lemma, and all 4,096 contracted order-six configurations.  Its output

```text
tmp/four_regular_balanced_bridge_obstruction_verified.json
```

has SHA-256
`9cd041727482da77d878d67191a38d1ea04a99bf8342429b5b229567559eca4e`
and reports `"verified": true`.
The independent direct perfect-matching audit has SHA-256
`20d474d5981d73a68bb8a6c18be555a1b8a7d9f2ecb26896ba067b4506d83987`;
it reconstructs the physical endpoint graphs and checks all 73,728
single-pair perturbation instances without importing the cycle verifier.
The arbitrary-order proof is
`FOUR_REGULAR_BALANCED_BRIDGE_OBSTRUCTION.md`.  The finite census is a
regression audit; generality comes from the transition-count argument.
The remaining simultaneous all-bridge branch must have a support vertex
of degree at least five.  The global conjecture remains unresolved.

### Orbit 44 exact 24-model theorem and the 67-of-93 frontier

The order-14 `C4+C4+C6` frontier has advanced by one complete first-factor
orbit.  Under selector 276, the independently accumulated 4,716,109-clause
predecessor has exactly 24 factor assignments.  Their negative width-21
support clauses equal the deletion-irredundant 24-clause core of the
original 6,912-clause orbit-44 extension.

Fresh enumeration binds eight of those clauses to the first independently
verified algebraic support orbit and sixteen to the second.  The 24
assignments use one, sixteen, and sixteen distinct factors in singleton
roles 0, 1, and 2.  Both pairs involving role 0 have cycle partition
`C6+C8`, while roles 1+2 have `C4+C4+C6`.  The exact enumeration/source
audit

```text
tmp/fourteen_vertex_c4_c4_c6_fullcolour_orbit44_core24_models_verified.json
```

has SHA-256
`b329e7d6d69e9c336a5d11a046377b3affd11b387701b0860dd0cc9f3a77c2a7`.

An independent streaming materializer appends only those 24 verified
clauses, and a second program reconstructs the 4,716,133-clause output
byte for byte.  Its SHA-256 is
`5bea81cd27ae21111f9466c7088694fd3732e1ecae718f0229ef3e08a934cd2b`.
All 93 fresh assumption solves exclude orbit 44 and leave exactly 26
selectors:

```text
9--11, 13--16, 22, 36--41, 45--51, 54--55, 57, 63, 68.
```

Conditioning on selector 276 gives SHA-256
`d1b390a66aee3d748bd12799850fd3a153df8b45872a33f30c2a8f49072a4739`.
Kissat's 192,160,906-byte proof has SHA-256
`26ec2bbc5100d11a4e8b3cc181189c78643ba1563e68688f67869a7c12ba7c0b`
and passes forward `drat-trim`; the replay record has SHA-256
`419f0e33e3a169f291e0b740734a13a02e704071a4b9c74908336aeba2a09702`.
The compact top-level audit with the stored verified replay also passes.

A redundant route keeps all 6,912 source clauses, reconstructs both
algebra supports and the entire augmentation, decides all 93 selectors,
and launches a fresh replay of a different 192,421,858-byte raw proof.
Its end-to-end record has SHA-256
`73f2d102b79fe279eed0cd360cfa63b126578db378a3d60de51b2da6d8ad7ac6`.
Thus 67 of 93 first-factor orbits are finite theorems under connectivity
at least three.  Full hashes and replay commands are in
`FOURTEEN_VERTEX_C4_C4_C6_ORBIT44_CERTIFICATE.md`.  The other 26 orbits
and the global conjecture remain unresolved.

### Four-connectivity layer and orbit-45/46 finite nulls

The known minimal-counterexample theorem gives a 4-connected branch, so
the orbit-44 full-colour CNF was augmented by every canonical quotient cut
for deletion sets of size at most three.  This adds 13,248 clauses.  The
result has 4,736,269 clauses and SHA-256
`2eaa8c3c08ea765bc1f28f9577487a6239fd2f6a52ef0b930c039748b01414ff`.
An independent reconstruction checks every deleted-set component quotient,
all cut clauses, exact clause order, and a fresh SAT solve; its artifact
has SHA-256
`1f427ad34fb1fd64a771062e389d016a78a1d9374d0ebe8acec6d8d66e943401`.
This layer applies only to the vertex-minimal-counterexample 4-connected
branch, not to every order-14 support.

An orbit-49 support outside the mandatory-core shortcut has an exact
16-variable, 10-clause relation selector with 64 inclusion-minimal
selections, all of size 10.  Complete radius-three closure excludes all 64
and expands to 9,216 verified full-colour clauses.  The clause-set and
independent verifier hashes are
`dab565ec60eedfe91956bfc7cd6a43147d22952511ca4e9d99760f09fa89a2a7`
and
`ad6953048c36e4da8501af6eb422e2d47d82adebd0e6cb0d7eccefdf1644daa5`.

On the 4-connected frontier, orbit 45 then supplied 30 mandatory-unit
support contradictions, all independently replayed and expanded under
full factor/colour symmetry.  They add 276,480 width-21 no-goods, producing
a 5,012,749-clause CNF with SHA-256
`3c32d426839bb1e802ea79156e6d3006dcd08d768bdc793ab111efe29975f298`.
The run manifest has SHA-256
`c343bab46035d2c9056ac00f17eaacc0f1c7c0018b11d56f2e5614fbe5ad9e2f`.
No new selector becomes UNSAT.

The orbit-49 support-2 theorem was then streamed onto that newer target
with source provenance unchanged.  All 9,216 clauses were new.  The
byte-reconstructed 5,021,965-clause output has SHA-256
`18efc986c32af2b358a585ca803b02e95f1ac041939d99e68df1a955e509c282`;
the independent materialization audit has SHA-256
`83702c2b40c2082af6cedf1b9cc644d4f75789214860b37416e7a391d4536bec`.
Its 93-selector audit still leaves the same 26 survivors and has SHA-256
`9797d9d67ca569528fd4da1e63acfb14f85a3d5b8f8a9054b8ad416261a20b2c`.

Orbit 46 supplied another 30 independently verified mandatory-unit
supports and 276,480 new full-colour no-goods.  Its 5,298,445-clause CNF
has SHA-256
`c1e0540f72649b8e73cafc055a1dd0df6df3f41f4e25c89ff80d296506692498`;
the run manifest has SHA-256
`3e2b0b5629af1fcd0dc6850a20baa68eeddb461b90419fe76a4cc9fde055de9e`.
A fresh all-93 audit again leaves exactly the same 26 selectors; its
SHA-256 is
`4de4d30403284d062b347e6f324782cc545eba4f38be2a07f0bfda28e0f047fe`.
These orbit-45/46 results are certified support exclusions and exact
finite nulls, not orbit theorems.

### Orbit 44 minimized replay, orbit 47 null, and orbit 48 support escalation

The orbit-44 theorem now has a second fresh replay from the minimized
24-clause top-level instance.  The complete record

```text
tmp/fourteen_vertex_c4_c4_c6_fullcolour_orbit44_core24_final_verified.json
```

has SHA-256
`1d0720cbaff4f4f12b119dda26f2cd338f2011badf47d75a5adf2845552130cb`;
its fresh forward `drat-trim` replay record has SHA-256
`b71b909e8285f0c15bf5bd78cdce7eeb68c6c1cca4be2a2a7f4770ca04a094af`.
This independently rebinds the same proof to the full 67/93 selector
census.

Orbit 47 supplied mandatory-unit support closures through support 30.
The run manifest and final 5.6-million-clause CNF have SHA-256
`01124ae3a943b37d88bda460aff5a483a48fe0ff0281335664b8387fb532ce28`
and
`77e1a58f34a0efb34f0b0f49c0bc248bcb3c81dbd153dc9db44ed8d1b35f60c7`.
Its all-93 audit has SHA-256
`af889bc1158a49d602e238b5b37fffb6d3a2be226c7e9da3f6af84b26f04ecdb`
and leaves the same 26 selectors.  The support verifier was extended to
reconstruct required unit amplitudes and mandatory-core survivors; its
source SHA-256 is
`f90e592aba9c3420803a6fbcad0134d4966e205631e97467a7378eb6504a977d`.
This is a finite null rather than a new orbit theorem.

Orbit 48 is harder.  Support 3 required exact enumeration of all 16
inclusion-minimal relation selections; fresh radius-three replay excludes
all of them.  The verified chain has SHA-256
`7bed7428d847a64498bbc22c79ddeea65f6325b86a61e26280c1f549b740ab92`,
and its 4,608-clause full-symmetry set has verified-artifact SHA-256
`05561dd3551bd5c714fae6c319bb10cdcf6304fd94da3838ebdc538327236357`.
Exact materialization and an all-93 audit again leave the same 26
selectors.

Mandatory cores then close supports 4 through 13.  Support 14 has 18
candidate relations and exactly 256 inclusion-minimal selections, all of
size 10.  Every branch fails a fresh radius-three replay; the complete
chain and its independent audit have SHA-256
`c34ae05a2a9cdef13b99cb91088683b4e72aaedcec077e9c1f1f3eddd5be6f24`
and
`5d8eaf4dcd69313be3800f632aa7e4126fbae9ea88fcadd42e84357fc66af79f`.
The resulting 9,216 clauses produce a 5,687,821-clause CNF with SHA-256
`e5200dce7ca64c777dba41fede096af4dbb69cf990d8550ce6c308e4763ec65a`;
the all-93 audit has SHA-256
`9d7bb20d28e38291b4f4a3da9310fc850286a7db74ee9749c84b7e0076d2db45`
and still leaves the same 26 selectors.

Supports 15 through 30 then all admit mandatory-unit cores and pass fresh
support and symmetry-materialization verification.  Their run manifest
has SHA-256
`e2e51bd6902d39e97d24a5d98638326cde1568cacd7d6f4c4ac9934dc3096741`.
The final 5,830,669-clause CNF has SHA-256
`fa00640a2abbd1883ee1a8fb666560fb9e6ed7b41c45ebae871ae04beb409570`;
the last independent materialization audit has SHA-256
`cdf119b99720b634cc41d52611bce83e5175dea1c4777bd8648eae5151ba2433`.
A fresh all-93 assumption audit again leaves exactly the same 26
selectors and has SHA-256
`5aa252fc7ce5642788b871e11307e18b9539b6741cc02ab56efe19ca19dc67e2`.

Supports 31 through 45 also all admit mandatory-unit cores.  The run
manifest has SHA-256
`72ec014b0c352b1999341af187c119d654f699d548db64c054a76ec3035431ad`;
the final 5,968,909-clause CNF has SHA-256
`68586d95916bf6ce0ed14fe173d6edcd4ca0d024fdf7b0e5000312f501fbbb52`.
The last independent batch-materialization audit has SHA-256
`782aed33d5d5c1d0f970e5043fdb679036cb8b389fd0332f50618e6dae40e1ce`.
A fresh all-93 assumption audit again leaves the same 26 selectors and
has SHA-256
`322ebb28725ae5bcccdf4f05916d95ece237b51babad233c95b778bc6645aef8`.

Supports 46 through 60 likewise all admit mandatory-unit cores.  The run
manifest has SHA-256
`8b48840e7516cbf3508edd61ab3a4ebdb2644539ec9efecf362d111572675bb1`;
the final 6,107,149-clause CNF has SHA-256
`d6bc21fdf95bbdc7120f4cbdfde91d51f9b346a5399c22dddfa5631ec490f6c5`.
The last independent batch-materialization audit has SHA-256
`0d73de3f739f406c7c6dfafdf14bd8004271ec609322ff51df0a28e0ad55c2c5`.
A fresh all-93 assumption audit again leaves the same 26 selectors and
has SHA-256
`0414286b07418bc6ea4ff893b9079c428fe2fb2530cb3bc9897361c11a1882d7`.
These are exact support exclusions and finite nulls, not a proof of orbit
48 or the global conjecture.

### Five-regular balanced-bridge diagonal backbone and hafnian cofactors

The simultaneous balanced all-bridge classification now yields an
arbitrary-order theorem for every hypothetical support of maximum degree
at most five.  Its three coordinate-primary killers at each vertex are
distinct off-diagonal singleton blocks.  Therefore the graph of edges
carrying diagonal entries has maximum degree two.  Each target
monochromatic amplitude supplies a perfect matching in this graph, so
every component is an even path or even cycle.

The unique perfect matching of an even path is common to all three
colours and joins complementary normal types.  On an even cycle, the
three colour matchings choose the two alternating parities.  In a `2+1`
split, a bit-incidence count

```text
2a + p = q,
p = q + 2b
```

forces `a=b=0`; hence every majority-parity edge flips all three type
bits and is complementary.  Thus the diagonal graph always contains a
spanning complementary-type anchor matching, with at least two nonzero
diagonal entries on every anchor edge.

There is a further arbitrary-length consequence.  For any fixed two
colours, the state `(anchor type, outgoing side, pair colour)` gives a
32-state directed automaton with 384 transitions.  Its eight strongly
connected components all have size four and each contains only one
colour.  Consequently every alternating cycle supported by a
pair-constant two-colour colouring is monochromatic.  If `V_c` is the
union of anchor pairs assigned colour `c` and
`L^c_ij=W_ij[c,c]`, the complete amplitude factors, without requiring
the anchor edges themselves to support the colouring, as

```text
T_W(g) = product_c haf(L^c[V_c]).
```

Because every anchor edge has at least two nonzero diagonal colours, the
one-pair-versus-rest partitions imply an additional exact constraint:
for every colour, every principal hafnian obtained by deleting one
anchor pair is zero, although the full principal hafnian is one.

The degree-two backbone then removes cancellation completely.  For any
proper subset of anchor pairs in a component, the induced diagonal graph
is a union of paths whose unique perfect matching consists of the selected
anchor edges.  A full-component factor is nonzero because the full
monochromatic hafnian is one and factors over the components of the
diagonal graph.  Finally, every anchor edge has a colour list of size at
least two.  Choosing distinct colours from two different lists extends
to all other pairs because every size-two subset of a three-colour set
meets that colour pair.  This produces a nonconstant two-colour
pair-colouring for which both principal-hafnian factors are nonzero,
contradicting the target coefficient zero.

The primary and independent audit outputs have SHA-256
`3fe977f5ecba23637fcd61a9b1dac29175542469b3da5720f6ef0e2b0a0b88c5`
and
`ca118d9b3a6b014d754d85685c5e3d467b8390c763233f28b4a55fea721aeaea`.
The theorem SHA-256 is
`3f9bb0ac2453539e6c4f642af3ef7c62b7e7cbe2caa896cc14cb863ca2d6bc87`.
Thus no simultaneous balanced all-bridge witness of maximum support
degree at most five exists at any even order `n >= 6`.  The global
conjecture remains open: a surviving all-bridge support must contain a
vertex of degree at least six, and the deeper-blocker branches remain
unresolved.

### Three-colour diagonal-matching bit balance

At the next diagonal-degree boundary, choose one nonzero perfect-matching
monomial `M_c` from each required monochromatic amplitude.  In the normal
type bit encoding, a diagonal colour-0 edge avoids `11` on bits 1 and 2;
a colour-1 edge avoids `11` on bit 0 and `00` on bit 2; and a colour-2
edge avoids `00` on bits 0 and 1.

Comparing the upper and lower perfect-matching incidence bounds forces
every bit to be one on exactly half the vertices.  Equality saturates
every matching edge:

```text
M_0 flips b1,b2,
M_1 flips b0,b2,
M_2 flips b0,b1.
```

An edge shared by any two matchings therefore flips all three bits, joins
complementary normal types, and carries both corresponding diagonal
weights.  If the three matchings are pairwise edge-disjoint, their union
is a properly three-edge-coloured cubic spanning graph; each colour edge
has Hamming distance two or three in type space.

Relative to any chosen `M_a`, a 64-state automaton for each pair of vertex
colours has 1,536 transitions and only monochromatic strongly connected
components.  Hence every pair-constant two-colour amplitude factors
relative to every monochromatic matching, without requiring its anchor
edges to support the pair colouring.  If `p` is an edge of `M_a`, colouring
`p` by `a` and every other vertex by `b != a` forces

```text
haf(L^b[V minus endpoints(p)]) = 0.
```

Thus the gradient of the full colour-`b` hafnian vanishes on both other
monochromatic perfect matchings even though the full hafnian equals one.

The same reconstruction with all three pair colours has 96 states, 2,880
transitions, and eight monochromatic strong components for each anchor
colour.  Hence the factorization holds for every pair-constant
three-colour partition, not merely the binary restrictions.

At the exact cubic diagonal boundary, suppose the three chosen matchings
are pairwise disjoint.  They exhaust the diagonal graph.  Expanding a
full colour-`a` hafnian at a vertex and using the two cross-cofactor zeros
leaves only its `M_a` term, whose cofactor is therefore nonzero.  This
forbids every extra diagonal colour on an `M_a` edge.  If
`M_a union M_b` had a proper alternating-cycle component, colouring that
component by `b` and its complement by `a` would then give two unique
nonzero factors.  Hence every pairwise union is Hamiltonian: this branch
is confined to a cubic perfect one-factorization, or Kotzig-type graph.

The primary and independent direct-restriction outputs have SHA-256
`b481fbbb95f14dfdb140d628ea8acd73700a825744690f38c9b9c3fd48e40c18`
and
`820fccaf6a25add3f0b520a6dbaa92e6cdc28a674c763d2f00cf3122e9146795`.
The theorem SHA-256 is
`1670832ef687379da26cf343a502cd80a8761e8e0f3264234eedb6015f166d43`.
This is an arbitrary-order structural theorem, not a complete exclusion of
the degree-three diagonal boundary or the global conjecture.

The same saturated table gives a further arbitrary-order sparsity normal
form.  After the cross-cofactor theorem removes the other two diagonals,
each `M_a` block has its forced `(a,a)` unit and at most one off-diagonal
unit.  For each matching colour, 2 of the 16 saturated ordered type
transitions are diagonal-only and 14 permit one optional off-diagonal.
Every such optional unit `(r,s)` satisfies

```text
f_i(s)=r,
f_j(r)=s,
```

so it is a reciprocal port-shaped transition.  In the exact
support-degree-six branch, the three primary killers exhaust the edges
outside the diagonal graph and are reciprocal at both endpoints.  Thus
the entire system is a cubic Kotzig diagonal graph with at most two units
per block plus a cubic singleton-port graph, with at most `9n/2` nonzero
matrix units.

The same exact eight-type table supplies a positive grading.  For a type
with bits `(b0,b1,b2)`, define

```text
q(0)=1-2b2,
q(1)=2(b2-b0),
q(2)=2(b0+b1-1).
```

Every forced own-colour diagonal transition has endpoint-potential sum
zero.  All 42 optional off-diagonal transitions have strictly positive
sum, with histogram

```text
potential 1:  6
potential 2:  4
potential 3: 22
potential 4: 10.
```

Choose a minimum-potential nonmonochromatic colouring induced by a
guaranteed matching.  Its potential is at most zero because the union of
the three differently coloured diagonal matchings has a nonmonochromatic
perfect matching.  If another matching for the chosen colouring used an
optional `D` unit, replacing that unit by the forced own-colour unit on
the same physical edge would give a guaranteed matching of strictly
smaller potential.  The new colouring would have negative potential and
hence remain nonmonochromatic, contradicting minimality.  Thus optional
`D` units are absent from every minimum-potential nonmonochromatic
guaranteed coefficient.

The remaining coefficient factors exactly.  For a fixed colouring, each
vertex sees at most one compatible forced `D` edge and one compatible
forced `K` edge, so every guaranteed filtered component has maximum
degree two.  Because the colouring has a guaranteed perfect matching,
its components are even paths and even alternating `D/K` cycles.  Paths
have one matching; each cycle contributes one binomial.  Therefore a
lowest-layer zero coefficient is a nonzero path product times cycle
binomials, and at least one alternating cycle must cancel.  Its `D` half
has total potential zero and covers the same vertices as its `K` half,
so the port-edge potential sum on every required cancellation cycle is
also zero.  This is an arbitrary-order localization to zero-potential
cycle binomials, not an arbitrary-order contradiction.

### Order-eight exact-degree-six Kotzig-port branch excluded

The singleton premise in the maximum-degree-five and exact-degree-six
arguments has been re-audited against its two analytic inputs.  The generic
killer proposition supplies a chosen nonzero block

```text
A_i^c transpose(e_c)
```

and proves that the three target colours use distinct neighbours.  In the
balanced all-bridge boundary, the normal-slice theorem makes every selected
`A_i^c` proportional to one of the two coordinate vectors different from
`e_c`.  Thus the chosen block really is the off-diagonal singleton
`(f_i(c),c)`.  The 64-pattern intersection theorem supplies reciprocity
after this singleton form is established; it is not being used to infer
singleton support from permissibility alone.

At order eight, now impose the exact-degree-six, diagonal-degree-three,
pairwise-disjoint matching branch.  The support splits into a cubic
diagonal graph `D` and a disjoint cubic reciprocal port graph `K`.
The three diagonal matchings partition `D`, every pairwise union is
Hamiltonian, and every normal-type bit has only two global assignments.

The five connected cubic classes contain respectively

```text
0, 6, 12, 0, 0
```

labelled perfect one-factorizations.  Across those 18 colourings, all
eight type assignments and all complement splittings
`complement(D)=K disjoint union U` give 2,016 port-graph tests.  Direct
pairing of the 24 `(vertex,target)` tasks leaves 72 reciprocal port
realizations.

For each realization, every permitted off-diagonal unit on `D` was added
before enumerating the 105 perfect matchings under all `3^8` vertex
colourings.  Every realization has a nonmonochromatic colouring with
exactly one compatible matching even in this maximal support, and every
unit in that matching is a forced nonzero own-colour diagonal or reciprocal
primary singleton.  Removing optional units cannot remove that monomial or
create a cancellation partner.  Hence all 72 realizations contradict the
zero target coefficient.

The primary and independent programs are

```text
explore_eight_vertex_degree_six_kotzig_ports.py
audit_eight_vertex_degree_six_kotzig_ports.py
```

The audit does not import the primary implementation.  It separately
decodes graph6, compares the five connected classes with the connected
part of the six-class nauty catalogue by brute-force isomorphism, enumerates
balanced four-subset bit masks, pairs reciprocal tasks, and rechecks every
mixed amplitude.  The primary and audit artifacts have SHA-256
`6b6c9fa2cb261fb894fc3bb4ee197cb9a16b9762d306ffd90788045b9864b4cf`
and
`905d51cad68b69c7871296300a325489c00d72ac84ea36c1cfb67ae627896456`;
the theorem SHA-256 is
`c163cecf01320d5f8e0831a24419a9d05f7fb5b00066b39594030d0264ed0fb3`.
Both report 72 contradictions and zero survivors.  This
is a finite exclusion of the stated order-eight branch only; overlapping
chosen matchings, degree-seven support, larger orders, and the deeper
blocker branch remain unresolved.

### Order-ten exact-degree-six Kotzig-port branch excluded

The same pairwise-disjoint exact-degree-six branch has now been exhausted
at order ten.  The nauty command

```text
geng -cq -d3 -D3 10
```

gives 19 connected cubic classes.  Ten classes admit the required
distinguished perfect one-factorization, with 102 labelled Kotzig
colourings in total.  Propagating the three balanced bits gives 816 type
assignments.  Direct exact-cover pairing of the 30 reciprocal port tasks,
with physical port edges simple and disjoint from `D`, gives 547,434
complete cubic port realizations.

The primary minimum-layer census enumerated 78,947,604 guaranteed perfect
matchings, of which 77,305,302 were nonmonochromatic.  Its result split as

```text
realizations with at least one unique minimum colouring: 547,042
minimum-layer residuals:                                  392.
```

The positive-potential theorem makes every unique minimum monomial a
direct contradiction: no optional `D` unit can contribute to that
coefficient.  Each of the 392 residuals has exactly one minimum colouring
and exactly two guaranteed matchings.  Its filtered graph has one
four-vertex alternating `D/K` cycle, and the port potentials on that
cycle sum to zero.  Thus these are genuine lowest-layer binomials rather
than missed singleton conflicts.

Relabelling colours gives six valid versions of the positive potential.
The identity residuals were recomputed under all five nonidentity
potentials.  Every residual has a unique minimum-layer colouring under at
least four of them:

```text
resolved by four nonidentity potentials: 270
resolved by all five:                    122
surviving all six:                         0.
```

The permutation fixing 0 and swapping 1,2 resolves 382; the swap of 0,1
resolves the remaining ten.  The primary and separately implemented
permuted-potential audits have SHA-256
`82dca38104a2be6af39ba1d96795ad15ac2993a8dba9fe2e14a7a749de47dd76`
and
`f52c387fce649cb0230e57823b942afc8f92dd40f5e1c6d12b387222e760ea7a`.
They check 35,280 diagonal zero-potential instances and 33,660 optional
strict-positivity instances.  The arbitrary-order symmetry statement is
`SIX_PERMUTED_POTENTIALS_LEMMA.md`, with SHA-256
`e73b7edc0281f8c6824f8e23d8d8a4f6a4f4ee8161501ea174a6a697b5f7c256`;
it narrows a witness to simultaneous survival of all six minimum layers,
but does not prove that impossible at larger orders.  Every nonnegative
nonzero combination of the six potentials is also valid, so the
replacement argument applies to a six-dimensional positive cone and to
all lexicographic refinements of its rays.  On the universal 24-state
local table the six columns are independent and have Gram matrix
`8 I_6 + 32 J_6`.  A larger-order witness must therefore keep
non-singleton minimum fibres at every cone-exposed colouring, not just at
the six individual ray minima.

As a second confirmation, for all 392 residuals every optional
off-diagonal unit allowed on `D` was restored simultaneously.  Each
maximal support still contains a different nonmonochromatic colouring
with exactly one compatible matching, and that matching uses only forced
own-colour diagonal or reciprocal singleton units.  Therefore removing
optional units cannot remove the monomial or create a cancellation
partner.  All 392 residuals are excluded, and the complete order-ten
finite branch has zero survivors.

The primary programs are

```text
explore_ten_vertex_degree_six_kotzig_ports.py
analyze_ten_vertex_degree_six_kotzig_port_survivors.py
analyze_ten_vertex_permuted_potential_survivors.py
audit_ten_vertex_permuted_potential_survivors.py
```

and the separate replay is

```text
audit_ten_vertex_degree_six_kotzig_ports.py.
```

The primary census and survivor-analysis artifacts have SHA-256
`b314c1691afcc1fb131c4e1eb44a37b61248ea498ebc998a1129c1c4fb3f61a1`
and
`e2ada391865290c13a3f7c0ac8b2160018d64392b91d5b8a1c7f0464bed8de36`.
The independent full audit has SHA-256
`ac3eeb46b878b29ce661e1d90e74293bd03e55fc03a522bb47fb99cab4508ea3`;
the finite theorem document has SHA-256
`fe53381d82d2041242f067f5a99a3e7f46a8782c8d9c1537f03eba1a2251f57f`.
This is a finite exclusion of the stated order-ten branch, not a result
for overlapping chosen matchings, order twelve, or the global conjecture.

### Order-twelve six-potential cell scout

A first order-twelve scout has been materialized without claiming a
catalogue exclusion.  The complete nauty connected cubic catalogue has 85
classes; 31 admit the required distinguished factorization, with 336
labelled Kotzig colourings and 2,688 normal-type cells.  For each cell the
scout constructs only the first deterministic reciprocal cubic port
realization, when one exists.  It found a port realization in 2,580 cells
and none in 108.

All 2,580 selected realizations have a unique minimum-layer guaranteed
colouring under at least three of the six permuted potentials:

```text
successful potential rays 3:    4 cells
successful potential rays 4:    9 cells
successful potential rays 5:   40 cells
successful potential rays 6: 2527 cells
surviving all six rays:          0 cells.
```

The artifact
`tmp/twelve_vertex_six_potential_cells_scouted.json` has SHA-256
`9cb74f95d00111bf0e8a977793dca445b956d63ad7458470b8bc8decd59c5631`;
the source `scout_twelve_vertex_six_potential_cells.py` has SHA-256
`96bdf827dbc0dd56506a30674881c848c8a129d395164e0802880098569d45f9`.
This is explicitly one port realization per feasible type cell.  It does
not enumerate the other reciprocal port graphs, does not exclude the
order-twelve branch, and is only evidence that the six-potential filter is
a promising first-stage reducer there.

### Orbit-48 mandatory supports 61--75

The orbit-48 full-colour support continuation now reaches support 75.
Every support from 61 through 75 has a mandatory-unit binomial
contradiction and passes the independent support and full-symmetry
materialization verifiers.  The final checkpoint has 6,245,389 clauses.
A fresh 93-selector CaDiCaL assumption audit again returns the same
67 UNSAT and 26 SAT selectors.  The run manifest, final CNF, final
batch-materialization audit, and all-93 audit have SHA-256
`2f8317172598ff85d5197b287d1251bba6edc931bc005d82020991ddd501f127`,
`ae0adc61aa9ac6d17a2af6ee6cf7db65feda56ab1d06c77733201e6f9cb8cd7b`,
`38af57ad2570e03332acef6c94ffbc6fe393a76afd2360d5ddd55dc47145a10e`,
and
`2fb4064261a28d752306bd655e8a59881bb997c78ba2d7d27f978a2ab62f8724`.
This is a certified collection of finite
support exclusions and an exact null at the current CNF layer, not an
orbit-48 theorem or a global proof.

### Complete admissible potential cone

The six colour-permuted potentials used in the order-ten and initial
order-twelve work are now proved to be a basis of the complete local
potential space neutral on forced own-colour diagonal transitions.  The
24-state neutrality matrix has exact rank 18 and nullity six.  The 42
permitted optional transitions reduce to nine distinct inequalities in
that basis.

The earlier nonnegative coefficient orthant is a proper subcone.  The
closure of the full admissible cone is simplicial with extreme rays

```text
(-4, 1, 1, 1, 6,-4)   (-4, 1, 6, 1, 1,-4)
( 1,-4, 1, 1,-4, 6)   ( 1,-4, 1, 6,-4, 1)
( 1, 6,-4,-4, 1, 1)   ( 6, 1,-4,-4, 1, 1).
```

If `R` has these columns and `W` is the nine-row inequality matrix,
every entry of `W R` is nonnegative and six rows are exactly
`10 e_0,...,10 e_5`.  Since `R` has rank six, this is an exact
two-direction cone certificate: `W lambda >= 0` iff
`lambda=R mu` with `mu>=0`, and strict positivity iff every `mu_i>0`.
The rays sum to the strict interior direction `(1,1,1,1,1,1)`, so each
boundary ray admits a valid extreme-first/interior-second lexicographic
refinement.

After division by five the local values are Boolean.  With
`s_i=(-1)^b_i`, the six colour triples are

```text
( s1, s2,-s1)  ( s1,-s0,-s1)  ( s2,-s2, s1)
( s2,-s2, s0)  (-s2, s0,-s0)  (-s1, s0,-s0).
```

The arbitrary-order statement is in
`FULL_ADMISSIBLE_POTENTIAL_CONE_LEMMA.md`.  Exact reconstruction is in
`verify_full_admissible_potential_cone.py` and
`tmp/full_admissible_potential_cone_verified.json`.  A separate symbolic
audit enumerates every five-facet intersection and independently
recovers exactly the same six extreme rays in
`tmp/full_admissible_potential_cone_audited.json`.  This strengthens the
grading only inside the pairwise-disjoint exact-cubic diagonal branch;
it does not resolve the overlapping-matching or global cases.

### Order-twelve exact-degree-six Kotzig-port branch excluded

The complete order-twelve pairwise-disjoint exact-degree-six branch is
now excluded.  The 85 connected cubic classes contain 336 labelled
distinguished Kotzig colourings and 2,688 propagated normal-type cells.
Quotienting by graph automorphisms and global colour permutations gives
154 cells, four without a port realization.  Exact-cover enumeration
gives

```text
representative reciprocal port realizations:  15,478,610
orbit-weighted labelled realizations:        281,720,460.
```

The original six rays give the success-count histogram

```text
successful rays 0:       395
successful rays 1:     1,266
successful rays 2:     4,754
successful rays 3:     8,522
successful rays 4:    33,641
successful rays 5:   118,323
successful rays 6: 15,311,709.
```

The 395 residuals are all exposed by the full-cone extreme/interior
refinements:

```text
successful refinements 2:   1
successful refinements 3:   3
successful refinements 4:  75
successful refinements 5: 120
successful refinements 6: 196.
```

There are zero full-cone residuals.  As a stronger-support confirmation,
adding every permitted optional diagonal unit still leaves a different
nonmonochromatic forced singleton in every one of the 395 architectures.

The primary compiled pass and a separately written compiled audit agree
exactly in every cell on the port count, survivor count, all 64
success-mask counts, port hash xor and sum, and classification hash xor
and sum.  The separate Python audit reconstructs all 395 residuals,
replays the old and new gradings, and directly counts each maximal-support
singleton.  Another audit independently decodes graph6, enumerates
perfect matchings and Kotzig colourings, propagates normal bits, and uses
NetworkX automorphisms to recover all 2,688 cells, 154 orbits, orbit
sizes, and stabilizers.  Its artifact
`tmp/twelve_vertex_port_cell_orbits_audited.json` has SHA-256
`2c8dc39dd3d98385287c63c99cf105dde2e17139084d71ef62ce973a52b850da`.
The finite theorem and scope boundary are in
`TWELVE_VERTEX_DEGREE_SIX_KOTZIG_PORT_OBSTRUCTION.md`.  This closes order
twelve only under the pairwise-disjoint exact-degree-six hypotheses; it
does not close order fourteen, overlapping chosen matchings, higher
support degree, or the global conjecture.

### Order-fourteen first-port cone scout

An explicitly exploratory order-fourteen continuation enumerates the
complete 509-class connected cubic catalogue, all 2,460 labelled
distinguished Kotzig colourings, and all 19,680 propagated normal-type
cells.  A reciprocal cubic port graph exists in every cell.  Only the
first deterministic port realization is tested in each cell.

All 19,680 selected architectures are exposed by both grading families:

```text
successful original rays 3:    21
successful original rays 4:    60
successful original rays 5:   171
successful original rays 6: 19,428

successful full-cone refinements 3:     2
successful full-cone refinements 4:   121
successful full-cone refinements 5:   308
successful full-cone refinements 6: 19,249.
```

The artifact
`tmp/fourteen_vertex_full_cone_cells_scouted.json` has SHA-256
`4d0e0819808a27640a573b368be3b137548201b8e6b38423fe6b4daf36e1b849`;
the source `scout_kotzig_full_cone_cells.py` has SHA-256
`0ecfa14dcb4a6b95d97bc9035db42e4b3fc0b27c015744b4db61065754758978`.
The test is complete for graph/factorization/type cells and incomplete
for port graphs.  It is not an order-fourteen theorem and must not be
reported as one.

A second seeded search samples 25,000 distinct randomized reciprocal
exact covers across uniformly selected cells.  It finds one architecture
that survives all six original rays and one additional architecture
exposed by only one original ray.  The new extreme family exposes every
sample:

```text
original-ray residuals:             1
extreme-refinement residuals:       0
combined twelve-direction residuals: 0.
```

The old-ray residual at sample 16,245 is exposed by five of the six new
directions, demonstrating that the full cone is already strictly useful
at order fourteen.  The random-search artifact has SHA-256
`825bc91a6c62f0bca9d5a81fc500fd4c1e6c2994fb51b6d37da91fb9123894ed`;
the source has SHA-256
`2fe2b34979a22caebc2d24de55dbd817117fac24e3fa3b83dcbedb35b745b9e6`.
This remains nonuniform randomized evidence, not domain coverage.

### Lifted state-cycle formulation of guaranteed fibres

The pairwise-disjoint exact-cubic branch has a useful arbitrary-order
state lift.  On the `3n` states `(vertex,colour)`, the own-colour
diagonal matchings define one fixed-point-free involution and the
reciprocal port cover defines another.  Their union is a disjoint
alternating cycle cover.  A physical colouring selects one state from
each vertex triple, and its compatible guaranteed graph is exactly the
induced subgraph of that lifted cycle cover.

Consequently every feasible colouring fibre has exactly `2^r` matching
monomials, where `r` is the number of entire lifted components contained
in the selected transversal.  A guaranteed colouring is a singleton iff
it avoids every full lifted component.  Components repeating a physical
vertex can never be fully selected, so only injectively projected
transversal cycles matter.

Every neutral potential sums to zero on each lifted component.  Under a
Boolean full-cone extreme direction, each component has equally many
positive and negative states.  If an extreme-minimum colouring contains
fewer positive states than half the shortest transversal lifted cycle,
it is therefore a singleton.  On the 395 hard order-twelve architectures
the transversal lifted girth is always four; this simple count closes
seven architectures, while the full cycle-avoidance mechanism is needed
for the rest.

`STATE_LIFT_CYCLE_FIBRE_LEMMA.md` has SHA-256
`f3cbb0b2ba8fcfef1e24dff7c308631e38fd31939e82867f14d42a8a1ed549a0`.
The finite regression checks all 130,581 feasible fibres and is stored in
`tmp/state_lift_cycle_fibres_verified.json`, SHA-256
`42f20b43827c838dfb0e6cac5e34fde790cc34bd47efdf8f0e0715c5325d568d`.
This is a structural reduction, not the missing arbitrary-order
cycle-avoidance theorem.

### 26 July 2026 port correction and arbitrary-order replacement

This section supersedes the preceding order-eight, order-ten,
order-twelve, order-fourteen-port, and lifted-state-cycle entries.  Those
calculations paired reciprocal *target tasks* correctly but emitted the
task labels as inherited half-colours.  If target `c` at `u` is paired
with target `r=f_u(c)` at `v`, the physical unit on oriented `uv` is
`(r,c)`, not `(c,r)`, and it must separately pass the complete
balanced-bridge table.

The corrected local census is

```text
reciprocal target-task transitions: 96
admissible physical port units:     72
reciprocal but bridge-forbidden:    24

physical-port potential 1: 24
physical-port potential 2: 16
physical-port potential 3: 24
physical-port potential 4:  8.
```

Thus every admissible physical port has strictly positive base
potential.  The exact convention, the legacy diagnostic, and its replay
are in `RECIPROCAL_PORT_ORIENTATION_CORRECTION.md` and
`verify_reciprocal_port_orientation.py`.  Their current SHA-256 values
are

```text
RECIPROCAL_PORT_ORIENTATION_CORRECTION.md
  ec6c3ed3f4692a7e91a39b002ef7d37066242e33fee1add5c11bf34316dcc34c
tmp/reciprocal_port_orientation_corrected.json
  2dce83453b7765bbd573796d5691de8cd83428004fb1bcac38641b7b0f122ee7.
```

The correction closes the complete pairwise-disjoint exact-degree-six
branch at arbitrary even order.  Its diagonal graph is properly
three-edge-coloured by the selected matchings.  Bogdanov's theorem,
reported as Theorem 1.7 in Chandran--Gajjala--Illickan, supplies a
nonmonochromatic perfect matching in that graph for `n>4`.  Its forced
diagonal units have potential zero.  Every optional diagonal and
corrected physical-port unit has positive potential, so no competing
monomial for the induced colouring can use one.  Proper edge-colouring
makes the forced matching unique, contradicting the required zero
coefficient.  The theorem and two independent local-table artifacts have
SHA-256

```text
ARBITRARY_ORDER_DEGREE_SIX_KOTZIG_PORT_OBSTRUCTION.md
  02601a7a8959f76c0197174efc191a21e775334a5e7c54a820a388a82cb63c3c
tmp/arbitrary_order_degree_six_kotzig_port_obstruction_verified.json
  a428a5f1ee470f54b157646290b22f129ea97b3e3975bbbb958437a0d1806fb7
tmp/arbitrary_order_degree_six_kotzig_port_obstruction_audited.json
  3c9c054effe66f6a7a72e66b1a6b2aec3095bd010bdd3d005522e29e1dddfdc2.
```

Fresh finite regressions agree with the arbitrary proof:

```text
order 8:
  labelled Kotzig colourings                    18
  normal assignments                          144
  unused-matching/port tests                 2,016
  admissible physical port covers                0

order 10:
  labelled Kotzig colourings                   102
  normal assignments                           816
  admissible physical port covers          374,544
  identity-potential contradictions        374,544
  residuals                                      0

order 12:
  labelled Kotzig colourings                   336
  labelled type cells                        2,688
  cell orbits                                  154
  zero-port cell orbits                        109
  representative admissible covers         51,168
  orbit-weighted labelled covers           860,250
  success mask 63                           51,168
  residuals                                      0.
```

The corrected finite artifacts have SHA-256

```text
tmp/eight_vertex_degree_six_kotzig_ports_explored.json
  5bdc097c8056957fb91ba4fb240bb33214fde092d19c133438d40e5e2d2dcf57
tmp/eight_vertex_degree_six_kotzig_ports_audited.json
  0272db28ac25bc66a14cd14ca4f18665fade49e9d768b8c465eadf3eb92213ed
tmp/ten_vertex_degree_six_kotzig_ports_explored.json
  ec1fd089798fd148d8e8ee2a8616a28feba9df2670975138fab4b93f371cc482
tmp/ten_vertex_degree_six_kotzig_port_survivors_analyzed.json
  5f5264caeeb109c539f66968e29989402ce704c098a3afe0ede3d100e87d9d7b
tmp/ten_vertex_degree_six_kotzig_ports_audited.json
  ea677545a0397dfb4514f963a1aa880393948caf744bd97668d175e537005ebc
tmp/twelve_vertex_port_cell_orbits_counted.json
  5d331c86d741dffaf158b39dba0892bbf165f459b87717045409507f5c0e95f9
tmp/twelve_vertex_port_cell_orbits_audited.json
  48129e37e9936f29ebbcb72dda2a94e92f4dbd49128a0656aedf4d267ba7a9ae
tmp/twelve_vertex_port_cell_orbits_input.txt
  16cae007ed5fc348f7f57eec72e85d7f479476cf0ec714ad4f0702e890ec639f
tmp/twelve_vertex_six_potential_orbits_exhausted.json
  e408a7c115a255f7f98e46e5f37618a1b6174421ad6391375282abd99877e2e3
tmp/twelve_vertex_six_potential_orbits_residuals.tsv
  e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
tmp/twelve_vertex_six_potential_orbits_independent_audit.tsv
  30ec1b5a573532a6b1d06b101c9df57ae81268e4de4b9839e725f28ae85b67dd
tmp/twelve_vertex_six_potential_orbits_independently_audited.json
  c2d2448efde6f81033194f46ac60d05c5fa292a16463b289e53bbf6a78e30b7b.
```

The former `STATE_LIFT_CYCLE_FIBRE_LEMMA.md` is withdrawn: a normal map
`c -> f(c)` need not be a permutation of the three physical colours, so
target-task pairing does not define the asserted involution on physical
vertex-colour states.  The old order-fourteen port scouts used the same
convention and are also withdrawn.

### Universal saturated-diagonal zero layer

Summing all six colour-permuted potentials gives a stronger,
support-degree-free reduction in the complete simultaneous balanced
all-bridge branch.  Across all 180 permitted oriented units, every one of
the six rays is separately nonnegative.  Their sum `Q` has exact
histogram

```text
Q edge potential  0: 48
Q edge potential 10: 96
Q edge potential 20: 36.
```

The 48 zero units are exactly the saturated monochromatic diagonal
transitions; no bichromatic unit is zero.  The three selected
monochromatic matchings lie in this zero layer.  Bogdanov's theorem
therefore produces a nonmonochromatic zero-layer matching in every
hypothetical all-bridge witness.  Any monomial inducing the same
colouring has total `Q`-potential zero, so it too can use only saturated
diagonal units.  Since the selected monomial is nonzero while the target
coefficient is zero, at least one other zero-layer matching and a
monochromatic alternating cancellation cycle are forced.

This does not yet exclude the overlapping or higher-support branches:
it localizes all their lowest-layer destructive interference to
saturated diagonal principal hafnians.  In particular, a selected edge
shared by colours `a,b` forces both complementary colour cofactors to
vanish despite containing the corresponding selected matching monomial.
The theorem and independent artifacts have SHA-256

```text
UNIVERSAL_SATURATED_DIAGONAL_ZERO_LAYER_THEOREM.md
  717acdd6f3380d5d13e01af827076647af9718dd54da606ff04f7ec0cf52cf98
tmp/universal_saturated_diagonal_zero_layer_verified.json
  7222e0f20486598bbf23b0a30718f617b6807ece375e5cec16b14fd22ad6bbdc
tmp/universal_saturated_diagonal_zero_layer_audited.json
  90eeb0709e9613c9a5808f37a393f29cd2fd62951bf7f622d77772f407c6bc92.
```

The global conjecture remains unresolved.  The next all-bridge target is
the representability and forced-intersection structure of these three
saturated-diagonal cancellation families; the separate deeper-blocker
alternative also remains open.

### Withdrawn overstrong order-eight set-tree exclusion

**WITHDRAWN.**  The calculation recorded in this historical section
forbade set partitions that reused a tree colour.  That multiplication
step is invalid: same-colour edges can cross between the proposed
blocks, so their two principal hafnians need not multiply to the
principal hafnian of the union.  The hashes and counts below identify
the withdrawn artifacts only.  The sound replacement is recorded after
the order-ten historical section.

The saturated-diagonal reduction admits a stronger finite closure at
order eight.  For each colour `c`, put

```text
T_c = {nonempty even U : haf(Z^c[U]) != 0}.
```

Hafnian expansion at any vertex makes `T_c` a set tree.  Every member
also obeys the saturated transition balance: on the two normal bits
other than `bc`, its `00` and `11` type counts agree and its `01` and
`10` counts agree.  The three trees must be incompatible, since a
partition of the vertices into nonzero blocks from at least two colours
would have a nonzero factorized zero-layer coefficient.

There are exactly 57 balanced multiplicity profiles of the eight normal
types on eight vertices.  A complete Boolean encoding introduces
variables only for colour-balanced subsets, asserts the set-tree
expansion axiom with Tseitin partner witnesses, and forbids every
differently coloured even set partition.  All 57 local formulas are
UNSAT in CaDiCaL 1.9.5.  A separate implementation enumerates profiles
in reverse, uses restricted-growth set partitions and reversed partner
orders, and independently obtains 57 UNSAT results in Glucose 4.

The combined selector CNF has

```text
variables:  55,494
clauses:   178,924
profiles:       57.
```

Kissat reports UNSAT and writes a 1,923,776-byte DRAT proof.  Independent
forward replay by `drat-trim` returns `s VERIFIED`, with 54,655 original
clauses and 11,246 lemmas in the checked core.  The principal hashes are

```text
EIGHT_VERTEX_BALANCED_ALL_BRIDGE_SET_TREE_OBSTRUCTION.md
  d322d13a556e3f70ed2db8a89eef844ccf52b9c0692ad3368ae7bb47d23e78ea
tmp/eight_vertex_balanced_set_trees_certified.json
  fd1e16d102c8a83d6a172423c30b9889a13ec5a140e8d900e99946a97b22877c
tmp/eight_vertex_balanced_set_trees_all_profiles.cnf
  3b9ec7043e2d56dd3100f96d663f809398be62d8f563eb2a9081fa3f5364cd76
tmp/eight_vertex_balanced_set_trees_all_profiles.drat
  9ab9e3ecbf1042c79b6487e46df79c4515bde72148ddf0acb42db668b0920cb9
tmp/eight_vertex_balanced_set_trees_kissat_run.json
  1456d10284f75585df01e7e878851fb539c194c77877b97270194150df5ebe23
tmp/eight_vertex_balanced_set_trees_drat_replay.json
  9dee2e5f003f5954458029bc8f5a261cd0adef978807081927a639097187f117
tmp/eight_vertex_balanced_set_trees_audited.json
  871e600ac3c0ae58c97ff8a475e922a0e13490f1cd1578a1f0e13e26332a5298.
```

This excludes every order-eight simultaneous balanced all-bridge
witness without a support-degree or matching-disjointness hypothesis.
It does not exclude the separate deeper-blocker branch, so the complete
order-eight and global conjectures remain unresolved.

### Superseded overstrong order-ten set-tree certificate

**SUPERSEDED.**  This historical certificate used the same repeated-colour
clauses as the withdrawn order-eight calculation.  Its conclusion
survives after deleting those clauses, but none of the counts, hashes, or
proof files in this section are current evidence.  The corrected
certificate is recorded below.

The same constrained set-tree argument closes the entire order-ten
simultaneous balanced all-bridge branch.  There are 104 balanced
normal-type multiplicity profiles.  Independent flips of the three bit
coordinates and coordinate permutations preserve every subset-balance
condition, set-tree axiom, and incompatibility clause.  The resulting
48-element cube action has 10 profile orbits.

The primary generator decides all 10 orbit formulas UNSAT with CaDiCaL
1.9.5.  The independent audit reverses the profile, coordinate, subset,
and partner enumerations, generates the 6,555 even set partitions by
restricted-growth strings, independently recovers the same 104 profiles
and 10 orbits, and decides all 10 formulas UNSAT with Glucose 4.

The combined selector CNF and proof have

```text
variables:   49,216
clauses:    308,959
orbits:          10
DRAT bytes: 7,044,511.
```

Kissat returns UNSAT.  Independent forward `drat-trim` replay returns
`s VERIFIED`, with 154,395 original clauses and 81,941 lemmas in the
checked core.  The principal SHA-256 values are

```text
TEN_VERTEX_BALANCED_ALL_BRIDGE_SET_TREE_OBSTRUCTION.md
  a1ad3d797e0c63c4e62e36b6b8d261c3551cadc6fd6531a62faec82626f93a8a
tmp/ten_vertex_balanced_set_trees_certified.json
  8f97b1ef0c307b1b6f756c32879d7ce221153b42799ce3ca71bfb05faecdbe15
tmp/ten_vertex_balanced_set_trees_all_orbits.cnf
  7cd5881859e5d88213a01c9d2c8f69900a78393af9cf5b1e38ffa27a627ab6fd
tmp/ten_vertex_balanced_set_trees_all_orbits.drat
  e6c74dd3a4f5eb30671277f79340a72cdba5a92f4d7857f437e7613b1422c35b
tmp/ten_vertex_balanced_set_trees_kissat_run.json
  8b284d8d8885ab219c71e119b5fae4cabe3e036c960c711ed10c82ffc309fe87
tmp/ten_vertex_balanced_set_trees_drat_replay.json
  4867b93f5f753f3c944950a4453a5e4820fe29464cf057e8f960dde435e972f8
tmp/ten_vertex_balanced_set_trees_audited.json
  de132a875e0049c7fa068187988adab2895531ef7da9a3a441590c24d1f5391d.
```

This exclusion has no support-degree or matching-disjointness
hypothesis.  A remaining order-ten witness must enter the separate
deeper-blocker alternative.  The complete order-ten and global
conjectures remain unresolved.

### Corrected order-eight balanced all-bridge exclusion

Restricting the set-tree incompatibility clauses to partitions of two or
three blocks assigned to pairwise distinct colours changes the order-eight
classification.  The 57 balanced profiles form eight cube-symmetry
orbits.  Seven corrected formulas are UNSAT and cover 55 profiles; the
one SAT orbit is

```text
(0,2,2,0,2,0,0,2)
(2,0,0,2,0,2,2,0).
```

The combined corrected CNF for the seven excluded orbits has 7,280
variables and 17,590 clauses.  CaDiCaL and an independent Glucose
encoding agree on all eight orbit statuses.  Kissat's 86,018-byte proof
is accepted by forward `drat-trim` replay, whose core uses 6,406 original
clauses and 1,304 lemmas.

The abstract SAT orbit is not realizable by saturated diagonal
hafnians.  Taking the odd profile, each colour graph is two disjoint
`K_2,2` components:

```text
colour 0:  1--7, 2--4
colour 1:  1--4, 2--7
colour 2:  1--2, 4--7.
```

The required full colour hafnians force all six component permanents
nonzero.  Among the 6,558 nonmonochromatic vertex colourings, 6,510 are
structurally zero and 48 reduce to products of those nonzero permanents
and singleton edge weights.  Their zero requirements, together with the
six component-perfect-matching requirements, form a 24-variable,
72-clause necessary support CNF.  It is UNSAT; Kissat's 729-byte DRAT
proof replays with a 56-clause, 24-lemma core.  A separate enumerator
tests all `7^6 = 117,649` component support products and finds zero
survivors.

Principal SHA-256 values are:

```text
EIGHT_VERTEX_BALANCED_ALL_BRIDGE_SET_TREE_OBSTRUCTION.md
  1ea9d0e66eae64d617e823ab3817197eefb04f2e71b50afa1c4bc3292ac36f8f
tmp/eight_vertex_balanced_set_trees_excluded_orbits.cnf
  2f4c22243261624a4f025149c55bd67a01d1995cc92a7776f3a5539bd25f6e38
tmp/eight_vertex_balanced_set_trees_excluded_orbits.drat
  c716284786d03ffd9ddb4b7a6ae14a8ee9831e922ab66539fdb0286893c0e551
tmp/eight_vertex_balanced_set_trees_audited.json
  da70dd404b12d2e1175a16205dba6f03eaed96b89c3fa2076116a437a47a2b16
tmp/eight_vertex_parity_hafnian_supports.cnf
  026ecf7128b1bf9b93f2aa98f93183dd393617fb1d0e7d29aa8ade643beb4896
tmp/eight_vertex_parity_hafnian_supports.drat
  065a9e775548c3ca262932a23608034cb6ef756729df62fc599e0a4b654cb512
tmp/eight_vertex_parity_hafnian_supports_audited.json
  16b66b5497d6753559bf7402c87d96d04596205532251e81926f9895d73920d2.
```

Thus no order-eight witness exists in the simultaneous balanced
all-bridge branch.  The separate deeper-blocker alternative remains.

### Corrected order-ten balanced all-bridge exclusion

After restricting incompatibility to injectively coloured two- or
three-block partitions, all 10 order-ten cube orbits remain UNSAT.  The
primary enumeration uses 2,460 eligible even set partitions.  An
independent restricted-growth implementation recovers the same 104
profiles, 10 orbits, and 10 UNSAT decisions.

The corrected combined CNF has 49,216 variables and 122,539 clauses.
Kissat's 39,164,774-byte DRAT proof is accepted by forward `drat-trim`
replay, whose core uses 76,326 original clauses and 666,962 lemmas.
Principal SHA-256 values are:

```text
TEN_VERTEX_BALANCED_ALL_BRIDGE_SET_TREE_OBSTRUCTION.md
  e6985f254964def68e86d71d20525308646c1a7f56627c178f787bb982c8a5e3
tmp/ten_vertex_balanced_set_trees_certified.json
  0ac33b5a3b2972099167f6a43484832ef6f2e27ae33861a452ef0fd0e2973cf4
tmp/ten_vertex_balanced_set_trees_all_orbits.cnf
  6cc999351933dc04f919c5c9059e85388408760c2bc0ad80ff72627ab7d3d103
tmp/ten_vertex_balanced_set_trees_all_orbits.drat
  0aff4b29c59c9bfe60a6583b80f172491408c1d4bc13c416bf1ae389ba2e9dee
tmp/ten_vertex_balanced_set_trees_drat_replay.json
  9b94d2b93a9ed0f1a735ea3101ab5f9b92b67f5c14dd482ca4c27d0c872406a6
tmp/ten_vertex_balanced_set_trees_audited.json
  bdc21533ddcc5544e70234e165cff0bb9e4db668303b41713e3af9fa709c29a8.
```

This restores the complete order-ten simultaneous balanced all-bridge
exclusion on sound clauses.  The deeper-blocker branch and global
conjecture remain unresolved.

### Hafnian convolution-split representability

For a symmetric matrix `L` on `2m` vertices, coefficientwise expansion
gives the arbitrary-order identity

```text
sum_(A subset V, |A|=2k)
  haf(L[A]) haf(L[V-A])
= binomial(m,k) haf(L).
```

Every full perfect-matching monomial occurs once for each choice of `k`
of its `m` edges.  Therefore, whenever a principal hafnian on `V` is
nonzero, at every intermediate even size there is a complementary split
`A,V-A` for which both principal hafnians are nonzero.

This is a sound strengthening of the set-tree abstraction.  It does not
factor same-colour blocks inside a forbidden coefficient; it uses a
nonzero convolution sum only to infer that at least one summand is
nonzero.  Iteration supplies partitions into nonzero same-colour
principal hafnians for every prescribed even block-size composition.

There is also an exact colour-exclusive consequence.  If all three
full-colour hafnians are nonzero and every mixed complementary product
vanishes, then for every colour and every split size, at least one
nonzero same-colour split has a zero factor in each of the other two
colours.  In particular, each colour has a saturated edge whose edge
and complementary cofactor are nonzero in that colour but whose
edge/cofactor product vanishes in both other colours.  This is
arbitrary-order and does not assume degree six or disjoint selected
matchings.

Two independent enumerators check every coefficient through order 12,
including all 10,395 perfect matchings at the largest order.  Principal
SHA-256 values are:

```text
HAFNIAN_CONVOLUTION_SPLIT_LEMMA.md
  7a0d7dccfc8b5f1ab7dbc9256de97e53cf8aa87cbf389543cec6a7fe59526210
tmp/hafnian_convolution_split_verified.json
  9de9b0fcb7c7565bb37888dc1dd0e262fcbe4f002b2e7a932f34420cc69635d2
tmp/hafnian_convolution_split_audited.json
  8fdc66c11b122ece8c6d6335f0bad6fdf3e932c4ac35370d8efd26e4e557b2f9.
```

The corrected order-12 complement-profile experiment now includes these
all-size split axioms.  That finite decision remains exploratory; this
section claims only the arbitrary-order identity and its necessary
nonzero-family consequence.

### Multi-star blocker surplus and exact factorisation

The double-star obstruction extends to an arbitrary zero-coupled root
set.  Let `R` contain `r >= 2` roots carrying vectors with nonzero
colour-`c` coordinates, and suppose every internal root contraction is
zero.  At an outside vertex `u`, call `u` a blocker when the colour-`c`
coordinate functional lies in the span of its `r` root covectors.

There must be at least `r` blockers.  Otherwise put every nonblocker in
the simultaneous kernel of its root covectors with nonzero `c`
coordinate, and put the blockers at `e_c`.  If there is no blocker, use
one arbitrary outside vertex as an `e_c` marker.  Fewer than `r`
exceptional vertices cannot receive all `r` roots in a perfect matching;
one root edge is killed, while the target retains a nonzero pure
colour-`c` product.

When the lower bound is tight, with blocker set `U` of size `r`, the
surviving perfect matchings factor exactly.  Every root must pair
bijectively with a blocker, while all remaining vertices match among
themselves.  If

```text
C_(i,u) = B_iu(x_i,e_c),
```

then the matching side is

```text
per(C) H_(V minus (R union U)).
```

The target identity forces `per(C) != 0` and forces the residual tensor,
on the simultaneous nonblocker kernel spaces, to be a nonzero pure
colour-`c` product.  Thus a deeper root pair has an exact alternative:
either it has a third blocker or its two blockers reduce the problem to
a pure `(n-4)`-vertex minor.

Allowing the blocker vectors to vary gives more.  The full
root--blocker permanent tensor times the residual matching tensor equals
the sum of the three diagonal blocker-coordinate tensors times the
three residual colour products.  Since the residual tensor is already
a nonzero pure `c` product, every active residual colour product is
collinear with it and every mixed root--blocker coefficient vanishes.
For two roots this makes the `2 x 2` root--blocker coefficient matrix
diagonal with rank at most two.

The arbitrary-order proof is in
`MULTI_STAR_BLOCKER_FACTORISATION_LEMMA.md`.  Independent finite checks
enumerate or dynamically count every factor case through order 12,
including all 10,395 perfect matchings at the largest order.  Principal
SHA-256 values are:

```text
MULTI_STAR_BLOCKER_FACTORISATION_LEMMA.md
  3f39439a2d191821435a2d05342548337004eeea4b6ebfa134fb87408999bcc4
tmp/multi_star_blocker_factorisation_verified.json
  40698f1c9886a3c2e268f570627cca20576c4bab082a20bb720232ed772c017f
tmp/multi_star_blocker_factorisation_audited.json
  f748ba5dc7a6da45d6a389f9d8b83d58fd333a1f08e40f932f40ecbe50ac5c31.
```

This is a strict arbitrary-order reduction of the deeper-blocker branch,
not its exclusion.  The next target is to contradict either persistent
blocker surplus by incidence or the exact pure-minor recursion by the
minor's inherited killer flags.

### Three-colour blocker-union lower bound

The tight-case tensor constraint rules out the smallest possible union
of blocker vertices across colours.  Fix a zero-coupled root pair
`x,y` with all three products `x[d]y[d]` nonzero.  The double-star
theorem supplies at least two blockers for each colour.  A vertex can
block at most two colours because its two root covectors span a space
of dimension at most two.

If only three blocker vertices existed, capacity would be tight.  Their
types would be exactly

```text
01, 02, 12.
```

For colour 0, the two exact blockers have covector spans
`span(e_0,e_1)` and `span(e_0,e_2)`.  Their root--blocker coefficient
matrix is `U J V^T` for two invertible `2 x 2` matrices and the swap
matrix `J`, so its determinant is `-det(U)det(V) != 0`.  But the
tight-case tensor theorem makes it globally diagonal; on those two
different coordinate planes only entry `(0,0)` can survive, giving
rank at most one.  This contradiction proves that at least four
distinct blocker vertices are necessary.

Every rank-at-least-two edge has a bilinear zero with all six root
coordinates nonzero, so the four-vertex conclusion applies around
every such edge.  The theorem and two independent finite audits have
SHA-256:

```text
THREE_COLOUR_BLOCKER_UNION_LEMMA.md
  ab3fe0d15257cc5f1a408eb16b653e599a850d3175b5d334af713df61fa30fdd
tmp/three_colour_blocker_union_verified.json
  72c9e87fb7e457507ac0994621445e25c50f16dc49dc0b5d291030405e2f2a22
tmp/three_colour_blocker_union_audited.json
  d6cfca5bed5fbd223a706e75b421d60e87e61b6ccd9046d343554349313604b7.
```

The bound is locally sharp at four blocker vertices.  The tight-pair
rank rule leaves exactly 12 labelled incidence multisets and three
orbits under colour permutation:

```text
0,0,12,12
0,01,12,12
01,01,02,02.
```

Intersecting these three four-vertex patterns across adjacent root edges
is the next incidence target.

### Certified order-twelve complementary profile

The corrected set-tree abstraction, strengthened by the all-size
hafnian-convolution split, is now decisively inconsistent for the single
order-twelve normal-type profile

```text
6 x 000 + 6 x 111.
```

Every eligible subset has equal size in the two type classes.  The base
formula has 2,769 membership variables, 54,216 vertex-expansion witness
variables, and 24,225 convolution-split witness variables, for 81,210
variables and 209,263 clauses.  Its 5,861 eligible two/three-block
partitions contribute 35,166 injective-colour incompatibility clauses.

Tree 0 can be normalized to an ordered identity matching.  Expanding
tree 1 at row 0, the same partner is immediately incompatible with tree
0, while the other five partners form one `S_5` orbit.  Recursive
stabilizers reduce the resulting 120 partner permutations to 16
canonical leaves whose orbit weights sum to 120.

A 17-selector combined CNF has 81,227 variables and 209,442 clauses.
Kissat proves it UNSAT with a 70,573,433-byte DRAT proof.  Forward
`drat-trim` replay returns `s VERIFIED`, using 971,733 core lemmas,
42,612,268 resolution steps, and 15,925 RAT lemmas.  A separate
restricted-growth/combination-split reconstruction with Glucose 4
independently returns UNSAT on all 17 branches and checks 31 local orbit
covers.

Principal SHA-256 values are:

```text
tmp/twelve_vertex_complement_set_trees_symmetry_broken.cnf
  6b1b77d1da94d189ef96865f319252c7398cd0c05521eb7e8bf2b2e56a78e0aa
tmp/twelve_vertex_complement_profile_selector.cnf
  f068909260432a7e2ae7107843210cffabfb13c36634d9fd9452c63a61caedc8
tmp/twelve_vertex_complement_profile_selector.drat
  22d560ecad355664894980d0002a6bd949ac12ef7ab8b33a3612090e4868fbe4
tmp/twelve_vertex_complement_profile_selector_manifest.json
  cd0e8ac1c9420de24fbb0c022838006dc69fb1c942b3b12cf699bf9a27755ecb
tmp/twelve_vertex_complement_profile_kissat_run.json
  c3a0c52d0698da2a5c09d7dca20d677d4bba5fc49cb322e03a766a9e7acf0458
tmp/twelve_vertex_complement_profile_drat_replay.json
  b170abcc6ab9b236dd832daf3ee1317a440f7080ab75d3a33ab237bcda767e2a
tmp/twelve_vertex_complement_profile_audited.json
  7bf711d3b94a856132d8b26d04797e5855eca4d31353525bf71f0220735f3a70
```

The full theorem statement and audit boundary are in
`TWELVE_VERTEX_COMPLEMENT_PROFILE_SET_TREE_OBSTRUCTION.md`.  This
excludes one order-twelve all-bridge profile only.  It does not close the
other balanced profiles or the separate deeper-blocker branch.

### Four-blocker ideal obstruction

The three four-vertex incidence patterns left by the tight blocker-pair
rank rule are all impossible once the full root-pair expansion is kept.
Fix a fully supported zero-coupled root pair and suppose the union of its
three blocker sets has four vertices `B`.  At every other outside vertex
`v`, restrict to

```text
K_v = ker(a_v) intersect ker(b_v).
```

Because `v` blocks no colour, every coordinate functional remains
nonzero on `K_v`.  The three residual coordinate-product tensors are
therefore nonzero.  A generic linear functional on all residual modes is
simultaneously nonzero on those three tensors.

After applying that functional, the matching identity on the four
blocker variables has the form

```text
sum_d lambda_d product_(i in B) z_i[d]
  = sum_(i<j in B) F_ij L_ij,

F_ij = m_i(z_i)^T [0 1; 1 0] m_j(z_j),
lambda_0 lambda_1 lambda_2 != 0.
```

Thus the right side vanishes at any common zero of the six `F_ij`.
Every surviving blocker-incidence orbit has such a common zero where
exactly one diagonal term on the left remains nonzero:

```text
0,0,12,12    -> colour 1 survives,
0,01,12,12   -> colour 2 survives,
01,01,02,02  -> colour 1 survives.
```

For example, in the last pattern put `e_1` at the two type-02 vertices,
which kills their two root covectors.  The exact type-01 pair has a
nondegenerate diagonal form

```text
delta_0 z[0]w[0] + delta_1 z[1]w[1],
```

so choose a zero with both colour-1 coordinates nonzero.  All six
root-pair generators vanish, but the colour-1 GHZ monomial does not.
The other patterns use the same construction, with the pure singleton
forced by the tight span dichotomy where needed.

Consequently every fully supported zero-coupled root pair needs at least
five distinct outside blocker vertices.  This is arbitrary-order and
strictly strengthens the earlier lower bound of four.

The primary verifier reconstructs the 12 labelled patterns and three
colour orbits and checks four symbolic common-zero cases, including the
pure and rank-two singleton subcases.  The independent bit-mask audit
checks 544 nonzero parameter assignments over `F_5`.  Principal SHA-256
values are:

```text
FOUR_BLOCKER_IDEAL_OBSTRUCTION.md
  69c6b28c7be671819673a1d63133f846a0e5277a01fe05cd98e1324104474d70
verify_four_blocker_ideal_obstruction.py
  f64304bb2aaa478e9590eeca4e9168c7f50dbf994d14ab0d4ca73792606d3411
audit_four_blocker_ideal_obstruction.py
  78739a353a81f9dae4941518d2e292daf6bb87263c0e2832e9d3b5a6dc4741d8
tmp/four_blocker_ideal_obstruction_verified.json
  0d16f4fbd0cda4d83626ddca832e1e3b903b85bf3d7064ca72b9ab31a51d38c6
tmp/four_blocker_ideal_obstruction_audited.json
  ab9e04ba0124a30b2db6485f597f0d130b93dcc2ad3961af069c2aa47de2dd3d
```

The remaining incidence target is now the five-blocker boundary or a
root-promotion argument that forces blocker surplus to propagate.

### Exact three-blocker permanent rank

The equality case after promoting a simultaneous-kernel vertex to a
third root has an additional tensor-rank obstruction.  Let three fully
supported root vectors be pairwise zero-coupled, and suppose colour `c`
has exactly three blockers.  The multi-star factorisation makes the
three-blocker tensor diagonal:

```text
F_U = gamma_0 D_0 + gamma_1 D_1 + gamma_2 D_2,
gamma_c != 0.
```

At each blocker, the three root covectors define a local map
`M_u:C^3 -> C^3`.  Before those maps are applied, `F_U` is the standard
order-three permanent tensor

```text
P_3 = sum_(sigma in S_3)
        e_(sigma(0)) tensor e_(sigma(1)) tensor e_(sigma(2)).
```

If all three diagonal coefficients were nonzero, every local map would
be invertible.  Tensor rank would therefore be preserved.  But `P_3`
has rank four.  Its first-mode slice space is

```text
[0 z y; z 0 x; y x 0].
```

The three principal `2 x 2` minors are `-z^2,-y^2,-x^2`, so this slice
space has no nonzero rank-one member.  A rank-three decomposition,
together with the three rank-three flattenings, would force three
rank-one matrices into that space.  A four-term polarization identity
gives the matching upper bound.  In contrast, a diagonal tensor with
three nonzero terms has rank three.

It follows that at most two residual coordinate products can remain
active.  Since the fixed colour-`c` product is nonzero, at least one
other residual kernel product vanishes.  In a promotion step this
exposes a blocker for another colour unless a fourth colour-`c` blocker
already supplies surplus.

The symbolic proof and independent 124-slice `F_5` audit have SHA-256:

```text
EXACT_THREE_BLOCKER_PERMANENT_RANK_LEMMA.md
  aabba14d7d3b5407142a50dffe3e19cec61ae7e4677c9fa84af5a93174236d54
verify_exact_three_blocker_permanent_rank.py
  bc21882c91acec43ae83143321cea462bd9fedb530d33efcbb72c81b9c021b98
audit_exact_three_blocker_permanent_rank.py
  58cb6a64fe3e29a021eb41ffac7bc248a5b22e0fe527551660fa12c338b57282
tmp/exact_three_blocker_permanent_rank_verified.json
  f52a4d7ff6df5698a0c0b788fedff7d9c02bf6091fb791fd5990912a1b4e9c5a
tmp/exact_three_blocker_permanent_rank_audited.json
  f72bb9cb53e225a9c5b36122768bb86212590d180ec17af364c7ba4d4e1a3d34
```

The result does not exclude the fourth-blocker alternative or by itself
return the newly exposed other-colour blocker to the original root pair.

### Fourth-order permanent subrank

The fully tight four-root endpoint has now been excluded over `C`.
Write

```text
P_4 = sum_(sigma in S_4)
        e_(sigma(0)) tensor e_(sigma(1))
        tensor e_(sigma(2)) tensor e_(sigma(3)).
```

If `P_4` restricted to the three-colour diagonal tensor, the four local
maps would have rank three and would select hyperplanes
`U_i=a_i^perp` in `C^4`.  For two such hyperplanes, send `u tensor v`
to the six off-diagonal symmetric products

```text
u[i]v[j] + u[j]v[i].
```

The permanent `2|2` flattening is the nondegenerate complement pairing
on these six coordinates.  If the two hyperplane normals are
independent, their pair image has dimension at least five.  If the
normals agree and have support size `k`, the image has dimension
`k+2`.  Hence a rank-three `2|2` flattening needs one equal-normal,
support-at-most-two pair.  Requiring this for all three pair partitions
forces at least three of the four hyperplanes to be equal.

Support size one makes the fourth one-mode flattening rank at most one.
For support size two, normalize the common hyperplane to
`x[0]+x[1]=0` and write `l=x[1],m=x[2],n=x[3]`.  The fourth-mode slice
space on the first three hyperplanes is

```text
l * span{mn, l n, l m}.
```

It contains no nonzero decomposable tensor: every member is symmetric,
so a decomposable member would be a cube `q^3`; divisibility by `l`
forces `q` to be a multiple of `l`, but `l^3` is absent.  A
three-colour diagonal slice space contains three decomposable tensors,
giving the contradiction.  Conversely, two cyclically shifted
permutations form one alternating eight-cycle and give an explicit
two-colour diagonal restriction.  Thus the exact subrank of `P_4` is
two.

For four fully supported pairwise zero-coupled roots, a four-vertex
total blocker union would make those same four vertices exact blockers
for all three colours.  All residual coordinate products are nonzero
because every remaining outside vertex is a nonblocker.  The multi-star
identity would therefore produce the forbidden concise diagonal
restriction of `P_4`.  Such a root set needs at least five blockers in
total.

The primary symbolic verifier and independent `F_5` audit have SHA-256:

```text
FOURTH_ORDER_PERMANENT_SUBRANK_OBSTRUCTION.md
  2b4e18cb0ce60d64e9100c96ea690ca091c0ae0690a462d3dec752358eda6c32
verify_fourth_order_permanent_subrank.py
  74baf64020cf1e4e8e25f2ec66fa0f73907e955889498131ca63842d1c8ad05f
audit_fourth_order_permanent_subrank.py
  57db531e72230f36efc0cadb1d9dce91f3483eed18a34888ff21d4c0fc352f73
tmp/fourth_order_permanent_subrank_verified.json
  a3020c682f9d72735f8f74d272c1174e132fbe3ca2fa49a58b48c9706b5b34ff
tmp/fourth_order_permanent_subrank_audited.json
  a05124c55b16f7978f406dd74dd40eea7bab70379358fcd1af430089e74e383d
```

This is an exact order-four theorem, not a proof that every higher-order
permanent tensor also has subrank two.  Extending the flattening/slice
mechanism beyond hyperplanes is the next analytic boundary.

### Support-three `P_5` contraction subrank

The first new contraction beyond the `P_4` theorem is now closed over
`C`.  Contracting `P_5` by a vector supported on three coordinates gives
the quartic

```text
a b q,
```

where `a,b` are independent linear factors and `q` is a nondegenerate
ternary quadratic.  If this tensor restricted to `Delta_3`, the common
kernel `K_i` of the pullbacks of `a,b` at each of the four modes would
be nonzero.  Contracting at a full-target-support vector in `K_i` would
turn the source into the essential `P_3` tensor and the target into
`Delta_3`, contradicting rank four versus rank three.  Therefore every
`K_i` lies in a target coordinate hyperplane and is one of nine abstract
line/plane types.

On restricting any complementary kernel pair, the quartic identity
reduces to one root-pair form times one quadratic cofactor.  Hence the
coordinatewise products of that kernel pair span at most one diagonal
matrix, and every nonzero such matrix must have the same rank and
row/column spaces as the complementary pair form.  Exhausting the
`9^4 = 6,561` abstract type assignments leaves no survivor.  A separate
`F_5` audit checks all 15 projective line kernels and three coordinate
planes, hence `18^4 = 104,976` actual kernel quadruples, again with no
survivor.

An induced two-edge coordinate box gives the matching lower bound, so
every support-three contraction has exact subrank two.  Support-one and
support-two contractions reduce to `P_4`, proving the upper bound two
for every support-at-most-three contraction of `P_5`.

```text
SUPPORT_THREE_P5_CONTRACTION_SUBRANK.md
  892f2445b19bf7e3c8ae3441138773ac889906ac5de6cb74898bf60699f44a3f
verify_support_three_p5_contraction_subrank.py
  ad34c04c6be209843e2570ba3733e6c38e2bd874a3cce0d57efbe8f51a5fb868
audit_support_three_p5_contraction_subrank.py
  57c66b27d542d2ec238e1f100ef5ae07571ec7c57e1494b0b71521b191bbc24c
tmp/support_three_p5_contraction_subrank_verified.json
  bbbf532386493ea1169aba64021b394900164e2dff53faa66e4e1b8b98fb3c36
tmp/support_three_p5_contraction_subrank_audited.json
  de5021ff581477a5f256061b6da1fcc5b9437d94d46d868f7a69f5f08fbacf94
```

For a hypothetical restriction `P_5 -> Delta_3`, intersecting any local
three-plane with any source coordinate three-plane now shows that the
span of every pair of its five row covectors must contain one of the
three target coordinate covectors.  Classifying that five-point
projective incidence condition is the next exact boundary.

### Support-four `P_5` contraction is positive

The support-at-most-three obstruction cannot be extended to support
four.  For the canonical contraction of `P_5` by `(1,1,1,1,0)`, the
four integer `5 x 3` matrices in
`SUPPORT_FOUR_P5_CONTRACTION_RESTRICTION.md` give exactly

```text
12 Delta_3.
```

All four maps have column rank three.  Direct expansion leaves precisely
the three diagonal target coefficients, each equal to 12, among all 81
coefficients.

The integer point is the specialization `(u,v,w)=(0,0,-1)` of a family
on

```text
u v w - u v - u w - u - v w - v - w - 1 = 0.
```

Modulo this relation, all 78 off-diagonal coefficients vanish and each
diagonal coefficient is `-12(u+v+w)`.  Independent finite-field audits
check 19 nonsingular family points over `F_5` and 39 over `F_7`.
Coordinate scaling shows that every contraction vector with exactly
four nonzero entries is equivalent to the canonical one.

```text
SUPPORT_FOUR_P5_CONTRACTION_RESTRICTION.md
  4ec294ed43bb0d450c6287c0877a00b3568fe36123c38cc82179ea091880217a
verify_support_four_p5_contraction_restriction.py
  d2c1983a5fb13f242083103b2a4317fc4ef9aa2dff96b6228f87101398bacae1
audit_support_four_p5_contraction_restriction.py
  fd2e2707f9f7c5efc99e31d27fee64aadd08ee7c74b157767106dff20dc3ee3f
tmp/support_four_p5_contraction_restriction_verified.json
  9c40ae8529c40f348faa7ef83a0974692adc6f852c5292d943e23ddcb566d975
tmp/support_four_p5_contraction_restriction_audited.json
  b62ea8b3d1fbfd6e75c87f0812e2abe05bb3d1d700c5627fe5189e168b49bda0
```

This is a local tensor restriction, not a `P_5 -> Delta_3` restriction
and not a graph witness.  It explains the bounded numerical solutions
in the support-four probe and establishes that the contraction strategy
stops sharply at support three.

### Five-row projective incidence

Although support-four contractions are positive, the support-at-most-three
theorem still constrains every local map in a hypothetical
`P_5 -> Delta_3` restriction.  If `r_0,...,r_4` are its five row
covectors, then for every pair `p,q`,

```text
span(r_p,r_q) contains one of e_0^*,e_1^*,e_2^*.
```

Indeed, the common kernel of `r_p,r_q` maps into a source coordinate
three-plane.  A full-target-support vector there would contract the
claimed restriction to the forbidden support-at-most-three quartic
restriction.

A projective-plane argument now forces at least one `r_p` to be a
coordinate covector.  If all five projective rows were non-coordinate,
no three could be collinear.  Every triangle would therefore have its
three sides pass through the three distinct coordinate points.  This
would be a three-edge-colouring of `K_5` in which every triangle is
rainbow, forcing four different incident colours at any vertex.

Thus every one of the five local maps has a nonzero singleton row.
The primary verifier checks all `3^10 = 59,049` edge colourings and also
counts 68 singleton-placement orbits.  The independent `F_5` audit
checks 376,992 five-point multisets; 2,556 span and satisfy the pair
incidence condition, and all 2,556 contain a coordinate point.

```text
FIVE_ROW_PROJECTIVE_INCIDENCE_LEMMA.md
  9c6aa200cdbf760d0e836f90eaab0804b1dda0c6f0c6baff354a8a57741386ed
verify_five_row_projective_incidence.py
  e67903169e0d3137125184c7f69f17a1f212f88bc5b7bddcccba5b0633863ec7
audit_five_row_projective_incidence.py
  03de5004b69b94d518004af395abb401cef39469481076702579a52caba1a540
tmp/five_row_projective_incidence_verified.json
  1f0689b4a48f6579511aa85212ecbce11b989b69ddd238b5523b07820b72a86b
tmp/five_row_projective_incidence_audited.json
  ac6bec1887922898759872c7825c39b01c1782ea07f7e9709c15c2f6ed645c2e
```

A first constrained numerical pass over all 68 placement orbits found
only rank-collapsing residual-one endpoints after polishing.  This is
exploratory rather than a proof.  The exact next task is to combine the
singleton placements with the mixed-row permanent identities.

### `P_5` source-row tricolour cover

The previously missing singleton case of the kernel Hall hierarchy has
an exact tensor-level resolution.  Fix a source row `p` and restrict
every local input to the kernel of that row.  All five source vectors
then avoid `p`, so the permanent vanishes.  On the target side this is
a dependence among the three restricted coordinate-product tensors.

Three nonzero decomposable tensors can be dependent only if, outside at
most one mode, all three local factors are proportional.  Here the
restricted coordinate functionals span the dual of a row kernel, of
dimension at least two, in every mode.  Two surviving terms are also
impossible: at a mode that kills the third colour, their factors are
the two independent coordinates on that coordinate plane.  Hence all
three terms are killed separately.

Therefore, for every source row and every target colour, some local map
has that exact coordinate row.  The five maps contain at least 15
coordinate rows in total, so one map contains at least three.  The
independent `F_3` audit checks all 8,568 multisets of five
zero-or-projective covectors and all 34,272 nonzero coefficient-ratio
cases.  Exactly 420 restrictions vanish, and every one contains all
three coordinate covectors.

```text
P5_SOURCE_ROW_TRICOLOUR_COVER.md
  faafd46d86cb815df9e65c7fc4e709528ea5ae708dcbe5b8689aa3fabfba0807
verify_p5_source_row_tricolour_cover.py
  a5c48f99b4a7a6546b02e39f18a518e54a2c11abdeb3887fafc276e0238fa569
audit_p5_source_row_tricolour_cover.py
  f552a1c0bc093f244174afade0fbe99d7a7b39288c4b72aaa9b2425c49f1b89b
tmp/p5_source_row_tricolour_cover_verified.json
  5d752f076acf2dd33ae9397a935b135a283938e3027582bb507a1adb43752b4a
tmp/p5_source_row_tricolour_cover_audited.json
  f9fe471272095662f8e3ac894e7759e9faf12b66c2bb8dfe1d1b2be3db15cdc2
```

A support-only search with the new 15-cell cover kills the former
11-coordinate survivor but leaves rare 20-coordinate architectures.
The first such architecture has an odd signed dependence among three
two-term mixed-colour equations, so it is impossible over `C`.  Making
that signed-cancellation obstruction exhaustive is the next finite
interface; the support survivor itself is not a tensor restriction.

### Complex coverage of the finite pair-signature catalogue

The finite `F_5` row catalogue can now be used rigorously for support
and pair-incidence case splits over `C`.  A separate abstract CNF keeps
only necessary complex-valid facts about exact row supports and the ten
statements

```text
e_c in span(r_p,r_q).
```

It includes pair-support compatibility, coordinate-plane inference,
projective plane closure, and structural rank three.  Blocking the
6,495 labelled signatures generated over `F_5` leaves 303 abstract
patterns.  All 303 have the same singleton coordinate incidence on
every row pair, form eight `S_5 x S_3` orbits of sizes

```text
3, 15, 15, 30, 30, 60, 60, 90,
```

and force all ten `3 x 3` row minors to vanish.  Geometrically, three
independent rows would give two distinct pair planes whose intersection
is one row line; a coordinate point common to every pair plane would
then make two independent rows proportional to that coordinate point.

After adding those 303 rank-loss exclusions, the 150-variable,
9,099-clause CNF is UNSAT.  CaDiCaL generated a 3,349,683-byte DRAT
proof, and independent forward `drat-trim` replay returned
`s VERIFIED`.  A separate audit reconstructs the catalogue, the 303
outside patterns, their Smith-form rank losses, their eight orbits, and
the artifact hashes.

```text
P5_PAIR_SIGNATURE_CATALOGUE_COVERAGE.md
  84c323376f408228ff75fda6df0950982a61a967f99369bfe7af1bb45fc0084f
verify_p5_pair_signature_catalogue_coverage.py
  188b200b3f0a343835704388c844888c673ffb8ac7d14ab24f8a1ee6f4b0aea7
audit_p5_pair_signature_catalogue_coverage.py
  81701bcfa8f6eb1726c50898708047aade90688975604ee904f3200529213b32

tmp/p5_pair_signature_catalogue_coverage_verified.json
  3ca857f513f2a2d02193b48953d339d3472b82e576bd91885b1510a545d4c6d4
tmp/p5_pair_signature_catalogue_coverage.cnf
  fdd8f2184d9efa50db1634a0c774009c17c60b236e113b4c80dac794cb31a093
tmp/p5_pair_signature_catalogue_coverage.drat
  fcdf1cdce1df1b68579c7404272635a30ecc13f02fc8615c1dd04ff9b4c7afe2
```

This does not import higher-subset ranks from finite characteristic and
does not claim that every catalogue pattern is realizable over `C`.
It proves only the direction needed for exhaustive complex case splits:
every complex support/pair-incidence signature lies in the list.

During the coefficient CEGAR work, a local Singular order (`ds`) was
briefly used as a speed probe.  A unit standard basis in a local order
does not certify a global unit ideal.  Every clause learned from that
order was removed from the active ledgers.  Only global orders such as
`dp`, together with exact signed-lattice and rank arguments, are accepted
as coefficient-level exclusions.

### Saturated three-coordinate `P_5` cycle dichotomy

The source-row tricolour cover has a sharp equality architecture.  If
every local map has at most three coordinate rows, its fifteen distinct
source-row/target-colour requirements saturate the total capacity.
Every mode therefore has exactly three coordinate rows, and every
source row is coordinate in three modes and non-coordinate in two.

The ten non-coordinate cells form a 2-regular simple bipartite graph
between the five modes and five source rows.  Its even-cycle component
sizes can only be

```text
10
```

or

```text
4 + 6.
```

A direct choice-of-two-neighbours enumeration finds 2,040 labelled
graphs, split as 1,440 `C10` and 600 `C4+C6`.  An independent
enumeration as unions of two pointwise-disjoint perfect matchings finds
5,280 ordered decompositions.  The decomposition multiplicities are two
and four respectively, reproducing

```text
1,440 * 2 + 600 * 4 = 5,280.
```

This is an exact structural theorem over `C`, not yet a coefficient
obstruction for either loop family.

```text
P5_THREE_COORDINATE_CYCLE_DICHOTOMY.md
  b83f11c5e48f17abb1079bca8cc0133d409e94e2ba86b0791d4d608b94f3064a
verify_p5_three_coordinate_cycle_dichotomy.py
  4129d41a5bbb9e4e724cbe4d4299971f4b4ba32d1ffa77ff9a342587985b627b
audit_p5_three_coordinate_cycle_dichotomy.py
  7c9b489024925a5c63129f5dec6d63565f8bdc641219b8541e5391ccbcee5ebd
```

### Universal five-blocker divisibility

The pointwise five-blocker lower bound has an arbitrary-order
algebraic upgrade.  Fix a rank-at-least-two root edge

```text
g(x,y) = x^T M y.
```

Its zero hypersurface is irreducible, and its fully supported part is
dense.  For every point of that dense part, the four-blocker ideal
obstruction supplies five distinct outside blockers.  There are only
finitely many choices of five vertices and one blocked colour at each,
so irreducibility forces one fixed choice to occur on a dense
constructible subset.

For an outside vertex `u`, blocked colour `c`, and complementary colours
`a,b`, the blocker determinant has coefficient matrix

```text
F_(u,c)
  = B_pu[:,a] B_ru[:,b]^T
    - B_pu[:,b] B_ru[:,a]^T.
```

It vanishes on the dense subset.  Since the prime ideal of the root
hypersurface is generated by `g` and both polynomials have bidegree
`(1,1)`, one obtains five fixed identities

```text
F_(u_j,c_j) = lambda_j M.
```

Every `F_(u,c)` factors as a `3 x 2` matrix times a `2 x 3` matrix.  A
nonzero scalar can therefore occur only when `rank(M)=2`.  When
`rank(M)=3`, all five matrices vanish, and at each selected outside
vertex at least one incident complementary-column pair has rank at most
one.  At least three of the five one-sided compressions lie at the same
root endpoint.

The zero factorisation has a sharper exact dichotomy.  If either
complementary-column pair has rank two, a left inverse forces the
opposite pair to be exactly zero; otherwise both pairs have rank at most
one.  Hence a full-rank incident block forces the opposite block to have
only its blocked-colour column nonzero.  Dense blocker membership rules
out that last column vanishing, so the opposite block is a genuine
one-sided killer.  In particular, both incident blocks at a frozen
blocker cannot have rank three.

The primary checker reconstructs the three determinant signs and the
rank-two factorisations and the rank-two-forces-zero implication
symbolically over `C`.  An independent audit checks all
`3^12 = 531,441` pairs of `3 x 2` matrices over `F_3`; 4,161 have zero
outer difference, with exact rank profiles

```text
(0,0):    1    (0,1): 104    (0,2): 624
(1,0):  104    (1,1): 2704   (2,0): 624.
```

Thus profiles `(2,1)`, `(1,2)`, and `(2,2)` are all absent.  The
dependency certificate for the four-blocker theorem was also rerun
successfully.

```text
UNIVERSAL_FIVE_BLOCKER_DIVISIBILITY_LEMMA.md
  2ed722fe01aa40a873570f3f1f6716bf5d1be1fba5c0b63778d9a4470a157496
verify_universal_five_blocker_divisibility.py
  172e6312c8fad8a1eb2fdf814f2dacada6f90f6f47275873285827ee596ef64b
audit_universal_five_blocker_divisibility.py
  a8ead1924c9d463fb5f22124f3bbf685369e97ca168f381d183586997b7828ee
tmp/universal_five_blocker_divisibility_verified.json
  8af287400c5fbd1025993f6886abf3a4688321aee76b326552f25d18fef664a2
tmp/universal_five_blocker_divisibility_audited.json
  e45c176a87513dfaa8c547822663163b11320dde8df6fa35a5e82544e10731c5
```

This is not yet a global contradiction.  The remaining arbitrary-order
target is to propagate the exact zero-or-killer alternatives through
adjacent rank-three edges, or to combine them with the existing root-set
blocker surplus.

### Proper all-full `P_5` tricolour obstruction

The exact-three-coordinate cycle dichotomy has a now-closed structured
subboundary.  Require both non-coordinate rows in every local map to have
full support, and require the three singleton coordinate colours to occur
once each in every mode and every source row.

An independent enumeration finds exactly three support orbits:

```text
two C10 orbits, of labelled sizes 6 and 30;
one C4+C6 orbit, of labelled size 24.
```

For each representative, the 45 supported entries have a connected gauge
graph.  Tree normalization leaves 26 variables.  Retaining only the 150
mixed coefficients whose target word uses all three colours, and saturating
by the 26 variables and three pure coefficients, gives an ideal with 151
equations in 27 variables over `Q`.

Singular `slimgb` returns `UNIT_IDEAL` for every representative.  A strict
syntax conversion of the identical systems to `msolve 0.6.5` independently
returns `[-1]:` for all three.  Thus the 90 two-colour mixed equations are
not needed.

The primary verifier reconstructs the coefficients from the support arrays
and checks source, conversion, outputs, and hashes.  The separate audit
reconstructs the full bipartite automorphism groups and orbit partition.

```text
P5_ALL_FULL_TRICOLOUR_OBSTRUCTION.md
verify_p5_all_full_tricolour_obstruction.py
audit_p5_all_full_tricolour_obstruction.py
research_snapshots/2026-07-27-p5-coordinate-cegar/
  all_full_tricolour_boundary/
```

This finite theorem does not cover partial non-coordinate support,
non-proper singleton-colour assignments, or a local map with four or five
coordinate rows.  Those branches remain active, and the global conjecture
remains unresolved.

### Entire all-full exact-three-coordinate `P_5` obstruction

The extra row-proper hypothesis in the preceding theorem is no longer
needed.  In the exact-three-coordinate branch, the source-row tricolour
cover uses all 15 available coordinate cells.  Every source column
therefore contains the three singleton colours exactly once, while the
ten non-coordinate cells form `C10` or `C4+C6`.

For either fixed full-cell graph there are

```text
6^5 = 7,776
```

labelled singleton assignments.  Quotienting by the graph automorphism
group and global colour permutation gives 148 `C10` support orbits and 78
`C4+C6` support orbits.  The exact orbit-size histograms are

```text
C10:   6:1, 30:35, 60:112
C4+C6: 12:1, 24:2, 36:7, 48:1, 72:31, 144:36.
```

Reconstructing the certified 6,495-pattern complex pair-signature
catalogue and imposing the 30 pair Hall quotas excludes 213 of the 226
supports.  The 13 viable supports consist of the three row-proper orbits
already excluded above and ten nonproper supports.  Those ten supports
have exactly 198 viable five-tuples of local signatures.

For each of the 198 tuples, the 45 supported entries have a connected
gauge graph.  Tree normalization leaves 26 variables.  The positive
pair-incidence minors have rank five and a unimodular pivot, leaving 21
Laurent parameters.  Expanding all nonzero mixed permanent coefficients
and saturating by the parameters and three pure coefficients produces the
mixed-equation histogram

```text
216:   9
220:  18
230:  45
240: 126.
```

Singular `slimgb` in the global `dp` order returns the unit ideal for 186
direct Rabinowitsch systems.  Replacing the one product saturation
equation by 24 exactly equivalent inverse equations certifies 15 cases,
three overlapping the direct set, so the Singular union is all 198.
The systems omit negative incidence inequations, making them safe
relaxations of the exact signature strata.  The same split conversion to
`msolve 0.10.1` independently returns the unit ideal in 111 cases.

The audit regenerates both automorphism groups, all labelled assignments,
the support quotient, the catalogue quotas, and the 198 case keys.  The
primary verifier independently regenerates every incidence minor,
unimodular Laurent substitution, permanent coefficient, and saturation
equation, checks exact source equality and artifact hashes, and requires a
unit-ideal result for every case.

```text
P5_ALL_FULL_BOUNDARY_OBSTRUCTION.md
audit_p5_all_full_boundary_obstruction.py
generate_p5_all_full_signature_system.py
verify_p5_all_full_boundary_obstruction.py
research_snapshots/2026-07-27-p5-coordinate-cegar/
  all_full_boundary/
```

This closes the entire all-full layer of both exact-three-coordinate cycle
architectures.  The remaining finite boundaries contain a support mask
`3`, `5`, or `6`, or have four/five coordinate rows in some mode.  The
global conjecture remains unresolved.

### Exact-one-partial exact-three-coordinate `P_5` obstruction

The next full support layer is now closed.  Fix either `C10` or `C4+C6`,
make exactly one of its ten non-coordinate cells partial with mask `3`,
`5`, or `6`, and leave the other nine cells full.  The source-row
tricolour cover again makes each source column contain singleton masks
`1`, `2`, and `4` exactly once.

There are

```text
6^5 * 10 * 3 = 233,280
```

labelled supports for each fixed graph.  Quotienting by the graph
automorphisms and global colour permutation gives 3,888 `C10` orbits and
1,788 `C4+C6` orbits.  The complex local catalogue rejects 144 and 80,
respectively.  Applying all 30 pair Hall quotas to the remaining 5,452
orbits leaves:

```text
C10:    236 viable supports, 4,631 viable signature tuples
C4+C6:   83 viable supports, 1,944 viable signature tuples
total:  319 viable supports, 6,575 viable signature tuples.
```

The final algebra deliberately forgets the pair signatures.  Every
support has 44 required nonzero entries and a connected gauge graph;
spanning-tree normalization leaves 25 Laurent parameters.  Expanding all
nonzero mixed permanent coefficients and saturating by those parameters
and the three pure coefficients gives:

```text
mixed equations  supports
216                    20
218                    15
219                     6
220                    21
222                    47
223                    83
224                   127
```

Exact Singular `slimgb` in global `dp` order returns the unit ideal
directly for 307 supports.  For the remaining 12, the exactly equivalent
split-saturation encoding returns the unit ideal.  There is no overlap,
so all 319 support strata are empty over `C`.  Since these systems omit
every pair-incidence equation and inequation, they are safe relaxations
of all 6,575 viable signature tuples.

The audit independently reconstructs all 466,560 labelled supports, both
symmetry quotients, the 6,495-pattern local catalogue, all Hall quotas,
and the final support keys.  The verifier regenerates every coefficient
system, checks byte equality and hashes, reconstructs the split
conversion, and requires exact unit-ideal output for every case.

```text
P5_ONE_PARTIAL_BOUNDARY_OBSTRUCTION.md
audit_p5_one_partial_boundary_obstruction.py
generate_p5_one_partial_support_system.py
verify_p5_one_partial_boundary_obstruction.py
research_snapshots/2026-07-27-p5-coordinate-cegar/
  one_partial_boundary/
```

Together with the all-full theorem, this proves that every hypothetical
exact-three-coordinate restriction has at least two partial
non-coordinate cells.  That deeper finite layer, the four/five-coordinate
branch, and the arbitrary-order conjecture remain unresolved.

### Exact-two-partial exact-three-coordinate `P_5` obstruction

The next support layer is now closed.  Fix `C10` or `C4+C6`, make exactly
two of the ten non-coordinate cells partial with masks `3`, `5`, or `6`,
and leave the other eight full.  There are

```text
6^5 * binomial(10,2) * 3^2 = 3,149,280
```

labelled supports per graph.  Independent packed-array enumeration and
the fixed-graph/global-colour quotient give:

```text
shape   support orbits   locally invalid   locally valid
C10              52,758             7,884          44,874
C4+C6            23,340             3,730          19,610
total            76,098            11,614          64,484
```

The 30 pair Hall quotas exclude 59,911 locally valid supports and leave
4,573 supports carrying 50,109 viable signature tuples.  The missing-pure
and unique-mixed-permanent support tests exclude another 14 and 1,251
supports respectively.  Their exclusion sets are disjoint, leaving 3,308
support-semantic survivors.

Every survivor has 43 required nonzero entries and a connected gauge
graph.  Spanning-tree normalization leaves 24 Laurent parameters.
Expanding all nonzero mixed permanent coefficients and saturating by the
parameters and three pure coefficients gives the unit ideal directly for
3,307 supports.  One system needs the exactly equivalent 27-equation
split saturation.  Thus every exact-two support stratum is empty over
`C`.

The primary verifier checks both independently regenerated audit hashes,
matches the audit and SAT catalogues orbit by orbit, replays every
signature witness and Hall quota, and semantically regenerates all 3,308
coefficient systems.  It checks byte equality, all hashes, the split
conversion, and exact unit-ideal output.  It returns `"verified": true`.

```text
P5_EXACT_TWO_PARTIAL_BOUNDARY_OBSTRUCTION.md
audit_p5_exact_two_partial_boundary.py
generate_p5_exact_two_partial_support_system.py
verify_p5_exact_two_partial_boundary_obstruction.py
research_snapshots/2026-07-27-p5-coordinate-cegar/
  two_partial_boundary/
```

Together with the all-full and exact-one-partial theorems, this proves
that every hypothetical exact-three-coordinate restriction has at least
three partial non-coordinate cells.  A symmetry-broken exact-cardinality
SAT enumeration avoids materializing the 50,388,480 labelled supports in
the next layer.  The four/five-coordinate branch and the arbitrary-order
conjecture remain unresolved.

### Degree-six invariant strategy boundary

An exact representation-theoretic calculation closes the first natural
scalar-invariant separator route.  For five qutrit modes, the
degree-three determinant contraction vanishes by odd-mode antisymmetry.
At degree six, the local `S_6` Specht module has shape `(2,2,2)` and
dimension five.  Exact character arithmetic gives

```text
dimension (([2,2,2]) tensor power 5)^(S_6) = 11.
```

Eleven explicit epsilon-pair contractions form a basis: their generic
evaluation determinant is `1 mod 5`.  Evaluating the same basis on
deterministically generated local restrictions of `P_5` gives an
`11 x 11` determinant of `2 mod 5`.  Therefore the pullback from
degree-six `SL(3)^5` scalar invariants to the `P_5` restriction family
is injective over characteristic zero.

Consequently no nonzero invariant of this precise type vanishes on the
entire restriction image.  This is a rigorous negative result about one
strategy, not an obstruction to `P_5 -> Delta_3` and not a solution of
the global conjecture.  Higher-degree invariant relations,
non-invariant equations, sparse Laurent identities, and Grassmannian
incidence elimination remain open routes.

```text
P5_DEGREE_SIX_INVARIANT_PULLBACK.md
analyze_p5_degree_six_invariant_space.py
verify_p5_degree_six_invariant_pullback.py
```

### No quadratic equations on the `P_5` restriction image

The broader covariant strategy also has a sharp low-degree boundary.
The quadratic polynomial space on `(C^3) tensor power 5` is the direct
sum of sixteen multiplicity-one `GL(3)^5` modules, with an even number
of local exterior-square factors.  For each module, an identity
permutation paired with a transposition or four-cycle gives an isolated
nonzero coefficient in the corresponding projection of
`P_5 tensor P_5`.

The restriction pullback is equivariant, so its kernel intersects each
irreducible multiplicity-one summand in either zero or the whole
summand.  The explicit nonzero projections prove that every intersection
is zero.  Hence no nonzero homogeneous quadratic polynomial vanishes on
the full local-restriction image of `P_5`; a covariant separator must
have degree at least three.

```text
P5_NO_QUADRATIC_RESTRICTION_EQUATIONS.md
verify_p5_no_quadratic_restriction_equations.py
```

### No cubic equations on the `P_5` restriction image

The full cubic covariant pullback is injective as well.  Schur--Weyl
duality decomposes the cubic polynomial space into 147 ordered
`GL(3)^5` module tuples with nonzero diagonal-`S_3` multiplicity.  Mode
symmetry reduces them to thirteen type-count representatives, with
multiplicities one, three, or five.

An exact verifier constructs rational `S_3` matrix units, contracts
deterministic local covectors with three simultaneous copies of `P_5`,
and checks that the resulting diagonal-invariant vectors span every
multiplicity space.  Explicit full-rank minors modulo five prove the
same ranks over `Q`, since the only matrix-unit denominator is six.
The dimension sum is the full

```text
binomial(245,3) = 2,421,090
```

cubic polynomial space.  Therefore no nonzero cubic polynomial
vanishes on all local restrictions of `P_5`.  Combined with the
quadratic theorem, a global covariant separator must have degree at
least four.

```text
P5_NO_CUBIC_RESTRICTION_EQUATIONS.md
verify_p5_no_cubic_restriction_equations.py
```

### No quartic equations on the `P_5` restriction image

The quartic covariant pullback is injective too.  The four relevant
`S_4` types `[4]`, `[3,1]`, `[2,2]`, and `[2,1,1]` produce 839 ordered
module tuples with nonzero multiplicity, or 44 representatives under
mode permutation.  Multiplicities range from one to ten, while the full
Schur-dimension sum is

```text
binomial(246,4) = 148,897,035.
```

A compiled exact verifier constructs integer models of the four
representations, checks their character and matrix-unit relations, and
uses a four-copy subset dynamic program to contract deterministic local
covectors with `P_5`.  Exact row reduction modulo five reaches the full
theoretical multiplicity in every representative.  Since the
matrix-unit denominator 24 is invertible modulo five, these ranks lift
to `Q`.

Thus the full local-restriction image of `P_5` has no nonzero defining
equation of degree at most four.  This is a rigorous strategy boundary,
not a restriction to `Delta_3`; the next covariant search begins in
degree five.

```text
P5_NO_QUARTIC_RESTRICTION_EQUATIONS.md
verify_p5_no_quartic_restriction_equations.cpp
```

### Complete exact-three-coordinate `P_5` obstruction

The remaining partial-support layers of the exact-three-coordinate
branch are now closed simultaneously.  For a fixed coordinate backbone,
normalize a 19-edge spanning tree of the coefficient support graph and
form the all-full non-coordinate closure.  Saturate only the three pure
permanent coefficients; every non-tree coefficient remains allowed to
vanish.  A unit ideal on this chart therefore excludes every descendant
support containing the same tree.

Adaptive SAT/algebra CEGAR across all support-semantic viable coordinate
backbones retains:

```text
shape   viable backbones   core tree charts
C10                  127                401
C4+C6                 73                411
total                 200                812.
```

All 812 characteristic-zero Singular sources were regenerated and
freshly replayed as unit ideals.  The global support replay reconstructs
the covered 6,495-pattern pair-signature semantics and adds canonical
coordinate-backbone lex leaders.  It yields:

```text
C10:    100,254 variables, 1,293,318 clauses, UNSAT
C4+C6:  107,898 variables, 1,323,652 clauses, UNSAT.
```

CaDiCaL and Glucose both replay the two CNFs as UNSAT.  Kissat emits
45,389,314- and 48,012,550-byte binary DRAT traces, both independently
accepted by backward `drat-trim`.

This proves that a hypothetical `P_5 -> Delta_3` restriction must have
at least four coordinate rows in some local map.  It does not close that
high-coordinate branch and does not provide the arbitrary-order lift.

```text
P5_EXACT_THREE_COORDINATE_TREE_CHART_OBSTRUCTION.md
p5_pair_support_semantics.py
p5_tree_chart_cover.py
verify_p5_exact_three_coordinate_tree_chart_obstruction.py
research_snapshots/2026-07-27-p5-tree-chart-cover/
```

### High-coordinate `P_5` chart cover in progress

The remaining local-restriction branch has a mode with four or five
coordinate rows.  The chart driver at this checkpoint retained three
normalized mode-zero types:

```text
q4_211: one noncoordinate cell and singleton multiplicities 2,1,1
q5_311: five singleton cells with multiplicities 3,1,1
q5_221: five singleton cells with multiplicities 2,2,1.
```

They form a disjoint priority partition inside the subcatalogue handled
by that driver.  A later audit found that they do not exhaust all
high-coordinate signatures: partial `3+1` and `2+2` rows were omitted.
The active driver combines the 6,495 exact local pair signatures with
branch stabilizer lex leaders and pure-only gauge-chart certificates.

The chart implication has been strengthened.  A coefficient permitted
by the closure but not chosen as a gauge pivot may vanish, so exact
singleton support is not an antecedent.  The exact applicability
condition is instead:

```text
every entry outside the closure vanishes;
every gauge-forest pivot is present.
```

Normalized singleton conditions already forced by the branch are
omitted.  Earlier pure-only unit-ideal records can therefore be upgraded
to these stronger clauses without changing their algebraic sources.
Disconnected support graphs use maximal acyclic gauge forests rather
than an unjustified spanning tree.

The first sparse affine identities in the `q5_311` tail permit a
stronger implication.  Thirty-four distinct records remain unit ideals
after deleting every gauge pivot.  These records require only that
entries outside their support closure vanish; coefficients inside the
closure may all vanish independently, subject to the three pure
coefficients remaining nonzero.  Fresh split-Singular replay verifies
all 34 self-contained records.  The package SHA-256 is
`952fc788b171174020917f0c2287c172a8e4dd88b89f80ecb35c1f4ed6216bce`.

The driver can now probe this zero-pivot closure before using a maximal
forest.  An inconclusive one-second probe falls back to the previous
exact chart calculation; it is never interpreted as algebraic evidence.
The independent ledger verifier accepts nonmaximal forests, regenerates
their exact sources, and records both actual-support and gauge-forest
component counts.

The three ledgers were in progress at this checkpoint.  The later
analytic theorem excludes `q5_311` without a reconstructed branch CNF.
The `q5_221` and `q4_211` ledgers remain exploratory infrastructure
rather than theorems.

```text
p5_high_coordinate_tree_chart_cegar.py
verify_p5_high_coordinate_chart_ledgers.py
minimize_p5_high_coordinate_gauge_forest.py
certify_p5_high_coordinate_zero_forest_batch.py
package_p5_high_coordinate_zero_forest_seeds.py
generate_p5_one_partial_support_system.py
research_snapshots/2026-07-28-p5-high-coordinate-zero-forests/
```

### Five-root zero-coupling intersection

For arbitrary bilinear forms on the ten edges among five chosen
vertices, the ten internal zero-coupling equations always have a
simultaneous point in `(P^2)^5`.  If `h_i` denotes the hyperplane class
of factor `i`, the intersection class is

```text
product_(i<j) (h_i+h_j)
  = 24 h_0^2 h_1^2 h_2^2 h_3^2 h_4^2.
```

The coefficient counts orientations of `K_5` with indegree two at every
vertex.  There are 24 labeled regular tournaments, forming one orbit
with stabilizer order five.

This does not guarantee a fully supported root tuple: all intersection
multiplicity may lie on the union of the fifteen coordinate
hyperplanes.  It turns the next arbitrary-order question into a precise
toric-boundary problem and does not by itself solve the conjecture.

```text
FIVE_ROOT_ZERO_COUPLING_INTERSECTION_LEMMA.md
verify_five_root_zero_coupling_intersection.py
```

### High-coordinate chart orbits and the rare `q5_311` slices

The `q5_311` continuation now transports each exact chart through all
288 branch symmetries.  A deterministic gauge-tree portfolio avoids the
large runtime variation caused by normalization choice, while Linux-side
timeouts and a bounded retry for only `WSL/Service/E_UNEXPECTED` keep
algebra failures fail-closed.

Two consecutive family-learning ledgers contain 260 and 300 exact dynamic
representatives.  Retrospective bitset evaluation of the complete chart
orbits ranks the 300-ledger families by actual source-model coverage.  The
leading four distinct representatives cover 24, 23, 22, and 19 recorded
models.  Fixed-gauge closure enlargement frees 4--5 cells in each and
shrinks their clauses:

```text
record   old literals   new literals
146               26             20
140               27             21
196               18             16
276               26             20
```

All four enlarged sources regenerate, replay freshly as rational unit
ideals, and pass both SAT solvers at the representative-clause boundary.
The next continuation reconstructs 510,198 unique startup chart clauses.

The normalized mode-zero multiplicities `3,1,1` expose a smaller algebraic
mechanism.  Fixing either rare colour deletes its unique source row and
forces the other four maps to compress the resulting `P_4` tensor to a
nonzero decomposable tensor.  Keeping only those two mixed slices gives at
most 160 mixed equations.

On the frozen 300-record ledger:

```text
rare mixed plus all pure unit ideals: 300 / 300
certificate methods:                 298 direct, 2 split
accepted elapsed mean:                0.1096 seconds
majority mixed equations used:        0
```

If only the two rare pure coefficients are saturated, 298 direct unit
ideals remain.  One exceptional rare-only split ideal is proper and
positive-dimensional.  Adding only nonvanishing of the majority pure
coefficient closes both exceptional records in under half a second; no
majority-colour mixed equation is needed.  The evidence therefore
motivates a simultaneous two-deletion `P_4` classification under all three
pure nonvanishing conditions.  It is a uniform finite mechanism, not yet a
universal theorem.

The first analytic part of that classification is now complete.  If a
restriction of `P_4` through four rank-at-least-two maps is a nonzero
decomposable tensor, at most two maps can have rank three.  The proof uses
the complement-pairing flattenings.  A hyperplane--plane pair image has
dimension at least three, so three putative rank-three maps would force
all three hyperplanes to be the same coordinate-support-one-or-two
hyperplane.  The remaining fourth-mode slice space is then either a copy
of `P_3` or

```text
l * span{mn,ln,lm},
```

and neither contains a nonzero decomposable tensor.

Applied to the two rare deletions, each one forces at least two rank-drop
modes.  If the drop sets intersect, the three source rows common to both
deletions span one line and the rare rows complete it to rank three.  If
they do not intersect, they are complementary two-element subsets of the
four modes.  Thus every chart lies in one of two determinantal incidence
branches, independently of its support masks.

The primary symbolic verifier passes over `C`.  An independent `F_3`
audit enumerates 40 hyperplanes, 130 planes, 28,900 ordered pair images,
and all

```text
40^4 + 40^3*130 = 10,880,000
```

canonical ordered rank profiles `3333` and `3332`, fixing the rank-two
position by mode symmetry; none has all three `2|2` flattening ranks equal
to one.

```text
P4_DECOMPOSABLE_RESTRICTION_RANK_DROP.md
  a98b48863a56ffa3031abeffa091aed61661cf12f1401ea60e08544cfffe1886
verify_p4_decomposable_restriction_rank_drop.py
  e71075cc48ff4d79f9d073ca435fab2794676f37958d030ed3e4283ca8754c0c
audit_p4_decomposable_restriction_rank_drop.py
  f65035964e614db002cc5aa35a6470e15946f2054fe0301bd20f53b36443be06
tmp/p4_decomposable_restriction_rank_drop_verified.json
  7184f9affae43a720596237555cb4c640bdc14b99aa74abfa42250aece1c1ea9
tmp/p4_decomposable_restriction_rank_drop_audited.json
  c395e9b0b91a770c5926089cfa0982c576a8a9210cb1e30d8422d2406524f3c2
```

These hashes pin the first rank-drop theorem draft.  Later sharpness and
`q5_311` cross-links modify the theorem document, so this hash block is
historical and must be replaced by a fresh replay block before the new
analytic package is published.

One leading unrelaxed chart has exact degree-one identities with only
`+1` and `-1` coefficients.  Six Macaulay rows express the colour-one pure
coefficient using five distinct mixed coefficients, and five rows express
the colour-two pure coefficient using four.  A standalone verifier pins the
closure and gauge tree and expands both identities directly from all
permanent terms.

The next `q5_311` run was stopped after 360 exact records.  It contains 38
zero-gauge-forest closures, all distinct from the earlier 34.  Fresh replay
accepts all 72 combined split-Singular certificates, while CaDiCaL and
Glucose both leave the residual branch CNF SAT.

On the 38 new closures, rare mixed equations plus all three pure
nonvanishing conditions give 36 direct zero-forest unit ideals and two
timeouts.  Removing lex leaders and restricting the support CNF to only the
same 160 rare mixed words resolves both timeouts:

```text
zero record 12: 16 exact support charts, two-solver UNSAT
zero record 13: 25 exact support charts, two-solver UNSAT
fresh Singular: 41 / 41 UNIT_IDEAL
majority mixed support conditions: 0
```

This proves the rare mechanism on all 38 finite zero-forest closures, not
on the complete `q5_311` branch.

```text
P5_HIGH_COORDINATE_CHART_ORBIT_CEGAR.md
P5_Q5_311_RARE_SLICE_REDUCTION.md
P5_Q5_311_RARE_AFFINE_CORE.md
rank_p5_high_coordinate_chart_orbits.py
maximize_p5_high_coordinate_chart_closure.py
probe_p5_q5_311_rare_slice_core.py
cover_p5_q5_311_rare_slice_supports.py
verify_p5_q5_311_rare_affine_core.py
verify_p5_q5_311_rare_slice_support_cover.py
research_snapshots/2026-07-28-p5-q5-311-rare-zero-wave2/
```

### Exact rank-two `P_4` family and complete `P_3` plane geometry

The rank-drop theorem is sharp.  Four rank-two maps with coordinate rows

```text
U_0=(0,1,1,0)       V_0=(1,0,0,-1)
U_1=(0,0,1,1)       V_1=(1,1,-1,-1)
U_2=(0,1,0,1)       V_2=(-1,0,1,0)
U_3=(1,0,1,0)       V_3=(0,0,-1,1)
```

send `P_4` to `2 e_0 tensor e_0 tensor e_0 tensor e_0`.  All 15 mixed
coefficients vanish over the integers.  More generally this point lies in
a five-parameter family:

```text
g=e*i*l,

U_0=(0,1,(c+g)/e,c)
U_1=(0,0,1,e)
U_2=(0,1,0,g)
U_3=(1,0,i,0)

V_0=(1,j,0,-e*i*(1+l*j))
V_1=(l,1,-i*l,-g)
V_2=(-1/i,0,1,0)
V_3=(0,0,-1/e,1),
```

with `e*i*(c+e*i*l)` nonzero.  The pure coefficient is
`2(c+e*i*l)`.  Thus one deleted-`P_4` pure compression is genuinely
possible; simultaneous deletion compatibility is indispensable.

The order-three residual admits a complete exact classification.  A zero
restriction of `P_3` to three rank-at-least-two subspaces occurs exactly
when all three are the same coordinate plane.  A nonzero decomposable
restriction forces rank profile `222`; after mode/source permutations its
three plane normals are

```text
(1,A,B), (1,-A,-B), (1,-A,B),   (A,B)!=(0,0).
```

The proof expands the common-coordinate chart to a binary tensor with
zero antipodal corners.  Rank one forces support on one of six middle
cube edges.  Support-one normals and the distinct-missing-coordinate
boundary each give an explicit rank-two flattening obstruction.

For four planes whose every triple restriction is zero or pure, this
classification has an all-or-nothing corollary:

```text
all four triples zero:
  all four planes are one coordinate plane;

all four triples nonzero pure:
  the four normals form a complete projective sign rectangle.
```

In support two the rectangle has two copies of each sign variant; in
support three it has all four sign variants.

The exact statements and replay sources are:

```text
P4_DECOMPOSABLE_RANK_TWO_FAMILY.md
verify_p4_decomposable_rank_two_family.py
audit_p4_decomposable_rank_two_family.py

P3_ZERO_HYPERPLANE_PRODUCT_THEOREM.md
verify_p3_zero_hyperplane_product.py
audit_p3_zero_hyperplane_product.py

P3_DECOMPOSABLE_RESTRICTION_CLASSIFICATION.md
verify_p3_decomposable_restriction_classification.py
audit_p3_decomposable_restriction_classification.py
```

### Exact exclusion of normalized `q5_311`

The shared rank-drop branch is impossible.  In a shared mode the three
common rows lie on one line.  Contracting the two rare deleted slices
along their respective exceptional rows exposes the same residual
`P_3`, but forces it to be zero or a pure cube in each of two independent
target-colour directions.  No case is compatible.

The remaining disjoint `2+2` branch is impossible too.  The three common
rows have rank two in all four modes.  Contracting each non-drop mode
produces four common-row `P_3` restrictions, each zero or pure.  The
four-plane theorem forces them to be all zero or all pure.

The all-zero alternative kills one common source row in every remaining
mode, making each rare deleted-`P_4` slice zero.  In the all-pure
alternative, a nonzero contraction at one non-drop mode places its pure
factor inside the common image plane of the other non-drop mode, forcing
the latter contraction to be zero.  Both alternatives contradict the
rare slice identities.

Therefore the complete normalized `q5_311` branch is excluded over `C`.
This does not exclude normalized `q4_211`, normalized `q5_221`, the full
restriction `P_5 -> Delta_3`, or the arbitrary-order prize conjecture.

```text
P5_Q5_311_SHARED_DROP_OBSTRUCTION.md
verify_p5_q5_311_shared_drop_obstruction.py
audit_p5_q5_311_shared_drop_obstruction.py

P5_Q5_311_EXCLUSION_THEOREM.md
verify_p5_q5_311_exclusion.py
audit_p5_q5_311_exclusion.py
```

After host memory recovered, all six primary replays passed.  Four
independent audits also passed: the `P_3` zero theorem, the sharp
rank-two family, the shared-drop obstruction, and the final `q5_311`
case split.  The two deliberately large finite-field censuses for the
full nonzero-`P_3` classification and the `P_4` rank-drop theorem remain
pending; no passing claim is made for those two audit programs.

### Normalized `q5_221`: marked incidence and first exact obstruction

Normalize the distinguished mode by one simultaneous diagonal source
rescaling:

```text
u_0=(1,1,0,0,0),
u_1=(0,0,1,1,0),
u_2=(0,0,0,0,1).
```

The three contractions of `P_5` are embedded `P_4` tensors on
hyperplanes with independent normals

```text
h_0=(1,-1,0,0,0),
h_1=(0,0,1,-1,0),
h_2=(0,0,0,0,1).
```

For each remaining row space `U_i`, restriction to the colour-`c`
hyperplane has rank two exactly when `h_c in U_i`.  The `P_4` rank-drop
theorem therefore gives three drop sets `D_c`, each of size at least
two.

Selecting two incidences per colour gives six underlying uncoloured
three-edge multigraphs.  The singleton colour is invariant under the
normalized branch stabilizer, however, so double-plus-adjacent,
double-plus-disjoint, and the path each split according to the marked
edge.  The correct minimal list has nine marked types.  The earlier
six-type draft incorrectly quotiented by all of `S_3`; it was corrected
before verification or publication.

At a mode containing `h_c,h_d`, cross-contraction leaves

```text
Q_cd=(u_c,h_d) contract P_5,
```

and at least one of `Q_cd,Q_dc` maps to a nonzero pure cube.  Their six
source spaces are explicit sign pencils.  For example,

```text
J_01=span(e_0+e_1,e_2-e_3,e_4),
J_01^perp=span(h_0,u_1),

J_02=span(e_0+e_1,e_2,e_3),
J_02^perp=span(h_0,h_2).
```

For another mode the residual rank is

```text
3-dim(U_i intersect J_cd^perp).
```

The dimension-two case has rank one and is now recorded as an explicit
gate rather than being passed incorrectly to the rank-at-least-two
`P_3` theorem.

The first three exact marked incidence boundaries are closed.  If

```text
D_0=D_1={A,B}
```

and one shared endpoint, say `A`, also lies in `D_2`, then
`U_A=span(h_0,h_1,h_2)`.  Contracting the colour-zero identity at `B`
by `h_1` leaves `Q_01`.  The `A` restriction is a rank-two coordinate
plane with support-one normal, while the two modes outside `D_0` have
residual rank at least two.  The nonzero-pure `P_3` classification
rejects the support-one normal, so the residual is zero.  The zero
theorem forces both outside maps to kill `e_0+e_1`.  The symmetric
`Q_10` argument forces them to kill `e_2+e_3`.  Their two-dimensional
kernels are therefore exactly the span of those two vectors, so their
row spaces contain all three `h_c`, contradicting the exact drop sets.

The shared-endpoint argument first forces

```text
D_0=D_1={A,B},  D_2={C,D}.
```

The complementary case is impossible too.  At one paired-majority mode
the only rank-one residual exceptions are `u_0` or `u_1` in its row
space.  The opposite residual then has a support-one plane normal and
must be zero; the zero theorem would make a singleton-drop mode kill
`e_4`, contradicting containment of `h_2`.

Outside those exceptions, both cross residuals pass the
rank-at-least-two gate.  A nonzero `Q_01` forces the paired-majority
mode's plane normal to have support `{x_+,z}`, while a mode containing
`h_2` has a plane normal with zero `z` coordinate.  The nonzero `P_3`
classification requires the same support in all three modes, so
`Q_01` is zero.  Symmetrically `Q_10` is zero.  This contradicts the
local zero-diagonal cross-scalar lemma, which makes at least one of the
two residuals nonzero.

Therefore the two majority colours cannot have the same exact
two-element drop set.  This excludes the exact triple-parallel and the
two singleton-lone double-edge types (adjacent and disjoint).  It does
not yet exclude extra-containment strata, the other six minimal marked
types, normalized `q5_221`, the full `P_5` restriction, or the global
conjecture.

```text
P5_Q5_221_HYPERPLANE_INCIDENCE_REDUCTION.md
verify_p5_q5_221_hyperplane_incidence.py
audit_p5_q5_221_hyperplane_incidence.py

P5_Q5_221_PAIRED_MAJORITY_DROP_OBSTRUCTION.md
verify_p5_q5_221_paired_majority_drop.py
audit_p5_q5_221_paired_majority_drop.py

P5_Q5_221_MARKED_DOUBLE_ADJACENT_OBSTRUCTION.md
verify_p5_q5_221_marked_double_adjacent.py
audit_p5_q5_221_marked_double_adjacent.py
```

After host memory recovered, all four primary replays and all four
independent finite-field audits in this section passed.  This verifies
the stated exact-pattern reductions; it does not promote them to a
complete `q5_221` exclusion.

The singleton-doubled double-plus-adjacent exact type is impossible too.
After symmetry its drop sets are

```text
D_0=D_2={A,B},  D_1={A,C}.
```

Mode `A` contains all three normals.  Contracting `T_2` at `B` by
`h_0` gives a nonzero `Q_20` through `A,C,D`.  The all-normal plane has
normal `y_+`; containment of `h_1` forces the same sign at `C`, so the
support-two `P_3` chart forces the opposite sign `y_-` at `D`.

Repeating `Q_20` from `A` leaves one possible rank-one exception,
`u_0 in U_B`.  In that case both `Q_12` and `Q_21` see a support-one
plane at `B`, so neither can be nonzero, contradicting the local
cross-scalar lemma.  Otherwise the mode-`B` `Q_20` normal is `y_+` or
`y_-`.

For the `y_+` sign,

```text
U_B=span(h_0,h_2,h_1+a u_0),  a!=0.
```

The `Q_12` zero theorem makes `C,D` kill `y_+`.  The forced nonzero
`Q_21` then has rank three at `C`, contradicting the nonzero `P_3`
classification.

For the `y_-` sign,

```text
U_B=span(h_0,h_2,u_1+a u_0).
```

If `a!=0`, the `Q_21` zero theorem makes `C` kill `y_-`, contrary to
`h_1 in U_C`.  If `a=0`, `Q_12` requires common normal support
`{e_0,e_1}`.  But the earlier `n_C=y_+` condition removes every
`u_1` component from `U_C`, leaving a support-one `J_12` normal.  This
is the final contradiction.

Thus four of the nine marked exact-six-incidence types are now closed.

The singleton-doubled double-plus-disjoint exact type is now excluded
too:

```text
D_0=D_2={A,B},  D_1={C,D}.
```

Repeated `h_2` contraction forces a nonzero `Q_20` direction.  Its
support-two `P_3` chart makes the `C,D` normals `y_+`, so both maps kill
`y_+`.  The only rank-one exception is handled by the opposite
`h_1` endpoint and forces the same conclusion.

On the colour-two hyperplane, the `C,D` row spaces are the common
hyperplane

```text
H=span(h_0,u_0,h_1)=y_+^perp.
```

The exact complement pairing in the `AB|CD` flattening forces one
doubled row plane to be

```text
K_0=span(h_0,u_0).
```

The key cancellations are `mu(u_0,h_0)=0` and orthogonality of
`mu(u_1,h_0)` to the four-dimensional pair image `A(H,H)`.  Two
nonexceptional planes create an independent flattening row and are
impossible.

Double contraction by `h_1` at `C,D` leaves a nondegenerate
`P_2(e_0,e_1)`.  It forces the other doubled plane to be

```text
K_1=span(h_0,u_1).
```

Finally, `T_1=Sym(e_0,e_1,y_+,z)` assigns `y_+` uniquely to the `K_1`
mode.  The residual `P_3(e_0,e_1,z)` has rank profile `322`, contrary
to the nonzero decomposable `P_3` classification.

```text
P5_Q5_221_MARKED_DOUBLE_DISJOINT_OBSTRUCTION.md
verify_p5_q5_221_marked_double_disjoint.py
audit_p5_q5_221_marked_double_disjoint.py
```

At this checkpoint, five of the nine marked exact-six-incidence types
were closed.  The triangle, star, two marked paths, and all
extra-containment strata remained open.

### Exact triangle type closed

For

```text
D_0={A,B}, D_1={A,C}, D_2={B,C},
```

double contraction by `h_2` leaves two complementary-support
chiralities, not one symmetry class.  In the chirality with nonzero
`Q_02` at `B` and `Q_12` at `C`, the two mode-`A` plane normals have
full three-coordinate support.  The nonzero decomposable-`P_3`
classification forces the adjacent mode-`B` and mode-`C` normals to
have the same full support.

Carrying all of those nonzero coordinates forward removes the two
apparent rank-one exceptions in the earlier draft.  Mode `C` has rank
three on `J_01`, mode `B` has rank three on `J_10`, and every other map
has residual rank at least two.  Hence both `Q_01` and `Q_10` must be
zero, contradicting the local cross-scalar lemma that makes at least one
nonzero.

This exactly excludes the first triangle chirality over `C`.

The opposite chirality uses the same cross-scalar pair but reverses the
two nonzero repeated-`h_2` residuals.  At `B`, the only rank-one
`Q_01` gate is supported on `h_2`, whose target image is colour one
rather than the required colour zero.  Outside that gate, mode `C`
has either rank three or a support-one normal.  Thus `Q_01=0`.
Symmetrically, the only rank-one `Q_10` gate at `C` lands in colour zero
rather than colour one; every other branch has a rank-three mode or
support-one normal.  Thus `Q_10=0`, again contradicting the cross-scalar
lemma.

This closes the complete exact triangle type over `C`.  A primary
symbolic replay and an independent `F_3/F_5` incidence audit pass.  Six
of the nine exact minimal types were closed at this checkpoint.

```text
P5_Q5_221_TRIANGLE_OBSTRUCTION.md
verify_p5_q5_221_triangle_obstruction.py
audit_p5_q5_221_triangle_obstruction.py
P5_Q5_221_TRIANGLE_WORKING_NOTE.md
```

### Exact star type closed

For the exact star, the central row space is
`span(h_0,h_1,h_2)`.  If `alpha_c` pulls back to `h_c`, its own-colour
entry is zero.  The three `alpha_c` form a basis, so their
zero-diagonal target-coordinate matrix has determinant

```text
q_10 q_21 q_02 + q_20 q_01 q_12 != 0.
```

Thus one of the two directed cross-residual cycles is entirely
nonzero.  In the cycle `Q_20,Q_01,Q_12`, the `Q_01` normal-support
conflict forces its colour-zero leaf to be rank one.  The `Q_12`
support-two chart then fixes normals `(u_0,h_0,h_0)`, while `Q_20`
forces the singleton-colour leaf to be rank one.  The resulting factor
directions pin the only row components needed in the colour-two slice.

For target colouring `(0,1,1,0)`, its coefficient factors as

```text
per(u_0,u_0 on e_0,e_1)
per(h_1,h_1 on e_2,e_3)
  = -4
```

times nonzero scalars.  A possible target-row shear cancels identically.
This forbidden coefficient contradicts the pure colour-two `P_4`
identity.  Swapping the majority colours excludes the other directed
cycle.

The symbolic verifier and an independent exact polynomial-permutation
audit pass.  At this checkpoint, seven of the nine exact minimal types
were closed; the two marked paths and all extra-containment strata
remained open.

```text
P5_Q5_221_STAR_OBSTRUCTION.md
verify_p5_q5_221_star_obstruction.py
audit_p5_q5_221_star_obstruction.py
```

### Both exact marked paths closed

The marked-end path is

```text
D_0={C,D}, D_1={B,D}, D_2={A,C}.
```

At `D`, a nonzero `Q_01` forces the mode-`C` rank-one gate and hence a
nonzero `Q_02`; a nonzero `Q_10` forces the mode-`B` rank-one gate.  In
the `Q_02` branch, either that second gate or the `AC|BD`
complement-pairing bound makes the `B,D` colour-two hyperplanes equal
to `u_1^perp`.  The `Q_02` sign chart then fixes normals
`(h_1,u_1,u_1)` and factor directions `(u_0,h_1,h_1)`.  A required
all-colour-one coefficient and the forbidden target colouring
`(2,1,1,1)` of `T_2` are nonzero multiples of the same two-row
permanent, a contradiction.

If `Q_02=0`, then `Q_01=0` and the opposite residuals `Q_10,Q_20` are
nonzero.  The vanished cross scalars pin

```text
L_C^* epsilon_1 in C^*h_2,
L_D^* epsilon_2 in C^*h_1.
```

If `Q_20` has rank one at `A`, the required all-colour-one coefficient
of `T_1` contains `per(u_0,h_0)=0`.  Otherwise the `Q_20` sign chart
fixes the same normal pattern `(h_1,u_1,u_1)`.  The required
all-colour-one coefficient is `-4cs`, while the forbidden colouring
`(1,0,1,0)` is `4Ccs`; required nonvanishing makes the forbidden
coefficient nonzero.  This closes the marked-end path over `C`.

The marked-middle path is

```text
D_0={B,D}, D_1={A,C}, D_2={C,D}.
```

Double contraction by `h_2` at `C,D` makes their two target covectors
have complementary singleton supports.  Thus either `Q_12,Q_02` are
both nonzero or `Q_21,Q_20` are both nonzero.

Let `K_i=ker L_i`.  A rank-two residual plane normal is the projective
line `K_i intersect J_cd`.  Because all four relevant residual spaces
lie in `h_2^perp`, exact absence of `h_2` at `A,B` makes the two
overlapping residual normal lines coincide at each mode.

In the first chirality, the common lines lie in
`J_12 intersect J_02=span(u_0,u_1)`.  Together with `h_0 in U_D`,
all three `Q_12` normals have equal first two coordinates.  A
full-support `P_3` chart needs three distinct vertices of a sign
rectangle but only two satisfy that equality; no support-two boundary
works either.  In the second chirality,
`J_21 intersect J_20=span(h_0,h_1)`.  The incidences at `A,B` force
the common lines to `h_0,h_1`, so the `Q_21` normal at `B` has support
one.  Both chiralities are impossible.

The two primary symbolic replays and two independent audits pass.  The
marked-middle audit enumerates only the 42 abstract oriented `P_3`
sign triples, not ambient row spaces; the marked-end audit checks its
small pair-image lemma over `F_3,F_5` and independently expands the
decisive coefficients.

```text
P5_Q5_221_MARKED_END_PATH_OBSTRUCTION.md
verify_p5_q5_221_marked_end_path.py
audit_p5_q5_221_marked_end_path.py

P5_Q5_221_MARKED_MIDDLE_PATH_OBSTRUCTION.md
verify_p5_q5_221_marked_middle_path.py
audit_p5_q5_221_marked_middle_path.py
```

All nine exact minimal marked incidence types are now excluded over
`C`.  This does not yet exclude normalized `q5_221`: the exact
theorems assume no unselected normal containments, and every
extra-containment stratum still needs a sound lifting argument.  The
full `P_5` restriction and the global conjecture remain open.

### Extra-containment cover reduction

The remaining incidence poset does not require a separate list at every
incidence count from seven through twelve.  From any pattern with
`|D_c|>=2` and at least seven total incidences, choose two incidences per
colour and then one additional incidence.  This produces a
seven-incidence subpattern with row-size multiset `{3,2,2}`.

Quotienting these cover patterns by the four mode permutations and the
swap of majority colours zero and one gives exactly fourteen marked
orbits.  A separate construction starts from the nine minimal marked
edge orbits, adds one incidence, and obtains the same fourteen covers.
Their mode-degree profiles are

```text
(3,3,1,0): 2
(3,2,2,0): 2
(3,2,1,1): 5
(2,2,2,1): 5.
```

The first nine covers have at least one all-normal mode, hence a fixed
kernel `span(u_0,u_1)`.  The final five have no fixed kernel; their
three double-incidence modes lie on the pairwise Schubert divisors
`h_c^perp intersect h_d^perp`.

This reduces complete normalized `q5_221` exclusion to fourteen
monotone obstruction theorems.  “Monotone” is essential: each theorem
must allow every undisplayed containment, so the already-proved exact
six-incidence results cannot simply be cited.

The triangle proof does lift one step without a new case split.  Its
mode-`D` rank gates use only

```text
h_0 notin U_D,  h_1 notin U_D;
```

they do not use `h_2 notin U_D`.  Therefore the same proof excludes

```text
D_0={A,B}, D_1={A,C}, D_2={B,C,D}
```

with no other containments.  Finite-field audits over `F_3,F_5`
confirm that adding exactly `h_2` at `D` leaves the two direct residual
ranks equal to two and both cross residual ranks at least two.

This closes the exact open stratum of cover `#4` in the fourteen-orbit
table.  It does not close that cover monotonically: adding `h_0` or
`h_1` at `D` can create a new cross-residual rank-one gate.

The majority-singleton triangle cover closes too.  By majority symmetry
take `h_0 in U_D` and exclude `h_1,h_2`.  The only new cross escape is
a rank-one `Q_01` gate, which has the form

```text
U_D=span(h_0,u_1,a u_0+b h_1+c h_2).
```

Its `Q_02` plane normal is `(b,-a,a)`, while its `J_12`
determinant is `-4a`.  In the first chirality, full `Q_02` support
forces `a,b!=0`, so `Q_12` has rank three.  In the other chirality,
rank two on `J_12` forces `a=0`, leaving the forbidden support-one
`Q_02` normal `u_0`.  Thus exact cover `#12` is excluded as well.

The two marked triangle-plus-singleton open strata are now closed.
Their monotone closures remain open because an eighth incidence changes
the rank-one gate analysis.

### Repeated-majority-pair seven-incidence obstruction

Exact cover `#8` has two modes `P,Q` containing `h_0,h_1`, a mode `R`
containing `h_1,h_2`, and a mode `S` containing only `h_2`.  Double
contraction at `P,Q` produces the two bilinear channels

```text
Sym(u_0,h_2) -> x_P x_Q e_0 tensor e_0,
Sym(u_1,h_2) -> y_P y_Q e_1 tensor e_1.
```

The rank-one sum lemma for `a tensor z'+z tensor a'` and exact absence
of the undisplayed normals force all four cross scalars to be nonzero.
The `Q_01,Q_10,Q_12` residual gates then give

```text
U_P=U_Q=span(h_0,h_1,u_1),
U_R=span(h_1,h_2,u_0),
n_S,12=h_0,
```

together with the target factor pins needed for a simultaneous
four-map normal form.  In that chart, direct polarization gives

```text
T_0[0000] = 4b(p_0q_0-1),
T_0[0020] = 4f(p_0q_0-1),
T_2[2222] = 4Cfp_2q_2.
```

The first coefficient is required nonzero and the second forbidden, so
`f=0`; the third required coefficient then vanishes.  This excludes
the exact seven-incidence stratum without enumerating row spaces or
maps.  Its monotone closure remains open.

```text
P5_Q5_221_REPEATED_MAJORITY_PAIR_COVER_OBSTRUCTION.md
verify_p5_q5_221_repeated_majority_pair_cover.py
audit_p5_q5_221_repeated_majority_pair_cover.py
```

### Distinguished-normal multiplicity is exactly two

The singleton-colour normal admits a monotone upper bound.  Suppose
three modes `A,B,C` contain `h_2`.  Double contraction of

```text
T_0=Sym(u_0,e_2,e_3,h_2)
```

at `A,B` by their `h_2` pullbacks is zero, so one pullback has zero
target-zero coordinate.  Its own target-two coordinate is already
zero; hence it is a nonzero multiple of `epsilon_1`.  Contracting

```text
T_1=Sym(e_0,e_1,u_1,h_2)
```

at that mode leaves a nonzero pure `Q_12` through the other three
modes.  At the two remaining `h_2` modes, apolarity to the `Q_12`
source space and the own-colour equation force their target-zero rows
to be multiples of `h_2`.  The required `T_0[0000]` coefficient then
contains two `h_2` contractions and vanishes.

Together with the earlier rank-drop lower bound, this proves

```text
|D_2|=2
```

without any absence assumption on `h_0,h_1`.  It monotonically excludes
cover orbits `#0--#4,#9`; the remaining monotone frontier is
`#5,#6,#7,#8,#10,#11,#12,#13`.  The primary verifier expands the
polarized tensors, while the independent audit differentiates the
squarefree polynomial representatives.  Neither enumerates maps or
row spaces.

```text
P5_Q5_221_DISTINGUISHED_NORMAL_MULTIPLICITY_THEOREM.md
verify_p5_q5_221_distinguished_normal_multiplicity.py
audit_p5_q5_221_distinguished_normal_multiplicity.py
```

### Final exact no-fixed-kernel cover

Cover `#13` has two modes containing `h_1,h_2`, one containing
`h_0,h_1`, and one containing only `h_0`.  Double `h_2` contraction of
`T_1` orients the repeated pair and forces a nonzero pure `Q_02`.
All three residual ranks are two.  Because the first two residual
planes contain `h_1`, their normals have equal last two coordinates.
The `P_3` classification leaves a support-two and a full-support
stratum.

In support two, the factor directions are `h_1,h_1,u_0`.  A nonzero
`Q_01` then forces a rank-one gate at the singleton mode.  The required
target-two rows lie in

```text
C h_1,  span(u_0,h_0),  span(u_0,h_0),  span(u_1,h_0).
```

Their `T_2` coefficient is zero: the `h_0` component has the wrong
`3+1` block degree, while the `u_1` component contains the zero
bilinear permanent `Perm_2(h_1,u_1)`.

In full support, the active and inactive rows at the two repeated-pair
modes differ by nonzero multiples of `h_1`.  Three mixed coefficients
and the required pure coefficient form a four-corner rectangle.  Its
alternating difference is

```text
T_2(h_1,h_1,h_1,S_2)=0,
```

so the supposedly forbidden fourth corner equals the required nonzero
corner.  This closes the last exact no-fixed-kernel cover without
searching maps or row spaces.  Its monotone boundary remains open.

```text
P5_Q5_221_COVER_13_OBSTRUCTION.md
verify_p5_q5_221_cover_13.py
audit_p5_q5_221_cover_13.py
```

### Monotone two-all-normal obstruction

The complementary-support orientation of the two `h_2` pullbacks
closes cover `#5` monotonically.  If both distinguished modes are
all-normal, contracting them leaves three nonzero bilinear tensors
through the other two modes:

```text
Sym(u_0,h_1) -> e_0 tensor e_0,
Sym(h_0,u_1) -> e_1 tensor e_1,
Sym(h_0,h_1) -> e_2 tensor e_2.
```

Each rank-one two-summand tensor forces its source pair to become
dependent at one endpoint.  The three dependency edges are

```text
{a,d}, {b,c}, {b,d}.
```

Colouring them by the two endpoints forces one endpoint to receive two
edges.  Any two of these edges leave at most two connected components
among `a,b,c,d`, so that endpoint has image rank at most two.  But the
two non-distinguished modes avoid `h_2` and therefore have rank three
on `H_2`.  This contradiction allows arbitrary additional majority
normal containments and hence proves the whole monotone cover.

```text
P5_Q5_221_TWO_ALL_NORMAL_MODES_OBSTRUCTION.md
verify_p5_q5_221_two_all_normal_modes.py
audit_p5_q5_221_two_all_normal_modes.py
```

### Monotone all-normal-partner obstruction

Covers `#6,#11` have one all-normal `h_2` mode and a second `h_2`
mode containing `h_1`.  The complementary target support of the two
`h_2` pullbacks gives two orientations.  In the first, the nonzero
`Q_02` sign chart closes by the same block-apolar dichotomy as cover
`#13`.

The second orientation requires a separate argument.  A preliminary
draft incorrectly claimed that the all-normal inverse forced `Q_21`.
Writing the full zero-diagonal pullback matrix exposes the correct
directed cycle

```text
Q_20 -> e_2^3,
Q_01 -> e_0^3,
Q_12 -> e_1^3.
```

If `Q_20` has rank two at the partner mode, its support-two sign chart
and the rank-three `Q_01` gate force the `Q_20` and `Q_01` factor lines
at the third `h_1` mode to coincide.  If it has rank one, contracting
at that mode leaves the two nondegenerate bilinear pairs

```text
Sym(h_0,h_1), Sym(u_0,u_1).
```

Their dependency endpoints must be opposite because both remaining
maps have rank three on `H_2`.  The rank-one `Q_01` gate then makes its
factor line coincide with one of those two bilinear factor lines.
Either branch asks one local line to map to two distinct target
colours, a contradiction.

The primary verifier reconstructs the zero-diagonal determinant, both
orientation-I strata, the support-two `Q_20` chart, and every bilinear
factorization.  The independent audit differentiates the squarefree
polynomials and checks the factor-line alternatives separately.  No
ambient maps or row spaces are enumerated.  Thus covers `#6,#11` are
closed monotonically, leaving

```text
#7,#8,#10,#12,#13.
```

```text
P5_Q5_221_H1_PARTNER_ALL_NORMAL_OBSTRUCTION.md
verify_p5_q5_221_h1_partner_all_normal.py
audit_p5_q5_221_h1_partner_all_normal.py
```

### Remaining fixed-kernel covers closed

The same directed-cycle viewpoint closes covers `#7,#10`
monotonically.  For `#7`, one orientation forces the support-two
`Q_12` chart

```text
normals: u_0,h_0,h_0,
factors: u_1,u_0,u_0.
```

A rank-one `Q_01` contraction then makes its factor at the third
majority mode equal to the same `u_0` line, despite a different target
colour.  In the opposite orientation, the `Q_02` chart makes two
`Q_21` restrictions invertible.  A nonzero directional derivative of
a squarefree cubic has matrix rank at least two, so it cannot become a
pure product through those maps.

For `#10`, the `Q_20` rank-one branch gives a support-one `Q_01`
normal, while its rank-two branch makes the other two `Q_01` maps
invertible.  The opposite orientation forces a `Q_20` residual whose
three kernel normals all satisfy the same coordinate equality; a valid
`P_3` sign chart has too few vertices in that slice.

```text
P5_Q5_221_REMAINING_FIXED_KERNEL_OBSTRUCTION.md
verify_p5_q5_221_remaining_fixed_kernel.py
audit_p5_q5_221_remaining_fixed_kernel.py
```

### Complete normalized `q5_221` exclusion

With eleven cover orbits closed monotonically, a fresh incidence-poset
audit shows that strict extensions of exact covers `#8,#12,#13` leave
only two eighth-incidence orbits:

```text
0011 1111 1100
0111 1011 1100.
```

Every ninth-incidence extension already contains one of the eleven
monotone covers.  In the repeated-pair boundary, a forced `Q_02`
residual has rank profile `222`, but all three kernel normals lie in
the common-coordinate slice, impossible in either the support-two or
full-support `P_3` sign chart.

The four-cycle boundary has two orientations.  One gives the same
`Q_02` contradiction.  In the other, independent `h_0` and `h_1`
cross pullbacks double-contract

```text
T_2=Sym(e_0,e_1,e_2,e_3)
```

to `Sym(h_0,h_1)` through two modes containing both covectors.  Both
maps are injective on `span(h_0,h_1)`, so the bilinear rank remains two
and cannot equal the required nonzero pure target product.

Together with the nine exact-six and fourteen cover-layer results,
this excludes the complete normalized `q5_221` branch over `C`.
Primary symbolic and independent apolar/projective audits pass.  The
separate normalized `q4_211` branch, the full `P_5 -> Delta_3`
restriction, and the global conjecture remain open.

```text
P5_Q5_221_FINAL_MONOTONE_BOUNDARY_OBSTRUCTION.md
verify_p5_q5_221_final_monotone_boundary.py
audit_p5_q5_221_final_monotone_boundary.py
```

```text
P5_Q5_221_EXTRA_CONTAINMENT_REDUCTION.md
verify_p5_q5_221_extra_containment_reduction.py
audit_p5_q5_221_extra_containment_reduction.py
```

### Normalized `q4_211` as a simultaneous diagonal pencil

The then-last branch inside the original three-type high-coordinate
partition has a chart-free deformation-theoretic reduction.  Normalize
the distinguished local map so its target-coordinate pullbacks are

```text
u_0=(a,1,1,0,0),
u_1=(b,0,0,1,0),
u_2=(c,0,0,0,1),
```

with at least two of `a,b,c` nonzero.  The four remaining maps must send
these three contractions to the three independent pure target tensors.
Consequently they diagonalize the entire three-plane
`span(u_0,u_1,u_2)`.

Projecting the contraction map away from the three diagonal target
words gives a `78 x 5` matrix.  A `q4_211` solution forces its kernel to
contain the displayed three-plane, hence

```text
off-diagonal rank <= 2,
diagonal rank on the kernel >= 3.
```

On the source-coordinate-zero slice, this becomes the projective
support-four pencil

```text
a t_0+b t_1+c t_2=0.
```

For `abc != 0`, its coordinate boundary is one support-two and two
support-three contractions mapping to the three `Delta_2` boundaries.
The two singleton-colour contractions are embedded `P_4` tensors with
normals

```text
h_1=(b,0,0,-1,0),
h_2=(c,0,0,0,-1),
```

so their rank drops select two edges on four modes: parallel, adjacent,
or disjoint.  If `a=0`, the doubled-colour contraction is a third
embedded `P_4`; if `a!=0`, it is `a b q` with ternary quadratic
determinant `2a`.

The known positive support-four construction does not lift.  Its
off-diagonal matrix has exact rank four, kernel
`span(1,1,1,1,0)`, and diagonal image `(12,12,12)`.  Nineteen
`4 x 4` minors and an exact two-variable elimination prove rank four
at every point of the published two-parameter family.  The primary
characteristic-zero verifier and independent `F_5/F_7` audit pass.

This is a structural checkpoint, not an exclusion of `q4_211`.
The remaining target is the exceptional rank-at-most-two
determinantal locus coupled to the two `P_4` incidence edges.

```text
P5_Q4_211_SIMULTANEOUS_PENCIL_REDUCTION.md
verify_p5_q4_211_simultaneous_pencil.py
audit_p5_q4_211_simultaneous_pencil.py
```

### Generic parallel `q4_211` incidence as a diagonal pencil

Assume `bc != 0` and two remaining modes `A,B` contain both singleton
normals

```text
h_1=(b,0,0,-1,0), h_2=(c,0,0,0,-1).
```

If the pullbacks of these normals at `i=A,B` are

```text
x_i=(r_i,0,q_i), y_i=(s_i,p_i,0),
```

then exact double contraction identifies the common complementary
bilinear residual

```text
G=(L_C tensor L_D) Sym(e_1,e_2)
```

with `p_Ap_B e_1^2` and `q_Aq_B e_2^2`, up to nonzero
scalars.  Hence `G` is zero or a pure tensor on exactly one singleton
line.

Put `s=e_1+e_2`, `d=e_1-e_2`, and
`X=span(e_0,e_3,e_4)`.  Three contractions of the doubled colour give

```text
L_C(s) tensor L_D(v)+L_C(v) tensor L_D(s)
 in span(e_0^2,G) for every v in X.
```

This is a diagonal matrix-pencil condition.  Each map has rank three,
so its image on `span(s)+X` has dimension at least two.  If both
`L_C(s),L_D(s)` are nonzero, the pencil must contain a rank-two
diagonal; its row and column spaces force both restricted map images
into the same target two-plane.  The identity

```text
G=(L_C(s) tensor L_D(s)-L_C(d) tensor L_D(d))/2
```

then contradicts rank three.  Exactly one zero gives an impossible
two-dimensional fixed-factor subspace of a diagonal plane.  Therefore

```text
L_C(s)=L_D(s)=0.
```

If `G=0`, one complementary map also kills `d`, so its kernel is
`span(e_1,e_2)` and its row space contains both normals.  This creates
a third common incidence and reduces to the adjacent extra-containment
type.  If `G != 0`, both restrictions to `span(e_1,e_2)` instead have
the common kernel `span(s)` and the same singleton target image.

The latter apparent exception is impossible.  Suppose for example
that `G` lies on the target `e_1^2` line.  Quotienting the complementary
modes by `e_1` in `u_2 contract P_5` forces the original common modes
to map `span(e_1,e_2)` onto `e_2`.  Quotienting those modes by `e_2`
then gives two rank-two maps on `X` with the same kernel

```text
span(e_0+b e_3+c e_4).
```

The same `u_2` contraction would require the quotient image of
`Sym(e_3,e_0+c e_4)` to vanish.  Modulo the common kernel it is
`-2b e_3^2`, nonzero because `b != 0`.  The colour-swapped residual is
`-2c e_4^2`.  Thus every parallel pattern on `bc != 0` has a third
common incidence and can be reselected as adjacent.  The boundaries
`b=0`, `c=0`, and the adjacent and disjoint incidence types remain
open.

```text
P5_Q4_211_PARALLEL_INCIDENCE_KERNEL_REDUCTION.md
verify_p5_q4_211_parallel_incidence.py
audit_p5_q4_211_parallel_incidence.py
```

### Adjacent `q4_211` incidence as a marked `P_4` pencil

Let a mode `A` contain both `h_1,h_2`, with target pullbacks

```text
x_A=(r,0,q), y_A=(t,p,0).
```

They are independent, so `(p,q)!=(0,0)`.  Quotient the target by their
common annihilator line.  The induced map kills
`E=span(e_1,e_2)` and has rank two on
`X=span(e_0,e_3,e_4)`, with kernel

```text
span(e_0+b e_3+c e_4).
```

For

```text
w_+=e_0+b e_3-c e_4,
w_-=e_0-b e_3+c e_4,
```

the determinant of the three `X`-vectors `k,w_+,w_-` is `-4bc`.
Thus the quotient maps `span(w_+,w_-)` isomorphically.  Applied to

```text
R=Sym(e_1,e_2,w_+,w_-),
```

the four maps give

```text
q bar L_A(w_+) tensor e_2^3
+p bar L_A(w_-) tensor e_1^3.
```

If exactly one scalar is nonzero, this is a nonzero pure `P_4` image.
The order-four rank-drop theorem forces another map to have rank two on
`H=span(e_1,e_2,w_+,w_-)`, equivalently to contain its normal

```text
n=(0,0,0,c,b).
```

If both scalars are nonzero, the image is `Delta_2`.  Since `P_4` has
exact subrank two, this is a sharp marked boundary, not a contradiction.

```text
P5_Q4_211_ADJACENT_P4_PENCIL_REDUCTION.md
verify_p5_q4_211_adjacent_p4_pencil.py
audit_p5_q4_211_adjacent_p4_pencil.py
```

### Marked `P_4 -> Delta_2` slice classification and obstruction

Fix the common-mode row plane

```text
U_0=span(e_2^*,e_3^*)
```

in the basis `(e_1,e_2,w_+,w_-)`.  A marked `Delta_2` restriction is
equivalent to two coordinate-deleted `P_3` restrictions, one supported
only at `alpha_1 alpha_2 alpha_3` and the other only at
`beta_1 beta_2 beta_3`.

If either slice has a rank-one local map, its annihilating singleton row
is `e_2^*` or `e_3^*` modulo the normal
`n=(0,0,0,c,b)`.  Otherwise the two nonzero decomposable-`P_3` sign
charts are compatible only when each uses the coordinate omitted by
the other as its common coordinate.  Up to symmetries their rows are

```text
alpha_1=(0,1,T,-B)       beta_1=(1,0,0,-A)
alpha_2=(1,0,0, A)       beta_2=(0,1,-T,B)
alpha_3=(1,0,0, A)       beta_3=(B,A,-AT,0),
```

with `AT != 0`.  The two diagonal coefficients are `2A,-2AT`; all
fourteen mixed coefficients vanish.

This family is incompatible with adjacent q4 incidence.  Assign its
three planes in any order to the `h_1` mode, `h_2` mode, and remaining
mode.  Adding `e_3^*` and `e_2^*` at the first two modes makes their
pair image the full six-space.  The common quotient plane paired with
the third marked plane has dimension four.  Complement pairing
therefore forces the `2|2` flattening rank to be at least

```text
6+4-6=4,
```

contradicting `rank(Delta_2)=2`.  Hence the generic adjacent boundary
is confined to a row space containing `n` or a singleton target row in

```text
C h_1+C n or C h_2+C n.
```

```text
P4_MARKED_DELTA2_SLICE_CLASSIFICATION.md
verify_p4_marked_delta2_slice_classification.py
audit_p4_marked_delta2_slice_classification.py

P5_Q4_211_MARKED_DELTA2_PAIR_IMAGE_OBSTRUCTION.md
verify_p5_q4_211_marked_delta2_pair_image.py
audit_p5_q4_211_marked_delta2_pair_image.py
```

### Alternating-gate classification and ambient obstruction

The residual rank-one marked boundary is also exact.  A gate in one
coordinate-deleted pure `P_3` slice forces a gate in the other slice.
There is exactly one gate of each kind and they occur at distinct
modes.  Normalize them as

```text
beta_1=e_2^*,   alpha_2=e_3^*.
```

Writing the shared-coordinate directions as `(p,q)` and `(r,t)`, put

```text
lambda=pt+qr != 0,   Delta=pt-qr.
```

The fourteen mixed vanishings reduce to only four equations:

```text
lambda y_j-Delta z_j=0,
-lambda x_j-Delta d_j=0,   j=2,3.
```

For `Delta != 0` these give one transverse normal form.  For
`Delta=0`, nonvanishing forces the directions proportional with
`pq != 0`, and the equations give a tangent normal form.  Thus the
gate boundary is a two-stratum orbit classification rather than an
ambient search.

The full third-colour lift closes both strata.  In the transverse
stratum the three one-mode slice matrices have rank four, with witness
minors

```text
-Delta^4 lambda^3,
-Delta^4 lambda^3,
-Delta^2 lambda.
```

All three third-colour rows therefore vanish on
`H=span(e_1,e_2,w_+,w_-)` and are nonzero multiples of
`n=(0,0,0,c,b)`.  Triple contraction by `n` is zero on `P_5` but leaves
the nonzero doubled-colour diagonal term on the target.

In the tangent stratum the slice ranks are `4,4,2`; the third kernel is
`span(e_2^*,e_3^*)`.  The first two third-colour rows are multiples of
`n`, so their double contraction exposes the nonzero `P_3` on
`span(e_0,e_1,e_2)`.  The tangent marked rows have independent
`e_1,e_2` projections of determinant `-2pq`.  The decomposable-`P_3`
rank and common-support theorem then contradicts both possible
singleton-incidence placements.

Consequently the whole adjacent branch with two nonzero cross
residuals is empty on `bc != 0`.  The only remaining adjacent outcome
is the one-cross case, where another ambient row space actually
contains `n`.

```text
P4_MARKED_DELTA2_ALTERNATING_GATE_CLASSIFICATION.md
verify_p4_marked_delta2_alternating_gate.py
audit_p4_marked_delta2_alternating_gate.py

P5_Q4_211_ALTERNATING_GATE_OBSTRUCTION.md
verify_p5_q4_211_alternating_gate_obstruction.py
audit_p5_q4_211_alternating_gate_obstruction.py
```

### One-cross normal-pencil saturation

In the remaining adjacent orientation `q != 0,p=0`, the common mode
pulls `h_2` back from target colour zero.  The other three maps satisfy
simultaneously

```text
P_3(e_1,e_2,w_-) -> nonzero e_2^3,
P_3(e_1,e_2,w_+) -> 0.
```

The zero-`P_3` theorem forces a rank-one local restriction: the
all-rank-two alternative would kill `e_1`, `e_2`, or `w_+`; the first
two kill the nonzero residual and the last contradicts
`h_2(w_+)=2c`.  Hence one remaining row space contains the whole
opposite pencil `span(h_1,n)`.  Colour interchange forces
`span(h_2,n)` in the other orientation.

The fourth normal has a fixed target colour.  Put

```text
m=c u_1-b u_2=(0,0,0,c,-b).
```

Since `(m,n) contract P_5=0`, independence of the two singleton target
cubes forces every target covector pulling back to `n` to be a
multiple of `e_0^*`.

The nonzero residual gives a second pencil.  Unless a mode contains
its whole normal plane or the common mode kills `e_1+e_2`, its three
rank-two intersections are projective lines.  Polarizing the
permanent on `span(h_2,n)` gives

```text
Perm_3(Ah_2+Bn)^3=6ABc^2(-A+bB).
```

The known lines `h_2,n` force the third line to the third root
`b h_2+n=c u_1`.  The colour-swapped cubic similarly forces
`c h_1+n=b u_2`.  Thus the one-cross branch is reduced to mandatory
opposite-pencil incidence plus explicit double-normal, common-kernel,
or rigid three-root boundaries.

```text
P5_Q4_211_ONE_CROSS_PENCIL_SATURATION_REDUCTION.md
verify_p5_q4_211_one_cross_pencil_saturation.py
audit_p5_q4_211_one_cross_pencil_saturation.py
```

### One-cross direction conic and four-gate core

The mandatory opposite-pencil mode and the common mode both pull their
new normals from target colour zero.  Contracting them with `u_0`
exposes the same nondegenerate ternary quadratic used in the disjoint
polarity theorem.  Unless one remaining row space contains the whole
direction plane `span(u_1,u_2)`, the two restrictions have rank two
and polar kernels.

Polarizing the direction pencil gives

```text
Perm_3(h_2,Au_1+Bu_2,Cu_1+Du_2)=-2bAC,
Perm_3(n,Au_1+Bu_2,Cu_1+Du_2)
 =2(Ab+Bc)(Cb+Dc).
```

Away from the two common-kernel lines, the `q` orientation therefore
forces direction lines `{u_2,c u_1-bu_2}`; the `p` orientation forces
`{u_1,c u_1-bu_2}`.  Combining this with the normal-pencil cubic
eliminates the free polar core: the unselected mode would contain both
`u_1` and `c u_1-bu_2` (or both `u_2` and that line), forcing the full
direction plane.  The adjacent one-cross branch is now confined to a
second common singleton-normal mode, a double-normal plane, the full
direction plane, or a common `e_1+e_2` kernel.

```text
P5_Q4_211_ONE_CROSS_DIRECTION_CONIC_REDUCTION.md
verify_p5_q4_211_one_cross_direction_conic.py
audit_p5_q4_211_one_cross_direction_conic.py
```

### Exact disjoint `q4_211` incidence as a conic polarity

Assume `abc != 0` and the exact disjoint containment pattern

```text
h_1 in R_A,R_B only,
h_2 in R_C,R_D only.
```

Put

```text
s=e_1+e_2,
d=e_1-e_2,
w=e_0-b e_3-c e_4,
H=span(s,d,w).
```

The mixed contraction

```text
Q=(u_0,h_1,h_2) contract P_5
```

is represented on `H`, up to scale, by

```text
M=[[a/2,0,1],[0,-a/2,0],[1,0,0]],
det(M)=a/2.
```

Every cross pair in `{A,B}|{C,D}` maps `Q` to the doubled target-colour
line, so its matrix rank is at most one.  No local restriction to `H`
can have rank one: its row space would contain all of `H^perp`, and
`c h_1-b h_2 in H^perp` would force the absent singleton normal.
Sylvester's inequality then excludes rank three, leaving rank two at
all four modes.

Let `k_i` be the four restricted kernel lines.  The applicable
singleton normal shows `k_i in span(s,d)`.  A cross-pair image has rank
one exactly when

```text
k_i^T M^(-1) k_j=0.
```

The restriction of `M^(-1)` to `span(s,d)` is

```text
[[0,0],[0,-2/a]].
```

Writing `k_i=sigma_i s+delta_i d`, the four polarities are the
`K_(2,2)` equations `delta_i delta_j=0`.  Therefore either

```text
k_A=k_B=span(s)
```

or

```text
k_C=k_D=span(s).
```

This reduces the generic exact disjoint type to one colour-symmetric
common-kernel boundary.  It does not yet exclude that boundary.

```text
P5_Q4_211_DISJOINT_CONIC_POLARITY_REDUCTION.md
verify_p5_q4_211_disjoint_conic_polarity.py
audit_p5_q4_211_disjoint_conic_polarity.py
```

### Exact disjoint `q4_211` exclusion

Assume `k_A=k_B=span(s)`.  Repeated `h_2` contraction shows that the
`d` images at `A,B` are nonzero target-colour-one vectors and that one
`h_2` row, say at `C`, pulls back from pure target colour one.  The
fourfold identity

```text
(u_0,h_1,h_1,h_2) contract P_5=2b s
```

then forces `L_D(s)=0`.  Repeating `h_1` leaves exactly two kernel
architectures:

```text
(s,s,s,s)
or
(s,s,d,s).
```

In the `3s+1d` architecture one `h_1` row pulls back from target colour
zero.  The zero residual

```text
(u_2,h_1) contract P_5=-P_3(e_1,e_2,w_-)
```

collapses to

```text
-2 L_B(e_1) tensor L_C(w_-) tensor L_D(e_1).
```

Thus `L_C(w_-)=0`; together with `L_C(d)=0` this puts
`n=(0,0,0,c,b)` in `R_C`.  But `n` pulls back from target colour zero
while the `h_2` row at `C` pulls back from target colour one.  Both
annihilate `span(e_1,e_2,w_-)`, forcing its image to target colour two,
contrary to the already nonzero target-colour-zero vector `L_C(s)`.

In the all-`s` architecture, `d` maps to target colour one at `A,B`
and target colour two at `C,D`.  Modulo the common `s` kernel, the
`u_0` contraction has two `d` factors.  No assignment of those factors
can contribute to the required `e_0^4` coefficient, so that nonzero
diagonal coefficient vanishes.  Therefore exact disjoint incidence is
empty on `abc != 0`.

```text
P5_Q4_211_DISJOINT_EXCLUSION_THEOREM.md
verify_p5_q4_211_disjoint_exclusion.py
audit_p5_q4_211_disjoint_exclusion.py
```

### Adjacent one-cross two-gate reduction

The direction-conic and normal-pencil constraints first leave four
gates.  A common `h_1,h_2` mode cannot also contain

```text
n=(0,0,0,c,b),
```

because independence would make both cross residuals nonzero, already
excluded by the alternating-gate theorem.  If a second common mode
exists, the parallel theorem produces exactly three common modes and
one `n`-mode.  Mixed common-mode orientations put all three normals in
the `n`-mode; a uniform orientation contradicts

```text
(h_1,h_1,h_1) contract P_5
=(h_2,h_2,h_2) contract P_5=0.
```

Thus a second common mode is impossible.  The double-normal gate is
absorbed by the fixed direction lines from the conic: either line
completes the mode to a forbidden common-plus-`n` row space unless a
full direction plane or common kernel is already present.  Only

```text
span(u_1,u_2) subset R_Z
```

or

```text
L_A(e_1+e_2)=0 or L_Y(e_1+e_2)=0
```

remains.

```text
P5_Q4_211_ONE_CROSS_TWO_GATE_REDUCTION.md
verify_p5_q4_211_one_cross_two_gate.py
audit_p5_q4_211_one_cross_two_gate.py
```

### Direction-plane gate obstruction

If `R_Z` contains `span(u_1,u_2)`, its rank-one conic image fixes

```text
L_Z^*e_1^* in C u_1,
L_Z^*e_2^* in C u_2.
```

Indeed both pullback covectors annihilate target `e_0`, and symmetry of
the mixed `(u_1,u_2)` contraction kills their off-diagonal entries.
In the `q` orientation, both the common mode `A` and the mandatory
`span(h_1,n)` mode `Y` send `span(e_1,e_2)` into target colour one.
But

```text
(u_2,u_2) contract P_5
 =2c P_3(e_1,e_2,e_3)
```

would have to map through `A,Y` and one other mode to a nonzero pure
target-colour-two cube.  Every source monomial assigns an
`e_1` or `e_2` factor to at least one of `A,Y`, so that coefficient is
zero.  Colour interchange handles the `p` orientation.

```text
P5_Q4_211_ONE_CROSS_DIRECTION_PLANE_OBSTRUCTION.md
verify_p5_q4_211_one_cross_direction_plane.py
audit_p5_q4_211_one_cross_direction_plane.py
```

### Common-kernel gate obstruction

In the `q` orientation, let `C` be the other selected `h_2` mode and
`D` the fourth mode.  The zero and nonzero repeated-normal
contractions

```text
(u_1,h_2,h_2)=-2c Sym(e_1,e_2),
(u_2,h_1,h_1)=-2b Sym(e_1,e_2)
```

give a binary polar pair through `Y,D` and a pure target-colour-two
pair through `C,D`.  Fourfold contraction by
`(u_0,h_1,h_2,n)` then forces

```text
L_D(s)=0,
L_Y(d)=0,
s=e_1+e_2,
d=e_1-e_2.
```

Thus the alleged common-kernel gate must be `L_A(s)=0`, and the
remaining pure pair gives `L_C(d) in C^*e_2`.  The contraction
`(u_0,h_2,h_2,n)` makes the selected `h_2` row at `C` pure target
colour one.

The target `e_0^4` coefficient of `u_0 contract P_5` factors as

```text
e_0^*L_C(s) *
Perm_3(rho_A|X,rho_Y|X,rho_D|X),
X=span(e_0,e_3,e_4),
```

so `L_C(s)` has a nonzero colour-zero component.  Under the propagated
sigma/delta kernels, both residual charts reduce to

```text
-L_Y(w) tensor L_C(d) tensor L_D(e_1)
+L_Y(e_1) tensor L_C(s) tensor L_D(w).
```

The nonzero pure `w_-` chart forces `L_D(w_-)=0`.  Since
`s,w_-,w_+` are independent and `ker L_D` has dimension two,
`L_D(w_+)!=0`.  The zero `w_+` chart then equates two nonzero
decomposable tensors and forces `L_C(s) in C e_2`, contradicting its
colour-zero component.  This excludes the last adjacent one-cross
gate.

```text
P5_Q4_211_ONE_CROSS_COMMON_KERNEL_OBSTRUCTION.md
verify_p5_q4_211_one_cross_common_kernel.py
audit_p5_q4_211_one_cross_common_kernel.py
```

### Generic normalized `q4_211` exclusion

For `abc != 0`, the two singleton-normal containment sets each have
size at least two.  Empty intersection is exact disjoint incidence;
one common mode is adjacent; two common modes are parallel and force a
third, hence reselect as adjacent.  Exact disjoint incidence, adjacent
two-cross incidence, and adjacent one-cross incidence are all excluded
by the preceding theorems.  Therefore normalized `q4_211` is empty on
the open parameter stratum.

The only remaining normalized parameter strata are

```text
a=0, b c!=0;
b=0, a c!=0;
c=0, a b!=0.
```

The last two are colour symmetric.

```text
P5_Q4_211_GENERIC_EXCLUSION_THEOREM.md
verify_p5_q4_211_generic_exclusion.py
audit_p5_q4_211_generic_exclusion.py
```

### Complete normalized `q4_211` exclusion

All three parameter faces are now closed without an ambient-map search.
On `b=0` (and symmetrically `c=0`), exact coordinate-normal incidence
leaves one marked architecture.  Its two target-image alternatives are
excluded by a binary polar system coupled to two simultaneous `P_3`
charts.

On `a=0`, the doubled-colour contraction becomes a third embedded
`P_4`.  In the adjacent one-cross branch, the relevant pair of row
planes lies on a degeneracy locus in `Gr(2,4)`.  Exact Pluecker
elimination reduces it to five ordered complete-quadrangle pairs, each
with a constant nonzero complementary flattening minor.  In exact
disjoint incidence, a zero marked corner makes one `P_3` slice vanish;
three direct evaluations force the remaining rows into one coordinate
hyperplane, and the decomposable-`P_3` classification gives an
incompatible antipodal binary cube.

The parameter package covers `abc!=0`, the three one-zero faces, and
the zero-row closure.  The latter was initially missed because the
sentence “fewer than two nonzero parameters means a coordinate row”
does not include the all-zero row.  It is excluded by the
two-singleton theorem below.  Thus the complete partial `q4_211`
subbranch is empty over `C`.

```text
P5_Q4_211_B0_FINAL_OBSTRUCTION.md
P5_Q4_211_A0_ADJACENT_GRASSMANN_OBSTRUCTION.md
P5_Q4_211_A0_DISJOINT_P3_OBSTRUCTION.md
P5_Q4_211_EXCLUSION_THEOREM.md
verify_p5_q4_211_exclusion.py
audit_p5_q4_211_exclusion.py
```

### Two-singleton theorem and corrected high-coordinate frontier

The `q5_311` proof uses less than its original normal form.  It needs
only two independent target coordinates whose pullbacks are supported
on two distinct singleton source rows.  Contracting those target
coordinates exposes two pure deleted copies of `P_4` sharing three
source rows.  The existing rank-drop, shared-drop, and common-plane
arguments exclude the configuration independently of all entries in
the third target coordinate.

An independent rebuild of the 6,495-signature catalogue finds exactly
360 two-singleton signatures:

```text
60  exact q5_311;
180 q4_211 coordinate rows plus one zero row;
120 partial 3+1 rows with support counts (4,1,1).
```

This audit also corrected the former three-type high-coordinate claim.
There are 1,680 catalogue signatures with at least four coordinate
rows.  Exact theorems exclude 1,170.  The remaining 510 are:

```text
H31, 240 signatures:
  e_0,e_0,e_0,e_1,a e_0+b e_1+c e_2,  b c!=0;

H22, 270 signatures:
  e_0,e_0,e_1,e_1,a e_0+b e_1+c e_2,  c!=0,
                                               (a,b)!=(0,0).
```

For `H31`, deleting the partial source row gives `P_4 -> pure`, while
deleting the singleton row gives a second embedded `P_4 -> Delta_2`;
the two tensors share three source rows.  For `H22`, contraction by
`e_0+e_1`, `e_2+e_3`, and `e_4` gives three embedded copies of `P_4`
with normals

```text
e_0^*-e_1^*, e_2^*-e_3^*, e_4^*.
```

The last maps pure and the first two map pure or to `Delta_2`, with at
least one sharp `Delta_2` image.  This reframes the current problem as
compatibility between a pure deletion and one or two marked
sharp-subrank-two deletions.  It is not a proof of nonexistence or a
construction.

```text
P5_TWO_SINGLETON_COORDINATE_OBSTRUCTION.md
verify_p5_two_singleton_coordinate_obstruction.py
audit_p5_two_singleton_coordinate_obstruction.py
P5_HIGH_COORDINATE_PARTIAL_FRONTIER.md
verify_p5_high_coordinate_partial_frontier.py
audit_p5_high_coordinate_partial_frontier.py
```

### The known rank-two pure family does not lift to `H31`

Fix the five-parameter family `P4_DECOMPOSABLE_RANK_TWO_FAMILY.md` on
the pure-deletion hyperplane and retain its three common source
coordinates on the neighbouring `Delta_2` hyperplane.  The fourteen
mixed binary coefficients are linear in the eight new exceptional-row
entries.

For `l!=0`, an explicit `7 x 7` minor is

```text
-4 i^2 l^4(c+e i l)/e^4.
```

The unique mixed-kernel direction kills the second diagonal, so no
binary `Delta_2` extension exists.  For `l=0`, the mixed matrix has
rank six and a two-dimensional kernel.  A sharp binary extension
exists precisely when

```text
j u(c t+e u) != 0.
```

This exceptional binary survivor still has no ternary lift.  At mode
one, the one-third-row coefficient map on the `Delta_2` hyperplane has
nonzero determinant

```text
8 j u^2(c t+e u)/(e^4 i),
```

so the third row vanishes there.  On the pure hyperplane the analogous
map has kernel exactly `C e_1^*`, transverse to the remaining
exceptional coordinate.  The third row is therefore globally zero and
the local map has rank at most two.

Independent modular row reduction checks all 1,600/10,584 admissible
family parameters over `F_5/F_7`.  It finds 4,096/46,656 binary
`Delta_2` extension vectors, all on the predicted divisor, and zero
third-row lifts.  No ambient local maps or Grassmannians are enumerated.

```text
P5_H31_KNOWN_RANK_TWO_FAMILY_OBSTRUCTION.md
verify_p5_h31_known_rank_two_family_obstruction.py
audit_p5_h31_known_rank_two_family_obstruction.py
```

### Complete exclusion of the `H31` single-gate boundary

Let the pure and `Delta_2` source hyperplanes share the source
three-space `M`.  A rank-one pair on the pure hyperplane is a unique
primary coordinate gate.  If all three remaining pairs have rank two
on `M`, the marked decomposable-`P_3` classification gives

```text
alpha_1=(-B,0,1), beta_1=(-A,1,0),
alpha_2=( A,1,0), beta_2=( B,0,1),
alpha_3=( A,1,0), beta_3=( 0,B,A).
```

Binary extension through the primary `beta` row is a `7 x 7` linear
system.  Its determinant is the product of seven projective lines, and
the exact viable locus is the union of four punctured components:

```text
B=0;
v_1=0;
v_2=0;
v_0=-A v_1+B v_2,
```

with the explicit open conditions recorded in
`P5_H31_SINGLE_GATE_P3_REDUCTION.md`.  Ten disjoint determinantal
strata have a transverse injective one-marked map.  Their sole deepest
intersection forces the two remaining third rows onto kernel lines,
where the mixed target coefficient `1122` is the nonzero binary
diagonal up to scale.  Hence no ternary lift exists.

If another pair drops rank on `M`, its wrong marked row vanishes there
and becomes a unique secondary gate.  The remaining common-plane data
is a `P_3 -> Delta_2` restriction.  For the pair map

```text
mu(x,y)=(
 x_1y_2+x_2y_1,
 x_0y_2+x_2y_0,
 x_0y_1+x_1y_0
),
```

a full three-dimensional pair image makes the secondary one-marked map
injective.  Rank two forces two off-diagonal pair products to vanish.
The exact classification of `mu(x,y)=0` leaves only:

```text
one coordinate line against its complementary plane;
two distinct coordinate planes.
```

Both support-polarity strata have explicit normal forms.  Their
one-marked determinant cascades either give an immediate transverse
contradiction or force a deepest form in which a mixed two-third-row
coefficient is nonzero.  Thus every single-gate `H31` pencil is
impossible.

Independent audits over `F_5,F_7` checked:

```text
2,036 / 8,538 viable projective extensions in the rank-two-M chart;
2,500 / 14,406 ordered deepest extension pairs;
120 / 252 exceptional zero-pair basis quadruples;
both support-polarity determinant cascades and deepest coefficients.
```

No ambient local maps or Grassmannians were enumerated.  The honest
`H31` remainder is now only the all-rank-two pure-`P_4` locus outside
the dense known-family charts, including possible all-rank-two
component boundaries and additional components.

```text
P5_H31_SINGLE_GATE_P3_REDUCTION.md
verify_p5_h31_single_gate_p3_reduction.py
audit_p5_h31_single_gate_p3_reduction.py
P5_H31_SINGLE_GATE_RANK_TWO_M_EXCLUSION.md
verify_p5_h31_single_gate_rank_two_m_exclusion.py
audit_p5_h31_single_gate_rank_two_m_exclusion.py
P5_H31_SECONDARY_GATE_EXCLUSION.md
verify_p5_h31_secondary_gate_exclusion.py
audit_p5_h31_secondary_gate_exclusion.py
```

### The rank-two family is a plane component; its canonical marked orbit does not lift

Put four rank-two source planes in the Grassmann chart

```text
R_0=((1,0,a,b),(0,1,c,d)),
R_1=((e,1,0,f),(g,0,1,h)),
R_2=((i,1,0,j),(k,0,1,l)),
R_3=((1,m,n,0),(0,o,p,1)).
```

In the Segre chart anchored at target word `1000`, decomposability is
the fifteen incidence equations

```text
T_beta-T_1000 product_{r:beta_r!=1000_r} z_r=0.
```

At family parameters `(E,I,L,Q,C)=(1,1,1,1,0)`, the compressed tensor
is `2(y_0-x_0)(x_1+y_1)x_2x_3`.  A `15 x 15` incidence-Jacobian minor
has determinant `-4096`, so the local incidence dimension is five.  A
`5 x 5` minor of the family tangent map has determinant `2`.  Hence the
family closure is a generically smooth five-dimensional irreducible
component, not merely a dimension-count construction.  This does not
classify other components or all-rank-two boundary points.

The earlier `H31` lift obstruction fixed one of four possible family
source coordinates as the coordinate replaced in the neighbouring
hyperplane.  The three missing orientations have exact mixed-extension
matrices.  On `L!=0`, each has rank seven and its unique kernel kills
the `AAAA` diagonal.  On `L=0`, their ranks are `6,3,5`.  The middle
orientation still kills `AAAA` identically.  For the other two,
mode-one marked minors are

```text
-8 I Q t^2(EI t+C u)/E
```

and

```text
8 t(Ct+Eu)(It-Qu-v)/(EI),
8 u(Ct+Eu)(It-Qu-v)/(EI).
```

The relevant diagonal nonvanishing makes the first determinant
nonzero, or at least one determinant in the second pair nonzero.  The
third-colour row therefore vanishes on the neighbouring hyperplane and
is supported only on the distinguished pure coordinate.  A pure-slice
marked coefficient, respectively `Q` or `1`, rules out that support.

Thus every displayed marked family chart in the full source/mode
symmetry orbit has no `H31` lift.  This statement concerns the chosen
row markings, not every marked basis over the same plane component.
The independent `F_5/F_7` audit checked all
admissible parameter tuples in the three new orientations and, on the
largest exceptional stratum, 63,504 projective binary extensions.
Every genuine `Delta_2` extension had the predicted injective marked
map.  No ambient local maps or Grassmannians were enumerated.

```text
P4_PURE_RANK_TWO_COMPONENT_THEOREM.md
verify_p4_pure_rank_two_component.py
audit_p4_pure_rank_two_component.py
P5_H31_RANK_TWO_COMPONENT_ORBIT_OBSTRUCTION.md
verify_p5_h31_rank_two_component_orbit.py
audit_p5_h31_rank_two_component_orbit.py
```

### Exact component-chart closure and exclusion of its nonzero boundary

Eliminating the five family parameters in the preferred Grassmann
chart gives eleven elementary component equations:

```text
f=g=i=l=m=o=0,
hp+1=nk+1=0,
j-hne=hc-d-j=b-h(a-n)=0.
```

The chart is irreducible of dimension five with free coordinates
`a,d,e,h,n`, where `hn!=0`.  Put `D=d+hne`.  The restricted tensor is

```text
2(ah x_0+D y_0)(en x_1+y_1)x_2x_3.
```

The original finite-parameter family is exactly `D!=0`, with inverse

```text
E=h, I=n, L=e, C=d, Q=-ah/D.
```

The only additional nonzero locus in this chart is therefore the
four-dimensional divisor `D=0,a!=0`.  Any other boundary of the
component must lie where one of

```text
Delta_0(01), Delta_1(12), Delta_2(12), Delta_3(03)
```

vanishes.

On `D=0,a!=0`, a binary basis change gives the pure coefficient
`AAAA=2AH`.  The four neighbouring mixed-extension matrices split by
`R!=0`, the collision `A=N`, and `R=0`.  Every binary `Delta_2`
survivor has an injective one-marked map.  Representative determinants
are

```text
8HNR(t+Hu)(Nt-H(A-N)u)^2,
8Au^2(t+HNRu),
8H^2N^3R^2tu^2,
-8H^2NR^3u^2(t+HNRu),
8AHN^3t^2u,
8Ht^2(Nu-H(A-N)v),
8Atu^2.
```

The pure-hyperplane marked map rejects the distinguished source
coordinate in every case, so the third target row vanishes globally.
Thus the displayed marked section of the nonzero preferred-chart
boundary is excluded in all four orientations.  Kernel-row shifts
inside the same planes were not parameters of this calculation.

The independent audit checked all 320/1,512 boundary parameter points
over `F_5/F_7` and all 4,608/31,104 projective binary `Delta_2`
extensions.  Every survivor had the predicted injective marked map.
No ambient local maps or Grassmannians were enumerated.

```text
P4_PURE_RANK_TWO_COMPONENT_CHART_CLOSURE.md
verify_p4_pure_rank_two_component_chart_closure.py
audit_p4_pure_rank_two_component_chart_closure.py
P5_H31_COMPONENT_CHART_BOUNDARY_OBSTRUCTION.md
verify_p5_h31_component_chart_boundary.py
audit_p5_h31_component_chart_boundary.py
```

### Marked-basis scope correction and an open shifted branch

The component calculations above live in `Gr(2,4)^4` and therefore
remember only four planes.  An `H31` map marks more data in each plane:
a kernel row and a complementary pure-colour row.  Replacing the latter
by itself plus a multiple of the kernel row preserves both the plane
and the pure deletion, but is not a symmetry of the neighbouring
`Delta_2` tensor.

This distinction produces a genuine dense binary branch.  Normalize
`E=I=1` and put

```text
D=C+L,  A=1+LQ,  B=1+DQ,
LQDAB !=0.
```

Keep the family kernel rows `alpha_r`, but replace the canonical
pure-colour rows `U_r` by

```text
beta_r=U_r+t_r alpha_r,
t=(-1/Q,0,L/A,0).
```

All four planes are unchanged.  On the pure hyperplane only
`BBBB=2D` survives.  For distinguished source coordinate `q=2`, the
fifth-coordinate extension

```text
x=(1,0,0,-1),
y=(B/Q,1,0,0)
```

kills all fourteen mixed binary coefficients and has nonzero
diagonals

```text
AAAA=-2A,  BBBB=2B/Q.
```

So the earlier canonical statement “off `L=0` there is no binary
extension” cannot be promoted from its marked row family to the whole
plane component.

The new branch still fails ternarily.  At mode two, rows
`000,001,011,111` of the one-marked map have determinant

```text
8 A^2 B.
```

The pure marked map has distinguished-coordinate entry `A`, so the
third target row vanishes globally.  A primary symbolic verifier and
an independent dynamic-programming audit over all 36/150 admissible
parameter tuples in `F_5/F_7` both pass.

This correction also changes the interpretation of the toric work.
The coupled base has 12 divisors, 26 edges, and 16 vertices; Segre
intersection leaves 21 all-rank toric plane/orientation pairs.  That is
an exact plane-level frontier, not yet a complete marked `H31`
frontier.  The finite component-interior fibre is classified in the
next checkpoint; the 21 toric cases remain.

```text
P5_H31_MARKED_BASIS_OPEN_BRANCH.md
verify_p5_h31_marked_basis_open_branch.py
audit_p5_h31_marked_basis_open_branch.py
P4_PURE_RANK_TWO_COMPONENT_TORIC_BOUNDARY.md
P4_PURE_RANK_TWO_TORIC_SLICE_SEGRE_REDUCTION.md
```

### Complete marked-basis fibre over the finite family chart

The Borel fibre over the normalized family is

```text
beta_r=U_r+t_r alpha_r,       t in C^4,
D=C+L!=0.
```

This is exhaustive: the pure tensor fixes the kernel line
`C alpha_r` in each plane, and nonzero row scalings reduce every
complement to `U_r+t_r alpha_r`.  The original `E,I` parameters are
removed by the invertible source scaling

```text
diag(EI,EI,E,1),
```

with a bijective corresponding rescaling of `t`.

For distinguished source coordinate `q`, binary extension is the
determinantal incidence

```text
M_q(t)z=0,        d_0(z)d_1(z)!=0,
```

where `M_q(t)` is `14 x 8`.  Exact elimination after the weighted
normalizations

```text
L!=0: (c,qbar,s)=(C/L,LQ,t_0/L,Lt_1,t_2/L,t_3),
L=0:  C=1
```

gives the complete constructible marking table.  The generic branches
are the expected `A=0`, `B=0`, and shifted `q=2,3` sections, together
with the `L=0` marking lines and axes.  A completeness audit found three
previously missed isolated `q=1` markings:

```text
C=-L/2, Q=-2/L: ( L/2,0, L,1),
C=-L/2, Q=-1/L: (   0,1/L,-L,0),
C=-L/2, Q=   0: (-L/2,0, L,1).
```

They are not closure artifacts: their mixed matrices have rank six and
both diagonal functionals are nonzero on the two-dimensional kernel.
The specialized normalized projection has triangular basis

```text
2s_0+qbar+1,
s_1+qbar^2+2qbar,
s_2-2qbar^2-4qbar-1,
s_3-qbar^2-2qbar-1,
qbar(qbar+1)(qbar+2).
```

Every survivor kernel is now obstructed **for all extensions**.  Each
useful one-marked determinant factors as

```text
d_0(z)d_1(z) ell(z).
```

The residual linear forms either repeat a diagonal factor or form a
spanning cover of the extension kernel.  The largest new kernel is the
three-dimensional `L=0,q=2` fibre; for `Q!=0` three residuals are

```text
u-w,  u-Qv,  Qv+w,
```

whose common zero is the origin.  Separate bases handle
`2C+L=0`, `T=D`, `S=0,1`, and `Q=0`; no generic kernel basis is
specialized through a pole.

The primary symbolic verifier passes 20 exact certificate strata.  An
independent implementation exhausts the normalized projection
varieties over `F_5,F_7`, checks 426 surviving markings and all 6,234
projective kernel directions, and finds 4,498 admissible binary
extensions.  Every admissible extension has an injective one-marked
map with a transverse pure coordinate.  It also rejects 32
`L=0` Zariski-closure points that are not actual incidence points.

Therefore no marked basis over any finite member of the known
five-parameter family lifts to `H31`.  The global conjecture remains
unresolved: the next known-component target is the full marked
incidence over the 21 Segre-capable toric boundary orientations, and
additional pure-compression components remain unclassified.

```text
P5_H31_MARKED_BASIS_FIBRE_CLASSIFICATION.md
derive_p5_h31_marked_basis_fibre_elimination.py
verify_p5_h31_marked_basis_fibre_classification.py
audit_p5_h31_marked_basis_fibre_classification.py
```

### Complete marked fibres on the genuine toric boundary

The coupled three-plane toric boundary was first reduced at plane level
to five genuine divisor orbits and four edge orbits.  Accounting for
the two pure directions on secants, the double direction on the
tangent slice, and distinguished-source orientations gives 17
pure-direction types and 39 direction/orientation types over 21
base-orbit/orientation cases.

The complete marked incidence is now closed.  Both projective charts
of the first-plane fibre, every kernel-row shift, and every binary
extension direction are excluded by exact selected-minor unit ideals
over characteristic zero.  The independent orientation-aware audit
exhausts 13,064 exact oriented projection points, 272,624 genuine
binary extensions, 291,176 selected-minor tests, and 520
projection-closure artifacts over `F_5,F_7`.

```text
P5_H31_TORIC_MARKED_FIBRE_OBSTRUCTION.md
derive_p5_h31_toric_marked_fibre_elimination.py
verify_p5_h31_toric_marked_fibre_obstruction.py
audit_p5_h31_toric_marked_fibre_obstruction.py
```

### Complete marked fibre on the nonzero component-chart divisor

The full row-basis bundle on the nonzero preferred-chart divisor
normalizes to `H=N=1`, `A!=0`, with four bijective row shifts.  Four
saturated projection ideals split into 16 elementary residual-factor
strata.  On every stratum a selected one-marked determinant is a
nonzero parameter multiple of one of the two inverted binary
diagonals, so every binary extension is ternarily excluded.

The characteristic-zero primary verifier passes all 16 strata.  The
independent audit checks 614 projection points, 5,400 binary
extensions, 6,918 selected-minor tests, and 12 closure artifacts over
`F_5,F_7`.

```text
P5_H31_COMPONENT_CHART_BOUNDARY_MARKED_FIBRE_OBSTRUCTION.md
derive_p5_h31_chart_boundary_marked_fibre_elimination.py
verify_p5_h31_component_chart_boundary_marked_fibre.py
audit_p5_h31_component_chart_boundary_marked_fibre.py
```

### Complete marked fibre on first-plane infinity

The line at infinity of the first-plane fibre normalizes by

```text
diag(N,N,1,1/H)
```

to `H=N=1`, `(A,D)!=(0,0)`, with a bijective action on all four row
shifts.  Absolute binary incidence for `q=0,1,2,3` has respectively
`4,3,6,8` minimal projection components.  Those 21 components admit a
25-chart rational atlas.  Exact kernel reconstruction gives 18
two-dimensional and 7 three-dimensional mixed kernels; after
inverting both binary diagonals and the chart parameters, the 154
selected pure-entry/minor residual products have no common zero.

The primary characteristic-zero verifier passes in full.  An
independent audit exhausts 1,054 projection points, 14,796 binary
extensions, and 24,202 selected-minor tests over `F_5,F_7`, while
correctly rejecting 72 projection-closure artifacts.

Thus the finite family, genuine toric boundary, nonzero chart divisor,
and first-plane infinity are closed at complete marked-fibre level.
The known-component remainder is the internal `E=0` marked fibre.
Additional pure-compression components and `H22` remain unresolved;
the prize problem is not solved.

```text
P5_H31_COMPONENT_FIBRE_INFINITY_MARKED_FIBRE_OBSTRUCTION.md
derive_p5_h31_fibre_infinity_marked_fibre_elimination.py
verify_p5_h31_component_fibre_infinity_marked_fibre.py
audit_p5_h31_component_fibre_infinity_marked_fibre.py
```

### Complete marked fibre on the internal `E=0` divisor

The last unclassified stratum of the known component is the internal
toric divisor with normal `(-1,0,0)`.  Its pure slice is secant, with
directions `(-1,-1)` and `(1,-1)`, and its all-rank distinguished
coordinates are `q=0,2,3`.  Including both projective charts of the
first-plane fibre gives twelve exact saturated binary projections.
Their squarefree decompositions have 24 components.

A 29-chart rational atlas isolates all kernel-pivot divisors.  One
chart is a genuine projection-closure artifact because a binary
diagonal vanishes identically.  Twenty-seven ordinary charts close by
characteristic-zero residual unit ideals, checking 1,172 nonzero
pure-entry/minor residual products in 8 two-dimensional and 20
three-dimensional mixed kernels.  The remaining coupled chart

```text
direction=(-1,-1), q=3, finite:
t1=t2=0, s=-1-t0 r
```

closes by a direct selected-minor unit ideal using four minors and 32
pure-entry products.

The independent audit exhausts 3,976 projection points, 58,280 genuine
binary extensions, 747,552 direct selected-minor tests, and 144
projection-closure artifacts over `F_5,F_7`.

Therefore the finite family, genuine toric base boundary, nonzero
component-chart divisor, first-plane infinity, and internal `E=0`
divisor are all closed at complete marked-fibre level.  The complete
marked fibre of the known pure-compression component is excluded.
The existence and marked fibres of other pure-compression components,
and `H22`, remained unresolved at this checkpoint; the next entry
constructs a second component.

```text
P5_H31_INTERNAL_E0_MARKED_FIBRE_OBSTRUCTION.md
verify_p5_h31_internal_e0_marked_fibre.py
audit_p5_h31_internal_e0_marked_fibre.py
```

### A second pure-compression component via diagonal quadrics

The component-completeness question for the all-rank-two pure `P_4`
plane locus has a negative answer.  The useful reframe is the
squarefree Frobenius algebra

```text
C[X_0,X_1,X_2,X_3]/(X_0^2,X_1^2,X_2^2,X_3^2).
```

Its degree-two multiplication identifies a deficient plane-pair image
with a diagonal quadric through the two annihilator lines.  A
complementary support-two kernel pair has a rank-two double-contraction
form; choosing its radical as the fourth plane reduces the remaining
pure condition to one `(3,3)` equation

```text
Psi =
 A^3 F^3 + A^2 C F^2 H - A B^2 F H^2
 - A C^2 E^2 F + A C^2 F H^2 - B^2 C E^2 H = 0.
```

`Psi` is irreducible by a valuation argument after writing it as
`P-B^2 Q`.  Its diagonal-source orbit has tangent rank five.  At the
rational point `(A,B,C,E,F,H)=(1,1,0,2,1,1)`, the incidence Jacobian
has rank fourteen.  A sixth tangent direction is killed by the exact
quadratic cokernel value `-132`, so the tangent cone has dimension at
most five.  This proves that the family closure is a five-dimensional
irreducible component.

The diagonal-quadric dimensions of the four annihilator lines at that
point are `(1,1,1,2)`.  Three planes have dimension at least two
throughout the first component and its symmetry orbit, so the new
component is genuinely distinct.  This is a proof that an additional
component exists, not a complete component classification.

```text
P4_DIAGONAL_QUADRIC_PURE_COMPONENT.md
verify_p4_diagonal_quadric_pure_component.py
audit_p4_diagonal_quadric_pure_component.py
```

### Complete `H31` marked fibre at one point of the second component

At the rational point above, use the pure kernel marking

```text
alpha_0=(3,-2,0,-1), alpha_1=(1,0,0,-1),
alpha_2=(0,1,-1,0), alpha_3=(1,-1,-1,1).
```

Exact binary elimination over all four Borel shifts gives no survivor
for distinguished `q=1,2`, and exactly

```text
q=0: t=(0, 1,1,1),
q=3: t=(0,-1,1,1).
```

Both survivor mixed matrices have two-dimensional kernels.  Writing
an extension as `u k_0+v k_1`, the two binary diagonals are, up to the
orientation sign,

```text
2(u-2v), 2u.
```

Every genuine extension therefore has `u(u-2v)!=0`.  The same
mode-one marked minor in both orientations is

```text
-8u(u-2v)^2,
```

and the pure transverse column contains `2`.  Hence every extension is
ternarily excluded.  Independent audits enumerate 12,104 marking
points and all 20 genuine projective binary extensions over `F_5,F_7`.

At this checkpoint, one complete fibre only was closed.  The next entry
extends the obstruction to a rational curve; the generic and boundary
marked fibres of the second component, possible further components,
`H22`, and the prize problem remained unresolved.

```text
P5_H31_DIAGONAL_QUADRIC_COMPONENT_POINT_OBSTRUCTION.md
verify_p5_h31_diagonal_quadric_component_point.py
audit_p5_h31_diagonal_quadric_component_point.py
```

### A complete marked rational curve on the second component

Set `A=B=E=F=H=1, C=c` in the diagonal-quadric normal form.  The
component equation vanishes identically and the sole pure coefficient
is `4(c+1)`, so `c=-1` is precisely the zero-tensor point.

Over `Q(c)`, normalized binary projection leaves only

```text
q=0: t=(-2c/(c-1),1,1,1),
q=2: t=(-1,1,1,0).
```

To prevent a function-field Gröbner basis from hiding exceptional
algebraic values of `c`, a second elimination retains `c` over `Q` and
saturates by `c+1`.  Its `q=0,1,2` ideals are the displayed family,
the unit ideal, and the constant `q=2` marking.  Its `q=3` ideal is

```text
(t3-1,t2-1,t1-2c+1,t0+c,c^2-c).
```

Thus `c=0,1` are rigorously the only nonzero-pure jump fibres.

The first kernel has binary diagonals proportional to

```text
(c-1)(u-2v), (c+1)((c+1)u+2(c-1)v)
```

and its selected mode-one minor is their product with an additional
nonzero factor `u-2v`.  The second kernel has diagonals
`2(u-v),4v(c+1)` and marked minor
`64v(c+1)(u-v)^2`.

Exact specialization closes the only omitted nonzero-pure fibres.
At `c=0`, the survivor orientations are `q=0,2,3`; at `c=1`, they are
`q=2,3`.  Their marked minors are respectively scalar multiples of

```text
u(u-2v)^2, v(u-v)^2.
```

Thus both nonzero binary diagonals force an injective one-marked map in
every case, excluding every marking and every extension on the full
curve `c!=-1`.  The characteristic-zero verifier recomputes four
function-field projections, eight special-fibre projections, and all
seven displayed kernel cases.  The independent `F_5,F_7` audit checks
67,624 marking fibres, 158 projective kernel directions, and all 114
genuine binary extensions.

This is a relative one-dimensional theorem, not a generic result on
the five-dimensional component.  The component away from this curve,
its boundary, possible further components, `H22`, and the prize
problem remain unresolved.

```text
P5_H31_DIAGONAL_QUADRIC_CURVE_MARKED_FIBRE_OBSTRUCTION.md
verify_p5_h31_diagonal_quadric_curve_marked_fibre.py
audit_p5_h31_diagonal_quadric_curve_marked_fibre.py
```

### A transverse complete `E=e` curve

The previously isolated second-component point lies on another curve.
Set

```text
A=B=F=H=1, C=0, E=e.
```

The component equation vanishes identically, all four planes retain
rank two, and the sole pure coefficient is the constant `4`.  Retaining
`e` in exact binary projection gives:

```text
q=0:
 (t3-1,t2-1,t0-t1+1,e(t1-1),t1(t1-1));
q=1:
 (1);
q=2:
 (t3,t2-1,t1-e,2t0+1,e^2-1);
q=3:
 (t3-1,t2-1,t0+t1+1,e(t1+1),t1(t1+1)).
```

Thus `q=0,3` each have one uniform marking for every `e`; `e=0`
adds one marking in both orientations, and `e=+/-1` adds one `q=2`
marking.  There are no hidden exceptional complex fibres.

For the two uniform kernels, the diagonals are, up to sign,
`2(u-2v),2u`, and the mode-one marked minor is

```text
-8u(u-2v)^2.
```

For the `e=0` jumps they are `2(u-v),2(u+v)`, with mode-zero minor
`8(u-v)(u+v)^2`.  For `e=+/-1`, they are
`4(u-v),4v`, up to sign, with mode-zero minor
`64v(u-v)^2`.  Hence every genuine extension is ternarily excluded.

The characteristic-zero verifier closes all six kernel types.  The
independent `F_5,F_7` audit checks 79,728 marking fibres, 228
projective kernel directions, and all 164 genuine binary extensions.
The curve contains the old rational point at `e=2` and meets the
previous `C=c` curve at `e=1,c=0`.

The two curves still have codimension two in the three-dimensional
normal-form hypersurface.  Their complement and boundary, possible
further components, `H22`, and the prize problem remain unresolved.

```text
P5_H31_DIAGONAL_QUADRIC_E_CURVE_MARKED_FIBRE_OBSTRUCTION.md
verify_p5_h31_diagonal_quadric_e_curve_marked_fibre.py
audit_p5_h31_diagonal_quadric_e_curve_marked_fibre.py
```

### Pure-direction boundary and the complete factored slice

On `A=B=F=H=1,C=-1,E=e`, the pure coefficient matrix changes factor
direction: only its upper-right entry survives.  With the corresponding
kernel/pure marking, the sole nonzero coefficient is `4(e^2-1)`.
Saturating by `e^2-1`, exact relative projection gives unit ideals for
`q=0,1,3` and

```text
(t3,t2+1,t0-1,2e t1+e^2+1)
```

for `q=2`.  At `e=0` this is also a unit.  Otherwise the unique marking
has a rank-six mixed matrix with diagonals

```text
-4e(u-2v)/(e^2-1), 2u(e^2-1),
```

and mode-one marked minor

```text
-64e u(u-2v)^2.
```

Every genuine extension is excluded.  The independent `F_5,F_7`
audit checks 55,520 marking fibres, 44 projective kernel directions,
and all 32 genuine extensions.

The larger slice equation is

```text
Psi|_(A=B=F=H=1) = -C(C+1)(E-1)(E+1).
```

The `E=1`, `C=0`, and `C=-1` branches are the three closed curve
theorems.  Swapping source coordinates `X_0,X_3` sends `E=1` to
`E=-1`.  Their only uncovered intersections are the zero-tensor points
`C=-1,E=+/-1`.  Therefore the complete nonzero factored slice is
excluded at marked-fibre level, together with its full source/mode
symmetry orbit.  In particular, the source permutation `(0 1)(2 3)`
followed by the mode swap `1<->2` carries the `C=c` curve to
`A=B=C=E=F=1,H=h`; no new elimination is needed for that transverse
line.

This is still a lower-dimensional slice of the second component.  Its
complement and boundary, possible further components, `H22`, and the
prize problem remain unresolved.

```text
P5_H31_DIAGONAL_QUADRIC_PURE_DIRECTION_CURVE_MARKED_FIBRE_OBSTRUCTION.md
verify_p5_h31_diagonal_quadric_pure_direction_curve.py
audit_p5_h31_diagonal_quadric_pure_direction_curve.py
```

### Interior `H=0` rulings

On `A=B=F=1,H=0`, the component equation reduces to

```text
1-C^2E^2=-(CE-1)(CE+1).
```

Parametrize `CE=1` by `E=e,C=1/e` and rescale the `x_1` plane row by
`e`.  The sole pure coefficient is `4e`.  Saturated relative
projection gives

```text
q=0: (1);
q=1: (t3,t2-1,t1-e,e t0+1);
q=2: (t3,t2+1,t1-e,e t0+1);
q=3: (t3-1,t2-e,t1-e,2t0+e,e^2-1).
```

The `q=1,2` kernels survive uniformly.  Their diagonals are, up to
sign, `2e(u-2v),2eu`, while the same mode-two marked minor is
`-8u(u-2v)^2`.  At `e=+/-1`, the added `q=3` kernel has diagonals
`4(u-v),4v` or `4(u+v),4v` and mode-zero minor
`-64v(u-v)^2` or `-64v(u+v)^2`.

Thus every genuine extension is excluded.  Swapping `X_0,X_3` sends
`E` to `-E` and exchanges the two rulings, closing the complete
nonzero `H=0` slice and its source/mode orbit.  The independent
`F_5,F_7` audit checks 67,624 marking fibres, 172 projective kernel
directions, and all 124 genuine extensions.

Together with the factored `H=1` slice orbit, this initially gave two
exact lower-dimensional cross-sections of the second component.  The
next elliptic-surface theorem below excludes the generic fibre; the
proper survivor divisor and boundary, possible further components,
`H22`, and the prize problem remain unresolved.

```text
P5_H31_DIAGONAL_QUADRIC_H0_RULING_MARKED_FIBRE_OBSTRUCTION.md
verify_p5_h31_diagonal_quadric_h0_ruling.py
audit_p5_h31_diagonal_quadric_h0_ruling.py
```

### Elliptic-surface generic obstruction

The normalized diagonal-quadric equation has a much smaller invariant
form.  On `A=B=F=1`, set

```text
U=C+H, S=1+CH, T=H+CE^2.
```

Direct expansion gives `Psi=S^2-UT`.  On `U!=0`, put `r=S/U`,
`x=1-rH`, and `Y=rEx`.  The inverse map is

```text
H=(1-x)/r,
C=rx/(x+r^2-1),
E=Y/(rx),
```

and the component becomes

```text
Y^2=x[(1-r^2)x^2+(3r^2-2)x+(r^2-1)^2].
```

The cubic discriminant is

```text
r^4(r-1)^4(r+1)^4(4r^2-3).
```

After `X=(1-r^2)x,W=(1-r^2)Y`, the minimal Weierstrass model has

```text
Delta=16r^4(r-1)^6(r+1)^6(4r^2-3).
```

Its fibres are `I4` at zero, `I6` at each of `+/-1`, `I1` at each
root of `4r^2-3`, and `I0*` at infinity.  Their Euler numbers total 24,
so the minimal resolution is a K3 surface.  The reducible fibres have
root rank 17.  The section `P=(1,r^2)` is non-torsion: at `r=2`, the
integral model has `P=(-3,-12)`, and its reductions have orders `10`
modulo `5` and `3` modulo `7`.  Good-reduction injectivity on
prime-to-characteristic torsion makes finite order impossible.
The same specialized curve has `10,12,14` points over
`F_5,F_7,F_11`, leaving only the visible two-torsion section.
Shioda--Tate then forces Picard number 20 and Mordell--Weil group
`Z + Z/2`.

The previously closed `H=0` rulings are exactly the sections
`(x,Y)=(1,+/-r^2)`.  The `H=1` factored slice maps to the singular
fibre `r=1` or the base locus `U=S=0`; the source-symmetric image lies
over `r=-1`.

For the generic marked plane tuple, retain `Y,t0,...,t3`, work over
`Q(r,x)`, and impose the elliptic relation.  For each distinguished
coordinate, normalize one binary diagonal and invert the other in the
`14 x 8` mixed system.  Exact block elimination gives

```text
q=0: (1)
q=1: (1)
q=2: (1)
q=3: (1).
```

Thus the generic marked fibre of the second component admits no
binary extension at all.  Every remaining survivor is supported on a
proper closed subset.  This does not classify that divisor: a bounded
attempt retaining a fibre coordinate exceeded the strict runtime
guard and was stopped rather than expanded into another ambient
search.  The next geometric task is to classify survivor sections and
multisections and compactify the elliptic boundary.

```text
P5_H31_DIAGONAL_QUADRIC_ELLIPTIC_GENERIC_OBSTRUCTION.md
verify_p5_h31_diagonal_quadric_elliptic_generic.py
audit_p5_h31_diagonal_quadric_elliptic_generic.py
```

### Universal mixed kernel and the first survivor-support chart

The generic unit ideal says only that the survivor projection is
proper.  A smaller determinantal calculation now locates its support
on a dense chart for the middle distinguished coordinates.

For `q=1,2`, the `14 x 8` mixed matrix has an explicit universal
kernel line for every marking.  Its first binary diagonal vanishes, so
a genuine extension requires a second kernel direction.  Deleting the
unit `a2` component gives a `14 x 7` quotient.  The same `6 x 6` pivot
works in both cases:

```text
-64 r^2 t0 x^2 (t3-1)(r^2x-t2)(x+r^2-1) Q^2,
Q=-f/x=-Y^2/x.
```

Bordering this pivot first forces `t3=0`, then splits into two branches.
Compatibility of only three further borders gives

```text
q=1: (x-1)(x-1-r)^2=0,
q=2: (x-1)(x-1+r)^2=0
```

on the main branch.  Away from the already-closed pure-direction
curves, this forces `x=1`, followed by

```text
t0=-1/r^2, t1=Y, t2=+r (q=1) or -r (q=2), t3=0.
```

These are exactly the previously closed `H=0` survivor markings.  The
second branch is compatible only at `r=-1` or `r=1` (or `r=0`), again
outside the pivot chart and on already-known geometric strata.  Thus
this dense chart contains no new survivor curve.

The exact primary verifier uses direct permutation permanents; an
independent verifier rebuilds the systems with a subset-DP permanent.
At this checkpoint the pivot complement and `q=0,3` remained open, so
the displayed result was a support theorem rather than a complete
second-component obstruction.  The later endpoint and pivot-complement
sections close those regular strata.

```text
P5_H31_ELLIPTIC_MIDDLE_COORDINATE_RANK_DROP.md
verify_p5_h31_elliptic_middle_coordinate_rank_drop.py
audit_p5_h31_elliptic_middle_coordinate_rank_drop.py
```

### End-coordinate kernels and a full-rank quotient chart

Canonical reduction in `Q(r,x)[Y]/(Y^2-f)` turns the initially large
`q=0,3` null vectors into

```text
q=0: (Y+r^2x,1,0,r, 1,D,Y+x-x^2,0),
q=3: (Y-r^2x,1,0,-r, -1,-D,Y-x+x^2,0).
```

Marking again acts only by `b_i -> b_i+t_i a_i`.  Both universal lines
kill the first binary diagonal.  After deleting the unit `a1` column,
a small `6 x 6` pivot and its row-11 border have respective factors

```text
(r^2x-/+Y)(x-t2)(t3-1)(x-1)
```

and the same product times `D`.  The elliptic identity

```text
(r^2x-Y)(r^2x+Y)=x(r^2-1)(x-1)D
```

shows that the signed `Y` factors are units away from the standard
geometric boundary.  Hence the quotient has rank seven, its kernel is
only the universal line, and there is no binary survivor on this dense
end-coordinate chart.

The remaining end-coordinate marking strata are now the explicit
divisors `t2=x` and `t3=1`, plus the already visible geometric factors.
The result was independently rebuilt with a subset-DP permanent.

```text
P5_H31_ELLIPTIC_END_COORDINATE_FULL_RANK_CHART.md
verify_p5_h31_elliptic_end_coordinate_full_rank_chart.py
audit_p5_h31_elliptic_end_coordinate_full_rank_chart.py
```

### The apparent endpoint exceptions are closed genus-two trisections

On the deepest end-coordinate intersection

```text
q=0 or 3, t2=x, t3=1,
```

put `epsilon=+1` for `q=0` and `epsilon=-1` for `q=3`.  Two quotient
minors linear in `t1` have compatibility divisor

```text
-epsilon(r^2-1)(Y-epsilon(x^2-x))J_epsilon,
J_epsilon=Y(x+r^2-1)-epsilon r^2x(x-r^2-1).
```

The first two factors are units on the regular non-pure chart.  Solving
`J_epsilon=0` and imposing the elliptic equation leaves conjugate
residual trisections.  Their common elementary normalization is

```text
u=r^2=(s^3+3s^2+3s+5)/(s^3+3s^2-s+1),
x=(s+1)^4/(s^3+3s^2-s+1),
v=r(s^3+3s^2-s+1),
v^2=(s^3+3s^2+3s+5)(s^3+3s^2-s+1).
```

The sextic has discriminant `2^24 3^3 11`, so this is a smooth
genus-two curve.  The remaining minors force unique `t1,t0` in each
endpoint orientation; `t1` changes sign and `t0` does not.  At those
candidates, two full quotient determinants share only chart units and
have residual factors

```text
s^3+2s^2-3s+2,
s^2+1.
```

Their gcd is one.  The quotients therefore have full rank everywhere
on the two regular genus-two charts, and each universal mixed-kernel
line kills the first binary diagonal.  Both apparent exception curves
are empty.  This closes only the deepest endpoint intersections, not
the full marking divisors.

```text
P5_H31_ELLIPTIC_END_GENUS_TWO_EXCEPTION_OBSTRUCTION.md
verify_p5_h31_elliptic_end_genus_two_exception.py
audit_p5_h31_elliptic_end_genus_two_exception.py
```

### The complete endpoint t2=x divisor is empty

A smaller quotient minor closes the entire regular `t2=x` divisor for
both `q=0,3`.  Put `epsilon=+1` for `q=0` and `epsilon=-1` for `q=3`.
The minor factors as

```text
128 r^5 x^6(r^2-1)(x-1)(t3-1)L_epsilon.
```

The quadratic-field norm of `L_epsilon` is, up to the standard chart
units, exactly the residual polynomial `R` of the genus-two
trisection.  Thus rank drop away from `t3=1` is forced back onto the
same curve

```text
v^2=(s^3+3s^2+3s+5)(s^3+3s^2-s+1).
```

On this normalization, successive minors force

```text
t1=epsilon (s-1)^2(s+1)(s+3)n/d^2,
t0=((s-1)t3-2s)d^2/[2s(s+1)^4n].
```

Two complementary determinants then have residual factors

```text
L1=s^4+3s^3-s^2+s+2(1-s)t3,
t3 L2=t3[s^3+s^2+3s-1+2(1-s)t3].
```

Their resultant is

```text
-2s(s-1)^2(s+1)(s^2+2s-1)d.
```

The only regular finite exception is `s^2+2s-1=0`, where `t3=-s`.
A third quotient minor reduces there to

```text
-2^34 v(12s+29),
```

which is nonzero because the two residual polynomials are coprime.
Hence the quotient has full rank everywhere on the regular divisor;
the universal line kills the first binary diagonal.

```text
P5_H31_ELLIPTIC_END_T2_DIVISOR_OBSTRUCTION.md
verify_p5_h31_elliptic_end_t2_divisor.py
audit_p5_h31_elliptic_end_t2_divisor.py
```

### The complete endpoint t3=1 divisor is empty

The last regular end-coordinate marking divisor also admits a
low-degree function-field description.  On `t3=1`, eliminating `t1`
from two quotient minors gives a quadratic in `t2`.  With
`Z=epsilon Y`, it splits over the elliptic function field as

```text
t2-=-x(-Z+r^2x-r^2-x+1)/(x+r^2-1),
t2+=r^2x(2Z+r^2x+r^2+x-1)/[(r^2-1)(x-1)^2].
```

This is the key geometric simplification: the apparent cover is not a
new high-genus object.  On the minus branch, direct substitution in two
further quotient minors has essential norm gcd `R`; on the plus branch,
using `t1`-resultants so that pivot-degenerate fibres are retained gives
essential norm gcd `R^2`.  Here `R=0` is precisely the already known
genus-two trisection.

On its normalization

```text
r=v/d, x=(s+1)^4/d,
Y=epsilon sigma (s-1)(s+1)^3n/d^2, v^2=nd,
```

the four sheet/branch combinations reduce to the square-free residual
gcds

```text
sigma=+1:  s^2+2s-1 (minus),  1 (plus);
sigma=-1:  s(s-1)(s^2+1) (both).
```

The `s=0` point is the closed `x=1` ruling.  At all remaining values
`s=-1+/-sqrt(2),1,+/-i`, and for both signs of `v`, the exact rank
triples

```text
(rank M, rank[M;d_alpha], rank[M;d_beta])
```

are respectively `(6,7,6)`, `(7,7,8)`, and `(6,7,6)`.  Thus the two
diagonal conditions retain only the universal line and no genuine
binary extension.  The same identities hold for `q=0,3`, with the
expected sign change in `t1`.

Therefore both regular endpoint marking divisors are now completely
closed.  At this intermediate checkpoint, the remaining regular
elliptic-chart work was the middle-coordinate pivot complement; the
next section closes it.

```text
P5_H31_ELLIPTIC_END_T3_DIVISOR_OBSTRUCTION.md
verify_p5_h31_elliptic_end_t3_divisor.py
audit_p5_h31_elliptic_end_t3_divisor.py
```

### The complete regular middle-coordinate pivot complement is empty

The middle-coordinate pivot exceptions can also be closed without a
large elimination.  For `q=1,2`, put `sigma=-1,+1` and define

```text
F=(x-1)(r^3-r+sigma)+sigma r^2(x+1),
L=Y r^2D+t1Q,
G=t3F+(r-sigma)D,

A=2sigma r^2x+rt2+rx^2-rx
  -sigma t2+sigma x^2-sigma x.
```

Four quotient determinants have residual factors

```text
t3FL,  t3LG,  AB,  FH.
```

Here `B|L=0` is a chart unit times `G`,
`H|t0=0=(t3-1)(t2-r^2x)`, and both
`A|t2=r^2x` and `G|t3=1` are chart units.  These identities give a
short Fitting-ideal cover of the three old pivot divisors
`t0=0,t3=1,t2=r^2x`.

The only auxiliary base factor is `F=0`.  It is linear in `x`; with

```text
a=r^3+sigma r^2-r+sigma,
b=r^3+3sigma r^2+3r+3sigma,
```

its pullback is

```text
x=(r+sigma)(r-sigma)^2/a,
Y^2=r^4(r+sigma)^2(r-sigma)^4 b/a^3.
```

Five terminal determinants reduce on this curve to units or one of
`t0,t3-1,C(t2)`, followed by a unit when `C=0`.  Thus this
genus-two-looking intermediate cover is not a survivor curve.

The temporary assumption `Y!=0` is removable.  On the regular
two-torsion bisection `Y=0,x!=0`, one adapted quotient determinant is a
chart unit times `t3`; at `t3=0`, a second determinant is itself a
chart unit and is independent of the remaining marking.

The primary verifier and an independent subset-DP permanent audit both
reproduce the complete case tree for `q=1,2`.  Combined with the
endpoint theorems, every marked fibre in the regular elliptic chart is
now excluded for all four distinguished coordinates.  The remaining
second-component problem is its birational/compactification boundary.

```text
P5_H31_ELLIPTIC_MIDDLE_COORDINATE_PIVOT_COMPLEMENT.md
verify_p5_h31_elliptic_middle_coordinate_pivot_complement.py
audit_p5_h31_elliptic_middle_coordinate_pivot_complement.py
```

### The complete elliptic-normalization boundary is empty

The inverse-map boundary of the normalized slice `A=B=F=1` has a
simple original-coordinate description.  With

```text
U=C+H, S=1+CH, T=H+CE^2, Psi=S^2-UT,
```

one has

```text
r=S/U,
x=C(1-H^2)/U,
D=S(1-H^2)/U^2.
```

The factors `H=+/-1` and `U=S=0` are the already closed factorized and
pure-direction loci.  The only residual finite boundary is `S=T=0`,
which is the pair of rational curves

```text
C=-1/h, H=h, E=delta h, delta=+/-1.
```

Two scaled row charts cover each projective curve.  Their pure
coefficients are `4(h^2-1)` and `4(1-z^2)`, where `z=1/h`.  Saturated
relative projection gives the unit ideal in three distinguished
orientations.  In the exceptional orientation, the unique marking is

```text
t0=-1, t1=delta, t2=(z^2+1)/2, t3=0.
```

For `z!=0`, the mixed rank is six.  Its two binary diagonal factors are

```text
delta(u-2v)/z,
-(z^2-1)[uz^2-u+6vz^2+2v]/(2z^2).
```

A mode-one marked determinant is

```text
(u-2v)^2(z^2-1)[uz^2-u+6vz^2+2v]/(2z^3),
```

so every genuine binary extension is injective on the marked
hyperplane.  At `z=0`, the mixed kernel has dimension four but the first
diagonal vanishes on all of it, so no binary extension exists.  The
finite endpoint `h=0` is excluded directly by the relative projection.

The independent subset-DP audit reproduces all sixteen projections and
the boundary identities.  Hence the complete nonzero-pure marked fibre
on the normalized affine slice `A=B=F=1` is empty.  At that checkpoint,
the next boundary was the outer projective/gauge locus `A B F=0`.

```text
P5_H31_DIAGONAL_QUADRIC_NORMALIZATION_BOUNDARY_OBSTRUCTION.md
verify_p5_h31_diagonal_quadric_normalization_boundary.py
audit_p5_h31_diagonal_quadric_normalization_boundary.py
```

### The complete outer boundary of the second component is empty

The remaining projective/gauge boundary is geometric rather than a
large chart search.  The all-rank conditions are

```text
(A,B)!=(0,0), (E,F)!=(0,0),
```

and on the three normalization coordinate hyperplanes one has

```text
Psi|A=0 = Psi|F=0 = -B^2 C E^2 H,
Psi|B=0 = A F K,

K=A^2F^2+ACFH-C^2E^2+C^2H^2.
```

Projective row scalings and the diagonal source torus

```text
diag(a,b,b,a):
(A,B,C;E,F,H) -> (aA,bB,bC;aE,bF,aH)
```

reduce every coordinate surface to a curve.  The source permutation
`(0,1,2,3)->(1,0,3,2)` with the mode swap `1<->2` pairs

```text
AC <-> FH, AE <-> FB, AH <-> FC,
```

and pairs the two residual toric edges.  Four representative curves
therefore suffice:

```text
AC:   (0,1,0;p,1,1),
AE:   (0,1,p;0,1,1),
AH:   (0,1,p;1,1,0),
edge: (0,1,p;1,0,0).
```

Exact relative binary projection gives respectively:

```text
AC:
 q1=(t1,t0,t3(t2-1)), q2=(t1,t0,t3(t2+1));

AE:
 q0=q3=(t1,t3,
   t0(pt2-1),
   t0t2^2-t0p^2-t2p^2+t2,
   t2p^3-t2p-p^2+1,
   t0p^3-t0t2+p^2-1);

AH:
 all four unit;

edge:
 q0=q3=(t2,t0,t1t3).
```

All omitted orientations are unit ideals.  On `AC`, the two
projection components reduce to marked minors proportional to the two
binary diagonals; the pivot divisor `p^2s+1=0` has an alternate kernel
basis with terminal minors

```text
16u(u+/-p^2v)^2.
```

On `AE`, the generic marking is

```text
t2=1/p, t0=-p/(p^2+1),
```

and the only special fibres are `p=+/-1`, where the survivor is
`t0=0` or `t2=p`.  Their complete one-parameter kernels have marked
minors equal to a unit times the two diagonal factors.

The edge has two marking lines.  Away from their intersection, its
minors are

```text
32ps^2v^2(u-v), 16u(su-/+v)^2.
```

At the intersection, the ordinary minor

```text
16pv(u-v)(u+v)
```

misses only `u+v=0`.  Stacking the pure and neighbouring one-marked
maps on that direction gives the exact `5 x 5` determinant

```text
128p.
```

The noncoordinate `B=0` surface becomes the rational conic

```text
E^2=H^2+H+1
```

after `A=C=F=1`.  Its homogeneous parametrization is

```text
H=u(u-2v), E=-(v^2-uv+u^2), F=v^2-u^2.
```

On the affine chart, relative projection leaves four markings over
`v/u=1/2`; the point at infinity leaves four more.  Their diagonal
pairs are

```text
(4u+3v,4u-3v), (2u+3v,u),
(u-v,u+v), (u-2v,u),
```

and selected one-marked minors contain exactly these factors.  The two
`F=0` conic endpoints lie on the already covered `FB` curve.

The characteristic-zero primary verifier checks 20 relative
projections, 32 kernel/minor cases, and both stacked exceptions.  The
independent `F_5/F_7` audit enumerates 362,328 markings on only these
one-parameter bundles.  It finds exactly 568 survivor markings and
tests every one of 3,032 genuine projective binary extensions; 3,012
have an injective neighbouring marked map, and the remaining 20 have
an injective stacked map.

Thus the entire projective parameter boundary `A B F=0` is excluded.
Combined with the normalized affine theorem, the complete marked fibre
of the second known pure-compression component is empty.  The honest
remainder is possible further pure-`P_4` components and `H22`.

```text
P5_H31_DIAGONAL_QUADRIC_OUTER_BOUNDARY_OBSTRUCTION.md
verify_p5_h31_diagonal_quadric_outer_boundary.py
audit_p5_h31_diagonal_quadric_outer_boundary.py
```

### Three more pure components from the cubic diagonal-quadric map

The diagonal-quadric reframe is more productive than the former chart
search.  For a line with Pluecker coordinates `p_ij`, the unique
generic diagonal quadric through it is the cubic Cremona-type map

```text
d_i=(-1)^i product_{j<k, j,k != i} p_jk.
```

Its base locus is the block-line locus `dim D(ell)>=2`, with two
permutation-invariant types: `2+2`, where `D(ell)` is in no coordinate
hyperplane, and `1+3`, where it is contained in one `d_i=0`.

On the `1+3` radical plane use

```text
y1=(0,1,-1,0), y2=(0,1,0,-1),
z1=(0,1,1,0),  z2=(0,1,0,1).
```

Double contraction by `y1,y2` has rank two and radical
`span(z1,z2)`.  With

```text
P=G-T, Q=D-S,
u0=(2,P+Q,Q-P,0), u1=(0,0,1,1),
x1=(1,0,S,D), x2=(1,0,G,T),
```

take

```text
U0=<u0,u1>, U1=<y1,x1>, U2=<x2,y2>, U3=<z1,z2>.
```

Only `0100,0101,1100,1101` can be nonzero.  Their `2 x 2`
determinant factors exactly as

```text
(D-G-S+T)(D+G-S-T)(D+G+S+T).
```

The three linear branches `L1,L2,L3` each have a rank-five family
tangent.  At rational samples, their `15 x 20` Segre-incidence
Jacobians have rank fifteen with determinants

```text
163840, 6193152, -737280.
```

Their generic diagonal-quadric jump signatures are

```text
L1=(1,1), L2=(0,2), L3=(0,1),
```

while the first two known components have `(2,1)` and `(1,0)`.
Hence the three branches are mutually symmetry-inequivalent and
inequivalent to the earlier components.  There are at least five
component orbits, but no exhaustiveness claim.

The characteristic-zero primary verifier and an independent modular
DP-permanent/dual-number audit at `101,103` are green.

```text
P4_DIAGONAL_QUADRIC_ONE_THREE_COMPONENTS.md
verify_p4_diagonal_quadric_one_three_components.py
audit_p4_diagonal_quadric_one_three_components.py
```

### Generic marked `H31` fibres on the three new components

Adaptive marked bases turn the branch tensors into a single `BBBB`
coefficient.  Exact projection over `C(S,D,G)` gives:

```text
L1:
 q0,q1 unit;
 q2 one marking;
 q3 one marking.

L2:
 q0,q1 unit;
 q2 one marking pencil;
 q3 one marking pencil.

L3:
 q0,q1,q2,q3 unit.
```

On every `L1` survivor, a selected mode-zero minor obeys

```text
det=A^2 B/[8DG(G+S)].
```

On both complete `L2` marking pencils, including the two values where
the generic kernel basis changes,

```text
det=A^2 B/[8D(D+G)(D+G-S)].
```

Here `A,B` are exactly the two required nonzero diagonal coefficients
of the neighbouring binary `Delta_2` slice.  The pure one-marked
transverse entry is the constant `-1` for `q=2` and `+1` for `q=3`.
Thus every generic binary extension is ternarily obstructed, while
`L3` has no binary extension at all.

The independent `F5/F7` audit exhausts 36,312 marked bases and all 144
genuine projective extension directions; every direction has an
injective neighbouring marked map and a transverse pure entry.

```text
P5_H31_ONE_THREE_COMPONENT_GENERIC_OBSTRUCTION.md
verify_p5_h31_one_three_component_generic_obstruction.py
audit_p5_h31_one_three_component_generic_obstruction.py
```

This is a generic theorem only.  A small `F5` reconnaissance over all
nonzero-pure affine parameter points found no escape on any branch,
but that census is discovery guidance, not proof.  Relative
characteristic-zero projection has already resolved the formerly
generic-unit `L1,q=0` boundary into two rational sheets:

```text
t3=0:
 S=-D, t1=-D, t2=-2D, t0=-1/(G-D);

t3=-1:
 S=D-2G, t1=-2G, t2=-G, t0=-1/(D-G).
```

On the first sheet the genuine binary conditions are
`u(u-v)!=0` and a mode-zero minor is
`-8D u^2(D-G)(u-v)`; on the second they are
`v(u-v)!=0` and a mode-zero minor is
`8G v^2(D-G)(u-v)`.  These are promising first charts for a complete
affine-boundary theorem.  The alternative pure-factor charts
`DG=0`, analogous `L2/L3` divisors, and projective torus boundary are
still pending.

### Common smooth diagonal-quadric spinor obstruction

Normalize a smooth diagonal quadric to

```text
X0^2+X1^2+X2^2+X3^2=0
```

and parametrize its two rulings by spinor coordinates `L(s),R(s)`.
For either ruling, the cubic diagonal-quadric map on the annihilator
line is

```text
2s(s^4-1)(1,1,1,1).
```

The missing point `s=infinity` is also a block line.  Up to ruling
swap and mode permutation the only four-line patterns are `LLLL`,
`LLLR`, and `LLRR`.

For each pattern, form all single-mode flattening minors of the
restricted `2^4` permanent tensor and saturate by the ideal of its
entries.  Fresh characteristic-zero Singular gives

```text
J_LLLL=(1),
dim J_LLLR=1,
dim J_LLRR=1.
```

After setting

```text
B=product_i s_i(s_i^4-1),
```

both mixed ideals satisfy `J:B^infinity=(1)`.  Thus every nonzero pure
common-smooth-quadric solution contains a block annihilator line, and
the mixed solution closures have total dimension at most four after
restoring the three-dimensional diagonal source torus.  The apparent
sixth-component lead is therefore a boundary phenomenon, not a new
component.

An independent DP-permanent audit over `F13,F17` checks the line/plane
duality and cubic map and exhausts 74,496 non-block parameter tuples
across the three patterns, finding zero nonzero-pure tuples.  It also
replays rational pure boundary samples for `LLLR` and `LLRR`.

```text
P4_COMMON_SMOOTH_DIAGONAL_QUADRIC_OBSTRUCTION.md
verify_p4_common_smooth_diagonal_quadric_obstruction.py
audit_p4_common_smooth_diagonal_quadric_obstruction.py
```

This closes only the semisimple common-smooth-quadric locus.  The
remaining component-classification problem is concentrated on the
star/triangle exceptional-pair graphs at `2+2` and `1+3` block-line
centers.

### Directed radical-star component classification

For a nonzero pure restriction, the perfect pairing on the
six-dimensional squarefree degree-two space gives

```text
r_ij+r_kl <= 7
```

for every opposite pair.  If all pair-image ranks are at least three,
one may choose an exceptional edge from each perfect matching; the
three chosen edges form a star or triangle.

In pure-factor bases `(kernel,active)`, the unique relation on a
rank-three pair has zero active-active coefficient.  If its `2 x 2`
coefficient matrix has rank one, the relation factors through a pure
kernel endpoint.  The resulting product `uv=0` in the squarefree
complete intersection forces `u,v` into one source-coordinate pair.

When two rank-one exceptional relations point away from a common mode,
their two independent common-mode vectors have either disjoint
supports or one-coordinate overlap.  These are exactly the `2+2` and
`1+3` block planes, and the common plane is automatically the radical
of the double contraction by the two outer kernel rows.

The dense complement-row gauges are exhaustive.  In the disjoint
case they recover the `(A:B:C),(E:F:H)` normal form and the irreducible
determinant `Psi`.  In the overlap case they recover the
`(S,D,G,T)` normal form and the split determinant

```text
(D-G-S+T)(D+G-S-T)(D+G+S+T).
```

Thus the directed radical-star stratum contains exactly four already
certified component closures: the second `2+2` component and
`L1,L2,L3`.  No additional component occurs generically there.

```text
P4_RADICAL_STAR_COMPONENT_CLASSIFICATION.md
verify_p4_radical_star_component_classification.py
audit_p4_radical_star_component_classification.py
```

The remaining component alternatives have mixed kernel-edge
orientations (including the known triangle component), predominantly
rank-two exceptional relations, pair-image rank at most two, or
coincident/support-one zero-product boundaries.

### Sixth pure component from the mixed zero-product orientation

Normalize the mixed pair relations to

```text
x1=(0,0,1,1),       y1=(a,1,c,d),
x2=(p,1,0,q),       y2=(-1,0,1,0),
x3=(1,0,1,0),       y3=(0,0,-1,1),
```

with `x1*y3=y2*x3=0` in the squarefree degree-two algebra.  Of the
seven kernel-containing contractions to mode zero, only three are
nonzero.  The exact rank-at-most-two determinantal ideal of their
`3 x 4` matrix has five linear minimal primes:

```text
(c+p+q,a+d),
(d+q,a+c+p),
(c,a+d+p+q),
(c-d+p-q,a),
(c-d,a+p-q).
```

On the first prime, set `N=q(d+p+q)` and take

```text
U0=span((-dp,d+q,N,0),(dp,-d-q,0,N)),
U1=span((0,0,1,1),(-d,1,-p-q,d)),
U2=span((p,1,0,q),(-1,0,1,0)),
U3=span((1,0,1,0),(0,0,-1,1)).
```

Every restricted coefficient vanishes except

```text
T0000=2q(d+p+q).
```

At `(d,p,q)=(1,2,3)`, the diagonal-source family tangent has rank five
with minor `-9/2`.  In pivots `(02),(02),(01),(02)`, the standard
Segre-incidence Jacobian has rank fifteen; the selected minor is
`-737280`.  Hence the irreducible family closure is a generically
smooth five-dimensional component.

Its pair profile is `(4,4,3,4,3,3)` and its jump signature is `(0,1)`,
the same coarse values as `L3`.  The finer directed relation invariant
separates them.  All three exceptional relations have rank one; the
new sorted pure-kernel endpoint indegrees are

```text
(2,1,0,0),
```

whereas `L1,L2,L3` have `(1,1,1,0)`, and the first two components have
only two rank-one exceptional edges.  This raises the certified lower
bound to six symmetry-inequivalent pure-component orbits.

The third linear prime above is a mode-`(0,1)` symmetry translate of
the first under

```text
d'=-q(d+p+q)/(d+q).
```

```text
P4_MIXED_ORIENTATION_PURE_COMPONENT.md
verify_p4_mixed_orientation_pure_component.py
audit_p4_mixed_orientation_pure_component.py
```

The sixth component's generic and boundary marked `H31` fibres were
open at this checkpoint.

### Generic marked `H31` fibre on the sixth component

Use the second row of each component plane as the pure kernel row and
the first row as the active row.  The only coefficient is then

```text
T_BBBB=2q(d+p+q).
```

Exact projection over `C(d,p,q)` makes the distinguished-coordinate
`0,1` ideals unit.  Coordinates two and three each leave two rational
marking sheets.  On the four sheets, selected all-extension minors
satisfy

```text
sheet  mode  rows  det/(A B^2)
2A       1   0237  -p^2 q/(d+p+q)
2B       2   0137   d(d+q)/q
3A       3   0267  -(d+q)
3B       3   0267  -(d+q).
```

The corresponding pure one-marked maps also have nonzero transverse
entries `d+q`, `d(d+p+q)`, `d+q`, and `d+q`.  Hence the complete marked
fibre at the generic point is empty.

The independent `F7/F11` audit exhausts 68,168 marked bases, finds
exactly four surviving markings in each field, and checks all 64
genuine projective extension directions.

```text
P5_H31_MIXED_ORIENTATION_COMPONENT_GENERIC_OBSTRUCTION.md
verify_p5_h31_mixed_orientation_component_generic_obstruction.py
audit_p5_h31_mixed_orientation_component_generic_obstruction.py
```

Only special parameter divisors and projective boundary points remain.

### A six-dimensional lower-pair-rank component

The determinantal prime

```text
d+q=0,        a+c+p=0
```

first appeared to be a singular five-dimensional branch at the sample
`(a,c,d)=(1,2,3)`.  That sample is accidentally on `d=a+c`; its entire
quadratic tangent obstruction vanishes.  Moving to `d=4` exposed the
correct geometry.

Put `h=a+c-d` and take

```text
U0=span((1,0,0,-1),(0,0,1,1)),
U1=span((1,b,0,1-bh),(0,e,1,1-eh)),
U2=span((1,0,-1,0),(0,1,-a-c,-d)),
U3=span((1,0,0,1),(0,0,1,-1)).
```

The only nonzero restricted coefficients are

```text
T1010=2(1-b(a+c)),
T1110=2(1-e(a+c)).
```

At `(a,c,d,b,e)=(1,2,4,1,2)`, with unit source-torus parameters, the
family-incidence map has rank six; the minor on rows
`(1,3,4,5,6,10)` and columns `(a,d,b,e,t0,t2)` is `1`.
The `15 x 20` Segre-incidence Jacobian has rank fourteen, with selected
minor `-215040`.  Thus the rational family closure is a generically
smooth six-dimensional component.

Its pair profile and directed signature are

```text
(4,3,2,4,4,3),
(2 rank-one edges, 0 rank-two-relation edges, (2,0,0,0)).
```

Its jump signature is `(0,2)`.  Dimension alone separates it from all
six previously certified five-dimensional components.  The old
determinantal prime embeds as the subfamily `b=1/a,e=0`, so it was not
an eighth component.

The characteristic-zero primary verifier and independent modular
dual-number audits over `F101,F103` are green.

```text
P4_SIX_DIMENSIONAL_PURE_COMPONENT.md
verify_p4_six_dimensional_pure_component.py
audit_p4_six_dimensional_pure_component.py
```

This raises the certified lower bound to seven component orbits, not
an exhaustive classification.

### Generic marked `H31` fibre on the six-dimensional component

The normal form depends on `a,c` only through `s=a+c`.  Set

```text
u=1-sb,       v=1-se.
```

After a common row scaling in `U1`, the pure kernel/active basis has

```text
alpha1=(sv,v-u,-su,d(v-u)),
beta1 =(s,1-u,0,d+u(s-d)),
```

and the only restricted coefficient is `T_BBBB=2su`.

Exact projection over `C(s,d,u,v)` makes the distinguished-coordinate
one ideal unit.  Its ubiquitous kernel direction simply restores the
deleted source coordinate and has diagonals `(0,2su)`, so it
reconstructs the pure tensor rather than a binary neighbour.

Put

```text
tau=(1-u)/(u-v),       sigma=sv/(u-v).
```

The other three coordinates have exactly the markings

```text
q0=(1,tau,sigma,0),
q2=(0,tau,sigma,1),
q3=(0,tau,sigma,0).
```

For these sheets, the ideals generated by the fourteen mixed
equations, an inverse of the two binary diagonals, and three
mode-zero minors are all unit.  The row triples are

```text
q0: 0127,0137,0147
q2: 0267,0367,0467
q3: 0127,0137,0147.
```

An independent audit over generic `F5,F7` samples exhausts 12,104
marked bases, finds precisely these three markings in each field,
checks 3,026 reconstruction-kernel instances, and excludes all 186
genuine projective extension directions.

```text
P5_H31_SIX_DIMENSIONAL_COMPONENT_GENERIC_OBSTRUCTION.md
verify_p5_h31_six_dimensional_component_generic_obstruction.py
audit_p5_h31_six_dimensional_component_generic_obstruction.py
```

All seven certified component orbits therefore have empty generic
marked `H31` fibre.  The new component's special parameter/projective
boundary, the other incomplete component boundaries, component
exhaustiveness, and `H22` remain open.

### Closure of the five mixed determinantal primes

The five linear primes in the mixed `3 x 4` determinantal normal form
are now identified without another component search:

```text
P1=(c+p+q,a+d)       -> sixth component,
P2=(d+q,a+c+p)       -> six-dimensional component subfamily,
P3=(c,a+d+p+q)       -> sixth component by mode swap,
P4=(c-d+p-q,a)       -> L2,
P5=(c-d,a+p-q)       -> L1.
```

For `P4`, swap source coordinates zero and one and reorder the
split-cubic modes as `(B2,B0,B1,B3)`.  The exact `L2` parameters are

```text
S=p, D=q, G=q(p-q-d)/(d+q),
T=D+G-S=-dp/(d+q).
```

For `P5`, the same symmetries use

```text
S=p, D=q, G=-dp/(d+q),
T=-D+G+S=-q(d-p+q)/(d+q).
```

All four plane Pluecker vectors agree identically in each case.  The
primary characteristic-zero verifier and independent modular
`F101/F103` audit are green.

```text
P4_MIXED_DETERMINANTAL_PRIME_CLASSIFICATION.md
verify_p4_mixed_determinantal_prime_classification.py
audit_p4_mixed_determinantal_prime_classification.py
```

Thus the dense mixed determinantal chart contains no eighth component.
Other mixed-orientation normal forms, rank-two exceptional relations,
and degenerate lower-rank boundaries remain part of the global
component-classification problem.

### Equal-weight `H22` component obstruction and slope correction

The normalized `H22` contractions do not meet the pure `P4` slice
along coordinate hyperplanes.  Their source bases are instead

```text
D01(r)=(r0+r1,r2,r3,r4),
D23(r)=(r0,r1,r2+r3,r4).
```

This diagonal-hyperplane reformulation was applied to the
six-dimensional apolar component over `C(s,d,u,v)`.  For an arbitrary
pure marking `beta_i+t_i alpha_i` and arbitrary fifth-coordinate
extensions `(x0,...,x3,y0,...,y3)`, each neighboring binary tensor has
fourteen mixed coefficients linear in the extensions.  Normalizing
one desired diagonal and saturating by the other projects to `(1)` for
both `D01` and `D23`.  Hence neither equal-weight pencil admits a
nonzero binary `Delta2` extension on this normal-form chart.

The `D23` unit ideal hides a short identity.  If `A` is the coefficient
row of the desired `0000` diagonal, then

```text
M1000=(t0-1)A,
(u-v)M1110=-G A,
G at t0=1 equals -s u.
```

Vanishing of `M1000` with `A z!=0` forces `t0=1`, after which
`M1110 z=su/(u-v) A z` is nonzero.  Thus the third target row is never
reached in this direction.

The characteristic-zero verifier and independent `F5,F7` audit are
green.  The audit tests all `625+2401=3026` marked bases for each
diagonal.  It finds no viable extension; for `D23`, it also replays the
two-row identity at every marking.

```text
P5_H22_SIX_DIMENSIONAL_EQUAL_WEIGHT_BINARY_OBSTRUCTION.md
verify_p5_h22_six_dimensional_equal_weight_binary_obstruction.py
audit_p5_h22_six_dimensional_equal_weight_binary_obstruction.py
```

An orbit-slope audit caught an essential limitation before publication.
Restoring the diagonal-source torus changes the pencils to

```text
D01_rho(r)=(rho r0+r1,r2,r3,r4),
D23_sigma(r)=(r0,r1,sigma r2+r3,r4).
```

These weighted pencils have genuine binary survivor loci.  In
particular, over `C(s,d,u,v,sigma)` the generic `D23` projection leaves

```text
t0=0,
(u-v)t1+u-1=0,
(u-v)t2-sv=0,
t3 free.
```

Therefore the exact equal-weight obstruction is not by itself a
generic six-dimensional-component obstruction.  The weighted
survivors require a separate ternary rank calculation.

### Generic weighted `H22` obstruction on the six-dimensional component

The slope-restored calculation is now closed on the generic component
point.  Over `C(s,d,u,v,r)`, the weighted `D01` projection is the unit
ideal.  The weighted `D23` projection is exactly the marking pencil
displayed above.

On that pencil, a selected `6 x 6` mixed minor is

```text
-2 s^2 u^2 (r-1)^2 (r+1)^3
   (u-1)(u-v)^2(pr-p+1).
```

The two-dimensional extension kernel has one reconstruction direction
whose two diagonals are zero.  On a complementary genuine direction,
the diagonals are

```text
-2r(r-1)(u-v)^2 /
  (su(r+1)(u-1)(pr-p+1)),

2(ru-r+u-v)/(u-1).
```

Thus every genuine binary extension is that direction plus an
arbitrary reconstruction multiple.  For the mode-zero one-marked
`8 x 4` map, adjoin the `0127` and `0137` minors to the fourteen mixed
equations and invert the diagonal product.  The resulting exact ideal
over `C(s,d,u,v,r,p)` is `(1)`.  Every genuine survivor therefore has
marked rank four and cannot factor through three target coordinates.

The independent `F7,F11` audit uses separate DP permanents and modular
row reduction.  It tests `2401+14641=17042` markings in each weighted
direction, recovers only the predicted `D23` marking prefix, and checks
rank four on all `42+110=152` genuine projective extension directions.
Some finite specializations make both selected minors zero, so the
audit deliberately checks the full marked rank; the
characteristic-zero two-minor certificate is over the generic function
field.

```text
P5_H22_SIX_DIMENSIONAL_COMPONENT_GENERIC_OBSTRUCTION.md
verify_p5_h22_six_dimensional_component_generic_obstruction.py
audit_p5_h22_six_dimensional_component_generic_obstruction.py
```

This is the first orbit-generic `H22` component obstruction.  Its
visible slope/parameter divisors, the component boundary, the other
pure components, component exhaustiveness, and the global conjecture
remain open.

### Generic weighted `H22` obstruction on the mixed-orientation component

The weighted diagonal-hyperplane method has now been transported to
the mixed-orientation fivefold.  Over `C(d,p,q,r)`, use its canonical
marked basis with

```text
N=q(d+p+q),
T1111=2N,
beta_i(t_i)=beta_i+t_i alpha_i.
```

For `D01`, the fourteen mixed coefficients form a `14 x 8` matrix
`M01(t)`.  Exhaustive `F5,F7` reconnaissance found rank eight at all
`625+2401` markings, but this modular observation was not promoted.
Direct saturation, all-maximal-minor computation, and several full
projective charts reached their time bounds; those runs are null
results.

The exact proof instead uses a hierarchical projective cover.  The
charts `x2=1` and `x3=1` are unit, so any kernel point has
`x2=x3=0`.  On that subspace the charts `y2=1,y3=1` are unit.  The
remaining kernel would lie in the four-coordinate subspace
`(x0,x1,y0,y1)`, whose four standard projective charts are all unit.
This covers `P7` exactly and proves

```text
ker M01(t)=0
```

for every marking over the algebraic closure of the function field.
No diagonal saturation is needed.

For `D23`, exact elimination after normalizing the first diagonal and
inverting the second gives a proper marking ideal containing

```text
t1*t3,
(t0-1)*t3,
t1*((d+q)*t2-p*q),
(t0-1)*(t2+d-p),
(t0-1)*t1.
```

These relations cover every genuine marking by three closures:

```text
A: t0=1, t1=0;
B: t0=1, t3=0, (d+q)t2=pq;
C: t1=0, t3=0, t2=p-d.
```

On each closure, adjoin the mode-three marked minors with rows `0267`
and `0467` to the mixed equations and invert the product of the two
binary diagonals.  All three exact ideals are `(1)`.  Hence every
genuine `D23` survivor has marked rank four and cannot extend to a
ternary local map.

The self-contained audit over `F5,F7` tests every marking.  It replays
rank eight for every `D01` matrix, finds respectively seven and six
genuine `D23` survivors, verifies that each is on the three-closure
cover with a one-dimensional extension kernel, and finds both selected
minors nonzero on every survivor.

```text
P5_H22_MIXED_ORIENTATION_COMPONENT_GENERIC_OBSTRUCTION.md
verify_p5_h22_mixed_orientation_component_generic_obstruction.py
audit_p5_h22_mixed_orientation_component_generic_obstruction.py
```

The characteristic-zero primary verifier and independent audit are
green.  At that checkpoint the component's parameter/slope divisors
and projective boundary, the other five known component orbits'
generic `H22` incidences, component exhaustiveness, and the global
conjecture remained open.

### Generic weighted `H22` obstruction on the three `1+3` components

The weighted diagonal method was next transported through the shared
radical-plane normal form of `L1,L2,L3`.  Over `C(S,D,G,r)`, exact
binary projection gives

```text
L1 D01=(1),
L2 D01=(1),
L3 D01=(1),
L3 D23=(1).
```

The remaining `L1 D23` ideal is

```text
S*t2+G*(D-S)*t3+(D-S)*(S+G),
(S-D+G)*t1+D*(S-D)*t3+(D-S)*(S-D+G),
(S+G)*t0+1,
t3*(t3+1).
```

It is exactly two rational marking sheets, obtained from `t3=0,-1`.
The remaining `L2 D23` ideal is

```text
(D+G)*t0+1,
t2*t3,
t1*(t3+1),
t1*t2.
```

Its point set is covered by three affine lines:

```text
t1=t2=0;
t1=t3=0;
t2=0, t3=-1,
```

with `t0=-1/(D+G)` throughout.

Modular reconnaissance over `F5,F7` found one fixed marked minor on
every genuine survivor: the mode-zero rows `0247`.  This pattern was
then proved exactly.  On the two `L1` sheets and three `L2` line
closures, adjoining that minor to the fourteen mixed equations and
inverting the product of the two binary diagonals gives `(1)` in all
five cases.  Every survivor therefore has marked rank four.

The independent audit checks all `12,104` branch/pencil markings over
`F5,F7`.  It replays the empty incidences, the two-sheet/three-line
cover, rank-seven one-dimensional extension kernels on every genuine
survivor, and a nonzero `0247` minor in every case.

```text
P5_H22_ONE_THREE_COMPONENTS_GENERIC_OBSTRUCTION.md
verify_p5_h22_one_three_components_generic_obstruction.py
audit_p5_h22_one_three_components_generic_obstruction.py
```

The exact primary verifier and independent audit are green.  Generic
weighted `H22` incidence is now empty on five of the seven certified
pure-component orbits.  Their boundaries, the two earlier rank-two
components, component exhaustiveness, and the global conjecture remain
open.

### Generic weighted `H22` obstruction on the first rank-two component

Transporting the weighted diagonal-hyperplane method to the original
five-parameter component gives a sixth generic exclusion.  After
canonicalization, work over `C(L,Q,C,r)` with

```text
T1111=2(C+L).
```

The weighted `D01` mixed matrix is injective at every marking.  The
proof is an exact hierarchical cover of its projective extension
kernel: the charts `x2=1,x3=1` are unit; after setting
`x2=x3=0`, the charts `y2=1,y3=1` are unit; after setting those four
coordinates to zero, the residual charts
`x0=1,x1=1,y0=1,y1=1` are unit.  Thus the eight charts cover `P7`
without enumerating markings.

For `D23`, put

```text
Z=Q(L+C)(r+1),
H=Z-r+1,
U=LQZ+2LQ+QC(r+1)-r+1,
P=C[LQ(r+1)(Z-r+2)+QC(r+1)-r+1],
R=L^2(r-1)(Z+1),
E=LC(r-1-Z).
```

Exact projection of the normalized binary system gives

```text
P*t2+R*t3+E,
t1,
Q*U*t0+(r-1)*t3+U,
t3*((r-1)*t3+H).
```

Hence every genuine marking is on one of two rational sheets,
`t3=0` or `(r-1)t3+H=0`.  On the first, adjoining the mode-two
`0147` marked minor to the mixed equations and saturating by the two
binary diagonals gives `(1)`.  On the second, the `0137` minor gives
`(1)`.  Every genuine binary extension therefore has marked rank four
and cannot lift to a ternary local map.

The independent `F5,F7` audit exhausts every `D01` marking, reconstructs
both exact `D23` sheets, and checks mixed rank seven, one-dimensional
extension kernel, nonzero diagonals, and the selected nonzero marked
minor at its two generic samples.

```text
P5_H22_FIRST_RANK_TWO_COMPONENT_GENERIC_OBSTRUCTION.md
verify_p5_h22_first_rank_two_component_generic_obstruction.py
audit_p5_h22_first_rank_two_component_generic_obstruction.py
```

Generic weighted `H22` incidence is now empty on six of the seven
certified pure-component orbits.  The remaining generic component
target is the diagonal-quadric component.  Parameter/slope divisors,
projective boundaries, component exhaustiveness, and the global
conjecture remain open.

### Diagonal-quadric weighted `H22` working frontier

The seventh generic target admits a smaller exact formulation.  In the
normal form

```text
U=C+H, S=1+CH, T=H+CE^2, S^2=UT,
```

one may choose the pure basis

```text
alpha_0=Uu_0+Su_1, beta_0=u_0,
alpha_1=y_1,       beta_1=x_1,
alpha_2=y_2,       beta_2=x_2,
alpha_3=Tk_0-Sk_1, beta_3=k_0.
```

Modulo `S^2-UT`, every binary coefficient except `T1111=-4S`
vanishes.  On the dense chart `l=S/U`, row scaling reduces the component
function field to

```text
Q(C,l,r)[E] /
(-C^2 E^2+C^2 l^2+C E^2 l-C l-l^2+1).
```

The relation is linear in `E^2`.  For either weighted diagonal, binary
extension is therefore the rank-drop scheme of a direct `14 x 8`
three-row-permanent matrix over a quadratic field.

Exact elimination on two rational elliptic fibres gives different
answers: at `(e,x,Y)=(2,-3,-12)`, `D01` has two marking sheets and
`D23` is empty; at `(2,-3/4,3/8)`, both are empty.  Projective
compactification exposes invalid proportional-marking survivors at
infinity, so these special fibres do not prove a generic statement.

Small exact finite-field scans likewise separate boundary from interior
behaviour.  At `(C,E,H,r)=(1,1,2,2)`, where `l=1`, both `F5` and `F7`
have isolated genuine rank-seven survivors, all rejected by the
mode-zero `0267` marked minor.  In contrast, the four nondegenerate
ratio-chart points over `F7` have no genuine affine survivor at slope
two; one of eight scans has a rank-drop point, but it fails a diagonal
gate.  These scans are discovery only and do not exclude algebraic
points or prove characteristic-zero genericity.

The exact maximal-minor, projective-kernel, and cofactor-Fitting
computations over the generic quadratic field all exceeded their
600-second caps.  They are recorded as null outcomes.  Exact
factorization of thirteen selected maximal minors did finish.  It
exposes recurrent factors `t3`, `l*t3+1`, `t2+(l^2-1)`, and the
direction-dependent pair `(l-1)t0-1`, `(l+1)t0+1`, but every selected
minor also has a large complementary factor.  These are branch hints,
not a complete support decomposition.  Even substituting the two
`t3` hyperplanes before determinant expansion left four
direction/branch Gröbner jobs beyond a 300-second cap.  The next proof
target is to reduce arithmetic to `a+bE`, decide the saturated
maximal-minor ideal at binary level, and, if it is proper, certify all
four marked Fitting ideals on its survivor algebra with separate
boundary covers.

```text
P5_H22_DIAGONAL_QUADRIC_WORKING_NOTE.md
```

This is an exploratory reframe, not a seventh component theorem.

### Generic weighted `H22` obstruction on the diagonal-quadric component

The generic quadratic-field Gröbner computations above were bypassed
by changing the geometry of the question.  Before marking, the sixteen
binary extension coefficients form the image `S` of a fixed
`16 x 8` multilinear/apolar extension map.  Replacing
`beta_i` by `beta_i+t_i alpha_i` does not move `S`; in fixed dual
coordinates, a binary target has the form

```text
A(t)+q B,

A(t)=tensor_i(alpha_i^*-t_i beta_i^*),
B=tensor_i beta_i^*.
```

After projective compactification, every such target lies in the join
of the Segre fourfold `X=(P1)^4` with its point `B`.  Thus binary
extension is implied by

```text
P(S) intersect J(B,X) != empty.
```

At the exact rational interior point

```text
(C,E,l,r)=(-2/3,-1/4,2,2),
```

the pure coefficient is `T1111=5` and both weighted directions have
extension rank eight.  Exact rational membership equations on the
sixteen standard Segre charts give fifteen unit ideals.  The last
chart gives only

```text
(x0,x1,x2,x3,q+1),
```

where `A=B` and `A+qB=0`; this is the zero-vector base point, not a
projective extension.  Blowing up the coordinate ideal resolves the
join parametrization.  Its exceptional divisor maps to

```text
span(e0111,e1011,e1101,e1110,e1111).
```

This five-space is disjoint from the extension eight-plane in both
directions: the augmented ranks are thirteen, certified by the exact
minors

```text
D01: -3107727,
D23: -6284849697/256.
```

Hence the full projective join intersection is empty at that fibre,
including marking-at-infinity and tangent limits.  On the open where
the extension map has rank eight, the intersection incidence is closed
inside a projective bundle, so its projection to the irreducible base
is proper.  Because the image misses one point, it is a proper closed
subset and misses the generic point.  This proves generic weighted
`H22` emptiness for both directions without a generic function-field
elimination.

The primary Singular verifier and a separate exact SymPy audit using a
subset-DP permanent both pass all thirty-two chart computations and the
exceptional-space ranks:

```text
P5_H22_DIAGONAL_QUADRIC_COMPONENT_GENERIC_OBSTRUCTION.md
verify_p5_h22_diagonal_quadric_component_generic_obstruction.py
audit_p5_h22_diagonal_quadric_component_generic_obstruction.py
```

Generic weighted `H22` incidence is therefore empty on all seven
certified pure-`P4` component orbits.  This is not component
exhaustiveness and does not close special parameter/slope divisors,
all of `H22`, the global lift, or the prize conjecture.

### Eighth pure component from the disjoint mixed-star support

The statement above closed all seven components known at that
checkpoint, but the component list was not exhaustive.  Returning to
the rank-one exceptional star reveals the omitted discrete alternative.
For two relations pointing to the centre and one pointing to a leaf,
the overlapping-support chart used previously has support pattern
`{23,23,02}`.  The distinct supports meet once.  The disjoint pattern
`{01,01,23}` is not a boundary of that normalization.

Normalize the kernel/active rows by

```text
y0=(0,0,1,-1),       x0=(a+b,a-b,0,2),
x1=x2=(1,1,0,0),
y3=(1,-1,0,0),       x3=(0,0,1,1).
```

Put

```text
j=f+b*phi^2,
kappa=phi*(b*f+1),
eta=-(b*f+1),

y1=(-a*f+1,-a*f-1,f+phi,f-phi),
y2=(-a*j+eta,-a*j-eta,j+kappa,j-kappa).
```

A separate subset-DP permanent expansion and the primary expansion
both give only

```text
T1001=-4*Phi,       T1111=4,

Phi=a^2*b*f*phi^2+a^2*f^2
    -b^2*f^2+b^2*phi^2-b*f-1.
```

The polynomial is the determinant of the remaining `3 x 3` linear
kernel system.  As a quadratic in `a`, its coefficient ratio has odd
valuation at `f=0`, so Gauss's lemma proves irreducibility.

At

```text
(a,b,f,phi)=(-12,-10,3/4,-5/28),
```

the hypersurface derivative in `phi` is `350`.  After adding the
diagonal source torus, the exact family tangent has rank five; its
selected minor is

```text
4129/365226400.
```

The universal Segre-incidence Jacobian has rank fifteen in twenty
variables, with selected minor

```text
46800000/34179505129.
```

Thus the family closure is a smooth five-dimensional irreducible
component.  Its generic pair profile is `(4,4,3,4,3,3)`, its directed
signature is `(3 rank-one,0 rank-two,(2,1,0,0))`, and its
diagonal-quadric jump signature is `(1,0)`.  The disjoint-versus-overlap
support intersection distinguishes it from the earlier mixed
component; the other pair and dimension invariants distinguish all
remaining certified orbits.

```text
P4_DISJOINT_MIXED_STAR_PURE_COMPONENT.md
verify_p4_disjoint_mixed_star_pure_component.py
audit_p4_disjoint_mixed_star_pure_component.py
```

The certified lower bound is now eight component orbits: seven
fivefolds and one sixfold.  At this checkpoint the generic `H31` and
weighted `H22` incidences of the eighth component were open; the next
section closes generic `H31`.  Component exhaustiveness and the global
prize conjecture remain unresolved.

### Generic marked `H31` fibre on the eighth component

Use the component's pure-factor bases `(alpha_i,beta_i)=(y_i,x_i)` and
write every marked basis as `beta_i+t_i alpha_i`.  Over

```text
K=C(a,b,f)[phi]/(Phi),

Phi=a^2*b*f*phi^2+a^2*f^2
    -b^2*f^2+b^2*phi^2-b*f-1,
```

the exact saturated projection of the genuine binary-neighbour
incidence is unit for distinguished source coordinates zero and one.
For coordinates two and three it is respectively

```text
(Phi,t1,t2,t3,L2),       (Phi,t1,t2,t3,L3),
```

where

```text
G=a^2*b*f^2+2*b^2*f+b,

L2=G*phi+(1-a^2*f^2)*t0
   +3*a^2*f^2-2*b^2*f^2-2*b*f-3,

L3=G*phi+(1-a^2*f^2)*t0
   -a^2*f^2+2*b^2*f^2+2*b*f+1.
```

Bidirectional ideal reduction proves these are the complete
projections, not merely necessary equations.  Thus each surviving
coordinate has one marking over the component function field.

On either marking the mixed extension matrix has rank six.  Exact
reduction modulo `(Phi,Lq,Mq*z)` gives

```text
det P2(z)[0137] =  R*A2(z)*B2(z)^2,
det P3(z)[0137] = -R*A3(z)*B3(z)^2,

R=f*(b*f+1)*(1-a^2*f^2)/(a^2*f+b).
```

Every genuine binary extension has both diagonals nonzero, so on the
dense open where `R!=0` its mode-zero one-marked map has rank four and
cannot factor through a ternary target local space.  The generic
marked `H31` fibre is empty.

The characteristic-zero verifier performs the four projections and
both all-extension reductions.  An independent subset-DP/modular audit
at generic points over `F_11` and `F_13` exhausts the marked bases,
recovers exactly the two projected markings, and replays the minor
identity on every genuine projective kernel direction:

```text
P5_H31_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md
verify_p5_h31_disjoint_mixed_star_component_generic_obstruction.py
audit_p5_h31_disjoint_mixed_star_component_generic_obstruction.py
```

All eight currently certified pure-component orbits are therefore
generically closed for `H31`.  The eighth component's special
parameter/projective boundary, its weighted `H22` incidence, component
exhaustiveness, and the global prize conjecture remain unresolved.

### Weighted `H22` working frontier on the eighth component

The weighted source directions were tested exactly at generic points
over `F_11` and `F_13`, with every affine marking and every genuine
projective extension direction replayed.  The `D_01` survivor marking
locus obeys `t_1*t_2=0`; the `D_23` locus obeys
`t_1=t_2=t_3=0`.  Every surviving mixed matrix has rank seven, and
the mode-zero one-marked map has rank four.

This is finite-field evidence only.  Direct characteristic-zero
Fitting ideals and most split marking saturations timed out.  Two
smaller `D_23` charts reduced to the unit ideal, but they do not cover
the unresolved `t_1!=0` and `t_2!=0` charts.  No `H22` theorem was
claimed:

```text
P5_H22_DISJOINT_MIXED_STAR_WORKING_NOTE.md
explore_p5_h22_disjoint_mixed_star_modular.py
```

### Generic weighted `H22` fibre on the disjoint mixed-star component

The modular pattern above has now been promoted to an exact
characteristic-zero theorem without repeating the broad elimination
that timed out.

For each weighted direction `D_01^r,D_23^r`, form the `14 x 8` matrix
of mixed binary coefficients.  On `D_23^r`, seven selected `8 x 8`
minors force

```text
t_1=t_2=t_3=0.
```

Two mode-zero one-marked minors, together with the two nonzero binary
diagonals, then generate the unit ideal.

On `D_01^r`, a different seven-minor ideal is zero-dimensional of
vector-space dimension ten over `C(a,b,f,r)`.  Since the component
equation is quadratic in `phi`, this is a degree-five marking scheme
over the component field.  One `7 x 7` pivot is invertible on the
whole scheme, so the selected minors define the exact rank-drop locus.
The basis contains `t_1*t_2`; on `t_1=0`, two further factored
relations give the complete cover

```text
t_2=0,
t_1=t_3=0,
t_1=L_3=L_2=0.
```

One- or two-minor ternary Fitting ideals are unit on all three charts.
Thus the generic weighted `H22` fibre of the eighth component is empty.
All eight currently certified pure-`P_4` component orbits are now
generically closed for both `H31` and weighted `H22`.

This remains a dense-open theorem.  Special parameter/slope/projective
boundaries, component exhaustiveness, the complete `P_5 -> Delta_3`
obstruction, and the global prize conjecture remain unresolved.

```text
P5_H22_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md
verify_p5_h22_disjoint_mixed_star_component_generic_obstruction.py
audit_p5_h22_disjoint_mixed_star_component_generic_obstruction.py
```

### Equal- and opposite-weight slope fibres

The generic weighted theorem uses a determinantal marking chart that
degenerates at `r^2=1`.  Specializing before elimination makes both
slope fibres simpler.

For each direction `D_01,D_23`, let `M_D(t)` be the fourteen-row mixed
coefficient matrix and `A_D,B_D` the two binary diagonals.  Over the
generic component-parameter field, exact standard bases give

```text
r= 1:  M_D(t)z=0  implies A_D(z)=0,
r=-1:  M_D(t)z=0  implies B_D(z)=0.
```

Equivalently, normalizing the indicated diagonal to one makes each of
the four mixed-incidence ideals the unit ideal.  Since a binary
`Delta_2` neighbour requires both diagonals nonzero, neither slope
admits even a binary extension.  No one-marked ternary minor is needed.

```text
P5_H22_DISJOINT_MIXED_STAR_EQUAL_OPPOSITE_WEIGHT_OBSTRUCTION.md
verify_p5_h22_disjoint_mixed_star_equal_opposite_weight_obstruction.py
audit_p5_h22_disjoint_mixed_star_equal_opposite_weight_obstruction.py
```

### Twelve parameter/coordinate boundary branches

Factoring `Phi` on

```text
a^2-b^2=0,  bf+1=0,  b=0,  f=0,  a=0,  phi=0
```

produces ten rational rank-two branches and two irreducible quadratic
branches.  The two additional branches on `bf=-1,b phi=+/-1` have
`y_2=0` and lie outside the all-rank-two stratum.

For both weighted directions, twenty-four exact ideals combine genuine
binary normalization with one or two mode-zero one-marked minors.  The
standard rows `0137,0157` close every branch except `f=0` in direction
`D_01`; there the finite survivor cover identifies `0157,0457`, and
that alternate characteristic-zero ideal is unit.

```text
P5_H22_DISJOINT_MIXED_STAR_PARAMETER_PIVOT_BOUNDARY_OBSTRUCTION.md
verify_p5_h22_disjoint_mixed_star_parameter_pivot_boundary_obstruction.py
audit_p5_h22_disjoint_mixed_star_parameter_pivot_boundary_obstruction.py
```

### Principal coupled slope-parameter boundary

The remaining visible coefficient in the degree-five cover is

```text
C=r(a^2 f+abf+a+b)+(-a^2 f+abf+a-b).
```

On the chart where the first parenthesis is nonzero, `C=0` is a
rational slope graph.  Direction `D_01` is excluded by the mode-one
minor `0457`, while `D_23` is excluded by the mode-zero minor `0137`.
If the denominator also vanishes, the equations force
`bf=-1,a=+/-b`, already in the parameter-boundary theorem.

```text
P5_H22_DISJOINT_MIXED_STAR_COUPLED_SLOPE_BOUNDARY_OBSTRUCTION.md
verify_p5_h22_disjoint_mixed_star_coupled_slope_boundary_obstruction.py
audit_p5_h22_disjoint_mixed_star_coupled_slope_boundary_obstruction.py
```

The suggested continuation is to classify the special
parameter/slope/projective boundaries still hidden in the exact
standard-basis certificates, then finish the exceptional
mixed-star/triangle and lower pair-rank strata needed for component
exhaustiveness.

### Symbolic pair pencils and triangle holonomy

The lower-pair-rank frontier has now been translated away from
permanent ideals.

For two local planes `U,V` with `dim(UV)=2`, the projective
multiplication kernel is a line in `P(U tensor V)=P^3`.  The rank-one
relations form the Segre quadric.  A squarefree linear form has
degree-one annihilator dimension at most one, so the kernel line cannot
be a Segre ruling.  It is therefore secant or tangent.  The secant
case reduces to the existing `2+2`/`1+3` block centers.  Exact-rank-two
tangency can occur only when

```text
U=V=span(X_p,w),       |supp(w)|>=2.
```

This is a computation-free classification of a single rank-two pair
kernel:

```text
P4_RANK_TWO_PAIR_KERNEL_GEOMETRY.md
verify_p4_rank_two_pair_kernel_geometry.py
```

For a triangle of rank-three pair images whose three relation matrices
have rank two, the three relations carry a multiplicative holonomy.
Writing their nonconstant coefficients as `b_ij,c_ij`, put

```text
Omega=c_12*b_13*c_23+b_12*c_13*b_23.
```

On `Omega!=0`, three Borel row shifts remove all constant terms and
the same determinant `-Omega` forces all six mixed triple products to
vanish.  Each cross-product is annihilated by the opposite local
plane.  Its degree-two multiplication catalecticant is a nonzero
symmetric zero-diagonal matrix of rank two, hence a weighted cut.
The only cut types are `1+3` and `2+2`; the latter has one tetrad
equation.  The full-support all-`1+3` compatibility is now closed
below.  At that checkpoint the resonant divisor, cycles containing
`2+2`, and proper cut-support boundaries remained; the following two
sections close the latter two, leaving only resonance.

```text
P4_NONRESONANT_RANK_TWO_TRIANGLE_CUT_REDUCTION.md
verify_p4_nonresonant_rank_two_triangle_cut_reduction.py
```

### Full-support `1+3` triangle cycles are empty

Let `Q_ij` be the three nonzero bridge quadrics on the nonresonant
rank-two-relation triangle, and assume each is a full-support `1+3`
cut with singleton label `s_k`.

For a representative

```text
q=q_12 X_1X_2+q_13 X_1X_3+q_23 X_2X_3,
```

any factorization `q=uv` is either internal to `X_0=0` or has

```text
v_j=-(v_0/u_0)u_j.
```

The identity

```text
u_0 q_jk+2v_0u_ju_k=u_je_k+u_ke_j
```

shows that the second sheet is fully supported.  But
`Ann_R1(Q_ij)` is a plane inside the singleton coordinate hyperplane.
Every bridge factor comes from one of these planes, so only the
internal sheet can occur.

Cyclically every `U_i` lies in all three singleton hyperplanes.  Three
distinct labels leave dimension one; two distinct labels leave one
coordinate two-plane, whose product has rank one.  Thus all labels
coincide.  The whole restriction then suspends a pure `P_3`
restriction.  Perfect pairing in the three-variable squarefree
algebra gives

```text
rank(U_iU_j)+2-3 <= 1,
```

so every pair rank is at most two, contradicting the triangle
hypothesis `rank(U_iU_j)=3`.

Hence the full-support all-`1+3` nonresonant triangle is empty.  Its
forced rank-drop closure is the already known embedded-`P_3`
component, whose complete marked projective `H31` fibre is empty.
At this checkpoint, cycles containing a `2+2` bridge, proper support
boundaries, and the resonant divisor remained.

```text
P4_NONRESONANT_ONE_THREE_TRIANGLE_OBSTRUCTION.md
verify_p4_nonresonant_one_three_triangle_obstruction.py
audit_p4_nonresonant_one_three_triangle_obstruction.py
```

### Full-support `2+2` bridges are incompatible with the triangle

Write a full `2+2` bridge as

```text
q=ab
```

across two coordinate binary blocks `A,B`, and let `a_bar,b_bar` be
the opposite binary directions.  Then

```text
Ann_R1(q)=span(a_bar,b_bar).
```

There are two short lemmas.

First, every factorization `q=uv` contains an anchor factor in
`C*a` or `C*b`.  Decompose the factors into their `A,B` blocks.  The
cross-block matrix has rank one, and

```text
det(u_A tensor v_B+v_A tensor u_B)
 =-det(u_A,v_A)det(u_B,v_B).
```

One pair of same-block pieces is therefore dependent.  Its direction
is the corresponding full-support anchor; the internal zero-product
equation then kills one piece, leaving the other whole factor on the
opposite anchor line.

Second, every plane `V` whose product with
`W=span(a_bar,b_bar)` has rank three and unique rank-two relation has
the crossed-graph form

```text
V=span(
 alpha*a+tau*b_bar,
 -tau*a_bar+beta*b
),
tau!=0.
```

The formula comes by splitting
`a_bar*v+b_bar*w=0` into its internal and cross-block pieces.  If
`tau=0`, the two products vanish separately and the kernel has
dimension at least two.  For `tau!=0`, the displayed plane contains
neither anchor `a` nor anchor `b`.

Now take `Q_12=q`.  Its opposite plane is `U_3=W`; the two remaining
rank-three edges put both `U_1,U_2` in crossed-graph form, so neither
contains an anchor.  But the bridge factorization
`q=b_12*y_1*x_2` requires one.  Contradiction.

Together with the all-`1+3` theorem, every full-support nonresonant
rank-two-relation triangle is empty.  At this checkpoint, proper
bridge-support boundaries and the resonant divisor remained.

```text
P4_NONRESONANT_TWO_TWO_TRIANGLE_OBSTRUCTION.md
verify_p4_nonresonant_two_two_triangle_obstruction.py
audit_p4_nonresonant_two_two_triangle_obstruction.py
```

### Proper cut supports close the nonresonant triangle

A proper nonzero `1+3` cut has one or two triangle edges.  A proper
`2+2` outer-product cut has support size two or one.  Thus, up to
coordinates, every remaining bridge is

```text
q=X_0X_1
```

or

```text
q=X_0(alpha X_1+beta X_2),       alpha beta!=0.
```

For the single edge, `Ann_R1(q)=span(X_0,X_1)`.  If `V` is a
rank-three partner with rank-two kernel relation, choose its basis
`v,w` so that

```text
X_0v+X_1w=0.
```

Coefficient comparison forces `v,w` back into
`span(X_0,X_1)`, whose product with the annihilator has dimension at
most one.  Contradiction.

For the two-edge star, put

```text
b=alpha X_1+beta X_2,
b_bar=alpha X_1-beta X_2.
```

Then `Ann_R1(q)=span(X_0,b_bar)` lies in `X_3=0`.  The partner
relation

```text
X_0v+b_bar*w=0
```

has `X_0X_3`, `X_1X_3`, and `X_2X_3` coefficients
`v_3,alpha*w_3,-beta*w_3`, so every partner lies in `X_3=0` as well.
All three triangle planes therefore lie in that hyperplane.  The
`P_4` restriction suspends a nonzero pure `P_3`, and perfect pairing
gives pair rank at most two, contradicting the assumed rank three.

This closes every proper cut support.  Together with the two
full-support theorems, the complete nonresonant rank-two-relation
triangle is empty.  Only the trivial-holonomy resonant divisor
remains.

```text
P4_NONRESONANT_DEGENERATE_CUT_TRIANGLE_OBSTRUCTION.md
verify_p4_nonresonant_degenerate_cut_triangle_obstruction.py
audit_p4_nonresonant_degenerate_cut_triangle_obstruction.py
```

### The resonant triangle is an affine connection

On the remaining divisor `Omega=0`, active-row and relation scalings
normalize the three rank-two relations to

```text
A_ij*y_i*y_j+y_i*x_j-x_i*y_j=0.
```

Borel shifts `x_i -> x_i+s_i*y_i` change
`A_ij -> A_ij+s_i-s_j`.  The unique residual class on the cycle is

```text
delta=A_12+A_23-A_13.
```

For `delta!=0`, multiplying the three relations first by the remaining
kernel row and then by the remaining active row gives two copies of
the same cycle identity.  In the notation

```text
Y=yyy,
K_i=(one active),
J_i=(two active),
X=xxx,
```

one obtains

```text
Y=K_1=K_2=K_3=0,
J_1=J_2=J_3=J.
```

Thus the `R_3`-valued triple tensor is the tangent first jet

```text
J(yxx+xyx+xxy)+Xxxx.
```

Moreover each kernel-pair product `q_ij=y_i*y_j` is nonzero and is
annihilated by the full opposite plane.  Its zero-diagonal
catalecticant has rank exactly two, so the three `q_ij` form a cyclic
`1+3`/`2+2` cut system.  Purity adds `U_0*J=0` and a nonzero
`U_0*X` covector.

For `delta=0`, one gauge kills all `A_ij`.  The three relations become
`y_i*x_j=x_i*y_j`, and every triple product depends only on Hamming
weight.  Multiplication factors through

```text
Sym^3(C^2) -> R_3,
y^3,y^2x,yx^2,x^3 -> Y,K,J,X.
```

The perfect `R_1 x R_3` pairing and purity imply

```text
dim span(Y,K,J)<=2,
X notin span(Y,K,J).
```

The last triangle divisor is therefore a tangent-cut incidence versus
a compressed binary-cubic map.  This is a reduction, not yet an
exclusion.

```text
P4_RESONANT_RANK_TWO_TRIANGLE_AFFINE_HOLONOMY_REDUCTION.md
verify_p4_resonant_rank_two_triangle_affine_holonomy.py
audit_p4_resonant_rank_two_triangle_affine_holonomy.py
```

### Ninth pure component from the common `1+3` boundary

Following the common `1+3` cut rather than discarding its pair-rank
drop exposes a new component.  Put three modes in `X_0=0` and use the
pure-`P_3` sign chart with normals

```text
(1,A,B),       (1,-A,-B),       (1,-A,B).
```

Let the fourth mode be an arbitrary plane not contained in `X_0=0`.
In fixed Grassmann charts the resulting six-parameter family has only

```text
T_0010=-2/B,       T_0110=-2A/B.
```

Its family tangent has rank six.  At the rational point

```text
(r,s,t,u,A,B)=(3/2,1/2,1,2,2,3),
```

the Segre-incidence Jacobian has rank fourteen and the selected
`14 x 14` minor is `114688/2187`.  Thus the family closure is a
generically smooth six-dimensional component.  Its generic pair
profile

```text
(4,4,4,2,2,2)
```

separates it from the earlier six-dimensional component and all seven
fivefolds.  The certified lower bound is now nine pure-`P_4`
component orbits.

```text
P4_EMBEDDED_P3_PURE_COMPONENT.md
verify_p4_embedded_p3_pure_component.py
audit_p4_embedded_p3_pure_component.py
```

The ninth component's generic marked `H31` fibre is now excluded in

```text
P5_H31_EMBEDDED_P3_COMPONENT_GENERIC_OBSTRUCTION.md
verify_p5_h31_embedded_p3_component_generic_obstruction.py
audit_p5_h31_embedded_p3_component_generic_obstruction.py
```

On the dense normalization `A B r!=0`, the three deletions retaining
source coordinate zero have identically zero all-alpha diagonal.
Deleting source coordinate zero gives the apolar insertion tensor

```text
D_w(u_1,u_2,u_3)
 =sum_i ell_i(u_i) P_3(w,u_j,u_k).
```

Its seven unwanted coefficients form a `7 x 6` matrix.  The maximal
minors cut out exactly the signed lines

```text
p-q-rho=0,       p-q+rho=0,       p+q+rho=0
```

plus the three coordinate points.  Away from nine exceptional
projective points, the three line kernels are respectively the
coordinate covectors `z_2,z_3,z_1`; all have
`x_1=x_2=x_3=0`.  A generic projected mode-zero line avoids those nine
points, with exact discriminant

```text
-T(T-1)(T+1)(ST-U)
 (ST-T-U)(ST+T-U)(ST-U-1)(ST-U+1).
```

Thus every possible mixed kernel kills the second binary diagonal.
No ternary/Fitting continuation is needed.  This closes the generic
`H31` fibre for all nine certified components.

The generic weighted `H22` fibre is now excluded in

```text
P5_H22_EMBEDDED_P3_COMPONENT_GENERIC_OBSTRUCTION.md
verify_p5_h22_embedded_p3_component_generic_obstruction.py
audit_p5_h22_embedded_p3_component_generic_obstruction.py
```

After restoring the weighted source-torus slope `r`,

```text
D_01^r(z,e)=(r z_0+z_1,z_2,z_3,e),
D_23^r(z,e)=(z_0,z_1,r z_2+z_3,e).
```

The `D_23` all-alpha matrix has a zero first column because every
`alpha_i` has source-coordinate-zero entry zero.  The `D_01`
direction is the same `P_3` insertion map as in `H31`, now over

```text
P span((1,S,U),(r,1,T)).
```

Its exact nine-point avoidance discriminant is

```text
(rS-1)(rU-T)(ST-U)
(rS-rU+T-1)(rS+rU-T-1)
(rS-ST+U-1)(rS+ST-U-1)
(rU-ST-T+U)(rU+ST-T-U).
```

On its complement, the only rank-jump kernels again have all
`x_i=0`, so the other binary diagonal vanishes.  Both `H22`
directions therefore fail before ternary rank is imposed.

All nine currently certified pure-`P_4` components now have empty
generic marked `H31` and weighted `H22` fibres.  Their special
boundaries, component exhaustiveness, and the global Krenn--Gu
conjecture remain unresolved.

### Complete normalized ninth-component `H31` boundary

The nine insertion points have now been classified and closed in

```text
P5_H31_EMBEDDED_P3_COMPONENT_NORMALIZED_BOUNDARY_OBSTRUCTION.md
verify_p5_h31_embedded_p3_component_normalized_boundary.py
audit_p5_h31_embedded_p3_component_normalized_boundary.py
```

The exact kernels at the six line-special points are coordinate
planes such as `<x_2,z_2>` or `<z_2,z_3>`; the three coordinate-point
kernels are one-dimensional.  Imposing the other mode-zero slice as a
truncated Segre tensor leaves exactly the projected-plane strata

```text
T=1,U=S+1;       T=1,U=S;       T=0,U=1.
```

They contain five marked binary families.  Four are excluded by pairs
of one-marked minors with factors among

```text
y, h, h-1, S, S+1, Sy+1, y+1.
```

At the sole deepest point `S=0,y=1`, all four neighboring one-marked
maps have rank three, but stacking the mode-one equations for source
contractions `e_0` and `e_4` gives the five-row determinant

```text
det rows(0,2,7,10,14)=8.
```

Thus the third target row vanishes globally, contradicting local rank
three.  The full normalized affine chart is closed for `H31`; the
omitted normalization/projective boundary remains.  The normalized
weighted `H22` boundary is closed by the two subsequent theorems below.

### Rank-two projected-line weighted boundary of the ninth component

The special weighted boundary has now been classified without a broad
elimination in

```text
P5_H22_EMBEDDED_P3_COMPONENT_RANK_TWO_LINE_BOUNDARY_OBSTRUCTION.md
verify_p5_h22_embedded_p3_component_rank_two_line_boundary.py
audit_p5_h22_embedded_p3_component_rank_two_line_boundary.py
```

For projected line

```text
Lambda_r=P span((1,S,U),(r,1,T)),
```

the insertion arrangement leaves exactly four rank-two strata:

```text
U=S+1,T=r+1;   U=S,T=1;   U=1,T=r;   S=r=-1.
```

Their truncated-Segre equations leave six marked binary families.
Small one-marked minors factor into complementary covers.  At the two
deepest points every neighboring map has rank three, but stacking the
weighted source contraction with the extension direction gives

```text
det=8,             det=-8.
```

Thus the weighted marked fibre is empty on every rank-two projected
line.  The remaining chart frontier is precisely the collapse

```text
rS=1,             T=rU,
```

where the two projected rows are proportional and `Lambda_r` becomes
a point.  This is not covered by the line-arrangement argument.

### Complementary-pencil closure of the rank-one collapse

The collapse is now closed in

```text
P5_H22_EMBEDDED_P3_COMPONENT_RANK_ONE_COLLAPSE_OBSTRUCTION.md
verify_p5_h22_embedded_p3_component_rank_one_collapse.py
audit_p5_h22_embedded_p3_component_rank_one_collapse.py
```

The first mixed coefficient forces `t_0=-r`.  The `D_01` beta row then
projects entirely to the extension coordinate, with beta diagonal
`-2y_0`.  Compatibility with `H22` requires the other marked slice
`D_23` to be nonzero pure.  After undoing the harmless markings in the
last three modes, its seven unwanted coefficients form a `7 x 6`
insertion pencil `N_S`.  Four nonzero maximal minors are

```text
+/-4(S-1)^2(S+1)^2/S^5.
```

Hence only `S=+/-1` can survive.  At `S=1`,

```text
ker N_1=<x_3,z_3>,
```

but the desired `D_23` pure coefficient vanishes on the kernel.  At
`S=-1`,

```text
ker N_{-1}=<z_1,z_2>,
```

so every alpha extension vanishes and the required `D_01` alpha
diagonal is zero.  Thus the collapse has no binary `H22`
compatibility.  Together with the rank-two theorem, the entire
normalized affine weighted `H22` chart of the ninth component is now
empty.  The omitted normalization/projective boundary remains.

### Support-two `H31` normalization divisor of the ninth component

The divisor `A=0`, `B!=0` has now been closed exactly in

```text
P5_H31_EMBEDDED_P3_COMPONENT_SUPPORT_TWO_BOUNDARY_OBSTRUCTION.md
verify_p5_h31_embedded_p3_component_support_two_boundary.py
audit_p5_h31_embedded_p3_component_support_two_boundary.py
```

The three nonzero-mode planes specialize to the support-two pure
`P_3` sign chart with residual source-torus scalar `C=1/B`.  Its
beta-slice extension problem is the singular `7 x 6` pencil
`N_C(p,q,rho)`.  A maximal minor is

```text
4 C q (Cp-rho)^2 (Cp+rho)^3,
```

but the all-alpha diagonal and the first unwanted row sharpen this:
every genuine binary family lies on `rho=-Cp`.  If `p!=0`, the
alpha-slice equations reduce to

```text
t2=0,  z1=2ht1,  z3=2ht3,  t1 t3=0,
```

and a neighboring one-marked determinant

```text
16 C^2 h^2 p^2 (CP+R) D
```

plus the transverse pure entry `-2Cp` excludes it.  At the coordinate
endpoint `p=rho=0`, the third root contraction has mixed coefficient
`(C+1)X`, leaving only the matrix-pencil resonance `C=-1`.

The resonant fibre has two invariant subcases.  When `P+R!=0`, three
factored one-marked covers leave one point, where a stacked map has
determinant

```text
-8 h^2 (P-R)^2 (P+R).
```

When `P+R=0`, the root equations force the antipodal ratios
`x=1/2,d=-1/2`.  Two one-marked covers leave `k=Q=0`; there the
pure-plus-neighbor kernel is `<(0,0,-2,0,1)>`, and its third-root
`BBBG` coefficient is the fixed integer `4`.  Hence the entire
support-two divisor is empty for `H31`.

This closes one genuine normalization face rather than a coordinate
artifact.  At that checkpoint, the other mode-zero-plane chart and
the projective compactification remained open, as did component
exhaustiveness and the global conjecture.  The next section closes the
former chart.

### The `r=0` tangent--Segre boundary of the ninth component

The remaining affine `H31` normalization divisor has now been closed
in

```text
P5_H31_EMBEDDED_P3_COMPONENT_R_ZERO_BOUNDARY_OBSTRUCTION.md
verify_p5_h31_embedded_p3_component_r_zero_boundary.py
audit_p5_h31_embedded_p3_component_r_zero_boundary.py
```

Assume `A B!=0,r=0`.  If `t!=0`, the signed source permutation

```text
X2'=-X3,        X3'=-X2
```

sends `r'=-t!=0` and exchanges the two nonzero pure-`P_3` sign
parameters.  This is the already closed normalized chart.  The
genuine corner is therefore `r=t=0`, where mode zero contains the
coordinate point `e0`.

After marking the last three beta rows by `a,b,c`, the six mixed
coefficients of the alpha insertion tensor have determinant

```text
-4(S-U-1)(S+U-1)(S+U+1) Phi.
```

Here

```text
Phi =
 S{U[(S-U)(a+1)(b+1)-a(b+1)+1]+b(S+1)}
 +c{Sb(S+U+1)+Ua(1-S-U)}.
```

This is the pullback of a tangent--secant incidence for the
`P1 x P1 x P1` Segre variety.  The three signed linear sheets have
generic kernels `<y3>,<y2>,<y1>`, all with zero `AAA`.  On the
residual sheet, a cofactor kernel has diagonal

```text
2 S U (S-U-1)(S+U-1)(S+U+1).
```

Three neighboring determinants have residual factors

```text
b+1,       a+1,       a,
```

so they cover the whole open sheet.

The boundary is still exact and small.  The `S=0` and `U=0` parts
give four branches with direct nonzero minors.  On each signed plane,
the associated `6 x 5` Fitting ideal has three branches, for nine
families total; every family has a one-marked determinant equal to
`8Y^2` times a chart unit.  Only five base points remain.  Two force
`AAA=0`; the other three have nine genuine marking families.  Seven
have constant determinants `4Y^2` or `8Y^2`, while the last two are
covered by `a,a+1` or `b,b+1`.

Thus the complete `r=0`, `A B!=0` marked fibre is empty.  Together
with the normalized theorem and the support-two `A=0` theorem, the
whole affine ninth-component family `B!=0` is empty for `H31`.
At that checkpoint only the projective compactification remained for
this component; component exhaustiveness and the global conjecture
remained open.

### Projective normal support closes the ninth component

The final compactification is now closed in

```text
P5_H31_EMBEDDED_P3_COMPONENT_PROJECTIVE_CLOSURE_OBSTRUCTION.md
verify_p5_h31_embedded_p3_component_projective_closure.py
audit_p5_h31_embedded_p3_component_projective_closure.py
```

The intrinsic base is not the inverse-pivot coordinate `B`; it is the
homogeneous absolute normal

```text
[C:A:B] in P2
```

with oriented sign-face normals

```text
(C,A,B),      (C,-A,-B),      (C,-A,B).
```

On `C!=0`, the only nonzero pure-`P_3` coefficients are

```text
2 A C^2,       -2 B C^2.
```

If the homogeneous normal has support one, all three projective
normals coincide and the pure `P_3`, hence embedded `P_4`,
restriction is zero.  Such a point cannot be the nonzero pure root
contraction required by `Delta_3`.

Every point of support at least two has two nonzero normal
coordinates.  A source-coordinate permutation moves them to the
common slot `C'` and sign slot `B'`; after projective rescaling,
`C'=1,B'!=0`.  Signed source changes and a last-three-mode permutation
restore the canonical oriented face.  Thus every nonzero projective
point lies in a symmetry copy of the affine chart already closed.

Therefore the ninth pure-`P_4` component's complete marked `H31`
fibre is empty.  This is a full component theorem, but not a proof
that the then-known nine pure components are exhaustive and not a global
solution of the Krenn--Gu problem.

### Nonzero additive holonomy is empty

The tangent branch of the resonant triangle reduction is now closed
in

```text
P4_RESONANT_NONZERO_ADDITIVE_HOLONOMY_OBSTRUCTION.md
verify_p4_resonant_nonzero_additive_holonomy_obstruction.py
audit_p4_resonant_nonzero_additive_holonomy_obstruction.py
```

When `delta!=0`, the three nonzero products

```text
q_ij=y_i y_j
```

have catalecticant rank two and the full opposite plane as their
annihilator.  They are therefore cut quadrics.  A proper cut support
is excluded by the earlier partner-rank argument.  A full `2+2` cut
is excluded because its factorization `y_i y_j` must use an anchor,
whereas every rank-three crossed partner avoids both anchors.

If all three cuts have full `1+3` support, each factorization is on
the internal sheet: the other sheet is fully supported, while the
factors already lie in coordinate hyperplanes.  Three distinct
singleton labels collapse the factors to a coordinate line, and two
labels collapse them to a coordinate two-plane.  Hence the labels
coincide.  All three local planes then lie in one coordinate
hyperplane, so the restriction suspends a pure `P_3`.  Perfect
pairing gives pair-image rank at most two, contradicting the triangle
hypothesis.

Thus

```text
Omega!=0                 empty,
Omega=0, delta!=0        empty,
Omega=0, delta=0         open flat binary-cubic branch.
```

This is a symbolic cut/duality proof and uses no component search.

### The one-kernel-zero flat chart is a binary-cubic problem

The one-kernel-zero, otherwise-distinct part of the last resonant
branch is closed in

```text
P4_RESONANT_FLAT_KERNEL_ZERO_BINARY_CUBIC_OBSTRUCTION.md
verify_p4_resonant_flat_kernel_zero_binary_cubic.py
audit_p4_resonant_flat_kernel_zero_binary_cubic.py
```

A kernel row with one zero coordinate and three otherwise-distinct
projective columns has the Borel normal form

```text
y=(1,0,1,1),       x=(0,1,1,lambda).
```

Every synchronized partner lies in the exact pencil `A+t A_sharp`.
For two partner parameters `t,u`, put the binary-cubic coefficients
in `C=[Y K J X]`.  A fixed `2 x 2` minor makes `K,J` independent.
One compression minor is `8(lambda-1)F`, while the complete third
compound factors as

```text
C_3(C)=8F N.
```

Purity therefore forces both `rank C=3` and `rank C<=2`.  The one- and
two-infinite projective pencil sheets close by the analogous factor
`lambda*u^2-1` and the nonzero minor `-8lambda^4`.  Consequently no
flat triangle can lie in this one-kernel-zero chart.

### WITHDRAWN: overstrong projective collision classification

The following claimed exhaustiveness was withdrawn.  It used full row
`GL2` to classify projective columns, but purity fixes each kernel
line and permits only Borel row gauge.  The displayed balanced family
and normal-form identities are exact; the claim that they exhaust the
flat branch and the four-dimensional component conclusion are not.

The withdrawn record is

```text
P4_RESONANT_FLAT_TRIANGLE_CLASSIFICATION_WITHDRAWN_OVERSTRONG.md
verify_p4_resonant_flat_triangle_classification_withdrawn_overstrong.py
audit_p4_resonant_flat_triangle_classification_withdrawn_overstrong.py
```

A zero source column propagates to all synchronized partners and
descends to the embedded pure-`P3` obstruction.  A `2+1+1`
projective collision makes every active row proportional to a
two-supported row, so `X=x^3=0`.  A `1+3` split makes all three planes
coincide and their square has dimension two.

The sole survivor is the balanced `2+2` family

```text
U0=span(a_bar,b_bar),
U1=span(a,b),
U2=span(a,b+s*a_bar),
U3=span(a,b+t*a_bar),                    s+t!=0.
```

Its restricted permanent is exactly `-4(s+t) x0*x1*x2*x3`; all three
triangle pair images have rank three and unique rank-two relations.
Thus the flat branch is nonempty, but its normalized two parameters
plus the source torus sweep dimension at most four.  Every nonzero
pure-incidence component has dimension at least five by its
twenty-variable/fifteen-equation Segre chart.  Hence the complete
rank-two-relation triangle cannot be the generic graph of a missing
component.

### WITHDRAWN: overstrong pure rank-two-relation star obstruction

The star conclusion below depended on the withdrawn complete triangle
classification.  Its tree gauge, pencil matching, and constant
balanced-chart coefficient remain local lemmas, but the global star
obstruction is not established.

The other three-edge graph is closed in

```text
P4_RANK_TWO_RELATION_STAR_OBSTRUCTION_WITHDRAWN_OVERSTRONG.md
verify_p4_rank_two_relation_star_obstruction_withdrawn_overstrong.py
audit_p4_rank_two_relation_star_obstruction_withdrawn_overstrong.py
```

Because a star is a tree, the three rank-two relations can be gauged
independently to

```text
y0*xi=x0*yi.
```

Thus all three leaf row-pairs lie in the synchronizer of the center.
For a generic four-point center this is the projective pencil
`A+t*A_sharp`.  Two pencil members have pair rank below three only
when their parameters form one of three disjoint pairs, cut out by
two of

```text
lambda*t*u-1,
lambda*t*u-t-u+1,
lambda*t*u-lambda*t-lambda*u+1.
```

The rank-drop graph is therefore a matching.  Among three leaves some
pair has rank three, so it and the center form the already classified
generic flat triangle, a contradiction.

The collision boundary is smaller.  Zero columns make the whole
degree-four product zero.  A `2+1+1` center forces all active rows to
one two-supported vector, whose fourth power is zero.  A `1+3`
center makes every leaf the same plane and drops center-leaf rank to
two.  Finally, at the balanced `2+2` center, the coefficient selecting
the center kernel, one leaf kernel, and two leaf active rows is

```text
a(a+beta*b_bar)(b+alpha*a_bar)(b+gamma*a_bar)=a^2*b^2=4,
```

contradicting purity.

Consequently an all-pair-rank-at-least-three missing component cannot
be supported by a star or generic triangle whose selected relations
are all rank two.  The remaining compatibility problem is genuinely
mixed rank one/rank two.

### Corrected Borel proof: the mixed `(2,2,1)` triangle is empty

The earlier proof was correctly withdrawn because its balanced-center
normalization used full row `GL2` while retaining the transformed first rows
as purity kernels.  The missing Borel chart is now closed, so the global
obstruction for this stated rank-three triangle stratum is restored in

```text
P4_MIXED_TWO_RANK_TWO_TRIANGLE_OBSTRUCTION.md
verify_p4_mixed_two_rank_two_triangle_obstruction.py
audit_p4_mixed_two_rank_two_triangle_obstruction.py
```

Gauge the two rank-two edges, which share a vertex, into a
synchronization `V`.  For a generic four-point center the two leaves
lie on the same totally synchronized adjugate pencil.  The
`2+1+1` collision synchronizer is totally synchronized too.  Thus the
leaf-leaf edge already has a rank-two relation, contradicting its
assumed unique rank-one relation.  Zero and `1+3` centers force the
previous embedded-`P3` or pair-rank collapses.

The support-two equal-ratio boundary retains the valid annihilator argument.
Its leaves have rows

```text
y_i=a+beta_i*b_bar,
x_i=b+alpha_i*a_bar.
```

A rank-one leaf-leaf relation must factor through one pure kernel
row.  If `beta_i!=0`, that kernel has support four and zero
degree-one annihilator.  If `beta_i=0`, its annihilator is the line
`C*a_bar`, but the other synchronized leaf plane never contains
`a_bar`.  Both orientations are impossible.

The formerly missing full-support `2+2` center instead has marked center
`(a+b,b)` and synchronized leaves

```text
y_i=a+b-r_i*b_bar-s_i*a_bar,
x_i=b-s_i*a_bar.
```

Put `Delta=r_2s_3-r_3s_2`.  Four maximal minors of the leaf-pair product
matrix are `Delta` times the signed pairs

```text
s_2s_3(r_2+r_3) +/- (s_2+s_3),
r_2r_3(s_2+s_3) +/- (r_2+r_3).
```

If the pair rank is at most three and `Delta!=0`, subtracting the two pairs
forces `s_2+s_3=r_2+r_3=0`, which makes `Delta=0`, a contradiction.  Hence
pair rank at most three forces `Delta=0`.  The leaf commutator is exactly

```text
y_2*x_3-x_2*y_3=Delta*(0,1,-1,-1,1,0).
```

At pair rank three this is the unique relation and has alternating
coefficient matrix of determinant one.  It therefore has rank two, never the
required rank one.  Thus `(2,2,1)` cannot occur on an exceptional rank-three
triangle.  Any remaining mixed triangle has at most one rank-two edge; mixed
stars with one or two rank-two spokes and lower pair-rank strata remain
separate.

### Borel-generic repair of the flat binary cubic

The correct full-kernel-support chart is now closed in

```text
P4_RESONANT_FLAT_GENERIC_BINARY_CUBIC_OBSTRUCTION.md
verify_p4_resonant_flat_generic_binary_cubic.py
audit_p4_resonant_flat_generic_binary_cubic.py
```

Purity fixes each kernel line.  With full kernel support, diagonal
source scaling and Borel row gauge—not full `GL2`—give

```text
y=(1,1,1,1),       x=(0,1,p,q),
pq(p-1)(q-1)(p-q)!=0.
```

The synchronizer is the pencil generated by `A=(y;x)` and

```text
y_sharp=(0,p+q-1,p(1-p+q),q(1+p-q)),
x_sharp=pq(-1,1,1,1).
```

For finite partner parameters `t,u`, let `C=[Y K J X]`.  Put

```text
H=p^2-2pq-2p+q^2-2q+1,

F=p^2q^2 H t^2u^2
  -6p^2q^2(t^2u+tu^2)
  -pq(p+q+1)(t^2+4tu+u^2)
  -2(pq+p+q)(t+u)-3.
```

One compression minor is

```text
-8(p-1)(p-q)(q-1)F,
```

all sixteen `3 x 3` minors of `C` are divisible by `F`, and

```text
det C=-16pq(p-1)(p-q)(q-1)F^2.
```

The compressed span cannot be a line: three `K,J` minors would force
the two parameters `{t,u}` to contain the three distinct values

```text
-1/p,       -1/q,       -1/(pq).
```

Thus purity forces `rank C=3` and `rank C<=2`, a contradiction.
This is the true generic finite-partner theorem.  The remaining projective
sheet is handled next.

### The projective sheet is an additive-parallelogram rank-drop seam

The synchronized pencil has now been compactified without moving the fixed
kernel flag:

```text
P4_RESONANT_FLAT_PROJECTIVE_PARTNER_CLASSIFICATION.md
verify_p4_resonant_flat_projective_partner.py
audit_p4_resonant_flat_projective_partner.py
```

Put one partner at `A_sharp` and the other at `A+u*A_sharp`.  Three
compression minors share

```text
G=pq(p^2-2pq-2p+q^2-2q+1)u^2-6pqu-p-q-1.
```

All full `3 x 3` minors are divisible by `G`.  If the first three cubic
coefficients collapse to the line needed for purity, three smaller minors
leave exactly

```text
q=p+1, u=-1/(2p),
p=q+1, u=-1/(2q),
p+q=1, u=-1/(2pq).
```

For the affine ratios `(0,1,p,q)`, these are the three equations equating
the sums on opposite edges of a perfect matching.  The compactification
therefore sees exactly an additive parallelogram, or weak Sidon failure.

Each curve is a real pure `P4` family: the compressed/full cubic ranks are
`(1,2)`.  But the product image of `(A_sharp,A+u*A_sharp)` has rank exactly
two on all three curves, so none remains in the all-rank-three-relation
triangle.  If both partners are `A_sharp`, two incompatible affine
difference factors exclude purity.  The complete projective partner sheet
is therefore empty in the intended triangle stratum.

The affine-ratio collisions are handled next.

### Full-support collisions are presymplectic rank-drop seams

The legal affine-ratio multiplicities are `1+1+1+1`, `2+1+1`, `2+2`,
`3+1`, and the rank-one `4` collapse.  The three collision types are now
classified in

```text
P4_RESONANT_FLAT_FULL_KERNEL_COLLISION_CLASSIFICATION.md
verify_p4_resonant_flat_full_kernel_collision.py
audit_p4_resonant_flat_full_kernel_collision.py
```

For `2+1+1` and `3+1`, the synchronizer pencil's point at infinity has
local rank one.  Every admissible finite partner has the same active row
`x`; since `x` has support at most two in the squarefree algebra, `x^3=0`.
The required escaping coefficient therefore vanishes.

The `2+2` center has a three-dimensional synchronizer
`span(A,B_0,B_1)`.  Its alternating multiplication form satisfies

```text
omega(A,B_0)=omega(A,B_1)=0,
omega(B_0,B_1)=w!=0.
```

Thus `A` is the radical of a presymplectic projective plane, and compatible
flat triples are exactly lines through `A`.  Writing a direction as
`D=rB_0+sB_1` and the other planes as `A+tD,A+uD`, the four compression
minors factor into `t+u` times signed binary factors and

```text
det C=-64rs(t+u)^2.
```

Purity leaves only `u=-t` with `rt,st in {+1,-1}`.  After rescaling `D`,
these are four signed points.  Their compressed/full ranks are `(1,2)`,
but the product image of `(A+D,A-D)` has rank two at every point.  Both
one- and two-endpoint projective sheets are empty.  Hence no `2+2` pure
point belongs to the all-rank-three triangle.

Together with the finite and projective distinct-ratio theorems, this
excludes the complete full-kernel-support flat triangle.  The
smaller-support analysis follows next.

### The corrected complete triangle has one annihilator-line survivor

The smaller kernel supports have now been classified in

```text
P4_RANK_TWO_RELATION_TRIANGLE_CORRECTED_CLASSIFICATION.md
verify_p4_rank_two_relation_triangle_corrected_classification.py
audit_p4_rank_two_relation_triangle_corrected_classification.py
```

Zero source columns descend to a pure `P3` and force all triangle pair
images to have rank at most two.  With no zero column, kernel support three
either lies in the previous distinct-ratio theorem or has a common active
row of support at most two, so its active cube is zero.  Kernel support one
has a single underlying plane whose square has dimension two.

Kernel support two is the unique survivor.  Put

```text
a=X0+X1,       a_bar=X0-X1,
b=X2+X3,       b_bar=X2-X3.
```

Every pure rank-three triangle with three rank-two relations is, up to the
allowed symmetries,

```text
U0=span(b_bar,a_bar),
Ui=span(a,b+alpha_i*a_bar),       i=1,2,3,
alpha_1+alpha_2+alpha_3 != 0.
```

The leaf products have fixed independent generators `a^2`, `ab`, and a
quadratic with nonzero `b^2` part, so all three pair ranks are exactly
three.  The triple coefficients are

```text
Y=0,
K=a^2*b,
J=a*b^2,
X=(sum alpha_i)b^2*a_bar-(sum_{i<j}alpha_i alpha_j)K.
```

Perfect pairing forces the opposite plane `span(b_bar,a_bar)`.  All sixteen
degree-four coefficients then vanish except

```text
-4(alpha_1+alpha_2+alpha_3)x0*x1*x2*x3.
```

This corrects the withdrawn empty-triangle claim.  The old balanced family
was an exact slice, but not exhaustive under the legal Borel gauge.  The
star is re-audited next; the mixed `(2,2,1)` compatibility remains after it.

### The rank-two-relation star is repaired

The formerly withdrawn star obstruction now has a valid Borel proof:

```text
P4_RANK_TWO_RELATION_STAR_OBSTRUCTION.md
verify_p4_rank_two_relation_star_obstruction.py
audit_p4_rank_two_relation_star_obstruction.py
```

Tree gauge synchronizes all three leaves with the center.  For four
distinct projective columns, the three exact rank-drop pairs in the
adjugate pencil are disjoint.  Three leaves therefore contain a rank-three
pair, and the corrected triangle theorem forces the center kernel onto a
two-coordinate line, contradicting support three or four.

Collision pencils with support-three/full kernels have a common active row
of support at most two, so their required active fourth power is zero.
Kernel support one already drops the center-leaf pair rank.  For support
two, both the distinct and equal finite-ratio charts contain the constant
forbidden coefficient

```text
a^2*b^2=4X0X1X2X3.
```

The missing Borel chart was the full-support `2+2` center
`(y,x)=(a+b,b)`.  Its synchronized leaves have

```text
y_i=c_i(a+b)-r_i*b_bar-s_i*a_bar,
x_i=c_i*b-s_i*a_bar.
```

A center-leaf `3 x 3` minor is `4c_i^3`, so rank three permits `c_i=1`.
Putting `E=s_1s_2+s_1s_3+s_2s_3`, two kernel-marked coefficients are
`-4E` and `-4(E-1)`.  Purity would require `E=0=E-1`, a contradiction.

Thus the rank-two-relation star is genuinely empty.  The old file stays
withdrawn because its proof moved the kernel flag; the replacement theorem
is the authoritative result.  The mixed `(2,2,1)` triangle is the next
Borel compatibility frontier.  The global conjecture remains open.

### A two-rank-two-spoke mixed star is the tenth component

The presymplectic chart left open by the graph obstructions produces a
component rather than another contradiction:

```text
P4_TWO_RANK_TWO_SPOKE_MIXED_STAR_COMPONENT.md
verify_p4_two_rank_two_spoke_mixed_star_component.py
audit_p4_two_rank_two_spoke_mixed_star_component.py
```

With `a,a_bar` and `b,b_bar` the opposite directions on two complementary
binary blocks, take

```text
U0=span(a+b,b),
U1=span(a+b-b_bar-s*a_bar,b-s*a_bar),
U2=span(a+b+b_bar-t*a_bar,b-t*a_bar),
U3=span(b_bar,(s+t-1-st,s+t+1+st,-s-t,-s-t)).
```

The only nonzero restricted coefficient is

```text
T_1111=-4(s+t).
```

The three center pair images have rank three and unique relation-matrix
ranks `(2,2,1)`; the three leaf pair images have rank four.  Thus the
exceptional graph is exactly the previously open two-rank-two-spoke mixed
star, with pair profile `(3,3,3,4,4,4)`.

The active row is governed by `d=(1+st)/(s+t)`.  The Cayley coordinate
`c(z)=(z-1)/(z+1)` turns this into the torus law `c(d)=c(s)c(t)`.  This
identifies the survivor as a toric multiplication graph inside the
presymplectic synchronizer plane.

At `(s,t)=(2,3)`, the diagonal-source family tangent has the exact minor
`-1/2`.  In the universal Segre incidence, a `15 x 15` Jacobian minor is
`345600000`, so the incidence is smooth of dimension five.  The irreducible
family closure is therefore a component.  Its exceptional relation-rank
multiset `{1,2,2}` separates it from all seven earlier fivefolds, and its
dimension separates it from the two sixfolds.  The certified lower bound is
now ten pure-`P4` component orbits.  Its marked `P5` fibres, special toric
boundary, component exhaustiveness, and the global conjecture remain open.

### The `{1,2,2}` rank-three star is completely classified

The component family is now the output of a reverse normal-form theorem, not
only a construction:

```text
P4_TWO_RANK_TWO_SPOKE_MIXED_STAR_CLASSIFICATION.md
verify_p4_two_rank_two_spoke_mixed_star_classification.py
audit_p4_two_rank_two_spoke_mixed_star_classification.py
```

Two rank-two spokes synchronize their leaves with the center.  All ordinary
two-dimensional synchronizer pencils are totally isotropic and would create
an extra leaf relation.  The only dimension-jump centers are full-support
`2+2` and support-two equal ratio.

For the full-support center, the all-kernel coefficient gives
`r_2=-r_1`.  Four remaining purity expressions obey

```text
F2-F3=-(H+Q),
F4-F3=H,
F0-F3=-H*r^2-2H-3Q,
F3=E*(s+t)-H+Q*s*t.
```

Nonzero purity and full leaf-pair rank therefore force, in order,

```text
Q=-H,       r^2=1,       E/H=(1+s*t)/(s+t).
```

After the legal sign, scale, and active-row-shift gauges this is exactly the
tenth-component family.

For the support-two equal-ratio center, the three Borel-distinct rank-one
spoke orientations were checked separately.  The kernel-kernel orientation
makes the active coefficient zero.  The other two force the fourth plane to
`span(a_bar,b_bar)`, whose product image with the center has rank two.  Hence
no second rank-three star family exists in that chart.

The next all-rank-three graph frontier is now a triangle with exactly one
rank-two relation.  Special divisors of the tenth component and lower
pair-image ranks remain separate.

### The tenth component has no generic marked `H31` lift

The complete marking chart of the new component admits a shorter obstruction
than the expected Fitting-divisor analysis:

```text
P5_H31_TWO_RANK_TWO_SPOKE_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md
verify_p5_h31_two_rank_two_spoke_mixed_star_component_generic_obstruction.py
audit_p5_h31_two_rank_two_spoke_mixed_star_component_generic_obstruction.py
```

Keep the first row `alpha_i` of each normal-form plane fixed and write every
compatible active row as `beta_i+h_i alpha_i`.  For each deleted source
coordinate `q`, the fourteen mixed extension coefficients form a `14 x 8`
matrix `M_q(h)` over `C(s,t)[h0,h1,h2,h3]`.  Exact module normal form gives

```text
NF_Mq(A_q)=0,       NF_Mq(B_q)!=0
```

for all four `q`, where `A_q,B_q` are the two diagonal rows.  Hence every
mixed-zero extension kills `A_q` and cannot be a genuine binary neighbour.
This includes every marking divisor; no rank assumption on `M_q` and no
ternary contraction are needed.

There are also explicit polynomial mixed-kernel directions `k_q(h)`.  Their
diagonal values are

```text
A_q(k_q)=0,
(B_0(k_0),B_1(k_1),B_2(k_2),B_3(k_3))
  =(4(s+t),4(s+t),4(s+t),-4(s+t)).
```

Thus the obstruction is best understood as an asymmetric cokernel class, not
as degeneration of the whole extension map.  The primary function-field
module calculation and the independent subset-DP audit pass.  All ten known
pure-`P_4` component orbits are now generically closed for `H31`.  The tenth
component's weighted `H22` fibre, special toric boundary, component
exhaustiveness, and the global conjecture remain open.

### Dense-marking weighted `H22` obstruction on the tenth component

The first weighted continuation is now exact but deliberately partial:

```text
P5_H22_TWO_RANK_TWO_SPOKE_MIXED_STAR_DENSE_MARKING_OBSTRUCTION.md
verify_p5_h22_two_rank_two_spoke_mixed_star_dense_marking_obstruction.py
audit_p5_h22_two_rank_two_spoke_mixed_star_dense_marking_obstruction.py
```

Use Cayley parameters `u=c(s)`, `v=c(t)`, and `rho=c(r)`.  The component law
becomes `d=(1+uv)/(1-uv)`, and clearing the three row denominators makes the
four planes polynomial.  The squarefree top form must still be pulled back to
the original `X_i` coordinates: the permanent is not invariant under the
Hadamard block change to `(a,a_bar,b,b_bar)`.  An initial shortcut that ignored
this was rejected before theorem status; the independent subset-DP audit now
guards the corrected pullback.

At the canonical marking, the first eight mixed rows have two nonzero
factored determinants.  The `D_23` determinant is

```text
4096 rho^3 uv(rho-1)(rho+1)
 (u-1)^2(u+1)^3(u+v)(v-1)^2(v+1)^3(uv-1)^4.
```

The `D_01` determinant is the product of the expected toric coordinate
factors and two additional low-degree factors displayed in the theorem.
Therefore both mixed matrices have rank eight on a dense open of the full
component/slope/marking space, so no binary extension exists there.

At the rational component points `(s,t)=(2,3),(3,5),(5,7)`, exact module
normal form over `C(rho)[h0,h1,h2,h3]` gives the eight standard free-module
generators in both directions.  These are complete all-marking, all-slope
fibres, not evaluations.  They do not prove the generic component's complete
marked fibre empty: possible dominant pieces of the remaining determinantal
divisors still need a symbolic cover.  The global conjecture remains open.

### The first component is a fixed apolar triangle bundle

The remaining generic graph shape contains the original component in a much
simpler normal form:

```text
P4_FIRST_COMPONENT_APOLAR_TRIANGLE_NORMAL_FORM.md
verify_p4_first_component_apolar_triangle_normal_form.py
audit_p4_first_component_apolar_triangle_normal_form.py
```

After preserving the two rank-one zero-product rows, a Borel shift
synchronizes the rank-two edge.  Its equation becomes a factorization of

```text
(X2+X3)(X0+X2).
```

On the dense missing-coordinate branch, the vanishing coefficients force the
second factor to be the signed coordinate reflection of the first.  Equality
of the three nonzero coefficients then makes the coordinates `0,2,3` equal;
the remaining coordinate is normalized by the unused source torus.  The
triangle modes become

```text
U1=span((1,1,1,1),(0,0,1,1)),
U2=span((1,0,1,0),(1,-1,1,1)),
U3=span((0,0,1,-1),(1,0,-1,0)).
```

Only their all-kernel and all-active triple products survive, with covectors
`(-1,-1,-1,1)` and `(1,1,-1,-1)`.  Hence the opposite plane is any two-plane
in the first covector's kernel.  Its dense chart is

```text
U0=span((1,0,p,1+p),(0,1,q,1+q)),
```

and the restriction is

```text
-2(p*e0+q*e1) tensor e1 tensor e1 tensor e1.
```

The generic pair profile is `(4,4,4,3,3,3)`, with triangle relation ranks
`(2,1,1)`.  Setting `e=i=l=1,c=-1-q,j=-p/q` in the old family and applying
`diag(-1,-1,1,1)` gives identical Pluecker vectors.  Thus this is the old
first component, expressed as a `P^2` apolar fibre plus the three-dimensional
source torus.  The other Borel orientations and support collisions of the
same triangle remain to be classified.

### The crossed `(2,1,1)` support problem is an octahedron

The first component normal form left one precise reverse question: could the
same crossed Borel orientation produce another full-support triangle when
the two binary zero-product supports collide differently?  This is now
classified exactly in

```text
P4_CROSSED_211_TRIANGLE_SUPPORT_CLASSIFICATION.md
verify_p4_crossed_211_triangle_support_classification.py
audit_p4_crossed_211_triangle_support_classification.py
```

A genuine zero product is an opposite binary pair
`(Xi+Xj)(Xi-Xj)=0`, labeled by `{i,j}`.  The six labels are the vertices of
the octahedron `J(4,2)=L(K4)`, giving three support orbits.

For equal labels, the rank-two edge factorization has target `X0X1`.
Nonzero active cubic forces one factor outside that binary block; its six
coefficient equations then force both factors to use exactly one common
outside coordinate.  All three triangle planes lie in a coordinate
hyperplane.

For disjoint labels, the target is the complete bipartite quadratic `ab`.
Writing the two factors in binary blocks gives

```text
[u u'] [v' v]^T = a b^T,
det(u,u') det(v',v)=0.
```

The internal zero coefficients force one block projection to vanish.  The
four resulting anchor forms either collapse `U1` or `U2`, or add a second
zero product to edge `13` or `23`, dropping that pair image to rank at most
two.  Thus the disjoint orbit is empty on the stated stratum.

For one-coordinate overlap, normalize the target to
`(X2+X3)(X0+X2)`.  The three coefficients incident with the missing
coordinate force the second factor to be the signed reflection of the first.
Equality of the three nonzero coefficients makes coordinates `0,2,3`
equal.  If the missing-coordinate entries vanish the triangle lies in a
coordinate hyperplane; otherwise the unused source torus gives exactly

```text
U1=span((1,1,1,1),(0,0,1,1)),
U2=span((1,0,1,0),(1,-1,1,1)),
U3=span((0,0,1,-1),(1,0,-1,0)).
```

The symbolic minors `(-2r^2,-2r,r^2)` certify pair ranks three before the
last source scaling.  An independent source-permuted, unequally scaled
subset-DP replay recovers pure support at exactly `0111,1111` and relation
ranks `(2,1,1)`.  No ideal or finite-field search is used.

Conceptually, the same proof is simultaneously a `D4` root-support orbit
calculation, a symmetric rank-two completion problem on `K2`, `K_(2,2)`, or
`K3`, and an apolar `Gr(2,3)` construction.  The remaining triangle frontier
is confined to common-factor/radical Borel orientations, support-one zero
products, and lower pair-image ranks.

### Equal support hides an eleventh, six-dimensional component

The common-factor orientation excluded from the crossed theorem is nonempty.
Put

```text
a=X0+X1,       a_bar=X0-X1,
b=X2+X3,       b_bar=X2-X3,

U0=span(a+p*b,a_bar+q*b),
U1=span(a,a_bar+b),
U2=span(a,r*a_bar+b),
U3=span(b_bar,a_bar).
```

The two rank-one relations are the same exact zero-divisor pair
`a*a_bar=0`; the rank-two relation is `y1*x2-x1*y2=0`.  This is the
homological synchronization law `x2-x1 in Ann(a)=(a_bar)`, leaving the affine
parameter `r`.

All kernel-containing triangle cubics span the single line `C*a^2*b_bar`.
Its degree-one annihilator is `span(a,a_bar,b)`, so `U0` is the dense chart
of an apolar `Gr(2,3)=P^2`.  Exact permanent expansion leaves only

```text
T_0111=-4p(r+1),
T_1111=-4(1+q(r+1)).
```

The generic pair profile is `(4,4,4,3,3,3)` and the triangle relation ranks
are `(2,1,1)`.  Restoring `diag(t0,t1,t2,1)`, the six-parameter family has a
Grassmann-chart tangent minor `3/128` at `(p,q,r)=(1,2,2)`.  On the universal
Segre incidence, a fourteen-by-fourteen Jacobian minor is `-9/2`, and the
family tangent bounds the full rank by fourteen.  Hence the incidence is
smooth of dimension six there and the irreducible family closure is a full
component.

The earlier six-dimensional component has sorted pair profile
`(2,3,3,4,4,4)`; the new one has `(3,3,3,4,4,4)`.  It is also dimensionally
distinct from every fivefold.  The certified lower bound is therefore eleven
component orbits.  An independent `F101` audit, after source permutation and
unequal diagonal scaling, recovers family tangent rank six, incidence rank
fourteen, the pair profile, and the two-point pure support by subset-DP
permanents.  No search is used.

The new component's generic `H31` and weighted `H22` fibres were open at this
checkpoint.  Thus the earlier statement that all ten known components were
generically closed for `H31` was a correct historical checkpoint but was not
yet the current exhaustive known-component status.

### The eleventh component has no generic marked `H31` lift

Use the intrinsic marked rows

```text
alpha0=(1+q(r+1))u-p(r+1)v,  beta0=u,
alpha1=a,                     beta1=a_bar+b,
alpha2=a,                     beta2=r*a_bar+b,
alpha3=b_bar,                 beta3=a_bar,
beta_i(h)=beta_i+h_i*alpha_i.
```

The only pure coefficient is `T_1111=-4p(r+1)`.  For each deleted source
coordinate `d`, form the fourteen-by-eight mixed binary extension matrix
`M_d` and the two diagonal rows `A_d,B_d` over
`C(p,q,r)[h0,h1,h2,h3]`.  Exact polynomial module reduction gives

```text
A_d in Row(M_d),       B_d notin Row(M_d),
module basis sizes = (4,4,8,8).
```

The first inclusion is structural.  `A_0=A_1=0`.  For the other deletions,
the reduced module contains `e0,e1,p*e2,p*e3,p*e4`; since `p` is a unit in
the component function field, these rows synthesize

```text
A2=(-2,-2Q,-2Q,2p,0,0,0,0),
A3=( 2, 2Q, 2Q,2p,0,0,0,0),  Q=1+q(r+1).
```

Hence every solution of the mixed equations has zero all-kernel diagonal,
contradicting the two nonzero binary diagonals required by `H31`.  This holds
simultaneously for every marking parameter, even on mixed-rank divisors.  At
`(p,q,r)=(1,2,2)`, adjoining `A_d` preserves mixed ranks `(4,4,7,7)` while
adjoining `B_d` raises them to `(5,5,8,8)`, so the cokernel asymmetry is
genuine.

An independent subset-DP permanent construction reproduces the complete
all-marking module statement at `(1,2,2)` and `(2,1,3)`.  No search or
ternary-rank test is used.  All eleven certified pure-`P4` components are
now generically closed for `H31`.  The eleventh component's weighted `H22`
fibre, special parameter/projective boundary, component exhaustiveness, and
the global conjecture remain open.

Primary theorem and verifier:

```text
P5_H31_EQUAL_SUPPORT_COMMON_FACTOR_COMPONENT_GENERIC_OBSTRUCTION.md
verify_p5_h31_equal_support_common_factor_component_generic_obstruction.py
audit_p5_h31_equal_support_common_factor_component_generic_obstruction.py
```

### The exact-zero-divisor block kills weighted `H22`

The eleventh component's weighted continuation is simpler than its `H31`
module.  Restore arbitrary diagonal source scalings `t0,t1,t2,t3`, merge
`X0,X1` with homogeneous weights `(lambda,mu)`, and append fifth-coordinate
entries `x_i` to the four kernel rows.  With `R=r+1` and `Q=1+qR`, they become

```text
A0=(*,p*t2,p*t3,x0),
A1=(lambda*t0+mu*t1,0,0,x1),
A2=(lambda*t0+mu*t1,0,0,x2),
A3=(0,t2,-t3,x3).
```

Rows `A1,A2` must occupy the merged and fifth channels in every permanent
matching.  The residual two-channel permanent is

```text
p*t2*(-t3)+p*t3*t2=0.
```

Therefore the all-kernel binary diagonal is identically zero for every
extension, marking, source scaling, and projective merge weight.  One of the
two binary `Delta2` neighbours required by `H22` cannot exist, before any
mixed equation or ternary-rank condition is considered.

This is simultaneously the squarefree exact-zero-divisor identity
`b*b_bar=0`, cancellation of the trivial/sign characters on a two-point
group, and a saturated two-channel tensor-network cut.  A separate subset-DP
permanent audit, with independent row scalings and a within-block source
swap, reproduces the zero polynomial.

The eleventh component is now generically closed for both `H31` and weighted
`H22`.  Ten of the eleven certified components are generically closed for
weighted `H22`; the tenth component's marking divisors are the sole remaining
generic known-component weighted frontier.  Special pure-factor degenerations,
projective boundaries, component exhaustiveness, and the global conjecture
remain open.

Primary theorem and verifiers:

```text
P5_H22_EQUAL_SUPPORT_COMMON_FACTOR_COMPONENT_GENERIC_OBSTRUCTION.md
verify_p5_h22_equal_support_common_factor_component_generic_obstruction.py
audit_p5_h22_equal_support_common_factor_component_generic_obstruction.py
```

### A fixed-vertex Segre join closes the last generic known-component fibre

The tenth component's weighted marking divisors become small after forgetting
the marking coordinates.  In canonical `(alpha,beta)` bases, write `C_w(z)`
for the sixteen weighted `23` binary coefficients, linear in the eight
extension entries.  If a Borel shift

```text
beta_i'=beta_i+h_i*alpha_i
```

diagonalizes the tensor with nonzero all-kernel coefficient `A`, then

```text
C_w=A*product_(i:w_i=1)(-h_i),   w!=1111.
```

Thus, after normalizing `C_0000=1`, the fifteen coordinates other than the
free all-active `C_1111` form a rank-one Boolean array.  Eliminating the four
`h_i` gives exactly

```text
C_S*C_empty^(|S|-1)=product_(i in S) C_{i},
2 <= |S| <= 3,
```

namely six quadratic and four cubic toric binomials.

For the Cayley component, put

```text
K=x3+rho*(1-u*v)*y0,
L=-2*(u+1)*(v+1),
M=-4*(u+v).
```

Four coefficients are

```text
C_1000=M*K,
C_1010=C_1100=C_1110=L*K.
```

On `K!=0`, the `{0,1}`, `{0,2}`, and `{0,1,2}` binomials force `L=M`, but
`M-L=2*(u-1)*(v-1)` is a unit in `C(u,v,rho)`.  Substituting all eight
extension variables into the full natural toric system closes `K=0` too:

```text
<C_0000-1, six quadrics, four cubics>=(1)
```

over `C(u,v,rho)`.  Hence the weighted `23` neighbour cannot be binary
`Delta2` in any marking; no ternary-rank test is reached.  An independent
audit uses the original `(s,t)` component rows and subset-DP permanents, and
gets reduced basis `{1}` over `C(rho)` at `(2,3)` and `(3,5)`.

All eleven certified pure-`P4` components are now generically closed for both
`H31` and weighted `H22`.  The live front moves to component exhaustiveness
and special parameter/projective boundaries.  This remains a finite
component theorem, not a global graph proof.

Primary theorem and verifiers:

```text
P5_H22_TWO_RANK_TWO_SPOKE_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md
verify_p5_h22_two_rank_two_spoke_mixed_star_component_generic_obstruction.py
audit_p5_h22_two_rank_two_spoke_mixed_star_component_generic_obstruction.py
```

### Transverse binary polarity detects a twelfth component

The common-active support-two `(2,1,1)` orientation has a complete local
annihilator reduction.  Normalize an exact pair `a*c=0`, so the two leaf
kernel rows are both `a`, the common active row is `c`, and the rank-two edge
synchronizes the other leaf rows as `m,m+r*c`.  Split their complementary
binary parts as

```text
s=u*X2+v*X3,       t=p*X2+q*X3,
A=u*q+v*p,         Q=u*q-v*p.
```

The four maximal minors of the three kernel-rich cubics factor as

```text
 4*q*A*(E+2*delta*u*v),
 4*p*A*(E+2*delta*u*v),
-4*(gamma-delta)*Q*(E-2*gamma*u*v),
 4*(gamma+delta)*Q*(E+2*gamma*u*v),
E=(2*beta+r)*A.
```

Thus `A=0` is the graph of the split exact-zero-divisor polarity, `Q=0` is
the diagonal in `P1 x P1`, and the transverse sheet forces
`gamma^2=delta^2`, i.e. a single-coordinate `1+3` projection.  The first two
sheets return to the eleventh component or its `q=0` boundary.

One transverse sheet is

```text
a=(1,1,0,0), c=(1,-1,0,0), b=(0,0,1,1),
m=b+c, m_r=b+(1+r)c,
d=(0,(r+2)(k+1),1,k),
n=(-(k-1)(r+2),0,-1,k),
U0=span(n,c), U1=span(a,m), U2=span(a,m_r), U3=span(d,c).
```

Its restriction is identically `-4*x0*x1*x2*x3`.  At
`(r,k)=(-4/3,2)`, the pair profile is `(3,3,4,3,3,3)` with four rank-one
relations and one rank-two relation.  Every three-mode kernel-rich cubic
span has rank two.  Restoring the source torus gives a rank-five family
tangent with minor `2`; the universal Segre-incidence Jacobian has rank
fourteen with minor `-131072`.  Fourteen selected equations define a regular
six-dimensional local ring, but along its excess implicit direction the
omitted `1001` equation begins with `12h^2`.  It is therefore nonzero in that
ring, so the full incidence has local dimension at most five.  The family
gives the matching lower bound and its irreducible closure is a component.
Its sorted pair profile `(3,3,3,3,3,4)` differs from every earlier fivefold;
dimension separates the three earlier sixfolds.  The certified component
lower bound is twelve.

The apparent sixth tangent direction is quadratically obstructed.  The
displayed family is a dense normal form for the new component.  Its generic
`H31/H22` fibres, component exhaustiveness, and the
global conjecture remain open.  The eleven-component generic-closure theorem
is retained as a historical checkpoint, not a claim about the newly found
twelfth component.

Primary theorem and verifiers:

```text
P4_TRANSVERSE_COMMON_FACTOR_COMPONENT.md
P4_TRANSVERSE_COMMON_FACTOR_COMPONENT_GRAPH.svg
verify_p4_transverse_common_factor_component.py
audit_p4_transverse_common_factor_component.py
```

### The twelfth component has no generic marked `H31` fibre

Use the intrinsic marking

```text
alpha=(n,a,a,d),       beta=(c,m,m_r,c),
beta_i(h)=beta_i+h_i*alpha_i
```

over `C(r,k)[h0,h1,h2,h3]`.  For each deleted coordinate `j`, let `M_j`
be the fourteen-row mixed extension matrix and `A_j,B_j` its all-kernel and
all-active diagonal rows.  Exact polynomial module reduction gives

```text
A_j in Row(M_j),       B_j notin Row(M_j),
module sizes (7,7,8,8).
```

The first two all-kernel rows vanish identically.  The other two are

```text
A_2=2k(1,r+2,r+2,1,0,0,0,0),
A_3=2(1,-k(r+2),-k(r+2),-1,0,0,0,0),
```

and the reduced modules contain the required standard-basis rows.  At
`(r,k)=(1,2)`, mixed ranks `(6,6,7,7)` are unchanged by adjoining `A_j`
and rise to `(7,7,8,8)` after adjoining `B_j`.  An independent subset-DP
audit reproduces all four all-marking modules at `(1,2)` and `(2,3)`.

Thus every mixed-zero extension kills one required binary diagonal before
any ternary-rank test.  All twelve certified components are generically
closed for `H31`; the twelfth component's weighted `H22` fibre, special
boundaries, component exhaustiveness, and the global conjecture remain open.

Primary theorem and verifiers:

```text
P5_H31_TRANSVERSE_COMMON_FACTOR_COMPONENT_GENERIC_OBSTRUCTION.md
verify_p5_h31_transverse_common_factor_component_generic_obstruction.py
audit_p5_h31_transverse_common_factor_component_generic_obstruction.py
```

### Binary polarity kills the twelfth component's weighted `H22` fibre

For the weighted `01` neighbor, restore arbitrary source scalings and
homogeneous merge weights.  The repeated kernel rows `a,a` are supported only
on the merged and fifth channels.  Every perfect matching assigns them to
those channels, leaving the kernel rows `n,d` on `X2,X3`:

```text
n -> (-t2,k*t3),       d -> (t2,k*t3).
```

Their residual permanent is

```text
(-t2)*(k*t3)+(k*t3)*t2=0,
```

the exact-zero-divisor identity `(-X2+kX3)(X2+kX3)=0`.  Hence the
all-kernel diagonal vanishes for every extension, marking, slope, and source
scaling before any mixed equation is imposed.  An independent subset-DP
audit with arbitrary kernel-row scalings and a within-block source swap
reproduces the zero polynomial.

All twelve certified pure-`P4` components are now generically closed for
both `H31` and weighted `H22`.  Special parameter/projective boundaries,
component exhaustiveness, and the global conjecture remain open.

Primary theorem and verifiers:

```text
P5_H22_TRANSVERSE_COMMON_FACTOR_COMPONENT_GENERIC_OBSTRUCTION.md
verify_p5_h22_transverse_common_factor_component_generic_obstruction.py
audit_p5_h22_transverse_common_factor_component_generic_obstruction.py
```

### The dense common-kernel `YY` triangle is empty

For the common-kernel Borel orientation of a `(2,1,1)` relation triangle,
normalize the exact pair to

```text
a=X0+X1,       c=X0-X1,       a*c=0.
```

In the kernel/kernel leaf chart the rank-two edge synchronizes the rows as

```text
y1=y2=a,       y3=c,
x1=m=beta*c+s, x2=m+r*c,
x3=d=gamma*a+delta*c+t,
s=uX2+vX3,     t=pX2+qX3.
```

The seven kernel-containing triple products have the same span as

```text
C0=a^2*d,       C1=a*m*d,       C2=m*(m+r*c)*c.
```

Set `A=u*q+v*p`, `Q=u*q-v*p`, and `E=(2*beta+r)*A`.  Their four maximal
minors factor exactly as

```text
8q*u*v*A,
8p*u*v*A,
4Q*(E-2gamma*u*v),
4Q*(E+2gamma*u*v).
```

On `u*v*p*q!=0`, rank at most two forces `A=0`; then `Q!=0` and the last
two factors force `gamma=0`.  Thus `s*t=0`, `d=delta*c+t`, and the all-active
cubic obeys

```text
m*(m+r*c)*d=delta*C2-beta*(beta+r)*C0.
```

Any opposite plane annihilating the kernel-rich cubics therefore annihilates
the required pure cubic.  This is an exact global contradiction on the dense
chart, not a sampled calculation.  In binary invariant-theory language
`A=0` is a quadratic polarity graph; in commutative algebra it is an exact
zero-divisor pair; in apolar geometry the active class has fallen into the
mixed span.  The mixed `YX`, active `XX`, support-one, and lower-pair-rank
strata remain.

Primary theorem and verifiers:

```text
P4_COMMON_KERNEL_YY_211_TRIANGLE_OBSTRUCTION.md
verify_p4_common_kernel_yy_211_triangle_obstruction.py
audit_p4_common_kernel_yy_211_triangle_obstruction.py
```

### The mixed common-kernel leaf always has a second relation

For the `YX` leaf orientation, the common exact pair gives

```text
y1=x2=a=X0+X1,       y3=c=X0-X1,
x1=b,                 y2=d,
b*d=a^2.
```

Write the binary coefficients of `b,d` as `(b0,b1)` and `(d0,d1)`, and
their complementary parts as `(s2,s3)` and `(t2,t3)`.  With
`Delta=b0*d1-b1*d0`, the four cross coefficients of `b*d=a^2` imply

```text
Delta*s_j=Delta*t_j=0,       j=2,3.
```

If `Delta!=0`, both complementary parts vanish and the pair-product image is
the line `C*X0*X1`.  If `Delta=0`, the nonzero `01` coefficient gives

```text
b=B+s,       d=lambda*(B-s),
lambda*b0*b1=1,       s^2=0.
```

Thus `s` lies on a coordinate ray, but this boundary still cannot produce a
rank-three pair: all four products lie in `span(a^2,a*s)`.  Besides the
given relation `b*d=a^2`, one has

```text
lambda^(-1)*a*d+a*b-(b0+b1)*a^2=0.
```

Hence the common-kernel `YX` orientation is empty throughout the genuine
support-two exact-pair stratum.  The active `XX` orientation is the remaining
dense common-kernel case.

Primary theorem and verifiers:

```text
P4_COMMON_KERNEL_YX_211_FACTORISATION_OBSTRUCTION.md
verify_p4_common_kernel_yx_211_factorisation_obstruction.py
audit_p4_common_kernel_yx_211_factorisation_obstruction.py
```

### An Eisenstein norm quadric gives a thirteenth component

The remaining `XX` common-kernel orientation has rows

```text
a=X0+X1, c=X0-X1, b=X2+X3, b_bar=X2-X3,
m=alpha*a+beta*c+b,
m_r=m+r*c,
d=gamma*a+b,
x0=b-(alpha+gamma)*a-(2*beta+r)*c,

U0=span(b_bar,x0),
U1=span(m,a),
U2=span(m_r,a),
U3=span(c,d).
```

The common-kernel triangle relations are

```text
y1*x2-x1*y2=0,       x1*y3=0,       x2*y3=0.
```

All kernel-rich cubics reduce to `C0=m*m_r*c`, `C1=m*m_r*d`, and
`C2=a*m*d`, with the exact compression

```text
C1=(2*beta+r)*C0+(2*alpha+gamma)*C2-2F*(0,0,1,1),
F=alpha^2+alpha*gamma+gamma^2-3*beta^2-3*beta*r-r^2.
```

The full restriction has only

```text
T_1001=-4F,       T_1111=4.
```

Hence `F=0` is a pure family.  Writing `N(x,y)=x^2+xy+y^2`, its equation is

```text
N(alpha,gamma)=N(r+beta,beta).
```

Over `C`, Eisenstein factorization turns this into `UV=ST`; the projective
parameter surface is the Segre quadric `P1 x P1`.  The affine radial
direction duplicates a block source scaling, leaving two quadric directions
plus the three-dimensional diagonal source torus.

At `(alpha,beta,r,gamma)=(2,1,1,1)`, the generic pair profile is
`(4,4,4,3,3,3)` and relation ranks are `(2,1,1)`.  A family tangent minor is
`1/864`; the universal Segre-incidence Jacobian has rank fifteen with minor
`-2/81`.  The family is therefore a smooth five-dimensional irreducible
component.  An independent mod-101 Pluecker-dual audit with source order
`(2,0,3,1)` and scales `(2,3,5,7)` obtains ranks `5/15` and incidence minor
`86`.

The coincident support-octahedron labels distinguish this from the first
apolar triangle; dimension and reversed kernel/active incidence distinguish
it from the eleventh equal-support sixfold.  The certified lower bound is now
thirteen components.  Generic `H31/H22` fibres for this new component are
open, so the earlier twelve-component closure statement is historical.

Primary theorem, graph, and verifiers:

```text
P4_EISENSTEIN_NORM_COMMON_KERNEL_COMPONENT.md
P4_EISENSTEIN_NORM_COMMON_KERNEL_COMPONENT_GRAPH.svg
verify_p4_eisenstein_norm_common_kernel_component.py
audit_p4_eisenstein_norm_common_kernel_component.py
```

### The Eisenstein component has no generic marked `H31` fibre

Use the intrinsic marking

```text
alpha_rows=(b_bar,m,m_r,c),
beta_rows=(x0,a,a,d),
beta_i(h)=beta_i+h_i*alpha_i.
```

To avoid an algebraic coefficient field, set `beta=1` on the norm quadric
and project from `(alpha,beta,r,gamma)=(2,1,1,1)`.  For line direction
`(u,v,1)`, put

```text
D=u^2+u*v+v^2-1,
lambda=(5-5u-4v)/D,
alpha=2+u*lambda,
r=1+lambda,
gamma=1+v*lambda.
```

This makes the norm equation identically zero and gives the dominant
component function field `C(u,v)`.  Over the full marking ring
`C(u,v)[h0,h1,h2,h3]`, exact row-module reduction gives, for all four source
deletions,

```text
A_j in Row(M_j),       B_j notin Row(M_j),
module sizes (10,10,10,10).
```

At `(u,v)=(2,0)`, the mixed ranks and ranks after adjoining `A_j` are all
seven; adjoining `B_j` raises all four to eight.  An independent subset-DP
constructor verifies every marking module at the norm-quadric points
`(-4/3,1,-2/3,1)` and `(2,1,-4,1)`.

Thus every mixed-zero extension kills the all-kernel binary diagonal before
any ternary rank test.  All thirteen certified components are generically
closed for `H31`; the new component's weighted `H22` fibre remains open.

Primary theorem and verifiers:

```text
P5_H31_EISENSTEIN_NORM_COMPONENT_GENERIC_OBSTRUCTION.md
verify_p5_h31_eisenstein_norm_component_generic_obstruction.py
audit_p5_h31_eisenstein_norm_component_generic_obstruction.py
```

### A diagonal-product ideal closes the weighted Eisenstein fibre

For the weighted `01` projection, retain the rational component field
`C(u,v)` and intrinsic marked rows.  With finite slope `rho`, marking
variables `h0,...,h3`, and eight extension entries `z`, let `I_mix` be the
ideal generated by the fourteen mixed binary coefficients.  Let `A,B` be
the all-kernel and all-active diagonal coefficients.

Treating every slope, marking, and extension coordinate as a polynomial
variable, exact reduction gives

```text
A*B in I_mix,
finite-chart reduced basis size 48.
```

Thus the mixed extension scheme lies in `V(A) union V(B)`; one required
binary diagonal always vanishes.  This product statement survives the
slope-torsion divisor where a fixed row-module membership does not.  On the
homogeneous infinite-slope chart the same product membership holds, with
reduced basis size `10`.

At `(u,v,rho)=(2,0,2)` the mixed rank is seven, remains seven after adjoining
`A`, and rises to eight after adjoining `B`.  Independent subset-DP ideal
constructors at `(-4/3,1,-2/3,1)` and `(2,1,-4,1)` reproduce the finite and
infinite product certificates.

The thirteenth component is therefore generically closed for weighted
`H22`; all thirteen certified components are now generically closed for both
marked types.  Special component divisors and component exhaustiveness
remain open.

Primary theorem and verifiers:

```text
P5_H22_EISENSTEIN_NORM_COMPONENT_GENERIC_OBSTRUCTION.md
verify_p5_h22_eisenstein_norm_component_generic_obstruction.py
audit_p5_h22_eisenstein_norm_component_generic_obstruction.py
```

### Any support-one triangle is lower-rank or embedded `P3`

For a coordinate zero divisor `e=Xi`, `Ann_R1(e)=C*e`.  If two rank-one
edges share a common-mode factor and both are support-one, all three factors
are `e`.  In `YY` and `XX`, the synchronization makes the two leaf planes
coincide and their product image lies in `span(e*x,x^2)`.  In `YX`, the four
products lie in `span(e*y,x*e)`.  Every common-factor orientation has pair
rank at most two.

For the crossed orientation, equal singleton supports collapse the common
plane.  Distinct supports normalize to

```text
x1=y3=X0,       y2=x3=X1,       p*q=X0*X1.
```

With `Delta=p0*q1-p1*q0`, the off-edge coefficients imply
`Delta*s_k=Delta*t_k=0`.  The nonrigid branch has

```text
p=P+s,
q=lambda*(P-s),
2*lambda*p0*p1=1,
s^2=0.
```

Thus `s` uses at most one of `X2,X3`.  The rank-three survivor puts all three
triangle planes in a coordinate three-space `H`.  Since
`R=R_H tensor C[X_missing]/(X_missing^2)`, all sixteen four-mode coefficients
factor as the missing-coordinate functional on `U0` times the restricted
ternary tensor.  A nonzero pure survivor is therefore in the embedded-`P3`
component.

The same conclusion holds when only one rank-one edge is support-one.  A
genuine mixed support-one/support-two pair cannot have a common factor, so
only the crossed orientation remains.  If the two supports overlap, its
synchronization is again a factorization of one edge monomial.  If they are
disjoint, normalize it to

```text
y1*x2=X0*(X1-X2).
```

Vanishing of the three edges incident with `X3` shows that a factorization
using `X3` in both factors would have `q_i=-k*p_i` for `i<3`.  Its internal
edge coefficients would then satisfy

```text
E01*E02+2*k*p0^2*E12=0,
```

whereas the target has `(E01,E02,E12)=(1,-1,0)`.  If exactly one factor used
`X3`, the other would be supported only there, which is equally impossible.
Thus both factors lie in `span(X0,X1,X2)`, and the same Frobenius--Kunneth
argument identifies every pure survivor with the embedded-`P3` component.
The support-one boundary is complete; genuinely lower pair-image ranks are
the remaining triangle frontier.

### Pair-image rank one is impossible for nonzero pure `P4`

Suppose two row planes `U,V` have one-dimensional product image.  Writing
`uv=B(u,v)Q`, the annihilator bound `dim Ann_R1(u)<=1` makes `B`
nondegenerate.  Its null pairs therefore form the graph of a projective
isomorphism `P(U)->P(V)`.

The full projectivized zero-product incidence in the squarefree algebra is
the union of six curves

```text
C_pq={([aX_p+bX_q],[aX_p-bX_q]):[a:b] in P1}.
```

The graph is irreducible, so it lies in one `C_pq`; both row planes are the
coordinate plane `span(X_p,X_q)`.  Their product coefficient is the binary
form `ad+bc`, whose matrix has determinant `-1`.  Frobenius pairing with any
nonzero opposite product leaves this rank-two binary slice, whereas every
slice of a nonzero decomposable four-tensor has rank one.  Thus every pair
image in a nonzero pure `P4` restriction has rank at least two.

This removes the rank-zero/rank-one strata without a chart computation.  The
single-pair secant/tangent theorem now covers the exact lower boundary; the
remaining issue is compatibility and purity for its rank-two kernels.

```text
P4_RANK_ONE_PAIR_OBSTRUCTION.md
verify_p4_rank_one_pair_obstruction.py
audit_p4_rank_one_pair_obstruction.py
```

Primary theorem and verifiers:

```text
P4_SUPPORT_ONE_211_TRIANGLE_REDUCTION.md
verify_p4_support_one_211_triangle_reduction.py
audit_p4_support_one_211_triangle_reduction.py
```
