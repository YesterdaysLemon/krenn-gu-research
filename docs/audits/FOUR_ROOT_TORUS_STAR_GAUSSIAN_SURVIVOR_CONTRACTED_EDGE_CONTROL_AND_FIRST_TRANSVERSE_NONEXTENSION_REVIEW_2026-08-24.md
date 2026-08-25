# Hostile review: Gaussian survivor contracted-edge control and first-transverse nonextension

Date: 2026-08-24

## Verdict

**Accept as exact single-fibre grade-zero edge control and pointwise
first-transverse nonextension.**  One pinned raw preimage of the `GLD72`
Gaussian survivor becomes a literal diagonal four-port target after a
covariant basis change and is realized by exact effective edge data on ten
vertices.  The complete first-response space at each contracted vertex meets
the diagonal target space only in the base-target line.  Therefore no choice
of the unused rows of edge matrices over those same effective data can extend
to the ten-mode GHZ identity.

The accepted statement concerns one point of a `35`-dimensional affine raw
coefficient fibre.  It does not exclude another preimage of the same `GLD72`
tensor, certify maximum-root order four or absence of a fifth root, construct
a global graph witness, or resolve Krenn--Gu.  The global conjecture remains
**UNRESOLVED**.

**Successor update (2026-08-24).**  `GLD74` subsequently excludes the entire
`35`-dimensional raw fibre at the complete `q_0` first response.  That does
not change the correctness or original single-fibre scope reviewed here; it
closes the parent obligation this review identified.  Whole-locus,
source-presentation, maximum-root, fifth-root, and global questions remain.

Reviewed artifacts:

- [`FOUR_ROOT_TORUS_STAR_GAUSSIAN_SURVIVOR_CONTRACTED_EDGE_CONTROL_AND_FIRST_TRANSVERSE_NONEXTENSION_THEOREM.md`](../../claims/arbitrary-order/FOUR_ROOT_TORUS_STAR_GAUSSIAN_SURVIVOR_CONTRACTED_EDGE_CONTROL_AND_FIRST_TRANSVERSE_NONEXTENSION_THEOREM.md);
- [`verify_four_root_torus_star_gaussian_survivor_contracted_edge_control_and_first_transverse_nonextension.py`](../../claims/arbitrary-order/verify_four_root_torus_star_gaussian_survivor_contracted_edge_control_and_first_transverse_nonextension.py);
- [`audit_four_root_torus_star_gaussian_survivor_contracted_edge_control_and_first_transverse_nonextension.py`](../../claims/arbitrary-order/audit_four_root_torus_star_gaussian_survivor_contracted_edge_control_and_first_transverse_nonextension.py);
- the owning [`GLD70` complete nuisance map](../../claims/arbitrary-order/FOUR_ROOT_COMPLETE_Q_LAYER_SECANT_BOUNDARY_TRAP_AND_TORUS_STAR_COMPRESSION_THEOREM.md);
- the [`GLD72` exact Gaussian survivor](../../claims/arbitrary-order/FOUR_ROOT_TORUS_STAR_GAUSSIAN_GHZ_SURVIVOR_AND_DETERMINANT_SAFE_ROUTE_REFUTATION_THEOREM.md).

## 1. Exact claim under review

Let `F_0=A` and `F_1=F_2=F_3=G` be the invertible Gaussian-rational frames
from `GLD72`, and put `S_u=F_u^(-1)`.  Transform the canonical root-to-port
matrices and raw coefficients by

```text
P'_u=P_u F_u^(-T),
h'_(rho,u)=S_u h_(rho,u),
H'_(uv)=S_u H_(uv) S_v^T.                              (1)
```

The reviewed assertions are:

```text
(tensor_u S_u)T=Delta_4,
b'(alpha_*)=Delta_4,
sha256(alpha_*)=4d227cac41d64bef66d062ffb6a052a12aa11e9c648ddbb59d8c27040c357f0a,
contracted ten-vertex matching tensor=Delta_4,
rank D_v=17 and rank(pi_mix D_v)=16 for all six contracted v. (2)
```

The last line implies

```text
Im D_v intersect Diag=C Delta_4.                        (3)
```

Because the derivative of a fully supported ten-mode GHZ target spans all of
the three-dimensional `Diag`, (3) excludes every edge-matrix completion over
the fixed effective data `alpha_*`.

## 2. Covariance and coefficient convention

The inverse and inverse-transpose positions in (1) were treated as
load-bearing.  Tensor coordinates transform by `S_u`.  A port map is stored
with local coordinates as columns, so its transformed matrix is
`P_u S_u^T=P_u F_u^(-T)`.  A labelled residual coefficient vector transforms
by `S_u`; a labelled pair coefficient transforms on both sides by
`S_u(-)S_v^T`.

The primary substitutes these formulas into the committed `GLD70` map.  The
standalone audit independently constructs the original `79` permanent
columns, obtains rank `44`, derives the same pinned `37`-sparse preimage,
performs its own Gaussian matrix inversions, and obtains the same transformed
`52`-nonzero preimage and hash.  Both replay all `81` coordinates of the
literal diagonal.  An inverse-transpose error would change the transformed
columns and fail this replay; none is hidden by a syndrome calculation.

## 3. Contracted edge semantics

The effective graph has four contracted roots, two contracted residual
vertices, and four open ports.  All six contraction vectors are literally
`(1,1,1)`, so the colour weights induced by the other five contractions are
all one.  The target is therefore the unweighted `Delta_4`, not a silently
rescaled diagonal.

The two residual-port raw labels require a convention that is easy to reverse:

```text
q_0--port uses h_eta,          q_1--port uses h_xi.       (4)
```

Pairing `q_0` directly leaves `q_1` in the companion permanent and hence
leaves `eta`; the other case leaves `xi`.  Both implementations encode (4)
explicitly and replay all `9!!=945` perfect matchings.  They obtain one on the
three diagonal port words and zero on the other `78` words.

The edge realization is genuine at this contracted grade.  Evaluation of an
independent `3 x 3` matrix at `(1,1,1)` is onto the required scalar or
three-vector space, and every raw label belongs to a distinct graph edge.
This establishes one physical boundary-edge fibre.  It does not establish
the uncontracted GHZ identity or any maximum-root hypothesis.

The audit additionally constructs explicit edge matrices with colour row one
zero.  Their global all-one coefficient is exactly zero.  This is a useful
sanity control, but it is not the reason every completion fails: other unused
rows are allowed in the response-space argument below.

## 4. Completeness of the first-response map

At a contracted vertex `v`, differentiating or replacing its incident row
can pair `v` with any of nine neighbours.  The five other contracted
neighbours contribute five scalar evaluations.  Each of the four open ports
contributes three coordinate evaluations.  Hence the complete response domain
has dimension

```text
5+4*3=17.                                               (5)
```

This count includes root--root first-order directions; zero base evaluations
do not delete their derivatives.  It also includes both residual directions
and every root/residual-to-port colour.  Because different incident edges are
independent matrices and a transverse vector together with `(1,1,1)` gives
independent row evaluations, no legal first-row parameter is omitted.

For each parameter, both implementations delete the varied edge and sum the
remaining four-edge products over the `105` matching cofactors containing
that edge.  Exact Gaussian elimination gives

```text
(rank D_v, rank(pi_mix D_v), difference)=(17,16,1)       (6)
```

at each of the six vertices.  The difference in (6) is exactly the dimension
of the image tensors whose `78` mixed coordinates vanish.  The base incident
row replays `Delta_4`, so this one-dimensional intersection is the claimed
line, not an unidentified diagonal direction.

On a ten-mode GHZ identity, replacing the vector at `v` by
`y=(y_0,y_1,y_2)` while leaving the other five contractions equal to
`(1,1,1)` gives

```text
y_0 e_0^(tensor 4)+y_1 e_1^(tensor 4)+y_2 e_2^(tensor 4). (7)
```

Its image is all of `Diag`.  Every graph-side row replacement belongs to
`Im D_v`, contradicting (3).  This proves universal nonextension over the
unused rows of the fixed effective edge data, not merely failure of the
displayed row-zero completion.

## 5. Hostile attacks and rejected strengthenings

### 5.1 The local basis change manufactures a graph realization

Rejected as a strengthening.  The basis change and coefficient covariance
only identify a raw preimage of the diagonal and its contracted edge values.
They do not provide a global GHZ graph.  The first-response theorem proves
that no global completion exists over this particular preimage.

### 5.2 The residual labels are attached to the wrong physical edges

Rejected.  The complementary residual, not the directly paired residual,
names the `GLD70` permanent column.  Equation (4) is independently checked by
both matching implementations.

### 5.3 Zero root--root base edges make their tangent directions disappear

Rejected.  A zero edge evaluation kills its grade-zero matching terms, but a
row replacement on that edge is multiplied by the matching cofactor after the
edge is deleted.  All five contracted-neighbour scalar columns, including the
other roots, occur in (5).

### 5.4 Rank difference one is being confused with a derivative rank

Rejected.  The difference is used only as
`dim(Im D_v intersect ker pi_mix)`.  The base replay identifies the resulting
line.  The target derivative rank three is established separately by the
explicit map (7).

### 5.5 One pinned raw solve excludes the survivor tensor

Rejected as unsupported.  The transformed map has rank `44`, so
`(b')^(-1)(Delta_4)` is an affine `35`-space.  Moving inside it changes the
matching cofactors and response maps.  The accepted theorem excludes only
the matrix-lift fibre over `alpha_*`.

### 5.6 A contracted edge array certifies a maximum fourth root

Rejected.  Pairwise zero root-root evaluations at the displayed contraction
do not prove that no fifth fully supported root exists, nor that this root
configuration arises as a maximum root of a hypothetical witness.  Those
source hypotheses remain open.

### 5.7 Modular fibre sampling proves the parent theorem

Rejected.  Seeded finite-field samples were useful reconnaissance and found
only the generic `(17,16)` response profile, but sampling neither covers the
affine fibre nor resolves exceptional rank charts.  No modular observation is
used in the accepted claim.

## 6. Independence and reproducibility

The primary route imports the owning `GLD70` and `GLD72` implementations so
the new calculation is checked against the live repository definitions.  The
standalone audit imports no repository code, SymPy, or third-party package.  It
separately implements `Q(i)` arithmetic, matrix inversion and elimination,
the permanent map, pivot solve, tensor covariance, edge blocks, matching
enumeration, and first-response ranks.

The accepted replay is:

```powershell
python claims/arbitrary-order/verify_four_root_torus_star_gaussian_survivor_contracted_edge_control_and_first_transverse_nonextension.py
python -I claims/arbitrary-order/audit_four_root_torus_star_gaussian_survivor_contracted_edge_control_and_first_transverse_nonextension.py
```

Both routes report the hash in (2), nonzero split `1/24/27`, `945` matchings,
six rank triples `(17,16,1)`, literal all-one contraction vectors, and no
maximum-root, full-fibre, graph-witness, or global claim.

## 7. Accepted frontier delta

The source-integrability frontier for the exact `GLD72` hostile control is now:

1. one pinned raw preimage is physically realizable at complete contracted
   edge grade zero;
2. every uncontracted edge-matrix lift over that effective data fails already
   at the complete first response;
3. the then-remaining parent object was the full affine `35`-dimensional
   preimage; `GLD74` now excludes it through a sharper one-vertex quotient;
4. maximum-root certification, higher root orders, non-star atlases, and
   global coverage remain separate.

This is a real universal-bridge advance from a formal nuisance-space point to
an exact physical fibre and its first obstruction.  It is not global closure.
