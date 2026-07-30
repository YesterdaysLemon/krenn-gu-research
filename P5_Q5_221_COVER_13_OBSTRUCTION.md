# Cover-13 obstruction in normalized `q5_221`

## Status

This is an exact tensor theorem over `C`.

There is no normalized `q5_221` restriction whose distinguished-normal
containments are exactly

```text
U_P,U_Q contain h_1,h_2,
U_R     contains h_0,h_1,
U_S     contains h_0,                                (1)
```

with no other containments among `h_0,h_1,h_2`.  This is exact
seven-incidence cover `#13` in
[`P5_Q5_221_EXTRA_CONTAINMENT_REDUCTION.md`](P5_Q5_221_EXTRA_CONTAINMENT_REDUCTION.md),
up to mode permutations and the majority-colour swap.

The theorem closes the last wholly untreated exact no-fixed-kernel
cover stratum.  It is not monotone: adding `h_0` at `P,Q` or `h_1` at
`S` changes the residual ranks below.  The later final-boundary theorem
closes those strict extensions and completes normalized `q5_221`.
The separate normalized `q4_211` branch, `P_5 -> Delta_3`, and the
global conjecture remain open.

## Orient the repeated `h_2` pair

Use

```text
u_0=e_0+e_1,  h_0=e_0-e_1,
u_1=e_2+e_3,  h_1=e_2-e_3,  h_2=e_4.
```

For `X=P,Q`, let `alpha_X2` pull back to `h_2`.  Double contraction of

```text
T_1=Sym(e_0,e_1,u_1,h_2)
```

at `P,Q` by these pullbacks is zero.  Therefore

```text
alpha_P2(e_1) alpha_Q2(e_1)=0.
```

Relabel so that `alpha_P2(e_1)=0`.  The own-colour identity also gives
`alpha_P2(e_2)=0`, hence

```text
alpha_P2 in C*epsilon_0,
L_P^*epsilon_0 in C*h_2.                             (2)
```

Contracting the colour-zero identity at `P` now leaves

```text
(L_Q tensor L_R tensor L_S)Q_02
  =mu e_0 tensor e_0 tensor e_0,   mu!=0,            (3)

Q_02=Sym(u_0,e_2,e_3).
```

At `Q`, the `h_2` pullback annihilates the `Q_02` source space and
therefore annihilates its nonzero local factor `e_0`.  Its target-two
coordinate vanishes by the own-colour identity.  Thus

```text
alpha_Q2 in C*epsilon_1,
L_Q^*epsilon_1 in C*h_2.                             (4)
```

Exactness in (1) makes all three maps in (3) have rank two: the
intersections with

```text
J_02^perp=span(h_0,h_2)
```

are respectively `span(h_2)`, `span(h_0)`, and `span(h_0)`.

## The two `P_3` sign strata

The restricted planes at `Q,R` both contain `h_1`.  Consequently their
projective normals in the ordered source coordinates
`(u_0,e_2,e_3)` satisfy

```text
n_1=n_2.                                             (5)
```

The nonzero decomposable-`P_3` classification leaves exactly two
possibilities.

### Support two

The normals and local factor directions are

```text
normals:  n_Q=n_R=u_1,  n_S=h_1,
factors:  h_1 at Q,R,   u_0 at S.                    (6)
```

All three factor directions map to target colour zero.  In particular,
`L_R(h_1) in C*e_0`, so the `h_1` pullback at `R` has nonzero
target-zero coordinate.  Contracting there gives a nonzero pure
`Q_01` residual through `P,Q,S`.

At `P,Q`, rank one on

```text
J_01=span(u_0,h_1,h_2),
J_01^perp=span(h_0,u_1)
```

would require the absent normal `h_0`.  If the mode-`S` rank were at
least two, the `P_3` theorem would force rank profile `222`; the planes
at `P,Q` would then be `span(h_1,h_2)` with support-one normal `u_0`,
impossible.  Hence `S` is the rank-one gate:

```text
span(h_0,u_1) subset U_S.                            (7)
```

Now inspect only the required colour-two coefficient.  On

```text
H_2=span(e_0,e_1,e_2,e_3),
```

the target-two pullback rows have the following block locations:

```text
P_2 in C*h_1,
Q_2,R_2 in span(u_0,h_0),
S_2 in span(u_1,h_0).                                (8)
```

The first statement follows from (2), `h_1 in U_P`, and the own-colour
equation for `h_1`.  The next two are the inactive directions in the
support-two chart (6), with their annihilator additions.  The last is
the rank-one gate (7).

The `h_0` component of `S_2` gives three rows in the
`span(e_0,e_1)` block and one in the `span(e_2,e_3)` block, so its
`T_2` coefficient is zero.  The `u_1` component gives two rows in each
block, but the remaining order-two permanent is

```text
Perm_2(h_1,u_1)=0.                                   (9)
```

Thus the required pure coefficient `T_2[2222]` vanishes, a
contradiction.

### Full support

In the full-support sign rectangle, the two normals satisfying (5)
are the two opposite vertices

```text
(a,b,b),  (a,-b,-b),   ab!=0.                        (10)
```

The local factor directions at `Q,R` are `e_2,e_3` in one order.
Both have nonzero `h_1` evaluation, so the same nonzero `Q_01`
residual and mode-`S` rank-one gate follow.

More importantly, the active and inactive rows in the two planes differ
by `h_1`.  After harmless nonzero target-coordinate rescalings and
restriction to `H_2`, write

```text
Q_2=Q_0+a' h_1,
R_0=R_2+b' h_1,   a'b'!=0.                           (11)
```

Also (2) and the `h_1` own-colour equation give

```text
P_2 in C*h_1
```

on `H_2`; absorb its nonzero scalar.  For fixed `S_2`, define

```text
F(q,r)=T_2(h_1,q,r,S_2).
```

Purity requires

```text
F(Q_0,R_2)=F(Q_0,R_0)=F(Q_2,R_0)=0,
F(Q_2,R_2)!=0.                                       (12)
```

But `T_2=Sym(e_0,e_1,e_2,e_3)` has degree two in the
`span(e_2,e_3)` block, so

```text
T_2(h_1,h_1,h_1,S_2)=0.                              (13)
```

Expanding the third zero in (12) with (11), and using the first two
zeros and (13), gives

```text
F(Q_2,R_0)=F(Q_2,R_2),
```

contradicting (12).  The full-support stratum is impossible as well,
which proves the theorem.

## Verification

Run:

```text
python verify_p5_q5_221_cover_13.py
python audit_p5_q5_221_cover_13.py
```

The primary verifier reconstructs both `Q_02` sign charts, their local
factor directions, the support-two block vanishing, and the
full-support four-coefficient rectangle identity.  The independent
audit treats the two decisive `T_2` statements as apolar derivatives
of the squarefree polynomial `x_0x_1x_2x_3`.  Neither verifier searches
ambient row spaces or local maps.
