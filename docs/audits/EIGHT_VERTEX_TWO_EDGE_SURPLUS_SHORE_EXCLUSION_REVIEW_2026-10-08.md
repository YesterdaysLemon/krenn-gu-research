# Review: eight-vertex two-edge surplus-shore exclusion (P17)

Date: 2026-10-08

Review status: **PASS (no mathematical gap found)**.  This is a same-day
agent review, produced by an adversarial reviewer working in the same
repository on the same day as the reviewed material.  It is not separate-human
refereeing, and it is not a Lean formalization.  The global Krenn--Gu status
remains **UNRESOLVED**.

Reviewed document:
[`EIGHT_VERTEX_TWO_EDGE_SURPLUS_SHORE_EXCLUSION.md`](../../claims/finite/n08/EIGHT_VERTEX_TWO_EDGE_SURPLUS_SHORE_EXCLUSION.md)
(ledger `document_sha256_16` `8a1a641ce3602105`, which matches the
LF-normalized file).  Ledger status `verified`; verifier provenance
`script_is_the_verifier`; audit provenance `independent_exact_identity_audit`.

## Exact claim as restated

Scope: `n=8`, every field (the identity is over Z), normalized ternary GHZ
matching tensor.  Physical entries are numbered one-based lexicographically:
pair index times nine, plus `3a+b+1`.  Put

```text
a=g172=W35[0,0], b=g174=W35[0,2], c=g244=W67[0,0], d=g245=W67[0,1].
```

Impose exactly the fifteen zeros `163,181,190,191,199,201,208,217,218,226,
232,235,236,241,242` (equivalently the fifteen named `W..[..]=0` conditions
inside the shore `S={3,4,5,6,7}` other than the edges 35 and 67 at the
relevant colours).  Require only `b*d != 0`; the base entries `a`, `c` and all
other entries are arbitrary.  Then, with `T_ij` the full matching coefficient
of the word that is 0 except vertex 5 coloured `i in {0,2}` and vertex 7
coloured `j in {0,1}`, and `P_00=T_00-1`, `P_ij=T_ij` otherwise,

```text
b*d = -a*c*P_21 + a*d*P_20 + b*c*P_01 - b*d*P_00.
```

At a GHZ witness every `P` vanishes, so `b*d=0`: contradiction.  Excluded:
every normalized-GHZ source with these fifteen zeros and `b*d != 0` (and, for
a diagonal target with base amplitude `lambda_0`, the same with `lambda_0*b*d`).
Not excluded: the unrestricted eight-vertex parent, any source violating the
guard, or anything at order other than eight.  Four isomorphism types
(disjoint or shared-centre covering edges, times equal or distinct alternate
colours) are claimed; each has its own fifteen zeros and two nonzeros.

## Argument check

* Shore principle.  With the guard, inside `S` for the four words only the two
  covering edges have nonzero entries (the document's grouped zeros are exactly
  the fifteen ids; I decoded all of them by hand).  Three vertices lie outside
  `S`, so every perfect matching uses an internal edge of `S`, hence one of the
  two covering edges.  Splitting by "35 only / 67 only / both" gives
  `T_ij = a_i c_j H + a_i U_j + c_j V_i`, where `H` is the hafnian on
  `{0,1,2,4}` and `U_j`, `V_i` depend only on `j`, `i` respectively (colour of
  vertex 6 and the rest is 0).  The `(b,-a)`/`(d,-c)` annihilation then kills
  every term; I re-derived the cancellation by hand (the `H`, `U`, `V` parts
  cancel separately).  The shared-centre case has no `H` term.  Sound.
* Sign and multiplier bookkeeping matches `src/krenn_gu/two_edge_surplus_shore.py`.
* Division-free, no cofactor assumption, no use of `rho`: confirmed (replay
  reports `uses_rho=false`, `cofactor_divisions=0`; the identity is over Z).
* 134-support claim.  I checked directly that the fifteen zeros are disjoint
  from the 134 live ids of
  `tests/fixtures/recursive_physical_support_n8_four_cut_survivor_134.json`
  and that 174, 245 are live.  So a source with exactly that support has
  `b*d != 0` and is excluded.  Correctly stated as exclusion of that support
  (exact nonzero pattern), not of the parent.
* Term counts (15 per source, 12 for shared-centre, 4,4,5,5 on the 134
  projection, 60 products in 24 pairs and three groups of four) were
  reproduced.

## Bridge and independence

There is no computation-to-mathematics bridge beyond the integer identity,
which is also proved by hand in the document, so the exhaustion and hash
questions do not arise.  The certificate fixture is not hash-pinned and need
not be: the audit regenerates the seed pattern itself and validates the
fixture against it, and it pins the 134-support bytes
(`75cef4c3...f9941fe`).  The audit
`audit_eight_vertex_degree6_source_134.py` uses only the standard library and
rebuilds numbering, all 105 matchings (bitmask recursion cross-checked with a
permutation quotient) and the four sources without importing the primary
module.  It is independent in implementation and enumeration route; it shares
the identity being checked with the primary by design (this is what
`independent_exact_identity_audit` means).  I added a third check below.

## Commands run (all from the worktree root; each under `run_bounded.py`)

```text
python claims/finite/n08/verify_eight_vertex_two_edge_surplus_shore.py          # PASS, 4 patterns, 0.3 s
python claims/finite/n08/audit_eight_vertex_degree6_source_134.py --fixture tests/fixtures/eight_vertex_two_edge_surplus_shore.json   # PASS, 0.4 s
python -m unittest -v tests.test_two_edge_surplus_shore                         # 6 tests OK
python tools/explore/probe_two_edge_shore_parent.py --output-dir <scratch> --replay-assignment tests/fixtures/eight_vertex_two_edge_parent_survivor.json   # PASS_FROZEN_BOOLEAN_ASSIGNMENT, 63 s
```

Reviewer's own sympy reconstruction (not committed): symbolic 252 entries,
all 105 matchings, all four types: identity holds exactly; zero sets equal the
repository's; the wrong-sign control fails; term counts 15+constant and
12+constant.  The parent replay reproduced 600,063 variables, 4,708,644
clauses, orbit sizes 20,160/20,160/10,080/10,080 and the checked assignment.
That last item is context for the "survivor" paragraph only; it is a Boolean
abstraction, not a weighted witness.  No computation exceeded one minute and
none was skipped.

## Frontier and ledger consistency

The frontier row `P17` in `docs/current-frontier.md` matches the document:
physical-source exclusion over every field, 134-support excluded, a different
Boolean survivor remains and is excluded by `ST20`, no unrestricted `n=8`
claim.  It does not overstate.  Ledger status `verified` is appropriate for an
in-document proved identity with exact replay; it does not claim a parent
cover, weights, or Lean.  The ledger `note` correctly says independence is
within one research session.

## Remarks and minor gaps (none blocks acceptance)

1. The sentence "Vertex permutations and one common colour permutation cover
   this defined two-moving-leaf family" is asserted, not proved.  It is not
   load-bearing: the 134 exclusion uses the first type directly, and the other
   three types are individually replayed.  Retain it as a description, not a
   classification.
2. `tests/fixtures/eight_vertex_two_edge_surplus_shore_audit.json` records
   the LF-normalized fixture hash.  On a Windows checkout with
   `core.autocrlf=true` the audit prints the raw CRLF hash instead, so a
   byte-for-byte comparison of the audit output with the stored fixture fails
   on `fixture_sha256` alone (all other fields equal).  Platform artifact,
   not a scientific defect.
3. "Removing any one zero destroys this particular identity" is correctly
   scoped by the document (no global minimality claim); the audit confirms it
   for each of the fifteen zeros.
4. The statement that the new-orbit survivor is excluded by `ST20` is a
   pointer to another entry; it was not re-reviewed here.
5. The primary replay depends on the shared module
   `eight_vertex_physical_hafnian_identity`; this is acceptable because the
   audit does not.

## Verdict

The identity is correct, division-free, and holds over every field as stated;
the four-type claim is individually replayed; the 134-support exclusion
follows.  The document, frontier row and ledger status agree and do not
overstate.  Same-day agent review only; global status unchanged.
