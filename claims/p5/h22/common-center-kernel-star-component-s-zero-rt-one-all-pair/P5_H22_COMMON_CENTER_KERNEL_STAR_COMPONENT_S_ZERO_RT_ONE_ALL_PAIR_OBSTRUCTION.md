# Component 23 `s=0, rt=1` all-pair weighted-`H22` obstruction

## Status

**Exact characteristic-zero normalized-face theorem.**  The complete
weighted-`H22` incidence is empty on the normalized affine all-pair part of
component twenty-three's projective parameter face

```text
s=0,       rt=1.
```

This includes every affine marking, every finite weight, the projective
weight, and the rank-drop divisor `k=0` that still has all six pair images of
rank three.  The proof works over exact localized rational polynomial rings;
no finite-field calculation is used.

The values `r=+/-1` leave the all-pair locus, and `r=0` is outside the chart
`t=1/r`.  Other normalized parameter faces, arbitrary ambient/source
degenerations, omitted projective charts, the arbitrary-order local-to-global
reduction, and the global Krenn--Gu conjecture remain **UNRESOLVED**.

## Exact face and its `P_4` placement

In the squarefree four-variable algebra, put

```text
A=X0+X1,   C=X0-X1,   B=X2+X3,   D=X2-X3.
```

On `s=0, rt=1`, with `r!=0`, the component-twenty-three rows are

```text
alpha=(A, A+kD, B+rD, B+D/r),
beta =(B, B,    C,    C).                         (1)
```

Direct expansion of all sixteen restricted permanents gives only

```text
T_1111=-4.                                        (2)
```

Thus the face is pure and nonzero.  In pair order
`01,02,03,12,13,23`, its generic profile is

```text
(3,3,3,4,4,3).                                   (3)
```

The nonzero maximal minors on edges `12` and `13` are respectively

```text
{-8k(r+1), 8k(r-1)},
{-8k(r+1)/r, -8k(r-1)/r}.                        (4)
```

At `k=0`, both rank-four edges drop to rank three and the profile becomes

```text
(3,3,3,3,3,3).                                   (5)
```

This is still an all-pair point, not a lower-pair boundary.  For example,
the unique `01` relation is represented by `(0,-1,1,0)` and has coefficient
matrix rank two, so the point is not silently identified with the
common-singleton generic stratum.  On edge `23`, all four-by-four minors
vanish and the nonzero three-by-three minors are

```text
+/- 4(r-1)(r+1)/r.                               (6)
```

Hence the exact all-pair locus of this chart is

```text
r*(r-1)*(r+1) != 0,       k arbitrary.            (7)
```

At `r=+/-1`, edge `23` has rank two.  Equation (1) is exactly the
`s=0,rt=1` face retained in the complete outward common-center-kernel
`P_4` boundary ledger, so (7) lies in the closure of component twenty-three.
No claim of exclusivity from every other component closure is needed here.

## Shared weighted module

Mark the rows by

```text
beta_i -> beta_i+h_i alpha_i
```

and let `z=(x0,...,x7)` be the shared fifth-coordinate extension.  For the
same weight, form the fourteen mixed rows for `D01` and the fourteen mixed
rows for `D23`.  Number them `0,...,13` and `14,...,27`, respectively, and
write their row module as `M`.

Because (2) is the inherited all-beta support, a genuine lift requires both
beta diagonals `B01,B23` to be nonzero and at least one alpha diagonal to be
nonzero.  Full mixed rank is therefore fatal, as is either membership

```text
B01 in M       or       B23 in M.                 (8)
```

Every denominator cleared below is a power of `r`, hence a unit on (7).

## Finite ordinary weights with `k!=0`

Work after inverting

```text
r(r-1)(r+1) k (lambda-1)(lambda+1).               (9)
```

Set

```text
q_minus=lambda(r+1)-(r-1),
q_plus =lambda(r+1)+(r-1).                        (10)
```

Their difference is `2(r-1)`, a unit in (9), so `q_minus` and `q_plus`
cannot vanish together.  Put

```text
C0=256(lambda-1)^4(lambda+1)^3(r-1)^2(r+1)^2.
```

The verifier checks the following exact paired eight-by-eight minors.  A row
entry ending in `14/15` denotes the two row sets obtained by choosing `14`
or `15`; the displayed values are in that order.

| restriction | rows | exact paired minors |
|---|---|---|
| none | `(0,1,2,3,8,9,12,14/15)` | `C0 h2 h3 k^4 (q_minus/r^2, q_plus/r^3)` |
| none | `(0,1,3,5,8,9,12,14/15)` | `C0 h2 k^3(r-k h1) (q_minus/r^2, q_plus/r^3)` |
| `h2=0` | `(0,1,3,7,8,9,12,14/15)` | `C0 k^4(h0-h1) (q_minus/r^2, q_plus/r^3)` |
| `h2=0, h0=h1` | `(0,1,3,8,9,11,12,14/15)` | `-C0 h1^2 k^4 (q_minus/r^2, q_plus/r^3)` |
| `h3=0, h1=r/k` | `(0,1,3,8,9,11,12,14/15)` | `-C0 k^2 (q_minus, q_plus/r)` |
| `h0=h1=h2=0` | `(0,1,3,8,9,12,13,14/15)` | `512 k^3(lambda-1)^5(lambda+1)^2(r^2-1) (q_minus/r, q_plus/r^2)` |

These minors give a complete branch tree.  If `h2!=0`, the second pair
closes `r-kh1!=0`; on `r-kh1=0`, the first pair closes `h3!=0` and the fifth
pair closes `h3=0`.  If `h2=0`, the third pair closes `h0!=h1`; after
`h0=h1`, the fourth closes `h1!=0` and the last pair closes `h1=0`
independently of `h3`.  Thus `M` has full rank eight at every point of (9).

## The `k=0` all-rank-three divisor

The preceding minors deliberately do not discard `k=0`.  Over

```text
Q[r,h0,h1,h2,h3,lambda,u]
 /
<u r(r-1)(r+1)(lambda-1)(lambda+1)-1>,            (11)
```

exact standard-basis reduction of the 28 mixed rows gives a seven-element
standard basis and

```text
A01,B01,A23,B23 in M.                              (12)
```

In particular `B01=0` on every shared mixed-kernel extension, contradicting
genuineness.  This closes all finite weights with `lambda!=+/-1` on `k=0`.

## Finite endpoints and projective weight

The remaining weights are computed over

```text
Q[r,k,h0,h1,h2,h3,u]
 /
<u r(r-1)(r+1)-1>.                                (13)
```

The exact diagonal-membership table is

| weight | `(A01,B01,A23,B23) in M` | killing diagonal |
|---|---|---|
| `lambda=1` | `(no,yes,no,no)` | `B01` |
| `lambda=-1` | `(yes,no,no,yes)` | `B23` |
| projective weight | `(yes,yes,yes,yes)` | `B01` and `B23` |

These calculations retain `k` as a polynomial variable, so they include
`k=0`; they are not generic-`k` specializations.  Combining them with the
ordinary minor cover and (11) proves emptiness for every finite or
projective weight on (7).

## Scope boundary

The older generic component-twenty-three proof works over a coefficient
field in which `rt-1` is nonzero, so it cannot be specialized to this face.
The theorem above is a new divisor calculation, not a formal consequence of
that generic proof.

This result closes only the normalized affine all-pair face (7).  It does
not cover `r=0`, the lower-pair fibres `r=+/-1`, arbitrary changes of ambient
or source coordinates, parameter directions absent from this normalized
chart, or the global gluing problem.

## Replay

```powershell
uv run --with sympy python claims/p5/h22/common-center-kernel-star-component-s-zero-rt-one-all-pair/verify_p5_h22_common_center_kernel_star_component_s_zero_rt_one_all_pair_obstruction.py
uv run --with sympy python claims/p5/h22/common-center-kernel-star-component-s-zero-rt-one-all-pair/audit_p5_h22_common_center_kernel_star_component_s_zero_rt_one_all_pair_obstruction.py
```

The primary verifier expands all permanents, pair-product ranks, determinant
identities, and localized row modules exactly.  The no-import audit rebuilds
the permanent by subset dynamic programming and clears every row by the
single unit `r`.  Neither replay uses finite fields.
