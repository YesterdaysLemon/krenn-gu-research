# Balanced `m=3` common-three-space single-root-block complete exclusion

## Status

**Exact characteristic-zero exclusion of the entire single-root-block part of
the S2Q common-three-space stratum.**  Let `U` be the total singleton span of
a normalized, target-consistent physical `m=3` common shore and assume

```text
dim U=3.                                                (1)
```

It is impossible for exactly one of the three root--root blocks to be
nonzero, at any rank of the joint root--nonroot cross-colour map `H`.

Together with S2X--S2AA, every surviving common-three-space incidence now
satisfies

```text
rank H<=6,
at least two root--root blocks are nonzero.             (2)
```

This excludes one physical component, not the common-three-space stratum.
The multi-root rank-at-most-six locus, the other multi-boundary, `beta=0`,
and collapsed cross-column components, the rank-one and pair-plane pole
strata, every higher order, the all-balanced branch, a witness, and a
counterexample remain open.  Global Krenn--Gu remains **UNRESOLVED**.

## 1. The universal single-root sparse equation

After permuting roots, let `B_23` be the unique nonzero root--root block.
The shared derivative formula gives

```text
U=image(H_1) tensor B_23.                              (3)
```

Equation (1) forces the aggregate root-1 block row `H_1` to have rank three.
Physical full-sensor rank also makes each of its three source projections
nonzero: if the root-1 cross block at one nonroot vanished, that singleton
sensor column would vanish.

The S2R torus obstruction forces `B_23` to be a coordinate monomial, and the
S2U pair globalization excludes an off-diagonal monomial without using the
rank of `H`.  Hence, for one target colour `s`,

```text
B_23=lambda e_(2,s) tensor e_(3,s),
U=A_1 tensor e_(2,s) tensor e_(3,s),                  (4)

G_N in J+U.                                            (5)
```

Write the three block-row bases of `H` as

```text
R=(r_0,r_1,r_2),      P=(p_0,p_1,p_2),
Q=(q_0,q_1,q_2)       in W=X direct-sum Y direct-sum Z. (6)
```

The rows `R` are independent and their projections to all three sources are
nonzero.  For the polarized three-source pair product `p*q` and its shared
derivative `Phi_R`, equation (5) gives

```text
Phi_R(p_b*q_c)=0                         for b!=c,    (7)
Phi_R(p_v*q_v)=ell_v tensor T_v          for v!=s,   (8)
```

where

```text
ell_v(r_a)=delta_(a,v),
T_v=X_v tensor Y_v tensor Z_v.                         (9)
```

The two maps in (8) are nonzero rank-one maps, their coefficient covectors
are independent, and their three target factor lines are distinct in every
source.

The S2X derivative-kernel dichotomy applies to `R`.  Its exceptional chart is
already incompatible with (8): S2Y proves that every nonzero rank-one
restriction there uses one fixed coefficient-covector line.  We may therefore
assume the regular chart, where `Phi_R` is injective and

```text
p_b*q_c=0                                 for b!=c.   (10)
```

No rank hypothesis on `H` has been used.

## 2. Only two crossed zero-product pairs remain

Let `t,u` be the two colours different from `s`.  Equation (8) makes

```text
p_t,q_t,p_u,q_u nonzero,
p_t*q_t!=0,                 p_u*q_u!=0.               (11)
```

### Lemma 1 (the exceptional marked rows vanish)

Under (10)--(11),

```text
p_s=q_s=0.                                             (12)
```

### Proof

If `p_s!=0`, then it is a common zero divisor of `q_t,q_u`.  By the S2Y
zero-divisor classification, either both `q` rows are pure in the same
source, or both are proportional mixed rows on the same source pair.  In the
first case `p_t*q_u=0` puts `p_t` in that same source and makes
`p_t*q_t=0`; in the second, proportionality gives the same conclusion.
Both contradict (11).  Thus `p_s=0`, and symmetry gives `q_s=0`.  QED.

The only off-diagonal equations left are

```text
p_t*q_u=0,                       p_u*q_t=0.            (13)
```

Every nonzero zero-product pair has one of two exact forms:

```text
P_S: both vectors lie in one source S;
M_ST: after rescaling, the marked vectors are a+b and a-b,
      with 0!=a in S, 0!=b in T, S!=T.                (14)
```

The pure pair may span a line or a plane; the mixed pair always spans its
two factor lines.  Thus the unordered pair of crossed forms in (13) is one
of `P/P`, `P/M`, or `M/M`.

## 3. Pure cases are impossible

### Case P/P

The two pure pairs must occupy different sources, or a diagonal product in
(11) would vanish.  Both diagonal quadratic triples consequently occupy the
same source pair.  Their derivatives depend only on the projection of `R`
to the third source.  Rank one for either map forces that projection to be a
line, so both derivatives use the same coefficient covector on `R`.  This
contradicts the independent covectors `ell_t,ell_u`.

### Case P/M with a shared source

If the pure source is one of the two mixed sources, both diagonal products
again occupy the same source pair.  The same missing-source projection gives
the common-covector contradiction.

### Case P/M on all three sources

After permuting sources and rescaling, write

```text
p_t=a_0,             q_u=a_1              in X,
q_t=b+c,             p_u=b-c,
0!=b in Y,           0!=c in Z.                        (15)
```

The two diagonal target tensors have independent `X` factor lines, so
`a_0,a_1` are independent.  On `Y direct-sum Z`, their derivatives reduce to

```text
L_+(y,z)= y tensor c+b tensor z,
L_-(y,z)=-y tensor c+b tensor z.                       (16)
```

The pair `(L_+,L_-)` is injective.  If `V` is the projection of `R` to
`Y direct-sum Z`, the two independent rank-one maps in (8) therefore give
`dim V=2`.  Rank one of each restriction makes `V` contain the two distinct
kernel lines

```text
span(b,-c),                     span(b,c).             (17)
```

Both restricted images are then the same line `span(b tensor c)`.  The two
target tensors would share their `Y` and `Z` factor lines, contradicting
`t!=u`.  This excludes P/M, including the possible one-dimensional pure
pair.

## 4. Mixed cases are impossible

### Case M/M on the same source pair

Normalize the crossed pairs as

```text
p_t=a+b,       q_u=a-b,
p_u=c+d,       q_t=c-d.                               (18)
```

Direct expansion gives

```text
p_t*q_t=-(p_u*q_u)                                    (19)
```

up to the nonzero normalization scalars.  The two derivative maps are
proportional, contradicting (8).

### Case M/M on different source pairs, transverse shared lines

After permuting sources, put

```text
p_t=a+b,       q_u=a-b,       a in X, b in Y,
p_u=c+d,       q_t=c-d,       c in X, d in Z.         (20)
```

If `a,c` are independent, the two diagonal derivatives have zero common
kernel on `W`.  Their sum first kills the `X` component; their difference
then separates the independent factors `a,c` and kills the `Y,Z` components.
The combined restriction to the three-plane `R` therefore has rank three.
But (8) expresses it as two rank-one maps, of combined rank at most two.
Contradiction.

### Case M/M on different source pairs, one shared line

It remains that `a,c` are proportional; rescale them to one vector `a`.
Both diagonal derivatives now take values in the Segre tangent space

```text
T_0=X tensor b tensor d
    +a tensor Y tensor d
    +a tensor b tensor Z.                             (21)
```

We use the elementary rank-one locus of this tangent space.

### Lemma 2 (decomposables in a Segre tangent space)

Every nonzero decomposable tensor in `T_0` belongs to one of its three
rulings in (21); equivalently, it shares at least two of the factor lines
`a,b,d`.

### Proof

Let `x tensor y tensor z` belong to `T_0`.  Projecting simultaneously modulo
`a,b`, modulo `a,d`, and modulo `b,d` gives respectively

```text
x parallel a or y parallel b,
x parallel a or z parallel d,
y parallel b or z parallel d.                        (22)
```

The three pairwise alternatives force at least two of the three displayed
parallelisms.  This is exactly membership in one ruling.  QED.

Both target lines `T_t,T_u` in (8) lie in `T_0`.  Lemma 2 makes each share
at least two of `a,b,d`.  Two two-element subsets of three modes intersect,
so `T_t,T_u` would share a factor line in at least one source.  Distinct GHZ
colours share none.  This final contradiction excludes M/M.

## 5. Proof-topology consequence

The cases in Sections 3--4 exhaust (14), so the single-root-block branch is
empty independently of `rank H`.  Combining this with the rank-nine,
rank-eight, and complete rank-seven exclusions gives

```text
common-three-space, exactly one root block:  IMPOSSIBLE;
common-three-space, joint rank >=7:          IMPOSSIBLE;
common-three-space, >=2 root blocks,
  joint rank <=6:                            OPEN;
other S2T component types / S2Q strata:     OPEN;
global Krenn--Gu conjecture:                UNRESOLVED.             (23)
```

The four-dimensional zero-grid bound in S2Y remains sharp as an abstract
grid.  What closes the entire physical single-root branch is the pair of
fixed diagonal GHZ rows, including the lower-dimensional and tangent-line
boundaries that were unnecessary in the rank-seven equality theorem.

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_single_root_block_complete_exclusion.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_single_root_block_complete_exclusion.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_single_root_block_complete_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_single_root_block_complete_exclusion.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_single_root_block_complete_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_single_root_block_complete_exclusion.py
```

The primary replay checks the six pure/mixed crossed-pair families, the two
P/M kernel lines, proportional same-pair M/M products, transverse
different-pair injectivity, and the shared-line tangent boundary.  The
independent no-import audit reconstructs the derivatives and tangent
projections with `Fraction` arithmetic.  Lemmas 1--2 and the arbitrary-vector
case analysis above are the characteristic-zero proof.

## Dependencies

- [`BALANCED_M3_COMMON_THREE_SPACE_SINGLE_ROOT_BLOCK_JOINT_CROSS_RANK_SEVEN_EXCLUSION_THEOREM.md`](BALANCED_M3_COMMON_THREE_SPACE_SINGLE_ROOT_BLOCK_JOINT_CROSS_RANK_SEVEN_EXCLUSION_THEOREM.md)
- [`BALANCED_M3_COMMON_THREE_SPACE_TWO_ROOT_BLOCK_JOINT_CROSS_RANK_SEVEN_EXCLUSION_THEOREM.md`](BALANCED_M3_COMMON_THREE_SPACE_TWO_ROOT_BLOCK_JOINT_CROSS_RANK_SEVEN_EXCLUSION_THEOREM.md)
