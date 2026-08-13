# Balanced `m=3` joint-rank-five Hilbert--Burch repeated-coordinate exclusion

## Status

**Exact characteristic-zero exclusion of the repeated-coordinate `(1,1,1)`
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

Suppose two triangle factors use the same target-coordinate line.  S2AN and
S2AO reduce the complete residual, after permuting roots and colours, to

```text
x=lambda e_s,       y=mu e_s,       z=nu e_t,
lambda mu nu!=0,                         s!=t.         (3)
```

The new conclusion is:

> No point satisfying (1)--(3) is target-consistent.

The proof first applies the S2R torus-annihilator theorem to the exact
seven-dimensional annihilator of `ker D_B`.  Its four-dimensional relation
space must lie in one coordinate hyperplane.  Equivalently, one of seven
distinguished rows is a coloop, so the other six lie in a two-plane.  Every
coloop orientation is then impossible.  Three orientations reduce to the
proved S2AL two-plane square obstruction.  Two orientations make the
required `T_t` coefficient identically zero.  The last two orientations
force two quadratic annihilators of one row plane to have a mixed image
fully transverse to its nonzero target image; an exact binary-cubic
restriction lemma forbids this.

Together with S2AN--S2AO this closes the entire **repeated-coordinate** part
of the `(1,1,1)` profile.  It does not exclude coordinate-distinct or other
allowed `(1,1,1)` charts, the `(1,1,2)` or `(1,2,2)` profiles, joint rank at
most four, other physical components or pole strata, higher orders, or the
global conjecture.  Global Krenn--Gu remains **UNRESOLVED**.

## 1. The discrete Hilbert--Burch grid

Let `u` be the third target colour, different from `s,t`.  The derivative is

```text
D_B(a,b,c)
 =-mu nu a tensor e_s tensor e_t
  -lambda nu e_s tensor b tensor e_t
  +lambda mu e_s tensor e_s tensor c.                (4)
```

Write the transposed root rows as

```text
r_i=rho(e_i^*),       p_j=pi(e_j^*),
q_k=theta(e_k^*),     T_k=X_k tensor Y_k tensor Z_k. (5)
```

Every coefficient of (4) with first two root colours in `{t,u}` is zero.
The complete target equation therefore gives

```text
per(r_i,p_j,q_k)=delta_(i,j,k) T_k,
i,j in {t,u},                    k in {t,u,s}.        (6)
```

There are four further untouched binary rectangles:

```text
per(r_s,p_j,q_k)=0,       j in {t,u}, k in {u,s},
per(r_i,p_s,q_k)=0,       i in {t,u}, k in {u,s}.    (7)
```

The same-colour row `q_s` is nonzero by the S2AO target gate: otherwise
`e_s^*` would annihilate `K`, while (4) and `z_s=0` would make both the
all-cross term and every singleton correction miss the required
`(s,s,s)` coefficient.  Equations (6) then show that

```text
R=span(r_t,r_u),       P=span(p_t,p_u),
Q=span(q_u,q_s)                                      (8)
```

are two-planes.

The annihilator of the derivative kernel is

```text
L=(ker D_B)^perp
 ={(alpha,beta,gamma):
     lambda alpha_s+nu gamma_t=0,
     mu beta_s+nu gamma_t=0},        dim L=7.        (9)
```

Since `ker D_B subset K` and `dim K=5`,

```text
N=K^perp subset L,       dim N=4,
V=H^T(L),                dim V=3.                    (10)
```

Put

```text
A=(nu/lambda) r_s,       B=(nu/mu) p_s,
h=A+B-q_t.                                             (11)
```

The seven rows

```text
r_t,r_u,p_t,p_u,q_u,q_s,h                            (12)
```

lie in `V` and are the images of a basis of `L`.  The cosets of `A,B` form
a basis of `image H^T/V`: indeed `ker H^T=N subset L`, so `H^T` induces an
isomorphism from the two-dimensional quotient of the full root-covector
space by `L` onto `image H^T/V`.  In particular,

```text
q_t=A+B-h.                                            (13)
```

In particular `q_t` is outside `V`, so `q_t,q_u` are independent.

## 2. Torus avoidance forces a coloop

For a root product functional `alpha tensor beta tensor gamma`, transpose
of (4) is

```text
D_B^T(alpha tensor beta tensor gamma)
 =(-mu nu beta_s gamma_t alpha,
   -lambda nu alpha_s gamma_t beta,
    lambda mu alpha_s beta_s gamma).                 (14)
```

This vector belongs to `L`.  Conversely, let
`ell=(alpha,beta,gamma) in L` have every one of its seven coordinates in
the basis underlying (12) nonzero.  Then all nine displayed root
coordinates of `alpha,beta,gamma` are nonzero, and (9) gives

```text
D_B^T(alpha tensor beta tensor gamma)
   =nu^2 gamma_t^2 ell.                              (15)
```

Here (15) uses the components of `ell` themselves as the three factors;
the two equations in (9) make all three scalar multipliers agree.

If such an `ell` belonged to `N=K^perp`, the fully supported product in
(15) would annihilate `D_B(K)=U`, contrary to S2R.  Hence the four-plane
`N` contains no point with all seven coordinates nonzero.  Over an infinite
characteristic-zero field, a linear space cannot be covered by finitely many
proper linear hyperplanes.  Therefore

```text
N is contained in one of the seven coordinate hyperplanes. (16)
```

Let `Phi:K^7 -> V` send the standard basis to (12).  It is onto and has
kernel `N`.  If, for example, `N subset {c_j=0}`, then restriction of `Phi`
to the other six coordinates has a four-dimensional kernel, hence rank two.
Thus (16) is equivalent to:

> One row in (12) is a coloop, and the other six span a two-plane. (17)

There are only the following incidence types, up to exchange of roots one
and two:

```text
coloop h, q_u, or q_s:       R=P;
coloop r_t or r_u:           P=Q;
coloop p_t or p_u:           R=Q.                    (18)
```

The equalities in (18) follow because the two displayed row pairs are
already two-planes and both lie in the two-plane spanned by the six
noncoloop rows.

## 3. Equal first and second row planes are impossible

Suppose `R=P`.  Write

```text
p_j=sum_i M_(j,i) r_i,              M in GL_2,       (19)
```

in the ordered colours `(t,u)`.  For fixed `q`, if `F` is the permanent
matrix in the `r,p` bases and `S` the corresponding matrix in the repeated
`r,r` basis, then

```text
F=S M^T,                 M F=M S M^T is symmetric.  (20)
```

At `q_t` and `q_u`, equation (6) gives respectively nonzero multiples of
`T_t E_tt` and `T_u E_uu`.  Symmetry in (20) forces both off-diagonal entries
of `M` to vanish.  Hence `p_t` is proportional to `r_t` and `p_u` to
`r_u`.  On the two-plane

```text
Q_0=span(q_t,q_u)                                      (21)
```

equation (6) becomes

```text
per(r_t,r_u,Q_0)=0,

per(r_t,r_t)|Q_0 and per(r_u,r_u)|Q_0 are nonzero
rank-one maps onto the fully transverse T_t,T_u.      (22)
```

The exact S2AL two-plane square lemma forbids (22).  This excludes the
coloops `h,q_u,q_s`.

## 4. Equal second and third row planes

It remains, up to the first/second-root symmetry, that `P=Q=S`.

### 4.1 The coloop `r_u`

If `r_u` is the coloop, then `r_t,h in S`.  Equations (6)--(7) give

```text
per(A,S,S)=0,       per(r_t,S,S)=0,
per(B,r_t,S)=0.                                      (23)
```

Using (13), the required target coefficient is therefore

```text
per(r_t,p_t,q_t)
 =per(r_t,p_t,A+B-h)=0,                              (24)
```

contrary to (6), which makes it `T_t!=0`.

### 4.2 A quadratic-annihilator lemma

We isolate the remaining exact obstruction.

**Lemma 1 (transverse mixed image of two quadratic annihilators).**  Let
`S subset X direct-sum Y direct-sum Z` be a two-plane over a
characteristic-zero field.  There do not exist `0!=v in S` and `a,b` such
that

```text
per(v,S,S) is nonzero with image in span(T_1),
per(a,S,S)=per(b,S,S)=0,
per(a,b,S) is nonzero with image in span(T_0),        (25)
```

where the decomposable tensors `T_0,T_1` are fully transverse.

**Proof.**  Choose source bases with
`T_i=X_i tensor Y_i tensor Z_i`.  Let `xi_i,eta_j,zeta_k` be the source
coordinate forms restricted to `S`.  The `(i,j,k)` coefficient of
`per(v,S,S)` is the directional derivative along `v` of the binary cubic

```text
xi_i eta_j zeta_k in S^3 S^*.                        (26)
```

Let `m` span the annihilator of `v` in `S^*`.  A binary cubic whose
directional derivative along `v` vanishes is a scalar multiple of `m^3`.
Since the `(1,1,1)` derivative in (25) is nonzero, the three forms
`xi_1,eta_1,zeta_1` are nonzero.  If, say, one off-`1` form in the first
source and one off-`1` form in the second source were both nonzero, the
zero derivatives of

```text
xi_i eta_1 zeta_1,        xi_1 eta_j zeta_1          (27)
```

and unique factorization would make all three of
`xi_1,eta_1,zeta_1` proportional to `m`.  Their `(1,1,1)` derivative would
then vanish.  Thus at most one source has any off-`1` restriction on `S`.

After permuting sources, every vector of `S` consequently has the form

```text
s=(x(s), y(s)Y_1, z(s)Z_1),                          (28)
```

where `x,y,z` are nonzero linear maps/forms.  If
`w=(w_X,w_Y,w_Z)` satisfies `per(w,S,S)=0`, project that identity to
`X tensor (Y/span(Y_1)) tensor span(Z_1)`.  It gives

```text
(x(s)z(t)+x(t)z(s)) tensor bar(w_Y)=0.               (29)
```

If `bar(w_Y)` were nonzero, setting `s=t` and using the integral-domain
property of `S^*` would force `x=0`, contrary to the nonzero target
coefficient.  Thus `w_Y` lies on `Y_1`.  The symmetric projection shows
that `w_Z` lies on `Z_1`.

Apply this to both `a,b`.  Every tensor in `per(a,b,S)` then lies in

```text
X tensor span(Y_1) tensor span(Z_1),                 (30)
```

so a nonzero decomposable image shares two source factor lines with `T_1`.
It cannot be the fully transverse `T_0`.  QED.

### 4.3 The coloop `r_t`

If `r_t` is the coloop, then `r_u,h in S`.  Equations (6)--(7) give

```text
per(A,S,S)=0,              per(r_t,S,S)=0,
per(B,r_t,S)=0.                                      (31)
```

The `q_t` row and (13) therefore give the nonzero rank-one map

```text
per(A,r_t,-)|S=span(T_t),                            (32)
```

The value in (32) is `T_t` at `p_t` and zero at `p_u`.  The `r_u` row of
(6) gives

```text
0!=per(r_u,S,S) subset span(T_u).                    (33)
```

Lemma 1, with `(a,b,v)=(A,r_t,r_u)`, contradicts the full transversality of
`T_t,T_u`.  This excludes `r_t`.  Exchanging the first two roots excludes
the two remaining coloops `p_t,p_u`.

## 5. Repeated-coordinate exclusion

Sections 3--4 exclude all seven alternatives in (17), contradicting the
coloop forced by S2R.  Therefore the discrete pattern (3) is impossible.
Together with S2AN--S2AO,

```text
Hilbert--Burch (1,1,1):
  any two factors on the same target-coordinate line: IMPOSSIBLE;
  coordinate-distinct / other allowed charts:          OPEN;

Hilbert--Burch (1,1,2), (1,2,2):                      OPEN;
joint rank at most four / other physical branches:     OPEN;
global Krenn--Gu conjecture:                           UNRESOLVED.     (34)
```

No finite scan, generic-point promotion, or numerical argument enters the
proof.

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_repeated_coordinate_exclusion.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_repeated_coordinate_exclusion.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_repeated_coordinate_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_repeated_coordinate_exclusion.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_repeated_coordinate_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_repeated_coordinate_exclusion.py
```

The primary replay checks the scalar-general Hilbert--Burch derivative,
kernel annihilator, torus self-recovery, untouched grid, coloop rank split,
equal-plane orientations, binary-cubic derivative kernel, and both
quadratic-annihilator quotient projections.  The independent audit imports
no repository or third-party module and reconstructs the same identities
with `Fraction` arithmetic, a different row convention, and separate exact
elimination.  The finite-union, unique-factorization, and inherited S2AL
square arguments are the written proof above.

## Dependencies

- [Repeated-coordinate support localization](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_REPEATED_COORDINATE_SUPPORT_LOCALIZATION_THEOREM.md)
- [Singleton-span torus-annihilator obstruction](BALANCED_M3_SINGLETON_SPAN_TORUS_ANNIHILATOR_PERMANENT_RANK_OBSTRUCTION.md)
- [Support-one higher-row-rank exclusion and two-plane square lemma](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_SUPPORT_ONE_HIGHER_ROW_RANK_EXCLUSION_THEOREM.md)
