# Balanced `m=3` joint-rank-five Hilbert--Burch repeated-coordinate support localization

## Status

**Exact characteristic-zero support localization on the repeated-coordinate
`(1,1,1)` Hilbert--Burch boundary of the normalized, target-consistent
physical `m=3` common-three-space full-sensor stratum.**  Let `U` be the
total singleton span, put `K=image H`, and assume

```text
dim U=3,                         rank H=5.             (1)
```

Use the S2AG Hilbert--Burch normal form

```text
ker D_B=span{(x,0,z),(0,y,z)},

B_23=-y tensor z,       B_13=-x tensor z,
B_12= x tensor y.                                      (2)
```

Suppose two triangle factors use the same target coordinate.  After a root
permutation write

```text
x=lambda e_s,             y=mu e_s,
lambda mu!=0.                                          (3)
```

S2AN proves `z_s=0`.  The new conclusion is:

> The remaining factor `z` is itself a target-coordinate vector, on a
> coordinate different from `s`.

Equivalently, every surviving repeated-coordinate chart has, up to root and
target-colour permutation, the discrete factor-line pattern

```text
(x,y,z)=(e_s,e_s,e_t),              s!=t.             (4)
```

The proof excludes the only other possibility, namely that `z` has both
complementary coordinates nonzero.  Its complete untouched root grid gives
two fully transverse diagonal targets at one contracted third row and zero
at another.  All six rows lie in one three-plane.  Pairwise-distinct row
planes fall to the cubic restriction kernels already isolated in S2AN;
equal row planes fall either to the S2AL two-square obstruction or directly
to a singular change-of-basis matrix.

This is a localization, not an exclusion of the discrete patterns (4), the
complete `(1,1,1)` profile, the `(1,1,2)` or `(1,2,2)` profiles, joint rank
at most four, other physical components or pole strata, higher orders, or
the global conjecture.  Global Krenn--Gu remains **UNRESOLVED**.

The successor repeated-coordinate exclusion now proves that the discrete
patterns (4) are impossible.  Thus S2AN--S2AP together close the complete
repeated-coordinate `(1,1,1)` chart.  This successor does not change the
scope or proof below.

## 1. The complementary support-two grid

Let `u,v` be the two colours different from `s`.  By S2AN,

```text
z=a e_u+b e_v.                                        (5)
```

Assume for contradiction that

```text
a b!=0.                                               (6)
```

With (3), the derivative is

```text
D_B(A,B,C)
 =-mu A tensor e_s tensor z
  -lambda e_s tensor B tensor z
  +lambda mu e_s tensor e_s tensor C.                (7)
```

For the transposed root rows write

```text
r_i=rho(e_i^*),       p_j=pi(e_j^*),
q_k=theta(e_k^*),     T_k=X_k tensor Y_k tensor Z_k. (8)
```

Every coefficient of (7) whose first two root colours lie in `{u,v}` is
zero.  Since `U=D_B(K)`, the complete target equation gives the exact grid

```text
per(r_i,p_j,q_k)=delta_(i,j,k) T_k,
i,j in {u,v},                  k in {s,u,v}.          (9)
```

The covector

```text
gamma=b e_u^*-a e_v^*                    satisfies gamma(z)=0. (10)
```

Put

```text
q'=theta(gamma)=b q_u-a q_v.                         (11)
```

Contracting (9) gives

```text
per(r_u,p_u,q')= b T_u,
per(r_v,p_v,q')=-a T_v,
per(r_u,p_v,q')=per(r_v,p_u,q')=0,                  (12)

per(r_i,p_j,q_s)=0,                  i,j in {u,v}.  (13)
```

The row `q_s` cannot vanish.  Indeed, `q_s=0` means that the third-root
covector `e_s^*` belongs to `ker H^T=K^perp`.  Every `(A,B,C) in K` would
then satisfy `C_s=0`.  Since `z_s=0`, equation (7) shows that every tensor
in `U=D_B(K)` has zero `(s,s,s)` coefficient.  The all-cross coefficient is
also zero because it contains `q_s`.  This cannot equal the nonzero target
coefficient `T_s` modulo `U`.

Moreover, `q_s` is not proportional to `q'`: equations (12)--(13), evaluated
at `(r_u,p_u)`, would otherwise force `q_s=0`.  Hence

```text
Q=span(q',q_s)                         is a two-plane. (14)
```

As in S2AN, every covector used in (12)--(13) annihilates `ker D_B`.
Because `ker D_B subset K`, their transposed rows lie in

```text
V=H^T((ker D_B)^perp),

dim V=dim((ker D_B)^perp)-dim K^perp=7-4=3.         (15)
```

The two target rows in (12) also show that

```text
R=span(r_u,r_v),       P=span(p_u,p_v)              (16)
```

are two-planes.  Thus `R,P,Q` are three two-planes inside the same
three-plane `V`.

## 2. A same-third-row binary diagonal frame is impossible

We isolate the exact incidence statement used by (12)--(16).

### Lemma 1 (same-third-row binary diagonal obstruction)

Let `W=X direct-sum Y direct-sum Z` over a characteristic-zero field.  Let
`V subset W` have dimension three, and let `R,P,Q subset V` be two-planes
with ordered bases

```text
(r_0,r_1),              (p_0,p_1),              (q_0,q_1). (17)
```

There are no nonzero scalars `c_0,c_1` and decomposable tensors `T_0,T_1`
with distinct factor lines in all three sources such that

```text
per(r_0,p_0,q_0)=c_0 T_0,
per(r_1,p_1,q_0)=c_1 T_1,                           (18)

per(r_a,p_b,q_c)=0                 at the other six binary triples. (19)
```

### Proof

Choose coordinate bases in the three tensor sources whose first two lines
are the factor lines of `T_0,T_1`.  Their restrictions to `V` are linear
forms

```text
xi_i, eta_j, zeta_k in V^*,             i,j,k in {0,1,2}. (20)
```

Let

```text
Res:S^3 V^* -> R^* tensor P^* tensor Q^*            (21)
```

be symmetric polarization restricted to `R x P x Q`.  Equations
(18)--(19) say that every source coefficient

```text
Res(xi_i eta_j zeta_k)                              (22)
```

vanishes except those for `(i,j,k)=(0,0,0)` and `(1,1,1)`.  Their locations
inside the binary row table differ from S2AN, but the zero source-coefficient
pattern is identical.

Let `alpha,beta,gamma` be normals to `R,P,Q`.

#### Pairwise-distinct planes

If the normals are independent, choose them as coordinates `A,B,C`.  The
exact restriction kernel is

```text
ker Res=span(A^3,B^3,C^3).                          (23)
```

The S2AN diagonal-divisor argument applies directly.  The two nonzero split
cubics

```text
xi_0 eta_1 zeta_0,            xi_0 eta_1 zeta_1     (24)
```

share a quadratic factor and lie in (23), so they are proportional and
`zeta_0` is proportional to `zeta_1`.  The analogous pairs force
`eta_0` proportional to `eta_1` and `xi_0` proportional to `xi_1`.  A
nonzero target product is then proportional to a mixed product in
`ker Res`, a contradiction.

If the three distinct normals span a pencil, normalize them to
`A,B,A+B`.  Then

```text
ker Res=span(A^3,B^3,AB(A+B)) subset S^3 N,
N=span(A,B).                                           (25)
```

For any nonzero source-coordinate form, choose the other two factors from
the nonzero target products so that the resulting coordinate triple is not
one of the two targets.  That nonzero split product lies in `S^3 N`.
Unique factorization puts each of its linear factors in `N`.  Hence all
nine coordinate forms in (20) lie in `N`, although together they separate
the points of the embedded three-space `V subset W`.  This would put `V^*`
inside a two-plane, again impossible.

#### Two planes agree

Suppose first that `R=P`, and write

```text
p_b=sum_i L_(b,i) r_i,                 L in GL_2.    (26)
```

For fixed `q`, the permanent matrix is `F=S L^T` with `S` symmetric, so
`L F` is symmetric.  At `q_0`, the two tensor coefficients in (18) are
`c_0 T_0 E_00` and `c_1 T_1 E_11`.  Since `T_0,T_1` are linearly
independent, symmetry forces both off-diagonal entries of `L` to vanish.
Thus `p_0` is proportional to `r_0` and `p_1` to `r_1`.  Equations
(18)--(19) now give on the two-plane `Q`

```text
per(r_0,r_1,Q)=0,

per(r_0,r_0)|Q and per(r_1,r_1)|Q are nonzero
rank-one maps onto the fully transverse T_0,T_1.     (27)
```

The exact two-plane square lemma of S2AL forbids (27).

Suppose instead that `R=Q`, with

```text
q_c=sum_i L_(c,i) r_i.                              (28)
```

Fixing `p_0` in (18)--(19) gives the matrix `c_0 T_0 E_00`; symmetry of its
left product by `L` forces `L_10=0`.  Fixing `p_1` gives
`c_1 T_1 E_10`; symmetry forces `L_11=0`.  The second row of `L` therefore
vanishes, contradicting invertibility.  The case `P=Q` is identical after
exchanging the first two permanent arguments.

The equal-plane case and the two possible incidences of three pairwise-
distinct plane normals exhaust all arrangements.  This proves the lemma.
QED.

## 3. Support localization

Equations (12)--(16) satisfy Lemma 1 with

```text
(q_0,q_1)=(q',q_s),       (T_0,T_1)=(T_u,T_v),
(c_0,c_1)=(b,-a).                                    (29)
```

This contradicts (6).  Consequently `a b=0`.  The Hilbert--Burch factor
`z` is nonzero, so exactly one of `a,b` is nonzero and

```text
z is proportional to e_t for one t!=s.              (30)
```

Root symmetry gives the same conclusion whenever any pair among `x,y,z`
uses the same coordinate line.

## 4. Proof-topology consequence

The repeated-coordinate part of the `(1,1,1)` frontier is now discrete:

```text
Hilbert--Burch (1,1,1):
  two equal coordinate factors and a third factor
  with nonzero same-colour coordinate:               IMPOSSIBLE (S2AN);
  two equal coordinate factors and a genuinely
  two-supported complementary factor:                IMPOSSIBLE;
  exact coordinate pattern (s,s,t), s!=t:            OPEN;
  coordinate-distinct / other allowed charts:        OPEN;

Hilbert--Burch (1,1,2), (1,2,2):                    OPEN;
joint rank at most four / other physical branches:   OPEN;
global Krenn--Gu conjecture:                         UNRESOLVED.       (31)
```

No point with pattern (4) is constructed here.  The result says only that
such discrete patterns are the complete residual of the repeated-coordinate
chart.

The successor theorem excludes that residual exactly.

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_repeated_coordinate_support_localization.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_repeated_coordinate_support_localization.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_repeated_coordinate_support_localization.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_repeated_coordinate_support_localization.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_repeated_coordinate_support_localization.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_repeated_coordinate_support_localization.py
```

The primary replay checks the scalar-general Hilbert--Burch derivative, the
complete untouched grid, the complementary annihilator, the `(s,s,s)` row
support, the independent and pencil incidence kernels, and all three
equal-plane matrix orientations.  The independent audit imports no
repository or third-party module and reconstructs those identities with
standard-library `Fraction` arithmetic, a row-oriented tensor convention,
and separate exact elimination.  The scripts replay displayed identities;
the arbitrary-field divisor, unique-factorization, and inherited square
arguments are the proof above.

## Dependencies

- [Repeated-coordinate Hilbert--Burch localization](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_REPEATED_COORDINATE_LOCALIZATION_THEOREM.md)
- [Support-one higher-row-rank exclusion and two-plane square lemma](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_SUPPORT_ONE_HIGHER_ROW_RANK_EXCLUSION_THEOREM.md)
