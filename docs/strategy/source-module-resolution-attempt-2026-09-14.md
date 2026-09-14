# Source-coupled resolution attempt — 2026-09-14

Status: two independently checked conditional source exclusions; the combined
Boolean occurrence parent is refuted. Global Krenn–Gu is **UNRESOLVED**.

## Parent and first load-bearing test

The global target is nonexistence of complex pair-source witnesses `T_W=Delta_n`
for every even `n>=6`, with three colours (restriction covers larger alphabets).
The selected finite parent P8 is the same nonexistence statement for all 252
physical entries on eight vertices. Its downstream consumer is unrestricted
eight-vertex exclusion; no reduction from arbitrary order to P8 is asserted.

The immediate implication P134 is: a P8 witness cannot have exactly the live
entry set in `tests/fixtures/recursive_physical_support_n8_four_cut_survivor_134.json`.
Every absent entry is zero and every listed entry is nonzero. The fixture is a
Boolean projection, not a physical witness. P134 is a necessary local test of
the proposed source-cancellation mechanism, not an exhaustive cover of P8.
Its upstream supply is the original full hafnian equations and the checked
17-zero/six-nonzero boundary consequence `rho=g88*g91-g82*g97=0`.

The first attempt synthesizes the physical 25-literal cofactor elimination and
the larger-sum row-space mechanism, as sharpened in the six-turn `Review Krenn
Gu Repo` discussion. The one-relation direct quotient is already inert; the
729 elementary shared-vertex rows are not the complete degree-five module.

Work over `Q[g_s:s live]`, interpreted pointwise over C, with actual induced
hafnians expanded as polynomials. Full source equations have physical degree
four. Include every full target equation `P_a=T_W(a)-delta_a` and every
`g_s*P_a`, plus the relevant polynomial consequences of rho through degree
five. No cofactor is made independent, divided out, or specialized. The three
pure-minus-one equations must remain visible. Any localization must use only
declared live physical entries and clear its denominators in the certificate.

Success is an exact, independently replayed identity
`M=sum q_a P_a + q_rho rho`, where M is a nonzero scalar times a monomial in
declared live entries; or a proved limitation of the entire stated bounded
space that identifies the next genuinely new interaction. High matrix rank,
modular consistency, or timeout alone is not either outcome. An apparent
weighted witness triggers dedicated full-target validation before any claim.

The reviewed base is d645b93105517634cac54930ab8ce23fc5f16563 (open PR 347),
which is a descendant of freshly fetched origin/main dc4e7c9e. An isolated
checkout was created from origin/main and fast-forwarded to this base. Other
worktrees and the original untracked review artifacts are preserved.

Initial resource limits: at most three research processes, each bounded to
900 seconds and 8192 MiB; preserve at least 20 percent free host memory.
No GPU expenditure until a concrete GPU-suitable calculation exists.
No replay of the unrelated large n=10 archive. One integration owner packages
accepted results after a mathematical delta exists. Exact adversarial review
precedes promotion; a finite support exclusion would leave parent coverage
and the all-order theorem open.

## Mathematical delta and next parent test

The degree-six search found a four-source identity excluding P134, independently
reconstructed by two implementations. It requires only 15 zeros and two nonzeros,
not rho. The mechanism is the already-known majority-shore internal-edge ideal
specialized to a five-shore whose two-edge cover can be annihilated. This is a
new explicit guarded pullback of that mechanism, not a new majority theorem.

The next declared parent implication P8-two-edge-occurrence is: every model of
the existing recursive full-source, column-killer, fixed-root-killer, ratio-
component conditions and the four previous physical-cut orbits contains a
two-edge-covered five-shore pattern. The family tested includes both disjoint
and shared-centre edge covers and both equal and distinct alternate colours;
the complete vertex/common-colour orbits are included. These four types exhaust
this specifically defined two-moving-leaf, two-edge family, not all possible
majority-shore annihilators. SAT with a fully checked assignment refutes this
Boolean occurrence implication only. UNSAT needs exact proof plus bridge review
before it could imply unrestricted eight-vertex nonexistence.

The protected pure-matching scaffold already blocks an inference from column
killers alone to general majority-shore exclusion. Full source coupling remains
load-bearing; the new cut must not be advertised as an all-order bridge.

## Second synthesis and observed boundary

The two-edge occurrence test returned a fully clause-checked, different
134-entry support. A degree-six eight-row identity then excluded it. Pulling
that identity back to complete source expansions gives the uniform two-slice
shared-hafnian transfer: for every even n>=4, the stated 4(n-4)+2 zeros and two
nonzeros force a contradiction. Its n=8 guard has eighteen zeros. Four ternary
colour-equality types exhaust this specific template; both the human proof and
their full physical polynomial specializations were independently reviewed.

The stronger Boolean parent, with all four old orbits, all four two-edge orbits,
and all four transfer orbits, still has a clause-checked 129-entry survivor.
Its exact parameters, canonical CNF identity and packed full assignment are
in `tests/fixtures/eight_vertex_two_slice_parent_survivor.json`. This is the
precise negative result for the proposed template-occurrence parent, not a
weighted counterexample.

The next bounded calculation includes all quadratic-multiplied full target
rows whose endpoint-colour grade can meet a pure target. It has 8,385 live
quadratic multipliers, 20,280 complete grades and 142,328 rows. Exact rational
elimination gives leading degree-six rank 142,328, hence zero high kernel:
there are no low quadratic residuals to couple between grades. The augmented
blocks contain no monomial either. This covers the complete declared
pure-attached space, including repeated/shared-vertex multipliers. It excludes
neither mixed-only unattached degree-six grades nor the full ideal. The primary
calculation and its independent audit are recorded below; no unbounded-degree
ideal-consistency claim is made.

The [independent degree-six audit](../../claims/finite/n08/audit_eight_vertex_degree6_pure_coupling.py)
reverses the enumeration (compatible words first, then multiplier lookup),
expands bitmask matchings without primary scientific imports, and uses exact
column dependencies. It checks 991,108 high monomial columns, retains all
25,155 pure tails, agrees on full high row rank, and finds zero augmented
coloops. Rank and coloop controls include an example whose rational rank differs
from its characteristic-two rank. The
[primary finite receipt](../../tests/fixtures/eight_vertex_degree6_pure_attached_129.json)
records the declared space and counts. The audit runs directly with
`python claims/finite/n08/audit_eight_vertex_degree6_pure_coupling.py`.

Checkout registration used the start-project workflow. Its generated root
manifest/import would violate this repository's stricter Phase-R3 allowlist;
the generated files were retained under ignored scratch and the checkout was
registered without adoption. No root policy or inherited instructions changed.

## Reproducible checkpoint and remaining parent

The owning mathematical results are
[the two-edge shore exclusion](../../claims/finite/n08/EIGHT_VERTEX_TWO_EDGE_SURPLUS_SHORE_EXCLUSION.md),
[the uniform two-slice transfer](../../claims/arbitrary-order/TWO_SLICE_SHARED_HAFNIAN_TRANSFER_OBSTRUCTION.md),
and [the complete degree-five limitation](../../claims/finite/n08/EIGHT_VERTEX_DEGREE_FIVE_SOURCE_MODULE_LIMITATION.md).
Their documents specify the exact premises, polynomial identities, independent
algorithms and mutation controls. No external paid model or GPU was required.

The two complete SAT assignments are durable compressed fixtures. These commands
regenerate the canonical CNFs and replay every frozen variable without solving:

```text
python tools/research/run_bounded.py --run-id shore-parent-replay --timeout-seconds 900 --memory-mb 8192 -- python tools/explore/probe_two_edge_shore_parent.py --replay-assignment tests/fixtures/eight_vertex_two_edge_parent_survivor.json --output-dir tmp/shore-parent-replay
python tools/research/run_bounded.py --run-id transfer-parent-replay --timeout-seconds 900 --memory-mb 8192 -- python tools/explore/probe_two_edge_shore_parent.py --include-two-slice --replay-assignment tests/fixtures/eight_vertex_two_slice_parent_survivor.json --output-dir tmp/transfer-parent-replay
python tools/research/run_bounded.py --run-id pure-degree6-replay --timeout-seconds 900 --memory-mb 8192 -- python tools/explore/probe_degree6_pure_coupling.py tests/fixtures/eight_vertex_two_slice_parent_survivor.json --output tmp/pure-degree6-replay.json
```

Use fresh run IDs and output directories on repetition. The stronger CNF has
SHA-256 `ccfb1128ef41ba2420d1958e31e2d84661cd12d8ba6762edda5a39e64882d296`.
Both original and no-solver replays checked every clause and the full physical
projection. SAT disproves only occurrence in this exact necessary Boolean model.

The sharp obstruction to the selected parent route is now a concrete 129-entry
Boolean model avoiding all twelve tested orbits, with no contradiction in the
complete pure-attached quadratic-multiplier space. Thus another certificate of
that same declared type cannot exclude this support. A further source-module
attack must use unattached mixed-only grades, higher multipliers, or additional
proved source relations. Before another sibling exclusion, select an implication
that explains why its mechanism is supplied in the remaining parent; no cover
has been established by the support count decreasing.

The broader structural control remains the protected pure-matching scaffold.
It satisfies the existing majority hierarchy, so a parent proof must either
exclude it through shared full-source equations or supply a detector that is
not forced by that hierarchy alone. No reduction of arbitrary sources to that
scaffold, or of arbitrary order to n=8, is claimed.
