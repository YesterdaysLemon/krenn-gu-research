# Arbitrary permanent co-two product-sensor rank-drop theorem

## Status

This is an exact arbitrary-order characteristic-zero necessary condition for
a weighted diagonal restriction

```text
P_r -> Delta_3,                 r >= 3.                 (1)
```

For every choice of two omitted modes, the products supplied by the other
`r-2` local pullback planes fail to span the full square-free degree-`r-2`
space.  Equivalently, every co-two product sensor is rank-deficient.  More
precisely, if `B_ab` is the two-mode product space and `A_S` is its
complementary product sensor, then

```text
dim B_ab >= 4,
dim A_S + dim B_ab <= binomial(r,2)+3,
dim A_S <= binomial(r,2)-1.                            (2)
```

For `r=6`, all fifteen four-mode product sensors therefore have rank at most
`14` rather than `15`.

The rank-drop locus is a proper closed locus in the ambient local-plane
space.  It is nevertheless not empty after imposing local rank and nonzero
pure products.  Thus (2) is a proved boundary, not a nonrestriction theorem:
unrestricted `P_6 -> Delta_3`, arbitrary-order permanent nonrestriction, and
the global Krenn--Gu conjecture remain **UNKNOWN/UNRESOLVED**.

## 1. Square-free permanent algebra

Let `K` have characteristic zero and put

```text
Z_r = K[x_0,...,x_(r-1)]/(x_0^2,...,x_(r-1)^2).       (3)
```

Write `(Z_r)_d` for its degree-`d` part.  If

```text
u_i = sum_p a_(i,p) x_p in (Z_r)_1,
```

then

```text
[x_0...x_(r-1)] product_i u_i = per(a_(i,p)).         (4)
```

The monomial bases give a perfect complement pairing

```text
< , > : (Z_r)_2 x (Z_r)_(r-2) -> K,
<x_p x_q, x_J> = 1 if J=[r] minus {p,q}, and 0 otherwise.  (5)
```

Suppose (1) exists.  Dually, each local map supplies three independent
linear forms

```text
u_(i,0), u_(i,1), u_(i,2) in (Z_r)_1                (6)
```

such that, for nonzero `lambda_0,lambda_1,lambda_2`, equation (4) is
`lambda_c` on the constant word `(c,...,c)` and zero on every nonconstant
word.  Independence in (6) follows from the rank-three one-mode flattening
of `Delta_3`.

Fix omitted modes `a,b`, put `S=[r] minus {a,b}`, and define

```text
B_ab = span{u_(a,c) u_(b,d) : c,d in {0,1,2}}
       subset (Z_r)_2,                                (7)

A_S  = span{product_(i in S) u_(i,c_i) :
            c_i in {0,1,2}}
       subset (Z_r)_(r-2).                            (8)
```

The pairing (5) restricted to `B_ab x A_S` is exactly the `2|(r-2)`
flattening of the pulled-back tensor.  Its rank is therefore three.

## 2. The degree-one annihilator lemma

### Lemma 1

For every nonzero `u in (Z_r)_1`,

```text
dim{v in (Z_r)_1 : uv=0} <= 1.                       (9)
```

If `u` has at least three nonzero coordinates, the dimension in (9) is
zero.

### Proof

Write `u=sum_p u_p x_p` and `v=sum_p v_p x_p`.  The equation `uv=0` says

```text
u_p v_q + u_q v_p = 0             for every p!=q.   (10)
```

If `u` has one nonzero coordinate `p`, (10) kills every `v_q`, `q!=p`,
and leaves only `K x_p`.  If its support is `{p,q}`, (10) kills all
coordinates of `v` outside that pair and leaves the one equation
`u_p v_q+u_q v_p=0`, again a line.

If `p,q,s` lie in the support, set `alpha_j=v_j/u_j`.  The three pair
equations give

```text
alpha_p+alpha_q=alpha_p+alpha_s=alpha_q+alpha_s=0.
```

Characteristic zero gives `alpha_p=alpha_q=alpha_s=0`.  Equations with
one of these indices then kill every other coordinate of `v`.  This proves
the lemma.  Notice that the argument is pointwise and permits arbitrary
algebraic coefficients.

## 3. Pair dimension and the co-two rank-drop theorem

### Lemma 2

For every omitted pair `{a,b}` in a restriction (1),

```text
dim B_ab >= 4.                                         (11)
```

### Proof

The three pure products

```text
d_c=u_(a,c)u_(b,c),                  c=0,1,2,          (12)
```

are independent modulo the left radical of the restricted pairing.  Pair
`d_c` with the complementary constant-`e` product.  The result is zero for
`c!=e` and `lambda_c!=0` for `c=e`.  Hence `dim B_ab>=3`.

Assume equality.  Since the restricted pairing has rank three, its left
radical in `B_ab` is zero.  For `c!=d`, the product

```text
u_(a,c)u_(b,d)                                        (13)
```

pairs to zero with every generator of `A_S`: every resulting target word is
nonconstant.  Thus (13) lies in the zero left radical and must itself be
zero.  Fixing `c=0` gives

```text
u_(a,0)u_(b,1)=u_(a,0)u_(b,2)=0.
```

But `u_(b,1),u_(b,2)` are independent, contradicting Lemma 1.  Therefore
`dim B_ab` is at least four.

### Theorem 3 (co-two product-sensor rank drop)

For every `S` of size `r-2` in every restriction (1), equations (2) hold.

### Proof

Let `N=dim (Z_r)_2=binomial(r,2)`.  For subspaces of a perfect `N`-by-`N`
pairing, the restricted rank is at least

```text
dim B_ab + dim A_S - N.                              (14)
```

The actual restricted rank is three.  Equations (11) and (14) give

```text
dim A_S <= N+3-dim B_ab <= N-1,                      (15)
```

which proves (2).

There is also a direct contradiction if one assumes `A_S=(Z_r)_(r-2)`.
Perfectness of (5) would make every mixed product (13) zero, and two such
products with the same nonzero first factor would again violate Lemma 1.

## 4. The rank-drop boundary is proper

The ambient product sensor can be full at every order.  Choose distinct
scalars `t_0,...,t_(r-1)` and the common three-plane spanned by

```text
a=sum_p x_p,
b=sum_p t_p x_p,
c=sum_p t_p^2 x_p.                                   (16)
```

Use this plane at each of the `r-2` sensor modes.  Its degree-`r-2`
products are the image of `Sym^(r-2)<a,b,c>`, whose dimension is
`binomial(r,2)`.

To prove that the image is all of `(Z_r)_(r-2)`, let

```text
L_p(X,Y,Z)=X+t_p Y+t_p^2 Z.                          (17)
```

The coefficient of the monomial missing `{p,q}` in
`(X a+Y b+Z c)^(r-2)` is, up to the common nonzero polarization factors,

```text
F_pq=product_(k notin {p,q}) L_k.                    (18)
```

The `binomial(r,2)` forms `F_pq` are linearly independent.  Indeed, evaluate
a proposed relation at the intersection `L_p=L_q=0`.  The Vandermonde
determinant says no third `L_k` passes through that point.  Every term in the
relation vanishes there except `F_pq`, and `F_pq` is nonzero.  Its coefficient
must vanish.  Repeating this for every pair proves independence.

Thus some maximal sensor minor is a nonzero polynomial in the ambient local
planes.  The simultaneous co-two rank-drop conclusion of Theorem 3 is a
genuine proper determinantal boundary, not a dimension identity.

## 5. Sharpness of what rank drop alone can say

At `r=6`, put

```text
U_0=U_1=U_2=span{x_0,x_1,x_2},
U_3=U_4=U_5=span{x_3,x_4,x_5}.                       (19)
```

All local planes have dimension three.  Give each block of three modes the
three cyclic coordinate bases.  Every constant colour then selects all six
source coordinates once, so all three pure coefficients are nonzero.  Yet
every four-mode product sensor has dimension at most nine, hence is
rank-deficient.

This is not a restriction to `Delta_3`.  The pulled-back tensor factors
across the first-three/last-three split as `P_3 tensor P_3`, so that split
has flattening rank one, while `Delta_3` has rank three.  Many mixed words
are nonzero as well.

Therefore local rank, nonzero pure coefficients, and even simultaneous
co-two rank drop do not prove nonrestriction.  Any completion of the P6
lane must use the mixed equations inside the rank-drop intersection, rather
than treating rank deficiency itself as a contradiction.

## 6. Consequence and exact boundary

For the live zero-surplus permanent node:

```text
every P_r -> Delta_3 co-two product sensor full:       IMPOSSIBLE;
every P_6 four-mode product sensor rank <=14:          PROVED;
ambient full product-sensor chart at every r>=3:       PROVED;
all-rank-drop plus local rank and pure nonvanishing:   INSUFFICIENT;
unrestricted P_6 -> Delta_3:                           UNKNOWN;
arbitrary-r permanent nonrestriction:                  UNKNOWN;
global Krenn--Gu conjecture:                            UNRESOLVED.
```

The theorem concerns the square-free permanent restriction algebra.  It is
not the balanced physical hafnian sensor, supplies no graph-extraction or
case-cover theorem, and does not reduce `P_6` to `P_5`.

## Replay

```powershell
python claims/arbitrary-order/verify_arbitrary_permanent_cotwo_product_sensor_rank_drop.py
python claims/arbitrary-order/audit_arbitrary_permanent_cotwo_product_sensor_rank_drop.py
python -m py_compile claims/arbitrary-order/verify_arbitrary_permanent_cotwo_product_sensor_rank_drop.py claims/arbitrary-order/audit_arbitrary_permanent_cotwo_product_sensor_rank_drop.py
python -m ruff check claims/arbitrary-order/verify_arbitrary_permanent_cotwo_product_sensor_rank_drop.py claims/arbitrary-order/audit_arbitrary_permanent_cotwo_product_sensor_rank_drop.py
```

The primary verifier checks the square-free pairing, symbolic annihilator
minors, concrete moment-curve full sensors through `r=8`, and the exact P6
block boundary.  The independent no-import audit uses star-configuration
intersection evaluation, separate modular row reduction, and a direct
support walk.  These bounded checks audit formulas and conventions; the
written arguments above prove the arbitrary-order theorem.
