# Weighted `H22` boundary obstruction for rank-two projected lines

## Status

This is an exact characteristic-zero theorem on the normalized ninth
pure-`P_4` component, including every zero of the generic weighted
discriminant for which the `D_01^r` projection of the mode-zero plane
still has rank two.

Every such weighted boundary point has empty marked `H22` fibre.  The
`D_23^r` direction retains its structural zero diagonal; the
`D_01^r` binary survivors form six explicit marked families, all
excluded by small one-marked or stacked one-marked determinants.

This theorem's projected-line argument does not cover the separate
rank-one projection collapse, where the two projected mode-zero rows
become proportional.  That stratum has since been closed by the
complementary marked contraction:
[`P5_H22_EMBEDDED_P3_COMPONENT_RANK_ONE_COLLAPSE_OBSTRUCTION.md`](P5_H22_EMBEDDED_P3_COMPONENT_RANK_ONE_COLLAPSE_OBSTRUCTION.md).
The two theorems still do not close the component's omitted
normalization/projective boundary, prove component exhaustiveness, or
resolve the global Krenn--Gu conjecture.

## Weighted projection and insertion arrangement

Use the normalized component bases

```text
alpha_0=(0, 1,S,U),       beta_0=(1, 0,1,T),

alpha_1=(0,-1,1,0),       beta_1=(0,-1,0,1),
alpha_2=(0, 1,0,1),       beta_2=(0, 1,1,0),
alpha_3=(0, 0,1,1),       beta_3=(0,-1,0,1).       (1)
```

For slope `r`,

```text
D_01^r(z,e)=(r z_0+z_1,z_2,z_3,e),
D_23^r(z,e)=(z_0,z_1,r z_2+z_3,e).                (2)
```

The `D_23^r` all-alpha coefficient is always zero because its first
target column is source coordinate zero and every `alpha_i` has zero
there.

For `D_01^r`, the projected mode-zero rows span

```text
Lambda_r=P span(a,b_r),
a=(1,S,U),          b_r=(r,1,T).                  (3)
```

When `a,b_r` are independent, the generic weighted theorem identifies
the mixed-extension map with the same apolar insertion matrix `N(w)`
as in `H31`.  Its rank-drop support consists of three signed lines and
three coordinate points.  The exact exceptional-kernel and
truncated-Segre classification in
[`P5_H31_EMBEDDED_P3_COMPONENT_NORMALIZED_BOUNDARY_OBSTRUCTION.md`](../../h31/embedded-p3/P5_H31_EMBEDDED_P3_COMPONENT_NORMALIZED_BOUNDARY_OBSTRUCTION.md)
now gives four possible projected-line strata:

```text
I.   U=S+1, T=r+1       (Lambda_r=V(p+q-rho));
II.  U=S,   T=1         (Lambda_r=V(q-rho));
III. U=1,   T=r         (Lambda_r=V(p-rho));
IV.  S=-1,  r=-1        (Lambda_r=V(p+q)).         (4)
```

Stratum I contains three exceptional markings; II--IV contain one
each.  No other rank-two projected line has a genuine binary
neighbor.

## The three signed-line markings

Put

```text
k=rs-1.
```

On I, rank two means `k!=0`.  With extension order

```text
(x_0,x_1,x_2,x_3,y_0,y_1,y_2,y_3),
```

the three complete binary families, scaled so the active `x_i=1`,
are

| `w` | marking `(t_0,t_1,t_2,t_3)` | extension | diagonals |
| --- | --- | --- | --- |
| `[1:0:1]` | `(-1/S,-1,-h,-1)` | `(0,0,1,0,y,0,0,0)` | `(-2S,-2y)` |
| `[0:1:1]` | `(-r,0,0,-h)` | `(0,0,0,1,y,0,0,0)` | `(2,-2y)` |
| `[1:-1:0]` | `(-(r+1)/(S+1),-h,-1,0)` | `(0,1,0,0,y,0,0,0)` | `(2(S+1),-2y)` | (5)

The first and third markings are present only when their denominators
are nonzero.  The genuine condition includes `y!=0`.

For the first row, neighboring one-marked minors are

```text
mode 1, rows 0567:   8y(h-1)k^2/S,
mode 3, rows 0127:  -8Shy.                         (6)
```

Their transverse pure evaluations on the kernel vector

```text
(1,-r,0,0)
```

contain `-2/S` and `2`; hence (6) excludes every `h`.

For the second row, if `S!=0`,

```text
mode 2, rows 0247:   8S y^2.                       (7)
```

At `S=0`, use

```text
mode 1, rows 0457:   8hyk^2,
mode 2, rows 0567:  -8y(h-1)k^2.                  (8)
```

The necessary transverse evaluations are respectively nonzero; on
the branch of the second minor at `h=0`, row `111` evaluates to `-2`.

For the third row, if `S!=0`,

```text
mode 2, rows 0147:   8S y^2(S+1).                  (9)
```

At `S=0`, use

```text
mode 3, rows 0127:   8hy,
mode 2, rows 0467:   8y(h-1)k^2.                  (10)
```

Again the transverse evaluations contain `2` and, on the second
branch, `-2`.

## The first two coordinate-point markings

For II, put

```text
k=rs-1 !=0.
```

The only binary family is

```text
t=(-1/S,-1,-1,-1/2),
e=(1,1,-1,0,y,0,0,1),

A=4S,
B=-2(-rS+Sy+1)/S.                                 (11)
```

Thus `S!=0` and `F_1=-rS+Sy+1!=0`.  The determinant

```text
mode 1, rows 0137:  -16S F_1                      (12)
```

is nonzero, and the transverse pure evaluation contains the constant
`1`.

For III, put

```text
k=1-rS !=0.
```

The only binary family is

```text
t=(-r,0,-1/2,0),
e=(-S,1,0,1,y,0,1,0),

A=4,
B=-2(-rS+y+1).                                    (13)
```

Let `F_2=-rS+y+1`.  If `S!=0`,

```text
mode 1, rows 0237:  -16S F_2.                     (14)
```

At `S=0`, the genuine condition is `y!=-1`.  If `y!=1`,

```text
mode 1, rows 0247:   8(y-1)(y+1).                 (15)
```

The dense minor uses the transverse pure entry at row `011`, equal to
`S`.  On the endpoint `S=0`, the endpoint minor instead uses row `000`,
whose transverse pure entry is `2`.

At the deepest point `S=0,y=1`, every neighboring one-marked map has
rank three.  Stack the mode-one maps for the weighted contraction row

```text
(1,r,0,0,0)
```

and the pure contraction row `e_4`.  Rows

```text
(0,2,7,10,14)
```

and all five source columns have determinant

```text
8,                                                   (16)
```

independent of `r`.  Hence the third local row is zero globally.

## The third coordinate-point marking

Stratum IV is new relative to the unweighted `H31` normalization.  Put

```text
k=T+U !=0.
```

The coordinate point `[0:0:1]` occurs at

```text
t=(1,-1/2,0,-1),
e=(-U,0,1,1,y,1,0,0),

A=4,
B=-2(T+U+y).                                      (17)
```

Let `F_3=T+U+y`, which is nonzero for a genuine neighbor.  If `U!=0`,

```text
mode 2, rows 0237:  -16U F_3,                     (18)
```

and the transverse pure evaluation contains `U`.

At `U=0`, rank two gives `T!=0`.  If `y!=T`,

```text
mode 2, rows 0247:  -8(y-T)(y+T),                 (19)
```

and the transverse pure evaluation contains `2`.

At the deepest point `U=0,y=T`, every neighboring one-marked map again
has rank three.  Stack, at mode two, the maps for contraction rows

```text
(1,-1,0,0,0),        e_4.
```

Rows `(0,2,8,14,15)` give

```text
det=-8.                                             (20)
```

Thus the candidate third row vanishes globally here as well.

Equations (6)--(20) exclude all six binary families.  Since the other
weighted direction has the structural zero diagonal, the marked
`H22` fibre is empty at every normalized point with rank-two
projected mode-zero image.

## Rank-one projection collapse requires the other marked slice

The two vectors in (3) become proportional precisely when

```text
rS=1,             T=rU.                            (21)
```

This is not a point of the projective-line incidence used above:
`Lambda_r` collapses from a line to a point.  At the special marking
`t_0=-r`, the projected marked-beta row is zero and the beta diagonal
can be supplied entirely by the extension coordinate.  The
single-slice insertion argument therefore changes type.  This
rank-one gate stratum is not claimed by the present theorem.  The
separate rank-one theorem uses the required pure `D_23^r` slice as a
second insertion pencil and excludes the collapse completely.

## Verification

Run

```text
python claims/p5/h22/embedded-p3/verify_p5_h22_embedded_p3_component_rank_two_line_boundary.py
python claims/p5/h22/embedded-p3/audit_p5_h22_embedded_p3_component_rank_two_line_boundary.py
```

The primary verifier reconstructs all six binary families, every
one-marked determinant and transverse pure evaluation, and the two
constant stacked determinants.  The independent audit rebuilds
permanents by squarefree subset multiplication and replays generic,
endpoint, and deepest samples over two finite fields.  The modular
audit is corroboration only; the theorem is the characteristic-zero
factor cover above.
