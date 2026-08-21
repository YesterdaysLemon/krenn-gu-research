# Maximum-root surplus-two promoted base-shadow all-port nuisance collapse

## Status

**Exact characteristic-zero arbitrary-root no-go theorem.**  In the promoted
two-probe chart of `GLS8` and its source-aligned base quotient `GLS20`, the
residual-absent all-port deck label is a nuisance for every source
top-minus-two target.  After maximum-root contraction its coefficient is
exactly the `GLS4` incidence polynomial `p_(A,Q)`.  Its complete coefficient
slices therefore contribute

```text
p_(A,Q) V_C^* subset N_C^base.                        (1)
```

On the required source gate `p_(A,Q)(z_Q)!=0`, every nine-dimensional base
nuisance is the whole `V_C^*`.  Hence no source-aligned base class survives,
no legal selector can factor through the maximum-root contraction, and every
`GLS20` base-shadow radical--Fitting failure containment is automatic.

This theorem closes the proposed **base-shadow survival route as a no-go**.
It does not show that the full `81`-dimensional `GLS8` desired class is
absorbed, exclude selectors which do not factor through maximum-root
contraction, force response zero, or supply a downstream detector.  It does
not close the strategic node.  The global Krenn--Gu conjecture remains
**UNRESOLVED**.

## Dependencies and provenance

The source gate and the identification

```text
p_(A,Q)(z_Q)=epsilon_A(G_Q^A(z_Q))                   (2)
```

come from

- [`GLS4`](MAXIMAL_ROOT_SURPLUS_TWO_SAME_PAIR_QUOTIENT_SURVIVAL_AND_COMPLEMENTARY_PERMANENT_DOMINANCE_THEOREM.md); and
- [`GLS8`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_TWO_PROBE_ONE_TARGET_ATTACHMENT_AND_POINTWISE_FAILURE_REDUCTION_THEOREM.md).

The base quotient, factor-through selector criterion, and nine-row Fitting
profile come from

- [`GLS20`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_SOURCE_ALIGNED_BASE_SHADOW_AND_TARGET_FAILURE_THEOREM.md).

No external literature claim is used.  The new content is the exact
all-port-nuisance identification and its pointwise and determinantal
consequences.

## 1. The complete nuisance term

Retain the `GLS8` notation

```text
Omega=R disjoint-union B,          |R|=r>=3,
Q={q_0,q_1} subset B,              A={a_0,a_1} subset R,
K_0=R-A,                           U=B-Q,
Uhat=K_0 disjoint-union U,
Bhat=Q disjoint-union Uhat.                              (3)
```

The promoted two-probe identity is

```text
T_W(-_A,-_Bhat)
 =sum_(D in binom(Bhat,2)) G_D^A tensor H_(Bhat-D)
  +G_empty^A tensor H_Bhat.                             (4)
```

Fix a source Laplace pair and target

```text
C in binom(U,2),                  S_C=Uhat-C.           (5)
```

The desired label for this target is `Bhat-C=Q union S_C`.  The distinct
choice `D=Q` in (4) supplies

```text
G_Q^A tensor H_Uhat.                                    (6)
```

It is an active same-grade label and is part of the complete nuisance
remainder for `S_C`.  It cannot be discarded by target projection or by
calling it residual-absent.

After evaluating the two `Q` slots, (6) is the operator

```text
G_Q^A(z_Q) tensor id_(W_Uhat):W_Uhat -> E_A^* tensor W_Uhat.
                                                               (7)
```

Factor

```text
W_Uhat=V_C^* tensor W_(S_C),
L_C^*=E_A^* tensor V_C^*.                              (8)
```

Every coefficient slice of (7) in the `W_(S_C)` factor is retained in the
complete `GLS8` nuisance `N_C subset L_C^*`.

## 2. Base-shadow collapse

Contract the probe-root slots at their fixed maximum-root vectors:

```text
epsilon_A:L_C^* -> V_C^*,
b_C=epsilon_A(G_C^A),
N_C^base=epsilon_A(N_C).                               (9)
```

### Theorem 1 (all-port identity submodule)

Over the residual Laurent ring,

```text
p_(A,Q) V_C^* subset N_C^base                         (10)
```

for every `C in binom(U,2)`.

#### Proof

Apply `epsilon_A` to (7).  Equation (2) turns it into

```text
p_(A,Q)(z_Q) id_(W_Uhat).                              (11)
```

Under the factorization (8), the coefficient slices of the identity operator
in the `W_(S_C)` factor are the nine coordinate vectors spanning `V_C^*`.
Multiplication by `p_(A,Q)` gives exactly `p_(A,Q)V_C^*`.  Since (6) is a
retained nuisance label, all these vectors lie in `N_C^base`.  `square`

### Corollary 1.1 (pointwise total base absorption)

At every residual point with `p_(A,Q)(z_Q)!=0`,

```text
N_C^base(z_Q)=V_C^*,                 dim N_C^base=9,   (12)
[b_C]=0 in V_C^*/N_C^base                              (13)
```

for every source pair `C`.  Thus the `GLS20` pointwise trichotomy always lies
in its base-absorption branch on the `GLS4` common gate.  The physical
response may be zero or nonzero; it is not used.

#### Proof

At the stated point, multiplication by `p_(A,Q)(z_Q)` is an invertible scalar,
so (10) contains all of `V_C^*`.  The reverse containment is definitional.
Equation (13) follows.  `square`

### Corollary 1.2 (factor-through selector no-go)

There is no legal normalized `GLS8` target selector of the form

```text
lambda_C=mu_C compose epsilon_A                       (14)
```

at a point with `p_(A,Q)!=0`.

#### Proof

Any such legal selector must annihilate `N_C^base` and normalize `b_C` by the
`GLS20` factor-through criterion.  Equation (12) forces `mu_C=0`, which cannot
normalize any desired coefficient.  `square`

This does not exclude a legal upstairs selector whose covector on
`E_A^* tensor V_C^*` does not factor through `epsilon_A`.

## 3. Automatic Fitting failure

Let `B_C^base(z)` be any presentation of `N_C^base(z)` over the residual
Laurent ring, and let `D_C^base` be the three diagonal pure columns of
`GLS20`.  Theorem 1 permits a presentation containing the block

```text
p I_9.                                                  (15)
```

### Theorem 2 (the GLS20 failure profile is forced)

For every `1<=j<=9`,

```text
(h p) I_j([B_C^base|D_C^base])
  subset sqrt_geom(I_j(B_C^base)).                     (16)
```

Consequently the source-aligned useful locus `U_C^base` is empty for every
`C in binom(U,2)`.

#### Proof

Every `j`-element coordinate subset of (15) has determinant `p^j`, so

```text
p^j in I_j(B_C^base),             p in sqrt_geom(I_j(B_C^base)). (17)
```

Every generator on the left side of (16) is a multiple of `p`, proving the
containment.  Equivalently, on `D(p)` the nuisance matrix has row rank nine and
adjoining any pure columns cannot raise rank.  The exact `GLS20` Fitting
criterion now makes `U_C^base` empty.  No minor or response is divided out.
`square`

### Corollary 2.1 (the Laplace circuit is automatic)

On `D(p)`, every source base coefficient lies in its base nuisance, so the
`GLS20` source identity writes the nonzero complementary permanent as

```text
0!=Pi_Q in sum_(C in binom(U,2))
  N_C^base tensor K Per_(K_0,U-C).                     (18)
```

This is precisely the all-port nuisance circuit induced by (6).  It is not a
contradiction to the complete GHZ equations.

## 4. Corrected proof-DAG boundary

The exact route is now

```text
GLS4 p_(A,Q)!=0
 -> GLS8 promoted complete nuisance
 -> GLS20 maximum-root base shadow
 -> D=Q all-port nuisance contributes p I_9
 -> every source base quotient is zero.                (19)
```

Therefore future work must not try to force survival in the `GLS20` base
quotient on the same `p!=0` gate.  The live promoted alternatives are:

1. use the full `81`-dimensional `GLS8` quotient and selectors not factoring
   through `epsilon_A`;
2. find a joint multi-target identity whose legal nuisance treatment does not
   discard the all-port label; or
3. use complete mixed GHZ coefficients to contradict the full upstairs
   simultaneous failure profile.

None is proved here.  In particular, quotienting out or deleting the
all-port label would change the legal-selector problem and is not allowed.

**Subsequent exact continuation.**  `GLS22` implements the first alternative
without deleting the label: on `D(p)`, the denominator-free operator
`P_Q=pI-G_Q^A(z_Q) tensor epsilon_A` quotients its exact uncontracted root
line and gives a selector-equivalent `72/8`-row transverse module.  See
[`GLS22`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_ALL_PORT_TRANSVERSE_QUOTIENT_AND_PROJECTIVE_SYNCHRONIZATION_FAILURE_THEOREM.md).

The following remain **OPEN**:

```text
full GLS8 selector survival/nonzero response:             OPEN;
full upstairs simultaneous-failure exclusion:             OPEN;
r=3 complete seven-row package and activity:               OPEN;
r>=4 named promoted downstream detector:                  OPEN;
original-chart projective synchronization/transport:       OPEN;
strategic-node closure:                                    OPEN.
```

The global Krenn--Gu conjecture remains **UNRESOLVED**.

## 5. Verification

Run the focused exact primary verifier:

```bash
python claims/arbitrary-order/verify_maximal_root_surplus_two_promoted_base_shadow_all_port_nuisance_collapse.py
```

Run the independent no-import audit:

```bash
python claims/arbitrary-order/audit_maximal_root_surplus_two_promoted_base_shadow_all_port_nuisance_collapse.py
```

The scripts replay the all-port identity slices, nine-row collapse,
factor-through no-go, determinantal divisibility, and arbitrary-root label
counts.  The arbitrary-root proof is the written operator argument above.
