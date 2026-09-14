# Physical-support refinement sprint — September 13, 2026

## Status and exact obligation

This sprint implements the next bounded step from the cancellation-consistency
handoff: replay guarded source algebra through the existing physical-support
core boundary, then test one fixed eight-vertex support with all proper
cofactor supports free.

It produces two exact **conditional physical-support exclusions** and a typed
replay interface. It does not exclude the eight-vertex parent, prove weighted
realizability of any survivor, or change the global Krenn–Gu status. The
global conjecture remains **UNRESOLVED**.

The parent diagnostic is the full eight-vertex recursive tensor-support
necessary model. The named downstream question is whether source-coupled
cancellation identities can cover every physical support admitted by that
parent. Success for this sprint meant one checked physical exclusion, a parent
exclusion, or a precise projection obstruction—not a count of cofactor
assignments rejected.

## Typed algebraic-clause boundary

[`source_quotient_core.py`](../../src/krenn_gu/source_quotient_core.py) now
accepts three explicit certificate kinds:

- `recursive_quotient_singleton`;
- `binomial_kernel`;
- `recursive-laurent-row-space-v1`.

The dispatch does not accept a caller-supplied success flag or arbitrary cut.
For quotient and binomial certificates it reconstructs original complete
Laplace fibres and exact integer transports. For row-space certificates it
reconstructs every source row, exact Laurent transport, guarded division, DAG
dependency, and final nonzero singleton. Only the clause returned by that
certificate-specific replay is admitted to the physical core.

For every kind, the packet must give exactly the coefficient supports needed
to reconstruct all used fibres. The core then admits only:

1. regenerated unaugmented recursive/target clauses;
2. one separately replayed algebraic clause; and
3. explicit unit assumptions on physical entry supports.

Killers, ratio clauses, preceding learned cuts, and hidden discovery history
remain forbidden premises. The final RUP sequence is replayed by plain unit
propagation without a SAT solver.

The reusable discovery and packing stages formerly left under ignored `tmp/`
are now tracked separately:

```text
python tools/explore/discover_recursive_row_space.py ...
python tools/explore/pack_recursive_row_space.py ...
```

Discovery output is deliberately not accepted as a certificate. The packer
reattaches original integer transports and requires the existing small exact
row-space replay before writing its output.

## Row-space integration control at n=6

The existing two-large-sum regression fixture has ten transported binomial
relations, six replay DAG nodes, and a 60-literal guarded row-space clause.
With its physical entries fixed and proper cofactors free, that one clause
makes the unaugmented full-target recursive model unit-inconsistent.

The new packet
[`recursive_row_space_n6_source_core.json`](../../tests/fixtures/recursive_row_space_n6_source_core.json)
has SHA-256
`984742d7b5f3cc097e2261e6b5abeccb0bf2bf001b4fe43deb93967a74ec19b3`.
Its solver-free replay reports:

| quantity | value |
|---|---:|
| physical literals in projected cut | 43 |
| regenerated recursive/target clauses in core | 102 |
| total core clauses | 146 |
| RUP additions, including empty clause | 1 |

This is the integration control requested by the review: a row-space clause
is consumed by a small physical-source core with every guard and premise
accounted for. It is not a new six-vertex frontier result; the full six-vertex
case is already excluded by stronger theorems.

## Latest 136-entry eight-vertex support

The fixed source is the latest support from the prior full-orbit SAT model,
whose complete Boolean assignment had SHA-256
`b1e97248a93b8dd38f9cda680fb7a1d9f041dac1cce8be1bf86ac2eb06f3af02`.
Only its 136 nonzero physical entry ids are retained in
[`recursive_physical_support_n8_latest136.json`](../../tests/fixtures/recursive_physical_support_n8_latest136.json),
SHA-256
`fddf11afb82d60c039e80db4b97f576f38aeaf817d64e36142627b99fca0abaa`.
The proper-cofactor support assignment from the old SAT model is not fixed.

The tracked bounded loop is:

```text
python tools/explore/refine_recursive_physical_support.py \
  --n 8 \
  --support tests/fixtures/recursive_physical_support_n8_latest136.json \
  --iterations 4 \
  --output-dir NEW_OUTPUT_DIR
```

With no ratio clauses, the base instance has 556,803 variables and 2,823,993
clauses after the 252 physical entry units. Unit propagation supplies a full
cofactor assignment. The cheapest recursive binomial stage finds no circuit;
the unit quotient then finds one nine-relation, 64-literal guarded clause.
That clause is replayed against the original source fibres. Adding it makes
the fixed-support instance UNSAT by unit propagation, with no second Boolean
assignment required.

The promoted small packet
[`recursive_source_quotient_n8_latest136_core.json`](../../tests/fixtures/recursive_source_quotient_n8_latest136_core.json)
has SHA-256
`8f9d6db69e05da80d4533780f7e71f55eb0c4f51b10a7e75e797ebb49fa56e8a`
for the tracked LF bytes. A Windows checkout with CRLF conversion has SHA-256
`3ef1365941080ea46ef9b03a77b375e9dfc28c9554e5638785abbb568fb5aa2d`.
Its solver-free replay reports:

| quantity | value |
|---|---:|
| physical literals in projected cut | 27 |
| regenerated recursive/target clauses in core | 107 |
| total core clauses | 135 |
| RUP additions, including empty clause | 1 |
| killers or ratio clauses used | no |

Therefore the specific 136-entry physical support is excluded by the declared
recursive full-target necessary model, independently of every choice of
proper-cofactor zero/nonzero values. This is stronger than rejecting the old
displayed Boolean assignment and is exactly one physical-support result.

## Parent-cover scorecard

The prior three checked physical cuts had 54, 38, and 32 literals. Their full
orbits under all vertex permutations and one common global colour permutation
left the 136-entry support above. The 27-literal cut removes that support.

The cumulative four-cut orbit test adds 241,920 images of each checked cut
(duplicates retained), for 4,648,164 clauses on 600,063 variables after the
full recursive target, column-killer, and ratio-component necessary
conditions. It remains
**SAT** after 45.884 seconds. Every clause was checked against the returned
assignment, whose physical support has 134 nonzero entries.

The local model has SHA-256
`31c79a4e2eaef4dd141b2a8ddc89350291dfbd4e59719c8df2a152008326a056`;
the summary has SHA-256
`3a71c5e98d48b3215062339ff1f509994a551580e1495a9fb97c0cd833fee459`.
Both remain ignored diagnostic artifacts under
`tmp/full-n8-four-source-cut-full-orbits/`.

Only vertex relabellings and a common global colour relabelling are used.
Independent local colour permutations are not GHZ target symmetries. The SAT
result is a new Boolean support diagnostic, not a weighted witness. It proves
that the four physical cuts and their allowed symmetries still do not cover
the parent; it does not prove that cancellation consistency is exhausted or
that the 134-entry support has complex weights.

## Proof-distance and next all-order question

The proof-distance delta is one physical support excluded and one certificate
kind connected to physical projection. No exhaustive parent edge is closed.
The result is an integration/projection deliverable requested by the parent
attempt, not a new sibling theorem.

The all-order question remains the supplied-family problem from the review.
For each colour `c`, let

```text
U_c = {U subset V : |U|=4 and haf(Z^c[V-U]) != 0}.
```

Each `U_c` is nonempty in a hypothetical all-diagonal witness. The existing
four-set coverage theorem restricts the other two colours on every genuinely
live member of `U_c`. The global-facing missing implication is to combine
those three supplied families with recursive accessibility and signed-ratio
transport to force an incompatible cancellation system—or to produce a
globally constrained Boolean countermodel showing that implication is still
too weak. This sprint does not replace that occurrence theorem with more
finite support counts.

## Follow-up: 25-literal refinement and explicit parent test

The follow-up review observed that physical entries 172 and 244 are not
needed. The independent tracked matching-enumeration verifier proves the
division-free identity in
[`EIGHT_VERTEX_25_LITERAL_PHYSICAL_HAFNIAN_IDENTITY.md`](../../claims/finite/n08/EIGHT_VERTEX_25_LITERAL_PHYSICAL_HAFNIAN_IDENTITY.md).
It retains all 18 zero assumptions but only seven of the nine nonzero
assumptions. The original 27-literal source-core fixture remains unchanged as
a regression and provenance record.

The exact finite parent proposition tested next was:

> **P8-25-occurrence.** Every model of the `n=8` recursive full-target,
> column-killer, fixed-root-killer, and ratio-component necessary conditions
> contains an allowed vertex/common-colour image of at least one of the first
> three source-core physical patterns or the 25-literal identity pattern.

Negating all images is precisely the cumulative four-cut SAT instance. The
27-literal fourth pattern was replaced by the 25-literal pattern, while the
54-, 38-, and 32-literal orbits were held fixed. The bounded run again built
600,063 variables and 4,648,164 clauses and returned
`SAT_ABSTRACTION_NOT_WEIGHTS` in 51.800 seconds; its complete assignment was
checked against every clause. Thus **P8-25-occurrence is false in this exact
Boolean parent abstraction**. This is an exact computational countermodel to
that proposed implication, not a complex-weight counterexample.

The solver returned the same 134-entry physical support as the prior
27-literal run. Both full-model identities, both generation parameter sets,
and the shared physical projection are preserved in
[`recursive_physical_support_n8_four_cut_survivor_134.json`](../../tests/fixtures/recursive_physical_support_n8_four_cut_survivor_134.json).
The large assignments remain ignored diagnostics.

Across the 241,920 images of the 25-literal pattern, the survivor has minimum
guard distance one, attained by exactly three images. The three closest
placements avoid the identity respectively by setting required entry 226 to
zero, or by keeping required-zero entry 122 or 97 nonzero. This identifies the
support-level escape mechanism exactly; entries 172 and 244 are not the
escape.

The resulting all-order candidate is now explicit rather than merely the
definition of `U_c`:

> **Source-isolated 25-pattern candidate (SIP25).** In every hypothetical
> all-diagonal witness, the supplied four-set families, recursive
> accessibility, and signed-ratio transport produce an eight-port source
> whose boundary terms isolate the four physical hafnians in the 25-literal
> identity, up to a common nonzero complementary cofactor.

SIP25 would make the conditional identity an all-order contradiction. The
current Boolean necessary conditions do not even force its `n=8`
support-occurrence specialization, as the checked survivor proves. A viable
next lemma must therefore use an additional weighted/source-isolation
consequence to close the three one-literal escape types, or replace SIP25 by a
different occurrence statement. Merely adding more checked support cuts does
not address that missing implication.
