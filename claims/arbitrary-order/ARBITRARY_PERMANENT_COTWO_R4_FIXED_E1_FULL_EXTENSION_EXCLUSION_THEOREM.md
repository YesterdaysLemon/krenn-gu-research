# Arbitrary permanent co-two `r=4` fixed-`e=1` full-extension exclusion

## Status

This note proves an exact characteristic-zero endpoint for the fixed
`(4,2)`, `e=1` based frame in the co-two equality-five branch.  For
representative `025`, there is no exact extension from `P_6` to the
three-colour diagonal tensor `Delta_3`.

The proof is pointwise for the integral based frame below.  It derives both
four-factor mixed projections, proves that each projection family must have
a rank-two mode, classifies every exceptional kernel-line companion, and
then excludes all three companions needed by one projection family.  The
two-sided projection-drop step has one new rank-three common cell; its exact
diagonal combination is the polarization of `X^2UV`, whose cubic slice
space contains no nonzero rank-one tensor.

This closes representative `025`.  It does not address the remaining fixed
`e=2` representative `024`, does not prove the dimension-at-least-six
co-two sensor residual, and does not prove unrestricted `P_6 -> Delta_3`.
The global Krenn--Gu conjecture remains **UNRESOLVED**.

## 1. The fixed `e=1` frame and exact target

Let `K` be a field of characteristic zero and work in

```text
Z_6=K[x_0,...,x_5]/(x_0^2,...,x_5^2).
```

At the first two modes use the based `(4,2)`, `e=1` frame

```text
u_0=x_1-x_2,       u_1=x_0-x_1,       u_2=x_0-x_3,

v_0=x_1+x_3,       v_1=x_0-x_1,       v_2=x_0+x_2.       (1)
```

This is representative `025` in the exact based-frame classification.  In
edge order `(01,02,03,12,13,23)`, take the mixed basis and the three
diagonal products

```text
m_1=u_0v_1=( 1,-1, 0, 1, 0, 0),
m_2=u_1v_0=( 1, 0, 1, 0,-1, 0),

d_0=u_0v_0=( 0, 0, 0,-1, 1,-1),
d_1=u_1v_1=(-2, 0, 0, 0, 0, 0),
d_2=u_2v_2=( 0, 1,-1, 0, 0,-1).                       (2)
```

Direct square-free multiplication gives

```text
dim span{u_iv_j:i!=j}=2,
dim span{u_iv_j:0<=i,j<=2}=5,                          (3)
```

and the other off-diagonal products are

```text
u_0v_2=m_1,       u_1v_2=-m_1,
u_2v_0=m_2,       u_2v_1=-m_2.                        (4)
```

Let `star` denote edge complementation in the first four coordinates,
followed by multiplication by `x_4x_5`.  Write

```text
star(z)=x_4x_5 g_z.
```

The five exact quadratic cores are

```text
g_(m_1)= x_3(x_0-x_1+x_2),
g_(m_2)= x_2(-x_0+x_1+x_3),

g_(d_0)=-x_0(x_1-x_2+x_3),
g_(d_1)=-2x_2x_3,
g_(d_2)=-x_1(x_0+x_2-x_3).                            (5)
```

Put

```text
h_1=x_0-x_1+x_2,              h_2=-x_0+x_1+x_3,

Phi_1=(x_3,h_1,x_4,x_5),      Phi_2=(x_2,h_2,x_4,x_5). (6)
```

Thus the two mixed complementary quartics are the polarizations of the
products of the four coordinates in `Phi_1` and `Phi_2`.

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
five-dimensional pair-product target.

### Theorem 1 (fixed-`e=1` full-extension exclusion)

No four ordered independent local triples satisfy (7) over a field of
characteristic zero.  Equivalently, the based fixed-`e=1` representative
`025` has no exact `P_6 -> Delta_3` extension.

## 2. All-support companion incidence

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
`x_4x_5g_z` with `p`.  Equations (7) make (14) zero away from the diagonal
colours in `S` and nonzero on every diagonal in `S`.

Fix vectors of different colours in two different modes.  The induced map
from the third copy of `W` to `D` kills an embedded three-space, so it has
rank at most `dim D-1`.  Its restriction to `D` is scalar multiplication by
the `J`-pairing of the two fixed `A`-parts.  Hence all cross-colour pairings
vanish.  The elementary two-dimensional orthogonality argument then
permits at most two active colours, while every colour in `S` is active.

If `|S|=2`, that same argument makes every `A`-column at the third colour
zero in all three remaining modes.  In the nonzero all-third-colour target,
the removed mode would be the only possible source of both distinct factors
`x_4,x_5`, which one tensor slot cannot supply.

If `|S|=1`, call its colour `e`.  Cross-colour orthogonality and a nonzero
diagonal value supply a nonzero same-colour pairing.  After permuting the
remaining modes, take that pairing between their first two colour-`e`
vectors.  For either off-`e` colour in the third mode, both cross pairings
in (14) vanish, so the zero mixed-colour value and the nonzero same-colour
pairing force its `D`-part to vanish.  Its `A`-part is orthogonal to the
same nonzero colour-`e` vector.  The two off-`e` vectors therefore lie in
one common line of `A` and are dependent.  This contradicts local
independence.

Thus another local plane meets `H_p`, proving (12).  For nonzero `q` in
(12), symmetry gives `B_zp(q)=0` for all five channels.  Double contraction
of (7) in the two distinct slots gives

```text
0=lambda_c alpha_c beta_c E_cc,             c=0,1,2.
```

Every `lambda_c` is nonzero, proving (13).  No two vectors from one local
mode were inserted into distinct tensor slots.  This proves the lemma.

We also use its immediate support filter: every relation

```text
sum_z rho_z B_zq=0                                    (15)
```

forces

```text
rho_(d_c) beta_c=0,                       c=0,1,2,      (16)
```

by a legal single contraction in the mode containing `q`.

## 3. Exceptional kernel lines and the rank floor

The ambient projection kernels are

```text
ker(Phi_1)={p_1(a,b)=(a-b,a,b,0,0,0):a,b in K},
ker(Phi_2)={p_2(a,b)=(a+b,a,0,b,0,0):a,b in K}.         (17)
```

In channel order `(m_2,d_0,d_1,d_2)` for `p_1`, and
`(m_1,d_0,d_1,d_2)` for `p_2`, the exact contraction determinants are

```text
det_1=-8ab^2(a-b),                 det_2=8ab^2(a+b).     (18)
```

Away from the displayed factors, `Q_p=R^*`, so `H_p=0`.  Lemma 2 would
produce a nonzero vector in the zero space.  Name the exceptional lines

```text
A=-x_0+x_2,       B=x_1+x_2,       N=x_0+x_1,
C= x_0+x_3,       D=x_1-x_3.                             (19)
```

Here `A,B,N` belong to `ker(Phi_1)` and `C,D,N` belong to
`ker(Phi_2)`.  Their contraction ranks and exact relations are

```text
line   dim Q_p       relations

A        3           B_(m_1)=B_(d_2)=0
B        3           B_(m_1)=B_(d_0)=0
C        3           B_(m_2)=B_(d_2)=0
D        3           B_(m_2)=B_(d_0)=0
N        2           B_(m_1)=B_(m_2)=B_(d_1)=0.        (20)
```

The support filter (16) therefore gives

```text
supp(A),supp(C) subset {0,1},
supp(B),supp(D) subset {1,2},
supp(N)         subset {0,2}.                           (21)
```

Every intersection `L_t cap ker(Phi_k)` is contained in the union of the
three family-labelled lines in (19).  Over the infinite field `K`, a vector
space cannot be a finite union of proper subspaces.  Hence

```text
rank(Phi_k|L_t)>=2                                    (22)
```

for every `k,t`; a rank-two mode contains exactly one of the corresponding
three exceptional lines.

## 4. A rank-two mode in both projection families

We use the frame-independent hyperplane-product and sharp
hyperplane-plane product lemmas proved in the fixed-pair boundary packages:

```text
claims/arbitrary-order/
ARBITRARY_PERMANENT_FIXED_PAIR_DIMENSION_FIVE_FULL_PROJECTION_BOUNDARY.md

claims/arbitrary-order/
ARBITRARY_PERMANENT_FIXED_PAIR_TWO_SIDED_PROJECTION_DROP_THEOREM.md
```

Assume first that every `Phi_1|L_t` has rank three.  The zero tensor
`T_(m_1)` forces all four hyperplane images to have one common missing
coordinate.  Missing `x_4` or `x_5` kills every sensor in (5), while missing
`x_3` kills `T_(d_1)`.  Therefore

```text
L_t subset ker(h_1)                         for every t. (23)
```

Inside `ker(h_1)`, the kernel of `Phi_2` is the single line `K N`.
Consequently every secondary image has rank two or three, and it has rank
two exactly when `N in L_t`; call such a mode low.

If there are no low modes, the full-rank hyperplane-product lemma for
`Phi_2` gives another common missing coordinate.  If there is exactly one,
group two hyperplane images against the remaining hyperplane and plane.
The hyperplane-hyperplane and hyperplane-plane products both have dimension
at least three, so edge-complement orthogonality forces equality; the
equality cases again put all four images in one coordinate hyperplane.  In
either case there is

```text
psi in {x_2,h_2,x_4,x_5}
such that L_t subset ker(h_1) cap ker(psi) for every t.  (24)
```

The `x_4,x_5` cells kill all sensors.  In the `x_2` cell, the restrictions
of `g_(d_0),g_(d_1),g_(d_2)` span only a two-dimensional space, contradicting
the three independent target tensors in (7).  It remains to exclude the
cell

```text
W=ker(h_1) cap ker(h_2).                                (25)
```

Parameterize its first-four-coordinate part by

```text
(x_0,x_1,x_2,x_3)=(s-t,s,t,-t).
```

The diagonal cores restrict to

```text
g_(d_0)=-(s-t)(s-2t),
g_(d_1)= 2t^2,
g_(d_2)=-s(s+t),

4g_(d_0)+3g_(d_1)+4g_(d_2)=-2(2s-t)^2.                (26)
```

All three target coefficients in the last combination are nonzero.  Put
`X=2s-t`, `U=x_4`, and `V=x_5`.  If every `L_t` lay in `W`, (7) and (26)
would identify the pullback of `pol(X^2UV)` with a concise weighted
`Delta_3`, a tensor of rank three.  Conciseness makes every evaluation map
`L_t -> span{X,U,V}` an isomorphism, so `pol(X^2UV)` itself would have rank
three.

This is impossible.  Its first-mode cubic slice space is

```text
span{pol(XUV), X^2V, X^2U}.                             (27)
```

Every cubic in (27) is divisible by `X`.  A symmetric rank-one cubic in
that space would be a nonzero cube `ell^3`; divisibility forces
`ell` to be proportional to `X`, but `X^3` is absent from (27).  Thus the
slice space contains no nonzero rank-one tensor, whereas a concise
four-tensor of rank at most three would place three such tensors there.
This excludes (25), and therefore zero or one low mode is impossible.

For a low mode `t`, write

```text
N=sum_c alpha_(t,c)y_(t,c).
```

Single contraction of `star(d_1)` with `N` is zero, so (7) gives
`alpha_(t,1)=0`, recovering the last line of (21).  For two distinct low
modes `s,t`, double contraction gives

```text
i_Ni_N star(m_1)=i_Ni_N star(m_2)=i_Ni_N star(d_1)=0,

i_Ni_N star(d_0)=i_Ni_N star(d_2)=-2J.                 (28)
```

The equal nonzero sensor forms in (28) occupy different diagonal target
cells.  Hence

```text
alpha_(s,0)alpha_(t,0)=alpha_(s,2)alpha_(t,2)=0.        (29)
```

Every pair of low modes is therefore supported on different singletons in
`{0,2}`.  Three low modes are impossible.  Exactly two remain, and after
rescaling and swapping them,

```text
N=y_(s,0),                         N=y_(t,2).            (30)
```

Apply the sharp `(3,3,2,2)` zero-permanent classification to the two high
and two low `Phi_2` images.  Its common-coordinate branch is (24), already
excluded.  In its only other branch, the two low images are one plane `P`
and the high images are complementary hyperplanes `H_+,H_-`.

Contract the target in the two low slots by (30).  All three diagonal cells
and both mixed cells vanish.  Equation (28) therefore gives

```text
J(H_+,H_-)=0.                                           (31)
```

In `Phi_2` factor coordinates, the radical of `J` is the plane spanned by
`x_2,h_2`.  Two mutually `J`-orthogonal hyperplanes must contain that
radical, so their intersection plane `P` is exactly the radical.  Both low
local planes then have `x_4=x_5=0`.  The high modes would have to supply
both factors `x_4,x_5`, but their pairing is zero by (31).  Every sensor
would vanish, contradicting (7).

This proves a rank-two mode in the `Phi_1` family.  Repeating the identical
argument with `(x_3,h_1,m_1)` and `(x_2,h_2,m_2)` exchanged uses the same
line `N`, the same identities (26)--(31), and the `x_3` common cell of
diagonal rank two.  Hence

```text
min_t rank(Phi_1|L_t)=min_t rank(Phi_2|L_t)=2.          (32)
```

## 5. Complete exceptional-line companion classification

Introduce

```text
A'= x_0+x_2,      B'=-x_1+x_2,
C'=-x_0+x_3,      D'= x_1+x_3.                          (33)
```

Exact contraction gives

```text
H_A=K A',        H_B=K B',        H_C=K C',        H_D=K D',

H_N=span{-x_0+x_1, x_2+x_3}.                           (34)
```

At the four one-dimensional companions, the relations and support filter
give

```text
A': B_(m_2)+B_(d_0)=B_(m_1)+B_(d_1)=0     => colour 2,
B': B_(m_1)+B_(d_1)=B_(m_2)+B_(d_2)=0     => colour 0,
C': B_(m_1)+B_(d_0)=B_(m_2)+B_(d_1)=0     => colour 2,
D': B_(m_2)+B_(d_1)=B_(m_1)+B_(d_2)=0     => colour 0. (35)
```

For the common line, write a general nonzero companion as

```text
q(u,v)=(-u,u,v,v) in H_N.                               (36)
```

The persistent relation `B_(d_0)-B_(d_2)=0` forces every such companion to
have colour `1`.  Thus `d_1` must be a coloop of its contraction family.
The full family has rank three exactly when `u!=0`.  The gcd of the
nonzero `3 x 3` minors after deleting `d_1` is

```text
4u(u-v)(u+v).                                           (37)
```

At `u=0`, the full and deleted ranks are both two.  At `u=v` and `u=-v`,
the full rank is three and the deleted rank is two.  These are the only
coloop directions:

```text
Q_+=-x_0+x_1+x_2+x_3,
Q_-=-x_0+x_1-x_2-x_3,                 both at colour 1. (38)
```

Consequently every necessary companion incidence is in the exact table

```text
low line     possible companion

A            A' at colour 2
B            B' at colour 0
C            C' at colour 2
D            D' at colour 0
N            Q_+ or Q_- at colour 1.                   (39)
```

These incidences are necessary; the table does not assert realizability.
For later use, direct contraction gives common residual covectors in
channel order `(m_1,m_2,d_0,d_1,d_2)`:

```text
low/companion   low combination       companion combination       ell

A,A'            -m_2-d_0-d_1          d_2                         -2x_1
B,B'            -m_2-d_1-d_2          d_0                          2x_0
C,C'            -m_1-d_0-d_1          d_2                          2x_1
D,D'            -m_1-d_1-d_2         -d_0                          2x_0
N,Q_+/-         -d_0+d_2             -m_1-m_2-d_1                  2(x_3-x_2).
                                                                    (40)
```

In every row, contracting the low and companion channel combinations gives
the same displayed nonzero `ell`.

## 6. The three load-bearing `Phi_1` incidences

By (32), choose a `Phi_1` low.  It is `A`, `B`, or `N`, so only

```text
(A,A'),                    (B,B'),                    (N,Q_+/-)      (41)
```

are needed for the endpoint.  Let the low `p` occur in mode `a`, its
companion `q` in mode `b`, and call the remaining modes `c,d`.  Use the
applicable covector `ell` in (40) and put

```text
(X,U,V)=(ell,x_4,x_5),              P=pol(XUV).          (42)
```

The channel coefficients in (40), together with the support filters, give
the full three-slot tensor identities

```text
P|_(L_a,L_c,L_d)=nu_e e_e^* tensor e_e^* tensor e_e^*,

P|_(L_b,L_c,L_d)=sum_(i in supp(p))
                 nu_i e_i^* tensor e_i^* tensor e_i^*, (43)
```

after harmlessly interchanging the names of the first slots.  Here `e` is
the forced companion colour and every displayed `nu` is nonzero.

Suppose first that `p` has support two.  Fixing `L_c,L_d`, the first-mode
slice map of `P` sends the companion-colour vector in `L_a` and the two
low-support colour vectors in `L_b` to nonzero multiples of the three
independent diagonal matrices.  Those three ambient vectors are therefore
independent.  On their span `Y`, (43) makes
`P|_(Y,L_c,L_d)` a concise weighted `Delta_3`, so `P=pol(XUV)` would have
tensor rank three.

This is impossible.  Its first-mode slice space is

```text
span{sym(UV),sym(XV),sym(XU)}.                          (44)
```

A rank-one symmetric matrix in (44) would be a nonzero scalar multiple of
`(aX+bU+cV)^2`; the three missing square coefficients force
`a=b=c=0`.  Thus (44) contains no nonzero rank-one matrix, while a concise
three-tensor of rank at most three would contain three.  Every low in (41)
is therefore singleton-supported.

## 7. Singleton slice dichotomy and factor gates

Let the low colour be `i`, the companion colour be `e`, and let

```text
t={0,1,2}\{i,e}.                                      (45)
```

For `v in K^6`, write

```text
bar(v)=(ell(v),x_4(v),x_5(v)) in E=K^3.
```

Define the slice map on the two untouched modes by

```text
S:E -> Mat_(3x3)(K),
S(w)_(kl)=P(w,bar(y_(c,k)),bar(y_(d,l))).               (46)
```

Equation (43) places nonzero multiples of `E_ee,E_ii` in `im S` and gives

```text
S(bar(y_(a,t)))=S(bar(y_(b,t)))=0.                     (47)
```

Hence `rank S` is two or three.  If it is three, then

```text
bar(y_(a,t))=bar(y_(b,t))=0.                           (48)
```

If it is two, its image is exactly `span{E_ee,E_ii}`.  For
`d=(X,U,V)`, the contraction matrix `c -> P(c,-,d)` is

```text
[ 0  V  U ]
[ V  0  X ]
[ U  X  0 ],                                           (49)
```

whose principal two-minors are `-V^2,-U^2,-X^2`.  Every nonzero `d` has
annihilator dimension at most one.  The two live diagonal cells and cross
zero cells make the colour-`e` and colour-`i` vectors independent on both
untouched shores.  Their common annihilators force

```text
bar(y_(c,t))=bar(y_(d,t))=0.                           (50)
```

The exact unused-colour factor gates for the three rows in (41) are

```text
g_(m_1)+g_(m_2)+g_(d_0)+g_(d_1)
                    =-x_1(x_0-x_2+x_3),

g_(m_1)+g_(m_2)+g_(d_1)+g_(d_2)
                    =-x_0(x_1+x_2-x_3),

-g_(d_0)+g_(d_2)=(x_0+x_1)(x_3-x_2).                  (51)
```

For `(A,A')`, `ell` is a nonzero multiple of `x_1`, and the first gate has
nonzero coefficients at both possible unused diagonals `d_0,d_1`.  For
`(B,B')`, `ell` is a multiple of `x_0`, and the second gate has nonzero
coefficients at `d_1,d_2`.  For `(N,Q_+/-)`, `ell` is a multiple of
`x_3-x_2`, and the third gate has nonzero coefficients at `d_0,d_2`.

In the rank-three case (48), the colour-`t` vectors in modes `a,b` have no
`A`-part and their `R`-parts lie in `ker(ell)`.  Full four-slot polarization
of the applicable gate at the all-colour-`t` entry factors as

```text
g(y_(a,t)^R,y_(b,t)^R) J(y_(c,t)^A,y_(d,t)^A)=0,       (52)
```

because the quadratic core is divisible by `ell`.  Equation (7) makes the
same channel combination a nonzero coefficient times `lambda_t`.

In the rank-two case (50), the identical argument uses the other two
shores:

```text
J(y_(a,t)^A,y_(b,t)^A) g(y_(c,t)^R,y_(d,t)^R)=0.       (53)
```

Again (51) gives zero and (7) gives a nonzero multiple of `lambda_t`.
Both cases are contradictions.  None of the necessary incidences (41) can
occur, contradicting the `Phi_1` rank drop in (32).  This proves Theorem 1.

## 8. Exact boundary

```text
field:                                                   CHARACTERISTIC ZERO;
based (4,2), e=1 frame 025:                              ASSUMED;
full five-sensor Delta_3 target:                         ASSUMED;

generic projection-kernel directions:                   EXCLUDED;
exceptional kernel lines:                                EXACTLY A,B,C,D,N;
rank-two mode in each mixed projection family:           PROVED NECESSARY;
all exceptional low-line companion incidences:           CLASSIFIED;
three load-bearing Phi_1 incidences:                      EXCLUDED;

exact extension of fixed-e=1 representative 025:         EXCLUDED;
fixed (4,2), e=2 representative 024:                     OPEN;
dimension-at-least-six co-two sensor residual:            OPEN;
unrestricted P_6 -> Delta_3:                             UNKNOWN;
global Krenn--Gu conjecture:                             UNRESOLVED.   (54)
```

## Replay

```powershell
python claims/arbitrary-order/verify_arbitrary_permanent_cotwo_r4_fixed_e1_full_extension_exclusion.py
python claims/arbitrary-order/audit_arbitrary_permanent_cotwo_r4_fixed_e1_full_extension_exclusion.py
python -m py_compile claims/arbitrary-order/verify_arbitrary_permanent_cotwo_r4_fixed_e1_full_extension_exclusion.py claims/arbitrary-order/audit_arbitrary_permanent_cotwo_r4_fixed_e1_full_extension_exclusion.py
python -m ruff check claims/arbitrary-order/verify_arbitrary_permanent_cotwo_r4_fixed_e1_full_extension_exclusion.py claims/arbitrary-order/audit_arbitrary_permanent_cotwo_r4_fixed_e1_full_extension_exclusion.py
```

The primary replay uses exact symbolic square-free arithmetic, determinants,
exceptional-line ranks, deletion minors, common-cell restrictions, residual
covectors, and factor gates.  The independent audit imports neither the
primary replay nor SymPy; it rebuilds the frame with rational arithmetic and
a separate polynomial determinant implementation, checks every incidence
and factor identity, and exhausts the two slice obstructions over two odd
finite fields as audit-only stress tests.  The written characteristic-zero
arguments above, not those finite-field stress tests, prove the theorem.
