# Balanced `m=3` common-three-space joint-rank-three transverse two-root uninvolved-rank-two exceptional normal form and pole controls

## Status

**Exact characteristic-zero localization, pair-pole graph-extension
exclusion, and sharp local physical controls for the complete
joint-rank-three, uninvolved-row-rank-two part of the transverse two-root
branch.**  Let `U` be the total singleton span of a normalized,
target-consistent physical `m=3` common shore whose complete four-column
sensor has full function-field rank.  Put `K=image H` and assume

```text
dim U=3,                         rank H=3.             (1)
```

Suppose exactly two root--root blocks are nonzero and the uninvolved third
root row has rank two.  Then every surviving point has both involved rows
of rank two, both root blocks are complementary coordinate monomials, and,
up to root exchange, colour permutation, and nonzero row/block rescaling,
the complete nonroot row system is the two-source conjugate common-zero
chart displayed in Section 4.  There are exactly two kernel-support types:
one missing third-root row, or two proportional nonzero third-root rows.

Both types are genuinely populated by exact physical common-shore sensors.
The controls have joint rank three, singleton span three, full four-column
sensor rank, the exact physical singleton and empty matching formulas, and
every GHZ target incidence.  Their unique rational pair coefficients have
explicit poles on the three source-coordinate divisors.  Because the atlas
is exhaustive, **every** point in this cell has those poles.  The exact
Cramer--Euler pair-pole gate therefore proves that no point in the cell
extends to regular bilinear pair blocks or a six-vertex graph.

This is a complete exclusion of this graph-extension cell while preserving
sharp local incidence evidence.  The rational controls are not regular
bilinear edge blocks and are not graphs or counterexamples.  The remaining
rank-one-row controls still require a complete pole-residue analysis;
lower-rank three-root derivatives, other S2T/S2Q components and pole strata,
higher orders, the all-rank-drop branch, a witness, and a counterexample
remain open.  Global Krenn--Gu remains **UNRESOLVED**.

## 1. Only three `(2,2)` support cells can reach the containment boundary

After permuting roots, write

```text
B_23=B!=0,                  B_13=C!=0,       B_12=0,

D_(B,C)(a,b,c)=a tensor B+C tensor b,
rank D_(B,C)=6.                                      (2)
```

S2BM gives a three-plane

```text
P=pr_(1,2)K subset A_1 direct-sum A_2,
U=D_(B,C)(P),                                       (3)
```

and transposed root-row spaces

```text
V=image rho+image pi,              Q=image theta,
dim V=3,        dim Q=2,           Q subset V.       (4)
```

The involved-row kernel argument in S2BN is rank-free, so each involved row
has rank two or three.  S2BM gives support one or two for the kernel line of
`theta`.

For support one, S2AL excludes `(3,3)`, `(3,2)`, and `(2,3)` without using
the `V,Q` incidence.  For support two, S2AJ similarly excludes the mixed
profiles.  Thus the only profiles not already excluded are

```text
support one:                    (2,2),
support two:                   (2,2) or (3,3).       (5)
```

The complete-target reductions of S2AI, S2AK, and S2AM put each profile in
the hypotheses of the S2BN diagonal common-zero lemma: there is a row `v`
whose square on `Q` has image one pure target `T_j`, and the remaining
mixed maps land in the plane spanned by the other fully transverse targets.
Because (4) is the sharp containment boundary, the old vanishing conclusion
does not apply.  The proof of that lemma nevertheless says exactly what a
nonzero alternating singleton tensor forces:

```text
V=span(x_j,y_j,z_j),                               (6)
```

where `x_j,y_j,z_j` are the three source-factor lines of `T_j`.  Therefore
**every** empty permanent is a scalar multiple of `T_j`.

## 2. The other two target diagonals force monomial blocks and rank two

Let `{d,c,j}` be the three colours.  Since the empty companion has no
`T_d` or `T_c` coefficient, target consistency puts both root diagonals

```text
d_d=e_d tensor e_d tensor e_d,
d_c=e_c tensor e_c tensor e_c                       (7)
```

inside `U`.  The exact two-diagonal derivative-forcing lemma in S2BM then
gives, after exchanging the involved roots,

```text
B_23=lambda e_d tensor e_d,
B_13=mu     e_c tensor e_c,             lambda mu!=0. (8)
```

The derivative is injective on the two involved roots, so the preimages of
(7) are unique:

```text
(e_d,0),(0,e_c) in P.                               (9)
```

A third generator of the three-plane `P` adds at most one new direction to
each projection.  Hence both involved row ranks are at most two.  The lower
bound from Section 1 makes them exactly two.  In particular the support-two
`(3,3)` profile in (5) is impossible.

The exact zero-row analyses of S2AI and S2AM now agree.  After rescaling
(8) and the third generator, every survivor has

```text
B_23=e_d tensor e_d,
B_13=e_c tensor e_c,

P=span{(e_d,0),(0,e_c),(e_j,e_j)}.                  (10)
```

If `v_d,v_c,v_j` is dual to the ordered basis in (10), the involved rows
are

```text
r_d=v_d,            r_c=0,              r_j=v_j,
p_d=0,              p_c=v_c,            p_j=v_j.   (11)
```

No unrestricted nonmonomial block entry remains: comparison of the
`T_d,T_c` coefficients of the complete target equation forces exactly the
two monomials in (10).

## 3. The containment atlas has one source normal form

We retain the sole nonvanishing chart from the proof of S2BN.  Before
normalization it has

```text
v=x+y,                         w=x-y,
q_0=w,                         q_1=lambda x+mu y+t,
u=-lambda x-mu y+t,           lambda+mu!=0,          (12)

common-zero(v,Q)=span(w,u).                          (13)
```

Write two independent common zeros as

```text
u_0=A w+B u,                   u_1=C w+D u,
Delta=A D-B C!=0.                                    (14)
```

The complete target table puts `M_(u_0,u_1)(Q)` in the target plane fully
transverse to `T_j`.  Every value in this chart instead has third factor
`t`, so the mixed map is zero.  S2BN's exact identities give

```text
0=-(A D+B C)x tensor y tensor t
   +B D(lambda-mu)x tensor y tensor t,              (15)

0=-(A C+lambda mu B D)x tensor y tensor t.          (16)
```

Changing `q_1` by a multiple of `q_0`, then rescaling `q_1,t,u`, makes

```text
lambda=mu=1,
q_1=x+y+t,                     u=-x-y+t.             (17)
```

Equations (15)--(16) become

```text
A D+B C=0,                    A C+B D=0.             (18)
```

All four coefficients are nonzero: any zero, together with (18), would
contradict `Delta!=0`.  Dividing the two equations gives

```text
(A/B)^2=1.                                           (19)
```

Thus, after rescaling and possibly exchanging `u_0,u_1`, their unordered
pair is `{w+u,w-u}`.  Put

```text
a=w+u=-2y+t,
b=w-u= 2x-t,
v=x+y,                    w=x-y,
q=(x+y+t)/2.                                           (20)
```

Direct polarization gives the complete grid

```text
per(v,v,q)=x tensor y tensor t,

per(a,v,w)=per(a,v,q)=0,
per(v,b,w)=per(v,b,q)=0,
per(a,b,w)=per(a,b,q)=0.                            (21)
```

The alternating singleton tensor is

```text
Alt_XYZ(a,b,v)=4x tensor y tensor t!=0.              (22)
```

## 4. The two exact kernel-support controls

Identify `x=x_j in X`, `y=y_j in Y`, `t=z_j in Z`, and use the involved
rows

```text
r_d=a,              r_c=0,              r_j=v,
p_d=0,              p_c=b,              p_j=v.      (23)
```

There are two third-root choices.

### Support one

```text
q_d=0,              q_c=w,              q_j=q,
ker theta=span(e_d^*).                                 (24)
```

### Support two

For any `gamma!=0`, take

```text
q_d=w,              q_c=gamma w,        q_j=q,
ker theta=span(gamma e_d^*-e_c^*).                    (25)
```

In both cases all nine root rows span `span(x,y,t)`, so `rank H=3`, while
`rank theta=2`.  Equations (21) give the exact empty companion

```text
G_N=d_j x y t.                                      (26)
```

The only nonzero empty target cell is `(j,j,j)`, with coefficient `T_j`.
Thus (23)--(26) satisfy every root row of the complete GHZ target equation
for both kernel supports.

## 5. Physical singleton columns and pole-bearing pair coefficients

In the basis of `U` supplied by (10),

```text
u_d=d_d,
u_c=d_c,
u_j=e_j tensor e_d tensor e_d
    +e_c tensor e_j tensor e_c,                     (27)
```

the three physical singleton columns are

```text
G_X=(0, 2x, x),
G_Y=(-2y,0,y),
G_Z=(t,-t,0).                                       (28)
```

Their determinant is

```text
det(G_X,G_Y,G_Z)=4x y t.                            (29)
```

The empty column (26) is not in `U`, so the complete four-column sensor has
full function-field rank.  Equations (27)--(29) are obtained from the
physical matching formulas for the two root blocks in (10); they are not an
abstract row-table substitution.

Write the two residual nonroot targets as `T_d,T_c`.  Solving the unique
singleton-column lift

```text
G_X C_X+G_Y C_Y+G_Z C_Z=(T_d,T_c,0)                 (30)
```

gives

```text
C_X=(T_d+T_c)/(4x),
C_Y=-(T_d+T_c)/(4y),
C_Z=(T_d-T_c)/(2t).                                 (31)
```

These rational tensors have the required multidegrees, but expose poles on

```text
x y t=0.                                            (32)
```

They are therefore exact common-shore pole controls, not regular global
pair blocks.  Support one and support two have the same singleton columns
and the same unique pair coefficients; only the third-root row relation
changes.

### Corollary 1 (the complete cell has no graph extension)

Every normalized target-consistent point under the hypotheses of this
theorem fails the pair-pole condition of the exact Cramer--Euler
globalization gate.

Indeed, the atlas in Sections 1--4 is exhaustive, so every survivor has
(31) after invertible gauge changes.  On the prime divisor `x=0`, the
numerator `T_d+T_c` is not divisible by `x`; the first component has
valuation `-1`.  The same argument applies to `y=0`.  On `t=0`, the
independent tensor `T_d-T_c` is not divisible by `t`, so the third component
also has valuation `-1`.  Thus the intrinsic pair-regularity condition

```text
nu_P(C_e)>=0 for every pair e and prime divisor P   (33)
```

fails.  The Cramer--Euler gate is an if-and-only-if same-shore extension
criterion.  Hence neither kernel-support type extends to physical bilinear
pair blocks or a graph.  The local controls prove sharpness only for the
preceding singleton/empty equations.  QED.

## 6. Proof-topology consequence

Together with S2BN, the transverse two-root lower-rank frontier is now

```text
joint rank 4, q=2:                                  IMPOSSIBLE (S2BN);

joint rank 4, q=1:
  exact physical pole control:                      EXISTS (S2BM);

joint rank 3, q=2:
  support-one and support-two exceptional forms:    COMPLETE ATLAS;
  exact physical local pole controls:               EXIST;
  regular graph extension:                          IMPOSSIBLE (here);

joint rank 3, q=1:
  exact physical pole control:                      EXISTS (S2BM);

common unresolved successor for all populated cells:
  rank-one-row pole-residue / pair-deck obstruction: OPEN.            (34)
```

No finite-field scan, numerical specialization, bounded sample, generic-
point promotion, or unproved incidence cover enters the theorem.

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_three_transverse_two_root_uninvolved_rank_two_exceptional_normal_form_and_pole_controls.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_three_transverse_two_root_uninvolved_rank_two_exceptional_normal_form_and_pole_controls.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_three_transverse_two_root_uninvolved_rank_two_exceptional_normal_form_and_pole_controls.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_three_transverse_two_root_uninvolved_rank_two_exceptional_normal_form_and_pole_controls.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_three_transverse_two_root_uninvolved_rank_two_exceptional_normal_form_and_pole_controls.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_three_transverse_two_root_uninvolved_rank_two_exceptional_normal_form_and_pole_controls.py
```

The primary verifier checks the conjugate-chart normalization, transverse
derivative and relation plane, both third-row support controls, all 27 empty
root cells, the physical singleton columns, full sensor rank, and the
rational Cramer identities with exact SymPy arithmetic.  The independent
audit imports no repository module or third-party package; it reconstructs
the two root blocks, sparse permanents, ranks, singleton columns, and pair
identities with standard-library `Fraction` arithmetic.  The scripts replay
the displayed identities.  The arbitrary-vector atlas and profile
exhaustion are the proof above and the cited exact predecessors.

## Dependencies

- [`lower-joint-rank transverse localization and pole controls`](BALANCED_M3_COMMON_THREE_SPACE_LOWER_JOINT_RANK_TRANSVERSE_TWO_ROOT_LOCALIZATION_AND_POLE_CONTROLS_THEOREM.md)
- [`joint-rank-four uninvolved-rank-two complete exclusion`](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FOUR_TRANSVERSE_TWO_ROOT_UNINVOLVED_RANK_TWO_COMPLETE_EXCLUSION_THEOREM.md)
- [`support-two (2,2) complete target table`](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_SUPPORT_TWO_TWO_BY_TWO_COMPLETE_EXCLUSION_THEOREM.md)
- [`support-two mixed-row-rank exclusion`](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_SUPPORT_TWO_MIXED_ROW_RANK_EXCLUSION_THEOREM.md)
- [`support-two (3,3) complete target table`](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_SUPPORT_TWO_THREE_BY_THREE_EXCLUSION_THEOREM.md)
- [`support-one higher-row-rank exclusion`](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_SUPPORT_ONE_HIGHER_ROW_RANK_EXCLUSION_THEOREM.md)
- [`support-one (2,2) complete target table`](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_SUPPORT_ONE_TWO_BY_TWO_COMPLETE_EXCLUSION_THEOREM.md)
- [`Cramer--Euler pair-pole globalization gate`](BALANCED_FULL_SENSOR_CRAMER_EULER_PAIR_POLE_GATE_THEOREM.md)
