# Arbitrary permanent star-pair singleton `N/N` exclusion

## Status

This note proves an exact characteristic-zero exclusion for the last
same-mode branch left by the displayed equality-five `(4,1)` star-pair
boundary.  The predecessor reduces a local plane that is rank two for both
mixed-factor projections to their common line

```text
N=K(x_1+x_2),
```

singleton-supported at local colour `0` or `1`, and propagates it to a
distinct-mode singleton

```text
Q=K(x_2+x_3)
```

at colour `2`.  Those two incidences force two independent diagonal slices
of `pol(x_0x_4x_5)`.  Its slice map has rank two or three.  In either case,
the still-unused diagonal colour is forced onto the hyperplane `x_0=0` on
one pair of tensor shores.  The exact star-core identity

```text
g_(d_0)-g_(d_1)=2g_(m_1)                 on x_0=0
```

then contradicts one live diagonal target and two zero targets.

Consequently no remaining local plane is simultaneously low for both
displayed star projection families.  This is pointwise for the displayed
based star frame.  It does not classify distinct-mode low incidences,
transport the conclusion to every based frame in the unbased `(4,1)` orbit,
or treat the `(3,1)` orbit.  Unrestricted permanent nonrestriction remains
unknown, and the global Krenn--Gu conjecture remains **UNRESOLVED**.

## 1. Exact residual and predecessor input

Let `K` be a field of characteristic zero and split

```text
K^6=R direct-sum A,
R=span{x_0,x_1,x_2,x_3},       A=span{x_4,x_5}.
```

Put

```text
J((u_4,u_5),(v_4,v_5))=u_4v_5+u_5v_4.                 (1)
```

For the displayed star frame, all five complementary quartics have the
form `x_4x_5g_z`, with

```text
g_(m_1)=x_3(x_0+x_1-x_2),
g_(m_2)=(x_0-x_3)(x_1-x_2),

g_(d_0)=x_0x_1+x_0x_3-x_1x_2+2x_1x_3-x_2x_3,
g_(d_1)=-x_2(x_0+x_1-x_3),
g_(d_2)=2x_0x_3.                                      (2)
```

Let four ordered independent triples span the remaining local planes
`L_a,L_b,L_c,L_d`.  Assume the full exact targets

```text
T_(m_1)=T_(m_2)=0,
T_(d_i)=lambda_i e_i^* tensor e_i^* tensor e_i^*
                         tensor e_i^*,
lambda_i!=0,                                      i=0,1,2. (3)
```

The exact star-pair kernel-support and same-mode boundary predecessors are

```text
ARBITRARY_PERMANENT_STAR_PAIR_KERNEL_SUPPORT_BOUNDARY_THEOREM.md
ARBITRARY_PERMANENT_STAR_PAIR_SAME_MODE_NONCOMMON_AND_SUPPORT_TWO_BOUNDARY_THEOREM.md
```

They leave only the following case.  In one mode `a` the common kernel line is
singleton-supported at a colour

```text
s in {0,1},                    y_(a,s) in K^* N,        (4)
```

and a distinct mode `b` contains

```text
y_(b,2) in K^* Q.                                      (5)
```

Write

```text
t={0,1}\{s}.                                           (6)
```

The remaining modes are named `c,d`.  No normalization of the nonzero
scalars in (4)--(5) will be used.

## 2. The two forced `x_0x_4x_5` slices

Contracting the five cores once with the displayed generators gives

```text
B_(m_1)N=B_(m_2)N=B_(d_2)N=0,
B_(d_0)N=h_0=( 1,-1,-1,1),
B_(d_1)N=h_1=(-1,-1,-1,1),                            (7)

B_(d_2)Q=2x_0.                                        (8)
```

In particular,

```text
x_0=(h_0-h_1)/2.                                      (9)
```

Let

```text
E=K^3 with coordinates (X,U,V)=(x_0,x_4,x_5),
P=pol(XUV) in (E^*) tensor 3,                          (10)
```

and write a bar for the evaluation projection `K^6 -> E`.  Thus
`bar(y)=(x_0(y),x_4(y),x_5(y))`; the assertion `bar(y)=0` below does not
mean that the ambient vector `y` is zero.

For `e in E`, define the `c,d` slice map

```text
S(e)_(kl)=P(e,bar(y_(c,k)),bar(y_(d,l))),
S:E -> Mat_(3x3)(K).                                  (11)
```

Equation (8), the colour-`2` singleton in (5), and the `d_2` target give

```text
S(bar(y_(a,i)))=rho_2 delta_(i,2) E_22,
rho_2!=0.                                              (12)
```

Equations (7)--(9), the colour-`s` singleton in (4), and the `d_0,d_1`
targets similarly give

```text
S(bar(y_(b,j)))=rho_s delta_(j,s) E_ss,
rho_s!=0.                                              (13)
```

For `s=0`, this is `P=(P_(h_0)-P_(h_1))/2` with a live `h_0` slice and a
zero `h_1` slice.  For `s=1`, the same formula has a zero `h_0` slice and a
live `h_1` slice, changing only the harmless nonzero sign of `rho_s`.

The matrices `E_ss,E_22` are independent.  Since `dim E=3`, (12)--(13)
prove the exhaustive dichotomy

```text
rank S in {2,3},
S(bar(y_(a,t)))=S(bar(y_(b,t)))=0.                    (14)
```

## 3. Two elementary exact identities

### Lemma 1 (the star-core identity)

For `p,q in R` satisfying `x_0(p)=x_0(q)=0`, polarization of (2) gives

```text
g_(d_0)(p,q)-g_(d_1)(p,q)=2g_(m_1)(p,q).              (15)
```

Indeed, as square-free quadratics,

```text
g_(d_0)-g_(d_1)-2g_(m_1)=x_0(x_1+x_2-x_3),            (16)
```

whose bilinear contraction vanishes when both arguments lie on `x_0=0`.

### Lemma 2 (the `XUV` annihilator)

For `c,d in E`, put

```text
kappa(c,d)=P(-,c,d) in E^*.                            (17)
```

If `d=(X,U,V)`, the matrix of `c -> kappa(c,d)` is

```text
M(d)= [ 0  V  U ]
      [ V  0  X ]
      [ U  X  0 ].                                    (18)
```

Its three principal two-minors are

```text
-V^2, -U^2, -X^2.                                     (19)
```

Thus every nonzero `d`, including vectors with zero coordinates or
isotropic vectors for `J`, gives `rank M(d)>=2`.  Consequently each left
or right annihilator of a nonzero vector under `kappa` has dimension at
most one.

## 4. The rank-three slice case

Suppose first that `rank S=3`.  Then `S` is injective, so (14) gives

```text
bar(y_(a,t))=bar(y_(b,t))=0.                           (20)
```

In particular, these two vectors have zero `x_0,x_4,x_5` coordinates and
their `R`-parts lie in `span{x_1,x_2,x_3}`.

Evaluate any complementary quartic at the all-colour-`t` entry.  Because
the `a,b` vectors in (20) have no `A`-part, the two factors `x_4,x_5` must
come from the `c,d` slots.  The full four-slot polarization, with no
same-mode contraction, therefore factors exactly as

```text
T_z(t,t,t,t)
 =g_z(y_(a,t)^R,y_(b,t)^R)
  J(y_(c,t)^A,y_(d,t)^A).                              (21)
```

The `d_t` target in (3) makes (21) nonzero, so the common `J` factor is
nonzero.  The `m_1` target and the other diagonal target `d_(1-t)` are
zero at this entry.  Cancelling the common nonzero factor yields

```text
g_(m_1)=g_(d_(1-t))=0,
g_(d_t)!=0                                             (22)
```

on the same pair of vectors.  This contradicts (15), for both `t=0` and
`t=1`.

The exact rational sharpness fixture in the predecessor lies in this
rank-three case: its colour-`1` vectors on the `a,b` shores have zero
`x_0,x_4,x_5` projection.  Its displayed failure of the live `d_1`
diagonal is therefore exactly the obstruction in (21)--(22), rather than
an accidental feature of that fixture.

## 5. The rank-two slice case

Suppose now that `rank S=2`.  Equations (12)--(13) make its image exactly

```text
im S=span{E_ss,E_22}.                                  (23)
```

Put

```text
C_i=bar(y_(c,i)),                  D_j=bar(y_(d,j)).    (24)
```

Every matrix entry outside `(s,s)` and `(2,2)` vanishes throughout (23),
so

```text
kappa(C_i,D_j)=0              off those two cells,      (25)

kappa(C_s,D_s)!=0,            kappa(C_2,D_2)!=0.       (26)
```

The cross zeros in (25) show that `D_s,D_2` are independent: if they were
proportional, `kappa(C_s,D_2)=0` would contradict the first nonzero entry
in (26).  Symmetrically, `C_s,C_2` are independent.

Now `C_t` annihilates both independent vectors `D_s,D_2`.  Lemma 2 says a
nonzero vector has an annihilator of dimension at most one, hence

```text
C_t=0.
```

The symmetric argument gives

```text
D_t=0.                                                 (27)
```

By (24), equation (27) means exactly that the `c,d` colour-`t` vectors
have zero `x_0,x_4,x_5` coordinates; it does not make either ambient vector
zero.

At the all-colour-`t` entry, the two `A` factors must now come from the
`a,b` slots.  Full polarization factors as

```text
T_z(t,t,t,t)
 =J(y_(a,t)^A,y_(b,t)^A)
  g_z(y_(c,t)^R,y_(d,t)^R).                            (28)
```

The live `d_t` target makes the common `J` factor nonzero.  The zero
`m_1,d_(1-t)` targets and (15), now applied to the `c,d` pair in (27),
again force the live `d_t` factor to vanish.  This is the required
contradiction.

## 6. Theorem and exact boundary

### Theorem 3 (singleton common-kernel exclusion)

Under the exact target equations for the displayed based star frame, no
remaining local plane can have the common exceptional line `N` as a
singleton-supported rank-two kernel for both projection families.

Together with the predecessor exclusions of every common/noncommon pair,
every noncommon/noncommon pair, and support-two `N/N`, this proves

```text
same-mode low for both displayed star projections:       EXCLUDED;
distinct-mode exceptional incidences:                    NOT CLASSIFIED HERE;
all based frames in the unbased (4,1) orbit:              NOT TREATED;
unrestricted P_6 -> Delta_3:                             UNKNOWN;
global Krenn--Gu conjecture:                             UNRESOLVED.     (29)
```

Replay the exact checks with

```powershell
python claims/arbitrary-order/verify_arbitrary_permanent_star_pair_singleton_nn_exclusion.py
python claims/arbitrary-order/audit_arbitrary_permanent_star_pair_singleton_nn_exclusion.py
python -m py_compile claims/arbitrary-order/verify_arbitrary_permanent_star_pair_singleton_nn_exclusion.py claims/arbitrary-order/audit_arbitrary_permanent_star_pair_singleton_nn_exclusion.py
python -m ruff check claims/arbitrary-order/verify_arbitrary_permanent_star_pair_singleton_nn_exclusion.py claims/arbitrary-order/audit_arbitrary_permanent_star_pair_singleton_nn_exclusion.py
```

The primary verifier reconstructs (7)--(9), derives the `XUV` annihilator
matrix and all three symbolic minors, checks (16), and verifies both full
four-slot factorizations (21),(28) in the six-variable square-free algebra
for all five star cores.  The independent audit imports neither the primary
verifier nor SymPy: it reconstructs the cores from edge dictionaries,
checks the factorizations exhaustively on basis vectors, and searches the
annihilator incidence over two finite fields in addition to replaying the
exact integer identities.  The finite-field search is corroboration, not
the characteristic-zero proof; the written argument and exact algebraic
checks prove the theorem.
