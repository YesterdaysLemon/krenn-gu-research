# Maximum-root surplus-two zero-anchor three-effective-label shared-polarization rank-seven normal form and other-rank exclusion

## Status and scope

The global Krenn--Gu conjecture is **UNRESOLVED**.

This document proves `GLS51`, an exact characteristic-zero, arbitrary-root,
pointwise classification of the exactly-three-effective-label part of the
zero-anchor fully swallowed fixed-residual target locus.

There are three possible support types.

1. Two residual labels and one promoted port are impossible by `GLS49`.
2. Three promoted ports are impossible: the mandatory coordinate deck frame,
   restricted to its three deck hyperplanes, would give a `GLS39` family whose
   pair image is both contained in and spans the three-colour diagonal.
3. One residual label and two promoted ports force a common coordinate deck
   line, pure residual shores on that line, a separated crossed-square normal
   form on the other two colours, injectivity of both port joint maps, and

   ```text
   rank B_Q^anc=7.
   ```

Consequently an exactly-three-effective-label point can occur only in the
last support type and only at nuisance rank seven.  In particular, combined
with `GLS48`, every rank-five, rank-six, rank-eight, or rank-nine zero-anchor
fully swallowed target point has at least four effective labels.  Rank seven
with the displayed normal form remains open: the theorem neither constructs
nor excludes a point coming from the principal complementary decks of one
physical graph.

Every assertion retains all inactive-port, deck-zero, cancellation,
incidence-rank, divisor, residual-shore, response, and root-order fibres.  No
response, deck, selector, parameter minor, or incidence determinant is
silently divided out.

This is not source-to-swallow coverage, raw-escape attachment, a named
physical response or selector, a legal downstream receiver package, or
strategic-node closure.  It does not treat four-or-more effective labels,
the nonzero-anchor branches, permanent restriction, extraction, or gluing.

## Dependencies and provenance

- `GLS21` owns the complete raw pair-labelled promoted decomposition.
- `GLS36` gives `B_Q^anc=im sigma_Q` and the fixed-residual target equation.
- `GLS39` identifies the auxiliary pair polarizations and proves the complete
  pairwise-diagonal family rank bound.
- `GLS48` proves the unconditional three-effective-label floor.
- `GLS49` excludes the residual-pair-plus-one-port support.
- `GLS50` records the inactive-port contraction and the two remaining support
  equations.  Its coordinate-cover and nonzero-deck arguments are repeated
  below without its rank-five hypothesis.

The new content is the denominator-free shifted determinant classification,
the complete crossed-square normal form and exact rank-seven conclusion, and
the deck-hyperplane reduction of the three-port support to `GLS39`.  A
focused exact verifier uses rational symbolic matrices.  A genuinely
independent no-import audit uses custom sparse-polynomial arithmetic,
rational row reduction, and a separate finite-field projective
classification.

## 1. Common notation and inactive-port contraction

Retain the `GLS39` auxiliary label family

```text
T=Q disjoint-union Uhat,             Q={q_0,q_1},
Act={t in T:X_t!=0 or Y_t!=0},
E=V_(a_0)^* tensor V_(a_1)^*,        Delta=span{r_0,r_1,r_2}.
                                                               (1)
```

Fix one `GLS8` chart, one fully supported residual contraction, and a
zero-anchor point with `|Act|=3`.  Thus the target coefficients
`alpha_0,alpha_1,alpha_2` are nonzero and `Delta subset B_Q^anc`.

Evaluate every inactive promoted port at `1=e_0+e_1+e_2`.  Every pure target
word remains one.  A raw pair term with an inactive endpoint has zero root
coefficient by the definition of `Act`; every surviving physical deck
becomes a form on the remaining active ports or a scalar.  This contraction
is exact for every root order `r>=3` and loses no source term relevant to the
displayed support.

For root-shore vectors write a joint vector as

```text
z=(x,y) in K^3 direct-sum K^3
```

and define

```text
mu(z,z')=x tensor y'+x' tensor y.                    (2)
```

### Lemma 1 (exact zero types)

If `z,z'` are nonzero and `mu(z,z')=0`, then exactly one of the following
broad types occurs:

```text
both X-only:       y=y'=0;
both Y-only:       x=x'=0;
both two-sided:    z' is proportional to (x,-y).
                                                               (3)
```

Thus the endpoints of a zero edge have the same broad type.  On a connected
zero graph, every nonzero vertex has one broad type.  A two-sided zero
triangle is impossible in characteristic different from two.

#### Proof

If both simple tensors in (2) are nonzero, their equality up to sign forces
proportional first and second factors, giving the last case.  If either
simple tensor is zero, nonvanishing of both joint vectors leaves exactly the
two one-sided cases.  Along two consecutive two-sided zero edges the sign on
the second root factor flips twice.  The third edge of a triangle is then a
nonzero scalar multiple of `2x tensor y`, not zero. `square`

## 2. One residual label and two promoted ports

Assume

```text
Act={q_s,u,v}.                                       (4)
```

The other residual label is ineffective, so its two shore vectors vanish
and `q=0`.  Let `a,b` be the shore vectors of `q_s` and put

```text
G_u(z)=a tensor Y_u(z)+X_u(z) tensor b,
G_v(w)=a tensor Y_v(w)+X_v(w) tensor b,
M_uv(z,w)=X_u(z) tensor Y_v(w)+X_v(w) tensor Y_u(z).
```

After the inactive-port contraction, the complete target equation is

```text
G_u(z)lambda_v(w)+G_v(w)lambda_u(z)+gamma M_uv(z,w)
 =sum_(d=0)^2 alpha_d z_d w_d r_d.                  (5)
```

Here `lambda_u,lambda_v` are evaluated complementary physical deck
covectors and `gamma` is the evaluated port-pair deck scalar.  They are not
named responses.

### Lemma 2 (the port-pair deck scalar is nonzero)

One has `gamma!=0`.

#### Proof

If `gamma=0`, restrict (5) to
`ker lambda_u times ker lambda_v`.  For each colour `d`, the simple
bilinear form

```text
(e_d^* restricted to ker lambda_u)
 tensor (e_d^* restricted to ker lambda_v)
```

would vanish.  One covector kernel can be contained in at most one of the
three coordinate hyperplanes, and a zero covector accounts for none.  The
two deck covectors can therefore account for at most two colours, a
contradiction. `square`

### Lemma 3 (denominator-free shifted polarization)

Define

```text
Xtilde_t=gamma X_t+a lambda_t,
Ytilde_t=gamma Y_t+b lambda_t.                       (6)
```

Then

```text
Xtilde_u(z) tensor Ytilde_v(w)
 +Xtilde_v(w) tensor Ytilde_u(z)
 =gamma sum_d alpha_d z_d w_d r_d
  +2(a tensor b)lambda_u(z)lambda_v(w).             (7)
```

#### Proof

Expand the left side.  The `gamma^2 M_uv` term and the four cross terms are
`gamma` times the left side of (5); the two remaining terms are the two
identical copies of `(a tensor b)lambda_u lambda_v`. `square`

Every matrix value on the left of (7) is a sum of two rank-one matrices, so
its determinant vanishes.  The matrix determinant lemma, used as a
polynomial identity and without inverting a coordinate, gives

```text
0=gamma^3 alpha_0 alpha_1 alpha_2
    z_0z_1z_2 w_0w_1w_2
  +2gamma^2 lambda_u(z)lambda_v(w)
    sum_d a_d b_d alpha_i alpha_j z_i z_j w_i w_j,  (8)
```

where `{d,i,j}={0,1,2}` in each summand.

### Lemma 4 (common coordinate deck and residual lock)

There is a unique colour `c` and nonzero scalars `s,t` such that

```text
lambda_u=s e_c^*,             lambda_v=t e_c^*,
a_c b_c!=0,                   a_d b_d=0 for d!=c,
gamma alpha_c+2st a_c b_c=0.                          (9)
```

#### Proof

If either deck covector were zero, the leading monomial in (8) would remain
uncancelled.  If every `a_d b_d` were zero, the same contradiction would
hold.  Choose `c` with `a_c b_c!=0` and set `z_c=0` in (8).  Only the
`c`-summand survives, so nonzero `lambda_v` forces `lambda_u` to vanish on
`z_c=0`; hence `lambda_u` is proportional to `e_c^*`.  Setting `w_c=0`
gives the same conclusion for `lambda_v`.  No second product `a_d b_d` can
be nonzero, because the same argument would put the nonzero covectors on a
second coordinate line.  Substitution in (8) gives the scalar lock. `square`

### Theorem 5 (complete rank-seven separated normal form)

Let `{i,j}={0,1,2}-{c}` and define shifted coordinate joint vectors

```text
Utilde_d=(Xtilde_u(e_d),Ytilde_u(e_d)),
Vtilde_d=(Xtilde_v(e_d),Ytilde_v(e_d)).              (10)
```

Then the following all hold.

1. `Utilde_c=Vtilde_c=0`.
2. The residual shores are pure on the common deck coordinate:

   ```text
   a tensor b=a_c b_c r_c,
   Ka=Kb=Ke_c.                                      (11)
   ```

3. Up to exchanging the two root shores and the two off-deck colours, the
   unique crossed-square broad-type pattern is

   ```text
   Utilde_i,Vtilde_j are X-only,
   Utilde_j,Vtilde_i are Y-only.                    (12)
   ```

   The two matched polarizations are nonzero multiples of `r_i,r_j`.
4. Both original port joint maps `z |-> (X_t(z),Y_t(z))` are injective.
5. The complete root-incidence image is exactly

   ```text
   B_Q^anc
    =Delta + K E_ci+K E_ic+K E_cj+K E_jc,
   rank B_Q^anc=7.                                  (13)
   ```

#### Proof

Equation (7) gives zero polarization for every unmatched pair
`Utilde_d,Vtilde_e` with `d!=e`, while the two off-deck matched values are
the nonzero independent matrices `gamma alpha_i r_i` and
`gamma alpha_j r_j`.  Hence the four off-deck joint vectors are nonzero.

If either deck-coordinate joint vector were nonzero, the graph of nonzero
vertices with all unmatched zero edges would be connected: the mandatory
four vertices form two crossed edges, and either deck-coordinate vertex
joins them.  Lemma 1 forces one broad type.  A one-sided type kills both
mandatory matching outputs.  In the two-sided type, a length-three zero path
from `Utilde_i` to `Vtilde_i` sign-propagates to make their matching
polarization zero.  Both alternatives are impossible.  Thus
`Utilde_c=Vtilde_c=0`.

The matched `c` value in (7) now gives the matrix identity

```text
gamma alpha_c r_c+2st(a tensor b)=0.
```

Together with the scalar lock (9), this proves (11).

For the four off-deck vertices, the two unmatched zero edges pair
`Utilde_i` with `Vtilde_j` and `Utilde_j` with `Vtilde_i`.  If both pairs
were two-sided, direct substitution into (2) would make the two matched
outputs proportional with opposite signs.  If one pair were two-sided and
the other one-sided, purity of the two matched diagonal outputs would force
one nonzero root factor onto both distinct coordinate lines `Ke_i` and
`Ke_j`.  Equal one-sided types kill both outputs.  The only remaining cases
are the two separated orientations (12), proving the crossed-square claim.

The shifts vanish off coordinate `c`.  At coordinate `c`, (6), the
vanishing shifted vectors, and `s,t!=0` give nonzero original joint vectors
supported on `Ke_c direct-sum Ke_c`.  At the other two coordinates, (12)
gives one nonzero X-only and one nonzero Y-only vector on distinct coordinate
lines for each port.  These three coordinate joint vectors are independent,
so both port joint maps are injective.

The four residual--port values at the off-deck coordinates supply, modulo
`Delta`, the four distinct star matrix-unit lines in (13).  Full swallow
supplies `Delta`, so the incidence rank is at least seven.  Conversely,
`G_u,G_v` take values in the diagonal-plus-star space because `a,b` are pure
on `Ke_c`.  Solving (5) for the nonzero scalar `gamma` puts every value of
`M_uv` in the same space.  Since `q=0` and these are all effective raw pair
images, `GLS36` gives the reverse containment in (13). `square`

### Exact shared-interface sharpness control

The rank-seven conclusion cannot be improved using only equation (5) and
shared `X/Y` polarization.  Over the rationals take `c=0`,

```text
gamma=1,                 lambda_u=lambda_v=e_0^*,
alpha_0=alpha_1=alpha_2=1,
a=e_0,                   b=-(1/2)e_0,

X_u=[-e_0, 0,   e_2],    Y_u=[(1/2)e_0, e_1, 0],
X_v=[-e_0, e_1, 0],      Y_v=[(1/2)e_0, 0,   e_2].  (14)
```

Direct expansion gives (5) coefficientwise, both port joint maps have rank
three, and the complete pair-image span is

```text
Delta+K E_01+K E_10+K E_02+K E_20,
```

of rank seven.  This is an exact contracted shared-interface control.  It is
not a realization of the complementary decks as principal minors of one
physical graph, not a full uncontracted target point, and not a Krenn--Gu
witness or counterexample.

## 3. Three promoted ports

Assume

```text
Act={u,v,w}.                                        (15)
```

Both residual labels are ineffective, so `q=0`.  After inactive-port
contraction the exact target equation is

```text
M_uv(z_u,z_v)lambda_w(z_w)
+M_uw(z_u,z_w)lambda_v(z_v)
+M_vw(z_v,z_w)lambda_u(z_u)
 =sum_(d=0)^2 alpha_d z_(u,d)z_(v,d)z_(w,d)r_d.    (16)
```

### Lemma 6 (complete coordinate deck-line cover)

All three deck covectors are nonzero and, after relabelling ports,

```text
lambda_u=rho_u e_0^*,
lambda_v=rho_v e_1^*,
lambda_w=rho_w e_2^*,             rho_u rho_v rho_w!=0.       (17)
```

#### Proof

For each colour `d`, select the `r_d` coefficient in (16) and quotient the
three covector factors by `Klambda_u,Klambda_v,Klambda_w`.  Every source term
vanishes, so the pure tensor

```text
(e_d^* mod Klambda_u) tensor
(e_d^* mod Klambda_v) tensor
(e_d^* mod Klambda_w)
```

is zero.  At least one deck line must therefore equal `Ke_d^*`.  One
nonzero line covers at most one colour and a zero covector covers none.
Three slots covering three colours must be the coordinate-line permutation,
which proves (17). `square`

### Theorem 7 (deck-hyperplane exclusion of the three-port support)

No exact target-consistent point satisfies (15).

#### Proof

Put

```text
H_u=ker lambda_u,       H_v=ker lambda_v,
H_w=ker lambda_w.                                    (18)
```

Restrict (16) to `H_u times H_v` and choose a `w` input on which
`lambda_w` is nonzero.  The other two source terms vanish, so

```text
M_uv(H_u,H_v) subset Delta.
```

Taking the `w` input on coordinate two and varying the coordinate-two
inputs in `H_u,H_v` shows that this restricted image contains `Kr_2`.
Cyclically,

```text
M_uw(H_u,H_w) subset Delta and contains Kr_1,
M_vw(H_v,H_w) subset Delta and contains Kr_0.        (19)
```

Now restrict the three whole-domain joint maps `(X_t,Y_t)` to `H_t`.
Every distinct-label polarization has image in `Delta`, but their combined
image contains all of `Delta` by (19), hence has rank at least three.  The
complete pairwise-diagonal family theorem `GLS39` says that such a combined
image has rank at most two in characteristic different from two.  This is a
contradiction. `square`

This exclusion uses neither a joint-kernel profile nor a nuisance-rank
hypothesis.  In particular it removes all three `GLS50` rank-five profiles
at once and retains every kernel and rank-drop fibre.

## 4. Exhaustive exactly-three-label classification and boundary

### Corollary 8 (only the rank-seven normal form survives)

At any zero-anchor, fully swallowed fixed-residual target point in
characteristic zero with `|Act|=3`, exactly one of the following exhaustive
support counts applies:

```text
two residuals plus one port:     impossible by GLS49;
one residual plus two ports:     Theorem 5, rank exactly seven;
three promoted ports:            impossible by Theorem 7.
                                                               (20)
```

Thus exactly three effective labels imply the complete rank-seven separated
normal form of Theorem 5.  Conversely, no existence claim is made.

Together with the `GLS48` floor `|Act|>=3`, the exact activity consequences
are

```text
zero-anchor ranks five, six, eight, nine:             |Act|>=4;
zero-anchor rank seven with |Act|=3:                  normal form (13);
zero-anchor rank seven with |Act|>=4:                 OPEN;
principal-deck realization/exclusion of (13):         OPEN;
four-or-more effective labels at every rank:          OPEN;
silent source necessarily enters full swallow:       UNKNOWN;
raw escape supplies an original legal target:        NOT SUPPLIED;
nonzero-anchor marginal/double-transverse branches:   OPEN;
selector/response/activity/synchronization gates:     OPEN;
nuisance survival and target-pure anchors:            OPEN;
arbitrary-root strategic-node closure:                UNKNOWN;
global Krenn--Gu conjecture:                          UNRESOLVED.
```

The smallest same-locus continuation is the physical principal-deck
realizability of the rank-seven separated normal form.  A different
support-free argument is still required for four-or-more effective labels.
Neither task may reinterpret the evaluated coordinate deck covectors as
named physical responses or legal selectors.

## Verification boundary

The focused verifier replays the shifted identity, determinant polynomial,
coordinate-deck lock, zero-graph and crossed-square classifications, exact
rank-seven control, and deck-hyperplane reduction over the rationals.  It is
an identity and finite-case replay, not the prose proof.

The independent audit imports no project code or algebra package.  It uses
custom sparse-polynomial determinant expansion, exact rational row
reduction, a projective `F_3` zero-pair census, and a separate graph/type
enumeration.  The written proof carries the characteristic-zero theorem.

Neither checker proves principal-minor realization of (14), source-to-
swallow coverage, a response or selector gate, four-label closure, node
closure, or the global conjecture.
