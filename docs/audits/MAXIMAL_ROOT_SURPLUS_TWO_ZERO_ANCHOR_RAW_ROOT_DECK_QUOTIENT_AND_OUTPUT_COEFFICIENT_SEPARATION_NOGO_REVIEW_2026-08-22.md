# GLS35 raw root-deck quotient and output/coefficient separation no-go review

## Review status and provenance

Date: 2026-08-22.

Base: `origin/main` at
`dfe2693d4fe4dfc5bf01662294dd7baff4439724`, the post-GLS34 merge.

Candidate branch:
`codex/kg-gls35-coefficient-anchor-bridge-20260822`.

Reviewed artifacts:

- [`GLS35 theorem`](../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_RAW_ROOT_DECK_QUOTIENT_AND_OUTPUT_COEFFICIENT_SEPARATION_NO_GO_THEOREM.md);
- [`focused exact primary verifier`](../../claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_raw_root_deck_quotient_and_output_coefficient_separation_nogo.py);
- [`independent no-import audit`](../../claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_raw_root_deck_quotient_and_output_coefficient_separation_nogo.py);
- the `GLS8`, `GLS21`--`GLS23`, `GLS33`--`GLS34`, and `GLD3` owning
  interfaces; and
- the README, current-frontier, and maximum-root node-DAG updates.

Three bounded read-only attacks were completed before publication:

1. an owning-interface reconstruction of the raw and transverse source/target
   maps;
2. an exact physical countermodel search against the proposed output-to-
   coefficient implication; and
3. an independent tangent-root/Segre coupling analysis.

A separate hostile reviewer then re-derived the theorem and control from the
candidate files.  The initial hostile verdict found one provenance blocker:
the theorem's load-bearing correction distinguishing `H_Uhat=C(B)` from
`GLD3`'s residual-present `T` did not list the owning `GLD3` document as a
dependency.  The dependency and its defining equations are now cited
explicitly.  After that correction, the hostile verdict is **ACCEPT at the
exact scope below**.

## 1. Owning-interface audit

The raw promoted identity has labelled coefficients

```text
G_D^A tensor H_(Bhat-D),       D in binom(Bhat,2),
G_empty^A tensor H_Bhat.
```

At a fixed residual contraction, the `D=Q` coefficient is

```text
q=G_Q^A(z_Q) in E_A^*.
```

When this one label is re-labelled desired, every other coefficient slice is
nuisance.  Therefore the unique complete raw module is

```text
B_Q^anc=K omega
 +sum_(D!=Q) Slice_(D intersect Uhat)(g_D(z_Q)).       (1)
```

The review checked that `K omega` is mandatory: `D=empty` is not the desired
label in this re-labelled problem.  On the zero-anchor branch it is zero, but
omitting it from the definition would change the module outside that branch.

The review also confirmed the interface correction:

- in every original promoted target, `q` is the retained `GLS21` nuisance;
- `GLS22` has `P_Q(q)=0`;
- on `omega=0`, applying `P_Q` label by label gives exactly
  `P_Q(B_Q^anc)=N_empty^tr`; and
- `q notin B_Q^anc` is therefore raw extension data erased by the transverse
  quotient, not `GLS22/GLS23` desired-target survival.

## 2. Quotient theorem audit

Finite-dimensional separation proves

```text
q notin B_Q^anc
 iff exists lambda with lambda(B_Q^anc)=0 and lambda(q)=p. (2)
```

Because the formal deck labels are a direct sum, this functional isolates
exactly the residual-absent label `H_Uhat`.

Modulo (1), the complete target equation is

```text
[q] tensor H_Uhat
 =sum_c alpha_c [r_c] tensor e_c^(tensor |Uhat|).     (3)
```

The three pure port words are independent and every `alpha_c` is a residual-
torus unit.  On the `GLS34` non-silent gate, `H_Uhat!=0`.  Hence:

- if `[q]!=0`, (3) has tensor rank one, the three `[r_c]` span `K[q]`, and
  the normalized functional makes `H_Uhat` nonzero pure diagonal;
- if `[q]=0`, coefficient comparison forces all three `r_c` into
  `B_Q^anc`.

The split is exhaustive.  The all-rank presentation

```text
rank[B_Q|q]=rank B_Q       or       rank B_Q+1         (4)
```

retains every nuisance-rank fibre and introduces no chosen-minor denominator.

## 3. Independent physical-control audit

Both exact implementations rebuild the rational graph from literal matrices.
They agree on:

```text
det W_0=det W_1=-1,
p=2,
K_u^00=K e_0                 for all four ports,
rank B_Q^anc=rank[B_Q^anc|q]=8,
rank P_Q(B_Q^anc)=7.                              (5)
```

For `v=e_1+e_2`, direct multiplication gives

```text
W_0v=e_2,       W_1v=e_1,

Slice_v(g_(q_0,u))
 =e_1 tensor e_1+e_2 tensor e_2=q.                   (6)
```

Thus one labelled one-`Q` slice swallows `q` exactly.

The four-port deck has

```text
H_Uhat(e_0,e_0,e_0,e_0)=1/2,
pH_Uhat(e_0,e_0,e_0,e_0)=1,

pH_Uhat(e_0,e_0,e_0,-)=e_0^* mod span{e_1^*,e_2^*}  (7)
```

at every free port.  All eight relevant one-`Q` singleton decks vanish, so
the singleton identities hold literally.  The target diagonal with
`delta=(1,1,1)` has the same all-port value one.  Therefore the complete
product-kernel conclusion and all four nonzero singleton output classes do
not force (2).

The primary verifier uses SymPy matrices, full raw slice generation, direct
rational ranks, and recursive perfect matchings.  The independent audit
imports no repository code or third-party algebra package; it uses `Fraction`
tuples, a separately written row reduction, and a bitmask matching recurrence.
They are independent in representation, elimination, and graph evaluation.

The full graph has pure coefficients `(0,0,0)`.  The review therefore rejects
any interpretation of the control as pure-normalized, a hypothetical witness,
or a conjecture counterexample.

## 4. Downstream type audit

At root order three, the selected deck is

```text
H_Uhat=C(B),                                           (8)
```

the residual-absent four-port matching compound.  `GLD3` instead defines

```text
T=z_1234=H_(Q union Uhat)
 =hC(B)+cross terms,                                  (9)
```

the residual-present four-port response.  In the promoted source identity,
that response belongs to `D=empty` and has coefficient `omega`, which is zero
on the present branch.  Consequently GLS35 supplies neither `GLD3`'s `T` nor
any original pair target/response.  No named downstream theorem accepts the
isolated `H_Uhat` alone.

## 5. Hostile scope verdict

Accepted:

- the exact raw module (1), including `K omega`;
- the selector equivalence and complete-target quotient (2)--(3);
- the exhaustive escape/swallow split and all-rank profile;
- the two independent exact replays of (5)--(7);
- the refutation of output survival alone as a route to coefficient
  separation; and
- the correction distinguishing the raw residual-absent selector from
  `GLS22/GLS23` target survival and `GLD3` attachment.

Not accepted or claimed:

- exclusion of the swallowed-pure branch on a hypothetical witness;
- any original promoted pair selector or nonzero response;
- synchronization, activity, nuisance survival, or top-anchor attachment;
- a maximum-root witness realization of the local control;
- other shore ranks, higher-root source coverage, or a named `r>=4` detector;
- strategic-node closure, permanent restriction, or global resolution.

The smallest remaining load-bearing obligation is to contradict

```text
r_0,r_1,r_2 in B_Q^anc                              (10)
```

using the same graph's complete mixed GHZ equations, or to prove an exact
uncontracted labelwise response-faithfulness identity forcing the augmented
rank jump on every exceptional fibre.  Even the escape branch has no named
downstream entry by itself.

Hostile verdict after the provenance correction: **ACCEPT**.

The global conjecture remains **UNRESOLVED**.
