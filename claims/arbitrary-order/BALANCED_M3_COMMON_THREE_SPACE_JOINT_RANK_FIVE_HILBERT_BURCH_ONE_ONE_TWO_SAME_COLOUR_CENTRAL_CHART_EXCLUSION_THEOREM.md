# Balanced `m=3` joint-rank-five Hilbert--Burch `(1,1,2)` same-colour central-chart exclusion

## Status

**Exact characteristic-zero exclusion of the same-colour central
coordinate-pair chart of the `(1,1,2)` Hilbert--Burch boundary.**  Retain the
normalized, target-consistent physical `m=3` common-three-space full-sensor
hypotheses

```text
dim U=3,                         rank H=5.             (1)
```

In the S2AG Hilbert--Burch normal form, suppose

```text
ker D_B=span{(lambda e_s,0,z),(0,mu e_s,w)},
lambda mu!=0,                    dim span(z,w)=2.     (2)
```

Then (2) is impossible.

S2AS already reduces this chart to four ordinary first-/second-root
coloops.  The proof below shows that all four are symmetric and excludes
one.  Its complete untouched binary diagonal table has two nonzero rank-one
target maps.  Writing the sole surviving first-row vector in the second-row
plane gives three cases.  In the generic case, the S2AL square/mixed tangent
lemma forces the two targets to share a factor.  At one endpoint, one
square-zero row would have to carry two fully transverse rank-one mixed
maps.  At the other, a rank-one square would have two independent mixed
radical rows.  New exact full-/two-/one-source lemmas exclude both endpoints.

Together with S2AW, this closes both central coordinate-pair charts of the
`(1,1,2)` profile.  It does not treat the genuinely outer coordinate-pair
charts `(x,w)` and `(y,z)`, other `(1,1,2)` boundaries, `(1,2,2)`, joint
rank at most four, another physical component, higher orders, or the global
conjecture.  Global Krenn--Gu remains **UNRESOLVED**.

## 1. Derivative, rows, and the three-dimensional third shore

The root--root blocks and derivative are

```text
B_23=-mu e_s tensor z,
B_13=-lambda e_s tensor w,
B_12= lambda mu e_s tensor e_s,

D_B(a,b,c)
 =-mu a tensor e_s tensor z
  -lambda e_s tensor b tensor w
  +lambda mu e_s tensor e_s tensor c.               (3)
```

Let `a,b` denote the two target colours other than `s`, and write

```text
r_i=rho(e_i^*),       p_j=pi(e_j^*),
q_k=theta(e_k^*),     T_k=X_k tensor Y_k tensor Z_k,

R=span(r_a,r_b),             P=span(p_a,p_b).       (4)
```

Both `R` and `P` are two-planes by S2AS.  Every coefficient whose first two
root colours avoid `s` is untouched by (3), so

```text
per(r_i,p_j,q(gamma))=delta_(i,j)gamma_i T_i,
                              i,j in {a,b}.         (5)
```

The annihilator of the derivative kernel is

```text
L={ (alpha,beta,gamma):
      lambda alpha_s+gamma(z)=0,
      mu beta_s+gamma(w)=0 },          dim L=7.     (6)
```

Put

```text
A=lambda^(-1)r_s,              B=mu^(-1)p_s,
h_k=q_k-z_k A-w_k B.                              (7)
```

The seven rows

```text
r_a,r_b,p_a,p_b,h_s,h_a,h_b                         (8)
```

span the three-plane `V=H^T(L)` and have four-dimensional relation kernel
`N=K^perp subset L`.  S2AS proves that `N` lies in one of

```text
alpha_a=0, alpha_b=0, beta_a=0, beta_b=0.           (9)
```

The third-row image

```text
Q=image theta                                           (10)
```

has dimension three.  Modulo `V`, (7) reads

```text
q(gamma) congruent gamma(z)A+gamma(w)B.              (11)
```

The classes of `A,B` form a basis of the two-dimensional quotient of the
full row image by `V`, and the independent forms `gamma(z),gamma(w)` give
quotient rank two.  Let `0!=n in z^perp intersect w^perp`.  Then
`q(n)=h(n) in V` is nonzero: otherwise third-root contraction by `n` kills
the all-cross term and every summand of `D_B(K)`, while the target
contraction `sum_i n_iT_i` is nonzero.  Thus

```text
dim Q=3.                                             (12)
```

For a basis `v_0,v_1,v_2` of `V`, physical full-sensor rank again gives the
nonzero alternating separated tensor

```text
Alt(v_0,v_1,v_2)
 =sum_(sigma in S_3) sign(sigma)
   (v_(sigma(1)))_X tensor
   (v_(sigma(2)))_Y tensor
   (v_(sigma(3)))_Z !=0.                            (13)
```

## 2. Two endpoint lemmas

For `u,v,q in W=X direct-sum Y direct-sum Z`, put

```text
M_(u,v)(q)=per(u,v,q).                               (14)
```

### Lemma 1 (one square-zero row cannot carry two transverse targets)

Let `dim Q=3` and suppose

```text
M_(v,v)(Q)=0.                                       (15)
```

If `M_(p,v)|Q` and `M_(w,v)|Q` are nonzero rank-one maps with
decomposable image tensors, those tensors cannot be fully transverse.

#### Proof

Split `v` by source support.

If `v` is pure, every nonzero mixed value containing it has the fixed
factor line supplied by `v`.

If `v=x+y+z` has all three components nonzero, its square kernel is the
two-plane

```text
{(c_X x,c_Y y,c_Z z):c_X+c_Y+c_Z=0},               (16)
```

which cannot contain the three-plane `Q`.

If `v=x+y` has exactly two components, (15) puts
`Q subset X direct-sum Y`.  For every `C in W`,

```text
M_(C,v)(q)=C_Z tensor L(q),
L(q)=x tensor q_Y+q_X tensor y.                     (17)
```

Either nonzero rank-one mixed map in the lemma would therefore require a
one-dimensional `L(Q)` image.  In fact the kernel of `L` is only
`span(x-y)`, so `dim L(Q)>=2`; even one such nonzero rank-one map is
impossible.  In particular two fully transverse ones cannot occur.  QED.

### Lemma 2 (a rank-one square cannot have two alternating radical rows)

Let `dim Q=3`.  Suppose

```text
M_(v,v)|Q has nonzero rank one,
M_(v,p)(Q)=M_(v,w)(Q)=0.                            (18)
```

Then

```text
Alt(v,p,w)=0.                                       (19)
```

#### Proof

A pure `v` has zero square.

If `v=x+y+z` has full support, the kernel of its square map is the
two-plane (16).  The rank-one restriction in (18) has a two-dimensional
kernel, so `Q` contains all of (16).  Exact coefficient comparison in

```text
M_(v,C)(c_X x,c_Y y,c_Z z)=0,
                 c_X+c_Y+c_Z=0                     (20)
```

gives

```text
x tensor C_Y=C_X tensor y,
y tensor C_Z=C_Y tensor z.                          (21)
```

Thus every mixed radical `C` is proportional to `v`.  In particular
`p,w` cannot complete `v` to a nonzero alternating tensor.

If `v=x+y` has two-source support, its square is

```text
M_(v,v)(q)=2x tensor y tensor q_Z.                  (22)
```

Rank one on the three-plane `Q` means

```text
Q_0=Q intersect (X direct-sum Y),          dim Q_0=2. (23)
```

For `q in Q_0`, the mixed zero is

```text
C_Z tensor(x tensor q_Y+q_X tensor y)=0.            (24)
```

The parenthesized map has the one-dimensional kernel `span(x-y)`.  Since
`dim Q_0=2`, (24) forces `C_Z=0`.  Applying this to both `p,w` shows that
`v,p,w` all miss `Z`, so their alternating separated tensor vanishes.
QED.

## 3. Excluding one coloop orientation

By target-colour permutation and first/second-root symmetry, all four
alternatives in (9) are equivalent.  Suppose

```text
N subset {alpha_a=0}.                               (25)
```

Deleting `r_a` leaves the other six rows in one two-plane.  Since `P` is
already a two-plane,

```text
S=P=span(p_a,p_b),
r_b,h_s,h_a,h_b subset S,
r_a notin S.                                        (26)
```

Write

```text
r_b=c p_a+d p_b,                 (c,d)!=(0,0).      (27)
```

The untouched table (5) is

```text
M_(r_a,p_a)(q(gamma))=gamma_a T_a,
M_(r_a,p_b)(Q)=0,
M_(r_b,p_a)(Q)=0,
M_(r_b,p_b)(q(gamma))=gamma_b T_b.                  (28)
```

We split (27).

### Both coefficients nonzero

By symmetry and (28),

```text
M_(r_b,r_b)|Q=d M_(r_b,p_b)|Q,
M_(r_a,r_b)|Q=c M_(r_a,p_a)|Q.                     (29)
```

These are nonzero rank-one maps onto `T_b` and `T_a`.  The S2AL
square/mixed tangent lemma says that a nonzero rank-one square and a
nonzero rank-one mixed map containing its repeated row have image tensors
sharing a source factor line.  This contradicts the full transversality of
`T_a,T_b`.

### The endpoint `d=0`

Now `r_b` is proportional to `p_a`.  Equations (28) give

```text
M_(p_a,p_a)(Q)=0,
M_(r_a,p_a)|Q and M_(p_b,p_a)|Q
  are nonzero rank-one maps onto T_a,T_b.            (30)
```

Lemma 1 contradicts their full transversality.

### The endpoint `c=0`

Now `r_b` is proportional to `p_b`.  Equations (28) give

```text
M_(p_b,p_b)|Q has nonzero rank one,
M_(p_b,r_a)(Q)=M_(p_b,p_a)(Q)=0.                    (31)
```

The three vectors `p_b,r_a,p_a` form a basis of `V`; hence (13) says their
alternating tensor is nonzero.  Lemma 2 says it is zero.  This final
contradiction excludes (25), and symmetry excludes the other three
ordinary coloops.

Therefore the same-colour central chart (2) is impossible.

## 4. Proof-topology consequence

Together with S2AS--S2AW, the central `(1,1,2)` frontier is now

```text
distinct-colour central coordinate pair:            IMPOSSIBLE;
same-colour central coordinate pair:                IMPOSSIBLE;

genuinely outer coordinate-pair charts / other
(1,1,2) boundaries:                                 OPEN;
(1,2,2), joint rank at most four, other physical
branches and higher orders:                         OPEN;
global Krenn--Gu conjecture:                         UNRESOLVED.      (32)
```

No finite scan, numerical specialization, generic-point promotion, or
unproved case cover enters the argument.

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_one_two_same_colour_central_chart_exclusion.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_one_two_same_colour_central_chart_exclusion.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_one_two_same_colour_central_chart_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_one_two_same_colour_central_chart_exclusion.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_one_two_same_colour_central_chart_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_one_two_same_colour_central_chart_exclusion.py
```

The primary replay checks the scalar-general derivative, kernel,
annihilator, recovery scalar, quotient-rank model, both endpoint
source-support atlases, and the three coefficient cases in (27).  The
independent no-import audit uses standard-library `Fraction`, reverse-flat
tensor storage, independent Gaussian elimination, and separately assembled
canonical models.

## Dependencies

- [`(1,1,2)` central-coordinate torus localization](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_ONE_TWO_CENTRAL_COORDINATE_TORUS_LOCALIZATION_THEOREM.md)
- [Support-one higher-row-rank exclusion, square/mixed tangent lemma](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_SUPPORT_ONE_HIGHER_ROW_RANK_EXCLUSION_THEOREM.md#2-two-exact-two-plane-lemmas)
- [Torus-annihilator obstruction](BALANCED_M3_SINGLETON_SPAN_TORUS_ANNIHILATOR_PERMANENT_RANK_OBSTRUCTION.md)
