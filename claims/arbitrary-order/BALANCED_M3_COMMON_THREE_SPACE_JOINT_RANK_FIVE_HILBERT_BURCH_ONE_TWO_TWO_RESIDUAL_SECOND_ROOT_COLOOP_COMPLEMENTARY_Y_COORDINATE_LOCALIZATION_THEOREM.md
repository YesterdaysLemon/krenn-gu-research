# Balanced `m=3` joint-rank-five Hilbert--Burch `(1,2,2)` residual second-root-coloop complementary-`y` coordinate localization

## Status

**Exact characteristic-zero complementary-`y` coordinate localization for
every surviving residual second-root coordinate-coloop endpoint on the
normalized, target-consistent physical `m=3` common-three-space full-sensor
stratum.**  Retain

```text
dim U=3,                         rank H=5,

ker D_B=span{(lambda e_s,y,z),(0,mu e_t,w)},
lambda mu!=0,                   y_t=0,
dim span(y,e_t)=dim span(z,w)=2,                     (1)
```

and suppose

```text
N=K^perp subset {beta_j=0},                   j!=t.  (2)
```

Let `k` be the third colour.  S2BE--S2BG give

```text
w is proportional to e_j or e_k,       s in {j,k}. (3)
```

Let `u` be the other colour in `{j,k}` from `s`.  Then

```text
y is proportional to e_u.                            (4)
```

Thus every surviving endpoint has the exact complementary coordinate pair

```text
x proportional to e_s,         y proportional to e_u,
{s,u,t}={0,1,2}.                                    (5)
```

The endpoint `w` may still be proportional to `e_s` or `e_u`.  This theorem
does not exclude either residual coloop, any surviving endpoint, the three
third-root coloops, the two complementary first-root coloops, joint rank at
most four, other physical components, higher orders, or the global
conjecture.  Global Krenn--Gu remains **UNRESOLVED**.

## 1. The endpoint equal to `s`

Absorb the nonzero endpoint scalar.  First suppose

```text
w=e_s.                                               (6)
```

This is the `s=l` row of the exact S2BF endpoint table.  Its projective gate
fork cannot use `z_s=w_s=0`, because `w_s=1`.  Hence `y_s=0`.  Together with
the gauge `y_t=0` and the independence of `y,e_t`, this gives exactly

```text
y proportional to e_u.                              (7)
```

S2BF additionally gives `z_u z_t=0` in this chart; that condition is
retained but is not needed to prove (7).

## 2. The endpoint different from `s`

It remains that

```text
w=e_u.                                               (8)
```

S2BF's projective factorization gives the exact alternative

```text
y_s=0                 or                 z_s=w_s=0. (9)
```

Suppose for contradiction that `y_s!=0`.  Then the second alternative in
(9) holds, and (8) already has `w_s=0`, so

```text
z_s=w_s=0.                                          (10)
```

Independence of `z,w` makes them a basis of the two-plane `e_s^perp`.

For a projective direction `delta=[h:kappa]`, use the determinant-pencil
planes

```text
P_delta={beta:kappa beta(y)-h mu beta_t=0},
Q_delta={gamma:kappa gamma(z)-h gamma(w)=0}.        (11)
```

Choose a direction with

```text
kappa!=0,
Q_delta=span(e_s^*,gamma_*),
(gamma_*)_u (gamma_*)_t!=0.                         (12)
```

This removes only three points from the projective line.  Indeed, by (10)
the normals `kappa z-hw` traverse every projective line in `e_s^perp`, so
their annihilator lines do too.  The characteristic-zero base field is
infinite.

The first coordinate-projection gate is now

```text
L_P(h,kappa)=kappa y_s!=0.                          (13)
```

Thus `P_delta` has coordinate lifts `beta^u,beta^t` over the two colours
different from `s`.  On the complete derivative-zero product face

```text
alpha_s=0,       beta in P_delta,       gamma in Q_delta,
```

the target equation gives, for `a,b in {u,t}`,

```text
per(r_a,p(beta^b),q(gamma_*))
 =delta_(a,b)(gamma_*)_aT_a,

per(r_a,p(beta^b),q_s)=0.                           (14)
```

Both active coefficients are nonzero and `T_u,T_t` are fully transverse.

S2BF puts the first-row plane, `q(Q_delta)`, and a nonzero line of
`p(P_delta)` in one space of dimension at most three.  S2BC's
target-contraction argument makes `pi` and `theta` injective, so no plane or
intersection row collapses.  Equation (14) therefore satisfies the
intersecting-middle-plane same-third-row obstruction proved in S2BG Lemma 1.
This contradiction excludes `y_s!=0`.

Consequently `y_s=0`.  Since `y_t=0` and `y,e_t` are independent, `y` is a
nonzero multiple of the sole remaining coordinate `e_u`.  This proves (4)
also under (8).

## 3. Proof-topology consequence

The live `(1,2,2)` rank-five coloop frontier is now

```text
beta_t coloop:                                      IMPOSSIBLE (S2BB);
alpha_s coloop:                                     IMPOSSIBLE (S2BC);

beta_j coloop, j!=t:
  s=t:                                              IMPOSSIBLE (S2BG);
  s in {j,k}, y proportional to the other
    coordinate in {j,k}, w proportional to e_j/e_k,
    subject to the remaining S2BF z conditions:     OPEN;

three gamma_k coloops / two complementary alpha coloops
  / joint rank <=4 / other components / higher m:  OPEN;

global Krenn--Gu conjecture:                        UNRESOLVED.     (15)
```

No surviving endpoint is asserted to exist.  No finite-field scan,
numerical specialization, generic-point promotion, or new computational
certificate enters this corollary; its permanent obstruction is exactly the
independently audited S2BG lemma.

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_complementary_y_coordinate_localization.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_complementary_y_coordinate_localization.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_complementary_y_coordinate_localization.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_complementary_y_coordinate_localization.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_complementary_y_coordinate_localization.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_residual_second_root_coloop_complementary_y_coordinate_localization.py
```

The primary replay checks exact symbolic coordinate lifts and the full eight
target cells.  The independent audit uses only standard-library rational
arithmetic and a separately oriented fixture.  The projective finite-avoidance
and inherited S2BG arbitrary-field lemma are the proof.

## Dependencies

- [`(1,2,2)` residual second-root-coloop `s=t` endpoint exclusion and generalized same-third-row lemma](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_TWO_TWO_RESIDUAL_SECOND_ROOT_COLOOP_S_EQUAL_T_ENDPOINT_EXCLUSION_THEOREM.md)
- [`(1,2,2)` residual second-root-coloop projective-pencil localization](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_TWO_TWO_RESIDUAL_SECOND_ROOT_COLOOP_PROJECTIVE_PENCIL_LOCALIZATION_THEOREM.md)
- [`(1,2,2)` determinant-face pencil and `pi,theta` injectivity](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_TWO_TWO_ALPHA_S_COLOOP_EXCLUSION_THEOREM.md)
