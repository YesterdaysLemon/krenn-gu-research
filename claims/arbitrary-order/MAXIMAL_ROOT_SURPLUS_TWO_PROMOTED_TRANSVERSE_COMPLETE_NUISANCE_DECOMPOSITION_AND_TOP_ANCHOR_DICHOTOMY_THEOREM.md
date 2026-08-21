# Maximum-root surplus-two promoted transverse complete-nuisance decomposition and top-anchor dichotomy

## Status

**Exact characteristic-zero arbitrary-root physical-module theorem.**  In the
`GLS22` transverse quotient, every remaining nuisance contribution has an
explicit coefficient-slice form determined only by how its promoted complement
pair meets the target complement.  For a complement pair `D`, project its
two-probe companion transversely and slice the port factors of `D` which lie
on the target side.  Tensor those slices with the full missing left port
factors.  Summing these typed spaces over all active unwanted labels, together
with the projected top-grade term, is exactly the complete transverse
nuisance--not merely a contained subspace.

Two consequences are immediate.

1. If the projected root slices of complement pairs disjoint from a pair
   target span `ker epsilon_A`, that target's entire `72`-row transverse space
   is nuisance.
2. Every top-minus-two target contains the common top-anchor nuisance

   ```text
   W_(a_0,a_1) tensor V_C^*.                           (1)
   ```

   If `W_(a_0,a_1)=0`, the promoted top target has zero desired coefficient.
   If it is nonzero, every pair-target selector factors through a further
   exact `63`-row quotient, while the top target survives exactly when this
   same root tensor escapes its explicitly described root-slice nuisance.

At `r=3`, this is an exhaustive top-anchor split for the six promoted pair
targets and promoted four-port target.  It does not force the top anchor to
survive, force any pair target to survive, provide common selection or
activity, or exclude either branch by complete mixed GHZ coefficients.  It
does not close the strategic node.  The global Krenn--Gu conjecture remains
**UNRESOLVED**.

## Dependencies and provenance

The promoted two-probe identity, active labels, complete nuisance definition,
and top desired coefficient come from

- [`GLS8`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_TWO_PROBE_ONE_TARGET_ATTACHMENT_AND_POINTWISE_FAILURE_REDUCTION_THEOREM.md).

The common all-port root line and exact transverse quotient come from

- [`GLS21`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_BASE_SHADOW_ALL_PORT_NUISANCE_COLLAPSE_THEOREM.md); and
- [`GLS22`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_ALL_PORT_TRANSVERSE_QUOTIENT_AND_PROJECTIVE_SYNCHRONIZATION_FAILURE_THEOREM.md).

No external literature claim is used.  The new content is the exact
label-by-label transverse nuisance formula, its disjoint-label collapse
criterion, and the top-anchor dichotomy and `63/8`-row interface.

## 1. Transverse label tensors

Retain the `GLS22` notation

```text
Bhat=Q disjoint-union Uhat,
E_A^*=tensor_(a in A)V_a^*,
q=G_Q^A(z_Q),                  p=epsilon_A(q)!=0,
P_Q=p id_(E_A^*)-q tensor epsilon_A,
E_A^tr=ker epsilon_A,          dim E_A^tr=8.           (2)
```

For a promoted target complement

```text
C in Cprom={empty} union binom(Uhat,2),
S_C=Uhat-C,                                             (3)
```

the transverse left space is

```text
K_C^tr=E_A^tr tensor V_C^*.                            (4)
```

Here `V_empty^*=K`.

For every active complement pair `D in binom(Bhat,2)`, put

```text
D_0=D intersect Uhat,
g_D(z_Q)=G_D^A(z_(D intersect Q))
          in E_A^* tensor V_(D_0)^*,
a_D=(P_Q tensor id_(V_(D_0)^*))g_D
          in E_A^tr tensor V_(D_0)^*.                  (5)
```

The notation means that the `Q` slots actually present in `G_D^A` are
evaluated at their residual vectors.  The remaining `Q-D` slots occur in the
deck input and are evaluated there.  Since every residual vector is nonzero,
that deck evaluation is surjective onto the formal tensor space on
`Uhat-D_0`.

For a tensor `a in E_A^tr tensor V_X^* tensor V_Y^*`, define

```text
Slice_Y(a)=span{(id tensor eta)(a):eta in (V_Y^*)^*}
             subset E_A^tr tensor V_X^*.              (6)
```

Empty-factor conventions are literal.

## 2. Exact coefficient-slice formula

For fixed `C` and `D`, set

```text
X_(C,D)=C intersect D_0,
Y_(C,D)=D_0-C,
Z_(C,D)=C-D_0.                                        (7)
```

Thus `X` is the part of the coefficient tensor kept on the left, `Y` is
sliced on the right, and `Z` comes from the identity action of the formal deck
input on a missing left factor.

Define the inserted subspace

```text
J_(C,D)=Slice_(Y_(C,D))(a_D) tensor V_(Z_(C,D))^*
         subset E_A^tr tensor V_C^*.                  (8)
```

For `C!=empty`, define also

```text
J_C^top=K(P_Q G_empty^A) tensor V_C^*
       =K(p W_(a_0,a_1)) tensor V_C^*.                (9)
```

For `C=empty`, the top-grade label is desired and no `J_empty^top` is nuisance.

### Theorem 1 (complete transverse nuisance decomposition)

For a top-minus-two target `C in binom(Uhat,2)`,

```text
N_C^tr=J_C^top+
 sum_(D in binom(Bhat,2), D!=C) J_(C,D).              (10)
```

For the top target `C=empty`,

```text
N_empty^tr=sum_(D in binom(Bhat,2)) J_(empty,D).       (11)
```

The `D=Q` term is zero in both formulas because `a_Q=P_Q(q)=0`.  Every other
active same-grade label is retained, and the top-grade label is retained
exactly when it is not desired.

#### Proof

The `D` summand of the promoted identity, after residual evaluation, is

```text
g_D(z_Q) tensor id_(V_(Uhat-D_0)^*).                  (12)
```

Applying the transverse operator replaces `g_D` by `a_D`.  Under the target
factorization `Uhat=C disjoint-union S_C`, its fixed coefficient factors in
`D_0` split as `X disjoint-union Y`.  Coefficient slicing over the right
factor contracts every `Y` slot, producing `Slice_Y(a_D)`.  The input identity
on the left slots absent from `D_0` supplies the full tensor factor `V_Z^*`.
All other identity slots are sliced on the right.  Hence the complete
coefficient-slice space of this labelled summand is exactly (8).

The evaluated formal domain is a direct sum of its labelled deck inputs, so
the nuisance of the sum is the sum of their coefficient-slice spaces.  The
top-grade term is `G_empty^A tensor id_(W_Uhat)` after `Q` evaluation.  Since
`epsilon_A(G_empty^A)=0`, its projection is `pG_empty^A`; slicing gives (9) for
a pair target.  For the top target it is the desired label and is omitted.
This proves (10)--(11).  `square`

### Explicit pair-target cases

For `|C|=2`, (8) specializes as follows.

```text
D_0=empty (D=Q):       J_(C,D)=0;
|D_0|=1, D_0 subset C: J_(C,D)=K a_D tensor V_(C-D_0)^*;
|D_0|=1, D_0 disjoint C:
                       J_(C,D)=Slice_(D_0)(a_D) tensor V_C^*;
|D_0|=2, |D_0 intersect C|=1:
                       J_(C,D)=Slice_(D_0-C)(a_D)
                                  tensor V_(C-D_0)^*;
|D_0|=2, D_0 disjoint C:
                       J_(C,D)=Slice_(D_0)(a_D) tensor V_C^*.
                                                               (13)
```

The missing case `D_0=C` is the desired label `D=C` and is not nuisance.

## 3. Disjoint-label collapse

For a pair target define the disjoint root-slice space

```text
R_C^dis=span{
 Slice_(D_0)(a_D):D!=C, D_0 intersect C=empty}
 subset E_A^tr.                                        (14)
```

This includes one-`Q` labels whose single promoted port is outside `C`, and
two-promoted-port labels disjoint from `C`.  The zero `D=Q` term changes
nothing.

### Theorem 2 (exact sufficient collapse criterion)

For every pair target,

```text
R_C^dis tensor V_C^* subset N_C^tr.                   (15)
```

Consequently,

```text
R_C^dis=E_A^tr  implies  N_C^tr=K_C^tr,               (16)
```

so the full legal `GLS8` target class is absorbed.

#### Proof

Every disjoint case in (13) is exactly its root slice tensored with the full
`V_C^*`.  Sum these contributions and use Theorem 1, proving (15).  Equality
in (16) fills the ambient transverse space.  `GLS22` then transfers absorption
back to the full quotient.  `square`

The converse to (16) is not asserted: overlapping labels and the top-anchor
space may fill the quotient even when `R_C^dis` is proper.

For the top target, (11) gives the exact stronger formula

```text
N_empty^tr=span{
 Slice_(D_0)(a_D):D in binom(Bhat,2)} subset E_A^tr.  (17)
```

There are no missing left port factors when `C=empty`.

## 4. Top-anchor dichotomy

Put

```text
omega=G_empty^A=W_(a_0,a_1) in E_A^tr.               (18)
```

The inclusion in `E_A^tr` is the maximum-root condition
`epsilon_A(omega)=0`.

### Theorem 3 (common top-anchor line)

For every top-minus-two target on `D(p)`,

```text
K omega tensor V_C^* subset N_C^tr.                   (19)
```

The top target has transverse desired coefficient

```text
t_empty=p omega.                                      (20)
```

Hence exactly one of the following holds.

#### Z. Zero anchor

`omega=0`.  Then the top target desired coefficient is zero and has no legal
selector.

#### N. Nonzero anchor

`omega!=0`.  Every pair-target legal selector annihilates
`omega tensor V_C^*`, and its selector problem factors exactly through

```text
(E_A^tr/K omega) tensor V_C^*,           dimension 7*9=63. (21)
```

The top target survives exactly when

```text
omega notin N_empty^tr,                               (22)
```

where `N_empty^tr` is the explicit root-slice span (17).

#### Proof

Equation (19) is (9) after using that `p` is a unit.  Equation (20) follows
from `P_Q(omega)=p omega`.  If `omega=0`, the desired coefficient vanishes.
If it is nonzero, (19) is a nuisance submodule, so quotienting it loses no
pair-target selector and reduces the root dimension from eight to seven.
For the top target, `t_empty=p omega` and `p` is a unit; `GLS22` survival is
therefore equivalent to (22).  `square`

### Corollary 3.1 (root-order-three seven-target interface)

At `r=3`, the six promoted pair targets and promoted four-port top target lie
in the exhaustive split:

```text
omega=0:
  the four-port desired coefficient is zero;

omega!=0:
  each pair target has an exact 63-row quotient,
  every pair selector annihilates the common top-anchor line,
  and the four-port target is legal exactly when omega escapes (17). (23)
```

Even in the nonzero branch, the theorem does not force the four-port escape,
any of the six pair escapes, a common seven-row normalization, nonzero physical
responses, or the `GLD3` activity gate.

## 5. Complete-target and failure consequences

The `GLS22` target identity descends through every nuisance subspace displayed
above.  Thus:

- disjoint-root fullness in (16) forces all three transverse pure columns of
  that target into nuisance;
- in branch `omega!=0`, pair-target pure columns may be tested in the exact
  `63`-row quotient without changing selector legality;
- top-target usefulness is exactly (22) together with nonzero physical top
  response; and
- every statement remains pointwise on all residual and nuisance-rank-drop
  fibres.

These are reductions, not witness exclusions.  A nonzero response cannot
repair a full nuisance quotient, and raw `omega!=0` cannot replace top-target
survival modulo (17).

## 6. Proof-DAG consequence and open boundary

The exact promoted path is now

```text
GLS22 transverse 72/8-row quotient
 -> GLS23 label-by-label complete nuisance formula
 -> pair target:
      {disjoint-root full collapse,
       proper disjoint root space plus overlap/top-anchor nuisance}
 -> top target:
      {omega=0 desired-zero,
       omega!=0 and explicit root-slice survival test}.       (24)
```

The next physical obligation is to use complete mixed GHZ equations to
exclude the simultaneous target-specific slice spans which absorb every
required transverse desired tensor, or to prove a useful common family with
all downstream response/activity gates.  Generic full root-slice rank is not
enough; every rank-drop fibre in (10)--(17) remains load-bearing.

The subsequent
[`GLS24` one-probe marginal theorem](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_ONE_PROBE_ANCHOR_MARGINAL_NINE_ROW_REDUCTION_AND_DOUBLE_TRANSVERSE_BOUNDARY_THEOREM.md)
refines the nonzero-anchor branch.  A nonzero actual-root marginal gives one
common denominator-free nine-row factor-through test for every pair target;
the zero-marginal divisor is retained as a nonzero double-transverse core.
That refinement does not make nine-row failure equivalent to full absorption.

The following remain **OPEN**:

```text
exclusion of disjoint/overlap transverse absorption:        OPEN;
top-anchor nonzero survival modulo root slices:              OPEN;
pair-target survival and nonzero responses:                  OPEN;
r=3 common seven-row normalization and activity:             OPEN;
r>=4 named promoted downstream detector:                    OPEN;
strategic-node closure:                                     OPEN.
```

The global Krenn--Gu conjecture remains **UNRESOLVED**.

## 7. Verification

Run the focused exact primary verifier:

```bash
python claims/arbitrary-order/verify_maximal_root_surplus_two_promoted_transverse_complete_nuisance_decomposition_and_top_anchor_dichotomy.py
```

Run the independent no-import audit:

```bash
python claims/arbitrary-order/audit_maximal_root_surplus_two_promoted_transverse_complete_nuisance_decomposition_and_top_anchor_dichotomy.py
```

The scripts replay every intersection pattern in (13), exact identity slicing,
the disjoint-root collapse, top-anchor quotient dimensions, and small-root
target counts.  The arbitrary-root proof is the written labelled-operator
argument above.
