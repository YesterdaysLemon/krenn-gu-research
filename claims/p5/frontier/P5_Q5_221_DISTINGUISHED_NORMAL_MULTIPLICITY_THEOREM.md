# Distinguished-normal multiplicity theorem for normalized `q5_221`

## Status

This is an exact monotone tensor theorem over `C`.

For every hypothetical normalized `q5_221` restriction, let

```text
D_2={i:h_2 in U_i}
```

among the four modes left after fixing the distinguished mode.  Then

```text
|D_2|=2.                                              (1)
```

The lower bound is the embedded-`P_4` rank-drop theorem.  The new
content is the upper bound `|D_2|<=2`.  It uses no absence assumption
on any other normal, so it excludes monotonically all six
seven-incidence covers whose distinguished row has size three:

```text
#0, #1, #2, #3, #4, #9.                             (2)
```

By itself this theorem leaves the other eight monotone cover orbits; a
later theorem closes one of those eight.  Normalized `q5_221`,
`P_5 -> Delta_3`, and the arbitrary-order Krenn--Gu conjecture remain
open.

## Source slices

Use

```text
u_0=e_0+e_1,  u_1=e_2+e_3,  h_2=e_4.
```

The colour-zero and colour-one contractions at the distinguished mode
are

```text
T_0=Sym(u_0,e_2,e_3,h_2),
T_1=Sym(e_0,e_1,u_1,h_2).                            (3)
```

For a mode `i in D_2`, let `alpha_i2` be the unique target covector
such that

```text
L_i^* alpha_i2=h_2.
```

Contracting the colour-two identity by `alpha_i2` gives the usual
own-colour diagonal equation

```text
alpha_i2(e_2)=0.                                     (4)
```

## Double contraction and a forced residual

Suppose for contradiction that three modes `A,B,C` belong to `D_2`.
Double-contract the colour-zero identity at `A,B` by their `h_2`
pullbacks.  The source side is zero because `T_0` in (3) has only one
`h_2` factor:

```text
(h_2,h_2) contract T_0=0.
```

The target side is a nonzero scalar times

```text
alpha_A2(e_0) alpha_B2(e_0) e_0 tensor e_0.
```

Therefore one factor vanishes.  Relabel `A,B` so that

```text
alpha_A2(e_0)=0.                                     (5)
```

Equations (4)--(5) and `alpha_A2!=0` imply

```text
alpha_A2 in C*epsilon_1.                              (6)
```

Now contract the colour-one identity at `A` by `alpha_A2`.  By (3)
and (6), the remaining three modes carry a nonzero pure residual

```text
(L_B tensor L_C tensor L_D)Q_12
    = mu e_1 tensor e_1 tensor e_1,

Q_12=Sym(e_0,e_1,u_1),   mu!=0.                      (7)
```

## Apolarity forces two identical target rows

Both `B,C` still belong to `D_2`.  Since `h_2` annihilates the source
space of `Q_12`, each pullback `alpha_i2`, for `i=B,C`, annihilates
the local residual image:

```text
alpha_i2(L_i(J_12))=0.                               (8)
```

The nonzero tensor in (7) belongs to

```text
L_B(J_12) tensor L_C(J_12) tensor L_D(J_12).
```

Hence its nonzero local factor `e_1` lies in both
`L_B(J_12)` and `L_C(J_12)`.  Equation (8) gives

```text
alpha_B2(e_1)=alpha_C2(e_1)=0.                       (9)
```

Combining (4) and (9), each nonzero pullback has only target coordinate
zero:

```text
alpha_B2,alpha_C2 in C*epsilon_0.
```

Equivalently, the target-zero pullback rows at both modes are

```text
L_B^*epsilon_0 in C*h_2,
L_C^*epsilon_0 in C*h_2.                             (10)
```

The required pure colour-zero coefficient of the original `T_0`
identity evaluates `T_0` on the four target-zero rows.  By (10), two
of those rows are `h_2`.  But the first identity after (3) says exactly
that every such double evaluation is zero.  This contradicts the
required nonzero coefficient of `e_0^4`.

Thus three `h_2` incidences are impossible.  Together with the
rank-drop lower bound, this proves (1).

## Complementary-support orientation

There is a useful global corollary for the exactly two modes `P,Q` in
`D_2`.  Write

```text
alpha_P2=(x_P,y_P,0),
alpha_Q2=(x_Q,y_Q,0),                                (11)
```

where the last zeros are the own-colour equations.  Double
`h_2` contraction of `T_0` and `T_1` gives respectively

```text
x_P x_Q=0,   y_P y_Q=0.                              (12)
```

Both covectors in (11) are nonzero.  If either had both first
coordinates nonzero, (12) would make the other zero.  Thus they have
complementary singleton support.  After swapping `P,Q`,

```text
alpha_P2 in C*epsilon_0,
alpha_Q2 in C*epsilon_1.                             (13)
```

Consequently every surviving normalized branch has simultaneous
nonzero `Q_02` and `Q_12` residuals on two overlapping triples.  This
orientation is the starting point of the later cover-`#13` and
two-all-normal-modes obstructions.

## Incidence-poset consequence

In the fourteen-cover table from
[`P5_Q5_221_EXTRA_CONTAINMENT_REDUCTION.md`](P5_Q5_221_EXTRA_CONTAINMENT_REDUCTION.md),
the distinguished row has size three precisely in the six orbits
listed in (2).  Because the proof assumes only the three displayed
`h_2` containments, all their higher-incidence strata are excluded as
well.

The multiplicity theorem by itself leaves the monotone frontier

```text
#5, #6, #7, #8, #10, #11, #12, #13.                 (11)
```

The later cover-`#13` theorem closes the final exact no-fixed-kernel
seven-incidence stratum, and the two-all-normal theorem closes monotone
cover `#5`.  Subsequent fixed-kernel and final-boundary theorems close
all the remaining rows and complete normalized `q5_221`.

## Verification

Run:

```text
python claims/p5/frontier/verify_p5_q5_221_distinguished_normal_multiplicity.py
python claims/p5/frontier/audit_p5_q5_221_distinguished_normal_multiplicity.py
```

The primary verifier expands the symmetric tensors, checks the zero
double contraction and the nonzero `Q_12` contraction, and reconstructs
the target-covector and final coefficient implications symbolically.
The independent audit treats (3) as squarefree polynomials and proves
the two source identities by apolar differentiation.  Neither verifier
enumerates row spaces, maps, or coefficient-support charts.
