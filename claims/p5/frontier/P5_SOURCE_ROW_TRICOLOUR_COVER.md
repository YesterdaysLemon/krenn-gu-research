# `P_5` source-row tricolour cover

## Status

This is an exact global structural theorem over `C`.  It strengthens the
kernel Hall hierarchy at the previously untreated singleton boundary:

```text
for every source row p and every target colour c,
some local map has row p proportional to e_c^*.          (1)
```

Consequently the five local maps in a hypothetical restriction
`P_5 -> Delta_3` contain at least 15 coordinate rows in total, and at
least one local map contains at least three coordinate rows.

This destroys the earlier 11-coordinate-row support survivor.  It does
not by itself exclude all coefficient-level configurations and is not
yet a complete solution of the Krenn--Gu conjecture.

## The missing-row identity

Suppose injective maps

```text
phi_i : C^3 -> C^5,  i=0,...,4,
```

pulled the order-five permanent tensor back to

```text
P_5(phi_0(x_0),...,phi_4(x_4))
  = sum_(c=0)^2 lambda_c product_(i=0)^4 x_i[c],
lambda_c != 0.                                         (2)
```

Let

```text
r_(i,p) = e_p^* composed with phi_i,
K_(i,p) = ker r_(i,p).                                 (3)
```

Fix a source row `p` and restrict every `x_i` to `K_(i,p)`.  Every
source vector `phi_i(x_i)` then has zero coordinate `p`.  Five such
vectors live on only four source coordinates, so every permanent
monomial vanishes.  Equation (2) therefore gives the tensor identity

```text
sum_(c=0)^2 lambda_c
  tensor_(i=0)^4 (e_c^* restricted to K_(i,p)) = 0.    (4)
```

The colour-`c` decomposable term in (4) is zero exactly when some
`r_(i,p)` is a nonzero multiple of `e_c^*`.  Indeed,
`e_c^*` vanishes on `ker r_(i,p)` exactly when it belongs to the line
spanned by `r_(i,p)`.

## Three decomposable tensors cannot cancel here

We use the elementary rank-one dependence fact:

> If three nonzero decomposable tensors of order at least two are
> linearly dependent, then, outside at most one tensor mode, their
> three local factors are all proportional.

To see this, write the third tensor as a nontrivial linear combination
of the first two.  If the first two have independent local factors in
two different modes, flattening across either one of those modes has
matrix rank two, whereas a decomposable tensor has rank one.  Thus the
first two differ projectively in at most one mode.  Their common factor
can be removed in every other mode, forcing the third factor there to
be proportional as well.

Now classify the number of nonzero terms in (4).

- Three nonzero terms cannot cancel.  The dependence fact would make
  all three restricted coordinate functionals proportional in at least
  four modes.  But they span `K_(i,p)^*`, whose dimension is two when
  `r_(i,p)` is nonzero and three when it is zero.
- If exactly two terms survived, they would be proportional factor by
  factor.  The missing third colour, say `c`, is killed in some mode
  with `r_(i,p)` proportional to `e_c^*`.  On the plane `x[c]=0`, the
  other two coordinate functionals are independent, a contradiction.
- One nonzero decomposable tensor cannot equal zero.

Therefore no term survives: each of the three colours is killed in at
least one mode.  This proves (1).

## Consequences

For a fixed source row, the three required coordinate rows occupy three
different modes.  Repeating this for all five source rows forces

```text
5 source rows * 3 colours = 15
```

distinct coordinate-row cells in the `5 x 5` mode/source array.  By
pigeonhole, one of the five local maps has at least three coordinate
rows.

This strictly strengthens the earlier pair-cover dichotomy.  In
particular, it is no longer enough for the global configuration merely
to contain one axial `4+1` map: coordinate rows of every colour must
cover every source position across the full five-mode array.

## Verification

Run:

```text
python claims/p5/frontier/verify_p5_source_row_tricolour_cover.py
python claims/p5/frontier/audit_p5_source_row_tricolour_cover.py
```

The primary verifier reconstructs the three possible nonempty-term
cases and the 15-cell count.  The independent audit enumerates all
8,568 multisets of five zero-or-projective row covectors over `F_3`
and all four nonzero diagonal coefficient ratios.  Every vanishing
restricted diagonal tensor contains all three coordinate covectors,
exactly as the complex proof requires.

## Boundary

Support incidence alone still admits rare architectures with 20
coordinate rows and no mixed coefficient supported on a unique
permutation.  A first such architecture is nevertheless excluded by an
odd triangle of two-term cancellation equations.  The next exact task
is to make that signed-cancellation obstruction exhaustive over the
finite coordinate-row architectures forced by (1).
