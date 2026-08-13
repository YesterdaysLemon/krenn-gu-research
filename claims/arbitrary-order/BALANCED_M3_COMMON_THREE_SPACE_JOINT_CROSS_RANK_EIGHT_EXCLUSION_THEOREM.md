# Balanced `m=3` common-three-space joint-cross-rank-eight exclusion

## Status

**Exact characteristic-zero exclusion of joint cross rank eight on the S2Q
common-three-space stratum.**  Let `U` be the total singleton span of a
normalized, target-consistent physical `m=3` common shore, assume

```text
dim U=3,                                                (1)
```

and let

```text
H:X direct-sum Y direct-sum Z
  -> A_1 direct-sum A_2 direct-sum A_3                 (2)
```

be the joint `9 x 9` root--nonroot cross-colour map.  Then

```text
rank H !=8.                                             (3)
```

Together with S2X, which excludes rank nine, every surviving
common-three-space incidence satisfies

```text
rank H<=7.                                              (4)
```

This is a strict local frontier advance, not a resolution.  Joint rank at
most seven, the multi-boundary, `beta=0`, and collapsed cross-column
component types, the rank-one and pair-plane pole strata, every higher order,
the all-balanced branch, a witness, and a counterexample remain open.  Global
Krenn--Gu remains **UNRESOLVED**.

## 1. A hyperplane cannot hide two root blocks

Let `D_B` be the shared derivative of the three root--root blocks, as in
S2U.  The singleton span is

```text
U=image(D_B H).                                        (5)
```

If `rank H=8`, its image `K` is a hyperplane in the nine-dimensional domain
of `D_B`, and

```text
rank(D_B restricted to K)=3.                           (6)
```

For every linear map `f` and every codimension-one subspace `K`,

```text
rank(f restricted to K)>=rank(f)-1.                    (7)
```

Two nonzero root blocks make `rank D_B>=5` by the pairwise shared-factor
intersection lemma in S2U.  Equations (6)--(7) would then give rank at least
four, a contradiction.  Since (6) is nonzero, exactly one root--root block
survives.

After permuting roots, write it as `B_23`.  Then

```text
U=A_1 tensor B_23.                                     (8)
```

The S2R torus obstruction and its bilinear torus-zero lemma force `B_23` to
be one coordinate monomial.  The explicit pair globalization in S2U uses no
invertibility of `H`; it excludes an off-diagonal monomial by reconstructing
a forbidden six-vertex graph.  Hence for one target colour `s`,

```text
B_23=lambda e_(2,s) tensor e_(3,s),
U=A_1 tensor e_(2,s) tensor e_(3,s).                   (9)
```

The physical empty equation now has exactly the same sparse form as S2U:

```text
G_N in J+U.                                            (10)
```

In particular all eighteen output rows `(a,b,c)` with `b!=c` vanish, while
the two diagonal colours `t!=s` retain their full GHZ rows.

## 2. The exceptional root row is a full-support three-plane

Let

```text
R=span(r_0,r_1,r_2) subset X direct-sum Y direct-sum Z (11)
```

be the row space of the exceptional root-1 block row of `H`.  Formula (9)
makes the three singleton columns

```text
H_(1,x)x tensor e_s tensor e_s,
H_(1,y)y tensor e_s tensor e_s,
H_(1,z)z tensor e_s tensor e_s.                       (12)
```

A physical full sensor makes these columns generically independent.  Thus
the row block has rank three and each source projection of `R` is nonzero.

For a quadratic triple

```text
Q=(A in Y tensor Z,
   B in X tensor Z,
   C in X tensor Y),                                  (13)
```

write

```text
Phi_R(Q):R -> X tensor Y tensor Z,
(x,y,z) |-> x tensor A+B tensor y+C tensor z.          (14)
```

If `p_b,q_c` are rows of the root-2 and root-3 block rows, let

```text
p_b*q_c=(
 p_(b,Y) tensor q_(c,Z)+q_(c,Y) tensor p_(b,Z),
 p_(b,X) tensor q_(c,Z)+q_(c,X) tensor p_(b,Z),
 p_(b,X) tensor q_(c,Y)+q_(c,X) tensor p_(b,Y)).       (15)
```

The off-diagonal rows of (10) say

```text
Phi_R(p_b*q_c)=0                         for b!=c.     (16)
```

The derivative-kernel dichotomy proved in S2X applies because all three
source projections of `R` are nonzero:

```text
Phi_R is injective;                                    (17a)
or, after source permutations and basis changes,
R=span(x+y+epsilon z_0,z_1,z_2), epsilon in {0,1}.     (17b)
```

We exclude both alternatives.

## 3. A six-row off-diagonal zero grid spans at most four

In the injective case, (16) gives

```text
p_b*q_c=0                                for b!=c.     (18)
```

We use the following exact degree-one zero-divisor lemma.

### Lemma 1 (three-source zero divisors)

For nonzero `q=(q_X,q_Y,q_Z)` in `X direct-sum Y direct-sum Z`, put

```text
Z(q)={p:p*q=0}.                                        (19)
```

Then

```text
q uses one source S:    Z(q)=S,                       dim 3;
q uses exactly S,T:     Z(q)=span(q_S-q_T),           dim 1;
q uses all three:       Z(q)=0.                       (20)
```

### Proof

The three equations are

```text
p_S tensor q_T+q_S tensor p_T=0                       (21)
```

for the source pairs.  With one source, tensoring by its nonzero component
kills every other component of `p` and leaves the same source free.  With
two sources, equality of nonzero rank-one tensors gives the one sign-flipped
line in (20).  With three sources, the three proportionalities have signs
whose product is negative; characteristic different from two forces the
common scalar to vanish.  QED.

### Lemma 2 (off-diagonal grid bound)

If six vectors `p_0,p_1,p_2,q_0,q_1,q_2` satisfy (18), then

```text
dim span(p_0,p_1,p_2,q_0,q_1,q_2)<=4.                 (22)
```

### Proof

Classify by the number of nonzero `q` rows.

- With none, only the three `p` rows remain.
- With one nonzero `q`, two `p` rows lie in `Z(q)` and the third is free.
  Formula (20) gives bounds four, three, and two according as `q` uses one,
  two, or three sources.
- With two nonzero `q` rows, the two paired `p` rows lie in their respective
  zero-divisor spaces and the third lies in their intersection.  Two pure
  zero divisors on the same source give dimension at most three; on distinct
  sources they give at most two dimensions in each source.  A pure and a
  mixed zero-divisor space intersect trivially.  Two mixed spaces are lines
  and intersect only when the lines agree.  If either `q` uses all three
  sources its zero-divisor space is zero.  Every subcase has dimension at
  most four.
- With all three `q` rows nonzero, a full-support row kills two `p` rows.  If
  all are pure, the source labels are either all equal, `2+1`, or all
  distinct, giving bounds three, four, and three.  For three mixed rows, a
  `p` row can survive only when the other two zero-divisor lines agree; all
  three equal lines also make the corresponding `q` rows proportional.  A
  mixture of pure and mixed rows has zero intersection across the two types.
  Again the bound is four.

These cases are exhaustive by Lemma 1.  Equality is sharp: take `q_0,p_1`
independent in `X`, `q_1,p_0` independent in `Y`, and set `p_2=q_2=0`.
QED.

Since the rows of `H` are the union of `R`, the `p` rows, and the `q` rows,
Lemmas 1--2 give

```text
rank H<=dim R+dim span(P,Q)<=3+4=7,                   (23)
```

contradicting rank eight.  Thus (17a) is impossible.

## 4. The exceptional derivative has only one rank-one covector

Assume (17b) and put

```text
S=R intersect Z=span(z_1,z_2),              dim S=2. (24)
```

For a quadratic triple `(A,B,C)`, restriction of (14) to `S` is

```text
z |-> C tensor z.                                      (25)
```

If `C!=0`, this map has rank two.  Therefore every nonzero rank-one map
`Phi_R(A,B,C)` must have `C=0` and must kill `S`.  Its coefficient covector
on `R` lies in

```text
S^perp subset R^*,                         dim S^perp=1. (26)
```

For each of the two colours `t!=s`, the fixed diagonal target row in (10)
says

```text
Phi_R(p_t*q_t)(r_a)
 =delta_(a,t) x_t tensor y_t tensor z_t.               (27)
```

These are two nonzero rank-one maps.  Their coefficient covectors are two
distinct coordinate covectors on the basis `(r_0,r_1,r_2)` and are therefore
independent.  Equation (26) says both must lie on one line, the final
contradiction.

This excludes (17b) and proves (3).

## 5. Proof-topology consequence

The exact common-three-space rank frontier is now

```text
rank H=9:                       IMPOSSIBLE (S2X);
rank H=8:                       IMPOSSIBLE (here);
rank H<=7:                      OPEN;
other S2T component types:     OPEN;
other S2Q strata / m>=4:       OPEN;
global Krenn--Gu conjecture:   UNRESOLVED.             (28)
```

At rank seven, a codimension-two image can reduce a five-dimensional
two-root-block derivative to dimension three, and the regular zero-grid bound
(23) is sharp.  Those two equality mechanisms are the next exact cases; this
theorem does not silently exclude them.

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_cross_rank_eight_exclusion.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_cross_rank_eight_exclusion.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_cross_rank_eight_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_cross_rank_eight_exclusion.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_cross_rank_eight_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_cross_rank_eight_exclusion.py
```

The primary replay checks sharp hyperplane rank loss, the three zero-divisor
orbits, all sixteen support-type budgets and a rank-four equality control,
both exceptional derivative charts, and the one-versus-two covector ranks.
The independent no-import audit uses its own `Fraction` row reduction and
separately reconstructs the same sharp boundaries.  The rank-one tensor
arguments and exhaustive support proof above establish the theorem over
characteristic zero.

## Dependencies

- [`BALANCED_M3_COMMON_THREE_SPACE_FULL_JOINT_CROSS_RANK_MONOMIAL_ROOT_EDGE_LOCALIZATION_THEOREM.md`](BALANCED_M3_COMMON_THREE_SPACE_FULL_JOINT_CROSS_RANK_MONOMIAL_ROOT_EDGE_LOCALIZATION_THEOREM.md)
- [`BALANCED_M3_COMMON_THREE_SPACE_FULL_JOINT_CROSS_RANK_EXCLUSION_THEOREM.md`](BALANCED_M3_COMMON_THREE_SPACE_FULL_JOINT_CROSS_RANK_EXCLUSION_THEOREM.md)
