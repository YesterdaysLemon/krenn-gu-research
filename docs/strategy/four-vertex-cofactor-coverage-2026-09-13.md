# Four-vertex cofactor coverage

This is a human proof explaining a bounded support diagnostic, with an
exhaustive local combinatorial check. It is not a frontier promotion and
awaits separate review. Its scope is all-diagonal complex sources only.
The global Krenn--Gu conjecture remains **UNRESOLVED**.

## A uniform sufficient obstruction

Let V have even size n>=6 and let c,d,e be the three colours. Write G_j
for the support of Z^j and h_j(A)=haf(Z^j[A]). Suppose that every four-set
U satisfies at least one of:

1. U has two disjoint edges, one in G_d and one in G_e;
2. both G_d[U] and G_e[U] have a perfect matching.

Then these supports cannot underlie an all-diagonal weighted GHZ witness.

**Proof.** Fix U and suppose h_c(V-U) is nonzero. Alternative 1 contradicts
the three-part mixed-word equation: its three factors are h_c(V-U) and the
two nonzero edge weights of colours d,e.

Under alternative 2, if there is a mixed d/e matching use the same argument.
Otherwise the geometric perfect-matching sets of G_d[U] and G_e[U] are
disjoint: a matching present in both could have its two edges assigned
different colours. There are only three geometric perfect matchings on four
vertices. Both sets are nonempty, so one is a singleton. That colour's
hafnian on U is a single nonzero monomial. The two-part mixed-word equation
with h_c(V-U) gives a contradiction. Both shores are nonempty since n>=6.

Thus h_c(V-U)=0 for every four-set U. Expand h_c(V) at any vertex, and each
resulting (n-2)-hafnian at any remaining vertex. Every resulting term contains
one of these zero (n-4)-hafnians, so h_c(V)=0, contrary to the required
nonzero monochromatic coefficient. This proves the obstruction.

This proof uses the complete four-vertex matching fibre, the two- and
three-colour equations, and two Laplace expansions. It does not use a rank
bound of the output tensor or an unproved source-reduction operation.

## Application to the dense-private diagnostic family

There is a simpler and stronger support criterion. A graph on n>=4 vertices
has a perfect matching on **every induced four-set** exactly when its
complement has maximum degree at most two and contains no triangle.

For necessity, three nonneighbours of one vertex give a four-set with an
isolated vertex. A triangle of nonedges, together with any fourth vertex,
gives three vertices that can only be matched to that one fourth vertex.
For sufficiency, a graph on four vertices without a perfect matching has
pairwise-intersecting edges; such an edge family is contained in a star or
a triangle. The former makes a triangle in its complement, and the latter
makes a complement vertex of degree three. Either violates the hypotheses.

Consequently, **two colour support graphs whose complements both have
maximum degree at most two and no triangle cannot occur in an all-diagonal
witness at any even n>=6**. Alternative 2 of the coverage obstruction holds
on every four-set. The third colour support is unrestricted. Equivalently,
for every pair of colours in a hypothetical witness, at least one colour's
nonedge graph has a vertex of degree at least three or a triangle.

Let P_c,P_d,P_e be three pairwise edge-disjoint perfect matchings of V.
It is sufficient that

    G_d contains K_V minus (P_c union P_e),
    G_e contains K_V minus (P_c union P_d).

There is no further hypothesis on G_c for this implication. To prove the
coverage condition, observe that each base support's complement is a union
of two disjoint perfect matchings, hence a disjoint union of even cycles
with maximum degree two and no triangle. The preceding criterion makes
both base supports matchable on every four-set. Adding edges preserves
that condition.

In particular the family

    G_j = K_V minus the other two P's,  j=0,1,2,

is excluded at every even n>=6, for every choice of three disjoint perfect
matchings and arbitrary nonzero complex weights on the required edges.
The n=4 boundary is essential: the three one-factor classes of K4 give a
genuine GHZ_4 source, and the two-part step would have an empty complement.

This is not permission to complete the support of an arbitrary witness.
The required dense supports are a genuine hypothesis. Monotonicity is used
only for the explicitly stated combinatorial coverage condition, not for
weighted realizability or nonexistence in general.

## What the experiments did and did not establish

The n=12 round-robin matching instance returned UNSAT both without and with
ratio-parity clauses, in about 0.36 seconds after generation. The n=14
ratio-parity instance returned UNSAT in about 1.57 seconds after generation.
Both diagnostic solvers reported zero decisions and zero conflicts; the
contradiction was propagated. These are solver observations, not proof-trace
certificates. The argument above independently explains the whole family
and makes further orders of this diagnostic unnecessary.

At n=12 an even simpler direct obstruction exists: shores
{1,3,6,11}, {4,7,8,10}, {0,2,5,9} are uniquely matchable in colours 0,1,2.
At larger orders one need not seek three small uniquely-matchable shores;
the cofactor argument handles the remaining vertices exactly.

Neither the signed constraints nor any new phase obstruction was needed for
this family. No claim of general n=12 or n=14 exclusion is made.

## Exact check and remaining parent

The local implication also gives a short redundant SAT cut. For every live
(n-4)-cofactor in colour c and every pair of geometric matchings M_d,M_e on
its complementary four-set, forbid all four indicated edge-support bits
being true. There are 27*C(n,4) such five-literal clauses. They follow from
the original RZP rules and full GHZ partition conditions, so they are
shortcuts, not additional mathematical assumptions. The implementation is
`src/krenn_gu/recursive_hafnian_cofactor_cuts.py`, enabled by the probe's
`--four-cofactor-coverage` flag. It is disallowed with the missing-singleton
or two-part-only controls; the n=4 case adds no clauses.

`python -m unittest -v tests.test_four_vertex_cofactor_coverage` exhausts
all 64^2 ordered graph pairs on four vertices and all ordered triples of
pairwise-disjoint partial matchings on four vertices. It checks the local
matching-count and density implications and retains the n=4 sharp boundary.
The written cofactor argument, not these finite tests, supplies all orders.

For the unrestricted all-diagonal parent, a surviving support must fail this
four-set coverage condition for every choice of the target colour c. Those
uncovered four-sets are a precise place to inspect the signed-ratio mechanism.
The coverage obstruction does not show that such surviving supports cannot
exist, and nothing here covers bichromatic physical blocks.
