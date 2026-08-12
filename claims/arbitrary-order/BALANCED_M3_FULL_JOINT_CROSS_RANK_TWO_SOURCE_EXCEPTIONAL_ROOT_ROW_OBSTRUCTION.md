# Balanced `m=3` two-source exceptional-root-row obstruction

## Status

**Exact characteristic-zero exclusion inside the S2U sparse
block-permanent branch.**  Retain the S2U normal form

```text
U=A_1 tensor e_(2,s) tensor e_(3,s),
G_N in J + U,                                           (1)
```

and let `R_1` be the row space of the exceptional root block row of the
invertible joint cross map

```text
H:(X direct-sum Y direct-sum Z)
  -> A_1 direct-sum A_2 direct-sum A_3.                 (2)
```

Then `R_1` is not contained in any sum of two source summands.  This includes
the source-aligned case and every rank profile and graph chart inside, for
example, `X direct-sum Y`.

This is a subcase exclusion, not a proof of the full block-permanent rank
floor.  It leaves only exceptional rows with nonzero projection to all three
source summands at full joint rank.  Joint rank at most eight, other S2Q
strata, all higher orders, a witness, and a counterexample remain open.
Global Krenn--Gu remains **UNRESOLVED**.

## 1. Off-diagonal rows split into two mixed products

Assume, after permuting the source summands, that

```text
R_1 subset X^* direct-sum Y^*.                         (3)
```

Write the three root-2 and three root-3 rows as

```text
p_b=(p_bX,p_bY,p_bZ),
q_c=(q_cX,q_cY,q_cZ).                                 (4)
```

Every target word with `b!=c` vanishes in (1).  The corresponding
block-permanent row, restricted to `R_1`, is

```text
(r_X,r_Y) |->
 r_X tensor (p_bY tensor q_cZ+q_cY tensor p_bZ)
+r_Y tensor (p_bX tensor q_cZ+q_cX tensor p_bZ).       (5)
```

for all `b!=c`.

### Lemma 1 (two-source splitting)

If a three-plane `R subset X^* direct-sum Y^*` is neither `X^*` nor `Y^*`,
then

```text
x tensor u+v tensor y=0 for every (x,y) in R           (6)
```

forces `u=v=0`.

### Proof

Separate basis changes put every three-plane in the normal form

```text
X_0 direct-sum Y_0 direct-sum span(x_i+y_i:1<=i<=t),
dim X_0+dim Y_0+t=3,                                  (8)
```

If `X_0` is nonzero, a pure-X generator first gives `u=0`; a pure-Y or
diagonal generator then gives `v=0`.  The symmetric argument handles
nonzero `Y_0`.  If both are zero, there are three independent diagonal
generators; equality of rank-one tensors for any one generator makes `u`
and `v` proportional to that generator, and a second generator forces both
to vanish.  The only exceptions are the two pure normal forms `R=X^*` and
`R=Y^*`, which are exactly the source-aligned cases already excluded by the
preceding theorem.  QED.

If `R_1` is a pure source summand, the source-aligned theorem already gives a
contradiction.  Otherwise applying Lemma 1 to (5) gives the two independent
equations

```text
p_bX tensor q_cZ+q_cX tensor p_bZ=0,
p_bY tensor q_cZ+q_cY tensor p_bZ=0                   (9)
```

for `b!=c`.

## 2. One `(6+3)` mixed-product zero grid

Put

```text
S=X^* direct-sum Y^*,
P_b=(p_bX,p_bY,p_bZ) in S direct-sum Z^*,
Q_c=(q_cX,q_cY,q_cZ) in S direct-sum Z^*.             (10)
```

The two equations in (9) concatenate to

```text
m(P_b,Q_c)=0 for b!=c,                                (11)
```

where

```text
m((s,z),(t,w))=s tensor w+t tensor z in S tensor Z^*. (12)
```

### Lemma 2 (pure-or-line zero divisor)

For nonzero `Q=(t,w)`, its zero-divisor space under (12) is

```text
S,                    if w=0;
Z^*,                  if t=0;
span((t,-w)),          if t!=0 and w!=0.               (13)
```

The proof is the equality classification of two rank-one tensors, exactly
as in the source-aligned theorem.

Because `H` is invertible, the six rows `P_0,P_1,P_2,Q_0,Q_1,Q_2` are
independent.  For fixed `c`, the two `P_b`, `b!=c`, are independent and lie
in `Z(Q_c)`.  Lemma 2 therefore makes every `Q_c` pure in the decomposition
`S direct-sum Z^*`.

Two of the three `Q_c` lie in the same summand.  Their off-diagonal equations
force all three `P_b` into that summand.  If all `Q_c` lie there, the six
vectors cannot be independent because the relevant summand has dimension at
most six and already contains the three independent `P_b`, while the
complementary root row `R_1` occupies a nonzero subspace of `S`.  If the
third `Q_c` lies in the other summand, its two off-diagonal equations force
two of the `P_b` into both summands, hence make them zero.  Both cases
contradict invertibility.  This proves the theorem.

## 3. Proof-topology consequence

The full-joint-rank residue is now

```text
invertible monomial H:                              IMPOSSIBLE (S2U);
exceptional root row on one or two sources:         IMPOSSIBLE (here);
exceptional root row supported on all three sources: OPEN;
joint cross rank <=8:                                OPEN;
global Krenn--Gu conjecture:                          UNRESOLVED.        (14)
```

The next exact local obligation is the fully supported exceptional-row
chart.  A proof there must control three coupled mixed products rather than
the single `(6+3)` product used here.

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_full_joint_cross_rank_two_source_exceptional_root_row_obstruction.py
python -I claims/arbitrary-order/audit_balanced_m3_full_joint_cross_rank_two_source_exceptional_root_row_obstruction.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_full_joint_cross_rank_two_source_exceptional_root_row_obstruction.py claims/arbitrary-order/audit_balanced_m3_full_joint_cross_rank_two_source_exceptional_root_row_obstruction.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_full_joint_cross_rank_two_source_exceptional_root_row_obstruction.py claims/arbitrary-order/audit_balanced_m3_full_joint_cross_rank_two_source_exceptional_root_row_obstruction.py
```

The primary replay checks all ten two-source normal forms, the exact
nullities `6,3,1` for the `(6+3)` mixed product, the eight purity patterns,
and the concatenation (9)--(12).  The independent no-import audit enumerates
all 511 nonzero binary vectors of the nine-space and all 1395 binary
three-planes in the six-space, and separately audits the purity pigeonhole.
The written tensor argument establishes characteristic zero.

## Dependencies

- [`BALANCED_M3_COMMON_THREE_SPACE_FULL_JOINT_CROSS_RANK_MONOMIAL_ROOT_EDGE_LOCALIZATION_THEOREM.md`](BALANCED_M3_COMMON_THREE_SPACE_FULL_JOINT_CROSS_RANK_MONOMIAL_ROOT_EDGE_LOCALIZATION_THEOREM.md)
- [`BALANCED_M3_FULL_JOINT_CROSS_RANK_SOURCE_ALIGNED_EXCEPTIONAL_ROOT_ROW_OBSTRUCTION.md`](BALANCED_M3_FULL_JOINT_CROSS_RANK_SOURCE_ALIGNED_EXCEPTIONAL_ROOT_ROW_OBSTRUCTION.md)
