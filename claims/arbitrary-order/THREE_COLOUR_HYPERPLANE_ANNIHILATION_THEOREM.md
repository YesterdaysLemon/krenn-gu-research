# Three-colour hyperplane-annihilation theorem

## Theorem

Let `m >= 2`, let `V = C^3`, and for each `u=1,...,m` let
`H_u` be a linear subspace of `V` of dimension at least two.  On
`H_1 x ... x H_m`, consider the restriction of

```text
G(y_1,...,y_m)
  = sum_(c=0)^2 product_(u=1)^m y_u[c].
```

Then `G` vanishes identically if and only if, for every colour `c`,
there is an index `u` such that

```text
H_u subset {y in C^3 : y[c] = 0}.
```

Because `dim(H_u) >= 2`, such an inclusion forces `H_u` to be exactly
that coordinate hyperplane.

The result is special to three summands.  Its point here is that complex
cancellation cannot create any additional way for the three-colour GHZ
form to vanish on a product of hyperplanes.

## Proof

Write `p_(u,c)` for the restriction to `H_u` of the `c`-th coordinate
functional.  The restricted tensor is

```text
T = tensor_u p_(u,0)
  + tensor_u p_(u,1)
  + tensor_u p_(u,2).
```

The reverse implication is immediate: if each colour `c` has some factor
with `p_(u,c)=0`, all three displayed decomposable tensors vanish.

For the forward implication, first suppose all three decomposable tensors
are nonzero.  We use the elementary fact that a sum of two nonzero
decomposable tensors is decomposable only if the two summands have
proportional factors in all but at most one tensor mode.  Indeed, if two
modes both contain independent factor pairs, flattening across those two
modes and applying suitable linear functionals in all remaining modes
produces a rank-two matrix, whereas a decomposable tensor has matrix rank
one.

Since the negative of the third summand is the sum of the first two, all
but at most one modes therefore have

```text
p_(u,0), p_(u,1), p_(u,2)
```

proportional.  This is impossible: the three coordinate functionals
restricted to `H_u` span `H_u^*`, whose dimension is at least two.

Next suppose exactly one of the three decomposable tensors is zero, say
the colour-2 tensor.  Some `p_(w,2)` is then zero.  Thus `H_w` is the
coordinate plane `y[2]=0`, on which `p_(w,0)` and `p_(w,1)` are linearly
independent.  But the two remaining nonzero decomposable tensors must be
negatives of one another, which forces their factors to be proportional
in every mode, including mode `w`.  This is again impossible.

If exactly two summands are zero, the remaining nonzero summand cannot
sum to zero.  Consequently all three summands must be zero, which is
precisely the asserted coordinate-hyperplane condition.

## Consequence for a hypothetical quantum graph

Fix a vertex `v` and contract its colour index against a vector
`x in C^3` with all coordinates nonzero.  For each neighbour `u`, define
the row functional

```text
a_u(x) = transpose(x) W_(v,u).
```

Independently restrict the colour vector at `u` to `ker(a_u(x))`.
Every perfect-matching channel pairs `v` with some `u`, so every channel
vanishes.  The target contraction is

```text
sum_(c=0)^2 x[c] product_(u != v) y_u[c].
```

Rescaling one factor absorbs the three nonzero coefficients `x[c]`.
The theorem says that, for each colour `c`, some neighbour `u` must obey

```text
a_u(x) is a nonzero multiple of e_c.
```

There are only finitely many neighbours.  As `x` ranges over a Zariski
open subset of `C^3`, a finite union of proper linear subspaces cannot
cover that open set.  Hence, for each `(v,c)`, one fixed incident block
works identically in `x`.  Equivalently,

```text
W_(v,u)[:,j] = 0  for every j != c,
W_(v,u)[:,c] != 0.
```

Thus every vertex and colour has a genuine column-killer edge.  Applying
the transposed statement at the other endpoint gives the corresponding
row-killer form.

This is a structural reduction only.  It does not by itself prove that
the required killer edges can be chosen compatibly throughout the graph,
and it does not resolve the global Krenn--Gu conjecture.
