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

The primary checker reconstructs the three determinant signs and the
rank-two factorisations symbolically over `C`.  An independent audit
checks all `3^12 = 531,441` pairs of `3 x 2` matrices over `F_3`;
4,161 have zero outer difference and none has both column-pair ranks
equal to two.  The dependency certificate for the four-blocker theorem
was also rerun successfully.

```text
UNIVERSAL_FIVE_BLOCKER_DIVISIBILITY_LEMMA.md
  1ed09eb7b208520e8e62a9c6db7e26629fcb8ed4ac8bbb04fe2a852c59d0dd5d
verify_universal_five_blocker_divisibility.py
  671d98c0d1d93ed4147072594c936620151214d36673e3b0cc141a92c39f511b
audit_universal_five_blocker_divisibility.py
  01565c88d0635ee61dd92ea87d43b4022fcc663d1cf733a56b2a69ad362349f6
tmp/universal_five_blocker_divisibility_verified.json
  2fdedba74d9bef6688f7e6bbd46d4f619ca2c912d29b3607137679eccb90d016
tmp/universal_five_blocker_divisibility_audited.json
  784000bb66cddb2617842808bd3868d04ddf72daa45034ee95394c26d0caa562
```

This is not yet a global contradiction.  The remaining arbitrary-order
target is to propagate the forced one-sided compressions through
adjacent rank-three edges, or to combine them with the existing
root-set blocker surplus.

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
