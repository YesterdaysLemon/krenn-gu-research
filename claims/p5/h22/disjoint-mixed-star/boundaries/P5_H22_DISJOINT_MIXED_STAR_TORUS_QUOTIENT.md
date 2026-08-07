# Source-torus quotient of the disjoint mixed-star component

## Status

This is an exact source-torus quotient lemma for the eighth pure-`P_4`
component and its two weighted `H22` incidences.

On the dense chart `f!=0`, the parameter `f` is pure gauge.  A diagonal
source transformation and invertible row-basis changes identify

```text
(a,b,f,phi)  ~  (af,bf,1,phi/f),                  (1)
```

without changing the weighted slope `r`.  Thus generic component and
boundary calculations may be performed on the slice `f=1`.

This lemma does not close the two remaining certificate-divisor
frontiers, prove component exhaustiveness, finish `P_5 -> Delta_3`, or
resolve the global Krenn--Gu conjecture.

## Exact plane identities

Let

```text
D=diag(f,f,1,1)                                    (2)
```

act on the four source coordinates.  Write `Y_i(a,b,f,phi)` for the
`2 x 4` plane matrices of the component family and put

```text
A=af,       B=bf,       P=phi/f.                   (3)
```

Direct symbolic multiplication gives

```text
Y_0(a,b,f,phi)D =             Y_0(A,B,1,P),
Y_1(a,b,f,phi)D = f I_2       Y_1(A,B,1,P),
Y_2(a,b,f,phi)D = f I_2       Y_2(A,B,1,P),
Y_3(a,b,f,phi)D = diag(f,1)   Y_3(A,B,1,P).        (4)
```

Every left factor in (4) is invertible when `f!=0`, so the four row
planes define the same points of `Gr(2,4)`.

The component equation is exactly invariant:

```text
Phi(a,b,f,phi)=Phi(af,bf,1,phi/f).                 (5)
```

In normalized variables it becomes the two-dimensional surface

```text
A^2 B P^2+A^2-B^2+B^2 P^2-B-1=0.                 (6)
```

The original three-dimensional family is therefore a one-dimensional
source-torus orbit over this surface on the dense chart.

## Compatibility with the weighted contractions

For a source row `u=(u_0,u_1,u_2,u_3)` and extension entry `e`, direct
calculation gives

```text
D_01^r(uD,e)
 =D_01^r(u,e) diag(f,1,1,1),

D_23^r(uD,e)
 =D_23^r(u,e) diag(f,f,1,1).                      (7)
```

The output changes in (7) are invertible and the same slope `r`
appears on both sides.  They preserve mixed-kernel dimensions,
nonvanishing of the two diagonal coefficients, and ranks of every
one-marked map.

The only marking-coordinate change not common to both basis rows is
in mode three:

```text
t_3 -> f t_3,                                      (8)
```

which is an automorphism of the affine marking line on `f!=0`.

Consequently the complete binary and ternary Fitting incidences on the
left of (1) are isomorphic to those on the normalized slice.

## Why this translation helps

The component initially appears as a hypersurface in four parameters.
Quotienting by the diagonal source torus turns it into the surface (6).
Coefficient and slope divisors then become curves or double covers of
this surface rather than three-dimensional hypersurfaces.

For example, the difficult remaining linear slope graph reduces at
`f=1` to

```text
(a^2+2ab+2a-1)r+(-a^2+2ab+2a+1)=0,               (9)
```

or, away from the already-closed charts `a=0,r=-1`,

```text
b=-1-(r-1)(a^2-1)/(2a(r+1)).                      (10)
```

This reduces its base to a quadratic cover over `C(a,r)`.  Current
standard-basis calculations on that cover still time out, so (9) is
not claimed closed.

## Honest frontier

The quotient identities (4)--(8) are exact.  They do not turn the
failed calculations on the remaining divisors into proofs.

The `f=0` boundary is outside this torus chart and was already closed
branchwise in the parameter-pivot theorem.  On `f!=0`, the remaining
visible candidate divisors from the first reduced `D_01` certificate
are one linear graph (9) and one quadratic-in-`r` graph.  Exact finite-
field diagnostics find fixed rank-four minors on both, but several
equivalent characteristic-zero presentations reached their time
limits.  Those timeouts are null results.

Other certificate factors may still appear, and other pure components
may exist.  The global prize conjecture remains unresolved.

## Verification

Run:

```text
python \
  claims/p5/h22/disjoint-mixed-star/boundaries/verify_p5_h22_disjoint_mixed_star_torus_quotient.py

python \
  claims/p5/h22/disjoint-mixed-star/boundaries/audit_p5_h22_disjoint_mixed_star_torus_quotient.py
```

The primary verifier reconstructs the four symbolic family matrices,
checks (4)--(5), and checks both contraction identities (7) over
characteristic zero.

The independent audit imports nothing from the primary verifier.  It
replays all four plane identities and 32 contraction identities at
component points over `F_11` and `F_13`.  This modular check is
corroboration only; the symbolic identities are the proof.
