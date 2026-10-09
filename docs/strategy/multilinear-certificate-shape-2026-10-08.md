# Shape of the multilinear certificate that kills the 51-entry survivor — 2026-10-08

This is a dated research record.  The global Krenn–Gu status is
**UNRESOLVED**.  `docs/current-frontier.md` is not edited (see the last
section).

Evidence labels:

- **[PROVED]**: a hand proof in
  [`THREE_COLUMN_BILINEAR_GRID_THEOREM.md`](../../claims/arbitrary-order/THREE_COLUMN_BILINEAR_GRID_THEOREM.md),
  whose identities are replayed by its verifier.
- **[EXACT]**: an exact computation by a committed script.  These are
  primary runs only; there is no independent audit.
- **[OBSERVATION]**: a reading of the data.

Inputs:

- [`row-space-all-orders-attempt-2026-10-08.md`](row-space-all-orders-attempt-2026-10-08.md),
  with the BL survivor `tests/fixtures/bl_full_word_survivor_n6_51.json`;
- [`holonomy-support-model-2026-10-08.md`](holonomy-support-model-2026-10-08.md),
  Section 5.4;
- the review
  [`TWO_TERM_RELATION_CLOSURE_THEOREMS_REVIEW_2026-10-08.md`](../audits/TWO_TERM_RELATION_CLOSURE_THEOREMS_REVIEW_2026-10-08.md);
- `claims/finite/n06/SIX_VERTEX_SUPPORT_SURVIVOR_PATTERNS_EXACT_REFUTATION.md`.

The question is what kind of multilinear relation kills these survivors,
stated so that it could be a theorem at every order.

## 0. The two 51-entry survivors are one support

[EXACT] The holonomy-model survivor (Section 5.4 there) and the BL fixture
are the same support up to a vertex relabelling and a common colour
permutation.  There are 6 isomorphisms, for example vertex map
`(0,2,1,3,5,4)` with colour map `(2,0,1)`.  The fixture's automorphism
group has order 6.  So one computation covers both, which settles the open
item "identity of the two supports was not checked".  Labelling below is
the fixture's: inner triangle `T = {0,2,3}` with full blocks; outer vertices
`U = {1,4,5}` with inner colours `sigma = (1:2, 4:0, 5:1)`.

## 1. Equations

[EXACT] Every supported entry is an unknown and every unsupported entry is
0.  Mixed words give `T(w) = 0` and constant words give `T(w) - 1 = 0`.

- Full system: 51 unknowns and 108 nonzero equations (105 mixed and 3
  constant; 621 mixed words have no live matching).
- Slice: the 27 words with `U` pinned to `sigma`.  These are 27 equations
  in 21 unknowns, and all 27 words are mixed because `sigma` is injective.

## 2. Minimal certificates (exact Macaulay test, physical entries)

A degree-`D` certificate is `sum_w g_w E_w = c * mu`, with `c` a nonzero
rational, `mu` a monomial in the unknowns (allowed to be `1`), and
`deg g_w <= D`.  On the torus this is a contradiction; it is the
saturation by the entries, written with an explicit monomial.  The test
splits `m * E_w` into blocks of the vertex-colour multigrading.  For the
full system the three constant-word degrees are quotiented out.  It then
looks for a unit row in the exact RREF over `Q` (python-flint `fmpq_mat`).

| system | D | rows | blocks | monomial in span? |
|---|---|---|---|---|
| full | 0 | 108 | 106 | no |
| full | 1 | 5,616 | 3,244 | no |
| full | 2 | 148,824 | 42,454 | **no** |
| slice | 0, 1, 2 | 27 / 1,377 / 35,802 | 27 / 810 / 10,620 | no |
| slice | 3 | 632,502 | 86,509 | **yes**, in 48 blocks |

[EXACT] So **in physical entries the minimal multiplier degree is exactly
3**.  It is at least 3 for the full 108-equation system, and the slice gives
3.  Every one of the 48 degree-3 blocks is a `2 x 2 x 2` cube of 8 words: two
colours at each inner vertex and `U` pinned.  Each has 14 rows and exactly
one monomial in its span.  On the slice, every degree-3 certificate needs
all 8 words of its cube; this was checked by an exact test of every word
subset of every hit block.  The full system was not searched at `D = 3`.

A 4-word certificate exists at `D = 4` (Section 3).  The review's
normalized-coordinate result, `D <= 2` on the slice, is consistent with
this: the torus normalization sets 11 entries to 1 and absorbs one degree
(a heuristic reconciliation, not an exact statement; relabelled after the
same-day review).

## 3. The certificate shape in graph terms

[EXACT] The slice coefficient is a `3 x 3` permanent across the cut,
`T(w) = perm(r_{0,w0}, r_{2,w2}, r_{3,w3})`, with
`r_{t,c} = (W_t1[c,2], W_t4[c,0], W_t5[c,1])`.  The reason is that `U` is
independent at `sigma`: `W14[2,0]`, `W15[2,1]` and `W45[0,1]` are
unsupported.  Each inner vertex has exactly:

- one **full row**: `r_{0,1}`, `r_{2,0}`, `r_{3,2}`;
- two **killer-plane rows** with a zero at a distinct outer column:
  vertex 0 at column 5, vertex 2 at column 4, vertex 3 at column 1.

So each inner vertex's two killer-plane rows span a plane; with the full
row added, the three rows of a vertex generically span all of `F^3`
(wording corrected after the same-day review).

Two certificate shapes kill the support.  Both are replayed exactly against
the actual word polynomials (48 and 96 instances respectively; the second
count includes relabellings of the same identity).

- **Bilinear grid, 4 words, multiplier degree 4** (Theorem 2).  Fix the
  third inner vertex at its full colour, say `x = r_{3,2}`.  Pin `U` and
  put colour 0 or 1 at each of vertices 0 and 2.  The four words `020201`,
  `120201`, `021201`, `121201` give the `2 x 2` grid `y_i^T B_x z_j`, with
  `y` the rows of vertex 0 and `z` the rows of vertex 2.  Here
  `B_x = [[0,x5,x4],[x5,0,x1],[x4,x1,0]]` is the hollow matrix of the full
  row, with `det B_x = 2 x1 x4 x5`.  The certificate is
  `sum g_ij T(w_ij) = 2 W04[00] W05[11] W13[22] W24[00] W25[11] W34[20] W35[21]`.
  The multipliers `g_ij` are the explicit `2 x 2` cofactors of the bordered
  grid matrix `G = [Z e_q]^T B_x [Y e_p]`.  Their entries are:
  - grid values `T(w)` (degree 3);
  - border values, i.e. one full-row entry times one inner-row entry
    (degree 2);
  - the corner `x_k` (degree 1).

  In graph terms: two inner vertices, three outer columns, and the third
  inner vertex frozen at its full colour acts as the "middle" form.
- **Cube, 8 words, multiplier degree 3** (Proposition 4).  Take two colours,
  the full row and a killer-plane row, at each inner vertex.  The
  alternating sum `sum (-1)^(i+j+k) phi(complementary rows) T(w_ijk)` equals
  twice a product of three `2 x 2` minors, and each minor is a monomial
  because the killer-plane row has a zero where the full row does not.  For
  example, on the words `020001 020201 021001 021201 120001 120201 121001
  121201`, the identity gives `2 W04[00] W05[11] W13[22] W24[00] W25[11] W34[00]`.
  The multipliers `phi` are trilinear: one entry from the complementary row
  of each inner vertex.  The degree-3 identity exists exactly when two of
  the three minors use the same pair of outer columns.

Neither shape uses a two-term transport; the three-, four- and six-term
fibres enter linearly with polynomial multipliers.  This matches the
earlier hand derivation ("three-term relations multiplied by monomials").

## 4. The general statements and their status

[PROVED] All of the following are in the theorem document.

- **Theorem 1 (all even `n`).**  The two-vertex expansion
  `T(w_{βγ}) = W_ab T_R(c) + sum_{u≠v} y_β[u] z_γ[v] T_{R-u-v}(c)`.
- **Theorem 2, three-column bilinear grid (all even `n >= 4`).**  Assume
  every order-`(n-4)` complementary coefficient vanishes outside three
  columns `C`, and that `W_ab T_R(c) = 0`.  Then
  `2 h12 h13 h23 det[y y' e_p] det[z z' e_q]` is an explicit degree-two
  cofactor combination of the four grid values.  At support level this is
  a contradiction when:
  - the three `h`'s are nonzero;
  - both row pairs are staircase;
  - the four words are mixed.
- **Theorem 3, permanent plane rigidity (char ≠ 2).**  The only triples of
  2-planes in `F^3` on which the trilinear permanent vanishes are
  `H_u, H_u, H_u`, with `H_u` a coordinate plane.  The key step is the
  full-row lemma: `det B_x = 2 x1 x2 x3`, so a full `x` makes
  `perm(x, ·, ·)` nondegenerate.
- **Proposition 4.**  The closed-form degree-3 cube identity.  The
  all-equal and pairwise-distinct minor choices are not in the degree-3
  span.
- **Corollary 5 (six-vertex cut).**  Theorems 2 and 3 specialized to a
  3-vs-3 cut with `U` independent at `sigma`.

The suggested statement "the ideal of the 27 cross permanents, saturated by
the entries, is the unit ideal" is **false as a general statement**.  If
every row of all three inner vertices has a zero at the same outer column,
the permanents vanish identically (Theorem 3, converse).  A sufficient
condition is Corollary 5 (i): one full row and two staircase pairs.
Condition (ii) of Corollary 5 is a statement about *values* (Theorem 3), not
about the ideal: the same-day [review](../audits/THREE_COLUMN_BILINEAR_GRID_THEOREM_REVIEW_2026-10-08.md)
exhibits proportional full rows `(1,1,1), (1,1,1), (1,1,-2)` for which all
eight cube permanents vanish with every entry nonzero, so "unit ideal
whenever (ii)" is false.  A repaired support-level condition, which the
51-entry survivor satisfies, is: at each inner vertex two rows with distinct
supports whose union is all three columns.  Necessity of any of these
conditions is not proved.

## 5. All-order form

[PROVED] **Theorem 2 is the all-`n` form.**  The 3-vs-`(n-3)` cut becomes:
two free vertices `a, b`, a pinned background on `R`, and three columns
`C`.  The "`U` independent at `sigma`" condition becomes the vanishing of
the complementary coefficients `T_{R-u-v}(c)` for pairs not inside `C`.  At
`n >= 8` these are recursive coefficients, so the theorem is a valid clause
family in the recursive support model at every level.  Its premises and
conclusion are literals of the model:

- premises: `not m[...]` for the vanishing coefficients, `m[...]` for the
  three `h`'s, `g`-literals for the staircases, **and** the killed `a`-`b`
  term (hypothesis 2 of Theorem 2; a clause encoded without it is unsound,
  as the same-day review notes);
- conclusion: one of the four grid coefficients is nonzero.

It sits beside the rules `H2`/`H3` of the holonomy note as a rank-3 (hollow)
companion of the rank-2 two-matching grid.  Two other all-`n` forms are
also proved:

- `k`-vs-`k` cuts with `U` independent give `perm_k`;
- single-entry inner rows contract `perm_k` to `perm_3`.

[PROVED, boundary] The naive `k`-ary support statements are false:

- plane rigidity fails at `k = 2`;
- the full-row bound fails at `k = 4`.  Explicitly, the full vectors
  `x = (1,1,1,1)` and `x' = (1,-4,-4,-1)` make `perm_4(x, x', ·, ·)`
  singular.

Only at `k = 3` is the relevant determinant a monomial.

## 6. Controls

[EXACT] The instances found by the application verifier:

| support | Theorem 2 instances | Proposition 4 instances | note |
|---|---|---|---|
| BL51 / HOL51 | 48 | 96 | the survivor |
| HOL50 (holonomy no-symmetry survivor) | 48 | 96 | also refuted by matching-level transport |
| P63 | 48 | 96 | also refuted by H3 |
| P41 | 0 | 288 | also refuted by H2 |
| P27 | 0 | 0 | refuted by two-term relations only |

[OBSERVATION] The cut/permanent mechanism and the two-term mechanisms
overlap but neither contains the other.  P27 needs the odd-cycle/grid rule,
and BL51 needs the multilinear rule.

## 7. What is not done

- The new clause family was not added to the recursive support model, so
  whether it makes the `n = 6` (or `n = 8`) model UNSAT is untested.  That
  is the obvious next experiment.
- `TM_D` of the attempt note is now measured on one support in physical
  entries (`D = 3` exactly).  No uniform bound is proved.
- There is no occurrence theorem: nothing here proves that a witness at
  general `n` must contain a three-column grid or a permanent cut.

## Commands

```text
python claims/arbitrary-order/verify_three_column_bilinear_grid_theorem.py
python claims/finite/n06/verify_51_entry_survivor_bilinear_grid_certificates.py
python tools/research/run_bounded.py --run-id <id> --timeout-seconds 600 --memory-mb 6000 -- \
  python claims/finite/n06/search_51_entry_survivor_multilinear_certificates.py --system slice --max-degree 3
python tools/research/run_bounded.py --run-id <id> --timeout-seconds 1800 --memory-mb 8000 -- \
  python claims/finite/n06/search_51_entry_survivor_multilinear_certificates.py --system full --max-degree 2
```

Recorded runs:

| run id | output | time |
|---|---|---|
| `mlshape-slice-d3-c` | D = 3 found, 48 blocks, minimal 8 words | 12 s at D = 3 |
| `mlshape-full-d2-a` | none at D <= 2 | 2 s |
| `mlshape-verify-thm-a` | PASS | 10 s |
| `mlshape-apply-a` | the table in Section 6 | 27 s |

The 27-case generic cube classification (Proposition 4's "exactly two
equal" criterion) was run once as a scratch script (`mlshape-cube-generic-a`).
The verifier replays one representative of each of the three symmetry
classes.

## Frontier

There is no frontier change.  Every result is either:

- a conditional implication valid at every order (Theorems 1–3,
  Proposition 4), with no occurrence theorem supplying its premises; or
- an exhibit inside the already-proved six-vertex order.

No order is closed, no reduction edge is created, and no route is refuted,
so `docs/current-frontier.md` needs no update.
