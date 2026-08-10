# Generic `H31` obstruction from an elliptic surface

## Status

This is an exact characteristic-zero theorem on a dense open subset of
the second, diagonal-quadric pure-compression component.

After normalizing `A=B=F=1`, the component is birational to an elliptic
surface over the `r`-line.  Over its function field, for every marking
of the four planes and every distinguished source coordinate, there is
no genuine binary `Delta_2` extension at all.  Consequently the marked
`H31` fibre is empty at the generic point of this component.

This is stronger than a marked-minor obstruction at the generic point,
but deliberately weaker than a theorem on the complete component.  It
proves that any remaining binary-extension locus is a proper closed
subset.  It does not classify every such curve, compactify the
normalization boundary, classify further pure-compression components,
settle `H22`, or solve the prize problem.

## A conic bundle hidden in the `(3,3)` equation

On the dense normalization chart

```text
A=B=F=1,
```

the component equation is

```text
Psi =
  1+CH-H^2-C^2 E^2+C^2 H^2-CE^2 H.                (1)
```

Put

```text
U=C+H,       S=1+CH,       T=H+CE^2.               (2)
```

Then the six-term equation collapses to

```text
Psi=S^2-UT.                                         (3)
```

Thus the parameter surface is the rank-one locus of the symmetric
matrix

```text
[ U S ]
[ S T ].
```

On `U!=0`, write

```text
r=S/U.
```

Solving for `C`, then introducing

```text
x=1-rH,       Y=rEx,                                (4)
```

gives

```text
H=(1-x)/r,
C=rx/(x+r^2-1),
E=Y/(rx).                                           (5)
```

The component equation becomes

```text
Y^2 =
x[(1-r^2)x^2+(3r^2-2)x+(r^2-1)^2].                 (6)
```

Indeed, if the right side of (6) is denoted by `f(r,x)`, direct
substitution in (1) gives

```text
Psi =
 ((x-1)^2-r^2)
 ----------------------- (Y^2-f(r,x)).             (7)
 r^2 x (x+r^2-1)^2
```

The factor `f(r,x)` has odd `x`-adic valuation over `Q(r)`, so it is
not a square in `Q(r,x)`.  Equation (6) therefore defines a quadratic
function-field extension rather than two artificial rational sheets.

The cubic in `x` has discriminant

```text
r^4(r-1)^4(r+1)^4(4r^2-3).                          (8)
```

Hence its finite singular fibres can occur only at

```text
r=0, +/-1, +/-sqrt(3)/2.                            (9)
```

The smooth projective completion has the rational two-torsion section

```text
(x,Y)=(0,0)
```

and the pair of sections

```text
P=(1,r^2),       -P=(1,-r^2).                       (10)
```

Under (5), the sections in (10) are precisely

```text
H=0, C=1/r, E=+/-r,                                (11)
```

so they are the two rulings already closed by the complete `H=0`
marked-fibre theorem.

## The minimal surface is an extremal-rank elliptic K3

The elliptic reframe is not just a convenient parameter substitution.
Set

```text
a=1-r^2,       X=ax,       W=aY.
```

Then (6) becomes the Weierstrass equation

```text
W^2=X^3+(3r^2-2)X^2+(1-r^2)^3 X.                  (12)
```

Its standard invariants factor as

```text
Delta =
16 r^4(r-1)^6(r+1)^6(4r^2-3),

c4=16(3r^6-3r^2+1).                               (13)
```

At the finite points, Tate's characteristic-zero criteria give fibres

```text
r=0:                      I4,
r=+1,-1:                  I6,I6,
r=+sqrt(3)/2,-sqrt(3)/2: I1,I1.                   (14)
```

At infinity put `s=1/r`, `X'=s^4X`, and `W'=s^6W`.  The local equation
is

```text
W'^2 =
X'^3+(3s^2-2s^4)X'^2+s^2(s^2-1)^3X'.             (15)
```

There `ord_s(Delta)=6` and `ord_s(c4)=2`, so the fibre is `I0*`.
The fibre Euler numbers total

```text
4+6+6+1+1+6=24.
```

Equivalently the fundamental line bundle has degree two.  The smooth
minimal resolution of (12) is therefore an elliptic K3 surface.

The reducible fibres contribute the root lattice

```text
A3 + A5 + A5 + D4,
```

of rank `17`.  The section `P` in (10) is non-torsion.  One exact
specialization proves this: at the good fibre `r=2`, equation (12) is

```text
W^2=X^3+10X^2-27X,
```

and

```text
P=(-3,-12),        2P=(9/4,-9/8).                  (16)
```

The specialized discriminant is nonzero modulo `5` and `7`.  Direct
group-law calculation gives reduction orders

```text
ord(P mod 5)=10,       ord(P mod 7)=3.
```

If `P` had finite order, the second equality would give it nontrivial
`3`-primary torsion.  Good reduction at `5` is injective on prime-to-5
torsion, forcing `3` to divide `ord(P mod 5)`, contrary to the first
equality.  Hence `P` is non-torsion over `Q(r)`.

The same specialization determines the torsion subgroup.  Direct
point counts give

```text
#E(F5)=10,       #E(F7)=12,       #E(F11)=14.
```

Good-reduction injectivity prime by prime leaves rational torsion of
order at most two.  The visible section `(X,W)=(0,0)` has order two,
so the generic torsion subgroup is exactly `Z/2`.

Shioda--Tate now gives

```text
rho = 2+17+rank MW.
```

A complex K3 surface has `rho<=20`, while `P` gives `rank MW>=1`.
Consequently

```text
rho=20,       MW = Z + Z/2.                        (17)
```

Thus every section of the elliptic fibration lies in a rank-one
Mordell--Weil group up to torsion.  Remaining survivor curves could
still be multisections, but section discovery is now an arithmetic
lattice problem rather than an unrestricted construction problem.

The other previously closed slice also has a natural place in this
picture.  Where `U!=0`,

```text
r-1=(C-1)(H-1)/U,
r+1=(C+1)(H+1)/U.                                  (18)
```

Thus the factorized `H=1` slice is carried into the singular fibre
`r=1`; the `H=-1` image lies over `r=-1`.  The indeterminacy `U=0` on
`Psi=0` forces

```text
(C,H)=(-1,1) or (1,-1),                             (19)
```

which is exactly the pure-factor-direction boundary and its symmetry
image.  This explains geometrically why the previously proved
one-dimensional slices cluster around two sections, two singular
fibres, and the birational base locus.

## Generic marked planes

Retain the fixed rows

```text
y1=(1,0,0,-1),       y2=(0,1,-1,0),
k0=(1,0,0, 1),       k1=(0,1, 1,0).
```

In the elliptic coordinates (5), put

```text
u0=(E,-1,-1,-E),       u1=(1,-1,1,1),
x1=(1,C+1,C-1,1),      x2=(H+E,1,1,H-E).
```

On the nonzero-pure chart use kernel and pure rows

```text
alpha0=u0+r u1,       beta0=u1,
alpha1=y1,            beta1=x1,
alpha2=y2,            beta2=x2,
alpha3=r k0-k1,       beta3=k1.                    (20)
```

Modulo (6), every restricted coefficient except the all-`beta`
coefficient vanishes.  The latter is

```text
4S =
-4(x-1-r)(x-1+r)/(x+r^2-1),                        (21)
```

which is nonzero at the generic point.  Every marking is

```text
beta_i(t)=beta_i+t_i alpha_i.                       (22)
```

## Function-field binary projection

Fix a distinguished old source coordinate `q`.  Extending the eight
rows in (14) to that coordinate gives a `14 x 8` mixed-coefficient
matrix `M_q(t)`, together with the two binary diagonal covectors
`d_alpha,q(t)` and `d_beta,q(t)`.

Work over `Q(r,x)`, retain `Y,t0,...,t3`, and impose (6).  Normalize
the first binary diagonal and invert the second:

```text
M_q(t) z=0,
d_alpha,q(t) z=1,
ub d_beta,q(t) z=1,
Y^2-f(r,x)=0.                                       (23)
```

Exact block elimination of `z,ub` gives

| distinguished `q` | projected marking ideal |
| ---: | --- |
| `0` | `(1)` |
| `1` | `(1)` |
| `2` | `(1)` |
| `3` | `(1)` |

Because `Y^2-f(r,x)` is irreducible over `Q(r,x)`, these are
function-field unit certificates on the actual elliptic surface, not
certificates on an inconsistent parameter branch.  Therefore no
marking at the generic point admits a binary extension with both
diagonals nonzero.

An `H31` lift would supply exactly such a neighbouring `Delta_2`
extension.  It follows that the generic marked fibre of the second
component is empty.

## From the generic theorem to the complete regular chart

The function-field calculation proves that the survivor projection
does not dominate the elliptic surface.  It does **not** determine the
support divisor of that projection.  The already closed loci include:

```text
the sections (x,Y)=(1,+/-r^2);
the factorized fibres over r=+/-1;
the pure-direction base-locus curves U=S=0;
their source/mode symmetry orbit.                   (24)
```

The generic theorem alone allowed further survivor curves inside the
regular elliptic chart.  The first quotient-kernel refinement treats
the middle
distinguished coordinates `q=1,2`, a universal mixed-kernel line reduces
the survivor question to rank drop of a `14 x 7` quotient matrix.  On
an explicit dense pivot chart, its bordered minors force every extra
kernel direction onto either the sections in (24), with exactly their
already-closed markings, or the pure-direction/singular-fibre loci:

- [`P5_H31_ELLIPTIC_MIDDLE_COORDINATE_RANK_DROP.md`](../elliptic-middle-coordinate-rank-drop/P5_H31_ELLIPTIC_MIDDLE_COORDINATE_RANK_DROP.md)

At that intermediate stage, the pivot complement and the end
coordinates `q=0,3` remained.  The end-coordinate generic chart is also
exact: their universal kernels
have a unit `a1` component, and one bordered quotient minor proves full
rank whenever `t2!=x` and `t3!=1`, away from the already displayed
geometric factors:

- [`P5_H31_ELLIPTIC_END_COORDINATE_FULL_RANK_CHART.md`](../elliptic-end-coordinate-full-rank-chart/P5_H31_ELLIPTIC_END_COORDINATE_FULL_RANK_CHART.md)

The deepest `q=0,3` intersections of those divisors are now closed as
well.  Two-minor compatibility produces conjugate residual trisections
whose common normalization is a smooth genus-two curve.  The marking
equations force one candidate in each orientation, but two further
quotient minors have coprime residual factors and exclude both:

- [`P5_H31_ELLIPTIC_END_GENUS_TWO_EXCEPTION_OBSTRUCTION.md`](../elliptic-end-genus-two-exception/P5_H31_ELLIPTIC_END_GENUS_TWO_EXCEPTION_OBSTRUCTION.md)

The complete regular `t2=x` divisor is now closed too.  The same
genus-two normalization reduces its residual markings to two
univariate minors; their resultant and one quadratic-exception minor
exclude every point for both endpoints:

- [`P5_H31_ELLIPTIC_END_T2_DIVISOR_OBSTRUCTION.md`](../elliptic-end-t2-divisor/P5_H31_ELLIPTIC_END_T2_DIVISOR_OBSTRUCTION.md)

The complete regular `t3=1` divisor is closed as well.  Its apparent
quadratic marking cover splits into two rational branches over the
elliptic function field.  Two quotient minors force both branches onto
the same genus-two trisection.  On its normalization, univariate gcds
leave only `s=-1+/-sqrt(2),1,+/-i`; exact mixed and binary-diagonal
ranks exclude every lift at those points for both endpoints:

- [`P5_H31_ELLIPTIC_END_T3_DIVISOR_OBSTRUCTION.md`](../elliptic-end-t3-divisor/P5_H31_ELLIPTIC_END_T3_DIVISOR_OBSTRUCTION.md)

The middle-coordinate pivot complement is now closed too.  Four
residual factors and five terminal quotient minors close
`t0=0,t3=1,t2=r^2x`; a separate two-minor pivot closes the regular
two-torsion slice `Y=0`:

- [`P5_H31_ELLIPTIC_MIDDLE_COORDINATE_PIVOT_COMPLEMENT.md`](../elliptic-middle-coordinate-pivot-complement/P5_H31_ELLIPTIC_MIDDLE_COORDINATE_PIVOT_COMPLEMENT.md)

Therefore every marked fibre in the regular elliptic chart is excluded
for all four distinguished coordinates.  The normalization boundary is
now closed as well.  The identities

```text
x=C(1-H^2)/U,  D=S(1-H^2)/U^2
```

reduce it to the closed factorized/base-locus strata and two rational
`r=0` curves.  Exact relative projection and a uniform marked minor
exclude both projective curves:

- [`P5_H31_DIAGONAL_QUADRIC_NORMALIZATION_BOUNDARY_OBSTRUCTION.md`](../diagonal-quadric-normalization-boundary/P5_H31_DIAGONAL_QUADRIC_NORMALIZATION_BOUNDARY_OBSTRUCTION.md)

Thus the complete normalized affine slice `A=B=F=1` is excluded.  A
complete component theorem must now classify the outer
projective/gauge boundary `A B F=0`.

## Verification

Run:

```text
python claims/p5/h31/diagonal-quadric-elliptic/verify_p5_h31_diagonal_quadric_elliptic_generic.py
python claims/p5/h31/diagonal-quadric-elliptic/audit_p5_h31_diagonal_quadric_elliptic_generic.py
```

The verifier checks (1)--(24), the irreducible quadratic extension,
the Weierstrass invariants and infinity model, the good-reduction
orders of the known section, and all four exact saturated projections
(23).  It uses `r,x` only as coefficient-field parameters; `Y` remains
a retained variable subject to (6).  This domain distinction is
essential: divisions by `x` or `x+r^2-1` would be invalid if those
symbols were ordinary polynomial variables.

The independent audit clears every row denominator, rebuilds the
mixed systems with a dynamic-programming permanent, and recomputes the
same four unit ideals.
