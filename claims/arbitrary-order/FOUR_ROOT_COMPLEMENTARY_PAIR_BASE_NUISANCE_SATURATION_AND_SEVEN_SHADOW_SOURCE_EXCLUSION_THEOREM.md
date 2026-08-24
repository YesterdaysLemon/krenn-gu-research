# Four-root complementary-pair base-nuisance saturation and seven-shadow source exclusion

## Status

**Exact characteristic-zero complete-module theorem and universal source-branch
exclusion at root order four.**  In the original fixed-`Q` maximum-root
surplus-two chart, two complementary port pairs cannot both have surviving
`GLS16` base classes.

More precisely, let `S` be a pair of the four ports and let `T=U-S`.  The
order-two deck label `I=T` belongs to the complete base nuisance for target
`S`.  After maximum-root evaluation, its term has the exact factorization

```text
H_T tensor Pi_T(z_Q) in
(tensor_(u in T)V_u^*) tensor (tensor_(s in S)V_s^*). (1)
```

If `Pi_T(z_Q)` is nonzero, coefficient slices in the target-`S` factor span
the entire base receiver space on `T`.  Hence the target-`S` base class is
swallowed.  If `Pi_T(z_Q)=0`, then the target-`T` base class is already zero.
Thus

```text
b_S!=0  =>  b_T=0.                                    (2)
```

The six pair targets split into three complementary pairs, so at most three
pair base shadows survive.  If three survive, their supports form exactly a
three-edge star or a triangle in `K_4`.

Consequently the former `GLS17 -> GLD16` source premise consisting of all six
pair base shadows plus one four-port first-root shadow is empty.  No
root-companion-to-full-coefficient bridge is needed on that branch.  This does
not exclude non-leading pure-`M` pair selectors, arbitrary common lines in the
full `GLD15` operator spaces, promoted `GLS8` sources, other root orders, or
the branches with swallowed pair shadows.  The global Krenn--Gu conjecture
remains **UNRESOLVED**.

## Dependencies and scope

The complete joint module and its two desired labels are those of

- [`GLD15`](FIXED_Q_JOINT_MZ_MODULE_QUOTIENT_PAIRED_ATTACHMENT_AND_RANK_ONE_FIBRE_BOUNDARY_THEOREM.md).

The maximum-root base shadow, including every other order-two label in its
nuisance, is

- [`GLS16`](MAXIMAL_ROOT_SURPLUS_TWO_BASE_GRADE_PAIR_SHADOW_AND_CROSS_TARGET_SELECTOR_ANNIHILATION_THEOREM.md).

The affected conditional source route is

- [`GLS17`](MAXIMAL_ROOT_SURPLUS_TWO_PARTIAL_ROOT_GRADE_SHADOW_AND_COMMON_PURE_M_SELECTOR_THEOREM.md), followed by
- [`GLD16`](FIXED_Q_COMMON_PROJECTIVE_JOINT_RESPONSE_SELECTOR_AND_SHIFTED_GLD3_DETECTOR_THEOREM.md).

The coefficient-type correction in

- [`GLD67`](FIXED_Q_PRODUCT_SELECTOR_ROOT_COMPANION_FULL_COEFFICIENT_SEPARATION_AND_THREE_COLOUR_COUNTEREXAMPLE.md)

remains valid.  The present theorem avoids that interface entirely: it uses
only labelled order-two companion terms before any direct outside edge is
restored.  No external literature claim is used.

## 1. The complementary label inside the complete base nuisance

Work over a characteristic-zero field `K`.  Fix

```text
R={r_0,r_1,r_2,r_3},       Q={q_0,q_1},
U={u_0,u_1,u_2,u_3},       B=Q disjoint-union U.       (3)
```

Let `x_R` be fully supported maximum-root vectors and let `z_Q` be one fixed
fully supported residual contraction.  For a pair target `S subset U`, put

```text
C_S=U-S,
L_S^0=tensor_(u in C_S)V_u^*,
W_S=tensor_(s in S)V_s^*.                             (4)
```

The `GLS16` base companion is

```text
Pi_S(z_Q) in L_S^0,                                  (5)
```

the root-to-`Q union C_S` permanent after evaluating `R` at `x_R` and `Q`
at `z_Q`.  Let `N_S^0 subset L_S^0` be the complete base nuisance shadow and

```text
b_S=[Pi_S(z_Q)] in L_S^0/N_S^0.                      (6)
```

By definition, `N_S^0` retains the coefficient slices of every order-two
deck label `I!=S`.  No port-pair label is omitted merely because it is the
complement of `S`.

Fix the complementary pair

```text
T=U-S.                                                (7)
```

Then `C_S=T` and `C_T=S`, so

```text
L_S^0=tensor_(u in T)V_u^*,
Pi_T(z_Q) in tensor_(s in S)V_s^*=W_S.                (8)
```

### Theorem 1 (complementary-label saturation)

The order-two nuisance label `I=T` contributes, after maximum-root
evaluation and the `L_S^0|W_S` target factorization, the operator

```text
H_T |-> H_T tensor Pi_T(z_Q).                         (9)
```

Consequently

```text
Pi_T(z_Q)!=0  =>  N_S^0=L_S^0  =>  b_S=0.            (10)
```

#### Proof

For the deck label `I=T`, the universal companion coefficient is

```text
G_(B-T)=G_(Q union S).                                (11)
```

Maximum-root evaluation turns (11) into the root-to-`Q union S` permanent,
which is exactly `Pi_T(z_Q)` and has the open slots `S`.  The deck input
`H_T` has the complementary open slots `T`.  Since `T!=S`, this labelled
summand belongs to the target-`S` nuisance, and reordering the disjoint tensor
slots gives (9).

Assume `Pi_T(z_Q)!=0`.  Choose a target functional `eta in W_S^*` with

```text
eta(Pi_T(z_Q))=1.                                     (12)
```

For every `H_T in L_S^0`, the coefficient slice of (9) by `eta` is precisely

```text
(id tensor eta)(H_T tensor Pi_T(z_Q))=H_T.            (13)
```

The deck summand `I=T` ranges over the whole tensor space `L_S^0`, so (13)
puts every element of `L_S^0` in `N_S^0`.  The reverse inclusion is part of
the definition of the nuisance space.  Hence `N_S^0=L_S^0`, and (6) gives
`b_S=0`.  `square`

The proof uses the complete labelled deck domain.  Replacing it by one fixed
physical value of `H_T`, or slicing the wrong target/complement factor, would
not prove (10).

## 2. Complementary anti-simultaneity and the exact survivor atlas

### Corollary 1.1 (complementary pair shadows are mutually exclusive)

For every complementary pair partition `U=S disjoint-union T`,

```text
b_S!=0  =>  Pi_T(z_Q)=0  =>  b_T=0.                  (14)
```

In particular, `b_S` and `b_T` cannot both be nonzero.

#### Proof

The contrapositive of Theorem 1 gives the first implication.  If
`Pi_T(z_Q)=0`, then its quotient class (6), now in the target-`T` quotient,
is zero.  This is the second implication.  `square`

The six pairs of `U` are partitioned into the three complementary pairs

```text
{01,23},             {02,13},             {03,12}.    (15)
```

### Corollary 1.2 (at most three survivors; star/triangle boundary)

At most one member of each pair in (15) has nonzero base class.  Therefore

```text
#{S in binom(U,2): b_S!=0}<=3.                        (16)
```

If equality holds, the three surviving edges are either

1. the three edges incident to one port, or
2. the three edges of the triangle on the other three ports.

#### Proof

Corollary 1.1 gives the bound by choosing at most one edge from each of the
three pairs in (15).  Three pairwise noncomplementary edges of `K_4` are
pairwise intersecting.  If they share one vertex they form its star.  If
they do not share one vertex, any first two share a vertex and the third must
join their two remaining endpoints, giving the complementary triangle.
`square`

The statement classifies only which **base classes** can survive.  It is not
a classification of direct-edge support, response activity, operator-space
rank, or physical graph support.

## 3. Universal-bridge consequence

`GLS17` Corollary 2.2 used the conditional source hypothesis

```text
b_(empty,S)!=0 for all six pair targets S,
b_(a,U)!=0 for at least one root a.                   (17)
```

The pair part of (17) contradicts (16).  Hence the `GLS17` leading-shadow
route never supplies the all-seven pure-`M` package used by the subsequent
`GLD16` activity detector.

This resolves the immediate parent attempt created after `GLD67` in a way
that does not identify root companions `G_D` with full coefficients `F_D`:

```text
single four-port product row -> direct response control:      NOT OBTAINED;
all-six pair-base source plus that row:                        EMPTY;
maximum number of surviving pair base shadows:                THREE;
maximal survivor types:                                       STAR/TRIANGLE;
at least one swallowed shadow in every complementary pair:    PROVED.       (18)
```

The result does not say that a target with `b_S=0` has no non-leading legal
row.  It also does not exclude a common vector in all seven full operator
spaces that is supplied by another grade, nor does it turn the three
swallowed complementary circuits into mixed GHZ coefficients.  Those are the
new load-bearing universal obligations.

## 4. Parent-theorem checkpoint and proof-distance delta

The serious parent proposition under attack was:

> On an actual root-order-four maximum-root surplus-two witness, combine all
> six surviving pair base shadows with one surviving four-port first-root
> shadow, and use a genuine full-target, second-axis, or coefficient-pure
> bridge to constrain the direct port responses strongly enough to enter a
> named detector.

Theorem 1 checks the source interface before choosing a detector.  A
complementary pair's desired raw companion is exactly a complete nuisance
label for the other target, and at four ports there are no exterior slots to
prevent its slices from saturating the whole receiver.  Thus the six-shadow
premise is self-inconsistent.

The proof-topology change is exact but limited:

- the all-six base-shadow source edge into `GLD16` is removed;
- every fixed-`Q`, root-order-four point has at least three swallowed pair
  shadows, one from each complementary pair;
- the maximal surviving base patterns reduce to eight labelled star/triangle
  choices; and
- the next parent attempt must exploit the swallowed circuits or obtain legal
  pair rows from a non-leading source.

No global resolution or numerical proof-distance claim follows.  The global
conjecture remains **UNRESOLVED**.

## Verification

Run from the repository root:

```powershell
python claims/arbitrary-order/verify_four_root_complementary_pair_base_nuisance_saturation.py
python -I claims/arbitrary-order/audit_four_root_complementary_pair_base_nuisance_saturation.py
```

The primary replay constructs the exact coefficient-slice matrices for every
ordered complementary pair at local dimensions one through four, verifies
that every nonzero companion coordinate supplies an identity block spanning
the whole receiver, and exhausts all `64` survivor masks.  The independent
no-import audit instead constructs the dual slice explicitly from the first
nonzero companion coordinate, recovers every receiver basis vector, and
classifies the eight maximal survivor families as four stars and four
triangles.  The arbitrary-field tensor-factor argument is the written proof.
