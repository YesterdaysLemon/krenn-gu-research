# Balanced `m=3` joint-rank-five Hilbert--Burch `(1,1,2)` central-colour coloop exclusion

## Status

**Exact characteristic-zero exclusion of the central-colour ordinary-coloop
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

Let `N=K^perp`.  Then neither alternative

```text
N subset {alpha_t=0},             N subset {beta_s=0} (4)
```

can occur.  These are the two ordinary coloops whose row colour is the
coordinate colour carried by the opposite one-dimensional kernel
projection.

Together with the third-colour exclusion S2AT, this closes every ordinary
coloop left by S2AS in the distinct-colour central chart away from (3)'s
two repeated outer-factor divisors.  It does not treat those divisors, the
same-colour central chart, an outer coordinate-pair chart, or another
Hilbert--Burch profile.  Global Krenn--Gu remains **UNRESOLVED**.

## 1. The central coloop and its three-dimensional third-row image

The derivative is

```text
D_B(a,b,c)
 =-mu a tensor e_t tensor z
  -lambda e_s tensor b tensor w
  +lambda mu e_s tensor e_t tensor c.                (5)
```

Use the S2AS notation

```text
r_i=rho(e_i^*),       p_j=pi(e_j^*),
q_k=theta(e_k^*),

A=lambda^(-1)r_s,     B=mu^(-1)p_t,
h_k=q_k-z_k A-w_k B.                                (6)
```

The seven annihilator-basis rows are

```text
r_t,r_u,p_s,p_u,h_0,h_1,h_2.                        (7)
```

Suppose first

```text
N subset {alpha_t=0}.                                (8)
```

Deleting `r_t` from (7) leaves a six-dimensional domain with the same
four-dimensional relation kernel `N`.  Its image is therefore a two-plane
`S`.  Since `p_s,p_u` are independent,

```text
P=span(p_s,p_u)=S,
r_u in S,                  h(A_3^*) subset S,
r_t notin S.                                         (9)
```

Let `V=H^T((ker D_B)^perp)` and `Q=image theta`.  Modulo `V`,

```text
q(gamma) congruent gamma(z)A+gamma(w)B.              (10)
```

The induced map from the full root dual modulo `(ker D_B)^perp` to `W/V`
is an isomorphism: its kernel is induced by `ker H^T=N`, already contained
in `(ker D_B)^perp`, and both quotients have dimension two.  Thus the row
classes of `A,B` are independent.  Independence of `z,w` makes (10) rank
two.

Let `0!=n` span `z^perp intersect w^perp`.  Then `q(n)=h(n) in S` is
nonzero.  Otherwise third-root contraction by `n` would kill the all-cross
term and all of `D_B(K)=U`: the first two summands of (5) have third factors
`z,w`, and the last has third factor in `pr_3 K`, annihilated by
`q(n)=theta(n)=0`.  The target contraction `sum_c n_c T_c` is nonzero.
Consequently

```text
dim Q=3.                                              (11)
```

For `i in {t,u}`, `j in {s,u}`, the S2AS untouched table is

```text
per(r_i,p_j,q_k)=delta_(i,j,k)T_k.                  (12)
```

Equations (9)--(12) give the load-bearing zero row and core value

```text
per(r_t,S,Q)=0,
per(r_u,p_u,q_u)=T_u!=0,       r_u,p_u in S.         (13)
```

## 2. The exterior `T_t` face is a square

For `gamma in z^perp`, S2AS gives

```text
per(r_t,B,q(gamma))=c gamma_t T_t,
c!=0.                                                 (14)
```

The restrictions of `gamma_t` and `gamma(w)` to `z^perp` are nonzero by
(3) and the independence of `z,w`.  Over the infinite field choose
`gamma in z^perp` with their product nonzero and set `q=q(gamma)`.  By (6),

```text
q=gamma(w)B+h(gamma),               h(gamma) in S.   (15)
```

The zero row (13), symmetry, and trilinearity turn (14) into

```text
per(q,q,r_t)=c gamma_t gamma(w)T_t!=0.               (16)
```

We now split `r_t` by its support in `W=X direct-sum Y direct-sum Z`.

## 3. One- and two-source support are impossible

### One source

Suppose, after a source permutation,

```text
r_t=x in X,                         x!=0.             (17)
```

Write the vector in (16) as `q=(q_X,y,zeta)`.  Then

```text
per(q,q,x)=2 x tensor y tensor zeta,                 (18)
```

so `y,zeta` are nonzero and are the `Y,Z` factor lines of `T_t`.
For every `p in S`, (13) at this `q` says

```text
p_Y tensor zeta+y tensor p_Z=0.
```

Hence there is a linear functional `a:S->F` with

```text
p_Y=a(p)y,                    p_Z=-a(p)zeta.         (19)
```

If `a=0`, then `S subset X`.  Both `r_u,p_u` in (13) are pure in `X`, so
their permanent with any third row is zero, contradicting the nonzero
`T_u` core.

If `a!=0`, use a row `p_0` with `a(p_0)!=0` in the complete zero table
`per(r_t,p_0,Q)=0`.  Every `q' in Q` then has, for a scalar `b(q')`,

```text
q'_Y=b(q')y,                   q'_Z=b(q')zeta.       (20)
```

For arbitrary `C in W`, direct expansion of (19)--(20) gives

```text
per(C,p,q') in
 X tensor Y tensor span(zeta)
 +X tensor span(y) tensor Z.                         (21)
```

A nonzero decomposable tensor in (21) shares `span(y)` or `span(zeta)`:
project to `X tensor (Y/span(y)) tensor (Z/span(zeta))`.  The core `T_u`
in (13) has the form on the left of (21), but is fully transverse to
`T_t`.  Contradiction.

### Two sources

Suppose instead, after a source permutation,

```text
r_t=x+y,                       x y!=0.               (22)
```

For `v in W` put

```text
L(v)=x tensor v_Y+v_X tensor y.                     (23)
```

Equation (16) is

```text
per(q,q,r_t)=2 L(q) tensor q_Z!=0.                  (24)
```

Thus `L(q)` and `q_Z` are nonzero.  For every `p in S`, the zero row at
this fixed `q` is

```text
L(p) tensor q_Z+L(q) tensor p_Z=0.                  (25)
```

Cancellation of the two nonzero pure outer factors gives a unique scalar
`a(p)` such that

```text
L(p)=a(p)L(q),                  p_Z=-a(p)q_Z.        (26)
```

The functional `a` cannot vanish identically: otherwise
`S subset ker L=span(x,-y)`, contradicting `dim S=2`.  Choose
`p_0 in S` with `a(p_0)!=0`.  Applying the complete zero row to
`p_0` and an arbitrary `q' in Q` gives a scalar `b(q')` with

```text
L(q')=b(q')L(q),                q'_Z=b(q')q_Z.       (27)
```

The map `v |-> (L(v),v_Z)` has kernel exactly
`span(x,-y,0)`.  Equation (27) therefore puts `Q` in the sum of the line
`span(q)` and that one-dimensional kernel.  This contradicts (11).

## 4. The full-source square lemma

It remains to suppose

```text
r_t=x+y+zeta,                 x y zeta!=0.           (28)
```

The repeated vector `q` in (16) must use at least two sources.  We treat
its two possible support sizes separately.

### The square vector uses exactly two sources

After a source permutation write

```text
q=a+b,                         a b!=0,
a in X,                        b in Y.               (29)
```

Then

```text
per(q,q,r_t)=2 a tensor b tensor zeta
              in span(T_t) minus {0}.                (30)
```

Put, for `p in W`,

```text
D=x tensor b+a tensor y,
M(p)=p_X tensor b+a tensor p_Y.                     (31)
```

The zero equation at `q` is exactly

```text
D tensor p_Z+M(p) tensor zeta=0.                    (32)
```

If `D!=0`, cancellation in (32), together with
`ker M=span(a,-b)`, gives the exact two-dimensional kernel

```text
span{(-x,-y,zeta),(a,-b,0)}.                        (33)
```

Thus `S` is the complete kernel.  Direct substitution of the two rows in
(33) into `per(r_t,S,q')=0` gives

```text
{q' in W:per(r_t,S,q')=0}=span(q),                  (34)
```

contradicting the three-dimensional `Q`.

If `D=0`, then `x=lambda a` and `y=-lambda b` for one nonzero scalar
`lambda`.  The kernel of (32) is

```text
span(a,-b,0) direct-sum Z.                           (35)
```

If `S subset Z`, its two rows cannot produce the nonzero core `T_u`.
Otherwise choose `p_0 in S` with nonzero component on `(a,-b,0)` and
`0!=p_1 in S intersect Z`.  The equations
`per(r_t,p_1,Q)=per(r_t,p_0,Q)=0` first force

```text
q'_X=c a,                       q'_Y=c b,
```

and then force `q'_Z=0` in characteristic zero.  Hence
`Q subset span(q)`, again contradicting (11).

### The square vector uses all three sources

Now the square in (16) lies in the Segre tangent space at
`q_X tensor q_Y tensor q_Z`:

```text
(1/2)per(q,q,r_t)
 =x tensor q_Y tensor q_Z
  +q_X tensor y tensor q_Z
  +q_X tensor q_Y tensor zeta.                      (36)
```

A nonzero decomposable tensor in this tangent space shares at least two
factor lines with that base point.  Indeed, its projections to each
quotient of two base lines vanish; the three resulting alternatives force
at least two shared lines.

After a source permutation, the `Y,Z` factor lines of `T_t` are
`span(q_Y),span(q_Z)`.  Project (36) first to `Y/span(q_Y)` and then to
`Z/span(q_Z)`.  Since all components of `q` are nonzero, this forces
`y in span(q_Y)` and `zeta in span(q_Z)`.  Thus the same two target factor
lines are `span(y),span(zeta)`, and there are nonzero scalars `b,c` and a
nonzero `a in X` such that

```text
q=(a,b y,c zeta),

per(q,q,r_t)
 =2(bc x+(b+c)a) tensor y tensor zeta!=0.            (37)
```

For `p in W`, direct expansion of `per(r_t,p,q)=0` is

```text
(a+c x) tensor p_Y tensor zeta
 +(a+b x) tensor y tensor p_Z
 +(b+c)p_X tensor y tensor zeta=0.                  (38)
```

Every `p in S` satisfies (38).  We exhaust its exact degeneracies.

Suppose first that `a` and `x` are independent.  If `b+c!=0`, (38) has
the exact two-dimensional kernel

```text
p_Y=alpha y,                    p_Z=beta zeta,

p_X=-((alpha+beta)a+(c alpha+b beta)x)/(b+c).        (39)
```

Thus `S` is this complete kernel.  Substitution of the two basis rows
`(alpha,beta)=(1,0),(0,1)` into `per(r_t,S,q')=0`, followed by coefficient
comparison off `span(y)`, off `span(zeta)`, and in the independent `x,a`
directions, gives

```text
{q' in W:per(r_t,S,q')=0}=span(q).                  (40)
```

This contradicts `dim Q=3`.

If `b+c=0`, then `b=-c!=0`.  The two vectors `a-bx,a+bx` are independent,
so (38) has kernel exactly `X`.  Thus `S subset X`, making the core in
(13) zero.

It remains that `a=A x` for one nonzero scalar `A`.  Equation (38) becomes

```text
(A+c)x tensor p_Y tensor zeta
 +(A+b)x tensor y tensor p_Z
 +(b+c)p_X tensor y tensor zeta=0.                  (41)
```

The three coefficients in (41) cannot all vanish in characteristic zero
with `b,c!=0`.  If at most one vanishes, every vector in the kernel of
(41) has at least two source components confined to the corresponding base
lines.  Hence, after a source permutation,

```text
per(S,S,W) subset
 X tensor Y tensor span(zeta)
 +X tensor span(y) tensor Z.                         (42)
```

A decomposable tensor in (42) shares one of those two lines with `T_t`, so
it cannot be the transverse core `T_u`.

Finally suppose exactly two coefficients vanish.  After rescaling and a
source permutation,

```text
q=(x,y,-zeta),
ker(41)=X direct-sum Y.                              (43)
```

Thus `S subset X direct-sum Y`.  For any `q' in Q`, project
`per(r_t,S,q')=0` to the quotient `Z/span(zeta)`.  At `p in S` the result
is

```text
(x tensor p_Y+p_X tensor y) tensor
       (q'_Z mod span(zeta))=0.                     (44)
```

The tangent map `p |-> x tensor p_Y+p_X tensor y` has one-dimensional
kernel `span(x,-y)`.  Since `dim S=2`, it is nonzero at some `p`, and (44)
forces `q'_Z in span(zeta)` for every `q' in Q`.  Both rows in the core
belong to `S` and have zero `Z` component, so every nonzero
`per(S,S,Q)` has `Z` factor `span(zeta)`.  Again `T_u` would share a factor
with `T_t`.

All full-source cases contradict (11) or the nonzero fully transverse core.
Together with Sections 3--4, every possible source support for `r_t` is
impossible.  This excludes (8).

## 5. Symmetry and proof-topology consequence

Exchange the first two roots and their associated source factors, exchange
`z,w`, and exchange target colours `s,t`.  The normal form (2), hypotheses
(3), and target equations are preserved.  The alternative `alpha_t=0`
becomes `beta_s=0`, proving both assertions in (4).

Combining S2AS, S2AT, and this theorem gives

```text
distinct-colour central coordinate-pair chart,
away from w proportional e_s and z proportional e_t: IMPOSSIBLE;

repeated outer lines:                                OPEN;

same-colour central chart / outer coordinate-pair
charts / other (1,1,2) boundaries:                   OPEN;

(1,2,2), joint rank at most four, other physical
branches and higher orders:                          OPEN;

global Krenn--Gu conjecture:                          UNRESOLVED.     (45)
```

No finite scan, numerical argument, or generic-point promotion enters the
proof.

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_one_two_central_colour_coloop_exclusion.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_one_two_central_colour_coloop_exclusion.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_one_two_central_colour_coloop_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_one_two_central_colour_coloop_exclusion.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_one_two_central_colour_coloop_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_one_two_central_colour_coloop_exclusion.py
```

The primary replay checks the central-coloop rank geometry, exact third-row
rank, square upgrade, one-/two-source contradictions, and every
full-support tangent degeneracy.  The independent no-import audit uses
rational arithmetic, separate elimination, a third-index-major tensor
convention, and independently constructed kernel/annihilator models.
