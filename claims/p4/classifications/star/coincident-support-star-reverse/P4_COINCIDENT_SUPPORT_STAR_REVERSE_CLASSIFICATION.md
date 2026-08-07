# Reverse classification of the coincident-support rank-one star

## Status

**Exact characteristic-zero projective placement theorem.**  Fix the
rank-one star orientation with selected edges `01,12,13`, one genuine binary
exact-pair support, and pure-kernel endpoint signature `(1,1,1,0)`.  Every
nonzero all-pair point in this marked orientation lies in the projective
closure of component twenty-one.  This includes all finite values of its
intrinsic parameters, both endpoint divisors of the mode-zero kernel line,
and the vertical projective mode-zero fibre.

This is a reverse classification of one star orientation, not a theorem for
other endpoint signatures, noncoincident support labels, singleton-support
collisions, or special/projective `P_5` fibres.  The global conjecture remains
**UNRESOLVED**.

## General Borel form

In the squarefree Frobenius algebra, put

```text
A=X_0+X_1,       C=X_0-X_1,
B=X_2+X_3,       D=X_2-X_3.                       (1)
```

On the finite mode-zero kernel chart take

```text
y_0=A-alpha C,            x_0=aA+bB+dD,
y_1=ell A+C,              x_1=A,
y_2=C,                    x_2=eA+fB+gD,
y_3=hA+jC+kB+nD,          x_3=A+ell C,             (2)
```

with `alpha!=0`.  Direct expansion leaves only

```text
T_0010=4(alpha+ell)(fk-gn),
T_0110=4(fk-gn),
T_1000=-4(bk-dn),
T_1010/4=afk ell-ag ell n+be k ell+bfh ell-bfj
           -de ell n-dgh ell+dgj,
T_1110/4=afk-agn+bek+bfh-den-dgh,
T_1111=4(bf-dg).                                  (3)
```

Purity with `T_1111!=0` forces

```text
fk-gn=0,              bk-dn=0.                    (4)
```

The rank-three edge `13` excludes `(k,n)=(0,0)`, so there are scalars
`beta,phi` with

```text
(b,d)=beta(n,k),       (f,g)=phi(n,k).             (5)
```

After (5), the three surviving expressions are

```text
T_1111=4 beta phi (n^2-k^2),
T_1110=T_1111 h,
T_1010-ell T_1110=-T_1111 j.                      (6)
```

Therefore nonzero purity gives

```text
beta phi (n^2-k^2)!=0,       h=j=0.               (7)
```

No division by an unchecked quantity occurs: every denominator below is
listed in (7).

## Exact normalization to component twenty-one

The diagonal source transformation

```text
diag(1,1,1/(n+k),1/(n-k))                         (8)
```

sends

```text
nB+kD -> B,            kB+nD -> D.                (9)
```

After harmless row scalings the tuple becomes

```text
U_0=<A-alpha C, aA+beta B>,
U_1=<A,C>,
U_2=<C,eA+phi B>,
U_3=<D,A+ell C>.                                  (10)
```

For `a!=0`, this is exactly the component-twenty-one family

```text
U_0=<A+pB,C+qB>,       U_2=<C,B+kappa A>
```

with

```text
p=beta/a,       q=beta/(alpha a),       kappa=e/phi. (11)
```

For `a=0`, use Pluecker coordinates

```text
(A wedge C, A wedge B, C wedge B).
```

Component twenty-one has mode-zero point `[1,q,-p]`, while (10) has
`[0,1,-alpha]`.  The arc

```text
p=alpha/t,       q=1/t,       t -> 0              (12)
```

has exactly this limit.

## The two missing kernel-line endpoints

The points omitted by `alpha!=0` have the same calculation.

For `y_0=A`, write `x_0=aC+bB+dD`.  Equations (4)--(7) persist.  If
`a!=0`, use `p=0,q=beta/a`; if `a=0`, use the projective arc
`p=0,q=1/t`.

For `y_0=C`, write `x_0=aA+bB+dD`.  If `a!=0`, use
`p=beta/a,q=0`; if `a=0`, use `p=1/t,q=0`.

These four finite/vertical placements exhaust the projective mode-zero
kernel line.  Representative exact pair profiles are

```text
generic:              (3,4,4,3,3,4),
endpoint boundary:    (3,3,4,3,3,4),               (13)
```

so the boundary remains on the all-pair-ranks-at-least-three locus.

## Replay

```text
uv run --with sympy python verify_p4_coincident_support_star_reverse_classification.py
uv run --with sympy python audit_p4_coincident_support_star_reverse_classification.py
```

Both scripts use exact characteristic-zero arithmetic.  The audit rebuilds
the coefficient reduction and all Pluecker arcs without importing the
primary verifier.
