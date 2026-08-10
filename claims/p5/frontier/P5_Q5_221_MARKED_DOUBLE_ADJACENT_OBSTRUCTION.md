# Marked double-plus-adjacent obstruction in normalized `q5_221`

## Status

This is an exact conditional obstruction over `C` inside normalized
`q5_221`.

Let colours zero and one be the two multiplicity-two colours and colour
two the distinguished singleton colour.  There is no exact rank-drop
pattern

```text
D_0=D_2={A,B},   D_1={A,C}.                           (1)
```

The pattern obtained by swapping the two majority colours or the two
endpoints of the doubled edge is equivalent.  Thus (1) excludes the
marked double-plus-adjacent minimal type in which the singleton edge is
one of the doubled edges.

Together with
[`P5_Q5_221_PAIRED_MAJORITY_DROP_OBSTRUCTION.md`](P5_Q5_221_PAIRED_MAJORITY_DROP_OBSTRUCTION.md),
this closed four of the nine marked exact-six-incidence types.  Later
obstructions close the other five exact minimal types.  Extra rank-drop
containments, normalized `q5_221`, `P_5 -> Delta_3`, and the
arbitrary-order prize conjecture remain open.

## Source coordinates

Use

```text
x_+=e_0+e_1,  x_-=e_0-e_1,
y_+=e_2+e_3,  y_-=e_2-e_3,  z=e_4,
```

with

```text
u_0=x_+, u_1=y_+, u_2=z,
h_0=x_-, h_1=y_-, h_2=z.
```

The pattern (1) makes mode `A` all-normal:

```text
U_A=K=span(h_0,h_1,h_2).                              (2)
```

The cross-residual source spaces used below are

```text
J_20=span(x_-,e_2,e_3),   J_20^perp=span(u_0,h_2),
J_12=span(e_0,e_1,y_+),   J_12^perp=span(h_1,h_2),
J_21=span(e_0,e_1,y_-),   J_21^perp=span(u_1,h_2).    (3)
```

For every mode `i`,

```text
rank(L_i|J_cd)=3-dim(U_i intersect J_cd^perp).         (4)
```

## The first `Q_20` contraction

Contract the colour-two pure `P_4` identity at mode `B` by the target
covector pulling back to `h_0`.  The source residual is

```text
Q_20=Sym(x_-,e_2,e_3)
```

through modes `A,C,D`.

By (2), the mode-`A` restriction is the rank-two plane

```text
span((x_-)^*,h_1|J_20),
```

whose normal is `y_+` and has coordinate support two.  Modes `C,D` are
outside `D_2`, so their restrictions to the subspace
`J_20 subset H_2` have rank at least two.

The residual cannot be zero: the zero-`P_3` theorem would require the
mode-`A` plane normal to have coordinate support one.  It is therefore
a nonzero pure cube.  The nonzero `P_3` classification applies and
forces every residual rank to be two, with common normal support
`{e_2,e_3}`.

Mode `C` contains `h_1`.  On `J_20`, the plane with normal `y_+` is
`span((x_-)^*,h_1)`, while the plane with normal `y_-` is
`span((x_-)^*,u_1)`.  Since the latter does not contain the nonzero
restriction of `h_1`, the three plane normals are

```text
n_A=y_+,   n_C=y_+,   n_D=y_-.                        (5)
```

The last sign follows because a nonzero support-two `P_3` chart uses
both projective sign variants.

## Remove the rank-one exception at `B`

Now form the same `Q_20` residual by contracting at mode `A`.  Its
restriction at `B` has rank one exactly when

```text
u_0 in U_B,
```

because `h_2 in U_B` and `J_20^perp=span(u_0,h_2)`.

If this exception occurred, exactness of (1) would give

```text
U_B=span(h_0,h_2,u_0).                                (6)
```

Use instead the pair `h_1,h_2` at the all-normal mode `A`.  On both
`J_12` and `J_21`, the row space in (6) restricts to the coordinate
plane `span(h_0,u_0)`, killing respectively `y_+` and `y_-`.
All three residual ranks are at least two:

- on `J_12`, modes `B,C` contain only `h_2` and `h_1`,
  respectively, from the two-dimensional annihilator in (3);
- on `J_21`, mode `B` contains only `h_2`, while `C,D` avoid `h_2`.

Neither `Q_12` nor `Q_21` can therefore have nonzero pure image, because
the mode-`B` plane normal has support one.  Both would be zero, but the
zero-diagonal cross-scalar lemma at mode `A` forces at least one of
them to be nonzero.  Thus

```text
u_0 notin U_B.                                        (7)
```

The second `Q_20` residual now has rank at least two in every mode.  It
cannot be zero because (5) gives non-coordinate planes in modes `C,D`.
Hence its mode-`B` normal is one of the two sign variants `y_+,y_-`.

## Mode `B` normal `y_+`

If `n_B=y_+`, then (7) and exactness give

```text
U_B=span(h_0,h_2,h_1+a u_0),   a!=0.                 (8)
```

On `J_12`, (8) restricts to the coordinate plane
`span(h_0,u_0)` that kills `y_+`.  Thus `Q_12` cannot be nonzero and
the zero theorem forces modes `C,D` to kill `y_+` as well:

```text
L_C(y_+)=L_D(y_+)=0.                                  (9)
```

The cross-scalar lemma at mode `A` now forces `Q_21` to be nonzero.
All its residual ranks are at least two.  But (9) says that `U_C` has
no `u_1` component, and exactness says `h_2 notin U_C`.  Therefore

```text
U_C intersect span(u_1,h_2)=0,
rank(L_C|J_21)=3,
```

contradicting the nonzero decomposable-`P_3` theorem.

## Mode `B` normal `y_-`

If `n_B=y_-`, write

```text
U_B=span(h_0,h_2,u_1+a u_0).                          (10)
```

For `a!=0`, the `J_21` restriction is the support-one plane
`span(h_0,u_0)` that kills `y_-`.  The residual `Q_21` must be zero,
so the zero theorem makes mode `C` kill `y_-`.  This is impossible
because `h_1 in U_C` and `h_1(y_-)!=0`.

It remains that `a=0`.  Then the `J_12` restriction of (10) has normal
support `{e_0,e_1}`, not support one, so `Q_12` cannot be zero and must
be a nonzero pure cube.  Its three plane normals must have that same
support.

However, (5) says the `J_20` restriction in mode `C` has normal `y_+`.
Equivalently, every covector in `U_C` annihilates `y_+`, so `U_C` has
no `u_1` component.  On `J_12`, where `h_1,h_2` vanish, its restricted
row space is therefore contained in `span(h_0,u_0)`.  The nonzero
`P_3` classification forces rank two, hence equality, whose normal is
the support-one factor `y_+`.  This contradicts the required support
`{e_0,e_1}`.

Both signs in (10) are impossible, completing the exclusion of (1).

## Verification

Run:

```text
python verify_p5_q5_221_marked_double_adjacent.py
python audit_p5_q5_221_marked_double_adjacent.py
```

The primary verifier reconstructs the three residual spaces, the
all-normal `Q_20` plane, the two rank-one boundary planes, and every
normal-support conflict in the proof.  The independent audit enumerates
rank-three row spaces over `F_3` and `F_5` and checks the exact
containment/rank gates and the two sign-plane alternatives.  The
finite-field census audits the linear-algebra boundary; the written
argument above is over `C`.
