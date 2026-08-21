# Maximum-root surplus-two physical pair-companion transform and projective synchronization obstruction

## Status

**Exact characteristic-zero physical companion-exchange and joint-module
theorem.**  The result applies at every root order `r>=2`.  It identifies the
two desired columns of each fixed-`Q` pair target as images of two physical
root-pair arrays under one and the same partial-matching transform.  On a
rank-one joint quotient, the projective selector direction is therefore
equivalent to absorption of one explicit root-pair pencil member.

For two rank-one pair targets, applying the absorbed direction of one target
to the transform of the other gives a denominator-free determinant class.
That class vanishes exactly when the two selector lines agree.  On a
hypothetical witness it also satisfies an exact target-coupled identity with
each active pure GHZ class.

This theorem does **not** prove that the cross-target determinant class is
nuisance, does not force any joint quotient to be nonzero, does not attach the
four-port row at `r=4`, and does not force selected-response activity.  It
turns projective synchronization into one precise physical transport
obligation, including pure-axis and incidence-rank-drop fibres.  The global
Krenn--Gu conjecture remains **UNRESOLVED**.

## Dependencies and provenance

The physical companion expansion is the one proved in

- [`GLS2`](MAXIMAL_ROOT_SURPLUS_TWO_COMPLETE_DECK_SENSOR_AND_HIGHER_SURPLUS_DEPTH_BOUNDARY_THEOREM.md),

and the complete two-column quotient is the labelled construction of

- [`GLD15`](FIXED_Q_JOINT_MZ_MODULE_QUOTIENT_PAIRED_ATTACHMENT_AND_RANK_ONE_FIBRE_BOUNDARY_THEOREM.md).

The arbitrary-root pair target is also the top-minus-two target isolated by

- [`GLS8`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_TWO_PROBE_ONE_TARGET_ATTACHMENT_AND_POINTWISE_FAILURE_REDUCTION_THEOREM.md).

The new point is to keep the physical root-pair origin of both GLD15 columns,
identify the exact kernel orientation, and compare different pair targets
without choosing a denominator or an incidence minor.  No literature claim is
used.

## 1. One common physical transform

Work over a characteristic-zero field `K`.  Let

```text
R={1,...,r},              |R|=r>=2,
Q={q_0,q_1},              U={u_1,...,u_r},
B=Q disjoint-union U.                                      (1)
```

Every local space is ternary.  Fix residual vectors `z_0,z_1`, leave the root
and port slots open, and write

```text
x_i=W_(i,q_0)(-,z_0) in V_i^*,
y_i=W_(i,q_1)(-,z_1) in V_i^*,
R_ij=W_ij in V_i^* tensor V_j^*,
L_(i,u)=W_(i,u) in V_i^* tensor V_u^*.                    (2)
```

The residual pair produces the effective root-pair array

```text
K_ij^Q=x_i tensor y_j+y_i tensor x_j.                    (3)
```

Both arrays are labelled by the root pairs `ij in binom(R,2)`; no root
evaluation and no division has been made.

Fix a pair target `S in binom(U,2)` and put

```text
C=U-S,                    |C|=r-2.                       (4)
```

For any labelled root-pair array

```text
A=(A_ij)_(ij in binom(R,2)),
A_ij in V_i^* tensor V_j^*,                              (5)
```

define its physical `C`-incidence transform by

```text
Psi_C(A)
 =sum_(ij in binom(R,2)) A_ij tensor
    sum_(sigma:R-{i,j} -> C bijective)
      product_(k in R-{i,j}) L_(k,sigma(k)).              (6)
```

Every factor in (6) is embedded in its labelled root or port slot.  When
`r=2`, the inner empty product is one.  The transform is linear in `A` and is
defined on every incidence-rank stratum.

Let `G_D` denote the physical root companion for the outside set `D`, with the
`Q` slots evaluated at `z_0,z_1` when they occur.

### Theorem 1 (physical pair-companion exchange)

For every pair target `S` and its complement `C`,

```text
G_C=Psi_C(R),
G_(Q union C)(z_Q)=Psi_C(K^Q).                           (7)
```

Consequently, in the complete fixed-`Q` joint quotient of GLD15,

```text
g_S^M=Psi_C(K^Q),             g_S^Z=Psi_C(R).           (8)
```

#### Proof

A matching contributing to `G_C` uses exactly `r-2` root--port edges.  The
two remaining roots have one root--root edge.  Its unordered root pair `ij`
and the bijection from `R-{i,j}` to `C` are unique, giving the first sum in
(7) with multiplicity one.

A matching contributing to `G_(Q union C)` sends every root to one outside
vertex.  The two roots sent to `Q` form a unique unordered pair `ij`.  The two
assignments to `q_0,q_1` give the two summands in (3), and the remaining roots
are bijected to `C`.  This is exactly the second sum in (7), again with
multiplicity one.  Formula (8) is the GLD15 labelling: `I=S` has companion
`G_(Q union C)`, while `I=Q union S` has companion `G_C`.  `square`

The proof is a matching bijection.  It does not assume that `Psi_C` is
injective, that an incidence minor is nonzero, or that the graph is a witness.

## 2. Rank-one absorption is one physical pencil member

For the target `S`, remove both desired labels and retain coefficient slices
of every other labelled deck summand.  Write

```text
N_C^J:=N_S^(MZ) subset L_S^*,
pi_S:L_S^* -> overline L_S=L_S^*/N_C^J,
bar g_M=pi_S(Psi_C(K^Q)),
bar g_Z=pi_S(Psi_C(R)),
k_S=dim span{bar g_M,bar g_Z}.                           (9)
```

The superscript `J` means **joint** and is only a shorter name for the complete
GLD15 nuisance space.  In particular it does not discard a deck label or
replace the full nuisance by a selected ledger.

Let `C_S subset K^2` be the exact GLD15 operator-coefficient space.  When
`k_S=1`, choose its projective direction `(delta_S,eta_S)` so that

```text
C_S=K(delta_S,eta_S).                                  (10)
```

### Theorem 2 (projective quotient-kernel identity)

Assume `k_S=1`.  There is a unique nonzero quotient generator `bar g_S`, up
to scale, for which

```text
bar g_M=delta_S bar g_S,
bar g_Z=eta_S bar g_S.                                 (11)
```

The same direction is characterized by the denominator-free physical
absorption identity

```text
Psi_C(delta_S R-eta_S K^Q) in N_C^J.                  (12)
```

Conversely, if `(delta,eta)!=0`, (12) holds with `(delta,eta)` in place of
`(delta_S,eta_S)`, and at least one of `bar g_M,bar g_Z` is nonzero, then
`k_S=1` and `C_S=K(delta,eta)`.

#### Proof

The GLD15 coefficient space is the row space of the two quotient classes.
At rank one, choose `bar g_S` so that the two columns have coordinates
`delta_S,eta_S`; this proves (11) and (10).  By (8),

```text
pi_S(Psi_C(delta_S R-eta_S K^Q))
 =delta_S bar g_Z-eta_S bar g_M=0,                    (13)
```

which is (12).

Conversely, (12) says `delta bar g_Z=eta bar g_M`.  If the pair of quotient
classes is not zero, its span has dimension one.  The axis cases are included:
`eta=0` forces `bar g_Z=0`, while `delta=0` forces `bar g_M=0`.  In every case
the nonzero row space is exactly `K(delta,eta)`.  `square`

Thus pure `M`, pure `Z`, and every finite slope are one homogeneous statement.
No selector coefficient is normalized.

## 3. The cross-target transport defect

Let `S,T in binom(U,2)` be rank-one targets.  Put

```text
C_S=U-S,                 C_T=U-T,
ell_S=K(delta_S,eta_S),  ell_T=K(delta_T,eta_T),
A_T=delta_T R-eta_T K^Q,
Delta_(T,S)=delta_T eta_S-eta_T delta_S.               (14)
```

The array `A_T` is absorbed by its own transform `Psi_(C_T)` by Theorem 2.
Apply the *same physical array* through the transform for `S`.

### Theorem 3 (denominator-free synchronization obstruction)

In the complete joint quotient for `S`,

```text
[Psi_(C_S)(A_T)]=Delta_(T,S) bar g_S.                  (15)
```

Consequently:

1. `ell_T=ell_S` if and only if

   ```text
   Psi_(C_S)(A_T) in N_(C_S)^J;                        (16)
   ```

2. a finite family of nonzero rank-one pair spaces has one common projective
   line if and only if every foreign absorbed direction transports into every
   target nuisance space;
3. it is enough to check (16) along the edges of any connected comparison
   graph on the targets;
4. if `ell_T!=ell_S`, the cross-target class in (15) is nonzero and spans the
   entire one-dimensional quotient generated by the two desired columns at
   `S`.

#### Proof

Use linearity of `Psi_(C_S)` and (11):

```text
[Psi_(C_S)(A_T)]
 =delta_T bar g_Z-eta_T bar g_M
 =(delta_T eta_S-eta_T delta_S)bar g_S.                (17)
```

Because `bar g_S!=0`, (15) vanishes exactly when the two nonzero vectors
`(delta_T,eta_T)` and `(delta_S,eta_S)` have zero determinant, which is
projective equality.  Equality of projective lines is transitive, proving the
connected-graph criterion.  The last claim is immediate from nonzero scalar
multiplication in a one-dimensional space.  `square`

Equation (15) is the exact missing **transport defect**.  Raw injectivity of
one `Psi_C`, generic response visibility, or the existence of unrelated
functionals does not prove (16): the membership is in the complete physical
nuisance `N_(C_S)^J` and must be obtained from the same graph's companion or
mixed-target equations.

## 4. Complete-target coupling

Now assume the fixed graph and contraction satisfy the complete
hypothetical-witness equation.  For every active residual colour `c`, use the
GLD15 notation

```text
alpha_c!=0,
d_(S,c)=the pure colour-c tensor on R union C,
w_(S,c)=the pure colour-c tensor on S.                  (18)
```

For a rank-one target `S`, let

```text
D_S=delta_S M_S+eta_S Z_S.                             (19)
```

This is the legally attached selected pair response.  Quotienting the full
target equation gives

```text
sum_c alpha_c[d_(S,c)] tensor w_(S,c)
  =bar g_S tensor D_S.                                 (20)
```

### Theorem 4 (target-coupled transport identity)

The tensor `D_S` is diagonal in the GHZ basis and, for every active colour
`c`,

```text
alpha_c[d_(S,c)]=D_S(c,c)bar g_S.                      (21)
```

For every other rank-one pair target `T`, the cross-target class obeys

```text
D_S(c,c)[Psi_(C_S)(A_T)]
 =Delta_(T,S) alpha_c[d_(S,c)]                         (22)
```

in `overline L_S`.  No factor in (22) has been inverted.

In particular, if `D_S(c,c)!=0` and the two selector lines are unequal, then
both the active pure target class and the cross-target transport defect are
nonzero.  Any independent physical proof that the latter lies in `N_(C_S)^J`
would contradict the complete target equation and force synchronization.

#### Proof

The pure tensors `w_(S,c)` are linearly independent and (20) has no mixed
target word.  Comparing target coordinates proves diagonality and (21).
Multiply (15) by `D_S(c,c)` and substitute (21), giving (22).  The final
statement uses only the displayed nonzero scalars.  `square`

This is target coupling, not target exclusion.  Equation (22) identifies the
precise class that a future companion-exchange syzygy must kill.

## 5. Pointwise branch ledger

The theorem does not discard any divisor:

```text
k_S=2:
  separate M/Z selectors already exist by GLD15;

k_S=1, D_S(c,c)!=0:
  (22) detects unequal pair lines by a nonzero pure target class;

k_S=1, D_S=0:
  the module identity (15) remains exact, but the target gives no active
  pure class and no contradiction;

k_S=0:
  both desired columns are swallowed; there is no projective line to compare;

delta_S=0 or eta_S=0:
  pure-axis lines are included in (12)--(22);

rank Psi_C drops or an incidence minor vanishes:
  every identity remains valid, but transport membership (16) is still open;

r=4 four-port target U:
  its desired root companions are quadratic matching expressions rather than
  the linear pair transform (6); its line must still be attached and compared;

r=3 and r>=5:
  Theorems 1--4 apply to every pair target, but no currently named downstream
  theorem accepts only these pair rows as a complete legal package.          (23)
```

Thus this result is not an `r=4` support atlas and not a restriction campaign.
It supplies one arbitrary-root, support-free physical invariant and exposes
the exact remaining synchronization map.

## 6. Exact frontier

```text
arbitrary-r common physical pair transform Psi_C:             PROVED;
g_S^M=Psi_C(K^Q), g_S^Z=Psi_C(R):                             PROVED;
rank-one selector iff one physical pencil member is absorbed: PROVED;
pure-M and pure-Z axes included without division:             PROVED;
cross-target determinant/transport identity:                 PROVED;
connected comparison graph criterion:                        PROVED;
complete-target identity (22):                               PROVED;
identities valid on every incidence/rank-drop fibre:          PROVED;

cross-target transport defect always nuisance:               UNKNOWN;
all pair joint spaces nonzero on every witness:               UNKNOWN;
pair selector lines forced to synchronize:                    UNKNOWN;
four-port line forced and synchronized at r=4:                UNKNOWN;
selected-response three-colour activity:                      UNKNOWN;
rank-zero and response-zero branches excluded:                UNKNOWN;
complete maximum-root supply/attachment node:                 OPEN;
global Krenn--Gu conjecture:                                  UNRESOLVED.     (24)
```

The smallest next obligation is now exact: prove (16), or contradict its
failure through (22), on every actual mixed-target point, while separately
covering `k=0`, response-zero, and the `r=4` four-port line.  A generic
incidence inverse is insufficient because (15)--(22) deliberately retain all
exceptional fibres.

## Verification boundary

From repository root run

```powershell
uv run --with sympy python claims/arbitrary-order/verify_maximal_root_surplus_two_physical_pair_companion_transform_and_projective_synchronization.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_physical_pair_companion_transform_and_projective_synchronization.py
python -m py_compile claims/arbitrary-order/verify_maximal_root_surplus_two_physical_pair_companion_transform_and_projective_synchronization.py claims/arbitrary-order/audit_maximal_root_surplus_two_physical_pair_companion_transform_and_projective_synchronization.py
uv run --with ruff ruff check claims/arbitrary-order/verify_maximal_root_surplus_two_physical_pair_companion_transform_and_projective_synchronization.py claims/arbitrary-order/audit_maximal_root_surplus_two_physical_pair_companion_transform_and_projective_synchronization.py
uv run --with ruff ruff format --check claims/arbitrary-order/verify_maximal_root_surplus_two_physical_pair_companion_transform_and_projective_synchronization.py claims/arbitrary-order/audit_maximal_root_surplus_two_physical_pair_companion_transform_and_projective_synchronization.py
```

The primary verifier independently enumerates the two matching sets in
Theorem 1 through root order seven, checks multiplicity one, and replays the
homogeneous quotient and target identities symbolically.  The no-import audit
uses a separate canonical matching-bijection representation through root order
eight and exact rational projective cases, including both axes.  Neither
script searches graph supports or treats finite replay as the arbitrary-root
proof.

See the
[`2026-08-20 hostile review`](../../docs/audits/MAXIMAL_ROOT_SURPLUS_TWO_PHYSICAL_PAIR_COMPANION_TRANSFORM_AND_PROJECTIVE_SYNCHRONIZATION_REVIEW_2026-08-20.md).
