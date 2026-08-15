# Arbitrary permanent star-pair two-sided projection-drop theorem

## Status

This note transports the two-sided projection-drop obstruction to the
explicit Delta-admissible `(4,1)` equality-five pair from
`ARBITRARY_PERMANENT_PAIR_DIMENSION_FIVE_R4_ORBIT_CLASSIFICATION_THEOREM.md`.
That pair is inequivalent to the earlier fixed `(4,2)` pair: its unique
annihilator graph is `K_(1,3)` rather than `K_(2,2)`.

For this star pair, every exact `P_6 -> Delta_3` extension satisfies

```text
min_(2<=t<=5) rank(Phi_1|L_t) <= 2,
min_(2<=t<=5) rank(Phi_2|L_t) <= 2.                         (1)
```

The proof localizes every putative all-rank-three projection family by the
same hyperplane-plane product split used for the `(4,2)` pair.  One new
common-missing-factor cell has sensor rank three, so a sensor-rank bound
alone cannot exclude it.  On that cell an exact rational linear combination
of the three diagonal sensors becomes the polarization of `r^2 x_4x_5`.
Its first-mode slice space contains no nonzero rank-one tensor, forcing
tensor rank greater than three; the corresponding weighted `Delta_3` tensor
has rank three.  This closes the cell exactly.

The proof uses the **full exact** `Delta_3` target tensor.  It does not close
the residual where both projection families already have rank-drop modes,
does not treat the Delta-admissible `(3,1)` orbit, and does not classify
active-support-five or active-support-six equality pairs.  Unrestricted
permanent nonrestriction remains unknown, and the global Krenn--Gu
conjecture remains **UNRESOLVED**.

## 1. The `(4,1)` star pair and its five sensors

Let `K` be a field of characteristic zero and

```text
Z_6=K[x_0,...,x_5]/(x_0^2,...,x_5^2).                       (2)
```

At modes `0,1`, fix the colour bases

```text
u_0=-x_0+x_2,      u_1=x_0-x_3,       u_2=x_1-x_2,
v_0=x_0+x_1-x_2+x_3,
v_1=x_0+x_1,       v_2=-x_1+x_2.                            (3)
```

In edge order `(01,02,03,12,13,23)`, the mixed plane and diagonal products
are

```text
m_1=(-1, 1, 0,1, 0,0),       m_2=( 1,-1, 0,0,-1,1),
d_0=(-1, 2,-1,1, 0,1),       d_1=( 1, 0,-1,0,-1,0),
d_2=( 0, 0, 0,2, 0,0).                                  (4)
```

They span a five-space

```text
B=M direct-sum span{d_0,d_1,d_2},       M=span{m_1,m_2}. (5)
```

Put

```text
ell_1=x_0+x_1-x_2,                    ell_2=x_1-x_2,
z_0=x_0-x_3,

Phi_1=(x_3,x_4,x_5,ell_1),            Phi_2=(z_0,x_4,x_5,ell_2).
                                                                  (6)
```

Edge complementation gives

```text
star(m_1)=x_4x_5 x_3 ell_1,
star(m_2)=x_4x_5 z_0 ell_2,

star(d_0)=x_4x_5(
  x_0x_1+x_0x_3-x_1x_2+2x_1x_3-x_2x_3),
star(d_1)=-x_4x_5 x_2(x_0+x_1-x_3),
star(d_2)= 2x_4x_5 x_0x_3.                               (7)
```

Let four independent local triples span planes `L_2,...,L_5 subset K^6`.
For a pair product `q`, let `T_q` be the pullback of `star(q)` to the four
local colour spaces.  An exact extension to `Delta_3` means

```text
T_(m_1)=T_(m_2)=0,
T_(d_c)=lambda_c e_c^* tensor e_c^* tensor e_c^* tensor e_c^*,
lambda_c!=0,                         c=0,1,2.              (8)
```

## 2. Exact common-missing-factor ranks

For

```text
phi in {x_3,x_4,x_5,ell_1},
psi in {z_0,x_4,x_5,ell_2},                              (9)
```

put

```text
K_(phi,psi)=ker(phi) intersect ker(psi),
C_(phi,psi)=span{y_2y_3y_4y_5:y_t in K_(phi,psi)}.       (10)
```

Pairing elements of `C_(phi,psi)` against `B` gives the exact rank table

```text
                       psi
                 z_0   x_4   x_5   ell_2
phi  x_3          1     0     0      2
     x_4          0     0     0      0
     x_5          0     0     0      0
     ell_1        3     0     0      1.                  (11)
```

Every cell except `(ell_1,z_0)` has rank at most two and is incompatible
with the three independent pure functionals in (8).  The rank-three cell
will be excluded in Section 7 by a tensor-rank invariant.

## 3. Full rank in one mixed projection

Assume first that

```text
rank(Phi_1|L_t)=3 for every t.                            (12)
```

The zero tensor `T_(m_1)` and the hyperplane-product theorem force all four
`Phi_1(L_t)` to have one common missing coordinate.  Missing `x_4` or `x_5`
kills every pure tensor in (7), while missing `x_3` kills `star(d_2)`.
Therefore

```text
L_t subset ker(ell_1)                    for every t.     (13)
```

Inside `ker(ell_1)`, the kernel of `Phi_2` is the line

```text
K N,                         N=x_1+x_2.                   (14)
```

Thus every `Phi_2|L_t` has rank two or three, with rank two exactly when
`N in L_t`.

If instead all four `Phi_2` ranks are three, their common missing coordinate
cannot be `x_4` or `x_5`.  It is therefore either `z_0` or `ell_2`.  In both
cases the kernel of `Phi_1` restricted to that common hyperplane is again
the line `K N`.  Consequently the rank-profile argument below applies in
both directions; only the names of the two projections are exchanged.

Call a rank-two mode in the secondary projection family **low**.

## 4. Zero, one, three, or four low modes

If there are no low modes, the secondary mixed zero tensor forces a common
missing coordinate there as well.  If there is exactly one low mode, group
two of the three hyperplane images against the remaining hyperplane and the
plane.  The hyperplane-hyperplane and hyperplane-plane product dimensions
are at least three.  Orthogonality forces equality; the first product is a
coordinate `W_i^2`, and the second product lying in its orthogonal
`W_i^2` forces both factors into `W_i`.  Thus zero or one low mode always
gives a common cell from (11).

For a low mode `t`, expand

```text
N=alpha_(t,0)y_(t,0)+alpha_(t,1)y_(t,1)
  +alpha_(t,2)y_(t,2).                                  (15)
```

Single contraction of `star(d_2)` with `N` is zero, so (8) implies

```text
alpha_(t,2)=0.                                          (16)
```

For two low modes `s,t`, the exact double contractions are

```text
i_N i_N star(m_1)=i_N i_N star(m_2)=i_N i_N star(d_2)=0,

i_N i_N star(d_0)=i_N i_N star(d_1)=-2J,                (17)

J(y,z)=x_4(y)x_5(z)+x_5(y)x_4(z).                       (18)
```

The two equal ambient bilinear tensors in (17) have target supports at the
distinct entries `(0,0)` and `(1,1)`.  Hence

```text
alpha_(s,0)alpha_(t,0)=0,
alpha_(s,1)alpha_(t,1)=0.                               (19)
```

Every nonzero coefficient vector in (15)--(16) is therefore supported at
one of the two labels `0,1`, and any two low modes use different labels.
Three or four low modes are impossible.

## 5. Exactly two low modes

With two rank-three hyperplane images and two rank-two plane images, the
sharp hyperplane-plane product classification gives exactly two branches.

```text
I.  all four images lie in one coordinate hyperplane W_i;

II. in factor coordinates z_0,z_1,z_2,z_3,

    P_2=P_3=P=span{z_k,z_l},
    H_+=P direct-sum K(z_i+t z_j),
    H_-=P direct-sum K(z_i-t z_j),       t!=0.            (20)
```

Branch I is another common cell from (11).  In branch II, equations
(15)--(19) allow the normalization

```text
N=y_(s,0),                         N=y_(t,1)              (21)
```

in the two low modes.

Contract the whole `B^*`-valued target tensor in those slots.  Every target
coordinate is zero because the two selected colours are different.  By
(17), the `d_0,d_1` ambient coordinates are both `-2J`, so

```text
J(H_+,H_-)=0.                                            (22)
```

In either projection's factor coordinates, the radical of `J` is the plane
spanned by the two factors other than `x_4,x_5`.  Two mutually
`J`-orthogonal hyperplanes must both contain that radical.  Their
intersection in (20) is `P`, so `P` equals the radical.  The original low
planes therefore have `x_4=x_5=0`.  The high modes would have to supply the
two common factors `x_4,x_5`, but their pairing is `J=0`.  Every pure sensor
vanishes, contradicting (8).  Branch II is impossible.

It remains only to exclude the dangerous common cell in (11).

## 6. Exact form of the dangerous cell

Put

```text
K=ker(ell_1) intersect ker(z_0).                          (23)
```

Its first-four-coordinate part has basis

```text
r_0=x_0+x_2+x_3,                  r_1=x_1+x_2.           (24)
```

Thus a vector in `K` is uniquely

```text
y=s r_0+t r_1+a x_4+b x_5.                              (25)
```

For

```text
q=c_0d_0+c_1d_1+c_2d_2,                                 (26)
```

the residual first-four-coordinate quadratic in `star(q)|K` is

```text
2c_2 s^2+(c_0-c_1)st-(c_0+c_1)t^2.                     (27)
```

This identifies the diagonal sensor with the full three-space
`Sym^2(span{s,t})^*`, explaining the rank-three entry in (11).

Choose the exact rational coefficients

```text
(c_0,c_1,c_2)=(1,2,-1/24).                              (28)
```

Every coefficient is nonzero, and (27) becomes

```text
-(1/12)(s+6t)^2.                                        (29)
```

Put `r=s+6t`.  The scalar target tensor for (28) is

```text
lambda_0 e_0^* tensor 4
+2lambda_1 e_1^* tensor 4
-(lambda_2/24)e_2^* tensor 4,                            (30)
```

with all three weights nonzero.  It has tensor rank exactly three.

## 7. The repeated-factor tensor has rank greater than three

Let `E` be the three-space with coordinates `(r,x_4,x_5)`, and let

```text
P=pol(r^2x_4x_5) in (E^*) tensor 4.                      (31)
```

For each local plane in the dangerous cell, the scalar tensor (30) is the
pullback of a nonzero scalar multiple of `P` under the evaluation map

```text
L_t -> E,                  y |-> (r(y),x_4(y),x_5(y)).   (32)
```

The mode flattenings of (30) have rank three.  Hence all four maps (32)
have rank three and are isomorphisms.  If (30) existed, `P` would therefore
be `GL_3^4`-equivalent to a weighted `Delta_3` tensor and would have tensor
rank three.

But `P` is concise: its first-mode slice space is

```text
S=span{sym(r x_4 x_5), sym(r^2x_5), sym(r^2x_4)},        (33)
```

a three-space of symmetric three-tensors.  It contains no nonzero rank-one
tensor.  Indeed, a rank-one three-tensor which is symmetric must be a
nonzero scalar multiple of a cube

```text
(alpha r+beta x_4+gamma x_5)^3.                          (34)
```

Membership in (33) makes the coefficients of `r^3,x_4^3,x_5^3` all zero.
Since the scalar is nonzero, this forces `alpha=beta=gamma=0` over a field,
so the rank-one tensor is zero after all.

If a concise four-tensor had tensor rank at most three, a three-term rank-one
decomposition would make its three first-mode factors independent; the
corresponding three nonzero rank-one three-tensors would lie in its slice
space.  Equation (33) forbids this.  Therefore

```text
tensor-rank(P)>3,                                        (35)
```

contradicting (30).  The dangerous common cell is excluded.

## 8. Two-sided conclusion and scope

Sections 3--7 apply whether `Phi_1` or `Phi_2` is assumed to have four full
ranks.  The possible common missing coordinates and all cells are already
covered by (11), and both restricted kernels are the same vector `N`.
This proves (1).

The exact boundary is

```text
star (4,1) pair, exact Delta_3 extension:
  a rank-drop mode in the Phi_1 family:                 PROVED;
  a rank-drop mode in the Phi_2 family:                 PROVED;

dangerous rank-three common cell:                       EXCLUDED;
simultaneous rank-drop residual:                        OPEN;
Delta-admissible (3,1) orbit:                           NOT TREATED;
active-support-five/six equality pairs:                 OPEN;
unrestricted P_6 -> Delta_3:                            UNKNOWN;
global Krenn--Gu conjecture:                            UNRESOLVED.      (36)
```

Replay the exact checks with

```powershell
python claims/arbitrary-order/verify_arbitrary_permanent_star_pair_two_sided_projection_drop.py
python claims/arbitrary-order/audit_arbitrary_permanent_star_pair_two_sided_projection_drop.py
python -m py_compile claims/arbitrary-order/verify_arbitrary_permanent_star_pair_two_sided_projection_drop.py claims/arbitrary-order/audit_arbitrary_permanent_star_pair_two_sided_projection_drop.py
python -m ruff check claims/arbitrary-order/verify_arbitrary_permanent_star_pair_two_sided_projection_drop.py claims/arbitrary-order/audit_arbitrary_permanent_star_pair_two_sided_projection_drop.py
```

The primary verifier checks the pair table, all five complemented quartics,
both restricted kernels, the complete 16-cell rank table, the common-kernel
contractions, the exact square (29), and the slice-space obstruction.  The
independent no-import audit uses separate modular square-free arithmetic,
replays every missing-factor rank, and exhausts the relevant product-space
and slice-space patterns over finite fields.  The finite audits check exact
identities and conventions; the written characteristic-zero arguments prove
the theorem.
