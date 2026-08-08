# The twelfth component has no generic marked `H31` lift

## Status

**Exact characteristic-zero generic-component theorem.**  The complete
marked-basis fibre over the generic point of the transverse binary-polarity
component is empty for `H31`.

Together with the earlier component theorems, all twelve currently certified
pure-`P_4` component orbits are now generically closed for `H31`.  The new
component's weighted `H22` fibre is subsequently closed by the direct
binary-polarity identity in
[`P5_H22_TRANSVERSE_COMMON_FACTOR_COMPONENT_GENERIC_OBSTRUCTION.md`](../../h22/transverse-common-factor/P5_H22_TRANSVERSE_COMMON_FACTOR_COMPONENT_GENERIC_OBSTRUCTION.md).
Special parameter/projective boundaries, component exhaustiveness, and the
global Krenn--Gu conjecture remain open.

## The component's intrinsic marking

Work over

```text
K=C(r,k)
```

and put

```text
a=X_0+X_1,       c=X_0-X_1,       b=X_2+X_3,
m=b+c,           m_r=b+(1+r)c,
d=(r+2)(k+1)X_1+X_2+kX_3,
n=-(k-1)(r+2)X_0-X_2+kX_3.                         (1)
```

The dense component normal form from
[`P4_TRANSVERSE_COMMON_FACTOR_COMPONENT.md`](../../../../P4_TRANSVERSE_COMMON_FACTOR_COMPONENT.md)
is

```text
U_0=span(n,c),
U_1=span(a,m),
U_2=span(a,m_r),
U_3=span(d,c).                                      (2)
```

The displayed rows already form intrinsic kernel/active pairs

```text
alpha=(n,a,a,d),          beta=(c,m,m_r,c).          (3)
```

Every compatible marked basis is, up to row scaling,

```text
alpha_i,
beta_i(h)=beta_i+h_i alpha_i,
h=(h_0,h_1,h_2,h_3).                               (4)
```

The restriction is independent of `r,k,h`:

```text
T_1111=-4,              T_w=0 for w!=1111.          (5)
```

Thus the whole affine marking chart is the polynomial ring

```text
S=K[h_0,h_1,h_2,h_3].                              (6)
```

## The extension row module

Delete source coordinate `j` and replace it by the fifth source coordinate.
The eight new entries form

```text
z=(x_0,x_1,x_2,x_3,y_0,y_1,y_2,y_3)^T.             (7)
```

Let `M_j(h)z` be the fourteen mixed binary coefficients, and let
`A_j(z),B_j(z)` be the all-kernel and all-active binary diagonals.  A binary
neighbor requires

```text
M_j z=0,                 A_j(z)B_j(z)!=0.           (8)
```

Polynomial row-module reduction over `S` gives, simultaneously for all four
deleted coordinates,

```text
A_j in Row_S(M_j),       B_j notin Row_S(M_j).       (9)
```

The reduced module sizes are

```text
(7,7,8,8).                                           (10)
```

This is an all-marking statement, including every divisor where a selected
maximal minor vanishes.

## The exact-zero-divisor structure

For the two coordinates in the shared binary block,

```text
A_0=A_1=0.                                          (11)
```

For the complementary deletions, the all-kernel rows are

```text
A_2=2k(1,r+2,r+2,1,0,0,0,0),
A_3=2(1,-k(r+2),-k(r+2),-1,0,0,0,0).               (12)
```

The reduced module for `j=2` contains

```text
(0,0,1,1,1,h_3,h_0,0),
e_0,e_1,e_2,e_3,e_4,
(0,0,0,0,0,1,0,h_0),
(0,0,0,0,0,0,-1,h_3),                              (13)
```

while the module for `j=3` contains

```text
(0,0,-1,-1,-1,h_3,h_0,0),
e_0,e_1,e_2,k e_3,k e_4,
(0,0,0,0,0,-1,0,h_0),
(0,0,0,0,0,0,-1,-h_3).                             (14)
```

Since `k` is a unit in `K`, (12)--(14) make both nontrivial memberships in
(9) immediate.  Therefore every solution of the mixed equations satisfies

```text
A_j(z)=0,                                           (15)
```

contradicting (8).  No ternary-rank test is reached.

The same exact pair `a c=0` that produced the component graph is responsible
for (11).  On the other two coordinates, binary polarity turns the remaining
kernel rows into standard-basis summands of the presentation module.  This is
the local commutative-algebra version of the general Fitting-module language
in the [Stacks Project, Section 15.8](https://stacks.math.columbia.edu/tag/07Z6):
the direct module inclusion is stronger than locating a generic rank-drop
divisor.

## The surviving active class

At the canonical marking and the rational component point `(r,k)=(1,2)`,
the mixed ranks are

```text
(6,6,7,7).                                          (16)
```

Adjoining `A_j` preserves them, whereas adjoining `B_j` raises them to

```text
(7,7,8,8).                                          (17)
```

Thus the module does not kill both pure diagonals.  Its cokernel retains the
all-active Segre vertex and kills precisely the opposite vertex required for
a binary neighbor.

## Proof boundary

This theorem closes the generic `H31` fibre of the twelfth component.  The
subsequent theorem linked above closes weighted `H22`.  Neither addresses
special values such as `k=0`, `k=+/-1`, or
`r=-2`, projective compactification boundaries, further pure components, or
the global prize problem.

## Verification

Run:

```text
uv run --with sympy python claims/p5/h31/transverse-common-factor/verify_p5_h31_transverse_common_factor_component_generic_obstruction.py
uv run --with sympy python claims/p5/h31/transverse-common-factor/audit_p5_h31_transverse_common_factor_component_generic_obstruction.py
```

The primary verifier reconstructs (1)--(12) and proves the four function-
field row-module statements over `C(r,k)[h_0,h_1,h_2,h_3]`.  The audit
imports neither its marked-row constructor nor its extension matrix; it
rebuilds permanents by subset dynamic programming and independently checks
the complete all-marking modules at `(r,k)=(1,2)` and `(2,3)`.  These
specializations corroborate the generic symbolic proof and are not a search.
