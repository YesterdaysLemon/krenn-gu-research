# Component 21: raw zero-base finite-H22 extension-kernel normals

## Status

**Exact characteristic-zero raw-chart theorem.**  At the displayed finite
component-21 zero base

```text
p=q=0,                                               (1)
```

the finite-weight stacked `D01/D23` extension map is never injective.  Its
rank and complete kernel are classified below for every finite
`kappa,ell,lambda`.  For every projective leading direction in every kernel,
the complete first normal is empty for weighted `H22`, including arbitrary
subordinate extensions, all first-order variations of
`p,q,kappa,ell,lambda`, and all finite marking tangents.

This is a theorem about projective extension poles in the raw displayed
chart.  It is distinct from the existing first projectivized `(p,q)`-normal
blow-up theorem: that result starts with a nonzero base-normal direction and
transports it to the vertical-`U_0` replacement sheet.  Here the leading
base direction is zero while a projective extension direction lies in the
raw extension kernel; the next coupled normal may then contain subordinate
extensions and later `p,q` terms.

The central pure `P4` tensor is still zero and is not itself a projective
`P5` point.  Higher normals after a zero first normal, iterated simultaneous
base/extension blow-ups, component-parameter infinity, arbitrary source or
ambient degenerations, and the arbitrary-order local-to-global reduction
remain **UNKNOWN**.  The global Krenn--Gu conjecture remains **UNRESOLVED**.
No finite-field or numerical rank evidence is used.

## The raw extension map

Let `M(kappa,ell,lambda)` be the `32 x 8` matrix obtained by stacking the
finite `D01` and `D23` extension coefficient maps at (1), with columns

```text
(z_a0,z_a1,z_a2,z_a3,z_b0,z_b1,z_b2,z_b3).         (2)
```

### Ordinary weights `lambda!=+/-1`

The map has rank exactly seven for every `kappa,ell`.  Its kernel line is

```text
K_lambda=(0,0,0,1-lambda,0,0,lambda+1,0).          (3)
```

Two fixed rank-seven minors are

```text
-128*(lambda-1)^3*(lambda+1)^4*(ell^2-1),
-128*ell*(lambda-1)^4*(lambda+1)^3.                (4)
```

They cover all finite `ell`, since `ell` and `ell^2-1` never vanish
simultaneously.

### Weight `lambda=-1`

If `kappa!=0`, the map has rank six and complete kernel plane

```text
span{e_a3,e_b3}.                                   (5)
```

A fixed rank-six minor is `-4096*kappa`.  If `kappa=0`, the rank is five and
the complete kernel is

```text
span{e_a3,-e_a1+e_b0,e_b3};                       (6)
```

a fixed rank-five minor is `-1024`.  Neither assertion restricts `ell`.

### Weight `lambda=1`

If `ell^2!=1`, the map has rank five and complete kernel

```text
span{e_a2,-e_a0+ell e_b0+e_b1,e_b2}.              (7)
```

A fixed rank-five minor is `-1024*(ell^2-1)`.  At `ell=epsilon`,
`epsilon=+1,-1`, the rank is four and the complete kernel is (7) plus

```text
-e_a0-epsilon e_a1+e_b3.                          (8)
```

A fixed rank-four minor is `-256*epsilon`.

Equations (3)--(8) classify the complete projective extension-kernel spaces:
a line at ordinary weight, a `P1` or `P2` at `lambda=-1`, and a `P2` or
`P3` at `lambda=1`.

## Complete normals at ordinary weights

Freeze the leading direction (3) and form the complete `32 x 13` normal

```text
N=[M | partial_p(MK) | partial_q(MK) | partial_kappa(MK)
     | partial_ell(MK) | partial_lambda(MK)].       (9)
```

Both `D01` diagonal rows of `N` are identically zero.  Thus no mixed-free
normal can supply the required pure `D01` diagonal, irrespective of its
remaining rank.

For completeness, the mixed rank is nine except on
`kappa=0,ell=+/-1`, where it is eight.  Exact minors certify this
stratification.  On the exceptional points a universal extra mixed-kernel
vector has diagonal image

```text
(0,0,2(lambda-1),2 epsilon(lambda+1)),             (10)
```

but (10) still has zero `D01` diagonal pair.

## Complete normals at `lambda=-1`

For `kappa!=0`, write a leading direction in (5) as

```text
H=X e_a3+Y e_b3.                                   (11)
```

The complete normal has mixed rank nine if `Y!=0`, certified by the minor
`-131072*Y^3*kappa^2`, and mixed rank eight on the remaining point
`[X:Y]=[1:0]`, certified by `65536*kappa^2`.

For `kappa=0`, write a direction in (6) as

```text
H=X e_a3+Y(-e_a1+e_b0)+Z e_b3.                    (12)
```

Its mixed rank stratifies further with `(X,Y,Z,ell)`, but no rank
localization is needed for the incidence theorem: for the full symbolic
normal of (12), both `D01` diagonal rows are identically zero before any
mixed equation is imposed.  The same row identity holds for (11).  Hence
every point of both projective kernel spaces has empty weighted-`H22` first
normal.

## Complete normals at `lambda=1`

For `ell^2!=1`, write a direction in (7) as

```text
H=X e_a2+Y(-e_a0+ell e_b0+e_b1)+Z e_b2.           (13)
```

In the complete normal, `D23(0000)` has only one possible nonzero entry: in
the `dlambda` column it equals

```text
2(ell X+Y).                                        (14)
```

Two exact mixed rows have only that same column, with entries `2X` and
`-2Y`.  Therefore every mixed-free coefficient vector kills (14) whenever
`(X,Y)!=(0,0)`; if `X=Y=0`, (14) is already zero.  Thus `D23(0000)` vanishes
on the complete mixed kernel for every point of the `P2` in (7).

At `ell=epsilon`, add a coordinate `T` on the fourth generator (8):

```text
H=X e_a2+Y(-e_a0+epsilon e_b0+e_b1)+Z e_b2
  +T(-e_a0-epsilon e_a1+e_b3).                    (15)
```

Now `D23(0000)` has `dlambda` entry

```text
2(T+epsilon X+Y).                                  (16)
```

The three exact mixed-row entries in that column are

```text
2X, -2Y, 2 epsilon(T-epsilon X-Y).                 (17)
```

If any of `X,Y,T` is nonzero, (17) forces the subordinate `dlambda`
coefficient to vanish; if all three vanish, (16) is zero.  Hence
`D23(0000)` vanishes on the complete mixed kernel for every point of the
endpoint `P3` as well.

A genuine shared weighted-`H22` contraction requires a pure `D01` diagonal
and both opposite `D23` diagonals after its mixed coefficients vanish.
The identically zero `D01` rows at ordinary weight and `lambda=-1`, and the
missing `D23(0000)` row at `lambda=1`, exclude every complete first normal
above.

Finite marking changes act by invertible triangular transformations on the
binary coefficient rows and extension columns.  Their derivative on a
leading zero vanishes, while their derivative on the kernel direction is
absorbed by subordinate extensions.  No finite marking tangent is omitted.

## Compatibility and boundary

The existing normalized parameter compactification remains valid and is not
reproved here.  Its `(p,q)` blow-up replaces a nonzero base-normal direction
by a vertical plane and proves the resulting fibre empty.  The present raw
kernel theorem instead starts one valuation level earlier in the extension
coordinates and then retains `dp,dq` inside (9).  The two results are
compatible and cover different leading-order regimes.

This note does not promote a zero complete normal to an obstruction at every
higher order.  In particular, the ordinary-weight normals in (9) can be
identically zero after their mixed equations vanish.  Such iterated zero
normals remain part of the **UNKNOWN** higher-normal problem.

## Replay

```powershell
uv run --with sympy python claims/p5/frontier/verify_p5_component21_finite_h22_extension_zero_base_raw_kernel_normal_obstruction.py
uv run --with sympy python claims/p5/frontier/audit_p5_component21_finite_h22_extension_zero_base_raw_kernel_normal_obstruction.py
```

The primary uses the committed component-21 contraction builder.  The
no-import audit reconstructs the finite bases and every three-row permanent
by direct six-term permutation summation.
