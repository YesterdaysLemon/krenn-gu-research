# Maximum-root surplus-two zero-anchor torus-kernel contraction and five-rigid-label floor

## Status and scope

The global Krenn--Gu conjecture is **UNRESOLVED**.

This document proves `GLS55`.  Let an actual characteristic-zero Krenn--Gu
hypothetical witness carry an eligible maximum-root surplus-two promoted
chart with two probes `A={a_0,a_1}` and auxiliary labels

```text
Bhat=Q disjoint-union Uhat,        |Bhat|=2r,        r>=3.
```

Assume that the physical probe--probe edge block is zero.  For every
`t in Bhat`, combine the two full physical probe-incidence maps into

```text
J_t:V_t -> V_(a_0)^* direct-sum V_(a_1)^*,
J_t(v)=(W_(a_0,t)(-,v),W_(a_1,t)(-,v)).               (1)
```

Call `t` **torus-rigid** when

```text
ker J_t intersect (K^*)^3 = empty.                    (2)
```

Then at least five auxiliary labels are torus-rigid:

```text
|Rig|>=5.                                             (3)
```

This is a statement about the original full maps, before any residual point
is fixed.  It is pointwise on every incidence-rank, deck-zero, response,
selector, nuisance, divisor, and cancellation fibre.  It assumes no full
swallow, no nonzero response, and no chosen minor.

Over a characteristic-zero field, (2) is equivalent to an exact coordinate
readout condition:

```text
e_(t,c)^* in im J_t^* for some c in {0,1,2}.           (4)
```

Consequently at least five labels have one local target coordinate in the
row span of their combined probe incidence.  This is not a legal target
selector: the coordinate and realizing probe row may depend on the label,
and (4) does not annihilate any complete labelled nuisance module or force a
physical response.

The proof partially contracts every non-rigid outside label at its own fully
supported simultaneous-kernel vector.  If there were at most four rigid
labels, four open vertices could be chosen to contain them all.  The complete
`GLS8` identity would then become the matching tensor of a legal weighted
six-vertex graph, excluded by the accepted six-vertex theorem.

## Dependencies and provenance

- `GLS8` owns the complete uncontracted two-probe identity and its physical
  companion/deck typing.
- The accepted computer-assisted
  [`six-vertex theorem`](../finite/n06/SIX_VERTEX_CERTIFICATE.md) excludes
  every complex six-vertex Krenn--Gu solution in three or more colours.
- `GLS54` previously proved the weaker pointwise activity floor.  It is now a
  corollary of (3), not a dependency of this proof.

The new step is to contract *all* outside non-rigid labels at independently
chosen torus-kernel vectors, rather than first fixing the residual pair and
classifying active labels.  The focused verifier checks the complete
four-slot contraction, target weights, matching reconstruction, rank
profiles, and coordinate-row criterion.  The independent no-import audit
uses a bit-mask matching census and a complete finite-field subspace census
with a different kernel representation.  The written proof carries the
arbitrary-root and characteristic-zero quantifiers.

## 1. Full-map rigidity

Work first over a characteristic-zero field `K`.  Put

```text
X_t=W_(a_0,t),             Y_t=W_(a_1,t),
J_t=(X_t,Y_t).                                        (5)
```

Here `X_t,Y_t` are whole-domain maps for *every* `t in Bhat`, including the
two residual labels.  No residual vector has yet been chosen.

Let

```text
Rig={t in Bhat:ker J_t intersect (K^*)^3=empty}.       (6)
```

### Lemma 1 (torus-free linear kernels)

For a linear map `J:K^3 -> W` over an infinite field, the following are
equivalent:

1. `ker J intersect (K^*)^3=empty`;
2. `ker J subset {v:v_c=0}` for some coordinate `c`;
3. `e_c^* in im J^*` for some coordinate `c`.

#### Proof

Let `L=ker J`.  If `L` has no fully supported vector, then

```text
L=union_(c=0)^2 (L intersect {v_c=0}).                (7)
```

An infinite-field vector space cannot be the union of finitely many proper
linear subspaces.  Hence one member of (7) equals `L`, which proves 1 implies
2.  The reverse implication is immediate.

Condition 2 says that the coordinate covector `e_c^*` annihilates `ker J`.
In finite dimensions,

```text
(ker J)^perp=im J^*,                                  (8)
```

so 2 and 3 are equivalent.  `square`

The rank profiles in Lemma 1 are exact:

```text
rank J=0: not rigid;
rank J=1: rigid iff ker J is one coordinate plane;
rank J=2: rigid iff its kernel line has a zero coordinate;
rank J=3: rigid.                                      (9)
```

These are rank equalities and row-space incidences.  They divide by no minor
and retain every exceptional fibre.

## 2. Four-slot contraction of the complete identity

Assume for contradiction that

```text
|Rig|<=4.                                             (10)
```

Since `|Bhat|=2r>=6`, choose a four-set

```text
P subset Bhat,             Rig subset P,             |P|=4,
C=Bhat-P.                                             (11)
```

Every `t in C` is non-rigid.  Choose, independently for every such label,

```text
k_t in ker J_t intersect (K^*)^3.                    (12)
```

Start from the complete uncontracted `GLS8` identity of the actual witness:

```text
T_W(-_A,-_Bhat)
 =sum_(D in binom(Bhat,2)) G_D^A tensor H_(Bhat-D)
  +omega tensor H_Bhat,                               (13)
```

where

```text
omega=W_(a_0,a_1)=0.                                 (14)
```

Leave the four vertices of `P` open and evaluate every `t in C` at `k_t`.
This is a direct partial evaluation of the actual complete graph identity.
No variable is reopened from a fixed-residual quotient.

### Lemma 2 (complete outside-pair vanishing)

After the evaluation (12), every term with `D not subset P` has zero root
companion.

#### Proof

Choose `t in D intersect C`.  The two-by-two companion is the sum of the two
probe-to-`D` bijections.  Each bijection uses either `X_t(k_t)` or
`Y_t(k_t)`.  Both vanish by (12), so the whole evaluated `G_D^A` is zero.
This covers pairs with one or two endpoints in `C`.  `square`

The top term is zero by (14).  For every pair `{k,l} subset P`, define the
partially contracted physical complement

```text
E_kl=H_(C union {k,l})(k_C,-_k,-_l)
     in V_k^* tensor V_l^*.                          (15)
```

For a surviving pair `D subset P`, its complement is

```text
Bhat-D=C union (P-D),                                 (16)
```

so (15) has exactly the two open slots in `P-D`.  Equation (13) becomes

```text
sum_(D in binom(P,2)) G_D^A tensor E_(P-D)
 =sum_(c=0)^2 beta_c
    e_(a_0,c)^* tensor e_(a_1,c)^*
    tensor tensor_(t in P)e_(t,c)^*,                 (17)
```

with

```text
beta_c=product_(t in C) k_(t,c) !=0.                 (18)
```

No response or complementary deck is assumed nonzero.  Zero `G_D^A` and
zero `E_(P-D)` terms remain legal zero edge contributions.

## 3. Legal six-vertex reconstruction

Build a graph on the six physical vertices `A disjoint-union P` as follows:

```text
edge a_0--a_1:           0;
edge a_i--t:             W_(a_i,t),       t in P;
edge k--l:               E_kl,            {k,l} subset P.    (19)
```

Every block in (19) is bilinear on the declared local spaces.  The fifteen
perfect matchings split exactly as follows:

- three use the zero probe edge and vanish;
- the remaining twelve choose one pair `D subset P` to meet the two probes,
  in either orientation, and use the edge on `P-D`.

For fixed `D`, the two orientations give exactly `G_D^A`, and the remaining
edge is `E_(P-D)`.  Thus the matching tensor of (19) is precisely the left
side of (17).

By (18), the right side is fully supported weighted ternary GHZ.  Scale the
three coordinate covectors at `a_0` by `beta_c^(-1)`.  This is an invertible
local change of basis and turns (17) into the normalized six-vertex
Krenn--Gu target.  The accepted six-vertex theorem excludes it.  This
contradiction proves (3).  `square`

For an arbitrary characteristic-zero field, all graph coefficients, chosen
vectors, and inverses used above generate a finitely generated extension of
`Q`.  It embeds in `C`; the embedding preserves every equality and every
declared nonzero coordinate.  The complex six-vertex theorem therefore gives
the same contradiction.

## 4. Pointwise consequences and remaining five-label interface

### Corollary 4.1 (uniform activity floor)

Fix any fully supported residual point.  Every torus-rigid promoted label is
active because its whole joint map is nonzero.  Every torus-rigid residual
label is active because its fully supported fixed residual vector cannot lie in the
joint kernel.  Hence the five labels supplied by (3) belong to the auxiliary
activity set at every fully supported residual point:

```text
|Act|>=|Rig|>=5.                                      (20)
```

Thus `GLS55` strictly strengthens the `GLS54` conclusion.  A nonzero map may
still be non-rigid when its joint kernel meets the torus, so the two notions
are not equivalent.

### Corollary 4.2 (coordinate readouts)

For at least five labels, Lemma 1 supplies a coordinate `c(t)` such that

```text
e_(t,c(t))^* in im J_t^*.                            (21)
```

At least two of those five labels must be assigned the same coordinate by
the pigeonhole principle.  Equation (21) remains only a local probe-incidence
row-space statement.  The realizing dual row, target coordinate, and probe
combination may vary with `t`.

If `|Rig|=5`, retain those five labels and contract every non-rigid label at
an independently chosen fully supported joint-kernel vector.  This leaves the
exact seven-party identity

```text
sum_(D in binom(Rig,2)) G_D^A tensor E_(Rig-D)
 =sum_c beta_c r_c tensor (e_c^*)^tensor Rig,         (22)
```

where each `E_(Rig-D)` is a physical trilinear deck.  Equation (22) is not a
legal graph reconstruction on seven vertices: an ordinary graph matching
tensor has even vertex number, and a trilinear deck is not an edge block.
No factorization of these ten trilinear decks follows from `GLS8`.

## 5. Exact frontier

```text
zero-anchor full-map torus-rigid label floor five:      PROVED;
coordinate-row certificate for each rigid label:        PROVED;
uniform pointwise activity floor five:                   PROVED (corollary);
all rank/divisor/response/deck fibres retained:          PROVED;
exactly-five-rigid trilinear physical identity:          PROVED;
six-or-more-rigid physical-deck coupling:                OPEN;
five-label trilinear decks factor as graph edges:        NOT CLAIMED;
nonzero physical promoted response:                      OPEN;
constant normalized selector / complete nuisance kill:  OPEN;
projective synchronization and selected activity:        OPEN;
target-pure anchor and named downstream receiver:        OPEN;
nonzero-anchor branches:                                 OPEN;
strategic-node closure:                                  OPEN;
global Krenn--Gu conjecture:                             UNRESOLVED.
```

The theorem is support-free and arbitrary-root, but it does not close the
maximum-root surplus-two supply-and-target-attachment node.  Coordinate
readout is not response activity, nuisance survival, or a selector theorem.

## Verification

Run from repository root:

```powershell
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_torus_kernel_contraction_and_five_rigid_label_floor.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_torus_kernel_contraction_and_five_rigid_label_floor.py
```

The primary verifier uses exact rational row reduction, enumerates every
four-slot/outside-pair type for root orders three through seven, checks the
target weights and the `15=3+12` matching reconstruction, and audits all four
joint-rank profiles.  The independent standard-library audit imports no
project code or algebra package.  It uses bit masks, reverse matching
enumeration, a complete `F_5^3` subspace census, and separate modular rank
and torus tests.  Those bounded computations replay the exact interfaces;
the written proof carries arbitrary `r` and characteristic zero.
