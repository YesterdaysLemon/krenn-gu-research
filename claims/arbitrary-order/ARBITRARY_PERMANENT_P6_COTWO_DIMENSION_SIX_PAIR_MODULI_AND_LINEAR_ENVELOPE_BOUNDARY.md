# `P_6` co-two dimension-six pair moduli and linear-envelope boundary

## Status

**Exact characteristic-zero pair-level sharpness theorem and residual
assessment.**  In the square-free permanent algebra

```text
Z_6=K[x_0,...,x_5]/(x_0^2,...,x_5^2),                  (1)
```

the minimum surviving co-two value

```text
dim B_ab=6                                               (2)
```

does not admit a finite-orbit continuation of the equality-five strategy.
There is a nonempty nine-dimensional open family of full-support three-planes
`U` for which `(U,U)`, with the same colour basis on both sides, is already a
pair-level `Delta_3`-admissible dimension-six frame.  Ambient coordinate
monomial covariance has effective dimension at most five, so these unbased
pairs require at least four parameters modulo that covariance.

For every such frame, the mixed three-space `M` has a twelve-dimensional
orthogonal complement `M^perp` in square-free degree four.  The restricted
complement pairing on `B x M^perp` has rank three and saturates

```text
dim B+dim M^perp=6+12=18=binomial(6,2)+3.               (3)
```

This is only a **linear envelope**.  The theorem does not express `M^perp`
as the product sensor of four further local three-planes, does not satisfy the
other fourteen omitted-pair conditions, and does not construct a restriction
`P_6 -> Delta_3`.  The simultaneous factored mixed-target incidence remains
open.  Unrestricted `P_6 -> Delta_3` is **UNKNOWN**, and the global Krenn--Gu
conjecture remains **UNRESOLVED**.

## 1. Pair-level setup

Let `U,V` be three-planes in `(Z_6)_1` with ordered bases

```text
u_0,u_1,u_2,                 v_0,v_1,v_2.              (4)
```

Put

```text
B=UV=span{u_c v_d:0<=c,d<=2} subset (Z_6)_2.           (5)
```

A dimension-six pair is pair-level `Delta_3` admissible when the six mixed
products span a three-space

```text
M=span{u_c v_d:c!=d},                                  (6)
```

and the three diagonal classes

```text
u_c v_c+M,                         c=0,1,2,             (7)
```

form a basis of `B/M`.  These are exactly the mixed-radical and diagonal-
quotient conditions forced at one omitted pair by an actual restriction with
`dim B_ab=6`.  They are necessary at that pair, not sufficient for the other
four modes to exist.

## 2. A nonempty open family

For a three-plane `U`, square-free multiplication induces

```text
mu_U:Sym^2(U) -> (Z_6)_2.                               (8)
```

The condition `rank(mu_U)=6` is Zariski open on `Gr(3,6)`: in any affine
Grassmann chart it is the nonvanishing of at least one six-by-six minor of a
matrix whose entries are polynomial in the chart coordinates.

It is nonempty.  Take

```text
w_0=x_0+x_3,        w_1=x_1+x_4,        w_2=x_2+x_5,
U=span{w_0,w_1,w_2}.                                    (9)
```

In the column order

```text
w_0^2,w_1^2,w_2^2,w_0w_1,w_0w_2,w_1w_2                (10)
```

and edge-row order

```text
03,14,25,01,02,12,                                      (11)
```

the named minor is diagonal with entries

```text
2,2,2,1,1,1
```

and therefore has determinant `8`.  Characteristic zero makes this nonzero,
so (8) is injective at (9).  The plane (9) uses all six coordinates.  Full
active support is also an open condition, obtained by requiring that `U` not
lie in any coordinate hyperplane.  Thus

```text
Omega={U in Gr(3,6): rank(mu_U)=6 and supp(U)=[6]}       (12)
```

is a nonempty open subset.  Since `Gr(3,6)` is irreducible of dimension

```text
3(6-3)=9,                                               (13)
```

`Omega` has dimension nine.

## 3. Every plane in the open set gives an admissible equality-six pair

Fix `U in Omega` and any basis `w_0,w_1,w_2`.  Use

```text
(u_0,u_1,u_2)=(v_0,v_1,v_2)=(w_0,w_1,w_2).             (14)
```

Injectivity of (8) says that the six unordered quadratic products

```text
w_0^2,w_1^2,w_2^2,w_0w_1,w_0w_2,w_1w_2                (15)
```

are independent.  Hence `B=U^2` has dimension six.  The six ordered mixed
products in (6) repeat the three cross products in (15), so

```text
M=span{w_0w_1,w_0w_2,w_1w_2},             dim M=3.     (16)
```

The three squares are independent modulo (16), proving (7).  Therefore every
`U in Omega` gives a full-support pair-level `Delta_3`-admissible
dimension-six frame.

This phenomenon is structurally different from equality five.  There the
pair-product kernel has dimension four and the pair-level condition reduces
to finitely many active-support-four monomial orbits.  Here the ordinary
symmetric-square family already supplies an open collection of admissible
pairs.

## 4. The maximal linear complementary envelope

The degree-two/degree-four complement pairing

```text
< , >:(Z_6)_2 x (Z_6)_4 -> K                           (17)
```

is perfect.  For a frame from Section 3, define

```text
A_lin=M^perp subset (Z_6)_4.                            (18)
```

Perfectness and `dim M=3` give

```text
dim A_lin=15-3=12.                                      (19)
```

The left radical of the restricted pairing on `B x A_lin` is

```text
B intersect (A_lin)^perp=B intersect M=M,              (20)
```

so that pairing has rank `dim B-dim M=3`.  Equations (19)--(20) prove (3).
The three diagonal classes from (7) remain a basis of the quotient detected
by this pairing.

Thus the co-two dimension-sum inequality is sharp at the level of one
pair and an arbitrary linear complementary space.  The adjective *linear*
is load-bearing: an actual complementary sensor has the special form

```text
A_S=span{product_(i in S) u_(i,c_i):c_i in {0,1,2}},
|S|=4,                                                  (21)
```

and the theorem neither proves `A_S=A_lin` nor constructs four local planes
whose products realize (18).

## 5. A finite monomial-orbit classification is impossible

The source covariance used by the equality-five endpoint synthesis is the
coordinate monomial group

```text
G=(K^*)^6 semidirect S_6.                               (22)
```

Its connected torus has dimension six, while the common scalar acts
trivially on `Gr(3,6)`.  Hence every `G`-orbit in the Grassmannian has
dimension at most five.  The finite permutation factor does not increase
orbit dimension.

The family of unbased diagonal pairs

```text
{(U,U):U in Omega}                                     (23)
```

has dimension nine.  A finite union of monomial orbits, or of their
closures, has dimension at most five and cannot cover (23).  Consequently
the underlying admissible equality-six pairs have orbit codimension at
least four.  In particular, there is no finite list of monomial endpoint
representatives analogous to the six equality-five exchange classes.

This is a route obstruction, not a nonrestriction theorem.  A different
global invariant could still exclude the whole family at once.

## 6. Exact surviving obligation

The equality-five theorem proves that every omitted pair of a hypothetical
exact `P_6 -> Delta_3` restriction has `dim B_ab>=6`.  At a pair where
equality holds, its actual mixed radical and complementary product sensor
must satisfy

```text
dim M_ab=3,
A_S subset M_ab^perp,
dim A_S<=12,                                             (24)
```

with the three constant-colour quartics detecting the three diagonal
classes and all other colour words vanishing.  Sections 2--5 show that the
first two-mode half of this condition has moduli and that the ambient
twelve-dimensional linear envelope is not itself contradictory.

The next load-bearing problem is therefore the **factorized four-mode
incidence** in (21), together with compatibility across all fifteen omitted
pairs.  The five-map simultaneous-kernel criterion in
[`P6_SIMULTANEOUS_KERNEL_AND_NATURAL_LIFT_OBSTRUCTIONS.md`](../p6/P6_SIMULTANEOUS_KERNEL_AND_NATURAL_LIFT_OBSTRUCTIONS.md)
is an alternative global encoding of those mixed equations.  Neither that
criterion nor the present pair theorem makes the factorized incidence
automatic.

The minimal dimension-six branch is only the first residual stratum.
Product dimensions seven, eight, and nine remain possible a priori and have
larger mixed radicals.

## 7. Exact boundary

```text
full-support U with injective Sym^2(U) in Z_6:          NONEMPTY OPEN;
dimension of that Grassmann open:                      NINE;
(U,U) with a common basis pair-level Delta_3 admissible: PROVED;
pair-product dimension:                                SIX;
mixed-radical dimension:                               THREE;
maximal linear complementary envelope dimension:       TWELVE;
restricted complement-pairing rank:                    THREE;
dimension-sum bound 6+12=18:                           SHARP LINEARLY;
monomial orbit dimension:                              AT MOST FIVE;
pair-moduli codimension after monomial covariance:      AT LEAST FOUR;

factorization of M^perp by four local planes:           NOT CLAIMED;
compatibility across all fifteen omitted pairs:         OPEN;
finite monomial-orbit equality-six endpoint list:        IMPOSSIBLE BY DIMENSION;
unrestricted P_6 -> Delta_3:                           UNKNOWN;
global Krenn--Gu conjecture:                            UNRESOLVED.
```

## Replay

```powershell
python claims/arbitrary-order/verify_arbitrary_permanent_p6_cotwo_dimension_six_pair_moduli_and_linear_envelope.py
python -I claims/arbitrary-order/audit_arbitrary_permanent_p6_cotwo_dimension_six_pair_moduli_and_linear_envelope.py
python -m py_compile claims/arbitrary-order/verify_arbitrary_permanent_p6_cotwo_dimension_six_pair_moduli_and_linear_envelope.py claims/arbitrary-order/audit_arbitrary_permanent_p6_cotwo_dimension_six_pair_moduli_and_linear_envelope.py
python -m ruff check claims/arbitrary-order/verify_arbitrary_permanent_p6_cotwo_dimension_six_pair_moduli_and_linear_envelope.py claims/arbitrary-order/audit_arbitrary_permanent_p6_cotwo_dimension_six_pair_moduli_and_linear_envelope.py
```

The primary replay uses exact rational linear algebra to reconstruct the
square-free products, named determinant-eight minor, mixed radical, maximal
orthogonal envelope, and restricted rank.  The independent `python -I`
audit imports neither the primary nor SymPy; it rebuilds the products and
annihilator bases with standalone modular elimination at two primes.  These
bounded computations audit the displayed example and dimension arithmetic.
The open-family and orbit-dimension statements are proved above.
