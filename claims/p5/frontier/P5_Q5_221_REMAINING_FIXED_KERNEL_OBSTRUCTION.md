# Remaining fixed-kernel obstructions in normalized `q5_221`

## Status

This is an exact monotone tensor theorem over `C`.

The two remaining seven-incidence covers with an all-normal mode,

```text
#7:  D_0=0011, D_1=0111, D_2=1001,
#10: D_0=0011, D_1=1101, D_2=0011,
```

are impossible, including every higher-incidence stratum above them.
Together with the preceding monotone theorems, only covers
`#8,#12,#13` remained at this checkpoint.  The later final-boundary
theorem closes their strict extensions and completes normalized
`q5_221`.  The full `P_5 -> Delta_3` problem and the global Krenn--Gu
conjecture remain open.

Use

```text
u_0=e_0+e_1, h_0=e_0-e_1,
u_1=e_2+e_3, h_1=e_2-e_3, h_2=e_4.
```

At an all-normal mode `F`, the zero-diagonal pullback determinant
forces one of the two directed residual cycles

```text
C_+: Q_20 -> e_2^3, Q_01 -> e_0^3, Q_12 -> e_1^3,
C_-: Q_02 -> e_0^3, Q_10 -> e_1^3, Q_21 -> e_2^3.   (1)
```

The two orientations of the complementary `h_2` pullbacks select the
two displayed cycles.

We repeatedly use two elementary facts.  First, a nonzero directional
derivative of a squarefree cubic has symmetric matrix

```text
[ 0 c b ]
[ c 0 a ]
[ b a 0 ],                                          (2)
```

which has rank at least two: its principal `2 x 2` minors are
`-a^2,-b^2,-c^2`.  Second, the nonzero decomposable-`P_3`
classification forces every rank-at-least-two triple to have profile
`222` and normals in one common-support sign chart.

## Cover `#7`

Let `F` be all-normal, let `H` contain `h_0,h_1`, let `X` contain
`h_1`, and let `P` contain `h_2`.  The distinguished-normal theorem
says that `F,P` are exactly the two `h_2` modes.  If `P` acquires
either majority normal, the all-normal-partner theorem, after swapping
the two majority colours if necessary, already gives a contradiction.
Thus assume

```text
h_0,h_1 notin U_P.                                  (3)
```

### The `C_+` orientation

The three residuals in `C_+` run through `H,X,P`.

On `Q_20`, the map at `P` has rank one or two.  If it had rank two,
all three local ranks would be at least two, hence exactly two.  This
would put `u_0` in `U_H`; then

```text
U_H=span(h_0,h_1,u_0).
```

The `Q_12` plane at `H` would have the support-one normal `u_1`,
impossible in a nonzero decomposable `P_3` chart.  Therefore

```text
rank_P(Q_20)=1,
u_0,h_2 in U_P.                                     (4)
```

Write, modulo `h_0,h_1`,

```text
U_H=span(h_0,h_1,A u_0+B u_1+C h_2).
```

The `Q_12` plane normal at `H`, in `(e_0,e_1,u_1)`
coordinates, is

```text
(-B,-B,A).
```

The nonzero sign classification excludes support one, so `B!=0`.
It follows that the `Q_20` map at `H` has rank three.

Suppose the `Q_01` map at `H` had rank two.  If the map at `X` also
had rank at least two, the `Q_01` map at `P` would be either rank
three or have the support-one plane normal `h_1`, both impossible.
Thus `X` would have rank one on `Q_01`, forcing

```text
U_X=span(h_0,u_1,h_1).
```

Both `H,X` would then have rank three on `Q_20`.  Contracting the
rank-one mode `P` leaves a nonzero bilinear derivative of rank at least
two by (2), which two invertible maps cannot turn into a pure product.
Hence

```text
rank_H(Q_01)=1,
U_H=span(h_0,h_1,u_1).                               (5)
```

The `Q_12` normal at `H` is now `u_0`.  At `P`, equation (4) puts the
row `u_0` in the `Q_12` plane, so its support-two normal is `h_0`.
If the normal at `X` were `u_0`, then both `H,X` would again have rank
three on `Q_20`, contradicting (2).  Thus the unique `Q_12` chart is

```text
normals: u_0 at H, h_0 at X,P,
factors: u_1 at H, u_0 at X,P.                       (6)
```

Contracting `Q_01` at the rank-one mode `H` by its surviving `h_1`
row leaves

```text
Sym(u_0,h_2) -> e_0 tensor e_0
```

through `X,P`.  The two directions have independent images at `P` by
(4), so they become dependent at `X`.  The `Q_01` factor at `X` is
therefore the line of `L_X(u_0)`.  Equation (6) says that the
`Q_12` factor at `X` is the same line, although the two residuals have
different target colours.  This factor-line collision excludes `C_+`.

### The `C_-` orientation

The nonzero `Q_02` residual has rank two at `H,P`; the map at `X` has
rank at least two.  The `P_3` theorem forces profile `222`, so
`h_0 in U_X`.

At each of `H,X`, the `Q_02` kernel normal has the form

```text
(a,b,b), b!=0                                       (7)
```

in `(u_0,e_2,e_3)` coordinates.  Modulo `h_0,h_1`, its third row may
be written

```text
b u_0-a u_1+c h_2.
```

Because `b!=0`, this row space has zero intersection with
`J_21^perp=span(u_1,h_2)`.  Thus both `H,X` have rank three on
`Q_21`.

If the `Q_21` map at `P` has rank at least two, the nonzero
decomposable-`P_3` theorem contradicts those two rank-three maps.  If
it has rank one, contraction at `P` leaves a nonzero bilinear
derivative of rank at least two by (2), and the two invertible maps
again preserve that rank.  Hence `C_-` is impossible, completing
cover `#7`.

## Cover `#10`

Let `F` be all-normal, let `P` contain `h_0,h_2`, and let `X,Y`
contain `h_1`.  If `P` also contains `h_1`, the two-all-normal theorem
applies.  If either `X` or `Y` also contains `h_0`, the
all-normal-partner theorem applies after a majority-colour swap.
Thus assume

```text
h_1 notin U_P,
h_0 notin U_X union U_Y.                             (8)
```

### The `C_+` orientation

First inspect `Q_20` through `P,X,Y`.  If its map at `P` has rank one,

```text
U_P=span(h_0,u_0,h_2).
```

On `Q_01`, the map at `P` then has rank two with support-one plane
normal `h_1`, while (8) makes the maps at `X,Y` have rank at least
two.  This cannot be a nonzero decomposable `P_3` image.

If the `Q_20` map at `P` has rank two, all three ranks are two.  Its
only sign chart is

```text
normals: h_1 at P, u_1 at X,Y,
factors: h_0 at P, h_1 at X,Y.                       (9)
```

For `Z=X,Y`, equations (8) and (9) give

```text
U_Z=span(u_0,h_1,h_0+a_Z h_2), a_Z!=0.
```

Both `Z` therefore have rank three on `Q_01`.  A rank-at-least-two
map at `P` is excluded by the `P_3` theorem; a rank-one map at `P`
leaves a bilinear derivative of rank at least two, which the two
invertible maps cannot reduce.  Thus `C_+` is impossible.

### The `C_-` orientation

Here the `h_2` pullback at `P` is supported on target colour one.
The independent `h_0` pullback has zero target-zero coordinate, so
its target-two coordinate is nonzero.  Contracting at `P` therefore
forces

```text
(L_F tensor L_X tensor L_Y)Q_20
  in C^* e_2^3.                                      (10)
```

All three local ranks in (10) are at least two, hence exactly two.
Their `Q_20` kernel normals all satisfy equality of the last two
coordinates because all three row spaces contain `h_1`.

No nonzero `P_3` sign chart has three such normals.  In support two,
the equality permits only the `u_1` variant, while a valid triple also
needs `h_1`.  In full support, only two vertices of the four-point sign
rectangle have equal last coordinates, while a valid triple needs
three distinct vertices.  This contradicts (10) and completes cover
`#10`.

## Verification

Run:

```text
python verify_p5_q5_221_remaining_fixed_kernel.py
python audit_p5_q5_221_remaining_fixed_kernel.py
```

The primary verifier reconstructs both directed cycles, the
support-one rank gates, the two support-two factor charts, the
kernel-normal intersection in (7), and the derivative-rank lemma.
The independent audit differentiates the squarefree cubics and checks
the relevant projective sign-chart slices over `F_3,F_5`.  Those
finite-field checks audit the case split; the written proof is over
`C`.  Neither script enumerates ambient row spaces or local maps.
