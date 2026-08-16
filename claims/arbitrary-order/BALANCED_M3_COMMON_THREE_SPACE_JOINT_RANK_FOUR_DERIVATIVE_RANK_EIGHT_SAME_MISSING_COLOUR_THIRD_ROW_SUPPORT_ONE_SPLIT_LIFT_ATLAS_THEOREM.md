# Balanced `m=3` common-three-space joint-rank-four derivative-rank-eight same-missing-colour third-row-support-one split-lift atlas

## Status

**Exact characteristic-zero split-lift rigidity on the complete
same-missing-colour `(2,2,2)` row-profile cell whose third-row kernel is one
target coordinate.**  Retain the normalized, target-consistent physical
`m=3` common-three-space full-sensor hypotheses with

```text
dim U=3,                         dim K=4,             (1)
```

all three root blocks nonzero, and shared-derivative rank eight.  In the
S2BR same-missing-colour survivor, let `d` be the common missing colour of
the first and second rows, and suppose the third row has coordinate kernel
colour `s`, where `d!=s`.  Put `t` for the remaining colour.

After exchanging the first two roots if necessary and rescaling nonzero
factors, the derivative has the form

```text
x=e_s,
D(a,b,c)=(a tensor y-e_s tensor b) tensor w+C tensor c,

C=kappa e_d tensor e_d+C_bar,       kappa!=0,
C_bar in A_(1,bar d) tensor A_(2,bar d),             (2)

ker D=span((e_s,y,0)),              e_s^*(w)!=0.     (3)
```

The complete empty-target identity forces the two exact vectors

```text
(0,0,e_d) in K,                  (0,e_s,0) in K.    (4)
```

Thus the missing-colour lift has **no nonsplit parameter**.  Moreover every
such four-space has exactly one of the following two normal forms.

If `y` is not proportional to `e_s`, then

```text
K=span((e_s,y,0), (0,0,e_d), (0,-e_s,0), (a,0,e_t)),

span(e_s,y)=span(e_s,a)=span(e_s,e_t).              (5)
```

If `y` is proportional to `e_s`, write `y=lambda e_s`; then

```text
K=span((e_s,lambda e_s,0), (0,0,e_d), (0,-e_s,0),
       (alpha e_t,beta e_t,e_t)),

lambda alpha beta!=0.                               (6)
```

The theorem also gives the exact polarized-root-permanent box in both
charts.  On the nonmonomial residual-block branch `C_bar!=0`, the inherited
root-torus gate makes `w=e_s`; the eight-dimensional root box is then
disjoint from `U`.  This is the exhaustive lift atlas needed to continue
the S2BS quotient attack.  It is not by itself an exclusion of the remaining
normal forms: arbitrary complementary tangent directions, arbitrary
`C_bar`, the aligned chart (6), and the wider open branches remain.
Global Krenn--Gu remains **UNRESOLVED**.

## 1. The two pure-target correction coefficients

Let `[E]G_N` denote the root-tensor coefficient of the physical source
tensor `E` in the complete empty permanent.  For the physical pure target

```text
T_c=X_c tensor Y_c tensor Z_c,                       (7)
```

target consistency gives

```text
u_c=[T_c]G_N-e_c tensor e_c tensor e_c in U.         (8)
```

The missing first row is `r_d=0`, and the missing third row is `q_s=0`.
Consequently, for every physical coefficient `E`,

```text
(e_d^* tensor id tensor id)[E]G_N=0,
(id tensor id tensor e_s^*)[E]G_N=0.                (9)
```

These are coefficientwise consequences of the complete six-term
permanent, not selected numerical evaluations.

### Lemma 1 (the missing-colour lift is vertical)

Choose `(a_d,b_d,c_d) in K` with

```text
D(a_d,b_d,c_d)=u_d.                                 (10)
```

The first contraction in (9), (8), and the isolated `d` row of `C` give

```text
kappa e_d tensor c_d=-e_d tensor e_d,
c_d=-kappa^(-1)e_d.                                 (11)
```

The third contraction in (9) has zero target contribution because `d!=s`.
Using (3) and (11), it becomes

```text
e_s^*(w)(a_d tensor y-e_s tensor b_d)=0.            (12)
```

Both `y` and `e_s` are nonzero, and the kernel of

```text
(a,b) |-> a tensor y-e_s tensor b                  (13)
```

is exactly `span((e_s,y))`: quotient first by `e_s`, then second by `y`.
Hence `(a_d,b_d)=lambda(e_s,y)`.  Subtracting the derivative syzygy in
(3) from (10) and rescaling proves

```text
(0,0,e_d) in K.                                    (14)
```

### Lemma 2 (the third-kernel colour also splits)

Choose `(a_s,b_s,c_s) in K` with derivative image `u_s`.  Contracting first
by `e_d^*` now has zero target contribution, so (2) and (9) give

```text
c_s=0.                                             (15)
```

The third contraction has target contribution `-e_s tensor e_s`; write
`delta=e_s^*(w)!=0`.  Therefore

```text
delta(a_s tensor y-e_s tensor b_s)=-e_s tensor e_s. (16)
```

Quotienting the first factor by `e_s` puts `a_s` on the line `e_s`.
Writing `a_s=mu e_s`, equation (16) then gives

```text
b_s=mu y+delta^(-1)e_s.                             (17)
```

Subtract the multiple `mu(e_s,y,0)` of the syzygy.  Up to a nonzero
rescaling this proves

```text
(0,e_s,0) in K.                                    (18)
```

Together, Lemmas 1--2 prove (4).  Notice that no assumption on the support
of `w` beyond `e_s^*(w)!=0`, and no assumption `C_bar!=0`, entered either
argument.

## 2. Exhaustive four-space normal forms

The row kernels `(d,d,s)` say

```text
pr_1 K=pr_2 K=span(e_s,e_t),
pr_3 K=span(e_d,e_t).                               (19)
```

The three vectors in (3)--(4) are independent.  Choose a fourth vector of
`K` whose third component is `e_t`, after subtracting a multiple of
`(0,0,e_d)`.

If `y` and `e_s` are independent, the second components of
`(e_s,y,0)` and `(0,e_s,0)` span the whole complementary plane.  Subtract a
unique combination of them to kill the second component of the fourth
vector.  It has the form `(a,0,e_t)`.  The first projection in (19) forces
`a` to be independent of `e_s`, proving (5).

If `y` is proportional to `e_s`, write `y=lambda e_s`, with `lambda!=0`.
Adding the first
and third displayed generators independently removes the `e_s` components
of the first two entries of the fourth vector.  It becomes

```text
(alpha e_t,beta e_t,e_t).                           (20)
```

The first two projection ranks in (19) force `alpha,beta` both nonzero,
proving (6).  The two cases exhaust the projective relation between `y` and
`e_s`.

## 3. Exact polarized-root-permanent boxes

For three elements of `A_1 direct-sum A_2 direct-sum A_3`, let `Perm`
denote the six-term polarized root permanent.

### 3.1 The nonaligned chart

Use the ordered basis in (5), denoted `k_0,k_1,k_2,k_3`.  Its only nonzero
unordered root products are

```text
Perm(k_0,k_0,k_1)= 2 e_s tensor y tensor e_d,
Perm(k_0,k_0,k_3)= 2 e_s tensor y tensor e_t,
Perm(k_0,k_1,k_2)=-  e_s tensor e_s tensor e_d,
Perm(k_0,k_1,k_3)=   a tensor y tensor e_d,
Perm(k_0,k_2,k_3)=-  e_s tensor e_s tensor e_t,
Perm(k_0,k_3,k_3)= 2 a tensor y tensor e_t,
Perm(k_1,k_2,k_3)=-  a tensor e_s tensor e_d,
Perm(k_2,k_3,k_3)=-2 a tensor e_s tensor e_t.        (21)
```

They form a basis of the eight-space

```text
L=span(e_s,e_t) tensor span(e_s,e_t)
  tensor span(e_d,e_t).                              (22)
```

Thus S2BS's eight-product incidence is universal throughout the nonaligned
split atlas; only the two target vectors' coordinates in this box vary.

### 3.2 The aligned chart

Use the ordered basis in (6) and abbreviate `L=lambda`, `A=alpha`,
`B=beta`.  The ten
nonzero unordered products are

```text
Perm(k_0,k_0,k_1)= 2L s s d,
Perm(k_0,k_1,k_2)=-  s s d,
Perm(k_0,k_1,k_3)= B s t d+AL t s d,
Perm(k_1,k_2,k_3)=-A t s d,
Perm(k_1,k_3,k_3)= 2AB t t d,

Perm(k_0,k_0,k_3)= 2L s s t,
Perm(k_0,k_2,k_3)=-  s s t,
Perm(k_0,k_3,k_3)= 2B s t t+2AL t s t,
Perm(k_2,k_3,k_3)=-2A t s t,
Perm(k_3,k_3,k_3)= 6AB t t t.                       (23)
```

Here juxtaposition abbreviates a root tensor.  Since `LAB!=0`, the products
span the same eight-space `L`; the only linear repetitions visible before
changing basis are the two proportional pairs in the first and sixth rows
of (23).

## 4. The nonmonomial root-box quotient

If `C_bar!=0`, then `C` contains its nonzero isolated `dd` monomial and a
second monomial.  It is nonmonomial, so S2BQ forces `w` to be coordinate.
Because `e_s^*(w)!=0`, rescale to

```text
w=e_s.                                              (24)
```

In either chart, `U=D(K)` is generated by the images of the last three
basis vectors.  Any linear combination lying in `L` has zero coefficient
on `e_d tensor e_d tensor e_d`, forcing the coefficient of `D(k_1)` to
vanish; zero coefficient on `e_d tensor e_d tensor e_t` then forces the
coefficient of `D(k_3)` to vanish; and the remaining `e_s tensor e_s tensor
e_s` coefficient forces that of `D(k_2)` to vanish.  Therefore

```text
U intersect L=0.                                   (25)
```

The vertical lift also gives the exact quotient reduction

```text
e_d tensor e_d tensor e_d
  congruent -kappa^(-1) C_bar tensor e_d      modulo U. (26)
```

Equations (21), (23), and (26) are the finite successor interface for the
remaining source-permanent obstruction.  S2BS is the specialization of
(5) with `y=a=e_t` and `C_bar=e_s tensor e_s`.

## 5. Proof-topology consequence

Inside the S2BR same-missing-colour cell, this theorem proves

```text
third-row rank two with coordinate kernel e_s^*:
  missing-colour lift (0,0,e_d):                    FORCED;
  third-kernel-colour split (0,e_s,0):              FORCED;
  nonaligned and aligned K normal forms (5),(6):    EXHAUSTIVE;
  nonsplit missing-colour lifts:                    IMPOSSIBLE;
  exact root-product boxes (21),(23):                PROVED.          (27)
```

The arbitrary complementary directions and residual block in (5), the
aligned chart (6), the monomial-`C` branch with possibly noncoordinate `w`,
third-row rank three, mixed or injective involved rows, joint rank three,
derivative rank seven, the pair gate, other components and pole strata,
higher orders, and all-rank-drop remain open.

## 6. Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_same_missing_colour_third_row_support_one_split_lift_atlas.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_same_missing_colour_third_row_support_one_split_lift_atlas.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_same_missing_colour_third_row_support_one_split_lift_atlas.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_same_missing_colour_third_row_support_one_split_lift_atlas.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_same_missing_colour_third_row_support_one_split_lift_atlas.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_same_missing_colour_third_row_support_one_split_lift_atlas.py
```

The primary replay checks the two affine contraction systems, both canonical
four-spaces, every unordered root product, both eight-dimensional product
spans, the derivative incidence, the direct quotient, and (26) with SymPy.
The independent no-import audit reverses tensor indexing, reconstructs the
affine solution spaces from exact rational row reduction, and independently
enumerates the two root-product atlases with `Fraction` arithmetic.  The
arbitrary-vector quotient arguments in Sections 1--2 are the proof.

## Dependencies

- [Rank-four/rank-eight target-kernel atlas](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_TARGET_KERNEL_ATLAS_AND_DISTINCT_MISSING_COLOUR_EXCLUSION_THEOREM.md)
- [Same-colour coordinate split-lift exclusion](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_SAME_MISSING_COLOUR_THIRD_ROW_RANK_TWO_COORDINATE_SPLIT_LIFT_EXCLUSION_THEOREM.md)
- [Lower-joint-rank three-root derivative and torus census](BALANCED_M3_COMMON_THREE_SPACE_LOWER_JOINT_RANK_THREE_ROOT_DERIVATIVE_AND_TORUS_CENSUS_THEOREM.md)

## Scope boundary

```text
support-one same-colour split-lift K atlas:                   PROVED;
nonsplit missing-colour lift parameter:                      IMPOSSIBLE;
nonaligned/aligned polarized root boxes:                     PROVED;
S2BS coordinate specialization:                             IMPOSSIBLE;
remaining parameters in the two exhaustive K charts:        OPEN;
other rank-eight row profiles / lower-rank target cells:     OPEN;
pair coupling / other components and poles:                  OPEN;
higher balanced orders / all-balanced rank-drop:             OPEN;
global Krenn--Gu conjecture:                                 UNRESOLVED. (28)
```
