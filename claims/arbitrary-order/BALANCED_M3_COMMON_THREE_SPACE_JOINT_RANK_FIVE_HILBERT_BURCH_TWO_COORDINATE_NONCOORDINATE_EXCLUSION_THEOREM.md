# Balanced `m=3` joint-rank-five Hilbert--Burch two-coordinate/noncoordinate exclusion

## Status

**Exact characteristic-zero exclusion of the last `(1,1,1)`
Hilbert--Burch boundary of the normalized, target-consistent physical `m=3`
common-three-space full-sensor stratum.**  Let `U` be the total singleton
span, put `K=image H`, and assume

```text
dim U=3,                         rank H=5.             (1)
```

Use the S2AG Hilbert--Burch normal form

```text
ker D_B=span{(x,0,z),(0,y,z)},

B_23=-y tensor z,       B_13=-x tensor z,
B_12= x tensor y.                                      (2)
```

S2AG proves that at least two of `x,y,z` are target-coordinate vectors.
S2AN--S2AP exclude a repeated coordinate line, and S2AQ excludes three
distinct coordinate lines.  The only remaining chart can therefore be
normalized, after permuting roots and colours, as

```text
x=lambda e_0,          y=mu e_1,
z=z_0 e_0+z_1 e_1+z_2 e_2,

lambda mu!=0,          z is noncoordinate.            (3)
```

Here noncoordinate means that `z` is not proportional to any `e_i`, or
equivalently that it has at least two nonzero coordinates.  The conclusion
is:

> No target-consistent point satisfying (1)--(3) exists.

The derivative-kernel annihilator is seven-dimensional.  Its
four-dimensional relation space avoids an eight-hyperplane torus open set,
so it lies either in one of seven basis-coordinate hyperplanes or in the
extra hyperplane `gamma(z)=0`.  Each alternative makes two of three exact
row planes agree.  Equal first/second planes violate a new square-zero
mixed-factor lemma.  Equal second/third planes have two ordinary-coloop
orientations: one makes fully transverse target lines cancel, while the
other reduces pointwise to the proved S2AL tangent-line factor-sharing
lemma.  First/third equality is symmetric.

Together with S2AN--S2AQ, this closes the complete Hilbert--Burch `(1,1,1)`
profile at joint rank five.  The `(1,1,2)` and `(1,2,2)` profiles, joint rank
at most four, other physical components and pole strata, higher orders, and
the global conjecture remain open.  Global Krenn--Gu remains
**UNRESOLVED**.

## 1. The exact derivative and three row planes

The derivative is

```text
D_B(a,b,c)
 =-mu a tensor e_1 tensor z
  -lambda e_0 tensor b tensor z
  +lambda mu e_0 tensor e_1 tensor c.                (4)
```

Write the transposed root rows and pure target tensors as

```text
r_i=rho(e_i^*),       p_j=pi(e_j^*),
q_k=theta(e_k^*),     T_k=X_k tensor Y_k tensor Z_k. (5)
```

Let

```text
z^perp={gamma:gamma(z)=0},
q(gamma)=sum_k gamma_k q_k,

R=span(r_1,r_2),      P=span(p_0,p_2),
Q=q(z^perp).                                           (6)
```

Every coordinate restriction

```text
ell_i:z^perp -> K,                 ell_i(gamma)=gamma_i (7)
```

is nonzero.  Indeed, `ell_i` vanishes identically on `z^perp` exactly when
`z` is proportional to `e_i`.

All three spaces in (6) are two-planes.  The untouched coefficient
`(2,2,2)` detects `r_2` and `p_2`.  If `r_1` were proportional to `r_2`,
the zero coefficient `(1,2,2)` would force `r_1=0`; but `r_1=0` makes both
the all-cross term and (4) miss the required `(1,1,1)` target coefficient.
Thus `R` is a two-plane.  The coefficients `(2,2,2)`, `(2,0,2)`, and the
analogous `(0,0,0)` target gate prove the same statement for `P`.

For `gamma in z^perp`, the complete untouched rectangle gives

```text
per(r_i,p_j,q(gamma))
 =delta_(i,2) delta_(j,2) gamma_2 T_2,
                  i in {1,2}, j in {0,2}.            (8)
```

Since `ell_2` is nonzero, (8) detects one direction of `Q`.  A putative
nonzero `gamma in z^perp` with `gamma_2=0` and `q(gamma)=0` would also be
impossible: contraction of (4) by `gamma` vanishes because
`gamma(z)=0` and `gamma` annihilates every third component of `K`, while
the contracted target is the nonzero tensor

```text
gamma_0 T_0+gamma_1 T_1.                             (9)
```

Hence `q:z^perp->Q` is injective and `Q` is a two-plane.

Put

```text
A=lambda^(-1) r_0,                 B=mu^(-1) p_1.   (10)
```

Contracting (4) by any `gamma in z^perp` kills its first two summands;
the third summand only affects the root pair `(0,1)`.  The three exact
exterior faces are therefore

```text
per(A,p_j,q(gamma))
 =lambda^(-1) delta_(j,0) gamma_0 T_0,
                                      j in {0,2},

per(r_i,B,q(gamma))
 =mu^(-1) delta_(i,1) gamma_1 T_1,
                                      i in {1,2},

per(r_i,p_j,q(gamma))
 =delta_(i,2) delta_(j,2) gamma_2 T_2,
                         i in {1,2}, j in {0,2}.     (11)
```

The scalar functionals `ell_0,ell_1,ell_2` in these faces are all nonzero.

## 2. Torus avoidance gives an eight-hyperplane fork

The annihilator of the derivative kernel is

```text
L=(ker D_B)^perp
 ={(alpha,beta,gamma):
     lambda alpha_0+gamma(z)=0,
     mu beta_1+gamma(z)=0},          dim L=7.        (12)
```

Since `ker D_B subset K` and `dim K=5`,

```text
N=K^perp subset L,       dim N=4,
V=H^T(L),                dim V=3.                    (13)
```

Define

```text
h_k=q_k-z_k(A+B),                  k=0,1,2.          (14)
```

The seven rows

```text
r_1,r_2,p_0,p_2,h_0,h_1,h_2                         (15)
```

span `V` and are the images of the basis of `L` with free coordinates

```text
alpha_1,alpha_2,beta_0,beta_2,gamma_0,gamma_1,gamma_2.
```

For a product root functional, transpose of (4) gives

```text
D_B^T(alpha tensor beta tensor gamma)
 =(-mu beta_1 gamma(z) alpha,
   -lambda alpha_0 gamma(z) beta,
    lambda mu alpha_0 beta_1 gamma).                 (16)
```

For every `ell=(alpha,beta,gamma) in L`, equations (12) turn (16) into

```text
D_B^T(alpha tensor beta tensor gamma)=gamma(z)^2 ell. (17)
```

Suppose `ell in N` avoided all eight hyperplanes

```text
alpha_1=0, alpha_2=0, beta_0=0, beta_2=0,
gamma_0=0, gamma_1=0, gamma_2=0, gamma(z)=0.         (18)
```

Then `alpha,beta,gamma` would have all nine target-coordinate evaluations
nonzero.  Equation (17) would put their nonzero product functional in
`U^perp`, contrary to the S2R fully supported product-annihilator theorem.
Thus `N` is covered by the eight proper hyperplanes in (18).  A linear
space over an infinite characteristic-zero field cannot be a finite union
of proper linear subspaces, so

```text
N is contained in one hyperplane of (18).            (19)
```

If the selected hyperplane is one of the first seven basis-coordinate
hyperplanes, deletion of its corresponding row in (15) leaves a two-plane:
the six-dimensional coordinate hyperplane contains the four-dimensional
kernel `N`, so its image has dimension two.  Consequently

```text
alpha_i=0:       P=Q,                i in {1,2},
beta_j=0:        R=Q,                j in {0,2},
gamma_k=0:       R=P,                k in {0,1,2}.   (20)
```

For example, in the first line all `p` and `h` rows lie in the two-plane,
and for `gamma in z^perp`, (14) gives
`q(gamma)=sum gamma_k h_k`, so `Q` lies there as well.

If instead `N subset {gamma(z)=0}`, the six-plane
`L intersect {gamma(z)=0}` maps to a two-plane.  It contains the preimages
of `R`, `P`, and `Q`, so

```text
R=P=Q.                                               (21)
```

It remains to exclude the three equality types.

## 3. Equal first and second row planes

We first record the exact obstruction needed here.

### Lemma 1 (square-zero mixed-factor sharing)

Let `W=X direct-sum Y direct-sum Z`, let `Q subset W` be a two-plane, and
let `0!=v in W` satisfy

```text
per(v,v,Q)=0.                                        (22)
```

If `per(a,v,-)|Q` and `per(b,v,-)|Q` are nonzero rank-one maps with
decomposable image tensors `T_a,T_b`, then `T_a,T_b` share at least one
source factor line.

### Proof

Write `v=x+y+z` by source components.

If `v` is pure, every nonzero mixed value has its factor in that source on
the fixed line supplied by `v`, so the conclusion is immediate.

Suppose exactly two components are nonzero, say `v=x+y`.  Its square is

```text
per(v,v,q)=2 x tensor y tensor q_Z.                  (23)
```

Thus (22) gives `Q_Z=0`, and

```text
per(a,v,q)
 =a_Z tensor (x tensor q_Y+q_X tensor y).            (24)
```

The parenthesized map is independent of `a`.  If (24) has a nonzero
one-dimensional decomposable image, that common map fixes its `X` and `Y`
factor lines.  The images obtained from `a` and `b` therefore share both
of those lines.

Finally suppose all three components are nonzero.  The square kernel is
exactly

```text
K_v={(c_x x,c_y y,c_z z):c_x+c_y+c_z=0}.            (25)
```

It is a two-plane, so (22) gives `Q=K_v`.  For a vector in (25), direct
expansion gives, up to an overall sign,

```text
c_x a_X tensor y tensor z
 +c_y x tensor a_Y tensor z
 +c_z x tensor y tensor a_Z.                         (26)
```

Thus every mixed value belongs to the Segre tangent space at
`x tensor y tensor z`.  Every nonzero decomposable tensor in this tangent
space shares at least two of the three base factor lines.  Two such tensors
therefore share at least one factor line.  This proves the lemma.  QED.

Now suppose

```text
R=P=S.                                               (27)
```

For any `gamma` with `gamma_2!=0`, the third face in (11) is a symmetric
rank-one bilinear form on `S`.  Its left radical in the `R` basis is
`span(r_1)`, and its right radical in the `P` basis is `span(p_0)`.
Symmetry forces those radical lines to agree.  Choose

```text
0!=v in span(r_1)=span(p_0).                         (28)
```

Equation (11) gives

```text
per(v,v,Q)=0,

per(A,v,-)|Q has nonzero rank-one image span(T_0),
per(B,v,-)|Q has nonzero rank-one image span(T_1).   (29)
```

The last two maps are nonzero because `ell_0` and `ell_1` are nonzero.
Lemma 1 says `T_0,T_1` share a source factor, contrary to their full
transversality.  Hence `R=P` is impossible.  This also excludes (21) and
all three `gamma_k` alternatives in (20).

## 4. Equal second and third row planes

Suppose

```text
P=Q=S.                                               (30)
```

Symmetry and the three faces in (11) give nonzero rank-one symmetric
bilinear forms on `S` such that

```text
per(A,S,S) has image span(T_0),
per(r_2,S,S) has image span(T_2),
per(r_1,S,S)=0,

per(B,r_1,S) has nonzero rank-one image span(T_1),
per(B,r_2,S)=0.                                      (31)
```

The radical of the first square is `span(p_2)`, and the radical of the
second is `span(p_0)`.  There are two coloop orientations.

### 4.1 The coloop `r_2`

If `N subset {alpha_2=0}`, then `r_2` is the coloop and

```text
r_1,h_0,h_1,h_2 in S.                               (32)
```

The raw untouched table is

```text
per(r_1,p_j,q_k)=0,                 j in {0,2}.      (33)
```

Substitute `q_k=h_k+z_k(A+B)` from (14).  The `h_k` term vanishes by
`per(r_1,S,S)=0`.  For any `k` with `z_k!=0`, equation (33) yields on the
basis `(p_0,p_2)` of `S`

```text
per(A,r_1,-)|S=-per(B,r_1,-)|S.                     (34)
```

The left side has image contained in `span(T_0)` by the first square in
(31), whereas the right side is a nonzero map with image `span(T_1)`.
The independent target lines cannot cancel.  This excludes `r_2`.

### 4.2 The coloop `r_1`

If `N subset {alpha_1=0}`, then `r_1` is the coloop and

```text
r_2,h_0,h_1,h_2 in S.                               (35)
```

The raw `r_1` table is still (33).  Again substitute (14); now its `h_k`
term vanishes because `per(r_1,S,S)=0`.  For a nonzero coordinate `z_k`,

```text
per(A,r_1,-)|S=-per(B,r_1,-)|S.                     (36)
```

Thus `per(A,r_1,-)|S` is a nonzero rank-one map with image `span(T_1)`.
The first line of (31) is a nonzero rank-one symmetric form with image
`span(T_0)`.  Choose `s in S` outside the radical of that square and the
kernel of the mixed map in (36).  Such an `s` exists because the field is
infinite.  Then, on the one-space `span(A)`,

```text
per(s,s,-) has nonzero image span(T_0),
per(s,r_1,-) has nonzero image span(T_1).            (37)
```

Part 2 of the exact S2AL tangent-line separation and mixed-factor-sharing
lemma says that the two decomposable images in (37) share a source factor
line.  This contradicts the full transversality of `T_0,T_1` and excludes
`r_1`.

Therefore `P=Q` is impossible.  Exchanging the first two root and source
blocks and simultaneously exchanging target colours `0,1` preserves (3),
up to replacing `z_0,z_1` by each other.  It swaps `P=Q` with `R=Q` and
`A,T_0` with `B,T_1`.  Hence `R=Q` is impossible as well.

All alternatives in (19)--(21) are now excluded.

## 5. Proof-topology consequence

S2AG proves that every `(1,1,1)` Hilbert--Burch point has at least two
coordinate triangle factors.  The complete profile is now

```text
two coordinate factors on the same line:             IMPOSSIBLE
  by S2AN--S2AP;

three pairwise-distinct coordinate factors:           IMPOSSIBLE
  by S2AQ;

two distinct coordinate factors and a genuinely
  noncoordinate third factor:                         IMPOSSIBLE
  by this theorem;

Hilbert--Burch (1,1,1):                               IMPOSSIBLE;

Hilbert--Burch (1,1,2), (1,2,2):                     OPEN;
joint rank at most four / other physical branches:    OPEN;
global Krenn--Gu conjecture:                          UNRESOLVED.     (38)
```

No finite scan, generic-point promotion, numerical inference, or unproved
case cover enters the argument.

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_two_coordinate_noncoordinate_exclusion.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_two_coordinate_noncoordinate_exclusion.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_two_coordinate_noncoordinate_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_two_coordinate_noncoordinate_exclusion.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_two_coordinate_noncoordinate_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_two_coordinate_noncoordinate_exclusion.py
```

The primary replay checks the scalar-general derivative, kernel,
annihilator, eight torus hyperplanes, contracted target faces, row-plane
rank, equality fork, square-zero mixed-factor atlas, and both ordinary
coloop equations.  The independent no-import audit uses rational arithmetic,
a different tensor indexing convention, a separate elimination routine,
direct permanent expansion, and independent hyperplane/equality models.
