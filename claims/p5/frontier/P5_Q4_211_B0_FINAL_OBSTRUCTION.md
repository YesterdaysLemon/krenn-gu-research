# Final obstruction on the `b=0` boundary of normalized `q4_211`

## Status

This note exactly excludes normalized `q4_211` over `C` on

```text
b=0,   a c != 0.                                    (1)
```

By singleton-colour symmetry it also excludes

```text
c=0,   a b != 0.                                    (2)
```

Together with the generic exclusion theorem, only the boundary

```text
a=0,   b c != 0
```

remains in normalized `q4_211`.

This does not exclude that last boundary, all normalized `q4_211`,
the other local strata of `P_5 -> Delta_3`, or the global Krenn--Gu
conjecture.

## The final marked architecture

Use the coordinate-normal labels and the result of
[`P5_Q4_211_B0_NONCOMMON_A_OBSTRUCTION.md`](P5_Q4_211_B0_NONCOMMON_A_OBSTRUCTION.md):

```text
L_A^*e_0^*=e_3,
L_B^*e_2^*=e_3,
h_2 in R_A,R_B,R_C,
L_D(s)=0,                                           (3)
```

where

```text
h_2=(c,0,0,0,-1),
s=e_1+e_2.
```

The row space at `A` contains `e_3,h_2`.  If the `h_2` target covector
there is `(r_A,p_A,0)`, independence from `e_0^*` gives

```text
p_A != 0.
```

Both rows annihilate `E=span(e_1,e_2)`, so

```text
L_A(E)=C e_2.                                       (4)
```

Put

```text
k=e_0+c e_4,
w=e_0-c e_4,
J=span(e_1,e_2,k).
```

The restriction at `D` has rank two on `J`: it kills `s`, while rank
one would put the forbidden coordinate normal `e_3` in `R_D`.

## The `h_2` rows at `B,C` have complementary pure colours

The tensor

```text
(u_0,e_3) contract P_5
```

is nonzero pure target colour zero through `B,C,D` and zero through
`A,C,D`.  Contract its nonzero version by the `h_2` rows at `B,C`.
Using

```text
(u_0,e_3,h_2,h_2) contract P_5=-2c s               (5)
```

and `L_D(s)=0`, the target-colour-zero components satisfy

```text
r_B r_C=0.                                         (6)
```

Triple contraction by `h_2` is zero.  Its target-colour-one
coefficient through `A,B,C`, together with `p_A!=0`, gives

```text
p_B p_C=0.                                         (7)
```

The covectors `(r_B,p_B,0)` and `(r_C,p_C,0)` are nonzero.  Equations
(6)--(7) therefore force exactly two cases:

```text
X: h_2 at B is e_0^*, h_2 at C is e_1^*;
Y: h_2 at B is e_1^*, h_2 at C is e_0^*.            (8)
```

## Two shared consequences

Let `Z` be the one of `B,C` whose `h_2` row is pure target colour one.
Then

```text
(u_1,h_2) contract P_5
 =-P_3(e_1,e_2,w)                                   (9)
```

maps through the other three modes to a nonzero pure `e_1^3` tensor.
At mode `A`, equation (4) says an `E` factor has target colour two.
Thus `A` must receive the unique factor `w`, while `D` receives an
`E` factor.  Since `D` kills `s`, its nonzero restriction to `E` has
rank one.  Therefore

```text
L_D(E)=C e_1.                                      (10)
```

The other simultaneous tensor is

```text
(u_2,e_3) contract P_5=P_3(e_1,e_2,k).             (11)
```

Using the colour-two `e_3` row at `B`, it maps through `A,C,D` to a
nonzero pure `e_2^3`.  Equation (10) forces `D` to receive the unique
factor `k`, so

```text
L_D(k) in C^*e_2.                                  (12)
```

On `J`, the row plane at `D` therefore has kernel `C s`.

## The zero chart has only two polar solutions

Using the colour-zero `e_3` row at `A`, the same source tensor (11)
maps to zero through `B,C,D`.  The restriction at `B` has rank one on
`J`; let its source functional be `g=(g_0,g_1,g_2)`.  Contracting
`P_3` by `g` gives

```text
M_g=[
 [  0, g_2, g_1 ],
 [g_2,   0, g_0 ],
 [g_1, g_0,   0 ]
].                                                   (13)
```

The restrictions at `C,D` have rank two.  Write `k_C` for the kernel
line at `C`; the kernel at `D` is `s`.  The vanishing of (13) between
their two row planes has only the following two relevant solutions:

```text
k_C=C d,  g=C k^*;
k_C=C s,  g=C s,                                    (14)
```

where `d=e_1-e_2`.  Indeed, in row-plane bases for `d^perp,s^perp`
and `s^perp,s^perp`, the two matrices are

```text
[[0,g_0+g_1],[g_0-g_1,0]],
[[-2g_2,g_0-g_1],[g_0-g_1,0]].
```

Their vanishing gives exactly (14).

## Excluding case `X`

In case `X`, the target-colour-zero row at `B` and
target-colour-one row at `C` make (9) simultaneously zero through
`A,C,D` and nonzero through `A,B,D`.

The nonzero version fixes the unique `w` factor at `A` and gives
`L_D(E)=C e_1`, as above.  In the zero version, separate the terms by
the target colour at `A`.  The terms assigning `w` to `A` force

```text
(L_C tensor L_D)Sym(e_1,e_2)=0.
```

Since the functional at `D` kills `s`, binary polarity gives

```text
L_C(d)=0.                                          (15)
```

Thus the first alternative in (14) holds and `g=C k^*`.  Modulo

```text
J^perp=span(e_3,h_2),
```

the functional `k^*` is represented by `e_0^*`.  Since

```text
u_2=2c e_0^*-h_2,
```

this puts `u_2` in `R_B`.

That is impossible by symmetry of (11).  Distinguished `u_2` with the
colour-two `e_3` row at `B` gives the nonzero tensor `e_2^3`, while
distinguished `e_3` with any pullback of `u_2` at `B` gives a multiple
of `e_1^3`.  The same nonzero source tensor cannot lie on both pure
target lines.  Hence case `X` is empty.

## Excluding case `Y`

In case `Y`, the nonzero version of (9) runs through `A,C,D`.  Again
`A` receives `w`, and the remaining binary image is pure
`e_1 tensor e_1`.  Since the functional at `D` kills `s`, this gives

```text
L_C(d) in C^*e_1.                                  (16)
```

The first alternative in (14) is incompatible with (16), so the
second holds:

```text
L_C(s)=0.                                          (17)
```

Equations (16)--(17) imply

```text
L_C(E)=C e_1.
```

Return to the required nonzero pure `e_2^3` image of (11) through
`A,C,D`.  By (10), `D` must receive `k`; hence `C` receives an
`E` factor.  But its image is target colour one, not target colour two.
The required `e_2^3` coefficient is zero, a contradiction.  Thus case
`Y` is empty as well.

## Consequence

The two cases in (8) are exhaustive, so the boundary (1) is empty.
Interchanging singleton colours proves the same for (2).

Combined with
[`P5_Q4_211_GENERIC_EXCLUSION_THEOREM.md`](P5_Q4_211_GENERIC_EXCLUSION_THEOREM.md),
the only normalized `q4_211` parameter stratum still open is

```text
a=0, b c != 0.
```

## Verification

Run:

```text
python claims/p5/frontier/verify_p5_q4_211_b0_final.py
python claims/p5/frontier/audit_p5_q4_211_b0_final.py
```

The primary verifier checks (5), (9), (11), the two polar systems
(14), and the binary cancellations in both cases.  The independent
audit repeats the target-label and polar calculation over `F_5,F_7`.
It enumerates no ambient maps or Grassmannians.  The finite-field
calculations audit the formulas; the proof above is over `C`.
