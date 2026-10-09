# Fibre-realizability of the two `n = 8` recursive-support-model patterns — 2026-10-09

This is a dated research record.  The global Krenn–Gu status is
**UNRESOLVED**, and nothing here changes it.  `docs/current-frontier.md` is
not edited (see Section 6).

Evidence labels:

- **[EXACT]**: an exact integer polynomial identity checked by the committed
  verifier `claims/finite/n08/verify_n8_recursive_support_s128_grid_identity.py`.
- **[MODULAR]**: linear algebra or Gröbner computations over a prime field;
  evidence only.
- **[SAT-RUN]**: a bounded run of
  `claims/finite/n08/explore_general_block_recursive_support_model.py` with
  the pattern fixed; no DRAT proof is attached, so not a proof.
- **[NUMERIC-EXPLORATION]**: floating-point local search; used only to
  steer, never as evidence for a claim.

## 1. Question and conventions

Section 4 of
[`hyperdeterminant-crossing-2026-10-09.md`](hyperdeterminant-crossing-2026-10-09.md)
reports two `n = 8` zero patterns that satisfy the recursive support model:

- **S128** (Section 4.2; killers + plane rigidity), 128 entries;
- **S156** (Section 3.4; killers + top-level H2/H3 + all-level plane
  rigidity), 156 entries: sixteen full blocks on a 4-regular graph `F` and
  twelve single entries on the complementary 3-regular graph `H`.

Both are support-level objects.  The question is whether either is
**fibre-realizable**: is there a complex configuration `W`, supported on
(exactly, or within) the pattern, with `T_W = GHZ(8,3)`?

Conventions are those of the model script: `W_ij[a,b]` for `i < j`, with
`a` the colour at `i` and `b` the colour at `j`.  The matching tensor is
`T_W(w) = sum_M prod_{ij in M} W_ij[w_i, w_j]`, summed over the 105 perfect
matchings of `K_8`.  This is also the convention of
`src/krenn_gu/full_tensor_cancellation.py`.  The pattern listings were
parsed from the inline text of the source note; no regeneration was needed.

The target is used up to the diagonal torus.  Nonconstant words must
vanish; the three constant words must be nonzero.  Rescaling one vertex
turns any nonzero constant values into `1`, so this is equivalent to
`T_W = GHZ`.

## 2. Summary

| pattern | verdict | strongest evidence | mechanism |
|---|---|---|---|
| S128 | **not realizable** | [EXACT] four-word polynomial identity | rank-one grid transport (holonomy rule H3) with one surviving term |
| S156 | **inconclusive** | survives every encoded support family with `g` fixed [SAT-RUN]; no low-degree certificate found [MODULAR] | none found; Section 4.4 says why the known families cannot fire |

## 3. S128 is not fibre-realizable  [EXACT]

### 3.1 The four words

Fix colours `1,1,0,1,0,1` at vertices `1,3,4,5,6,7`.  Vary colour `a` at
vertex 0 and colour `b` at vertex 2 over `{0,1}`.  Restricted to S128, the
four word polynomials are:

```text
E00 = T(01010101) = p0*X0 + q0*Y0
E10 = T(11010101) = p1*X0 + q1*Y0
E11 = T(11110101) = p1*X1 + q1*Y1
E01 = T(01110101) = p0*X1 + q0*Y1 + Z
```

The symbols are:

- `p_a = W05[a,1]` and `q_a = W07[a,1]`;
- `X0 = W13[1,1]W24[0,0]W67[0,1] + W13[1,1]W27[0,1]W46[0,0] + W17[1,1]W23[0,1]W46[0,0]`;
- `X1 = W13[1,1]W24[1,0]W67[0,1] + W17[1,1]W23[1,1]W46[0,0]`;
- `Y_b = W15[1,1] W23[b,1] W46[0,0]`;
- `Z = W02[0,1] W15[1,1] W37[1,1] W46[0,0]`.

Hub vertex 0 has exactly two live partners, 5 and 7, in three corners.  In
the corner `(a,b) = (0,1)` the single entry `W02[0,1]` adds a third partner,
2, whose complementary six-vertex coefficient is the single monomial
`W15[1,1]W37[1,1]W46[0,0]`.

### 3.2 The identity

As polynomials, with every entry outside S128 set to zero,

```text
p1*Y0*Z = p1*Y0*E01 - p0*Y0*E11 + p0*Y1*E10 - p1*Y1*E00.
```

At a GHZ witness all four words are nonconstant, so the right side
vanishes.  The left side is a product of six support entries:
`W05[1,1]`, `W15[1,1]` (twice), `W23[0,1]`, `W46[0,0]` (twice), `W02[0,1]`,
`W37[1,1]`.

So **no configuration supported within S128 in which those six entries are
nonzero has matching tensor `GHZ(8,3)`**.  This holds over every field and
uses no division.  In particular, S128 is not fibre-realizable with exact
support.  Realizations on proper subpatterns that kill one of the six
entries are not covered.

The verifier also reduces the zero hypotheses greedily.  The identity
already holds with only 17 of the 24 outside entries that occur in the four
unrestricted word polynomials set to zero:

```text
W02[00] W02[10] W02[11] W03[01] W03[11] W04[00] W04[10] W06[00] W06[10]
W25[01] W25[11] W34[10] W35[11] W36[10] W45[01] W56[10] W57[11]
```

So this is a 23-literal conditional obstruction (17 zeros and 6 nonzeros)
on `K_8`.  The greedy order is arbitrary, so this is not claimed to be a
minimum.

Hand derivation:

1. The `b = 0` words say that `(p_a, q_a)` is orthogonal to `(X0, Y0)` for
   `a = 0, 1`.
2. Since `Y0 != 0`, the vectors `(p_0,q_0)` and `(p_1,q_1)` are parallel.
   This is the rank-one step.
3. Then `E11 = 0` forces `p0*X1 + q0*Y1 = 0`.
4. Hence `E01 = Z != 0`.

### 3.3 Minimality and conceptual reading

The subsystem is minimal: on the torus, each three-word subset is
satisfiable.  This was checked by hand, not by a committed script.
Dropping `E01` removes `Z`.  For any other dropped word, the remaining
equations are solved as follows.  Choose the `p_a`, `q_a` generic (or
parallel, if both `b = 0` words remain).  Solve linearly for `W27[0,1]`
(through `X0`) and for `W24[1,0]` and `W23[1,1]` (through `X1` and `Y1`).
The solved values are generically nonzero.

Two searches support that it is the smallest kind of certificate.  The
search used is **degree-1 Laurent XL**:

- for a target word `t` and source words `w`, the rows are the Laurent
  shifts `(m'/m) * f_w`, with `m` a monomial of `f_w` and `m'` a monomial of
  `f_t`, together with `f_t` itself;
- all rows then have the torus character of `t`;
- a single Laurent monomial in their row span mod 1000003 is a certificate
  of inconsistency on the torus.

Results [MODULAR]:

- over all 99 words with at most three live terms it finds no certificate;
- over the 751 words with at most four live terms it finds certificates
  (five targets were checked), all using the same four words above.

**Reading.**  This is exactly an instance of the holonomy rule **H3**
(rank-one grid transport, Lemma B′ of
[`holonomy-support-model-2026-10-08.md`](holonomy-support-model-2026-10-08.md)).
The instance is:

- level `A = V`, hub `p = 0`, partners `k1 = 5` and `k2 = 7`;
- varied vertices `u = 0` and `v = 2`;
- three corners have live set exactly `{5, 7}`, so CAN holds there, and the
  square rule transports CAN to the fourth corner;
- the fourth corner then has exactly one further live term, the `W02` term,
  in a non-`m` word.

It is **not** a column killer, and not a plane-rigidity instance (PR never
fires on S128: Section 4.2 of the source note).  It is not a new mechanism.
S128 was produced without `--holonomy`, and H3 alone already excludes it.

### 3.4 Corroboration

- **[SAT-RUN]** The model was rerun with `g` fixed to S128 (`--pattern-file`,
  `--no-symmetry`) and with killers, H2/H3 at every level, and PR.  It is
  **UNSAT** after 2 CEGAR rounds (39 s).  The lazy instances were 3,096 H2
  and 211,863 H3 components (E/C/S); the first violation reported is an
  "H3 single surviving term".
  - The final DIMACS SHA-256 is
    `19da3aa3b6eaf2c11c8f1325407c7ba3ccb2aa20ae077ceb074070c81a3ac86c`.
  - It was not DRAT-checked, so it corroborates the identity but is not used
    as a proof.
- **[MODULAR]** Grid census (Section 4.2): searching single `(p, v, c)`
  grids, smallest first, for degree-1 Laurent certificates found 203
  certificate-bearing grids among the first roughly 6,300 of 20,328 (176
  among the first 6,250).  The search stopped at its 900 s cap.  The
  obstruction is therefore abundant in S128, not isolated.

## 4. S156: inconclusive

### 4.1 Support-level families do not exclude it  [SAT-RUN]

The model was rerun with `g` fixed to S156 and **all** encoded families:
killers, H2 and H3 at every level (`|A| = 4, 6, 8`), and PR at every level.
It is **SAT in the first CEGAR round**, with 0 lazy instances and every
checker passing (`check_model`, `check_holonomy`, `check_plane`).

The source note had imposed holonomy only at the top level for this model.
So S156 survives the full rule set, not only the top-level one.  PR premises
never hold in the model; the failure census is:

- 2,265,680 instances fail because an outside summand is live;
- 1,395,040 instances fail because `h` is dead.

### 4.2 Algebraic tests  [MODULAR]

- **Jacobian rank.**  The support-restricted map from `C^156` to `C^6561`
  has generic Jacobian rank **149 = 156 − 7** at random points mod
  `2^31 − 1`, in two trials.  For S128 the rank is 121 = 128 − 7.
  - The kernel is the 7-dimensional trivial torus: one scalar per vertex,
    with product 1.
  - So the map is generically finite-to-one modulo trivial gauge, and the
    image has dimension 149.
  - A preimage of GHZ would lie in the degeneracy locus `rank J <= 135`,
    because the 21-dimensional GHZ-stabilizer subtorus acts on the fibre
    with finite kernel (the support characters have full rank 24).
  - This is a necessary condition, not a contradiction.
- **Closure certificates.**  A polynomial identity would express a product
  of constant-word coordinates as a linear combination of products that
  each contain a nonconstant word, all of the same torus multidegree.  Such
  an identity would exclude every configuration supported within the
  pattern, and every limit of such configurations.
  - Degree 2, colour pairs `01`, `02`, `12`: exact coefficient matrices mod
    1000003, for both patterns.
  - Degree 3, multisets `001`, `011`, `002`, `022`, `112`, `122`, and degree
    4, `0001`: evaluation sketches at `#rows + 40` random points mod
    `2^31 − 19`, for S156.
  - In every case the constant row is **not** in the span.  In fact all
    product rows are linearly independent (ranks 127/128, 1093/1094,
    2794/2795).
  - So **no closure certificate exists in these multidegrees**, and S156
    shows no low-degree sign of being outside the closure of its own image.
- **Laurent XL inside grids.**  For a hub pair `(p, v)` and a colouring `c`
  of the other six vertices, the nine words form a grid.  A degree-1
  Laurent certificate was searched inside each grid.
  - The search reproduces the S128 identity of Section 3.
  - For S156 it found **no certificate** in the 250 smallest grids (126
    live terms each, out of 20,328 grids without a constant word), before its 1,200 s cap.  Each
    S156 grid costs several seconds, against milliseconds for S128.  This
    is a small sample, not a census.
- **Full Gröbner basis.**  The system was gauge-fixed (24 independent
  entries set to 1), with inverse variables forcing exact support and the
  constant words nonzero.  Singular 4.3.2 `std`, `dp`, char 32003:
  - S128: 104 free variables plus inverses, 6,665 generators;
  - S156: 132 free variables plus inverses, 6,693 generators;
  - **both timed out at 1,200 s**: inconclusive, not a consistency result.
  - Smaller subsystems were no easier.  One 9-word S156 grid (24 free
    variables plus inverses) did not finish in 50 s.  The 99 three-term
    words of S128 did not finish in 300 s in any of three formulations
    (inverse variables, one Rabinowitsch variable, iterated saturation).
    Direct Gröbner bases are not the right tool at this size; the S128
    certificate came from the targeted Laurent XL.

### 4.3 Numerical exploration  [NUMERIC-EXPLORATION, not evidence]

Complex Levenberg–Marquardt on S156 (scratch script, not committed), with 4
starts of 400 iterations:

- one start stalled at residual² 1, losing one constant word;
- three starts reached residual² of about `5e-8` to `1e-7`, with `max|W|`
  between 50 and 560 and some entries driven numerically to 0.

This is the degeneration pattern already recorded for GHZ: GHZ is a border
limit of matching tensors, and a cost tending to 0 with diverging weights is
**not** a witness.  It says nothing about exact realizability on S156.  No
apparent exact witness arose, so there is nothing to escalate.

### 4.4 Why the known mechanisms are silent on S156  [OBSERVATION]

Every vertex of S156 has four full blocks.  So every row `(v, a)` has at
least 12 nonzero entries spread over four partners.  In every word, every
hub has live partners among its four `F`-neighbours, each weighted by a
dense six-vertex coefficient.

- The two-term rules (H2, and H3's CAN edges) need a live set of exactly two.
- PR needs every summand outside a 3-column cut to be dead.
- Neither situation arises: the SAT model finds a consistent `m`-assignment
  with no violated instance.

The only rigid ingredients are the twelve single entries of `H`.  These
cannot be gauged away together with the full blocks: only the diagonal
torus preserves the pattern, and a single entry is then just a scale.

## 5. The sharper next lemma this suggests

Write the `(p, v, c)` grid as a 3×3 matrix.  Expanding at `p` and then at `v`:

```text
E_c(a, b) = h_c * W_pv[a, b] + (R_c K_c S_c^T)(a, b),
```

where:

- `R_c[a, u] = W_pu[a, c_u]` and `S_c[b, u'] = W_vu'[b, c_u']`;
- `K_c[u, u'] = T_{V - {p, v, u, u'}}(c)`, a four-vertex coefficient;
- `h_c = T_{V - {p, v}}(c)`.

At a witness, `E_c` is 0 for nonconstant `c`, and has one nonzero corner
when `c` is constant.  S128 dies at the simplest instance:

- `R_c` restricted to the grid rows has support on two partners (rank ≤ 2
  structure);
- `W_pv` is a single entry, so `h_c W_pv` is a rank-one matrix unit;
- two rows of `R_c` are forced parallel.

On S156 every `R_c` has at least four full columns (the four `F` partners of
`p`), so no single grid is rank-deficient for support reasons.  Any
obstruction must couple many grids through shared entries.  At vertex 2 for
`a in {0,1}`, and at vertex 4 for `a in {0,2}`, the rows are purely
`F`-supported (12 entries over four full partners).  Hence:

- the vectors `Phi(c) in C^12` with `Phi(c)[u, c_u] = T_{V - {2, u}}(c)`, over
  all colourings `c != 0^7, 1^7` of `V - 2`, must span a subspace of
  codimension at least 2;
- equivalently, for each colouring `gamma` of the `F`-neighbours
  `{1, 3, 6, 7}`, the four 3×3×3 slices `T_{V - {2, u}}(gamma, .)` (over the
  colours of `{0, 4, 5}`) satisfy two independent linear relations, with
  coefficients that are the entries `W_2u[0, gamma_u]` and `W_2u[1, gamma_u]`.

The candidate next lemma is a **multi-partner grid-rank transport**: an
all-order statement that propagates this codimension-2 condition from vertex
2 through the six-vertex coefficients.  It would be the `k = 4` analogue of
the `k = 2` rank-one transport that kills S128.  This is a direction only;
it is not attempted here.

## 6. Status, scope and frontier

- S128: excluded with exact support (and within support, with six named
  entries nonzero) by an exact identity.  This is a finite statement about
  one Boolean pattern.  It is an instance of the already-proved H3 rule and
  creates no new reduction edge.
- S156: open.  Neither realizability nor non-realizability is established.
  The modular and SAT evidence above shows only that the known families and
  low-degree certificates do not decide it.
- Neither result is about unrestricted `n = 8` configurations.  The support
  model is a relaxation, and other `n = 8` patterns satisfying it exist and
  were not examined.

No theorem, branch closure, or reduction edge changes, so
`docs/current-frontier.md` needs no update.

## 7. Commands and runs

The scratch scripts live in the session scratchpad and are not committed:

- the system builder;
- the Jacobian rank;
- the Singular generators;
- the closure sketch;
- the Laurent XL (all words, and per grid);
- the numeric LM.

The one committed check is:

```text
python claims/finite/n08/verify_n8_recursive_support_s128_grid_identity.py
```

Model runs (pattern fixtures written in `physical-support-v1` form from the
inline listings):

```text
python tools/research/run_bounded.py --run-id n8r-s128-khpr-fixed --timeout-seconds 2400 --memory-mb 14000 -- \
  python claims/finite/n08/explore_general_block_recursive_support_model.py 8 --pattern-file pattern_S128.json \
  --killers --holonomy --plane-rigidity --no-symmetry --proof proof_S128 --out out_S128_khpr.json      # UNSAT, 2 rounds
python tools/research/run_bounded.py --run-id n8r-s156-khpr-fixed --timeout-seconds 2400 --memory-mb 14000 -- \
  python claims/finite/n08/explore_general_block_recursive_support_model.py 8 --pattern-file pattern_S156.json \
  --killers --holonomy --plane-rigidity --no-symmetry --proof proof_S156 --out out_S156_khpr.json      # SAT, 1 round, checker PASS
```

Other bounded run ids:

- `n8r-le3-forms`: Singular, 3 formulations, all timed out at 300 s;
- `n8r-lxl-s128-k4`;
- `n8r-gridxl-s128`;
- `n8r-gridxl-s156-b`;
- `n8r-full-gb-2`;
- `n8r-numlm-s156` (stopped early);
- `n8r-s128-exact-32003` (aborted: its input file was overwritten while it
  ran; no result).

The Singular jobs ran inside WSL with an inner `timeout` and `ulimit -v`,
because the Windows Job Object of `run_bounded.py` does not reach processes
inside WSL.  One early job orphaned this way was found and killed by PID.
