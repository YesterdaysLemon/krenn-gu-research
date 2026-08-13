# Balanced `m=3` joint-rank-five Hilbert--Burch `(1,1,2)` third-colour coloop exclusion

## Status

**Exact characteristic-zero exclusion of the third-colour ordinary-coloop
orbit left by S2AS in the distinct-colour central branch of the `(1,1,2)`
Hilbert--Burch boundary.**  Retain the normalized, target-consistent physical
`m=3` common-three-space full-sensor hypotheses

```text
dim U=3,                         rank H=5,             (1)
```

and the Hilbert--Burch normal form

```text
ker D_B=span{(lambda e_s,0,z),(0,mu e_t,w)},
dim span(z,w)=2,

B_23=-mu e_t tensor z,
B_13=-lambda e_s tensor w,
B_12= lambda mu e_s tensor e_t,                     (2)
```

where `s,t,u` are the three distinct target colours.  Assume, as in the
distinct-colour part of S2AS,

```text
w is not proportional to e_s,
z is not proportional to e_t.                        (3)
```

Let `N=K^perp`.  Then neither of the two alternatives

```text
N subset {alpha_u=0},             N subset {beta_u=0} (4)
```

can occur.  Equivalently, the torus-forced ordinary coloop cannot be the
row carrying the third colour `u` in either of the two one-dimensional
kernel projections.

The proof uses the primal/row-plane consequence of (4).  In the first
orientation, `r_u` is a coloop while `r_t`, the complete second-row plane,
and all three combined third rows lie in one two-plane `S`.  The full
third-row image `Q` has dimension three, and

```text
per(r_t,S,Q)=0.                                      (5)
```

A nonzero exterior `T_t` face upgrades, using (5), to a genuine square
`per(q,q,r_t)=T_t`.  A complete source-support split forces `r_t` to be
pure.  Its zero table then either puts three independent target factor lines
inside `S`, or makes every decomposable value on `S x Q` share a factor with
`T_t`.  The required `T_s` and `T_u` values contradict both alternatives.
The second orientation in (4) is symmetric.

Together with S2AS, this leaves in the stated distinct-colour central chart
only the central-colour ordinary coloops `alpha_t=0` and `beta_s=0`, plus
the repeated outer-factor divisors excluded from (3).  The same-colour
central chart, outer coordinate-pair charts, the rest of `(1,1,2)`,
`(1,2,2)`, lower joint ranks, other physical branches, higher orders, and
the global conjecture remain open.  Global Krenn--Gu remains
**UNRESOLVED**.

## 1. The ordinary-coloop row geometry

The derivative is

```text
D_B(a,b,c)
 =-mu a tensor e_t tensor z
  -lambda e_s tensor b tensor w
  +lambda mu e_s tensor e_t tensor c.                (6)
```

Use the S2AS notation

```text
r_i=rho(e_i^*),       p_j=pi(e_j^*),
q_k=theta(e_k^*),

A=lambda^(-1)r_s,     B=mu^(-1)p_t,
h_k=q_k-z_k A-w_k B.                                (7)
```

The seven annihilator-basis rows are

```text
r_t,r_u,p_s,p_u,h_0,h_1,h_2.                        (8)
```

Suppose first

```text
N subset {alpha_u=0}.                                (9)
```

Deleting `r_u` from (8) leaves a six-dimensional domain with
four-dimensional kernel.  Its image is therefore a two-plane `S`, and

```text
P=span(p_s,p_u)=S,
r_t in S,                 h(A_3^*) subset S.         (10)
```

The complete untouched table of S2AS has only its `(u,u,u)` target on
`span(r_t,r_u) x P x image theta`.  Its `r_t` row is identically zero, so

```text
per(r_t,S,Q)=0,                Q=image theta.         (11)
```

We also need the exact dimension of `Q`.  Modulo `V=H^T((ker D_B)^perp)`,
equation (7) is

```text
q(gamma) congruent gamma(z)A+gamma(w)B.              (12)
```

The induced map

```text
(A_1^* direct-sum A_2^* direct-sum A_3^*)/L
  ---> W/V
```

is injective: a representative whose row lies in `V=H^T(L)` differs from
an element of `L` by an element of `ker H^T=N subset L`.  Both sides have
dimension two, so it is an isomorphism.  The classes represented by the
first-root `s` coordinate and second-root `t` coordinate form a basis of
the source quotient.  Their row classes are nonzero multiples of `A,B`;
hence `A,B` are independent modulo `V`.  Since `z,w` are independent,
(12) has rank two.

Let `0!=n` span `z^perp intersect w^perp`.  Then `q(n)=h(n) in S` is
nonzero.  Otherwise `q(n)=theta(n)=0` would say that `n` annihilates the
third projection of `K`.  Contracting the physical coefficient equation in
the third root coordinate would then kill the all-cross term.  It would
also kill `D_B(K)=U`: the first two summands of (6) have third factors
`z,w`, and the last has third factor in `pr_3 K`.  The target contraction
`sum_c n_c T_c` is nonzero because the three `T_c` are linearly independent
and `n!=0`.  Therefore

```text
dim Q=3.                                               (13)
```

## 2. The exterior target becomes a square

For `gamma in z^perp`, the second exterior face from S2AS is

```text
per(r_t,B,q(gamma))=c gamma_t T_t,
c!=0.                                                 (14)
```

The restrictions of `gamma_t` and `gamma(w)` to the two-plane `z^perp`
are both nonzero.  The first assertion is exactly `z not proportional e_t`;
the second follows from the independence of `z,w`.  Over the infinite field
choose `gamma in z^perp` with

```text
gamma_t gamma(w)!=0.                                 (15)
```

Put `q=q(gamma)`.  By (7),

```text
q=gamma(w)B+h(gamma),              h(gamma) in S.   (16)
```

Equation (11) kills the term containing `h(gamma)`, so (14)--(16) give

```text
per(q,q,r_t)=c gamma_t gamma(w) T_t!=0.              (17)
```

Thus a target face originally linear in `B` is an actual nonzero
decomposable square at one vector of `Q`.

## 3. The zero row forces `r_t` to be pure

Write `r_t` by its source support in
`W=X direct-sum Y direct-sum Z`.

If all three source components are nonzero, the kernel of the square map

```text
q |-> per(r_t,r_t,q)                                 (18)
```

is the two-dimensional scaling plane.  Equation (11), with `r_t in S`,
puts the three-plane `Q` in that kernel, contradicting (13).

Suppose exactly two components are nonzero.  After permuting sources write

```text
r_t=x+y,                    x y!=0.                  (19)
```

The square-zero part of (11) gives

```text
Q subset X direct-sum Y.                             (20)
```

For any `p in S` and `q' in Q`, the remaining mixed equation is

```text
per(r_t,p,q')
 =p_Z tensor (x tensor q'_Y+q'_X tensor y)=0.        (21)
```

The parenthesized linear map has a one-dimensional kernel, whereas `Q` has
dimension three.  Hence `p_Z=0` for every `p in S`.  Thus both `S` and `Q`
lie in `X direct-sum Y`, making the square in (17) zero.  This contradiction
excludes two-source support.

Consequently, after a source permutation,

```text
r_t=x in X,                     x!=0.                (22)
```

Write the vector in (17) as `q=(q_X,y,zeta)`.  Its square is

```text
per(q,q,x)=2 x tensor y tensor zeta.                 (23)
```

Both `y,zeta` are nonzero, and (23) says that the three factor lines of
`T_t` are

```text
span(x),             span(y),             span(zeta). (24)
```

## 4. The remaining targets cannot be transverse

Equation (11) and (22) say that for every `p in S`, `q' in Q`,

```text
p_Y tensor q'_Z+q'_Y tensor p_Z=0.                  (25)
```

Apply (25) to the vector `q` in (23).  There is a linear functional
`a:S->K` such that

```text
p_Y=a(p)y,                 p_Z=-a(p)zeta.            (26)
```

There are two cases.

### The functional `a` is zero

Then `S subset X`.  The three nonzero target values are

```text
per(A,p_s,q_s') in span(T_s),
per(q,q,r_t)     in span(T_t),
per(r_u,p_u,q_u) in span(T_u),                       (27)
```

where the first is supplied by the nonzero first exterior face (use (3))
and the last is the untouched core target.  Since `p_s,p_u,r_t` are pure in
`X`, they must supply the `X` factor lines of `T_s,T_u,T_t`, respectively.
Those are the three independent target-coordinate lines in `X`, but all
three vectors lie in the two-plane `S`.  Contradiction.

### The functional `a` is nonzero

Choose `p_0 in S` with `a(p_0)!=0`.  Equation (25) then makes every
`q' in Q` satisfy, for a scalar `b(q')`,

```text
q'_Y=b(q')y,                 q'_Z=b(q')zeta.         (28)
```

For arbitrary `C in W`, direct expansion of (26)--(28) gives

```text
per(C,p,q') in
 X tensor Y tensor span(zeta)
 +X tensor span(y) tensor Z.                         (29)
```

A nonzero decomposable tensor in (29) shares the `Y` factor line `span(y)`
or the `Z` factor line `span(zeta)`: project to
`(Y/span(y)) tensor (Z/span(zeta))`.  Hence it shares a factor with `T_t`.

Both the nonzero `T_s` exterior value and the nonzero `T_u` core value in
(27) have the form on the left of (29), with their middle argument in `S`
and third argument in `Q`.  They are fully transverse to `T_t`, contrary to
(29).  This excludes the second case.

Both possibilities in (26) are impossible, so (9) cannot occur.

## 5. Symmetry and proof-topology consequence

Exchange the first two roots and their associated nonroot source factors,
exchange `z,w`, and exchange target colours `s,t`.  The normal form (2),
hypotheses (3), and target equations are preserved.  The excluded
alternative `alpha_u=0` becomes `beta_u=0`.  This proves both assertions in
(4).

The S2AS four-coloop residual in the distinct-colour central chart is now

```text
alpha_u=0 or beta_u=0:                              IMPOSSIBLE;

alpha_t=0 or beta_s=0:                              OPEN;

w proportional e_s or z proportional e_t:          OPEN;

same-colour central chart / outer coordinate-pair
charts / other (1,1,2) boundaries:                  OPEN;

(1,2,2), joint rank at most four, other physical
branches and higher orders:                         OPEN;

global Krenn--Gu conjecture:                         UNRESOLVED.      (30)
```

No finite scan, numerical argument, or generic-point promotion enters the
proof.

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_one_two_third_colour_coloop_exclusion.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_one_two_third_colour_coloop_exclusion.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_one_two_third_colour_coloop_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_one_two_third_colour_coloop_exclusion.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_one_two_third_colour_coloop_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_one_two_third_colour_coloop_exclusion.py
```

The primary replay checks the coloop rank geometry, exact third-row rank,
square upgrade, source-support split, pure-row conjugate projections, and
factor-sharing quotient.  The independent no-import audit uses rational
arithmetic, a separate elimination and permanent implementation, a
third-index-major tensor convention, and independent pure/two-/three-source
models.
