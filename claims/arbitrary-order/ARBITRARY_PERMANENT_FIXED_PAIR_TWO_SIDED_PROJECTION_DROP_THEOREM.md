# Arbitrary permanent fixed-pair two-sided projection-drop theorem

## Status

This note proves an exact characteristic-zero strengthening of
`ARBITRARY_PERMANENT_FIXED_PAIR_DIMENSION_FIVE_FULL_PROJECTION_BOUNDARY.md`
for the same fixed equality-five two-mode pair.  Any exact
`P_6 -> Delta_3` restriction extending that pair must have a rank-drop mode
in **each** of the two mixed-factor projection families:

```text
min_(2<=t<=5) rank(Phi_1|L_t) <= 2,
min_(2<=t<=5) rank(Phi_2|L_t) <= 2.                         (1)
```

The earlier theorem proved only that the minimum over all eight ranks is at
most two.  The new point is an exhaustive localization when one family has
all four ranks equal to three.  The possible ranks in the other family are
split by the number of rank-two modes.  Zero or one such mode restores a
common missing factor.  Three or four are incompatible with exact target
contractions by the common kernel vector.  With exactly two, a sharp
hyperplane-plane product classification leaves one genuine cancellation
family; a second common-kernel contraction excludes it.

The proof uses the **full exact** `Delta_3` target tensor, not merely its
Hamming-one or Hamming-two shell.  It does not exclude the residual in which
both projection families have rank-drop modes, does not normalize every
dimension-five pair to this fixed pair, and does not prove unrestricted
`P_6 -> Delta_3` nonrestriction.  The global Krenn--Gu conjecture remains
**UNRESOLVED**.

## 1. Fixed pair, tensors, and projections

Let `K` be a field of characteristic zero and

```text
Z_6=K[x_0,...,x_5]/(x_0^2,...,x_5^2).                       (2)
```

At modes `0,1`, fix

```text
u_0=x_0-x_3,      u_1=x_1-x_3,      u_2=x_2-x_3,
v_0=x_1+x_2,      v_1=x_0+x_2,      v_2=x_2-x_3.            (3)
```

In edge order `(01,02,03,12,13,23)`, put

```text
m_1=(0,1,-1,0,0,-1),       m_2=(0,0,0,1,-1,-1),
d_0=(1,1,0,0,-1,-1),       d_1=(1,0,-1,1,0,-1),
d_2=(0,0,0,0,0,-2).                                      (4)
```

Write

```text
ell_1=x_3-x_2-x_0,                 ell_2=x_3-x_2-x_1,
Phi_1=(x_1,x_4,x_5,ell_1),         Phi_2=(x_0,x_4,x_5,ell_2).
                                                                  (5)
```

The five complementary quartics are

```text
star(m_1)= x_4x_5 x_1 ell_1,
star(m_2)= x_4x_5 x_0 ell_2,

star(d_0)= x_4x_5 (x_1+x_2)(x_3-x_0),
star(d_1)= x_4x_5 (x_0+x_2)(x_3-x_1),
star(d_2)=-2x_4x_5 x_0x_1.                               (6)
```

Let four independent local triples span planes `L_2,...,L_5 subset K^6`.
For `q` from (4), let `T_q` be the pullback of `star(q)` to the four local
colour spaces.  An exact extension of the fixed pair to `Delta_3` means

```text
T_(m_1)=T_(m_2)=0,
T_(d_c)=lambda_c e_c^* tensor e_c^* tensor e_c^* tensor e_c^*,
lambda_c != 0,                       c=0,1,2.              (7)
```

Every statement below is pointwise for planes and bases satisfying (7).

## 2. A hyperplane-plane product lemma

Let `E=K^4` with coordinate basis `z_0,...,z_3`, and use the square-free
algebra

```text
Z(E)=K[z_0,...,z_3]/(z_0^2,...,z_3^2).                    (8)
```

For subspaces `A,B subset E`, write `AB` for the span in `Z(E)_2` of all
products `ab`.  The degree-two space has the perfect edge-complement
pairing.

### Lemma 1 (hyperplane-plane products)

Assume `char K != 2`.  If `H subset E` is a hyperplane and `P subset E`
is a two-plane, then

```text
dim(HP) >= 3.                                             (9)
```

Equality holds precisely in one of the following two forms, up to a
permutation and nonzero rescaling of the coordinate vectors.

```text
A. H=W_i:=span{z_j:j!=i},              P subset W_i;

B. H=span{z_k,z_l,z_i+t z_j},          P=span{z_k,z_l},
   {i,j,k,l}={0,1,2,3},                t!=0.              (10)
```

In case A, `HP=W_i^2`.  In case B,

```text
HP=span{z_kz_l,
        z_iz_k+t z_jz_k,
        z_iz_l+t z_jz_l}.                               (11)
```

### Proof

Identify the dual of `Z(E)_2` with symmetric zero-diagonal `4`-by-`4`
matrices

```text
C=(c_ij),              c_ii=0.                           (12)
```

If `H=ker(alpha)`, then `C` annihilates `HP` exactly when

```text
C(P) subset K alpha.                                    (13)
```

Choose a basis `p,q` of `P`.  Substitution of (12) into (13) is a linear
system in

```text
(c_01,c_02,c_03,c_12,c_13,c_23).                        (14)
```

Row reduction, after permuting coordinates and rescaling the nonzero
coordinates of `alpha`, gives the exact table

```text
support(alpha)     dim(HP)=3 exactly when

1                  P subset ker(alpha);
2                  P is the coordinate plane on the two
                   coordinates outside support(alpha);
3 or 4             never.                               (15)
```

Here is an explicit chart check of the equality part.  On a Pluecker chart,
row-reduce the two basis vectors of `P` so a chosen pair of coordinate
columns is the identity.  If `alpha=z_0^*`, the only nonempty
rank-at-most-three charts have both pivots in `{1,2,3}`; the four-by-four
minors reduce to the two entries of `p,q` in coordinate `0`.  Their
vanishing says exactly `P subset W_0`.

If `alpha=z_0^*+z_1^*`, the only nonempty chart has pivots `(2,3)`.  Write
its rows as

```text
z_2+a z_0+b z_1,                 z_3+c z_0+d z_1.        (15a)
```

The four-by-four minors row-reduce to

```text
b^2, d^2, a+b, c+d.                                     (15b)
```

Over a field these force `a=b=c=d=0`, giving the complementary coordinate
plane.  For support size three or four every Pluecker chart contains a
nonzero constant among the reduced minors.  Thus rank below four occurs
exactly in (10).  The displayed product bases then have dimension three;
otherwise `dim(HP)>=4`.  This proves (9)--(15).

The following consequence will be used repeatedly:

```text
HP subset W_i^2  =>  H=W_i and P subset W_i.             (16)
```

Indeed, choose `0!=p in P intersect W_i`.  Writing a form as
`a z_i+x` with `x in W_i`, the coefficients of all `z_i z_j` in `hp`
force every `h in H` to have `a=0`.  Hence `H=W_i`; using all `h in W_i`
then forces every element of `P` to have zero `z_i` coefficient.

## 3. The sharp `(3,3,2,2)` permanent-zero classification

### Lemma 2 (two hyperplanes and two planes)

Let `H_0,H_1 subset E` be hyperplanes and `P_2,P_3 subset E` be
two-planes.  If the four-linear permanent tensor vanishes on

```text
H_0 x H_1 x P_2 x P_3,                                  (17)
```

then exactly one of the following occurs.

```text
I.  H_0=H_1=W_i and P_2,P_3 subset W_i for one coordinate i;

II. for a coordinate partition {i,j}|{k,l} and t!=0,

    P_2=P_3=P:=span{z_k,z_l},
    H_0=P direct-sum K(z_i+t z_j),
    H_1=P direct-sum K(z_i-t z_j).                        (18)
```

### Proof

Group (17) first as `(H_0P_2)(H_1P_3)`.  The two product spaces are
orthogonal under edge complementation.  Lemma 1 gives dimension at least
three for each, so both have dimension exactly three.  The crossed grouping
`(H_0P_3)(H_1P_2)` gives the same conclusion for the other two products.

If any one of these four equality cases is type A in Lemma 1, its product
is `W_i^2`.  Its orthogonal complement is again `W_i^2`; (16) forces the
opposite hyperplane and plane into `W_i`, and then forces the crossed pair
there as well.  This is I.

Otherwise all four equality cases are type B.  A type-B hyperplane has a
unique complementary coordinate plane from (10), so `P_2=P_3=P` and the
two hyperplanes use the same coordinate partition.  If their third lines
are `z_i+t z_j` and `z_i+s z_j`, direct pairing of (11) gives

```text
HP(t) perpendicular HP(s)  iff  s=-t.                    (19)
```

This is II.  The alternatives are disjoint and exhaustive.

## 4. Assuming one projection family has four full ranks

We prove that

```text
rank(Phi_1|L_t)=3 for all t=2,3,4,5                       (20)
```

is impossible under (7).

The zero tensor `T_(m_1)` and the full-rank hyperplane-product theorem from
the predecessor package force all four `Phi_1(L_t)` to be one common
coordinate hyperplane.  The missing coordinate cannot be `x_4` or `x_5`,
since then every pure tensor in (6) is zero.  It cannot be `x_1`, since
then `star(d_2)` is zero.  Therefore

```text
L_t subset ker(ell_1)                 for every t.        (21)
```

Inside `ker(ell_1)`, the kernel of `Phi_2` is the single line

```text
K N,                         N=x_2+x_3.                   (22)
```

Consequently every `Phi_2|L_t` has rank two or three, and it has rank two
exactly when `N in L_t`.  Call such a mode **low**.

If there are no low modes, the full-rank argument for `Phi_2` gives a
common missing coordinate.  If there is exactly one low mode, group two of
the three hyperplane images against the remaining hyperplane and the plane.
The hyperplane-hyperplane and hyperplane-plane product dimensions are both
at least three, so orthogonality forces equality.  The hyperplane product
is `W_i^2`; (16) puts the remaining hyperplane and plane in the same `W_i`.
Thus in both cases there is

```text
psi in {x_0,x_4,x_5,ell_2}
such that L_t subset ker(ell_1) intersect ker(psi) for all t. (23)
```

The exact 16-cell calculation in the predecessor theorem gives

```text
rank(C_(ell_1,psi) -> B^*) <= 2.                          (24)
```

But the three pure products in (7) give three independent functionals on
`B`, a contradiction.  Hence zero or one low mode is impossible.

## 5. Common-kernel contractions and the number of low modes

For a low mode `t`, write the fixed kernel vector in its colour basis as

```text
N=alpha_(t,0)y_(t,0)+alpha_(t,1)y_(t,1)
  +alpha_(t,2)y_(t,2).                                  (25)
```

Contracting `star(d_2)=-2x_4x_5x_0x_1` once with `N` gives zero.  Contracting
the target expression (7) in the same slot gives

```text
lambda_2 alpha_(t,2) e_2^* tensor e_2^* tensor e_2^*=0,
```

so

```text
alpha_(t,2)=0.                                          (26)
```

For two distinct low modes `s,t`, double contraction with `N,N` gives the
following exact bilinear identities obtained by contracting the quartics in
two modes:

```text
i_N i_N star(m_1)=i_N i_N star(m_2)=i_N i_N star(d_2)=0,

i_N i_N star(d_0)=i_N i_N star(d_1)=2J,                 (27)

J(y,z)=x_4(y)x_5(z)+x_5(y)x_4(z).                       (28)
```

The two target contractions in (27) are supported at different colour
matrix entries, `(0,0)` and `(1,1)`.  Their equality therefore implies

```text
alpha_(s,0)alpha_(t,0)=0,
alpha_(s,1)alpha_(t,1)=0.                               (29)
```

Together with (26) and `N!=0`, this says that, for every pair of low modes,
the two coefficient vectors in `K^{\{0,1\}}` are supported on different
singletons.  Three low modes are impossible by the pigeonhole principle.
Thus there cannot be three or four low modes.

Exactly two low modes remain.  After swapping the two modes, rescaling
their colour vectors, and possibly swapping colours `0,1`, equations
(25)--(29) say

```text
N=y_(s,0),                       N=y_(t,1).               (30)
```

## 6. The last cancellation family is impossible

With exactly two low modes, Lemma 2 applies to the two rank-three and two
rank-two `Phi_2` images.  Alternative I again gives (23)--(24), so only
alternative II could survive.  In `Phi_2` factor coordinates

```text
(z_0,z_1,z_2,z_3)=(x_0,x_4,x_5,ell_2),                  (31)
```

write its images as

```text
H_+=P direct-sum K(z_i+t z_j),
H_-=P direct-sum K(z_i-t z_j),
P,P.                                                     (32)
```

Contract the entire `B^*`-valued target tensor in the two low slots with
the two vectors in (30).  Every diagonal target contribution is zero:
`d_0` needs colour `0` in both slots, `d_1` needs colour `1` in both, and
`d_2` needs colour `2` in both.  The mixed contributions were already zero.
Hence the remaining bilinear sensor is identically zero.

By (27), its two equal potentially nonzero `B^*` coordinates are the `d_0`
and `d_1` coordinates, both `2J`.  Therefore

```text
J(H_+,H_-)=0.                                            (33)
```

In the coordinates (31), the radical of `J` is

```text
R=span{z_0,z_3}.                                        (34)
```

Two three-dimensional hyperplanes in a four-space that are mutually
orthogonal for this rank-two form must both contain its two-dimensional
radical: modulo `R`, each has image of dimension at most one.  Thus

```text
R subset H_+ intersect H_-=P.                            (35)
```

Both spaces in (35) have dimension two, so `P=R`.  The two original low
planes consequently have

```text
x_4=x_5=0.                                               (36)
```

Every quartic in (6) has the common factors `x_4x_5`.  Those two factors
would have to be supplied by the two high modes, but their pairing is
exactly `J`, which vanishes by (33).  All three pure coefficients are
therefore zero, contradicting (7).  This excludes alternative II and
completes the contradiction to (20).

## 7. Two-sided conclusion and exact boundary

Interchanging `x_0,x_1` swaps

```text
Phi_1 <-> Phi_2,       m_1 <-> m_2,       d_0 <-> d_1,
```

and preserves `d_2` and the exact diagonal target after swapping colours
`0,1`.  The argument therefore also excludes four full `Phi_2` ranks.
This proves (1).

The exact proved and open boundary is

```text
fixed pair, every exact Delta_3 extension:
  a rank-drop mode in the Phi_1 family:                 PROVED;
  a rank-drop mode in the Phi_2 family:                 PROVED;

simultaneous rank-drop residual (one or more in each):  OPEN;
classification of all dimension-five pair orbits:      NOT USED HERE;
unrestricted P_6 -> Delta_3:                            UNKNOWN;
global Krenn--Gu conjecture:                            UNRESOLVED.      (37)
```

Replay the exact checks with

```powershell
python claims/arbitrary-order/verify_arbitrary_permanent_fixed_pair_two_sided_projection_drop.py
python claims/arbitrary-order/audit_arbitrary_permanent_fixed_pair_two_sided_projection_drop.py
python -m py_compile claims/arbitrary-order/verify_arbitrary_permanent_fixed_pair_two_sided_projection_drop.py claims/arbitrary-order/audit_arbitrary_permanent_fixed_pair_two_sided_projection_drop.py
python -m ruff check claims/arbitrary-order/verify_arbitrary_permanent_fixed_pair_two_sided_projection_drop.py claims/arbitrary-order/audit_arbitrary_permanent_fixed_pair_two_sided_projection_drop.py
```

The primary verifier symbolically checks all five contractions, the common
kernel, the exceptional product-space orthogonality, the radical argument,
and the relevant row of the 16-cell sensor-rank table.  The independent
no-import audit uses separate modular arithmetic to exhaust the
hyperplane-plane equality cases and all `(3,3,2,2)` zero-permanent tuples
over `F_3`.  Those finite computations replay identities and conventions;
the written characteristic-zero arguments prove the theorem.
