# Complete eight-vertex protected-scaffold exclusion

## Status and exact statement

**Proved finite computer-assisted exclusion over C.** Take two four-vertex
components L={0,1,2,3}, R={4,5,6,7}. In each component fix

~~~text
M0={01,23}, M1={02,13}, M2={03,12}.
~~~

For every internal edge in Mc its physical block is exactly E_cc, of weight
one. Every crossing physical block is an arbitrary hollow three-by-three
complex matrix. Thus all 96 crossing entries X_cd[i,j]=W_(i,j+4)[c,d], c!=d,
are free, with zeros allowed and no genericity or nonzero assumptions.
No source in this entire family has the normalized ternary GHZ matching
tensor. All three pure amplitudes are identically one.

This closes the complete k=2 instance of the
[protected pure-matching scaffold family](../../arbitrary-order/PURE_MATCHING_SCAFFOLD_STRUCTURAL_GATE_NO_GO_THEOREM.md).
It does not exclude arbitrary eight-vertex sources, larger protected
scaffolds, or the earlier 129-entry Boolean survivor. There is no reduction
from arbitrary witnesses to this scaffold. Global Krenn–Gu remains
**UNRESOLVED**. No Lean formalization is supplied.

The proof is an exact witness-to-Boolean implication followed by a checked
refutation. Polynomial reconstruction and proof replay have independent
implementations within this session; this is not separate-human refereeing.

## Exact source and exhaustive parameter scope

Let P_w=T_W(w)-delta_w for every w in {0,1,2}^8. Expand all 105 physical
perfect matchings, substitute only the stated internal entries and hollow
crossing diagonals, and combine equal monomials over Z. Keep the
pure-minus-one constants until they cancel exactly.

The 6,561 rows contain 33,702 combined nonzero terms, all of coefficient +1.
There are 33,696 distinct nonconstant monomials. Six nonpure
component-constant rows contain the fixed constant one. The three pure rows
are zero polynomials after target subtraction. Both reconstructions check
these facts; pure normalization is not discarded.

Number crossing entries 1 through 96 lexicographically by (c,d,i,j), c!=d.
The [primary](../../../src/krenn_gu/scaffold_source.py) enumerates matchings
by quotienting vertex permutations, then assigns allowed endpoint colours.
The independent audit enumerates each word first, with bitmask matching
recursion and explicit scalar edge factors. Both reproduce the complete
coefficient-bearing equation SHA-256:

~~~text
f10ab786a60cb8dc85a575eef373e90cb4fc4ea9eec95ec68b3388ed781780ee
~~~

No sampling, fixed support, weight grid, or numerical tolerance enters the
accepted exclusion.

## Witness-to-CNF bridge

At a hypothetical complex source let b_x mean x!=0. For every distinct
nonconstant monomial m, let z_m mean all its factors are nonzero. Encode
both directions:

~~~text
z_m => b_x                     for every factor x;
(AND_(x divides m) b_x) => z_m.
~~~

This is exact because C has no zero divisors. One-factor monomials use b_x
directly. If a zero-target row has no constant, it cannot have exactly one
nonzero monomial, so for each m add

~~~text
z_m => OR_(m' in that row, m'!=m) z_m'.
~~~

If the row has constant one, at least one nonconstant term is nonzero; add
their disjunction. These clauses are necessary only: they do not assert
that two terms can cancel or that a satisfying support admits weights.

Every hypothetical physical source therefore induces a model of this
single CNF, including every possible pattern of zero crossing entries.
There is no extra case-cover premise. The CNF has 33,792 variables and
196,806 clauses, with canonical LF DIMACS SHA-256

~~~text
024f9b3a6cee02b4a90327915ea029ff567d3ebb694edfd498e1c5422ec84b6a
~~~

## Portable exact proof leaf

The [RUP fixture](../../../tests/fixtures/eight_vertex_scaffold_full_source_rup.json)
contains 1,521 zero-based original-clause indices and 108 ordered additions,
ending with the empty clause. It is about 13 KB. No SAT solver or discovery
run directory is required.

The [primary checker](verify_eight_vertex_scaffold_full_source_exclusion.py)
regenerates the full CNF, checks both hashes and all original indices, then
starts from exactly those original clauses. For each proposed clause C it
assumes the negation of each literal and performs exact unit propagation.
A conflict proves that the preceding clauses imply C. Induction proves
every addition, including the empty clause. Thus the core and full CNF
are unsatisfiable, completing the physical-source exclusion.

The primary reuses the repository's
[plain RUP checker](../../../src/krenn_gu/source_quotient_core.py).
The [independent audit](audit_eight_vertex_scaffold_full_source_exclusion.py)
reconstructs the equations and entire CNF without primary scientific imports,
and independently propagates the portable proof. Bridge controls detect
omitted target constants, matchings, AND directions, singleton clauses and
constant-row constraints. The [tests](../../../tests/test_scaffold_full_source.py)
reject wrong hashes, invalid origins, a false lemma, a necessary omitted
step and a missing final empty clause; propagation has positive and negative
controls.

Discovery used CaDiCaL195 through python-sat. Its Windows child failed with
exit 3221226505 after writing the full proof and result. That run remains
failed; it is not the acceptance gate. The saved proof passed drat-trim
v05.22.2023 with -U, reporting s VERIFIED and zero RAT steps. Checker
binary SHA-256:

~~~text
a48ebed7b4b6b373d3ddbeb3368dae7622a9e17bab7fe6eb751ab996757f9fbe
~~~

Full DRAT SHA-256:

~~~text
e214e4fdde2f7954c0e7c6c2de3b9a342e03d293b50153386577bdcb2b9a4db6
~~~

The durable fixture retains the checked core and ordered additions, omitting
deletions. This is sound: extra clauses cannot destroy a unit-propagation
conflict. The two portable replays are the durable acceptance gate. The
optional exploratory probe can emit the canonical CNF without a solver.
Its native Glucose4 binding also produced a truncated trace in a separate
calibration run; that trace was rejected. Use a standalone solver and
independent proof checking when native proof export fails.

## Exact countermodels to the proposed weaker parent

Monochromatic-shore equations do not exclude this scaffold. Adding every
binary restriction still does not exclude it. The
[control fixture](../../../tests/fixtures/eight_vertex_scaffold_subsystem_controls.json)
lists explicit physical families. In each X_cd the two displayed entries
have weights r_cd,-1/r_cd; all others vanish. The six parameters are
independent and nonzero.

| Family | Equations satisfied identically | Full-word failures |
|---|---|---|
| monochromatic_shores_v1 | All 477 words constant on L or R | 27 nonzero Laurent monomials |
| binary_and_monochromatic_shores_v2 | All 1,065 words in the union of both shore conditions and every binary restriction | 29 nonzero Laurent monomials, all involving three colours |
| independent_minorities_and_component_constants_v3 | All 1,869 words in the union of every independent-minority condition and all nine component-constant targets | 27 nonzero Laurent monomials, all involving three colours |

For family one, P_00012121=-r02/r12. For family two,
P_00020011=-r01/r21 and P_01000002=r02*r10. No nonzero parameter choice
repairs either family into a full witness. All r=1 gives rational controls
with crossing weights +1,-1.

The third family sharpens the failure of the proposed larger-order mechanism:
even every localized minority equation together with all component-constant
targets is insufficient. Its 1,875 indexed minority evaluations represent
1,863 distinct words; adjoining the six nonpure component-constant words
gives 1,869. Its first full error is P_00010221=-r01/r10, from the unique
matching (01)(27)(34)(56). Its directed minority graphs have only the cycles
(2,7,3,5), (0,6,2,5), and (1,7,2,6), respectively; each contains an Mc pair
and is therefore inadmissible. All parameter choices remain nonwitnesses.

The construction allocates each colour's two internal matching edges to the
other two colours. Crossing pairs of product -1 cancel unwanted
component-constant coefficients. Appropriate opposite-direction routing
sends extra contributions into three-colour words. The same six matrices
serve every equation, preserving physical coupling.

The [primary](verify_eight_vertex_scaffold_subsystem_controls.py) substitutes
into the complete 96-variable polynomials. The
[independent Laurent audit](audit_eight_vertex_scaffold_shore_countermodel.py)
reconstructs matchings for each word, and also checks rational and Gaussian
specializations.

## Larger-order boundary and reproduction

The [minority-cycle and exterior-resource theorem](../../arbitrary-order/PROTECTED_SCAFFOLD_MINORITY_CYCLE_AND_RESOURCE_BOUNDARY.md)
identifies equations that localize at arbitrary order. General slices also
contain exterior matching-edge resources, each usable once. An exact
twelve-vertex control satisfies the complete localized minority subsystem
while an exterior component changes a mixed amplitude from 1 to 0.
Applying the eight-vertex theorem to an induced restriction is therefore
not justified. Controlling the shared resource sums remains open.

From repository root:

~~~bash
python claims/finite/n08/verify_eight_vertex_scaffold_full_source_exclusion.py
python claims/finite/n08/audit_eight_vertex_scaffold_full_source_exclusion.py
python claims/finite/n08/verify_eight_vertex_scaffold_subsystem_controls.py
python claims/finite/n08/audit_eight_vertex_scaffold_shore_countermodel.py --output tmp/scaffold-controls-replay.json
python -m unittest -v tests.test_scaffold_full_source
~~~

The [strategy note](../../../docs/strategy/scaffold-source-parent-attempt-2026-09-14.md)
records the parent attempt, countermodels and exact proof-topology delta.
