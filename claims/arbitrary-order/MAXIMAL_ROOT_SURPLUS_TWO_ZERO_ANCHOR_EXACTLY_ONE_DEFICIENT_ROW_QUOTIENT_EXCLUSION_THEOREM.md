# Maximum-root surplus-two zero-anchor exactly-one-deficient row-quotient exclusion

## Status and scope

**Exact characteristic-zero root-order-three source-branch exclusion
(`GLS62`).**  Work in the complete zero-anchor same-source tensor hierarchy
of `GLS61`, and assume all six auxiliary labels are torus-rigid.  If exactly
one joint probe map is deficient, quotient its open covector slot by its
joint row space while quotienting every injective pure-probe-axis slot by
its active full-row line.  The hierarchy first forces at least three
distinct injective nonaxis zero labels for every coordinate visible on the
deficient kernel.  Disjointness of the injective nonaxis zero sets then
forces the deficient map to have rank two with a pure-coordinate kernel.
The remaining zero, one, and two pure-axis cases are all contradictory.

Consequently, on the all-six-rigid, zero-anchor, root-order-three branch,
every hypothetical witness has **at least two deficient joint probe maps**.
This excludes the complete exactly-one-deficient branch.  It does not
exclude any branch with two or more deficient maps, the unique-nonrigid
branch, nonzero anchor, arbitrary-root attachment, response, selector,
synchronization, activity, or the global conjecture.  The global Krenn--Gu
status remains **UNRESOLVED**.

## Dependencies and provenance

- [`GLS8`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_TWO_PROBE_ONE_TARGET_ATTACHMENT_AND_POINTWISE_FAILURE_REDUCTION_THEOREM.md)
  owns the complete promoted two-probe physical identity.
- [`GLS23`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_TRANSVERSE_COMPLETE_NUISANCE_DECOMPOSITION_AND_TOP_ANCHOR_DICHOTOMY_THEOREM.md)
  owns the zero-anchor branch.
- [`GLS55`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_TORUS_KERNEL_CONTRACTION_AND_FIVE_RIGID_LABEL_FLOOR_THEOREM.md)
  owns torus rigidity and the rigid rank classification.
- [`GLS58`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_ALL_RIGID_KERNEL_CONTRACTION_AND_CROSS_PRODUCT_REDUCTION_THEOREM.md)
  owns the deficient-kernel support classification and the cross-product
  definition.
- [`GLS61`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_CROSS_PRODUCT_PARTIAL_UNCONTRACTION_AND_INJECTIVE_NONAXIS_EXCLUSION_THEOREM.md)
  owns the complete partial-uncontraction hierarchy, the one-zero-coordinate
  classification for injective nonaxis labels, and the same-colour
  nonaxis-pair orientation obstruction.

The new step uses several members of the one **same-graph** hierarchy.  All
complementary decks below are evaluations of the original physical
`H`-tensors.  They are never replaced by independently chosen local tensors.
No response, selector, cross-product coordinate, physical deck, or target
coefficient is divided by.

## 1. Same-source hierarchy and the exactly-one-deficient profile

Let `Bhat` be the six auxiliary labels at promoted root order three.  For
independent probe variables `z_0,z_1`, put

```text
p_t=X_t(z_0,-),       q_t=Y_t(z_1,-),
k_t=p_t cross q_t.                                      (1)
```

For every open set `S subseteq Bhat`, `GLS61` proves

```text
sum_(D in binom(S,2))
  g_D(z_0,z_1)
    tensor H_(Bhat-D)(k_(Bhat-S),-_(S-D))

 =sum_(a=0)^2 mu_a z_(0,a)z_(1,a)
      product_(t in Bhat-S)(k_t)_a
      tensor_(s in S)e_(s,a)^*.                       (2)
```

Here

```text
g_(su)=p_s tensor q_u+q_s tensor p_u,                 (3)
```

with the canonical labelled-factor order, and every `mu_a` is nonzero.
Equation (2) is an identity over the ambient polynomial ring.  We embed it
in its fraction field `F` only to take the quotients below; all zero-factor
deductions are made before any pointwise specialization.

Assume exactly one label `n` is deficient:

```text
rank J_n<3,             J_n=(X_n,Y_n),
rank J_u=3              for u!=n.                    (4)
```

All six labels remain torus-rigid.  Among the five injective labels, let

```text
P={pure-probe-axis labels},
U=Bhat-({n} union P).                                  (5)
```

Thus every `u in U` is injective and nonaxis.  Define

```text
A_n={a : e_(n,a)^*|_(K_n) !=0},       K_n=ker J_n,
E_a={u in U : (k_u)_a is the zero polynomial}.        (6)
```

The sets `E_0,E_1,E_2` are pairwise disjoint: `GLS61` proves that an
injective nonaxis label has at most one identically zero cross-product
coordinate.

## 2. Row-space and active-line quotients

Extend all covector spaces to `F`.  At the deficient label set

```text
rho_n: V_n^* tensor F
       -> (V_n^* tensor F)/(row J_n tensor F).         (7)
```

Ordinary annihilator duality gives

```text
rho_n(e_(n,a)^*)!=0  iff  a in A_n.                   (8)
```

For `p in P`, let `a_p` be its active full-row probe covector, as in
`GLS61`: if `X_p=0`, then `a_p=q_p`, and if `Y_p=0`, then `a_p=p_p`.
Put

```text
pi_p: V_p^* tensor F -> (V_p^* tensor F)/(F a_p).     (9)
```

Full row space implies that `a_p` is not proportional over `F` to a fixed
coordinate covector, so

```text
pi_p(e_(p,a)^*)!=0             for every a.           (10)
```

### Lemma 1 (companion annihilation)

Apply `rho_n` and all the `pi_p` to their corresponding open slots in (2).
Every retained pair companion meeting `{n} union P` is killed.

### Proof

If `D` meets `n`, its `n`-shore is either `p_n` or `q_n`, hence lies in
`row J_n` and is killed by `rho_n`.  If `D` meets a pure-axis label, every
nonzero companion has the active line `F a_p` in that labelled factor and
is killed by `pi_p`; same-type pure-axis pairs are already zero.  The killed
factor lies in the physical companion, separate from its complementary
deck.  No deck value can evade the quotient. `square`

If `U` were empty, take `S=Bhat` in (2) and apply only the five active-line
quotients.  Every source pair meets `P` and is killed.  The untouched
`n`-slot separates the three nonzero target colours, and every coordinate
survives every active quotient by (10), a contradiction.  Henceforth

```text
U!=empty.                                               (11)
```

## 3. Three nonaxis zeros for every deficient-kernel colour

### Lemma 2 (supported two-zero floor)

For every `a in A_n`,

```text
|E_a|>=2.                                               (12)
```

### Proof

Suppose `|E_a|<=1`.  Choose `u in U` with `E_a subseteq {u}`; when `E_a`
is empty, choose any `u`.  Use (2) with

```text
S=P union {n,u}.                                       (13)
```

After applying `rho_n` and every active-line quotient, Lemma 1 kills every
source pair because `u` is the only open nonaxis label.  The colour-`a`
target coefficient is nonzero: all its nonaxis zero labels are open, and
pure-axis labels and `n` are not cross-product contracted.  Its tensor
factor is nonzero by (8), (10), and the untouched coordinate covector at
`u`.  Projecting the `u`-slot to coordinate `a` isolates this term from all
other colours.  The zero source therefore equals a nonzero target, a
contradiction. `square`

### Lemma 3 (two-zero pair obstruction)

For every `a in A_n`,

```text
|E_a|!=2.                                               (14)
```

### Proof

Suppose `E_a={u,v}`.  Use (2) with

```text
S=P union {n,u,v}                                      (15)
```

and apply the same quotients.  By Lemma 1, the only source pair that can
remain is `D={u,v}`.  Write its projected same-source deck as
`Hbar_(uv)`.  The colour-`a` target survives and is nonzero.

Every other target colour is zero after the quotients.  If `b notin A_n`,
its `n`-coordinate is killed by `rho_n`.  If `b in A_n-{a}`, Lemma 2 gives
at least two members of `E_b`; disjointness puts all of them in the
contracted set `U-{u,v}`, so its scalar coefficient vanishes.  Thus (15)
becomes, up to the canonical factor permutation,

```text
g_(uv) tensor Hbar_(uv)
 =lambda_a e_(u,a)^* tensor e_(v,a)^*
    tensor rho_n(e_(n,a)^*)
    tensor tensor_(p in P)pi_p(e_(p,a)^*),
lambda_a!=0.                                           (16)
```

The right side is nonzero, so both `g_(uv)` and `Hbar_(uv)` are nonzero.
Apply an `F`-linear functional nonzero on `Hbar_(uv)`.  Equation (16) forces
`g_(uv)` to be supported only at `(a,a)`.  But `u,v` are injective nonaxis
labels with zero cross-product coordinate `a`, and `GLS61` Lemma 5 proves
that all four possible shore-orientation pairs have a nonzero off-`(a,a)`
projection.  Contradiction. `square`

Combining Lemmas 2--3 gives the load-bearing strengthening

```text
|E_a|>=3              for every a in A_n.             (17)
```

## 4. The deficient map has a pure-coordinate kernel

Because the `E_a` are disjoint subsets of the five-element injective label
set, (17) implies

```text
|A_n|=1.                                                (18)
```

Indeed, two visible kernel colours would require six distinct labels in
`U`.  Rank zero is impossible because `GLS55` proves that a rank-zero joint
map is not torus-rigid.  A rigid rank-one map has a coordinate-plane kernel
and hence `|A_n|=2`.  A rigid rank-two map has a kernel line whose support is
one or two.  Therefore (18) forces, after renaming colours,

```text
rank J_n=2,
K_n=K e_c,
row J_n=span{e_d^*,e_e^*},      {c,d,e}={0,1,2}.       (19)
```

Moreover (17) gives `|U|>=3`, so

```text
|P|<=2.                                                 (20)
```

It remains to exclude the three possible pure-axis counts.

## 5. No pure-axis labels

Assume `P=empty`, so `|U|=5`.  Use (2) with `S={n}`.  There are no retained
source pairs.  The three coordinate covectors at the untouched `n`-slot are
linearly independent, so every target-colour product over `U` must vanish:

```text
E_c,E_d,E_e are all nonempty.                          (21)
```

Together with (17), disjointness and `|U|=5` force

```text
|E_c|=3,        |E_d|=|E_e|=1.                        (22)
```

Write `E_d={u}` and use (2) with `S={n,u}`.  The colour `d` is the only
surviving target colour: its sole zero is open, while a zero for each other
colour remains contracted.  The complementary deck is now a scalar
`h_(nu)`, and

```text
h_(nu) g_(nu)=lambda_d e_(n,d)^* tensor e_(u,d)^*,
lambda_d!=0.                                           (23)
```

Thus `h_(nu)` is nonzero and `g_(nu)` would have to be pure at `(d,d)`.

### Lemma 4 (rank-two/nonaxis companion obstruction)

Under (19), if an injective nonaxis label `u` has `(k_u)_d=0`, then
`g_(nu)` cannot be a nonzero tensor supported only at `(d,d)`.

### Proof

Suppose first that `u` has the `X`-orientation at `d`.  Then `p_u` is a
nonzero polynomial covector on the `d`-axis and the projection of `q_u` off
that axis is nonzero and spans the complementary two-space.  Project the
`u`-factor of

```text
g_(nu)=p_n tensor q_u+q_n tensor p_u                  (24)
```

off the `d`-axis.  Purity would give

```text
p_n tensor pi_d(q_u)=0,
```

so `p_n=0`.  Hence `row Y_n=row J_n` has dimension two.  Equation (24)
reduces to `q_n tensor p_u`; purity at `(d,d)` then forces all of `row Y_n`
onto the `d`-axis, a contradiction.  The `Y`-orientation is symmetric.
The claims that the pure shore and opposite projection are nonzero include
the zero-shore boundaries: a zero pure shore would make the injective label
a pure-probe axis, which `u` is not. `square`

Lemma 4 contradicts (23), so `P=empty` is impossible.

## 6. One pure-axis label

Assume `P={p}`, so `|U|=4`.  Use (2) with `S={n,p}` and apply only the
active-line quotient `pi_p`; do **not** quotient the `n`-slot.  The sole
source companion meets `p` and is killed.  A target colour survives exactly
when its `E`-set is empty.  The untouched coordinate covectors at `n`
separate the surviving colours, and (10) keeps each pure-axis coordinate
nonzero.  Hence the zero source forces

```text
E_c,E_d,E_e are all nonempty.                          (25)
```

But (17) says `|E_c|>=3`, so the three disjoint sets in (25) would contain
at least five elements of the four-element set `U`.  Contradiction.

## 7. Two pure-axis labels

Assume `P={p,q}`, so `|U|=3`.  Equation (17) forces

```text
E_c=U,           E_d=E_e=empty.                       (26)
```

Use (2) with `S={n,p,q}` and apply only `pi_p tensor pi_q`.  Every retained
pair meets a pure-axis label and is killed.  The colour-`c` target is killed
by the three contracted nonaxis cross products, while the `d` and `e`
coefficients are nonzero.  The untouched `n`-coordinate separates those two
terms, and their pure-axis coordinate factors survive both quotients.  Thus
the target is nonzero while the source is zero, a contradiction.

### Theorem 5 (exactly-one-deficient exclusion)

There is no complete zero-anchor root-order-three witness for which all six
auxiliary labels are torus-rigid and exactly one joint probe map is
deficient.

### Corollary 5.1 (two-deficient floor)

On the all-six-rigid zero-anchor root-order-three branch, every hypothetical
witness has at least two deficient joint probe maps.

### Proof

`GLS61` excludes the no-deficient branch.  Theorem 5 excludes the
exactly-one-deficient branch. `square`

## 8. Sharp boundary and remaining obstruction

The proof is deliberately an exclusion of one exhaustive rank-profile
cell.  It does not say that a two-kernel contraction has three target
colours.  For deficient labels `n,m` and kernel vectors `k,l`, the exact
`GLS58` double contraction has target support

```text
supp(k) intersect supp(l),                             (27)
```

which is zero, mono, or binary on the rigid branch.  The accepted
three-colour six-vertex theorem therefore does not exclude it.  Nor do
pairwise contractions automatically synchronize the different kernel
choices or physical decks.

The next same-source parent obligation is to characterize the common kernel
of the one-, two-, and higher-deficient members of (2), retaining the
bilinear shared-edge polarization and all common physical `H`-tensors.  A
successful continuation must obtain either an exhaustive honest lower-order
GHZ/permanent restriction or a proved nonzero promoted receiver with its
response, selector, synchronization, nuisance-survival, activity, and anchor
gates.  A collection of independent mono/binary restrictions is not source
integrability.

The following remain open:

- every all-six-rigid profile with at least two deficient maps;
- the unique-nonrigid branch and its mono/binary overlap descents;
- nonzero anchor and silent `p=0` source coverage;
- complete-nuisance survival, normalized selectors, response
  synchronization/activity, and entry to a named downstream detector;
- promoted root order at least four;
- any global proof or exact counterexample.

## 9. Exact frontier

```text
GLS61 all-injective r=3 branch:                         EXCLUDED;
exactly-one-deficient all-six-rigid r=3 branch:         EXCLUDED;
all-six-rigid r=3 deficient-map floor:                  at least two;
two-or-more-deficient same-source overlap:              OPEN;
unique-nonrigid branch:                                 OPEN;
response/selector/synchronization/activity package:     OPEN;
nonzero-anchor and arbitrary-root strategic node:       OPEN;
global Krenn--Gu conjecture:                             UNRESOLVED. (28)
```

## 10. Verification boundary

The primary verifier independently enumerates the finite zero-incidence
cover and checks the quotient/orientation lemmas with exact algebra.  The
independent audit uses only the Python standard library, shares no project
imports, and derives the same exhaustive profile count by a separate route.
These scripts audit the finite/support and displayed linear-algebra leaves;
the written same-source tensor argument remains the proof.

From repository root run

```powershell
uv run --with sympy python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_exactly_one_deficient_row_quotient_exclusion.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_exactly_one_deficient_row_quotient_exclusion.py
python -m py_compile claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_exactly_one_deficient_row_quotient_exclusion.py claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_exactly_one_deficient_row_quotient_exclusion.py
uv run --with ruff ruff check claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_exactly_one_deficient_row_quotient_exclusion.py claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_exactly_one_deficient_row_quotient_exclusion.py
uv run --with ruff ruff format --check claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_exactly_one_deficient_row_quotient_exclusion.py claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_exactly_one_deficient_row_quotient_exclusion.py
```
