# Five-root zero-coupling intersection lemma

## Status

This is an exact arbitrary-order algebraic-geometric lemma.  Given any
five vertices and arbitrary complex bilinear edge blocks between them,
there are nonzero projective vectors at the five vertices that kill all
ten internal edge couplings simultaneously.

The vectors need not have all three target coordinates nonzero.  That
coordinate-boundary issue is essential: this lemma alone does not invoke
the blocker theorems, exclude a Krenn--Gu witness, or solve the prize
conjecture.

## Theorem

For every pair `0 <= i < j <= 4`, let

```text
B_ij : C^3 x C^3 -> C
```

be a bilinear form.  There are projective points

```text
[x_i] in P^2(C),  i=0,...,4,
```

such that

```text
B_ij(x_i,x_j) = 0
```

for all ten pairs `i<j`.

## Intersection proof

First suppose that none of the ten forms is identically zero.  Work on

```text
X = (P^2)^5.
```

Let `h_i` be the pullback of the hyperplane class from factor `i`.
The zero locus of `B_ij` is an effective Cartier divisor `D_ij` with
class

```text
[D_ij] = h_i + h_j.
```

The Chow ring is

```text
A*(X) = Z[h_0,...,h_4] / (h_0^3,...,h_4^3).
```

Consequently the intersection class of the ten divisors is

```text
product_(i<j) (h_i+h_j).
```

Every term has total degree ten.  A monomial survives the relations
`h_i^3=0` only when every exponent is exactly two, so

```text
product_(i<j) (h_i+h_j)
  = 24 h_0^2 h_1^2 h_2^2 h_3^2 h_4^2.                 (1)
```

To see the coefficient, choose one endpoint from every edge of `K_5`.
The exponent of `h_i` is the number of edges assigned to vertex `i`.
Thus a contribution to the top monomial is an orientation of `K_5`
with indegree two at every vertex, namely a labeled regular tournament.
All regular tournaments on five vertices are cyclic.  Their automorphism
group has order five, so there are

```text
5! / 5 = 24
```

of them.

The class in (1) is nonzero.  Intersecting Cartier divisors gives a
class supported on their common zero locus.  An empty common zero locus
would therefore give the zero class, contradicting (1).  Hence the ten
forms have a simultaneous projective zero.

If some `B_ij` is identically zero, replace it temporarily by any
nonzero bilinear form.  A simultaneous zero of the stronger ten-form
system supplied above also solves the original system, whose replaced
equation was vacuous.

## Exact boundary exposed by the lemma

Let

```text
T = {([x_0],...,[x_4]) in X :
     every one of the 15 coordinates x_i[c] is nonzero}.
```

The theorem proves that the projective zero locus `Z` is nonempty, but
it does not prove `Z intersect T` is nonempty.  Therefore every set of
five vertices lies in one of two sharply stated cases:

1. a fully supported, pairwise zero-coupled five-root tuple exists; or
2. the entire common zero locus lies in the union of the fifteen
   coordinate hyperplanes `x_i[c]=0`.

The second alternative is a toric-boundary condition on a fixed
multihomogeneous system.  It is substantially more rigid than merely
failing to find roots numerically: in a proper intersection, all 24
points counted with multiplicity must lie on that boundary.

This connects directly to the blocker program.  A fully supported
five-root tuple activates the multi-star lower bound in every colour.
At order ten, exact five-blocker equality would leave no residual
vertices, and the root--blocker permanent would be a restriction

```text
P_5 -> Delta_3.
```

Thus a complete obstruction to that tensor restriction would reduce
the unrestricted ten-vertex case to the explicit coordinate-boundary
alternative above.  At larger orders a residual matching tensor
remains, so additional work is still required.

## Verification

Run:

```text
python verify_five_root_zero_coupling_intersection.py
```

The verifier expands the Chow product in the truncated ring, enumerates
all `2^10` endpoint choices, checks that exactly 24 have exponent vector
`(2,2,2,2,2)`, and independently confirms that they form one
`S_5`-orbit with stabilizer order five.
