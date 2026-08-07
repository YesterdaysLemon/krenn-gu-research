# Classification of the one-double-endpoint star `(1,1,1)`

## Status

**Exact characteristic-zero orientation and support classification.**  Let a
nonzero pure `P_4` compression have all six pair-image ranks at least three,
and choose a rank-one exceptional star.  If exactly one of its three selected
relations is kernel--kernel, then the point is already in a certified
component closure.

More precisely, either an exterior leaf pair also has rank three, so a
completed rank-one or `(2,1,1)` triangle theorem applies, or the point is on
the dense overlapping-support radical-star chart already placed in one of
the split-cubic components `L_1,L_2,L_3`.  Thus the one-double-endpoint
orientation creates no new component orbit.

This theorem does not itself classify stars with exactly two double-endpoint
spokes, or the remaining no-double support collisions.  The subsequent exact
two-double theorem now closes the first of those.  Special `P_5` fibres and
the global Krenn--Gu conjecture remain **UNRESOLVED**.

## Orientation quotient

Center the selected star at mode zero and write `U_i=<y_i,x_i>`, with `y_i`
the pure-kernel row.  Relabel the leaves so that the unique double relation
is

```text
y_0 y_1=0.                                         (1)
```

The annihilator of a nonzero degree-one zero divisor is one-dimensional.
After interchanging leaves two and three, the other two strict relations
have exactly three orientations:

```text
C:  y_0 x_2=0,       y_0 x_3=0,                  common center,
M:  y_0 x_2=0,       x_0 y_3=0,                  mixed,
L:  x_0 y_2=0,       (x_0+t y_0)y_3=0.           common leaf. (2)
```

The parameter `t` is homogeneous: `t=0` means equal center factors, while
the endpoint at which the second factor becomes `y_0` changes the endpoint
signature and belongs to the separate two-double stratum.

Whenever an exterior edge has rank three, it completes a triangle with two
selected star edges.  Its third relation has coefficient rank one or two,
so the already complete triangle-`(1,1,1)` and triangle-`(2,1,1)` theorems
place the point in a certified component closure.  It remains only to rule
out a new minimal-star branch with exterior profile `(4,4,4)`.

## Common-center orientation

On singleton support, the common annihilator is the same singleton `e`.
Then `y_1=x_2=x_3=e`, and the all-active coefficient contains `e^2`; it is
zero.

On genuine binary support put

```text
A=X_0+X_1, C=X_0-X_1, B=X_2+X_3, D=X_2-X_3,
y_0=A,       y_1=x_2=x_3=C,
x_0=a_0C+b_0B+d_0D,
x_1=a_1A+b_1B+d_1D,
y_i=a_iA+b_iB+d_iD,  i=2,3.                       (3)
```

Purity includes

```text
b_0b_2-d_0d_2=0,       b_0b_3-d_0d_3=0.           (4)
```

Since `(b_0,d_0)` is nonzero at a nonzero active coefficient, (4) makes
`(b_2,d_2)` and `(b_3,d_3)` proportional.  Every `4 x 4` minor of the pair
product `U_2U_3` is divisible by

```text
b_2d_3-d_2b_3.                                    (5)
```

Thus `r_23<=3`; on the all-pair locus it equals three.

## Mixed orientation support ledger

Let `S` be the support of the exact pair `(y_0,y_1=x_2)` and `T` the support
of `(x_0,y_3)`.  Source and leaf symmetries leave the following complete
ledger.

| `S` | `T` | exact outcome |
|---|---|---|
| singleton | arbitrary | `U_1U_2` has a zero `e^2` column, hence rank at most three |
| binary | singleton inside `S` | zero/lower-pair, or `r_13=3` |
| binary | singleton outside `S` | purity puts `U_2,U_3` in one three-coordinate source space, so `r_23=3` |
| binary | same binary support | zero/lower-pair, or `r_13=3` |
| binary | overlapping binary support | purity removes both transverse coefficients of `U_2,U_3`, so `r_23=3` |
| binary | disjoint binary support | zero/lower-pair, or one of `U_2,U_3` is the fixed boundary plane; then an exterior pair has rank three |

For example, in the overlapping case normalize the two exact pairs to
supports `01` and `02`.  The forbidden coefficient `T_1011` is `-2d_3`,
while

```text
T_1111=d_1(c_3-2a_3),       T_1001=d_2(c_3-2a_3). (6)
```

Nonzero purity forces `d_1(c_3-2a_3)!=0` and `d_2=d_3=0`.  Both planes on
the exterior pair then live in `span(X_0,X_1,X_2)`.  The other rows of the
table are the same two-dimensional polar calculation; the verifier records
their exact coefficients without dividing by a support parameter.

## Common-leaf orientation

The projective line `P(U_0)` meets the degree-one zero-divisor locus in the
two selected center factors.  Its complete possibilities are:

1. one common support, where every factor lies in one binary coordinate
   plane;
2. equal factors on a second singleton or binary support;
3. two unequal overlapping binary supports, whose third factor is the
   unique closing edge of their source-coordinate triangle.

Disjoint supports admit no third factor, and coefficient-zero boundaries of
the binary cases are precisely the singleton cases.  This is the complete
projective support ledger.

If the double support is singleton, the coordinate-pencil branch has its
all-active coefficient in the ideal of two displayed forbidden coefficients;
the disjoint-binary branch is zero or makes `U_0=U_1`, hence lower-pair.
For binary double support, same-support and equal-overlap branches have zero
all-active coefficient.  Equal disjoint support either gives `r_23=3`, or
forces `r_12=3` or `r_13=3`.  Singleton endpoints also have `r_23<=3`.

Only the unequal-overlap source triangle requires a nontrivial split.  Put

```text
y_0=X_0+X_1,        y_1=X_0-X_1,
x_0=X_0+X_2,        y_2=X_0-X_2,
x_0-y_0=X_2-X_1,    y_3=X_2+X_1,                  (7)
```

and use the complete complementary rows

```text
x_1=a_1(X_0+X_1)+b_1X_2+d_1X_3,
x_2=a_2(X_0+X_2)+c_2X_1+d_2X_3,
x_3=a_3(X_2-X_1)+c_3X_0+d_3X_3.                  (8)
```

The four nonredundant forbidden coefficients generate an ideal with exactly
seven characteristic-zero minimal primes.  Exact radical reconstruction
places them as follows:

```text
primes 1,3,4,7:  all-active coefficient zero,
prime 2:          a selected or exterior pair has rank at most two,
primes 5,6:       boundary d_2=d_3=0 has r_23<=3;
                  on d_2d_3!=0 this is the dense overlapping radical star.
```

On the last dense open, the relations `x_0y_2=(x_0-y_0)y_3=0` have distinct
overlapping genuine-binary supports and independent center factors.  The
exact radical-star classification therefore places the tuple in one of
`L_1,L_2,L_3`.  No finite-field inference is involved.

## Consequence and boundary

Every point with exactly one double selected spoke is therefore routed to:

```text
lower-pair closure,
completed triangle-(1,1,1) or triangle-(2,1,1) closure,
or split-cubic L_1/L_2/L_3.                        (9)
```

All singleton limits and finite/projective support collisions that retain
exactly one double spoke occur in the ledger above.  The sole omitted
endpoint is where a strict center factor becomes `y_0`; intrinsically it has
two double spokes and is closed by the subsequent two-double classification.

## Replay

```text
uv run --with sympy python claims/p4/classifications/star/one-double-endpoint-star-111/verify_p4_one_double_endpoint_star_111_classification.py
uv run --with sympy python claims/p4/classifications/star/one-double-endpoint-star-111/audit_p4_one_double_endpoint_star_111_classification.py
```

The primary replay reconstructs every displayed permanent coefficient,
pair-rank implication, and the seven-prime radical decomposition over `Q`.
The no-import audit uses a separate subset-DP permanent, independently
rechecks the radical intersection over `Q`, and verifies rational dense
points on both surviving radical primes.  No finite-field result is used as
proof.
