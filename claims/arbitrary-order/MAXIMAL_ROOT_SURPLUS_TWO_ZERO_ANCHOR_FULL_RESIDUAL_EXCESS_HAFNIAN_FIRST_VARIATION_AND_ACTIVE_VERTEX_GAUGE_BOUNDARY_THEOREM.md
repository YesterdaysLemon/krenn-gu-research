# Maximum-root surplus-two zero-anchor full-residual excess hafnian first variation and active vertex-gauge boundary theorem

## Status and scope

**Exact characteristic-zero arbitrary-root identity and exact physical
sharpness boundary.**  Fix a `GLS8` promoted chart with open probe roots
`A={a_0,a_1}` and even complementary label set

```text
Bhat=Q disjoint-union Uhat.
```

On the zero-anchor branch, every constant probe-root row annihilating the
three pure diagonal tensors turns the complete open-`A` GHZ equation into a
one-edge first variation of the internal hafnian on `Bhat`.  This identity is
valid before a residual contraction and on every residual/rank/divisor
fibre.  It has a denominator-free vertex recurrence.

The first variation contains an exact trace-zero vertex-gauge family.  A
rational eight-vertex physical graph, with six complementary labels in
`Bhat`, realizes one nonzero `GLS40` excess row as such a gauge.  The same
graph has rank-six full swallow; nonzero tensors `H_Q` and `Pi_Q`; the value
`p(z_Q)=2` at the chosen fully supported contraction; the original root-root
orthogonality; and four nonzero labelled deletion decks detected by that row.
Two are promoted-pair response decks and two are one-`Q` nuisance-label decks.
Their full first variation cancels.  The graph fails another displayed
open-`A` GHZ coefficient, so it is neither a hypothetical witness nor a
counterexample.

This is `GLS42`.  It proves that one selected excess equation, even together
with the listed source data and the four detected nonzero decks on the same
physical graph, does not by itself force a contradiction.  It does not itself
supply or decide `GLS41` pure-core survival.  It also does **not** classify the
whole first-variation kernel, show that every excess direction is a gauge,
satisfy the complete GHZ equations, prove `GLS8` eligibility, force a useful
target, synchronize responses, supply a downstream receiver, cover `p=0`, or
close the strategic node.  The global Krenn--Gu conjecture remains
**UNRESOLVED**.

## Dependencies and provenance

The owning interfaces are:

- [`GLS8`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_TWO_PROBE_ONE_TARGET_ATTACHMENT_AND_POINTWISE_FAILURE_REDUCTION_THEOREM.md)
  for the complete open-`A` companion expansion, `H_Q`, `Pi_Q`, and the
  promoted source typing;
- [`GLS22`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_ALL_PORT_TRANSVERSE_QUOTIENT_AND_PROJECTIVE_SYNCHRONIZATION_FAILURE_THEOREM.md)
  and [`GLS23`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_TRANSVERSE_COMPLETE_NUISANCE_DECOMPOSITION_AND_TOP_ANCHOR_DICHOTOMY_THEOREM.md)
  for the transverse target and labelled physical response interfaces;
- [`GLS36`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_INCIDENCE_IMAGE_COMMON_ROW_SILENCE_AND_LABELWISE_LIFT_SHARPNESS_THEOREM.md)
  for the fixed-residual incidence/deck map; and
- [`GLS40`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_FULL_SWALLOW_AGGREGATE_DECK_EXCESS_SYZYGY_AND_TRANSVERSE_CYLINDER_THEOREM.md)
  and [`GLS41`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_FULL_SWALLOW_PURE_CORE_EXCESS_RESPONSE_DICHOTOMY_AND_ALL_RANK_INTERSECTION_THEOREM.md)
  for the excess module and the remaining pure-core attachment obligation.

No external literature claim is used.  The new content is the full-residual
first-variation identity, its recurrence, the exact trace-zero vertex-gauge
family contained in its kernel, and the source-retyped active physical
boundary.

## 1. The complete excess first variation

Let `K` be a characteristic-zero field.  For every even
`I subseteq Bhat`, let

```text
H_I(W)=sum_(M a perfect matching of I) tensor_(D in M) W_D,
H_empty(W)=1,                                         (1)
```

be the physical principal hafnian tensor of the internal edge array `W`.
For every pair `D={s,t} subseteq Bhat`, the promoted root companion is

```text
G_D^A=X_s tensor Y_t+X_t tensor Y_s.                  (2)
```

Retain

```text
E_A^*=V_(a_0)^* tensor V_(a_1)^*,
Delta=span{r_0,r_1,r_2},
omega=G_empty^A=W_(a_0,a_1).                         (3)
```

Choose one **constant** row

```text
lambda in Ann(Delta) subset (E_A^*)^*
```

and define the physical edge tensor

```text
Theta_D^lambda=(lambda tensor id_(V_D^*))G_D^A
              in V_D^*.                              (4)
```

For even `I`, put

```text
F_I^lambda(W)=sum_(D in binom(I,2))
                 Theta_D^lambda tensor H_(I-D)(W).   (5)
```

All tensor products in (1) and (5) use disjoint labelled vertex factors, so
no ordering or symmetrization ambiguity is hidden.

### Theorem 1 (full-residual excess equation)

On the zero-anchor branch `omega=0`, the complete open-`A` GHZ equation
implies the tensor identity

```text
F_Bhat^lambda(W)=0.                                  (6)
```

This holds before evaluating either residual label.  Therefore it holds
after every residual contraction, including every exceptional rank or
divisor fibre.  No response, incidence factor, or minor is divided out.

#### Proof

The exact `GLS8` open-`A` expansion is

```text
T_W=sum_(D in binom(Bhat,2))
        G_D^A tensor H_(Bhat-D)+omega tensor H_Bhat. (7)
```

The probe-root factor of the ternary GHZ target `T_W` lies in `Delta`.
Apply `lambda` to that factor.  It kills the target by
`lambda(Delta)=0`, kills the final term by `omega=0`, and turns every pair
term into (4).  The result is exactly (6). `square`

The row may be chosen after fixing a residual point and then held constant.
In particular, on a `GLS40` full-swallow point put

```text
q=G_Q^A(z_Q),                 S=Delta+Kq,
lambda in Ann(S),             theta=sigma_Q^*(lambda). (8)
```

Evaluating (6) at `z_Q` gives

```text
F_Bhat^lambda(z_Q,-)=theta compose rho_Q=0,           (9)
```

because the `D=Q` term is `lambda(q)H_Uhat=0` and the other terms are
exactly the labelled `GLS36` deck insertion.  Thus the `GLS40` excess
syzygy is the fixed-residual shadow of (6), not a second independent
equation.

## 2. Coefficient and recurrence identities

Introduce a central scalar indeterminate `t` and replace every internal edge
by `W_D+t Theta_D^lambda`.

### Theorem 2 (hafnian coefficient and vertex recurrence)

For every even `I subseteq Bhat`,

```text
F_I^lambda(W)=[t]H_I(W+tTheta^lambda).               (10)
```

For every `u in I`, it also obeys the denominator-free recurrence

```text
F_I^lambda
 =sum_(v in I-{u}) [
     Theta_(u,v)^lambda tensor H_(I-{u,v})
    +W_(u,v) tensor F_(I-{u,v})^lambda].             (11)
```

#### Proof

In the product belonging to one perfect matching, the coefficient of `t`
is the sum obtained by selecting `Theta` on exactly one matched edge and
`W` on every other edge.  Summing over matchings proves (10).  Partition
those pointed matchings by the unique partner `v` of `u`.  If the pointed
edge is `{u,v}`, the first term of (11) results; otherwise `{u,v}` supplies
`W_(u,v)` and the pointed edge lies in the complementary matching, giving
the second term. `square`

## 3. Exact trace-zero vertex-gauge family in the kernel

Let `(a_s)_(s in I)` be scalars.  Suppose the physical tensors obey

```text
Theta_(s,t)^lambda=(a_s+a_t)W_(s,t)
for every pair {s,t} subseteq I.                     (12)
```

### Theorem 3 (vertex-gauge formula)

Under (12),

```text
F_I^lambda=(sum_(s in I)a_s)H_I.                    (13)
```

Consequently every trace-zero gauge,

```text
sum_(s in I)a_s=0,                                   (14)
```

lies in the kernel of the complete first variation, independently of
whether `H_I` or the individual deletion responses vanish.  No equality with
or classification of the full kernel is asserted.

#### Proof

Fix a perfect matching `M` of `I`.  Its contribution to (5) is its `W`
monomial multiplied by

```text
sum_({s,t} in M)(a_s+a_t)=sum_(s in I)a_s,
```

because every vertex occurs exactly once.  Sum over all `M`. `square`

Equation (13) is the tangent of vertex rescaling
`W_(s,t) -> z_s z_t W_(s,t)`.  Only the elementary matching proof above is
used; no generic smoothness or hafnian-variety theorem is invoked.

## 4. A source-retyped active physical boundary

Work over `K=Q`, take

```text
Bhat=(q_0,u_0,q_1,u_1,u_2,u_3),
Q={q_0,q_1},          K_0={u_0},
U={u_1,u_2,u_3},      Uhat=K_0 disjoint-union U.     (15)
```

All six label spaces and both probe-root spaces are ternary.  Write `P_c`
for the diagonal coordinate projector onto colour `c`.  Set equal root-leg
maps `X_t=Y_t=M_t` with

```text
M_(q_0)=P_0,          M_(q_1)=P_1,
M_(u_0)=P_0-P_1,      M_(u_1)=P_1,
M_(u_2)=M_(u_3)=P_2.                                (16)
```

The residual and maximum-root vectors are the fully supported all-ones
vectors.  Let `x_(t,c)` denote the coordinate functional at label `t`.
Every nonzero internal edge below is the displayed rational scalar times
`x_(s,c_s)x_(t,c_t)` with

```text
c_(q_0)=c_(u_0)=0,
c_(q_1)=c_(u_1)=1,
c_(u_2)=c_(u_3)=2:

W_(q_0,u_2)=1,       W_(q_0,u_3)=-1/3,
W_(u_0,u_2)=1/3,     W_(u_0,u_3)=-1,
W_(q_1,u_1)=1,       W_(u_0,u_1)=1,
W_(u_2,u_3)=1,       W_(q_0,q_1)=1.                 (17)
```

Every other internal edge is zero, and `W_(a_0,a_1)=0`.  Let

```text
lambda=E_02^*,
(a_(q_0),a_(u_0),a_(q_1),a_(u_1),a_(u_2),a_(u_3))
 =(-1,1,1,-1,2,-2).                                 (18)
```

Here `E_02^*` extracts the `(0,2)` probe-root matrix coordinate.

### Theorem 4 (active gauge cancellation with source data)

The graph (15)--(18) has the following exact properties.

1. Excluding the pair `Q`, the incidence map has

   ```text
   B=im sigma_Q=Sym_3,           dim B=6,
   q=E_01+E_10,
   S=Delta+Kq,                   dim S=4.             (19)
   ```

   Thus it is a rank-six full-swallow point, and `lambda in Ann(S)` gives a
   nonzero `GLS40` excess row.

2. `lambda` detects exactly the four pairs joining
   `{q_0,u_0}` to `{u_2,u_3}`.  Tensorwise on every pair of `Bhat`,

   ```text
   Theta_(s,t)^lambda=(a_s+a_t)W_(s,t),
   sum_(s in Bhat)a_s=0.                             (20)
   ```

   Hence `F_Bhat^lambda=0` by Theorem 3.

3. After factoring the common labelled coordinate monomial, the principal
   hafnians and the four detected labelled deletion decks are

   ```text
   H_Q=1,             H_Uhat=1,
   H_Bhat=-1/9,

   H_(Bhat-{u_0,u_3})=1,
   H_(Bhat-{u_0,u_2})=-1/3,
   H_(Bhat-{q_0,u_3})=1/3,
   H_(Bhat-{q_0,u_2})=-1.                            (21)
   ```

   The first two displayed deletions are promoted-pair physical response
   decks.  The last two are one-`Q` nuisance-label decks.  Every term detected
   by the selected excess row has a nonzero physical deck, but this is not the
   complete selected-response activity gate of any downstream theorem.  The
   four signed first-variation terms sum to zero.

4. Evaluation at the two all-ones probe-root vectors gives

   ```text
   p=epsilon_A(q)=2.                                 (22)
   ```

   The original three roots are `A disjoint-union K_0`.  Their root-root
   edges obey maximum-root orthogonality: the `A`--`A` edge is zero and each
   `A`--`u_0` edge evaluates as

   ```text
   1^T(P_0-P_1)1=0.                                 (23)
   ```

   The `r=3` source Laplace permanent is

   ```text
   Pi_Q=2(-1+1/3+1)
          x_(u_1,1)x_(u_2,2)x_(u_3,2)
       =(2/3)x_(u_1,1)x_(u_2,2)x_(u_3,2)!=0.         (24)
   ```

5. The graph is not a GHZ witness.  For the row `lambda_01=E_01^*`, which
   also annihilates `Delta`, the `q_0q_1` and `u_0u_1` matching cofactors
   each contribute the same nonzero labelled word.  The orthogonality
   correction `-P_1` in `M_(u_0)` contributes a second word through the
   `q_0u_0` pair.  Therefore

   ```text
   F_Bhat^(lambda_01)
    =2x_(q_0,0)x_(u_0,0)x_(q_1,1)x_(u_1,1)
       x_(u_2,2)x_(u_3,2)
     -x_(q_0,0)x_(u_0,1)x_(q_1,1)x_(u_1,1)
       x_(u_2,2)x_(u_3,2)
    !=0.                                             (25)
   ```

   This violates Theorem 1's necessary open-`A` GHZ coefficient.

#### Proof

The images in (16) contain all three coordinate lines.  Pairing the lines
through the non-`Q` labels produces all three diagonal and all three
symmetric off-diagonal matrices, proving (19).  Evaluation of `Q` gives the
displayed `q`.  The row `E_02^*` kills the diagonal and `(0,1)` directions
and is nonzero on `B`, so it represents an excess class.

The correction `-P_1` in `M_(u_0)` has no `(0,2)` output.  Thus `lambda`
sees exactly the four coordinate monomials asserted in item 2.  Substitution
of (17)--(18) proves (20) edge by edge.  The matching recurrence gives
(21), and the four detected deletion values sum as

```text
1-1/3+1/3-1=0.
```

Equations (22)--(23) are direct evaluations.  In (24), choosing the two
`A`-assigned ports leaves respectively the `u_0u_3`, `u_0u_2`, and
`u_0u_1` edges; each two-root coefficient evaluates to `2`.  Finally, direct
matching expansion in the `(0,1)` root coordinate gives the two distinct
words in (25), so they cannot cancel. `square`

The repair `M_(u_0)=P_0-P_1` is load-bearing.  The tempting all-projector
choice `M_(u_0)=P_0` retains the same gauge arithmetic but violates the
original root-root orthogonality because `1^T P_0 1=1`.

## 5. Frontier and unresolved remainder

```text
full-residual excess first-variation identity:           PROVED;
denominator-free pointed-hafnian recurrence:              PROVED;
trace-zero vertex-gauge family lies in the kernel:        PROVED;
rank-six selected gauge with four detected nonzero decks: PROVED;
same-graph H_Q, Pi_Q, p and root orthogonality:            PROVED;
control satisfies complete GHZ equations:                 FALSE;
every excess direction is a vertex gauge:                 NOT CLAIMED;
full first-variation kernel classified:                    NOT CLAIMED;
pure-core survival / useful response:                     OPEN;
synchronization / activity / downstream attachment:       OPEN;
p=0 and raw-escape source coverage:                       OPEN;
strategic-node closure:                                   OPEN;
global Krenn--Gu conjecture:                              UNRESOLVED.
```

The smallest remaining `D(p)` obligation is still the `GLS41` pure-core
intersection escape: force, on one eligible same-graph point,

```text
im D_C^tr not subset N_C^tr intersect R_C^pure
```

for some promoted pair `C`, or contradict all simultaneous containments by
using additional GHZ coefficients and their coupling.  Theorem 4 shows only
that the selected excess equation and its four detected nonzero decks do not
by themselves contradict the displayed physical graph; pure-core containment
for that graph was not audited.  A positive continuation must couple
different root rows/targets or use a nonlinear principal-deck relation, while
retaining every response, synchronization, activity, nuisance, source, and
receiver gate.

## Verification boundary

Run the focused exact primary verifier:

```text
uv run --with sympy python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_full_residual_excess_hafnian_first_variation_and_active_vertex_gauge_boundary.py
```

Run the genuinely independent no-import audit:

```text
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_full_residual_excess_hafnian_first_variation_and_active_vertex_gauge_boundary.py
```

The primary uses SymPy to replay the formal first-variation coefficient and
recurrence, the rank-six incidence/full-swallow data, the tensorwise gauge,
all hafnian/deletion values, root orthogonality, `p`, `Pi_Q`, and the explicit
failed `(0,1)` GHZ coefficient.  The audit imports no project module or
third-party package; it uses an independent polynomial matching expansion,
fractional elimination, and separately entered sparse tensors.  The
arbitrary-root statements are the written matching proofs above, not a
bounded computation.
