# Legal five-port pentad windows: root budget and null-polar sparsity

## Status

**Exact characteristic-zero legality theorem and selector no-go.**  In the
two-residual graph cell behind `P_m`, the corrected pair response is

```text
D_uv=z_uv-hm_uv.                                      (1)
```

For `m=5,6,7`, the residual-present pair `z_uv` lies exactly at the maximal
root-deletion depth and has the correct parity.  The direct pair `m_uv` lies
two deletion levels beyond the accessible staircase and is absent.
Consequently:

- on `h=0`, every corrected pair is root-budget eligible because `D_uv=z_uv`;
- on `h!=0`, one principal root window cannot form the correction (1).

Thus parity does **not** prohibit a five-port pentad on the `h=0` branch.
The obstruction is selector compatibility.

The most natural existing selector is the residual-null polar contraction:
to isolate the pair `{u,v}`, contract every other mode in the common null
space of the two residual rows.  This note proves that, in a genuine
`P_m -> Delta_3` identity, all such contractions together can produce
nonzero corrected blocks on at most **three** mode pairs.  The proof is
independent of whether the null vectors are chosen commonly or separately
for different pairs.  Every monomial of the five-port pentad uses five pair
blocks, so the resulting determinant-cleared pentad is zero term by term.

Therefore the residual-null marked-star/fan construction cannot activate the
new pentad obstruction for `P_5`, `P_6`, or `P_7`.  A complete mixed-label
sensor could still do so: at `P_7` such a graph-side open sensor exists, but
its compatibility with a nonzero GHZ target remains **UNKNOWN**.  The
unrestricted `P_5/P_6/P_7` problems and global Krenn--Gu remain
**UNKNOWN/UNRESOLVED**.

No graph, support, word, matching family, parameter family, field, or tuple
family is enumerated.

## 1. Exact two-residual root budget

Let there be

```text
B: m blocker ports,
Q={q_0,q_1}: two retained residual vertices,
R: r=m-2 probe roots.                                (2)
```

For an even blocker subset `S`, write

```text
z_S=haf G[Q union S],              m_S=haf G[S].      (3)
```

The corrected two-port decomposition at a blocker pair is

```text
z_uv=h m_uv+D_uv,
h=haf G[Q],
D_uv=a_u tensor b_v+b_u tensor a_v.                  (4)
```

Restrict a perfect matching to the `r` roots.  If `j` root--root edges are
used, exactly `r-2j` nonroots are deleted from the complementary principal
hafnian.  This is the mixed-root deletion filtration.

To leave `Q union {u,v}`, the roots delete precisely `B minus {u,v}`, of
order

```text
m-2=r.                                                (5)
```

Hence `z_uv` occurs at the maximal grade `j=0`.  To leave only `{u,v}`, the
roots would have to delete

```text
Q union (B minus {u,v}),
|Q|+m-2=m=r+2,                                       (6)
```

which is impossible.

### Theorem 1 (pair-correction budget and parity)

For every `m>=3` in the two-residual cell:

```text
z_uv: deletion depth r,     eligible at maximal parity grade;
m_uv: deletion depth r+2,   absent from every mixed root word. (7)
```

In particular:

| source | roots | accessible depths | `z_uv` | `m_uv` |
|---|---:|---|---|---|
| `P_5` | 3 | `3,1` | depth 3, eligible | depth 5, absent |
| `P_6` | 4 | `4,2,0` | depth 4, eligible | depth 6, absent |
| `P_7` | 5 | `5,3,1` | depth 5, eligible | depth 7, absent |

Thus `h=0` removes the normalization problem and places every corrected
pair on an allowed grade.  When `h!=0`, forming (1) requires a synchronized
direct-pair depth or some other legal correction mechanism not contained in
one root-deletion family.

Eligibility is not observability.  A root coefficient generally contains a
linear combination of all maximal-depth pair labels, weighted by companion
shore permanents.  A legal five-port pentad requires ten compatible named
pair values, not merely the presence of their ten columns.

## 2. The row-pair polar identity and the colour quota

Work now with an arbitrary multilinear restriction

```text
P_m(phi_1(x_1),...,phi_m(x_m))
 =sum_(c=0)^2 lambda_c product_w x_w[c],
lambda_0 lambda_1 lambda_2 !=0.                      (8)
```

Fix two source rows `p,q`.  At mode `w`, let their local covectors be

```text
a_w=e_p^* composed with phi_w,
b_w=e_q^* composed with phi_w,
A_w=span{a_w,b_w},
K_w=ker a_w intersection ker b_w.                    (9)
```

For each target colour define its incidence neighbourhood

```text
N_c={w:e_c^* belongs to A_w}.                         (10)
```

The standard kernel-deletion argument gives

```text
|N_c|>=2                      for c=0,1,2.            (11)
```

For completeness, suppose `|N_c|<=1`.  Reserve the unique mode of `N_c` when
it exists, and otherwise reserve any one mode.  In every other mode choose
`kappa_w in K_w` with `kappa_w[c]!=0`; this is possible because the relevant
coordinate functional is nonzero on `K_w`.  Put `x_w=e_c` at the reserved
mode.  The target value in (8) is nonzero.  On the permanent side, at least
`m-1` modes now vanish on both rows `p,q`, so they would have to occupy only
the other `m-2` rows.  This is impossible.  Hence (11).

For a mode pair `e={u,v}`, choose arbitrary nonzero

```text
kappa_w^(e) in K_w,             w notin e,            (12)
```

and leave the two modes in `e` open.  Choices for different pairs need not
agree.  Expanding along the selected rows gives

```text
L_e=s_e D_e
   =sum_c lambda_c product_(w notin e) kappa_w^(e)[c]
       e_c^* tensor e_c^*,                            (13)

D_e=a_u tensor b_v+b_u tensor a_v.                   (14)
```

Every competing pair term meets a contracted common-null mode and vanishes
separately.  The scalar `s_e` is the complementary `(m-2)`-row shore
permanent.

## 3. Three-colour sparsity of every null-polar family

### Theorem 2 (at most three nonzero null-polar pair blocks)

Across all mode pairs `e`, and allowing independent choices (12) for every
pair, at most three tensors `L_e` in (13) are nonzero.

### Proof

If `L_e!=0`, at least one diagonal coefficient on the right of (13) is
nonzero.  Choose such a colour `c`.  Then

```text
kappa_w^(e)[c]!=0              for every w notin e.   (15)
```

If `w in N_c`, then `e_c^* in A_w`, so every vector of `K_w` has coordinate
`c` equal to zero.  Equation (15) therefore forces

```text
N_c subset e.                                           (16)
```

The quota (11) and `|e|=2` sharpen this to

```text
N_c=e.                                                  (17)
```

One colour has one fixed neighbourhood, so the same colour cannot certify
two distinct nonzero pair blocks.  Assigning one witnessing colour to every
nonzero `L_e` gives an injection into `{0,1,2}`.  Hence at most three such
pairs exist.

The conclusion applies to tensor blocks before choosing endpoint vectors.
Scalar evaluations can only reduce the number of nonzero pairs.  It also
does not assume that `a_w,b_w` are independent, that `K_w` is a line, that
the shore scalars are nonzero generically, or that the null vectors are
shared between pair contractions.

### Corollary 3 (no nondegenerate null-polar five-port window)

Choose any five modes `U`.  A nondegenerate pentad window would require at
least one Hamiltonian five-cycle `C` in the complete graph on `U` for which
all five selected corrected blocks are nonzero and have nonzero selector
normalizations.  Theorem 2 permits at most three nonzero selected blocks in
the entire mode set.  Therefore no such window exists.

This is stronger than a failure of one fixed marked star: adding every
residual-null polar fan, with pair-dependent null vectors, still cannot
activate one pentad monomial.

The corollary concerns ordinary evaluations of the fixed tensor identity.
Differentiating a shore-zero family in an external graph parameter, or
constructing a limiting selector that recovers `D_e` from a vanishing
`s_eD_e`, would be a new cross-parameter jet mechanism and is not ruled out
here.

## 4. The determinant-cleared weighted pentad is vacuous

Fix five modes `U={1,2,3,4,5}` and, now, choose one common null vector
`kappa_w in K_w` for every mode.  Choose endpoint vectors `x_i` for `i in U`.
For an edge `e={i,j}` of `K_5`, let

```text
d_e=D_e(x_i,x_j),
s_e=the complementary shore permanent at the kappa modes,
l_e=s_e d_e=the legally contracted full-tensor value. (18)
```

Let the twelve signed Hamiltonian cycles in the pentad be `(C,epsilon_C)`.
The ordinary factor-analysis pentad is

```text
P(d)=sum_C epsilon_C product_(e in C)d_e.             (19)
```

Define its denominator-free polar pullback by

```text
P_hat(l,s)=sum_C epsilon_C
  product_(e in C)l_e product_(e notin C)s_e.         (20)
```

### Theorem 4 (exact weighted pullback and termwise collapse)

For arbitrary shore scalars,

```text
P_hat(l,s)=product_(all ten e)s_e times P(d).         (21)
```

Hence a common two-residual channel forces `P_hat=0` without division, even
when some shores vanish.  But in every genuine diagonal target identity (8),
Theorem 2 makes at most three `l_e` nonzero.  Each term in (20) contains five
distinct `l_e`, so

```text
every summand of P_hat is already zero separately.    (22)
```

Thus the null-polar transfer supplies no five-port factor-analysis circuit:
its weighted pentad is a support tautology on the target fibre.

### Proof

Substitute `l_e=s_e d_e` into one summand of (20).  Its two edge products
together contain every one of the ten `s_e` exactly once, leaving the cycle
monomial in `d`.  Factoring out their common product proves (21).  Equation
(22) is Corollary 3.

## 5. What remains legal in P5, P6, and P7

The theorem separates three mechanisms that should not be conflated.

1. **Named maximal-depth labels on `h=0`.**  If a target-compatible mixed-
   root sensor individually exposes the ten values `z_ij` on five named
   blockers with one common labeling, then `D_ij=z_ij` and the ordinary
   pentad is a legal observable equation.  The root budget permits this.
2. **Residual-null polar fans.**  These isolate `s_ijD_ij` by killing all
   competitors termwise, but Theorems 2--4 prove that their simultaneous
   five-port pentad is necessarily vacuous.
3. **The `h!=0` branch.**  The same null contraction kills `D_wj` on a null
   leg but need not kill the direct term `hB_wj`.  Since `m_ij` is below the
   root budget, a synchronized second depth, herald, or target-specific
   cancellation is required before the corrected pentad can be formed.

The present exact status by order is:

- **P5:** maximal-depth corrected pairs are parity-eligible on `h=0`, but
  the selected-label sensor must defeat the known nuisance-column span.  A
  termwise support gate cannot do so.  The null-polar pentad is vacuous.
- **P6:** maximal-depth corrected pairs are parity-eligible on `h=0`.  The
  clean `2 x 3` fan reconstructs six faces of one four-window, not ten common
  pairs on five modes; physical deck integrability and nuisance separation
  remain unknown.  The null-polar pentad is vacuous.
- **P7:** the complete 219-label mixed-root sensor proves that all named
  maximal-depth pairs are simultaneously selectable on a nonempty legal
  graph-side open chart.  The displayed sensor open is disjoint from the
  nonzero diagonal target, and whether the GHZ incidence locus meets a full-
  sensor chart remains unknown.  The null-polar pentad is vacuous on every
  actual target identity.

Therefore the exact surviving pentad route is narrow:

```text
h=0
 + target-compatible named mixed-label sensor
 + five common blocker modes
 -> legal ordinary pentad obstruction.               (23)
```

The root budget and parity allow (23); the currently available target-
compatible selectors do not establish it.

## Scope wall

```text
q=2 corrected pair z_uv at maximal root depth:         PROVED;
q=2 direct pair m_uv two depths beyond budget:         PROVED;
h=0 removes direct-pair normalization:                  PROVED;
P5/P6/P7 corrected pair parity eligibility on h=0:     PROVED;
two-per-colour row-pair incidence quota:                PROVED;
nonzero residual-null polar pair blocks:                AT MOST THREE;
pair-dependent null vectors evade the bound:            FALSE;
nondegenerate five-port null-polar window:               IMPOSSIBLE;
shore-zero parameter-jet desingularization:              UNKNOWN;
weighted determinant-cleared pentad identity:            PROVED;
weighted pentad on a diagonal target null-polar fibre:   TERMWISE ZERO;
P7 graph-side full mixed-label sensor:                   EXISTS PREVIOUSLY;
P7 target-compatible full sensor:                        UNKNOWN;
P5 nuisance-compressed ten-pair sensor:                  UNKNOWN;
P6 physical five-port corrected sensor:                  UNKNOWN;
h!=0 synchronized direct-layer cancellation:             CONDITIONAL ONLY;
unrestricted P5, P6, or P7 nonrestriction:               UNKNOWN;
global Krenn--Gu conjecture:                              UNRESOLVED.
```

## Replay

Run from the repository root:

```powershell
uv run --with sympy python verify_legal_five_port_pentad_window_root_budget_and_null_polar_sparsity.py
python audit_legal_five_port_pentad_window_root_budget_and_null_polar_sparsity.py
python -m py_compile verify_legal_five_port_pentad_window_root_budget_and_null_polar_sparsity.py audit_legal_five_port_pentad_window_root_budget_and_null_polar_sparsity.py
uv run --with ruff ruff check verify_legal_five_port_pentad_window_root_budget_and_null_polar_sparsity.py audit_legal_five_port_pentad_window_root_budget_and_null_polar_sparsity.py
```

The primary verifier checks the exact P5/P6/P7 depth ledger, the
determinant-cleared pentad pullback, the three-colour neighbourhood injection,
and a fixed symbolic null-polar contraction.  The independent no-import audit
uses a separate sparse polynomial dictionary, direct set logic, and exact
integer bilinear contractions.  Neither replay searches supports, graphs,
words, matchings, fields, or parameters.

## Dependencies

- `RESIDUAL_TWO_PORT_FACTOR_ANALYSIS_IDEAL_AND_FIVE_PORT_PENTAD_THEOREM.md`
- `MIXED_ROOT_DELETION_FILTRATION_AND_HERALD_FREE_PAIR_NO_GO.md`
- `P7_RESIDUAL_NULL_POLAR_SELECTOR_H0_THEOREM.md`
- `ARBITRARY_PERMANENT_FIVE_MODE_ROW_PAIR_INCIDENCE_THEOREM.md`
- `P7_FULL_MIXED_ROOT_219_LABEL_SENSOR_AND_PINNED_STAR_GATING_BOUNDARY.md`
- `P6_CLEAN_TWO_BY_THREE_SELECTOR_SEGRE_PULLBACK_AND_TORUS_PERMISSION_THEOREM.md`
