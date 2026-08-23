# Maximum-root surplus-two zero-anchor simultaneous absorption, evaluation-pencil identities, and mixed-equation sharpness

## Status

**Exact characteristic-zero physical polarization theorem and rational
same-graph sharpness certificate.**  On the rank-two-shore zero-anchor branch,
the two residual-shore normals polarize the complete top-target identity into
three denominator-free coefficient equations.  The bidegree `(1,1)` equation
is exactly the `GLS29` product-normal channel.  The first-polarized equations
retain all one-`Q` labelled nuisance terms and do not define a second
support-free quotient channel.

At root order three, an exact rational eight-vertex graph simultaneously has

- a maximum torus root of order three and incidence defect exactly six;
- `(d_0,d_1)=(2,2)`, `p=2`, `omega=0`, `L=H`, and one active normal-product
  colour;
- pure coefficients exactly `(1,1,1)`;
- all six physical pair responses nonzero and every normal nuisance image
  full;
- the exact scalar normal identity;
- the full diagonal inclusion occurring in `GLS26`; and
- all six nonzero desired pair tensors absorbed in their complete `GLS23`
  transverse nuisances.

It is not a hypothetical witness: exact evaluation finds `313` nonzero mixed
GHZ coefficients, including one displayed value `-1`.  Thus maximum-root
incidence, pure normalization, simultaneous pair absorption, nonzero
responses, full normal images, and top diagonal reconstruction are jointly
insufficient without the original mixed equations.  Those equations and
their one-`Q` labelled terms are load-bearing.

This is `GLS31`.  It does not exclude the one-active divisor, supply a legal
selector, close the maximum-root surplus-two strategic node, or resolve the
conjecture.  The global Krenn--Gu status remains **UNRESOLVED**.

## Dependencies and notation

Use

- [`GLS22`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_ALL_PORT_TRANSVERSE_QUOTIENT_AND_PROJECTIVE_SYNCHRONIZATION_FAILURE_THEOREM.md) for `q`, `p`, and `P_Q`;
- [`GLS23`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_TRANSVERSE_COMPLETE_NUISANCE_DECOMPOSITION_AND_TOP_ANCHOR_DICHOTOMY_THEOREM.md) for the complete labelled nuisance;
- [`GLS26`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_ZERO_ANCHOR_DIAGONAL_RECONSTRUCTION_AND_RESIDUAL_SHORE_COVER_THEOREM.md) for the zero-anchor diagonal inclusion and residual tangent envelope;
- [`GLS29`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_RANK_TWO_SHORE_NORMAL_CHANNEL_AND_INTERSECTING_SUPPLIER_EXCLUSION_THEOREM.md) for the product-normal channel and complete normal equation; and
- [`GLS30`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_NORMAL_PRODUCT_DIVISOR_KERNEL_PROFILE_AND_SAME_GRAPH_SHARPNESS_THEOREM.md) for the one-/two-active divisor profiles.

Retain the `GLS29` rank-two-shore notation over a characteristic-zero field:

```text
A={a_0,a_1},                  Q={q_0,q_1},
Uhat={u_1,...,u_m},           m=2r-2,
s_i=x_(a_i),                  X_i=span{xi_i^0,xi_i^1},
d_0=d_1=2,                    n_i spans X_i^perp,
q in X_0 tensor X_1,          p=q(s_0,s_1)!=0,
P_Q(v)=p v-v(s_0,s_1)q,       E_A^tr=ker ev_(s_0,s_1),
omega=W_(a_0,a_1)=0.                                  (1)
```

The normal vectors are residual-shore normals.  The affine expressions below
are evaluation pencils in the two `A` slots; they are not asserted to be
torus roots or tangent curves in the maximum-root locus.

## 1. Exact two-variable physical polarization

For every promoted port `u`, define covectors

```text
a_u=W_(a_0,u)(s_0,-),       x_u=W_(a_0,u)(n_0,-),
b_u=W_(a_1,u)(s_1,-),       y_u=W_(a_1,u)(n_1,-).       (2)
```

For `D={u,v}`, with factors put in the canonical `u,v` order, set

```text
K_D^00=a_u tensor b_v+b_u tensor a_v,
K_D^10=x_u tensor b_v+b_u tensor x_v,
K_D^01=a_u tensor y_v+y_u tensor a_v,
K_D^11=x_u tensor y_v+y_u tensor x_v.                 (3)
```

The final tensor is exactly the `GLS29` normal supplier `k_D`.

### Theorem 1 (denominator-free evaluation-pencil identity)

For formal parameters `tau,upsilon`,

```text
q(s_0+tau n_0,s_1+upsilon n_1)=p                     (4)
```

and the projected promoted-pair coefficient `t_D=P_Q(g_D)` obeys

```text
t_D(s_0+tau n_0,s_1+upsilon n_1)
 =p(tau K_D^10+upsilon K_D^01+tau upsilon K_D^11).   (5)
```

For `r_c=e_(a_0,c)^* tensor e_(a_1,c)^*` and
`delta_c=P_Q(r_c)`, one likewise has

```text
delta_c(s_0+tau n_0,s_1+upsilon n_1)
 =p(tau n_0(c)s_1(c)+upsilon s_0(c)n_1(c)
      +tau upsilon n_0(c)n_1(c)).                    (6)
```

No response, normal coordinate, rank minor, or incidence factor is inverted.

#### Proof

Each `n_i` annihilates `X_i`, while `q` belongs to
`X_0 tensor X_1`; hence every nonconstant term in (4) vanishes.  Before
projection, the two-root companion evaluates as

```text
g_D(s_0+tau n_0,s_1+upsilon n_1)
 =K_D^00+tau K_D^10+upsilon K_D^01
    +tau upsilon K_D^11.                              (7)
```

By definition,

```text
P_Q(g_D)(z_0,z_1)=p g_D(z_0,z_1)-g_D(s_0,s_1)q(z_0,z_1).
```

Use (4), `g_D(s_0,s_1)=K_D^00`, and (7); the constant term cancels and
gives (5).  The same calculation with
`r_c(z_0,z_1)=z_0(c)z_1(c)` gives (6).  `square`

## 2. The three complete top-target coefficient equations

Write

```text
lambda_i^s=xi_i^s(s_i).
```

For a one-`Q` label `{q_s,u}`, retain the exact deck tensor

```text
S_(s,u)=H_(Bhat-{q_s,u})
          (z_(q_(1-s)),-_(Uhat-{u})).                 (8)
```

This is a labelled one-residual deck tensor, not a physical pair response.
Let `R_(Uhat-D)` denote the promoted complement-response tensor in the
owning `GLS29` identity.

### Theorem 2 (complete polarized top equations)

On the zero-anchor hypothetical-witness branch, the coefficients of `tau`,
`upsilon`, and `tau upsilon` in the complete projected top equation are

```text
sum_D K_D^10 tensor R_(Uhat-D)
 +sum_(s,u) lambda_1^s x_u tensor S_(s,u)
 =sum_c alpha_c n_0(c)s_1(c)e_c^(tensor m),           (9)

sum_D K_D^01 tensor R_(Uhat-D)
 +sum_(s,u) lambda_0^s y_u tensor S_(s,u)
 =sum_c alpha_c s_0(c)n_1(c)e_c^(tensor m),          (10)

sum_D K_D^11 tensor R_(Uhat-D)
 =sum_c alpha_c n_0(c)n_1(c)e_c^(tensor m).          (11)
```

Here the first sums run over promoted pairs and the second sums run over
`s in {0,1}` and `u in Uhat`.  Equation (11) is exactly the `GLS29`
product-normal identity.  In particular, omitting the one-`Q` sums from
(9)--(10) is a type error.

#### Proof

Apply `P_Q` to the complete `GLS22` top identity and evaluate its two `A`
slots at the pencils in Theorem 1.  A promoted-pair label gives (5).  For a
one-`Q` label, the raw two-root coefficient is

```text
xi_0^s tensor W_(a_1,u)+W_(a_0,u) tensor xi_1^s.
```

The normals kill the corresponding `xi` factors, so after the same constant
projection cancellation its nonconstant terms are exactly

```text
p tau lambda_1^s x_u,
p upsilon lambda_0^s y_u,
```

with no bidegree `(1,1)` term.  The label `D=Q` projects to zero.  The
top-grade label has coefficient `omega` and vanishes only because the branch
assumes `omega=0`.  The diagonal target side expands by (6).  Thus every
displayed equation first has a common factor `p`; cancel it using the declared
gate `p!=0`.  This proves (9)--(11).  `square`

## 3. The retained-root quotient is the old normal channel

Define

```text
C_0:E_A^tr -> V_(a_1)^*,       C_0(v)=v(n_0,-),
C_1:E_A^tr -> V_(a_0)^*,       C_1(v)=v(-,n_1),
Tbar=P_Q(T_Q).                                         (12)
```

### Theorem 3 (no second support-free quotient channel)

On the rank-two-shore branch,

```text
C_0(E_A^tr)=V_(a_1)^*,       C_0(Tbar)=X_1,
E_A^tr/Tbar  ~=  V_(a_1)^*/X_1,                       (13)
```

and symmetrically with the shores transposed.  Under the first isomorphism,

```text
[delta_c] |-> p n_0(c)[e_c^*].                        (14)
```

The unique quotient functional on the right is `n_1`; applying it to (14)
gives `p n_0(c)n_1(c)=p gamma_c`.  Hence this retained-root quotient is
exactly the existing `GLS29` product-normal channel, not a new independent
invariant.

#### Proof

The vectors `s_0,n_0` are independent: otherwise `q(n_0,s_1)=0` would
contradict `q(s_0,s_1)=p!=0`.  Choose a covector `h` with
`h(n_0)=1,h(s_0)=0`.  Then `h tensor ell` lies in `E_A^tr` and maps to any
prescribed `ell`, proving surjectivity.  Contraction by `n_0` kills
`X_0 tensor V_(a_1)^*` and maps
`V_(a_0)^* tensor X_1` onto `X_1`.  It also kills `q`, so
`C_0(P_Q(T_Q))=pX_1=X_1` as subspaces.  Both quotients have dimension one
because `d_0=d_1=2`, proving (13).  Direct evaluation of `P_Q(r_c)` proves
(14).  `square`

This theorem does not say that no legal selector exists.  It says only that
this support-free contraction supplies no quotient channel beyond `gamma`.
For an inactive colour, `gamma_c=0` makes its image vanish in the quotient;
target-specific separation may still occur elsewhere in the complete
`GLS23` nuisance.

## 4. Exact maximum-root simultaneous-absorption control

Work over `Q`.  Order the vertices

```text
(a_0,a_1,q_0,q_1,k,u_1,u_2,u_3),                     (15)
```

and use the all-ones vector at the three displayed roots and both residual
ports.  Let `E_ij=e_i e_j^T` and

```text
J=(e_1+e_2)(e_1+e_2)^T.
```

All unlisted edges are zero.  For the listed orientation, rows belong to the
first endpoint and columns to the second:

```text
W_(a_0,q_0)=E_11,             W_(a_0,q_1)=E_22,
W_(a_1,q_0)=E_22,             W_(a_1,q_1)=E_11,
W_(q_0,q_1)=E_00,

W_(a_0,k)=(e_0-e_2)e_0^T,
W_(a_1,k)=(e_0+e_1-2e_2)e_0^T,
W_(a_i,u_j)=E_00             (i=0,1; j=1,2,3),

W_(q_0,k)=W_(q_0,u_1)=E_11+E_22,
W_(q_1,u_2)=E_11+E_22,
W_(q_1,u_3)=(E_11+E_22)/2,

W_(k,u_1)=E_00,
W_(k,u_2)=W_(u_1,u_2)=E_00-J,
W_(k,u_3)=W_(u_1,u_3)=E_00-J/2,
W_(u_2,u_3)=-(9/2)E_00.                              (16)
```

### Theorem 4 (same-graph sharpness certificate)

The graph (16) has all of the properties listed in the status section, with
the following exact records.

1. `R={a_0,a_1,k}` is a maximum torus root.  On the outside vertices
   `(q_0,q_1,u_1,u_2,u_3)`, the incidence ranks are

   ```text
   (2,2,1,2,2),        sum_v (3-rank H_v)=6.           (17)
   ```

2. The residual data are

   ```text
   X_0=X_1=span{e_1,e_2},       q=E_11+E_22,
   p=2,                          n_0=n_1=e_0,
   gamma=(1,0,0),                omega=0,
   L=H,                          dim H=1.               (18)
   ```

3. In promoted-pair order

   ```text
   (ku_1,ku_2,ku_3,u_1u_2,u_1u_3,u_2u_3),
   ```

   every normal supplier is `k_D=2E_00`, while the physical response matrices
   are

   ```text
   (1,1,1,1,1,-9/2) E_00.                             (19)
   ```

   Hence all six responses are nonzero, every target has a nonzero disjoint
   normal supplier, every normal nuisance image is full, and

   ```text
   sum_D k_D tensor R_(Uhat-D)=e_0^(tensor 4).         (20)
   ```

4. The pure coefficients are exactly `(1,1,1)`.  Every promoted desired
   tensor `t_D` is nonzero and has root-slice rank one.  The exact complete
   `GLS23` pair-nuisance ranks are

   ```text
   (36,36,36,50,50,50),                               (21)
   ```

   in the same pair order, and adjoining the corresponding desired tensor
   never raises the rank.  Thus all six desired classes are absorbed.

5. The complete top transverse nuisance has rank six.  The projected
   diagonal space has rank two and lies in that nuisance.  Explicitly,

   ```text
   P_Q(r_0)=2E_00-q,
   P_Q(r_1)=E_11-E_22,
   P_Q(r_2)=-P_Q(r_1).                                (22)
   ```

6. The graph is not a GHZ witness.  Exact coefficient evaluation gives

   ```text
   coeff(0,0,0,0,0,1,0,1)=-1                         (23)
   ```

   although the target coefficient is zero.  In total exactly `313` mixed
   words have nonzero coefficients.

#### Proof

The internal root edge `W_(a_0,a_1)` is zero and both displayed `A-k` blocks
have total entry sum zero, so `R` is a torus root.  Consider the graph of
nonzero matrix-unit edges.  If an independent set contains either `a_i`, it
contains no `q_s` or `u_j`, leaving at most `{a_0,a_1,k}`.  Without the two
`A` vertices, the three disjoint matrix-unit edges

```text
q_0q_1,       ku_1,       u_2u_3
```

force size at most three.  A torus root cannot contain both endpoints of a
nonzero matrix-unit edge, so every torus root has order at most three.

Direct contraction of (16) by the three root vectors gives

```text
H_(q_0)=[[0,1,0],[0,0,1],[0,1,1]],
H_(q_1)=[[0,0,1],[0,1,0],[0,0,0]],
H_(u_1)=[[1,0,0],[1,0,0],[1,0,0]],
H_(u_2)=[[1,0,0],[1,0,0],[1,-2,-2]],
H_(u_3)=[[1,0,0],[1,0,0],[1,-1,-1]],
```

proving (17).  The four `A-Q` blocks give (18).  Contracting the `A-Uhat`
blocks by the normals gives `x_u=y_u=e_0`, hence `k_D=2E_00`.  The two
cross-matchings through `Q` cancel precisely the `J` parts in (16), proving
(19).  Since `2(1+1+1+1+1-9/2)=1`, (20) follows.

For colour zero, the perfect-matching expansion is
`2 sum_D R_D(0,0)=1`.  For each of colours one and two, the `A-Q` matching is
forced and the remaining promoted hafnian is
`(-1)(-1/2)+(-1/2)(-1)=1`.  This proves pure normalization.

Apply the literal labelled-slice formula of `GLS23` to every pair in (16).
Exact row reduction gives (21), with each desired column already in the
corresponding nuisance.  For the top target, the same formula gives rank six;
the three direct projector calculations in (22) show the diagonal inclusion.
These are finite exact rational row reductions, independently replayed by the
two retained scripts below.  Finally, the direct perfect-matching expansion
of (23) is `-1`; exhaustive evaluation of the `3^8-3` mixed words gives the
declared count.  `square`

## 5. Exact boundary and next obligation

Theorem 4 is an off-target sharpness graph, not a source witness.  It proves
that none of the following implication patterns is valid without an original
mixed-equation premise:

```text
maximum root + defect bound + pure normalization
 + six nonzero responses + full normal images
 + scalar normal identity + top diagonal inclusion
 + simultaneous complete pair absorption
 => contradiction or legal selector.                                (24)
```

Theorems 1--3 then identify the first surviving exact coefficient family.
The smallest load-bearing continuation is to retain the one-`Q` terms in
(9)--(10) and prove, on every one-/two-active divisor and every rank-drop
fibre, either

- a target-specific complete-`GLS23` separator with nonzero physical
  response and every downstream legal gate; or
- a contradiction from (9)--(10) together with the original mixed GHZ/root
  deck.

Neither the first-polarized suppliers nor their scalar evaluations are by
themselves legal selectors.  Arbitrary-root source coverage and all
downstream attachment gates remain open.

## Verification

Run the focused exact primary verifier:

```text
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_simultaneous_absorption_and_tangent_pencil_sharpness.py
```

It reconstructs the graph, maximum-root and incidence certificates, physical
responses, normal identity, complete `GLS23`/`GLS26` spaces, pure and mixed
coefficients, and the two-variable polarization and quotient dimensions using
exact SymPy arithmetic.

Run the independent no-import audit:

```text
python claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_simultaneous_absorption_and_tangent_pencil_sharpness.py
```

It imports neither the primary verifier nor SymPy.  It uses standard-library
`Fraction`, a separate recursive matching engine, sparse column reduction,
literal labelled-slice assembly, and a separate bivariate-polynomial replay.

These scripts certify the finite exact mechanisms and graph.  The
arbitrary-root physical polarization is proved by the written tensor
calculation above.  They do not certify a witness, node closure, or global
resolution.
