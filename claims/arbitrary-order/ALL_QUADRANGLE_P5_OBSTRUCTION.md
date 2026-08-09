# All-quadrangle `P_5` obstruction

## Status

This is an exact global branch obstruction over `C`.  Combined with the
five-row projective normal-form theorem, it proves:

```text
in a hypothetical restriction P_5 -> Delta_3,
not all five local maps can have quadrangle type.       (1)
```

Consequently at least one local map must either have two coordinate
rows or have the one-coordinate line type.  This does not yet exclude
those two remaining branches and is not a complete solution of the
Krenn--Gu conjecture.

The later
[`P5_COORDINATE_PLANE_PAIR_COVER.md`](../../P5_COORDINATE_PLANE_PAIR_COVER.md)
strengthens this: every one of the ten source pairs must span a
coordinate plane in some mode, forcing either a multiple-coordinate-row
map or an axial `4+1` line map.

## Setup

Write the order-five permanent form as

```text
P_5(z_0,...,z_4)
  = sum_(sigma in S_5) product_(i=0)^4 z_i[sigma(i)].
```

Suppose, for a contradiction, that injective maps

```text
phi_i : C^3 -> C^5
```

pull it back to a concise diagonal tensor:

```text
P_5(phi_0(x_0),...,phi_4(x_4))
  = sum_(c=0)^2 lambda_c product_(i=0)^4 x_i[c],
lambda_c != 0.                                         (2)
```

Let `r_(i,s)=e_s^* composed with phi_i` be the five row covectors of
mode `i`.  Assume all five row configurations have quadrangle type:
each has one coordinate row, and its other four projective rows form a
complete quadrangle with diagonal points `E_0,E_1,E_2`.

## Every row pair has a two-colour annihilator

Fix a mode `i` and two different source coordinates `p,q`.  The
projective line through `r_(i,p),r_(i,q)` contains exactly one
coordinate point.

- Two non-coordinate quadrangle vertices form a side, and every side
  contains exactly one of `E_0,E_1,E_2`.
- If one row is the unique coordinate row and the other is a
  quadrangle vertex, their line contains that coordinate point.  It
  cannot contain a second coordinate point, because every quadrangle
  vertex has all three coordinates nonzero.

The two rows are independent.  Their common kernel is therefore a line;
choose a nonzero generator

```text
t_i(p,q) in ker r_(i,p) intersect ker r_(i,q).          (3)
```

The unique coordinate point in the row span says that one coordinate
of `t_i(p,q)` is zero.  Exactly one is zero: two zero coordinates would
make `t_i(p,q)` a coordinate vector, but no quadrangle vertex vanishes
on a coordinate vector.  Hence

```text
support(t_i(p,q)) has size two.                         (4)
```

## Four modes share a surviving colour

Fix any source pair `p,q`.  For each of the five modes, record the
unique missing target colour of `t_i(p,q)`.  These are five elements of
a three-element set.

There are four modes whose missing colours omit at least one colour
`c`.  Indeed, if all three colours occur among the five records, one of
them occurs only once; discard that mode.  If at most two colours
occur, discard any mode.  Let `I` be the retained four modes and `j`
the fifth.  Then

```text
t_i(p,q)[c] != 0 for every i in I.                      (5)
```

Evaluate (2) with `x_i=t_i(p,q)` for `i in I` and
`x_j=e_c`.  The right side is

```text
lambda_c product_(i in I) t_i(p,q)[c],
```

which is nonzero by (5).

On the left side, each source vector `phi_i(t_i(p,q))`, for `i in I`,
has zero coordinates `p` and `q`.  Thus four modes are supported on
only the other three source coordinates.  No permutation in `S_5` can
assign distinct source coordinates to those four modes.  Every
permanent monomial is zero, so the left side is zero.  This contradicts
(2) and proves (1).

## Verification

Run:

```text
python claims/arbitrary-order/verify_all_quadrangle_p5_obstruction.py
python claims/arbitrary-order/audit_all_quadrangle_p5_obstruction.py
```

The primary verifier reconstructs the standard complete quadrangle,
checks that all ten row-pair annihilators have support two, exhausts all
`3^5=243` missing-colour lists, and checks all `5!=120` permanent
assignments in the four-modes-versus-three-sources contradiction.  The
independent audit enumerates all 360 labelled quadrangle local types
over `F_7`, checks all 3,600 row pairs, and independently replays the
four-mode colour selection.

## Boundary

The proof uses the fact that every pair annihilator in a quadrangle map
has support exactly two.  A line-type map can have a common annihilator
of support one for its four collinear rows, while a map with multiple
coordinate rows has additional degeneracies.  Those are precisely the
branches not covered by this theorem.
