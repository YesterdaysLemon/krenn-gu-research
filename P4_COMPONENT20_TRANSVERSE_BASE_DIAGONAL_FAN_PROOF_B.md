---
role: proof_b
date_utc: 2026-08-01T14:40:40Z
git_commit: f997c8366b461f3952faef0d35b512318341909d
claim_label: VERIFIED
discovery_claim_label: DERIVED
scope: complete diagonal source-torus valuative classification over the transverse component-20 base points (p,q)=(0,1) and (-1,0)
inputs:
  P4_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT.md: dcaae5365f5e2072e798c2ee52dea47c0d5c48f073ed7553ae5f758e9830f0b2
  P4_COMMON_SINGLETON_COMPONENT.md: 9506c62510deebfb19c2cba5fff22940c35946007d9deafb2d12588676c6980d
  P4_TRIPLE_KERNEL_RANK_ONE_TRIANGLE_CLASSIFICATION.md: 81b7346d5f4ce7205dc4c4563e6ecd95a98c59363db3498b1c355ea62489647c
method: polynomial Pluecker and subset-algebra tensor reconstruction, factor-covector kernel normalization, exact min-plus inequalities checked by rational-linear SMT, and direct symbolic limit planes
command: uv run --with sympy --with z3-solver python derive_p4_component20_transverse_base_diagonal_fan_proof_b.py
outputs:
  derive_p4_component20_transverse_base_diagonal_fan_proof_b.py: sha256 emitted by the replay JSON
  P4_COMPONENT20_TRANSVERSE_BASE_DIAGONAL_FAN_PROOF_B.md: sha256 emitted by the replay JSON
limitations: diagonal source tori only; no non-diagonal or arbitrary GL4 arcs, no component-intersection equality, marked H31, weighted H22, component exhaustiveness, arbitrary-order reduction, prize graph, or global Krenn-Gu conclusion
---

# Component-20 transverse-base diagonal fan: proof B

## Result

For each diagonal source arc

```
D(t)=diag(c0*t^x0,c1*t^x1,c2*t^x2,1),  c0*c1*c2 != 0,
```

over either transverse base point, and with at least one nonconstant local
deviation, the limiting `P4` restriction is nonzero if and only if, in the
local coordinates specified below,

```
x1=x2=0  and  x0<=-R,     R=min(P,Q).
```

There are exactly two nonzero faces.  The strict face `x0<-R` lies in the
common-singleton component 18.  The boundary face `x0=-R` lies in component
16 by the fully kernel-kernel triangle classification.  This independently
derived result is now `VERIFIED` by the separate no-import atlas audit; its
discovery label remains `DERIVED`.

If both local deviations vanish identically, then `R=infinity` and the raw
restricted tensor is identically zero for every finite diagonal weight triple;
there is no additional face.

## Raw regular data and exact centre symmetry

At `(p,q)=(0,1)`, set

```
u=p,  v=q-1,  s=u-v=p-q+1,  delta=p+q.
P=val(u)>0,  Q=val(v)>0,  S=val(s)>=R=min(P,Q),
```

where orders may equal `infinity`.

The regular polynomial Pluecker vector for mode zero, in coordinate order
`01,02,03,12,13,23`, is

```
(p(p+1), -q(q-1), -s, delta^2, -delta, delta).
```

The normalized restriction has pure support

```
T0111=2s,   T1111=-2q(q-1),
```

and its factor-covector kernel in mode zero is, projectively,

```
kappa0=(0,-p(p+1),q(q-1),s).
```

These are polynomial objects and remain regular at the centre.  In
particular, no singular choice of a row basis is used.

The exact involution

```
(p,q) -> (-q,-p),       (e,A,B,C) -> (e,B,A,-C)
```

takes the plus centre to `(-1,0)`, fixes the four modes, and exchanges the
source weights `x1` and `x2`.  Thus the minus-centre table below follows by
exchanging `P,Q` and `x1,x2`.

There is also an exact, equivalent chart transport

```
(p,q) -> (-p-1,1-q),    diag(1,1,1,-1) on (e,A,B,C),
                         modes 1 and 2 exchanged.
```

This second model preserves `P,Q` and the diagonal weights.  The replay checks
projective equality of every transformed plane under both transports.  Thus
the coordinate-swap/no-mode-swap description and the diagonal-plus-mode-swap
description are two distinct exact automorphisms of the same family, not
conflicting chart conventions.

## Why the factor kernel is necessary

Let a plane have rows `alpha,beta` and let a tensor factor on it have
covector `(a,b)`.  Its intrinsic factor-kernel row is

```
k=b*alpha-a*beta.
```

If `w` is the valuation of the plane's Pluecker content, saturation of the
plane changes the factor content by exactly `val(k)-w`.  Consequently the
normalization must be computed from the factor kernel and the Pluecker
content together.  Dividing by a whole-plane determinant and then reading a
selected row is not invariant.  For example,

```
P=Q=S=1,  (x0,x1,x2)=(1,0,0)
```

has correct excess `E=1`, so its limiting restriction is zero.  The rejected
selected-row shortcut instead gives a spurious negative exponent.

## Exact min-plus fan

Put

```
M   = max(x1,x2)
z   = min(x0,x1,x2)
k   = min(P+x1,Q+x2,S)
ell = min(x1+x2,x1,x2)
u0  = min(x0+k,ell)
b1  = min(x1,Q+x2,0)
b2  = min(P+x1,x2,0).
```

The saturated restricted tensor has excess

```
E=M+z+k-u0-b1-b2.
```

The order triples that can actually arise obey

```
P<Q  => S=P,
Q<P  => S=Q,
P=Q  => S>=P,
```

where the last case includes exact intrinsic cancellation `S=infinity`.
For every actual order triple,

```
E=0  <=>  x1=x2=0 and x0<=-R.
```

Here is a short exact proof.  Write `n=min(x1,x2)` and
`ci=min(xi,0)`.  If `x0<=n`, then

```
E=(M-b1-b2)+(x0+k-u0).
```

Both summands are nonnegative: `b1<=c1`, `b2<=c2`, and
`M-c1-c2>=0`; equality in the first is possible only when `x1=x2=0`.
Then `k=R`, `ell=0`, and `E=max(x0+R,0)`, giving precisely `x0<=-R`.

If `x0>=n`, use `u0<=ell`,
`x1+x2-ell=max(M,0)`, and
`k>=R+min(n,0)` to obtain

```
E >= R+abs(M) > 0.
```

This proves necessity and sufficiency without a grid.  The replay also asks
Z3 to refute the negation of nonnegativity, necessity, and sufficiency over
the full rational-linear fan, separately for finite `S` and for
`S=infinity`.

The one-sided axes are included exactly.  If `u=0` and `Q=S<infinity`, drop
the infinite terms and use

```
k=min(Q+x2,Q),  b1=min(x1,Q+x2,0),  b2=min(x2,0).
```

If `v=0` and `P=S<infinity`, use

```
k=min(P+x1,P),  b1=min(x1,0),  b2=min(P+x1,x2,0).
```

Separate rational-linear SMT checks prove the same equivalence on each axis.
If `u=v=0`, direct substitution into the polynomial tensor gives zero.

## Residue fan at the plus centre

Let `pi0` be the leading residue of `p` when `P=R` (zero otherwise), and let
`theta0` be the leading residue of `q-1` when `Q=R` (zero otherwise).  The
four mutually exclusive leading cases are

| order cell | leading residues |
|---|---|
| `P<Q` | `(pi0,theta0)=(pi,0)` |
| `Q<P` | `(pi0,theta0)=(0,theta)` |
| `P=Q, S=R` | `pi0=pi`, `theta0=theta`, `pi!=theta` |
| `P=Q, S>R` | `pi0=theta0=pi` |
| `P=infinity` | same leading cell as `Q<P` |
| `Q=infinity` | same leading cell as `P<Q` |

The last row includes both finite higher-order cancellation and
`S=infinity`; they have the same leading planes.

Set

```
v1=c1*A+C,
v2=c2*B+C,
v3=c1*A+c2*B,
W =pi0*c1*A-theta0*c2*B-(pi0-theta0)*C.
```

### Strict face: `x0<-R`

The four limiting planes and nonzero pure support are

```
U0=<e,W>,  U1=<e,v1>,  U2=<e,v2>,  U3=<e,v3>,
T0111=2*c1*c2.
```

This is directly the common-singleton family, hence lies in component 18.
Its pair-rank profiles, ordered `01,02,03,12,13,23`, are

| order cell | pair ranks |
|---|---|
| `P<Q` | `(2,3,3,3,3,3)` |
| `Q<P` | `(3,2,3,3,3,3)` |
| `P=Q, S=R` | `(3,3,3,3,3,3)` |
| `P=Q, S>R` | `(3,3,2,3,3,3)` |

The rank-two specializations do not obstruct this route because the displayed
planes already have the intrinsic common-singleton form.

### Boundary face: `x0=-R`

The mode-zero plane is

```
U0=<-c0*theta0*e+c1*A-C, -c0*pi0*e+c2*B-C>,
```

while `U1,U2,U3` remain as above.  Its polynomial Pluecker vector is

```
(c0*pi0*c1, -c0*theta0*c2, -c0*(pi0-theta0),
 c1*c2, -c1, c2).
```

The nonzero pure support is

```
T0111=-2*c0*theta0*c1*c2,
T1111=-2*c0*pi0*c1*c2.
```

At least one entry is nonzero.  The mode-zero factor kernel is `W`.
The other three factor kernels are all `e`, and the relations on their three
pairs are uniquely `e*e=0`.  On the other hand `e` is not in `U0`: the
minor of the two displayed rows with `e` on columns `e,A,B` is `c1*c2`,
which is nonzero.  All six pair ranks are at least three, so the fully
kernel-kernel triangle theorem routes this face to component 16.

The exact pair-rank profiles are

| order cell | pair ranks |
|---|---|
| `P<Q` | `(3,4,4,3,3,3)` |
| `Q<P` | `(4,3,4,3,3,3)` |
| `P=Q, S=R` | `(4,4,4,3,3,3)` |
| `P=Q, S>R` | `(4,4,3,3,3,3)` |

These profiles are not inferred from numerical residue representatives.  For
each of the 48 face/pair cells the replay checks a fixed nonzero minor and all
larger minors.  In the potentially troublesome `P=Q,S=R` deep `03` cell, the
fixed rank-three witness is

```
rows (0,2,4), columns (1,2,3):  c1^2*(pi-theta)^2,
```

so it stays nonzero even when `pi+theta=0`.  The boundary `03` rank-four
witness is `-2*c0*c1^2*c2^2*(pi-theta)`.  Every witness factor is drawn only
from `c0,c1,c2,pi,theta,pi-theta` as permitted by its residue cell.

## Minus centre and claim boundary

For `(-1,0)`, use local deviations `p+1` and `q`.  Either apply the first exact
involution above (swap `P,Q`, swap `x1,x2`, exchange `A,B`, and send `C` to
`-C`) or the second (preserve the local orders and weights, apply the source
diagonal, and swap modes 1 and 2).  Both give the same zero cone and the same
strict/boundary component routing.

This diagonal classification makes no assertion about arbitrary source
`GL4` arcs, whether the closures of components 16, 18, and 20 intersect only
on these loci, or whether any routed point has marked `H31` or weighted
`H22`.  In particular, it does not resolve the global Krenn-Gu problem.
