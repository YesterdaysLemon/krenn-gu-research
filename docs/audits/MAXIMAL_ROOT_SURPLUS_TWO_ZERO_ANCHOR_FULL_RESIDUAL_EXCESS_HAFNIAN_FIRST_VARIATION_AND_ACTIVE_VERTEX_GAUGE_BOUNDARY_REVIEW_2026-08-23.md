# Hostile review: zero-anchor full-residual excess hafnian first variation and active vertex-gauge boundary

## Verdict

**ACCEPT after mathematical, owning-interface, physical-fixture,
independence, and scope audit.**  On the zero-anchor branch, applying a
constant probe-root row in `Ann(Delta)` to the complete open-`A` GHZ equation
gives the exact one-edge first variation of the internal principal hafnian on
the entire complementary label set.  This is an uncontracted tensor identity,
so every residual contraction and exceptional fibre is retained.

The first variation has an exact pointed-matching recurrence.  Tensorwise
vertex gauges satisfy `F_I=(sum_s a_s)H_I`, so every trace-zero vertex gauge
lies in the kernel.  This is a contained family, not a classification of the
whole kernel.

An exact eight-vertex physical control with six complementary labels realizes
one selected nonzero `GLS40` excess row as a trace-zero gauge.  It retains
rank-six full swallow, nonzero tensors `H_Q` and `Pi_Q`, `p(z_Q)=2` at the
chosen fully supported contraction, the original three-root root-root
orthogonality, and four nonzero labelled deletion decks.  Two are
promoted-pair response decks and two are one-`Q` nuisance-label decks.  A
different root row fails an exact GHZ coefficient, so the graph is not a
hypothetical witness or a counterexample.

The selected excess equation and these four detected decks therefore do not
by themselves contradict a physical graph.  Pure-core containment for the
control was not computed, and the theorem does not force or refute `GLS41`
pure-core survival.  Complete `GLS8` eligibility, synchronization, downstream
selected-response activity, nuisance survival, a named receiver, `p=0`
coverage, raw escape, and node closure remain open.  The global Krenn--Gu
conjecture remains **UNRESOLVED**.

## Reviewed artifacts

- [`GLS42 theorem`](../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_FULL_RESIDUAL_EXCESS_HAFNIAN_FIRST_VARIATION_AND_ACTIVE_VERTEX_GAUGE_BOUNDARY_THEOREM.md)
- [`focused primary verifier`](../../claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_full_residual_excess_hafnian_first_variation_and_active_vertex_gauge_boundary.py)
- [`independent no-import audit`](../../claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_full_residual_excess_hafnian_first_variation_and_active_vertex_gauge_boundary.py)
- owning interfaces `GLS8`, `GLS22`, `GLS23`, `GLS36`, `GLS40`, and `GLS41`
- the `GLS42` current-frontier, supply/target DAG, and arbitrary-order README
  entries.

Three read-only hostile passes checked the tranche.  One reviewer rederived
the arbitrary-root matching identities and audited the logical no-go scope;
one checked the complete source/target typing against every owning interface;
and one separately rederived the repaired rational graph, including tensor
orientations and source retyping.  Genuine implementation independence is
provided by the separately entered no-import audit, not merely by review
labels.

## Complete first-variation audit

The exact `GLS8` open-`A` identity is

```text
T_W=sum_(D in binom(Bhat,2))
      G_D^A tensor H_(Bhat-D)+omega tensor H_Bhat.    (1)
```

The ternary GHZ target has probe-root factor in

```text
Delta=span{r_0,r_1,r_2}.                              (2)
```

For a constant `lambda in Ann(Delta)`, define

```text
Theta_D^lambda=(lambda tensor id)G_D^A,
F_I^lambda=sum_(D in binom(I,2))
              Theta_D^lambda tensor H_(I-D).         (3)
```

On the declared zero-anchor branch `omega=0`, applying `lambda` to (1)
kills both the target and the top term, yielding

```text
F_Bhat^lambda=0.                                     (4)
```

Nothing has been evaluated or divided in this derivation.  Thus (4) holds
before residual contraction and remains valid after every contraction,
including rank-drop and divisor fibres.  The row is constant in the
probe-root coefficient space; it is not a residual-dependent selector being
silently differentiated.

At a fixed `GLS40` full-swallow point, choose

```text
S=Delta+Kq,                 lambda in Ann(S),
theta=sigma_Q^*(lambda).                              (5)
```

After evaluating the residual pair, the `D=Q` term of (4) is
`lambda(q)H_Uhat=0`.  Every other term is the corresponding labelled
incidence row times its complementary physical deck.  Therefore

```text
F_Bhat^lambda(z_Q,-)=theta compose rho_Q=0.           (6)
```

This verifies the interface correction: the `GLS40` fixed-point excess
syzygy is the shadow of the complete equation, not an independent extra row.

## Matching coefficient and recurrence audit

For central `t`, the coefficient of `t` in one matching monomial of
`H_I(W+tTheta)` selects exactly one `Theta` edge and leaves `W` on every
other edge.  Summing over matchings gives

```text
F_I=[t]H_I(W+tTheta).                                 (7)
```

Partitioning pointed matchings by the unique partner `v` of a fixed vertex
`u` gives

```text
F_I=sum_(v in I-{u})[
      Theta_(u,v)H_(I-{u,v})+W_(u,v)F_(I-{u,v})].    (8)
```

Both formulas are polynomial and denominator-free.  They use only disjoint
labelled tensor factors, so no implicit ordering convention changes a sign or
multiplicity.

If

```text
Theta_(s,t)=(a_s+a_t)W_(s,t),                         (9)
```

then each matching monomial is multiplied in the first variation by

```text
sum_({s,t} in M)(a_s+a_t)=sum_(s in I)a_s.            (10)
```

Hence

```text
F_I=(sum_(s in I)a_s)H_I.                            (11)
```

Trace-zero vertex gauges are therefore contained in the kernel.  Review
required the theorem and frontier to say **contained in**, not to call this
the whole or exact kernel.

## Physical control audit

The complementary labels are

```text
Bhat=(q_0,u_0,q_1,u_1,u_2,u_3),
Q={q_0,q_1},        K_0={u_0},       U={u_1,u_2,u_3}.
```

Together with the two open probe roots this is an eight-vertex physical
graph.  Its equal root-leg maps are

```text
M_(q_0)=P_0,        M_(q_1)=P_1,
M_(u_0)=P_0-P_1,    M_(u_1)=P_1,
M_(u_2)=M_(u_3)=P_2.                                (12)
```

The correction `-P_1` is necessary.  With all maximum-root vectors equal to
the fully supported all-ones vector,

```text
1^T(P_0-P_1)1=0,                                    (13)
```

so both `A`--`u_0` root-root edges obey the original orthogonality equation;
the `A`--`A` edge is zero.  The tempting `P_0` map would give `1`, not zero.

Excluding `Q`, the pair-incidence columns span exactly `Sym_3`, of rank six.
The fixed residual companion is

```text
q=E_01+E_10,
S=Delta+Kq,               dim S=4.                   (14)
```

Thus the control is full swallow.  The row `lambda=E_02^*` annihilates `S`
and is nonzero on the incidence image, so it represents a nonzero excess
class.

The internal scalar weights, after factoring their declared coordinate
monomials, are

```text
q_0u_2=1,       q_0u_3=-1/3,
u_0u_2=1/3,     u_0u_3=-1,
q_1u_1=1,       u_0u_1=1,
u_2u_3=1,       q_0q_1=1.                            (15)
```

For vertex weights

```text
(-1,1,1,-1,2,-2),                                    (16)
```

in the displayed label order, exact tensor comparison on all fifteen pairs
gives (9), and the vertex-weight sum is zero.  The selected first variation
therefore vanishes.

Independent matching expansion gives

```text
H_Q=1,               H_Uhat=1,       H_Bhat=-1/9,

H_(Bhat-{u_0,u_3})=1,
H_(Bhat-{u_0,u_2})=-1/3,
H_(Bhat-{q_0,u_3})=1/3,
H_(Bhat-{q_0,u_2})=-1.                               (17)
```

The first two deletions in (17) are promoted-pair response decks.  The last
two have one residual label in the deleted pair and are nuisance-label decks.
All four are nonzero, but this is not the complete downstream
selected-response activity gate.

At the chosen residual contraction,

```text
p(z_Q)=epsilon_A(q)=2.                               (18)
```

The literal three-root source Laplace expansion gives

```text
Pi_Q=2(-1+1/3+1)
      x_(u_1,1)x_(u_2,2)x_(u_3,2)
    =(2/3)x_(u_1,1)x_(u_2,2)x_(u_3,2)!=0.            (19)
```

Thus `H_Q` and `Pi_Q` are nonzero tensors and the displayed point has
`p(z_Q)!=0`.  These source data and root orthogonality do not make the graph a
complete `GLS8`-eligible maximum-root source point.

## Explicit non-witness audit

For `lambda_01=E_01^*`, exact sparse matching expansion gives two distinct
labelled words:

```text
F_Bhat^(lambda_01)
 =2x_(q_0,0)x_(u_0,0)x_(q_1,1)x_(u_1,1)
    x_(u_2,2)x_(u_3,2)
  -x_(q_0,0)x_(u_0,1)x_(q_1,1)x_(u_1,1)
    x_(u_2,2)x_(u_3,2)
 !=0.                                                (20)
```

The second word is produced by the load-bearing `-P_1` orthogonality repair;
an earlier draft omitted it.  The primary and independent audit both caught
that omission before publication.  Since `lambda_01` also annihilates
`Delta`, (20) violates the necessary complete equation (4).  The graph is
therefore explicitly not a witness.  No global counterexample or theorem
contradiction is present.

## Corrections required by hostile review

The review required and verified these publication corrections:

1. include the extra `(0,1)` word introduced by `P_0-P_1`;
2. state that trace-zero gauges form a family **inside** the kernel, without
   claiming full-kernel equality or classification;
3. call the control an eight-vertex graph with six complementary labels;
4. distinguish the two promoted-pair response decks from the two one-`Q`
   nuisance-label decks and disclaim downstream activity;
5. type `H_Q` and `Pi_Q` as nonzero tensors and `p(z_Q)=2` as the value at one
   contraction;
6. retain the explicit nonclaim of complete `GLS8` eligibility; and
7. narrow the no-go conclusion to consistency/no contradiction from the
   selected excess equation and its four detected decks.  Pure-core
   containment for the control was not audited.

All corrections are present in the accepted artifacts.

## Exact computational audits

The SymPy primary verifies the formal coefficient identity, pivot recurrence,
and gauge formula symbolically on six labels.  It independently builds the
`9`-row incidence matrix, proves ranks `6/4`, checks all fifteen tensorwise
gauge equations, computes every displayed principal/deletion hafnian, checks
orthogonality, `p`, and `Pi_Q`, and obtains both words of the failed `(0,1)`
coefficient.

The no-import audit uses only the Python standard library.  It derives the
coefficient and recurrence from explicit eight-label perfect matchings and
coefficient arrays, uses independent `Fraction` elimination for the
incidence ranks, and separately enters sparse labelled-coordinate tensors for
the physical graph.  It imports neither the primary verifier nor repository
mathematics code.

## Verification replay

The following pass on the candidate tree:

```text
uv run --with sympy python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_full_residual_excess_hafnian_first_variation_and_active_vertex_gauge_boundary.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_full_residual_excess_hafnian_first_variation_and_active_vertex_gauge_boundary.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_promoted_two_probe_one_target_attachment_and_pointwise_failure_reduction.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_promoted_two_probe_one_target_attachment_and_pointwise_failure_reduction.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_promoted_all_port_transverse_quotient_and_projective_synchronization_failure.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_promoted_all_port_transverse_quotient_and_projective_synchronization_failure.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_promoted_transverse_complete_nuisance_decomposition_and_top_anchor_dichotomy.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_promoted_transverse_complete_nuisance_decomposition_and_top_anchor_dichotomy.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_incidence_image_common_row_silence_and_labelwise_lift_sharpness.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_incidence_image_common_row_silence_and_labelwise_lift_sharpness.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_full_swallow_aggregate_deck_excess_syzygy_and_transverse_cylinder.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_full_swallow_aggregate_deck_excess_syzygy_and_transverse_cylinder.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_full_swallow_pure_core_excess_response_dichotomy_and_all_rank_intersection.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_full_swallow_pure_core_excess_response_dichotomy_and_all_rank_intersection.py
```

The focused scripts, Ruff, compilation, and all six owning primary/audit
pairs pass.  Candidate-tree hygiene compiles `2308` Python files and resolves
all links in `1441` Markdown files.  The mandatory unit suites pass `191+14`
tests, and link rewriting is idempotent with zero changes.  Exact-head hosted
CI and merged-main replay remain publication gates to be recorded before and
after merge.

## Unresolved boundary

At one common contraction retaining `H_Q(z_Q)p(z_Q)!=0`, force

```text
im D_C^tr not subset N_C^tr intersect R_C^pure       (21)
```

for one eligible promoted pair, or contradict all simultaneous containments
with additional complete same-graph GHZ rows/targets and principal-deck
compatibility.  The selected excess first variation and its four detected
nonzero decks do not alone supply (21), and pure-core containment in the
control is undecided.  Any rank rise still needs response synchronization,
selected activity, every additional/common nuisance gate, and a named
receiver.  The zero-anchor top target is dead.  Silent `p=0` source coverage
and raw escape remain separate.
