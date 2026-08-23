# Maximum-root surplus-two zero-anchor first-polarized singleton kernels and simultaneous-absorption sharpness

## Status

**Exact characteristic-zero first-polarized kernel theorem and rational
same-graph sharpness certificate.**  The two first-polarized `GLS31` equations
admit denominator-free singleton isolation after contracting every other port
by its exact two-row kernel.  All zero-star and zero-deck fibres remain
explicit.

At root order three, one exact rational eight-vertex graph simultaneously has

- a maximum torus root of order three and outside incidence defect three;
- the one-active rank-two-shore zero-anchor profile, with `p=2` and `L=H`;
- pure coefficients exactly `(1,1,1)`;
- all six physical pair responses nonzero, all six normal images full, and the
  exact product-normal equation;
- both complete first-polarized equations, including every one-`Q` labelled
  deck term; and therefore the entire two-variable `GLS31` projected
  evaluation-pencil equation;
- the `GLS26` projected-diagonal inclusion; and
- all six nonzero desired pair tensors absorbed in their complete `GLS23`
  transverse nuisances.

The graph is not a hypothetical witness: exact evaluation finds `316`
nonzero mixed coefficients, including the Hamming-one word
`(1,1,1,1,1,1,1,2)` with coefficient `1`.  Thus the entire projected
shore-normal evaluation pencil plus every listed `GLS31` static gate is
insufficient.  The next
load-bearing equations must leave that two-dimensional evaluation plane or
resolve the residual-`Q`/actual-root mixed deck.

This is `GLS32`.  It does not exclude the one-active divisor, force a legal
selector, cover two-active or arbitrary-root source branches, close the
maximum-root surplus-two strategic node, or resolve the conjecture.  The
global Krenn--Gu status remains **UNRESOLVED**.

## Dependencies and notation

Use

- [`GLS22`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_ALL_PORT_TRANSVERSE_QUOTIENT_AND_PROJECTIVE_SYNCHRONIZATION_FAILURE_THEOREM.md) for `P_Q` and the exact transverse quotient;
- [`GLS23`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_TRANSVERSE_COMPLETE_NUISANCE_DECOMPOSITION_AND_TOP_ANCHOR_DICHOTOMY_THEOREM.md) for complete labelled nuisances;
- [`GLS26`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_ZERO_ANCHOR_DIAGONAL_RECONSTRUCTION_AND_RESIDUAL_SHORE_COVER_THEOREM.md) for the zero-anchor diagonal inclusion and `L`;
- [`GLS29`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_RANK_TWO_SHORE_NORMAL_CHANNEL_AND_INTERSECTING_SUPPLIER_EXCLUSION_THEOREM.md) for the product-normal equation;
- [`GLS30`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_NORMAL_PRODUCT_DIVISOR_KERNEL_PROFILE_AND_SAME_GRAPH_SHARPNESS_THEOREM.md) for the divisor profiles; and
- [`GLS31`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_SIMULTANEOUS_ABSORPTION_EVALUATION_PENCIL_AND_MIXED_EQUATION_SHARPNESS_THEOREM.md) for the complete first-polarized equations.

Retain `GLS31` notation over a characteristic-zero field.  In particular,
`Uhat` has `m=2r-2` promoted ports and

```text
a_u=W_(a_0,u)(s_0,-),       x_u=W_(a_0,u)(n_0,-),
b_u=W_(a_1,u)(s_1,-),       y_u=W_(a_1,u)(n_1,-),
lambda_i^s=xi_i^s(s_i),
S_(s,u)=H_(Bhat-{q_s,u})(z_(q_(1-s)),-_(Uhat-{u})).   (1)
```

The first-polarized equations are

```text
sum_D K_D^10 tensor R_(Uhat-D)
 +sum_(s,u)lambda_1^s x_u tensor S_(s,u)
 =sum_c alpha_c n_0(c)s_1(c)e_c^(tensor m),           (2)

sum_D K_D^01 tensor R_(Uhat-D)
 +sum_(s,u)lambda_0^s y_u tensor S_(s,u)
 =sum_c alpha_c s_0(c)n_1(c)e_c^(tensor m).           (3)
```

Every one-`Q` label in these sums is retained.

## 1. Denominator-free singleton isolation

For a port `u`, collect its one-`Q` decks as

```text
F_u^10=sum_s lambda_1^s S_(s,u),
F_u^01=sum_s lambda_0^s S_(s,u).                      (4)
```

Define exact local kernel spaces

```text
K_v^10=ker x_v intersect ker b_v,
K_v^01=ker a_v intersect ker y_v.                     (5)
```

### Theorem 1 (first-polarized singleton kernel identities)

Fix `u in Uhat`.  For arbitrary `z_v in K_v^10`, `v!=u`, equation (2)
contracts to

```text
sum_c alpha_c n_0(c)s_1(c)
  (product_(v!=u)z_v(c)) e_(u,c)^*
 =F_u^10((z_v)_(v!=u)) x_u.                          (6)
```

Symmetrically, for arbitrary `z_v in K_v^01`, equation (3) contracts to

```text
sum_c alpha_c s_0(c)n_1(c)
  (product_(v!=u)z_v(c)) e_(u,c)^*
 =F_u^01((z_v)_(v!=u)) y_u.                          (7)
```

Consequently the active-coordinate image of the corresponding multi-Hadamard
kernel product has dimension at most one.  If either left side is zero, the
identity gives no separate nonvanishing conclusion about its deck scalar or
local channel.  No response, deck value, coordinate, or minor is divided out.

#### Proof

Contract (2) at every port except `u`.  Every promoted-pair tensor

```text
K_D^10=x_i tensor b_j+b_i tensor x_j
```

contains a contracted endpoint, and its covector there is killed by the
declared intersection kernel.  A one-`Q` term indexed by `w!=u` is killed by
`z_w in ker x_w`; the unique singleton `w=u` remains and equals the right side
of (6).  The pure diagonal target contracts to the left side.  This proves
(6), and (7) is identical with the shores transposed.  The dimension and
zero-fibre statements follow directly.  `square`

This theorem is a necessary profile, not a selector theorem.  In particular,
the graph below lies in the completely silent fibre of both identities.

## 2. Exact first-polarized simultaneous-absorption control

Work over `Q`, order vertices

```text
(a_0,a_1,q_0,q_1,k,u_1,u_2,u_3),                     (8)
```

and use the all-ones vectors at the displayed roots and residual pair.  Let
`E_ij=e_i e_j^T`, put `w=e_1+e_2`, `J=ww^T`, and retain the edges

```text
W_(a_0,q_0)=E_11,             W_(a_0,q_1)=E_22,
W_(a_1,q_0)=E_22,             W_(a_1,q_1)=E_11,
W_(q_0,q_1)=E_00,

W_(a_0,k)=(e_0-e_2)e_0^T,
W_(a_1,k)=(e_0+e_1-2e_2)e_0^T,
W_(a_i,u_j)=E_00             (i=0,1; j=1,2,3).       (9)
```

For promoted-port order `P=(k,u_1,u_2,u_3)`, set

```text
(t_k,t_(u_1),t_(u_2),t_(u_3))=(1,1,1,1/12),         (10)
```

and define

```text
W_(q_0,u)= t_u e_0 w^T,
W_(q_1,u)=-t_u e_0 w^T.                              (11)
```

For pair order

```text
(ku_1,ku_2,ku_3,u_1u_2,u_1u_3,u_2u_3),
```

put

```text
(lambda_D)=(1,1,-3/2,1,1,-2),
W_D=lambda_D E_00+2t_ut_v J       (D={u,v}).          (12)
```

All unlisted edges are zero.

### Theorem 2 (complete evaluation-pencil sharpness)

The graph (9)--(12) has the following exact properties.

1. `R={a_0,a_1,k}` is a maximum torus root.  On outside order
   `(q_0,q_1,u_1,u_2,u_3)`, the incidence ranks are

   ```text
   (3,3,2,2,2),       sum_v(3-rank H_v)=3.            (13)
   ```

2. Its residual data are

   ```text
   X_0=X_1=span{e_1,e_2},       q=E_11+E_22,
   p=2,                          n_0=n_1=e_0,
   gamma=(1,0,0),                omega=0,
   L=H,                          dim H=1.               (14)
   ```

3. Every normal supplier is `2E_00`.  The physical response deck is

   ```text
   R_D=lambda_D E_00,                                  (15)
   ```

   so all six responses are nonzero, every target has full normal image, and

   ```text
   sum_D k_D tensor R_(Uhat-D)=e_0^(tensor4).          (16)
   ```

4. Both complete first-polarized equations (2)--(3) hold with every one-`Q`
   label retained.  Since the projected evaluation-pencil identity has
   bidegree at most `(1,1)` and its constant term cancels identically under
   `P_Q`, the entire two-variable `GLS31` projected evaluation-pencil equation
   holds.

5. The pure coefficients are `(1,1,1)`.  Each promoted desired tensor is
   nonzero of root-slice rank one.  The six complete `GLS23` pair-nuisance
   ranks, and the ranks after adjoining the desired tensor, are

   ```text
   (36,36,36,50,50,50).                               (17)
   ```

   Thus all six desired classes are absorbed.  The complete top nuisance has
   rank six and contains the projected diagonal rank-two space.

6. The graph is not a witness.  It has exactly `316` nonzero mixed words and

   ```text
   coeff(1,1,1,1,1,1,1,2)=1.                         (18)
   ```

#### Proof

The displayed `A` root equations hold because both `A-k` first factors sum to
zero and `W_(a_0,a_1)=0`.  A torus root containing either `a_i` contains no
`q_s` or `u_j`, by the matrix-unit edges in (9), and therefore has size at
most three.

Now omit `A`.  The edge `q_0q_1` prevents both residual vertices.  If a root
contains one `q_s` and a promoted port `u`, equation (11) forces
`w(z_u)=0`.  Two promoted ports `u,v` would then make their direct edge equal
the nonzero scalar `lambda_(uv)z_u(0)z_v(0)`, a contradiction.  Finally, four
promoted root vectors would, after division only by their nonzero torus
coordinates inside this contradiction proof, force

```text
lambda_(ku_1)lambda_(u_2u_3)
 =lambda_(ku_2)lambda_(u_1u_3)
 =lambda_(ku_3)lambda_(u_1u_2).                       (19)
```

The three values are `-2,1,-3/2`, so no four-port torus root exists.  This
proves maximality.  Direct contraction gives (13)--(14).

Residual evaluation of (11) gives opposite covectors `t_uw` and `-t_uw`.
Their two cross-matchings contribute `-2t_ut_vJ`, cancelling the second term
of (12) and proving (15).  The normal rows of every `A-Uhat` block are `e_0`,
so every supplier is `2E_00`; since

```text
2 sum_D lambda_D=1,
```

equation (16) follows.

For the first-polarized suppliers,

```text
a_k=b_k=0,          a_(u_j)=b_(u_j)=e_0,
x_u=y_u=e_0         for every u.                      (20)
```

Thus `K_D^10=K_D^01` is `E_00` on pairs meeting `k` and `2E_00` on the other
three pairs.  The promoted part of each first-polarized equation is

```text
1(lambda_(u_1u_2)+lambda_(u_1u_3)+lambda_(u_2u_3))
 +2(lambda_(ku_1)+lambda_(ku_2)+lambda_(ku_3))
 =0+2(1/2)=1.                                        (21)
```

All four residual-shore values `lambda_i^s` equal one.  For each fixed port,
the intact decks obey

```text
S_(0,u)+S_(1,u)=0,                                   (22)
```

because their unique remaining residual-to-port edge has opposite sign in
(11).  Hence, for each port, the complete one-`Q` sums cancel pairwise across
the two retained `s` labels.  Both right sides are
`e_0^(tensor4)`, proving the first-polarized equations without deleting a
label.  The constant and bidegree `(1,1)` statements give the full evaluation
pencil.

For colour zero, direct matching gives
`2(lambda_(ku_1)+lambda_(ku_2)+lambda_(ku_3))=1`.  For colours one and two,
the relevant `A-Q` matching is forced, every promoted edge has entry
`2t_ut_v`, and its four-port hafnian is

```text
3*4 product_u t_u=12*(1/12)=1.                       (23)
```

This proves pure normalization.  The `GLS23` companions depend only on the
unchanged `A-Q` and `A-Uhat` edges because `omega=0`; literal exact row
reduction gives (17), top rank six, and diagonal containment.  The two
independent retained verifiers replay those spaces.  Direct perfect-matching
evaluation proves (18) and the exhaustive mixed count.  `square`

In the singleton kernels of Theorem 1, every port of this control has
`K_v^10=K_v^01=e_0^perp`.  Every active-colour product in (6)--(7) is therefore
zero, so both identities are silent and yield no illicit activity inference.

## 3. Exact boundary and next obligation

Theorem 2 is an off-target control.  It refutes only the implication

```text
all GLS31 static gates + complete projected shore-normal evaluation pencil
 => contradiction or legal selector.                                (24)
```

It does not refute a theorem using the original coefficient deck.  The
smallest surviving one-active obligation is now residual-`Q`-resolved or
out-of-pencil mixed coupling: retain individual residual-colour coefficients
and root-coordinate directions outside `span{s_i,n_i}`, or prove a
synchronized residual-family argument which prevents their cancellation.
Every response/rank-drop fibre, the two-active divisor, other shore ranks,
arbitrary-root source coverage, and downstream legal attachment remain open.

## Verification

Run the focused exact primary verifier:

```text
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_first_polarized_simultaneous_absorption_sharpness.py
```

It rebuilds the graph, maximum-root and incidence certificates, complete
physical responses, all three nonconstant evaluation-pencil equations with
one-`Q` pairwise cancellation across retained labels, the complete
`GLS23`/`GLS26` modules, pure
coefficients, actual-root contraction failures, and all `3^8` mixed words.

Run the independent no-import audit:

```text
python claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_first_polarized_simultaneous_absorption_sharpness.py
```

It uses standard-library `Fraction`, a separate recursive matching engine,
sparse exact row reduction, and independently assembled labelled nuisances.
It imports neither the primary verifier, the `GLS31` verifier, nor SymPy.

The arbitrary-root singleton identities are proved by the written contraction
argument.  Neither script certifies a witness, divisor exclusion, node
closure, or global resolution.
