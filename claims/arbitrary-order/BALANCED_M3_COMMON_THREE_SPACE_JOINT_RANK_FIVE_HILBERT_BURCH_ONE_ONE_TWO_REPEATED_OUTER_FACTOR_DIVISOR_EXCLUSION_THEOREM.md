# Balanced `m=3` joint-rank-five Hilbert--Burch `(1,1,2)` repeated-outer-factor divisor exclusion

## Status

**Exact characteristic-zero exclusion of the single repeated-outer-factor
divisors in the distinct-colour central chart of the `(1,1,2)`
Hilbert--Burch boundary.**  Retain the normalized, target-consistent physical
`m=3` common-three-space full-sensor hypotheses

```text
dim U=3,                         rank H=5.             (1)
```

Let `s,t,u` be the three distinct target colours.  In the S2AS central
coordinate chart, write one repeated divisor as

```text
ker D_B=span{(lambda e_s,0,z),(0,mu e_t,nu e_s)},
lambda mu nu!=0,
z not proportional to e_s,
z not proportional to e_t.                           (2)
```

Then (2) is impossible.  By exchanging the first two roots, the symmetric
divisor

```text
ker D_B=span{(lambda e_s,0,nu e_t),(0,mu e_t,w)},
w not proportional to e_t,
w not proportional to e_s                            (3)
```

is also impossible.  Thus, in the distinct-colour central chart, S2AU and
this theorem leave only the **simultaneous** repeated intersection

```text
z proportional to e_t,              w proportional to e_s. (4)
```

The proof replaces the exterior `T_s` face that vanishes on (2).  Exact
transpose recovery still gives a finite hyperplane fork.  A new one-face
equal-plane lemma uses the surviving exterior `T_t` and untouched `T_u`
core to eliminate every combined-row alternative.  Four ordinary coloops
remain.  The two first-root coloops follow from strengthened one-sided
versions of S2AT--S2AU.  The two second-root coloops require new exact
permanent lemmas: one uses a common radical, the other a complete zero
rectangle.  In both, the nonzero alternating separated tensor forced by
full singleton rank leaves a canonical source-support model in which every
decomposable exterior value shares a factor with `T_u`, contradicting the
fully transverse `T_t` face.

This theorem does not treat the double intersection (4), the same-colour
central chart, a genuinely outer coordinate-pair chart, the rest of
`(1,1,2)`, `(1,2,2)`, joint rank at most four, another physical branch,
higher orders, or the global conjecture.  Global Krenn--Gu remains
**UNRESOLVED**.

## 1. Derivative, rows, and the surviving exterior face

The root--root blocks and derivative on (2) are

```text
B_23=-mu e_t tensor z,
B_13=-lambda nu e_s tensor e_s,
B_12= lambda mu e_s tensor e_t,

D_B(a,b,c)
 =-mu a tensor e_t tensor z
  -lambda nu e_s tensor b tensor e_s
  +lambda mu e_s tensor e_t tensor c.                (5)
```

Use the S2AS row notation

```text
r_i=rho(e_i^*),       p_j=pi(e_j^*),
q_k=theta(e_k^*),     T_k=X_k tensor Y_k tensor Z_k,

A=lambda^(-1)r_s,     B=mu^(-1)p_t,
h_k=q_k-z_k A-nu delta_(k,s)B.                       (6)
```

Put

```text
R=span(r_t,r_u),             P=span(p_s,p_u),
Q=image theta.                                            (7)
```

The annihilator of the derivative kernel is

```text
L={ (alpha,beta,gamma):
      lambda alpha_s+gamma(z)=0,
      mu beta_t+nu gamma_s=0 },             dim L=7. (8)
```

Its seven row images are

```text
r_t,r_u,p_s,p_u,h_0,h_1,h_2.                         (9)
```

For a product root functional, transpose of (5) is

```text
D_B^T(alpha tensor beta tensor gamma)
 =(-mu beta_t gamma(z)alpha,
   -lambda nu alpha_s gamma_s beta,
    lambda mu alpha_s beta_t gamma).                 (10)
```

Substitution of (8) gives the exact repeated-divisor recovery identity

```text
D_B^T(alpha tensor beta tensor gamma)
 =nu gamma(z)gamma_s(alpha,beta,gamma),
                                  (alpha,beta,gamma) in L. (11)
```

Every root coefficient with `i!=s` and `j!=t` is untouched by (5), so the
complete rectangular table remains

```text
per(r_i,p_j,q_k)=delta_(i,j,k)T_k,
             i in {t,u}, j in {s,u}, 0<=k<=2.       (12)
```

In particular, (12) contains only the nonzero core `T_u`.  Since the third
projection of `K=image H` contains the independent vectors `z,e_s`,

```text
dim Q>=2.                                             (13)
```

For `gamma in z^perp`, (5) has zero correction on the second exterior
face.  Hence

```text
per(r_t,B,q(gamma))=mu^(-1)gamma_t T_t.              (14)
```

The restrictions of `gamma_t` and `gamma_s` to `z^perp` are nonzero by
(2).  Over the infinite characteristic-zero field choose

```text
gamma_* in z^perp,       gamma_*t gamma_*s!=0,
q_*=q(gamma_*).                                      (15)
```

Equation (6) becomes

```text
q_*=nu gamma_*s B+h(gamma_*).                        (16)
```

This is the one surviving exterior target used throughout the proof.

## 2. The repeated-divisor torus fork

For a point of `L`, all nine target-coordinate evaluations are nonzero
exactly when

```text
alpha_t,alpha_u,beta_s,beta_u,
gamma_s,gamma_t,gamma_u,gamma(z)                    (17)
```

are nonzero.  If a point of `N=K^perp subset L` avoided their zero
hyperplanes, (11) would produce a fully supported product annihilator of
`U=D_B(K)`, contrary to S2R.  Thus the four-plane `N` is covered by the
eight hyperplanes in (17).  Some may coincide when `z` is itself a target
coordinate; this only shortens the cover.  A vector space over an infinite
field cannot be a finite union of proper subspaces, so `N` is contained in
one fixed hyperplane.

If that hyperplane is `gamma_k=0` or `gamma(z)=0`, deleting the corresponding
combined row or restricting (9) to the six-dimensional hyperplane leaves
four-dimensional kernel and two-dimensional image.  It contains both
two-planes in (7), hence

```text
R=P.                                                  (18)
```

We now exclude (18) without the vanished `T_s` face.

### Lemma 1 (one-face equal-plane obstruction)

Let `S` be a two-plane in `W=X direct-sum Y direct-sum Z`, let `Q` have
dimension at least two, and choose a basis `v,d` of `S`.  Suppose

```text
per(v,S,Q)=0,
per(d,d,q_u)=T_u!=0,
per(C,v,q_*)=T_t!=0,                                (19)
```

where `T_t,T_u` are decomposable and fully transverse.  Then (19) is
impossible.

#### Proof

Split `v` by its source support.

If `v=x+y+zeta` has all three components nonzero, the square kernel

```text
{q:per(v,v,q)=0}
 ={(a x,b y,c zeta):a+b+c=0}                        (20)
```

is a two-plane.  Thus `Q` is this plane.  Comparing the coefficients of
`a,b,c` in `per(v,d,q)=0` gives

```text
x tensor d_Y=d_X tensor y,
y tensor d_Z=d_Y tensor zeta.                       (21)
```

Consequently `d` is proportional to `v`, contradicting `dim S=2`.

If `v=x+y` has exactly two components, square zero puts `Q` in
`X direct-sum Y`.  With

```text
L(q)=x tensor q_Y+q_X tensor y,
```

the mixed zero is `d_Z tensor L(q)=0`.  If `d_Z!=0`, then `Q` lies in the
one-dimensional kernel `span(x,-y)` of `L`; if `d_Z=0`, the core square in
(19) has no `Z` source.  Both alternatives are impossible.

It remains that `v=x` is pure in one source.  The mixed zero says

```text
d_Y tensor q_Z+q_Y tensor d_Z=0,             q in Q. (22)
```

The nonzero core forces `d_Y,d_Z!=0`, and (22) gives

```text
q_Y=a(q)d_Y,                    q_Z=-a(q)d_Z.        (23)
```

Direct expansion then gives

```text
per(d,d,q)=2 q_X tensor d_Y tensor d_Z.             (24)
```

Thus `T_u` has factor lines `d_Y,d_Z`.  On the other hand,

```text
per(C,v,q)
 =a(q)x tensor(d_Y tensor C_Z-C_Y tensor d_Z).      (25)
```

A nonzero rank-one matrix in the parenthesis of (25) has row line `d_Y`
or column line `d_Z`; this is the elementary two-ruling description of a
Segre tangent.  Hence the decomposable `T_t` shares a factor with `T_u`,
the final contradiction.  QED.

If (18) holds, permanent symmetry applied to (12) aligns the two radical
lines `span(r_t)=span(p_s)`.  After rescaling a complementary vector, (12)
has the form

```text
per(v,S,Q)=0,                  per(d,d,q(gamma))=gamma_u T_u. (26)
```

Equation (14) supplies the last value in (19), with `C=B` and `q_*` from
(15).  Lemma 1 excludes (18).  The torus fork therefore leaves only

```text
N subset {alpha_t=0},  {alpha_u=0},
         {beta_s=0},   or {beta_u=0}.                (27)
```

## 3. Coloop geometry, the third-row rank, and full singleton rank

If `N` lies in one coordinate hyperplane in (27), the corresponding row in
(9) is a primal coloop.  Deleting it leaves a six-dimensional domain with
the same four-dimensional relation kernel, so the other six rows span a
two-plane `S`; the deleted row lies outside `S` and completes

```text
V=H^T(L),                         dim V=3.            (28)
```

In every coloop orientation,

```text
dim Q=3.                                             (29)
```

Indeed, modulo `V`, (6) reads

```text
q(gamma) congruent gamma(z)A+nu gamma_s B.           (30)
```

The classes of `A,B` form a basis of the two-dimensional source quotient,
and the independent forms `gamma(z),gamma_s` give quotient rank two.  Let
`0!=n` span `z^perp intersect e_s^perp`.  Then `q(n)=h(n) in S` is nonzero:
if it vanished, third-root contraction by `n` would kill the all-cross term
and every summand of `D_B(K)`, while the target contraction
`sum_c n_cT_c` is nonzero.  This supplies the third direction in (29).

For a basis `v_0,v_1,v_2` of `V`, define the alternating separated tensor

```text
Alt(v_0,v_1,v_2)
 =sum_(sigma in S_3) sign(sigma)
   (v_(sigma(1)))_X tensor
   (v_(sigma(2)))_Y tensor
   (v_(sigma(3)))_Z.                                (31)
```

The restriction `D_B|K` has kernel exactly `ker D_B` and identifies
`K/ker D_B` with the three-dimensional singleton span `U`.  The three
separately linear singleton columns are the `X,Y,Z` components of this
quotient map.  Their generic determinant is (31).  Physical full-sensor
rank therefore gives

```text
Alt(v_0,v_1,v_2)!=0.                                (32)
```

We next record the two exact permanent lemmas needed for the second-root
coloops.

## 4. Two full-sensor coloop lemmas

### Lemma 2 (common-radical coloop factor lemma)

Let `S=span(v,d)=span(a,b)` be a two-plane, let `p` complete it to a
three-plane `V`, and let `dim Q=3`.  Assume

```text
Alt(v,d,p)!=0,
per(v,S,Q)=0,
per(a,p,Q)=0,
per(b,p,q)=ell(q)T,                                 (33)
```

where the last map has rank one and `T` is nonzero decomposable.  Then every
nonzero decomposable value

```text
per(a,C,q),                    C in W, q in Q,       (34)
```

shares a source factor line with `T`.

#### Proof

If `v` has all three source components, its square kernel has dimension two,
contrary to `dim Q=3`.

If `v=x+y` has exactly two components, square zero puts `Q` in
`X direct-sum Y`.  The mixed zero with `d` says

```text
d_Z tensor(x tensor q_Y+q_X tensor y)=0.            (35)
```

If `d_Z!=0`, then `dim Q<=1`; hence `S subset X direct-sum Y`.  Nonvanishing
of (31) forces `p_Z!=0` and a nonzero alternating `X,Y` minor.  The zero
`per(a,p,Q)=0` now puts the three-plane `Q` in the kernel of
`q |-> a_X tensor q_Y+q_X tensor a_Y`.  Thus `a` is pure in `X` or `Y` and
`Q` is that complete three-dimensional source.  The nonzero map in the
last line of (33) then has rank three, not one.  This excludes two-source
`v`.

After a source permutation, let `v=x` be pure.  Write
`d=(d_X,d_Y,d_Z)`.  The radical equation is

```text
d_Y tensor q_Z+q_Y tensor d_Z=0.                    (36)
```

Nonvanishing of (31) says

```text
D=d_Y tensor p_Z-p_Y tensor d_Z!=0.                 (37)
```

If exactly one of `d_Y,d_Z` vanishes, (36) removes that source from `Q`.
The zero map with `a` then makes `Q` a complete pure source, and the last
map in (33) again has rank zero or three.  Thus `d_Y,d_Z` are both nonzero.
Equation (36) has the exact form

```text
q_Y=tau(q)d_Y,                 q_Z=-tau(q)d_Z.       (38)
```

If `tau` vanished on all of `Q`, the last map in (33) would again have rank
zero or three.  Hence `ker(tau|Q)` is a two-plane in `X`.  Write
`a=A v+B d`.  Evaluation of `per(a,p,Q)=0` first on that two-plane and then
at one point with `tau=1` gives

```text
B!=0,
d_Y tensor p_Z+p_Y tensor d_Z=0,
a_X=0.                                               (39)
```

Together with (37), (39) gives nonzero `c` such that

```text
p_Y=c d_Y,                    p_Z=-c d_Z.            (40)
```

After rescaling, `a=d_Y+d_Z` and the rank-one core in (33) has factor lines

```text
T in span(x tensor d_Y tensor d_Z).                 (41)
```

Finally, (38) gives

```text
per(a,C,q)
 =q_X tensor(d_Y tensor C_Z+C_Y tensor d_Z).        (42)
```

If (42) is nonzero decomposable, its `Y,Z` matrix has rank one.  It lies in
the Segre tangent `d_Y tensor Z+Y tensor d_Z`, so it has row line `d_Y` or
column line `d_Z`.  Equations (41)--(42) prove the lemma.  QED.

### Lemma 3 (zero-rectangle coloop factor lemma)

Let `S=span(a,b)` be a two-plane, let `p` complete it to `V`, let
`0!=v in S`, and let `dim Q=3`.  Assume

```text
Alt(a,b,p)!=0,
per(p,S,Q)=0,
per(a,v,Q)=0,
per(b,v,q)=ell(q)T,                                 (43)
```

where the last map has rank one and `T` is nonzero decomposable.  Then every
nonzero decomposable value `per(a,C,q)`, with `C in W,q in Q`, shares a
source factor line with `T`.

#### Proof

We split `p` by source support.

If `p=x` is pure, (32) says

```text
a_Y tensor b_Z-b_Y tensor a_Z!=0.                   (44)
```

The two equations `per(p,a,q)=per(p,b,q)=0` and (44) force
`q_Y=q_Z=0`.  Thus `Q=X`.  Every map `per(s,t,-)|Q` with `s,t in S` has
rank zero or three, contradicting the last rank-one map in (43).

Suppose `p=x+y` has exactly two components and put `k=x-y`.  For
`s=(s_X,s_Y,s_Z)` define

```text
L(s)=x tensor s_Y+s_X tensor y.                     (45)
```

Direct expansion gives

```text
per(p,s,q)=L(s) tensor q_Z+L(q) tensor s_Z.          (46)
```

The kernel in `q` has dimension at least three exactly on the union

```text
X direct-sum Y,
span(k) direct-sum Z.                               (47)
```

Indeed, both spaces in (47) are immediate from (46).  Outside them,
`L(s),s_Z` are nonzero and (46) gives
`q_Z=c s_Z`, `L(q)=-cL(s)`, leaving only the two parameters `c` and the
kernel line `span(k)` of `L`.

Every point of `S` has a kernel containing the three-plane `Q`, so the
two-plane `S` is contained in the finite union (47).  Over the infinite
field it lies in one member.  The first member would make (31) zero;
therefore

```text
S subset span(k) direct-sum Z.                      (48)
```

Nonvanishing of (31) gives a row of `S` with nonzero `Z` component, and
(46) then forces

```text
Q subset span(k) direct-sum Z.                      (49)
```

Every nonzero value on `S x S x Q` has the two fixed factor lines `x,y`,
so `T` has those lines.  For arbitrary `C`, expansion of (48)--(49) puts

```text
per(a,C,q) in
 X tensor span(y) tensor Z
 +span(x) tensor Y tensor Z.                        (50)
```

A decomposable tensor in (50) has `X` factor `x` or `Y` factor `y`, proving
the lemma in this case.

It remains that `p=x+y+zeta` has all three components.  The exact
rank-drop atlas for

```text
q |-> per(p,s,q)                                    (51)
```

is

```text
dim ker(51)>=3
iff s belongs to L_X union L_Y union L_Z,

L_X=X direct-sum span(y-zeta),
L_Y=Y direct-sum span(x-zeta),
L_Z=Z direct-sum span(x-y).                         (52)
```

For completeness, extend `x,y,zeta` to source bases.  If `s` has an
off-base component in exactly one source, say `s_X=u`, coefficient
comparison gives

```text
per(p,s,q)
 =(u+b x) tensor y tensor q_Z
  +(u+c x) tensor q_Y tensor zeta
  +(b+c)q_X tensor y tensor zeta.                   (53)
```

Its kernel has dimension at least three exactly when `b+c=0`, namely
`s in L_X`.  If no source has an off-base component, the three coefficients
are `a+b,a+c,b+c`, and the same conclusion is (52).  If at least two
sources have off-base components, projection to the corresponding two
source quotients first fixes their components of `q` up to one common
scalar; the remaining one-source projections leave at most one further
scalar.  Thus the kernel has dimension at most two.  This proves (52).

As before, the finite-union argument puts `S` in one member, say `L_X`.
Write a basis

```text
s_i=(u_i,a_i y,-a_i zeta),                  i=1,2.  (54)
```

Its alternating separated tensor is

```text
Alt(s_1,s_2,p)
 =2(a_2u_1-a_1u_2) tensor y tensor zeta.             (55)
```

Nonvanishing of (55) makes the common kernel of the two maps (51) exactly
the pure source `X`: a solution with a nonzero `Y` or `Z` component in
(53) would make `a_2u_1-a_1u_2=0`.  Hence `Q=X`.  For `s,t in L_X`,

```text
per(s,t,q)=-2a(s)a(t)q_X tensor y tensor zeta.       (56)
```

Its restriction to the three-dimensional `Q=X` has rank zero or three,
again contradicting the last line of (43).  The full-source case is
impossible, and the two-source case already proved the factor-sharing
conclusion.  QED.

## 5. Excluding the four ordinary coloops

We apply the preceding geometry to (27).

### The coloop `alpha_t=0`

Deleting `r_t` gives

```text
S=P=span(p_s,p_u),
r_u,h(A_3^*) subset S,
r_t notin S,
per(r_t,S,Q)=0,
per(r_u,p_u,q_u)=T_u.                               (57)
```

Equations (14)--(16) upgrade the exterior target to the square

```text
per(q_*,q_*,r_t) in span(T_t) minus {0}.             (58)
```

The abstract external-zero-row square/core lemma proved in Sections 3--4
of S2AU uses only (29), (57), (58), and transversality of `T_t,T_u`.  Its
one-source case gives a zero or factor-sharing core; its two-source case
puts `Q` in a two-dimensional fibre; and its full-source tangent atlas
leaves a one-dimensional common annihilator, a zero core, or factor
sharing.  None of those steps uses `w not proportional to e_s`; that old
hypothesis served only to obtain the symmetric `T_s` orientation.  Thus the
`alpha_t` coloop is impossible on (2).

### The coloop `alpha_u=0`

Deleting `r_u` gives

```text
S=P=span(p_s,p_u),
r_t,h(A_3^*) subset S,
per(r_t,S,Q)=0.                                      (59)
```

Again (14)--(16) give the nonzero square (58).  The source-support argument
of S2AT now works one-sided.  A full-source `r_t` has square kernel dimension
two, and a two-source `r_t` would put both `S,Q` in those two sources and
kill (58).  Hence, after permuting sources,

```text
r_t=x in X.                                         (60)
```

Writing `q_*=(q_X,y,zeta)`, the zero table gives a functional `c:S->K`
with

```text
p_Y=c(p)y,                    p_Z=-c(p)zeta.         (61)
```

If `c!=0`, the same equation for all `q in Q` puts every value
`per(C,p,q)`, `p in S`, in

```text
X tensor Y tensor span(zeta)
+X tensor span(y) tensor Z.                         (62)
```

The nonzero core `T_u=per(r_u,p_u,q_u)` has this form and would share a
factor with `T_t`, impossible.

If `c=0`, then `S subset X`.  At `q_u`, put

```text
M=(r_u)_Y tensor(q_u)_Z+(q_u)_Y tensor(r_u)_Z.
```

The two untouched entries are

```text
per(r_u,p_s,q_u)=p_s tensor M=0,
per(r_u,p_u,q_u)=p_u tensor M=T_u!=0.                (63)
```

Both `p_s,p_u` are nonzero pure `X` vectors, so (63) says simultaneously
`M=0` and `M!=0`.  Thus `alpha_u` is impossible.

### The coloop `beta_u=0`

Deleting `p_u` gives

```text
S=R=span(r_t,r_u),
p_s,h(A_3^*) subset S,
p_u notin S.                                        (64)
```

Set

```text
v=p_s,       a=r_t,       b=r_u,       p=p_u.       (65)
```

The untouched table (12) is exactly

```text
per(v,S,Q)=0,
per(a,p,Q)=0,
per(b,p,q(gamma))=gamma_u T_u.                      (66)
```

The basis `S,p` spans `V`, so (32) supplies the nonzero alternating tensor
in Lemma 2.  That lemma says the nonzero decomposable exterior value
`per(a,B,q_*)` must share a source factor with `T_u`.  Equation (14) says it
is a nonzero multiple of the fully transverse `T_t`.  Contradiction.

### The coloop `beta_s=0`

Deleting `p_s` gives

```text
S=R=span(r_t,r_u),
p_u,h(A_3^*) subset S,
p_s notin S.                                        (67)
```

Set

```text
a=r_t,       b=r_u,       v=p_u,       p=p_s.       (68)
```

Now (12) gives the complete zero rectangle and core

```text
per(p,S,Q)=0,
per(a,v,Q)=0,
per(b,v,q(gamma))=gamma_u T_u.                      (69)
```

Again `S,p` is a basis of `V`, so (32) applies.  Lemma 3 makes every
nonzero decomposable `per(a,C,q)` share a factor with `T_u`; taking
`C=B,q=q_*` contradicts the exterior `T_t` in (14).  Thus the last coloop
is impossible.

All four alternatives in (27) have been excluded, proving (2).

## 6. Symmetry and proof-topology consequence

Exchange the first two roots and their associated nonroot source factors,
exchange `z,w`, and exchange target colours `s,t`.  The normal form,
physical target equation, full-sensor determinant, and permanent lemmas are
preserved.  This sends (2) to (3), proving the symmetric assertion.

Together with S2AU, the distinct-colour central-chart frontier is now

```text
neither outer factor repeated:                      IMPOSSIBLE;
exactly one outer factor repeated:                  IMPOSSIBLE;
both outer factors repeated, (4):                   OPEN;

same-colour central / genuinely outer coordinate
charts / other (1,1,2) boundaries:                  OPEN;
(1,2,2), joint rank at most four, other physical
branches and higher orders:                         OPEN;
global Krenn--Gu conjecture:                         UNRESOLVED.      (70)
```

No finite scan, numerical specialization, generic-point promotion, or
unproved case cover enters the argument.

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_one_two_repeated_outer_factor_divisor_exclusion.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_one_two_repeated_outer_factor_divisor_exclusion.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_one_two_repeated_outer_factor_divisor_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_one_two_repeated_outer_factor_divisor_exclusion.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_one_two_repeated_outer_factor_divisor_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_one_one_two_repeated_outer_factor_divisor_exclusion.py
```

The primary replay checks the scalar-general derivative, kernel,
annihilator, repeated recovery scalar, hyperplane fork, surviving exterior
face, one-face equal-plane atlas, full-sensor alternating tensor, complete
common-radical normal form, and the pure/two-/three-source zero-rectangle
rank atlases.  The independent no-import audit uses standard-library
`Fraction`, a different tensor indexing convention, separate elimination,
and independently assembled canonical models for every support case.

## Dependencies

- [Joint-rank-five derivative and torus localization](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_DERIVATIVE_TORUS_LOCALIZATION_THEOREM.md)
- [`(1,1,2)` central-coordinate torus localization](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_ONE_TWO_CENTRAL_COORDINATE_TORUS_LOCALIZATION_THEOREM.md)
- [`(1,1,2)` third-colour coloop exclusion](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_ONE_TWO_THIRD_COLOUR_COLOOP_EXCLUSION_THEOREM.md)
- [`(1,1,2)` central-colour coloop exclusion](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_ONE_ONE_TWO_CENTRAL_COLOUR_COLOOP_EXCLUSION_THEOREM.md)
- [Support-two double-monomial exclusion](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_SUPPORT_TWO_DOUBLE_MONOMIAL_EXCLUSION_THEOREM.md)
