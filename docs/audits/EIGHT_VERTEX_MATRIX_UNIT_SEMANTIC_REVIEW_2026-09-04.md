> Integration status: the source-semantics audit below is PASS. Its earlier
> pending-UNSAT statements record the discovery phase. The separate
> [certificate audit](EIGHT_VERTEX_MATRIX_UNIT_CERTIFICATE_REVIEW_2026-09-04.md)
> subsequently accepted all eighteen exact final instances, and the
> [integration review](EIGHT_VERTEX_MATRIX_UNIT_INTEGRATION_REVIEW_2026-09-04.md)
> composes those distinct gates. The semantic audit is not relabelled as a
> DRAT checker or a formal proof.

# Independent eight-vertex r=1 bridge, scaffold, encoding, and model audit

2026-09-04. Reviewer lab_r2_consolidation_review. Scratch research review; no PR or mathematical-status promotion. Global Krenn--Gu remains UNRESOLVED.

## Current disposition

PASS for the mathematical bridge to complete nonzero matrix units and necessary matching-word collisions; PASS for the exhaustive 18-scaffold cover; PASS for independent reconstruction of all 18 support CNFs and exact checking of all 10 exported SAT label tables.

There is NO complete r=1 exclusion at this checkpoint. Eight UNSAT reports are native solver outcomes without accepted proof traces, and ten scaffolds have SAT label assignments. Those assignments are not weighted GHZ witnesses. Even proving a weight obstruction for all ten exported tables would not exhaust all label assignments within their scaffolds.

The coordinator has subsequently proposed proof-producing algebraic CEGAR. Its abstract complete-fibre nogood rule is audited in Section 7 below; implementation and any final UNSAT proof remain separate checks.

## 1. Existing repository status and scope

The owning MAXIMAL_TORUS_ROOT_SATURATION_AND_COORDINATE_ABSORPTION_THEOREM.md, Section 3, proves the r=1 matrix-unit normal form and a forbidden-word cancellation obligation; it explicitly does not exclude that branch. The current frontier's U1 node likewise remains open.

The existing eight-vertex U7D work is a fixed-template sharpness construction and its subsequent exact template exclusion, not an all-label r=1 theorem. Its mixed singleton already prevents it from being a witness. The finite n08 navigation contains the recently completed r=2 common-coordinate and diagonal-root-leg results but no general n8/r1 closure. The present parent therefore does not duplicate a committed full r=1 exclusion found in the focused owning-document search.

## 2. Exact mathematical bridge

For maximum torus-root cardinality one, every physical edge form must be zero-free on the product torus. This includes exclusion of a zero block, which would admit a pair immediately. Over C a zero-free Laurent polynomial is a unit, and bilinearity then forces one nonzero matrix entry. Thus ALL 28 blocks are nonzero matrix units. Conversely such blocks make every torus edge evaluation nonzero, hence the maximum is one. No edge may silently disappear in this branch.

Each perfect matching uses four nonzero edge weights and determines exactly one ordered vertex-colour word. Its product weight is nonzero. Therefore a nonconstant word with precisely one contributing matching cannot have zero target coefficient. More than one contribution may still fail to cancel, and a pure fibre with multiple terms may sum to zero; cardinalities alone do not solve the complex source equations.

Each nonzero pure coefficient supplies at least one all-c matching. Choose an ordered triple M0,M1,M2. They are edge-disjoint because one physical matrix unit cannot have two different diagonal labels. Their 12-edge union is a spanning cubic, properly three-edge-coloured scaffold. It need not be connected. The other SIXTEEN physical edges remain nonzero units with unrestricted endpoint labels and nonzero complex weights.

Vertex permutation can fix the chosen M0 as 01|23|45|67, preserving GHZ and the torus-root condition; reorientation of an edge simply transports its endpoint colours and transposes its block when necessary. No colour permutation or weight normalization is needed. Multiple possible scaffold choices for one graph cause harmless overlap, not a loss of coverage.

## 3. Independent complete scaffold verification

Cover artifact:

  tmp/lab-r1-scaffold-cover.json
  SHA256 608408587cfadaafd4e746a0f601d8353a64e4bf16fb9cbdebd27a85bac384c7

The primary constructor uses least-unpaired-vertex recursion and an explicit 4! times 2^4 group list. My independent audit uses a different finite route: partition every permutation of eight vertices into four adjacent pairs and deduplicate, obtaining all 105 matchings. It separately generates the M0 stabilizer by closure under four within-pair swaps and three adjacent pair swaps, obtaining exactly 384 permutations. Raw ordered pairs are selected by independent edge-mask disjointness.

The audit recovered 60 M1 choices and 1884 ordered disjoint (M1,M2) pairs. It generated their orbits by breadth-first closure under the seven generators, not by copying the producer's all-384-image routine. It recovered 18 orbits with sizes

  12:1, 48:7, 96:6, 192:3, 384:1.

Every reported representative, orbit size, stabilizer size, and all 1884 explicit representative-to-raw permutation witnesses were checked. The full raw set is covered exactly once by these orbits. This includes the disconnected two-K4 scaffold. There is no connectedness assumption, hidden graph catalogue, colour swap, or additional quotient.

The count 197820 for ordered triples without fixing M0 is 105 times 1884. It is a count of selected matching triples, not distinct weighted graphs or physical label tables.

## 4. Encoding semantics and independent clause reconstruction

Encoding source:

  tmp/lab-r1-sat.py
  SHA256 9ba5ff9084688e6df9eb90b77862ea9dba5fd71792698333e1c275d4e417aa96

Results:

  tmp/lab-r1-sat-results.json
  SHA256 5e7d2b85169717e6eb748050206be31d93ae16a9e4b932f2eac70002b0d1be7e

The 12 scaffold edges are fixed to their respective monochromatic labels. Each endpoint of every other edge has exactly one of three colours; thus all 16 remaining blocks remain nonzero units, with one ordered endpoint label pair each.

For every matching, a clause requires a pure-word witness or an equality witness with ANOTHER matching. A pure witness implies all vertex labels equal its colour. An equality witness implies all eight vertex labels agree between its two distinct matchings. The variables may be one-way witnesses: if a physical label table has the requisite pure words or collisions, truthful witnesses exist; conversely any selected witness forces the requisite word condition. No reverse witness implications are needed for this encoding. Pruning uses only contradictions among already fixed scaffold labels.

My standard-library audit imports neither the constructor nor the SAT solver. It reads the semantic variable map, independently reconstructs the full allowed variable set and every expected clause, and compares the complete clause MULTISET against each of the 18 frozen CNFs. It also verifies their raw hashes, map hashes, scaffold metadata, and matching index order. Fixed/fixed, fixed/variable, shared-half-edge, and variable/variable equality cases are all reconstructed. All 18 comparisons passed.

This establishes the stated necessary support semantics. It does not add unknown phase or magnitude constraints, enforce a converse from support to a complex witness, or normalize selected matching weights to one.

## 5. Independent SAT label and 105-fibre checks

For all ten SAT reports, the audit checks all 28 decoded edge-label pairs and every fixed scaffold label. It independently evaluates all 105 matching words using its permutation-generated matching list and compares EVERY exported word fibre and matching index. It then constructs truthful pure/equality auxiliary assignments from those words and verifies that they satisfy the ACTUAL frozen CNF. This is more than repeating the producer's own direct_replay function.

All ten tables have 41 nonempty word fibres and no mixed singleton. The detailed results are:

- 002,003,006,013,014,016,017 each have 38 mixed binomial fibres and pure multiplicities a permutation of (24,4,1).
- 004,005,015 each have 36 mixed binomial fibres, one four-term mixed fibre, one 24-term mixed fibre, and pure multiplicities a permutation of (2,2,1).

Each table therefore accounts for exactly 105 matching terms. No scalar edge weights were solved or claimed. Binomial relations require actual ratios -1, aggregate fibres require actual sums zero, and each pure fibre must have its prescribed nonzero sum.

These are ONE exported SAT table per surviving scaffold, not an exhaustive physical-label cover. The 18 scaffolds are exhaustive; the ten label tables are not. Their exact weighted exclusion alone would not close those scaffolds.

## 6. Independent run and process ownership

Independent script:

  tmp/lab-r1-independent-audit.py
  SHA256 54f095e94ee69b91bc25327eaa642431b42b618fd2c52979cd154c0b098608eb

Machine-readable result:

  tmp/lab-r1-independent-audit.json
  SHA256 a723356ef2aabcb7c069a729ec8e003e8c8e64f974c4f1a0251eb3f8a3bd2d3d

The single owned run used tools/research/run_bounded.py with run id r1-independent-cover-cnf-models, timeout 180 seconds, aggregate memory 2048 MB. Its durable run.json records status succeeded, elapsed 2.468 seconds, child exit 0 and runner exit 0. The child PID was 32836 and has completed. No worker or unrelated process was stopped, and no owned process remains running.

The eight reported UNSAT statuses were not independently certified by this audit. Exact clause reconstruction does not turn a solver verdict into a proof.

## 7. Proposed algebraic CEGAR: mathematical schema audit

The coordinator's proposed rule is sound if implemented exactly as follows. For a MIXED word whose COMPLETE matching fibre is {M,N}, nonzero edge weights give

  w^(chi_M-chi_N)=-1.

If a saved integer combination of such exponent differences is exactly zero in all 28 edge coordinates, and its coefficient sum is odd, multiplication of the Laurent equations gives 1=-1 over C. Negative exponents and coefficients are legal because all edge weights are nonzero. No modular-only relation or selected-weight normalization suffices.

A learned label nogood must negate ONLY the conjunction that these word fibres remain COMPLETE. For each involved word it includes negative membership literals for its two claimed members and positive membership literals for EVERY other matching. Hence a new labeling that adds another potential cancellation term is allowed. Blocking an entire arbitrary SAT labeling without this proved condition would be invalid as a general weighted-source cut.

Membership(w,M) must be an IFF with the eight endpoint-colour conditions, including fixed-mismatch false and all-fixed-match true cases. One-way witness clauses are insufficient for these new exact-fibre literals. A core receipt must identify mixed words, member matching IDs, the full integer exponent relation, odd coefficient sum, and the corresponding learned clause. The complete-fibre condition, rather than just survival of two terms, is load-bearing.

This audits the mathematical learning SCHEMA only. Its eventual implementation, every emitted core, all reconstructed models, and any final UNSAT certificate are separate required checks. A SAT table surviving the bounded search for an odd relation is still not a weighted GHZ witness and must not be blocked without another proof.

## Final boundary

The finite bridge, cover, existing collision encoding, and all exported SAT models pass independent exact review. They do not yet prove the n8/r1 parent. Current all-label source exclusion requires either complete certified unsatisfiability of a sound refined cover, or another exhaustive mathematical implication. Existing fixed-template exclusions cannot be promoted to that result.

No tracked files were edited. All produced artifacts are assigned scratch, and no process remains running. Global and other root-order scopes remain unchanged.

## 8. Completed independent CEGAR implementation and artifact audit

2026-09-04. PASS for the exact necessary-source refinement implemented by:

  tmp/lab-r1-cegar.py
  SHA256 c933a20570fc32ae90afecf645859b5db0ef661793a6e9f4dea52c3791ae3809

Manifest:

  tmp/lab-r1-cegar-results.json
  SHA256 56c48349478e901c742357452fd792e4f97263aa813a31fdaa108a8662073320

The manifest reports all 18 final instances solver-UNSAT after 39 exact odd-triple cuts. This audit DOES NOT certify those final UNSAT verdicts. It independently verifies that every added clause is a necessary condition for a weighted source and that the final CNFs contain exactly the reviewed ingredients.

Independent audit script and result:

- tmp/lab-r1-cegar-independent-audit.py, SHA256 fa95e73c68d77a1de1c03a6b5885ffbcd25ef9765980f9169b2630abc169ad08.
- tmp/lab-r1-cegar-independent-audit.json, SHA256 12948ddcb68d212205a98a139cfecff72bd727c60cb8ce4634e46bca5b9e7250.

The script imports neither the SAT producer, its base encoder, nor a solver. It pins the previously independently audited base manifest/CNFs/maps, independently regenerates all 105 matchings through vertex permutations, and checks every newly emitted semantic variable and learned clause.

All checks passed:

1. Every final representative, scaffold, matching index, CNF hash, map hash, and model-log hash agrees with the frozen manifests. Base variable semantics remain an unchanged prefix.
2. Every one of the 39 generating label tables has all 28 unit labels, the required pure scaffold, and exactly the independently reconstructed 105 word-fibre memberships. No mixed singleton occurs.
3. Each core contains three DISTINCT mixed words with their actual COMPLETE two-member fibres. Its three exponent differences are recomputed from all 28 physical-edge incidence coordinates. The signed sum is exactly zero over the integers and the coefficient sum is odd. Saved vectors and totals match, without a modular approximation.
4. Membership variables are precisely the nonconstant word/matching pairs requested by the cores. Their clauses encode BOTH directions of the endpoint conjunction. A fixed mismatch is correctly false, and an all-fixed matching word is correctly true; no unconstrained witness can stand in for an exact membership.
5. Each learned clause is reconstructed as the negation of ALL three complete fibres: negative literals for their two members, positive literals for every other matching. Constant literals, deduplication, and absence of tautological complements are checked. No whole-label-table blocking clause or omitted potential repair matching is present.
6. Truthful auxiliary membership/pure/equality assignments show every generating label model satisfies the actual base CNF and every prior learned cut, and violates its new cut. This confirms both semantic validity and the claimed incremental progress.
7. For ALL 18 final CNFs, the entire clause multiset is exactly the audited base CNF plus all reconstructed membership IFF definitions and the 39 independently proved core clauses. No other hidden clause or unsupported cut was added.

The owned run used run id r1-independent-cegar-chain, 180 seconds and 2048 MB. Durable metadata reports succeeded in 14.233 seconds, child exit zero and runner exit zero. Its child PID 31056 has completed. No process remains running.

### Why the final SAT proof remains a separate gate

The algebraic cuts are necessary consequences of the COMPLEX WEIGHTED SOURCE, not necessarily propositional consequences of the weaker collision-only base CNF. They are therefore accepted as additional input clauses only through their explicit odd-Laurent-relation bridge above. A final propositional UNSAT checker must check the frozen FINAL CNFs containing these clauses. Its proof plus the independently checked cover/encoding/algebraic bridge could close the whole n8/r1 parent; a native UNSAT status alone cannot.

Current final disposition: PASS for cover, encoding, all initial and incremental label models, every algebraic core, and final-CNF reconstruction. HOLD for mathematical promotion of the r=1 exclusion until all 18 final UNSAT instances receive accepted exact certificates and independent checking. No weighted witness or global resolution is claimed.
