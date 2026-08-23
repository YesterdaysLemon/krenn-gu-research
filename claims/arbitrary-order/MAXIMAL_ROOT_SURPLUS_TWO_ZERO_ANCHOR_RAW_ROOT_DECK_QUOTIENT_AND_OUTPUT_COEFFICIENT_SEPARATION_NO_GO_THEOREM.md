# Maximum-root surplus-two zero-anchor raw root-deck quotient and output/coefficient separation no-go theorem

## Status and scope

This document proves an exact continuation of `GLS34` and corrects the type of
its proposed coefficient-side rank jump.

At a fixed residual contraction, the coefficient

```text
q=G_Q^A(z_Q) in E_A^*
```

is the raw coefficient of the residual-absent deck `H_Uhat`.  It is also the
retained `D=Q` nuisance killed by the `GLS22` transverse projector.  We define
the complete raw coefficient nuisance for the **re-labelled root-deck target**
and prove:

1. `q` survives this raw nuisance exactly when one constant functional
   isolates `H_Uhat` from every other labelled companion summand;
2. on a complete ternary GHZ hypothetical witness, the resulting quotient has
   an exact escape/swallow dichotomy;
3. on the non-silent branch of `GLS34`, escape makes `H_Uhat` a nonzero pure
   diagonal deck, while swallowing forces all three raw pure probe tensors
   into the same nuisance;
4. the `GLS34` all-port kernel equation and all singleton output classes do
   **not** force escape: an exact rational local physical graph has every one
   of those output conclusions but a single raw one-`Q` slice equal to `q`.

The isolated deck is `H_Uhat=C(B)` at root order three.  It is not the
residual-present four-port response `T=H_(Q union Uhat)` used by `GLD3` and is
not a `GLS22/GLS23` desired target.  This theorem therefore supplies no named
downstream detector entry, response/activity package, divisor exclusion,
arbitrary-root source cover, strategic-node closure, permanent restriction,
or global resolution.

This is `GLS35`.  The global Krenn--Gu conjecture remains **UNRESOLVED**.

## Dependencies and provenance

The owning interfaces are:

- [`GLS8`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_TWO_PROBE_ONE_TARGET_ATTACHMENT_AND_POINTWISE_FAILURE_REDUCTION_THEOREM.md)
  for the raw promoted companion identity and constant module selectors;
- [`GLS21`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_BASE_SHADOW_ALL_PORT_NUISANCE_COLLAPSE_THEOREM.md)
  for the retained `D=Q` all-port label;
- [`GLS22`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_ALL_PORT_TRANSVERSE_QUOTIENT_AND_PROJECTIVE_SYNCHRONIZATION_FAILURE_THEOREM.md)
  for `q`, `p`, and `P_Q`;
- [`GLS23`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_TRANSVERSE_COMPLETE_NUISANCE_DECOMPOSITION_AND_TOP_ANCHOR_DICHOTOMY_THEOREM.md)
  for the complete label-by-label slice notation;
- [`GLS33`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_RESIDUAL_LAURENT_POLARIZATION_AND_ROOT_DECK_KERNEL_ANCHOR_THEOREM.md)
  for the constant root-deck equations; and
- [`GLS34`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_TANGENT_ROOT_FITTING_AND_CONSTANT_ANCHOR_SEGRE_SILENCE_THEOREM.md)
  for the non-silent output-side anchor classes; and
- [`GLD3`](TWO_RESIDUAL_PAIR_FOUR_PORT_DIAGONAL_INTERFERENCE_AND_CAMOUFLAGE_BOUNDARY_THEOREM.md)
  for the residual-present pair responses and four-port response `T`.

No external literature claim is used.  The new content is the raw re-labelled
anchor module, its exact complete-target quotient, the interface correction,
and the physical local no-go.

## 1. The complete raw root-deck coefficient module

Let `K` have characteristic zero.  Retain the promoted notation

```text
Bhat=Q disjoint-union Uhat,       Q={q_0,q_1},
E_A^*=V_(a_0)^* tensor V_(a_1)^*,
q=G_Q^A(z_Q),                     p=epsilon_A(q),
omega=G_empty^A=W_(a_0,a_1).                         (1)
```

At one fixed residual contraction, for every
`D in binom(Bhat,2)` put

```text
D_0=D intersect Uhat,
g_D(z_Q)=G_D^A(z_(D intersect Q))
           in E_A^* tensor V_(D_0)^*.                 (2)
```

For an empty port factor, `Slice_empty(g)=Kg`.  Otherwise
`Slice_(D_0)(g_D)` is the span in `E_A^*` of all coefficient contractions in
every `D_0` slot, exactly as in the raw form underlying `GLS23`.

### Definition 1 (complete raw anchor nuisance)

Define

```text
B_Q^anc=K omega
 +sum_(D in binom(Bhat,2), D!=Q) Slice_(D_0)(g_D(z_Q))
 subseteq E_A^*.                                      (3)
```

The `K omega` term is mandatory.  Once the `D=Q` label is re-labelled as the
desired residual-absent deck, the `D=empty` top label is nuisance.  On the
zero-anchor branch `omega=0`, this summand vanishes but remains part of the
quantified definition.

Equivalently, let `A_Q` be the formal projection onto the deck label
`I=Uhat`.  If

```text
Gammahat_Q=q tensor A_Q+Theta_Q^anc,                  (4)
```

then `B_Q^anc` is the coefficient-slice space of `Theta_Q^anc`.

### Theorem 1 (exact residual-absent anchor selector criterion)

Assume `p!=0`.  The following are equivalent.

1. The raw anchor coefficient survives:

   ```text
   q notin B_Q^anc.                                   (5)
   ```

2. There is a constant functional `lambda_Q^anc in (E_A^*)^*` with

   ```text
   lambda_Q^anc(B_Q^anc)=0,
   lambda_Q^anc(q)=p.                                 (6)
   ```

3. One constant coefficient functional annihilates every raw labelled
   summand other than `D=Q` and isolates the root deck:

   ```text
   (lambda_Q^anc tensor id)(Gammahat_Q)=p A_Q.        (7)
   ```

#### Proof

Finite-dimensional separation gives `(5) <=> (6)`; the nonzero scalar `p`
fixes the normalization without dividing by a rank minor.  Definition (3)
says exactly that every coefficient of every non-`Q` labelled summand lies in
the kernel declared in (6).  Applying the functional to (4) gives (7).
Conversely, (7) forces the coefficient of `A_Q` to be nonzero and every
coefficient of `Theta_Q^anc` to vanish, which is (6).  `square`

This is a selector for a newly re-labelled residual-absent anchor.  It is not
a legal selector for any original promoted target: `GLS21` places `q` inside
every promoted target nuisance, and `GLS22` has `P_Q(q)=0`.

### Corollary 1.1 (the transverse quotient erases the rank jump)

On `omega=0`,

```text
P_Q(B_Q^anc)=N_empty^tr.                              (8)
```

In particular, `q notin B_Q^anc` cannot be expressed as survival in the
`GLS22/GLS23` transverse top quotient.

#### Proof

The operator `P_Q` acts only on the `E_A^*` factor, so it commutes with every
coefficient slice in (3).  Applying it label by label gives the exact
`GLS23` top-target formula.  The omitted label `D=Q` has `P_Q(q)=0`, and the
top term is zero under `omega=0`, proving (8).  Since `q` itself is killed by
`P_Q`, its extension class relative to the raw span is lost.  `square`

## 2. Complete-target quotient dichotomy

Assume now the complete ternary GHZ tensor equation.  Put

```text
r_c=e_(a_0,c)^* tensor e_(a_1,c)^*,
alpha_c=z_(q_0,c)z_(q_1,c),
W_Uhat=tensor_(u in Uhat)V_u^*.                       (9)
```

Every `alpha_c` is a residual-torus unit.  Write `[v]` for the class of
`v in E_A^*` modulo `B_Q^anc`.

### Theorem 2 (raw anchor escape/swallow dichotomy)

The complete target identity descends exactly to

```text
[q] tensor H_Uhat
 =sum_(c=0)^2 alpha_c [r_c] tensor e_c^(tensor |Uhat|)
 in (E_A^*/B_Q^anc) tensor W_Uhat.                   (10)
```

If the non-silent branch of `GLS34` holds, so that `H_Uhat!=0` and `p!=0`,
exactly one of the following occurs.

#### E. Raw anchor escape

`q notin B_Q^anc`.  Then the three pure quotient columns `[r_c]` span the
one-dimensional line `K[q]`, at least one is nonzero, and the functional of
Theorem 1 gives

```text
p H_Uhat=sum_c alpha_c lambda_Q^anc(r_c)
                         e_c^(tensor |Uhat|) !=0.     (11)
```

Thus the isolated residual-absent deck is nonzero and exactly pure diagonal.

#### S. Raw pure-probe swallow

`q in B_Q^anc`.  Then

```text
r_0,r_1,r_2 in B_Q^anc.                              (12)
```

#### Proof

Evaluate the two residual slots in the raw promoted identity.  By (3), the
coefficient of every term other than `D=Q` dies in the quotient.  The `D=Q`
term is `[q] tensor H_Uhat`, and the complete GHZ target is the right side of
(10).  This proves the identity without deleting a label.

In branch E, `[q]` and `H_Uhat` are both nonzero, so the left side has tensor
rank one.  Comparing the independent pure port words on the right shows that
all `[r_c]` lie on `K[q]` and at least one survives.  Applying the normalized
functional proves (11).  In branch S the left side of (10) is zero.  The three
pure port words are independent and every `alpha_c` is nonzero, so every
`[r_c]` is zero, giving (12).  The two membership alternatives are exhaustive
and disjoint.  `square`

Theorem 2 is pointwise on every residual coordinate, shore-rank, nuisance-rank,
and divisor fibre inside its declared `p!=0` non-silent gate.  It introduces
no response, shore-minor, or rank-minor denominator.

### Theorem 3 (all-rank finite presentation)

Let a matrix `B_Q(z)` have columns spanning `B_Q^anc(z)` in a fixed basis of
`E_A^*`, and let `[B_Q|q]` denote column augmentation.  At every point,

```text
q in B_Q^anc
 iff rank[B_Q|q]=rank B_Q,

q notin B_Q^anc
 iff rank[B_Q|q]=rank B_Q+1.                          (13)
```

The strata

```text
rank B_Q=k=rank[B_Q|q],             0<=k<=9,

and

rank B_Q=k,  rank[B_Q|q]=k+1,       0<=k<=8.          (14)
```

are an exhaustive pointwise case cover.  Thus exceptional nuisance-rank
fibres are part of the statement rather than being discarded by one chosen
minor.

#### Proof

Equation (13) is the column-span criterion.  Adjoining one column changes rank
by either zero or one, proving (14).  `square`

## 3. Exact physical local no-go

We now show that the output-side conclusion of `GLS34`, even together with
its exact all-port and singleton kernel equations, does not force branch E.

Work over `Q` with root-probe vertices `a_0,a_1`, residual vertices `q_0,q_1`,
and four promoted ports `u_0,u_1,u_2,u_3`.  Use column basis
`e_0,e_1,e_2` and put `one=(1,1,1)^T`.  Take

```text
s_0=s_1=z_(q_0)=z_(q_1)=one,

xi_0^0=e_1,   xi_0^1=e_2,
xi_1^0=e_2,   xi_1^1=e_1,

W_(a_i,q_s)=xi_i^s e_0^T,
W_(a_0,a_1)=0.                                       (15)
```

Hence

```text
q=e_1 tensor e_1+e_2 tensor e_2,       p=2.          (16)
```

At every promoted port use

```text
W_0=W_(a_0,u)=
 [[ 0, 1,-1],
  [ 1, 0, 0],
  [-1, 0, 1]],

W_1=W_(a_1,u)=
 [[ 1, 1,-1],
  [ 0,-1, 2],
  [-1, 0, 0]].                                       (17)
```

Both determinants are `-1`, and

```text
W_0^T one=e_1,        W_1^T one=e_2,
K_u^00=K e_0.                                         (18)
```

For `v=e_1+e_2`,

```text
W_0 v=e_2,            W_1 v=e_1.                     (19)
```

Therefore the single raw label `D={q_0,u}` has coefficient slice

```text
(id tensor v)(g_D)
 =xi_0^0 tensor W_1v+W_0v tensor xi_1^0
 =e_1 tensor e_1+e_2 tensor e_2=q.                   (20)
```

Thus `q in B_Q^anc` literally, before summing labels.  For the complete raw
slice matrix of this graph the exact ranks are

```text
rank B_Q=rank[B_Q|q]=8.                              (21)
```

Finish the four-port deck with

```text
W_(u_0,u_1)=e_0 e_0^T,
W_(u_2,u_3)=(1/2)e_0 e_0^T,                          (22)
```

and set all other port-pair, residual-port, residual-residual, and undeclared
edges to zero.  Then

```text
H_Uhat(e_0,e_0,e_0,e_0)=1/2,
p H_Uhat(e_0,e_0,e_0,e_0)=1.                         (23)
```

Choose the target-side diagonal weights

```text
delta=(1,1,1).
```

Its restriction at the same kernel tuple is also one.  Thus the exact
all-port `GLS33` kernel equation (and hence the non-silent `GLS34` branch)
holds at this local interface.  More strongly, after fixing the other three
ports at `e_0`, every free-port singleton identity has

```text
p H_Uhat(e_0,e_0,e_0,-)=e_0^*
   notin span{e_1^*,e_2^*}=A_u.                      (24)
```

The one-`Q` deck nuisance in those singleton contractions is zero because all
residual-port edges vanish.  Hence all four singleton identities hold exactly,
not merely modulo `A_u`.

### Theorem 4 (output survival does not force coefficient separation)

The graph (15)--(22) satisfies (16)--(24): `p!=0`, the constant diagonal is
non-silent on the complete product kernel, and every singleton output anchor
class survives, but `q in B_Q^anc` by one raw labelled slice.  Consequently
the implication

```text
GLS34 non-silent output classes
 + exact all-port/singleton kernel identities
 => q notin B_Q^anc                                  (25)
```

is false without an additional uncontracted mixed-GHZ or labelwise
faithfulness hypothesis.

The full eight-vertex graph has exact pure coefficients

```text
(0,0,0),                                              (26)
```

so it is not pure-normalized and is not a hypothetical witness.  It is not a
counterexample to Theorem 2 or to the Krenn--Gu conjecture.

#### Proof

Equations (16)--(20) follow by direct matrix multiplication.  Complete exact
coefficient slicing gives (21).  The only nonzero perfect matching of the
four ports at `e_0^tensor4` is the product of the two edges in (22), proving
(23).  Leaving one endpoint free gives `(1/2)e_0^*`; multiplication by `p=2`
proves (24).  Direct enumeration of the `105` perfect matchings on eight
vertices gives (26).  `square`

## 4. Corrected interface and remaining obligation

The new rank jump is not a hidden `GLS22/GLS23` target theorem.

```text
q:
  coefficient of D=Q residual-absent deck H_Uhat,
  retained nuisance for every original promoted target,
  killed by P_Q;

q notin B_Q^anc:
  legal only for the newly re-labelled raw anchor target,
  erased rather than represented by the transverse quotient;

H_Uhat at r=3:
  residual-absent C(B),
  not GLD3 residual-present T=H_(Q union Uhat).        (27)
```

Here the `GLD3` definitions are literal: its equations (2)--(4) call the
residual-present pair rows `D_uv` and set `T=z_1234`, with
`T=hC(B)+cross terms`.  The zero-anchor raw deck selected here is only the
`C(B)` factor before residual-pair attachment.

The `GLS34` observation map also cannot by itself repair this mismatch.  Its
profiles constrain response-weighted aggregate equations after physical decks
are inserted.  The raw module (3) contains every labelled coefficient slice,
including zero-response labels.  Turning aggregate tangent control into raw
coefficient separation therefore requires a new labelwise response-faithful
transport theorem.

The smallest load-bearing continuation on the same zero-anchor branch is now
the explicit swallowed-pure alternative

```text
r_0,r_1,r_2 in B_Q^anc
 => contradiction from the same graph's complete mixed GHZ equations,      (28)
```

or a physical uncontracted identity forcing the rank jump in (13).  Even
branch E supplies only a target-pure residual-absent anchor.  It does not
supply:

- any surviving original pair class `t_C` modulo `N_C^tr`;
- the distinct nonzero physical response required by `GLS22`;
- selector synchronization, selected-response activity, or nuisance survival;
- the residual-present top row (which has coefficient `omega=0` here);
- a named `r>=4` detector or arbitrary-root source cover.

Every one of those gates remains open.  The maximum-root surplus-two
supply-and-target-attachment strategic node and the global conjecture remain
**UNRESOLVED**.

## Verification

Run the focused exact primary verifier:

```text
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_raw_root_deck_quotient_and_output_coefficient_separation_nogo.py
```

Run the independent no-import audit:

```text
python claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_raw_root_deck_quotient_and_output_coefficient_separation_nogo.py
```

The audit uses only the Python standard library, a different exact elimination
route, and a separately generated perfect-matching recursion.
