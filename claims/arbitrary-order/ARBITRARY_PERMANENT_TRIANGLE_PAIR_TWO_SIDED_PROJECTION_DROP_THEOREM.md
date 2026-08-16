# Arbitrary permanent triangle-pair two-sided projection-drop theorem

## Status

This note proves an exact characteristic-zero obstruction for the
Delta-admissible `(3,1)` triangle pair in the `r=4` equality-five
classification.  Any exact `P_6 -> Delta_3` restriction extending the
displayed pair has a rank-drop mode in each of its two mixed-factor
projection families:

```text
min_(2<=t<=5) rank(Phi_1|L_t) <= 2,
min_(2<=t<=5) rank(Phi_2|L_t) <= 2.                         (1)
```

The two halves of (1) are not related by a coordinate symmetry.  When all
`Phi_2` ranks are three, the other projection has a one-dimensional common
kernel and the hyperplane/plane profile argument resembles the fixed
`(4,2)` proof.  When all `Phi_1` ranks are three, the other kernel is
two-dimensional.  Full `Phi_1` rank nevertheless makes every low kernel
line `K(x_3+sN)`.  Exact double contractions and the fixed noncoordinate
high hyperplane exclude the additional three-low profile.

The proof uses the full exact `Delta_3` target tensor.  It does not exclude
the residual in which both projection families have rank-drop modes, does
not classify the active-support-five or active-support-six pairs in `r=6`,
and does not prove unrestricted `P_6 -> Delta_3` nonrestriction.  The global
Krenn--Gu conjecture remains **UNRESOLVED**.

## 1. The triangle pair and its five complementary quartics

Let `K` be a field of characteristic zero and put

```text
Z_6=K[x_0,...,x_5]/(x_0^2,...,x_5^2).                       (2)
```

At modes `0,1`, take

```text
u_0=x_1-x_2,       u_1=x_3,          u_2=-x_0+x_2,
v_0=-x_1+x_2,      v_1=x_0+x_1,      v_2=x_3.                (3)
```

In edge order `(01,02,03,12,13,23)`, define

```text
m_1=(1,-1,0,-1,0,0),       m_2=(0,0,0,0,1,-1),
d_0=(0,0,0,2,0,0),         d_1=(0,0,1,0,1,0),
d_2=(0,0,-1,0,0,1).                                      (4)
```

Direct multiplication gives

```text
(u_i v_j)= [ d_0   m_1   m_2 ]
            [-m_2  d_1    0  ] .                           (5)
            [ m_1  -m_1  d_2 ]
```

Consequently

```text
B=UV=span{m_1,m_2,d_0,d_1,d_2},       dim B=5,
M=span{m_1,m_2},                       dim M=2,              (6)
```

and the three diagonal classes form a complement to `M`.

Put

```text
ell_1=x_2-x_1-x_0,                 ell_2=x_2-x_1,
Phi_1=(x_3,x_4,x_5,ell_1),         Phi_2=(x_0,x_4,x_5,ell_2).
                                                                  (7)
```

Edge complementation in six variables gives

```text
F_1=star(m_1)=x_4x_5 x_3 ell_1,
F_2=star(m_2)=x_4x_5 x_0 ell_2,

D_0=star(d_0)= 2x_4x_5 x_0x_3,
D_1=star(d_1)=  x_4x_5 x_2(x_0+x_1),
D_2=star(d_2)=  x_4x_5 x_1(x_0-x_2).                       (8)
```

Let four independent local triples span planes
`L_2,...,L_5 subset K^6`.  Pull each quartic in (8) back to the four local
colour spaces.  An exact extension to `Delta_3` says

```text
T_(m_1)=T_(m_2)=0,
T_(d_c)=lambda_c e_c^* tensor e_c^* tensor e_c^* tensor e_c^*,
lambda_c!=0,                           c=0,1,2.              (9)
```

All subsequent statements are pointwise for planes and ordered colour
bases satisfying (9).

If `phi_(k,0),...,phi_(k,3)` are the four covectors listed in `Phi_k`,
then direct polarization of (8) gives, for `y_t in L_t`,

```text
[x_0...x_5] m_k y_2y_3y_4y_5
 =per(phi_(k,s)(y_t))_(0<=s<=3, 2<=t<=5).                 (9a)
```

Thus `T_(m_k)=0` is the zero four-variable permanent tensor on the four
images `Phi_k(L_t)`.  Each restricted map is surjective onto its image, so
no information is lost when the profile lemmas below are applied there.

## 2. Hyperplane/plane zero-permanent profiles

Let `E=K^4` with coordinate basis `z_0,...,z_3`, and write `AB` for the
degree-two square-free product span of subspaces `A,B subset E`.

### Lemma 1 (hyperplane and hyperplane-plane products)

If `H,H' subset E` are hyperplanes and `P subset E` is a plane, then

```text
dim(HH')>=3,                    dim(HP)>=3.                  (10)
```

Equality in the first inequality holds precisely when

```text
H=H'=W_i:=span{z_j:j!=i}.                                  (11)
```

Equality in the second holds precisely in one of the following forms, up
to coordinate permutation and nonzero coordinate rescaling:

```text
A. H=W_i and P subset W_i;

B. H=span{z_k,z_l,z_i+t z_j},       P=span{z_k,z_l},
   {i,j,k,l}={0,1,2,3},             t!=0.                  (12)
```

Moreover,

```text
HP subset W_i^2       implies       H=W_i and P subset W_i. (13)
```

### Proof

Identify the dual of the six-dimensional degree-two space with symmetric
zero-diagonal `4`-by-`4` matrices.  If `H=ker(alpha)`, such a matrix `C`
annihilates `HP` exactly when

```text
C(P) subset K alpha.                                       (14)
```

Choose a basis of `P` and row-reduce (14) in the six off-diagonal entries
of `C`.  Normalize the support of `alpha` by coordinate rescaling.  On
each Pluecker chart of the plane, the rank-at-most-three locus is

```text
|supp(alpha)|=1:  P subset ker(alpha);
|supp(alpha)|=2:  P is the coordinate plane on the two
                   coordinates outside supp(alpha);
|supp(alpha)|=3,4: empty.                                  (15)
```

For completeness, in the only nontrivial support-two chart take
`alpha=z_0^*+z_1^*` and write

```text
P=span{z_2+a z_0+b z_1, z_3+c z_0+d z_1}.
```

The decisive maximal minors reduce to

```text
b^2, d^2, a+b, c+d,
```

so `a=b=c=d=0`.  In support three or four, every chart has a nonzero
constant maximal minor.  This proves the second classification in
(10)--(12).  Its two product spaces have the displayed bases

```text
W_i^2,

span{z_kz_l,
     z_iz_k+t z_jz_k,
     z_iz_l+t z_jz_l},                                    (16)
```

and hence dimension three.

For two hyperplanes with independent normals `alpha,beta`, every symmetric
form vanishing on their product is

```text
c alpha alpha^T+e beta beta^T.
```

The zero-diagonal equations cut out a space of dimension at most two, so
the product dimension is at least four.  When the normals are proportional
to `alpha`, every annihilating symmetric form is

```text
alpha z^T+z alpha^T.
```

Its zero-diagonal equations give product dimension

```text
2+|supp(alpha)|,
```

which is three only for a coordinate normal.  This proves (11).

Finally choose `0!=p in P intersect W_i`.  The coefficients of `z_i z_j`
in all products `hp` force every `h in H` to have zero `z_i` coefficient.
Thus `H=W_i`; multiplying all of `W_i` by `P` then forces `P subset W_i`.
This proves (13).

### Corollary 2 (the profiles used below)

If the four-variable permanent vanishes on four hyperplanes, they are all
one coordinate hyperplane.

If it vanishes on three hyperplanes and one plane, the three hyperplanes
are one coordinate hyperplane `W_i` and the plane lies in `W_i`.

If it vanishes on two hyperplanes `H_0,H_1` and two planes `P_2,P_3`, then
exactly one of the following holds:

```text
I.  H_0=H_1=W_i and P_2,P_3 subset W_i;

II. for a coordinate partition {i,j}|{k,l} and t!=0,

    P_2=P_3=P=span{z_k,z_l},
    H_0=P direct-sum K(z_i+t z_j),
    H_1=P direct-sum K(z_i-t z_j).                          (17)
```

### Proof

Group the four factors in pairs and use the perfect edge-complement
pairing.  The two product-space dimensions sum to at most six.  Lemma 1
makes both dimensions at least three, so both equal three.

For four hyperplanes, (11) applies to both pairs and their coordinate
product spaces can be orthogonal only when the omitted coordinate agrees.
For three hyperplanes and one plane, one product is `W_i^2`; (13) puts the
remaining hyperplane and plane in the same `W_i`.

For the last profile, apply both the direct and crossed pairings.  If any
hyperplane-plane equality is type A, (13) gives I.  Otherwise all four are
type B.  The plane associated with a type-B hyperplane is unique, so
`P_2=P_3=P`.  If the two remaining lines are `z_i+t z_j` and
`z_i+s z_j`, direct edge-complement pairing of (16) gives `s=-t`.  This is
II.  The alternatives are disjoint and exhaustive.

## 3. The double common-factor sensor table

Let

```text
f in {x_3,x_4,x_5,ell_1},       g in {x_0,x_4,x_5,ell_2},
K_(f,g)=ker(f) intersect ker(g).                            (18)
```

Let `C_(f,g)` be the span of all fourfold square-free products of vectors
from `K_(f,g)`, and pair it against `B` by full-monomial extraction.  In
the basis `(m_1,m_2,d_0,d_1,d_2)`, the exact sensor ranks are

```text
                         g
                  x_0   x_4   x_5   ell_2
f       x_3        1     0     0      2
        x_4        0     0     0      0
        x_5        0     0     0      0
        ell_1      1     0     0      1.                   (19)
```

Indeed, a row or column involving `x_4` or `x_5` has zero sensor.  In the
other four cells, write

```text
K_(f,g)=K_0 direct-sum span{x_4,x_5}.
```

After extracting `x_4x_5`, bases of `K_0^2` and their pairing rows are

```text
(x_3,x_0):
  K_0^2=span{x_1x_2},
  [0 0 0 1 -1];

(x_3,ell_2):
  K_0^2=span{x_0x_1+x_0x_2, 2x_1x_2},
  [0 0 0 1  1],
  [0 0 0 2 -2];

(ell_1,x_0) and (ell_1,ell_2):
  K_0^2=span{2x_1x_2, x_1x_3+x_2x_3},
  [0 0 0 2 -2],
  [0 0 0 0  0].                                           (20)
```

Thus every double common-factor sensor has rank at most two.  If all four
local planes lie in one `K_(f,g)`, their three constant-colour products
would induce three independent functionals on `B` by (9), contradicting
(19).

We also use two immediate single-factor observations:

```text
L_t subset ker(x_3) for all t  => T_(d_0)=0;
L_t subset ker(x_0) for all t  => T_(d_0)=0.                (21)
```

## 4. Four full `Phi_2` ranks are impossible

Assume

```text
rank(Phi_2|L_t)=3,                    t=2,3,4,5.             (22)
```

The zero tensor `T_(m_2)` and Corollary 2 force the four `Phi_2(L_t)` to
be one common coordinate hyperplane.  Omitting `x_4` or `x_5` kills all
three tensors `D_c`, while omitting `x_0` kills `D_0`.  Therefore

```text
L_t subset ker(ell_2)                 for every t.           (23)
```

Inside `ker(ell_2)`, the kernel of `Phi_1` is the line

```text
K N,                         N=x_1+x_2.                     (24)
```

Hence every `Phi_1|L_t` has rank two or three, and it has rank two exactly
when `N in L_t`.  Call such a mode low.

For a low mode write

```text
N=sum_(c=0)^2 alpha_(t,c)y_(t,c).                          (25)
```

Single contraction gives

```text
i_N D_0=0,
```

so (9) and `lambda_0!=0` imply

```text
alpha_(t,0)=0.                                             (26)
```

For two distinct low modes, double contraction gives

```text
i_N i_N D_0=0,
i_N i_N D_1= 2J,
i_N i_N D_2=-2J,

J(y,z)=x_4(y)x_5(z)+x_5(y)x_4(z).                         (27)
```

The last two target contractions are supported at the distinct colour
entries `(1,1)` and `(2,2)`.  Since they are negatives of the same
bilinear tensor, both vanish.  Thus

```text
alpha_(s,1)alpha_(t,1)=alpha_(s,2)alpha_(t,2)=0.            (28)
```

Every nonzero coefficient vector in (25) is supported in `{1,2}`.
Equations (28) make three low modes impossible.

If there are zero low modes, Corollary 2 applied to `T_(m_1)=0` gives a
common omitted `Phi_1` coordinate.  With one low mode, the
hyperplane-hyperplane-hyperplane-plane case of the same corollary gives the
same conclusion.  In either case all four planes lie in

```text
ker(ell_2) intersect ker(f),
f in {x_3,x_4,x_5,ell_1},                                 (29)
```

contradicting the sensor table (19).

Exactly two low modes remain.  Equations (26)--(28) let us normalize their
kernel vectors as

```text
N=y_(s,1),                         N=y_(t,2).                (30)
```

Apply the last case of Corollary 2 to the two rank-three and two rank-two
`Phi_1` images.  Alternative I again yields (29).  In alternative II, use
factor coordinates

```text
(z_0,z_1,z_2,z_3)=(x_3,x_4,x_5,ell_1)                    (31)
```

and denote the two high hyperplanes by `H_+,H_-` and the common low plane
by `P`.

Contract (9) in the two low slots with the vectors (30).  Every diagonal
target contribution is zero, while (27) shows that the remaining ambient
bilinear sensor is `2J`.  Hence

```text
J(H_+,H_-)=0.                                             (32)
```

The radical of `J` in (31) is

```text
R=span{z_0,z_3}.                                          (33)
```

Two mutually `J`-orthogonal hyperplanes must both contain `R`: modulo
`R`, each has nonzero image in a nondegenerate two-space, and neither image
can have dimension two.  In alternative II their intersection is `P`, so
`R subset P`; dimensions give `P=R`.

The two low original planes therefore have `x_4=x_5=0`.  In every quartic
in (8), the factors `x_4,x_5` must then be supplied by the two high modes,
but their two assignments sum to `J(H_+,H_-)=0`.  All three pure tensors
vanish, contradicting (9).  This excludes (22).

## 5. Four full `Phi_1` ranks are impossible

Assume instead

```text
rank(Phi_1|L_t)=3,                    t=2,3,4,5.             (34)
```

The zero tensor `T_(m_1)` again supplies one common omitted factor.
Omitting `x_4` or `x_5` kills every pure tensor, and omitting `x_3` kills
`D_0`.  Hence

```text
L_t subset ker(ell_1)                 for every t.           (35)
```

On `ker(ell_1)` one has

```text
x_2=x_0+x_1,                    ell_2=x_0.                  (36)
```

Since `Phi_1|L_t` has rank three and its last coordinate vanishes, the
restrictions of `x_3,x_4,x_5` form a basis of `L_t^*`.  In particular,
`x_4,x_5` are independent on every `L_t`.  Thus every `Phi_2|L_t` has rank
at least two.

In `Phi_2` factor coordinates

```text
(z_0,z_1,z_2,z_3)=(x_0,x_4,x_5,ell_2),                   (37)
```

all images lie in the fixed noncoordinate hyperplane

```text
bar H={z_3=z_0}.                                           (38)
```

A rank-three image is exactly `bar H`; call it high.  A rank-two image is
a plane; call it low.  The kernel line of a low mode lies in

```text
ker(ell_1) intersect ker(Phi_2)=span{N,x_3}.               (39)
```

But `Phi_1|L_t` is injective and `Phi_1(N)=0`, so this line is never `KN`.
It has a unique normalized generator

```text
K_t=x_3+s_t N.                                             (40)
```

Write its local colour coordinates as

```text
K_t=sum_(c=0)^2 alpha_(t,c)y_(t,c).                        (41)
```

For two low modes `s,t`, exact double contraction gives

```text
i_(K_s)i_(K_t)D_0=0,
i_(K_s)i_(K_t)D_1= 2s_s s_t J,
i_(K_s)i_(K_t)D_2=-2s_s s_t J.                            (42)
```

The zero `D_0` contraction gives the colour-zero instance of (43).  The
last two target tensors have disjoint colour supports, so their common
bilinear tensor is zero and the other two instances also hold:

```text
alpha_(s,c)alpha_(t,c)=0,                 c=0,1,2.          (43)
```

The nonempty colour supports of distinct low kernel vectors are pairwise
disjoint.  Four low modes are therefore impossible.

With no low modes, `T_(m_2)=0` would make the four copies of `bar H` one
coordinate hyperplane, contrary to (38).  With one low mode, the
three-hyperplane/one-plane case of Corollary 2 gives the same contradiction.
With two low modes, alternative I in (17) again makes `bar H` coordinate,
while alternative II has two distinct high hyperplanes in characteristic
zero; they cannot both equal `bar H`.

It remains to exclude exactly three low modes.  Equation (43) says their
kernel vectors have singleton supports at the three different colours
`0,1,2`.  If `s_t=0`, then `K_t=x_3`, and

```text
i_(x_3)D_1=i_(x_3)D_2=0.                                 (44)
```

The nonzero target contractions in (9) show that such a vector cannot have
colour `1` or `2`; it must have colour `0`.  Consequently the low kernel
vectors of colours `1` and `2` have nonzero parameters in (40).  Applying
(42) to those two modes gives

```text
J(P,bar H)=0,                                              (45)
```

where `P` is the remaining low `Phi_2` image and `bar H` is the sole high
image.

For `J=z_1 tensor z_2+z_2 tensor z_1`, the orthogonal complement of
`bar H` is its radical `span{z_0,z_3}`.  Its intersection with `bar H` is
the line `K(z_0+z_3)`.  Equation (45) would put the two-plane `P` inside
that line, a contradiction.  This excludes (34).

## 6. Conclusion and exact boundary

Sections 4 and 5 prove (1).  The exact proved and open boundary is

```text
displayed triangle pair, every exact Delta_3 extension:
  a rank-drop mode in the Phi_1 family:                 PROVED;
  a rank-drop mode in the Phi_2 family:                 PROVED;

simultaneous rank-drop residual:                        OPEN;
finer based-frame stabilizer orbits of the (3,1) type:  OPEN;
active-support-five/six equality-five pairs in r=6:     OPEN;
unrestricted P_6 -> Delta_3:                            UNKNOWN;
global Krenn--Gu conjecture:                            UNRESOLVED.      (46)
```

Replay the exact checks with

```powershell
python claims/arbitrary-order/verify_arbitrary_permanent_triangle_pair_two_sided_projection_drop.py
python claims/arbitrary-order/audit_arbitrary_permanent_triangle_pair_two_sided_projection_drop.py
python -m py_compile claims/arbitrary-order/verify_arbitrary_permanent_triangle_pair_two_sided_projection_drop.py claims/arbitrary-order/audit_arbitrary_permanent_triangle_pair_two_sided_projection_drop.py
python -m ruff check claims/arbitrary-order/verify_arbitrary_permanent_triangle_pair_two_sided_projection_drop.py claims/arbitrary-order/audit_arbitrary_permanent_triangle_pair_two_sided_projection_drop.py
```

The primary verifier checks the pair table, all five complementary
quartics, both restricted kernels, the common-factor sensor table, every
`N` and `x_3+sN` contraction, and the two radical arguments with exact
symbolic algebra.  The independent no-import audit uses separate modular
row reduction to exhaust the hyperplane/plane profile classifications over
`F_3`, independently replays the contraction identities over three odd
fields, and checks the sensor ranks with exact rational arithmetic.  The
finite computations audit conventions and transcription; the written
characteristic-zero arguments prove the theorem.
