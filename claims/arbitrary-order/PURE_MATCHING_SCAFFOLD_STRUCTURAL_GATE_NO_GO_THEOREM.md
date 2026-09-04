# Pure-matching scaffold obstruction to structural-gate closure

## Status and evidence

**Proved mechanism obstruction over C**, independently reviewed on
2026-09-04. This is an arbitrary-order family of physical edge arrays that
satisfy the explicitly listed necessary conditions and fail the full GHZ
equations. It is neither a Krenn--Gu counterexample nor a proof of
nonexistence. The global conjecture remains **UNRESOLVED**.

The arbitrary-order and generic statements have written proofs below.
Two separately implemented exact rational replays check the finite algebra
used by those proofs. They do not certify a numerical generic specialization
or replace the incidence arguments. No Lean formalization is supplied.
See the [independent review](../../docs/audits/PURE_MATCHING_SCAFFOLD_STRUCTURAL_GATE_NO_GO_REVIEW_2026-09-04.md).

## Parent actually attempted

Can exact pure target amplitudes, the column-killer theorem, all termwise
root-annihilation tests, and maximal-root blocker incidence force a small
surplus, a missing torus root, or some contradiction at arbitrary order?

Answer: this collection of conditions admits physical graphs with dense
bichromatic blocks, arbitrarily large order, maximum torus root exactly five,
and every outside mode a three-colour blocker at every maximum root. Moreover
they satisfy every majority-subset ideal-power inclusion, including the
entangled harmonic consequence. Thus this collection cannot alone prove the
parent. Full source/cofactor coefficient equalities are essential.

This does NOT say all accepted maximal-root theorems are satisfied. In
particular the exact nonzero source identity is not an annihilation test.

## Family

Let n=4k, k>=5. Partition the vertices into k four-vertex blocks. On each
K4 use its three perfect matchings as the three colours: on vertices 0,1,2,3,
take M_0={01,23}, M_1={02,13}, M_2={03,12}. Their unions across components
are three pairwise edge-disjoint perfect matchings, whose union is H.

Set W_e=E_cc on e in M_c. On every remaining unordered pair set W_e to an
arbitrary hollow 3-by-3 matrix, with six independent parameters. Orient
blocks consistently; reversal means transpose. Let P be this affine
parameter space, D=6*(binom(n,2)-3n/2).

The following assertions hold for EVERY parameter point:

1. T_W(c,...,c)=1 for each c. The only scalar colour-c support is M_c.
2. Each vertex has an exact monochromatic column killer for each colour.
3. If arbitrary local vectors x_v make every perfect-matching PRODUCT of
   contracted edge forms zero, then Delta_3((x_v))=0. Indeed the product
   belonging to M_c is exactly product_v x_v[c]; each of the three products
   therefore vanishes separately. The same holds identically on any chosen
   product subspaces. This includes arbitrary termwise star-annihilation
   tests, without any torus assumption.
4. For any zero-coupled root set R and any colour c with all x_i[c]!=0,
   no M_c edge can be internal to R. Its matching maps the r roots injectively
   outside, and each image vertex is an actual colour-c blocker: its root
   row is x_i[c] e_c^T. Thus every raw colourwise multi-star quota |B_c|>=r
   holds for all such tuples.
5. A fully supported zero-coupled root set contains at most one vertex from
   each K4 block. Its 3r scaffold neighbours are distinct actual blockers,
   giving r in each colour and at least 3r in total. In particular a
   zero-coupled pair has six distinct scaffold blockers, satisfying both the
   actual double-star per-colour quota and the five-total-blocker quota.
6. Let n=2m and |S|=m+q, 1<=q<=m-1. In the block-squarefree edge ideal I_S,
   each pure tensor tensor_(i in S)e_(i,c) belongs to I_S^q. The matching
   M_c has at least q internal S edges, each exactly the generator
   e_(i,c)e_(j,c). Multiply any q of these disjoint generators by the
   remaining coordinate factors. This is a literal ideal-power expression,
   not merely radical membership. It proves the complete majority hierarchy
   and all its entangled harmonic consequences on this family.

## Generic maximum torus-root theorem

There is a nonempty Zariski-open subset P_good on which the largest fully
supported pairwise zero-coupled root set has cardinality EXACTLY FIVE.
The field is C, and the parameter space and constructions are defined over
Q. No particular rational specialization satisfying all the generic
conditions has been computationally certified here. A torus root means a
set of distinct vertices with a nonzero vector at each vertex, all three
coordinates nonzero, and every internal scalar coupling x_i^T W_ij x_j
zero. Vectors are taken projectively; the normalization x_i[0]=1 is legal
throughout the torus.

### No six roots

For a fixed six-set containing a scaffold edge, torus zero coupling is
impossible since x_i[c]x_j[c]!=0. For a fixed scaffold-independent six-set,
its root space is ((G_m)^2)^6 of dimension 12 after projective normalization.
Each of its fifteen pairs is an independently parameterized hollow block.
At every torus root tuple its coupling equation is a nonzero linear equation
on that block's six parameters. Thus all fifteen equations have independent
parameter directions, and the incidence has dimension D+12-15=D-3. Its
projection closure in P is proper. Avoid the finitely many such closures.
A larger root set would contain a six-set, so none exists either.

### Five roots exist generically

Take one vertex from each of five distinct K4 components. All ten internal
blocks are free. Normalize each root x_i=(1,s_i,t_i), i in Z/5, and use the
regular tournament i->i+1,i+2 (mod5). On edge i->i+1 use the bilinear form

  x_(j,2) (x_(i,1)-x_(i,0)) = t_j(s_i-1),

whose only nonzero matrix entries are W_12=1,W_02=-1. On edge i->i+2 use

  x_(j,1) (x_(i,2)-x_(i,0)) = s_j(t_i-1),

whose only nonzero entries are W_21=1,W_01=-1. If edge orientation reverses,
transpose its block. These are hollow blocks. At all roots (1,1,1), all ten
forms vanish and their Jacobian in the ten variables s_i,t_i is a permutation
matrix. The incidence projection is consequently dominant (local
implicit function theorem, equivalently a smooth point with surjective
projection differential). Its constructible image contains a nonempty open.
Intersect with the no-six open. Then maximum root size is exactly five.

### Every maximum root has full outside row span generically

For each scaffold-independent five-set, its internal incidence is a vector
bundle of codimension ten over a ten-dimensional torus, so has dimension D.
Fix an outside vertex u. At most one root is a scaffold neighbour of u,
so let t in {0,1} denote their number. This row, if present, is a nonzero
multiple of one coordinate vector. Each of the other 5-t hollow blocks has an
unrestricted row value at the corresponding fully supported root vector:
the map B -> x_i^T B is onto C^3. These parameter blocks are independent
of the ten internal root equations.

There are at least four unconstrained row vectors. Their failure to
complete rank three has codimension three: when t=0 it is the rank-at-most-two
locus of a 5-by-3 matrix; when t=1 it is the rank-at-most-one locus of the
4-by-2 matrix modulo the fixed row. These parameters are independent of the
internal equations. The bad incidence therefore has dimension D-3.
Avoid its projection closure for all finitely many (R,u). Then at EVERY
five-root tuple, every outside span is C^3. Every outside vertex is an actual
blocker for all three colours, with K_u=0. There is no residual simultaneous
kernel to exploit.

Therefore maximum-root surplus is s=n-10, unbounded along n=4k, and all
maximum-root outside modes are triple blockers. In particular s>=10, so the
accepted companion-depth theorem places the physical pair deck below the
linear root sensor's depth floor. Small-surplus supply cannot be forced
using this collection of structural conditions.

## Explicit failure of the full source

At zero hollow filling, choose a colour assignment constant on each K4,
but different on two components. Within each K4 there is exactly one
matching inheriting its chosen pure colour, so this global mixed word has
coefficient exactly one. For general filling that coefficient is a polynomial
with constant term one. Its nonvanishing open can be intersected with all
the generic opens above. Alternatively choose the hollow parameters to be
positive algebraically independent real numbers: all proper rational
algebraic bad loci are avoided, and the exhibited mixed coefficient is at
least one since every matching summand is nonnegative. This specifies an
exact existence family, not a certified explicit numerical specialization.

The first-jet controls use signed specializations solely to prove dominance;
they need not themselves satisfy the other generic conditions or positivity.

## What this DOES NOT prove, and the sharper next lemma

These graphs are not claimed to be witnesses. Generic fillings have mixed
coefficients which do not vanish. Pure normalization, killer structure,
all termwise annihilation gates, the complete majority ideal hierarchy,
and even full triple-blocker maximal-root incidence leave those coefficients
uncontrolled. The construction does not refute an implication that includes
the full source identity; that identity is exactly what it does not assert.

The attempted parent synthesis combined the column-killer/root-blocker
mechanism with the entangled majority-ideal mechanism to supply the
small-surplus source receivers. This family satisfies both mechanisms at
once, with unbounded surplus. Thus that proposed implication from the listed
structural premises is false; neither premise was merely tested in isolation.

A sharper open route must retain the actual coefficients of the same
physical source. For example, for an array in this family with maximum torus
root five and every exterior span full, prove directly that some mixed
coefficient is nonzero, including the exceptional complex fillings where
the displayed mixed coefficient vanishes. The generic nonvanishing proved
above does not decide those exceptional fibres. Nor would excluding this
family alone exclude all hypothetical witnesses.

One possible direct consumer is a full-source high-surplus descent theorem:
under T_W=Delta, either some maximum root has surplus <=2, or an exact
mixed-word contradiction can be derived from the same physical source.
This would feed the existing surplus-two machinery where its additional
hypotheses apply, but is still OPEN; the downstream attachment and gluing
obligations would also remain. The proof-topology delta here is elimination
of a structural-only supply mechanism, not closure of a witness branch.

## Owning interfaces and replay

- [Column-killer theorem](THREE_COLOUR_HYPERPLANE_ANNIHILATION_THEOREM.md).
- [Double-star blockers](DOUBLE_STAR_ANNIHILATION_LEMMA.md) and
  [multi-star blockers](MULTI_STAR_BLOCKER_FACTORISATION_LEMMA.md).
- [Majority ideal hierarchy](MAJORITY_SUBSET_INTERNAL_EDGE_IDEAL_HIERARCHY.md).
- [Complete-deck sensor and higher-surplus depth boundary](MAXIMAL_ROOT_SURPLUS_TWO_COMPLETE_DECK_SENSOR_AND_HIGHER_SURPLUS_DEPTH_BOUNDARY_THEOREM.md).
- [Same-pair supply](MAXIMAL_ROOT_SURPLUS_TWO_SAME_PAIR_QUOTIENT_SURVIVAL_AND_COMPLEMENTARY_PERMANENT_DOMINANCE_THEOREM.md),
  whose nonzero complete source equation is not supplied by this control.

```text
python claims/arbitrary-order/verify_pure_matching_scaffold_structural_gate_no_go.py
python claims/arbitrary-order/audit_pure_matching_scaffold_structural_gate_no_go.py
```

The primary replay expands sparse bilinear polynomials, computes the
ten-variable Jacobian determinant exactly, and enumerates all 105 matchings
of the eight-vertex zero-filling control. The independent replay instead
solves the five-by-six first-jet map by rational row reduction and constructs
the tournament Jacobian from the resulting jet preimages. It imports no
primary constructor or arithmetic helper. Both are finite corroboration.
