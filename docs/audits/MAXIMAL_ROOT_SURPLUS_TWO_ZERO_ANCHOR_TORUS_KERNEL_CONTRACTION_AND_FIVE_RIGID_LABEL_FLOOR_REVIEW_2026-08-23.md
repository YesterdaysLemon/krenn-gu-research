# Hostile review: zero-anchor torus-kernel contraction and five-rigid-label floor

## Verdict

**ACCEPT after hostile mathematical review, focused exact verification,
genuinely independent no-import audit, exact source-interface correction, and
authenticated six-vertex dependency replay.**

`GLS55` proves that every actual characteristic-zero zero-anchor promoted
chart has at least five auxiliary labels whose full joint two-probe incidence
kernel contains no fully supported local vector.  Equivalently, each of
those labels has some target coordinate covector in the row span of its full
joint probe-incidence map.

This strengthens `GLS54`: the five labels are active at every fully supported
residual point.  It does not assume full swallow or start from one evaluated
residual equation.

The coordinate readouts are local and label-dependent.  They are not physical
responses, constant normalized target selectors, complete-nuisance
annihilators, synchronized projective rows, or target-pure anchors.  The
maximum-root supply-and-target-attachment node and the global Krenn--Gu
conjecture remain **UNRESOLVED**.

## Reviewed artifacts and exact owners

- [`GLS55 theorem`](../../claims/arbitrary-order/MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_TORUS_KERNEL_CONTRACTION_AND_FIVE_RIGID_LABEL_FLOOR_THEOREM.md)
- [`focused exact primary verifier`](../../claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_torus_kernel_contraction_and_five_rigid_label_floor.py)
- [`independent no-import audit`](../../claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_torus_kernel_contraction_and_five_rigid_label_floor.py)
- complete uncontracted two-probe identity and physical typing: `GLS8`
- accepted
  [`six-vertex theorem`](../../claims/finite/n06/SIX_VERTEX_CERTIFICATE.md)
- comparison-only predecessor: `GLS54`
- current-frontier, node-DAG, and arbitrary-order README updates.

The complete identity is owned by `GLS8`, not `GLS21`.  `GLS54` is not a
load-bearing dependency: the hostile audits found a stronger proof that
chooses the four open labels directly from the full auxiliary set and
contracts every outside non-rigid label at its own full-map kernel vector.

## Quantifier and typing audit

For every residual or promoted label `t`, the theorem uses the original full
physical map

```text
J_t=(W_(a_0,t),W_(a_1,t))
  :V_t -> V_(a_0)^* direct-sum V_(a_1)^*.
```

For a residual label this is not the one-dimensional evaluated auxiliary map
used in `GLS39`.  Rigidity is a property of this full map and is independent
of a residual contraction point.

If at most four labels are rigid, choose any four-set `P` containing all of
them.  Every outside label `t` is non-rigid, so its own fully supported vector

```text
k_t in ker J_t intersect (K^*)^3
```

may be selected independently.  Partially evaluate the actual complete
witness at all `k_t`, leaving `P` open.  This operation changes no graph and
does not infer or reopen variables from a fixed-residual identity.

The proof covers residual and promoted labels uniformly.  It also covers
every `r>=3`: there are `2r>=6` auxiliary labels, so a four-set exists and at
least two labels are contracted.  No incidence minor, response, deck, or
nuisance rank is assumed nonzero.

## Complete pair and target audit

For every raw pair `D` outside `P`, choose `t in D-P`.  Both root shores at
`t` vanish on `k_t`, so both orientations in the two-by-two companion vanish.
This includes pairs with one or two outside endpoints.  The top term vanishes
because the physical probe edge is zero.

For each surviving `D subset P`,

```text
Bhat-D=(Bhat-P) union (P-D).
```

After the outside contraction its physical complementary deck is a bilinear
edge on the two vertices of `P-D`.  Zero decks remain legal zero edges.

The target weights are

```text
beta_c=product_(t outside P) k_(t,c).
```

Every factor is nonzero, so every `beta_c` is nonzero.  Scaling one probe's
three coordinate covectors by `beta_c^(-1)` is invertible and gives the
normalized ternary target.

The independent matching census rebuilds all fifteen six-vertex matchings in
reverse vertex order.  Three use the zero probe edge.  The remaining twelve
split into six probe-target pairs and two orientations, exactly the six
surviving `GLS8` companions.  There is no multiplicity, transpose, or edge
typing defect.

## Linear-algebra and exceptional-fibre audit

Let `L=ker J_t`.  Over an infinite field, `L` misses `(K^*)^3` exactly when
it is contained in the union of the three coordinate hyperplanes.  A finite
union of proper subspaces cannot cover `L`, so `L` lies in one coordinate
hyperplane.  Taking annihilators gives

```text
e_c^* in im J_t^*.
```

This retains every rank profile:

- rank zero is never rigid;
- rank one is rigid exactly for a coordinate row line;
- rank two is rigid exactly when its kernel line has a zero coordinate;
- rank three is always rigid.

The primary implementation checks `18,279` exact rational row families with
all rank drops and duplicates.  The independent implementation enumerates
all `64` subspaces of `F_5^3`, where the field size is larger than the number
of coordinate hyperplanes, and separately compares torus incidence with
coordinate-row containment.  This modular census is an audit representation;
the written infinite-field proof carries characteristic zero.

The characteristic-zero transfer is sound.  All coefficients, chosen kernel
vectors, and target-weight inverses generate a finitely generated extension
of `Q`, which embeds in `C` and preserves the declared equations and
nonvanishing.

## Sharp non-closure boundary

An exact incidence-only interface attains the floor at `r=3`: give five
labels the injective joint map `(I,I)` and the sixth label the zero joint map,
with zero probe edge.  Each active pair map has the six-dimensional symmetric
image containing the three-colour diagonal, yet the incidence data forces no
nonzero complementary deck or physical response.  This is a local physical
interface control, not a complete GHZ witness.

On the equality branch `|Rig|=5`, contracting every non-rigid label at a
fully supported joint-kernel vector leaves ten terms whose complementary
physical decks are trilinear.  The open tensor has seven vertices.  It is not
an ordinary graph matching tensor, and the trilinear decks cannot be retyped
as bilinear edges without a new common factorization theorem.  The branch
`|Rig|>=6` has no five-label contraction.  Retaining six auxiliary labels
instead leaves four-linear decks and does not automatically produce an
eight-vertex graph.

Thus `GLS55` does not enter any named downstream theorem.  In particular it
does not prove:

- nonzero physical promoted response;
- selector survival modulo the complete labelled nuisance;
- one constant normalized row across a target family;
- projective synchronization or three-colour pair-depth activity;
- nuisance survival, augmented-weight alignment, or a target-pure anchor;
- raw-escape/full-swallow source coverage;
- any nonzero-anchor branch.

## Authenticated dependency replay

The protected authority checkout was read without editing it.  The
current-main verifier wrote its audit outside every repository:

```text
python claims/finite/n06/verify_six_vertex_final.py \
  --base C:\Users\Yeste\OneDrive\Documents\open-graph-theory-with-prize \
  --output C:\w\kg-gls55-six-vertex-dependency-audit-20260823.json
```

```text
GLS55 base HEAD:              2555476acfaebf29ab649e3a5a57d8998bac7ef3
authority checkout HEAD:      a16315f145324b503c3ec0ccd017ee7562f9626d
six-vertex theorem SHA-256:   63d41774e2a8c45ded67cb949b920c34d0cabb499ba6c215423dc274686066c4
top verifier SHA-256:         e383454d167b8d0cc7c35d6c56fb69fe7d302c2ca15d5d234047016c783a889e
replay output SHA-256:        2e539db1802048560e7e18c8bc69c5e1274ffd7883863e33dbe1551070de67b7
verified:                     true
CNF SHA-256:                  154b1a64a70b10eef5bd7cb3ddb929033d408b65f26ff2704eacc610030154c7
DRAT proof SHA-256:           9273c872b3aa071e67b3ff176d84c50d104e212bcab38980be38de69f9ffb1d1
```

No protected checkout, worktree, or process was modified.

## Required replay

```text
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_torus_kernel_contraction_and_five_rigid_label_floor.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_torus_kernel_contraction_and_five_rigid_label_floor.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_promoted_two_probe_one_target_attachment_and_pointwise_failure_reduction.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_promoted_two_probe_one_target_attachment_and_pointwise_failure_reduction.py
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_four_slot_partial_uncontraction_six_vertex_reconstruction_and_five_label_floor.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_four_slot_partial_uncontraction_six_vertex_reconstruction_and_five_label_floor.py
```

The package must still pass full candidate-tree validation, exact-head hosted
CI, safe merge, and fresh merged-main replay before publication is complete.

## Unresolved boundary

The smallest receiver-relevant successor remains the root-order-three common
seven-target attachment problem: supply all six pair rows and the four-port
row at one contraction, or contradict their simultaneous complete-module
failure by the full mixed GHZ equations.  `GLD3`'s separate three-colour
pair-depth activity gate would still have to be proved.

At higher root orders, no committed detector accepts only the promoted
top-minus-two/top layers.  Both equality-branch trilinear-deck coupling and
the six-or-more-rigid branch remain open.  The strategic node and global
conjecture remain **UNRESOLVED**.
