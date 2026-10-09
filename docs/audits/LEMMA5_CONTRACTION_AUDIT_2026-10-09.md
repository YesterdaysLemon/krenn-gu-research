# Adversarial audit of Lemma 5 (two-ancilla contraction) and its use for C_{6,1} — 2026-10-09

The global Krenn–Gu status is **UNRESOLVED**, and this audit does not change
it.  No theorem, node or live edge is added, withdrawn or re-scoped.

## Object of audit

- **Lemma 5** of
  [`compressed-hessian-family-2026-10-09.md`](../strategy/compressed-hessian-family-2026-10-09.md),
  Section 8, on `origin/main` at `ed34ffe7` (PR #389): the two-ancilla
  contraction identity, the weighted-GHZ form (3), and the "full-weight
  choice" criterion.
- Its use in `docs/strategy/ancilla-c61-2026-10-09.md` (branch
  `claude/ancilla-c61-20261009`, not on `main` at the time of this audit),
  Sections 0.3, 3.2, 3.3, 6 and 7: the implication
  `C_{6,1} = ∅  ==>  no ternary Krenn–Gu witness on eight vertices`, with
  the residual closed by `N8R1`.

**Independence.**  The auditor did not reuse the notes' scratch scripts
(they are not committed).  The replay
[`tests/test_lemma5_two_ancilla_contraction_audit.py`](../../tests/test_lemma5_two_ancilla_contraction_audit.py)
is a new implementation.  It differs from the notes' route as follows:

- it uses native one-colour vertices, not the three-colour embedding;
- it checks the identity in its split form for arbitrary `(ℓ, m)`, not only
  on the kernel quadric;
- the matching sum is cross-checked by the permutation-formula hafnian;
- the full-weight criterion is checked on every support pattern.

The auditor did derive the identity by hand from the same definition the
notes use; no other route to the definition exists.  So this is an
independent re-derivation and replay, not an independent formalization.

## Verdicts

| item | subject | verdict |
|---|---|---|
| 1 | contraction identity, conventions, one-colour semantics | **PASS** |
| 2 | full-weight criterion | **PASS with correction** (proof gap at `W_uv = 0`; statement true over `C`) |
| 3 | normalization to unit GHZ inside C_{6,1} | **PASS** |
| 4 | residual = hypothesis of `N8R1` | **PASS with citation and provenance corrections** |
| 5 | independent exact replay | **PASS** |

**Net effect on the C_{6,1} reduction.**  No correction changes what the
reduction says.

```text
C_{6,1} = ∅   ==>   no ternary block graph on eight vertices realizes Δ_(8,3)
```

holds as an exact implication.  It rests on two things:

- Lemma 5, with the full-weight criterion (items 1–3);
- the proved, computer-assisted, independently reviewed theorem `N8R1`
  (item 4).

Two scope remarks matter for whoever integrates it:

- In the frontier's own language, the dichotomy *is* the existing `M1`
  split at `n = 8`.
  - "Some pair is not a single nonzero entry" is exactly "maximum torus-root
    cardinality `r >= 2`", and Lemma 5 is the root-pair contraction.
  - "Every pair is a single nonzero entry" is exactly `r = 1`, which `N8R1`
    excludes.
  - So `C_{6,1} = ∅` would close the whole `M2` child at `n = 8`, including
    the max-`r = 2` program (`N8R2C`, `N8R2K`, `N8R2S`, `N8R2E`).
  - It is a strictly stronger target than that child, because C_{6,1}
    forgets the other root pairs, maximality and blocker saturation.
- The ancilla note's Section 3.3 says a witness gives a C_{6,1} element for
  every `(ℓ, m)` on the quadric.  It should say **every full-support**
  `(ℓ, m)` on the quadric.  Otherwise some weight `λ_c ℓ_c m_c` vanishes and
  the contraction is a two- or one-colour GHZ, not a C_{6,1} element.

## Conventions used (from the repository)

- [`src/krenn_gu/search_witness.py`](../../src/krenn_gu/search_witness.py)
  stores the block of the edge `e = (i, j)`, `i < j`, as `W[e, a, b]`, with
  `a` the colour at `i` and `b` the colour at `j`.
  - The amplitude of a colouring `s` is `Σ_M Π_{(i,j) ∈ M} W[(i,j), s_i, s_j]`
    over all perfect matchings `M`.
  - The target is 1 on constant colourings and 0 elsewhere, which is
    `Δ_(n,3)` with unit weights.
- The compressed-Hessian note uses the same convention ("`W_ij[a, b]`, where
  `a` is the colour at `i`").  It writes `W_ji = W_ij^T` implicitly, so
  `W_ij[a, b]` always has `a` at `i`.
- A witness in that note means `T_V = GHZ` up to the diagonal torus (pure
  weights `λ_c != 0`).  `N8R1` is stated for `Δ_(8,3)` with unit weights.
  Item 4 reconciles the two.

**One-colour vertex.**  A vertex `a` with a single colour.  Its block to a
three-colour `z` is a `1 x 3` row `r_z`, indexed by the colour at `z`.  Its
block to another one-colour vertex is a scalar.  The matching sum is the same
hafnian with `a` fixed to its only colour.  Equivalently, embed `a` as a
three-colour vertex whose colour-0 row is `r_z` and whose other rows are
zero, and evaluate at colour 0 (the ancilla note's Section 3.1 embedding).
The replay uses the native definition.

## Item 1 — the contraction identity: PASS

**Statement audited.**  Let `W` be any configuration of `3 x 3` blocks on
`V`, let `{u, v}` be a pair, and let `B = V - {u, v}`.  Take `ℓ, m ∈ C^3`
and put:

```text
r_z[c] = Σ_x ℓ_x W_uz[x, c]      (the row of u' to z)
s_z[c] = Σ_y m_y W_vz[y, c]      (the row of v' to z)
κ      = ℓ^T W_uv m = Σ_{x,y} ℓ_x W_uv[x, y] m_y
```

Then for every word `γ` on `B`:

```text
Σ_{x,y} ℓ_x m_y T_V(x, y, γ) = κ · T_B(γ) + Φ(γ),
Φ(γ) = matching sum of B ∪ {u', v'} with no u'v' edge, at γ
     = Σ_{z ≠ z'} r_z[γ_z] s_z'[γ_z'] T_{B - {z,z'}}(γ|).                       (A)
```

If `κ = 0`, the left side equals the ancilla matching sum, which is Lemma 5.
If `T_V = Σ_c λ_c |c^{|V|}⟩`, the left side is `[γ = c^{|B|}] λ_c ℓ_c m_c`,
which is (3) of the note.

**Re-derivation (split by the matching class of `{u, v}`).**  This route is
different from the note's, which contracts the matrix pair expansion (1).

1. Fix `γ` and expand `T_V(x, y, γ)` as the sum over perfect matchings `M`
   of `V`.  Partition the matchings into two classes.
   - **Class I:** `{u, v} ∈ M`.
   - **Class II:** `u` is matched to some `z ∈ B` and `v` to some `z' ∈ B`,
     with `z != z'` forced.
2. **Class I.**  `M = {uv} ∪ M'`, where `M'` runs over the perfect matchings
   of `B` exactly once.  The contracted contribution is
   `Σ_{x,y} ℓ_x m_y W_uv[x, y] · Π_{M'} = κ · T_B(γ)`.  The weight
   `W_uv[x, y]` has `x` at `u`, so the contraction is `ℓ^T W_uv m` and not
   `m^T W_uv ℓ`.
3. **Class II.**  `M = {uz, vz'} ∪ M''`, with `M''` a perfect matching of
   `B - {z, z'}`.  The contracted contribution factorizes:
   `(Σ_x ℓ_x W_uz[x, γ_z]) (Σ_y m_y W_vz'[y, γ_z']) Π_{M''}`, which is
   `r_z[γ_z] s_z'[γ_z'] Π_{M''}`.
4. The map `M ↦ {u'z, v'z'} ∪ M''` is a bijection from Class II onto the
   perfect matchings of `B ∪ {u', v'}` that do not contain `u'v'`.  It
   preserves the product weights.  With no `u'v'` edge these are all the
   matchings with nonzero weight.  If a `u'v'` edge of weight `κ` is added,
   its matchings give exactly Class I.  ∎

**Orientation, checked explicitly.**

- The colour index contracted at `u` is the row index of `W_uz` in the
  oriented convention.
- If the stored label order is `z < u`, the stored block is `W_zu = W_uz^T`,
  and `r_z = W_zu ℓ`, so `r_z[c] = Σ_x W_zu[c, x] ℓ_x`.
- The ancilla's own block is a `1 x 3` row when the ancilla's label is
  smaller, and a `3 x 1` column when it is larger.  The replay builds the
  ancilla configuration in both label orders.
- It also builds a deliberately wrong variant that contracts the colour at
  `z` instead of the colour at `u`.  The identity fails for that variant
  (`test_orientation_control`), so the replay is sensitive to the
  convention.

**Remarks.**

- (A) is a polynomial identity over any commutative ring.  Only Class I
  uses `κ`; nothing uses a witness property.
- The note's one-line proof, `(ℓ^T A_γ) Θ_γ (B_γ^T m)`, matches (A) with
  `ρ_γ = ℓ^T A_γ` and `σ_γ = B_γ^T m`.  This uses `A_γ[x, z] = W_uz[x, γ_z]`
  and `B_γ[y, z] = W_vz[y, γ_z]` from the note's Section 1.
- **Provenance.**  For full-support `ℓ, m`, the Class I / Class II partition
  is the `r = 2` case of the matching partition in the proof of Theorem 3 of
  the
  [maximal torus-root theorem](../../claims/arbitrary-order/MAXIMAL_TORUS_ROOT_SATURATION_AND_COORDINATE_ABSORPTION_THEOREM.md#2-the-saturated-principal-hafnian-layer),
  with roots `R = {u, v}` and an internal root edge of value zero.  That
  partition does not use maximality.  Lemma 5 is therefore not a new
  mechanism.  It restates the root-pair contraction with the roots read as
  ancillas.  The ancilla rows `r_z` and `s_z` are the root-incidence
  columns `H_z`, and `Φ` is the `s = n - 4` layer
  `Σ_{|S| = n-4} H_S ⊗ P_2`.

## Item 2 — full-weight criterion: PASS with correction

**Statement audited.**  Over `C`, there exist `ℓ, m` with `ℓ^T W_uv m = 0`
and `ℓ_c m_c != 0` for every `c` **iff** `W_uv` is not a single nonzero
entry.  `W_uv = 0` counts as "not a single nonzero entry".

**The statement is true.**  Independent proof, by a different route from the
note's case analysis:

- `f(ℓ, m) = ℓ^T W_uv m` is a bilinear polynomial.  "Some full-support `ℓ, m`
  make it vanish" means `f` has a zero on the torus `(C^*)^3 x (C^*)^3`.
- If `W_uv = α E_ab` with `α != 0`, then `f = α ℓ_a m_b`, which is nonzero on
  the torus.
- If `W_uv = 0`, every point is a zero.
- Otherwise `W_uv` has two nonzero entries.  Suppose `f` were zero-free on
  the torus.
  - By the weak Nullstellensatz in the Laurent ring, `f` would be a unit,
    hence a scalar monomial.
  - A bilinear monomial is `α ℓ_a m_b`, one entry, which is a contradiction.

This is the argument of Section 3 of the maximal torus-root theorem.  So:

```text
W_uv is not a single nonzero entry   <=>   {u, v} is a torus-root pair (B_uv(x_u, x_v) = 0, x ∈ (C^*)^3).
```

**Elementary constructive proof** (used by the replay).  Choose a
full-support `ℓ` with `h = W_uv^T ℓ` not a nonzero multiple of a unit vector.
Then `h^⊥` contains a full-support `m`:

- if `h = 0`, any `m` works;
- if `supp h = {i, j}`, take `m_i = h_j`, `m_j = -h_i` and the third entry 1;
- if `supp h` is everything, take `m = (1, t, -(h_0 + t h_1)/h_2)`, with
  `t ∈ {1, 2}` chosen so that the last entry is nonzero.

Such an `ℓ` exists unless `W_uv` is a single nonzero entry:

- if `W_uv` is zero, or not supported in one column, the bad set of `ℓ` is a
  finite union of proper subspaces;
- if `W_uv = a e_i^T` with `|supp a| >= 2`, take a full-support `ℓ ⊥ a`, so
  `h = 0`.

**Correction to the note's written proof.**  Step 3 ("otherwise, for generic
full-support `ℓ`, `h = W_uv^T ℓ` is not a multiple of a unit vector")
silently includes `W_uv = 0`.  For that block `h = 0` for every `ℓ`, and `0`
*is* a multiple of a unit vector, so the sentence is false as written.  The
case is trivial: any full-support `ℓ, m` works.  The note does state
afterwards that "`W_uv = 0` allowed", so the conclusion is right and only
the proof needs the one-line case.  Steps 1 and 2 are correct.

**Field.**  "Infinite field" is needed.  Over `F_2`, `W = I` has no
full-support `ℓ, m` with `ℓ · m = 0`.  The repository works over `C`, so
this is not a gap.

**Cases asked for, all confirmed exactly** (`FullWeightCriterion` tests):

| block | full-support kernel pair? |
|---|---|
| zero block | yes |
| single nonzero entry | **no** (monomial) |
| rank 1, two entries in one row | yes |
| rank 1, full row | yes |
| rank 1, two entries in one column | yes (`ℓ ⊥` column, so `h = 0`) |
| rank 1, `a b^T` for all 49 support pairs | yes iff `|supp a| + |supp b| > 2` |
| rank 2 (diagonal, antidiagonal) | yes |
| rank 3 (identity) | yes |
| all 512 support patterns, random nonzero integer values, 3 fillings each | yes iff not a single entry |

## Item 3 — normalization: PASS

C_{6,1}, as defined in both notes, asks for GHZ(6,3) **up to the torus**, so
no normalization is needed.  If unit weights are wanted, the operation is
this.

**Rescaling.**  Fix a three-colour vertex `z ∈ B`.  For every other vertex
`w`, divide the colour-`c` row at `z` of the block between `z` and `w` by
`μ_c`.  This includes the ancilla blocks, where it divides the entry
`r_z[c]` (or `s_z[c]`).

- Every perfect matching covers `z` exactly once, so `T(γ)` becomes
  `T(γ) / μ_{γ_z}`.
- Taking `μ_c = λ_c ℓ_c m_c` gives unit GHZ.
- The ancillas stay one-colour vertices: their blocks are still `1 x 3`
  rows, with entries rescaled.
- No `u'v'` edge is created, because that pair is never touched.
- `B` is nonempty (`|B| = 6`).

The rescaling cannot be done at an ancilla: a one-colour vertex has one
colour, so rescaling it multiplies every word by the same scalar.

The replay checks the rescaling on an order-8 contraction with
`μ = (2, -3, 5/7)` (`TorusNormalization`).

The same rescaling maps a nonzero matrix unit to a nonzero matrix unit.  It
is used in item 4 to pass between weighted and unit targets.

## Item 4 — the residual is `N8R1`'s hypothesis class: PASS with corrections

**Citation correction (to the audit brief, not to the note).**  The theorem
`N8R1` is owned by
[`claims/finite/n08/EIGHT_VERTEX_MATRIX_UNIT_EXCLUSION_THEOREM.md`](../../claims/finite/n08/EIGHT_VERTEX_MATRIX_UNIT_EXCLUSION_THEOREM.md).
That is the frontier's `N8R1` row, with the
[certificate package](../../claims/finite/n08/r1-source-certificate/README.md)
and the
[integration review](EIGHT_VERTEX_MATRIX_UNIT_INTEGRATION_REVIEW_2026-09-04.md).
The maximal torus-root theorem (Section 3) supplies the `r = 1` ⇔
complete-matrix-unit equivalence; it does not prove the `n = 8` exclusion.
The ancilla note cites the correct file.

**Exact hypothesis of `N8R1`.**

> There is no ternary complex block graph on eight vertices with full
> matching tensor `Δ_(8,3)` whose maximum fully supported pairwise-zero
> torus-root cardinality is one.  Equivalently, a complete graph with one
> nonzero matrix unit on every physical pair cannot realize `Δ_(8,3)`, for
> any assignment of nonzero complex edge weights.  Endpoint colours may
> differ.  No positivity, phase restriction, genericity, or weight
> normalization is imposed.

**Comparison with the Lemma-5 residual**, "every one of the 28 pairs carries
a single nonzero entry":

| point | Lemma 5 residual | `N8R1` | match? |
|---|---|---|---|
| quantifier over pairs | all 28 pairs | "every physical pair", complete graph | yes |
| zero blocks | not in the residual: `W_uv = 0` is handled by Lemma 5 (any full-support `ℓ, m`) | not allowed: all 28 blocks present | yes; the dichotomy has no gap |
| block shape | exactly one nonzero entry, any position `(a, b)` | one nonzero matrix unit, endpoint colours may differ | yes |
| weights | arbitrary nonzero complex | arbitrary nonzero complex, no normalization | yes |
| target | witness tensor: `Δ_(8,3)` (repository target) or weighted GHZ | `Δ_(8,3)` | yes; a weighted GHZ is rescaled to `Δ_(8,3)` at one vertex (item 3), which keeps every block a nonzero matrix unit |
| "maximum root one" | by item 2, "no pair is a torus-root pair", which is `r = 1` | `r = 1`, equivalent to complete matrix units (Laurent-unit argument; the converse holds since a matrix unit is zero-free on the torus) | yes, in both directions |

The `N8R1` proof (Sections 1–4 of its theorem file) starts from complete
matrix units directly:

- it keeps all 105 matchings and all 28 nonzero blocks;
- its cuts are exact relations over `C` with every `λ_e != 0`;
- its leaves are 18 DRAT proofs, independently accepted.

**The dichotomy is exhaustive.**  For any ternary block graph `W` on eight
vertices realizing `Δ_(8,3)`, exactly one of the following holds.

- **(i)** Some pair `{u, v}` has `W_uv` that is not a single nonzero entry.
  Then item 2 gives full-support `ℓ, m` on the quadric, and item 1 gives a
  C_{6,1} configuration with weights `ℓ_c m_c != 0`.
- **(ii)** All 28 pairs are single nonzero entries.  `N8R1` excludes this.

So `C_{6,1} = ∅ ⇒` no ternary `n = 8` witness, with nothing left over.  The
ancilla note's "with nothing left over" is correct.

**Provenance correction (to the ancilla note).**  The note presents this as
a new candidate edge "`C_{6,1} -> N8 exclusion`".  By item 2, case (i) is
exactly the frontier's `M1` branch `r >= 2`, and Lemma 5 is the root-pair
contraction (item 1).  The candidate edge should therefore be recorded as
"`C_{6,1} = ∅` closes the `n = 8` child of `M2`".  It is not a parallel
route, and the existing max-`r = 2` nodes are partial results on the same
child.  The note's Section 3.3 already says that `C_{6,1} = ∅` is
sufficient but not necessary.

**Wording correction (ancilla note, Section 3.3).**  "for **every** `(ℓ, m)`
on the quadric" should read "for every **full-support** `(ℓ, m)` on the
quadric".

## Item 5 — independent exact replay: PASS

[`tests/test_lemma5_two_ancilla_contraction_audit.py`](../../tests/test_lemma5_two_ancilla_contraction_audit.py)
uses the standard library only, with exact integer and `Fraction`
arithmetic.  It takes about 2 s.

| test | what it checks |
|---|---|
| `test_hafnian_cross_check` | recursive matching sum = permutation-formula hafnian on all 729 words of two random order-6 configurations, and on an order-6 ancilla configuration with `κ = 7` (81 words) |
| `test_split_identity_n6` | (A) with `κ != 0` in general: LHS = `κ T_B + Φ`, and LHS = the ancilla sum with a `u'v'` edge of weight `κ`.  3 random configurations x 4 pairs (including `u > v` and interior labels), all 81 words, ancilla labels alternately above and below `B`.  Non-vacuity: in more than a quarter of the words both terms are nonzero |
| `test_split_identity_n8` | the same at order 8, pairs `(5,2)` and `(7,0)`, all 729 words |
| `test_kernel_identity_n6` | Lemma 5 proper (`ℓ^T W_uv m = 0`, full-support `ℓ, m`): 4 configurations x 3 pairs, all words, more than half of them nonzero |
| `test_kernel_identity_n8` | the same at order 8, 2 configurations x pairs `(6,3)`, `(1,4)`, all 729 words |
| `test_orientation_control` | rows built from the transposed block fail the identity |
| `FullWeightCriterion` (2 tests) | item 2, as tabulated above |
| `TorusNormalization` | item 3 |
| `OrderFourWitness` | the full statement (3) on an exact weighted GHZ(4,3) (complete matrix units, `λ = (3, -2, 5/3)`), for all 12 ordered pairs |

Random configurations have entries in `[-3, 3]` with about 20% zeros.  They
are not witnesses; the identity is tested in its contracted form for every
configuration, as asked.

**No non-residual weighted-GHZ fixture exists.**  The repository has no
committed exact ternary witness, and none at all at `n = 6, 8` (`n = 6` is
excluded).  The only exact family available is the order-4 matrix-unit
graph.  Every pair in it is a single entry, so it lies in the residual: a
kernel pair must have `ℓ_a m_b = 0`.  The test checks (3) with that weight
equal to zero, and it checks that no full-support kernel pair exists.

**A consistency consequence at order 4** [EXACT, three-line hand proof;
audit cross-check, not a new frontier claim].  Every ternary block graph on
four vertices realizing a weighted GHZ(4,3) has all six blocks single
nonzero entries.

*Proof.*  Suppose a pair is not a single entry.  Items 1–2 give a
two-vertex `B = {z_0, z_1}` and two non-adjacent ancillas whose matching sum
is the diagonal matrix `diag(λ_c ℓ_c m_c)`, of rank 3.  But that sum is
`r_0 s_1^T + s_0 r_1^T`, of rank at most 2.  ∎

[OBSERVATION]  Levenberg–Marquardt from random complex starts:

- 25 of 43 restarts converged to cost `< 1e-24` at `max|w| <= 12`;
- **every** one has exactly one entry per block above `1e-6 · max|w|`;
- the other 18 are slow border runs (cost `1e-10` to `1e-6` at `max|w|`
  from 300 to 2,400).

So this attempt to falsify Lemma 5 and item 2 together at the smallest order
found nothing.  It is floating-point evidence only.

## Evidence status

- Lemma 5 and the full-weight criterion:
  - proved by hand (items 1 and 2);
  - re-derived here by different routes, and replayed exactly by a new
    implementation;
  - no Lean formalization.
- This audit is an **independent re-derivation** in the sense of
  AGENTS.md Section 5:
  - a different proof route for both statements;
  - a different implementation (native one-colour vertices, a split form, a
    second hafnian algorithm);
  - but the same author family (automated agents), and no formal checker.
- `N8R1`: proved exact computer-assisted exclusion, independently reviewed
  2026-09-04.  It was not re-checked here.  Only its hypothesis was compared.
- The implication `C_{6,1} = ∅ ⇒` no ternary `n = 8` witness is exact.
  - Its premise `C_{6,1} = ∅` is **OPEN**.
  - The ancilla note's Section 2.2 shows the edge-allowed class C'_{6,1} is
    nonempty.  That does not bear on C_{6,1}.

## Frontier

This audit does not edit
[`docs/current-frontier.md`](../current-frontier.md).  It changes no
theorem, node, edge or scope; it confirms an implication the notes already
state as candidate.  For the integrator:

- the stale clause "outside the residual where every pair carries a
  single-entry block" can now cite `N8R1` as closing that residual;
- the `C_{6,1}` edge should be attached to the `n = 8` child of `M2` (the
  `M1` branch `r >= 2`), not drawn as a parallel route.

## Commands and runs

```text
python -m unittest -v tests.test_lemma5_two_ancilla_contraction_audit
```

Bounded runs (`tools/research/run_bounded.py`):

- `lemma5-audit-tests-1` to `-5`: the replay during development.
  - `-1` failed one support-pattern case.  Its search box was too small for
    `W = [[-3,2,0],[-1,-3,0],0]`, whose solution needs `m = (1, -4, 1)`.
  - The search was replaced by the constructive procedure of item 2.
  - `-5` and the committed version pass.
- `lemma5-audit-n4-obs-1`: a first, slow version of the order-4 observation.
  It timed out at 600 s with no output and was superseded.
- `lemma5-audit-n4-obs-2`: the vectorized order-4 observation.  It was
  stopped by the runner's 300 s limit after 43 restarts; the figures above
  are from those 43.  Its scratch script is not committed.

No process launched by this audit is still running.  The three 24-hour runs
of another worktree were not touched.
