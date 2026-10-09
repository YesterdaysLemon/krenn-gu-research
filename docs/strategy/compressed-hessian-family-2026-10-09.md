# The compressed-Hessian family CH, and whether it is hereditary — 2026-10-09

This is a dated research record.  The global Krenn–Gu status is
**UNRESOLVED**, and nothing here changes it.  No theorem about witnesses is
added, withdrawn or re-scoped.  Section 9 says what the frontier needs.

Evidence labels:

- **[EXACT]**: a hand proof (a few lines each, given here).  Lemma 1, the
  Cauchy–Binet expansions and Lemma 5 were also checked by exact integer
  arithmetic on random configurations (scratch, Section 10); that is a
  replay of the identities, not the proof.
- **[SAT-RUN]**: a bounded solver run (CaDiCaL 1.5.3 via python-sat).  Every
  SAT model passed the script's independent support-level checkers.  No
  UNSAT answer here carries a DRAT proof; none is load-bearing.
- **[OBSERVATION]**: a reading of one solver model, not a theorem.

## 0. Answer

1. **Lemma (EXACT, every order, every configuration).**  For a pair
   `{u, v}`, `B = A - {u, v}` and a word `γ` on `B`, the compressed Hessian
   `H_γ = A_γ Θ_γ B_γ^T` satisfies `H_γ[X,Y] = -T_B(γ) W_uv[X,Y]` on every
   block `X x Y` whose words `(x, y, γ)` vanish.  At the top set of a witness
   this gives `H_γ ∈ span(W_uv)` for every nonconstant `γ`, so
   `rank H_γ ∈ {0, rank W_uv}`.  If `T_B(γ) = 0` (an order-`n` (G) zero),
   then `H_γ = 0`; if `W_uv != 0`, the converse holds too.  The minor form is
   `det H_γ[X,Y] = (-T_B(γ))^k det W_uv[X,Y]`.
2. **Clause family CH (EXACT soundness, any field, no genericity).**  CH
   forbids three zero-pattern conjunctions (Section 3.2).  A determinant is
   certified only through a Cauchy–Binet expansion with exactly one supported
   product (nonzero) or none (zero).  Only one clause, `(b)`, can force a
   zero `T_B(γ) = 0`.  It needs a **single-transversal `k x k` minor of
   `W_uv` with `k >= 2`**, so it is vacuous whenever `W_uv` is supported in
   one row or one column, in particular for every column-killer block.  The
   `k = 1` part of CH is already implied by (L) and (F') (Proposition 4).
3. **Heredity test (SAT-RUN).**  The pair relaxation `D_6` of order 8, with
   killers, anchors, H2/H3, PR **and CH**, is **SAT**.  Its run is identical
   to the run without CH: 140 s, 38 rounds, and CH is never violated.
   - The deleted pair's block is a column killer, so `(b)` has no instance.
   - We then forced `W_uv` to carry a certified rank-2 or rank-3 minor.
     With a rank-3 minor, `(b)` fires: 196 lazy instances with the two-step
     family alone, and 349 with the one-step factorizations added.  With a
     rank-2 minor it fires 0 and 8 times respectively.  The relaxation is
     still SAT in every case, in 4 to 11 rounds.
   - In the final models, every eligible word of `B` (every nonconstant `γ`
     with `T_B(γ) != 0`) has at least two supported Cauchy–Binet products in
     each of the three factorizations, so `det H_γ` is never
     support-certified.
   - The six-set keeps 222 to 717 of its 726 nonconstant words nonzero.
   - The four-set inside six (`D_4`) is SAT in one round, also with CH.
   - At order 6, CH with only (L), (F'), (G) is satisfied by the full-support
     pattern at **every** order (proved).  With the full families plus CH,
     order 6 is still UNSAT, in the reference trajectory, and CH adds no
     clause.
4. **Q2.**  CH is **not** a support-level hereditary input.  With
   `Q = P + CH`, (Q2) is the circular statement of the induction note's
   Section 5.1.  The seeded part of CH does not generate the needed (G)
   zeros on any six-set of the order-8 relaxation (item 3), and the
   `(not m)`-premise part excludes nothing on its own.
   - **Sharper statement.**  The value-level content of CH is exactly a
     two-ancilla contraction (Lemma 5).  Every order-`(n+2)` witness with one
     pair whose block is not a single entry yields `GHZ(n,3)`, realized by
     `n` three-colour vertices plus two one-colour vertices with no edge
     between them.  So the induction's heredity holds exactly at the value
     level for ancilla-extended classes.  The whole obstruction moves to one
     finite question: can `GHZ(6,3)` be realized with two one-colour
     ancillas (Section 8)?

**Most load-bearing fact.**  CH's only zero-generating clause needs the
determinant of the compressed Hessian to be support-certified zero.  In
every model the solver produced, including models with `W_uv` forced to
full certified rank, every eligible minor has at least two supported
Cauchy–Binet products.  So the rank condition that Lemma 1 imposes on the
deleted pair is invisible to zero patterns, and its exact content is the
two-ancilla identity of Lemma 5, not a support clause.

## 1. Question and inputs

The question comes from the coordinator.  The support-model induction note
[`support-model-induction-2026-10-09.md`](support-model-induction-2026-10-09.md)
proved the pair expansion (its Proposition 3).  Its Section 5.4 named the
compressed-Hessian rank condition as the candidate hereditary input, and it
left open whether that input is hereditary in the sense of (Q2).

Inputs, all on `origin/main` at `f4e5b881`:

- that note (Sections 2–5: Propositions 1–3, `D_n`, the schema
  (Q1)–(Q3));
- [`multi-partner-grid-transport-2026-10-09.md`](multi-partner-grid-transport-2026-10-09.md)
  (the G(r,s)/M clause style: "a zero pattern certifies a minor nonzero only
  through a single supported transversal");
- [`s156-hub-trichotomy-2026-10-09.md`](s156-hub-trichotomy-2026-10-09.md)
  (diagonal anchors);
- the model script
  [`explore_general_block_recursive_support_model.py`](../../claims/finite/n08/explore_general_block_recursive_support_model.py).

Conventions are the script's:

- `W_ij[a, b]`, where `a` is the colour at `i`;
- `T_A(w)` is the matching sum of `W` restricted to an even set `A`, with
  `T_∅ = 1`;
- a witness on `V` has `T_V = GHZ` up to the diagonal torus: nonconstant
  words vanish and `T_V(c...c) = λ_c != 0`.

Fix an even set `A`, a pair `{u, v} ⊆ A`, put `B = A - {u, v}`, and let `γ`
be a word on `B`.  The matrices are indexed by `z, z' in B` and colours
`x, y`:

```text
A_γ[x, z]  = W_uz[x, γ_z]                Θ_γ[z, z'] = T_{B-{z,z'}}(γ|)  (z != z'),  Θ_γ[z, z] = 0
B_γ[y, z]  = W_vz[y, γ_z]                K_γ[z, y]  = T_{A-{u,z}}(y, γ|)     K'_γ[x, z] = T_{A-{v,z}}(x, γ|)
H_γ = A_γ Θ_γ B_γ^T = A_γ K_γ = K'_γ B_γ^T.
```

The last line holds by Laplace expansion of `T_{A-{u,z}}` at `v` (so
`K_γ = Θ_γ B_γ^T`) and of `T_{A-{v,z}}` at `u` (so `K'_γ = A_γ Θ_γ`).

Note the levels: `Θ_γ` holds coefficients of `B` of order `|A| - 4`, while
`K_γ` and `K'_γ` hold order-`(|A|-2)` coefficients of sets containing
exactly one of `u` and `v`.

## 2. The value-level lemma  [EXACT]

**Pair expansion** (Proposition 3 of the induction note, at any level).
For every configuration over a commutative ring and every `A`, `{u, v}` and
`γ`,

```text
( T_A(x, y, γ) )_{x,y} = T_B(γ) W_uv + H_γ.                                  (1)
```

**Lemma 1 (block form; every configuration, every level).**  Let
`X, Y ⊆ {0,1,2}` with `|X| = |Y| = k`.  Suppose `T_A(x, y, γ) = 0` for every
`(x, y) in X x Y`.  Then

```text
H_γ[X, Y] = -T_B(γ) W_uv[X, Y]     and     det H_γ[X, Y] = (-T_B(γ))^k det W_uv[X, Y].     (2)
```

*Proof.*  Restrict (1) to the block; the left side is zero.  The
determinant of a scalar multiple is the `k`-th power times the
determinant.  ∎

**Corollary 2 (top set of a witness; all orders).**  Let `W` be a witness
on `V`, with `|V| = n + 2`, and take `A = V`.

- (a) For nonconstant `γ`, all nine words `(x, y, γ)` vanish, so
  `H_γ = -T_B(γ) W_uv`.
  - Thus `H_γ ∈ span(W_uv)`, a fixed matrix independent of `γ`.
  - `rank H_γ` is `rank W_uv` if `T_B(γ) != 0`, and `0` otherwise.
  - `T_B(γ) = 0` forces `H_γ = 0`.  In particular, imposing the order-`n`
    (G) zero of `B` at `γ` forces the compressed Hessian to vanish.
  - If `W_uv != 0`, then conversely `H_γ = 0` forces `T_B(γ) = 0`.
- (b) For `γ = c^n`, `H_γ = λ_c E_cc - T_B(γ) W_uv`.  Every block `X x Y`
  with `c ∉ X` or `c ∉ Y` still satisfies (2).

*Proof.*  Lemma 1 with `X = Y = {0, 1, 2}`, and the GHZ values.  ∎

**Cauchy–Binet expansions.**  Over any commutative ring, for
`|X| = |Y| = k`:

```text
det H_γ[X,Y] = Σ_{S,S'} det A_γ[X,S] det Θ_γ[S,S'] det B_γ[Y,S']       (F3, two-step)
             = Σ_S      det A_γ[X,S] det K_γ[S,Y]                       (F1, one-step at u)
             = Σ_S      det K'_γ[X,S] det B_γ[Y,S]                      (F2, one-step at v)
```

The sums run over `k`-subsets `S, S'` of `B`.  Each summand expands into
`k!` (for F1 and F2) or `(k!)^3` (for F3) signed products of atoms, where
each atom is one entry of `W`, `Θ`, `K` or `K'`.  The diagonal of `Θ` is the
constant zero atom.

## 3. The support-level family CH  [EXACT]

### 3.1 Certificates

An atom is **supported** when its model literal is true: `g` for an entry of
`W`, and `m` for a coefficient.  A product of atoms is supported when all of
its atoms are.  For a factorization `f` in `{F3, F1, F2}`, let `nH_f` be
the number of supported products in the `f`-expansion of `det H_γ[X,Y]`.
Let `nW` be the number of supported transversals of `W_uv[X,Y]`.

- `ONE_f` (`nH_f = 1`) certifies `det H_γ[X,Y] != 0`.
- `ZERO_f` (`nH_f = 0`) certifies `det H_γ[X,Y] = 0`.
- `W-ONE` (`nW = 1`) certifies `det W_uv[X,Y] != 0`.
- `W-ZERO` (`nW = 0`) certifies `det W_uv[X,Y] = 0`.

An expansion with two or more supported products certifies nothing.  This
is the G(r,s) rule of the multi-partner note: a determinant is
support-certified nonzero only when exactly one transversal survives.

### 3.2 Clauses

The premise is `P = AND_{(x,y) in X x Y} not m[A, (x, y, γ)]`.  Write
`s = m[B, γ]`.  The family CH consists of, for each `f`:

```text
(a1_f)  not ( P  and  ONE_f  and  not s )
(a2_f)  not ( P  and  ONE_f  and  W-ZERO )
(b_f)   not ( P  and  W-ONE  and  s  and  ZERO_f )
```

These are encoded for `k = 2, 3`.  The case `k = 1` adds nothing, by
Proposition 4 (i).

Each instance is written as one clause.  It contains:

- the premise literals;
- the literals of the one supported product;
- for every other product, one false atom (respectively, for `ZERO_f`, one
  false atom of every product).

### 3.3 Soundness

Take any configuration over a field (or any integral domain) whose zero
pattern satisfies a forbidden conjunction.

- By `P` and Lemma 1, `det H_γ[X,Y] = (-T_B(γ))^k det W_uv[X,Y]`.
- Under `ONE_f`, the expansion along the exact identity `f` equals one
  product of nonzero elements, so `det H_γ[X,Y] != 0`.
  - Hence `T_B(γ) != 0`, contradicting `not s` in `(a1)`.
  - Hence `det W_uv[X,Y] != 0`, contradicting `W-ZERO` in `(a2)`.  Under
    `W-ZERO` every transversal product of `W_uv[X,Y]` has a zero factor.
- In `(b)`, `W-ONE` and `s` make the right side nonzero.  `ZERO_f` makes
  the left side zero.  ∎

No division, no characteristic assumption and no genericity is used.  The
identities hold over any commutative ring, and the certificates use only
the fact that a product of nonzero elements of an integral domain is
nonzero.  Products that coincide or cancel formally are harmless:
"exactly one supported product" is a statement about the expansion as
written.

**Scope.**  With the premise `P` written as `not m` literals, CH holds for
the zero pattern of **every** configuration at **every** level.  At the top
set of a witness, `P` is supplied by (G) for every nonconstant block word.
F3 uses exactly the atoms of the brief:

- the attachment entries `W_u.` and `W_v.`;
- the block `W_uv`;
- the order-`(n-2)` coefficient supports of `B`;
- `s` itself.

F1 and F2 also use the order-`n` coefficients of the sets `A - {u, z}` and
`A - {v, z}`.

### 3.4 What CH can and cannot conclude

**Proposition 4.**

- **(i) `k = 1` is already encoded.**  At `k = 1`, `(a1)`, `(a2)` and `(b)`
  follow by unit propagation from (L) and (F') at the hub `u` of `A` and the
  hub `v` of the sets `A - {u, z}` (for F3 and F1), or symmetrically at `v`
  and `u` (for F2), together with `P`.

  *Proof.*  Take F3 with `nH = 0`.  For each `z` with `W_uz[x, γ_z]`
  supported, the hub-`v` live set of `(A - {u,z}, (y, γ|))` is empty, so
  (L) makes that coefficient zero.  The hub-`u` live set of
  `(A, (x, y, γ))` is then contained in `{v}`.  Its term is live exactly
  when `g[uv, x, y]` and `s` hold, and (F') forbids a live set of size one
  under `P`.  This gives `(b)`.

  For `nH = 1`, with unique live product `(z0, z0')`:
  - (F') at `v` makes `K[z0, y]` true;
  - (L) makes every other `K[z, y]` false;
  - so the hub-`u` live set is `{z0}`, plus `v` when `g[uv,x,y]` and `s`
    hold;
  - (F') then forces `g[uv,x,y]` and `s`.

  This gives `(a1)` and `(a2)`.  F1 and F2 are the same argument with one
  step fewer.  ∎

- **(ii) Only `(b)` generates a zero of `T_B`.**  The conclusion of `(a1)`
  is `s`, and that of `(a2)` is a supported transversal of `W_uv`.  Read
  backwards, `(a1)` and `(a2)` can force one atom of the unique product to
  be zero.  That atom is an attachment entry, a `Θ` coefficient of order
  `n - 2`, or a `K`/`K'` coefficient; it is never `T_B(γ)`.
- **(iii) `(b)` needs `rank W_uv >= 2` at the support level.**  `W-ONE`
  for a `k x k` minor requires a matching of size `k >= 2` in the support of
  `W_uv`.  So `(b)` has no instance when the support of `W_uv` lies in one
  row or one column.  This covers every column killer and every single
  entry.  The killer theorem supplies such blocks at every vertex.
- **(iv) `ZERO_f` is a König condition.**  For example, `ZERO_F1` holds iff
  every `k`-subset `S` has a support-zero factor `A_γ[X, S]` or
  `K_γ[S, Y]`.  Its simplest instance is that the rows `X` of `u`'s
  attachments at the colours `γ` have no matching of size `k`.  At `k = 2`,
  the pure row case (both rows supported on one common partner) is again
  implied by (L) and (F'), through the coefficients `K[z0, ·]`.  The new
  content of CH is the mixed and `k = 3` certificates.
- **(v) CH plus (L), (F') and (G) is satisfiable at every even order
  `n >= 4`.**  Take every `g` true, every `m` true below the top, and (G)
  at the top.
  - (L) and (F') hold: each nonconstant top word has `n - 1 >= 3` live
    terms at every hub.
  - In CH, `nW` is 2 or 6, and every expansion with `nH_f >= 1` has
    `nH_f >= 2`.  For `k = 2` the summand `S = S' = {z1, z2}` of F3
    already gives `2 · 1 · 2` products.  For `k = 3` with `|B| = 2`,
    `nH = 0`, but `nW = 6 != 1`.
  - The `(not m)`-premise instances below the top are vacuous.

  So CH, like H2/H3/PR (Proposition 1 of the induction note), excludes
  nothing without the killers.

## 4. The script change

The script is
[`explore_general_block_recursive_support_model.py`](../../claims/finite/n08/explore_general_block_recursive_support_model.py).

- **`--compressed-hessian`** adds CH lazily, in the existing CEGAR loop.
  - `check_ch(N, gsup, msup, frames, ks, stats, factorizations)` is the
    independent support-level checker.  It computes `nH_f` as products of
    per-factor transversal-count matrices.
  - `GSM.ch_instances` / `_ch_clause` build one clause per violation, by
    enumerating the expansion explicitly.  Each clause is **asserted to be
    falsified** by the model that produced it.  The final SAT acceptance
    re-runs `check_ch`.
- **Frames.**
  - Default: the top set with every pair.
  - With `--g-minus`: only the deleted pair `(n, n+1)` at `V`.  This is the
    only pair whose `Θ` lies in `D_n`'s variables.
  - `--ch-all-levels` adds every even `A` below the top, with the
    `not m` premises.
- **`--ch-orders`** (default `2,3`).
- **`--ch-factorizations`** (default `F3`, the family of the brief;
  `F3,F1,F2` adds the one-step expansions).
- **Default behaviour is unchanged.**  For `GSM(4)` and `GSM(6)`, with and
  without killers and anchors, and for `PairDecoratedGSM(4)` and
  `PairDecoratedGSM(6)` with killers:
  - the SHA-256 of the base clause list matches HEAD `f4e5b881`;
  - so do the variable and clause counts (ten comparisons, all identical;
    run `chs-cmp-head`).
- **Tests** (`tests/test_general_block_support_model_fast.py`, class
  `CompressedHessianTests`):
  - The exact zero patterns of twelve random sparse integer configurations
    on six vertices satisfy CH at every level in all three factorizations,
    with a nonzero number of premise instances having a certified side.
  - On random assignments, every reported violation of every kind and
    factorization produces a clause falsified by that assignment, for
    `GSM(6)` and for `PairDecoratedGSM(4)`.

## 5. Experiments  [SAT-RUN]

All runs went through `tools/research/run_bounded.py`.  Run ids are in
Section 10.  Every SAT model passed the independent checkers, including
`check_ch` with the factorizations of that run.

| run | families | result | time, rounds | CH instances added |
|---|---|---|---|---|
| order 6 | killers, H2/H3, PR, CH (F3) | UNSAT (uncertified) | 245 s, 77 | **0** |
| order 6 | killers, H2/H3, PR, CH (F3,F1,F2) | UNSAT (uncertified) | 323 s, 77 | **0** |
| order 6 | CH (F3) only, with (L)(F')(G) | SAT | 0.4 s, 1 | 0 (full support, 135 entries) |
| order 6 | killers, CH (F3) | SAT | 0.7 s, 1 | 0 |
| order 6 | killers, anchors, CH (F3) all levels | SAT | 0.8 s, 1 | 0 |
| order 6 | killers, anchors, CH (F3,F1,F2) all levels | SAT | 1.1 s, 1 | 0 |
| `D_6` (six-set in eight) | killers, anchors, H2/H3, PR, CH (F3) | **SAT** | 140 s, 38 | **0** |
| `D_6` | the same, CH (F3,F1,F2) | **SAT** | 200 s, 38 | **0** |
| `D_6` + `W_uv` certified rank 2 (scratch) | the same, CH (F3) | SAT | 42 s, 10 | 0 |
| `D_6` + `W_uv` certified rank 3 (scratch) | the same, CH (F3) | SAT | 12 s, 4 | 196 (`b`, `k = 3`) |
| `D_6` + `W_uv` certified rank 2 (scratch) | the same, CH (F3,F1,F2) | SAT | 59 s, 11 | 8 (`b`: 4 F1, 4 F2) |
| `D_6` + `W_uv` certified rank 3 (scratch) | the same, CH (F3,F1,F2) | SAT | 24 s, 6 | 349 (`b`: 280 F3, 65 F2, 4 F1) |
| `D_4` (four-set in six) | killers, anchors, H2/H3, CH (any; also rank 2, 3) | SAT | <= 2 s, 1 | 0 |

"Certified rank `k`" means an extra hypothesis: `W_uv` has a `k x k` minor
with exactly one supported transversal.  It was imposed by a scratch driver
that subclasses `PairDecoratedGSM` and runs the unchanged `main()`.  This
hypothesis is not implied by anything.  It asks whether `(b)` transfers
zeros when it is allowed to fire.

**(a) Order 6.**  The full-family run with CH reproduces the reference
trajectory: 77 rounds and 576 PR instances, all at level 6, as in the
hyperdeterminant note.  CH is never violated.  CH alone with (L), (F'),
(G) is SAT through the full-support pattern of Proposition 4 (v).  With
killers (and anchors, at every level, in all factorizations) it is still
SAT in one round.  **CH does not replace H2/H3/PR at order 6, and it does
not exclude order 6 on its own.**

**(b) Heredity test.**  `D_6` with CH is SAT.  The run with F3 is
**identical** to the run without CH (`sind-g6-kahp`): 38 rounds, 239,129
lazy instances, and the same model.  CH had no violated instance in any
round.  The forced-rank variants make `(b)` fire, and the solver escapes in
a few rounds (Section 6).

**(c) Four-set inside six.**  `D_4` with CH is SAT in one round with no CH
instance, in every factorization, with and without the rank hypotheses
[OBSERVATION]:

- In two of the three decoded models, every nonconstant word of the
  four-set is already zero.
- In the rank-3 model, the four-set carries exactly the order-4 GHZ pattern,
  with its own killers and anchors.

At order 4 the support model is not the obstacle; the six-vertex exclusion
is not pair-local (induction note, 4.1).

### 5.1 The two runs with all three factorizations

- **Order 6, full families, CH (F3,F1,F2):** UNSAT (uncertified), 323 s,
  77 rounds, 322,856 lazy instances (576 PR), and 0 CH instances.  These
  are the same counts as with F3 alone; the extra time is the checker.
- **`D_6`, CH (F3,F1,F2):** SAT, 200 s, 38 rounds, 0 CH instances, and the
  same model as without CH.  This run went through the scratch
  model-capture driver, which calls the unchanged `main()` with no extra
  hypothesis.

So, in the unforced runs, **no CH instance in any factorization was ever
violated by any intermediate model**: 77 rounds at order 6 and 38 rounds
of `D_6`.

## 6. The decoded models: which CH premise fails  [OBSERVATION]

| model | `W_uv` (the deleted pair) | nonconstant words of `B` nonzero | constant words of `B` nonzero |
|---|---|---|---|
| `D_6` + CH (F3 or all) | `01 11 21` (column-1 killer) | 717 / 726 | 3 |
| rank 2, all factorizations | `00 11 22` (diagonal) | 222 / 726 | 1 |
| rank 3, F3 | `01 02 10 20 22` | 453 / 726 | 3 |
| rank 3, all factorizations | `00 01 10 20 22` | 338 / 726 | 3 |

- **Unforced `D_6`.**  `W_uv` is a column killer.  Every `2 x 2` and
  `3 x 3` minor has a zero column, so `nW = 0` and `(b)` has no instance
  (Proposition 4 (iii)).  `(a1)` and `(a2)` hold because no Cauchy–Binet
  expansion in the model has exactly one supported product.  **The failing
  premise is `W-ONE`.**
- **Forced rank.**  `W_uv` has one single-transversal `3 x 3` minor.  Then
  for every nonconstant `γ` all nine block words vanish, so every `γ` with
  `s = m[B,γ]` true is `(b)`-eligible.  In the final models:
  - rank 2: 222 eligible `3 x 3` instances and 667 eligible `2 x 2`
    instances;
  - rank 3: 338 eligible `3 x 3` instances and 1,698 eligible `2 x 2`
    instances.

  Every one of the `3 x 3` instances has `nH_f >= 2` in **each** of F3, F1
  and F2.  The `2 x 2` ones have `min_f nH_f >= 1` (188 of them have
  exactly 1, which is consistent with `s`).  **The failing premise is
  `ZERO_f`**: the attachment rows of both deleted vertices are
  support-matchable at `γ`, and the `Θ`, `K` and `K'` minors are live.
  - What CH demands at those words is a **nonzero** determinant
    `-T_B(γ)^3 det W_uv`.  A dense pattern supplies that without any
    cancellation.
  - The cancellations that Lemma 1 really imposes sit at the six zero
    entries of `W_uv`, where `H_γ` must vanish.  Those are entry-level, and
    the model meets them with two or more live terms, exactly as (F')
    allows.
- **Where the zeros of `B` come from.**  In the forced runs `(b)` fired up
  to 349 times, so CH can force zeros of `B`:
  - rank 3: 196 times with F3 alone, 349 with all three factorizations;
  - rank 2: 0 times with F3 alone, 8 with all three.  The solver then rearranged
  the attachments until no eligible minor was certified.  The final
  six-sets keep 222–453 nonzero nonconstant words, spread over all six word
  types.  The six-vertex certificate needs zeros of each of the types
  `4+2`, `3+3`, `3+2+1`, `2+2+2` together with the six-set's own killers
  (induction note, 4.3).  The final models also fail 3–6 order-6 killer
  tasks of `B`.

## 7. Is CH hereditary in the sense of (Q2)?

Recall the schema (induction note, 5.2):

- **(Q1)** witnesses satisfy `Q_n`;
- **(Q2)** every `Q_{n+2}` pattern has an `n`-subset satisfying `Q_n`;
- **(Q3)** `Q_6` is UNSAT.

**(α) With `Q = P + CH`, (Q2) is circular.**  `Q_6` is UNSAT, so by the
induction note's 5.1, "(Q2) for `Q_8 -> Q_6`" is equivalent to "`Q_8` is
UNSAT".  Adding CH changes nothing.

**(β) The inherited part of CH excludes nothing.**  With its `not m`
premises, CH holds for every configuration at every level.  An `n`-subset
inherits every instance literally, as with H2/H3/PR.  So (Q2) holds for it,
and (Q3) fails by Proposition 4 (v).

**(γ) The seeded part of CH does not supply the zero-generating
hypothesis.**  At the deleted pair, the only seeded clause that produces a
(G)-type zero on `B` is `(b)`.  It needs two things:

- a support-certified rank `>= 2` minor of `W_uv`;
- a support-certified zero Cauchy–Binet expansion of the compressed
  Hessian.

The first fails for every column-killer pair.  When it is forced, the
second fails at every eligible word of every final model.  An exact
obstruction to a support-level proof of (Q2) for CH can be stated as
follows (this is an obstruction for these relaxations, not a theorem about
witnesses):

> In the order-8 pair relaxation `D_6` with killers, anchors, H2, H3, PR and
> CH in all three factorizations, there are models in which the deleted
> pair's block has a certified full-rank `3 x 3` minor, while at least 338
> of the 726 nonconstant words of the six-set stay nonzero.  At each of
> those words, each of the three Cauchy–Binet expansions of
> `det H_γ` has at least two supported products.

So no proof of (Q2) can use CH at a single pair through zero patterns
alone.  The rank drop `rank H_γ <= rank W_uv` is a determinantal condition
that has to be met by cancellation, or by nonvanishing, among two or more
supported products.

**Proof sketch of what does hold (value level).**  The value-level content
of Corollary 2 (a) is hereditary in an exact sense.  The next section makes
this precise.

## 8. The value-level content: a two-ancilla contraction, and the sharper statement

**Lemma 5 (two-ancilla contraction)  [EXACT].**  Let `W` be any
configuration on `V`, `{u, v}` a pair and `B = V - {u, v}`.  Let `ℓ, m` be
in `F^3` with `ℓ^T W_uv m = 0`.  Define two one-colour vertices `u'` and
`v'`:

- the block of `u'` to `z in B` is the row vector `ℓ^T W_uz`;
- the block of `v'` to `z` is `m^T W_vz`;
- there is no `u'v'` edge.

Then for every word `γ` on `B`, the matching sum of `B ∪ {u', v'}` at `γ`
equals `Σ_{x,y} ℓ_x m_y T_V(x, y, γ)`.  If `W` is a witness, this is

```text
T_{B ∪ {u',v'}}(γ) = [γ = c^n] λ_c ℓ_c m_c.                                 (3)
```

*Proof.*  Contract (1) with `ℓ` and `m`.  The `T_B` term carries
`ℓ^T W_uv m = 0`.  The rest is `(ℓ^T A_γ) Θ_γ (B_γ^T m)`, which is the sum
over perfect matchings that match `u'` and `v'` into `B`.  ∎

**Equivalence.**  For a nonzero `W_uv`, the rank-one matrices `ℓ m^T` with
`ℓ^T W_uv m = 0` span the hyperplane `W_uv^⊥`.  Change bases so that `W_uv`
becomes `I_r ⊕ 0`:

- the `e_i e_j^T` with `i != j` are in the hyperplane;
- so are the `e_i e_i^T` with `i > r`;
- and `(e_1 + e_2)(e_1 - e_2)^T` supplies `E_11 - E_22`.

Hence "(3) for all such `(ℓ, m)` and every nonconstant `γ`" is equivalent to
`H_γ ∈ span(W_uv)`, which is Corollary 2 (a).  An exact random check of the
spanning claim at ranks 1–3 passed (scratch).

**Full-weight choice.**  Work over an infinite field.  There exist `ℓ, m`
with `ℓ^T W_uv m = 0` and `ℓ_c m_c != 0` for every colour `c` **iff**
`W_uv` is not a single nonzero entry.

*Proof.*

1. If `W_uv = α E_ji`, then `ℓ_j m_i = 0`.
2. If `W_uv = a e_i^T` (one nonzero column) with `|supp a| >= 2`, choose
   `ℓ ⊥ a` with full support.  The plane `a^⊥` is not a coordinate plane.
   Then `W_uv^T ℓ = 0`, so any full-support `m` works.
3. Otherwise, for generic full-support `ℓ`, the vector `h = W_uv^T ℓ` is
   not a multiple of a unit vector.  If it were, the image of `W_uv^T`
   would lie in a coordinate line, and `W_uv` would be one nonzero column.
   So `h^⊥` is not a coordinate plane and contains a full-support `m`.  ∎

So every order-`(n+2)` witness with at least one pair whose block is not a
single nonzero entry (`W_uv = 0` allowed) yields a realization of a
`GHZ(n,3)` state up to the torus (weights `λ_c ℓ_c m_c != 0`).  That
realization has `n` three-colour vertices and two one-colour vertices with
no edge between them.  Call this class `C_{n,1}`, and `C_{n,j}` with `j`
such ancilla pairs.

The residual case is narrow: every pair of `V` is adjacent through exactly
one single-entry block.

**Heredity at the value level.**  Lemma 5 needs no property of the
coloured vertices other than (1).  So the same contraction maps a
configuration in `C_{n+2, j}` to one in `C_{n, j+1}`, outside the same
residual (the contracted pair must be two coloured vertices).  With
`Q_n = ∪_j C_{n,j}`:

- (Q1) holds (`j = 0`);
- (Q2) holds exactly at the value level, modulo the residual;
- (Q3) becomes the single base statement below.

This is the induction structure the note asked for.  It is **not** proved,
because its base case is open.

**Sharper next statement (one).**  Decide `C_{6,1}`:

> Is there a configuration on six three-colour vertices and two one-colour
> vertices `a, a'`, with `W_aa' = 0`, whose matching sum is `GHZ(6,3)` up to
> the torus?

- **If no**, then every order-8 witness is excluded, except the
  single-entry residual.
- **If yes** (even only at the support level), then pair contraction cannot
  carry the order-6 exclusion to order 8 by itself.  Any order-8 argument
  must then use more than one pair at a time.

The support model of `C_{6,1}` has the size of `D_6`: `3^6` top words, and
the ancillas carry no colour.  It differs from `D_6` in two ways:

- it keeps (L), (F') and (G) at **every** hub of the top set, including
  hubs in `B`;
- it drops the colours of `u` and `v`.

Two things must be settled before encoding it:

- Which of the encoded families hold for configurations with one-colour
  vertices.  Hub flattening at a three-colour hub (Lemma 1 of the
  multi-partner note) uses only the GHZ values, so it survives.  The column
  killer and the diagonal anchor need re-examination, because a one-colour
  partner's block is a single column.
- Whether ancilla-assisted `GHZ(6,3)` is already known to be realizable in
  the literature.  This was **not** checked here.  If it is realizable with
  two such ancillas, the route stops at (Q3).

## 9. Status and frontier

- Global status: **UNRESOLVED**.  No theorem about witnesses changes.
- Lemma 1, Corollary 2, the Cauchy–Binet expansions, Proposition 4 and
  Lemma 5 are proved here by short hand proofs, with exact integer replays
  (scratch).  There is no independent audit and no Lean formalization.
  CH's soundness rests on Lemma 1 and the single-product certificate rule.
- The runs are experiments.  The SAT answers are re-checked models of
  relaxations: they exclude nothing and realize nothing.  The order-6
  UNSAT answers are uncertified, they repeat the reference result, and
  they are not load-bearing.
- **Frontier.**  No node, theorem or live reduction edge changes.  The
  integrator should extend the refuted-route row that the induction note
  proposed ("support-level exclusion at order `n` to `n + 2` by restriction
  to an `n`-subset") by one clause:

  > the compressed-Hessian family CH (two-step and one-step Cauchy–Binet
  > certificates) does not transfer the needed (G) zeros: `D_6` + CH is SAT,
  > also with the deleted pair's block forced to certified full rank.

  The integrator may record Lemma 5 and the `C_{6,1}` question as a
  **candidate** (not live) reduction note on the `SL6 -> GL` edge.  It is
  an exact implication from order-8 witnesses to a different class, whose
  emptiness is open.  It becomes a live edge only if `C_{6,1}` is shown
  empty and the single-entry residual is handled.

## 10. Commands and runs

```text
python claims/finite/n08/explore_general_block_recursive_support_model.py 6 --killers --holonomy --plane-rigidity --fast --cross-check-fast --compressed-hessian
python claims/finite/n08/explore_general_block_recursive_support_model.py 6 --compressed-hessian --fast
python claims/finite/n08/explore_general_block_recursive_support_model.py 6 --g-minus --no-symmetry --killers --anchors --holonomy --plane-rigidity --compressed-hessian [--ch-factorizations F3,F1,F2]
python claims/finite/n08/explore_general_block_recursive_support_model.py 4 --g-minus --no-symmetry --killers --anchors --holonomy --compressed-hessian
python -m unittest -q tests.test_general_block_support_model_fast
```

Bounded run ids, all under `tools/research/run_bounded.py`:

- **Exact replays (scratch):**
  - `chs-identity-1`: identity (1) and the F3 expansion, exact, `n = 4, 6`;
  - `chs-sound-1`: CH on 20 exact zero patterns;
  - `chs-ancilla-3`, `chs-ancilla-4`: Lemma 5 on six configurations, and
    the spanning claim.
- **Default-encoding comparison:** `chs-cmp-head`.
- **Order 6:** `chs-a1-full6` (245 s), `chs-a1-full6-allf`,
  `chs-a2-chonly6`, `chs-a3-kill6`, `chs-a4-kill6-all`, `chs-a3-kill6-allf`.
- **`D_6`:** `chs-b-g6` (140 s); the scratch decoders `chs-b-g6-dec{0,2,3}`,
  `chs-b-g6-pkl{0,2,3}` and `chs-b-g6-all{0,2,3}`; the factorization and
  census replays `chs-fact-*` and `chs-census-all_b{2,3}`.
- **`D_4`:** `chs-c-g4`, `chs-c-g4-wrank{2,3}`, `chs-c-g4-dec{0,2,3}`,
  `chs-c-g4-pkl{0,2,3}`, `chs-c-g4-all{0,2,3}`.

The scratch drivers (rank hypothesis, model capture, factorization census,
exact replays) are in the session scratchpad and are not committed.  No
process was left running.
