# At most one residual endpoint forces two axis types in the full root jet

## Status

**Exact arbitrary-order characteristic-zero topology theorem.**  Let
`r>=2` fully supported pairwise-zero roots of a hypothetical three-colour
GHZ graph witness have projectively constant root--blocker first derivatives.
In logarithmic coordinates, restrict root `i` to

```text
S_i=ker(a_i),                 a_i(1,1,1) != 0,          (1)
```

so every differentiated root--blocker edge vanishes.  Suppose that among all
fixed nonblocker vertices there is at most one vertex having a nonzero
one-tangent contraction with any `S_i`.  Allow completely arbitrary
tangent--tangent edges between roots.

Then the tangent covectors `{a_i}` contain at least two distinct coordinate
axis types.  In other words, there are roots `i,j` and different coordinates
`c!=d` such that

```text
a_i is projectively e_c^*,       a_j is projectively e_d^*.    (2)
```

If there is no effective nonroot endpoint and `r` is odd, all three
coordinate-axis types must occur.

This removes the all-nonaxis and one-axis escape routes with zero or one
residual endpoint even when every root--root tangent channel is available.
It does not exclude the surviving two-/three-axis patterns, two or more
effective residual endpoints, nonprojective root--blocker variation, or the
actual cofactor identities.  The arbitrary-order local-to-global reduction
and the global Krenn--Gu conjecture remain **UNRESOLVED**.  No finite field is
used.

## One deletion set on the graph side

Differentiate once at every root and restrict the derivative at root `i` to
`S_i`.  A surviving matching cannot use a root--blocker edge.  It can only
pair roots to one another or to an effective fixed nonblocker endpoint.

If `r` is even, the unique possible endpoint cannot be used: using it once
would leave an odd number of roots to pair internally.  Every surviving term
therefore deletes exactly the root set `R`.  All root-pair matchings multiply
the same complementary matching tensor `C_R`.

If `r` is odd, a surviving term must use the unique endpoint `q` exactly
once.  Every such term deletes exactly `R union {q}` and multiplies the same
complementary tensor `C_(R union {q})`.  If no effective endpoint exists,
there is no surviving term.

Consequently the complete graph-side full-root derivative has tensor-image
rank at most one.  This conclusion allows every root--root bilinear
restriction and every cancellation among the scalar matching forms.  It is
stronger here than merely taking quotient classes modulo the original GHZ
diagonal: there is only one actual complementary deletion tensor.

## Rank of the full GHZ jet

For each coordinate `c`, let

```text
l_(i,c)=e_c^* restricted to S_i,
F_c=tensor_(i in R) l_(i,c).                           (3)
```

Up to nonzero diagonal coefficients, the full-root GHZ derivative is the map
whose three coefficient forms are `F_0,F_1,F_2`.  Since the three diagonal
target tensors are independent, its tensor-image rank is

```text
dim span{F_0,F_1,F_2}.                                (4)
```

A decomposable form `F_c` is zero exactly when one factor `l_(i,c)` is zero.
Both `S_i` and `ker(e_c^*)` are hyperplanes, so

```text
F_c=0
  iff some S_i=ker(e_c^*)
  iff some a_i is projectively e_c^*.                 (5)
```

Suppose first that exactly one form, say `F_c`, is zero.  Choose an axis-`c`
root `i`.  On `S_i=ker(e_c^*)`, the other two coordinate restrictions
`l_(i,p),l_(i,q)` are linearly independent.  Therefore the nonzero pure
tensors `F_p,F_q` cannot be proportional, and (4) has rank two.

If none of the `F_c` vanishes, rank at most one would make all three nonzero
pure tensors proportional.  Equality of nonzero decomposable tensors forces
their factors to be proportional at every root.  Thus, for each `i`, the
three restrictions

```text
l_(i,0), l_(i,1), l_(i,2)                             (6)
```

would all lie on one line.  But they span `S_i^*`, which has dimension two.
This is impossible.

Hence (4) has rank at most one exactly when at least two of the `F_c` vanish,
which by (5) is exactly the two-axis conclusion (2).  If the graph derivative
is zero, all three `F_c` must vanish, giving all three axis types.  Combining
this with the odd/no-endpoint parity case proves the theorem.

## Relation to the existing jet frontier

The earlier matching-saturation theorem only asks for one effective matching
on an axis-deficient subset.  Here every full-root matching may exist, but
zero/one endpoint parity makes all of them share one deletion cofactor.  The
cofactor-span obstruction therefore sees information that support saturation
alone discards.

In particular, the uniform balanced resonance

```text
a_i=e_p^*+e_q^*       for every i                         (7)
```

is impossible with at most one effective residual endpoint, regardless of
the parity law of its quotient jet and regardless of how densely the roots
are joined.  Any all-nonaxis survivor must instead use at least two effective
nonroot endpoints or escape projective root--blocker variation.

At order twelve, a five-root/six-blocker first-surplus configuration has
exactly one residual vertex.  Therefore every projectively constant tangent
lift of that `P_6` slice must contain at least two coordinate-axis tangent
types, even when all root--root tangent blocks are retained.  This is a
necessary condition on the maximal-overlap order-twelve cores, not a
nonrestriction theorem for `P_6`.

## Replay

```powershell
uv run --with sympy python verify_root_at_most_one_endpoint_full_jet_axis_necessity.py
python audit_root_at_most_one_endpoint_full_jet_axis_necessity.py
uv run --with sympy --with ruff python -m ruff check verify_root_at_most_one_endpoint_full_jet_axis_necessity.py audit_root_at_most_one_endpoint_full_jet_axis_necessity.py
python -m py_compile verify_root_at_most_one_endpoint_full_jet_axis_necessity.py audit_root_at_most_one_endpoint_full_jet_axis_necessity.py
```

The primary reconstructs the exact full coefficient-form rank on all small
projective covector tuples through four roots and audits endpoint parity
through twelve roots.  The no-import audit uses a different integer kernel,
rational row reduction, a wider covector box, and an independent recursive
matching count.  These bounded calculations audit the indexing and rank
criterion; the decomposable-tensor and parity arguments above prove the
arbitrary-order statement.
