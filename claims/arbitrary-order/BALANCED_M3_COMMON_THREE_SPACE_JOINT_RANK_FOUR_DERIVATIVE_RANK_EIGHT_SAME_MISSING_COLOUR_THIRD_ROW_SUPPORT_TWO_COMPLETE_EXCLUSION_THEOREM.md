# Balanced `m=3` common-three-space joint-rank-four derivative-rank-eight same-missing-colour third-row-support-two complete exclusion

## Status

**Exact characteristic-zero exclusion of the complete support-two third-row
kernel cell in the S2BR same-missing-colour `(2,2,2)` profile.**  Retain the
normalized, target-consistent physical `m=3` common-three-space full-sensor
hypotheses with singleton span dimension three, joint rank four, all three
root blocks nonzero, and shared-derivative rank eight.  Let `d` be the common
missing colour of the first and second rows.  Suppose the third row has rank
two and its kernel generator has both complementary colours `s,t` in its
support.

S2BR then puts the derivative, after exchanging the first two roots and
rescaling nonzero factors, in the form

```text
D(a,b,c)=(a tensor e_t-e_s tensor b) tensor w+C tensor c,

C=kappa e_d tensor e_d+C_bar,        kappa!=0,
ker D=span((e_s,e_t,0)),                              (1)

eta=eta_s e_s^*+eta_t e_t^*,
eta_s eta_t eta(w)!=0,                               (2)
```

where `eta` spans the third-row kernel.  The complete empty-target identity
forces all three exact vectors

```text
(0,0,e_d),             (0,e_s,0),             (e_t,0,0)
  in K.                                                (3)
```

Together with the derivative syzygy `(e_s,e_t,0)`, these are four
independent vectors.  They therefore span the four-space `K`, but their
third projection is only `span(e_d)`.  This contradicts the assumed
third-row rank two.  Hence the support-two cell is empty.

Combined with S2BU--S2BV, this closes the complete same-missing-colour
`(2,2,2)` graph cell for every rank-two third row: support one is excluded at
the empty or pair gate, and support two is impossible here.  Third-row rank
three, mixed or injective involved rows, joint rank three, derivative rank
seven, other components and pole strata, higher orders, and all-rank drop
remain open.  Global Krenn--Gu remains **UNRESOLVED**.

## 1. Three pure-target correction preimages

For the physical pure source tensor

```text
T_c=X_c tensor Y_c tensor Z_c,                       (4)
```

write

```text
u_c=[T_c]G_N-e_c tensor e_c tensor e_c in U.         (5)
```

Choose `(a_c,b_c,c_c) in K` with

```text
D(a_c,b_c,c_c)=u_c.                                  (6)
```

The common missing first row is `r_d=0`.  Contracting (5)--(6) in the first
root by `e_d^*`, and using the isolated `d` row of `C`, gives

```text
c_d=-kappa^(-1)e_d,
c_s=c_t=0.                                           (7)
```

Indeed the `T_d` target leaves `-e_d tensor e_d`, while the `T_s,T_t`
targets have zero first-`d` contraction.  This fixes the entire third
component because `(e_d^* tensor id)C=kappa e_d` is nonzero.

Now contract in the third root by `eta`.  The row-kernel condition kills
the corresponding contraction of every coefficient of `G_N`.  Since
`eta(e_d)=0`, equations (1), (2), and (7) give

```text
eta(w)(a_d tensor e_t-e_s tensor b_d)=0,             (8)

eta(w)(a_s tensor e_t-e_s tensor b_s)
  =-eta_s e_s tensor e_s,                            (9)

eta(w)(a_t tensor e_t-e_s tensor b_t)
  =-eta_t e_t tensor e_t.                           (10)
```

The kernel of the two-factor tangent map

```text
(a,b) |-> a tensor e_t-e_s tensor b                 (11)
```

is exactly `span((e_s,e_t))`.  Equation (8), after subtracting a multiple
of the contained derivative syzygy, proves

```text
(0,0,e_d) in K.                                     (12)
```

For (9), quotienting the first factor by `e_s` puts `a_s` on the line
`e_s`; substitution then shows that `(a_s,b_s)` differs from a nonzero
multiple of `(0,e_s)` only by the tangent kernel.  Hence

```text
(0,e_s,0) in K.                                     (13)
```

Root exchange in the two-factor tangent map, or the same quotient argument
applied to (10), gives

```text
(e_t,0,0) in K.                                     (14)
```

The nonzero scalars `eta_s,eta_t,eta(w),kappa` only rescale the three
vectors and never change their lines.

## 2. Projection-rank contradiction

The four vectors

```text
(e_s,e_t,0),       (0,0,e_d),
(0,e_s,0),         (e_t,0,0)                        (15)
```

are independent: the last three have distinct third or complementary first
and second components, and the first vector cannot lie in their span by its
`e_s` first component and `e_t` second component.  Since `dim K=4`, (15) is
a basis of `K`.  Therefore

```text
pr_3 K=span(e_d),                  dim pr_3 K=1.      (16)
```

But the rank of the transposed third root row equals `dim pr_3 K`, while the
cell hypothesis is rank two.  This contradiction proves the exclusion.

No assumption on `C_bar`, no coordinate assumption on `w`, no source-support
classification, no pair regularity, and no numerical specialization enters
the proof.

## 3. Proof-topology consequence

Inside the S2BR same-missing-colour `(2,2)` survivor,

```text
third-row rank two:
  kernel support one:    complete graph cell IMPOSSIBLE (S2BU--S2BV);
  kernel support two:    IMPOSSIBLE (this theorem);

same-colour (2,2,2) profile:                         CLOSED.           (17)
```

## 4. Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_same_missing_colour_third_row_support_two_complete_exclusion.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_same_missing_colour_third_row_support_two_complete_exclusion.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_same_missing_colour_third_row_support_two_complete_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_same_missing_colour_third_row_support_two_complete_exclusion.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_same_missing_colour_third_row_support_two_complete_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_four_derivative_rank_eight_same_missing_colour_third_row_support_two_complete_exclusion.py
```

The primary replay checks the derivative kernel, the three combined
first-/third-contraction affine systems, their common one-dimensional
syzygy freedom, and the forced four-space projection rank with SymPy.  The
independent no-import audit reverses tensor indexing and reconstructs the
three affine systems, exact ranks, forced representatives, and projection
contradiction with standard-library `Fraction` arithmetic.  The arbitrary-
vector contractions above are the proof.

## Dependencies

- [Rank-four/rank-eight target-kernel atlas](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_TARGET_KERNEL_ATLAS_AND_DISTINCT_MISSING_COLOUR_EXCLUSION_THEOREM.md)
- [Support-one split-lift atlas](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_SAME_MISSING_COLOUR_THIRD_ROW_SUPPORT_ONE_SPLIT_LIFT_ATLAS_THEOREM.md)
- [Nonaligned source atlas and pair-pole exclusion](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_DERIVATIVE_RANK_EIGHT_SAME_MISSING_COLOUR_THIRD_ROW_SUPPORT_ONE_NONALIGNED_SOURCE_ATLAS_AND_PAIR_POLE_EXCLUSION_THEOREM.md)

## Scope boundary

```text
same-colour (2,2,2) support-two third-row cell:       IMPOSSIBLE;
complete same-colour (2,2,2) rank-two-third-row cell: CLOSED;
third-row rank three / other involved-row profiles:  OPEN;
lower-rank target cells / other components and poles: OPEN;
higher balanced orders / all-balanced rank-drop:     OPEN;
global Krenn--Gu conjecture:                         UNRESOLVED.       (18)
```
