# Exact three-blocker permanent-rank lemma

## Status

This is an arbitrary-order refinement of the multi-star exact-blocker
factorisation.  For three zero-coupled roots with exactly three blockers,
the full root--blocker tensor cannot have all three diagonal colours
active.

It is a structural reduction, not a global contradiction.

## Setup

Let `R={r_0,r_1,r_2}` be three roots carrying vectors `x_i in C^3`.
Assume

```text
B_(r_i,r_j)(x_i,x_j)=0 for i != j,
x_i[d] != 0 for every root i and every colour d
```

and fix a colour `c`.  At every outside vertex `u`, let `A_u` be the span
of the three root covectors

```text
z -> B_(r_i,u)(x_i,z).
```

Suppose the colour-`c` blocker lower bound is tight: exactly three
outside vertices `U={u_0,u_1,u_2}` have `e_c^* in A_u`.

The multi-star exact-factorisation theorem gives a nonzero residual
tensor `H_res`, and the full identity has the form

```text
F_U H_res = sum_(d=0)^2 X_d D_d R_d,                  (1)
```

where

```text
X_d = product_i x_i[d],
D_d = product_(u in U) z_u[d],
R_d = product over residual kernel modes of coordinate d.
```

Moreover `H_res` is a nonzero multiple of `R_c`.  Consequently every
nonzero `R_d` is proportional to `R_c`, and

```text
F_U = gamma_0 D_0 + gamma_1 D_1 + gamma_2 D_2,        (2)
```

with `gamma_c != 0`.

## Theorem

At least one of the two residual coordinate products with `d != c`
vanishes:

```text
R_d = 0 for some d != c.                              (3)
```

Equivalently, the diagonal tensor in (2) has at most two nonzero
coefficients.

## Proof

For each blocker `u_j`, collect its three root covectors into the linear
map

```text
M_j : C^3 -> C^3.
```

Pairing the three roots bijectively with the three blockers gives

```text
F_U(z_0,z_1,z_2)
  = sum_(sigma in S_3)
      product_(i=0)^2 (M_(sigma(i)) z_(sigma(i)))[i].
```

Thus `F_U` is obtained from the standard order-three permanent tensor

```text
P_3 = sum_(sigma in S_3)
        e_(sigma(0)) tensor e_(sigma(1)) tensor e_(sigma(2))  (4)
```

by applying the local maps `M_0,M_1,M_2`.

Suppose all three coefficients in (2) were nonzero.  Then every
one-mode flattening of `F_U` would have rank three.  Hence every local
map `M_j` must have rank three and is invertible.  Local invertible maps
preserve tensor rank, so

```text
rank_tensor(F_U) = rank_tensor(P_3).                  (5)
```

The tensor `P_3` has rank four.  For the lower bound, its first-mode
slice space is

```text
{ [0 z y; z 0 x; y x 0] : x,y,z in C }.              (6)
```

This space contains no nonzero rank-one matrix.  Indeed, its three
principal `2 x 2` minors are `-z^2,-y^2,-x^2`; rank at most one forces
`x=y=z=0`.

If `P_3` had tensor rank three, its rank-three one-mode flattenings would
force the three factors in every mode of a minimal three-term
decomposition to be linearly independent.  Its slice space would then
be spanned by, and in particular contain, three nonzero rank-one
matrices.  This contradicts (6).

For completeness, rank four is attained by the polarization identity

```text
P_3 = 1/4 (
    (e_0+e_1+e_2) tensor 3
  - (e_0+e_1-e_2) tensor 3
  - (e_0-e_1+e_2) tensor 3
  - (-e_0+e_1+e_2) tensor 3 ).                        (7)
```

On the other hand, the diagonal tensor in (2), with all three
coefficients nonzero, has tensor rank exactly three: its flattening rank
is three and its displayed diagonal expression has three terms.  This
contradicts (5), so at most two diagonal coefficients are active.

Because `X_d != 0` for a fully supported root triple and a nonzero
`R_d` would create a nonzero diagonal coefficient in (1), one of the
two residual products outside colour `c` must vanish.  This proves (3).

## Consequence for root promotion

Suppose a nonblocker of an exact root pair is placed in its simultaneous
kernel and promoted to a third root.  If the enlarged triple has exactly
three colour-`c` blockers, deleting those roots and blockers cannot leave
all three residual coordinate products active.  Some residual kernel
space is contained in another coordinate hyperplane, exposing a blocker
for that other colour relative to the enlarged root set.

This supplies a rank obstruction in the equality case of the promotion
step.  A surplus fourth blocker is the other alternative.

## Verification

Run:

```text
python claims/arbitrary-order/verify_exact_three_blocker_permanent_rank.py
python claims/arbitrary-order/audit_exact_three_blocker_permanent_rank.py
```

The primary verifier constructs (4), checks all flattening and slice
ranks symbolically, verifies the four-term polarization identity, and
checks that a three-term diagonal has rank three.  The independent audit
repeats the slice-space and polarization calculations over `F_5`,
exhausting all 124 nonzero slice combinations.  The written theorem is
over `C`.

## Boundary

The proof concerns exactly three roots and exactly three blockers.  It
does not exclude a fourth blocker, nor does it by itself propagate the
new residual blocker back to the original root pair.
