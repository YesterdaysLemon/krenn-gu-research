# Complete `H31` obstruction on the diagonal-quadric outer boundary

## Status

This is an exact characteristic-zero theorem on the all-rank-two,
nonzero-pure outer boundary of the second `P_4` compression component.

In the diagonal-quadric normal form, the complete marked `H31` fibre is
empty over

```text
Psi=0,   A B F=0.
```

Together with the complete obstruction on the normalized affine slice
`A=B=F=1`, this excludes the entire presently known second
pure-compression component from `H31`, including all of its projective
parameter boundary.

This does **not** prove that the two known pure-`P_4` components exhaust
the compression locus.  It also does not settle `H22` or the global
prize problem.  The honest remainder is now:

```text
possible further all-rank-two pure-P_4 components;
H22.
```

## The projective boundary is a toric curve problem

Recall the normal-form rows

```text
u0=(E,-F,-F,-E),       u1=(A,-B,B,A),
y1=(1,0,0,-1),         x1=(A,C+B,C-B,A),
x2=(H+E,F,F,H-E),      y2=(0,1,-1,0),
k0=(1,0,0,1),          k1=(0,1,1,0),
```

and the planes

```text
U0=span(u0,u1),   U1=span(y1,x1),
U2=span(x2,y2),   U3=span(k0,k1).                  (1)
```

The four active pure coefficients are

```text
T0100=-4F(AF+CH),
T0101=-4(AFH+CE^2),
T1100= 4(ACF+B^2H),
T1101= 4A(AF+CH),                                  (2)
```

and their determinant is `-16 Psi`, where

```text
Psi =
 A^3F^3+A^2CF^2H-AB^2FH^2
 -AC^2E^2F+AC^2FH^2-B^2CE^2H.                    (3)
```

All four planes have rank two exactly when

```text
(A,B)!=(0,0),       (E,F)!=(0,0).                  (4)
```

On `A=0`, equation (3) becomes

```text
-B^2 C E^2 H=0.
```

On `F=0`, it has the same residual monomial.  On `B=0`,

```text
Psi=A F K,

K=A^2F^2+ACFH-C^2E^2+C^2H^2.                      (5)
```

After imposing (4) and requiring that (2) is not the zero matrix, the
outer boundary is therefore the union of seven coordinate surfaces and
the surface `B=0,K=0`.  This is not a large surface calculation.

Two independent projective row scalings act on

```text
(A:B:C),       (E:F:H),
```

and the diagonal source torus

```text
diag(a,b,b,a)
```

acts by

```text
(A,B,C;E,F,H)
  -> (aA,bB,bC; aE,bF,aH).                         (6)
```

Thus every two-dimensional coordinate surface reduces to a
one-parameter curve.  The source permutation

```text
(0,1,2,3) -> (1,0,3,2)
```

together with the mode swap `1<->2` identifies the following pairs:

```text
A=C=0   <->   F=H=0,
A=E=0   <->   F=B=0,
A=H=0   <->   F=C=0.                               (7)
```

The sole missing toric edge in these dense curve gauges is

```text
A=F=H=0,
```

whose partner under (7) is `A=C=F=0`.  Consequently it is enough to
analyze four coordinate curves and one rational conic.

## The four coordinate curves

Use a parameter `p`.  The representative parameter rows are:

| label | `(A,B,C;E,F,H)` | nonzero pure coefficient |
| --- | --- | ---: |
| `AC` | `(0,1,0;p,1,1)` | `4` |
| `AE` | `(0,1,p;0,1,1)` | `4` |
| `AH` | `(0,1,p;1,1,0)`, `p!=0` | `-4p` |
| `edge` | `(0,1,p;1,0,0)`, `p!=0` | `-4p` |

For each curve, choose the kernel rows of the pure tensor as the
`alpha_i`, choose pure complements `beta_i`, and write every marking
as

```text
beta_i(t)=beta_i+t_i alpha_i.                       (8)
```

For a distinguished old source coordinate `q`, let `M_q(t)` be the
`14 x 8` binary mixed-coefficient matrix.  Saturate by both binary
diagonal coefficients and eliminate the eight extension entries.
Exact relative elimination gives:

### The `AC` curve

```text
q=0: (1)
q=1: (t1,t0,t3(t2-1))
q=2: (t1,t0,t3(t2+1))
q=3: (1).                                           (9)
```

The apparent survivors at `p=0` are projection-closure artifacts: the
first binary diagonal vanishes on the entire mixed kernel.  For
`p!=0`, the two components in (9) have mixed rank six.

On the component `t3=0`, use kernel coordinates `u,v`.  For both
`q=1,2`, the binary diagonals are, up to signs,

```text
-2p(u-v),       4v,
```

and a mode-one marked minor is

```text
16 p v (u-v)^2.                                    (10)
```

On `t2=+1` for `q=1`, or `t2=-1` for `q=2`, put `s=t3`.  Away from
`s=0` and `p^2s+1=0`, the diagonals are

```text
 +/- p(su-2v)/(s(p^2s+1)),
 2(2p^2v+u)/(p^2s+1),
```

and a mode-zero marked minor is

```text
 -/+ 2p^2(2p^2v+u)(su-2v)^2/(p^2s+1)^3.           (11)
```

The section `s=0` already belongs to the first component of (9).
On the remaining pivot divisor `p^2s+1=0`, alternate kernel bases give
diagonals

```text
2p(u+/-p^2v),       +/-4u
```

and marked minors

```text
16u(u+/-p^2v)^2.                                   (12)
```

Equations (10)--(12) are nonzero for every genuine binary extension.

### The `AE` curve

For `q=1,2` the relative ideal is `(1)`.  For `q=0,3` it is generated
by `t1,t3` and

```text
t0(pt2-1),
t0t2^2-t0p^2-t2p^2+t2,
t2p^3-t2p-p^2+1,
t0p^3-t0t2+p^2-1.                                  (13)
```

If `p^2!=1`, (13) has exactly the rational marking

```text
t2=1/p,       t0=-p/(p^2+1),                       (14)
```

provided `p(p^2+1)!=0`; otherwise it has no point.  At `p=epsilon`,
`epsilon=+/-1`, the complete fibre is

```text
t0=0       or       t2=epsilon.                    (15)
```

At (14), put

```text
L=p^2u+2pv-u.
```

The binary diagonals are

```text
 +/-2(p^2+1)u,       2L/p,
```

and a mode-zero marked minor is

```text
 +/-16(p^2+1)u^2L.                                 (16)
```

On the first branch of (15), with `s=t2`, the diagonals are

```text
 +/-2(u-v),
 2epsilon[(s+epsilon)u-(s-epsilon)v],
```

and a mode-zero marked minor is

```text
 +/-8(u-v)^2[(s+epsilon)u-(s-epsilon)v].           (17)
```

On the second branch of (15), with `s=t0` and
`2s+epsilon!=0`, the diagonals are

```text
 +/-2(u-v)/(2s+epsilon),       4u,
```

and a mode-zero marked minor is

```text
 +/-16u(u-v)^2/(2s+epsilon)^2.                     (18)
```

The omitted point `2s+epsilon=0` is exactly the marking (14), already
closed by (16).  Thus (16)--(18) exclude the full projection (13).

### The `AH` curve

For all four distinguished coordinates, the exact saturated relative
projection ideal is

```text
(1).                                                (19)
```

There is no genuine binary extension in any marking.

### The extra toric edge

For `A=F=H=0`, with parameter `p=C/B!=0`,

```text
q=0,3: (t2,t0,t1t3),
q=1,2: (1).                                         (20)
```

On `t3=0`, put `s=t1`.  When `s!=0`, a marked minor is, up to sign,

```text
32 p s^2 v^2(u-v),                                 (21)
```

while the binary diagonals are `2(u-v)` and `+/-4pv`.
On `t1=0`, put `s=t3!=0`; the diagonals are, up to signs,

```text
2(su-/+v)/s,       4pu,
```

and a marked minor is

```text
16u(su-/+v)^2.                                     (22)
```

At the intersection `t1=t3=0`, a mode-zero minor is

```text
 +/-16pv(u-v)(u+v).                                (23)
```

Only the genuine direction `u+v=0` is not covered by (23).  Normalize
it to `(u,v)=(-1,1)`.  Stack the pure-hyperplane and neighbouring
one-marked maps as maps from the full five-dimensional third row.
For both `q=0,3`, the rows

```text
3,4,7,8,12
```

form a `5 x 5` minor

```text
128p.                                               (24)
```

Since `p!=0`, the stacked map is injective.  The corresponding third
target row is globally zero, contradicting target rank three.  This
closes the sole non-transverse edge direction.

## The `B=0` conic

On `B=0,F!=0`, normalize `A=C=F=1`.  Equation (5) becomes

```text
E^2=H^2+H+1.                                       (25)
```

It is the rational conic parametrized homogeneously by

```text
H=u(u-2v),
E=-(v^2-uv+u^2),
F=v^2-u^2.                                         (26)
```

On the affine chart `u=1`, write `p=v` and invert
`F=p^2-1`; the two points `F=0` already lie on the closed `FB` curve
in (7).  Exact relative projection gives

```text
q=0,3: (1),

q=1:
  (2p-1, 3t3+4, t1-1, 9t0+16t2, 4t2^2+3t2),

q=2:
  (2p-1, 3t3+4, t1-1, 9t0-16t2, 4t2^2-3t2).       (27)
```

Thus the finite chart has only four survivor markings, all over
`p=1/2`.  At each marking the mixed rank is six.  In suitable kernel
coordinates, the diagonal pairs and selected marked minors are:

```text
(4u+3v,4u-3v):
  const (4u-3v)(4u+3v)^2;

(2u+3v,u):
  2u(2u+3v)^2.                                     (28)
```

The point at infinity in (26) is `(E,F,H)=(-1,1,0)`.  Its exact
projection is

```text
q=0,3: (1),
q=1: (t3-1,t1+1,t0+t2,t2^2-t2),
q=2: (t3-1,t1+1,t0-t2,t2^2+t2).                   (29)
```

The four survivor markings in (29) have diagonal pairs

```text
(u-v,u+v),       (u-2v,u),
```

and marked minors

```text
8(u-v)(u+v)^2,       8u(u-2v)^2.                   (30)
```

Equations (28) and (30) exclude every genuine conic extension.

## Ternary conclusion

Every marked minor above belongs to a neighbouring one-marked map.
For its selected mode, the pure-hyperplane one-marked map has a
nonzero entry in the distinguished source column.  Hence an injective
neighbouring map forces that mode's third target row to be supported
only on the distinguished coordinate, while the pure map kills that
remaining coordinate.  The row is globally zero, contradicting rank
three.

The only direction without an injective neighbouring map is handled
by the stacked injectivity certificate (24), which gives the same
contradiction directly.

The four coordinate curves, their exact partners (7), the extra edge
and its partner, the affine conic, its point at infinity, and its two
`F=0` endpoints exhaust every all-rank-two point of

```text
Psi=0,   A B F=0
```

with nonzero pure restriction.  Therefore the complete marked `H31`
fibre on the outer boundary is empty.

## Verification

Run:

```text
python verify_p5_h31_diagonal_quadric_outer_boundary.py
python audit_p5_h31_diagonal_quadric_outer_boundary.py
```

The primary verifier expands the boundary decomposition, checks the
torus and source/mode symmetries, recomputes all relative saturated
projection ideals over characteristic zero, verifies every displayed
kernel, binary diagonal, one-marked minor, and the stacked determinant
`128p`.

The independent audit imports no primary code.  Over `F_5` and `F_7`
it uses a separate dynamic-programming permanent and modular row
reduction, enumerates only the four one-parameter marking bundles and
the projective conic, compares every actual binary survivor with the
displayed projection strata, and tests every projective kernel
direction by neighbouring or stacked marked-map rank.  This is
finite-field QA of the exact characteristic-zero certificates, not a
replacement for them and not an ambient brute-force construction.
