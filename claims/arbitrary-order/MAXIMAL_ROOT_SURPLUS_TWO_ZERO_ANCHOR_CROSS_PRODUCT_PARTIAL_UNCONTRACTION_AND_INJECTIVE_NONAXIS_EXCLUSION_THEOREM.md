# Maximum-root surplus-two zero-anchor cross-product partial-uncontraction and all-injective exclusion

## Status and scope

**Exact characteristic-zero arbitrary-root partial-uncontraction hierarchy and
root-order-three source-branch exclusion (`GLS61`).**  Begin with an actual
hypothetical Krenn--Gu witness in the complete promoted two-probe interface of
`GLS8`, and assume the zero-anchor branch of `GLS23`.  Retain the same physical
graph and all complete mixed target equations.

For arbitrary promoted root order, contract each selected auxiliary label at
the cross product of its two evaluated probe rows, but leave an arbitrary set
of auxiliary labels open.  A physical companion term is **structurally
retained exactly** when both of its labels remain open; a retained term may
still evaluate to zero.  This gives one compatible hierarchy of partially
uncontracted complete equations.  Its zero-open member is the scalar
cross-product identity of `GLS58`; its one-open and higher-open members are
strictly stronger.

At root order three there are six auxiliary labels.  The one-open equations
force every target colour to have at least two labels whose corresponding
cross-product coordinate vanishes identically.  If all six joint probe maps
are injective and no label lies on a pure-probe axis, the exact injective
classification from `GLS58` then forces a labelled `2+2+2` partition.  The
two-open equation for either same-colour pair forces its physical companion
to be a nonzero pure diagonal rank-one tensor.  Each of the four possible
injective shore orientations has a nonzero off-diagonal projection, a
contradiction.

The same hierarchy also excludes every nonempty collection of
**pure-probe-axis** labels:

```text
row X_t=0, row Y_t=V_t^*,
or
row Y_t=0, row X_t=V_t^*.                              (1)
```

Combined with `GLS58`, every all-six-rigid point is therefore in the exact
cover

```text
some joint probe map has rank < 3.                     (2)
```

This closes the complete all-injective root-order-three branch.  It does not
exclude any deficient-map branch, the unique-nonrigid branch, nonzero
anchor, arbitrary-root attachment, response or selector failure, or the
global conjecture.  The global Krenn--Gu status remains **UNRESOLVED**.

## Dependencies and provenance

- [`GLS8`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_TWO_PROBE_ONE_TARGET_ATTACHMENT_AND_POINTWISE_FAILURE_REDUCTION_THEOREM.md)
  owns the complete uncontracted two-probe physical identity.
- [`GLS23`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_TRANSVERSE_COMPLETE_NUISANCE_DECOMPOSITION_AND_TOP_ANCHOR_DICHOTOMY_THEOREM.md)
  owns the zero-anchor branch.
- [`GLS55`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_TORUS_KERNEL_CONTRACTION_AND_FIVE_RIGID_LABEL_FLOOR_THEOREM.md)
  owns torus rigidity and the rank-zero through rank-three joint-kernel
  classification.
- [`GLS58`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_ALL_RIGID_KERNEL_CONTRACTION_AND_CROSS_PRODUCT_REDUCTION_THEOREM.md)
  owns the cross-product definition, the fully contracted scalar identity,
  and the injective coordinate-visibility lemma.

The new step is to return to the **complete tensor identity before fully
contracting the auxiliary labels**.  No source term, deck label, or mixed
target coefficient is discarded.  No response, selector, rank minor,
cross-product coordinate, or physical deck is divided by.

## 1. Complete promoted identity and cross-product kernels

Let

```text
A={a_0,a_1}
```

be the two probes, and let `Bhat` be the even auxiliary set in the complete
`GLS8` chart.  At promoted root order `r`, `|Bhat|=2r`.  On the zero-anchor
branch the complete physical matching identity is

```text
T_W(-_A,-_Bhat)
 =sum_(D in binom(Bhat,2)) G_D^A tensor H_(Bhat-D).    (3)
```

The target is the weighted diagonal

```text
T_W
 =sum_(c=0)^2
    mu_c e_(a_0,c)^* tensor e_(a_1,c)^*
      tensor tensor_(t in Bhat)e_(t,c)^*.             (4)
```

Here every target weight `mu_c` is nonzero.  They are retained explicitly;
only their nonvanishing is used below.

Introduce independent probe indeterminates `z_0,z_1`.  At every auxiliary
label `t`, write

```text
p_t=X_t(z_0,-),
q_t=Y_t(z_1,-),
k_t=p_t cross q_t.                                    (5)
```

Thus

```text
p_t(k_t)=q_t(k_t)=0                                   (6)
```

as polynomial identities in the probe coordinates.  All expressions below
belong to the polynomial ring over the characteristic-zero source field in
the coordinates of `z_0,z_1`.

## 2. The partial-uncontraction hierarchy

For a subset `S subseteq Bhat`, contract every `t in Bhat-S` at `k_t` and
leave precisely the labels of `S` open.  For `D subseteq S`, put

```text
g_D(z_0,z_1)=G_D^A(z_0,z_1,-_D),                     (7)
```

and evaluate the deck `H_(Bhat-D)` at `k_t` for the labels outside `S`,
leaving its `S-D` slots open.

### Theorem 1 (complete cross-product partial-uncontraction)

For every `S subseteq Bhat`, the exact tensor identity

```text
sum_(D in binom(S,2))
  g_D(z_0,z_1)
    tensor H_(Bhat-D)(k_(Bhat-S),-_(S-D))

 =sum_(c=0)^2 mu_c z_(0,c)z_(1,c)
      product_(t in Bhat-S)(k_t)_c
      tensor_(s in S)e_(s,c)^*                       (8)
```

holds in the polynomial ring over the source field.  It therefore
specializes as an identity to every joint-rank and cross-product divisor
fibre.  All domain deductions below are made in the ambient polynomial ring
before any such specialization.

### Proof

Apply the declared partial evaluation to (3).  If a pair `D` contains a
contracted label `t`, its companion factor contains

```text
p_t(k_t) or q_t(k_t),                                 (9)
```

and is zero by (6).  Conversely, a pair term whose two labels lie in `S` is
not killed by this contraction argument and is retained with its complete
physical deck.  Thus the **structurally retained** pair set is exactly
`binom(S,2)`; an individual retained companion or deck is still allowed to
vanish.  This gives the left side of (8).

The same partial evaluation of (4) gives the right side.  This is one
evaluation of the original same-graph identity, not a reconstruction from
independently chosen local charts.  `square`

The first three levels are:

```text
S=empty:
  sum_c mu_c z_(0,c)z_(1,c) product_t(k_t)_c=0;       (10)

S={s}:
  mu_c z_(0,c)z_(1,c) product_(t!=s)(k_t)_c=0
  for every c;                                        (11)

S={s,u}:
  g_(su)(z_0,z_1) H_(Bhat-{s,u})(k_(Bhat-{s,u}))
   =sum_c mu_c z_(0,c)z_(1,c)
      product_(t notin {s,u})(k_t)_c
      e_(s,c)^* tensor e_(u,c)^*.                    (12)
```

Equation (10) is `GLS58`.  Equations (11)--(12) retain target coordinates
that (10) sums together and are therefore genuinely stronger.

## 3. The one-open double-cover theorem

Define

```text
Z_c={t in Bhat : (k_t)_c is the zero polynomial}.    (13)
```

### Corollary 2 (two labels kill every colour)

For every target colour `c`,

```text
|Z_c|>=2.                                             (14)
```

### Proof

Fix `s,c` in (11).  The polynomial ring is a domain, and
`mu_c z_(0,c)z_(1,c)` is nonzero.  Therefore some `t!=s` lies in `Z_c`.
If `Z_c` were empty this would fail for every `s`; if it were the singleton
`{s_0}`, it would fail for `s=s_0`.  Hence (14).  `square`

This is a complete-mixed target consequence.  The fully contracted scalar
identity (10) proves only `|Z_c|>=1` when its three summands vanish termwise.

## 4. Injective nonaxis labels

For a label `t`, put

```text
R_t^X=row X_t,
R_t^Y=row Y_t.                                        (15)
```

Assume the joint map `J_t=(X_t,Y_t)` is injective.  `GLS58` proves that
`(k_t)_c=0` identically exactly in one of the two orientations

```text
X-orientation at c:
  R_t^X subseteq K e_c^*,  pi_c(R_t^Y)=K^2;

Y-orientation at c:
  R_t^Y subseteq K e_c^*,  pi_c(R_t^X)=K^2.           (16)
```

Moreover `k_t=0` identically exactly on a pure-probe axis (1).

### Lemma 3 (one zero coordinate per nonaxis injective label)

If `J_t` is injective and `k_t` is not the zero polynomial, then `t` belongs
to at most one of `Z_0,Z_1,Z_2`.

### Proof

Suppose (16) holds for two distinct colours.  If the two orientations agree,
the corresponding pure shore is contained in two distinct coordinate lines
and is therefore zero.  Injectivity then forces the opposite shore to equal
`V_t^*`, which is a pure-probe axis and makes `k_t=0`.

If the orientations differ, one orientation requires the projection of a
coordinate line onto a complementary two-space to be surjective, which is
impossible.  Thus a nonaxis label has at most one zero coordinate.  `square`

## 5. Root-order-three `2+2+2` forcing

Now let `r=3`, so `|Bhat|=6`, and assume all six joint maps are injective and
no label lies on a pure-probe axis.

### Corollary 4 (exact zero-coordinate partition)

The sets in (13) are pairwise disjoint and

```text
Bhat=Z_0 disjoint-union Z_1 disjoint-union Z_2,
|Z_0|=|Z_1|=|Z_2|=2.                                  (17)
```

### Proof

Corollary 2 gives at least six total label-colour incidences.  Lemma 3 gives
at most one incidence per label, hence at most six.  Equality holds
throughout.  `square`

This conclusion does not choose a generic rank minor or a convenient
contraction.  It holds on the complete all-injective nonaxis locus.

## 6. The two-open contradiction

Fix `c` and write

```text
Z_c={s,u}.                                             (18)
```

In (12), every target-colour coefficient except `c` vanishes because both
of its zero labels remain among the four contracted labels.  The `c`
coefficient is nonzero because neither of its two zero labels is contracted
and every remaining `(k_t)_c` is a nonzero polynomial.  Thus

```text
g_(su)(z_0,z_1) h_(su)(z_0,z_1)
 =lambda_c(z_0,z_1)e_(s,c)^* tensor e_(u,c)^*,        (19)
```

where

```text
h_(su)=H_(Bhat-{s,u})(k_(Bhat-{s,u})),
lambda_c=mu_c z_(0,c)z_(1,c)
  product_(t notin {s,u})(k_t)_c !=0.                 (20)
```

In particular `h_(su)` and `g_(su)` are nonzero, and `g_(su)` has no
off-`(c,c)` coordinate.

### Lemma 5 (injective orientation obstruction)

Let `s,u` satisfy either orientation in (16) for the same colour `c`, and
assume neither is a pure-probe axis.  Then

```text
g_(su)=p_s tensor q_u+q_s tensor p_u                 (21)
```

has a nonzero coordinate outside `(c,c)`.

### Proof

There are four orientation pairs.

- In the `X/X` case, project the `u` factor by `pi_c`.  The second summand
  dies because `p_u` is on the `c`-axis, while the first becomes
  `p_s tensor pi_c(q_u)`, which is nonzero: `p_s` cannot vanish without
  making `s` a pure-probe axis, and `pi_c(R_u^Y)=K^2`.
- The `Y/Y` case is symmetric.
- In the `X/Y` case, project both factors by `pi_c`.  The first summand dies,
  while the second has both projected factors spanning `K^2` and is nonzero.
- The `Y/X` case is symmetric.

Thus (21) is never supported only at `(c,c)`.  `square`

### Theorem 6 (all-injective nonaxis exclusion)

There is no root-order-three zero-anchor complete witness for which all six
joint probe maps are injective and every cross product `k_t` is nonzero as a
polynomial.

### Proof

Corollary 4 supplies (18).  Equation (19) says the corresponding companion is
pure at `(c,c)`, while Lemma 5 gives a nonzero off-diagonal coordinate.  This
is a contradiction.  `square`

### Corollary 6.1 (intermediate all-six-rigid cover)

On the `GLS56` all-six-rigid, zero-anchor, root-order-three branch, every
hypothetical witness satisfies at least one of:

1. some `J_t` has rank below three;
2. all `J_t` have rank three and some label is on a pure-probe axis (1).

`GLS58` owns the deficient-map continuations.  Before using the higher-open
equations in Section 7, the pure-probe-axis source boundary is the only
remaining all-injective leaf.

## 7. Every pure-probe-axis multiplicity is impossible

Assume again that all six `J_t` are injective.  Let `P` be the nonempty set
of pure-probe-axis labels and put `U=Bhat-P`.  For every colour define the
nonaxis zero set

```text
E_c={u in U : (k_u)_c is the zero polynomial}.        (22)
```

The three `E_c` are pairwise disjoint by Lemma 3.  Every member of `P` lies
in all three `Z_c` because its whole cross product is zero.

Work over the fraction field `F` of the ambient polynomial ring.  For
`p in P`, define its active full-row covector

```text
a_p=q_p if R_p^X=0 and R_p^Y=V_p^*,
a_p=p_p if R_p^Y=0 and R_p^X=V_p^*.                  (23)
```

Let

```text
pi_p: V_p^* tensor F -> (V_p^* tensor F)/(F a_p)     (24)
```

be the active-line quotient.  Since the active probe map has full row
space, every coordinate component of `a_p` is a nonzero element of `F`, and
`a_p` is not proportional over `F` to any fixed coordinate covector.  Thus
`pi_p(e_(p,c)^*)!=0` for every colour.

### Lemma 7.1 (active-line annihilation)

If a physical pair `D` meets `P`, then its evaluated companion `g_D` is
killed by the active-line quotient at some pure endpoint.

Indeed, two same-type pure axes have zero companion.  Two opposite-type
axes have companion `a_p tensor a_q`.  A pure axis paired with a nonaxis
label has companion `a_p tensor p_u` or `a_p tensor q_u`, up to the canonical
labelled-factor order.  In every nonzero case an active line is explicit.
`square`

Consequently, if `S` contains `P` and at most one member of `U`, applying
`tensor_(p in P) pi_p` to the `P`-slots kills every term on the left side of
(8).  The physical deck factors cannot evade this quotient because the
active line occurs in the separate companion factor.

### Lemma 7.2 (a nonempty diagonal survives the active quotients)

Let `|P|>=2`.  Any nonempty weighted coordinate diagonal

```text
sum_(c in C) lambda_c tensor_(p in P)e_(p,c)^*,
lambda_c!=0,                                           (25)
```

has nonzero image under `tensor_(p in P) pi_p`.

To see this, select `c_0 in C`.  There are at most two other colours and at
least two pure slots.  Assign each other colour `d` to a different pure
slot.  At that slot choose an `F`-linear functional annihilating `a_p` and `e_(p,d)^*`
but not `e_(p,c_0)^*`; it exists because the remaining coordinate of the
full variable covector `a_p` is nonzero.  At every unused pure slot choose a
similar `F`-linear functional annihilating `a_p` but not `e_(p,c_0)^*`.
All these functionals are `F`-linear; they are used only after embedding the
polynomial identity into its fraction field.  Their tensor product kills
every unwanted diagonal term and reads the `c_0` term nontrivially. `square`

We now force a nonaxis zero for every colour.

- If `|P|=1`, Corollary 2 and `P subseteq Z_c` give `E_c!=empty` for all
  `c`.
- If `|P|>=2` and some `E_c` were empty, use the `S=P` member of (8).  Its
  target is the nonempty diagonal indexed by
  `{c:E_c=empty}`.  Lemma 7.1 kills its entire source side after the active
  quotients, while Lemma 7.2 retains its target side, a contradiction.

Thus all three disjoint sets `E_c` are nonempty.  Hence `|U|>=3` and
`1<=|P|<=3`.  Since `|U|` is respectively five, four, or three, at least one
colour `c` has a unique nonaxis zero

```text
E_c={u}.                                               (26)
```

Use the hierarchy member `S=P union {u}`.  Colour `c` has no zero factor
outside `S`, while every other colour has a member of its nonempty disjoint
set `E_d` outside `S`.  The target side is therefore the single nonzero pure
tensor

```text
lambda_c
  tensor_(p in P)e_(p,c)^* tensor e_(u,c)^*,
lambda_c!=0.                                          (27)
```

Every retained pair in `binom(S,2)` meets `P`, because `u` is the only
nonaxis label in `S`.  Lemma 7.1 therefore kills the complete source side
after applying all active-line quotients.  The pure tensor (27) survives
every quotient, a contradiction.

### Theorem 7 (all-injective branch exclusion)

There is no root-order-three zero-anchor complete witness for which all six
joint probe maps are injective.  Theorem 6 excludes the empty pure-axis set;
the preceding argument excludes every nonempty pure-axis set.  `square`

### Corollary 7.3 (sharpened all-six-rigid cover)

On the `GLS56` all-six-rigid, zero-anchor, root-order-three branch, every
hypothetical witness has at least one joint probe map of rank below three.
The deficient-map source-integrability branches are the only remaining
all-six-rigid leaves.

## 8. Sharp controls and scope walls

The exact all-injective physical control in `GLS58` has three termwise-zero
products in (10) and therefore satisfies the scalar cross-product identity.
Its zero sets are

```text
Z_0={2},       Z_1={1,4,5},       Z_2={0,3}.          (28)
```

The `c=0,s=2` instance of (11) is nonzero, so the control fails the complete
one-open hierarchy.  This is consistent with its `61` nonzero mixed target
words.  It proves that the passage from (10) to (11) genuinely uses the
complete GHZ tensor equation and is not formal cross-product algebra.

The following remain open and are not weakened by this theorem:

- every one-deficient and two-deficient GLS58 branch, including binary
  six-vertex descents;
- the GLS57 rank-one pure-companion receiver problem and GLS60 splice
  boundary;
- the GLS59 unique-nonrigid branch;
- nonzero anchor and silent `p=0` source coverage;
- complete-nuisance survival, normalized selectors, response
  synchronization/activity, and entry to a named downstream detector;
- promoted root order at least four, where (14) does not by itself exhaust
  all labels;
- any global proof or exact counterexample.

In particular this theorem does not call a binary or monocolour six-vertex
descent contradictory, and it does not convert a raw pure companion into a
legal target selector.

## 9. Exact frontier

```text
arbitrary-root cross-product partial-uncontraction hierarchy: PROVED;
one-open two-zero-label floor for every colour:                PROVED;
two-open physical companion/deck identity:                     PROVED;
r=3 nonaxis injective 2+2+2 partition:                         PROVED;
r=3 all-injective nonaxis branch:                              EXCLUDED;
r=3 every nonempty pure-axis branch:                           EXCLUDED;
r=3 complete all-injective branch:                             EXCLUDED;
deficient all-rigid and unique-nonrigid branches:              OPEN;
response/selector/synchronization/activity package:            OPEN;
nonzero-anchor and arbitrary-root strategic node:              OPEN;
global Krenn--Gu conjecture:                                   UNRESOLVED. (29)
```

The smallest parent continuation is now to couple the deficient branches
through further members of (8), rather than returning to the fully
contracted scalar identity.  A useful successor must either:

1. obtain a same-source lower-order GHZ/permanent restriction from an
   exhaustive deficient-rank cover; or
2. transport a nonzero pure companion/deck coefficient into a complete
   promoted quotient with response, selector, synchronization, activity,
   and anchor gates.

## 10. Verification boundary

From repository root run

```powershell
uv run --with sympy python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_cross_product_partial_uncontraction.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_cross_product_partial_uncontraction.py
python -m py_compile claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_cross_product_partial_uncontraction.py claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_cross_product_partial_uncontraction.py
uv run --with ruff ruff check claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_cross_product_partial_uncontraction.py claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_cross_product_partial_uncontraction.py
uv run --with ruff ruff format --check claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_cross_product_partial_uncontraction.py claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_cross_product_partial_uncontraction.py
```

The primary verifier checks all `64` open-label sets, the exact companion
survival ledger, all `4^6=4096` nonaxis zero-coordinate assignments, the `90`
labelled `2+2+2` partitions, all twelve nonaxis colour/orientation cases, the
`1365` zero-coordinate assignments across all six nonempty pure-axis
multiplicities, their exhaustive one-open/axis-set/singleton-quotient
classification, and the GLS58 scalar sharpness control with its one-open
failure.

The independent audit imports no project code and no symbolic algebra.  It
uses a separate bitmask open-set census, support-set companion calculation,
and finite zero-cover enumeration.  Both scripts audit the finite and
displayed identities; the arbitrary-root matching partition, polynomial
domain argument, and tensor-projection obstruction are the written proof.
