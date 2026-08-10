# The endpoint genus-two exception curve does not survive

## Status

This is an exact characteristic-zero obstruction for both end
coordinates on the deepest marking intersection

```text
q=0 or 3,  t2=x,  t3=1
```

inside the elliptic normalization of the diagonal-quadric component.

Compatibility of two quotient-rank minors produces an apparent
residual trisection of the elliptic K3.  Reframing that trisection as a
smooth hyperelliptic curve of genus two makes the remaining marking
equations elementary.  They force one candidate marking in each
endpoint orientation, but two complementary full-rank minors are
coprime on the genus-two normalization.  Hence both apparent survivor
curves are empty.

The theorem is stated away from the standard factors already separated
in the elliptic chart: `r x D(r^2-1)(x-1)`, the pure-direction factors,
and the parameterization denominators below.  It does not close the
whole `t2=x` or `t3=1` divisors or the compactification boundary.

## The quotient matrix

Put

```text
D=x+r^2-1,
f=x[(1-r^2)x^2+(3r^2-2)x+(r^2-1)^2],
Y^2=f.                                                   (1)
```

Use the marked rows

```text
alpha0=(Y+r^2x,-rx-r^2x,-rx+r^2x,-Y+r^2x),
alpha1=(1,0,0,-1),
alpha2=(0,1,-1,0),
alpha3=(r,-1,-1,r),

beta0=(1,-1,1,1),
beta1=(D,rx+D,rx-D,D),
beta2=(x(1-x)+Y,rx,rx,x(1-x)-Y),
beta3=(0,1,1,0),

beta_i(t)=beta_i+t_i alpha_i.                            (2)
```

For `q=0,3`, delete the unit `a1` component of the corresponding
universal mixed kernel.  This gives the `14 x 7` quotient matrices

```text
N_q=M_q[:,(a0,a2,a3,b0,b1,b2,b3)].                     (3)
```

Put `epsilon=+1` for `q=0` and `epsilon=-1` for `q=3`.  Specialize
`t2=x,t3=1`.  Two full `7 x 7` minors, on row sets

```text
A=(0,1,3,4,5,6,9),
C=(0,1,3,5,6,9,13),
```

are linear in `t1`.  Eliminating `t1` between their non-unit factors
gives, modulo (1),

```text
-epsilon(r^2-1)(Y-epsilon(x^2-x)) J_epsilon,           (4)

J_epsilon=Y D-epsilon r^2x(x-r^2-1).
```

The factor `Y-epsilon(x^2-x)` can vanish on (1) only when

```text
x(x-1-r)(x-1+r)D=0,
```

so it is a unit on the regular non-pure chart.  Thus any quotient rank
drop there must lie on `J_epsilon=0`.

## The residual trisection

Solving `J_epsilon=0` for `Y` gives

```text
Y=epsilon r^2x(x-r^2-1)/D.
```

Substitution in (1) yields

```text
x(x-1)R(r,x)/D^2,
```

where the residual factor is

```text
R =
 r^8-r^6x-4r^6+3r^4x^2-9r^4x+6r^4
 +r^2x^3-6r^2x^2+9r^2x-4r^2
 -x^3+3x^2-3x+1.                                      (5)
```

The factors `x=0` and `x=1` are the visible two-torsion and `-P`
sections.  The remaining curve `R=0` is an irreducible trisection.

Its geometry is simple after using the involution `r -> -r`.  Set

```text
u=r^2,  s=(x-1)/u,
d=s^3+3s^2-s+1,
n=s^3+3s^2+3s+5.                                      (6)
```

Then `R=0` is equivalent on the regular chart to

```text
u=n/d,  x=(s+1)^4/d.                                  (7)
```

Restoring `r` by `v=rd` gives the normalization

```text
v^2=n d.                                               (8)
```

The sextic `nd` has discriminant

```text
2^24 3^3 11,
```

so (8) is a smooth genus-two curve.  The remaining elliptic coordinate
is

```text
Y=epsilon(s-1)(s+1)^3 n/d^2.                          (9)
```

For `q=0`, fibrewise, the zero divisor of `J_+` has degree five.  Its
visible points are the two-torsion section `T` and `-P`; hence the three
residual points have elliptic trace `P+T`.  The `q=3` divisor is its
elliptic conjugate.  This explains both trisections without requiring a
point search.

## The unique candidate marking

On `R=0`, the minor `A` forces

```text
t1 =
 epsilon r^2x(x-r^2-1)^2(x+3r^2-1)/D^3
 =
 epsilon(s-1)^2(s+1)(s+3)n/d^2.                       (10)
```

A further full minor on rows

```text
(0,1,3,4,6,7,9)
```

then forces

```text
t0=-d^2/[2s(s+1)^3n].                                 (11)
```

Thus (7), (9)--(11), together with `t2=x,t3=1`, give the only candidate
in each endpoint orientation.

## Coprime full-rank minors

At that candidate, reduce modulo (8).  The quotient determinants on
rows

```text
(0,1,3,4,6,9,11),
(0,1,3,4,6,9,12)
```

are respectively

```text
epsilon 4096 v(s+1)^28 n^7
  (s^3+2s^2-3s+2)/d^17,

epsilon 4096 v(s+1)^28 n^7
  (s^2+1)/d^17.                                       (12)
```

The two displayed residual polynomials are coprime:

```text
gcd(s^3+2s^2-3s+2, s^2+1)=1.                         (13)
```

Consequently at least one determinant in (12) is nonzero at every
point of either regular genus-two chart.  Each quotient matrix has rank
seven, so the full mixed kernel is only its universal line.  That line
kills the first binary diagonal.  No genuine binary extension, and
hence no `H31` lift, occurs on either apparent exception curve.

## Verification

Run:

```text
python claims/p5/h31/elliptic-end-genus-two-exception/verify_p5_h31_elliptic_end_genus_two_exception.py
python claims/p5/h31/elliptic-end-genus-two-exception/audit_p5_h31_elliptic_end_genus_two_exception.py
```

The primary verifier expands permanents directly.  For both `q=0,3`,
it checks the minor compatibility (4), the residual factor (5), the
birational normalization (6)--(9), the smooth sextic, the forced
markings (10)--(11), and both coprime determinants (12).

The independent audit rebuilds the mixed system with a subset-DP
permanent before replaying the primary verifier.
