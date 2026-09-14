# Exact controls for proposed hafnian reductions

These controls arose while trying to bridge recursive cancellation
consistency to all-order weighted Bogdanov. They are actual one-colour
integer matrices, not three-colour GHZ witnesses. They disprove overly broad
intermediate premises, not the Krenn--Gu conjecture. The global status remains
**UNRESOLVED**.

## Active edges need not contain a perfect matching

Take the hollow symmetric six-by-six matrix Z with bipartite block B,

    B = [ 1  1  1 ]
        [ 1  1  1 ]
        [ 1 -1 -1 ],       Z = [ 0  B ; B^T  0 ].

Its hafnian is the permanent of B, namely -2. For an edge e write
q_e = Z_e haf(Z[V-e]). The nonzero scores are

    q_03=q_13=q_24=q_25=-2,   q_23=2.

All other scores are zero. Thus the active-edge graph has edges
03,13,23,24,25. Vertices 0 and 1 both have 3 as their only neighbour, so this
graph has no perfect matching. Nevertheless every vertex's score sum is -2;
the normalized Laplace scores sum to 1 at every vertex exactly as required.

This example is bipartite and uses only nonzero integer weights +/-1 on its
support. Odd-cycle concerns and irrational phases are not the explanation.
Every genuine one-colour hafnian identity, including all signed-ratio and
integer-circuit constraints, is satisfied. Therefore those identities alone
cannot supply a perfect matching of active edges. A proposed weighted
Bogdanov proof selecting private active matchings must use additional global
two-/three-colour partition hypotheses to establish their existence.

Appending any number of isolated unit-weight pairs preserves the hafnian -2
and appends isolated active matching edges; the original Hall obstruction
remains. The countercontrol therefore exists at every even order n>=6.
This does not contradict WB1, whose full three-colour degree-four hypotheses
are much stronger.

## Principal-hafnian supports do not have unrestricted symmetric exchange

On vertices 0,...,5, set

    Z_01=Z_02=Z_12=1,
    Z_0t=Z_1t=1, Z_2t=-2  for t=3,4,5,
    Z_34=Z_35=Z_45=0.

Then h({0,1})=1 and h(V)=-12. But h({0,1,2,t})=1+1-2=0 for
each t=3,4,5. Consequently the family S={A: h(A)!=0} fails the following
proposed exchange premise:

> For A,B in S and x in A symmetric-difference B, there is a distinct y in
> A symmetric-difference B such that A symmetric-difference {x,y} is in S.

Choose A={0,1}, B=V, and x=2. Every eligible y fails. Even this one-sided
exchange conclusion is false, before asking the exchanged B to survive too.
Thus a uniform support-family argument cannot import this exchange property
without proving genuinely stronger hypotheses. The countercontrol extends
to every even n>=6 by the same isolated-pair construction: extra eligible y
also fail because their unique partner is absent from the four-set.

## Pair contraction is not a free Schur-complement reduction

Take all pair weights 1 on six vertices. The exact coefficient after
contracting vertices 0,1 against their one-colour test vectors is
haf(K6)=15. The tempting replacement on the remaining four vertices,

    Z'_ij = Z_ij + (Z_0i Z_1j + Z_0j Z_1i)/Z_01,

has every edge equal to 3, hence haf(Z')=27. It wrongly includes matchings
using two inserted rank-two correction edges, which would use the removed
vertices twice. A valid source-preserving reduction must control those extra
terms; writing the contracted tensor as a sum of hafnians does not itself
produce a smaller source of the original kind.

## Reproduction and consequence

`python -m unittest -v tests.test_hafnian_source_reduction_controls` checks
the exact values with an independent recursive integer hafnian oracle,
checks matching existence directly, and tests the isolated-pair extensions
through twelve vertices. The written factorization proves the extensions
at all orders; the finite checks alone would not.

These controls narrow the parent obligation. A successful reduction must
exploit the simultaneous colour equations and explicitly preserve nonzero
target coefficients and the original pair-source representation. Single-colour
recursion and signed consistency remain useful necessary conditions, but
do not furnish either active matchings, unrestricted exchange, or a general
pair-deletion induction.
