# Four-root maximal-base-survivor common-incidence and sparse-radical detector boundary

## Status

**Exact characteristic-zero parent reduction, bounded mixed-target detector,
and coefficient-only no-go.**  This theorem makes one common attempt on all
eight maximal star/triangle families left by `GLD68`.

There are two distinct conclusions.

1. The three targetwise swallowed/surviving relations, even after they are
   retained in one labelled direct-sum module and combined with an aggregate
   four-port GHZ identity, do **not** force a contradiction.  Every one of the
   four stars and four triangles has an exact three-colour formal model.
2. On an actual maximum-root graph the six raw pair companions are not
   independent: they are the six pullbacks of one symmetric residual
   permanent form

   ```text
   J=P_4(xi,eta,-,-).                                  (1)
   ```

   If all four port maps have rank three, any maximal survivor family forces
   `rank J=2`.  A star forces all four port hyperplanes to contain the common
   radical plane.  A triangle forces its three sibling port hyperplanes to be
   one common maximal isotropic hyperplane; the fourth hyperplane need not
   contain the whole radical.

On that physical rank-three locus, the six internal port-pair labels have one
universal image: dimension `21` for a star and `19` for a triangle.  A
weighted concise three-colour diagonal belongs to neither image.  This closes
the internal pair layer for all eight profiles, including the triangle branch
where the fourth port projects onto the whole rank-two quotient.  It does not
kill the remaining nine labels meeting `Q`.

Every rank-two zero-diagonal `J` has a nonzero radical vector supported on at
most two root coordinates.  If one such vector belongs to all four port
images, it gives one explicit decomposable coefficient functional which kills
**all fifteen** contracted order-two deck labels.  A nonzero evaluation of the
contracted GHZ target by that functional is therefore an immediate
contradiction.  The common-image premise is automatic for a maximal star, but
the final target scalar can vanish.  For a maximal triangle, even the sparse
common-radical line is an additional incidence condition.

Thus the naive universal bridge is false as a coefficient-module argument,
while the physical common-incidence lift yields a universal pair-layer
obstruction, a genuine fifteen-label bounded detector, and an exact detector
boundary.  It does not exclude the complete scalar-zero star fibre, the
general triangle fibre, any lower-port-rank fibre, or a family with fewer than
three surviving base classes.  The global Krenn--Gu conjecture remains
**UNRESOLVED**.

The upstream inputs are the
[`GLS16` base-shadow theorem](MAXIMAL_ROOT_SURPLUS_TWO_BASE_GRADE_PAIR_SHADOW_AND_CROSS_TARGET_SELECTOR_ANNIHILATION_THEOREM.md),
the
[`GLD68` complementary-label saturation theorem](FOUR_ROOT_COMPLEMENTARY_PAIR_BASE_NUISANCE_SATURATION_AND_SEVEN_SHADOW_SOURCE_EXCLUSION_THEOREM.md),
and the standard maximum-root order-two coefficient identity.  No external
literature result is used.

## 1. One labelled module for the three relations

Work over a characteristic-zero field `K`.  Put

```text
U={0,1,2,3},                 E_u=K^3,
E_S=tensor_(u in S) E_u^*.                         (2)
```

For a pair `S`, write `bar S=U-S`.  The target-`S` base receiver is
`E_(bar S)`.  The complementary nuisance label `I=bar S` has the typed term

```text
H_(bar S) tensor Pi_(bar S) in E_(bar S) tensor E_S. (3)
```

Let `A` be one of the eight maximal survivor families.  Thus `A` contains
one edge from each complementary pair and is a star or a triangle.  Retain
the three target labels before forgetting their ownership:

```text
M_A = direct-sum_(S in A) (E_(bar S) tensor E_S).     (4)
```

The common labelled complementary map is

```text
widetilde Phi_A:
 direct-sum_(S in A) E_(bar S) -> M_A,
 (H_(bar S))_S |->
 (H_(bar S) tensor Pi_(bar S))_S.                    (5)
```

The forgetful map `sum_A:M_A->E_U` only reorders the four port factors and
adds the three labelled tensors.  Equations (4)--(5) are the common module;
they do not identify the three target-dependent annihilators in the quotient
duals.  In particular, a functional normalizing the target-`S` desired class
has no declared value on a different labelled summand.

### Theorem 1 (exact coefficient-only countermodels)

For every maximal star or triangle `A`, there are tensors satisfying

```text
Pi_S!=0 and Pi_(bar S)=0       for every S in A,       (6)

sum_(I in binom(U,2)) H_I tensor Pi_I = Delta_4       (7)
```

after the natural slot reorderings.  Consequently `GLD68` anti-simultaneity,
the labelled module (4), and the aggregate GHZ equality alone do not imply a
mixed-target contradiction.

#### Proof

Choose a bijection

```text
gamma:A->{0,1,2}.                                     (8)
```

For `S in A`, set

```text
H_S  = tensor_(u in S)     e_(gamma(S),u)^*,
Pi_S = tensor_(u in bar S) e_(gamma(S),u)^*.          (9)
```

For `I notin A`, set `H_I=Pi_I=0`.  Then (6) holds because `A` contains no
complementary pair.  Each nonzero summand in (7) is the pure four-port word
of colour `gamma(S)`, so their sum is exactly

```text
Delta_4=sum_(c=0)^2 tensor_(u in U)e_(c,u)^*.         (10)
```

The desired class at `S` may be retained in a one-dimensional quotient while
the complementary nuisance term is zero.  More explicitly, for
`I in A-{S}`, slicing the `I`-label term in the target-`S` factor leaves one
receiver factor arbitrary and fixes the other receiver factor to
`e_(gamma(I))^*`.  Since the two other members of `A` have colours different
from `gamma(S)`, neither nuisance ruling contains the desired receiver word

```text
Pi_S=tensor_(u in bar S)e_(gamma(S),u)^*.             (10a)
```

Thus the complete nuisance generated by all five foreign port-pair labels
still leaves the displayed desired class nonzero for every `S in A`.  This is
a model of the declared coefficient relations, not of the common physical
permanent incidence proved below.  Hence it disproves only the
coefficient-only implication.  `square`

## 2. The physical common residual form

Let `X=K^4` have the standard root-coordinate basis `epsilon_0,...,epsilon_3`,
and let

```text
P_4:X^4->K                                             (11)
```

be the symmetric four-linear permanent form.  For the fixed fully supported
residual contraction `z_Q=(z_(q0),z_(q1))`, put

```text
xi = L_(q0)(z_(q0)) in X,
eta= L_(q1)(z_(q1)) in X.                             (12)
```

At a port `u`, evaluation of the four root rows gives a linear map

```text
A_u:V_u->X.                                           (13)
```

The raw base companion for a port pair `S`, on the two complementary open
ports `bar S={u,v}`, is

```text
Pi_S(a_u,a_v)=P_4(xi,eta,A_u a_u,A_v a_v).            (14)
```

Define the symmetric form

```text
J(x,y)=P_4(xi,eta,x,y).                               (15)
```

Then all six companions are the six typed pullbacks

```text
Pi_S=(A_u tensor A_v)^*J,          {u,v}=bar S.       (16)
```

This is the first common physical lift of the three `GLD68` relations.  It is
strictly stronger than the formal module of Section 1.

The matrix of `J` in the root-coordinate basis has zero diagonal.  Indeed,
two equal coordinate columns cannot occur in a nonzero permanent term:

```text
J(epsilon_i,epsilon_i)=0.                             (17)
```

## 3. Rank-three maximal-profile compression

Assume for this section that every `A_u` has rank three, and put

```text
U_u=im A_u subset X,                  dim U_u=3.       (18)
```

Let `A` be the exact set of three nonzero base classes.  For `S in A`,
`b_S!=0` implies both `Pi_S!=0` and, by `GLD68`, `Pi_(bar S)=0`.  Equations
(16) therefore give

```text
J(U_s,U_t)=0                         for {s,t} in A,
J(U_s,U_t)!=0                        for {s,t} notin A. (19)
```

### Theorem 2 (one rank-two form and the two profile geometries)

Under (18)--(19):

1. `rank J=2`; write `R=rad J`, so `dim R=2`.
2. If `A` is the star centred at `0`, then

   ```text
   U_0=R+Kp,                       U_1=U_2=U_3=R+Kr,
   J(p,r)=0,                       J(p,p)J(r,r)!=0.    (20)
   ```

3. If `A` is the triangle on `{1,2,3}`, then

   ```text
   U_1=U_2=U_3=R+Kl,               J(l,l)=0,          (21)
   ```

   while `U_0` is a three-space with nonzero pairing against this common
   hyperplane.  It has `dim(U_0 intersect R)>=1`, but need not contain `R`.

The other labelled stars and triangles follow by port permutation.

#### Proof

Choose any zero edge in (19), say `J(U_s,U_t)=0`.  If `rho=rank J`, then the
restriction of `x |-> J(x,-)` to the hyperplane `U_s` has rank at least
`rho-1`.  Hence

```text
dim U_s^perp <= 4-(rho-1)=5-rho.                      (22)
```

Since the three-space `U_t` lies in `U_s^perp`, (22) gives `rho<=2`.
Nonzero blocks in (19) give `J!=0`.  A nonzero symmetric rank-one matrix is a
scalar multiple of `vv^T`; its zero diagonal would force every coordinate of
`v` to vanish.  Thus (17) excludes rank one and `rho=2`.

If two three-spaces are `J`-orthogonal, the same dimension argument shows
that each contains the two-dimensional radical `R`; their images in the
nondegenerate plane `X/R` are orthogonal lines.

For a star, apply this to each centre--leaf edge.  The orthogonal complement
of the centre line in `X/R` is unique, so all three leaf images coincide.
The nonzero leaf--leaf blocks in (19) say that the leaf line is
nonisotropic; its orthogonal centre line is then nonisotropic as well.  This
is (20).

For a triangle, the three leaf lines in `X/R` are pairwise orthogonal.  Three
nonzero lines in a nondegenerate plane can have this property only when they
are the same isotropic line.  This proves (21).  No zero edge in (19) is
incident with the centre, so only the dimension bound
`dim(U_0 intersect R)>=1` and the declared nonzero centre--leaf pairing are
available there.  `square`

The last sentence is load-bearing: silently replacing the triangle centre
by `R+Km` would discard a genuine incidence fibre.

## 4. Universal exclusion of the internal pair layer

Let `P_U subset E_U` be the image of the six internal port-pair labels alone:

```text
P_U=sum_(I in binom(U,2)) E_I tensor Pi_I.             (22a)
```

Here every label tensor in `E_I` ranges freely and the typed companion
`Pi_I` occupies `bar I`.  The other nine order-two labels meeting `Q` are not
part of `P_U`.

### Theorem 3 (rank-21/rank-19 pair-layer obstruction)

Under the rank-three maximal-profile hypotheses of Theorem 2, the following
hold after port relabelling.

For a star centred at `0`, there are nonzero covectors `c_i in E_i` on the
three leaves such that

```text
P_U=E_0 tensor (
       E_1 tensor Kc_2 tensor Kc_3
      +Kc_1 tensor E_2 tensor Kc_3
      +Kc_1 tensor Kc_2 tensor E_3),
dim P_U=21.                                             (22b)
```

For a triangle on `{0,1,2}` with isolated port `3`, there are nonzero
covectors `c_i in E_i`, `i=0,1,2`, and `d_3 in E_3` such that

```text
P_U=(
       E_0 tensor E_1 tensor Kc_2
      +E_0 tensor Kc_1 tensor E_2
      +Kc_0 tensor E_1 tensor E_2) tensor Kd_3,
dim P_U=19.                                             (22c)
```

Both formulas include every allowed triangle-centre projection in Theorem 2.
In either profile,

```text
Delta_U(z_Q) notin P_U.                                (22d)
```

#### Proof

In the star geometry (20), write the quotient component of `A_i` at a leaf
as the nonzero local covector `c_i` times the common leaf line.  The only
nonzero companions are complements of leaf--leaf blocks, hence are the three
rank-one tensors `c_j tensor c_k`.  Their freely varying label tensors occupy
the centre and the remaining leaf.  This is exactly (22b).  The parenthesized
space is the affine tangent space to the three-factor Segre cone at
`c_1 tensor c_2 tensor c_3`; inclusion--exclusion gives dimension
`3+3+3-1-1-1+1=7`, and hence `dim P_U=3*7=21`.

Let `q_i:E_i->E_i/Kc_i`.  Applying `q_1 tensor q_2` kills every tensor in the
parenthesized space of (22b).  If the weighted diagonal (28) belonged to
`P_U`, contraction in the centre and fourth leaf would give, for every target
colour `a`,

```text
q_1(e_(a,1)^*) tensor q_2(e_(a,2)^*)=0.               (22e)
```

Thus each of three independent coordinate covectors would have to lie in one
of the two lines `Kc_1,Kc_2`, impossible.

For the triangle, the common sibling hyperplane is one of the two maximal
isotropic hyperplanes in the factorization (23), say `ker ell`.  Put

```text
c_i=m after A_i,             i=0,1,2,
d_3=ell after A_3.                                    (22f)
```

The nonzero centre--sibling block is `c_i tensor d_3`, regardless of whether
`U_3` contains all of `R` or projects onto the whole quotient.  The three
surviving triangle labels therefore give (22c).  Inclusion--exclusion gives
`9+9+9-3-3-3+1=19`.  Every tensor in (22c) has its port-`3` factor on the one
line `Kd_3`, whereas the port-`3` flattening of the weighted concise diagonal
has rank three.  This proves (22d).  `square`

Theorem 3 is a universal mixed-GHZ obstruction for the internal pair layer,
not for the complete contracted base equation.  A complete successor must
annihilate, synchronize, or absorb the eight residual--port labels and the
label `Q` without erasing the target conclusion.

## 5. Sparse radical lines

### Lemma 4 (disjoint-support factorization)

Let `J` be a nonzero rank-two symmetric form on `K^4` with zero diagonal in
the standard basis.  There are independent linear forms `ell,m in X^*` and
`kappa!=0` such that

```text
J=kappa(ell tensor m+m tensor ell),
supp(ell) intersect supp(m)=empty.                    (23)
```

Consequently

```text
R=ker ell intersect ker m                             (24)
```

contains a nonzero vector `r` with root-coordinate support at most two.

#### Proof

The nondegenerate two-dimensional quotient form on `X/R` is isotropic over
`K`: some standard coordinate vector is not in `R`, and every standard
coordinate vector is isotropic by (17).  Hence the quotient is a hyperbolic
plane, which gives (23) before the support statement.  Its diagonal entries
are `2 kappa ell_i m_i`; characteristic zero gives `ell_i m_i=0` for every
`i`, proving disjoint support.

If a coordinate belongs to neither support, its coordinate vector lies in
`R`.  Otherwise the two nonempty disjoint supports cover all four
coordinates, so one has size at least two.  A nonzero vector supported on two
coordinates of that support can be chosen in the kernel of its one linear
form; it is automatically killed by the other.  In either case (24) contains
a nonzero support-at-most-two vector.  `square`

## 6. One bounded full-target detector

Suppose `r` is a nonzero vector satisfying

```text
r in R intersect intersection_(u in U) U_u,
|supp(r)|<=2.                                         (25)
```

Because each `A_u:V_u->U_u` is an isomorphism, there is a unique

```text
a_u(r) in V_u,                  A_u a_u(r)=r.         (26)
```

Put

```text
chi_r=tensor_(u in U) a_u(r).                         (27)
```

After contracting the two residual target slots, the four-port GHZ tensor is

```text
Delta_U(z_Q)=sum_(c=0)^2 omega_c
                tensor_(u in U)e_(c,u)^*,
omega_c=z_(q0,c)z_(q1,c)!=0.                         (28)
```

Define its detector value

```text
D_r=chi_r(Delta_U(z_Q))
   =sum_(c=0)^2 omega_c product_(u in U) a_u(r)_c.    (29)
```

### Theorem 5 (sparse-radical mixed-GHZ detector)

On a complete maximum-root order-two coefficient identity, (25) forces

```text
D_r=0.                                                (30)
```

Therefore `D_r!=0` excludes the profile.

#### Proof

The maximum-root base identity has one summand for each of the fifteen
two-element labels in `Q union U`.

For a port--port label `{u,v}`, evaluation by `chi_r` evaluates its companion
on the other two ports and gives

```text
J(r,r)=0.                                             (31)
```

For a label `{q0,u}`, the residual contraction and `chi_r` evaluate its
companion to

```text
P_4(eta,r,r,r)=0,                                     (32)
```

and `{q1,u}` similarly gives `P_4(xi,r,r,r)=0`.  The three identical `r`
columns in (32) are supported on at most two root coordinates and therefore
cannot occupy three distinct permanent rows.  Finally the label `Q` gives

```text
P_4(r,r,r,r)=0.                                       (33)
```

Thus `chi_r` annihilates every one of the fifteen labelled deck summands.
Applying it to the target side gives exactly (29), proving (30).  `square`

### Corollary 5.1 (maximal-star nonzero-scalar exclusion)

For a maximal star with four rank-three ports, Theorem 2 puts `R` in every
port image and Lemma 4 supplies `r` satisfying (25).  Hence every such
hypothetical witness lies on

```text
D_r=0                                                 (34)
```

for every support-at-most-two radical line.  Any one nonzero value excludes
the star.  This is a pointwise principal-open detector, not a proof that (34)
is empty or a componentwise genericity statement.

### Corollary 5.2 (triangle incidence gate)

For a maximal triangle with four rank-three ports, the three sibling images
already contain `R`.  The same detector applies if the centre intersection
`U_0 intersect R` contains a support-at-most-two line.  Theorem 2 does not
force that condition.

## 7. Sharp boundaries and outcome of the parent attempt

Neither extra gate in Theorem 5 may be silently removed.

### Scalar-zero star control

Take `R=span(epsilon_2,epsilon_3)` and a hyperbolic quotient with orthogonal
nonisotropic lines `p,r`.  Put

```text
U_0=R+Kp,                     U_1=U_2=U_3=R+Kr.       (35)
```

Choose the inverse images of `R` in the four ternary local spaces to be the
coordinate planes with supports

```text
{0,1}, {0,1}, {1,2}, {0,2}.                          (36)
```

For every `r0 in R`, each target colour is absent from at least one of the
four inverse images, so

```text
D_(r0)=0                                              (37)
```

identically.  All four port maps still have rank three and (35) has the
required star zero/nonzero `J` pattern.  This is an incidence control, not a
full graph witness, but it proves that port rank and the star pattern do not
force detector activity.

### Nonsparse triangle-centre control

Let

```text
ell=x_0+x_1,              m=x_2+x_3,
R={x_0+x_1=x_2+x_3=0},
B=ker ell.                                               (38)
```

Use `B` for the three sibling images and take the centre hyperplane

```text
U_0={x_0-x_2=0}.                                      (39)
```

Then `J=B`-isotropic, the centre--sibling block is nonzero, and

```text
U_0 intersect R=K(1,-1,1,-1),                        (40)
```

whose nonzero vectors all have support four.  Thus the common sparse line in
(25) is not forced on the triangle profile.

Combining Theorems 1--5 gives the exact answer to the attempted universal
bridge:

```text
GLD68 + an aggregate GHZ identity, without common incidence:  INSUFFICIENT;
physical common J, maximal profile, all port ranks three:      COMPRESSED;
internal six-label port-pair layer on that physical locus:     EXCLUDED;
star + one nonzero sparse-radical target value:                EXCLUDED;
triangle + sparse centre-radical line + nonzero target value:  EXCLUDED;
scalar-zero / nonsparse-centre / lower-rank residual fibres:   OPEN.        (41)
```

The smallest honest successors are therefore not third sibling theorems.
They are parent obligations:

1. construct a coefficient-pure quotient or synchronization invariant which
   removes the nine `Q`-meeting labels and lands in Theorem 3's pair layer;
2. prove target activity `D_r!=0` for at least one sparse radical line, or
   classify the simultaneous divisor (34), on the physical star locus;
3. on the triangle locus, first force a sparse centre--radical intersection
   or build a different bounded separator that also covers (40);
4. separately route the port-rank-deficient profiles using the existing
   maximum-root deficiency budget;
5. keep non-leading/promoted row supply as a distinct alternative.

No statement here supplies a full operator-space intersection, a nonzero
response, arbitrary-root coverage, or a permanent restriction outside the
declared rank-three maximal-profile scope.

## Verification

Run

```text
python claims/arbitrary-order/verify_four_root_maximal_base_survivor_common_incidence_and_sparse_radical_detector_boundary.py
python -I claims/arbitrary-order/audit_four_root_maximal_base_survivor_common_incidence_and_sparse_radical_detector_boundary.py
python -m py_compile claims/arbitrary-order/verify_four_root_maximal_base_survivor_common_incidence_and_sparse_radical_detector_boundary.py claims/arbitrary-order/audit_four_root_maximal_base_survivor_common_incidence_and_sparse_radical_detector_boundary.py
uv run --with ruff ruff check claims/arbitrary-order/verify_four_root_maximal_base_survivor_common_incidence_and_sparse_radical_detector_boundary.py claims/arbitrary-order/audit_four_root_maximal_base_survivor_common_incidence_and_sparse_radical_detector_boundary.py
uv run --with ruff ruff format --check claims/arbitrary-order/verify_four_root_maximal_base_survivor_common_incidence_and_sparse_radical_detector_boundary.py claims/arbitrary-order/audit_four_root_maximal_base_survivor_common_incidence_and_sparse_radical_detector_boundary.py
```

The primary verifier replays all eight formal coefficient countermodels, the
common `J` pullback, both rank-21/rank-19 physical pair layers, canonical
star/triangle incidence controls, the fifteen-label sparse-radical
annihilation, and both sharp boundaries.  The
independent no-import audit exhausts every symmetric zero-diagonal `4 x 4`
matrix over `F_5`, checks the rank-two sparse-radical lemma, reconstructs the
eight survivor families by a different traversal, and independently replays
the detector identities.  The finite-field census is an audit of formulas
and case coverage; the written linear-algebra proof is the characteristic-zero
theorem.
