# Maximum-root surplus-two base-grade pair shadow and cross-target selector annihilation

## Status

**Exact characteristic-zero arbitrary-root companion/module theorem.**  In
the original fixed-`Q` chart of GLS15, maximum-root evaluation sends the two
physical pair columns to

```text
g_S^M |_(x_R)=Pi_S(z_Q),       g_S^Z |_(x_R)=0.
```

It also sends the complete joint nuisance to the coefficient-slice space of
the other order-two deck labels.  Hence a surviving base pair class rules out
joint rank zero and forces every rank-one joint operator line to be the pure
residual-absent line `K(1,0)`.  Conversely, every rank-zero target and every
rank-one target with a nonzero residual-present coefficient produces an
explicit order-two base circuit.  Thus unequal nonzero pair lines cannot occur
unless at least one of the compared pair columns is swallowed already in the
base-grade quotient.

Independently, a legal selector for one pair target annihilates both labelled
columns of every other pair target after contraction over their common
complement slots.  This is an exact cross-target operator constraint on the
same physical graph.  It is **not** the foreign transport membership required
by GLS15: the cross-contraction uses the selector for the receiving target,
whereas membership in the foreign complete nuisance must be tested against
every selector for that foreign target.

The theorem includes all pure axes, all incidence-rank drops, and every root
order `r>=2`; it divides by no response, minor, permanent, or selector
coordinate.  It does not force any base pair class to survive, does not attach
the four-port row, does not force response activity, and does not close the
supply-and-target-attachment node.  The promoted two-probe module of GLS8 is
a different partition and is not covered.  The global Krenn--Gu conjecture
remains **UNRESOLVED**.

## Dependencies and provenance

The companion grade and maximum-root evaluation are from

- [`GLS2`](MAXIMAL_ROOT_SURPLUS_TWO_COMPLETE_DECK_SENSOR_AND_HIGHER_SURPLUS_DEPTH_BOUNDARY_THEOREM.md),

the common physical pair transform is from

- [`GLS15`](MAXIMAL_ROOT_SURPLUS_TWO_PHYSICAL_PAIR_COMPANION_TRANSFORM_AND_PROJECTIVE_SYNCHRONIZATION_OBSTRUCTION_THEOREM.md),

and the complete two-column nuisance quotient and operator rows are from

- [`GLD15`](FIXED_Q_JOINT_MZ_MODULE_QUOTIENT_PAIRED_ATTACHMENT_AND_RANK_ONE_FIBRE_BOUNDARY_THEOREM.md).

No external literature claim is used.  The new content is the exact
base-grade image of the **complete** joint nuisance, the resulting projective
rank trichotomy, and the labelled cross-target annihilation maps.

## 1. Original fixed-Q chart and the base shadow

Work over a characteristic-zero field `K`.  Let

```text
R={1,...,r},              |R|=r>=2,
B=Q disjoint-union U,     |Q|=2,       |U|=r.         (1)
```

Every local space is ternary.  Fix fully supported maximum-root vectors
`x_i`, `i in R`, satisfying

```text
W_ij(x_i,x_j)=0                     for i!=j,          (2)
```

and fix residual vectors `z_Q`.  For a pair target `S in binom(U,2)`, put

```text
C=U-S,
L_S^*=(tensor_(i in R)V_i^*) tensor
      (tensor_(u in C)V_u^*),
epsilon_(x,S):L_S^* -> tensor_(u in C)V_u^*           (3)
```

where `epsilon_(x,S)` contracts every root slot with `x_R`.

Put

```text
xi_i=W_(i,q_0)(-,z_(q_0)),       yi_i=W_(i,q_1)(-,z_(q_1)),
R_ij=W_ij,
K_ij^Q=xi_i tensor yi_j+yi_i tensor xi_j.             (4)
```

and the partial-matching transform `Psi_C`.  The complete GLD15 desired
columns and joint nuisance are

```text
g_S^M=Psi_C(K^Q),       g_S^Z=Psi_C(R),
N_S^J=N_S^(MZ) subset L_S^*.                          (5)
```

Let `Pi_S` be the base-root complementary permanent for the order-two label
`S`.  After the fixed `Q` contraction it is a tensor on `C`:

```text
Pi_S(z_Q)=per(L_u:u in B-S)(z_Q,-_C).
                                                               (6)
```

Define the exact base-grade nuisance shadow

```text
N_S^0=epsilon_(x,S)(N_S^J)
     subset tensor_(u in C)V_u^*.                    (7)
```

Equivalently, `N_S^0` is spanned by the coefficient slices, in the target
factorization `C|S`, of every base-root order-two companion label `P!=S`.
This includes pair labels meeting `Q`; their fixed residual slots are simply
evaluated at `z_Q`.  No pair label is discarded by name other than the desired
label `S`.

### Theorem 1 (complete base-grade shadow)

For every pair target and every fixed residual contraction,

```text
epsilon_(x,S)(g_S^M)=Pi_S(z_Q),
epsilon_(x,S)(g_S^Z)=0,                               (8)
```

and (7) is exactly the other-order-two slice space just described.
Consequently maximum-root evaluation induces a well-defined linear map

```text
bar epsilon_(x,S):
  L_S^*/N_S^J ->
  (tensor_(u in C)V_u^*)/N_S^0                      (9)
```

with

```text
bar g_M |-> [Pi_S(z_Q)],       bar g_Z |-> 0.         (10)
```

#### Proof

The transform `Psi_C(K^Q)` chooses an unordered root pair `ij`, sends those
two roots to the two residual vertices in both possible orders, and bijects
the remaining roots to `C`.  Contracting with `x_R` turns the first factor
into the two-root/two-`Q` permanent and the other factors into root-to-`C`
incidences.  The choice of `ij`, its two residual assignments, and the
remaining bijection are exactly one bijection from all roots to `Q union C`.
Thus every permanent monomial in (6) occurs once, proving the first identity
in (8).

Every summand of `Psi_C(R)` contains one actual root--root edge.  Its value on
`x_R` is zero by (2), proving the second identity.

For a surplus-two deck label `I`, the GLS2 grade rule is

```text
|I|=2+2p,                                             (11)
```

where `p` is the number of root--root edges in its companion.  Maximum-root
evaluation kills every `p>=1` coefficient slice.  The only surviving labels
therefore have `|I|=2`.  In the joint nuisance, `I=S` is removed, while the
other desired label `I=Q union S` has order four and is killed anyway.  Every
other order-two label remains in the nuisance definition, with all of its
target coefficient slices.  This proves the characterization of `N_S^0`.
Equation (9) now follows from the definition (7), and (10) is (8) modulo the
two nuisance spaces.  No rank assumption is used.  `square`

The base shadow is pointwise.  It is weaker than function-field collective
observability and stronger than merely asking whether the raw tensor
`Pi_S(z_Q)` is nonzero.

## 2. Rank-zero and projective-slope localization

Write

```text
pi_S:L_S^* -> overline L_S=L_S^*/N_S^J,
k_S=dim span{bar g_M,bar g_Z},
b_S=[Pi_S(z_Q)] in
    (tensor_(u in C)V_u^*)/N_S^0.                    (12)
```

When `k_S=1`, orient its operator line as in GLS15:

```text
bar g_M=delta_S bar g_S,
bar g_Z=eta_S bar g_S,
C_S=K(delta_S,eta_S),                                (13)
```

with `bar g_S!=0`.  Equivalently,

```text
Psi_C(delta_S R-eta_S K^Q) in N_S^J.                (14)
```

### Theorem 2 (base-survival projective trichotomy)

At every point:

1. if `k_S=0`, then `b_S=0`;
2. if `k_S=1`, then

   ```text
   eta_S b_S=0;                                      (15)
   ```

3. if `b_S!=0`, then exactly one of the following holds:

   ```text
   k_S=1 and C_S=K(1,0),
   k_S=2.                                             (16)
   ```

Thus every rank-zero pair target and every non-pure-`M` rank-one target lies
on the explicit base-swallowing branch `b_S=0`.  If a finite family of pair
targets all has nonzero base class and joint rank one, every operator line in
the family is the common pure-`M` line.  In particular, two unequal nonzero
rank-one lines force `b_S=0` for at least one of the two targets.

#### Proof

If `k_S=0`, then both desired columns belong to `N_S^J`; apply (9) to the
`M` column to obtain `b_S=0`.

For rank one, apply `epsilon_(x,S)` to (14).  The first term vanishes and the
second becomes `-eta_S Pi_S(z_Q)` by Theorem 1.  Modulo `N_S^0` this is
exactly (15).  If `b_S!=0`, rank zero is impossible and (15) forces
`eta_S=0`.  The projective vector in (13) is nonzero, so `delta_S!=0` and its
line is `K(1,0)`.  The only remaining joint rank is two.  Finally, two
different projective lines cannot both equal `K(1,0)`.  `square`

No normalization is needed to prove (15).  The pure-`Z` axis is included: it
has `delta_S=0`, `eta_S!=0`, and therefore forces `b_S=0`.

### Corollary 2.1 (useful pure-M row on an active base pair)

Assume the complete hypothetical-witness equation.  If

```text
b_S!=0,          k_S=1,          H_S!=0,              (17)
```

then the unique operator line is pure `M`, its selected response is a nonzero
multiple of

```text
M_S=H_S,                                             (18)
```

and the pure target quotient has rank one.  Hence this target supplies a
legal normalized constant pure-`M` selector, nonzero response, and its exact
pure GHZ anchor.

#### Proof

Theorem 2 gives `(delta_S,eta_S)=(delta_S,0)` with `delta_S!=0`.
GLD15's witness trichotomy says that a rank-one selected response has pure
quotient rank one exactly when `delta_S M_S+eta_S Z_S` is nonzero.  This is
`delta_S H_S`, nonzero by (17).  Normalize by `delta_S`.  `square`

Condition (17) is not proved universal.  The corollary records the exact
pointwise gate rather than replacing it by raw activity `H_S Pi_S!=0` without
base quotient survival.

## 3. Cross-target annihilation of labelled companion maps

Let `S,T in binom(U,2)` be distinct.  Put

```text
A=S intersect T,       B_ST=S-T,       D_ST=T-S,
E=U-(S union T).                                      (19)
```

Thus `B_ST` and `D_ST` have the same size, either one or two.  Let

```text
lambda_T in L_T=(L_T^*)^*                            (20)
```

be any legal GLD15 operator functional, with coefficient row `(a_T,b_T)`.
Contract `lambda_T` and `g_S^X`, for `X in {M,Z}`, over the common labelled
slots `R union E`.  The remaining tensor is the linear map

```text
X_(T<-S)^X(lambda_T):
 tensor_(u in B_ST)V_u^* -> tensor_(v in D_ST)V_v^*.
                                                               (21)
```

The unchanged common target slots `A` carry an identity map and are omitted
from (21).

### Theorem 3 (foreign-label cross-annihilation)

Every legal target-`T` operator row satisfies

```text
X_(T<-S)^M(lambda_T)=0,
X_(T<-S)^Z(lambda_T)=0                              (22)
```

for every `S!=T`.  Using GLS15, these are equivalently

```text
X_(T<-S)(lambda_T,Psi_(U-S)(K^Q))=0,
X_(T<-S)(lambda_T,Psi_(U-S)(R))=0.                   (23)
```

Hence every linear combination, including every foreign absorbed physical
direction, has zero cross-contraction against `lambda_T`.

#### Proof

The exact operator identity for `lambda_T` is

```text
(lambda_T tensor id_(W_T))Gamma_Q
  =a_T P_T^M+b_T P_T^Z.                              (24)

```

Restrict (24) first to the labelled deck summand `I=S`.  Because `S!=T`, the
right side is zero on that direct summand.  On the left, the companion factor
is `g_S^M`; the slots in `A` pass unchanged from input to output, the slots in
`B_ST` are contracted by `lambda_T`, and the slots in `D_ST` come from
`g_S^M`.  The coefficient map is therefore

```text
id_(tensor_(u in A)V_u^*) tensor X_(T<-S)^M(lambda_T).
```

It is zero for every input, so the second factor is zero.  Restricting (24)
to the distinct label `I=Q union S`, after the fixed `z_Q` evaluation, gives
the same argument for `g_S^Z`.  This proves (22), and (23) is GLS15's
physical companion exchange.  `square`

Theorem 3 is stronger than checking one scalar cross reading, but it is not
foreign nuisance membership.  For example, the GLS15 transport condition
for a direction `A_T` at target `S` is

```text
Psi_(U-S)(A_T) in N_S^J,                             (25)
```

which is equivalent to annihilation by **every** member of `(N_S^J)^perp`.
Equations (22)--(23) instead use a functional belonging to the differently
labelled space `L_T` and leave a map between `S-T` and `T-S`.  There is no
canonical implication from (22) to (25).  Treating them as identical would
silently exchange the target and complement tensor factors.

## 4. Exhaustive pointwise ledger

For each original fixed-`Q` pair target, the new reduction is

```text
b_S!=0:
  k_S=2, or k_S=1 with the pure-M line;
  if additionally H_S!=0 on a witness, a useful pure-M row exists;

b_S=0:
  k_S may be 0, 1, or 2;
  every pure-Z or oblique rank-one line is confined here;

two unequal nonzero rank-one pair lines:
  at least one corresponding base pair class is swallowed;

any simultaneous legal rows:
  all foreign M/Z labelled maps obey the exact cross-annihilations (22),
  but GLS15 transport membership remains a distinct obligation.          (26)
```

This ledger is pointwise on generic and exceptional incidence fibres.  It
does not assert that `N_S^0` has maximal rank, that `Pi_S` is nonzero, or that
any finite family of base classes survives simultaneously.

```text
base shadow g_M -> Pi_S and g_Z -> 0:                       PROVED;
complete joint nuisance shadows to other order-two slices: PROVED;
base survival excludes k=0:                                PROVED;
base survival orients rank one to pure M:                   PROVED;
active base survivor gives useful pure-M witness row:       PROVED;
unequal pair lines force a base-swallowed target:           PROVED;
foreign labelled M/Z cross-annihilation:                    PROVED;
cross-annihilation implies foreign nuisance membership:     NOT PROVED;
one/all required base pair classes survive on every witness: UNKNOWN;
four-port synchronization and selected-response activity:    UNKNOWN;
distinct GLS8 promoted interface:                            OPEN;
complete maximum-root supply/attachment node:                OPEN;
global Krenn--Gu conjecture:                                 UNRESOLVED.      (27)
```

The smallest next obligation is now sharper.  On the nonzero pair-line
branch, either use the common pure-`M` base-survival stratum together with the
four-port/activity gates, or derive a complete mixed-target contradiction
from the explicit base-swallowing circuit forced by every oblique/pure-`Z`
line and every rank-zero target.  The cross maps (22) are additional exact
physical equations available in that contradiction; they do not themselves
supply the missing transport membership.

## Verification boundary

Run from repository root:

```powershell
python claims/arbitrary-order/verify_maximal_root_surplus_two_base_grade_pair_shadow_and_cross_target_selector_annihilation.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_base_grade_pair_shadow_and_cross_target_selector_annihilation.py
python -m py_compile claims/arbitrary-order/verify_maximal_root_surplus_two_base_grade_pair_shadow_and_cross_target_selector_annihilation.py claims/arbitrary-order/audit_maximal_root_surplus_two_base_grade_pair_shadow_and_cross_target_selector_annihilation.py
uv run --with ruff ruff check claims/arbitrary-order/verify_maximal_root_surplus_two_base_grade_pair_shadow_and_cross_target_selector_annihilation.py claims/arbitrary-order/audit_maximal_root_surplus_two_base_grade_pair_shadow_and_cross_target_selector_annihilation.py
uv run --with ruff ruff format --check claims/arbitrary-order/verify_maximal_root_surplus_two_base_grade_pair_shadow_and_cross_target_selector_annihilation.py claims/arbitrary-order/audit_maximal_root_surplus_two_base_grade_pair_shadow_and_cross_target_selector_annihilation.py
```

The focused primary verifier enumerates the GLS15 matching bijection and its
maximum-root image through root order seven, checks the grade/nuisance label
census, exhausts projective axes and finite quotient ranks, and checks every
ordered pair-target slot partition.  The independent no-import audit uses a
separate recursive injection/matching representation through root order eight,
bitmask grade bookkeeping, and independently enumerated rational projective
controls.  These bounded programs audit conventions and identities; the
arbitrary-root matching, labelled-direct-summand, and quotient arguments above
are the proofs.
