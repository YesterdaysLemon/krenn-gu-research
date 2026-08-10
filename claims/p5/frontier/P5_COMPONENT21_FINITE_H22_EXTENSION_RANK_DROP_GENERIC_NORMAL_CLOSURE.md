# Component 21: generic finite-H22 extension rank-drop normals

## Status

**Exact characteristic-zero open-chart theorem.**  On the finite component-21
sheet, put

```text
p*ell*(ell^2-1) != 0.                              (1)
```

For the stacked finite-weight `D01/D23` extension map, the complete rank-drop
locus on this chart is

```text
lambda=1   or   (kappa=0 and lambda=-1).            (2)
```

Both loci have extension rank exactly seven, and their unique projective
kernel directions have empty complete first normal for weighted `H22`.
The first-normal statement allows arbitrary subordinate extension
coefficients and all first-order variations of `p,q,kappa,ell,lambda`.
Finite marking tangents are also included by triangular rank invariance.

This closes the generic finite-extension rank-drop chart (1), not its omitted
divisors.  The divisors `p=0`, `ell=0`, `ell=+/-1`, the zero base, component
parameter infinity, higher normals after a zero first normal, arbitrary
source or ambient degenerations, and the arbitrary-order local-to-global
reduction remain **UNKNOWN**.  The global Krenn--Gu conjecture remains
**UNRESOLVED**.  No finite-field or numerical rank evidence is used.

## The finite extension map

Let `M(p,q,kappa,ell,lambda)` be the `32 x 8` matrix obtained by stacking the
sixteen binary coefficients of the finite `D01` contraction above the
sixteen coefficients of finite `D23`.  The eight columns are ordered as

```text
(z_a0,z_a1,z_a2,z_a3,z_b0,z_b1,z_b2,z_b3).         (3)
```

Write

```text
A=(ell+1)*lambda-ell+1,
B=(ell+1)*lambda+ell-1.                             (4)
```

Three exact `8 x 8` minors of `M` are

```text
rows (2,3,16,17,18,20,21,24):
 -256*ell^2*p^4*(lambda-1)^4*(lambda+1)^3
     *(ell^2-1)*B,

rows (3,6,7,16,17,18,20,24):
 -256*ell*p^4*(lambda-1)^4*(lambda+1)^3
     *(ell^2-1)*A,

rows (2,3,7,16,18,20,22,24):
  256*kappa*p^3*(lambda-1)^6*A*B.                  (5)
```

If `lambda` is neither `+1` nor `-1`, the first two minors cannot both
vanish on (1), because `B-A=2(ell-1)`.  At `lambda=-1`, the last minor is
nonzero unless `kappa=0`, since `(A,B)=(-2ell,-2)`.  Conversely, the two
displayed vectors

```text
Z=(-p,0,0,0,-q,0,1,0)          at lambda=1,
W=(0,-1/ell,0,0,1/ell,0,0,1)  at kappa=0, lambda=-1   (6)
```

are exact kernel vectors.  Fixed `7 x 7` minors on the two loci are,
respectively,

```text
-16384*ell*p^5*(ell^2-1),
 16384*ell^3*p^3.                                  (7)
```

Thus (2) is exact and both kernels in (6) are lines throughout (1).

## The `lambda=1` complete first normal

At a centre on `lambda=1`, let `C_lambda=partial_lambda(MZ)`.  The universal
identity `MZ=0` gives

```text
partial_p(MZ)=M e_a0,   partial_q(MZ)=M e_b0,
partial_kappa(MZ)=partial_ell(MZ)=0.                (8)
```

Consequently the complete normal has the same column image as

```text
N_+ = [M | C_lambda].                               (9)
```

Delete the two diagonal words from each contraction block.  In the resulting
`28 x 9` mixed matrix, two fixed `7 x 7` minors, using columns
`(0,1,2,3,5,7,8)`, are

```text
rows (2,3,7,17,21,23,24):
 -8192*ell*p^5*q*(ell^2-1),

rows (2,3,7,17,21,23,26):
  8192*ell*p^5*(ell^2-1)*(ell*kappa*q+1).           (10)
```

They cover (1), because `q` and `ell*kappa*q+1` cannot both vanish.  The
mixed kernel is therefore exactly the span of

```text
e_b0,   -p e_a0 + e_b2.                            (11)
```

On these generators the four diagonal rows
`D01(0000),D01(1111),D23(0000),D23(1111)` are

```text
(0,0,0,4),   (0,0,0,4q).                           (12)
```

Only one `D23` diagonal can survive after all mixed coefficients vanish.
A genuine binary `H22` contraction requires both opposite diagonals, so the
complete first normal along `[Z]` is empty.

## The `kappa=0, lambda=-1` complete first normal

Here the universal identity is `MW=0`.  Component tangents in `p,q` vanish,
the `ell` derivative is absorbed by the extension columns, and the two
transverse columns are

```text
C_kappa=partial_kappa(MW),
C_lambda=partial_lambda(MW).                        (13)
```

Thus the complete normal has the same column image as

```text
N_- = [M | C_kappa | C_lambda].                     (14)
```

Its mixed matrix has the exact `8 x 8` minor

```text
rows    (2,3,7,18,19,20,22,24),
columns (1,2,3,4,5,6,8,9),
determinant = 32768*p^3*(ell^2-1).                  (15)
```

Two universal mixed-kernel vectors are `e_a0` and `W`, so (15) says they
are the complete mixed kernel on (1).  Their four diagonal row vectors are

```text
(0,0,4,0),   (0,0,0,0).                            (16)
```

Again only one of the two `D23` diagonals can survive, and the complete first
normal along `[W]` is empty for weighted `H22`.

Finite marking changes replace `b_i` by `b_i+h_i a_i`.  They act by
invertible triangular transformations on the binary coefficient rows and
extension columns.  Their derivative on a leading zero `MZ` or `MW`
vanishes, while their derivative on the kernel vector is absorbed by the
subordinate extension variables.  Hence no finite marking tangent is
missing from (9) or (14).

## Replay

```powershell
uv run --with sympy python claims/p5/frontier/verify_p5_component21_finite_h22_extension_rank_drop_generic_normal_closure.py
uv run --with sympy python claims/p5/frontier/audit_p5_component21_finite_h22_extension_rank_drop_generic_normal_closure.py
```

The primary builds the component-21 contraction matrices from the committed
finite bases.  The no-import audit reconstructs those bases and every
three-row permanent independently by direct permutation summation.
