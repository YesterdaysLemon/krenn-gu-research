# Balanced `m=3` joint-rank-five Hilbert--Burch `(1,1,2)` double-repeated outer intersection exclusion

## Status

**Exact characteristic-zero exclusion of the simultaneous repeated-outer
intersection in the distinct-colour central chart of the `(1,1,2)`
Hilbert--Burch boundary.**  Retain the normalized, target-consistent physical
`m=3` common-three-space full-sensor hypotheses

```text
dim U=3,                         rank H=5.             (1)
```

Let `s,t,u` be the three distinct target colours.  The only point left by
S2AU and S2AV in the central chart has

```text
ker D_B=span{(lambda e_s,0,nu e_t),
             (0,mu e_t,xi e_s)},
lambda mu nu xi!=0.                                  (2)
```

Then (2) is impossible.

The proof uses the exact recovery scalar `nu xi gamma_s gamma_t`.  Its seven
distinct torus factors give three combined-row and four ordinary-coloop
alternatives.  A new three-dimensional square-radical lemma excludes every
combined-row alternative.  A strengthened common-radical lemma excludes the
two third-colour coloops because `q_u=h_u` lies simultaneously in the row
plane and in the third-row image.  A strengthened zero-rectangle lemma puts
the two central-colour coloops in one two-source normal form.  The full
coefficientwise correction identity then forces `T_s` or `T_t` to share two
source factors with `T_u`, contradicting target transversality.

Together with S2AS--S2AV, this closes the complete **distinct-colour central
coordinate-pair chart** of the `(1,1,2)` profile.  It does not treat the
same-colour central chart, a genuinely outer coordinate-pair chart, the rest
of `(1,1,2)`, `(1,2,2)`, joint rank at most four, another physical component,
higher orders, or the global conjecture.  Global Krenn--Gu remains
**UNRESOLVED**.

## 1. Derivative, rows, and exact recovery

The three root--root blocks and derivative on (2) are

```text
B_23=-mu nu e_t tensor e_t,
B_13=-lambda xi e_s tensor e_s,
B_12= lambda mu e_s tensor e_t,

D_B(a,b,c)
 =-mu nu a tensor e_t tensor e_t
  -lambda xi e_s tensor b tensor e_s
  +lambda mu e_s tensor e_t tensor c.               (3)
```

Write

```text
r_i=rho(e_i^*),       p_j=pi(e_j^*),
q_k=theta(e_k^*),     T_k=X_k tensor Y_k tensor Z_k. (4)
```

Put

```text
R=span(r_t,r_u),             P=span(p_s,p_u),
A=(nu/lambda)r_s,            B=(xi/mu)p_t,

h_t=q_t-A,       h_s=q_s-B,       h_u=q_u.          (5)
```

The annihilator of the derivative kernel is

```text
L={ (alpha,beta,gamma):
      lambda alpha_s+nu gamma_t=0,
      mu beta_t+xi gamma_s=0 },       dim L=7.       (6)
```

Its seven row images are

```text
r_t,r_u,p_s,p_u,h_s,h_t,h_u.                        (7)
```

They span the three-plane

```text
V=H^T(L),                                            (8)
```

and their relation kernel is the four-plane

```text
N=K^perp subset L.                                  (9)
```

For a product root functional, transpose of (3) is

```text
D_B^T(alpha tensor beta tensor gamma)
 =(-mu nu beta_t gamma_t alpha,
   -lambda xi alpha_s gamma_s beta,
    lambda mu alpha_s beta_t gamma).                (10)
```

Substitution of (6) gives the exact recovery identity

```text
D_B^T(alpha tensor beta tensor gamma)
 =nu xi gamma_s gamma_t(alpha,beta,gamma),
                                  (alpha,beta,gamma) in L. (11)
```

Every root coefficient with `i!=s` and `j!=t` is untouched by (3).  Hence

```text
per(r_i,p_j,q_k)=delta_(i,j,k)T_k,
             i in {t,u}, j in {s,u}, k in {s,t,u}. (12)
```

Only the nonzero `T_u` core occurs in this table.

The third-row image

```text
Q=image theta                                           (13)
```

has dimension three.  Indeed, modulo `V`, (5) reads

```text
q(gamma) congruent (nu/lambda)gamma_t r_s
                   +(xi/mu)gamma_s p_t.             (14)
```

The classes of `r_s,p_t` form a basis of the two-dimensional quotient of
the full row image by `V`, because `rank H=5`.  Thus (14) has rank two.
Moreover `q_u=h_u!=0`: if it vanished, third-root contraction by `e_u^*`
would kill the all-cross term and all three summands of (3), whereas target
contraction leaves the nonzero `T_u` coefficient.  This supplies the third
direction, so

```text
dim Q=3.                                             (15)
```

For a basis `v_0,v_1,v_2` of `V`, define

```text
Alt(v_0,v_1,v_2)
 =sum_(sigma in S_3) sign(sigma)
   (v_(sigma(1)))_X tensor
   (v_(sigma(2)))_Y tensor
   (v_(sigma(3)))_Z.                                (16)
```

As in S2AV, `D_B|K` identifies `K/ker D_B` with `U`; the three separately
linear singleton columns are the three source components of the quotient
map.  Full singleton rank therefore gives

```text
Alt(v_0,v_1,v_2)!=0.                                (17)
```

## 2. The seven-factor torus fork

On `L`, all nine root-coordinate evaluations are nonzero exactly when

```text
alpha_t,alpha_u,beta_s,beta_u,gamma_s,gamma_t,gamma_u (18)
```

are nonzero.  The two recovery factors in (11) are already among these
seven coordinate factors.  If a point of `N` avoided their zero
hyperplanes, (11) would give a fully supported product annihilator of
`U=D_B(K)`, contrary to S2R.  A vector space over an infinite field cannot
be a finite union of proper subspaces, so `N` lies in one fixed hyperplane
from (18).

If `N subset {gamma_k=0}`, deleting `h_k` from (7) leaves six rows with
four-dimensional relation kernel and hence two-dimensional image.  That
image contains both two-planes `R` and `P`, so

```text
R=P.                                                 (19)
```

We first exclude all three instances of (19).

## 3. A three-dimensional square-radical obstruction

For `a,b,q in W=X direct-sum Y direct-sum Z`, write

```text
M_(a,b)(q)=per(a,b,q).                               (20)
```

### Lemma 1 (rank-one square cannot have a three-dimensional radical shore)

Let `S=span(v,d)` be a two-plane and let `dim Q=3`.  If

```text
M_(v,S)(Q)=0                                         (21)
```

then the restriction `M_(d,d)|Q` cannot have nonzero rank one.

#### Proof

Split `v` by source support.

If `v=x+y+z` has all three components nonzero, the square kernel is

```text
{(a x,b y,c z):a+b+c=0},                            (22)
```

which has dimension two.  Equation (21) includes the square zero, so it
cannot contain the three-plane `Q`.

If `v=x+y` has exactly two components, square zero puts `Q` in
`X direct-sum Y`.  The mixed zero is

```text
d_Z tensor(x tensor q_Y+q_X tensor y)=0.            (23)
```

If `d_Z!=0`, its kernel is the one line `span(x-y)`, impossible for `Q`.
Thus `d_Z=0`; then `v,d,Q` all miss `Z`, so `M_(d,d)(Q)=0`.

It remains that `v=x` is pure.  A nonzero square forces
`d_Y,d_Z!=0`, and the mixed zero gives

```text
q_Y=a(q)d_Y,                  q_Z=-a(q)d_Z.          (24)
```

The complete solution space of (24) is

```text
E=X direct-sum span(d_Y-d_Z),             dim E=4.  (25)
```

Direct expansion gives

```text
M_(d,d)(q)=2q_X tensor d_Y tensor d_Z.              (26)
```

If its restriction to `Q` had rank one, the projection of `Q` to `X`
would have dimension one.  The kernel of that projection on `E` has
dimension one, so `dim Q<=2`, a contradiction.  QED.

Assume (19).  The first row of (12) annihilates all of `P=R`; hence

```text
M_(r_t,R)(Q)=0.                                     (27)
```

Write `p_s=a r_t+b r_u`.  The zero
`M_(r_u,p_s)(Q)=0`, together with the nonzero rank-one map

```text
M_(r_u,p_u)(q(gamma))=gamma_u T_u,                  (28)
```

forces `b=0`; otherwise it would kill the nonzero square map.  Thus
`p_s` is proportional to `r_t`, and (28) is a nonzero rank-one multiple of
`M_(r_u,r_u)|Q`.  Lemma 1 contradicts (15).  Therefore none of the three
combined-row alternatives can occur.

The torus fork now leaves only

```text
N subset {alpha_t=0}, {alpha_u=0},
         {beta_s=0},  or {beta_u=0}.                (29)
```

In each case, the named row is a coloop: deleting it leaves the other six
rows in a two-plane `S`, while the deleted row completes `S` to `V`.

## 4. The third-colour coloops

We first sharpen the common-radical lemma used by S2AV.

### Lemma 2 (common radical cannot carry its nonzero core in `S intersect Q`)

Let `S=span(v,d)=span(a,b)` be a two-plane, let `p` complete it to a
three-plane `V`, and let `dim Q=3`.  Assume

```text
Alt(v,d,p)!=0,
M_(v,S)(Q)=0,
M_(a,p)(Q)=0,
M_(b,p)(q)=ell(q)T,                                 (30)
```

where the last map has nonzero rank one.  Then

```text
ell(q)=0                         for every q in S intersect Q. (31)
```

#### Proof

The full-source and two-source cases for `v` are impossible exactly as in
the common-radical atlas of S2AV.  In the full-source case the square
kernel has dimension two.  If `v=x+y`, square zero puts `Q` in
`X direct-sum Y`; the mixed zero either leaves a one-dimensional `Q` or
puts `S` there.  Nonvanishing of `Alt` then supplies the missing source in
`p`.  The zero `M_(a,p)(Q)=0` makes `a` pure and `Q` the complete
corresponding source, on which the last map has rank zero or three, not
one.

Thus, after permuting sources, `v=x` is pure.  Write
`d=(d_X,d_Y,d_Z)`.  The radical and alternating conditions are

```text
d_Y tensor q_Z+q_Y tensor d_Z=0,
d_Y tensor p_Z-p_Y tensor d_Z!=0.                   (32)
```

The rank-one core excludes either `d_Y` or `d_Z` vanishing.  Hence

```text
q=(q_X,tau(q)d_Y,-tau(q)d_Z).                       (33)
```

Write `a=A v+B d`.  Evaluating `M_(a,p)(Q)=0` first on the at least
two-dimensional space `Q intersect X` and then at a point with `tau!=0`
gives

```text
B!=0,       a_X=0,
p_Y=c d_Y,                 p_Z=-c d_Z,              (34)
```

with `c!=0` by the second line of (32).  After rescaling,

```text
S=span{x,d_Y+d_Z},
Q subset X direct-sum span(d_Y-d_Z),
ell is a nonzero multiple of tau.                   (35)
```

In characteristic zero, comparison of the `Y` and `Z` components in (35)
shows that every vector of `S intersect Q` has zero `tau`.  This is (31).
QED.

Suppose first that `N subset {alpha_u=0}`.  Deleting `r_u` gives

```text
S=P=span(p_s,p_u),
r_t,h_s,h_t,h_u subset S,
r_u notin S.                                        (36)
```

Use Lemma 2 with

```text
v=r_t,       a=p_s,       b=p_u,       p=r_u.       (37)
```

The untouched table (12) supplies all three maps in (30), with
`ell(q(gamma))=gamma_u` and `T=T_u`; (17) supplies the nonzero alternating
tensor.  But

```text
q_u=h_u in S intersect Q,             ell(q_u)=1.   (38)
```

This contradicts Lemma 2.  Thus `alpha_u` is impossible.  Exchanging the
first two roots and `s,t` excludes `beta_u`.

## 5. The central-colour coloops and the full correction identity

We need one exact refinement of the zero-rectangle atlas.

### Lemma 3 (rank-one zero rectangle normal form)

Let `S=span(a,b)` be a two-plane, let `p` complete it to `V`, let
`0!=v in S`, and let `dim Q=3`.  Assume

```text
Alt(a,b,p)!=0,
M_(p,S)(Q)=0,
M_(a,v)(Q)=0,
M_(b,v)(q)=ell(q)T,                                 (39)
```

where the last map has nonzero rank one.  Then, after permuting sources,
there are nonzero `x in X`, `y in Y`, and `z in Z` such that, with
`k=x-y`,

```text
p=x+y,
S,Q subset E=span(k) direct-sum Z,
v proportional to a proportional to z,
T in span(x tensor y tensor z),
ker(ell|Q)=Q intersect Z.                           (40)
```

In particular every permanent of three vectors in `E` belongs to

```text
span(x) tensor span(y) tensor Z.                    (41)
```

#### Proof

The pure- and full-source cases for `p` are impossible by the exact
zero-rectangle atlas of S2AV.  In the two-source case write `p=x+y` and
`k=x-y`.  Nonvanishing of `Alt` selects the only viable branch of that
atlas:

```text
S,Q subset E=span(k) direct-sum Z.                  (42)
```

For `w_i=c_i k+z_i` in `E`, direct expansion gives

```text
M_(w_1,w_2)(w_3)
 =-2 x tensor y tensor
   (c_1 c_2 z_3+c_1 c_3 z_2+c_2 c_3 z_1).          (43)
```

Write `v=c k+z`, `a=c_0 k+z_0`.  The first zero map in (39) has a
three-dimensional kernel only if

```text
c c_0=0,                     c z_0+c_0 z=0.         (44)
```

Otherwise (43) has rank three, or its kernel is exactly the pure
three-dimensional source `Z`; on that source the last map has rank zero or
three.  Since `a` is nonzero, (44) forces `c=0`, then `c_0=0`.  Thus `v,a`
are pure `Z` vectors.  Because `v in span(a,b)` and the last map is nonzero,
`b` has nonzero `k` coefficient, so `v` is proportional to `a`.  Formula
(43) now shows that the last map is a nonzero multiple of

```text
q |-> c(q)x tensor y tensor z.                      (45)
```

This proves (40), and (41) is immediate from (43).  QED.

It remains to connect the correction terms at the two touched target
diagonals.  Target consistency says

```text
G_N-J in (X tensor Y tensor Z) tensor U.             (46)
```

Pull (46) back through the isomorphism
`D_B:K/ker D_B -> U`.  There is consequently a linear map

```text
Phi:V -> X tensor Y tensor Z                         (47)
```

such that contraction by a product point of `L`, followed by (11), equals
`nu xi gamma_s gamma_t Phi(H^T(alpha,beta,gamma))`.  Comparing the seven
coefficients gives, for `i!=s`, `j!=t`,

```text
mu nu Phi(r_i)
 =delta_(i,t)T_t-per(r_i,p_t,q_t),

lambda xi Phi(p_j)
 =delta_(j,s)T_s-per(r_s,p_j,q_s),

lambda mu Phi(h_k)=per(r_s,p_t,q_k).                (48)
```

These are identities in the full target tensor space, not selected-slice
or quotient statements.

Suppose `N subset {alpha_t=0}`.  Deleting `r_t` gives

```text
S=P=span(p_s,p_u),
r_u,h_s,h_t,h_u subset S,
r_t notin S.                                        (49)
```

Apply Lemma 3 with

```text
p=r_t,       a=p_s,       b=p_u,       v=r_u.       (50)
```

The table (12) gives (39), with
`ell(q(gamma))=gamma_u` and `T=T_u`.  Since `dim Q=3`, the vectors
`q_s,q_t` form a basis of `ker ell`; Lemma 3 therefore puts both in the
pure `Z` part of `E`.  Equations (5) and (49) then give

```text
r_s,p_t,A,B in E.                                   (51)
```

Moreover Lemma 3 gives a nonzero scalar `c` with

```text
p_s=c r_u.                                          (52)
```

By (41), both permanent terms below lie in
`span(x) tensor span(y) tensor Z`.  Linearity of `Phi`, (48), and (52)
give

```text
T_s-per(r_s,p_s,q_s)
 =lambda xi Phi(p_s)
 =c lambda xi Phi(r_u)
 =-(c lambda xi/(mu nu))per(r_u,p_t,q_t).           (53)
```

Thus

```text
T_s in span(x) tensor span(y) tensor Z.             (54)
```

But Lemma 3 also puts

```text
T_u in span(x tensor y tensor z).                   (55)
```

The nonzero decomposable targets `T_s,T_u` would share their `X` and `Y`
factor lines, contradicting full target transversality.  Hence `alpha_t`
is impossible.  Root symmetry excludes `beta_s`.

All seven alternatives from the torus fork are impossible, proving (2).

## 6. Proof-topology consequence

Combining S2AS--S2AV with this theorem gives

```text
distinct-colour central (1,1,2), nonrepeated:       IMPOSSIBLE;
distinct-colour central (1,1,2), one repeated:      IMPOSSIBLE;
distinct-colour central (1,1,2), double repeated:   IMPOSSIBLE;

same-colour central / genuinely outer coordinate
charts / other (1,1,2) boundaries:                  OPEN;
(1,2,2), joint rank at most four, other physical
branches and higher orders:                         OPEN;
global Krenn--Gu conjecture:                         UNRESOLVED.      (56)
```

No finite scan, numerical specialization, generic-point promotion, or
unproved case cover enters the argument.

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_one_two_double_repeated_outer_intersection_exclusion.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_one_two_double_repeated_outer_intersection_exclusion.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_one_two_double_repeated_outer_intersection_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_one_two_double_repeated_outer_intersection_exclusion.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_one_two_double_repeated_outer_intersection_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_one_two_double_repeated_outer_intersection_exclusion.py
```

The primary replay checks the scalar-general derivative, kernel,
annihilator, recovery scalar, seven-factor fork, three-dimensional
square-radical dimension obstruction, common-radical intersection normal
form, zero-rectangle rank-one normal form, and all seven coefficientwise
correction scalings.  The independent no-import audit uses standard-library
`Fraction`, a different tensor representation, separate elimination, and
independently assembled canonical models.

## Dependencies

- [`(1,1,2)` central-coordinate torus localization](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_ONE_TWO_CENTRAL_COORDINATE_TORUS_LOCALIZATION_THEOREM.md)
- [`(1,1,2)` central-colour coloop exclusion](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_ONE_TWO_CENTRAL_COLOUR_COLOOP_EXCLUSION_THEOREM.md)
- [`(1,1,2)` repeated-outer-factor divisor exclusion](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_ONE_TWO_REPEATED_OUTER_FACTOR_DIVISOR_EXCLUSION_THEOREM.md)
- [Torus-annihilator obstruction](BALANCED_M3_SINGLETON_SPAN_TORUS_ANNIHILATOR_PERMANENT_RANK_OBSTRUCTION.md)
