# Balanced `m=3` joint-rank-five Hilbert--Burch `(1,1,2)` central-coordinate torus localization

## Status

**Exact characteristic-zero localization inside the central-coordinate
branch of the `(1,1,2)` Hilbert--Burch boundary of the normalized,
target-consistent physical `m=3` common-three-space full-sensor stratum.**
Let `U` be the total singleton span, put `K=image H`, and assume

```text
dim U=3,                         rank H=5.             (1)
```

Use the S2AG Hilbert--Burch normal form

```text
ker D_B=span{(x,0,z),(0,y,w)},
dim span(z,w)=2,

B_23=-y tensor z,       B_13=-x tensor w,
B_12= x tensor y.                                      (2)
```

Consider the central coordinate-pair chart from the S2AG atlas:

```text
x=lambda e_s,             y=mu e_t,
lambda mu!=0.                                          (3)
```

If `s!=t`, assume additionally

```text
w is not proportional to e_s,
z is not proportional to e_t.                         (4)
```

There is no extra assumption when `s=t`.  Let

```text
N=K^perp subset (ker D_B)^perp.                       (5)
```

Then `N` is contained in one of the four ordinary coordinate hyperplanes

```text
alpha_i=0 for some i!=s,
or
beta_j=0 for some j!=t.                               (6)
```

Equivalently, `K` contains a pure first-root coordinate vector outside
`span(x)`, or a pure second-root coordinate vector outside `span(y)`.

The proof starts from the exact self-recovery scalar
`gamma(z)gamma(w)`.  Torus avoidance gives nine hyperplane alternatives:
four ordinary root coordinates, three combined third-root rows, and
`gamma(z)=0` or `gamma(w)=0`.  Each of the last five makes the first and
second row planes equal.  When `s=t`, the untouched binary diagonal cube
contradicts the S2AL two-square lemma.  When `s!=t`, a new exact
source-support lemma uses the two exterior target faces and the remaining
`T_u` square to exclude equality under (4).

This theorem is a localization, not an exclusion of the `(1,1,2)` profile.
It leaves the four ordinary-coloop orientations in (6), the repeated outer
factor boundaries excluded by (4), the outer coordinate-pair charts
`(x,w)` and `(y,z)`, the `(1,2,2)` profile, joint rank at most four, other
physical branches, higher orders, and the global conjecture open.  Global
Krenn--Gu remains **UNRESOLVED**.

## 1. Derivative, annihilator, and untouched row planes

The derivative is

```text
D_B(a,b,c)
 =-mu a tensor e_t tensor z
  -lambda e_s tensor b tensor w
  +lambda mu e_s tensor e_t tensor c.                (7)
```

Write

```text
r_i=rho(e_i^*),       p_j=pi(e_j^*),
q_k=theta(e_k^*),     T_k=X_k tensor Y_k tensor Z_k. (8)
```

Put

```text
R=span(r_i:i!=s),            P=span(p_j:j!=t).       (9)
```

Both are two-planes.  If `s=t`, the two complementary diagonal target
coefficients are untouched and separate both pairs.  If `s!=t`, let `u` be
the third colour.  The untouched coefficient `(u,u,u)` detects `r_u` and
`p_u`.  The rows `r_t` and `p_s` cannot vanish: for example, `r_t=0` says
that every first component of `K` has zero `t` coordinate, so both the
all-cross term and the first summand of (7) miss the required `(t,t,t)`
coefficient.  The crossed untouched coefficient `(t,u,u)` separates
`r_t` from `r_u`; `(u,s,u)` gives the symmetric separation in `P`.

For every `i!=s`, `j!=t`, and every `k`, (7) has zero `(i,j,k)`
coefficient.  Hence the complete untouched table is

```text
per(r_i,p_j,q_k)=delta_(i,j,k) T_k,
                         i!=s, j!=t, 0<=k<=2.        (10)
```

The annihilator of the derivative kernel is

```text
L=(ker D_B)^perp
 ={(alpha,beta,gamma):
     lambda alpha_s+gamma(z)=0,
     mu beta_t+gamma(w)=0},          dim L=7.        (11)
```

Since `ker D_B subset K` and `dim K=5`,

```text
N=K^perp subset L,       dim N=4,
V=H^T(L),                dim V=3.                    (12)
```

Set

```text
A=lambda^(-1)r_s,                 B=mu^(-1)p_t,
h_k=q_k-z_k A-w_k B.                               (13)
```

The seven rows

```text
(r_i)_(i!=s), (p_j)_(j!=t), h_0,h_1,h_2             (14)
```

are the images of a basis of `L` and span `V`.

For a product root functional, transpose of (7) is

```text
D_B^T(alpha tensor beta tensor gamma)
 =(-mu beta_t gamma(z) alpha,
   -lambda alpha_s gamma(w) beta,
    lambda mu alpha_s beta_t gamma).                 (15)
```

Equations (11) give the exact self-recovery identity

```text
D_B^T(alpha tensor beta tensor gamma)
 =gamma(z)gamma(w)(alpha,beta,gamma)                 (16)
```

for every point of `L`.

## 2. Torus avoidance gives nine hyperplanes

The seven basis coordinates in (14) are

```text
alpha_i (i!=s),       beta_j (j!=t),
gamma_0,gamma_1,gamma_2.                             (17)
```

A point of `L` has all nine root-coordinate evaluations nonzero exactly
when the seven values in (17) and the two values

```text
gamma(z),                    gamma(w)                (18)
```

are nonzero.  If such a point belonged to `N`, (16) would give a fully
supported product functional annihilating `U=D_B(K)`, contrary to S2R.
Thus the four-plane `N` is covered by nine proper hyperplanes.  Over the
infinite characteristic-zero field it is contained in one of them.

If `N` lies in a hyperplane `gamma_k=0`, deletion of `h_k` from (14) leaves
a six-dimensional subspace with four-dimensional kernel and hence
two-dimensional image.  It contains both two-planes `R` and `P`, so

```text
R=P.                                                 (19)
```

If `N subset {gamma(z)=0}`, the six-plane
`L intersect {gamma(z)=0}` also has two-dimensional image and contains the
preimages of both `R` and `P`.  Thus (19) again holds.  The same argument
applies to `gamma(w)=0`.

It remains to prove that (19) is impossible under (3)--(4).  That will
eliminate five of the nine alternatives and leave exactly (6).

## 3. Equal row planes when the coordinate colours agree

Assume first `s=t`, and let `a,b` be the other two colours.  If
`R=P=S`, write the `P` basis in the `R` basis.  At `q_a` and `q_b`, (10)
gives the two permanent matrices

```text
T_a E_aa,                         T_b E_bb.           (20)
```

Permanent symmetry forces the change-of-basis matrix to be diagonal.
Therefore, after harmless rescaling,

```text
per(r_a,r_b,Q)=0,

per(r_a,r_a)|Q and per(r_b,r_b)|Q are nonzero
rank-one maps onto T_a,T_b,

Q=span(q_a,q_b).                                    (21)
```

The rows `q_a,q_b` are independent: evaluating a putative dependence at
`(r_a,p_a)` and `(r_b,p_b)` uses (20) and its crossed zeros.  Hence `Q` is a
two-plane.  The exact S2AL two-plane square lemma forbids (21), because
`T_a,T_b` are fully transverse.  Thus (19) is impossible when `s=t`.

## 4. A split-centre equal-plane obstruction

Assume now that `s,t,u` are distinct.  Contraction of (7) by a covector
`gamma in w^perp` kills the second summand, while `j!=t` kills the other two.
Similarly use `z^perp` on the second exterior face.  Equation (10) and the
complete target equation give

```text
per(A,p_j,q(gamma))
 =lambda^(-1) delta_(j,s) gamma_s T_s,
                                  j!=t, gamma(w)=0,

per(r_i,B,q(gamma))
 =mu^(-1) delta_(i,t) gamma_t T_t,
                                  i!=s, gamma(z)=0.  (22)
```

The two maps displayed in (22) are nonzero precisely because (4) says that
the restrictions of `gamma_s` to `w^perp` and of `gamma_t` to `z^perp` are
nonzero.

Suppose `R=P=S`.  At every `q(gamma)`, the matrix in (10) has only its
`(u,u)` entry.  Symmetry therefore aligns its left and right radical lines:

```text
span(r_t)=span(p_s).                                 (23)
```

Choose `0!=v` on this common line and choose `d in S` off it.  After
rescaling `d`, equations (10), (22), and (23) have the exact form

```text
per(v,v,q(gamma))=per(v,d,q(gamma))=0,
per(d,d,q(gamma))=gamma_u T_u,

per(A,v,q(gamma))=c_s gamma_s T_s,  gamma(w)=0,
per(B,v,q(gamma))=c_t gamma_t T_t,  gamma(z)=0,      (24)
```

with `c_s c_t!=0`.

We show that (24) is impossible by splitting `v` according to its source
support in `W=X direct-sum Y direct-sum Z`.

### One source

If `v` is pure in one source, every nonzero mixed permanent containing `v`
has the fixed factor line supplied by `v` in that source.  The two nonzero
maps in the last line of (24) would make `T_s,T_t` share that line,
contrary to full transversality.

### Three sources

Write `v=x+y+zeta` with all three components nonzero.  Its square kernel is
the two-plane

```text
K_v={(a x,b y,c zeta):a+b+c=0}.                     (25)
```

The first line of (24) puts `image theta` in `K_v`.  Since the third
projection of `K` contains the two-plane `span(z,w)`, `rank theta>=2`, and
therefore `image theta=K_v`.  Every mixed value
`per(C,v,q)` with `q in K_v` belongs to the Segre tangent space at
`x tensor y tensor zeta`.  A decomposable tensor in that tangent space
shares at least two base factor lines.  The nonzero `T_s,T_t` values in
(24) must therefore share at least one factor line, again impossible.

### Two sources

After permuting the tensor sources, write

```text
v=x+y,                         x y!=0.               (26)
```

The square identity in (24) forces every `q(gamma)` to lie in
`X direct-sum Y`.  Put

```text
L(q)=x tensor q_Y+q_X tensor y.                     (27)
```

Then

```text
per(C,v,q)=C_Z tensor L(q).                          (28)
```

Every nonzero decomposable value of `L` belongs to one of the two rulings
of the Segre tangent at `x tensor y`: it has fixed `X` factor `x` or fixed
`Y` factor `y`.  If the nonzero `T_s,T_t` values in (24) used the same
ruling, they would share that factor.  Full transversality therefore forces
them to use opposite rulings.

Let `0!=n in z^perp intersect w^perp`.  At `q(n)`, the last line of (24) is

```text
A_Z tensor L(q(n))=c_s n_s T_s,
B_Z tensor L(q(n))=c_t n_t T_t.                     (29)
```

The two fixed `Z` components in (29) are nonzero because the corresponding
maps in (24) are nonzero.  If `L(q(n))` were nonzero, (29) would either make
`T_s,T_t` share its two factor lines, or a zero scalar on one side would
force `L(q(n))=0`.  Consequently

```text
L(q(n))=0,                   n_s=n_t=0.              (30)
```

Thus `n` is proportional to `e_u^*`,
`span(z,w)=span(e_s,e_t)`, and the exact kernel of (27) gives

```text
q_u=c(x-y),                         c!=0.             (31)
```

The scalar is nonzero because the second line of (24) at `gamma=e_u^*`
is the nonzero target `T_u`.  Direct expansion gives

```text
per(d,d,q_u)
 =2c (x tensor d_Y-d_X tensor y) tensor d_Z.         (32)
```

The nonzero tensor (32) is decomposable.  The matrix in parentheses has
rank one only if `d_X` is proportional to `x` or `d_Y` is proportional to
`y`; otherwise its restriction to the two independent row and column lines
has rank two.  Hence `T_u` shares `x` with the target on the first tangent
ruling or shares `y` with the target on the second ruling.  Either
alternative contradicts the pairwise full transversality of
`T_s,T_t,T_u`.

The one-, two-, and three-source cases exhaust `v`, so (19) is impossible
also when `s!=t` under (4).

## 5. Residual ordinary coloops

The five hyperplanes

```text
gamma_0=0, gamma_1=0, gamma_2=0,
gamma(z)=0, gamma(w)=0                              (33)
```

all imply (19), now excluded.  Therefore the torus alternative lies among
the other four hyperplanes in (17), proving (6).

If, for example, `N subset {alpha_i=0}`, duality gives the primal inclusion

```text
(e_i,0,0) in K,                                     (34)
```

and deleting the corresponding row `r_i` from (14) leaves a two-plane.
The `beta_j` alternatives are symmetric.  These are exact ordinary-coloop
residuals; this theorem does not assert that they are realizable.

Together with S2AR, the immediate rank-five Hilbert--Burch frontier is

```text
(1,1,1):                                             IMPOSSIBLE;

(1,1,2), central coordinate pair away from (4)'s
  repeated outer lines:                              FOUR ORDINARY
                                                     COLOOPS ONLY;

(1,1,2), repeated outer lines / outer coordinate
  pairs:                                             OPEN;

(1,2,2):                                             OPEN;
joint rank at most four / other physical branches:   OPEN;
global Krenn--Gu conjecture:                          UNRESOLVED.     (35)
```

No finite scan, generic-point promotion, or numerical inference enters the
proof.

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_one_two_central_coordinate_torus_localization.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_one_two_central_coordinate_torus_localization.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_one_two_central_coordinate_torus_localization.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_one_two_central_coordinate_torus_localization.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_one_two_central_coordinate_torus_localization.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_one_two_central_coordinate_torus_localization.py
```

The primary replay checks the scalar-general derivative, kernel,
annihilator, self-recovery, nine-hyperplane rank fork, same-colour square
table, distinct-colour exterior faces, and the complete one-/two-/three-
source equal-plane atlas.  The independent no-import audit uses rational
arithmetic, a different tensor indexing convention, separate row reduction,
direct permanent expansion, and all same-/distinct-colour support models.
