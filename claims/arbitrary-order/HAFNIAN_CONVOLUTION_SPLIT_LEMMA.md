# Hafnian convolution-split lemma

## Status

This is an arbitrary-order algebraic strengthening of the hafnian
set-tree reduction.  It applies to every complex symmetric matrix and
therefore to each saturated-diagonal colour matrix in the simultaneous
balanced all-bridge branch.

It supplies necessary representability constraints that are absent from
an abstract set tree.  It is a strict reduction, not a contradiction and
not a proof of the global Krenn--Gu conjecture.

## Identity

Let `L` be a symmetric matrix indexed by an even set `U`, with
`|U|=2m`.  For every `0 <= k <= m`,

```text
sum_(A subset U, |A|=2k)
    haf(L[A]) haf(L[U minus A])
  = binomial(m,k) haf(L[U]).                          (1)
```

To prove (1), expand the left side into perfect-matching monomials.  A
perfect matching `M` of `U` occurs exactly when `A` is the union of `k`
edges of `M`.  There are exactly `binomial(m,k)` such choices.  No sign
is introduced, so the coefficient of every matching monomial is the
same on both sides.

The bipartite specialization is

```text
sum_(|S|=|T|=k)
    per(P[S,T]) per(P[X-S,Y-T])
  = binomial(m,k) per(P),                             (2)
```

for an `m x m` matrix `P`.

## Nonzero-family consequence

Define

```text
T(L) = {nonempty even A subset U : haf(L[A]) != 0}.
```

If `U` belongs to `T(L)`, then for every `1 <= k < m`
there is a subset `A` of size `2k` such that

```text
A belongs to T(L),
U minus A belongs to T(L).                            (3)
```

Indeed, the right side of (1) is nonzero over `C`, so at least one
summand on the left is nonzero.  Iterating (3) shows that a nonzero
principal hafnian admits a partition into nonzero principal hafnians of
every prescribed even block-size composition.

The familiar set-tree axiom uses vertex-wise Laplace expansion and gives
only the `k=1` split through a prescribed vertex.  Equation (3) adds
complementary splits at every size.  It is necessary for an abstract
Boolean family to be representable by actual principal hafnians.

## Application to the balanced all-bridge zero layer

For a colour `c`, let `Z^c` be its saturated-diagonal matrix and

```text
T_c = {nonempty even A : haf(Z^c[A]) != 0}.
```

Every member of `T_c` obeys the two normal-bit balance equations from the
universal zero-layer theorem.  The split pieces in (3) are themselves
members, so they obey the same balance equations.  Consequently every
hypothetical all-bridge witness gives three families that satisfy
simultaneously:

1. the vertex-wise set-tree expansion axiom;
2. the all-size convolution-split axiom (3); and
3. incompatibility under partitions assigned to pairwise distinct
   colours.

This corrected system is stronger than the earlier set-tree SAT
abstraction without making the invalid assumption that same-colour
blocks factor inside a forbidden coefficient.

## Exclusive-cut corollary

There is a useful three-colour consequence.  Suppose the three full
hafnians are nonzero and every mixed complementary product vanishes:

```text
haf(Z^c[A]) haf(Z^d[V-A]) = 0
for c != d and every nontrivial even A.                (4)
```

Fix a size `2k`.  By (1), for each colour `c` there is some `A_c` with

```text
haf(Z^c[A_c]) != 0,
haf(Z^c[V-A_c]) != 0.                                 (5)
```

At that same cut, both factors for every other colour `d` vanish.
Indeed, applying (4) in the two orientations gives

```text
haf(Z^d[A_c]) haf(Z^c[V-A_c]) = 0,
haf(Z^c[A_c]) haf(Z^d[V-A_c]) = 0,
```

and the colour-`c` factors in (5) are nonzero.  Thus every intermediate
size has three colour-exclusive complementary cuts.  The cuts for
different colours are necessarily distinct.

At `k=1`, every colour has a saturated diagonal edge `e_c` satisfying

```text
Z^c[e_c] != 0,
haf(Z^c[V-e_c]) != 0,

Z^d[e_c] = 0,
haf(Z^d[V-e_c]) = 0          for every d != c.         (6)
```

So each colour admits a selected monochromatic matching through an edge
that is absent from the other two zero-layer colour supports, while both
other complementary cofactors vanish.  This conclusion has no
support-degree or selected-matching-disjointness hypothesis.

Condition (4) holds in a hypothetical balanced all-bridge witness:
otherwise the corresponding two-colour zero-layer coefficient would be
nonzero.  Therefore the exclusive cuts in (5)--(6) are an
arbitrary-order necessary condition for every remaining all-bridge case.

## Verification

Run:

```text
python claims/arbitrary-order/verify_hafnian_convolution_split.py
python claims/arbitrary-order/audit_hafnian_convolution_split.py
```

The primary verifier expands every convolution term through order 12,
counts each perfect-matching monomial, and checks the finite support
logic behind the exclusive-cut corollary.  The independent audit starts
from each full matching and chooses edge subsets directly.  Both recover
the exact coefficient `binomial(m,k)` for every `m <= 6`; the proofs
above are arbitrary-order.

## Boundary

The all-size split axiom does not itself prove that three such families
must be compatible.  The corrected order-12 complement-profile SAT
experiment uses it as an additional necessary condition; that
exploratory decision remains separate from this proved identity.
