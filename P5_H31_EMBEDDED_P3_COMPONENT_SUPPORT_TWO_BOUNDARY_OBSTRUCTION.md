# `H31` obstruction on the support-two boundary of the ninth component

## Status

This is an exact characteristic-zero theorem on the normalization
divisor `A=0`, `B!=0` of the embedded-`P_3` ninth pure-`P_4`
component.

The complete marked `H31` fibre is empty on this divisor.  Together
with the normalized-chart theorem, this closes the entire
support-three chart and its nonzero support-two specialization.  The
remaining `r=0`, `A B!=0` divisor has since been closed separately,
so only the projective compactification of the component remains.

The proof is symbolic.  The support-two `P_3` degeneration has a
seven-by-six insertion matrix whose first unwanted row already forces
one exceptional line.  Its generic points fail a one-marked
determinant.  The coordinate endpoint is excluded by the third
`H31` contraction, except at one matrix-pencil resonance; three
factored covers, a stacked determinant, and one fixed coefficient
close that resonance.

This theorem does not prove component exhaustiveness, produce a prize
graph, or resolve the global Krenn--Gu conjecture.

## Support-two normal form

Use source coordinates `0,1,2,3` on the pure hyperplane.  After putting
the `H31` root row into its standard common-three form, the remaining
source-torus invariant is a nonzero scalar `C=1/B`.  Choose pure-factor
bases

```text
alpha_0=(0,P,Q,R),         beta_0=(1,p,q,rho),

alpha_1=(0,0,1,0),         beta_1=(0,1,0,-C),
alpha_2=(0,1,0,C),         beta_2=(0,0,1,0),
alpha_3=(0,0,1,0),         beta_3=(0,1,0,-C).      (1)
```

The last three plane normals have common support two; modes one and
three coincide.  The only nonzero pure coefficient is

```text
T_BBBB=-2C.                                         (2)
```

Since all four alpha rows have source coordinate zero equal to zero,
deleting any source coordinate other than zero leaves an identically
zero all-alpha column.  Only deletion zero can be a genuine
`Delta_2` neighbour.

## Degenerate insertion matrix

Write

```text
(x_1,x_2,x_3,z_1,z_2,z_3)
```

for the extension coordinates in the unmarked bases of the last three
modes, and let `w=(p,q,rho)` be the projected marked beta row in mode
zero.  Ordering unwanted words

```text
000,001,010,011,100,101,110,
```

the beta-slice insertion matrix is

```text
N_C(w)=
[Cp+rho,       0, Cp+rho,       0,       0,       0]
[     0, -Cp+rho,      0,       0,       0, Cp+rho]
[     0,        0,      0,       0,       0,       0]
[-Cp+rho,       0,      0,       0, -Cp+rho,       0]
[     0, -Cp+rho,      0, Cp+rho,       0,       0]
[     0,    -2Cq,      0,       0,       0,       0]
[     0,        0,-Cp+rho,       0, -Cp+rho,       0].
                                                               (3)
```

Its only potentially nonzero maximal minor is, up to the row choice,

```text
4Cq(Cp-rho)^2(Cp+rho)^3.                          (4)
```

More importantly, the all-alpha coefficient is

```text
A=(CP+R)(x_1+x_3).                                 (5)
```

The first row of (3) is `(Cp+rho)(x_1+x_3)=0`.
Therefore every genuine binary neighbour satisfies

```text
rho=-Cp.                                           (6)
```

This avoids a case-by-case traversal of all three Fitting lines.

## Generic points of the exceptional line

First suppose `p!=0`.  Equations (3) give, after a nonzero scaling,

```text
x_1=x_3=-h,      x_2=0,      z_2=h.               (7)
```

Undoing the marked-basis shears in modes `1,2,3`, the alpha-slice
mixed equations are

```text
(CP+R)(z_3-2ht_3),
-2ht_2(CP+R),
t_2(CP+R)(z_3-2ht_3),

(CP+R)(z_1-2ht_1),
(CP+R)(-2ht_1t_3+t_1z_3+t_3z_1),
t_2(CP+R)(z_1-2ht_1).                              (8)
```

Since `h(CP+R)!=0`, they are equivalent to

```text
t_2=0,       z_1=2ht_1,       z_3=2ht_3,
t_1t_3=0.                                         (9)
```

Put

```text
D=hq+2hp(t_1+t_3)+y_0.
```

The two binary diagonals are

```text
A=-2h(CP+R),            B=-2CD,                   (10)
```

so `D!=0`.  The neighboring mode-two one-marked determinant is

```text
det rows 0457=16C^2h^2p^2(CP+R)D.                 (11)
```

It is nonzero.  Hence the candidate third row restricts to zero on
the neighbouring hyperplane.  On the pure hyperplane, mode two and
row `101` evaluate on the transverse coordinate `e_0` as

```text
-2Cp!=0.                                           (12)
```

Thus the third row vanishes globally, contradicting local rank three.

## The coordinate endpoint

It remains to take

```text
p=rho=0,          q!=0.
```

Scale `q=1` and put

```text
X=x_1+x_3.
```

Equation (5) says `(CP+R)X!=0`.  The third `H31` root contraction is,
up to its adjustable pure term, contraction by

```text
v=e_1+e_2+e_3.
```

Its mixed coefficient on the binary word `BAAA` is

```text
P_5(v,beta_0,alpha_1,alpha_2,alpha_3)
  =(C+1)X.                                         (13)
```

Thus the coordinate endpoint is impossible unless

```text
C=-1.                                              (14)
```

This scalar is the matrix-pencil resonance invisible after setting
`B=1` too early.

## The resonant coordinate fibre

At `C=-1`, the alpha-slice equations first give

```text
t_2=0,       z_1=-t_1X,       z_3=-t_3X,
t_1t_3=0.                                         (15)
```

There are two geometric subcases.

### Transverse mode-zero alpha row

Suppose `P+R!=0`.  Then the remaining two mixed equations give

```text
x_1=x_3=h,             z_2=-h,                    (16)
```

with `h!=0`.  By symmetry take `t_1=0,t_3=k`, and write `y` for the
mode-zero beta extension.  Genuineness is `y!=h`.

The following exact cover excludes every point:

```text
y!=-h:
  mode 3, rows 0347:
  -4h(P-R)(P+R)(y-h)(y+h);

y=-h, k!=0:
  mode 1, rows 0157:
   4hk^2(P-R)^2(y-h)^2;

y=-h, k=0, Q!=0:
  mode 2, rows 0137:
 -16Q^2h^2(P-R)(y-h).                              (17)
```

The pure transverse entries are respectively `R-P`, `R-P`, and `2`.

At the sole deepest point

```text
y=-h,       k=Q=0,
```

stack the mode-one one-marked maps for contractions `e_0` and `e_4`.
Rows

```text
(0,3,7,8,12)
```

give

```text
det=-8h^2(P-R)^2(P+R).                             (18)
```

### Antipodal mode-zero alpha row

Now suppose `P+R=0`.  Scale `X=1`, write

```text
x_1=x,       x_3=1-x,       z_2=d.
```

The third root contraction has two remaining binary mixed
coefficients

```text
2(d+x),             -2(-d+x-1).
```

Both vanish only at

```text
x=1/2,             d=-1/2.                        (19)
```

Here genuineness is `y!=1/2`.  Again take `t_1=0,t_3=k`.  If `k!=0`,

```text
mode 1, rows 0137:
 4P^3k^2(2y-1),                                    (20)
```

and if `k=0,Q!=0`,

```text
mode 2, rows 0137:
 4PQ^2(2y-1).                                      (21)
```

The pure transverse entries contain `2P` and `2`.

At `k=Q=0`, the pure-plus-neighbouring one-marked kernel in mode three
is the line

```text
<(0,0,-2,0,1)>.
```

Any rank-three completion must use this nonzero row.  In the third
root contraction, the target word `BBBG` then has the fixed
coefficient

```text
4.                                                  (22)
```

It cannot be cancelled by the adjustable all-beta pure term.

Equations (11)--(22) exclude every support-two binary family and prove
the theorem.

## Cross-specialty interpretation

The support-two boundary changes the insertion arrangement from three
signed lines plus points into a singular matrix pencil with a zero
row.  The useful invariants are not a large elimination ideal but:

```text
one Fitting factor Cp+rho,
one residual source-torus ratio C,
two exceptional kernel types.
```

This is close in spirit to invariant reductions and Kronecker data for
matrix pencils ([Verdier](https://arxiv.org/abs/1205.1138)) and to
minimal-rank strata of pencils viewed as tensors
([Goulart--Comon](https://arxiv.org/abs/1712.05742)).  The resonant
value `C=-1` is exactly where the binary third-contraction covector
joins the kernel; the next kernel layer then supplies the constant
coefficient (22).

## Verification

Run

```text
python verify_p5_h31_embedded_p3_component_support_two_boundary.py
python audit_p5_h31_embedded_p3_component_support_two_boundary.py
```

The primary verifier reconstructs the insertion pencil, all binary
families, the factor covers, the stacked determinant, and the fixed
third-contraction coefficient symbolically.  The independent modular
audit rebuilds permanent coefficients and replays generic, resonant,
and deepest samples over two finite fields.  The finite-field audit is
corroboration only; the theorem is the characteristic-zero proof above.

The complementary mode-zero-plane divisor is closed in
[`P5_H31_EMBEDDED_P3_COMPONENT_R_ZERO_BOUNDARY_OBSTRUCTION.md`](P5_H31_EMBEDDED_P3_COMPONENT_R_ZERO_BOUNDARY_OBSTRUCTION.md).
