# Arbitrary permanent fixed-pair same-mode `N/N`, `q_+` exclusion

## Status

This note closes one exact characteristic-zero branch of the proportional
same-mode common-line residual at the fixed equality-five pair.  Suppose a
remaining local plane contains the common exceptional line

```text
N=K(x_2+x_3)
```

as the restricted kernel line of both mixed-factor projections.  The exact
target equations propagate this incidence to a colour-2 singleton companion
in

```text
span{x_0+x_1,x_2-x_3}.
```

There are two projective companion possibilities.  This note proves that

```text
q_+=x_0+x_1
```

is impossible, for both singleton- and support-two-supported occurrences of
`N`.  The sibling
[`q_-` exclusion](ARBITRARY_PERMANENT_FIXED_PAIR_SAME_MODE_NN_Q_MINUS_EXCLUSION_THEOREM.md)
treats the other projective companion.  The present theorem claims only the
`q_+` branch; a later synthesis may combine the two siblings with the
common/noncommon theorem.  It does not prove unrestricted permanent
nonrestriction.  The global Krenn--Gu conjecture remains **UNRESOLVED**.

Every double contraction below uses two distinct local modes.  Two vectors
from one local plane are never inserted into two tensor slots.  All fields
below have characteristic zero.

## 1. Fixed pair, notation, and predecessor inputs

Work in

```text
Z_6=K[x_0,...,x_5]/(x_0^2,...,x_5^2)
```

and split

```text
K^6=R direct-sum A,
R=span{x_0,x_1,x_2,x_3},       A=span{x_4,x_5},
J((r_4,r_5),(s_4,s_5))=r_4s_5+r_5s_4.                 (1)
```

At the fixed equality-five pair the five complementary quartics are

```text
star(m_1)= x_4x_5 x_1(x_3-x_2-x_0),
star(m_2)= x_4x_5 x_0(x_3-x_2-x_1),
star(d_0)= x_4x_5 (x_1+x_2)(x_3-x_0),
star(d_1)= x_4x_5 (x_0+x_2)(x_3-x_1),
star(d_2)=-2x_4x_5 x_0x_1.                            (2)
```

For the four remaining ordered local triples assume the full target
equations

```text
T_(m_1)=T_(m_2)=0,
T_(d_c)=lambda_c e_c^* tensor e_c^* tensor e_c^*
                         tensor e_c^*,
lambda_c!=0,                                      c=0,1,2. (3)
```

Put

```text
N=x_2+x_3,                    P=x_0-x_1,
M=x_0+x_1,                    L=-x_0-x_1-x_2+x_3,
h_0=-x_0+x_1+x_2+x_3,         h_1=x_0-x_1+x_2+x_3,
h_2'= -x_0+x_1-x_2+x_3,       k=-x_0+x_1+x_2-x_3.    (4)
```

The committed kernel-support theorem says that a local occurrence of `N`
misses colour `2` and has support one or two.  The committed singleton
propagation theorem supplies the companion when the support is one.  The
support-two extension in the sibling `q_-` package uses only the common
`N` contraction and supplies the same companion when the support is two.
For completeness, the exact localization is replayed next.

Contracting (2) with `N` gives

```text
m_1=m_2=d_2=0,          d_0=h_0,          d_1=h_1,    (5)
```

and

```text
ann_R(h_0,h_1)=span{M,x_2-x_3}.                       (6)
```

Thus the propagated colour-2 singleton is projectively

```text
q=sM+u(x_2-x_3),                    s!=0.              (7)
```

Its five residual covectors are

```text
m_1: sL-2u x_1,             m_2: sL-2u x_0,
d_0=d_1: (s+u)L,            d_2: -2sM.                (8)
```

The first four target contractions vanish and the last is nonzero.  If
`u!=0` and `s+u!=0`, the zero residuals span `L,x_0,x_1` and contain the live
residual `M`, impossible.  Hence

```text
q_+=M  (u=0),             or             q_-=M-x_2+x_3 (u=-s). (9)
```

Only `q_+` is treated below.  Put its colour-2 occurrence in mode `s`, put
the original `N` occurrence in a distinct mode `t`, and call the other modes
`u,v`.  Contraction by `q_+` gives, on `(t,u,v)`,

```text
C_L=0,                    C_M=nu e_2^* tensor e_2^* tensor e_2^*,
nu!=0.                                                        (10)
```

The common kernel of the two covectors is

```text
H=ker L intersect ker M=span{N,P}.                    (11)
```

Write `A_a` for the `2 by 3` matrix of `A`-projections in mode `a`, and

```text
G_ab=A_a^T J A_b.                                      (12)
```

## 2. The return plane cannot lie in the original `N` mode

Suppose first that `L_t` contains all of `H`.  Then `P` lies in `L_t`.
Let `(p_0,p_1,p_2)` be its coordinate row in the local basis of mode `t`.
The legal double contraction of `q_+=y_(s,2)` and `P` has zero left side in
all five channels, because both `L(P)` and `M(P)` vanish.  Its `d_2` target
is `p_2` times a nonzero pure colour-2 quadratic, so

```text
p_2=0.                                                  (13)
```

Let `Theta` send a residual covector to its cubic tensor on the three modes
other than `t`.  Direct contraction by `P` gives

```text
a=(1,-1, 1,-1),       b=(1,-1,-1, 1),
c=(1,-1,-1,-1),       d=(1,-1, 1, 1),
e=(2,-2, 0, 0),

e=a+b=c+d.                                              (14)
```

Here `a,b,c,d,e` are respectively the residuals of
`m_1,m_2,d_0,d_1,d_2`.  The mixed targets and (13) give

```text
Theta(a)=Theta(b)=Theta(e)=0,
Theta(d)=-Theta(c).                                    (15)
```

On the other hand the residuals of `d_0,d_1` after contraction by `N` are
`-c,d`.  If `(n_0,n_1,0)` is the nonzero local coordinate row of `N`, (3)
and (15) make the same cubic tensor equal to

```text
Theta(-c)=Theta(d)=n_0 lambda_0 e_0^3
                         =n_1 lambda_1 e_1^3.          (16)
```

The two displayed pure tensors are independent.  Equation (16) forces
`n_0=n_1=0`, contradicting `N!=0`.  This argument contracts `P` and `N` in
separate evaluations of the same slot; it never inserts them in two slots.
Henceforth

```text
L_t intersect H=K N.                                   (17)
```

## 3. The no-other-`H` quotient gate

Assume in this section that

```text
L_u intersect H=L_v intersect H=0.                    (18)
```

Put `D=R/H` and `W=D direct-sum A`, so `dim W=4`.  The images `U,V` of
`L_u,L_v` are three-dimensional hyperplanes in `W`.

Choose a local vector `z` in mode `t` whose colour is not `2` and whose
image in `W` is nonzero.  For singleton `N`, take the other colour among
`0,1`; for support-two `N=y_(t,0)+y_(t,1)`, take `y_(t,0)`.  If this image
were zero, (17) would fail.  Write the image as `(p,a) in D direct-sum A`.
Both contractions of (10) by `z` vanish on `U times V`.

### Lemma 1 (two zero forms on quotient hyperplanes)

Let `U,V` be hyperplanes in `W=D direct-sum A`, where both summands have
dimension two and `J` is nondegenerate on `A`.  For nonzero `(p,a) in W`,
suppose the two scalar components of

```text
B_(p,a)((d,b),(e,c))
 =p J(b,c)+d J(a,c)+e J(a,b)                           (19)
```

vanish on `U times V`.  Then one of the following holds:

1. `p!=0`, and `U=D direct-sum Kb`, `V=D direct-sum Kc` for nonzero
   `b,c in A` with `J(b,c)=0`;
2. `p=0`, `a!=0`, and
   `U=V=D direct-sum Kb`, where `Kb=ker J(a,-)`.

### Proof

If `p!=0`, choose coordinates `(x,y)` on `D` with `p=(1,0)` and put
`ell=J(a,-)`.  The two symmetric forms are

```text
F_0=J(A,A')+x ell(A')+x' ell(A),
F_1=y ell(A')+y' ell(A).                               (20)
```

Cross-vanishing on two hyperplanes forces each form to have rank at most
two: its restriction to one hyperplane maps into the one-dimensional
annihilator of the other, and one complementary vector adds rank at most
one.  If `J(a,a)!=0`, `F_0` has rank three, impossible.  If `a=0`, the
radical of `F_0` is `D`, and both hyperplanes are `D` plus mutually
orthogonal `A`-lines.

It remains that `a` is nonzero isotropic.  Choose hyperbolic coordinates
`A=K a direct-sum Kb`, write an `A` vector as `alpha a+beta b`, and normalize
`J(a,b)=1`.  Then

```text
F_0=(alpha+x) beta'+beta(alpha'+x'),
F_1=y beta'+beta y'.                                  (21)
```

The two radicals have one-dimensional intersection.  If `U!=V`, their
two-dimensional intersection lies in both radicals, a contradiction.
Thus `U=V`.  A hyperplane totally isotropic for both forms in (21) must be
`ker beta`: otherwise it would have to equal both `ker(alpha+x)` and
`ker y`.  Hence `U=V=D direct-sum K a`.

If `p=0`, then `a!=0` and the two forms are

```text
F_0=x ell'+x'ell,             F_1=y ell'+y'ell.        (22)
```

Their radicals again have one-dimensional intersection, so `U=V`; the
unique common totally isotropic hyperplane is `ker ell`.  This proves the
lemma.  Notice that (22), absent from the first `p!=0` chart, is essential.

Now contract (10) with the colour-2 vector `w=y_(t,2)`.  In bases

```text
u_i=(d_i,alpha_i b),          v_j=(e_j,beta_j c),      (23)
```

the resulting `D`-valued bilinear tensor is a nonzero fixed output vector
times `E_22`.  In the first chart of Lemma 1 it is

```text
c_0 beta_j d_i+d_0 alpha_i e_j.                       (24)
```

The maps `ker alpha -> D` and `ker beta -> D` are isomorphisms.  If
`c_0!=0`, restriction to `ker alpha` has two-dimensional output, contrary
to the one-output-line target; hence `c_0=0`.  Symmetrically `d_0=0`, and
(24) vanishes, contradicting the live target.

In the second chart `b=c`, and a possible pure term remains:

```text
c_0 beta_j d_i+d_0 alpha_i e_j+r h alpha_i beta_j,
h=J(b,b),                  r in D.                     (25)
```

When `c_0d_0!=0`, the half-shifts

```text
d_i -> d_i+(h/(2c_0))alpha_i r,
e_j -> e_j+(h/(2d_0))beta_j r                         (26)
```

absorb the last term and retain rank two on the two pure-`D` kernels.
The same output-line argument is impossible.  If exactly one of `c_0,d_0`
is zero, restriction to the other pure-`D` kernel is again surjective.
Consequently `c_0=d_0=0`, and (25) is live only if

```text
alpha proportional e_2^*,             beta proportional e_2^*. (27)
```

Thus the colour-0 and colour-1 vectors of both modes `u,v` have zero
`A`-part.  Contracting the original `N`, each live `d_0` or `d_1` pure
coefficient then has at most the companion mode `s` available as an
`A`-supplier.  Every quartic in (2) needs two distinct `A` suppliers, so
the coefficient is zero.  This contradicts `lambda_0!=0` or
`lambda_1!=0`.  The branch (18) is excluded.

## 4. Support-two `N`: the two `H` lines

Normalize the support-two occurrence by

```text
N=y_(t,0)+y_(t,1).                                    (28)
```

By Sections 2--3, some mode among `u,v` meets `H`; rename it `u` and choose
`0!=r in L_u intersect H`.  The legal `q_+,r` double contraction is zero,
so the colour-2 coefficient of `r` is zero.  Write

```text
r=aN+bP.
```

The legal `N,r` double contractions are

```text
2(a-b)G_sv=lambda_0 r_0 E_00,
2(a+b)G_sv=lambda_1 r_1 E_11.                         (29)
```

They cannot both be live.  Hence `r` is singleton-supported, and exactly
one of the following occurs:

```text
r_-=N-P=y_(u,0),                    G_sv=mu E_00,
r_+=N+P=y_(u,1),                    G_sv=mu E_11,      (30)
```

with `mu!=0`.  A two-dimensional intersection with `H` is also impossible,
because over the infinite field it contains a line other than the two in
(30).

It suffices by colour symmetry to exclude `r_-`.  The nonzero rank-one
pairing in (30) permits exactly three `A`-rank profiles for `(s,v)`:

```text
(2,1),                   (1,1),                   (1,2). (31)
```

In profile `(2,1)`, the colour-1 slice of the live `C_(h_1)` obtained from
(5) gives `G_su` proportional to `E_11`.  Thus `A_u` has rank one supported
only at colour `1`.  Also `A_s e_2=0` because `q_+=y_(s,2)`, and the
rank-one shore gives `A_v e_2=0`.  The pure `d_2` coefficient has only mode
`t` as a possible `A` supplier, contradiction.

In profile `(1,1)`, both rank-one shores in (30) are supported only at
colour `0`.  Hence `A_s e_1=A_v e_1=0`.  Legally contract the actual
pure-`R` vector `N` in mode `t`: the live `C_(h_1)` cell `(1,1,1)` on
`(s,u,v)` then has only mode `u` as a possible `A` supplier, so the cubic
coefficient vanishes, contradiction.

In profile `(1,2)`, the colour-1 slice of `C_(h_1)` gives

```text
G_uv proportional E_11,
```

so `A_u` has rank one supported only at colour `1`.  The live `q_+`
contraction at `u_2` then gives

```text
G_tv proportional E_22.                               (32)
```

The two zero columns of `G_sv` and `G_uv` make `A_v e_2` orthogonal to
both rank-one shore lines; (32) makes it nonzero, so those lines coincide.
Finally contract `r_-` in mode `u`.  Its zero residuals include

```text
h_2',                    k,                    P,       (33)
```

while its live `d_0` residual is a nonzero multiple of `h_0`.  At the
pure-`R` vector `y_(s,1)`, every corresponding target slice is zero and
`G_tv!=0`, so all four covectors in (33) and `h_0` vanish there.  Their
common kernel is `KM=Kq_+`, contradicting independence of
`y_(s,1),y_(s,2)`.  This closes `(1,2)`, and therefore `r_-`.  Swapping
`x_0,x_1` and colours `0,1` closes `r_+`.

## 5. Singleton `N`: localization of the `H` continuum

By colour symmetry put

```text
N=y_(t,0).                                             (34)
```

Again choose `0!=r in L_u intersect H` and write `r=aN+bP`.  Its colour-2
coefficient is zero.  The legal `N,r` double contraction gives

```text
2(a-b)G_sv=lambda_0 r_0 E_00,
2(a+b)G_sv=0.                                         (35)
```

If `r_0!=0`, then `G_sv!=0`, `a+b=0`, and the zero `d_1` residual of this
line forces `r_1=0`.  Thus

```text
r_-=N-P=y_(u,0),                G_sv=mu E_00.          (36)
```

If `r_0=0`, then `r=y_(u,1)` is an opposite-colour singleton.  The line
may be `N` itself; otherwise scale `b=1` and write

```text
r=rho N+P.                                             (37)
```

The same-colour line (36), the continuum (37), and the second-`N` endpoint
are treated in the next three sections.

## 6. Singleton same-colour cycle `r_-`

Keep the mode order `t,s,u,v` from (34), `q_+=y_(s,2)`, and (36).  The
pairing `G_sv=mu E_00` again gives the three profiles (31).

In profile `(2,1)`, `A_v e_1=A_v e_2=0`.  Slicing (10) at `v_2` gives

```text
M(v_2)!=0,             L(v_2)=0,
G_tu proportional E_22,                               (38)
```

and the slice at `v_1` gives `L(v_1)=M(v_1)=0`.  If `G_su=0`, the rank-two
map `A_s` forces `A_u=0`, contradicting (38).  Thus `G_su!=0`.  Contracting
the singleton `N` gives a live `C_(h_0)` and zero `C_(h_1)`; their
off-target slices at `v_1,v_2` force

```text
h_0(v_j)=h_1(v_j)=0,                  j=1,2.           (39)
```

The common kernel of `L,h_0,h_1` is
`K(M-x_2+x_3)`.  Since also `M(v_1)=0`, (39) makes `v_1=0`, contradicting
the local basis.

In profile `(1,2)`, `A_s e_1=0`.  Contract `r_-` in mode `u`.  At `s_1`,
the three zero residuals (33) and the off-target `h_0` slice show that, if
`G_tv!=0`, then `s_1` lies in their common kernel `KM=Kq_+`, impossible.
Hence `G_tv=0`.  Since `A_v` has rank two, `A_t=0`.  The three zero tensors
from (33) now reduce to

```text
ell|_(L_t) tensor G_sv=0,              ell=h_2',k,P.   (40)
```

Because `G_sv!=0`, the three-dimensional `L_t subset R` would lie in the
two-dimensional common `R`-kernel of those covectors, impossible.

In profile `(1,1)`, `A_v e_1=A_v e_2=0`.  Equation (10) gives
`G_tu` proportional to `E_22` and puts `v_1 in H`.  The `h_0,h_1` slices
from the singleton `N` give

```text
h_0(v_1)G_su=h_1(v_1)G_su=0.                          (41)
```

No nonzero vector of `H` annihilates both covectors, so `G_su=0`.  The
rank-one image of `A_s` then confines `A_u` to one orthogonal line, and the
nonzero `E_22` pairing makes `A_u` rank one supported only at colour `2`.
At pure colour `1`, modes `s,u,v` therefore have zero `A`-parts.  Only mode
`t` can supply an `A` factor, so the live `d_1` coefficient vanishes.
This closes the same-colour cycle.

## 7. Generic opposite-colour `H` line

For (37), contraction by `r=rho N+P` gives

```text
m_1: (1,-1, 1,-1),       m_2: (1,-1,-1, 1),
d_0: (rho-1)h_0,          d_1: (rho+1)h_1,
d_2: 2P.                                                (42)
```

The `d_1` target is live, so `rho=-1` is immediately impossible.  Assume
first `rho!=1` as well.  Equation (35) gives `G_sv=0`.  Neither `A_s` nor
`A_v` can have rank zero: the live `N,h_0` tensor followed by the zero
`N,h_1` tensor would make the corresponding `h_1` row zero, while the live
`r,h_1` tensor needs the same row.  Since `G_sv=0`, nondegeneracy of `J`
then forces both ranks to be one.

Write

```text
A_s=p alpha^T,                 A_v=q gamma^T,
J(p,q)=0,                      alpha_2=0.              (43)
```

Define rows on the indicated local triples by

```text
beta_j=J(p,A_u e_j),           delta_j=J(A_u e_j,q),
pi_i=J(p,A_t e_i),             epsilon_i=J(A_t e_i,q),
X=h_0R_s, Y=h_1R_s,            Z=h_0R_v, W=h_1R_v.     (44)
```

The legal contractions by `N` in mode `t`, in order `(s,u,v)`, and by `r`
in mode `u`, in order `(s,t,v)`, are exactly

```text
X tensor delta tensor gamma + alpha tensor beta tensor Z
  =lambda_0 e_0 tensor e_0 tensor e_0,
Y tensor delta tensor gamma + alpha tensor beta tensor W=0,

X tensor epsilon tensor gamma + alpha tensor pi tensor Z=0,
Y tensor epsilon tensor gamma + alpha tensor pi tensor W
  =lambda_1' e_1 tensor e_1 tensor e_1,                (45)
```

where `lambda_1'!=0`.  Quotient the first tensor factor by `K alpha`.
Because `alpha_2=0`, the first and fourth equations force

```text
alpha proportional e_0             or             alpha proportional e_1.
                                                               (46)
```

In the `e_1` branch, (45) successively gives

```text
delta,gamma proportional e_0,       epsilon=0,
pi,W proportional e_1,              Z=0,
Y=0,                                beta=0.            (47)
```

In the `e_0` branch it gives

```text
epsilon,gamma proportional e_1,     delta=0,
beta,Z proportional e_0,            W=0,
X=0,                                pi=0.              (48)
```

In (47), `A_u e_2 in p^perp=Kq` and
`A_t e_2 in q^perp=Kp`; in (48) the two memberships are interchanged.
Thus

```text
J(A_t e_2,A_u e_2)=0.                                (49)
```

The colour-2 columns of modes `s,v` vanish by (43), so (49) kills the pure
`d_2` coefficient, a contradiction.  This excludes every nonspecial line
in (37).

## 8. The special opposite-colour line `r_+=N+P`

At `rho=1`, the third equation of (45) disappears because the `d_0`
residual in (42) is zero.  The first, second, and fourth equations remain.
They still force (46).

If `alpha=e_1`, the three tensors give

```text
delta,gamma proportional e_0,       Y=0, beta=0,
pi,W proportional e_1.                                  (50)
```

Because `A_v e_2=0`, the `v_2` slice of (10) yields

```text
L(v_2)=0,              M(v_2)!=0,
G_tu proportional E_22.                                 (51)
```

Also `W_2=h_1(v_2)=0`.  The two mixed residuals in (42), sliced at `v_2`,
multiply the nonzero matrix `G_st=alpha pi^T`; hence they vanish on `v_2`.
The common kernel of those two covectors and `h_1` is `KM`.  But
`L(M)=-2`, so (51) forces `v_2=0`, contradicting `M(v_2)!=0`.

If `alpha=e_0`, the three tensors instead give

```text
epsilon,gamma proportional e_1,     delta=0,
beta,Z proportional e_0,            W=0.               (52)
```

Again (51) gives `G_tu` proportional to `E_22`.  The row `delta=0` puts
every `A_u` column in `q^perp`, while `beta_0!=0` says that `J(p,-)` is
nonzero on this one-dimensional line.  Since `beta_2=0`, it follows that
`A_u e_2=0`, contradicting the `(2,2)` entry of `G_tu`.  Thus the special
line is excluded too.

## 9. The second-`N` endpoints

### 9.1 A second `N` in a third mode

The remaining endpoint of the opposite-colour continuum in mode `u` is

```text
r=N=y_(u,1).                                           (53)
```

Equal singleton colours, or a support-two second occurrence, are already
impossible because the legal double contractions
`i_N i_N star(d_0)` and `i_N i_N star(d_1)` are the same nonzero quadratic
`2x_4x_5`, whereas their targets have incompatible colour support.

For (53), both double-contraction targets vanish and `G_sv=0`.  The
rank-zero shore argument of Section 7 again leaves ranks `(1,1)`.  The four
single-contraction tensors are exactly (45), now with the third equation
coming from the zero `h_0` tensor of the second `N` and the fourth from its
live `h_1` tensor.  Therefore (46)--(49) apply verbatim and kill the pure
`d_2` coefficient.  This is the q-independent collapsed two-singleton-`N`
lemma also replayed in the sibling `q_-` package.

### 9.2 A second `N` in the companion mode

There is one distinct legal-slot configuration not covered by (45): the
same companion mode may contain

```text
y_(s,1)=N,                    y_(s,2)=q_+=M,           (54)
```

while the original occurrence is `y_(t,0)=N`.  The two vectors in (54)
must be evaluated in separate contractions, never in separate tensor slots.

The legal double contraction of `N` in the distinct modes `t,s` makes the
same nonzero `2x_4x_5` residual in channels `d_0,d_1`, while both targets
vanish because the singleton colours differ.  Hence

```text
G_uv=0.                                                 (55)
```

Neither `A_u` nor `A_v` has rank zero.  If, for example, `A_u=0`, the live
contractions of `N=y_(s,1)` and `M=y_(s,2)` would both be a scalar row on
`L_u` times the same matrix `G_tv`; the former target is supported at
`(1,1,1)` and the latter at `(2,2,2)`, impossible.  Thus (55) and
nondegeneracy of `J` force ranks `(1,1)`.  Write

```text
A_u=u alpha^T,                 A_v=v gamma^T,
J(u,v)=0.                                               (56)
```

Put

```text
epsilon_i=J(A_t e_i,v),        pi_i=J(A_t e_i,u).
```

Because `y_(t,0)=N` is pure `R`,

```text
epsilon_0=pi_0=0.                                      (57)
```

The live `h_1` contraction of `N=y_(s,1)` and the live `M` contraction of
`q_+=y_(s,2)` have first-factor support `e_1` and `e_2`, respectively.
Their left sides have first factors only in `span{epsilon,pi}`.  Therefore
`epsilon,pi` are independent (and by (57) span `span{e_1,e_2}`).

The zero `h_0` contraction of `N=y_(s,1)`, in tensor order `(t,u,v)`, is

```text
epsilon tensor (h_0R_u) tensor gamma
 +pi tensor alpha tensor (h_0R_v)=0.                   (58)
```

Independence of `epsilon,pi` gives

```text
h_0R_u=h_0R_v=0.                                      (59)
```

Finally contract the original `N=y_(t,0)`.  Its `h_0` tensor on `(s,u,v)`
is live at `(0,0,0)`, but by (55) and (59) its exact left side is

```text
(h_0R_s) tensor G_uv
 +(h_0R_u) tensor G_sv
 +(h_0R_v) tensor G_su=0.                             (60)
```

This contradiction closes (54) using only legal single-slot evaluations.

## 10. Theorem and exact boundary

### Theorem 2 (same-mode `N/N`, `q_+` exclusion)

Under (1)--(3), suppose one remaining local plane contains `N` as the
common restricted kernel line for both mixed-factor projections.  If the
companion forced by (5)--(9) is projectively

```text
q_+=x_0+x_1,
```

then the target equations have no solution.

Indeed, Section 2 excludes a two-dimensional return in the original mode.
If neither of the other two modes meets `H`, Section 3 applies.  Otherwise
choose a nonzero `H` line in one of them.  Section 4 exhausts support-two
`N`.  For singleton `N`, (35)--(37) split the line into the same-colour
`r_-` cycle, the complete opposite-colour projective continuum (including
the exceptional `r_+` chart), and the second-`N` endpoint in a third mode;
Sections 6--9.1 exclude them all.  Section 9.2 separately closes a second
`N` in the companion mode, where treating `N` and `q_+` as two tensor slots
would be illegal.  This is an exhaustive characteristic-zero case cover.

The exact scope is

```text
same-mode common kernel line N/N:                       ASSUMED;
singleton or support-two local support of N:           EXHAUSTIVE;
forced companion q_+:                                  EXCLUDED;
forced companion q_-:                                  SIBLING THEOREM;
combined same-mode synthesis:                          NOT CLAIMED HERE;
unrestricted P_6 -> Delta_3:                           UNKNOWN;
global Krenn--Gu conjecture:                           UNRESOLVED.     (61)
```

## 11. Failed shortcuts and corrections retained

1. Finite-field sampling first suggested the no-`H` orbit, but it did not
   prove the hyperplane classification.  Lemma 1 is the characteristic-zero
   proof.
2. The initial `p!=0` chart missed the pure-`A` case `p=0`.  Equations
   (22), (25), and the half-shift (26) repair that omission.
3. A single zero bilinear gate does not align local colour support.  The
   proof uses both zero components and the full live `E_22` output line.
4. When a second `N` collapses a quotient shore, the no-`H` gate is not
   applicable.  Sections 7--9 use the uncontracted diagonal tensors.
5. Modular searches and random separating fixtures in the audit are stress
   evidence only.  They are not used as a proof or a case cover.

## 12. Exact replay

Run

```powershell
python claims/arbitrary-order/verify_arbitrary_permanent_fixed_pair_same_mode_nn_q_plus_exclusion.py
python claims/arbitrary-order/audit_arbitrary_permanent_fixed_pair_same_mode_nn_q_plus_exclusion.py
python -m py_compile claims/arbitrary-order/verify_arbitrary_permanent_fixed_pair_same_mode_nn_q_plus_exclusion.py claims/arbitrary-order/audit_arbitrary_permanent_fixed_pair_same_mode_nn_q_plus_exclusion.py
python -m ruff check claims/arbitrary-order/verify_arbitrary_permanent_fixed_pair_same_mode_nn_q_plus_exclusion.py claims/arbitrary-order/audit_arbitrary_permanent_fixed_pair_same_mode_nn_q_plus_exclusion.py
```

The primary verifier uses exact SymPy arithmetic to rebuild all contractions,
the companion and `H` spans, the missing `p=0` hyperplane chart, the
half-shift identity, every rank-profile kernel, and the generic and special
rank-`(1,1)` tensor forks.  It also compares the displayed tensor equations
with a direct complete-polarization evaluator.

The independent audit imports neither the primary verifier nor SymPy.  It
rebuilds the quartics from square-free monomial masks, uses `Fraction`
row-reduction and a separately written polarization routine, checks the
quotient radicals and coordinate forks on exact separating fixtures, and
enumerates the two hyperplane charts over a small finite field as explicitly
labelled stress evidence.  The scripts replay the displayed algebra; the
written characteristic-zero argument proves the theorem.
