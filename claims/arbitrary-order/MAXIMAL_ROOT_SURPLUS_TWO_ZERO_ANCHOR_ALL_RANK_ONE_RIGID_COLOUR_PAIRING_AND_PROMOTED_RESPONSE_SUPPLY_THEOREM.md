# Maximum-root surplus-two zero-anchor all-rank-one rigid colour pairing and promoted-response supply

## Status and scope

**Exact characteristic-zero root-order-three source/deck theorem and
old-probe receiver no-go; the all-rigid branch and the strategic node remain
open.**  Fix an actual
hypothetical Krenn--Gu witness in one `GLS4`-eligible promoted `GLS8` chart
with

```text
r=3,       A={a_0,a_1},
Bhat=Q disjoint-union Uhat,       |Q|=2,       |Uhat|=4,
omega=W_(a_0,a_1)=0.                                      (1)
```

For every `t in Bhat`, let `J_t` be its full joint incidence map to the two
probe roots.  Assume all six maps are torus-rigid and have rank one.  Then:

1. the six labels have a canonical partition into three two-element sets
   `P_0,P_1,P_2`, where `row(J_t)=K e_(t,c)^*` exactly when `t in P_c`;
2. for every colour `c`, the complete same-graph equation has only one term
   on the auxiliary all-`c` slice, and gives the denominator-free identity

   ```text
   h_c G^A_(P_c)=d_c,       h_c!=0,                   (2)
   ```

   where `h_c` is the all-`c` coefficient of the complementary physical deck
   `H_(Bhat-P_c)` and `d_c` is the fully pure tensor on the two probe slots
   and the two labels of `P_c`;
3. every auxiliary coordinate word obeys one exact master equation.  On the
   complementary `2 x 2 x 2 x 2` off-readout face of `H_(Bhat-P_c)`, all
   fifteen mixed cells vanish and the sole all-`c` cell is nonzero;
4. at least one `P_c` is contained in `Uhat`.  For every such pair, putting
   `S_c=Uhat-P_c` makes `G^A_(P_c)` the desired coefficient of a named `GLS8`
   promoted pair target, and its residual-present physical response

   ```text
   H_(Q union S_c)(z_Q,-_(S_c))                       (3)
   ```

   is a nonzero polynomial in the residual contraction.  It is nonzero on a
   common dense torus open with the two original `GLS4` gates.
5. after any fixed contraction of the old probes `A`, every physical pair
   response on auxiliary labels `s,t` is supported only at the coordinate
   cell `(kappa(s),kappa(t))`.  Consequently, at any fixed auxiliary port,
   diagonal pair-depth activity can occur in at most one colour.  The direct
   old-probe `GLD3` three-colour activity gate is therefore pointwise
   impossible on this branch.

This is a genuine same-graph source-to-response-polynomial advance.  It does
**not** prove survival of `G^A_(P_c)` modulo the complete labelled nuisance,
a normalized legal selector, simultaneous attachment of all six pair rows,
projective synchronization, selected-response activity for any other
receiver, nuisance survival, a `GLD3` receiver entry, the higher-rank rigid
branch, any `r>=4` branch, or
pointwise nonvanishing on every residual fibre.  The maximum-root surplus-two
strategic node and the global Krenn--Gu conjecture remain **UNRESOLVED**.

## Dependencies and provenance

The proof uses exactly the following committed interfaces.

- `GLS4` supplies one eligible pair/probe chart and nonzero residual gate
  polynomials.
- `GLS8` supplies the complete two-probe matching identity, the promoted
  target labels, and the exact complete-nuisance selector criterion.
- `GLS55` supplies the rank-one torus-rigidity equivalence
  `row(J_t)=K e_(t,c)^*`.
- `GLS56` owns the complementary nonrigid branch and records why a rigid
  coordinate readout is not itself a response or selector.

The new argument is the complete pure-slice coupling of all six rank-one
rigid readouts, its exact `Q`-incidence classification, and the resulting
nonzero promoted-response polynomial, together with the pointwise old-probe
`GLD3` activity no-go.  No logical dependence is inferred from filenames.

## 1. Joint rank-one coordinate readouts

Write the two probe-incidence blocks at `t` as

```text
X_t=sum_(i=0)^2 x_(t,i) tensor e_(t,i)^*,
Y_t=sum_(i=0)^2 y_(t,i) tensor e_(t,i)^*,             (4)
```

and put

```text
J_t(v)=(X_t(v),Y_t(v)).                               (5)
```

By `GLS55`, a rank-one map `J_t` is torus-rigid exactly when its kernel is a
coordinate plane.  Hence there is a unique colour `kappa(t)` such that

```text
row(J_t)=K e_(t,kappa(t))^*,
X_t=x_t tensor e_(t,kappa(t))^*,
Y_t=y_t tensor e_(t,kappa(t))^*,
(x_t,y_t)!=(0,0).                                     (6)
```

Define

```text
P_c={t in Bhat:kappa(t)=c}.                           (7)
```

The sets `P_0,P_1,P_2` are disjoint and partition `Bhat`.

For `D={s,t}`, the two-probe pair companion is

```text
G_D^A=(x_s tensor y_t+x_t tensor y_s)
      tensor e_(s,kappa(s))^* tensor e_(t,kappa(t))^*, (8)
```

with the canonical slot order understood.  In particular, its all-`c`
auxiliary coefficient is zero unless `D subset P_c`.

## 2. Complete pure-slice pairing

The zero-anchor `GLS8` identity is

```text
T_W(-_A,-_Bhat)
 =sum_(D in binom(Bhat,2)) G_D^A tensor H_(Bhat-D).    (9)
```

For a colour `c` and a pair `D`, put

```text
h_(D,c)=H_(Bhat-D)(tensor_(u in Bhat-D)e_(u,c)).      (10)
```

### Theorem 1 (rank-one rigid colour-pair partition)

Each `P_c` has exactly two elements.

### Proof

Evaluate every auxiliary slot of (9) at colour `c`, leaving the two probe
slots open.  The target side is the nonzero tensor

```text
E_(A,c)=e_(a_0,c)^* tensor e_(a_1,c)^*.               (11)
```

By (8), only pairs `D subset P_c` can contribute.  If `|P_c|<2`, the entire
left side would be zero, contradicting (11).  Thus `|P_c|>=2` for all three
colours.  The three sets partition the six-element set `Bhat`, so all three
have size exactly two.  `square`

Write

```text
P_c={s_c,t_c},
M_c=x_(s_c) tensor y_(t_c)+x_(t_c) tensor y_(s_c),
h_c=h_(P_c,c).                                        (12)
```

### Theorem 2 (full pure-companion/deck factorization)

For every colour `c`,

```text
h_c M_c=E_(A,c),       h_c!=0,
G^A_(P_c)=h_c^(-1) E_(A,c)
 tensor e_(s_c,c)^* tensor e_(t_c,c)^*.               (13)
```

Equivalently, without displaying an inverse,

```text
h_c G^A_(P_c)
 =E_(A,c) tensor e_(s_c,c)^* tensor e_(t_c,c)^*.      (14)
```

### Proof

Theorem 1 leaves exactly one pair `D=P_c` in the all-`c` auxiliary slice of
(9).  Equations (8)--(12) therefore give

```text
h_c M_c=E_(A,c).                                      (15)
```

The right side is nonzero, so both factors on the left are nonzero.  Equation
(8) says the full companion has no auxiliary support outside the single
`(c,c)` cell.  Multiplying that full tensor by `h_c` gives (14).  The inverse
form in (13) is now a consequence over the field; no denominator was used to
obtain the identity or to remove an exceptional fibre.  `square`

This is stronger than a nonzero diagonal coefficient.  The entire desired
coefficient tensor, including both old probe slots, is one pure target row.
It remains a labelled coefficient, not yet a quotient-surviving selector.

### Theorem 2.1 (mixed-word master identity and pure off-readout face)

For a coordinate word

```text
sigma:Bhat -> {0,1,2},
A(sigma)={t in Bhat:sigma(t)=kappa(t)},               (15a)
```

and a pair `D={s,t}`, define

```text
h_D(sigma)=H_(Bhat-D)
 (tensor_(u in Bhat-D)e_(u,sigma(u))).                (15b)
```

Then the complete coefficient comparison is

```text
sum_(D in binom(A(sigma),2)) M_D h_D(sigma)
 = { E_(A,c),  if sigma is the constant word c;
   { 0,        otherwise.                             (15c)
```

Fix any pair `D` and impose

```text
sigma(t)=kappa(t)             for t in D,
sigma(u)!=kappa(u)            for u in Bhat-D.        (15d)
```

Then `A(sigma)=D`, so (15c) has one summand.  If `D=P_c`, its sixteen
off-readout complement words consist of the constant all-`c` word and
fifteen mixed words.  Therefore the restriction of `H_(Bhat-P_c)` to that
`2 x 2 x 2 x 2` face is supported at exactly one cell:

```text
h_(P_c)(sigma)=0 on all fifteen mixed cells,
h_(P_c)(c,c,c,c)=h_c!=0.                              (15e)
```

If the two members of `D` have different readout colours, all sixteen words
are mixed; whenever `M_D!=0`, all sixteen corresponding complementary-deck
coefficients vanish.

### Proof

Evaluate (9) at the auxiliary coordinate word `sigma`, leaving the two probe
slots open.  Equation (8) kills exactly the pair terms not contained in
`A(sigma)`, giving the left side of (15c).  The GHZ target is zero on every
mixed auxiliary word and equals `E_(A,c)` on the constant word `c`, proving
(15c).

Under (15d), the active set is exactly `D`.  Thus (15c) is the single equation
`M_D h_D(sigma)=0` unless the word is constant.  For `D=P_c`, the constant
word `c` is the unique constant member of the off-readout face, and Theorem 2
gives its nonzero value.  On every other word `M_(P_c)!=0`, so the scalar deck
coefficient vanishes.  If the readout colours on `D` differ, the word is
already mixed; the final assertion follows whenever `M_D!=0`.  `square`

The face theorem is not a claim that the whole complementary deck is pure.
Coordinates where another label uses its own readout colour can receive
several pair terms in (15c), and exact mixed cancellations remain possible.

## 3. Residual incidence and promoted response supply

The two residual labels `Q={q_0,q_1}` occur in the disjoint three-pair
partition in exactly one of two ways.

### Corollary 3 (exhaustive `Q`-incidence classification)

1. **Same-colour residual pair.**  If `Q=P_d` for one colour `d`, then the
   other two pairs lie in `Uhat`.  The `D=Q` term has the residual-absent deck
   `H_Uhat`; it is the raw-anchor label, not a promoted pair target.  The
   other two pairs each give a named promoted pair target.
2. **Split-colour residual pair.**  If `q_0` and `q_1` lie in different
   colour pairs, exactly one `P_c` is contained in `Uhat`.  The two mixed
   `Q`--`Uhat` pair labels have one-residual three-port complementary decks
   and are nuisance labels for the promoted pair module.  The remaining pair
   gives one named promoted pair target.

Thus at least one and at most two colour pairs lie in `Uhat`, with two
exactly when `Q` itself is one colour pair.

### Proof

Each residual label lies in one unique member of the partition.  If they lie
in the same member, that two-element member is `Q` and both other members are
disjoint from `Q`.  If they lie in different members, exactly the third
member is disjoint from `Q`.  A pair disjoint from `Q` is contained in
`Uhat`; the deck labels follow by taking its complement in
`Bhat=Q disjoint-union Uhat`.  `square`

Fix a colour `c` with `P_c subset Uhat` and put

```text
C=P_c,       S_c=Uhat-C.                              (16)
```

Then `|S_c|=2`, and the exact `GLS8` target typing is

```text
g_(S_c)=G_C^A,
P_(S_c)(H;z_Q)=H_(Q union S_c)(z_Q,-_(S_c))
              =H_(Bhat-C)(z_Q,-_(S_c)).              (17)
```

### Theorem 4 (nonzero promoted-response polynomial)

The pure-`c` output coordinate of `P_(S_c)(H;z_Q)` is a nonzero bilinear
polynomial in `z_(q_0),z_(q_1)`.  Its coefficient of
`z_(q_0,c)z_(q_1,c)` is the nonzero scalar `h_c`.

Consequently, over the infinite characteristic-zero source field, there is
a dense torus open on which this response, `H_Q(z_Q)`, and
`p_(A,Q)(z_Q)` are all nonzero.

### Proof

The response in (17), evaluated at the pure-`c` output word on `S_c`, is

```text
sum_(i,j=0)^2 z_(q_0,i)z_(q_1,j)
 H_(Bhat-C)(e_(q_0,i),e_(q_1,j),
            tensor_(u in S_c)e_(u,c)).                (18)
```

The coefficient at `(i,j)=(c,c)` is exactly (10) with `D=C`, namely
`h_c!=0`.  Distinct residual monomials are linearly independent, so (18) is
not the zero polynomial.

The two `GLS4` gate polynomials are nonzero by eligibility.  Their product
with (18) is therefore nonzero in the residual polynomial ring.  The
complement of its zero set meets the residual torus over the actual complex
source field (and over any infinite characteristic-zero field after the
usual base-field qualification).  This gives one common fully supported
residual point with all three stated nonvanishings.  `square`

The theorem does not claim that (18) is nonzero at a previously chosen
residual point.  Its zero divisor and every rank-drop fibre remain part of
the exact one-row `GLS8` failure analysis.

## 4. Exact receiver boundary

For every pair `C=P_c subset Uhat`, Theorem 2 supplies

```text
g_(S_c)=h_c^(-1)d_(S_c,c),                            (19)
```

in the notation of `GLS8`.  There are two correct conditional interfaces.
Write `h(z_Q)=H_Q(z_Q)` and `p(z_Q)=p_(A,Q)(z_Q)` for the original `GLS4`
gate polynomials.  At a specified fully supported residual point `z_Q`,
assume simultaneously

```text
h(z_Q)p(z_Q)!=0,       P_(S_c)(H;z_Q)!=0,
[g_(S_c)]!=0 in L_(S_c)^*/N_(S_c)(z_Q).              (20)

```

Then `GLS8` gives one normalized constant selector annihilating every
labelled nuisance and having nonzero physical response at that same point.
Alternatively, if the desired column survives the complete nuisance over the
residual function field, its dense survival open intersects the dense
`h p P_(S_c)` open from Theorem 4, again giving one common useful point.

Neither form of the survival hypothesis is proved here.  Pointwise survival
at one unspecified point cannot be combined with response nonvanishing at a
different point.  More importantly, even one useful row is
not a named downstream detector package.

### Theorem 5 (old-probe `GLD3` activity no-go)

Use the old probes `A` as the physical residual pair of `GLD3`.  Fix arbitrary
contraction vectors on them, and let `D_(st)` be the resulting physical
residual-present pair response on any two auxiliary labels `s,t`.  Then

```text
supp D_(st) subset {(kappa(s),kappa(t))}.              (21)
```

For every four-label window `U subset Bhat`, every port `u in U`, and every
colour `c`, a diagonal response coefficient can be nonzero only if

```text
D_(uv)(c,c)!=0  ==>  c=kappa(u)=kappa(v).             (22)
```

Thus the set of colours having any diagonal pair response incident with `u`
has size at most one.  In particular, the three-colour pair-depth activity
condition (10) of `GLD3` is impossible for every old-probe four-label window,
including all response-zero and contraction-divisor fibres.

### Proof

Because the old-probe edge is the zero tensor in (1), the `h B_(st)` direct
term in the `GLD3` response formula is zero.  Before contracting `A`, the
remaining response is exactly `G^A_(st)`, and equation (8) says that it has
only one possible auxiliary coordinate cell, namely
`(kappa(s),kappa(t))`.  Evaluation in the probe slots changes only its scalar
coefficient and cannot create a new auxiliary cell.  This proves (21), hence
(22).

In the notation of `GLD3`, three-colour activity at `u` requires, for each
colour `c`, a nonzero product whose first factor is a diagonal coefficient
`d_(u v_c,c)=D_(u v_c)(c,c)`.  Equation (22) permits such a factor only for
the single colour `c=kappa(u)`.  At least two of the three required products
therefore vanish.  The argument uses no division and covers every choice of
probe contraction and every four-label window.  `square`

This rules out the formerly suggested direct old-probe `GLD3` successor; it
does not create a different receiver.  The local readout rows realizing (6)
may also vary with `t`, so they cannot be silently synchronized into one
probe contraction.

The zero tensor `omega=W_(a_0,a_1)` is also not the promoted residual scalar
`H_Q(z_Q)`.  Hence (1) is not an `h=0` entry to the distinct promoted-`Q`
`GLD15/GLD16` operator interface.

The direct finite endpoint is the accepted six-vertex theorem.  Equation (9)
is already the eight-vertex matching identity on `A union Bhat`; the missing
step is not physicality of that original tensor.  After a common probe
contraction, its six-label presentation is a matrix-valued first-variation
sum of contracted pair companions times complementary four-decks, not
automatically the matching tensor of a six-vertex graph.  A legal
contraction/splicing that identifies a six-mode tensor with one weighted
`P_6` restriction would enter the accepted theorem.  Rank-one colour pairing
alone does not supply that reduction.

## 5. Sharpness and no-go boundaries

The following distinctions are load-bearing.

1. **Complete target is essential.**  Six rank-one rigid maps may have a
   `2+2+2` colour profile while every same-colour pair companion cancels.
   Such incidence data satisfy rigidity but violate (15), so they are not a
   witness.  Rigidity alone does not prove Theorem 2.
2. **Polynomial nonzero is not fibrewise nonzero.**  A bilinear response can
   contain the nonzero monomial `z_(q_0,c)z_(q_1,c)` and still vanish at a
   particular fully supported point by cancellation with other residual
   monomials.  No response divisor is deleted in Theorem 4.
3. **Pure coefficient is not quotient survival.**  Complete nuisance slices
   can occupy the same pure row.  Equation (19) does not imply (20).
4. **One target is not common attachment.**  `GLD3` does not accept an
   isolated promoted pair row, and `GLD6` requires a much larger lower-depth
   attachment package.  No activity or synchronization is manufactured.
5. **Old-probe activity is structurally unavailable.**  Even if all six
   old-probe pair responses were legally attached and target-diagonal,
   Theorem 5 permits at most one active diagonal colour at each port.  More
   selector work cannot make this branch enter `GLD3` through that window.
6. **Root order is fixed.**  The counting step uses exactly six auxiliary
   labels.  At `r>=4`, the inequalities `|P_c|>=2` leave additional labels
   and do not force a three-pair partition.

## 6. Exact frontier

```text
all-six rigid, all six joint ranks one at r=3:          ASSUMPTION;
canonical 2+2+2 coordinate-colour partition:            PROVED;
full pure pair companion for every colour:              PROVED;
nonzero complementary physical pure deck coefficient:   PROVED;
one or two named promoted pair response polynomials:     PROVED NONZERO;
common torus point retaining GLS4 gates and one response: PROVED EXISTS;
response nonzero on every residual fibre:                OPEN / FALSE IN GENERAL;
complete-nuisance survival and legal selector:            OPEN;
old-probe GLD3 three-colour activity:                      PROVED IMPOSSIBLE;
other-receiver synchronization and activity:              OPEN;
higher-rank all-six-rigid branch:                         OPEN;
unique-nonrigid alternate receiver:                       OPEN;
arbitrary-root and nonzero-anchor coverage:               OPEN;
strategic-node closure:                                   OPEN;
global Krenn--Gu conjecture:                              UNRESOLVED.
```

The smallest successor on this branch is to use the complete mixed/deck
equations either to force a legal contraction/splicing that identifies the
contracted six-mode tensor with a weighted `P_6` restriction accepted by the
committed six-vertex theorem, or to construct a different named receiver with
all of its selector, response, synchronization, nuisance-survival, activity,
and anchor gates.  The old-probe `GLD3` route is closed by Theorem 5.

The higher-rank rigid maps and the unique-nonrigid low-activity star remain
separate branches.

## Verification

Run from repository root:

```text
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_all_rank_one_rigid_colour_pairing_and_promoted_response_supply.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_all_rank_one_rigid_colour_pairing_and_promoted_response_supply.py
```

The primary verifier uses exact rational tensors to replay the unique
pure-slice factorization, exhaustively checks all `3^6` coordinate-readout
profiles and all residual-pair placements, audits the response-monomial
coefficient and cancellation boundary, and checks all `5400` compatible
old-probe profile/window/port activity cases.  The independent
no-project-import audit uses a bounded finite-field shore replay, a separately
implemented sparse label algebra, polynomial-support masks, and a distinct
bit-mask census of the same `5400` cases.  The written proof carries the
characteristic-zero and complete-witness quantifiers; neither bounded replay
is used as a source-witness coverage argument.
