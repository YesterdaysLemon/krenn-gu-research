# Balanced `m=3` common-three-space single-root-block joint-rank-seven exclusion

## Status

**Exact characteristic-zero exclusion of joint cross rank seven on the
single-root-block part of the S2Q common-three-space stratum.**  Let `U` be
the total singleton span of a normalized, target-consistent physical `m=3`
common shore, assume

```text
dim U=3,                                                (1)
```

and suppose exactly one of the three root--root blocks is nonzero.  If

```text
H:X direct-sum Y direct-sum Z
  -> A_1 direct-sum A_2 direct-sum A_3                 (2)
```

is the joint root--nonroot cross-colour map, then

```text
rank H !=7.                                             (3)
```

Together with S2X--S2Y, ranks nine and eight are impossible without the
single-root-block hypothesis.  The remaining rank-seven common-three-space
case must therefore use at least two nonzero root--root blocks.  Joint rank
at most six, that two-root-block rank-seven boundary, the other S2T component
types, the rank-one and pair-plane pole strata, every higher order, the
all-balanced branch, a witness, and a counterexample remain open.  Global
Krenn--Gu remains **UNRESOLVED**.

## 1. The single root block still gives the sparse equation

After permuting roots, let `B_23` be the unique nonzero root--root block.
The shared-factor formula is

```text
U=image(D_B H)=image(H_1) tensor B_23.                 (4)
```

The three physical singleton columns are independent over the function
field.  Hence the first root block row `H_1` has rank three, and each of its
three source blocks is nonzero.  Equation (1) therefore gives

```text
U=A_1 tensor B_23.                                     (5)
```

The S2R torus-annihilator theorem now applies exactly as in S2U: `B_23` is
one coordinate monomial.  The explicit pair globalization in S2U does not
use invertibility of `H`, so an off-diagonal monomial would reconstruct a
forbidden six-vertex graph.  Thus, for one colour `s`,

```text
B_23=lambda e_(2,s) tensor e_(3,s),
U=A_1 tensor e_(2,s) tensor e_(3,s),                  (6)
```

and the empty companion obeys

```text
G_N in J+U.                                            (7)
```

Let

```text
R=span(r_0,r_1,r_2)
```

be the row space of `H_1`, and write the other two marked block rows as
`P=(p_0,p_1,p_2)` and `Q=(q_0,q_1,q_2)`.  The vectors lie in

```text
W=X direct-sum Y direct-sum Z.                        (8)
```

For `p,q in W`, write `p*q` for their three polarized cross-source products,
and let

```text
Phi_R(p*q)(r)=per(r,p,q)                              (9)
```

be the corresponding shared derivative restricted to `R`.  Equation (7)
gives

```text
Phi_R(p_b*q_c)=0                         for b!=c,    (10)
Phi_R(p_t*q_t)=ell_t tensor T_t          for t!=s,   (11)
```

where `ell_t(r_a)=delta_(a,t)` and

```text
T_t=x_t tensor y_t tensor z_t.                        (12)
```

The two covectors `ell_t`, `t!=s`, are independent, both maps in (11) have
rank one, and the two target tensors have distinct factor lines in every
source.

Every source projection of `R` is nonzero.  The derivative-kernel dichotomy
of S2X therefore applies.  In its exceptional chart, S2Y proves that every
nonzero rank-one restriction has its coefficient covector on one fixed
line; this contradicts the two independent covectors in (11).  It remains
only to exclude the regular chart, in which `Phi_R` is injective and (10)
becomes

```text
p_b*q_c=0                                 for b!=c.   (13)
```

## 2. Equality in the off-diagonal zero grid

We use the S2Y zero-divisor classification.  For nonzero `q in W`,

```text
Z(q)={p:p*q=0}                                         (14)
```

is the whole source summand when `q` is pure, the one conjugate line when
`q` uses exactly two sources, and zero when `q` uses all three sources.

Let `t,u` be the two colours different from `s`.  Equation (11) makes

```text
p_t,q_t,p_u,q_u nonzero,
p_t*q_t !=0,                  p_u*q_u !=0.             (15)
```

### Lemma 1 (rank-four marked-grid normal forms)

If (13), (15), and

```text
dim span(P,Q)=4                                        (16)
```

hold, then

```text
p_s=q_s=0.                                             (17)
```

Moreover the two planes

```text
E=span(p_t,q_u),             F=span(p_u,q_t)           (18)
```

are complementary two-planes.  Each is exactly one of:

```text
P_S: a two-plane contained in one source S;
M_ST: span(a,b), with 0!=a in S, 0!=b in T, S!=T,
      and its two marked vectors proportional to a+b and a-b.  (19)
```

### Proof

Suppose `p_s!=0`.  Then `p_s` belongs to `Z(q_t) intersect Z(q_u)`.  A
nonzero intersection can occur only when `q_t,q_u` are pure in the same
source or when they are proportional two-source vectors.  In the first
case, `p_t*q_u=0` puts `p_t` in that same source, making `p_t*q_t=0`.  In the
second case, `p_t*q_u=0` also gives `p_t*q_t=0`.  Both contradict (15), so
`p_s=0`.  The symmetric argument gives `q_s=0`.

The span in (16) is therefore `E+F`.  Each marked zero-product pair spans at
most two dimensions.  Equality four makes both dimensions two and makes
their intersection zero.  The pure-or-conjugate-line classification of a
nonzero zero-product pair is exactly (19).  QED.

The four dimensions in Lemma 1 are sharp before the diagonal target rows
are imposed.  For instance, one may take

```text
p_t,q_u in X independent,
p_u,q_t in Y independent,
p_s=q_s=0.                                             (20)
```

The rest of the proof shows that none of the three unordered combinations
`P/P`, `P/M`, and `M/M` can also satisfy (11).

## 3. Pure/pure and pure/mixed equality are impossible

### Case P/P

Let `E` lie in source `S` and `F` in source `T`.  The diagonal products in
(15) force `S!=T`.  Both `p_t*q_t` and `p_u*q_u` then lie in `S tensor T`,
so their derivative maps depend only on the projection of `R` to the third
source `V`:

```text
r |-> C_i tensor pi_V(r),                 i=t,u.      (21)
```

Because both restrictions have rank one, `pi_V(R)` is one-dimensional.
The two maps in (21) consequently use the same scalar covector on `R`,
contradicting the independence of `ell_t,ell_u`.

### Case P/M with a shared source

Suppose the pure plane lies in one of the two sources supporting the mixed
plane.  Both diagonal products again lie in the same source pair.  Equation
(21), with the remaining source as `V`, gives the same common-covector
contradiction.

### Case P/M on all three sources

After permuting sources and rescaling marked vectors, write

```text
p_t=a_0,             q_u=a_1             in X,
q_t=b+c,             p_u=b-c,
0!=b in Y,           0!=c in Z.                       (22)
```

The plane `E` makes `a_0,a_1` independent.  On `Y direct-sum Z`, the two
diagonal derivatives are, up to the fixed factors `a_0,a_1`,

```text
L_+(y,z)= y tensor c+b tensor z,
L_-(y,z)=-y tensor c+b tensor z.                      (23)
```

The combined map `(L_+,L_-)` is injective, since its sum and difference
recover `b tensor z` and `y tensor c`.  Put

```text
V=projection_(Y direct-sum Z)(R).                     (24)
```

The two independent coefficient covectors in (11) make the combined
restriction have rank two.  Thus `dim V=2`.  Each of `L_+|V,L_-|V` has rank
one, so `V` contains their two global kernel lines

```text
span(b,-c),                    span(b,c).              (25)
```

These lines are distinct in characteristic zero and span
`span((b,0),(0,c))`.  Both images in (23) are therefore the same tensor line
`span(b tensor c)`.  The two target tensors in (12) would share their `Y`
and `Z` factor lines, contrary to `t!=u`.

This excludes every P/M configuration.

## 4. Mixed/mixed equality is impossible

### Case M/M on the same source pair

Normalize the two complementary marked planes as

```text
p_t=a+b,       q_u=a-b,
p_u=c+d,       q_t=c-d,                               (26)
```

where `a,c` lie in one source and `b,d` in the other.  Directness of the
planes makes the diagonal product nonzero, and direct expansion gives

```text
p_t*q_t=-(p_u*q_u)                                    (27)
```

up to the harmless nonzero scalars removed in (26).  Their derivative maps
are proportional, while the two nonzero maps in (11) are not.  Contradiction.

### Case M/M on different source pairs

Two distinct source pairs share one source.  After permuting sources, use

```text
p_t=a+b,       q_u=a-b,       a in X, b in Y,
p_u=c+d,       q_t=c-d,       c in X, d in Z.         (28)
```

The complementarity in Lemma 1 forces `a,c` to be independent.  After
rescaling the two diagonal derivatives, they are

```text
D_t(x,y,z)=-x tensor b tensor d
             -a tensor y tensor d+c tensor b tensor z,
D_u(x,y,z)=-x tensor b tensor d
             +a tensor y tensor d-c tensor b tensor z. (29)
```

Their common kernel is zero.  Indeed, their sum first gives `x=0`; their
difference and the independence of `a,c` then give `y=z=0`.  Hence

```text
(D_t,D_u):W -> (X tensor Y tensor Z)^2                (30)
```

is injective.  Its restriction to the three-plane `R` has rank three.  But
(11) says each component of that restriction has rank one, so the combined
rank is at most two.  This final contradiction excludes M/M.

## 5. Rank-seven consequence

S2Y gives the sharp regular bound

```text
dim span(P,Q)<=4.                                     (31)
```

If `rank H=7`, then `dim R=3` and

```text
7=dim(R+span(P,Q))<=3+4.                              (32)
```

Thus equality holds in (31), and Lemma 1 plus Sections 3--4 exclude its
three exhaustive normal-form families.  The exceptional derivative chart
was already excluded in Section 1.  This proves (3).

The exact common-three-space rank frontier is now

```text
rank H=9:                                  IMPOSSIBLE (S2X);
rank H=8:                                  IMPOSSIBLE (S2Y);
rank H=7 with exactly one root block:      IMPOSSIBLE (here);
rank H=7 with at least two root blocks:    OPEN;
rank H<=6:                                 OPEN;
other S2T component types / S2Q strata:   OPEN;
global Krenn--Gu conjecture:              UNRESOLVED.             (33)
```

The next exact equality mechanism is therefore codimension two hiding the
five-dimensional shared derivative of two root blocks.  This theorem does
not infer that such a hidden derivative is physically realizable or
impossible.

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_single_root_block_joint_cross_rank_seven_exclusion.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_single_root_block_joint_cross_rank_seven_exclusion.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_single_root_block_joint_cross_rank_seven_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_single_root_block_joint_cross_rank_seven_exclusion.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_single_root_block_joint_cross_rank_seven_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_single_root_block_joint_cross_rank_seven_exclusion.py
```

The primary replay checks the five equality normal forms, the common-source
projection obstructions, the two `P/M` kernel lines and shared output factor,
the proportional same-pair `M/M` products, and injectivity of the different-
pair `M/M` derivative pair.  The independent no-import audit reconstructs
the permanent maps directly with `Fraction` arithmetic and a separate row
reduction.  Lemma 1 and the arbitrary-vector case analysis above are the
characteristic-zero proof; the normal-form replays are not a finite-sample
substitute.

## Dependencies

- [`BALANCED_M3_COMMON_THREE_SPACE_JOINT_CROSS_RANK_EIGHT_EXCLUSION_THEOREM.md`](BALANCED_M3_COMMON_THREE_SPACE_JOINT_CROSS_RANK_EIGHT_EXCLUSION_THEOREM.md)
- [`BALANCED_M3_COMMON_THREE_SPACE_FULL_JOINT_CROSS_RANK_MONOMIAL_ROOT_EDGE_LOCALIZATION_THEOREM.md`](BALANCED_M3_COMMON_THREE_SPACE_FULL_JOINT_CROSS_RANK_MONOMIAL_ROOT_EDGE_LOCALIZATION_THEOREM.md)
