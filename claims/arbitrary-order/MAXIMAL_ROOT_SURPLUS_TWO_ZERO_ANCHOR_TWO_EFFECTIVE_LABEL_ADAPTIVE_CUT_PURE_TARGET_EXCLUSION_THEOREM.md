# Maximum-root surplus-two zero-anchor two-effective-label adaptive-cut pure-target exclusion theorem

## Status and scope

**Exact characteristic-zero arbitrary-root pointwise exclusion.**  Fix a
`GLS8`-eligible `(Q,A)` chart, a fully supported residual contraction, and the
zero-anchor fibre `omega=0`.  Adjoin the two residual labels to the promoted
ports as in `GLS39`, and call an auxiliary label effective when at least one
of its two root-incidence maps is nonzero on its whole domain.

If at most two auxiliary labels are effective, the complete fixed-residual
physical source has flattening rank at most one across the adaptive cut which
puts `A` and all effective promoted labels on one shore.  The contracted
three-colour GHZ target has rank three across the same cut.  Hence every
target-consistent zero-anchor point has at least three effective auxiliary
labels.  This includes every residual-shore, response, deck-zero, incidence-
rank, and divisor fibre, and it divides by no response or minor.

This is `GLS48`.  It excludes the complete two-effective-label cell,
including the exact rank-five `GLS40` control and any physical deformation
which remains in that cell.  It does **not** exclude rank five with at least
three effective labels, classify ranks five through nine, force a silent
source point into full swallow, supply a legal selector, or close the
strategic node.  The global Krenn--Gu conjecture remains **UNRESOLVED**.

## Dependencies and provenance

The owning interfaces are:

- [`GLS8`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_TWO_PROBE_ONE_TARGET_ATTACHMENT_AND_POINTWISE_FAILURE_REDUCTION_THEOREM.md)
  for `|Uhat|=2r-2>=4`, the promoted chart, and the contracted ternary target;
- [`GLS21`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_BASE_SHADOW_ALL_PORT_NUISANCE_COLLAPSE_THEOREM.md)
  for the raw promoted matching decomposition;
- [`GLS23`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_TRANSVERSE_COMPLETE_NUISANCE_DECOMPOSITION_AND_TOP_ANCHOR_DICHOTOMY_THEOREM.md)
  for complete labelled coefficient slicing;
- [`GLS36`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_INCIDENCE_IMAGE_COMMON_ROW_SILENCE_AND_LABELWISE_LIFT_SHARPNESS_THEOREM.md)
  for the fixed-residual equation `q H+sigma_Q rho_Q=GHZ`; and
- [`GLS39`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_COMPLETE_PAIRWISE_DIAGONAL_FAMILY_RANK_BOUND_AND_MINIMAL_RAW_SWALLOW_EXCLUSION_THEOREM.md)
  for the auxiliary residual labels and the exact identification of every
  residual--residual, residual--port, and port--port coefficient with one
  distinct-label polarization.

No external literature claim is used.  The new content is the adaptive-cut
rank argument and the resulting pointwise three-effective-label floor.  The
argument was motivated by the exact rank-five two-label boundary in `GLS40`;
that control is not used as proof evidence.

## 1. Complete auxiliary family and effective support

Retain

```text
A={a_0,a_1},                    Q={q_0,q_1},
T=Q disjoint-union Uhat,        |Uhat|=2r-2>=4,
E=V_(a_0)^* tensor V_(a_1)^*.
```

For every `t in T`, let `V_t` be its auxiliary domain and let

```text
X_t:V_t -> V_(a_0)^*,          Y_t:V_t -> V_(a_1)^*.
```

The residual domains are one-dimensional, with the maps defined by the fixed
residual contraction as in `GLS39`.  For distinct labels define

```text
mu_(s,t)(x tensor y)
 =X_s(x) tensor Y_t(y)+X_t(y) tensor Y_s(x).          (1)
```

Thus `mu_(q_0,q_1)` is the root companion `q`, the two residual--port
families are the corresponding components of `sigma_Q`, and the port--port
families are its remaining components.

Define the whole-domain effective support

```text
Act={t in T:X_t!=0 or Y_t!=0}.                        (2)
```

This definition does not choose a vector in any label domain.  If
`t notin Act`, then

```text
mu_(s,t)=0 for every s!=t.                            (3)
```

Consequently, if `|Act|<=2`, at most one unordered pair label in the complete
raw decomposition has a nonzero root coefficient.  This remains true if
that last pair map is itself zero, if its complementary physical deck is
zero, or if its image has arbitrary dimension in `E`.

## 2. Adaptive-cut exclusion

Let

```text
P=Act intersect Uhat,          R=Uhat-P.              (4)
```

Since `|Act|<=2` and `|Uhat|>=4`, the right shore `R` is nonempty.  Consider
the tensor flattening

```text
(A union P) | R.                                      (5)
```

### Theorem 1 (two-effective-label source rank is at most one)

On `omega=0`, if `|Act|<=2`, the complete fixed-residual physical source has
rank at most one across (5).

#### Proof

The `GLS21` raw source is the sum over all unordered two-label sets
`D subset T`.  After the residual vertices are fixed, the `D=Q` term is
`q tensor H`, and every other term is the corresponding component of
`sigma_Q rho_Q` in the `GLS36` equation.

By (3), every term vanishes unless both endpoints of `D` lie in `Act`.
There is at most one such `D`.  If there is none, the source is zero.  If
there is one, then `D` contains every effective promoted label, so its root
coefficient and all its open promoted variables lie on the `A union P`
shore.  Its complementary physical deck has only promoted variables in
`R` after the residual contraction.  The whole term is therefore one simple
tensor across (5), irrespective of the internal tensor rank of its root
coefficient.  Its flattening rank is at most one.  The zero-anchor hypothesis
removes the separate top `omega` term, so there are no other source terms.
`square`

### Theorem 2 (the GHZ target has adaptive-cut rank three)

At a fully supported residual contraction, the exact target is

```text
sum_(c=0)^2 alpha_c
  (r_c tensor (e_c^*)^(tensor P))
  tensor (e_c^*)^(tensor R),                          (6)
```

where every `alpha_c` is nonzero.  Its rank across (5) is exactly three.

#### Proof

The three left factors in (6) are independent because their restrictions to
the two root-probe modes are the independent diagonal tensors
`r_0,r_1,r_2`.  The right factors are independent because `R` is nonempty
and the three pure colour words on any nonempty ternary tensor product are
independent.  Nonzero rescaling by the `alpha_c` preserves rank. `square`

### Corollary 2.1 (pointwise three-effective-label floor)

Every exact target-consistent zero-anchor fixed-residual point satisfies

```text
|Act|>=3.                                             (7)
```

In particular, no zero-anchor full-swallow point of rank five through nine
can lie in the complete two-effective-label cell.

#### Proof

If `|Act|<=2`, Theorems 1 and 2 assign ranks at most one and exactly three to
the two equal sides of the same physical target equation, a contradiction.
The proof is pointwise and uses no rank-open condition. `square`

## 3. Exact case cover and boundary

For clarity, the support cases used above are exhaustive:

```text
effective labels               only possible nonzero raw pair
0 or 1                         none
{q_0,q_1}                      q tensor H
{q_s,u}                        sigma_(s,u) with its deck
{u,v}                          sigma_(u,v) with its deck
```

The two-label set may also have a zero polarization or zero deck, which only
lowers the source rank.  Residual labels are not physical promoted ports and
are not incorrectly placed on either shore: they have already been evaluated
in the fixed-residual equation.  The cut retains at least two inactive
promoted ports when `r=3`, and more at higher order.

The exact frontier after this theorem is

```text
zero-anchor target point with <=2 effective labels:       EXCLUDED;
GLS40 rank-five two-label control made physical:           IMPOSSIBLE;
rank-five full swallow with >=3 effective labels:          OPEN;
ranks six through nine full swallow:                       OPEN;
silent source necessarily enters full swallow:             UNKNOWN;
raw escape supplies an original legal target package:      NOT SUPPLIED;
nonzero-anchor marginal/double-transverse branches:         OPEN;
selector/response/activity/synchronization/nuisance gates:  OPEN;
arbitrary-root strategic-node closure:                      UNKNOWN;
global Krenn--Gu conjecture:                                UNRESOLVED.
```

The smallest continuation is target-coupled classification of the
`rank B_Q^anc=5`, `|Act|>=3` full-swallow cell, or a rank-independent
physical identity which either excludes that cell and its higher-rank
successors or produces a complete named downstream attachment package.

## Verification boundary

Run the focused exact primary verifier:

```bash
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_two_effective_label_adaptive_cut_pure_target_exclusion.py
```

It enumerates every effective subset of a six-label auxiliary family with
four promoted ports, checks that at most one raw pair survives, builds the
adaptive flattening, verifies target rank three exactly with SymPy, and
checks the universal rank-one factorization of the sole source term.

Run the independent no-import audit:

```bash
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_two_effective_label_adaptive_cut_pure_target_exclusion.py
```

It independently represents labels as bit masks, reconstructs every
residual/port support case, uses custom exact modular elimination for the GHZ
flattening, and checks the rank-one source minors as formal monomial
cancellations.  Neither script proves the arbitrary-root theorem by finite
enumeration; the proof is the support and flattening argument above.
