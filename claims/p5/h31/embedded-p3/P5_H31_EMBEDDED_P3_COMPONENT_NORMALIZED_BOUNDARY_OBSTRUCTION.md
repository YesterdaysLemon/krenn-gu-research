# Complete normalized-chart `H31` obstruction on the embedded-`P_3` component

## Status

This is an exact characteristic-zero theorem on the full normalized
affine chart

```text
A B r !=0
```

of the ninth pure-`P_4` component.  It strengthens
[`P5_H31_EMBEDDED_P3_COMPONENT_GENERIC_OBSTRUCTION.md`](P5_H31_EMBEDDED_P3_COMPONENT_GENERIC_OBSTRUCTION.md)
by closing every zero of that theorem's nine-point discriminant.

The complete marked `H31` fibre is empty throughout this normalized
chart.  The proof classifies the binary boundary exactly and then uses
small one-marked or stacked one-marked determinants; it does not use
ambient-map enumeration or a broad elimination.

This theorem does not close the omitted normalization divisors
`A r=0`, the projective boundary of the pure component, component
exhaustiveness, or the global Krenn--Gu conjecture.  The normalized
weighted `H22` boundary has since been closed separately by
[`P5_H22_EMBEDDED_P3_COMPONENT_RANK_TWO_LINE_BOUNDARY_OBSTRUCTION.md`](../../../../P5_H22_EMBEDDED_P3_COMPONENT_RANK_TWO_LINE_BOUNDARY_OBSTRUCTION.md)
and
[`P5_H22_EMBEDDED_P3_COMPONENT_RANK_ONE_COLLAPSE_OBSTRUCTION.md`](../../../../P5_H22_EMBEDDED_P3_COMPONENT_RANK_ONE_COLLAPSE_OBSTRUCTION.md).

## Normalized component and insertion map

Use

```text
alpha_0=(0, 1,S,U),       beta_0=(1, 0,1,T),

alpha_1=(0,-1,1,0),       beta_1=(0,-1,0,1),
alpha_2=(0, 1,0,1),       beta_2=(0, 1,1,0),
alpha_3=(0, 0,1,1),       beta_3=(0,-1,0,1),       (1)
```

with markings

```text
beta_i(t_i)=beta_i+t_i alpha_i.                   (2)
```

The generic theorem reduces source-coordinate-zero extension to the
`7 x 6` apolar insertion matrix `N(w)`.  Its projective rank-drop
support is

```text
V(L_1) union V(L_2) union V(L_4)
 union {e_p,e_q,e_r},                              (3)
```

where

```text
L_1=p-q-rho,       L_2=p-q+rho,
L_3=p+q-rho,       L_4=p+q+rho.                   (4)
```

At generic points of the first three lines, the kernels are
`<z_2>,<z_3>,<z_1>`, so the all-alpha diagonal vanishes.  It remains
to understand the nine special points where either a coordinate
point occurs or a line kernel grows.

## Exact kernels at the nine points

Use columns

```text
(x_1,x_2,x_3,z_1,z_2,z_3).
```

The kernels are

| point `w` | `ker N(w)` |
| --- | --- |
| `[1:0:0]` | `<(1,-1,0,1,-1,1)>` |
| `[0:1:0]` | `<(1,0,1,0,1,0)>` |
| `[0:0:1]` | `<(0,1,1,1,0,1)>` |
| `[1:0:1]` | `<x_2,z_2>` |
| `[1:1:0]` | `<z_2,z_3>` |
| `[0:1:-1]` | `<z_1,z_2>` |
| `[1:0:-1]` | `<z_1,z_3>` |
| `[0:1:1]` | `<x_3,z_3>` |
| `[1:-1:0]` | `<x_1,z_1>` |                    (5)

The three kernels in the middle of the lower block have all
`x_i=0`, so they cannot give a nonzero all-alpha diagonal.

For the other three lower-block points, the insertion tensor is

```text
ell_i tensor f(a,-,-),
```

where `a=(1,S,U)` is the projected alpha row.  Its all-alpha
coefficient is nonzero only when `x_i!=0`.  Modulo the adjustable
all-beta coefficient, it can be a rank-one diagonal tensor only when
the corresponding pair matrix has rank one.  The determinants are

```text
w=[1:0:1]:   -L_1(a)L_3(a),
w=[0:1:1]:    L_2(a)L_3(a),
w=[1:-1:0]:   L_3(a)L_4(a).                       (6)
```

The factor other than `L_3(a)` is the nonzero all-alpha coefficient.
Thus all three cases require

```text
Lambda=P span((1,S,U),(0,1,T))=V(L_3).            (7)
```

At the coordinate points, the three truncated Segre relations factor
as

```text
[1:0:0]:  4(Q-R)(Q+R),
[0:1:0]:  4(P-R)(P+R),
[0:0:1]:  4(P-Q)(P+Q),                            (8)
```

where `(P,Q,R)=a`, and the second factor in each row is the
all-alpha coefficient.  Hence a genuine binary direction requires

```text
[1:0:0]:  Lambda=V(q-rho),
[0:1:0]:  Lambda=V(p-rho),
[0:0:1]:  Lambda=V(p+q).                          (9)
```

The last alternative is impossible in the normalization (1), because
`(0,1,T)` never lies in `V(p+q)`.

Equations (5)--(9) prove that only the following three plane strata
can have a binary neighbor:

```text
I.   T=1, U=S+1       (Lambda=V(L_3));
II.  T=1, U=S         (Lambda=V(q-rho));
III. T=0, U=1         (Lambda=V(p-rho)).           (10)
```

## Complete binary survivor table

Write extension coordinates in the order

```text
e=(x_0,x_1,x_2,x_3,y_0,y_1,y_2,y_3)
```

and call the free reconstruction coordinate `y`.  Scaling a genuine
extension gives the following complete list.  In stratum I, the first
row requires `S!=0`, the third requires `S!=-1`; an inaccessible row
means that the marked beta direction would equal alpha.

| stratum; `w` | marking `(t_0,t_1,t_2,t_3)` | extension `e` | diagonals `(A,B)` |
| --- | --- | --- | --- |
| I; `[1:0:1]` | `(-1/S,-1,-h,-1)` | `(0,0,1,0,y,0,0,0)` | `(-2S,-2y)` |
| I; `[0:1:1]` | `(0,0,0,-h)` | `(0,0,0,1,y,0,0,0)` | `(2,-2y)` |
| I; `[1:-1:0]` | `(-1/(S+1),-h,-1,0)` | `(0,1,0,0,y,0,0,0)` | `(2(S+1),-2y)` |
| II; `[1:0:0]` | `(-1/S,-1,-1,-1/2)` | `(1,1,-1,0,y,0,0,1)` | `(4S,-2(Sy+1)/S)` |
| III; `[0:1:0]` | `(0,0,-1/2,0)` | `(-S,1,0,1,y,0,1,0)` | `(4,-2(y+1))` |  (11)

Here `h` is arbitrary, while both displayed diagonals must be nonzero.
Every extension omitted from (11) either has a zero diagonal or differs
only by an overall nonzero scale.

## One-marked exclusion

Rows of an `8 x 4` neighboring one-marked map are numbered
`000,...,111` by `0,...,7`.  The following determinants cover the
first four rows of (11).

For I, `[1:0:1]`,

```text
mode 1, rows 0567:   8y(h-1)/S,
mode 3, rows 0127:  -8Shy.                        (12)
```

They cannot both vanish.  Their transverse pure-hyperplane columns
contain respectively `-2/S` and `2`.

For I, `[0:1:1]`, if `S!=0`,

```text
mode 2, rows 0247:   8S y^2.                      (13)
```

At the endpoint `S=0`, use instead

```text
mode 1, rows 0457:   8hy,
mode 2, rows 0567:  -8y(h-1).                     (14)
```

The transverse pure entries are `-2,2,-2`.

For I, `[1:-1:0]`, if `S!=0`,

```text
mode 2, rows 0147:   8S y^2(S+1).                 (15)
```

At `S=0`, use

```text
mode 3, rows 0127:   8hy,
mode 2, rows 0467:   8y(h-1).                     (16)
```

The corresponding transverse pure entries are
`-2/(S+1),2,-2`.

For II,

```text
mode 1, rows 0137:  -16S(Sy+1),                   (17)
```

and the transverse pure entry is `1`.

Every factor required in (12)--(17) is nonzero on its stated branch.
Thus some neighboring one-marked map is injective, and its pure
transverse column forces the same third target row to vanish globally.

## The deepest point of stratum III

For III with `S!=0`,

```text
mode 1, rows 0237:  -16S(y+1),                    (18)
```

with transverse pure entry `1`, excludes the lift.

At `S=0`, the genuine binary condition gives `y!=-1`.  If `y!=1`,
use

```text
mode 1, rows 0247:   8(y-1)(y+1).                 (19)
```

The only remaining point is

```text
S=0,       y=1.                                   (20)
```

Here every neighboring one-marked map has rank at most three, so a
single-hyperplane minor cannot finish the argument.  Reconstruct the
full five-dimensional binary rows:

```text
alpha_0=(0, 1,0,1,0),   beta_0=(1, 0,1, 0,1),
alpha_1=(0,-1,1,0,1),   beta_1=(0,-1,0, 1,0),
alpha_2=(0, 1,0,1,0),   beta_2=(0,1/2,1,-1/2,1),
alpha_3=(0, 0,1,1,1),   beta_3=(0,-1,0, 1,0).     (21)
```

Stack, at mode one, the one-marked equations on the neighboring
source hyperplane with contraction row `e_0` and the pure source
hyperplane with contraction row `e_4`.  Rows

```text
(0,2,7,10,14)
```

and all five source columns have determinant

```text
8.                                                  (22)
```

Thus the candidate third row at mode one is zero on the full
five-dimensional source.  This contradicts rank three of the local
map, which is forced by conciseness of `Delta_3`.

Equations (12)--(22) exclude every binary survivor in (11).  Combined
with the exact arrangement classification, they prove that the
complete marked `H31` fibre is empty on the normalized component
chart.

## Verification

Run

```text
python claims/p5/h31/embedded-p3/verify_p5_h31_embedded_p3_component_normalized_boundary.py
python claims/p5/h31/embedded-p3/audit_p5_h31_embedded_p3_component_normalized_boundary.py
```

The primary verifier reconstructs the nine insertion kernels, the
truncated Segre factorizations, all five binary survivor families,
every one-marked determinant and transverse pure entry, and the
stacked determinant (22).  The independent audit rebuilds permanents
by subset multiplication over two finite fields, checks the survivor
tables at generic modular parameters, and replays the deepest stacked
rank certificate.  The modular audit is corroboration only; the
theorem is the characteristic-zero case split above.

## Honest frontier

The ninth component's full normalized affine chart is now closed for
`H31`.  The support-two normalization divisor `A=0`, `B!=0` is closed
separately in
[`P5_H31_EMBEDDED_P3_COMPONENT_SUPPORT_TWO_BOUNDARY_OBSTRUCTION.md`](P5_H31_EMBEDDED_P3_COMPONENT_SUPPORT_TWO_BOUNDARY_OBSTRUCTION.md).
Other mode-zero-plane charts and the projective compactification
were the remaining frontier at that checkpoint.  The `r=0`, `A B!=0`
divisor is now closed in
[`P5_H31_EMBEDDED_P3_COMPONENT_R_ZERO_BOUNDARY_OBSTRUCTION.md`](P5_H31_EMBEDDED_P3_COMPONENT_R_ZERO_BOUNDARY_OBSTRUCTION.md).
Together with the support-two theorem, this closes the whole affine
`B!=0` family.  Its projective compactification is now closed in
[`P5_H31_EMBEDDED_P3_COMPONENT_PROJECTIVE_CLOSURE_OBSTRUCTION.md`](P5_H31_EMBEDDED_P3_COMPONENT_PROJECTIVE_CLOSURE_OBSTRUCTION.md),
so the complete component fibre is empty.
The exact binary boundary classification is reusable for weighted
`H22`, where the slope-dependent projected line can meet the same
nine insertion points.
