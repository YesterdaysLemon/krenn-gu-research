# Maximum-root surplus-two promoted source-aligned base shadow and target failure

## Status

**Exact characteristic-zero arbitrary-root source-to-target quotient theorem.**
In the promoted two-probe chart of `GLS8`, contract the two probe-root
coefficient slots at the same maximum-root vectors used by the `GLS4`
source.  For every source Laplace pair `C subset U`, this sends the complete
`81`-dimensional target coefficient module to a `9`-dimensional base module

```text
V_C^*/N_C^base,
N_C^base=epsilon_A(N_(S_C)).                           (1)
```

Survival of the contracted desired coefficient is equivalent to a legal
normalized target selector which factors through this maximum-root
contraction.  The `GLS4` Laplace identity forces at least one of the raw
contracted desired coefficients to be nonzero, and it gives an exact
source-level circuit when all of them are swallowed by their base nuisances.

On the complete GHZ target, the base quotient obeys

```text
sum_c alpha_c kappa_(A,c)[e_(C,c)^*] tensor w_(S_C,c)
  =[b_C] tensor P_(S_C)(H;z_Q).                       (2)
```

Consequently its three diagonal pure columns have rank at most one.  A
source-aligned target is useful exactly when the base desired class survives
and its physical response is nonzero.  Failure at a point is the exhaustive
three-way split: base absorption, or base survival with response zero, or a
useful legal row.  Geometric radical--Fitting containments encode simultaneous
failure for every source Laplace pair at one residual point, including every
nuisance-rank-drop fibre and without division.

This theorem sharpens and integrates the `GLS8` source interface; it does
**not** force a base class or response to survive, exclude the simultaneous
failure locus, supply the complete seven-row `GLD3` package at `r=3`, provide
a named downstream detector at `r>=4`, or prove synchronization, activity,
alignment, nuisance survival beyond the selected row, or any permanent
restriction.  It does not close the strategic node.  The global Krenn--Gu
conjecture remains **UNRESOLVED**.

**Subsequent route closure.**  `GLS21` identifies the retained `D=Q`
residual-absent all-port label as the exact nuisance block `p_(A,Q)I_9`.
Therefore on the required `p_(A,Q)!=0` source gate every base quotient in this
document is zero.  The conditional equivalences proved here remain correct,
but their base-survival branch is not physically available on that gate.  See
[`GLS21`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_BASE_SHADOW_ALL_PORT_NUISANCE_COLLAPSE_THEOREM.md).

## Dependencies and provenance

The same-pair source, the nonzero complementary permanent, the surviving
order-two source class, and the nonzero incidence polynomial come from

- [`GLS4`](MAXIMAL_ROOT_SURPLUS_TWO_SAME_PAIR_QUOTIENT_SURVIVAL_AND_COMPLEMENTARY_PERMANENT_DOMINANCE_THEOREM.md).

The promoted partition, complete nuisance module, legal-selector criterion,
complete target quotient, and geometric pointwise failure method come from

- [`GLS8`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_TWO_PROBE_ONE_TARGET_ATTACHMENT_AND_POINTWISE_FAILURE_REDUCTION_THEOREM.md).

No external literature claim is used.  The new content is the factor-through
base quotient, its source-level Laplace circuit, the contracted complete-target
identity, and the exact source-aligned failure profile.

## 1. Promoted source chart and base quotient

Work over a characteristic-zero field `K`.  Retain the notation and all
hypotheses of `GLS8`:

```text
Omega=R disjoint-union B,       |R|=r>=3,       |B|=r+2,
Q={q_0,q_1} subset B,           A={a_0,a_1} subset R,
K_0=R-A,                        U=B-Q,
Uhat=K_0 disjoint-union U.                              (3)
```

The root vectors `x_a`, `a in A`, are fully supported and satisfy

```text
W_(a_0,a_1)(x_(a_0),x_(a_1))=0.                       (4)
```

For a source Laplace pair and its promoted target put

```text
C in binom(U,2),              S_C=Uhat-C,
E_A^*=tensor_(a in A)V_a^*,   L_C^*=E_A^* tensor V_C^*,
g_C=G_C^A in L_C^*.                                    (5)
```

Let `N_C=N_(S_C)` be the **complete** `GLS8` nuisance coefficient-slice
space.  Thus no unwanted label, same-grade slice, residual-absent slice, or
higher-grade slice has been discarded.

Contract the probe-root slots at their fixed maximum-root vectors:

```text
epsilon_A:L_C^* -> V_C^*,
epsilon_A=(x_(a_0) tensor x_(a_1)) contraction id_(V_C^*),
b_C=epsilon_A(g_C),
N_C^base=epsilon_A(N_C) subset V_C^*.                 (6)
```

Although `N_C` has ambient dimension `81`, its base shadow has ambient
dimension `9`.  This is an image of the complete nuisance, not a selected or
truncated nuisance presentation.

### Theorem 1 (factor-through selector equivalence)

For every `C in binom(U,2)`, the following are equivalent.

1. The base desired class survives:

   ```text
   [b_C]!=0 in V_C^*/N_C^base.                         (7)
   ```

2. There is a covector `mu_C in (V_C^*)^*` such that

   ```text
   mu_C(N_C^base)=0,              mu_C(b_C)=1.         (8)
   ```

3. There is a legal normalized `GLS8` selector of the special form

   ```text
   lambda_C=mu_C compose epsilon_A,
   (lambda_C tensor id)Gammahat_Q=mathsf P_(S_C).      (9)
   ```

In particular, base survival implies full `GLS8` survival.  Conversely, full
absorption `g_C in N_C` implies base absorption `b_C in N_C^base`.  A full
selector which does not factor through `epsilon_A` need not be visible in the
base quotient.

#### Proof

Finite-dimensional separation gives the equivalence of (7) and (8).  If
(8) holds, then `lambda_C` annihilates `N_C` because `epsilon_A(N_C)` is
`N_C^base`, and `lambda_C(g_C)=mu_C(b_C)=1`.  The complete legal-selector
criterion of `GLS8` gives (9).  Conversely, a selector in (9) supplies a
`mu_C` satisfying (8).  Finally, applying `epsilon_A` to an inclusion
`g_C in N_C` gives `b_C in N_C^base`.  No converse is asserted.  `square`

## 2. Exact source Laplace circuit

For `C in binom(U,2)`, let

```text
tau_C=Per_(K_0,U-C) in V_(U-C)^*.                     (10)
```

Tensor factors are inserted in the fixed `U` order.  The `GLS8` Laplace
identity is

```text
Pi_Q=sum_(C in binom(U,2)) b_C tensor tau_C.           (11)
```

Define the source-aligned base nuisance space

```text
N_Q^Lap=sum_(C in binom(U,2))
  N_C^base tensor K tau_C       subset V_U^*.          (12)
```

### Theorem 2 (source survival and swallowed-base circuit)

At least one `C in binom(U,2)` has `b_C!=0`.  Moreover,

```text
[Pi_Q]=sum_(C:b_C notin N_C^base)
  [b_C tensor tau_C]              in V_U^*/N_Q^Lap.   (13)
```

Hence either some source-aligned base class survives, or

```text
0!=Pi_Q in N_Q^Lap.                                   (14)
```

Equation (14) is an explicit nonzero swallowed-base circuit.  The theorem
does not assert that `Pi_Q` survives modulo `N_Q^Lap`; `GLS4` proves only
`Pi_Q!=0`.

#### Proof

If every `b_C` were zero, (11) would contradict `Pi_Q!=0`.  In the quotient
by (12), every summand with `b_C in N_C^base` vanishes, proving (13).  If no
base class survives, (11) places `Pi_Q` in `N_Q^Lap`; it remains nonzero by
the `GLS4` source theorem.  `square`

## 3. Complete-target coupling

Assume now that the full graph tensor is the ternary GHZ target.  For
`c in {0,1,2}`, put

```text
e_(C,c)^*=tensor_(u in C)e_(u,c)^*,
w_(S_C,c)=tensor_(u in S_C)e_(u,c)^*,
alpha_c=z_(q_0,c)z_(q_1,c),
kappa_(A,c)=e_(a_0,c)^*(x_(a_0))e_(a_1,c)^*(x_(a_1)). (15)
```

Every `alpha_c` is a unit on the residual torus, and every `kappa_(A,c)` is
nonzero because the two root vectors are fully supported.

### Theorem 3 (base target identity and useful-row equivalence)

In the base quotient `V_C^*/N_C^base`, the complete target identity is

```text
sum_(c=0)^2 alpha_c kappa_(A,c)[e_(C,c)^*]
  tensor w_(S_C,c)
 =[b_C] tensor P_(S_C)(H;z_Q).                        (16)
```

Consequently

```text
dim span{[e_(C,0)^*],[e_(C,1)^*],[e_(C,2)^*]}<=1.     (17)
```

The following are equivalent at every fully supported residual contraction.

1. `[b_C]!=0` and `P_(S_C)(H;z_Q)!=0`.
2. At least one diagonal pure class `[e_(C,c)^*]` is nonzero.
3. The pure base quotient in (17) has rank exactly one.
4. A factor-through selector from Theorem 1 exists and has the named nonzero
   physical response.

Equivalently, rank zero is the exact disjunction

```text
b_C in N_C^base       or       P_(S_C)(H;z_Q)=0.      (18)
```

#### Proof

Apply `epsilon_A` to the complete `GLS8` quotient identity.  Its pure columns
are

```text
epsilon_A(d_(S_C,c))=kappa_(A,c)e_(C,c)^*,            (19)
```

and its desired coefficient is `b_C`, giving (16).  The right side is
decomposable, so the left flattening has rank at most one.  The three
`w_(S_C,c)` are independent and all `alpha_c kappa_(A,c)` are nonzero.
Therefore the left side is nonzero exactly when some diagonal class survives,
while the right side is nonzero exactly when both its factors are nonzero.
Theorem 1 supplies the normalized legal selector.  This proves every claimed
equivalence and (18).  `square`

## 4. Exact pointwise source-aligned failure

Let

```text
Lambda=K[z_(q,c)^(+/-1):q in Q,c=0,1,2],
T_Q=Spec Lambda,
h(z)=H_Q(z),                    p(z)=p_(A,Q)(z).       (20)
```

As in `GLS8`, all radicals below are geometric radicals after extending to
the algebraic closure.  Choose fixed bases.  Let `B_C^base(z)` present
`N_C^base(z)` and let

```text
D_C^base=[kappa_(A,0)e_(C,0)^* |
          kappa_(A,1)e_(C,1)^* |
          kappa_(A,2)e_(C,2)^*].                      (21)
```

This matrix has nine rows.  Define

```text
U_C^base={z in T_Q:
 h(z)p(z)!=0 and
 rank[B_C^base(z)|D_C^base]>rank B_C^base(z)}.        (22)
```

By Theorem 3, this is exactly the locus where the source-aligned base shadow
supplies a legal nonzero physical target row.

### Theorem 4 (all-rank base-shadow Fitting criterion)

For fixed `C in binom(U,2)`, the following are equivalent.

1. `U_C^base` is empty.
2. For every `1<=j<=9`,

   ```text
   (h p) I_j([B_C^base|D_C^base])
     subset sqrt_geom(I_j(B_C^base)).                 (23)
   ```

There is no source-aligned useful target for the fixed eligible `(Q,A)` at
any residual point exactly when (23) holds for every `C in binom(U,2)`.
The statement includes the generic nuisance rank, every exceptional rank
drop, every response-zero fibre, and every selector-escape fibre.

#### Proof

At a fibre of nuisance rank `j-1`, adjoining the three pure columns raises
rank exactly when all `j`-minors of `B_C^base` vanish and some `j`-minor of
the augmented matrix does not.  Intersecting this rank-rise locus with
`D(hp)` and applying the Laurent Nullstellensatz gives (23), exactly as in the
`GLS5` and `GLS8` all-rank argument.  Taking the finite intersection over the
source pairs proves the simultaneous statement.  No minor, response, or
incidence coordinate is divided out.  `square`

### Corollary 4.1 (pointwise source failure trichotomy)

At each point of `D(hp)` and for every `C in binom(U,2)`, exactly one of the
following holds after putting the absorption case first:

1. `b_C in N_C^base` (base absorption; the response may be arbitrary);
2. `b_C notin N_C^base` and `P_(S_C)=0` (surviving zero-response row);
3. `b_C notin N_C^base` and `P_(S_C)!=0` (useful legal row).

At least one raw `b_C` is nonzero by Theorem 2, but raw nonvanishing does not
remove either failure branch 1 or 2.

## 5. Root-order interfaces

For `r=3`, `K_0` is one promoted old root and the three pairs
`C in binom(U,2)` give three of the six pair targets in the standard
two-root/four-port `GLD3` shape.  A useful base shadow supplies one legal pair
row.  It does not supply the other five pair rows, the four-port row, a common
seven-row selector, or the three-colour activity gate.

For `r=4`, the six pairs `C in binom(U,2)` give six of the fifteen promoted
four-port targets on `Uhat`; the remaining promoted target is the six-port
top target.  These are not the six pair rows plus four-port row of the
original four-root `GLD3`/`GLD16` chart.

For `r>=5`, the target size is `2r-4`.  No named committed downstream theorem
accepts one such row as a complete detector package.

Thus this theorem integrates the promoted source coefficient with a smaller
legal target quotient at every root order, but it does not turn one-row
attachment into the required downstream common package.

## 6. Proof-DAG consequence and open boundary

The proved edge is

```text
GLS4 source pair and probe pair
 -> GLS8 promoted top-minus-two target family
 -> source-aligned 9-row base quotient
 -> {useful legal row,
     surviving response-zero row,
     swallowed nonzero/raw base circuit}.             (24)
```

`GLS21` proves that the retained all-port nuisance contributes
`p_(A,Q)V_C^*` to every base nuisance.  Hence on the source gate `D(p)` the
base Fitting profile (23) is automatic and the first two displayed branches
collapse to the swallowed-base branch.  Future work must use the uncontracted
`81`-row `GLS8` quotient, a legal joint construction retaining the all-port
label, or complete mixed equations contradicting full upstairs failure.

The following remain **OPEN**:

```text
base-shadow survival on the p!=0 source gate:               CLOSED NO-GO (GLS21);
full 81-row GLS8 survival/nonzero response:                  OPEN;
exclusion of full upstairs simultaneous failure:            OPEN;
r=3 common seven-row package and activity:                  OPEN;
r>=4 named downstream detector:                            OPEN;
GLS15 foreign transport and original-chart synchronization: OPEN;
strategic-node closure:                                    OPEN.
```

The global Krenn--Gu conjecture remains **UNRESOLVED**.

## 7. Verification

Run the focused exact primary verifier:

```bash
python claims/arbitrary-order/verify_maximal_root_surplus_two_promoted_source_aligned_base_shadow_and_target_failure.py
```

Run the independent no-import audit:

```bash
python claims/arbitrary-order/audit_maximal_root_surplus_two_promoted_source_aligned_base_shadow_and_target_failure.py
```

The scripts replay finite exact instances of the Laplace partition,
factor-through selector equivalence, target contraction, failure trichotomy,
and all-rank Fitting logic.  The arbitrary-root proof is the written argument
above; bounded checks do not prove source survival or node closure.
