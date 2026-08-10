# Component twenty-three `s=0,k=infinity` projective `r/t` boundary obstruction

## Status

**Exact characteristic-zero normalized-boundary theorem.**  Compactify the
two parameters of component twenty-three's `s=0,k=infinity` corner as
`P^1_r x P^1_t`.  Both coordinate boundary curves

```text
r=infinity, t finite,       t=infinity, r finite
```

and their common point `(r,t)=(infinity,infinity)` have empty complete
affine-marked `H31` fibre and empty complete homogeneous weighted-`H22`
fibre in the fixed normalized contraction order.  The calculation includes
every marking, all four source-coordinate insertions, every finite weight,
and projective weight.  Everything is over `Q`; no finite-field calculation
is used.

This does not cover arbitrary ambient/source bases, arbitrary contraction
order, another projective component chart, the local-to-global reduction,
or the global Krenn--Gu conjecture.  Those scopes remain **UNKNOWN** or
**UNRESOLVED** as appropriate.

## Exact compactification

Put

```text
A=X0+X1,   C=X0-X1,   B=X2+X3,   D=X2-X3.
```

The finite corner is

```text
alpha=(A,D,B+rD,B+tD),
beta =(B,B,C,C).                                    (1)
```

Homogenize the third and fourth alpha rows separately.  On the two boundary
charts, legal row rescaling gives

```text
R_infinity(t): alpha=(A,D,D,B+tD), beta=(B,B,C,C),
T_infinity(r): alpha=(A,D,B+rD,D), beta=(B,B,C,C).  (2)
```

Their common `P^1 x P^1` point is

```text
I_infinity: alpha=(A,D,D,D), beta=(B,B,C,C).        (3)
```

The tensor-mode transposition `(2 3)` exchanges the two curves and fixes
(3).  Both verifiers nevertheless reconstruct the two boundary curves
independently.

All sixteen pure coefficients vanish except `T1111=-4`.  In edge order
`01,02,03,12,13,23`, the generic profiles and their parameter-zero drops
are

```text
R_infinity: (3,2,3,3,3,4) -> (3,2,3,3,3,3),
T_infinity: (3,3,2,3,3,4) -> (3,3,2,3,3,3),
I_infinity: (3,2,2,3,3,3).                         (4)
```

Every local plane has rank two.  Once `alpha_i` is fixed as its first row,
every genuine marked basis is therefore represented by

```text
marked_i=beta_i+h_i alpha_i.                       (5)
```

The omitted projective marking is proportional to `alpha_i` and is not a
basis.

## Complete marked `H31` fibre on a boundary curve

Let `q` denote the remaining finite parameter (`q=t` on `R_infinity` and
`q=r` on `T_infinity`).  For insertion `d`, normalize the alpha binary
diagonal and invert the beta diagonal.  Exact elimination gives the unit
ideal for `d=2,3`.  For `d=0,1`, the complete projected marking ideal on
`R_infinity` is

```text
<h1-q, h0, q h3, h2 h3, (q^2-1)h2>.               (6)
```

On `T_infinity`, exchange `h2` and `h3`.  Thus the exact branch list is

```text
C:    h=(0,q,0,0),
Z_R:  q=0, h=(0,0,0,p),
S_R:  q=+/-1, h=(0,q,p,0),                         (7)
```

and the mode-swapped list `Z_T,S_T`.  In (7), `C` covers the zero marking
at all intersections; `p` is nonzero on the punctured parts of `S_R,S_T`.

Every branch has mixed rank six and nullity two.  With kernel parameters
`c0,c1`, the selected mode-zero pure-plus-neighbour determinant is a unit
multiple of a genuine diagonal product.  The exact representatives for
`d=0` are

```text
C_R:  A=2c0, B=-4c1, det[01279]= 32 c0^2 c1,
C_T:  A=2c0, B=-4c1, det[01279]=-32 q c0^2 c1,

Z_R:  A=2c0, B=-2(c0p+2c1), det[01279]= 16 c0^2(c0p+2c1),
Z_T:  A=2c0, B=-2(c0p+2c1), det[0127,10]=-16 c0^2(c0p+2c1),

S_R:  A=2q(c0-c1)/p, B=-2(c0+c1),
      det[01279]=16(c0-c1)^2(c0+c1)/p^2,
S_T:  A=-2q(c0-c1)/p, B=-2(c0+c1),
      det[01279]=-16q(c0-c1)^2(c0+c1)/p^2.         (8)
```

For `d=1`, the beta diagonal and every displayed determinant reverse sign.
The factor `q` in `C_T` is harmless on `q!=0`; its `q=0` point is already
covered by `Z_T`, whose determinant has no extra factor.  Equations (8)
force one required third target row to vanish throughout every genuine
binary branch.  Hence both complete boundary-curve marked-`H31` fibres are
empty.

## The double endpoint in marked `H31`

At (3), insertion `d=2,3` again has unit projected ideal.  For `d=0,1`,
the exact projection is

```text
<h0,h1 h2,h1 h3,h2 h3>,                            (9)
```

the union of the three marking axes.  On the `h1` axis, including their
common origin, the mode-zero determinants for `d=0,1` are

```text
+/-64 c0 c1^2,
```

with diagonals `A=-2c0`, `B=+/-4c1`.  On the punctured `h2` and `h3`
axes the determinants are, respectively,

```text
-/+16(c0-c1)(c0+c1)^2/p,
+/-16(c0-c1)(c0+c1)^2/p,                           (10)
```

with `A=+/-2(c0-c1)/p` and `B=+/-2(c0+c1)`.  They
are nonzero on the genuine diagonal open, so the double endpoint also has
empty marked-`H31` fibre.

## Complete homogeneous weighted `H22` fibre

For the shared `D01/D23` extension, genuineness requires both beta
diagonals nonzero and at least one alpha diagonal nonzero.  On either
boundary curve, exact elimination in both alpha-normalization charts and in
both homogeneous weight charts gives only one nonunit alpha chart.  On
`R_infinity` its projected ideal is

```text
<h1-q,h0,q h3,h2 h3,q(q-1)(q+1),(q^2-1)h2>.       (11)
```

On `T_infinity`, exchange `h2,h3`.  Thus binary incidence is empty for
`q` outside `0,+1,-1`; at those three values it lies exactly on the
exceptional lines `Z_R,S_R` and their mode swaps.  At the double endpoint,
both alpha-normalization charts give the unit ideal for finite and
projective weight, so even shared binary incidence is empty.

On every exceptional boundary line the combined mixed matrix has rank
seven and a unique extension line.  Normalize it as

```text
Z_R: z=(0,0,0,-1;0,1,0,0),
Z_T: z=(0,0,-1,0;0,1,0,0),

S_R: z=(0,0,0,-q;0,q,p,0),
S_T: z=(0,0,-q,0;0,q,0,p).                        (12)
```

In every case `A23=0`.  At finite weight the remaining three genuine
diagonals are unit multiples of

```text
A01=lambda+1,   B01=p(lambda-1),   B23=lambda+1.   (13)
```

Thus genuine incidence requires `p(lambda-1)(lambda+1)!=0`.  At projective
weight it requires `p!=0`.

None of these binary incidences extends to a ternary local map.  In the
sixteen one-missing-row equations for mode zero, the following determinants
are exact:

```text
Z_R rows 0127,10: -8 p(lambda-1)^4(lambda+1),
Z_T rows 01279:   +8 p(lambda-1)^4(lambda+1),
S_R rows 0127,10: -8 q p(lambda-1)^4(lambda+1),
S_T rows 01279:   +8 q p(lambda-1)^4(lambda+1).    (14)
```

At projective weight, remove the factors in `lambda`; the determinants are
`-8p,+8p,-8qp,+8qp`.  They are nonzero everywhere genuine, forcing the
missing mode-zero row to vanish and contradicting ternary rank three.
Together with the empty generic and double-endpoint binary fibres, this
proves complete homogeneous weighted-`H22` emptiness on the entire
projective `r/t` boundary.

## Replay

```powershell
uv run --with sympy python claims/p5/boundaries/verify_p5_component23_s_zero_k_infinity_projective_r_t_boundary_obstruction.py
uv run --with sympy python claims/p5/boundaries/audit_p5_component23_s_zero_k_infinity_projective_r_t_boundary_obstruction.py
```

The primary reconstructs both boundary limits, the double endpoint, all
profiles, complete marked-`H31` and weighted-`H22` projections, exact
kernels, rank certificates, and ternary-compatibility determinants.  The
audit imports no project code and independently rebuilds every permanent,
contraction, elimination, stack, and determinant.  Neither replay uses a
finite field.
