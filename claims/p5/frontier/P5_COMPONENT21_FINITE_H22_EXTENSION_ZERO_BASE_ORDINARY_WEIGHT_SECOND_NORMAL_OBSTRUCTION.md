# Component 21: ordinary-weight zero-base second-normal obstruction

## Status

**Exact characteristic-zero theorem in the displayed raw finite chart.**  Fix

```text
p=q=0,  lambda finite,  lambda!=+/-1.                 (1)
```

The component-21 stacked finite `D01/D23` extension map has the kernel line

```text
K_lambda=(0,0,0,1-lambda,0,0,lambda+1,0).            (2)
```

This note treats precisely the ordinary-weight directions (2) for which the
complete first normal from the preceding raw-kernel theorem can itself be
zero.  It includes subordinate extensions, the first and second appearances
of `p,q`, and all finite `kappa,ell,lambda` and extension-scale tangents.

Every complete second normal is empty for genuine weighted `H22`.  Moreover,
the second normal is zero only when its later `p,q` terms vanish and its
subordinate extension is another multiple of (2).  Thus the sole surviving
second-zero directions remain tangent to the exact zero family; no new
projective direction or valuation pattern appears at this level.

This is not a theorem at `lambda=+/-1`, at parameter or weight infinity, for
arbitrary source or ambient degenerations, or for every iterated higher
normal.  A zero second normal may continue to higher order, which remains
**UNKNOWN** here.  The arbitrary-order local-to-global reduction remains
**UNKNOWN**, and the global Krenn--Gu conjecture remains **UNRESOLVED**.  No
finite-field or numerical inference is used.

## Exact zero family and complete first kernel

Let

```text
M(p,q,kappa,ell,lambda)                              (3)
```

be the `32 x 8` stacked finite extension coefficient matrix, with the first
sixteen rows belonging to `D01` and the last sixteen to `D23`.  Direct
symbolic expansion gives the identity

```text
M(0,0,kappa,ell,lambda) K_lambda = 0                (4)
```

for arbitrary finite `kappa,ell,lambda`.  Consequently varying `kappa` or
`ell`, varying `lambda` together with (2), and rescaling (2) all lie in an
explicit exact zero family.

Freeze (2) and form the complete first normal

```text
N = [M_0 | M_p K_lambda | M_q K_lambda
         | M_kappa K_lambda | M_ell K_lambda
         | M_lambda K_lambda],                     (5)
```

where `M_0=M(0,0,kappa,ell,lambda)`.  Its columns are ordered as eight
subordinate extension coefficients followed by
`dp,dq,dkappa,dell,dlambda`.

For every ordinary weight, `N` has rank exactly nine.  Four independent
kernel vectors are

```text
(K_lambda,0,0,0,0,0),
e_dkappa,
e_dell,
-2 e_z_a3 + (lambda+1)e_dlambda.                   (6)
```

Four families of exact rank-nine minors cover all finite `kappa,ell`:

```text
512 ell (lambda-1)^5 (lambda+1)^6 (ell^2-1),
512 (lambda-1)^5 (lambda+1)^4 (ell^2-1)
    (lambda ell+lambda+ell-1)^2,
512 ell kappa (lambda-1)^6 (lambda+1)^5,
-512 (lambda-1)^6 (lambda+1)^5,                   (7)
```

where the fourth is used at `kappa=0,ell=1`.  At
`kappa=0,ell=-1` a fifth fixed minor is

```text
2048 (lambda-1)^6 (lambda+1)^3.                   (8)
```

The first minor covers `ell` outside `0,+/-1`; the second covers `ell=0`;
the third covers `ell=+/-1,kappa!=0`; and (7)--(8) cover the two remaining
points.  Equations (6)--(8) therefore give the complete kernel, not merely
four known directions.

In particular, a zero complete first normal necessarily has

```text
dp=dq=0,                                           (9)
```

and its subordinate extension and `dlambda` term are exactly a tangent to
the scale-and-weight motion of `K_lambda`; `dkappa,dell` are free because
(4) is independent of them.

## Straightening and the complete second normal

Let an arc have zero first normal.  Using (6), choose series
`a(t),kappa(t),ell(t),lambda(t)`, with `a(0)=1`, that have the same first jet
as the arc.  The
extension and base coordinates can then be written through the next order
as

```text
z(t)=a(t)K_{lambda(t)}+t^2 w+O(t^3),
p(t)=t^2 P+O(t^3),
q(t)=t^2 Q+O(t^3).                                (10)
```

Because (4) is an exact identity, all first-tangent and cross terms internal
to that zero family cancel.  The coefficient at order `t^2` is exactly

```text
S (w,P,Q),
S=[M_0 | M_p K_lambda | M_q K_lambda].             (11)
```

Thus (11) includes subordinate extensions, later `p,q` terms, and arbitrary
parameter, weight, and scale tangents rather than freezing them silently.

The apparently omitted first-normal columns satisfy the exact identities

```text
M_kappa K_lambda=0,
M_ell K_lambda=0,
(lambda+1)M_lambda K_lambda=2 M_0 e_z_a3.          (12)
```

Hence `N` and `S` have the same column image at ordinary weight.  It follows
from (7)--(8) that

```text
rank(S)=9,
ker(S)=span{(K_lambda,0,0)}.                       (13)
```

So a zero second normal forces `P=Q=0` and `w` to be a scale multiple of the
old kernel direction.  These are exactly the second-order directions that
can be absorbed back into the explicit zero family.

## Weighted-H22 obstruction and boundary

Both `D01` diagonal rows of `S` are identically zero before imposing any
mixed equations.  Therefore no nonzero vector in the second-normal image
can have the pure `D01` diagonal required by a genuine shared weighted-H22
contraction.  Every nonzero complete second normal is H22-empty, while (13)
classifies all zero ones.

This closes the second normal only in the ordinary finite-weight raw
zero-base stratum.  It does not replace the separate `lambda=+/-1` first
normal analysis, the projectivized `(p,q)` blow-up theorem, or the parameter
compactification.  It also does not assert that the formal straightening has
already been iterated to arbitrary order.  Higher zero normals and global
gluing retain the status stated above.

## Replay

```powershell
uv run --with sympy python claims/p5/frontier/verify_p5_component21_finite_h22_extension_zero_base_ordinary_weight_second_normal_obstruction.py
uv run --with sympy python claims/p5/frontier/audit_p5_component21_finite_h22_extension_zero_base_ordinary_weight_second_normal_obstruction.py
```

The primary verifier uses the committed component-21 contraction builder.
The audit has no repository imports and reconstructs every three-row
permanent by direct six-term permutation summation.
