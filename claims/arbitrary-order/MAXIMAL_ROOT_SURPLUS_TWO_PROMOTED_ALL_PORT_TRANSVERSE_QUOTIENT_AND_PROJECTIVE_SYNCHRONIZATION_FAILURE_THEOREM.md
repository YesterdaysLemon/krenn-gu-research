# Maximum-root surplus-two promoted all-target transverse quotient and projective synchronization failure

## Status

**Exact characteristic-zero arbitrary-root promoted-module theorem.**  On the
required `GLS4` gate `p_(A,Q)!=0`, the `GLS21` all-port nuisance identifies one
common probe-root line

```text
K q,              q=G_Q^A(z_Q),
epsilon_A(q)=p.                                         (1)
```

For every top-minus-two target and the top all-port target of `GLS8`, quotient
this line without deleting its nuisance label.  The denominator-free operator

```text
P_Q=p id_(E_A^*)-q tensor epsilon_A                    (2)
```

kills `q`, has image `ker epsilon_A`, and satisfies `P_Q^2=pP_Q`.  It induces,
after localization at the already-required `p`, an exact isomorphism from the
full `GLS8` coefficient module modulo the all-port nuisance to a transverse
module.  Thus the legal-selector problem is reduced **equivalently**, not just
sufficiently, from `81` to `72` rows for every top-minus-two target and from
`9` to `8` rows for the top target.

For a desired coefficient `g_C`, the exact transverse defect is

```text
t_C=(P_Q tensor id)g_C
   =p g_C-q tensor epsilon_A(g_C).                     (3)
```

Full legal survival is equivalent to survival of `t_C` modulo the projected
complete nuisance.  Applying the same operator to the complete GHZ target
gives an exact rank-one pure quotient and an all-rank geometric
radical--Fitting failure criterion.  For the source Laplace pairs, the
transverse aggregate is

```text
T_Q=p F_Q-q tensor Pi_Q,                               (4)
```

giving an exact fork between a nonzero raw transverse term and an aggregate
projective synchronization identity.

The theorem does **not** force any `t_C` or physical response to survive,
exclude the simultaneous transverse failure profile, provide common selectors
or selected-response activity, or supply a named downstream detector.  It does
not close the strategic node.  The global Krenn--Gu conjecture remains
**UNRESOLVED**.

## Dependencies and provenance

The source pair, common residual gate, and incidence polynomial come from

- [`GLS4`](MAXIMAL_ROOT_SURPLUS_TWO_SAME_PAIR_QUOTIENT_SURVIVAL_AND_COMPLEMENTARY_PERMANENT_DOMINANCE_THEOREM.md); and
- [`GLS6`](MAXIMAL_ROOT_SURPLUS_TWO_COMMON_RESIDUAL_CONTRACTION_AND_AUGMENTED_ALIGNMENT_GATE_THEOREM.md).

The promoted target family, complete nuisance, selector criterion, target
identity, and original all-rank failure profile come from

- [`GLS8`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_TWO_PROBE_ONE_TARGET_ATTACHMENT_AND_POINTWISE_FAILURE_REDUCTION_THEOREM.md).

The source-aligned contraction and the all-port collapse are

- [`GLS20`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_SOURCE_ALIGNED_BASE_SHADOW_AND_TARGET_FAILURE_THEOREM.md); and
- [`GLS21`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_BASE_SHADOW_ALL_PORT_NUISANCE_COLLAPSE_THEOREM.md).

No external literature claim is used.  The new content is the canonical
denominator-free transverse projector, its exact equivalence with the full
legal quotient, the projected target/Fitting identities, and the source
projective-synchronization aggregate.

## 1. Uniform target notation

Retain the promoted `GLS8` partition

```text
E_A^*=tensor_(a in A)V_a^*,          dim E_A^*=9,
Uhat=K_0 disjoint-union U.                              (5)
```

Index the full promoted target family by

```text
C in Cprom={empty} union binom(Uhat,2),
S_C=Uhat-C.                                             (6)
```

For `|C|=2`, put

```text
V_C^*=tensor_(u in C)V_u^*,
L_C^*=E_A^* tensor V_C^*,          dim L_C^*=81,
g_C=G_C^A.                                              (7)
```

For `C=empty`, use `V_empty^*=K` and

```text
L_empty^*=E_A^*,                    dim L_empty^*=9,
g_empty=G_empty^A=W_(a_0,a_1).                         (8)
```

Let `N_C subset L_C^*` be the **complete** `GLS8` nuisance for the target
`S_C`.  For every `C in Cprom`, the distinct active `D=Q` label contributes

```text
H_C^all=q tensor V_C^* subset N_C,                     (9)
q=G_Q^A(z_Q) in E_A^*.
```

For `C=empty`, this means the one-dimensional line `Kq`.  Equation (9) is the
uncontracted form of the `GLS21` all-port nuisance.

Work over the residual Laurent ring and then localize at

```text
p=epsilon_A(q)=p_(A,Q),              p!=0.             (10)
```

No new denominator is introduced.

## 2. Canonical transverse projector

Define `P_Q:E_A^* -> E_A^*` by (2), and for each target define

```text
mathcal P_C=P_Q tensor id_(V_C^*):L_C^* -> L_C^*,
K_C^tr=(ker epsilon_A) tensor V_C^*,
N_C^tr=mathcal P_C(N_C) subset K_C^tr,
t_C=mathcal P_C(g_C).                                  (11)
```

The dimensions are

```text
dim K_C^tr=72       for |C|=2,
dim K_empty^tr=8.                                      (12)
```

### Theorem 1 (projector identities and quotient isomorphism)

On `D(p)`,

```text
P_Q(q)=0,             epsilon_A compose P_Q=0,
P_Q^2=pP_Q,
ker P_Q=Kq,           im P_Q=ker epsilon_A.            (13)
```

Consequently `mathcal P_C` induces an isomorphism

```text
L_C^*/H_C^all  -> K_C^tr                              (14)
```

for every promoted target, and under this isomorphism the class of `g_C`
maps to `t_C`.

#### Proof

For `v in E_A^*`,

```text
P_Q(v)=pv-epsilon_A(v)q.                               (15)
```

Using `epsilon_A(q)=p` gives the first three identities in (13).  If `P_Q(v)=0`
and `p` is invertible, then `v=p^(-1)epsilon_A(v)q`, so the kernel is `Kq`.
If `epsilon_A(v)=0`, then `P_Q(v)=pv`; hence the image is exactly
`ker epsilon_A`.  Tensoring with `V_C^*` gives kernel `q tensor V_C^*`, which
is (9), and proves (14).  `square`

### Theorem 2 (exact full-selector equivalence)

For every promoted target and every point of `D(p)`, the following are
equivalent.

1. The full desired class survives:

   ```text
   [g_C]!=0 in L_C^*/N_C.                              (16)
   ```

2. The transverse desired class survives:

   ```text
   [t_C]!=0 in K_C^tr/N_C^tr.                          (17)
   ```

3. There is a functional `mu_C in (K_C^tr)^*` satisfying

   ```text
   mu_C(N_C^tr)=0,                 mu_C(t_C)=p.         (18)
   ```

4. There is a legal normalized full `GLS8` selector `lambda_C`.

The translations are

```text
lambda_C=p^(-1) mu_C compose mathcal P_C,              (19)
mu_C(mathcal P_C(v))=p lambda_C(v).                    (20)
```

Equation (18) is denominator-free.  Equation (19) divides only by the declared
unit `p` on the source gate.

#### Proof

Because `H_C^all subset N_C`, Theorem 1 identifies the quotient of `L_C^*` by
`N_C` with the quotient of `K_C^tr` by `mathcal P_C(N_C)`.  Explicitly, if
`t_C=mathcal P_C(n)` for `n in N_C`, then
`mathcal P_C(g_C-n)=0`, so `g_C-n in H_C^all subset N_C`; the converse is
immediate.  This proves (16)--(17).  Finite-dimensional separation gives
(17)--(18).  Formula (19) annihilates `N_C` and normalizes `g_C`.  Conversely,
a legal `lambda_C` kills `H_C^all`, so (20) is well-defined on the image of
`mathcal P_C`; it satisfies (18).  The full `GLS8` selector theorem completes
the equivalence.  `square`

Thus `GLS21` does not destroy the full selector problem.  It removes exactly
one common probe-root line and exposes the transverse obstruction that every
legal selector must detect.

## 3. Complete-target transverse identity

Assume the complete ternary GHZ tensor equation.  For `c in {0,1,2}`, let

```text
r_c=e_(a_0,c)^* tensor e_(a_1,c)^* in E_A^*,
kappa_c=epsilon_A(r_c)!=0,
v_(C,c)=tensor_(u in C)e_(u,c)^*,
d_(C,c)=r_c tensor v_(C,c),
d_(C,c)^tr=(p r_c-kappa_c q) tensor v_(C,c).           (21)
```

For `C=empty`, the empty tensor `v_(empty,c)` is `1`.  Let

```text
w_(S_C,c)=tensor_(u in S_C)e_(u,c)^*,
alpha_c=z_(q_0,c)z_(q_1,c).                           (22)
```

Every `alpha_c` is a residual-torus unit.

### Theorem 3 (transverse target coupling)

In `K_C^tr/N_C^tr`,

```text
sum_(c=0)^2 alpha_c[d_(C,c)^tr] tensor w_(S_C,c)
  =[t_C] tensor P_(S_C)(H;z_Q).                       (23)
```

The transverse pure quotient has rank at most one, and the following are
equivalent.

1. `[t_C]!=0` and `P_(S_C)(H;z_Q)!=0`.
2. At least one `[d_(C,c)^tr]` is nonzero.
3. The three transverse pure columns have rank exactly one.
4. A legal full `GLS8` selector exists and has the named nonzero response.

#### Proof

Apply `mathcal P_C` to the complete `GLS8` target quotient.  Equations (3) and
(21) give (23), and the complete nuisance maps to `N_C^tr`.  Its right side is
decomposable.  Since the three `w_(S_C,c)` are independent and the `alpha_c`
are units, its left side is nonzero exactly when a transverse pure class
survives.  Its right side is nonzero exactly when both factors are nonzero.
Theorem 2 supplies the legal selector.  `square`

## 4. Exact all-rank transverse failure

Let `B_C^tr(z)` present `N_C^tr(z)` in fixed bases of `K_C^tr`, and let

```text
D_C^tr=[d_(C,0)^tr|d_(C,1)^tr|d_(C,2)^tr],
h(z)=H_Q(z).                                           (24)
```

Put `k_C=72` for `|C|=2` and `k_empty=8`.  Define

```text
U_C^tr={z:
 h(z)p(z)!=0 and rank[B_C^tr(z)|D_C^tr(z)]
                    >rank B_C^tr(z)}.                 (25)
```

### Theorem 4 (transverse radical--Fitting criterion)

For a fixed promoted target `C`, `U_C^tr` is empty if and only if, for every
`1<=j<=k_C`,

```text
(h p) I_j([B_C^tr|D_C^tr])
  subset sqrt_geom(I_j(B_C^tr)).                      (26)
```

No legal nonzero promoted row exists at any common-gate residual point exactly
when (26) holds for every `C in Cprom`.  This includes all top-minus-two
targets, the top target, every nuisance-rank drop, response-zero fibres, and
every exceptional transverse escape.

#### Proof

Theorem 3 identifies useful legal attachment with rank rise of the transverse
pure matrix.  At nuisance rank `j-1`, rank rises exactly when the `j`-minors of
`B_C^tr` vanish and some augmented `j`-minor does not.  Intersecting with
`D(hp)` and applying the geometric Laurent Nullstellensatz gives (26).  Taking
the finite intersection over `Cprom` proves the simultaneous statement.  No
minor or response coordinate is divided out.  `square`

## 5. Source Laplace synchronization aggregate

For source pairs `C in binom(U,2)`, put

```text
tau_C=Per_(K_0,U-C),
F_Q=sum_C g_C tensor tau_C,
T_Q=sum_C t_C tensor tau_C.                            (27)
```

The `GLS8` source Laplace identity is

```text
Pi_Q=sum_C epsilon_A(g_C) tensor tau_C.                (28)
```

### Theorem 5 (denominator-free projective synchronization fork)

The transverse aggregate satisfies

```text
T_Q=p F_Q-q tensor Pi_Q,
(epsilon_A tensor id)(T_Q)=0.                         (29)
```

Therefore exactly one of the following holds.

1. `T_Q!=0`; then at least one source term `t_C tensor tau_C` is nonzero, so
   at least one raw transverse desired coefficient `t_C` is nonzero.
2. `T_Q=0`; then the source aggregate obeys the projective synchronization

   ```text
   p F_Q=q tensor Pi_Q.                                (30)
   ```

If every individual `t_C` vanishes, then the stronger identities

```text
p g_C=q tensor epsilon_A(g_C)                         (31)
```

hold for all source pairs.  No converse from (30) to (31) is asserted.

#### Proof

Substitute (3) into (27) and use (28), giving the first identity in (29).
Applying `epsilon_A` gives `pPi_Q-pPi_Q=0`.  If the sum is nonzero, some
summand is nonzero.  If it is zero, rearrangement gives (30).  Individual
vanishing gives (31) termwise.  `square`

The source theorem proves `Pi_Q!=0`, but this does not decide which branch of
the fork occurs and does not prove survival modulo `N_C^tr`.

## 6. Small-root and downstream interfaces

At `r=3`, the transverse reduction covers all six promoted pair targets with
`72` rows and the promoted four-port top target with `8` rows.  It is exactly
equivalent to the full individual `GLS8` selector problem on `D(p)`.  It does
not force one common selector across all seven targets or the three-colour
activity required by `GLD3`.

At `r=4`, it covers all fifteen promoted four-port targets and the promoted
six-port top target.  These are still not the original six-pair plus four-port
`GLD3`/`GLD16` family.

For `r>=5`, the exact top-minus-two target size is `2r-4`; no named committed
downstream theorem accepts one transverse row as a complete package.

## 7. Proof-DAG consequence and open boundary

The corrected promoted route is

```text
GLS8 complete 81/9-row target quotient
 -> GLS21 common all-port nuisance line Kq
 -> GLS22 exact 72/8-row transverse quotient
 -> {useful full legal row,
     transverse absorption,
     transverse survival with response zero}.         (32)
```

The smallest remaining promoted obligation is now to contradict the
simultaneous transverse Fitting profile (26) with complete mixed GHZ
coefficients, or to prove enough transverse rows useful at one shared point
and assemble every gate of a named downstream detector.  The aggregate fork
(29)--(30) supplies the exact source projective-synchronization split; it is
not itself an exclusion.

The subsequent
[`GLS23` complete-nuisance theorem](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_TRANSVERSE_COMPLETE_NUISANCE_DECOMPOSITION_AND_TOP_ANCHOR_DICHOTOMY_THEOREM.md)
expands every projected nuisance label into an exact physical coefficient-slice
space and isolates the common top-anchor dichotomy.  It refines the failure
topology but does not exclude the simultaneous profile or supply a downstream
package.

The following remain **OPEN**:

```text
nonzero/surviving transverse source coefficient:           OPEN;
nonzero response for a surviving transverse target:        OPEN;
exclusion of simultaneous transverse failure:              OPEN;
r=3 common seven-row synchronization and activity:          OPEN;
r>=4 named promoted downstream package:                    OPEN;
original-chart GLS15 transport and coexistence:             OPEN;
strategic-node closure:                                    OPEN.
```

The global Krenn--Gu conjecture remains **UNRESOLVED**.

## 8. Verification

Run the focused exact primary verifier:

```bash
python claims/arbitrary-order/verify_maximal_root_surplus_two_promoted_all_port_transverse_quotient_and_projective_synchronization_failure.py
```

Run the independent no-import audit:

```bash
python claims/arbitrary-order/audit_maximal_root_surplus_two_promoted_all_port_transverse_quotient_and_projective_synchronization_failure.py
```

The scripts replay the projector algebra, quotient/selector equivalence,
transverse target rank, Fitting strata, source aggregate, and all-target
dimension counts.  The arbitrary-root proof is the written argument above;
bounded checks do not prove transverse survival or node closure.
