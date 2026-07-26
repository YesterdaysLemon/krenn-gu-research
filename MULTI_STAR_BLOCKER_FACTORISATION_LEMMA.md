# Multi-star blocker and exact-factorisation lemma

## Status

This is an arbitrary-order strengthening of the double-star annihilation
argument.  It applies directly to every hypothetical Krenn--Gu witness.

It proves a blocker-surplus versus exact-reduction dichotomy.  It does
not by itself exclude the deeper-blocker branch or prove the global
conjecture.

## Setup

Let `R` be a set of `r >= 2` root vertices in an even `n`-vertex
instance, with `R` a proper subset of the vertex set.  Fix one colour
`c` and root vectors `x_i in C^3`, `i in R`, such that

```text
x_i[c] != 0                                              (1)
```

and every internal root edge vanishes:

```text
B_ij(x_i,x_j) = 0 for all distinct i,j in R.             (2)
```

For every outside vertex `u`, let

```text
a_(i,u)(z) = B_iu(x_i,z),
A_u = span{a_(i,u) : i in R} subset (C^3)*,
K_u = intersection_(i in R) ker(a_(i,u)).
```

Call `u` a colour-`c` blocker for `R` when

```text
e_c^* belongs to A_u.                                    (3)
```

Equivalently, `K_u` is contained in the coordinate plane `z[c]=0`.

## Blocker lower bound

**Theorem.**  There are at least `r` distinct colour-`c` blockers
outside `R`.

Suppose instead that there are `b < r`.  At every nonblocker `u`,
linear duality gives a vector

```text
z_u in K_u with z_u[c] != 0.                             (4)
```

Put `z_u=e_c` at each blocker.  If there is no blocker, choose one
arbitrary outside vertex as a marker and put `z_u=e_c` there instead.
The number of exceptional outside vertices is then strictly smaller
than `r`.

In any perfect matching, an internal root pair has zero weight by (2).
Thus all `r` roots would have to use distinct outside vertices.  One of
those outside vertices is nonexceptional, and its incident root edge
has zero weight by (4).  Every perfect-matching monomial therefore
vanishes.

At least one outside vector is `e_c`, so the other two GHZ products
vanish.  The colour-`c` product is nonzero by (1) and (4), a
contradiction.

In particular, a zero-coupled root set satisfying (1) cannot have more
than `n/2` vertices.

## Exact-blocker factorisation

Suppose the blocker lower bound is tight: there are exactly `r`
blockers, forming a set `U`.

For each `u in U`, put `z_u=e_c`.  For every remaining outside vertex
`w`, allow `z_w` to vary in `K_w`.  Define the `r x r` root--blocker
matrix

```text
C_(i,u) = B_iu(x_i,e_c),   i in R, u in U.              (5)
```

Every surviving perfect matching must pair the roots bijectively with
the blockers.  A root--root edge vanishes by (2), and a root--nonblocker
edge vanishes on `K_w`.  If two blockers were paired together, too few
blockers would remain for all roots.  Therefore the full matching
contraction factors exactly as

```text
per(C) H_(V minus (R union U))((z_w)_w).                 (6)
```

The target contraction is

```text
(product_(i in R) x_i[c])
(product_(w notin R union U) z_w[c]).                   (7)
```

The equality first holds on the dense product locus where every
`z_w[c]` is nonzero and then, by polynomiality, on the full product of
the spaces `K_w`.  Consequently

```text
per(C) != 0                                             (8)
```

and the residual matching tensor restricts to the pure product

```text
H_(V minus (R union U))((z_w)_w)
  = (product_(i in R) x_i[c]) / per(C)
    * product_w z_w[c].                                 (9)
```

There is a stronger full-tensor conclusion.  Let

```text
F_U((z_u)_u)
  = per([B_iu(x_i,z_u)]_(i in R,u in U)),

D_d((z_u)_u) = product_(u in U) z_u[d],
R_d((z_w)_w) = product_(w notin R union U) z_w[d],
X_d = product_(i in R) x_i[d].
```

Keep every nonblocker vector in its simultaneous kernel, but now allow
the blocker vectors to vary arbitrarily.  The same matching
classification gives the tensor identity

```text
F_U H_(V minus (R union U))
  = sum_(d=0)^2 X_d D_d R_d.                           (10)
```

Equation (9) says that the residual factor on the left is `h R_c` for
some `h != 0`.  The three blocker tensors `D_0,D_1,D_2` are linearly
independent.  Consequently, for every `d` with `X_d != 0`, there is a
scalar `rho_d` such that

```text
R_d = rho_d R_c,   with rho_c=1,                       (11)
```

and

```text
F_U = h^(-1) sum_(d=0)^2 X_d rho_d D_d,                (12)
```

where a term with `X_d=0` is omitted.  Thus the
root--blocker permanent tensor has no mixed-colour coefficient at all.
If every root vector has all three coordinates nonzero, all three
residual colour-product tensors are zero or collinear, and `F_U` is a
three-term diagonal GHZ tensor on the blocker variables.

For two roots and exactly two blockers, (12) says explicitly that

```text
B_pu(x,z_u) B_rv(y,z_v)
  + B_pv(x,z_v) B_ru(y,z_u)
```

has zero coefficient on every `z_u[a]z_v[b]` with `a != b`, while its
`z_u[c]z_v[c]` coefficient is nonzero.  This is a concrete algebraic
constraint on the minimal-surplus deeper-blocker branch.

Thus every zero-coupled root set gives the exact alternative:

1. it has at least `r+1` blockers; or
2. it has exactly `r` blockers, their root--blocker permanent is
   nonzero, deleting the roots and blockers leaves a forced pure
   colour-`c` tensor on the simultaneous kernel spaces, and the full
   tight-case tensor obeys (10)--(12).

For `r=2`, this sharpens the existing double-star theorem: every
deeper root pair has either a third blocker or an exact `2 x 2`
permanent reduction to an `(n-4)`-vertex pure minor.

## Verification

Run:

```text
python verify_multi_star_blocker_factorisation.py
python audit_multi_star_blocker_factorisation.py
```

The primary verifier enumerates every perfect matching through order 12
and checks that, under the zero pattern used in the proof, the surviving
matchings are exactly the Cartesian product of a root--blocker
bijection and a residual perfect matching.  It also checks the
coefficient-level rank-one implication in (10)--(12).  The independent
audit builds that Cartesian product directly, compares it with a
separate dynamic-programming count, and reconstructs the tensor
coefficient argument from independent symbolic labels.  The written
proof is arbitrary-order.

## Boundary

For three-dimensional local spaces, blocker membership becomes
automatic when the root covectors span the full dual space.  The useful
new content is therefore the exact-surplus dichotomy, especially at
`r=2`, rather than an expectation that arbitrarily large root sets can
always be constructed.

The next analytic task is to combine the forced pure residual tensor in
(9) with the local killer flags inside that residual minor, or to show
that persistent blocker surplus is incompatible with finite incidence.
