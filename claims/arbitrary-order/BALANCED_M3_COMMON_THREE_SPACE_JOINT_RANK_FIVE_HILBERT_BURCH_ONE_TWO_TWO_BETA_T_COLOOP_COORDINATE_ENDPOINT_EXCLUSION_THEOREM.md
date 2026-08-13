# Balanced `m=3` joint-rank-five Hilbert--Burch `(1,2,2)` `beta_t`-coloop coordinate-endpoint exclusion

## Status

**Exact characteristic-zero exclusion of both coordinate endpoints left by
S2BA in the distinguished second-root coloop orientation of the normalized,
target-consistent physical `m=3` common-three-space full-sensor stratum.**
Retain

```text
dim U=3,                         rank H=5,             (1)
```

the S2AZ gauge

```text
ker D_B=span{(lambda e_s,y,z),(0,mu e_t,w)},
lambda mu!=0,                   y_t=0,
dim span(y,e_t)=dim span(z,w)=2,                     (2)
```

and the distinguished coloop

```text
N=K^perp subset {beta_t=0}.                          (3)
```

Let `a,b` be the two colours different from `t`.  S2BA proves that only

```text
w proportional to e_a             or
w proportional to e_b                                      (4)
```

can remain.  Neither alternative in (4) is possible.  Consequently

```text
N subset {beta_t=0}:                              IMPOSSIBLE. (5)
```

The proof uses one exact permanent lemma.  On a three-dimensional row shore,
a nonzero row cannot have a two-plane of permanent partners annihilating the
whole shore while a second row has exactly one of those two partner rows
zero.  The three possible source supports of the first row give respectively
a one-dimensional shore, a missing source, or a pure-source partner plane;
the last case makes both partner rows simultaneously zero for every second
row.

This closes only the distinguished `beta_t` coloop orientation.  The other
eight `(1,2,2)` coordinate coloops, joint rank at most four, other physical
component types, higher orders, and the global conjecture remain open.
Global Krenn--Gu remains **UNRESOLVED**.

## 1. The endpoint gives a single-cell table in an exact three-space

Use the notation of S2AZ--S2BA:

```text
E=image H^T,                    V=H^T((ker D_B)^perp),
dim E=5,                        dim V=3,

A=lambda^(-1)r_s,              B=mu^(-1)p_t,
R=rho(e_s^perp),               dim R=2.             (6)
```

The classes of `A,B` form a basis of `E/V`.  In particular `A` is not in
`V`, while `R` is contained in `V`.  Therefore

```text
S=R direct-sum span(A),                       dim S=3. (7)
```

The two rows `r_i`, `i!=s`, form a basis of `R`, and `r_s=lambda A`.
Consequently

```text
rho:A_1^* -> S                                  is an isomorphism. (8)
```

S2BA also proves that `pi` and `theta` are injective and, on the complete
derivative-zero face,

```text
per(r(alpha),p(beta),q(gamma))
 =sum_i alpha_i beta_i gamma_i T_i,
 beta_t=0,                  gamma(w)=0.             (9)
```

Assume one endpoint in (4), and absorb its nonzero scalar into the kernel
generator:

```text
w=e_a.                                               (10)
```

The endpoint annihilator is `w^perp={gamma_a=0}`.  The corrected-row
identities of S2BA put

```text
p_a,p_b,q_b,q_t in S.                               (11)
```

Injectivity makes each displayed row nonzero and makes

```text
Q=span(q_b,q_t)                         a two-plane. (12)
```

Substitution of the coordinate covectors in (9) gives the complete table

```text
per(S,p_a,Q)=0,
per(S,p_b,q_t)=0,
per(r(alpha),p_b,q_b)=alpha_b T_b.                  (13)
```

The last map is nonzero because `T_b!=0`; by (8) it is a nonzero rank-one
map on all of `S`.  Thus (13) has exactly one surviving cell in the
`3 x 2 x 2` table.

## 2. A single-cell `3 x 2 x 2` permanent table is impossible

For `u,v in W=X direct-sum Y direct-sum Z`, write

```text
M_(u,v)(d)=per(u,v,d).                               (14)
```

### Lemma 1 (two-partner radical propagation)

Let `S subset W` have dimension three, let `0!=p,d in S`, and let
`Q=span(q_0,q_1) subset S` be a two-plane.  In characteristic different
from two, the conditions

```text
M_(S,p)(Q)=0,                    M_(S,d)(q_1)=0       (15)
```

imply

```text
M_(S,d)(q_0)=0.                                    (16)
```

In particular (15) cannot coexist with a nonzero value of the last map.

#### Proof

Split `p` according to its number of nonzero source components.

Suppose first that

```text
p=x+y+z,                     x in X, y in Y, z in Z,
                             xyz!=0.                 (17)
```

Because `p in S`, the first equation of (15) includes
`M_(p,p)(Q)=0`.  Direct expansion gives

```text
ker M_(p,p)
 ={a x+b y+c z:a+b+c=0}
 =span(x-y,x-z).                                    (18)
```

The kernel has dimension two, so it equals `Q`.  For `v in S`, the two
mixed zero equations are

```text
M_(v,p)(x-y)=(x tensor v_Y-v_X tensor y) tensor z=0,

M_(v,p)(x-z)=x tensor y tensor v_Z
             -v_X tensor y tensor z=0.              (19)
```

The first identity makes `v_X=c x` and `v_Y=c y`; the second makes
`v_X=c x` and `v_Z=c z`, with the same scalar.  Hence `v=c p` for every
`v in S`, contradicting `dim S=3`.

Suppose next that, after permuting sources,

```text
p=x+y,                         xy!=0.                (20)
```

The square zero in (15) first gives

```text
Q subset X direct-sum Y.                             (21)
```

For `v in S`, `q in Q`, expansion now gives

```text
M_(v,p)(q)
 =(x tensor q_Y+q_X tensor y) tensor v_Z.            (22)
```

If some `v_Z` is nonzero, all of `Q` lies in the kernel of

```text
q |-> x tensor q_Y+q_X tensor y,                    (23)
```

whose kernel inside `X direct-sum Y` is exactly the line `span(x-y)`.
This contradicts `dim Q=2`.  Otherwise `S subset X direct-sum Y`, so every
permanent of three vectors in `S` is zero.  Then both sides of (16) vanish.

It remains that, after a source permutation,

```text
p=x in X.                                            (24)
```

For each `q in Q`, put `v=q` in the first equation of (15).  Since the
characteristic is not two,

```text
0=M_(q,x)(q)=2 x tensor q_Y tensor q_Z              (25)
```

shows that `q_Y=0` or `q_Z=0`.  A two-plane cannot be the union of two
proper linear subspaces, so either

```text
Q subset X direct-sum Y          or
Q subset X direct-sum Z.                            (26)
```

Take the first alternative; the second is symmetric.  The full mixed zero
becomes

```text
0=M_(v,x)(q)=x tensor q_Y tensor v_Z,
                         v in S, q in Q.             (27)
```

If some `q_Y` is nonzero, (27) puts `S` in `X direct-sum Y`, and every
permanent on `S` is zero.  Otherwise

```text
Q subset X.                                          (28)
```

For a nonzero pure `X` row `q`, direct expansion is

```text
M_(v,d)(q)
 =q tensor(v_Y tensor d_Z+d_Y tensor v_Z).           (29)
```

The bracket in (29) is independent of the choice of nonzero `q in Q`.
Since `q_1!=0`, the second equation of (15) kills that bracket for every
`v in S`; equation (29) then proves (16) for `q_0`.  This exhausts the
source supports of `p` and proves the lemma.  QED.

## 3. Endpoint exclusion and proof-topology consequence

Apply Lemma 1 to (13) with

```text
p=p_a,              d=p_b,
q_0=q_b,            q_1=q_t.                        (30)
```

The first two lines of (13) are (15), so the lemma gives

```text
per(S,p_b,q_b)=0,                                   (31)
```

contradicting the last line of (13).  Thus `w=e_a` is impossible.
Interchanging the two colours complementary to `t` excludes `w=e_b`.
Together with S2BA this proves (5).

The live `(1,2,2)` frontier is therefore

```text
beta_t coloop:                                      IMPOSSIBLE;

other eight coordinate coloops / joint rank <=4
  / other components / higher m:                    OPEN;

global Krenn--Gu conjecture:                        UNRESOLVED.      (32)
```

No finite scan, numerical specialization, generic-point promotion, target
factor-sharing assumption, or unproved incidence classification enters the
argument.

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_beta_t_coloop_coordinate_endpoint_exclusion.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_beta_t_coloop_coordinate_endpoint_exclusion.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_beta_t_coloop_coordinate_endpoint_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_beta_t_coloop_coordinate_endpoint_exclusion.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_beta_t_coloop_coordinate_endpoint_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_two_two_beta_t_coloop_coordinate_endpoint_exclusion.py
```

The primary replay checks all six endpoint-colour choices and the full-,
two-, and pure-source linear maps in Lemma 1 exactly.  The independent audit
uses standard-library rational arithmetic, a different tensor-coordinate
order, and separate elimination code to reconstruct the same kernel and
radical dimensions.  The scripts replay the displayed identities; the
arbitrary-vector support exhaustion is the proof above.

## Dependencies

- [`(1,2,2)` `beta_t`-coloop support localization](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_TWO_TWO_BETA_T_COLOOP_SUPPORT_LOCALIZATION_THEOREM.md)
