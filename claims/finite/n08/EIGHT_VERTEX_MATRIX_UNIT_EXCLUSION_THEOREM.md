# Eight-vertex exclusion of the maximum-root-one branch

**Proved exact computer-assisted exclusion over C, independently reviewed
on 2026-09-04.**
The global Krenn--Gu conjecture remains **UNRESOLVED**. No Lean
formalization or arbitrary-order exclusion is claimed.

## Exact statement and upstream reduction

There is no ternary complex block graph on eight vertices with full
matching tensor Delta_(8,3) whose maximum fully supported pairwise-zero
torus-root cardinality is one.

Equivalently, a complete graph with one nonzero matrix unit on every
physical pair cannot realize Delta_(8,3), for any assignment of nonzero
complex edge weights. Endpoint colours may differ. No positivity, phase
restriction, genericity, or weight normalization is imposed.

The [maximum-root theorem, Section 3](../../arbitrary-order/MAXIMAL_TORUS_ROOT_SATURATION_AND_COORDINATE_ABSORPTION_THEOREM.md#3-the-maximum-one-monomial-branch)
supplies the equivalence. If a physical edge had a product-torus zero,
its endpoints would give a root pair. A bilinear form zero-free on the
product torus is a Laurent-ring unit, hence a nonzero scalar matrix
monomial. Conversely every nonzero matrix unit is zero-free on that torus.
Thus all 28 blocks are present and have exactly one nonzero entry.

Write the unit on edge e={u,v}, u<v, as lambda_e E_(a_e,b_e), with
lambda_e in C*. Every perfect matching M has exactly one compatible
colour word w(M) and contributes the nonzero monomial

```text
m_M = product_(e in M) lambda_e.
```

All 105 physical perfect matchings are retained throughout the proof.

## 1. A complete finite scaffold cover

Each of the three pure amplitudes is nonzero, so choose one nonzero
monochromatic perfect matching M_c for each colour c. The three matchings
are physically edge-disjoint: one matrix unit cannot have two different
diagonal colours. Their union is a spanning cubic graph with twelve
labelled edges. It may be disconnected.

This union is only a selected scaffold. The other sixteen physical blocks
remain nonzero matrix units and participate in every relevant coefficient.
No essential-skeleton edge bound is inferred by discarding them.

A vertex permutation sends M_0 to 01|23|45|67 and preserves Delta_(8,3).
The recursive least-unpaired-vertex construction gives all
7*5*3*1=105 perfect matchings, without duplication. Sixty are disjoint
from M_0. For each such M_1, enumerate every M_2 disjoint from both:

```text
M_0 union M_1 type       number of M_1       allowed M_2 per M_1
C8                             48                      31
C4 + C4                        12                      33
ordered (M_1,M_2) total                                1,884
```

The stabilizer of M_0 consists exactly of permutations of the four pairs and
independent flips inside each pair, of order 4!*2^4=384. Its orbits on the
1,884 ordered pairs give eighteen representatives, with orbit-size counts

```text
size 12: 1 orbit; size 48: 7; size 96: 6; size 192: 3; size 384: 1.
```

These sizes sum to 1,884. No colour permutation, connectedness condition,
or unproved graph catalogue is used. The independent semantic checker
reconstructs the entire raw set and group action and verifies that the
eighteen recorded orbits cover exactly that set. The representative data
are in [certificate.json](r1-source-certificate/certificate.json).

## 2. Necessary matching-word clauses

For each scaffold, each unknown half-edge has exactly one of three
colours. Its two endpoint choices specify one of the nine possible matrix
units on that physical pair. The twelve scaffold labels are fixed; all
other labels remain free.

Introduce a pure witness for a matching and colour only if its fixed
positions permit that pure word. It implies all remaining endpoint
colours equal that colour. Introduce an equality witness for two matchings
only if their fixed positions permit equality; it implies equality at
every endpoint. Every matching requires a pure witness or an equality
witness with another matching.

These clauses express exactly that no mixed word has a singleton matching
fibre. A genuine source must satisfy them: a singleton coefficient is a
nonzero monomial and cannot cancel. Conversely a label table with no mixed
singleton can set truthful witness variables. Reverse implications for
these existence witnesses are unnecessary.

This is a necessary support relaxation, not equivalence to cancelling
complex weights. Ten first returned label tables survived it. Their
subsequent exclusion never substitutes those ten examples for a complete
cover of all remaining label assignments.

## 3. Exact algebraic cuts from complete fibres

For a mixed word w whose COMPLETE fibre is {M,N}, the source gives
m_M+m_N=0, hence

```text
lambda^(chi(M)-chi(N)) = -1,
```

where chi(M) is the 28-coordinate physical-edge incidence vector.
Suppose three such fibres have differences d_1,d_2,d_3 and integers
epsilon_i in {+1,-1} satisfying

```text
sum_i epsilon_i d_i = 0 in Z^28,
sum_i epsilon_i is odd.
```

Multiplying their equations gives 1=-1, impossible over C. This is an
exact integer/Laurent identity. It does not use a mod-two approximation,
independence of matching monomials, or normalization of selected matching
weights. Every physical lambda_e is nonzero by the root-one reduction.

Each of the 39 stored cuts records its three mixed words, exact member
matchings, and signed integer relation. The independent checker recomputes
the incidence differences and their exact zero sum.

For each recorded word and matching, an auxiliary membership variable is
equivalent in BOTH directions to its eight endpoint-colour conditions.
Fixed mismatches are false and all-fixed matches are true. A learned
clause is the negation of the conjunction that all three fibres retain
their exact two members: it contains negative membership literals for
those members and positive membership literals for EVERY other matching.

Thus a label table may escape a cut by admitting a new cancellation term
or losing an old member. No additional matching is silently excluded.
The cuts are necessary consequences of the weighted source; they need
not be propositional consequences of the weaker collision-only CNF.

For illustration, one audited label table supplies the complete fibres

```text
00021012: {01,25,37,46} and {05,12,37,46}
00021210: {01,27,35,46} and {07,12,35,46}
01011010: {05,13,27,46} and {07,13,25,46}.
```

After dividing their nonzero spectator factors, they say the three
two-by-two permanents of

```text
[[lambda01, lambda05, lambda07],
 [lambda12, lambda25, lambda27]]
```

vanish. The first two equations substituted in the third give
-2 lambda01 lambda25 lambda27/lambda12=0, a contradiction. The complete
certificate uses the same signed-relation principle for all 39 cuts,
not only this illustrative label table.

## 4. Exact certificate leaves and their bridge

After the 39 algebraic cuts, all eighteen final CNFs are UNSAT. This
claim is supported by supplied proof objects, not solver status alone:

1. The portable generator reconstructs each final CNF from its scaffold
   and exact core data, with pinned variable/clausal order and explicit
   ASCII CRLF bytes. Every count and raw SHA256 must match the certificate.
2. A separately implemented semantic audit regenerates matchings by
   permutations and the stabilizer by generator closure, checks the full
   1,884-case cover, verifies all integer relations, and independently
   reconstructs every base, membership, and algebraic clause.
3. CaDiCaL 1.7.3 produced eighteen text DRAT proofs of the frozen FINAL
   CNFs. An independent drat-trim checker accepted all eighteen with
   exit zero and the exact verdict `s VERIFIED`. Positive and negative
   checker controls were also checked.
4. The [certificate package](r1-source-certificate/README.md) supplies all
   eighteen proof archives, raw and compressed hashes, reproducible
   generators, and separate semantic/certificate checkers. The archives
   decompress to the exact independently checked proof bytes.

The raw proofs total 8,003,487 bytes, stored losslessly in 2,039,952 bytes
of compressed certificate data. Raw CNFs are regenerated; discovery models
and solver logs are not proof inputs. External binaries are not committed.
The proof replay records and pins its checker executable as an explicit
tool dependency. The generator needs no SAT solver.

The mathematical bridge is now complete: any hypothetical source supplies
one scaffold representative and a label assignment satisfying its base
clauses and every algebraically proved cut. Truthful auxiliary variables
extend it to a satisfying assignment of that representative's final CNF.
The accepted UNSAT certificate contradicts this. Since the representatives
exhaust all selected pure-matching triples, no source in the stated
root-one branch exists.

## Evidence status and remaining scope

The [independent semantic review](../../../docs/audits/EIGHT_VERTEX_MATRIX_UNIT_SEMANTIC_REVIEW_2026-09-04.md),
[independent certificate audit](../../../docs/audits/EIGHT_VERTEX_MATRIX_UNIT_CERTIFICATE_REVIEW_2026-09-04.md),
and [final integration review](../../../docs/audits/EIGHT_VERTEX_MATRIX_UNIT_INTEGRATION_REVIEW_2026-09-04.md)
have distinct roles. The certificate checker does not establish the
physical source bridge; the source audit does not itself certify UNSAT.
No Lean or other kernel-checked formalization is asserted.

Consequently every hypothetical ternary eight-vertex witness has maximum
torus-root cardinality at least two. This removes the entire n=8/r=1
child of M1 and supplies its r>=2 source branch at that order. It does not
assert an invertible edge exists: zero or nonmonomial rank-one blocks can
also supply a root pair. Other root orders and incidence configurations,
arbitrary even n, and the original global conjecture remain open.
