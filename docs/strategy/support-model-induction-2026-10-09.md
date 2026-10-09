# Does the recursive support model induct from order n to n + 2? — 2026-10-09

This is a dated research record.  The global Krenn–Gu status is
**UNRESOLVED**, and nothing here changes it.  No theorem about witnesses is
added, withdrawn or re-scoped.  Section 7 says what the frontier needs.

Evidence labels:

- **[EXACT]**: a hand proof, or a statement read off the encoding of
  [`explore_general_block_recursive_support_model.py`](../../claims/finite/n08/explore_general_block_recursive_support_model.py)
  by inspection.  No verifier is attached; the proofs are a few lines each.
- **[SAT-RUN]**: a bounded solver run (CaDiCaL 1.5.3 via python-sat).  Every
  SAT model passed the script's independent brute-force checker.  No UNSAT
  answer here carries a DRAT proof; none is load-bearing.
- **[OBSERVATION]**: a reading of one solver model or a comparison, not a
  theorem.

## 0. Answer

**No inductive mechanism exists inside the model as it stands, and the
reason is exact.**  The clause families that a level-`n` sub-configuration
inherits literally — Laplace accessibility (L), singleton noncancellation
(F'), the holonomy rules H2/H3 and plane rigidity PR — hold for the zero
pattern of *every* configuration, including the all-zero and the
full-support ones, so they exclude nothing at any order.  Every support-level
exclusion therefore consumes the top-level GHZ pattern (G) and its
witness-level consequences (column killers, diagonal anchors).  At order
`n + 2` an `n`-vertex sub-configuration `B = V - {u, v}` receives (G) only
through one matrix identity (Proposition 3):

```text
T_B(γ) W_uv + A_γ Θ_γ B_γ^T = [γ = c^n] λ_c E_cc       for every word γ on B,
```

where `A_γ`, `B_γ` are the `3 x n` attachment columns of the deleted pair at
the colours of `γ` and `Θ_γ = (T_{B-{z,z'}}(γ))` is the order-`(n-2)`
"Hessian" of `B`.  So a nonconstant `T_B(γ)` vanishes exactly when the
compressed Hessian `A_γ Θ_γ B_γ^T` does, and nothing in (G) makes that
vanish.  The six-vertex certificate needs, on one and the
same six-set, zeros from each of four of the six nonconstant word types
(`4+2`, `3+3`, `3+2+1`, `2+2+2`: omitting any one type gives SAT; omitting
`5+1` or `4+1+1` alone stays UNSAT) **and** the
column killers inside the six-set (Section 4.3).  The pair-decorated
relaxation of order 8 (the order-6 model with (G) replaced by what the
deleted pair forces, `--g-minus`) is **SAT**, and in its model the six-set
has 717 of its 726 nonconstant words nonzero and five failing killer tasks
(Section 4.2).

**Most load-bearing fact.**  Because the order-6 model is UNSAT, the
statement "every order-8 model contains an order-6 model on some six-set" is
*equivalent* to the order-8 exclusion (Section 5.1).  Restriction to a
sub-model of the same kind therefore cannot carry a finite exclusion upward
without proving the larger exclusion first; an all-`n` argument must find a
strictly weaker hypothesis class that is (i) implied by witnesses, (ii)
reproduced on some `n`-subset of every order-`(n+2)` model of the class, and
(iii) already unsatisfiable at order 6.  The non-hereditary ingredient that
any such class must replace is named exactly in Section 5.3: the top-level
(G) zeros on the balanced and rainbow word types together with the killers
of the same set.

## 1. Question and inputs

The question (from the coordinator): does the general-block recursive
support model have a hereditary structure that turns a support-level
exclusion at order `n` into one at order `n + 2`?  Inputs, all on
`origin/main` at `2dbc3374`:

- `docs/current-frontier.md`, nodes `SL6`, `BR1`, `GL` and their rows;
- the model script and its docstring (variables `g`, `m`, `t`; rules (L),
  (F'), (G); families killers, anchors, H2/H3, PR);
- [`hyperdeterminant-crossing-2026-10-09.md`](hyperdeterminant-crossing-2026-10-09.md)
  (PR, its soundness at every level, the checked `n = 6` certificate, and
  `OCC-PR`);
- [`multi-partner-grid-transport-2026-10-09.md`](multi-partner-grid-transport-2026-10-09.md)
  (hub flattening `R_A Φ_c = 0`);
- [`s156-hub-trichotomy-2026-10-09.md`](s156-hub-trichotomy-2026-10-09.md)
  (anchors);
- [`trunk-level-attempt-2026-10-08.md`](trunk-level-attempt-2026-10-08.md)
  and [`ecology-run-2026-10-08.md`](ecology-run-2026-10-08.md) (first-order
  mechanisms; not re-derived here).

Conventions are the script's: `W_ij[a, b]` with `a` the colour at `i`;
`T_A(w)` the matching sum of `W` restricted to an even set `A`
(`T_∅ = 1`); a witness on `V` has `T_V = GHZ` up to the diagonal torus.
Throughout, `|V| = n + 2`, `{u, v}` is a pair and `B = V - {u, v}`.

## 2. What a level-`n` sub-configuration inherits  [EXACT]

### 2.1 The families and their scope

| family | proved for | where instantiated | inherited by `B` |
|---|---|---|---|
| (L), (F') | every configuration | every even `A`, every hub | **yes**, literally, at every `A ⊆ B` |
| H2, H3 | every configuration | every even `A` | **yes**, every instance with `A ⊆ B` |
| PR | every configuration | every `A`, `\|A\| >= 6` | **yes**, every instance with `A ⊆ B` |
| (G) | witnesses | `A = V` only | **no** |
| column killers | witnesses | each `(x, c)`, partner anywhere in `V` | **no**; only the weak form (K⁻) below |
| diagonal anchors | witnesses | each `(x, c)`, partner anywhere in `V` | **no**; weak form (A⁻) as for killers |
| hub clause `M`, grid clause `G(r,s)` as stated | witnesses (top-level words) | `A = V` | **no** (`G(r,s)` with `not m` premises in place of "nonconstant" is valid at every level and would be inherited; it is not encoded) |
| chain normalization, lex-leader | symmetry of the order-`n` model | — | not applicable |

**(K⁻).**  At order `n + 2` each `x` has, for each colour `c`, a partner
whose block is supported on the single column `c`; the three partners are
distinct (one block cannot be column-`c`-only for two `c`).  At most two of
them are `u, v`, so every `x in B` keeps a killer partner inside `B` for at
least one colour, and for at least two colours unless `u` and `v` are both
killer partners of `x`.  That is all that survives: the order-`n` killer
clause needs all three colours inside `B`.

### 2.2 Proposition 1 (the inherited families exclude nothing)

The zero pattern of any configuration satisfies (L), (F'), H2, H3 and PR at
every level, by their soundness proofs (each is proved for every complex
configuration, no GHZ input).  In particular two trivial patterns satisfy
all of them at every order:

- the **zero** pattern (all `g`, `m` false): no term is live, so (L) is
  vacuous and (F') holds; every H2/H3/PR premise asks for a live term or a
  certified nonzero minor;
- the **full** pattern (all `g`, `m` true): (F') and every H2/H3/PR premise
  ask for some `m = false`.

So the hereditary part of the model is satisfiable at every order, and every
support-level exclusion uses (G), the killers, the anchors or `M` — all of
them statements about the top set `V`.  This sharpens the trunk record's
remark that single-term consequences cannot exclude order 6: here even the
multilinear families cannot, without a top-level seed.

### 2.3 Proposition 2 (where `m[B, ·]` occurs at order `n + 2`)

In the order-`(n+2)` encoding, with every family switched on at every level,
the variables `m[B, γ]` (`B = V - {u, v}`) occur only in:

1. the clauses of level `B` itself ((L), (F') of `B` at its hubs; H2, H3, PR
   instances with `A = B`); and
2. the two term definitions `t[V, w, u, v] <-> g[uv, w_u, w_v] & m[B, γ]`
   and `t[V, w, v, u]` (the same conjunction), `w = (w_u, w_v, γ)`.

*Proof by inspection.*  A Laplace clause of a set `A` mentions `m` only at
`A - {p, q}`, so `m[B, ·]` appears as a remainder only for `A = V`, through
the term of the partner pair `{u, v}`.  A top-level H2 premise mentions
`m[V, w]` and `t` literals; its inner sets `V - {p, a}` are reached only
through a live `t[V, w, p, a]`, which for `{p, a} = {u, v}` is the same
conjunction.  H3 closure clauses mention `m[V, w]` and `t[V, w, p, ·]`.  A
top-level PR clause mentions `m[V, ·]` and `m` at sizes `n - 2` and `n - 4`
(the `T_{R-u}` and `T_{R-S}` of its `T`-expansion).  Killers and anchors are
`g`-only.  (With symmetry breaking on, the chain unit `m[V - {0,1}, 0^n]` is
an extra occurrence; it is justified by relabelling, not by a rule.)  ∎

So if `u` and `v` are not adjacent in the support (`W_uv = 0`), the top-level
coefficients of `B` are constrained by nothing outside `B`.

### 2.4 Proposition 3 (the value-level (G⁻): pair expansion)

For a word `γ` on `B` put, as `3 x n` matrices with columns indexed by
`z in B`,

```text
A_γ[x, z] = W_uz[x, γ_z],      B_γ[y, z] = W_vz[y, γ_z],
Θ_γ[z, z'] = T_{B-{z,z'}}(γ|)   (z != z'),   Θ_γ[z, z] = 0.
```

Then for **every** configuration and every `γ`,

```text
( T_V(x, y, γ) )_{x, y} = T_B(γ) W_uv + A_γ Θ_γ B_γ^T,                    (1)
```

and at a witness the left side is `0` for nonconstant `γ` and `λ_c E_cc`
for `γ = c^n`, `λ_c != 0`.

*Proof.*  A perfect matching of `V` either contains the edge `uv` (weight
`W_uv[x, y]` times a perfect matching of `B`), or matches `u` to some `z` and
`v` to some `z' != z` in `B` (weight `W_uz[x, γ_z] W_vz'[y, γ_z']` times a
perfect matching of `B - {z, z'}`).  Each matching is counted once.  ∎

(1) is the two-open identity of the trunk record written in matrix form.
Its consequences for `B`:

- **(a) Non-adjacent pair.**  If `W_uv = 0`, then (1) says
  `A_γ Θ_γ B_γ^T = 0` for nonconstant `γ`, and `T_B` does not occur.
- **(b) Hessian proportionality.**  For nonconstant `γ`,
  `A_γ Θ_γ B_γ^T = -T_B(γ) W_uv`.  The compressed Hessian is a multiple of
  one fixed matrix, the same for every `γ`; and `T_B(γ) = 0` if and only if
  `A_γ Θ_γ B_γ^T = 0`.  This is the exact (G⁻): a nonconstant coefficient of
  `B` vanishes exactly when the deleted pair's compressed Hessian at `γ`
  does.
- **(c) Box transfer (the hub-flattening form).**  If the columns of
  `W_uv` do not all lie in the column space of `A_γ` — in particular if
  `rank A_γ <= 2` and some column of `W_uv` sticks out — take `ℓ` with
  `ℓ^T A_γ = 0`, `ℓ^T W_uv != 0`; multiplying (1) by `ℓ^T` gives
  `T_B(γ) = 0` for nonconstant `γ`.  This is Lemma 1 of the multi-partner
  note at hub `u` with the coordinate of partner `v`, and it is the
  mechanism of the box statements (a), (b) of the S156 hub trichotomy.  If
  `A_γ` (and symmetrically `B_γ`) has rank 3, hub flattening gives no
  zero/nonzero information about `T_B(γ)`.

### 2.5 Support form of (G⁻)

What the zero pattern can certify from (1) is (L)/(F') applied to the
two-step sum `W_uv[x,y] T_B(γ) + Σ_{z != z'} W_uz W_vz' T_{B-zz'}`:

- `not m[B, γ]` is forced iff for some `(x, y)` with `(x, y, γ)` nonconstant,
  `W_uv[x, y] != 0` and the `(x, y)` entry of `A_γ Θ_γ B_γ^T` has no live
  term; the commonest instance is a **dead row**: row `x` of `u` is zero on
  every column `γ_z`, `z in B` (then (c) applies with `ℓ = e_x`);
- `m[B, γ]` is forced iff the entry has exactly one live term.

By Proposition 2, every other support-level consequence for `m[B, γ]` must
also pass through the literal `g[uv, x, y] & m[B, γ]`: for instance a
top-level H3 cancellation at the hub `u` can force it.  The two items above
are exactly what the (L)/(F') clauses of the order-`(n+2)` model at the hubs
`u` and `v` give (the two-step form is implied by the one-step clauses at
`u` and the Laplace clauses of `V - {u, z}` at `v`); `D_n` below encodes
those and omits the top-level holonomy and PR.

## 3. The pair-decorated model `D_n` (`--g-minus`)

To test (G⁻) by computation, the script gained a flag `--g-minus` (class
`PairDecoratedGSM`; default behaviour unchanged, Section 6).  `D_n` is the
order-`n` model on `B = {0, ..., n-1}` with (G) replaced by the deleted pair
`u = n`, `v = n + 1`:

- every even `A ⊆ B`, `|A| >= 4`: `m[A, w]` with (L), (F') at every hub;
  H2, H3 and PR lazily at these levels;
- `g` on every pair of `V`, including the attachments `W_uz`, `W_vz`,
  `W_uv`;
- `m` on the `2n` sets `V - {u, z}`, `V - {v, z}` with (L), (F') at the hub
  `v`, respectively `u`, only;
- `m` on `V` with (L), (F') at the hubs `u` and `v` only, and (G) on `V`;
- with `--killers` / `--anchors`, the **order-`(n+2)`** statements (partners
  anywhere in `V`).

Every clause of `D_n` is a clause of the order-`(n+2)` model, so `D_n` is a
sound relaxation of it: UNSAT of `D_n` would exclude order `n + 2` at the
support level, SAT says only that this relaxation does not.  What `D_n`
drops: the top-level clauses at hubs inside `B`, the other hubs of the
decoration sets, the sets containing both `u` and `v` other than `V`, H2/H3/PR
on sets meeting `{u, v}`, and the order-`n` (G), killers and anchors of `B`.
There is no symmetry breaking (`--no-symmetry` is required).  A SAT model is
re-checked by `check_model_gminus` ((L), (F') at the declared hubs, (G) on
`V`, the order-`(n+2)` killers), `check_anchors` on `V`, and the unchanged
`check_holonomy` / `check_plane` on the levels inside `B`.

## 4. Experiments  [SAT-RUN]

All runs went through `tools/research/run_bounded.py`; run ids in Section 8.

### 4.1 `D_4`: a four-set inside six vertices

`4 --g-minus --no-symmetry --killers --anchors --holonomy` is **SAT** in
0.1 s, one round, 49 entries, independent check PASS (PR is empty below six
vertices).  The six-vertex model with killers, H2/H3 and PR is UNSAT
(checked DRAT), so the six-vertex exclusion is **not pair-local**: it needs
the top-level clauses at hubs inside the four-set and the top-level families.
This agrees with the recorded fact that every one of the 576 PR clauses of
the six-vertex run is at level 6, the top level (hyperdeterminant note,
Section 3.4, `deg3` row).

### 4.2 `D_6`: a six-set inside eight vertices

`6 --g-minus --no-symmetry --killers --anchors --holonomy --plane-rigidity`
is **SAT**: 105 s, 38 CEGAR rounds, 239,129 lazy instances (10,247 H2;
228,807 H3 edge/closure/square; 75 PR, all at level 6), 122 entries,
independent check PASS.  A scratch re-run of the same loop (identical round
count) decoded the model [OBSERVATION; one model, not forced]:

| quantity | value |
|---|---|
| `W_uv` | column-1-only (a killer block): entries `01 11 21` |
| entries inside `B` | 71 |
| constant words of `B` nonzero | all three |
| nonconstant words of `B` nonzero | **717 of 726** |
| ... by type `5+1, 4+2, 4+1+1, 3+3, 3+2+1, 2+2+2` | 35/36, 89/90, 89/90, 60/60, 356/360, 88/90 |
| order-6 killer tasks of `B` failing | 5 of 18: `(0,0) (1,1) (2,0) (2,2) (5,2)` |
| order-6 anchor tasks of `B` failing | 4 of 18 |

So the six-set of this model has only nine nonconstant zeros, while the
six-vertex certificate needs zeros from each of four word types
(Section 4.3).  With `W_uv` rank one, (1)(b) forces
every compressed Hessian `A_γ Θ_γ B_γ^T` onto the fixed rank-one matrix
`W_uv`, a multi-word rank condition that the support model encodes only
entrywise.

A companion test added the order-6 (G) of `B` itself as extra unit clauses
to `D_6` (not implied by anything; it asks whether the deleted pair can
coexist with a GHZ-patterned six-set when the six-set's own killers are not
imposed).  It was **inconclusive** at its 1,200 s bound (run
`sind-g6-bghz`, scratch driver).  No conclusion is drawn from it.

### 4.3 What the six-vertex certificate consumes

Order 6, killers + H2/H3 + PR, repaired symmetry, `--fast`, with the (G)
zero clauses of one nonconstant word type omitted (`--g-drop-types`; every
union of types is invariant under vertex and colour permutations, so the
symmetry block stays sound):

| omitted type (words) | result | time, rounds | model |
|---|---|---|---|
| none (reference, hyperdeterminant note) | UNSAT | 145 s, 77 | — |
| `5+1` (36) | UNSAT (uncertified) | 825 s, 99 | 697 PR, all at level 6 |
| `4+2` (90) | **SAT** | 73 s, 17 | 16 entries |
| `4+1+1` (90) | UNSAT (uncertified) | 285 s, 80 | 596 PR, all at level 6 |
| `3+3` (60) | **SAT** | 27 s, 16 | 14 entries |
| `3+2+1` (360) | **SAT** | 15 s, 13 | 48 entries |
| `2+2+2` (90) | **SAT** | 0.5 s, 1 | 14 entries |
| (G) in full, **killers omitted** | **SAT** | 0.2 s, 1 | 135 entries (every block full) |

Every SAT model passed the independent checker with the omitted type exempt.
So, given the other hypotheses, the certificate needs the GHZ zeros of each
of the types `4+2`, `3+3`, `3+2+1`, `2+2+2` **and** the column killers;
the zeros of type `5+1` and of type `4+1+1` are each not needed on their own.  These are
statements about one relaxation each, not a minimal core: a type that is
not needed alone may be needed jointly with another.
Without killers the full-support pattern is a model in one round: then every
coefficient has at least two live terms and no rule's premise can hold.

## 5. Conclusion: the non-hereditary ingredient

### 5.1 Restriction is circular  [EXACT, elementary]

Let `P_n` be the order-`n` support model with a fixed rule set containing
(G) and the killers.  If `P_n` is UNSAT, then the re-seating statement
"every `P_{n+2}`-model restricts, on some `n`-subset, to a `P_n`-model" is
equivalent to "`P_{n+2}` is UNSAT": its conclusion asserts a `P_n`-model,
which does not exist.  The same holds at the value level ("every witness of
order `n + 2` contains a witness of order `n`").  This is the induction
analogue of `OCC-PR(n)` being as strong as the exclusion.

### 5.2 Lemma schema for an induction

An all-order exclusion by induction on `n` through this model needs
hypothesis classes `Q_n` on order-`n` zero patterns with

- **(Q1) soundness:** the zero pattern of every order-`n` witness satisfies
  `Q_n`;
- **(Q2) heredity:** for every pattern satisfying `Q_{n+2}` (not only
  witness patterns) some `n`-subset `B` carries a pattern satisfying `Q_n`;
- **(Q3) base:** `Q_6` is UNSAT.

Then no pattern satisfies any `Q_n`, `n >= 6`, so no witness exists.  The
two classes in hand each fail one condition:

- `Q = P` (the full model): (Q1) and (Q3) hold; (Q2) is the circular
  statement of 5.1;
- `Q = 𝓗` (the inherited families): (Q1) and (Q2) hold (Section 2.1);
  (Q3) fails (Proposition 1).

A working `Q` must contain a **zero-generating** hypothesis at every level —
a condition that the full-support pattern violates — that is reproduced on a
subset by (1).  By Section 2.5 the only zero-generating input (1) supplies at
the support level is the dead-row / dead-Hessian-entry transfer, so (Q2)
would have to say: every `Q_{n+2}`-pattern has a pair `{u, v}` whose
compressed Hessian entries are support-dead on enough words, and whose
killer partners avoid `{u, v}`, for `B` to satisfy `Q_n`.

### 5.3 The exact gap (sharpest statement)

The ingredient that blocks induction is **(G) at the top set restricted to
the nonconstant word types `4+2`, `3+3`, `3+2+1`, `2+2+2` (each needed on
its own; `5+1` and `4+1+1` each dispensable on its own), together with the
column killers of the same set**.
At order `n + 2` a level-`n` set `B = V - {u, v}` gets:

- the killers only in the weak form (K⁻);
- the (G) zero at `γ` only when `A_γ Θ_γ B_γ^T = 0` (Proposition 3 (b)),
  certified at the support level only when the `(x, y)` entry is dead for
  some nonzero `W_uv[x, y]` (Section 2.5);
- nothing at all when `W_uv = 0` (Proposition 2).

The pair-decorated relaxation `D_6` shows that the clauses at the deleted
pair do not force any of this (Section 4.2: 717 of 726 nonconstant words
nonzero).  Whether the full order-8 rule set, with its top-level clauses at
hubs inside `B`, forces some six-set to receive the needed zeros is exactly
the order-8 question the 24-hour runs address; by 5.1 it cannot be answered
by restriction alone.

### 5.4 One load-bearing next lemma

Proposition 3 (b) is a **multi-word rank condition** the model does not
encode: for every nonconstant `γ`, the `3 x 3` matrix `A_γ Θ_γ B_γ^T` is a
scalar multiple of the fixed matrix `W_uv`.  When `W_uv` is a killer block
(rank one, as in the `D_6` model), every compressed Hessian has rank at most
one with fixed column and row spaces — `9 * 3^n` entries tied to one
direction.  A support-certifiable form (single-transversal `2 x 2` minors of
`A_γ Θ_γ B_γ^T`, in the style of the grid clause `G(r, s)`) is the natural
clause family to try next; it is a top-level family at the deleted pair, so
it supplies a candidate zero-generating hypothesis for (Q2) rather than a
new local exclusion.  Whether it is hereditary in the sense of (Q2) is open.

## 6. The script change

`claims/finite/n08/explore_general_block_recursive_support_model.py`:

- `--g-minus` builds `PairDecoratedGSM` (Section 3); it requires
  `--no-symmetry` and refuses the `--fast` and pattern options;
- `--g-drop-types T1,T2,...` omits the (G) zero clauses of the listed
  nonconstant word types (`word_type`: colour-class sizes, e.g. `4+2`); the
  final `check_model` exempts the same types;
- `_laplace` takes an optional hub list, and `_ghz` iterates over `len(V)`.

With neither flag the encoding is unchanged: the base CNF of `GSM(n)` and
`GSM(n, killers=True)` plus anchors, for `n = 4, 6`, has the same clause list
(SHA-256 of the clause list) and the same variable count as at `2dbc3374`
(scratch comparison).  The lazy families and checkers are untouched.

## 7. Status and frontier

- Global status: **UNRESOLVED**.  No theorem about witnesses changes.
- Propositions 1–3 and 5.1 are proved here (short hand proofs; no
  independent audit, no Lean).  Proposition 3 is a matrix form of the
  existing two-open identity; (c) is a special case of hub flattening.
- The runs are experiments.  The SAT answers are re-checked models of
  relaxations; they exclude nothing and realize nothing.
- **Frontier:** the integrator should add one refuted-route row — "turning
  the support-level exclusion at order `n` into order `n + 2` by restriction
  to an `n`-subset": circular by 5.1, the inherited families exclude nothing
  (Proposition 1), and the pair relaxation `D_6` is SAT — and may extend the
  `SL6 -> GL` edge label with the named gap of 5.3.  No node, theorem or
  reduction edge is added.

## 8. Commands and runs

```text
python claims/finite/n08/explore_general_block_recursive_support_model.py 4 --g-minus --no-symmetry --killers --anchors --holonomy
python claims/finite/n08/explore_general_block_recursive_support_model.py 6 --g-minus --no-symmetry --killers --anchors --holonomy --plane-rigidity
python claims/finite/n08/explore_general_block_recursive_support_model.py 6 --killers --holonomy --plane-rigidity --fast --g-drop-types 4+2
python claims/finite/n08/explore_general_block_recursive_support_model.py 6 --holonomy --plane-rigidity --fast
```

Bounded run ids (all under `tools/research/run_bounded.py`):

- `sind-g4-kah` (0.1 s), `sind-g6-kahp` (105 s);
- `sind-g6-dump` (108 s; scratch decoder of the `D_6` model, not committed);
- `sind-drop-5-1`, `sind-drop-4-2`, `sind-drop-4-1-1`, `sind-drop-3-3`,
  `sind-drop-3-2-1`, `sind-drop-2-2-2` (bound 900 s each);
- `sind-nokill-6` (0.2 s);
- `sind-g6-bghz` (timed out at 1,200 s; scratch driver, inconclusive).

The `5+1` run was UNSAT in 825 s and the `4+1+1` run in 285 s; both are
uncertified and neither is load-bearing.  Total solver time about 45 minutes.

No process was left running.
