# Final independent integration review: eight-vertex maximum-root-one exclusion

2026-09-04. Reviewer lab_r2_consolidation_review. Disposition: PASS for the complete finite parent theorem and its connected semantic/certificate package.

Reviewed pins:

| Artifact | SHA256 |
| --- | --- |
| claims/finite/n08/EIGHT_VERTEX_MATRIX_UNIT_EXCLUSION_THEOREM.md | c170542ba74a074cccfb5d3e1e388cc0d416ba0ff0d3dd427c0d8930661acb7c |
| claims/finite/n08/r1-source-certificate/certificate.json | 34d3f3557e952d0c2d03c3b2f8fcb04c2f786400209f76e8e39a7dcbc9e31b8d |
| claims/finite/n08/r1-source-certificate/generate_instances.py | 0c98d9df8f7cd0ebfc3b0c01619a902322f0d075aafb9ab0379816a12fd558ec |
| claims/finite/n08/r1-source-certificate/audit_instances.py | 6efe0812cdb45bc89c1425e61df406e76cdadc61c9bd6ae7338f5b6a5081454e |
| claims/finite/n08/r1-source-certificate/check_proofs.py | e2c0ed26bf21070c2416228fe7f2c9a6c18e781a4732b7cd176d82e9819b7b89 |
| claims/finite/n08/r1-source-certificate/README.md | 133f4fd092c1ab4ab713fe0150cdd50ed4d0843f2e891c9a65e5c20816b76b91 |
| independent packaged proof-replay receipt | 48c76e88836aa50c9d4743616c5c055871ca571d8a13e7c9bb7f58358c06f7e5 |

The frozen specification pins every one of the eighteen final CNFs and all eighteen compressed/raw proof pairs. The final theorem, README, generators/checkers, and the accepted proof-replay records were read. This review does not silently turn a source checker into a DRAT checker; those roles remain separate.

## 1. Exact statement and U1 bridge

The theorem excludes ALL ternary complex eight-vertex GHZ witnesses with maximum fully supported pairwise-zero torus-root cardinality one. Its equivalent complete nonzero matrix-unit statement is correct: a zero physical block or any nonunit bilinear Laurent polynomial admits a torus root pair, while a nonzero matrix monomial has no torus zero. Thus every one of the 28 physical pairs is present, has exactly one ordered endpoint-colour label, and carries a nonzero complex scalar.

No positivity, genericity, moment gauge, scalar-weight normalization, or bounded-variable reduction is used. The conclusion is not an arbitrary-order theorem and not a global Krenn--Gu resolution. It does imply that any hypothetical ternary eight-vertex witness has maximum root cardinality at least two, without asserting an invertible edge exists.

## 2. Exhaustive 1,884-case scaffold cover

Each nonzero pure coefficient supplies a matching of that colour. Three selected pure matchings are edge-disjoint because one physical unit cannot carry two different diagonal labels. Their cubic union is only a scaffold: the other sixteen physical units remain free and nonzero. Disconnected scaffolds are retained.

Vertex permutation fixes M0=01|23|45|67 without changing GHZ or the unit/nonzero property. The stabilizer consists of all permutations of its four pairs and independent pair flips. No colour permutation, additional isomorphism quotient, or unproved catalogue is used.

The previously completed independent audit regenerated 105 matchings by all vertex orders, the 384-element stabilizer by seven-generator closure, and all orbits by breadth-first search. It checked all 1,884 raw ordered pairs and their explicit orbit witnesses. The portable semantic checker independently repeats that reconstruction directly from the durable specification and obtains all eighteen orbits with the exact stated distribution. The C8 and two-C4 count split is consistent: the latter has 3 pair partitions times two switches on each component, giving 12 M1 choices; the remaining 48 form C8. The independently computed allowed-M2 counts are 33 and 31 respectively.

The cover is exhaustive over selected matching triples, not a claim that the eighteen representatives enumerate all physical labelings or weights. The main text correctly preserves that distinction.

## 3. Collision clauses and exact algebraic cuts

Every matching contributes to exactly one word with a nonzero four-edge product. Therefore a mixed singleton is impossible. The pure/equality existence-witness clauses express this support condition exactly: selected witnesses imply the word property, and a label table with the property can choose truthful witnesses. Reverse implications are unnecessary for these existence variables.

The later EXACT membership variables are different. They are IFFs for the eight endpoint labels, with fixed mismatches false and all-fixed matches true. Each algebraic cut negates the conjunction that three mixed fibres retain precisely their two named matching members. The clause includes every possible outside matching as a positive repair literal. It therefore allows a labeling that adds a new cancellation term, and is not an arbitrary whole-model block.

For each stored two-term mixed fibre, nonzero weights give lambda^(chi(M)-chi(N))=-1. Every stored signed relation is exactly zero in Z^28 with odd coefficient sum. Multiplication yields 1=-1 over C. These are necessary SOURCE consequences, not claimed RUP consequences of the weaker collision-only CNF. The final propositional certificates correctly take the augmented final CNFs as their starting inputs.

All 39 cores and every final clause were independently reconstructed earlier, including every generating model's complete 105-word fibre table and satisfaction of prior cuts. The portable checker needs no generating models: each core is a conditional algebraic implication for any labeling retaining those exact fibres. Omitting discovery models from the durable package therefore loses no proof premise.

The theorem's illustrative triple was independently located as exactly the displayed COMPLETE fibres in the audited 002/006 initial models. Removing their nonzero spectator factors gives the three two-by-two permanents of the written matrix. Substituting the first two into the third gives exactly -2 lambda01 lambda25 lambda27/lambda12, nonzero because all four relevant weights are nonzero. The illustration is not substituted for the complete 39-core cover.

## 4. Portable independent semantic checker

The independent checker uses only the Python standard library. It imports neither the generator, discovery producer, SAT solver, nor their semantic maps. It generates matchings from all 8! vertex orders, uses generator closure/BFS for the full stabilizer and raw cover, validates every mixed core and exact integer relation, and rebuilds every clause from semantic descriptors.

Stable IDs are reconstructed using the public wire order: unknown half-edges, allowed pure witnesses, allowed equality witnesses, then first-encounter nonconstant memberships in core/word/matching order. This shared serialization convention is necessary to compare the frozen CNFs; the checker does not trust a producer-supplied variable map or acceptance flag. Clause construction is separated from allocation and compared by full multiset, while raw hashes and header dimensions are checked independently.

Its full bounded run passed all eighteen regenerated instances and all 39 cores in 1.968 seconds, with 180-second/2048-MB containment and child/runner exit zero. Ten self-controls passed. The negative semantic controls bypass the raw-spec hash gate internally and genuinely reject a changed core sign, a pure word treated as zero target, a repeated matching, an omitted scaffold orbit, a missing reverse membership implication, a dropped possible repair matching, an incorrect variable header, and malformed DIMACS termination.

The packaged audit_instances.py is EXACTLY the original independently written checker after CRLF-to-LF normalization. Both a byte-normalized comparison and an AST comparison confirmed this. Its scope explicitly excludes DRAT checking. The self-test-only mode is correctly documented as insufficient to verify generated CNFs.

The generator's default adjacent certificate path and canonical case-id filenames agree with the documented root-directory commands and with the independent checker. The coordinator also ran those public default-path commands successfully. All 14,899,605 generated CNF bytes are pinned rather than inferred from counts alone.

## 5. Connection to independently accepted UNSAT proofs

The original independent DRAT audit records all eighteen exact CNF/proof pairs with stable before/after hashes, exit zero, and the exact line s VERIFIED, without s NOT VERIFIED. It checked the source/binary provenance and meaningful positive/negative proof controls.

I separately compared every specification case against those accepted audit records and against the packaged replay receipt. Every case has the same CNF hash and raw proof hash in all three places. The packaged replay also records stable input bytes and accepted exit-zero/exact-VERIFIED results for all eighteen cases, with all three controls passing.

All eighteen current proof archives were losslessly decompressed in memory for identity comparison. Their compressed bytes match the specification, and every decompressed stream matches the exact independently checked raw proof hash and length. Totals match the owning text: 8,003,487 raw proof bytes stored in 2,039,952 compressed bytes. No compression semantics or omitted discovery artifact changes the mathematical proof object.

The earlier HOLD pending final UNSAT certificates is therefore discharged by the separately completed certificate audit, not by reinterpreting the solver's native status or by the semantic checker alone. With the exhaustive source-to-final-CNF implication already checked, the accepted UNSAT leaves close the whole stated n8/r1 parent.

## 6. Tool provenance, portability, and trust boundary

The README accurately separates generator, semantic audit, and native proof verification. The pinned DRAT-trim source commit, LF source hash, and executed binary hash agree with the independent audit. The recorded independent rebuild was byte-identical. The pinned Makefile's drat-trim target uses the documented gcc drat-trim.c -std=c99 -O2 command, so the build instructions match the cited build recipe.

The proof driver verifies specification/CNF/compressed/raw pins, uses a new output directory, checks exact acceptance lines with exit codes, retains durable replay logs, and removes temporary decompressions. It requires Linux/WSL and documents outer containment. The checker-hash override is explicitly for an independently trusted alternate build, and the README correctly states that a hash does not prove an arbitrary executable sound. The external proof checker remains an explicit tool dependency; no Lean or kernel formalization is claimed.

The proof archives are treated as opaque binary certificate data through the package .gitattributes. Raw CNFs, external executables, solver logs, and discovery models are not misrepresented as required committed proof objects.

## Final verdict and remaining scope

PASS for the whole integrated finite parent proof. The hypothetical-witness-to-scaffold, scaffold-to-final-CNF, exact Laurent-core, and independently checked UNSAT implications are connected with explicit scope and immutable data pins. No selected-weight gauge, unsupported variable bound, partial model cover, missing repair term, unconnected UNSAT verdict, or generic-to-pointwise step was found.

The result removes only the ternary eight-vertex maximum-root-one child. Other root orders/incidences, arbitrary n, and the original global conjecture remain open as stated. No publication or tracked edits were performed by this reviewer. All owned audit runs completed; no process remains running. A later status/frontier-only change may be checked by a pinned diff addendum.

## Final editorial and frontier addendum

2026-09-04. Final PASS for owning-document SHA256:

  ea9c5f5e749cfed0191a7342b708ac76abb621ba92828ea5e3c322bc32c93383

An exact byte-level reversal of only the proved-status header and the clarification 'permutations of the four pairs' reproduced the previously reviewed owner hash c170542ba74a074cccfb5d3e1e388cc0d416ba0ff0d3dd427c0d8930661acb7c. Thus no mathematical proof, hypothesis, quantified conclusion, or example changed.

The specification, three program files, and README retain all hashes pinned in the main review. The package .gitattributes now has SHA256 a59ec2244708793d9984880e89a3cdf1d8b256b56fc4d6ee7613fea700a47883. Resolved Git attributes were checked: certificate.json has text unset, and proof archives have text and diff unset. This preserves the exact JSON/proof byte pins across checkout without altering any certificate data.

Reviewed the new N8R1 node, U1 finite-specialization entry, complete-cover relationship, and N8R1-to-M2 source-branch arrow. They correctly close only the TERNARY n=8/r=1 case, preserve arbitrary-order U1 as open, and infer r>=2 at that order without an invertible-edge assumption. The n08 README and parent-outcome record were explicitly clarified to say ternary. No arbitrary-d root-one claim is being inferred from a three-colour restriction, which could introduce zero physical blocks.

The parent strategy accurately records that the first ten label tables were not a complete labeling catalogue, that exact complete-fibre cuts retained potential repair matchings, and that all eighteen final instances subsequently received independent certificates. It does not introduce a weight-gauge or bounded-variable fallback as a proof premise.

The public semantic review's integration prefix explicitly treats its earlier UNSAT HOLD statements as discovery history and discharges the separate gate through the certificate and integration audits. It does not relabel semantic reconstruction as DRAT proof checking. The certificate review's portable appendix accurately preserves checker provenance, gzip/raw identities, process closure, and the external compiled-tool trust boundary. Those evidence roles remain distinct.

Final mathematical, package-byte, and proof-topology disposition: PASS. No new proof run or research was performed for this addendum. No tracked files were edited by this reviewer, and no process remains running. Ready for the coordinator's staging and ordinary final checks.
