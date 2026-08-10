# Component 21: finite-H22 extension normals at `ell=0,+/-1`

## Status

**Exact characteristic-zero divisor theorem.**  Assume `p!=0` on the finite
component-21 sheet and put `ell` equal to `0`, `+1`, or `-1`.  On each of
these three omitted divisors, the stacked finite-weight `D01/D23` extension
map has rank drop exactly on

```text
lambda=1   or   (kappa=0 and lambda=-1).           (1)
```

Every projective leading extension direction on both loci has empty complete
first normal for weighted `H22`.  This includes arbitrary subordinate
extension coefficients, every first-order variation of
`p,q,kappa,ell,lambda`, and all finite marking tangents.

This closes the extension-rank and first-normal problem only on the three
displayed divisors with `p!=0`.  The divisor `p=0`, the zero base, component
parameter infinity, higher normals after a zero first normal, arbitrary
source or ambient degenerations, and the arbitrary-order local-to-global
reduction remain **UNKNOWN**.  The global Krenn--Gu conjecture remains
**UNRESOLVED**.  No finite-field or numerical rank evidence is used.

## Exact rank-drop classification

Let `M(p,q,kappa,ell,lambda)` be the stacked `32 x 8` extension map, with
columns

```text
(z_a0,z_a1,z_a2,z_a3,z_b0,z_b1,z_b2,z_b3).        (2)
```

On `ell=0`, two `8 x 8` minors are

```text
rows (2,3,7,16,17,20,22,24):
 256*p^4*(lambda-1)^5*(lambda+1)^3,

rows (2,3,16,18,20,22,24,26):
-256*kappa^2*p^2*(lambda-1)^8.                    (3)
```

For `ell=epsilon`, `epsilon=+1,-1`, use

```text
rows (6,7,16,17,18,20,21,24):
-256*epsilon*p^4*(lambda-1)^4*(lambda+1)^4,       (4)
```

and rows `(2,3,7,16,18,20,22,24)`, whose determinant is

```text
 epsilon=+1:  1024*lambda^2*kappa*p^3*(lambda-1)^6,
 epsilon=-1: -1024*kappa*p^3*(lambda-1)^6.        (5)
```

Equations (3)--(5) prove injectivity away from (1).  Conversely, at
`lambda=1` the universal kernel vector is

```text
Z=(-p,0,0,0,-q,0,1,0).                            (6)
```

On `ell=0` it is the complete kernel line: a fixed `7 x 7` minor is
`-16384*p^5`.  At `ell=epsilon`, the map has rank six, with complete kernel
plane spanned by `Z` and

```text
V_epsilon=(0,-epsilon,-epsilon,0,-epsilon,-1,0,1); (7)
```

a fixed `6 x 6` minor is `4096*epsilon*p^4`.

At `kappa=0,lambda=-1`, the complete kernel is a line.  Its generator and a
fixed rank-seven minor are

```text
ell=0:       W_0=(0,-1,0,0,1,0,0,0),  -16384*p^2,
ell=epsilon: W_e=(0,-epsilon,0,0,epsilon,0,0,1),
             16384*epsilon*p^3.                   (8)
```

Thus (1) is the exact rank-drop locus on all three divisors.

## The `ell=0` first normals

Along `[Z]` at `lambda=1`, all component derivatives are zero or absorbed by
the extension columns; only `C_lambda=partial_lambda(MZ)` is transverse.
For

```text
N_0+=[M | C_lambda],                               (9)
```

the mixed matrix has rank seven.  Rows
`(3,6,7,17,21,23,26)` and columns `(0,1,2,3,5,7,8)` give determinant
`8192*p^5`.  Its mixed kernel is exactly

```text
span{e_b0, -p e_a0+e_b2}.                         (10)
```

On these vectors the four diagonal rows
`D01(0000),D01(1111),D23(0000),D23(1111)` are

```text
(0,0,0,4), (0,0,0,4q).                            (11)
```

Along `[W_0]` at `kappa=0,lambda=-1`, the `ell` derivative is `-M e_b3`
and the `p,q` derivatives vanish.  Hence the complete normal has the same
column image as

```text
N_0-=[M | partial_kappa(MW_0) | partial_lambda(MW_0)]. (12)
```

Its mixed rank is eight: rows `(2,3,18,19,20,22,24,28)` and columns
`(1,2,3,5,6,7,8,9)` have determinant `32768*p^2`.  The complete mixed kernel
is `span{e_a0,W_0}`, with diagonal rows

```text
(0,0,4,0), (0,0,0,0).                             (13)
```

Thus only one `D23` diagonal can survive on either normal.

## The `ell=+/-1`, `lambda=1` kernel plane

Write a nonzero leading direction as

```text
H=X Z+Y V_epsilon.                                (14)
```

The complete normal has thirteen columns: eight subordinate extensions and
the five frozen-leading-vector derivatives in
`p,q,kappa,ell,lambda`.

If `Y!=0`, its mixed rank is seven.  Rows
`(2,3,7,17,20,21,23)` and columns `(0,1,2,3,5,11,12)` have determinant

```text
16384*epsilon*Y^2*p^5.                            (15)
```

Six universal mixed-kernel generators certify the opposite inequality; all
their diagonal images are multiples of `(0,0,0,1)`.

For the remaining direction `[Z]`, the mixed rank is six.  Two fixed minors,
with columns `(0,1,2,3,5,12)`, are

```text
rows (2,3,7,21,23,24): -2048*epsilon*p^4*q,
rows (2,3,7,21,23,26):  2048*p^4*(kappa*q+epsilon). (16)
```

They cover `p!=0`, because `q` and `kappa*q+epsilon` cannot both vanish.
Seven universal mixed-kernel generators again map only to the single row
`D23(1111)`.  Therefore every projective direction in (14) loses the other
three diagonal rows after its mixed coefficients vanish.

## The `ell=+/-1`, `kappa=0,lambda=-1` normal

The `p,q` derivatives along `W_epsilon` vanish and its `ell` derivative is
absorbed by `M`.  The reduced complete normal is

```text
N_e-=[M | partial_kappa(MW_e) | partial_lambda(MW_e)]. (17)
```

Rows `(2,3,7,18,20,22,23,24)` and columns `(1,2,3,4,5,6,8,9)` give the
mixed determinant

```text
32768*epsilon*p^3.                                (18)
```

The complete mixed kernel is `span{e_a0,W_epsilon}`, whose diagonal images
are `(0,0,4,0)` and zero.  Only `D23(0000)` can survive.

A genuine binary `H22` contraction needs both opposite diagonal
coefficients after all mixed coefficients vanish.  Equations (11), (13),
(15)--(18) therefore make every complete first normal above empty.

Finite marking changes act by invertible triangular transformations on the
binary coefficient rows and extension columns.  Their derivative on a
leading zero vanishes, while their derivative on the kernel direction is
absorbed by the subordinate extension variables.  Thus no finite marking
tangent is omitted.

## Replay

```powershell
uv run --with sympy python claims/p5/frontier/verify_p5_component21_finite_h22_extension_ell_zero_unit_endpoint_normal_closure.py
uv run --with sympy python claims/p5/frontier/audit_p5_component21_finite_h22_extension_ell_zero_unit_endpoint_normal_closure.py
```

The primary uses the committed component-21 contraction builder.  The
no-import audit reconstructs the finite bases and all three-row permanents by
direct six-term permutation summation.
