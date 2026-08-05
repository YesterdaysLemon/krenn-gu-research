# Principal hafnian cofactors are locally algebraically independent

## Status

**Exact arbitrary-order characteristic-zero structural theorem.**  Let
`H_(2m)` be the scalar hafnian of the generic symmetric zero-diagonal
`2m x 2m` matrix, with `m>=2`.  Send its edge variables to all principal
two-vertex cofactors:

```text
Phi=(partial H_(2m)/partial w_ij)_(i<j).
```

At the point supported with weight one on one fixed perfect matching and
weight zero on every other edge, the Jacobian determinant of `Phi` is

```text
(-1)^(m-1) (m-1).                                  (1)
```

It is nonzero in characteristic zero.  Hence `Phi` is etale at that point
and dominant.  In particular, principal scalar hafnian cofactors satisfy no
nonzero polynomial relation, and every sufficiently small complex
perturbation of the displayed cofactor array is realized by nearby scalar
edge weights.

Applied independently to the three diagonal entries of every `3 x 3` edge
block, this shows that diagonal complementary-cofactor data alone cannot
obstruct the root-tangent quotient frames.  The missing global condition
must use mixed-colour cancellation, simultaneous off-diagonal tensors,
higher jets, or other graph incidence.

This does not realize a GHZ matching tensor: the diagonal edge blocks
constructed from three scalar graphs generally have nonzero mixed-colour
matching coefficients.  It is a no-go theorem for a narrower proof route,
not a counterexample.  The global Krenn--Gu conjecture remains
**UNRESOLVED**.  No finite field is used.

## The matching point

Number the vertices `0,...,2m-1` and fix

```text
p_a={2a,2a+1},             a=0,...,m-1.            (2)
```

Let `x` be the edge-weight point with `w_(p_a)=1` and all other edge weights
zero.  The coordinates of `Phi` are

```text
Phi_e=H_(2m-2)(V\e),                               (3)
```

the hafnians after deleting the endpoints of `e`.

For two edges `e,f`, the Jacobian entry at `x` is zero if the edges meet.
If they are disjoint, it is

```text
J_(e,f)=H_(2m-4)(V\(e union f)) evaluated at x.    (4)
```

At `x`, equation (4) is one exactly when the four deleted vertices form the
union of two matching pairs in (2); otherwise it is zero.

## Exact block decomposition

There are two kinds of Jacobian blocks.

First index the `m` matching edges themselves.  Any two distinct such edges
delete two complete matching pairs, while the diagonal entries vanish.
Their block is

```text
J_m-I_m,                                           (5)
```

with determinant `(-1)^(m-1)(m-1)`.

Now fix two matching pairs `p_a,p_b`.  The four cross edges between their
vertices split into the two complementary pairs

```text
{(2a,2b),(2a+1,2b+1)},
{(2a,2b+1),(2a+1,2b)}.                             (6)
```

Each pair gives the block

```text
[0 1]
[1 0].                                             (7)
```

Cross edges belonging to different pair-pairs do not interact at `x`, and
there are no entries between (5) and (7).  There are
`2*binomial(m,2)=m(m-1)` swap blocks.  Their determinant product is one
because `m(m-1)` is even.  Multiplying by (5) proves (1).

The source and target of `Phi` both have `binomial(2m,2)` coordinates, so
the nonzero Jacobian determinant proves etaleness and dominance.

## Three-colour diagonal corollary

Choose three independent scalar edge systems `w^(0),w^(1),w^(2)` and put

```text
W_ij=diag(w_ij^(0),w_ij^(1),w_ij^(2)).             (8)
```

On the all-colour-`c` input, every matching uses only the `c`th diagonal
entry, so its principal cofactor array is exactly `Phi(w^(c))`.  The product
map `Phi^3` is dominant.  Therefore a Zariski-open set of triples of
diagonal principal-cofactor arrays, including independent perturbations
needed to frame a two-dimensional diagonal quotient, is realizable by
honest symmetric edge blocks.

Equation (8) does not cancel mixed colour words.  Thus the corollary removes
only a diagonal-cofactor algebraic-relation route; it does not solve the
simultaneous GHZ equations.

## Boundary

```text
scalar principal-cofactor gradient dominance: PROVED for every m>=2;
three independent diagonal cofactor arrays: LOCALLY REALIZABLE;
mixed-colour coefficient cancellation: UNKNOWN;
simultaneous tangent and higher-jet graph realization: UNKNOWN;
full arbitrary-order local-to-global reduction: UNKNOWN;
global Krenn--Gu conjecture: UNRESOLVED.
```

In positive characteristic dividing `m-1`, the displayed matching point is
not an etale certificate.  No claim is made there.

## Replay

```powershell
uv run --with sympy python verify_hafnian_principal_cofactor_gradient_dominance.py
python audit_hafnian_principal_cofactor_gradient_dominance.py
```

The primary differentiates the exact six-vertex hafnian symbolically and
checks the arbitrary-order block ledger and exact determinants through
twenty vertices.  The no-import audit reconstructs the second cofactors by
an independent anchored matching recurrence and checks integer determinants
through twelve vertices.
