# Arbitrary permanent co-two `r=4` pure-star full-extension exclusion

## Status

This note proves an exact characteristic-zero endpoint for the remaining
pure-star based frame in the co-two equality-five branch.  For the
`(4,1)`, `k=3` representative `014`, there is no exact extension from
`P_6` to the three-colour diagonal tensor `Delta_3`.

The proof is pointwise for the integral based frame displayed below.  It
first derives both four-factor mixed projections.  A quotient-incidence
lemma then excludes every generic projection-kernel direction, removes the
common kernel line, and leaves exactly four noncommon low lines.  Exact
deletion minors classify all of their companion incidences.  The one
projection family needed for the endpoint has only three possible
low/companion cycles.  A common cubic rank obstruction removes the sole
support-two cycle, and an unused-colour factor gate removes every singleton
cycle.

This closes representative `014`; it does not address the fixed `(4,2)`
representatives `025` or `024`, does not prove the dimension-at-least-six
sensor residual, and does not prove unrestricted `P_6 -> Delta_3`.
The global Krenn--Gu conjecture remains **UNRESOLVED**.

## 1. The pure-star frame and exact target

Let `K` be a field of characteristic zero and work in

```text
Z_6=K[x_0,...,x_5]/(x_0^2,...,x_5^2).
```

At the first two modes use the based `(4,1)`, `k=3` frame

```text
u_0=x_0-x_1,       u_1=x_0-x_3,       u_2=x_0-x_2,

v_0=x_0-x_1+x_2+x_3,
v_1=x_0+x_1+x_2-x_3,
v_2=x_0+x_1-x_2+x_3.                                  (1)
```

This is representative `014` in the exact based-frame classification.
In edge order `(01,02,03,12,13,23)`, take the mixed basis and the three
diagonal products

```text
m_1=u_0v_1=( 0, 1,-1,-1, 1, 0),
m_2=u_1v_0=(-1, 1, 0, 0, 1,-1),

d_0=u_0v_0=(-2, 1, 1,-1,-1, 0),
d_1=u_1v_1=( 1, 1,-2, 0,-1,-1),
d_2=u_2v_2=( 1,-2, 1,-1, 0,-1).                       (2)
```

Direct square-free multiplication gives

```text
dim span{u_iv_j:i!=j}=2,
dim span{u_iv_j:0<=i,j<=2}=5,                          (3)
```

and the off-diagonal products are

```text
u_0v_2=-m_1,      u_1v_2=-m_2,
u_2v_0=-m_1+m_2, u_2v_1=m_1-m_2.                      (4)
```

Let `star` denote edge complementation in the first four coordinates,
followed by multiplication by `x_4x_5`.  Write

```text
star(z)=x_4x_5 g_z.
```

The five exact quadratic cores are

```text
g_(m_1)=(x_0-x_1)(x_2-x_3),
g_(m_2)=-(x_0-x_3)(x_1-x_2),

g_(d_0)=-x_0x_2-x_0x_3+x_1x_2+x_1x_3-2x_2x_3,
g_(d_1)=-x_0x_1-x_0x_2-2x_1x_2+x_1x_3+x_2x_3,
g_(d_2)=-x_0x_1-x_0x_3+x_1x_2-2x_1x_3+x_2x_3.        (5)
```

Put

```text
Phi_1=(x_0-x_1,x_2-x_3,x_4,x_5),
Phi_2=(x_0-x_3,x_1-x_2,x_4,x_5).                      (6)
```

Thus the two mixed complementary quartics are, up to the displayed sign,
the polarizations of the products of the four coordinates in `Phi_1` and
`Phi_2`.

Let four ordered independent local triples

```text
(y_(t,0),y_(t,1),y_(t,2)),                 t=2,3,4,5,
```

span local three-planes `L_t subset K^6`.  An exact full extension of (1)
would satisfy

```text
T_(m_1)=T_(m_2)=0,

T_(d_c)=lambda_c e_c^* tensor e_c^* tensor e_c^*
                         tensor e_c^*,
lambda_c!=0,                                      c=0,1,2. (7)
```

Here `T_z` is the complete four-slot polarization of `star(z)` pulled back
to `L_2 tensor L_3 tensor L_4 tensor L_5`.  Equation (3) makes (7) the full
five-dimensional pair-product target, not a selected subsystem.

### Theorem 1 (pure-star full-extension exclusion)

No four ordered independent local triples satisfy (7) over a field of
characteristic zero.  Equivalently, the based pure-star representative
`014` has no exact `P_6 -> Delta_3` extension.

## 2. A quotient-incidence lemma

Split

```text
K^6=R direct-sum A,
R=span{x_0,x_1,x_2,x_3},       A=span{x_4,x_5},          (8)
```

and put

```text
J((a_4,a_5),(b_4,b_5))=a_4b_5+a_5b_4.                  (9)
```

For `p in R`, define

```text
B_zp=i_p g_z in R^*,
Q_p=span{B_zp:z=m_1,m_2,d_0,d_1,d_2},
H_p=ann_R(Q_p).                                        (10)
```

If `0!=p in L_t`, write its local colour expansion as

```text
p=sum_c alpha_c y_(t,c),       S=supp(alpha).           (11)
```

### Lemma 2 (all-support companion incidence)

Assume `p in L_t cap R` is nonzero and `dim Q_p>=2`.  Then some distinct
local mode `s` contains a nonzero vector

```text
q in L_s cap H_p.                                      (12)
```

If `q=sum_c beta_c y_(s,c)`, then

```text
supp(alpha) cap supp(beta)=empty.                       (13)
```

In particular `|supp(alpha)|<=2`.

### Proof

Suppose first that all three other local planes miss `H_p`.  Put
`D=R/H_p`.  Since `D^*=Q_p`, each of those local triples embeds in

```text
W=D direct-sum A,                  dim D>=2.
```

For `y=(r(y),a(y))`, define the `D`-valued symmetric trilinear map

```text
C(y,z,w)=r(y)J(a(z),a(w))+r(z)J(a(y),a(w))
                         +r(w)J(a(y),a(z)).             (14)
```

Evaluation of (14) by `B_zp` is the single contraction of
`x_4x_5g_z` with `p`.  Equations (7) therefore make (14) zero away from
the diagonal colours in `S` and nonzero on every diagonal in `S`.

Fix vectors of different colours in two different modes.  The induced
map from the third copy of `W` to `D` kills an embedded three-space, so it
has rank at most `dim D-1`.  Its restriction to `D` is scalar multiplication
by the `J`-pairing of the two fixed `A`-parts.  Hence all cross-colour
pairings vanish.  The elementary two-dimensional orthogonality argument
then permits at most two active colours, while every colour in `S` is
active.  Thus `|S|<=2`.

If `|S|=2`, the same two-dimensional argument makes every `A`-column at
the third colour zero in all three remaining modes.  In the nonzero
all-third-colour target, the removed mode would be the only possible source
of both distinct factors `x_4,x_5`; one tensor slot cannot supply both.
This is impossible.

If `|S|=1`, call its colour `e`.  Cross-colour orthogonality and a nonzero
diagonal value supply a nonzero same-colour pairing.  After permuting the
remaining modes, take that pairing between their first two colour-`e`
vectors.  For either off-`e` colour in the third mode, both cross pairings
in (14) vanish, so the zero mixed-colour value and the nonzero same-colour
pairing force its `D`-part to vanish.  Its `A`-part is orthogonal to the
same nonzero colour-`e` vector.  The two off-`e` vectors therefore lie in
one common line of `A` and are dependent.  This also contradicts local
independence.

The assumption that all other planes miss `H_p` is therefore impossible,
proving (12).  For a nonzero `q` in (12), symmetry gives

```text
B_zp(q)=0                                             (15)
```

for all five channels.  Double contraction of (7) in the two distinct
slots gives

```text
0=lambda_c alpha_c beta_c E_cc,             c=0,1,2.
```

Every `lambda_c` is nonzero, proving (13).  Since `q` has nonempty local
support, (13) also gives `|S|<=2`.  No two vectors from one local mode were
inserted into distinct tensor slots.  This proves the lemma.

We will also use the immediate support filter: every relation

```text
sum_z rho_z B_zq=0                                    (16)
```

forces

```text
rho_(d_c) beta_c=0,                       c=0,1,2,      (17)
```

by a legal single contraction in the mode containing `q`.

## 3. Exactly four noncommon low lines

The ambient projection kernels are

```text
ker(Phi_1)={p_1(a,b)=(a,a,b,b,0,0):a,b in K},
ker(Phi_2)={p_2(a,b)=(a,b,b,a,0,0):a,b in K}.           (18)
```

Contracting the five cores in (5) gives the following covectors on `R`.
For `p_1(a,b)`, channel order is `m_2,d_0,d_1,d_2`:

```text
(b-a, b-a, a-b, a-b),
(-2b, 2b,-2b,-2b),
(-a-b,-a-b,-3a+b, a+b),
(-a-b,-a-b, a+b,-3a+b).                               (19)
```

For `p_2(a,b)`, channel order is `m_1,d_0,d_1,d_2`:

```text
(b-a, a-b, a-b, b-a),
(-a-b, a+b,-3a+b,-a-b),
(-2b,-2b,-2b, 2b),
(-a-b,-3a+b, a+b,-a-b).                               (20)
```

Both `4 x 4` determinants are

```text
-64 a^2 b(a-b).                                       (21)
```

Away from `a=0`, `b=0`, and `a=b`, equation (21) makes
`Q_p=R^*`, hence `H_p=0`.  Lemma 2 would produce a nonzero vector in the
zero space, so every generic direction is impossible.

Name the exceptional lines

```text
A=x_2+x_3,       B=x_0+x_1,       N=x_0+x_1+x_2+x_3,
C=x_1+x_2,       D=x_0+x_3.                              (22)
```

Here `A,B,N` belong to `ker(Phi_1)` and `C,D,N` belong to
`ker(Phi_2)`.  The exact exceptional relations are

```text
A: B_(m_2)+B_(d_1)=B_(m_2)+B_(d_2)=0,
B: B_(d_0)=0,

C: B_(m_1)+B_(d_0)=B_(m_1)+B_(d_2)=0,
D: B_(d_1)=0.                                         (23)
```

Equations (17) and (23) force

```text
A has support {0},        B has support contained in {1,2},
C has support {1},        D has support contained in {0,2}. (24)
```

It remains to remove the common line `N`.  Its three diagonal contractions
are independent, so `dim Q_N=3`, and

```text
H_N=K h,                 h=-x_0+x_1+x_2+x_3.           (25)
```

Lemma 2 supplies `0!=q in K h` in another local mode.  At `h`, the exact
relations

```text
-B_(m_1)+B_(m_2)-B_(d_0)+B_(d_1)=0,
 B_(m_2)-B_(d_0)+B_(d_2)=0                            (26)
```

force all three local coefficients of `q` to vanish by (17), a
contradiction.  Therefore `N` never occurs.

Every intersection `L_t cap ker(Phi_k)` is now contained in a union of two
lines.  Over the infinite field `K`, a vector space cannot be a finite union
of proper subspaces.  Hence

```text
rank(Phi_k|L_t)>=2                                    (27)
```

for every `k,t`; a rank-two kernel is exactly one of the four family-labelled
lines `A,B,C,D` in (22).

## 4. A rank-two mode in both projection families

Assume for contradiction that every `Phi_1|L_t` has rank three.  The exact
hyperplane-product lemma applied to the zero mixed tensor `T_(m_1)` says
that all four hyperplane images have one common missing factor.  This is the
frame-independent lemma proved in

```text
claims/arbitrary-order/
ARBITRARY_PERMANENT_FIXED_PAIR_DIMENSION_FIVE_FULL_PROJECTION_BOUNDARY.md
```

Missing `x_4` or `x_5` kills every sensor in (5), contradicting (7).
Thus every `L_t` lies in one of

```text
ker(x_0-x_1),                    ker(x_2-x_3).           (28)
```

Inside either hyperplane in (28), the kernel of `Phi_2` is exactly `K N`.
Since Section 3 excludes `N`, every `Phi_2|L_t` also has rank three.  The
second mixed zero tensor then gives a common missing factor for `Phi_2`.
Again `x_4,x_5` are impossible, leaving `x_0-x_3` or `x_1-x_2`.

On the four common cells, restrict the three diagonal cores to the
two-dimensional first-four-coordinate quotient.  Their exact ranks are

```text
                         Phi_2 missing
                       x_0-x_3   x_1-x_2

Phi_1 missing x_0-x_1      2         2
              x_2-x_3      2         1.                (29)
```

The three target tensors `T_(d_0),T_(d_1),T_(d_2)` in (7) are linearly
independent, so every rank in (29) is too small.  This contradiction proves

```text
min_t rank(Phi_1|L_t)=2.                               (30)
```

The same argument with the two families exchanged proves

```text
min_t rank(Phi_2|L_t)=2.                               (31)
```

Together with (27), every putative extension has at least one low line in
each family.

## 5. Complete companion classification

Introduce three further lines

```text
E=x_1+x_3,             F=x_1-x_0,             G=x_3-x_0. (32)
```

Direct contraction gives

```text
H_A=span{C,E},       H_B=K F,
H_C=span{A,E},       H_D=K G.                          (33)
```

For `q=uC+vE`, the common vanishing factors of the `3 x 3` minors after
deleting columns `d_1,d_2` from the contraction matrix are respectively

```text
8uv^2,                         8u^2v.                  (34)
```

If the companion coefficient `beta_c` is nonzero, (17) says that `d_c` is
a coloop: deleting it must lower the contraction rank.  Since a companion
of `A` misses colour `0`, equations (34) force `uv=0`.  The endpoint
relations then give

```text
A -> C at colour 1,            or A -> E at colour 2.  (35)
```

Likewise, for `q=uA+vE`, the deletion factors for `d_0,d_2` are

```text
8uv^2,                         8u^2v,                  (36)
```

so

```text
C -> A at colour 0,            or C -> E at colour 2.  (37)
```

On the one-dimensional companions, the exact filters are

```text
F: -B_(m_2)+B_(d_1)=0,
    B_(m_1)-B_(m_2)+B_(d_2)=0;

G: -B_(m_1)+B_(d_0)=0,
   -B_(m_1)+B_(m_2)+B_(d_2)=0.                         (38)
```

Consequently

```text
B -> F at colour 0,             D -> G at colour 1.    (39)
```

Every arrow occurs in a distinct local mode, by Lemma 2.  Equations
(33)--(39) classify necessary incidences; they do not assert realizability.

For later use, the common residual covectors for all five possible arrows
are

```text
low/companion    low channel combination      companion combination   ell

A,C              -2m_2+d_0                    -2m_1+d_1               -4x_0
A,E              -2m_2+d_0                     2m_1+d_2               -4x_0
C,A              -2m_1+d_1                    -2m_2+d_0               -4x_0
C,E              -2m_1+d_1                     2m_1+d_2               -4x_0
B,F               2m_2-d_1-d_2                 2d_0                    4(x_2+x_3)
D,G               2m_1-d_0-d_2                 2d_1                    4(x_1+x_2).
                                                                    (40)
```

In every row, contracting the low and companion channel combinations gives
the same displayed nonzero `ell`.

## 6. The three load-bearing cycles

By (30), choose a `Phi_1` low.  It is either `A` or `B`.

If it is `A`, its support is the singleton colour `0`, and (35) gives a
companion `C` at colour `1` or `E` at colour `2`.  If it is `B`, its
support is contained in `{1,2}`, and (39) gives `F` at colour `0`.
Thus only the three rows

```text
(A,C),                         (A,E),                         (B,F) (41)
```

are needed for the endpoint.

Let a low `p` occur in mode `a`, its companion `q` in mode `b`, and call
the remaining modes `c,d`.  Use the applicable common covector `ell` in
(40) and put

```text
(X,U,V)=(ell,x_4,x_5),              P=pol(XUV).          (42)
```

The channel coefficients in (40), together with the support filters, give
the full three-slot tensors

```text
P|_(L_a,L_c,L_d)=nu_e e_e^* tensor e_e^* tensor e_e^*,

P|_(L_b,L_c,L_d)=sum_(i in supp(p))
                 nu_i e_i^* tensor e_i^* tensor e_i^*, (43)
```

after harmlessly interchanging the names of the first slots.  Every
displayed `nu` is nonzero.  These are full tensor identities, not scalar
double contractions.

## 7. The support-two `B` case is impossible

Only `B` can have support two.  Suppose its support is `{1,2}`; its
companion `F` has colour `0`.  Fixing `L_c,L_d`, the first-mode slice map of
`P` sends

```text
y_(a,0),             y_(b,1),             y_(b,2)       (44)
```

to nonzero multiples of the three independent diagonal matrices.  Hence
the vectors in (44) are independent.  On their span `Y`, equation (43)
makes `P|_(Y,L_c,L_d)` a concise weighted `Delta_3`.  The three evaluation
maps to `E=span{X,U,V}` are therefore isomorphisms, so `P=pol(XUV)` would
have tensor rank three.

This is impossible.  The first-mode slice space of `P` is

```text
span{sym(UV),sym(XV),sym(XU)}.                          (45)
```

A rank-one symmetric matrix is a nonzero scalar multiple of
`(aX+bU+cV)^2`; membership in (45) kills all three square coefficients and
forces `a=b=c=0`.  Thus (45) contains no nonzero rank-one matrix.  A concise
three-tensor of rank at most three would put three nonzero rank-one matrices
in its slice space.  Therefore `rank(P)>3`, a contradiction.

Every low in the three cycles (41) is consequently singleton-supported.

## 8. The singleton slice dichotomy

Let the low colour be `i`, the companion colour be `e`, and let

```text
t={0,1,2}\{i,e}.                                      (46)
```

For `v in K^6`, write

```text
bar(v)=(ell(v),x_4(v),x_5(v)) in E.
```

Define the slice map on the two untouched modes by

```text
S:E -> Mat_(3x3)(K),
S(w)_(kl)=P(w,bar(y_(c,k)),bar(y_(d,l))).              (47)
```

Equation (43) places nonzero multiples of `E_ee,E_ii` in `im S` and gives

```text
S(bar(y_(a,t)))=S(bar(y_(b,t)))=0.                    (48)
```

Hence `rank S` is two or three.  If it is three, (48) gives

```text
bar(y_(a,t))=bar(y_(b,t))=0.                          (49)
```

If it is two, its image is exactly `span{E_ee,E_ii}`.  For
`d=(X,U,V)`, the contraction matrix `c -> P(c,-,d)` is

```text
[ 0  V  U ]
[ V  0  X ]
[ U  X  0 ],                                          (50)
```

whose principal two-minors are `-V^2,-U^2,-X^2`.  Every nonzero `d`
therefore has annihilator dimension at most one.  The two live diagonal
cells and the cross zero cells make the colour-`e` and colour-`i` vectors
independent on both untouched shores.  Their common annihilators in (50)
force

```text
bar(y_(c,t))=bar(y_(d,t))=0.                          (51)
```

Equations (49)--(51) assert vanishing only after evaluation by
`ell,x_4,x_5`.

## 9. The unused-colour factor gates

The exact core identities needed for the three cycles are

```text
g_(d_0)+g_(d_1)+g_(d_2)
                    =-2x_0(x_1+x_2+x_3),

-g_(m_1)+2g_(m_2)-2g_(d_0)-g_(d_1)-g_(d_2)
                    = 4x_0(x_2+x_3).                  (52)
```

For `(A,C)` and `(A,E)`, `ell` is a nonzero multiple of `x_0`, and the
first line of (52) has a nonzero coefficient at every possible unused
diagonal.  For `(B,F)`, `ell` is a nonzero multiple of `x_2+x_3`, and the
second line has nonzero coefficients at both possible unused diagonals
`d_1,d_2`.  Thus in every cycle there is a channel combination whose core
is divisible by `ell` and whose coefficient at `d_t` is nonzero.

In the rank-three case (49), the colour-`t` vectors in modes `a,b` have no
`A`-part and their `R`-parts lie in `ker(ell)`.  Full four-slot polarization
of a channel core factors at the all-colour-`t` entry as

```text
T_z(t,t,t,t)=g_z(y_(a,t)^R,y_(b,t)^R)
             J(y_(c,t)^A,y_(d,t)^A).                  (53)
```

The applicable combination in (52) makes (53) zero because its quadratic
factor vanishes on `ker(ell) x ker(ell)`.  Equation (7), however, makes the
same combination a nonzero coefficient times `lambda_t`.

In the rank-two case (51), the identical argument uses the other two shores:

```text
T_z(t,t,t,t)=J(y_(a,t)^A,y_(b,t)^A)
             g_z(y_(c,t)^R,y_(d,t)^R).                (54)
```

Again (52) gives zero and (7) gives a nonzero multiple of `lambda_t`.
Both cases are contradictions.  Hence none of the cycles in (41) can
occur.  This contradicts the necessary `Phi_1` low in (30) and proves
Theorem 1.

## 10. Exact boundary

```text
field:                                                   CHARACTERISTIC ZERO;
based (4,1), k=3 pure-star frame 014:                    ASSUMED;
full five-sensor Delta_3 target:                         ASSUMED;

generic projection-kernel directions:                   EXCLUDED;
common kernel line N:                                    EXCLUDED;
noncommon rank-two kernel lines:                         EXACTLY A,B,C,D;
rank-two mode in each mixed projection family:           PROVED NECESSARY;
all four low-line companion incidences:                  CLASSIFIED;
three load-bearing Phi_1 low/companion cycles:           EXCLUDED;

exact extension of pure-star representative 014:         EXCLUDED;
fixed (4,2), e=1 representative 025:                     OPEN;
fixed (4,2), e=2 representative 024:                     OPEN;
dimension-at-least-six co-two sensor residual:            OPEN;
unrestricted P_6 -> Delta_3:                             UNKNOWN;
global Krenn--Gu conjecture:                             UNRESOLVED.   (55)
```

## Replay

```powershell
python claims/arbitrary-order/verify_arbitrary_permanent_cotwo_r4_pure_star_full_extension_exclusion.py
python claims/arbitrary-order/audit_arbitrary_permanent_cotwo_r4_pure_star_full_extension_exclusion.py
python -m py_compile claims/arbitrary-order/verify_arbitrary_permanent_cotwo_r4_pure_star_full_extension_exclusion.py claims/arbitrary-order/audit_arbitrary_permanent_cotwo_r4_pure_star_full_extension_exclusion.py
python -m ruff check claims/arbitrary-order/verify_arbitrary_permanent_cotwo_r4_pure_star_full_extension_exclusion.py claims/arbitrary-order/audit_arbitrary_permanent_cotwo_r4_pure_star_full_extension_exclusion.py
```

The primary replay uses exact symbolic square-free arithmetic, determinants,
deletion minors, common-cell restrictions, companion tables, and the two
factor gates.  The independent audit imports neither the primary replay nor
SymPy; it rebuilds the frame with integer arithmetic, uses a separate
polynomial determinant implementation, checks every incidence and factor
identity, and exhausts the rank-one slice obstruction over two odd finite
fields as an audit-only stress test.  The written characteristic-zero
arguments above, not the finite-field stress tests, prove the theorem.
