# Complete affine classification of the disjoint mixed star

## Status

**Exact characteristic-zero reverse classification.**  Consider a nonzero
pure `P_4` restriction whose exceptional graph is the rank-one mixed star
with support pattern

```text
{01,01,23},                                          (1)
```

as in
[`P4_DISJOINT_MIXED_STAR_PURE_COMPONENT.md`](P4_DISJOINT_MIXED_STAR_PURE_COMPONENT.md).
On the full affine Borel chart where the first moving kernel row has nonzero
coefficient in the direction opposite `X_0+X_1`, every such tuple lies in
the closure of component eight.  This includes the rank-one fibers where
the old cross-product parameterization vanishes.

Thus the family in the component theorem is the complete affine stratum,
not merely a construction.  The complementary projective leaf chart remains
a separate boundary problem.

## Normalize the three exact pairs

Use the complementary binary directions

```text
a=X_0+X_1,       a_bar=X_0-X_1,
b=X_2+X_3,       b_bar=X_2-X_3.                    (2)
```

The mixed-star relations are

```text
x_1 y_3=0,       x_2 y_3=0,       y_0 x_3=0.       (3)
```

Their disjoint support pattern and the degree-one annihilator theorem
normalize

```text
y_0=b_bar,       x_1=x_2=a,
y_3=a_bar,       x_3=b.                             (4)
```

The all-active coefficient is nonzero, so a Borel shift by `b_bar` and row
scaling put the remaining row of `U_0` in the unique form

```text
x_0=A a+B a_bar+b-b_bar.                            (5)
```

Write a general first leaf kernel as

```text
y_1=lambda a+mu a_bar+f b+phi b_bar.                (6)
```

The forbidden coefficient `x_0 y_1 a b` is proportional to
`lambda+A f`.  On the affine chart `mu!=0`, rescale to `mu=1`; purity forces

```text
y_1=-A f a+a_bar+f b+phi b_bar.                     (7)
```

The same argument writes the second leaf kernel as

```text
y_2=-A j a+eta a_bar+j b+kappa b_bar.               (8)
```

No ansatz has been made: (5),(7),(8) are the general marked rows on this
chart after the two one-word purity equations.

## Purity is one `3 x 3` kernel incidence

Only four permanent coefficients can remain.  Direct squarefree
multiplication gives

```text
T_0000= 4(eta phi+kappa),

T_1000=-4(Bfj-Bkappa phi+eta f+eta phi+j+kappa),

T_1001=-4(A^2fj+B eta f+Bj+eta),

T_1111=4.                                           (9)
```

Hence all forbidden coefficients vanish exactly when

```text
N (j,kappa,eta)^T=0,                                (10)

N=
[ 0          1           phi   ]
[ Bf+1       1-Bphi      f+phi ]
[ A^2f+B     0           Bf+1  ].                   (11)
```

Its determinant is the irreducible component-eight equation

```text
Phi=A^2 B f phi^2+A^2 f^2-B^2 f^2+B^2 phi^2-Bf-1. (12)
```

Put

```text
delta=Bf+1,
J=f+B phi^2,
D=A^2f+B.                                           (13)
```

Then the determinant identity takes the especially transparent form

```text
Phi=D J-delta^2.                                    (14)
```

On the open set where the first two rows of `N` are independent, their
cross product is

```text
(j,kappa,eta)=(J,phi delta,-delta).                 (15)
```

Equations (12),(15) are exactly the family in the original component
theorem.  Thus every rank-two `N` point on this open set is component eight.

## The dependent-row rank-two boundary

The first two rows of `N` are dependent precisely when

```text
delta=J=0.                                          (16)
```

If `D!=0`, the matrix still has rank two and its unique kernel line is

```text
(0,-phi,1).                                         (17)
```

It is a limit of (15).  For example, let `delta` tend to zero, set
`f=(delta-1)/B`, and impose (14) by `J=delta^2/D`, with `D` tending to the
chosen nonzero value.  After scaling (15) by `-1/delta`, it tends to (17).
The required `A` and `phi` exist as formal power series because their
squares have nonzero constant terms.

## Every rank-one fiber is in the same closure

Since the first row of `N` never vanishes, rank one is equivalent to the
three equations

```text
delta=J=D=0.                                        (18)
```

They imply

```text
f=-1/B,       B phi=plus-or-minus 1,
A=plus-or-minus B.                                  (19)
```

The full projective kernel is

```text
P(ker N)={(h,-phi,1):h in C} union {(1,0,0)}.       (20)
```

Every point of (20) is a valuative limit of rank-two points from (15).
It is useful to see this without an existence theorem.  Fix `B=1` after
the harmless block scaling and let `t` be formal.

For a finite target `h`, put

```text
delta=t,
f=t-1,
phi=1-((h+1)/2)t,
J=f+phi^2,
D=delta^2/J,
A^2=(D-1)/f.                                        (21)
```

Then `D J=delta^2`, `A^2 -> 1`, `phi -> 1`, and

```text
-(1/delta)(J,phi delta,-delta) -> (h,-1,1).         (22)
```

The other sign choices in (19) follow by the binary source symmetries.  For
the projective endpoint, take instead

```text
delta=t^2,       f=t^2-1,       phi=1+t.            (23)
```

Now `J` has valuation one, while the last two entries of (15) have valuation
two, so its leading projective vector is `(1,0,0)`.  Again define
`D=delta^2/J` and `A^2=(D-1)/f`; both have the required limits.

Therefore the complete rank-one fiber, rather than merely one selected
kernel direction, belongs to the component-eight closure.

This is a small incidence-resolution phenomenon.  The determinant
hypersurface remembers only `det N=0`; its kernel-line graph resolves the
rank-one singular locus, and formal arcs fill the exceptional `P^1`.  The
same geometry appears in Springer resolutions of determinantal varieties,
but here all maps are the explicit permanent coefficients (9).

## Exact replay

```text
uv run --with sympy python verify_p4_disjoint_mixed_star_affine_classification.py
python audit_p4_disjoint_mixed_star_affine_classification.py
```

The primary verifier reconstructs (9)--(23), the determinant, the generic
kernel, the exact rank-one locus, and representative pair profiles.  The
independent audit uses rational matrix arithmetic and a subset-DP permanent.
Neither performs a parameter search or elimination.
