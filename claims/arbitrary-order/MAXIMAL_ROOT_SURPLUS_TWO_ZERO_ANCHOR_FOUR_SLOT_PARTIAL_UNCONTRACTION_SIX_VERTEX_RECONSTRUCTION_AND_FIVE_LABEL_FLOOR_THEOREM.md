# Maximum-root surplus-two zero-anchor four-slot partial-uncontraction six-vertex reconstruction and five-label floor

## Status and scope

The global Krenn--Gu conjecture is **UNRESOLVED**.

This document proves `GLS54`.  Let an actual characteristic-zero Krenn--Gu
hypothetical witness carry an eligible maximum-root surplus-two promoted
chart.  Fix any fully supported residual point and suppose the physical
probe--probe anchor is zero.  Then at least five of the two residual labels
and promoted labels are effective at that point:

```text
|Act|>=5.                                             (1)
```

The proof starts from the complete uncontracted graph identity, not from one
abstract fixed-residual equation.  If at most four labels are effective, pad
them to four using only inactive promoted ports, leave those four physical
vertices open, and contract every other target vertex.  Every raw root-pair
label outside the open four-set vanishes.  Each surviving complementary
physical deck becomes a bilinear edge on the other two open vertices, so the
complete source is a reconstructed legal six-vertex graph.  The accepted
six-vertex theorem excludes its fully supported ternary GHZ target.

The distinction between active and inactive residual labels is load-bearing.
An active residual vertex may be left open because the proof retains it from
the complete tensor equality.  An inactive residual vertex is contracted at
the exact fixed vector that kills both of its root shores; it is never
reopened.  Its full physical incidence maps may be nonzero transversely.

The result is pointwise on every incidence-rank, nuisance-rank, deck-zero,
response, selector, divisor, cancellation, and residual-shore fibre inside
the fully supported residual torus.  It assumes no full-swallow condition
and divides by no response, deck, selector, or minor.  It does not supply a
source-to-attachment edge, a legal downstream package, a five-label
classification, nonzero-anchor closure, strategic-node closure, or global
resolution.

## Dependencies and provenance

- `GLS8` gives the complete open-probe identity
  before any residual vertex is contracted.
- `GLS39` gives the auxiliary residual/promoted label convention and its
  pointwise effectiveness interface.
- `GLS36` supplies an essential scope warning: one fixed residual equation
  does not imply the full residual family.  The present theorem assumes an
  actual complete witness and partially contracts its full identity.
- `GLS53` is the no-residual, exactly-four-promoted special case and
  corroborates the matching reconstruction.  It is not needed to prove the
  stronger floor (1).
- The accepted computer-assisted
  [`six-vertex theorem`](../finite/n06/SIX_VERTEX_CERTIFICATE.md) excludes
  every complex six-vertex Krenn--Gu solution in three or more colours.

The new step is the licensed partial uncontraction of active residual
vertices together with inactive-promoted padding.  The focused verifier
checks every activity size and residual-label composition, exact complement
typing, target weights, and the fifteen-matching identity.  The independent
no-import audit uses a separate bit-mask representation, exact finite-field
physical maps, and a hostile inactive-residual transverse control.  The
written proof carries arbitrary root order and characteristic zero.

## 1. Activity after fixing the residual point

Retain

```text
A={a_0,a_1},                  Q={q_0,q_1},
Bhat=Q disjoint-union Uhat,   |Uhat|=2r-2>=4,
T=Q disjoint-union Uhat.
```

For every promoted `u in Uhat`, let

```text
X_u:V_u -> V_(a_0)^*,        Y_u:V_u -> V_(a_1)^*   (2)
```

be the whole-domain physical root-incidence maps.  Fix fully supported
residual vectors `z_(q_0),z_(q_1)`.  For `q_s in Q`, put

```text
xi_0^s=W_(a_0,q_s)(-,z_(q_s)),
xi_1^s=W_(a_1,q_s)(-,z_(q_s)).                       (3)
```

The auxiliary activity set at this fixed point is

```text
Act={u in Uhat:X_u!=0 or Y_u!=0}
    union {q_s in Q:xi_0^s!=0 or xi_1^s!=0}.         (4)
```

Assume for contradiction that

```text
m=|Act|<=4.                                          (5)
```

Let `s=|Act intersect Q|` and `p=|Act intersect Uhat|`, so `m=s+p`.
The number of inactive promoted labels is

```text
2r-2-p.
```

The number needed to pad `Act` to four is `4-m`.  Their difference is

```text
(2r-2-p)-(4-m)=2r-6+s>=0.                            (6)
```

Choose `F subset Uhat-Act` with `|F|=4-m` and put

```text
P=Act union F,             |P|=4,
C=Bhat-P.                                             (7)
```

Every label in `F` is an inactive promoted port, so both of its whole-domain
maps in (2) vanish.  No inactive residual label is used for padding.

## 2. Legal partial contraction of the full identity

Start from the complete `GLS8` identity of the actual witness:

```text
T_W(-_A,-_Bhat)
 =sum_(D in binom(Bhat,2)) G_D^A tensor H_(Bhat-D)
  +omega tensor H_Bhat.                              (8)
```

This equality is multilinear in every vertex of `Bhat`.  Leave all four
vertices of `P` open.  For every vertex in `C`, contract as follows:

```text
q_s in C intersect Q:       evaluate at z_(q_s),
u   in C intersect Uhat:    evaluate at 1=e_0+e_1+e_2.       (9)
```

The order of operations matters.  Equation (8) is partially evaluated
directly; no active residual variable is inferred or reopened from a
fixed-`Q` quotient.

### Lemma 1 (complete outside-label vanishing)

After (9), every raw pair term with `D not subset P` has zero root companion.

#### Proof

Such a pair `D` contains some `t in C`.  Since `P` contains `Act`, the label
`t` is inactive at the fixed point.

If `t` is promoted, `X_t=Y_t=0` as whole-domain maps.  Both root bijections
in `G_D^A` therefore vanish before or after evaluation.

If `t=q_s` is residual, (9) evaluates its two root edges to the shore vectors
`xi_0^s,xi_1^s`.  Inactivity makes both zero.  Again, each of the two root
bijections contains one of these zero shores.  This covers pairs with one or
two endpoints in `C`, including the residual pair `D=Q` whenever it is not
contained in `P`. `square`

The separate top term in (8) vanishes because the zero-anchor hypothesis is

```text
omega=W_(a_0,a_1)=0.                                 (10)
```

For every pair `{k,l} subset P`, define the partially contracted physical
deck

```text
E_kl
 =H_(C union {k,l})(z_(C intersect Q),1_(C intersect Uhat),-_k,-_l)
 in V_k^* tensor V_l^*.                              (11)
```

This is correctly indexed because for a surviving root pair `D subset P`
with `P-D={k,l}`,

```text
Bhat-D=C union {k,l}.                                 (12)
```

Thus `E_kl` is a bilinear tensor on exactly two open vertices.  It is a legal
effective edge block, whether zero or nonzero; it is not an original induced
edge and is not chosen independently of the physical graph.

For `D={u,v} subset P`, retain the full physical root-pair tensor

```text
mu_uv
 =W_(a_0,u) tensor W_(a_1,v)
  +W_(a_0,v) tensor W_(a_1,u).                       (13)
```

Here `u` or `v` may be residual and left open.  If it is a padded inactive
promoted port, both corresponding root edges in (13) are identically zero.

Lemmas 1 and (10)--(13) turn (8) exactly into

```text
sum_({u,v} subset P) mu_uv tensor E_(P-{u,v})
 =sum_(c=0)^2 beta_c
    e_(a_0,c)^* tensor e_(a_1,c)^*
    tensor (tensor_(t in P)e_(t,c)^*).               (14)
```

Only residual vertices in `C` contribute nontrivial contraction factors to
the target:

```text
beta_c=product_(q_s in C intersect Q) z_(q_s,c).     (15)
```

The empty product is one.  Fully supported residual vectors make every
`beta_c` nonzero.  All-ones promoted contractions contribute one, while an
open padded promoted vertex remains an ordinary pure-colour target slot.

## 3. Reconstructed six-vertex contradiction

Construct a weighted ternary graph on the six vertices `A union P` with edge
blocks

```text
W'_(a_0,a_1)=0,
W'_(a_i,u)=W_(a_i,u),          i in {0,1}, u in P,
W'_(k,l)=E_kl,                 {k,l} subset P.        (16)
```

### Lemma 2 (matching bijection)

The hafnian tensor of (16) is the left side of (14).

#### Proof

There are fifteen perfect matchings on six labelled vertices.  Exactly three
use the zero edge `{a_0,a_1}`.  Every other matching chooses an unordered
pair `{u,v} subset P` hit by the probes.  Its two root orientations sum to
`mu_uv`, and the other two vertices are paired by `E_(P-{u,v})`.
Conversely these six choices and two orientations are the twelve remaining
matchings.  Each has coefficient one. `square`

### Theorem 3 (five-effective-label floor)

Every point in the stated actual-witness scope satisfies (1).

#### Proof

Suppose (5).  Lemma 2 and (14) show that (16) produces weighted ternary GHZ
on six vertices with all three weights nonzero.  Apply at `a_0` the
invertible diagonal local scaling

```text
e_(a_0,c)^* |-> beta_c^(-1)e_(a_0,c)^*.             (17)
```

Every perfect matching contains exactly one edge incident with `a_0`, so
(17) normalizes the three pure weights and preserves every zero mixed
coefficient.  This contradicts the accepted complete six-vertex theorem
over `C`.

For an arbitrary characteristic-zero ground field, the finitely many graph,
contraction, and target coefficients, together with the inverses in (17),
generate a finitely generated extension of `Q`.  It embeds injectively into
`C`, preserving the exact equations and nonzero weights.  The complex
contradiction therefore applies. `square`

At `r=3`, `Bhat` has six vertices and `C` always has two vertices.  The
possible open-set compositions are zero, one, or two residual vertices plus
respectively four, three, or two promoted vertices.  Padding and contraction
work uniformly in all three cases.

## 4. Exact frontier and non-closure boundary

The new pointwise frontier on the zero-anchor branch of an actual witness is

```text
fully supported residual point with |Act|<=4:                 EMPTY;
fully supported residual point with |Act|>=5:                 OPEN;
full-swallow hypothesis:                                     NOT USED;
five-label physical-deck classification or exclusion:        OPEN;
silent source enters full swallow:                            NOT NEEDED FOR (1),
                                                              OPEN FOR ATTACHMENT;
raw escape supplies an original legal target package:        NOT SUPPLIED;
nonzero-anchor marginal/double-transverse branches:           OPEN;
response/activity/synchronization/nuisance/anchor gates:      OPEN;
arbitrary-root strategic-node closure:                        UNKNOWN;
global Krenn--Gu conjecture:                                  UNRESOLVED.
```

`GLS48`, `GLS52`, and `GLS53` remain valid finer fixed-residual theorems and
audited special cases.  The present theorem strengthens only their activity
floor on an actual complete witness.  It does not convert activity into a
physical response, constant selector, synchronized quotient line,
nuisance-surviving target, or named downstream receiver package.

The smallest zero-anchor successor is a support-free treatment of five or
more effective labels using the full physical deck coupling.  Incidence rank
alone is insufficient: existing exact controls may have few labels and
swallow pure rows while failing mixed target coefficients.

## Verification boundary

The focused verifier checks padding availability for every activity size
`0<=m<=4`, all zero/one/two-active-residual compositions, the exact live-pair
and complement census for several root orders, symbolic inactive-residual
shore annihilation, the fifteen-matching identity, target weights, and local
normalization.

The independent audit imports no project code or algebra package.  It uses a
separate bit-mask hafnian, finite-field physical incidence matrices, reversed
support traversal, and an explicit inactive-residual map that kills the
chosen fully supported vector but is nonzero transversely.  That hostile
control confirms why inactive residuals must remain contracted while
inactive promoted labels are safe padding.

The written proof, not either bounded test range, carries arbitrary root
order and characteristic zero.  The accepted six-vertex theorem is a
computer-assisted upstream premise; its authenticated certificate replay is
recorded in the retained review.  Neither checker proves the five-plus-label
successor, any attachment gate, strategic-node closure, or the global
conjecture.
