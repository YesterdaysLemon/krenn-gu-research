# Component twenty-three `s=0,k=infinity,rt=1` weighted-`H22` obstruction

## Status

**Exact characteristic-zero normalized-divisor theorem.**  On the
simultaneous `s=0,k=infinity` corner of component twenty-three, the complete
homogeneous weighted-`H22` incidence is empty on the all-pair divisor

```text
rt=1,       r*(r-1)*(r+1) != 0.                  (1)
```

This includes every affine marking, every finite weight, and the projective
weight in the fixed normalized `D01/D23` contraction order.  For ordinary
weights, a single shared-binary residual marking exists, but a required beta
diagonal vanishes identically there; it is an exact nongenuine survivor, not
a ternary counterexample.

The result is the `k=infinity` endpoint of the separately closed finite-`k`
face `s=0,rt=1`; it is not obtained by substituting infinity into that affine
theorem.  The parameter endpoints `r=0,infinity`, the lower-pair values
`r=+/-1`, other corner divisors and charts, arbitrary ambient/source changes,
arbitrary order, global gluing, and the global Krenn--Gu conjecture remain
**UNKNOWN** or **UNRESOLVED** as appropriate.  No finite-field calculation is
used.

## Exact corner divisor

Put

```text
A=(1,1,0,0),   C=(1,-1,0,0),
B=(0,0,1,1),   D=(0,0,1,-1).
```

After the legal row rescaling defining `k=infinity`, the corner rows are

```text
alpha=(A,D,B+rD,B+tD),
beta =(B,B,C,C).                                   (2)
```

On `rt=1`, write `t=1/r`.  Direct expansion of all sixteen restricted
permanents gives only

```text
T1111=-4.                                          (3)
```

All six pair images have rank three on (1), so the pair profile is

```text
(3,3,3,3,3,3).                                    (4)
```

For edge `23`, the gcd of the nonzero three-by-three minors is

```text
4*(r-1)*(r+1)/r.                                  (5)
```

Thus `r=+/-1` are exactly the finite lower-pair boundary values, while (1)
is an all-pair locus.  This rank-all-three placement differs from the
generic finite-`k` profile on the adjacent face and requires its own fibre
calculation.

## Weighted shared-extension system

Mark every plane by

```text
marked_i=beta_i+h_i alpha_i.                      (6)
```

This represents every genuine marked basis after rescaling its second row.
Let `x=(x0,...,x3;y0,...,y3)` be the common fifth-coordinate extension.
For the same homogeneous weight, expand the fourteen mixed binary words for
each of `D01` and `D23`, and let `M` be their combined `28 x 8` coefficient
matrix.

The inherited pure word is all-beta.  In diagonal order

```text
(A01,B01,A23,B23),                                (7)
```

genuineness requires both beta diagonals to be nonzero and at least one alpha
diagonal to be nonzero.  Hence rank eight is fatal, as is membership of
either beta diagonal in the mixed row module.

## Ordinary weights

Use the finite chart `[lambda:1]` and first invert

```text
r(r-1)(r+1)(lambda-1)(lambda+1).                 (8)
```

The verifier checks seven exact eight-by-eight minors.  Put

```text
C=256*(lambda-1)^4*(lambda+1)^4*(r-1)^2*(r+1)^2.
```

The first four hold without a marking specialization:

| rows | determinant |
|---|---|
| `(0,1,2,3,8,9,12,16)` | `C*h2*h3/r^2` |
| `(0,1,3,5,8,9,12,16)` | `C*h2*(r-h1)/r^2` |
| `(0,1,3,4,8,9,12,16)` | `-C*h3*(r*h1-1)/r^3` |
| `(0,1,3,7,8,9,12,16)` | `C*h0/r^2` |

The remaining three all use rows `(0,1,3,8,9,12,13,16)`:

| restriction | determinant |
|---|---|
| `h0=h3=0,h1=r` | `-256*(lambda-1)^5*(lambda+1)^3*(r-1)^2*(r+1)^2/r` |
| `h0=h2=0,h1=1/r` | `256*(lambda-1)^5*(lambda+1)^3*(r-1)^2*(r+1)^2/r^3` |
| `h0=h2=h3=0` | `-256*(lambda-1)^5*(lambda+1)^3*(r-1)*(r+1)*(h1*(r^2+1)-2r)/r^2` |

These minors give a complete branch tree.  If `h0!=0`, the fourth minor is
nonzero.  Put `h0=0`.  If `h2*h3!=0`, the first is nonzero.  If only `h2` is
nonzero, the second closes `h1!=r`, and its displayed specialization closes
`h1=r`.  The third minor and its specialization do the same when only `h3`
is nonzero.  Finally, on `h2=h3=0`, full rank fails only on

```text
h0=h2=h3=0,       h1*(r^2+1)=2r.                 (9)
```

On (9), `r^2+1` is automatically a unit: its inverse is `h1/(2r)`.  The
mixed matrix has the exact kernel

```text
z0=(0,0,-1,-1;0,1,0,0).                          (10)
```

The seven-by-seven minor on rows `(0,1,3,8,9,12,16)` and columns
`(0,1,2,3,4,6,7)` is

```text
128*(lambda-1)^4*(lambda+1)^3*(r-1)^2*(r+1)^2
    /(r*(r^2+1)).                                  (11)
```

Thus the residual mixed rank is exactly seven and (10) spans its projective
kernel.  Its four diagonals are

```text
(2*(lambda+1)*(r^2+1)/r, 0, 0, -2*(lambda+1)).   (12)
```

In particular `B01=0`.  The sole binary residual is nongenuine, so every
ordinary weight `lambda!=+/-1` is obstructed before any ternary condition is
needed.

## Exceptional and projective weights

The remaining three weights are checked directly over

```text
Q[r,h0,h1,h2,h3,1/(r(r-1)(r+1))].                (13)
```

Exact standard-basis reduction of the four diagonal rows by the complete
mixed row module gives:

| weight | `(A01,B01,A23,B23) in M` | killing diagonal |
|---|---|---|
| `lambda=1` | `(no,yes,yes,no)` | `B01` |
| `lambda=-1` | `(yes,no,yes,yes)` | `B23` |
| `[1:0]` | `(no,yes,yes,no)` | `B01` |

Every possible mixed-kernel extension at these weights therefore has a
required beta diagonal equal to zero.  Combining this table with the
ordinary analysis closes the complete homogeneous weight line on (1).

## Exact boundary of the claim

The divisor `r=t` in this corner is already represented by the separately
closed `s=1,k=infinity` boundary, so it was not recomputed here.  The present
`rt=1` theorem supplies the nonredundant projective-`k` endpoint missing from
the affine finite-`k` face theorem.  It does not include the four parameter
boundary points excluded in (1), and it makes no arbitrary-order or global
claim.

## Replay

```powershell
uv run --with sympy python verify_p5_h22_common_center_kernel_star_component_s_zero_k_infinity_rt_one_all_pair_obstruction.py
uv run --with sympy python audit_p5_h22_common_center_kernel_star_component_s_zero_k_infinity_rt_one_all_pair_obstruction.py
```

The primary uses the repository contraction builder and checks the pure
tensor, pair placement, seven-minor ordinary branch cover, residual kernel
and diagonals, and three exact row-module certificates.  The audit has no
repository imports: it rebuilds the permanent by subset dynamic programming
and repeats every calculation independently over `Q`.
