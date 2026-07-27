# `P_5` coordinate-plane pair cover

## Status

This is an exact global structural theorem over `C`.  For every one of
the ten pairs of source coordinates, it forces at least one local map
to span a target coordinate plane on that row pair.  Combined with the
five-row projective normal forms, it gives the dichotomy

```text
every hypothetical P_5 -> Delta_3 restriction contains either

1. a local map with at least two coordinate rows, or
2. an axial 4+1 local map:
   four rows supported on the same two target colours and
   one coordinate row supported on the third colour.     (1)
```

This is not yet an exclusion of the two displayed branches and is not
a complete solution of the Krenn--Gu conjecture.

## Common-pair obstruction

Suppose injective maps

```text
phi_i : C^3 -> C^5,  i=0,...,4,
```

pulled the order-five permanent tensor back to

```text
sum_(c=0)^2 lambda_c e_c tensor 5,  lambda_c != 0.      (2)
```

Let

```text
r_(i,s) = e_s^* composed with phi_i,
K_i(p,q) = ker r_(i,p) intersect ker r_(i,q).           (3)
```

The support-at-most-three contraction theorem says that every nonzero
vector in `K_i(p,q)` has a zero target coordinate.  Since a linear
subspace over `C` cannot be covered by three proper subspaces,
`K_i(p,q)` lies in a target coordinate hyperplane.

For fixed `p,q`, define its active-colour set in mode `i` by

```text
A_i(p,q) = {c : some t in K_i(p,q) has t[c] != 0}.      (4)
```

Every `A_i(p,q)` is nonempty and has size at most two.

No colour can be active in four modes.  If `c` were active in modes
`I`, with `|I|=4`, choose `t_i in K_i(p,q)` with `t_i[c] != 0` for
`i in I`, and use `e_c` in the fifth mode.  The target value in (2)
would be

```text
lambda_c product_(i in I) t_i[c] != 0.                 (5)
```

On the source side, the four vectors `phi_i(t_i)` all vanish in source
coordinates `p,q`.  A permanent permutation cannot inject four modes
into the remaining three coordinates, so the source value is zero.
This contradicts (2).

Therefore every target colour belongs to at most three of the five
sets in (4).  If all five active sets had size two, they would contain
ten colour incidences, while three colours used at most three times
provide room for only nine.  Hence some `A_i(p,q)` is a singleton
`{c}`.  Then

```text
K_i(p,q) = <e_c>,
span(r_(i,p),r_(i,q)) = <e_d^* : d != c>.              (6)
```

The second equality is annihilator duality.  It proves the main pair
cover statement:

> For every source pair `p,q`, at least one local map has those two
> rows spanning one of the three target coordinate planes.

Equivalently, if `C_i` is the set of coordinate-plane row pairs in
mode `i`, then

```text
C_0 union C_1 union C_2 union C_3 union C_4 = E(K_5).  (7)
```

## Combining the local normal forms

Assume first that no local map has two coordinate rows.  Each mode is
then either line type or quadrangle type.

A quadrangle-type map has no coordinate-plane row pair.  Every side
through two quadrangle vertices contains exactly one coordinate point,
not a coordinate line; a line through its unique coordinate row and a
quadrangle vertex likewise contains no second coordinate point.  Thus

```text
|C_i| = 0.                                             (8)
```

For a line-type map, let its unique coordinate row be `E_c` and let
the other four rows lie on a projective line `L` not containing `E_c`.

- If `L` is a coordinate line, it is the line through the other two
  coordinate points.  Its six pairs of non-coordinate rows span that
  coordinate plane, and no pair involving `E_c` does.  Hence
  `|C_i|=6`.  This is the **axial** case.
- If `L` is not a coordinate line, it contains exactly one coordinate
  point `E_a`.  Pairs among its four rows do not span a coordinate
  plane.  Of the two coordinate lines through `E_c`, the line
  `E_cE_a` meets `L` at the excluded coordinate point `E_a`; only the
  other can meet `L` at a non-coordinate row.  Consequently
  `|C_i|<=1`.

If no mode were axial, (8) and the last bound would give

```text
|C_0 union ... union C_4| <= 5,
```

contradicting the ten-edge cover (7).  Thus, in the absence of a map
with two coordinate rows, an axial line-type map is forced.

After source and target coordinate permutations, an axial map has the
support form

```text
[ *  *  0 ]
[ *  *  0 ]
[ *  *  0 ]    with both displayed entries nonzero,
[ *  *  0 ]
[ 0  0  * ].                                            (9)
```

This is exactly the `4+1` alternative in (1).

## Verification

Run:

```text
python verify_p5_coordinate_plane_pair_cover.py
python audit_p5_coordinate_plane_pair_cover.py
```

The primary verifier exhausts all `6^5=7,776` five-tuples of nonempty
active-colour sets of size at most two, checks the four-mode
obstruction, reconstructs the three local normal-form pair counts, and
checks all `5!=120` permanent assignments in (5).  The independent
`F_7` audit enumerates every projective line relevant to an exact-one-
coordinate line configuration and every four-point choice on it,
confirming pair-count `6` for axial lines and at most `1` otherwise.

## Boundary

The remaining two cases in (1) are genuinely more degenerate than the
quadrangle and generic-line strata.  In the axial case, (7) assigns the
six pairs among the four-row block to that mode and forces the other
four modes to cover the four remaining star pairs.  This provides the
next finite incidence interface for the mixed-row permanent equations.
