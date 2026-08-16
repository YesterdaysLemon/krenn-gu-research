# Arbitrary permanent co-two `r=4` fixed-`e=2` full-extension exclusion

## Status

This note proves an exact characteristic-zero endpoint for the last
unexcluded based frame in the co-two equality-five branch.  For the fixed
`(4,2)`, `e=2` representative `024`, there is no exact extension from
`P_6` to the three-colour diagonal tensor `Delta_3`.

The proof is pointwise for the integral frame below.  A quotient-incidence
lemma first treats the common projection-kernel line, including its a priori
possible support-three case; its forced companion has relations killing all
three colours, so the common line cannot occur.  Exact determinants leave
six ordinary low lines.  Both mixed projection families must contain a
rank-two mode, their six companions are forced to single colours, and the
three incidences needed by one family are removed by a cubic rank obstruction
and unused-colour factor gates.

This closes representative `024`.  Together with the separately reviewed
representative packages, every equality-five based-frame representative now
has an endpoint exclusion.  A dedicated full equality-five synthesis and
proof-consolidation audit is still required before marking that branch
closed.  The dimension-at-least-six co-two sensor residual and unrestricted
`P_6 -> Delta_3` remain open.  The global Krenn--Gu conjecture remains
**UNRESOLVED**.

## 1. The fixed `e=2` frame and exact target

Let `K` be a field of characteristic zero and work in

```text
Z_6=K[x_0,...,x_5]/(x_0^2,...,x_5^2).
```

At the first two modes use the based `(4,2)`, `e=2` frame

```text
u_0=x_0+x_1-x_2-x_3,    u_1=x_1-x_3,    u_2=x_0-x_3,

v_0=x_0+x_1+x_2+x_3,    v_1=x_1+x_2,    v_2=x_0+x_2.    (1)
```

This is representative `024` in the exact based-frame classification.  In
edge order `(01,02,03,12,13,23)`, take the mixed basis and three diagonal
products

```text
m_1=u_0v_1=( 1, 1, 0, 0,-1,-1),
m_2=u_1v_0=( 1, 0,-1, 1, 0,-1),

d_0=u_0v_0=( 2, 0, 0, 0, 0,-2),
d_1=u_1v_1=( 0, 0, 0, 1,-1,-1),
d_2=u_2v_2=( 0, 1,-1, 0, 0,-1).                       (2)
```

Direct square-free multiplication gives

```text
dim span{u_iv_j:i!=j}=2,
dim span{u_iv_j:0<=i,j<=2}=5,                          (3)
```

and

```text
u_0v_2=u_1v_0=u_1v_2=m_2,
u_2v_0=u_2v_1=u_0v_1=m_1.                             (4)
```

Let `star` denote edge complementation in the first four coordinates,
followed by multiplication by `x_4x_5`.  Write

```text
star(z)=x_4x_5 g_z.
```

The five exact quadratic cores are

```text
g_(m_1)=-(x_0-x_3)(x_1+x_2),
g_(m_2)=-(x_0+x_2)(x_1-x_3),

g_(d_0)=-2(x_0x_1-x_2x_3),
g_(d_1)=-x_0(x_1+x_2-x_3),
g_(d_2)=-x_1(x_0+x_2-x_3).                            (5)
```

Put

```text
a=x_0-x_3,       b=x_1+x_2,       c=x_0+x_2,       d=x_1-x_3,

Phi_1=(a,b,x_4,x_5),              Phi_2=(c,d,x_4,x_5). (6)
```

The mixed complementary quartics are the polarizations of the products of
the four coordinates in `Phi_1` and `Phi_2`.

Let four ordered independent local triples

```text
(y_(t,0),y_(t,1),y_(t,2)),                 t=2,3,4,5,
```

span local three-planes `L_t subset K^6`.  An exact full extension would
satisfy

```text
T_(m_1)=T_(m_2)=0,

T_(d_i)=lambda_i e_i^* tensor e_i^* tensor e_i^*
                         tensor e_i^*,
lambda_i!=0,                                      i=0,1,2. (7)
```

Here `T_z` is the complete four-slot polarization of `star(z)` pulled back
to `L_2 tensor L_3 tensor L_4 tensor L_5`.  Equation (3) makes (7) the full
five-dimensional pair-product target.

### Theorem 1 (fixed-`e=2` full-extension exclusion)

No four ordered independent local triples satisfy (7) over a field of
characteristic zero.  Equivalently, the based fixed-`e=2` representative
`024` has no exact `P_6 -> Delta_3` extension.

## 2. All-support companion incidence

Split

```text
K^6=R direct-sum A,
R=span{x_0,x_1,x_2,x_3},       A=span{x_4,x_5},          (8)
```

and put

```text
J((r_4,r_5),(s_4,s_5))=r_4s_5+r_5s_4.                  (9)
```

For `p in R`, define

```text
B_zp=i_p g_z in R^*,
Q_p=span{B_zp:z=m_1,m_2,d_0,d_1,d_2},
H_p=ann_R(Q_p).                                        (10)
```

If `0!=p in L_t`, write its local colour expansion as

```text
p=sum_i alpha_i y_(t,i),       S=supp(alpha).           (11)
```

### Lemma 2 (all-support companion incidence)

Assume `p in L_t cap R` is nonzero and `dim Q_p>=2`.  Then some distinct
local mode `s` contains a nonzero vector

```text
q in L_s cap H_p.                                      (12)
```

If `q=sum_i beta_i y_(s,i)`, then

```text
supp(alpha) cap supp(beta)=empty.                       (13)
```

In particular `|supp(alpha)|<=2`.

### Proof

Suppose all three other local planes miss `H_p`.  Put `D=R/H_p`.  Since
`D^*=Q_p`, each of those local triples embeds in

```text
W=D direct-sum A,                  dim D>=2.
```

For `y=(r(y),q(y))`, define the `D`-valued symmetric trilinear map

```text
C(y,z,w)=r(y)J(q(z),q(w))+r(z)J(q(y),q(w))
                         +r(w)J(q(y),q(z)).             (14)
```

Evaluation by `B_zp` is the single contraction of `x_4x_5g_z` with `p`.
Equations (7) make (14) zero off the diagonal colours in `S` and nonzero on
every diagonal in `S`.

Fix different colours in two different modes.  The induced map from the
third copy of `W` to `D` kills an embedded three-space, so its rank is at
most `dim D-1`.  Its restriction to `D` is scalar multiplication by the
`J`-pairing of the two fixed `A`-parts.  Hence all cross-colour pairings
vanish.  The elementary orthogonality argument in the two-dimensional
nondegenerate `J`-space permits at most two active colours.

If `|S|=2`, every `A`-column at the third colour vanishes in all three
remaining modes.  In the nonzero all-third-colour target, the removed mode
would be the only source of both distinct factors `x_4,x_5`, impossible in
one tensor slot.  If `|S|=1`, cross-colour orthogonality and one nonzero
same-colour pairing force the two off-support vectors in another local mode
into one common line of `A`, contradicting local independence.  Thus a
distinct companion (12) exists.

For that companion, symmetry gives `B_zp(q)=0` in all five channels.  Legal
double contraction of (7) in the two distinct modes yields

```text
0=lambda_i alpha_i beta_i E_ii,             i=0,1,2,
```

and proves (13).  No vector was inserted into two tensor slots.

We also use the immediate support filter: every relation

```text
sum_z rho_z B_zq=0                                    (15)
```

forces

```text
rho_(d_i) beta_i=0,                       i=0,1,2,      (16)
```

by a legal single contraction in the mode containing `q`.

## 3. The common line, including support three, is impossible

The ambient projection kernels are

```text
ker(Phi_1)={(r,s,-s,r,0,0):r,s in K},
ker(Phi_2)={(r,s,-r,s,0,0):r,s in K}.                  (17)
```

In channel order `(m_2,d_0,d_1,d_2)` for the first family and
`(m_1,d_0,d_1,d_2)` for the second, the contraction determinants are

```text
8rs(r-s)(r+s),                       -8rs(r-s)(r+s).    (18)
```

The common exceptional root `r=s` is

```text
N=x_0+x_1-x_2+x_3.                                    (19)
```

At `N`, the contraction rank is three and

```text
B_(m_1)N=B_(m_2)N=0,
H_N=K G,                         G=x_2+x_3.             (20)
```

There is no diagonal relation at `N`, so before incidence its local support
could have size three.  Lemma 2 applies because `dim Q_N=3` and supplies a
nonzero copy of `G` in a distinct local mode.  At `G`, however,

```text
-B_(m_1)G-B_(m_2)G+B_(d_0)G=0,
B_(d_1)G=B_(d_2)G=0.                                  (21)
```

The support filter (16) successively gives

```text
beta_0=beta_1=beta_2=0,
```

contradicting `G!=0`.  Therefore `N` cannot occur with any support.  In
particular the only a priori support-three low line is excluded before the
ordinary incidence classification.

## 4. Six ordinary low lines and the rank floor

The remaining roots of (18) are

```text
Phi_1:
A=x_1-x_2,        B=x_0+x_3,        C=x_0-x_1+x_2+x_3;

Phi_2:
D=x_1+x_3,        E=x_0-x_2,        F=x_0-x_1-x_2-x_3. (22)
```

Every one has contraction rank three.  Their exact relations give

```text
A: B_(m_1)=B_(d_1)=0,             supp(A) subset {0,2};
B: B_(m_1)=B_(d_2)=0,             supp(B) subset {0,1};
C: B_(m_1)=0, -B_(m_2)+B_(d_0)=0, supp(C) subset {1,2};

D: B_(m_2)=B_(d_1)=0,             supp(D) subset {0,2};
E: B_(m_2)=B_(d_2)=0,             supp(E) subset {0,1};
F: B_(m_2)=0, -B_(m_1)+B_(d_0)=0, supp(F) subset {1,2}. (23)
```

Every intersection `L_t cap ker(Phi_k)` is contained in the union of the
three family-labelled lines in (22), since `N` is impossible.  Over the
infinite field `K`, a vector space cannot be a finite union of proper
subspaces.  Therefore

```text
rank(Phi_k|L_t)>=2                                    (24)
```

for every family and local mode.

## 5. A rank-two mode in both projection families

Assume every `Phi_1|L_t` has rank three.  The frame-independent
hyperplane-product lemma applied to `T_(m_1)=0` forces one common missing
factor.  Missing `x_4` or `x_5` kills every sensor, so all local planes lie
in `ker(a)` or all lie in `ker(b)`.

Inside either hyperplane, the kernel of `Phi_2` is exactly `K N`.  Section 3
excludes `N`, so every `Phi_2|L_t` also has rank three.  The second mixed zero
tensor now gives one common missing factor `c` or `d`.

On the four common cells, restrict the three diagonal cores to the
two-dimensional first-four-coordinate quotient.  The exact ranks are

```text
                         Phi_2 missing
                           c       d

Phi_1 missing a            2       2
              b            2       2.                 (25)
```

The target tensors `T_(d_0),T_(d_1),T_(d_2)` are linearly independent, so
every entry in (25) is too small.  This contradiction proves a rank-two
mode in the first projection family.  Exchanging the two families gives

```text
min_t rank(Phi_1|L_t)=min_t rank(Phi_2|L_t)=2.          (26)
```

## 6. Complete ordinary companion classification

Introduce

```text
A'=x_1+x_2,       B'=-x_0+x_3,      C'=x_0+x_1,
D'=-x_1+x_3,      E'= x_0+x_2.                          (27)
```

Direct contraction gives

```text
H_A=K A',      H_B=K B',      H_C=K C',
H_D=K D',      H_E=K E',      H_F=K C'.                (28)
```

At those companion lines, the exact relations are

```text
A': -B_(m_1)+B_(d_0)=0,  -B_(m_2)+B_(d_2)=0  => colour 1;
B': -B_(m_1)+B_(d_0)=0,  -B_(m_2)+B_(d_1)=0  => colour 2;
C': -B_(m_1)+B_(m_2)=0,
    -B_(m_1)+B_(d_1)=0,  -B_(m_1)+B_(d_2)=0  => colour 0;
D': -B_(m_2)+B_(d_0)=0,  -B_(m_1)+B_(d_2)=0  => colour 1;
E': -B_(m_2)+B_(d_0)=0,  -B_(m_1)+B_(d_1)=0  => colour 2. (29)
```

The support filter makes the arrows exhaustive:

```text
A -> A'/1,       B -> B'/2,       C -> C'/0,
D -> D'/1,       E -> E'/2,       F -> C'/0.           (30)
```

Every arrow occurs in a distinct local mode by Lemma 2.  The table lists
necessary incidences and does not assert realizability.

For later use, direct contraction gives common residual covectors in channel
order `(m_1,m_2,d_0,d_1,d_2)`:

```text
low/companion   low combination       companion combination       ell

A,A'            -m_2+d_0+d_2          d_1                         -2x_0
B,B'            -m_2+d_0+d_1         -d_2                         -2x_1
C,C'            -d_1+d_2             -2m_1+d_0                     2(x_2-x_3)
D,D'            -m_1+d_0+d_2         -d_1                         -2x_0
E,E'            -m_1+d_0+d_1          d_2                         -2x_1
F,C'            -d_1+d_2             -2m_1+d_0                     2(x_2-x_3).
                                                                    (31)
```

In every row, contraction of the low and companion combinations gives the
same displayed nonzero `ell`.

## 7. The three load-bearing `Phi_1` incidences

By (26), choose a `Phi_1` low.  It is `A`, `B`, or `C`, so the endpoint only
needs

```text
(A,A'),                         (B,B'),                         (C,C'). (32)
```

Let the low `p` occur in mode `r`, its companion `q` in mode `s`, and call
the remaining modes `t,u`.  Use the applicable `ell` in (31) and put

```text
(X,U,V)=(ell,x_4,x_5),              P=pol(XUV).          (33)
```

The channel coefficients and support filters give full three-slot tensor
identities

```text
P|_(L_r,L_t,L_u)=nu_e e_e^* tensor e_e^* tensor e_e^*,

P|_(L_s,L_t,L_u)=sum_(i in supp(p))
                 nu_i e_i^* tensor e_i^* tensor e_i^*, (34)
```

after harmlessly interchanging the names of the first slots.  Here `e` is
the forced companion colour and every displayed `nu` is nonzero.

Suppose `p` has support two.  Fixing `L_t,L_u`, the first-mode slice map of
`P` sends the companion-colour vector in `L_r` and the two support-colour
vectors in `L_s` to nonzero multiples of the three independent diagonal
matrices.  Those three ambient vectors are independent, and on their span
`Y`, equation (34) makes `P|_(Y,L_t,L_u)` a concise weighted `Delta_3`.
Thus `P=pol(XUV)` would have tensor rank three.

Its first-mode slice space is

```text
span{sym(UV),sym(XV),sym(XU)}.                          (35)
```

A rank-one symmetric matrix in (35) is a nonzero multiple of
`(rX+sU+tV)^2`; its missing square coefficients force `r=s=t=0`.  Hence
(35) contains no nonzero rank-one matrix, while a concise three-tensor of
rank at most three would contain three.  Every low in (32) is therefore
singleton-supported.

## 8. Singleton slice dichotomy and factor gates

Let the low colour be `i`, companion colour `e`, and unused colour

```text
j={0,1,2}\{i,e}.                                      (36)
```

For `v in K^6`, write

```text
bar(v)=(ell(v),x_4(v),x_5(v)) in E=K^3.
```

On the two untouched modes define

```text
S:E -> Mat_(3x3)(K),
S(w)_(kl)=P(w,bar(y_(t,k)),bar(y_(u,l))).               (37)
```

Equation (34) places nonzero multiples of `E_ee,E_ii` in `im S` and gives

```text
S(bar(y_(r,j)))=S(bar(y_(s,j)))=0.                     (38)
```

Thus `rank S` is two or three.  At rank three,

```text
bar(y_(r,j))=bar(y_(s,j))=0.                           (39)
```

At rank two, `im S=span{E_ee,E_ii}`.  For `w=(X,U,V)`, the contraction
matrix `z -> P(z,-,w)` is

```text
[ 0  V  U ]
[ V  0  X ]
[ U  X  0 ],                                           (40)
```

whose principal two-minors are `-V^2,-U^2,-X^2`.  Every nonzero `w` has
annihilator dimension at most one.  The live diagonal and zero cross cells
force

```text
bar(y_(t,j))=bar(y_(u,j))=0.                           (41)
```

The exact unused-colour factor gates for (32) are

```text
-g_(m_1)-g_(m_2)+g_(d_0)+g_(d_2)
                    =-x_0(x_1-x_2+x_3),

-g_(m_1)-g_(m_2)+g_(d_0)+g_(d_1)
                    =-x_1(x_0-x_2+x_3),

-g_(d_1)+g_(d_2)=(x_0-x_1)(x_2-x_3).                  (42)
```

For `(A,A')`, `ell` is a multiple of `x_0`, and the first gate has nonzero
coefficients at both possible unused diagonals `d_0,d_2`.  For `(B,B')`,
`ell` is a multiple of `x_1`, and the second gate has nonzero coefficients
at `d_0,d_1`.  For `(C,C')`, `ell` is a multiple of `x_2-x_3`, and the
third gate has nonzero coefficients at `d_1,d_2`.

In the rank-three case (39), the unused-colour vectors in modes `r,s` have
no `A`-part and their `R`-parts lie in `ker(ell)`.  Full polarization of the
applicable gate at the all-colour-`j` entry factors as

```text
g(y_(r,j)^R,y_(s,j)^R) J(y_(t,j)^A,y_(u,j)^A)=0,       (43)
```

because its quadratic core is divisible by `ell`.  Equation (7) makes the
same channel combination a nonzero coefficient times `lambda_j`.

In the rank-two case (41), use the other two shores:

```text
J(y_(r,j)^A,y_(s,j)^A) g(y_(t,j)^R,y_(u,j)^R)=0.       (44)
```

Again (42) gives zero while (7) gives a nonzero multiple of `lambda_j`.
Both cases contradict the target.  None of the necessary incidences (32)
can occur, contradicting the `Phi_1` rank drop in (26).  This proves
Theorem 1.

## 9. Exact boundary

```text
field:                                                   CHARACTERISTIC ZERO;
based (4,2), e=2 frame 024:                              ASSUMED;
full five-sensor Delta_3 target:                         ASSUMED;

generic projection-kernel directions:                   EXCLUDED;
common line N, including support three:                  EXCLUDED;
ordinary low lines:                                      EXACTLY A,B,C,D,E,F;
rank-two mode in each mixed projection family:           PROVED NECESSARY;
all ordinary low-line companion incidences:              CLASSIFIED;
three load-bearing Phi_1 incidences:                      EXCLUDED;

exact extension of fixed-e=2 representative 024:         EXCLUDED;
all equality-five representatives individually:          EXCLUDED;
equality-five full-extension synthesis audit:             PENDING;
dimension-at-least-six co-two sensor residual:            OPEN;
unrestricted P_6 -> Delta_3:                             UNKNOWN;
global Krenn--Gu conjecture:                             UNRESOLVED.   (45)
```

## Replay

```powershell
python claims/arbitrary-order/verify_arbitrary_permanent_cotwo_r4_fixed_e2_full_extension_exclusion.py
python claims/arbitrary-order/audit_arbitrary_permanent_cotwo_r4_fixed_e2_full_extension_exclusion.py
python -m py_compile claims/arbitrary-order/verify_arbitrary_permanent_cotwo_r4_fixed_e2_full_extension_exclusion.py claims/arbitrary-order/audit_arbitrary_permanent_cotwo_r4_fixed_e2_full_extension_exclusion.py
python -m ruff check claims/arbitrary-order/verify_arbitrary_permanent_cotwo_r4_fixed_e2_full_extension_exclusion.py claims/arbitrary-order/audit_arbitrary_permanent_cotwo_r4_fixed_e2_full_extension_exclusion.py
```

The primary replay uses exact symbolic square-free arithmetic, determinants,
exceptional-line ranks, common-line relations, common-cell restrictions,
residual covectors, and factor gates.  The independent audit imports neither
the primary nor SymPy; it rebuilds the frame with rational arithmetic and a
separate polynomial determinant implementation, checks every incidence and
factor identity, and exhausts the rank-one slice obstruction over two odd
finite fields as audit-only stress evidence.  The written characteristic-zero
arguments above, not the finite-field checks, prove the theorem.
