# Marked double-plus-disjoint obstruction in normalized `q5_221`

## Status

This is an exact conditional obstruction over `C` inside normalized
`q5_221`.

There is no exact rank-drop pattern

```text
D_0=D_2={A,B},   D_1={C,D},                           (1)
```

where colour two is the distinguished singleton colour and colour zero
is one of the two majority colours.  Thus the marked
double-plus-disjoint minimal type in which the singleton edge is one of
the doubled edges is impossible.

Together with the paired-majority and marked-adjacent obstructions,
this closed five of the nine marked exact-six-incidence types.  The
later triangle, star, and marked-path theorems close all nine exact
minimal types.  Extra containments, normalized `q5_221`,
`P_5 -> Delta_3`, and the arbitrary-order prize conjecture remain open.

## Coordinates and a forced `Q_20`

Use

```text
x_+=e_0+e_1,  x_-=e_0-e_1,
y_+=e_2+e_3,  y_-=e_2-e_3,  z=e_4,
```

and

```text
u_0=x_+, u_1=y_+, u_2=z,
h_0=x_-, h_1=y_-, h_2=z.
```

For `i=A,B`, let `alpha_(i,0),alpha_(i,2)` pull back to `h_0,h_2`.
Their own-colour diagonal entries vanish:

```text
alpha_(i,0)(e_0)=alpha_(i,2)(e_2)=0.
```

Contract the colour-zero identity at both `A,B` by the two covectors
pulling back to `h_2`.  The source contraction contains `h_2=z` twice
and is zero.  Therefore

```text
alpha_(A,2)(e_0) alpha_(B,2)(e_0)=0.                 (2)
```

At each endpoint, the two cross entries for `h_0,h_2` cannot both
vanish.  Equation (2) consequently makes at least one of

```text
alpha_(A,0)(e_2), alpha_(B,0)(e_2)
```

nonzero.  Relabel `A,B` so that contracting the colour-two identity at
`A` by `h_0` gives a nonzero pure `Q_20` through `B,C,D`.

## Both majority-one modes kill `y_+`

The source residual is

```text
Q_20=Sym(x_-,e_2,e_3),
J_20^perp=span(u_0,h_2).                              (3)
```

Modes `C,D` are outside `D_2`, so their residual ranks are at least
two.  At `B`, rank one occurs exactly when

```text
U_B=K_0:=span(h_0,h_2,u_0).                           (4)
```

If (4) does not occur, the nonzero `P_3` classification applies.  The
mode-`B` plane contains the coordinate covector `(x_-)^*`, so its
normal has support `{e_2,e_3}`.  Modes `C,D` contain `h_1`, forcing
their two coordinates on that support to have equal signs.  The
support-two sign chart therefore gives

```text
n_B=y_-,   n_C=n_D=y_+.                               (5)
```

In particular,

```text
L_C(y_+)=L_D(y_+)=0.                                  (6)
```

If (4) does occur, the pure `Q_20` factor at `B` is `e_2`.  Since
`h_0` is the unique nonzero row functional on `J_20`, its target
pullback does not annihilate that factor:

```text
alpha_(B,0)(e_2)!=0.
```

The rank-one `Q_20` slice assigns `x_-` to mode `B` and leaves the
nondegenerate `P_2(e_2,e_3)` through `C,D`.  A decomposable nonzero
bilinear tensor forces at least one of those two maps to have rank one
on `span(e_2,e_3)`.  Since both contain `h_1`, this says that at least
one kills `y_+`; call it `C`.

Now contract the colour-zero and colour-two identities at the other
`h_1` endpoint `D`.  The residuals are `Q_01` and `Q_21`.  Mode `C`
has rank three on both source spaces: killing `y_+` removes `u_1`,
while exactness removes respectively `h_0` and `h_2` from the two
annihilators.  Mode `B=K_0` has rank two.  Unless

```text
U_A=K_1:=span(h_0,h_2,u_1),                           (5a)
```

mode `A` also has rank at least two.  The target covector pulling back
to `h_1` has zero colour-one entry but cannot have both other entries
zero, so one of `Q_01,Q_21` is nonzero pure.  This is impossible with
the rank-three mode `C`.  Hence (5a) holds.

The reverse nonzero `Q_20` contraction at `B` now passes the
rank-at-least-two gate.  Its mode-`A` plane has normal `y_-`, so it
cannot be zero; the nonzero classification forces both `C,D` normals
to be `y_+`.  Thus (6) holds in the exceptional case as well.

## The `AB|CD` flattening leaves only `K_0`

On

```text
H_2=span(e_0,e_1,e_2,e_3),
```

equation (6) and rank three give

```text
U_C|H_2=U_D|H_2
  =H:=span(h_0,u_0,h_1)=y_+^perp.                    (7)
```

Choose the non-exceptional doubled endpoint supplied by (5) and call it
`B`.  Its row plane on `H_2` is

```text
U_B|H_2=span(h_0,u_1+b u_0)=:U(b).                   (8)
```

Write the other plane as

```text
U_A|H_2=span(h_0,p u_0+q h_1+r u_1).                 (9)
```

The `AB|CD` flattening of the colour-two `P_4` identity is the
complement pairing between the two pair-image spaces.  The target is
pure, so this pairing has rank one.

Use the six off-diagonal pair coordinates of `H_2`.  Put

```text
E=mu(h_0,h_0),
X=mu(h_0,u_1),
Y=mu(h_0,h_1).
```

The pair image `A(H,H)` has dimension four.  Under the complement
pairing:

- `E` detects `mu(h_1,h_1)`;
- `X` is orthogonal to all of `A(H,H)`;
- `Y` gives a nonzero independent functional, detected on
  `mu(h_0,h_1)`.

The first three generators of the `A,B` pair image include

```text
E, X, qY+rX.
```

Here the `p` term vanishes because `mu(u_0,h_0)=0`, while the `rX`
term pairs to zero against `A(H,H)`.  Rank one therefore forces
`q=0`.

If `r!=0`, normalize (9) to `U_A=U(a)`.  The remaining pair-image
generator

```text
mu(u_1+a u_0,u_1+b u_0)
```

pairs nontrivially with `mu(h_0,h_0)`, whereas `E` does not.  This
again gives two independent flattening rows.  Consequently `r=0`, and

```text
U_A|H_2=K_0|H_2=span(h_0,u_0).                       (10)
```

## A `P_2` contraction leaves `K_1`

Contract the colour-two identity in modes `C,D` by the covectors
pulling back to `h_1`.  On the source side,

```text
(u_2,h_1,h_1) contract P_5
  = -2 Sym(e_0,e_1).                                  (11)
```

The restriction of (11) at `A` has rank two.  At `B`, (8) restricts
to `span(h_0,b u_0)` on `span(e_0,e_1)`, which also has rank two when
`b!=0`.  A nondegenerate `P_2` through two rank-two maps has matrix
rank two, but the contracted target is either zero or pure.  Hence
`b=0`, and

```text
U_B|H_2=K_1:=span(h_0,u_1).                           (12)
```

The full five-dimensional row spaces are therefore

```text
U_A=span(h_0,h_2,u_0),
U_B=span(h_0,h_2,u_1).                                (13)
```

## Final `P_3` contradiction

The colour-one tensor is

```text
T_1=Sym(e_0,e_1,y_+,z).
```

By (6) and (13), modes `A,C,D` kill `y_+`, while mode `B` does not.
Every surviving term must assign `y_+` to mode `B`.  The nonzero pure
`T_1` identity therefore requires the residual

```text
P_3(e_0,e_1,z)
```

through modes `A,C,D` to have nonzero pure image.

Mode `A` has rank three on `S=span(e_0,e_1,z)`.  Modes `C,D` have rank
two there.  Indeed,

```text
S^perp=span(h_1,u_1).
```

Their row spaces contain `h_1`, while (6) removes `u_1`; hence
`U_i intersect S^perp=span(h_1)` and the restriction rank is two.

This gives residual rank profile `322`, contradicting the theorem that
every nonzero decomposable rank-at-least-two restriction of `P_3` has
rank profile `222`.  Pattern (1) is impossible.

## Verification

Run:

```text
python claims/p5/frontier/verify_p5_q5_221_marked_double_disjoint.py
python claims/p5/frontier/audit_p5_q5_221_marked_double_disjoint.py
```

The primary verifier reconstructs the complement-pairing calculation,
the `K_0/U(b)` two-mode contraction, and the final `322` residual.  The
independent audit repeats the pair-image rank classification over
`F_3` and `F_5` by enumerating row planes containing `h_0`.  The
finite-field census audits the linear-algebra boundary; the written
argument above is over `C`.
