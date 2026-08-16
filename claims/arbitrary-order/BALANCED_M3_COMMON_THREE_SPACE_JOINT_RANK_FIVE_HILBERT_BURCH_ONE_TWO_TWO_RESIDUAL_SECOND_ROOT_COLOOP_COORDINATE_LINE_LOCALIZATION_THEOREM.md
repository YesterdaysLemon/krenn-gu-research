# Balanced `m=3` joint-rank-five Hilbert--Burch `(1,2,2)` residual second-root-coloop coordinate-line localization

## Status

**Exact characteristic-zero coordinate-line localization for both residual
second-root coordinate-coloop orientations in the normalized,
target-consistent physical `m=3` common-three-space full-sensor stratum.**
Retain the S2AZ gauge

```text
dim U=3,                         rank H=5,

ker D_B=span{(lambda e_s,y,z),(0,mu e_t,w)},
lambda mu!=0,                   y_t=0,
dim span(y,e_t)=dim span(z,w)=2,                     (1)
```

and suppose the coordinate-coloop fork selects

```text
N=K^perp subset {beta_j=0},                   j!=t.  (2)
```

Let `k` be the third colour.  Then

```text
w is proportional to e_j or e_k.                     (3)
```

S2BD already proves `w_t=0`.  The new content is that

```text
w_j w_k!=0                                           (4)
```

is impossible.  Under (4), the complete derivative-zero face is a
same-third-row binary diagonal table.  Its first- and third-row planes and
one middle row lie in the exact three-space `S=R direct-sum span(A)`; the
other middle row may escape.  A new four-dimensional obstruction excludes
this one-row escape.  Plane incidence first forces the zero third row to be
the intersection of the two planes inside `S`.  The remaining row-space
orbits are 14 endpoint-support charts, five generic fixed-support charts,
and two one-parameter charts.  All 21 families have pinned exact rational
Nullstellensatz identities; the parameter identities hold polynomially for
every parameter value.

This is a localization, not an exclusion of either coloop in (2).  The four
coordinate endpoints in (3), counted with their two coloop orientations,
the three third-root coloops, the two complementary first-root coloops,
joint rank at most four, other physical component types, higher orders, and
the global conjecture remain open.  Global Krenn--Gu remains
**UNRESOLVED**.

## 1. The exact same-third-row face

Use the row notation

```text
r_i=rho(e_i^*),       p_i=pi(e_i^*),
q_i=theta(e_i^*),     T_i=X_i tensor Y_i tensor Z_i,

A=lambda^(-1)r_s,     R=rho(e_s^perp),
S=R direct-sum span(A),                         dim S=3. (5)
```

S2BD proves

```text
p_k in S,                      q(w^perp) subset S.   (6)
```

The exact target-contraction argument recorded in S2BC, which uses only the
S2AZ gauge and not its selected `alpha_s` coloop, makes both `pi` and
`theta` injective.  Therefore all ordered row pairs used below are genuine
two-plane bases.

By S2BD, `w_t=0`.  Assume (4) and put

```text
n=w_k e_j^*-w_j e_k^*,
q'=q(n).                                               (7)
```

Then `(n,e_t^*)` is a basis of `w^perp`.  On the complete face

```text
beta_t=0,                         gamma(w)=0,
```

the derivative transpose vanishes and the full target equation is

```text
per(r(alpha),p(beta),q(gamma))
 =sum_i alpha_i beta_i gamma_i T_i.                  (8)
```

Substitute the coordinate first- and second-root covectors and the two
third-root rows from (7).  One obtains

```text
per(r_j,p_j,q')= w_k T_j,
per(r_k,p_k,q')=-w_j T_k,
per(r_j,p_k,q')=per(r_k,p_j,q')=0,                  (9)

per(r_a,p_b,q_t)=0,                    a,b in {j,k}. (10)
```

The two row planes

```text
R_0=span(r_j,r_k),             Q_0=span(q',q_t)     (11)
```

lie in `S` by (5)--(7), while `p_k in S` and `p_j` may escape.  Relabel
`j,k` as binary indices `0,1`, respectively, and absorb the two nonzero
scalars in (9) into source-factor representatives.  Equations (9)--(10)
then have the abstract form in the next lemma.

## 2. A same-third-row frame cannot have one middle-row escape

### Lemma 1 (one-row-escape same-third-row obstruction)

Let `W=X direct-sum Y direct-sum Z` over a characteristic-zero field.  Let
`S subset W` be a three-space.  Let

```text
R=span(r_0,r_1),             Q=span(q_0,q_1) subset S
```

be two-planes, and let `P=span(p_0,p_1)` be a two-plane with `p_1 in S`.
There are no nonzero scalars `c_0,c_1` and fully transverse decomposable
tensors `T_0,T_1` such that

```text
per(r_0,p_0,q_0)=c_0T_0,
per(r_1,p_1,q_0)=c_1T_1,                             (12)

per(r_a,p_b,q_c)=0                 at the other six binary cells. (13)
```

#### Proof: the intersection is the zero third row

If `p_0 in S`, all three two-planes lie in one three-space and the S2AO
same-third-row obstruction applies.  Assume `p_0` is outside `S` and put

```text
S'=S direct-sum span(p_0),                 dim S'=4. (14)
```

If `R=Q`, write `q_c=sum_i L_(c,i)r_i` with `L in GL_2`.  At `p_0`, the
permanent coefficient matrix in the `R,Q` bases is a nonzero multiple of
`E_00`; symmetry of its left product by `L` gives `L_10=0`.  At `p_1`, it
is a nonzero multiple of `E_10`; symmetry gives `L_11=0`.  The second row
of `L` vanishes, a contradiction.  Hence `R` and `Q` are distinct and meet
in one line in `S`.

Choose a nonzero intersection representative

```text
ell=a_0r_0+a_1r_1=b_0q_0+b_1q_1.                    (15)
```

Equation (12)--(13) gives the exact square values on `P`:

```text
M_(ell,ell)(p_0)=a_0b_0c_0T_0,
M_(ell,ell)(p_1)=a_1b_0c_1T_1.                      (16)
```

If `b_0a_0a_1!=0`, one square map contains two fully transverse
decomposable tensors, contrary to S2AL tangent-line separation.  Thus
`b_0=0` or `ell` is a coordinate line in `R`.

Suppose `b_0!=0`.  Then `ell=r_a` after rescaling.  Representing this same
line by its `Q` coordinates in (15), the square map

```text
M_(ell,ell)|P
```

has nonzero rank-one image `span(T_a)`, while

```text
M_(ell,r_(1-a))|P
```

has nonzero rank-one image `span(T_(1-a))`.  S2AL mixed factor sharing says
the two decomposable images share a source factor, contradicting full
transversality.  Therefore `b_0=0`.  Since the `Q` representation in (15)
is nonzero,

```text
R intersect Q=span(q_1).                              (17)
```

This is the promised incidence reduction: the zero third row, not the
active row `q_0`, is exactly the plane-intersection line.

#### Proof: 21 normalized row-space families

Choose a basis of `S'` so that

```text
r_0=e_0,       r_1=e_1,       q_0=e_2,       p_0=e_3. (18)
```

By (17), write

```text
q_1=a e_0+b e_1,              (a,b)!=(0,0),
p_1=c e_0+d e_1+f e_2,        (c,d,f)!=(0,0,0).     (19)
```

Independent diagonal rescaling of `(e_0,e_1,e_2)`, together with rescaling
of the row representatives, gives the complete orbit list below.

If `ab=0`, normalize `q_1` to `e_0` or `e_1`.  Each nonzero coefficient of
`p_1` can then be normalized independently to one.  This gives

```text
2 endpoint choices * 7 nonempty support masks = 14 families. (20)
```

If `ab!=0`, normalize `q_1=e_0+e_1`.  When at most one of `c,d` is nonzero,
all nonzero coefficients of `p_1` again normalize to one.  The possible
support masks are

```text
1,2,4,5,6,                                      five families. (21)
```

When `cd!=0`, normalize

```text
p_1=e_0+tau e_1                       or
p_1=e_0+tau e_1+e_2,                  tau!=0.        (22)
```

These are two one-parameter families.  Equations (20)--(22) are exhaustive,
for a total of 21 families.  Notice that no finite selection of values of
`tau` is being made.

Choose source-coordinate bases whose first two lines are the factor lines
of `T_0,T_1`.  Let the restrictions of their six selected coordinate forms
to `S'` be

```text
xi_0,xi_1, eta_0,eta_1, zeta_0,zeta_1 in (S')^*.    (23)
```

For each of the eight source triples and eight row triples, expand the
symmetric polarized product of the forms (23) on the rows (18)--(22).  Set
the coefficient to one exactly at

```text
(source;row)=(000;000),             (111;110),       (24)
```

and to zero at the other 62 positions.  The second row triple is `110`
because both surviving targets use `q_0`.  Thus every family gives 64
polynomial equations `f_1,...,f_64`.  In the two parameter families these
belong to the rational polynomial ring in the 24 form coefficients and
`tau`.

For all 21 families, the durable certificate supplies an exact identity

```text
1=sum_(nu=1)^64 h_nu f_nu.                           (25)
```

The identities contain 9,256 sparse multiplier terms in total.  Their
SHA-256 is

```text
e822cb443173acbab3604d6e3e28afaf7fd99a3e306731e21c7c7bc5023ac5fc. (26)
```

The two parameter identities are polynomial identities in `tau`; they use
no inverse of `tau` and in fact remain valid at `tau=0`.  In particular they
hold on the required punctured parameter line `tau!=0` over every
characteristic-zero field.  Both replay programs reconstruct all 64
generators for every family before checking (25).  The independent audit
reverses the 25-variable order and uses a separate standard-library sparse
permanent expansion.  Therefore no family in (20)--(22) exists.  This proves
Lemma 1.  QED.

## 3. Coordinate-line consequence

Equations (9)--(11) satisfy Lemma 1 with

```text
(q_0,q_1)=(q',q_t),          (T_0,T_1)=(T_j,T_k),
(c_0,c_1)=(w_k,-w_j).                              (27)
```

This contradicts (4).  Since S2BD gives `w_t=0` and (1) makes `w` nonzero,
exactly one of `w_j,w_k` is nonzero.  This proves (3).

The live `(1,2,2)` rank-five coloop frontier is now

```text
beta_t coloop:                                      IMPOSSIBLE (S2BB);
alpha_s coloop:                                     IMPOSSIBLE (S2BC);

beta_j coloop, j!=t:
  w proportional to e_j or e_k:                    OPEN;

three gamma_k coloops / two complementary alpha coloops
  / joint rank <=4 / other components / higher m:  OPEN;

global Krenn--Gu conjecture:                        UNRESOLVED.     (28)
```

No coordinate endpoint in (28) is asserted to exist.  No finite field
scan, numerical specialization, bounded parameter sample, generic-point
promotion, or unproved case cover enters the argument.

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_coordinate_line_localization.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_coordinate_line_localization.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_coordinate_line_localization.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_coordinate_line_localization.py claims/arbitrary-order/generate_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_same_third_row_certificates.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_coordinate_line_localization.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_coordinate_line_localization.py claims/arbitrary-order/generate_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_same_third_row_certificates.py
```

The primary verifier uses SymPy rational polynomials.  The independent audit
imports no repository module or third-party package.  Optional certificate
regeneration requires Singular 4.x, directly or through WSL:

```text
python claims/arbitrary-order/generate_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_same_third_row_certificates.py
```

Singular is not needed for either replay.

## Dependencies

- [Residual second-root-coloop `w_t=0` localization](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_TWO_TWO_RESIDUAL_SECOND_ROOT_COLOOP_SUPPORT_LOCALIZATION_THEOREM.md)
- [`pi,theta` injectivity in the S2AZ gauge](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_TWO_TWO_ALPHA_S_COLOOP_EXCLUSION_THEOREM.md#1-the-determinant-face-pencil)
- [Tangent-line and mixed factor-sharing lemmas](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_SUPPORT_ONE_HIGHER_ROW_RANK_EXCLUSION_THEOREM.md#2-two-exact-two-plane-lemmas)
- [Three-space same-third-row obstruction](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_REPEATED_COORDINATE_SUPPORT_LOCALIZATION_THEOREM.md#2-a-same-third-row-binary-diagonal-frame-is-impossible)
