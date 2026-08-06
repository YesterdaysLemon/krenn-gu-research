# Parameter-pivot `H22` boundaries of the disjoint mixed-star component

## Status

This is an exact characteristic-zero theorem at the generic points of
twelve codimension-one rank-two boundary branches of the eighth
pure-`P_4` component.

On every branch, in both weighted `H22` directions, a genuine binary
neighbour violates one of two mode-zero one-marked rank conditions.
Thus the generic weighted `H22` incidence is empty there.

This does not close further special divisors inside the twelve branches,
all parameter or projective boundaries, component exhaustiveness, the
complete `P_5 -> Delta_3` obstruction, or the global prize conjecture.

## Splitting the pivot divisors

The component equation is

```text
Phi =
 a^2 b f phi^2+a^2 f^2
 -b^2 f^2+b^2 phi^2-bf-1.                         (1)
```

The two symmetric coordinate-pivot divisors split as

```text
Phi|_(a=b)
 = (bf+1)(b phi-1)(b phi+1),

Phi|_(a=-b)
 = (bf+1)(b phi-1)(b phi+1).                      (2)
```

On the other normalized pivot,

```text
b^2 Phi|_(bf=-1)
 = -(a-b)(a+b)(b phi-1)(b phi+1).                 (3)
```

If

```text
bf=-1,       b phi=+1 or -1,                       (4)
```

then

```text
j=f+b phi^2=0,
kappa=phi(bf+1)=0,
eta=-(bf+1)=0,
```

so the row `y_2` in the component normal form vanishes and the second
local plane has rank one.  Those two branches are outside the
all-rank-two stratum.

The coordinate divisors split as

```text
Phi|_(b=0) = (af-1)(af+1),
Phi|_(f=0) = (b phi-1)(b phi+1).                  (5)
```

The two remaining coordinate sections used here are irreducible
quadratic branches:

```text
B_11: a=0,
      b^2 phi^2-b^2 f^2-bf-1=0,

B_12: phi=0,
      a^2 f^2-b^2 f^2-bf-1=0.                    (6)
```

Indeed, in either case reducibility over `C(b,f)` would require

```text
(bf)^2+bf+1
```

to be a square.  Its two simple cyclotomic divisors rule that out.

The twelve generic rank-two branches treated here are therefore

```text
B_1: a= b,  bf=-1,
B_2: a=-b,  bf=-1,

B_3: a= b,  b phi= 1,
B_4: a= b,  b phi=-1,
B_5: a=-b,  b phi= 1,
B_6: a=-b,  b phi=-1,

B_7: b=0,  af= 1,
B_8: b=0,  af=-1,
B_9: f=0,  b phi= 1,
B_10:f=0,  b phi=-1,

B_11:a=0 with its quadratic relation,
B_12:phi=0 with its quadratic relation.            (7)
```

Their function fields are respectively `C(b,phi,r)` for `B_1,B_2`
and `C(b,f,r)` for `B_3,...,B_6`, `C(f,phi,r)` for
`B_7,B_8`, and `C(a,phi,r)` for `B_9,B_10`.
The final two fields are the quadratic extensions
`C(b,f,r)(phi)` and `C(b,f,r)(a)` defined in (6).

## Binary incidence and ternary rank

For either weighted direction `D_01^r,D_23^r`, let

```text
M_D(t) z=0                                          (6)
```

be the fourteen mixed binary equations in the eight extension
coordinates.  Let `A_D(z),B_D(z)` be the two binary diagonal
coefficients.

Normalize a genuine extension by

```text
A_D(z)=1,       w B_D(z)-1=0.                      (9)
```

For a ternary lift, the mode-zero one-marked map factors through a
three-dimensional target local space, so every `4 x 4` minor must
vanish.  Let

```text
H_0137, H_0157.                                   (10)
```

be the determinants of its row sets `0137` and `0157`.

For branches `B_1,...,B_8,B_11,B_12` in both directions, and for `B_9,B_10` in
direction `D_23`, exact standard-basis reduction gives

```text
(
  M_D(t)z,
  A_D(z)-1,
  w B_D(z)-1,
  H_0137,
  H_0157
) over K(B_i) = (1).                              (11)
```

On `B_9,B_10` in direction `D_01`, the minor `H_0137` loses the last
six finite survivor directions.  Replacing it by the row minor

```text
H_0457                                            (12)
```

gives

```text
(
  M_D(t)z,
  A_D(z)-1,
  w B_D(z)-1,
  H_0157,
  H_0457
) over K(B_i) = (1).                              (13)
```

Equations (11)--(13) comprise twenty-four independently replayed unit
ideals.
Hence every genuine binary neighbour on a generic point of any branch
has one-marked rank four and cannot lift to ternary `H22`.

## Geometric interpretation

The normalized component chart loses a Grassmann pivot when `a+b=0`
or `bf+1=0`.  Factoring `Phi` before elimination replaces that singular
chart boundary by rational branch fields.  The broad incidence
then becomes easier than the generic component: the same two Fitting
coordinates cut the binary survivor scheme away from the ternary
rank-three locus on eight branches.  On the `f=0` branches, a second
two-minor chart closes the only exceptional direction.

This is a small instance of normalization by irreducible boundary
components: factor the base first, pass to each branch function field,
and only then compute the incidence fibre.

## Honest frontier

Together with the generic theorem and the `r=+/-1` theorem, this closes:

1. the generic total-space point of the eighth component's weighted
   `H22` incidence;
2. the equal- and opposite-weight slope divisors; and
3. the generic points of all twelve genuine rank-two branches cut out
   by `a^2-b^2=0`, `bf+1=0`, `b=0`, `f=0`, `a=0`, or `phi=0`.

Further coefficient divisors inside those branch fields, other
component-parameter divisors, projective charts, and component
exhaustiveness remain open.  No graph satisfying the prize equation
and no global nonexistence proof is claimed.

## Verification

Run:

```text
python \
  verify_p5_h22_disjoint_mixed_star_parameter_pivot_boundary_obstruction.py

python \
  audit_p5_h22_disjoint_mixed_star_parameter_pivot_boundary_obstruction.py
```

The primary verifier reconstructs ten rationally parametrized and two
quadratic component branches, checks their component relations and
irreducibility claims, builds both weighted mixed matrices and
one-marked maps, and requires all twenty-four ideals in (11)--(13) to
reduce to `(1)`.

The independent audit imports nothing from the primary verifier.  At
one rank-two point of each rational branch over `F_7` and of each
quadratic branch over `F_11`, it exhausts every affine
marked basis at slope two and verifies both row minors on every genuine
projective extension direction.  This finite-field census is
corroboration only; (11)--(13) prove the theorem over `C`.
