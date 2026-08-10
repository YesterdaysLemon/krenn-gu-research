# Repeated-majority-pair cover obstruction in normalized `q5_221`

## Status

This is an exact tensor theorem over `C`.

There is no normalized `q5_221` restriction whose distinguished-normal
containments are exactly

```text
U_P,U_Q contain h_0,h_1,
U_R     contains h_1,h_2,
U_S     contains h_2,                                (1)
```

with no other containments among `h_0,h_1,h_2`.  This is exact
seven-incidence cover `#8` in
[`P5_Q5_221_EXTRA_CONTAINMENT_REDUCTION.md`](P5_Q5_221_EXTRA_CONTAINMENT_REDUCTION.md),
up to mode permutations and the majority-colour swap.

The theorem closes the exact open stratum, not its monotone closure:
additional distinguished-normal containments invalidate several
rank-one exclusions below.  The other cover strata, normalized
`q5_221`, the full restriction `P_5 -> Delta_3`, and the
arbitrary-order Krenn--Gu conjecture remain open.

## A two-channel rank-one lemma

Use

```text
u_0=e_0+e_1,  h_0=e_0-e_1,
u_1=e_2+e_3,  h_1=e_2-e_3,  h_2=e_4.                (2)
```

At `X=P,Q`, let `alpha_X0,alpha_X1` be the target covectors pulling
back to `h_0,h_1`, respectively, and put

```text
x_X=alpha_X1(e_0),   y_X=alpha_X0(e_1).              (3)
```

The own-colour diagonal entries vanish, and the cross-scalar lemma says
that `(x_X,y_X)` is not `(0,0)`.

Double-contract the colour-zero identity at `P,Q` by the two
`h_1` pullbacks and the colour-one identity by the two `h_0`
pullbacks.  Through modes `R,S` this gives, up to nonzero scalars,

```text
(L_R tensor L_S) Sym(u_0,h_2)
    = x_P x_Q e_0 tensor e_0,

(L_R tensor L_S) Sym(u_1,h_2)
    = y_P y_Q e_1 tensor e_1.                        (4)
```

Write

```text
a=L_R(u_0), b=L_R(u_1), z=L_R(h_2),
a'=L_S(u_0), b'=L_S(u_1), z'=L_S(h_2).
```

Both `z,z'` are nonzero.  The matrix

```text
a tensor z' + z tensor a'
```

has rank at most one only if `a,z` are proportional or `a',z'` are
proportional.  If it is zero, both proportionalities hold.  This is
the elementary two-summand Segre lemma: every `2 x 2` minor is a
product of the corresponding wedges.

Neither `R` nor `S` can absorb both `u_0,u_1` into its `h_2` image.
At `R`, the two resulting kernel vectors would make `h_0` belong to
`U_R`; at `S`, they would make both `h_0,h_1` belong to `U_S`.
Consequently, if one product in (4) vanished, both modes would absorb
that channel, while the other equation would make one of them absorb
the second channel as well.  Thus

```text
x_P x_Q != 0,   y_P y_Q != 0.                        (5)
```

## Three residual gates

The nonzero `Q_01` residual obtained by contracting at `P` runs through
`Q,R,S`.  If all three residual maps had rank at least two, the
decomposable-`P_3` theorem would force rank profile `222`.  At `R`, the
resulting plane contains `h_1,h_2`, so its normal on

```text
J_01=span(u_0,h_1,h_2)
```

would have support one, which the same theorem forbids.  Exactness in
(1) rules out rank one at `R` and `S`.  Hence the rank-one gate is at
`Q`, and

```text
U_Q=span(h_0,h_1,u_1).                               (6)
```

Interchanging `P,Q` gives the same formula for `U_P`.

Now use the nonzero `Q_10` residual.  On

```text
J_10=span(h_0,u_1,h_2),
```

the planes at `P,Q` have support-one normal `h_2`.  Neither of them can
have rank one, and exactness rules out rank one at `S`.  The only
escape from the rank-at-least-two `P_3` contradiction is therefore
the rank-one gate at `R`:

```text
U_R=span(h_1,h_2,u_0).                               (7)
```

In particular, `L_R(u_1)=0`.  The second equation in (4) now pins

```text
L_R(h_2) in C*e_1,   L_S(u_1) in C*e_1.             (8)
```

The vectors `L_R(u_0),L_R(h_2)` are independent, so the first equation
in (4) forces the rank-one dependency on the `S` side and pins

```text
L_S(h_2) in C*e_0.                                   (9)
```

Let `alpha_R2` pull back to `h_2`.  From (8),
`alpha_R2(e_1)` is nonzero.  The resulting `Q_12` residual through
`P,Q,S` is therefore nonzero pure in colour one.  All three local
ranks are two.  The `P,Q` plane normals on

```text
J_12=span(e_0,e_1,u_1)
```

are both `u_0`.  The support-two sign chart for decomposable `P_3`
then makes the `S` normal the opposite sign:

```text
n_S,12=h_0.                                          (10)
```

The local factor lines of this residual also recover

```text
L_P(h_0),L_Q(h_0) in C*e_1.                          (11)
```

The earlier rank-one `Q_01` gates similarly give

```text
L_P(h_1),L_Q(h_1) in C*e_0.                          (12)
```

## Multilinear normal form

Independent nonzero diagonal rescalings in the four target factors
preserve every pure-coordinate and forbidden mixed-coordinate
condition.  Using (6)--(12), write the pullback rows of the four local
maps as

```text
P_0=h_1+p_0 u_1,   P_1=h_0+p_1 u_1,   P_2=p_2 u_1,
Q_0=h_1+q_0 u_1,   Q_1=h_0+q_1 u_1,   Q_2=q_2 u_1,

R_0=a h_1+b u_0,
R_1=h_2+c h_1+d u_0,
R_2=e h_1+f u_0,

r_0=u_0+alpha h_1,   r_1=u_1+beta h_1,
S_0=h_2+A r_0,       S_1=r_1+B r_0,   S_2=C r_0,    (13)
```

where

```text
p_2 q_2 C != 0,   af-be != 0.                        (14)
```

The form of `S` is exactly (9), (10), and `L_S(u_1) in C*e_1`.

Now evaluate only three tensor coordinates.  Direct polarization of
the permanent tensors gives, up to the common nonzero normalization
factor,

```text
[e_0 e_0 e_0 e_0] (L_P tensor L_Q tensor L_R tensor L_S)T_0
    = 4b(p_0 q_0-1),

[e_0 e_0 e_2 e_0] (L_P tensor L_Q tensor L_R tensor L_S)T_0
    = 4f(p_0 q_0-1),

[e_2 e_2 e_2 e_2] (L_P tensor L_Q tensor L_R tensor L_S)T_2
    = 4Cfp_2q_2.                                     (15)
```

The first coordinate is the required nonzero pure colour-zero
coefficient, so `b(p_0q_0-1)` is nonzero.  The second is forbidden by
purity and therefore forces `f=0`.  But then the third, which must be
the nonzero pure colour-two coefficient, vanishes.  This contradiction
excludes (1).

## Verification

Run:

```text
python claims/p5/frontier/verify_p5_q5_221_repeated_majority_pair_cover.py
python claims/p5/frontier/audit_p5_q5_221_repeated_majority_pair_cover.py
```

The primary verifier reconstructs the residual planes, the normal
forms, the two-summand rank-one identity, and the three decisive
permanent coefficients over `C`.  The independent audit obtains the
same coefficients as mixed polynomial coefficients rather than as
permanents and separately checks all normal-form incidences and rank
conditions.  These are symbolic identity checks; no ambient row-space
or map search is used.
