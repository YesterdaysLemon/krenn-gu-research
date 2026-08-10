# Exact obstruction for the marked-middle `q5_221` path

## Status

This is an exact tensor theorem over `C`.

There is no exact normalized `q5_221` rank-drop pattern

```text
D_0={B,D},  D_1={A,C},  D_2={C,D}.                  (1)
```

This is the three-edge path whose distinguished singleton-colour edge
is the middle edge.  The proof is a kernel-plane incidence argument:
it uses the exact nonzero decomposable-`P_3` normal classification, but
no search through row spaces.

Together with the marked-end path theorem, this closes all nine exact
minimal marked incidence types.  Extra containments are not covered by
this exact-stratum theorem.  Normalized `q5_221`, the full restriction
`P_5 -> Delta_3`, and the arbitrary-order Krenn--Gu conjecture remain
open.

## Coordinates and the two residual chiralities

Use

```text
u_0=e_0+e_1,  h_0=e_0-e_1,
u_1=e_2+e_3,  h_1=e_2-e_3,  h_2=e_4.
```

At `C`, let `alpha_(C,1),alpha_(C,2)` pull back to `h_1,h_2`.
At `D`, let `alpha_(D,0),alpha_(D,2)` pull back to `h_0,h_2`.
The own-colour diagonal identities give

```text
alpha_(C,2)(e_2)=alpha_(D,2)(e_2)=0.                (2)
```

Contract both the colour-zero and colour-one `P_4` identities at
`C,D` by the covectors pulling back to `h_2`.  The source side has two
copies of the single factor `h_2`, so it is zero.  Hence

```text
alpha_(C,2)(e_0) alpha_(D,2)(e_0)=0,
alpha_(C,2)(e_1) alpha_(D,2)(e_1)=0.                (3)
```

The covectors in (3) are nonzero and both vanish in target coordinate
two.  Their supports in target coordinates zero and one must therefore
be complementary singletons.  Thus there are exactly two cases:

```text
I:  alpha_(C,2) in C^* epsilon_1,
    alpha_(D,2) in C^* epsilon_0;

II: alpha_(C,2) in C^* epsilon_0,
    alpha_(D,2) in C^* epsilon_1.                   (4)
```

Equivalently, case I makes both

```text
Q_12=Sym(e_0,e_1,u_1),
Q_02=Sym(u_0,e_2,e_3)                               (5)
```

nonzero pure residuals, through `A,B,D` and `A,B,C` respectively.  In
case II the local cross-scalar alternative makes both

```text
Q_21=Sym(e_0,e_1,h_1),
Q_20=Sym(h_0,e_2,e_3)                               (6)
```

nonzero pure residuals, through `A,B,D` and `A,B,C`.

## Kernel lines

Let

```text
K_i=ker L_i=U_i^perp,
```

a two-plane in the five-dimensional source space.  If `L_i` has rank
two on a residual source three-space `J`, its plane normal is exactly
the projective line

```text
K_i intersect J.                                    (7)
```

Every residual map in (5) or (6) has rank at least two.  Indeed, a
rank-one restriction would require two of the residual annihilator
normals in one exact row space, while (1) supplies at most the one
displayed incidence.  A possible rank-three map is ruled out by the
nonzero decomposable-`P_3` theorem.  Thus every normal line used below
is defined.

The four residual source spaces are

```text
J_12=span(e_0,e_1,u_1),
J_02=span(u_0,e_2,e_3),
J_21=span(e_0,e_1,h_1),
J_20=span(h_0,e_2,e_3).                              (8)
```

All lie in `H_2=h_2^perp`.

## Chirality I: three normals lie on two sign vertices

At mode `A`, the two normal lines

```text
K_A intersect J_12,  K_A intersect J_02
```

cannot be distinct.  If they were, they would span the two-plane
`K_A` inside `H_2`, which would put `h_2` in `U_A=K_A^perp`,
contrary to exactness of (1).  The lines therefore coincide.  The same
argument applies at `B`.  Since

```text
J_12 intersect J_02=span(u_0,u_1),                  (9)
```

write the common lines as

```text
ell_A=C(x_A u_0+y_A u_1),
ell_B=C(x_B u_0+y_B u_1).                            (10)
```

In the factor coordinates `(e_0,e_1,u_1)` of `Q_12`, both normals in
(10) have the form

```text
(x,x,y).
```

Mode `D` contains `h_0`, so its `Q_12` normal also has equal first two
coordinates.  Thus all three normals of the nonzero `Q_12` residual
obey

```text
n_0=n_1.                                             (11)
```

This is incompatible with every nonzero decomposable-`P_3` sign chart.
If the common support has size three, the three normals are three
distinct vertices of a four-point projective sign rectangle.  Only two
vertices have equal first two coordinates, so (11) cannot hold for all
three.

If the common support has size two, the chart uses both projective sign
variants, one of them twice.  For support `{0,1}`, only one variant has
equal coordinates.  For support `{0,2}` or `{1,2}`, equality would
force the nonzero coordinate in `{0,1}` to vanish.  No support-two chart
satisfies (11) at all three modes.  Chirality I is impossible.

## Chirality II: a support-one normal

Apply the same kernel-line argument to `J_21,J_20`.  Exact absence of
`h_2` at `A,B` makes the two residual normal lines coincide at each
mode, and

```text
J_21 intersect J_20=span(h_0,h_1).                  (14)
```

Because `h_1 in U_A`, every vector in `K_A` annihilates `h_1`.
The common line in (14) is therefore

```text
K_A intersect J_21=K_A intersect J_20=C h_0.        (15)
```

Similarly `h_0 in U_B` gives

```text
K_B intersect J_21=K_B intersect J_20=C h_1.        (16)
```

In the factor coordinates `(e_0,e_1,h_1)` of the nonzero residual
`Q_21`, the two normals (15)-(16) are

```text
(1,-1,0),  (0,0,1).
```

The second has coordinate support one.  No plane normal in a nonzero
decomposable rank-at-least-two restriction of `P_3` can have support
one.  This excludes chirality II.

Both cases in (4) are impossible, so the exact marked-middle path (1)
does not occur.

## Verification

Run:

```text
python claims/p5/frontier/verify_p5_q5_221_marked_middle_path.py
python claims/p5/frontier/audit_p5_q5_221_marked_middle_path.py
```

The primary verifier reconstructs the residual-space intersections,
the complementary-support chirality law, and the sign-rectangle
implications symbolically.  The independent audit uses a separate
small exact sign-chart representation to check that neither chirality
has an admissible pair of overlapping `P_3` charts.  Neither program
enumerates ambient row spaces.
