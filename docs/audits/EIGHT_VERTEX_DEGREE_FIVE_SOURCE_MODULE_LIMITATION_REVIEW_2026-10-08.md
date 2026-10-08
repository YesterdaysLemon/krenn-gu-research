# Review: original 134-support degree-five source-module limitation

Date: 2026-10-08

Review status: **PASS as a negative (limitation) record; no mathematical gap
found**.  This is a same-day agent review by an adversarial reviewer working in
the same repository on the same day; it is not separate-human refereeing and
not a Lean formalization.  The global Krenn--Gu status remains **UNRESOLVED**.

Reviewed document:
[`EIGHT_VERTEX_DEGREE_FIVE_SOURCE_MODULE_LIMITATION.md`](../../claims/finite/n08/EIGHT_VERTEX_DEGREE_FIVE_SOURCE_MODULE_LIMITATION.md)
(ledger `document_sha256_16` `f0dea31f51b64ffe`, matches the LF-normalized
file).  Ledger status `verified_finite`; verifier provenance
`script_is_the_verifier`; audit provenance `independent_exact_identity_audit`.

## Nature of the document

This is not a theorem about the conjecture and not an exclusion.  It is an
exact finite non-existence statement about a bounded certificate space, and
the document says so ("exact finite bounded-space limitation, not consistency
of the full target ideal") and points to the degree-six two-edge identity
([P17 document](../../claims/finite/n08/EIGHT_VERTEX_TWO_EDGE_SURPLUS_SHORE_EXCLUSION.md))
that excludes the very same support using multipliers outside the space.  The
ledger status `verified_finite` ("an exact finite claim accepted through the
recorded exhaustive computation ... says nothing beyond that finite scope")
fits, provided it is read as "no monomial in this bounded space", never as
"this support is consistent" or "this support survives".  The ledger
assumptions text states exactly that, so the status does not overstate.

## Exact claim as restated

Fix the 134 live entries of
`tests/fixtures/recursive_physical_support_n8_four_cut_survivor_134.json`
(sha256 `75cef4c3...f9941fe`); all other entries are set to zero.  Let
`R=Q[g_s : s live]`, `P_a=T_W(a)-delta_a` for the 6,561 words `a`, and
`rho=g88*g91-g82*g97`.  Then

```text
L = span_Q{ P_a, g_s*P_a : a a word, s live } + { q*rho : q in R, deg q <= 3 }
```

contains no nonzero monomial.  Degrees count physical entries, so the layers
have degrees {0,4} (rows `P_a`) and {1,5} (rows `g_s P_a`); `q*rho` reaches
degree five.  The pure rows keep their `-1` constants (with 5, 8, 10 matching
monomials, which I confirmed in the result fixture), and all 402 =3x134 pure
linear tails are kept.  Not claimed: anything about higher-degree or Laurent
multipliers, localization, the full ideal, other supports, or other fields
beyond the stated rational-scalar extension remark (correct: a rational
matrix has a unit vector in its row space over `Q` iff over any extension).

## Argument check

* Reduction modulo `rho`.  A single binomial with monic leading term is a
  Groebner basis of its principal ideal; the normal form is homogeneous of
  degree 2 and degree-preserving, sends monomials to monomials, and its kernel
  in degree <=5 is exactly `{q*rho : deg q <= 3}`.  So a monomial lies in `L`
  iff its normal form lies in the normal-form row span of the generators.
  Either orientation of the rule is valid; the audit uses the reverse one.
  Correct.
* Unit vector in a row space.  `e_m` is in a row space iff the RREF has a
  singleton row, equivalently iff column `m` is a coloop of the column matroid
  (deleting it lowers rank).  Both are standard and correct, and are what the
  primary and the audit respectively test.
* Layer separation.  The two layers occupy disjoint degree classes, so a
  monomial in `L` would lie in one layer.  Correct.
* Block decomposition.  Primary: endpoint-colour multigrade; every row
  `g_s P_a` is multigrade-homogeneous (up to the pure constant tails, which
  join the three pure blocks of the same multiplier).  Audit: grouping by the
  physical pair of the multiplier, valid because a matching plus one edge has
  exactly two vertices of degree two, which determine the extra edge's pair,
  followed by genuine row/column connected components.  Both decompositions
  are sound; they are different, which strengthens the independence.
* Layer 0 (constant multipliers).  The audit asserts that every quartic
  matching monomial belongs to a single word (no sharing) and that every word
  has at least three live terms; so every row has at least three private
  columns and no combination of rows can be a unit vector.  This argument is
  correct but appears only as an audit comment, not in the document.

## Commands run (under `run_bounded.py`, 900 s / 8 GiB; nothing skipped)

```text
python tools/explore/probe_physical_degree5_module_134.py tests/fixtures/recursive_physical_support_n8_four_cut_survivor_134.json --expected tests/fixtures/eight_vertex_degree5_module_134.json   # PASS, 46 s
python claims/finite/n08/audit_eight_vertex_degree5_module_134.py              # PASS, 19 s
```

Primary: ranks 6,561 and 877,851, 879,174 product rows with unique labels,
3,294 rho-changed terms, `singleton_rref_rows=0`, result equal to the frozen
fixture.  Audit: `constant_multiplier_rank=6561`,
`linear_multiplier_rank=877851`, 402 pure tails, 3,294 reverse-rho
reductions, 104,999 singleton columns tested, `coloop_count=0`.  The two
implementations agree on both ranks and on the absence of a monomial.  The
rank-additivity of the audit's blocks was exercised through its built-in
positive and negative coloop controls.

## Frontier consistency

The `P17` row of `docs/current-frontier.md` says "the full declared
degree-five module on the original support has no monomial certificate".  That
is faithful and correctly scoped (declared space, original support).

## Remarks and minor gaps (none blocks acceptance)

1. Terminology.  The document says the multiplied layer "occupies 463,376
   connected components".  That number (the fixture field
   `connected_components_after_pure_lower_columns`) counts multigrade blocks
   after the pure joins, not row/column connected components; the audit's
   finer true components number 602,615 over its edge blocks.  The rank and
   absence statements are unaffected, but the word "connected components"
   should be read as "multigrade blocks".
2. Timings.  The document says about 27 s and 10 s; here 46 s and 19 s on a
   different machine.  Immaterial, same order, far below any bound.
3. The primary probe lives in `tools/explore/`, an exploratory directory, yet
   serves as the ledger's primary verifier; there is no unit test or CI hook
   for either script, only the `--expected` fixture comparison for the primary.
   The audit does not itself pin the support-file hash (it prints it); both
   read the same bytes (`75cef4c3...`).
4. `rho` is used only to enlarge the space.  Because the claim is a
   non-membership statement, the correctness of `rho` as a consequence of the
   target is not needed here (and is not asserted by the document); enlarging
   `L` only strengthens the limitation.
5. The 134-entry support is itself now excluded by the degree-six identity, so
   this record is diagnostic and historical: it measures what the declared
   low-degree module could not do, and is not a premise of any live proof.

## Verdict

An accurate, correctly scoped limitation record: exact over `Q` (hence over
`C`), two genuinely different implementations agree, and neither the ledger
status nor the frontier row reads it as more than "no monomial certificate in
the declared degree-five space".  Same-day agent review only; global status
unchanged.
