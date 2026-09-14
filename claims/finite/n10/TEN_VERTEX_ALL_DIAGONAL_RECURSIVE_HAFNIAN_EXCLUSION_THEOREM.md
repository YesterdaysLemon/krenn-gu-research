# Ten-vertex all-diagonal recursive-hafnian exclusion

## Status

This is a **finite computer-assisted exact theorem** over the complex numbers.
It proves:

> No ternary all-diagonal Krenn–Gu witness exists on ten vertices.

Here *all-diagonal* means that every edge block has only its three
monochromatic entries, so the data are three complex symmetric hollow
matrices `Z^0,Z^1,Z^2`. The theorem does **not** exclude the weaker AP'
support abstraction at `n=10`, does not address graphs with bichromatic block
entries, and is not an arbitrary-order theorem. The global Krenn–Gu
conjecture remains **UNRESOLVED**.

Mathematical status, certificate status, independent-audit status, and
formalization status are separate:

- mathematical status: finite computer-assisted theorem at the scope above;
- certificate evidence: thirteen exact CNF/binary-DRAT pairs replayed by the
  pinned `drat-trim` executable, including positive and negative checker
  controls;
- independent audit: a no-import implementation reconstructs every CNF byte,
  the seven matching-pair types, all 945 matching transporters, and the exact
  proof-file identities;
- formalization status: no Lean formalization is claimed;
- external review: the September 13 review inspected the bridge and finite
  cover but did not itself replay the proof archive. The independent code path
  below is reproducible scrutiny, not a claim of a separate human referee.

## 1. Recursive zero-pattern model (RZP)

For a colour `c`, an even vertex set `A`, and an edge `e={u,v}` in `A`, write

```text
g(c,e) = 1  iff Z^c_e != 0,
s(c,A) = 1  iff haf(Z^c[A]) != 0,
b(c,A,e) = g(c,e) AND s(c,A-e).
```

The empty hafnian is one, and `s(c,{u,v})` is identified with `g(c,{u,v})`.
For each vertex `v` in `A`, the exact Laplace expansion is

```text
haf(Z^c[A]) = sum_(u in A-v) Z^c_vu haf(Z^c[A-{v,u}]).
```

RZP retains the two support consequences that are valid over `C`:

1. if `s(c,A)=1`, at least one incident `b` term is one;
2. if `s(c,A)=0`, the number of incident `b` terms is not exactly one.

It also defines every `b` by the full Boolean equivalence above. For every
ordered even three-part partition `V=A_0 disjoint-union A_1 disjoint-union
A_2` with at least two nonempty parts, it imposes

```text
not s(0,A_0) or not s(1,A_1) or not s(2,A_2).
```

Finally, `s(c,V)=1` for all three colours. RZP is stronger than AP' because it
shares every principal-hafnian support variable across all Laplace expansions
and retains singleton noncancellation. It remains only a necessary model, not
a sufficient condition for complex weights.

### Witness-to-RZP bridge

Every complex all-diagonal witness yields an RZP model.

The product equivalences are definitions of nonzero products. A nonzero sum
has a nonzero summand, while a sum with exactly one nonzero summand cannot be
zero in a field; hence both Laplace support rules hold. The three constant
target words give `haf(Z^c[V])=1`. For a nonconstant word with colour classes
`A_0,A_1,A_2`, diagonality factorizes its coefficient as

```text
haf(Z^0[A_0]) haf(Z^1[A_1]) haf(Z^2[A_2]).
```

The GHZ target makes this product zero, giving the rainbow clause. Thus RZP
UNSAT is sufficient to exclude an all-diagonal witness. No converse is used.

## 2. Exhaustive thirteen-case cover

Because `haf(Z^c[V])` is nonzero, the support graph of each colour contains a
perfect matching. Choose support matchings `M_0,M_1,M_2`.

Fix `M_0` to the standard matching. The union of two perfect matchings is a
disjoint union of alternating even cycles; shared edges are cycles of
half-length one. At ten vertices the possible partitions of five are exactly

```text
(5), (4,1), (3,2), (3,1,1), (2,2,1), (2,1,1,1), (1,1,1,1,1).
```

For the first six, `M_1` is not equal to `M_0`. A vertex relabelling takes
`(M_0,M_1)` to the corresponding canonical pair. The six top-level CNFs fix
only those colour-0 and colour-1 matching edges; `M_2` remains existential.

In the seventh case `M_1=M_0`. The same matching is therefore fixed for both
first colours. A relabelling that preserves this common matching takes `M_2`
to one of the same seven canonical cycle types, giving seven further CNFs.
This second normalization is used only in the shared case. The independent
audit constructs the transporter for every one of the 945 perfect matchings,
not merely the cycle-type census.

These six plus seven branches are exhaustive. Each conditioned RZP CNF is
UNSAT by its checked binary DRAT proof, so no RZP model exists at `n=10`.
The witness-to-RZP bridge proves the stated theorem.

## 3. Evidence and replay

The typed evidence manifest is
[`recursive-cancellation-consistency-evidence-2026-09-12.json`](../../../docs/strategy/recursive-cancellation-consistency-evidence-2026-09-12.json).
It pins all thirteen CNF and proof sizes and SHA-256 hashes, the normalized
encoder source, `python-sat` version, DIMACS serialization, checker source,
checker executable, and build provenance.

Primary exact replay from a POSIX shell or WSL:

```text
python tools/explore/replay_recursive_hafnian_drat.py \
  --manifest docs/strategy/recursive-cancellation-consistency-evidence-2026-09-12.json \
  --artifact-dir ARTIFACT_DIR \
  --checker /path/to/pinned/drat-trim \
  --output-dir NEW_REPLAY_DIR \
  --case-timeout-seconds 300
```

Acceptance requires exact CNF regeneration, frozen input identities, an exact
`s VERIFIED` result for every binary proof, and stable bytes during checking.
One valid-proof positive control and two semantically rejected false-proof
controls run once before the thirteen-case loop. Solver UNSAT without checked
proof bytes is not accepted.

Independent no-import audit:

```text
python claims/finite/n10/audit_recursive_hafnian_rzp_all_diagonal_exclusion.py \
  --manifest docs/strategy/recursive-cancellation-consistency-evidence-2026-09-12.json \
  --artifact-dir ARTIFACT_DIR \
  --output tmp/n10-rzp-independent-audit.json
```

The audit imports neither repository encoder code nor `python-sat`. It passed
13/13 cases on September 13, 2026, reconstructing the exact CNF bytes and
checking all proof identities. It does not implement a second DRAT checker;
proof semantics remain the pinned checker leaf.

The portable archive is deliberately outside ordinary Git history:

```text
filename = n10-all-diagonal-rzp-20260913-v2.zip
bytes  = 282243424
sha256 = 80c3a2cd5ec1d76e9b325fbc060b385198115b76d1ec78d2b4fd328b1d21fd04
```

It contains the 529,175,070 checked CNF/proof bytes, manifest, exact pinned
checker executable, checker source and Makefile, encoder/replay/audit sources,
and pinned Python requirements. A source rebuild produced a different binary
hash on the same host, so the bundle retains both source provenance and the
exact executable identity instead of silently substituting the rebuild.

Portable bundle construction:

```text
python tools/explore/build_recursive_hafnian_bundle.py \
  --manifest docs/strategy/recursive-cancellation-consistency-evidence-2026-09-12.json \
  --artifact-dir ARTIFACT_DIR \
  --checker-source-dir CHECKER_SOURCE_DIR \
  --output NEW_BUNDLE.zip
```

The unpacked v2 bundle passed its independent audit and its full thirteen-proof
portable replay. The replay receipt is 33,240 bytes with SHA-256
`41af58d23ec7f74f201af52a2e008c2a5f54ee8048ff39d13afad49f8640e807`.
The unpacked independent-audit receipt has SHA-256
`7fdfaef892ecb0880a7891cc279a3ae3496c87d253c59e8b56b084f86fa0db59`.
Within an unpacked replay directory the receipts are:

```text
replay/replay.json
independent-audit.json
```

## 4. Boundaries and proof-distance delta

- This is all-diagonal only. Mixed words cease to factorize in the presence of
  bichromatic block entries.
- It proves actual complex-witness nonexistence through the stronger necessary
  RZP model. It does not prove AP' UNSAT at `n=10`; WB2's AP' theorem remains
  scoped to `n=6,8`, and its older no-DRAT evidence gap remains separate.
- The result is finite at exactly ten vertices. It supplies no all-order
  occurrence theorem and no source-preserving reduction for general `n`.
- The thirteen branches are an exhaustive cover of selected support-matching
  normal forms, not an enumeration of weighted graphs.
- Large proof bytes remain outside ordinary Git. Distribution or publication
  is a separate owner action.

The parent obligation is exact all-diagonal weighted Bogdanov at every even
order. The upstream bridge is the all-diagonal factorization above; the named
downstream consumer is the conclusion that any full-model witness at a covered
order must contain a bichromatic block. The proof-distance delta is one closed
finite child (`n=10`) with an exhaustive certificate-backed cover. This work is
execution and independent audit of an already defined finite cover, not a
third sibling refinement. The all-order parent and global conjecture remain
open.
