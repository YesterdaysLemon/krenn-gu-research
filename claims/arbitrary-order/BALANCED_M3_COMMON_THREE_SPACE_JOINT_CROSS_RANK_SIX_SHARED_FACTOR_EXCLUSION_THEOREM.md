# Balanced `m=3` common-three-space rank-six shared-factor exclusion

## Status

**Exact characteristic-zero exclusion of the rank-five shared-derivative part
of joint cross rank six on the S2Q common-three-space stratum.**  Let `U` be
the total singleton span of a normalized, target-consistent physical `m=3`
common shore, assume

```text
dim U=3,                 rank H=6,                     (1)
```

and suppose at least two root--root blocks are nonzero.  It is impossible
for the shared derivative `D_B` to have rank five.

By the complete single-root exclusion and the three-nonzero-summand syzygy
bound, every surviving rank-six point therefore has exactly two nonzero
root blocks and

```text
rank D_B=6;                                             (2)
```

equivalently, their two three-dimensional derivative summands are disjoint.
This leaves that transverse derivative-rank-six case open.  Joint rank at
most five, the other S2T/S2Q branches, every higher order, all-rank-drop, a
witness, and a counterexample remain open.  Global Krenn--Gu remains
**UNRESOLVED**.

## 1. The shared-factor rank-five normal form

Put `K=image H`.  Since `K` has codimension three and `D_B(K)=U`,

```text
rank D_B<=6.                                           (3)
```

If `rank D_B=5` and at least two root blocks are nonzero, S2U's pairwise
intersection lemma gives exactly two rank-one blocks with one shared endpoint
factor.  A third block would make all three derivative summands nonzero, and
the S2X two-syzygy lemma would give derivative rank at least seven.

After permuting roots and rescaling, write

```text
B_23=y tensor z,
B_13=x tensor z,
B_12=0,                                               (4)

D_B(a,b,c)=(a tensor y+x tensor b) tensor z.          (5)
```

The derivative kernel has dimension four.  Rank--nullity gives the sharp
intersection

```text
dim(K intersect ker D_B)=3.                           (6)
```

Moreover

```text
U=U_0 tensor z,
U_0 subset A_1 tensor y+x tensor A_2,       dim U_0=3. (7)
```

The S2R no-torus-annihilator theorem forces `z` to be a target coordinate:
if it used at least two coordinates, a fully supported covector could
annihilate it and hence all of `U`.  Thus, for one colour `s`,

```text
z=e_(3,s),
G_N in J+U_0 tensor e_(3,s).                          (8)
```

Let `t,u` be the other two colours.  Write the three transposed block rows of
`H` as

```text
rho:A_1^*->W^*,       pi:A_2^*->W^*,       theta:A_3^*->W^*,
W=X direct-sum Y direct-sum Z,                       (9)

r_a=rho(e_a^*),       p_b=pi(e_b^*),       q_c=theta(e_c^*). (10)
```

The two root-3 slices unaffected by (8) satisfy

```text
per(r_a,p_b,q_v)
 =delta_(a,v) delta_(b,v) T_v,       v=t,u,           (11)

T_v=X_v tensor Y_v tensor Z_v.                        (12)
```

## 2. The involved row ranks are at least two

If `alpha in ker rho`, contracting (11) first at `v=t` and then at `v=u`
gives `alpha_t=alpha_u=0`.  Hence

```text
rank rho>=2,                    rank pi>=2.            (13)
```

If both ranks were two, their kernels would be the missing coordinate lines
and

```text
r_s=p_s=0.                                             (14)
```

Thus every vector `(a,b,c) in K` would have `a_s=b_s=0`.  Formula (5) would
make the `(s,s)` coefficient of every tensor in `U_0` zero.  On the other
hand (14) makes the `(s,s,s)` root coefficient of `G_N` zero, so the pure
source word `X_sY_sZ_s` in (8) requires
`e_(1,s) tensor e_(2,s)` to belong to `U_0`.  Contradiction.  Therefore the
rank profile `(2,2)` is impossible.

Suppose both ranks were three.  Evaluate every source component at arbitrary
local colour vectors and form the `3 x 3` matrices `R,P` with rows the
evaluated `r_a,p_b`.  As in the rank-seven two-root theorem, (11) becomes

```text
R M(q_t) P^T=mu_t E_(t,t),
R M(q_u) P^T=mu_u E_(u,u),                            (15)
```

where `mu_t mu_u` is nonzero on a dense open set and

```text
M(q_X,q_Y,q_Z)=
[  0   q_Z q_Y ]
[ q_Z   0  q_X ].                                    (16)
[ q_Y q_X   0  ]
```

The two target column and row lines force generic evaluated ranks at least
two.  If `det R` vanished identically, its generic column space would be the
fixed plane `span(e_t,e_u)`, making `r_s=0` and contradicting `rank rho=3`.
Thus `R` is generically invertible; the same holds for `P`.  At a common
invertible point (15) would make the nonzero zero-diagonal matrix `M(q_t)`
rank one.  Every such matrix has a nonzero principal `2 x 2` minor and rank
at least two.  Contradiction.  The profile `(3,3)` is impossible.

Up to exchanging roots, only

```text
rank rho=2,                  rank pi=3                (17)
```

remains.  Then `r_s=0`, while the three `p_b` form a basis of the three-plane

```text
V=image pi.                                            (18)
```

## 3. Exact slice zeros become crossed zero products

The same two target slices show that the evaluated matrix `P` is generically
invertible.  Otherwise its generic column space would again be
`span(e_t,e_u)`, forcing `p_s=0` and contradicting `rank pi=3`.

For `a=u`, the entire `q_t` slice in (11) is zero:

```text
per(r_u,p_b,q_t)=0                 for b=0,1,2.       (19)
```

At a point where `P` is invertible, (19) says

```text
hat r_u M(hat q_t)=0.                                (20)
```

Since this holds on a dense open set, its polynomial coefficients vanish:

```text
r_u*q_t=0.                                            (21)
```

The other slice gives symmetrically

```text
r_t*q_u=0.                                            (22)
```

The diagonal slice entries are nonzero, so

```text
r_t*q_t!=0,                    r_u*q_u!=0.             (23)
```

Finally (11), now viewed as derivatives on the marked basis `(p_0,p_1,p_2)`
of `V`, says

```text
D_(r_v*q_v) restricted to V
 =epsilon_v tensor T_v,                  v=t,u,       (24)
```

where `epsilon_t,epsilon_u` are independent coordinate covectors on `V`.

## 4. Crossed-pair diagonal lemma

We isolate the rank-free obstruction already implicit in the complete
single-root theorem.

### Lemma 1 (two crossed zero pairs cannot carry two GHZ diagonals)

Let `V subset X direct-sum Y direct-sum Z` be any three-plane.  Suppose
nonzero vectors `a_t,a_u,q_t,q_u` satisfy

```text
a_t*q_u=0,                       a_u*q_t=0,            (25)
a_t*q_t!=0,                      a_u*q_u!=0,           (26)
```

and their derivative restrictions to `V` are two nonzero rank-one maps with
independent coefficient covectors and target tensors having distinct factor
lines in all three sources.  No such data exist.

### Proof

Every nonzero zero-product pair is either pure in one source or a conjugate
mixed pair `a+b,a-b` on two sources.

- `P/P` on different sources and `P/M` sharing one source make both diagonal
  derivatives depend on the same remaining-source projection of `V`, hence
  use one coefficient covector.
- `P/M` on all three sources has two derivative kernels
  `span(b,-c)` and `span(b,c)`.  Independent rank-one restrictions force the
  projected plane to contain both; the two target tensors then share the
  factor lines `b,c`.
- `M/M` on the same source pair makes the two diagonal quadratic triples
  proportional with opposite sign.
- `M/M` on different source pairs has two subcases.  Independent lines in
  their shared source make the combined derivative injective, so its
  restriction to a three-plane has rank three rather than at most two.
  Proportional shared-source lines put both target tensors in one Segre
  tangent space.  Every decomposable in that tangent shares at least two of
  its three base factor lines, so two target tensors with no common factor
  line cannot both belong.

These cases are exhaustive.  QED.

Equations (21)--(24) satisfy Lemma 1 with `a_v=r_v`.  This contradiction
excludes (17), and hence every possible row-rank profile.  The assumed
rank-five derivative branch is empty.

## 5. Proof-topology consequence

At joint rank six, (3) and the three-nonzero-summand rank floor give the
exhaustive derivative alternatives

```text
exactly two root blocks, shared-factor rank D_B=5:  IMPOSSIBLE (here);
exactly two root blocks, transverse rank D_B=6:     OPEN;
three nonzero root blocks:                          IMPOSSIBLE at rank H=6;
one nonzero root block:                             IMPOSSIBLE (S2AB).
                                                               (27)
```

Thus the transverse two-root case is the sole rank-six common-three-space
obligation.  Joint rank at most five and the other physical branches remain
open.  Global Krenn--Gu remains **UNRESOLVED**.

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_cross_rank_six_shared_factor_exclusion.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_cross_rank_six_shared_factor_exclusion.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_cross_rank_six_shared_factor_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_cross_rank_six_shared_factor_exclusion.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_cross_rank_six_shared_factor_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_cross_rank_six_shared_factor_exclusion.py
```

The primary replay checks the rank-five derivative and its four-dimensional
kernel, the row-rank trichotomy, pointwise matrix identity and rank floor,
promotion of a three-row slice zero to a quadratic zero product, and all six
crossed-pair cases.  The independent audit reconstructs those calculations
with `Fraction` elimination and a separate six-term permanent.  The
arbitrary-tensor intersection, density, and Lemma 1 arguments are the proof.

## Dependencies

- [`BALANCED_M3_COMMON_THREE_SPACE_FULL_JOINT_CROSS_RANK_MONOMIAL_ROOT_EDGE_LOCALIZATION_THEOREM.md`](BALANCED_M3_COMMON_THREE_SPACE_FULL_JOINT_CROSS_RANK_MONOMIAL_ROOT_EDGE_LOCALIZATION_THEOREM.md)
- [`BALANCED_M3_COMMON_THREE_SPACE_FULL_JOINT_CROSS_RANK_EXCLUSION_THEOREM.md`](BALANCED_M3_COMMON_THREE_SPACE_FULL_JOINT_CROSS_RANK_EXCLUSION_THEOREM.md)
- [`BALANCED_M3_COMMON_THREE_SPACE_TWO_ROOT_BLOCK_JOINT_CROSS_RANK_SEVEN_EXCLUSION_THEOREM.md`](BALANCED_M3_COMMON_THREE_SPACE_TWO_ROOT_BLOCK_JOINT_CROSS_RANK_SEVEN_EXCLUSION_THEOREM.md)
- [`BALANCED_M3_COMMON_THREE_SPACE_SINGLE_ROOT_BLOCK_COMPLETE_EXCLUSION_THEOREM.md`](BALANCED_M3_COMMON_THREE_SPACE_SINGLE_ROOT_BLOCK_COMPLETE_EXCLUSION_THEOREM.md)
- [`BALANCED_M3_SINGLETON_SPAN_TORUS_ANNIHILATOR_PERMANENT_RANK_OBSTRUCTION.md`](BALANCED_M3_SINGLETON_SPAN_TORUS_ANNIHILATOR_PERMANENT_RANK_OBSTRUCTION.md)
