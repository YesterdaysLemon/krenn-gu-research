# Recursive cancellation consistency experiment — 2026-09-12

## Status and parent obligation

This is an **experimental parent attempt**, not a theorem, certificate, or
change to the live frontier.  The global Krenn--Gu conjecture remains
**UNRESOLVED**.  The target is the all-diagonal weighted Bogdanov parent:
exclude actual complex all-diagonal witnesses at every even order, or isolate
an exact cancellation mechanism that survives changing the order.

The upstream supply is the exact hafnian recurrence and the diagonal mixed-word
factorization.  The intended downstream consumer is first the all-diagonal
parent and, only after a separate source-preserving bridge, the unrestricted
conjecture.  A Boolean survivor is not a weighted witness.  An UNSAT solver
status without a checked proof trace is bounded computational evidence.

## The recursive zero-pattern model RZP

For each colour `c` and even set `A`, write

```text
s(c,A)  iff  haf(Z^c[A]) != 0,
g(c,uv) iff  Z^c_uv != 0,
b(c,A,uv) iff g(c,uv) and s(c,A-{u,v}).
```

Here `s(c,empty)=true` and `s(c,{u,v})=g(c,uv)`.  The `b` variables are
truthful equivalences, not existential witnesses.  For every `v in A`, impose

```text
s(c,A) -> OR_(u != v) b(c,A,uv),
b(c,A,uv) -> s(c,A) OR OR_(w != u,v) b(c,A,vw).
```

The first clause says a nonzero Laplace sum has a nonzero term.  The second
says a zero Laplace sum cannot have exactly one nonzero term.  Together they
are the complete local zero-pattern semantics of addition over `C`: zero
terms force a zero result; one nonzero term forces a nonzero result; with two
or more nonzero terms either result is locally possible.

As in AP', require all three full-set hafnians nonzero and forbid every ordered
even two- or three-colour partition for which all participating principal
hafnians are nonzero.

## Exact implication chain

```text
actual all-diagonal complex witness  =>  RZP model  =>  AP' model.
```

The first implication uses the exact values of every principal hafnian.  A
nonzero sum has a nonzero summand; if a zero sum had exactly one nonzero
summand, that summand would itself be zero, a contradiction.  Full-set and
rainbow clauses are the constant- and mixed-word equations.

For the second implication, support follows by induction: from `s(c,A)`,
follow one true `b` term and append its edge to a perfect matching supplied by
the smaller set.  Unique-perfect-matching forcing also follows by induction.
If `G_c[A]` has unique perfect matching `M`, the mate `u` of a chosen vertex
`v` has a unique-matchable remainder, hence its `b` term is true.  Any other
true term would, by support on its remainder, create a second perfect matching
of `A`.  The unique live term therefore forces `s(c,A)`.

The recurrence clauses are strictly stronger than AP' locally, before the
global full-set and rainbow axioms are imposed.  On a six-element proper
subset take the disjoint union of edge `01` and cycle `2-3-4-5-2`.  Declare
the four-cycle hafnian nonzero and the induced six-set hafnian zero.  The local
AP' rules (L), (S), and (F) permit this: both graphs have two perfect
matchings, so forcing does not decide either hafnian, and accessibility holds
on the declared four-cycle.  RZP forbids it because the expansion at vertex
`0` has exactly one live term, namely edge `01` times the declared-nonzero
four-cycle hafnian.  This local separation does not claim that the complete
three-colour RZP and AP' models differ at a tested order.

The reverse implications are not claimed.  RZP forgets the values needed to
make all multi-term cancellations consistent across different recurrences.

## First implementation and controls

The primary implementation is
`src/krenn_gu/recursive_hafnian_support.py`, exercised by
`tools/explore/probe_recursive_hafnian_support.py`.  It uses one unordered
product variable for the same edge/cofactor product shared by the two endpoint
expansions.  The audit implementation
`tools/explore/audit_recursive_hafnian_support.py` imports neither builder nor
variable maps; it uses bitmask subsets, ordered term variables, disjoint-submask
partitions, and a different solver.

Required controls are:

- `n=4` remains SAT;
- deleting singleton-cancellation consistency remains SAT at `n=8`;
- deleting three-part rainbow clauses remains SAT at `n=8`, with the classical
  three-disjoint-perfect-matching support;
- the full model reproduces the known `n=6,8` exclusions;
- exact DIMACS bytes, hashes, bounds, and solver identity are retained.

Agreement between two same-author implementations is useful but is not a
socially independent audit.  A promoted finite theorem still needs a frozen
instance, checked proof trace, independently scrutinized witness-to-CNF bridge,
and the repository's ordinary evidence gates.

## Next exact layer

On any surviving support branch, a zero hafnian with exactly two live Laplace
terms gives a binomial relation among nonzero edge weights and shared subset
hafnians.  These relations may be passed to the existing signed integer-lattice
machinery.  Any learned no-good must name the complete live-term set and allow
escape by gaining or losing a term.  Passing the binomial tests is not a
weighted realization; larger cancellation sums remain.

The experiment succeeds if it produces a checked finite exclusion, an explicit
RZP survivor that sharpens the missing value-level constraint, or a reusable
exact cancellation lemma.  More solver volume alone is not a parent advance.

For `n=10`, H1 and recursive accessibility guarantee a perfect matching in
each colour support.  Vertex symmetry fixes one colour-0 matching.  Its union
with a chosen colour-1 matching is classified under the stabilizer by a
partition of five, where a part `k` denotes an alternating cycle of length
`2k` and a part `1` denotes a shared edge.  The seven conditioned cases are an
exhaustive symmetry cover, not seven independently selected restrictions.
If the first two selected matchings coincide, their common stabilizer is again
the full matching stabilizer.  Choosing a colour-2 matching and applying the
same seven cycle types is therefore an exhaustive subsplit of that one shared
case.

## Observed results

All times below are solver wall times from bounded local runs.  Hashes identify
the exact generated DIMACS bytes.  `UNSAT` in these tables remains a solver
status unless the separate proof column says otherwise.

The finite baselines and sharpness controls behaved as intended:

| instance | result | solver | seconds | DIMACS SHA-256 |
| --- | --- | --- | ---: | --- |
| full `n=6` | UNSAT | CaDiCaL 1.9.5 via python-sat | 0.015 | `16338eda657719933baa6d887091893ef6e3baed0f4eba35f8059de86c123fa4` |
| full `n=8` | UNSAT | CaDiCaL 1.9.5 via python-sat | 107.380 | `f4aa62e8d39121c6bdcf5b17f0e235d1f4b233ddc77382b2fc4462de40098445` |
| same full `n=8` | UNSAT | Glucose 4.1 via python-sat | 71.996 | same bytes |
| `n=8`, omit singleton-cancellation clauses | SAT | CaDiCaL 1.9.5 via python-sat | 0.012 | `860ba6d2f41cfa19d9f5c4bf5fd0ecdc7727e60afccca31d91d913a5b2f0e9f2` |
| `n=8`, omit three-part rainbow clauses | SAT | CaDiCaL 1.9.5 via python-sat | 0.009 | `0d5ca0012a573e1f7f61941571f27632e69e7cc734ac37af8bf7d04f23d2b8b3` |

The primary `n=10` encoding has 18,678 variables and 107,908 clauses in
each top-level conditioned case. The shared-third subcases add five units,
giving 107,913 clauses with the same variables. The exhaustive seven-case
top-level cover returned:

| matching-pair cycle type | result | solver | seconds | DIMACS SHA-256 |
| --- | --- | --- | ---: | --- |
| `(5)` | UNSAT | CaDiCaL 1.9.5 | 198.245 | `98f013336a427ee0899df85423636ab30b6d609036c2bd6ee162dec3009c1a51` |
| `(4,1)` | UNSAT | CaDiCaL 1.9.5 | 146.925 | `fea7a8c38cf6cda17f2b2f8401ff3b2f07fbb78a10ce8cf02c241823e26ebaaf` |
| `(3,2)` | UNSAT | CaDiCaL 1.9.5 | 159.430 | `cbb234db12571733f31d4e7d850a6de5c8eb437fc2f23d08db22d822078f11f4` |
| `(3,1,1)` | UNSAT | CaDiCaL 1.9.5 | 232.875 | `62e1e301ba306c48ed1006314eb086c2d41209f53d08764b690a58e8f0915707` |
| `(2,2,1)` | UNSAT | CaDiCaL 1.9.5 | 165.056 | `3d55f6971600e1127f7d9a3ee875df0f5252b1d95a15579b7925d48f9e6798a6` |
| `(2,1,1,1)` | UNSAT | CaDiCaL 1.9.5 | 121.933 | `fd17a9f60cf91fe6fed3c4494d83f502a4653f380beb1d9e708e2bf28b3bdfab` |
| `(1,1,1,1,1)` | UNSAT | Glucose 4.1 | 225.407 | `61000420ca321b20268b3130ef93047aaddef799e5d468febfd0d0a244b1467a` |

CaDiCaL timed out at 600 seconds on the last unsplit case.  As a diagnostic,
fixing a colour-2 perfect matching and exhausting the same seven cycle types
closed all seven subcases under CaDiCaL in 11.2--28.2 seconds each.  Glucose
then closed the original unsplit bytes, so the subsplit is not needed for the
top-level solver-evidence cover.

The no-import audit encoding has 35,823 variables and 159,343 clauses in each
conditioned case.  Its seven Glucose runs all independently returned `UNSAT`:

| cycle type | seconds | audit DIMACS SHA-256 |
| --- | ---: | --- |
| `(5)` | 107.650 | `725fbe4539c6e001d3d3324609bd3abfb274d35bb36c1a7d7838be5db8abfc77` |
| `(4,1)` | 100.806 | `0625e96102847089e59a6d7368b6288b7b8498b878c4859640a69430d2f5eff4` |
| `(3,2)` | 188.090 | `15096de71da99431a8e2271ef1d96202fe2cd31e1a35a85cfabc13224d7d8c39` |
| `(3,1,1)` | 183.537 | `e1cde4963b8d195af66a65ab5139a446fbc4937a9f3e99742a5a8cffab124b45` |
| `(2,2,1)` | 136.043 | `588e3fd2f48278e1657b0f4932adee309172cd73aa11338d748f6653460c8b46` |
| `(2,1,1,1)` | 225.612 | `524b557fc8f3f9b08d84179a97900708dacb9164f0d10910c93b7d78265aa20f` |
| `(1,1,1,1,1)` | 235.556 | `c47139949ec09c71d083bdf382b4ae27273e13fabb233cae979adbaae6d86334` |

For the smaller frozen instances, native CaDiCaL 1.7.3 emitted binary DRAT
proofs and the separately built `drat-trim` checker accepted them with exact
`s VERIFIED` output.  The `n=6` proof is 27,734 bytes; the `n=8` proof is
76,373,631 bytes.

The same pipeline was then completed for an exhaustive checked `n=10` cover.
The six nonshared top-level cases have direct proofs.  The shared top-level
case is covered by the seven exhaustive colour-2 matching subcases, each with
its own proof.  All thirteen exact CNF/DRAT pairs returned `s VERIFIED` under
the same `drat-trim` executable.  The proof bytes total 496,615,747 bytes.
Their exact identities, cover roles, solver/checker identities, and artifact
policy are frozen in
`recursive-cancellation-consistency-evidence-2026-09-12.json`.  The proofs and
CNFs remain local under ignored `tmp/`; this experiment does not add a roughly
500 MB proof payload to Git.

From the repository root, the complete identity-checking replay is:

```powershell
wsl.exe -d Ubuntu -- python3 tools/explore/replay_recursive_hafnian_drat.py `
  --manifest docs/strategy/recursive-cancellation-consistency-evidence-2026-09-12.json `
  --artifact-dir tmp `
  --checker /home/lemon/conway99-proof-tools/drat-trim-v05.22.2023/drat-trim `
  --output-dir tmp/recursive-hafnian-rzp-replay `
  --case-timeout-seconds 300
```

The original reference invocation reported passing controls and all
thirteen proof cases in 456.873 seconds. Its negative controls were later
found to reject malformed binary input rather than an unjustified proof
step; they are superseded by the semantic controls below. Its untracked
23,892-byte receipt has
SHA-256
`2f282f67987eb105555007051ed74b5783dde8a0271935f52b02407355c74ff9`.
The receipt records driver SHA-256
`27d39e461cdb3ba37c9a8e165dd4d14e2f793d6ad7bbf2cd8f88f5c29438c8d3`
and manifest SHA-256
`21fe7f70b3e1028e53f457f46e3481da057444749654027d88951813c0411ed5`.

On 2026-09-13 the strengthened v2 replay regenerated all thirteen original
CNFs from pinned builder text and typed parameters, matched their exact
bytes, and checked all thirteen proofs again. Its binary controls accepted
the valid proof and semantically rejected both false empty steps, with no
binary parser errors. Recompiling the pinned upstream checker source
reproduced the original binary hash. This replay completed in 560.844 seconds.
The receipt at `tmp/recursive-hafnian-rzp-replay-v2/replay.json` has 32,492
bytes and SHA-256
`3714e6bd534a2043d403834c43dcc0961ca9ba4ab7ca2b12b3e0eaa3e694f6e8`.
It records driver hash
`35a8b2cefc075770a51ca6f190c7a5b447328731431f894b12a2b2504d624c49`
and manifest hash
`be7188269e4e94d75ec9df5a09b133207e8dc2b3f55a58b6c5fbf7e373bacaba`.
These receipt hashes identify raw checkout bytes; builder-source pinning
explicitly normalizes CRLF to LF, whereas frozen CNF identity never does.
The replay now requires python-sat 1.9.dev7 under Linux/WSL. Use a fresh
output directory on each invocation. The constructive symmetry test also
checks an explicit matching-stabilizer relabelling for all 945 matchings.

Fable 5.1's read-only mathematical review found no blocking defect in the
witness bridge, recursive clauses, or cover. It did not rerun the proofs.
The v2 repairs and the new signed-ratio mechanism are documented in
[the continuation journal](cancellation-consistency-continuation-2026-09-13.md).

## Current interpretation

The experiment found no RZP survivor at `n=10`, so there was no surviving
support on which to begin signed-circuit extraction.  Subject to independent
scrutiny of the witness bridge, both encodings, and the symmetry cover, the
checked thirteen-proof result is a candidate exclusion of actual complex
all-diagonal `n=10` witnesses.  It is not a proof of the weaker AP' conjecture:
RZP is the stronger necessary model.  It is not an all-order weighted Bogdanov
theorem, and it changes neither the unrestricted eight-vertex frontier nor the
global Krenn--Gu status.

The independent review and local replay gates have now been exercised as
described above. Durable distribution of the roughly 500 MB proof payload
and final review of the repair delta remain before moving this experimental
strategy note into an owning finite claim. No frontier promotion is made here.
