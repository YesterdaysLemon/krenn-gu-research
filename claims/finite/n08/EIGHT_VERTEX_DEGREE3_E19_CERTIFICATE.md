# Eight-vertex degree-three exact-19-edge exclusion

## Claim

There is no eight-vertex, three-colour complex Krenn-Gu witness whose
essential skeleton has exactly 19 nonzero blocks and a degree-three vertex.

This is a finite theorem.  It does not exclude denser eight-vertex
skeletons, degree-four-or-higher exact-19 skeletons, or arbitrary even
order, and therefore does not solve the full prize conjecture.

An essential skeleton contains exactly the nonzero blocks that lie in at
least one perfect matching.  It is connected and matching-covered.  The
generic killer theorem gives minimum degree at least three.  At a
degree-three vertex the singleton-star theorem forces, after relabelling,

```text
W_01 = alpha_0 e_0 outer(e_0)
W_02 = alpha_1 e_1 outer(e_1)
W_03 = alpha_2 e_2 outer(e_2)
```

with all three scalars nonzero.  It also forces three overlapping pure
six-vertex minors, which yield the restricted killer and diagonal-anchor
constraints used below.

## Complete skeleton catalogue

The pinned source catalogue is:

```text
tmp/n8_mindeg3_e12_28.g6
SHA-256 24f5ab1f8fbc7f03c9648f7217da54a544acd4223a70931b43d57c6b0ac4c0c7
```

Independent decoding, exact-19 filtering, matching-covered filtering,
degree-three star selection, and stabilizer canonicalization give:

```text
unlabeled connected matching-covered skeletons   198
canonical degree-three star roles                 235
```

The residual stabilizer is regenerated during audit, and all role indices
from 0 through 234 are required.  No partial catalogue is accepted.

## Necessary support relaxation

The base CNF uses only necessary consequences of an exact witness:

1. every selected skeleton block is nonzero;
2. every monochromatic amplitude has a nonzero matching monomial;
3. no forbidden amplitude has exactly one nonzero matching monomial;
4. every vertex-colour task has a distinct generic killer and a diagonal
   anchor;
5. the degree-three centre is the normalized monochromatic singleton star;
6. each of its three pure six-vertex minors has its own restricted killer
   and anchor at every remaining vertex;
7. the exact local killer-flag constraints hold.

The initial support CNF is:

```text
tmp/eight_vertex_local_degree3_flag_max19.cnf
variables       326,990
clauses       2,408,339
SHA-256 a2218c5f4b0cc29069ef22766a48b7b13abb90fa82f7a6ccaf775ea8fb44ccfe
```

SAT in this relaxation would not establish a complex witness.  The audited
UNSAT certificate below soundly excludes every exact witness in scope.

## Exact algebraic conflict chain

For a support survivor, the checker restricts all characteristic-zero
amplitude equations to the selected nonzero entries.  It then records
either an exact integer-lattice derivation of a Laurent unit or an exact
rational linear-monomial relation.  Only the support entries used by the
derivation enter the learned cube, and every stabilizer image is checked.

The theorem-level checkpoint contributes:

```text
exact conflicts                    112
distinct learned clauses        15,912
checkpoint SHA-256
  8bf094ae6651df95a4fddd84a00cc470f71671ab036c35b6b135f13039ef46d8
```

The clean complete-catalogue pass contributes:

```text
support models/conflicts            252
Laurent-unit conflicts               236
linear-monomial relations             16
learned clauses                   35,496
processed/UNSAT roles             235/235
Singular fallbacks                      0
```

Thus the chained certificate contains 364 exact algebraic conflicts and
51,408 learned clauses.  Its final learned CNF is:

```text
tmp/degree3_e19_clean_linear_laurent.cnf
variables       326,990
clauses       2,459,747
SHA-256 58789994a3c73498fab97a72336eb6c7817546a9ee3c190251cf3cc766b920f1
```

`verify_laurent_batch_manifest.py` replays every exact derivation and its
support cube.  `verify_skeleton_laurent_batch.py` regenerates all 235 roles
and requires complete no-fallback coverage.

## Elementary cancellation subcertificates

Twelve of the 252 fresh conflicts have a shorter value-free proof.  Two
forbidden colourings differ at one vertex; the common active matchings all
use the same incident edge and therefore scale by one common nonzero ratio,
while one colouring has exactly one extra nonzero matching monomial.
Cancellation transports across the shared set and leaves that extra
monomial equal to zero, a contradiction.

`verify_cancellation_transport_manifest.py` independently reconstructs both
active matching sets and checks the nonzero ratio entries.  The certified
conflict indices are:

```text
1, 3, 4, 5, 77, 84, 142, 156, 202, 228, 229, 230
```

These 12 elementary proofs are a strict subset of the 364-conflict algebraic
certificate.

Thirty-five further fresh conflicts have a two-monomial rectangle proof.
The same two nonzero matching monomials survive at three or four colourings
obtained by independently changing two vertices.  Because neither matching
pairs those vertices together, their partial amplitudes form a sum of two
full-support rank-one `2 x 2` matrices.  Vanishing at three corners forces
their partial sum to vanish at the fourth.  That either contradicts a
required monochromatic value or isolates one additional nonzero monomial in
a forbidden amplitude.  The independently certified indices are:

```text
0, 2, 9, 14, 15, 17, 18, 34, 68, 72, 73, 74, 91, 106, 111, 114,
115, 127, 129, 130, 132, 133, 134, 135, 147, 161, 162, 165, 166,
234, 235, 236, 237, 239, 241
```

`verify_matching_rectangle_manifest.py` reconstructs all four active
matching sets, checks the rank-one separation condition, and pins these
indices.  The two elementary classes are disjoint, so 47 of the 252 fresh
conflicts now have characteristic-free subproofs.  This is not a claim that
the remaining 205 fresh conflicts, or the 112 checkpoint conflicts, are
combinatorial; their exact algebraic certificates remain authoritative.

## Portable selector certificate

One selector per canonical role, one selector disjunction, and 5,640
selector-to-block implications compile the complete case split into:

```text
tmp/degree3_e19_clean_linear_selector.cnf
variables       327,225
clauses       2,465,388
SHA-256 5954ac1b35dc3dd5e60fad2cde9a2d37a8b4cb41e78064d54a68c71aca551a3e
```

`verify_catalogue_selector.py` independently regenerates the roles and
checks the base prefix, selector disjunction, and every implication.

## Independent decisions and proof checking

Kissat returned `s UNSATISFIABLE` independently.  CaDiCaL 1.9.5 also
returned `s UNSATISFIABLE` and produced:

```text
tmp/degree3_e19_clean_linear_selector_cadical195.drat
bytes   186,169,429
SHA-256 bb31b580436f12b922d8b4ff0bb74dc5d1704361c4e94e5a653efc7b3831b934
```

Independent `drat-trim` backward checking reports:

```text
224,826 of 2,465,388 input clauses in the core
428,409 of 1,706,963 lemmas in the core
64,029,123 resolution steps
0 RAT lemmas
s VERIFIED
```

## Fail-closed audit

Run:

```text
python claims/finite/n08/verify_eight_vertex_degree3_e19.py
```

The verifier replays both algebraic-conflict stages, reconstructs the
complete catalogue, checks all 12 transport and 35 rectangle
subcertificates, audits the selector CNF, pins every artifact by SHA-256,
and requires the independent solver and proof-checker terminal lines.  Its
authoritative output is:

```text
tmp/eight_vertex_degree3_e19_final_audit.json
```

with `"verified": true`.
